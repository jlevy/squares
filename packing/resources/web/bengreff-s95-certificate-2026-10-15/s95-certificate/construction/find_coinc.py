"""Find exact 3-4-5 coincidence poses inside zm_mixed's uncertified boxes, and the cover's point atoms on
the edges of the unit square at that pose (exact rationals).

At theta* = 2 arctan(1/3) (cos 4/5, sin 3/5), or its complement 2 arctan(1/2) (cos 3/5, sin 4/5), the
rotated coordinates of 1/20-lattice points are multiples of 1/100. When the centre's rotated coordinates
(c_u, c_v) are multiples of 1/100 as well, many atoms lie exactly on the square's edges and zm_mixed
cannot close the pose at any depth. For each box whose angle range contains theta*, this tries every
centre with (c_u, c_v) in (1/100)Z inside the box and prints the free point atoms on the edges.

usage: python find_coinc.py COVER LOG [LOG ...]   (zm_mixed logs with "uncertified boxes" lists)
prints lines "x y" (exclusion candidates, 6 decimals) and a summary per box to stderr
"""
import sys, re, math
from fractions import Fraction as F

cover, logs = sys.argv[1], sys.argv[2:]
toks = [ln.split() for ln in open(cover) if ln.strip() and not ln.startswith("#")]
K = int(toks[1][0]); D = int(toks[2][0]); m = int(toks[4][0])
pts = [(int(a), int(b), int(w)) for a, b, w in toks[5:5 + m]]
lo, hi = F(5, 2), K - F(5, 2)


def in_cross(x, y):
    return lo <= x <= hi or lo <= y <= hi


ANG = [(F(4, 5), F(3, 5), 2 * math.degrees(math.atan(1 / 3))), (F(3, 5), F(4, 5), 2 * math.degrees(math.atan(1 / 2)))]
boxes = []
for lg in logs:
    for ln in open(lg):
        mm = re.match(r"\s*-\s+([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)\s*$", ln)
        if mm:
            boxes.append((lg,) + tuple(map(float, mm.groups())))
out = set()
for lg, x0, x1, y0, y1, t0, t1 in boxes:
    hit = False
    for co, si, tdeg in ANG:
        if not (t0 - 1e-6 <= tdeg <= t1 + 1e-6):
            continue
        cxm, cym = (x0 + x1) / 2, (y0 + y1) / 2
        cu0 = round((float(co) * cxm + float(si) * cym) * 100); cv0 = round((-float(si) * cxm + float(co) * cym) * 100)
        for du in range(-2, 3):
            for dv in range(-2, 3):
                cu, cv = F(cu0 + du, 100), F(cv0 + dv, 100)
                cx, cy = co * cu - si * cv, si * cu + co * cv
                if not (x0 - 1e-9 <= cx <= x1 + 1e-9 and y0 - 1e-9 <= cy <= y1 + 1e-9):
                    continue
                on, fixed = [], []
                for X, Y, w in pts:
                    px, py = F(X, D), F(Y, D)
                    u = co * (px - cx) + si * (py - cy); v = -si * (px - cx) + co * (py - cy)
                    if (abs(u) == F(1, 2) and abs(v) <= F(1, 2)) or (abs(v) == F(1, 2) and abs(u) <= F(1, 2)):
                        (on if in_cross(px, py) else fixed).append((px, py, w))
                if on or fixed:
                    hit = True
                    print("%s: box x[%.6f,%.6f] y[%.6f,%.6f] th[%.4f,%.4f]: pose (%s, %s) at %.4f deg: %d free + %d fixed atoms on edges"
                          % (lg, x0, x1, y0, y1, t0, t1, cx, cy, tdeg, len(on), len(fixed)), file=sys.stderr)
                    for px, py, w in on:
                        out.add("%.6f %.6f" % (float(px), float(py)))
    if not hit:
        print("%s: box x[%.6f,%.6f] y[%.6f,%.6f] th[%.4f,%.4f]: no 3-4-5 coincidence pose found" % (lg, x0, x1, y0, y1, t0, t1), file=sys.stderr)
for s in sorted(out):
    print(s)
