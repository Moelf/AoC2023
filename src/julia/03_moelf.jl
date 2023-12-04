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

function seek_and_accumulate(schematics; seeder, reducer)
    s = 0
    seen = Set{CartesianIndex{2}}()
    nums = Int[]
    for start in findall(seeder, schematics)
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
issymbol(c) = !isdigit(c) && c != '.'

# Part 2
p2_reducer(nums) = length(nums) == 2 ? prod(nums) : 0

function main(path)
    SCHEMATICS = stack(readlines(path); dims=1)
    println(seek_and_accumulate(SCHEMATICS; seeder = issymbol, reducer = sum))
    println(seek_and_accumulate(SCHEMATICS; seeder = ==('*'), reducer = p2_reducer))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
