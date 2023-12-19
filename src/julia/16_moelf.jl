const CI = CartesianIndex{2}

const L, R, U, D = CI(0, -1), CI(0, 1), CI(-1, 0), CI(1, 0)

struct Photon
    pos::CI
    dir::CI
end

function interact(photon, tile_loc, tile) 
    if tile == '.'
        [Photon(tile_loc, photon.dir)]
    elseif tile == '|'
        if photon.dir in (U, D)
            [Photon(tile_loc, photon.dir)]
        else
            [Photon(tile_loc, U), Photon(tile_loc, D)]
        end
    elseif tile == '-'
        if photon.dir in (L, R)
            [Photon(tile_loc, photon.dir)]
        else
            [Photon(tile_loc, L), Photon(tile_loc, R)]
        end
    elseif tile == '\\'
        dir = photon.dir
        new_dir = if dir == R
            D
        elseif dir == L
            U
        elseif dir == U
            L
        elseif dir == D
            R
        end
        [Photon(tile_loc, new_dir)]
    elseif tile == '/'
        dir = photon.dir
        new_dir = if dir == R
            U
        elseif dir == L
            D
        elseif dir == U
            R
        elseif dir == D
            L
        end
        [Photon(tile_loc, new_dir)]
    end
end

function count_energy(init_photon, M)
    photons = [init_photon]
    energized = Set{Photon}()
    while !isempty(photons)
        photon = pop!(photons)
        if isassigned(M, photon.pos)
            push!(energized, photon)
        end
        next_pos = photon.pos + photon.dir
        !isassigned(M, next_pos) && continue
        tile = M[next_pos]
        new_photons = interact(photon, next_pos, tile)

        filter!(∉(energized), new_photons)
        append!(photons, new_photons)
    end
    us = unique([x.pos for x in energized])
    return length(us)
end

function main(path)
    M = stack(readlines(path); dims=1)
    counter = Base.Fix2(count_energy, M)

    p1 = counter(Photon(CI(1, 0), R))
    println(p1)

    HEIGHT, WIDTH = size(M)
    all_starts = @. [
        Photon(CI(1:HEIGHT, 0), R);
        Photon(CI(1:HEIGHT, WIDTH+1), L);
        Photon(CI(0, 1:WIDTH), D);
        Photon(CI(HEIGHT+1, 1:WIDTH), U);
    ]

    p2, _ = findmax(counter, all_starts)
    println(p2)
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
