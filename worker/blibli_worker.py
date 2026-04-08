import sys
import requests
import json
import time
import urllib.parse
from curl_cffi import requests
from urllib.parse import urlparse
from libs.beans import Worker, Producer
from libs.graceful_killer import GracefulKiller
from service.service_blibli import ServiceBlibli
from service.service_general import store_raw

class WorkerBlibli():
    def worker_keyword(self):
        w = Worker(tubename='blibli_keyword')
        p = Producer(tubename='blibli_keyword')
        killer = GracefulKiller()
        service = ServiceBlibli()
        print("[*] Blibli Worker is active...")
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
                
                print(f" [Blibli] Processing: {keyword} | Page: {current_page}")
                
                resp = service.scrape_blibli_keyword(keyword, page=current_page)   
                
                if resp.status_code == 200:
                    store_raw(
                        raw=resp.json(), 
                        platform='blibli', 
                        type_data='keyword', 
                        keyword=keyword, 
                        page=current_page
                    )
                    
                    w.deleteJob(job)
                    if current_page < max_page:
                        message['page'] = current_page + 1
                        p.setJob(json.dumps(message))
                        print(f" [Blibli] Push to job {current_page + 1}")
                    else:
                        print(f" Done {keyword} already reach {max_page} max page.")
                elif resp.status_code == 403:
                    w.releaseJob(job)                      
            except Exception as e:
                print(f" [Blibli] Error: {e}")
                w.buryJob(job)
            
        print(f"\n[Blibli] Stop {killer._signal}")
    
    def worker_comments(self):
        # w = Worker(tubename='blibli_comment')
        # p = Producer(tubename='blibli_comment')
        w = Worker(tubename='test_link_blibli')
        p = Producer(tubename='test_link_blibli')
        killer = GracefulKiller()
        service = ServiceBlibli()
        print("[*] blibli Worker is active...")
        print("[*] Press Ctrl+C to stop.")
        while not killer.kill_now:
            job = w.getJob(timeout=5)
            
            if not job:
                continue
            
            try:
                message = json.loads(job.job_data)
                url_product = message['url_product']
                current_page = message.get('page', 1)
                max_page = message.get('max_page', 2)
                
                print(f" [+] Processing: {url_product} | Page: {current_page}")
                
                resp = service.scrape_blibli_comments(url_product, page=current_page)   
                
                if resp.status_code == 200:
                    store_raw(
                        raw=resp.json(), 
                        platform='blibli', 
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
        w = Worker(tubename='blibli_store_link')
        p = Producer(tubename='blibli_store_link')
        p_comment = Producer(tubename='blibli_product_link')
        killer = GracefulKiller()
        service = ServiceBlibli()
        print("[*] blibli Worker is active...")
        print("[*] Press Ctrl+C to stop.")
        product_url_list = []
        while not killer.kill_now:
            job = w.getJob(timeout=5)
            
            if not job:
                continue
            
            try:
                message = json.loads(job.job_data)
                url_store = message['url_store']
                current_page = message.get('page', 1)
                max_page = message.get('max_page', 2)
                
                print(f" [+] Processing: {url_store} | Page: {current_page}")
                
                resp = service.scrape_blibli_store(url_store, page=current_page)   
                
                if resp.status_code == 200:
                    res_json = resp.json()
                    data_products = res_json.get('data', {}).get('products', [])
                    if not data_products:
                        print(f" [!] Page {current_page} is empty")
                        w.deleteJob(job)
                        continue
                    for product in data_products:
                        relative_url = product.get('url', '')
                        if relative_url:
                            clean_url = f"https://www.blibli.com{relative_url}"
                            product_url_list.append(clean_url)
                            comment_job = {
                                "url_product": clean_url,
                                "page": 1,
                                "max_page": 10 
                            }
                            p_comment.setJob(json.dumps(comment_job))
                            print(f" [->] Pushed product to comment queue: {clean_url}")
                    print(f"Obtained {len(product_url_list)} url")
                    print(product_url_list)
                    store_raw(
                        raw=resp.json(), 
                        platform='blibli', 
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
                elif resp.status_code == 403:
                    w.releaseJob(job)
            except Exception as e:
                print(f" [X] Error: {e}")
                w.buryJob(job)
            
        print(f"\n[!] Stop {killer._signal}")
        
