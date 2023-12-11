const CI = CartesianIndex
cityblock(a::CI, b::CI) = sum(abs, Tuple(a-b))

function impl(MAP, exp_const)
    galaxies = findall(==('#'), MAP)
    N = exp_const - 1
    for (i, j) in zip(axes(MAP, 1), axes(MAP, 2))
        if all(==('.'), @view MAP[i, :])
            mask = findall(c -> c[1] < i, galaxies)
            galaxies[mask] .-= CI(N, 0)
        end

        if all(==('.'), @view MAP[:, j])
            mask = findall(c -> c[2] < j, galaxies)
            galaxies[mask] .-= CI(0, N)
        end
    end

    res = 0
    for i in eachindex(galaxies), j in i+1:lastindex(galaxies)
        res += cityblock(galaxies[i], galaxies[j])
    end

    res
end

function main(path)
    MAP = stack(readlines(path); dims=1)
    println(impl(MAP, 2))
    println(impl(MAP, 1000000))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
