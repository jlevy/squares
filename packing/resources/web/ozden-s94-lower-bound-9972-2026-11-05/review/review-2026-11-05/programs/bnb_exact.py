"""Exact branch and bound over a small region of centres for one oblique direction.

The same mathematics as bnb.py (README, "The deciders"), carried out entirely in exact
rationals (gmpy2.mpq), so no error budget enters: boxes have rational endpoints, the
inside/outside tests are exact, F(p0) is the exact capture by polygon clipping
(capture_exact.py), and each edge-length enclosure is computed exactly from its corner
values. A box is accepted when F(p0) - G_x d_x - G_y d_y >= T exactly. It is meant for
small regions (a crate leaf, a minimizer's neighbourhood), where it also reports the
least exact centre capture found.

Usage: bnb_exact.py CERT_GZ R X0 X1 Y0 Y1 OUT_JSON [--threshold a/b] [--max-boxes N]
(region bounds as exact rationals or decimal strings; a decimal string is read exactly)
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
from gmpy2 import mpq

from capture_exact import Evaluator, clip, poly_area
from xzcommon import direction, frac_str, load_certificate


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("r", type=int)
    ap.add_argument("x0")
    ap.add_argument("x1")
    ap.add_argument("y0")
    ap.add_argument("y1")
    ap.add_argument("out")
    ap.add_argument("--threshold", default="1")
    ap.add_argument("--max-boxes", type=int, default=20000)
    a = ap.parse_args()
    t0 = time.process_time()
    cert = load_certificate(Path(a.cert))
    ev = Evaluator(cert)
    dr = direction(cert, a.r)
    c, s, h = dr.c, dr.s, ev.h
    T = mpq(a.threshold)
    assert T >= 1
    region = [mpq(v) for v in (a.x0, a.x1, a.y0, a.y1)]
    keys = ev.keys
    rho = [ev.dens[k] for k in keys]
    arr = ev.arr
    ext = h * (c + s)

    def classify(px: mpq, py: mpq, dx: mpq, dy: mpq, idxs: list[int]) -> tuple[mpq, list[int]]:
        """Exact: mass of rectangles inside Q(p) for all p in the box; boundary list."""
        inside = mpq(0)
        bnd = []
        bu, bv = c * dx + s * dy, s * dx + c * dy
        for i in idxs:
            x1, y1, x2, y2 = keys[i]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            wx, wy = (x2 - x1) / 2, (y2 - y1) / 2
            DX, DY = mx - px, my - py
            du, dv = abs(c * DX + s * DY), abs(-s * DX + c * DY)
            eu, ev_ = c * wx + s * wy, s * wx + c * wy
            if du + eu + bu <= h and dv + ev_ + bv <= h:
                inside += rho[i] * (x2 - x1) * (y2 - y1)
            elif (du > eu + h + bu or dv > ev_ + h + bv or abs(DX) > wx + ext + dx or abs(DY) > wy + ext + dy):
                pass
            else:
                bnd.append(i)
        return inside, bnd

    def edge(corners: list[tuple[mpq, mpq]], at: mpq, e1: mpq, e2: mpq, vertical: bool):
        tops, bots = [], []
        for cx, cy in corners:
            if vertical:
                xi = at - cx
                tops.append((e2, cy + (h - c * xi) / s, cy + (h + s * xi) / c))
                bots.append((e1, cy + (-h - c * xi) / s, cy + (s * xi - h) / c))
            else:
                ze = at - cy
                tops.append((e2, cx + (h - s * ze) / c, cx + (c * ze + h) / s))
                bots.append((e1, cx + (-h - s * ze) / c, cx + (c * ze - h) / s))
        eta = [min(t) - max(b) for t, b in zip(tops, bots, strict=True)]
        lo = max(mpq(0), min(eta))
        hi = min(max(t[i] - b[j] for t, b in zip(tops, bots, strict=True)) for i in range(3) for j in range(3))
        hi = min(max(mpq(0), hi), e2 - e1)
        top_stable = any(all(t[i] <= min(t) for t in tops) for i in range(3))
        bot_stable = any(all(b[j] >= max(b) for b in bots) for j in range(3))
        sign = all(e >= 0 for e in eta) or all(e <= 0 for e in eta)
        stable = top_stable and bot_stable and sign
        return [max(mpq(0), e) for e in eta], lo, hi, stable

    def area_at(px: mpq, py: mpq, i: int) -> mpq:
        x1, y1, x2, y2 = keys[i]
        sq = ev.square(a.r, px, py)
        poly = clip(clip(clip(clip(sq, 0, x1, True), 0, x2, False), 1, y1, True), 1, y2, False)
        return poly_area(poly)

    x0r, x1r, y0r, y1r = region
    near = np.nonzero(
        (arr[:, 0] < float(x1r) + 1.5) & (arr[:, 2] > float(x0r) - 1.5)
        & (arr[:, 1] < float(y1r) + 1.5) & (arr[:, 3] > float(y0r) - 1.5)
    )[0].tolist()
    stack = [(x0r, x1r, y0r, y1r, mpq(0), near)]
    boxes = 0
    accepted = 0
    least_bound = None
    least_centre = None
    least_centre_at = None
    status = "verified"
    while stack:
        bx0, bx1, by0, by1, inherited, cand = stack.pop()
        boxes += 1
        if boxes > a.max_boxes:
            status = "unresolved"
            break
        px, py = (bx0 + bx1) / 2, (by0 + by1) / 2
        dx, dy = (bx1 - bx0) / 2, (by1 - by0) / 2
        ins, bnd = classify(px, py, dx, dy, cand)
        inside = inherited + ins
        F0 = inside + sum((rho[i] * area_at(px, py, i) for i in bnd), mpq(0))
        if least_centre is None or F0 < least_centre:
            least_centre, least_centre_at = F0, (px, py)
        if F0 < T:
            status = "counterexample"
            break
        corners = [(bx0, by0), (bx0, by1), (bx1, by0), (bx1, by1)]
        G = []
        for vertical in (True, False):
            S = [mpq(0)] * 4
            ilo = mpq(0)
            ihi = mpq(0)
            for i in bnd:
                x1, y1, x2, y2 = keys[i]
                if vertical:
                    s1, lo1, hi1, st1 = edge(corners, x1, y1, y2, True)
                    s2, lo2, hi2, st2 = edge(corners, x2, y1, y2, True)
                    cap = min(y2 - y1, (x2 - x1) / (s * c))
                else:
                    s1, lo1, hi1, st1 = edge(corners, y1, x1, x2, False)
                    s2, lo2, hi2, st2 = edge(corners, y2, x1, x2, False)
                    cap = min(x2 - x1, (y2 - y1) / (s * c))
                if st1 and st2:
                    for j in range(4):
                        S[j] += rho[i] * (s1[j] - s2[j])
                else:
                    ilo += rho[i] * max(lo1 - hi2, -cap)
                    ihi += rho[i] * min(hi1 - lo2, cap)
            glo = min(S) + ilo
            ghi = max(S) + ihi
            G.append(max(abs(glo), abs(ghi)))
        bound = F0 - G[0] * dx - G[1] * dy
        if bound >= T:
            accepted += 1
            if least_bound is None or bound < least_bound:
                least_bound = bound
            continue
        if G[0] * dx >= G[1] * dy:
            m = px
            stack.append((bx0, m, by0, by1, inside, bnd))
            stack.append((m, bx1, by0, by1, inside, bnd))
        else:
            m = py
            stack.append((bx0, bx1, by0, m, inside, bnd))
            stack.append((bx0, bx1, m, by1, inside, bnd))
    in_quadrant = all(cert.L / 2 <= v <= dr.U for v in region)
    rep = {
        "r": a.r,
        "region": [frac_str(v) for v in region],
        "region_float": [float(v) for v in region],
        "region_in_quadrant": in_quadrant,
        "threshold": frac_str(T),
        "status": status,
        "boxes": boxes,
        "accepted": accepted,
        "least_exact_bound": float(least_bound) if least_bound is not None else None,
        "least_exact_bound_rational_digits": len(frac_str(least_bound)) if least_bound is not None else None,
        "least_centre_capture": float(least_centre) if least_centre is not None else None,
        "least_centre_at": [frac_str(v) for v in least_centre_at] if least_centre_at else None,
        "cpu_seconds": time.process_time() - t0,
    }
    for k, v in rep.items():
        print(f"{k}: {v}")
    Path(a.out).write_text(json.dumps(rep, indent=1) + "\n")
    return 0 if status == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
