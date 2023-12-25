function make_graph(path)
    V = Set{String}()
    E = Set{Tuple{String,String}}()
    for l in eachline(path)
        nodes = split(replace(l, ": " => " "))
        union!(V, nodes)

        v, us... = nodes
        for u in us
            push!(E, (v, u))
            push!(E, (v, u))
        end
    end
    return V, E
end

ff(n, V) = findfirst(∋(n), V)

function impl1(_V, E)
    while true
        V = [[v] for v in _V]
        while length(V) > 2
            u, v = rand(E)
            ui = ff(u, V)
            vi = ff(v, V)
            if ui != vi
                union!(V[ui], V[vi])
                deleteat!(V, vi)
            end
        end
        if count(ff(u, V) != ff(v, V) for (u, v) in E) < 4
            return prod(length, V)
        end
    end
end

function main(path)
    V, E = make_graph(path)
    println(impl1(V, E))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
