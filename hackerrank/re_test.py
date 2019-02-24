# https://www.hackerrank.com/challenges/incorrect-regex/problem
import re

n = int(input())
for i in range(n):
    # print()
    # print(i)
    r = input()
    try:
        re.compile(r)
    except re.error as e:
        print(False)
        continue
    print(True)
