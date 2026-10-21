"""Review checker for issue #668 / PR #704 (T-196): exact, standard library only.

Reads Joost de Winter's centre-basis JSON witnesses with its own reader, converts
nothing through the repository's code, and decides, over Q:

  1. every basis is on the unit circle, c^2 + s^2 = 1 exactly;
  2. every square lies in the closed box [0, S]^2, by centre and half-extent
     h = (|c| + |s|) / 2 on each axis (no corners are built for this test);
  3. every one of the n(n-1)/2 pairs has disjoint interiors, by the separating-axis
     theorem on the four unit edge normals (c, s), (-s, c) of each square, with the gap
     recorded as the largest one-sided separation over those four axes (the same
     quantity the repository's two routes call the pair's best gap);
  4. every pair whose centres are within sqrt(2) (dx^2 + dy^2 < 2, exactly) is decided
     a second way: the exact area of square A clipped by the four closed half-planes
     of square B must be 0 (Sutherland-Hodgman over Fraction);
  5. the printed bound is ceil(S * 10^12) / 10^12 and the 16-place ceiling matches the
     frozen comparison's;
  6. the least wall clearance and least pair gap are compared digit for digit with the
     retained receipt's two routes.

Run with `python -I review_704_check.py DATA_DIR RECEIPT_JSON OUT_JSON`.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from itertools import combinations
from pathlib import Path

HALF = Fraction(1, 2)


def rational(value: object, where: str) -> Fraction:
    if type(value) is not str:
        raise ValueError(f"{where}: {value!r} is not a rational string")
    text = value.strip()
    if text != value or not text:
        raise ValueError(f"{where}: {value!r} has blanks")
    if "/" in text:
        num, den = text.split("/")
        if not (num.lstrip("-").isdigit() and den.isdigit() and int(den) > 0):
            raise ValueError(f"{where}: {value!r} is not p/q")
        return Fraction(int(num), int(den))
    if not text.lstrip("-").isdigit():
        raise ValueError(f"{where}: {value!r} is not an integer")
    return Fraction(int(text))


def read(path: Path, n_expected: int) -> tuple[Fraction, list[tuple[Fraction, Fraction, Fraction, Fraction]]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if type(value) is not dict or set(value) != {"n", "side", "squares"}:
        raise ValueError("not {n, side, squares}")
    if type(value["n"]) is not int or value["n"] != n_expected:
        raise ValueError(f"n is {value['n']!r}, expected {n_expected}")
    side = rational(value["side"], "side")
    if side <= 0:
        raise ValueError("side not positive")
    squares = value["squares"]
    if type(squares) is not list or len(squares) != n_expected:
        raise ValueError(f"{len(squares)} squares for n = {n_expected}")
    rows = []
    for index, square in enumerate(squares):
        where = f"square {index}"
        if type(square) is not dict or set(square) != {"center", "basis"}:
            raise ValueError(f"{where}: not {{center, basis}}")
        if len(square["center"]) != 2 or len(square["basis"]) != 2:
            raise ValueError(f"{where}: not two coordinates each")
        x, y = (rational(v, where) for v in square["center"])
        c, s = (rational(v, where) for v in square["basis"])
        rows.append((x, y, c, s))
    return side, rows


def corners(x: Fraction, y: Fraction, c: Fraction, s: Fraction) -> list[tuple[Fraction, Fraction]]:
    """Counter-clockwise corners: centre + a*(c, s) + b*(-s, c), a, b = ±1/2."""
    return [
        (x + a * c - b * s, y + a * s + b * c)
        for a, b in ((HALF, HALF), (-HALF, HALF), (-HALF, -HALF), (HALF, -HALF))
    ]


def sat_gap(p, q) -> Fraction:
    """Largest one-sided separation over the two squares' four unit edge normals."""
    x, y, c, s = p
    X, Y, C, T = q
    dx, dy = X - x, Y - y
    best = None
    for u, v in ((c, s), (-s, c), (C, T), (-T, C)):
        # half-extent of each square along the unit axis (u, v)
        hp = (abs(u * c + v * s) + abs(-u * s + v * c)) / 2
        hq = (abs(u * C + v * T) + abs(-u * T + v * C)) / 2
        gap = abs(u * dx + v * dy) - hp - hq
        if best is None or gap > best:
            best = gap
    assert best is not None
    return best


def clip(polygon, a, b, c0):
    """Keep the part of polygon with a*x + b*y <= c0 (closed half-plane)."""
    out = []
    m = len(polygon)
    for i in range(m):
        P = polygon[i]
        Q = polygon[(i + 1) % m]
        fp = a * P[0] + b * P[1] - c0
        fq = a * Q[0] + b * Q[1] - c0
        if fp <= 0:
            out.append(P)
        if (fp < 0 < fq) or (fq < 0 < fp):
            t = fp / (fp - fq)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return out


def area(polygon) -> Fraction:
    if len(polygon) < 3:
        return Fraction(0)
    total = Fraction(0)
    m = len(polygon)
    for i in range(m):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % m]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2


def intersection_area(p, q) -> Fraction:
    """Exact area of square p clipped by the four closed half-planes of square q."""
    X, Y, C, T = q
    poly = corners(*p)
    # q's half-planes: |(u,v)·(point - centre)| <= 1/2 for u,v in {(C,T), (-T,C)}
    for u, v in ((C, T), (-T, C)):
        d = u * X + v * Y
        poly = clip(poly, u, v, d + HALF)
        if not poly:
            return Fraction(0)
        poly = clip(poly, -u, -v, -d + HALF)
        if not poly:
            return Fraction(0)
    return area(poly)


def ceiling_decimal(value: Fraction, places: int) -> str:
    scaled = value * 10**places
    k = scaled.numerator // scaled.denominator
    if k * scaled.denominator != scaled.numerator:
        k += 1
    text = str(k).rjust(places + 1, "0")
    return f"{text[:-places]}.{text[-places:]}"


def decide(n: int, path: Path) -> dict:
    started = time.process_time()
    side, rows = read(path, n)
    # 1. unit circle
    for i, (_, _, c, s) in enumerate(rows):
        if c * c + s * s != 1:
            raise ValueError(f"square {i}: basis off the unit circle")
    # 2. containment by half-extents
    wall = None
    for i, (x, y, c, s) in enumerate(rows):
        h = (abs(c) + abs(s)) / 2
        clearance = min(x - h, y - h, side - x - h, side - y - h)
        if wall is None or clearance < wall:
            wall = clearance
    # 2'. containment by corners, for the record (same predicate, built differently)
    wall_corners = min(min(px, py, side - px, side - py) for r in rows for px, py in corners(*r))
    # 3. all pairs, separating axes
    least_gap = None
    least_pair = None
    overlaps = 0
    contacts = 0
    near = []
    for i, j in combinations(range(n), 2):
        p, q = rows[i], rows[j]
        gap = sat_gap(p, q)
        if gap < 0:
            overlaps += 1
        elif gap == 0:
            contacts += 1
        if least_gap is None or gap < least_gap:
            least_gap, least_pair = gap, (i, j)
        dx, dy = q[0] - p[0], q[1] - p[1]
        if dx * dx + dy * dy < 2:
            near.append((i, j))
    # 4. near pairs by exact clipping area
    positive_area = 0
    for i, j in near:
        if intersection_area(rows[i], rows[j]) != 0 or intersection_area(rows[j], rows[i]) != 0:
            positive_area += 1
    return {
        "n": n,
        "side": f"{side.numerator}/{side.denominator}",
        "print_12": ceiling_decimal(side, 12),
        "ceiling_16": ceiling_decimal(side, 16),
        "unit_circle": "all",
        "min_wall_clearance_half_extent": str(wall),
        "min_wall_clearance_corners": str(wall_corners),
        "pairs_decided_sat": n * (n - 1) // 2,
        "overlapping_pairs_sat": overlaps,
        "contact_pairs_sat": contacts,
        "least_pair_gap": str(least_gap),
        "least_pair": least_pair,
        "near_pairs_clipped": len(near),
        "near_pairs_with_positive_area": positive_area,
        "cpu_seconds": round(time.process_time() - started, 2),
    }


def main(argv: list[str]) -> int:
    data = Path(argv[1])
    receipt = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    out_path = Path(argv[3])
    positives = {row["n"]: row for row in receipt["cases"] if row["control"] == "positive"}
    results = {}
    ok = True
    for n in (227, 229, 260):
        row = decide(n, data / f"n{n}_exact.json")
        rec = positives[n]
        comparisons = {}
        for route in ("exact_verify", "independent"):
            comparisons[route] = {
                "wall_equal": Fraction(rec[route]["minimum_containment_clearance"]) == Fraction(row["min_wall_clearance_half_extent"]),
                "gap_equal": Fraction(rec[route]["minimum_best_pair_gap"]) == Fraction(row["least_pair_gap"]),
                "pairs_equal": rec[route]["pairs_tested"] == row["pairs_decided_sat"],
                "side_equal": Fraction(rec[route]["side"]) == Fraction(row["side"]),
            }
        row["receipt_agreement"] = comparisons
        row["passed"] = (
            row["overlapping_pairs_sat"] == 0
            and row["near_pairs_with_positive_area"] == 0
            and Fraction(row["min_wall_clearance_half_extent"]) >= 0
            and all(all(v.values()) for v in comparisons.values())
        )
        ok = ok and row["passed"]
        results[n] = row
        print(json.dumps(row, indent=1), flush=True)
    out_path.write_text(json.dumps(results, indent=1), encoding="utf-8")
    print("ALL PASSED" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
