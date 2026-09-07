"""The fixed BC-254 support screen, separated from source loading and acceptance.

Calling this module does not run anything. The command owner must freeze and authorize
a target run; finite-row values alone never certify almost-everywhere feasible depth.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from sqpack.field import FieldElement
from sqpack.full_size_density.support_ceiling import (
    BoundaryPointError,
    ControlSolution,
    NecessaryRow,
    Point,
    Square,
    SquareKey,
    Support,
    SupportError,
    build_support,
    check_upper,
    necessary_row,
    solve_control_lp,
    square_key,
)
from sqpack.verify import exact_sign, verify_packing

SOURCE_MAPS = 8
MAX_ROWS = 47


@dataclass(frozen=True)
class BoundSupport:
    support: Support
    preimages: tuple[tuple[SquareKey, tuple[tuple[int, int, int], ...]], ...]
    original_counts: tuple[int, ...]
    baseline: tuple[Fraction, ...]


@dataclass(frozen=True)
class RowDisposition:
    phase: str
    source: tuple[int, ...]
    trial: int
    skipped: tuple[int, ...]
    row_index: int | None


@dataclass(frozen=True)
class ScreenResult:
    rows: tuple[NecessaryRow, ...]
    dispositions: tuple[RowDisposition, ...]
    solution: ControlSolution
    solve_pivots: tuple[int, ...]


def bind_source(seeds: Sequence[Square], side: FieldElement) -> BoundSupport:
    """Bind all labelled preimages and certify the uniform average of valid packings."""
    support = build_support(seeds, side)
    if not verify_packing(seeds, side, sign=exact_sign).valid:
        raise SupportError("declared source is not an exact unit-square packing")
    preimages: dict[SquareKey, list[tuple[int, int, int]]] = {}
    for index, seed in enumerate(seeds):
        for reflected in (0, 1):
            current = tuple((side - x if reflected else x, y) for x, y in seed)
            for turn in range(4):
                preimages.setdefault(square_key(current), []).append((index, reflected, turn))
                current = tuple((side - y, x) for x, y in current)
    counts = tuple(
        sum(square_key(seed) in {square_key(square) for square in orbit} for seed in seeds)
        for orbit in support.orbits
    )
    baseline = tuple(
        Fraction(count, size) for count, size in zip(counts, support.sizes, strict=True)
    )
    for orbit, weight in zip(support.orbits, baseline, strict=True):
        if any(
            Fraction(len(preimages[square_key(square)]), SOURCE_MAPS) != weight
            for square in orbit
        ):
            raise SupportError("labelled preimages do not match orbit-average weights")
    if sum(weight * size for weight, size in zip(baseline, support.sizes, strict=True)) != len(
        seeds
    ):
        raise SupportError("uniform averaging lost source mass")
    return BoundSupport(
        support,
        tuple((key, tuple(preimages[key])) for key in sorted(preimages)),
        counts,
        baseline,
    )


def _center(square: Square) -> Point:
    return ((square[0][0] + square[2][0]) / 2, (square[0][1] + square[2][1]) / 2)


def check_fallback_direction(support: Support) -> None:
    """The fixed displacement (1, 2) must cross every supporting line."""
    for orbit in support.orbits:
        for square in orbit:
            for index, (x, y) in enumerate(square):
                nx, ny = square[(index + 1) % 4]
                if (2 * (nx - x) - (ny - y)).is_zero():
                    raise SupportError("fallback direction is parallel to a supporting line")


def initial_rows(
    support: Support,
) -> tuple[tuple[NecessaryRow, ...], tuple[RowDisposition, ...]]:
    rows: list[NecessaryRow] = []
    dispositions: list[RowDisposition] = []
    seen: dict[tuple[int, ...], int] = {}
    direction_checked = False
    trial_stop = 4 + 4 * sum(support.sizes)
    for index, orbit in enumerate(support.orbits):
        center = _center(orbit[0])
        skipped: list[int] = []
        admitted: NecessaryRow | None = None
        selected_trial = 0
        for trial in (0, *range(4, trial_stop + 1)):
            if trial:
                if not direction_checked:
                    check_fallback_direction(support)
                    direction_checked = True
                step = Fraction(1, 2**trial)
                point = (center[0] + step, center[1] + 2 * step)
            else:
                point = center
            try:
                admitted = necessary_row(support, point)
            except BoundaryPointError:
                skipped.append(trial)
                continue
            selected_trial = trial
            break
        if admitted is None:
            raise SupportError("fixed center fallback exhausted its proved finite guard")
        if admitted.coefficients[index] <= 0:
            raise SupportError("initial row does not cover its source orbit")
        if admitted.coefficients not in seen:
            seen[admitted.coefficients] = len(rows)
            rows.append(admitted)
        dispositions.append(
            RowDisposition(
                "initial", (index,), selected_trial, tuple(skipped), seen[admitted.coefficients]
            )
        )
    if any(
        not any(row.coefficients[column] for row in rows)
        for column in range(len(support.orbits))
    ):
        raise SupportError("initial matrix has an uncovered orbit column")
    return tuple(rows), tuple(dispositions)


def extension_points(side: FieldElement) -> tuple[tuple[int, int, int, Point], ...]:
    return tuple(
        (k, i, j, (side * Fraction(i, 2**k), side * Fraction(j, 2**k)))
        for k in range(1, 5)
        for i in range(1, 2 ** (k - 1) + 1)
        for j in range(i, 2 ** (k - 1) + 1)
        if i % 2 or j % 2
    )


def extend_rows(
    support: Support, initial: Sequence[NecessaryRow]
) -> tuple[tuple[NecessaryRow, ...], tuple[RowDisposition, ...]]:
    rows = list(initial)
    seen = {row.coefficients: index for index, row in enumerate(rows)}
    dispositions: list[RowDisposition] = []
    for k, i, j, point in extension_points(support.side):
        try:
            row = necessary_row(support, point)
        except BoundaryPointError:
            dispositions.append(RowDisposition("extension", (k, i, j), 0, (0,), None))
            continue
        if row.coefficients not in seen:
            seen[row.coefficients] = len(rows)
            rows.append(row)
        dispositions.append(
            RowDisposition("extension", (k, i, j), 0, (), seen[row.coefficients])
        )
    if len(rows) > MAX_ROWS:
        raise SupportError("fixed row cap exceeded")
    return tuple(rows), tuple(dispositions)


def primal_value(
    rows: Sequence[NecessaryRow], sizes: Sequence[int], point: Sequence[Fraction]
) -> Fraction:
    if len(point) != len(sizes) or any(value < 0 for value in point):
        raise SupportError("invalid primal weights")
    if any(
        sum(
            value * coefficient
            for value, coefficient in zip(point, row.coefficients, strict=True)
        )
        > 1
        for row in rows
    ):
        raise SupportError("primal weights violate a necessary row")
    return sum((weight * size for weight, size in zip(point, sizes, strict=True)), Fraction())


def solve_screen(
    bound: BoundSupport,
    *,
    threshold: Fraction = Fraction(11),
    stage_check: Callable[[ScreenResult], None] | None = None,
) -> ScreenResult:
    """At most two 64-pivot solves; this routine is not a research acceptance rule."""
    support = bound.support
    rows, dispositions = initial_rows(support)
    primal_value(rows, support.sizes, bound.baseline)
    solution = solve_control_lp(tuple(row.coefficients for row in rows), support.sizes)
    pivots = [solution.pivots]
    if stage_check is not None:
        stage_check(ScreenResult(rows, dispositions, solution, tuple(pivots)))
    if solution.bound > threshold:
        old_length = len(rows)
        rows, extra = extend_rows(support, rows)
        dispositions += extra
        primal_value(rows, support.sizes, bound.baseline)
        try:
            primal_value(rows, support.sizes, solution.point)
        except SupportError:
            solution = solve_control_lp(tuple(row.coefficients for row in rows), support.sizes)
            pivots.append(solution.pivots)
        else:
            multipliers = solution.multipliers + (Fraction(),) * (len(rows) - old_length)
            value = check_upper(
                tuple(row.coefficients for row in rows), support.sizes, multipliers
            )
            if value != solution.bound:
                raise SupportError("extended upper witness changed the optimum")
            solution = ControlSolution(solution.point, multipliers, value, solution.pivots)
    result = ScreenResult(rows, dispositions, solution, tuple(pivots))
    if stage_check is not None and len(dispositions) > len(support.orbits):
        stage_check(result)
    return result


def encode_element(value: FieldElement) -> list[str]:
    return [str(coefficient) for coefficient in value.coeffs]


def support_metadata(bound: BoundSupport) -> dict[str, Any]:
    def key_data(key: SquareKey) -> list[list[list[str]]]:
        return [
            [[str(value) for value in coordinate] for coordinate in corner] for corner in key
        ]

    return {
        "side": encode_element(bound.support.side),
        "orbits": [
            [key_data(square_key(square)) for square in orbit] for orbit in bound.support.orbits
        ],
        "preimages": [
            {"square": key_data(key), "labels": [list(label) for label in labels]}
            for key, labels in bound.preimages
        ],
        "sizes": list(bound.support.sizes),
        "original_counts": list(bound.original_counts),
        "uniform_weights": [str(weight) for weight in bound.baseline],
    }


def make_packet(source: str, bound: BoundSupport, result: ScreenResult) -> dict[str, Any]:
    return {
        "version": 1,
        "source": source,
        "support": support_metadata(bound),
        "rows": [
            {
                "point": [encode_element(value) for value in row.point],
                "radius": str(row.radius),
                "coefficients": list(row.coefficients),
            }
            for row in result.rows
        ],
        "dispositions": [
            {
                "phase": entry.phase,
                "source": list(entry.source),
                "trial": entry.trial,
                "skipped": list(entry.skipped),
                "row_index": entry.row_index,
            }
            for entry in result.dispositions
        ],
        "primal": [str(weight) for weight in result.solution.point],
        "multipliers": [str(weight) for weight in result.solution.multipliers],
        "bound": str(result.solution.bound),
        "solve_pivots": list(result.solve_pivots),
    }
