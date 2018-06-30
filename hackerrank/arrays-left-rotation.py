#!/bin/python3

# Complete the rotLeft function below.
def rotLeft(a, d):
    print(a, d)
    # d items
    right = a[:d]
    print(right)
    left = a[d:]
    print(left)
    print(left + right)
    return left + right


if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')
    #
    # nd = input().split()
    #
    # n = int(nd[0])
    #
    # d = int(nd[1])
    #
    # a = list(map(int, input().rstrip().split()))
    #
    # result = rotLeft(a, d)
    #
    # fptr.write(' '.join(map(str, result)))
    # fptr.write('\n')
    #
    # fptr.close()
    print(rotLeft([1, 2, 3, 4, 5], 4))
