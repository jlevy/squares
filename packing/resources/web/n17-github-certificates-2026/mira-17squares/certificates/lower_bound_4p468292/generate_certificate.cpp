#include "lower_bound_common.hpp"
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace square17lb468292;

int main(int argc, char** argv) {
    const std::string path = argc > 1 ? argv[1] : "square17_lb_4p468292.cert";
    std::ofstream out(path, std::ios::binary);
    if (!out) { std::cerr << "cannot open output\n"; return 2; }

    std::vector<Box> stack;
    stack.reserve(256);
    stack.push_back(initial_box());
    Stats s;

    while (!stack.empty()) {
        const Box b = stack.back();
        stack.pop_back();
        ++s.nodes;
        s.max_depth = std::max(s.max_depth, b.depth);

        if (box_is_infeasible(b)) {
            out.put(static_cast<char>(0));
            ++s.infeasible;
            continue;
        }
        const int point = first_covering_point(b);
        if (point >= 0) {
            out.put(static_cast<char>(1 + point));
            ++s.covered;
            ++s.point_counts[static_cast<std::size_t>(point)];
            continue;
        }
        const int triangle = first_covering_triangle(b);
        if (triangle >= 0) {
            out.put(static_cast<char>(20 + triangle));
            ++s.triangle;
            ++s.triangle_counts[static_cast<std::size_t>(triangle)];
            continue;
        }

        const int dim = choose_split_dimension(b);
        out.put(static_cast<char>(17 + dim));
        ++s.split;
        const auto [a, c] = split_box(b, dim);
        stack.push_back(c);
        stack.push_back(a);
    }
    out.close();
    if (!out) { std::cerr << "write failure\n"; return 3; }

    std::cout << "CERTIFICATE_GENERATED_4P468292\n"
              << "L=4468292/1000000\n"
              << "nodes=" << s.nodes << "\n"
              << "split=" << s.split << "\n"
              << "covered=" << s.covered << "\n"
              << "triangle=" << s.triangle << "\n"
              << "infeasible=" << s.infeasible << "\n"
              << "max_depth=" << s.max_depth << "\n"
              << "certificate=" << path << "\n";
    return 0;
}
