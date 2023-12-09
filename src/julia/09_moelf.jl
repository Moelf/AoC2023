using DelimitedFiles: readdlm

predict(vec) = allequal(vec) ? last(vec) : last(vec) + predict(diff(vec))

function main(path)
    M = readdlm(path, Int)
    p1 = p2 = 0
    for row in eachrow(M)
        p1 += predict(row)
        p2 += predict(reverse(row))
    end
    println(p1)
    println(p2)
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
