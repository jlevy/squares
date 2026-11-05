#!/usr/bin/env python3
"""Exact feasibility of a square-packing certificate in Evan Daniel's text format.

Written for the stage 4 review of jlevy/squares#895 (the 5 November 2026 review), from
the mathematics and the certificate format alone. It reads no other checker's code.

The format, as the issue and the packet README state it: lines starting with `#` are
comments; then a header `n S`; then n rows `x y t`, each a rational centre and the
rational tangent t = tan(theta/2) of the square's half-angle. With
c = (1 - t^2)/(1 + t^2) and s = 2t/(1 + t^2), which satisfy c^2 + s^2 = 1 exactly, the
square's edge directions are u = (c, s) and v = (-s, c) under the counterclockwise
sense (`ccw`), or u = (c, -s) and v = (s, c) under the reversed sense (`cw`), and its
corners are centre + (+-u +- v)/2. The container is [0, S]^2.

Two methods decide every wall and every pair, both in exact rational arithmetic
(fractions.Fraction), with no distance filter:

A. Separating axes. A pair of convex polygons has disjoint interiors exactly when the
   projections of their corners onto one of their edge normals overlap in at most a
   point. For a pair of squares the four normals are u_i, v_i, u_j, v_j. The gap on an
   axis is max(lo_j - hi_i, lo_i - hi_j); the pair is accepted when the largest gap over
   the four axes is >= 0. The axes are unit vectors exactly, so a gap is a distance.
   A square is inside the container when every corner coordinate lies in [0, S].

B. Exact clipped areas. Square j is clipped by the four closed half-planes of square i
   (Sutherland-Hodgman, each half-plane the left side of a counterclockwise edge, tested
   by a cross product); the shoelace area of what remains is the area of the
   intersection, and the pair is accepted when it is exactly 0. A square is inside the
   container when clipping it by the container leaves area exactly 1. Each square's own
   shoelace area is also required to be exactly 1.

Usage (paths are arguments; run with the project interpreter, -I):
  python -I certcheck.py CERT --out RECEIPT.json [--sense ccw|cw] [--label NAME]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path

RATIONAL = re.compile(r"^[+-]?[0-9]+(?:/[0-9]+)?$")
DECIMAL = re.compile(r"^[+-]?[0-9]+\.[0-9]+$")
INTEGER = re.compile(r"^[0-9]+$")


class FormatError(ValueError):
    """The file is not a certificate in the stated format."""


def parse_rational(token: str) -> tuple[Fraction, str]:
    """Read one rational token: an integer, p/q, or a plain decimal."""
    if RATIONAL.match(token):
        if "/" in token:
            num, den = token.split("/")
            if int(den) == 0:
                raise FormatError(f"zero denominator in {token!r}")
            value = Fraction(int(num), int(den))
            written_lowest = Fraction(int(num), int(den)).denominator == int(den)
            return value, "fraction" if written_lowest else "fraction-not-lowest"
        return Fraction(int(token)), "integer"
    if DECIMAL.match(token):
        return Fraction(token), "decimal"
    raise FormatError(f"not a rational token: {token!r}")


def parse_cert(path: str | Path) -> dict:
    """Parse strictly; refuse anything outside the stated format."""
    raw = Path(path).read_bytes()
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise FormatError(f"non-ASCII byte: {exc}") from exc
    if "\r" in text:
        raise FormatError("carriage return present")
    if not text.endswith("\n"):
        raise FormatError("no final newline")
    lines = text.split("\n")[:-1]
    comments: list[str] = []
    body: list[tuple[int, str]] = []
    for number, line in enumerate(lines, 1):
        if line.startswith("#"):
            if body:
                raise FormatError(f"line {number}: comment after the header")
            comments.append(line)
        elif line.strip() == "":
            raise FormatError(f"line {number}: blank line")
        else:
            body.append((number, line))
    if not body:
        raise FormatError("no header")
    header_line, header = body[0]
    head = header.split()
    if len(head) != 2 or not INTEGER.match(head[0]):
        raise FormatError(f"line {header_line}: header is not `n S`")
    n = int(head[0])
    side, side_form = parse_rational(head[1])
    rows = body[1:]
    if len(rows) != n:
        raise FormatError(f"header says {n} squares, file has {len(rows)} rows")
    forms: dict[str, int] = {side_form: 1}
    irregular_spacing = 0
    if header != " ".join(head):
        irregular_spacing += 1
    squares = []
    for row_index, (line_number, line) in enumerate(rows, 1):
        tokens = line.split()
        if len(tokens) != 3:
            raise FormatError(f"line {line_number}: {len(tokens)} tokens, expected 3")
        if line != " ".join(tokens):
            irregular_spacing += 1
        values = []
        for token in tokens:
            value, form = parse_rational(token)
            forms[form] = forms.get(form, 0) + 1
            values.append(value)
        squares.append(
            {
                "row": row_index,
                "line": line_number,
                "x": values[0],
                "y": values[1],
                "t": values[2],
                "tokens": tokens,
            }
        )
    return {
        "path": str(path),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "lines": len(lines),
        "comments": comments,
        "n": n,
        "side": side,
        "side_token": head[1],
        "token_forms": forms,
        "irregular_spacing_lines": irregular_spacing,
        "squares": squares,
    }


def frame(t: Fraction, sense: str) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    """Unit edge directions (u, v) of a square whose half-angle tangent is t."""
    den = 1 + t * t
    c = (1 - t * t) / den
    s = 2 * t / den
    if sense == "ccw":
        return (c, s), (-s, c)
    if sense == "cw":
        return (c, -s), (s, c)
    raise ValueError(sense)


def corners(x: Fraction, y: Fraction, u, v) -> list[tuple[Fraction, Fraction]]:
    """Corners in counterclockwise order: local (1/2,1/2), (-1/2,1/2), (-1/2,-1/2), (1/2,-1/2)."""
    half = Fraction(1, 2)
    out = []
    for a, b in ((half, half), (-half, half), (-half, -half), (half, -half)):
        out.append((x + a * u[0] + b * v[0], y + a * u[1] + b * v[1]))
    return out


def poses(cert: dict, sense: str = "ccw") -> list[dict]:
    """Exact frame and corners of every square."""
    out = []
    for sq in cert["squares"]:
        u, v = frame(sq["t"], sense)
        out.append({"x": sq["x"], "y": sq["y"], "u": u, "v": v, "P": corners(sq["x"], sq["y"], u, v)})
    return out


# ---------------------------------------------------------------- method A
def sat_gap(Pi, axes_i, Pj, axes_j) -> Fraction:
    """Largest separation of two squares over their four edge normals (>= 0: interiors disjoint)."""
    best = None
    for a in (*axes_i, *axes_j):
        pi = [a[0] * p[0] + a[1] * p[1] for p in Pi]
        pj = [a[0] * p[0] + a[1] * p[1] for p in Pj]
        gap = max(min(pj) - max(pi), min(pi) - max(pj))
        if best is None or gap > best:
            best = gap
    return best


def wall_clearances(P, side: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Clearances to the left, right, bottom and top walls of [0, S]^2, from the corners."""
    xs = [p[0] for p in P]
    ys = [p[1] for p in P]
    return (min(xs), side - max(xs), min(ys), side - max(ys))


# ---------------------------------------------------------------- method B
def cross(ax, ay, bx, by):
    return ax * by - ay * bx


def clip(poly, edge_from, edge_to):
    """Keep the part of poly on the closed left side of the directed line edge_from->edge_to."""
    ex = edge_to[0] - edge_from[0]
    ey = edge_to[1] - edge_from[1]

    def f(p):
        return cross(ex, ey, p[0] - edge_from[0], p[1] - edge_from[1])

    out = []
    m = len(poly)
    if m == 0:
        return out
    values = [f(p) for p in poly]
    for k in range(m):
        a, b = poly[k], poly[(k + 1) % m]
        fa, fb = values[k], values[(k + 1) % m]
        if fa >= 0:
            out.append(a)
            if fb < 0:
                r = fa / (fa - fb)
                out.append((a[0] + (b[0] - a[0]) * r, a[1] + (b[1] - a[1]) * r))
        elif fb >= 0:
            r = fa / (fa - fb)
            out.append((a[0] + (b[0] - a[0]) * r, a[1] + (b[1] - a[1]) * r))
    return out


def area(poly) -> Fraction:
    """Shoelace area (positive for counterclockwise order)."""
    m = len(poly)
    if m < 3:
        return Fraction(0)
    total = Fraction(0)
    for k in range(m):
        a, b = poly[k], poly[(k + 1) % m]
        total += a[0] * b[1] - a[1] * b[0]
    return total / 2


def clipped_area(subject, clipper) -> Fraction:
    """Area of subject intersected with the convex counterclockwise polygon clipper."""
    poly = list(subject)
    m = len(clipper)
    for k in range(m):
        poly = clip(poly, clipper[k], clipper[(k + 1) % m])
        if not poly:
            return Fraction(0)
    return area(poly)


# ---------------------------------------------------------------- deciding
def decide(cert: dict, sense: str = "ccw", methods: str = "AB", pair_list=None) -> dict:
    """Decide every wall and every pair (or the given pairs) by the named methods."""
    side = cert["side"]
    sq = poses(cert, sense)
    n = len(sq)
    result: dict = {"n": n, "sense": sense}
    pairs = pair_list if pair_list is not None else [(i, j) for i in range(n) for j in range(i + 1, n)]
    result["pairs_decided"] = len(pairs)
    if "A" in methods:
        t0 = time.process_time()
        walls = [wall_clearances(s["P"], side) for s in sq]
        names = ("left", "right", "bottom", "top")
        wall_summary = {}
        wall_fail = []
        for w, name in enumerate(names):
            values = [walls[i][w] for i in range(n)]
            least = min(values)
            at = [i + 1 for i in range(n) if values[i] == least]
            wall_summary[name] = {
                "least": str(least),
                "least_float": float(least),
                "rows_at_least": at,
                "rows_at_zero": [i + 1 for i in range(n) if values[i] == 0],
            }
            wall_fail += [(i + 1, name, str(values[i])) for i in range(n) if values[i] < 0]
        gaps = {}
        overlap_a = []
        for i, j in pairs:
            g = sat_gap(sq[i]["P"], (sq[i]["u"], sq[i]["v"]), sq[j]["P"], (sq[j]["u"], sq[j]["v"]))
            gaps[(i, j)] = g
            if g < 0:
                overlap_a.append((i + 1, j + 1))
        cpu_a = time.process_time() - t0
        order = sorted(gaps, key=lambda k: gaps[k])
        least_pairs = [
            {"rows": [i + 1, j + 1], "gap": str(gaps[(i, j)]), "gap_float": float(gaps[(i, j)])}
            for i, j in order[:25]
        ]
        thresholds = {}
        for exp in (-30, -20, -15, -12, -10, -9, -8, -6, -4, -3, -2, -1):
            bound = Fraction(1, 10 ** (-exp))
            thresholds[f"1e{exp}"] = sum(1 for k in gaps if gaps[k] < bound)
        result["_overlap_set_A"] = set(overlap_a)
        result["_wall_set_A"] = {f[0] for f in wall_fail}
        result["A"] = {
            "walls_accepted": not wall_fail,
            "wall_failures": wall_fail[:50],
            "wall_failure_count": len(wall_fail),
            "walls": wall_summary,
            "pairs_accepted": not overlap_a,
            "overlapping_pairs": overlap_a[:200],
            "overlapping_pair_count": len(overlap_a),
            "pairs_at_exact_contact": sum(1 for k in gaps if gaps[k] == 0),
            "pairs_with_gap_below": thresholds,
            "least_pairs": least_pairs,
            "cpu_seconds": round(cpu_a, 3),
        }
        result["_gaps"] = gaps
        result["_walls"] = walls
    if "B" in methods:
        t0 = time.process_time()
        container = [
            (Fraction(0), Fraction(0)),
            (side, Fraction(0)),
            (side, side),
            (Fraction(0), side),
        ]
        own_area_bad = [i + 1 for i in range(n) if area(sq[i]["P"]) != 1]
        wall_bad = []
        for i in range(n):
            inside = clipped_area(sq[i]["P"], container)
            if inside != 1:
                wall_bad.append((i + 1, float(1 - inside)))
        overlap_b = []
        for i, j in pairs:
            a = clipped_area(sq[j]["P"], sq[i]["P"])
            if a < 0:
                raise AssertionError("negative clipped area")
            if a > 0:
                overlap_b.append((i + 1, j + 1, float(a)))
        cpu_b = time.process_time() - t0
        result["_overlap_set_B"] = {(p[0], p[1]) for p in overlap_b}
        result["_wall_set_B"] = {f[0] for f in wall_bad} | set(own_area_bad)
        result["B"] = {
            "own_area_not_one": own_area_bad,
            "walls_accepted": not wall_bad and not own_area_bad,
            "wall_failures": wall_bad[:50],
            "wall_failure_count": len(wall_bad),
            "pairs_accepted": not overlap_b,
            "overlapping_pairs": overlap_b[:200],
            "overlapping_pair_count": len(overlap_b),
            "cpu_seconds": round(cpu_b, 3),
        }
    if "A" in result and "B" in result:
        # compared on the complete sets, before any list in the receipt is truncated
        result["methods_agree_on_pairs"] = result.pop("_overlap_set_A") == result.pop("_overlap_set_B")
        result["methods_agree_on_walls"] = result.pop("_wall_set_A") == result.pop("_wall_set_B")
        result["accepted_by_A"] = result["A"]["walls_accepted"] and result["A"]["pairs_accepted"]
        result["accepted_by_B"] = result["B"]["walls_accepted"] and result["B"]["pairs_accepted"]
    return result


def program_digest() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def cpu_now() -> float:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_utime + usage.ru_stime


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cert")
    ap.add_argument("--out", required=True)
    ap.add_argument("--sense", default="ccw", choices=("ccw", "cw"))
    ap.add_argument("--label", default="")
    args = ap.parse_args(argv)
    wall0 = time.time()
    cert = parse_cert(args.cert)
    res = decide(cert, args.sense, "AB")
    res.pop("_gaps", None)
    res.pop("_walls", None)
    receipt = {
        "program": "certcheck.py",
        "program_sha256": program_digest(),
        "python": platform.python_version(),
        "label": args.label,
        "input": {
            "path": args.cert,
            "bytes": cert["bytes"],
            "sha256": cert["sha256"],
            "lines": cert["lines"],
            "comments": cert["comments"],
            "n": cert["n"],
            "side": cert["side_token"],
            "side_float": float(cert["side"]),
            "token_forms": cert["token_forms"],
            "irregular_spacing_lines": cert["irregular_spacing_lines"],
        },
        "result": res,
        "verdict": "accepted"
        if res.get("accepted_by_A") and res.get("accepted_by_B")
        else ("refused" if not res.get("accepted_by_A") and not res.get("accepted_by_B") else "METHODS DISAGREE"),
        "cpu_seconds_total": round(cpu_now(), 3),
        "wall_seconds": round(time.time() - wall0, 3),
    }
    Path(args.out).write_text(json.dumps(receipt, indent=1) + "\n")
    print(json.dumps({k: receipt[k] for k in ("label", "verdict", "cpu_seconds_total", "wall_seconds")}))
    print(
        "A:",
        res["A"]["walls_accepted"],
        res["A"]["pairs_accepted"],
        res["A"]["overlapping_pair_count"],
        "least pair",
        res["A"]["least_pairs"][0],
        "cpu",
        res["A"]["cpu_seconds"],
    )
    print("B:", res["B"]["walls_accepted"], res["B"]["pairs_accepted"], res["B"]["overlapping_pair_count"], "cpu", res["B"]["cpu_seconds"])
    for name, w in res["A"]["walls"].items():
        print(f"  wall {name}: least {w['least_float']:.6e} at rows {w['rows_at_least'][:8]} zero-count {len(w['rows_at_zero'])}")
    return 0 if receipt["verdict"] in ("accepted", "refused") else 2


if __name__ == "__main__":
    sys.exit(main())
