#!/usr/bin/env python3
"""Paired fixed-support covering LPs for four flush corner obstacles.

This is an exploratory instrument, not a packing-bound verifier.  It compares an
unrestricted covering LP with the conditional LP whose ``B``-square placements avoid
four axis-aligned unit squares fixed flush in the container corners.  Both arms use the
same finite direction subset and the same D4-closed candidate support.  The reported
score is ``M_global - M_residual - 4``; it is never compared with an unrelated primal
packing mass.

The residual centre domain is an exact union of six convex rational pieces.  Search is
floating point, and every run record says so.  A run writes its raw solver point after
each arm, including on a deadline stop.  Exact replay is deliberately a separate step;
``exact_minimum_covered_mass`` is retained here for that reader and for independent
small controls.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import pairwise
from math import lcm
from pathlib import Path
from typing import Any, cast

import numpy as np
from scipy.optimize import linprog

from sqpack.cover import write_text_atomic
from sqpack.fractional.colgen import (
    SiteSet,
    rationalise_sites,
    site_set_from_grids,
    site_set_from_points,
)
from sqpack.fractional.generate import LP_FEASIBILITY, direction_net, net_half_tangents
from sqpack.fractional.model import Atom, Direction, require_nonnegative_atom_weights
from sqpack.fractional.sweep import centre_domain

ANGLE_LIMIT = Fraction(207107, 500000)
DEFAULT_SCALE = 4_000_000
DOMAIN_LABELS = (
    "vertical-central-strip",
    "horizontal-central-strip",
    "bottom-left-cap",
    "bottom-right-cap",
    "top-left-cap",
    "top-right-cap",
)

type Point = tuple[Fraction, Fraction]
type Polygon = tuple[Point, ...]
type FloatPolygon = tuple[tuple[float, float], ...]


@dataclass(frozen=True, slots=True)
class HalfPlane:
    """The closed half-plane ``a*u + b*v <= bound`` in the rotated frame."""

    a: Fraction | float
    b: Fraction | float
    bound: Fraction | float


@dataclass(frozen=True, slots=True)
class Complexity:
    """Worst fixed-support dense grids for one separation round."""

    per_direction: tuple[int, ...]

    @property
    def maximum(self) -> int:
        return max(self.per_direction, default=0)

    @property
    def total(self) -> int:
        return sum(self.per_direction)

    def as_dict(self, indices: tuple[int, ...]) -> dict[str, object]:
        return {
            "kind": "all-support dense-event-cell upper estimate per separation round",
            "selected_directions": len(indices),
            "maximum_cells_one_direction": self.maximum,
            "sum_cells_one_round": self.total,
            "by_direction": [
                {"direction_index": index, "dense_cells": cells}
                for index, cells in zip(indices, self.per_direction, strict=True)
            ],
        }


@dataclass(slots=True)
class RoundRecord:
    index: int
    rows_held: int
    rows_added: int
    violated: int
    objective: float | None
    least_covered: float | None
    dense_cells: int
    seconds: float


@dataclass(slots=True)
class ProgramSolution:
    """One raw floating-point point, whether converged or stopped early."""

    weights: np.ndarray
    stopped: str
    objective: float | None = None
    least_covered: float | None = None
    rows: int = 0
    rounds: list[RoundRecord] = field(default_factory=list)
    seconds: float = 0.0

    @property
    def converged(self) -> bool:
        return self.stopped.startswith("converged")


def _clip_polygon(polygon: tuple[tuple[Any, Any], ...], half_plane: HalfPlane) -> tuple:
    """Clip one convex polygon, preserving exact arithmetic when its inputs are exact."""

    if not polygon:
        return ()
    a, b, bound = half_plane.a, half_plane.b, half_plane.bound
    output: list[tuple[Any, Any]] = []

    def signed(point: tuple[Any, Any]) -> Any:
        return a * point[0] + b * point[1] - bound

    previous = polygon[-1]
    previous_value = signed(previous)
    previous_inside = previous_value <= 0
    for current in polygon:
        current_value = signed(current)
        current_inside = current_value <= 0
        if current_inside != previous_inside:
            factor = previous_value / (previous_value - current_value)
            output.append(
                (
                    previous[0] + factor * (current[0] - previous[0]),
                    previous[1] + factor * (current[1] - previous[1]),
                )
            )
        if current_inside:
            output.append(current)
        previous = current
        previous_value = current_value
        previous_inside = current_inside
    # Repeated vertices arise when a clipping line passes through a vertex.  They do
    # not change the polygon, but removing them makes area and witness checks clearer.
    cleaned: list[tuple[Any, Any]] = []
    for point in output:
        if not cleaned or point != cleaned[-1]:
            cleaned.append(point)
    if len(cleaned) > 1 and cleaned[0] == cleaned[-1]:
        cleaned.pop()
    return tuple(cleaned)


def _clip_many(polygon: Polygon, half_planes: tuple[HalfPlane, ...]) -> Polygon:
    clipped: tuple = polygon
    for half_plane in half_planes:
        clipped = _clip_polygon(clipped, half_plane)
        if not clipped:
            break
    return cast(Polygon, clipped)


def _xy_half_planes(
    *,
    cosine: Fraction,
    sine: Fraction,
    x_low: Fraction | None = None,
    x_high: Fraction | None = None,
    y_low: Fraction | None = None,
    y_high: Fraction | None = None,
) -> tuple[HalfPlane, ...]:
    """Bounds on ``x=c*u-s*v`` and ``y=s*u+c*v`` as rotated-frame planes."""

    planes: list[HalfPlane] = []
    if x_low is not None:
        planes.append(HalfPlane(-cosine, sine, -x_low))
    if x_high is not None:
        planes.append(HalfPlane(cosine, -sine, x_high))
    if y_low is not None:
        planes.append(HalfPlane(-sine, -cosine, -y_low))
    if y_high is not None:
        planes.append(HalfPlane(sine, cosine, y_high))
    return tuple(planes)


def residual_domain_pieces(
    outer_side: Fraction, square_side: Fraction, direction: Direction
) -> tuple[Polygon, ...]:
    """Exact centres of cores avoiding four flush axis-aligned corner units.

    The six components are kept separate.  In a fixed ``u`` slab their vertical
    sections need not join, so replacing them by one min/max interval would admit a
    forbidden gap.  All inequalities are weak: obstacle tangency is admissible.
    """

    cosine, sine = direction.ux, direction.uy
    if cosine < 0 or sine < 0:
        raise ValueError("the six-piece contract requires a first-quadrant direction")
    half = square_side / 2
    extent = half * (cosine + sine)
    low, high = 1 + extent, outer_side - 1 - extent
    if low > high:
        raise ValueError("corner obstacles leave no central-strip ordering at this setting")
    domain = centre_domain(outer_side, square_side, direction)
    components = (
        _xy_half_planes(cosine=cosine, sine=sine, x_low=low, x_high=high),
        _xy_half_planes(cosine=cosine, sine=sine, y_low=low, y_high=high),
        (
            *_xy_half_planes(cosine=cosine, sine=sine, x_high=low, y_high=low),
            HalfPlane(Fraction(-1), Fraction(0), -(cosine + sine + half)),
        ),
        (
            *_xy_half_planes(cosine=cosine, sine=sine, x_low=high, y_high=low),
            HalfPlane(
                Fraction(0),
                Fraction(-1),
                -(cosine - sine * (outer_side - 1) + half),
            ),
        ),
        (
            *_xy_half_planes(cosine=cosine, sine=sine, x_high=low, y_low=high),
            HalfPlane(Fraction(0), Fraction(1), cosine * (outer_side - 1) - sine - half),
        ),
        (
            *_xy_half_planes(cosine=cosine, sine=sine, x_low=high, y_low=high),
            HalfPlane(
                Fraction(1),
                Fraction(0),
                (cosine + sine) * (outer_side - 1) - half,
            ),
        ),
    )
    return tuple(_clip_many(domain, planes) for planes in components)


def unrestricted_domain_pieces(
    outer_side: Fraction, square_side: Fraction, direction: Direction
) -> tuple[Polygon, ...]:
    return (centre_domain(outer_side, square_side, direction),)


def _area_twice(polygon: tuple[tuple[Any, Any], ...]) -> Any:
    if len(polygon) < 3:
        return 0
    return sum(
        x0 * y1 - y0 * x1
        for (x0, y0), (x1, y1) in zip(polygon, polygon[1:] + polygon[:1], strict=True)
    )


def point_in_closed_polygon(point: Point, polygon: Polygon) -> bool:
    """Exact membership in a convex polygon of either orientation."""

    if not polygon:
        return False
    if len(polygon) == 1:
        return point == polygon[0]
    if _area_twice(polygon) == 0:
        for first, second in zip(polygon, polygon[1:] + polygon[:1], strict=True):
            cross = (second[0] - first[0]) * (point[1] - first[1]) - (second[1] - first[1]) * (
                point[0] - first[0]
            )
            if (
                cross == 0
                and min(first[0], second[0]) <= point[0] <= max(first[0], second[0])
                and min(first[1], second[1]) <= point[1] <= max(first[1], second[1])
            ):
                return True
        return False
    signs: set[int] = set()
    for first, second in zip(polygon, polygon[1:] + polygon[:1], strict=True):
        value = (second[0] - first[0]) * (point[1] - first[1]) - (second[1] - first[1]) * (
            point[0] - first[0]
        )
        if value:
            signs.add(1 if value > 0 else -1)
    return len(signs) <= 1


def _float_pieces(pieces: tuple[Polygon, ...]) -> tuple[FloatPolygon, ...]:
    return tuple(tuple((float(u), float(v)) for u, v in polygon) for polygon in pieces)


def _with_cell_bounds(
    polygon: tuple[tuple[Any, Any], ...], u0: Any, u1: Any, v0: Any, v1: Any
) -> tuple:
    clipped: tuple = polygon
    for half_plane in (
        HalfPlane(Fraction(-1), Fraction(0), -u0),
        HalfPlane(Fraction(1), Fraction(0), u1),
        HalfPlane(Fraction(0), Fraction(-1), -v0),
        HalfPlane(Fraction(0), Fraction(1), v1),
    ):
        clipped = _clip_polygon(clipped, half_plane)
        if not clipped:
            break
    return clipped


def reachable_spans(
    u_events: tuple[Any, ...],
    v_events: tuple[Any, ...],
    pieces: tuple[tuple[tuple[Any, Any], ...], ...],
) -> tuple[tuple[int, int, int], ...]:
    """Union piece reachability as disjoint inclusive ``j`` spans per ``u`` slab."""

    spans: list[tuple[int, int, int]] = []
    for i, (u0, u1) in enumerate(pairwise(u_events)):
        ranges: list[tuple[int, int]] = []
        for polygon in pieces:
            if len(polygon) < 3 or _area_twice(polygon) == 0:
                continue
            if max(u for u, _ in polygon) <= u0 or min(u for u, _ in polygon) >= u1:
                continue
            slab = _clip_polygon(
                _clip_polygon(polygon, HalfPlane(Fraction(-1), Fraction(0), -u0)),
                HalfPlane(Fraction(1), Fraction(0), u1),
            )
            if len(slab) < 3:
                continue
            low = min(v for _, v in slab)
            high = max(v for _, v in slab)
            if high <= low:
                continue
            j0 = max(0, bisect_right(v_events, low) - 1)
            j1 = min(len(v_events) - 2, bisect_left(v_events, high) - 1)
            if j0 <= j1:
                ranges.append((j0, j1))
        if not ranges:
            continue
        ranges.sort()
        first, last = ranges[0]
        for next_first, next_last in ranges[1:]:
            if next_first <= last + 1:
                last = max(last, next_last)
            else:
                spans.append((i, first, last))
                first, last = next_first, next_last
        spans.append((i, first, last))
    return tuple(spans)


def _event_arrays(
    points: np.ndarray,
    weights: np.ndarray,
    direction: Direction,
    square_side: float,
    pieces: tuple[FloatPolygon, ...],
    *,
    all_points: bool,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    cosine, sine = float(direction.ux), float(direction.uy)
    half = square_side / 2
    u = points[:, 0] * cosine + points[:, 1] * sine
    v = -points[:, 0] * sine + points[:, 1] * cosine
    if all_points:
        live = np.ones(points.shape[0], dtype=bool)
    else:
        live = weights > 0
        if not live.any():
            stride = max(1, math.ceil(points.shape[0] / 600))
            live = np.zeros(points.shape[0], dtype=bool)
            live[::stride] = True
    vertices = [point for polygon in pieces for point in polygon]
    if not vertices:
        raise ValueError("the centre domain is empty")
    vertex_u = np.array([point[0] for point in vertices])
    vertex_v = np.array([point[1] for point in vertices])
    u_events = np.unique(np.concatenate((u[live] - half, u[live] + half, vertex_u)))
    v_events = np.unique(np.concatenate((v[live] - half, v[live] + half, vertex_v)))
    return u, v, live, u_events, v_events


def _dense_mass_grid(
    points: np.ndarray,
    weights: np.ndarray,
    direction: Direction,
    square_side: float,
    pieces: tuple[FloatPolygon, ...],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    u, v, live, u_events, v_events = _event_arrays(
        points, weights, direction, square_side, pieces, all_points=False
    )
    half = square_side / 2
    live_u, live_v, live_weights = u[live], v[live], weights[live]
    grid = np.zeros((len(u_events), len(v_events)))
    left = np.searchsorted(u_events, live_u - half)
    right = np.searchsorted(u_events, live_u + half)
    bottom = np.searchsorted(v_events, live_v - half)
    top = np.searchsorted(v_events, live_v + half)
    np.add.at(grid, (left, bottom), live_weights)
    np.add.at(grid, (right, bottom), -live_weights)
    np.add.at(grid, (left, top), -live_weights)
    np.add.at(grid, (right, top), live_weights)
    mass = np.cumsum(np.cumsum(grid, axis=1), axis=0)[:-1, :-1]
    return u, v, u_events, v_events, mass


def _exact_geometry_mass_grid(
    points: tuple[Point, ...],
    weights: np.ndarray,
    direction: Direction,
    square_side: Fraction,
    pieces: tuple[Polygon, ...],
) -> tuple[tuple[Point, ...], tuple[Fraction, ...], tuple[Fraction, ...], np.ndarray]:
    """Rebuild one ambiguous event grid from the original rational sites."""

    if len(points) != len(weights):
        raise ValueError("exact site provenance does not match the float support")
    live = weights > 0
    if not live.any():
        stride = max(1, math.ceil(len(points) / 600))
        live = np.zeros(len(points), dtype=bool)
        live[::stride] = True
    projected = tuple(
        (
            direction.ux * x + direction.uy * y,
            direction.vx * x + direction.vy * y,
        )
        for x, y in points
    )
    half = square_side / 2
    u_events = tuple(
        sorted(
            {
                u + offset
                for (u, _), is_live in zip(projected, live, strict=True)
                if is_live
                for offset in (-half, half)
            }
            | {u for polygon in pieces for u, _ in polygon}
        )
    )
    v_events = tuple(
        sorted(
            {
                v + offset
                for (_, v), is_live in zip(projected, live, strict=True)
                if is_live
                for offset in (-half, half)
            }
            | {v for polygon in pieces for _, v in polygon}
        )
    )
    u_index = {value: index for index, value in enumerate(u_events)}
    v_index = {value: index for index, value in enumerate(v_events)}
    grid = np.zeros((len(u_events), len(v_events)))
    for (u, v), weight, keep in zip(projected, weights, live, strict=True):
        if not keep:
            continue
        left, right = u_index[u - half], u_index[u + half]
        bottom, top = v_index[v - half], v_index[v + half]
        grid[left, bottom] += weight
        grid[right, bottom] -= weight
        grid[left, top] -= weight
        grid[right, top] += weight
    mass = np.cumsum(np.cumsum(grid, axis=1), axis=0)[:-1, :-1]
    return projected, u_events, v_events, mass


def _witness_for_cell(
    pieces: tuple[FloatPolygon, ...],
    u0: float,
    u1: float,
    v0: float,
    v1: float,
) -> tuple[float, float]:
    for polygon in pieces:
        clipped = _with_cell_bounds(polygon, u0, u1, v0, v1)
        if len(clipped) < 3 or abs(float(_area_twice(clipped))) <= 1e-18:
            continue
        centre = (
            sum(u for u, _ in clipped) / len(clipped),
            sum(v for _, v in clipped) / len(clipped),
        )
        if u0 < centre[0] < u1 and v0 < centre[1] < v1:
            return float(centre[0]), float(centre[1])
    raise ValueError("reachable residual cell has no interior witness")


def _exact_witness_for_cell(
    pieces: tuple[Polygon, ...],
    u0: Fraction,
    u1: Fraction,
    v0: Fraction,
    v1: Fraction,
) -> Point:
    for polygon in pieces:
        clipped = cast(Polygon, _with_cell_bounds(polygon, u0, u1, v0, v1))
        if len(clipped) < 3 or _area_twice(clipped) == 0:
            continue
        centre = (
            sum((u for u, _ in clipped), Fraction(0)) / len(clipped),
            sum((v for _, v in clipped), Fraction(0)) / len(clipped),
        )
        if u0 < centre[0] < u1 and v0 < centre[1] < v1:
            return centre
    raise ValueError("exact reachable residual cell has no interior witness")


def _core_is_admissible_exact(
    centre_uv: Point,
    direction: Direction,
    outer_side: Fraction,
    square_side: Fraction,
    *,
    residual: bool,
) -> bool:
    """Full exact SAT check, independent of the six-piece clipping formulas."""

    cosine, sine = direction.ux, direction.uy
    u, v = centre_uv
    x, y = cosine * u - sine * v, sine * u + cosine * v
    extent = square_side * (cosine + sine) / 2
    if not (extent <= x <= outer_side - extent and extent <= y <= outer_side - extent):
        return False
    if not residual:
        return True
    half = square_side / 2
    obstacles = (
        (Fraction(1, 2), Fraction(1, 2)),
        (outer_side - Fraction(1, 2), Fraction(1, 2)),
        (Fraction(1, 2), outer_side - Fraction(1, 2)),
        (outer_side - Fraction(1, 2), outer_side - Fraction(1, 2)),
    )
    axes = (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (cosine, sine),
        (-sine, cosine),
    )
    for obstacle_x, obstacle_y in obstacles:
        separated = False
        for axis_x, axis_y in axes:
            core_radius = half * (
                abs(axis_x * cosine + axis_y * sine) + abs(-axis_x * sine + axis_y * cosine)
            )
            obstacle_radius = (abs(axis_x) + abs(axis_y)) / 2
            gap = abs(axis_x * (x - obstacle_x) + axis_y * (y - obstacle_y))
            if gap >= core_radius + obstacle_radius:
                separated = True
                break
        if not separated:
            return False
    return True


def _ranked_cells(
    mass: np.ndarray, spans: tuple[tuple[int, int, int], ...], keep: int
) -> tuple[list[tuple[float, int, int]], int]:
    survey = max(keep * 4, keep)
    ranked: list[tuple[float, int, int]] = []
    for i, j0, j1 in spans:
        column = mass[i, j0 : j1 + 1]
        count = min(survey, column.size)
        if count == column.size:
            offsets = np.argsort(column)
        else:
            offsets = np.argpartition(column, count - 1)[:count]
        ranked.extend((float(column[offset]), i, j0 + int(offset)) for offset in offsets)
    ranked.sort()
    return ranked, survey


def _placement_cells_exact_geometry(
    points: tuple[Point, ...],
    weights: np.ndarray,
    direction: Direction,
    *,
    outer_side: Fraction,
    square_side: Fraction,
    pieces: tuple[Polygon, ...],
    residual: bool,
    keep: int,
    max_event_cells: int,
) -> tuple[list[tuple[float, float, float, np.ndarray]], int]:
    projected, u_events, v_events, mass = _exact_geometry_mass_grid(
        points, weights, direction, square_side, pieces
    )
    dense_cells = int(mass.size)
    if dense_cells > max_event_cells:
        raise ValueError(
            f"exact fallback for direction {direction.label} needs {dense_cells:,} dense "
            f"event cells, above guard {max_event_cells:,}"
        )
    spans = reachable_spans(u_events, v_events, pieces)
    if not spans:
        raise ValueError("the exact selected centre domain reaches no event cell")
    ranked, survey = _ranked_cells(mass, spans, keep)
    found: list[tuple[float, float, float, np.ndarray]] = []
    half = square_side / 2
    for event_mass, i, j in ranked[: max(survey, keep)]:
        centre = _exact_witness_for_cell(
            pieces, u_events[i], u_events[i + 1], v_events[j], v_events[j + 1]
        )
        if not _core_is_admissible_exact(
            centre, direction, outer_side, square_side, residual=residual
        ):
            raise ValueError("exact-event witness failed the independent SAT/containment check")
        cu, cv = centre
        covers = np.array(
            [abs(u - cu) <= half and abs(v - cv) <= half for u, v in projected],
            dtype=bool,
        )
        direct_mass = float(weights[covers].sum())
        if abs(direct_mass - event_mass) > 1e-8:
            raise ValueError(
                f"exact-event mass {event_mass} disagrees with witness mass {direct_mass}"
            )
        found.append((direct_mass, float(cu), float(cv), covers))
        if len(found) >= keep:
            break
    if not found:
        raise ValueError("the exact event fallback found no witness for the least cells")
    return found, dense_cells


def _core_is_admissible_float(
    centre_uv: tuple[float, float],
    direction: Direction,
    outer_side: float,
    square_side: float,
    *,
    residual: bool,
) -> bool:
    """Independent full separating-axis check for a proposed float witness."""

    cosine, sine = float(direction.ux), float(direction.uy)
    u, v = centre_uv
    x, y = cosine * u - sine * v, sine * u + cosine * v
    extent = square_side * (cosine + sine) / 2
    slack = 2e-10
    if not (extent - slack <= x <= outer_side - extent + slack):
        return False
    if not (extent - slack <= y <= outer_side - extent + slack):
        return False
    if not residual:
        return True
    core_half = square_side / 2
    corners = (
        (0.5, 0.5),
        (outer_side - 0.5, 0.5),
        (0.5, outer_side - 0.5),
        (outer_side - 0.5, outer_side - 0.5),
    )
    axes = ((1.0, 0.0), (0.0, 1.0), (cosine, sine), (-sine, cosine))
    for obstacle_x, obstacle_y in corners:
        overlap_on_every_axis = True
        for axis_x, axis_y in axes:
            core_radius = core_half * (
                abs(axis_x * cosine + axis_y * sine) + abs(-axis_x * sine + axis_y * cosine)
            )
            obstacle_radius = 0.5 * (abs(axis_x) + abs(axis_y))
            projected_gap = abs(axis_x * (x - obstacle_x) + axis_y * (y - obstacle_y))
            if projected_gap + slack >= core_radius + obstacle_radius:
                overlap_on_every_axis = False
                break
        if overlap_on_every_axis:
            return False
    return True


def placement_cells_on_pieces(
    points: np.ndarray,
    weights: np.ndarray,
    direction: Direction,
    outer_side: Fraction,
    square_side: Fraction,
    *,
    residual: bool,
    keep: int,
    max_event_cells: int,
    exact_points: tuple[Point, ...] | None = None,
) -> tuple[list[tuple[float, float, float, np.ndarray]], int]:
    """Least cells for one domain, plus the dense grid size allocated.

    ``exact_points`` preserves the rational provenance of ``points``.  It is used only
    when binary64 clipping cannot represent a ranked cell's interior witness.
    """

    exact_pieces = (
        residual_domain_pieces(outer_side, square_side, direction)
        if residual
        else unrestricted_domain_pieces(outer_side, square_side, direction)
    )
    pieces = _float_pieces(exact_pieces)
    u, v, u_events, v_events, mass = _dense_mass_grid(
        points, weights, direction, float(square_side), pieces
    )
    dense_cells = int(mass.size)
    if dense_cells > max_event_cells:
        raise ValueError(
            f"direction {direction.label} needs {dense_cells:,} dense event cells, "
            f"above guard {max_event_cells:,}"
        )
    spans = reachable_spans(tuple(u_events), tuple(v_events), pieces)
    if not spans:
        raise ValueError("the selected centre domain reaches no event cell")
    ranked, survey = _ranked_cells(mass, spans, keep)
    found: list[tuple[float, float, float, np.ndarray]] = []
    half = float(square_side) / 2
    for event_mass, i, j in ranked[: max(survey, keep)]:
        try:
            cu, cv = _witness_for_cell(
                pieces,
                float(u_events[i]),
                float(u_events[i + 1]),
                float(v_events[j]),
                float(v_events[j + 1]),
            )
        except ValueError:
            if exact_points is None:
                raise
            provenance = np.array([[float(x), float(y)] for x, y in exact_points])
            if points.shape != provenance.shape or not np.array_equal(points, provenance):
                message = "exact site provenance does not reproduce the float support"
                raise ValueError(message) from None
            return _placement_cells_exact_geometry(
                exact_points,
                weights,
                direction,
                outer_side=outer_side,
                square_side=square_side,
                pieces=exact_pieces,
                residual=residual,
                keep=keep,
                max_event_cells=max_event_cells,
            )
        if not _core_is_admissible_float(
            (cu, cv), direction, float(outer_side), float(square_side), residual=residual
        ):
            raise ValueError("piece witness failed the independent SAT/containment check")
        covers = (np.abs(u - cu) <= half) & (np.abs(v - cv) <= half)
        direct_mass = float(weights[covers].sum())
        if abs(direct_mass - event_mass) > 1e-8:
            raise ValueError(
                f"event-cell mass {event_mass} disagrees with witness mass {direct_mass}"
            )
        found.append((direct_mass, cu, cv, covers))
        if len(found) >= keep:
            break
    if not found:
        raise ValueError("no representable witness was found for the least cells")
    return found, dense_cells


def solve_program(  # noqa: PLR0911 -- each stop preserves a distinct partial receipt
    sites: SiteSet,
    square_side: Fraction,
    directions: tuple[Direction, ...],
    *,
    residual: bool,
    max_rounds: int,
    rows_per_direction: int,
    deadline_seconds: float,
    max_event_cells: int,
) -> ProgramSolution:
    """Float row generation on one fixed support with a per-arm wall deadline."""

    started = time.perf_counter()
    deadline = started + deadline_seconds
    points, sizes, membership = sites.points(), sites.sizes(), sites.membership()
    weights = np.zeros(len(sites.orbits))
    rows: list[np.ndarray] = []
    held: set[bytes] = set()
    objective: float | None = None
    least_covered: float | None = None
    round_records: list[RoundRecord] = []

    def stopped(reason: str) -> ProgramSolution:
        return ProgramSolution(
            weights=weights,
            stopped=reason,
            objective=objective,
            least_covered=least_covered,
            rows=len(rows),
            rounds=round_records,
            seconds=time.perf_counter() - started,
        )

    for round_index in range(max_rounds):
        if time.perf_counter() >= deadline:
            return stopped(f"deadline {deadline_seconds:g}s reached before round {round_index}")
        round_started = time.perf_counter()
        site_weights = weights[membership]
        violated = added = dense_cells = 0
        least = float("inf")
        for direction in directions:
            if time.perf_counter() >= deadline:
                least_covered = None if not math.isfinite(least) else least
                return stopped(
                    f"deadline {deadline_seconds:g}s reached during round "
                    f"{round_index} separation"
                )
            try:
                placements, cells = placement_cells_on_pieces(
                    points,
                    site_weights,
                    direction,
                    sites.outer_side,
                    square_side,
                    residual=residual,
                    keep=rows_per_direction,
                    max_event_cells=max_event_cells,
                    exact_points=sites.positions(),
                )
            except (MemoryError, ValueError) as error:
                least_covered = None if not math.isfinite(least) else least
                return stopped(
                    f"separation unresolved at direction {direction.label}: "
                    f"{type(error).__name__}: {error}"
                )
            dense_cells += cells
            least = min(least, placements[0][0])
            for mass, _, _, covers in placements:
                if mass >= 1 - 1e-9:
                    break
                row = np.zeros(len(sites.orbits))
                np.add.at(row, membership[covers], 1.0)
                if not row.any():
                    return stopped("a placement covers no candidate site")
                violated += 1
                key = row.tobytes()
                if key not in held:
                    held.add(key)
                    rows.append(row)
                    added += 1
        if time.perf_counter() >= deadline:
            least_covered = least
            return stopped(
                f"deadline {deadline_seconds:g}s reached after round {round_index} separation"
            )
        least_covered = least
        elapsed = time.perf_counter() - round_started
        if violated == 0 or (added == 0 and 1 - least <= LP_FEASIBILITY):
            objective = float(sizes @ weights)
            round_records.append(
                RoundRecord(
                    round_index,
                    len(rows),
                    added,
                    violated,
                    objective,
                    least,
                    dense_cells,
                    elapsed,
                )
            )
            return stopped("converged: every surveyed placement covers mass 1")
        if added == 0:
            return stopped(f"a held row is violated by {1 - least:.3e}")
        remaining = deadline - time.perf_counter()
        if remaining <= 0:
            return stopped(f"deadline {deadline_seconds:g}s reached before LP solve")
        result = linprog(
            c=sizes,
            A_ub=-np.vstack(rows),
            b_ub=-np.ones(len(rows)),
            bounds=[(0.0, None)] * len(sites.orbits),
            method="highs",
            options={"time_limit": remaining},
        )
        if not result.success:
            if result.status == 1 or time.perf_counter() >= deadline:
                return stopped(f"deadline {deadline_seconds:g}s reached during LP solve")
            return stopped(f"linear program refused: {result.message}")
        weights = np.asarray(result.x, dtype=float)
        objective = float(result.fun)
        round_records.append(
            RoundRecord(
                round_index,
                len(rows),
                added,
                violated,
                objective,
                least,
                dense_cells,
                time.perf_counter() - round_started,
            )
        )
    return stopped(f"round limit {max_rounds} reached")


def estimate_complexity(
    sites: SiteSet,
    square_side: Fraction,
    directions: tuple[Direction, ...],
    *,
    residual: bool,
) -> Complexity:
    points = sites.points()
    weights = np.ones(points.shape[0])
    estimates: list[int] = []
    for direction in directions:
        exact = (
            residual_domain_pieces(sites.outer_side, square_side, direction)
            if residual
            else unrestricted_domain_pieces(sites.outer_side, square_side, direction)
        )
        pieces = _float_pieces(exact)
        _, _, _, u_events, v_events = _event_arrays(
            points, weights, direction, float(square_side), pieces, all_points=True
        )
        estimates.append((len(u_events) - 1) * (len(v_events) - 1))
    return Complexity(tuple(estimates))


def exact_minimum_covered_mass(
    atoms: tuple[Atom, ...],
    direction: Direction,
    outer_side: Fraction,
    square_side: Fraction,
    *,
    residual: bool,
) -> tuple[Fraction, int]:
    """Exact rational minimum and reachable-cell count for one direction.

    This reader does not call the float generator or the production sweep reduction.
    It adds every component vertex to the event grid and unions each component's
    per-slab spans without filling gaps.
    """

    require_nonnegative_atom_weights(atoms)
    pieces = (
        residual_domain_pieces(outer_side, square_side, direction)
        if residual
        else unrestricted_domain_pieces(outer_side, square_side, direction)
    )
    half = square_side / 2
    projected = tuple(
        (
            direction.ux * atom.x + direction.uy * atom.y,
            direction.vx * atom.x + direction.vy * atom.y,
            atom.weight,
        )
        for atom in atoms
    )
    u_events = tuple(
        sorted(
            {u + offset for u, _, _ in projected for offset in (-half, half)}
            | {u for polygon in pieces for u, _ in polygon}
        )
    )
    v_events = tuple(
        sorted(
            {v + offset for _, v, _ in projected for offset in (-half, half)}
            | {v for polygon in pieces for _, v in polygon}
        )
    )
    scale = lcm(*(atom.weight.denominator for atom in atoms)) if atoms else 1
    scaled = [int(atom.weight * scale) for atom in atoms]
    if sum(scaled) >= 2**60:
        raise ValueError("scaled total mass exceeds the exact pilot grid limit")
    grid = np.zeros((len(u_events), len(v_events)), dtype=np.int64)
    u_index = {value: index for index, value in enumerate(u_events)}
    v_index = {value: index for index, value in enumerate(v_events)}
    for (u, v, _), weight in zip(projected, scaled, strict=True):
        left, right = u_index[u - half], u_index[u + half]
        bottom, top = v_index[v - half], v_index[v + half]
        grid[left, bottom] += weight
        grid[right, bottom] -= weight
        grid[left, top] -= weight
        grid[right, top] += weight
    np.cumsum(grid, axis=1, out=grid)
    np.cumsum(grid, axis=0, out=grid)
    spans = reachable_spans(u_events, v_events, pieces)
    if not spans:
        raise ValueError("the exact residual domain reaches no event cell")
    best: int | None = None
    cells = 0
    for i, j0, j1 in spans:
        column = grid[i, j0 : j1 + 1]
        score = int(column.min())
        best = score if best is None else min(best, score)
        cells += j1 - j0 + 1
    if best is None:
        raise ValueError("the exact residual sweep found no score")
    return Fraction(best, scale), cells


def _load_support(path: Path, outer_side: Fraction) -> tuple[SiteSet, str]:
    data = path.read_bytes()
    record = json.loads(data)
    if not isinstance(record, dict) or Fraction(record.get("outer_side", "")) != outer_side:
        raise ValueError("support certificate outer_side must equal the requested side")
    raw_atoms = record.get("atoms")
    if not isinstance(raw_atoms, list):
        raise TypeError("support certificate has no atom list")
    points: set[Point] = set()
    for entry in raw_atoms:
        if not isinstance(entry, list) or len(entry) < 2:
            raise ValueError("support atom must begin with exact x and y strings")
        points.add((Fraction(entry[0]), Fraction(entry[1])))
    sites = site_set_from_points(outer_side, points)
    if set(sites.positions()) != points:
        raise ValueError("support certificate is not closed under D4 at this side")
    return sites, hashlib.sha256(data).hexdigest()


def _support_record(sites: SiteSet, *, source: str, digest: str) -> dict[str, object]:
    return {
        "source": source,
        "sha256": digest,
        "orbits": len(sites.orbits),
        "sites": sites.size,
        "coordinates": [[[str(x), str(y)] for x, y in orbit] for orbit in sites.orbits],
    }


def _proposal_record(
    solution: ProgramSolution, sites: SiteSet, *, scale: int
) -> dict[str, object]:
    atoms = rationalise_sites(sites, solution.weights, scale=scale)
    rational_total = sum((atom.weight for atom in atoms), Fraction(0))
    return {
        "search_arithmetic": "floating point; exploratory",
        "stopped": solution.stopped,
        "converged": solution.converged,
        "seconds": solution.seconds,
        "rounds": [
            {
                "index": item.index,
                "rows_held": item.rows_held,
                "rows_added": item.rows_added,
                "violated": item.violated,
                "objective": item.objective,
                "least_covered": item.least_covered,
                "dense_cells": item.dense_cells,
                "seconds": item.seconds,
            }
            for item in solution.rounds
        ],
        "rows": solution.rows,
        "objective": solution.objective,
        "least_covered": solution.least_covered,
        "orbit_weights": [float(weight) for weight in solution.weights],
        "rationalisation_scale": scale,
        "rationalised_total_mass": str(rational_total),
        "rationalised_atoms": [[str(atom.x), str(atom.y), str(atom.weight)] for atom in atoms],
        "exact_validation": None,
    }


def _json(record: dict[str, object]) -> str:
    return json.dumps(record, indent=1, allow_nan=False) + "\n"


def _reserve(path: Path, record: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(_json(record))


def run_pair(
    sites: SiteSet,
    directions: tuple[Direction, ...],
    direction_indices: tuple[int, ...],
    square_side: Fraction,
    *,
    support: dict[str, object],
    output: Path,
    max_rounds: int,
    rows_per_direction: int,
    deadline_seconds: float,
    max_event_cells: int,
    max_round_cells: int,
    scale: int,
) -> dict[str, object]:
    complexities = {
        "unrestricted": estimate_complexity(sites, square_side, directions, residual=False),
        "residual": estimate_complexity(sites, square_side, directions, residual=True),
    }
    for label, complexity in complexities.items():
        if complexity.maximum > max_event_cells:
            raise ValueError(
                f"{label} estimate {complexity.maximum:,} cells in one direction exceeds "
                f"the {max_event_cells:,} guard"
            )
        if complexity.total > max_round_cells:
            raise ValueError(
                f"{label} estimate {complexity.total:,} cells per round exceeds "
                f"the {max_round_cells:,} guard"
            )
    record: dict[str, object] = {
        "schema": "residual-cover-pilot/v1",
        "status": "running",
        "evidence_tier": "finite-direction exploratory paired covering LP",
        "claim_limit": (
            "No packing bound: float proposals require separate exact validation, and a "
            "direction subset does not cover omitted directions."
        ),
        "conditioning": "four axis-aligned unit squares fixed flush in the container corners",
        "residual_domain_components": list(DOMAIN_LABELS),
        "score": "M_global - M_residual - 4",
        "settings": {
            "outer_side": str(sites.outer_side),
            "square_side": str(square_side),
            "direction_indices": list(direction_indices),
            "directions": len(directions),
            "full_181_direction_net": len(direction_indices) == 181
            and direction_indices == tuple(range(181)),
            "max_rounds_per_arm": max_rounds,
            "rows_per_direction": rows_per_direction,
            "deadline_seconds_per_arm": deadline_seconds,
            "max_dense_event_cells_per_direction": max_event_cells,
            "max_dense_event_cells_per_round": max_round_cells,
            "rationalisation_scale": scale,
        },
        "support": support,
        "complexity": {
            label: complexity.as_dict(direction_indices)
            for label, complexity in complexities.items()
        },
        "arms": {},
        "comparison": None,
    }
    _reserve(output, record)
    arms = cast(dict[str, object], record["arms"])
    try:
        for label, residual in (("unrestricted", False), ("residual", True)):
            solution = solve_program(
                sites,
                square_side,
                directions,
                residual=residual,
                max_rounds=max_rounds,
                rows_per_direction=rows_per_direction,
                deadline_seconds=deadline_seconds,
                max_event_cells=max_event_cells,
            )
            arms[label] = _proposal_record(solution, sites, scale=scale)
            write_text_atomic(output, _json(record))
    except Exception as error:
        record["status"] = "error"
        record["error"] = f"{type(error).__name__}: {error}"
        write_text_atomic(output, _json(record))
        raise
    unrestricted = cast(dict[str, object], arms["unrestricted"])
    residual = cast(dict[str, object], arms["residual"])
    both_converged = bool(unrestricted["converged"] and residual["converged"])
    if both_converged:
        global_mass = float(cast(float, unrestricted["objective"]))
        residual_mass = float(cast(float, residual["objective"]))
        record["comparison"] = {
            "arithmetic": "floating point; exploratory",
            "M_global": global_mass,
            "M_residual": residual_mass,
            "M_global_minus_M_residual_minus_4": global_mass - residual_mass - 4,
            "residual_mass_below_7": residual_mass < 7,
        }
    record["status"] = "complete" if both_converged else "partial"
    write_text_atomic(output, _json(record))
    return record


def _indices(text: str, steps: int) -> tuple[int, ...]:
    if text == "all":
        return tuple(range(steps + 1))
    try:
        values = tuple(sorted({int(value) for value in text.split(",")}))
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "direction indices must be comma-separated integers"
        ) from error
    if not values or values[0] < 0 or values[-1] > steps:
        raise argparse.ArgumentTypeError(f"direction indices must lie in 0..{steps}")
    return values


def _counts(text: str) -> tuple[int, ...]:
    try:
        values = tuple(int(value) for value in text.split(","))
    except ValueError as error:
        raise ValueError("grid-counts must be comma-separated integers") from error
    if not values or min(values) < 2:
        raise ValueError("every grid count must be at least 2")
    return values


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", type=Fraction, required=True)
    parser.add_argument("--shrink", type=Fraction, required=True)
    support = parser.add_mutually_exclusive_group(required=True)
    support.add_argument("--support-certificate", type=Path)
    support.add_argument("--grid-counts", help="comma-separated explicit grid counts")
    parser.add_argument("--inset", type=Fraction, default=Fraction(1, 2))
    parser.add_argument("--angle-limit", type=Fraction, default=ANGLE_LIMIT)
    parser.add_argument("--direction-steps", type=int, default=180)
    parser.add_argument(
        "--direction-indices",
        required=True,
        help="comma-separated retained-net indices, or 'all'",
    )
    parser.add_argument("--max-rounds", type=int, default=60)
    parser.add_argument("--rows-per-direction", type=int, default=3)
    parser.add_argument("--deadline-seconds", type=float, required=True)
    parser.add_argument("--max-event-cells", type=int, default=8_000_000)
    parser.add_argument("--max-round-cells", type=int, default=1_000_000_000)
    parser.add_argument("--scale", type=int, default=DEFAULT_SCALE)
    parser.add_argument("--estimate-only", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if args.side <= 0 or args.shrink <= 0:
        parser.error("side and shrink must be positive")
    if args.direction_steps < 1:
        parser.error("direction-steps must be positive")
    if (
        min(
            args.max_rounds,
            args.rows_per_direction,
            args.max_event_cells,
            args.max_round_cells,
            args.scale,
        )
        < 1
    ):
        parser.error("round, row, event-cell, and scale limits must be positive")
    if not math.isfinite(args.deadline_seconds) or args.deadline_seconds <= 0:
        parser.error("deadline-seconds must be finite and positive")
    try:
        direction_indices = _indices(args.direction_indices, args.direction_steps)
    except argparse.ArgumentTypeError as error:
        parser.error(str(error))
    full_tangents = net_half_tangents(args.angle_limit, args.direction_steps)
    full_directions = direction_net(full_tangents)
    directions = tuple(full_directions[index] for index in direction_indices)
    try:
        if args.support_certificate is not None:
            sites, digest = _load_support(args.support_certificate, args.side)
            source = str(args.support_certificate)
        else:
            counts = _counts(args.grid_counts)
            sites = site_set_from_grids(args.side, counts, args.inset)
            canonical = json.dumps(
                [[[str(x), str(y)] for x, y in orbit] for orbit in sites.orbits],
                separators=(",", ":"),
            ).encode()
            digest = hashlib.sha256(canonical).hexdigest()
            source = f"grids={counts};inset={args.inset}"
        support_record = _support_record(sites, source=source, digest=digest)
        complexity = {
            label: estimate_complexity(
                sites, args.shrink, directions, residual=residual
            ).as_dict(direction_indices)
            for label, residual in (("unrestricted", False), ("residual", True))
        }
        if args.estimate_only:
            print(
                _json(
                    {
                        "evidence_tier": "complexity estimate only",
                        "support": support_record,
                        "complexity": complexity,
                    }
                ),
                end="",
            )
            return 0
        if args.output is None:
            parser.error("--output is required unless --estimate-only is set")
        record = run_pair(
            sites,
            directions,
            direction_indices,
            args.shrink,
            support=support_record,
            output=args.output,
            max_rounds=args.max_rounds,
            rows_per_direction=args.rows_per_direction,
            deadline_seconds=args.deadline_seconds,
            max_event_cells=args.max_event_cells,
            max_round_cells=args.max_round_cells,
            scale=args.scale,
        )
    except (FileExistsError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(_json(record), end="")
    return 0 if record["status"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
