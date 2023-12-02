#include "io_utils.hpp"

namespace io_utils {

std::vector<std::string> parseInputFile(const fs::path& path) {
    if (!fs::exists(path)) {
        return {};
    }

    std::ifstream file(path);

    std::vector<std::string> parsed_file;
    std::string line;
    while (std::getline(file, line)) {  
        parsed_file.push_back(line);  
    }

    return parsed_file;
}

} // io_utils