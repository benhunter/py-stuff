#!/bin/python3
# https://www.hackerrank.com/challenges/new-year-chaos/problem?h_l=playlist&slugs%5B%5D=interview&slugs%5B%5D=interview-preparation-kit&slugs%5B%5D=arrays

import builtins
import unittest.mock


# Complete the minimumBribes function below.
def debug(*s):
    print(*s)
    # pass


def minimumBribes_bubblerev(q):
    '''
    SOLVED!
    :param q:
    :return:
    '''
    total = 0
    tracker = [0 for x in range(len(q))]

    for x in range(len(q)):
        rightbound = len(q) - 1
        # debug('outer x', x)
        for index in range(len(q) - 2, -1, -1):
            # debug('inner index', index)
            item = q[index]
            debug('index', index, 'item', item)
            if item > q[index + 1]:
                debug('item', item, '>', q[index + 1])
                debug('swapping before:', q)
                q[index] = q[index + 1]
                q[index + 1] = item
                total += 1
                debug('swapping after: ', q)
                tracker[item - 1] += 1
                if tracker[item - 1] >= 3:
                    print('Too chaotic')
                    return
                debug('tracker:        ', tracker)
                debug()
            elif (index + 1) == rightbound:
                rightbound = index
                debug('rightbound', rightbound)
        if rightbound == 0:
            break

    debug('answer:', total)
    print(total)

    # print('final', q, 'total', total)


def minimumBribes_count(q):
    '''
    FAIL
    :param q:
    :return:
    '''
    # print(type(q))
    # print(q)
    total = 0
    for index, item in enumerate(q):
        if index >= len(q) - 1:
            # print(index)
            # print(item)
            continue
        if q[index] > (index + 1):

            difference = q[index] - (index + 1)
            # print('Jumped: ' + str(difference))
            if difference > 2:
                print("Too chaotic")
                return
            else:
                total += difference
        elif q[index] > q[index + 1]:
            total += 1
        elif q[len(q) - 1] - (len(q) - 1) == -4:
            total += 1
    if q[len(q) - 1] - (len(q) - 1) == -4:
        total += 1
    print(total)


def minimumBribes_bubble(q):
    '''
    FAIL
    :param q:
    :return:
    '''
    total = 0
    tracker = [0 for x in range(len(q))]
    for x in range(len(q)):
        for index, item in enumerate(q):
            # print(index, item)

            # don't touch last item
            if index >= (len(q) - 1):
                break
            # if item != (index + 1):
            #     print(item, 'index+1:', index + 1, 'difference:', str(item - (index + 1)))

            if item > (index + 1):
                # print('swapping', item, 'index', index)
                q[index] = q[index + 1]
                q[index + 1] = item
                # print(q)
                total += 1
                tracker[index] += 1

            if tracker[index] > 2:
                print(tracker)
                print('Too chaotic')
                return

    print('answer:', sum(tracker))
    # print('final', q, 'total', total)


def test_minimumBribes():
    # minimumBribes_count([2, 1, 5, 3, 4])  # print: 3
    # minimumBribes_count([2, 5, 1, 3, 4])  # print: Too chaotic
    # minimumBribes_count([1, 2, 5, 3, 7, 8, 6, 4])  # print: 7
    # print()
    # print()

    # minimumBribes_bubblerev([2, 1, 5, 3, 4])  # print: 3
    # print('answer: 3')
    # print()

    minimumBribes_bubblerev([2, 5, 1, 3, 4])  # print: Too chaotic
    print('answer: Too chaotic')
    print()

    # minimumBribes_bubblerev([1, 2, 5, 3, 7, 8, 6, 4])  # print: 7
    #                 -   1, 2, 3, 4, 5, 6, 7, 8
    #                 =   0, 0, 2, -1, 2, 2, -1, -4
    #                 =   0, 0, 2, 0, 2, 2, 1, 0
    # print('answer: 7')
    # print()

    # minimumBribes_bubblerev([1, 2, 5, 3, 7, 8, 6, 4, 9, 10])  # print: 7
    #                 -   1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    #             diff=   0, 0, 2,-1, 2, 2,-1,-4, 0, 0
    #            jumps=   0, 0, 2, 0, 2, 2, 1, 0, 0, 0
    # print('answer: 7')
    # print()

    # minimumBribes_bubblerev([1, 2, 5, 3, 7, 8, 6, 9, 4, 10])  # print: 8
    #                 -   1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    #             diff=   0, 0, 2,-1, 2, 2,-1, 1,-5, 0
    #            jumps=   0, 0, 2, 0, 2, 2, 1, 1, 0, 0
    # print('answer: 8')
    # print()
    # case = [3, 1, 2, 5, 4]


'''
Input:
2
8
5 1 2 3 7 8 6 4
8
1 2 5 3 7 8 6 4

Output:
Too chaotic
7
'''



def test_function(capsys):
    mock_input = unittest.mock.Mock()
    mock_input.side_effect = ['2', '5', '2 1 5 3 4', '5', '2 5 1 3 4']

    expected_output = '3\nToo chaotic'

    with unittest.mock.patch.object(builtins, 'input', mock_input):
        main()
        out, err = capsys.readouterr()
        assert out == expected_output
        # assert main() == expected_output


def main():
    t = int(input())
    for t_itr in range(t):
        n = int(input())

        q = list(map(int, input().rstrip().split()))

        minimumBribes(q)


if __name__ == '__main__':
    # main()
    test_minimumBribes()
