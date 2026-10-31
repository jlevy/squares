"""Clean-room exact checker for half-angle rational square-packing certificates.

Written for the stage 4 review of Couzo's #843, #844 and a5a5d76 certificates
(bold-ritchie-rv-couzo, 2026-10-31). Its author read the certificates' format line and
the mathematics only; no source checker, maintained route or identity tool was read
before it decided.

Format: a comment line, then "n S", then n rows "x y t", each field an integer or p/q,
a unit square centred at (x, y) whose edge direction is u = ((1-t^2)/(1+t^2),
2t/(1+t^2)) and v = (-u_y, u_x).

Route A: every pair by separating axes (the four edge normals), exact over Q, with a
binary64 hint choosing which axis to try first; every wall by the support function.
Route B: walls by exact corners; pairs whose centres are closer than sqrt(2) by the
exact area of the clipped intersection (Sutherland-Hodgman over Q), which must be 0;
farther pairs are disjoint since each closed square lies in the closed disc of radius
sqrt(2)/2 about its centre and its interior in the open disc.

Usage: check_certs.py LABEL=PATH ... --out RECEIPT.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from fractions import Fraction as F

HALF = F(1, 2)
INT_OR_RATIO = re.compile(r"^-?\d+(/\d+)?$")


class Refused(Exception):
    pass


def parse(text: str):
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("#"):
        raise Refused("no comment line")
    head = lines[1].split()
    if len(head) != 2 or not re.fullmatch(r"\d+", head[0]) or not INT_OR_RATIO.match(head[1]):
        raise Refused("bad header")
    n = int(head[0])
    side = F(head[1])
    rows = lines[2:]
    if len(rows) != n:
        raise Refused(f"header n={n} but {len(rows)} rows")
    sq = []
    for k, row in enumerate(rows):
        f = row.split()
        if len(f) != 3 or not all(INT_OR_RATIO.match(x) for x in f):
            raise Refused(f"row {k + 1} malformed")
        x, y, t = (F(z) for z in f)
        sq.append((x, y, t))
    return n, side, sq


def frame(x, y, t):
    d = 1 + t * t
    ux, uy = (1 - t * t) / d, 2 * t / d
    if ux * ux + uy * uy != 1:
        raise Refused("rotation not on the unit circle")
    return (x, y, ux, uy, -uy, ux)


def corners(s):
    x, y, ux, uy, vx, vy = s
    out = []
    for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1)):  # counter-clockwise
        out.append((x + HALF * (a * ux + b * vx), y + HALF * (a * uy + b * vy)))
    return out


# ---------- route A ----------


def axis_margin(si, sj, ax, ay):
    """Separation margin of squares si, sj along unit axis (ax, ay): >= 0 separates."""
    d = abs((sj[0] - si[0]) * ax + (sj[1] - si[1]) * ay)
    ri = HALF * (abs(si[2] * ax + si[3] * ay) + abs(si[4] * ax + si[5] * ay))
    rj = HALF * (abs(sj[2] * ax + sj[3] * ay) + abs(sj[4] * ax + sj[5] * ay))
    return d - ri - rj


def axes_of(si, sj):
    return ((si[2], si[3]), (si[4], si[5]), (sj[2], sj[3]), (sj[4], sj[5]))


def float_margins(fi, fj):
    out = []
    for ax, ay in ((fi[2], fi[3]), (fi[4], fi[5]), (fj[2], fj[3]), (fj[4], fj[5])):
        d = abs((fj[0] - fi[0]) * ax + (fj[1] - fi[1]) * ay)
        ri = 0.5 * (abs(fi[2] * ax + fi[3] * ay) + abs(fi[4] * ax + fi[5] * ay))
        rj = 0.5 * (abs(fj[2] * ax + fj[3] * ay) + abs(fj[4] * ax + fj[5] * ay))
        out.append(d - ri - rj)
    return out


def route_a(side, S, *, exact_margin_below=1e-6):
    fl = [tuple(float(c) for c in s) for s in S]
    walls = []
    for k, s in enumerate(S):
        hx = HALF * (abs(s[2]) + abs(s[4]))
        hy = HALF * (abs(s[3]) + abs(s[5]))
        walls.append((min(s[0] - hx, side - s[0] - hx, s[1] - hy, side - s[1] - hy), k + 1))
    least_wall = min(walls)
    bad_walls = [k for w, k in walls if w < 0]
    extent = max(max(s[0] + HALF * (abs(s[2]) + abs(s[4])), s[1] + HALF * (abs(s[3]) + abs(s[5]))) for s in S)
    low = min(min(s[0] - HALF * (abs(s[2]) + abs(s[4])), s[1] - HALF * (abs(s[3]) + abs(s[5]))) for s in S)
    bad_pairs = []
    least = None
    near = 0
    n = len(S)
    for i in range(n):
        si, fi = S[i], fl[i]
        for j in range(i + 1, n):
            sj, fj = S[j], fl[j]
            fm = float_margins(fi, fj)
            best = max(range(4), key=lambda q: fm[q])
            axes = axes_of(si, sj)
            if fm[best] > exact_margin_below:
                # exact check on the hinted axis; fall back to all axes
                if axis_margin(si, sj, *axes[best]) >= 0:
                    continue
            near += 1
            m = max(axis_margin(si, sj, *a) for a in axes)
            if m < 0:
                bad_pairs.append((i + 1, j + 1))
            if least is None or m < least[0]:
                least = (m, i + 1, j + 1)
    return {
        "pairs": n * (n - 1) // 2,
        "pairs_decided_exactly_on_all_axes": near,
        "bad_pairs": bad_pairs[:20],
        "n_bad_pairs": len(bad_pairs),
        "least_pair_margin": least,
        "least_wall": least_wall,
        "bad_walls": bad_walls[:20],
        "extent": extent,
        "low": low,
        "accepted": not bad_pairs and not bad_walls,
    }


# ---------- route B ----------


def clip(subject, clipper):
    """Sutherland-Hodgman: subject polygon clipped by convex CCW clipper, exact."""
    out = subject
    m = len(clipper)
    for k in range(m):
        ax, ay = clipper[k]
        bx, by = clipper[(k + 1) % m]
        ex, ey = bx - ax, by - ay

        def side_of(p):
            return ex * (p[1] - ay) - ey * (p[0] - ax)  # >0 inside (left of edge)

        inp = out
        out = []
        if not inp:
            break
        prev = inp[-1]
        sp = side_of(prev)
        for cur in inp:
            sc = side_of(cur)
            if sc >= 0:
                if sp < 0:
                    tt = sp / (sp - sc)
                    out.append((prev[0] + tt * (cur[0] - prev[0]), prev[1] + tt * (cur[1] - prev[1])))
                out.append(cur)
            elif sp >= 0:
                tt = sp / (sp - sc)
                out.append((prev[0] + tt * (cur[0] - prev[0]), prev[1] + tt * (cur[1] - prev[1])))
            prev, sp = cur, sc
    return out


def area2(poly):
    a = F(0)
    for k in range(len(poly)):
        x1, y1 = poly[k]
        x2, y2 = poly[(k + 1) % len(poly)]
        a += x1 * y2 - x2 * y1
    return a


def route_b(side, S):
    C = [corners(s) for s in S]
    bad_walls = []
    least_wall = None
    for k, cs in enumerate(C):
        for x, y in cs:
            m = min(x, side - x, y, side - y)
            if least_wall is None or m < least_wall[0]:
                least_wall = (m, k + 1)
            if m < 0:
                bad_walls.append(k + 1)
                break
    n = len(S)
    fl = [(float(s[0]), float(s[1])) for s in S]
    near = 0
    bad_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            dx = fl[j][0] - fl[i][0]
            dy = fl[j][1] - fl[i][1]
            if dx * dx + dy * dy > 2.0 + 1e-9:
                continue
            ex = S[j][0] - S[i][0]
            ey = S[j][1] - S[i][1]
            if ex * ex + ey * ey >= 2:
                continue
            near += 1
            a = area2(clip(C[i], C[j]))
            if a != 0:
                bad_pairs.append((i + 1, j + 1))
    return {
        "pairs_by_area": near,
        "bad_pairs": bad_pairs[:20],
        "n_bad_pairs": len(bad_pairs),
        "least_wall": least_wall,
        "bad_walls": bad_walls[:20],
        "accepted": not bad_pairs and not bad_walls,
    }


def decide(side, S):
    a = route_a(side, S)
    b = route_b(side, S)
    return a, b


def short(x):
    if isinstance(x, F):
        return float(x)
    if isinstance(x, tuple):
        return [short(y) for y in x]
    if isinstance(x, list):
        return [short(y) for y in x]
    if isinstance(x, dict):
        return {k: short(v) for k, v in x.items()}
    return x


def controls(side, S, a_res):
    """Controls built in memory by exact rules; each is decided by both routes."""
    out = {}
    eps = F(1, 10**30)
    m, i, j = a_res["least_pair_margin"]
    i0, j0 = i - 1, j - 1
    # 1. duplicate of the tightest pair's neighbour
    T = list(S)
    T[j0] = S[i0]
    out["duplicate"] = T
    # 2. box at the exact extent, and 1e-30 below it (packing translated to touch origin)
    low = a_res["low"]
    shifted = [(s[0] - low, s[1] - low) + s[2:] for s in S]
    ext = a_res["extent"] - low
    out["box_at_extent"] = ("side", ext, shifted)
    out["box_below_extent"] = ("side", ext - eps, shifted)
    # 3. tightest pair closed along its separating axis to contact, and 1e-30 past it
    si, sj = S[i0], S[j0]
    axes = axes_of(si, sj)
    margins = [axis_margin(si, sj, *ax) for ax in axes]
    q = max(range(4), key=lambda k: margins[k])
    ax, ay = axes[q]
    sgn = 1 if (sj[0] - si[0]) * ax + (sj[1] - si[1]) * ay > 0 else -1
    for name, mv in (("pair_contact", margins[q]), ("pair_past_contact", margins[q] + eps)):
        T = list(S)
        T[j0] = (sj[0] - sgn * mv * ax, sj[1] - sgn * mv * ay) + sj[2:]
        out[name] = T
    # 4. move j halfway to i
    T = list(S)
    T[j0] = ((si[0] + sj[0]) / 2, (si[1] + sj[1]) / 2) + sj[2:]
    out["halfway"] = T
    # 5. every rotation reversed (reported only)
    rev = []
    for s in S:
        rev.append((s[0], s[1], s[2], -s[3], -s[4], s[5]))
    out["rotation_reversed"] = rev
    return out


def run(label, path):
    text = open(path, encoding="utf-8").read()
    t0 = time.process_time()
    n, side, raw = parse(text)
    S = [frame(*r) for r in raw]
    a, b = decide(side, S)
    rec = {
        "label": label,
        "path": path,
        "n": n,
        "side": f"{side.numerator}/{side.denominator}",
        "side_float": float(side),
        "route_a": short(a),
        "route_b": short(b),
        "side_minus_extent": float(side - a["extent"]),
        "low_corner_min": float(a["low"]),
    }
    # reader controls
    lines = text.splitlines()
    hdr = lines[1].split()
    bumped = "\n".join([lines[0], f"{int(hdr[0]) + 1} {hdr[1]}"] + lines[2:])
    dec = list(lines)
    f3 = dec[2].split()
    f3[0] = repr(float(F(f3[0])))
    dec[2] = " ".join(f3)
    reader = {}
    for nm, tx in (("count_plus_one", bumped), ("decimal_field", "\n".join(dec))):
        try:
            parse(tx)
            reader[nm] = "accepted"
        except Refused as e:
            reader[nm] = f"refused: {e}"
    rec["reader_controls"] = reader
    ctl = {}
    for nm, val in controls(side, S, a).items():
        if isinstance(val, tuple) and val[0] == "side":
            sd, T = val[1], val[2]
        else:
            sd, T = side, val
        ca, cb = decide(sd, T)
        ctl[nm] = {
            "route_a": "accepted" if ca["accepted"] else f"refused ({ca['n_bad_pairs']} pairs, walls {ca['bad_walls'][:5]})",
            "route_b": "accepted" if cb["accepted"] else f"refused ({cb['n_bad_pairs']} pairs, walls {cb['bad_walls'][:5]})",
        }
    rec["controls"] = ctl
    rec["cpu_s"] = round(time.process_time() - t0, 1)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items", nargs="+")
    ap.add_argument("--out", required=True)
    ns = ap.parse_args()
    res = []
    for it in ns.items:
        label, path = it.split("=", 1)
        r = run(label, path)
        print(json.dumps({k: r[k] for k in ("label", "n", "side_float", "side_minus_extent", "cpu_s")}), flush=True)
        print("  A:", r["route_a"]["accepted"], "least pair", r["route_a"]["least_pair_margin"], "least wall", r["route_a"]["least_wall"], flush=True)
        print("  B:", r["route_b"]["accepted"], "pairs by area", r["route_b"]["pairs_by_area"], "least wall", r["route_b"]["least_wall"], flush=True)
        print("  reader:", r["reader_controls"], flush=True)
        for k, v in r["controls"].items():
            print(f"  {k}: A {v['route_a']}; B {v['route_b']}", flush=True)
        res.append(r)
    with open(ns.out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
