"""Independent corner reader for one fixed-S full-square compatibility falsifier.

Only exact field arithmetic is shared with the producer. Scientific reconstruction
and reading the retained S packet are lazy and forbidden in source-free controls.
No-witness, tangency and failed guards establish no continuous covering conclusion.
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
type Marks = tuple[tuple[str, Point], ...]

REPO = Path(__file__).resolve().parents[2]
SOURCE = (
    "packing/campaign/series/series-000-smoke-and-calibration/results/"
    "exp-122-diamond-conditional-cover-screen/packet.json"
)
FIELD = {"minimal_polynomial": ["1", "0", "-2"], "isolating_interval": ["1", "2"]}
P10_IDS = tuple(f"p10-{index:02}" for index in range(1, 11))
P9_IDS = ("B", "C0", "D", "E", "F", "G", "H", "I", "J")
SQUARE_KEYS = {"frame_id", "offset", "cos", "sin", "center", "corners"}
MAX_PACKET_BYTES = 262144


class GuardError(ValueError):
    """The packet does not establish a valid strictly disjoint pair."""


@dataclass(frozen=True)
class Square:
    frame_id: str
    offset: Fraction
    frame: Point
    center: Point
    corners: Polygon


@dataclass(frozen=True)
class Expected:
    field: NumberField
    source: str
    q: FieldElement
    frame: Point
    p10: Marks
    p9: Marks
    fixed_square: Square


@dataclass(frozen=True)
class Pair:
    identity: Expected
    x_domain: Point
    y_domain: Point
    center: Point
    corners: Polygon
    axis: Point
    gap: FieldElement


def make_field() -> NumberField:
    return NumberField((1, 0, -2), (1, 2))


def square_corners(center: Point, frame: Point) -> Polygon:
    """Fixed cyclic CCW order, starting at center minus both half-axes."""
    x, y = center
    c, s = frame
    return (
        (x - (c - s) / 2, y - (s + c) / 2),
        (x + (c + s) / 2, y + (s - c) / 2),
        (x + (c - s) / 2, y + (s + c) / 2),
        (x - (c + s) / 2, y - (s - c) / 2),
    )


def validate_unit_square(corners: Polygon) -> None:
    if len(corners) != 4:
        raise GuardError("square needs exactly four cyclic corners")
    edges = tuple(
        (b[0] - a[0], b[1] - a[1])
        for a, b in zip(corners, (*corners[1:], corners[0]), strict=True)
    )
    for edge, following in zip(edges, (*edges[1:], edges[0]), strict=True):
        if edge[0] ** 2 + edge[1] ** 2 != 1 or following != (-edge[1], edge[0]):
            raise GuardError("corners are not an exact CCW unit square")


def determinants(corners: Polygon, point: Point) -> tuple[FieldElement, ...]:
    return tuple(
        (b[0] - a[0]) * (point[1] - a[1]) - (b[1] - a[1]) * (point[0] - a[0])
        for a, b in zip(corners, (*corners[1:], corners[0]), strict=True)
    )


def dot(axis: Point, point: Point) -> FieldElement:
    return axis[0] * point[0] + axis[1] * point[1]


def signed_gap(first: Polygon, second: Polygon, axis: Point) -> FieldElement:
    if axis == (axis[0].field.zero, axis[0].field.zero):
        raise GuardError("a separating axis must be nonzero")
    return min(dot(axis, point) for point in first) - max(dot(axis, point) for point in second)


def separating_axis(first: Polygon, second: Polygon) -> tuple[Point, FieldElement] | None:
    """Independent SAT axes are derived from vertices, not producer projections."""
    for polygon in (first, second):
        for index in (0, 1):
            a, b = polygon[index], polygon[index + 1]
            normal = a[1] - b[1], b[0] - a[0]
            for sign in (-1, 1):
                axis = sign * normal[0], sign * normal[1]
                gap = signed_gap(first, second, axis)
                if gap > 0:
                    return axis, gap
    return None


def offset_frame(field: NumberField, chart: str, offset: Fraction) -> Point:
    denominator = 1 + offset * offset
    if chart == "axis":
        return (
            field.rational((1 - offset * offset) / denominator),
            field.rational(2 * offset / denominator),
        )
    if chart == "near45":
        return (
            field.element((0, (1 - 2 * offset - offset * offset) / (2 * denominator))),
            field.element((0, (1 + 2 * offset - offset * offset) / (2 * denominator))),
        )
    raise GuardError("foreign angle chart")


def _keys(raw: Any, expected: set[str], label: str) -> None:
    if not isinstance(raw, dict) or set(raw) != expected:
        raise GuardError(f"{label} has missing, extra, or nonobject fields")


def _rational(raw: Any) -> Fraction:
    if not isinstance(raw, str) or not raw or len(raw) > 512:
        raise GuardError("expected bounded canonical rational string")
    try:
        value = Fraction(raw)
    except (ValueError, ZeroDivisionError) as exc:
        raise GuardError("invalid rational string") from exc
    if str(value) != raw:
        raise GuardError("noncanonical rational string")
    return value


def _scalar(raw: Any, field: NumberField) -> FieldElement:
    if not isinstance(raw, list) or len(raw) != 2:
        raise GuardError("scalar requires two exact basis coefficients")
    return field.element(tuple(_rational(value) for value in raw))


def _point(raw: Any, field: NumberField) -> Point:
    if not isinstance(raw, list) or len(raw) != 2:
        raise GuardError("point requires exactly two coordinates")
    return _scalar(raw[0], field), _scalar(raw[1], field)


def _corners(raw: Any, field: NumberField) -> Polygon:
    if not isinstance(raw, list) or len(raw) != 4:
        raise GuardError("four corners required")
    return tuple(_point(point, field) for point in raw)


def _marks(raw: Any, field: NumberField, ids: tuple[str, ...]) -> Marks:
    if not isinstance(raw, list) or len(raw) != len(ids):
        raise GuardError("complete marked-point inventory required")
    result: list[tuple[str, Point]] = []
    for entry, identity in zip(raw, ids, strict=True):
        _keys(entry, {"id", "xy"}, "mark")
        if entry["id"] != identity:
            raise GuardError("missing, repeated, or reordered mark identity")
        result.append((identity, _point(entry["xy"], field)))
    if len({point for _, point in result}) != len(ids):
        raise GuardError("marked-point inventory aliases distinct identities")
    return tuple(result)


def _square(raw: Any, field: NumberField) -> Square:
    _keys(raw, SQUARE_KEYS, "fixed square")
    if raw["frame_id"] not in (
        "axis-negative",
        "axis-positive",
        "near45-negative",
        "near45-positive",
    ):
        raise GuardError("foreign fixed-square frame identity")
    return Square(
        raw["frame_id"],
        _rational(raw["offset"]),
        (_scalar(raw["cos"], field), _scalar(raw["sin"], field)),
        _point(raw["center"], field),
        _corners(raw["corners"], field),
    )


def _parse(raw: Any, field: NumberField) -> Pair:
    _keys(
        raw,
        {
            "kind",
            "status",
            "field",
            "source",
            "frame",
            "domain",
            "p10",
            "p9",
            "fixed_square",
            "summary",
            "witness",
        },
        "pair packet",
    )
    if raw["kind"] != "full-square-compatibility/v1" or raw["field"] != FIELD:
        raise GuardError("foreign packet kind or exact field embedding")
    if raw["status"] != "witness":
        raise GuardError(
            "no-witness or incomplete screening cannot establish a pair or a cover"
        )
    if not isinstance(raw["source"], str) or not raw["source"] or len(raw["source"]) > 1024:
        raise GuardError("source identity must be a bounded path string")
    _keys(raw["frame"], {"id", "cos", "sin"}, "Q frame")
    if raw["frame"]["id"] != "exact45":
        raise GuardError("only the fixed exact45 Q frame is admitted")
    frame = _scalar(raw["frame"]["cos"], field), _scalar(raw["frame"]["sin"], field)
    _keys(raw["domain"], {"q", "x", "y"}, "domain")
    q = _scalar(raw["domain"]["q"], field)
    if q <= 0:
        raise GuardError("container side must be positive")
    x_domain, y_domain = _point(raw["domain"]["x"], field), _point(raw["domain"]["y"], field)
    p10, p9 = _marks(raw["p10"], field, P10_IDS), _marks(raw["p9"], field, P9_IDS)
    fixed_square = _square(raw["fixed_square"], field)
    summary = raw["summary"]
    _keys(
        summary,
        {"cells_checked", "canonical_cells_checked", "uncovered_cells_checked", "complete"},
        "summary",
    )
    counts = [
        summary[key]
        for key in ("cells_checked", "canonical_cells_checked", "uncovered_cells_checked")
    ]
    if (
        any(type(value) is not int or value < 1 for value in counts)
        or not counts[0] >= counts[1] >= counts[2]
        or summary["complete"] is not False
    ):
        raise GuardError("malformed witness-summary provenance")
    witness = raw["witness"]
    _keys(witness, {"center", "corners", "axis", "gap"}, "witness")
    identity = Expected(field, raw["source"], q, frame, p10, p9, fixed_square)
    return Pair(
        identity,
        x_domain,
        y_domain,
        _point(witness["center"], field),
        _corners(witness["corners"], field),
        _point(witness["axis"], field),
        _scalar(witness["gap"], field),
    )


def _encode(value: FieldElement) -> list[str]:
    return [str(coefficient) for coefficient in value.coeffs]


def _check(pair: Pair, expected: Expected) -> dict[str, Any]:
    if pair.identity != expected:
        raise GuardError(
            "pair differs from independently reconstructed source or point identity"
        )
    field, q, fixed = expected.field, expected.q, expected.fixed_square
    if pair.x_domain != (field.one, q / 2) or pair.y_domain != (field.zero, field.one):
        raise GuardError("foreign canonical center domain")
    if expected.frame != (field.alpha / 2, field.alpha / 2):
        raise GuardError("Q must use the exact positive45 frame")
    chart, label = fixed.frame_id.split("-")
    if (
        (label == "negative" and fixed.offset >= 0)
        or (label == "positive" and fixed.offset <= 0)
        or abs(fixed.offset) >= Fraction(1, 480)
    ):
        raise GuardError("fixed-square actual-angle sufficient guard failed")
    if fixed.frame != offset_frame(field, chart, fixed.offset):
        raise GuardError("fixed-square frame disagrees with its exact angle")
    for polygon, center, frame in (
        (pair.corners, pair.center, expected.frame),
        (fixed.corners, fixed.center, fixed.frame),
    ):
        validate_unit_square(polygon)
        if polygon != square_corners(center, frame):
            raise GuardError("corner order, frame, or center disagreement")
    wall_slacks = tuple(
        (coordinate, q - coordinate)
        for polygon in (pair.corners, fixed.corners)
        for point in polygon
        for coordinate in point
    )
    if any(value < 0 for bounds in wall_slacks for value in bounds):
        raise GuardError("a square violates closed container containment")
    x, y = pair.center
    if not (1 <= x <= q / 2 and 0 <= y <= 1):
        raise GuardError("Q center is outside the canonical region")
    point_checks: list[dict[str, Any]] = []
    for name, polygon, marks in (
        ("Q", pair.corners, expected.p10),
        ("S", fixed.corners, expected.p9),
    ):
        for identity, point in marks:
            values = determinants(polygon, point)
            point_checks.append(
                {
                    "square": name,
                    "id": identity,
                    "determinants": [_encode(value) for value in values],
                    "strictly_outside": any(value < 0 for value in values),
                }
            )
    if not all(check["strictly_outside"] for check in point_checks):
        raise GuardError("a closed square contains a required avoided mark")
    if pair.gap <= 0 or signed_gap(pair.corners, fixed.corners, pair.axis) != pair.gap:
        raise GuardError("claimed separating gap is not exact and strictly positive")
    independent = separating_axis(pair.corners, fixed.corners)
    if independent is None:
        raise GuardError("closed squares overlap or touch; strict disjointness is unproved")
    axis, gap = independent
    return {
        "kind": "full-square-compatibility-check/v1",
        "status": "verified_pair",
        "complete": True,
        "guard_status": "passed",
        "source": expected.source,
        "q": _encode(q),
        "Q_points_checked": 10,
        "S_points_checked": 9,
        "edge_determinants_checked": 76,
        "coordinate_wall_checks": 16,
        "wall_inequalities_checked": 32,
        "wall_slacks": [[_encode(value) for value in bounds] for bounds in wall_slacks],
        "point_checks": point_checks,
        "actual_angle_membership": True,
        "strict_disjointness": True,
        "canonical_Q": True,
        "independent_axis": [_encode(value) for value in axis],
        "independent_gap": _encode(gap),
        "unresolved": [],
        "scope": "One fixed-S pair only; no continuous cover or H-036 conclusion.",
    }


def check_packet(raw: Any, *, expected: Expected) -> dict[str, Any]:
    """Source-free seam; the caller supplies an unrelated complete identity."""
    return _check(_parse(raw, expected.field), expected)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GuardError("duplicate JSON object key")
        result[key] = value
    return result


def read_json(path: Path) -> Any:
    with path.open("rb") as stream:
        data = stream.read(MAX_PACKET_BYTES + 1)
    if len(data) > MAX_PACKET_BYTES:
        raise GuardError("packet exceeds byte cap")
    return json.loads(data, object_pairs_hook=_unique_object)


def load_target(field: NumberField) -> Expected:
    """Scientific data binding; never executed during source-free author controls."""
    raw = read_json(REPO / SOURCE)
    _keys(raw, {"kind", "status", "field", "frames", "witness"}, "retained source")
    if (
        raw["kind"] != "diamond-cover-screen/v1"
        or raw["status"] != "witness"
        or raw["field"] != FIELD
    ):
        raise GuardError("retained source identity is not the frozen witness packet")
    witness = raw["witness"]
    if not isinstance(witness, dict) or not set(witness) >= SQUARE_KEYS:
        raise GuardError("retained source lacks complete fixed-square data")
    fixed = _square({key: witness[key] for key in SQUARE_KEYS}, field)
    q = field.rational(Fraction(1939, 500))
    if (
        fixed.frame_id != "axis-negative"
        or fixed.offset != Fraction(-1, 500)
        or _scalar(witness.get("q"), field) != q
    ):
        raise GuardError("foreign retained experiment frame or side")
    one, half = field.one, Fraction(1, 2)
    seeds = ((one, one), (q / 2, one), (Fraction(3, 2) - q / 4, q / 2), (half + q / 4, q / 2))
    ten = tuple(
        sorted(
            {
                (q - x if flip_x else x, q - y if flip_y else y)
                for x, y in seeds
                for flip_x in (False, True)
                for flip_y in (False, True)
            }
        )
    )
    if len(ten) != 10:
        raise GuardError("independent P10 reflection inventory is not ten distinct marks")
    nine = (
        (q - 1, one),
        (q - Fraction(4, 5), q / 2),
        (q - 1, q - 1),
        (q / 2, q - Fraction(4, 5)),
        (one, q - 1),
        (field.rational("4/5"), q - 2),
        (field.rational("17/10"), field.rational("11/5")),
        (field.rational("11/5"), field.rational("11/5")),
        (field.rational("11/5"), field.rational("17/10")),
    )
    p10, p9 = tuple(zip(P10_IDS, ten, strict=True)), tuple(zip(P9_IDS, nine, strict=True))
    if _marks(witness.get("points"), field, P9_IDS) != p9:
        raise GuardError("retained P9 source identity disagrees with independent formulas")
    return Expected(field, SOURCE, q, (field.alpha / 2, field.alpha / 2), p10, p9, fixed)


def check_target_packet(raw: Any) -> dict[str, Any]:
    field = make_field()
    pair = _parse(raw, field)
    if pair.identity.source != SOURCE or pair.identity.q != field.rational("1939/500"):
        raise GuardError("foreign source or target side")
    return _check(pair, load_target(field))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = check_target_packet(read_json(args.input))
    except (OSError, ValueError, RecursionError) as exc:
        print(
            json.dumps(
                {
                    "status": "unresolved",
                    "complete": False,
                    "guard_status": "refused",
                    "unresolved": [str(exc)],
                    "scope": "No pair, cover or packing bound established.",
                },
                sort_keys=True,
            )
        )
        print(f"pair reader refused: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
