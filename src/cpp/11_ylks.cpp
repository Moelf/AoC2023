#include "io_utils.hpp"

#include <algorithm>
#include <vector>
#include <string>
#include <numeric>
#include <set>

using Map = std::vector<std::string>;
using Coord = std::pair<int, int>;
using ExpansionSet = std::pair<std::set<size_t>, std::set<size_t>>;

ExpansionSet convertMap(std::vector<std::string> & lines) {
    ExpansionSet space;
    for (size_t idx = 0; idx < lines.size(); idx++) {
        if (std::all_of(lines.at(idx).begin(), lines.at(idx).end(), [](const auto c){return c == '.';})) {
            space.first.insert(idx);
        }
    }

    for (size_t idx = 0; idx < lines.front().size(); ++idx) {
        bool all_dots = true;
        for (size_t row_idx = 0; row_idx < lines.size(); ++row_idx) {
            all_dots &= lines.at(row_idx).at(idx) == '.';
        }

        if (all_dots) {
            space.second.insert(idx);
        }
    }

    return space;
}

std::vector<Coord> getGalaxies(const Map & map) {
    std::vector<Coord> ret;
    for (int row_idx = 0; row_idx < map.size(); row_idx++) {
        for (int col_idx = 0; col_idx < map.front().size(); col_idx++) {
            if (map[row_idx][col_idx] == '#') {
                ret.emplace_back(row_idx, col_idx);
            }
        }
    }
    return ret;
}

int manhattanDist(const Coord & a, const Coord & b) {
    return std::abs(a.first - b.first) + std::abs(a.second - b.second);
}

int getNumEmptySpaces(int min_val, int max_val, const std::set<size_t> & space) {
    auto lower = space.lower_bound(min_val);
    auto upper = space.upper_bound(max_val);
    return std::distance(lower, upper);
}

long spaceDistance(const Coord& a, const Coord & b, const ExpansionSet & space, const int expansion_factor) {
    int min_x = std::min(a.first, b.first);
    int max_x = std::max(a.first, b.first);
    int min_y = std::min(a.second, b.second);
    int max_y = std::max(a.second, b.second);

    long extra_values = getNumEmptySpaces(min_x, max_x, space.first) * expansion_factor
        + getNumEmptySpaces(min_y, max_y, space.second) * expansion_factor;
    return  extra_values + manhattanDist(a, b);
}

long sumOfShortestPairWise(const std::vector<Coord> & coords, const ExpansionSet & space, const int expansion_factor) {
    long sum = 0;
    for (size_t idx = 0; idx < coords.size(); ++idx) {
        for (size_t idx2 = idx + 1; idx2 < coords.size(); idx2++) {
            sum += spaceDistance(coords.at(idx), coords.at(idx2), space, expansion_factor);
        }
    }
    return sum;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "No input given" << std::endl;
        return 1;
    }
    std::string filename(argv[1]);
    auto lines = io_utils::parseInputFile(filename);

    const auto space = convertMap(lines);
    auto g = getGalaxies(lines);

    std::cout << sumOfShortestPairWise(g, space, 1) << std::endl;
    std::cout << sumOfShortestPairWise(g, space, 1000000 - 1) << std::endl;

    return 0;
}
