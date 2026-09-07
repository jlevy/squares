#include <boost/multiprecision/cpp_int.hpp>

#include <algorithm>
#include <charconv>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
using Integer = boost::multiprecision::cpp_int;
constexpr std::int64_t kTarget = 1'000'000'000'000LL;
constexpr int kGrid = 4000;
constexpr int kSideScaled = 18282;
constexpr std::size_t kExpectedAtoms = 560;

struct Atom { int x; int y; std::int64_t weight; };

std::vector<std::string> split_csv(const std::string& line) {
  std::vector<std::string> fields;
  std::string current;
  for (char c : line) {
    if (c == ',') { fields.push_back(current); current.clear(); }
    else if (c != '\r') current.push_back(c);
  }
  fields.push_back(current);
  return fields;
}

long long parse_integer(const std::string& text) {
  long long value = 0;
  auto [ptr, ec] = std::from_chars(text.data(), text.data() + text.size(), value);
  if (ec != std::errc{} || ptr != text.data() + text.size()) {
    throw std::runtime_error("invalid integer: " + text);
  }
  return value;
}

std::vector<Atom> load_atoms(const std::string& path) {
  std::ifstream in(path);
  if (!in) throw std::runtime_error("cannot open " + path);
  std::string line;
  std::getline(in, line);
  std::vector<Atom> atoms;
  while (std::getline(in, line)) {
    if (line.empty()) continue;
    auto f = split_csv(line);
    if (f.size() != 4) throw std::runtime_error("malformed atom row");
    atoms.push_back(Atom{static_cast<int>(parse_integer(f[0])),
                         static_cast<int>(parse_integer(f[1])),
                         parse_integer(f[3])});
  }
  if (atoms.size() != kExpectedAtoms) throw std::runtime_error("bad atom count");
  return atoms;
}

// Exact element a+b*sqrt(2), with integer a and b.
struct Quad {
  Integer a;
  Integer b;
};

Quad operator+(const Quad& x, const Quad& y) { return {x.a + y.a, x.b + y.b}; }
Quad operator-(const Quad& x, const Quad& y) { return {x.a - y.a, x.b - y.b}; }
Quad operator-(const Quad& x) { return {-x.a, -x.b}; }
Quad operator*(long long k, const Quad& x) { return {Integer(k) * x.a, Integer(k) * x.b}; }
bool operator==(const Quad& x, const Quad& y) { return x.a == y.a && x.b == y.b; }

int sign(const Quad& x) {
  if (x.a == 0) return x.b > 0 ? 1 : (x.b < 0 ? -1 : 0);
  if (x.b == 0) return x.a > 0 ? 1 : -1;
  if (x.a > 0 && x.b > 0) return 1;
  if (x.a < 0 && x.b < 0) return -1;
  const Integer a2 = x.a * x.a;
  const Integer two_b2 = 2 * x.b * x.b;
  if (x.a > 0) return a2 > two_b2 ? 1 : -1;
  return two_b2 > a2 ? 1 : -1;
}

bool operator<(const Quad& x, const Quad& y) { return sign(x - y) < 0; }
bool operator<=(const Quad& x, const Quad& y) { return sign(x - y) <= 0; }
Quad absolute(const Quad& x) { return sign(x) < 0 ? -x : x; }
Quad maximum(const Quad& x, const Quad& y) { return x < y ? y : x; }

int exact_index(const std::vector<Quad>& edges, const Quad& value) {
  auto it = std::lower_bound(edges.begin(), edges.end(), value);
  if (it == edges.end() || !(*it == value)) throw std::runtime_error("edge missing");
  return static_cast<int>(it - edges.begin());
}

struct AlgebraicRectangle {
  Quad left, right, bottom, top;
  std::int64_t weight;
};

bool rectangle_intersects_endpoint_diamond(
    const Quad& left, const Quad& right,
    const Quad& bottom, const Quad& top) {
  const Quad center_u_twice = left + right - Quad{Integer(36564), Integer(0)};
  const Quad center_v_twice = bottom + top;
  const Quad width = right - left;
  const Quad height = top - bottom;
  const Quad extent{Integer(18282), Integer(-4000)};  // 1828-400*sqrt(2)

  const Quad gap_u = absolute(center_u_twice) - width - 2 * extent;
  const Quad gap_v = absolute(center_v_twice) - height - 2 * extent;
  const Quad gap_minus = absolute(center_u_twice - center_v_twice) -
      width - height - 2 * extent;
  const Quad gap_plus = absolute(center_u_twice + center_v_twice) -
      width - height - 2 * extent;
  return sign(maximum(maximum(gap_u, gap_v), maximum(gap_minus, gap_plus))) <= 0;
}

void verify_zero_endpoint(const std::vector<Atom>& atoms) {
  // In units of 1/400, feasible axis-aligned centers are [200,1628]^2.
  constexpr int lo = 2000;
  constexpr int hi = 16282;
  std::vector<int> xs{lo, hi};
  std::vector<int> ys{lo, hi};
  struct Rect { int l, r, b, t; std::int64_t w; };
  std::vector<Rect> rectangles;
  for (const Atom& atom : atoms) {
    Rect r{atom.x - 2000, atom.x + 2000, atom.y - 2000, atom.y + 2000, atom.weight};
    rectangles.push_back(r);
    if (lo <= r.l && r.l <= hi) xs.push_back(r.l);
    if (lo <= r.r && r.r <= hi) xs.push_back(r.r);
    if (lo <= r.b && r.b <= hi) ys.push_back(r.b);
    if (lo <= r.t && r.t <= hi) ys.push_back(r.t);
  }
  std::sort(xs.begin(), xs.end()); xs.erase(std::unique(xs.begin(), xs.end()), xs.end());
  std::sort(ys.begin(), ys.end()); ys.erase(std::unique(ys.begin(), ys.end()), ys.end());
  const int nx = static_cast<int>(xs.size()) - 1;
  const int ny = static_cast<int>(ys.size()) - 1;
  const int stride = ny + 1;
  std::vector<std::int64_t> diff(static_cast<std::size_t>(nx + 1) * (ny + 1), 0);
  auto idx = [](const std::vector<int>& e, int z) {
    return static_cast<int>(std::lower_bound(e.begin(), e.end(), z) - e.begin());
  };
  for (const Rect& r : rectangles) {
    const int l = r.l <= lo ? 0 : (r.l >= hi ? nx : idx(xs, r.l));
    const int rr = r.r <= lo ? 0 : (r.r >= hi ? nx : idx(xs, r.r));
    const int b = r.b <= lo ? 0 : (r.b >= hi ? ny : idx(ys, r.b));
    const int t = r.t <= lo ? 0 : (r.t >= hi ? ny : idx(ys, r.t));
    if (l >= rr || b >= t) continue;
    diff[static_cast<std::size_t>(l) * stride + b] += r.w;
    diff[static_cast<std::size_t>(rr) * stride + b] -= r.w;
    diff[static_cast<std::size_t>(l) * stride + t] -= r.w;
    diff[static_cast<std::size_t>(rr) * stride + t] += r.w;
  }
  std::int64_t minimum = std::numeric_limits<std::int64_t>::max();
  for (int i = 0; i <= nx; ++i) for (int j = 0; j <= ny; ++j) {
    auto& value = diff[static_cast<std::size_t>(i) * stride + j];
    if (i) value += diff[static_cast<std::size_t>(i - 1) * stride + j];
    if (j) value += diff[static_cast<std::size_t>(i) * stride + j - 1];
    if (i && j) value -= diff[static_cast<std::size_t>(i - 1) * stride + j - 1];
    if (i < nx && j < ny) minimum = std::min(minimum, value);
  }
  if (minimum < kTarget) throw std::runtime_error("theta=0 coverage failure");
  std::cout << "theta_0_min_open_cell_coverage=" << minimum << '\n';
}

void verify_quarter_turn_endpoint(const std::vector<Atom>& atoms) {
  // U=400*sqrt(2)*u and V=400*sqrt(2)*v. Atom-capture sets are
  // axis-aligned rectangles with boundaries integer +/- 200*sqrt(2).
  const Quad extent{Integer(18282), Integer(-4000)};
  const Quad min_u{Integer(0), Integer(4000)};
  const Quad max_u{Integer(36564), Integer(-4000)};
  const Quad min_v = -extent;
  const Quad max_v = extent;

  std::vector<Quad> xs{min_u, max_u};
  std::vector<Quad> ys{min_v, max_v};
  std::vector<AlgebraicRectangle> rectangles;
  for (const Atom& atom : atoms) {
    const Quad u_center{Integer(atom.x + atom.y), Integer(0)};
    const Quad v_center{Integer(-atom.x + atom.y), Integer(0)};
    const Quad half{Integer(0), Integer(2000)};
    AlgebraicRectangle r{u_center - half, u_center + half,
                         v_center - half, v_center + half, atom.weight};
    rectangles.push_back(r);
    if (min_u <= r.left && r.left <= max_u) xs.push_back(r.left);
    if (min_u <= r.right && r.right <= max_u) xs.push_back(r.right);
    if (min_v <= r.bottom && r.bottom <= max_v) ys.push_back(r.bottom);
    if (min_v <= r.top && r.top <= max_v) ys.push_back(r.top);
  }
  std::sort(xs.begin(), xs.end()); xs.erase(std::unique(xs.begin(), xs.end()), xs.end());
  std::sort(ys.begin(), ys.end()); ys.erase(std::unique(ys.begin(), ys.end()), ys.end());
  const int nx = static_cast<int>(xs.size()) - 1;
  const int ny = static_cast<int>(ys.size()) - 1;
  const int stride = ny + 1;
  std::vector<std::int64_t> diff(static_cast<std::size_t>(nx + 1) * (ny + 1), 0);

  auto clipped = [](const Quad& z, const Quad& lo, const Quad& hi,
                    const std::vector<Quad>& edges, int cells) {
    if (z <= lo) return 0;
    if (hi <= z) return cells;
    return exact_index(edges, z);
  };
  for (const auto& r : rectangles) {
    const int l = clipped(r.left, min_u, max_u, xs, nx);
    const int rr = clipped(r.right, min_u, max_u, xs, nx);
    const int b = clipped(r.bottom, min_v, max_v, ys, ny);
    const int t = clipped(r.top, min_v, max_v, ys, ny);
    if (l >= rr || b >= t) continue;
    diff[static_cast<std::size_t>(l) * stride + b] += r.weight;
    diff[static_cast<std::size_t>(rr) * stride + b] -= r.weight;
    diff[static_cast<std::size_t>(l) * stride + t] -= r.weight;
    diff[static_cast<std::size_t>(rr) * stride + t] += r.weight;
  }
  for (int i = 0; i <= nx; ++i) for (int j = 0; j <= ny; ++j) {
    auto& value = diff[static_cast<std::size_t>(i) * stride + j];
    if (i) value += diff[static_cast<std::size_t>(i - 1) * stride + j];
    if (j) value += diff[static_cast<std::size_t>(i) * stride + j - 1];
    if (i && j) value -= diff[static_cast<std::size_t>(i - 1) * stride + j - 1];
  }

  std::uint64_t runs = 0;
  std::int64_t minimum = std::numeric_limits<std::int64_t>::max();
  for (int i = 0; i < nx; ++i) {
    int j = 0;
    while (j < ny) {
      const auto coverage = diff[static_cast<std::size_t>(i) * stride + j];
      minimum = std::min(minimum, coverage);
      if (coverage >= kTarget) { ++j; continue; }
      const int start = j;
      while (j < ny && diff[static_cast<std::size_t>(i) * stride + j] < kTarget) {
        minimum = std::min(minimum, diff[static_cast<std::size_t>(i) * stride + j]);
        ++j;
      }
      ++runs;
      if (rectangle_intersects_endpoint_diamond(
              xs[i], xs[i + 1], ys[start], ys[j])) {
        throw std::runtime_error("theta=pi/4 coverage failure");
      }
    }
  }
  std::cout << "theta_pi_over_4_subthreshold_runs=" << runs << '\n';
  std::cout << "theta_pi_over_4_min_arrangement_coverage=" << minimum << '\n';
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const std::string atom_path =
        argc > 1 ? argv[1] : "compressed457_atoms_rational_safe.csv";
    const auto atoms = load_atoms(atom_path);
    Integer total_mass = 0;
    for (const auto& atom : atoms) total_mass += atom.weight;
    const Integer expected_mass("16994734834452");
    if (total_mass != expected_mass) throw std::runtime_error("unexpected total mass");
    if (total_mass >= Integer(17) * kTarget) throw std::runtime_error("mass is not below 17");
    std::cout << "exact_total_mass_numerator=" << total_mass << '\n';
    verify_zero_endpoint(atoms);
    verify_quarter_turn_endpoint(atoms);
    std::cout << "EXACT ENDPOINT COVERAGE PASS\n";
    return 0;
  } catch (const std::exception& e) {
    std::cerr << "error: " << e.what() << '\n';
    return 1;
  }
}
