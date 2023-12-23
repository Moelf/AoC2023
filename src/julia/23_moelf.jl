const CI = CartesianIndex{2}
const L, R, U, D = CI(0, -1), CI(0, 1), CI(-1, 0), CI(1, 0)
const DIRS = (L, R, U, D)
const SLOPE = Dict('>' => R, '<' => L, '^' => U, 'v' => D)

function neighbors(map, start; p1=true)
    tile = map[start]
    res = if p1 && haskey(SLOPE, tile)
        (start + SLOPE[tile],)
    else
        DIRS .+ start
    end
    filter(x -> isassigned(map, x) && map[x] != '#', res)
end

function dfs(map, start, target, visited)
    if start == target || !isassigned(map, start)
        return 0
    end
    tile = map[start]
    tile == '#' && return -1

    nexts = neighbors(map, start)

    vis = push!(copy(visited), start)
    lens = Int[]
    for np in nexts
        np ∈ vis && continue
        len = dfs(map, np, target, vis)
        if len >= 0
            push!(lens, len + 1)
        end
    end

    isempty(lens) ? -1 : maximum(lens)
end

function make_edges(MAP)
    # double linked list
    # from_node -> (to_node -> distance)
    edges = Dict{CI,Dict{CI,Int}}()
    for pos in CartesianIndices(MAP)
        v = MAP[pos]
        v == '#' && continue
        for np in neighbors(MAP, pos)
            get!(edges, pos, Dict())[np] = 1
            get!(edges, np, Dict())[pos] = 1
        end
    end

    @label notdone
    n = findfirst(e -> length(e) == 2, edges)
    if !isnothing(n)
        (pos1, l1), (pos2, l2) = edges[n]
        delete!(edges[pos1], n)
        delete!(edges[pos2], n)
        new_len = l1 + l2
        edges[pos1][pos2] = new_len
        edges[pos2][pos1] = new_len
        delete!(edges, n)
        @goto notdone
    end
    edges
end

function longest(edges, start, STOP)
    q = [(start, 0)]
    visited = Set{CI}()
    best = 0
    while !isempty(q)
        rc, d = pop!(q)
        if d == -1
            delete!(visited, rc)
        elseif rc == STOP
            best = max(best, d)
        elseif rc ∉ visited
            push!(visited, rc)
            push!(q, (rc, -1))
            for (np, l) in edges[rc]
                push!(q, (np, d + l))
            end
        end
    end
    return best
end

function main(path)
    MAP = stack(readlines(path); dims=1)
    height = size(MAP, 1)
    START = findfirst(==('.'), MAP[begin:begin, :])
    stop_x = findfirst(==('.'), MAP[end, :])
    STOP = CI(height, stop_x)

    p1 = dfs(MAP, START, STOP, Set([START]))
    println(p1)

    edges = make_edges(MAP)
    println(longest(edges, START, STOP))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
