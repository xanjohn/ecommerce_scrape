import redis
import json
import os
import base64


def cookies_from_redis(ecommerce):
    r = redis.Redis(
        host='localhost',
        port=6379,
        db=1,
        decode_responses=True
    )
    resp_redis = r.lpop(f"{ecommerce}_cookies")
    r.close()
    if resp_redis:
        print("[Cookies] Cookies from redis availible")
        return json.loads(resp_redis)
    else:
        print('[Cookies] No Cookies availible')
        return None

def cookies_from_local(ecommerce):
    cookies_file = f"{ecommerce}_cookies.json"
    if not os.path.exists(cookies_file):
        print(f"[Cookies] File {cookies_file} not found")
        return None
        
    with open(cookies_file, 'r') as f:
        return json.load(f)

def get_cookies(ecommerce):
    cookies_data = cookies_from_redis(ecommerce)
    if not cookies_data:
        cookies_data = cookies_from_local(ecommerce)
        if cookies_data:
            print("[Cookies] Cookies from file is ready")
    else:
        print('[Cookies] Cookies from Redis is ready')
    return cookies_data

    
def store_invalid_cookies_to_redis(ecommerce, cookies):
    r = redis.Redis(
        host='localhost',
        port=6379,
        db=1,
        decode_responses=True
    )
    invalid_key = f"{ecommerce}_invalid_cookies"
    cookies_string = json.dumps(cookies)
    r.sadd(invalid_key, cookies_string)
    print(f"[Cookies] Invalid cookies store to {invalid_key}")
    r.close()

def store_valid_cookies_to_redis(ecommerce, cookies):
    r = redis.Redis(
        host='localhost',
        port=6379,
        db=1,
        decode_responses=True
    )
    session_key = f"{ecommerce}_cookies"
    cookies_string = json.dumps(cookies)
    
    existing = r.lrange(session_key, 0, -1)
    if cookies_string not in existing:
        r.rpush(session_key, cookies_string)
        print('[Cookies] Push valid cookies to redis')
    else:
        print('[Cookies] cookies is already in queue')
    r.close()