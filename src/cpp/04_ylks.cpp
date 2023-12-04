#include "io_utils.hpp"

#include <cmath>
#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <unordered_set>

namespace {

    std::vector<std::string> splitBySpace(const std::string & str) {
        std::string s;
        std::stringstream ss(str);
 
        std::vector<std::string> ret_val;
 
        while (getline(ss, s, ' ')) {
            if (!s.empty()) {
                ret_val.push_back(s);
            }
        }

        return ret_val;    
    }

    int parseSingleLine(const std::string & line) {
        const std::string card_infos = line.substr(line.find(": ") + 2);

        const auto deliminator_pos = card_infos.find(" | ");
        const std::string winning_numbers = card_infos.substr(0, deliminator_pos);
        const std::string my_numbers = card_infos.substr(deliminator_pos + 3);
        
        const std::vector<std::string> numbers_w_split = splitBySpace(winning_numbers);
        const std::unordered_set<std::string> numbers_w_set(numbers_w_split.begin(), numbers_w_split.end());

        const std::vector<std::string> numbers_m_split = splitBySpace(my_numbers);
        int num_contains = 0;
        for (const auto & m : numbers_m_split) {
            if (numbers_w_set.contains(m)) {
                num_contains++;
            }
        }

        return static_cast<int>(pow(2, num_contains - 1));
    }
    
}


struct IntDefaultOne {
    int value = 1;
};

void printScratchCard(const std::map<int, IntDefaultOne> & map) {
    for (const auto & [k, v] : map) {
        std::cout << "K: " << k << ", v: " << v.value << std::endl;
    }
    std::cout << "--------------" << std::endl;
    return;
}


int main(int argc, char** argv) {
    std::string filename(argv[1]);
    const auto & lines = io_utils::parseInputFile(filename);

    int part1_number = 0;
    std::vector<int> num_wins;
    for (size_t idx = 0; idx < lines.size(); ++idx) {
        int current_wins = parseSingleLine(lines.at(idx));
        part1_number += current_wins;
        num_wins.push_back(current_wins);
    }
    std::cout << part1_number << std::endl;

    // ---- Part 2 : run simulation
    std::map<int, IntDefaultOne> num_scratches;
    int num_cards;
    for (size_t idx = 0; idx < num_wins.size(); ++idx) {
        if (num_wins[idx] != 0) {
            num_cards = static_cast<int>(std::log2(num_wins[idx])) + 1;
        } else {
            num_cards = 0;
        }
        
        for (int second_roll = 1; second_roll < num_cards + 1; ++second_roll) {
            num_scratches[idx + second_roll].value += num_scratches[idx].value;
        }
    }

    int total_nums = std::accumulate(
        num_scratches.begin(),
        num_scratches.end(),
        0.,
        [](int value, std::map<int, IntDefaultOne>::value_type cards)
            {return value + cards.second.value;}
        );
    if (num_scratches.size() < lines.size()) {
        total_nums += static_cast<int>(lines.size() - num_scratches.size());
    }

    std::cout << total_nums << std::endl;

}