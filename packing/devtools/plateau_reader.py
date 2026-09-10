"""Plateau reader: exact feasibility of a depth-one family for the rank-one cut families.

A ceiling family (`sqpack.fractional.ceiling`) is a fractional packing ``y`` of closed
``B``-squares at net directions: depth at most one at every point of the container, total
weight at least ``n``. It shows the point-atom covering program stops at ``n``. The
threshold-atom program (`sqpack.fractional.threshold`) adds, on the dual side, the cuts
``y(K(S, k)) <= floor(|S| / k)`` where ``K(S, k)`` is the set of cores holding at least
``k`` points of the finite set ``S``; the floor form ``sum_P floor(a(P) / t) y_P <=
floor(a(S) / t)`` with integer multiplicities ``a`` is the exact rank-one Chvátal--Gomory
cut of the point system and dominates the threshold form. This tool answers, for one
family, the question a plateau of the threshold loop poses: is the family feasible for
every atom of a named class -- in which case that class is capped at this side, a theorem
about the method -- and if not, which atom cuts it, with its exact violation.

Every verdict is decided in rational arithmetic. Floats appear in three places and none
of them decides anything: the screening of arrangement vertices and memberships inside
the envelope `ceiling.py` proves for them (a float superset is confirmed member by member
in integers), the proposal of a piercing measure by a linear program (rationalised and
certified by an exact primal--dual pair, or replaced by an exact simplex), and the
proposal of a Chvátal--Gomory cut by a mixed-integer program (rebuilt as integer
multiplicities and re-verified against the family in rationals).

**Candidate points (PROVED).** Let ``A`` be the arrangement of every placement edge line
and the four container walls. A point outside the closed container lies in no placement
(condition K1), so its membership set is empty. Inside, membership in a closed placement
is constant on each relatively open face of ``A``: a face lies on one closed side of every
line, strictly on one side of every line it does not lie on, and a placement is the
intersection of four closed half-planes bounded by lines of ``A``. Every face of ``A`` in
the container is bounded (the walls are in ``A``) and its closure is a polygon or segment
whose vertices are vertices of ``A``; a closed placement containing the face contains its
closure, so the membership set ``T(p)`` of any point is contained in ``T(v)`` for some
vertex ``v``. Every charge in this module -- ``[|P ∩ S| >= k]``, ``floor(a(P) / t)``, the
piercing condition ``λ(P) >= 1`` -- is nondecreasing in each point's membership set, so
its supremum over all finite point sets in the plane is attained on the arrangement
vertices, and two points with the same membership set are interchangeable. The searches
therefore run over the *distinct membership sets* of the vertices, each with a
representative vertex whose coordinates are exact.

**K4, two-of-three (PROVED complete).** With ``T_i = T(v_i)``, the cores holding at
least two of three points are ``(T_1 ∩ T_2) + (T_3 ∩ (T_1 Δ T_2))``, a disjoint union, so
the charge is
``y(T_1 ∩ T_2) + y(T_3 ∩ (T_1 Δ T_2)) <= y(T_1 ∩ T_2) + min(y(T_1 Δ T_2), D)`` where
``D`` is the maximum depth. The search visits the pairs in decreasing order of that bound
and stops when the bound no longer exceeds the best charge found, taking the third set by
a vectorised maximum; that is branch and bound with an exact bound, hence exact and
complete over triples of distinct membership sets. A triple with a repeated membership
set charges ``y(T) + y(T' ∩ T minus T) = y(T) <= D <= 1`` and cannot violate the budget, so
distinct sets lose nothing for the feasibility question; the report states the maximum
over distinct sets and, separately, the depth.

**K5, all budget-one atoms (PROVED complete).** For ``2k > |S|`` any two ``k``-subsets
of ``S`` meet, so ``K(S, k)`` is a clique of the closed-intersection graph and the atom is
the clique inequality ``y(C) <= 1``. Conversely a clique inequality is a rank-one atom iff
its fractional piercing number ``tau*(C) = min {λ(S) : λ >= 0, λ(P) >= 1 on C}`` is below
two (agenda-034 lane T, F5): with ``λ = a / t`` the atom ``(S, a, t)`` charges every
member and has budget ``floor(λ(S)) = 1``. ``tau*`` is monotone under inclusion, so a
violated budget-one atom exists iff some clique of weight above one has ``tau* < 2``, and
the heaviest such clique is found by enumerating the maximal cliques of weight above one
(Bron--Kerbosch, pruned on weight) and descending into sub-cliques only where ``tau* >=
2``. The piercing program of a clique runs over the distinct membership sets restricted to
the clique, which by the candidate-point argument loses nothing. The two-of-three and
three-of-five atoms are the cases ``|S| = 3, k = 2`` and ``|S| = 5, k = 3``.

**Line chords (PROVED never violated).** For a line ``l`` and threshold ``c``, the cores
whose chord on ``l`` has length at least ``c`` are pairwise-disjoint closed segments of a
segment of length ``|l ∩ container|`` when they come from a packing, so at most
``floor(|l ∩ container| / c)`` of them are packed: the continuum form of the collinear
threshold atoms. A depth-one family can never violate it: its restriction to the chords
is a fractional packing of an interval graph under all its point (clique) constraints,
and interval graphs are perfect, so the restriction is a convex combination of packings.
The tool measures how tight the resource is, exactly, at every offset of every direction
it scans; a violation would indicate depth above one, which step one has excluded.

**K6, the rank-one closure (bounded search).** The Chvátal--Gomory separation problem of
Fischetti and Lodi over the point constraints: multiplicities ``a_s`` on the candidate
points, threshold ``t``, cut ``sum_P floor(a(P) / t) y_P <= floor(a(S) / t)``. Rows are
0/1 with right-hand side one, so multiplicities may be taken below ``t`` (a multiplicity
of ``t`` at a point subtracts that point's own constraint from the cut, which cannot
weaken the violation), and candidate points may be taken among the distinct membership
sets (moving a multiplier to a dominating vertex cannot weaken the cut). For each ``t``
the tool solves the integer program with HiGHS under a time limit; a returned cut is
rebuilt as integer multiplicities and verified exactly. A positive verified objective is
a violated floor atom. A zero or absent optimum is the solver's claim within its bound
and its ``t`` range, and the report labels it so; it is not a theorem.

**What the tool does not protect against.** It reads one family at one ``(L, B, net)``
and says nothing about other families or other sides; the plateau is a theorem about the
class only when the family is the plateau dual itself. It decides threshold and floor
atoms of Chvátal rank one; rank-two atoms, class-indexed certificates and any cut outside
the point system are outside its language. K6 is bounded by the thresholds searched and
the solver's time limit. The three-of-five search of K4's generalisation is a branch and
bound whose completeness the report states per run; the complete decision for that shape
is K5's, by the clique argument above. It assumes the family is what the record says; a
family whose depth exceeds one is refused at step one, but a record with the wrong ``B``
or net is read at face value, as `verify_ceiling` reads it.

Run from ``packing/``, with ``uv run --frozen --all-extras --group dev`` in front::

    python -m devtools.plateau_reader FAMILY.json --out REPORT.json
    python -m devtools.plateau_reader FAMILY.json --skip-k6 --skip-shape
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from math import lcm
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import sparse
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

from sqpack.fractional.ceiling import (
    CeilingCertificate,
    CeilingVerdict,
    Placement,
    arrangement_lines,
    container_vertices,
    depth_screening_is_safe,
    float_family,
    loose_membership,
    verify_ceiling,
)

Point = tuple[Fraction, Fraction]
IntVertex = tuple[int, int, int]

#: Lines the chord scan reads by default: normals of the walls and the diagonals.
LINE_NORMALS: tuple[tuple[str, tuple[Fraction, Fraction]], ...] = (
    ("horizontal", (Fraction(0), Fraction(1))),
    ("vertical", (Fraction(1), Fraction(0))),
    ("diagonal x+y", (Fraction(1), Fraction(1))),
    ("diagonal x-y", (Fraction(1), Fraction(-1))),
)
DEFAULT_LINE_THRESHOLDS: tuple[Fraction, ...] = (
    Fraction(9, 10),
    Fraction(19, 20),
    Fraction(99, 100),
)
DEFAULT_LINE_OFFSETS: tuple[Fraction, ...] = (
    Fraction(1, 100),
    Fraction(1, 20),
    Fraction(1, 10),
    Fraction(1, 4),
    Fraction(1, 2),
    Fraction(3, 4),
    Fraction(1),
)
DEFAULT_CG_THRESHOLDS: tuple[int, ...] = (2, 3, 4)
#: Rationalisation denominators tried, in order, on a float linear-program solution.
_RATIONALISE_DENOMINATORS: tuple[int, ...] = (
    1,
    2,
    3,
    4,
    6,
    8,
    12,
    24,
    60,
    120,
    840,
    10**4,
    10**6,
)


def _f(value: Fraction) -> str:
    return str(value)


def _point_record(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


# ---------------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------------


def load_family(
    path: Path,
    *,
    outer_side: Fraction | None = None,
    square_side: Fraction | None = None,
) -> CeilingCertificate:
    """A ceiling-family record, optionally re-declared at another side or ``B``.

    The record's own ``outer_side`` and ``square_side`` are the method's ``L`` and ``B``;
    an override re-reads the same placements against another instrument, which is what a
    family transported between sides needs. Placements are never changed.
    """

    record = json.loads(path.read_text())
    if outer_side is not None:
        record["outer_side"] = str(outer_side)
    if square_side is not None:
        record["square_side"] = str(square_side)
    return CeilingCertificate.from_record(record)


# ---------------------------------------------------------------------------------
# Exact membership by integer slabs
# ---------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class IntegerSquare:
    """A closed square as two integer slabs: ``|A x + B y - U D| <= H D`` on ``(x, y, D)``.

    Scaling every coefficient of a slab by the least common denominator turns the exact
    rational test of `Placement.contains` into integer arithmetic on a vertex written as
    ``(X, Y, D)`` with ``x = X / D``, ``y = Y / D``. Same decision, no `Fraction` overhead.
    """

    slabs: tuple[tuple[int, int, int, int], ...]

    @classmethod
    def of(cls, placement: Placement) -> IntegerSquare:
        ax, ay, u, bx, by, v = placement.slabs()
        half = placement.side / 2
        rows = []
        for nx, ny, offset in ((ax, ay, u), (bx, by, v)):
            scale = lcm(nx.denominator, ny.denominator, offset.denominator, half.denominator)
            rows.append(
                (
                    int(nx * scale),
                    int(ny * scale),
                    int(offset * scale),
                    int(half * scale),
                )
            )
        return cls(tuple(rows))

    def contains(self, vertex: IntVertex) -> bool:
        x, y, d = vertex
        return all(abs(a * x + b * y - u * d) <= h * d for a, b, u, h in self.slabs)


def integer_vertex(point: Point) -> IntVertex:
    x, y = point
    d = lcm(x.denominator, y.denominator)
    return x.numerator * (d // x.denominator), y.numerator * (d // y.denominator), d


@dataclass(slots=True)
class Arrangement:
    """The family read once: exact vertices, their membership sets, integer weights.

    ``masks`` are the distinct nonempty membership sets as bit masks over placements;
    ``representative[m]`` is one exact vertex carrying mask ``m`` and ``multiplicity[m]``
    how many vertices do. Weights are integers ``W_P`` with ``y_P = W_P / scale``, so
    every charge in the searches is an integer and a violation is ``charge > scale``.
    """

    family: CeilingCertificate
    vertices: list[Point]
    masks: list[int]
    representative: dict[int, Point]
    multiplicity: dict[int, int]
    weights: list[int]
    scale: int
    max_depth: int
    seconds: float

    @property
    def placements(self) -> int:
        return len(self.family.placements)

    def weight_of(self, mask: int) -> int:
        """Integer weight of a set of placements given as a bit mask."""
        total = 0
        while mask:
            low = mask & -mask
            total += self.weights[low.bit_length() - 1]
            mask ^= low
        return total

    def rational(self, units: int) -> Fraction:
        return Fraction(units, self.scale)

    def members(self, mask: int) -> list[int]:
        return [index for index in range(self.placements) if mask >> index & 1]


def exact_membership_masks(family: CeilingCertificate, vertices: list[Point]) -> list[int]:
    """The exact membership bit mask of every vertex.

    Inside the envelope `ceiling.depth_screening_is_safe` proves, a loosened float test
    supplies a superset of the members and each candidate is confirmed in integers;
    outside it every pair is decided in integers.
    """

    squares = [IntegerSquare.of(p) for p in family.placements]
    integer_vertices = [integer_vertex(v) for v in vertices]
    masks: list[int] = []
    if vertices and depth_screening_is_safe(family, vertices):
        normals, offsets, halves, _ = float_family(family)
        points = np.array([[float(x), float(y)] for x, y in vertices])
        loose = loose_membership(points, normals, offsets, halves)
        for row, vertex in enumerate(integer_vertices):
            mask = 0
            for index in np.flatnonzero(loose[row]):
                if squares[int(index)].contains(vertex):
                    mask |= 1 << int(index)
            masks.append(mask)
        return masks
    for vertex in integer_vertices:
        mask = 0
        for index, square in enumerate(squares):
            if square.contains(vertex):
                mask |= 1 << index
        masks.append(mask)
    return masks


def read_arrangement(family: CeilingCertificate) -> Arrangement:
    """Enumerate the arrangement exactly and reduce it to distinct membership sets."""

    started = time.perf_counter()
    vertices = container_vertices(family, arrangement_lines(family))
    scale = lcm(*(p.weight.denominator for p in family.placements))
    weights = [int(p.weight * scale) for p in family.placements]
    representative: dict[int, Point] = {}
    multiplicity: dict[int, int] = {}
    for vertex, mask in zip(vertices, exact_membership_masks(family, vertices), strict=True):
        if not mask:
            continue
        if mask not in representative:
            representative[mask] = vertex
            multiplicity[mask] = 0
        multiplicity[mask] += 1
    masks = sorted(representative)
    arrangement = Arrangement(
        family,
        vertices,
        masks,
        representative,
        multiplicity,
        weights,
        scale,
        0,
        0.0,
    )
    arrangement.max_depth = max((arrangement.weight_of(m) for m in masks), default=0)
    arrangement.seconds = time.perf_counter() - started
    return arrangement


# ---------------------------------------------------------------------------------
# Bit-mask arrays with weighted popcounts
# ---------------------------------------------------------------------------------


class MaskTable:
    """The distinct membership sets as ``uint64`` words, with exact weighted counts.

    ``weighted(q)`` returns, for every stored mask ``m``, the integer weight of ``m & q``:
    one popcount per weight class, since every placement in a class has the same integer
    weight. Exact by construction; the arrays only hold bits.
    """

    def __init__(self, arrangement: Arrangement) -> None:
        self.arrangement = arrangement
        n = arrangement.placements
        self.words = max(1, (n + 63) // 64)
        self.count = len(arrangement.masks)
        self.array = np.zeros((self.count, self.words), dtype=np.uint64)
        for row, mask in enumerate(arrangement.masks):
            for word in range(self.words):
                self.array[row, word] = (mask >> (64 * word)) & ((1 << 64) - 1)
        classes: dict[int, int] = {}
        for index, weight in enumerate(arrangement.weights):
            classes[weight] = classes.get(weight, 0) | (1 << index)
        self.classes = [(weight, mask) for weight, mask in classes.items() if weight > 0]
        self.sizes = self.weighted((1 << n) - 1)

    def _words(self, mask: int) -> NDArray[np.uint64]:
        return np.array(
            [(mask >> (64 * word)) & ((1 << 64) - 1) for word in range(self.words)],
            dtype=np.uint64,
        )

    def weighted(self, query: int) -> NDArray[np.int64]:
        total = np.zeros(self.count, dtype=np.int64)
        for weight, class_mask in self.classes:
            words = self._words(query & class_mask)
            counts = np.bitwise_count(self.array & words[None, :]).astype(np.int64)
            total += weight * counts.sum(axis=1)
        return total


# ---------------------------------------------------------------------------------
# Atoms with multiplicities, verified against the family
# ---------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class WeightedPoint:
    point: Point
    multiplicity: int


@dataclass(frozen=True, slots=True)
class AtomVerdict:
    """An atom ``(S, a, t)`` checked exactly against the family by `Placement.contains`.

    ``threshold_charge`` is ``sum_P y_P [a(P) >= t]`` (the `ThresholdAtom` form, which
    needs repeated points allowed or near-duplicates in the same cell), ``floor_charge``
    is ``sum_P y_P floor(a(P) / t)`` (the Chvátal--Gomory form), the budget is
    ``floor(a(S) / t)`` for both. Both violations are ``charge - budget``.
    """

    family: str
    points: tuple[WeightedPoint, ...]
    threshold: int
    budget: int
    threshold_charge: Fraction
    floor_charge: Fraction
    charged: tuple[int, ...]
    note: str = ""

    @property
    def threshold_violation(self) -> Fraction:
        return self.threshold_charge - self.budget

    @property
    def floor_violation(self) -> Fraction:
        return self.floor_charge - self.budget

    @property
    def violated(self) -> bool:
        return self.floor_violation > 0

    def record(self) -> dict[str, Any]:
        return {
            "family": self.family,
            "points": [
                {"x": str(p.point[0]), "y": str(p.point[1]), "multiplicity": p.multiplicity}
                for p in self.points
            ],
            "threshold": self.threshold,
            "size": sum(p.multiplicity for p in self.points),
            "budget": self.budget,
            "threshold_charge": _f(self.threshold_charge),
            "floor_charge": _f(self.floor_charge),
            "threshold_violation": _f(self.threshold_violation),
            "floor_violation": _f(self.floor_violation),
            "charged_placements": list(self.charged),
            "note": self.note,
        }


def verify_atom(
    family: CeilingCertificate,
    points: Sequence[WeightedPoint],
    threshold: int,
    *,
    label: str,
    note: str = "",
) -> AtomVerdict:
    """Charge and budget of ``(S, a, t)`` on the family, decided by exact containment."""

    if threshold < 1:
        raise ValueError("the threshold must be positive")
    if any(p.multiplicity < 1 for p in points):
        raise ValueError("multiplicities must be positive")
    total = sum(p.multiplicity for p in points)
    threshold_charge = Fraction(0)
    floor_charge = Fraction(0)
    charged: list[int] = []
    for index, placement in enumerate(family.placements):
        held = sum(p.multiplicity for p in points if placement.contains(*p.point))
        if held >= threshold:
            threshold_charge += placement.weight
            floor_charge += placement.weight * (held // threshold)
            charged.append(index)
    return AtomVerdict(
        label,
        tuple(points),
        threshold,
        total // threshold,
        threshold_charge,
        floor_charge,
        tuple(charged),
        note,
    )


# ---------------------------------------------------------------------------------
# K4: k-of-(2k-1) searches over membership sets
# ---------------------------------------------------------------------------------


@dataclass(slots=True)
class ShapeSearch:
    """The maximum charge of a ``k``-of-``(2k-1)`` atom over distinct membership sets."""

    k: int
    size: int
    best: int
    witnesses: list[tuple[int, ...]]
    complete: bool
    nodes: int
    seconds: float
    method: str
    maximiser_count: int = 0

    def record(self, arrangement: Arrangement) -> dict[str, Any]:
        return {
            "k": self.k,
            "size": self.size,
            "max_charge": _f(arrangement.rational(self.best)),
            "max_charge_float": float(arrangement.rational(self.best)),
            "violated": self.best > arrangement.scale,
            "complete": self.complete,
            "method": self.method,
            "nodes": self.nodes,
            "maximiser_count": self.maximiser_count,
            "witness_count": len(self.witnesses),
            "witnesses": [
                {
                    "memberships": sorted(
                        (arrangement.masks[index]).bit_count() for index in witness
                    ),
                    "points": [
                        _point_record(arrangement.representative[arrangement.masks[index]])
                        for index in witness
                    ],
                }
                for witness in self.witnesses[:8]
            ],
            "seconds": round(self.seconds, 3),
        }


def two_of_three_maximum(
    arrangement: Arrangement,
    table: MaskTable | None = None,
    *,
    witness_limit: int = 64,
) -> ShapeSearch:
    """The exact maximum two-of-three charge over triples of distinct membership sets.

    Branch and bound on pairs with the bound ``y(T_i ∩ T_j) + min(y(T_i Δ T_j), D)``
    proved in the module docstring; the third set is the vectorised maximum of
    ``y(T_k ∩ (T_i Δ T_j))``. Every maximising triple among the pairs the bound admits
    is collected up to ``witness_limit``.
    """

    started = time.perf_counter()
    table = table or MaskTable(arrangement)
    count = table.count
    sizes = table.sizes
    depth = arrangement.max_depth
    bounds: list[NDArray[np.int64]] = []
    firsts: list[NDArray[np.int64]] = []
    seconds: list[NDArray[np.int64]] = []
    for i in range(count):
        inter = table.weighted(arrangement.masks[i])
        sym = sizes + sizes[i] - 2 * inter
        bound = inter + np.minimum(sym, depth)
        later = np.arange(count) > i
        keep = np.flatnonzero(later & (bound > 0))
        bounds.append(bound[keep])
        firsts.append(np.full(keep.size, i, dtype=np.int64))
        seconds.append(keep.astype(np.int64))
    if bounds:
        all_bounds = np.concatenate(bounds)
        all_i = np.concatenate(firsts)
        all_j = np.concatenate(seconds)
    else:
        all_bounds = np.zeros(0, dtype=np.int64)
        all_i = all_j = np.zeros(0, dtype=np.int64)
    order = np.argsort(-all_bounds, kind="stable")
    best = 0
    maximisers: list[tuple[int, ...]] = []
    nodes = 0
    for position in order:
        # A pair whose bound equals the best cannot improve it, but it can carry another
        # maximiser, and the witness list is meant to be complete.
        if all_bounds[position] < best:
            break
        i, j = int(all_i[position]), int(all_j[position])
        nodes += 1
        mask_i, mask_j = arrangement.masks[i], arrangement.masks[j]
        inter = arrangement.weight_of(mask_i & mask_j)
        third = table.weighted(mask_i ^ mask_j)
        top = int(third.max()) if count else 0
        total = inter + top
        if total > best:
            best = total
            maximisers = []
        if total == best and best > 0:
            maximisers.extend(
                (i, j, int(k)) for k in np.flatnonzero(third == top) if int(k) not in (i, j)
            )
    witnesses = _sparsest(arrangement, maximisers, witness_limit)
    return ShapeSearch(
        2,
        3,
        best,
        witnesses,
        complete=True,
        nodes=nodes,
        seconds=time.perf_counter() - started,
        method="pair branch and bound over distinct membership sets, exact bound",
        maximiser_count=len(maximisers),
    )


def _sparsest(
    arrangement: Arrangement, tuples: Sequence[tuple[int, ...]], limit: int
) -> list[tuple[int, ...]]:
    """The maximisers with the fewest memberships first: the most local witnesses."""

    def key(witness: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
        sizes = tuple(sorted((arrangement.masks[index]).bit_count() for index in witness))
        return sizes, witness

    return sorted(set(tuples), key=key)[:limit]


def _demand_bound(
    arrangement: Arrangement,
    counts: NDArray[np.int64],
    k: int,
    *,
    remaining: int,
    supply: int,
) -> int:
    """An upper bound on the final charge from a partial choice of sets.

    Points already held by ``k`` sets are charged; a point held by ``c < k`` sets needs
    ``k - c`` of the ``remaining`` sets, and the remaining sets can supply at most
    ``supply`` units of weighted membership in total. The fractional knapsack over the
    demands, cheapest first, bounds what they can add.
    """

    charged = 0
    demands: list[tuple[int, int]] = []
    for index, weight in enumerate(arrangement.weights):
        c = int(counts[index])
        if c >= k:
            charged += weight
        elif c + remaining >= k and weight > 0:
            demands.append((k - c, weight))
    demands.sort()
    left = supply
    extra = Fraction(0)
    for demand, weight in demands:
        cost = demand * weight
        if cost <= left:
            extra += weight
            left -= cost
        else:
            extra += Fraction(left, demand)
            break
    return charged + int(extra)


def k_of_search(
    arrangement: Arrangement,
    k: int,
    table: MaskTable | None = None,
    *,
    node_limit: int = 200_000,
    target: int | None = None,
) -> ShapeSearch:
    """Branch and bound for the maximum ``k``-of-``(2k-1)`` charge over distinct sets.

    Sets are chosen in nonincreasing order of weight (the charge is symmetric in the
    points, so this loses nothing), pruned by two exact bounds -- the weight-order bound
    ``k y(K) <= sum_chosen y(T_i) + r y(T_last)`` and the demand bound of
    `_demand_bound` -- and the last set is taken by a vectorised maximum. ``target`` (in
    integer units) makes the search look only for charges above it; ``node_limit`` bounds
    the nodes, and ``complete`` in the result says whether the bound was hit.
    """

    started = time.perf_counter()
    table = table or MaskTable(arrangement)
    size = 2 * k - 1
    count = table.count
    order = sorted(range(count), key=lambda index: (-int(table.sizes[index]), index))
    rank_size = [int(table.sizes[index]) for index in order]
    best = target if target is not None else 0
    witnesses: list[tuple[int, ...]] = []
    nodes = 0
    complete = True
    counts = np.zeros(arrangement.placements, dtype=np.int64)
    member_rows = [np.array(arrangement.members(m), dtype=np.int64) for m in arrangement.masks]

    def last_set(chosen: list[int], counts_now: NDArray[np.int64], limit_rank: int) -> None:
        nonlocal best, witnesses
        charged = 0
        need = 0
        for index, weight in enumerate(arrangement.weights):
            c = int(counts_now[index])
            if c >= k:
                charged += weight
            elif c == k - 1:
                need |= 1 << index
        gains = table.weighted(need)
        candidates = np.array(order[limit_rank:], dtype=np.int64)
        if candidates.size == 0:
            return
        totals = charged + gains[candidates]
        top = int(totals.max())
        if top > best:
            best = top
            witnesses = []
        if top == best and best > 0 and len(witnesses) < 4096:
            witnesses.extend(
                (*chosen, int(pick))
                for pick in candidates[totals == top]
                if int(pick) not in chosen
            )

    def descend(chosen: list[int], rank: int, chosen_weight: int) -> None:
        nonlocal nodes, complete
        remaining = size - len(chosen)
        if remaining == 1:
            nodes += 1
            last_set(chosen, counts, rank)
            return
        for position in range(rank, count):
            if nodes >= node_limit:
                complete = False
                return
            nodes += 1
            index = order[position]
            weight = rank_size[position]
            if k * best >= chosen_weight + weight + (remaining - 1) * weight and best > 0:
                return
            counts[member_rows[index]] += 1
            chosen.append(index)
            supply = (remaining - 1) * weight
            bound = _demand_bound(
                arrangement, counts, k, remaining=remaining - 1, supply=supply
            )
            if bound > best or best == 0:
                descend(chosen, position + 1, chosen_weight + weight)
            chosen.pop()
            counts[member_rows[index]] -= 1

    descend([], 0, 0)
    found = best if witnesses or target is None else 0
    return ShapeSearch(
        k,
        size,
        found,
        _sparsest(arrangement, witnesses, 64),
        complete=complete,
        nodes=nodes,
        seconds=time.perf_counter() - started,
        method="depth-first branch and bound over distinct membership sets, exact bounds",
        maximiser_count=len(set(witnesses)),
    )


def shape_atom(
    arrangement: Arrangement, witness: Sequence[int], k: int, label: str
) -> AtomVerdict:
    points = [
        WeightedPoint(arrangement.representative[arrangement.masks[index]], 1)
        for index in witness
    ]
    return verify_atom(arrangement.family, points, k, label=label)


# ---------------------------------------------------------------------------------
# K5: cliques of the closed-intersection graph and their piercing numbers
# ---------------------------------------------------------------------------------


def closed_squares_intersect(first: Placement, second: Placement) -> bool:
    """Whether two closed squares share a point, by the separating-axis theorem.

    Two closed convex polygons are disjoint iff some edge normal of one of them
    separates their projections; for squares the four candidate normals are the two of
    each. Projections are closed intervals compared exactly.
    """

    for placement in (first, second):
        ax, ay, _, bx, by, _ = placement.slabs()
        for nx, ny in ((ax, ay), (bx, by)):
            first_lo, first_hi = _projection(first, nx, ny)
            second_lo, second_hi = _projection(second, nx, ny)
            if first_hi < second_lo or second_hi < first_lo:
                return False
    return True


def _projection(placement: Placement, nx: Fraction, ny: Fraction) -> tuple[Fraction, Fraction]:
    values = [nx * x + ny * y for x, y in placement.corners()]
    return min(values), max(values)


def intersection_graph(family: CeilingCertificate) -> list[int]:
    """Adjacency bit masks of the closed-intersection graph on the placements."""

    n = len(family.placements)
    adjacency = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if closed_squares_intersect(family.placements[i], family.placements[j]):
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
    return adjacency


def maximal_cliques_above(
    arrangement: Arrangement,
    adjacency: Sequence[int],
    floor_weight: int,
    *,
    node_limit: int = 5_000_000,
) -> tuple[list[int], bool]:
    """Every maximal clique of weight above ``floor_weight``, as bit masks.

    Bron--Kerbosch with pivoting, pruned when the clique so far plus every remaining
    candidate cannot exceed the floor: a maximal clique above the floor has, on every
    path leading to it, ``R ⊆ C ⊆ R + P``, so the pruned branches contain none.
    """

    found: list[int] = []
    nodes = 0
    complete = True

    def expand(r: int, p: int, x: int) -> None:
        nonlocal nodes, complete
        nodes += 1
        if nodes > node_limit:
            complete = False
            return
        if arrangement.weight_of(r | p) <= floor_weight:
            return
        if p == 0:
            if x == 0:
                found.append(r)
            return
        pivot_pool = p | x
        pivot = max(
            (index for index in range(arrangement.placements) if pivot_pool >> index & 1),
            key=lambda index: (p & adjacency[index]).bit_count(),
        )
        candidates = p & ~adjacency[pivot]
        while candidates:
            low = candidates & -candidates
            v = low.bit_length() - 1
            expand(r | low, p & adjacency[v], x & adjacency[v])
            p &= ~low
            x |= low
            candidates &= ~low
            if not complete:
                return

    expand(0, (1 << arrangement.placements) - 1, 0)
    return found, complete


@dataclass(frozen=True, slots=True)
class Piercing:
    """``tau*`` of a clique with its exact primal and dual certificates.

    ``measure`` is a feasible piercing measure (upper bound on ``tau*``), ``packing`` a
    feasible fractional packing of the clique against the candidate points (lower bound);
    ``exact`` says the two values agree, in which case ``value`` is ``tau*``.
    """

    value: Fraction
    lower: Fraction
    measure: tuple[tuple[Point, Fraction], ...]
    exact: bool
    candidates: int
    route: str


def _feasible_measure(
    rows: Sequence[int], values: Sequence[Fraction], members: Sequence[int]
) -> bool:
    if any(v < 0 for v in values):
        return False
    return all(
        sum(
            (v for row, v in zip(rows, values, strict=True) if row >> member & 1),
            start=Fraction(0),
        )
        >= 1
        for member in members
    )


def _feasible_packing(
    rows: Sequence[int], members: Sequence[int], values: Sequence[Fraction]
) -> bool:
    if any(v < 0 for v in values):
        return False
    return all(
        sum(
            (v for member, v in zip(members, values, strict=True) if row >> member & 1),
            start=Fraction(0),
        )
        <= 1
        for row in rows
    )


def exact_packing_simplex(
    rows: Sequence[int], members: Sequence[int]
) -> tuple[Fraction, list[Fraction], list[Fraction]]:
    """``max sum mu`` subject to ``sum_{P ∋ s} mu_P <= 1`` per candidate ``s``, exactly.

    Dense primal simplex in `Fraction` with Bland's rule (finite by construction); the
    origin is feasible. Returns the optimum, ``mu``, and the dual ``lambda`` read from the
    reduced costs of the slack columns, which is an optimal piercing measure.
    """

    m, n = len(rows), len(members)
    tableau: list[list[Fraction]] = []
    for row in rows:
        line = [Fraction(int(row >> member & 1)) for member in members]
        line += [Fraction(0)] * m
        line.append(Fraction(1))
        tableau.append(line)
    for i in range(m):
        tableau[i][n + i] = Fraction(1)
    objective = [Fraction(-1)] * n + [Fraction(0)] * m + [Fraction(0)]
    basis = [n + i for i in range(m)]
    while True:
        entering = next((j for j in range(n + m) if objective[j] < 0), None)
        if entering is None:
            break
        best_ratio: Fraction | None = None
        leaving = -1
        for i in range(m):
            coefficient = tableau[i][entering]
            if coefficient > 0:
                ratio = tableau[i][-1] / coefficient
                if (
                    best_ratio is None
                    or ratio < best_ratio
                    or (ratio == best_ratio and basis[i] < basis[leaving])
                ):
                    best_ratio, leaving = ratio, i
        if leaving < 0:
            raise ValueError("the packing program is unbounded, which a bounded clique forbids")
        pivot = tableau[leaving][entering]
        tableau[leaving] = [value / pivot for value in tableau[leaving]]
        for i in range(m):
            if i != leaving and tableau[i][entering] != 0:
                factor = tableau[i][entering]
                tableau[i] = [
                    a - factor * b for a, b in zip(tableau[i], tableau[leaving], strict=True)
                ]
        if objective[entering] != 0:
            factor = objective[entering]
            objective = [
                a - factor * b for a, b in zip(objective, tableau[leaving], strict=True)
            ]
        basis[leaving] = entering
    mu = [Fraction(0)] * n
    for i, column in enumerate(basis):
        if column < n:
            mu[column] = tableau[i][-1]
    lam = [objective[n + i] for i in range(m)]
    return objective[-1], mu, lam


def piercing_number(arrangement: Arrangement, clique: int) -> Piercing:
    """``tau*`` of a clique over the distinct membership sets restricted to it, exactly.

    A float linear program proposes; the proposal is rationalised at increasing
    denominators until an exact feasible measure and an exact feasible packing agree,
    and failing that the exact simplex decides. Dominated candidate points (restricted
    sets contained in another's) are dropped first, which loses nothing.
    """

    members = arrangement.members(clique)
    restricted: dict[int, Point] = {}
    for mask in arrangement.masks:
        part = mask & clique
        if part and part not in restricted:
            restricted[part] = arrangement.representative[mask]
    rows = [
        part
        for part in restricted
        if not any(other != part and other & part == part for other in restricted)
    ]
    if not rows:
        raise ValueError(
            "a clique with no candidate point: the family is not what its record says"
        )
    matrix = np.array([[float(row >> member & 1) for row in rows] for member in members])
    result = linprog(
        np.ones(len(rows)),
        A_ub=-matrix,
        b_ub=-np.ones(len(members)),
        bounds=(0, None),
        method="highs",
    )
    upper: Fraction | None = None
    lower: Fraction | None = None
    measure: list[Fraction] = []
    route = "float proposal certified by an exact primal-dual pair"
    if result.status == 0:
        primal = [float(v) for v in result.x]
        dual = [-float(v) for v in result.ineqlin.marginals]
        for denominator in _RATIONALISE_DENOMINATORS:
            lam = [Fraction(v).limit_denominator(denominator) for v in primal]
            mu = [Fraction(v).limit_denominator(denominator) for v in dual]
            if _feasible_measure(rows, lam, members):
                value = sum(lam, start=Fraction(0))
                if upper is None or value < upper:
                    upper, measure = value, lam
            if _feasible_packing(rows, members, mu):
                value = sum(mu, start=Fraction(0))
                if lower is None or value > lower:
                    lower = value
            if upper is not None and lower is not None and upper == lower:
                break
    if upper is None or lower is None or upper != lower:
        value, _, lam = exact_packing_simplex(rows, members)
        if not _feasible_measure(rows, lam, members):
            raise ValueError("the exact simplex returned an infeasible dual")
        upper = lower = value
        measure = lam
        route = "exact rational simplex"
    return Piercing(
        upper,
        lower,
        tuple(
            (restricted[row], value)
            for row, value in zip(rows, measure, strict=True)
            if value > 0
        ),
        upper == lower,
        len(rows),
        route,
    )


def piercing_atom(
    arrangement: Arrangement, piercing: Piercing, label: str, note: str = ""
) -> AtomVerdict:
    """The integer-multiplicity atom of a piercing measure, verified on the family."""

    denominator = lcm(*(value.denominator for _, value in piercing.measure))
    points = [
        WeightedPoint(point, int(value * denominator)) for point, value in piercing.measure
    ]
    return verify_atom(arrangement.family, points, denominator, label=label, note=note)


@dataclass(slots=True)
class CliqueScan:
    edges: int
    maximal_above_one: int
    enumeration_complete: bool
    piercings_solved: int
    heaviest_clique: int | None
    heaviest_weight: Fraction
    heaviest_tau: Piercing | None
    heaviest_rank_one_clique: int | None
    heaviest_rank_one_weight: Fraction
    heaviest_rank_one_tau: Piercing | None
    atom: AtomVerdict | None
    tau_at_least_two: int
    seconds: float

    def record(self, arrangement: Arrangement) -> dict[str, Any]:
        def clique_record(mask: int | None, tau: Piercing | None) -> dict[str, Any] | None:
            if mask is None or tau is None:
                return None
            return {
                "members": arrangement.members(mask),
                "size": (mask).bit_count(),
                "weight": _f(arrangement.rational(arrangement.weight_of(mask))),
                "tau_star": _f(tau.value),
                "tau_star_lower": _f(tau.lower),
                "tau_exact": tau.exact,
                "tau_route": tau.route,
                "candidate_points": tau.candidates,
                "piercing_measure": [
                    {"x": str(p[0]), "y": str(p[1]), "weight": _f(w)} for p, w in tau.measure
                ],
            }

        return {
            "graph": "closed intersection (separating-axis test, exact)",
            "edges": self.edges,
            "maximal_cliques_above_one": self.maximal_above_one,
            "enumeration_complete": self.enumeration_complete,
            "piercing_programs_solved": self.piercings_solved,
            "cliques_with_tau_at_least_two": self.tau_at_least_two,
            "heaviest_clique": clique_record(self.heaviest_clique, self.heaviest_tau),
            "heaviest_rank_one_clique": clique_record(
                self.heaviest_rank_one_clique, self.heaviest_rank_one_tau
            ),
            "atom": self.atom.record() if self.atom else None,
            "seconds": round(self.seconds, 3),
        }


def clique_scan(arrangement: Arrangement, *, node_limit: int = 5_000_000) -> CliqueScan:
    """K5: the heaviest clique with ``tau* < 2`` and its atom, exactly.

    Maximal cliques above weight one are enumerated; each gets its piercing number; a
    clique with ``tau* >= 2`` is descended into (one member removed at a time, pruned at
    weight at most ``max(1, best)``), since a sub-clique may still have ``tau* < 2``.
    """

    started = time.perf_counter()
    adjacency = intersection_graph(arrangement.family)
    edges = sum((a).bit_count() for a in adjacency) // 2
    maximal, complete = maximal_cliques_above(
        arrangement, adjacency, arrangement.scale, node_limit=node_limit
    )
    memo: dict[int, Piercing] = {}

    def tau(mask: int) -> Piercing:
        if mask not in memo:
            memo[mask] = piercing_number(arrangement, mask)
        return memo[mask]

    heaviest: int | None = None
    heaviest_weight = 0
    best: int | None = None
    best_weight = 0
    at_least_two = 0
    stack = sorted(maximal, key=lambda mask: -arrangement.weight_of(mask))
    seen: set[int] = set()
    while stack:
        mask = stack.pop()
        if mask in seen:
            continue
        seen.add(mask)
        weight = arrangement.weight_of(mask)
        if weight <= max(arrangement.scale, best_weight):
            continue
        piercing = tau(mask)
        if weight > heaviest_weight:
            heaviest, heaviest_weight = mask, weight
        if piercing.value < 2:
            if weight > best_weight:
                best, best_weight = mask, weight
            continue
        at_least_two += 1
        remaining = mask
        while remaining:
            low = remaining & -remaining
            remaining ^= low
            child = mask ^ low
            if child not in seen and arrangement.weight_of(child) > max(
                arrangement.scale, best_weight
            ):
                stack.append(child)
    atom = None
    if best is not None:
        atom = piercing_atom(
            arrangement,
            tau(best),
            "weighted clique (piercing measure)",
            note=f"clique of {best.bit_count()} members, tau* = {tau(best).value}",
        )
    return CliqueScan(
        edges,
        len(maximal),
        complete,
        len(memo),
        heaviest,
        arrangement.rational(heaviest_weight),
        tau(heaviest) if heaviest is not None else None,
        best,
        arrangement.rational(best_weight),
        tau(best) if best is not None else None,
        atom,
        at_least_two,
        time.perf_counter() - started,
    )


# ---------------------------------------------------------------------------------
# Line chords, exactly, in Q(sqrt 2)
# ---------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, order=False)
class Surd:
    """``a + b sqrt(2)`` with rational ``a, b``: the field the diagonal chords live in.

    Comparison is exact: the sign of ``a + b sqrt 2`` is decided from the signs of ``a``
    and ``b`` and, when they differ, from ``a^2`` against ``2 b^2`` (equality is
    impossible unless both vanish, since ``sqrt 2`` is irrational).
    """

    a: Fraction
    b: Fraction = Fraction(0)

    @classmethod
    def of(cls, value: Fraction | int) -> Surd:
        return cls(Fraction(value))

    def sign(self) -> int:
        a, b = self.a, self.b
        if a == 0 and b == 0:
            return 0
        if a >= 0 and b >= 0:
            return 1
        if a <= 0 and b <= 0:
            return -1
        positive_part = a > 0
        return 1 if (a * a > 2 * b * b) == positive_part else -1

    def __add__(self, other: Surd) -> Surd:
        return Surd(self.a + other.a, self.b + other.b)

    def __sub__(self, other: Surd) -> Surd:
        return Surd(self.a - other.a, self.b - other.b)

    def __neg__(self) -> Surd:
        return Surd(-self.a, -self.b)

    def __mul__(self, other: Surd) -> Surd:
        return Surd(
            self.a * other.a + 2 * self.b * other.b, self.a * other.b + self.b * other.a
        )

    def scale(self, factor: Fraction) -> Surd:
        return Surd(self.a * factor, self.b * factor)

    def __lt__(self, other: Surd) -> bool:
        return (self - other).sign() < 0

    def __le__(self, other: Surd) -> bool:
        return (self - other).sign() <= 0

    def __gt__(self, other: Surd) -> bool:
        return (self - other).sign() > 0

    def __ge__(self, other: Surd) -> bool:
        return (self - other).sign() >= 0

    def __float__(self) -> float:
        return float(self.a) + float(self.b) * 2**0.5

    def __str__(self) -> str:
        if self.b == 0:
            return str(self.a)
        return f"{self.a} + ({self.b})*sqrt(2)"


@dataclass(frozen=True, slots=True)
class LineFamily:
    """Lines ``n . p = s`` for a rational normal ``n``; ``d = (-n_y, n_x)`` runs along them.

    The chord of a convex set on the line is ``|d|`` times its extent in the parameter
    ``t`` of ``p = s n / |n|^2 + t d``, and ``|d|^2 = n . n``; with ``|n|^2 = 2`` the
    thresholds become ``c / sqrt 2``, a `Surd`.
    """

    label: str
    nx: Fraction
    ny: Fraction

    @property
    def norm_squared(self) -> Fraction:
        return self.nx * self.nx + self.ny * self.ny

    def threshold(self, length: Fraction) -> Surd:
        """The extent in ``t`` that a chord of length ``length`` requires."""
        if self.norm_squared == 1:
            return Surd(length)
        if self.norm_squared == 2:
            return Surd(Fraction(0), length / 2)
        raise ValueError("line normals must have squared norm 1 or 2")

    def extent_pieces(
        self, placement: Placement
    ) -> list[tuple[Fraction, Fraction, Fraction, Fraction]]:
        """The chord extent ``f(s)`` as linear pieces ``(s_lo, s_hi, f_lo, f_hi)``.

        Between consecutive offsets of the square's corners the two edges the line
        crosses are fixed, so the extent is linear there; its values at the corner
        offsets are computed by clipping the line against the slabs it is not parallel
        to. On the closed support the slabs the line is parallel to hold automatically.
        """

        ax, ay, u, bx, by, v = placement.slabs()
        half = placement.side / 2
        nn = self.norm_squared
        dx, dy = -self.ny, self.nx
        offsets = sorted({self.nx * x + self.ny * y for x, y in placement.corners()})

        def extent(s: Fraction) -> Fraction:
            px, py = self.nx * s / nn, self.ny * s / nn
            lower: Fraction | None = None
            upper: Fraction | None = None
            for cx, cy, centre in ((ax, ay, u), (bx, by, v)):
                g = cx * dx + cy * dy
                if g == 0:
                    continue
                base = cx * px + cy * py
                first, second = (centre - half - base) / g, (centre + half - base) / g
                lo, hi = min(first, second), max(first, second)
                lower = lo if lower is None else max(lower, lo)
                upper = hi if upper is None else min(upper, hi)
            if lower is None or upper is None:
                raise ValueError("a line parallel to both edge directions of a square")
            return max(upper - lower, Fraction(0))

        values = [extent(s) for s in offsets]
        return [
            (offsets[i], offsets[i + 1], values[i], values[i + 1])
            for i in range(len(offsets) - 1)
        ] or [(offsets[0], offsets[0], values[0], values[0])]

    def chord_interval(self, placement: Placement, tau: Surd) -> tuple[Surd, Surd] | None:
        """The closed set of offsets where the chord extent is at least ``tau``.

        By concavity of the section length of a convex body it is one interval; each
        linear piece is solved and the pieces' solutions are joined.
        """

        lo: Surd | None = None
        hi: Surd | None = None
        for s_lo, s_hi, f_lo, f_hi in self.extent_pieces(placement):
            piece = _solve_piece(s_lo, s_hi, f_lo, f_hi, tau)
            if piece is None:
                continue
            lo = piece[0] if lo is None else min(lo, piece[0])
            hi = piece[1] if hi is None else max(hi, piece[1])
        if lo is None or hi is None:
            return None
        return lo, hi

    def extent_at(self, placement: Placement, s: Surd) -> Surd | None:
        """The chord extent at an offset, or None outside the square's support."""
        for s_lo, s_hi, f_lo, f_hi in self.extent_pieces(placement):
            if Surd(s_lo) <= s <= Surd(s_hi):
                if s_hi == s_lo:
                    return Surd(f_lo)
                slope = (f_hi - f_lo) / (s_hi - s_lo)
                return Surd(f_lo) + (s - Surd(s_lo)).scale(slope)
        return None


def _solve_piece(
    s_lo: Fraction, s_hi: Fraction, f_lo: Fraction, f_hi: Fraction, tau: Surd
) -> tuple[Surd, Surd] | None:
    left, right = Surd(s_lo), Surd(s_hi)
    if s_hi == s_lo:
        return (left, right) if Surd(f_lo) >= tau else None
    slope = (f_hi - f_lo) / (s_hi - s_lo)
    if slope == 0:
        return (left, right) if Surd(f_lo) >= tau else None
    crossing = left + (tau - Surd(f_lo)).scale(1 / slope)
    if slope > 0:
        lo, hi = max(left, crossing), right
    else:
        lo, hi = left, min(right, crossing)
    return (lo, hi) if lo <= hi else None


def container_square(family: CeilingCertificate) -> Placement:
    side = family.outer_side
    return Placement(Fraction(0), side / 2, side / 2, Fraction(1), side)


@dataclass(slots=True)
class LineResult:
    direction: str
    threshold: Fraction
    max_count: Fraction
    max_count_budget: int
    max_count_offset: str
    max_slack_violation: Fraction
    tight_somewhere: bool
    named: list[dict[str, Any]]
    tight_count: Fraction = Fraction(0)
    tight_offset: str = "none"

    def record(self) -> dict[str, Any]:
        return {
            "direction": self.direction,
            "threshold": _f(self.threshold),
            "max_weight_with_chord_at_least_threshold": _f(self.max_count),
            "budget_there": self.max_count_budget,
            "offset_there": self.max_count_offset,
            "max_of_count_minus_budget": _f(self.max_slack_violation),
            "tight_somewhere": self.tight_somewhere,
            "largest_tight_count": _f(self.tight_count),
            "largest_tight_offset": self.tight_offset,
            "violated": self.max_slack_violation > 0,
            "named_lines": self.named,
        }


def line_chords(
    family: CeilingCertificate,
    *,
    thresholds: Sequence[Fraction] = DEFAULT_LINE_THRESHOLDS,
    offsets: Sequence[Fraction] = DEFAULT_LINE_OFFSETS,
    normals: Sequence[tuple[str, tuple[Fraction, Fraction]]] = LINE_NORMALS,
) -> list[LineResult]:
    """The exact maximum over every offset of the weighted chord count against its budget.

    The count is constant between interval endpoints and the budget is monotone on each
    side of the container's centre line, so ``count - budget`` is maximised at an
    endpoint of some placement's interval; every endpoint is evaluated. The named
    offsets (``y = h`` from each wall, the centre diagonals) are reported as well.
    """

    container = container_square(family)
    results: list[LineResult] = []
    for label, (nx, ny) in normals:
        line = LineFamily(label, nx, ny)
        for threshold in thresholds:
            tau = line.threshold(threshold)
            intervals = [
                (placement.weight, line.chord_interval(placement, tau))
                for placement in family.placements
            ]

            def count_at(
                s: Surd, intervals: list[tuple[Fraction, tuple[Surd, Surd] | None]] = intervals
            ) -> Fraction:
                return sum(
                    (
                        w
                        for w, interval in intervals
                        if interval and interval[0] <= s <= interval[1]
                    ),
                    start=Fraction(0),
                )

            def budget_at(s: Surd, line: LineFamily = line, tau: Surd = tau) -> int:
                extent = line.extent_at(container, s)
                if extent is None:
                    return 0
                m = 0
                while tau.scale(Fraction(m + 1)) <= extent:
                    m += 1
                return m

            best_count, best_budget, best_offset = Fraction(0), 0, "none"
            best_gap: Fraction | None = None
            tight = False
            tight_count, tight_offset = Fraction(0), "none"
            for _, interval in intervals:
                if interval is None:
                    continue
                for s in interval:
                    count = count_at(s)
                    budget = budget_at(s)
                    gap = count - budget
                    if count == budget and count > 0:
                        tight = True
                        if count > tight_count:
                            tight_count, tight_offset = count, str(s)
                    if best_gap is None or gap > best_gap:
                        best_gap = gap
                    if count > best_count or (count == best_count and budget < best_budget):
                        best_count, best_budget, best_offset = count, budget, str(s)
            named: list[dict[str, Any]] = []
            for offset in _named_offsets(line, family.outer_side, offsets):
                s = Surd(offset)
                count = count_at(s)
                budget = budget_at(s)
                named.append(
                    {
                        "offset": str(offset),
                        "weight": _f(count),
                        "budget": budget,
                        "tight": count == budget and count > 0,
                    }
                )
            results.append(
                LineResult(
                    label,
                    threshold,
                    best_count,
                    best_budget,
                    best_offset,
                    best_gap if best_gap is not None else Fraction(0),
                    tight,
                    named,
                    tight_count,
                    tight_offset,
                )
            )
    return results


def _named_offsets(
    line: LineFamily, side: Fraction, offsets: Sequence[Fraction]
) -> list[Fraction]:
    if line.norm_squared == 1:
        values = {offset for offset in offsets if 0 <= offset <= side}
        values |= {side - offset for offset in offsets if 0 <= offset <= side}
        return sorted(values)
    if line.nx * line.ny > 0:
        return [side]
    return [Fraction(0)]


# ---------------------------------------------------------------------------------
# K6: Chvátal--Gomory separation by integer programming
# ---------------------------------------------------------------------------------


@dataclass(slots=True)
class SeparationResult:
    threshold: int
    max_multiplicity: int
    total_multiplicity: int | None
    status: int
    message: str
    solver_objective: float | None
    solver_bound: float | None
    exact_objective: Fraction | None
    atom: AtomVerdict | None
    mask_atom_floor_charge: Fraction | None
    candidates: int
    seconds: float

    @property
    def claim(self) -> str:
        if self.atom is not None and self.atom.violated:
            return "violated floor atom found and verified exactly"
        if self.status == 0 and (self.solver_bound is None or self.solver_bound <= 1e-9):
            return (
                "solver reports no violated cut of this shape on the candidate points "
                "(solver claim, not a theorem)"
            )
        return "bounded search: nothing verified within the time limit"

    def record(self) -> dict[str, Any]:
        return {
            "threshold": self.threshold,
            "max_multiplicity": self.max_multiplicity,
            "total_multiplicity": self.total_multiplicity,
            "solver_status": self.status,
            "solver_message": self.message,
            "solver_objective": self.solver_objective,
            "solver_bound": self.solver_bound,
            "exact_objective": _f(self.exact_objective)
            if self.exact_objective is not None
            else None,
            "mask_floor_charge": (
                _f(self.mask_atom_floor_charge)
                if self.mask_atom_floor_charge is not None
                else None
            ),
            "atom": self.atom.record() if self.atom else None,
            "candidates": self.candidates,
            "claim": self.claim,
            "seconds": round(self.seconds, 3),
        }


def _loose(values: NDArray[Any]) -> Any:
    """scipy's stubs type constraint bounds as scalars; the solver takes arrays."""
    return values


def cg_separation(
    arrangement: Arrangement,
    threshold: int,
    *,
    max_multiplicity: int | None = None,
    total_multiplicity: int | None = None,
    time_limit: float = 60.0,
    label: str | None = None,
) -> SeparationResult:
    """Separate a floor atom with threshold ``t`` by a HiGHS integer program.

    Variables: multiplicities ``a_s`` on the candidate points (integer, at most
    ``max_multiplicity``, default ``t - 1``), ``f_P = floor(a(P) / t)`` and ``f_0 =
    floor(a(S) / t)`` (integer, enforced by ``t f_P <= a(P)`` and ``t f_0 >= a(S) - t +
    1``); objective ``sum_P y_P f_P - f_0``, the violation. ``total_multiplicity`` fixes
    ``a(S)``, which turns the program into the exact search for one shape (``5`` with
    ``t = 3`` and multiplicity one: three-of-five). The returned multiplicities are
    verified exactly, first on the membership masks and then geometrically.
    """

    started = time.perf_counter()
    if threshold < 2:
        raise ValueError("a threshold below two gives a cut the point constraints imply")
    cap = threshold - 1 if max_multiplicity is None else max_multiplicity
    masks = arrangement.masks
    m, n = len(masks), arrangement.placements
    weights = np.array([float(arrangement.rational(w)) for w in arrangement.weights])
    rows: list[int] = []
    cols: list[int] = []
    vals: list[float] = []
    for s, mask in enumerate(masks):
        for p in arrangement.members(mask):
            rows.append(p)
            cols.append(s)
            vals.append(-1.0)
    for p in range(n):
        rows.append(p)
        cols.append(m + p)
        vals.append(float(threshold))
    budget_row = n
    for s in range(m):
        rows.append(budget_row)
        cols.append(s)
        vals.append(1.0)
    rows.append(budget_row)
    cols.append(m + n)
    vals.append(-float(threshold))
    lower = np.full(n + 1, -np.inf)
    upper = np.zeros(n + 1)
    upper[budget_row] = float(threshold - 1)
    constraints = [
        LinearConstraint(
            sparse.csr_matrix((vals, (rows, cols)), shape=(n + 1, m + n + 1)),
            _loose(lower),
            _loose(upper),
        )
    ]
    if total_multiplicity is not None:
        total_row = sparse.csr_matrix(
            (np.ones(m), (np.zeros(m, dtype=int), np.arange(m))), shape=(1, m + n + 1)
        )
        constraints.append(
            LinearConstraint(total_row, float(total_multiplicity), float(total_multiplicity))
        )
    held = np.zeros(n)
    for mask in masks:
        for p in arrangement.members(mask):
            held[p] += cap
    variable_upper = np.concatenate(
        [np.full(m, float(cap)), np.floor(held / threshold), [float(cap * m // threshold)]]
    )
    objective = np.concatenate([np.zeros(m), -weights, [1.0]])
    result = milp(
        objective,
        constraints=constraints,
        integrality=np.ones(m + n + 1),
        bounds=Bounds(_loose(np.zeros(m + n + 1)), _loose(variable_upper)),
        options={"time_limit": time_limit, "disp": False},
    )
    atom = None
    exact_objective = None
    mask_floor = None
    solver_objective = None
    if result.x is not None:
        solver_objective = -float(result.fun)
        multiplicities = [round(float(v)) for v in result.x[:m]]
        points = [
            WeightedPoint(arrangement.representative[mask], a)
            for mask, a in zip(masks, multiplicities, strict=True)
            if a > 0
        ]
        if points:
            held_exact = [0] * n
            for mask, a in zip(masks, multiplicities, strict=True):
                if a:
                    for p in arrangement.members(mask):
                        held_exact[p] += a
            total = sum(multiplicities)
            mask_floor = sum(
                (
                    arrangement.rational(arrangement.weights[p]) * (held_exact[p] // threshold)
                    for p in range(n)
                ),
                start=Fraction(0),
            )
            shape = label or f"Chvátal-Gomory floor atom, t = {threshold}"
            atom = verify_atom(
                arrangement.family,
                points,
                threshold,
                label=shape,
                note=f"multiplicities from the separation program; a(S) = {total}",
            )
            if atom.floor_charge != mask_floor:
                raise ValueError(
                    "the membership masks and the geometry disagree on a returned cut"
                )
            exact_objective = atom.floor_violation
    bound = getattr(result, "mip_dual_bound", None)
    return SeparationResult(
        threshold,
        cap,
        total_multiplicity,
        int(result.status),
        str(result.message),
        solver_objective,
        -float(bound) if bound is not None else None,
        exact_objective,
        atom,
        mask_floor,
        m,
        time.perf_counter() - started,
    )


# ---------------------------------------------------------------------------------
# The reader
# ---------------------------------------------------------------------------------


@dataclass(slots=True)
class ReaderOptions:
    cg_thresholds: Sequence[int] = DEFAULT_CG_THRESHOLDS
    time_limit: float = 60.0
    shape_node_limit: int = 200_000
    line_thresholds: Sequence[Fraction] = DEFAULT_LINE_THRESHOLDS
    line_offsets: Sequence[Fraction] = DEFAULT_LINE_OFFSETS
    skip_k6: bool = False
    skip_shape: bool = False
    skip_lines: bool = False
    skip_cliques: bool = False
    progress: Callable[[str], None] | None = None


@dataclass(slots=True)
class PlateauReport:
    verdict: CeilingVerdict
    arrangement: Arrangement | None
    refused: str | None
    two_of_three: ShapeSearch | None = None
    two_of_three_atom: AtomVerdict | None = None
    three_of_five: ShapeSearch | None = None
    three_of_five_atom: AtomVerdict | None = None
    three_of_five_program: SeparationResult | None = None
    cliques: CliqueScan | None = None
    lines: list[LineResult] = field(default_factory=list)
    separations: list[SeparationResult] = field(default_factory=list)
    violated: list[AtomVerdict] = field(default_factory=list)
    statements: list[dict[str, str]] = field(default_factory=list)
    seconds: float = 0.0

    def record(self) -> dict[str, Any]:
        arrangement = self.arrangement
        verdict = self.verdict
        base: dict[str, Any] = {
            "kind": "plateau-reader/v1",
            "family": {
                "placements": len(verdict.conditions) and None,
                "total_weight": _f(verdict.total_weight),
                "max_depth": _f(verdict.max_depth),
                "vertices": verdict.vertices,
                "regime": verdict.regime,
                "symmetric_only": verdict.symmetric_only,
                "conditions": [
                    {"name": c.name, "holds": c.holds, "detail": c.detail}
                    for c in verdict.conditions
                ],
            },
            "refused": self.refused,
            "seconds": round(self.seconds, 3),
        }
        if arrangement is None:
            return base
        base["family"]["placements"] = arrangement.placements
        base["family"]["distinct_membership_sets"] = len(arrangement.masks)
        base["family"]["weight_scale"] = arrangement.scale
        base["family"]["arrangement_seconds"] = round(arrangement.seconds, 3)
        base["k4_two_of_three"] = (
            self.two_of_three.record(arrangement) if self.two_of_three else None
        )
        base["k4_two_of_three_atom"] = (
            self.two_of_three_atom.record() if self.two_of_three_atom else None
        )
        base["k4_three_of_five_search"] = (
            self.three_of_five.record(arrangement) if self.three_of_five else None
        )
        base["k4_three_of_five_atom"] = (
            self.three_of_five_atom.record() if self.three_of_five_atom else None
        )
        base["k4_three_of_five_program"] = (
            self.three_of_five_program.record() if self.three_of_five_program else None
        )
        base["k5_cliques"] = self.cliques.record(arrangement) if self.cliques else None
        base["lines"] = [line.record() for line in self.lines]
        base["k6_separation"] = [s.record() for s in self.separations]
        base["violated_atoms"] = [atom.record() for atom in self.violated]
        base["statements"] = self.statements
        return base


def _statement(family: str, searched: str, verdict: str, *, status: str) -> dict[str, str]:
    """One per class: ``status`` is ``violated``, ``feasible`` (a theorem for the class on
    this family), ``never`` (a class no depth-one family violates) or ``bounded`` (a
    search that found nothing within its bound and proves nothing)."""

    return {"family": family, "searched": searched, "verdict": verdict, "status": status}


def read_plateau(
    family: CeilingCertificate, options: ReaderOptions | None = None
) -> PlateauReport:
    """Run every search on one family and rank the exact violations found."""

    options = options or ReaderOptions()
    started = time.perf_counter()
    say = options.progress or (lambda _text: None)
    verdict = verify_ceiling(family)
    say(
        f"K0-K3: total {verdict.total_weight}, depth {verdict.max_depth}, "
        f"{verdict.vertices} vertices"
    )
    if verdict.max_depth > 1:
        return PlateauReport(
            verdict,
            None,
            f"depth {verdict.max_depth} exceeds one: not a feasible point dual",
            seconds=time.perf_counter() - started,
        )
    failures = [name for name in verdict.failures if not name.startswith("K3")]
    if failures:
        return PlateauReport(
            verdict,
            None,
            "refused: " + "; ".join(failures),
            seconds=time.perf_counter() - started,
        )
    arrangement = read_arrangement(family)
    if arrangement.rational(arrangement.max_depth) != verdict.max_depth:
        raise ValueError(
            "the membership masks and verify_ceiling disagree on the maximum depth"
        )
    say(
        f"arrangement: {len(arrangement.masks)} distinct membership sets "
        f"({arrangement.seconds:.1f}s)"
    )
    report = PlateauReport(verdict, arrangement, None)
    table = MaskTable(arrangement)

    search = two_of_three_maximum(arrangement, table)
    report.two_of_three = search
    say(
        f"K4 two-of-three: max {arrangement.rational(search.best)} over {search.nodes} pairs "
        f"({search.seconds:.1f}s)"
    )
    if search.witnesses:
        atom = shape_atom(arrangement, search.witnesses[0], 2, "two-of-three")
        if atom.threshold_charge != arrangement.rational(search.best):
            raise ValueError(
                "the two-of-three witness does not reproduce its charge geometrically"
            )
        report.two_of_three_atom = atom
        if atom.violated:
            report.violated.append(atom)
    report.statements.append(
        _statement(
            "two-of-three",
            f"all triples of distinct membership sets ({len(arrangement.masks)} sets, "
            f"{search.nodes} pairs expanded; complete by the exact pair bound)",
            "violated"
            if search.best > arrangement.scale
            else "feasible: no violated two-of-three atom exists",
            status="violated" if search.best > arrangement.scale else "feasible",
        )
    )

    if not options.skip_shape:
        shape = k_of_search(arrangement, 3, table, node_limit=options.shape_node_limit)
        report.three_of_five = shape
        say(
            f"K4 three-of-five search: max {arrangement.rational(shape.best)}, "
            f"complete={shape.complete} ({shape.seconds:.1f}s)"
        )
        if shape.witnesses:
            atom = shape_atom(arrangement, shape.witnesses[0], 3, "three-of-five")
            report.three_of_five_atom = atom
            if atom.violated:
                report.violated.append(atom)
        if not options.skip_k6:
            program = cg_separation(
                arrangement,
                3,
                max_multiplicity=1,
                total_multiplicity=5,
                time_limit=options.time_limit,
                label="three-of-five (integer program)",
            )
            report.three_of_five_program = program
            say(f"K4 three-of-five program: {program.claim} ({program.seconds:.1f}s)")
            if program.atom and program.atom.violated:
                report.violated.append(program.atom)
        shape_violated = shape.best > arrangement.scale or (
            report.three_of_five_program is not None
            and report.three_of_five_program.atom is not None
            and report.three_of_five_program.atom.violated
        )
        report.statements.append(
            _statement(
                "three-of-five",
                f"branch and bound over distinct membership sets, {shape.nodes} nodes, "
                + ("complete" if shape.complete else "node limit reached")
                + (
                    f"; integer program: {report.three_of_five_program.claim}"
                    if report.three_of_five_program
                    else ""
                ),
                "violated" if shape_violated else "nothing found within the search",
                status="violated" if shape_violated else "bounded",
            )
        )

    if not options.skip_cliques:
        cliques = clique_scan(arrangement)
        report.cliques = cliques
        say(
            f"K5 cliques: {cliques.maximal_above_one} maximal above one, heaviest rank-one "
            f"{cliques.heaviest_rank_one_weight} ({cliques.seconds:.1f}s)"
        )
        if cliques.atom is not None and cliques.atom.violated:
            report.violated.append(cliques.atom)
        report.statements.append(
            _statement(
                "budget-one atoms (weighted cliques with tau* < 2)",
                f"{cliques.maximal_above_one} maximal cliques above weight one of the "
                f"closed-intersection graph ({cliques.edges} edges), "
                f"{cliques.piercings_solved} piercing programs decided exactly, descent below "
                f"{cliques.tau_at_least_two} "
                "cliques with tau* >= 2; "
                + (
                    "complete"
                    if cliques.enumeration_complete
                    else "enumeration node limit reached"
                ),
                "violated"
                if cliques.atom is not None and cliques.atom.violated
                else "feasible: no clique of weight above one has tau* < 2",
                status="violated"
                if cliques.atom is not None and cliques.atom.violated
                else ("feasible" if cliques.enumeration_complete else "bounded"),
            )
        )

    if not options.skip_lines:
        lines = line_chords(
            family, thresholds=options.line_thresholds, offsets=options.line_offsets
        )
        report.lines = lines
        tight = [
            f"{line.direction} c={line.threshold}" for line in lines if line.tight_somewhere
        ]
        violated = [line for line in lines if line.max_slack_violation > 0]
        say(f"lines: {len(lines)} direction/threshold pairs, tight on {len(tight)}")
        report.statements.append(
            _statement(
                "line chords (collinear atoms, continuum form)",
                f"every offset of {len({line.direction for line in lines})} directions at "
                f"thresholds {[str(t) for t in options.line_thresholds]}, exact in Q(sqrt 2)",
                "violated (impossible at depth <= 1: check the family)"
                if violated
                else "never violated (theorem); tight on: " + (", ".join(tight) or "none"),
                status="violated" if violated else "never",
            )
        )

    if not options.skip_k6:
        for threshold in options.cg_thresholds:
            separation = cg_separation(arrangement, threshold, time_limit=options.time_limit)
            report.separations.append(separation)
            say(f"K6 t={threshold}: {separation.claim} ({separation.seconds:.1f}s)")
            if separation.atom is not None and separation.atom.violated:
                report.violated.append(separation.atom)
        report.statements.append(
            _statement(
                "rank-one Chvátal-Gomory floor atoms",
                f"thresholds {list(options.cg_thresholds)}, multiplicities below the "
                f"threshold, {len(arrangement.masks)} candidate points, HiGHS with "
                f"{options.time_limit}s "
                "per threshold",
                "; ".join(f"t={s.threshold}: {s.claim}" for s in report.separations),
                status="violated"
                if any(s.atom is not None and s.atom.violated for s in report.separations)
                else "bounded",
            )
        )

    report.violated.sort(
        key=lambda atom: (-atom.floor_violation, -atom.threshold_violation, atom.family)
    )
    report.seconds = time.perf_counter() - started
    return report


def summary_lines(report: PlateauReport) -> list[str]:
    """The printed summary: every number exact, with a float beside it where it helps."""

    verdict = report.verdict
    lines = [
        (
            f"family: total weight {verdict.total_weight} "
            f"({float(verdict.total_weight):.6f}), max depth {verdict.max_depth}, "
            f"{verdict.vertices} vertices, regime {verdict.regime}"
        ),
    ]
    if report.refused:
        lines.append(f"REFUSED: {report.refused}")
        return lines
    arrangement = report.arrangement
    assert arrangement is not None
    lines.append(
        f"arrangement: {arrangement.placements} placements, {len(arrangement.masks)} distinct "
        f"membership sets, weight scale 1/{arrangement.scale}"
    )
    if report.two_of_three:
        lines += _shape_lines(arrangement, report.two_of_three, "K4 two-of-three")
    if report.three_of_five:
        lines += _shape_lines(arrangement, report.three_of_five, "K4 three-of-five (bound)")
    if report.three_of_five_program:
        lines += _separation_lines(report.three_of_five_program, "K4 three-of-five (program)")
    if report.cliques:
        lines += _clique_lines(report.cliques)
    lines += [_line_summary(line) for line in report.lines]
    for separation in report.separations:
        lines += _separation_lines(separation, f"K6 t={separation.threshold}")
    lines.append("violated atoms, ranked by exact floor violation:")
    lines += [_atom_line(atom) for atom in report.violated] or ["   none"]
    lines += [
        f"{statement['family']}: {statement['verdict']} [searched: {statement['searched']}]"
        for statement in report.statements
    ]
    lines.append(f"total {report.seconds:.1f}s")
    return lines


def _shape_lines(arrangement: Arrangement, search: ShapeSearch, title: str) -> list[str]:
    value = arrangement.rational(search.best)
    state = "complete" if search.complete else "INCOMPLETE"
    lines = [
        (
            f"{title}: max {value} ({float(value):.6f}), {state} at {search.nodes} nodes, "
            f"{search.maximiser_count} maximisers, {search.seconds:.1f}s"
        )
    ]
    if search.witnesses:
        sizes = sorted(arrangement.masks[i].bit_count() for i in search.witnesses[0])
        lines.append(f"   sparsest witness memberships {sizes}")
    return lines


def _separation_lines(separation: SeparationResult, title: str) -> list[str]:
    return [
        (
            f"{title}: {separation.claim}; exact objective {separation.exact_objective}, "
            f"solver bound {separation.solver_bound}, {separation.seconds:.1f}s"
        )
    ]


def _clique_lines(scan: CliqueScan) -> list[str]:
    lines = [
        (
            f"K5 cliques: {scan.edges} edges, {scan.maximal_above_one} maximal cliques above "
            f"one, {scan.piercings_solved} piercing programs, {scan.tau_at_least_two} with "
            f"tau* >= 2, {scan.seconds:.1f}s"
        )
    ]
    if scan.heaviest_tau is not None:
        lines.append(
            f"   heaviest clique: weight {scan.heaviest_weight}, tau* {scan.heaviest_tau.value}"
        )
    if scan.heaviest_rank_one_tau is not None and scan.heaviest_rank_one_clique is not None:
        lines.append(
            f"   heaviest rank-one clique: {scan.heaviest_rank_one_clique.bit_count()} "
            f"members, weight {scan.heaviest_rank_one_weight}, "
            f"tau* {scan.heaviest_rank_one_tau.value} "
            f"({scan.heaviest_rank_one_tau.route})"
        )
    if scan.atom is not None:
        lines.append("   atom: " + _atom_line(scan.atom).strip())
    return lines


def _line_summary(line: LineResult) -> str:
    state = (
        f"tight at count {line.tight_count} (offset {line.tight_offset})"
        if line.tight_somewhere
        else "slack"
    )
    return (
        f"line {line.direction} c={line.threshold}: max weight {line.max_count} against budget "
        f"{line.max_count_budget} at offset {line.max_count_offset}; max(count - budget) = "
        f"{line.max_slack_violation}; {state}"
    )


def _atom_line(atom: AtomVerdict) -> str:
    total = sum(p.multiplicity for p in atom.points)
    return (
        f"   {atom.family}: {len(atom.points)} points (a(S) = {total}), t = {atom.threshold}, "
        f"budget {atom.budget}, threshold charge {atom.threshold_charge}, floor charge "
        f"{atom.floor_charge}, violation {atom.floor_violation}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Exact plateau reader for a ceiling family.")
    parser.add_argument("family", type=Path)
    parser.add_argument("--out", type=Path, default=None, help="write the JSON report here")
    parser.add_argument("--outer-side", type=Fraction, default=None)
    parser.add_argument("--square-side", type=Fraction, default=None)
    parser.add_argument(
        "--time-limit", type=float, default=60.0, help="seconds per integer program"
    )
    parser.add_argument(
        "--cg-thresholds",
        type=str,
        default=",".join(str(t) for t in DEFAULT_CG_THRESHOLDS),
        help="comma-separated thresholds t for the K6 separation",
    )
    parser.add_argument("--shape-node-limit", type=int, default=200_000)
    parser.add_argument("--skip-k6", action="store_true")
    parser.add_argument("--skip-shape", action="store_true")
    parser.add_argument("--skip-lines", action="store_true")
    parser.add_argument("--skip-cliques", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    family = load_family(args.family, outer_side=args.outer_side, square_side=args.square_side)
    options = ReaderOptions(
        cg_thresholds=tuple(int(t) for t in args.cg_thresholds.split(",") if t),
        time_limit=args.time_limit,
        shape_node_limit=args.shape_node_limit,
        skip_k6=args.skip_k6,
        skip_shape=args.skip_shape,
        skip_lines=args.skip_lines,
        skip_cliques=args.skip_cliques,
        progress=None if args.quiet else (lambda text: print(f"... {text}", file=sys.stderr)),
    )
    report = read_plateau(family, options)
    for line in summary_lines(report):
        print(line)
    if args.out is not None:
        record = report.record()
        record["source"] = str(args.family)
        args.out.write_text(json.dumps(record, indent=1))
    if report.refused:
        return 2
    return 0


__all__ = [
    "Arrangement",
    "AtomVerdict",
    "CliqueScan",
    "LineFamily",
    "MaskTable",
    "Piercing",
    "PlateauReport",
    "ReaderOptions",
    "SeparationResult",
    "ShapeSearch",
    "Surd",
    "WeightedPoint",
    "cg_separation",
    "clique_scan",
    "closed_squares_intersect",
    "exact_packing_simplex",
    "k_of_search",
    "line_chords",
    "load_family",
    "main",
    "maximal_cliques_above",
    "piercing_number",
    "read_arrangement",
    "read_plateau",
    "summary_lines",
    "two_of_three_maximum",
    "verify_atom",
]


if __name__ == "__main__":
    sys.exit(main())
