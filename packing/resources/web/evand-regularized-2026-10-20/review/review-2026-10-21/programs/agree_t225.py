"""Hold the review checker's results to the import lane's receipt, number by number.

Reads the four certificates (with review_t225_check's own reader), the decompressed
receipt `exact-certification.json` and the checker's outputs, and reports, per count:
whether every pose the receipt's `checker_input` carries equals the certificate row this
review's reader read, as rationals; whether the sides agree; and whether the least wall
clearance, the least pair gap and the number of pairs decided agree exactly across the
four computations (this review's two routes, the receipt's `exact_verify` and
`independent`). It also checks each JSON's S_cert against the header. Decides nothing
about feasibility itself; it compares.

Usage: python -I agree_t225.py CERT_DIR RECEIPT.json OUT.json CHECK.json [CHECK.json ...]
"""

from __future__ import annotations

import gzip
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import review_t225_check as check  # noqa: E402


def main(argv: list[str]) -> int:
    folder, receipt_path, out = Path(argv[1]), Path(argv[2]), Path(argv[3])
    mine = {}
    for path in argv[4:]:
        mine.update(json.loads(Path(path).read_text()))
    receipt = json.loads(receipt_path.read_text())
    report = {}
    ok_all = True
    for case in receipt["cases"]:
        if case["control"] != "positive":
            continue
        n = case["n"]
        text = gzip.decompress((folder / f"n-{n:03d}.cert.gz").read_bytes()).decode("ascii")
        side, rows = check.read_certificate(text, n)
        poses = case["checker_input"]["poses"]
        same_poses = len(poses) == len(rows) and all(
            tuple(Fraction(v) for v in pose) == tuple(Fraction(a, b) for a, b in row) for pose, row in zip(poses, rows)
        )
        same_side = Fraction(case["checker_input"]["side"]) == Fraction(*side)
        document = json.loads(gzip.decompress((folder / f"n-{n:03d}.json.gz").read_bytes()))
        s_cert = Fraction(document["S_cert"]) == Fraction(*side)
        m = mine[str(n)]
        walls = {
            "review_integers": Fraction(m["route_integers"]["least_wall_clearance"]["exact"]),
            "review_fraction": Fraction(m["route_fraction"]["least_wall_clearance"]["exact"]),
            "exact_verify": Fraction(case["exact_verify"]["minimum_containment_clearance"]),
            "independent": Fraction(case["independent"]["minimum_containment_clearance"]),
        }
        gaps = {
            "review_integers": Fraction(m["route_integers"]["least_pair_gap"]["exact"]),
            "review_fraction": Fraction(m["route_fraction"]["least_pair_gap"]["exact"]),
            "exact_verify": Fraction(case["exact_verify"]["minimum_best_pair_gap"]),
            "independent": Fraction(case["independent"]["minimum_best_pair_gap"]),
        }
        pairs = {
            "review_integers": m["route_integers"]["pairs_decided"],
            "exact_verify": case["exact_verify"]["pairs_tested"],
            "independent": case["independent"]["pairs_tested"],
            "n(n-1)/2": n * (n - 1) // 2,
        }
        row = {
            "poses_equal_certificate_rows": same_poses,
            "side_equal": same_side,
            "json_S_cert_equal_header": s_cert,
            "least_wall_all_equal": len(set(walls.values())) == 1,
            "least_wall": str(walls["review_integers"]),
            "least_gap_all_equal": len(set(gaps.values())) == 1,
            "least_gap": str(gaps["review_integers"]),
            "least_gap_approx": f"{float(gaps['review_integers']):.12e}",
            "pairs_all_equal": len(set(pairs.values())) == 1,
            "pairs": pairs["n(n-1)/2"],
            "receipt_passed": [case["exact_verify"]["verification_passed"], case["independent"]["verification_passed"]],
            "review_passed": m["passed"],
            "review_strict": m["strict"],
        }
        ok = all(v for k, v in row.items() if isinstance(v, bool)) and all(row["receipt_passed"])
        row["all_agree"] = ok
        ok_all &= ok
        report[str(n)] = row
        print(n, json.dumps(row))
    out.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print("agreement", "complete" if ok_all else "BROKEN")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
