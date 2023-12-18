#!/usr/bin/env python3
import sys
import util
import math

def parse():
    l = []
    with open(sys.argv[1], 'r') as infile:
        for line in infile:
            line = line.strip()
            di, step, color = line.split()
            color = color[2:-1]
            l.append((di, int(step), color))
    return l

def decode(color):
    return int(color[:5], 16), util.diDecode[int(color[5])]


def getSign(prev_di, di):
    if prev_di == "R" and di == "D" or prev_di == "U" and di == "L":
        return "7"
    elif prev_di == "R" and di == "U" or prev_di == "D" and di == "L":
        return "J"
    elif prev_di == "L" and di == "D" or prev_di == "U" and di == "R":
        return "F"
    elif prev_di == "L" and di == "U" or prev_di == "D" and di == "R":
        return "L"

def sol(l, sol1 = True):
    maxr, maxc = -math.inf, -math.inf
    minr, minc = math.inf, math.inf
    output = 0
    pos = (0, 0)
    for di, s, color in l:
        if not sol1:
            s, di = decode(color)
        pos = util.tuple_add(pos, util.tuple_mul(util.direction_map[di], s)) 
        output += s
        maxr = max(maxr, pos[0])
        maxc = max(maxc, pos[1])
        minr = min(minr, pos[0])
        minc = min(minc, pos[1])
    assert pos == (0, 0)

    nr = int(maxr-minr+1)
    nc = int(maxc-minc+1)

    #  a projection of (minr, minc) --> (0, 0)

    pos = (-minr, -minc)

    l_loop = util.matrix([[0 for j in range(nc)] for i in range(nr)])
    m = util.matrix([["." for j in range(nc)] for i in range(nr)])
    #  print(l_loop, m, sep="\n")


    # sort out the starting point first
    prev_di = ""
    for di, s, color in l:
        if not sol1:
            s, di = decode(color)
        if prev_di != "":
            m[pos] = getSign(prev_di, di)
        for i in range(s):
            pos = util.tuple_add(pos, util.direction_map[di]) 
            l_loop[pos] = 1

            if di == "D" or di == "U":
                m[pos] = "|"
            elif di == "L" or di == "R":
                m[pos] = "-"

            pass
        prev_di = di
        pass
    m[pos] = getSign(l[-1][0], l[0][0])
    #  print(pos, m[pos])

    #  print(l_loop, m, sep="\n")

    output += util.calculate_inside(l_loop, m)
    return output

def sol2(l, sol2=True):
    maxr, maxc = -math.inf, -math.inf
    minr, minc = math.inf, math.inf
    l_boundary = {0:{}}
    output = 0
    pos = (0, 0)
    first_di = None
    prev_di = None
    for di, s, color in l:
        if sol2:
            s, di = decode(color)
        if not first_di:
            first_di = di

        # correct the turning point
        if prev_di != "":
            l_boundary[pos[0]][pos[1]] = getSign(prev_di, di)

        prev_di = di
        if di == "U" or di == "D":
            for i in range(s):
                pos = util.tuple_add(pos, util.direction_map[di]) 
                if pos[0] in l_boundary:
                    l_boundary[pos[0]][pos[1]] = "|"
                else:
                    l_boundary[pos[0]] = {pos[1]:"|"}
        else:
            pos = util.tuple_add(pos, util.tuple_mul(util.direction_map[di], s)) 
            pass

        output += s
        maxr = max(maxr, pos[0])
        maxc = max(maxc, pos[1])
        minr = min(minr, pos[0])
        minc = min(minc, pos[1])
        pass
    assert pos == (0, 0)

    l_boundary[0][0] = getSign(prev_di, first_di)
    #  print(l_boundary)
    #  print(l_boundary[0][0])

    inside = False
    s_prevline = 0
    l_prevline = None
    for r in range(minr, maxr+1):
        lb = sorted([(i, j) for i, j in  l_boundary[r].items()], key = lambda x:x[0])
        #  print(lb)
        if l_prevline == lb:
            output += s_prevline
            continue
        s_prevline = 0
        l_prevline = lb

        ib = 0
        l_group = []
        inside = False
        true_next = False
        prev_type_bound = None
        prev_pos   = None
        for ib in range(len(lb)-1):
            p1, s1 = lb[ib]
            p2, s2 = lb[ib+1]
            dist = p2-p1-1

            if s1+s2 in ["F7", "LJ"]:
                true_next = False
                continue
            elif s1 == "|" or true_next:
                true_next = False
                inside = not inside
            elif s1+s2 in ["FJ", "L7"]:
                true_next = True
                continue

            if inside:
                s_prevline += dist
        output += s_prevline
        #  print(output, s_prevline)
    return output

def main():
    l = parse()
    #  print(l)
    #  print(sol(l))
    print(sol2(l, False))
    print(sol2(l))
    pass

main()
