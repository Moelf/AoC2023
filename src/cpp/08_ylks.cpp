#include "io_utils.hpp"

#include <algorithm>
#include <chrono>
#include <numeric>
#include <ranges>
#include <span>
#include <string>
#include <unordered_map>
#include <vector>

using Network = std::unordered_map<std::string, std::pair<std::string, std::string>>;

namespace {

const std::string traverse(const Network& network, const std::string & current_node, const char movement) {
    const auto iter = network.find(current_node);
    if (iter == network.end()) {
        std::cout << "Couldn't find node" << std::endl;
        return "";
    }

    if (movement == 'R') {
        return iter->second.second;
    } else {
        return iter->second.first;
    }
}

} // namespace

Network parseInput(
    std::vector<std::string>::const_iterator input_begin,
    std::vector<std::string>::const_iterator input_end)
{
    std::unordered_map<std::string, std::pair<std::string, std::string>> return_val;
    for (auto iter = input_begin; iter != input_end; ++iter) {
        const std::vector<std::string> node = io_utils::splitString(*iter, " = \\(|, |\\)");
        return_val[node[0]] = std::pair<std::string, std::string>(node[1], node[2]);
    }
    return return_val;
}

int part1(const Network & network, const std::string& input_sequence) {
    std::string current{"AAA"};
    std::string goal{"ZZZ"};
    // bool reached_goal{false};
    int num_steps = 0;
    while (true) {
        for (const char m : input_sequence) {
            current = traverse(network, current, m);
            num_steps++;
            if (current == goal) {
                return num_steps;
            }
        }
    }
}

long part2(const Network & network, const std::string& input_sequence) {
    auto keys = std::views::keys(network);
    std::vector<std::string> starts;
    std::copy_if(keys.begin(), keys.end(), std::back_inserter(starts), [](const auto key) {return key.back() == 'A';});

    std::vector<long> results;

    for (size_t idx = 0; idx < starts.size(); ++idx) {
        long num_steps = 0;
        auto current = starts.at(idx);
        bool reached = false;
        while (true) {
            for (const char m : input_sequence) {
                current = traverse(network, current, m);
                num_steps++;
                if (current.back() == 'Z') {
                    reached = true;
                    break;
                }
            }
            if (reached) {
                results.push_back(num_steps);
                break;
            }
        }
    }

    for (size_t idx = 0; idx < results.size() - 1; ++idx) {
        results[idx + 1] = std::lcm(results[idx], results[idx + 1]);
    }
    
    return results.back();
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "No input given" << std::endl;
        return 1;
    }
    std::string filename(argv[1]);
    const auto lines = io_utils::parseInputFile(filename);

    const auto network = parseInput(lines.begin() + 2, lines.end());

    std::cout << part1(network, lines[0]) << std::endl;
    std::cout << part2(network, lines[0]) << std::endl;
    
    return 0;
}