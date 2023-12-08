function make_cycle_network(path)
    raw_input = read(path, String)
    instructs, network_string = split(raw_input, "\n\n")

    network = Dict{String,NTuple{2,String}}()
    for line in split(network_string, "\n"; keepempty = false)
        k, L, R = eachmatch(r"[A-Z0-9]{3}", line)
        network[k.match] = (L.match, R.match)
    end

    instructs_cycle = Iterators.Cycle(instructs)
    return instructs_cycle, network
end

function find_steps(instructs_cycle, network, location="AAA"; pred = ==("ZZZ"))
    step = 0
    for i in instructs_cycle
        step += 1
        next = network[location]
        location = i == 'L' ? next[1] : next[2]
        pred(location) && break
    end
    return step
end

function main(path)
    instructs_cycle, network = make_cycle_network(path)
    p1 = find_steps(instructs_cycle, network)
    println(p1)

    locations = filter(endswith("A"), collect(keys(network)))
    factors = find_steps.(Ref(instructs_cycle), Ref(network), locations; pred = endswith("Z"))
    println(lcm(factors...))

end

main(ARGS[1])

