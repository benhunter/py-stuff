#!/bin/python3
# https://www.hackerrank.com/challenges/new-year-chaos/problem?h_l=playlist&slugs%5B%5D=interview&slugs%5B%5D=interview-preparation-kit&slugs%5B%5D=arrays

import builtins
import unittest.mock


# Complete the minimumBribes function below.
def minimumBribes(q):
    print('3')


next(iter(['2', '5', '2 1 5 3 4', '5', '2 5 1 3 4']))


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
    main()
