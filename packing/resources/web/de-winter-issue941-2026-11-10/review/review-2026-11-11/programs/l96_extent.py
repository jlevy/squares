"""The exact extent of each certificate's packing: the least side of a box that holds it
after a translation, and the slack between that and the certificate's side.

L96 review program. Usage: python -I -B l96_extent.py OUT_JSON CERT...
Extent = max(xmax - xmin, ymax - ymin) over the squares' exact bounding boxes. A
translation puts the packing in [0, extent]^2, so the certificate also proves s(n) <=
extent; the claim the issues print is the side's ceiling, not this. It decides nothing
about overlap (l96_check.py did, and translation keeps every margin).
"""

import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l96_read as R  # noqa: E402


def ceil10(q):
    v = -((-q.numerator * 10**10) // q.denominator)
    return f"{v // 10**10}.{v % 10**10:010d}"


def main():
    out = {}
    for path in sys.argv[2:]:
        with open(path, "rb") as fh:
            c = R.read_cert(fh.read())
        side = F(*c["side"])
        xs0, xs1, ys0, ys1 = [], [], [], []
        for a, b, t in c["squares"]:
            x, y, t = F(*a), F(*b), F(*t)
            d = 1 + t * t
            h = (abs(1 - t * t) + abs(2 * t)) / d / 2
            xs0.append(x - h)
            xs1.append(x + h)
            ys0.append(y - h)
            ys1.append(y + h)
        ex = max(max(xs1) - min(xs0), max(ys1) - min(ys0))
        out[os.path.basename(path)] = {
            "n": c["n"],
            "extent_x": f"{float(max(xs1) - min(xs0)):.17g}",
            "extent_y": f"{float(max(ys1) - min(ys0)):.17g}",
            "slack": f"{float(side - ex):.6e}",
            "left_gap": f"{float(min(xs0)):.6e}",
            "bottom_gap": f"{float(min(ys0)):.6e}",
            "right_gap": f"{float(side - max(xs1)):.6e}",
            "top_gap": f"{float(side - max(ys1)):.6e}",
            "extent_ceil_10": ceil10(ex),
            "side_ceil_10": ceil10(side),
            "same_10_place_print": ceil10(ex) == ceil10(side),
        }
        o = out[os.path.basename(path)]
        print(os.path.basename(path), o["slack"], o["left_gap"], o["bottom_gap"], o["right_gap"], o["top_gap"], o["same_10_place_print"])
    with open(sys.argv[1], "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")


if __name__ == "__main__":
    main()
