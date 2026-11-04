"""Undo the 299 certificate's stated "exact radial repair" and measure what it repaired.

Usage: oz_repair.py CERT.yaml EXPORT.json.gz OUT.json

The lab's export (n299-refill2-t000173.json) names the method "rational half-angle basis and
exact radial repair" and a repair_factor r. This program reads r from the export, maps every
centre back by the scaling about (1/2, 1/2) by 1/r, keeps the bases, and sets the side to
S0 = 1 + (S - 1)/r. It reports the decimal places of the pre-images and S0, and the pre-repair
packing's overlapping pairs and wall violations, exactly. A measurement of how the
certificate was made; it decides nothing about the bound, which oz_check.py decides.
"""

from __future__ import annotations

import json
import platform
import sys
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ozlib as oz  # noqa: E402


def main() -> int:
    cert_p, export_p, out_p = sys.argv[1:4]
    t0 = time.process_time()
    doc = oz.read_witness_yaml(cert_p)
    exp = oz.read_witness_json(export_p, gz=export_p.endswith(".gz"))
    r = oz.to_F(exp["claim"]["repair_factor"])
    h = Fraction(1, 2)
    S = oz.to_F(doc["header"]["side"])
    S0 = 1 + (S - 1) / r
    squares = oz.witness_squares(doc)
    pre = []
    places = Counter()
    for sq in squares:
        x, y, a, b, s = sq["F"]
        x0 = h + (x - h) / r
        y0 = h + (y - h) / r
        for c in (x0, y0):
            k = oz.terminating_places(c)
            places[str(k) if k is not None and k <= 40 else "none"] += 1
        pre.append((sq["id"], (x0, y0, a, b, s)))
    tvals = [sq["F"][3] / (1 + sq["F"][2]) for sq in squares if sq["F"][3] != 0]
    neg = []
    least = None
    for p in range(len(pre)):
        for q in range(p + 1, len(pre)):
            m, _ = oz.sat_margin_F(pre[p][1], pre[q][1])
            if m < 0:
                neg.append((m, pre[p][0], pre[q][0]))
            if least is None or m < least[0]:
                least = (m, pre[p][0], pre[q][0])
    neg.sort()
    outside = []
    for sid, s0 in pre:
        c = min(oz.wall_clearances_F(s0, S0))
        if c < 0:
            outside.append([sid, oz.sci(c)])
    receipt = {
        "program": "oz_repair.py",
        "program_sha256": oz.sha256_file(__file__),
        "ozlib_sha256": oz.sha256_file(HERE / "ozlib.py"),
        "python": platform.python_version(),
        "argv": sys.argv[1:],
        "repair_factor": oz.frac_str(r),
        "repair_factor_minus_1": oz.sci(r - 1, 12),
        "S0": oz.frac_str(S0),
        "S0_places": oz.terminating_places(S0),
        "S0_decimal": oz.decimal_places(S0, oz.terminating_places(S0), "exact") if oz.terminating_places(S0) is not None else None,
        "centre_preimage_decimal_places": dict(sorted(places.items())),
        "half_angle_t_max_digits": [max(len(str(abs(t.numerator))) for t in tvals), max(len(str(t.denominator)) for t in tvals)],
        "pre_repair_overlapping_pairs": len(neg),
        "pre_repair_worst": [oz.sci(least[0]), least[1], least[2]],
        "pre_repair_five_worst": [[oz.sci(m, 6), i, j] for m, i, j in neg[:5]],
        "pre_repair_squares_outside_box": outside,
        "decides": "nothing about the bound; how the certificate was made",
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    Path(out_p).write_text(json.dumps(receipt, indent=1) + "\n")
    print(f"repair r - 1 = {receipt['repair_factor_minus_1']}; S0 = {receipt['S0_decimal']}; pre-images {receipt['centre_preimage_decimal_places']}; "
          f"pre-repair overlaps {len(neg)} (worst {receipt['pre_repair_worst']}); outside {outside}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
