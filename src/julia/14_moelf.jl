function slide!(col)
    i = START = firstindex(col)
    END = lastindex(col)
    while i <= END
        c = col[i]
        if c == 'O'
            j = i-1
            if get(col, j, ' ') == '.'
                col[j], col[i] = col[i], col[j]
                i = START
                continue
            end
        end
        i += 1
    end
end

slide_north!(M::Matrix) = slide!.(eachcol(M))
slide_west!(M::Matrix) = slide!.(eachrow(M))

function cycle!(M)
    slide_north!(M)

    slide_west!(M)

    reverse!(M; dims=1)
    slide_north!(M)
    reverse!(M; dims=1)

    reverse!(M; dims=2)
    slide_west!(M)
    reverse!(M; dims=2)
end

function load(M)
    res = 0
    for (i,row) in zip(reverse(axes(M,1)), eachrow(M))
        res += i * count(==('O'), row)
    end
    return res
end

function main(path)
    M = stack(readlines(path); dims=1)
    M2 = copy(M)
    slide!.(eachcol(M))
    println(load(M))

    seen = Matrix{Char}[]
    local j
    N = 1000000000
    for outer j in 1:N
        cycle!(M2)
        any(==(M2), seen) && break
        push!(seen, copy(M2))
    end
    first_occur = findfirst(==(M2), seen)
    PERIOD = j - first_occur
    REM = N - first_occur
    println(load(seen[first_occur + mod(REM , PERIOD)]))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
