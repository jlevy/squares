#!/usr/bin/env python3
"""Re-price Overbeck's external ``n = 17`` measure on its own final catalogue.

The retained artifact under ``packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/``
carries a measure whose slack distribution is strongly bimodal: 5,222 of its 7,853
catalogue rows clear ``1.00207``, 2,140 of them share one identical minimum, and the
global minimum ``1.000020517`` is attained by a single row. A measure whose row minima
pile up on one plateau is a measure that was priced against an *earlier* catalogue and
never re-priced against the one row generation finished on. That is headroom at fixed
``(L, A)`` on the existing support, and this tool measures how much of it there is.

The measurement is a covering linear program on the artifact's own support:

* **Variables.** The 1,134 point-orbit weights and the 253 two-of-three orbit weights,
  1,387 in all, non-negative. Every orbit is a variable, the 282 that the artifact prices
  at zero included, because re-pricing is free to turn one on.
* **Constraints.** One per catalogue row, at the *cell where that row's charge is least*.
  The artifact's own sweep reports each row's minimum; this tool reports where it is
  attained. Each extracted cell contributes ``sum_o a_o w_o + sum_s b_s w_s >= 1``, with
  ``a_o`` the number of that orbit's sites the row's core captures at that centre and
  ``b_s`` the number of that orbit's triples with at least two of three captured.
* **Objective.** The measure's own budget, ``sum_o |orbit_o| w_o + sum_s |triples_s| w_s``,
  which is exactly how the artifact totals ``budget_units``.

**The value this returns is a lower bound on a re-priced measure's mass, not a
certificate.** The constraint set is one cell per row, and a real certificate has to hold
over the whole continuum of every row -- every cell, not the least one. Dropping the
other cells enlarges the feasible set, so the optimum can only fall: the number below is
a *relaxation* of the re-pricing problem. An LP value under 17 therefore does not say a
certificate exists at this ``(L, A)``; it says nothing at all is ruled out yet, and the
next rung is a separation loop that puts the violated cells back. An LP value at or above
the artifact's own normalised mass says the opposite and says it conclusively, because a
relaxation that cannot go below a number proves the unrelaxed problem cannot either.

The translation from the artifact's bytes is not re-done here.
`devtools.translate_kleddamag_certificate` owns it, with the nine controls that prove it
preserves the object, and this module imports `read_source` and `expand` from it rather
than reading the source a second way.
What is new here is the *argmin*: the artifact's checker reports each row's least charge
and throws away the cell, so the cell is recovered by a second sweep with the same
rectangles, the same event grid and the same restricted legal-centre polygon.

The controls, all exact:

``K1`` this sweep's per-row minimum against the artifact's own retained replay
(`evidence/average4-adaptive-r1.python-replay.json`), row by row over every row swept.
``K2`` this sweep's per-row slab and cell counts against the same replay, row by row.
Agreeing on the cell counts is the sharp half: a differently partitioned sweep would not.
``K1`` and ``K2`` are decided together and the tool refuses to emit if either fails.
``K3`` this sweep's ``(units, slabs, cells)`` against
`translate_kleddamag_certificate.restricted_row_minimum`, the translator's own
implementation, on a sample of rows -- a third implementation of the same number.
``K4`` the artifact's own weights evaluated through the emitted constraint matrix. The
objective must return ``budget_units``; *each* constraint must return that row's own
swept minimum, which is what says the capture set read off the minimising cell is the
charge the sweep found; and on a complete catalogue the least of them must return
``minimum_units``. The artifact is then an exactly feasible point of the relaxation, and
``budget_units / minimum_units`` is the number the program's value is read against.
``K5`` every minimising cell clipped against its own row's parent-centre envelope, and
the reported centre taken as the centroid of the intersection. The sweep's window is the
artifact's own and takes a boundary cell whole, so a cell's midpoint can lie outside the
envelope; the charge is constant on the open cell, so the clip moves the reported centre
without moving the constraint. A row whose cell meets the envelope only in measure zero
is counted and named, because there the constraint is the artifact's window rather than
its envelope.
``K6`` the LP solution rationalised on the artifact's own weight denominator and
re-verified exactly: the reported mass is ``objective / least charge`` in integers, so it
is the exact mass of an exactly feasible rational measure and never a solver's float.
``K7`` the solver's dual rationalised the same way and scaled down until ``A^T y <= c``
holds in integers, which by weak duality is an exact floor under the relaxation's
optimum -- and therefore under the unrelaxed problem's optimum as well. The two together
bracket the answer in rationals with no float between them.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python \
        -m devtools.reprice_kleddamag_measure --stride 400 --workers 2 \
        --cells cells.jsonl --matrix matrix.npz --report report.json
    uv run --frozen --all-extras --group dev python \
        -m devtools.reprice_kleddamag_measure --from-matrix matrix.npz --report report.json
"""

from __future__ import annotations

import argparse
import json
import time
from bisect import bisect_left, bisect_right
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace
from fractions import Fraction
from math import atan, degrees, lcm
from multiprocessing import get_context
from pathlib import Path
from typing import Any, cast

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_array

from devtools.translate_kleddamag_certificate import (
    REPLAY,
    SOURCE,
    Expansion,
    TranslationError,
    expand,
    orbit,
    read_source,
    restricted_row_minimum,
)

#: The three folded Bidwell tilt classes, in degrees. ``H-239`` asks what share of the
#: LP's dual mass sits within half a degree of one of them; at or above half would mean
#: the cap signature X-014 predicts is present at 4.6198.
BIDWELL_CLASSES: tuple[float, ...] = (0.0, 36.62, 39.80)
BIDWELL_WINDOW = 0.5

#: Forked workers inherit this rather than receiving the expansion with every task: the
#: expansion is 8,988 sites and 7,853 rows of rationals, and pickling it 7,853 times
#: costs more than the sweep it carries.
_CONTEXT: dict[str, Any] = {}


class RepricingError(ValueError):
    """A control refuses the measurement, or the linear program cannot be read."""


@dataclass(frozen=True, slots=True)
class Support:
    """Which orbit each expanded site and each physical triple came from.

    `translate_kleddamag_certificate.expand` flattens the orbits and keeps no map back,
    because the unrestricted gate does not need one. The linear program does: its
    variables are orbits and its constraints are sites, so the charge at a cell has to be
    folded from sites onto the orbit that owns them.
    """

    site_orbit: tuple[int, ...]
    orbit_size: tuple[int, ...]
    triple_orbit: tuple[int, ...]
    triple_orbit_size: tuple[int, ...]
    orbit_weight: tuple[int, ...]
    triple_orbit_weight: tuple[int, ...]

    @property
    def variables(self) -> int:
        return len(self.orbit_size) + len(self.triple_orbit_size)


@dataclass(frozen=True, slots=True)
class RowCell:
    """One catalogue row's minimising cell, and the charge it carries."""

    row: int
    units: int
    slabs: int
    cells: int
    half_tangent: Fraction
    core_side: Fraction
    centre_x: Fraction
    centre_y: Fraction
    captured: int
    inside: bool
    meets: bool
    columns: np.ndarray
    counts: np.ndarray

    @property
    def degrees(self) -> float:
        """The core's rotation, from its half-tangent, for the dual histogram only."""
        return degrees(2 * atan(self.half_tangent))


def support_of(source: dict[str, Any], expansion: Expansion) -> Support:
    """Rebuild the orbit partition of the expanded sites and triples.

    Re-derived from the source in the same order `expand` walks it, rather than returned
    by it, so this module can be added without touching the translator that four other
    controls already stand on.
    """
    span = int(expansion.outer_side * expansion.coordinate_denominator)
    site_orbit: list[int] = []
    orbit_size: list[int] = []
    orbit_weight: list[int] = []
    for index, entry in enumerate(cast(list[Any], source["point_orbits"])):
        x, y, weight = (int(v) for v in entry)
        images = len(orbit(x, y, span))
        site_orbit.extend([index] * images)
        orbit_size.append(images)
        orbit_weight.append(weight)
    if len(site_orbit) != len(expansion.sites):
        raise RepricingError(
            f"the orbit partition covers {len(site_orbit)} sites, not {len(expansion.sites)}"
        )

    triple_orbit: list[int] = []
    triple_orbit_size: list[int] = []
    triple_orbit_weight: list[int] = []
    for index, entry in enumerate(cast(list[Any], source["threshold_orbits"])):
        count = len(cast(list[Any], entry["triples"]))
        triple_orbit.extend([index] * count)
        triple_orbit_size.append(count)
        triple_orbit_weight.append(int(entry["weight"]))
    if len(triple_orbit) != len(expansion.triples):
        raise RepricingError(
            f"the triple partition covers {len(triple_orbit)} triples, "
            f"not {len(expansion.triples)}"
        )
    return Support(
        site_orbit=tuple(site_orbit),
        orbit_size=tuple(orbit_size),
        triple_orbit=tuple(triple_orbit),
        triple_orbit_size=tuple(triple_orbit_size),
        orbit_weight=tuple(orbit_weight),
        triple_orbit_weight=tuple(triple_orbit_weight),
    )


def _row_geometry(
    expansion: Expansion, row: tuple[Fraction, Fraction, Fraction, Fraction]
) -> tuple[
    list[tuple[int, int]],
    dict[tuple[int, int, int, int], int],
    list[tuple[int, int]],
    int,
    int,
    int,
    int,
]:
    """The row's rotated site frame, signed capture rectangles and centre polygon.

    The same construction `translate_kleddamag_certificate._row_rectangles` makes and the
    artifact's own ``exact_mixed.geometry`` makes before it: the rotation enters as the
    integer pair ``(C, S) = (q^2 - p^2, 2pq)`` for the half-tangent ``t = p / q``, the
    half-side carries the matching ``R = q^2 + p^2``, and nothing rational survives into
    the sweep. It is repeated here rather than imported because this sweep needs the site
    frame itself -- the capture set at the minimising cell is read off it -- and the
    translator's helper returns only the rectangles.
    """
    a, b, t, side = row
    p, q = t.numerator, t.denominator
    cosine, sine, norm = q * q - p * p, 2 * p * q, q * q + p * p
    denominator = expansion.coordinate_denominator
    span = int(expansion.outer_side * denominator)

    def width(u: Fraction) -> Fraction:
        return (1 + 2 * u - u * u) / (1 + u * u)

    reach = expansion.parent_side * min(width(a), width(b)) / 2
    half_domain = expansion.outer_side / 2 - reach
    scale = lcm(2 * denominator, (side / 2).denominator, half_domain.denominator)
    factor = scale // (2 * denominator)
    domain = int(half_domain * scale)
    half = int(side * scale / 2) * norm
    frame = [
        (
            cosine * (2 * x - span) * factor + sine * (2 * y - span) * factor,
            -sine * (2 * x - span) * factor + cosine * (2 * y - span) * factor,
        )
        for x, y in expansion.sites
    ]
    rectangles: dict[tuple[int, int, int, int], int] = {}

    def insert(indices: tuple[int, ...], weight: int) -> None:
        if not weight:
            return
        us = [frame[i][0] for i in indices]
        vs = [frame[i][1] for i in indices]
        box = (max(us) - half, min(us) + half, max(vs) - half, min(vs) + half)
        if box[0] < box[1] and box[2] < box[3]:
            rectangles[box] = rectangles.get(box, 0) + weight

    for index, weight in enumerate(expansion.weights):
        insert((index,), weight)
    for (i, j, k), weight in zip(expansion.triples, expansion.triple_weights, strict=True):
        insert((i, j), weight)
        insert((i, k), weight)
        insert((j, k), weight)
        insert((i, j, k), -2 * weight)
    polygon = [
        (cosine * x + sine * y, -sine * x + cosine * y)
        for x, y in ((-domain, -domain), (domain, -domain), (domain, domain), (-domain, domain))
    ]
    live = {box: weight for box, weight in rectangles.items() if weight}
    # The frame map is ``(dx, dy) -> scale * (C dx + S dy, -S dx + C dy)`` and its inverse
    # divides by ``scale * (C^2 + S^2) = scale * norm^2``, not by ``scale * norm``: the
    # rotation enters unnormalised on both coordinates, so its determinant is ``norm^2``.
    return frame, live, polygon, half, cosine, sine, norm * norm * scale


def _polygon_window(
    polygon: list[tuple[int, int]], us: list[int], vs: list[int], row: int
) -> tuple[list[int], list[int]]:
    """Per-slab ``[first, last)`` cell windows over the restricted legal-centre polygon.

    The artifact walks its four edges for every slab; the polygon is convex, so exactly
    two of them span any slab inside it, and each edge spans a contiguous run of slabs.
    Evaluating each edge once per grid line instead of twice per slab is the whole of the
    difference, and ``K2`` and ``K3`` are what say the windows are the same windows.
    """
    index = {value: position for position, value in enumerate(us)}
    slabs = len(us) - 1
    first = [-1] * slabs
    last = [-1] * slabs
    low_num: list[int] = [0] * slabs
    low_den: list[int] = [0] * slabs
    high_num: list[int] = [0] * slabs
    high_den: list[int] = [0] * slabs
    hits = [0] * slabs
    for corner, start in enumerate(polygon):
        end = polygon[(corner + 1) % 4]
        if end[0] == start[0]:
            continue
        (u0, v0), (u1, v1) = (start, end) if start[0] < end[0] else (end, start)
        slope, offset, length = v1 - v0, v0 * (u1 - u0) - u0 * (v1 - v0), u1 - u0
        i0, i1 = index[u0], index[u1]
        values = [slope * us[i] + offset for i in range(i0, i1 + 1)]
        for slab in range(i0, i1):
            left, right = values[slab - i0], values[slab - i0 + 1]
            bottom = min(right, left)
            top = max(left, right)
            if hits[slab] == 0:
                low_num[slab], low_den[slab] = bottom, length
                high_num[slab], high_den[slab] = top, length
            else:
                if bottom * low_den[slab] < low_num[slab] * length:
                    low_num[slab], low_den[slab] = bottom, length
                if top * high_den[slab] > high_num[slab] * length:
                    high_num[slab], high_den[slab] = top, length
            hits[slab] += 1
    for slab in range(slabs):
        if hits[slab] == 0:
            continue
        if hits[slab] != 2:
            raise RepricingError(f"row {row} slab {slab} met {hits[slab]} polygon edges")
        first[slab] = bisect_right(vs, low_num[slab] // low_den[slab]) - 1
        last[slab] = bisect_left(vs, -((-high_num[slab]) // high_den[slab]))
        if not 0 <= first[slab] < last[slab] <= len(vs) - 1:
            raise RepricingError(f"row {row} slab {slab} left the event grid")
    return first, last


def minimising_cell(expansion: Expansion, support: Support, index: int) -> RowCell:
    """One catalogue row's least charge, and the cell and centre where it is attained.

    The sweep is the artifact's: signed rectangles from the expansion
    ``1[i + j + k >= 2] = ij + ik + jk - 2ijk``, a slab sweep in ``int64`` under the
    artifact's own ``sum(w) + 5 sum(w_t) < 2^50`` headroom, and the minimum taken only
    over cells the restricted legal-centre polygon reaches. What is added is the argmin:
    the slab and the cell, from which the centre follows by inverting the rotation
    exactly, and the capture set at that centre follows from the site frame.

    The representative centre is the cell's midpoint. Every rectangle boundary is a grid
    line, so the midpoint is strictly interior to the cell and the charge there is the
    cell's mass -- which ``K1`` then re-derives from the capture set and checks against
    the artifact's own replay.
    """
    row = expansion.rows[index]
    frame, rectangles, polygon, half, cosine, sine, unscale = _row_geometry(expansion, row)
    boxes = list(rectangles)
    weights = [rectangles[box] for box in boxes]
    us = sorted({point[0] for point in polygon} | {v for box in boxes for v in box[:2]})
    vs = sorted({point[1] for point in polygon} | {v for box in boxes for v in box[2:]})
    u_index = {value: i for i, value in enumerate(us)}
    v_index = {value: i for i, value in enumerate(vs)}
    low = np.array([v_index[box[2]] for box in boxes], np.int64)
    high = np.array([v_index[box[3]] for box in boxes], np.int64)
    events = sorted(
        [(u_index[box[0]], i, 1) for i, box in enumerate(boxes)]
        + [(u_index[box[1]], i, -1) for i, box in enumerate(boxes)]
    )
    first, last = _polygon_window(polygon, us, vs, index)

    masses = np.zeros(len(vs) - 1, np.int64)
    least: int | None = None
    best_slab = best_cell = -1
    slabs = cells = cursor = 0
    for slab in range(len(us) - 1):
        while cursor < len(events) and events[cursor][0] == slab:
            _, box, sign = events[cursor]
            masses[low[box] : high[box]] += sign * weights[box]
            cursor += 1
        if first[slab] < 0:
            continue
        window = masses[first[slab] : last[slab]]
        position = int(window.argmin())
        value = int(window[position])
        slabs += 1
        cells += last[slab] - first[slab]
        if least is None or value < least:
            least, best_slab, best_cell = value, slab, first[slab] + position
    if least is None:
        raise RepricingError(f"row {index} has no cell in its legal-centre polygon")

    twice_u = us[best_slab] + us[best_slab + 1]
    twice_v = vs[best_cell] + vs[best_cell + 1]
    reach = 2 * half
    captured = [
        i
        for i, (fu, fv) in enumerate(frame)
        if abs(2 * fu - twice_u) <= reach and abs(2 * fv - twice_v) <= reach
    ]
    flags = bytearray(len(frame))
    for i in captured:
        flags[i] = 1
    tally: dict[int, int] = {}
    for i in captured:
        key = support.site_orbit[i]
        tally[key] = tally.get(key, 0) + 1
    offset = len(support.orbit_size)
    for position, (i, j, k) in enumerate(expansion.triples):
        if flags[i] + flags[j] + flags[k] >= 2:
            key = offset + support.triple_orbit[position]
            tally[key] = tally.get(key, 0) + 1
    columns = sorted(tally)

    inside = _inside(polygon, Fraction(twice_u, 2), Fraction(twice_v, 2))
    legal = _legal_centre(
        polygon, (us[best_slab], us[best_slab + 1], vs[best_cell], vs[best_cell + 1])
    )
    if legal is not None and not _inside(polygon, legal[0], legal[1]):
        raise RepricingError(f"K5 row {index} produced a centre outside its own polygon")
    frame_u, frame_v = (
        legal if legal is not None else (Fraction(twice_u, 2), Fraction(twice_v, 2))
    )
    middle = expansion.outer_side / 2
    centre_x = middle + (cosine * frame_u - sine * frame_v) / unscale
    centre_y = middle + (sine * frame_u + cosine * frame_v) / unscale
    if not (0 <= centre_x <= expansion.outer_side and 0 <= centre_y <= expansion.outer_side):
        raise RepricingError(f"row {index} produced a centre outside the container")
    return RowCell(
        row=index,
        units=least,
        slabs=slabs,
        cells=cells,
        half_tangent=row[2],
        core_side=row[3],
        centre_x=centre_x,
        centre_y=centre_y,
        captured=len(captured),
        inside=inside,
        meets=legal is not None,
        columns=np.array(columns, np.int32),
        counts=np.array([tally[c] for c in columns], np.int32),
    )


def _inside(polygon: list[tuple[int, int]], u: Fraction, v: Fraction) -> bool:
    """Is the point inside the convex, counter-clockwise legal-centre polygon, exactly?"""
    signs: set[bool] = set()
    for corner, start in enumerate(polygon):
        end = polygon[(corner + 1) % 4]
        du, dv = end[0] - start[0], end[1] - start[1]
        cross = du * (v - start[1]) - dv * (u - start[0])
        if cross:
            signs.add(cross > 0)
    return len(signs) <= 1


def _legal_centre(
    polygon: list[tuple[int, int]], box: tuple[int, int, int, int]
) -> tuple[Fraction, Fraction] | None:
    """``K5``: a legal centre inside the minimising cell, or ``None`` if there is none.

    The sweep minimises over every cell the legal-centre polygon *reaches*, and it reaches
    a cell by a corner as readily as by its middle -- the window's ends are taken at the
    floor and ceiling of the polygon's own crossings, so a boundary cell counts whole. The
    cell's midpoint can therefore sit outside the parent-centre envelope even though the
    cell is one the artifact's own checker scores, and on this catalogue that is the
    common case rather than the exception, because a row's charge is least where its core
    is pushed hardest against a wall.

    The charge is constant on the open cell, so any interior point of the cell carries the
    swept minimum and captures the same sites. This clips the cell to the polygon and
    returns the intersection's centroid, which is interior to both whenever the
    intersection has positive area: the constraint is then at a centre a legal side-``A``
    parent could actually put its core at. ``None`` means the cell only touches the
    envelope on a set of measure zero, so no legal centre attains this row's swept
    minimum and the constraint is the artifact's window rather than its envelope.
    """
    u0, u1, v0, v1 = box
    subject: list[tuple[Fraction, Fraction]] = [
        (Fraction(u0), Fraction(v0)),
        (Fraction(u1), Fraction(v0)),
        (Fraction(u1), Fraction(v1)),
        (Fraction(u0), Fraction(v1)),
    ]
    for corner, start in enumerate(polygon):
        end = polygon[(corner + 1) % 4]
        du, dv = end[0] - start[0], end[1] - start[1]
        sides = [du * (v - start[1]) - dv * (u - start[0]) for u, v in subject]
        clipped: list[tuple[Fraction, Fraction]] = []
        for position, current in enumerate(subject):
            previous = subject[position - 1]
            here, before = sides[position], sides[position - 1]
            if (before < 0) != (here < 0):
                span = before - here
                if span:
                    ratio = before / span
                    clipped.append(
                        (
                            previous[0] + ratio * (current[0] - previous[0]),
                            previous[1] + ratio * (current[1] - previous[1]),
                        )
                    )
            if here >= 0:
                clipped.append(current)
        subject = clipped
        if len(subject) < 3:
            return None
    twice_area = Fraction(0)
    sum_u = Fraction(0)
    sum_v = Fraction(0)
    for current, following in zip(subject, [*subject[1:], subject[0]], strict=True):
        cross = current[0] * following[1] - following[0] * current[1]
        twice_area += cross
        sum_u += (current[0] + following[0]) * cross
        sum_v += (current[1] + following[1]) * cross
    if twice_area <= 0:
        return None
    return sum_u / (3 * twice_area), sum_v / (3 * twice_area)


def _initialise(expansion: Expansion, support: Support) -> None:
    _CONTEXT["expansion"] = expansion
    _CONTEXT["support"] = support


def _task(index: int) -> RowCell:
    return minimising_cell(_CONTEXT["expansion"], _CONTEXT["support"], index)


def sweep(
    expansion: Expansion,
    support: Support,
    sample: list[int],
    *,
    workers: int,
    quiet: bool,
) -> list[RowCell]:
    """Every sampled row's minimising cell, forked over ``workers`` processes."""
    started = time.perf_counter()
    if workers <= 1:
        _initialise(expansion, support)
        results: list[RowCell] = []
        for position, index in enumerate(sample):
            results.append(_task(index))
            if not quiet and position % 100 == 0:
                print(
                    f"  row {position + 1}/{len(sample)} (index {index}) "
                    f"{time.perf_counter() - started:.1f}s",
                    flush=True,
                )
        return results
    with ProcessPoolExecutor(
        max_workers=workers,
        mp_context=get_context("fork"),
        initializer=_initialise,
        initargs=(expansion, support),
    ) as pool:
        results = []
        for position, cell in enumerate(pool.map(_task, sample, chunksize=16)):
            results.append(cell)
            if not quiet and position % 200 == 0:
                print(
                    f"  row {position + 1}/{len(sample)} {time.perf_counter() - started:.1f}s",
                    flush=True,
                )
    return results


def replay_control(cells: list[RowCell], replay: dict[str, Any]) -> dict[str, Any]:
    """``K2``: this sweep's minimum, slab count and cell count against the artifact's."""
    rows = {int(entry["row"]): entry for entry in cast(list[Any], replay["rows"])}
    mismatched: list[int] = []
    for cell in cells:
        entry = rows.get(cell.row)
        if entry is None:
            raise RepricingError(f"the retained replay has no row {cell.row}")
        if (
            int(entry["minimum_units"]) != cell.units
            or int(entry["slabs"]) != cell.slabs
            or int(entry["cells"]) != cell.cells
        ):
            mismatched.append(cell.row)
    if mismatched:
        raise RepricingError(
            f"K2 {len(mismatched)} rows disagree with the retained replay: {mismatched[:8]}"
        )
    return {
        "rows_checked": len(cells),
        "fields": ["minimum_units", "slabs", "cells"],
        "mismatched": 0,
    }


def translator_control(
    expansion: Expansion, cells: list[RowCell], sample: list[int]
) -> dict[str, Any]:
    """``K3``: the translator's own sweep, on a sample, against this one."""
    found = {cell.row: cell for cell in cells}
    checked = 0
    for index in sample:
        cell = found.get(index)
        if cell is None:
            continue
        if restricted_row_minimum(expansion, index) != (cell.units, cell.slabs, cell.cells):
            raise RepricingError(f"K3 row {index} disagrees with restricted_row_minimum")
        checked += 1
    return {"rows_checked": checked, "against": "restricted_row_minimum"}


def build_matrix(cells: list[RowCell], support: Support) -> tuple[csr_array, np.ndarray]:
    """The integer constraint matrix and the integer budget objective.

    Column ``o < 1134`` is a point orbit, whose coefficient counts the orbit's captured
    sites and whose objective coefficient is the orbit's size; column ``1134 + s`` is a
    two-of-three orbit, whose coefficient counts its triples with at least two of three
    captured and whose objective coefficient is the number of triples in it. That is the
    artifact's own budget arithmetic: ``sum(weights) + sum(triple_weights)`` over the
    expanded objects, which is what ``K4`` re-derives.
    """
    indptr = np.zeros(len(cells) + 1, np.int64)
    for position, cell in enumerate(cells):
        indptr[position + 1] = indptr[position] + len(cell.columns)
    empty = np.empty(0, np.int32)
    indices = np.concatenate([cell.columns for cell in cells]) if cells else empty
    data = np.concatenate([cell.counts for cell in cells]) if cells else empty
    matrix = csr_array(
        (data.astype(np.int64), indices.astype(np.int64), indptr),
        shape=(len(cells), support.variables),
    )
    budget = np.array(
        list(support.orbit_size) + list(support.triple_orbit_size), dtype=np.int64
    )
    return matrix, budget


def artifact_control(
    matrix: csr_array,
    budget: np.ndarray,
    support: Support,
    expansion: Expansion,
    cells: list[RowCell],
) -> dict[str, Any]:
    """``K4``: the artifact's own weights, read back through the emitted program.

    Two equalities, and the second is the one that closes the loop. The objective has to
    return ``budget_units``, which says the columns are priced the way the artifact totals
    its budget. Each constraint has to return that row's own swept minimum, which says the
    capture set folded onto the orbits is the same charge the slab sweep found -- and
    ``K2`` has already matched those minima to the artifact's retained replay, so the
    matrix reproduces the artifact row by row before it is asked to improve on it.
    """
    weights = np.array(
        list(support.orbit_weight) + list(support.triple_orbit_weight), dtype=np.int64
    )
    total = int(budget @ weights)
    if total != expansion.budget_units:
        raise RepricingError(
            f"K4 the objective returns {total}, not the artifact's {expansion.budget_units}"
        )
    charges = np.asarray(matrix @ weights, dtype=np.int64)
    swept = np.array([cell.units for cell in cells], np.int64)
    wrong = np.flatnonzero(charges != swept)
    if wrong.size:
        rows = [cells[int(i)].row for i in wrong[:8]]
        raise RepricingError(
            f"K4 {wrong.size} constraints disagree with their own swept minimum: {rows}"
        )
    least = int(charges.min())
    complete = len(cells) == len(expansion.rows)
    if complete and least != expansion.minimum_units:
        raise RepricingError(
            f"K4 the least constraint returns {least}, "
            f"not the artifact's {expansion.minimum_units}"
        )
    baseline = Fraction(expansion.budget_units, expansion.minimum_units)
    return {
        "objective_units": total,
        "least_charge_units": least,
        "complete_catalogue": complete,
        "constraints_matching_sweep": int(charges.size),
        "normalised_mass": str(baseline),
        "normalised_mass_float": float(baseline),
        "normalised_mass_on_sample": str(Fraction(total, least)),
    }


def solve(
    matrix: csr_array,
    budget: np.ndarray,
    denominator: int,
    *,
    columns: np.ndarray | None = None,
) -> dict[str, Any]:
    """Solve the covering LP, then rationalise and re-verify its answer exactly.

    ``columns`` restricts the program to a subset of the orbits, which is how the run
    separates re-pricing the artifact's live support from turning its 282 zero-weight
    orbits on.

    The returned mass is ``K6``: the float solution is rounded onto the artifact's own
    ``1e-9`` weight grid, the least charge over the constraint set is recomputed in
    integers, and the mass reported is ``objective / least charge`` as an exact rational.
    That is the mass of a measure that is exactly feasible on the extracted cells after
    rescaling, so it is an exact *upper* bound on the relaxation's optimum, while the
    solver's own value is the corresponding estimate from below.
    """
    shape = cast(tuple[int, int], matrix.shape)
    active = np.arange(shape[1], dtype=np.int64) if columns is None else columns
    reduced = matrix[:, active]
    costs = budget[active].astype(float)
    started = time.perf_counter()
    result = linprog(
        c=costs,
        A_ub=-reduced.astype(float),
        b_ub=-np.ones(reduced.shape[0]),
        bounds=(0.0, None),
        method="highs",
    )
    seconds = time.perf_counter() - started
    if not result.success:
        raise RepricingError(f"the linear program did not solve: {result.message}")

    raw = np.maximum(np.asarray(result.x, dtype=float), 0.0)
    units = np.rint(raw * denominator).astype(np.int64)
    charges = reduced @ units
    least = int(charges.min())
    if least <= 0:
        raise RepricingError("K6 the rationalised solution charges nothing somewhere")
    total = int(budget[active] @ units)
    mass = Fraction(total, least)
    duals = np.maximum(-np.asarray(result.ineqlin.marginals, dtype=float), 0.0)
    floor, dual_support = _dual_bound(reduced, budget[active], duals, denominator)
    return {
        "variables": len(active),
        "constraints": int(reduced.shape[0]),
        "nonzeros": int(reduced.nnz),
        "solver_objective_float": float(result.fun),
        "exact_mass": str(mass),
        "exact_mass_float": float(mass),
        "exact_floor": str(floor),
        "exact_floor_float": float(floor),
        "dual_support": dual_support,
        "rationalised_objective_units": total,
        "rationalised_least_charge_units": least,
        "weight_denominator": denominator,
        "support": int(np.count_nonzero(units)),
        "seconds": round(seconds, 1),
        "duals": duals,
        "weights": units,
        "active": active,
    }


def _dual_bound(
    reduced: csr_array, costs: np.ndarray, duals: np.ndarray, denominator: int
) -> tuple[Fraction, int]:
    """An exact floor under the relaxation's optimum, from the solver's own dual.

    Weak duality: any ``y >= 0`` with ``A^T y <= c`` has ``sum(y) <= OPT``. The solver's
    dual is a float and satisfies neither inequality exactly, so it is rounded onto the
    same ``1e-9`` grid, clipped non-negative, and then scaled down by the largest factor
    that makes ``A^T y <= c`` hold in integers. What comes back is the exact mass of an
    exactly dual-feasible ``y``, and therefore a rational number no re-priced measure on
    this constraint set can go below.

    This is the half of the measurement that can settle the negative. The primal side
    returns an exact mass *above* the relaxation's optimum, which can only ever say that
    the relaxation has room; a floor at or above the artifact's own normalised mass would
    say the opposite, and say it about every measure on this support at this ``A``.
    """
    units = np.rint(duals * denominator).astype(np.int64)
    loads = np.asarray(reduced.T @ units, dtype=np.int64)
    room = costs.astype(np.int64) * denominator
    scale = None
    for position in np.flatnonzero(loads > 0):
        ratio = Fraction(int(room[position]), int(loads[position]))
        if scale is None or ratio < scale:
            scale = ratio
    if scale is None:
        return Fraction(0), 0
    return scale * Fraction(int(units.sum()), denominator), int(np.count_nonzero(units))


def separation_probe(
    expansion: Expansion,
    support: Support,
    solution: dict[str, Any],
    budget: np.ndarray,
    sample: list[int],
    *,
    workers: int,
    quiet: bool,
) -> dict[str, Any]:
    """One round of separation: what the re-priced measure actually charges.

    The linear program is a relaxation, and a relaxation's value is worth exactly as much
    as the question of whether its answer survives the constraints it dropped. This puts
    the LP's own weights back into the artifact's sweep and re-minimises over the *whole*
    continuum of a sample of rows, not over the one cell the program was given.

    By the same homogeneity the ``H-235`` screen uses, a measure of integer budget ``B``
    whose least charge over every row is ``G`` rescales to one charging at least 1
    everywhere with mass ``B / G``. The sample's least charge is an upper bound on the
    true ``G``, so ``B / G`` over the sample is a *lower* bound on the re-priced measure's
    real mass -- and a sample that already pushes it to 17 or past refutes the LP's answer
    as a certificate without sweeping the other rows. A sample that does not is silent:
    it takes every row to pass, and this takes a few hundred.
    """
    started = time.perf_counter()
    repriced, whole = _reprice(expansion, support, solution)
    total = int(budget @ whole)
    cells = sweep(repriced, support, sample, workers=workers, quiet=quiet)
    worst = min(cells, key=lambda cell: cell.units)
    mass = Fraction(total, worst.units) if worst.units > 0 else None
    return {
        "rows_swept": len(cells),
        "rows_available": len(expansion.rows),
        "budget_units": total,
        "least_charge_units": worst.units,
        "least_charge_row": worst.row,
        "least_charge": str(Fraction(worst.units, expansion.weight_denominator)),
        "least_charge_float": float(Fraction(worst.units, expansion.weight_denominator)),
        "mass_lower_bound": str(mass) if mass is not None else None,
        "mass_lower_bound_float": float(mass) if mass is not None else None,
        "survives_as_certificate_on_sample": bool(mass is not None and mass < 17),
        "seconds": round(time.perf_counter() - started, 1),
    }


def _reprice(
    expansion: Expansion, support: Support, solution: dict[str, Any]
) -> tuple[Expansion, np.ndarray]:
    """The expansion with the program's own weights on its sites and triples."""
    whole = np.zeros(support.variables, np.int64)
    whole[cast(np.ndarray, solution["active"])] = cast(np.ndarray, solution["weights"])
    offset = len(support.orbit_size)
    repriced = replace(
        expansion,
        weights=tuple(int(whole[o]) for o in support.site_orbit),
        triple_weights=tuple(int(whole[offset + t]) for t in support.triple_orbit),
    )
    if sum(repriced.weights) + 5 * sum(repriced.triple_weights) >= 2**50:
        raise RepricingError("the re-priced measure leaves the artifact's int64 headroom")
    return repriced, whole


def row_generate(
    expansion: Expansion,
    support: Support,
    budget: np.ndarray,
    sample: list[int],
    *,
    rounds: int,
    deadline: float,
    workers: int,
    quiet: bool,
) -> dict[str, Any]:
    """Re-price and re-separate a sub-catalogue until the sweep stops finding a cell.

    The one-cell-per-row program is a weak relaxation, and its weakness is measurable
    rather than arguable: the separation probe says how far the answer falls when the
    dropped cells come back. This closes the loop on a *stratified sub-catalogue*, which
    is the same relaxation applied to fewer rows and a far tighter one, because each row
    that is kept is kept whole.

    Two numbers come out and they say different things. The final program's exact dual
    floor is a lower bound on the optimum over the cells held, hence over the
    sub-catalogue, hence over the whole catalogue: a rigorous floor under any re-priced
    measure on this support at this ``A``. The final sweep's mass is what the loop's own
    measure achieves on those rows, an upper bound on the sub-catalogue's optimum and a
    lower bound on nothing. Convergence is when a round adds no cell, at which point the
    two meet and the sub-catalogue is solved exactly.
    """
    started = time.perf_counter()
    held = sweep(expansion, support, sample, workers=workers, quiet=quiet)
    seen = {(cell.row, cell.columns.tobytes(), cell.counts.tobytes()) for cell in held}
    log: list[dict[str, Any]] = []
    solution: dict[str, Any] | None = None
    stopped = "rounds exhausted"
    for index in range(rounds):
        matrix, _ = build_matrix(held, support)
        solution = solve(matrix, budget, expansion.weight_denominator)
        repriced, whole = _reprice(expansion, support, solution)
        fresh = sweep(repriced, support, sample, workers=workers, quiet=quiet)
        worst = min(fresh, key=lambda cell: cell.units)
        mass = Fraction(int(budget @ whole), worst.units) if worst.units > 0 else None
        added = 0
        for cell in fresh:
            key = (cell.row, cell.columns.tobytes(), cell.counts.tobytes())
            if key not in seen:
                seen.add(key)
                held.append(cell)
                added += 1
        log.append(
            {
                "round": index,
                "cells_held": len(held),
                "cells_added": added,
                "lp_floor_float": cast(float, solution["exact_floor_float"]),
                "lp_mass_float": cast(float, solution["exact_mass_float"]),
                "swept_mass": str(mass) if mass is not None else None,
                "swept_mass_float": float(mass) if mass is not None else None,
                "least_charge_units": worst.units,
                "least_charge_row": worst.row,
                "seconds": round(time.perf_counter() - started, 1),
            }
        )
        if not quiet:
            swept = f"{float(mass):.6f}" if mass is not None else "none"
            print(
                f"  round {index}: held {len(held)} (+{added}) "
                f"floor {solution['exact_floor_float']:.6f} swept {swept} "
                f"({time.perf_counter() - started:.1f}s)",
                flush=True,
            )
        if added == 0:
            stopped = "converged: the sweep found no cell the program had not priced"
            break
        if time.perf_counter() - started > deadline:
            stopped = "deadline reached"
            break
    if solution is None:
        raise RepricingError("row generation ran no round")
    return {
        "rows": len(sample),
        "rows_available": len(expansion.rows),
        "rounds": len(log),
        "stopped": stopped,
        "cells_held": len(held),
        "exact_floor": cast(str, solution["exact_floor"]),
        "exact_floor_float": cast(float, solution["exact_floor_float"]),
        "final_swept_mass": log[-1]["swept_mass"],
        "final_swept_mass_float": log[-1]["swept_mass_float"],
        "log": log,
        "seconds": round(time.perf_counter() - started, 1),
    }


def dual_histogram(cells: list[RowCell], duals: np.ndarray) -> dict[str, Any]:
    """``H-239``: what share of the dual mass sits at a folded Bidwell tilt class."""
    total = float(duals.sum())
    near = 0.0
    per_class = [0.0] * len(BIDWELL_CLASSES)
    for cell, value in zip(cells, duals.tolist(), strict=True):
        angle = cell.degrees
        for position, target in enumerate(BIDWELL_CLASSES):
            if abs(angle - target) <= BIDWELL_WINDOW:
                per_class[position] += float(value)
                near += float(value)
                break
    return {
        "window_degrees": BIDWELL_WINDOW,
        "classes": list(BIDWELL_CLASSES),
        "total_dual_mass": total,
        "near_class_mass": near,
        "near_class_fraction": (near / total) if total else 0.0,
        "per_class_mass": per_class,
        "support_rows": int(np.count_nonzero(duals)),
        "signature_present": bool(total and near / total >= 0.5),
    }


def slack_summary(cells: list[RowCell], expansion: Expansion) -> dict[str, Any]:
    """The slack distribution the re-pricing question rests on, recomputed here.

    X-042 reports it from one-off code and calls the reading ``V0/C0``; it is the whole
    argument for this lane, so it is re-measured from the swept minima -- which ``K2`` has
    already matched, row by row, to the artifact's own retained replay. A measure whose
    row minima pile onto one plateau far above the global minimum is one that was priced
    against a catalogue it no longer has.
    """
    units = [cell.units for cell in cells]
    tally: dict[int, int] = {}
    for value in units:
        tally[value] = tally.get(value, 0) + 1
    plateau = sorted(tally.items(), key=lambda item: (-item[1], item[0]))[:3]
    least = min(units)
    denominator = expansion.weight_denominator
    windows = {
        f"within_{gap}_units": sum(1 for value in units if value - least <= gap)
        for gap in (10, 10**4, 10**5, 5 * 10**5, 10**6)
    }
    above = sum(1 for value in units if value >= denominator + 2040000)
    return {
        "rows": len(units),
        "least_units": least,
        "least_rows": [cell.row for cell in cells if cell.units == least],
        "plateau": [{"units": value, "rows": count} for value, count in plateau],
        "plateau_share": round(sum(count for _, count in plateau) / max(len(units), 1), 4),
        "rows_at_or_above_slack_2040e-6": above,
        "windows_above_least": windows,
    }


#: The two pre-declared thresholds. Below ``16.99`` there is real room on this support at
#: this ``A``; at or above ``16.998`` -- the artifact's own normalised mass to three places
#: -- there is none, and the next rung is a sites problem rather than a pricing one.
HEADROOM_AT = Fraction(1699, 100)
NO_HEADROOM_AT = Fraction(16998, 1000)


def verdict_of(floor: Fraction, mass: Fraction) -> str:
    """The pre-declared discriminator, read off the exact bracket.

    The two sides are not symmetric and the asymmetry is the point. ``mass`` is an exact
    *upper* bound on the relaxation's optimum, so ``mass`` under ``16.99`` says the
    relaxation has room -- and the relaxation is not the problem a certificate has to
    solve, so that is a signal and not a result. ``floor`` is an exact *lower* bound on
    the same optimum and therefore on the unrelaxed problem's optimum too, so ``floor`` at
    or above ``16.998`` settles the negative outright.
    """
    if floor >= NO_HEADROOM_AT:
        return "no-headroom"
    if mass < HEADROOM_AT:
        return "headroom-in-the-relaxation"
    return "inconclusive"


def write_cells(path: Path, cells: list[RowCell]) -> None:
    """One JSON object per row: the cell, its centre and its charge, exact."""
    with path.open("w", encoding="utf-8") as handle:
        for cell in cells:
            handle.write(
                json.dumps(
                    {
                        "row": cell.row,
                        "minimum_units": cell.units,
                        "slabs": cell.slabs,
                        "cells": cell.cells,
                        "half_tangent": str(cell.half_tangent),
                        "core_side": str(cell.core_side),
                        "centre_x": str(cell.centre_x),
                        "centre_y": str(cell.centre_y),
                        "captured_sites": cell.captured,
                        "midpoint_inside_envelope": cell.inside,
                        "cell_meets_envelope": cell.meets,
                        "columns": len(cell.columns),
                        "core_degrees_float": cell.degrees,
                    }
                )
                + "\n"
            )


def save_matrix(
    path: Path, matrix: csr_array, budget: np.ndarray, cells: list[RowCell]
) -> None:
    """The program's integer bytes, so a later solve need not re-sweep."""
    np.savez_compressed(
        path,
        data=matrix.data,
        indices=matrix.indices,
        indptr=matrix.indptr,
        shape=np.array(matrix.shape, np.int64),
        budget=budget,
        rows=np.array([cell.row for cell in cells], np.int64),
        units=np.array([cell.units for cell in cells], np.int64),
        half_tangent_p=np.array([cell.half_tangent.numerator for cell in cells], object),
        half_tangent_q=np.array([cell.half_tangent.denominator for cell in cells], object),
        inside=np.array([cell.inside for cell in cells], bool),
        meets=np.array([cell.meets for cell in cells], bool),
    )


def load_matrix(path: Path) -> tuple[csr_array, np.ndarray, list[RowCell]]:
    """Read back what `save_matrix` wrote, as the program and its row stubs."""
    with np.load(path, allow_pickle=True) as bundle:
        matrix = csr_array(
            (bundle["data"], bundle["indices"], bundle["indptr"]),
            shape=tuple(int(v) for v in bundle["shape"]),
        )
        budget = bundle["budget"]
        rows = [int(v) for v in bundle["rows"]]
        units = [int(v) for v in bundle["units"]]
        ps = list(bundle["half_tangent_p"])
        qs = list(bundle["half_tangent_q"])
        inside = [bool(v) for v in bundle["inside"]]
        meets = [bool(v) for v in bundle["meets"]]
    empty = np.empty(0, np.int32)
    cells = [
        RowCell(
            row=rows[i],
            units=units[i],
            slabs=0,
            cells=0,
            half_tangent=Fraction(int(ps[i]), int(qs[i])),
            core_side=Fraction(0),
            centre_x=Fraction(0),
            centre_y=Fraction(0),
            captured=0,
            inside=inside[i],
            meets=meets[i],
            columns=empty,
            counts=empty,
        )
        for i in range(len(rows))
    ]
    return matrix, budget, cells


def _sample(total: int, stride: int, limit: int | None) -> list[int]:
    chosen = list(range(0, total, max(stride, 1)))
    if total - 1 not in chosen:
        chosen.append(total - 1)
    if limit is not None:
        chosen = chosen[:limit]
    return chosen


def _report_solution(name: str, solution: dict[str, Any]) -> dict[str, Any]:
    trimmed = {k: v for k, v in solution.items() if k not in {"duals", "weights", "active"}}
    trimmed["verdict"] = verdict_of(
        Fraction(cast(str, solution["exact_floor"])),
        Fraction(cast(str, solution["exact_mass"])),
    )
    print(
        f"  {name}: exact bracket [{solution['exact_floor_float']:.9f}, "
        f"{solution['exact_mass_float']:.9f}] "
        f"(solver {solution['solver_objective_float']:.9f}), "
        f"support {solution['support']}, {solution['seconds']}s "
        f"-> {trimmed['verdict']}",
        flush=True,
    )
    return trimmed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__ and __doc__.splitlines()[0])
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--replay", type=Path, default=REPLAY)
    parser.add_argument("--stride", type=int, default=1, help="sweep every Nth catalogue row")
    parser.add_argument("--limit", type=int, default=None, help="cap the number of rows swept")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--control-rows", type=int, default=8, help="rows given to K3")
    parser.add_argument("--cells", type=Path, default=None)
    parser.add_argument("--matrix", type=Path, default=None)
    parser.add_argument("--from-matrix", type=Path, default=None)
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--skip-lp", action="store_true")
    parser.add_argument(
        "--rowgen-rows",
        type=int,
        default=0,
        help="row-generate on this many stratified rows after the one-cell program",
    )
    parser.add_argument("--rowgen-rounds", type=int, default=40)
    parser.add_argument("--rowgen-deadline", type=float, default=900.0)
    parser.add_argument(
        "--separation-rows",
        type=int,
        default=0,
        help="re-sweep this many rows with the LP's own weights, one round of separation",
    )
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    started = time.perf_counter()
    source, digest = read_source(args.source)
    expansion = expand(source)
    support = support_of(source, expansion)
    report: dict[str, Any] = {
        "source": str(args.source),
        "source_sha256": digest,
        "outer_side": str(expansion.outer_side),
        "parent_side": str(expansion.parent_side),
        "point_orbits": len(support.orbit_size),
        "threshold_orbits": len(support.triple_orbit_size),
        "variables": support.variables,
        "catalogue_rows": len(expansion.rows),
    }

    if args.from_matrix is not None:
        matrix, budget, cells = load_matrix(args.from_matrix)
        report["loaded_from"] = str(args.from_matrix)
    else:
        sample = _sample(len(expansion.rows), args.stride, args.limit)
        if not args.quiet:
            print(f"sweeping {len(sample)} rows on {args.workers} workers", flush=True)
        cells = sweep(expansion, support, sample, workers=args.workers, quiet=args.quiet)
        report["sweep_seconds"] = round(time.perf_counter() - started, 1)
        report["rows_swept"] = len(cells)
        text = args.replay.read_text(encoding="utf-8")
        report["K2_replay"] = replay_control(cells, cast(dict[str, Any], json.loads(text)))
        wanted = max(args.control_rows, 1)
        stride = max(len(cells) // wanted, 1)
        control = [cell.row for cell in cells[::stride]][:wanted]
        report["K3_translator"] = translator_control(expansion, cells, control)
        matrix, budget = build_matrix(cells, support)
        if args.cells is not None:
            write_cells(args.cells, cells)
        if args.matrix is not None:
            save_matrix(args.matrix, matrix, budget, cells)

    report["K4_artifact"] = artifact_control(matrix, budget, support, expansion, cells)
    outside = [cell.row for cell in cells if not cell.inside]
    detached = [cell.row for cell in cells if not cell.meets]
    report["K5_envelope"] = {
        "rows": len(cells),
        "midpoint_outside": len(outside),
        "cell_detached_from_envelope": len(detached),
        "detached_examples": detached[:8],
        "note": (
            "the sweep window is the artifact's own and takes a boundary cell whole, so a "
            "cell's midpoint can lie outside the parent-centre envelope; a detached row is "
            "one whose minimising cell meets the envelope in measure zero, and only there "
            "is the constraint the artifact's window rather than its envelope"
        ),
    }
    report["slack"] = slack_summary(cells, expansion)
    report["captured_sites"] = {
        "least": min((cell.captured for cell in cells), default=0),
        "greatest": max((cell.captured for cell in cells), default=0),
    }

    if not args.skip_lp:
        print("solving the covering LP on the extracted cells", flush=True)
        full = solve(matrix, budget, expansion.weight_denominator)
        report["lp_full"] = _report_solution("all orbits", full)
        live = np.array(
            [i for i, w in enumerate(support.orbit_weight) if w]
            + [
                len(support.orbit_size) + i
                for i, w in enumerate(support.triple_orbit_weight)
                if w
            ],
            dtype=np.int64,
        )
        restricted = solve(matrix, budget, expansion.weight_denominator, columns=live)
        report["lp_positive_orbits_only"] = _report_solution("positive orbits", restricted)
        if detached:
            keep = np.array([i for i, cell in enumerate(cells) if cell.meets], np.int64)
            legal = solve(matrix[keep, :], budget, expansion.weight_denominator)
            report["lp_envelope_cells_only"] = _report_solution("envelope cells", legal)
        report["H239_dual"] = dual_histogram(cells, full["duals"])
        if args.separation_rows > 0:
            stride = max(len(expansion.rows) // args.separation_rows, 1)
            probe = _sample(len(expansion.rows), stride, None)
            report["separation"] = separation_probe(
                expansion,
                support,
                full,
                budget,
                probe,
                workers=args.workers,
                quiet=args.quiet,
            )
        report["headroom"] = {
            "artifact_normalised_mass": report["K4_artifact"]["normalised_mass"],
            "lp_exact_floor": full["exact_floor"],
            "lp_exact_mass": full["exact_mass"],
            "difference": str(
                Fraction(cast(str, report["K4_artifact"]["normalised_mass"]))
                - Fraction(cast(str, full["exact_mass"]))
            ),
            "difference_float": float(
                Fraction(cast(str, report["K4_artifact"]["normalised_mass"]))
                - Fraction(cast(str, full["exact_mass"]))
            ),
            "verdict": verdict_of(
                Fraction(cast(str, full["exact_floor"])),
                Fraction(cast(str, full["exact_mass"])),
            ),
        }

        if args.rowgen_rows > 0:
            stride = max(len(expansion.rows) // args.rowgen_rows, 1)
            report["rowgen"] = row_generate(
                expansion,
                support,
                budget,
                _sample(len(expansion.rows), stride, None),
                rounds=args.rowgen_rounds,
                deadline=args.rowgen_deadline,
                workers=args.workers,
                quiet=args.quiet,
            )
            floor = max(
                Fraction(cast(str, full["exact_floor"])),
                Fraction(cast(str, report["rowgen"]["exact_floor"])),
            )
            report["headroom"]["best_exact_floor"] = str(floor)
            report["headroom"]["best_exact_floor_float"] = float(floor)
            report["headroom"]["verdict"] = verdict_of(
                floor, Fraction(cast(str, full["exact_mass"]))
            )

    report["seconds"] = round(time.perf_counter() - started, 1)
    if args.report is not None:
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in report.items() if not k.startswith("lp_")},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RepricingError, TranslationError) as error:
        print(f"refused: {error}")
        raise SystemExit(1) from None
