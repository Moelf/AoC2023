#!/usr/bin/env python3
import sys

"""
repair broken spring record
""" 

def parse(infile):
    '''
    build the map
    '''
    fullMap = []
    fullMapFolded = []
    for row in infile:
        #  print(row)
        #  print(row.split()[0].split("."))
        spring_expo = [i for i in row.split()[0].split(".") if i != '']
        group_set = [int(i) for i in row.split()[1].split(",")]
        fullMap.append((spring_expo, group_set))

        
        
        new_str1 = "?".join([row.split()[0]] * 5)
        #  print(row.split()[0], new_str1)
        sp_fold = [i for i in new_str1.split(".") if i != '']
        gs_fold = group_set * 5
        fullMapFolded.append((sp_fold, gs_fold))
        pass
    return fullMap, fullMapFolded


def solve_row(sp, gs, cache = {}, index = 0):
    """
    index count from backward for the very original sp
    """

    # starting from the last
    # let's do recursive
    igroup = len(gs) - 1

    while len(sp) and igroup >= 0:
        # there's only one solution here
        group = sp[-1]
        if group == "":
            sp.pop()
            continue
        s = gs[igroup]

        #  print( (index, igroup, group[-1]), sp, gs )
        if (index, igroup, group[-1]) in cache:
            #  print( "found cache", cache[(index, igroup, group[-1])] )
            return cache[(index, igroup, group[-1])]

        if len(group) < s:
            if group.find("#") != -1:
                #  if any #, break!
                cache[(index, igroup, group[-1])] = 0
                return 0
            else:
                index += len(sp.pop())
                continue

        if group[-1] == "#":
            # the only solution is a continuous "s" number of "#"
            # wipe out those, and continue considering
            result = group[:-s]
            if result != "" and result[-1] == "#" :
                # this is not a valid solution
                cache[(index, igroup, "#")] = 0
                return 0

            # valid one, move forward
            sp[-1] = result[:-1]
            if result == "":
                index += s
            else:
                index += s+1
            igroup -= 1
        else:
            # this is a ?

            # consider if it's a #
            nsol = solve_row([i for i in sp[:-1]] + [group[:-1] + "#"], gs[:igroup+1], cache, index)
            cache[(index, igroup, "#")] = nsol
            # consider if it's a .
            res = solve_row([i for i in sp[:-1]] + [group[:-1]      ], gs[:igroup+1], cache, index+1)
            #  print(res, nsol, index, igroup, sp, s)
            nsol += res
            #  print("added cache", nsol)
            cache[(index, igroup, "?")] = nsol
            return nsol
        pass

    if igroup >= 0:
        # len(sp) is already 0
        #  print("no solution", sp, igroup)
        return 0
    elif len(sp) > 0:
        # igroup is -1, the only solution is when everything left are "?"
        if "".join(sp).find("#") == -1:
            return 1
        else:
            return 0
        pass
    else:
        #  print("ILLEGAL")
        return -99999
    pass

def sol1(m):
    nsol = 0
    for i, (sp, gs) in enumerate(m):
        # DP
        result = solve_row(sp, gs, {})
        nsol += result
        #  print(sp, gs, "sol",i," = ", result)
            
        pass
    return nsol

# sol1 is not clean, maybe? pop and duplicate probably requires a lot of mem/cpu..
def solve_row2(sp, gs):
    #  print(sp, gs)
    if len(gs) == 0:
        if "".join(sp).find("#") == -1:
            #  print("inspect, no group left and all ?")
            return 1
        else:
            #  print("inspect, no group left and # left")
            return 0
    elif len(sp) == 0:
        #  print("empty group, no solution")
        return 0
    elif len("".join(sp)) < sum(gs):
        return 0
    else:
        # at least one in each
        group = sp[0]
        req_size = gs[0]
        if len(group) < req_size:
            # the group has a # but doesn't match the size
            if group.find("#") != -1:
                return 0
            # the group can't satisfy the requirement, move on
            return solve_row2(sp[1:], gs)
        else:
            s = 0
            modified_first = group[req_size:]
            #  print("mod", modified_first)
            if modified_first == "":
                s += solve_row2(sp[1:], gs[1:])
                #  print(sp, "empty", gs, s)
            elif modified_first[0] == "?":
                # consider when the first is a "#", but not followed by an "#"
                s += solve_row2([modified_first[1:]] + sp[1:], gs[1:])
                #  print(sp, gs, "#", s)
            elif modified_first[0] == "#":
                #  print("discard")
                s = 0
            else:
                #  print("ILLEGAL", modified_first)
                pass

            if group[0] == "?":
                # add when the first is a "."
                res = 0
                res = solve_row2([group[1:]] + sp[1:], gs)
                #  print(sp, gs, '.', res, "#", s)
                s += res
            return s
            pass
        pass
    pass

"""
no plan to do DP
"""
def sol2(m):
    nsol = 0
    for i, (sp, gs) in enumerate(m):
        result = solve_row2(sp, gs) 
        nsol += result
        print(sp, gs, "sol",i," = ", result)
        pass
    return nsol

def sol3(s, gps, cache, index = 0, group = 0):
    output = 0
    if (index, group) in cache:
        return cache[(index, group)]
    if len(gps) == 0:
        if s.find("#") == -1:
            output = 1
    elif len(s) >= sum(gps):
        if s[0] == ".":
            return sol3(s[1:], gps, cache, index+1, group)

        if s[0] == "?":
            output += sol3(s[1:], gps, cache, index+1, group)
            pass
        # consider case when the first char is "#"
        nword = gps[0]
        if sum(1 for i in range(nword) if s[i] != ".") == nword:
            if nword >= len(s) or s[nword] != "#":
                output += sol3(s[nword+1:], gps[1:], cache, index+1, group+1)
        pass
    cache[(index, group)] = output
    return output
    pass

def main():
    with open(sys.argv[1], 'r') as infile: 
        s1, s2 = 0, 0
        for iline, row in enumerate(infile):
            spring_expo = row.split()[0]
            group_set = [int(i) for i in row.split()[1].split(",")]
            # DP
            s1 += sol3(spring_expo, group_set, dict(), 0, 0)
            s2 += sol3("?".join([spring_expo]*5), group_set * 5, {})
            pass
        print(s1)
        print(s2)

    # also work but nastily
    #  with open(sys.argv[1], 'r') as infile: 
        #  m, mfolded = parse(infile)
        #  sol = sol1(m)
        #  print(sol)
        #  sol = sol1(mfolded)
        #  print(sol)
    #  pass

main()
