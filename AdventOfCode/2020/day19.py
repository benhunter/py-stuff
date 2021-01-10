# Advent of Code 2020 Day 19
# https://adventofcode.com/2020/day/19


def is_valid(rules, message):
    
    
    
    return


def count_matches(rules, messages):
    matches = 0

    # parse rules
    rules = sorted(rules)
    rules_dict = {}

    print(rules)
    for i, r in enumerate(rules):
        rule = r.split(":")
        rules_dict[rule[0]] = rule[1]
        print(rules_dict)
        rule = int(rule[0]), rule[1].strip().strip("\"")

        print(rule)

        if "|" in rule[1]:
            rule = rule[0], [x.strip() for x in rule[1].split("|")]
            print(rule)

        rules[i] = rule
        print(f"{rules[i]}")

    print(rules)

    # parse messages
    for m in messages:
        if is_valid(rules, m):
            matches += 1
    return matches


def test_example1():
    with open(".\\AdventOfCode\\2020\\day19-test1-input.txt") as f:
        rules, messages = [x.splitlines() for x in f.read().split("\n\n")]
    # print(rules)
    # print(messages)

    assert count_matches(rules, messages) == 2

if __name__ == "__main__":
    test_example1()
