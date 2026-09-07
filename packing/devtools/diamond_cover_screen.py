"""Fixed-frame exact H-122 falsifier; finite no-witness output is never a cover proof."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction

from cases.stromquist.restricted_orientation import (
    Cell,
    Plane,
    Point,
    Polygon,
    event_cells_for_frame,
    project,
    unproject,
)
from sqpack.field import FieldElement, NumberField

POINT_IDS = ("B", "C0", "D", "E", "F", "G", "H", "I", "J")


@dataclass(frozen=True)
class FrameSpec:
    id: str
    offset: Fraction
    frame: Point


@dataclass(frozen=True)
class ScreenInput:
    side: FieldElement
    frames: tuple[FrameSpec, ...]
    diamond: Polygon
    points: tuple[Point, ...]


@dataclass(frozen=True)
class Witness:
    center: Point
    axis: Point
    gap: FieldElement


@dataclass(frozen=True)
class FrameResult:
    cells_checked: int
    uncovered_cells_checked: int
    complete: bool
    witness: Witness | None


def absolute(value: FieldElement) -> FieldElement:
    """Exact ordered-field absolute value; no numerical approximation."""
    return -value if value < 0 else value


def dot(left: Point, right: Point) -> FieldElement:
    return left[0] * right[0] + left[1] * right[1]


def signed_axes(frame: Point, diamond: Polygon) -> tuple[Point, ...]:
    """Two square normals and two nonparallel parallelogram normals, each signed."""
    if len(diamond) != 4:
        raise ValueError("diamond requires four vertices")
    edges = tuple(
        (diamond[(i + 1) % 4][0] - point[0], diamond[(i + 1) % 4][1] - point[1])
        for i, point in enumerate(diamond)
    )
    if edges[2] != (-edges[0][0], -edges[0][1]) or edges[3] != (-edges[1][0], -edges[1][1]):
        raise ValueError("diamond must be a cyclic parallelogram")
    if edges[0][0] * edges[1][1] - edges[0][1] * edges[1][0] == 0:
        raise ValueError("diamond must have positive area")
    axes = (
        frame,
        (-frame[1], frame[0]),
        (-edges[0][1], edges[0][0]),
        (-edges[1][1], edges[1][0]),
    )
    return tuple((sign * x, sign * y) for x, y in axes for sign in (1, -1))


def separation_gap(center: Point, frame: Point, diamond: Polygon, axis: Point) -> FieldElement:
    """Signed gap: minimum square projection minus maximum diamond projection."""
    perpendicular = (-frame[1], frame[0])
    radius = (absolute(dot(axis, frame)) + absolute(dot(axis, perpendicular))) / 2
    return dot(axis, center) - radius - max(dot(axis, point) for point in diamond)


def positive_cell_point(cell: Cell, plane: Plane) -> Point | None:
    """Move a positive closure maximum into every open event stratum exactly."""
    a, b, bound = plane

    def value(point: Point) -> FieldElement:
        return a * point[0] + b * point[1] - bound

    vertex = max(cell.polygon, key=value)
    high = value(vertex)
    if high <= 0:
        return None
    witness_value = value(cell.witness)
    if witness_value > 0:
        return cell.witness
    epsilon = high / (2 * (high + absolute(witness_value)))
    point = tuple((1 - epsilon) * vertex[i] + epsilon * cell.witness[i] for i in (0, 1))
    result = point[0], point[1]
    if not cell.u.contains(result[0]) or not cell.v.contains(result[1]) or value(result) <= 0:
        raise ArithmeticError("strict-cell mixture failed its exact invariant")
    return result


def scan_frame(
    side: FieldElement, frame: Point, diamond: Polygon, points: tuple[Point, ...]
) -> FrameResult:
    """Stop at the first exact witness, otherwise exhaust only this single fixed frame."""
    if any(
        value.field is not side.field for point in (*diamond, *points, frame) for value in point
    ):
        raise ValueError("all geometry must use one exact field")
    planes = []
    for axis in signed_axes(frame, diamond):
        a, b = dot(axis, frame), dot(axis, (-frame[1], frame[0]))
        bound = (absolute(a) + absolute(b)) / 2 + max(dot(axis, point) for point in diamond)
        planes.append((axis, (a, b, bound)))
    checked = uncovered = 0
    for cell in event_cells_for_frame(side, frame, points):
        checked += 1
        if cell.covered:
            continue
        uncovered += 1
        for axis, plane in planes:
            projected = positive_cell_point(cell, plane)
            if projected is None:
                continue
            center = unproject(projected, frame)
            gap = separation_gap(center, frame, diamond, axis)
            extent = (absolute(frame[0]) + absolute(frame[1])) / 2
            if gap <= 0 or not all(extent <= value <= side - extent for value in center):
                raise ArithmeticError("screen witness fails exact containment or separation")
            if any(
                absolute(project(point, frame)[0] - projected[0]) <= Fraction(1, 2)
                and absolute(project(point, frame)[1] - projected[1]) <= Fraction(1, 2)
                for point in points
            ):
                raise ArithmeticError("screen witness contains a marked point")
            return FrameResult(
                checked, uncovered, complete=False, witness=Witness(center, axis, gap)
            )
    return FrameResult(checked, uncovered, complete=True, witness=None)


def target_input() -> ScreenInput:
    """The scientific constructor is reserved for prospective target execution."""
    field = NumberField((1, 0, -2), ("1", "2"))
    q = field.rational("1939/500")
    width, bottom = q / 2 - 1, q - 3
    kappa = Fraction(49, 50)
    diamond = (
        (field.one, bottom),
        (1 + width / 2, bottom + kappa * width / 2),
        (1 + width, bottom),
        (1 + width / 2, bottom - kappa * width / 2),
    )
    points = (
        (q - 1, field.one),
        (q - Fraction(4, 5), q / 2),
        (q - 1, q - 1),
        (q / 2, q - Fraction(4, 5)),
        (field.one, q - 1),
        (field.rational("4/5"), q - 2),
        (field.rational("17/10"), field.rational("11/5")),
        (field.rational("11/5"), field.rational("11/5")),
        (field.rational("11/5"), field.rational("17/10")),
    )
    frames = []
    for family in ("axis", "near45"):
        for sign, label in ((-1, "negative"), (1, "positive")):
            offset = Fraction(sign, 500)
            denominator = 1 + offset * offset
            cosine = field.rational((1 - offset * offset) / denominator)
            sine = field.rational(2 * offset / denominator)
            if family == "near45":
                root_half = field.alpha / 2
                cosine, sine = root_half * (cosine - sine), root_half * (cosine + sine)
            frames.append(FrameSpec(f"{family}-{label}", offset, (cosine, sine)))
    return ScreenInput(q, tuple(frames), diamond, points)


def scalar_packet(value: FieldElement) -> list[str]:
    """Canonical coefficients in the fixed positive-square-root-of-two basis."""
    if (
        value.field.degree != 2
        or value.field.alpha * value.field.alpha != 2
        or value.field.alpha <= 0
    ):
        raise ValueError("packet field must be Q of the positive square root of two")
    return [str(coefficient) for coefficient in value.coeffs]


def point_packet(point: Point) -> list[list[str]]:
    return [scalar_packet(value) for value in point]


def square_corners(center: Point, frame: Point) -> Polygon:
    """CCW, beginning at center minus both half-axes."""
    cosine, sine = frame
    return tuple(
        (center[0] + (a * cosine - b * sine) / 2, center[1] + (a * sine + b * cosine) / 2)
        for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    )


def run_screen(data: ScreenInput) -> dict[str, object]:
    """Serialize only a complete finite screen or an independently checkable witness."""
    scalar_packet(data.side)
    if (
        data.side <= 0
        or not data.frames
        or len({frame.id for frame in data.frames}) != len(data.frames)
    ):
        raise ValueError("positive side and nonempty uniquely identified frames are required")
    if len(data.points) != len(POINT_IDS) or len(set(data.points)) != len(POINT_IDS):
        raise ValueError("all nine distinct points are required in source order")
    summaries: list[dict[str, object]] = []
    packet: dict[str, object] = {
        "kind": "diamond-cover-screen/v1",
        "status": "no_witness",
        "field": {"minimal_polynomial": ["1", "0", "-2"], "isolating_interval": ["1", "2"]},
        "frames": summaries,
        "witness": None,
    }
    for frame in data.frames:
        if not isinstance(frame.offset, Fraction):
            raise TypeError("frame offset must be an exact Fraction")
        result = scan_frame(data.side, frame.frame, data.diamond, data.points)
        summaries.append(
            {
                "id": frame.id,
                "cells_checked": result.cells_checked,
                "uncovered_cells_checked": result.uncovered_cells_checked,
                "complete": result.complete,
            }
        )
        if result.witness is None:
            continue
        witness = result.witness
        packet["status"] = "witness"
        packet["witness"] = {
            "frame_id": frame.id,
            "offset": str(frame.offset),
            "q": scalar_packet(data.side),
            "cos": scalar_packet(frame.frame[0]),
            "sin": scalar_packet(frame.frame[1]),
            "center": point_packet(witness.center),
            "corners": [
                point_packet(point) for point in square_corners(witness.center, frame.frame)
            ],
            "diamond": [point_packet(point) for point in data.diamond],
            "points": [
                {"id": name, "xy": point_packet(point)}
                for name, point in zip(POINT_IDS, data.points, strict=True)
            ],
            "axis": point_packet(witness.axis),
            "gap": scalar_packet(witness.gap),
        }
        break
    return packet


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-h122", action="store_true", required=True)
    parser.parse_args(argv)
    try:
        packet = run_screen(target_input())
    except (ValueError, TypeError, ArithmeticError) as exc:
        print(f"diamond-cover screen refused: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(packet, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
