const CI = CartesianIndex{2}
const L, R, U, D = CI(0, -1), CI(0, 1), CI(-1, 0), CI(1, 0)
const DIRS = Dict(
    "R" => R, "D" => D, "L" => L, "U" => U,
    '0' => R, '1' => D, '2' => L, '3' => U)

function make_poly(dirs, nums)
    POS = CI(0, 0)
    PATH = CI[]
    for (D, N) in zip(dirs, nums)
        for _ in 1:N
            POS += D
            push!(PATH, POS)
        end
    end
    return PATH
end
# https://en.wikipedia.org/wiki/Shoelace_formula
function shoelace(poly)
    a = 0
    for i in 1:lastindex(poly)-1
        p1 = poly[i]
        p2 = poly[i+1]
        a += p1[1] * p2[2] - p2[1] * p1[2]
    end
    return abs(a ÷ 2)
end
# https://en.wikipedia.org/wiki/Pick's_theorem
function in_area(poly)
    A = shoelace(poly)
    b = length(poly)
    return A + 1 - b ÷ 2
end

function impl(dirs, nums)
    poly = make_poly(dirs, nums)
    return in_area(poly) + length(poly)
end

function main(path)
    M_str = stack(split.(readlines(path)); dims=1)
    dir_str, num_str, color_str = eachcol(M_str)

    dirs = [DIRS[s] for s in dir_str]
    nums = parse.(Int, num_str)
    println(impl(dirs, nums))

    empty!(dirs); empty!(nums)

    for s in color_str
        num_str..., dir_str = replace(s, r"(#|\)|\()" => "")
        push!(dirs, DIRS[dir_str])
        push!(nums, parse(Int, num_str; base=16))
    end
    println(impl(dirs, nums))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
