#include "io_utils.hpp"

#include <cmath>
#include <numeric>
#include <iostream>
#include <vector>
#include <map>
#include <set>

namespace {

    // Thanks ChatGPT
    struct IntPairCompare {
        bool operator()(const std::pair<int, int>& lhs, const std::pair<int, int>& rhs) const {
            if (lhs.first != rhs.first) {
                return lhs.first < rhs.first;
            }
            return lhs.second < rhs.second;
        }
    };

    using GearInfo = std::vector<int>;

    int countRelevantNumbers(
        const std::vector<std::string>& matrix,
        const size_t line_idx,
        std::map<std::pair<int, int>, GearInfo, IntPairCompare> & map_information)
    {
        std::vector<int> vertical_search;
        if (line_idx != 0) {
            vertical_search.push_back(line_idx - 1);
        }
        if (line_idx < matrix.size() - 1) {
            vertical_search.push_back(line_idx + 1);
        }

        std::vector<int> vertical_search_end_points = vertical_search;
        vertical_search_end_points.push_back(line_idx);

        const auto & line = matrix.at(line_idx);
        int sum_of_marked_numbers = 0;

        int number_sequence = 0;
        bool is_number_marked = false;
        int current_number = 0;

        std::set<std::pair<int, int>, IntPairCompare> number_to_gear_association;

        for (int idx = line.size() - 1; idx > -1; --idx) {
            if (std::isdigit(line.at(idx))) {
                // Got a number

                // Each of those blocks are checking
                // 1. if it's safe to check a position for symbols, and
                // 2. associate them with the current number, which will eventually add the current number to the
                //     bookkeeping @c map_information
                if (number_sequence == 0 && idx != static_cast<int>(line.size() - 1)) {
                    for (const auto vertical_idx : vertical_search_end_points) {
                        char symbol = matrix.at(vertical_idx).at(idx + 1);

                        bool is_gear_symbol = (!std::isdigit(symbol)) && (symbol != '.');
                        is_number_marked |= is_gear_symbol;

                        if (is_gear_symbol) {
                            number_to_gear_association.emplace(std::pair<int, int>{vertical_idx, idx + 1});
                        }
                    }
                }

                if (idx != 0) {
                    for (const auto vertical_idx : vertical_search_end_points) {
                        char symbol = matrix.at(vertical_idx).at(idx - 1);
                        bool is_gear_symbol = (!std::isdigit(symbol)) && (symbol != '.');
                        is_number_marked |= is_gear_symbol;

                        if (is_gear_symbol) {
                            number_to_gear_association.emplace(std::pair<int, int>{vertical_idx, idx - 1});
                        }
                    }
                }

                for (const auto vertical_idx : vertical_search) {
                    char symbol = matrix.at(vertical_idx).at(idx);
                    bool is_gear_symbol = (!std::isdigit(symbol)) && (symbol != '.');
                    is_number_marked |= is_gear_symbol;

                    if (is_gear_symbol) {
                        number_to_gear_association.emplace(std::pair<int, int>{vertical_idx, idx});
                    }
                }

                // Record the number
                current_number += std::pow(10, number_sequence++) * (line[idx] - 48);
                
            } else if (number_sequence != 0) {
                if (is_number_marked) {
                    sum_of_marked_numbers += current_number;

                    for (const auto & gear_location : number_to_gear_association) {
                        map_information[gear_location].push_back(current_number);
                    }
                }

                // Reset state
                is_number_marked = false;
                number_sequence = 0;
                current_number = 0;
                number_to_gear_association.clear();
            }
        }

        if (number_sequence != 0 && is_number_marked) {
            sum_of_marked_numbers += current_number;

            for (const auto & gear_location : number_to_gear_association) {
                map_information[gear_location].push_back(current_number);
            }
        } 

        return sum_of_marked_numbers;
    }
}

int main(int argc, char** argv) {
    std::string filename(argv[1]);
    const auto & parsed_file = io_utils::parseInputFile(filename);

    std::map<std::pair<int, int>, GearInfo, IntPairCompare> gear_status;
    int part1_result = 0;
    for (size_t idx = 0; idx < parsed_file.size(); idx++) {
        part1_result += countRelevantNumbers(parsed_file, idx, gear_status);
    }
    std::cout << part1_result << std::endl;

    int part2_result = 0;
    for (const auto &[k, v] : gear_status) {
        if (v.size() == 2) {
            part2_result += v[0] * v[1];
        }
    }
    std::cout << part2_result << std::endl;;

    return 0;
}