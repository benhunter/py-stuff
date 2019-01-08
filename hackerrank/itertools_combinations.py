# https://www.hackerrank.com/challenges/itertools-combinations/problem

import itertools

string, length = input().split()
string = ''.join(sorted(string))
length = int(length)

# print(string, length)
for i in range(1, length + 1):
    for combo in itertools.combinations(string, i):
        print(''.join(combo))
