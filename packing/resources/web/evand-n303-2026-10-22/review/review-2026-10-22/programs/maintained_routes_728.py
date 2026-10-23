#!/usr/bin/env python3
"""Run this repository's two maintained exact routes on one evand-format certificate.

A premise-check driver for the review of #728, written after review_728_check.py had
decided the certificate. It decides nothing of its own: it reaches the two maintained
routes the way `devtools.upper_bound_reports certify` reaches them for an evand
certificate, through the `evand-cert` adapter (`upper_bound_reports.evand_cert`, which
calls `evand_exact_certificates.parse`) and the kernel's `run_case` and `validate_job`
(`devtools.evand_arrangement_reports`), and prints each route's verdict and its least
wall clearance and pair gap, exactly.

Usage, with the project interpreter (Python 3.14):
    python3 -I maintained_routes_728.py --packing /path/to/squares/packing \
        CERT --n 303 --control positive [--sharp] [--out FILE.json]

--control is one of the kernel's JOBS (positive, duplicate-square-overlap,
square-translated-outside-container). --sharp also runs the kernel's own `run_sharp`
controls (at contact and past it) on the certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from fractions import Fraction

PREFIX = "W-evand-728-n"
LIMITS = "Review 728 driver: Evan Daniel's rational certificate, decided by the maintained routes."


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("--packing", required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--control", default="positive")
    ap.add_argument("--sharp", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    sys.path.insert(0, args.packing)
    from devtools import evand_arrangement_reports as kernel
    from devtools import upper_bound_reports as ubr

    raw = open(args.cert, "rb").read()
    out: dict = {"certificate_sha256": hashlib.sha256(raw).hexdigest(), "control": args.control}
    try:
        cert = ubr.evand_cert(raw, args.n, {})
    except Exception as exc:  # the adapter's refusal is the result
        out["adapter"] = f"refused: {type(exc).__name__}: {exc}"
        print(json.dumps(out, indent=1))
        if args.out:
            open(args.out, "w").write(json.dumps(out, indent=1) + "\n")
        return 2
    out["adapter"] = "read"
    started = time.monotonic()
    row = kernel.run_case(cert, args.control, witness_prefix=PREFIX, claim_limitations=LIMITS)
    try:
        kernel.validate_job(row, cert, args.control, witness_prefix=PREFIX, claim_limitations=LIMITS)
        out["validate_job"] = "passed"
    except Exception as exc:
        out["validate_job"] = f"refused: {type(exc).__name__}: {exc}"
    out["wall_seconds"] = round(time.monotonic() - started, 2)
    out["cpu_seconds"] = {k: round(v, 2) for k, v in row["cpu_seconds"].items()}
    ci = row["checker_input"]
    out["checker_input_sha256"] = hashlib.sha256(json.dumps(ci, sort_keys=True).encode()).hexdigest()
    out["side"] = ci["side"]
    for route in kernel.ROUTES:
        v = row[route]
        keys = sorted(v)
        out[route] = {
            "keys": keys,
            "verification_passed": v.get("verification_passed"),
            "pairs_tested": v.get("pairs_tested"),
            "minimum_containment_clearance": v.get("minimum_containment_clearance"),
            "minimum_best_pair_gap": v.get("minimum_best_pair_gap"),
            "failures": v.get("failures", [])[:5],
            "failure_count": len(v.get("failures", [])),
        }
        for extra in ("touching_pairs", "contacts", "minimum_pair", "tightest_pair", "near_pairs"):
            if extra in v:
                out[route][extra] = v[extra]
    if args.sharp:
        sharp = {}
        for control in kernel.SHARP_CONTROLS:
            for past in (False, True):
                res = kernel.run_sharp(cert, control, past=past, witness_prefix=PREFIX, claim_limitations=LIMITS)
                sharp[f"{control}{' past' if past else ' at contact'}"] = {
                    r: {"passed": d["passed"], "wall": str(d["wall"]), "gap": str(d["gap"])} for r, d in res.items()
                }
        out["kernel_run_sharp"] = sharp
    text = json.dumps(out, indent=1, default=str)
    if args.out:
        open(args.out, "w").write(text + "\n")
    brief = {
        "control": args.control,
        "validate_job": out["validate_job"],
        **{
            r: {
                "passed": out[r]["verification_passed"],
                "pairs": out[r]["pairs_tested"],
                "wall": out[r]["minimum_containment_clearance"],
                "gap": out[r]["minimum_best_pair_gap"],
                "failures": out[r]["failure_count"],
            }
            for r in kernel.ROUTES
        },
    }
    print(json.dumps(brief, indent=1))
    passed = all(out[r]["verification_passed"] for r in kernel.ROUTES)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
