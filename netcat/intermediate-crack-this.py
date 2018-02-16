# https://netcat.us/challenges/intermediate/intermediate7/

import base64
import gzip
import hashlib

import requests

link = 'https://netcat.us/static/crackme.txt'

# download the txt
txt = requests.get(url=link)
decoded = None

# print(txt.content)

# decode base64
decoded = base64.b64decode(txt.content)
# print(decoded)

# decompress gzip
ungzipped = gzip.decompress(decoded)
# print(ungzipped)
# print(ungzipped.decode())

# make a list of the md5 hashes
md5_list = ungzipped.decode().split(' ')
# print(md5_list)

# build a dict (rainbow table) of single character to md5 to reverse lookup
rainbow = {}
for i in range(1, 256):
    # print(chr(i))
    # print(chr(i).encode())
    m = hashlib.md5()
    m.update(chr(i).encode())
    # print(m)
    digest = m.hexdigest()
    rainbow.update({digest: chr(i)})
# print(rainbow)

for m in md5_list:
    if m in rainbow:
        print(rainbow.get(m), end='')
