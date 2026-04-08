import sys
import requests
import json
import time
from time import sleep
import urllib.parse
from curl_cffi import requests
from urllib.parse import urlparse
from libs.beans import Worker, Producer
from libs.graceful_killer import GracefulKiller
from service.service_tokopedia import ServiceTokopedia
from service.service_general import store_raw

class WorkerTokopedia():
    def worker_keyword(self):
        w = Worker(tubename='tokopedia_keyword')
        p = Producer(tubename='tokopedia_keyword')
        killer = GracefulKiller()
        service = ServiceTokopedia()
        print("[*] Tokopedia Worker is active...")
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
                
                resp = service.scrape_tokped_keyword(keyword, page=current_page)   
                
                if resp.status_code == 200:
                    store_raw(
                        raw=resp.json(), 
                        platform='tokopedia', 
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
        # w = Worker(tubename='tokopedia_shop_link')
        # p = Producer(tubename='tokopedia_shop_link')
        w = Worker(tubename='test_link2')
        p = Producer(tubename='test_link2')
        killer = GracefulKiller()
        service = ServiceTokopedia()
        print("[*] Tokopedia Worker is active...")
        print("[*] Press Ctrl+C to stop.")
        while not killer.kill_now:
            job = w.getJob(timeout=5)
            
            if not job:
                sleep(10)
            else:
                try:
                    message = json.loads(job.job_data)
                    url_product = message['url_product']
                    current_page = message.get('page', 1)
                    max_page = message.get('max_page', 2)
                    
                    print(f" [+] Processing: {url_product} | Page: {current_page}")
                    
                    resp = service.scrape_tokopedia_comments(url_product, page=current_page)   
                    
                    if resp.status_code == 200:
                        store_raw(
                            raw=resp.json(), 
                            platform='tokopedia', 
                            type_data='comments', 
                            url_product=url_product, 
                            page=current_page
                        )
                        
                        w.deleteJob(job)
                        if current_page < max_page:
                            message['page'] = current_page + 1
                            p.setJob(json.dumps(message))
                            print(f" [->] Push to job {current_page + 1}")
                        else:
                            print(f" Done {url_product} already reach {max_page} max page.")
                    elif resp.status_code == 403:
                        w.releaseJob(job)   
                except Exception as e:
                    print(f" [X] Error: {e}")
                    w.buryJob(job)
                
            print(f"\n[!] Stop {killer._signal}")
        
    def worker_store(self):
        w = Worker(tubename='tokopedia_store_link')
        p = Producer(tubename='tokopedia_store_link')
        p_comment = Producer(tubename='tokopedia_product_link')
        killer = GracefulKiller()
        service = ServiceTokopedia()
        print("[*] Tokopedia Worker is active...")
        print("[*] Press Ctrl+C to stop.")
        product_url_list=[]
        while not killer.kill_now:
            job = w.getJob()
            
            if not job:
                sleep(10)
            else:
                try:
                    message = json.loads(job.job_data)
                    url_store = message['url_store']
                    current_page = message.get('page', 1)
                    max_page = message.get('max_page', 2)
                    
                    print(f" [+] Processing: {url_store} | Page: {current_page}")
                    
                    resp = service.get_shop_product(url_store, page=current_page)   
                    
                    res_json = resp.json()
                    if resp.status_code == 200:
                        first_node = res_json[0].get('data', {})
                        shop_product_node = first_node.get('GetShopProduct') 
                        items = shop_product_node.get('data', [])
                        for item in items:
                            url = item.get('product_url') 
                            product_url_list.append(url)
                            comment_job = {
                                    "url_product": url,
                                    "page": 1,
                                    "max_page": 10 
                            }
                            p_comment.setJob(json.dumps(comment_job))
                        print(f"Obtained {len(product_url_list)} Links")
                        print(product_url_list)
                        store_raw(
                            raw=resp.json(), 
                            platform='tokopedia', 
                            type_data='store', 
                            url_store=url_store, 
                            page=current_page
                        )
                        
                        w.deleteJob(job)
                        if current_page < max_page:
                            message['page'] = current_page + 1
                            p.setJob(json.dumps(message))
                            print(f" [->] Push to job {current_page + 1}")
                        else:
                            print(f" Done {url_store} already reach {max_page} max page.")
                            print('=======================================================')
                            
                    elif resp.status_code == 403:
                        w.releaseJob(job)         
                except Exception as e:
                    print(f" [X] Error: {e}")
                    w.buryJob(job)
            
        print(f"\n[!] Stop {killer._signal}")
        
