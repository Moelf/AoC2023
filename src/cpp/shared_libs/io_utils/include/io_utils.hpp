#pragma once

#include <fstream>
#include <filesystem>
#include <vector>
#include <regex>
#include <type_traits>
#include <iostream>

namespace io_utils {

namespace fs = std::filesystem;

// Parse input text files into vector of strings separated by line
std::vector<std::string> parseInputFile(const fs::path& path);

template <typename T = std::string>
T stringToNumber(const std::string & arg)
{
    if (std::is_same_v<T, int>) {
        return std::stoi(arg);
    } else if (std::is_same_v<T, long>) {
        return std::stol(arg);
    } else {
        return T();
    }
}

std::vector<std::string> splitString(const std::string & line, const std::string && delim);

} // io_utils
