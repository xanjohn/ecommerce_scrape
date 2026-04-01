from camoufox.sync_api import Camoufox
import json
import redis


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


with Camoufox(
    os=["windows", "macos", "linux"],
    headless=False             
) as browser:
    page = browser.new_page()
    page.goto("https://shopee.co.id/buyer/login")
    
    # cookies = page.context.cookies()  

    print("Login From Browser")
    page.wait_for_event('close', timeout=0)
    cookies_list = page.context.cookies()
    
    store_cookies_to_redis('shopee', cookies_list)
    print(cookies_list)
    with open("shopee_cookies.json", "w", encoding="utf-8") as f:
        json.dump(cookies_list, f, indent=2, ensure_ascii=False)
    print("Browser Close")
    print("Saved Cookies to Redis")
    
    
    