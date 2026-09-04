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

import math
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


def net_half_tangents(limit: Fraction, steps: int) -> tuple[Fraction, ...]:
    """The uniform half-angle net: ``steps`` equal steps up to ``limit``."""

    return tuple(limit * index / steps for index in range(steps + 1))


def direction_net(half_tangents: tuple[Fraction, ...]) -> tuple[Direction, ...]:
    """The net as exact unit rotations."""

    return tuple(
        rotation_from_half_tangent(str(index), tangent)
        for index, tangent in enumerate(half_tangents)
    )


# How far a float comparison may fall short before a cell is still counted
# reachable. The events and the domain's edges are rationals evaluated in
# floats, and a cell the exact sweep scores must never be dropped for an ulp.
# Erring the other way only admits a cell whose row is a neighbouring real
# placement's, or a redundant one, so the slack points in the safe direction.
_REACH_SLACK = 1e-12


@dataclass(frozen=True, slots=True)
class _CentreDomain:
    """The admissible centres at one direction, in the rotated frame, in floats.

    The same tilted square `sweep.centre_domain` returns, held as its edge
    lines so that a slab's v-extent and a height's u-chord are closed forms.
    The net's arc is [0, pi/4], so ``cosine >= sine >= 0`` throughout and the
    corner of least ``v`` is the image of ``(high, low)``, that of greatest
    ``v`` the image of ``(low, high)``.
    """

    cosine: float
    sine: float
    low: float
    high: float
    u_low: float
    u_high: float
    v_low: float
    v_high: float
    u_bottom: float
    u_top: float

    @classmethod
    def at(cls, direction: Direction, outer_side: float, square_side: float) -> _CentreDomain:
        cosine, sine = float(direction.ux), float(direction.uy)
        extent = square_side * (cosine + sine) / 2
        low, high = extent, outer_side - extent
        corner_x = np.array([low, high, high, low])
        corner_y = np.array([low, low, high, high])
        corner_u = corner_x * cosine + corner_y * sine
        corner_v = -corner_x * sine + corner_y * cosine
        return cls(
            cosine,
            sine,
            low,
            high,
            float(corner_u.min()),
            float(corner_u.max()),
            float(corner_v.min()),
            float(corner_v.max()),
            float(corner_u[1]),
            float(corner_u[3]),
        )

    def _floor(self, u: np.ndarray) -> np.ndarray:
        """The least ``v`` with ``(u, v)`` in the domain: the lower edges' maximum."""

        v = (self.low - u * self.sine) / self.cosine
        if self.sine > 0:
            v = np.maximum(v, (u * self.cosine - self.high) / self.sine)
        return v

    def _ceiling(self, u: np.ndarray) -> np.ndarray:
        v = (self.high - u * self.sine) / self.cosine
        if self.sine > 0:
            v = np.minimum(v, (u * self.cosine - self.low) / self.sine)
        return v

    def v_range(self, u0: np.ndarray, u1: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """The v-extent of the domain within each closed slab ``[u0, u1]``.

        The floor is convex and the ceiling concave in ``u``, so over a slab
        each is extreme at an end of the slab unless its corner lies strictly
        inside, where the extreme is the corner itself.
        """

        a = np.maximum(u0, self.u_low)
        b = np.minimum(u1, self.u_high)
        lows = np.minimum(self._floor(a), self._floor(b))
        highs = np.maximum(self._ceiling(a), self._ceiling(b))
        lows = np.where((a < self.u_bottom) & (self.u_bottom < b), self.v_low, lows)
        highs = np.where((a < self.u_top) & (self.u_top < b), self.v_high, highs)
        return lows, highs

    def u_chord(self, v: float) -> tuple[float, float]:
        """The ``u``-interval of the domain at height ``v``."""

        lo = (self.low + v * self.sine) / self.cosine
        hi = (self.high + v * self.sine) / self.cosine
        if self.sine > 0:
            lo = max(lo, (self.low - v * self.cosine) / self.sine)
            hi = min(hi, (self.high - v * self.cosine) / self.sine)
        return lo, hi


@dataclass(frozen=True, slots=True)
class EventGrid:
    """The float mirror of `sweep.Reduction` at one direction.

    ``mass[i, j]`` is what the open cell ``(u_events[i], u_events[i+1]) x
    (v_events[j], v_events[j+1])`` covers, and ``reachable[i, j]`` says whether
    that open cell meets the centre domain -- the cell set the theorem's C4
    quantifies over, and the one the exact sweep scores. ``lows`` and ``highs``
    are the domain's v-extent within each u-slab, kept because a row has to be
    generated at a point of the cell's overlap with the domain.
    """

    u: np.ndarray
    v: np.ndarray
    u_events: np.ndarray
    v_events: np.ndarray
    mass: np.ndarray
    reachable: np.ndarray
    lows: np.ndarray
    highs: np.ndarray
    domain: _CentreDomain


def event_grid(
    points: np.ndarray,
    weights: np.ndarray,
    direction: Direction,
    outer_side: float,
    square_side: float,
) -> EventGrid:
    """Project the sites, accumulate the cell masses, and mark the reachable cells.

    Mirrors `sweep.reduce_to_cells` in floating point, and on the same cell
    set: a cell is reachable when its open interior meets the centre domain,
    read per u-slab as the sweep reads it. That is the set the theorem needs
    (D-434 records the derivation), and the earlier rule -- the cell's centre
    inside the domain -- missed about one cell in ninety away from the axes,
    which is why programs converged and were then refused at C4.

    The event grid is built from the sites that carry weight, not from all of
    them: mass is constant between those, so the cells are coarser but the
    minimum is the same and the grid stays quadratic in the support rather
    than in the site count.
    """

    cosine, sine = float(direction.ux), float(direction.uy)
    half = square_side / 2
    u = points[:, 0] * cosine + points[:, 1] * sine
    v = -points[:, 0] * sine + points[:, 1] * cosine
    domain = _CentreDomain.at(direction, outer_side, square_side)

    live = weights > 0
    if not live.any():
        # With nothing weighted, the only events are the domain's own extremes,
        # and the single cell they leave is wider than any square: no site
        # contains it, so the first round would report that the sites cannot
        # cover. Stride through them instead. The mass is zero either way; this
        # only makes the first round's rows fine enough to be worth keeping.
        live = np.zeros(points.shape[0], dtype=bool)
        live[:: max(1, points.shape[0] // 600)] = True
    live_u, live_v, live_w = u[live], v[live], weights[live]
    u_events = np.unique(
        np.concatenate([live_u - half, live_u + half, [domain.u_low, domain.u_high]])
    )
    v_events = np.unique(
        np.concatenate([live_v - half, live_v + half, [domain.v_low, domain.v_high]])
    )
    grid = np.zeros((u_events.size, v_events.size))
    left = np.searchsorted(u_events, live_u - half)
    right = np.searchsorted(u_events, live_u + half)
    bottom = np.searchsorted(v_events, live_v - half)
    top = np.searchsorted(v_events, live_v + half)
    np.add.at(grid, (left, bottom), live_w)
    np.add.at(grid, (right, bottom), -live_w)
    np.add.at(grid, (left, top), -live_w)
    np.add.at(grid, (right, top), live_w)
    mass = np.cumsum(np.cumsum(grid, axis=1), axis=0)[:-1, :-1]

    # The domain's extremes are events themselves, so against those the tests
    # are exact; only the per-slab v-extent, which is computed, needs the slack.
    # Without the exact pair every slab at direction zero would admit the cell
    # just above the domain and the one just below it, tied to the ulp.
    u0, u1 = u_events[:-1], u_events[1:]
    slabs = (u1 > domain.u_low) & (u0 < domain.u_high)
    bands = (v_events[:-1] < domain.v_high) & (v_events[1:] > domain.v_low)
    lows, highs = domain.v_range(u0, u1)
    reachable = (
        slabs[:, None]
        & bands[None, :]
        & (v_events[None, :-1] < highs[:, None] + _REACH_SLACK)
        & (v_events[None, 1:] > lows[:, None] - _REACH_SLACK)
    )
    return EventGrid(u, v, u_events, v_events, mass, reachable, lows, highs, domain)


def placement_cells(
    points: np.ndarray,
    weights: np.ndarray,
    direction: Direction,
    outer_side: float,
    square_side: float,
    *,
    keep: int,
) -> list[tuple[float, float, float, np.ndarray]]:
    """Least-mass placements at one direction: ``(mass, u, v, covering mask)``.

    A row is generated at a point of the cell's overlap with the domain rather
    than at the cell's centre. With the grid built on the weighted sites only,
    a cell can meet the domain while its centre hangs outside the container,
    and a row read there constrains a placement that does not exist; the first
    attempt at the reachability rule did that and reported optima of 13.5 and
    15.4 on a program whose accepted certificate carries 11.9375.
    """

    half = square_side / 2
    cells = event_grid(points, weights, direction, outer_side, square_side)
    u, v = cells.u, cells.v
    u_events, v_events = cells.u_events, cells.v_events
    lows, highs, domain = cells.lows, cells.highs, cells.domain
    u0, u1 = u_events[:-1], u_events[1:]

    scored = np.where(cells.reachable, cells.mass, np.inf)
    flat = scored.ravel()
    if flat.size == 0:
        return []
    # Survey more cells than are kept. A cell let in by the slack, or thinner
    # than a float can place a point in, re-scores at a neighbouring
    # placement's mass; it is still a real row, but it must not crowd out the
    # cells whose own mass is the violation.
    take = min(4 * keep, flat.size - 1) if flat.size > 1 else 0
    order = np.argpartition(flat, take)[: take + 1]
    order = order[np.isfinite(flat[order])]

    found: list[tuple[float, float, float, np.ndarray]] = []
    exact = 0
    for index in order[np.argsort(flat[order])]:
        i, j = divmod(int(index), v_events.size - 1)
        # A point of the cell's overlap with the domain: the middle of the
        # v-overlap, then the middle of the domain's chord at that height
        # within the slab. Where the whole cell lies inside this is the cell's
        # centre. No live event lies strictly inside the cell, so the mask read
        # here carries the cell's own mass -- the number the difference array
        # holds and, more to the point, the number the exact verifier reads for
        # the same cell.
        va, vb = max(v_events[j], lows[i]), min(v_events[j + 1], highs[i])
        cv = float((va + vb) / 2)
        chord_lo, chord_hi = domain.u_chord(cv)
        ua, ub = max(u0[i], chord_lo), min(u1[i], chord_hi)
        cu = float((ua + ub) / 2)
        covers = (np.abs(u - cu) <= half) & (np.abs(v - cv) <= half)
        cell_mass = float(weights[covers].sum())
        found.append((cell_mass, cu, cv, covers))
        exact += abs(cell_mass - float(flat[index])) <= 1e-9
        if exact >= keep:
            break
    found.sort(key=lambda entry: entry[0])
    return found[:keep]


# How far below 1 a held row may sit in the solver's optimum and still count as
# satisfied: HiGHS's primal feasibility tolerance. The rationaliser's bump of one
# part in a million is what absorbs it, so the two numbers belong together.
LP_FEASIBILITY = 1e-7


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

    directions = direction_net(half_tangents)
    outer = float(grid.outer_side)
    side = float(square_side)
    rows: list[np.ndarray] = []
    # Seed at zero, not at one. Unit weights already cover every placement, so
    # the first separation finds nothing and the loop would report convergence
    # having never solved the program. From zero, every placement violates, and
    # the first round is what seeds the row set.
    weights = np.zeros(len(grid.orbits))
    log = GenerationLog()

    held: set[bytes] = set()
    for round_index in range(max_rounds):
        log.rounds = round_index + 1
        site_weights = weights[membership]
        violated = 0
        added = 0
        least = float("inf")
        for direction in directions:
            for mass, _, _, covers in placement_cells(
                points, site_weights, direction, outer, side, keep=rows_per_direction
            ):
                if mass >= 1 - tolerance:
                    break
                row = np.zeros(len(grid.orbits))
                np.add.at(row, membership[covers], 1.0)
                if row.sum() == 0:
                    log.stopped = "a placement covers no site: the grid cannot cover"
                    return weights, log
                violated += 1
                least = min(least, mass)
                key = row.tobytes()
                if key not in held:
                    held.add(key)
                    rows.append(row)
                    added += 1
        log.rows = len(rows)
        if violated == 0 or (added == 0 and least >= 1 - LP_FEASIBILITY):
            # Nothing violated, or every violation is a row the program already
            # holds and misses by no more than the solver's own feasibility
            # tolerance -- which the rationaliser's bump absorbs. Re-solving
            # the same rows would return the same point.
            log.objective = float(sizes @ weights)
            log.stopped = "converged: every placement covers mass 1"
            return weights, log
        if added == 0:
            log.stopped = (
                f"a held row is violated by {1 - least:.3e}: the solver's point is off"
            )
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
        # Round UP. ``-ceil(-x)`` is ``floor(x)``, and floor is exactly wrong
        # here: every row is a ``>= 1`` constraint that the solver leaves tight,
        # so shaving any weight drops a tight cell below 1 and the exact verifier
        # refuses a certificate the program had found. The first version of this
        # line did that (D-433), and the ``max(units, 1)`` guard below hid it.
        units = math.ceil(raw * scale)
        weight = Fraction(max(units, 1), scale)
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
    half_tangents = net_half_tangents(angle_limit, direction_steps)
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
    "LP_FEASIBILITY",
    "Certificate",
    "EventGrid",
    "GenerationLog",
    "SiteGrid",
    "build_site_grid",
    "direction_net",
    "event_grid",
    "generate",
    "net_half_tangents",
    "placement_cells",
    "rationalise",
    "solve_covering_lp",
    "verify",
]
