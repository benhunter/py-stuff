# Advent of Code 2020 Day 4
# https://adventofcode.com/2020/day/4

import re


ECL_LIST = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


with open(".\\AdventOfCode\\2020\\day4-input.txt") as f:
    lines = f.read()  # read file to a single string

# make a list of records. Two newlines seperate records.
records = lines.split("\n\n")

# clean up the records
for i in range(len(records)):
    records[i] = records[i].replace("\n", " ")
    records[i] = records[i].strip()

count_part1 = 0
count_part2 = 0

for r in records:
    # Part 1 checks
    if 'byr:' in r and \
       'ecl:' in r and \
       'eyr:' in r and \
       'hcl:' in r and \
       'hgt:' in r and \
       'iyr:' in r and \
       'pid:' in r:
       count_part1 += 1
    else:
        continue


    # Part 2 checks
    r = r.split()
    r.sort()

    # byr 1920-2002
    byr_match = re.match(r"^byr:(\d{4})$", r[0])
    if byr_match:
        byr = int(byr_match.group(1))
        if not (1920 <= byr <= 2002):
            continue
    else:
        continue

    # cid ignore. remove if it's there
    if re.match(r"^cid:", r[1]):
        del r[1]

    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    ecl_match = re.match(r"^ecl:(.{3})$", r[1])
    if ecl_match:
        ecl = ecl_match.group(1)
        if ecl not in ECL_LIST:
            continue
    else:
        continue

    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    eyr_match = re.match(r"^eyr:(\d{4})$", r[2])
    if eyr_match:
        eyr = int(eyr_match.group(1))
        if not (2020 <= eyr <= 2030):
            continue
    else:
        continue

    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    hcl_match = re.match(r"^hcl:#[0-9a-f]{6}$", r[3])
    if not hcl_match:
        continue

    # hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    hgt_match = re.match(r"^hgt:(\d+)(cm|in)$", r[4])
    if hgt_match:
        hgt_num = int(hgt_match.group(1))
        if hgt_match.group(2) == 'cm':
            if not (150 <= hgt_num <= 193):
                continue 
        elif hgt_match.group(2) == 'in':
            if not (59 <= hgt_num <= 76):
                continue
    else:
        continue

    # iyr 2010-2020
    iyr_match = re.match(r"^iyr:(\d{4})$", r[5])
    if iyr_match:
        iyr = int(iyr_match.group(1))
        if not (2010 <= iyr <= 2020):
            continue
    else:
        continue

    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    if not re.match(r"^pid:\d{9}$", r[6]):
        continue

    # print(r)
    count_part2 += 1


print("Part 1:", count_part1)
print("Part 2:", count_part2)
