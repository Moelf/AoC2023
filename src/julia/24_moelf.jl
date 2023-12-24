using LinearAlgebra: ×

struct Hail
    pos::Vector{Int}
    vel::Vector{Int}
end

slope(h, dim) = big(h.vel[dim]) / h.vel[1]
isfuture(h, x0) = sign(x0 - h.pos[1]) == sign(h.vel[1])

function intersect(h1, h2)
    x1, y1 = h1.pos
    x2, y2 = h2.pos
    S1, S2 = slope(h1, 2), slope(h2, 2)
    x0 = (y2 - y1 - S2 * x2 + S1 * x1) / (S1 - S2)
    y0 = (x0 - x1) * S1 + y1

    x0, y0
end

function skew(x)
    x₁, x₂, x₃ = x
    [
        0  -x₃  x₂
        x₃  0  -x₁
       -x₂  x₁  0
    ]
end

function main(path)
    hails = map(eachline(path)) do line
        l, r = split(line, " @ ")
        pos = parse.(Int, split(l, ", "))
        vel = parse.(Int, split(r, ", "))
        Hail(pos, vel)
    end

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

    x₁, y₁ = hails[1].pos, hails[1].vel
    x₂, y₂ = hails[2].pos, hails[2].vel
    x₃, y₃ = hails[3].pos, hails[3].vel

    A₁ = hcat(skew(y₁ - y₂), skew(x₂ - x₁))
    RHS₁ = x₂ × y₂ - x₁ × y₁

    A₂ = hcat(skew(y₁ - y₃), skew(x₃ - x₁))
    RHS₂ = x₃ × y₃ - x₁ × y₁

    A = vcat(A₁, A₂)
    RHS = vcat(RHS₁, RHS₂)

    sol = A \ RHS
    println(sum(round.(Int, first(sol, 3))))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
