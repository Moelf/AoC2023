const CI = CartesianIndex{2}

const L, R, U, D = CI(0, -1), CI(0, 1), CI(-1, 0), CI(1, 0)

struct Photon
    pos::CI
    dir::CI
end

function interact(photon::Photon, ::Val{'.'}) 
    [Photon(photon.pos + photon.dir, photon.dir)]
end

function interact(photon::Photon, ::Val{'|'}) 
    if photon.dir in (U, D)
        [Photon(photon.pos + photon.dir, photon.dir)]
    else
        [Photon(photon.pos + photon.dir, U), Photon(photon.pos + photon.dir, D)]
    end
end

function interact(photon::Photon, ::Val{'-'}) 
    if photon.dir in (L, R)
        [Photon(photon.pos + photon.dir, photon.dir)]
    else
        [Photon(photon.pos + photon.dir, L), Photon(photon.pos + photon.dir, R)]
    end
end

function interact(photon::Photon, ::Val{'\\'}) 
    new_dir = if photon.dir == R
        D
    elseif photon.dir == L
        U
    elseif photon.dir == U
        L
    elseif photon.dir == D
        R
    end
    [Photon(photon.pos + photon.dir, new_dir)]
end

function interact(photon::Photon, ::Val{'/'}) 
    new_dir = if photon.dir == R
        U
    elseif photon.dir == L
        D
    elseif photon.dir == U
        R
    elseif photon.dir == D
        L
    end
    [Photon(photon.pos + photon.dir, new_dir)]
end

function step(photon, MAP)
    next_pos = photon.pos + photon.dir
    if !isassigned(MAP, next_pos)
        return nothing
    end
    tile = MAP[next_pos]
    return interact(photon, Val(tile))
end

function count_energy(init_photon, M)
    photons = [init_photon]
    energized = Set{Photon}()
    while !isempty(photons)
        photon = pop!(photons)
        if isassigned(M, photon.pos)
            push!(energized, photon)
        end
        new_photons = step(photon, M)
        if !isnothing(new_photons)
            for np in new_photons
                if np ∉ energized
                    push!(photons, np)
                end
            end
        end
    end
    return length(unique(getproperty.(energized, :pos)))
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
main(ARGS[1])
