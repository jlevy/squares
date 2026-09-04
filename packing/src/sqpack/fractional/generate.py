"""Generate weighted fractional unavoidable-set certificates by row generation.

The certificate that `sqpack.fractional.certificate` verifies is the optimum of
a covering linear program: put weights on a grid of candidate sites so that
every placement of a shrunken square covers mass at least 1, and minimise the
total mass. When that optimum falls strictly below ``n``, the rounded solution
is a certificate for ``s(n) >= L``.

The program has one constraint per placement, which is a continuum, so the rows
are generated rather than enumerated. The separation oracle is the same
event-cell sweep the verifier uses: at fixed weights it returns the placements
of least mass, and any below 1 become new rows. Between net directions nothing
is sampled -- the containment condition covers those angles, which is the whole
reason the net is finite.

Search runs in floating point because it is a search; the certificate it
proposes is rationalised and then re-decided by the exact verifier, which is
the only thing that decides anything.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog

from sqpack.fractional.certificate import Certificate, verify
from sqpack.fractional.model import Atom, Direction, rotation_from_half_tangent


@dataclass(frozen=True, slots=True)
class SiteGrid:
    """D4-symmetric candidate atom sites, and the orbit each belongs to."""

    outer_side: Fraction
    coordinates: tuple[Fraction, ...]
    orbits: tuple[tuple[tuple[int, int], ...], ...]

    @property
    def size(self) -> int:
        return len(self.coordinates)

    def positions(self) -> tuple[tuple[Fraction, Fraction], ...]:
        return tuple(
            (self.coordinates[i], self.coordinates[j])
            for orbit in self.orbits
            for i, j in orbit
        )


def build_site_grid(outer_side: Fraction, count: int, inset: Fraction) -> SiteGrid:
    """A square grid inset from the container wall, folded into D4 orbits."""

    if count < 2:
        raise ValueError("the site grid needs at least two coordinates per axis")
    span = outer_side - 2 * inset
    if span <= 0:
        raise ValueError("the inset leaves no room for sites")
    step = span / (count - 1)
    coordinates = tuple(inset + step * index for index in range(count))
    last = count - 1
    seen: set[tuple[int, int]] = set()
    orbits: list[tuple[tuple[int, int], ...]] = []
    for i in range(count):
        for j in range(count):
            if (i, j) in seen:
                continue
            orbit = {
                (i, j),
                (last - i, j),
                (i, last - j),
                (last - i, last - j),
                (j, i),
                (last - j, i),
                (j, last - i),
                (last - j, last - i),
            }
            seen |= orbit
            orbits.append(tuple(sorted(orbit)))
    return SiteGrid(outer_side, coordinates, tuple(orbits))


def _net(limit: Fraction, steps: int) -> tuple[Fraction, ...]:
    return tuple(limit * index / steps for index in range(steps + 1))


def _rotations(half_tangents: tuple[Fraction, ...]) -> tuple[Direction, ...]:
    return tuple(
        rotation_from_half_tangent(str(index), tangent)
        for index, tangent in enumerate(half_tangents)
    )


def _worst_cells(
    points: np.ndarray,
    weights: np.ndarray,
    direction: Direction,
    outer_side: float,
    square_side: float,
    *,
    keep: int,
) -> list[tuple[float, np.ndarray]]:
    """Least-mass placements at one direction, as (mass, covering-site mask).

    Mirrors the verifier's reduction in floating point: project the sites, take
    the coordinates where coverage can change as the event grid, accumulate a
    two-dimensional difference array, and read the cells the centre domain can
    actually reach.
    """
    cosine, sine = float(direction.ux), float(direction.uy)
    half = square_side / 2
    u = points[:, 0] * cosine + points[:, 1] * sine
    v = -points[:, 0] * sine + points[:, 1] * cosine

    extent = square_side * (cosine + sine) / 2
    corners = np.array(
        [
            [extent, extent],
            [outer_side - extent, extent],
            [outer_side - extent, outer_side - extent],
            [extent, outer_side - extent],
        ]
    )
    cu = corners[:, 0] * cosine + corners[:, 1] * sine
    cv = -corners[:, 0] * sine + corners[:, 1] * cosine
    u_lo, u_hi = cu.min(), cu.max()
    v_lo, v_hi = cv.min(), cv.max()

    u_events = np.unique(np.concatenate([u - half, u + half, [u_lo, u_hi]]))
    v_events = np.unique(np.concatenate([v - half, v + half, [v_lo, v_hi]]))
    grid = np.zeros((u_events.size, v_events.size))
    left = np.searchsorted(u_events, u - half)
    right = np.searchsorted(u_events, u + half)
    bottom = np.searchsorted(v_events, v - half)
    top = np.searchsorted(v_events, v + half)
    np.add.at(grid, (left, bottom), weights)
    np.add.at(grid, (right, bottom), -weights)
    np.add.at(grid, (left, top), -weights)
    np.add.at(grid, (right, top), weights)
    mass = np.cumsum(np.cumsum(grid, axis=1), axis=0)[:-1, :-1]

    u_mid = (u_events[:-1] + u_events[1:]) / 2
    v_mid = (v_events[:-1] + v_events[1:]) / 2
    # The centre domain is a rotated square, not its bounding box. Testing the
    # box admits placements that hang outside the container, and those cover no
    # site at all -- which reads as an infeasible program rather than as the
    # oversight it is. Rotate each cell centre back and test it where it lives.
    back_x = u_mid[:, None] * cosine - v_mid[None, :] * sine
    back_y = u_mid[:, None] * sine + v_mid[None, :] * cosine
    inside = (
        (back_x >= extent)
        & (back_x <= outer_side - extent)
        & (back_y >= extent)
        & (back_y <= outer_side - extent)
    )
    scored = np.where(inside, mass, np.inf)
    flat = scored.ravel()
    order = np.argpartition(flat, min(keep, flat.size - 1))[:keep]
    order = order[np.isfinite(flat[order])]

    found = []
    for index in order[np.argsort(flat[order])]:
        i, j = divmod(int(index), v_mid.size)
        cu_, cv_ = u_mid[i], v_mid[j]
        covers = (np.abs(u - cu_) <= half) & (np.abs(v - cv_) <= half)
        found.append((float(flat[index]), covers))
    return found


@dataclass(slots=True)
class GenerationLog:
    rounds: int = 0
    rows: int = 0
    objective: float = float("inf")
    stopped: str = ""


def solve_covering_lp(
    grid: SiteGrid,
    square_side: Fraction,
    half_tangents: tuple[Fraction, ...],
    *,
    max_rounds: int = 60,
    rows_per_direction: int = 3,
    tolerance: float = 1e-9,
) -> tuple[np.ndarray, GenerationLog]:
    """Row-generate until every direction's least placement carries mass 1."""

    positions = grid.positions()
    points = np.array([[float(x), float(y)] for x, y in positions])
    sizes = np.array([len(orbit) for orbit in grid.orbits], dtype=float)
    membership = np.zeros(len(positions), dtype=int)
    cursor = 0
    for index, orbit in enumerate(grid.orbits):
        membership[cursor : cursor + len(orbit)] = index
        cursor += len(orbit)

    directions = _rotations(half_tangents)
    outer = float(grid.outer_side)
    side = float(square_side)
    rows: list[np.ndarray] = []
    # Seed at zero, not at one. Unit weights already cover every placement, so
    # the first separation finds nothing and the loop would report convergence
    # having never solved the program. From zero, every placement violates, and
    # the first round is what seeds the row set.
    weights = np.zeros(len(grid.orbits))
    log = GenerationLog()

    for round_index in range(max_rounds):
        log.rounds = round_index + 1
        site_weights = weights[membership]
        added = 0
        for direction in directions:
            for mass, covers in _worst_cells(
                points, site_weights, direction, outer, side, keep=rows_per_direction
            ):
                if mass >= 1 - tolerance:
                    break
                row = np.zeros(len(grid.orbits))
                np.add.at(row, membership[covers], 1.0)
                if row.sum() == 0:
                    log.stopped = "a placement covers no site: the grid cannot cover"
                    return weights, log
                rows.append(row)
                added += 1
        log.rows = len(rows)
        if added == 0:
            log.objective = float(sizes @ weights)
            log.stopped = "converged: every placement covers mass 1"
            return weights, log

        matrix = np.vstack(rows)
        result = linprog(
            c=sizes,
            A_ub=-matrix,
            b_ub=-np.ones(len(rows)),
            bounds=[(0.0, None)] * len(grid.orbits),
            method="highs",
        )
        if not result.success:
            log.stopped = f"linear program refused: {result.message}"
            return weights, log
        weights = result.x
        log.objective = float(result.fun)
    log.stopped = f"round limit {max_rounds} reached"
    return weights, log


def rationalise(
    grid: SiteGrid,
    weights: np.ndarray,
    *,
    scale: int,
    bump: Fraction = Fraction(1000001, 1000000),
) -> tuple[Atom, ...]:
    """Bump, round up to a multiple of ``1/scale``, and drop the empty sites.

    Rounding up is what keeps the coverage rows valid after rationalisation;
    the bump absorbs the solver's own slack. Both inflate the total, which is
    the quantity that has to stay below ``n``, so this is the step that decides
    whether a converged solve survives as a certificate.
    """
    atoms: list[Atom] = []
    for index, orbit in enumerate(grid.orbits):
        raw = Fraction(weights[index]).limit_denominator(10**9) * bump
        if raw <= 0:
            continue
        units = -((-raw * scale).__ceil__())
        units = max(units, 1) if raw > 0 else 0
        weight = Fraction(units, scale)
        for i, j in orbit:
            atoms.append(
                Atom(f"{i:03d},{j:03d}", grid.coordinates[i], grid.coordinates[j], weight)
            )
    return tuple(atoms)


def generate(
    n: int,
    outer_side: Fraction,
    square_side: Fraction,
    *,
    grid_count: int,
    inset: Fraction,
    angle_limit: Fraction,
    direction_steps: int,
    scale: int = 576,
    max_rounds: int = 60,
) -> tuple[Certificate | None, GenerationLog, float]:
    """Search for a certificate at one setting, then decide it exactly."""

    grid = build_site_grid(outer_side, grid_count, inset)
    half_tangents = _net(angle_limit, direction_steps)
    weights, log = solve_covering_lp(grid, square_side, half_tangents, max_rounds=max_rounds)
    if not log.stopped.startswith("converged"):
        return None, log, log.objective
    atoms = rationalise(grid, weights, scale=scale)
    if not atoms:
        log.stopped = "every site rounded to zero weight"
        return None, log, log.objective
    candidate = Certificate(
        n=n,
        outer_side=outer_side,
        square_side=square_side,
        atoms=atoms,
        half_tangents=half_tangents,
    )
    return candidate, log, log.objective


__all__ = [
    "Certificate",
    "GenerationLog",
    "SiteGrid",
    "build_site_grid",
    "generate",
    "rationalise",
    "solve_covering_lp",
    "verify",
]
