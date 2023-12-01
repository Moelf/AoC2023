[![Build Status](https://github.com/Moelf/AoC2023/workflows/CI/badge.svg)](https://github.com/Moelf/AoC2023/actions)

Advent of Code 2023: https://adventofcode.com/2023

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
- the `src/<lang>/<day>_<optional name>.<ext>` should matched the double-digit day number convention. The `<lang>` should match what appears in [`runtests.jl`](https://github.com/Moelf/AoC2023/blob/86fd788cfd96334194b1f9defb096824eaa7776f/runtests.jl#L16-L25)

## How to contribute
- upload input and solutions in the same PR. Name and clean up them properly
- when adding a new programming language, remember to update `runtests.jl` to "teach" it how to compile & run the `<lang>`
