#!/usr/bin/env python
import sys, math, util
import collections
from heapq import heappop, heappush
"""
assumption: boundary are all dots.
"""

def parse():
    m = []
    si, sj = 0, 0
    with open(sys.argv[1], 'r') as infile:
        for i, line in enumerate(infile):
            line = line.strip()
            if "S" in line:
                si = i
                sj = line.find("S")
            m.append([c for c in line])
    return (si, sj), util.matrix(m)

def walk(pos, m):
    """
    check inbound
    attempt to walk in 4 direction, yield as long as it's not #
    """
    for di in range(4):
        di_vec = util.direction_map[util.diDecode[di]]
        newpos = util.tuple_add(pos, di_vec)
        if m[newpos] == "#":
            continue
        else:
            yield newpos


def find_for_one(s, m):
    """
    given a starting point in a block, 
    find the distance of all points and return
    """
    visited = {}
    dq = collections.deque()
    dq.append((s, 0))
    step = 0
    while len(dq):
        pos, step = dq.popleft()
        if not m.inbound(pos):
            continue
        if pos in visited:
            continue
        visited[pos] = step
        for newpos in walk(pos, m):
            if not m.inbound(newpos):
                continue
            dq.append((newpos, step+1))

    tup = collections.namedtuple('StartEndMap', 'R, D, L, U, max')

    minR, minD, minL, minU = math.inf, math.inf, math.inf, math.inf
    posR, posD, posL, posU = [], [], [], []
    for r in range(m._nr):
        if visited[(r, 0)] < minL:
            minL = visited[(r, 0)]
            posL = [(r, 0)]
        if visited[(r, 0)] == minL:
            posL += [(r, 0)]

        if visited[(r, m._nc-1)] < minR:
            minR = visited[(r, m._nc-1)]
            posR = [(r, m._nc-1)]
        if visited[(r, m._nc-1)] == minR:
            posR += [(r, m._nc-1)]
        pass

    for c in range(m._nc):
        if visited[(0, c)] < minU:
            minU = visited[(0, c)]
            posU = [(0, c)]
        if visited[(0, c)] == minU:
            posU += [(0, c)]

        if visited[(m._nr-1, c)] < minD:
            minD = visited[(m._nr-1, c)]
            posD = [(m._nr-1, c)]
        if visited[(m._nr-1, c)] == minD:
            posD += [(m._nr-1, c)]

    max_step = max(visited.values())

    tup.R = [posR, minR]
    tup.D = [posD, minD]
    tup.L = [posL, minL]
    tup.U = [posU, minU]
    tup.max = max_step 

    return tup, visited

def sol2_old(s, m, ns):
    # save pos:0 or 1, for even or odd steps
    visited = {}
    dq = collections.deque()
    dq.append((s, 0))
    step = 0
    while len(dq):
        pos, step =  dq.popleft()
        global_pos = (pos[0] // m._nr, pos[1] // m._nc)
        local_pos = (pos[0] % m._nr, pos[1] % m._nc)

        if pos in visited:
            continue
        visited[pos] = step
        if step >= ns:
            continue

        for newpos in walk(local_pos, m):
            dq.append(((global_pos[0] * m._nr + newpos[0], global_pos[1] * m._nc + newpos[1]), step+1))
        pass

    sum = 0
    for _, s in visited.items():
        if (s % 2) == (ns % 2):
            sum += 1
    #  print(len(visited))
    return visited

def sol1(s, m, ns):
    # save pos:0 or 1, for even or odd steps
    visited = {}
    dq = collections.deque()
    dq.append((s, 0))
    step = 0
    while len(dq):
        pos, step =  dq.popleft()
        if pos in visited:
            continue
        #  print(pos)
        visited[pos] = step % 2
        if step >= ns:
            continue
        for newpos in walk(pos, m):
            if not m.inbound(newpos):
                continue
            dq.append((newpos, step+1))
        pass

    sum = 0
    for _, s in visited.items():
        if s == ns % 2:
            #  print(_)
            sum += 1
    #  print(visited)
    return sum

def sol2(s, m, ns):
    # m is a square
    nr, nc = m.dim()

    max_step_cross_block = nc + nr 

    # position end : named tuple (R, D, L, U, max)
    # R, D, L, U are tuple of (list of pos, min step)
    border_map = { s : find_for_one(s, m) }

    for r in range(nr):
        for c in range(nc):
            if r != 0 and r != nr-1 and c != 0 and c != nc-1:
                continue
            pos = (r, c)
            if m[pos] == "#":
                continue
            border_map[pos] = find_for_one(pos, m)

    # save maxed out block, and it has the same even/oddity for 0 and 1
    maxed_out_visited_blocks = {}
    # non-maxed out. (globalpos, realpos) : step
    # in case it is maxed out somewhere else
    boundary_block_visited = {}
    dq = []
    #  step 0 and the "real start"
    heappush(dq, (0, s) )
    while len(dq):
        # prioritize lower steps
        step, pos = heappop(dq)
        #  print(pos)

        if step > ns: 
            continue

        global_pos = (pos[0] // nr, pos[1] // nc)
        local_pos = (pos[0] % nr, pos[1] % nc)

        if (global_pos, local_pos) in boundary_block_visited and boundary_block_visited[(global_pos, local_pos)] <= step:
            continue

        boundary_block_visited[(global_pos, local_pos)] = step

        if step == ns:
            continue

        diff_even_odd = int((local_pos[0] - s[0] + local_pos[1] - s[1]) % 2 != step % 2)

        # this block is visited before, and is calculated to be maxed out.
        # mathematically I am not sure, but I feel that the priority queue should satisfy this..?
        #  if global_pos in maxed_out_visited_blocks:
            #  continue
        #  if global_pos in maxed_out_visited_blocks and step + tup.max + 3 * max_step_cross_block < ns:
            #  # maxed out by others, do nothing
            #  continue

        # check if this specific start is stored already 
        if local_pos not in border_map:
            raise RuntimeError("YOU ALWAYS START IN A BOUNDARY/START FOR A BLOCK.")

        tup, visited = border_map[local_pos]
        # you'll flood all blocks before you run out of steps.
        if step + tup.max < ns:
            if global_pos not in maxed_out_visited_blocks:
                # if not maxed out by others yet
                maxed_out_visited_blocks[global_pos] = diff_even_odd
                pass

        #  elif global_pos in maxed_out_visited_blocks and step + tup.max + max_step_cross_block < ns:
            #  # maxed out by others, do nothing
            #  continue
        else: 
            # newstep includes itself
            for new_local_pos, newstep in visited.items():
                if step + newstep > ns:
                    continue
                boundary_block_visited[(global_pos, new_local_pos)] = step + newstep

                #  lpr = new_local_pos[0]
                #  lpc = new_local_pos[1]
                #  if lpr == 0 or lpc == 0 or lpc == nc-1 or lpr == nr-1:
                    #  #  consider three other edges
                    #  curr_pos = (global_pos[0] * nr + lpr, global_pos[1] * nc + lpc)
                    #  if lpr == 0 and step+newstep+1 <= ns: #U
                        #  heappush(dq, (step+newstep+1, util.tuple_add(curr_pos, util.direction_map["U"])))
                    #  if lpc == 0 and step+newstep+1 <= ns: #L
                        #  heappush(dq, (step+newstep+1, util.tuple_add(curr_pos, util.direction_map["L"])))
                    #  if lpr == nr-1 and step+newstep+1 <= ns: #D
                        #  heappush(dq, (step+newstep+1, util.tuple_add(curr_pos, util.direction_map["D"])))
                    #  if lpc == nc-1 and step+newstep+1 <= ns: #R
                        #  heappush(dq, (step+newstep+1, util.tuple_add(curr_pos, util.direction_map["R"])))
                    #  pass

        #  well if you reach here, let's consider the next block..
        #  for newpos, extra_step in mapwalk(global_pos, tup, m):
            #  if step + extra_step <= ns:
                #  heappush(dq, (step+extra_step, newpos))

        for new_local_pos, newstep in visited.items():
            lpr = new_local_pos[0]
            lpc = new_local_pos[1]
            if lpr == 0 or lpc == 0 or lpc == nc-1 or lpr == nr-1:
                #  consider three other edges
                curr_pos = (global_pos[0] * nr + lpr, global_pos[1] * nc + lpc)
                if lpr == 0 and step+newstep+1 <= ns: #U
                    heappush(dq, (step+newstep+1, util.tuple_add(curr_pos, util.direction_map["U"])))
                if lpc == 0 and step+newstep+1 <= ns: #L
                    heappush(dq, (step+newstep+1, util.tuple_add(curr_pos, util.direction_map["L"])))
                if lpr == nr-1 and step+newstep+1 <= ns: #D
                    heappush(dq, (step+newstep+1, util.tuple_add(curr_pos, util.direction_map["D"])))
                if lpc == nc-1 and step+newstep+1 <= ns: #R
                    heappush(dq, (step+newstep+1, util.tuple_add(curr_pos, util.direction_map["R"])))
        pass

    _, visited = border_map[s]

    l_even_odd = [0, 0]
    for steps in visited.values():
        l_even_odd[steps % 2] += 1
    #  print(l_even_odd)

    even_odd_sign = ns % 2
    tile = 0
    visited = {}
    for global_pos, diff_eo in maxed_out_visited_blocks.items():
        #  if diff is false, be the same as the original map
        for pos, step in border_map[s][1].items():
            npr = global_pos[0] * m._nr + pos[0]
            npc = global_pos[1] * m._nc + pos[1]
            visited[(npr, npc)] = (step + diff_eo) % 2
        tile += l_even_odd[(even_odd_sign + diff_eo) % 2]
        pass
    
    d = {}
    for (global_pos, local_pos), step in boundary_block_visited.items():
        dd = {}
        if global_pos in d:
            dd = d[global_pos]
        else:
            d[global_pos] = dd
        dd[local_pos] = step
        pass

    for gp, dd in d.items():
        #  print(gp)
        for p, s in dd.items():
            #  print(p, s)
            pass

    for (global_pos, local_pos), step in boundary_block_visited.items():
        npr = global_pos[0] * m._nr + local_pos[0]
        npc = global_pos[1] * m._nc + local_pos[1]
        visited[(npr, npc)] = step
        if global_pos in maxed_out_visited_blocks:
            continue
        elif step % 2 == even_odd_sign:
            tile += 1
    #  print("result", tile)
    return tile





def getN(l, m, ns):
    """
    s is the remaining step. 
    when step == ns, that's the last step, the state to check
    so (ns - step) % == 0 is the condition for summing
    """
    visited = {}
    output = 0
    dq = collections.deque()
    for pos in l:
        dq.append((pos, 1))
    while len(dq):
        pos, step = dq.popleft()
        if not m.inbound(pos):
            continue
        if pos in visited:
            continue
        visited[pos] = step

        if (ns - step) % 2 == 0:
            output += 1

        if step == ns:
            # stop processing
            continue

        for newpos in walk(pos, m):
            if not m.inbound(newpos):
                continue
            dq.append((newpos, step+1))
    return output

def sol2_cheat(s, m, ns):
    """
    matrix has dim of mxn, assuming it's nxn
    1. from one start to another start, there's no #, it takes n steps precisely
    2. it takes n-1 to flood a whole block from the start
        therefore, after n-1 step, the first block is flood.
                   after n step, the neighboring start is reached. The edge of the neighboring block also start to flood
                   after 2n step, the flood from the 2nd start permeates the entier 2nd block. The flood from the edge is not faster. 
    3. start is at the center
        this is important because it guarantees that at n//2 step, the flood side way does not beat the central one
    """

    _, visited = find_for_one(s, m)

    dim = m._nr
    center = s[0]

    l_even_odd = [0, 0]
    for steps in visited.values():
        l_even_odd[steps % 2] += 1
    #  print(l_even_odd)

    output = 0
    nblock = ns // dim - 1
    #  print(nblock)

    # total nsteps to arrive at the boundary(before entering corner tile)
    #  nsteps = nblock * dim - center
    #  remain = ns - nsteps

    #  1 + 2 + .. (nblock + 1) + nblock + ... + 2 + 1 for the outer
    #      1 + 2 + ... + nblock + (nblock - 1) + ... + 2 + 1
    #  s_outer = (1 + nblock) * nblock + (nblock + 1)
    #  s_inner = (1 + nblock-1) * (nblock - 1) + nblock

    s_outer = (nblock+1) **2
    s_inner = nblock ** 2

    sign_outer = (nblock + ns) % 2
    sign_inner = (nblock + ns + 1) % 2

    output += s_outer * l_even_odd[sign_outer]
    output += s_inner * l_even_odd[sign_inner]

    # now calculate the rims
    l = [(center, 0),
         (0, center),
         (center, dim-1),
         (dim-1, center)]
    for i, pos in enumerate(l):
        # 4 corners
        output += getN([pos], m, ns - dim * nblock - center)


    for pos in [(dim-1, dim-1), (dim-1, 0), (0, dim-1), (0, 0)]:
        # 4 rims(each has nblock)
        output += getN([pos], m, ns - dim * (nblock - 1) - 2 * center - 1) * nblock
        # 4 secondary rim enters from the corner
        output += getN([pos], m, ns - dim * nblock - 2 * center -1) * (nblock + 1)

    return output

def main():
    s, m = parse()
    #  print(m)
    #  print(s)
    #  print(m.dim())

    # example
    #  print(sol1(s, m, 6))
    print(sol1(s, m, 64))
    #  print()
    #  print(sol2(s, m, 0))
    #  print(sol2(s, m, 1))
    #  print(sol2(s, m, 2))
    #  print(sol2(s, m, 3))
    #  print(sol2(s, m, 4))
    #  #  print(sol2(s, m, 5))

    #  v1 = sol2(s, m, 50)
    #  print(v1)
    #  v2 = sol2_old(s, m, 50)
    #  for x, step in v2.items():
        #  if step % 2 != 10 % 2:
            #  continue
        #  if x not in v1:
            #  print("missing", x)
        #  elif step % 2 != v1[x] % 2:
            #  print("different even/odd", x)
    #  print(sol2(s, m, 6))
    #  print(sol2_old(s, m, 6))
    #  print()

    #  print(sol2(s, m, 8))
    #  print(sol2_old(s, m, 8))
    #  print()

    #  print(sol2(s, m, 10))
    #  print(sol2_old(s, m, 10))
    #  print()

    #  _, v = find_for_one(s, m)
    #  print(m._nc, m._nr)
    #  print(max(v.values()))

    #  print(sol2_cheat(s, m, 6))
    #  print(sol2_cheat(s, m, 10))
    #  print(sol2_cheat(s, m, 50))
    #  print(sol2_cheat(s, m, 100))
    #  print(sol2_cheat(s, m, 500))
    #  print(sol2_cheat(s, m, 1000))
    #  print(sol2_cheat(s, m, 5000))

    #  print(sol1(s, m, 64))
    #  print(sol2_cheat(s, m, 131))
    print(sol2_cheat(s, m, 26501365))
    pass

main()
