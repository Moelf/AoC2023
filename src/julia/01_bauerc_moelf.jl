const INPUT_PATH = ARGS[1]

# Part I
function getnumber(line)
    i = findfirst(isdigit, line)
    j = findlast(isdigit, line)
    return parse(Int, string(line[i], line[j]))
end

function part1()
    lines = readlines(INPUT_PATH)
    println(sum(getnumber, lines))
end

part1() # Answer: 55123

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

# Part II
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

function part2()
    lines = readlines(INPUT_PATH)
    println(sum(getnumber_part2, lines))
end

part2() # Answer: 55260
