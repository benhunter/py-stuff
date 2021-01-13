# Advent of Code 2020 Day 19
# https://adventofcode.com/2020/day/19


def match(message, rule_num, rules_dict):
    '''Match the message against the rules, starting with rule_num. Check left to right.

    There are 3 types of rule:
    1. literal: "a"
    2. sequence: 1 2
    3. option: sequence | sequence

    Return the substring that matches successfully. "" means no match.
    If the full message is returned, it matched entirely.
    '''

    # determine the type of rule that is rules_dict[rule_num]
    if isinstance(rules_dict[rule_num], str) and message[0] == rules_dict[rule_num]:
        # literal rule
        return message[0]
    
    elif isinstance(rules_dict[rule_num], list):
        if isinstance(rules_dict[rule_num][0], int):
            # sequence rule
            consumed = ""
            for index, seq_rule_num in enumerate(rules_dict[rule_num]):
                if message[len(consumed):] == "":
                    return ""
                seq_match = match(message[len(consumed):], seq_rule_num, rules_dict)
                if seq_match == "":
                    return ""
                elif seq_match != "":
                    consumed += seq_match
            return consumed

        elif isinstance(rules_dict[rule_num][0], list):
            # option rule
            # print(rules_dict[rule_num])
            for option in rules_dict[rule_num]:
                try_next_option = False  # flag to break out of inner for loop and go to the next option
                consumed = ""
                for seq_rule_num in option:
                    if message[len(consumed):] == "":
                        # no more of the message is left to consume, but we still have sequence left in the rule
                        # try the next option
                        try_next_option = True
                        break
                    seq_match = match(message[len(consumed):], seq_rule_num, rules_dict)
                    if seq_match == "":
                        # no match, try next option
                        try_next_option = True
                        break

                    elif seq_match != "":
                        consumed += seq_match

                if try_next_option:
                    continue

                if consumed == message:
                    # this rule matches completely
                    return consumed
                elif consumed == message[:len(consumed)]:
                    # everything consumed so far matches
                    # note there is still more message to the right of the match
                    return consumed
                else:
                    # try the next option
                    continue
    
    return ""


def is_valid(message, rule_num, rules_dict):
    if match(message, rule_num, rules_dict) == message:
        return True
    else:
        return False


def test_is_valid1():
    # literal rule
    rules_dict = {0: "a"}
    assert is_valid("a", 0, rules_dict)  # good
    assert not is_valid("b", 0, rules_dict)  # wrong char
 

def test_is_valid2():
    # sequence and literal rules
    rules_dict = {0: [1, 2], 1: "a", 2: "b"}
    assert is_valid("ab", 0, rules_dict)  # good
    assert not is_valid("a", 0, rules_dict)  # message too short
    assert not is_valid("b", 0, rules_dict)  # message too short
    assert not is_valid("abc", 0, rules_dict) # message too long


def test_is_valid3():
    # sequence of repeating literals
    rules_dict = {0: [1, 2], 1: "a", 2: "a"}
    assert is_valid("aa", 0, rules_dict)  # good
    assert not is_valid("aaa", 0, rules_dict)  # too long


def test_is_valid4():
    # sequence of repeating literals, same rule used again
    rules_dict = {0: [1, 1], 1: "a", 2: "a"}
    assert is_valid("aa", 0, rules_dict)  # good
    assert not is_valid("aaa", 0, rules_dict)  # too long

    rules_dict = {0: [1, 1, 1], 1: "a", 2: "a"}
    assert not is_valid("aa", 0, rules_dict)  # too short
    assert is_valid("aaa", 0, rules_dict)  # good
    assert not is_valid("aaaa", 0, rules_dict)  # too long

    rules_dict = {0: [1, 1, 1, 1], 1: "a", 2: "a"}
    assert not is_valid("aaa", 0, rules_dict)  # too short
    assert is_valid("aaaa", 0, rules_dict)  # good
    assert not is_valid("aaaaa", 0, rules_dict)  # too long


def test_is_valid5():
    # sequence of sequences, nested rules
    rules_dict = {0: [1, 2], 1: [3, 4], 2: [4, 3], 3: "a", 4: "b"}
    assert is_valid("abba", 0, rules_dict)  # good
    assert not is_valid("baab", 0, rules_dict)  # bad
    assert not is_valid("a", 0, rules_dict)  # bad
    assert not is_valid("ab", 0, rules_dict)  # bad
    assert not is_valid("abb", 0, rules_dict)  # bad
    assert not is_valid("abbab", 0, rules_dict)  # bad


def test_is_valid6():
    # rule with simple option: a | b
    rules_dict = {0: [[1], [2]], 1: "a", 2: "b"}
    assert is_valid("a", 0, rules_dict)
    assert is_valid("b", 0, rules_dict)
    assert not is_valid("ab", 0, rules_dict)
    assert not is_valid("aa", 0, rules_dict)


def test_is_valid7():
    # option of sequences
    rules_dict = {0: [1, 2], 1: "a", 2: [[1, 3], [3, 1]], 3: "b"}
    assert is_valid("aab", 0, rules_dict)
    assert is_valid("aba", 0, rules_dict)
    assert not is_valid("ab", 0, rules_dict)
    assert not is_valid("abab", 0, rules_dict)
    assert not is_valid("abba", 0, rules_dict)


def test_is_valid_example2():
    rules_dict = {0: [4, 1, 5], 1: [[2, 3], [3, 2]], 2: [[4, 4], [5, 5]], 3: [[4, 5], [5, 4]], 4: 'a', 5: 'b'}
    assert is_valid("ababbb", 0, rules_dict)
    assert is_valid("abbbab", 0, rules_dict)
    assert not is_valid("bababa", 0, rules_dict)
    assert not is_valid("aaabbb", 0, rules_dict)
    assert not is_valid("aaaabbb", 0, rules_dict)


def count_matches(rules, messages):
    matches = 0

    # parse rules
    rules = sorted(rules)
    rules_dict = {}

    for i, r in enumerate(rules):
        rule = r.split(":")
        rule[0] = int(rule[0])
        rules_dict[rule[0]] = rule[1]
        rule = [rule[0], rule[1].strip().strip("\"")]

        if rule[1].isalpha():
            pass
        
        elif "|" in rule[1]:
            rule = [rule[0], [x.strip() for x in rule[1].split("|")]]

            options = []
            for option_index, option in enumerate(rule[1]):
                option = list(map(int, option.split()))
                # print(f"option_index: {option_index}, option: {option}")
                options.append(option)
            rule[1] = options

        else:
            rule[1] = list(map(int, rule[1].split()))

        rules_dict[rule[0]] = rule[1]

    # parse messages
    for message in messages:
        FIRST_RULE = 0
        if is_valid(message, FIRST_RULE, rules_dict):
            # print(f"Matched: {message}")
            matches += 1
    return matches


def test_example1():
    with open(".\\AdventOfCode\\2020\\day19-test1-input.txt") as f:
        rules, messages = [x.splitlines() for x in f.read().split("\n\n")]

    assert count_matches(rules, messages) == 2


def test_example2():
    with open(".\\AdventOfCode\\2020\\day19-test2-input.txt") as f:
        rules, messages = [x.splitlines() for x in f.read().split("\n\n")]

    assert count_matches(rules, messages) == 2


if __name__ == "__main__":
    
    with open(".\\AdventOfCode\\2020\\day19-input.txt") as f:
        rules, messages = [x.splitlines() for x in f.read().split("\n\n")]

    print(f"Part 1: {count_matches(rules, messages)}")
