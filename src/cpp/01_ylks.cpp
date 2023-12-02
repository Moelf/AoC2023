// I'll fix bazel build when I have the time

#include "io_utils.hpp"

#include "CLI11.hpp"

#include <filesystem>
#include <cmath>

namespace {

int sumOfCalibrationNumber(const std::vector<std::string>& parsed_file) {
    int sum = 0;
    for (const auto & line : parsed_file) {
        // 12 -> first number 2, second number 1.
        int first_num = -1;
        int last_num = -1;
        for (auto iter = line.rbegin(); iter != line.rend(); ++iter) {
            if (std::isdigit(*iter)) {
                if (first_num == -1) {
                    first_num = (*iter - 48);
                    last_num = first_num;
                } else {
                    last_num = (*iter - 48);
                }
            }
        }
        sum += 10 * last_num + first_num;
    }
    return sum;
}

std::vector<std::string> numbers = {
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
};

const int parseMixedCalibrationLine(const std::string & line) {
    std::vector<int> forward_search_results;
    std::vector<int> reverse_search_results;
    for (const auto & num : numbers) {
        auto location = line.find(num);
        if (location == std::string::npos) {
            location = line.size();
        }
        forward_search_results.push_back(static_cast<int>(location));

        auto r_location = line.rfind(num);
        if (r_location == std::string::npos) {
            reverse_search_results.push_back(-1);
        } else {
            reverse_search_results.push_back(static_cast<int>(r_location));
        }
    }

    // Distance to the start mod 10 is the number
    int first_value = std::distance(forward_search_results.begin(),
        // Find the element that appeared the first
        std::min_element(
            forward_search_results.begin(),
            forward_search_results.end())
        ) % 10;

    int last_value = std::distance(reverse_search_results.begin(),
        std::max_element(
            reverse_search_results.begin(),
            reverse_search_results.end())
        ) % 10;

    return first_value * 10 + last_value;
}

int sumOfAlphanumericCalibrationNumber(const std::vector<std::string> & parsed_file) {
    int sum = 0;
    for (const auto & line : parsed_file) {
        sum += parseMixedCalibrationLine(line);
    }
    return sum;
}

}

int main(int argc, char** argv) {
    // Parse inputs
    CLI::App parser("Run Day 1 of AoC", "01_ylks");
    std::string filename;
    parser.add_option("-i,--input", filename, "Input file");
    CLI11_PARSE(parser, argc, argv);

    const auto parsed_file = io_utils::parseInputFile(std::filesystem::path(filename));

    const int part1_result = sumOfCalibrationNumber(parsed_file);
    const int part2_result = sumOfAlphanumericCalibrationNumber(parsed_file);

    std::cout << part1_result << std::endl;
    std::cout << part2_result << std::endl;

    return 0;
}