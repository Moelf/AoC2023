#!/usr/bin/env python3
import sys
import collections

def parse():
    l = []
    with open(sys.argv[1], 'r') as infile:
        for line in infile:
            l.append(line.strip())
    return l

def sol1(l):
    togo = collections.deque([((0, 0), (0, 1))])
    return sol(l, togo)

def sol2(l):
    width = len(l[0])
    height = len(l)

    s = 0

    # edges
    for i in range(0, width):
        cmd = ((0, i), (1, 0))
        s = max(s, sol(l, collections.deque([cmd])))
        cmd = ((height-1, i), (-1, 0))
        s = max(s, sol(l, collections.deque([cmd])))
        pass
    for i in range(0, height):
        cmd = ((i, 0), (0, 1))
        s = max(s, sol(l, collections.deque([cmd])))
        cmd = ((i, width-1), (0, -1))
        s = max(s, sol(l, collections.deque([cmd])))
        pass

    # list of tuple of set
    #  l_corner = []
    #  for pos in [
            #  (0, 0),
            #  (0, width-1),
            #  (height-1, 0),
            #  (height-1, width-1),
            #  ]:
        #  s1 = sol(l, collections.deque([(pos, (0, 1 if pos[1] == 0 else -1))]))
        #  s2 = sol(l, collections.deque([(pos, (1 if pos[0] == 0 else -1, 0))]))
        #  l_corner.append([s1, s2])
    
    #  s = 0
    #  for i in range(16):
        #  v = visited
        #  v = v.union(l_corner[0][(i) & 1])
        #  v = v.union(l_corner[1][(i >> 1) & 1])
        #  v = v.union(l_corner[2][(i >> 2) & 1])
        #  v = v.union(l_corner[3][(i >> 3) & 1])
        #  s = max(s, len(v))
    return s


def sol(l, togo):
    visited = set()
    width = len(l[0])
    height = len(l)
    while len(togo):
        # position and direction
        pos, di = togo.pop()
        if pos[0] < 0 or pos[0] >= height or pos[1] < 0 or pos[1] >= width:
            continue
        if (pos, di) in visited:
            continue
        visited.add((pos, di))

        sign = l[pos[0]][pos[1]]

        if sign == "." or (sign == "-" and di[0] == 0) or (sign == "|" and di[1] == 0):
            # go in the same direction
            togo.append(((pos[0] + di[0], pos[1] + di[1]), di))
        elif sign == "-":
            # go in two horizontal direction (y)
            togo.append(((pos[0], pos[1] + 1), (0,  1)))
            togo.append(((pos[0], pos[1] - 1), (0, -1)))
        elif sign == "|":
            # go in two horizontal direction (y)
            togo.append(((pos[0] + 1, pos[1]), (1,  0)))
            togo.append(((pos[0] - 1, pos[1]), (-1, 0)))
        elif sign == "/":
            # go in two horizontal direction (y)
            togo.append(((pos[0] - di[1], pos[1] - di[0]), (-di[1],  -di[0])))
        elif sign == "\\":
            # go in two horizontal direction (y)
            togo.append(((pos[0] + di[1], pos[1] + di[0]), (di[1],  di[0])))
            pass
        pass
    return len(set([pos for pos, _ in visited]))

def main():
    l = parse()
    print(sol1(l))
    print(sol2(l))
    pass

main()
