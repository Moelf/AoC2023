module AoC2023

const DAY_MODULES = Dict{String, Module}()
function __init__()
    files = readdir(joinpath(@__DIR__, "julia"); join=true)
    for path in files
        m = get!(DAY_MODULES, path, Module())
        Base.include(m, path)
    end
end

end
