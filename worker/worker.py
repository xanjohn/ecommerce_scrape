from pystalk import BeanstalkClient

processed= []
def parse(u):
    return 'Processed the link:- ' + u

client = BeanstalkClient(host='localhost', port=14711, auto_decode=True)
client.watch('unprocessed')

for job in client.reserve_iter():
    try:
        url = job.job_data
        print(url)
        
        parsed_url = parse(url)
        print(parsed_url)
        
        client.put_job_into('parsed', parsed_url)
        client.delete_job(job.job_id)
        print(f"Job Finished")
    except Exception as e:
        print(f"Error{e}")
        client.release_job(job.job_id)
    print('-' * 30)

