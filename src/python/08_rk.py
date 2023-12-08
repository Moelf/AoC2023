#!/usr/bin/env python3
import sys
import re
import math
import collections
"""
    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards' labels are distinct: 23456
    6 - 0 respectively.
    comparator uses    type * 15**5 + word(0-13) * 15**X ...


    In Clever, type is 3**(5-1) = 81, 
                       3**(4-1) + 3**(1-1) = 28,
                       3**(3-1) + 3**(2-1) = 12,
                       3**(3-1) + 3**(1-1) * 2 = 11, 
                       3**(2-1) * 2 + 3**(1-1) * 1 = 7, 
                       3**(2-1) * + 3**(1-1) * 3   = 6, 
                       3**(1-1) * 5 = 5
                       respectively.
    When J is there, it always joins the highest one, that is if you have 2, 1, you need to add two J, you will only make 4, 1, but not 3, 2
"""

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
    #  stores [loop size, [n steps for this Z ]]
    l_good_endings = []
    for start in l_start:
        current = start
        d_nstep_from_start = set([])
        l_step_ending_in_Z = []
        nseq = 0
        while current not in d_nstep_from_start:
            if current[-1] == "Z":
                l_step_ending_in_Z.append(nseq)
            d_nstep_from_start.insert(curent)
            current = dmap[current]
            # for the next
            nseq += 1
        l_good_endings.append(len(d_nstep_from_start), [ l_step_ending_in_Z])
        pass

    while True:
        break
        pass

    return 0

def main():
    with open(sys.argv[1], 'r') as infile: 
        seq, d = parse(infile)
        print(seq, d)
        print(sol1(seq, d))
        print(sol2(seq, d))
    pass

main()
