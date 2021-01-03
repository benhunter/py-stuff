# Advent of Code Day 9
# https://adventofcode.com/2020/day/9


import itertools
import logging


def is_sumoftwo(target, parts):
    """Test if any two parts sum to the target.

    Parameters:
    target : int
    parts : list of ints
    """
    
    #itertools list of all combinations of pairs of parts 
    combos = itertools.combinations(parts, 2)
    sums = [a + b for (a, b) in combos]

    return target in sums


def find_first_fail(preamble_length, lines):
    for i in range(len(lines) - preamble_length):
        preamble = lines[i:i+preamble_length]

        if is_sumoftwo(lines[i+preamble_length], preamble):
            continue
        else:
            return lines[i+preamble_length], i + preamble_length
    return 0, 0


def test_testinput1():
    preamble_length = 5

    with open(".\\AdventOfCode\\2020\\day9-test-input.txt") as f:
        lines = [int(line.rstrip()) for line in f]

    part1 = 0
    # preamble = lines[:preamble_length]
    # logging.debug(f"preamble: {preamble}")

    part1, position = find_first_fail(preamble_length, lines)
    
    assert part1 == 127


def find_contiguous_set(target, position, lines):
    contig = []

    for i in range(2, len(lines)):
        for j in range(len(lines) - i):
            if sum(lines[j:j+i]) == target:
                return lines[j:j+i]

    return contig


def test_testinput2():
    preamble_length = 5
    part2 = 0

    with open(".\\AdventOfCode\\2020\\day9-test-input.txt") as f:
        lines = [int(line.rstrip()) for line in f]
    part1, position = find_first_fail(preamble_length, lines)

    part2_contiguous = find_contiguous_set(part1, position, lines)
    part2 = min(part2_contiguous) + max(part2_contiguous)

    assert part2 == 62


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")

    # test_testinput1()

    preamble_length = 25

    with open(".\\AdventOfCode\\2020\\day9-input.txt") as f:
        lines = [int(line.rstrip()) for line in f]

    part1 = 0
    part1, position = find_first_fail(preamble_length, lines)
    print(f"Part 1: {part1}")

    # test_testinput2()

    part2_contiguous = find_contiguous_set(part1, position, lines)
    part2 = min(part2_contiguous) + max(part2_contiguous)
    print(f"Part 2: {part2}")
