"""Independent H-122 counterexample reader using exact corner and vertex projections.

The shared number-field kernel supplies arithmetic only. No producer or case geometry
is imported. Target reconstruction is lazy and forbidden in source-free controls.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from sqpack.field import FieldElement, NumberField

type Point = tuple[FieldElement, FieldElement]
type Polygon = tuple[Point, ...]

POINT_IDS = ("B", "C0", "D", "E", "F", "G", "H", "I", "J")
FRAME_IDS = ("axis-negative", "axis-positive", "near45-negative", "near45-positive")
MAX_PACKET_BYTES = 131072
FIELD_DESCRIPTOR = {
    "minimal_polynomial": ["1", "0", "-2"],
    "isolating_interval": ["1", "2"],
}


class GuardError(ValueError):
    """A malformed identity or insufficient receipt establishes no geometric result."""


@dataclass(frozen=True)
class Domain:
    """Reconstructed obstacle, marks and frame; the witness center remains free."""

    field: NumberField
    q: FieldElement
    frame_id: str
    offset: Fraction
    cosine: FieldElement
    sine: FieldElement
    diamond: Polygon
    points: tuple[tuple[str, Point], ...]


@dataclass(frozen=True)
class Witness:
    domain: Domain
    center: Point
    corners: Polygon
    axis: Point
    gap: FieldElement


def make_field() -> NumberField:
    """Use the positive sqrt(2) embedding, not a packet-selected number field."""
    return NumberField([1, 0, -2], (1, 2))


def coefficients(value: FieldElement) -> list[str]:
    """Serialize a+b*sqrt(2) in the fixed low-to-high power basis."""
    return [str(coefficient) for coefficient in value.coeffs]


def offset_frame(field: NumberField, chart: str, offset: Fraction) -> Point:
    """Generic exact offset frames; tests use no frozen scientific offset."""
    denominator = 1 + offset * offset
    if chart == "axis":
        return (
            field.rational((1 - offset * offset) / denominator),
            field.rational(2 * offset / denominator),
        )
    if chart == "near45":
        return (
            field.element([0, (1 - 2 * offset - offset * offset) / (2 * denominator)]),
            field.element([0, (1 + 2 * offset - offset * offset) / (2 * denominator)]),
        )
    raise GuardError("unknown frame chart")


def square_corners(center: Point, cosine: FieldElement, sine: FieldElement) -> Polygon:
    """Direct cyclic CCW corners from the center and its two oriented unit edges."""
    x, y = center
    return (
        (x - (cosine - sine) / 2, y - (sine + cosine) / 2),
        (x + (cosine + sine) / 2, y + (sine - cosine) / 2),
        (x + (cosine - sine) / 2, y + (sine + cosine) / 2),
        (x - (cosine + sine) / 2, y - (sine - cosine) / 2),
    )


def validate_unit_square(corners: Polygon) -> None:
    """Require four exact unit edges and counterclockwise right turns."""
    if len(corners) != 4:
        raise GuardError("unit square needs four cyclic corners")
    edges = tuple(
        (b[0] - a[0], b[1] - a[1])
        for a, b in zip(corners, (*corners[1:], corners[0]), strict=True)
    )
    for edge, following in zip(edges, (*edges[1:], edges[0]), strict=True):
        if edge[0] ** 2 + edge[1] ** 2 != 1 or following != (-edge[1], edge[0]):
            raise GuardError("corners are not a counterclockwise exact unit square")


def edge_determinants(corners: Polygon, point: Point) -> tuple[FieldElement, ...]:
    """Closed square membership requires every one of these four signs to be >=0."""
    if len(corners) != 4:
        raise GuardError("edge check needs four cyclic corners")
    return tuple(
        (end[0] - start[0]) * (point[1] - start[1])
        - (end[1] - start[1]) * (point[0] - start[0])
        for start, end in zip(corners, (*corners[1:], corners[0]), strict=True)
    )


def _validate_convex_quad(polygon: Polygon) -> None:
    if len(polygon) != 4:
        raise GuardError("obstacle needs four vertices")
    turn = edge_determinants(polygon, polygon[2])[0].sign()
    if turn == 0:
        raise GuardError("obstacle is degenerate")
    for point in polygon:
        if any(value.sign() not in (0, turn) for value in edge_determinants(polygon, point)):
            raise GuardError("obstacle is not cyclic and convex")


def projection_gap(first: Polygon, second: Polygon, axis: Point) -> FieldElement:
    """Signed unnormalized interval separation; zero is contact, not disjointness."""
    if not first or not second or all(value == 0 for value in axis):
        raise GuardError("nonempty polygons and a nonzero axis are required")
    first_values = tuple(x * axis[0] + y * axis[1] for x, y in first)
    second_values = tuple(x * axis[0] + y * axis[1] for x, y in second)
    return max(min(first_values) - max(second_values), min(second_values) - max(first_values))


def strict_separation(first: Polygon, second: Polygon) -> tuple[Point, FieldElement] | None:
    """Find a strictly separating edge normal of either convex polygon."""
    for polygon in (first, second):
        for start, end in zip(polygon, (*polygon[1:], polygon[0]), strict=True):
            axis = (start[1] - end[1], end[0] - start[0])
            if all(value == 0 for value in axis):
                raise GuardError("polygon has a zero-length edge")
            gap = projection_gap(first, second, axis)
            if gap > 0:
                return axis, gap
    return None


def reconstruct_target(field: NumberField, frame_id: str) -> Domain:
    """Scientific invocation only: transcribe H-122 without producer or case imports."""
    if frame_id not in FRAME_IDS:
        raise GuardError("unknown frozen frame identity")
    offset = Fraction(-1 if frame_id.endswith("negative") else 1, 500)
    cosine, sine = offset_frame(field, frame_id.split("-", maxsplit=1)[0], offset)
    q = field.rational(Fraction(1939, 500))
    width, baseline, slope = q / 2 - 1, q - 3, Fraction(49, 50)
    diamond = (
        (field.one, baseline),
        (1 + width / 2, baseline + slope * width / 2),
        (1 + width, baseline),
        (1 + width / 2, baseline - slope * width / 2),
    )
    rational = field.rational
    points = (
        ("B", (q - 1, field.one)),
        ("C0", (q - Fraction(4, 5), q / 2)),
        ("D", (q - 1, q - 1)),
        ("E", (q / 2, q - Fraction(4, 5))),
        ("F", (field.one, q - 1)),
        ("G", (rational(Fraction(4, 5)), q - 2)),
        ("H", (rational(Fraction(17, 10)), rational(Fraction(11, 5)))),
        ("I", (rational(Fraction(11, 5)), rational(Fraction(11, 5)))),
        ("J", (rational(Fraction(11, 5)), rational(Fraction(17, 10)))),
    )
    return Domain(field, q, frame_id, offset, cosine, sine, diamond, points)


def _rational(value: object) -> Fraction:
    if not isinstance(value, str) or len(value) > 512:
        raise GuardError("rational coefficients must be bounded canonical strings")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise GuardError(f"invalid rational coefficient: {exc}") from exc
    if str(result) != value:
        raise GuardError("noncanonical rational coefficient")
    return result


def _element(raw: object, field: NumberField) -> FieldElement:
    if not isinstance(raw, list) or len(raw) != 2:
        raise GuardError("field element must have exactly two rational coefficients")
    return field.element([_rational(value) for value in raw])


def _point(raw: object, field: NumberField) -> Point:
    if not isinstance(raw, list) or len(raw) != 2:
        raise GuardError("point must have exactly two field elements")
    return _element(raw[0], field), _element(raw[1], field)


def _polygon(raw: object, field: NumberField) -> Polygon:
    if not isinstance(raw, list) or len(raw) != 4:
        raise GuardError("polygon must have exactly four vertices")
    return tuple(_point(point, field) for point in raw)


def _admit(raw: object) -> dict[str, Any]:
    if not isinstance(raw, dict) or set(raw) != {
        "kind",
        "status",
        "field",
        "frames",
        "witness",
    }:
        raise GuardError("screen packet must have exactly the v1 fields")
    if raw["kind"] != "diamond-cover-screen/v1" or raw["field"] != FIELD_DESCRIPTOR:
        raise GuardError("wrong screen kind or positive-sqrt(2) field identity")
    if raw["status"] == "no_witness":
        raise GuardError("no witness to verify; a finite screen cannot accept H-122")
    if raw["status"] != "witness" or not isinstance(raw["frames"], list):
        raise GuardError("screen is not a witness receipt")
    witness = raw["witness"]
    keys = {
        "frame_id",
        "offset",
        "q",
        "cos",
        "sin",
        "center",
        "corners",
        "diamond",
        "points",
        "axis",
        "gap",
    }
    if not isinstance(witness, dict) or set(witness) != keys:
        raise GuardError("incomplete or unknown witness fields")
    return witness


def _parse(raw: dict[str, Any], field: NumberField) -> Witness:
    frame_id = raw["frame_id"]
    if frame_id not in FRAME_IDS:
        raise GuardError("unknown frame identity")
    points = raw["points"]
    if not isinstance(points, list) or len(points) != len(POINT_IDS):
        raise GuardError("witness needs the full nine-point inventory")
    marks: list[tuple[str, Point]] = []
    for name, entry in zip(POINT_IDS, points, strict=True):
        if not isinstance(entry, dict) or set(entry) != {"id", "xy"} or entry["id"] != name:
            raise GuardError("marked-point identity or source order mismatch")
        marks.append((name, _point(entry["xy"], field)))
    domain = Domain(
        field,
        _element(raw["q"], field),
        frame_id,
        _rational(raw["offset"]),
        _element(raw["cos"], field),
        _element(raw["sin"], field),
        _polygon(raw["diamond"], field),
        tuple(marks),
    )
    return Witness(
        domain,
        _point(raw["center"], field),
        _polygon(raw["corners"], field),
        _point(raw["axis"], field),
        _element(raw["gap"], field),
    )


def _verify(witness: Witness, expected: Domain) -> dict[str, Any]:
    if witness.domain != expected:
        raise GuardError("witness differs from independent exact domain reconstruction")
    if not 0 < abs(expected.offset) < Fraction(1, 480):
        raise GuardError("failed sufficient angle guard; actual angular domain unresolved")
    chart = expected.frame_id.split("-")[0]
    if (
        (expected.cosine, expected.sine) != offset_frame(expected.field, chart, expected.offset)
        or expected.cosine**2 + expected.sine**2 != 1
        or expected.q <= 0
    ):
        raise GuardError("exact frame or container guard failed")
    if witness.corners != square_corners(witness.center, expected.cosine, expected.sine):
        raise GuardError("corners do not match center and exact oriented frame")
    validate_unit_square(witness.corners)
    _validate_convex_quad(expected.diamond)
    slacks = tuple((x, expected.q - x, y, expected.q - y) for x, y in witness.corners)
    contained = all(value >= 0 for row in slacks for value in row)
    checks = tuple(
        (name, edge_determinants(witness.corners, point)) for name, point in expected.points
    )
    hits = [name for name, values in checks if all(value >= 0 for value in values)]
    gap = projection_gap(witness.corners, expected.diamond, witness.axis)
    if gap != witness.gap:
        raise GuardError("supplied gap disagrees with exact vertex projections")
    separation = strict_separation(witness.corners, expected.diamond)
    geometrically_valid = contained and not hits and separation is not None
    if geometrically_valid and gap <= 0:
        raise GuardError("supplied axis is not strictly separating; witness receipt refused")
    return {
        "kind": "diamond-cover-witness-check/v1",
        "status": "verified_counterexample" if geometrically_valid else "not_a_counterexample",
        "guard_status": "passed",
        "complete": True,
        "frame_id": expected.frame_id,
        "offset": str(expected.offset),
        "q": coefficients(expected.q),
        "actual_angle_membership": True,
        "offset_angle_upper_bound": str(2 * abs(expected.offset)),
        "angle_argument": "abs(2*atan(offset))<2*abs(offset)<1/240<pi/720 (pi>3)",
        "unit_square": True,
        "contained": contained,
        "strictly_disjoint": separation is not None,
        "contained_points": hits,
        "corners_checked": len(witness.corners),
        "points_checked": len(checks),
        "edge_determinants_checked": sum(len(values) for _, values in checks),
        "corner_wall_slacks": [[coefficients(value) for value in row] for row in slacks],
        "point_checks": [
            {
                "id": name,
                "determinants": [coefficients(value) for value in values],
                "strictly_outside": any(value < 0 for value in values),
            }
            for name, values in checks
        ],
        "independent_separating_axis": None
        if separation is None
        else [coefficients(value) for value in separation[0]],
        "independent_separating_gap": None
        if separation is None
        else coefficients(separation[1]),
        "claimed_axis_gap": coefficients(gap),
        "screen_coverage_used": False,
        "unresolved": [],
        "scope": "counterexample check only; no covering proof or H-036 conclusion",
    }


def check_packet(raw: object, *, expected: Domain) -> dict[str, Any]:
    """Generic identity-bound control seam; never reconstructs scientific geometry."""
    return _verify(_parse(_admit(raw), expected.field), expected)


def check_target_packet(raw: object) -> dict[str, Any]:
    """Reject foreign receipts before lazily reconstructing the fixed scientific domain."""
    admitted = _admit(raw)
    field = make_field()
    witness = _parse(admitted, field)
    frame_id = witness.domain.frame_id
    expected_offset = Fraction(-1 if frame_id.endswith("negative") else 1, 500)
    if witness.domain.offset != expected_offset or witness.domain.q != Fraction(1939, 500):
        raise GuardError("foreign frozen frame offset or container identity")
    return _verify(witness, reconstruct_target(field, frame_id))


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GuardError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main(argv: list[str] | None = None) -> int:
    """Print JSON; an invalid geometric witness is distinct from a refused receipt."""
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        with args.input.open("rb") as stream:
            payload = stream.read(MAX_PACKET_BYTES + 1)
        if len(payload) > MAX_PACKET_BYTES:
            raise GuardError("witness packet exceeds the bounded input size")
        raw = json.loads(payload.decode("utf-8"), object_pairs_hook=_unique_object)
        result = check_target_packet(raw)
    except (OSError, ValueError, RecursionError) as exc:
        result = {
            "kind": "diamond-cover-witness-check/v1",
            "status": "unresolved",
            "guard_status": "failed",
            "complete": False,
            "unresolved": [str(exc)],
            "scope": "no conclusion about H-122 or H-036",
        }
        print(json.dumps(result, sort_keys=True, indent=2))
        print(f"witness reader refused: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
