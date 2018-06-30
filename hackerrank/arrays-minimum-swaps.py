#!/bin/python3
# https://www.hackerrank.com/challenges/minimum-swaps-2/problem?h_l=playlist&slugs%5B%5D=interview&slugs%5B%5D=interview-preparation-kit&slugs%5B%5D=arrays

# Complete the minimumSwaps function below.
def minimumSwapsIndex(arr):
    count = 0
    for item in range(1, len(arr)):
        index = arr.index(item)
        if item == (index + 1):
            continue
        # swap
        arr[index] = arr[item - 1]
        arr[item - 1] = item
        count += 1
        print(arr)
    print(count)


def minimumSwaps(arr):
    count = 0
    for index in range(len(arr)):
        item = arr[index]
        # print('index', index, 'item', item, 'arr', arr)
        if index == item - 1:
            continue

        # swap with index+1, wherever it is. arr[index] must be good to proceed
        # print('swapping', arr[item-1], 'with', item)
        swaploc = arr.index(index + 1)
        arr[index] = arr[swaploc]
        arr[swaploc] = item

        count += 1
        # print('after swap', arr)
    # print(count)
    return count


if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')
    #
    # n = int(input())
    #
    # arr = list(map(int, input().rstrip().split()))
    #
    # res = minimumSwaps(arr)
    #
    # fptr.write(str(res) + '\n')
    #
    # fptr.close()
    arr = [4, 3, 1, 2]
    arr = [7, 1, 3, 2, 4, 5, 6]
    minimumSwaps(arr)
