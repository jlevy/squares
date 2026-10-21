"""Hold the #703 certificate to the construction the source's search/exact/README.md
describes: the KKT configuration (`s270_sw.exact.txt`, `n S*` then `x y theta_deg`, 70
digits) scaled about the origin corner by 1 + 1e-20, centres rounded to 1e-35,
tangents t = tan(theta/2) rounded to 1e-35, and S' = ceil(S* (1 + 1e-20) at 30 places).

Reads both files with the review checker's reader and the standard library; tan at 60
digits with mpmath. A measurement; it decides nothing about the bound.

Usage: python -I construction_708.py REVIEW_DIR CERT KKT OUT.json
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import mpmath

EPS = Fraction(1, 10**20)


def main(argv: list[str]) -> int:
    review, cert, kkt, out = (Path(a) for a in argv[1:5])
    sys.path.insert(0, str(review))
    import review_708_check as rc  # noqa: E402

    side, squares, tangents = rc.read(cert, 270)
    lines = [ln for ln in kkt.read_text("ascii").split("\n") if ln.strip()]
    n, s_star = lines[0].split()
    assert int(n) == 270 and len(lines) == 271
    S = Fraction(Decimal(s_star))
    scaled = S * (1 + EPS)
    constructed = Fraction(-(-scaled.numerator * 10**30 // scaled.denominator), 10**30)
    mpmath.mp.dps = 80
    centre_diffs = []
    tangent_diffs = []
    upright = 0
    for (x, y, _c, _s), t, row in zip(squares, tangents, lines[1:], strict=True):
        kx, ky, kth = row.split()
        for coord, lit in ((x, kx), (y, ky)):
            exact = Fraction(Decimal(lit)) * (1 + EPS)
            centre_diffs.append(abs(coord - exact))
        theta = mpmath.mpf(kth)
        tan_half = mpmath.tan(mpmath.radians(theta) / 2)
        approx = Fraction(mpmath.nstr(tan_half, 60, strip_zeros=False)) if tan_half != 0 else Fraction(0)
        tangent_diffs.append(abs(t - approx))
        if t == 0:
            upright += 1
    result = {
        "kkt_side_first_40": s_star[:42],
        "certificate_side": str(side),
        "side_is_kkt_scaled_rounded_up_at_30": constructed == side,
        "rounded_up_by": f"{float(side - scaled):.3e}",
        "side_exceeds_kkt_by": f"{float(side - S):.3e}",
        "largest_centre_difference_from_scaled_kkt": f"{float(max(centre_diffs)):.3e}",
        "centres_within_5e-36": sum(1 for d in centre_diffs if d <= Fraction(5, 10**36)) // 2,
        "largest_tangent_difference_from_tan_half_angle": f"{float(max(tangent_diffs)):.3e}",
        "tangents_within_1e-35": sum(1 for d in tangent_diffs if d <= Fraction(1, 10**35)),
        "upright_t0": upright,
        "predicted_least_wall_clearance": "eps/2 = 5e-21 for an upright square whose centre is 1/2 from a wall",
    }
    out.write_text(json.dumps(result, indent=1), encoding="utf-8")
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
