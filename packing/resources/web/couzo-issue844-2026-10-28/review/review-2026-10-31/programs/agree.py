"""Hold the clean-room checker to the maintained replay receipts; decides nothing new.

For each positive case of each receipt: the receipt's side and poses equal the
certificate's, literal for literal; both routes passed; and their least pair gap and
least wall clearance equal route A's here, exactly. Run after check_certs.py decided.

Usage: agree.py RECEIPT.json.xz CERT [CERT ...]
"""

from __future__ import annotations

import json
import lzma
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_certs import frame, parse, route_a  # noqa: E402


def main():
    rec = json.loads(lzma.open(sys.argv[1]).read())
    certs = {}
    for p in sys.argv[2:]:
        n, side, raw = parse(Path(p).read_text(encoding="utf-8"))
        certs[n] = (side, raw)
    checks = 0
    equal = 0
    for case in rec["cases"]:
        if case["control"] != "positive":
            print(f"  control {case['n']} {case['control']}: exact_verify passed={case['exact_verify']['verification_passed']}, independent passed={case['independent']['verification_passed']}")
            continue
        n = case["n"]
        side, raw = certs[n]
        ci = case["checker_input"]
        res = []
        res.append(("side literal", F(ci["side"]) == side))
        poses = ci["poses"]
        same = len(poses) == len(raw)
        if same:
            for p, r in zip(poses, raw):
                vals = [F(str(v)) for v in (p.values() if isinstance(p, dict) else p)]
                if vals[:3] != list(r):
                    same = False
                    break
        res.append(("poses literal", same))
        S = [frame(*r) for r in raw]
        a = route_a(side, S)
        m = a["least_pair_margin"][0]
        w = a["least_wall"][0]
        for route in ("exact_verify", "independent"):
            rr = case[route]
            res.append((f"{route} passed", rr["verification_passed"] is True and not rr["failures"]))
            res.append((f"{route} pairs tested = all", rr["pairs_tested"] == n * (n - 1) // 2))
            res.append((f"{route} least pair gap = route A's", F(rr["minimum_best_pair_gap"]) == m))
            res.append((f"{route} least wall = route A's", F(rr["minimum_containment_clearance"]) == w))
        for k, ok in res:
            checks += 1
            equal += ok
            print(f"  {n}: {k}: {'equal' if ok else 'DIFFERENT'}")
    print(f"{equal} of {checks} checks equal")
    return 0 if equal == checks else 1


if __name__ == "__main__":
    sys.exit(main())
