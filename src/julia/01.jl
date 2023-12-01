const INPUT_PATH = ARGS[1]

using Test

# Part I
function getnumber(line)
    i = findfirst(isdigit, line)
    j = findlast(isdigit, line)
    return parse(Int, string(line[i],line[j]))
end

function part1()
    lines = readlines(INPUT_PATH)
    println(sum(getnumber, lines))
end

part1() # Answer: 55123

const lookup = Dict("one" => 1, "two" => 2, "three" => 3, "four" => 4, "five" => 5, "six" => 6, "seven" => 7, "eight" => 8, "nine" => 9)

const RE = Regex("$(join(keys(lookup), '|'))|\\d")

# Part II
function get_num_from_string(str)
	dig = tryparse(Int, str)
    !isnothing(dig) && return dig
    return lookup[str]
end

function getnumber_part2(line)
    captures = collect(eachmatch(RE, line; overlap=true))
    num_first = get_num_from_string(captures[begin].match)
    num_last = get_num_from_string(captures[end].match)
    return num_first * 10 + num_last
end

# @testset "getnumber_part2" begin
#     @test getnumber_part2("two1nine") == 29
#     @test getnumber_part2("6vzpjhtwonemc") == 61
#     @test getnumber_part2("eightwothree") == 83
#     @test getnumber_part2("abcone2threexyz") == 13
#     @test getnumber_part2("xtwone3four") == 24
#     @test getnumber_part2("4nineeightseven2") == 42
#     @test getnumber_part2("zoneight234") == 14
#     @test getnumber_part2("7pqrstsixteen") == 76
# end

function part2()
    lines = readlines(INPUT_PATH)
    println(sum(getnumber_part2, lines))
end

part2() # Answer: 55260
