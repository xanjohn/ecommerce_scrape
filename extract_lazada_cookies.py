import json
import redis
from playwright.sync_api import sync_playwright

def store_cookies_to_redis(ecommerce, cookies, ttl=43200):
    r = redis.Redis(
        host='localhost',
        port=6379,
        db=1,
        decode_responses=True
    )
    session_key = f"{ecommerce}_cookies"
    cookies_string = json.dumps(cookies)
    r.rpush(session_key, cookies_string)
    

with sync_playwright() as p:
    browser = p.chromium.launch(headless= True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.lazada.co.id/")
    
    cookies = context.cookies()
    store_cookies_to_redis("lazada", cookies, 43200)
    print(cookies)
    print("Saved to redis")
    #Save Cookies
    # with open("lazada_cookies.json", "w") as f:
    #     json.dump(cookies, f, indent=4)
        