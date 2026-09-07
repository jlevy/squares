#include "exact_sturm.hpp"

#include <omp.h>

#include <algorithm>
#include <atomic>
#include <fstream>
#include <iostream>
#include <mutex>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
using exact_sturm::Integer;
using exact_sturm::IntegerPolynomial;
using exact_sturm::RationalPoint;


std::vector<RationalPoint> load_samples(const std::string& path) {
  std::ifstream in(path);
  if (!in) throw std::runtime_error("cannot open " + path);
  std::vector<RationalPoint> samples;
  std::string numerator;
  std::string denominator;
  while (in >> numerator >> denominator) {
    RationalPoint sample{Integer(numerator), Integer(denominator)};
    if (sample.denominator <= 0) throw std::runtime_error("nonpositive denominator");
    if (sample.numerator <= 0) throw std::runtime_error("nonpositive sample");
    // t < sqrt(2)-1 iff t^2 + 2t - 1 < 0 for t > 0.
    const Integer endpoint_sign = sample.numerator * sample.numerator +
        2 * sample.numerator * sample.denominator -
        sample.denominator * sample.denominator;
    if (endpoint_sign >= 0) throw std::runtime_error("sample is not below sqrt(2)-1");
    if (!samples.empty() &&
        exact_sturm::as_rational(samples.back()) >= exact_sturm::as_rational(sample)) {
      throw std::runtime_error("samples are not strictly increasing");
    }
    samples.push_back(std::move(sample));
  }
  return samples;
}

std::vector<IntegerPolynomial> load_polynomials(const std::string& path) {
  std::ifstream in(path);
  if (!in) throw std::runtime_error("cannot open " + path);
  std::vector<IntegerPolynomial> polynomials;
  long long a0 = 0;
  long long a1 = 0;
  long long a2 = 0;
  long long a3 = 0;
  long long a4 = 0;
  while (in >> a0 >> a1 >> a2 >> a3 >> a4) {
    polynomials.push_back(IntegerPolynomial{
        Integer(a0), Integer(a1), Integer(a2), Integer(a3), Integer(a4)});
  }
  return polynomials;
}

bool is_interior_boundary(int index, int boundary_count) {
  return index > 0 && index + 1 < boundary_count;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const int threads = argc > 1 ? std::stoi(argv[1]) : 8;
    const std::string event_path =
        argc > 2 ? argv[2] : "data/event_polys_4p55.tsv";
    const std::string sample_path =
        argc > 3 ? argv[3] : "data/orientation_samples_exact_4p55.tsv";
    omp_set_num_threads(threads);

    const auto samples = load_samples(sample_path);
    const auto polynomials = load_polynomials(event_path);
    const int expected_interior_roots = static_cast<int>(samples.size()) - 1;
    std::cout << "polynomials=" << polynomials.size() << " samples=" << samples.size() << " expected_roots=" << expected_interior_roots << '\n';

    // The final rational is strictly above sqrt(2)-1. It is used only as an
    // exact right bracket; the endpoint factor t^2+2t-1 is removed from every
    // event polynomial before root counting.
    const RationalPoint upper_bracket{
        Integer("4142135623730950489"), Integer("10000000000000000000")};
    const Integer upper_sign =
        upper_bracket.numerator * upper_bracket.numerator +
        2 * upper_bracket.numerator * upper_bracket.denominator -
        upper_bracket.denominator * upper_bracket.denominator;
    if (upper_sign <= 0) throw std::runtime_error("upper bracket is not above endpoint");

    std::vector<RationalPoint> boundaries;
    boundaries.reserve(samples.size() + 2);
    boundaries.push_back(RationalPoint{Integer(0), Integer(1)});
    boundaries.insert(boundaries.end(), samples.begin(), samples.end());
    boundaries.push_back(upper_bracket);

    std::vector<std::vector<int>> gap_polynomials(boundaries.size() - 1);
    std::mutex gap_mutex;
    std::atomic<bool> ok(true);
    std::atomic<long long> incidences(0);
    double start = omp_get_wtime();

#pragma omp parallel for schedule(dynamic, 20)
    for (int id = 0; id < static_cast<int>(polynomials.size()); ++id) {
      if (!ok.load()) continue;
      try {
        const auto sturm = exact_sturm::sturm_sequence(polynomials[id]);
        const int total = exact_sturm::root_count(
            sturm, boundaries.front(), boundaries.back());
        if (total < 0 || total > 4) throw std::runtime_error("invalid root count");

        struct Node {
          int left;
          int right;
          int count;
        };
        std::vector<Node> stack;
        if (total > 0) {
          stack.push_back(Node{0, static_cast<int>(boundaries.size()) - 1, total});
        }
        std::vector<int> found;

        while (!stack.empty()) {
          const Node node = stack.back();
          stack.pop_back();
          if (node.right == node.left + 1) {
            if (node.count != 1) {
              throw std::runtime_error("multiple roots in one sample gap");
            }
            if (is_interior_boundary(node.left, boundaries.size()) &&
                exact_sturm::sign_at(polynomials[id], boundaries[node.left]) == 0) {
              throw std::runtime_error("event root equals an interior sample");
            }
            if (is_interior_boundary(node.right, boundaries.size()) &&
                exact_sturm::sign_at(polynomials[id], boundaries[node.right]) == 0) {
              throw std::runtime_error("event root equals an interior sample");
            }
            found.push_back(node.left);
            continue;
          }

          const int middle = (node.left + node.right) / 2;
          if (is_interior_boundary(middle, boundaries.size()) &&
              exact_sturm::sign_at(polynomials[id], boundaries[middle]) == 0) {
            throw std::runtime_error("event root equals an interior sample");
          }
          const int left_count = exact_sturm::root_count(
              sturm, boundaries[node.left], boundaries[middle]);
          const int right_count = node.count - left_count;
          if (left_count < 0 || right_count < 0 ||
              left_count + right_count != node.count) {
            throw std::runtime_error("inconsistent root split");
          }
          if (left_count > 0) {
            stack.push_back(Node{node.left, middle, left_count});
          }
          if (right_count > 0) {
            stack.push_back(Node{middle, node.right, right_count});
          }
        }

        {
          std::lock_guard<std::mutex> lock(gap_mutex);
          for (const int gap : found) gap_polynomials[gap].push_back(id);
        }
        incidences += static_cast<long long>(found.size());
      } catch (const std::exception& e) {
        ok = false;
#pragma omp critical
        { std::cerr << "polynomial " << id << ": " << e.what() << '\n'; }
      }
    }

    if (!ok.load()) return 1;
    std::cout << "located_incidences=" << incidences.load()
              << " seconds=" << (omp_get_wtime() - start) << '\n';

    if (!gap_polynomials.front().empty() || !gap_polynomials.back().empty()) {
      throw std::runtime_error("unexpected root before first or after last sample");
    }
    int missing_gaps = 0;
    for (int gap = 1; gap <= expected_interior_roots; ++gap) {
      if (gap_polynomials[gap].empty()) {
        if (missing_gaps < 100) std::cerr << "missing_gap=" << gap << "\n";
        ++missing_gaps;
      }
    }
    if (missing_gaps) {
      std::cerr << "missing_gaps_total=" << missing_gaps << "\n";
      throw std::runtime_error("missing event roots in proposed gaps");
    }

    // Every polynomial assigned to one gap has exactly one root there. Prove
    // that all such roots are identical by taking exact polynomial gcds with
    // one anchor polynomial.
    std::atomic<bool> common(true);
    long long gcd_checks = 0;
    start = omp_get_wtime();
#pragma omp parallel for schedule(dynamic, 1) reduction(+ : gcd_checks)
    for (int gap = 1; gap <= expected_interior_roots; ++gap) {
      if (!common.load()) continue;
      const int anchor_id = gap_polynomials[gap].front();
      const auto anchor = exact_sturm::to_rational(polynomials[anchor_id]);
      for (const int id : gap_polynomials[gap]) {
        const auto other = exact_sturm::to_rational(polynomials[id]);
        const auto gcd = exact_sturm::integerize(
            exact_sturm::polynomial_gcd(anchor, other));
        const auto gcd_sturm = exact_sturm::sturm_sequence(gcd);
        const int count = exact_sturm::root_count(
            gcd_sturm, boundaries[gap], boundaries[gap + 1]);
        ++gcd_checks;
        if (count != 1) {
          common = false;
#pragma omp critical
          {
            std::cerr << "distinct roots in gap " << gap
                      << ", anchor=" << anchor_id << ", other=" << id
                      << ", gcd_root_count=" << count << '\n';
          }
          break;
        }
      }
    }

    std::cout << "root_gaps=" << expected_interior_roots
              << " gcd_checks=" << gcd_checks
              << " common=" << common.load()
              << " seconds=" << (omp_get_wtime() - start) << '\n';
    if (!common.load()) return 1;

    std::cout << "EXACT EVENT PARTITION PASS\n";
    return 0;
  } catch (const std::exception& e) {
    std::cerr << "error: " << e.what() << '\n';
    return 2;
  }
}
