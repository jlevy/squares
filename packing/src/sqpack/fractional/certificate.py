"""Weighted fractional unavoidable-set certificates for square packing.

A certificate is the Burns--Massaccesi object: an outer side ``L``, a shrunken
square side ``B``, rational-weight atoms in the container, and a rational
direction net reaching pi/4. It proves ``s(n) >= L`` when five conditions
hold together, so the conditions are named here rather than left to a caller:

``Condition 2``  the total atom mass is strictly below ``n``.
``Condition 3``  the direction net reaches pi/4, which the container's D4
        symmetry needs in order to reduce every angle to the net's arc.
``Condition 4``  ``B (1 + D) < 1`` for ``D`` the largest half-gap tangent of the
        net. A unit square at any angle then contains a ``B``-square at some net
        angle, because ``cos d + sin d <= 1 + tan d``.
``Condition 5``  every event cell the ``B``-square sweep can reach, at every net
        direction, carries mass at least 1.

``Condition 1``  the atom multiset is invariant under the container's D4 group,
        which is what lets a square at an angle past pi/4 be reflected onto the
        net's arc without changing the mass it covers.

Given all five: each of ``n`` interior-disjoint unit squares contains, about
its own centre, a closed ``B``-square at some net angle. That ``B``-square lies
*strictly* inside the unit square's interior: with ``d`` the angle between the
two, ``tan d <= D``, so its width across the unit square,
``B (cos d + sin d) <= B (1 + D)``, is below 1 by ``Condition 4``. (It would be
even with ``<=`` there, since ``D > 0`` and ``cos d < 1`` for ``d > 0``; the
strict test is sufficient, not necessary.) So the ``n`` shrunken squares are
pairwise disjoint as closed sets and no atom is counted twice. Each covers mass at least
1 by ``Condition 5``, for a total of at least ``n``, which ``Condition 2``
forbids. So ``n`` unit squares do not fit in a container of side ``L``, and
``s(n) >= L``. The bound is
``L`` itself; ``B`` rescales nothing (see ``Certificate.bounded_side``).

The arithmetic is exact throughout. Every quantity is a ``Fraction``; nothing
here rounds, samples an angle, or compares against a tolerance.
"""

from __future__ import annotations

import math
import multiprocessing as mp
import os
import sys
import threading
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from fractions import Fraction
from functools import partial
from itertools import pairwise
from multiprocessing.context import BaseContext
from pathlib import Path

from sqpack.fractional.model import (
    Atom,
    Direction,
    require_nonnegative_atom_weights,
    rotation_from_half_tangent,
)
from sqpack.fractional.sweep import minimum_covered_mass


@dataclass(frozen=True, slots=True)
class ConditionReport:
    """One condition's verdict, with the numbers it was decided on.

    ``holds`` is keyword-only: a bare ``True`` sitting between two strings at a
    call site reads as noise, and this value is the verdict.
    """

    name: str
    detail: str
    holds: bool = field(kw_only=True)


@dataclass(frozen=True, slots=True)
class Verdict:
    conditions: tuple[ConditionReport, ...]
    total_mass: Fraction
    minimum_cell_mass: Fraction | None
    worst_direction: str | None

    @property
    def accepted(self) -> bool:
        return all(condition.holds for condition in self.conditions)

    @property
    def failures(self) -> tuple[str, ...]:
        return tuple(c.name for c in self.conditions if not c.holds)


@dataclass(frozen=True, slots=True)
class Certificate:
    """A candidate weighted fractional unavoidable set at one (n, L, B)."""

    n: int
    outer_side: Fraction
    square_side: Fraction
    atoms: tuple[Atom, ...]
    half_tangents: tuple[Fraction, ...]
    symmetry: str = "D4"

    def __post_init__(self) -> None:
        if self.n < 1:
            raise ValueError("n must be positive")
        if self.outer_side <= 0 or self.square_side <= 0:
            raise ValueError("sides must be positive")
        if len(self.half_tangents) < 2:
            raise ValueError("the direction net needs at least two directions")
        if list(self.half_tangents) != sorted(set(self.half_tangents)):
            raise ValueError("half-angle tangents must be strictly increasing")
        if self.half_tangents[0] != 0:
            raise ValueError("the direction net must start at angle zero")
        # Nonnegative weights are a precondition of the theorem, not one of its
        # five conditions: Condition 2 bounds the total, and the counting step
        # that turns the total into a bound on the disjoint inner squares is
        # monotonicity of the measure, which signed weights break.
        require_nonnegative_atom_weights(self.atoms)

    @property
    def total_mass(self) -> Fraction:
        return sum((atom.weight for atom in self.atoms), start=Fraction(0))

    @property
    def bounded_side(self) -> Fraction:
        """The side the certificate bounds: ``L`` itself.

        ``B`` does not divide out here, and getting that wrong inflates the
        result. The shrunken square is not a rescaling of the container; it
        sits *inside* a unit square that is itself inside the side-``L``
        container, and it exists only so that ``Condition 4`` can absorb the net's
        angular gap. So the contradiction is about ``n`` unit squares in side
        ``L``, and what the certificate proves is ``s(n) >= L``.

        Checked against the retained n = 17 certificate: ``L = 22529/5000`` is
        exactly Massaccesi's published 4.5058, while ``L / B`` would claim
        4.51799 and overstate a published result.
        """
        return self.outer_side

    @property
    def directions(self) -> tuple[Direction, ...]:
        """The net as exact unit rotations, via the half-angle parametrisation."""
        return tuple(
            rotation_from_half_tangent(str(index), tangent)
            for index, tangent in enumerate(self.half_tangents)
        )

    @property
    def largest_half_gap_tangent(self) -> Fraction:
        """``D``: the largest tangent of a half-gap between adjacent net angles.

        With ``t = tan(theta / 2)`` the net angle is ``2 arctan t``, so half the
        gap between adjacent directions is ``arctan(t2) - arctan(t1)``, whose
        tangent is ``(t2 - t1) / (1 + t1 t2)`` -- rational, and exactly what the
        containment step needs, not a bound on it. (An earlier docstring called
        this a conservative full-gap value; the independent review of T-017
        corrected that reading.)
        """
        return max(
            (right - left) / (1 + left * right) for left, right in pairwise(self.half_tangents)
        )


def least_size_certified(total_mass: Fraction) -> int:
    """The smallest ``n`` a set of atoms of this mass can certify: ``floor(mass) + 1``.

    ``n`` appears in exactly one of the five conditions. ``Condition 1``,
    ``Condition 3``, ``Condition 4`` and ``Condition 5`` say nothing about it,
    and the covering linear program behind the
    search does not contain it either: minimising total mass subject to every
    admissible ``B``-square carrying mass at least 1 is a question about ``L``,
    ``B`` and the net alone. ``Condition 2`` is where ``n`` enters, and it only asks that
    the mass fall below it.

    So one atom set proves ``s(n) >= L`` for *every* integer ``n`` above its
    mass, not just the one its record happens to declare, and a larger ``n`` is
    strictly easier at the same side. That is the lever for the cases above
    ``n = 17``: a run at a side whose covering value lands between 17 and 18
    raises ``n = 18`` and leaves ``n = 17`` where it was.

    The claim stays consistent with ``ceiling_side`` automatically. If
    ``L > ceil(sqrt(n)) B`` then ``Condition 5`` forces the mass to
    ``ceil(sqrt(n))^2 >= n``, which is exactly what this function then refuses
    to certify.
    """

    return math.floor(total_mass) + 1


def grid_refutation_order(n: int) -> int:
    """The least ``m`` with ``m * m >= n``: the grid that refutes a certificate.

    ``m`` axis-parallel ``B``-squares fit across a container whose side exceeds
    ``m B``, so ``m * m`` of them fit inside it, and the least such ``m`` with
    ``m * m >= n`` is the one that matters. This is ``ceil(sqrt(n))``, written
    with ``isqrt`` so that no float decides an integer.
    """

    root = math.isqrt(n)
    return root if root * root >= n else root + 1


def ceiling_side(n: int, square_side: Fraction) -> Fraction:
    """``ceil(sqrt(n)) * B``: the largest ``L`` at which a certificate can exist.

    The method has a ceiling, and it is elementary. Write ``m = ceil(sqrt(n))``
    and suppose ``L > m B``. Set ``g = (L - m B) / (m + 1) > 0`` and place
    ``m * m`` closed ``B``-squares axis-parallel on a lattice of pitch ``B + g``
    starting at ``(g, g)``. The far edge sits at ``m B + m g < L``, so every
    square lies inside the container; consecutive squares are separated by ``g``,
    so they are pairwise disjoint as closed sets and no atom lies in two of them.
    Direction ``0`` is always a net direction because ``t_0 = 0``, so ``Condition 5``
    applies to each and gives it mass at least ``1``; with non-negative weights
    the total mass is then at least ``m * m >= n``, and ``Condition 2`` forbids that.

    So a certificate for ``n`` forces ``L <= m B``, and ``Condition 4`` forces
    ``B < 1 / (1 + D)`` -- see ``ceiling_side_for_net``, which takes the
    supremum over the shrinks a net admits.

    The consequence worth carrying: ``s(n) <= ceil(sqrt(n))`` holds trivially by
    grid packing, and every single certificate on a finite net sits strictly
    below ``ceil(sqrt(n))``. So no one certificate of this shape certifies the
    grid value; at ``n = 12`` none reaches the conjectured 4. What this lemma
    does not exclude is a proved family of certificates whose sides tend to the
    grid value, followed by a limit argument -- whether such a family exists is
    a question about the covering value, not about this ceiling.
    """

    return grid_refutation_order(n) * square_side


def ceiling_side_for_net(n: int, half_tangents: tuple[Fraction, ...]) -> Fraction:
    """``ceil(sqrt(n)) / (1 + D)``: the ceiling over every shrink this net admits.

    ``Condition 4`` is strict, so this value is a supremum and not attained; a real
    certificate sits below it by whatever margin its own ``B`` leaves. Refining
    the net is what raises it, and only slowly -- ``D`` is about ``T / K`` at the
    axis-parallel end, so halving the gap costs twice the directions and twice
    the cost of every decision made over them.
    """

    gap = max((right - left) / (1 + left * right) for left, right in pairwise(half_tangents))
    return Fraction(grid_refutation_order(n)) / (1 + gap)


def _condition_mass_below_n(certificate: Certificate) -> ConditionReport:
    total = certificate.total_mass
    return ConditionReport(
        "Condition 2 total mass below n",
        f"total {total} against n = {certificate.n}",
        holds=total < certificate.n,
    )


def _condition_arc_reaches_eighth_turn(certificate: Certificate) -> ConditionReport:
    """The net must reach pi/4, i.e. its last half-tangent reaches tan(pi/8).

    ``tan(pi/8) = sqrt(2) - 1`` is irrational, so the test is the exact
    equivalent ``t^2 + 2t - 1 >= 0`` on the final tangent.
    """
    last = certificate.half_tangents[-1]
    slack = last * last + 2 * last - 1
    return ConditionReport(
        "Condition 3 net reaches pi/4",
        f"final half-tangent {last}, t^2 + 2t - 1 = {slack}",
        holds=slack >= 0,
    )


def d4_images(
    x: Fraction, y: Fraction, outer_side: Fraction
) -> tuple[tuple[Fraction, Fraction], ...]:
    """The eight images of a point under the container's symmetry group."""
    far_x, far_y = outer_side - x, outer_side - y
    return (
        (x, y),
        (far_x, y),
        (x, far_y),
        (far_x, far_y),
        (y, x),
        (far_y, x),
        (y, far_x),
        (far_y, far_x),
    )


def _condition_symmetric_atoms(certificate: Certificate) -> ConditionReport:
    """The atom set must carry the symmetry ``Condition 3`` claims to exploit.

    ``Condition 3`` only checks that the net *reaches* pi/4; what makes stopping there
    sound is that a square at any angle in (pi/4, pi/2) reflects to one in
    [0, pi/4] across a symmetry of both the container and the atom set. Declare
    that symmetry without holding it and every angle past pi/4 goes unchecked,
    so this decides it rather than trusting the declaration.
    """
    if certificate.symmetry != "D4":
        return ConditionReport(
            "Condition 1 atoms carry the declared symmetry",
            f"only D4 is supported, not {certificate.symmetry!r}",
            holds=False,
        )
    weights: dict[tuple[Fraction, Fraction], Fraction] = {}
    for atom in certificate.atoms:
        key = (atom.x, atom.y)
        if key in weights:
            return ConditionReport(
                "Condition 1 atoms carry the declared symmetry",
                f"two atoms share the site {key}",
                holds=False,
            )
        weights[key] = atom.weight
    for atom in certificate.atoms:
        for image in d4_images(atom.x, atom.y, certificate.outer_side):
            if weights.get(image) != atom.weight:
                return ConditionReport(
                    "Condition 1 atoms carry the declared symmetry",
                    f"site ({atom.x}, {atom.y}) has no matching image at {image}",
                    holds=False,
                )
    return ConditionReport(
        "Condition 1 atoms carry the declared symmetry",
        f"{len(certificate.atoms)} atoms closed under D4 about the centre",
        holds=True,
    )


def _condition_containment(certificate: Certificate) -> ConditionReport:
    gap = certificate.largest_half_gap_tangent
    product = certificate.square_side * (1 + gap)
    return ConditionReport(
        "Condition 4 containment B(1 + D) < 1",
        f"B = {certificate.square_side}, D = {gap}, B(1 + D) = {product}",
        holds=product < 1,
    )


def closed_form_conditions(certificate: Certificate) -> tuple[ConditionReport, ...]:
    """Conditions 1 to 4, which cost nothing, so a gate can refuse on them before the sweep.

    ``verify`` decides these and then pays for Condition 5 whatever they said, so that a
    verdict reports every condition; a gate that is about to spend minutes on the sweep
    has reason to ask these four first.
    """

    return (
        _condition_symmetric_atoms(certificate),
        _condition_mass_below_n(certificate),
        _condition_arc_reaches_eighth_turn(certificate),
        _condition_containment(certificate),
    )


def sweep_direction_minimum(
    certificate: Certificate, direction: Direction
) -> tuple[Fraction, tuple[Fraction, Fraction]]:
    """The least mass any reachable ``B``-square placement covers, exactly."""

    return minimum_covered_mass(
        certificate.atoms, direction, certificate.outer_side, certificate.square_side
    )


#: Below this many atoms one direction costs milliseconds and a worker pool costs
#: more to start than it saves; the small fixtures the fast tests decide stay in
#: process, where a failure's traceback is also the caller's own.
_PARALLEL_ATOMS = 400

#: Each worker holds one dense int64 event grid, (2N + 2)^2 entries for N atoms, so a
#: host with many cores could turn one decision into an allocation of gigabytes. The
#: pool is capped at this many workers and at this many bytes of grids in flight; a
#: certificate whose single grid exceeds the budget runs one worker rather than
#: refusing. PR 78's adversarial review, F38.
_MAX_PARALLEL_WORKERS = 4
_PARALLEL_GRID_BUDGET_BYTES = 512 * 1024 * 1024


def _estimated_grid_bytes(atom_count: int) -> int:
    """Bytes of one direction's dense grid, at most 2N + 2 events on each axis."""
    events = 2 * atom_count + 2
    return events * events * 8


def _worker_count(certificate: Certificate, requested: int | None) -> int:
    """The pool size: the request or the core count, under the worker and grid caps."""
    available = os.process_cpu_count() or 1
    desired = available if requested is None else max(1, requested)
    per_worker = _estimated_grid_bytes(len(certificate.atoms))
    by_memory = max(1, _PARALLEL_GRID_BUDGET_BYTES // max(1, per_worker))
    return min(
        desired, available, len(certificate.directions), _MAX_PARALLEL_WORKERS, by_memory
    )


def _main_is_importable() -> bool:
    """Whether a forkserver or spawn worker could re-import the caller's ``__main__``."""
    main = sys.modules.get("__main__")
    main_file = getattr(main, "__file__", None) if main is not None else None
    return (
        isinstance(main_file, str)
        and not main_file.startswith("<")
        and Path(main_file).is_file()
    )


def _pool_context() -> BaseContext | None:
    """The start method for the direction pool, or ``None`` to run in this process.

    Python 3.14 starts workers by forkserver on Linux, which re-imports the caller's
    ``__main__``; a caller run from stdin or a REPL has none, and the pool dies with a
    connection reset. Forking inherits the parent and asks nothing of it, but is unsafe
    once the parent has other threads (Python warns, and a lock held by another thread
    is held forever in the child). So: fork while the process is single-threaded; the
    platform default once it is not, provided a worker can import ``__main__``; and no
    pool at all when neither is safe. Off Linux the platform default stands throughout.
    """
    if not sys.platform.startswith("linux"):
        return mp.get_context()
    if threading.active_count() == 1:
        return mp.get_context("fork")
    if _main_is_importable():
        return mp.get_context()
    return None


def _direction_minimum(certificate: Certificate, direction: Direction) -> tuple[Fraction, str]:
    return sweep_direction_minimum(certificate, direction)[0], direction.label


def sweep_all_directions(
    certificate: Certificate, *, workers: int | None = None
) -> tuple[tuple[Fraction, str], ...]:
    """The least covered mass at every net direction, in net order.

    Directions are independent, so they are decided in parallel processes;
    ``workers`` defaults to the process's available core count, or to this process
    alone below ``_PARALLEL_ATOMS`` atoms, and ``1`` runs them in this process. Both
    the default and an explicit count sit under ``_MAX_PARALLEL_WORKERS`` and the
    grid budget (``_worker_count``), and the pool's start method -- or the decision
    to run in this process after all -- is ``_pool_context``'s. An explicit count
    otherwise always gets a pool, so the two schedules can be compared on a
    certificate small enough to compare them quickly. The result is ordered by
    direction whichever way it ran, so the reduction that follows -- first direction
    attaining the minimum wins -- does not depend on the schedule.
    """

    directions = certificate.directions
    count = _worker_count(certificate, workers)
    small = workers is None and len(certificate.atoms) < _PARALLEL_ATOMS
    context = _pool_context() if count > 1 else None
    if count == 1 or len(directions) < 2 or small or context is None:
        return tuple(_direction_minimum(certificate, d) for d in directions)
    with ProcessPoolExecutor(max_workers=count, mp_context=context) as pool:
        return tuple(pool.map(partial(_direction_minimum, certificate), directions))


def verify(certificate: Certificate, *, workers: int | None = None) -> Verdict:
    """Decide all four conditions.

    Exact, and never short-circuits Condition 2 to Condition 4.
    """

    conditions = list(closed_form_conditions(certificate))
    worst: Fraction | None = None
    worst_label: str | None = None
    for minimum, label in sweep_all_directions(certificate, workers=workers):
        if worst is None or minimum < worst:
            worst, worst_label = minimum, label
    conditions.append(
        ConditionReport(
            "Condition 5 every reachable cell carries mass 1",
            f"least cell mass {worst} at direction {worst_label}",
            holds=worst is not None and worst >= 1,
        )
    )
    return Verdict(tuple(conditions), certificate.total_mass, worst, worst_label)
