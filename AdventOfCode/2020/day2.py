# Advent of Code 2020 Day 2
# https://adventofcode.com/2020/day/2

countpart1 = 0
countpart2 = 0

with open("day2-input.txt") as f:
    password_list = [line.rstrip() for line in f]
    # print(password_list)

# part 1
for p in password_list:
    # print(p)

    parts = p.split()
    # print(parts)

    min, max = map(int, parts[0].split('-'))
    # print(min, max)

    char = parts[1][0]
    # print(char)

    # print(parts[2].countpart1(char))

    if max >= parts[2].count(char) >= min:
        # print("pass")
        countpart1 += 1

    if (parts[2][min-1] == char and parts[2][max-1] != char) or (parts[2][min-1] != char and parts[2][max-1] == char):
        countpart2 += 1
     
print("Part 1:", countpart1)
print("Part 2:", countpart2)
