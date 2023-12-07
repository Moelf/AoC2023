const CARDS_DICT = Dict(['2':'9'; "TJQKA"...] .=> 1:13)
const CARDS_DICT_JOKER = copy(CARDS_DICT)
CARDS_DICT_JOKER['J'] = 0

struct Hand
    counts::Vector{Int}
    cards::Vector{Int}
    bid::Int
end

function card_counts(cards; joker=false) 
    _cards = joker ? filter(!iszero, cards) : cards
    counts = sort!([count(==(c), _cards) for c in unique(_cards)]; rev=true)

    if joker
        nJ = count(==(0), cards)
        if nJ == 5
            return [5]
        end
        counts[begin] += nJ
    end
    return counts
end

Base.isless(h1::Hand, h2::Hand) = h1.counts == h2.counts ? h1.cards < h2.cards : h1.counts < h2.counts

function total(hands)
    shs = sort(hands)
    sum(shs[i].bid * i for i in eachindex(shs))
end

function main(path)
    lines = split.(readlines(path))
    hand_strs, bids = first.(lines), parse.(Int, last.(lines))
    hands = map(hand_strs, bids) do hand_str, b
        cards = [CARDS_DICT[c] for c in hand_str]
        counts = card_counts(cards)
        Hand(counts, cards, b)
    end
    println(total(hands))

    hands2 = map(hand_strs, bids) do hand_str, b
        cards = [CARDS_DICT_JOKER[c] for c in hand_str]
        counts = card_counts(cards; joker=true)
        Hand(counts, cards, b)
    end
    println(total(hands2))
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
