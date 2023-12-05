function seed_map(map_str)
    range_strs = split(map_str, "\n"; keepempty = false)[2:end]
    return nums_to_range_pair.(range_strs)
end

function nums_to_range_pair(str)
    dst, src, len = parse.(Int, split(str))
    return nums_to_range_pair(dst, src, len)
end

nums_to_range_pair(dst, src, length) =
    range(; start = src, length) => range(; start = dst, length)

function apply_map(seed, M)
    # @show seed
    for (src, dst) in M
        i = findfirst(==(seed), src)
        if !isnothing(i)
            return dst[i]
        end
    end
    return seed
end

function through_all_maps(seed, seed_maps)
    for M in seed_maps
        seed = apply_map(seed, M)
    end
    return seed
end

const F = Base.Fix2(through_all_maps, seed_maps)
function main(path)
    seed_str, rest_str... = split(read(path, String), "\n\n")
    seed_nums = parse.(Int, split(seed_str)[2:end])
    seed_maps = seed_map.(rest_str)
    println(minimum(F, seed_nums))

    seed_groups = Iterators.partition(seed_nums, 2)
    seed_ranges = map(seed_groups) do (start, length)
        range(; start, length)
    end
    M = typemax(Int)
    for rg in seed_ranges
        temp = minimum(F, rg)
        M = min(M, temp)
    end
    println(M)
end


(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
