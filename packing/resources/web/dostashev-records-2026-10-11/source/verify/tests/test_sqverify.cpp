// Unit tests for sqverify. Run one case: sqverify_tests <name>; CTest registers each case.
#include <cmath>
#include <cstdio>
#include <filesystem>
#include <functional>
#include <map>
#include <random>
#include <string>

#include "geometry.hpp"
#include "numparse.hpp"
#include "sqpk.hpp"
#include "verifier.hpp"

using namespace sqv;

namespace {

int g_failures = 0;

#define CHECK(cond)                                                          \
  do {                                                                       \
    if (!(cond)) {                                                           \
      std::fprintf(stderr, "%s:%d: CHECK failed: %s\n", __FILE__, __LINE__, #cond); \
      ++g_failures;                                                          \
    }                                                                        \
  } while (0)

std::string data(const std::string& name) { return std::string(SQV_TEST_DATA) + "/" + name; }

Options precise_opts() {
  Options o;
  o.precise = true;
  return o;
}

void dump(const FileResult& r) {
  std::fprintf(stderr, "  %s: class=%s err='%s' minsep=%s contacts=%ld walls=%ld overlaps=%ld outside=%ld tol=%s\n",
               r.path.c_str(), r.classification.c_str(), r.error.c_str(), r.min_sep.c_str(), r.n_contacts,
               r.n_wall_contacts, r.n_overlaps, r.n_outside, r.tol.c_str());
  if (r.cert)
    std::fprintf(stderr, "  cert: passed=%d delta=%s s=%s minsep=%s err='%s'\n", r.cert->passed, r.cert->delta.c_str(),
                 r.cert->s_cert_decimal.c_str(), r.cert->min_exact_sep.c_str(), r.cert->error.c_str());
}

void test_decimal_parser() {
  CHECK(decimal_to_mpq("1.5") == mpq_class(3, 2));
  CHECK(decimal_to_mpq("-0.25") == mpq_class(-1, 4));
  CHECK(decimal_to_mpq(".5") == mpq_class(1, 2));
  CHECK(decimal_to_mpq("+3.") == mpq_class(3));
  CHECK(decimal_to_mpq("1e-3") == mpq_class(1, 1000));
  CHECK(decimal_to_mpq("-1.25E+2") == mpq_class(-125));
  CHECK(decimal_to_mpq("0") == mpq_class(0));
  CHECK(decimal_to_mpq("-0.000") == mpq_class(0));
  CHECK(decimal_to_mpq("00012.0500") == mpq_class(241, 20));
  CHECK(decimal_to_mpq("1.49999999999999999999") == mpq_class(mpz_class("149999999999999999999"), pow10(20)));
  for (const char* bad : {"", ".", "1.2.3", "e5", "1e", "1e+", "--1", "1x", " 1", "1 ", "nan", "inf", "1e100000", "0x10"}) {
    CHECK(!is_decimal_literal(bad));
    bool threw = false;
    try {
      decimal_to_mpq(bad);
    } catch (const std::invalid_argument&) {
      threw = true;
    }
    CHECK(threw);
  }
  // Every literal form we accept must also be accepted (whole string) by MPFR's parser.
  for (const char* good : {"1.5", "-0.25", ".5", "+3.", "1e-3", "-1.25E+2", "0", "-0.000", "00012.0500", "7.", "-.5e+1"}) {
    CHECK(is_decimal_literal(good));
    mpfr_t x;
    mpfr_init2(x, 200);
    CHECK(mpfr_set_str(x, good, 10, MPFR_RNDN) == 0);
    mpfr_t y;
    mpfr_init2(y, 200);
    mpfr_set_q(y, decimal_to_mpq(good).get_mpq_t(), MPFR_RNDN);
    CHECK(mpfr_equal_p(x, y));
    mpfr_clear(x);
    mpfr_clear(y);
  }
  CHECK(significant_digits("0.00120") == 3);
  CHECK(significant_digits("6.59861960924436011617837046268") == 30);
  CHECK(significant_digits("12") == 2);
  CHECK(significant_digits("0") == 1);
  CHECK(mpq_to_decimal_ceil(mpq_class(1, 3), 5) == "0.33334");
  CHECK(mpq_to_decimal_ceil(mpq_class(-1, 3), 5) == "-0.33333");
  CHECK(mpq_to_decimal_ceil(mpq_class(7), 40) == "7");
  CHECK(mpq_to_decimal_ceil(mpq_class(2, 3), 3) == "0.667");
  CHECK(mpq_to_decimal_ceil(mpq_class(1001, 1000), 3) == "1.01");
  CHECK(mpq_to_decimal_ceil(mpq_class(1, 300), 2) == "0.0034");
}

void test_rational_parser() {
  CHECK(rational_to_mpq("3/6") == mpq_class(1, 2));
  CHECK(rational_to_mpq("-7/2") == mpq_class(-7, 2));
  CHECK(rational_to_mpq("0/1") == mpq_class(0));
  CHECK(rational_to_mpq("2.5") == mpq_class(5, 2));
  CHECK(rational_to_mpq("12") == mpq_class(12));
  for (const char* bad : {"1/0", "1/", "/2", "1/-2", "1.5/2", "1//2", "a/b", "1/2/3"}) CHECK(!is_rational_literal(bad));
}

void test_sat_formula_vs_bruteforce() {
  std::mt19937_64 rng(12345);
  std::uniform_real_distribution<double> pos(-1.5, 1.5), ang(-3.2, 3.2);
  double worst = 0;
  int overlapping = 0;
  for (int k = 0; k < 200000; ++k) {
    double ax = 0, ay = 0, tha = ang(rng), bx = pos(rng), by = pos(rng), thb = ang(rng);
    double f = sat_sep<double>(ax, ay, std::cos(tha), std::sin(tha), bx, by, std::cos(thb), std::sin(thb));
    double g = sat_sep_bruteforce(ax, ay, tha, bx, by, thb);
    worst = std::max(worst, std::fabs(f - g));
    if (f < 0) ++overlapping;
  }
  std::fprintf(stderr, "  max |formula - bruteforce| = %.3e over 200000 pairs (%d overlapping)\n", worst, overlapping);
  CHECK(worst < 1e-12);
  CHECK(overlapping > 1000);
  // Known values.
  CHECK(std::fabs(sat_sep<double>(0, 0, 1, 0, 1, 0, 1, 0)) < 1e-15);        // side by side: touching
  CHECK(std::fabs(sat_sep<double>(0, 0, 1, 0, 0.9, 0, 1, 0) + 0.1) < 1e-15);  // overlap 0.1
  CHECK(std::fabs(sat_sep<double>(0, 0, 1, 0, 1, 1, 1, 0)) < 1e-15);        // corner to corner
}

void test_trivial_grid() {
  for (bool precise : {false, true}) {
    Options o;
    o.precise = precise;
    o.certify = true;
    FileResult r = verify_file(data("grid9.sqpk"), o);
    dump(r);
    CHECK(r.error.empty());
    CHECK(r.classification == "valid-with-contacts");
    CHECK(r.n_contacts == 20);  // 6 horizontal + 6 vertical + 8 diagonal corner touches
    CHECK(r.n_wall_contacts == 12);
    CHECK(r.n_overlaps == 0 && r.n_outside == 0);
    CHECK(r.n_rattlers == 0 && r.n_free == 0);
    CHECK(r.min_sep == "0");
    CHECK(r.cert && r.cert->passed);
    CHECK(r.cert && r.cert->delta == "1e-30");  // integer s -> D = 30 -> smallest rung passes
    CHECK(r.ok());
  }
}

void test_goebel5() {
  Options o = precise_opts();
  o.certify = true;
  auto dir = std::filesystem::temp_directory_path() / "sqverify_test_goebel";
  std::filesystem::remove_all(dir);
  o.cert_dir = dir.string();
  FileResult r = verify_file(data("goebel5.sqpk"), o);
  dump(r);
  CHECK(r.error.empty());
  CHECK(r.digits == 40);
  CHECK(r.tol == "1e-37");
  CHECK(r.classification == "valid-with-contacts");
  CHECK(r.n_contacts == 4);       // tilted square touches each corner square
  CHECK(r.n_wall_contacts == 8);  // corner squares touch two walls each
  CHECK(r.n_rattlers == 0);
  CHECK(r.exact_s == "2+sqrt(2)/2");
  CHECK(r.cert && r.cert->passed);
  if (r.cert) {
    CHECK(r.cert->has_delta_exp && r.cert->delta_exp <= -9);
    mpq_class sc = rational_to_mpq(r.cert->s_cert);
    CHECK(sc >= decimal_to_mpq(r.claimed_s));
    CHECK(sc - decimal_to_mpq(r.claimed_s) <= mpq_class(1, 100000000));
    CHECK(decimal_to_mpq(r.cert->s_cert_decimal) >= sc);
    CHECK(!r.cert->cert_file.empty());
  }
  // Double-only pass agrees on the classification.
  FileResult d = verify_file(data("goebel5.sqpk"), Options{});
  dump(d);
  CHECK(d.classification == "valid-with-contacts" && d.tol == "1e-12");
}

void test_overlap_pair() {
  for (bool precise : {false, true}) {
    Options o;
    o.precise = precise;
    FileResult r = verify_file(data("overlap_pair.sqpk"), o);
    dump(r);
    CHECK(r.classification == "overlap/outside");
    CHECK(r.n_overlaps == 1);
    CHECK(std::fabs(std::strtod(r.max_overlap.c_str(), nullptr) - 0.1) < 1e-12);
    CHECK(!r.ok());
  }
}

void test_poking_out() {
  for (bool precise : {false, true}) {
    Options o;
    o.precise = precise;
    FileResult r = verify_file(data("poking_out.sqpk"), o);
    dump(r);
    CHECK(r.classification == "overlap/outside");
    CHECK(r.n_outside == 2);  // right and top walls
    CHECK(r.n_overlaps == 0);
    // 30 deg extent = (cos30 + sin30)/2 = 0.6830127..., centre 2.5 -> slack 3 - 3.1830127 = -0.1830127
    CHECK(std::fabs(std::strtod(r.containment_slack.c_str(), nullptr) + 0.18301270189221932) < 1e-12);
    CHECK(!r.ok());
  }
}

void test_overlap_1e20_axis() {
  FileResult d = verify_file(data("overlap_1e20_axis.sqpk"), Options{});
  dump(d);
  CHECK(d.classification == "valid-with-contacts");  // double cannot see 1e-20
  CHECK(d.n_overlaps == 0);
  FileResult p = verify_file(data("overlap_1e20_axis.sqpk"), precise_opts());
  dump(p);
  CHECK(p.classification == "overlap/outside");
  CHECK(p.n_overlaps == 1);
  CHECK(std::fabs(std::strtod(p.max_overlap.c_str(), nullptr) / 1e-20 - 1) < 1e-15);
  Options c;
  c.certify = true;
  FileResult q = verify_file(data("overlap_1e20_axis.sqpk"), c);
  dump(q);
  CHECK(q.cert && q.cert->passed);  // a 1e-20 overlap is fixed by a dilation of ~1e-20
  CHECK(q.cert && q.cert->delta_exp >= -20);
}

void test_overlap_1e20_rotated() {
  FileResult d = verify_file(data("overlap_1e20_rotated.sqpk"), Options{});
  dump(d);
  CHECK(d.classification == "valid-with-contacts");
  FileResult p = verify_file(data("overlap_1e20_rotated.sqpk"), precise_opts());
  dump(p);
  CHECK(p.classification == "overlap/outside");
  CHECK(std::fabs(std::strtod(p.max_overlap.c_str(), nullptr) / 1e-20 - 1) < 1e-12);
}

void test_touching_rotated() {
  FileResult p = verify_file(data("touching_rotated.sqpk"), precise_opts());
  dump(p);
  CHECK(p.classification == "valid-with-contacts");
  CHECK(p.n_contacts == 1 && p.n_wall_contacts == 0);
  CHECK(std::fabs(std::strtod(p.min_sep.c_str(), nullptr)) < 1e-45);
  CHECK(p.n_free == 0 && p.n_rattlers == 2);  // one contact each: both are loose
}

void test_single_free_square() {
  Options o = precise_opts();
  o.certify = true;
  FileResult r = verify_file(data("single_free.sqpk"), o);
  dump(r);
  CHECK(r.classification == "valid");
  CHECK(r.n_free == 1 && r.n_rattlers == 1);
  CHECK(r.min_sep == "inf" && r.min_i == -1);
  CHECK(r.cert && r.cert->passed);
}

void test_certify_rejects_overlap() {
  Options o = precise_opts();
  o.certify = true;
  FileResult r = verify_file(data("overlap_1e3.sqpk"), o);
  dump(r);
  CHECK(r.classification == "overlap/outside");
  CHECK(r.cert && !r.cert->passed);
  CHECK(r.cert && r.cert->delta == "1e-9");
  CHECK(r.cert && r.cert->min_exact_sep[0] == '-');
  CHECK(!r.ok());
  // Also overlap_pair and poking_out.
  for (const char* f : {"overlap_pair.sqpk", "poking_out.sqpk"}) {
    FileResult q = verify_file(data(f), o);
    CHECK(q.cert && !q.cert->passed);
  }
}

void test_certify_roundtrip_check_cert() {
  auto dir = std::filesystem::temp_directory_path() / "sqverify_test_roundtrip";
  std::filesystem::remove_all(dir);
  Options o;
  o.certify = true;
  o.cert_dir = dir.string();
  for (const char* f : {"goebel5.sqpk", "grid9.sqpk", "touching_rotated.sqpk", "overlap_1e20_rotated.sqpk"}) {
    FileResult r = verify_file(data(f), o);
    dump(r);
    CHECK(r.cert && r.cert->passed && !r.cert->cert_file.empty());
    if (!r.cert || r.cert->cert_file.empty()) continue;
    FileResult c = check_cert_file(r.cert->cert_file, Options{});
    dump(c);
    CHECK(c.classification == "certified");
    CHECK(c.cert && c.cert->passed);
    CHECK(c.n_contacts == 0);  // dilation opened every contact
    CHECK(c.cert && c.cert->s_cert == r.cert->s_cert);
  }
}

void test_check_cert_good() {
  FileResult c = check_cert_file(data("grid4.sqcert"), Options{});
  dump(c);
  CHECK(c.classification == "certified");
  CHECK(c.n_contacts == 6);  // 2 horizontal + 2 vertical + 2 diagonal, all exactly 0
  CHECK(c.n_wall_contacts == 8);
  CHECK(c.cert && c.cert->n_exact_contacts == 6);
  CHECK(c.ok());
}

void test_check_cert_bad() {
  FileResult c = check_cert_file(data("grid4_bad.sqcert"), Options{});
  dump(c);
  CHECK(c.classification == "cert-fail");
  CHECK(c.n_overlaps >= 1);
  CHECK(c.min_sep[0] == '-');
  CHECK(!c.ok());
}

void test_check_cert_pythagorean() {
  FileResult c = check_cert_file(data("pythagorean.sqcert"), Options{});
  dump(c);
  CHECK(c.classification == "certified");
  CHECK(c.n_wall_contacts == 4);
  CHECK(c.bounding_minus_claimed == "0");
}

void test_malformed_input() {
  FileResult r = verify_file(data("malformed.sqpk"), Options{});
  dump(r);
  CHECK(r.classification == "error" && !r.error.empty() && !r.ok());
  FileResult m = verify_file(data("does_not_exist.sqpk"), Options{});
  CHECK(m.classification == "error");
  for (const char* text : {"n 2\ns 2\n0.5 0.5 0\n", "n 1\ns abc\n0.5 0.5 0\n", "n 1\n0.5 0.5 0\ns 2\n",
                           "n 1\ns 2\n0.5 0.5\n", "n 1\ns 2\n0.5 0.5 0 1\n", "s 2\n0.5 0.5 0\n", "n 0\ns 1\n",
                           "n 1\nn 1\ns 1\n0.5 0.5 0\n", "n 1\ns 1\n0.5 0.5 1e99999\n"}) {
    bool threw = false;
    try {
      parse_sqpk(text, "inline");
    } catch (const std::runtime_error&) {
      threw = true;
    }
    if (!threw) std::fprintf(stderr, "  accepted malformed input: %s\n", text);
    CHECK(threw);
  }
  Packing ok = parse_sqpk("# sqpk v1\r\n# digits 33\r\nn 1\r\ns 1\r\n# c\r\n  0.5\t0.5  0  \r\n", "inline");
  CHECK(ok.n == 1 && ok.digits == 33 && ok.squares[0][1] == "0.5");
  Packing free_text = parse_sqpk("# digits of s truncated at 30\n#digits 12\nn 1\ns 1\n0.5 0.5 0\n", "inline");
  CHECK(free_text.digits == 12);
}

}  // namespace

int main(int argc, char** argv) {
  std::map<std::string, std::function<void()>> tests = {
      {"decimal_parser", test_decimal_parser},
      {"rational_parser", test_rational_parser},
      {"sat_formula_vs_bruteforce", test_sat_formula_vs_bruteforce},
      {"trivial_grid", test_trivial_grid},
      {"goebel5", test_goebel5},
      {"overlap_pair", test_overlap_pair},
      {"poking_out", test_poking_out},
      {"overlap_1e20_axis", test_overlap_1e20_axis},
      {"overlap_1e20_rotated", test_overlap_1e20_rotated},
      {"touching_rotated", test_touching_rotated},
      {"single_free_square", test_single_free_square},
      {"certify_rejects_overlap", test_certify_rejects_overlap},
      {"certify_roundtrip_check_cert", test_certify_roundtrip_check_cert},
      {"check_cert_good", test_check_cert_good},
      {"check_cert_bad", test_check_cert_bad},
      {"check_cert_pythagorean", test_check_cert_pythagorean},
      {"malformed_input", test_malformed_input},
  };
  std::vector<std::string> run;
  if (argc > 1) {
    for (int a = 1; a < argc; ++a) run.push_back(argv[a]);
  } else {
    for (const auto& [k, v] : tests) run.push_back(k);
  }
  for (const auto& name : run) {
    auto it = tests.find(name);
    if (it == tests.end()) {
      std::fprintf(stderr, "unknown test %s\n", name.c_str());
      return 2;
    }
    int before = g_failures;
    it->second();
    std::fprintf(stderr, "%s: %s\n", name.c_str(), g_failures == before ? "ok" : "FAILED");
  }
  return g_failures ? 1 : 0;
}
