"""Independent continuous near-axis point-cover reader.

This module derives its own rational corner polynomials and Bernstein transform.
It imports no producer geometry, tiling, polynomial, or sign routines. The only
shared project foundation is the bounded JSON byte loader; exact arithmetic uses
the standard-library Fraction implementation.

The mathematical claim is one closed ten-point cover at side 1939/500 on the two
fixed half-angle slabs. It is not the full restricted-orientation theorem, its
45-degree clause, or a packing bound. The external degree-to-half-tangent bound
for T is documented with H-106; this reader binds the exact rational T, not pi.
Target construction occurs only after a complete positive packet is admitted.
"""

from __future__ import annotations

import argparse
import json
import signal
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any

from devtools.check_full_size_density_support_ceiling import load_packet

type Polynomial = tuple[Fraction, ...]
type Point = tuple[Fraction, Fraction]
type Assignment = tuple[tuple[int, ...], ...]
type Slab = tuple[Fraction, Fraction]
type Failure = tuple[int, int, int, int, int]

SIGN_DEPTH = 12
COLUMNS = 6
ROWS = 3
POINT_CAP = 10
FIXED_SIDE = Fraction(1939, 500)
ANGLE_MAJORANT = Fraction(11, 5040)
HALF_TANGENT = ANGLE_MAJORANT / (1 - ANGLE_MAJORANT**2 / 2)
SLABS = ((-HALF_TANGENT, Fraction(0)), (Fraction(0), HALF_TANGENT))
ASSIGNMENTS = ((1, 1, 4, 4, 7, 7), (0, 3, 3, 6, 6, 9), (2, 2, 5, 5, 8, 8))
PRODUCER_INEQUALITIES = 2 * ROWS * COLUMNS * 2 * 3 * 4
READER_INEQUALITIES = 2 * ROWS * COLUMNS * 4 * 4
PACKET_BYTE_CAP = 262144
WALL_CAP_SECONDS = 10
SCOPE = "fixed P10 closed near-axis point cover at side 1939/500 and the declared slabs only"
PACKET_KEYS = {
    "version",
    "kind",
    "side",
    "grid",
    "half_angle_slabs",
    "assignments",
    "status",
    "inequalities_checked",
    "unresolved",
}


@dataclass(frozen=True)
class SlabResult:
    rectangles_checked: int
    corners_checked: int
    inequalities_checked: int
    uncertified: tuple[Failure, ...]

    @property
    def proved(self) -> bool:
        return not self.uncertified


def reflected_points(side: Fraction) -> tuple[Point, ...]:
    """Construct the four source formulas and K4 reflections, in numeric order.

    The formulas are Stromquist Theorem 3's P10 seeds, evaluated at the supplied
    rational side, not Theorem 2's repaired point set. Tests may use a toy side;
    target_input alone binds the scientific side.
    """
    if type(side) is not Fraction or side <= 1:
        raise ValueError("source formulas require an exact rational side greater than one")
    seeds = (
        (Fraction(1), Fraction(1)),
        (side / 2, Fraction(1)),
        (Fraction(3, 2) - side / 4, side / 2),
        (Fraction(1, 2) + side / 4, side / 2),
    )
    points = {
        (side - x if rx else x, side - y if ry else y)
        for x, y in seeds
        for rx in (False, True)
        for ry in (False, True)
    }
    if len(points) != POINT_CAP or any(not 0 <= value <= side for p in points for value in p):
        raise ValueError("source formulas must yield ten distinct contained points")
    return tuple(sorted(points))


def target_input() -> tuple[Fraction, tuple[Point, ...]]:
    """Fixed target binding; never called in author tests except as a mocked boundary."""
    return FIXED_SIDE, reflected_points(FIXED_SIDE)


def _labels(value: Any, point_count: int) -> Assignment:
    if type(value) not in (tuple, list) or len(value) != ROWS:
        raise ValueError("assignments require exactly three rows")
    result = []
    for row in value:
        if type(row) not in (tuple, list) or len(row) != COLUMNS:
            raise ValueError("each assignment row requires exactly six labels")
        if any(type(label) is not int or not 0 <= label < point_count for label in row):
            raise ValueError("assignments contain an invalid point label")
        result.append(tuple(row))
    return tuple(result)


def check_closed_slabs(
    side: Fraction,
    points: Sequence[Point],
    assignments: object,
    slabs: Sequence[Slab],
) -> SlabResult:
    """Check all rectangle corners over both closed slabs, with no omitted faces.

    For each t, every admissible unit-square center is in the closed center box
    [r(t), side-r(t)]². Its affine image of [0,1]² is covered by the 6-by-3 grid.
    At fixed t each signed membership margin is affine in the two normalized
    center coordinates, so its minimum on a closed rectangle is at a corner.
    A sign proof at all four corners therefore covers the rectangle, including
    edges and vertices. The two slabs include their common t=0 seam.
    """
    if type(side) is not Fraction or side <= 1:
        raise ValueError("side must define a positive-width rational center box")
    if not 1 <= len(points) <= POINT_CAP:
        raise ValueError("point inventory must be nonempty and bounded")
    if any(
        type(point) not in (tuple, list)
        or len(point) != 2
        or any(type(value) is not Fraction for value in point)
        for point in points
    ):
        raise ValueError("point coordinates must be exact rational pairs")
    canonical_points = tuple(tuple(point) for point in points)
    if any(not 0 <= value <= side for point in points for value in point):
        raise ValueError("point is outside the container")
    if (
        len(set(canonical_points)) != len(points)
        or tuple(sorted(canonical_points)) != canonical_points
    ):
        raise ValueError("points must be distinct and in numeric lexicographic order")
    if (
        len(slabs) != 2
        or any(len(slab) != 2 or any(type(t) is not Fraction for t in slab) for slab in slabs)
        or not -1 < slabs[0][0] < slabs[0][1] == 0 == slabs[1][0] < slabs[1][1] < 1
        or slabs[0][0] != -slabs[1][1]
    ):
        raise ValueError("slabs must be symmetric negative/positive closed rational intervals")
    labels = _labels(assignments, len(points))
    uncertified: list[Failure] = []
    corners = checked = rectangles = 0
    for slab_index, (left, right) in enumerate(slabs):
        sine_sign = -1 if slab_index == 0 else 1
        # D*(side-2r) = (side-1)-2*sign(t)*t+(side+1)*t².
        width = (side - 1, Fraction(-2 * sine_sign), side + 1)
        if not certifies_nonnegative(width, left, right):
            raise ValueError("could not certify a nonnegative center-box width on the slab")
        for row in range(ROWS):
            for column in range(COLUMNS):
                rectangles += 1
                point = points[labels[row][column]]
                for corner, (ix, iy) in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))):
                    normalized = (Fraction(column + ix, COLUMNS), Fraction(row + iy, ROWS))
                    corners += 1
                    for axis, polynomial in enumerate(
                        corner_polynomials(side, point, normalized, sine_sign)
                    ):
                        checked += 1
                        if not certifies_nonnegative(polynomial, left, right):
                            uncertified.append((slab_index, row, column, corner, axis))
    return SlabResult(rectangles, corners, checked, tuple(uncertified))


def _add(first: Polynomial, second: Polynomial) -> Polynomial:
    return tuple(
        (first[i] if i < len(first) else Fraction(0))
        + (second[i] if i < len(second) else Fraction(0))
        for i in range(max(len(first), len(second)))
    )


def _scale(polynomial: Polynomial, scalar: Fraction) -> Polynomial:
    return tuple(coefficient * scalar for coefficient in polynomial)


def _multiply(first: Polynomial, second: Polynomial) -> Polynomial:
    product = [Fraction(0)] * (len(first) + len(second) - 1)
    for i, a in enumerate(first):
        for j, b in enumerate(second):
            product[i + j] += a * b
    return tuple(product)


def corner_polynomials(
    side: Fraction, point: Point, normalized: Point, sine_sign: int
) -> tuple[Polynomial, ...]:
    """Return 2(1+t²)² times the four signed closed membership margins.

    Write D=1+t², C=1-t², S=2t and R=C+sign(t)S. The center coordinate for
    normalized z is side*z+(1-2z)R/(2D). Thus DX=2D(px-side*zx)-(1-2zx)R,
    and similarly DY. The u and v projection numerators are C*DX+S*DY and
    -S*DX+C*DY. Subtracting each signed numerator from D² clears a strictly
    positive denominator. This derivation does not use producer polynomials.
    """
    if type(sine_sign) is not int or sine_sign not in (-1, 1):
        raise ValueError("sine sign must be exactly -1 or +1")
    if (
        type(side) is not Fraction
        or len(point) != 2
        or len(normalized) != 2
        or any(type(value) is not Fraction for value in (*point, *normalized))
        or any(not 0 <= value <= 1 for value in normalized)
    ):
        raise ValueError(
            "corner coordinates must be rational and normalized coordinates in [0,1]"
        )
    denominator = (Fraction(1), Fraction(0), Fraction(1))
    cosine = (Fraction(1), Fraction(0), Fraction(-1))
    sine = (Fraction(0), Fraction(2))
    radius_numerator = _add(cosine, _scale(sine, Fraction(sine_sign)))
    offsets = tuple(
        _add(
            _scale(denominator, 2 * (coordinate - side * unit)),
            _scale(radius_numerator, -(1 - 2 * unit)),
        )
        for coordinate, unit in zip(point, normalized, strict=True)
    )
    u = _add(_multiply(cosine, offsets[0]), _multiply(sine, offsets[1]))
    v = _add(
        _scale(_multiply(sine, offsets[0]), Fraction(-1)),
        _multiply(cosine, offsets[1]),
    )
    denominator_squared = _multiply(denominator, denominator)
    return tuple(
        _add(denominator_squared, _scale(projection, Fraction(sign)))
        for projection in (u, v)
        for sign in (-1, 1)
    )


def bernstein_coefficients(
    polynomial: Polynomial, left: Fraction, right: Fraction
) -> Polynomial:
    """Convert a rational quartic from powers of t to Bernstein on [left, right].

    First substitute t=left+(right-left)z. Then z**j has degree-n Bernstein
    coefficients binomial(i,j)/binomial(n,j), for i>=j. Nonnegative resulting
    coefficients prove nonnegativity on the entire closed interval.
    """
    if not 1 <= len(polynomial) <= 5 or any(type(c) is not Fraction for c in polynomial):
        raise ValueError("expected one to five exact rational polynomial coefficients")
    if type(left) is not Fraction or type(right) is not Fraction or left > right:
        raise ValueError("Bernstein interval requires ordered exact rational endpoints")
    degree = len(polynomial) - 1
    width = right - left
    powers = tuple(
        sum(
            (
                polynomial[k] * comb(k, j) * left ** (k - j) * width**j
                for k in range(j, degree + 1)
            ),
            Fraction(0),
        )
        for j in range(degree + 1)
    )
    return tuple(
        sum(
            (powers[j] * Fraction(comb(i, j), comb(degree, j)) for j in range(i + 1)),
            Fraction(0),
        )
        for i in range(degree + 1)
    )


def certifies_nonnegative(polynomial: Polynomial, left: Fraction, right: Fraction) -> bool:
    """Sufficient sign proof by bounded exact bisection; False means uncertified.

    A depth limit is never a disproof. Closed child intervals include their seam,
    and zero Bernstein coefficients are permitted, preserving exact contacts.
    """
    pending = [(left, right, 0)]
    while pending:
        low, high, depth = pending.pop()
        coefficients = bernstein_coefficients(polynomial, low, high)
        if min(coefficients) >= 0:
            continue
        if coefficients[0] < 0 or coefficients[-1] < 0 or depth == SIGN_DEPTH:
            return False
        middle = (low + high) / 2
        pending.extend(((middle, high, depth + 1), (low, middle, depth + 1)))
    return True


def validate_packet(packet: Any) -> Assignment:
    """Admit the frozen wire, retaining honest stopped prefixes without geometry."""
    if type(packet) is not dict or set(packet) != PACKET_KEYS:
        raise ValueError("proof packet has missing or unexpected keys")
    if type(packet["version"]) is not int or packet["version"] != 1:
        raise ValueError("unsupported proof packet version")
    if packet["kind"] != "fixed-side-near-axis-ten-cover-grid":
        raise ValueError("packet kind is not the fixed near-axis clause")
    if type(packet["side"]) is not str or packet["side"] != str(FIXED_SIDE):
        raise ValueError("packet changes the fixed side or its canonical spelling")
    if (
        type(packet["grid"]) is not list
        or packet["grid"] != [COLUMNS, ROWS]
        or any(type(value) is not int for value in packet["grid"])
    ):
        raise ValueError("packet changes the complete fixed grid")
    slabs = packet["half_angle_slabs"]
    if (
        type(slabs) is not list
        or len(slabs) != 2
        or any(type(slab) is not list for slab in slabs)
        or slabs != [[str(a), str(b)] for a, b in SLABS]
    ):
        # Equality with bounded canonical strings precedes any rational parsing.
        raise ValueError("packet changes the fixed canonical half-angle slabs")
    assignments = packet["assignments"]
    if type(assignments) is not list or any(type(row) is not list for row in assignments):
        raise ValueError("assignments must be JSON row arrays")
    labels = _labels(assignments, POINT_CAP)
    if labels != ASSIGNMENTS:
        raise ValueError("packet changes the frozen source labels")
    status, count = packet["status"], packet["inequalities_checked"]
    if type(status) is not str or status not in ("proved", "unresolved"):
        raise ValueError("invalid producer status")
    if type(count) is not int or not 0 <= count <= PRODUCER_INEQUALITIES:
        raise ValueError("invalid producer completed-prefix count")
    failures = packet["unresolved"]
    if type(failures) is not list or len(failures) > count:
        raise ValueError("invalid unresolved inventory")
    previous = -1
    for entry in failures:
        limits = (2, ROWS, COLUMNS, 2, 3, 4)
        if (
            type(entry) is not list
            or len(entry) != len(limits)
            or any(
                type(value) is not int or not 0 <= value < limit
                for value, limit in zip(entry, limits, strict=True)
            )
        ):
            raise ValueError("invalid unresolved inequality coordinates")
        ordinal = 0
        for value, limit in zip(entry, limits, strict=True):
            ordinal = ordinal * limit + value
        if not previous < ordinal < count:
            raise ValueError("unresolved entries must be unique ordered members of the prefix")
        previous = ordinal
    if status == "proved" and (count != PRODUCER_INEQUALITIES or failures):
        raise ValueError("positive producer status requires every inequality and no failures")
    return labels


def check_packet(packet: Any) -> dict[str, Any]:
    """Reconstruct fixed geometry only for a complete positive producer packet.

    The producer's counters are admission metadata, not a proof. A successful
    result requires this reader's full independent rectangle/slab calculation.
    A producer's nonzero process exit remains an external refusal even if its
    packet is positive; the experiment dispatcher owns that exit-code guard.
    """
    labels = validate_packet(packet)
    base: dict[str, Any] = {"scope": SCOPE, "h036_outcome": "unresolved"}
    if packet["status"] != "proved":
        return {
            **base,
            "decision": "unresolved",
            "reason": "producer did not report a completed positive proof",
        }
    side, points = target_input()
    result = check_closed_slabs(side, points, labels, SLABS)
    if (
        result.rectangles_checked != 36
        or result.corners_checked != 144
        or result.inequalities_checked != READER_INEQUALITIES
    ):
        raise ValueError("reader did not complete every required rectangle-corner inequality")
    return {
        **base,
        "decision": "proved" if result.proved else "unresolved",
        "reason": "all closed corner inequalities certified"
        if result.proved
        else "bounded Bernstein proof left uncertified inequalities; not a refutation",
        "side": str(FIXED_SIDE),
        "half_angle_slabs": [[str(a), str(b)] for a, b in SLABS],
        "rectangles_checked": result.rectangles_checked,
        "corners_checked": result.corners_checked,
        "inequalities_checked": result.inequalities_checked,
        "producer_inequalities_checked": packet["inequalities_checked"],
        "unresolved": [list(entry) for entry in result.uncertified],
    }


def _expired(_signal: int, _frame: Any) -> None:
    raise TimeoutError("near-axis replay reached its fixed ten-second wall cap")


def main(argv: Sequence[str] | None = None) -> int:
    """Emit proof receipt on stdout and process metadata on stderr, with no retry.

    The fixed alarm covers file admission, source binding and exact geometry.
    Receipt serialization follows the bounded computation. The caller retains
    both streams and the actual exit status; this tool does not publish files.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--target-control", action="store_true", required=True)
    args = parser.parse_args(argv)
    if not args.packet.is_absolute():
        parser.error("packet path must be absolute")
    started, cpu_started = time.monotonic(), time.process_time()
    previous = signal.signal(signal.SIGALRM, _expired)
    signal.alarm(WALL_CAP_SECONDS)
    try:
        result = check_packet(load_packet(args.packet, max_bytes=PACKET_BYTE_CAP))
        code = 0 if result["decision"] == "proved" else 1
    except TimeoutError as error:
        result = {
            "decision": "unresolved",
            "scope": SCOPE,
            "reason": str(error),
            "h036_outcome": "unresolved",
        }
        code = 1
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as error:
        result = {
            "decision": "refused",
            "scope": SCOPE,
            "reason": str(error),
            "h036_outcome": "unresolved",
        }
        code = 2
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)
    costs = {
        "input": str(args.packet),
        "exit_code": code,
        "wall_cap_seconds": WALL_CAP_SECONDS,
        "sign_depth": SIGN_DEPTH,
        "wall_seconds": time.monotonic() - started,
        "cpu_seconds": time.process_time() - cpu_started,
    }
    print(json.dumps(costs, sort_keys=True), file=sys.stderr)
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
