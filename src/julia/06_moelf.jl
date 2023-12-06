boat_distance(hold, total) = hold * (total - hold)

ways_to_win(total_time, to_beat) = sum(i -> boat_distance(i, total_time) > to_beat, 1:total_time)

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
