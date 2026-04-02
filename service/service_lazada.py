import sys
import requests
import json
import time
import urllib.parse
import hashlib
import re
from urllib.parse import urlparse
from curl_cffi import requests
import random
import os
import json
from playwright.sync_api import sync_playwright
from libs.cookies_manager import get_cookies


class ServiceLazada:
    def __init__(self):
        proxy_url = "http://bandung:456xyz@proxycrawler.dashboard.nolimit.id:2570"
        self.proxies = {"http": proxy_url, "https": proxy_url}
                
    def get_cookies_data(self, cookies_file):
        cookies_dict = {c['name']: c['value'] for c in cookies_file}
        
        cookies_string = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
        
        token = cookies_dict.get('_m_h5_tk', '').split('_')[0]
        return token, cookies_string
    
    def generate_lazada_sign(self, token, timestamp, app_key, data_json):
        raw_string = f"{token}&{timestamp}&{app_key}&{data_json}"
        return hashlib.md5(raw_string.encode('utf-8')).hexdigest()

    def extract_item_id_lazada(self, url):
        match = re.search(r'i(\d+)(?:-|\.)', url)
        if match:
            return match.group(1)
        return None
            
    def scrape_lazada_comments(self, product_url, page, cookies_redis):
        # self.extract_cookies_lazada()
        # cookies_redis = get_cookies('lazada')
        item_id = self.extract_item_id_lazada(product_url)
        token, cookies = self.get_cookies_data(cookies_redis)
        token_from_cookies = token
        cookies_full = cookies
        app_key = 24677475
        comment_data = {
                "itemId": item_id, 
                "pageSize": 5,
                "pageNo": page,
                "ratingFilter": 0,
                "sort": 1,
                "tagId": 0
        }
        max_retries = 3
        last_resp = None
        data_string = json.dumps(comment_data, separators=(',', ':'))
        
        for attempt in range(max_retries):
            timestamp = str(int(time.time() * 1000))
            sign = self.generate_lazada_sign(token_from_cookies, timestamp, app_key, data_string)
            api_url = (
                    f"https://acs-m.lazada.co.id/h5/mtop.lazada.review.item.getpcreviewlist/1.0/?"
                    f"jsv=2.7.2&appKey={app_key}&t={timestamp}&sign={sign}&"
                    f"api=mtop.lazada.review.item.getPcReviewList&v=1.0&type=originaljson&"
                    f"isSec=1&AntiCreep=true&timeout=10000&dataType=json&sessionOption=AutoLoginOnly&"
                    f"x-i18n-language=id&x-i18n-regionID=ID"
            )
            payload = {"data": data_string}
            headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                    "Referer": "https://www.lazada.co.id/",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Cookie": cookies_full
            }
            
            time_sleep = random.uniform(3, 7)
            
            try:
                print(f" [Service Lazada] [Attempt {attempt+1}] Requesting Page {page}...")
                resp = requests.post(api_url, data=payload, headers=headers, impersonate="chrome110")
                last_resp = resp
                if resp.status_code == 200:
                    data = resp.json()
                    print(data)
                    ret_list = data.get("ret", [])
                    ret_status = str(ret_list)
                    if "FAIL_SYS" in ret_status or "RGV587_ERROR" in ret_status:
                        print("FAIL_SYS or Captcha detected")
                        print(f"[Service Lazada] Attempt {attempt+1}: {time_sleep:.2f}s...")
                        time.sleep(time_sleep)
                        continue 
                    
                    if "SUCCESS" in ret_status:
                        return resp 
                    
                    return resp
                else:
                    print(f"{resp.status_code} in {attempt+1}. Retrying")
                    time.sleep(time_sleep)
                
            except Exception as e:
                print(f" [Service Lazada] [!] Connection Error: {e}")
                time.sleep(random.uniform(2, 5))
        
        return last_resp
    
    def scrape_lazada_keyword(self, keyword, page):
        encoded_keyword = urllib.parse.quote(keyword)
        token, cookies = self.get_cookies_data('lazada_cookies.json')
        print(f"[Lazada] Scraping keyword ({encoded_keyword}) from Lazada, Page {page}")
        api_url = f"https://www.lazada.co.id/catalog/?ajax=true&isFirstRequest=true&page={page}&q={encoded_keyword}"
        headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                    # "Cookie": cookies
                    'Cookie': '__wpkreporterwid_=d0f62c5e-1eff-45c7-a4ab-99abc4067d72; miidlaz=miidgl3vcs1j90s7lepr44k; t_fv=1762039933572; t_uid=zZK4vjlaQojkbsmlB4FiUOdoVtyHCIJW; lwrid=AgGaQcOrAVp%2ByGA3cSsLX39uI5Qx; lzd_cid=f6e5d77d-06a4-4e85-b04d-87f843e91374; lzd_click_id=clkgg5vbk1j9qnl02145te; userLanguageML=id; hng=ID|id-ID|IDR|360; hng.sig=to18pG508Hzz7EPB_okhuQu8kDUP3TDmLlnu4IbIOY8; __itrace_wid=77f6df93-7f39-4af5-a9e3-cbb122738a57; _bl_uid=89mb9m9db2zfdFf3sc7I2qp0pI4b; isg=BJ2dpYoCqJucoUwWV2-hflw4rHmXutEMxOh8519ih_Q0FrxIJgol3FRFRBIQ1unE; EGG_SESS=S_Gs1wHo9OvRHCMp98md7FWq2FVz6tfLS6v06vH8sU3TszpGTwbRo6nHqPpFkgsQCStxu4jWAS-7kzknCdEr1G6hGL4UM99uZqMKuY7JPknB5vGsqtko5yOOsyWWlOYkEzsiGuenBVQqcEorlFbfL40JoN_Yt8t2OI5OKgSoyVY=; lwrtk=AAIEabF19dqIzmdElvkeaBwjWHkeLmzLBETS7iMLF/N2Xqzy/DHRjFQ=; tfstk=gkWqpWOeS-eqno4hYMvaL8nbH2vvKdzI0OT6jGjMcEYmhxgGaaQZfoUTM_8NrUsfCKXNwASdXtZvCopADdpgRywN7iIvBCE8VfXqZYxFqhcMi79uZ5uM8ywQdijcSBq3RsOoHNxMjdxDohmu4H-6jdAMoYqyjhgmsxbGqu8JxnDMSdAorHxemdvGSgqycHpMSNA04gYJjdYisW1f1b-Hio4Os7L0lLd2-iYrLwBym9hA0UuSyT5P2eXwzADGznjgb10nL5Th9EOBla2S3dSkbw-Fu44yIgWALQX0yARR7UdNUQyz8gWwuBXDaDHOVgKGSC588vt2h_RF3sEtribBu6vAfDzf4B5y93AobjvfOM69tt2qJUOpbw-FuqSPPVKuEJB9a_cwi3KyRurrjq5wmYzeAyGt6QYe4eZvkfh9inxyRurr6fdja38QDlC..; t_sid=qHhRHSf1dNRuFJGmEqYCfUXeI7Xwjt3K; utm_channel=NA; lzd_sid=1a155993d3bc8c1325584cea19cdf084; _tb_token_=e53a4eeb3bb00; _m_h5_tk=bfbcbf01793f2988f92e4804b624482e_1773228014832; _m_h5_tk_enc=562c65c92d4495c41b983545a02e9d66; clkgg5vbk1j9qnl02145te_click_time=1773220090414; epssw=11*mmLhKmqm2XZ3gRAzEN0dWhn0WnCLtJjGuiSfY5WWXLxtyzI0S_1fgC6ktyncmuZ-REQJ1rT1po8kc5fvEOMBUmA4Y43vQRAx3fjWQiAxpEAQe5kF7LOUhX_YW-Aur6a3mDRkz1BMammmmCHKxt_U1DRsVGymNtV3M8H4KtnDijDcQJXP4h0u5paWzyFCzucniWvMnepqPaNBP8JE1_7C1zWmuuMCtnkbiammmmXmSRmmqeam7D7tStF3fDv0NRemfDZJuw8aEmNEBBBmBjaYNtym2PmemvgEuu7nEHLxaYIJhXMJf-N8mvfa'

        }      
        resp = requests.get(api_url, impersonate="chrome110", headers=headers)
        return resp
                
    
    def scrape_lazada_store(self, shop_url, page):
        # product_url_list = []
        # with open('lazada_cookies.json', 'r') as f:
        #     cookies_data = json.load(f)
        path = urlparse(shop_url).path
        shop_name = path.split('/')[-1]
        proxy_url = "http://bandung:456xyz@proxycrawler.dashboard.nolimit.id:2570"
        proxies = {"http": proxy_url, "https": proxy_url}
        # cookies = self.get_cookies_data('lazada_cookies.json')
        
        print(f"[Lazada] Scraping product from store ({shop_name}), Page {page}")
        api_url = f"https://www.lazada.co.id/{shop_name}/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=id&page={page}&pageTypeId=2&q=All-Products"
        payload = {}
        headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=1, i',
        'referer': 'https://www.lazada.co.id/',
        'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'x-csrf-token': 'f317f51e157ee',
        'Cookie': '__wpkreporterwid_=02631038-e686-4dcf-1e45-963bf0e95d2e; lzd_cid=6c61c345-5d0e-448c-80be-855661eb8483; lwrid=AgGdQxkMlgpNCTBxquNeX39uI7qt; userLanguageML=id; _bl_uid=dzm71n7wey5d9eq99os86XpsUnab; t_fv=1774947209943; t_uid=G5psM9RjveC5ObhNHfUagzwLIjqaP0YB; xlly_s=1; cna=jHlSIlFNdGgCAbb9+u+KOuWV; _gcl_au=1.1.1920824345.1774947210; _ga=GA1.3.1324004323.1774947211; _fbp=fb.2.1774947211615.25591898649954003; lzd_sid=16586375d7a9168994d622115bb938cc; _tb_token_=f317f51e157ee; undefined_click_time=1775111905692; lwrtk=AAIEac5/YSObKRLwTAEpWTNwDJbItPTzfcY1YT5EJk2mUEEGie/9Krw=; t_sid=OLshLSrBTcWcd5EZHSKzGcvsJbygwAmD; utm_channel=NA; _m_h5_tk=ca955e520455adb7febcec7e1a4ed612_1775119831152; _m_h5_tk_enc=94a531cb353e80b1b22c5ac2ba05aa68; hng=ID|id-ID|IDR|360; hng.sig=to18pG508Hzz7EPB_okhuQu8kDUP3TDmLlnu4IbIOY8; EGG_SESS=S_Gs1wHo9OvRHCMp98md7CXpHQ05eSuwQd-wSkDjjIh6uQCRoYb0bdyVgjdluDfMvMmW2ak8PM7Lu5PPbo_JfWhhHAkw6ECTjk3Y8zeikas08HGkJQPBXoyenLVdisR4wF4ZzDc0FjmcGuKqIvFu12x6gNGPJYbgwZCJb3jn9CI=; _gid=GA1.3.1848751026.1775113268; _gat_UA-29801013-1=1; AMCVS_126E248D54200F960A4C98C6%40AdobeOrg=1; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C20546%7CMCMID%7C28013983688099196300847155555133644639%7CMCAAMLH-1775718068%7C3%7CMCAAMB-1775718068%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1775120468s%7CNONE%7CvVersion%7C5.2.0; _uetsid=b9b982d02e6111f18fea0fa73ee7eaf5; _uetvid=17fe69502cdf11f184e759fbc941ac50; _ga_44FMGEPY40=GS2.3.s1775113268$o2$g1$t1775113312$j16$l0$h0; isg=BJWVwRxbUBqXknTjDGEjyJRApJFPkkmkONkTcBc6I4wcbrRg3-K6dYItOGpYtmFc; epssw=12*n8vyL0BGGI60-0LzV-_lEUT0Gtrzml3SqQ_Ymw_a95LzljohMFczlGGIMFvhML53rjcnplIGGbS3miDjNcjSQT7wjYsLD3jOt0OMWieMj_UVfC8pc-s9P73pFNBajwm7AgVmmyMjBZE6XqOWgVkDq046jGJGMPetRGIGuRnh-zz9uO0YXRFKjwItUhIfgRDO7eUqCjPw461ie0zLesCMIGGGGrbHsL14IMeisk8gwl5n3GrGGMEvGGGIjmlNAJIOabziSNvtSsiRaTptJ6s1D3xw7GrOtIbN_zmqaLTj-13vt3jpHM07jEfRSVF6rzE8XMrOJw92MQYrqlzR-6jrhw..; tfstk=gYwmX-OOGSlbWVLPKFkfw87-qtCJkxMsJPptWA3Na4uWkEpYbGDgmP2Ocl7bS74Y8qJYBxEarP4hfSUOGV4oh8FvBqQjIlzKIwQdp9EbqYMNJwhJqZx-LcnwuFhw4TktjOsEcvqbcAt7rzwEbo6MEXytbAzZU4oj0ARqgKSoacotQKlw3QurPckZQju2ULoEAnowgfSu44iZQVzZQgDrPckZ7PkZ_iCqlRyzUwPHGEVtNcwomj0UqT9wImpKg2rqrd-rombZ8ouk7F0eX1QzqoQDduHbHymLkTJ0-oPU7WzPEKc7gu2iORTV4AlZPfe47ERqxx0mT-lyvLEr_72oH-76OuEouXD8w__x6x40O2GVNaagqqUanb8cyVFL2-lu8apu5fV4o0kF4SAyTzPHC0STUCOsg0ioJ6Hcsr6oMTSNqgAFfjoSc2IlqCOsg0ioJgjkTOGqVmgd.; _m_h5_tk=2c33210b5ff997e95317c977a013415e_1774798785044; _m_h5_tk_enc=5e913bb7b8e453b4f5be8f0d65ffe775; x5secdata=xg5709c1ea87fc5033naeab76b6ef1eff53e4f68aa9969a762b01775113420a1984346082a-2092571265abaxc3dajrecaptcha33b17c35bca214dd6a4b30f5f2434efd6c9__bx__www.lazada.co.id:443/bebelac; x5sectag=195562'
        } 
        resp = requests.get(api_url, impersonate="chrome110", headers=headers)
        return resp
        # return items

