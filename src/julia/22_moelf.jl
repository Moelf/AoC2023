const CI = CartesianIndex{3}
const DOWN = CI(0, 0, -1)
to_CI(str) = CI(parse.(Int, split(str, ','))...)

function fall_to(b, bricks)
    while true
        propose_b = b .+ DOWN
        propose_b[begin][3] == 0 && @goto blocked
        for bkg_b in bricks
            if !isempty(intersect(bkg_b, propose_b)) 
                @goto blocked
            end
        end
        b = propose_b
    end
    @label blocked
    return b
end

function free_fall!(bricks)
    for i in eachindex(bricks)
        b = bricks[i]
        bricks[i] = fall_to(b, @view bricks[1:i-1])
    end
end

function impl(bricks)
    sort!(bricks; by=last)
    free_fall!(bricks)

    p1 = p2 = 0
    for i in eachindex(bricks)
        temp_b = popat!(bricks, i)
        dummy = copy(bricks)
        free_fall!(dummy)

        cnt = count(bricks .!= dummy)
        p1 += iszero(cnt)
        p2 += cnt

        insert!(bricks, i, temp_b)
    end
    p1, p2
end

function main(path)
    bricks = map(eachline(path)) do l
        end1, end2 = to_CI.(split(l, '~'))
        brick = end1:end2
        @assert !isempty(brick)
        brick
    end
    println.(impl(bricks))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
