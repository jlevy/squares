"""Exact feasibility checker written for the stage 4 review of the n = 204 certificate (T-231).

The certificate is a comment line, a header ``n S`` and ``n`` rows ``x y t``, each a
rational literal ``p`` or ``p/q``: a unit square with centre ``(x, y)`` whose edges run
along ``u = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))`` and ``v = (-u_y, u_x)``. It proves
``s(n) <= S`` when every square lies in the closed box ``[0, S]^2`` and no two squares
share an interior point.

Two routes decide that, and they share only the reader:

* Route Z uses integers alone and never loads ``fractions``. For ``t = p/q`` it takes the
  Pythagorean triple ``a = q^2 - p^2``, ``b = 2pq``, ``d = q^2 + p^2``; containment is the
  centre's clearance of each wall by the half-extent ``(|a| + |b|)/(2d)``, and a pair is
  decided by the four separating-axis inequalities along the two squares' edge normals,
  with every denominator cleared.
* Route C uses ``Fraction``. It builds the four corners, checks unit edges, right angles,
  positive orientation and the corner mean, decides containment from the corners, and
  decides every pair by the exact area that one square's four closed half-planes clip
  from the other, which is positive exactly when the interiors meet. It also projects
  the corners on the four edge normals, so that every pair's separating-axis gap is
  computed a second way, and it computes the exact squared Euclidean distance of every
  pair whose centres lie within 2.

Neither route rounds, dilates or tolerates. Standard library only; this file imports
nothing from the repository under review or from the certificate's source.

Usage (run with ``python3 -I``)::

    review_t231_check.py --route Z CERT --out RECEIPT.json
    review_t231_check.py --route C CERT --out RECEIPT.json
    review_t231_check.py --self-test [--out RECEIPT.json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import random
import re
import sys
import time
from dataclasses import dataclass
from functools import cmp_to_key
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence
    from fractions import Fraction

PROGRAM = Path(__file__).resolve()
TOKEN = re.compile(r"-?[0-9]+(?:/[0-9]+)?")
WALLS = ("left", "right", "bottom", "top")
CLOSE_CENTRES_SQUARED = 4  # route C's Euclidean distances: pairs whose centres lie within 2

type Rat = tuple[int, int]
type Row = tuple[Rat, Rat, Rat]


class CertificateError(ValueError):
    """The text is not a certificate in the format this checker reads."""


@dataclass(frozen=True)
class Certificate:
    n: int
    side: Rat
    rows: tuple[Row, ...]
    comments: tuple[str, ...]


def parse_rational(token: str) -> Rat:
    if TOKEN.fullmatch(token) is None:
        msg = f"not an integer or p/q literal: {token!r}"
        raise CertificateError(msg)
    if "/" in token:
        num_text, den_text = token.split("/")
        num, den = int(num_text), int(den_text)
    else:
        num, den = int(token), 1
    if den == 0:
        msg = f"zero denominator: {token!r}"
        raise CertificateError(msg)
    g = math.gcd(num, den)
    return num // g, den // g


def read_certificate(text: str) -> Certificate:
    """Read the format strictly: leading comments, a header, n rows, nothing after."""
    if not text.isascii():
        msg = "the text is not ASCII"
        raise CertificateError(msg)
    if "\r" in text:
        msg = "carriage return in the text"
        raise CertificateError(msg)
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    index = 0
    comments: list[str] = []
    while index < len(lines) and lines[index].startswith("#"):
        comments.append(lines[index])
        index += 1
    if index >= len(lines):
        msg = "no header line"
        raise CertificateError(msg)
    header = lines[index].split()
    index += 1
    if len(header) != 2 or not header[0].isdigit():
        msg = f"the header is not 'n S': {lines[index - 1]!r}"
        raise CertificateError(msg)
    n = int(header[0])
    side = parse_rational(header[1])
    if n <= 0 or side[0] <= 0:
        msg = "the count and the side must be positive"
        raise CertificateError(msg)
    body = lines[index:]
    if len(body) != n:
        msg = f"{len(body)} square rows for n = {n}"
        raise CertificateError(msg)
    rows: list[Row] = []
    for number, line in enumerate(body):
        fields = line.split()
        if len(fields) != 3:
            msg = f"row {number} has {len(fields)} fields, not 3: {line!r}"
            raise CertificateError(msg)
        x, y, t = (parse_rational(field) for field in fields)
        rows.append((x, y, t))
    return Certificate(n=n, side=side, rows=tuple(rows), comments=tuple(comments))


# Exact rational helpers on (num, den) pairs with den > 0, integers only.


def reduce(num: int, den: int) -> Rat:
    if den < 0:
        num, den = -num, -den
    g = math.gcd(num, den)
    return (num // g, den // g) if g else (0, 1)


def less(left: Rat, right: Rat) -> bool:
    return left[0] * right[1] < right[0] * left[1]


def compare_pairs(
    left: tuple[Rat, int, int, int], right: tuple[Rat, int, int, int]
) -> int:
    """Exact order of (gap, i, j, normal) records: by gap, then by pair."""
    product_left = left[0][0] * right[0][1]
    product_right = right[0][0] * left[0][1]
    if product_left != product_right:
        return -1 if product_left < product_right else 1
    return -1 if left[1:3] < right[1:3] else (1 if left[1:3] > right[1:3] else 0)


def text_of(value: Rat) -> str:
    num, den = reduce(*value)
    return str(num) if den == 1 else f"{num}/{den}"


def sci(num: int, den: int, digits: int = 13) -> str:
    """Round num/den to ``digits`` significant digits, in integers alone."""
    if den < 0:
        num, den = -num, -den
    if num == 0:
        return "0"
    sign = "-" if num < 0 else ""
    num = abs(num)
    exponent = len(str(num)) - len(str(den))
    if (exponent >= 0 and num < den * 10**exponent) or (
        exponent < 0 and num * 10 ** (-exponent) < den
    ):
        exponent -= 1
    shift = digits - 1 - exponent
    top, bottom = (num * 10**shift, den) if shift >= 0 else (num, den * 10 ** (-shift))
    quotient, remainder = divmod(top, bottom)
    if 2 * remainder >= bottom:
        quotient += 1
    if quotient >= 10**digits:
        quotient //= 10
        exponent += 1
    mantissa = str(quotient)
    return f"{sign}{mantissa[0]}.{mantissa[1:]}e{exponent:+d}"


def sha256_lines(lines: Sequence[str]) -> str:
    digest = hashlib.sha256()
    for line in lines:
        digest.update(line.encode())
        digest.update(b"\n")
    return digest.hexdigest()


# Route Z: integers alone.


@dataclass(frozen=True)
class PoseZ:
    xn: int
    xd: int
    yn: int
    yd: int
    a: int
    b: int
    d: int


def poses_z(cert: Certificate) -> list[PoseZ]:
    poses: list[PoseZ] = []
    for number, ((xn, xd), (yn, yd), (p, q)) in enumerate(cert.rows):
        a, b, d = q * q - p * p, 2 * p * q, q * q + p * p
        if a * a + b * b != d * d or d <= 0:
            msg = f"row {number}: the rotation is not on the unit circle"
            raise CertificateError(msg)
        poses.append(PoseZ(xn, xd, yn, yd, a, b, d))
    return poses


def wall_clearances_z(pose: PoseZ, side: Rat) -> dict[str, Rat]:
    sn, sd = side
    extent = abs(pose.a) + abs(pose.b)
    d = pose.d
    return {
        "left": reduce(2 * d * pose.xn - extent * pose.xd, 2 * d * pose.xd),
        "right": reduce(
            2 * d * (sn * pose.xd - pose.xn * sd) - extent * sd * pose.xd, 2 * d * sd * pose.xd
        ),
        "bottom": reduce(2 * d * pose.yn - extent * pose.yd, 2 * d * pose.yd),
        "top": reduce(
            2 * d * (sn * pose.yd - pose.yn * sd) - extent * sd * pose.yd, 2 * d * sd * pose.yd
        ),
    }


def pair_gap_z(first: PoseZ, second: PoseZ) -> tuple[Rat, int]:
    """The largest separation over the four edge normals, and which normal gives it.

    Normals 0 and 1 are the first square's u and v, 2 and 3 the second's. The pair has
    disjoint interiors exactly when the gap is at least 0.
    """
    dx_num = second.xn * first.xd - first.xn * second.xd
    big_dx = first.xd * second.xd
    dy_num = second.yn * first.yd - first.yn * second.yd
    big_dy = first.yd * second.yd
    x_term = dx_num * big_dy
    y_term = dy_num * big_dx
    ai, bi, di = first.a, first.b, first.d
    aj, bj, dj = second.a, second.b, second.d
    cosine = ai * aj + bi * bj
    sine = ai * bj - bi * aj
    reach = big_dx * big_dy * (di * dj + abs(cosine) + abs(sine))
    projections = (
        2 * dj * abs(ai * x_term + bi * y_term),
        2 * dj * abs(-bi * x_term + ai * y_term),
        2 * di * abs(aj * x_term + bj * y_term),
        2 * di * abs(-bj * x_term + aj * y_term),
    )
    axis = max(range(4), key=projections.__getitem__)
    return reduce(projections[axis] - reach, 2 * di * dj * big_dx * big_dy), axis


def route_z(cert: Certificate) -> dict[str, Any]:
    poses = poses_z(cert)
    clearances = [wall_clearances_z(pose, cert.side) for pose in poses]
    least_wall: dict[str, dict[str, Any]] = {}
    for wall in WALLS:
        values = [row[wall] for row in clearances]
        least = values[0]
        for value in values[1:]:
            if less(value, least):
                least = value
        at = [k for k, value in enumerate(values) if value == least]
        least_wall[wall] = {
            "clearance": text_of(least),
            "approx": sci(*least),
            "squares": at,
            "contacts": sum(1 for value in values if value[0] == 0),
            "violations": sum(1 for value in values if value[0] < 0),
        }
    contained = all(value[0] >= 0 for row in clearances for value in row.values())
    gap_lines: list[str] = []
    pairs: list[tuple[Rat, int, int, int]] = []
    for i in range(cert.n):
        for j in range(i + 1, cert.n):
            gap, axis = pair_gap_z(poses[i], poses[j])
            pairs.append((gap, i, j, axis))
            gap_lines.append(f"{i} {j} {text_of(gap)}")
    overlapping = [(i, j) for gap, i, j, _ in pairs if gap[0] < 0]
    touching = [(i, j) for gap, i, j, _ in pairs if gap[0] == 0]
    exact_head = sorted(pairs, key=cmp_to_key(compare_pairs))
    wall_lines = [
        f"{k} " + " ".join(text_of(row[wall]) for wall in WALLS)
        for k, row in enumerate(clearances)
    ]
    return {
        "route": "Z",
        "accepted": contained and not overlapping,
        "contained": contained,
        "pairs_decided": len(pairs),
        "overlapping_pairs": overlapping,
        "touching_pairs": touching,
        "least_wall": least_wall,
        "least_gap": None
        if not exact_head
        else {
            "gap": text_of(exact_head[0][0]),
            "approx": sci(*exact_head[0][0]),
            "pair": [exact_head[0][1], exact_head[0][2]],
            "normal": ["u of first", "v of first", "u of second", "v of second"][
                exact_head[0][3]
            ],
        },
        "smallest_gaps": [
            {"pair": [i, j], "gap": text_of(gap), "approx": sci(*gap), "normal": axis}
            for gap, i, j, axis in exact_head[:10]
        ],
        "gaps_below": {
            f"1e-{k}": sum(1 for gap, _, _, _ in pairs if gap[0] * 10**k < gap[1])
            for k in (6, 9, 12, 15, 18, 19, 20)
        },
        "pair_gap_digest": sha256_lines(gap_lines),
        "wall_clearance_digest": sha256_lines(wall_lines),
        "wall_clearances": wall_lines,
        "rotations": rotation_summary(poses),
    }


def rotation_summary(poses: Sequence[PoseZ]) -> dict[str, int]:
    """Rows that are axis-aligned exactly: t = 0 (b = 0) or a quarter turn, t = +-1 (a = 0)."""
    t_zero = sum(1 for pose in poses if pose.b == 0)
    quarter = sum(1 for pose in poses if pose.a == 0)
    return {
        "t_zero": t_zero,
        "quarter_turns": quarter,
        "axis_aligned": t_zero + quarter,
        "tilted": len(poses) - t_zero - quarter,
    }


# Route C: Fraction, corners, clipping area.


def route_c(cert: Certificate) -> dict[str, Any]:  # noqa: C901, PLR0912, PLR0914, PLR0915
    from fractions import Fraction  # noqa: PLC0415 - route Z must never load it

    side = Fraction(*cert.side)
    half = Fraction(1, 2)
    signs = ((half, half), (-half, half), (-half, -half), (half, -half))
    squares: list[list[tuple[Fraction, Fraction]]] = []
    normals: list[tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]] = []
    centres: list[tuple[Fraction, Fraction]] = []
    for number, (x_rat, y_rat, t_rat) in enumerate(cert.rows):
        x, y, t = Fraction(*x_rat), Fraction(*y_rat), Fraction(*t_rat)
        cos = (1 - t * t) / (1 + t * t)
        sin = 2 * t / (1 + t * t)
        if cos * cos + sin * sin != 1:
            msg = f"row {number}: (c, s) is not a unit vector"
            raise CertificateError(msg)
        corners = [(x + cos * ex - sin * ey, y + sin * ex + cos * ey) for ex, ey in signs]
        check_unit_square(corners, (x, y), number)
        squares.append(corners)
        normals.append(((cos, sin), (-sin, cos)))
        centres.append((x, y))
    clearances: list[dict[str, Fraction]] = [
        {
            "left": min(px for px, _ in corners),
            "right": side - max(px for px, _ in corners),
            "bottom": min(py for _, py in corners),
            "top": side - max(py for _, py in corners),
        }
        for corners in squares
    ]
    contained = all(value >= 0 for row in clearances for value in row.values())
    least_wall: dict[str, dict[str, Any]] = {}
    for wall in WALLS:
        values = [row[wall] for row in clearances]
        least = min(values)
        least_wall[wall] = {
            "clearance": str(least),
            "approx": sci(least.numerator, least.denominator),
            "squares": [k for k, value in enumerate(values) if value == least],
            "contacts": sum(1 for value in values if value == 0),
            "violations": sum(1 for value in values if value < 0),
        }
    gap_lines: list[str] = []
    positive_area: list[tuple[int, int, str]] = []
    nonempty_clip: list[tuple[int, int]] = []
    sat_negative: list[tuple[int, int]] = []
    least_gap: tuple[Fraction, int, int] | None = None
    distances: list[tuple[Fraction, int, int]] = []
    for i in range(cert.n):
        for j in range(i + 1, cert.n):
            gap = sat_gap_from_corners(squares[i], squares[j], (*normals[i], *normals[j]))
            gap_lines.append(f"{i} {j} {gap}")
            if gap < 0:
                sat_negative.append((i, j))
            if least_gap is None or gap < least_gap[0]:
                least_gap = (gap, i, j)
            clipped = clip(squares[j], squares[i])
            if clipped:
                nonempty_clip.append((i, j))
                area = polygon_area(clipped)
                if area > 0:
                    positive_area.append((i, j, str(area)))
            dx = centres[i][0] - centres[j][0]
            dy = centres[i][1] - centres[j][1]
            if dx * dx + dy * dy < CLOSE_CENTRES_SQUARED:
                distances.append((polygon_distance_squared(squares[i], squares[j]), i, j))
    distances.sort()
    sat_ok = not sat_negative
    area_ok = not positive_area
    if sat_ok != area_ok:
        msg = "route C's two pair procedures disagree"
        raise AssertionError(msg)
    least_distance = distances[0] if distances else None
    wall_lines = [
        f"{k} " + " ".join(str(row[wall]) for wall in WALLS) for k, row in enumerate(clearances)
    ]
    return {
        "route": "C",
        "accepted": contained and area_ok,
        "contained": contained,
        "pairs_decided": len(gap_lines),
        "positive_area_pairs": positive_area,
        "nonempty_clip_pairs": nonempty_clip,
        "sat_overlapping_pairs": sat_negative,
        "least_wall": least_wall,
        "least_gap": None
        if least_gap is None
        else {
            "gap": str(least_gap[0]),
            "approx": sci(least_gap[0].numerator, least_gap[0].denominator),
            "pair": [least_gap[1], least_gap[2]],
        },
        "close_pairs": len(distances),
        "least_distance_squared": None
        if least_distance is None
        else {
            "value": str(least_distance[0]),
            "approx_distance": sci(
                math.isqrt(least_distance[0].numerator * least_distance[0].denominator * 10**80),
                least_distance[0].denominator * 10**40,
            ),
            "pair": [least_distance[1], least_distance[2]],
        },
        "smallest_distances": [
            {
                "pair": [i, j],
                "distance_squared": str(value),
                "approx_distance_squared": sci(value.numerator, value.denominator),
            }
            for value, i, j in distances[:10]
        ],
        "pair_gap_digest": sha256_lines(gap_lines),
        "wall_clearance_digest": sha256_lines(wall_lines),
    }


def check_unit_square(
    corners: Sequence[tuple[Fraction, Fraction]], centre: tuple[Fraction, Fraction], number: int
) -> None:
    for k in range(4):
        p, q, r = corners[k], corners[(k + 1) % 4], corners[(k + 2) % 4]
        e1 = (q[0] - p[0], q[1] - p[1])
        e2 = (r[0] - q[0], r[1] - q[1])
        if e1[0] * e1[0] + e1[1] * e1[1] != 1:
            msg = f"row {number}: an edge is not of unit length"
            raise CertificateError(msg)
        if e1[0] * e2[0] + e1[1] * e2[1] != 0:
            msg = f"row {number}: adjacent edges are not orthogonal"
            raise CertificateError(msg)
        if e1[0] * e2[1] - e1[1] * e2[0] <= 0:
            msg = f"row {number}: the corners are not counter-clockwise"
            raise CertificateError(msg)
    if (
        sum(p[0] for p in corners) != 4 * centre[0]
        or sum(p[1] for p in corners) != 4 * centre[1]
    ):
        msg = f"row {number}: the corner mean is not the centre"
        raise CertificateError(msg)


def sat_gap_from_corners(
    first: Sequence[tuple[Fraction, Fraction]],
    second: Sequence[tuple[Fraction, Fraction]],
    axes: Sequence[tuple[Fraction, Fraction]],
) -> Fraction:
    best: Fraction | None = None
    for nx, ny in axes:
        p = [nx * px + ny * py for px, py in first]
        q = [nx * px + ny * py for px, py in second]
        separation = max(min(q) - max(p), min(p) - max(q))
        if best is None or separation > best:
            best = separation
    if best is None:
        msg = "no axes"
        raise ValueError(msg)
    return best


def clip(
    subject: Sequence[tuple[Fraction, Fraction]], window: Sequence[tuple[Fraction, Fraction]]
) -> list[tuple[Fraction, Fraction]]:
    """The subject polygon cut by the window's closed half-planes (window counter-clockwise)."""
    polygon = list(subject)
    for k in range(len(window)):
        ax, ay = window[k]
        bx, by = window[(k + 1) % len(window)]
        ex, ey = bx - ax, by - ay
        values = [ex * (py - ay) - ey * (px - ax) for px, py in polygon]
        if all(value < 0 for value in values):
            return []
        out: list[tuple[Fraction, Fraction]] = []
        for m, point in enumerate(polygon):
            following = polygon[(m + 1) % len(polygon)]
            fp, fq = values[m], values[(m + 1) % len(polygon)]
            if fp >= 0:
                out.append(point)
            if (fp > 0 > fq) or (fp < 0 < fq):
                ratio = fp / (fp - fq)
                out.append(
                    (
                        point[0] + (following[0] - point[0]) * ratio,
                        point[1] + (following[1] - point[1]) * ratio,
                    )
                )
        polygon = out
        if not polygon:
            return []
    return polygon


def polygon_area(polygon: Sequence[tuple[Fraction, Fraction]]) -> Fraction:
    total = sum(
        (
            polygon[k][0] * polygon[(k + 1) % len(polygon)][1]
            - polygon[(k + 1) % len(polygon)][0] * polygon[k][1]
            for k in range(len(polygon))
        ),
        start=polygon[0][0] * 0,
    )
    return abs(total) / 2


def point_segment_squared(
    point: tuple[Fraction, Fraction], start: tuple[Fraction, Fraction], end: tuple[Fraction, Fraction]
) -> Fraction:
    wx, wy = end[0] - start[0], end[1] - start[1]
    px, py = point[0] - start[0], point[1] - start[1]
    along = px * wx + py * wy
    length = wx * wx + wy * wy
    if along <= 0:
        return px * px + py * py
    if along >= length:
        qx, qy = point[0] - end[0], point[1] - end[1]
        return qx * qx + qy * qy
    return px * px + py * py - along * along / length


def polygon_distance_squared(
    first: Sequence[tuple[Fraction, Fraction]], second: Sequence[tuple[Fraction, Fraction]]
) -> Fraction:
    """Squared Euclidean distance of two convex polygons with disjoint interiors."""
    best: Fraction | None = None
    for one, other in ((first, second), (second, first)):
        for point in one:
            for k in range(len(other)):
                value = point_segment_squared(point, other[k], other[(k + 1) % len(other)])
                if best is None or value < best:
                    best = value
    if best is None:
        msg = "empty polygons"
        raise ValueError(msg)
    return best


# The self-test: hand-built cases with known answers, malformed texts, random pairs.


def certificate_text(side: str, rows: Sequence[tuple[str, str, str]]) -> str:
    lines = ["# test", f"{len(rows)} {side}"] + [" ".join(row) for row in rows]
    return "\n".join(lines) + "\n"


def frac_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def self_test() -> dict[str, Any]:  # noqa: C901, PLR0914, PLR0915
    from fractions import Fraction  # noqa: PLC0415 - the self-test runs both routes

    cases: list[tuple[str, str, bool]] = [
        ("one square in a unit box, all four walls in contact", certificate_text("1", [("1/2", "1/2", "0")]), True),
        ("side 1 - 1e-30 with one unit square", certificate_text(f"{10**30 - 1}/{10**30}", [("1/2", "1/2", "0")]), False),
        ("two squares sharing an edge", certificate_text("2", [("1/2", "1/2", "0"), ("3/2", "1/2", "0")]), True),
        ("two squares overlapping by 1e-30", certificate_text("2", [("1/2", "1/2", "0"), (f"{3 * 10**30 - 2}/{2 * 10**30}", "1/2", "0")]), False),
        ("a duplicated square", certificate_text("2", [("1/2", "1/2", "0"), ("1/2", "1/2", "0")]), False),
        ("a quarter turn (t = 1) sharing an edge", certificate_text("2", [("1/2", "1/2", "1"), ("3/2", "1/2", "0")]), True),
        ("a quarter turn the other way (t = -1) touching all four walls", certificate_text("1", [("1/2", "1/2", "-1")]), True),
        ("a 3-4-5 square touching all four walls", certificate_text("7/5", [("7/10", "7/10", "1/3")]), True),
        ("the same 1e-30 past the left wall", certificate_text("7/5", [(f"{7 * 10**29 - 1}/{10**30}", "7/10", "1/3")]), False),
        ("a 3-4-5 vertex touching an axis square's right edge", certificate_text("3", [("1/2", "3/2", "0"), ("17/10", "7/5", "1/2")]), True),
        ("the same vertex 1e-30 inside", certificate_text("3", [("1/2", "3/2", "0"), (f"{17 * 10**29 - 1}/{10**30}", "7/5", "1/2")]), False),
        ("a 3-4-5 square crossing an axis square's corner", certificate_text("4", [("1/2", "1/2", "0"), ("6/5", "6/5", "1/2")]), False),
        ("two tilted squares far apart", certificate_text("4", [("1", "1", "1/2"), ("3", "3", "1/3")]), True),
    ]
    results: list[dict[str, Any]] = []
    failures: list[str] = []
    for name, text, expected in cases:
        cert = read_certificate(text)
        z = route_z(cert)
        c = route_c(cert)
        ok = z["accepted"] == expected and c["accepted"] == expected
        ok = ok and z["pair_gap_digest"] == c["pair_gap_digest"]
        ok = ok and z["wall_clearance_digest"] == c["wall_clearance_digest"]
        results.append({"case": name, "expected": expected, "z": z["accepted"], "c": c["accepted"], "ok": ok})
        if not ok:
            failures.append(name)
    malformed = {
        "a row dropped": certificate_text("2", [("1/2", "1/2", "0")]).replace("1 2", "2 2", 1),
        "a decimal literal": certificate_text("2", [("0.5", "1/2", "0")]),
        "a zero denominator": certificate_text("2", [("1/0", "1/2", "0")]),
        "a blank line after the header": "# test\n1 2\n\n1/2 1/2 0\n",
        "a comment after the header": "# test\n1 2\n# x\n1/2 1/2 0\n",
        "four fields on a row": "# test\n1 2\n1/2 1/2 0 0\n",
        "a plus sign": "# test\n1 2\n+1/2 1/2 0\n",
        "an exponent": "# test\n1 2\n1e0 1/2 0\n",
        "a trailing row": "# test\n1 2\n1/2 1/2 0\n1/2 1/2 0\n",
        "a carriage return": "# test\r\n1 2\r\n1/2 1/2 0\r\n",
        "no header": "# test\n",
        "a negative side": "# test\n1 -2\n1/2 1/2 0\n",
    }
    refused: dict[str, str] = {}
    for name, text in malformed.items():
        try:
            read_certificate(text)
        except CertificateError as error:
            refused[name] = str(error)
        else:
            failures.append(f"malformed accepted: {name}")
    rng = random.Random(20261023)
    random_pairs = 0
    touching_built = 0
    disagreements = 0
    for trial in range(1500):
        p1, q1 = rng.randint(-9, 9), rng.randint(1, 9)
        p2, q2 = rng.randint(-9, 9), rng.randint(1, 9)
        t1, t2 = Fraction(p1, q1), Fraction(p2, q2)
        if trial % 3 == 0:
            # Built to touch: a vertex of the second square on an edge of the first.
            c1, s1 = (1 - t1 * t1) / (1 + t1 * t1), 2 * t1 / (1 + t1 * t1)
            c2, s2 = (1 - t2 * t2) / (1 + t2 * t2), 2 * t2 / (1 + t2 * t2)
            centre1 = (Fraction(5), Fraction(5))
            edge = rng.randrange(4)
            normal = [(c1, s1), (-s1, c1), (-c1, -s1), (s1, -c1)][edge]
            tangent = (-normal[1], normal[0])
            along = Fraction(rng.randint(-49, 49), 100)
            contact = (
                centre1[0] + normal[0] / 2 + tangent[0] * along,
                centre1[1] + normal[1] / 2 + tangent[1] * along,
            )
            offsets = [
                (c2 * ex - s2 * ey, s2 * ex + c2 * ey)
                for ex, ey in ((Fraction(1, 2), Fraction(1, 2)), (Fraction(-1, 2), Fraction(1, 2)), (Fraction(-1, 2), Fraction(-1, 2)), (Fraction(1, 2), Fraction(-1, 2)))
            ]
            offset = min(offsets, key=lambda o: o[0] * normal[0] + o[1] * normal[1])
            push = Fraction(0) if trial % 2 == 0 else Fraction(1, 10**30)
            centre2 = (
                contact[0] - offset[0] - normal[0] * push,
                contact[1] - offset[1] - normal[1] * push,
            )
            expected_pair: bool | None = push == 0
            touching_built += 1
        else:
            centre1 = (Fraction(5), Fraction(5))
            centre2 = (
                Fraction(5) + Fraction(rng.randint(-160, 160), 100),
                Fraction(5) + Fraction(rng.randint(-160, 160), 100),
            )
            expected_pair = None
        text = certificate_text(
            "12",
            [
                (frac_text(centre1[0]), frac_text(centre1[1]), frac_text(t1)),
                (frac_text(centre2[0]), frac_text(centre2[1]), frac_text(t2)),
            ],
        )
        cert = read_certificate(text)
        z = route_z(cert)
        c = route_c(cert)
        random_pairs += 1
        agree = z["accepted"] == c["accepted"] and z["pair_gap_digest"] == c["pair_gap_digest"]
        if expected_pair is not None:
            agree = agree and z["accepted"] == expected_pair
            if expected_pair:
                agree = agree and z["touching_pairs"] == [(0, 1)]
        if not agree:
            disagreements += 1
            failures.append(f"random trial {trial}")
    return {
        "cases": results,
        "malformed_refused": refused,
        "random_pairs": random_pairs,
        "random_built_to_touch": touching_built,
        "random_disagreements": disagreements,
        "failures": failures,
        "passed": not failures,
    }


def provenance(cert_path: Path | None) -> dict[str, Any]:
    info: dict[str, Any] = {
        "program": PROGRAM.name,
        "program_sha256": hashlib.sha256(PROGRAM.read_bytes()).hexdigest(),
        "python": sys.version,
        "implementation": platform.python_implementation(),
    }
    if cert_path is not None:
        data = cert_path.read_bytes()
        info["certificate"] = str(cert_path)
        info["certificate_sha256"] = hashlib.sha256(data).hexdigest()
        info["certificate_bytes"] = len(data)
    return info


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("certificate", nargs="?", type=Path)
    parser.add_argument("--route", choices=("Z", "C"))
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    started = time.process_time()
    wall_started = time.perf_counter()
    if args.self_test:
        report: dict[str, Any] = {"self_test": self_test()}
        report["provenance"] = provenance(None)
        ok = report["self_test"]["passed"]
    else:
        if args.certificate is None or args.route is None:
            parser.error("a certificate and --route are required")
        try:
            cert = read_certificate(args.certificate.read_text(encoding="ascii"))
        except (CertificateError, UnicodeDecodeError) as error:
            report = {"accepted": False, "refused_by_reader": str(error)}
            report["provenance"] = provenance(args.certificate)
            ok = False
        else:
            body = route_z(cert) if args.route == "Z" else route_c(cert)
            report = {
                "n": cert.n,
                "side": text_of(cert.side),
                "side_approx": sci(*cert.side, digits=32),
                "comment_lines": list(cert.comments),
                **body,
            }
            report["provenance"] = provenance(args.certificate)
            if args.route == "Z":
                report["fractions_loaded"] = "fractions" in sys.modules
                if report["fractions_loaded"]:
                    msg = "route Z loaded fractions"
                    raise AssertionError(msg)
            ok = bool(report["accepted"])
    report["cpu_seconds"] = round(time.process_time() - started, 3)
    report["wall_seconds"] = round(time.perf_counter() - wall_started, 3)
    text = json.dumps(report, indent=1, sort_keys=False)
    if args.out is not None:
        args.out.write_text(text + "\n", encoding="utf-8")
    summary = {
        key: report.get(key)
        for key in ("route", "n", "side", "accepted", "contained", "pairs_decided", "cpu_seconds")
        if key in report
    }
    if report.get("least_gap") is not None:
        summary["least_gap"] = report["least_gap"]["approx"]
        summary["least_gap_pair"] = report["least_gap"]["pair"]
        summary["least_wall"] = {w: report["least_wall"][w]["approx"] for w in WALLS}
    if "self_test" in report:
        summary["self_test_passed"] = report["self_test"]["passed"]
        summary["failures"] = report["self_test"]["failures"]
    if "refused_by_reader" in report:
        summary["refused_by_reader"] = report["refused_by_reader"]
    sys.stdout.write(json.dumps(summary) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
