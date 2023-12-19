const CI = CartesianIndex{2}
const MAX_HEAT = typemax(Int)

const ALL_DIRS = (CI(0, -1), CI(0, 1), CI(-1, 0), CI(1, 0))

struct MapState
    pos::CI
    dir::CI
    n_block::Int
end

struct State
    loc::MapState
    heat_loss::Int
end
heat(s::State) = s.heat_loss
Base.isless(s1::State, s2::State) = heat(s1) < heat(s2)

function pathfinding(MAP, MIN, MAX)
    DEST = CI(size(MAP))

    Aqueue = [State(MapState(CI(1, 1), CI(0, 0), 0), 0)]
    seen = Set{MapState}()

    while !isempty(Aqueue)
        state = popfirst!(Aqueue)
        (; loc, heat_loss) = state
        loc ∈ seen && continue

        (; pos, dir, n_block) = loc

        push!(seen, loc)
        pos == DEST && n_block >= MIN && return heat_loss

        for new_dir in ALL_DIRS
            new_pos = pos + new_dir
            new_n_block = (new_dir == dir ? n_block + 1 : 1)

            if dir == -new_dir || new_n_block > MAX || !isassigned(MAP, new_pos)
                continue
            end

            if new_dir != dir && n_block < MIN && dir != CI(0, 0)
                continue
            end

            Δ_heat = MAP[new_pos]
            ns = State(MapState(new_pos, new_dir, new_n_block), heat_loss + Δ_heat)
            i = searchsortedfirst(Aqueue, ns)
            insert!(Aqueue, i, ns)
        end
    end
end

function main(path)
    MAP = parse.(Int, stack(readlines(path); dims=1))
    println(pathfinding(MAP, 1, 3))
    println(pathfinding(MAP, 4, 10))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
