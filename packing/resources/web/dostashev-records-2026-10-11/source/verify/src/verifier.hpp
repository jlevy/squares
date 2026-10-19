// sqverify core: fast double pass, MPFR precise pass, exact GMP certificate.
// Semantics are documented at the top of sqverify.cpp and in `sqverify --help`.
#pragma once

#include <optional>
#include <string>
#include <utility>
#include <vector>

#include "sqpk.hpp"

namespace sqv {

struct Options {
  bool precise = false;
  bool certify = false;
  bool contacts = false;  // include the full contact lists in the result
  std::string tol;        // empty: default 1e-(D-3)
  std::string near;       // empty: default max(1e-6, 100 tol)
  std::string rattler_gap;  // empty: default max(tol, 1e-9); structural-contact gap for rattlers
  std::string cert_dir;   // empty: do not write certificate files
};

struct CertResult {
  bool passed = false;
  std::string delta;           // "1e-28", or "0" for --check-cert
  int delta_exp = 0;
  bool has_delta_exp = false;  // false for --check-cert (no dilation)
  std::string s_cert;          // exact p/q
  std::string s_cert_decimal;  // ceiling, 40 significant digits
  std::string min_exact_sep = "inf";
  std::string min_exact_slack;
  std::string cert_file;
  std::string error;
  long n_exact_pairs = 0;          // pairs with exact centre distance^2 <= 2
  long n_exact_contacts = 0;       // --check-cert only: sep == 0 exactly
  long n_exact_wall_contacts = 0;  // --check-cert only: slack == 0 exactly
  double time_ms = 0;
};

struct PairOut {
  int i, j;
  std::string val;
};
struct WallOut {
  int i;
  std::string wall;
  std::string val;
};

struct FileResult {
  std::string path;
  std::string error;  // empty if read and evaluated
  std::string classification;
  int n = 0;
  std::string claimed_s, exact_s;
  int digits = 0;
  std::string tol;          // tolerance actually used for classification
  std::string tol_nominal;  // 1e-(D-3) or --tol, before the double-mode floor
  std::string near;
  std::string rattler_gap;
  int precision_bits = 53;
  bool precise = false;
  std::string bounding_s, bounding_minus_claimed, containment_slack;
  std::string min_sep = "inf", max_overlap = "0";
  int min_i = -1, min_j = -1;
  long n_candidate_pairs = 0, n_near_pairs = 0, n_contacts = 0, n_wall_contacts = 0;
  long n_overlaps = 0, n_outside = 0, n_free = 0, n_rattlers = 0;
  std::vector<int> rattlers;
  std::vector<PairOut> worst_pairs, contacts;
  std::vector<WallOut> worst_walls, wall_contacts;
  std::optional<CertResult> cert;
  double time_ms = 0;

  // valid / valid-with-contacts / certified, and the certificate passed if one was attempted.
  bool ok() const;
};

FileResult verify_packing(const Packing& p, const Options& opt);
FileResult verify_file(const std::string& path, const Options& opt);
FileResult check_cert(const Cert& c, const Options& opt);
FileResult check_cert_file(const std::string& path, const Options& opt);

// Rattler estimate from a contact graph. Returns (#free, sorted rattler indices).
std::pair<long, std::vector<int>> rattler_estimate(int n, const std::vector<std::pair<int, int>>& pair_contacts,
                                                   const std::vector<int>& wall_contacts);

// Candidate pairs from a uniform grid: all pairs with centre distance^2 < r2 (computed in double).
// Cell size is max(1.5, sqrt(r2)) so pairs in non-adjacent cells are farther apart than that.
std::vector<std::pair<int, int>> candidate_pairs(const std::vector<double>& x, const std::vector<double>& y,
                                                 double r2);

}  // namespace sqv
