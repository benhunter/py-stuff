# Advent of Code Day 7
# https://adventofcode.com/2020/day/7

import re

from functools import reduce
from pprint import pprint


with open("day7-input.txt") as f:
    lines = [line.rstrip() for line in f]

# print(rules)
# print(len(rules))

class BagRule:
    
    def __init__(self, container, contains):
        self.container = container
        self.contains = contains

    # def __init__(self, str_rule: str):
    #     self.str_rule = str_rule

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.container + " contains " + str(self.contains)

    def list_contains_names(self):
        names = [i[0] for i in self.contains]
        return names


rules = []

for line in lines:
    # rule = re.match(r"(.+) bags contain (.+[\.,]?)+", line)
    rule = re.match(r"(.+) bags contain (.+[,]?)+\.$", line)
    # rule = re.match(r"(.+) bags contain (\d+.+ bag[s,]?)+", line)

    # print(rule)
    groups = rule.groups()
    # print(groups)
    container = groups[0]
    # print(container)
    contains = groups[1].split(",")
    # print(contains)

    if contains[0] == "no other bags":
        # don't add a rule, go to the next line
        continue

    for i, bag in enumerate(contains):
        # print(bag)
        color = re.search(r"(\d+) (.*) bags?", bag)
        # print(color.group(2))
        contains[i] = [color.group(2), int(color.group(1))]

    rules.append(BagRule(container, contains))

target = "shiny gold"
check_right = []
check_right.append(target)
part1 = set()
while len(check_right) > 0:
    for rule in rules:
        if check_right[0] in rule.list_contains_names():
            # print(rule, "matched on", check_right[0])
            check_right.append(rule.container)
            part1.add(rule.container)
    check_right.pop(0)

# print(solution)

# Part 1
print(len(part1))

# Part 2
def calculate_bag(bag, rules):

    if isinstance(bag, BagRule):
        for i, rule in enumerate(bag.contains):
            if isinstance(rule[0], str):
                if rule[0] in [r.container for r in rules]:
                    # don't forget the + 1 here to include the bag holding the others:
                    bag.contains[i][0] = calculate_bag([r for r in rules if r.container == rule[0]][0], rules) + 1
                    # print(bag, "calculated bag from str")
                else:
                    # print(bag, rule[0], "not in rules")
                    bag.contains[i][0] = 1

    expanded_list = [isinstance(y, int) for x in bag.contains for y in x]
    if all(expanded_list):
        total = 0
        for i in bag.contains:
            total += i[0] * i[1]
        # print(bag, "returning", total)
        return total
    else:
        print("ERROR", bag)

target_rule = [r for r in rules if r.container == target][0]
part2 = calculate_bag(target_rule, rules)
print(part2)


