const NBOX = 256

function HASH(str)
    res = 0
    for c in str
        res += Int(c)
        res *= 17
        res %= NBOX
    end
    return res
end

function sum_boxes(boxes)
    res = 0
    for (i, box) in enumerate(boxes), (j, lens) in enumerate(box)
        res += i * j * lens.second
    end
    return res
end

function main(path)
    seq = split(readchomp(path), ",")
    println(sum(HASH, seq))

    BOXES = [Pair{String, Int}[] for _ in 1:NBOX]
    for s in seq
        label, num_str = split(s, r"(=|-)")
        focal = tryparse(Int, num_str)

        box_idx = HASH(label) + 1
        box = BOXES[box_idx]
        lens_idx = findfirst(x -> x.first == label, box)

        if !isnothing(focal)
            lens = Pair(label, focal)
            if isnothing(lens_idx)
                push!(box, lens)
            else
                box[lens_idx] = lens
            end
        elseif !isnothing(lens_idx)
            deleteat!(box, lens_idx)
        end
    end
    println(sum_boxes(BOXES))

end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
