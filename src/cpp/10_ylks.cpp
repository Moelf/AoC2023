#include "io_utils.hpp"

#include <algorithm>
#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_set>
#include <unordered_map>
#include <functional>

struct MapInfo {
    char connection;
    int dist;
};

// Thanks ChatGPT
struct PairHash {
    size_t operator()(const std::pair<int, int>& p) const {
        // Hash the pair by combining hashes of its elements
        size_t hashFirst = std::hash<int>{}(p.first);
        size_t hashSecond = std::hash<int>{}(p.second);

        // Combine the hashes using bitwise operations or other techniques
        return hashFirst ^ (hashSecond + 0x9e3779b9 + (hashFirst << 6) + (hashFirst >> 2));
    }
};

using OccupancyRow = std::vector<char>;
using OccupancyMap = std::vector<OccupancyRow>;
using MapRow = std::vector<MapInfo>;
using Map = std::vector<MapRow>;
using Coordinate = std::pair<int, int>;

Map parseInputs(const std::vector<std::string> & inputs, Coordinate & start_location) {
    Map map;
    map.reserve(inputs.size());
    int max_dist = inputs.size() * inputs.front().size();
    for (int row_idx = 0; row_idx < inputs.size(); row_idx++) {
        const auto & input = inputs[row_idx];
        MapRow row; row.reserve(input.size());
        for (int col_idx = 0; col_idx < input.size(); ++col_idx) {
            row.emplace_back(input[col_idx], max_dist);
            if (input[col_idx] == 'S') {
                start_location.first = row_idx;
                start_location.second = col_idx;
            }
        }
        map.push_back(row);
    }
    map[start_location.first][start_location.second].dist = 0;
    return map;
}

// Up is 0, down is 1, left = 2, right = 3
std::unordered_map<char, std::vector<int>> neighbor_lookup = {
    {'|', {0, 1}}, {'-', {2, 3}},
    {'L', {0, 3}}, {'J', {0, 2}},
    {'7', {1, 2}}, {'F', {1, 3}},
    {'.', {}}, {'S', {0, 1, 2, 3}}
};

std::vector<std::unordered_set<char>> acceptable_neighbors = {
    {'|', '7', 'F', 'S'}, {'|', 'L', 'J', 'S'},
    {'-', 'F', 'L', 'S'}, {'-', '7' ,'J', 'S'}
};

std::vector<Coordinate> getNeighbors(const Map & map, const Coordinate & center) {
    std::vector<Coordinate> neighbors;
    const auto value = map[center.first][center.second].connection;
    auto directional_lookups = neighbor_lookup[value];
    for (auto v : directional_lookups) {
        switch (v)
        {
        case 0:
            // Goes up
            if (center.first > 0) {
                if (acceptable_neighbors[v].contains(map[center.first - 1][center.second].connection)) {
                    neighbors.emplace_back(center.first - 1, center.second);
                }
            }
            break;
        case 1:
            // Goes down
            if (center.first < map.size() - 1) {
                if (acceptable_neighbors[v].contains(map[center.first + 1][center.second].connection)) {
                    neighbors.emplace_back(center.first + 1, center.second);
                }
            }
            break;
        case 2:
            // Goes left
            if (center.second > 0) {
                if (acceptable_neighbors[v].contains(map[center.first][center.second - 1].connection)) {
                    neighbors.emplace_back(center.first, center.second - 1);
                }
            }
            break;
        case 3:
            // Goes right
            if (center.second < map.front().size() - 1) {
                if (acceptable_neighbors[v].contains(map[center.first][center.second + 1].connection)) {
                    neighbors.emplace_back(center.first, center.second + 1);
                }
            }
            break;
        default:
            break;
        }
    }

    return neighbors;
}

int getMaxGraphContent(const Map & map) {
    const int max_possible_value = map.size() * map.front().size();
    int max_dist = 0;
    for (const MapRow & row : map) {
        for (const MapInfo & info : row) {
            // For unreachable states
            if (info.dist != max_possible_value && info.dist > max_dist) {
                max_dist = info.dist;
            }
        }
    }
    return max_dist;
}

OccupancyMap mapToOccupancyMap(const Map & map) {
    OccupancyMap new_map(map.size() * 2 + 1, OccupancyRow(map.front().size() * 2 + 1, '.'));
    int max_possible_value = map.size() * map.front().size();
    for (size_t idx = 0; idx < map.size(); ++idx) {
        const auto & row = map.at(idx);
        for (size_t col_idx = 0; col_idx < row.size(); ++col_idx) {
            // For unreachable states
            const auto & info = row.at(col_idx);
            if (info.dist != max_possible_value) {
                new_map[idx * 2 + 1][col_idx * 2 + 1] = 'X';
                const auto neighbors = getNeighbors(map, {idx, col_idx});
                for (const auto & n : neighbors) {
                    new_map.at(idx + n.first + 1).at(col_idx + n.second + 1) = 'X';
                }
            }
        }
    }
    return new_map;
}

std::vector<Coordinate> getOccupancyMapNeighbors(const OccupancyMap& map, const Coordinate& center) {
    std::vector<Coordinate> neighbors;
    if (center.first > 0) {
        if (map.at(center.first - 1).at(center.second) == '.') {
            neighbors.emplace_back(center.first - 1, center.second);
        }
    }

    if (center.first < map.size() - 1) {
        if (map.at(center.first + 1).at(center.second) == '.') {
            neighbors.emplace_back(center.first + 1, center.second);
        }
    }

    if (center.second > 0) {
        if (map.at(center.first).at(center.second - 1) == '.') {
            neighbors.emplace_back(center.first, center.second - 1);
        }
    }

    if (center.second < map.front().size() - 1) {
        if (map.at(center.first).at(center.second + 1) == '.') {
            neighbors.emplace_back(center.first, center.second + 1);
        }
    }

    return neighbors;
}

template<typename Map_T, typename getEdgeFunc_T, typename changeMapFunc_T>
void propagateMap(Map_T& map, const Coordinate & start, getEdgeFunc_T getEdge, changeMapFunc_T changeMap) {
    std::queue<Coordinate> candidates({start});
    // Don't queue duplicate candidates, this happens since this is a densely connected graph
    std::unordered_set<Coordinate, PairHash> queued_candidates = {start};
    std::unordered_set<Coordinate, PairHash> explored = {start};
    while (!candidates.empty()) {
        const Coordinate v = candidates.front();
        explored.insert(v);
        auto neighbors = getEdge(map, v);

        std::for_each(neighbors.begin(), neighbors.end(),
            [&candidates, &explored, &queued_candidates](const auto & coord) {
                if (!explored.contains(coord) && !queued_candidates.contains(coord)) {
                    candidates.push(coord);
                    queued_candidates.insert(coord);
                }
            }
        );

        changeMap(map, v, neighbors);
        candidates.pop();
    }
}

void printOccupancyMap(const OccupancyMap& map) {
    for (const auto & row : map) {
        for (const auto & item : row) {
            std::cout << item;
        }
        std::cout << std::endl;
    }
    return;
}

int getEnclosed(const OccupancyMap& map) {
    int count = 0;
    for (size_t row_idx = 1; row_idx < map.size(); row_idx += 2) {
        for (size_t col_idx = 1; col_idx < map.front().size(); col_idx += 2) {
            if (map.at(row_idx).at(col_idx) == '.') {
                count++;
            }
        }
    }
    return count;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "No input given" << std::endl;
        return 1;
    }
    std::string filename(argv[1]);
    const auto lines = io_utils::parseInputFile(filename);

    // Part 1
    Coordinate start(0, 0);
    Map map = parseInputs(lines, start);
    propagateMap(map, start, getNeighbors,
        [](auto & map, const Coordinate& v, auto & neighbors) {
            auto iter = std::min_element(neighbors.begin(), neighbors.end(), [&map](auto a, auto b){
                return map.at(a.first).at(a.second).dist < map.at(b.first).at(b.second).dist;
            });
            if (iter != neighbors.end()) {
                auto min_dist = map.at(iter->first).at(iter->second).dist;
                if (map.at(v.first).at(v.second).dist > min_dist) {
                    map.at(v.first).at(v.second).dist = min_dist + 1;
                }
            }
        }
    );
    std::cout << getMaxGraphContent(map) << std::endl;

    // Part 2
    auto occupancy_map = mapToOccupancyMap(map);
    propagateMap(occupancy_map, {0, 0}, getOccupancyMapNeighbors,
        [](auto & map, const Coordinate & c, auto) {
            if (map.at(c.first).at(c.second) == '.') {
                map.at(c.first).at(c.second) = 'O';
            }
        }
    );
    std::cout << getEnclosed(occupancy_map) << std::endl;
    return 0;
}
