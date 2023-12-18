const CI = CartesianIndex{2}
const L, R, U, D = CI(0, -1), CI(0, 1), CI(-1, 0), CI(1, 0)
const DIRS = Dict(
    "R" => R, "D" => D, "L" => L, "U" => U,
    '0' => R, '1' => D, '2' => L, '3' => U)

# https://en.wikipedia.org/wiki/Shoelace_formula
# https://en.wikipedia.org/wiki/Pick's_theorem
function impl(dirs, nums)
    POS1 = POS2 = CI(0, 0)
    b = A = 0
    for (D, N) in zip(dirs, nums)
        for _ in 1:N
            b += 1
            POS2 += D
            A += POS1[1] * POS2[2] - POS2[1] * POS1[2]
            POS1 = POS2
        end
    end
    in_area = abs(A)÷2 + 1 - b ÷ 2
    return in_area + b
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
