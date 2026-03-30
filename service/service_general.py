import json
import os

def store_raw(raw, platform, type_data, **kwargs):
    page = kwargs.get('page', 1)
    shop_name = kwargs.get('shop_name', 'general')
    keyword = kwargs.get('keyword', 'no_keyword')
    product_id = kwargs.get('product_id', 'no_id')

    base_dir = "ScrapeData"
    target_dir = os.path.join(base_dir, platform, type_data)
    
    if type_data == 'product':
        target_dir = os.path.join(target_dir, shop_name.replace(' ', '_'))
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if type_data == 'keyword':
        filename = f"{platform}_{keyword.replace(' ', '_')}_page_{page}.json"
    elif type_data == 'comment':
        filename = f"{platform}_comment_{product_id}_page_{page}.json"
    else:
        filename = f"{platform}_{shop_name.replace(' ', '_')}_page_{page}.json"

    output = {
        "raw": raw,
        "metadata": kwargs 
    }
    output["metadata"]["platform"] = platform

    full_path = os.path.join(target_dir, filename)
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully saved {type_data} to: {full_path}")