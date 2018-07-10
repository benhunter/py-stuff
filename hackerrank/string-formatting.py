# https://www.hackerrank.com/challenges/python-string-formatting/

"""
    1     1     1     1
    2     2     2    10
    3     3     3    11
    4     4     4   100
    5     5     5   101
    6     6     6   110
    7     7     7   111
    8    10     8  1000
    9    11     9  1001
   10    12     A  1010
   11    13     B  1011
   12    14     C  1100
   13    15     D  1101
   14    16     E  1110
   15    17     F  1111
   16    20    10 10000
   17    21    11 10001
"""


def table(n):
    column = len(bin(n)[2:])
    print(column)

    for i in range(1, n + 1):
        # print(str(i).rjust(column, ' '), oct(i)[2:].rjust(column, ' '), hex(i)[2:].rjust(column, ' '),
        #       bin(i)[2:].rjust(column, ' '))
        print(str(i).rjust(column, ' '), oct(i)[2:].rjust(column, ' '),
              '{:X}'.format(i).rjust(column, ' '), bin(i)[2:].rjust(column, ' '))


table(2)
print()
print(''' 1  1  1  1
 10''')
print()
table(17)
print()
print('''    1     1     1     1
    2     2     2    10
    3     3     3    11
    4     4     4   100
    5     5     5   101
    6     6     6   110
    7     7     7   111
    8    10     8  1000
    9    11     9  1001
   10    12     A  1010
   11    13     B  1011
   12    14     C  1100
   13    15     D  1101
   14    16     E  1110
   15    17     F  1111
   16    20    10 10000
   17    21    11 10001''')
