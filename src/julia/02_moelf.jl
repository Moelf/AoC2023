const INPUT_PATH = ARGS[1]
const ALL_LINES = readlines(INPUT_PATH)

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
    return dict["red"] <= 12 &&
    dict["green"] <= 13 &&
    dict["blue"] <= 14
end

p1 = sum(findall(part1_pred, ALL_LINES))
println(p1)

# Part II
part2(line) = line |> line_max |> values |> prod
p2 = sum(part2, ALL_LINES)
println(p2)
