#include "io_utils.hpp"

#include <algorithm>
#include <string>
#include <vector>
#include <map>

char mapCards(char a) {
    if (a == 'T') {
        a = 58;
    } else if (a == 'J') {
        a = 59;
    } else if (a == 'Q') {
        a = 60;
    } else if (a == 'K') {
        a = 61;
    }
    return a;
}

char mapCardsPart2(char a) {
    if (a == 'T') {
        a = 58;
    } else if (a == 'J') {
        a = 47;
    } else if (a == 'Q') {
        a = 60;
    } else if (a == 'K') {
        a = 61;
    }
    return a;
}

struct Hand {
    std::string cards;
    int bid;

    bool operator<(const Hand & other) const {
        for (size_t idx = 0; idx < 5; ++idx) {
            if (cards[idx] != other.cards[idx]) {
                return mapCards(cards[idx]) < mapCards(other.cards[idx]);
            }
        }
        return true;
    }
};

std::vector<Hand> convertInputs(const std::vector<std::string> & lines) {
    std::vector<Hand> game;
    for (const auto & line : lines) {
        int bid = io_utils::stringToNumber<int>(line.substr(line.find(" ")));
        game.emplace_back(line.substr(0, 5), bid);
    }

    return game;
}

// Yeah sure, yell at me ; )
// fives 
// fours
// houses
// threes
// twice // 2 pairs
// once // 1 pairs
// pesants

size_t deckDetermination(const std::vector<int> & values) {
    size_t deck_index;
    if (values.back() == 5) {
        // fives.push_back(hand);
        deck_index = 6;
    } else if (values.back() == 4) {
        // fours.push_back(hand);
        deck_index = 5;
    } else if (values.back() == 3) {
        if (values.rbegin()[1] == 2) {
            deck_index = 4;
        } else {
            deck_index = 3;
        }
    } else if (values.back() == 2) {
        if (values.rbegin()[1] == 2) {
            deck_index = 2;
        } else {
            deck_index = 1;
        }
    } else {
        deck_index = 0;
    }
    return deck_index;
}

std::vector<std::vector<Hand>> distributeHands(const std::vector<Hand> & game, bool part2 = false) {
    std::vector<std::vector<Hand>> sorted_deck(7);
    for (const auto & hand : game) {
        std::map<char, int> count;
        count.clear();
        for (const char c : hand.cards) {
            count[c] = count[c] + 1;
        }

        if (part2) {
            if (count.count('J') != 0) {
                auto iter = std::max_element(count.begin(), count.end(), [](const auto & p1, const auto & p2){
                    // J shall never be the biggest number

                    if (p1.first == 'J') {
                        return true;
                    }

                    if (p2.first == 'J') {
                        return false;
                    }

                    return p1.second < p2.second;
                });

                if (iter->first != 'J') {
                    iter->second += count['J'];
                }

                if (count.size() != 1) {
                    count.erase('J');
                }
            }
        }

        std::vector<int> values;
        std::for_each(count.begin(), count.end(), [&values](const auto & m) {return values.push_back(m.second);});
        if (part2) {
            std::sort(values.begin(), values.end(), [](const auto & a, const auto & b) {return mapCardsPart2(a) < mapCardsPart2(b);});
        } else {
            std::sort(values.begin(), values.end());
        }

        size_t deck_index = deckDetermination(values);

        // std::cout << hand.cards << ", " << deck_index << std::endl;

        sorted_deck.at(deck_index).push_back(hand);

        // std::cout << "end" << std::endl;
    }
    return sorted_deck;
}

std::vector<Hand> sort_each_deck_and_merge(std::vector<std::vector<Hand>> & deck, bool part2 = false) {
    for (auto & hands : deck) {
        if (part2) {
            std::sort(hands.begin(), hands.end(), [](const auto & a, const auto & b) {
                for (size_t idx = 0; idx < 5; ++idx) {
                    if (a.cards[idx] != b.cards[idx]) {
                        return mapCardsPart2(a.cards[idx]) < mapCardsPart2(b.cards[idx]);
                    }
                }
                return true;
                }
            );
        } else {
            std::sort(hands.begin(), hands.end());
        }
    }

    std::vector<Hand> final_deck;
    std::for_each(deck.begin(), deck.end(),
        [&final_deck](const std::vector<Hand> & hands) {
            std::copy(hands.begin(), hands.end(), std::back_inserter(final_deck));
        }
    );

    return final_deck;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "No input given" << std::endl;
        return 1;
    }
    std::string filename(argv[1]);

    const auto lines = io_utils::parseInputFile(filename);
    auto game = convertInputs(lines);

    auto sorted_deck = distributeHands(game);

    const auto final_deck = sort_each_deck_and_merge(sorted_deck);
    int final_score = 0;
    for (size_t idx = 0; idx < final_deck.size(); idx++) {
        final_score += final_deck.at(idx).bid * (idx + 1);
    }
    std::cout << final_score << std::endl;

    auto sorted_deck_p2 = distributeHands(game, true);
    const auto final_deck_p2 = sort_each_deck_and_merge(sorted_deck_p2, true);

    for (size_t idx = 0; idx < 20; idx++) {
        std::cout << final_deck_p2.at(idx).cards << std::endl;
    }

    int final_score_p2 = 0;
    for (size_t idx = 0; idx < final_deck.size(); idx++) {
        final_score_p2 += final_deck_p2.at(idx).bid * (idx + 1);
    }
    std::cout << final_score_p2 << std::endl;

    return 0;
}