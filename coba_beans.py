import beanstalkc
beanstalk = beanstalkc.Connection(host='localhost', port=14711)

beanstalk.put('hey!')
job = beanstalk.reserve()

job_consume = job.body
print(job_consume)