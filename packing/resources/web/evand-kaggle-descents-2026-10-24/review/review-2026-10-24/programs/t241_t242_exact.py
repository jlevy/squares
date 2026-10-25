"""Clean-room exact check of the certificates T-241 and T-242 report, with controls.

A program of the stage 4 mathematical review of T-241 and T-242 (bead think-vm3m),
written from the mathematics and the certificate format alone. It reads each
certificate as data and imports nothing from sqpack, devtools or any source's code.
Every decision is made in exact rational arithmetic (fractions.Fraction).

Certificate format, as each file's header comment states it: optional comment lines
starting with '#', a line "n S", then n lines "x y t", each token a decimal integer or
a fraction p/q. Each line is a unit square with centre (x, y) and edge directions
u = (c, s) and v = (-s, c), where (c, s) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2)), so
t = tan(theta/2) and c^2 + s^2 = 1 exactly. The claim is that the n squares lie in
the box [0, S]^2 with pairwise disjoint interiors (touching is allowed).

Two methods decide each certificate, and they must agree:

A. Separating axes. A square lies in the box iff its four vertices do. Two convex
   polygons have disjoint interiors iff some edge normal of one of them weakly
   separates their projections, so a pair is checked on the four axes u_i, v_i, u_j,
   v_j; its gap is the largest projected gap among them.
B. Clipped areas. A square lies in the box iff clipping it to the box leaves its whole
   area, and two squares have disjoint interiors iff clipping one to the other leaves
   area 0 (Sutherland-Hodgman clipping and the shoelace formula, exactly).

A pair whose centres are at least 2 apart (decided exactly, by a grid of 2 x 2 cells
and the exact squared distance) has disjoint interiors, since each square lies in its
circumscribed disc of radius h*sqrt(2) <= 0.99 for every half side h <= 0.7 used here,
and its separating-axis gap is at least |d|/sqrt(2) - h_i - sqrt(2) h_j > 0.2 for unit
squares. Every nearer pair is decided by both methods; --all-pairs decides every pair
by method A as well.

Run from packing/ with the project interpreter, for example
    python -I resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/programs/t241_t242_exact.py \
        --all-pairs --out resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/outputs/t241_t242_exact.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, replace
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKING = HERE.parents[5]
HALF = Fraction(1, 2)
TINY = Fraction(1, 10**30)
TOKEN = re.compile(r"[+-]?[0-9]+(?:/[0-9]+)?")
COUNT = re.compile(r"[0-9]+")

# The three certificates under review, the SHA-256 the packets pin, and the exact side
# and prints the record states for each (transcribed from packing/frontier/results.yaml
# and the packet READMEs at main 84d4a75af).
CERTIFICATES = (
    {
        "key": "T-241 n=304",
        "path": "resources/web/couzo-issue763-2026-10-23/source/certificates/best/n304.cert",
        "sha256": "c8433dd798aef6f190790c6c78c63b4ab5c26baabe372405f8ff9029d175231d",
        "n": 304,
        "stated_side": (
            "42654421699169959072564987841514227093543746926117736119087439/"
            "2379353056489745832681562849107891444171481219500000000000000"
        ),
        "stated_cut_decimals": "17.92689890339264",
        "stated_print_up_12": "17.926898903393",
    },
    {
        "key": "T-242 n=268",
        "path": "resources/web/evand-kaggle-descents-2026-10-24/source/search/packer/candidates/s268_lightning.cert",
        "sha256": "c87da316589dd3843e9344e5461add99c4f80ca495ba862f302bf958bc154a49",
        "n": 268,
        "stated_side": "16.874361715869345824484822296466",
        "stated_side_fraction": "8437180857934672912242411148233/500000000000000000000000000000",
        "stated_print_up_12": "16.874361715870",
    },
    {
        "key": "T-242 n=304",
        "path": "resources/web/evand-kaggle-descents-2026-10-24/source/search/packer/candidates/s304_pub.cert",
        "sha256": "5dd7436a0f658d360c643a3465bf5ac39382fd682cd10f354b2f046ed7656f21",
        "n": 304,
        "stated_side": "17.92689890035674158972360842897",
        "stated_side_fraction": "1792689890035674158972360842897/100000000000000000000000000000",
    },
)

# Sides the record compares against, read from the files that hold them. Each is
# only read for its stated side, never verified here.
COMPARISONS = (
    {
        "key": "#763's entry at 268 (964ee2b n268.cert)",
        "kind": "certificate-header",
        "path": "resources/web/couzo-issue763-2026-10-23/source/certificates/best/n268.cert",
        "sha256": "e9833bf26e1bf7e4719ee983c91979ba51f7319d6caa8dd1911fce820903e07e",
        "n": 268,
    },
    {
        "key": "T-174, the house at 268 (known-best witness)",
        "kind": "witness-side",
        "path": "witnesses/known-best/n-268.yaml",
        "n": 268,
    },
    {
        "key": "T-186, the house at 304 (known-best witness)",
        "kind": "witness-side",
        "path": "witnesses/known-best/n-304.yaml",
        "n": 304,
    },
)

# Margins the record states, as (reviewed certificate, comparison, printed margin).
STATED_MARGINS = (
    ("T-242 n=268", "#763's entry at 268 (964ee2b n268.cert)", "4.48e-12"),
    ("T-242 n=268", "T-174, the house at 268 (known-best witness)", "4.45e-3"),
    ("T-241 n=304", "T-186, the house at 304 (known-best witness)", "2.53e-3"),
    ("T-242 n=304", "T-241 n=304", "3.04e-9"),
    ("T-242 n=304", "T-186, the house at 304 (known-best witness)", "2.53e-3"),
)


class CertificateError(ValueError):
    """A certificate that does not have the stated format."""


def rational(token: str) -> Fraction:
    if TOKEN.fullmatch(token) is None:
        raise CertificateError(f"not an integer or a fraction p/q: {token[:40]!r}")
    if "/" in token:
        numerator, denominator = token.split("/")
        if int(denominator) == 0:
            raise CertificateError("zero denominator")
        return Fraction(int(numerator), int(denominator))
    return Fraction(int(token))


@dataclass(frozen=True)
class Certificate:
    path: str
    sha256: str
    n: int
    side: Fraction
    poses: tuple[tuple[Fraction, Fraction, Fraction], ...]
    comments: tuple[str, ...]


def read_certificate(path: Path) -> Certificate:
    raw = path.read_bytes()
    text = raw.decode("ascii")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    comments: list[str] = []
    rows: list[list[str]] = []
    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            raise CertificateError(f"line {number}: blank line inside the certificate")
        if stripped.startswith("#"):
            if rows:
                raise CertificateError(f"line {number}: comment after the header")
            comments.append(stripped)
            continue
        rows.append(stripped.split())
    if not rows or len(rows[0]) != 2 or COUNT.fullmatch(rows[0][0]) is None:
        raise CertificateError("the first data line is not 'n S'")
    n = int(rows[0][0])
    side = rational(rows[0][1])
    if side <= 0:
        raise CertificateError("side is not positive")
    if len(rows) - 1 != n:
        raise CertificateError(f"header says {n} squares, file has {len(rows) - 1} lines")
    poses = []
    for number, row in enumerate(rows[1:], 1):
        if len(row) != 3:
            raise CertificateError(f"square {number}: {len(row)} tokens, not 3")
        poses.append((rational(row[0]), rational(row[1]), rational(row[2])))
    return Certificate(
        path=str(path),
        sha256=hashlib.sha256(raw).hexdigest(),
        n=n,
        side=side,
        poses=tuple(poses),
        comments=tuple(comments),
    )


@dataclass(frozen=True)
class Square:
    x: Fraction
    y: Fraction
    c: Fraction
    s: Fraction
    h: Fraction = HALF


def square_from_pose(x: Fraction, y: Fraction, t: Fraction) -> Square:
    denominator = 1 + t * t
    c = (1 - t * t) / denominator
    s = 2 * t / denominator
    if c * c + s * s != 1:
        raise AssertionError("half-angle direction is not a unit vector")
    return Square(x, y, c, s)


Point = tuple[Fraction, Fraction]


def vertices(q: Square) -> tuple[Point, Point, Point, Point]:
    """The four corners, counterclockwise: centre +- h u +- h v."""
    ux, uy = q.h * q.c, q.h * q.s
    vx, vy = -q.h * q.s, q.h * q.c
    return (
        (q.x + ux + vx, q.y + uy + vy),
        (q.x - ux + vx, q.y - uy + vy),
        (q.x - ux - vx, q.y - uy - vy),
        (q.x + ux - vx, q.y + uy - vy),
    )


def axes(q: Square) -> tuple[Point, Point]:
    return ((q.c, q.s), (-q.s, q.c))


def sat_gap(va: tuple[Point, ...], vb: tuple[Point, ...], directions: tuple[Point, ...]) -> tuple[Fraction, int, int]:
    """Largest projected gap over the axes, its axis, and the side b lies on (+1/-1)."""
    best: Fraction | None = None
    best_axis = -1
    best_sign = 0
    for k, (dx, dy) in enumerate(directions):
        pa = [dx * px + dy * py for px, py in va]
        pb = [dx * px + dy * py for px, py in vb]
        above = min(pb) - max(pa)
        below = min(pa) - max(pb)
        gap, sign = (above, 1) if above >= below else (below, -1)
        if best is None or gap > best:
            best, best_axis, best_sign = gap, k, sign
    if best is None:
        raise AssertionError("no axes")
    return best, best_axis, best_sign


def clip(poly: list[Point], a: Fraction, b: Fraction, c: Fraction) -> list[Point]:
    """The part of a convex polygon with a*x + b*y <= c (Sutherland-Hodgman, one plane)."""
    out: list[Point] = []
    m = len(poly)
    for k in range(m):
        p = poly[k]
        q = poly[(k + 1) % m]
        fp = a * p[0] + b * p[1] - c
        fq = a * q[0] + b * q[1] - c
        if fp <= 0:
            out.append(p)
        if (fp < 0 < fq) or (fq < 0 < fp):
            r = fp / (fp - fq)
            out.append((p[0] + r * (q[0] - p[0]), p[1] + r * (q[1] - p[1])))
    return out


def area(poly: list[Point]) -> Fraction:
    m = len(poly)
    if m < 3:
        return Fraction(0)
    twice = sum(
        (poly[k][0] * poly[(k + 1) % m][1] - poly[(k + 1) % m][0] * poly[k][1] for k in range(m)),
        Fraction(0),
    )
    return abs(twice) / 2


def half_planes(q: Square) -> list[tuple[Fraction, Fraction, Fraction]]:
    out = []
    for dx, dy in axes(q):
        centre = dx * q.x + dy * q.y
        out.append((dx, dy, centre + q.h))
        out.append((-dx, -dy, -centre + q.h))
    return out


def overlap_area(a: Square, vb: tuple[Point, ...]) -> Fraction:
    poly = list(vb)
    for plane in half_planes(a):
        poly = clip(poly, *plane)
        if not poly:
            return Fraction(0)
    return area(poly)


def area_in_box(vs: tuple[Point, ...], side: Fraction) -> Fraction:
    poly = list(vs)
    one, zero = Fraction(1), Fraction(0)
    for plane in ((-one, zero, zero), (one, zero, side), (zero, -one, zero), (zero, one, side)):
        poly = clip(poly, *plane)
        if not poly:
            return Fraction(0)
    return area(poly)


def point_segment_d2(p: Point, a: Point, b: Point) -> Fraction:
    ex, ey = b[0] - a[0], b[1] - a[1]
    wx, wy = p[0] - a[0], p[1] - a[1]
    length2 = ex * ex + ey * ey
    tau = (wx * ex + wy * ey) / length2
    tau = max(Fraction(0), min(Fraction(1), tau))
    dx, dy = wx - tau * ex, wy - tau * ey
    return dx * dx + dy * dy


def polygon_distance2(va: tuple[Point, ...], vb: tuple[Point, ...]) -> Fraction:
    """Squared Euclidean distance between two disjoint convex polygons."""
    best: Fraction | None = None
    for p_vs, q_vs in ((va, vb), (vb, va)):
        for p in p_vs:
            for k in range(len(q_vs)):
                d2 = point_segment_d2(p, q_vs[k], q_vs[(k + 1) % len(q_vs)])
                if best is None or d2 < best:
                    best = d2
    if best is None:
        raise AssertionError("empty polygons")
    return best


def dec(q: Fraction, digits: int = 30) -> str:
    with localcontext() as ctx:
        ctx.prec = digits
        return str(Decimal(q.numerator) / Decimal(q.denominator))


def print_up(q: Fraction, places: int = 12) -> str:
    scaled = math.ceil(q * 10**places)
    return f"{scaled // 10**places}.{scaled % 10**places:0{places}d}"


def cut(q: Fraction, places: int) -> str:
    scaled = math.floor(q * 10**places)
    return f"{scaled // 10**places}.{scaled % 10**places:0{places}d}"


def candidate_pairs(squares: list[Square]) -> tuple[list[tuple[int, int]], int, int]:
    """Pairs with exact squared centre distance below 4; and the counts of the rest."""
    cells: dict[tuple[int, int], list[int]] = defaultdict(list)
    for k, q in enumerate(squares):
        cells[(math.floor(q.x / 2), math.floor(q.y / 2))].append(k)
    near: list[tuple[int, int]] = []
    far_measured = 0
    for (cx, cy), members in cells.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                others = cells.get((cx + dx, cy + dy))
                if not others:
                    continue
                for i in members:
                    for j in others:
                        if i < j:
                            ddx = squares[i].x - squares[j].x
                            ddy = squares[i].y - squares[j].y
                            if ddx * ddx + ddy * ddy < 4:
                                near.append((i, j))
                            else:
                                far_measured += 1
    total = len(squares) * (len(squares) - 1) // 2
    return sorted(near), far_measured, total - len(near) - far_measured


def decide(squares: list[Square], side: Fraction, *, all_pairs: bool = False, keep: int = 5) -> dict[str, object]:
    """Decide the packing by both methods; return verdicts and the least slacks."""
    if max(q.h for q in squares) > Fraction(7, 10):
        raise AssertionError("the far-pair disc bound assumes half sides <= 0.7")
    verts = [vertices(q) for q in squares]
    walls: list[tuple[Fraction, int, str]] = []
    for k, vs in enumerate(verts):
        walls.append((min(min(px, py) for px, py in vs), k, "near"))
        walls.append((min(min(side - px, side - py) for px, py in vs), k, "far"))
    near_walls = sorted(w for w in walls if w[2] == "near")
    far_walls = sorted(w for w in walls if w[2] == "far")
    contained_a = near_walls[0][0] >= 0 and far_walls[0][0] >= 0
    areas_wrong = [k for k, (q, vs) in enumerate(zip(squares, verts, strict=True)) if area_in_box(vs, side) != 4 * q.h * q.h]
    contained_b = not areas_wrong

    near, far_measured, far_by_cell = candidate_pairs(squares)
    gaps: list[tuple[Fraction, int, int, int, int]] = []
    for i, j in near:
        gap, axis, sign = sat_gap(verts[i], verts[j], axes(squares[i]) + axes(squares[j]))
        gaps.append((gap, i, j, axis, sign))
    gaps.sort()
    disjoint_a = not gaps or gaps[0][0] >= 0
    overlapping_b = [(i, j) for i, j in near if overlap_area(squares[i], verts[j]) > 0]
    disjoint_b = not overlapping_b

    all_pairs_least: Fraction | None = None
    if all_pairs:
        for i in range(len(squares)):
            for j in range(i + 1, len(squares)):
                gap, _, _ = sat_gap(verts[i], verts[j], axes(squares[i]) + axes(squares[j]))
                if all_pairs_least is None or gap < all_pairs_least:
                    all_pairs_least = gap

    valid_a = contained_a and disjoint_a and (all_pairs_least is None or all_pairs_least >= 0)
    valid_b = contained_b and disjoint_b
    least_pairs = []
    for gap, i, j, axis, _sign in gaps[:keep]:
        entry: dict[str, object] = {
            "squares": [i + 1, j + 1],
            "sat_gap": str(gap),
            "sat_gap_decimal": dec(gap, 30),
            "axis": ["u_i", "v_i", "u_j", "v_j"][axis],
        }
        if gap >= 0:
            d2 = polygon_distance2(verts[i], verts[j])
            with localcontext() as ctx:
                ctx.prec = 12
                entry["euclidean_distance_decimal"] = str((Decimal(d2.numerator) / Decimal(d2.denominator)).sqrt())
        least_pairs.append(entry)
    return {
        "valid": valid_a and valid_b,
        "methods_agree": valid_a == valid_b,
        "method_a_separating_axes": {
            "contained": contained_a,
            "pairs_disjoint": disjoint_a,
            "valid": valid_a,
        },
        "method_b_clipped_areas": {
            "every_square_area_in_box_whole": contained_b,
            "squares_with_area_outside": [k + 1 for k in areas_wrong[:10]],
            "near_pairs_with_positive_overlap_area": len(overlapping_b),
            "first_overlapping_pairs": [[i + 1, j + 1] for i, j in overlapping_b[:10]],
            "valid": valid_b,
        },
        "least_near_wall_slack": str(near_walls[0][0]),
        "least_near_wall_slack_decimal": dec(near_walls[0][0], 30),
        "least_near_wall_square": near_walls[0][1] + 1,
        "squares_at_least_near_wall_slack": sum(1 for w in near_walls if w[0] == near_walls[0][0]),
        "least_far_wall_slack": str(far_walls[0][0]),
        "least_far_wall_slack_decimal": dec(far_walls[0][0], 30),
        "least_far_wall_square": far_walls[0][1] + 1,
        "squares_at_least_far_wall_slack": sum(1 for w in far_walls if w[0] == far_walls[0][0]),
        "pairs_total": len(squares) * (len(squares) - 1) // 2,
        "pairs_decided_both_methods": len(near),
        "pairs_far_by_exact_distance": far_measured,
        "pairs_far_by_grid_cell": far_by_cell,
        "least_pair_gaps": least_pairs,
        "pairs_with_gap_below_1e-9": sum(1 for g in gaps if g[0] < Fraction(1, 10**9)),
        "pairs_with_gap_below_1e-18": sum(1 for g in gaps if g[0] < Fraction(1, 10**18)),
        "all_pairs_method_a_least_gap": None if all_pairs_least is None else str(all_pairs_least),
        "all_pairs_method_a_least_gap_decimal": None if all_pairs_least is None else dec(all_pairs_least, 30),
        "_least": {
            "near": near_walls[0],
            "far": far_walls[0],
            "pair": gaps[0] if gaps else None,
        },
    }


def public(result: dict[str, object]) -> dict[str, object]:
    return {k: v for k, v in result.items() if not k.startswith("_")}


def translate(q: Square, dx: Fraction, dy: Fraction) -> Square:
    return replace(q, x=q.x + dx, y=q.y + dy)


def controls(squares: list[Square], side: Fraction, base: dict[str, object]) -> list[dict[str, object]]:
    """Mutations each run through decide(); 'expect' is fixed before the run."""
    least = base["_least"]
    assert isinstance(least, dict)
    far_slack, far_k, _ = least["far"]
    near_slack, near_k, _ = least["near"]
    pair = least["pair"]
    gap, i, j, axis, sign = pair
    direction = (axes(squares[i]) + axes(squares[j]))[axis]
    out: list[dict[str, object]] = []

    def run(name: str, expect: str, mutated: list[Square], new_side: Fraction, note: str) -> None:
        started = time.process_time()
        result = decide(mutated, new_side)
        verdict = "accept" if result["valid"] else "refuse"
        out.append(
            {
                "control": name,
                "note": note,
                "expected": expect,
                "outcome": verdict,
                "methods_agree": result["methods_agree"],
                "passed": result["methods_agree"] and (expect == "either" or verdict == expect),
                "least_wall_slack": str(min(Fraction(str(result["least_near_wall_slack"])), Fraction(str(result["least_far_wall_slack"])))),
                "least_pair_gap": result["least_pair_gaps"][0]["sat_gap"] if result["least_pair_gaps"] else None,
                "cpu_seconds": round(time.process_time() - started, 2),
            }
        )

    run("side-to-far-contact", "accept", squares, side - far_slack,
        "side lowered by the least far-wall slack: exact contact, which touching allows")
    run("side-past-far-contact", "refuse", squares, side - far_slack - TINY,
        "side lowered by the least far-wall slack and 1e-30 more")
    run("side-shrunk-by-twice-least-far-slack", "refuse", squares, side - 2 * far_slack,
        "side lowered by twice the least far-wall slack")
    step = (-direction[0] * sign, -direction[1] * sign)
    mutated = list(squares)
    mutated[j] = translate(squares[j], step[0] * gap, step[1] * gap)
    run("pair-to-contact", "either", mutated, side,
        f"square {j + 1} moved toward square {i + 1} along their separating axis by their gap")
    mutated = list(squares)
    mutated[j] = translate(squares[j], step[0] * (gap + TINY), step[1] * (gap + TINY))
    run("pair-past-contact", "refuse", mutated, side,
        f"square {j + 1} moved toward square {i + 1} along their separating axis by their gap and 1e-30")
    mutated = list(squares)
    toward = (squares[i].x - squares[j].x, squares[i].y - squares[j].y)
    norm = Fraction(1, 1000) / Fraction(max(abs(toward[0]), abs(toward[1])))
    mutated[j] = translate(squares[j], toward[0] * norm, toward[1] * norm)
    run("square-perturbed", "refuse", mutated, side,
        f"square {j + 1} moved toward the centre of square {i + 1} by 1e-3 in its larger coordinate")
    mutated = list(squares)
    mutated[j] = replace(squares[j], h=squares[j].h + gap + TINY)
    run("square-enlarged-past-pair", "refuse", mutated, side,
        f"square {j + 1} enlarged to side 1 + 2(gap + 1e-30), past its least-gap pair")
    mutated = list(squares)
    mutated[far_k] = replace(squares[far_k], h=squares[far_k].h + far_slack + TINY)
    run("square-enlarged-past-wall", "refuse", mutated, side,
        f"square {far_k + 1} enlarged by the least far-wall slack and 1e-30 on each side")
    mutated = list(squares)
    mutated[-1] = squares[0]
    run("square-duplicated", "refuse", mutated, side, "the last square replaced by a copy of the first")
    mutated = list(squares)
    q = squares[near_k]
    vs = vertices(q)
    if min(px for px, _ in vs) <= min(py for _, py in vs):
        mutated[near_k] = translate(q, -(near_slack + TINY), Fraction(0))
    else:
        mutated[near_k] = translate(q, Fraction(0), -(near_slack + TINY))
    run("square-past-near-wall", "refuse", mutated, side,
        f"square {near_k + 1} moved toward its nearest near wall by its slack and 1e-30")
    factor = 1 - Fraction(1, 10**9)
    middle = side / 2
    mutated = [replace(q, x=middle + (q.x - middle) * factor, y=middle + (q.y - middle) * factor) for q in squares]
    run("centres-drawn-in", "refuse", mutated, side,
        "every centre drawn toward the box centre by the factor 1 - 1e-9, squares kept unit, side kept")
    mutated = list(squares)
    q = squares[j]
    t_old = q.s / (1 + q.c) if q.c != -1 else None
    if t_old is not None:
        mutated[j] = square_from_pose(q.x, q.y, t_old + Fraction(1, 10**9))
        run("square-rotated", "either", mutated, side,
            f"square {j + 1} turned by about 2e-9 radians (t + 1e-9); both methods must agree")
    return out


def selftests() -> list[dict[str, object]]:
    """Hand-decided small packings, degenerate contacts included."""
    zero = Fraction(0)
    half = Fraction(1, 2)
    cases = [
        ("two squares in edge contact", Fraction(2), [(half, half, zero), (Fraction(3, 2), half, zero)], "accept"),
        ("a duplicated square", Fraction(2), [(half, half, zero), (half, half, zero)], "refuse"),
        ("a square shifted half along its neighbour's edge", Fraction(2), [(half, half, zero), (Fraction(1), half, zero)], "refuse"),
        ("two squares touching corner to corner", Fraction(2), [(half, half, zero), (Fraction(3, 2), Fraction(3, 2), zero)], "accept"),
        ("a turned square (c, s) = (3/5, 4/5) touching all four walls", Fraction(7, 5), [(Fraction(7, 10), Fraction(7, 10), half)], "accept"),
        ("the same square 1e-30 past the left wall", Fraction(7, 5), [(Fraction(7, 10) - TINY, Fraction(7, 10), half)], "refuse"),
        ("a turned square's corner touching an edge", Fraction(3), [(half, Fraction(3, 2), zero), (Fraction(17, 10), Fraction(8, 5), half)], "accept"),
        ("the same corner 1e-30 into the edge", Fraction(3), [(half, Fraction(3, 2), zero), (Fraction(17, 10) - TINY, Fraction(8, 5), half)], "refuse"),
        ("a square outside the box", Fraction(2), [(half, half, zero), (Fraction(5, 2), half, zero)], "refuse"),
    ]
    out = []
    for name, side, poses, expect in cases:
        squares = [square_from_pose(x, y, t) for x, y, t in poses]
        result = decide(squares, side)
        verdict = "accept" if result["valid"] else "refuse"
        out.append({"case": name, "expected": expect, "outcome": verdict, "methods_agree": result["methods_agree"],
                    "passed": verdict == expect and result["methods_agree"]})
    return out


def comparison_side(entry: dict[str, object]) -> Fraction:
    path = PACKING / str(entry["path"])
    if entry["kind"] == "certificate-header":
        cert = read_certificate(path)
        if cert.sha256 != entry["sha256"] or cert.n != entry["n"]:
            raise AssertionError(f"{path}: not the pinned certificate")
        return cert.side
    # A known-best witness: its 'side:' line, read as data (no YAML library needed).
    for line in path.read_text(encoding="ascii").splitlines():
        stripped = line.strip()
        if stripped.startswith("side:"):
            return rational(stripped.removeprefix("side:").strip().strip("'\""))
    raise AssertionError(f"{path}: no side line")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--all-pairs", action="store_true", help="also decide every pair by method A")
    parser.add_argument("--no-controls", action="store_true")
    parser.add_argument("--out", type=Path, help="write the JSON receipt here")
    args = parser.parse_args()
    started = time.process_time()
    report: dict[str, object] = {
        "program": "t241_t242_exact.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": sys.version.split()[0],
        "selftests": selftests(),
        "certificates": [],
        "sides": {},
    }
    sides: dict[str, Fraction] = {}
    certificates = report["certificates"]
    assert isinstance(certificates, list)
    for spec in CERTIFICATES:
        path = PACKING / str(spec["path"])
        cert = read_certificate(path)
        squares = [square_from_pose(x, y, t) for x, y, t in cert.poses]
        t0 = time.process_time()
        result = decide(squares, cert.side, all_pairs=args.all_pairs)
        stated = rational(str(spec["stated_side"])) if "/" in str(spec["stated_side"]) else Fraction(str(spec["stated_side"]))
        side_checks: dict[str, object] = {
            "header_side": str(cert.side),
            "header_side_decimal": dec(cert.side, 40),
            "equals_the_side_the_record_states": cert.side == stated,
            "print_rounded_up_12": print_up(cert.side, 12),
        }
        if "stated_side_fraction" in spec:
            side_checks["equals_the_fraction_the_packet_states"] = cert.side == rational(str(spec["stated_side_fraction"]))
        if "stated_print_up_12" in spec:
            side_checks["stated_print_up_12"] = spec["stated_print_up_12"]
            side_checks["print_matches"] = print_up(cert.side, 12) == spec["stated_print_up_12"]
        if "stated_cut_decimals" in spec:
            places = len(str(spec["stated_cut_decimals"]).split(".")[1])
            side_checks["cut_decimals_match"] = cut(cert.side, places) == spec["stated_cut_decimals"]
        sides[str(spec["key"])] = cert.side
        entry: dict[str, object] = {
            "key": spec["key"],
            "path": spec["path"],
            "sha256": cert.sha256,
            "sha256_matches_pin": cert.sha256 == spec["sha256"],
            "n": cert.n,
            "n_as_stated": cert.n == spec["n"],
            "header_comment": list(cert.comments),
            "tilted_squares": sum(1 for _, _, t in cert.poses if t != 0),
            "side": side_checks,
            "decision": public(result),
            "cpu_seconds_decision": round(time.process_time() - t0, 2),
        }
        if not args.no_controls:
            entry["controls"] = controls(squares, cert.side, result)
        certificates.append(entry)
        print(f"{spec['key']}: valid={result['valid']} agree={result['methods_agree']} "
              f"near={result['least_near_wall_slack_decimal']} far={result['least_far_wall_slack_decimal']} "
              f"pair={result['least_pair_gaps'][0]['sat_gap_decimal'] if result['least_pair_gaps'] else None} "
              f"print={print_up(cert.side, 12)}", flush=True)
    for comparison in COMPARISONS:
        sides[str(comparison["key"])] = comparison_side(comparison)
    margins = []
    for lower, upper, printed in STATED_MARGINS:
        difference = sides[upper] - sides[lower]
        margins.append({
            "certificate": lower,
            "below": upper,
            "exact_difference_decimal": dec(difference, 6),
            "stated": printed,
            "stated_matches_to_its_digits": f"{float(difference):.{len(printed.split('e')[0].split('.')[1])}e}".replace("e-0", "e-") == printed,
        })
    report["sides"] = {
        "values": {k: {"exact": str(v), "decimal": dec(v, 25), "print_up_12": print_up(v, 12)} for k, v in sides.items()},
        "stated_margins": margins,
    }
    report["cpu_seconds_total"] = round(time.process_time() - started, 2)
    text = json.dumps(report, indent=2)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    for case in report["selftests"]:  # type: ignore[union-attr]
        print(f"selftest {case['case']}: {case['outcome']} (expected {case['expected']}) passed={case['passed']}")
    for entry in certificates:
        assert isinstance(entry, dict)
        for control in entry.get("controls", []):
            print(f"{entry['key']} control {control['control']}: {control['outcome']} "
                  f"(expected {control['expected']}) agree={control['methods_agree']} passed={control['passed']}")
    for margin in margins:
        print(f"margin {margin['certificate']} below {margin['below']}: {margin['exact_difference_decimal']} "
              f"(stated {margin['stated']}, matches={margin['stated_matches_to_its_digits']})")
    print(f"cpu seconds: {report['cpu_seconds_total']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
