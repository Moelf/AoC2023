#!/usr/bin/env python3
import sys
import re
"""
"""

def parse(infile):
    # (line, start, stop, number)
    # stop is exlusive. 3 char long from 0, line 2 is (2, 0, 3)
    l_win = []
    l_own = []
    for ln, line in enumerate(infile):
        card_group = line.split(':')[1].strip().split('|')
        win = card_group[0].strip().split()
        own = card_group[1].strip().split()
        l_win.append(win)
        l_own.append(own)
        pass
    return l_win, l_own

def score_sol1(n):
    if n == 0:
        return 0
    else:
        return 2**(n-1)

def sol():
    s1 = 0
    s2 = 0
    n = [1] * 500 # safe anyway
    with open(sys.argv[1], 'r') as infile: 
        nCard = 0
        for iCard, (win, own) in enumerate(zip(*parse(infile))):
            nCard += 1
            nMatch = len(set(win) & set(own))
            s1 += score_sol1( nMatch )
            if n[iCard] == 0: continue
            for i in range(nMatch):
                n[iCard + i + 1] += n[iCard]
            pass
        pass

    return s1, sum(n[:nCard])


s1, s2 = sol()
print(s1)
print(s2)
