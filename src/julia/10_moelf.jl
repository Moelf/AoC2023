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
    return in_dir == E1 ? E2 : E1
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
    dir_idx = findfirst(FOUR_DIRS) do dir
        !isassigned(M, pos+dir) && return false
        sym = M[pos+dir]
        !haskey(CONNECTIONS, sym) && return false
        out_dir = in_out(sym, -dir)
        !isnothing(out_dir)
    end
    dir = FOUR_DIRS[dir_idx]
    p1, main_loop_pipes = impl1(M, pos, dir)
    println(p1)
    M_str = string.(M)
    for i in CartesianIndices(M_str)
        if i in main_loop_pipes
            M_str[i] = Base.text_colors[:red] * M_str[i]
        end
        M_str[i] = Base.text_colors[:default] * M_str[i]
    end

    for r in eachrow(M_str)
        println(join(r))
    end

    p2 = 0
    for ir in axes(M, 1)
        inside = false 
        pipe_start = ' '
        for ic in axes(M, 2)
            pos = CI(ir, ic)
            on_boundary = pos in main_loop_pipes
            if on_boundary
                sym = M[pos]
                if sym == '|'
                    inside = !inside
                elseif pipe_start == ' '
                    pipe_start = sym
                elseif sym != '-'


                end
            end
        end
    end
    println(p2)

end


(abspath(PROGRAM_FILE) == @__FILE__) && (main(ARGS[1]))
