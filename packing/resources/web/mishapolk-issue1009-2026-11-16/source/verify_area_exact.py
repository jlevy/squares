#!/usr/bin/env python3
"""Independent exact-rational square-packing verifier by polygon clipping.

Uses Python standard library `fractions.Fraction` only and shares no geometry
code with `verify_bound_certificate.py`. For each unit square in a `.cert`
file (`n S` header followed by `x y t` lines), this script:
  1. Constructs the four exact rational vertices from `(x, y)` and
     `(c, s) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))`, checking exact unit
     edge vectors and orthogonality.
  2. Verifies strict open-container inclusion: every vertex `(vx, vy)` lies
     strictly inside `(0, S)^2`, recording the minimum exact wall clearance.
  3. Clips every pair of squares whose centres satisfy `|dc|^2 <= 2` against
     one another via exact rational Sutherland-Hodgman half-plane clipping,
     verifying that the intersection polygon is empty (strict separation) or,
     without `--strict`, has area identically `0`.
"""
from __future__ import annotations

import argparse
import sys
from fractions import Fraction
from pathlib import Path

HALF = Fraction(1, 2)


def load_cert_vertices(path: Path) -> tuple[int, Fraction, list[tuple[Fraction, Fraction, list[tuple[Fraction, Fraction]]]]]:
    rows = [
        line.split()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not rows or len(rows[0]) != 2:
        raise ValueError(f"{path}: expected 'n S' header")
    n = int(rows[0][0])
    side = Fraction(rows[0][1])
    if n < 1 or side <= 0 or len(rows) != n + 1:
        raise ValueError(f"{path}: square count mismatch (expected {n}, got {len(rows) - 1})")

    polys = []
    for row in rows[1:]:
        if len(row) != 3:
            raise ValueError(f"{path}: expected 'x y t' row")
        cx, cy, t = Fraction(row[0]), Fraction(row[1]), Fraction(row[2])
        denom = 1 + t * t
        ux = HALF * (1 - t * t) / denom
        uy = t / denom
        vx, vy = -uy, ux
        # Check exact half-edge lengths (|u|^2 == 1/4, |v|^2 == 1/4, u.v == 0)
        if ux * ux + uy * uy != Fraction(1, 4) or vx * vx + vy * vy != Fraction(1, 4) or ux * vx + uy * vy != 0:
            raise ValueError(f"{path}: invalid rational frame")
        # Counter-clockwise vertices
        verts = [
            (cx - ux - vx, cy - uy - vy),
            (cx + ux - vx, cy + uy - vy),
            (cx + ux + vx, cy + uy + vy),
            (cx - ux + vx, cy - uy + vy),
        ]
        polys.append((cx, cy, verts))
    return n, side, polys


def clip_polygon_ccw(
    subject: list[tuple[Fraction, Fraction]],
    clipper: list[tuple[Fraction, Fraction]],
    strict_disjoint_closed: bool,
) -> list[tuple[Fraction, Fraction]]:
    """Clip `subject` against convex CCW `clipper` using exact rational arithmetic."""
    output = list(subject)
    m = len(clipper)
    for k in range(m):
        if not output:
            break
        ax, ay = clipper[k]
        bx, by = clipper[(k + 1) % m]
        ex, ey = bx - ax, by - ay

        def inside(pt: tuple[Fraction, Fraction]) -> bool:
            cross = ex * (pt[1] - ay) - ey * (pt[0] - ax)
            return cross >= 0 if strict_disjoint_closed else cross > 0

        def intersect(p1: tuple[Fraction, Fraction], p2: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
            c1 = ex * (p1[1] - ay) - ey * (p1[0] - ax)
            c2 = ex * (p2[1] - ay) - ey * (p2[0] - ax)
            denom = c1 - c2
            if denom == 0:
                return p1
            alpha = c1 / denom
            return (p1[0] + alpha * (p2[0] - p1[0]), p1[1] + alpha * (p2[1] - p1[1]))

        inp = output
        output = []
        prev = inp[-1]
        prev_in = inside(prev)
        for cur in inp:
            cur_in = inside(cur)
            if cur_in:
                if not prev_in:
                    output.append(intersect(prev, cur))
                output.append(cur)
            elif prev_in:
                output.append(intersect(prev, cur))
            prev, prev_in = cur, cur_in
    return output


def polygon_twice_area(pts: list[tuple[Fraction, Fraction]]) -> Fraction:
    if len(pts) < 3:
        return Fraction(0)
    acc = Fraction(0)
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        acc += x1 * y2 - x2 * y1
    return abs(acc)


def check_certificate(path: Path, strict: bool = True) -> dict:
    n, side, polys = load_cert_vertices(path)
    min_wall: Fraction | None = None
    for _, _, verts in polys:
        for x, y in verts:
            m = min(x, side - x, y, side - y)
            if min_wall is None or m < min_wall:
                min_wall = m

    assert min_wall is not None
    wall_ok = (min_wall > 0) if strict else (min_wall >= 0)

    close_pairs = 0
    overlap_pairs = 0
    for i in range(n):
        cxi, cyi, vi = polys[i]
        for j in range(i + 1, n):
            cxj, cyj, vj = polys[j]
            dx, dy = cxj - cxi, cyj - cyi
            if dx * dx + dy * dy > 2:
                continue
            close_pairs += 1
            clipped = clip_polygon_ccw(vi, vj, strict_disjoint_closed=strict)
            if strict:
                if clipped:
                    overlap_pairs += 1
            else:
                if polygon_twice_area(clipped) > 0:
                    overlap_pairs += 1

    ok = wall_ok and overlap_pairs == 0
    return {
        "file": str(path),
        "n": n,
        "side": str(side),
        "close_pairs_clipped": close_pairs,
        "min_wall_float": float(min_wall),
        "overlap_pairs": overlap_pairs,
        "valid": ok,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify .cert files via exact rational polygon clipping.")
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--strict", action="store_true", help="Require open-container inclusion and disjoint closed squares.")
    args = ap.parse_args()

    all_ok = True
    for p in args.paths:
        res = check_certificate(p, strict=args.strict)
        status = "VALID" if res["valid"] else "INVALID"
        print(
            f"{status}: n={res['n']} ({p.name}) | close_pairs={res['close_pairs_clipped']} "
            f"| min_wall={res['min_wall_float']:.3e} | overlaps={res['overlap_pairs']}"
        )
        if not res["valid"]:
            all_ok = False
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
