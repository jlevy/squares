// Readers for the sqpk v1 packing format (data/README.md) and the sqcert v1 certificate format.
// Every number stays a string; callers convert at the precision they need.
#pragma once

#include <array>
#include <string>
#include <vector>

namespace sqv {

struct Packing {
  std::string path;
  int n = 0;
  std::string s;                                   // claimed side, decimal literal
  std::vector<std::array<std::string, 3>> squares;  // cx, cy, theta_deg
  int digits = -1;                                 // from '# digits D', -1 if absent
  std::string exact_s;                             // from '# exact_s ...', may be empty
};

struct Cert {
  std::string path;
  int n = 0;
  std::string s;                                   // rational literal
  std::vector<std::array<std::string, 3>> squares;  // x, y, t (rational literals)
};

// Throw std::runtime_error with a message naming the file and line on malformed input.
Packing read_sqpk(const std::string& path);
Packing parse_sqpk(const std::string& text, const std::string& path_for_errors);
Cert read_sqcert(const std::string& path);
Cert parse_sqcert(const std::string& text, const std::string& path_for_errors);

}  // namespace sqv
