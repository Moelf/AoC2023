const CACHE = Dict()

function rec_count(str, intvec)
    get!(CACHE, (str, intvec)) do
        if isempty(intvec)
            # no group left, illegal to have any '#'
            all(!=('#'), str)
        elseif sum(intvec) > length(str)
            # not enough chars left to form all groups
            0
        elseif first(str) == '.'
            rec_count(str[2:end], intvec)
        else
            count = 0
            if first(str) == '?'
                count += rec_count(str[2:end], intvec)
            end
            N = first(intvec)
            # first N is mix of "#?"
            # followed by a '.'
            stub = get(str, N + 1, '.')
            if all(!=('.'), first(str, N)) && stub != '#'
                count += rec_count(str[N+2:end], intvec[2:end])
            end
            count
        end
    end
end

function impl(pairs, N)
    sum(pairs) do (str, intvec)
        str, intvec = join(fill(str, N), '?'), repeat(intvec, N)
        rec_count(str, intvec)
    end
end

function main(path)
    lines = map(eachline(path)) do l
        str, int_str = split(l)
        intvec = parse.(Int, split(int_str, ","))
        (str, intvec)
    end
    println(impl(lines, 1))
    println(impl(lines, 5))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
