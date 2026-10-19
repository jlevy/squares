#include "sqpk.hpp"

#include <fstream>
#include <sstream>
#include <stdexcept>

#include "numparse.hpp"

namespace sqv {
namespace {

constexpr long kMaxSquares = 10'000'000;

std::vector<std::string> split_ws(const std::string& line) {
  std::vector<std::string> out;
  std::istringstream is(line);
  std::string tok;
  while (is >> tok) out.push_back(tok);
  return out;
}

std::string slurp(const std::string& path) {
  std::ifstream f(path, std::ios::binary);
  if (!f) throw std::runtime_error(path + ": cannot open");
  std::ostringstream ss;
  ss << f.rdbuf();
  if (f.bad()) throw std::runtime_error(path + ": read error");
  return ss.str();
}

[[noreturn]] void fail(const std::string& path, long line, const std::string& msg) {
  throw std::runtime_error(path + ":" + std::to_string(line) + ": " + msg);
}

int parse_count(const std::string& path, long line, const std::string& tok) {
  if (tok.empty() || tok.size() > 9) fail(path, line, "bad count '" + tok + "'");
  long v = 0;
  for (char c : tok) {
    if (c < '0' || c > '9') fail(path, line, "bad count '" + tok + "'");
    v = v * 10 + (c - '0');
  }
  if (v < 1 || v > kMaxSquares) fail(path, line, "count out of range '" + tok + "'");
  return static_cast<int>(v);
}

// Shared line-oriented parser. `num_ok` validates data tokens and the s value.
template <class Out, class Pred>
void parse_common(const std::string& text, const std::string& path, Out& out, Pred num_ok,
                  const char* what, Packing* pk) {
  bool have_n = false, have_s = false;
  std::istringstream is(text);
  std::string line;
  long lineno = 0;
  while (std::getline(is, line)) {
    ++lineno;
    if (!line.empty() && line.back() == '\r') line.pop_back();
    size_t first = line.find_first_not_of(" \t");
    if (first == std::string::npos) continue;
    if (line[first] == '#') {
      if (pk) {
        auto toks = split_ws(line.substr(first + 1));
        // '# digits D' is recognised only in exactly that form; any other comment is free text.
        if (toks.size() == 2 && toks[0] == "digits" && toks[1].size() <= 9 &&
            toks[1].find_first_not_of("0123456789") == std::string::npos) {
          pk->digits = parse_count(path, lineno, toks[1]);
        } else if (toks.size() >= 2 && toks[0] == "exact_s") {
          size_t pos = line.find("exact_s");
          std::string rest = line.substr(pos + 7);
          size_t a = rest.find_first_not_of(" \t");
          pk->exact_s = a == std::string::npos ? "" : rest.substr(a);
        }
      }
      continue;
    }
    auto toks = split_ws(line);
    if (toks[0] == "n") {
      if (have_n) fail(path, lineno, "duplicate 'n'");
      if (toks.size() != 2) fail(path, lineno, "expected 'n <count>'");
      out.n = parse_count(path, lineno, toks[1]);
      out.squares.reserve(static_cast<size_t>(out.n));
      have_n = true;
    } else if (toks[0] == "s") {
      if (have_s) fail(path, lineno, "duplicate 's'");
      if (toks.size() != 2 || !num_ok(toks[1])) fail(path, lineno, std::string("expected 's <") + what + ">'");
      out.s = toks[1];
      have_s = true;
    } else {
      if (!have_n || !have_s) fail(path, lineno, "data line before 'n' and 's'");
      if (toks.size() != 3) fail(path, lineno, "expected 3 numbers, got " + std::to_string(toks.size()));
      for (const auto& t : toks)
        if (!num_ok(t)) fail(path, lineno, std::string("not a ") + what + ": '" + t + "'");
      if (static_cast<long>(out.squares.size()) >= out.n) fail(path, lineno, "more data lines than n");
      out.squares.push_back({toks[0], toks[1], toks[2]});
    }
  }
  if (!have_n) fail(path, lineno, "missing 'n'");
  if (!have_s) fail(path, lineno, "missing 's'");
  if (static_cast<long>(out.squares.size()) != out.n)
    fail(path, lineno, "n=" + std::to_string(out.n) + " but " + std::to_string(out.squares.size()) + " data lines");
}

}  // namespace

Packing parse_sqpk(const std::string& text, const std::string& path) {
  Packing p;
  p.path = path;
  parse_common(text, path, p, [](const std::string& t) { return is_decimal_literal(t); }, "decimal", &p);
  return p;
}

Packing read_sqpk(const std::string& path) { return parse_sqpk(slurp(path), path); }

Cert parse_sqcert(const std::string& text, const std::string& path) {
  Cert c;
  c.path = path;
  parse_common(text, path, c, [](const std::string& t) { return is_rational_literal(t); }, "rational", nullptr);
  return c;
}

Cert read_sqcert(const std::string& path) { return parse_sqcert(slurp(path), path); }

}  // namespace sqv
