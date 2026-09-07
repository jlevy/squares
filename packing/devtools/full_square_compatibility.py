"""Exact fixed-square, fixed-frame H-124 falsifier; no-witness is unresolved.

The CLI needs a coordinator-enforced whole-process cap. Importing this module
does not load the retained scientific square or construct either target frame.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from cases.stromquist.restricted_orientation import (
    Cell,
    Point,
    Polygon,
    cell_witness,
    clip_polygon,
    event_cells_for_frame,
    point_sets,
    project,
    unproject,
)
from devtools.check_full_size_density_support_ceiling import load_packet
from devtools.diamond_cover_screen import (
    POINT_IDS,
    Witness,
    absolute,
    dot,
    point_packet,
    positive_cell_point,
    scalar_packet,
    separation_gap,
    signed_axes,
    square_corners,
)
from sqpack.field import FieldElement, NumberField

P10_IDS = tuple(f"p10-{index:02d}" for index in range(1, 11))
FIELD_PACKET = {"minimal_polynomial": ["1", "0", "-2"], "isolating_interval": ["1", "2"]}
SOURCE = (
    "packing/campaign/series/series-000-smoke-and-calibration/results/"
    "exp-122-diamond-conditional-cover-screen/packet.json"
)
PACKET_BYTE_CAP = 131072


@dataclass(frozen=True)
class FixedSquare:
    frame_id: str
    offset: Fraction
    frame: Point
    center: Point
    corners: Polygon


@dataclass(frozen=True)
class ScreenInput:
    side: FieldElement
    frame_id: str
    frame: Point
    fixed_square: FixedSquare
    p10: tuple[Point, ...]
    p9: tuple[Point, ...]
    source: str


@dataclass(frozen=True)
class ScreenResult:
    cells_checked: int
    canonical_cells_checked: int
    uncovered_cells_checked: int
    complete: bool
    witness: Witness | None


def clip_canonical_cell(side: FieldElement, frame: Point, cell: Cell) -> Cell | None:
    """Intersect the closure with closed canonical bounds, then redo strict feasibility."""
    cosine, sine = frame
    polygon = cell.polygon
    for plane in (
        (-cosine, sine, -side.field.one),
        (cosine, -sine, side / 2),
        (-sine, -cosine, side.field.zero),
        (sine, cosine, side.field.one),
    ):
        polygon = clip_polygon(polygon, plane)
    witness = cell_witness(polygon, cell.u, cell.v)
    return None if witness is None else Cell(cell.u, cell.v, polygon, witness, cell.covered)


def validate_square(side: FieldElement, square: FixedSquare, points: tuple[Point, ...]) -> None:
    """Guard exact unit geometry, closed container walls and strict marked-point avoidance."""
    values = (
        *square.frame,
        *square.center,
        *(x for p in (*square.corners, *points) for x in p),
    )
    if any(value.field is not side.field for value in values):
        raise ValueError("all square geometry must use one exact field")
    if dot(square.frame, square.frame) != 1:
        raise ValueError("square frame must have exact unit length")
    if square.corners != square_corners(square.center, square.frame):
        raise ValueError("square corners must be the declared ordered CCW unit corners")
    if any(value < 0 or value > side for corner in square.corners for value in corner):
        raise ValueError("square fails closed container containment")
    center = project(square.center, square.frame)
    for point in points:
        projected = project(point, square.frame)
        if all(absolute(projected[i] - center[i]) <= Fraction(1, 2) for i in (0, 1)):
            raise ValueError("square contains a closed marked point")


def scan_frame(
    side: FieldElement,
    frame: Point,
    fixed_square: FixedSquare,
    p10: tuple[Point, ...],
    p9: tuple[Point, ...],
) -> ScreenResult:
    """Early-stop on one strict pair witness; exhaustion covers only the fixed frame."""
    if side < 2 or len(p10) > 64 or len(p9) > 64:
        raise ValueError("canonical screen needs side at least two and bounded point sets")
    if any(value.field is not side.field for point in (*p10, frame) for value in point):
        raise ValueError("all event geometry must use one exact field")
    if dot(frame, frame) != 1:
        raise ValueError("event frame must have exact unit length")
    validate_square(side, fixed_square, p9)
    planes = []
    for axis in signed_axes(frame, fixed_square.corners):
        a, b = dot(axis, frame), dot(axis, (-frame[1], frame[0]))
        bound = (absolute(a) + absolute(b)) / 2 + max(
            dot(axis, point) for point in fixed_square.corners
        )
        planes.append((axis, (a, b, bound)))
    checked = canonical = uncovered = 0
    for original in event_cells_for_frame(side, frame, p10):
        checked += 1
        cell = clip_canonical_cell(side, frame, original)
        if cell is None:
            continue
        canonical += 1
        if cell.covered:
            continue
        uncovered += 1
        for axis, plane in planes:
            projected = positive_cell_point(cell, plane)
            if projected is None:
                continue
            center = unproject(projected, frame)
            candidate = FixedSquare(
                "candidate", Fraction(0), frame, center, square_corners(center, frame)
            )
            validate_square(side, candidate, p10)
            if not (1 <= center[0] <= side / 2 and 0 <= center[1] <= 1):
                raise ArithmeticError("strict mixture escaped the closed canonical domain")
            gap = separation_gap(center, frame, fixed_square.corners, axis)
            if gap <= 0:
                raise ArithmeticError("strict mixture lost the positive separation gap")
            return ScreenResult(
                checked,
                canonical,
                uncovered,
                complete=False,
                witness=Witness(center, axis, gap),
            )
    return ScreenResult(checked, canonical, uncovered, complete=True, witness=None)


def fixed_square_packet(square: FixedSquare) -> dict[str, object]:
    """The six fields copied from the retained witness, with unchanged corner order."""
    return {
        "frame_id": square.frame_id,
        "offset": str(square.offset),
        "cos": scalar_packet(square.frame[0]),
        "sin": scalar_packet(square.frame[1]),
        "center": point_packet(square.center),
        "corners": [point_packet(point) for point in square.corners],
    }


def run_screen(data: ScreenInput) -> dict[str, object]:
    """Generic typed entry; the independent target reader must bind all serialized inputs."""
    scalar_packet(data.side)
    if len(data.p10) != 10 or len(set(data.p10)) != 10:
        raise ValueError("all ten distinct points are required in source order")
    if len(data.p9) != 9 or len(set(data.p9)) != 9:
        raise ValueError("all nine distinct points are required in source order")
    if not data.source or not data.frame_id or not data.fixed_square.frame_id:
        raise ValueError("source and frame identifiers must be nonempty")
    if type(data.fixed_square.offset) is not Fraction:
        raise TypeError("fixed-square offset must be an exact Fraction")
    result = scan_frame(data.side, data.frame, data.fixed_square, data.p10, data.p9)
    witness = result.witness
    one, zero = data.side.field.one, data.side.field.zero
    return {
        "kind": "full-square-compatibility/v1",
        "status": "no_witness" if witness is None else "witness",
        "field": FIELD_PACKET,
        "source": data.source,
        "frame": {
            "id": data.frame_id,
            "cos": scalar_packet(data.frame[0]),
            "sin": scalar_packet(data.frame[1]),
        },
        "domain": {
            "q": scalar_packet(data.side),
            "x": [scalar_packet(one), scalar_packet(data.side / 2)],
            "y": [scalar_packet(zero), scalar_packet(one)],
        },
        "p10": [
            {"id": name, "xy": point_packet(point)}
            for name, point in zip(P10_IDS, data.p10, strict=True)
        ],
        "p9": [
            {"id": name, "xy": point_packet(point)}
            for name, point in zip(POINT_IDS, data.p9, strict=True)
        ],
        "fixed_square": fixed_square_packet(data.fixed_square),
        "summary": {
            "cells_checked": result.cells_checked,
            "canonical_cells_checked": result.canonical_cells_checked,
            "uncovered_cells_checked": result.uncovered_cells_checked,
            "complete": result.complete,
        },
        "witness": None
        if witness is None
        else {
            "center": point_packet(witness.center),
            "corners": [
                point_packet(point) for point in square_corners(witness.center, data.frame)
            ],
            "axis": point_packet(witness.axis),
            "gap": scalar_packet(witness.gap),
        },
    }


def _object(raw: object, keys: set[str]) -> dict[str, Any]:
    if not isinstance(raw, dict) or set(raw) != keys:
        raise ValueError("retained source has missing or unknown fields")
    return raw


def _rational(raw: object) -> Fraction:
    if not isinstance(raw, str) or len(raw) > 256:
        raise ValueError("retained coefficients require bounded rational strings")
    value = Fraction(raw)
    if str(value) != raw:
        raise ValueError("retained coefficients require canonical rational strings")
    return value


def _element(raw: object, field: NumberField) -> FieldElement:
    if not isinstance(raw, list) or len(raw) != 2:
        raise ValueError("retained field elements require two coefficients")
    return field.element([_rational(value) for value in raw])


def _point(raw: object, field: NumberField) -> Point:
    if not isinstance(raw, list) or len(raw) != 2:
        raise ValueError("retained points require two coordinates")
    return _element(raw[0], field), _element(raw[1], field)


def parse_fixed_source(raw: object, side: FieldElement, p9: tuple[Point, ...]) -> FixedSquare:
    """Admit the retained format without running its producer or trusting its geometry."""
    packet = _object(raw, {"kind", "status", "field", "frames", "witness"})
    if (
        packet["kind"] != "diamond-cover-screen/v1"
        or packet["status"] != "witness"
        or packet["field"] != FIELD_PACKET
    ):
        raise ValueError("retained source must be a complete exact diamond witness")
    witness = _object(
        packet["witness"],
        {
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
        },
    )
    if witness["q"] != scalar_packet(side) or witness["points"] != [
        {"id": name, "xy": point_packet(point)}
        for name, point in zip(POINT_IDS, p9, strict=True)
    ]:
        raise ValueError("retained side or nine-point inventory does not match the source")
    corners = witness["corners"]
    if (
        not isinstance(corners, list)
        or len(corners) != 4
        or not isinstance(witness["frame_id"], str)
    ):
        raise ValueError("retained square needs four ordered corners and a frame identifier")
    field = side.field
    square = FixedSquare(
        witness["frame_id"],
        _rational(witness["offset"]),
        (_element(witness["cos"], field), _element(witness["sin"], field)),
        _point(witness["center"], field),
        tuple(_point(point, field) for point in corners),
    )
    validate_square(side, square, p9)
    return square


def target_input() -> ScreenInput:
    """Scientific construction is reserved for a separately preregistered invocation."""
    field = NumberField((1, 0, -2), ("1", "2"))
    side = field.rational("1939/500")
    p10, twelve = point_sets(side)
    p9 = twelve[3:]
    raw = load_packet(Path(__file__).resolve().parents[2] / SOURCE, max_bytes=PACKET_BYTE_CAP)
    fixed = parse_fixed_source(raw, side, p9)
    offset = Fraction(-1, 500)
    denominator = 1 + offset * offset
    expected_frame = (
        field.rational((1 - offset * offset) / denominator),
        field.rational(2 * offset / denominator),
    )
    if (
        fixed.frame_id != "axis-negative"
        or fixed.offset != offset
        or fixed.frame != expected_frame
    ):
        raise ValueError("retained fixed square is not the frozen axis-negative frame")
    root_half = field.alpha / 2
    return ScreenInput(side, "exact45", (root_half, root_half), fixed, p10, p9, SOURCE)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-h124", action="store_true", required=True)
    parser.parse_args(argv)
    try:
        packet = run_screen(target_input())
    except (ValueError, TypeError, ArithmeticError, OSError) as exc:
        print(f"full-square compatibility screen refused: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(packet, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
