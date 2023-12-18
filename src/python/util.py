class matrix:
    def __init__(self, l):
        self._l = [[e for e in il] for il in l]

    def dim(self):
        return len(self._l), len(self._l[0])

    def __iter__(self):
        for x in self._l:
            yield x


    def __getitem__(self, tup):
        if type(tup) == type((0,0)):
            return self._l[tup[0]][tup[1]]
        else:
            return self._l[tup]

    def __setitem__(self, tup, val):
        self._l[tup[0]][tup[1]] = val

    def __str__(self):
        s = ""
        for l in self:
            for e in l:
                s += str(e)
            s += "\n"
        return s

def tuple_add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def tuple_mul(a, b):
    return (a[0]*b, a[1]*b)

diDecode = [
        "R", "D", "L", "U"
        ]

direction_map = {
        "r":(0,  1),
        "d":(1,  0),
        "l":(0, -1),
        "u":(-1, 0),

        "R":(0,  1),
        "D":(1,  0),
        "L":(0, -1),
        "U":(-1, 0),
    }


# day 10
def calculate_inside(l_loop, m):
    """
    l_loop is the matrix where 1 is boundary, 0 is anything else
    m is the whole matrix (list of list/str), but only boundary part will be accessed
    """
    ninside = 0
    for x, line in enumerate(l_loop):
        boundary_start = ""
        inside = False
        #  print(line)
        for y, boundary in enumerate(line):
            if boundary:
                t = m[x][y]
                #  print(t)
                if t == "|":
                    #  print("flip")
                    inside = not inside
                elif boundary_start == "":
                    #  print("start with ", t)
                    # this can't be '-'
                    boundary_start = t
                elif t != "-":
                    # skip over -
                    #  print("end in", t)
                    #  print(f"{boundary_start}{t}")
                    if f"{boundary_start}{t}" in ["FJ", "L7"]:
                        #  print("flip")
                        # flip only in those cases
                        inside = not inside
                    boundary_start = ""
            elif inside:
                #  print(x,y)
                ninside += 1

        pass
    return ninside
