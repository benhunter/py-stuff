# https://www.hackerrank.com/challenges/kangaroo/problem

def kangaroo(x1, v1, x2, v2):
    # (x1 + v1 * time) == (x2 + v2 * time)
    # (x1 + v1 * time) - (x2 + v2 * time) == 0
    #
    # x1 - x2 + ((v1 - v2) * time) == 0
    # x1 - x2 == ((v2 - v1) * time)
    # (x1 - x2) / (v2 - v1) == time
    # (x1 - x2) % (v2 - v1) == 0

    if v1 <= v2:
        return 'NO'
    if (x1 - x2) % (v2 - v1) == 0:
        return 'YES'
    else:
        return 'NO'


def test_kangaroo():
    assert kangaroo(43, 2, 70, 2) == 'NO'
