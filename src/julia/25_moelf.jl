using Graphs

function make_graph(path)
    G = Graph()
    V = String[]
    ls = readlines(path)
    for l in ls
        nodes = split(replace(l, ": " => " "))
        append!(V, nodes)
    end
    unique!(V)
    add_vertices!(G, length(V))
    V_d = Dict(V .=> eachindex(V))
    for l in ls
        v, us... = split(replace(l, ": " => " "))
        for u in us
            add_edge!(G, V_d[v], V_d[u])
        end
    end
    return G
end

function main(path)
    G = make_graph(path)
    NV = nv(G)
    while true
        cut = karger_min_cut(G)
        if length(karger_cut_edges(G, cut)) == 3
            x = count(==(1), cut)
            y = NV - x
            println(x*y)
            break
        end
    end
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])

# function make_graph(path)
#     V = Set{String}()
#     E = Set{Tuple{String,String}}()
#     for l in eachline(path)
#         nodes = split(replace(l, ": " => " "))
#         union!(V, nodes)

#         v, us... = nodes
#         for u in us
#             push!(E, (v, u))
#             push!(E, (v, u))
#         end
#     end
#     return V, E
# end

# ff(n, V) = findfirst(∋(n), V)

# function impl1(_V, E)
#     while true
#         V = [[v] for v in _V]
#         while length(V) > 2
#             u, v = rand(E)
#             ui = ff(u, V)
#             vi = ff(v, V)
#             if ui != vi
#                 union!(V[ui], V[vi])
#                 deleteat!(V, vi)
#             end
#         end
#         if count(ff(u, V) != ff(v, V) for (u, v) in E) < 4
#             return prod(length, V)
#         end
#     end
# end

