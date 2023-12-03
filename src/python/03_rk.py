#!/usr/bin/env python3
import sys
import re
"""

add up all the part numbers in the engine schematic
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
any number adjacent to a symbol
"""

def parse(infile):
    # (line, start, stop, number)
    # stop is exlusive. 3 char long from 0, line 2 is (2, 0, 3)
    l_pos_num = []
    # 2D array of line, pos
    l_pos_sym = []

    # solution 2
    l_pos_num_line = []
    # (start, stop, number)
    l_pos_gear = []
    for ln, line in enumerate(infile):
        line = line.rstrip()
        l_pos_sym.append([False] * len(line))
        l_pos_num_line.append([])
        # each line is a game
        for match in re.finditer(r"\d+", line):
            l_pos_num.append((ln, match.start(), match.end(), int(match.group())))
            l_pos_num_line[ln].append((match.start(), match.end(), int(match.group())))
        for match in re.finditer(r"[^.\d]", line):
            l_pos_sym[ln][match.start()] = True
        for match in re.finditer(r"\*", line):
            l_pos_gear.append((ln, match.start()))
        pass
    return l_pos_num, l_pos_sym, l_pos_num_line, l_pos_gear

def is_part(n, l_pos):
    l  = n[0]
    p1 = n[1]
    p2 = n[2]
    length = len(l_pos)
    width = len(l_pos[0])

    for p in range(p1 if p1 == 0 else p1 - 1, p2 if p2 == width else p2 + 1):
        if l != 0 and l_pos[l-1][p]:
            return True
        if l != length - 1 and l_pos[l+1][p]:
            return True
        if l_pos[l][p]:
            return True
    return False

def locate_gear(l_num_line, gl, gp):
    # assumes always 2 number matches
    l = []
    length = len(l_num_line)
    #  current line
    for start, stop, num in l_num_line[gl]:
        if stop == gp or start == gp + 1:
            l.append(num)
    # previous line
    if gl != 0:
        for start, stop, num in l_num_line[gl-1]:
            if gp >= start - 1 and gp <= stop:
                l.append(num)
    if gl != length - 1:
        for start, stop, num in l_num_line[gl+1]:
            if gp >= start - 1 and gp <= stop:
                l.append(num)

    if len(l) == 2:
        return l[0] * l[1]
    else:
        return 0


def sol():
    s1 = 0
    s2 = 0
    with open(sys.argv[1], 'r') as infile:
        l_num, l_pos, l_n_l, l_p_g = parse(infile)
        for n in l_num :
            if is_part(n, l_pos):
                s1 += n[3]
        for l, p in l_p_g:
            s2 += locate_gear(l_n_l, l, p)
    return s1, s2
    pass


s1, s2 = sol()
print(s1)
print(s2)
