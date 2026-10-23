#!/usr/bin/env python3
"""Exact feasibility checker for rational centre/half-angle unit-square certificates.

Written for the stage 4 mathematical review of T-226, T-227 and T-228 (think-0nse,
lane c-review-t226-t228-math) from the format line one of the certificates carries
("unit squares, centre (x, y), rotation t = tan(theta/2)") and the mathematics.
Standard library only; it imports nothing from the repository and shares no code with
`sqpack.verify`, `devtools.check_rational_witness_independent`, the T-225 review's
checker or the source's `verify_bound_certificate.py`, none of which its author read
before writing it.

A certificate is optional comment lines starting with '#', a header `n S`, and n rows
`x y t`, each token a rational literal `[-]digits[/digits]`. Row k is the unit square
with centre (x, y) turned by theta, where t = tan(theta/2). The bound s(n) <= S holds
when the n squares lie in the closed box [0, S]^2 with pairwise disjoint interiors.

It decides that twice, on two routes that share only the reader:

route Z  integers only, no `fractions`: t = p/q gives the Pythagorean triple
         a = q^2 - p^2, b = 2pq, d = q^2 + p^2 (checked), so (a/d, b/d) is a unit
         vector; containment is decided by the half-extent (|a| + |b|)/(2d) against
         each wall; every one of the n(n-1)/2 pairs is decided by the four
         separating-axis inequalities (the two edge normals of each square), with all
         denominators cleared. A pair's gap is the largest separation over the four
         axes, an exact rational; the interiors are disjoint iff it is >= 0.
route C  `fractions.Fraction`: (cos, sin) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2)) from t
         directly; four corners built from them, with unit edges, right angles,
         positive orientation and corner mean = centre checked on the corners;
         containment of every corner; every pair decided by the exact area that one
         square's four closed half-planes clip from the other (Sutherland-Hodgman,
         then the shoelace formula), which is 0 iff the interiors are disjoint, with
         no distance filter.

Usage: python -I review_0nse_check.py OUT.json LABEL=PATH [LABEL=PATH ...]
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from fractions import Fraction
from math import gcd

_LITERAL = re.compile(r"(-?)([0-9]+)(?:/([0-9]+))?")
_COUNT = re.compile(r"[0-9]+")


class FormatError(ValueError):
    """The text is not a certificate in the stated format."""


def literal(token: str) -> tuple[int, int]:
    """A rational literal as (p, q) with q > 0, unreduced; no decimals, no '+'."""
    match = _LITERAL.fullmatch(token)
    if match is None:
        raise FormatError(f"not a rational literal: {token!r}")
    sign, num, den = match.groups()
    p = int(num)
    q = int(den) if den is not None else 1
    if q == 0:
        raise FormatError(f"zero denominator: {token!r}")
    return (-p if sign else p), q


def read(text: str) -> tuple[int, tuple[int, int], list[tuple[tuple[int, int], ...]], int]:
    """Return (n, S, rows, comment_lines); refuse anything outside the format."""
    if "\r" in text:
        raise FormatError("carriage return in the text")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    comments = 0
    k = 0
    while k < len(lines) and lines[k].startswith("#"):
        comments += 1
        k += 1
    if k == len(lines):
        raise FormatError("no header line")
    header = lines[k].split(" ")
    if len(header) != 2 or _COUNT.fullmatch(header[0]) is None:
        raise FormatError(f"bad header: {lines[k]!r}")
    n = int(header[0])
    if n <= 0:
        raise FormatError("n must be positive")
    side = literal(header[1])
    if side[0] <= 0:
        raise FormatError("side must be positive")
    rows = []
    for line in lines[k + 1 :]:
        if line == "" or line.startswith("#"):
            raise FormatError("blank or comment line after the header")
        tokens = line.split(" ")
        if len(tokens) != 3:
            raise FormatError(f"row with {len(tokens)} tokens: {line[:60]!r}")
        rows.append(tuple(literal(token) for token in tokens))
    if len(rows) != n:
        raise FormatError(f"{len(rows)} square rows for n = {n}")
    return n, side, rows, comments


# ---------------------------------------------------------------------------------
# Exact rationals as integer pairs (p, q), q > 0, for route Z.


def _lt(r: tuple[int, int], s: tuple[int, int]) -> bool:
    return r[0] * s[1] < s[0] * r[1]


def _reduce(r: tuple[int, int]) -> tuple[int, int]:
    g = gcd(r[0], r[1]) or 1
    return r[0] // g, r[1] // g


def _show(r: tuple[int, int] | None) -> str | None:
    if r is None:
        return None
    p, q = _reduce(r)
    return f"{p}/{q}" if q != 1 else str(p)


def _approx(r: tuple[int, int] | None) -> str | None:
    """A 17-digit decimal of p/q computed in integers (sign, mantissa, exponent)."""
    if r is None:
        return None
    p, q = _reduce(r)
    if p == 0:
        return "0"
    sign = "-" if p < 0 else ""
    p = abs(p)
    e = len(str(p)) - len(str(q))
    # scale so that 10^16 <= m < 10^18
    shift = 17 - e
    m = (p * 10**shift) // q if shift >= 0 else p // (q * 10 ** (-shift))
    while m >= 10**17:
        m //= 10
        shift -= 1
    while m < 10**16:
        shift += 1
        m = (p * 10**shift) // q if shift >= 0 else p // (q * 10 ** (-shift))
    digits = str(m)
    exponent = len(digits) - 1 - shift
    return f"{sign}{digits[0]}.{digits[1:]}e{exponent:+d}"


class RouteZ:
    """Integers only."""

    def __init__(self, n: int, side: tuple[int, int], rows) -> None:
        self.n = n
        self.side = side
        self.sq = []
        self.failures: list[str] = []
        for index, ((xn, xd), (yn, yd), (tp, tq)) in enumerate(rows):
            g = gcd(tp, tq)
            tp, tq = tp // g, tq // g
            a = tq * tq - tp * tp
            b = 2 * tp * tq
            d = tq * tq + tp * tp
            if a * a + b * b != d * d or d <= 0:
                self.failures.append(f"square {index}: not a Pythagorean triple")
            self.sq.append((xn, xd, yn, yd, a, b, d))

    def wall_clearances(self, index: int) -> list[tuple[int, int]]:
        """Left, bottom, right, top clearances of square `index`, exact."""
        xn, xd, yn, yd, a, b, d = self.sq[index]
        sn, sd = self.side
        e = abs(a) + abs(b)
        left = (2 * d * xn - xd * e, 2 * d * xd)
        bottom = (2 * d * yn - yd * e, 2 * d * yd)
        right = (2 * d * sn * xd - 2 * d * xn * sd - e * xd * sd, 2 * d * xd * sd)
        top = (2 * d * sn * yd - 2 * d * yn * sd - e * yd * sd, 2 * d * yd * sd)
        return [left, bottom, right, top]

    def pair_gap(self, i: int, j: int) -> tuple[tuple[int, int], int, int]:
        """(gap, axis, sign): gap = max separation over the four axes, as (p, q).

        axis 0, 1 are u_i, v_i; 2, 3 are u_j, v_j; sign is the sign of the
        projection of c_j - c_i on that axis.
        """
        xni, xdi, yni, ydi, ai, bi, di = self.sq[i]
        xnj, xdj, ynj, ydj, aj, bj, dj = self.sq[j]
        dx = xdi * xdj
        dy = ydi * ydj
        x = xnj * xdi - xni * xdj
        y = ynj * ydi - yni * ydj
        xdy = x * dy
        ydx = y * dx
        projections = (
            xdy * ai + ydx * bi,
            -xdy * bi + ydx * ai,
            xdy * aj + ydx * bj,
            -xdy * bj + ydx * aj,
        )
        weights = (dj, dj, di, di)
        best = -1
        axis = 0
        for k in range(4):
            value = 2 * weights[k] * abs(projections[k])
            if value > best:
                best = value
                axis = k
        c = ai * aj + bi * bj
        s = ai * bj - aj * bi
        reach = dx * dy * (di * dj + abs(c) + abs(s))
        sign = 1 if projections[axis] > 0 else (-1 if projections[axis] < 0 else 0)
        return (best - reach, 2 * dx * dy * di * dj), axis, sign

    def axis_vector(self, index: int, axis: int) -> tuple[tuple[int, int], tuple[int, int]]:
        """The unit axis (x, y) as integer pairs; axis 0 = u, 1 = v of square `index`."""
        _, _, _, _, a, b, d = self.sq[index]
        if axis == 0:
            return (a, d), (b, d)
        return (-b, d), (a, d)

    def run(self) -> dict:
        start = time.process_time()
        failures = list(self.failures)
        least_wall = None
        least_wall_at = None
        wall_contacts = 0
        names = ("x>=0", "y>=0", "x<=S", "y<=S")
        for index in range(self.n):
            for wall, clearance in enumerate(self.wall_clearances(index)):
                if clearance[0] < 0:
                    failures.append(f"square {index} violates {names[wall]}")
                if clearance[0] == 0:
                    wall_contacts += 1
                if least_wall is None or _lt(clearance, least_wall):
                    least_wall = clearance
                    least_wall_at = (index, names[wall])
        least_gap = None
        least_gap_at = None
        pairs = overlaps = touching = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                pairs += 1
                gap, axis, _sign = self.pair_gap(i, j)
                if gap[0] < 0:
                    overlaps += 1
                    if overlaps <= 20:
                        failures.append(f"squares {i} and {j} overlap")
                elif gap[0] == 0:
                    touching += 1
                if least_gap is None or _lt(gap, least_gap):
                    least_gap = gap
                    least_gap_at = (i, j, axis)
        return {
            "accepted": not failures,
            "failures": failures[:40],
            "pairs_decided": pairs,
            "overlapping_pairs": overlaps,
            "touching_pairs": touching,
            "wall_contacts": wall_contacts,
            "least_wall_clearance": _show(least_wall),
            "least_wall_clearance_approx": _approx(least_wall),
            "least_wall_at": least_wall_at,
            "least_gap": _show(least_gap),
            "least_gap_approx": _approx(least_gap),
            "least_gap_pair": least_gap_at,
            "cpu_seconds": round(time.process_time() - start, 3),
        }


# ---------------------------------------------------------------------------------
# Route C: Fraction corners and exact clipping area.


class RouteC:
    """fractions.Fraction, corners and clipping."""

    def __init__(self, n: int, side: tuple[int, int], rows) -> None:
        self.n = n
        self.side = Fraction(*side)
        self.squares = []
        self.failures: list[str] = []
        half = Fraction(1, 2)
        for index, (x, y, t) in enumerate(rows):
            x, y, t = Fraction(*x), Fraction(*y), Fraction(*t)
            cos = (1 - t * t) / (1 + t * t)
            sin = 2 * t / (1 + t * t)
            if cos * cos + sin * sin != 1:
                self.failures.append(f"square {index}: (cos, sin) not a unit vector")
            ux, uy = cos * half, sin * half
            vx, vy = -sin * half, cos * half
            corners = [
                (x + ux + vx, y + uy + vy),
                (x - ux + vx, y - uy + vy),
                (x - ux - vx, y - uy - vy),
                (x + ux - vx, y + uy - vy),
            ]
            self._check_unit(index, corners, x, y)
            self.squares.append(((x, y), (cos, sin), corners))

    def _check_unit(self, index, corners, x, y) -> None:
        edges = []
        for k in range(4):
            (px, py), (qx, qy) = corners[k], corners[(k + 1) % 4]
            edges.append((qx - px, qy - py))
        for k in range(4):
            ex, ey = edges[k]
            fx, fy = edges[(k + 1) % 4]
            if ex * ex + ey * ey != 1:
                self.failures.append(f"square {index}: edge {k} not of length 1")
            if ex * fx + ey * fy != 0:
                self.failures.append(f"square {index}: corner {k + 1} not a right angle")
        ex, ey = edges[0]
        fx, fy = edges[1]
        if ex * fy - ey * fx != 1:
            self.failures.append(f"square {index}: corners not in positive order")
        mx = sum(c[0] for c in corners) / 4
        my = sum(c[1] for c in corners) / 4
        if (mx, my) != (x, y):
            self.failures.append(f"square {index}: corner mean is not the centre")

    @staticmethod
    def _clip(poly, centre, axis, sense):
        """Keep the part of convex `poly` with sense*(p - centre).axis <= 1/2."""
        cx, cy = centre
        ax, ay = axis
        half = Fraction(1, 2)

        def f(p):
            return sense * ((p[0] - cx) * ax + (p[1] - cy) * ay) - half

        values = [f(p) for p in poly]
        if all(v <= 0 for v in values):
            return poly
        if all(v > 0 for v in values):
            return []
        out = []
        m = len(poly)
        for k in range(m):
            p, q = poly[k], poly[(k + 1) % m]
            fp, fq = values[k], values[(k + 1) % m]
            if fp <= 0:
                out.append(p)
            if (fp < 0 < fq) or (fq < 0 < fp):
                r = fp / (fp - fq)
                out.append((p[0] + (q[0] - p[0]) * r, p[1] + (q[1] - p[1]) * r))
        return out

    def intersection(self, i: int, j: int):
        """The vertices of square j clipped by square i's four closed half-planes."""
        (centre, (cos, sin), _) = self.squares[i]
        poly = list(self.squares[j][2])
        for axis in ((cos, sin), (-sin, cos)):
            for sense in (1, -1):
                poly = self._clip(poly, centre, axis, sense)
                if not poly:
                    return poly
        return poly

    @staticmethod
    def area(poly) -> Fraction:
        if len(poly) < 3:
            return Fraction(0)
        total = Fraction(0)
        m = len(poly)
        for k in range(m):
            (px, py), (qx, qy) = poly[k], poly[(k + 1) % m]
            total += px * qy - qx * py
        return abs(total) / 2

    def run(self) -> dict:
        start = time.process_time()
        failures = list(self.failures)
        s = self.side
        least_wall = None
        wall_contacts = 0
        for index, (_, _, corners) in enumerate(self.squares):
            square_least = None
            for cx, cy in corners:
                for value in (cx, cy, s - cx, s - cy):
                    if square_least is None or value < square_least:
                        square_least = value
            if square_least < 0:
                failures.append(f"square {index} has a corner outside the box")
            if least_wall is None or square_least < least_wall:
                least_wall = square_least
        for _, _, corners in self.squares:
            for cx, cy in corners:
                wall_contacts += sum(1 for v in (cx, cy, s - cx, s - cy) if v == 0)
        pairs = positive = touching = near = 0
        largest_area = Fraction(0)
        for i in range(self.n):
            (xi, yi) = self.squares[i][0]
            for j in range(i + 1, self.n):
                pairs += 1
                (xj, yj) = self.squares[j][0]
                if (xj - xi) ** 2 + (yj - yi) ** 2 <= 2:
                    near += 1
                poly = self.intersection(i, j)
                area = self.area(poly)
                if area > 0:
                    positive += 1
                    largest_area = max(largest_area, area)
                    if positive <= 20:
                        failures.append(f"squares {i} and {j} overlap with area {float(area):.3e}")
                elif poly:
                    touching += 1
        return {
            "accepted": not failures,
            "failures": failures[:40],
            "pairs_clipped": pairs,
            "pairs_with_centres_within_sqrt2": near,
            "positive_area_pairs": positive,
            "largest_area": str(largest_area),
            "touching_pairs": touching,
            "corner_wall_contacts": wall_contacts,
            "least_wall_clearance": str(least_wall),
            "cpu_seconds": round(time.process_time() - start, 3),
        }


def decide_text(text: str) -> dict:
    """Decide one certificate text on both routes; a format refusal is a refusal."""
    try:
        n, side, rows, comments = read(text)
    except FormatError as error:
        return {"accepted": False, "format_error": str(error)}
    z = RouteZ(n, side, rows).run()
    c = RouteC(n, side, rows).run()
    agree = (
        z["accepted"] == c["accepted"]
        and Fraction(z["least_wall_clearance"]) == Fraction(c["least_wall_clearance"])
        and z["touching_pairs"] == c["touching_pairs"]
        and (z["overlapping_pairs"] == 0) == (c["positive_area_pairs"] == 0)
    )
    return {
        "n": n,
        "side": _show(side),
        "comment_lines": comments,
        "accepted": z["accepted"] and c["accepted"],
        "routes_agree": agree,
        "route_Z": z,
        "route_C": c,
    }


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2
    out_path = argv[1]
    results = {}
    for spec in argv[2:]:
        label, path = spec.split("=", 1)
        data = open(path, "rb").read()
        result = decide_text(data.decode("ascii"))
        result["file"] = path
        result["sha256"] = hashlib.sha256(data).hexdigest()
        results[label] = result
        z, c = result.get("route_Z", {}), result.get("route_C", {})
        print(
            f"{label}: accepted={result['accepted']} agree={result.get('routes_agree')} "
            f"n={result.get('n')} side={result.get('side')}\n"
            f"  Z: pairs={z.get('pairs_decided')} overlaps={z.get('overlapping_pairs')} "
            f"touching={z.get('touching_pairs')} wall_contacts={z.get('wall_contacts')} "
            f"least_wall={z.get('least_wall_clearance_approx')} at {z.get('least_wall_at')} "
            f"least_gap={z.get('least_gap_approx')} at {z.get('least_gap_pair')} "
            f"cpu={z.get('cpu_seconds')}s\n"
            f"  C: pairs={c.get('pairs_clipped')} near={c.get('pairs_with_centres_within_sqrt2')} "
            f"positive_area={c.get('positive_area_pairs')} touching={c.get('touching_pairs')} "
            f"corner_wall_contacts={c.get('corner_wall_contacts')} cpu={c.get('cpu_seconds')}s"
        )
        for failure in (z.get("failures") or [])[:5] + (c.get("failures") or [])[:5]:
            print("   failure:", failure)
        if "format_error" in result:
            print("   format error:", result["format_error"])
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=1, sort_keys=True)
        handle.write("\n")
    return 0 if all(r["accepted"] for r in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
