#!/usr/bin/env python3
import sys

def parse(instr):
    l = [] # contains list of tuples of RGB
    with open(instr, 'r') as infile:
        for line in infile:
            # each line is a game
            game_output = []
            for rnd in line.strip().split(':')[1].split(';'):
                round_output = []
                for match_color in ["red", "green", "blue"]:
                    num = 0
                    if rnd.find(match_color) != -1:
                        num = int(rnd.split(match_color)[0].split(',')[-1])
                        pass
                    round_output.append(num)
                game_output.append(round_output)
                pass
            l.append(game_output)
            pass
        pass
    return l
    pass

def sol(r, g, b):
    s1 = 0
    s2 = 0
    for i, game in enumerate(parse(sys.argv[1])):
        game_poss = True
        rm = -1
        gm = -1
        bm = -1
        for rnd in game:
            if rnd[0] > r or rnd[1] > g or rnd[2] > b:
                game_poss = False
                pass
            rm = max(rnd[0], rm)
            gm = max(rnd[1], gm)
            bm = max(rnd[2], bm)
            pass
        s2 += rm*gm*bm
        if game_poss:
            s1 += i + 1
    return s1, s2
    pass

s1, s2 = sol(12, 13, 14)
print(s1)
print(s2)
