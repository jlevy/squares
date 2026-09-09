"""Re-optimise the weights of a retained ceiling family on its own fixed support.

A cutting run's family is the dual of a covering program on a site set: its depth
is at most 1 at the sites, and a uniform scaling then restores depth at most 1 at
every vertex of the placements' own arrangement, which is where the depth peaks.
The scaling is blunt. It pays for the worst vertex with every placement's weight,
whereas the fixed-support program -- maximise the total weight over the *same*
placements subject to depth at most 1 at every arrangement vertex -- pays only
where it must. Its optimum ``nu_S`` is the most this support can prove: a lower
bound on the fractional packing value at this side, and by weak duality
(`sqpack.fractional.ceiling`) on every covering measure's mass.

The arrangement does not depend on the weights, so its vertices are enumerated
once, in floats within the checked envelope `cutting.float_vertices` requires, and
the program is solved on a working set of vertices: those the retained weights
bring near depth 1, then whatever the last solution pushes above 1, until the
screen finds nothing new. Weights are tied over D4 orbits, which loses nothing
(averaging an optimal solution over the group keeps feasibility and the objective)
and keeps the family D4-symmetric. Floats propose and rationals confirm, as in
`cutting`: the working-set rows are exact memberships decided by
`Placement.contains`, the solution is rebuilt as the exact rational vertex of its
tight rows, an exact dual on the same rows bounds the working-set optimum from
above, and `verify_ceiling` decides the depth over every vertex of the
arrangement. What is printed as ``exact`` was decided that way; the linear
program's own numbers are labelled ``float``.

A float optimum need not be a vertex: on a degenerate face the tight rows do not
determine the free columns and no exact vertex can be read from them. The tool
then falls back to what any exact depth-feasible family gives, a verified lower
bound on the fixed-support optimum: every float weight is rounded *down* to a
multiple of ``1e-9`` (the rule of `cutting.tidy_family`), the family is verified,
and if a vertex still exceeds depth 1 every weight is scaled by the rational
``1 - 1e-6`` as many times as the exact maximum depth requires, then verified
again. The total is then an exact rational within about ``1e-5`` of the float
optimum, and the exact dual bound from the same rows still bounds the optimum
from above, so the record brackets ``nu_S`` between two rationals.

Run from ``packing/``, with ``uv run --frozen --all-extras --group dev`` in front::

    python -m devtools.polish_ceiling_family FAMILY.json --out POLISHED.json
    python -m devtools.polish_ceiling_family FAMILY.json --square-side 9977/10000 --out ...

``--square-side`` overrides the method's ``B`` the record declares; a transported
unit family that declares ``square_side`` 1 is otherwise decided in the net regime
at ``B = 1``, a weaker statement than the unit regime the transport was for. The
output is a record `devtools.replay_ceiling_family --check` reproduces, with the
program's statistics and the exact dual bound under ``provenance``.
"""

from __future__ import annotations

import argparse
import json
import math
import pickle
import subprocess
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any, TextIO

import numpy as np
from scipy import sparse
from scipy.linalg import qr as scipy_qr
from scipy.optimize import linprog

from sqpack.fractional.ceiling import (
    INTERSECTION_MARGIN,
    SCREEN_MARGIN,
    CeilingCertificate,
    CeilingVerdict,
    Line,
    Placement,
    arrangement_lines,
    depth_screening_is_safe,
    exact_intersection,
    float_family,
    intersection_screening_is_safe,
    loose_membership,
    verify_ceiling,
)
from sqpack.fractional.cutting import float_vertices

REPO = Path(__file__).resolve().parents[2]

#: Membership margin for approximate intersections: each coordinate is within
#: 1e-7 of the exact vertex, so this is the margin `cutting.screened_separation`
#: justifies for the same points.
APPROXIMATE_MARGIN = 2 * INTERSECTION_MARGIN

#: A vertex whose loosened float depth exceeds 1 by more than this is violated
#: and is always added to the working set; the loop cannot stop while one is new.
FEASIBLE = 1e-9

#: A vertex within this of depth 1 from below is near-tight: a bounded number are
#: added each pass so the exact vertex is rebuilt on the rows that will bind, but
#: they do not keep the loop going.
NEAR_TIGHT = 1e-7
NEAR_TIGHT_CAP = 5000

#: A float weight or dual below this is treated as zero when the basis is read.
ZERO = 1e-9

#: A row within this of depth 1 in floats may enter the basis of the exact rebuild.
BASIS_TOLERANCE = 1e-9

#: How many tight rows the basis is chosen from: the priced rows first, then the
#: tightest; a basis needs at most one row per free column.
BASIS_CANDIDATES = 4000

Point = tuple[Fraction, Fraction]


def rows_of(matrix: sparse.csr_matrix) -> int:
    return int(matrix.get_shape()[0])


def columns_of(matrix: sparse.csr_matrix) -> int:
    return int(matrix.get_shape()[1])


def placement_key(p: Placement) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return (p.half_tangent, p.centre_x, p.centre_y, p.side)


def d4_placement_images(
    p: Placement, side: Fraction
) -> tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...]:
    """The eight D4 images of a placement's geometry, as `cutting.symmetric_placements`
    spreads them: rotations keep the half-tangent, reflections mirror it."""

    x, y = p.centre_x, p.centre_y
    far_x, far_y = side - x, side - y
    t = p.half_tangent
    mirrored = (1 - t) / (1 + t)
    images = [
        (t, px, py, p.side) for px, py in ((x, y), (far_y, x), (far_x, far_y), (y, far_x))
    ]
    images.extend(
        (mirrored, px, py, p.side)
        for px, py in ((far_x, y), (x, far_y), (y, x), (far_y, far_x))
    )
    return tuple(images)


def d4_point_images(x: Fraction, y: Fraction, side: Fraction) -> tuple[Point, ...]:
    far_x, far_y = side - x, side - y
    return (
        (x, y),
        (far_y, x),
        (far_x, far_y),
        (y, far_x),
        (far_x, y),
        (x, far_y),
        (y, x),
        (far_y, far_x),
    )


def placement_orbits(certificate: CeilingCertificate) -> tuple[np.ndarray, int]:
    """Orbit index of every placement, and the number of orbits.

    The record must be closed under D4 and free of duplicate placements; anything
    else is a family this tool was not written for, and it says so.
    """

    keys = [placement_key(p) for p in certificate.placements]
    index = {key: i for i, key in enumerate(keys)}
    if len(index) != len(keys):
        raise ValueError("the record repeats a placement; merge duplicates first")
    orbit = np.full(len(keys), -1, dtype=np.int64)
    count = 0
    for i, p in enumerate(certificate.placements):
        if orbit[i] >= 0:
            continue
        for image in d4_placement_images(p, certificate.outer_side):
            j = index.get(image)
            if j is None:
                raise ValueError(f"placement {i} has a D4 image missing from the record")
            orbit[j] = count
        count += 1
    return orbit, count


@dataclass(slots=True)
class Arrangement:
    """The support's arrangement in floats, enumerated once, with a loose membership
    matrix good for any weights: rows are approximate vertices, columns placements."""

    lines: list[Line]
    points: np.ndarray
    pairs: np.ndarray
    cache: dict[int, Point]
    membership: sparse.csr_matrix

    @property
    def size(self) -> int:
        return int(self.points.shape[0])

    def exact_point(self, index: int) -> Point | None:
        """The exact vertex behind an approximate one, rebuilt from its two lines."""

        exact = self.cache.get(index)
        if exact is None:
            exact = exact_intersection(
                self.lines[int(self.pairs[index, 0])], self.lines[int(self.pairs[index, 1])]
            )
        return exact


def enumerate_arrangement(certificate: CeilingCertificate) -> Arrangement:
    """Every vertex of the arrangement, and which placements loosely contain it."""

    lines = arrangement_lines(certificate)
    if not intersection_screening_is_safe(certificate, lines) or not depth_screening_is_safe(
        certificate
    ):
        raise ValueError("the family is outside the floating envelope the screen needs")
    points, pairs, cache = float_vertices(certificate, lines)
    normals, offsets, halves, _ = float_family(certificate)
    blocks = []
    chunk = max(1, 2_000_000 // max(1, len(certificate.placements)))
    for start in range(0, points.shape[0], chunk):
        loose = loose_membership(
            points[start : start + chunk], normals, offsets, halves, margin=APPROXIMATE_MARGIN
        )
        blocks.append(sparse.csr_matrix(loose, dtype=np.int8))
    membership = (
        sparse.csr_matrix(sparse.vstack(blocks)) if blocks else sparse.csr_matrix((0, 0))
    )
    return Arrangement(lines, points, pairs, cache, membership)


def exact_membership(
    certificate: CeilingCertificate,
    vertex: Point,
    normals: np.ndarray,
    offsets: np.ndarray,
    halves: np.ndarray,
) -> np.ndarray:
    """Indices of the placements that contain the exact vertex.

    The float screen on the rounded exact point decides the clear cases within the
    checked `SCREEN_MARGIN`; a placement whose edge passes within the margin is
    decided by `Placement.contains`.
    """

    point = np.array([[float(vertex[0]), float(vertex[1])]])
    first = np.abs(point @ normals[:, 0, :].T - offsets[None, :, 0])
    second = np.abs(point @ normals[:, 1, :].T - offsets[None, :, 1])
    loose = (first <= halves[None, :] + SCREEN_MARGIN) & (
        second <= halves[None, :] + SCREEN_MARGIN
    )
    strict = (first <= halves[None, :] - SCREEN_MARGIN) & (
        second <= halves[None, :] - SCREEN_MARGIN
    )
    members = [int(i) for i in np.flatnonzero(strict[0])]
    members.extend(
        int(index)
        for index in np.flatnonzero(loose[0] & ~strict[0])
        if certificate.placements[int(index)].contains(*vertex)
    )
    return np.array(sorted(members), dtype=np.int64)


@dataclass(slots=True)
class WorkingSet:
    """Exact vertices with exact membership rows, in the order they were added."""

    vertices: list[Point] = field(default_factory=list)
    rows: list[np.ndarray] = field(default_factory=list)
    index: dict[Point, int] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.vertices)

    def add(self, vertex: Point, members: np.ndarray) -> bool:
        if vertex in self.index:
            return False
        self.index[vertex] = len(self.vertices)
        self.vertices.append(vertex)
        self.rows.append(members)
        return True

    def matrix(self, columns: np.ndarray, width: int) -> sparse.csr_matrix:
        """Rows over ``columns[placement]`` (orbit or placement index), summing
        placements that share a column."""

        rows = np.concatenate(
            [np.full(len(members), r, dtype=np.int64) for r, members in enumerate(self.rows)]
        )
        cols = columns[np.concatenate(self.rows)]
        data = np.ones(rows.size)
        matrix = sparse.coo_matrix((data, (rows, cols)), shape=(len(self.rows), width))
        return sparse.csr_matrix(matrix)


@dataclass(slots=True)
class Solution:
    """One working-set solve, in floats."""

    weights: np.ndarray
    duals: np.ndarray
    objective: float
    status: str


def solve_working_set(matrix: sparse.csr_matrix, objective: np.ndarray) -> Solution:
    """Maximise ``objective . z`` subject to ``matrix z <= 1`` and ``0 <= z <= 1``.

    The upper bound is implied by the full program -- a placement's own corners
    are arrangement vertices in the container, where its weight alone is a depth
    -- and keeps a working set that has not yet seen a column from making the
    program unbounded.
    """

    result = linprog(
        -objective,
        A_ub=matrix,
        b_ub=np.ones(rows_of(matrix)),
        bounds=(0, 1),
        method="highs-ds",
    )
    if result.status != 0:
        raise RuntimeError(f"the working-set program failed: {result.message}")
    return Solution(result.x, -result.ineqlin.marginals, -result.fun, result.message)


def rational_solve(rows: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction] | None:
    """The unique exact solution of a consistent full-column-rank system, or None."""

    if not rows:
        return None
    width = len(rows[0])
    augmented = [[*row, value] for row, value in zip(rows, rhs, strict=True)]
    r = 0
    for c in range(width):
        pivot = next((i for i in range(r, len(augmented)) if augmented[i][c] != 0), None)
        if pivot is None:
            return None
        augmented[r], augmented[pivot] = augmented[pivot], augmented[r]
        scale = augmented[r][c]
        augmented[r] = [v / scale for v in augmented[r]]
        for i in range(len(augmented)):
            if i != r and augmented[i][c] != 0:
                factor = augmented[i][c]
                augmented[i] = [
                    a - factor * b for a, b in zip(augmented[i], augmented[r], strict=True)
                ]
        r += 1
    for i in range(r, len(augmented)):
        if augmented[i][width] != 0:
            return None
    return [augmented[i][width] for i in range(width)]


def integer_depths(
    matrix: sparse.csr_matrix, weights: Sequence[Fraction]
) -> tuple[list[int], int]:
    """Every row's exact depth as an integer over one common denominator."""

    denominator = 1
    for w in weights:
        denominator = denominator * w.denominator // math.gcd(denominator, w.denominator)
    numerators = [int(w * denominator) for w in weights]
    widest = max(1, int(matrix.sum(axis=1).max())) if rows_of(matrix) else 1
    bound = max((abs(n) for n in numerators), default=0) * widest
    if bound < 2**62:
        counts = sparse.csr_matrix(matrix, dtype=np.int64)
        depth = counts @ np.array(numerators, dtype=np.int64)
        return [int(d) for d in depth], denominator
    coo = matrix.tocoo()
    depth = [0] * rows_of(matrix)
    for r, c, v in zip(coo.row, coo.col, coo.data, strict=True):
        depth[int(r)] += int(v) * numerators[int(c)]
    return depth, denominator


def exact_feasible(matrix: sparse.csr_matrix, weights: Sequence[Fraction]) -> bool:
    """Whether every working-set row has exact depth at most 1 under the weights."""

    depth, denominator = integer_depths(matrix, weights)
    return all(d <= denominator for d in depth)


def exact_dual_bound(
    matrix: sparse.csr_matrix, objective: np.ndarray, rows: list[int], duals: list[Fraction]
) -> Fraction:
    """The exact upper bound any nonnegative dual gives on the working-set program.

    With ``0 <= z <= 1`` and ``A z <= 1``, for every ``u >= 0`` the objective is
    at most ``sum u + sum_P max(0, c_P - (A^T u)_P)``; at the optimal dual the
    second sum is the reduced cost of the columns held at 1 and the bound is tight.
    """

    if any(u < 0 for u in duals):
        raise ValueError("a dual bound needs nonnegative duals")
    priced = [Fraction(0)] * columns_of(matrix)
    sub = matrix[rows].tocoo()
    for r, c, v in zip(sub.row, sub.col, sub.data, strict=True):
        priced[int(c)] += duals[int(r)] * int(v)
    bound = sum(duals, Fraction(0))
    for column, value in enumerate(priced):
        short = Fraction(int(objective[column])) - value
        if short > 0:
            bound += short
    return bound


class RebuildError(RuntimeError):
    """The float solution did not rebuild as an exact feasible vertex; says why."""


@dataclass(slots=True)
class ExactVertex:
    """The exact rational optimum on the working set and its certificate."""

    weights: list[Fraction]
    total: Fraction
    basis_rows: int
    support: int
    at_bound: int
    dual_bound: Fraction | None
    dual_exact: bool
    dual_rows: int
    kind: str = "vertex"
    scalings: int = 0


#: The rounding quantum of the fallback, and the factor each scaling applies.
FALLBACK_DENOMINATOR = 10**9
FALLBACK_FACTOR = Fraction(999_999, 1_000_000)


def rounded_vertex(
    matrix: sparse.csr_matrix, objective: np.ndarray, solution: Solution
) -> ExactVertex:
    """The float solution with every weight rounded down to a multiple of
    ``1 / FALLBACK_DENOMINATOR``, and the exact dual bound of its rows.

    Depth is monotone in the weights, so rounding down keeps every row the float
    solution satisfied; a row it violated within the solver's tolerance may still
    exceed 1 by that much, which `scaled_vertex` removes once the verifier has
    measured the exact excess.
    """

    weights = [
        max(
            Fraction(0),
            Fraction(math.floor(float(z) * FALLBACK_DENOMINATOR), FALLBACK_DENOMINATOR),
        )
        for z in solution.weights
    ]
    total = sum(
        (Fraction(int(c)) * w for c, w in zip(objective, weights, strict=True)), Fraction(0)
    )
    positive = [int(i) for i in np.flatnonzero(solution.duals > ZERO)]
    duals = [Fraction(float(solution.duals[i])).limit_denominator(10**12) for i in positive]
    dual_bound = exact_dual_bound(matrix, objective, positive, duals) if positive else None
    return ExactVertex(
        weights,
        total,
        basis_rows=0,
        support=sum(1 for w in weights if w > 0),
        at_bound=sum(1 for w in weights if w == 1),
        dual_bound=dual_bound,
        dual_exact=False,
        dual_rows=len(positive),
        kind="rounded",
    )


def scaled_vertex(
    exact: ExactVertex, objective: np.ndarray, max_depth: Fraction
) -> ExactVertex:
    """The same weights scaled by ``FALLBACK_FACTOR`` as often as the exact maximum
    depth requires to fall to at most 1."""

    scalings = 0
    factor = Fraction(1)
    while max_depth * factor > 1:
        factor *= FALLBACK_FACTOR
        scalings += 1
    weights = [w * factor for w in exact.weights]
    total = sum(
        (Fraction(int(c)) * w for c, w in zip(objective, weights, strict=True)), Fraction(0)
    )
    return ExactVertex(
        weights,
        total,
        basis_rows=exact.basis_rows,
        support=exact.support,
        at_bound=exact.at_bound,
        dual_bound=exact.dual_bound,
        dual_exact=exact.dual_exact,
        dual_rows=exact.dual_rows,
        kind="rounded",
        scalings=exact.scalings + scalings,
    )


def exact_vertex(
    matrix: sparse.csr_matrix, objective: np.ndarray, solution: Solution
) -> ExactVertex:
    """Rebuild the float solution as the exact vertex of a basis of its tight rows,
    with an exact dual bound; `RebuildError` says why when no basis does.

    Columns at the upper bound are held at 1 exactly. Among the tight rows, those
    the solver priced come first, and a float pivoted QR picks a full-rank basis
    for the free columns -- a heuristic that only chooses which square rational
    system to solve; feasibility of the result on every working-set row and the
    dual bound are decided exactly.
    """

    z = solution.weights
    at_one = [int(i) for i in np.flatnonzero(z > 1 - ZERO)]
    free = [int(i) for i in np.flatnonzero((z > ZERO) & (z <= 1 - ZERO))]
    depth = np.asarray(matrix @ z).ravel()
    tight = np.flatnonzero(depth >= 1 - BASIS_TOLERANCE)
    order = tight[np.lexsort((-depth[tight], -solution.duals[tight]))][:BASIS_CANDIDATES]
    found: list[Fraction] | None = None
    basis_rows = 0
    if free:
        dense = matrix[order][:, free].toarray()
        factors: Any = scipy_qr(dense.T, mode="economic", pivoting=True)
        r, pivots = factors[1], factors[2]
        diagonal = np.abs(np.diag(r))
        rank = int(np.count_nonzero(diagonal > 1e-9 * max(1.0, float(diagonal[0]))))
        if rank < len(free):
            msg = f"tight rows span rank {rank} for {len(free)} free columns"
            raise RebuildError(msg)
        chosen = [int(order[i]) for i in pivots[:rank]]
        system = matrix[chosen][:, free].toarray()
        held = (
            np.asarray(matrix[chosen][:, at_one].sum(axis=1)).ravel()
            if at_one
            else np.zeros(rank)
        )
        rows = [[Fraction(int(v)) for v in row] for row in system]
        rhs = [Fraction(1) - Fraction(int(held[i])) for i in range(rank)]
        values = rational_solve(rows, rhs)
        if values is None:
            msg = "the chosen basis rows are singular in exact arithmetic"
            raise RebuildError(msg)
        if any(v < 0 or v > 1 for v in values):
            worst = min(values) if min(values) < 0 else max(values)
            msg = f"the exact basis solution leaves [0, 1]: {worst}"
            raise RebuildError(msg)
        candidate = [Fraction(0)] * columns_of(matrix)
        for i in at_one:
            candidate[i] = Fraction(1)
        for i, v in zip(free, values, strict=True):
            candidate[i] = v
        depth_int, denominator = integer_depths(matrix, candidate)
        excess = max(depth_int) - denominator
        if excess > 0:
            msg = (
                f"the exact basis solution has depth 1 + {Fraction(excess, denominator)} "
                "on a working-set row"
            )
            raise RebuildError(msg)
        found, basis_rows = candidate, rank
    elif at_one:
        candidate = [Fraction(0)] * columns_of(matrix)
        for i in at_one:
            candidate[i] = Fraction(1)
        if not exact_feasible(matrix, candidate):
            msg = "the columns at bound 1 alone exceed depth 1 on a working-set row"
            raise RebuildError(msg)
        found = candidate
    if found is None:
        msg = "the float solution has no positive column"
        raise RebuildError(msg)
    total = sum(
        (Fraction(int(c)) * w for c, w in zip(objective, found, strict=True)), Fraction(0)
    )
    positive = [int(i) for i in np.flatnonzero(solution.duals > ZERO)]
    duals: list[Fraction] | None = None
    if positive and free:
        system = matrix[positive][:, free].toarray().T
        rows = [[Fraction(int(v)) for v in row] for row in system]
        duals = rational_solve(rows, [Fraction(int(objective[i])) for i in free])
        if duals is not None and any(u < 0 for u in duals):
            duals = None
    dual_exact = duals is not None
    if duals is None:
        duals = [Fraction(float(solution.duals[i])).limit_denominator(10**12) for i in positive]
    dual_bound = exact_dual_bound(matrix, objective, positive, duals) if positive else None
    return ExactVertex(
        found,
        total,
        basis_rows,
        len(free) + len(at_one),
        len(at_one),
        dual_bound,
        dual_exact,
        len(positive),
    )


@dataclass(slots=True)
class PolishLog:
    """Every stage of one polish, as JSON-ready dictionaries, echoed to the sink."""

    iterations: list[dict[str, Any]] = field(default_factory=list)
    stopped: str = ""
    sink: TextIO | None = None

    def record(self, entry: dict[str, Any]) -> None:
        self.iterations.append(entry)
        if self.sink is not None:
            self.sink.write(json.dumps(entry) + "\n")
            self.sink.flush()


@dataclass(slots=True)
class Polished:
    """What the polish decided: the family, its exact vertex, the verdict, the
    working set it was decided on, and the column of every placement."""

    family: CeilingCertificate
    exact: ExactVertex
    verdict: CeilingVerdict
    working: WorkingSet
    columns: np.ndarray
    duals: np.ndarray
    log: PolishLog


def with_weights(
    certificate: CeilingCertificate, weights: Sequence[Fraction]
) -> CeilingCertificate:
    return CeilingCertificate(
        certificate.n,
        certificate.outer_side,
        certificate.square_side,
        certificate.half_tangents,
        tuple(
            Placement(p.half_tangent, p.centre_x, p.centre_y, w, p.side)
            for p, w in zip(certificate.placements, weights, strict=True)
        ),
    )


def polish(
    certificate: CeilingCertificate,
    *,
    start_depth: float = 0.98,
    cap: int = 20000,
    max_iterations: int = 60,
    symmetric: bool = True,
    verify_rounds: int = 3,
    log: PolishLog | None = None,
    dump_path: Path | None = None,
) -> Polished:
    """The exact fixed-support optimum, decided."""

    log = log if log is not None else PolishLog()
    orbit, count = placement_orbits(certificate)
    if symmetric:
        columns, width = orbit, count
    else:
        columns, width = np.arange(len(certificate.placements)), len(certificate.placements)
    objective = np.bincount(columns, minlength=width).astype(float)
    started = time.perf_counter()
    arrangement = enumerate_arrangement(certificate)
    log.record(
        {
            "stage": "arrangement",
            "vertices": arrangement.size,
            "nonzeros": int(arrangement.membership.nnz),
            "seconds": round(time.perf_counter() - started, 1),
        }
    )
    normals, offsets, halves, _ = float_family(certificate)
    working = WorkingSet()
    side = certificate.outer_side

    def add_vertex(vertex: Point) -> int:
        if not (0 <= vertex[0] <= side and 0 <= vertex[1] <= side):
            return 0
        images = (vertex,) if symmetric else d4_point_images(vertex[0], vertex[1], side)
        added = 0
        for image in images:
            if image not in working.index:
                working.add(
                    image, exact_membership(certificate, image, normals, offsets, halves)
                )
                added += 1
        return added

    def add_candidates(candidates: np.ndarray, depth: np.ndarray, limit: int) -> int:
        added = 0
        order = candidates[np.argsort(-depth[candidates], kind="stable")]
        for index in order[:limit]:
            vertex = arrangement.exact_point(int(index))
            if vertex is None or vertex in working.index:
                continue
            added += add_vertex(vertex)
        return added

    # Every placement's corners first, so that no column starts unconstrained;
    # then the vertices the retained weights already bring near depth 1.
    for p in certificate.placements:
        for corner in p.corners():
            add_vertex(corner)
    weights = np.array([float(p.weight) for p in certificate.placements])
    depth = np.asarray(arrangement.membership @ weights).ravel()
    add_candidates(np.flatnonzero(depth >= start_depth), depth, cap)
    exact: ExactVertex | None = None
    verdict: CeilingVerdict | None = None
    solution: Solution | None = None
    polished = certificate
    round_index = 0
    for iteration in range(max_iterations):
        started = time.perf_counter()
        matrix = working.matrix(columns, width)
        solution = solve_working_set(matrix, objective)
        weights = solution.weights[columns]
        depth = np.asarray(arrangement.membership @ weights).ravel()
        violated = np.flatnonzero(depth > 1 + FEASIBLE)
        near = np.flatnonzero((depth >= 1 - NEAR_TIGHT) & (depth <= 1 + FEASIBLE))
        added = add_candidates(violated, depth, cap)
        added_near = add_candidates(near, depth, NEAR_TIGHT_CAP)
        log.record(
            {
                "stage": "solve",
                "iteration": iteration,
                "rows": rows_of(matrix),
                "columns": int(width),
                "objective_float": solution.objective,
                "screen_max_depth_float": float(depth.max()) if depth.size else 0.0,
                "screen_violated": int(violated.size),
                "screen_near_tight": int(near.size),
                "added_violated": added,
                "added_near_tight": added_near,
                "seconds": round(time.perf_counter() - started, 1),
            }
        )
        if added:
            continue
        started = time.perf_counter()
        if dump_path is not None:
            dump_path.write_bytes(
                pickle.dumps(
                    {
                        "vertices": working.vertices,
                        "rows": working.rows,
                        "columns": columns,
                        "objective": objective,
                        "weights": solution.weights,
                        "duals": solution.duals,
                        "objective_float": solution.objective,
                    }
                )
            )
        try:
            exact = exact_vertex(matrix, objective, solution)
        except RebuildError as error:
            log.record(
                {
                    "stage": "exact",
                    "failed": str(error),
                    "fallback": "float weights rounded down to multiples of 1e-9",
                }
            )
            exact = rounded_vertex(matrix, objective, solution)
        polished = with_weights(certificate, [exact.weights[int(c)] for c in columns])
        verdict = verify_ceiling(polished)
        log.record(
            {
                "stage": "exact",
                "round": round_index,
                "kind": exact.kind,
                "scalings": exact.scalings,
                "total": str(exact.total),
                "total_float": float(exact.total),
                "basis_rows": exact.basis_rows,
                "support": exact.support,
                "at_bound": exact.at_bound,
                "dual_bound": None if exact.dual_bound is None else str(exact.dual_bound),
                "dual_exact": exact.dual_exact,
                "dual_rows": exact.dual_rows,
                "max_depth": str(verdict.max_depth),
                "vertices": verdict.vertices,
                "decided_exactly": verdict.decided_exactly,
                "seconds": round(time.perf_counter() - started, 1),
            }
        )
        if verdict.max_depth <= 1:
            log.stopped = (
                f"exact {exact.kind} feasible at every vertex after {iteration + 1} solves"
            )
            break
        round_index += 1
        if round_index >= verify_rounds:
            log.stopped = (
                f"the exact {exact.kind} kept exceeding depth 1 outside the working set"
            )
            break
        if exact.kind == "rounded":
            # A rounded family is scaled down by the excess the verifier measured and
            # verified again; nothing is re-solved.
            exact = scaled_vertex(exact, objective, verdict.max_depth)
            polished = with_weights(certificate, [exact.weights[int(c)] for c in columns])
            verdict = verify_ceiling(polished)
            log.record(
                {
                    "stage": "exact",
                    "round": round_index,
                    "kind": exact.kind,
                    "scalings": exact.scalings,
                    "total": str(exact.total),
                    "total_float": float(exact.total),
                    "max_depth": str(verdict.max_depth),
                    "vertices": verdict.vertices,
                    "decided_exactly": verdict.decided_exactly,
                }
            )
            if verdict.max_depth <= 1:
                log.stopped = f"rounded family feasible after {exact.scalings} scalings"
                break
            continue
        for vertex in offending_vertices(polished, arrangement):
            add_vertex(vertex)
    else:
        log.stopped = f"iteration cap {max_iterations} reached"
    if exact is None or verdict is None or solution is None:
        raise RuntimeError(log.stopped or "the polish produced no exact vertex")
    return Polished(polished, exact, verdict, working, columns, solution.duals, log)


def offending_vertices(family: CeilingCertificate, arrangement: Arrangement) -> list[Point]:
    """Every exact vertex whose exact depth exceeds 1 under the family's weights,
    found by the loose screen and decided exactly."""

    weights = np.array([float(p.weight) for p in family.placements])
    depth = np.asarray(arrangement.membership @ weights).ravel()
    normals, offsets, halves, _ = float_family(family)
    found: list[Point] = []
    seen: set[Point] = set()
    side = family.outer_side
    for index in np.flatnonzero(depth >= 1 - NEAR_TIGHT):
        vertex = arrangement.exact_point(int(index))
        if vertex is None or vertex in seen:
            continue
        seen.add(vertex)
        if not (0 <= vertex[0] <= side and 0 <= vertex[1] <= side):
            continue
        members = exact_membership(family, vertex, normals, offsets, halves)
        exact = sum((family.placements[int(i)].weight for i in members), Fraction(0))
        if exact > 1:
            found.append(vertex)
    return found


def git_commit() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True, check=True
        ).stdout.strip()
    except OSError, subprocess.CalledProcessError:
        return None


def polished_record(result: Polished, *, source: Path, symmetric: bool) -> dict[str, Any]:
    """The polished family as `CeilingCertificate.from_record` reads it, with the
    program's statistics and the verifier's verdict under ``provenance``."""

    family, exact, verdict = result.family, result.exact, result.verdict
    record = family.to_record()
    record["total_weight"] = str(family.total_weight)
    record["total_weight_float"] = float(family.total_weight)
    record["provenance"] = {
        "tool": "devtools.polish_ceiling_family",
        "source": {"path": str(source), "git_commit": git_commit()},
        "program": {
            "variables": "D4 orbits, images tied" if symmetric else "placements",
            "working_set_vertices": len(result.working),
            "kind": exact.kind,
            "scalings": exact.scalings,
            "basis_rows": exact.basis_rows,
            "support": exact.support,
            "at_bound": exact.at_bound,
            "exact_total": str(exact.total),
            "exact_dual_bound": None if exact.dual_bound is None else str(exact.dual_bound),
            "dual_exact": exact.dual_exact,
            "dual_rows": exact.dual_rows,
            "iterations": result.log.iterations,
            "stopped": result.log.stopped,
        },
        "verify_ceiling": {
            "proved": verdict.proved,
            "failures": list(verdict.failures),
            "max_depth": str(verdict.max_depth),
            "vertices": verdict.vertices,
            "decided_exactly": verdict.decided_exactly,
            "total_weight": str(verdict.total_weight),
            "regime": verdict.regime,
            "symmetric_only": verdict.symmetric_only,
            "statement": verdict.statement,
        },
    }
    return record


def load_family(path: Path, square_side: Fraction | None) -> CeilingCertificate:
    data = json.loads(path.read_text())
    record = data.get("best_family", data)
    if square_side is not None:
        record = dict(record)
        record["square_side"] = str(square_side)
    return CeilingCertificate.from_record(record)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--out", type=Path, help="write the polished family record here")
    parser.add_argument(
        "--square-side", type=Fraction, help="the method's B to declare, overriding the record"
    )
    parser.add_argument(
        "--start-depth",
        type=float,
        default=0.98,
        help="initial working set: vertices of float depth at least this",
    )
    parser.add_argument(
        "--cap", type=int, default=20000, help="vertices added per iteration at most"
    )
    parser.add_argument(
        "--per-placement",
        action="store_true",
        help="one variable per placement instead of per D4 orbit (same optimum, larger)",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="echo every stage to stderr as it completes"
    )
    parser.add_argument(
        "--dump", type=Path, help="pickle the working set and float solution before the rebuild"
    )
    parser.add_argument(
        "--working-set",
        type=Path,
        help="write the final working-set vertices here, each with its float dual",
    )
    arguments = parser.parse_args(argv)
    certificate = load_family(arguments.path, arguments.square_side)
    started = time.perf_counter()
    result = polish(
        certificate,
        start_depth=arguments.start_depth,
        cap=arguments.cap,
        symmetric=not arguments.per_placement,
        log=PolishLog(sink=sys.stderr if arguments.verbose else None),
        dump_path=arguments.dump,
    )
    seconds = time.perf_counter() - started
    record = polished_record(
        result, source=arguments.path, symmetric=not arguments.per_placement
    )
    if arguments.out is not None:
        arguments.out.parent.mkdir(parents=True, exist_ok=True)
        arguments.out.write_text(json.dumps(record) + "\n")
    if arguments.working_set is not None:
        # Rows added after the last solve (near-tight, never priced) carry dual 0.
        duals = np.concatenate(
            [result.duals, np.zeros(len(result.working) - result.duals.size)]
        )
        arguments.working_set.write_text(
            json.dumps(
                [
                    [str(x), str(y), float(u)]
                    for (x, y), u in zip(result.working.vertices, duals, strict=True)
                ]
            )
            + "\n"
        )
    exact, verdict = result.exact, result.verdict
    print(
        json.dumps(
            {
                "path": str(arguments.path),
                "placements": len(result.family.placements),
                "source_total_float": float(certificate.total_weight),
                "kind": exact.kind,
                "scalings": exact.scalings,
                "exact_total": str(exact.total),
                "exact_total_float": float(exact.total),
                "exact_dual_bound": None if exact.dual_bound is None else str(exact.dual_bound),
                "dual_exact": exact.dual_exact,
                "dual_gap_float": (
                    None if exact.dual_bound is None else float(exact.dual_bound - exact.total)
                ),
                "working_set_vertices": len(result.working),
                "max_depth": str(verdict.max_depth),
                "vertices": verdict.vertices,
                "proved": verdict.proved,
                "failures": list(verdict.failures),
                "regime": verdict.regime,
                "stopped": result.log.stopped,
                "seconds": round(seconds, 1),
            }
        )
    )
    return 0 if verdict.max_depth <= 1 else 1


if __name__ == "__main__":
    sys.exit(main())
