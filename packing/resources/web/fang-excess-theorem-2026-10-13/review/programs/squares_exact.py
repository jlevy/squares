"""Exact rational reading and checking of unit-square certificates, for the review.

Written for the mathematical review of Kevin Fang's excess theorem (14 October 2026)
from the certificate convention his README states (lines 94-102 at 078789a): line 1 is
``n S`` for a square container or ``n W H`` for a rectangle, then one line ``x y t`` per
unit square, every value an exact rational, with ``t = tan(theta/2)`` so that
``cos theta = (1 - t^2)/(1 + t^2)`` and ``sin theta = 2t/(1 + t^2)``; lines starting with
``#`` are comments. A certificate is strict-valid when every square lies in the open box
and every pair is strictly separated along one of the four edge normals.

Everything is Python ``Fraction`` arithmetic. The pair test is the separating-axis test
on the two squares' edge normals, which for closed squares is equivalent to disjointness.
Pairs whose centres are farther apart than sqrt 2 are disjoint, since a closed unit
square lies in the closed disc of radius sqrt 2 / 2 about its centre; ``check_strict``
decides such pairs by the exact comparison ``dx^2 + dy^2 > 2`` and the rest by the axis
test, and with ``all_pairs=True`` decides every pair by the axis test.

Standard library only. It imports nothing of the source's and nothing of the
repository's.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, replace
from fractions import Fraction

Pose = tuple[Fraction, Fraction, Fraction]


@dataclass(frozen=True)
class Certificate:
    """``n`` unit squares ``(x, y, t)`` in the box ``[0, width] x [0, height]``."""

    n: int
    width: Fraction
    height: Fraction
    squares: tuple[Pose, ...]

    @property
    def is_square(self) -> bool:
        return self.width == self.height

    @property
    def box(self) -> tuple[int, int]:
        """The integer box ``ceil W x ceil H``."""
        return math.ceil(self.width), math.ceil(self.height)

    @property
    def squeeze(self) -> Fraction:
        """``min(a - W, b - H)``: how far the box can shrink and still hold the packing."""
        a, b = self.box
        return min(a - self.width, b - self.height)

    @property
    def waste(self) -> int:
        a, b = self.box
        return a * b - self.n


def parse_certificate(text: str) -> Certificate:
    rows = [line.split() for line in text.splitlines()]
    rows = [row for row in rows if row and not row[0].startswith("#")]
    if not rows:
        raise ValueError("no header line")
    head = rows[0]
    if len(head) not in (2, 3):
        raise ValueError(f"header is not `n S` or `n W H`: {head}")
    n = int(head[0])
    width = Fraction(head[1])
    height = Fraction(head[2]) if len(head) == 3 else width
    body = rows[1:]
    if len(body) != n:
        raise ValueError(f"header says {n} squares, file holds {len(body)}")
    squares = []
    for row in body:
        if len(row) != 3:
            raise ValueError(f"a square line is not `x y t`: {row}")
        squares.append((Fraction(row[0]), Fraction(row[1]), Fraction(row[2])))
    return Certificate(n, width, height, tuple(squares))


def certificate_text(cert: Certificate, comment: str | None = None) -> str:
    lines = [f"# {comment}"] if comment else []
    head = (
        f"{cert.n} {cert.width}" if cert.is_square else f"{cert.n} {cert.width} {cert.height}"
    )
    lines.append(head)
    lines.extend(f"{x} {y} {t}" for x, y, t in cert.squares)
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------------- geometry


def direction(t: Fraction) -> tuple[Fraction, Fraction]:
    """``(cos theta, sin theta)`` from ``t = tan(theta/2)``, exactly."""
    tt = t * t
    return (1 - tt) / (1 + tt), 2 * t / (1 + tt)


@dataclass(frozen=True)
class Square:
    """A unit square: centre, its two unit edge vectors and its four corners."""

    x: Fraction
    y: Fraction
    u: tuple[Fraction, Fraction]
    v: tuple[Fraction, Fraction]

    @classmethod
    def from_pose(cls, pose: Pose) -> Square:
        x, y, t = pose
        c, s = direction(t)
        return cls(x, y, (c, s), (-s, c))

    def corners(self) -> Iterator[tuple[Fraction, Fraction]]:
        (ux, uy), (vx, vy) = self.u, self.v
        for su in (Fraction(-1, 2), Fraction(1, 2)):
            for sv in (Fraction(-1, 2), Fraction(1, 2)):
                yield self.x + su * ux + sv * vx, self.y + su * uy + sv * vy

    def half_width(self, axis: tuple[Fraction, Fraction]) -> Fraction:
        """Half the width of the square's projection onto the unit vector ``axis``."""
        ax, ay = axis
        return (abs(ax * self.u[0] + ay * self.u[1]) + abs(ax * self.v[0] + ay * self.v[1])) / 2


def wall_clearance(square: Square, width: Fraction, height: Fraction) -> Fraction:
    """The least distance from a corner to a wall; negative when a corner is outside."""
    return min(min(cx, width - cx, cy, height - cy) for cx, cy in square.corners())


def pair_gap(p: Square, q: Square) -> Fraction:
    """The largest separation along the four edge normals; the pair is disjoint iff > 0.

    Along a unit axis ``a`` the two projections are intervals centred at ``p . a`` and
    ``q . a`` with half-widths ``h_p(a)`` and ``h_q(a)``; their separation is
    ``|(q - p) . a| - h_p(a) - h_q(a)``. The squares are strictly separated along ``a``
    when it is positive, and the separating-axis theorem says two closed convex polygons
    are disjoint exactly when some edge normal separates them.
    """
    dx, dy = q.x - p.x, q.y - p.y
    best: Fraction | None = None
    for axis in (p.u, p.v, q.u, q.v):
        separation = abs(dx * axis[0] + dy * axis[1]) - p.half_width(axis) - q.half_width(axis)
        if best is None or separation > best:
            best = separation
    assert best is not None
    return best


@dataclass(frozen=True)
class Verdict:
    """What ``check_strict`` decided about a certificate."""

    n: int
    strict_valid: bool
    least_wall_clearance: Fraction
    wall_square: int
    least_pair_gap: Fraction | None
    gap_pair: tuple[int, int] | None
    pairs_by_axes: int
    pairs_by_distance: int
    failures: tuple[str, ...]


def _cells(squares: Sequence[Square]) -> dict[tuple[int, int], list[int]]:
    cells: dict[tuple[int, int], list[int]] = {}
    for index, square in enumerate(squares):
        cells.setdefault((math.floor(square.x / 2), math.floor(square.y / 2)), []).append(index)
    return cells


def _candidate_pairs(squares: Sequence[Square]) -> Iterator[tuple[int, int]]:
    """Every pair whose centres may lie within sqrt 2 of each other, each once.

    Cells have side 2. Two squares in cells whose indices differ by two or more in
    either coordinate have centres at least 2 apart, so only the 3 x 3 block of
    neighbouring cells is searched.
    """
    cells = _cells(squares)
    for (cx, cy), members in cells.items():
        for i in members:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for j in cells.get((cx + dx, cy + dy), ()):
                        if j > i:
                            yield i, j


def _all_pairs(count: int) -> Iterator[tuple[int, int]]:
    for i in range(count):
        for j in range(i + 1, count):
            yield i, j


def check_strict(cert: Certificate, *, all_pairs: bool = False) -> Verdict:
    """Decide strict validity: open-box containment and strict pairwise separation."""
    squares = [Square.from_pose(pose) for pose in cert.squares]
    failures: list[str] = []
    least_wall: Fraction | None = None
    wall_square = -1
    for index, square in enumerate(squares):
        clearance = wall_clearance(square, cert.width, cert.height)
        if least_wall is None or clearance < least_wall:
            least_wall, wall_square = clearance, index
        if clearance <= 0:
            failures.append(f"square {index} is not strictly inside the box")
    least_gap: Fraction | None = None
    gap_pair: tuple[int, int] | None = None
    by_axes = by_distance = 0
    pairs: Iterable[tuple[int, int]] = (
        _all_pairs(len(squares)) if all_pairs else _candidate_pairs(squares)
    )
    for i, j in pairs:
        p, q = squares[i], squares[j]
        if not all_pairs:
            dx, dy = q.x - p.x, q.y - p.y
            if dx * dx + dy * dy > 2:
                by_distance += 1
                continue
        gap = pair_gap(p, q)
        by_axes += 1
        if least_gap is None or gap < least_gap:
            least_gap, gap_pair = gap, (i, j)
        if gap <= 0:
            failures.append(f"squares {i} and {j} are not strictly separated")
    assert least_wall is not None
    return Verdict(
        n=cert.n,
        strict_valid=not failures,
        least_wall_clearance=least_wall,
        wall_square=wall_square,
        least_pair_gap=least_gap,
        gap_pair=gap_pair,
        pairs_by_axes=by_axes,
        pairs_by_distance=by_distance,
        failures=tuple(failures),
    )


# ----------------------------------------------------------------------------- controls


def duplicate_control(cert: Certificate) -> Certificate:
    """Square 1 replaced by a copy of square 0: two coincident squares, which must fail."""
    squares = list(cert.squares)
    squares[1] = squares[0]
    return replace(cert, squares=tuple(squares))


def outside_control(cert: Certificate) -> Certificate:
    """Square 0 moved right by the width plus two: outside the box, which must fail."""
    squares = list(cert.squares)
    x, y, t = squares[0]
    squares[0] = (x + cert.width + 2, y, t)
    return replace(cert, squares=tuple(squares))


def scientific(value: Fraction | None) -> str:
    """A rational printed in scientific notation, for reading; the decision is exact."""
    if value is None:
        return "none"
    return f"{float(value):.6e}"
