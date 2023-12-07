#!/usr/bin/env python3
import sys
import re

class Almanac:
    def __init__(self, ):
        self._seeds = []
        self._seeds_sol2 = []
        self._cal = [] 
        # store the conversion ranges
        self._map = []
        self._config = 0
        pass

    def check_input(self, line):
        is_map = True
        if "-to-" in line:
            self._config += 1
            self._cal.append(lambda x : x)
            self._map.append([])
        else:
            is_map = False
            pass
        return is_map

    def take_map(self, line):
        des, src, r = [int(i) for i in line.split()]
        func_ori = self._cal[ self._config - 1 ]
        def func(x):
            if x >= src and x < src + r:
                return x - src + des
            else:
                return func_ori(x)
        self._cal[ self._config - 1 ] = func
        self._map[self._config - 1].append( (des, src, r) )
        pass

    def set_seeds(self, seed_strl):
        s = [int(i) for i in seed_strl]
        self._seeds      = s
        for i in range(len(s) // 2):
            self._seeds_sol2.append( (s[2 * i], s[2 * i] + s[2 * i + 1]) )
        pass

    def sol1(self,):
        l_loc = []
        for current in self._seeds:
            # current identifier(starting with seed)
            for i in range(self._config):
                # if exist, map, if not, don't need to do anything
                current = self._cal[i](current)
            l_loc.append(current)
        return min(l_loc)

    def sol2_bf(self,):
        l_loc = []
        for s1, s2 in self._seeds_sol2:
            for current in range(s1, s2):
                # current identifier(starting with seed)
                for i in range(self._config):
                    # if exist, map, if not, don't need to do anything
                    current = self._cal[i](current)
                l_loc.append(current)
        return min(l_loc)

    def sol2(self,):
        """
        back trace from location and find all possible seed 
        """
        l_current = self._seeds_sol2
        # sort our map first
        #  for i in range(self._config):
            #  self._map[i]  = sorted(self._map[i], key = lambda x : x[1])
            #  #  print(self._map[i])
            #  pass

        for map_ranges in self._map:
            l_mapped = []
            for des, src, r in map_ranges:
                #  print("new range", src, src+r, l_current)
                # go through each map and start segmenting
                l_next = []
                for rmin, rmax in l_current:
                    #  print(rmin, rmax, src, src+r, des)
                    if rmax < src or rmin >= src + r: 
                        l_next.append((rmin, rmax))
                    else: 
                        if rmin < src:
                            #  print("lower")
                            l_next.append((rmin, src))
                            rmin = src
                            pass
                        if rmax > src + r:
                            #  print("upper")
                            l_next.append((src+r, rmax))
                            rmax = src + r
                        if rmin < rmax:
                            l_mapped.append((des + rmin - src, des + rmax - src))
                        pass
                    #  print(l_next, l_mapped)
                    pass
                l_current = l_next
                pass
            # after one round of mapping, go to next level
            l_current += l_mapped
            #  print("out of maps")
            #  print(l_current)
            pass

        #  print(l_current)
        return min([i[0] for i in l_current])



def parse(infile):
    '''
    build the map
    '''
    al = Almanac()
    l_seeds = []

    for ln, line in enumerate(infile):
        line = line.strip()
        if len(line) == 0: continue
        if "seeds: " in line:
            # applys to first line
            al.set_seeds(line.split("seeds: ")[1].split())
            continue
        elif al.check_input(line):
            # applys to config
            continue
        else:
            al.take_map(line)
        pass
    return al

def sol():
    s1 = 0
    with open(sys.argv[1], 'r') as infile: 
        al = parse(infile)
        return al.sol1(), al.sol2()


s1, s2 = sol()
print(s1)
print(s2)
