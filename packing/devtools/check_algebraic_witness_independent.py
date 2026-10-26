#!/usr/bin/env python3
"""Independent exact checker for Witness/v2 files over a real number field.

Usage, from `packing/`:

    uv run --frozen python -m devtools.check_algebraic_witness_independent WITNESS.yaml[.gz]

The second exact route for a pose over a number field `Q(alpha)`, the role
`devtools.check_rational_witness_independent` has over `Q` (regularization policy,
obligation 1). It shares no arithmetic, geometry or verification code with
`sqpack.field`, `sqpack.witness` or `sqpack.verify`, which decide the first route, so a
shared sign, reduction, root-isolation or corner-order defect cannot pass both. It reads
the witness's own text, expands its squares itself and decides:

1. **The field.** The minimal polynomial `p` and the isolating interval `(lo, hi)` as the
   file states them. Its own Sturm sequence shows that `p` has exactly one real root in
   the open interval and that neither endpoint is a root; that root is `alpha`. An element
   is a polynomial in `alpha` of degree below `deg p`, reduced modulo `p`. Irreducibility
   is not assumed: reduction modulo `p` is evaluation at `alpha` because `p(alpha) = 0`, so
   a reduced polynomial that is identically zero is zero at `alpha`, and a nonzero one is
   decided by the next step whether `p` factors or not.
2. **Signs.** A nonzero element `q` is enclosed by the mean-value form at the midpoint
   `m` of the current root interval, `q(m) +- r * sum(k |q_k| R^(k-1))` with `r` the half
   width and `R` the larger endpoint magnitude, all in exact rationals; where the enclosure
   holds zero the interval is bisected by the sign of `p` at its midpoint and the form
   evaluated again. After `GCD_AFTER` bisections, `gcd(p, q)` decides whether `q(alpha) = 0`
   by a Sturm count of its roots in the interval, so the loop ends for every element.
   (`sqpack.field` encloses by interval Horner over a polynomial it requires irreducible.)
3. **Squares.** Each square is a centre and a basis `(c, s)` or four corners; its two
   axes must be exact unit vectors at a right angle (`c^2 + s^2 - 1 = 0`, or for corners
   `|e0|^2 = |e1|^2 = 1`, `e0 . e1 = 0` and the corners closing a parallelogram).
4. **Containment.** Every corner's coordinates lie in `[0, S]`, `S` the side, decided
   exactly.
5. **Non-overlap.** A pair whose centres lie at least `3/2` apart along `x` or `y` is
   separated: a unit square lies within `sqrt(2)/2 < 3/4` of its centre. That is read off
   exact rational enclosures of the centres, from a sweep over `x`. Every other pair is
   decided by the separating-axis theorem over the four edge normals: along a unit normal
   `u`, the separation `|u . d| - h_i(u) - h_j(u)`, with `d` the centre difference and
   `h(u) = (|u . e0| + |u . e1|) / 2` a square's half-extent, is computed exactly in the
   field with every absolute value resolved by an exact sign; the interiors are disjoint
   exactly when one of the four separations is non-negative. The normals are tried in
   the order binary64 ranks them, which decides nothing.

The result has the rational checker's shape (`verification_passed`, `failures`,
`pairs_tested`), with `field` naming the field, and the least separations as decimals.
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from sqpack.yamlio import safe_load

#: Bisections of the root interval before `gcd(p, q)` decides whether `q(alpha)` is zero.
GCD_AFTER = 400
#: A pair of unit squares this far apart along an axis cannot overlap (`3/2 > sqrt(2)`).
REACH = Fraction(3, 2)
#: Bisections made before any element is enclosed, so most signs need none of their own.
START_BITS = 160

type Poly = list[Fraction]
"""Coefficients, lowest degree first."""


class WitnessFormatError(ValueError):
    """The file is not a number-field Witness/v2 document this checker reads."""


# --------------------------------------------------------------------------------------
# Polynomials over Q, lowest degree first
# --------------------------------------------------------------------------------------


def trim(poly: Sequence[Fraction]) -> Poly:
    out = list(poly)
    while out and out[-1] == 0:
        out.pop()
    return out


def evaluate(poly: Sequence[Fraction], x: Fraction) -> Fraction:
    total = Fraction(0)
    for coefficient in reversed(poly):
        total = total * x + coefficient
    return total


def remainder(dividend: Sequence[Fraction], divisor: Sequence[Fraction]) -> Poly:
    """`dividend mod divisor`, the divisor nonzero."""
    rest = trim(dividend)
    divisor = trim(divisor)
    lead = divisor[-1]
    while len(rest) >= len(divisor):
        factor = rest[-1] / lead
        shift = len(rest) - len(divisor)
        for k, value in enumerate(divisor):
            rest[shift + k] -= factor * value
        rest.pop()
        rest = trim(rest)
    return rest


def derivative(poly: Sequence[Fraction]) -> Poly:
    return trim([k * poly[k] for k in range(1, len(poly))])


def gcd(left: Sequence[Fraction], right: Sequence[Fraction]) -> Poly:
    a, b = trim(left), trim(right)
    while b:
        a, b = b, remainder(a, b)
    return a


def sturm_chain(poly: Sequence[Fraction]) -> list[Poly]:
    chain = [trim(poly), derivative(poly)]
    while chain[-1]:
        chain.append([-value for value in remainder(chain[-2], chain[-1])])
    return [link for link in chain if link]


def sign_changes(chain: Sequence[Sequence[Fraction]], x: Fraction) -> int:
    signs = [value for value in (evaluate(link, x) for link in chain) if value != 0]
    return sum(1 for a, b in itertools.pairwise(signs) if (a > 0) != (b > 0))


def roots_between(poly: Sequence[Fraction], low: Fraction, high: Fraction) -> int:
    """Distinct real roots in `(low, high]` by Sturm's theorem, neither a multiple root's
    concern: a square-free part is taken first."""
    poly = trim(poly)
    if len(poly) <= 1:
        return 0
    square_free = trim(_exact_quotient(poly, gcd(poly, derivative(poly))))
    chain = sturm_chain(square_free)
    return sign_changes(chain, low) - sign_changes(chain, high)


def _exact_quotient(dividend: Sequence[Fraction], divisor: Sequence[Fraction]) -> Poly:
    rest = trim(dividend)
    divisor = trim(divisor)
    quotient = [Fraction(0)] * max(len(rest) - len(divisor) + 1, 1)
    while len(rest) >= len(divisor) and rest:
        factor = rest[-1] / divisor[-1]
        shift = len(rest) - len(divisor)
        quotient[shift] = factor
        for k, value in enumerate(divisor):
            rest[shift + k] -= factor * value
        rest = trim(rest[:-1]) if rest[-1] == 0 else trim(rest)
    return quotient


# --------------------------------------------------------------------------------------
# The field Q(alpha)
# --------------------------------------------------------------------------------------


class Field:
    """`Q(alpha)`, `alpha` the one root of `p` in the stated open interval."""

    def __init__(self, high_to_low: Sequence[Fraction], interval: Sequence[Fraction]):
        coefficients = [Fraction(value) for value in high_to_low]
        if len(coefficients) < 2 or coefficients[0] == 0:
            raise WitnessFormatError("the minimal polynomial must have degree at least one")
        lead = coefficients[0]
        self.p: Poly = [value / lead for value in reversed(coefficients)]
        self.degree = len(self.p) - 1
        low, high = Fraction(interval[0]), Fraction(interval[1])
        if low >= high:
            raise WitnessFormatError("the isolating interval is empty")
        if evaluate(self.p, low) == 0 or evaluate(self.p, high) == 0:
            raise WitnessFormatError("an endpoint of the isolating interval is a root")
        if roots_between(self.p, low, high) != 1:
            raise WitnessFormatError("the isolating interval holds no single root")
        self.declared = (low, high)
        self.low, self.high = low, high
        self.low_positive = evaluate(self.p, low) > 0
        self.bisections = 0
        self.gcd_decisions = 0
        self.refine(START_BITS)

    # -- the root ---------------------------------------------------------------------

    def bisect(self) -> None:
        middle = (self.low + self.high) / 2
        value = evaluate(self.p, middle)
        if value == 0:  # `p` factors over Q with a rational root, and it is `alpha`.
            self.low = self.high = middle
            return
        if (value > 0) == self.low_positive:
            self.low = middle
        else:
            self.high = middle
        self.bisections += 1

    def refine(self, bits: int) -> None:
        width = (self.high - self.low) / 2**bits
        while self.high - self.low > width and self.high != self.low:
            self.bisect()

    # -- elements ---------------------------------------------------------------------

    def reduce(self, poly: Sequence[Fraction]) -> Poly:
        out = list(poly)
        d = self.degree
        for top in range(len(out) - 1, d - 1, -1):
            value = out[top]
            if value:
                out[top] = Fraction(0)
                for k in range(d):
                    out[top - d + k] -= value * self.p[k]
        out = out[:d]
        return out + [Fraction(0)] * (d - len(out))

    def scalar(self, value: Any) -> Poly:
        """A literal of the witness format: a rational string or coefficient strings."""
        if isinstance(value, str):
            return self.reduce([Fraction(value)])
        if isinstance(value, list) and value and all(isinstance(item, str) for item in value):
            return self.reduce([Fraction(item) for item in value])
        raise WitnessFormatError(f"not a scalar of the field: {value!r}")

    def rational(self, value: Fraction) -> Poly:
        return self.reduce([Fraction(value)])

    def mul(self, left: Sequence[Fraction], right: Sequence[Fraction]) -> Poly:
        out = [Fraction(0)] * (len(left) + len(right) - 1)
        for i, a in enumerate(left):
            if a:
                for j, b in enumerate(right):
                    if b:
                        out[i + j] += a * b
        return self.reduce(out)

    def enclose(self, q: Sequence[Fraction]) -> tuple[Fraction, Fraction]:
        """The mean-value enclosure of `q(alpha)` on the current root interval."""
        middle = (self.low + self.high) / 2
        radius = (self.high - self.low) / 2
        reach = max(abs(self.low), abs(self.high))
        slope = sum((k * abs(q[k]) * reach ** (k - 1) for k in range(1, len(q))), Fraction(0))
        centre = evaluate(q, middle)
        return centre - radius * slope, centre + radius * slope

    def sign(self, q: Sequence[Fraction]) -> int:
        if all(value == 0 for value in q):
            return 0
        tries = 0
        while True:
            low, high = self.enclose(q)
            if low > 0:
                return 1
            if high < 0:
                return -1
            if self.high == self.low:  # a rational root: the centre is the value
                value = evaluate(q, self.low)
                return (value > 0) - (value < 0)
            tries += 1
            if tries == GCD_AFTER:
                common = gcd(self.p, q)
                if len(common) > 1 and roots_between(common, self.low, self.high) > 0:
                    self.gcd_decisions += 1
                    return 0
            self.bisect()

    def decimal(self, q: Sequence[Fraction], digits: int = 12) -> str:
        low, high = self.enclose(q)
        return f"{float((low + high) / 2):.{digits}e}"

    def approximate(self, q: Sequence[Fraction]) -> float:
        low, high = self.enclose(q)
        return float((low + high) / 2)


def add(left: Sequence[Fraction], right: Sequence[Fraction]) -> Poly:
    return [a + b for a, b in zip(left, right, strict=True)]


def sub(left: Sequence[Fraction], right: Sequence[Fraction]) -> Poly:
    return [a - b for a, b in zip(left, right, strict=True)]


def scale(value: Fraction, poly: Sequence[Fraction]) -> Poly:
    return [value * a for a in poly]


# --------------------------------------------------------------------------------------
# Squares
# --------------------------------------------------------------------------------------

type Vector = tuple[Poly, Poly]


@dataclass(frozen=True)
class Square:
    """A unit square: its centre and its two axes, exact in the field."""

    label: str
    centre: Vector
    axes: tuple[Vector, Vector]
    corners: tuple[Vector, ...]


def dot(field: Field, u: Vector, v: Vector) -> Poly:
    return add(field.mul(u[0], v[0]), field.mul(u[1], v[1]))


def parse(witness: Mapping[str, Any]) -> tuple[Field, Poly, list[Square], dict[str, Any]]:
    """The field, the side and the squares, read from a witness's own fields."""
    scalar = witness.get("scalar")
    if not isinstance(scalar, Mapping) or scalar.get("kind") != "algebraic-number-field":
        raise WitnessFormatError("this checker reads algebraic-number-field witnesses only")
    if witness.get("square_size") != "1":
        raise WitnessFormatError("this checker reads unit squares only")
    if witness.get("coordinates") != {
        "origin": "lower-left",
        "axes": "x-right-y-up",
        "angle_unit": "not-applicable",
    }:
        raise WitnessFormatError("this checker requires lower-left x-right-y-up coordinates")
    representation = witness.get("representation")
    if representation not in ("center-basis", "corners"):
        raise WitnessFormatError("this checker reads center-basis or corners witnesses")
    polynomial = scalar.get("minimal_polynomial")
    interval = scalar.get("isolating_interval")
    if not isinstance(polynomial, list) or not isinstance(interval, list) or len(interval) != 2:
        raise WitnessFormatError("the field needs a minimal polynomial and an interval")
    field = Field(
        [Fraction(str(value)) for value in polynomial], [Fraction(str(v)) for v in interval]
    )
    raw = witness.get("squares")
    n = witness.get("n")
    if type(n) is not int or not isinstance(raw, list) or len(raw) != n or n < 1:
        raise WitnessFormatError("declared n does not match the complete square list")
    ids = [square.get("id") if isinstance(square, Mapping) else None for square in raw]
    if len({str(value) for value in ids}) != len(ids):
        raise WitnessFormatError("square ids are not unique")
    half = Fraction(1, 2)
    squares: list[Square] = []
    for square in raw:
        label = str(square.get("id"))
        if representation == "center-basis":
            centre = (field.scalar(square["center"][0]), field.scalar(square["center"][1]))
            c, s = field.scalar(square["basis"][0]), field.scalar(square["basis"][1])
            e0: Vector = (c, s)
            e1: Vector = ([-v for v in s], c)
            corners = tuple(
                (
                    add(centre[0], sub(scale(a, c), scale(b, s))),
                    add(centre[1], add(scale(a, s), scale(b, c))),
                )
                for a, b in ((-half, -half), (half, -half), (half, half), (-half, half))
            )
        else:
            corners = tuple(
                (field.scalar(point[0]), field.scalar(point[1])) for point in square["corners"]
            )
            if len(corners) != 4:
                raise WitnessFormatError(f"square {label} has no four corners")
            e0 = (sub(corners[1][0], corners[0][0]), sub(corners[1][1], corners[0][1]))
            e1 = (sub(corners[2][0], corners[1][0]), sub(corners[2][1], corners[1][1]))
            centre = (
                scale(half, add(corners[0][0], corners[2][0])),
                scale(half, add(corners[0][1], corners[2][1])),
            )
        squares.append(Square(label, centre, (e0, e1), corners))
    side = field.scalar(witness.get("side"))
    info = {"n": n, "id": witness.get("id"), "representation": representation}
    return field, side, squares, info


def square_failures(field: Field, square: Square) -> list[str]:
    e0, e1 = square.axes
    one = field.rational(Fraction(1))
    failures = []
    if field.sign(sub(dot(field, e0, e0), one)) != 0:
        failures.append(f"square {square.label}: its first axis is not a unit vector")
    if field.sign(sub(dot(field, e1, e1), one)) != 0:
        failures.append(f"square {square.label}: its second axis is not a unit vector")
    if field.sign(dot(field, e0, e1)) != 0:
        failures.append(f"square {square.label}: its axes are not at a right angle")
    p0, _p1, p2, p3 = square.corners
    closing = (
        sub(add(p0[0], e1[0]), p3[0]),
        sub(add(p0[1], e1[1]), p3[1]),
        sub(add(p0[0], add(e0[0], e1[0])), p2[0]),
        sub(add(p0[1], add(e0[1], e1[1])), p2[1]),
    )
    if any(field.sign(value) != 0 for value in closing):
        failures.append(f"square {square.label}: its corners do not close a square")
    return failures


def magnitude(field: Field, q: Poly) -> Poly:
    return [-v for v in q] if field.sign(q) < 0 else q


def half_extent(field: Field, square: Square, normal: Vector) -> Poly:
    """`(|u . e0| + |u . e1|) / 2` for the unit normal `u`."""
    e0, e1 = square.axes
    return scale(
        Fraction(1, 2),
        add(magnitude(field, dot(field, normal, e0)), magnitude(field, dot(field, normal, e1))),
    )


def separation(field: Field, left: Square, right: Square, normal: Vector, own: Square) -> Poly:
    """`|u . d| - h_left(u) - h_right(u)` along `normal`, an axis of `own`."""
    d = (sub(right.centre[0], left.centre[0]), sub(right.centre[1], left.centre[1]))
    along = magnitude(field, dot(field, normal, d))
    half = field.rational(Fraction(1, 2))
    h_left = half if own is left else half_extent(field, left, normal)
    h_right = half if own is right else half_extent(field, right, normal)
    return sub(sub(along, h_left), h_right)


def float_separation(
    centre: Sequence[tuple[float, float]],
    axes: Sequence[tuple[tuple[float, float], tuple[float, float]]],
    i: int,
    j: int,
    normal: tuple[float, float],
) -> float:
    dx, dy = centre[j][0] - centre[i][0], centre[j][1] - centre[i][1]
    along = abs(normal[0] * dx + normal[1] * dy)

    def h(k: int) -> float:
        (a, b), (c, d) = axes[k]
        return 0.5 * (abs(normal[0] * a + normal[1] * b) + abs(normal[0] * c + normal[1] * d))

    return along - h(i) - h(j)


def near_pairs(field: Field, squares: Sequence[Square]) -> tuple[list[tuple[int, int]], int]:
    """Pairs whose exact centre enclosures are within `REACH` along both axes, and how many
    pairs the sweep separated."""
    boxes = []
    for square in squares:
        (x_low, x_high), (y_low, y_high) = (
            field.enclose(square.centre[0]),
            field.enclose(square.centre[1]),
        )
        boxes.append((x_low, x_high, y_low, y_high))
    order = sorted(range(len(squares)), key=lambda k: boxes[k][0])
    pairs: list[tuple[int, int]] = []
    for position, i in enumerate(order):
        for j in order[position + 1 :]:
            if boxes[j][0] - boxes[i][1] >= REACH:
                break
            far_y = boxes[j][2] - boxes[i][3] >= REACH or boxes[i][2] - boxes[j][3] >= REACH
            if not far_y:
                pairs.append((min(i, j), max(i, j)))
    total = len(squares) * (len(squares) - 1) // 2
    return sorted(pairs), total - len(pairs)


def check_document(document: Mapping[str, Any]) -> dict[str, Any]:
    """Decide a number-field Witness/v2 document (its envelope) exactly, from its text."""
    metadata = document.get("softschema")
    if not isinstance(metadata, Mapping) or metadata.get("contract") != (
        "packing.squares:Witness/v2"
    ):
        raise WitnessFormatError("expected the Witness/v2 contract")
    witness = document.get("witness")
    if not isinstance(witness, Mapping):
        raise WitnessFormatError("expected a Witness/v2 envelope")
    return check_witness(witness)


def check_witness(witness: Mapping[str, Any]) -> dict[str, Any]:
    """Decide a number-field witness's packing exactly, from its own fields."""
    started = time.perf_counter()
    field, side, squares, info = parse(witness)
    failures: list[str] = []
    if field.sign(side) <= 0:
        failures.append("the side is not positive")
    for square in squares:
        failures.extend(square_failures(field, square))
    least_containment: tuple[float, str] | None = None
    leaving: list[str] = []
    for square in squares:
        for corner in square.corners:
            for coordinate in corner:
                for clearance in (coordinate, sub(side, coordinate)):
                    if field.sign(clearance) < 0 and square.label not in leaving:
                        leaving.append(square.label)
                    value = field.approximate(clearance)
                    if least_containment is None or value < least_containment[0]:
                        least_containment = (value, square.label)
    if leaving:
        failures.append(f"{len(leaving)} squares leave the container: {', '.join(leaving[:8])}")
    pairs, swept = near_pairs(field, squares)
    centre = [(field.approximate(s.centre[0]), field.approximate(s.centre[1])) for s in squares]

    def unit(axis: Vector) -> tuple[float, float]:
        return field.approximate(axis[0]), field.approximate(axis[1])

    axes = [(unit(s.axes[0]), unit(s.axes[1])) for s in squares]
    touching = 0
    overlapping: list[str] = []
    least_gap: float | None = None
    for i, j in pairs:
        ranked = sorted(
            ((owner, k) for owner in (i, j) for k in range(2)),
            key=lambda item: -float_separation(centre, axes, i, j, axes[item[0]][item[1]]),
        )
        decided = False
        best: float | None = None
        for owner, k in ranked:
            own = squares[owner]
            gap = separation(field, squares[i], squares[j], own.axes[k], own)
            sign = field.sign(gap)
            value = field.approximate(gap)
            best = value if best is None else max(best, value)
            if sign >= 0:
                touching += sign == 0
                decided = True
                break
        if best is not None and (least_gap is None or best < least_gap):
            least_gap = best
        if not decided:
            overlapping.append(f"squares {squares[i].label} and {squares[j].label} overlap")
    if overlapping:
        failures.append(f"{len(overlapping)} overlapping pairs: {'; '.join(overlapping[:4])}")
    return {
        "verification_passed": not failures,
        "coordinate_provenance": "verified" if not failures else "not-established",
        "method": "exact-algebraic",
        "field": (
            f"Q(alpha), alpha the root of a degree-{field.degree} polynomial in its stated "
            "interval"
        ),
        "checker": "devtools.check_algebraic_witness_independent",
        "n": info["n"],
        "side_decimal": field.decimal(side, 30),
        "pairs_tested": len(pairs),
        "pairs_separated_by_sweep": swept,
        "touching_pairs": touching,
        "minimum_containment_clearance": (
            f"{least_containment[0]:.6e}" if least_containment is not None else None
        ),
        "minimum_best_pair_gap": f"{least_gap:.6e}" if least_gap is not None else None,
        "root_bisections": field.bisections,
        "gcd_decisions": field.gcd_decisions,
        "seconds": round(time.perf_counter() - started, 3),
        "failures": failures,
        "limitations": "Verifies witness feasibility and its upper bound, not optimality.",
    }


def read(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if path.suffix == ".gz":
        data = gzip.decompress(data)
    document = safe_load(data.decode("utf-8"))
    if not isinstance(document, dict):
        raise WitnessFormatError("expected a YAML mapping")
    return document


def check(path: Path) -> dict[str, Any]:
    return check_document(read(path))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Decide a number-field Witness/v2 file exactly, independently of sqpack."
    )
    parser.add_argument("witness", type=Path)
    args = parser.parse_args()
    result = check(args.witness)
    print(
        ("VERIFIED" if result["verification_passed"] else "VERIFICATION FAILED")
        + f": {result['n']} squares, {result['pairs_tested']} pairs decided exactly, "
        f"{result['pairs_separated_by_sweep']} separated by the sweep"
    )
    print(f"  side: {result['side_decimal']}")
    print(f"  field: {result['field']}")
    print(f"  minimum pair gap: {result['minimum_best_pair_gap']}")
    for failure in result["failures"]:
        print(f"  FAILURE: {failure}")
    return 0 if result["verification_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
