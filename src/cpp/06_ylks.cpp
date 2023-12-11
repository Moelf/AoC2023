#include "io_utils.hpp"

#include <cmath>
#include <iostream>
#include <vector>
#include <algorithm>

template<typename T>
bool isInteger(T var) {
    if (std::abs(var - static_cast<int>(var)) < 1e-6) {
        return true;
    } 

    return false;
}

std::vector<std::pair<int, int>> convertInputs(const std::vector<std::string> & input_lines) {
    auto parse_line = [](const std::string & line) {
        const std::vector<std::string> split_result = io_utils::splitString(line, std::string(" "));
        std::vector<int> result;
        std::for_each(split_result.begin(), split_result.end(),
            [&result](const auto & v) {
                if (!v.empty()) {
                    result.push_back(io_utils::stringToNumber<int>(v));
                }
            });
        return result;
    };

    auto time = parse_line(input_lines.at(0).substr(11));
    auto target_distance = parse_line(input_lines.at(1).substr(11));

    std::vector<std::pair<int, int>> parsed_inputs;
    parsed_inputs.reserve(time.size());
    for (size_t idx = 0; idx < time.size(); idx++) {
        parsed_inputs.emplace_back(time.at(idx), target_distance.at(idx));
    }

    return parsed_inputs;
}

std::pair<double, double> convertInputsPart2(const std::vector<std::string> & input_lines) {
    auto stripSpaces = [](const std::string& input) {
        std::string str(input);
        std::string::iterator end_pos = std::remove(str.begin(), str.end(), ' ');
        str.erase(end_pos, str.end());
        return str;
    };

    return std::make_pair<double, double>(
        std::stod(stripSpaces(input_lines.at(0).substr(11))),
        std::stod(stripSpaces(input_lines.at(1).substr(11)))
    );
}

int num_ways(const double num_seconds, const double target_distance) {
    double lower_bound = (num_seconds - sqrt(pow(num_seconds, 2) - 4 * target_distance)) / 2;
    double upper_bound = (num_seconds + sqrt(pow(num_seconds, 2) - 4 * target_distance)) / 2;

    if (isInteger(lower_bound)) {
        lower_bound++;
    } else {
        lower_bound = std::ceil(lower_bound);
    }

    if (isInteger(upper_bound)) {
        upper_bound--;
    } else {
        upper_bound = std::floor(upper_bound);
    }

    return upper_bound - lower_bound + 1;
}

int main(int argc, char** argv) {
    std::string filename(argv[1]);

    const auto parsed_inputs = io_utils::parseInputFile(filename);
    const auto my_input = convertInputs(parsed_inputs);

    int final_output = 1;
    for (const auto & [a, b] : my_input) {
        final_output *= num_ways(a, b);
    }

    std::cout << final_output << std::endl;

    const auto part2 = convertInputsPart2(parsed_inputs);

    std::cout << num_ways(part2.first, part2.second) << std::endl;


    return 0;
}