const CI = CartesianIndex{2}
const L, R, U, D = CI(0, -1), CI(0, 1), CI(-1, 0), CI(1, 0)
const DIRS = (L, R, U, D)
const SLOPE = Dict('>' => R, '<' => L, '^' => U, 'v' => D)

function mutual!(edges, pos, dir)
    get!(edges, pos, Dict())[pos+dir] = 1
    get!(edges, pos - dir, Dict())[pos] = 1
end

function make_edges(MAP)
    # double linked list
    # from_node -> (to_node -> distance)
    edges = Dict{CI,Dict{CI,Int}}()
    for pos in CartesianIndices(MAP)
        v = MAP[pos]
        v == '#' && continue
        if haskey(SLOPE, v)
            mutual!(edges, pos, SLOPE[v])
        else
            for np in pos .+ DIRS
                if isassigned(MAP, np) && MAP[np] == '.'
                    get!(edges, pos, Dict())[np] = 1
                    get!(edges, np, Dict())[pos] = 1
                end
            end
        end
    end

    # graph condense
    ns = findall(e -> length(e) == 2, edges)
    while !isempty(ns)
        n = pop!(ns)
        (pos1, l1), (pos2, l2) = edges[n]
        if !haskey(edges[pos1], n) || !haskey(edges[pos2], n)
            continue
        end
        delete!(edges[pos1], n)
        delete!(edges[pos2], n)
        new_len = l1 + l2
        edges[pos1][pos2] = new_len
        edges[pos2][pos1] = new_len
        delete!(edges, n)
    end
    edges
end

function dfs(edges, start, STOP)
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
    START = findfirst(==('.'), MAP[begin:begin, :])
    stop_x = findfirst(==('.'), MAP[end, :])
    STOP = CI(size(MAP, 1), stop_x)

    edges = make_edges(MAP)
    println(dfs(edges, START, STOP))

    replace!(MAP, (x => '.' for x in keys(SLOPE))...)
    edges2 = make_edges(MAP)
    println(dfs(edges2, START, STOP))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
