#!/usr/bin/env python3
"""Follow-up: strict exact check of a certificate, and export to the text format `n S` / `x y t`.

Not a judge (the frozen top-level verifier is). This applies the stricter convention used by other
public checkers of this problem: every wall margin must be positive and every pair of squares must be
strictly separated along one of the four edge normals. Exact rational arithmetic throughout
(fractions.Fraction); no floats in any decision.

Pairs whose centres are at squared distance >= 2 are disjoint without further test (two unit squares
have circumradius sqrt(2)/2 each). For the others, with D the centre difference, u_k the four edge
normals and delta the difference of the rotation angles, the squares have disjoint interiors iff
max_k |D . u_k| >= R, R = (1 + |cos delta| + |sin delta|) / 2; the margin reported is that maximum
minus R.

  fu_strict_check.py CERT.json [--export FILE.cert]
"""
import json
import sys
import time
from fractions import Fraction as F

HALF = F(1, 2)


def load(path):
    d = json.load(open(path))
    S = F(d["side"])
    sq = []
    for s in d["squares"]:
        cx, cy = F(s["cx"]), F(s["cy"])
        if "t" in s:
            t = F(s["t"])
            den = 1 + t * t
            c, sn = (1 - t * t) / den, 2 * t / den
        else:
            c, sn = F(s["c"]), F(s["s"])
            t = None
        assert c * c + sn * sn == 1
        sq.append((cx, cy, c, sn, t))
    assert len(sq) == int(d["n"])
    return int(d["n"]), S, sq


def dec(x, places=18):
    neg = x < 0
    x = abs(x)
    q = x.numerator * 10 ** places // x.denominator
    s = str(q).rjust(places + 1, "0")
    return ("-" if neg else "") + s[:-places] + "." + s[-places:]


def sci(x):
    return f"{float(x):.3e}"


def main():
    path = sys.argv[1]
    t0 = time.time()
    n, S, sq = load(path)
    wall = None
    for cx, cy, c, sn, _ in sq:
        h = (abs(c) + abs(sn)) * HALF
        m = min(cx - h, S - cx - h, cy - h, S - cy - h)
        wall = m if wall is None or m < wall else wall
    close = 0
    pair = None
    for i in range(n):
        xi, yi, ci, si, _ = sq[i]
        for j in range(i + 1, n):
            xj, yj, cj, sj, _ = sq[j]
            dx, dy = xj - xi, yj - yi
            if dx * dx + dy * dy >= 2:
                continue
            close += 1
            cd = ci * cj + si * sj
            sd = sj * ci - cj * si
            R = (1 + abs(cd) + abs(sd)) * HALF
            p = max(abs(dx * ci + dy * si), abs(-dx * si + dy * ci), abs(dx * cj + dy * sj), abs(-dx * sj + dy * cj))
            m = p - R
            pair = m if pair is None or m < pair else pair
    ok = wall > 0 and pair is not None and pair > 0
    print(f"file: {path}")
    print(f"n = {n}; side = {dec(S, 30)}… (exact fraction in the file)")
    print(f"pairs: {n * (n - 1) // 2} in all; {close} with centres at squared distance < 2 tested on the four edge normals")
    print(f"smallest pair margin: {sci(pair)} (exact: {pair})")
    print(f"smallest wall margin: {sci(wall)} (exact: {wall})")
    print("STRICT VALID" if ok else "NOT STRICT (a margin is zero or negative)")
    print(f"seconds: {time.time() - t0:.1f}")
    if "--export" in sys.argv:
        out = sys.argv[sys.argv.index("--export") + 1]
        with open(out, "w") as f:
            f.write(f"# {n} unit squares in a square of side {dec(S, 18)}… ; exact rationals\n")
            f.write("# line 1: n S ; then one line per square: x y t (centre, t = tan(theta/2))\n")
            f.write(f"{n} {S}\n")
            for cx, cy, c, sn, t in sq:
                assert t is not None
                f.write(f"{cx} {cy} {t}\n")
        print(f"exported: {out}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
