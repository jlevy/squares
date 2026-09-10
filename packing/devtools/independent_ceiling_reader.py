"""Independent exact reader for the agenda-031 ceiling family at 191/50 (lane T).

Written from the statement alone, without importing or copying
``sqpack.fractional.ceiling``: the standard library, ``Fraction`` and Python integers
only, and no float takes part in any decision. Run from packing/ with
uv run --frozen --all-extras --group dev python -m devtools.independent_ceiling_reader
[RECORD] [--output RESULT.json] [--expect-sha256 HEX] [--control].

Object read: a ``CeilingCertificate`` record -- ``n``, ``outer_side`` L, ``square_side``
B, ``half_tangents`` (the net; angle = 2 arctan t), and ``placements`` as
[half_tangent, centre_x, centre_y, weight, side] rational strings.

Claim decided, four conditions:
  K0 every placement is a closed square of side B whose half-tangent t is in the net or is
     the mirror (1 - t) / (1 + t) of a net half-tangent, with a non-negative weight;
  K1 every placement lies in the closed container [0, L]^2 (its four corners, exactly);
  K2 the depth d(p) = sum of the weights of the closed placements containing p has
     maximum exactly 1 over the container, decided at every vertex of the arrangement cut
     by the placements' edge lines and the four container walls;
  K3 the total weight is exactly n.
Then, by weak duality (the statement is in the docstring of sqpack/fractional/ceiling.py),
no D4-symmetric measure of mass below n gives mass >= 1 to every closed B-square at a net
angle inside [0, L]^2: for this net and every net containing the angles used, for this B
and every smaller B (a concentric smaller core lies inside the larger one), and for this
L and every larger L (embed the family concentrically). A mirror-image angle is
admissible only against D4-symmetric measures, which condition C1 of the certificate
demands anyway, so the family's own D4 symmetry is checked as well.

Design (fixed before running):
  * the square with half-tangent t = p / q has edge directions a = (cos, sin) and
    b = (-sin, cos), cos = (q^2 - p^2) / (q^2 + p^2), sin = 2 p q / (q^2 + p^2); it is the
    closed slab intersection |a.p - a.c| <= B / 2, |b.p - b.c| <= B / 2 about its centre c;
  * each slab is scaled to integers lo <= A x + B y <= hi, so membership of the rational
    point (X / D, Y / D), D > 0, is the integer test lo D <= A X + B Y <= hi D;
  * vertices are the intersections of every non-parallel pair among the distinct edge
    lines and the four walls, by Cramer's rule as (X, Y, D) with D = |det| > 0, kept when
    inside the closed container and deduplicated after dividing by gcd(X, Y, D);
  * depth at a vertex is the exact Fraction sum of the weights of the containing
    placements; the maximum over the vertices is the maximum over the container because
    depth is a finite sum of indicators of closed convex sets, hence upper semicontinuous
    and constant on the open faces of the arrangement, every face inside the compact
    container has a vertex in its closure, and a closed square containing a face contains
    its closure;
  * D4 symmetry is decided on corner sets: each of the eight isometries of the container
    about (L / 2, L / 2) is applied to the four corners of every placement and the weighted
    multiset of corner sets must be invariant; independently, the same is decided on the
    (t, x, y) triples with the half-tangent fixed by rotations and sent to
    (1 - t) / (1 + t) by reflections, t = 1 folded to t = 0 (the same axis-parallel square);
  * ``--control`` perturbs the record three ways (weights scaled by 8/7, one centre shifted
    by L, one half-tangent replaced by 1/3) and requires the reader to reject each on the
    expected condition, so a reader that cannot fail is not mistaken for a proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from fractions import Fraction
from itertools import combinations, pairwise
from math import gcd, lcm
from pathlib import Path
from typing import Any

PACKING = Path(__file__).resolve().parent.parent
DEFAULT_RECORD = (
    PACKING
    / "campaign/series/series-000-smoke-and-calibration/results/agenda-031"
    / "ceiling-family-191-50.json"
)
RETAINED_SHA256 = "95cf06473f185764076d21021b75cc65962ef6b68dc717c045c2c7d76ae12427"

type Point = tuple[Fraction, Fraction]
# A x + B y = C over the integers, (A, B) != (0, 0), normalised by gcd and sign.
type Line = tuple[int, int, int]
# lo <= A x + B y <= hi over the integers.
type Slab = tuple[int, int, int, int]
# (X, Y, D) names the point (X / D, Y / D) with D > 0 and gcd(X, Y, D) = 1.
type Vertex = tuple[int, int, int]
type Isometry = Callable[[Point], Point]


@dataclass(frozen=True, slots=True)
class Square:
    """A closed square in the container, carrying a weight. Nothing here is a float."""

    half_tangent: Fraction
    centre_x: Fraction
    centre_y: Fraction
    weight: Fraction
    side: Fraction

    def frame(self) -> tuple[Fraction, Fraction]:
        """``(cos theta, sin theta)`` for ``theta = 2 arctan(half_tangent)``, exactly."""
        p, q = self.half_tangent.numerator, self.half_tangent.denominator
        norm = p * p + q * q
        return Fraction(q * q - p * p, norm), Fraction(2 * p * q, norm)

    def corners(self) -> list[Point]:
        c, s = self.frame()
        h = self.side / 2
        ax, ay, bx, by = c * h, s * h, -s * h, c * h
        x, y = self.centre_x, self.centre_y
        return [
            (x + ax + bx, y + ay + by),
            (x + ax - bx, y + ay - by),
            (x - ax + bx, y - ay + by),
            (x - ax - bx, y - ay - by),
        ]

    def slabs(self) -> tuple[Slab, Slab]:
        """The two closed slabs whose intersection is the square, over the integers."""
        c, s = self.frame()
        h = self.side / 2
        u = c * self.centre_x + s * self.centre_y
        v = -s * self.centre_x + c * self.centre_y
        return integer_slab(c, s, u - h, u + h), integer_slab(-s, c, v - h, v + h)

    @property
    def mirror_half_tangent(self) -> Fraction:
        """The half-tangent of ``pi/2 - theta``: the angle of the reflected square."""
        return (1 - self.half_tangent) / (1 + self.half_tangent)


def integer_slab(a: Fraction, b: Fraction, lo: Fraction, hi: Fraction) -> Slab:
    m = lcm(a.denominator, b.denominator, lo.denominator, hi.denominator)
    return (
        a.numerator * (m // a.denominator),
        b.numerator * (m // b.denominator),
        lo.numerator * (m // lo.denominator),
        hi.numerator * (m // hi.denominator),
    )


def normalised_line(a: int, b: int, c: int) -> Line:
    g = gcd(a, b, c)
    a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return a, b, c


def slab_lines(slab: Slab) -> tuple[Line, Line]:
    a, b, lo, hi = slab
    return normalised_line(a, b, lo), normalised_line(a, b, hi)


def wall_lines(outer: Fraction) -> list[Line]:
    n, d = outer.numerator, outer.denominator
    return [
        normalised_line(1, 0, 0),
        normalised_line(d, 0, n),
        normalised_line(0, 1, 0),
        normalised_line(0, d, n),
    ]


def arrangement_vertices(
    lines: Sequence[Line], outer: Fraction
) -> tuple[set[Vertex], int, int]:
    """Distinct vertices inside the closed container, with the pair counts behind them."""
    ln, ld = outer.numerator, outer.denominator
    inside: set[Vertex] = set()
    crossing_pairs = 0
    inside_pairs = 0
    for (a1, b1, c1), (a2, b2, c2) in combinations(lines, 2):
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue
        crossing_pairs += 1
        x = c1 * b2 - c2 * b1
        y = a1 * c2 - a2 * c1
        if det < 0:
            x, y, det = -x, -y, -det
        if x < 0 or y < 0 or x * ld > ln * det or y * ld > ln * det:
            continue
        inside_pairs += 1
        g = gcd(x, y, det)
        inside.add((x // g, y // g, det // g))
    return inside, crossing_pairs, inside_pairs


def depth_at(vertex: Vertex, prepared: Sequence[tuple[Slab, Slab, Fraction]]) -> Fraction:
    x, y, d = vertex
    total = Fraction(0)
    for (a1, b1, lo1, hi1), (a2, b2, lo2, hi2), weight in prepared:
        value = a1 * x + b1 * y
        if value < lo1 * d or value > hi1 * d:
            continue
        value = a2 * x + b2 * y
        if value < lo2 * d or value > hi2 * d:
            continue
        total += weight
    return total


def fold(half_tangent: Fraction) -> Fraction:
    """One representative per square orientation: ``t = 1`` is the axis-parallel square."""
    return Fraction(0) if half_tangent == 1 else half_tangent


def d4_isometries(outer: Fraction) -> list[tuple[str, Isometry, bool]]:
    """The eight symmetries of ``[0, L]^2`` about its centre; the flag marks reflections."""
    side = outer
    return [
        ("identity", lambda p: (p[0], p[1]), False),
        ("rotation by 90", lambda p: (side - p[1], p[0]), False),
        ("rotation by 180", lambda p: (side - p[0], side - p[1]), False),
        ("rotation by 270", lambda p: (p[1], side - p[0]), False),
        ("reflection in x = L/2", lambda p: (side - p[0], p[1]), True),
        ("reflection in y = L/2", lambda p: (p[0], side - p[1]), True),
        ("reflection in y = x", lambda p: (p[1], p[0]), True),
        ("reflection in x + y = L", lambda p: (side - p[1], side - p[0]), True),
    ]


# ----------------------------------------------------------------------------- the record


@dataclass(frozen=True, slots=True)
class Record:
    n: int
    outer_side: Fraction
    square_side: Fraction
    net: list[Fraction]
    squares: list[Square]


def parse_record(data: dict[str, Any]) -> Record:
    n = data["n"]
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ValueError("n must be a positive integer")
    net_raw = data["half_tangents"]
    placements_raw = data["placements"]
    if not isinstance(net_raw, list) or not isinstance(placements_raw, list):
        raise TypeError("half_tangents and placements must be lists")
    net = [Fraction(str(t)) for t in net_raw]
    squares: list[Square] = []
    for entry in placements_raw:
        if not isinstance(entry, list) or len(entry) != 5:
            raise ValueError(f"placement is not a 5-tuple: {entry!r}")
        t, x, y, w, s = (Fraction(str(v)) for v in entry)
        squares.append(Square(t, x, y, w, s))
    return Record(
        n=n,
        outer_side=Fraction(str(data["outer_side"])),
        square_side=Fraction(str(data["square_side"])),
        net=net,
        squares=squares,
    )


def describe_net(net: Sequence[Fraction]) -> dict[str, Any]:
    """Whether the net is the uniform half-tangent net ``T k / steps``; a record fact."""
    steps = len(net) - 1
    limit = net[-1] if net else Fraction(0)
    uniform = steps > 0 and all(net[k] == limit * k / steps for k in range(steps + 1))
    return {
        "size": len(net),
        "limit": str(limit),
        "uniform_steps": steps if uniform else None,
        "strictly_increasing": all(a < b for a, b in pairwise(net)),
    }


# ----------------------------------------------------------------------------- conditions


def check_k0(record: Record) -> dict[str, Any]:
    net_index = {t: k for k, t in enumerate(record.net)}
    failures: list[str] = []
    classes: list[str] = []
    indices_used: set[int] = set()
    for i, sq in enumerate(record.squares):
        if sq.side != record.square_side:
            failures.append(f"placement {i}: side {sq.side} is not B = {record.square_side}")
        if sq.weight < 0:
            failures.append(f"placement {i}: negative weight {sq.weight}")
        if not 0 <= sq.half_tangent <= 1:
            failures.append(f"placement {i}: half-tangent {sq.half_tangent} outside [0, 1]")
            classes.append("invalid")
            continue
        if sq.half_tangent in net_index:
            classes.append("net")
            indices_used.add(net_index[sq.half_tangent])
        elif sq.mirror_half_tangent in net_index:
            classes.append("mirror")
            indices_used.add(net_index[sq.mirror_half_tangent])
        else:
            classes.append("invalid")
            failures.append(
                f"placement {i}: half-tangent {sq.half_tangent} is neither a net angle "
                f"nor the mirror of one"
            )
    return {
        "holds": not failures,
        "failures": failures,
        "net_placements": classes.count("net"),
        "mirror_placements": classes.count("mirror"),
        "net_indices_used": sorted(indices_used),
        "net_half_tangents_used": [str(record.net[k]) for k in sorted(indices_used)],
        "distinct_half_tangents": len({sq.half_tangent for sq in record.squares}),
        "distinct_orientations": len({fold(sq.half_tangent) for sq in record.squares}),
    }


def check_k1(record: Record) -> dict[str, Any]:
    outer = record.outer_side
    failures: list[str] = []
    for i, sq in enumerate(record.squares):
        for x, y in sq.corners():
            if not (0 <= x <= outer and 0 <= y <= outer):
                failures.append(f"placement {i}: corner ({x}, {y}) outside [0, {outer}]^2")
    return {
        "holds": not failures,
        "failures": failures,
        "corners_checked": 4 * len(record.squares),
    }


def check_k2(record: Record) -> dict[str, Any]:
    started = time.perf_counter()
    prepared = [(*sq.slabs(), sq.weight) for sq in record.squares]
    edge_lines = [
        line for slab_pair in prepared for slab in slab_pair[:2] for line in slab_lines(slab)
    ]
    lines = sorted({*edge_lines, *wall_lines(record.outer_side)})
    vertices, crossing_pairs, inside_pairs = arrangement_vertices(lines, record.outer_side)
    enumerated = time.perf_counter()
    histogram: Counter[Fraction] = Counter()
    best = Fraction(-1)
    attaining = 0
    witness: Vertex | None = None
    for vertex in sorted(vertices):
        depth = depth_at(vertex, prepared)
        histogram[depth] += 1
        if depth > best:
            best, attaining, witness = depth, 1, vertex
        elif depth == best:
            attaining += 1
    finished = time.perf_counter()
    witness_point = None
    if witness is not None:
        witness_point = [
            str(Fraction(witness[0], witness[2])),
            str(Fraction(witness[1], witness[2])),
        ]
    return {
        "holds": best == 1,
        "max_depth": str(best),
        "max_depth_float": float(best),
        "attaining_vertices": attaining,
        "first_attaining_vertex": witness_point,
        "vertices": len(vertices),
        "edge_lines": 4 * len(record.squares),
        "distinct_lines": len(lines),
        "crossing_pairs": crossing_pairs,
        "inside_pairs": inside_pairs,
        "depth_histogram": {str(d): histogram[d] for d in sorted(histogram)},
        "enumeration_seconds": round(enumerated - started, 3),
        "depth_seconds": round(finished - enumerated, 3),
    }


def check_k3(record: Record) -> dict[str, Any]:
    total = sum((sq.weight for sq in record.squares), Fraction(0))
    return {"holds": total == record.n, "total_weight": str(total), "n": record.n}


def check_d4(record: Record) -> dict[str, Any]:
    """Both multisets, corner sets and folded triples, under each of the eight isometries."""
    corner_sets = Counter((frozenset(sq.corners()), sq.weight) for sq in record.squares)
    triples = Counter(
        (fold(sq.half_tangent), sq.centre_x, sq.centre_y, sq.weight, sq.side)
        for sq in record.squares
    )
    by_corners: dict[str, bool] = {}
    by_triples: dict[str, bool] = {}
    for name, image, reflects in d4_isometries(record.outer_side):
        moved_corners = Counter(
            (frozenset(image(p) for p in sq.corners()), sq.weight) for sq in record.squares
        )
        by_corners[name] = moved_corners == corner_sets
        moved_triples: Counter[tuple[Fraction, Fraction, Fraction, Fraction, Fraction]] = (
            Counter()
        )
        for sq in record.squares:
            t = sq.mirror_half_tangent if reflects else sq.half_tangent
            x, y = image((sq.centre_x, sq.centre_y))
            moved_triples[fold(t), x, y, sq.weight, sq.side] += 1
        by_triples[name] = moved_triples == triples
    return {
        "holds": all(by_corners.values()) and all(by_triples.values()),
        "corner_multiset_invariant": by_corners,
        "triple_multiset_invariant": by_triples,
        "orbit_count_if_free": Fraction(len(record.squares), 8).__str__(),
    }


def theorem(record: Record, k0: dict[str, Any]) -> str:
    used = ", ".join(str(k) for k in k0["net_indices_used"])
    return (
        f"For n = {record.n}, L = {record.outer_side}, B = {record.square_side}: no "
        f"D4-symmetric measure on [0, L]^2 of total mass below {record.n} gives mass >= 1 "
        f"to every closed "
        f"B-square at a net angle inside [0, L]^2, for this net and every net containing the "
        f"net angles with indices {used}, for this B and every smaller B, and for this L and "
        f"every larger L. Hence the point-atom certificate method (conditions C1-C5) cannot "
        f"certify s({record.n}) >= {record.outer_side} at this shrink, at any smaller shrink "
        f"on such a net, or at any larger side. It says nothing about whether {record.n} unit "
        f"squares fit in side {record.outer_side}."
    )


def decide(record: Record) -> dict[str, Any]:
    started = time.perf_counter()
    k0 = check_k0(record)
    k1 = check_k1(record)
    k2 = check_k2(record)
    k3 = check_k3(record)
    d4 = check_d4(record)
    proved = k0["holds"] and k1["holds"] and k2["holds"] and k3["holds"]
    return {
        "n": record.n,
        "outer_side": str(record.outer_side),
        "square_side": str(record.square_side),
        "placements": len(record.squares),
        "net": describe_net(record.net),
        "K0": k0,
        "K1": k1,
        "K2": k2,
        "K3": k3,
        "D4": d4,
        "regime": "net" if k0["holds"] else "invalid",
        "symmetric_only": k0["mirror_placements"] > 0,
        "proved": proved,
        "theorem": theorem(record, k0) if proved else None,
        "seconds": round(time.perf_counter() - started, 3),
    }


# ----------------------------------------------------------------------------- controls


def controls(record: Record) -> list[dict[str, Any]]:
    """Three perturbations the reader must reject, each on the condition named."""
    first = record.squares[0]
    scaled = replace(
        record,
        squares=[replace(sq, weight=sq.weight * Fraction(8, 7)) for sq in record.squares],
    )
    shifted = replace(
        record,
        squares=[
            replace(first, centre_x=first.centre_x + record.outer_side),
            *record.squares[1:],
        ],
    )
    tilted = replace(
        record, squares=[replace(first, half_tangent=Fraction(1, 3)), *record.squares[1:]]
    )
    outcomes: list[dict[str, Any]] = []
    for name, perturbed, must_fail in (
        ("weights scaled by 8/7", scaled, ("K2", "K3")),
        ("first centre shifted by L", shifted, ("K1",)),
        ("first half-tangent set to 1/3", tilted, ("K0",)),
    ):
        verdict = decide(perturbed)
        failed = [k for k in ("K0", "K1", "K2", "K3") if not verdict[k]["holds"]]
        outcomes.append(
            {
                "control": name,
                "rejected": not verdict["proved"],
                "expected_failures": list(must_fail),
                "observed_failures": failed,
                "as_expected": (not verdict["proved"]) and all(k in failed for k in must_fail),
                "max_depth": verdict["K2"]["max_depth"],
                "total_weight": verdict["K3"]["total_weight"],
            }
        )
    return outcomes


# ----------------------------------------------------------------------------- CLI


def read_record(path: Path, expected_sha256: str | None = None) -> tuple[Record, str]:
    """The parsed record and its SHA-256, refused when the digest is not the expected one."""
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if expected_sha256 is not None and digest != expected_sha256.lower():
        raise ValueError(f"SHA-256 {digest} differs from the expected {expected_sha256}")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise TypeError("record is not a JSON object")
    return parse_record(data), digest


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("record", nargs="?", type=Path, default=DEFAULT_RECORD)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--expect-sha256",
        default=None,
        help=f"refuse a record whose SHA-256 differs (retained: {RETAINED_SHA256})",
    )
    parser.add_argument(
        "--control",
        action="store_true",
        help="also run the three perturbed records and require each to be rejected",
    )
    args = parser.parse_args(argv)
    try:
        record, digest = read_record(args.record, args.expect_sha256)
        result = decide(record)
        result["record"] = str(args.record)
        result["sha256"] = digest
        result["retained_sha256_matches"] = digest == RETAINED_SHA256
        code = 0 if result["proved"] else 1
        if args.control:
            outcomes = controls(record)
            result["controls"] = outcomes
            if not all(o["as_expected"] for o in outcomes):
                code = 1
    except (ValueError, OSError, KeyError, TypeError, ZeroDivisionError) as error:
        result = {
            "status": "error",
            "proved": False,
            "error": f"{type(error).__name__}: {error}",
        }
        code = 2
    text = json.dumps(result, indent=2) + "\n"
    if args.output is not None:
        args.output.write_text(text)
    print(text, end="")
    return code


if __name__ == "__main__":
    sys.exit(main())
