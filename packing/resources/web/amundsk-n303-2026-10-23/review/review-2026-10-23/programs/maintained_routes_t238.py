#!/usr/bin/env python3
"""Run this repository's two maintained exact routes on the issue 755 certificate.

Written for the stage 4 review of T-238 (bead think-jdz0) after the review's own checker,
`review_t238_check.py`, had decided. A premise check: it decides nothing itself. The
deciding is done by the maintained routes it calls, `sqpack.witness.exact_verify` on the
kernel's `center-basis` witness (`V-sqpack-verify`) and
`devtools.check_rational_witness_independent.check_squares` on the kernel's corners
(`V-check-rational-witness-independent`).

The certificate's bytes are read through the `evand-cert` adapter of
`devtools.upper_bound_reports` (`evand_cert`, which calls
`devtools.evand_exact_certificates.parse`). Then, for each job of the kernel's roster
(`positive`, `duplicate-square-overlap`, `square-translated-outside-container`), it calls
`devtools.evand_arrangement_reports.decide_job` with the witness prefix and claim
limitations of the records lane's declaration, as the child of `upper_bound_reports
certify` does: `run_case`, then `validate_job`, then the row is written. The one
difference from `certify` is the input: `certify`'s child reads the packet's derived fact,
and this program reads the certificate's own bytes, so that `agree_t238.py` can hold the
fact's round trip to them through the two `checker_input` blocks.

With `--sharp` it also runs the kernel's `run_sharp` for both `SHARP_CONTROLS`, at exact
contact (`past=False`) and 1e-30 past it (`past=True`).

Usage, from anywhere, with the project interpreter:
  python3 -I -B maintained_routes_t238.py CERT --packing /home/user/squares/packing \
      --declaration report.json --out DIR [--sharp]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("--packing", required=True)
    ap.add_argument("--declaration", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sharp", action="store_true")
    args = ap.parse_args()
    sys.path.insert(0, str(Path(args.packing).resolve()))
    from devtools import evand_arrangement_reports as kernel  # noqa: PLC0415
    from devtools import upper_bound_reports as reports  # noqa: PLC0415

    raw = Path(args.cert).read_bytes()
    declaration = json.loads(Path(args.declaration).read_text())
    profile = {
        "witness_prefix": declaration["witness_prefix"],
        "claim_limitations": declaration["claim_limitations"],
    }
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    certificate = reports.evand_cert(raw, 303, {})
    summary: dict = {
        "program": "maintained_routes_t238.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "python": platform.python_version(),
        "kernel_sha256": hashlib.sha256(Path(kernel.__file__).read_bytes()).hexdigest(),
        "reports_sha256": hashlib.sha256(Path(reports.__file__).read_bytes()).hexdigest(),
        "profile": profile,
        "jobs": {},
        "sharp": {},
    }
    for control in kernel.JOBS:
        path = out / f"n303-{control}.json"
        if path.exists():
            path.unlink()
        started = time.perf_counter()
        kernel.decide_job(certificate, control, path, **profile)
        row = json.loads(path.read_text())
        with lzma.open(out / f"n303-{control}.json.xz", "wb") as stream:
            stream.write(path.read_bytes())
        path.unlink()
        summary["jobs"][control] = {
            "validated": True,
            "routes": {
                route: {
                    "passed": row[route]["verification_passed"],
                    "pairs_tested": row[route]["pairs_tested"],
                    "minimum_containment_clearance": row[route]["minimum_containment_clearance"],
                    "minimum_best_pair_gap": row[route]["minimum_best_pair_gap"],
                    "failures": len(row[route]["failures"]),
                    "cpu_seconds": round(row["cpu_seconds"][route], 3),
                }
                for route in kernel.ROUTES
            },
            "checker_input_sha256": hashlib.sha256(
                json.dumps(row["checker_input"], sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest(),
            "wall_seconds": round(time.perf_counter() - started, 2),
        }
        print(control, json.dumps(summary["jobs"][control]["routes"])[:400])
    if args.sharp:
        left, right, gap, normal = kernel.legacy.tightest_pair(certificate)
        summary["tightest_pair"] = {
            "left": left,
            "right": right,
            "gap": kernel.legacy.literal(gap),
            "normal": [kernel.legacy.literal(v) for v in normal],
        }
        summary["top_clearance"] = kernel.legacy.literal(kernel.legacy.top_clearance(certificate))
        for control in kernel.SHARP_CONTROLS:
            for past in (False, True):
                started = time.perf_counter()
                result = kernel.run_sharp(certificate, control, past=past, **profile)
                summary["sharp"][f"{control}:{'past' if past else 'contact'}"] = {
                    route: {
                        "passed": v["passed"],
                        "wall": f"{Fraction(v['wall']).numerator}/{Fraction(v['wall']).denominator}",
                        "gap": f"{Fraction(v['gap']).numerator}/{Fraction(v['gap']).denominator}",
                    }
                    for route, v in result.items()
                } | {"wall_seconds": round(time.perf_counter() - started, 2)}
                print(control, "past" if past else "contact", {r: v["passed"] for r, v in result.items()})
    (out / "maintained-routes.json").write_text(json.dumps(summary, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
