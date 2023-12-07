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
    comparator uses    type * 14**5 + word(0-13) * 14**X ...
"""

d_map  = {**{str(i):i-1 for i in range(2, 10)}, **{"T": 9, "J":10, "Q": 11, "K": 12, "A": 13}}
d_map2 = {**{str(i):i-1 for i in range(2, 10)}, **{"T": 9, "J":0,  "Q": 11, "K": 12, "A": 13}}

def parse(infile):
    '''
    build the map
    '''
    l = []

    for ln, line in enumerate(infile):
        _ = line.split()
        l.append(( _[0].upper(), int(_[1]) ))
    return l

def key_hand(hand, bid, playJ = False):
    """
    key is called only once
    """
    s = collections.Counter(hand)
    most_card, n_mc = s.most_common(1)[0]

    offset = 0

    if not playJ or "J" not in s:
        if n_mc == 5:
            offset = 6
        elif n_mc == 4:
            offset = 5
        elif n_mc == 3:
            n_mc2 = s.most_common(2)[1][1]
            if n_mc2 == 2:
                offset = 4
            else:
                offset = 3
            pass
        elif n_mc == 2:
            n_mc2 = s.most_common(2)[1][1]
            if n_mc2 == 2:
                offset = 2
            else:
                offset = 1
            pass
    else:
        # 5J
        if n_mc == 5:
            offset = 6
        # 4J + X or 4X+J = 5X
        elif n_mc == 4:
            offset = 6
        elif n_mc == 3:
            # 3J + 2X or 2J+3X
            if s.most_common(2)[1][1] == 2:
                offset = 6
            # 3J + X + Y = 4X+Y 
            # 3X + J + Y = 4X+Y
            else:
                offset = 5
        #  2X+???
        elif n_mc == 2:
            hand_2, n_mc2 = s.most_common(2)[1]
            if  n_mc2 == 2:
                # 2J+2X+Y = 4X+Y
                if hand_2 == "J" or most_card == "J":
                    offset = 5
                # 2X+2Y+J = 3X+2Y
                else:
                    offset = 4
            #  2J+X+Y+Z = 3X+Y+Z
            #  2X+J+Y+Z = 3X+Y+Z
            else:
                offset = 3
        #  J+X+Y+Z+M = 2X+Y+Z+M
        else:
            offset = 1

    score = offset * 15**5
    for i in range(5):
        if playJ :
            score += d_map2[hand[i]] * 15**(4-i)
        else:
            score += d_map[hand[i]] * 15**(4-i)
    return score

def sol2(l):
    # rank will be the index + 1
    l_s = sorted(l, key = lambda x : key_hand(x[0], x[1], True))
    s = 0
    for i, (_, bid) in enumerate(l_s):
        #  print(i+1, _, bid)
        s += (i+1) * bid
    return s

def sol1(l):
    # rank will be the index + 1
    l_s = sorted(l, key = lambda x : key_hand(x[0], x[1]))
    s = 0
    for i, (_, bid) in enumerate(l_s):
        #  print(i+1, _, bid)
        s += (i+1) * bid
    return s

def main():
    with open(sys.argv[1], 'r') as infile: 
        l = parse(infile)
        print(sol1(l))
        print(sol2(l))
    pass

main()
