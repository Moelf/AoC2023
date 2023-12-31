using Test
using Pkg
using Downloads
Pkg.activate(@__DIR__)
using AoC2023

const cookie = get(ENV, "AOC_COOKIE", "")
if get(ENV, "CI", "false") == "true"
    isempty(cookie) && error("AOC_COOKIE environment variable must be set for CI")
end
const HEADERS = headers=Dict("Cookie" => "session=$cookie")

const ALL_LANGUAGES = isempty(ARGS) ? ["julia","cpp","python"] : ARGS

"""
    run_solution(source_path, input_path, ::Val{T}) -> Vector{String}

Given path to source code and an input file path `input_path`, run the algorithm
and return the output as a vector of strings.

`T` is the language type, for example `Val{:cpp}` or `Val{:julia}`.

For `Val{:cpp}`, you probably want to use `readlines(`cmd`)` to read the stdout of your executable into a vector of strings.
"""
function run_solution() end


function run_solution(source_path, input_path, ::Val{:cpp})
    exename = joinpath("bazel-bin/src/cpp", replace(splitpath(source_path)[end], ".cpp"=>""))
    return readlines(`./$exename $input_path`)
end

function run_solution(source_path, input_path, ::Val{:julia})
    original_stdout = stdout
    rd, wr = redirect_stdout()
    AoC2023.DAY_MODULES[source_path].main(input_path)
    close(wr)
    redirect_stdout(original_stdout)
    result = readlines(rd)
    return result
end

function run_solution(source_path, input_path, ::Val{:python})
    return readlines(`python3 $source_path $input_path`)
end

function get_all_inputs_solutions(day_num_str)
    input_paths = readdir(joinpath(@__DIR__, "inputs"))
    paths = filter(startswith(day_num_str), input_paths)
    pairs = map(paths) do p
        input = joinpath("./inputs", p)
        solution = joinpath("./solutions", p)
        if !isfile(solution)
            return (input, nothing)
        end
        return (input, readlines(solution))
    end

    return pairs
end


function test_lang(day_num_str, input_path, reference_output, lang)
    LANG_DIR = joinpath(@__DIR__, "src/$lang")
    all_sources = readdir(LANG_DIR)
    filter!(startswith(day_num_str), all_sources)

    input_string = rpad(last(splitpath(input_path)), 10, " ")
    for source in all_sources
        source_string = rpad(source, 20, " ")
        @testset "$(rpad(lang, 7, ' ')) $source_string $input_string" begin
            source_path = joinpath(LANG_DIR, source)
            isfile(source_path) || return
            our_output = run_solution(source_path, input_path, Val(Symbol(lang)))
            for (our, ref) in zip(our_output, reference_output)
                @test our == ref
            end
        end
    end
end

for day_num in 0:25
    day_num_str = lpad(day_num, 2, '0')
    input_path = joinpath(@__DIR__, "inputs", "$(day_num_str)_moelf.txt")
    if day_num > 0 && !isempty(cookie)
        try
            Downloads.download("https://adventofcode.com/2023/day/$day_num/input", input_path; headers)
        catch e
            break
        end
    end
    inputs_solutions = get_all_inputs_solutions(day_num_str)
    isempty(inputs_solutions) && continue

    if ("cpp" ∈ ALL_LANGUAGES)
        cd(@__DIR__) do
            run(`bazel build //...`)
        end
    end

    @testset verbose = true "Day $day_num_str" begin
        for lang in ALL_LANGUAGES, (input_path, reference_output) in inputs_solutions
            isnothing(reference_output) && continue
            test_lang(day_num_str, input_path, reference_output, lang)
        end
    end
end
