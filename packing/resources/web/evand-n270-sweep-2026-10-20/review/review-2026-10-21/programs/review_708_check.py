"""Review checker for issue #703 / PR #708 (T-224): exact, standard library only.

Reads Evan Daniel's `evand-cert` text format with its own reader, converts nothing
through the repository's code, and decides over Q:

  1. the file holds a header `n S` and then exactly n rows `x y t` of rational literals;
  2. the half-angle map c = (1 - t^2)/(1 + t^2), s = 2t/(1 + t^2) lands on the unit
     circle, c^2 + s^2 = 1 exactly, for every row (an identity, checked anyway);
  3. every square's four corners lie in the closed box [0, S]^2 (also by half-extent
     h = (|c| + |s|)/2, which must agree);
  4. every one of the n(n-1)/2 pairs has disjoint interiors by the separating-axis
     theorem on the four unit edge normals of the two squares, the gap recorded as the
     largest one-sided separation over those axes (the quantity both maintained routes
     call the pair's best gap); contact (gap 0) is allowed, the problem being closed;
  5. every pair whose centres are within sqrt(2) (dx^2 + dy^2 < 2, exactly) is decided a
     second way: the exact area of square A clipped by the four closed half-planes of
     square B must be 0 (Sutherland-Hodgman over Fraction);
  6. the printed bound is ceil(S * 10^12)/10^12 and the 16-place ceiling is reported;
  7. the least wall clearance, least pair gap, closest pair, pair count and side are
     compared digit for digit with the retained receipt's two routes, when given.

Run with `python -I review_708_check.py CERT N OUT_JSON [RECEIPT_JSON]`.
"""

from __future__ import annotations

import json
import math
import sys
import time
from fractions import Fraction
from itertools import combinations
from pathlib import Path

HALF = Fraction(1, 2)
Square = tuple[Fraction, Fraction, Fraction, Fraction]


def rational(text: str, where: str) -> Fraction:
    if "/" in text:
        num, den = text.split("/")
        if not (num.lstrip("-").isdigit() and den.isdigit() and int(den) > 0):
            raise ValueError(f"{where}: {text!r} is not p/q")
        return Fraction(int(num), int(den))
    if not text.lstrip("-").isdigit():
        raise ValueError(f"{where}: {text!r} is not an integer literal")
    return Fraction(int(text))


def read(path: Path, n_expected: int) -> tuple[Fraction, list[Square], list[Fraction]]:
    lines = [ln for ln in path.read_text(encoding="ascii").split("\n") if ln.strip() and not ln.startswith("#")]
    head = lines[0].split()
    if len(head) != 2:
        raise ValueError("header is not `n S`")
    n = int(head[0])
    if n != n_expected:
        raise ValueError(f"n is {n}, expected {n_expected}")
    side = rational(head[1], "side")
    if side <= 0:
        raise ValueError("side not positive")
    rows = lines[1:]
    if len(rows) != n:
        raise ValueError(f"{len(rows)} rows for n = {n}")
    squares: list[Square] = []
    tangents: list[Fraction] = []
    for index, row in enumerate(rows):
        parts = row.split()
        if len(parts) != 3:
            raise ValueError(f"row {index}: {len(parts)} fields")
        x, y, t = (rational(p, f"row {index}") for p in parts)
        tt = t * t
        c = (1 - tt) / (1 + tt)
        s = 2 * t / (1 + tt)
        if c * c + s * s != 1:
            raise ValueError(f"row {index}: not on the unit circle")
        squares.append((x, y, c, s))
        tangents.append(t)
    return side, squares, tangents


def corners(sq: Square) -> list[tuple[Fraction, Fraction]]:
    x, y, c, s = sq
    return [(x + a * c - b * s, y + a * s + b * c) for a, b in ((-HALF, -HALF), (HALF, -HALF), (HALF, HALF), (-HALF, HALF))]


def wall_clearance(sq: Square, side: Fraction) -> Fraction:
    """Least distance from any corner to any wall of the closed box; negative if outside."""
    cs = corners(sq)
    least = min(min(px, side - px, py, side - py) for px, py in cs)
    x, y, c, s = sq
    h = (abs(c) + abs(s)) / 2
    by_extent = min(x - h, side - x - h, y - h, side - y - h)
    if by_extent != least:
        raise AssertionError("corner and half-extent clearances disagree")
    return least


def sat_gap(p: Square, q: Square) -> tuple[Fraction, int]:
    """Largest one-sided separation over the four face normals; >= 0 means disjoint interiors."""
    x, y, c, s = p
    X, Y, C, T = q
    dx, dy = X - x, Y - y
    best = None
    best_axis = -1
    for k, (u, v) in enumerate(((c, s), (-s, c), (C, T), (-T, C))):
        hp = (abs(u * c + v * s) + abs(-u * s + v * c)) / 2
        hq = (abs(u * C + v * T) + abs(-u * T + v * C)) / 2
        gap = abs(u * dx + v * dy) - hp - hq
        if best is None or gap > best:
            best, best_axis = gap, k
    assert best is not None
    return best, best_axis


def clip(poly: list[tuple[Fraction, Fraction]], a: Fraction, b: Fraction, c0: Fraction) -> list[tuple[Fraction, Fraction]]:
    """Keep the part of poly with a*x + b*y <= c0 (closed half-plane)."""
    out: list[tuple[Fraction, Fraction]] = []
    m = len(poly)
    for i in range(m):
        P, Q = poly[i], poly[(i + 1) % m]
        fp, fq = a * P[0] + b * P[1] - c0, a * Q[0] + b * Q[1] - c0
        if fp <= 0:
            out.append(P)
        if (fp < 0 < fq) or (fq < 0 < fp):
            t = fp / (fp - fq)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return out


def intersection_area(p: Square, q: Square) -> Fraction:
    poly = corners(p)
    X, Y, C, T = q
    for u, v in ((C, T), (-C, -T), (-T, C), (T, -C)):
        poly = clip(poly, u, v, u * X + v * Y + HALF)
        if len(poly) < 3:
            return Fraction(0)
    area = Fraction(0)
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2


def lit(v: Fraction) -> str:
    return f"{v.numerator}/{v.denominator}" if v.denominator != 1 else str(v.numerator)


def ceil_at(v: Fraction, places: int) -> str:
    scaled = -(-v.numerator * 10**places // v.denominator)
    text = str(scaled).rjust(places + 1, "0")
    return text[:-places] + "." + text[-places:]


def check(path: Path, n: int) -> dict:
    started = time.process_time()
    side, squares, tangents = read(path, n)
    # containment
    wall = None
    wall_square = -1
    for i, sq in enumerate(squares):
        cl = wall_clearance(sq, side)
        if wall is None or cl < wall:
            wall, wall_square = cl, i
    assert wall is not None
    # pairs
    least = None
    least_pair = (-1, -1)
    pairs = 0
    near = 0
    overlaps: list[tuple[int, int, str]] = []
    clip_fail: list[tuple[int, int, str]] = []
    for i, j in combinations(range(n), 2):
        pairs += 1
        p, q = squares[i], squares[j]
        gap, _axis = sat_gap(p, q)
        if gap < 0:
            overlaps.append((i, j, lit(gap)))
        if least is None or gap < least:
            least, least_pair = gap, (i, j)
        dx, dy = q[0] - p[0], q[1] - p[1]
        if dx * dx + dy * dy < 2:
            near += 1
            area = intersection_area(p, q)
            if area != 0:
                clip_fail.append((i, j, lit(area)))
    assert least is not None
    passed = wall >= 0 and not overlaps and not clip_fail
    return {
        "n": n,
        "side": lit(side),
        "side_decimal": f"{side.numerator // side.denominator}.{str(side.numerator * 10**40 // side.denominator)[-40:]}",
        "printed_12_up": ceil_at(side, 12),
        "ceiling_16_up": ceil_at(side, 16),
        "upright_t0": sum(1 for t in tangents if t == 0),
        "min_wall_clearance": lit(wall),
        "min_wall_square": wall_square,
        "least_pair": list(least_pair),
        "least_pair_gap": lit(least),
        "least_pair_gap_float": float(least),
        "pairs": pairs,
        "near_pairs_clipped": near,
        "overlaps": overlaps[:5],
        "clip_failures": clip_fail[:5],
        "passed": passed,
        "cpu_seconds": round(time.process_time() - started, 1),
    }


def main(argv: list[str]) -> int:
    cert, n, out = Path(argv[1]), int(argv[2]), Path(argv[3])
    result = check(cert, n)
    if len(argv) > 4:
        receipt = json.loads(Path(argv[4]).read_text(encoding="utf-8"))
        positive = next(c for c in receipt["cases"] if c["control"] == "positive")
        comparison = {}
        for route in ("exact_verify", "independent"):
            r = positive[route]
            comparison[route] = {
                "wall_equal": Fraction(r["minimum_containment_clearance"]) == Fraction(result["min_wall_clearance"]),
                "gap_equal": Fraction(r["minimum_best_pair_gap"]) == Fraction(result["least_pair_gap"]),
                "side_equal": Fraction(r["side"]) == Fraction(result["side"]),
                "pairs_equal": r["pairs_tested"] == result["pairs"],
                "passed": r["verification_passed"],
            }
        result["receipt_comparison"] = comparison
        result["agrees_with_receipt"] = all(all(v for k, v in c.items()) for c in comparison.values())
    out.write_text(json.dumps(result, indent=1), encoding="utf-8")
    print(json.dumps(result, indent=1))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
