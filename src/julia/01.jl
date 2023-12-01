const INPUTDIR = joinpath(@__DIR__, "../../inputs/")

using Test

# Part I

# function test_getnumber()
#     @testset "getnumber" begin
#         @test getnumber("1abc2") == 12
#         @test getnumber("pqr3stu8vwx") == 38
#         @test getnumber("a1b2c3d4e5f") == 15
#         @test getnumber("treb7uchet") == 77
#     end
# end

function getnumber(line)
    i = findfirst(isdigit, line)
    j = findlast(isdigit, line)
    return parse(Int, string(line[i],line[j]))
end

function part1()
    lines = readlines(joinpath(INPUTDIR, "01_bauerc.txt"))
    println("Answer: ", sum(getnumber, lines))
end

part1() # Answer: 55123


# Part II

function try_get_num_from_string(str)
	startswith(str, "one") && return 1
	startswith(str, "two") && return 2
	startswith(str, "three") && return 3
	startswith(str, "four") && return 4
	startswith(str, "five") && return 5
	startswith(str, "six") && return 6
	startswith(str, "seven") && return 7
	startswith(str, "eight") && return 8
	startswith(str, "nine") && return 9
	return nothing
end

function getnumber_part2(line)
	num_first = nothing
	num_last  = nothing
	for (i, c) in pairs(line)
		if isdigit(c)
			num = parse(Int, c)
		else
			num = try_get_num_from_string(@view line[i:end])
			isnothing(num) && continue
		end

		if isnothing(num_first)
			num_first = num
		end
		num_last = num
	end
    return parse(Int, string(num_first, num_last))
end

# function test_getnumber_part2()
#     @testset "getnumber_part2" begin
#         @test getnumber_part2("two1nine") == 29
#         @test getnumber_part2("eightwothree") == 83
#         @test getnumber_part2("abcone2threexyz") == 13
#         @test getnumber_part2("xtwone3four") == 24
#         @test getnumber_part2("4nineeightseven2") == 42
#         @test getnumber_part2("zoneight234") == 14
#         @test getnumber_part2("7pqrstsixteen") == 76
#     end
# end

function part2()
    lines = readlines(joinpath(INPUTDIR, "01_bauerc.txt"))
    println("Answer: ", sum(getnumber_part2, lines))
end

part2() # Answer: 55260
