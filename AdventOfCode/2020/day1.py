# Advent of Code Day 1
# https://adventofcode.com/2020/day/1

import itertools

in_file_name = "day1-input.txt"

with open(in_file_name) as f:
    # expense_report = [line.rstrip() for line in f]
    expense_report = [int(line.rstrip()) for line in f]

pairs = itertools.combinations(expense_report, 2)
for p in pairs:
    if p[0] + p[1] == 2020:
        print(p, p[0] * p[1])

# part 2
triples = itertools.combinations(expense_report, 3)
for t in triples:
    if t[0] + t[1] + t[2] == 2020:
        print(p, t[0] * t[1] * t[2])
