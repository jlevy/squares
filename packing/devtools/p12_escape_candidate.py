"""Exact producer for the single H-110 candidate; no search or target work on import."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from typing import Literal, TypedDict

type Point = tuple[Fraction, Fraction]
type Status = Literal["escaped", "not_escaped", "unresolved"]

POINT_IDS = ("A1", "A2", "A3", "B", "C0", "D", "E", "F", "G", "H", "I", "J")


class MarkPacket(TypedDict):
    id: str
    xy: list[str]


class CandidatePacket(TypedDict):
    kind: Literal["p12-escape-candidate/v1"]
    q: str
    t: str
    cos: str
    sin: str
    center: list[str]
    corners: list[list[str]]
    points: list[MarkPacket]
    status: Status


@dataclass(frozen=True)
class Mark:
    """A source identity is distinct from its coordinates and order."""

    id: str
    xy: Point


@dataclass(frozen=True)
class Candidate:
    """Generic exact data; only `target_candidate` supplies the scientific instance."""

    q: Fraction
    t: Fraction
    center: Point
    points: tuple[Mark, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.q, Fraction) or self.q <= 0:
            raise ValueError("container side must be a positive Fraction")
        if not isinstance(self.t, Fraction):
            raise TypeError("half-angle must be an exact Fraction")
        _require_point(self.center)
        if not isinstance(self.points, tuple) or not all(
            isinstance(mark, Mark) for mark in self.points
        ):
            raise ValueError("point inventory must be a tuple of marks")
        if tuple(mark.id for mark in self.points) != POINT_IDS:
            raise ValueError("point inventory must have all twelve identities in source order")
        for mark in self.points:
            _require_point(mark.xy)
        if len({mark.xy for mark in self.points}) != len(POINT_IDS):
            raise ValueError("point coordinates must be distinct")


def half_angle_frame(t: Fraction) -> Point:
    """Return a rational orthonormal frame without a trigonometric approximation."""
    if not isinstance(t, Fraction):
        raise TypeError("half-angle must be an exact Fraction")
    denominator = 1 + t * t
    if denominator <= 0:
        raise ArithmeticError("nonpositive half-angle denominator")
    return (1 - t * t) / denominator, 2 * t / denominator


def strip_midpoint_center(q: Fraction, t: Fraction) -> Point:
    """Use the frozen strip-midpoint construction, with generic rational toy inputs."""
    if not isinstance(q, Fraction) or q <= 0:
        raise ValueError("container side must be a positive Fraction")
    cosine, sine = half_angle_frame(t)
    if cosine <= 0:
        raise ValueError("strip construction requires positive cosine")
    h = (cosine + sine) / 2
    v_a = -sine + cosine * (q - 3)
    v_g = -Fraction(4, 5) * sine + cosine * (q - 2)
    midpoint = (v_a + v_g) / 2
    return h, (midpoint + sine * h) / cosine


def _require_point(point: Point) -> None:
    if not isinstance(point, tuple) or len(point) != 2:
        raise ValueError("coordinates must be a pair")
    if not all(isinstance(value, Fraction) for value in point):
        raise TypeError("coordinates must be exact Fractions")


def _require_frame(cosine: Fraction, sine: Fraction) -> None:
    _require_point((cosine, sine))
    if cosine * cosine + sine * sine != 1:
        raise ValueError("frame is not exactly unit length")


def ccw_corners(center: Point, cosine: Fraction, sine: Fraction) -> tuple[Point, ...]:
    """Start at center minus both half-axes; keep cyclic counterclockwise order."""
    _require_point(center)
    _require_frame(cosine, sine)
    x, y = center
    return tuple(
        (x + (a * cosine - b * sine) / 2, y + (a * sine + b * cosine) / 2)
        for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    )


def closed_contains(center: Point, cosine: Fraction, sine: Fraction, point: Point) -> bool:
    """Boundary equality is membership; an extended supporting line is not enough."""
    _require_point(center)
    _require_point(point)
    _require_frame(cosine, sine)
    dx, dy = point[0] - center[0], point[1] - center[1]
    return abs(cosine * dx + sine * dy) <= Fraction(1, 2) and abs(
        -sine * dx + cosine * dy
    ) <= Fraction(1, 2)


def contained_in_box(q: Fraction, center: Point, cosine: Fraction, sine: Fraction) -> bool:
    """Exact support widths include contact with all four closed container walls."""
    _require_point(center)
    _require_frame(cosine, sine)
    if not isinstance(q, Fraction) or q <= 0:
        raise ValueError("container side must be a positive Fraction")
    extent = (abs(cosine) + abs(sine)) / 2
    return all(extent <= coordinate <= q - extent for coordinate in center)


def actual_angle_guard(t: Fraction) -> bool:
    """Certify 0 < 2 atan(t) < pi/720 using atan(t) < t and pi > 3.

    Failure is inconclusive about actual angle membership, not a domain refutation.
    """
    if not isinstance(t, Fraction):
        raise TypeError("half-angle must be an exact Fraction")
    return 0 < t < Fraction(1, 480)


def make_packet(candidate: Candidate) -> CandidatePacket:
    """Produce a full exact packet; status is a computation, not scientific acceptance."""
    cosine, sine = half_angle_frame(candidate.t)
    corners = ccw_corners(candidate.center, cosine, sine)
    status: Status = "unresolved"
    if actual_angle_guard(candidate.t):
        contained = contained_in_box(candidate.q, candidate.center, cosine, sine)
        hits = tuple(
            closed_contains(candidate.center, cosine, sine, mark.xy)
            for mark in candidate.points
        )
        status = "escaped" if contained and not any(hits) else "not_escaped"
    return {
        "kind": "p12-escape-candidate/v1",
        "q": str(candidate.q),
        "t": str(candidate.t),
        "cos": str(cosine),
        "sin": str(sine),
        "center": [str(value) for value in candidate.center],
        "corners": [[str(value) for value in point] for point in corners],
        "points": [
            {"id": mark.id, "xy": [str(value) for value in mark.xy]}
            for mark in candidate.points
        ],
        "status": status,
    }


def target_candidate() -> Candidate:
    """Construct the frozen scientific instance only on an explicit target dispatch."""
    q, t = Fraction(1939, 500), Fraction(1, 1000)
    # Transcription of H-110 and restricted_orientation.point_sets, not a rescaling.
    points = (
        Mark("A1", (Fraction(1), q - 3)),
        Mark("A2", (q / 2, q - 3)),
        Mark("A3", (Fraction(3, 2), Fraction(13, 10))),
        Mark("B", (q - 1, Fraction(1))),
        Mark("C0", (q - Fraction(4, 5), q / 2)),
        Mark("D", (q - 1, q - 1)),
        Mark("E", (q / 2, q - Fraction(4, 5))),
        Mark("F", (Fraction(1), q - 1)),
        Mark("G", (Fraction(4, 5), q - 2)),
        Mark("H", (Fraction(17, 10), Fraction(11, 5))),
        Mark("I", (Fraction(11, 5), Fraction(11, 5))),
        Mark("J", (Fraction(11, 5), Fraction(17, 10))),
    )
    return Candidate(q, t, strip_midpoint_center(q, t), points)


def main(argv: list[str] | None = None) -> int:
    """Emit one packet; external recorded-command limits cover the whole process."""
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--target-h110", action="store_true", required=True)
    parser.parse_args(argv)
    try:
        packet = make_packet(target_candidate())
    except (ArithmeticError, TypeError, ValueError) as error:
        print(f"candidate construction refused: {error}", file=sys.stderr)
        return 2
    print(json.dumps(packet, sort_keys=True, allow_nan=False, separators=(",", ":")))
    if packet["status"] == "unresolved":
        print("sufficient angle guard failed; no mathematical verdict", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
