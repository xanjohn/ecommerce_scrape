import argparse
# Import Class dari file worker kamu
from worker.shopee_worker import WorkerShopee 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tokopedia Worker Control Center')
    parser.add_argument('-m', '--mode', type=str, required=True,
                        choices=['keyword', 'comments', 'store'], 
                        help='Pilih jenis worker yang mau dijalankan')

    args = parser.parse_args()
    
    # Buat instance/objek dari Class
    worker = WorkerShopee()

    if args.mode == 'keyword':
        worker.worker_keyword()
        
    elif args.mode == 'comments':
        worker.worker_comments()
        
    elif args.mode == 'store':
        worker.worker_store()