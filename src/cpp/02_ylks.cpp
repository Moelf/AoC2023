
#include "io_utils.hpp"

#include <iostream>
#include <numeric>
#include <unordered_map>
#include <regex>

namespace {

std::unordered_map<std::string, int> constraint_set {
    {"red", 12},
    {"green", 13},
    {"blue", 14}
};

struct Solution {
    int part_1 = 0;
    int part_2 = 0;
};

bool checkGameCompliance(const std::string & game_info, int & part_2_soln) {
    const auto start = game_info.find(": ");
    const auto & rounds = game_info.substr(start + 2);

    /// Thanks ChatGPT
    // Regular expression pattern to match ", " or "; " as delimiters
    std::regex pattern("(, |; )");

    // Using std::sregex_token_iterator to split the string based on the regex pattern
    std::sregex_token_iterator it(rounds.begin(), rounds.end(), pattern, -1);
    std::sregex_token_iterator end;

    // Store the parsed parts into a vector of strings
    std::vector<std::string> result(it, end);

    bool compliance = true;
    std::unordered_map<std::string, int> min_cubes;
    for (const auto & balls : result) {
        const auto deliminator_pos = balls.find(" ");

        int number_of_balls = std::stoi(balls.substr(0, deliminator_pos));
        const std::string& ball_color = balls.substr(deliminator_pos + 1);

        // Part 1
        if (constraint_set[ball_color] < number_of_balls) {
            compliance = false;
        }

        // Part 2
        if (!min_cubes[ball_color]) {
            min_cubes[ball_color] = number_of_balls;
        } else {
            min_cubes[ball_color] = std::max(min_cubes[ball_color], number_of_balls);
        }
         
    }

    part_2_soln = 1;
    for (const auto [k, v] : min_cubes) {
        part_2_soln *= v;
    }

    return compliance;
}

Solution partOne(const std::vector<std::string> & rounds) {
    int part_1 = 0;
    int part_2 = 0;
    for (size_t idx = 0; idx < rounds.size(); ++idx) {
        int min_round_num = 0;
        if (checkGameCompliance(rounds[idx], min_round_num)) {
            part_1 += static_cast<int>(idx) + 1;
        }
        part_2 += min_round_num;
    }

    return {part_1, part_2};
}

}

int main(int argc, char** argv) {
    // Parse inputs
    std::string filename(argv[1]);
    const auto parsed_file = io_utils::parseInputFile(std::filesystem::path(filename));

    const auto result = partOne(parsed_file);
    std::cout << result.part_1 << std::endl;
    std::cout << result.part_2 << std::endl;

    return 0;
}