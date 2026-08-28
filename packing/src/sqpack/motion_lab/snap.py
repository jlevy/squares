"""Pure setup-only snapping and temporary editor-group transforms.

These operations never add constraints to the numerical optimizer. The editor may
merge touching squares into a temporary group for convenient placement; conversion to
`QuenchRequest` keeps only the container side and square poses.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from enum import StrEnum

from sqpack.motion_lab.contracts import QuenchRequest, SolverKind

GEOMETRY_EPSILON = 1e-10
QUARTER_TURN_RADIANS = math.pi / 2
PAIR_AXIS_COUNT = 4
SQUARE_CORNER_COUNT = 4
_WALL_NAMES = ("left", "right", "bottom", "top")


class SnapTargetKind(StrEnum):
    """Kinds of editor geometry that can receive a setup snap."""

    SQUARE = "square"
    WALL = "wall"


@dataclass(frozen=True)
class EditorSquare:
    """One editable unit-square pose."""

    square_id: int
    x: float
    y: float
    theta: float

    def __post_init__(self) -> None:
        if (
            isinstance(self.square_id, bool)
            or not isinstance(self.square_id, int)
            or self.square_id < 0
        ):
            raise ValueError("editor square ID must be a non-negative integer")
        if not all(math.isfinite(value) for value in (self.x, self.y, self.theta)):
            raise ValueError("editor square pose must be finite")


@dataclass(frozen=True)
class EditorState:
    """Editor pose plus a stable partition of square IDs into temporary groups."""

    side: float
    squares: tuple[EditorSquare, ...]
    groups: tuple[tuple[int, ...], ...]
    snapping_enabled: bool = True

    def __post_init__(self) -> None:
        if not math.isfinite(self.side) or self.side <= 0:
            raise ValueError("editor container side must be finite and positive")
        if not isinstance(self.snapping_enabled, bool):
            raise TypeError("snapping toggle must be boolean")
        if not self.squares:
            raise ValueError("editor state must contain squares")
        square_ids = tuple(square.square_id for square in self.squares)
        if square_ids != tuple(sorted(set(square_ids))):
            raise ValueError("editor squares must have unique, stable IDs")
        if any(
            not group
            or any(
                isinstance(square_id, bool) or not isinstance(square_id, int)
                for square_id in group
            )
            or group != tuple(sorted(set(group)))
            for group in self.groups
        ):
            raise ValueError("editor groups must contain unique, stable IDs")
        if self.groups != tuple(sorted(self.groups, key=lambda group: group[0])):
            raise ValueError("editor groups must use stable order")
        grouped_ids = tuple(sorted(square_id for group in self.groups for square_id in group))
        if grouped_ids != square_ids:
            raise ValueError("editor groups must partition the square IDs")

    @classmethod
    def with_singletons(
        cls,
        *,
        side: float,
        squares: tuple[EditorSquare, ...],
        snapping_enabled: bool = True,
    ) -> EditorState:
        """Create an editor state in which no squares are initially grouped."""
        return cls(
            side=side,
            squares=squares,
            groups=tuple((square.square_id,) for square in squares),
            snapping_enabled=snapping_enabled,
        )


@dataclass(frozen=True)
class SnapResult:
    """The deterministic translation and group effect of one accepted snap."""

    dx: float
    dy: float
    distance: float
    target_kind: SnapTargetKind
    target_id: str
    moving_group: tuple[int, ...]
    stationary_group: tuple[int, ...] = ()


@dataclass(frozen=True)
class EditorDiagnostics:
    """Overlap and containment marks shown beside an editable pose."""

    overlap_pairs: tuple[tuple[int, int], ...]
    outside_square_ids: tuple[int, ...]


@dataclass(frozen=True)
class _SnapCandidate:
    result: SnapResult
    rank: tuple[float, int, int, int, int]


def _square_map(state: EditorState) -> dict[int, EditorSquare]:
    return {square.square_id: square for square in state.squares}


def _group_for(state: EditorState, square_id: int) -> tuple[int, ...]:
    for group in state.groups:
        if square_id in group:
            return group
    raise ValueError(f"unknown editor square ID: {square_id}")


def _axes(square: EditorSquare) -> tuple[tuple[float, float], ...]:
    cosine = math.cos(square.theta)
    sine = math.sin(square.theta)
    return ((cosine, sine), (-sine, cosine))


def _half_extent(square: EditorSquare, axis: tuple[float, float]) -> float:
    axis_x, axis_y = axis
    cosine = math.cos(square.theta)
    sine = math.sin(square.theta)
    return 0.5 * (abs(axis_x * cosine + axis_y * sine) + abs(-axis_x * sine + axis_y * cosine))


def _corners(square: EditorSquare) -> tuple[tuple[float, float], ...]:
    cosine = math.cos(square.theta)
    sine = math.sin(square.theta)
    return tuple(
        (
            square.x + 0.5 * (sign_x * cosine - sign_y * sine),
            square.y + 0.5 * (sign_x * sine + sign_y * cosine),
        )
        for sign_x, sign_y in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    )


def pair_gap(first: EditorSquare, second: EditorSquare) -> float:
    """Return the greatest SAT separation; negative means an overlap."""
    delta_x = first.x - second.x
    delta_y = first.y - second.y
    return max(
        abs(delta_x * axis_x + delta_y * axis_y)
        - _half_extent(first, axis)
        - _half_extent(second, axis)
        for axis in _axes(first) + _axes(second)
        for axis_x, axis_y in (axis,)
    )


def translate_group(
    state: EditorState,
    *,
    square_id: int,
    dx: float,
    dy: float,
) -> EditorState:
    """Translate every square in the selected temporary group."""
    if not math.isfinite(dx) or not math.isfinite(dy):
        raise ValueError("editor translation must be finite")
    moving = set(_group_for(state, square_id))
    return replace(
        state,
        squares=tuple(
            replace(square, x=square.x + dx, y=square.y + dy)
            if square.square_id in moving
            else square
            for square in state.squares
        ),
    )


def rotate_group(state: EditorState, *, square_id: int, delta: float) -> EditorState:
    """Rotate a temporary group about the centroid of its square centers."""
    if not math.isfinite(delta):
        raise ValueError("editor rotation must be finite")
    group = _group_for(state, square_id)
    moving = set(group)
    squares = _square_map(state)
    pivot_x = sum(squares[value].x for value in group) / len(group)
    pivot_y = sum(squares[value].y for value in group) / len(group)
    cosine = math.cos(delta)
    sine = math.sin(delta)
    rotated = []
    for square in state.squares:
        if square.square_id not in moving:
            rotated.append(square)
            continue
        offset_x = square.x - pivot_x
        offset_y = square.y - pivot_y
        rotated.append(
            replace(
                square,
                x=pivot_x + cosine * offset_x - sine * offset_y,
                y=pivot_y + sine * offset_x + cosine * offset_y,
                theta=square.theta + delta,
            )
        )
    return replace(state, squares=tuple(rotated))


def set_snapping(state: EditorState, *, enabled: bool) -> EditorState:
    """Enable or disable sticky placement without changing the current groups."""
    if not isinstance(enabled, bool):
        raise TypeError("snapping toggle must be boolean")
    return replace(state, snapping_enabled=enabled)


def reset_editor(state: EditorState, baseline: EditorState) -> EditorState:
    """Restore the last declared baseline pose and its temporary groups."""
    current_ids = tuple(square.square_id for square in state.squares)
    baseline_ids = tuple(square.square_id for square in baseline.squares)
    if current_ids != baseline_ids:
        raise ValueError("editor reset baseline must contain the same square IDs")
    return baseline


def _translated_squares(
    state: EditorState,
    moving_group: tuple[int, ...],
    dx: float,
    dy: float,
) -> tuple[EditorSquare, ...]:
    moving = set(moving_group)
    return tuple(
        replace(square, x=square.x + dx, y=square.y + dy)
        if square.square_id in moving
        else square
        for square in state.squares
    )


def _inside_container(square: EditorSquare, side: float) -> bool:
    horizontal = _half_extent(square, (1.0, 0.0))
    vertical = _half_extent(square, (0.0, 1.0))
    return (
        square.x - horizontal >= -GEOMETRY_EPSILON
        and square.x + horizontal <= side + GEOMETRY_EPSILON
        and square.y - vertical >= -GEOMETRY_EPSILON
        and square.y + vertical <= side + GEOMETRY_EPSILON
    )


def editor_diagnostics(state: EditorState) -> EditorDiagnostics:
    """Classify visible overlaps and out-of-container squares without repairing them."""
    overlap_pairs = tuple(
        (first.square_id, second.square_id)
        for index, first in enumerate(state.squares)
        for second in state.squares[index + 1 :]
        if pair_gap(first, second) < -GEOMETRY_EPSILON
    )
    outside_square_ids = tuple(
        square.square_id
        for square in state.squares
        if not _inside_container(square, state.side)
    )
    return EditorDiagnostics(overlap_pairs, outside_square_ids)


def _valid_candidate(
    state: EditorState,
    moving_group: tuple[int, ...],
    dx: float,
    dy: float,
) -> bool:
    translated = _translated_squares(state, moving_group, dx, dy)
    moving = set(moving_group)
    if any(
        not _inside_container(square, state.side)
        for square in translated
        if square.square_id in moving
    ):
        return False
    return not any(
        pair_gap(first, second) < -GEOMETRY_EPSILON
        for first in translated
        if first.square_id in moving
        for second in translated
        if second.square_id not in moving
    )


def _square_candidates(
    state: EditorState,
    moving_group: tuple[int, ...],
    threshold: float,
) -> list[_SnapCandidate]:
    squares = _square_map(state)
    moving = set(moving_group)
    candidates = []
    for moving_id in moving_group:
        first = squares[moving_id]
        for second in state.squares:
            if second.square_id in moving:
                continue
            stationary_group = _group_for(state, second.square_id)
            delta_x = first.x - second.x
            delta_y = first.y - second.y
            for axis_order, axis in enumerate(_axes(first) + _axes(second)):
                axis_x, axis_y = axis
                projection = delta_x * axis_x + delta_y * axis_y
                sign = 1.0 if projection >= 0 else -1.0
                contact_projection = sign * (
                    _half_extent(first, axis) + _half_extent(second, axis)
                )
                amount = contact_projection - projection
                distance = abs(amount)
                dx = amount * axis_x
                dy = amount * axis_y
                translated_first = replace(first, x=first.x + dx, y=first.y + dy)
                if (
                    distance > threshold
                    or not _valid_candidate(state, moving_group, dx, dy)
                    or abs(pair_gap(translated_first, second)) > GEOMETRY_EPSILON
                ):
                    continue
                result = SnapResult(
                    dx=dx,
                    dy=dy,
                    distance=distance,
                    target_kind=SnapTargetKind.SQUARE,
                    target_id=str(second.square_id),
                    moving_group=moving_group,
                    stationary_group=stationary_group,
                )
                candidates.append(
                    _SnapCandidate(
                        result=result,
                        rank=(
                            distance,
                            second.square_id,
                            moving_id,
                            axis_order,
                            0 if sign < 0 else 1,
                        ),
                    )
                )
            for moving_corner, first_corner in enumerate(_corners(first)):
                for stationary_corner, second_corner in enumerate(_corners(second)):
                    dx = second_corner[0] - first_corner[0]
                    dy = second_corner[1] - first_corner[1]
                    distance = math.hypot(dx, dy)
                    translated_first = replace(first, x=first.x + dx, y=first.y + dy)
                    if (
                        distance > threshold
                        or not _valid_candidate(state, moving_group, dx, dy)
                        or abs(pair_gap(translated_first, second)) > GEOMETRY_EPSILON
                    ):
                        continue
                    result = SnapResult(
                        dx=dx,
                        dy=dy,
                        distance=distance,
                        target_kind=SnapTargetKind.SQUARE,
                        target_id=str(second.square_id),
                        moving_group=moving_group,
                        stationary_group=stationary_group,
                    )
                    candidates.append(
                        _SnapCandidate(
                            result=result,
                            rank=(
                                distance,
                                second.square_id,
                                moving_id,
                                PAIR_AXIS_COUNT
                                + moving_corner * SQUARE_CORNER_COUNT
                                + stationary_corner,
                                0,
                            ),
                        )
                    )
    return candidates


def _wall_candidates(
    state: EditorState,
    moving_group: tuple[int, ...],
    threshold: float,
) -> list[_SnapCandidate]:
    squares = _square_map(state)
    candidates = []
    target_offset = len(state.squares)
    for moving_id in moving_group:
        square = squares[moving_id]
        horizontal = _half_extent(square, (1.0, 0.0))
        vertical = _half_extent(square, (0.0, 1.0))
        translations = (
            (horizontal - square.x, 0.0),
            (state.side - horizontal - square.x, 0.0),
            (0.0, vertical - square.y),
            (0.0, state.side - vertical - square.y),
        )
        for wall_order, ((dx, dy), wall) in enumerate(
            zip(translations, _WALL_NAMES, strict=True)
        ):
            distance = math.hypot(dx, dy)
            if distance > threshold or not _valid_candidate(state, moving_group, dx, dy):
                continue
            result = SnapResult(
                dx=dx,
                dy=dy,
                distance=distance,
                target_kind=SnapTargetKind.WALL,
                target_id=wall,
                moving_group=moving_group,
            )
            candidates.append(
                _SnapCandidate(
                    result=result,
                    rank=(distance, target_offset + wall_order, moving_id, 0, 0),
                )
            )
    return candidates


def _merge_groups(
    state: EditorState,
    first: tuple[int, ...],
    second: tuple[int, ...],
) -> EditorState:
    merged = tuple(sorted((*first, *second)))
    groups = [group for group in state.groups if group not in (first, second)]
    groups.append(merged)
    return replace(state, groups=tuple(sorted(groups, key=lambda group: group[0])))


def apply_best_snap(
    state: EditorState,
    *,
    moving_square_id: int,
    threshold: float,
) -> tuple[EditorState, SnapResult | None]:
    """Apply the stable nearest valid snap after a direct manipulation."""
    if not math.isfinite(threshold) or threshold < 0:
        raise ValueError("snap threshold must be finite and non-negative")
    moving_group = _group_for(state, moving_square_id)
    if not state.snapping_enabled:
        return state, None
    candidates = [
        *_square_candidates(state, moving_group, threshold),
        *_wall_candidates(state, moving_group, threshold),
    ]
    if not candidates:
        return state, None
    candidate = min(candidates, key=lambda value: value.rank)
    result = candidate.result
    snapped = translate_group(
        state,
        square_id=moving_square_id,
        dx=result.dx,
        dy=result.dy,
    )
    if result.target_kind is SnapTargetKind.SQUARE:
        snapped = _merge_groups(snapped, result.moving_group, result.stationary_group)
    return snapped, result


def release_quench_request(
    state: EditorState,
    *,
    max_sweeps: int,
    time_budget: float,
) -> QuenchRequest:
    """Discard editor groups and return the unconstrained Phase 1 payload."""
    return QuenchRequest(
        side=state.side,
        x=tuple(square.x for square in state.squares),
        y=tuple(square.y for square in state.squares),
        theta=tuple(square.theta % QUARTER_TURN_RADIANS for square in state.squares),
        solver=SolverKind.QUENCH_BRACKET,
        max_sweeps=max_sweeps,
        time_budget=time_budget,
    )
