# Advent of Code Day 3
# https://adventofcode.com/2020/day/3

with open("day3-input.txt") as f:
    slope = [line.rstrip() for line in f]

# print(slope[0])
len_slope = len(slope[0])

count_right1 = 0
column_right1 = 0

count_right3 = 0
column_right3 = 0

count_right5 = 0
column_right5 = 0

count_right7 = 0
column_right7 = 0

count_right1down2 = 0
column_right1down2 = 0

for row_num, row in enumerate(slope):
    posn_right1 = column_right1 % len_slope
    # print(row, row_num, column_right3, posn_right3, row[posn_right3])
    posn_right3 = column_right3 % len_slope
    posn_right5 = column_right5 % len_slope
    posn_right7 = column_right7 % len_slope
    posn_right1down2 = column_right1down2 % len_slope

    if row[posn_right1] == "#":
        count_right1 += 1    
    if row[posn_right3] == "#":
        count_right3 += 1
    if row[posn_right5] == "#":
        count_right5 += 1
    if row[posn_right7] == "#":
        count_right7 += 1
    if (row_num % 2) == 0:
        if row[posn_right1down2] == "#":
            count_right1down2 += 1
        column_right1down2 += 1

    column_right1 += 1
    column_right3 += 3
    column_right5 += 5
    column_right7 += 7

product = count_right1 * count_right3 * count_right5 * count_right7 * count_right1down2

print("Part 1:", count_right3)
print("Part 2:", product)
