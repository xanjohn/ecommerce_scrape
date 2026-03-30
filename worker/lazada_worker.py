import sys
import requests
import json
import time
import urllib.parse
from curl_cffi import requests
from urllib.parse import urlparse
from libs.beans import Worker, Producer
from libs.graceful_killer import GracefulKiller
from service.service_lazada import ServiceLazada
from service.service_general import store_raw

class WorkerLazada():
    def worker_keyword(self):
        w = Worker(tubename='lazada_keyword')
        p = Producer(tubename='lazada_keyword')
        killer = GracefulKiller()
        service = ServiceLazada()
        print("[*] Lazada Worker is active...")
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
                
                resp = service.scrape_lazada_keyword(keyword, page=current_page)   
                
                if resp.status_code == 200:
                    store_raw(
                        raw=resp.json(), 
                        platform='Lazada', 
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
        w = Worker(tubename='lazada_link_product')
        p = Producer(tubename='lazada_comment')
        killer = GracefulKiller()
        service = ServiceLazada()
        print("[*] Lazada Worker is active...")
        print("[*] Press Ctrl+C to stop.")
        while not killer.kill_now:
            job = w.getJob(timeout=100)
            if not job:
                continue
            
            try:
                message = json.loads(job.job_data)
                url_product = message['url_product']
                current_page = message.get('page', 1)
                max_page = message.get('max_page', 2)
                
                print(f" [+] Processing: {url_product} | Page: {current_page}")
                
                resp = service.scrape_lazada_comments(url_product, page=current_page)   
                
                if resp.status_code == 200:
                    data = resp.json()
                    if "FAIL_SYS" in str(data.get("ret", [])):
                        print(f" [!] Job Released: Error Captcha")
                        w.releaseJob(job, delay=60)
                    else:
                        store_raw(
                            raw=data, 
                            platform='lazada', 
                            type_data='comments', 
                            url_product=url_product, 
                            page=current_page
                        )
                        
                        w.deleteJob(job)
                        
                        with open(f"comment_lazada_{url_product}_{current_page}.json", "w") as file:
                            json.dump(data, file)
                        
                        should_stop = getattr(resp, 'stop_pagination', False)
                        
                        if current_page < max_page and should_stop == False:
                            message['page'] = current_page + 1
                            p.setJob(json.dumps(message))
                            print(f" [->] Push to job {current_page + 1}")
                        else:
                            print(f" Done {url_product} already reach {max_page} max page.")
                else:
                    w.buryJob(job)       
            except Exception as e:
                print(f" [X] Error: {e}")
                w.buryJob(job)
            
        print(f"\n[!] Stop {killer._signal}")
        
    def worker_store(self):
        w = Worker(tubename='lazada_store_link')
        p = Producer(tubename='lazada_store')
        p_page = Producer(tubename='lazada_store_link')
        killer = GracefulKiller()
        service = ServiceLazada()
        print("[*] Lazada Worker is active...")
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
                
                print(f" [+] Processing: {url_store} | Page: {current_page}")
                
                resp = service.scrape_lazada_store(url_store, page=current_page)   
                print(resp)
                all_links = []
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get('mods', {}).get('listItems', [])
    
                    p_comment = Producer(tubename='lazada_link_product')
                    
                    if not items:
                        print(f"No Product Found in page {current_page}")
                        w.deleteJob(job)
                        continue
                    
                    for item in items:
                        raw_url = item.get('itemUrl')
                        if raw_url:
                            clean_url = f"https:{raw_url}" if raw_url.startswith('//') else raw_url
                            comment_job = {
                                "url_product": clean_url,
                                "page": 1,
                                "max_page": 10 
                            }
                            all_links.append(clean_url)
                            p_comment.setJob(json.dumps(comment_job))
                            print(f" [->] Pushed product to comment queue: {clean_url}")
                            
                    print(f"Obtained {len(all_links)} Links")
                    print(all_links)
                    
                    w.deleteJob(job)
                    if current_page < max_page:
                        message['page'] = current_page + 1
                        p_page.setJob(json.dumps(message))
                        print(f" [->] Push to job {current_page + 1}")
                    else:
                        print(f" Done {url_store} already reach {max_page} max page.")
                elif resp.status_code == 403:
                    w.buryJob(job)       
            except Exception as e:
                print(f" [X] Error: {e}")
                w.buryJob(job)
            
        print(f"\n[!] Stop {killer._signal}")
        
# if __name__ == "__main__":
#     start_worker()