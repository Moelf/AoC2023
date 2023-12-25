#!/usr/bin/env python3
import fileinput, math
import util
from collections import defaultdict, deque

def parse():
    #  m = util.matrix(default = 0)
    d = defaultdict(set)
    l_full = []
    for line in fileinput.input(encoding="utf-8"):
        key, l = line.strip().split(":")

        if key not in l_full:
            l_full.append(key)

        for val in l.split():
            if val not in l_full:
                l_full.append(val)
                pass
            d[l_full.index(key)].add(l_full.index(val))
            d[l_full.index(val)].add(l_full.index(key))
            #  d[(l_full.index(key), l_full.index(val))] = 1
            #  d[(l_full.index(val), l_full.index(key))] = 1
            pass
        pass
    return d, l_full

def sol1(m):
    n_node = len(m)
    # a dictionary of node - path to all other node
    d_node_all_other = defaultdict(lambda : defaultdict(list))


    def bfs(m, src, target):
        """
        return one of the shortest path
        """
        prev = {src : None}
        q = deque([ src ])
        while len(q):
            curr = q.popleft()
            if curr == target:
                break

            for next_node in m[curr]:
                if next_node in prev:
                    continue
                prev[next_node] = curr
                q.append(next_node)
                pass
            pass

        # utilizing the feature we discussed about :P
        if curr == target:
            # found the solution, rebuild path
            #  print("found", prev)
            path = []
            while curr != None:
                path.append(curr)
                curr = prev[curr]
            return path
        else:
            # all connected ones should have been visited at this point
            # TODO
            return list(prev.keys())


    for j in range(1, n_node):
        # from the target
        removed = []
        for _ in range(3):
            # compare with node 0
            path = bfs(m, 0, j)
            #  print(path)
            # remove this flow and find another flow
            for i in range(len(path)-1):
                m[path[i]].remove(path[i+1])
                m[path[i+1]].remove(path[i])
                removed.append((path[i], path[i+1]))
                pass
            pass

        # do you still find the flow or not?
        path = bfs(m, 0, j)
        if path[0] == j:
            # find the path. same component, go to next j
            # rebuild the path before going
            for src, goal in removed:
                m[src].add(goal)
                m[goal].add(src)
        else:
            return len(path) * (n_node - len(path))
    pass

def main():
    m, l_full = parse()
    #  print(m)
    #  for i, e in enumerate(l_full):
        #  print(i, e)

    print(sol1(m))

main()
