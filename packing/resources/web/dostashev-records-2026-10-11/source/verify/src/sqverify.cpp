// sqverify — verifier for squares-in-squares packings (.sqpk v1, see data/README.md).
//
// PASSES
//   fast (always)  Double precision. Uniform-grid broad phase (cell >= 1.5): only pairs whose
//                  centres are closer than sqrt(2) + 2*near can be within `near` of touching,
//                  because two unit squares with centres >= sqrt(2) apart have disjoint
//                  circumscribed disks. SAT separation for each candidate pair, wall slacks.
//   --precise      MPFR at max(128, ceil((D+25) log2 10)) bits. Every square's centre, angle
//                  (mpfr_sinu/cosu with u = 360, so degrees are handled exactly), wall slacks,
//                  bounding side and containment slack are recomputed from the decimal strings;
//                  pairs whose double separation is below `near` are recomputed. Double error is
//                  ~1e-13, far below near (>= 1e-6), so pairs that are not recomputed have true
//                  separation > tol and their double value is reported as is.
//   --certify      Exact rational certificate (GMP), independent of the two passes above:
//                  centres become exact rationals from the decimal strings; each angle becomes a
//                  rational half-angle tangent t ~ tan(theta/2) rounded to D+10 fractional
//                  digits, so (cos, sin) = ((1-t^2)/(1+t^2), 2t/(1+t^2)) exactly and every square
//                  is an exact unit square; the packing is dilated by f = 1 + delta (centres
//                  c -> f c, side s -> f s, i.e. dilation about the container centre with the
//                  container re-anchored at the origin; squares keep unit size). Every pair with
//                  exact centre distance^2 < 2 must have exact sep >= 0 and every wall slack must
//                  be >= 0. delta runs over 10^-k, k = max(30, D) ... 9: 1e-9 is tried first (if
//                  it fails, certification fails), then a binary search finds the smallest delta
//                  that passes; the reported delta always passed the exact check. The certified
//                  bound is s(1+delta), printed exactly (p/q) and rounded up to 40 digits.
//   --check-cert   Exact check of an existing .sqcert file (no dilation).
//
// GEOMETRY  (verify/src/geometry.hpp)
//   Square i has vertices c_i + R(theta_i)(+-1/2, +-1/2). Wall slack = min(x, y, s-x, s-y) over
//   its vertices; containment slack = min over squares. Pair separation = max over the 4 edge
//   normals of the projection gap = max_k |d.u_k| - (1 + |cos D| + |sin D|)/2 (d = centre
//   difference, D = relative angle). sep >= 0 <=> interiors disjoint; sep < 0 => penetration
//   depth -sep. Bounding side = max(x extent, y extent) of all squares, compared to claimed s.
//
// TOLERANCE  tol is an absolute length.
//   D (source digits) = the '# digits D' comment if present; else the significant digits of the
//   claimed s when s has a nonzero fractional part; else 30. D is clamped to [6, 1000].
//   Default tol = 10^-(D-3); --tol X overrides. In double-only mode (no --precise) the effective
//   tol is max(tol, 1e-12), because double cannot resolve less; the JSON field "tol" is the
//   effective value and "tol_nominal" the requested one.
//   Classification:
//     overlap/outside      some pair sep < -tol or some wall slack < -tol    (exit status 1)
//     valid-with-contacts  otherwise, and some |sep| <= tol or |slack| <= tol
//     valid                everything separated by more than tol
//     error                unreadable / malformed input                       (exit status 1)
//   A contact means "touching, or overlapping by at most tol": numerically indistinguishable at
//   the source's precision. Only --certify / --check-cert prove feasibility.
//
// RATTLERS (estimate)  Structural contact graph incl. walls: pairs / walls with gap <=
//   rattler_gap (default max(tol, 1e-9), --rattler-gap X), so that a certificate dilated by
//   ~1e-12 keeps its contact structure. free = squares with no structural contact.
//   rattlers = squares removed by iteratively pruning squares with < 3 contacts. Heuristic.
//
// JSON  --json FILE writes {"tool","version","mode","precise","certify","jobs","total_ms","files":[...]},
//   one object per input (0-based square indices); see json_out.cpp for the exact keys.

#include <mpfr.h>

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <thread>
#include <vector>

#include "json_out.hpp"
#include "numparse.hpp"
#include "verifier.hpp"

namespace {

const char* kUsage = R"(usage: sqverify [--precise] [--certify] [--cert-dir DIR] [--tol X] [--near X] [--rattler-gap X]
                [--jobs N] [--json OUT.json] [--contacts] [--quiet] FILE.sqpk...
       sqverify --check-cert [--json OUT.json] [--contacts] [--jobs N] [--quiet] FILE.sqcert...

  --precise      recheck near pairs, walls and bounding side with MPFR
                 (max(128, ceil((D+25)*log2(10))) bits)
  --certify      exact rational certificate: half-angle tangents, dilation 1+delta,
                 delta = 1e-k from 1e-max(30,D) up to 1e-9 (smallest passing is reported)
  --cert-dir DIR write DIR/<stem>.sqcert for every certified packing
  --check-cert   verify .sqcert files exactly (no dilation)
  --tol X        absolute tolerance (default 1e-(D-3); D = '# digits D', else digits of s
                 if non-integer, else 30; clamped to [6,1000]); double-only mode uses
                 max(tol, 1e-12)
  --near X       recompute pairs with double sep < X in MPFR (default max(1e-6, 100*tol))
  --rattler-gap X  gap counted as a structural contact for the rattler estimate
                 (default max(tol, 1e-9))
  --jobs N       worker threads (default 8)
  --json FILE    machine-readable report
  --contacts     include full pair / wall contact lists in the JSON
  --quiet        no per-file lines, only the summary

classification: overlap/outside (sep < -tol or slack < -tol) | valid-with-contacts
(|sep| <= tol or |slack| <= tol somewhere) | valid | error.
exit status: 0 if every file is valid / valid-with-contacts (and certified when
--certify / --check-cert), 1 otherwise, 2 on usage errors.
)";

[[noreturn]] void usage_error(const std::string& msg) {
  std::fprintf(stderr, "sqverify: %s\n\n%s", msg.c_str(), kUsage);
  std::exit(2);
}

// Shorten a number for the one-line summary, keeping any exponent ("4.5696...e+01").
std::string short_num(const std::string& s, size_t width = 24) {
  if (s.size() <= width) return s;
  size_t e = s.find_first_of("eE");
  if (e == std::string::npos) return s.substr(0, width) + "...";
  return s.substr(0, std::min(e, width)) + "..." + s.substr(e);
}

void print_line(const sqv::FileResult& r, bool check_cert) {
  if (!r.error.empty()) {
    std::printf("%s  ERROR %s\n", r.path.c_str(), r.error.c_str());
    return;
  }
  std::printf("%s  n=%d s=%s bound=%s (%s) minsep=%s maxov=%s contacts=%ld walls=%ld rattlers=%ld tol=%s %s",
              r.path.c_str(), r.n, short_num(r.claimed_s).c_str(), short_num(r.bounding_s).c_str(),
              r.bounding_minus_claimed.c_str(), r.min_sep.c_str(), r.max_overlap.c_str(), r.n_contacts,
              r.n_wall_contacts, r.n_rattlers, r.tol.c_str(), r.classification.c_str());
  if (r.cert && !check_cert) {
    const auto& c = *r.cert;
    if (c.passed)
      std::printf(" cert=PASS delta=%s s<=%s", c.delta.c_str(), c.s_cert_decimal.c_str());
    else
      std::printf(" cert=FAIL%s%s (min exact sep %s at delta=%s)", c.error.empty() ? "" : ": ", c.error.c_str(),
                  c.min_exact_sep.c_str(), c.delta.c_str());
  }
  std::printf(" %.1fms\n", r.time_ms);
}

}  // namespace

int main(int argc, char** argv) {
  sqv::Options opt;
  bool check_cert = false, quiet = false;
  int jobs = 8;
  std::string json_path;
  std::vector<std::string> files;
  for (int a = 1; a < argc; ++a) {
    std::string arg = argv[a];
    auto value = [&](const char* name) -> std::string {
      if (a + 1 >= argc) usage_error(std::string(name) + " needs a value");
      return argv[++a];
    };
    if (arg == "--help" || arg == "-h") {
      std::fputs(kUsage, stdout);
      return 0;
    } else if (arg == "--precise") {
      opt.precise = true;
    } else if (arg == "--certify") {
      opt.certify = true;
    } else if (arg == "--check-cert") {
      check_cert = true;
    } else if (arg == "--contacts") {
      opt.contacts = true;
    } else if (arg == "--quiet") {
      quiet = true;
    } else if (arg == "--cert-dir") {
      opt.cert_dir = value("--cert-dir");
    } else if (arg == "--tol") {
      opt.tol = value("--tol");
      if (!sqv::is_decimal_literal(opt.tol) || std::strtod(opt.tol.c_str(), nullptr) <= 0)
        usage_error("--tol must be a positive decimal");
    } else if (arg == "--near") {
      opt.near = value("--near");
      if (!sqv::is_decimal_literal(opt.near) || std::strtod(opt.near.c_str(), nullptr) <= 0)
        usage_error("--near must be a positive decimal");
    } else if (arg == "--rattler-gap") {
      opt.rattler_gap = value("--rattler-gap");
      if (!sqv::is_decimal_literal(opt.rattler_gap) || std::strtod(opt.rattler_gap.c_str(), nullptr) <= 0)
        usage_error("--rattler-gap must be a positive decimal");
    } else if (arg == "--jobs" || arg == "-j") {
      std::string v = value("--jobs");
      char* end = nullptr;
      long j = std::strtol(v.c_str(), &end, 10);
      if (end == v.c_str() || *end != '\0' || j < 1 || j > 256) usage_error("--jobs must be 1..256");
      jobs = static_cast<int>(j);
    } else if (arg == "--json") {
      json_path = value("--json");
    } else if (!arg.empty() && arg[0] == '-') {
      usage_error("unknown option " + arg);
    } else {
      files.push_back(arg);
    }
  }
  if (files.empty()) usage_error("no input files");
  if (check_cert && (opt.certify || opt.precise || !opt.tol.empty() || !opt.cert_dir.empty()))
    usage_error("--check-cert is exact; it takes no --precise/--certify/--tol/--cert-dir");
  if (!mpfr_buildopt_tls_p() && jobs > 1) {
    std::fprintf(stderr, "sqverify: MPFR built without thread-local storage; using 1 job\n");
    jobs = 1;
  }
  jobs = std::min<int>(jobs, static_cast<int>(files.size()));

  auto t0 = std::chrono::steady_clock::now();
  std::vector<sqv::FileResult> results(files.size());
  std::atomic<size_t> next{0};
  auto worker = [&]() {
    for (size_t k; (k = next.fetch_add(1)) < files.size();)
      results[k] = check_cert ? sqv::check_cert_file(files[k], opt) : sqv::verify_file(files[k], opt);
    mpfr_free_cache();
  };
  std::vector<std::thread> pool;
  for (int t = 1; t < jobs; ++t) pool.emplace_back(worker);
  worker();
  for (auto& th : pool) th.join();
  double total_ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();

  std::map<std::string, int> counts;
  int bad = 0, cert_pass = 0, cert_fail = 0;
  for (const auto& r : results) {
    if (!quiet) print_line(r, check_cert);
    ++counts[r.classification];
    if (!r.ok()) ++bad;
    if (r.cert) (r.cert->passed ? cert_pass : cert_fail)++;
  }
  std::printf("summary: %zu files, %.1f ms (%d jobs%s%s):", files.size(), total_ms, jobs,
              opt.precise ? ", precise" : (check_cert ? ", exact" : ", double only"), opt.certify ? ", certify" : "");
  for (const auto& [k, v] : counts) std::printf(" %s=%d", k.c_str(), v);
  if (opt.certify || check_cert) std::printf(" cert_pass=%d cert_fail=%d", cert_pass, cert_fail);
  std::printf("\n");

  if (!json_path.empty()) {
    std::ofstream o(json_path);
    sqv::RunInfo info;
    info.precise = opt.precise || check_cert;
    info.certify = opt.certify || check_cert;
    info.check_cert = check_cert;
    info.contacts = opt.contacts;
    info.jobs = jobs;
    info.total_ms = total_ms;
    sqv::write_json(o, results, info);
    o.close();
    if (!o) {
      std::fprintf(stderr, "sqverify: cannot write %s\n", json_path.c_str());
      return 1;
    }
  }
  return bad ? 1 : 0;
}
