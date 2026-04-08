import argparse
from worker.tokopedia_worker import WorkerTokopedia 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tokopedia Worker Control Center')
    parser.add_argument('-m', '--mode', type=str, required=True,
                        choices=['keyword', 'comments', 'store'], 
                        help='Pilih jenis worker yang mau dijalankan')

    args = parser.parse_args()
    
    worker = WorkerTokopedia()

    if args.mode == 'keyword':
        worker.worker_keyword()
        
    elif args.mode == 'comments':
        worker.worker_comments()
        
    elif args.mode == 'store':
        worker.worker_store()