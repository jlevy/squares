"""Digest-bound SVG source cells and canonical rigid-pose receipts.

The fitter and verifier deliberately do not share geometric predicates.  The fitter
constructs one compatible unit-square witness and a conservative local pose enclosure;
the verifier replays the retained receipt independently.  This module does not retain
or write source SVG bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import logging
import math
import re
import xml.etree.ElementTree as ET
from collections.abc import Callable, Mapping, Sequence
from contextlib import closing
from dataclasses import dataclass
from decimal import Decimal
from typing import BinaryIO, cast
from urllib.request import urlopen

_NUMBER = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")
_TRANSFORM = re.compile(r"([A-Za-z]+)\s*\(([^)]*)\)")
_SOURCE_MODELS = ("declared:svg-literal", "nearest-6", "truncate-6")
_FIT_TOLERANCE = Decimal("2e-12")
_TRANSFORM_PAD = Decimal("2e-15")
_OUTPUT_QUANTUM = Decimal("1e-14")
MODEL_ORDER = ("declared:svg-literal", "nearest-6", "truncate-6")
RESULT_SCHEMA = "UnitSquarePrecisionResult/v1"
RESULT_PATH = (
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-047-h-053-unitsquare-rigid-pose-serialization.json"
)


class PrecisionBridgeError(ValueError):
    """Bounded refusal at a provenance, parsing, fitting, or verification boundary."""


class TargetMeasurementGatedError(PrecisionBridgeError):
    """The target driver was reached without explicit coordinator W6 authorization."""


@dataclass(frozen=True, order=True)
class Interval:
    """Closed decimal interval."""

    lower: Decimal
    upper: Decimal

    def __post_init__(self) -> None:
        if not self.lower.is_finite() or not self.upper.is_finite():
            raise PrecisionBridgeError("interval endpoints must be finite")
        if self.lower > self.upper:
            raise PrecisionBridgeError("interval lower endpoint exceeds upper endpoint")

    @property
    def midpoint(self) -> Decimal:
        return (self.lower + self.upper) / 2

    @property
    def width(self) -> Decimal:
        return self.upper - self.lower


@dataclass(frozen=True)
class PointCell:
    """One source vertex as a Cartesian product of two closed intervals."""

    x: Interval
    y: Interval


@dataclass(frozen=True)
class SourceSquare:
    """Four source cells in published vertex order."""

    square_id: str
    vertices: tuple[PointCell, PointCell, PointCell, PointCell]


@dataclass(frozen=True)
class PoseFit:
    """A compatible unit-square witness and conservative local pose enclosure."""

    square_id: str
    center_x: Decimal
    center_y: Decimal
    theta: Decimal
    center_x_enclosure: Interval
    center_y_enclosure: Interval
    theta_enclosure: Interval
    source_cells: tuple[PointCell, PointCell, PointCell, PointCell]
    maximum_corner_residual: Decimal


@dataclass(frozen=True)
class TargetPair:
    """Frozen provenance inputs for one paired target."""

    n: int
    child_path: str
    child_sha256: str
    parent_url: str
    parent_sha256: str


@dataclass(frozen=True)
class ParentEvaluation:
    """Sanitized parent-only outcome for one frozen model."""

    model: str
    compatible: bool
    valid: bool
    receipt: Mapping[str, object] | None


@dataclass(frozen=True)
class SealedParent:
    """Immutable parent-only selection made before child access."""

    n: int
    model: str
    receipt_sha256: str


TARGET_PAIRS = (
    TargetPair(
        68,
        "resources/web/known-best-packings/unitsquare/n068.svg",
        "d7385d6ce1b5a959d06893c94f3c0355f17175bd68608db6f012ca309854ed66",
        "https://kingbird.myphotos.cc/packing/square-68.svg",
        "558fbdddfeb0b2f8752b88e172d2776544beb4d2a7122189ef77c1e1c5ebdc6d",
    ),
    TargetPair(
        69,
        "resources/web/known-best-packings/unitsquare/n069.svg",
        "b32aa37d37b07248ac92e683bbfd9be7ca6eb6aafa35a35e46a2484467afee41",
        "https://kingbird.myphotos.cc/packing/square-69.svg",
        "0333814c7b43ddc7db549a54771de117f8a6b7b3db0f89c12fe035115546fd08",
    ),
)


@dataclass(frozen=True)
class SvgScene:
    """Normalized source-cell scene, with no retained source bytes."""

    model: str
    side: Decimal
    squares: tuple[SourceSquare, ...]

    def receipt(self, fits: Sequence[PoseFit]) -> dict[str, object]:
        """Build a stable, verifier-facing receipt from one fit per parsed square."""
        by_id = {fit.square_id: fit for fit in fits}
        expected = {square.square_id for square in self.squares}
        if set(by_id) != expected or len(fits) != len(by_id):
            raise PrecisionBridgeError("receipt requires exactly one fit per square")
        ordered = tuple(by_id[square_id] for square_id in sorted(by_id))
        square_rows = [_fit_row(fit, self.side) for fit in ordered]
        pair_rows = []
        for first, second in itertools.combinations(ordered, 2):
            pair_rows.append(
                {
                    "first": first.square_id,
                    "second": second.square_id,
                    "signed_separation": _decimal_text(_pair_separation(first, second)),
                }
            )
        return {
            "schema": "UnitSquareRigidPoseReceipt/v1",
            "source_model": self.model,
            "container_side": _decimal_text(self.side),
            "squares": square_rows,
            "pairs": pair_rows,
        }


@dataclass(frozen=True)
class _Affine:
    a: Decimal = Decimal(1)
    b: Decimal = Decimal(0)
    c: Decimal = Decimal(0)
    d: Decimal = Decimal(1)
    e: Decimal = Decimal(0)
    f: Decimal = Decimal(0)
    inexact: bool = False

    def compose(self, local: _Affine) -> _Affine:
        """Return ``self * local``, the SVG current-transform-matrix update."""
        return _Affine(
            self.a * local.a + self.c * local.b,
            self.b * local.a + self.d * local.b,
            self.a * local.c + self.c * local.d,
            self.b * local.c + self.d * local.d,
            self.a * local.e + self.c * local.f + self.e,
            self.b * local.e + self.d * local.f + self.f,
            self.inexact or local.inexact,
        )

    def point_cell(self, point: PointCell) -> PointCell:
        return PointCell(
            _linear_interval(
                (self.a, point.x), (self.c, point.y), self.e, inexact=self.inexact
            ),
            _linear_interval(
                (self.b, point.x), (self.d, point.y), self.f, inexact=self.inexact
            ),
        )


def source_cell(literal: str, model: str) -> Interval:
    """Interpret one published decimal under a predeclared source model."""
    if model not in _SOURCE_MODELS:
        raise PrecisionBridgeError(f"unsupported source model: {model}")
    try:
        value = Decimal(literal)
    except Exception as error:
        raise PrecisionBridgeError("source coordinate is not a decimal literal") from error
    if not value.is_finite():
        raise PrecisionBridgeError("source coordinate must be finite")
    if model == "declared:svg-literal":
        return Interval(value, value)
    if value.as_tuple().exponent != -6:
        raise PrecisionBridgeError(f"{model} requires exactly six fractional decimal places")
    quantum = Decimal("0.000001")
    if model == "nearest-6":
        half = quantum / 2
        return Interval(value - half, value + half)
    if value >= 0:
        return Interval(value, value + quantum)
    return Interval(value - quantum, value)


def verify_parent_bytes[T](
    payload: bytes,
    *,
    expected_sha256: str,
    consume: Callable[[bytes], T],
) -> T:
    """Pass bytes to a parser only after their exact expected digest is established."""
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise PrecisionBridgeError("expected SHA-256 must be 64 lowercase hex digits")
    actual = hashlib.sha256(payload).hexdigest()
    if actual != expected_sha256:
        raise PrecisionBridgeError(
            f"source digest mismatch: expected {expected_sha256}, observed {actual}"
        )
    return consume(payload)


def _open_parent(url: str) -> BinaryIO:
    return cast(BinaryIO, urlopen(url, timeout=30))


def consume_verified_parent[T](
    url: str,
    *,
    expected_sha256: str,
    consume: Callable[[bytes], T],
    opener: Callable[[str], BinaryIO] = _open_parent,
) -> T:
    """Retrieve, hash, consume, and close a parent source without retaining raw bytes."""
    with closing(opener(url)) as response:
        payload = response.read()
        result = verify_parent_bytes(
            payload,
            expected_sha256=expected_sha256,
            consume=consume,
        )
    if isinstance(result, (bytes, bytearray, memoryview)):
        raise PrecisionBridgeError("parent consumer may not return raw source bytes")
    return result


def seal_first_parent_model(
    n: int, evaluations: Sequence[ParentEvaluation]
) -> SealedParent | None:
    """Select the first qualifying parent-only model, without a child input channel."""
    if tuple(evaluation.model for evaluation in evaluations) != MODEL_ORDER:
        raise PrecisionBridgeError("parent evaluations are not in the frozen model order")
    for evaluation in evaluations:
        if not evaluation.compatible or not evaluation.valid:
            continue
        if evaluation.receipt is None:
            raise PrecisionBridgeError("qualifying parent evaluation lacks a receipt")
        digest = hashlib.sha256(canonical_bytes(evaluation.receipt)).hexdigest()
        return SealedParent(n, evaluation.model, digest)
    return None


def prepare_target_run(record_path: str, *, authorized: bool = False) -> dict[str, object]:
    """Return the frozen target plan only after the coordinator opens W6."""
    if record_path != RESULT_PATH:
        raise PrecisionBridgeError(f"result path must be exactly {RESULT_PATH}")
    if not authorized:
        raise TargetMeasurementGatedError(
            "W6 target measurement is gated; no child read or parent retrieval was attempted"
        )
    return {
        "schema": RESULT_SCHEMA,
        "record_path": RESULT_PATH,
        "model_order": list(MODEL_ORDER),
        "pairs": [
            {
                "n": pair.n,
                "child_path": pair.child_path,
                "child_sha256": pair.child_sha256,
                "parent_url": pair.parent_url,
                "parent_sha256": pair.parent_sha256,
            }
            for pair in TARGET_PAIRS
        ],
        "selection": "first-compatible-valid-parent-model-no-fallthrough",
        "retention": "raw-parent-bytes-forbidden",
    }


def parse_svg_scene(payload: bytes, *, model: str, side: Decimal) -> SvgScene:
    """Parse polygon source cells and normalize the SVG container to ``[0, side]^2``."""
    if model not in _SOURCE_MODELS:
        raise PrecisionBridgeError(f"unsupported source model: {model}")
    if not side.is_finite() or side <= 0:
        raise PrecisionBridgeError("normalized container side must be positive and finite")
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as error:
        raise PrecisionBridgeError("source is not well-formed XML") from error

    container = _find_container(root)
    if container is None:
        raise PrecisionBridgeError("SVG has no unambiguous axis-aligned container")
    x0, y0, width, height = container
    if width <= 0 or height <= 0:
        raise PrecisionBridgeError("SVG container dimensions must be positive")

    squares: list[SourceSquare] = []
    identifiers: set[str] = set()

    def visit(element: ET.Element, parent: _Affine) -> None:
        local = _parse_transform(element.attrib.get("transform", ""))
        current = parent.compose(local)
        if _local_name(element.tag) == "polygon":
            square_id = element.attrib.get("id")
            if not square_id:
                raise PrecisionBridgeError("every square polygon requires a stable id")
            if square_id in identifiers:
                raise PrecisionBridgeError(f"duplicate square id: {square_id}")
            identifiers.add(square_id)
            literals = _NUMBER.findall(element.attrib.get("points", ""))
            if len(literals) != 8:
                raise PrecisionBridgeError(
                    f"square {square_id} must publish exactly four coordinate pairs"
                )
            cells = []
            for index in range(0, 8, 2):
                local_point = PointCell(
                    source_cell(literals[index], model),
                    source_cell(literals[index + 1], model),
                )
                cells.append(
                    _normalize_point(
                        current.point_cell(local_point), (x0, y0, width, height), side
                    )
                )
            squares.append(SourceSquare(square_id, tuple(cells)))  # type: ignore[arg-type]
        for child in element:
            visit(child, current)

    visit(root, _Affine())
    if not squares:
        raise PrecisionBridgeError("SVG contains no square polygons")
    return SvgScene(model, side, tuple(sorted(squares, key=lambda square: square.square_id)))


def fit_rigid_pose(square: SourceSquare) -> PoseFit:
    """Fit and enclose one compatible unit-square pose from four source cells."""
    if len(square.vertices) != 4:
        raise PrecisionBridgeError("rigid-pose fitting requires exactly four source cells")
    points = [
        (float(vertex.x.midpoint), float(vertex.y.midpoint)) for vertex in square.vertices
    ]
    center_x_float = math.fsum(point[0] for point in points) / 4
    center_y_float = math.fsum(point[1] for point in points) / 4
    angle_candidates = []
    for index, point in enumerate(points):
        following = points[(index + 1) % 4]
        dx = following[0] - point[0]
        dy = following[1] - point[1]
        if math.hypot(dx, dy) > 0.5:
            angle_candidates.append(_canonical_angle(math.atan2(dy, dx)))
    if not angle_candidates:
        raise PrecisionBridgeError(f"square {square.square_id} has no usable edge")
    theta_float = sorted(angle_candidates)[len(angle_candidates) // 2]
    predicted = _corners_float(center_x_float, center_y_float, theta_float)

    best_permutation: tuple[int, ...] | None = None
    best_residual = math.inf
    best_violation = math.inf
    for permutation in itertools.permutations(range(4)):
        residual = 0.0
        violation = 0.0
        for corner, cell_index in zip(predicted, permutation, strict=True):
            cell = square.vertices[cell_index]
            residual = max(
                residual,
                math.hypot(
                    corner[0] - float(cell.x.midpoint),
                    corner[1] - float(cell.y.midpoint),
                ),
            )
            violation = max(violation, _cell_violation(corner, cell))
        if (violation, residual, permutation) < (
            best_violation,
            best_residual,
            best_permutation or permutation,
        ):
            best_permutation = permutation
            best_residual = residual
            best_violation = violation
    if best_permutation is None or best_violation > float(_FIT_TOLERANCE):
        raise PrecisionBridgeError(f"square {square.square_id} has no compatible rigid pose")

    center_x = _quantized_float(center_x_float)
    center_y = _quantized_float(center_y_float)
    theta = _quantized_float(theta_float)
    ordered_cells = tuple(square.vertices[index] for index in best_permutation)
    cell_radius = max(
        (max(cell.x.width, cell.y.width) for cell in square.vertices),
        default=Decimal(0),
    )
    center_radius = cell_radius + Decimal("3e-12")
    theta_radius = cell_radius * 4 + Decimal("6e-12")
    return PoseFit(
        square.square_id,
        center_x,
        center_y,
        theta,
        Interval(center_x - center_radius, center_x + center_radius),
        Interval(center_y - center_radius, center_y + center_radius),
        Interval(theta - theta_radius, theta + theta_radius),
        ordered_cells,  # type: ignore[arg-type]
        _quantized_float(best_residual),
    )


def canonical_bytes(document: Mapping[str, object]) -> bytes:
    """Serialize a receipt deterministically without binary-float conversion."""
    normalized = _json_value(document)
    return (
        json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode("ascii")


def verify_receipt(document: Mapping[str, object]) -> list[str]:
    """Independently replay a rigid-pose receipt; return bounded public errors."""
    errors: list[str] = []
    try:
        if document.get("schema") != "UnitSquareRigidPoseReceipt/v1":
            return ["unsupported receipt schema"]
        side = _read_decimal(document.get("container_side"), "container_side")
        rows = document.get("squares")
        if not isinstance(rows, list) or not rows:
            return ["squares must be a nonempty list"]
        verified: list[tuple[str, float, float, float]] = []
        identifiers: set[str] = set()
        for row_index, row in enumerate(rows):
            if not isinstance(row, dict):
                errors.append(f"square[{row_index}] is not an object")
                continue
            square_id = row.get("id")
            if not isinstance(square_id, str) or not square_id or square_id in identifiers:
                errors.append(f"square[{row_index}] has an invalid or duplicate id")
                continue
            identifiers.add(square_id)
            try:
                pose = row["pose"]
                cells = row["source_cells"]
                pose, cells = _require_pose_structure(pose, cells)
                cx = _read_decimal(pose.get("center_x"), "center_x")
                cy = _read_decimal(pose.get("center_y"), "center_y")
                theta = _read_decimal(pose.get("theta"), "theta")
                enclosure = pose.get("enclosure")
                enclosure = _require_enclosure(enclosure)
                for name, value in (("center_x", cx), ("center_y", cy), ("theta", theta)):
                    bounds = enclosure.get(name)
                    interval = _read_interval(bounds, f"{name} enclosure")
                    if not interval.lower <= value <= interval.upper:
                        errors.append(f"{square_id}: witness lies outside {name} enclosure")
                decoded_cells = tuple(_read_point_cell(cell, square_id) for cell in cells)
                corners = _verifier_corners(float(cx), float(cy), float(theta))
                for corner_index, (corner, cell) in enumerate(
                    zip(corners, decoded_cells, strict=True)
                ):
                    if _cell_violation(corner, cell) > float(_FIT_TOLERANCE):
                        errors.append(
                            f"{square_id}: corner {corner_index} lies outside its source cell"
                        )
                    if not (
                        -float(_FIT_TOLERANCE) <= corner[0] <= float(side + _FIT_TOLERANCE)
                    ):
                        errors.append(f"{square_id}: corner {corner_index} crosses an x wall")
                    if not (
                        -float(_FIT_TOLERANCE) <= corner[1] <= float(side + _FIT_TOLERANCE)
                    ):
                        errors.append(f"{square_id}: corner {corner_index} crosses a y wall")
                for index in range(4):
                    following = (index + 1) % 4
                    dx = corners[following][0] - corners[index][0]
                    dy = corners[following][1] - corners[index][1]
                    if abs(math.hypot(dx, dy) - 1.0) > 5e-13:
                        errors.append(f"{square_id}: reconstructed edge is not unit length")
                verified.append((square_id, float(cx), float(cy), float(theta)))
            except (KeyError, PrecisionBridgeError, TypeError, ValueError) as error:
                errors.append(f"{square_id}: malformed square receipt ({error})")

        for first, second in itertools.combinations(verified, 2):
            if _verifier_pair_separation(first, second) < -float(_FIT_TOLERANCE):
                errors.append(f"{first[0]}/{second[0]}: reconstructed squares overlap")
    except (PrecisionBridgeError, TypeError, ValueError) as error:
        errors.append(f"malformed receipt ({error})")
    return errors


def _find_container(root: ET.Element) -> tuple[Decimal, Decimal, Decimal, Decimal] | None:
    view_box = root.attrib.get("viewBox")
    if view_box:
        values = _NUMBER.findall(view_box)
        if len(values) == 4:
            return tuple(Decimal(value) for value in values)  # type: ignore[return-value]
    containers = [
        element
        for element in root.iter()
        if _local_name(element.tag) == "rect" and element.attrib.get("id") == "container"
    ]
    if len(containers) != 1 or containers[0].attrib.get("transform"):
        return None
    rectangle = containers[0]
    try:
        return (
            Decimal(rectangle.attrib.get("x", "0")),
            Decimal(rectangle.attrib.get("y", "0")),
            Decimal(rectangle.attrib["width"]),
            Decimal(rectangle.attrib["height"]),
        )
    except KeyError, ValueError:
        return None


def _parse_transform(text: str) -> _Affine:
    if not text.strip():
        return _Affine()
    matches = list(_TRANSFORM.finditer(text))
    if not matches or "".join(match.group(0) for match in matches).replace(" ", "") != re.sub(
        r"\s+", "", text
    ):
        raise PrecisionBridgeError("malformed SVG transform list")
    result = _Affine()
    for match in matches:
        name = match.group(1)
        values = [Decimal(value) for value in _NUMBER.findall(match.group(2))]
        if name == "matrix" and len(values) == 6:
            operation = _Affine(
                a=values[0],
                b=values[1],
                c=values[2],
                d=values[3],
                e=values[4],
                f=values[5],
            )
        elif name == "translate" and len(values) in (1, 2):
            operation = _Affine(e=values[0], f=values[1] if len(values) == 2 else Decimal(0))
        elif name == "scale" and len(values) in (1, 2):
            operation = _Affine(a=values[0], d=values[1] if len(values) == 2 else values[0])
        elif name == "rotate" and len(values) in (1, 3):
            radians = math.radians(float(values[0]))
            cosine = Decimal(str(math.cos(radians)))
            sine = Decimal(str(math.sin(radians)))
            rotation = _Affine(cosine, sine, -sine, cosine, inexact=True)
            if len(values) == 3:
                cx, cy = values[1:]
                operation = _Affine(e=cx, f=cy).compose(rotation).compose(_Affine(e=-cx, f=-cy))
            else:
                operation = rotation
        else:
            raise PrecisionBridgeError(f"unsupported SVG transform: {name}")
        result = result.compose(operation)
    return result


def _linear_interval(
    first_term: tuple[Decimal, Interval],
    second_term: tuple[Decimal, Interval],
    offset: Decimal,
    *,
    inexact: bool,
) -> Interval:
    first, x = first_term
    second, y = second_term
    values = (
        first * x.lower + second * y.lower + offset,
        first * x.lower + second * y.upper + offset,
        first * x.upper + second * y.lower + offset,
        first * x.upper + second * y.upper + offset,
    )
    pad = _TRANSFORM_PAD if inexact else Decimal(0)
    return Interval(min(values) - pad, max(values) + pad)


def _normalize_point(
    point: PointCell,
    container: tuple[Decimal, Decimal, Decimal, Decimal],
    side: Decimal,
) -> PointCell:
    x0, y0, width, height = container
    return PointCell(
        Interval(side * (point.x.lower - x0) / width, side * (point.x.upper - x0) / width),
        Interval(
            side * (y0 + height - point.y.upper) / height,
            side * (y0 + height - point.y.lower) / height,
        ),
    )


def _canonical_angle(angle: float) -> float:
    quarter_turn = math.pi / 2
    return (angle + math.pi / 4) % quarter_turn - math.pi / 4


def _corners_float(cx: float, cy: float, theta: float) -> tuple[tuple[float, float], ...]:
    cosine = math.cos(theta)
    sine = math.sin(theta)
    return tuple(
        (
            cx + cosine * local_x - sine * local_y,
            cy + sine * local_x + cosine * local_y,
        )
        for local_x, local_y in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5))
    )


def _cell_violation(point: tuple[float, float], cell: PointCell) -> float:
    x, y = point
    return max(
        float(cell.x.lower) - x,
        x - float(cell.x.upper),
        float(cell.y.lower) - y,
        y - float(cell.y.upper),
        0.0,
    )


def _quantized_float(value: float) -> Decimal:
    if not math.isfinite(value):
        raise PrecisionBridgeError("fitted pose is not finite")
    return Decimal(str(value)).quantize(_OUTPUT_QUANTUM)


def _decimal_text(value: Decimal) -> str:
    if not value.is_finite():
        raise PrecisionBridgeError("cannot serialize a non-finite decimal")
    normalized = value.normalize()
    if normalized == 0:
        return "0"
    return format(normalized, "f")


def _point_row(cell: PointCell) -> dict[str, list[str]]:
    return {
        "x": [_decimal_text(cell.x.lower), _decimal_text(cell.x.upper)],
        "y": [_decimal_text(cell.y.lower), _decimal_text(cell.y.upper)],
    }


def _fit_row(fit: PoseFit, side: Decimal) -> dict[str, object]:
    corners = _corners_float(float(fit.center_x), float(fit.center_y), float(fit.theta))
    wall = min(min(x, y, float(side) - x, float(side) - y) for x, y in corners)
    return {
        "id": fit.square_id,
        "pose": {
            "center_x": _decimal_text(fit.center_x),
            "center_y": _decimal_text(fit.center_y),
            "theta": _decimal_text(fit.theta),
            "enclosure": {
                "center_x": [
                    _decimal_text(fit.center_x_enclosure.lower),
                    _decimal_text(fit.center_x_enclosure.upper),
                ],
                "center_y": [
                    _decimal_text(fit.center_y_enclosure.lower),
                    _decimal_text(fit.center_y_enclosure.upper),
                ],
                "theta": [
                    _decimal_text(fit.theta_enclosure.lower),
                    _decimal_text(fit.theta_enclosure.upper),
                ],
            },
        },
        "source_cells": [_point_row(cell) for cell in fit.source_cells],
        "maximum_corner_residual": _decimal_text(fit.maximum_corner_residual),
        "signed_wall_clearance": _decimal_text(_quantized_float(wall)),
    }


def _pair_separation(first: PoseFit, second: PoseFit) -> Decimal:
    first_row = (
        first.square_id,
        float(first.center_x),
        float(first.center_y),
        float(first.theta),
    )
    second_row = (
        second.square_id,
        float(second.center_x),
        float(second.center_y),
        float(second.theta),
    )
    return _quantized_float(_verifier_pair_separation(first_row, second_row))


def _verifier_corners(cx: float, cy: float, theta: float) -> tuple[tuple[float, float], ...]:
    # Deliberately separate from the fitter's corner constructor.
    unit_x = (math.cos(theta), math.sin(theta))
    unit_y = (-unit_x[1], unit_x[0])
    output = []
    for horizontal, vertical in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        output.append(
            (
                cx + (horizontal * unit_x[0] + vertical * unit_y[0]) / 2,
                cy + (horizontal * unit_x[1] + vertical * unit_y[1]) / 2,
            )
        )
    return tuple(output)


def _verifier_pair_separation(
    first: tuple[str, float, float, float],
    second: tuple[str, float, float, float],
) -> float:
    first_corners = _verifier_corners(first[1], first[2], first[3])
    second_corners = _verifier_corners(second[1], second[2], second[3])
    axes = []
    for corners in (first_corners, second_corners):
        for index in (0, 1):
            dx = corners[index + 1][0] - corners[index][0]
            dy = corners[index + 1][1] - corners[index][1]
            length = math.hypot(dx, dy)
            axes.append((-dy / length, dx / length))
    gaps = []
    for axis_x, axis_y in axes:
        first_projection = [x * axis_x + y * axis_y for x, y in first_corners]
        second_projection = [x * axis_x + y * axis_y for x, y in second_corners]
        gaps.append(
            max(
                min(second_projection) - max(first_projection),
                min(first_projection) - max(second_projection),
            )
        )
    return max(gaps)


def _read_decimal(value: object, label: str) -> Decimal:
    if not isinstance(value, str):
        raise PrecisionBridgeError(f"{label} must be a decimal string")
    try:
        result = Decimal(value)
    except Exception as error:
        raise PrecisionBridgeError(f"{label} is not a decimal") from error
    if not result.is_finite():
        raise PrecisionBridgeError(f"{label} must be finite")
    return result


def _read_interval(value: object, label: str) -> Interval:
    if not isinstance(value, list) or len(value) != 2:
        raise PrecisionBridgeError(f"{label} must have two endpoints")
    return Interval(_read_decimal(value[0], label), _read_decimal(value[1], label))


def _read_point_cell(value: object, square_id: str) -> PointCell:
    if not isinstance(value, dict):
        raise PrecisionBridgeError(f"{square_id} source cell is not an object")
    return PointCell(
        _read_interval(value.get("x"), f"{square_id} source x cell"),
        _read_interval(value.get("y"), f"{square_id} source y cell"),
    )


def _require_pose_structure(
    pose: object, cells: object
) -> tuple[dict[str, object], list[object]]:
    if not isinstance(pose, dict) or not isinstance(cells, list) or len(cells) != 4:
        raise PrecisionBridgeError("pose/source_cells structure is malformed")
    return pose, cells


def _require_enclosure(enclosure: object) -> dict[str, object]:
    if not isinstance(enclosure, dict):
        raise PrecisionBridgeError("pose enclosure is malformed")
    return enclosure


def _json_value(value: object) -> object:
    if isinstance(value, Decimal):
        return _decimal_text(value)
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise PrecisionBridgeError(f"unsupported canonical JSON value: {type(value).__name__}")


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _selftest() -> None:
    for model in _SOURCE_MODELS:
        literal = "1.234567"
        source_cell(literal, model)
    payload = (
        b'<svg xmlns="http://www.w3.org/2000/svg">'
        b'<rect id="container" width="2" height="2"/>'
        b'<polygon id="s" points="0,0 1,0 1,1 0,1"/>'
        b"</svg>"
    )
    scene = parse_svg_scene(payload, model="declared:svg-literal", side=Decimal(2))
    receipt = scene.receipt((fit_rigid_pose(scene.squares[0]),))
    errors = verify_receipt(receipt)
    if errors:
        raise PrecisionBridgeError("selftest verification failed: " + "; ".join(errors))


logger = logging.getLogger(__name__)


def main(argv: Sequence[str] | None = None) -> int:
    """Run synthetic readiness checks; target measurement is a separate gated phase."""
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--selftest", action="store_true")
    mode.add_argument("--record")
    arguments = parser.parse_args(argv)
    try:
        if arguments.selftest:
            _selftest()
            logger.info("unitsquare precision synthetic controls passed")
            return 0
        prepare_target_run(arguments.record)
    except TargetMeasurementGatedError as error:
        logger.error("unitsquare-precision: %s", error)  # noqa: TRY400 - a refusal, not a traceback
        return 3
    except PrecisionBridgeError as error:
        logger.error("unitsquare-precision: %s", error)  # noqa: TRY400 - a refusal, not a traceback
        return 1
    raise AssertionError("authorized target execution is not exposed by the W7 CLI")


if __name__ == "__main__":
    raise SystemExit(main())
