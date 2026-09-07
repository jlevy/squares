#pragma once

#include <boost/multiprecision/cpp_int.hpp>
#include <boost/rational.hpp>

#include <algorithm>
#include <stdexcept>
#include <utility>
#include <vector>

namespace exact_sturm {

using Integer = boost::multiprecision::cpp_int;
using Rational = boost::rational<Integer>;
using RationalPolynomial = std::vector<Rational>;  // ascending coefficients
using IntegerPolynomial = std::vector<Integer>;    // ascending coefficients

struct RationalPoint {
  Integer numerator;
  Integer denominator;
};

inline void trim(RationalPolynomial& p) {
  while (p.size() > 1 && p.back() == 0) p.pop_back();
}

inline bool is_zero(const RationalPolynomial& p) {
  return p.size() == 1 && p.front() == 0;
}

inline RationalPolynomial derivative(const RationalPolynomial& p) {
  if (p.size() <= 1) return RationalPolynomial{Rational(0)};
  RationalPolynomial result(p.size() - 1);
  for (std::size_t i = 1; i < p.size(); ++i) {
    result[i - 1] = p[i] * Integer(i);
  }
  trim(result);
  return result;
}

inline std::pair<RationalPolynomial, RationalPolynomial> divide_with_remainder(
    RationalPolynomial dividend, const RationalPolynomial& divisor_input) {
  trim(dividend);
  RationalPolynomial divisor = divisor_input;
  trim(divisor);
  if (is_zero(divisor)) throw std::runtime_error("polynomial division by zero");
  if (dividend.size() < divisor.size()) {
    return {RationalPolynomial{Rational(0)}, dividend};
  }

  RationalPolynomial quotient(dividend.size() - divisor.size() + 1, Rational(0));
  while (!is_zero(dividend) && dividend.size() >= divisor.size()) {
    const std::size_t shift = dividend.size() - divisor.size();
    const Rational coefficient = dividend.back() / divisor.back();
    quotient[shift] += coefficient;
    for (std::size_t j = 0; j < divisor.size(); ++j) {
      dividend[j + shift] -= coefficient * divisor[j];
    }
    trim(dividend);
  }
  trim(quotient);
  return {quotient, dividend};
}

inline RationalPolynomial monic(RationalPolynomial p) {
  trim(p);
  if (is_zero(p)) return p;
  const Rational leading = p.back();
  for (Rational& coefficient : p) coefficient /= leading;
  return p;
}

inline RationalPolynomial polynomial_gcd(RationalPolynomial a,
                                         RationalPolynomial b) {
  trim(a);
  trim(b);
  while (!is_zero(b)) {
    RationalPolynomial remainder = divide_with_remainder(a, b).second;
    a = std::move(b);
    b = std::move(remainder);
  }
  return monic(std::move(a));
}

inline Integer integer_gcd(Integer a, Integer b) {
  if (a < 0) a = -a;
  if (b < 0) b = -b;
  while (b != 0) {
    Integer remainder = a % b;
    a = std::move(b);
    b = std::move(remainder);
  }
  return a;
}

inline Integer integer_lcm(const Integer& a, const Integer& b) {
  if (a == 0 || b == 0) return 0;
  return (a / integer_gcd(a, b)) * b;
}

inline IntegerPolynomial integerize(const RationalPolynomial& p) {
  Integer common_denominator = 1;
  for (const Rational& coefficient : p) {
    common_denominator = integer_lcm(common_denominator, coefficient.denominator());
  }

  IntegerPolynomial result;
  result.reserve(p.size());
  for (const Rational& coefficient : p) {
    result.push_back(coefficient.numerator() *
                     (common_denominator / coefficient.denominator()));
  }

  Integer common_factor = 0;
  for (const Integer& coefficient : result) {
    common_factor = integer_gcd(common_factor, coefficient);
  }
  if (common_factor != 0) {
    for (Integer& coefficient : result) coefficient /= common_factor;
  }
  return result;
}

inline RationalPolynomial to_rational(const IntegerPolynomial& p) {
  RationalPolynomial result;
  result.reserve(p.size());
  for (const Integer& coefficient : p) result.emplace_back(coefficient);
  trim(result);
  return result;
}

// Return the square-free polynomial with endpoint factors t and
// t^2 + 2t - 1 removed. Those endpoint roots correspond to theta=0 and pi/4.
inline IntegerPolynomial physical_open_interval_polynomial(
    const IntegerPolynomial& input) {
  RationalPolynomial p = to_rational(input);
  const RationalPolynomial dp = derivative(p);
  RationalPolynomial square_free =
      divide_with_remainder(p, polynomial_gcd(p, dp)).first;
  square_free = monic(std::move(square_free));

  while (square_free.size() > 1 && square_free.front() == 0) {
    square_free.erase(square_free.begin());
  }

  const RationalPolynomial upper_endpoint{
      Rational(-1), Rational(2), Rational(1)};  // t^2 + 2t - 1
  const RationalPolynomial endpoint_gcd =
      polynomial_gcd(square_free, upper_endpoint);
  if (endpoint_gcd.size() > 1) {
    square_free = divide_with_remainder(square_free, endpoint_gcd).first;
  }
  return integerize(monic(std::move(square_free)));
}

inline std::vector<IntegerPolynomial> sturm_sequence(
    const IntegerPolynomial& input) {
  RationalPolynomial square_free = to_rational(
      physical_open_interval_polynomial(input));
  square_free = monic(std::move(square_free));

  std::vector<RationalPolynomial> sequence{
      square_free, derivative(square_free)};
  while (!is_zero(sequence.back())) {
    RationalPolynomial remainder = divide_with_remainder(
        sequence[sequence.size() - 2], sequence.back()).second;
    if (is_zero(remainder)) break;
    for (Rational& coefficient : remainder) coefficient = -coefficient;
    sequence.push_back(std::move(remainder));
  }

  std::vector<IntegerPolynomial> result;
  result.reserve(sequence.size());
  for (const RationalPolynomial& polynomial : sequence) {
    result.push_back(integerize(polynomial));
  }
  return result;
}

inline int sign(const Integer& value) {
  return value > 0 ? 1 : (value < 0 ? -1 : 0);
}

inline int sign_at(const IntegerPolynomial& p, const RationalPoint& x) {
  const int degree = static_cast<int>(p.size()) - 1;
  Integer value = p[degree];
  Integer denominator_power = x.denominator;
  for (int i = degree - 1; i >= 0; --i) {
    value = value * x.numerator + p[i] * denominator_power;
    denominator_power *= x.denominator;
  }
  return sign(value);
}

inline int sign_variations(const std::vector<IntegerPolynomial>& sequence,
                           const RationalPoint& x) {
  int previous = 0;
  int variations = 0;
  for (const IntegerPolynomial& polynomial : sequence) {
    const int current = sign_at(polynomial, x);
    if (current == 0) continue;
    if (previous != 0 && current != previous) ++variations;
    previous = current;
  }
  return variations;
}

inline int root_count(const std::vector<IntegerPolynomial>& sequence,
                      const RationalPoint& left,
                      const RationalPoint& right) {
  return sign_variations(sequence, left) - sign_variations(sequence, right);
}

inline Rational as_rational(const RationalPoint& x) {
  return Rational(x.numerator, x.denominator);
}

}  // namespace exact_sturm
