"""
#size 3

----c----
--c-b-c--
c-b-a-b-c
--c-b-c--
----c----

#size 5

--------e--------
------e-d-e------
----e-d-c-d-e----
--e-d-c-b-c-d-e--
e-d-c-b-a-b-c-d-e
--e-d-c-b-c-d-e--
----e-d-c-d-e----
------e-d-e------
--------e--------

#size 10

------------------j------------------
----------------j-i-j----------------
--------------j-i-h-i-j--------------
------------j-i-h-g-h-i-j------------
----------j-i-h-g-f-g-h-i-j----------
--------j-i-h-g-f-e-f-g-h-i-j--------
------j-i-h-g-f-e-d-e-f-g-h-i-j------
----j-i-h-g-f-e-d-c-d-e-f-g-h-i-j----
--j-i-h-g-f-e-d-c-b-c-d-e-f-g-h-i-j--
j-i-h-g-f-e-d-c-b-a-b-c-d-e-f-g-h-i-j
--j-i-h-g-f-e-d-c-b-c-d-e-f-g-h-i-j--
----j-i-h-g-f-e-d-c-d-e-f-g-h-i-j----
------j-i-h-g-f-e-d-e-f-g-h-i-j------
--------j-i-h-g-f-e-f-g-h-i-j--------
----------j-i-h-g-f-g-h-i-j----------
------------j-i-h-g-h-i-j------------
--------------j-i-h-i-j--------------
----------------j-i-j----------------
------------------j------------------
"""


def draw(n):
    lines = n * 2 - 1
    width = n * 4 - 3

    for i in range(n):
        mid = '-'.join([chr(x + 96) for x in range(n, n - i - 1, -1)])
        if n > n - i:
            mid += '-' + '-'.join([chr(x + 97) for x in range(n - i, n)])
        pad_len = ((width - len(mid)) / 2)
        pad = '-' * int(pad_len)
        print(pad + mid + pad)

    for i in range(n - 2, -1, -1):
        mid = '-'.join([chr(x + 95) for x in range(n + 1, n - i, -1)])
        if n > n - i:
            mid += '-' + '-'.join([chr(x + 97) for x in range(n - i, n)])
        pad = '-' * int((width - len(mid)) / 2)
        print(pad + mid + pad)


draw(1)
print()
draw(2)
print()
draw(10)
print()


# Boki's awesome solution: https://www.hackerrank.com/challenges/alphabet-rangoli/forum/comments/138799
def boki(n):
    import string
    alpha = string.ascii_lowercase

    # n = int(input())
    L = []
    for i in range(n):
        s = "-".join(alpha[i:n])
        L.append((s[::-1] + s[1:]).center(4 * n - 3, "-"))
    print('\n'.join(L[:0:-1] + L))


boki(5)
boki(10)
