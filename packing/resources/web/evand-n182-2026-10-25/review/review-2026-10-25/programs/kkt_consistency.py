"""How the #806 certificate stands to the source's 80-digit KKT point.

Written for the stage 4 mathematical review of jlevy/squares issue 806. It decides
nothing about the bound, which rests on the exact certificate alone (exact_check.py).
It checks the source's `.exact.txt` only as far as it bears on what the record would
state:

1. that the certificate is that point, centres dilated about the origin by 1 + 1e-20
   and tan(theta/2) rounded to rationals, by measuring the largest centre and angle
   differences at 100 digits;
2. how far the point's side S* lies below the certificate's side, and below
   S* (1 + 1e-20);
3. that the point is a packing at S* to within its 80 digits, and has the contact
   structure the certificate shows: pairs and walls at |gap| below 1e-60 (active),
   against those the certificate puts below 1e-15, and the least gap among the rest;
4. which squares the point leaves at binary64 values (the source's free squares).

It does not check stationarity, the multipliers, the second-order test or the flat
motions, which bear on local minimality and not on s(182).

Run with the project interpreter in isolated mode:

    python3 -I kkt_consistency.py CERT EXACT_TXT INPUT_TXT --json OUT
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction
from itertools import combinations

import mpmath as mp

mp.mp.dps = 100
TOKEN = re.compile(r"^-?[0-9]+(?:/[0-9]+)?$")
DELTA = mp.mpf(10) ** -20


def digest(path: str) -> str:
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def read_cert(path: str) -> tuple[Fraction, list[tuple[Fraction, Fraction, Fraction]]]:
    rows = [ln.split() for ln in open(path, encoding="ascii") if ln.strip() and not ln.startswith("#")]
    for row in rows[1:]:
        for tok in row:
            if not TOKEN.match(tok):
                raise ValueError(tok[:40])
    return Fraction(rows[0][1]), [tuple(Fraction(t) for t in row) for row in rows[1:]]  # type: ignore[misc]


def read_point(path: str) -> tuple[str, list[tuple[str, str, str]]]:
    rows = [ln.split() for ln in open(path, encoding="ascii") if ln.strip()]
    return rows[0][1], [(x, y, d) for x, y, d in rows[1:]]


def mpq(q: Fraction) -> mp.mpf:
    return mp.mpf(q.numerator) / q.denominator


def frame_deg(deg: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
    r = deg * mp.pi / 180
    return mp.cos(r), mp.sin(r)


def corners(x: mp.mpf, y: mp.mpf, c: mp.mpf, s: mp.mpf) -> list[tuple[mp.mpf, mp.mpf]]:
    h = mp.mpf(1) / 2
    return [(x + c * u - s * v, y + s * u + c * v) for (u, v) in ((-h, -h), (h, -h), (h, h), (-h, h))]


def gap(a: tuple, b: tuple) -> mp.mpf:
    (ca, sa, va), (cb, sb, vb) = a, b
    best = None
    for ux, uy in ((ca, sa), (-sa, ca), (cb, sb), (-sb, cb)):
        pa = [ux * px + uy * py for px, py in va]
        pb = [ux * px + uy * py for px, py in vb]
        g = max(min(pb) - max(pa), min(pa) - max(pb))
        best = g if best is None or g > best else best
    return best


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cert")
    ap.add_argument("exact")
    ap.add_argument("input")
    ap.add_argument("--json", required=True)
    a = ap.parse_args()
    side, cert = read_cert(a.cert)
    s_star_txt, point = read_point(a.exact)
    _, inp = read_point(a.input)
    s_star = mp.mpf(s_star_txt)
    L = mpq(side)
    out: dict = {"program": "kkt_consistency.py", "program_sha256": digest(__file__), "python": sys.version.split()[0], "mpmath_dps": mp.mp.dps,
                 "inputs": {"cert": [a.cert, digest(a.cert)], "exact": [a.exact, digest(a.exact)], "input": [a.input, digest(a.input)]}}

    # 1. The certificate against the point dilated by 1 + 1e-20.
    dx = dy = da = mp.mpf(0)
    worst = None
    for i, ((xc, yc, tc), (xk, yk, dk)) in enumerate(zip(cert, point, strict=True)):
        ex = abs(mpq(xc) - (1 + DELTA) * mp.mpf(xk))
        ey = abs(mpq(yc) - (1 + DELTA) * mp.mpf(yk))
        deg_c = 2 * mp.atan(mpq(tc)) * 180 / mp.pi
        d = abs(deg_c - mp.mpf(dk)) % 90
        d = min(d, 90 - d)
        if worst is None or max(ex, ey) > worst[0]:
            worst = (max(ex, ey), i)
        dx, dy, da = max(dx, ex), max(dy, ey), max(da, d)
    assert worst is not None
    out["certificate_vs_dilated_point"] = {"max_centre_x_diff": mp.nstr(dx, 5), "max_centre_y_diff": mp.nstr(dy, 5), "max_angle_diff_deg": mp.nstr(da, 5), "worst_square": worst[1]}
    print(f"1. certificate vs point dilated by 1 + 1e-20: max |dx| {mp.nstr(dx, 5)}, max |dy| {mp.nstr(dy, 5)}, max angle diff {mp.nstr(da, 5)} deg")

    # 2. The sides.
    out["sides"] = {
        "S_star": s_star_txt,
        "S_cert": str(side),
        "S_cert_minus_S_star": mp.nstr(L - s_star, 12),
        "S_cert_minus_S_star_times_1_plus_1e-20": mp.nstr(L - s_star * (1 + DELTA), 12),
    }
    print(f"2. S_cert - S* = {mp.nstr(L - s_star, 12)}; S_cert - S*(1 + 1e-20) = {mp.nstr(L - s_star * (1 + DELTA), 12)}")

    # 3. The point as a packing at S*, at 100 digits.
    sq = []
    for xk, yk, dk in point:
        x, y = mp.mpf(xk), mp.mpf(yk)
        c, s = frame_deg(mp.mpf(dk))
        sq.append((c, s, corners(x, y, c, s)))
    walls = []
    for i, (_, _, v) in enumerate(sq):
        for name, val in (("left", min(px for px, _ in v)), ("bottom", min(py for _, py in v)), ("right", s_star - max(px for px, _ in v)), ("top", s_star - max(py for _, py in v))):
            walls.append((val, i, name))
    pairs = [(gap(sq[i], sq[j]), i, j) for i, j in combinations(range(len(sq)), 2)]
    act_w = [w for w in walls if abs(w[0]) < mp.mpf(10) ** -60]
    act_p = [p for p in pairs if abs(p[0]) < mp.mpf(10) ** -60]
    rest_w = min(w[0] for w in walls if abs(w[0]) >= mp.mpf(10) ** -60)
    rest_p = min(p[0] for p in pairs if abs(p[0]) >= mp.mpf(10) ** -60)
    out["point_as_packing"] = {
        "least_wall_gap": mp.nstr(min(w[0] for w in walls), 5),
        "least_pair_gap": mp.nstr(min(p[0] for p in pairs), 5),
        "active_walls_below_1e-60": len(act_w),
        "active_pairs_below_1e-60": len(act_p),
        "least_inactive_wall_gap": mp.nstr(rest_w, 8),
        "least_inactive_pair_gap": mp.nstr(rest_p, 8),
        "pairs_between_1e-60_and_1e-15": sum(1 for p in pairs if mp.mpf(10) ** -60 <= abs(p[0]) < mp.mpf(10) ** -15),
    }
    print(f"3. point at S*: least wall gap {mp.nstr(min(w[0] for w in walls), 5)}, least pair gap {mp.nstr(min(p[0] for p in pairs), 5)};"
          f" active (|gap| < 1e-60): {len(act_w)} walls + {len(act_p)} pairs = {len(act_w) + len(act_p)};"
          f" least inactive gaps: wall {mp.nstr(rest_w, 8)}, pair {mp.nstr(rest_p, 8)}")

    # 4. Squares the point leaves at the binary64 input's values.
    same = [i for i, ((xk, yk, _), (xi, yi, _)) in enumerate(zip(point, inp, strict=True)) if xk == xi and yk == yi]
    short = [i for i, (xk, yk, dk) in enumerate(point) if max(len(xk), len(yk), len(dk)) < 30]
    touching = {i for _, i, _ in act_w} | {i for _, i, j in act_p} | {j for _, i, j in act_p}
    free = sorted(set(range(len(point))) - touching)
    out["free_squares"] = {"point_equals_input_text": same, "short_lines": short, "touching_nothing_at_1e-60": free}
    print(f"4. squares whose point centre is the input's text: {same}; short lines: {short}; touching nothing: {free}")
    with open(a.json, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
