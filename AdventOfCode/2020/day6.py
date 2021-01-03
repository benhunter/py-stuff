# Advent of Code Day 6
# https://adventofcode.com/2020/day/6

import string

with open(".\\AdventOfCode\\2020\\day6-input.txt") as f:
    lines = f.read()  # read file to a single string

# make a list of groups. Two newlines seperate records.
groups = lines.split("\n\n")

part1 = 0
part2 = 0

for i, g in enumerate(groups):

    # Part 1
    groups[i] = "".join(sorted(set("".join(g.split()))))
    part1 += len(groups[i])

    # Part 2
    people = g.split()
    if len(people) == 1:
        part2 += len(people[0])
    elif len(people) > 1:
        group = "".join(sorted("".join(g.split())))
        
        for letter in string.ascii_lowercase:
            if group.count(letter) == len(people):
                part2 += 1
            


print("Part 1:", part1)
print("Part 2:", part2)
