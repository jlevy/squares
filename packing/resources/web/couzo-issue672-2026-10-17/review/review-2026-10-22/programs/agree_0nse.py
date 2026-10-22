#!/usr/bin/env python3
"""Hold this review's checker output to the packets' retained receipts; decides nothing.

For each certificate: every pose of the receipt's positive `checker_input` against the
row this review's reader read (as rationals), the side, the pair count, and the least
wall clearance and least pair gap of both maintained routes against both of this
review's routes. Also lists each receipt's controls and their verdicts.

Usage: python -I agree_0nse.py OUT.json CHECK.json[,CHECK.json] LABEL=N=CERT=RECEIPT ...
"""

from __future__ import annotations

import importlib.util
import json
import lzma
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("review_0nse_check", HERE / "review_0nse_check.py")
mine = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mine)


def main(argv: list[str]) -> int:
    out_path = Path(argv[1])
    checks: dict = {}
    for path in argv[2].split(","):
        checks |= json.loads(Path(path).read_text(encoding="utf-8"))
    report = {}
    every = True
    for spec in argv[3:]:
        label, n, cert, receipt = spec.split("=", 3)
        n = int(n)
        _, side, rows, _ = mine.read(Path(cert).read_bytes().decode("ascii"))
        record = json.loads(lzma.open(receipt).read())
        cases = [c for c in record["cases"] if c["n"] == n]
        positive = next(c for c in cases if c["control"] == "positive")
        poses = positive["checker_input"]["poses"]
        poses_equal = len(poses) == len(rows) and all(
            tuple(Fraction(v) for v in pose) == tuple(Fraction(p, q) for p, q in row)
            for pose, row in zip(poses, rows)
        )
        side_equal = Fraction(positive["checker_input"]["side"]) == Fraction(*side)
        mine_row = checks[label]
        z, c = mine_row["route_Z"], mine_row["route_C"]
        fields = {}
        for route in ("exact_verify", "independent"):
            r = positive[route]
            fields[route] = {
                "passed": r["verification_passed"],
                "pairs_tested": r["pairs_tested"],
                "least_wall": r["minimum_containment_clearance"],
                "least_gap": r["minimum_best_pair_gap"],
                "wall_equal_Z": Fraction(r["minimum_containment_clearance"]) == Fraction(z["least_wall_clearance"]),
                "wall_equal_C": Fraction(r["minimum_containment_clearance"]) == Fraction(c["least_wall_clearance"]),
                "gap_equal_Z": Fraction(r["minimum_best_pair_gap"]) == Fraction(z["least_gap"]),
                "pairs_equal": r["pairs_tested"] == z["pairs_decided"] == c["pairs_clipped"] == n * (n - 1) // 2,
                "side_equal": Fraction(r["side"]) == Fraction(*side),
            }
        controls = {
            case["control"]: {
                route: {"passed": case[route]["verification_passed"], "failures": [str(f)[:120] for f in case[route]["failures"][:2]]}
                for route in ("exact_verify", "independent")
            }
            for case in cases
            if case["control"] != "positive"
        }
        ok = poses_equal and side_equal and all(
            v["passed"] and v["wall_equal_Z"] and v["wall_equal_C"] and v["gap_equal_Z"] and v["pairs_equal"] and v["side_equal"]
            for v in fields.values()
        ) and all(not route["passed"] for control in controls.values() for route in control.values())
        every &= ok
        report[label] = {
            "receipt": receipt,
            "receipt_format": record["format"],
            "poses_equal": poses_equal,
            "side_equal": side_equal,
            "routes": fields,
            "controls_refused_by_both": controls,
            "all_equal": ok,
        }
        print(label, "all equal" if ok else "DIFFERENT", json.dumps(fields)[:400])
        for name, control in controls.items():
            print("  control", name, {k: v["passed"] for k, v in control.items()}, control["exact_verify"]["failures"][:1])
    out_path.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    return 0 if every else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
