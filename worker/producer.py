import json
from pystalk import BeanstalkClient

# links = ['https://www.tokopedia.com/nutrilonshop','https://www.tokopedia.com/s26','https://www.tokopedia.com/enfagrow-indonesia']

class Producer():
    def __init__(self, tubename, host='localhost', port = 1471):
        self.beans = BeanstalkClient(host=host, port=port, auto_decode=True)
        self.beans.use(tubename)
        self.tubename = tubename
    
    def setJob(self, message, delay=0):
        self.beans.put_job(message, delay)
        
    def close(self):
        pass

class Worker():
    def __init__(self, tubename, host='localhost', port = 1471):
        self.beans = BeanstalkClient(host=host, port=port, auto_decode=True)
        self.beans.watch(tubename)
        self.tubename = tubename
    
    def getJob(self):
        return self.beans.reserve_iter(timeout)
        
    def deleteJob(self, job: Job):
        self.beans.delete_job(job.job_id)
    
    def buryJob(self, job: Job):
        self.beans.bury_job(job.job_id)

        
# try:
#     client = BeanstalkClient(host='localhost', port=14711, auto_decode=True)
#     client.use('unprocessed')
#     for l in links:
#         client.put_job(str(l))
        
# except Exception as e:
#     print(f"Not Connected {e}")

