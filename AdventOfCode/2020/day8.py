# Advent of Code Day 8
# https://adventofcode.com/2020/day/8


import copy
import pytest


class Machine():
    
    def __init__(self, code):
        """
        Arguments
        code : list
            The list of instructions to execute.
        """
        # initialize state
        self.code = code
        self.ip = 0  # instruction pointer
        self.acc = 0  # accumulator
        self.history_instructions = []  # list of instructions executed
        self.history_states = []  # list of tuples (new_ip, new_acc) after the corresponding instruction was executed


    def execute(self):
        """Execute a single instruction."""

        # check if this instruction executed already
        if self.ip in self.history_instructions:
            raise RuntimeError("Infinite loop detected at instruction " + str(self.ip) + ", " + self.code[self.ip] + ". Machine state: " + str(self.history_states[-1]))

        # check to terminate code
        if self.ip == len(self.code):
            # print("Terminated")
            return 0 
        
        old_ip = self.ip
        instruction, operand = self.code[self.ip].split()
        operand = int(operand)

        if instruction == "acc":
            self.acc += operand
            self.ip += 1
        elif instruction == "jmp":
            self.ip += operand
        elif instruction == "nop":
            # move to next instruction
            self.ip += 1

        self.history_instructions.append(old_ip)
        self.history_states.append((self.ip, self.acc))

        return self.ip

    
    def run(self):
        try:
            while self.execute():
                pass
        except RuntimeError as exc:
            # print(exc)
            pass


def test_init():
    code = []
    m = Machine(code)
    assert m
    assert m.code == code
    assert m.acc == 0
    assert m.ip == 0


def test_acc():
    code = ["acc +1", "acc -1"]
    m = Machine(code)
    m.execute()
    assert m.acc == 1
    assert m.ip == 1

    m.execute()
    assert m.acc == 0
    assert m.ip == 2


def test_jmp():
    code = ["jmp +2", "jmp +1", "jmp -2"]
    m = Machine(code)
    m.execute()
    assert m.acc == 0
    assert m.ip == 2

    m.execute()
    assert m.acc == 0
    assert m.ip == 0


def test_nop():
    code = ["nop +2", "nop +1", "nop -2"]
    m = Machine(code)
    m.execute()
    assert m.acc == 0
    assert m.ip == 1

    m.execute()
    assert m.acc == 0
    assert m.ip == 2


def test_input1_part1():
    with open(".\\AdventOfCode\\2020\\day8-test-input.txt") as f:
        code = [line.rstrip() for line in f]
    
    m = Machine(code)

    # execute until instruction tries to execute twice
    with pytest.raises(RuntimeError) as exc:
        while True:
            m.execute()
    print(exc)


def test_input2_part2():
    with open(".\\AdventOfCode\\2020\\day8-test-input.txt") as f:
        code = [line.rstrip() for line in f]
    
    for i in range(len(code)):
        test_code = copy.copy(code)
        if test_code[i].split()[0] == "jmp":
            test_code[i] = "nop" + test_code[i][3:]
        elif test_code[i].splitlines()[0] == "nop":
            test_code[i] = "jmp" + test_code[i][3:]
        else:
            continue

        m = Machine(test_code)
        m.run()
        # if m.history_states[-1][1] == 8:
        if m.ip == len(m.code):
            break

    assert m.history_states[-1][1] == 8


if __name__ == "__main__":
    # test_input1_part1()

    with open(".\\AdventOfCode\\2020\\day8-input.txt") as f:
        code = [line.rstrip() for line in f]
    
    m = Machine(code)

    # execute until instruction tries to execute twice
    try:
        while m.execute():
            # print(m.history_states[-1])
            pass
            
    except RuntimeError as exc:
        print(exc)
        print("Part 1:", m.history_states[-1][1])

    # Part 2
    for i in range(len(code)):
        test_code = copy.copy(code)
        if test_code[i].split()[0] == "jmp":
            test_code[i] = "nop" + test_code[i][3:]
        elif test_code[i].splitlines()[0] == "nop":
            test_code[i] = "jmp" + test_code[i][3:]
        else:
            continue

        m = Machine(test_code)
        m.run()

        if m.ip == len(m.code):
            print("Part 2:", m.history_states[-1][1])

