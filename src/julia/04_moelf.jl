function winning_numbers(line)
    _, left, right = split(line, r":|\|")
    return split(left) ∩ split(right)
end

prize(n) = iszero(n) ? 0 : 2^(n - 1)

function scratch_all_count(cards)
    N_cards = ones(Int, length(cards))
    for (i, N_copies) in enumerate(N_cards)
        score = cards[i]
        for j = (i + 1):(i + score)
            isassigned(N_cards, j) || continue
            N_cards[j] += N_copies
        end
    end
    return N_cards
end

function main(path)
    lines = readlines(path)
    cards = length.(winning_numbers.(lines))
    println(sum(prize, cards))
    println(sum(scratch_all_count(cards)))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
