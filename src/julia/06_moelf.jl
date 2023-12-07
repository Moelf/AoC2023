"""
h*t - h^2 = B
h^2 - h*t + B = 0
h = (t ± sqrt(t^2 - 4B)) / 2
you need to round up the smaller root and round down the larger root
and compute the number of integers between them and +1
"""
function ways_to_win(total_time, to_beat)
    discri = total_time^2 - 4to_beat
    discri < 0 && return 0
    sq = sqrt(discri)
    small_root = (total_time - sq) / 2
    small_root = isinteger(small_root) ? Int(small_root)+1 : ceil(Int, small_root)
    larger_root = (total_time + sq) / 2
    larger_root = isinteger(larger_root) ? Int(larger_root)-1 : floor(Int, larger_root)
    return larger_root - small_root + 1
end

function main(path)
    time_str, dist_str = readlines(path)
    time_digits = split(time_str)[2:end]
    dist_digits = split(dist_str)[2:end]

    total_times = parse.(Int, time_digits)
    to_beat = parse.(Int, dist_digits)
    println(prod(ways_to_win.(total_times, to_beat)))

    big_time = parse(Int, join(time_digits))
    big_to_beat = parse(Int, join(dist_digits))
    println(ways_to_win(big_time, big_to_beat))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
