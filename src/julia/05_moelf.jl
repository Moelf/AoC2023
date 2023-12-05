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

"""
    apply_map(seeds::Vector{UnitRange}, M::Vector{Pair{UnitRange}})

1. `pop!()` one seed range out
2. loop over all src/dst ranges
3. if there's intersection, map the intersection and put the result into `results`
4. for the left-over in seed range, put everything before intersection into the `seeds` for the next iteration
5. if there's no intersection at all, directly put into results

"""
function apply_map(seeds, M)
    results = UnitRange{Int64}[]
    while !isempty(seeds)
        seed_range = pop!(seeds)
        any = false
        for (src_range, dst_range) in M
            int = intersect(seed_range, src_range)
            if !isempty(int)
                any=true
                S, L = int[begin], length(int)
                i = findfirst(==(S), src_range)
                push!(results, dst_range[i:i+L-1])
                if S > seed_range[begin]
                    j = findfirst(==(S), seed_range)
                    push!(seeds, seed_range[begin:j-1])
                end
            end
        end
        if !any
            push!(results, seed_range)
        end
    end
    return results
end

function through_all_maps(seed, seed_maps)
    seeds = [seed]
    for M in seed_maps
        seeds = apply_map(seeds, M)
    end
    return mapreduce(minimum, min, seeds)
end

function main(path)
    seed_str, rest_str... = split(read(path, String), "\n\n")
    seed_nums = parse.(Int, split(seed_str)[2:end])
    seed_ranges = [s:s for s in seed_nums]
    seed_maps = seed_map.(rest_str)
    F = Base.Fix2(through_all_maps, seed_maps)
    println(minimum(F, seed_ranges))

    seed_groups = Iterators.partition(seed_nums, 2)
    seed_ranges2 = map(seed_groups) do (start, length)
        range(; start, length)
    end
    println(minimum(F, seed_ranges2))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
