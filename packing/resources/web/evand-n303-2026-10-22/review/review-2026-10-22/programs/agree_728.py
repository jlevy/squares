#!/usr/bin/env python3
"""Hold review_728_check.py's results to the maintained routes' and to the source's numbers.

A comparison for the review of #728 (lane c-review-728-math), written after every decider
had run. It decides nothing. It reads this lane's outputs (route-Z.json, route-C.json,
maintained-*.json), the certificate (with review_728_check.py's reader) and, as data,
the source's pipeline report s303_r303w0.json, and checks that:

  - both readers read the same side and the same 303 poses: the digest of the maintained
    adapter's checker_input, rebuilt from this lane's reader, equals the one the driver
    recorded;
  - the least wall clearance and least pair gap are equal, as exact rationals, on this
    review's route Z and route C (clearance), and on both maintained routes;
  - every route decided all n(n-1)/2 = 45,753 pairs, and the two maintained gross controls
    were refused by both maintained routes;
  - the source's stated numbers (695 close pairs, min pair separation 1.2e-12, its two
    checkers' VALID lines) agree with what was measured here.

Usage:
    python3 -I agree_728.py CERT OUTPUTS_DIR SOURCE_REPORT.json --out FILE.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review_728_check as chk  # noqa: E402


def literal(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("outputs")
    ap.add_argument("source_report")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    cert = chk.read_certificate(open(a.cert, "rb").read())
    z = json.load(open(os.path.join(a.outputs, "route-Z.json")))
    c = json.load(open(os.path.join(a.outputs, "route-C.json")))
    m = json.load(open(os.path.join(a.outputs, "maintained-positive.json")))
    dup = json.load(open(os.path.join(a.outputs, "maintained-duplicate-square-overlap.json")))
    out_ = json.load(open(os.path.join(a.outputs, "maintained-square-translated-outside-container.json")))
    src = json.load(open(a.source_report))
    ci = {
        "n": cert["n"],
        "side": literal(F(*cert["side"])),
        "poses": [[literal(F(*v)) for v in row] for row in cert["rows"]],
    }
    digest = hashlib.sha256(json.dumps(ci, sort_keys=True).encode()).hexdigest()
    n = cert["n"]
    pairs = n * (n - 1) // 2
    checks = {
        "same_side_and_poses_as_maintained_reader": digest == m["checker_input_sha256"],
        "side_same_everywhere": z["side"] == c["side"] == m["side"],
        "least_wall_clearance_equal_Z_C_sqpack_independent": z["least_wall_clearance"]
        == c["least_wall_clearance"]
        == m["exact_verify"]["minimum_containment_clearance"]
        == m["independent"]["minimum_containment_clearance"],
        "least_pair_gap_equal_Z_sqpack_independent": z["least_gap"]
        == m["exact_verify"]["minimum_best_pair_gap"]
        == m["independent"]["minimum_best_pair_gap"],
        "least_gap_squared_equals_least_squared_distance_C": F(z["least_gap"]) ** 2 == F(c["least_squared_distance"]),
        "every_pair_decided_on_all_four_routes": z["pairs_decided"]
        == c["pairs_decided"]
        == m["exact_verify"]["pairs_tested"]
        == m["independent"]["pairs_tested"]
        == pairs,
        "per_pair_decisions_identical_Z_C": z["pair_sign_digest"] == c["pair_sign_digest"],
        "all_four_routes_accept": z["accepted"]
        and c["accepted"]
        and m["exact_verify"]["verification_passed"]
        and m["independent"]["verification_passed"],
        "gross_controls_refused_by_both_maintained_routes": not any(
            r[k]["verification_passed"] for r in (dup, out_) for k in ("exact_verify", "independent")
        ),
        "source_close_pairs_equal_centre_pairs_within_sqrt2": f"({z['centre_pairs_within_sqrt2']} close pairs checked)"
        in src["checkers"]["verify_cert2"]["line"]
        and z["centre_pairs_within_sqrt2"] == c["centre_pairs_within_sqrt2"],
        "source_min_pair_separation_1.2e-12_consistent": f"{float(F(z['least_gap'])):.1e}" == "1.2e-12",
        "source_checkers_report_valid": src["checkers"]["verify_cert"]["ok"] is True
        and src["checkers"]["verify_cert2"]["ok"] is True,
        "source_report_S_cert_is_float_of_side": float(F(*cert["side"])) == float(src["S_cert"]),
    }
    record = {
        "checker_input_sha256_rebuilt": digest,
        "pairs": pairs,
        "least_wall_clearance": z["least_wall_clearance"],
        "least_pair_gap": z["least_gap"],
        "least_gap_pair_numbered_from_0": z["least_gap_pair"],
        "source_report_lines": {k: v["line"] for k, v in src["checkers"].items()},
        "checks": checks,
        "all_agree": all(checks.values()),
    }
    open(a.out, "w").write(json.dumps(record, indent=1) + "\n")
    print(json.dumps(record, indent=1))
    return 0 if record["all_agree"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
