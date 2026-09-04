"""Interval-certified decision of a weighted fractional certificate.

This is the second decision procedure for the Burns--Massaccesi certificate, and
it exists to differ from ``sqpack.fractional.certificate`` in *method*, not only
in code. The exact verifier decides ``C4`` by an event-cell decomposition in
rational arithmetic; a modelling error there -- a wrong cell set, a wrong
domain polygon -- reproduces itself exactly on every replay. This module
decides the same theorem by branch and bound over boxes of square centres in
floating-point interval arithmetic with directed rounding, whose failure modes
are different ones: an enclosure too wide to resolve, or a rounding step in the
wrong direction. Two methods that could only fail in the same way are what the
``C4`` confirmation rung exists to rule out.

What is decided. With ``n``, container side ``L``, shrink ``B``, a rational
half-tangent net ``0 = t_0 < ... < t_K < 1`` and nonnegative rational-weight
atoms:

``C1``  total atom mass is strictly below ``n``;
``C2``  the net reaches pi/4, i.e. ``t_K^2 + 2 t_K - 1 >= 0``;
``C3``  ``B (1 + D) < 1`` for ``D`` the largest half-gap tangent;
``C4``  every closed ``B``-square at a net direction lying inside ``[0, L]^2``
        covers atom mass at least 1 -- decided here over the *doubled* net,
        the ``K + 1`` directions ``theta_k`` and their reflections
        ``pi/2 - theta_k``.

``C0`` (D4 invariance of the atom multiset) is not decided, and not because it
was skipped: an equality of rationals is exactly what interval arithmetic can
never establish. It is not needed either. The exact proof uses ``C0`` only to
reflect a square at an angle past pi/4 onto the net's arc; deciding ``C4`` on
the doubled net covers every orientation in ``[0, pi/2)`` directly, so the
symmetry reduction is never invoked and the conclusion rests on strictly fewer
hypotheses. For a certificate that is D4-symmetric the two conditions coincide
in strength; for one that is not, this decision is the one that is still
sound.

Why the lower bound is a lower bound. Fix a direction with rotation ``(c, s)``
and write ``u = c x + s y``, ``v = -s x + c y`` for the rotated frame. A closed
``B``-square centred at ``p`` covers atom ``i`` exactly when ``p`` lies in the
closed axis-aligned box ``R_i = [u_i - B/2, u_i + B/2] x [v_i - B/2, v_i + B/2]``.
For a box of centres ``X``, the covered mass at *every* ``p`` in ``X`` is at
least ``sum(w_i : R_i contains X)``, because a region containing the whole box
contains each of its points. Each ``R_i`` is known only as an enclosure, so the
test is made against the *inner* box ``[hi(u_i - B/2), lo(u_i + B/2)] x ...``
that surely lies inside ``R_i``. Because every weight is nonnegative, omitting a
region that fails that test can only lower the bound. Masses are exact
nonnegative integers on a common scale, so the sum itself rounds nothing. The
bound is therefore below the true covered mass at every centre of the box, with
no assumption on the box's size.

Why the domain is handled soundly. The admissible centres are ``[h, L - h]^2``
in container coordinates, ``h = B (c + s) / 2``, which is a rotated square in
the ``(u, v)`` frame. A box is bounded on ``X`` intersected with that domain,
never on the box alone: the intersection's bounding box is enclosed by
propagating the four half-plane constraints through the box's own bounds with
outward rounding, so it is a superset of the true bounding box and the
containment test above stays a lower bound. A box whose tightened bounds cross
is provably outside the domain and is dropped. The initial box encloses the
whole domain, and every split covers its parent, so the leaves cover every
admissible centre.

Why refutation is sound. The mass at a *point* ``p`` is at most
``sum(w_i : outer box of R_i contains p)``, and ``p`` is admissible when the
enclosures of its container coordinates lie inside ``[h, L - h]``. A box centre
that passes both tests with mass below 1 is a genuine placement the certificate
does not cover.

The upper bound used for refutation has the same dependency: the regions whose
outer boxes contain ``p`` are a superset of the regions that truly contain it,
and summing a superset is an upper bound only for nonnegative weights.

What this method cannot do. A leave-edge of one region lying *exactly* on the
enter-edge of another, or a region edge passing exactly through a domain corner,
leaves a sliver no enclosure can close; the search then reaches its resolution
floor or its conservative work budget with boxes still undecided and reports
that explicitly, which is a refusal to accept and never an acceptance. The seam
census in ``tests/test_fractional_interval.py`` finds no such coincidence in the
retained certificates, and the full-net searches report no stalled box or
exhausted budget.
"""

from __future__ import annotations

import math
from collections.abc import Iterator
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import pairwise
from typing import Literal

import numpy as np
from numpy.typing import NDArray

from sqpack.fractional.certificate import Certificate

Floats = NDArray[np.float64]
Ints = NDArray[np.int64]

Status = Literal["holds", "fails", "undecided"]


class IntervalInputError(ValueError):
    """The certificate lies outside the interval verifier's safe input domain."""


# Boxes narrower than this in both axes are not split further. Region edges are
# enclosed to a few ulps of their magnitude (about 1e-15 here); a box thinner than
# the fuzz cannot be told apart from the edge it straddles, so splitting it would
# loop forever. A valid certificate never needs boxes this thin unless two edges
# coincide to within the fuzz, which is the case the module docstring describes.
RESOLUTION_FLOOR = 1e-12

# Boxes are bounded in batches so the per-atom comparisons run as one array
# operation per batch. The size trades Python overhead against memory: each
# batch holds a boxes-by-atoms boolean mask.
BATCH = 4096

# Refuse a direction rather than let an unresolvable seam tile a continuum down
# to RESOLUTION_FLOOR. The budget is a per-direction diagnostic limit; retained
# certificates remain below it, and the validator records the total boxes examined.
BOX_BUDGET = 100_000

# Every NumPy mass operation is an int64 sum of a subset of the atom masses.
# Keeping the exact Python-integer total below this conservative limit makes
# each such accumulation safe, with room below the signed-int64 boundary.
INT64_MASS_LIMIT = 2**62

# Each search batch materialises boxes-by-atoms masks. The retained maximum is 2,097,
# whose 4,096-by-2,097 boolean mask is about 8.2 MiB. The hard 4,096-atom limit leaves
# nearly twofold research headroom and caps one such mask at 16 MiB rather than allowing
# an input-driven multi-gigabyte allocation.
MAX_INTERVAL_ATOMS = 4096


# ---------------------------------------------------------------------------
# Scalar and vector interval arithmetic with directed rounding.
#
# Every arithmetic result is rounded to nearest by the hardware; the true value
# then lies between the two floats adjacent to the result, so stepping one ulp
# outward on each side is a rigorous enclosure of a single operation. Nothing
# here relies on a global rounding mode, which Python cannot set.
# ---------------------------------------------------------------------------


def _down(values: Floats) -> Floats:
    return np.nextafter(values, -np.inf)


def _up(values: Floats) -> Floats:
    return np.nextafter(values, np.inf)


def _require_finite(*values: Floats) -> None:
    if not all(np.isfinite(value).all() for value in values):
        raise IntervalInputError(
            "interval operation cannot be enclosed by finite float arithmetic"
        )


def _add(alo: Floats, ahi: Floats, blo: Floats, bhi: Floats) -> tuple[Floats, Floats]:
    with np.errstate(over="ignore", invalid="ignore"):
        low, high = _down(alo + blo), _up(ahi + bhi)
    _require_finite(low, high)
    return low, high


def _sub(alo: Floats, ahi: Floats, blo: Floats, bhi: Floats) -> tuple[Floats, Floats]:
    with np.errstate(over="ignore", invalid="ignore"):
        low, high = _down(alo - bhi), _up(ahi - blo)
    _require_finite(low, high)
    return low, high


def _mul(alo: Floats, ahi: Floats, blo: Floats, bhi: Floats) -> tuple[Floats, Floats]:
    """Sign-agnostic: the extreme products among the four corner pairs."""
    with np.errstate(over="ignore", invalid="ignore"):
        products = (alo * blo, alo * bhi, ahi * blo, ahi * bhi)
        _require_finite(*products)
        low = np.minimum(
            np.minimum(products[0], products[1]), np.minimum(products[2], products[3])
        )
        high = np.maximum(
            np.maximum(products[0], products[1]), np.maximum(products[2], products[3])
        )
        low, high = _down(low), _up(high)
    _require_finite(low, high)
    return low, high


def _div(alo: Floats, ahi: Floats, blo: Floats, bhi: Floats) -> tuple[Floats, Floats]:
    """Division by an interval that is strictly positive; the caller guarantees it."""
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        quotients = (alo / blo, alo / bhi, ahi / blo, ahi / bhi)
        _require_finite(*quotients)
        low = np.minimum(
            np.minimum(quotients[0], quotients[1]), np.minimum(quotients[2], quotients[3])
        )
        high = np.maximum(
            np.maximum(quotients[0], quotients[1]), np.maximum(quotients[2], quotients[3])
        )
        low, high = _down(low), _up(high)
    _require_finite(low, high)
    return low, high


@dataclass(frozen=True, slots=True)
class Interval:
    """A closed interval of floats known to contain one real number."""

    lo: float
    hi: float

    def __post_init__(self) -> None:
        if not (math.isfinite(self.lo) and math.isfinite(self.hi)):
            raise IntervalInputError(
                "certificate arithmetic cannot be enclosed by finite floats"
            )
        if self.lo > self.hi:
            raise ValueError(f"not an interval: [{self.lo}, {self.hi}]")

    @classmethod
    def of(cls, value: Fraction | int) -> Interval:
        """The tightest float enclosure of a rational.

        ``float(Fraction)`` is correctly rounded, so the enclosure is that float
        widened by one ulp on the side the rational actually lies. This is the
        one place exact rational comparison is used: the data enters as
        rationals and has to be enclosed before interval arithmetic can start.
        """
        exact = Fraction(value)
        try:
            nearest = float(exact)
        except OverflowError:
            raise IntervalInputError(
                "exact certificate input is outside the finite float range"
            ) from None
        if not math.isfinite(nearest):
            raise IntervalInputError(
                "exact certificate input is outside the finite float range"
            )
        if Fraction(nearest) == exact:
            lo, hi = nearest, nearest
        elif Fraction(nearest) < exact:
            lo, hi = nearest, math.nextafter(nearest, math.inf)
        else:
            lo, hi = math.nextafter(nearest, -math.inf), nearest
        if not (math.isfinite(lo) and math.isfinite(hi)):
            raise IntervalInputError(
                "exact certificate input cannot be enclosed by finite floats"
            )
        return cls(lo, hi)

    def arrays(self) -> tuple[Floats, Floats]:
        return np.array([self.lo]), np.array([self.hi])

    def __add__(self, other: Interval) -> Interval:
        with np.errstate(over="ignore", invalid="ignore"):
            lo, hi = _add(*self.arrays(), *other.arrays())
        return Interval(float(lo[0]), float(hi[0]))

    def __sub__(self, other: Interval) -> Interval:
        with np.errstate(over="ignore", invalid="ignore"):
            lo, hi = _sub(*self.arrays(), *other.arrays())
        return Interval(float(lo[0]), float(hi[0]))

    def __mul__(self, other: Interval) -> Interval:
        with np.errstate(over="ignore", invalid="ignore"):
            lo, hi = _mul(*self.arrays(), *other.arrays())
        return Interval(float(lo[0]), float(hi[0]))

    def __truediv__(self, other: Interval) -> Interval:
        if other.lo <= 0:
            raise ZeroDivisionError("interval division needs a strictly positive divisor")
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            lo, hi = _div(*self.arrays(), *other.arrays())
        return Interval(float(lo[0]), float(hi[0]))

    @property
    def width(self) -> float:
        return self.hi - self.lo


ONE = Interval(1.0, 1.0)
TWO = Interval(2.0, 2.0)


# ---------------------------------------------------------------------------
# The direction net.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Rotation:
    """An enclosure of ``(cos theta, sin theta)`` for one net direction.

    Both components are non-negative and the cosine is strictly positive for
    every direction the doubled net produces, which the domain bounds rely on.
    """

    label: str
    cosine: Interval
    sine: Interval

    def __post_init__(self) -> None:
        if self.cosine.lo <= 0 or self.sine.lo < 0:
            raise IntervalInputError(f"direction {self.label} is outside the first quadrant")


def rotation_from_half_tangent(label: str, tangent: Fraction) -> Rotation:
    """``theta = 2 arctan t``: cos = (1 - t^2) / (1 + t^2), sin = 2t / (1 + t^2)."""
    if tangent < 0 or tangent >= 1:
        raise IntervalInputError(f"half-tangent {tangent} is outside [0, 1)")
    t = Interval.of(tangent)
    square = t * t
    denominator = ONE + square
    sine = (TWO * t) / denominator
    # ``t >= 0`` exactly makes the sine non-negative; the enclosure of an exact
    # zero still steps one ulp below it, and intersecting with a known fact is
    # rigorous where widening the guard would not be.
    return Rotation(label, (ONE - square) / denominator, Interval(max(sine.lo, 0.0), sine.hi))


def doubled_net(half_tangents: tuple[Fraction, ...]) -> tuple[Rotation, ...]:
    """The net and its reflection across the diagonal, so no symmetry is assumed.

    ``pi/2 - theta`` has cosine ``sin theta`` and sine ``cos theta``: the
    reflection is a swap of enclosures, not new arithmetic. The reflection of
    ``theta_0 = 0`` is a quarter turn, which is the same square as the upright
    one, so it is omitted rather than checked twice.
    """
    forward = tuple(
        rotation_from_half_tangent(str(index), tangent)
        for index, tangent in enumerate(half_tangents)
    )
    mirrored = tuple(
        Rotation(f"{rotation.label}'", rotation.sine, rotation.cosine)
        for rotation in forward[1:]
    )
    return forward + mirrored


# ---------------------------------------------------------------------------
# One direction: the branch-and-bound search over boxes of centres.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DirectionOutcome:
    """The verdict of one direction's search, on the certificate's mass scale."""

    label: str
    status: Literal["certified", "refuted", "undecided"]
    lower: int | None
    upper: int | None
    witness: tuple[float, float] | None
    boxes: int
    stalled: int
    budget_exhausted: bool = False


@dataclass(frozen=True, slots=True)
class AtomData:
    """The atoms as coordinate enclosures and exact integer masses."""

    xlo: Floats
    xhi: Floats
    ylo: Floats
    yhi: Floats
    mass: Ints
    scale: int
    total: int

    @classmethod
    def of(cls, certificate: Certificate) -> AtomData:
        if len(certificate.atoms) > MAX_INTERVAL_ATOMS:
            raise IntervalInputError(
                f"the interval verifier supports at most {MAX_INTERVAL_ATOMS} atoms"
            )
        scale, scaled_mass, total = scaled_atom_masses(certificate)
        xs = [Interval.of(atom.x) for atom in certificate.atoms]
        ys = [Interval.of(atom.y) for atom in certificate.atoms]
        return cls(
            xlo=np.array([x.lo for x in xs]),
            xhi=np.array([x.hi for x in xs]),
            ylo=np.array([y.lo for y in ys]),
            yhi=np.array([y.hi for y in ys]),
            mass=np.array(scaled_mass, dtype=np.int64),
            scale=scale,
            total=total,
        )


def scaled_atom_masses(certificate: Certificate) -> tuple[int, list[int], int]:
    """Return exact integer masses, refusing before a common scale can explode."""

    scale = 1
    for atom in certificate.atoms:
        scale = math.lcm(scale, atom.weight.denominator)
        if certificate.n * scale >= INT64_MASS_LIMIT:
            raise IntervalInputError("the weight scale is too large for exact integer masses")
    scaled_mass = [int(atom.weight * scale) for atom in certificate.atoms]
    if any(mass < 0 for mass in scaled_mass):
        raise IntervalInputError("the interval verifier requires nonnegative atom weights")
    total = sum(scaled_mass)
    if total >= INT64_MASS_LIMIT:
        raise IntervalInputError(
            "the total scaled atom mass is too large for safe int64 arithmetic"
        )
    return scale, scaled_mass, total


class DirectionSearch:
    """Branch and bound over centre boxes for one rotation.

    Boxes live in the rotated ``(u, v)`` frame, where every coverage region is
    axis-aligned; the admissible domain is the rotated container square, met
    through the bound propagation in ``tighten``.
    """

    def __init__(
        self,
        atoms: AtomData,
        rotation: Rotation,
        outer_side: Interval,
        square_side: Interval,
    ) -> None:
        self.label = rotation.label
        self.mass = atoms.mass
        self.scale = atoms.scale
        self.cosine = rotation.cosine
        self.sine = rotation.sine
        cos = rotation.cosine.arrays()
        sin = rotation.sine.arrays()
        half = square_side / TWO
        # Rotated atom positions, then the inner and outer enclosures of each
        # region. Inner is what a box must lie within to count an atom; outer is
        # what a point must lie within to possibly be covered by it.
        ulo, uhi = _add(*_mul(*cos, atoms.xlo, atoms.xhi), *_mul(*sin, atoms.ylo, atoms.yhi))
        vlo, vhi = _sub(*_mul(*cos, atoms.ylo, atoms.yhi), *_mul(*sin, atoms.xlo, atoms.xhi))
        u_low = _sub(ulo, uhi, *half.arrays())
        u_high = _add(ulo, uhi, *half.arrays())
        v_low = _sub(vlo, vhi, *half.arrays())
        v_high = _add(vlo, vhi, *half.arrays())
        self.inner = (u_low[1], u_high[0], v_low[1], v_high[0])
        self.outer = (u_low[0], u_high[1], v_low[0], v_high[1])
        if not all(np.isfinite(bound).all() for bound in (*self.inner, *self.outer)):
            raise IntervalInputError(
                "atom geometry cannot be enclosed by finite float arithmetic"
            )
        # The domain [h, L - h]^2 in container coordinates.
        self.margin = square_side * (rotation.cosine + rotation.sine) / TWO
        self.far = outer_side - self.margin
        if self.far.lo <= self.margin.hi:
            raise IntervalInputError("the square does not fit the container at this direction")
        h, far = self.margin, self.far
        # Its bounding box in the rotated frame: with both rotation components
        # non-negative, u is extreme at the near and far corners and v at the
        # two off-diagonal corners.
        u_min = (rotation.cosine + rotation.sine) * h
        u_max = (rotation.cosine + rotation.sine) * far
        v_min = rotation.cosine * h - rotation.sine * far
        v_max = rotation.cosine * far - rotation.sine * h
        self.initial = np.array([[u_min.lo, u_max.hi, v_min.lo, v_max.hi]])
        if not np.isfinite(self.initial).all():
            raise IntervalInputError(
                "search domain cannot be enclosed by finite float arithmetic"
            )

    def tighten(self, boxes: Floats) -> Floats:
        """Enclose the bounding box of each box's intersection with the domain.

        Each container constraint, say ``c u - s v >= h``, is solved for one
        rotated coordinate with the other replaced by the box bound that makes
        the inequality weakest, e.g. ``u >= (h + s v) / c >= (h + s c_lo) / c``.
        The result is a superset of the true bounding box, and two passes let
        a bound tightened from one constraint sharpen the others. A box whose
        bounds cross has no admissible centre.
        """
        a, b, c, d = (boxes[:, i].copy() for i in range(4))
        cos, sin = self.cosine.arrays(), self.sine.arrays()
        h, far = self.margin.arrays(), self.far.arrays()
        for _ in range(2):
            # From x >= h and x <= L - h, bounds on u; from y, bounds on v.
            a = np.maximum(a, _div(*_add(*h, *_mul(*sin, c, c)), *cos)[0])
            b = np.minimum(b, _div(*_add(*far, *_mul(*sin, d, d)), *cos)[1])
            c = np.maximum(c, _div(*_sub(*h, *_mul(*sin, b, b)), *cos)[0])
            d = np.minimum(d, _div(*_sub(*far, *_mul(*sin, a, a)), *cos)[1])
            if self.sine.lo > 0:
                # The same constraints solved the other way round need sin > 0.
                a = np.maximum(a, _div(*_sub(*h, *_mul(*cos, d, d)), *sin)[0])
                b = np.minimum(b, _div(*_sub(*far, *_mul(*cos, c, c)), *sin)[1])
                c = np.maximum(c, _div(*_sub(*_mul(*cos, a, a), *far), *sin)[0])
                d = np.minimum(d, _div(*_sub(*_mul(*cos, b, b), *h), *sin)[1])
        return np.stack([a, b, c, d], axis=1)

    def admissible(self, u: Floats, v: Floats) -> NDArray[np.bool_]:
        """Points whose container coordinates provably lie in ``[h, L - h]^2``."""
        cos, sin = self.cosine.arrays(), self.sine.arrays()
        xlo, xhi = _sub(*_mul(*cos, u, u), *_mul(*sin, v, v))
        ylo, yhi = _add(*_mul(*sin, u, u), *_mul(*cos, v, v))
        return (
            (xlo >= self.margin.hi)
            & (xhi <= self.far.lo)
            & (ylo >= self.margin.hi)
            & (yhi <= self.far.lo)
        )

    def lower_bound(self, boxes: Floats) -> Ints:
        """Mass of the atoms whose inner region contains the whole box."""
        ulo, uhi, vlo, vhi = self.inner
        a, b, c, d = (boxes[:, i : i + 1] for i in range(4))
        contains = (ulo <= a) & (b <= uhi) & (vlo <= c) & (d <= vhi)
        return contains @ self.mass

    def upper_bound_at(self, u: Floats, v: Floats) -> Ints:
        """Mass of the atoms whose outer region contains the point."""
        ulo, uhi, vlo, vhi = self.outer
        uu, vv = u[:, None], v[:, None]
        meets = (ulo <= uu) & (uu <= uhi) & (vlo <= vv) & (vv <= vhi)
        return meets @ self.mass

    def _split(self, boxes: Floats) -> tuple[Floats, Floats]:
        """Bisect each box across the axis with more region edges inside it.

        A box fails to certify because some regions cover only part of it, so the
        useful split is the one that separates their edges: an axis with no edge
        strictly inside the box is never split, because both children would count
        exactly the atoms the parent did. That holds at the domain boundary too --
        the intersection with the domain is handled by ``tighten``, and a strip
        along the boundary with no edge inside already carries its cell's mass. A
        box that can be split along neither axis is stalled: it is thinner than
        the resolution floor across every seam it straddles, and returned as
        undecided rather than sliced along its length forever, which an earlier
        version of this rule did at a boundary that coincided with a region edge.
        """
        # Inner edges, because those are the ones a child must clear to count an
        # atom the parent could not; the outer ones matter only to point bounds.
        ulo, uhi, vlo, vhi = self.inner
        a, b, c, d = (boxes[:, i : i + 1] for i in range(4))
        u_edges = (((a < ulo) & (ulo < b)) | ((a < uhi) & (uhi < b))).sum(axis=1)
        v_edges = (((c < vlo) & (vlo < d)) | ((c < vhi) & (vhi < d))).sum(axis=1)
        width_u = boxes[:, 1] - boxes[:, 0]
        width_v = boxes[:, 3] - boxes[:, 2]
        can_u = (width_u > RESOLUTION_FLOOR) & (u_edges > 0)
        can_v = (width_v > RESOLUTION_FLOOR) & (v_edges > 0)
        prefer_u = (u_edges > v_edges) | ((u_edges == v_edges) & (width_u >= width_v))
        along_u = can_u & (prefer_u | ~can_v)
        along_v = can_v & ~along_u
        stalled = boxes[~(along_u | along_v)]
        children: list[Floats] = []
        if along_u.any():
            chosen = boxes[along_u]
            mid = (chosen[:, 0] + chosen[:, 1]) / 2
            left = chosen.copy()
            left[:, 1] = mid
            right = chosen.copy()
            right[:, 0] = mid
            children += [left, right]
        if along_v.any():
            chosen = boxes[along_v]
            mid = (chosen[:, 2] + chosen[:, 3]) / 2
            low = chosen.copy()
            low[:, 3] = mid
            high = chosen.copy()
            high[:, 2] = mid
            children += [low, high]
        if not children:
            return np.empty((0, 4)), stalled
        return np.concatenate(children), stalled

    def search(self, *, prune_at: int | None) -> DirectionOutcome:
        """Bound the least covered mass over the admissible centres.

        With ``prune_at`` given, a box is settled once its lower bound reaches
        it, which decides ``mass >= prune_at`` everywhere and stops early on a
        counterexample. Without it, boxes are settled against the best point
        value seen so far, which encloses the minimum itself. Exhausting the
        work budget returns a conservative ``undecided`` outcome with lower
        bound zero, unless an admissible sampled point already refutes ``C4``.
        Nonnegative weights make zero valid for every abandoned box.
        """
        pending: list[Floats] = [self.initial]
        lower: int | None = None
        upper: int | None = None
        witness: tuple[float, float] | None = None
        boxes = 0
        stuck_bounds: list[int] = []
        while pending:
            batch = pending.pop()
            if len(batch) > BATCH:
                pending.append(batch[BATCH:])
                batch = batch[:BATCH]
            tight = self.tighten(batch)
            if not np.isfinite(tight).all():
                raise IntervalInputError(
                    "search bounds cannot be enclosed by finite float arithmetic"
                )
            tight = tight[(tight[:, 0] <= tight[:, 1]) & (tight[:, 2] <= tight[:, 3])]
            boxes += len(tight)
            if not len(tight):
                continue
            low = self.lower_bound(tight)
            cu = (tight[:, 0] + tight[:, 1]) / 2
            cv = (tight[:, 2] + tight[:, 3]) / 2
            admissible = self.admissible(cu, cv)
            if admissible.any():
                high = self.upper_bound_at(cu[admissible], cv[admissible])
                best = int(high.argmin())
                if upper is None or int(high[best]) < upper:
                    upper = int(high[best])
                    witness = (float(cu[admissible][best]), float(cv[admissible][best]))
                    if prune_at is not None and upper < prune_at:
                        stalled = sum(1 for value in stuck_bounds if value < prune_at)
                        return DirectionOutcome(
                            self.label, "refuted", None, upper, witness, boxes, stalled
                        )
            threshold = prune_at if prune_at is not None else upper
            settled = (
                np.zeros(len(tight), dtype=bool) if threshold is None else low >= threshold
            )
            if settled.any():
                least = int(low[settled].min())
                lower = least if lower is None else min(lower, least)
            unresolved = tight[~settled]
            if boxes >= BOX_BUDGET and (len(unresolved) or pending):
                budget_status: Literal["refuted", "undecided"] = (
                    "refuted" if upper is not None and upper < self.scale else "undecided"
                )
                budget_stalled = sum(
                    1 for value in stuck_bounds if threshold is None or value < threshold
                )
                return DirectionOutcome(
                    self.label,
                    budget_status,
                    0,
                    upper,
                    witness,
                    boxes,
                    budget_stalled,
                    budget_exhausted=True,
                )
            children, stuck = self._split(unresolved)
            if len(stuck):
                stuck_bounds.extend(int(value) for value in self.lower_bound(stuck))
            if len(children):
                pending.append(children)
        if stuck_bounds:
            lower = min(stuck_bounds) if lower is None else min(lower, *stuck_bounds)
        # A box stalls against the threshold in force when it is reached; without
        # ``prune_at`` that threshold is the best point value so far, which the
        # search keeps lowering. Judged against the final one, a box whose bound
        # already reaches it cannot hide a smaller value and is no stall at all.
        final = prune_at if prune_at is not None else upper
        stalled = sum(1 for value in stuck_bounds if final is None or value < final)
        if upper is not None and upper < self.scale:
            status: Literal["certified", "refuted", "undecided"] = "refuted"
        elif stalled == 0 and lower is not None and lower >= self.scale:
            status = "certified"
        else:
            status = "undecided"
        return DirectionOutcome(self.label, status, lower, upper, witness, boxes, stalled)


# ---------------------------------------------------------------------------
# The whole certificate.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class IntervalCondition:
    name: str
    detail: str
    status: Status = field(kw_only=True)

    @property
    def holds(self) -> bool:
        return self.status == "holds"


@dataclass(frozen=True, slots=True)
class IntervalVerdict:
    conditions: tuple[IntervalCondition, ...]
    directions: tuple[DirectionOutcome, ...]
    scale: int
    total_mass: Fraction

    @property
    def accepted(self) -> bool:
        return all(condition.holds for condition in self.conditions)

    @property
    def failures(self) -> tuple[str, ...]:
        return tuple(c.name for c in self.conditions if not c.holds)

    @property
    def enclosure(self) -> tuple[Fraction, Fraction] | None:
        """``[lower, upper]`` on the least covered mass over every direction searched.

        The lower end is the least box bound over all leaves of every search
        and the upper end the least admissible point value, both exact on the
        mass scale; the minimum lies between them. ``None`` when a direction
        was refuted before either bound was established.
        """
        lows = [d.lower for d in self.directions if d.lower is not None]
        highs = [d.upper for d in self.directions if d.upper is not None]
        if not lows or not highs or len(lows) != len(self.directions):
            return None
        return Fraction(min(lows), self.scale), Fraction(min(highs), self.scale)


def _condition_mass_below_n(certificate: Certificate, atoms: AtomData) -> IntervalCondition:
    total = atoms.total
    return IntervalCondition(
        "C1 total mass below n",
        f"total {Fraction(total, atoms.scale)} against n = {certificate.n}, exact integers",
        status="holds" if total < certificate.n * atoms.scale else "fails",
    )


def _strict_sign(value: Interval, *, want_positive: bool) -> Status:
    """Decide the sign of an enclosed real; straddling zero decides nothing."""
    if want_positive:
        if value.lo >= 0:
            return "holds"
        return "fails" if value.hi < 0 else "undecided"
    if value.hi < 0:
        return "holds"
    return "fails" if value.lo >= 0 else "undecided"


def _condition_net_reaches_eighth_turn(certificate: Certificate) -> IntervalCondition:
    """``t_K >= tan(pi/8)`` as the sign of ``t_K^2 + 2 t_K - 1``, enclosed."""
    last = Interval.of(certificate.half_tangents[-1])
    slack = last * last + TWO * last - ONE
    return IntervalCondition(
        "C2 net reaches pi/4",
        f"t_K^2 + 2 t_K - 1 in [{slack.lo:.3e}, {slack.hi:.3e}]",
        status=_strict_sign(slack, want_positive=True),
    )


def _condition_containment(certificate: Certificate) -> IntervalCondition:
    """``B (1 + D) < 1`` with ``D`` the largest half-gap tangent, all enclosed."""
    gaps = [
        (Interval.of(right) - Interval.of(left))
        / (ONE + Interval.of(left) * Interval.of(right))
        for left, right in pairwise(certificate.half_tangents)
    ]
    largest = Interval(max(g.lo for g in gaps), max(g.hi for g in gaps))
    product = Interval.of(certificate.square_side) * (ONE + largest)
    return IntervalCondition(
        "C3 containment B(1 + D) < 1",
        f"B(1 + D) in [{product.lo:.12f}, {product.hi:.12f}]",
        status=_strict_sign(product - ONE, want_positive=False),
    )


def searches(certificate: Certificate, atoms: AtomData) -> Iterator[DirectionSearch]:
    outer = Interval.of(certificate.outer_side)
    square = Interval.of(certificate.square_side)
    for rotation in doubled_net(certificate.half_tangents):
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            search = DirectionSearch(atoms, rotation, outer, square)
        yield search


def verify_by_intervals(
    certificate: Certificate,
    *,
    enclose: bool = False,
    directions: tuple[str, ...] | None = None,
) -> IntervalVerdict:
    """Decide the certificate; ``enclose`` also pins the least covered mass.

    ``directions`` restricts the searches to named labels of the doubled net.
    Such a run remains a useful diagnostic: a selected direction can refute
    ``C4``, and certified outcomes and enclosures describe those directions.
    It cannot establish ``C4`` or produce an accepted theorem verdict; omit
    ``directions`` to decide the full doubled net.

    """
    if any(t >= 1 for t in certificate.half_tangents):
        raise IntervalInputError(
            "half-tangents must stay below 1 so the net stays inside a quarter turn"
        )
    atoms = AtomData.of(certificate)
    conditions = [
        _condition_mass_below_n(certificate, atoms),
        _condition_net_reaches_eighth_turn(certificate),
        _condition_containment(certificate),
    ]
    outcomes: list[DirectionOutcome] = []
    for search in searches(certificate, atoms):
        if directions is not None and search.label not in directions:
            continue
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            outcome = search.search(prune_at=None if enclose else atoms.scale)
        outcomes.append(outcome)
        if outcomes[-1].status == "refuted":
            break
    if any(
        outcome.status == "refuted"
        or (outcome.upper is not None and outcome.upper < atoms.scale)
        for outcome in outcomes
    ):
        status: Status = "fails"
    elif (
        directions is None
        and outcomes
        and all(
            outcome.status == "certified"
            and outcome.lower is not None
            and outcome.lower >= atoms.scale
            for outcome in outcomes
        )
    ):
        status = "holds"
    else:
        status = "undecided"
    worst = min(
        (o for o in outcomes if o.upper is not None), key=lambda o: o.upper or 0, default=None
    )
    detail = (
        f"{len(outcomes)} directions, {sum(o.boxes for o in outcomes)} boxes, "
        f"{sum(o.stalled for o in outcomes)} stalled, "
        f"{sum(o.budget_exhausted for o in outcomes)} budget-exhausted"
    )
    if worst is not None and worst.upper is not None:
        detail += f"; least point mass {Fraction(worst.upper, atoms.scale)} at {worst.label}"
    if directions is not None:
        detail += "; restricted diagnostic, full doubled net not decided"
    conditions.append(
        IntervalCondition("C4 every admissible centre covers mass 1", detail, status=status)
    )
    return IntervalVerdict(
        tuple(conditions), tuple(outcomes), atoms.scale, Fraction(atoms.total, atoms.scale)
    )
