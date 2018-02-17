# input = input()
# input = 5

# for i in range(1, int(input)+1): #More than 2 lines will result in 0 score. Do not leave a blank line also
#
#     # first = list(map(str, range(1, i + 1)))
#     first = list(range(1, i + 1))
#     # print(first)
#     second = list(map(str, reversed(range(1, i))))
#     # print(second)
#     print(''.join(first + second))
#
#     print(ascii(list(map(str, range(1, i + 1))) + list(map(str, reversed(range(1, i))))))

# print(121)

# 5
# 123454321

# string = ''.join(list(map(lambda x: str(x), [0,1,2,3,4,5])))
# string = ''.join(list(map(lambda x: str(x), list(map(lambda x: x, [1])))))
# print(string)


# map(lambda n: (lambda f, *a: f(f, *a))(lambda rec, n: 1 if n == 0 else n*rec(rec, n-1), n), range(10))

# (lambda a:lambda v:a(a,v))(lambda s,x:1 if x==0 else x*s(s,x-1))(10)

import hashlib

md5 = hashlib.md5()
md5.update(b'n')
# print(md5.digest().decode())
# print(md5.digest())
print(md5.hexdigest())

# print(0x110000)
# print(chr(1114111))
i = 0
# print(i)
c = chr(i)
# print(c)
# print(hashlib.md5().update(c.encode()))


char_set = '123456789abcdefghijklmnopqrstuvwxyz'
for c in char_set:
    m = hashlib.md5()
    m.update(c.encode())
    print(m.hexdigest())
    print(type(m.hexdigest()))
    print({m.hexdigest(): c})
    print({c: m.hexdigest()})

print(ord(chr(40)))
