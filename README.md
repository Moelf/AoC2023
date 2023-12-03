[![Build Status](https://github.com/Moelf/AoC2023/workflows/CI/badge.svg)](https://github.com/Moelf/AoC2023/actions)

Advent of Code 2023: https://adventofcode.com/2023

## How to contribute
- upload input and solutions in the same PR. Name and clean up them properly
- when adding a new programming language, remember to update `runtests.jl` to "teach" it how to compile & run the `<lang>`

When testing locally, you can choose languages you want. For example, to avoid building C++ with bezel:
  to run - `julia runtests.jl python cpp`
```
> julia runtests.jl python cpp
Test Summary:                              | Pass  Total  Time
Day 00                                     |    4      4  0.3s
  python  00.py                00_test.txt |    2      2  0.0s
  cpp     00.cpp               00_test.txt |    2      2  0.3s
```

## Repo structure
```bash
AoC2023/
├── runtests.jl
├── inputs
│   ├── 00_test.txt
│   ├── 01_bauerc.txt
│   └── 01_moelf.txt
├── solutions
│   ├── 00_test.txt
│   ├── 01_bauerc.txt
│   └── 01_moelf.txt
└── src
    ├── cpp
    │   ├── 00.cpp
    │   └── 01.cpp
    └── julia
        ├── 00_test.jl
        └── 01_bauerc_moelf.jl
```

- the input files should be named as `<day>_<name>.txt`, the content should be the input of the day without any dangling empty lines at the end
- the solutions files should be named exactly as corresponding input file, the content should be exactly one or two lines (depending on if you solved both parts)
- the `src/<lang>/<day>_<optional name>.<ext>` should matched the double-digit day number convention. The `<lang>` should match what appears in [`runtests.jl`](https://github.com/Moelf/AoC2023/blob/main/runtests.jl#L18-L28)
