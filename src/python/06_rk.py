#!/usr/bin/env python3
import sys
import re
import math


def parse(infile):
    '''
    build the map
    '''
    l_times = []
    l_dists = []

    for ln, line in enumerate(infile):
        if "Time:" in line:
            l_times = [int(i) for i in line.split(":")[1].split()]
        elif "Dist" in line:
            l_dists = [int(i) for i in line.split(":")[1].split()]
    return l_times, l_dists

def sub_sol(t, d):
    delta = (t**2/4-d-1) ** 0.5 
    #  print(t/2 + delta, t/2 - delta)
    sol2 = max(math.floor(t/2 + delta), 0)
    sol1 = min(math.ceil(t/2 - delta), t)
    #  print(sol1, sol2, sol2 - sol1 + 1)
    num = sol2 - sol1 + 1
    return max(num, 1)

def sol():
    with open(sys.argv[1], 'r') as infile: 
        l_times, l_dists = parse(infile)
        #  print(l_times)
        #  print(l_dists)
        mul = 1
        # n for charing, to speed n
        # time - n for running, distance d = n * (time - n)
        # solving -n**2 + tn - (d + 1) = 0
        # - (x - t/2) ** 2 = d + 1 - t**2/4
        st_t = ""
        st_d = ""
        for t, d in zip(l_times, l_dists):
            st_t += str(t)
            st_d += str(d)
            mul *= sub_sol(t, d)

        return mul, sub_sol(int(st_t), int(st_d))
    pass

s1, s2 = sol()
print(s1)
print(s2)
