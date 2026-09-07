#include "lower_bound_common.hpp"
#include <fstream>
#include <iostream>

using namespace square17lb;

int main(int argc, char** argv) {
    const std::string out_path = argc >= 2 ? argv[1] : "square17_lb_4p456575.cert";
    std::ofstream out(out_path, std::ios::binary);
    if (!out) {
        std::cerr << "cannot open certificate output: " << out_path << "\n";
        return 2;
    }

    std::vector<Box> stack;
    stack.reserve(128);
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
        const int witness = first_covering_point(b);
        if (witness >= 0) {
            out.put(static_cast<char>(1 + witness));
            ++s.covered;
            ++s.witness_count[static_cast<std::size_t>(witness)];
            continue;
        }
        const int dim = choose_split_dimension(b);
        out.put(static_cast<char>(17 + dim));
        ++s.split;
        const auto [a, c] = split_box(b, dim);
        stack.push_back(c);
        stack.push_back(a);
        if ((s.nodes % 250000) == 0) {
            std::cerr << "nodes=" << s.nodes << " stack=" << stack.size()
                      << " depth=" << s.max_depth << "\n";
        }
    }
    out.close();
    if (!out) {
        std::cerr << "error while writing certificate\n";
        return 3;
    }
    std::cout << "CERTIFICATE_GENERATED\n"
              << "L=4456575/1000000\n"
              << "nodes=" << s.nodes << "\n"
              << "split=" << s.split << "\n"
              << "covered=" << s.covered << "\n"
              << "infeasible=" << s.infeasible << "\n"
              << "max_depth=" << s.max_depth << "\n"
              << "certificate=" << out_path << "\n";
    std::cout << "witness_counts=";
    for (std::size_t i = 0; i < s.witness_count.size(); ++i) {
        if (i) std::cout << ',';
        std::cout << s.witness_count[i];
    }
    std::cout << "\n";
    return 0;
}
