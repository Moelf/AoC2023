function color_dict(a::RegexMatch)
    num, color = a.captures
    Dict(color => parse(Int, num))
end

function line_max(line)
    RE = r"(\d+)\s(blue|green|red)"
    parts = eachmatch(RE, line)
    mapreduce(color_dict, mergewith(max), parts)
end

# Part I
function part1_pred(line)
    dict = line_max(line)
    return dict["red"] <= 12 && dict["green"] <= 13 && dict["blue"] <= 14
end


# Part II
part2(line) = line |> line_max |> values |> prod

function main(path)
    lines = readlines(path)
    p1 = sum(findall(part1_pred, lines))
    println(p1)
    println(sum(part2, lines))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
