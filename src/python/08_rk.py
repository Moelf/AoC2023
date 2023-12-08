#!/usr/bin/env python3
import sys
import re
from functools import reduce

def parse(infile):
    '''
    build the map
    '''
    d = {}
    l = [line.strip() for line in infile]
    label = "LR"
    seq = [label.index(i) for i in l[0]]

    for line in l[2:]:
        start = line.split("=")[0].strip()
        L, R = line.split("=")[1].split(",")
        L = L.split("(")[1].strip()
        R = R.split(")")[0].strip()
        d[start] = (L, R)
    return seq, d

def sol1(seq, d):
    if "AAA" not in d: 
        return 0

    current = "AAA"
    nseq = 0
    # assumes there is solution(no looop, always has ending at ZZZ)
    while current != "ZZZ":
        nseq += 1
        for step in seq:
            current = d[current][step]
            pass
        pass
    return nseq * len(seq)

def sol2(seq, d):
    l_start = []
    #  1-1 mapping of start and stop before and after a sequence
    dmap = {}
    for start in d:
        if start[-1] == "A": 
            l_start.append(start)
        current = start
        # it's a closed graph, loop
        while current not in dmap:
            start_seq = current
            for step in seq:
                current = d[current][step]
            dmap[start_seq] = current
            pass


    # I can blend this in the previous loop, but for cleanness, I prefer not to
    # find the loop for each start
    #  stores [loop size, set(n steps for this Z )]
    l_good_endings = []
    for start in l_start:
        current = start
        d_nstep_from_start = []
        l_step_ending_in_Z = []
        nseq = 0
        while current not in d_nstep_from_start:
            if current[-1] == "Z":
                l_step_ending_in_Z.append(nseq)
            d_nstep_from_start.append(current)
            current = dmap[current]
            # for the next
            nseq += 1
        #  print("last", current, d_nstep_from_start)
        # size of the loop first
        l_good_endings.append([len(d_nstep_from_start) - d_nstep_from_start.index(current), set(l_step_ending_in_Z)])
        pass

    l_sets = [set(i[1]) for i in l_good_endings]
    #  print("MAP", dmap)
    #  print(l_good_endings)
    #  print("START", len(seq))
    # hacky answer due to the nature of the problem set:
    return reduce(lambda x, y : x * y, [i[0] for i in l_good_endings]) * len(seq)

    inters = set()
    it = 0
    while len(inters) == 0:
        it += 1
        inters = reduce(lambda x, y : x & y, l_sets)
        for i, (num, s) in enumerate(l_good_endings):
            #  print([i + num for i in s])
            l_sets[i] |= set([i + it * num for i in s])
        #  print(l_sets)
        pass

    # assumed there is a solution
    #  print(inters, seq, len(seq))
    nseq = min(inters)

    return nseq * len(seq)

def main():
    with open(sys.argv[1], 'r') as infile: 
        seq, d = parse(infile)
        #  print(seq, d)
        print(sol1(seq, d))
        print(sol2(seq, d))
    pass

main()
