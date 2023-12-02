#include <fstream>
#include <sstream>
#include <iostream>
#include <string_view>
#include <ranges>



int main(int argc,  char **argv) {
  std::ifstream file(argv[1]);

  auto tf = [](auto &&rng) {
    return std::string_view (&*rng.begin(), std::ranges::distance(rng));
  };
  auto get_color = [](auto color, auto color_match, auto& R) {
    auto pos = color.find(color_match);
    if (pos == std::string_view::npos)
      return;
    R = std::max(R, std::stoi(std::string( color.substr(0, color.find(color_match)) )));
  };

  int s1 = 0, s2 = 0;
  int igame = 0;
  std::string line;
  while (std::getline(file, line)) {
    ++igame;
    const auto game = line.substr(line.find(":") + 1, line.size());
    int R = 0, G = 0, B = 0;
    for (const auto rnd : game | std::views::split(';') | std::views::transform(tf)) {
      for (const auto color_str : rnd | std::views::split(',') | std::views::transform(tf)) { 
        get_color(color_str, "red", R);
        get_color(color_str, "green", G);
        get_color(color_str, "blue", B);
      }
    }
    s2 += R*G*B;
    if (R <= 12 && G <= 13 && B <= 14)
      s1 += igame;
  }
  std::cout << s1 << std::endl;
  std::cout << s2 << std::endl;
  return 0;
}
