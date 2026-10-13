"""Check the point pattern behind Green's DS7 Theorem 9, and whether it is unavoidable.

Friedman's survey DS7 states Theorem 9, from Trevor Green's private communication of
2000, and gives no proof:

    s(k^2 + 1) >= G_k = 2 sqrt 2 - 1 + (k (k - 1)^2 + (k - 1) sqrt(2k)) / (k^2 + 1).

Its Figure 34 draws sixteen points for ``k = 4`` and calls them an unavoidable set.
DS7's Section 5 says what that means: a set ``P`` is unavoidable in the closed square
``S`` when every closed unit square inside ``S`` contains a point of ``P``, possibly on
its boundary; shrinking ``P`` by ``1 - eps/L`` then puts a point in the interior of every
unit square in a square of side ``L - eps``, so ``k^2`` points unavoidable at side ``G_k``
prove ``s(k^2 + 1) >= G_k``.

Hosono's write-up of 2026-10-02 (jlevy/squares#308, retained under
``resources/web/wand125-green-ds7-theorem9-2026-10-02``) reconstructs the pattern for
every ``k``, and MacIver's manuscript of August 2026 gives the same one for ``k = 4``:
``k`` rows at heights ``m_y + j t``, even rows at offsets ``0, u, u + 1, ..., u + k - 2``
and odd rows at ``0, 1, ..., k - 2, u + k - 2`` from ``m_x``, with

    t = (k (k - 1) + sqrt(2k)) / (k^2 + 1),   u = (k sqrt(2k) - (k - 1)) / (k^2 + 1),
    m_x = sqrt 2 - t/2,                       m_y = sqrt 2 - 1/2.

For each ``k`` asked, this tool checks:

- **That the pattern reproduces G_k.** ``t^2 + u^2 = 1``, ``k t - u = k - 1``, and the
  width ``2 m_x + u + k - 2`` and height ``2 m_y + (k - 1) t`` both equal DS7's ``G_k``,
  as exact identities. It counts the mesh edges of displacement ``(+-(1 - u), t)``
  between neighbouring rows, of length ``d = sqrt(2 - 2u)``, and decides ``d <= 1``,
  DS7 Lemma 3's hypothesis for the triangles they bound, and ``m_x <= 1``, without which
  a strip of width one along a side wall holds no point.
- **The write-up's empty square** ``Q_k`` (``k >= 4``), centred at the midpoint of the
  long edge from ``A = (u + 1, 0)`` to ``D = (2, t)`` with sides along it, and at
  ``k = 4`` the square the write-up publishes, each against every point and every wall.
- **An independent search.** By DS7 Lemma 3 the centre of an empty unit square lies in a
  mesh triangle with a side longer than one, or outside the mesh. The search runs a
  compass search of the clearance from poses in all of those regions, in floating point,
  and hands its best pose to the same exact check. A search that finds nothing proves
  nothing.
- **A certificate where nothing escapes** (``--certify``). The pattern, scaled to a
  rational side a little below ``G_k`` and rounded to the grid of
  ``cases.green17.interval_audit``, goes to that module's exhaustive branch-and-bound,
  which certifies that every closed unit square in the container contains a point or
  refuses. The certified set is the rounded one, within ``1e-18`` of the scaled pattern,
  and proves ``s(k^2 + 1)`` at least its side. At ``G_k`` itself the pattern is tight --
  DS7 Lemma 2 holds with equality at the walls -- and a rational branch-and-bound cannot
  close a family of zero width on irrational coordinates.

**Exactness.** Every coordinate lies in ``Q(sqrt 2, sqrt k)`` and is held as a finite
sum of rational multiples of square roots of distinct squarefree integers (`Surd`).
Square roots of distinct squarefree integers are linearly independent over the
rationals (Besicovitch, 1940), so such a sum is zero exactly when every coefficient is,
and the sign of a nonzero one is decided by integer square-root enclosures refined until
they exclude zero. A checked square has a `Surd` centre and a rational rotation,
``cos = (1 - tau^2)/(1 + tau^2)``, ``sin = 2 tau/(1 + tau^2)`` for a rational ``tau``, so
``cos^2 + sin^2 = 1`` holds exactly and every quantity compared is a `Surd`. Floating
point chooses where to look; it decides nothing.

**Conventions.** A square *fits* when it lies in the closed container ``[0, G_k]^2``, so
touching a wall is allowed, and *contains* a point lying in the closed square, so a point
on its boundary counts. An *empty* square is a fitting square with every point strictly
outside it. That is the hardest form of the claim to refute: it refutes DS7's
unavoidability with boundary points counted, and, because the reported clearances are
positive, every shrunk or open variant as well. ``ceiling`` bounds the largest side at
which the pattern, scaled, is unavoidable: an empty square of half side ``h > 1/2`` is
found and checked, so the scaled pattern fails at every side from ``G_k/(2h)`` up.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.check_green_ds7
    uv run --frozen --all-extras --group dev python -m devtools.check_green_ds7 \\
        --k 2 12 --certify --json /tmp/green.json
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import math
import re
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path
from typing import Any, cast

import numpy as np
import numpy.typing as npt
from scipy.spatial import Delaunay

HALF = Fraction(1, 2)

#: The finest refinement `Surd.sign` attempts; reaching it means a bug, not a hard case.
MAX_BITS = 1 << 16

#: Rounding grid for the rational centre and tangent of a square found in floating point.
ROUND = 10**18

#: How far below `G_k` the certified side sits, as a fraction of `G_k`.
CERTIFY_MARGIN = Fraction(1, 1000)

#: The square Hosono's write-up publishes for `k = 4`: centre and `tan(theta/2)`. The
#: centre is in container coordinates, as the dashed square of its Figure 1 places it, a
#: translate of `Q_4` along the long edge's normal.
PUBLISHED_K4 = (Fraction(29638179, 10**7), Fraction(302261, 250000), Fraction(179111, 312500))

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "resources/web/wand125-green-ds7-theorem9-2026-10-02"

#: The write-up's copy of DS7 Figure 34's left panel, which embeds DS7's own GIF.
FIGURE = PACKET / "green-theorem9-gist/ds7-fig34-L17.svg"

#: The SHA-256 of DS7's `pic/L17.gif` as combinatorics.org served it on 2026-10-02.
DS7_L17_GIF_SHA256 = "2b6b3af60fe9b629e00824d80c937c8f7de9f9fa354b4b96af03d9ca5a6e8c54"

Interval = tuple[Fraction, Fraction]
Array = npt.NDArray[np.float64]


# --------------------------------------------------------------------------- arithmetic


def squarefree_split(value: int) -> tuple[int, int]:
    """``(a, s)`` with ``value = a * a * s`` and ``s`` squarefree, for ``value >= 1``."""
    if value < 1:
        raise ValueError(f"squarefree_split needs a positive integer, got {value}")
    outside, inside, factor = 1, value, 2
    while factor * factor <= inside:
        while inside % (factor * factor) == 0:
            inside //= factor * factor
            outside *= factor
        factor += 1
    return outside, inside


def _sqrt_interval(radicand: int, bits: int) -> Interval:
    scale = 1 << bits
    root = isqrt(radicand * scale * scale)
    exact = root * root == radicand * scale * scale
    return Fraction(root, scale), Fraction(root if exact else root + 1, scale)


@dataclass(frozen=True)
class Surd:
    """``sum c_s sqrt(s)`` over distinct squarefree ``s >= 1``, every ``c_s`` rational.

    ``terms`` is sorted by radicand and holds no zero coefficient, so the empty tuple is
    zero and two values are equal exactly when their terms are.
    """

    terms: tuple[tuple[int, Fraction], ...] = ()

    @classmethod
    def of(cls, value: Surd | Fraction | int) -> Surd:
        if isinstance(value, Surd):
            return value
        return cls(((1, Fraction(value)),)) if value else cls()

    @classmethod
    def sqrt(cls, value: int) -> Surd:
        """The square root of a nonnegative integer."""
        if value == 0:
            return cls()
        outside, inside = squarefree_split(value)
        return cls(((inside, Fraction(outside)),))

    @classmethod
    def _collect(cls, pairs: Sequence[tuple[int, Fraction]]) -> Surd:
        total: dict[int, Fraction] = {}
        for radicand, coefficient in pairs:
            total[radicand] = total.get(radicand, Fraction(0)) + coefficient
        return cls(tuple(sorted((r, c) for r, c in total.items() if c != 0)))

    def __add__(self, other: Surd | Fraction | int) -> Surd:
        return Surd._collect((*self.terms, *Surd.of(other).terms))

    def __radd__(self, other: Fraction | int) -> Surd:
        return self + other

    def __neg__(self) -> Surd:
        return Surd(tuple((r, -c) for r, c in self.terms))

    def __sub__(self, other: Surd | Fraction | int) -> Surd:
        return self + (-Surd.of(other))

    def __rsub__(self, other: Fraction | int) -> Surd:
        return Surd.of(other) - self

    def __mul__(self, other: Surd | Fraction | int) -> Surd:
        pairs: list[tuple[int, Fraction]] = []
        for r1, c1 in self.terms:
            for r2, c2 in Surd.of(other).terms:
                # Both radicands are squarefree, so r1 r2 = g^2 (r1/g)(r2/g) with the
                # last factor squarefree.
                g = gcd(r1, r2)
                pairs.append(((r1 // g) * (r2 // g), c1 * c2 * g))
        return Surd._collect(pairs)

    def __rmul__(self, other: Fraction | int) -> Surd:
        return self * other

    def __truediv__(self, other: Fraction | int) -> Surd:
        divisor = Fraction(other)
        if divisor == 0:
            raise ZeroDivisionError("Surd division by zero")
        return Surd(tuple((r, c / divisor) for r, c in self.terms))

    def interval(self, bits: int = 96) -> Interval:
        """Rational bounds on the value, each square root enclosed to ``2**-bits``."""
        lo = hi = Fraction(0)
        for radicand, coefficient in self.terms:
            r_lo, r_hi = _sqrt_interval(radicand, bits)
            if coefficient > 0:
                lo += coefficient * r_lo
                hi += coefficient * r_hi
            else:
                lo += coefficient * r_hi
                hi += coefficient * r_lo
        return lo, hi

    def sign(self) -> int:
        """The exact sign: zero only for the empty sum, by linear independence."""
        if not self.terms:
            return 0
        bits = 64
        while bits <= MAX_BITS:
            lo, hi = self.interval(bits)
            if lo > 0:
                return 1
            if hi < 0:
                return -1
            bits *= 2
        raise ArithmeticError(f"sign of a nonzero Surd not separated at {MAX_BITS} bits")

    def midpoint(self, bits: int = 192) -> Fraction:
        lo, hi = self.interval(bits)
        return (lo + hi) / 2

    def __float__(self) -> float:
        return float(self.midpoint(80))

    def __str__(self) -> str:
        if not self.terms:
            return "0"
        parts = [str(c) if r == 1 else f"{c}*sqrt({r})" for r, c in self.terms]
        return " + ".join(parts).replace("+ -", "- ")


SQRT2 = Surd.sqrt(2)


def floor_to(value: Fraction, denominator: int = 10**12) -> Fraction:
    return Fraction(math.floor(value * denominator), denominator)


def ceil_to(value: Fraction, denominator: int = 10**12) -> Fraction:
    return Fraction(math.ceil(value * denominator), denominator)


def nearest(value: float | Fraction, denominator: int = ROUND) -> Fraction:
    return Fraction(round(Fraction(value) * denominator), denominator)


# --------------------------------------------------------------------------- the pattern


def green_bound(k: int) -> Surd:
    """DS7 Theorem 9's ``G_k``, transcribed as printed."""
    return 2 * SQRT2 - 1 + (k * (k - 1) ** 2 + (k - 1) * Surd.sqrt(2 * k)) / (k * k + 1)


@dataclass(frozen=True)
class Pattern:
    """Green's ``k^2`` points for ``s(k^2 + 1)``, as the write-up and MacIver read them.

    ``rows[j]`` holds the indices into ``points`` of row ``j``, left to right.
    """

    k: int
    t: Surd
    u: Surd
    mx: Surd
    my: Surd
    side: Surd
    points: tuple[tuple[Surd, Surd], ...]
    rows: tuple[tuple[int, ...], ...]

    @property
    def n(self) -> int:
        return self.k * self.k + 1


def pattern(k: int) -> Pattern:
    if k < 2:
        raise ValueError(f"the pattern needs k >= 2, got {k}")
    root = Surd.sqrt(2 * k)
    t = (k * (k - 1) + root) / (k * k + 1)
    u = (k * root - (k - 1)) / (k * k + 1)
    mx = SQRT2 - t / 2
    my = SQRT2 - HALF
    points: list[tuple[Surd, Surd]] = []
    rows: list[tuple[int, ...]] = []
    for j in range(k):
        if j % 2 == 0:
            offsets = [Surd(), *(u + i for i in range(k - 1))]
        else:
            offsets = [*(Surd.of(i) for i in range(k - 1)), u + (k - 2)]
        start = len(points)
        points.extend((mx + offset, my + j * t) for offset in offsets)
        rows.append(tuple(range(start, len(points))))
    return Pattern(k, t, u, mx, my, green_bound(k), tuple(points), tuple(rows))


def identities(p: Pattern) -> dict[str, bool]:
    """The exact identities that make the pattern Green's; each must hold."""
    k = p.k
    inside = all(
        coordinate.sign() > 0 and (p.side - coordinate).sign() > 0
        for point in p.points
        for coordinate in point
    )
    return {
        "t^2 + u^2 = 1": p.t * p.t + p.u * p.u == Surd.of(1),
        "k t - u = k - 1": k * p.t - p.u == Surd.of(k - 1),
        "width 2 m_x + u + k - 2 = G_k": 2 * p.mx + p.u + (k - 2) == p.side,
        "height 2 m_y + (k - 1) t = G_k": 2 * p.my + (k - 1) * p.t == p.side,
        "0 < u < 1 and 0 < t < 1": all(v.sign() > 0 and (1 - v).sign() > 0 for v in (p.u, p.t)),
        "k^2 points strictly inside the container": len(p.points) == k * k and inside,
    }


def long_edges(p: Pattern) -> list[tuple[int, int]]:
    """Index pairs in neighbouring rows displaced by ``(+-(1 - u), t)``, length ``d``."""
    run = 1 - p.u
    edges: list[tuple[int, int]] = []
    for lower, upper in zip(p.rows, p.rows[1:], strict=False):
        for i in lower:
            for j in upper:
                dx = p.points[j][0] - p.points[i][0]
                if dx in (run, -run):
                    edges.append((i, j))
    return edges


def long_edge_exceeds_one(p: Pattern) -> bool:
    """``d > 1`` exactly; ``d^2 = (1 - u)^2 + t^2 = 2 - 2u``, so this is ``u < 1/2``."""
    return (HALF - p.u).sign() > 0


def side_margin_exceeds_one(p: Pattern) -> bool:
    """``m_x > 1``: the strip ``[0, m_x) x [0, G_k]`` then holds a unit square and no point."""
    return (p.mx - 1).sign() > 0


# --------------------------------------------------------------------------- squares


@dataclass(frozen=True)
class Square:
    """The closed square of half side ``half`` centred at ``(x, y)`` with frame
    ``e = (cos, sin)``, ``n = (-sin, cos)``; ``cos^2 + sin^2 = 1`` exactly."""

    x: Surd
    y: Surd
    cos: Fraction
    sin: Fraction
    half: Fraction = HALF

    def __post_init__(self) -> None:
        if self.cos * self.cos + self.sin * self.sin != 1:
            raise ValueError("a Square's frame must be an exact unit vector")
        if self.half <= 0:
            raise ValueError("a Square's half side must be positive")

    @classmethod
    def from_tangent(
        cls,
        x: Surd | Fraction,
        y: Surd | Fraction,
        tau: Fraction,
        half: Fraction = HALF,
    ) -> Square:
        """The frame at angle ``theta`` with ``tan(theta/2) = tau``, exactly unit."""
        denominator = 1 + tau * tau
        return cls(
            Surd.of(x), Surd.of(y), (1 - tau * tau) / denominator, 2 * tau / denominator, half
        )

    @property
    def theta_degrees(self) -> float:
        return math.degrees(math.atan2(self.sin, self.cos))

    def grown(self, half: Fraction) -> Square:
        return Square(self.x, self.y, self.cos, self.sin, half)


@dataclass(frozen=True)
class SquareCheck:
    """What the exact check found; the two bounds are rounded down to ``1e-12``."""

    fits: bool
    empty: bool
    covered_by: tuple[int, ...]
    clearance_lower: Fraction
    slack_lower: Fraction

    @property
    def escapes(self) -> bool:
        return self.fits and self.empty


def check_square(p: Pattern, square: Square) -> SquareCheck:
    """Decide exactly whether ``square`` fits in ``[0, G_k]^2`` and misses every point."""
    reach = square.half * (abs(square.cos) + abs(square.sin))
    walls = (
        square.x - reach,
        p.side - square.x - reach,
        square.y - reach,
        p.side - square.y - reach,
    )
    fits = all(wall.sign() >= 0 for wall in walls)
    clearance = min(wall.interval()[0] for wall in walls)
    covered: list[int] = []
    slack: Fraction | None = None
    for index, (px, py) in enumerate(p.points):
        dx, dy = px - square.x, py - square.y
        along = square.cos * dx + square.sin * dy
        across = square.cos * dy - square.sin * dx
        outside = any(
            (side * value - square.half).sign() > 0
            for value in (along, across)
            for side in (1, -1)
        )
        if not outside:
            covered.append(index)
        a_lo, a_hi = along.interval()
        b_lo, b_hi = across.interval()
        reach_lower = max(a_lo, -a_hi, b_lo, -b_hi) - square.half
        slack = reach_lower if slack is None else min(slack, reach_lower)
    return SquareCheck(
        fits=fits,
        empty=not covered,
        covered_by=tuple(covered),
        clearance_lower=floor_to(clearance),
        slack_lower=floor_to(slack if slack is not None else Fraction(0)),
    )


def writeup_square(p: Pattern, half: Fraction = HALF) -> Square:
    """The write-up's ``Q_k``: centred on the long edge ``A = (u + 1, 0)`` to
    ``D = (2, t)`` (offsets from ``(m_x, m_y)``), sides along it; ``k >= 4``."""
    if p.k < 4:
        raise ValueError("the edge A D needs k >= 4")
    x = p.mx + (p.u + 3) / 2
    y = p.my + p.t / 2
    theta = math.atan2(float(p.t), float(1 - p.u))
    return Square.from_tangent(nearest(float(x)), nearest(float(y)), _tangent(theta), half)


def strip_square(p: Pattern) -> Square:
    """An axis-parallel unit square in the left wall strip, centred between the wall and
    the first column and halfway up; it misses every point when ``m_x > 1``."""
    return Square.from_tangent(
        nearest(float(p.mx / 2)), nearest(float(p.side / 2)), Fraction(0)
    )


def published_square(p: Pattern) -> Square:
    """The empty square the write-up publishes for ``k = 4``, exactly as printed."""
    if p.k != 4:
        raise ValueError("the write-up publishes its square for k = 4 only")
    x, y, tau = PUBLISHED_K4
    return Square.from_tangent(x, y, tau)


def _tangent(theta: float) -> Fraction:
    return nearest(math.tan(theta / 2))


def widest_empty(p: Pattern, square: Square, base: SquareCheck) -> tuple[Square, SquareCheck]:
    """Grow an empty square about its centre as far as the exact check allows.

    A concentric square of half side ``1/2 + s`` keeps every point out while ``s`` is
    below the slack, and fits while ``s sqrt 2`` is below the wall clearance. The grown
    square is checked again, exactly.
    """
    grow = min(base.slack_lower, base.clearance_lower * Fraction(7, 10))
    for fraction in (Fraction(99, 100), Fraction(9, 10), Fraction(1, 2)):
        candidate = square.grown(square.half + floor_to(grow * fraction))
        result = check_square(p, candidate)
        if result.escapes:
            return candidate, result
    return square, base


def ceiling_bound(p: Pattern, square: Square) -> Fraction:
    """An upper bound on ``G_k/(2h)``: the scaled pattern fails at every side above it."""
    return ceil_to(p.side.interval()[1] / (2 * square.half))


# --------------------------------------------------------------------------- the figure


@dataclass(frozen=True)
class FigureMatch:
    """DS7 Figure 34's dots against the ``k = 4`` pattern, in pixels of the image.

    ``row_zero`` says where the figure draws the pattern's row ``j = 0`` (the even row at
    height ``m_y``): ``"top"`` means the figure is the pattern reflected in ``y``.
    """

    gif_sha256: str
    dots: int
    pixels_per_unit: float
    row_zero: str
    max_residual: float
    other_residual: float


def figure_image(gif: bytes) -> npt.NDArray[np.uint8]:
    """The image as greyscale pixels, rows first."""
    from PIL import Image  # noqa: PLC0415 -- only the figure check reads an image

    return np.asarray(Image.open(io.BytesIO(gif)).convert("L"))


def figure_dots(image: npt.NDArray[np.uint8]) -> Array:
    """Centres ``(column, row)`` of the black dots inside the black frame."""
    from scipy import ndimage  # noqa: PLC0415

    dark = image < 80
    dark[[0, -1], :] = False
    dark[:, [0, -1]] = False
    labels, count = cast("tuple[npt.NDArray[np.int32], int]", ndimage.label(dark))
    centres = ndimage.center_of_mass(dark, labels, range(1, count + 1))
    return np.array([(column, row) for row, column in centres], dtype=np.float64)


def figure_gif(svg: str) -> bytes:
    """The GIF a retained SVG embeds as a base64 data URI."""
    match = re.search(r"data:image/gif;base64,([A-Za-z0-9+/=]+)", svg)
    if match is None:
        raise ValueError("no embedded GIF in the SVG")
    return base64.b64decode(match.group(1))


def match_figure(p: Pattern, gif: bytes) -> FigureMatch:
    """Map the container's walls to the image frame and match dots to points one-to-one.

    The frame is the outermost dark row and column, at pixels ``0`` and ``size - 1``, so
    a coordinate ``c`` sits at pixel ``c (size - 1)/G_k``. Image rows count downward. The
    pattern is drawn both ways up, which between them cover all four reflections: the
    half-turn maps it to itself. The worst residual of the better one is reported, with
    the other's for comparison.
    """
    from scipy.optimize import linear_sum_assignment  # noqa: PLC0415

    image = figure_image(gif)
    dots = figure_dots(image)
    top = image.shape[0] - 1
    scale = top / float(p.side)
    worst: dict[str, float] = {}
    for row_zero in ("top", "bottom"):
        drawn = _float_points(p) * scale
        if row_zero == "bottom":
            drawn[:, 1] = top - drawn[:, 1]
        if len(dots) != len(drawn):
            worst[row_zero] = math.inf
            continue
        cost = np.hypot(
            dots[:, None, 0] - drawn[None, :, 0], dots[:, None, 1] - drawn[None, :, 1]
        )
        rows, columns = linear_sum_assignment(cost)
        worst[row_zero] = float(cost[rows, columns].max())
    best = min(worst, key=lambda key: worst[key])
    other = "bottom" if best == "top" else "top"
    return FigureMatch(
        gif_sha256=hashlib.sha256(gif).hexdigest(),
        dots=len(dots),
        pixels_per_unit=scale,
        row_zero=best,
        max_residual=worst[best],
        other_residual=worst[other],
    )


# --------------------------------------------------------------------------- the search


def _float_points(p: Pattern) -> Array:
    return np.array([[float(x), float(y)] for x, y in p.points], dtype=np.float64)


def search_starts(p: Pattern, angles: int = 6, step: float = 0.25) -> Array:
    """Poses ``(x, y, theta)`` covering every region DS7 Lemma 3 leaves open.

    The centroid and side midpoints of each Delaunay triangle with a side longer than one,
    and a grid over the container outside the triangulation; each at ``angles``
    orientations in ``[0, pi/2)``.
    """
    points = _float_points(p)
    side = float(p.side)
    mesh = Delaunay(points)
    centres: list[Array] = []
    for simplex in mesh.simplices:
        corners = points[simplex]
        sides = [float(np.linalg.norm(corners[i] - corners[(i + 1) % 3])) for i in range(3)]
        if max(sides) <= 1:
            continue
        centres.append(corners.mean(axis=0))
        centres.extend((corners[i] + corners[(i + 1) % 3]) / 2 for i in range(3))
    grid = np.arange(0.5, side - 0.5 + 1e-12, step)
    xx, yy = np.meshgrid(grid, grid)
    lattice = np.column_stack([xx.ravel(), yy.ravel()])
    centres.extend(lattice[mesh.find_simplex(lattice) < 0])
    thetas = (np.arange(angles) + 0.5) * (math.pi / 2) / angles
    rows = [(c[0], c[1], theta) for c in centres for theta in thetas]
    return np.array(rows, dtype=np.float64).reshape(-1, 3)


def _clearance(points: Array, near: npt.NDArray[np.intp], side: float, poses: Array) -> Array:
    """``min(point clearance, wall clearance)`` of poses ``(S, M, 3)`` over near ``(S, W)``."""
    x, y, theta = poses[..., 0], poses[..., 1], poses[..., 2]
    c, s = np.cos(theta)[..., None], np.sin(theta)[..., None]
    dx = points[near, 0][:, None, :] - x[..., None]
    dy = points[near, 1][:, None, :] - y[..., None]
    reach = np.maximum(np.abs(c * dx + s * dy), np.abs(c * dy - s * dx)).min(axis=-1)
    half_width = 0.5 * (np.abs(c[..., 0]) + np.abs(s[..., 0]))
    wall = np.minimum(
        np.minimum(x - half_width, side - x - half_width),
        np.minimum(y - half_width, side - y - half_width),
    )
    return np.minimum(reach - 0.5, wall)


@dataclass(frozen=True)
class SearchResult:
    starts: int
    best: float
    pose: tuple[float, float, float]


#: The 26 compass directions of pose space.
MOVES = np.array(
    [(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1) if a or b or c],
    dtype=np.float64,
)


def search_empty_square(
    p: Pattern, *, angles: int = 6, step: float = 0.25, radius: float = 2.5, chunk: int = 2048
) -> SearchResult:
    """Maximise the clearance from every start by compass search over 26 directions."""
    points = _float_points(p)
    side = float(p.side)
    starts = search_starts(p, angles=angles, step=step)
    best = (-math.inf, (0.0, 0.0, 0.0))
    for begin in range(0, len(starts), chunk):
        poses = starts[begin : begin + chunk].copy()
        distance = np.hypot(
            points[None, :, 0] - poses[:, None, 0], points[None, :, 1] - poses[:, None, 1]
        )
        width = int(max(1, (distance <= radius).sum(axis=1).max()))
        near = np.argsort(distance, axis=1)[:, :width]
        value = _clearance(points, near, side, poses[:, None, :])[:, 0]
        stride = np.full(len(poses), step / 2)
        for _ in range(4000):
            index = np.flatnonzero(stride > 1e-10)
            if not len(index):
                break
            trial = poses[index, None, :] + stride[index, None, None] * MOVES[None, :, :]
            scores = _clearance(points, near[index], side, trial)
            pick = scores.argmax(axis=1)
            gain = scores[np.arange(len(index)), pick]
            better = gain > value[index]
            moved = index[better]
            poses[moved] = trial[better, pick[better]]
            value[moved] = gain[better]
            stride[index[~better]] /= 2
        top = int(value.argmax())
        if value[top] > best[0]:
            x, y, theta = (float(v) for v in poses[top])
            best = (float(value[top]), (x, y, theta))
    return SearchResult(len(starts), best[0], best[1])


def square_from_pose(x: float, y: float, theta: float) -> Square:
    """The rational square nearest a floating pose, with an exactly unit frame."""
    return Square.from_tangent(nearest(x), nearest(y), _tangent(theta % (math.pi / 2)))


# --------------------------------------------------------------------------- certificate


@dataclass(frozen=True)
class Certification:
    side: Fraction
    certified: bool
    detail: str
    boxes: int
    seconds: float


def certify_scaled(p: Pattern, margin: Fraction = CERTIFY_MARGIN) -> Certification:
    """Certify the pattern scaled to a rational side ``<= (1 - margin) G_k``, or refuse.

    The side is rounded down to ``1e-6`` and the scaled points to the pose grid
    ``1/(10^6 2^40)`` of `cases.green17.interval_audit`, whose `certify` decides them.
    """
    from cases.green17.interval_audit import (  # noqa: PLC0415 -- only this mode needs it
        PSCALE,
        IntervalAuditError,
        certify,
    )

    side = floor_to((1 - margin) * p.side.interval()[0], 10**6)
    scale = side / p.side.midpoint()

    def grid(value: Surd) -> Fraction:
        return Fraction(round(scale * value.midpoint() * PSCALE), PSCALE)

    points = [(grid(x), grid(y)) for x, y in p.points]
    started = time.monotonic()
    try:
        stats = certify(side=side, points=points)
    except IntervalAuditError as error:
        return Certification(
            side=side,
            certified=False,
            detail=str(error),
            boxes=0,
            seconds=time.monotonic() - started,
        )
    return Certification(
        side=side,
        certified=True,
        detail=f"every closed unit square in [0, {side}]^2 contains a point; "
        f"max depth {stats.max_depth}",
        boxes=stats.boxes,
        seconds=time.monotonic() - started,
    )


# --------------------------------------------------------------------------- report


def check(
    k: int,
    *,
    certify: bool = False,
    search: bool = True,
    margin: Fraction = CERTIFY_MARGIN,
) -> dict[str, Any]:
    """Every check for one ``k``, as a JSON-ready record with a verdict."""
    p = pattern(k)
    edges = long_edges(p)
    record: dict[str, Any] = {
        "k": k,
        "n": p.n,
        "G_k": f"{float(p.side):.9f}",
        "t": f"{float(p.t):.6f}",
        "u": f"{float(p.u):.6f}",
        "m_x": f"{float(p.mx):.6f}",
        "d": f"{math.sqrt(float(2 - 2 * p.u)):.6f}",
        "identities": identities(p),
        "long_edges": len(edges),
        "long_edge_exceeds_one": long_edge_exceeds_one(p),
        "side_margin_exceeds_one": side_margin_exceeds_one(p),
    }
    escapes: list[tuple[Square, SquareCheck]] = []

    def checked(square: Square) -> dict[str, Any]:
        result = check_square(p, square)
        if result.escapes:
            escapes.append((square, result))
        return _square_record(square, result)

    if record["side_margin_exceeds_one"]:
        record["strip_square"] = checked(strip_square(p))
    if k >= 4:
        record["writeup_square"] = checked(writeup_square(p))
    if k == 4:
        record["published_square"] = checked(published_square(p))
        figure = match_figure(p, figure_gif(FIGURE.read_text(encoding="utf-8")))
        record["figure"] = {
            "gif_sha256": figure.gif_sha256,
            "is_ds7_l17_gif": figure.gif_sha256 == DS7_L17_GIF_SHA256,
            "dots": figure.dots,
            "pixels_per_unit": round(figure.pixels_per_unit, 4),
            "row_zero_drawn_at": figure.row_zero,
            "max_residual_pixels": round(figure.max_residual, 3),
            "other_way_up_residual_pixels": round(figure.other_residual, 3),
        }
    if search:
        found = search_empty_square(p)
        record["search"] = {"starts": found.starts, "best_clearance": f"{found.best:.9f}"}
        if found.best > 1e-9:
            record["search"]["square"] = checked(square_from_pose(*found.pose))
    if escapes:
        square, result = max(escapes, key=lambda pair: pair[1].slack_lower)
        grown, grown_check = widest_empty(p, square, result)
        record["ceiling"] = str(ceiling_bound(p, grown))
        record["ceiling_square"] = _square_record(grown, grown_check)
    elif certify:
        outcome = certify_scaled(p, margin)
        record["certificate"] = {
            "side": str(outcome.side),
            "certified": outcome.certified,
            "detail": outcome.detail,
            "boxes": outcome.boxes,
            "seconds": round(outcome.seconds, 1),
        }
    record["verdict"] = _verdict(record, escaped=bool(escapes))
    return record


def _square_record(square: Square, result: SquareCheck) -> dict[str, Any]:
    return {
        "centre": [str(square.x), str(square.y)],
        "cos": str(square.cos),
        "sin": str(square.sin),
        "theta_degrees": round(square.theta_degrees, 6),
        "half": str(square.half),
        "fits": result.fits,
        "empty": result.empty,
        "covered_by": list(result.covered_by),
        "wall_clearance_at_least": str(result.clearance_lower),
        "point_slack_at_least": str(result.slack_lower),
    }


def _verdict(record: dict[str, Any], *, escaped: bool) -> str:
    if not all(record["identities"].values()):
        return "pattern-mismatch"
    if escaped:
        return "fails"
    certificate = record.get("certificate")
    if certificate is not None:
        return "unavoidable-below-G_k" if certificate["certified"] else "undecided"
    return "no-empty-square-found"


def _slack(record: dict[str, Any], key: str) -> str:
    block = record.get(key)
    if not isinstance(block, dict):
        return "-"
    return f"{float(Fraction(block['point_slack_at_least'])):.9f}"


def summary_line(record: dict[str, Any]) -> str:
    return (
        f"{record['k']:>3} {record['n']:>4} {record['G_k']:>13} {record['m_x']:>9} "
        f"{record['d']:>9} {'yes' if all(record['identities'].values()) else 'NO':>4} "
        f"{record['long_edges']:>5} {_slack(record, 'writeup_square'):>12} "
        f"{record.get('search', {}).get('best_clearance', '-'):>12} "
        f"{_ceiling(record):>12}  {record['verdict']}"
    )


def _ceiling(record: dict[str, Any]) -> str:
    ceiling = record.get("ceiling")
    return "-" if ceiling is None else f"{float(Fraction(ceiling)):.6f}"


HEADER = (
    "  k    n           G_k       m_x         d  ids  long   Q_k slack  best search"
    "     ceiling  verdict"
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--k", nargs=2, type=int, default=(2, 12), metavar=("FIRST", "LAST"))
    parser.add_argument(
        "--certify",
        action="store_true",
        help="certify the scaled pattern for each k where nothing escapes",
    )
    parser.add_argument(
        "--margin",
        type=Fraction,
        default=CERTIFY_MARGIN,
        help="how far below G_k, as a fraction of it, --certify works (default 1/1000)",
    )
    parser.add_argument("--no-search", action="store_true", help="skip the float search")
    parser.add_argument("--json", type=Path, help="write the records here")
    args = parser.parse_args(argv)
    first, last = args.k
    if not 2 <= first <= last:
        parser.error("--k needs 2 <= FIRST <= LAST")
    if not 0 < args.margin < 1:
        parser.error("--margin must lie strictly between 0 and 1")
    print(HEADER)
    records = []
    for k in range(first, last + 1):
        record = check(k, certify=args.certify, search=not args.no_search, margin=args.margin)
        records.append(record)
        print(summary_line(record), flush=True)
        if "certificate" in record:
            certificate = record["certificate"]
            print(
                f"      certificate: {certificate['detail']} "
                f"({certificate['boxes']} boxes, {certificate['seconds']} s)"
            )
    if args.json:
        # One record per line keeps a receipt for k = 2..17 far below the archive's
        # 1,000-line threshold for plain retained data.
        lines = ",\n".join(json.dumps(record, sort_keys=True) for record in records)
        args.json.write_text(f"[\n{lines}\n]\n", encoding="utf-8")
    return 0 if all(r["verdict"] != "pattern-mismatch" for r in records) else 1


if __name__ == "__main__":
    sys.exit(main())
