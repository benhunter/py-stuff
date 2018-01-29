import re
import subprocess
import time

import requests

now = int(time.time())
print(now)

s = requests.Session()
print(type(s.cookies))
# s.cookies.set('rounds', '0', domain='netcat.us')

regex = re.compile(b'Incorrect')
incorrect = 0
rounds = 50

for i in range(rounds):
    command = 'php -r \'$rnd = 1; srand(time()); $rnd &= rand(); echo $rnd;\''  # or add 1 second to time?
    cmd_output = subprocess.check_output(command, shell=True)
    guess = cmd_output.decode()
    # print('guess:', guess)
    r = requests.post('http://netcat.us:6655/', data={'guess': guess})
    # print(r.cookies)
    # print(r.content)

    if regex.search(r.content):
        print(r.content)
        incorrect += 1

    print(i)

print("Incorrect: ", incorrect)
print("% Correct: ", str((rounds - incorrect) / rounds * 100) + '%')

#
# r = s.get('http://netcat.us:6655/')
# r = s.post('http://netcat.us:6655/', data={'guess': 0})

#
# round = 3

'''  PHP Code
$time = 1517226214;
//Make it more difficult with every round
$rnd =  mt_rand(1, 1); //$_COOKIE['rounds']);
//Add some randomness
srand($time);
$rnd &= rand();
'''

# for i in range(20):
#     command = 'php -r \'echo $rnd = mt_rand(1, ' + str(round) + '); srand(time()+1); $rnd &= rand();\''
#     cmd_output = subprocess.check_output(command, shell=True)
#     guess = cmd_output.decode()
#     print('guess:', guess)
#     # guess &= now
#     r = s.post('http://netcat.us:6655/', data={'guess': guess})
#     # print(s.cookies)
#     # print(r.content)
#     round += 1
#     print('round: ', round)
#     print('cookie round: ', s.cookies)
#     print()
#
# print(s.cookies)
# print(r.content)


# cookies = r.cookies
# print(type(cookies))

# for i in range(5):
#     r = s.get('http://netcat.us:6655/') #, cookies=cookies)
#     # cookies = r.cookies
#     print(r.content)
#     print(r.cookies)
