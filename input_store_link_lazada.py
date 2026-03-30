import sys
import json
from libs.beans import Producer

def seed_store(url):
    p = Producer(tubename='lazada_store_link')
    
    payload = {
        "url_store": url,
        "page": 1,
        "max_page": 5
    }
    
    p.setJob(json.dumps(payload))
    print(f"Seed Inputed: {url}")
    

if __name__ == "__main__":
    seed_store(sys.argv[1])