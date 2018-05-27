# https://hackers.gg/challenges/web/realistic1/

from pprint import pprint

import requests

url = 'https://hackers.gg/drone/dronelogin'
r = requests.post(url, data={'username': 'test', 'password': 'pass123', 'name': 'testtesttest'})
print(r)
pprint(r.content)
