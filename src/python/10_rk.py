#!/usr/bin/env python3
import sys
import collections
import util

"""
assuming there is loop
"""

def parse(infile):
    '''
    build the map
    '''
    l = [[c for c in line.strip()] for line in infile]
    for i, line in enumerate(l):
        if "S" in line:
            return l, (i, line.index("S"))

def walk(m, l):
    """
    failed attempt to do recursion

    the entier map, the tiles you've already stepped on
        last of the been to is the current

        return finding the loop
    """
    x = l[-1][0]
    y = l[-1][1]

    #  print(m[x][y], l)

    if len(l) >= 3 and l[-3][0] != -1 and l[-3][1] != -1 and l[-3][0] == x and l[-3][1] == y:
        # you have just turned around..
        #  print("repeat")
        return False, None
    elif m[x][y] == "S" and len(l) >= 4 :
        # find the loop(min size 4)
        #  print("Find")
        return True, l


    if x > 0 and m[x][y] in set(["|", "J", "L", "S"])                 and m[x-1][y] in set(["F", "7", "|", "S"]):
        # try going up
        #  print("Up")
        solved, lout = walk(m, l + [[x-1, y]])
        if solved:
            return True, lout
    if x < len(m) - 1 and m[x][y] in set(["|", "F", "7", "S"])        and m[x+1][y] in set(["J", "L", "|", "S"]):
        # try going down
        #  print("Down")
        solved, lout = walk(m, l + [[x+1, y]])
        if solved:
            return True, lout
    if y > 0 and m[x][y] in set(["7", "J", "-", "S"])             and m[x][y-1] in set(["F", "L", "-", "S"]):
        # try going left
        #  print("Left")
        solved, lout = walk(m, l + [[x, y-1]])
        if solved:
            return True, lout
    #  print(m[x][y], l)
    if y < len(m[0]) - 1 and m[x][y] in set(["L", "F", "-", "S"]) and m[x][y+1] in set(["J", "7", "-", "S"]):
        # try going right
        print("Right")
        solved, lout = walk(m, l + [[x, y+1]])
        if solved:
            return True, lout

    # should not end here..
    return False, l

"""
legal direction to go IN this tile
"""
dlegal = {
        "-":[(0, 1),  (0, -1)],
        "|":[(1,  0),  (-1, 0)],
        "L":[(0, -1), (1, 0)],
        "J":[(0, 1),  (1, 0)],
        "F":[(0, -1), (-1, 0)],
        "7":[(0, 1),  (-1, 0)],
        }

def next(m, pos, d):
    """
    current is pos, direction is where it is coming from

    check if it's legal
    """

    # is it out of bound?
    if pos[0] < 0 or pos[0] >= len(m) or pos[1] < 0 or pos[1] >= len(m[0]):
        return False

    # ending tile legality
    t = m[pos[0]][pos[1]]

    if t == ".":
        return False

    # current and previous must both be legal
    if d not in dlegal[t]:
        return False

    # next position must the the other direction, in the going OUT direction
    dIN = dlegal[t][1 - dlegal[t].index(d)]
    return (-dIN[0], -dIN[1])

def sol1(IN):
    m = IN[0]
    height = len(m)
    width = len(m[0])
    pos = IN[1]
    to_try = collections.deque([ (-1, 0), (1, 0), (0, -1), (0, 1) ])

    dinitial = ()
    nstep = 0
    # 0 is not boundary
    # 1 is boundary
    l_loop = [[0 for i in range(width)] for j in range(height)]
    d = ()
    while len(to_try) > 0:
        if nstep == 0:
            #  print("FROM THE START")
            d = to_try.popleft()
            dinitial = d
            pass
        # walk, and check legality
        nstep += 1
        pos = (pos[0] + d[0], pos[1] + d[1])
        l_loop[pos[0]][pos[1]] = 1
        #  print("walk in", d, "arrive at", pos)

        if m[pos[0]][pos[1]] == "S" and nstep >= 4:
            break

        d = next(m, pos, d)
        if not d:
            nstep = 0
            l_loop = [[0 for i in range(width)] for j in range(height)]
            pos = IN[1]
            # if not legal, continue!
            pass
        pass

    # replace S with meaningful pipe
    for c, legal in dlegal.items():
        if (-dinitial[0], -dinitial[1]) not in legal:
            continue
        if d not in legal:
            continue
        m[IN[1][0]][IN[1][1]] = c
            
    ninside = util.calculate_inside(l_loop, m)


    #  print(l_loop)
    #  #  initialize outtermost boundary first
    #  for i in range(width + 2):
        #  l_loop[0][i] = 2
        #  l_loop[height + 1][i] = 2
    #  for i in range(height + 2):
        #  l_loop[i][0] = 2
        #  l_loop[i][width + 2] = 2

    #  d = 1
    #  #  check line by looking at boundary that is not '-'
    #  # get the outtermost boundary first
    #  for x in range(d, height + 2 - d):
        #  for x in range(d, width + 2 - d):


    return nstep  // 2, ninside

def main():
    with open(sys.argv[1], 'r') as infile: 
        l = parse(infile)
        #  print(l)
        sol = sol1(l)
        print(sol[0])
        print(sol[1])
    pass

main()
