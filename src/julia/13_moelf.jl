function reflection_line(M, tol; dims)
    max_size = size(M, dims)
    for x in axes(M, dims)
        window_size = min(x, max_size - x)
        pattern1 = selectdim(M, dims, x-window_size+1:x)
        pattern2 = selectdim(M, dims, reverse(x+1:x+window_size))
        isempty(pattern1) && return 0
        if count(pattern1 .!= pattern2) == tol
            return x
        end
    end
end

function impl(Ms, tol)
    sum(Ms) do M
        100 * reflection_line(M, tol; dims=1) + 
        reflection_line(M, tol; dims=2)
    end
end

function main(path)
    rawstr = read(path, String)
    vec_Ms = stack.(split.(split(rawstr, "\n\n")); dims=1)

    println(impl(vec_Ms, 0))
    println(impl(vec_Ms, 1))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
