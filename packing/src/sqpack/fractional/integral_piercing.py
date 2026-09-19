"""Integral piercing of closed squares by a finite candidate site set.

M3 (think-k4vb / BC-359) asks whether eleven of the T-018 atom sites pierce every
closed unit square in ``[0, 19/5]^2``. An 11-point set is not a sum of D4 orbit
sizes ``{1, 4, 8}``, so no D4 producer can search for one. The measurement is a
set-cover integer program over event cells of a finite direction net.

The placed square is the closed unit square (``B = 1``), not T-018's retained
shrink ``9977/10000``. Memo II ownership is unit squares in the container; the
shrink is a fractional-certificate device that lets Condition 4 absorb the net's
angular gap. Using it here would answer a different covering problem.

A coarse-net IP optimum is a kill-test measurement, not a verified ``s(11)``
movement. Timeout is unresolved, never a kill. A float LP relaxation is not a
verdict; the only solver path is a HiGHS MIP with integrality on site indicators.
"""

from __future__ import annotations

import json
import time
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum
from fractions import Fraction
from pathlib import Path
from typing import Any, Never

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csr_array

from sqpack.fractional.generate import net_half_tangents
from sqpack.fractional.model import Atom, Direction, rotation_from_half_tangent
from sqpack.fractional.sweep import SpanReduction, reduce_to_spans
from sqpack.fractional.threshold_coverage_encoding import (
    pareto_minimal_rows,
    unique_rows,
)
from sqpack.project import require_project_root

type Point = tuple[Fraction, Fraction]

T018_CERTIFICATE = Path("cases/n11_fractional_certificate/certificate.json")
DEFAULT_SIDE = Fraction(19, 5)
DEFAULT_SQUARE_SIDE = Fraction(1)
T018_SHRINK = Fraction(9977, 10000)
DEFAULT_ANGLE_LIMIT = Fraction(207107, 500000)
DEFAULT_DIRECTION_STEPS = 36
CANDIDATE_CARDINALITY = 11
KILL_PIERCING = 12
_EVENT_WEIGHT = Fraction(0)
_PARETO_ROW_LIMIT = 4096
_CHUNK_CELLS = 4096
MAX_UNIQUE_ROWS = 80_000
SQUARE_SIDE_REASON = (
    "Memo II ownership is closed unit squares in the container. T-018's shrink "
    f"{T018_SHRINK} is a fractional-certificate device (Condition 4), not the "
    "ownership object."
)


class SearchStatus(StrEnum):
    feasible = "feasible"
    infeasible = "infeasible"
    timeout = "timeout"
    encoding_ready = "encoding_ready"


class M3Verdict(StrEnum):
    unresolved = "unresolved"
    killed_coarse_net = "killed_coarse_net"
    eleven_candidate = "eleven_candidate"


class CoverEncodingTimeoutError(Exception):
    """Event-cell enumeration hit the search deadline before the MIP ran."""


class PiercingError(ValueError):
    """The site list, square family, or covering matrix is not a piercing instance."""


@dataclass(frozen=True, slots=True)
class ClosedSquare:
    """A closed axis-aligned or rotated square, given by centre, frame, and side."""

    center_x: Fraction
    center_y: Fraction
    direction: Direction
    side: Fraction = DEFAULT_SQUARE_SIDE


@dataclass(frozen=True, slots=True)
class CoverEncoding:
    """Unique 0/1 covering rows of reachable event cells (one column per site)."""

    rows: np.ndarray
    reachable_cells: int
    direction_count: int
    site_count: int
    truncated: bool


@dataclass(frozen=True, slots=True)
class SetCoverOutcome:
    """HiGHS integral set-cover result. Not an exact infeasibility certificate."""

    search_status: SearchStatus
    piercing: int | None
    selected: tuple[int, ...] | None
    message: str
    optimizer_ran: bool


def _inexact(text: str) -> Never:
    raise PiercingError(f"inexact JSON number {text!r}; use an exact rational string")


def t018_certificate_path(root: Path | None = None) -> Path:
    """The frozen T-018 atom file. This module never writes it."""

    packing = require_project_root(root)
    return packing / T018_CERTIFICATE


def load_unique_sites(path: Path | None = None) -> tuple[Point, ...]:
    """Unique ``(x, y)`` from T-018 atoms ``[x, y, w]``, first-seen order."""

    source = t018_certificate_path() if path is None else path
    try:
        record = json.loads(
            source.read_text(encoding="utf-8"),
            parse_float=_inexact,
            parse_constant=_inexact,
        )
    except (OSError, UnicodeError, ValueError) as error:
        raise PiercingError(f"cannot read sites from {source}: {error}") from error
    if not isinstance(record, dict):
        raise PiercingError("certificate JSON must be an object")
    atoms = record.get("atoms")
    if not isinstance(atoms, list) or not atoms:
        raise PiercingError("certificate atoms must be a non-empty list")
    sites: list[Point] = []
    seen: set[Point] = set()
    for index, entry in enumerate(atoms):
        if not isinstance(entry, list) or len(entry) < 2:
            raise PiercingError(f"atom {index} must be [x, y, w]")
        try:
            point = (Fraction(str(entry[0])), Fraction(str(entry[1])))
        except (TypeError, ValueError) as error:
            raise PiercingError(f"atom {index} has a non-rational coordinate") from error
        if point not in seen:
            seen.add(point)
            sites.append(point)
    return tuple(sites)


def sites_inside_container(sites: Sequence[Point], outer_side: Fraction) -> tuple[Point, ...]:
    """Drop candidate sites that cannot meet a square contained in ``[0, L]^2``."""

    if outer_side <= 0:
        raise PiercingError("outer_side must be positive")
    return tuple((x, y) for x, y in sites if 0 <= x <= outer_side and 0 <= y <= outer_side)


def axis_aligned() -> Direction:
    return rotation_from_half_tangent("0", Fraction(0))


def site_covers_closed_square(site: Point, square: ClosedSquare) -> bool:
    """True when the closed square contains the site."""

    half = square.side / 2
    ux, uy = square.direction.ux, square.direction.uy
    vx, vy = square.direction.vx, square.direction.vy
    site_u = ux * site[0] + uy * site[1]
    site_v = vx * site[0] + vy * site[1]
    center_u = ux * square.center_x + uy * square.center_y
    center_v = vx * square.center_x + vy * square.center_y
    return abs(site_u - center_u) <= half and abs(site_v - center_v) <= half


def cover_matrix_for_squares(
    sites: Sequence[Point], squares: Sequence[ClosedSquare]
) -> np.ndarray:
    """One row per square, one column per site: 1 iff the closed square contains the site."""

    if not sites:
        raise PiercingError("a piercing instance needs at least one site")
    if not squares:
        raise PiercingError("a piercing instance needs at least one square")
    rows = np.zeros((len(squares), len(sites)), dtype=np.uint8)
    for row, square in enumerate(squares):
        if square.side <= 0:
            raise PiercingError("square side must be positive")
        for column, site in enumerate(sites):
            if site_covers_closed_square(site, square):
                rows[row, column] = 1
    return rows


def _event_atoms(sites: Sequence[Point]) -> tuple[Atom, ...]:
    return tuple(Atom(str(index), x, y, _EVENT_WEIGHT) for index, (x, y) in enumerate(sites))


def _reachable_cells(spans: tuple[tuple[int, int, int], ...]) -> tuple[np.ndarray, np.ndarray]:
    count = sum(j1 - j0 + 1 for _, j0, j1 in spans)
    cell_i = np.empty(count, dtype=np.int32)
    cell_j = np.empty(count, dtype=np.int32)
    offset = 0
    for i, j0, j1 in spans:
        width = j1 - j0 + 1
        cell_i[offset : offset + width] = i
        cell_j[offset : offset + width] = np.arange(j0, j1 + 1, dtype=np.int32)
        offset += width
    return cell_i, cell_j


def _index_rectangles(
    reduction: SpanReduction,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    u_index = {value: index for index, value in enumerate(reduction.u_events)}
    v_index = {value: index for index, value in enumerate(reduction.v_events)}
    count = len(reduction.rectangles)
    left = np.empty(count, dtype=np.intp)
    right = np.empty(count, dtype=np.intp)
    bottom = np.empty(count, dtype=np.intp)
    top = np.empty(count, dtype=np.intp)
    for index, (u1, u2, v1, v2, _weight) in enumerate(reduction.rectangles):
        left[index] = u_index[u1]
        right[index] = u_index[u2]
        bottom[index] = v_index[v1]
        top[index] = v_index[v2]
    return left, right, bottom, top


def _chunk_cover_rows(
    cells: tuple[np.ndarray, np.ndarray],
    rectangles: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    *,
    deadline_monotonic: float | None = None,
) -> np.ndarray:
    cell_i, cell_j = cells
    left, right, bottom, top = rectangles
    n_cells = int(cell_i.size)
    n_sites = int(left.size)
    if n_cells == 0:
        return np.zeros((0, n_sites), dtype=np.uint8)
    accumulated = np.zeros((0, n_sites), dtype=np.uint8)
    pending: list[np.ndarray] = []
    pending_rows = 0
    for start in range(0, n_cells, _CHUNK_CELLS):
        if _deadline_hit(deadline_monotonic):
            raise CoverEncodingTimeoutError("event-cell encoding hit the search deadline")
        sl = slice(start, start + _CHUNK_CELLS)
        i = cell_i[sl][:, np.newaxis]
        j = cell_j[sl][:, np.newaxis]
        cover = (
            (left[np.newaxis, :] <= i)
            & (i < right[np.newaxis, :])
            & (bottom[np.newaxis, :] <= j)
            & (j < top[np.newaxis, :])
        )
        chunk = unique_rows(cover.astype(np.uint8, copy=False))
        if chunk.shape[0] == 0:
            continue
        if not bool(np.all(chunk.any(axis=1))):
            return np.zeros((1, n_sites), dtype=np.uint8)
        pending.append(chunk)
        pending_rows += int(chunk.shape[0])
        if pending_rows >= _CHUNK_CELLS:
            stacked = (
                np.vstack((*pending,))
                if accumulated.shape[0] == 0
                else np.vstack((accumulated, *pending))
            )
            accumulated = _maybe_truncate(unique_rows(stacked))
            pending = []
            pending_rows = 0
    if pending:
        stacked = (
            np.vstack((*pending,))
            if accumulated.shape[0] == 0
            else np.vstack((accumulated, *pending))
        )
        accumulated = _maybe_truncate(unique_rows(stacked))
    return accumulated


def _remember_covering(
    seen: dict[frozenset[int], None],
    covering: set[int],
    *,
    cap: int,
    worst_weight: list[int],
    hit_cap: list[bool],
) -> bool:
    """Store a competitive nonzero covering set. True when the segment is uncovered.

    Once ``cap`` unique rows are held, only a strictly lighter set replaces a
    heaviest one. That is a lower-bound row set: enough to kill, not to nominate.
    """

    weight = len(covering)
    if weight == 0:
        return True
    if cap > 0 and len(seen) >= cap and weight >= worst_weight[0]:
        hit_cap[0] = True
        return False
    key = frozenset(covering)
    if key in seen:
        return False
    if cap > 0 and len(seen) >= cap:
        hit_cap[0] = True
        drop = next(old for old in seen if len(old) == worst_weight[0])
        del seen[drop]
        seen[key] = None
        worst_weight[0] = max(len(old) for old in seen)
        return False
    seen[key] = None
    worst_weight[0] = max(worst_weight[0], weight)
    return False


def _rows_from_covers(seen: dict[frozenset[int], None], n_sites: int) -> np.ndarray:
    rows = np.zeros((len(seen), n_sites), dtype=np.uint8)
    for index, key in enumerate(seen):
        if key:
            rows[index, np.fromiter(key, dtype=np.intp, count=len(key))] = 1
    return rows


def _sweep_span(
    *,
    j0: int,
    j1: int,
    site_ids: np.ndarray,
    start_j: np.ndarray,
    end_j: np.ndarray,
    seen: dict[frozenset[int], None],
    row_cap: int,
    worst_weight: list[int],
    hit_cap: list[bool],
) -> bool:
    """Sweep one reachable column. True when a reachable cell is uncovered."""

    event_j = np.concatenate((start_j, end_j))
    n_live = int(site_ids.size)
    event_kind = np.concatenate(
        (np.zeros(n_live, dtype=np.int8), np.ones(n_live, dtype=np.int8))
    )
    event_site = np.concatenate((site_ids, site_ids))
    order = np.lexsort((event_kind, event_j))
    covering: set[int] = set()
    cursor = int(j0)
    for index in order:
        event_at = int(event_j[index])
        if event_at > cursor:
            last_cell = min(event_at - 1, int(j1))
            if cursor <= last_cell and _remember_covering(
                seen,
                covering,
                cap=row_cap,
                worst_weight=worst_weight,
                hit_cap=hit_cap,
            ):
                return True
            cursor = event_at
            if cursor > j1:
                break
        site = int(event_site[index])
        if event_kind[index] == 0:
            covering.add(site)
        else:
            covering.discard(site)
    return cursor <= j1 and _remember_covering(
        seen,
        covering,
        cap=row_cap,
        worst_weight=worst_weight,
        hit_cap=hit_cap,
    )


def _span_cover_rows(
    spans: tuple[tuple[int, int, int], ...],
    rectangles: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    *,
    deadline_monotonic: float | None = None,
    row_cap: int = MAX_UNIQUE_ROWS,
    span_cap: int | None = None,
) -> tuple[np.ndarray, bool]:
    """Unique covering rows of reachable spans, without expanding every event cell.

    Coverage is constant between a site rectangle's v-events, so a per-column sweep
    emits one row per segment instead of one row per cell. An uncovered reachable
    cell still returns a single zero row, matching ``_chunk_cover_rows``.
    ``span_cap`` keeps the hardest columns and marks the row set truncated.
    """

    left, right, bottom, top = rectangles
    n_sites = int(left.size)
    empty = np.zeros((0, n_sites), dtype=np.uint8)
    if not spans:
        return empty, False
    ranked: list[tuple[int, int, int, int]] = []
    for i, j0, j1 in spans:
        if _deadline_hit(deadline_monotonic):
            raise CoverEncodingTimeoutError("event-cell encoding hit the search deadline")
        if j1 < j0:
            continue
        active_count = int(np.count_nonzero((left <= i) & (i < right)))
        if active_count == 0:
            return np.zeros((1, n_sites), dtype=np.uint8), False
        ranked.append((active_count, i, j0, j1))
    ranked.sort(key=lambda item: item[0])
    hit_span_cap = False
    if span_cap is not None and len(ranked) > span_cap:
        ranked = ranked[:span_cap]
        hit_span_cap = True
    seen: dict[frozenset[int], None] = {}
    worst_weight = [0]
    hit_cap = [False]
    for _count, i, j0, j1 in ranked:
        if _deadline_hit(deadline_monotonic):
            raise CoverEncodingTimeoutError("event-cell encoding hit the search deadline")
        active = np.flatnonzero((left <= i) & (i < right))
        starts = np.maximum(bottom[active], j0)
        ends = np.minimum(top[active], j1 + 1)
        live = starts < ends
        if not bool(np.any(live)):
            return np.zeros((1, n_sites), dtype=np.uint8), False
        if _sweep_span(
            j0=j0,
            j1=j1,
            site_ids=active[live],
            start_j=starts[live].astype(np.int64, copy=False),
            end_j=ends[live].astype(np.int64, copy=False),
            seen=seen,
            row_cap=row_cap,
            worst_weight=worst_weight,
            hit_cap=hit_cap,
        ):
            return np.zeros((1, n_sites), dtype=np.uint8), False
    if not seen:
        return empty, hit_span_cap or hit_cap[0]
    return unique_rows(_rows_from_covers(seen, n_sites)), hit_span_cap or hit_cap[0]


def span_and_broadcast_cover_rows(
    sites: Sequence[Point],
    *,
    outer_side: Fraction,
    square_side: Fraction,
    direction: Direction,
) -> tuple[np.ndarray, np.ndarray]:
    """Span-sweep and expanded-cell covering rows of one direction.

    Both arrays are unique 0/1 rows, or a single zero row when a reachable cell
    is uncovered. The expanded-cell path is the original encoder; they must agree.
    """

    if not sites:
        raise PiercingError("a piercing instance needs at least one site")
    if outer_side <= 0 or square_side <= 0:
        raise PiercingError("sides must be positive")
    atoms = _event_atoms(sites)
    reduction = reduce_to_spans(atoms, direction, outer_side, square_side)
    rectangles = _index_rectangles(reduction)
    span_rows, _hit_cap = _span_cover_rows(reduction.spans, rectangles)
    cells = _reachable_cells(reduction.spans)
    chunk_rows = _chunk_cover_rows(cells, rectangles)
    return span_rows, chunk_rows


def _maybe_truncate(rows: np.ndarray) -> np.ndarray:
    if rows.shape[0] <= MAX_UNIQUE_ROWS:
        return rows
    order = np.argsort(rows.sum(axis=1), kind="stable")[:MAX_UNIQUE_ROWS]
    return np.ascontiguousarray(rows[order])


def _maybe_pareto(rows: np.ndarray) -> np.ndarray:
    if rows.shape[0] == 0 or rows.shape[0] > _PARETO_ROW_LIMIT:
        return rows
    if not bool(np.all(rows.any(axis=1))):
        return np.zeros((1, rows.shape[1]), dtype=rows.dtype)
    return pareto_minimal_rows(rows)


def _deadline_hit(deadline: float | None) -> bool:
    return deadline is not None and time.monotonic() >= deadline


def geometry_fields(square_side: Fraction) -> dict[str, object]:
    """Record which B was used and why the default is the unit square."""

    return {
        "square_side": str(square_side),
        "t018_shrink": str(T018_SHRINK),
        "using_unit_squares": square_side == DEFAULT_SQUARE_SIDE,
        "square_side_reason": SQUARE_SIDE_REASON,
    }


def encode_event_cell_covers(
    sites: Sequence[Point],
    *,
    outer_side: Fraction,
    square_side: Fraction = DEFAULT_SQUARE_SIDE,
    angle_limit: Fraction = DEFAULT_ANGLE_LIMIT,
    direction_steps: int = DEFAULT_DIRECTION_STEPS,
    deadline_monotonic: float | None = None,
) -> CoverEncoding:
    """Unique covering rows of reachable closed-``B`` event cells on the net.

    Coverage is constant on open event cells. For closed squares the binding
    constraints are those open cells: a boundary placement only adds sites.
    """

    if not sites:
        raise PiercingError("a piercing instance needs at least one site")
    if outer_side <= 0 or square_side <= 0:
        raise PiercingError("sides must be positive")
    if direction_steps < 1:
        raise PiercingError("the direction net needs at least one step")
    if angle_limit <= 0:
        raise PiercingError("angle_limit must be positive")
    half_tangents = net_half_tangents(angle_limit, direction_steps)
    atoms = _event_atoms(sites)
    n_sites = len(sites)
    accumulated = np.zeros((0, n_sites), dtype=np.uint8)
    reachable = 0
    truncated = False
    for index, tangent in enumerate(half_tangents):
        if _deadline_hit(deadline_monotonic):
            raise CoverEncodingTimeoutError("event-cell encoding hit the search deadline")
        direction = rotation_from_half_tangent(str(index), tangent)
        reduction = reduce_to_spans(atoms, direction, outer_side, square_side)
        reachable += sum(j1 - j0 + 1 for _column, j0, j1 in reduction.spans)
        rectangles = _index_rectangles(reduction)
        rows, hit_cap = _span_cover_rows(
            reduction.spans,
            rectangles,
            deadline_monotonic=deadline_monotonic,
            row_cap=_PARETO_ROW_LIMIT,
        )
        truncated = truncated or hit_cap
        if rows.shape[0] == 0:
            continue
        if not bool(np.all(rows.any(axis=1))):
            return CoverEncoding(
                np.zeros((1, n_sites), dtype=np.uint8),
                reachable,
                len(half_tangents),
                n_sites,
                truncated=False,
            )
        stacked = rows if accumulated.shape[0] == 0 else np.vstack((accumulated, rows))
        accumulated = unique_rows(stacked)
        if accumulated.shape[0] > MAX_UNIQUE_ROWS:
            accumulated = _maybe_truncate(accumulated)
            truncated = True
    if accumulated.shape[0] == 0:
        raise PiercingError("the centre domain produced no event cell")
    if accumulated.shape[0] <= _PARETO_ROW_LIMIT and n_sites <= 64:
        reduced = _maybe_pareto(accumulated)
        if reduced.shape[0] < accumulated.shape[0]:
            accumulated = reduced
    return CoverEncoding(
        accumulated, reachable, len(half_tangents), n_sites, truncated=truncated
    )


def _solver_bound(values: np.ndarray) -> Any:
    """scipy's stubs type constraint bounds as scalars; HiGHS takes arrays."""

    return values


def _selected_covers(rows: np.ndarray, selected: np.ndarray) -> bool:
    if selected.size == 0:
        return rows.shape[0] == 0
    covered = rows[:, selected].sum(axis=1)
    return bool(np.all(covered >= 1))


def solve_integral_set_cover(
    rows: np.ndarray,
    *,
    time_limit_s: float | None = None,
    cardinality_limit: int | None = None,
) -> SetCoverOutcome:
    """Minimise the number of sites that hit every covering row, with 0/1 indicators.

    HiGHS is a float MIP. A feasible incumbent is re-checked in integers before it
    is reported. A timeout or a non-infeasible solver failure is unresolved. Only
    HiGHS status 2 is treated as infeasible. The LP relaxation is never solved.
    """

    if rows.ndim != 2:
        raise PiercingError("covering rows must be a 2-D 0/1 matrix")
    n_rows, n_sites = int(rows.shape[0]), int(rows.shape[1])
    if n_sites < 1 or n_rows < 1:
        raise PiercingError("covering rows must have at least one cell and one site")
    if not bool(np.all(rows.any(axis=1))):
        return SetCoverOutcome(
            SearchStatus.infeasible,
            None,
            None,
            "a cell is covered by no candidate site",
            optimizer_ran=False,
        )
    matrix = csr_array(rows.astype(np.float64, copy=False))
    constraints = [
        LinearConstraint(matrix, lb=1.0, ub=np.inf),
    ]
    if cardinality_limit is not None:
        if cardinality_limit < 0:
            raise PiercingError("cardinality_limit must be nonnegative")
        constraints.append(
            LinearConstraint(
                np.ones((1, n_sites), dtype=np.float64),
                lb=0.0,
                ub=float(cardinality_limit),
            )
        )
    bounds = Bounds(lb=_solver_bound(np.zeros(n_sites)), ub=_solver_bound(np.ones(n_sites)))
    integrality = np.ones(n_sites, dtype=np.int8)
    cost = np.ones(n_sites, dtype=np.float64)
    options: dict[str, Any] = {}
    if time_limit_s is not None:
        options["time_limit"] = time_limit_s
    try:
        result = milp(
            cost,
            constraints=constraints,
            bounds=bounds,
            integrality=integrality,
            options=options or None,
        )
    except (ValueError, TypeError, RuntimeError) as error:
        return SetCoverOutcome(
            SearchStatus.encoding_ready,
            None,
            None,
            f"HiGHS refused: {error}",
            optimizer_ran=True,
        )
    status = int(result.status)
    search_status = SearchStatus.encoding_ready
    piercing: int | None = None
    selected: tuple[int, ...] | None = None
    message = result.message or "HiGHS returned no incumbent"
    if status == 1:
        search_status = SearchStatus.timeout
        message = "HiGHS reached its time limit; timeout is unresolved, never a kill"
    elif status == 2:
        search_status = SearchStatus.infeasible
        message = "integer HiGHS reported infeasible on the coarse net (kill-test measurement)"
    elif result.success and result.x is not None:
        chosen = np.flatnonzero(np.rint(np.asarray(result.x, dtype=np.float64)) >= 0.5)
        if _selected_covers(rows, chosen):
            selected = tuple(int(index) for index in chosen.tolist())
            piercing = len(selected)
            search_status = SearchStatus.feasible
            message = (
                "integral set-cover incumbent; coarse-net measurement, not a retained bound"
            )
        else:
            message = "HiGHS incumbent failed the integer cover check; not a verdict"
    else:
        message = (
            f"HiGHS returned status {status} with no usable incumbent; "
            "solver error is unresolved, never a kill"
        )
    return SetCoverOutcome(search_status, piercing, selected, message, optimizer_ran=True)


def m3_verdict_for(
    status: SearchStatus,
    piercing: int | None,
    *,
    truncated: bool = False,
) -> M3Verdict:
    """Map a coarse-net solve onto the M3 kill-test vocabulary.

    ``killed_coarse_net`` only when the net forbids an 11-set (optimum ≥ 12, or
    infeasible at cardinality 11). ``eleven_candidate`` only when a feasible
    11-or-fewer set covers every enumerated cell. Truncated row sets can kill
    (a lower bound) but cannot nominate a candidate.
    """

    if status in {SearchStatus.timeout, SearchStatus.encoding_ready}:
        return M3Verdict.unresolved
    if status is SearchStatus.infeasible:
        return M3Verdict.killed_coarse_net
    if status is SearchStatus.feasible and piercing is not None:
        if piercing >= KILL_PIERCING:
            return M3Verdict.killed_coarse_net
        if piercing <= CANDIDATE_CARDINALITY and not truncated:
            return M3Verdict.eleven_candidate
    return M3Verdict.unresolved
