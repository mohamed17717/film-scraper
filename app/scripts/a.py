from json import loads
from re import findall

with open('data-sample.1.json') as f:
    d = loads(f.read())
    f.close()

new_d = {}
[new_d.update({k:v}) for k,v in d.items() if v['film_url']]

for i in new_d:
    print(i)