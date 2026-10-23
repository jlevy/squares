#!/usr/bin/env python3
"""Hold review_t229_check.py's results to the packet's exact-certification receipt.

Standard library only. For each count it compares, exactly, what the review's checker
decided from the source certificate with what both maintained routes recorded in the
receipt: the side, every pose the receipt's checker input lists (x, y and t against the
review reader's rows), the pairs decided, the least wall clearance and the least pair
gap; and it confirms that the receipt's two controls at each count were refused by both
routes. It decides nothing itself.

Usage: agree_t229.py OUT.json CHECK.json[,CHECK.json] RECEIPT.json.xz LABEL=N=CERT_OR_FACT [...]
"""

import json
import lzma
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review_t229_check as rc  # noqa: E402
from fractions import Fraction  # noqa: E402


def half_tangent(rot):
    """A row's t = tan(theta/2) as a reduced pair: the certificate's own, or, from a fact's
    unit basis (c, s), exactly s / (1 + c), which the half-angle map inverts (c != -1)."""
    if rot[0] == "t":
        return rot[1]
    c, s = Fraction(*rot[1]), Fraction(*rot[2])
    if c == -1:
        raise ValueError("a basis with c = -1 has no finite half-angle tangent")
    t = s / (1 + c)
    return (t.numerator, t.denominator)


def main(argv):
    out_path, checks, receipt_path, specs = argv[0], argv[1].split(","), argv[2], argv[3:]
    mine = {}
    for path in checks:
        for entry in json.load(open(path))["inputs"]:
            mine[entry["label"]] = entry
    receipt = json.loads(lzma.decompress(open(receipt_path, "rb").read()))
    routes = receipt["routes"]
    report = {"receipt": receipt_path, "receipt_format": receipt["format"], "routes": routes,
              "counts": []}
    all_equal = True
    for spec in specs:
        label, n, cert_path = spec.split("=", 2)
        n = int(n)
        cert = rc.load(cert_path)
        entry = mine[label]
        rows = {c["control"]: c for c in receipt["cases"] if c["n"] == n}
        pos = rows["positive"]
        z, c = entry["route_Z"], entry["route_C"]
        poses = pos["checker_input"]["poses"]
        mine_poses = [[rc.rat_str(r["x"]), rc.rat_str(r["y"]), rc.rat_str(half_tangent(r["rot"]))]
                      for r in cert["squares"]]
        checks_n = {
            "side": entry["side"] == pos["checker_input"]["side"] == rc.rat_str(cert["side"]),
            "poses": poses == mine_poses,
        }
        for route in routes:
            v = pos[route]
            checks_n[f"{route}: passed"] = v["verification_passed"] is True and entry["accepted"]
            checks_n[f"{route}: pairs"] = v["pairs_tested"] == z["pairs_decided"] == c["pairs_decided"]
            checks_n[f"{route}: least wall clearance"] = (
                v["minimum_containment_clearance"] == z["least_wall_clearance"]
                == c["least_wall_clearance"])
            checks_n[f"{route}: least pair gap"] = v["minimum_best_pair_gap"] == z["least_gap"]
            checks_n[f"{route}: no failures"] = v["failures"] == []
            for control in ("duplicate-square-overlap", "square-translated-outside-container"):
                checks_n[f"{route}: {control} refused"] = (
                    rows[control][route]["verification_passed"] is False)
        ok = all(checks_n.values())
        all_equal = all_equal and ok
        report["counts"].append({"label": label, "n": n, "all_equal": ok, "checks": checks_n,
                                 "receipt_least_wall": pos[routes[0]]["minimum_containment_clearance"],
                                 "receipt_least_gap": pos[routes[0]]["minimum_best_pair_gap"],
                                 "review_least_wall": z["least_wall_clearance"],
                                 "review_least_gap": z["least_gap"]})
        print(f"{label}: " + ("every field equal" if ok else "DIFFERENCES: " + ", ".join(
            k for k, v in checks_n.items() if not v)))
    report["all_equal"] = all_equal
    with open(out_path, "w") as fh:
        json.dump(report, fh, indent=1)
    return 0 if all_equal else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
