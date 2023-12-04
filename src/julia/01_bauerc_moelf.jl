# Part I
function getnumber(line)
    i = findfirst(isdigit, line)
    j = findlast(isdigit, line)
    return parse(Int, string(line[i], line[j]))
end

part1(lines) = sum(getnumber, lines)


# Part II
const lookup = Dict(
    "one" => 1,
    "two" => 2,
    "three" => 3,
    "four" => 4,
    "five" => 5,
    "six" => 6,
    "seven" => 7,
    "eight" => 8,
    "nine" => 9,
)

const RE = Regex("$(join(keys(lookup), '|'))|\\d")

function get_num_from_string(str)
    dig = tryparse(Int, str)
    !isnothing(dig) && return dig
    return lookup[str]
end

function getnumber_part2(line)
    # overlap=true is important
    # getnumber_part2("6vzpjhtwonemc") == 61
    captures = collect(eachmatch(RE, line; overlap = true))
    num_first = get_num_from_string(captures[begin].match)
    num_last = get_num_from_string(captures[end].match)
    return num_first * 10 + num_last
end

part2(lines) = sum(getnumber_part2, lines)

function main(path)
    lines = readlines(path)
    println(part1(lines))
    println(part2(lines))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
