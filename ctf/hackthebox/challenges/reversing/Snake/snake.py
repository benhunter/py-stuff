#!/usr/bin/python2.7
import random

lr = '\x64'
print('''
___________.__               _________              __           
\__    ___/|  |__   ____    /   _____/ ____ _____  |  | __ ____  
  |    |   |  |  \_/ __ \   \_____  \ /    \\__  \ |  |/ // __ \ 
  |    |   |   Y  \  ___/   /        \   |  \/ __ \|    <\  ___/ 
  |____|   |___|  /\___  > /_______  /___|  (____  /__|_ \\___  >
                \/     \/          \/     \/     \/     \/    \/ 

''')
chains = [0x74, 0x68, 0x69, 0x73, 0x20, 0x69, 0x73, 0x20, 0x61, 0x20, 0x74, 0x72, 0x6f, 0x6c, 0x6c]

str_chains = ''.join([chr(c) for c in chains])
print('str_chains:', str_chains)

db = '\x6e'
ef = '\x63'
nn = '\x61'
ty = '\x61'
gh = '\x6e'
aa = '\x61'
rr = '\x6f'

chars = []

keys = [0x70, 0x61, 0x73, 0x73, 0x77, 0x6f, 0x72, 0x64, 0x21, 0x21]
str_keys = ''.join([chr(c) for c in keys])
print('str_keys:', str_keys)

password = [0x69, 0x74, 0x73, 0x20, 0x6e, 0x6f, 0x74, 0x20, 0x74, 0x68, 0x61, 0x74, 0x20, 0x65, 0x61, 0x73, 0x79]
str_password = ''.join([chr(c) for c in password])

auth = [0x6b, 0x65, 0x65, 0x70, 0x20, 0x74, 0x72, 0x79, 0x69, 0x6e, 0x67]
str_auth = ''.join([chr(c) for c in auth])
print('str_auth:', str_auth)
print()

print('str_password:', str_password)

lock_pick = random.randint(0, 0x3e8)
# lock_pick = 0 # TODO
lock = lock_pick * 2
lock = lock + 10
lock = lock / 2
lock = lock - lock_pick

lock = (((lock_pick * 2) + 10) / 2) - lock_pick

# added for python 3
print('lock', lock)
lock = int(lock)
print('lock', lock)

print('The Snake Created by 3XPL017')
print('Your number is ' + str(lock_pick))
for key in keys:
    keys_encrypt = lock ^ key
    chars.append(keys_encrypt)

str_chains_encrypt = ''

for chain in chains:
    chains_encrypt = chain + 0xA
    str_chains_encrypt += chr(chains_encrypt)
    chars.append(chains_encrypt)

print('str_chains_encrypt:', str_chains_encrypt)

print()
str_chars = ''.join([chr(c) for c in chars])
print('str_chars:', str(str_chars))
print('chars:', chars)
print('len(chars)', len(chars))
slither = aa + db + nn + ef + rr + gh + lr + ty
print('Authentication required')
print('')

# user_input = raw_input('Enter your username\n')
user_input = slither
print('slither:', slither)
if user_input == slither:
    pass

else:
    print('Wrong username try harder')
    exit()
# pass_input = raw_input('Enter your password\n')

pass_input = 'AAAAA'

# print('chars', chars)
str_chars = ''.join([chr(c) for c in chars])
print('str_chars:', str(str_chars))

pass_input = str_chars

for passes in pass_input:
    for char in chars:
        if passes == str(chr(char)):
            print('Good Job')
            break
        else:
            print('Wrong password try harder')
            exit(0)
    break
