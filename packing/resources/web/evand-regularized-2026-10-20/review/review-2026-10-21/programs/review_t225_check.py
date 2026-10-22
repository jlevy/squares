"""Stage 4 review checker for T-225: Evan Daniel's regularized views at 204, 227, 229, 260.

Written for the review `review-2026-10-21-evand-regularized-views.md` from the
certificate format line each file carries ("unit squares, centre (x, y), rotation
(c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2))") and the mathematics, before its author read
this repository's two maintained routes or the source's checkers. Standard library only;
it imports nothing from the repository and has its own reader.

It decides, for a certificate with header `n S` and n rows `x y t`, that the n squares
are unit squares inside the closed box [0, S]^2 with pairwise disjoint interiors, on two
routes that share only the reader:

* Route I, integers only (no `fractions`). Each t = p/q gives the integer Pythagorean
  triple a = q^2 - p^2, b = 2pq, d = q^2 + p^2 (checked a^2 + b^2 = d^2), so the square's
  unit edge directions are (a, b)/d and (-b, a)/d. Containment is the four integer
  inequalities of the half-extent test, |x - wall| >= (|a| + |b|)/(2d), cleared of
  denominators. Every pair of the n(n-1)/2 is decided by the separating-axis theorem on
  the four unit edge normals, each axis test cleared of denominators to
  2 d_j |a_i DxN DyD + b_i DyN DxD| >= (d_i d_j + |A| + |B|) DxD DyD (and its three
  siblings), with A = a_i a_j + b_i b_j and B = a_i b_j - b_i a_j. All four tests share
  the positive factor 2 d_i d_j DxD DyD, so the pair's exact gap is
  (max lhs - rhs) / (2 d_i d_j DxD DyD), an integer ratio.
* Route F, `fractions.Fraction`. Corners are built from (c, s); containment is read
  from the corners; every pair is decided by projecting all eight corners on the four
  unit edge normals (a corner-based separating-axis test, computed independently of
  route I's closed formula); and every pair whose axis-aligned bounding boxes overlap
  with positive area is decided again by the exact area of one square clipped by the
  other's four closed half-planes (Sutherland-Hodgman, shoelace area), which must be 0.
  Pairs whose bounding boxes do not overlap with positive area cannot overlap, since
  each square lies in its box.

The two routes' least wall clearances and least pair gaps are compared exactly
(by integer cross-multiplication) and must agree.

Usage:
  python -I review_t225_check.py CERT_DIR OUT.json [N ...]
CERT_DIR holds n-NNN.cert.gz (the packet's files, read as gzip by this program).
"""

from __future__ import annotations

import gzip
import json
import re
import sys
import time
from fractions import Fraction
from pathlib import Path

LITERAL = re.compile(r"(-?)(0|[1-9][0-9]*)(?:/([1-9][0-9]*))?")


class Refused(Exception):
    """The text is not a certificate this program reads."""


def literal(token: str) -> tuple[int, int]:
    """A rational literal as (numerator, positive denominator), not reduced."""
    match = LITERAL.fullmatch(token)
    if match is None:
        raise Refused(f"not a rational literal: {token[:40]!r}")
    sign, num, den = match.groups()
    numerator = int(num) * (-1 if sign else 1)
    return numerator, int(den) if den else 1


def read_certificate(text: str, n_expected: int) -> tuple[tuple[int, int], list[tuple]]:
    """Header and rows of the evand-cert text: comment lines, `n S`, then n rows `x y t`."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    k = 0
    while k < len(lines) and lines[k].startswith("#"):
        k += 1
    if k >= len(lines):
        raise Refused("no header")
    header = lines[k].split(" ")
    if len(header) != 2 or header[0] != str(n_expected):
        raise Refused(f"header is not '{n_expected} S': {lines[k][:60]!r}")
    side = literal(header[1])
    if side[0] <= 0:
        raise Refused("side is not positive")
    rows = lines[k + 1 :]
    if len(rows) != n_expected:
        raise Refused(f"{len(rows)} rows, not {n_expected}")
    squares = []
    for number, row in enumerate(rows):
        tokens = row.split(" ")
        if len(tokens) != 3:
            raise Refused(f"row {number} has {len(tokens)} fields")
        squares.append(tuple(literal(token) for token in tokens))
    return side, squares


# ---------------------------------------------------------------- route I: integers only


def route_integers(side: tuple[int, int], squares: list[tuple]) -> dict:
    sn, sd = side
    data = []
    for (xn, xd), (yn, yd), (p, q) in squares:
        a, b, d = q * q - p * p, 2 * p * q, q * q + p * p
        if a * a + b * b != d * d or d <= 0:
            raise AssertionError("not a Pythagorean triple")
        data.append((xn, xd, yn, yd, a, b, d))
    # containment: four clearances per square as integer ratios (num, den), den > 0
    least_wall = None  # (num, den, square, wall)
    walls_ok = True
    for index, (xn, xd, yn, yd, a, b, d) in enumerate(data):
        e = abs(a) + abs(b)
        for wall, num, den in (
            ("x>=0", 2 * d * xn - e * xd, 2 * d * xd),
            ("x<=S", 2 * d * sn * xd - e * sd * xd - 2 * d * sd * xn, 2 * d * sd * xd),
            ("y>=0", 2 * d * yn - e * yd, 2 * d * yd),
            ("y<=S", 2 * d * sn * yd - e * sd * yd - 2 * d * sd * yn, 2 * d * sd * yd),
        ):
            if num < 0:
                walls_ok = False
            if least_wall is None or num * least_wall[1] < least_wall[0] * den:
                least_wall = (num, den, index, wall)
    # every pair, no filter
    least_gap = None  # (num, den, i, j)
    overlaps = []
    contacts = 0
    pairs = 0
    count = len(data)
    for i in range(count):
        xni, xdi, yni, ydi, ai, bi, di = data[i]
        for j in range(i + 1, count):
            xnj, xdj, ynj, ydj, aj, bj, dj = data[j]
            pairs += 1
            dxn, dxd = xnj * xdi - xni * xdj, xdi * xdj
            dyn, dyd = ynj * ydi - yni * ydj, ydi * ydj
            px, py = dxn * dyd, dyn * dxd  # D * dxd * dyd, componentwise
            big_a = ai * aj + bi * bj
            big_b = ai * bj - bi * aj
            rhs = (di * dj + abs(big_a) + abs(big_b)) * dxd * dyd
            lhs = max(
                2 * dj * abs(ai * px + bi * py),
                2 * dj * abs(-bi * px + ai * py),
                2 * di * abs(aj * px + bj * py),
                2 * di * abs(-bj * px + aj * py),
            )
            num, den = lhs - rhs, 2 * di * dj * dxd * dyd
            if num < 0:
                overlaps.append((i, j))
            elif num == 0:
                contacts += 1
            if least_gap is None or num * least_gap[1] < least_gap[0] * den:
                least_gap = (num, den, i, j)
    return {
        "walls_ok": walls_ok,
        "least_wall": least_wall,
        "pairs": pairs,
        "overlapping_pairs": overlaps,
        "contacts": contacts,
        "least_gap": least_gap,
    }


# ---------------------------------------------------------------- route F: Fraction


def frac(pair: tuple[int, int]) -> Fraction:
    return Fraction(pair[0], pair[1])


def corners_of(x: Fraction, y: Fraction, t: Fraction) -> tuple[tuple, tuple, list]:
    c = (1 - t * t) / (1 + t * t)
    s = 2 * t / (1 + t * t)
    if c * c + s * s != 1:
        raise AssertionError("basis off the unit circle")
    ux, uy = c / 2, s / 2  # half of the first edge direction
    vx, vy = -s / 2, c / 2  # half of the second
    corners = [
        (x + ux + vx, y + uy + vy),
        (x - ux + vx, y - uy + vy),
        (x - ux - vx, y - uy - vy),
        (x + ux - vx, y + uy - vy),
    ]  # counter-clockwise: (u+v), (-u+v), (-u-v), (u-v)
    return (c, s), (-s, c), corners


def projection(axis: tuple, corners: list) -> tuple[Fraction, Fraction]:
    values = [axis[0] * px + axis[1] * py for px, py in corners]
    return min(values), max(values)


def clip_area(subject: list, clipper: list) -> Fraction:
    """Area of the convex polygon `subject` inside the closed counter-clockwise `clipper`."""
    polygon = list(subject)
    m = len(clipper)
    for k in range(m):
        (ax, ay), (bx, by) = clipper[k], clipper[(k + 1) % m]

        def inside(point: tuple) -> Fraction:
            return (bx - ax) * (point[1] - ay) - (by - ay) * (point[0] - ax)

        result = []
        for idx in range(len(polygon)):
            current, following = polygon[idx], polygon[(idx + 1) % len(polygon)]
            fc, ff = inside(current), inside(following)
            if fc >= 0:
                result.append(current)
            if (fc > 0 and ff < 0) or (fc < 0 and ff > 0):
                r = fc / (fc - ff)
                result.append(
                    (current[0] + r * (following[0] - current[0]), current[1] + r * (following[1] - current[1]))
                )
        polygon = result
        if not polygon:
            return Fraction(0)
    twice = Fraction(0)
    for idx in range(len(polygon)):
        (x1, y1), (x2, y2) = polygon[idx], polygon[(idx + 1) % len(polygon)]
        twice += x1 * y2 - x2 * y1
    return abs(twice) / 2


def route_fraction(side: tuple[int, int], squares: list[tuple], clip: bool = True) -> dict:
    big_s = frac(side)
    shapes = []
    least_wall = None
    walls_ok = True
    for index, (x, y, t) in enumerate(squares):
        x, y, t = frac(x), frac(y), frac(t)
        e1, e2, corners = corners_of(x, y, t)
        # unit edges and right angles, read from the corners
        for k in range(4):
            (x1, y1), (x2, y2), (x3, y3) = corners[k], corners[(k + 1) % 4], corners[(k + 2) % 4]
            if (x2 - x1) ** 2 + (y2 - y1) ** 2 != 1 or (x2 - x1) * (x3 - x2) + (y2 - y1) * (y3 - y2) != 0:
                raise AssertionError("not a unit square")
        xs = [cx for cx, _ in corners]
        ys = [cy for _, cy in corners]
        for wall, value in (("x>=0", min(xs)), ("x<=S", big_s - max(xs)), ("y>=0", min(ys)), ("y<=S", big_s - max(ys))):
            if value < 0:
                walls_ok = False
            if least_wall is None or value < least_wall[0]:
                least_wall = (value, index, wall)
        shapes.append((e1, e2, corners, (min(xs), max(xs), min(ys), max(ys))))
    least_gap = None
    overlaps = []
    contacts = 0
    clipped = 0
    clip_positive = []
    clip_disagree = []
    count = len(shapes)
    for i in range(count):
        e1i, e2i, ci, boxi = shapes[i]
        for j in range(i + 1, count):
            e1j, e2j, cj, boxj = shapes[j]
            gap = None
            for axis in (e1i, e2i, e1j, e2j):
                lo1, hi1 = projection(axis, ci)
                lo2, hi2 = projection(axis, cj)
                separation = max(lo2 - hi1, lo1 - hi2)
                if gap is None or separation > gap:
                    gap = separation
            if gap < 0:
                overlaps.append((i, j))
            elif gap == 0:
                contacts += 1
            if least_gap is None or gap < least_gap[0]:
                least_gap = (gap, i, j)
            if clip:
                ox = min(boxi[1], boxj[1]) - max(boxi[0], boxj[0])
                oy = min(boxi[3], boxj[3]) - max(boxi[2], boxj[2])
                if ox > 0 and oy > 0:
                    clipped += 1
                    area = clip_area(ci, cj)
                    if area != 0:
                        clip_positive.append((i, j))
                    if (area == 0) != (gap >= 0):
                        clip_disagree.append((i, j))
                elif gap < 0:
                    clip_disagree.append((i, j))  # boxes apart cannot overlap
    return {
        "walls_ok": walls_ok,
        "least_wall": least_wall,
        "overlapping_pairs": overlaps,
        "contacts": contacts,
        "least_gap": least_gap,
        "clipped_pairs": clipped,
        "clip_positive_pairs": clip_positive,
        "clip_disagreements": clip_disagree,
    }


# ---------------------------------------------------------------- decision


def show(value: Fraction) -> dict:
    return {"exact": f"{value.numerator}/{value.denominator}", "approx": f"{float(value):.6e}"}


def decide(text: str, n: int, clip: bool = True) -> dict:
    side, squares = read_certificate(text, n)
    started = time.process_time()
    ints = route_integers(side, squares)
    cpu_i = time.process_time() - started
    started = time.process_time()
    fr = route_fraction(side, squares, clip=clip)
    cpu_f = time.process_time() - started
    if ints["least_gap"] is None:  # one square: no pair
        ints["least_gap"] = (1, 1, None, None)
        fr["least_gap"] = (Fraction(1), None, None)
    wall_i = Fraction(ints["least_wall"][0], ints["least_wall"][1])
    gap_i = Fraction(ints["least_gap"][0], ints["least_gap"][1])
    # exact agreement of the two routes, compared by integer cross-multiplication
    wf, gf = fr["least_wall"][0], fr["least_gap"][0]
    agree_wall = ints["least_wall"][0] * wf.denominator == wf.numerator * ints["least_wall"][1]
    agree_gap = ints["least_gap"][0] * gf.denominator == gf.numerator * ints["least_gap"][1]
    passed_i = ints["walls_ok"] and not ints["overlapping_pairs"]
    passed_f = fr["walls_ok"] and not fr["overlapping_pairs"] and not fr["clip_positive_pairs"]
    return {
        "n": n,
        "side": f"{Fraction(*side).numerator}/{Fraction(*side).denominator}",
        "route_integers": {
            "passed": passed_i,
            "least_wall_clearance": show(wall_i),
            "least_wall_at": [ints["least_wall"][2], ints["least_wall"][3]],
            "pairs_decided": ints["pairs"],
            "overlapping_pairs": ints["overlapping_pairs"][:10],
            "overlapping_count": len(ints["overlapping_pairs"]),
            "contacts": ints["contacts"],
            "least_pair_gap": show(gap_i),
            "least_pair": [ints["least_gap"][2], ints["least_gap"][3]],
            "cpu_s": round(cpu_i, 2),
        },
        "route_fraction": {
            "passed": passed_f,
            "least_wall_clearance": show(wf),
            "least_wall_at": [fr["least_wall"][1], fr["least_wall"][2]],
            "overlapping_pairs": fr["overlapping_pairs"][:10],
            "overlapping_count": len(fr["overlapping_pairs"]),
            "contacts": fr["contacts"],
            "least_pair_gap": show(gf),
            "least_pair": [fr["least_gap"][1], fr["least_gap"][2]],
            "clipped_pairs": fr["clipped_pairs"],
            "clip_positive_pairs": fr["clip_positive_pairs"][:10],
            "clip_disagreements": fr["clip_disagreements"][:10],
            "cpu_s": round(cpu_f, 2),
        },
        "routes_agree": {"least_wall": agree_wall, "least_gap": agree_gap, "verdict": passed_i == passed_f},
        "passed": passed_i and passed_f,
        "strict": passed_i and passed_f and wall_i > 0 and gap_i > 0,
    }


def main(argv: list[str]) -> int:
    folder, out = Path(argv[1]), Path(argv[2])
    counts = [int(a) for a in argv[3:]] or [204, 227, 229, 260]
    results = {}
    for n in counts:
        text = gzip.decompress((folder / f"n-{n:03d}.cert.gz").read_bytes()).decode("ascii")
        result = decide(text, n)
        results[str(n)] = result
        print(json.dumps(result), flush=True)
    out.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    return 0 if all(r["passed"] for r in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
