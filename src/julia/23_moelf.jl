const CI = CartesianIndex{2}
const L, R, U, D = CI(0, -1), CI(0, 1), CI(-1, 0), CI(1, 0)
const SLOPE = Dict('>' => R, '<' => L, '^' => U, 'v' => D)

struct State
    pos::CI
    steps::Int
end

function paint(map)
    for row in eachrow(map)
        for c in row
            print(c)
        end
        println()
    end
end

function legal_next(pos, prev, q, MAP; part1=true)
    res = CI[]
    if part1 && haskey(SLOPE, MAP[pos])
        next_p = pos + SLOPE[MAP[pos]]
        next_p == prev && return res
        next_p in q && return res
        return [next_p]
    else
        for dir in (L, R, U, D)
            next_p = pos + dir
            !isassigned(MAP, next_p) && continue
            MAP[next_p] == '#' && continue
            next_p == prev && continue
            next_p in q && continue
            push!(res, next_p)
        end
    end
    res
end

function main(path)
    MAP = stack(readlines(path); dims=1)
    height = size(MAP, 1)
    START = findfirst(==('.'), MAP[begin:begin, :])

    stop_x = findfirst(==('.'), MAP[end, :])
    STOP = CI(height, stop_x)

    path_queue = [[START]]
    done_queue = empty(path_queue)

    while !isempty(path_queue)
        i = 1
        while i <= length(path_queue)
            q = path_queue[i]
            L = length(q)
            pos = q[L]
            prev = get(q, L - 1, CI(0, 0))
            nexts = legal_next(pos, prev, q, MAP; part1=true)
            if pos == STOP
                push!(done_queue, popat!(path_queue, i))
                break
            end
            if isempty(nexts)
                deleteat!(path_queue, i)
                break
            end
            primal, alts... = nexts
            push!(q, primal)
            for a in alts
                copy_q = copy(q)
                copy_q[end] = a
                push!(path_queue, copy_q)
            end
            i += 1
        end
    end

    println(maximum(length.(done_queue)) - 1)
end


(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
