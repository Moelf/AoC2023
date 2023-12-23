#!/usr/bin/env python3
import sys, math, util
import collections

def parse():
    m = util.matrix()
    with open(sys.argv[1], 'r') as infile:
        for i, line in enumerate(infile):
            m[i] = [i for i in line.strip()]
    return m


def find_start_end(m):
    s = None
    e = None
    for i, c in enumerate(m[0]):
        if c == ".":
            s =  (0, i)
    for i, c in enumerate(m[-1]):
        if c == ".":
            e =  (m.dim()[0] - 1, i)
    #  print(m.dim())
    #  print(s, e)
    return (s, e)

def walk(pos, m, l_visited, sol2):
    """
    yield one by one all possible direction to go
    """
    slope = [">", "v", "<", "^"]
    if not sol2:
        if m[pos] in slope:
            di = slope.index(m[pos])
            new_pos = util.tuple_add(pos, util.direction_map[util.diDecode[di]])
            # ASSUMPTION: no check of whether slope is legal
            yield (di, new_pos)
            return

    for di in range(4):
        new_pos = util.tuple_add(pos, util.direction_map[util.diDecode[di]])
        if new_pos in l_visited :
            continue
        if not m.inbound(new_pos):
            continue
        if m[new_pos] == "#":
            continue
        if not sol2:
            # you must follow the arrow
            # ASSUMPTION: assume you will never access a slope from the side of it
            if m[new_pos] in slope and di != slope.index(m[new_pos]):
                continue
        yield (di, new_pos)
    pass

def sol_bf(m, sol2):
    """
    brute force first
    disadvantage: there's a lot of list copy and addition, memory use intensive. And slow due to all possibility explored.
        10s for part 1
        part 2 > 10min

    cannot use due to data format change
    """
    (start, end) = find_start_end(m)
    q = collections.deque([ [start] ])
    max_length = 0
    while len(q):
        l_visited = q.popleft()
        #  print(l_visited)
        if l_visited[-1] == end:
            max_length = max(max_length, len(l_visited))
            continue
        for _, new_pos in walk(l_visited[-1], m, l_visited, sol2):
            q.append( l_visited + [new_pos] ) 

    #  excluding start
    return max_length -1 

def check_surrounding(pos, prevpos, m):
    """
    check possible direction to go
    if it's <=2, keep going forward
    """
    l_possible_sol1 = []
    l_possible_sol2 = []
    slope = [">", "v", "<", "^"]
    for di in range(4):
        new_pos = util.tuple_add(pos, util.direction_map[util.diDecode[di]])
        if prevpos == new_pos:
            continue
        if m[new_pos] == "#":
            continue
        if not m.inbound(new_pos):
            continue
        # you must follow the arrow
        # ASSUMPTION: assume you will never access a slope from the side of it
        l_possible_sol2.append(new_pos)
        if m[new_pos] in slope and di != slope.index(m[new_pos]):
            continue
        l_possible_sol1.append(new_pos)
    return l_possible_sol1, l_possible_sol2



def sol(m, sol2):
    """
    find the graph feature and then loop inside
    """
    (start, end) = find_start_end(m)
    q = [(start, (-1, -1))]

    #  here study every junction/start
    d_graph = {}
    while len(q):
        # DFS find all nodes, same as WFS
        startpos, prevpos = q.pop()
        if startpos in d_graph:
            continue
        d_graph[startpos] = []
        pos = startpos
        for pos in check_surrounding(pos, prevpos, m)[sol2]:
            # this is the actual possible step after the current pos
            prevpos = startpos
            step = 1

            while True:
                # in fact just check junction here.
                # this is l_possible_sol2, which is effectively any junction(considering direction going in)
                l_possible = check_surrounding(pos, prevpos, m)[1]
                if len(l_possible) != 1:
                    break

                prevpos = pos
                pos = l_possible[0]
                step += 1


            # outside, then pos is the junction/end
            d_graph[startpos].append((pos, step))

            # if you have already visited this junction
            if pos in d_graph:
                continue

            # this is a node, and consider it next
            # consider all possible direction(even back to this node itself due to symmetry in part 2, it might take slightly longer but code is simpler)
            if pos != end:
                q.append((pos, (-1, -1)))
    
    #  print(d_graph)
    q = [([start], 0)]
    max_s = 0
    while len(q):
        visited_nodes, step = q.pop()
        start = visited_nodes[-1]
        #  print(visited_nodes)
        if start == end:
            #  print(visited_nodes, step)
            max_s = max(max_s, step)
            continue

        for next, added_step in d_graph[start]:
            #  print("next", next)
            if next in visited_nodes:
                continue
            q.append((visited_nodes + [next], step+added_step))


    return max_s

def main():
    m = parse()
    #  print(m)
    #  print(sol_bf(m, False))
    #  print(sol_bf(m, True))
    print(sol(m, False))
    print(sol(m, True))

main()
