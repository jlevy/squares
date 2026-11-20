"""C2: the 21-point covering lemma for s(18), decided by an exact branch and bound.

Usage:
  python -I r1050_rack.py --rack stabs18-endpoint-window.json --out out.json
      [--erosion P/Q] [--drop X,Y]

Claim checked (strong form): for every angle theta and every centre c such that the
closed unit square at (c, theta) lies in [0, U]^2, some mark m has
||R(-theta)(m - c)||_inf < (1 - eps)/2, where U is the rack's cap, the marks are the
orbit closure of its lattice representatives scaled by U/scale, and eps its erosion.

Method. theta is parametrised by t = tan(theta/2) in [0, T], T = 4143/10000 > tan(pi/8);
the diagonal reflection (which maps the rack to itself, checked) and the square's own
quarter-turn symmetry reduce every angle to [0, pi/4]. Centres range over the whole box.
A cell [t0,t1] x [x0,x1] x [y0,y1] is closed exactly in one of two ways:
  * infeasible: the wall half-width w = (cos + sin)/2 is concave on [0, pi/2], so its
    least value on the cell is at t0 or t1, and every centre of the cell lies strictly
    outside [w_min, U - w_min] in some coordinate;
  * captured by one mark p: with d = p - c, each of d.u < h, -d.u < h, d.v < h, -d.v < h
    (u = (cos, sin), v = (-sin, cos), h = (1-eps)/2) becomes, after multiplying by
    1 + t^2 > 0, a polynomial linear in d and quadratic in t; its maximum over the cell
    is the maximum over the four corners of d of the maximum of a quadratic on [t0, t1],
    computed exactly (endpoints and the vertex).
Floats only choose which mark to try and where to split. Cells are closed, and children
share their boundaries, so the leaves cover the root. A cell that cannot be closed by
depth 96 is reported undecided. At every cell that is not closed, the centre and corner
poses are tested in floats and, if one looks uncovered, exactly; an exact uncovered pose
(a witness of failure) stops the search.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

T_MAX = Fraction(4143, 10000)
MAX_DEPTH = 96

F = Fraction


def strict_q(s: str) -> Fraction:
    if not isinstance(s, str) or "e" in s.lower():
        raise ValueError(f"bad number {s!r}")
    return Fraction(s)


def d4(x: int, y: int, s: int) -> list[tuple[int, int]]:
    return [(x, y), (s - x, y), (x, s - y), (s - x, s - y),
            (y, x), (s - y, x), (y, s - x), (s - y, s - x)]


def load_rack(path: Path) -> tuple[Fraction, int, Fraction, list[tuple[int, int]], int]:
    raw = json.loads(path.read_text())
    want = {"cap", "orbits", "scale", "erosion", "depth", "marks"}
    if set(raw) != want:
        raise ValueError(f"unexpected rack keys {sorted(raw)}")
    cap = strict_q(raw["cap"])
    scale = raw["scale"]
    eps = strict_q(raw["erosion"])
    pts: set[tuple[int, int]] = set()
    for x, y in raw["orbits"]:
        if not (isinstance(x, int) and isinstance(y, int) and 0 < x < scale and 0 < y < scale):
            raise ValueError("bad orbit representative")
        pts.update(d4(x, y, scale))
    return cap, scale, eps, sorted(pts), raw["marks"]


def w_of(t: Fraction) -> Fraction:
    return (1 - t * t + 2 * t) / (2 * (1 + t * t))


def qmax_on(a: Fraction, b: Fraction, c: Fraction, t0: Fraction, t1: Fraction) -> Fraction:
    """max of a t^2 + b t + c on [t0, t1], exactly."""
    m = max(a * t0 * t0 + b * t0 + c, a * t1 * t1 + b * t1 + c)
    if a < 0:
        tv = -b / (2 * a)
        if t0 < tv < t1:
            m = max(m, a * tv * tv + b * tv + c)
    return m


def capture_exact(p: tuple[Fraction, Fraction], cell: tuple[Fraction, ...], h: Fraction) -> bool:
    t0, t1, x0, x1, y0, y1 = cell
    for dx in (p[0] - x1, p[0] - x0):
        for dy in (p[1] - y1, p[1] - y0):
            forms = (
                (-dx - h, 2 * dy, dx - h),
                (dx - h, -2 * dy, -dx - h),
                (-dy - h, -2 * dx, dy - h),
                (dy - h, 2 * dx, -dy - h),
            )
            for a, b, c in forms:
                if qmax_on(a, b, c, t0, t1) >= 0:
                    return False
    return True


def capture_float(p: tuple[float, float], cell: tuple[float, ...], h: float) -> float:
    """Float estimate of the largest form value (negative means captured)."""
    t0, t1, x0, x1, y0, y1 = cell
    worst = -1e300
    for dx in (p[0] - x1, p[0] - x0):
        for dy in (p[1] - y1, p[1] - y0):
            for a, b, c in ((-dx - h, 2 * dy, dx - h), (dx - h, -2 * dy, -dx - h),
                            (-dy - h, -2 * dx, dy - h), (dy - h, 2 * dx, -dy - h)):
                m = max(a * t0 * t0 + b * t0 + c, a * t1 * t1 + b * t1 + c)
                if a < 0:
                    tv = -b / (2 * a)
                    if t0 < tv < t1:
                        m = max(m, a * tv * tv + b * tv + c)
                worst = max(worst, m)
    return worst


def infeasible_exact(cell: tuple[Fraction, ...], cap: Fraction) -> bool:
    t0, t1, x0, x1, y0, y1 = cell
    wmin = min(w_of(t0), w_of(t1))
    return x1 < wmin or x0 > cap - wmin or y1 < wmin or y0 > cap - wmin


def pose_uncovered(c: tuple[Fraction, Fraction], t: Fraction, marks: list[tuple[Fraction, Fraction]],
                   h: Fraction, cap: Fraction) -> bool:
    """Exact: the tile at (c, t) is inside the box and no mark is captured."""
    w = w_of(t)
    if not (w <= c[0] <= cap - w and w <= c[1] <= cap - w):
        return False
    cs, sn = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    for p in marks:
        dx, dy = p[0] - c[0], p[1] - c[1]
        if abs(dx * cs + dy * sn) < h and abs(-dx * sn + dy * cs) < h:
            return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rack", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--erosion", default=None)
    ap.add_argument("--drop", default=None, help="lattice point X,Y to remove from the rack")
    args = ap.parse_args()

    start = time.process_time()
    cap, scale, eps, lattice, nmarks = load_rack(args.rack)
    premises = {
        "marks_from_orbits": len(lattice),
        "marks_declared": nmarks,
        "reflection_invariant": sorted((y, x) for x, y in lattice) == lattice,
        "d4_invariant": all(sorted(d4(x, y, scale)[k] for x, y in lattice) == lattice
                            for k in range(8)),
        "T_exceeds_tan_pi_8": (T_MAX + 1) ** 2 > 2,
        "cap": str(cap),
        "cap_exceeds_H": (2 * cap - 7) > 0 and (2 * cap - 7) ** 2 > 7,
    }
    if args.erosion is not None:
        eps = Fraction(args.erosion)
    if args.drop is not None:
        dx, dy = (int(v) for v in args.drop.split(","))
        lattice = [q for q in lattice if q != (dx, dy)]
    marks = [(F(x) * cap / scale, F(y) * cap / scale) for x, y in lattice]
    fmarks = [(float(a), float(b)) for a, b in marks]
    h = (1 - eps) / 2
    fh = float(h)
    fcap = float(cap)

    stack: list[tuple[tuple[Fraction, ...], int]] = [((F(0), T_MAX, F(0), cap, F(0), cap), 0)]
    leaves_captured = 0
    leaves_infeasible = 0
    max_depth = 0
    mark_use = [0] * len(marks)
    undecided: list[dict[str, object]] = []
    witnesses: list[dict[str, object]] = []
    while stack:
        cell, depth = stack.pop()
        max_depth = max(max_depth, depth)
        t0, t1, x0, x1, y0, y1 = cell
        if infeasible_exact(cell, cap):
            leaves_infeasible += 1
            continue
        fcell = tuple(float(v) for v in cell)
        # Try marks near the cell, best float estimate first.
        cands = []
        for k, p in enumerate(fmarks):
            if p[0] < fcell[2] - 0.75 or p[0] > fcell[3] + 0.75 or p[1] < fcell[4] - 0.75 \
                    or p[1] > fcell[5] + 0.75:
                continue
            cands.append((capture_float(p, fcell, fh), k))
        cands.sort()
        closed = False
        for est, k in cands[:3]:
            if est < -1e-12 and capture_exact(marks[k], cell, h):
                leaves_captured += 1
                mark_use[k] += 1
                closed = True
                break
        if closed:
            continue
        # Is the centre or a corner pose of this cell uncovered? Lenient floats, then exactly.
        hit = None
        for xm, ym, tm in [((x0 + x1) / 2, (y0 + y1) / 2, (t0 + t1) / 2)] + [
                (xx, yy, tt) for tt in (t0, t1) for xx in (x0, x1) for yy in (y0, y1)]:
            fx, fy, ft = float(xm), float(ym), float(tm)
            fw = (1 - ft * ft + 2 * ft) / (2 * (1 + ft * ft))
            if not (fw - 1e-9 <= fx <= fcap - fw + 1e-9 and fw - 1e-9 <= fy <= fcap - fw + 1e-9):
                continue
            fc, fs = (1 - ft * ft) / (1 + ft * ft), 2 * ft / (1 + ft * ft)
            if all(max(abs((p[0] - fx) * fc + (p[1] - fy) * fs),
                       abs(-(p[0] - fx) * fs + (p[1] - fy) * fc)) > fh - 1e-9 for p in fmarks) \
                    and pose_uncovered((xm, ym), tm, marks, h, cap):
                hit = (xm, ym, tm)
                break
        if hit is not None:
            witnesses.append({"cell_float": [float(v) for v in cell], "depth": depth,
                              "witness": {"cx": str(hit[0]), "cy": str(hit[1]), "t": str(hit[2]),
                                          "float": [float(v) for v in hit]}})
            break
        if depth >= MAX_DEPTH:
            undecided.append({"cell_float": [float(v) for v in cell]})
            if len(undecided) > 50:
                break
            continue
        # Split the widest dimension (t weighted by 1.5: a turn moves capture squares
        # by about |d| * 2 dt with |d| <= 0.75).
        sizes = [1.5 * (fcell[1] - fcell[0]), fcell[3] - fcell[2], fcell[5] - fcell[4]]
        dim = sizes.index(max(sizes))
        lo, hi = cell[2 * dim], cell[2 * dim + 1]
        mid = (lo + hi) / 2
        a = list(cell)
        b = list(cell)
        a[2 * dim + 1] = mid
        b[2 * dim] = mid
        stack.append((tuple(a), depth + 1))
        stack.append((tuple(b), depth + 1))

    if witnesses:
        verdict = "UNCOVERED_POSE_FOUND"
    elif undecided or stack:
        verdict = "UNDECIDED"
    else:
        verdict = "COVERED"
    report = {
        "program": "r1050_rack.py",
        "premises": premises,
        "erosion": str(eps),
        "dropped": args.drop,
        "marks_used": len(marks),
        "leaves_captured": leaves_captured,
        "leaves_infeasible": leaves_infeasible,
        "max_depth": max_depth,
        "captures_per_mark": {f"{x},{y}": mark_use[k] for k, (x, y) in enumerate(lattice)},
        "witnesses": witnesses[:5],
        "undecided": undecided[:5],
        "cpu_seconds": round(time.process_time() - start, 1),
        "verdict": verdict,
    }
    args.out.write_text(json.dumps(report, indent=1) + "\n")
    print(verdict, f"captured {leaves_captured}", f"infeasible {leaves_infeasible}",
          f"depth {max_depth}", f"cpu {report['cpu_seconds']}s",
          "premises", all(v is True for k, v in premises.items() if k not in ("cap", "marks_from_orbits", "marks_declared"))
          and premises["marks_from_orbits"] == premises["marks_declared"])
    return 0 if verdict == "COVERED" else 1


if __name__ == "__main__":
    sys.exit(main())
