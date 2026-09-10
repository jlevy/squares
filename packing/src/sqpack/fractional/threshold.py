"""Threshold atoms: rank-1 Chvátal--Gomory cuts stated on the certificate side.

A point atom of weight ``w`` charges ``w`` to every core containing its point; a packing's
pairwise disjoint cores can be charged at most once, so its budget is ``w``. A
*threshold atom* ``(S, k, w)`` charges ``w`` to every core containing at least ``k`` of the
points of the finite set ``S``. Disjoint cores have disjoint traces on ``S``, each of size
at least ``k`` when charged, so at most ``floor(|S| / k)`` of them are charged: the budget
is ``w floor(|S| / k)``. A *threshold certificate* is a nonnegative combination of point
atoms and threshold atoms whose total budget is below ``n`` while every admissible core
(every closed ``B``-square at a net direction inside the container) is charged at least
``1``. The counting proof of `sqpack.fractional.certificate` then goes through unchanged:
each of ``n`` interior-disjoint unit squares holds a core charged at least ``1``, the
cores are pairwise disjoint, and the sum of their charges is at most the budget. Point
atoms are the case ``|S| = k = 1``; when ``k`` divides ``|S|`` the threshold inequality is
implied by the point inequalities, so the atoms that add anything are ``2-of-3``,
``3-of-4``, ``2-of-5``, ``3-of-5`` and their kin -- on the dual (fractional packing) side,
the clique and odd-cycle inequalities ``sum_{P : |P ∩ S| >= k} y_P <= floor(|S| / k)``.

The five conditions become: ``Condition 1'`` the point atoms *and* the threshold atoms are
D4-invariant (the image of ``(S, k, w)`` under a symmetry of the container is the atom
``(gS, k, w)``, and it must be present with the same weight); ``Condition 2'`` the total
budget is below ``n``; ``Condition 3`` and ``Condition 4`` as before; ``Condition 5'``
every admissible core is charged at least ``1``.

``Condition 5'`` is still decided by the exact event-cell sweep. At a fixed net direction
the charge of a core is a function of its centre; the centres whose core contains a point
``s`` form a closed axis-aligned rectangle ``R_s`` in the rotated frame -- exactly what
`sqpack.fractional.sweep.reduce_to_spans` builds -- so the trace of the core on the union
of all atom points is constant on every open cell of the event grid built from *all* the
points. On a cell boundary the closed core contains every point it contains on any
adjacent open cell, and every charge is monotone in the trace, so the boundary charge is
at least the adjacent open cells' charges: the minimum is attained on an open cell and the
sweep may omit boundaries, as for point atoms.

A threshold atom enters the same integer difference array by inclusion--exclusion. For
an open cell whose trace on ``S`` has ``m`` points,

    [m >= k] = sum_{j >= k} (-1)^(j-k) C(j-1, k-1) C(m, j),

and ``C(m, j)`` counts the ``j``-subsets ``T`` of ``S`` with ``C ⊆ ⋂_{t ∈ T} R_t``. Each
intersection is a closed axis-aligned rectangle with event-coordinate corners, so the atom
is ``sum_{j >= k} C(|S|, j)`` signed rectangle terms whose *sum* on every open cell is the
nonnegative, monotone value ``w [m >= k]``. `sqpack.fractional.sweep` refuses signed
*point weights* because a signed weight makes the charge non-monotone and breaks the
counting; the signs here are internal to an exact expansion of a monotone function and
never reach the theorem. `ThresholdAtom` refuses negative weights, thresholds outside
``1..|S|`` and repeated points; `charge_grid` checks the ``int64`` headroom against the
sum of the absolute expansion coefficients, the largest magnitude any intermediate prefix
sum can reach; and `charge_grid_direct`, which thresholds one integer count grid per
atom instead, is the independent route the tests hold it to, cell for cell.
"""

# The sweep's cell witness and int64 limit are its own and used here on purpose: one
# implementation of the witness, one headroom constant, the test files' own pattern.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import multiprocessing as mp
import sys
from collections.abc import Callable, Iterable
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from fractions import Fraction
from functools import partial
from itertools import combinations
from math import comb, lcm
from typing import Any

import numpy as np

from sqpack.fractional.certificate import (
    Certificate,
    ConditionReport,
    Verdict,
    closed_form_conditions,
    d4_images,
)
from sqpack.fractional.model import Atom, Direction
from sqpack.fractional.sweep import (
    _INTEGER_MASS_LIMIT,
    MassGrid,
    SpanReduction,
    _cell_witness,
    centre_domain,
    reduce_to_spans,
)

Point = tuple[Fraction, Fraction]

#: Threshold-atom points enter the event grid as atoms of this weight: they make events
#: and no mass, and `reduce_to_spans` accepts a zero weight.
_EVENT_ONLY = Fraction(0)


@dataclass(frozen=True, slots=True)
class ThresholdAtom:
    """``(S, k, w)``: weight ``w`` to every core containing at least ``k`` points of ``S``."""

    points: tuple[Point, ...]
    threshold: int
    weight: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.threshold, int) or isinstance(self.threshold, bool):
            raise TypeError("the threshold must be an integer")
        if not self.points:
            raise ValueError("a threshold atom needs at least one point")
        if len(set(self.points)) != len(self.points):
            raise ValueError("a threshold atom's points must be distinct")
        if self.threshold < 1 or self.threshold > len(self.points):
            raise ValueError(
                f"threshold {self.threshold} is outside 1..{len(self.points)}; the charge "
                "would be constant and the budget meaningless"
            )
        if self.weight < 0:
            raise ValueError(
                f"threshold atom has weight {self.weight} < 0; the counting argument needs "
                "every weight nonnegative"
            )

    @property
    def size(self) -> int:
        return len(self.points)

    @property
    def budget(self) -> Fraction:
        """``w floor(|S| / k)``: the most a family of disjoint cores can be charged."""

        return self.weight * (self.size // self.threshold)

    @property
    def key(self) -> tuple[tuple[Point, ...], int]:
        """``(S, k)`` with ``S`` in a canonical order, for symmetry and duplicate checks."""

        return tuple(sorted(self.points)), self.threshold

    def trace_count(self, contains: Callable[[Fraction, Fraction], bool]) -> int:
        return sum(1 for x, y in self.points if contains(x, y))

    def charge(self, contains: Callable[[Fraction, Fraction], bool]) -> Fraction:
        """The charge on a core given its membership test."""

        return self.weight if self.trace_count(contains) >= self.threshold else Fraction(0)

    def images(self, outer_side: Fraction) -> tuple[ThresholdAtom, ...]:
        """The eight D4 images, in `d4_images` order; an atom on a mirror repeats."""

        per_point = [d4_images(x, y, outer_side) for x, y in self.points]
        return tuple(
            ThresholdAtom(tuple(images[g] for images in per_point), self.threshold, self.weight)
            for g in range(8)
        )

    def orbit(self, outer_side: Fraction) -> tuple[ThresholdAtom, ...]:
        """The distinct D4 images, keyed on ``(S, k)``."""

        seen: dict[tuple[tuple[Point, ...], int], ThresholdAtom] = {}
        for image in self.images(outer_side):
            seen.setdefault(image.key, image)
        return tuple(seen.values())

    def to_record(self) -> dict[str, Any]:
        return {
            "points": [[str(x), str(y)] for x, y in self.points],
            "threshold": self.threshold,
            "weight": str(self.weight),
        }

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> ThresholdAtom:
        points = tuple((Fraction(x), Fraction(y)) for x, y in record["points"])
        threshold = record["threshold"]
        if not isinstance(threshold, int) or isinstance(threshold, bool):
            raise TypeError("field 'threshold' must be a JSON integer")
        return cls(points, threshold, Fraction(record["weight"]))


def expansion_terms(size: int, threshold: int) -> tuple[tuple[int, int], ...]:
    """``(j, (-1)^(j-k) C(j-1, k-1))`` for ``j = k .. size``: the inclusion--exclusion
    coefficients of ``[m >= k]`` over the ``j``-subsets of an ``m``-point trace."""

    if threshold < 1 or threshold > size:
        raise ValueError("threshold outside 1..size")
    return tuple(
        (j, (-1) ** (j - threshold) * comb(j - 1, threshold - 1))
        for j in range(threshold, size + 1)
    )


def absolute_expansion_sum(size: int, threshold: int) -> int:
    """``sum_j C(j-1, k-1) C(size, j)``: the total absolute coefficient mass of one atom."""

    return sum(
        abs(coefficient) * comb(size, j) for j, coefficient in expansion_terms(size, threshold)
    )


def threshold_weight_scale(
    atoms: Iterable[Atom], threshold_atoms: Iterable[ThresholdAtom]
) -> int:
    """The least common denominator of every point and threshold weight."""

    scale = 1
    for atom in atoms:
        scale = lcm(scale, atom.weight.denominator)
    for threshold_atom in threshold_atoms:
        scale = lcm(scale, threshold_atom.weight.denominator)
    return scale


def _event_atoms(
    atoms: tuple[Atom, ...], threshold_atoms: tuple[ThresholdAtom, ...]
) -> tuple[Atom, ...]:
    """The point atoms followed by one zero-weight atom per threshold-atom point."""

    extra = [
        Atom(f"t{index}:{offset}", x, y, _EVENT_ONLY)
        for index, threshold_atom in enumerate(threshold_atoms)
        for offset, (x, y) in enumerate(threshold_atom.points)
    ]
    return (*atoms, *extra)


def _scaled(weight: Fraction, scale: int) -> int:
    scaled = weight * scale
    if scaled.denominator != 1:
        raise ValueError("weights are not integers on the declared common scale")
    return int(scaled)


def _headroom(
    atoms: tuple[Atom, ...], threshold_atoms: tuple[ThresholdAtom, ...], scale: int
) -> None:
    """Refuse a grid whose intermediate prefix sums could leave ``int64``."""

    if not isinstance(scale, int) or isinstance(scale, bool) or scale <= 0:
        raise ValueError("the common weight scale must be a positive integer")
    total = sum(_scaled(atom.weight, scale) for atom in atoms)
    total += sum(
        _scaled(t.weight, scale) * absolute_expansion_sum(t.size, t.threshold)
        for t in threshold_atoms
    )
    if total >= _INTEGER_MASS_LIMIT:
        raise ValueError("scaled absolute charge mass exceeds the safe int64 limit")


@dataclass(frozen=True, slots=True)
class Terms:
    """The signed rectangle terms of one direction, on the event grid they index.

    ``left, right, bottom, top`` index ``reduction.u_events`` / ``v_events``; the term
    contributes ``weight`` (scaled, signed) to every open cell ``(i, j)`` with
    ``left <= i < right`` and ``bottom <= j < top``. Point atoms are one term each and
    threshold atoms their inclusion--exclusion expansion.
    """

    reduction: SpanReduction
    left: np.ndarray
    right: np.ndarray
    bottom: np.ndarray
    top: np.ndarray
    weight: np.ndarray
    scale: int


def rectangle_terms(
    atoms: tuple[Atom, ...],
    threshold_atoms: tuple[ThresholdAtom, ...],
    direction: Direction,
    outer_side: Fraction,
    square_side: Fraction,
    *,
    scale: int,
) -> Terms:
    """Every signed rectangle term at one direction, with the event grid it indexes."""

    _headroom(atoms, threshold_atoms, scale)
    for threshold_atom in threshold_atoms:
        for x, y in threshold_atom.points:
            if not (0 <= x <= outer_side and 0 <= y <= outer_side):
                raise ValueError(f"threshold point ({x}, {y}) lies outside the container")
    everything = _event_atoms(atoms, threshold_atoms)
    reduction = reduce_to_spans(everything, direction, outer_side, square_side)
    u_index = {value: index for index, value in enumerate(reduction.u_events)}
    v_index = {value: index for index, value in enumerate(reduction.v_events)}

    lefts: list[int] = []
    rights: list[int] = []
    bottoms: list[int] = []
    tops: list[int] = []
    weights: list[int] = []
    for k, atom in enumerate(atoms):
        u1, u2, v1, v2, _ = reduction.rectangles[k]
        lefts.append(u_index[u1])
        rights.append(u_index[u2])
        bottoms.append(v_index[v1])
        tops.append(v_index[v2])
        weights.append(_scaled(atom.weight, scale))
    cursor = len(atoms)
    for threshold_atom in threshold_atoms:
        rectangles = reduction.rectangles[cursor : cursor + threshold_atom.size]
        cursor += threshold_atom.size
        scaled_weight = _scaled(threshold_atom.weight, scale)
        if scaled_weight == 0:
            continue
        for j, coefficient in expansion_terms(threshold_atom.size, threshold_atom.threshold):
            for subset in combinations(rectangles, j):
                u_low = max(r[0] for r in subset)
                u_high = min(r[1] for r in subset)
                if u_low >= u_high:
                    continue
                v_low = max(r[2] for r in subset)
                v_high = min(r[3] for r in subset)
                if v_low >= v_high:
                    continue
                lefts.append(u_index[u_low])
                rights.append(u_index[u_high])
                bottoms.append(v_index[v_low])
                tops.append(v_index[v_high])
                weights.append(coefficient * scaled_weight)
    return Terms(
        reduction,
        np.array(lefts, dtype=np.intp),
        np.array(rights, dtype=np.intp),
        np.array(bottoms, dtype=np.intp),
        np.array(tops, dtype=np.intp),
        np.array(weights, dtype=np.int64),
        scale,
    )


def charge_grid(
    atoms: tuple[Atom, ...],
    threshold_atoms: tuple[ThresholdAtom, ...],
    direction: Direction,
    outer_side: Fraction,
    square_side: Fraction,
    *,
    scale: int,
) -> MassGrid:
    """The dense integer charge grid at one direction, by inclusion--exclusion.

    The event grid and the reachable spans are `reduce_to_spans`'s, built from the point
    atoms and every threshold-atom point; the difference array holds the point weights and
    the signed rectangle terms of every threshold atom. ``grid[i, j]`` is ``scale`` times
    the charge of open cell ``(i, j)`` -- an exact integer -- on every reachable cell.
    """

    terms = rectangle_terms(
        atoms, threshold_atoms, direction, outer_side, square_side, scale=scale
    )
    reduction = terms.reduction
    width, height = len(reduction.u_events), len(reduction.v_events)
    grid = np.zeros((width, height), dtype=np.int64)
    np.add.at(grid, (terms.left, terms.bottom), terms.weight)
    np.subtract.at(grid, (terms.right, terms.bottom), terms.weight)
    np.subtract.at(grid, (terms.left, terms.top), terms.weight)
    np.add.at(grid, (terms.right, terms.top), terms.weight)
    np.cumsum(grid, axis=1, out=grid)
    np.cumsum(grid, axis=0, out=grid)
    return MassGrid(reduction, grid, scale)


def sweep_slabs(terms: Terms) -> tuple[np.ndarray, np.ndarray]:
    """The least charge in every reachable slab, one slab at a time, in ``O(V)`` memory.

    Returns ``(scores, cells)``: for each entry of ``reduction.spans`` the least scaled
    charge over the span and the ``(i, j)`` cell attaining it, first occurrence winning.
    The difference array over ``v`` is updated as the sweep line crosses each ``u`` event
    and one prefix sum per slab reads the slab's cells: the same numbers the dense grid
    holds, without ever holding the grid.
    """

    reduction = terms.reduction
    height = len(reduction.v_events)
    diff = np.zeros(height, dtype=np.int64)
    add_order = np.argsort(terms.left, kind="stable")
    remove_order = np.argsort(terms.right, kind="stable")
    add_at = terms.left[add_order]
    remove_at = terms.right[remove_order]
    spans = reduction.spans
    scores = np.empty(len(spans), dtype=np.int64)
    cells = np.empty((len(spans), 2), dtype=np.intp)
    a = r = 0
    for k, (i, j0, j1) in enumerate(spans):
        # Every term whose left edge is at or before slab ``i`` is active, and every
        # term whose right edge is at or before ``i`` has been retired.
        a_next = int(np.searchsorted(add_at, i, side="right"))
        if a_next > a:
            idx = add_order[a:a_next]
            np.add.at(diff, terms.bottom[idx], terms.weight[idx])
            np.subtract.at(diff, terms.top[idx], terms.weight[idx])
            a = a_next
        r_next = int(np.searchsorted(remove_at, i, side="right"))
        if r_next > r:
            idx = remove_order[r:r_next]
            np.subtract.at(diff, terms.bottom[idx], terms.weight[idx])
            np.add.at(diff, terms.top[idx], terms.weight[idx])
            r = r_next
        column = np.cumsum(diff[: j1 + 1])[j0 : j1 + 1]
        offset = int(np.argmin(column))
        scores[k] = column[offset]
        cells[k] = (i, j0 + offset)
    return scores, cells


def charge_grid_direct(
    atoms: tuple[Atom, ...],
    threshold_atoms: tuple[ThresholdAtom, ...],
    direction: Direction,
    outer_side: Fraction,
    square_side: Fraction,
    *,
    scale: int,
) -> MassGrid:
    """The reference: one integer count grid per threshold atom, thresholded.

    Quadratic in the grid per atom, so a check and not a route; it shares nothing with
    `charge_grid` past the event grid, which is `reduce_to_spans`'s in both.
    """

    _headroom(atoms, threshold_atoms, scale)
    everything = _event_atoms(atoms, threshold_atoms)
    reduction = reduce_to_spans(everything, direction, outer_side, square_side)
    u_index = {value: index for index, value in enumerate(reduction.u_events)}
    v_index = {value: index for index, value in enumerate(reduction.v_events)}
    width, height = len(reduction.u_events), len(reduction.v_events)
    grid = np.zeros((width, height), dtype=np.int64)

    def paint(target: np.ndarray, rectangle: tuple[Fraction, ...], value: int) -> None:
        u1, u2, v1, v2 = rectangle[:4]
        target[u_index[u1], v_index[v1]] += value
        target[u_index[u2], v_index[v1]] -= value
        target[u_index[u1], v_index[v2]] -= value
        target[u_index[u2], v_index[v2]] += value

    for k, atom in enumerate(atoms):
        paint(grid, reduction.rectangles[k], _scaled(atom.weight, scale))
    np.cumsum(grid, axis=1, out=grid)
    np.cumsum(grid, axis=0, out=grid)
    cursor = len(atoms)
    for threshold_atom in threshold_atoms:
        counts = np.zeros((width, height), dtype=np.int64)
        for rectangle in reduction.rectangles[cursor : cursor + threshold_atom.size]:
            paint(counts, rectangle, 1)
        cursor += threshold_atom.size
        np.cumsum(counts, axis=1, out=counts)
        np.cumsum(counts, axis=0, out=counts)
        grid += (counts >= threshold_atom.threshold) * _scaled(threshold_atom.weight, scale)
    return MassGrid(reduction, grid, scale)


def _witness(
    reduction: SpanReduction,
    cell: tuple[int, int],
    outer_side: Fraction,
    square_side: Fraction,
    direction: Direction,
) -> Point:
    i, j = cell
    return _cell_witness(
        centre_domain(outer_side, square_side, direction),
        reduction.u_events[i],
        reduction.u_events[i + 1],
        reduction.v_events[j],
        reduction.v_events[j + 1],
    )


#: Above this many cells the sweep runs slab by slab instead of filling the dense grid:
#: a dense int64 grid of this size is 800 MB.
DENSE_CELL_LIMIT = 100_000_000


def minimum_charge(
    atoms: tuple[Atom, ...],
    threshold_atoms: tuple[ThresholdAtom, ...],
    direction: Direction,
    outer_side: Fraction,
    square_side: Fraction,
    *,
    dense_cell_limit: int = DENSE_CELL_LIMIT,
) -> tuple[Fraction, Point]:
    """The least charge any reachable core carries at one direction, with a witness
    centre in the rotated frame. Exact; first occurrence wins, in span order.

    The dense grid is filled when it fits ``dense_cell_limit`` cells and the slab sweep
    runs otherwise; the two agree cell for cell (the tests hold them to it).
    """

    scale = threshold_weight_scale(atoms, threshold_atoms)
    terms = rectangle_terms(
        atoms, threshold_atoms, direction, outer_side, square_side, scale=scale
    )
    reduction = terms.reduction
    if len(reduction.u_events) * len(reduction.v_events) <= dense_cell_limit:
        grid = np.zeros((len(reduction.u_events), len(reduction.v_events)), dtype=np.int64)
        np.add.at(grid, (terms.left, terms.bottom), terms.weight)
        np.subtract.at(grid, (terms.right, terms.bottom), terms.weight)
        np.subtract.at(grid, (terms.left, terms.top), terms.weight)
        np.add.at(grid, (terms.right, terms.top), terms.weight)
        np.cumsum(grid, axis=1, out=grid)
        np.cumsum(grid, axis=0, out=grid)
        best: int | None = None
        cell: tuple[int, int] | None = None
        for i, j0, j1 in reduction.spans:
            column = grid[i, j0 : j1 + 1]
            offset = int(np.argmin(column))
            score = int(column[offset])
            if best is None or score < best:
                best, cell = score, (i, j0 + offset)
    else:
        scores, cells = sweep_slabs(terms)
        k = int(np.argmin(scores))
        best, cell = int(scores[k]), (int(cells[k, 0]), int(cells[k, 1]))
    if best is None or cell is None:  # pragma: no cover - reduce_to_spans raises first
        raise ValueError("the sweep produced no reachable cell")
    return Fraction(best, scale), _witness(reduction, cell, outer_side, square_side, direction)


def least_charged_slabs(
    terms: Terms,
    direction: Direction,
    outer_side: Fraction,
    square_side: Fraction,
    *,
    keep: int,
    below: Fraction,
) -> list[tuple[Fraction, Point]]:
    """Up to ``keep`` slab minima charged below ``below``, least first, with witnesses.

    The slab route's row generator: one cell per slab at most, which is what a row per
    placement wants anyway. Cells without a witness name no placement and are skipped.
    """

    scores, cells = sweep_slabs(terms)
    limit = below * terms.scale
    candidates = np.flatnonzero(scores < limit)
    order = candidates[np.argsort(scores[candidates], kind="stable")]
    found: list[tuple[Fraction, Point]] = []
    for index in order:
        cell = (int(cells[index, 0]), int(cells[index, 1]))
        try:
            witness = _witness(terms.reduction, cell, outer_side, square_side, direction)
        except ValueError:
            continue
        found.append((Fraction(int(scores[index]), terms.scale), witness))
        if len(found) >= keep:
            break
    return found


def least_charged_cells(
    grid: MassGrid,
    direction: Direction,
    outer_side: Fraction,
    square_side: Fraction,
    *,
    keep: int,
    below: Fraction,
) -> list[tuple[Fraction, Point]]:
    """Up to ``keep`` reachable cells charged below ``below``, least first, with witnesses.

    For row generation: a cell the span reduction marks but that does not meet the centre
    domain has no witness and is skipped, since it names no placement.
    """

    scores: list[np.ndarray] = []
    cells: list[np.ndarray] = []
    for i, j0, j1 in grid.reduction.spans:
        column = grid.grid[i, j0 : j1 + 1]
        scores.append(column)
        cells.append(np.stack([np.full(column.size, i), np.arange(j0, j1 + 1)], axis=1))
    if not scores:
        return []
    flat = np.concatenate(scores)
    where = np.concatenate(cells)
    limit = below * grid.scale
    candidates = np.flatnonzero(flat < limit)
    if candidates.size == 0:
        return []
    order = candidates[np.argsort(flat[candidates], kind="stable")]
    found: list[tuple[Fraction, Point]] = []
    for index in order:
        i, j = int(where[index, 0]), int(where[index, 1])
        try:
            witness = _witness(grid.reduction, (i, j), outer_side, square_side, direction)
        except ValueError:
            continue
        found.append((Fraction(int(flat[index]), grid.scale), witness))
        if len(found) >= keep:
            break
    return found


def exact_charge(
    atoms: Iterable[Atom],
    threshold_atoms: Iterable[ThresholdAtom],
    contains: Callable[[Fraction, Fraction], bool],
) -> Fraction:
    """The charge of one core given its exact membership test, atom by atom."""

    charge = sum((atom.weight for atom in atoms if contains(atom.x, atom.y)), start=Fraction(0))
    return charge + sum((t.charge(contains) for t in threshold_atoms), start=Fraction(0))


@dataclass(frozen=True, slots=True)
class ThresholdCertificate:
    """A candidate threshold certificate at one ``(n, L, B)``."""

    n: int
    outer_side: Fraction
    square_side: Fraction
    atoms: tuple[Atom, ...]
    threshold_atoms: tuple[ThresholdAtom, ...]
    half_tangents: tuple[Fraction, ...]
    symmetry: str = "D4"

    def __post_init__(self) -> None:
        # The point part carries every precondition of the point certificate, and
        # constructing it is how they are enforced here.
        self.point_certificate  # noqa: B018 - constructing it is the check
        keys = [t.key for t in self.threshold_atoms]
        if len(set(keys)) != len(keys):
            raise ValueError("two threshold atoms share the same (points, threshold)")

    @property
    def point_certificate(self) -> Certificate:
        return Certificate(
            n=self.n,
            outer_side=self.outer_side,
            square_side=self.square_side,
            atoms=self.atoms,
            half_tangents=self.half_tangents,
            symmetry=self.symmetry,
        )

    @property
    def point_mass(self) -> Fraction:
        return sum((atom.weight for atom in self.atoms), start=Fraction(0))

    @property
    def threshold_budget(self) -> Fraction:
        return sum((t.budget for t in self.threshold_atoms), start=Fraction(0))

    @property
    def total_budget(self) -> Fraction:
        """``Condition 2'``'s quantity: point mass plus every threshold budget."""

        return self.point_mass + self.threshold_budget

    @property
    def directions(self) -> tuple[Direction, ...]:
        return self.point_certificate.directions

    def to_record(self) -> dict[str, Any]:
        return {
            "n": self.n,
            "outer_side": str(self.outer_side),
            "square_side": str(self.square_side),
            "half_tangents": [str(t) for t in self.half_tangents],
            "symmetry": self.symmetry,
            "atoms": [[str(a.x), str(a.y), str(a.weight)] for a in self.atoms],
            "threshold_atoms": [t.to_record() for t in self.threshold_atoms],
            "total_budget": str(self.total_budget),
        }


def _condition_symmetric_threshold_atoms(certificate: ThresholdCertificate) -> ConditionReport:
    """``Condition 1'`` for the threshold atoms: every D4 image present, same weight."""

    name = "Condition 1' threshold atoms carry the declared symmetry"
    if certificate.symmetry != "D4":
        return ConditionReport(
            name, f"only D4 is supported, not {certificate.symmetry!r}", holds=False
        )
    weights = {t.key: t.weight for t in certificate.threshold_atoms}
    for threshold_atom in certificate.threshold_atoms:
        for image in threshold_atom.images(certificate.outer_side):
            if weights.get(image.key) != threshold_atom.weight:
                return ConditionReport(
                    name,
                    f"threshold atom on {threshold_atom.points} has no matching image on "
                    f"{image.points}",
                    holds=False,
                )
    return ConditionReport(
        name,
        f"{len(certificate.threshold_atoms)} threshold atoms closed under D4 about the centre",
        holds=True,
    )


def _condition_budget_below_n(certificate: ThresholdCertificate) -> ConditionReport:
    total = certificate.total_budget
    return ConditionReport(
        "Condition 2' total budget below n",
        f"point mass {certificate.point_mass} + threshold budget "
        f"{certificate.threshold_budget} = {total} against n = {certificate.n}",
        holds=total < certificate.n,
    )


def closed_form_threshold_conditions(
    certificate: ThresholdCertificate,
) -> tuple[ConditionReport, ...]:
    """Conditions 1', 2', 3 and 4: everything but the sweep."""

    point = [
        report
        for report in closed_form_conditions(certificate.point_certificate)
        if not report.name.startswith("Condition 2")
    ]
    return (
        point[0],
        _condition_symmetric_threshold_atoms(certificate),
        _condition_budget_below_n(certificate),
        *point[1:],
    )


def _direction_minimum(
    certificate: ThresholdCertificate, direction: Direction
) -> tuple[Fraction, str]:
    minimum, _ = minimum_charge(
        certificate.atoms,
        certificate.threshold_atoms,
        direction,
        certificate.outer_side,
        certificate.square_side,
    )
    return minimum, direction.label


def sweep_all_threshold_directions(
    certificate: ThresholdCertificate, *, workers: int = 1
) -> tuple[tuple[Fraction, str], ...]:
    """The least charge at every net direction, in net order; ``workers > 1`` forks."""

    directions = certificate.directions
    if workers <= 1 or len(directions) < 2 or not sys.platform.startswith("linux"):
        return tuple(_direction_minimum(certificate, d) for d in directions)
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("fork")) as pool:
        return tuple(pool.map(partial(_direction_minimum, certificate), directions))


def verify_threshold(certificate: ThresholdCertificate, *, workers: int = 1) -> Verdict:
    """Decide Conditions 1', 2', 3, 4 and 5'. Exact; never short-circuits."""

    conditions = list(closed_form_threshold_conditions(certificate))
    worst: Fraction | None = None
    worst_label: str | None = None
    for minimum, label in sweep_all_threshold_directions(certificate, workers=workers):
        if worst is None or minimum < worst:
            worst, worst_label = minimum, label
    conditions.append(
        ConditionReport(
            "Condition 5' every reachable cell is charged at least 1",
            f"least cell charge {worst} at direction {worst_label}",
            holds=worst is not None and worst >= 1,
        )
    )
    return Verdict(tuple(conditions), certificate.total_budget, worst, worst_label)


__all__ = [
    "DENSE_CELL_LIMIT",
    "Point",
    "Terms",
    "ThresholdAtom",
    "ThresholdCertificate",
    "absolute_expansion_sum",
    "charge_grid",
    "charge_grid_direct",
    "closed_form_threshold_conditions",
    "exact_charge",
    "expansion_terms",
    "least_charged_cells",
    "least_charged_slabs",
    "minimum_charge",
    "rectangle_terms",
    "sweep_all_threshold_directions",
    "sweep_slabs",
    "threshold_weight_scale",
    "verify_threshold",
]
