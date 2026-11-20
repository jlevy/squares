"""A packing decided by both methods: every square, every wall and every pair.

There is no distance filter and no tolerance: each of the n squares is tested for being a
unit square and against each of the four walls, and each of the n(n-1)/2 pairs is decided,
by method A (`r1038_sat`, integers) and by method B (`r1038_clip`, GMP rationals). The
verdict is ACCEPT only when both methods find every square a unit square inside the box,
no pair overlapping, and the same class everywhere.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from decimal import Context, Decimal
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1038_clip as clip  # noqa: E402
import r1038_sat as sat  # noqa: E402

WALLS = ("left", "bottom", "right", "top")
A_PAIR = {1: "apart", 0: "contact", -1: "overlap"}
A_WALL = {1: "clear", 0: "touching", -1: "crossing"}
_CONTEXT = Context(prec=80)


def decimal(value: Fraction, digits: int = 16) -> str:
    """A reporting decimal (never used to decide): `digits` significant figures."""
    if value == 0:
        return "0"
    quotient = _CONTEXT.divide(Decimal(value.numerator), Decimal(value.denominator))
    return f"{quotient:.{digits - 1}e}"


def fixed(value: Fraction, places: int) -> str:
    """A reporting decimal truncated toward zero at `places` places (never used to decide)."""
    scaled = abs(value.numerator) * 10**places // value.denominator
    sign_text = "-" if value < 0 else ""
    whole, part = divmod(scaled, 10**places)
    return f"{sign_text}{whole}.{part:0{places}d}"


@dataclass
class Decision:
    """Everything both methods found, in exact terms."""

    n: int
    side: Fraction
    unit_a: list[bool] = field(default_factory=list)
    unit_b: list[bool] = field(default_factory=list)
    sense_b: list[int] = field(default_factory=list)
    clear_a: list[list[Fraction]] = field(default_factory=list)
    wall_a: list[list[str]] = field(default_factory=list)
    wall_b: list[list[str]] = field(default_factory=list)
    inside_b: list[Fraction] = field(default_factory=list)
    margins: dict[tuple[int, int], Fraction] = field(default_factory=dict)
    pair_b: dict[tuple[int, int], tuple[str, Fraction]] = field(default_factory=dict)
    disagreements: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    verdict: str = "REFUSE"

    def pair_class_a(self, key: tuple[int, int]) -> str:
        value = self.margins[key]
        return A_PAIR[(value > 0) - (value < 0)]


def decide(
    side: Fraction,
    centers: list[tuple[Fraction, Fraction]],
    bases: list[tuple[Fraction, Fraction]],
) -> Decision:
    """Decide a packing of len(centers) squares in [0, side]^2 by both methods."""
    n = len(centers)
    result = Decision(n=n, side=side)
    ints = [sat.integer_square(c[0], c[1], u[0], u[1]) for c, u in zip(centers, bases)]
    side_q = clip.to_mpq(side)
    polygons: list[list[clip.Point] | None] = []
    for index, (c, u) in enumerate(zip(centers, bases), start=1):
        unit_a = sat.is_unit(ints[index - 1])
        points = clip.corners(clip.to_mpq(c[0]), clip.to_mpq(c[1]), clip.to_mpq(u[0]), clip.to_mpq(u[1]))
        unit_b = clip.unit_square(points)
        result.unit_a.append(unit_a)
        result.unit_b.append(unit_b)
        if unit_a != unit_b:
            result.disagreements.append(f"square {index}: unit by A {unit_a}, by B {unit_b}")
        if not (unit_a and unit_b):
            result.reasons.append(f"square {index} is not a unit square")
            result.sense_b.append(0)
            polygons.append(None)
            result.clear_a.append([])
            result.wall_a.append([])
            result.wall_b.append([])
            result.inside_b.append(Fraction(-1))
            continue
        ccw, sense = clip.counterclockwise(points)
        result.sense_b.append(sense)
        polygons.append(ccw)
        ratios = sat.clearances(ints[index - 1], side)
        values = [sat.as_fraction(r) for r in ratios]
        classes_a = [A_WALL[sat.sign(r)] for r in ratios]
        classes_b, area = clip.walls(ccw, side_q)
        inside = Fraction(int(area.numerator), int(area.denominator))
        result.clear_a.append(values)
        result.wall_a.append(classes_a)
        result.wall_b.append(classes_b)
        result.inside_b.append(inside)
        for wall, class_a, class_b in zip(WALLS, classes_a, classes_b):
            if class_a != class_b:
                result.disagreements.append(f"square {index} {wall}: A {class_a}, B {class_b}")
            if class_a == "crossing":
                result.reasons.append(f"square {index} crosses the {wall} wall")
        inside_a = all(sat.sign(r) >= 0 for r in ratios)
        if inside_a != (inside == 1):
            result.disagreements.append(f"square {index}: inside by A {inside_a}, area inside by B {inside}")
        if inside != 1 and inside_a:
            result.reasons.append(f"square {index} is not inside by B")
    for i in range(n):
        poly_i = polygons[i]
        if poly_i is None:
            continue
        for j in range(i + 1, n):
            poly_j = polygons[j]
            if poly_j is None:
                continue
            ratio = sat.margin(ints[i], ints[j])
            value = sat.as_fraction(ratio)
            key = (i + 1, j + 1)
            result.margins[key] = value
            class_a = A_PAIR[sat.sign(ratio)]
            class_b, area, agree = clip.pair(poly_i, poly_j)
            result.pair_b[key] = (class_b, Fraction(int(area.numerator), int(area.denominator)))
            if not agree:
                result.disagreements.append(f"pair {key}: B's two orders disagree")
            if class_a != class_b:
                result.disagreements.append(f"pair {key}: A {class_a}, B {class_b}")
            if class_a == "overlap" or class_b == "overlap":
                result.reasons.append(f"pair {key} overlaps")
    if result.disagreements:
        result.reasons.append(f"{len(result.disagreements)} disagreements between the methods")
    result.verdict = "ACCEPT" if not result.reasons else "REFUSE"
    return result


def summary(result: Decision, near: int = 40) -> dict[str, object]:
    """The facts a receipt reports: counts, contacts, least margins and clearances."""
    ordered = sorted(result.margins.items(), key=lambda item: (item[1], item[0]))
    classes = {"apart": 0, "contact": 0, "overlap": 0}
    for key in result.margins:
        classes[result.pair_class_a(key)] += 1
    contacts = []
    least_positive: tuple[Fraction, int, str] | None = None
    for index, values in enumerate(result.clear_a, start=1):
        for wall, value in zip(WALLS, values):
            if value == 0:
                contacts.append([index, wall])
            elif value > 0 and (least_positive is None or value < least_positive[0]):
                least_positive = (value, index, wall)
    extents = {}
    for k, wall in enumerate(WALLS):
        column = [values[k] for values in result.clear_a if values]
        if column:
            extents[wall] = {"least_clearance": str(min(column)), "decimal": decimal(min(column))}
    out: dict[str, object] = {
        "verdict": result.verdict,
        "n": result.n,
        "side": str(result.side),
        "side_decimal_40": fixed(result.side, 40),
        "unit_squares": {"A": sum(result.unit_a), "B": sum(result.unit_b)},
        "senses_B": {"counterclockwise": result.sense_b.count(1), "clockwise": result.sense_b.count(-1)},
        "pairs": len(result.margins),
        "pair_classes_A": classes,
        "pair_classes_B": {
            name: sum(1 for value in result.pair_b.values() if value[0] == name)
            for name in ("apart", "contact", "overlap")
        },
        "wall_contacts": contacts,
        "wall_crossings": [
            [index, wall]
            for index, values in enumerate(result.clear_a, start=1)
            for wall, value in zip(WALLS, values)
            if value < 0
        ],
        "least_positive_clearance": None
        if least_positive is None
        else {
            "value": str(least_positive[0]),
            "decimal": decimal(least_positive[0]),
            "square": least_positive[1],
            "wall": least_positive[2],
        },
        "least_clearance_by_wall": extents,
        "inside_area_one_B": sum(1 for value in result.inside_b if value == 1),
        "least_pair_margin": None
        if not ordered
        else {"pair": list(ordered[0][0]), "value": str(ordered[0][1]), "decimal": decimal(ordered[0][1])},
        "nearest_pairs": [
            {"pair": list(key), "margin": str(value), "decimal": decimal(value)} for key, value in ordered[:near]
        ],
        "pairs_below": {
            label: sum(1 for value in result.margins.values() if value < bound)
            for label, bound in (
                ("1e-15", Fraction(1, 10**15)),
                ("1e-12", Fraction(1, 10**12)),
                ("1e-9", Fraction(1, 10**9)),
                ("1e-6", Fraction(1, 10**6)),
                ("1e-3", Fraction(1, 10**3)),
            )
        },
        "disagreements": result.disagreements[:50],
        "disagreement_count": len(result.disagreements),
        "reasons": result.reasons[:50],
    }
    return out
