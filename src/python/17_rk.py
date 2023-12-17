#!/usr/bin/env python3
import sys
import collections

def parse():
    l = []
    with open(sys.argv[1], 'r') as infile:
        for line in infile:
            l.append([int(i) for i in line.strip()])
    return l


def dim(l):
    return len(l), len(l[0])

def sol_first(l, sol1 = True):
    height, width = dim(l)
    # min heat loss of ID=(pos row, pos col, direction row, direction col, step) : loss
    # the direction is how you enter this tile
    mhl = {}
    dq = collections.deque()
    # ID of five number, last is the loss before entering
    dq.append((0, 1, 0, 1, 1, 0))
    dq.append((1, 0, 1, 0, 1, 0))
    # need to know the min loss from all 3!
    #  while (height-1, width-1, 0) not in mhl or (height-1, width-1, 1) not in mhl or (height-1, width-1, 2) not in mhl:
    while len(dq):
        r, c, dr, dc, step, loss = dq.popleft()
        ID = (r, c, dr, dc, step)
        if r < 0 or c < 0 or r >= height or c >= width:
            # illegal step
            continue

        #  print(ID, loss)
        # new loss
        #  if not (r, c) == (0, 0):
        loss += l[r][c]
        if ID in mhl:
            if loss >= mhl[ID]:
                #  print("skip")
                # equal/more optimal scenario already considered
                continue

        # cache first
        mhl[ID] = loss
        
        # next step
        if sol1:
            # go straight
            if step < 3:
                dq.append((r+dr, c+dc, dr, dc, step+1, loss))
            # turn left/right
            # if going right or down, consider go up or left
            if dc > 0 or dr > 0:
                dq.append((r+dc, c+dr, dc, dr, 1, loss))
                dq.append((r-dc, c-dr, -dc, -dr, 1, loss))
            # if going left, only consider go down
            if dc < 0:
                dq.append((r+1, c, 1, 0, 1, loss))
            # if going up, only consider go right
            if dr < 0:
                dq.append((r, c+1, 0, 1, 1, loss))
        else:
            # go straight is a possibility  when steps < 10
            if step < 10:
                dq.append((r+dr, c+dc, dr, dc, step+1, loss))

            if step >= 4:
                # go left and right only when step is >=4
                if dc > 0 or dr > 0:
                    dq.append((r+dc, c+dr, dc, dr, 1, loss))
                    dq.append((r-dc, c-dr, -dc, -dr, 1, loss))
                # if going left, only consider go down
                if dc < 0:
                    dq.append((r+1, c, 1, 0, 1, loss))
                # if going up, only consider go right
                if dr < 0:
                    dq.append((r, c+1, 0, 1, 1, loss))
            pass
        pass

    #  print(mhl)
    
    return min([l for ID, l in mhl.items() if ID[0] == height - 1 and ID[1] == width - 1])

def main():
    l = parse()
    print(sol_first(l))
    print(sol_first(l, False))
    pass

main()
