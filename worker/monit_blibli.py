from pystalk import BeanstalkClient
from pprint import pprint

client = BeanstalkClient('localhost', 14711)

stats = client.stats_tube('blibli_keyword')
stats2 = client.stats_tube('blibli_comment')
stats3 = client.stats_tube('blibli_store')

print(f"--- Statistik Tube: {stats['name']} ---")
print(stats)
print(f"--- Statistik Tube: {stats2['name']} ---")
print(stats2)
print(f"--- Statistik Tube: {stats3['name']} ---")
print(stats3)
# print(f"Tugas menunggu (Ready)   : {stats['current-jobs-ready']}")
# print(f"Tugas sedang dikerjakan : {stats['current-jobs-reserved']}")
# print(f"Total tugas masuk       : {stats['total-jobs']}")