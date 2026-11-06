"""The 260 certificate's sides against its binary64 input and pre-descent input.

Usage (from packing/, Python 3.14):
  python -I input_260.py CANDIDATES_DIR OUT.json

A measurement; it decides nothing about the bound. It compares the certificate's exact
side with the stated sides of s260_ks_1105.input.txt and s260_ks_1105.predescent.txt
(read as exact decimals), and measures the binary64 input itself at 60 digits: its
least separating-axis pair gap over pairs whose centres lie within 1.8 (see
house_slack.py for why no other pair can be closer), how many pairs overlap, and its
least wall clearance against its own stated side. Angles in the input are degrees.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import mpmath

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cert_reader import read_cert  # noqa: E402

mpmath.mp.dps = 60


def main() -> None:
    cand, out = Path(sys.argv[1]), Path(sys.argv[2])
    side = read_cert(cand / "s260_ks_1105.cert")["S"]
    s_pre = F(cand.joinpath("s260_ks_1105.predescent.txt").read_text().split()[1])
    s_in = F(cand.joinpath("s260_ks_1105.input.txt").read_text().split()[1])
    rows = [r.split() for r in cand.joinpath("s260_ks_1105.input.txt").read_text().strip().split("\n")[1:]]
    sq = []
    for x, y, a in rows:
        th = mpmath.radians(mpmath.mpf(a))
        c, s = mpmath.cos(th), mpmath.sin(th)
        X, Y = mpmath.mpf(x), mpmath.mpf(y)
        cs = [(X + (sa * c - sb * s) / 2, Y + (sa * s + sb * c) / 2) for sa, sb in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
        sq.append((cs, ((c, s), (-s, c)), (float(X), float(Y))))
    gmin = None
    neg = 0
    for i in range(len(sq)):
        for j in range(i + 1, len(sq)):
            (xi, yi), (xj, yj) = sq[i][2], sq[j][2]
            if math.hypot(xi - xj, yi - yj) >= 1.8:
                continue
            best = None
            for ax, ay in sq[i][1] + sq[j][1]:
                pi = [px * ax + py * ay for px, py in sq[i][0]]
                pj = [px * ax + py * ay for px, py in sq[j][0]]
                g = max(min(pj) - max(pi), min(pi) - max(pj))
                best = g if best is None or g > best else best
            if best < 0:
                neg += 1
            gmin = best if gmin is None or best < gmin else gmin
    sin_mp = mpmath.mpf(s_in.numerator) / s_in.denominator
    wmin = min(min(px, sin_mp - px, py, sin_mp - py) for cs, _, _ in sq for px, py in cs)
    res = {
        "S_prime_minus_S_input": float(side - s_in),
        "S_prime_minus_S_predescent": float(side - s_pre),
        "S_predescent_minus_S_input": float(s_pre - s_in),
        "input_least_pair_gap": mpmath.nstr(gmin, 6),
        "input_pairs_overlapping": neg,
        "input_least_wall_clearance_vs_its_side": mpmath.nstr(wmin, 6),
    }
    out.write_text(json.dumps(res, indent=1) + "\n")
    print(res)


if __name__ == "__main__":
    main()
