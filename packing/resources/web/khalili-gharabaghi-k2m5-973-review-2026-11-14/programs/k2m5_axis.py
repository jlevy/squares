"""Exact theta = 0 face of a board (review of #973, L144): clean-room Lemma Z over the whole axis face.

usage: python -I k2m5_axis.py COVER OUT_JSON

For a closed axis-parallel unit square with centre (X, Y), a horizontal elementary piece on the line y0 counts
w * |[s, s+1] cap [X-5, X+5]| (tenths) if |y0 - Y| <= 5, else 0; vertical pieces likewise; the Lebesgue part is
rho |[X-5, X+5] cap [x0, x1]| |[Y-5, Y+5] cap [y0, y1]|.  On an open cell (a, a+1) x (b, b+1) of the 1/10 grid the
set of lines counted is fixed (y0 in [b-4, b+5], x0 in [a-4, a+5]) and the mass is bilinear, so its infimum over
the closed cell is the least of the four one-sided corner limits; on a cell boundary the mass is upper
semicontinuous, hence at least each adjacent cell's limit.  So the least corner limit over all cells of
[1/2, side - 1/2]^2 is the infimum of the mass over every closed axis-parallel unit square in the container.
At an integer corner (X, Y) every elementary piece is wholly in or out, so a corner limit is a sum of whole
weights plus the Lebesgue term.  Exact integers in units of 1/(wden * pitch^2).
"""
import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k2m5_exact import load_cover  # noqa: E402


def main():
    path, out = sys.argv[1:3]
    cv = load_cover(path)
    P = cv["pitch"]
    n = int(cv["side"] * P)
    wden = cv["wden"]
    # prefix sums per line of whole weights by start index
    def prefix(lines):
        pre = {}
        for line, segs in lines.items():
            arr = [0] * (n + 2)
            for s0, s1, w in segs:
                arr[s0 + 1] += w
            for k in range(1, n + 2):
                arr[k] += arr[k - 1]
            pre[line] = arr
        return pre
    H, V = prefix(cv["hor"]), prefix(cv["ver"])

    def rng_sum(pre, line, lo, hi):          # sum of weights with start in [lo, hi]
        arr = pre.get(line)
        if arr is None:
            return 0
        lo, hi = max(lo, 0), min(hi, n - 1)
        return arr[hi + 1] - arr[lo] if lo <= hi else 0
    rects = [(int(x0 * P), int(x1 * P), int(y0 * P), int(y1 * P), rho) for x0, x1, y0, y1, rho in cv["rects"]]
    # every value scaled by S = wden * P^2 (Lebesgue: rho * ox * oy / P^2 -> rho * ox * oy * wden)
    S = wden * P * P
    best = None
    cnt_tight = 0
    corners = 0
    hist = {}
    d4 = dict(corners=0, tight=0, min=None)
    for a in range(P // 2, n - P // 2):
        for b in range(P // 2, n - P // 2):
            hl = list(range(b - 4, b + 6))
            vl = list(range(a - 4, a + 6))
            for X in (a, a + 1):
                for Y in (b, b + 1):
                    m = 0
                    for y0 in hl:
                        m += rng_sum(H, y0, X - 5, X + 4)
                    for x0 in vl:
                        m += rng_sum(V, x0, Y - 5, Y + 4)
                    m *= P * P
                    for x0, x1, y0, y1, rho in rects:
                        ox = max(0, min(X + 5, x1) - max(X - 5, x0))
                        oy = max(0, min(Y + 5, y1) - max(Y - 5, y0))
                        val = rho * ox * oy * wden
                        if val.denominator != 1:
                            raise ValueError("non-integer Lebesgue term")
                        m += int(val)
                    corners += 1
                    if best is None or m < best[0]:
                        best = (m, (a, b, X, Y))
                    if m == S:
                        cnt_tight += 1
                    in_d4 = a < n // 2 and b < n // 2
                    if in_d4:
                        d4["corners"] += 1
                        d4["tight"] += m == S
                        d4["min"] = m if d4["min"] is None else min(d4["min"], m)
    res = dict(cover=os.path.basename(path), cells=(n - P) ** 2, corner_limits=corners,
               min_mass=str(F(best[0], S)), min_at_cell_corner_tenths=best[1],
               corners_at_exactly_1=cnt_tight, min_ge_1=best[0] >= S,
               d4_region=dict(corners=d4["corners"], at_exactly_1=d4["tight"], min_mass=str(F(d4["min"], S))))
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
