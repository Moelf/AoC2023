using Test

const ALL_LANGUAGES = readdir("src")
const INPUTS = readdir("./inputs")

"""
    run_solution(day_num_str, input_path, ::Val{T}) -> Vector{String}

Given number of day in two-digit format (e.g. "00", "12") and an input file path `input_path`, run the algorithm
and return the output as a vector of strings.

`T` is the language type, for example `Val{:cpp}` or `Val{:julia}`.

For `Val{:cpp}`, you probably want to use `readlines(`cmd`)` to read the stdout of your executable into a vector of strings.
"""
function run_solution() end

function run_solution(day_num_str, input_path, ::Val{:cpp})
    source_path = joinpath(@__DIR__, "src/cpp/$day_num_str.cpp")
    !isfile(source_path) && return nothing
    run(`g++ -std=c++20 $source_path -o $day_num_str.o`)
    return readlines(`./$day_num_str.o $input_path`)
end

function run_solution(day_num_str, input_path, ::Val{:julia})
    source_path = joinpath(@__DIR__, "src/julia/$day_num_str.jl")
    return readlines(`julia $source_path $input_path`)
end

function get_all_inputs_solutions(day_num_str)
    paths = filter(startswith(day_num_str), INPUTS)
    pairs = map(paths) do p
        input = joinpath("./inputs", p)
        solution = joinpath("./solutions", p)
        if !isfile(solution)
            error("Solution file $solution does not exist but input file $input does, make sure to upload both")
            exit(1)
        end
        return (input, readlines(solution))
    end

    return pairs
end



for day_num in 0:25
    day_num_str = lpad(day_num, 2, '0')
    inputs_solutions = get_all_inputs_solutions(day_num_str)
    isempty(inputs_solutions) && continue
    @testset verbose = true "Day $day_num_str" begin
        for lang in ALL_LANGUAGES, (input_path, reference_output) in inputs_solutions
            our_output = run_solution(day_num_str, input_path, Val(Symbol(lang)))
            isnothing(our_output) && continue
            for (i, (our, ref)) in enumerate(zip(our_output, reference_output))
                input_filename = last(splitpath(input_path))
                @testset "$(rpad(lang, 7, ' ')) $input_filename Part $i" begin
                    @test our == ref
                end
            end
        end
    end
end
