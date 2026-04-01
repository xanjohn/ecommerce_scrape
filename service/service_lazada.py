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
                print(f" [Attempt {attempt+1}] Requesting Page {page}...")
                resp = requests.post(api_url, data=payload, headers=headers, impersonate="chrome110")
                last_resp = resp
                if resp.status_code == 200:
                    data = resp.json()
                    print(data)
                    ret_list = data.get("ret", [])
                    ret_status = str(ret_list)
                    if "FAIL_SYS" in ret_status or "RGV587_ERROR" in ret_status:
                        print("FAIL_SYS or Captcha detected")
                        print(f"Attempt {attempt+1}: {time_sleep:.2f}s...")
                        time.sleep(time_sleep)
                        continue 
                    
                    if "SUCCESS" in ret_status:
                        return resp 
                    
                    return resp
                else:
                    print(f"{resp.status_code} in {attempt+1}. Retrying")
                    time.sleep(time_sleep)
                
            except Exception as e:
                print(f" [!] Connection Error: {e}")
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
        product_url_list = []
        with open('lazada_cookies.json', 'r') as f:
            cookies_data = json.load(f)
        path = urlparse(shop_url).path
        shop_name = path.split('/')[-1]
        proxy_url = "http://bandung:456xyz@proxycrawler.dashboard.nolimit.id:2570"
        proxies = {"http": proxy_url, "https": proxy_url}
        cookies = self.get_cookies_data('lazada_cookies.json')
        
        print(f"[Lazada] Scraping shop ({shop_name}) from Lazada, Page {page}")
        api_url = f"https://www.lazada.co.id/{shop_name}/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=id&page={page}&pageTypeId=2&q=All-Products"
        payload = {}
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=1, i',
            'referer': 'https://www.lazada.co.id/',
            'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
            #   'Cookie': cookies
            'Cookie': '__wpkreporterwid_=da27ce1d-fb2b-4abb-841f-e09c65358ae5; t_fv=1772588276894; t_uid=fnsiN5sL2N1m47Kq9zkUoFhd6yaw2TOr; userLanguageML=id; lwrid=AgGctn6dCfndDFv7q5wXX39uI%2FEO; lzd_cid=c33115fd-0207-49d3-b363-9bb9ae1977ca; lzd_sid=1882f651c945e6e2fb05b473b41a6c8d; _tb_token_=7e94f73be55e3; cna=DXsuIh9VuH8CAWeqH2DbHFPF; lwrtk=AAIEaaf9dWDmQdCakUrspqy598ffqjcJysbX4f0If5rg0HLUKE1z1OE=; xlly_s=1; hng=ID|id-ID|IDR|360; hng.sig=to18pG508Hzz7EPB_okhuQu8kDUP3TDmLlnu4IbIOY8; EGG_SESS=S_Gs1wHo9OvRHCMp98md7N0Cls3SvdIH7XYfllZh6Yz7634O4Q6xh2j3wpJWnk9UM8dbjAdbgQMmAFyk_jSzlZ8D4K07_gpKRZHpxYBrAHZktY1zbk6DvOkWv8V823hIRAc4k-VpM5iwdc67qg9knKT0SrsG_LuxWnrzFbaoJPw=; undefined_click_time=1772588341693; _m_h5_tk=a613d288a40ef89555bb81c9717385e3_1772614928889; _m_h5_tk_enc=cd414853f9d2a916a8ca7cb2319d9da3; t_sid=rMdeUU94681gH6VG4cQbFTH1a3XY3LXL; utm_channel=NA; _bl_uid=0bmdame1bhzmvFxOnj8g6v9xwv6O; _gcl_au=1.1.1459322457.1772604466; _ga=GA1.3.1128913782.1772604467; _gid=GA1.3.1310077654.1772604467; _gat_UA-29801013-1=1; _fbp=fb.2.1772604466837.394077540194083574; AMCVS_126E248D54200F960A4C98C6%40AdobeOrg=1; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C20517%7CMCMID%7C33933849864538145223333802798903367954%7CMCAAMLH-1773209267%7C3%7CMCAAMB-1773209267%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1772611667s%7CNONE%7CvVersion%7C5.2.0; _uetsid=775c1a80179011f197fe61394aeb2e77; _uetvid=775c5de0179011f1ac1b2727d055ce8b; _ga_44FMGEPY40=GS2.3.s1772604466$o1$g1$t1772604488$j38$l0$h0; isg=BF9fYFu5SrFxGU6tLe51hpbN7rPpxLNm0h7-XfGs_o5VgH8C-ZVXttZTQgj-cIve; epssw=11*mmLDomob3X6igEbg3uflcJ0lguKQrYcnl0S4k_Xu5l-EXiFNip12pMAq-tyDC2sgUSF10XT1yQwo3ImmEOyGQiAx3temmWTiLOAZSBDodjZszrlFEVLS2UEB2cXZD8Eruj6HROAZmTH_DtVMjDi1KGcunDK9Ln_uzDL0fRqDZ0I-OfbmFMvwERTTmCcncJA8iojmNREBP8JEmmHuuuCr1_UbuUkbiaHuu0ulnRmmCvgeRAYSB_EEEmNVVjEmBjQplI8aBjPYNBBmEmEYNBmmV5-uFuuFB5kyxmjmbiNVhgnO12acd15voTEmBB..; tfstk=gcUIL9xbNpvQDX5dep5whFLRp037P17VAQG8i7Lew23peLFxQ45H4McSPAwoL0EFERM8KRDrpvzUPB4_hU8FKMVJP4uR3t7VuWfnr4B24vDE4vcu6YCZvdBl0g0R3t7a5KAjG4FUB-mnW5HiNbdKv8H9XAcDv4HK2dKtwAH-y8HpBdhENLpJv4HO1bDte4nKw1NtIbg-e83R15haBOGGAvFCNS0PivR_CWH6yUUdxDMb138JyyhIAveKCWNQ5XiIH0_UW6aLQ7UU-cjk44Vac8Z8BNTQFWEYevzOHUMzmbN-Gqd2y5NxNm3-fQL812HiXygAkdGgXWr8-JOWyX4Uu0Mmf_Lo4VUqDoeBZsVtJbeomzWD-vF8irqqlaTtR0IPQEkXRTxW1mY-1x5113xooXNxF6xjlaoKsfzV119BqDhi1x5113xovfcZ0116d3f..'
            # 'Cookie': ''
        } 
        resp = requests.get(api_url, impersonate="chrome110", headers=headers)
        return resp
        # return items