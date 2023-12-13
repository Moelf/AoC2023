#!/usr/bin/env python3

import sys

def parse():
    l_whole_block = []
    with open(sys.argv[1], 'r') as infile:
        lines = infile.readlines()
        ln = 0
        while ln < len(lines):
            row_block = []
            for line in lines[ln:]:
                line = line.strip()
                ln += 1
                if line == "":
                    break
                row_block.append(line)
                pass

            width = len(row_block[0])
            column_block = []
            for i in range(width):
                st = ""
                for j in range(len(row_block)):
                    st += row_block[j][i]
                column_block.append(st)
                pass

            l_whole_block.append((row_block, column_block))
            pass
        pass
    return l_whole_block
    pass

def find_mirror(grp, smudge = False):
    """
    part 1
    """
    for mirror_pos in range(len(grp) - 1):
        # the position of mirror will be between mirror_pos and mirror_pos + 1
        #  mirror_pos - shift should be [0, mirror_pos], 
        #    shift from [0, mirror_pos]
        #  mirror_pos + shift + 1 should be [mirror_pos + 1, len(grp) - 1]
        #    shift from [0, len(grp) - 2 - mirror_pos]
        ndiff = 0
        for shift in range(min(mirror_pos+1, len(grp) - 1 - mirror_pos)):
            if not smudge:
                if grp[mirror_pos - shift] != grp[mirror_pos + shift + 1]:
                    ndiff = 2
                    break
                pass
            else:
                for i in range(len(grp[mirror_pos - shift])):
                    if grp[mirror_pos - shift][i] != grp[mirror_pos + shift + 1][i]:
                        ndiff += 1
                        if ndiff >= 2:
                            break
                        pass
                    pass
                #  print(mirror_pos, grp[mirror_pos - shift], grp[mirror_pos + shift + 1], ndiff)
                if ndiff >= 2:
                    break
                pass

        if (not smudge and ndiff == 0) or (smudge and ndiff == 1):
            return mirror_pos + 1
    return 0



def main():
    l = parse()
    s, s2 = 0, 0
    for row, col in l:
        r = find_mirror(row)
        c = find_mirror(col)
        s += 100 * r + c
        #  print("row")
        r = find_mirror(row, True)
        #  print("col")
        c = find_mirror(col, True)
        #  print(r, c, "\n")
        s2 += 100 * r + c
    print(s)
    print(s2)

main()
