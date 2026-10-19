#include "verifier.hpp"

#include <gmpxx.h>
#include <mpfr.h>

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <numbers>
#include <stdexcept>

#include "geometry.hpp"
#include "numparse.hpp"

#if MPFR_VERSION < MPFR_VERSION_NUM(4, 2, 0)
#error "sqverify needs MPFR >= 4.2 (mpfr_sinu / mpfr_cosu / mpfr_tanu)"
#endif

namespace sqv {
namespace {

using Clock = std::chrono::steady_clock;
double ms_since(Clock::time_point t0) {
  return std::chrono::duration<double, std::milli>(Clock::now() - t0).count();
}

const char* const kWallNames[4] = {"left", "bottom", "right", "top"};
constexpr mpfr_rnd_t RN = MPFR_RNDN;
// Coordinates beyond this make the double broad phase's error bound (see certify) unproven.
constexpr double kMaxCoord = 1e4;

// RAII wrapper over mpfr_t. Movable (by swap), not copyable.
class Mpf {
 public:
  explicit Mpf(mpfr_prec_t prec) {
    mpfr_init2(v_, prec);
    mpfr_set_zero(v_, 1);
  }
  Mpf(Mpf&& o) noexcept {
    mpfr_init2(v_, MPFR_PREC_MIN);
    mpfr_swap(v_, o.v_);
  }
  Mpf& operator=(Mpf&& o) noexcept {
    mpfr_swap(v_, o.v_);
    return *this;
  }
  Mpf(const Mpf&) = delete;
  Mpf& operator=(const Mpf&) = delete;
  ~Mpf() { mpfr_clear(v_); }
  mpfr_ptr p() { return v_; }
  mpfr_srcptr p() const { return v_; }

 private:
  mpfr_t v_;
};

void set_dec(mpfr_ptr x, const std::string& s) {
  if (mpfr_set_str(x, s.c_str(), 10, RN) != 0) throw std::runtime_error("MPFR cannot parse '" + s + "'");
}

struct MpSq {
  Mpf cx, cy, C, S, e;
  explicit MpSq(mpfr_prec_t b) : cx(b), cy(b), C(b), S(b), e(b) {}
};

struct MpWork {
  Mpf dx, dy, m, q, cd, sd;
  explicit MpWork(mpfr_prec_t b) : dx(b), dy(b), m(b), q(b), cd(b), sd(b) {}
};

// sep = max_k |d . u_k| - (1 + |cD| + |sD|)/2, see geometry.hpp.
void mp_sep(mpfr_ptr out, const MpSq& a, const MpSq& b, MpWork& w) {
  mpfr_sub(w.dx.p(), b.cx.p(), a.cx.p(), RN);
  mpfr_sub(w.dy.p(), b.cy.p(), a.cy.p(), RN);
  mpfr_fmma(w.m.p(), w.dx.p(), a.C.p(), w.dy.p(), a.S.p(), RN);
  mpfr_abs(w.m.p(), w.m.p(), RN);
  mpfr_fmms(w.q.p(), w.dy.p(), a.C.p(), w.dx.p(), a.S.p(), RN);
  mpfr_abs(w.q.p(), w.q.p(), RN);
  mpfr_max(w.m.p(), w.m.p(), w.q.p(), RN);
  mpfr_fmma(w.q.p(), w.dx.p(), b.C.p(), w.dy.p(), b.S.p(), RN);
  mpfr_abs(w.q.p(), w.q.p(), RN);
  mpfr_max(w.m.p(), w.m.p(), w.q.p(), RN);
  mpfr_fmms(w.q.p(), w.dy.p(), b.C.p(), w.dx.p(), b.S.p(), RN);
  mpfr_abs(w.q.p(), w.q.p(), RN);
  mpfr_max(w.m.p(), w.m.p(), w.q.p(), RN);
  mpfr_fmma(w.cd.p(), a.C.p(), b.C.p(), a.S.p(), b.S.p(), RN);
  mpfr_abs(w.cd.p(), w.cd.p(), RN);
  mpfr_fmms(w.sd.p(), a.S.p(), b.C.p(), a.C.p(), b.S.p(), RN);
  mpfr_abs(w.sd.p(), w.sd.p(), RN);
  mpfr_add(w.cd.p(), w.cd.p(), w.sd.p(), RN);
  mpfr_add_ui(w.cd.p(), w.cd.p(), 1, RN);
  mpfr_div_2ui(w.cd.p(), w.cd.p(), 1, RN);
  mpfr_sub(out, w.m.p(), w.cd.p(), RN);
}

std::string fmt_g(double x) {
  char buf[48];
  std::snprintf(buf, sizeof buf, "%.3g", x);
  return buf;
}

double parse_positive(const std::string& s, const char* what) {
  if (!is_decimal_literal(s)) throw std::runtime_error(std::string(what) + " is not a decimal literal: '" + s + "'");
  double v = std::strtod(s.c_str(), nullptr);
  if (!(v > 0) || !std::isfinite(v)) throw std::runtime_error(std::string(what) + " must be positive: '" + s + "'");
  return v;
}

// theta (exact, degrees) reduced into [0, 90): squares have 90-degree symmetry.
mpq_class reduce_angle(mpq_class theta) {
  mpq_class q = theta / 90;
  mpz_class fl;
  mpz_fdiv_q(fl.get_mpz_t(), q.get_num_mpz_t(), q.get_den_mpz_t());
  theta -= mpq_class(90 * fl);
  return theta;
}

struct ExactSquare {
  mpq_class x, y, t, C, S, E;
};

void set_trig_from_t(ExactSquare& q) {
  mpq_class t2 = q.t * q.t;
  mpq_class den = 1 + t2;
  q.C = (1 - t2) / den;
  q.S = 2 * q.t / den;
  q.E = (absval(q.C) + absval(q.S)) / 2;
}

mpq_class wall_base(const ExactSquare& q, const mpq_class& s, int w) {
  switch (w) {
    case 0: return q.x;
    case 1: return q.y;
    case 2: return s - q.x;
    default: return s - q.y;
  }
}

// ---------------------------------------------------------------------------------------------
// Exact certificate (see sqverify.cpp header for the argument).
CertResult certify_packing(const Packing& p, int D, mpfr_prec_t bits, const std::vector<std::pair<int, int>>& cands,
                           const std::vector<double>& X, const std::vector<double>& Y, double s_d,
                           const std::string& cert_dir) {
  auto t0 = Clock::now();
  CertResult c;
  const int n = p.n;
  // Rigour of the broad phase: every coordinate is a correctly rounded double of magnitude
  // <= 1e4, so each is within 1e4 * 2^-53 ~ 1.1e-12 of the exact decimal and the double
  // centre distance^2 of any pair the grid can see (|dx|,|dy| < 3) is within ~1e-10 of the exact
  // value. Candidates are all pairs with double distance^2 < r2 where r2 >= 2 + 1e-6, and pairs in
  // non-adjacent grid cells are more than sqrt(r2) apart, so every pair NOT examined below has
  // exact centre distance^2 > 2 + 1e-6 - 1e-10 > 2: its circumscribed disks (radius sqrt(2)/2) are
  // disjoint, hence so are the squares. The same holds for examined pairs whose exact distance^2
  // is > 2. Dilation by f >= 1 only increases centre distances.
  for (int i = 0; i < n; ++i) {
    if (!(std::fabs(X[i]) <= kMaxCoord && std::fabs(Y[i]) <= kMaxCoord)) {
      c.error = "coordinate magnitude exceeds 1e4; broad-phase error bound not established";
      c.time_ms = ms_since(t0);
      return c;
    }
  }
  if (!(std::fabs(s_d) <= kMaxCoord)) {
    c.error = "side exceeds 1e4";
    c.time_ms = ms_since(t0);
    return c;
  }
  mpq_class s = decimal_to_mpq(p.s);
  if (sgn(s) <= 0) {
    c.error = "non-positive side";
    c.time_ms = ms_since(t0);
    return c;
  }

  // Exact squares: rational centres, rational half-angle tangent t rounded to K fractional digits.
  const unsigned long K = static_cast<unsigned long>(D) + 10;
  const mpz_class p10K = pow10(K);
  std::vector<ExactSquare> sq(static_cast<size_t>(n));
  Mpf th(bits), tt(bits);
  mpz_class z;
  for (int i = 0; i < n; ++i) {
    ExactSquare& q = sq[static_cast<size_t>(i)];
    q.x = decimal_to_mpq(p.squares[static_cast<size_t>(i)][0]);
    q.y = decimal_to_mpq(p.squares[static_cast<size_t>(i)][1]);
    mpq_class theta = reduce_angle(decimal_to_mpq(p.squares[static_cast<size_t>(i)][2]));
    if (sgn(theta) == 0) {
      q.t = 0;
    } else {
      mpfr_set_q(th.p(), theta.get_mpq_t(), RN);
      mpfr_tanu(tt.p(), th.p(), 720, RN);  // tan(2 pi theta / 720) = tan(theta/2), theta in degrees
      mpfr_mul_z(tt.p(), tt.p(), p10K.get_mpz_t(), RN);
      mpfr_get_z(z.get_mpz_t(), tt.p(), RN);
      q.t = mpq_class(z, p10K);
      q.t.canonicalize();
    }
    set_trig_from_t(q);
  }

  struct EP {
    int i, j;
    mpq_class M, R;
  };
  std::vector<EP> eps;
  for (auto [i, j] : cands) {
    const ExactSquare& a = sq[static_cast<size_t>(i)];
    const ExactSquare& b = sq[static_cast<size_t>(j)];
    mpq_class dx = b.x - a.x, dy = b.y - a.y;
    mpq_class d2 = dx * dx + dy * dy;
    if (d2 > 2) continue;  // strictly disjoint circumscribed disks (d2 == 2 may be a corner touch)
    EP e{i, j, 0, 0};
    sat_parts<mpq_class>(a.x, a.y, a.C, a.S, b.x, b.y, b.C, b.S, e.M, e.R);
    eps.push_back(std::move(e));
  }
  c.n_exact_pairs = static_cast<long>(eps.size());
  std::vector<mpq_class> A(static_cast<size_t>(4 * n));
  for (int i = 0; i < n; ++i)
    for (int w = 0; w < 4; ++w) A[static_cast<size_t>(4 * i + w)] = wall_base(sq[static_cast<size_t>(i)], s, w);

  auto factor = [](int k) {
    mpq_class f(mpz_class(1), pow10(static_cast<unsigned long>(k)));
    f += 1;
    return f;
  };
  // Dilated geometry: centres f c, side f s. Pair sep = f M - R; wall slack = f A - E.
  auto passes = [&](int k) {
    mpq_class f = factor(k), tmp;
    for (const auto& e : eps) {
      tmp = f * e.M;
      if (tmp < e.R) return false;
    }
    for (int i = 0; i < n; ++i)
      for (int w = 0; w < 4; ++w) {
        tmp = f * A[static_cast<size_t>(4 * i + w)];
        if (tmp < sq[static_cast<size_t>(i)].E) return false;
      }
    return true;
  };

  const int kmin = 9;
  const int kmax = std::max(30, D);
  int k_ok = kmin;
  if (!passes(kmin)) {
    c.passed = false;
  } else {
    c.passed = true;
    if (passes(kmax)) {
      k_ok = kmax;
    } else {
      int lo = kmin, hi = kmax;  // passes(lo), !passes(hi)
      while (hi - lo > 1) {
        int mid = (lo + hi) / 2;
        if (passes(mid))
          lo = mid;
        else
          hi = mid;
      }
      k_ok = lo;
    }
  }
  mpq_class f = factor(k_ok);
  mpq_class minsep, minslack, tmp;
  bool have_sep = false;
  for (const auto& e : eps) {
    tmp = f * e.M - e.R;
    if (!have_sep || tmp < minsep) {
      minsep = tmp;
      have_sep = true;
    }
  }
  for (int i = 0; i < n; ++i)
    for (int w = 0; w < 4; ++w) {
      tmp = f * A[static_cast<size_t>(4 * i + w)] - sq[static_cast<size_t>(i)].E;
      if ((i == 0 && w == 0) || tmp < minslack) minslack = tmp;
    }
  c.delta = "1e-" + std::to_string(k_ok);
  c.delta_exp = -k_ok;
  c.has_delta_exp = true;
  mpq_class sc = f * s;
  c.s_cert = sc.get_str();
  c.s_cert_decimal = mpq_to_decimal_ceil(sc, 40);
  c.min_exact_sep = have_sep ? mpq_to_sci(minsep) : "inf";
  c.min_exact_slack = mpq_to_sci(minslack);

  if (c.passed && !cert_dir.empty()) {
    namespace fs = std::filesystem;
    fs::create_directories(cert_dir);
    fs::path out = fs::path(cert_dir) / (fs::path(p.path).stem().string() + ".sqcert");
    std::ofstream o(out);
    o << "# sqcert v1\n"
      << "# generated-by: sqverify --certify\n"
      << "# source: " << p.path << "\n"
      << "# claimed_s: " << p.s << "\n"
      << "# delta: " << c.delta << " (centres and side multiplied by 1 + delta)\n"
      << "# digits: " << D << ", t rounded to " << K << " fractional digits\n"
      << "# square i: centre (x, y), (cos, sin) = ((1-t^2)/(1+t^2), 2t/(1+t^2))\n"
      << "n " << n << "\n"
      << "s " << sc.get_str() << "\n"
      << "# x y t\n";
    for (int i = 0; i < n; ++i) {
      const ExactSquare& q = sq[static_cast<size_t>(i)];
      mpq_class xx = f * q.x, yy = f * q.y;
      o << xx.get_str() << ' ' << yy.get_str() << ' ' << q.t.get_str() << '\n';
    }
    o.close();
    if (!o) {
      c.error = "cannot write " + out.string();
      c.passed = false;
    } else {
      c.cert_file = out.string();
    }
  }
  c.time_ms = ms_since(t0);
  return c;
}

void finish_rattlers(FileResult& r, int n, const std::vector<std::pair<int, int>>& pc, const std::vector<int>& wc) {
  auto [nfree, rat] = rattler_estimate(n, pc, wc);
  r.n_free = nfree;
  r.rattlers = std::move(rat);
  r.n_rattlers = static_cast<long>(r.rattlers.size());
}

}  // namespace

// ---------------------------------------------------------------------------------------------
bool FileResult::ok() const {
  if (!error.empty()) return false;
  if (cert && !cert->passed) return false;
  return classification == "valid" || classification == "valid-with-contacts" || classification == "certified";
}

std::vector<std::pair<int, int>> candidate_pairs(const std::vector<double>& x, const std::vector<double>& y,
                                                 double r2) {
  const size_t n = x.size();
  std::vector<std::pair<int, int>> out;
  if (n < 2) return out;
  const double h = std::max(1.5, std::sqrt(r2) * (1 + 1e-9));
  double xmin = x[0], xmax = x[0], ymin = y[0], ymax = y[0];
  for (size_t i = 0; i < n; ++i) {
    if (!std::isfinite(x[i]) || !std::isfinite(y[i])) throw std::runtime_error("non-finite centre");
    xmin = std::min(xmin, x[i]);
    xmax = std::max(xmax, x[i]);
    ymin = std::min(ymin, y[i]);
    ymax = std::max(ymax, y[i]);
  }
  if (!(std::max(xmax - xmin, ymax - ymin) / h < 1e9)) throw std::runtime_error("centres too spread for the grid");
  auto key = [](int64_t ix, int64_t iy) { return (static_cast<uint64_t>(ix) << 32) | static_cast<uint64_t>(iy); };
  std::vector<int64_t> cx(n), cy(n);
  std::vector<std::pair<uint64_t, int>> keyed(n);
  for (size_t i = 0; i < n; ++i) {
    cx[i] = static_cast<int64_t>(std::floor((x[i] - xmin) / h));
    cy[i] = static_cast<int64_t>(std::floor((y[i] - ymin) / h));
    keyed[i] = {key(cx[i], cy[i]), static_cast<int>(i)};
  }
  std::sort(keyed.begin(), keyed.end());
  for (size_t i = 0; i < n; ++i) {
    for (int64_t ddx = -1; ddx <= 1; ++ddx)
      for (int64_t ddy = -1; ddy <= 1; ++ddy) {
        int64_t jx = cx[i] + ddx, jy = cy[i] + ddy;
        if (jx < 0 || jy < 0) continue;
        uint64_t k = key(jx, jy);
        auto lo = std::lower_bound(keyed.begin(), keyed.end(), std::make_pair(k, -1));
        for (auto it = lo; it != keyed.end() && it->first == k; ++it) {
          size_t j = static_cast<size_t>(it->second);
          if (j <= i) continue;
          double dx = x[j] - x[i], dy = y[j] - y[i];
          if (dx * dx + dy * dy < r2) out.emplace_back(static_cast<int>(i), static_cast<int>(j));
        }
      }
  }
  std::sort(out.begin(), out.end());
  return out;
}

std::pair<long, std::vector<int>> rattler_estimate(int n, const std::vector<std::pair<int, int>>& pc,
                                                   const std::vector<int>& wc) {
  std::vector<std::vector<int>> adj(static_cast<size_t>(n));
  for (auto [i, j] : pc) {
    adj[static_cast<size_t>(i)].push_back(j);
    adj[static_cast<size_t>(j)].push_back(i);
  }
  std::vector<int> deg(static_cast<size_t>(n));
  long nfree = 0;
  std::vector<int> stack;
  for (int i = 0; i < n; ++i) {
    deg[static_cast<size_t>(i)] = static_cast<int>(adj[static_cast<size_t>(i)].size()) + wc[static_cast<size_t>(i)];
    if (deg[static_cast<size_t>(i)] == 0) ++nfree;
    if (deg[static_cast<size_t>(i)] < 3) stack.push_back(i);
  }
  std::vector<char> removed(static_cast<size_t>(n), 0);
  while (!stack.empty()) {
    int i = stack.back();
    stack.pop_back();
    if (removed[static_cast<size_t>(i)]) continue;
    removed[static_cast<size_t>(i)] = 1;
    for (int j : adj[static_cast<size_t>(i)]) {
      if (removed[static_cast<size_t>(j)]) continue;
      if (--deg[static_cast<size_t>(j)] < 3) stack.push_back(j);
    }
  }
  std::vector<int> out;
  for (int i = 0; i < n; ++i)
    if (removed[static_cast<size_t>(i)]) out.push_back(i);
  return {nfree, out};
}

// ---------------------------------------------------------------------------------------------
FileResult verify_packing(const Packing& p, const Options& opt) {
  auto t0 = Clock::now();
  FileResult r;
  r.path = p.path;
  r.n = p.n;
  r.claimed_s = p.s;
  r.exact_s = p.exact_s;
  r.precise = opt.precise;
  const int n = p.n;
  const size_t N = static_cast<size_t>(n);

  // Source digits D and tolerance.
  int D;
  if (p.digits > 0) {
    D = p.digits;
  } else {
    mpq_class sq = decimal_to_mpq(p.s);
    D = sq.get_den() != 1 ? significant_digits(p.s) : 30;
  }
  D = std::clamp(D, 6, 1000);
  r.digits = D;
  const std::string tol_s = opt.tol.empty() ? "1e-" + std::to_string(D - 3) : opt.tol;
  const double tol_d = parse_positive(tol_s, "tol");
  r.tol_nominal = tol_s;
  std::string tol_eff_s = tol_s;
  double tol_eff = tol_d;
  if (!opt.precise && tol_d < 1e-12) {
    tol_eff_s = "1e-12";
    tol_eff = 1e-12;
  }
  r.tol = tol_eff_s;
  double near_d;
  if (!opt.near.empty()) {
    near_d = parse_positive(opt.near, "near");
    r.near = opt.near;
  } else {
    near_d = std::max(1e-6, 100 * tol_eff);
    r.near = fmt_g(near_d);
  }
  // Rattler estimate uses structural contacts: gap <= rattler_gap (default max(tol, 1e-9)), so
  // that a certificate dilated by ~1e-12 still shows its contact structure.
  double rgap = std::max(tol_eff, 1e-9);
  if (!opt.rattler_gap.empty()) rgap = std::max(tol_eff, parse_positive(opt.rattler_gap, "rattler-gap"));
  r.rattler_gap = fmt_g(rgap);
  const mpfr_prec_t bits = std::max<mpfr_prec_t>(
      128, static_cast<mpfr_prec_t>(std::ceil((D + 25) * std::numbers::ln10 / std::numbers::ln2)));
  r.precision_bits = opt.precise ? static_cast<int>(bits) : 53;

  // ---- fast pass (double) ----
  const double s_d = std::strtod(p.s.c_str(), nullptr);
  if (!std::isfinite(s_d) || s_d <= 0) throw std::runtime_error("claimed side must be positive and finite");
  std::vector<double> X(N), Y(N), C(N), S(N), E(N);
  for (size_t i = 0; i < N; ++i) {
    X[i] = std::strtod(p.squares[i][0].c_str(), nullptr);
    Y[i] = std::strtod(p.squares[i][1].c_str(), nullptr);
    double th = std::strtod(p.squares[i][2].c_str(), nullptr);
    if (!std::isfinite(X[i]) || !std::isfinite(Y[i]) || !std::isfinite(th))
      throw std::runtime_error("non-finite value on square " + std::to_string(i));
    double rad = th * (std::numbers::pi / 180.0);
    C[i] = std::cos(rad);
    S[i] = std::sin(rad);
    E[i] = (std::fabs(C[i]) + std::fabs(S[i])) / 2;
  }
  const double rc = std::sqrt(2.0) + 2 * near_d;
  const double r2 = std::max(rc * rc, 2.0 + 1e-6);
  const auto cands = candidate_pairs(X, Y, r2);
  const size_t P = cands.size();
  r.n_candidate_pairs = static_cast<long>(P);
  std::vector<double> sep_d(P);
  for (size_t k = 0; k < P; ++k) {
    size_t i = static_cast<size_t>(cands[k].first), j = static_cast<size_t>(cands[k].second);
    sep_d[k] = sat_sep<double>(X[i], Y[i], C[i], S[i], X[j], Y[j], C[j], S[j]);
  }
  std::vector<double> wall_d(4 * N);
  for (size_t i = 0; i < N; ++i) {
    wall_d[4 * i + 0] = X[i] - E[i];
    wall_d[4 * i + 1] = Y[i] - E[i];
    wall_d[4 * i + 2] = s_d - X[i] - E[i];
    wall_d[4 * i + 3] = s_d - Y[i] - E[i];
  }
  std::vector<int> near_pos(P, -1);
  std::vector<size_t> near_idx;
  for (size_t k = 0; k < P; ++k)
    if (sep_d[k] < near_d) {
      near_pos[k] = static_cast<int>(near_idx.size());
      near_idx.push_back(k);
    }
  r.n_near_pairs = static_cast<long>(near_idx.size());

  std::vector<double> approx = sep_d;
  std::vector<char> contact(P, 0), overlap(P, 0);
  std::vector<double> wapprox = wall_d;
  std::vector<char> wcontact(4 * N, 0), woutside(4 * N, 0);
  std::vector<Mpf> near_val, wall_val;
  std::size_t kmin = P;  // index of min-sep pair

  if (opt.precise) {
    // ---- precise pass (MPFR) ----
    std::vector<MpSq> M;
    M.reserve(N);
    Mpf ms(bits), tolm(bits), negtol(bits), th(bits);
    set_dec(ms.p(), p.s);
    set_dec(tolm.p(), tol_s);
    mpfr_neg(negtol.p(), tolm.p(), RN);
    for (size_t i = 0; i < N; ++i) {
      M.emplace_back(bits);
      MpSq& q = M.back();
      set_dec(q.cx.p(), p.squares[i][0]);
      set_dec(q.cy.p(), p.squares[i][1]);
      set_dec(th.p(), p.squares[i][2]);
      mpfr_sinu(q.S.p(), th.p(), 360, RN);
      mpfr_cosu(q.C.p(), th.p(), 360, RN);
      mpfr_abs(q.e.p(), q.C.p(), RN);
      mpfr_abs(th.p(), q.S.p(), RN);
      mpfr_add(q.e.p(), q.e.p(), th.p(), RN);
      mpfr_div_2ui(q.e.p(), q.e.p(), 1, RN);
    }
    MpWork w(bits);
    near_val.reserve(near_idx.size());
    for (size_t k : near_idx) {
      near_val.emplace_back(bits);
      mpfr_ptr v = near_val.back().p();
      mp_sep(v, M[static_cast<size_t>(cands[k].first)], M[static_cast<size_t>(cands[k].second)], w);
      approx[k] = mpfr_get_d(v, RN);
      contact[k] = mpfr_cmpabs(v, tolm.p()) <= 0;
      overlap[k] = mpfr_cmp(v, negtol.p()) < 0;
    }
    for (size_t k = 0; k < P; ++k)
      if (near_pos[k] < 0) {
        contact[k] = std::fabs(sep_d[k]) <= tol_eff;
        overlap[k] = sep_d[k] < -tol_eff;
      }
    // Walls, containment and bounding side for every square.
    wall_val.reserve(4 * N);
    Mpf xmin(bits), xmax(bits), ymin(bits), ymax(bits), t1(bits);
    for (size_t i = 0; i < N; ++i) {
      const MpSq& q = M[i];
      for (int wv = 0; wv < 4; ++wv) {
        wall_val.emplace_back(bits);
        mpfr_ptr v = wall_val.back().p();
        switch (wv) {
          case 0: mpfr_sub(v, q.cx.p(), q.e.p(), RN); break;
          case 1: mpfr_sub(v, q.cy.p(), q.e.p(), RN); break;
          case 2:
            mpfr_sub(v, ms.p(), q.cx.p(), RN);
            mpfr_sub(v, v, q.e.p(), RN);
            break;
          default:
            mpfr_sub(v, ms.p(), q.cy.p(), RN);
            mpfr_sub(v, v, q.e.p(), RN);
            break;
        }
        size_t idx = 4 * i + static_cast<size_t>(wv);
        wapprox[idx] = mpfr_get_d(v, RN);
        wcontact[idx] = mpfr_cmpabs(v, tolm.p()) <= 0;
        woutside[idx] = mpfr_cmp(v, negtol.p()) < 0;
      }
      mpfr_add(t1.p(), q.cx.p(), q.e.p(), RN);
      if (i == 0 || mpfr_cmp(t1.p(), xmax.p()) > 0) mpfr_set(xmax.p(), t1.p(), RN);
      mpfr_sub(t1.p(), q.cx.p(), q.e.p(), RN);
      if (i == 0 || mpfr_cmp(t1.p(), xmin.p()) < 0) mpfr_set(xmin.p(), t1.p(), RN);
      mpfr_add(t1.p(), q.cy.p(), q.e.p(), RN);
      if (i == 0 || mpfr_cmp(t1.p(), ymax.p()) > 0) mpfr_set(ymax.p(), t1.p(), RN);
      mpfr_sub(t1.p(), q.cy.p(), q.e.p(), RN);
      if (i == 0 || mpfr_cmp(t1.p(), ymin.p()) < 0) mpfr_set(ymin.p(), t1.p(), RN);
    }
    mpfr_sub(xmax.p(), xmax.p(), xmin.p(), RN);
    mpfr_sub(ymax.p(), ymax.p(), ymin.p(), RN);
    mpfr_max(xmax.p(), xmax.p(), ymax.p(), RN);
    r.bounding_s = mpfr_to_sci(xmax.p(), 30);
    mpfr_sub(xmax.p(), xmax.p(), ms.p(), RN);
    r.bounding_minus_claimed = mpfr_to_sci(xmax.p());
    size_t wmin = 0;
    for (size_t idx = 1; idx < 4 * N; ++idx)
      if (mpfr_cmp(wall_val[idx].p(), wall_val[wmin].p()) < 0) wmin = idx;
    r.containment_slack = mpfr_to_sci(wall_val[wmin].p());
    // Min sep: the near pairs (MPFR) hold it whenever any exist.
    if (!near_idx.empty()) {
      size_t best = 0;
      for (size_t a = 1; a < near_idx.size(); ++a)
        if (mpfr_cmp(near_val[a].p(), near_val[best].p()) < 0) best = a;
      kmin = near_idx[best];
    }
    for (size_t k = 0; k < P; ++k)
      if (near_pos[k] < 0 && (kmin == P || approx[k] < approx[kmin])) kmin = k;
  } else {
    for (size_t k = 0; k < P; ++k) {
      contact[k] = std::fabs(sep_d[k]) <= tol_eff;
      overlap[k] = sep_d[k] < -tol_eff;
      if (kmin == P || sep_d[k] < sep_d[kmin]) kmin = k;
    }
    double xmin = 0, xmax = 0, ymin = 0, ymax = 0;
    for (size_t i = 0; i < N; ++i) {
      for (int wv = 0; wv < 4; ++wv) {
        size_t idx = 4 * i + static_cast<size_t>(wv);
        wcontact[idx] = std::fabs(wall_d[idx]) <= tol_eff;
        woutside[idx] = wall_d[idx] < -tol_eff;
      }
      if (i == 0 || X[i] + E[i] > xmax) xmax = X[i] + E[i];
      if (i == 0 || X[i] - E[i] < xmin) xmin = X[i] - E[i];
      if (i == 0 || Y[i] + E[i] > ymax) ymax = Y[i] + E[i];
      if (i == 0 || Y[i] - E[i] < ymin) ymin = Y[i] - E[i];
    }
    double b = std::max(xmax - xmin, ymax - ymin);
    r.bounding_s = double_to_sci(b);
    r.bounding_minus_claimed = double_to_sci(b - s_d);
    r.containment_slack = double_to_sci(*std::min_element(wall_d.begin(), wall_d.end()));
  }

  auto pair_str = [&](size_t k) {
    return near_pos[k] >= 0 && opt.precise ? mpfr_to_sci(near_val[static_cast<size_t>(near_pos[k])].p())
                                           : double_to_sci(sep_d[k]);
  };
  auto wall_str = [&](size_t idx) {
    return opt.precise ? mpfr_to_sci(wall_val[idx].p()) : double_to_sci(wall_d[idx]);
  };

  if (kmin < P) {
    r.min_i = cands[kmin].first;
    r.min_j = cands[kmin].second;
    r.min_sep = pair_str(kmin);
    r.max_overlap = !r.min_sep.empty() && r.min_sep[0] == '-' ? r.min_sep.substr(1) : "0";
  }

  std::vector<std::pair<int, int>> pc;  // structural contacts (gap <= rgap) for the rattler estimate
  std::vector<int> wc(N, 0);
  for (size_t k = 0; k < P; ++k) {
    if (contact[k]) {
      ++r.n_contacts;
      if (opt.contacts) r.contacts.push_back({cands[k].first, cands[k].second, pair_str(k)});
    }
    if (contact[k] || overlap[k] || approx[k] <= rgap) pc.push_back(cands[k]);
    if (overlap[k]) ++r.n_overlaps;
  }
  for (size_t idx = 0; idx < 4 * N; ++idx) {
    if (wcontact[idx]) {
      ++r.n_wall_contacts;
      if (opt.contacts) r.wall_contacts.push_back({static_cast<int>(idx / 4), kWallNames[idx % 4], wall_str(idx)});
    }
    if (wcontact[idx] || woutside[idx] || wapprox[idx] <= rgap) ++wc[idx / 4];
    if (woutside[idx]) ++r.n_outside;
  }
  finish_rattlers(r, n, pc, wc);

  // Worst pairs / walls by (approximate) value; strings at full precision.
  {
    std::vector<size_t> order(P);
    for (size_t k = 0; k < P; ++k) order[k] = k;
    size_t m = std::min<size_t>(10, P);
    std::partial_sort(order.begin(), order.begin() + static_cast<long>(m), order.end(),
                      [&](size_t a, size_t b) { return approx[a] < approx[b]; });
    for (size_t a = 0; a < m; ++a) r.worst_pairs.push_back({cands[order[a]].first, cands[order[a]].second, pair_str(order[a])});
    std::vector<size_t> word(4 * N);
    for (size_t k = 0; k < 4 * N; ++k) word[k] = k;
    size_t mw = std::min<size_t>(5, 4 * N);
    std::partial_sort(word.begin(), word.begin() + static_cast<long>(mw), word.end(),
                      [&](size_t a, size_t b) { return wapprox[a] < wapprox[b]; });
    for (size_t a = 0; a < mw; ++a)
      r.worst_walls.push_back({static_cast<int>(word[a] / 4), kWallNames[word[a] % 4], wall_str(word[a])});
  }

  if (r.n_overlaps > 0 || r.n_outside > 0)
    r.classification = "overlap/outside";
  else if (r.n_contacts > 0 || r.n_wall_contacts > 0)
    r.classification = "valid-with-contacts";
  else
    r.classification = "valid";

  if (opt.certify) r.cert = certify_packing(p, D, bits, cands, X, Y, s_d, opt.cert_dir);
  r.time_ms = ms_since(t0);
  return r;
}

FileResult verify_file(const std::string& path, const Options& opt) {
  auto t0 = Clock::now();
  try {
    return verify_packing(read_sqpk(path), opt);
  } catch (const std::exception& e) {
    FileResult r;
    r.path = path;
    r.error = e.what();
    r.classification = "error";
    r.time_ms = ms_since(t0);
    return r;
  }
}

// ---------------------------------------------------------------------------------------------
FileResult check_cert(const Cert& cert, const Options& opt) {
  auto t0 = Clock::now();
  FileResult r;
  r.path = cert.path;
  r.n = cert.n;
  r.claimed_s = cert.s;
  r.precise = true;
  r.precision_bits = 0;
  r.digits = 0;
  r.tol = "0";
  r.tol_nominal = "0";
  r.near = "0";
  r.rattler_gap = "0";
  const int n = cert.n;
  const size_t N = static_cast<size_t>(n);
  CertResult c;
  c.delta = "0";
  c.has_delta_exp = false;
  c.cert_file = cert.path;

  mpq_class s = rational_to_mpq(cert.s);
  if (sgn(s) <= 0) throw std::runtime_error("non-positive side");
  std::vector<ExactSquare> sq(N);
  std::vector<double> X(N), Y(N);
  for (size_t i = 0; i < N; ++i) {
    sq[i].x = rational_to_mpq(cert.squares[i][0]);
    sq[i].y = rational_to_mpq(cert.squares[i][1]);
    sq[i].t = rational_to_mpq(cert.squares[i][2]);
    set_trig_from_t(sq[i]);
    X[i] = sq[i].x.get_d();
    Y[i] = sq[i].y.get_d();
    if (!(std::fabs(X[i]) <= kMaxCoord && std::fabs(Y[i]) <= kMaxCoord))
      throw std::runtime_error("coordinate magnitude exceeds 1e4; broad-phase error bound not established");
  }
  // Same broad-phase argument as certify_packing (mpq_get_d truncates: error <= 1 ulp).
  const auto cands = candidate_pairs(X, Y, 2.0 + 1e-6);
  r.n_candidate_pairs = static_cast<long>(cands.size());
  struct Ev {
    int i, j;
    mpq_class sep;
  };
  std::vector<Ev> evs;
  for (auto [i, j] : cands) {
    const ExactSquare& a = sq[static_cast<size_t>(i)];
    const ExactSquare& b = sq[static_cast<size_t>(j)];
    mpq_class dx = b.x - a.x, dy = b.y - a.y;
    if (dx * dx + dy * dy > 2) continue;  // d2 == 2 can be an exact corner-to-corner contact
    evs.push_back({i, j, sat_sep<mpq_class>(a.x, a.y, a.C, a.S, b.x, b.y, b.C, b.S)});
  }
  r.n_near_pairs = static_cast<long>(evs.size());
  c.n_exact_pairs = r.n_near_pairs;
  std::vector<std::pair<int, int>> pc;
  std::vector<int> wc(N, 0);
  size_t best = evs.size();
  for (size_t k = 0; k < evs.size(); ++k) {
    int sg = sgn(evs[k].sep);
    if (sg < 0) ++r.n_overlaps;
    if (sg == 0) {
      ++r.n_contacts;
      pc.emplace_back(evs[k].i, evs[k].j);
      if (opt.contacts) r.contacts.push_back({evs[k].i, evs[k].j, "0"});
    }
    if (best == evs.size() || evs[k].sep < evs[best].sep) best = k;
  }
  std::vector<mpq_class> slack(4 * N);
  size_t wbest = 0;
  mpq_class xmin, xmax, ymin, ymax, t;
  for (size_t i = 0; i < N; ++i) {
    for (int w = 0; w < 4; ++w) {
      size_t idx = 4 * i + static_cast<size_t>(w);
      slack[idx] = wall_base(sq[i], s, w) - sq[i].E;
      int sg = sgn(slack[idx]);
      if (sg < 0) ++r.n_outside;
      if (sg == 0) {
        ++r.n_wall_contacts;
        ++wc[i];
        if (opt.contacts) r.wall_contacts.push_back({static_cast<int>(i), kWallNames[w], "0"});
      }
      if (slack[idx] < slack[wbest]) wbest = idx;
    }
    t = sq[i].x + sq[i].E;
    if (i == 0 || t > xmax) xmax = t;
    t = sq[i].x - sq[i].E;
    if (i == 0 || t < xmin) xmin = t;
    t = sq[i].y + sq[i].E;
    if (i == 0 || t > ymax) ymax = t;
    t = sq[i].y - sq[i].E;
    if (i == 0 || t < ymin) ymin = t;
  }
  mpq_class bw = xmax - xmin, bh = ymax - ymin;
  mpq_class bnd = bw > bh ? bw : bh;
  r.bounding_s = mpq_to_sci(bnd, 30);
  r.bounding_minus_claimed = mpq_to_sci(mpq_class(bnd - s));
  r.containment_slack = mpq_to_sci(slack[wbest]);
  if (best < evs.size()) {
    r.min_i = evs[best].i;
    r.min_j = evs[best].j;
    r.min_sep = mpq_to_sci(evs[best].sep);
    r.max_overlap = sgn(evs[best].sep) < 0 ? mpq_to_sci(mpq_class(-evs[best].sep)) : "0";
  }
  finish_rattlers(r, n, pc, wc);
  {
    std::vector<size_t> order(evs.size());
    for (size_t k = 0; k < order.size(); ++k) order[k] = k;
    size_t m = std::min<size_t>(10, order.size());
    std::partial_sort(order.begin(), order.begin() + static_cast<long>(m), order.end(),
                      [&](size_t a, size_t b) { return evs[a].sep < evs[b].sep; });
    for (size_t a = 0; a < m; ++a) r.worst_pairs.push_back({evs[order[a]].i, evs[order[a]].j, mpq_to_sci(evs[order[a]].sep)});
    std::vector<size_t> word(4 * N);
    for (size_t k = 0; k < word.size(); ++k) word[k] = k;
    size_t mw = std::min<size_t>(5, word.size());
    std::partial_sort(word.begin(), word.begin() + static_cast<long>(mw), word.end(),
                      [&](size_t a, size_t b) { return slack[a] < slack[b]; });
    for (size_t a = 0; a < mw; ++a)
      r.worst_walls.push_back({static_cast<int>(word[a] / 4), kWallNames[word[a] % 4], mpq_to_sci(slack[word[a]])});
  }
  c.passed = r.n_overlaps == 0 && r.n_outside == 0;
  c.s_cert = s.get_str();
  c.s_cert_decimal = mpq_to_decimal_ceil(s, 40);
  c.min_exact_sep = r.min_sep;
  c.min_exact_slack = r.containment_slack;
  c.n_exact_contacts = r.n_contacts;
  c.n_exact_wall_contacts = r.n_wall_contacts;
  r.classification = c.passed ? "certified" : "cert-fail";
  c.time_ms = ms_since(t0);
  r.cert = c;
  r.time_ms = ms_since(t0);
  return r;
}

FileResult check_cert_file(const std::string& path, const Options& opt) {
  auto t0 = Clock::now();
  try {
    return check_cert(read_sqcert(path), opt);
  } catch (const std::exception& e) {
    FileResult r;
    r.path = path;
    r.error = e.what();
    r.classification = "error";
    r.time_ms = ms_since(t0);
    return r;
  }
}

}  // namespace sqv
