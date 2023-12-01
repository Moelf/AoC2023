#!/usr/bin/env python3

import sys
def sol1():
    sum=0
    with open(sys.argv[1], 'r') as infile:
        for line in infile:
            digit1 = 0
            digit2 = 0
            for c in line:
                if c.isdigit():
                    digit1 = int(c)
                    break
            for c in line[::-1]:
                if c.isdigit():
                    digit2 = int(c)
                    break
            sum += digit1*10 + digit2
        print(sum)

LUT = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        ]


def find_min(line, tofind, num, min_pos):
    pos = line.find(tofind)
    if pos != -1 and pos < min_pos:
        return pos, num

def find_max(line, tofind, num, max_pos):
    pos = line.find(tofind)
    if pos != -1 and pos > max_pos:
        return pos, num

def find_code(line):
    """
    return the code for each line
    assumes code exists
    """
    min_pos, min_num = len(line), -1
    max_pos, max_num = -1, -1
    line = line.lower()
    for i, numstr in enumerate(LUT):
        num = i + 1

        pos = line.find(numstr)
        if pos != -1 and pos < min_pos:
            min_pos = pos
            min_num = num
        pos = line.find(str(num))
        if pos != -1 and pos < min_pos:
            min_pos = pos
            min_num = num

        pos = line.rfind(numstr)
        if pos != -1 and pos > max_pos:
            max_pos = pos
            max_num = num
        pos = line.rfind(str(num))
        if pos != -1 and pos > max_pos:
            max_pos = pos
            max_num = num
        pass
    return min_num * 10 + max_num

def sol2():
    sum=0
    with open(sys.argv[1], 'r') as infile:
        for line in infile:
            sum += find_code(line)
            pass
        print(sum)

sol1()
for i in """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""".splitlines():
    #  print(find_code(i))
    pass
sol2()
