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


def conversion(c, d_graph, pos):
    if c == "#":
        return 0
    elif pos in d_graph:
        return 2
    else:
        return 1

def plot(d_graph, m, sol2, solution):
    from matplotlib import pyplot as plt
    import numpy as np

    num_m = [[conversion(c, d_graph, (irow, icol)) for icol, c in enumerate(row)] for irow, row in enumerate(m)]
    #  print(num_m)

    map = np.array(num_m)
    #  print(map)

    fig, ax = plt.subplots()
    im = ax.imshow(map)

    #  ax.set_xticks(np.arange(len(farmers)), labels=farmers)
    #  ax.set_yticks(np.arange(len(vegetables)), labels=vegetables)

    fig.savefig("23_full_trace.png")

    import networkx as nx
    G = None
    G = nx.DiGraph()



    for i in range(len(solution)-1):
        start = solution[i]
        end = solution[i+1]
        for end2, step in d_graph[start]:
            if end != end2: continue

            G.add_edge(f"{(start[0], start[1])}", f"{(end[0], end[1])}", weight = 1, length = step, color = "tab:red")
            break
        pass

    esolution = [(u, v) for (u, v, d) in G.edges(data=True) if d["color"] == "tab:red"]

    for start, l in d_graph.items():
        for end, step in l:
            if (end, start) in esolution or (start, end) in esolution:
                continue
            G.add_edge(f"{(start[0], start[1])}", f"{(end[0], end[1])}", weight = 1, length = step, color = "k")


    eother    = [(u, v) for (u, v, d) in G.edges(data=True) if d["color"] != "tab:red"]


    options = {
		#  'node_color': 'black',
		'node_size': 1000,
		'font_size': 7,
        'width': 6,
        #  'horizontalalignment' : 'left',
        #  'verticalalignment' : '',
        }

    #  fig, ax = plt.subplots(figsize=(30, 30))
    fig, ax = plt.subplots(figsize=(30, 30))
    pos = nx.spectral_layout(G)
    #  pos = nx.spring_layout(G)
    #  pos = nx.spring_layout(G, seed = 0)
    nx.draw_networkx_nodes(G, pos = pos, node_size = options['node_size'])
    nx.draw_networkx_labels(G, pos = pos, font_size = options['font_size'])
    #  colors = nx.get_edge_attributes(G,'color')
    #  [print(i) for i in colors.values()]
    #  nx.draw_networkx_edges(G, pos, edge_color = colors)
    if sol2:
        nx.draw_networkx_edges(G, pos, edgelist=eother,    edge_color = "k", arrows = True, width = 6, arrowsize = 15, arrowstyle = "-")
    else:
        nx.draw_networkx_edges(G, pos, edgelist=eother,    edge_color = "k", arrows = True, width = 6, arrowsize = 15)
    nx.draw_networkx_edges(G, pos, edgelist=esolution, edge_color = "tab:red", arrows = True, width = 6, arrowsize = 15)
    labels = nx.get_edge_attributes(G,'length')
    nx.draw_networkx_edge_labels(G, pos = pos, edge_labels=labels, font_size=options["font_size"])
    plt.savefig(f"23_graph_part{int(sol2) + 1}.png", dpi = 400)

    pass

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
    solution = None
    max_s = 0
    while len(q):
        visited_nodes, step = q.pop()
        start = visited_nodes[-1]
        #  print(visited_nodes)
        if start == end:
            #  print(visited_nodes, step)
            max_s = max(max_s, step)
            if max_s == step:
                solution = visited_nodes
            continue

        for next, added_step in d_graph[start]:
            #  print("next", next)
            if next in visited_nodes:
                continue
            q.append((visited_nodes + [next], step+added_step))

    if len(sys.argv) > 2:
        plot(d_graph, m, sol2, solution)

    return max_s

def main():
    m = parse()
    #  print(m)
    #  print(sol_bf(m, False))
    #  print(sol_bf(m, True))
    print(sol(m, False))
    print(sol(m, True))

main()
