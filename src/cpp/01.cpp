#include <iostream>
#include <fstream>

auto strtonum_part1(std::string str)
{
    auto result = 0;
    auto num_first = -1;
    auto num_last = -1;
    for (int i = 0; i < str.length(); i++)
    {
        if (std::isdigit(str[i]))
        {
            if (num_first == -1)
            {
                num_first = str[i] - '0';
            }
            num_last = str[i] - '0';
        }
    }
    result += num_first * 10 + num_last;
    return result;
}

auto substrtonum(std::string str)
{
    if (str.starts_with("one"))
        return 1;
    else if (str.starts_with("two"))
        return 2;
    else if (str.starts_with("three"))
        return 3;
    else if (str.starts_with("four"))
        return 4;
    else if (str.starts_with("five"))
        return 5;
    else if (str.starts_with("six"))
        return 6;
    else if (str.starts_with("seven"))
        return 7;
    else if (str.starts_with("eight"))
        return 8;
    else if (str.starts_with("nine"))
        return 9;
    else
        return -1;
}

auto strtonum_part2(std::string str)
{
    auto result = 0;
    auto num_first = -1;
    auto num_last = -1;
    for (int i = 0; i < str.length(); i++)
    {
        auto num = -1;
        if (std::isdigit(str[i]))
            num = str[i] - '0';
        else
        {
            num = substrtonum(str.substr(i));
            if (num == -1)
                continue;
        }

        if (num_first == -1)
        {
            num_first = num;
        }
        num_last = num;
    }
    result += num_first * 10 + num_last;
    return result;
}

int main()
{
    std::ifstream file("inputs/01_bauerc.txt");
    std::string str;
    auto result_part1 = 0;
    auto result_part2 = 0;
    while (std::getline(file, str))
    {
        // std::cout << str << std::endl;
        result_part1 += strtonum_part1(str);
        result_part2 += strtonum_part2(str);
    }
    std::cout << "Answer: " << result_part1 << std::endl;
    std::cout << "Answer: " << result_part2 << std::endl;
    return 0;
}
