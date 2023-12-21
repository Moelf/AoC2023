const CI = CartesianIndex{2}
const L, R, U, D = CI(0, -1), CI(0, 1), CI(-1, 0), CI(1, 0)
const DIRS = (L, R, U, D)

wrap_around(pos, size) = CI(mod1.(Tuple(pos), size))

function explore(MAP, start_pos, N)
    queue = [start_pos]
    temp_queue = copy(queue)
    seen = Set(queue)
    SIZE = size(MAP)

    for _ in 1:N
        for q in queue
            push!(seen, q)
        end
        copy!(temp_queue, queue)
        empty!(queue)

        while !isempty(temp_queue)
            pos = pop!(temp_queue)
            for dir in DIRS
                new_pos = pos + dir
                idx_pos = wrap_around(new_pos, SIZE)
                MAP[idx_pos] == '#' && continue
                new_pos ∈ seen && continue
                push!(seen, new_pos)
                push!(queue, new_pos)
            end
        end
        empty!(seen)
    end
    return length(queue)
end

function main(path)
    MAP = stack(readlines(path); dims=1)
    start_pos = findfirst(==('S'), MAP)
    println(explore(MAP, start_pos, 64))

    N = 26501365
    L = size(MAP, 1)
    # S row and col are 100% walkable
    @assert all(!=('#'), MAP[start_pos[1], :])
    @assert all(!=('#'), MAP[:, start_pos[2]])
    # Walking in a straight line would end on the edge of a garden plot
    @assert mod(N - L ÷ 2, L) == 0

    _mod = mod(N, L)
    f1, f2, f3 = [explore(MAP, start_pos, n) for n in [_mod, _mod + L, _mod + L * 2]]
    # 3d + b = f2 - f1 = f21
    f21 = f2 - f1
    # 5a + b = f3 - f2 = f32
    f32 = f3 - f2
    a = (f32 - f21) ÷ 2
    b = f21 - 3a
    c = f1 - b - a

    reach = cld(N, L)
    println(a * reach^2 + b * reach + c)

end


(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
