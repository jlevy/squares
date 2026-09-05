"""Validity checking for square packings, by the separating axis theorem.

A packing of `n` unit squares in `[0, s]^2` is valid when every square lies
inside the container and every pair of squares has disjoint interiors.  For
convex polygons, disjoint interiors is equivalent to the existence of a
separating line parallel to an edge of one of them, so for two squares four
candidate axes suffice (two per square, since opposite edges are parallel).

Every quantity tested is a polynomial in the coordinates: dot products and
differences, no divisions and no square roots.  That is what lets the same
code run over exact algebraic scalars and over floats.  Pass the `sign`
function for the scalar type in use:

- exact: ``field.sign`` from :mod:`sqpack.field` -- decides zero exactly, so
  touching squares are certified rather than guessed at;
- approximate: :func:`float_sign` with a tolerance -- fast, and unable to
  distinguish a true contact from a small overlap.  See
  :func:`verify_packing` docs for why no tolerance is safe.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from dataclasses import field as _dc_field

Point = tuple  # (x, y) of some scalar type
Square = Sequence[Point]  # four corners in order


def float_sign(tol: float = 1e-9) -> Callable:
    """Sign function for float scalars, treating |v| <= tol as zero."""

    def _sign(v):
        if v > tol:
            return 1
        if v < -tol:
            return -1
        return 0

    return _sign


def exact_sign(value):
    """Sign function for :class:`sqpack.field.FieldElement` scalars."""
    return value.sign()


@dataclass
class Report:
    """Outcome of a validity check."""

    valid: bool
    n: int
    container_contacts: int = 0
    touching_pairs: int = 0
    strict_pairs: int = 0
    pairs_tested: int = 0
    touching_pair_indices: list[tuple[int, int]] = _dc_field(default_factory=list)
    failures: list = _dc_field(default_factory=list)

    def __str__(self) -> str:
        head = "VALID" if self.valid else "INVALID"
        lines = [
            f"{head}: {self.n} squares, {self.pairs_tested} pairs tested",
            (
                f"  container: {self.container_contacts} corner coordinates "
                "exactly on the boundary"
            ),
            (
                f"  pairs:     {self.touching_pairs} separated with zero gap, "
                f"{self.strict_pairs} strictly"
            ),
        ]
        for kind, detail in self.failures:
            lines.append(f"  FAILURE [{kind}]: {detail}")
        return "\n".join(lines)


def edge_axes(square: Square) -> list:
    """The two distinct outward edge normals of a square."""
    axes = []
    for k in (0, 1):
        (px, py), (qx, qy) = square[k], square[k + 1]
        axes.append((-(qy - py), qx - px))
    return axes


def project(square: Square, axis, sign) -> tuple:
    """Interval of the square's projection onto `axis`, as (min, max)."""
    values = [axis[0] * px + axis[1] * py for px, py in square]
    lo = hi = values[0]
    for v in values[1:]:
        if sign(v - lo) < 0:
            lo = v
        if sign(v - hi) > 0:
            hi = v
    return lo, hi


def separated(a: Square, b: Square, sign) -> int | None:
    """Separation verdict for a pair.

    Returns ``1`` if some axis separates them strictly, ``0`` if the best
    separation is an exact contact, and ``None`` if their interiors overlap.
    """
    best = None
    for axis in edge_axes(a) + edge_axes(b):
        alo, ahi = project(a, axis, sign)
        blo, bhi = project(b, axis, sign)
        gap = max(sign(blo - ahi), sign(alo - bhi))
        if gap > 0:
            return 1
        if gap == 0:
            best = 0
    return best


def _buckets(squares: Sequence[Square], cell: float = 2.0) -> dict:
    """Grid-bucket square centres so pair enumeration is linear in n.

    Only used when the scalar type supports float conversion; exact scalars
    fall back to the full quadratic sweep, which is what a correctness check
    wants anyway.
    """
    grid: dict = {}
    for i, sq in enumerate(squares):
        cx = sum(float(p[0]) for p in sq) / 4.0
        cy = sum(float(p[1]) for p in sq) / 4.0
        grid.setdefault((math.floor(cx / cell), math.floor(cy / cell)), []).append(i)
    return grid


def candidate_pairs(squares: Sequence[Square], *, bucket: bool = False):
    """Yield index pairs that must be tested."""
    n = len(squares)
    if not bucket:
        for i in range(n):
            for j in range(i + 1, n):
                yield i, j
        return
    grid = _buckets(squares)
    seen = set()
    for (gx, gy), members in grid.items():
        neighbours = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                neighbours.extend(grid.get((gx + dx, gy + dy), ()))
        for i in members:
            for j in neighbours:
                if i < j and (i, j) not in seen:
                    seen.add((i, j))
                    yield i, j


def check_unit_squares(squares: Sequence[Square], sign) -> list:
    """Confirm each piece really is a unit square: unit edges, right corners."""
    failures = []
    for i, sq in enumerate(squares):
        for k in range(4):
            (px, py), (qx, qy) = sq[k], sq[(k + 1) % 4]
            d2 = (qx - px) * (qx - px) + (qy - py) * (qy - py)
            if sign(d2 - 1) != 0:
                failures.append(("shape", f"square {i} edge {k} is not unit length"))
        for k in range(4):
            (ax, ay), (bx, by), (cx, cy) = sq[(k - 1) % 4], sq[k], sq[(k + 1) % 4]
            dot = (ax - bx) * (cx - bx) + (ay - by) * (cy - by)
            if sign(dot) != 0:
                failures.append(("shape", f"square {i} corner {k} is not a right angle"))
    return failures


def verify_packing(
    squares: Sequence[Square],
    side,
    sign=exact_sign,
    *,
    check_shapes: bool = True,
    bucket: bool = False,
) -> Report:
    """Check that `squares` is a valid packing of unit squares in [0, side]^2.

    With `sign` = :func:`exact_sign` over a :class:`sqpack.field.NumberField`
    this is a proof.  With :func:`float_sign` it is not, and cannot be made
    one by raising precision: a valid tight packing has pairs whose
    separation is exactly zero, so any tolerance large enough to accept those
    contacts also accepts overlaps smaller than the tolerance, and a
    tolerance of zero rejects the valid packing outright.
    """
    report = Report(valid=True, n=len(squares))
    if check_shapes:
        report.failures.extend(check_unit_squares(squares, sign))

    for i, sq in enumerate(squares):
        for px, py in sq:
            for value, edge in (
                (px, "x>=0"),
                (py, "y>=0"),
                (side - px, "x<=s"),
                (side - py, "y<=s"),
            ):
                s = sign(value)
                if s < 0:
                    report.failures.append(("container", f"square {i} violates {edge}"))
                elif s == 0:
                    report.container_contacts += 1

    for i, j in candidate_pairs(squares, bucket=bucket):
        report.pairs_tested += 1
        verdict = separated(squares[i], squares[j], sign)
        if verdict is None:
            report.failures.append(("overlap", f"squares {i} and {j} overlap"))
        elif verdict == 0:
            report.touching_pairs += 1
            report.touching_pair_indices.append((i, j))
        else:
            report.strict_pairs += 1

    report.valid = not report.failures
    return report


def corners_from_poses(x, y, theta):
    """Turn centre-and-angle poses into the corner form this module verifies.

    The one door between the pose representation every search and quench works in and
    the corner representation the validity oracle checks. It exists so that a component
    which emits poses can be checked by code it does not share -- which is the whole
    point of an independent oracle, and precisely what was missing when the quench
    returned a packing that violated its own constraints (defect D-014).
    """
    squares = []
    for cx, cy, t in zip(x, y, theta, strict=True):
        c, s = math.cos(t), math.sin(t)
        # Half-edge vectors of a unit square at this angle.
        ux, uy = 0.5 * c, 0.5 * s
        vx, vy = -0.5 * s, 0.5 * c
        squares.append(
            [
                (cx - ux - vx, cy - uy - vy),
                (cx + ux - vx, cy + uy - vy),
                (cx + ux + vx, cy + uy + vy),
                (cx - ux + vx, cy - uy + vy),
            ]
        )
    return squares
