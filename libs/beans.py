import json
from pystalk import BeanstalkClient


class Producer():
    def __init__(self, tubename, host='localhost', port = 14711):
        self.beans = BeanstalkClient(host=host, port=port, auto_decode=True)
        self.beans.use(tubename)
        self.tubename = tubename
    
    def setJob(self, message, pri=1024, delay=0):
        self.beans.put_job(message, delay)
        
    def close(self):
        pass

class Worker():
    def __init__(self, tubename, host='localhost', port = 14711):
        self.beans = BeanstalkClient(host=host, port=port, auto_decode=True)
        self.beans.watch(tubename)
        self.tubename = tubename
    
    def getJob(self, timeout=10):
        return self.beans.reserve_job(timeout)
        
    def deleteJob(self, job):
        self.beans.delete_job(job.job_id)
    
    def buryJob(self, job):
        self.beans.bury_job(job.job_id)
    
    def releaseJob(self, job, delay=30):
        self.beans.release_job(job.job_id, delay=delay)
        
    def kickJob(self, number_job=10):
        self.beans.use(self.tubename)
        self.beans.kick_jobs(number_job)



