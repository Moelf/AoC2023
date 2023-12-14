const CI = CartesianIndex{2}

# Matrix coord:    up         down      right     left
const U, D, R, L = CI(-1, 0), CI(1, 0), CI(0, 1), CI(0, -1)
const FOUR_DIRS = (U, D, L, R)

const CONNECTIONS = Dict(
    '|' => (U, D),
    '-' => (L, R),
    'L' => (U, R),
    'J' => (U, L),
    '7' => (L, D),
    'F' => (R, D),
)

function in_out(pipe, in_dir)
    E1, E2 = CONNECTIONS[pipe]
    if in_dir == E1
        E2
    elseif in_dir == E2
        E1
    else
        nothing
    end
end

function step(M, here, here_dir)
    next = here + here_dir
    next_pipe = M[next]
    if next_pipe == 'S'
        return next, next
    end
    next_dir = in_out(next_pipe, -here_dir)
    return next, next_dir
end

function impl1(M, pos, dir)
    res = 0
    loop_pipes = [pos]
    while true
        pos, dir = step(M, pos, dir)
        push!(loop_pipes, pos)
        res += 1
        M[pos] == 'S' && break
    end
    return res ÷ 2, loop_pipes
end

function main(path)
    M = stack(readlines(path); dims=1)
    pos = findfirst(==('S'), M)::CI
    dir_idx = findall(FOUR_DIRS) do dir
        !isassigned(M, pos + dir) && return false
        sym = M[pos+dir]
        !haskey(CONNECTIONS, sym) && return false
        out_dir = in_out(sym, -dir)
        !isnothing(out_dir)
    end
    dirs = FOUR_DIRS[dir_idx]
    p1, main_loop_pipes = impl1(M, pos, dirs[begin])
    println(p1)

    # replace 'S' with real pipe
    M[pos] = findfirst(CONNECTIONS) do v
        Set(Tuple(v)) == Set(Tuple(dirs))
    end
    # clear out non-pipe map with ' '
    for c in CartesianIndices(M)
        if c ∉ main_loop_pipes
            M[c] = ' '
        end
    end

    for col in eachcol(M)
        inside = false
        path_start = area_start = 0
        if first(col) != ' '
            path_start = 1
        else
            area_start = 1
        end
        for (i, c) in enumerate(col)
            # maintain state
            c in (' ', '|') && continue

            prevc = get(col, i - 1, '.')
            if prevc == ' ' # area -> path
                col[area_start:i-1] .= inside ? 'I' : 'O'
                area_start = nothing
                path_start = i
            end

            nextc = get(col, i + 1, '.')
            if nextc == ' ' # path -> area
                if string(col[path_start], c) ∉ ("FL", "7J")
                    inside = !inside
                end
                area_start = i + 1
                path_start = nothing
            elseif c in ('L', 'J', '-') # path -> new path
                if string(col[path_start], c) ∉ ("FL", "7J")
                    inside = !inside
                end
                path_start = i + 1
            end
        end
    end
    println(count(==('I'), M))

end

(abspath(PROGRAM_FILE) == @__FILE__) && (main(ARGS[1]))
