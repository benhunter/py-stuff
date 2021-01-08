# Advent of Code Day 10
# https://adventofcode.com/2020/day/10


import itertools
import math


def prod_diffs(filepath):
    with open(filepath) as f:
        lines = [int(line) for line in f]

    # print(lines)
    # print(max(lines))
    # print(f"Device builtin adapter: {max(lines) + 3}")
    # print(sorted(lines, reverse=True))

    lines.append(max(lines) + 3)

    prev = 0
    # total = 0
    ones = 0
    threes = 0
    lines = sorted(lines)
    # print(lines)
    diffs = []
    for num in lines:
        diff = num - prev
        diffs.append(diff)
        # print(diff)
        # print(f"prev: {prev} num: {num} diff: {diff}")
        # total += num - prev
        if diff == 1:
            ones += 1
        elif diff == 3:
            threes += 1
        
        prev = num

    # print(f"ones: {ones} threes: {threes}")
    print(diffs)

    return ones * threes


def test_test1():
    assert prod_diffs(".\\AdventOfCode\\2020\\day10-test1-input.txt") == 35


def test_test2():
    assert prod_diffs(".\\AdventOfCode\\2020\\day10-test2-input.txt") == 220


def arrangements(adapters):
    # Part 2
    # Dynamic programming solution / memoization
    # Credit: https://www.reddit.com/r/adventofcode/comments/ka8z8x/2020_day_10_solutions/gf9mvrh/
    # https://www.reddit.com/r/adventofcode/comments/ka8z8x/2020_day_10_solutions/
    
    combos = {}
    combos[0] = 1

    for a in adapters[1:]:
        # every adapter can be connected to all possible combos of adapters that are 3 less than itself
        combos[a] = combos.get(a - 1, 0) + combos.get(a - 2, 0) + combos.get(a - 3, 0)

    return combos[max(combos)]


def difflist(adapters):
    diffs = []
    prev = 0
    for a in adapters:
        diffs.append(a - prev)
        prev = a
    return diffs


def part2(adapters):
    # My solution - lookup table for how many combos based on on the length of a group of 1s
    # manually calculated the possible combos for small groups where an adapter may be skipped
    
    groups = [len(x) - 1 for k, g in itertools.groupby(difflist(adapters)) if k == 1 and len(x := list(g)) > 1] 
    # groups = [len(x) for k, g in itertools.groupby(difflist(adapters)) if k == 1 and len((x := list(g))) > 2]
    # for k, g in itertools.groupby(difflist(adapters)):
        # print(k, list(g))
    # print(groups)

    combos = []
    for x in groups:
        if x == 1:
            combos.append(2)
        elif x == 2:
            combos.append(4)
        elif x == 3:
            combos.append(7)

    return math.prod(combos)

    # notes in OneNote
    # general solution (maybe?) for groups greater than 3 (where all adapters in the group are optional)
    # relies on previous calculation - dynamic programming / memoization
    # result is how many bad combos exist for the group size (not the number of good combos)
    # (run 1) = 0
    # (run 2) = 0
    # (run 3) = 1
    # (run x) = (run x-1)*2 + 2^(x-4)


if __name__ == "__main__":
    # test_test1()
    # test_test2()
    print(prod_diffs(".\\AdventOfCode\\2020\\day10-input.txt"))

    with open(".\\AdventOfCode\\2020\\day10-input.txt") as f:
        lines = [int(line) for line in f]

    lines.append(0)
    lines.append(max(lines) + 3)
    lines = sorted(lines)

    print(f"Part 2: {arrangements(lines)}")

    # print(difflist(lines))

    print(f"Part 2: {part2(lines)}")
    
