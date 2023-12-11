#!/usr/bin/env python3
import sys
import collections

def parse(infile):
    '''
    build the map
    '''
    fullMap = [[c for c in line.strip()] for line in infile]
    return fullMap


def dis(pos1, pos2, empty_row, empty_col, sol2 = False):
    # empty col inside 
    dist = len([i for i in empty_row if (i - pos1[0]) * (i - pos2[0]) < 0])
    dist += len([i for i in empty_col if (i - pos1[1]) * (i - pos2[1]) < 0])

    dist *= (1000000-1) if sol2 else 1
    # test case
    #  dist *= (10-1) if sol2 else 1
    #  dist *= (100-1) if sol2 else 1

    dist += abs(pos1[0] - pos2[0])
    dist += abs(pos1[1] - pos2[1])

    #  print(pos1, pos2, dist)
    return dist


def sol1(m):
    height = len(m)
    width = len(m[0])
    l_galaxy = []
    l_empty_row = []
    l_empty_col = []

    for r, row_content in enumerate(m):
        all_dot = True
        for c, char in enumerate(row_content):
            if char == "#":
                l_galaxy.append((r, c))
                all_dot = False
        if all_dot:
            l_empty_row.append(r)

    for c in range(width):
        all_dot = True
        for r in range(height):
            if m[r][c] == "#":
                all_dot = False
        if all_dot:
            l_empty_col.append(c)


    #  print(l_empty_row)
    #  print(l_empty_col)
    s = 0
    s2 = 0
    for i in range(len(l_galaxy)):
        for j in range(i+1, len(l_galaxy)):
            s += dis(l_galaxy[i], l_galaxy[j], l_empty_row, l_empty_col)
            s2 += dis(l_galaxy[i], l_galaxy[j], l_empty_row, l_empty_col, True)
            pass
        pass
    return s, s2


def main():
    with open(sys.argv[1], 'r') as infile: 
        m = parse(infile)
        #  print(m)
        sol = sol1(m)
        print(sol[0])
        print(sol[1])
    pass

main()
