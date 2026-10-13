// JSON report writer for sqverify (schema documented in sqverify.cpp).
#pragma once

#include <ostream>
#include <vector>

#include "verifier.hpp"

namespace sqv {

struct RunInfo {
  bool precise = false;
  bool certify = false;
  bool check_cert = false;
  bool contacts = false;
  int jobs = 1;
  double total_ms = 0;
};

void write_json(std::ostream& os, const std::vector<FileResult>& results, const RunInfo& info);

}  // namespace sqv
