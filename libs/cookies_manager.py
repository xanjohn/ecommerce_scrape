import redis
import json
import os
import base64


def fresh_cookies_from_redis(ecommerce):
    r = redis.Redis(
        host='localhost',
        port=6379,
        db=1,
        decode_responses=True
    )
    resp_redis = r.lpop(f"{ecommerce}_cookies")
    r.close()
    if resp_redis:
        return json.loads(resp_redis)
    else:
        print('[Cookies] No Cookies availible')
        return None
    