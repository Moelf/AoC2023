const INPUTDIR = joinpath(@__DIR__, "../../inputs/")

function getnumber(line)
    i = findfirst(isdigit, line)
    j = findlast(isdigit, line)
    return parse(Int, string(line[i],line[j]))
end

function main()
    lines = readlines(joinpath(INPUTDIR, "01_bauerc.txt"))
    println("Answer: ", sum(getnumber, lines))
end

main() # Answer: 55123
