from itertools import combinations_with_replacement

s, len = input().split()
# s, len = "HACKER 3".split()
# print('s', s)
# print('list(s)', list(s))
s = ''.join(sorted(s))
# print(s)
combos = [''.join(combo) for combo in list(combinations_with_replacement(s, int(len)))]
combos.sort()

for c in combos:
    print(c)
