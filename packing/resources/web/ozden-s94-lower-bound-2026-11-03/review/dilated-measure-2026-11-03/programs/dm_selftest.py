"""Self-test of this review's capture evaluators, before any of them is used.

Usage: dm_selftest.py CERTIFICATE.json.gz CONTROL_RECEIPT.json N31_CERT.json.gz N31_D529.jsonl OUT.json

1. Synthetic measures with known exact captures at oblique net angles (t = 1/2, so
   cos = 3/5 and sin = 4/5; and t = 1/7): a rectangle holding the whole square
   (density B^2), one disjoint from it (0), the half-plane through the centre (B^2/2,
   since a line through a square's centre halves it) and the quadrant at the centre
   (B^2/4, by the square's quarter-turn symmetry about its centre).
2. The certificate at directions 1, 77, 144, 277 and 599, at ten seeded poses each in
   the quadrant [L/2, U_r]^2: method 1 (clipping) and method 2 (sections) agree exactly,
   and the binary64 section method is within 1e-9 of them.
3. The census control receipt's exact capture at the least-bound leaf (direction 277),
   which the crate's oracle and the census tool computed: method 1 must equal it exactly.
4. The author's n = 31 refusal (`notes/n31-negative/d529.jsonl`). That receipt's
   summary names an input (`input_sha256`, `mass_exact`) other than the retained
   `n31_L5978.json.gz`: its masses total 31 - 7.00003e-7, the retained file's 31 - 1e-5.
   So method 1 is run on the retained file at direction 529 and the witness's exact pose,
   and its capture times the ratio of the two masses must equal the receipt's exact
   capture, which holds exactly if the receipt's input is the retained file with every
   mass scaled by that ratio; the retained file's own capture there must lie below 1.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dmlib  # noqa: E402


def synthetic(step: Fraction, index: int, core: Fraction, rects: list[tuple]) -> dmlib.ExactMeasure:
    side = Fraction(100)
    cert = dmlib.Certificate(
        n=2, side=side, core=core, step=step, last=index, rows=[], total_mass_declared=None, keys=[]
    )
    images = [dmlib.Image(Fraction(a), Fraction(b), Fraction(c), Fraction(d), Fraction(1)) for a, b, c, d in rects]
    return dmlib.ExactMeasure.of(cert, images)


def main() -> None:
    cert_path, control_path, n31_path, d529_path, out_path = (Path(a) for a in sys.argv[1:6])
    started = time.process_time()
    results: dict = {
        "program": "dm_selftest.py",
        "program_sha256": dmlib.sha256_file(Path(__file__)),
        "dmlib_sha256": dmlib.sha256_file(Path(dmlib.__file__)),
    }
    failures: list[str] = []

    # 1. synthetic cases with known answers
    cases = []
    for step, index in ((Fraction(1, 2), 1), (Fraction(1, 14), 2), (Fraction(83, 120000), 599)):
        core = Fraction(9, 10)
        cx, cy = Fraction(50), Fraction(50)
        known = {
            "whole": ((0, 0, 100, 100), core * core),
            "disjoint": ((0, 0, 10, 10), Fraction(0)),
            "half-plane through the centre": ((50, 0, 100, 100), core * core / 2),
            "quadrant at the centre": ((50, 50, 100, 100), core * core / 4),
        }
        for name, (rect, want) in known.items():
            m = synthetic(step, index, core, [rect])
            got, _ = dmlib.capture_exact(m, index, dmlib.q(cx), dmlib.q(cy))
            got2 = dmlib.capture_exact_sections(m, index, dmlib.q(cx), dmlib.q(cy))
            ok = got == dmlib.q(want) and got2 == dmlib.q(want)
            cases.append({"t": str(step * index), "case": name, "want": str(want), "method1": str(got), "method2": str(got2), "ok": ok})
            if not ok:
                failures.append(f"synthetic {name} at t = {step * index}")
    results["synthetic"] = cases

    # 2. the certificate: the two exact methods agree; binary64 is close
    cert = dmlib.certificate(dmlib.read_gzip_json(cert_path).data)
    images = dmlib.expand(cert)
    exact = dmlib.ExactMeasure.of(cert, images)
    floats = dmlib.FloatMeasure.of(cert, images)
    rng = random.Random(20261103)
    agreement = []
    worst_float = 0.0
    for index in (1, 77, 144, 277, 599):
        low, high = dmlib.domain(cert, index)
        half = cert.side / 2
        for _ in range(10):
            x = float(half) + rng.random() * float(high - half)
            y = float(half) + rng.random() * float(high - half)
            cx, cy = dmlib.exact_of_float(x), dmlib.exact_of_float(y)
            one, stats = dmlib.capture_exact(exact, index, cx, cy)
            two = dmlib.capture_exact_sections(exact, index, cx, cy)
            approx = floats.capture(index, x, y)
            error = abs(approx - float(one))
            worst_float = max(worst_float, error)
            agreement.append({"r": index, "pose": [x, y], "capture": dmlib.short(one), "methods_equal": one == two, "float_error": error, "stats": stats})
            if one != two:
                failures.append(f"methods disagree at r {index}, pose {x}, {y}")
            if error > 1e-9:
                failures.append(f"binary64 off by {error} at r {index}")
    results["certificate_poses"] = agreement
    results["worst_float_error"] = worst_float

    # 3. the census control receipt's exact capture at the least-bound leaf
    control = json.loads(control_path.read_text())
    index = int(control["index"])
    x, y = control["centre"]
    mine, _ = dmlib.capture_exact(exact, index, dmlib.exact_of_float(x), dmlib.exact_of_float(y))
    theirs = Fraction(control["exact_capture_crate"])
    results["control_least_bound_leaf"] = {
        "r": index,
        "centre": [x, y],
        "mine": dmlib.short(mine),
        "equal_to_crate_and_census_exact_capture": dmlib.fraction_of(mine) == theirs
        and Fraction(control["exact_capture_independent"]) == theirs,
    }
    if dmlib.fraction_of(mine) != theirs:
        failures.append("my exact capture at the least-bound leaf differs from the crate's")

    # 4. the author's n = 31 refusal witness
    n31 = dmlib.certificate(dmlib.read_gzip_json(n31_path).data)
    n31_exact = dmlib.ExactMeasure.of(n31, dmlib.expand(n31))
    lines = [json.loads(line) for line in d529_path.read_text().splitlines() if line.strip()]
    row = next(line for line in lines if line.get("r") == 529)
    summary = next(line for line in lines if line.get("kind") == "sqverify-fast-summary/v1")
    wx, wy = row["witness"]["exact_pose"]
    got, _ = dmlib.capture_exact(n31_exact, 529, dmlib.exact_of_float(wx), dmlib.exact_of_float(wy))
    want = Fraction(row["witness"]["exact_coverage"])
    scale = Fraction(summary["premises"]["mass_exact"]) / n31.mass
    low, high = dmlib.domain(n31, 529)
    in_domain = all(low <= Fraction(v) <= high for v in (wx, wy))
    results["n31_refusal"] = {
        "r": 529,
        "pose": [wx, wy],
        "receipt_input_sha256": summary["premises"]["input_sha256"],
        "retained_file_sha256": dmlib.read_gzip_json(n31_path).raw_sha256,
        "receipt_mass": summary["premises"]["mass_exact"],
        "retained_mass": str(n31.mass),
        "mass_ratio": str(scale),
        "receipt_capture": dmlib.short(want, 17),
        "retained_file_capture": dmlib.short(got, 17),
        "retained_file_capture_minus_1": dmlib.short(got - 1),
        "retained_capture_times_ratio_equals_receipt": dmlib.fraction_of(got) * scale == want,
        "retained_file_below_1": got < 1,
        "pose_in_per_bin_domain": in_domain,
        "distance_to_domain_end_x": dmlib.short(high - Fraction(wx)),
    }
    if dmlib.fraction_of(got) * scale != want or not got < 1:
        failures.append("the n = 31 witness does not reproduce")

    results["failures"] = failures
    results["status"] = "PASSED" if not failures else "FAILED"
    results["cpu_seconds"] = round(time.process_time() - started, 2)
    Path(out_path).write_text(dmlib.dumps(results) + "\n")
    print(json.dumps({k: results[k] for k in ("status", "failures", "worst_float_error", "control_least_bound_leaf", "n31_refusal", "cpu_seconds")}, indent=1))


if __name__ == "__main__":
    main()
