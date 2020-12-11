# Advent of Code Day 5
# https://adventofcode.com/2020/day/5

import pytest
import re

def decode_boarding_pass(seat_encoded):
    # first 7 chars must be F or B
    # last 3 chars must be L or R

    if not re.match(r"^[FB]{7}[LR]{3}$", seat_encoded):
        # Manually raise Exception because assert can be stripped at runtime
        raise ValueError("Boarding pass format is invalid.")
    
    # row: F=0, B=1, convert to int
    row = seat_encoded[:7].replace("F", "0").replace("B", "1")
    row = int(row, base=2)

    # column: R=1, L=0, convert to int
    column = seat_encoded[7:].replace("R", "1").replace("L", "0")
    column = int(column, base=2)

    seat_id = row * 8 + column

    return (row, column, seat_id)


if __name__ == "__main__":
    with open("day5-input.txt") as f:
        passes = [line.rstrip() for line in f]
    # print(passes)
    # print(len(passes))

    # Part 1
    # what is highest seat ID on a pass?
    # max of seat[2] of passes
    part1 = max([decode_boarding_pass(p)[2] for p in passes])
    print("Part 1:", part1)

    # Part 2
    # print list of all missing seats by ID
    seat_IDs = [decode_boarding_pass(p)[2] for p in passes]
    possible_seat = []
    for i in range(part1):
        if i not in seat_IDs:
            possible_seat.append(i)
    print("Part 2:", max(possible_seat))

    


def test_decode_bad_passes():
    with pytest.raises(TypeError):
        decode_boarding_pass()
    
    with pytest.raises(ValueError):
        decode_boarding_pass("")

    with pytest.raises(ValueError):
        decode_boarding_pass("FFFFFFLLL")
    
    with pytest.raises(ValueError):
        decode_boarding_pass("FFFFFFFLL")

    with pytest.raises(ValueError):
        decode_boarding_pass("FFFFFFALLL")

    with pytest.raises(ValueError):
        decode_boarding_pass("FFFFFFFLLA")

def test_decode_good_passes():
    # assert decode_boarding_pass("") == (, , )

    # FBFBBFFRLR: row 44, column 5, seat ID 357.
    assert decode_boarding_pass("FBFBBFFRLR") == (44, 5, 357)

    # BFFFBBFRRR: row 70, column 7, seat ID 567.
    assert decode_boarding_pass("BFFFBBFRRR") == (70, 7, 567)

    # FFFBBBFRRR: row 14, column 7, seat ID 119.
    assert decode_boarding_pass("FFFBBBFRRR") == (14, 7, 119)

    # BBFFBBFRLL: row 102, column 4, seat ID 820.
    assert decode_boarding_pass("BBFFBBFRLL") == (102, 4, 820)
