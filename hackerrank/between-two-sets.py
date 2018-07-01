#!/bin/python3
# https://www.hackerrank.com/challenges/between-two-sets/


import os


#
# Complete the getTotalX function below.
#
def getTotalX(a, b):
    total = 0
    a.sort()
    b.sort()

    range_min = max(a)
    range_max = min(b)

    for i in range(range_min, range_max + 1):
        # tempa = a.copy()
        # tempb = b.copy()
        # print(i)
        next_i = False
        for ai in a:
            if i % ai != 0:
                next_i = True
                break
        for bi in b:
            if bi % i != 0:
                next_i = True
                break
        if next_i:
            continue
        # print('found:', i)
        total += 1

    return total


def test_getTotalX():
    assert getTotalX([2, 4], [16, 32, 96]) == 3


def main():
    f = open(os.environ['OUTPUT_PATH'], 'w')
    nm = input().split()
    n = int(nm[0])
    m = int(nm[1])
    a = list(map(int, input().rstrip().split()))
    b = list(map(int, input().rstrip().split()))
    total = getTotalX(a, b)
    f.write(str(total) + '\n')
    f.close()


if __name__ == '__main__':
    main()
