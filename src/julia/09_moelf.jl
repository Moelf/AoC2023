using DelimitedFiles: readdlm

function predict(vec; rev=false)
    if allequal(vec)
        first(vec)
    elseif rev
        first(vec) - predict(diff(vec); rev)
    else
        last(vec) + predict(diff(vec); rev)
    end
end

function main(path)
    M = readdlm(path, Int)
    p1 = p2 = 0
    for row in eachrow(M)
        p1 += predict(row)
        p2 += predict(row; rev=true)
    end
    println(p1)
    println(p2)
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
