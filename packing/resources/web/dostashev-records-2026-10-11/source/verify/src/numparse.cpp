#include "numparse.hpp"

#include <cmath>
#include <cstdio>
#include <stdexcept>

namespace sqv {
namespace {

constexpr long kMaxExponent = 10000;

bool is_digit(char c) { return c >= '0' && c <= '9'; }

struct DecParts {
  bool neg = false;
  std::string_view ip, fp;
  long exp = 0;
};

bool split_decimal(std::string_view s, DecParts& out) {
  size_t i = 0;
  const size_t n = s.size();
  out = DecParts{};
  if (i < n && (s[i] == '+' || s[i] == '-')) {
    out.neg = s[i] == '-';
    ++i;
  }
  size_t a = i;
  while (i < n && is_digit(s[i])) ++i;
  out.ip = s.substr(a, i - a);
  if (i < n && s[i] == '.') {
    ++i;
    size_t b = i;
    while (i < n && is_digit(s[i])) ++i;
    out.fp = s.substr(b, i - b);
  }
  if (out.ip.empty() && out.fp.empty()) return false;
  if (i < n && (s[i] == 'e' || s[i] == 'E')) {
    ++i;
    bool eneg = false;
    if (i < n && (s[i] == '+' || s[i] == '-')) {
      eneg = s[i] == '-';
      ++i;
    }
    size_t c = i;
    long e = 0;
    while (i < n && is_digit(s[i])) {
      e = e * 10 + (s[i] - '0');
      if (e > kMaxExponent) return false;
      ++i;
    }
    if (i == c) return false;
    out.exp = eneg ? -e : e;
  }
  return i == n;
}

bool is_integer_literal(std::string_view s, bool allow_sign) {
  size_t i = 0;
  if (allow_sign && !s.empty() && (s[0] == '+' || s[0] == '-')) i = 1;
  if (i >= s.size()) return false;
  for (; i < s.size(); ++i)
    if (!is_digit(s[i])) return false;
  return true;
}

mpz_class parse_int(std::string_view s) {
  bool neg = false;
  if (!s.empty() && (s[0] == '+' || s[0] == '-')) {
    neg = s[0] == '-';
    s.remove_prefix(1);
  }
  mpz_class z;
  if (z.set_str(std::string(s), 10) != 0) throw std::invalid_argument("bad integer: " + std::string(s));
  return neg ? mpz_class(-z) : z;
}

}  // namespace

bool is_decimal_literal(std::string_view s) {
  DecParts p;
  return split_decimal(s, p);
}

bool is_rational_literal(std::string_view s) {
  size_t slash = s.find('/');
  if (slash == std::string_view::npos) return is_decimal_literal(s);
  std::string_view num = s.substr(0, slash), den = s.substr(slash + 1);
  if (!is_integer_literal(num, true) || !is_integer_literal(den, false)) return false;
  for (char c : den)
    if (c != '0') return true;
  return false;  // zero denominator
}

mpz_class pow10(unsigned long k) {
  mpz_class r;
  mpz_ui_pow_ui(r.get_mpz_t(), 10, k);
  return r;
}

mpq_class decimal_to_mpq(std::string_view s) {
  DecParts p;
  if (!split_decimal(s, p)) throw std::invalid_argument("not a decimal literal: '" + std::string(s) + "'");
  std::string digits;
  digits.reserve(p.ip.size() + p.fp.size());
  digits.append(p.ip);
  digits.append(p.fp);
  size_t nz = digits.find_first_not_of('0');
  if (nz == std::string::npos) return mpq_class(0);
  mpz_class m;
  if (m.set_str(digits.substr(nz), 10) != 0) throw std::invalid_argument("bad digits: " + std::string(s));
  long e10 = p.exp - static_cast<long>(p.fp.size());
  mpq_class q;
  if (e10 >= 0) {
    q = mpq_class(m * pow10(static_cast<unsigned long>(e10)));
  } else {
    q = mpq_class(m, pow10(static_cast<unsigned long>(-e10)));
    q.canonicalize();
  }
  if (p.neg) q = -q;
  return q;
}

mpq_class rational_to_mpq(std::string_view s) {
  if (!is_rational_literal(s)) throw std::invalid_argument("not a rational literal: '" + std::string(s) + "'");
  size_t slash = s.find('/');
  if (slash == std::string_view::npos) return decimal_to_mpq(s);
  mpq_class q(parse_int(s.substr(0, slash)), parse_int(s.substr(slash + 1)));
  q.canonicalize();
  return q;
}

int significant_digits(std::string_view s) {
  DecParts p;
  if (!split_decimal(s, p)) throw std::invalid_argument("not a decimal literal: '" + std::string(s) + "'");
  std::string digits(p.ip);
  digits.append(p.fp);
  size_t nz = digits.find_first_not_of('0');
  if (nz == std::string::npos) return 1;
  return static_cast<int>(digits.size() - nz);
}

std::string mpq_to_decimal_ceil(const mpq_class& q, int sig) {
  if (sgn(q) == 0) return "0";
  mpq_class a = abs(q);
  mpz_class fl;
  mpz_fdiv_q(fl.get_mpz_t(), a.get_num_mpz_t(), a.get_den_mpz_t());
  long m;
  if (sgn(fl) > 0) {
    long intdig = static_cast<long>(mpz_sizeinbase(fl.get_mpz_t(), 10));
    if (pow10(static_cast<unsigned long>(intdig - 1)) > fl) --intdig;
    m = sig - intdig;
  } else {
    long z = 0;
    mpq_class t = a * 10;
    while (t < 1) {
      t *= 10;
      ++z;
    }
    m = sig + z;
  }
  if (m < 0) m = 0;
  mpz_class num = q.get_num() * pow10(static_cast<unsigned long>(m));
  mpz_class N;
  mpz_cdiv_q(N.get_mpz_t(), num.get_mpz_t(), q.get_den_mpz_t());
  bool neg = sgn(N) < 0;
  std::string d = mpz_class(abs(N)).get_str();
  if (m > 0) {
    if (d.size() <= static_cast<size_t>(m)) d.insert(0, static_cast<size_t>(m) + 1 - d.size(), '0');
    d.insert(d.size() - static_cast<size_t>(m), ".");
    while (d.back() == '0') d.pop_back();
    if (d.back() == '.') d.pop_back();
  }
  if (neg && d != "0") d.insert(0, "-");
  return d;
}

std::string mpfr_to_sci(mpfr_srcptr x, int sig) {
  if (mpfr_nan_p(x)) return "nan";
  if (mpfr_inf_p(x)) return mpfr_sgn(x) > 0 ? "inf" : "-inf";
  if (mpfr_zero_p(x)) return "0";
  char* buf = nullptr;
  if (mpfr_asprintf(&buf, "%.*Re", sig - 1, x) < 0 || buf == nullptr) return "nan";
  std::string out(buf);
  mpfr_free_str(buf);
  return out;
}

std::string mpq_to_sci(const mpq_class& q, int sig) {
  mpfr_t x;
  mpfr_init2(x, static_cast<mpfr_prec_t>(sig) * 4 + 64);
  mpfr_set_q(x, q.get_mpq_t(), MPFR_RNDN);
  std::string out = mpfr_to_sci(x, sig);
  mpfr_clear(x);
  return out;
}

std::string double_to_sci(double x) {
  if (std::isnan(x)) return "nan";
  if (std::isinf(x)) return x > 0 ? "inf" : "-inf";
  if (x == 0) return "0";
  char buf[64];
  std::snprintf(buf, sizeof buf, "%.16e", x);
  return buf;
}

}  // namespace sqv
