import sys
import json
import hashlib
import time
import re
import random
import os
import urllib.parse
from urllib.parse import urlparse
from curl_cffi import requests
from camoufox.sync_api import Camoufox


class ServiceShopee:
    def scrape_shopee_store(self, store_url, page_num):
        product_url_list = []
        url_parse = urlparse(store_url)
        store_name = url_parse.path.split('/')[-1]
        print(store_name)
        # encoded_keyword = urllib.parse.quote(keyword)
        with Camoufox(
            os=["windows", "macos", "linux"],
            # persistent_context=True,
            # user_data_dir='./shopee_session',
            headless=True,
            humanize = 2.0
        ) as browser:
            with open('shopee_cookies.json', 'r') as f:
                cookies_data = json.load(f)
            context = browser.new_context()
            context.add_cookies(cookies_data)
            page = context.new_page()
            
            extracted_data = {"items": None}
            product_link = []
            def handle_response(response):
                try:
                    if response.request.resource_type in ['fetch', 'xhr']:
                        url = response.url
                        # print(url)
                        target_api = "api/v4/shop/rcmd_items"
                        if target_api in url:
                            print(url)
                            data = response.json()
                            # print(data)
                            raw = data.get("data", {})
                            centralize_item_card = raw.get('centralize_item_card',{})
                            items = centralize_item_card.get('item_cards',[])
                            print(items)                        
                            if not items:
                                print(items)
                                print("Data Not Found")
                                return
                            extracted_data['items'] = items         
                    else:
                        pass

                except Exception as e:
                    print(f"[Shopee] Error {e}")

            page.on('response', handle_response)

            print(f"[Shopee] Open Page {page_num}")
            try:
                    print(f"[Shopee] Scraping page {page_num}")
                    url = f"https://shopee.co.id/{store_name}?page={page_num}&sortBy=pop&tab=0"
                    # url = f"https://shopee.co.id/search?keyword={encoded_keyword}&page={p}"
                    page.goto(url, wait_until="domcontentloaded")
                    page.mouse.wheel(0, 1000)
                    page.wait_for_timeout(2000)
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight / 1.5)")
                    page.wait_for_timeout(10000)
                    cookies_data = page.context.cookies()
                    with open("shopee_cookies.json", "w", encoding="utf-8") as f:
                        json.dump(cookies_data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                    print(f"Cannot access pages")
                    pass
            return extracted_data['items']

    def scrape_shopee_keyword(self, keyword, page_num):
        encoded_keyword = urllib.parse.quote(keyword)
        with Camoufox(
            os=["windows", "macos", "linux"],
            # persistent_context=True,
            # user_data_dir='./shopee_session',
            headless=True
        ) as browser:
            with open('shopee_cookies.json', 'r') as f:
                cookies_data = json.load(f)
            context = browser.new_context()
            context.add_cookies(cookies_data)
            page = context.new_page()
            
            extracted_data = {"items": None}            
            def handle_response(response):
                try:
                    if response.request.resource_type in ['fetch', 'xhr']:
                        url = response.url
                        target_api = "api/v4/search/search_items"
                        if target_api in url:
                            data = response.json()
                            print(data)
                            items = data.get("items", [])
                            if not items:
                                print("Data Not Found")
                                return
                            extracted_data['items'] = items
                    else:
                        pass

                except Exception as e:
                    print(f"[Shopee] Error {e}")

            page.on('response', handle_response)
            print(f"[Shopee] Open Page {page_num}")
            try:
                    print(f"[Shopee] Scraping page {p}")
                    url = f"https://shopee.co.id/search?keyword={encoded_keyword}&page={page_num}"
                    page.goto(url)
                    page.mouse.wheel(0, 1000)
                    page.wait_for_timeout(2000)
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight / 1.5)")
                    page.wait_for_timeout(8000)
                    cookies_data = page.context.cookies()
                    with open("shopee_cookies.json", "w", encoding="utf-8") as f:
                        json.dump(cookies_data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                    print(f"Cannot access pages")
                    pass
            return extracted_data['items']

    def scrape_shopee_comments(self, product_url, start_page):
        
        results = []
        with Camoufox(
            os=["windows","linux"],
            headless=True,
            humanize = 2.0
        ) as browser:
            with open('shopee_cookies.json', 'r') as f:
                cookies_data = json.load(f)
            context = browser.new_context()
            page = context.new_page()
            context.add_cookies(cookies_data)
            
            results = {'data': None, "has_next": True}
            # state = {'current_page': page, 'has_review': True}
            def handle_response(response):
                    if response.request.resource_type in ['fetch', 'xhr']:
                        url = response.url
                        # print(url)
                        target_api = "api/v2/item/get_ratings"
                        if target_api in url:
                            print(url)
                            data = response.json()
                            review_data = data.get('data', {})
                            # print(data)
                            product_id = data['data']['ratings'][0]['itemid']
                            if not review_data:
                                print("Review Not Found")
                                state['has_review'] = False
                                return
                            

            page.on('response', handle_response)
                    
            time_out = random.randint(3000, 6000)
            print("Navigating...")
            page.goto(product_url, wait_until="domcontentloaded")
            with open("shopee_cookies.json", "w", encoding="utf-8") as f:
                json.dump(cookies_data, f, indent=2, ensure_ascii=False)            
            
            for _ in range(2):
                print(f"Pressing arrow down")
                page.keyboard.press("PageDown")
                print(f"Waiting For {time_out}")
                page.wait_for_timeout(time_out)
                
            # end_page = start_page + 1
            
            # for p in range(2, max_pages + 1):
                if not state['has_review']:
                    break
                state['current_page'] = p
                for _ in range(2):
                    print(f"Pressing arrow down")
                    page.keyboard.press("PageDown")
                    print(f"Waiting For {time_out}")
                    page.wait_for_timeout(time_out)
                    
                page.locator(f"button.shopee-button-no-outline:has-text('{p}')").dispatch_event("click")
                page.wait_for_timeout(time_out)
