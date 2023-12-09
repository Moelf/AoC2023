#!/usr/bin/env python3
import sys


def parse(infile):
    '''
    build the map
    '''
    l = [[int(i) for i in line.strip().split()] for line in infile]
    return l

def sol1(l):
    """
    it is in fact a sum of the last element of all lines, until all element in a line 0.
    if a line is all 0, it doesn't matter if you continue to derive the following line, it will also be all 0, and therefore the sum will be unchanged. 

    """
    s = 0
    for history in l:
        l_current = history
        while len(l_current):
            l_next = []
            s += l_current[-1]
            for i in range(len(l_current)-1):
                l_next.append(l_current[i+1] - l_current[i])
            l_current = l_next
    return s

def sol2(l):
    """
    a(i,0) = a(i,1) - a(i+1,0)
    line 0 calculate element 0, a00 = a01 - a10
        a10 = a11 - a20
        a00 = a01 - a11 + a20 
        ... just alternating between positive and negative.
        0 can still be ignored safely
    """
    s = 0
    for history in l:
        sign = 1
        l_current = history
        while len(l_current):
            l_next = []
            s += l_current[0] * sign
            for i in range(len(l_current)-1):
                l_next.append(l_current[i+1] - l_current[i])
            l_current = l_next
            sign *= -1
    return s
    pass

def main():
    with open(sys.argv[1], 'r') as infile: 
        l = parse(infile)
        #  print(l)
        print(sol1(l))
        print(sol2(l))
    pass

main()
