#include "lower_bound_common.hpp"
#include <fstream>
#include <iostream>

using namespace square17lb;

[[noreturn]] static void fail(const std::string& message, std::uint64_t node) {
    std::cerr << "CERTIFICATE_INVALID at node " << node << ": " << message << "\n";
    std::exit(1);
}

int main(int argc, char** argv) {
    const std::string path = argc >= 2 ? argv[1] : "square17_lb_4p456575.cert";
    std::ifstream in(path, std::ios::binary);
    if (!in) {
        std::cerr << "cannot open certificate: " << path << "\n";
        return 2;
    }

    std::vector<Box> stack;
    stack.reserve(128);
    stack.push_back(initial_box());
    Stats s;
    while (!stack.empty()) {
        const Box b = stack.back();
        stack.pop_back();
        const int raw = in.get();
        if (raw == EOF) fail("unexpected end of file", s.nodes + 1);
        const unsigned code = static_cast<unsigned char>(raw);
        ++s.nodes;
        s.max_depth = std::max(s.max_depth, b.depth);
        if (code == 0) {
            if (!box_is_infeasible(b)) fail("false infeasibility leaf", s.nodes);
            ++s.infeasible;
        } else if (code >= 1 && code <= 16) {
            const std::size_t witness = code - 1;
            if (!point_covers_box(POINTS[witness], b)) fail("false point witness", s.nodes);
            ++s.covered;
            ++s.witness_count[witness];
        } else if (code >= 17 && code <= 19) {
            const int dim = static_cast<int>(code - 17);
            const auto [a, c] = split_box(b, dim);
            ++s.split;
            stack.push_back(c);
            stack.push_back(a);
        } else {
            fail("unknown opcode", s.nodes);
        }
    }
    if (in.get() != EOF) fail("trailing bytes", s.nodes + 1);
    if (s.nodes != s.covered + s.infeasible + s.split) fail("internal node accounting", s.nodes);
    if (s.split + 1 != s.covered + s.infeasible) fail("tree is not full binary", s.nodes);
    std::cout << "CERTIFICATE_VALID\n"
              << "theorem: every unit square contained in [0,4456575/1000000]^2 contains"
                 " one of the 16 listed rational points strictly in its interior\n"
              << "packing consequence: no 17-square packing exists at this side length\n"
              << "nodes=" << s.nodes << "\n"
              << "split=" << s.split << "\n"
              << "covered=" << s.covered << "\n"
              << "infeasible=" << s.infeasible << "\n"
              << "max_depth=" << s.max_depth << "\n";
    std::cout << "witness_counts=";
    for (std::size_t i = 0; i < s.witness_count.size(); ++i) {
        if (i) std::cout << ',';
        std::cout << s.witness_count[i];
    }
    std::cout << "\n";
    return 0;
}
