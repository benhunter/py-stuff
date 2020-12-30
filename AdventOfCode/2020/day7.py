# Advent of Code Day 7
# https://adventofcode.com/2020/day/7

import re


with open("day7-input.txt") as f:
    lines = [line.rstrip() for line in f]

# print(rules)
# print(len(rules))

for line in lines:
    rule = re.match(r"(.+) bags contain (.+[\.,]?)+", line)
    print(rule)
    print(rule.groups())
    pass

