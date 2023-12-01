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
    run(`g++ -std=c++20 ./src/cpp/$day_num_str.cpp -o $day_num_str.o`)
    return readlines(`./$day_num_str.o $input_path`)
end

function run_solution(day_num_str, input_path, ::Val{:julia})
    return readlines(`julia src/julia/$day_num_str.jl $input_path`)
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
            reference_output
            for (i, (our, ref)) in enumerate(zip(our_output, reference_output))
                @testset "$lang $input_path Part $i" begin
                    @test our == ref
                end
            end
        end
    end
end
