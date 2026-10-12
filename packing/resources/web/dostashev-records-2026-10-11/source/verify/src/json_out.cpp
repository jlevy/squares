#include "json_out.hpp"

#include <cstdio>
#include <string>

namespace sqv {
namespace {

std::string q(const std::string& s) {
  std::string o = "\"";
  for (unsigned char c : s) {
    switch (c) {
      case '"': o += "\\\""; break;
      case '\\': o += "\\\\"; break;
      case '\n': o += "\\n"; break;
      case '\r': o += "\\r"; break;
      case '\t': o += "\\t"; break;
      default:
        if (c < 0x20) {
          char buf[8];
          std::snprintf(buf, sizeof buf, "\\u%04x", c);
          o += buf;
        } else {
          o += static_cast<char>(c);
        }
    }
  }
  return o + "\"";
}

std::string num(double x) {
  char buf[40];
  std::snprintf(buf, sizeof buf, "%.3f", x);
  return buf;
}

const char* b(bool v) { return v ? "true" : "false"; }

void pairs(std::ostream& os, const std::vector<PairOut>& v) {
  os << "[";
  for (size_t k = 0; k < v.size(); ++k)
    os << (k ? "," : "") << "[" << v[k].i << "," << v[k].j << "," << q(v[k].val) << "]";
  os << "]";
}

void walls(std::ostream& os, const std::vector<WallOut>& v) {
  os << "[";
  for (size_t k = 0; k < v.size(); ++k)
    os << (k ? "," : "") << "[" << v[k].i << "," << q(v[k].wall) << "," << q(v[k].val) << "]";
  os << "]";
}

void file(std::ostream& os, const FileResult& r, const RunInfo& info) {
  os << "  {\"path\":" << q(r.path) << ",\"n\":" << r.n << ",\"claimed_s\":" << q(r.claimed_s)
     << ",\"exact_s\":" << (r.exact_s.empty() ? "null" : q(r.exact_s)) << ",\"digits\":" << r.digits
     << ",\"tol\":" << q(r.tol) << ",\"tol_nominal\":" << q(r.tol_nominal) << ",\"near\":" << q(r.near) << ",\"rattler_gap\":" << q(r.rattler_gap)
     << ",\"precise\":" << b(r.precise) << ",\"precision_bits\":" << r.precision_bits
     << ",\n   \"bounding_s\":" << q(r.bounding_s) << ",\"bounding_minus_claimed\":" << q(r.bounding_minus_claimed)
     << ",\"containment_slack\":" << q(r.containment_slack) << ",\"min_sep\":" << q(r.min_sep)
     << ",\"max_overlap\":" << q(r.max_overlap) << ",\"min_sep_pair\":";
  if (r.min_i >= 0)
    os << "[" << r.min_i << "," << r.min_j << "]";
  else
    os << "null";
  os << ",\n   \"n_candidate_pairs\":" << r.n_candidate_pairs << ",\"n_near_pairs\":" << r.n_near_pairs
     << ",\"n_contacts\":" << r.n_contacts << ",\"n_wall_contacts\":" << r.n_wall_contacts
     << ",\"n_overlaps\":" << r.n_overlaps << ",\"n_outside\":" << r.n_outside << ",\"n_free\":" << r.n_free
     << ",\"n_rattlers\":" << r.n_rattlers << ",\"rattlers\":[";
  for (size_t k = 0; k < r.rattlers.size(); ++k) os << (k ? "," : "") << r.rattlers[k];
  os << "],\n   \"classification\":" << q(r.classification) << ",\"error\":" << (r.error.empty() ? "null" : q(r.error))
     << ",\"time_ms\":" << num(r.time_ms) << ",\n   \"worst_pairs\":";
  pairs(os, r.worst_pairs);
  os << ",\n   \"worst_walls\":";
  walls(os, r.worst_walls);
  if (info.contacts) {
    os << ",\n   \"contacts\":";
    pairs(os, r.contacts);
    os << ",\n   \"wall_contacts\":";
    walls(os, r.wall_contacts);
  }
  os << ",\n   \"certify\":";
  if (!r.cert) {
    os << "null";
  } else {
    const CertResult& c = *r.cert;
    os << "{\"passed\":" << b(c.passed) << ",\"delta\":" << q(c.delta) << ",\"delta_exp\":";
    if (c.has_delta_exp)
      os << c.delta_exp;
    else
      os << "null";
    os << ",\"s_cert\":" << q(c.s_cert) << ",\"s_cert_decimal\":" << q(c.s_cert_decimal)
       << ",\"min_exact_sep\":" << q(c.min_exact_sep) << ",\"min_exact_slack\":" << q(c.min_exact_slack)
       << ",\"n_exact_pairs\":" << c.n_exact_pairs << ",\"n_exact_contacts\":" << c.n_exact_contacts
       << ",\"n_exact_wall_contacts\":" << c.n_exact_wall_contacts
       << ",\"cert_file\":" << (c.cert_file.empty() ? "null" : q(c.cert_file))
       << ",\"error\":" << (c.error.empty() ? "null" : q(c.error)) << ",\"time_ms\":" << num(c.time_ms) << "}";
  }
  os << "}";
}

}  // namespace

void write_json(std::ostream& os, const std::vector<FileResult>& results, const RunInfo& info) {
  os << "{\"tool\":\"sqverify\",\"version\":1,\"mode\":" << q(info.check_cert ? "check-cert" : "verify")
     << ",\"precise\":" << b(info.precise) << ",\"certify\":" << b(info.certify) << ",\"jobs\":" << info.jobs
     << ",\"total_ms\":" << num(info.total_ms) << ",\n \"files\":[\n";
  for (size_t k = 0; k < results.size(); ++k) {
    file(os, results[k], info);
    os << (k + 1 < results.size() ? ",\n" : "\n");
  }
  os << " ]}\n";
}

}  // namespace sqv
