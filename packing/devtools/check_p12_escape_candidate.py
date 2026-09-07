"""Independent rational corner reader for H-110; imports no producer or geometry code.

Only the CLI's fixed-target path reconstructs the scientific candidate. Generic
corner arithmetic and receipt checks are separately usable by source-free controls.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

type Point = tuple[Fraction, Fraction]
type Corners = tuple[Point, ...]

PACKET_KIND = "p12-escape-candidate/v1"
RESULT_KIND = "p12-escape-check/v1"
POINT_IDS = ("A1", "A2", "A3", "B", "C0", "D", "E", "F", "G", "H", "I", "J")
TARGET_Q_TEXT = "1939/500"
TARGET_T_TEXT = "1/1000"
MAX_PACKET_BYTES = 65536
MAX_RATIONAL_CHARACTERS = 512


class GuardError(ValueError):
    """An untrusted receipt or insufficient check cannot decide the hypothesis."""


@dataclass(frozen=True)
class Candidate:
    """Exact geometry, separate from any producer's asserted outcome."""

    q: Fraction
    t: Fraction
    cosine: Fraction
    sine: Fraction
    center: Point
    corners: Corners
    points: tuple[tuple[str, Point], ...]


def rational_frame(t: Fraction) -> Point:
    """Exact cosine and sine for twice a rational half-angle's arctangent."""
    denominator = 1 + t * t
    return (1 - t * t) / denominator, 2 * t / denominator


def alternate_center(q: Fraction, cosine: Fraction, sine: Fraction) -> Point:
    """Expanded strip-midpoint formula, testable without constructing H-110."""
    if cosine <= 0:
        raise GuardError("alternate center requires positive cosine")
    h = (cosine + sine) / 2
    return h, q - Fraction(5, 2) + (sine / cosine) * (h - Fraction(9, 10))


def square_corners(center: Point, cosine: Fraction, sine: Fraction) -> Corners:
    """Build cyclic CCW corners from the two orthonormal edge vectors."""
    x, y = center
    return (
        (x - (cosine - sine) / 2, y - (sine + cosine) / 2),
        (x + (cosine + sine) / 2, y + (sine - cosine) / 2),
        (x + (cosine - sine) / 2, y + (sine + cosine) / 2),
        (x - (cosine + sine) / 2, y - (sine - cosine) / 2),
    )


def validate_unit_square(corners: Corners) -> None:
    """Reject degeneracy, wrong edge lengths and clockwise/noncyclic ordering."""
    if len(corners) != 4:
        raise GuardError("exactly four cyclic corners are required")
    edges = tuple(
        (end[0] - start[0], end[1] - start[1])
        for start, end in zip(corners, (*corners[1:], corners[0]), strict=True)
    )
    for edge, following in zip(edges, (*edges[1:], edges[0]), strict=True):
        if edge[0] ** 2 + edge[1] ** 2 != 1:
            raise GuardError("a corner edge does not have exact unit length")
        if following != (-edge[1], edge[0]):
            raise GuardError("corner edges do not make counterclockwise right turns")


def edge_determinants(corners: Corners, point: Point) -> tuple[Fraction, ...]:
    """Left-side determinants for four cyclic, counterclockwise corners."""
    if len(corners) != 4:
        raise ValueError("exactly four corners are required")
    return tuple(
        (end[0] - start[0]) * (point[1] - start[1])
        - (end[1] - start[1]) * (point[0] - start[0])
        for start, end in zip(corners, (*corners[1:], corners[0]), strict=True)
    )


def closed_membership(corners: Corners, point: Point) -> bool:
    """A supporting-line zero is insufficient unless all edge signs are nonnegative."""
    return all(value >= 0 for value in edge_determinants(corners, point))


def reconstruct_target() -> Candidate:
    """Reconstruct H-110 independently; scientific invocation only, never a test fixture.

    The center uses H-110's alternate expanded formula, not the producer's strip
    midpoint coordinates. The full source-ordered point inventory is transcribed
    from the hypothesis rather than imported from the producer or source geometry.
    """
    q, t = Fraction(TARGET_Q_TEXT), Fraction(TARGET_T_TEXT)
    cosine, sine = rational_frame(t)
    center = alternate_center(q, cosine, sine)
    points: tuple[tuple[str, Point], ...] = (
        ("A1", (Fraction(1), q - 3)),
        ("A2", (q / 2, q - 3)),
        ("A3", (Fraction(3, 2), Fraction(13, 10))),
        ("B", (q - 1, Fraction(1))),
        ("C0", (q - Fraction(4, 5), q / 2)),
        ("D", (q - 1, q - 1)),
        ("E", (q / 2, q - Fraction(4, 5))),
        ("F", (Fraction(1), q - 1)),
        ("G", (Fraction(4, 5), q - 2)),
        ("H", (Fraction(17, 10), Fraction(11, 5))),
        ("I", (Fraction(11, 5), Fraction(11, 5))),
        ("J", (Fraction(11, 5), Fraction(17, 10))),
    )
    return Candidate(q, t, cosine, sine, center, square_corners(center, cosine, sine), points)


def _rational(value: object, label: str) -> Fraction:
    if not isinstance(value, str) or len(value) > MAX_RATIONAL_CHARACTERS:
        raise GuardError(f"{label} must be a bounded canonical rational string")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise GuardError(f"{label} is not a rational: {exc}") from exc
    if str(result) != value:
        raise GuardError(f"{label} is not a canonical rational string")
    return result


def _point(value: object, label: str) -> Point:
    if not isinstance(value, list) or len(value) != 2:
        raise GuardError(f"{label} must be exactly two rational strings")
    return _rational(value[0], f"{label}[0]"), _rational(value[1], f"{label}[1]")


def _parse_packet(raw: object) -> tuple[Candidate, str]:
    keys = {"kind", "q", "t", "cos", "sin", "center", "corners", "points", "status"}
    if not isinstance(raw, dict) or set(raw) != keys:
        raise GuardError("candidate packet must have exactly the v1 fields")
    if raw["kind"] != PACKET_KIND:
        raise GuardError("wrong candidate kind")
    status = raw["status"]
    if not isinstance(status, str) or status not in ("escaped", "not_escaped"):
        raise GuardError("producer packet is refused or incomplete")
    corners = raw["corners"]
    points = raw["points"]
    if not isinstance(corners, list) or len(corners) != 4:
        raise GuardError("packet must carry four corners")
    if not isinstance(points, list) or len(points) != len(POINT_IDS):
        raise GuardError("packet must carry the full twelve-point inventory")
    parsed_points: list[tuple[str, Point]] = []
    for expected_id, entry in zip(POINT_IDS, points, strict=True):
        if not isinstance(entry, dict) or set(entry) != {"id", "xy"}:
            raise GuardError("each marked point must carry exactly id and xy")
        if entry["id"] != expected_id:
            raise GuardError(f"point inventory must have {expected_id} at its source position")
        parsed_points.append((expected_id, _point(entry["xy"], expected_id)))
    candidate = Candidate(
        _rational(raw["q"], "q"),
        _rational(raw["t"], "t"),
        _rational(raw["cos"], "cos"),
        _rational(raw["sin"], "sin"),
        _point(raw["center"], "center"),
        tuple(_point(value, f"corner {i}") for i, value in enumerate(corners)),
        tuple(parsed_points),
    )
    return candidate, status


def _check_reconstructed(
    candidate: Candidate, producer_status: str, expected: Candidate
) -> dict[str, Any]:
    if candidate != expected:
        raise GuardError("packet differs from the independent exact reconstruction")
    denominator = 1 + candidate.t * candidate.t
    if denominator <= 0 or candidate.q <= 0 or candidate.cosine <= 0:
        raise GuardError("positive rational-frame or container guard failed")
    if (candidate.cosine, candidate.sine) != rational_frame(
        candidate.t
    ) or candidate.cosine**2 + candidate.sine**2 != 1:
        raise GuardError("frame does not equal its rational half-angle reconstruction")
    # This proves membership in the actual angle band using arctan(t)<t and pi>3.
    # Its failure is only a failed sufficient guard, not a domain counterexample.
    if not 0 < candidate.t < Fraction(1, 480):
        raise GuardError("sufficient angle guard 0 < t < 1/480 failed; domain unresolved")
    if candidate.corners != square_corners(candidate.center, candidate.cosine, candidate.sine):
        raise GuardError("corners do not match the exact center and oriented frame")
    validate_unit_square(candidate.corners)
    wall_slacks = tuple((x, candidate.q - x, y, candidate.q - y) for x, y in candidate.corners)
    contained = all(slack >= 0 for row in wall_slacks for slack in row)
    determinants = tuple(
        (name, edge_determinants(candidate.corners, point)) for name, point in candidate.points
    )
    contained_points = [
        name for name, values in determinants if all(value >= 0 for value in values)
    ]
    status = "escaped" if contained and not contained_points else "not_escaped"
    if producer_status != status:
        raise GuardError("producer status disagrees with independent geometry")
    return {
        "kind": RESULT_KIND,
        "input_kind": PACKET_KIND,
        "q": str(candidate.q),
        "t": str(candidate.t),
        "status": status,
        "producer_status": producer_status,
        "guard_status": "passed",
        "complete": True,
        "unit_square": True,
        "actual_angle_membership": True,
        "angle_argument": "0<t<1/480 implies 2*atan(t)<2*t<1/240<pi/720 (pi>3)",
        "contained": contained,
        "contained_points": contained_points,
        "corners_checked": len(candidate.corners),
        "points_checked": len(determinants),
        "edge_determinants_checked": sum(len(values) for _, values in determinants),
        "corner_wall_slacks": [[str(value) for value in row] for row in wall_slacks],
        "point_checks": [
            {
                "id": name,
                "edge_determinants": [str(value) for value in values],
                "strictly_outside": any(value < 0 for value in values),
            }
            for name, values in determinants
        ],
        "unresolved": [],
        "scope": "one auxiliary P12 candidate only; H-036 remains unresolved",
    }


def check_packet(raw: object, *, expected: Candidate) -> dict[str, Any]:
    """Check against an explicit independently supplied identity; source-free test seam."""
    candidate, status = _parse_packet(raw)
    return _check_reconstructed(candidate, status, expected)


def check_target_packet(raw: object) -> dict[str, Any]:
    """Refuse malformed/foreign receipts before reconstructing the fixed target."""
    candidate, status = _parse_packet(raw)
    if str(candidate.q) != TARGET_Q_TEXT or str(candidate.t) != TARGET_T_TEXT:
        raise GuardError("receipt is not the frozen H-110 q and t identity")
    return _check_reconstructed(candidate, status, reconstruct_target())


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GuardError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main(argv: list[str] | None = None) -> int:
    """Emit one JSON result; complete positive and negative decisions both exit zero."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", type=Path, required=True, help="complete producer JSON packet"
    )
    args = parser.parse_args(argv)
    try:
        with args.input.open("rb") as stream:
            payload = stream.read(MAX_PACKET_BYTES + 1)
        if len(payload) > MAX_PACKET_BYTES:
            raise GuardError("candidate packet exceeds the 65536-byte input guard")
        raw = json.loads(payload.decode("utf-8"), object_pairs_hook=_unique_object)
        result = check_target_packet(raw)
    except (OSError, ValueError, RecursionError) as exc:
        result = {
            "kind": RESULT_KIND,
            "status": "unresolved",
            "guard_status": "failed",
            "complete": False,
            "unresolved": [str(exc)],
            "scope": "no mathematical rejection; H-036 remains unresolved",
        }
        print(json.dumps(result, sort_keys=True, indent=2))
        print(f"reader refused: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
