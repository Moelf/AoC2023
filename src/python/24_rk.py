#!/usr/bin/env python3
import fileinput
import numpy as np
from collections import namedtuple

Hail =  namedtuple("HailPresentration", "p, v")
#  Vec  =  namedtuple("Vec", "x, y, z")



def parse():
    hails = []
    for line in fileinput.input(encoding="utf-8"):
        pos, vel = line.strip().split("@")
        p = np.array([int(i) for i in pos.split(",")])
        v = np.array([int(i) for i in vel.split(",")])
        hails.append(Hail(p, v))
    return hails

def solve_eq(h1, h2, i=0, j=1):
    """
    can be used to solve rock, too
    """
    C = h2.v[i] * h1.v[j] - h1.v[i] * h2.v[j]
    # parallel, never cross
    if C == 0:
        return -1, -1, -1, -1
    A = (h1.p[i] - h2.p[i]) / C
    B = (h1.p[j] - h2.p[j]) / C
    t1 = A * h2.v[j] - B * h2.v[i]
    t2 = A * h1.v[j] - B * h1.v[i]
    x = h1.p[i] + h1.v[i] * t1
    y = h1.p[j] + h1.v[j] * t1
    return t1, t2, x, y

def sol1(hails, MIN = 200000000000000, MAX = 400000000000000):
    s = 0
    nhails = len(hails)
    for i in range(nhails):
        for j in range(i+1, nhails):
            h1 = hails[i]
            h2 = hails[j]

            t1, t2, x, y = solve_eq(h1, h2)

            if t1 < 0 or t2 < 0:
                continue
            if x < MIN or x > MAX or y < MIN or y > MAX:
                continue
            s += 1
    return s

def is_integer_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False

def sol2(hails):
    nhails = len(hails)

    d_invalid = {0:set(), 1:set(), 2:set()}
    for i in range(nhails):
        for j in range(nhails):
            if i==j: continue
            h1 = hails[i]
            h2 = hails[j]
            for idx in range(3):
                if h1.p[idx] > h2.p[idx] and h1.v[idx] > h2.v[idx]:
                    for v in range(h2.v[idx], h1.v[idx] + 1):
                        d_invalid[idx].add(v)


    for vx in range(-500, 500):
        if vx in d_invalid[0]:continue
        for vy in range(-500, 500):
            if vy in d_invalid[1]:continue
            for vz in range(-500, 500):
                if vz in d_invalid[2]:continue
                vR = np.array([vx, vy, vz])
                #  print(vR)
                xR = None
                skip = False
                newhail = [Hail(h.p, h.v-vR) for h in hails[:3]]
                # screw it.. first 3 should work
                h1 = newhail[0]
                h2 = newhail[1]
                h3 = newhail[2]

                _, _, x12, y12 = solve_eq(h1, h2)
                _, _, x122, z12 = solve_eq(h1, h2, 0, 2)
                _, _, x13, y13 = solve_eq(h1, h3)
                _, _, x132, z13 = solve_eq(h1, h3, 0, 2)


                x12 = int(x12)
                x122 = int(x122)
                x13 = int(x13)
                x132 = int(x132)

                y12 = int(y12)
                y13 = int(y13)
                z12 = int(z12)
                z13 = int(z13)

                if x12 != x122 or x12 != x13 or x12 != x132 or y12 != y13 or z12 != z13:
                    continue


                else:
                    xR = np.array([x12, y12, z12])
                    return sum(xR)


    pass

def plot(hails, att = 0):
    from matplotlib import pyplot as plt
    l1 = sorted([(h.v[att], h.p[att])  for h in hails])
    #  [print(i) for i in l1]
    x = [p[0] for p in l1]
    y = [p[1] for p in l1]
    fig, ax = plt.subplots()
    plt.plot(x, y)
    fig.savefig(f"24_{att}.png")

def main():
    hails = parse()
    #  [print(i) for i in hails]
    nhails = len(hails)

    for i in range(3):
        plot(hails, i)


    print(sol1(hails))
    print(sol2(hails))


main()
