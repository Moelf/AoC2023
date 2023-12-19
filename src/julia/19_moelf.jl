function parse_rule(str)
    left, right... = split(str, ':')
    if !isempty(right)
        cate, op_sym, num... = left
        (op_sym, cate, parse(Int, num), only(right))
    else
        (nothing, nothing, nothing, left)
    end
end

function make_workflow(str)
    wf_name, wf_steps_str, _ = split(str, r"{|}")
    wf_rules = split(wf_steps_str, ",")
    return wf_name => map(parse_rule, wf_rules)
end

function parse_part(str) 
    res = Dict{Char, Int}()
    for (s, _, num...) in eachsplit(str[begin+1:end-1], ",")
        res[s] = parse(Int, num)
    end
    return res
end

function execute(key, part, wf_dict)
    wf = wf_dict[key]
    for rule in wf
        (op_sym, cate, num, res) = rule
        if !isnothing(op_sym)
            cond = op_sym == '<' ? part[cate] < num : part[cate] > num
            !cond && continue
        end

        if res == "A"
            return sum(values(part))
        elseif res == "R"
            return 0
        end
        return execute(res, part, wf_dict)
    end
end

function range_split(op, num, range)
    if isempty(range)
        return range, range
    end
    e1, e2 = range[begin], range[end]
    if op == '<'
        return e1:num-1, num:e2
    else
        return num+1:e2, e1:num
    end
end

function impl2(key, wf_dict, ranges)
    if key == "R"
        return 0
    elseif key == "A"
        return prod(length, values(ranges))
    end

    output = 0
    entry = wf_dict[key]

    for rule in entry
        op_sym, cate, num, res = rule
        if isnothing(op_sym)
            return output + impl2(res, wf_dict, ranges)
        end

        new_ranges = copy(ranges)

        divert, fallthrough = range_split(op_sym, num, ranges[cate])
        ranges[cate] = fallthrough
        new_ranges[cate] = divert

        output += impl2(res, wf_dict, new_ranges)
    end
end

function main(path)
    wf_str, part_str = split.(split(readchomp(path), "\n\n"))
    wf_dict = Dict(make_workflow.(wf_str))
    parts = parse_part.(part_str)

    p1 = sum(execute("in", p, wf_dict) for p in parts)
    println(p1)

    ranges = Dict(x => collect(1:4000) for x in "xmas")
    println(impl2("in", wf_dict, ranges))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
