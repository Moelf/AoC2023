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

std::vector<std::string> splitString(const std::string & line, const std::string && delim) {
    std::regex pattern("(" + delim + ")");

    std::sregex_token_iterator it(line.begin(), line.end(), pattern, -1);
    std::sregex_token_iterator end;

    std::vector<std::string> result(it, end);
    std::vector<std::string> ret_val;
    std::for_each(result.begin(), result.end(),[&ret_val](const std::string& str){ret_val.push_back(str);});
    return ret_val;
} 

} // io_utils
