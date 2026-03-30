import argparse
# Import Class dari file worker kamu
from worker.lazada_worker import WorkerLazada

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lazada Worker Control Center')
    parser.add_argument('-m', '--mode', type=str, required=True,
                        choices=['keyword', 'comments', 'store'], 
                        help='set worker')

    args = parser.parse_args()
    
    worker = WorkerLazada()

    if args.mode == 'keyword':
        worker.worker_keyword()
        
    elif args.mode == 'comments':
        worker.worker_comments()
        
    elif args.mode == 'store':
        worker.worker_store()