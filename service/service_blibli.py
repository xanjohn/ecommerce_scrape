import json
import time
import urllib.parse
import os
import random
from curl_cffi import requests
from urllib.parse import urlparse
import sys


class ServiceBlibli:
    def __init__(self):
        proxy_url = "http://bandung:456xyz@proxycrawler.dashboard.nolimit.id:2570"
        self.proxies = {"http": proxy_url, "https": proxy_url}
    
    def scrape_blibli_keyword(self, keyword, page):
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://www.blibli.com/cari/{encoded_keyword}"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.6",
            "content-type": "application/json",
            "if-modified-since": "Fri, 20 Feb 2026 04:02:45 GMT",
            "priority": "u=1, i",
            "referer": f"https://www.blibli.com/cari/{encoded_keyword}",
            "sec-ch-ua": '"Not:A-Brand";v="99", "Brave";v="145", "Chromium";v="145"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        }
        base_api_url = "https://www.blibli.com/backend/search/products"
        query_params = {
            "searchTerm": keyword,
            "page": page,
            "start": (page - 1) * 40, 
            "merchantSearch": "true",
            "multiCategory": "true",
            "channelId": "mobile-web", 
            "itemPerPage": 40
            }
        print(f"[Blibli] Scraping keyword ({encoded_keyword}) from Blibli, Page {page}")
        resp = requests.get(base_api_url, params=query_params, impersonate="chrome110", headers=headers, proxies=self.proxies)
        return resp


    def scrape_blibli_comments(self, product_url, page):
        path = urlparse(product_url).path 
        last_part = path.split('/')[-1] 

        product_id = last_part.replace("is--", "").rsplit("-", 1)[0]
        print(f"{product_id}")
        

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.6",
            "content-type": "application/json",
            # "if-modified-since": "Fri, 20 Feb 2026 04:02:45 GMT",
            "priority": "u=1, i",
            "referer": f"{product_url}",
            "sec-ch-ua": '"Not:A-Brand";v="99", "Brave";v="145", "Chromium";v="145"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        }
        print(f"💬 [Blibli] Memproses ID: {product_id} | Page: {page}")
        api_url = f"https://www.blibli.com/backend/product-review/public-reviews?itemPerPage=5&page={page}&hasMedia=true&productSku={product_id}"
        resp = requests.get(api_url, headers=headers, impersonate="chrome110", proxies=self.proxies)
            
        return resp
    
    def scrape_blibli_store(self, url_brand, page):
        product_url_list = []
        path = urlparse(url_brand).path
        brand_name = path.strip('/').split('/')[-1]
        encoded_brand = urllib.parse.quote(brand_name)    
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "referer": f"https://www.blibli.com/brand/{encoded_brand}",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        start_index = (page - 1) * 40
        print(f"💬 [Blibli] Memproses Brand: {brand_name} | Page: {page}")
        base_api_url = f"https://www.blibli.com/backend/search/brand/{brand_name}?promoTab=false&excludeProductList=false&page={page}&start=40&intent=false&multiCategory=true&showFacet=false"
        query_params = {
                    "promoTab": "false",
                    "excludeProductList": "false",
                    "page": page,
                    "start": start_index,
                    "intent": "false",
                    "multiCategory": "true",
                    "showFacet": "false",
                    "brandSearch": "false"
        }
        resp = requests.get(base_api_url, params=query_params, impersonate="chrome110", headers=headers, proxies=self.proxies)
                    
        return resp