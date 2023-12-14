#!/usr/bin/env python3
import sys
import copy

def parse():
    row_block = []
    with open(sys.argv[1], 'r') as infile:
        for line in infile:
            line = line.strip()
            if line == "":
                break
            row_block.append([c for c in line])
            pass

    width = len(row_block[0])
    column_block = []
    for i in range(width):
        st = ""
        for j in range(len(row_block)):
            st += row_block[j][i]
        column_block.append(st)
        pass
    return row_block, column_block

def roll_column_north(c):
    """
    part 1
    just go over each column, find the O and calculate its corresponding resultant row after rolling to the north
    """
    s = 0
    l = len(c)
    i_after_roll = 0
    for i in range(len(c)):
        if c[i] == "O":
            s += l - i_after_roll
            i_after_roll += 1
        elif c[i] == "#":
            i_after_roll = i + 1
        pass
    return s

def print_map(l_row):
    for r in l_row:
        print("".join(r))
    print()

def roll_one_section(l_row, di, fall_to_row, fall_to_col, nO, irow, icol):
    """
    irow and icol don't need to be considered(# or out of bound)
    """
    count = 0
    if di[0] == 0:
        for i in range(fall_to_col, icol, di[1]):
            if count < nO:
                l_row[irow][i] = "O"
            else:
                l_row[irow][i] = "."
            count += 1
    else:
        for i in range(fall_to_row, irow, di[0]):
            if count < nO:
                l_row[i][icol] = "O"
            else:
                l_row[i][icol] = "."
            count += 1
    return l_row

def roll_side(l_row, di):
    """
    part 2
    di is the direction variable indicating where the increment should go
        slide to north, meaning we should inspect from line 0 to line N
    """
    nrow = len(l_row)
    ncol = len(l_row[0])
    # initialize to the correct starting point
    irow = 0 if di[0] >= 0 else nrow-1
    icol = 0 if di[1] >= 0 else ncol-1
    nO = 0
    fall_to_row = 0 if di[0] >= 0 else nrow-1
    fall_to_col = 0 if di[1] >= 0 else ncol-1

    while True:
        # slide along column
        if di[0] != 0 and (irow == nrow or irow == -1):
            l_row = roll_one_section(l_row, di, fall_to_row, fall_to_col, nO, irow, icol)
            nO = 0
            icol += 1
            if icol == ncol: break
            fall_to_col += 1
            irow = 0 if di[0] >= 0 else nrow-1
            fall_to_row = 0 if di[0] >= 0 else nrow-1
            pass
        elif di[1] != 0 and (icol == ncol or icol == -1):
            l_row = roll_one_section(l_row, di, fall_to_row, fall_to_col, nO, irow, icol)
            nO = 0
            irow += 1
            if irow == nrow: break
            fall_to_row += 1
            icol = 0 if di[1] >= 0 else ncol-1
            fall_to_col = 0 if di[1] >= 0 else ncol-1
            pass

        if l_row[irow][icol] == "O": 
            nO += 1
        elif l_row[irow][icol] == "#":
            l_row = roll_one_section(l_row, di, fall_to_row, fall_to_col, nO, irow, icol)
            nO = 0
            fall_to_row = irow + di[0]
            fall_to_col = icol + di[1]
            pass

        irow += di[0]
        icol += di[1]
        pass
    return l_row

def calculate(l_row):
    """
    for part 2 calculate score
    """
    s = 0
    nrow = len(l_row)
    ncol = len(l_row[0])
    for i in range(nrow):
        for j in range(ncol):
            if l_row[i][j] == "O":
                s += nrow - i
    return s



def main():
    s, s2 = 0, 0
    l_row, l_col = parse()
    #  print("original")
    #  print_map(l_row)
    #  print(l_col)
    for c in l_col:
        res = roll_column_north(c)
        s += res

    # assume there's a loop
    unique_sol = []
    row_record = []
    loop_found_i = 0
    start_loop = 0
    N = 1000000000
    for i in range(N):
        #  l_ori = [[c for c in r] for r in l_row]
        #  print("Before")
        #  print_map(l_row)
        l_row = roll_side(l_row, (1, 0))
        #  print("North")
        #  print_map(l_row)
        l_row = roll_side(l_row, (0, 1))
        l_row = roll_side(l_row, (-1, 0))
        l_row = roll_side(l_row, (0, -1))

        #  print("after", i+1, "cycle")
        cmp_str = "".join(["".join(r) for r in l_row])
        #  print(cmp_str)
        #  print(calculate(l_row))
        #  print_map(l_row)
        if cmp_str in unique_sol:
            # period, and break?
            loop_found_i = i
            start_loop = unique_sol.index(cmp_str)
            break
        unique_sol.append(cmp_str)
        row_record.append(copy.deepcopy(l_row))
        pass

    size_loop = loop_found_i - start_loop 

    #  print(start_loop, size_loop)
    #  for i in row_record:
        #  print_map(i)
        #  print(calculate(i))

    #  for i in unique_sol:
        #  print(i)
    
    #  print((N - start_loop) % size_loop)
    l_row = row_record[start_loop + (N - 1 - start_loop) % size_loop]

    #  print("solution")
    #  print_map(l_row)
    s2 = calculate(l_row)

    print(s)
    print(s2)
    pass

main()

