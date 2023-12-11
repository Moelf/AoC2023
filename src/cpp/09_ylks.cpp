#include "io_utils.hpp"

#include <algorithm>
#include <vector>
#include <string>
#include <numeric>

std::vector<std::vector<int>> parseInputs(const std::vector<std::string> & inputs) {
    std::vector<std::vector<int>> result;
    result.reserve(inputs.size());

    for (const auto & line : inputs) {
        result.push_back(io_utils::splitString<int>(line, " "));
    }

    return result;
}

int soln(const std::vector<int>& inputs, bool is_part_1 = true) {
    std::vector<std::vector<int>> diff = {inputs};
    while (diff.back().back() != 0) {
        std::vector<int> new_diff;
        std::adjacent_difference(diff.back().begin(), diff.back().end(), std::back_inserter(new_diff));
        diff.push_back(new_diff);
    }

    if (is_part_1) {
        return std::accumulate(diff.begin(), diff.end(), 0, [](int base, const auto & v) {return base + v.back();});
    } else {
        std::fill(diff.back().begin(), diff.back().end(), 0);
        for (int idx = diff.size() - 2; idx > 0; --idx) {
            diff.at(idx).at(idx - 1) = diff.at(idx).at(idx) - diff.at(idx + 1).at(idx);
        }
        return diff.front().front() - diff.at(1).front();
    }
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "No input given" << std::endl;
        return 1;
    }
    std::string filename(argv[1]);
    const auto lines = io_utils::parseInputFile(filename);

    auto result = parseInputs(lines);
    std::cout << std::accumulate(result.begin(), result.end(), 0,
        [](int base, const auto & v) {return base + soln(v);}) << std::endl; // totally readable
    std::cout << std::accumulate(result.begin(), result.end(), 0,
        [](int base, const auto & v) {return base + soln(v, false);}) << std::endl; // totally readable

    return 0;
}