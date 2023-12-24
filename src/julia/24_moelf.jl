struct Hail
    pos::NTuple{3,Int}
    vel::NTuple{3,Int}
end

slopey(h) = big(h.vel[2]) / h.vel[1]
slopez(h) = big(h.vel[3]) / h.vel[1]
isfuture(h, x0) = sign(x0 - h.pos[1]) == sign(h.vel[1])

function intersect(h1, h2)
    x1, y1 = h1.pos
    x2, y2 = h2.pos
    S1, S2 = slopey(h1), slopey(h2)
    x0 = (y2 - y1 - S2 * x2 + S1 * x1) / (S1 - S2)
    y0 = (x0 - x1) * S1 + y1

    x0, y0
end

function forecast(h, x0)
    x, y, z = h.pos
    Sy = slopey(h)
    Sz = slopez(h)
    Δy = (x0 - x) * Sy
    Δz = (x0 - x) * Sz
    return (x0, y + Δy, z + Δz)
end

function impl2(hails, v_extrema)
    xlim, ylim, zlim = v_extrema
    for xi in range(xlim...), yi in 0:100
        v_offset = (xi, yi, 0)
        dummy = [Hail(x.pos, x.vel .- v_offset) for x in hails]
        h1, rest... = dummy
        xy = intersect(h1, rest[1])
        x0 = xy[1]
        isinf(x0) && continue
        if all(h -> all(intersect(h1, h) .≈ xy), rest)
            for zi in range(zlim...)
                v_offset = (xi, yi, zi)
                dummy2 = [Hail(x.pos, x.vel .- v_offset) for x in hails]
                h2, rest2... = dummy2
                est = forecast(h2, x0)
                if all(h -> all(forecast(h, x0) .≈ est), rest2)
                    return sum(round.(BigInt, est))
                end
            end
        end
    end
    error("no solution")
end

function main(path)
    vs = Int[]

    hails = map(eachline(path)) do line
        l, r = split(line, " @ ")
        pos = Tuple(parse.(Int, split(l, ", ")))
        vel = Tuple(parse.(Int, split(r, ", ")))
        append!(vs, vel)
        Hail(pos, vel)
    end

    v_extrema = extrema.(eachrow(reshape(vs, 3, :)))

    p1 = 0
    for i in eachindex(hails), j in i+1:lastindex(hails)
        h1 = hails[i]
        h2 = hails[j]
        x0, y0 = intersect(h1, h2)
        !isfuture(h1, x0) && continue
        !isfuture(h2, x0) && continue
        if all(x -> 200000000000000 <= x <= 400000000000000, (x0, y0))
            p1 += 1
        end
    end
    println(p1)

    println(impl2(hails, v_extrema))
end


(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
