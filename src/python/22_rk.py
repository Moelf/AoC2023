#!/usr/bin/env python3
import sys, math, util
from collections import namedtuple, deque

Brick = namedtuple("LongBrick", "x, y, z")

def parse():
    m = []
    with open(sys.argv[1], 'r') as infile:
        for i, line in enumerate(infile):
            start_str, end_str = line.strip().split("~")
            # it's ok to provide ranges I supppose, memory should fit
            start = [int(i) for i in start_str.split(",")]
            end   = [int(i) for i in end_str.split(",")]
            brick = Brick((start[0], end[0]+1),
                          (start[1], end[1]+1),
                          (start[2], end[2]+1),
                           )
            m.append(brick)
    return sorted(m, key = lambda x : x.z)

def fall(bricks_ss):
    nbrick = len(bricks_ss)
    minx, miny = min(b.x[0] for b in bricks_ss), min(b.y[0] for b in bricks_ss)
    assert minx == 0
    assert miny == 0
    maxx, maxy = max(b.x[0] for b in bricks_ss), max(b.y[0] for b in bricks_ss)
    # holding matrix 
    # first index, the holding brick
    # second index, the brick being hold
    # brick indexed from 1...nbrick, 0 means ground
    m_hold = [[False for i in range(nbrick + 1)] for j in range(nbrick + 1)]

    # the heatmap of height for actual falling, and
    # the index of the brick occupying the highest spot, initialize with ground 0
    highest_brick = util.matrix([[(0, 0) for i in range(maxy+1)] for j in range(maxx+1)])
    #  print(highest_brick)

    for ib, b in enumerate(bricks_ss):
        expected_zpos = 0
        zlength = b.z[1] - b.z[0]
        for x in range(*b.x):
            for y in range(*b.y):
                expected_zpos = max(highest_brick[(x, y)][0] + 1, expected_zpos)

        #  print("expected ", ib, expected_zpos, zlength)
        # fall and record map
        for x in range(*b.x):
            for y in range(*b.y):
                if highest_brick[(x, y)][0] == expected_zpos - 1:
                    m_hold[highest_brick[(x, y)][1]][ib+1] = True
                # update the heat map and current higehst brick index
                highest_brick[(x, y)] = (expected_zpos + zlength - 1, ib+1)

        #  [print(i) for i in m_hold]
        #  print(highest_brick)
        pass

    return m_hold

def sol1(m_hold):
    nbricks = len(m_hold) - 1
    nbrick = 0

    l_cannot_remove = []

    for ibrick in range(1, nbricks + 1):
        can_remove = True
        for isb, supported_brick in enumerate(m_hold[ibrick]):
            # consider each of the supported brick
            if not supported_brick: continue

            # try to find other supporting brick. (ground is not possible)
            found_other_support = False
            for i_other_support in range(1, nbricks + 1):
                if i_other_support != ibrick and m_hold[i_other_support][isb]:
                    found_other_support = True

            if not found_other_support:
                can_remove = False
        if can_remove: nbrick += 1
        else: l_cannot_remove.append(ibrick)
        pass




    # part 2
    nfall = 0
    for remove in l_cannot_remove:
        this_fall = set()
        # WFS
        dq = deque([remove])
        while len(dq):
            ibrick = dq.popleft()
            if ibrick in this_fall:
                continue
            this_fall.add(ibrick)
            #  print(f"consider {ibrick}")
            for isb, supported_brick in enumerate(m_hold[ibrick]):
                if not supported_brick: continue
                #  print("will it fall", isb)

                found_other_support = False
                for i_other_support in range(1, nbricks + 1):
                    if i_other_support not in this_fall and m_hold[i_other_support][isb]:
                        found_other_support = True
                if not found_other_support:
                    dq.append(isb)
        nfall += len(this_fall) - 1
        #  print(remove, len(this_fall) - 1)
    return nbrick, nfall



def main():
    ss = parse()
    #  [print(i) for i in ss]
    m_hold = fall(ss)
    #  print(m_hold)
    #  [print(i) for i in m_hold]
    print(*sol1(m_hold), sep = "\n")
    pass

main()
