#pragma once

#include <fstream>
#include <filesystem>
#include <vector>

namespace io_utils {

namespace fs = std::filesystem;

// Parse input text files into vector of strings separated by line
std::vector<std::string> parseInputFile(const fs::path& path);

} // io_utils