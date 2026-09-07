#include "lower_bound_common.hpp"
#include <fstream>
#include <iostream>
#include <iterator>
#include <string>
#include <vector>

using namespace square17lb468292;

int main(int argc, char** argv) {
    const std::string path = argc > 1 ? argv[1] : "square17_lb_4p468292.cert";
    std::ifstream in(path, std::ios::binary);
    if (!in) { std::cerr << "cannot open certificate\n"; return 2; }
    const std::vector<unsigned char> cert((std::istreambuf_iterator<char>(in)), {});

    std::vector<Box> stack;
    stack.reserve(256);
    stack.push_back(initial_box());
    std::size_t cursor = 0;
    Stats s;

    try {
        while (!stack.empty()) {
            if (cursor >= cert.size()) throw std::runtime_error("early EOF");
            const unsigned op = cert[cursor++];
            const Box b = stack.back();
            stack.pop_back();
            ++s.nodes;
            s.max_depth = std::max(s.max_depth, b.depth);

            if (op == 0) {
                if (!box_is_infeasible(b)) throw std::runtime_error("false infeasible leaf");
                ++s.infeasible;
            } else if (op >= 1 && op <= 16) {
                if (!point_covers_box(POINTS[op - 1], b)) throw std::runtime_error("false point leaf");
                ++s.covered;
                ++s.point_counts[op - 1];
            } else if (op >= 17 && op <= 19) {
                const auto [a, c] = split_box(b, static_cast<int>(op - 17));
                stack.push_back(c);
                stack.push_back(a);
                ++s.split;
            } else if (op >= 20 && op < 20 + TRIANGLES.size()) {
                const std::size_t index = op - 20;
                if (!triangle_covers_box(index, b)) throw std::runtime_error("false triangle leaf");
                ++s.triangle;
                ++s.triangle_counts[index];
            } else {
                throw std::runtime_error("unknown opcode");
            }
        }
        if (cursor != cert.size()) throw std::runtime_error("trailing bytes");
        if (s.covered + s.triangle + s.infeasible != s.split + 1) {
            throw std::runtime_error("not a full binary tree");
        }
    } catch (const std::exception& e) {
        std::cerr << "CERTIFICATE_REJECTED at node " << s.nodes << ": " << e.what() << "\n";
        return 1;
    }

    std::cout << "CERTIFICATE_VALID_4P468292\n"
              << "theorem: every unit square in [0,4468292/1000000]^2 contains a witness strictly in its interior\n"
              << "consequence: s(17) > 4468292/1000000 = 4.468292\n"
              << "nodes=" << s.nodes << "\n"
              << "split=" << s.split << "\n"
              << "covered=" << s.covered << "\n"
              << "triangle=" << s.triangle << "\n"
              << "infeasible=" << s.infeasible << "\n"
              << "max_depth=" << s.max_depth << "\n";
    return 0;
}
