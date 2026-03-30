from libs.beans import Producer
p = Producer(tubename='tokopedia')

keywords = ['sgm', 'nutrilone', 'bebelac']

for k in keywords:
    p.setJob(k)
    print("Success sending job")
    