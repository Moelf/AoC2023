const INPUT_PATH = ARGS[1]
const ALL_LINES = readlines(INPUT_PATH)

issymbol(c) = !isdigit(c) && c != '.'

const SCHEMATICS = mapreduce(permutedims ∘ collect, vcat, ALL_LINES)::Matrix{Char}

const ADJACENTS = [CartesianIndex(x, y) for x = -1:1, y = -1:1]

function grow!(schematics, start, direction, pusher!; digits, seen)
    while true
        start += direction
        if !isassigned(schematics, start) || !isdigit(schematics[start])
            break
        end
        push!(seen, start)
        pusher!(digits, schematics[start])
    end
end


function grow_digits(schematics, start; seen)
    push!(seen, start)
    digits = [schematics[start]]
    grow!(schematics, start, CartesianIndex(0, -1), pushfirst!; digits, seen)
    grow!(schematics, start, CartesianIndex(0, 1), push!; digits, seen)
    return digits
end

function seek_and_accumulate(schematics, seeds; reducer)
    s = 0
    seen = Set{CartesianIndex{2}}()
    nums = Int[]
    for start in seeds
        for offset in ADJACENTS
            surround = start + offset
            # look around to find a digit to start growing
            if !isassigned(schematics, surround) ||
               !isdigit(schematics[surround]) ||
               surround ∈ seen
                continue
            end
            digits = grow_digits(schematics, surround; seen)
            push!(nums, parse(Int, join(digits)))
        end
        s += reducer(nums)
        empty!(nums)
    end
    return s
end

# Part 1
const SYMBOLS = findall(issymbol, SCHEMATICS)
p1 = seek_and_accumulate(SCHEMATICS, SYMBOLS; reducer = sum)
println(p1)

# Part 2
const GEARS = findall(==('*'), SCHEMATICS)
p2_reducer(nums) = length(nums) == 2 ? prod(nums) : 0
p2 = seek_and_accumulate(SCHEMATICS, GEARS; reducer = p2_reducer)
println(p2)
