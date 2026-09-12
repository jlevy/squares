"""Interval-certified decision of a threshold certificate.

This is the second decision procedure for the threshold-certificate theorem of
`sqpack.fractional.threshold`, and it exists to differ from that module's exact sweep in
*method*. The sweep decides ``Condition 5'`` on an event grid built from every atom
point, with each threshold atom expanded by inclusion--exclusion into signed rectangle
terms of one integer difference array; a modelling error there -- a wrong cell set, a
wrong expansion coefficient, a wrong domain polygon -- reproduces itself exactly on every
replay. This module decides the same condition by branch and bound over boxes of square
centres in floating-point interval arithmetic with directed rounding, never expands a
threshold atom into anything, and counts instead: a threshold atom ``(S, k, w)`` charges
``w`` to a box when at least ``k`` of its points are *provably* inside every core the box
names. Its failure modes are an enclosure too wide to resolve, a rounding step in the
wrong direction, or a member table that names the wrong sites -- none of which is a
failure mode of the sweep. Two methods that could only fail in the same way are what the
``C4`` confirmation rung exists to rule out.

What is decided. With ``n``, container side ``L``, shrink ``B``, a rational half-tangent
net ``0 = t_0 < ... < t_K < 1``, nonnegative rational-weight point atoms and threshold
atoms ``(S, k, w)``:

``Condition 2'`` the total budget -- point mass plus ``w floor(|S| / k)`` over the
        threshold atoms -- is strictly below ``n``, decided in exact integers;
``Condition 3``  the net reaches pi/4, i.e. ``t_K^2 + 2 t_K - 1 >= 0``;
``Condition 4``  ``B (1 + D) < 1`` for ``D`` the largest half-gap tangent;
``Condition 5'`` every closed ``B``-square at a net direction lying inside ``[0, L]^2``
        is charged at least 1 -- decided here over the *doubled* net, the ``K + 1``
        directions ``theta_k`` and their reflections ``pi/2 - theta_k``.

``Condition 1'`` (D4 invariance of the point atoms and of the threshold atoms) is not
decided, for the reason `sqpack.fractional.interval` gives: an equality of rationals is
what interval arithmetic can never establish, and it is not needed, because deciding
``Condition 5'`` on the doubled net covers every orientation in ``[0, pi/2)`` directly
and the reflection argument is never invoked. The conclusion rests on strictly fewer
hypotheses than the sweep's.

Why the lower bound is a lower bound. Fix a direction with rotation ``(c, s)`` and the
rotated frame ``u = c x + s y``, ``v = -s x + c y``. The closed ``B``-square centred at
``p`` contains the point ``q`` exactly when ``p`` lies in the closed axis-aligned box
``R_q = [u_q - B/2, u_q + B/2] x [v_q - B/2, v_q + B/2]``. For a box of centres ``X``
let ``H(X)`` be the set of atom points whose *inner* enclosure of ``R_q`` -- the box
``[hi(u_q - B/2), lo(u_q + B/2)] x ...`` that surely lies inside ``R_q`` -- contains
the whole of ``X``. Every core centred in ``X`` then contains every point of ``H(X)``,
so its trace on ``S`` has at least ``|H(X) ∩ S|`` points, and the charge
``w [|trace ∩ S| >= k]`` is monotone in the trace: it is at least
``w [|H(X) ∩ S| >= k]``. Summed over atoms with nonnegative weights this is a lower
bound on the charge at *every* centre in ``X``, with no assumption on the size of ``X``.
A point whose region is only partly resolved against the box is not in ``H(X)`` and is
dropped rather than assumed, which can only lower the bound. Point atoms are the case
``|S| = k = 1``, where the bound is the point route's own. Weights are exact nonnegative
integers on a common scale, so the sum itself rounds nothing.

The upper bound used for refutation has the same shape the other way round: the points
whose *outer* enclosures contain a centre ``p`` are a superset of the points its core
contains, so ``w [|outer trace ∩ S| >= k]`` is at least the true charge of that atom at
``p``, and the sum is an upper bound. A provably admissible centre whose upper bound is
below 1 is a genuine placement the certificate does not charge, and the search reports
it as a refutation; `exact_charge_at_witness` then re-evaluates the charge at that
centre in rational arithmetic, by membership counting, so that a refutation is never
taken on the floats' word either.

What is shared and what is not. The box search -- the domain tightening, the admissibility
test, the split rule, the resolution floor, the box budget and the stall accounting -- is
`sqpack.fractional.interval.DirectionSearch`'s, inherited unchanged; only the two bounds
are this module's, and on a certificate with no threshold atom they reduce, number for
number, to the point route's. With the exact sweep this route shares the
`ThresholdCertificate` object, the meaning of a charge, and the closed-form formulas of
Conditions 2', 3 and 4; it shares no part of the ``Condition 5'`` decision: not the
event grid, not the span reduction, not the expansion, not the prefix sums, not the
witness construction.

What this method cannot do. A leave-edge of one point's region lying *exactly* on the
enter-edge of another -- for a threshold atom, two of its points at distance exactly
``B`` along an axis of the rotated frame, so that one leaves the core as the other enters
and the charge is constant across a seam no box can straddle -- or a region edge through
a domain corner, leaves a sliver no enclosure can close; the search reaches its
resolution floor with the box still undecided and reports it as such, a refusal to
accept and never an acceptance. The tests exhibit exactly that seam and hold the verdict
to ``undecided``.
"""

# The closed-form Conditions 3 and 4 are the point route's own enclosures, imported rather
# than retyped so there is one formula and one enclosure of each; the pattern
# `sqpack.fractional.threshold` set for the sweep's witness.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import multiprocessing as mp
import sys
from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from fractions import Fraction
from functools import partial
from math import lcm

import numpy as np
from numpy.typing import NDArray

from sqpack.fractional.interval import (
    INT64_MASS_LIMIT,
    MAX_INTERVAL_ATOMS,
    AtomData,
    DirectionOutcome,
    DirectionSearch,
    Interval,
    IntervalCondition,
    IntervalInputError,
    Rotation,
    Status,
    _condition_containment,
    _condition_net_reaches_eighth_turn,
    doubled_net,
)
from sqpack.fractional.threshold import Point, ThresholdCertificate

Floats = NDArray[np.float64]
Ints = NDArray[np.int64]

# Each search batch gathers one boolean per (box, atom, member slot) before it counts, a
# block of BATCH rows by this many columns, and then holds one int16 count per (box, atom).
# The cap keeps the gathered block at twice the point route's mask bound and the count
# block under it; an input past it is refused before any array exists.
MAX_MEMBER_SLOTS = 2 * MAX_INTERVAL_ATOMS
#: Tokens per atom. `_counts` sums a member row into one `int16`, so a row has to stay
#: inside that lane; this cap is far above any admitted atom and exists so a weighted
#: atom fails loudly rather than overflowing a count.
MAX_TOKENS_PER_ATOM = 4096

CONDITION_5 = "Condition 5' every admissible centre is charged at least 1"


@dataclass(frozen=True, slots=True)
class ThresholdAtomData:
    """The atoms as a member table over distinct sites, with exact integer weights.

    ``sites`` holds every distinct atom point as a coordinate enclosure; its per-site mass
    is zero, because mass lives on the atoms here, not on the sites. Row ``a`` of
    ``members`` lists the site indices of atom ``a`` -- a point atom is one site, a
    threshold atom its points -- padded to the table's width with ``len(sites)``, an index
    that every gathered mask carries as a column of ``False``. ``thresholds[a]`` is the
    ``k`` of atom ``a`` (``1`` for a point atom) and ``mass[a]`` its weight on ``scale``.
    ``budget`` is ``Condition 2'``'s quantity on the same scale, summed in Python
    integers.
    """

    sites: AtomData
    members: NDArray[np.intp]
    thresholds: NDArray[np.int16]
    mass: Ints
    scale: int
    budget: int
    point_count: int
    threshold_count: int

    @classmethod
    def of(cls, certificate: ThresholdCertificate) -> ThresholdAtomData:
        scale, point_masses, threshold_masses, budget = scaled_threshold_masses(certificate)
        index: dict[Point, int] = {}

        def site(point: Point) -> int:
            return index.setdefault(point, len(index))

        rows: list[list[int]] = [[site((atom.x, atom.y))] for atom in certificate.atoms]
        # One slot per TOKEN, repeating a site's index for each of its tokens. The boolean
        # gather at `_counts` then sums tokens rather than sites, while the interval
        # enclosure below is still built once per distinct coordinate.
        rows.extend(
            [site(threshold_atom.points[s]) for s in threshold_atom.token_sites]
            for threshold_atom in certificate.threshold_atoms
        )
        for threshold_atom in certificate.threshold_atoms:
            # `_counts` accumulates this row into one `int16` per (box, atom), so the token
            # total has to fit with the threshold it is compared against.
            if threshold_atom.token_count > MAX_TOKENS_PER_ATOM:
                raise IntervalInputError(
                    f"an atom carries {threshold_atom.token_count} tokens, above the "
                    f"{MAX_TOKENS_PER_ATOM} this verifier counts in one int16 lane"
                )
        if len(index) > MAX_INTERVAL_ATOMS:
            raise IntervalInputError(
                f"the interval verifier supports at most {MAX_INTERVAL_ATOMS} distinct sites"
            )
        if len(rows) > MAX_INTERVAL_ATOMS:
            raise IntervalInputError(
                f"the interval verifier supports at most {MAX_INTERVAL_ATOMS} atoms"
            )
        width = max((len(row) for row in rows), default=1)
        if len(rows) * width > MAX_MEMBER_SLOTS:
            raise IntervalInputError(
                f"the member table would hold {len(rows) * width} slots, above the "
                f"{MAX_MEMBER_SLOTS} this verifier gathers per batch"
            )
        members = np.full((len(rows), width), len(index), dtype=np.intp)
        for a, row in enumerate(rows):
            members[a, : len(row)] = row
        thresholds = np.array(
            [1] * len(certificate.atoms) + [t.threshold for t in certificate.threshold_atoms],
            dtype=np.int16,
        )
        xs = [Interval.of(x) for x, _ in index]
        ys = [Interval.of(y) for _, y in index]
        sites = AtomData(
            xlo=np.array([x.lo for x in xs]),
            xhi=np.array([x.hi for x in xs]),
            ylo=np.array([y.lo for y in ys]),
            yhi=np.array([y.hi for y in ys]),
            mass=np.zeros(len(index), dtype=np.int64),
            scale=scale,
            total=0,
        )
        return cls(
            sites=sites,
            members=members,
            thresholds=thresholds,
            mass=np.array(point_masses + threshold_masses, dtype=np.int64),
            scale=scale,
            budget=budget,
            point_count=len(certificate.atoms),
            threshold_count=len(certificate.threshold_atoms),
        )


def scaled_threshold_masses(
    certificate: ThresholdCertificate,
) -> tuple[int, list[int], list[int], int]:
    """The common scale, every point and threshold weight on it, and the total budget.

    All exact Python integers, summed here and not by NumPy, for the reason
    `sqpack.fractional.interval.scaled_atom_masses` gives: an ``int64`` sum of masses that
    individually fit can still wrap. The budget bounds every sum any array operation
    forms -- a charge counts each atom at most once and ``floor(|S| / k) >= 1`` -- so
    refusing a budget at or above ``INT64_MASS_LIMIT`` keeps every such sum inside
    ``int64``. The scale is checked as it grows, so pathological denominators cannot cost
    the product before the refusal.
    """
    scale = 1
    weights = [atom.weight for atom in certificate.atoms] + [
        t.weight for t in certificate.threshold_atoms
    ]
    for weight in weights:
        scale = lcm(scale, weight.denominator)
        if certificate.n * scale >= INT64_MASS_LIMIT:
            raise IntervalInputError("the weight scale is too large for exact integer masses")
    point_masses = [int(atom.weight * scale) for atom in certificate.atoms]
    threshold_masses = [int(t.weight * scale) for t in certificate.threshold_atoms]
    if any(mass < 0 for mass in point_masses + threshold_masses):
        raise IntervalInputError("the interval verifier requires nonnegative weights")
    budget = sum(point_masses) + sum(
        mass * (t.token_count // t.threshold)
        for mass, t in zip(threshold_masses, certificate.threshold_atoms, strict=True)
    )
    if budget >= INT64_MASS_LIMIT:
        raise IntervalInputError(
            "the total scaled budget is too large for safe int64 arithmetic"
        )
    return scale, point_masses, threshold_masses, budget


class ThresholdDirectionSearch(DirectionSearch):
    """Branch and bound over centre boxes for one rotation, charging threshold atoms.

    Everything but the two bounds is the point route's: boxes live in the rotated frame,
    the domain is met through ``tighten``, boxes are split across the axis with more
    region edges inside them, and a box that can be split along neither axis is stalled
    and reported, never accepted. The site enclosures the inherited machinery reads are
    the distinct atom points; the bounds below turn a site mask into a charge through the
    member table.
    """

    def __init__(
        self,
        data: ThresholdAtomData,
        rotation: Rotation,
        outer_side: Interval,
        square_side: Interval,
    ) -> None:
        super().__init__(data.sites, rotation, outer_side, square_side)
        self.members = data.members
        self.thresholds = data.thresholds
        # Mass per atom, replacing the inherited per-site array, which is all zeros here.
        self.mass = data.mass

    def charge(self, held: NDArray[np.bool_]) -> Ints:
        """Scaled charge of each row of ``held``, a mask over the sites in the core.

        With ``held`` the sites provably in every core of a box this is the box's lower
        bound; with ``held`` the sites possibly in the core at a point it is that point's
        upper bound. Both directions rest on the charge being monotone in the trace.
        """
        rows = held.shape[0]
        padded = np.concatenate([held, np.zeros((rows, 1), dtype=bool)], axis=1)
        counts = padded[:, self.members].sum(axis=2, dtype=np.int16)
        return (counts >= self.thresholds) @ self.mass

    def lower_bound(self, boxes: Floats) -> Ints:
        """Charge from the sites whose inner region contains the whole box."""
        ulo, uhi, vlo, vhi = self.inner
        a, b, c, d = (boxes[:, i : i + 1] for i in range(4))
        return self.charge((ulo <= a) & (b <= uhi) & (vlo <= c) & (d <= vhi))

    def upper_bound_at(self, u: Floats, v: Floats) -> Ints:
        """Charge from the sites whose outer region contains the point."""
        ulo, uhi, vlo, vhi = self.outer
        uu, vv = u[:, None], v[:, None]
        return self.charge((ulo <= uu) & (uu <= uhi) & (vlo <= vv) & (vv <= vhi))


# ---------------------------------------------------------------------------
# Exact re-evaluation at a witness centre.
# ---------------------------------------------------------------------------


def exact_rotation(certificate: ThresholdCertificate, label: str) -> tuple[Fraction, Fraction]:
    """``(cos, sin)`` of a doubled-net direction, exactly, from the label's half-tangent.

    ``k`` is ``theta_k = 2 arctan t_k``; ``k'`` is its reflection ``pi/2 - theta_k``, a
    swap of the two components. This is the exact counterpart of `doubled_net`.
    """
    index = int(label.rstrip("'"))
    tangent = certificate.half_tangents[index]
    denominator = 1 + tangent * tangent
    cosine, sine = (1 - tangent * tangent) / denominator, 2 * tangent / denominator
    return (sine, cosine) if label.endswith("'") else (cosine, sine)


@dataclass(frozen=True, slots=True)
class WitnessCharge:
    """The exact charge of the core at a search's witness centre, by membership counting."""

    label: str
    witness: tuple[float, float]
    charge: Fraction
    admissible: bool


def exact_charge_at_witness(
    certificate: ThresholdCertificate, label: str, witness: tuple[float, float]
) -> WitnessCharge:
    """Count, in rational arithmetic, what the core centred at a float witness contains.

    The witness is a pair of floats in the rotated frame of the labelled direction, so
    it is an exact rational point; the direction is rotated exactly; a point is in the
    closed core when both rotated coordinates are within ``B/2`` of the centre; a
    threshold atom charges its weight when its count reaches its threshold. Nothing here
    is shared with the search's arithmetic or with the sweep.
    """
    cosine, sine = exact_rotation(certificate, label)
    u, v = Fraction(witness[0]), Fraction(witness[1])
    x, y = cosine * u - sine * v, sine * u + cosine * v
    side, square = certificate.outer_side, certificate.square_side
    margin = square * (cosine + sine) / 2
    admissible = margin <= x <= side - margin and margin <= y <= side - margin
    half = square / 2

    def inside(px: Fraction, py: Fraction) -> bool:
        return (
            abs(cosine * px + sine * py - u) <= half
            and abs(-sine * px + cosine * py - v) <= half
        )

    charge = sum((a.weight for a in certificate.atoms if inside(a.x, a.y)), start=Fraction(0))
    for t in certificate.threshold_atoms:
        if sum(1 for px, py in t.points if inside(px, py)) >= t.threshold:
            charge += t.weight
    return WitnessCharge(label, witness, charge, admissible)


# ---------------------------------------------------------------------------
# The whole certificate.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ThresholdIntervalVerdict:
    conditions: tuple[IntervalCondition, ...]
    directions: tuple[DirectionOutcome, ...]
    scale: int
    total_budget: Fraction
    refutations: tuple[WitnessCharge, ...]

    @property
    def accepted(self) -> bool:
        return all(condition.holds for condition in self.conditions)

    @property
    def failures(self) -> tuple[str, ...]:
        return tuple(c.name for c in self.conditions if not c.holds)

    @property
    def enclosure(self) -> tuple[Fraction, Fraction] | None:
        """``[lower, upper]`` on the least charge over every direction searched.

        The lower end is the least box bound over all leaves of every search and the
        upper end the least admissible point value, both exact on the weight scale; the
        minimum lies between them. ``None`` when a direction was refuted before either
        bound was established.
        """
        lows = [d.lower for d in self.directions if d.lower is not None]
        highs = [d.upper for d in self.directions if d.upper is not None]
        if not lows or not highs or len(lows) != len(self.directions):
            return None
        return Fraction(min(lows), self.scale), Fraction(min(highs), self.scale)


def _condition_budget_below_n(
    certificate: ThresholdCertificate, data: ThresholdAtomData
) -> IntervalCondition:
    return IntervalCondition(
        "Condition 2' total budget below n",
        f"budget {Fraction(data.budget, data.scale)} against n = {certificate.n}, "
        "exact integers",
        status="holds" if data.budget < certificate.n * data.scale else "fails",
    )


def threshold_searches(
    certificate: ThresholdCertificate, data: ThresholdAtomData
) -> Iterator[ThresholdDirectionSearch]:
    outer = Interval.of(certificate.outer_side)
    square = Interval.of(certificate.square_side)
    for rotation in doubled_net(certificate.half_tangents):
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            search = ThresholdDirectionSearch(data, rotation, outer, square)
        yield search


def _search_direction(
    data: ThresholdAtomData,
    outer: Interval,
    square: Interval,
    prune_at: int | None,
    rotation: Rotation,
) -> DirectionOutcome:
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        search = ThresholdDirectionSearch(data, rotation, outer, square)
        return search.search(prune_at=prune_at)


def _search_directions(
    certificate: ThresholdCertificate,
    data: ThresholdAtomData,
    rotations: tuple[Rotation, ...],
    *,
    prune_at: int | None,
    workers: int,
) -> list[DirectionOutcome]:
    """Every rotation's outcome in net order, stopping after the first refutation.

    ``workers > 1`` forks a pool on Linux; the outcomes are consumed in net order and the
    pool is shut down at the first refutation, so the list is the same whichever
    schedule ran it.
    """
    outer = Interval.of(certificate.outer_side)
    square = Interval.of(certificate.square_side)
    task = partial(_search_direction, data, outer, square, prune_at)
    outcomes: list[DirectionOutcome] = []
    if workers <= 1 or len(rotations) < 2 or not sys.platform.startswith("linux"):
        for rotation in rotations:
            outcomes.append(task(rotation))
            if outcomes[-1].status == "refuted":
                break
        return outcomes
    pool = ProcessPoolExecutor(
        max_workers=min(workers, len(rotations)), mp_context=mp.get_context("fork")
    )
    try:
        for outcome in pool.map(task, rotations):
            outcomes.append(outcome)
            if outcome.status == "refuted":
                break
    finally:
        pool.shutdown(wait=True, cancel_futures=True)
    return outcomes


def verify_threshold_by_intervals(
    certificate: ThresholdCertificate,
    *,
    enclose: bool = False,
    directions: tuple[str, ...] | None = None,
    workers: int = 1,
) -> ThresholdIntervalVerdict:
    """Decide the certificate; ``enclose`` also pins the least charge.

    ``directions`` restricts ``Condition 5'`` to the named labels of the doubled net (a
    sub-net decides a weaker statement and is for controls, not for claims). ``workers``
    is the number of forked processes the directions are shared among; the verdict does
    not depend on it.
    """
    if any(t >= 1 for t in certificate.half_tangents):
        raise IntervalInputError(
            "half-tangents must stay below 1 so the net stays inside a quarter turn"
        )
    data = ThresholdAtomData.of(certificate)
    point = certificate.point_certificate
    conditions = [
        _condition_budget_below_n(certificate, data),
        _condition_net_reaches_eighth_turn(point),
        _condition_containment(point),
    ]
    rotations = tuple(
        rotation
        for rotation in doubled_net(certificate.half_tangents)
        if directions is None or rotation.label in directions
    )
    outcomes = _search_directions(
        certificate,
        data,
        rotations,
        prune_at=None if enclose else data.scale,
        workers=workers,
    )
    # A refutation is a float upper bound below 1 at a provably admissible centre: a
    # direction the pruned search refuted outright, or -- under ``enclose``, where the
    # search never refutes but pins the minimum -- the least point value falling below 1.
    # Either is re-evaluated exactly before the verdict rests on it: a witness whose
    # exact charge reaches 1, or that is not admissible, would mean the floats and the
    # rationals disagree, and that is reported as undecided, never as a refusal on the
    # floats' word.
    refuting = [o for o in outcomes if o.status == "refuted" and o.witness is not None]
    if not refuting:
        pinned_below_one = [
            o
            for o in outcomes
            if o.upper is not None and o.upper < data.scale and o.witness is not None
        ]
        if pinned_below_one:
            refuting.append(min(pinned_below_one, key=lambda o: o.upper or 0))
    refutations = tuple(
        exact_charge_at_witness(certificate, o.label, o.witness)
        for o in refuting
        if o.witness is not None
    )
    confirmed = all(r.admissible and r.charge < 1 for r in refutations)
    statuses = {o.status for o in outcomes}
    # Certified means only that every box was resolved against the threshold the search
    # ran with, and under ``enclose`` that threshold is the minimum itself; whether the
    # pinned value reaches 1 is asked here, so acceptance means the same thing in both
    # modes (the point route's D-435).
    reaches_one = all(o.lower is not None and o.lower >= data.scale for o in outcomes)
    if "refuted" in statuses:
        status: Status = "fails" if confirmed else "undecided"
    elif directions is not None:
        # A restricted run decides its directions and nothing about the rest of the net:
        # it can refute, but only the full doubled net establishes Condition 5'.
        status = "undecided"
    elif statuses == {"certified"}:
        status = "holds" if reaches_one else ("fails" if confirmed else "undecided")
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
        detail += f"; least point charge {Fraction(worst.upper, data.scale)} at {worst.label}"
    for refutation in refutations:
        detail += (
            f"; exact charge {refutation.charge} at the witness of {refutation.label}"
            f" ({'admissible' if refutation.admissible else 'NOT admissible'})"
        )
    if refutations and not confirmed:
        detail += "; the exact re-evaluation does not confirm the interval refutation"
    conditions.append(IntervalCondition(CONDITION_5, detail, status=status))
    return ThresholdIntervalVerdict(
        tuple(conditions),
        tuple(outcomes),
        data.scale,
        Fraction(data.budget, data.scale),
        refutations,
    )


__all__ = [
    "CONDITION_5",
    "MAX_MEMBER_SLOTS",
    "ThresholdAtomData",
    "ThresholdDirectionSearch",
    "ThresholdIntervalVerdict",
    "WitnessCharge",
    "exact_charge_at_witness",
    "exact_rotation",
    "scaled_threshold_masses",
    "threshold_searches",
    "verify_threshold_by_intervals",
]
