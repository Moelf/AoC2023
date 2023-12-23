class matrix:
    """
    a list of M lists with size N of the same type of element, default to be int(0)
    [[],
     [],
     ...
     []]
    """
    def __init__(self, l = [], default = 0):
        self._l = [[e for e in il] for il in l]
        self.dim()
        self._default = default

    def dim(self):
        self._nr = len(self._l)
        if len(self._l):
            self._nc = len(self._l[0])
        else:
            self._nc = 0
        return self._nr, self._nc

    def __iter__(self):
        for x in self._l:
            yield x

    def inbound(self, p):
        return p[0] >= 0 and p[0] < self._nr and p[1] >= 0 and p[1] < self._nc


    def __getitem__(self, tup):
        # do not do inbound check
        if type(tup) == type((0,0)):
            return self._l[tup[0] % self._nr][tup[1] % self._nc]
        else:
            return self._l[tup]

    def __setitem__(self, tup, val):
        if type(tup) == type((0,0)):
            if tup[0] >= self._nr:
                for i in range(self._nr, tup[0]+1):
                    self._l.append([])
            self.dim()
            if tup[1] >= self._nc:
                for r in range(0, self._nr):
                    for c in range(self._nc, tup[1]+1):
                        self._l[r].append(self._default)

            self._l[tup[0]][tup[1]] = val
            self.dim()
        else:
            if tup >= self._nr:
                for i in range(self._nr, tup+1):
                    self._l.append([])
            self._l[tup] = val
            self.dim()

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
