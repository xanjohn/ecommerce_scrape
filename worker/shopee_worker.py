import sys
import requests
import json
import time
import re
import urllib.parse
from curl_cffi import requests
from urllib.parse import urlparse
from libs.beans import Worker, Producer
from libs.graceful_killer import GracefulKiller
from service.service_shopee import ServiceShopee
from service.service_general import store_raw

class WorkerShopee:
    def worker_keyword(self):
        w = Worker(tubename='shopee_keyword')
        p = Producer(tubename='shopee_keyword')
        killer = GracefulKiller()
        service = ServiceShopee()
        print("[*] Shopee Worker is active...")
        print("[*] Press Ctrl+C to stop.")
        
        while not killer.kill_now:
            job = w.getJob(timeout=5)
            
            if not job:
                continue
            
            try:
                message = json.loads(job.job_data)
                keyword = message['keyword']
                current_page = message.get('page', 1)
                max_page = message.get('max_page', 2)
                
                print(f" [+] Processing: {keyword} | Page: {current_page}")
                
                resp = service.scrape_shopee_keyword(keyword, page_num=current_page)   
                
                if resp.status_code == 200:
                    store_raw(
                        raw=resp.json(), 
                        platform='shopee', 
                        type_data='keyword', 
                        keyword=keyword, 
                        page=current_page
                    )
                    
                    w.deleteJob(job)
                    if current_page < max_page:
                        message['page'] = current_page + 1
                        p.setJob(json.dumps(message))
                        print(f" [->] Push to job {current_page + 1}")
                    else:
                        print(f" Done {keyword} already reach {max_page} max page.")
                elif resp.status_code == 403:
                    w.releaseJob(job)            
            except Exception as e:
                print(f" [X] Error: {e}")
                w.buryJob(job)
            
        print(f"\n[!] Stop {killer._signal}")
    
    def worker_comments(self):
        # w = Worker(tubename='shopee_product_link')
        # p = Producer(tubename='shopee_product_link')
        w = Worker(tubename='shopee_test')
        p = Producer(tubename='shopee_test')
        killer = GracefulKiller()
        service = ServiceShopee()
        print("[*] Shopee Worker is active...")
        print("[*] Press Ctrl+C to stop.")
        while not killer.kill_now:
            job = w.getJob(timeout=5)
            
            if not job:
                continue
            try:
                message = json.loads(job.job_data)
                url_product = message['url_store']
                current_page = message.get('page', 1)
                max_page = message.get('max_page', 2)
                
                print(f" [+] Processing: {url_product} | Page: {current_page}")
                
                resp = service.scrape_shopee_comments(url_product, p=current_page)   
                
                if resp['has_review'] and resp['items']:
                    items = resp['items']
                    store_raw(
                        raw=items, 
                        platform='shopee', 
                        type_data='comments', 
                        url_product=url_product, 
                        page=current_page
                    )
                    
                    w.deleteJob(job)
                    # if current_page < max_page:
                    #     message['page'] = current_page + 1
                    #     p.setJob(json.dumps(message))
                    #     print(f" [->] Push to job {current_page + 1}")
                    # else:
                    #     print(f" Done {url_product} already reach {max_page} max page.")
                elif resp['has_review'] == False:
                    w.deleteJob(job)        
            except Exception as e:
                print(f" [X] Error: {e}")
                w.buryJob(job)
            
        print(f"\n[!] Stop {killer._signal}")
        
    def worker_store(self):
        w = Worker(tubename='shopee_store_link')
        p = Producer(tubename='shopee_store_link')
        p_comment = Producer(tubename='shopee_product_link')
        killer = GracefulKiller()
        service = ServiceShopee()
        print("[*] Shopee Worker is active...")
        print("[*] Press Ctrl+C to stop.")
        while not killer.kill_now:
            job = w.getJob(timeout=5)
            
            if not job:
                continue
            
            try:
                message = json.loads(job.job_data)
                url_store = message['url_store']
                current_page = message.get('page', 1)
                max_page = message.get('max_page', 2)
                
                print(f" [+] Processing: {url_store} | Page: {current_page-1}")
                
                resp = service.scrape_shopee_store(url_store, page_num=current_page)
                print(resp['items'])
                
                if resp['status'] == 200 and resp['items']:
                    items = resp['items']
                    # print(f'[Shopee] Get {len(items)} Data')
                    
                    product_list_link = []
                    for item in items:
                        item_id = item.get('itemid')
                        shop_id = item.get('shopid')
                        raw_name = item.get('item_card_displayed_asset', {}).get('name', '')
                        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', raw_name) # Hapus simbol
                        clean_name = clean_name.replace(' ', '-') 
                        clean_name = re.sub(r'-+', '-', clean_name).strip('-') 
                        product_url = f"https://shopee.co.id/{clean_name}-i.{shop_id}.{item_id}"
                        product_list_link.append(product_url)
                        
                        comment_job = {
                            "url_product": product_url,
                            "page": 1,
                            "max_page": 5
                        }
                        p_comment.setJob(json.dumps(comment_job))
                    
                    store_raw(
                        raw=items, 
                        platform='Shopee', 
                        type_data='store', 
                        url_store=url_store, 
                        page=current_page
                    )
                    
                    w.deleteJob(job)
                    print('[Shopee] Scraping Success')
                    print(f"Obtained {len(product_list_link)} link")

                    if current_page < max_page :
                        message['page'] = current_page + 1
                        p.setJob(json.dumps(message))
                        print(f" [->] Push to job, Page: {current_page + 1}")
                    else:
                        print(f" Done {url_store} already reach {max_page} max page.")
                elif resp['status'] == 403:
                    w.releaseJob(job)
                elif resp['items'] == None:
                    w.buryJob(job)                
            except Exception as e:
                print(f" [X] Error: {e}")
                w.buryJob(job)

        print(f"\n[!] Stop {killer._signal}")
        
if __name__ == "__main__":
    start_worker()