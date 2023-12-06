#include "io_utils.hpp"

#include <iostream>
#include <vector>
#include <regex>
#include <set>

namespace {
    struct Transform {
        long diff;
        long source;
        long source_end;
    };

    using TransformMap = std::vector<Transform>;

    Transform parseTransform(const std::string& line) {
        const auto first_space = line.find_first_of(' ');
        Transform t;
        t.diff = std::stol(line.substr(0, first_space));
        const auto second_space = line.substr(first_space + 1).find_first_of(' ');
        t.source = std::stol(line.substr(first_space + 1, first_space + second_space + 1));
        t.source_end = t.source + std::stol(line.substr(first_space + second_space + 2));
        t.diff = t.diff - t.source;
        return t;
    }

    std::vector<long> parseInput(const std::string & line) {
        std::regex pattern("( )");

        std::sregex_token_iterator it(line.begin(), line.end(), pattern, -1);
        std::sregex_token_iterator end;

        std::vector<std::string> result(it, end);
        std::vector<long> ret_val;
        std::for_each(result.begin(), result.end(), [&ret_val](const std::string& str){ret_val.push_back(std::stol(str));});
        return ret_val;
    } 

    std::vector<TransformMap> parseTransformMaps(const std::vector<std::string> & lines) {
        std::vector<TransformMap> return_values;

        TransformMap current_map;
        for (size_t idx = 1; idx < lines.size(); ++idx) {
            if (lines.at(idx).empty()) {
                if (!current_map.empty()) {
                    return_values.push_back(current_map);
                    current_map.clear();
                }
            } else if (lines.at(idx).back() == ':') {
                // Do nothing
            } else {
                current_map.push_back(parseTransform(lines.at(idx)));
            }
        }
        return_values.push_back(current_map);
        
        return return_values;
    }

    void applyTransform(const TransformMap & map, long & seed) {
        for (const auto & transform : map) {
            if (seed >= transform.source && seed < transform.source_end) {
                seed += transform.diff;
                return;
            }
        }
    }

    void applyTransformToAllSeeds(const std::vector<TransformMap>& all_transforms, std::vector<long> & num) {
        for (auto & value : num) {
            for (const auto & transform : all_transforms) {
                applyTransform(transform, value);
            }
        }
        return;
    }

    std::vector<std::pair<long, long>> convertInputs(const std::vector<long> & inputs) {
        std::vector<std::pair<long, long>> return_value;
        for (size_t idx = 0; idx < inputs.size(); idx += 2) {
            return_value.emplace_back(inputs.at(idx), inputs.at(idx) + inputs.at(idx + 1));
        }
        return return_value;
    }

    std::vector<std::pair<long, long>> applyTransformToRange(
        const TransformMap& map,
        std::vector<std::pair<long, long>> input_ranges)
    {
        // Needs copying over, and also needs modification
        std::vector<std::pair<long, long>> transformed_seeds;
        for (size_t idx = 0; idx < input_ranges.size(); ++idx)
        {
            bool modified = false;
            for (const auto & transform : map) {
                const auto range = input_ranges.at(idx);
                if (range.first >= transform.source && range.first < transform.source_end) {
                    // If the starting portion is within range
                    if (range.second <= transform.source_end) {
                        // Fully contained
                        transformed_seeds.emplace_back(range.first + transform.diff, range.second + transform.diff);
                        modified = true;
                        break;
                    } else {
                        // Needs to split up
                        transformed_seeds.emplace_back(range.first + transform.diff, transform.source_end + transform.diff);
                        input_ranges.emplace_back(transform.source_end, range.second);
                        modified = true;
                        break;
                    }
                }

                if (range.second <= transform.source_end && range.second > transform.source) {
                    if (range.first < transform.source) {
                        input_ranges.emplace_back(range.first, transform.source);
                        transformed_seeds.emplace_back(transform.source + transform.diff, range.second + transform.diff);
                        modified = true;
                        break;
                    } else {
                        std::cout << "This shouldn't happen" << std::endl;
                    }
                }

                if (range.first < transform.source && range.second > transform.source_end) {
                    transformed_seeds.emplace_back(transform.source + transform.diff, transform.source_end + transform.diff);
                    // std::cout << "Happened 4" << std::endl;
                    input_ranges.emplace_back(range.first, transform.source);
                    input_ranges.emplace_back(transform.source_end, range.second);
                    modified = true;
                    break;
                }
            }

            if (!modified) {
                transformed_seeds.push_back(input_ranges.at(idx));
            }

        }

        return transformed_seeds;
    }

    std::vector<std::pair<long, long>> mergeSeedRanges(const std::vector<std::pair<long, long>> & seeds) {
        // TODO: implement this
        // std::set<long> starts;
        // for (const auto & [start, end] : seeds) {
        //     starts.insert(start);
        // }
        return seeds;
    }
}

int main(int argc, char** argv) {
    std::string filename(argv[1]);
    const auto lines = io_utils::parseInputFile(filename);

    
    std::vector<long> input = parseInput(lines.at(0).substr(7));
    std::vector<long> copy_of_input = input;
    auto part_2_input = convertInputs(copy_of_input);

    const auto result = parseTransformMaps(lines);

    applyTransformToAllSeeds(result, input);
    std::cout << *std::min_element(input.begin(), input.end()) << std::endl;

    // Part 2
    for (const auto & tf : result) {
        part_2_input = applyTransformToRange(tf, part_2_input);
        part_2_input = mergeSeedRanges(part_2_input);
    }

    auto iter = std::min_element(part_2_input.begin(), part_2_input.end(), [](const auto & a, const auto & b) {return a.first < b.first;});
    std::cout << iter->first << std::endl;

}
