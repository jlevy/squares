// Exact number handling for sqverify: decimal / rational literals <-> GMP, formatting.
#pragma once

#include <gmpxx.h>
#include <mpfr.h>

#include <string>
#include <string_view>

namespace sqv {

// [+-]? (digits ('.' digits?)? | '.' digits) ([eE] [+-]? digits)?   with |exponent| <= 10000.
bool is_decimal_literal(std::string_view s);
// A decimal literal, or [+-]?digits '/' digits with a nonzero denominator.
bool is_rational_literal(std::string_view s);

// Exact conversions. Throw std::invalid_argument on malformed input.
mpq_class decimal_to_mpq(std::string_view s);
mpq_class rational_to_mpq(std::string_view s);

// Significant digits of a decimal literal's mantissa (leading zeros dropped, trailing kept).
int significant_digits(std::string_view s);

mpz_class pow10(unsigned long k);

// q rounded toward +infinity to `sig` significant digits, as a plain decimal string.
std::string mpq_to_decimal_ceil(const mpq_class& q, int sig);
// Approximate scientific-notation strings (round to nearest), `sig` significant digits.
std::string mpq_to_sci(const mpq_class& q, int sig = 20);
std::string mpfr_to_sci(mpfr_srcptr x, int sig = 20);
std::string double_to_sci(double x);

}  // namespace sqv
