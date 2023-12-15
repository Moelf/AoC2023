#!/usr/bin/env python3
import sys

def parse():
    d1, d = [], []
    with open(sys.argv[1], 'r') as infile:
        line = infile.readlines()[0].strip()
        d1 = line.split(",")
    return d1

def alg1(w):
    s = 0
    for c in w:
        s += ord(c)
        s *= 17
        s %= 256
        pass
    #  print(w, s)
    return s

def sol2(d):
    l_label = [[] for i in range(256)]
    l_focal = [[] for i in range(256)]
    for word in d:
        if "=" in word:
            label, focal_length = word.split("=")
            box = alg1(label)
            if label in l_label[box]:
                # replace
                idx = l_label[box].index(label)
                l_focal[box][idx] = focal_length
            else:
                l_label[box].append(label)
                l_focal[box].append(focal_length)
            #  print(word, box, l_focal[box], l_label[box])
        elif "-" in word:
            label = word.split("-")[0]
            box = alg1(label)
            if label in l_label[box]:
                idx = l_label[box].index(label)
                l_label[box].pop(idx)
                l_focal[box].pop(idx)
            #  print(word, box, l_focal[box], l_label[box])
            pass
        else:
            print("ILLEGAL")
            pass

    s = 0
    for i in range(256):
        for j in range(len(l_focal[i])):
            s += (i+1) * (j+1) * int(l_focal[i][j])
    return s

def main():
    s1, s2 = 0, 0
    d1 = parse()
    for w in d1:
        s1 += alg1(w)
    s2 = sol2(d1)

    print(s1)
    print(s2)
    pass

main()
