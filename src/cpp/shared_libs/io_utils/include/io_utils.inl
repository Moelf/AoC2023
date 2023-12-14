
namespace io_utils{

template<typename T = std::string>
std::vector<T> splitString(const std::string & line, const std::string && delim) {
    std::regex pattern(delim);

    std::sregex_token_iterator it(line.begin(), line.end(), pattern, -1);
    std::sregex_token_iterator end;

    std::vector<std::string> result(it, end);
    std::vector<T> ret_val;
    std::for_each(result.begin(), result.end(),[&ret_val](const std::string& str){ret_val.push_back(stringToNumber<T>(str));});
    return ret_val;
} 

template <typename T = std::string>
T stringToNumber(const std::string & arg)
{
    if constexpr (std::is_same_v<T, int>) {
        return std::stoi(arg);
    } else if constexpr (std::is_same_v<T, long>) {
        return std::stol(arg);
    } else if constexpr (std::is_same_v<T, std::string>){
        return arg;
    } else {
        return T();
    }
}

}
