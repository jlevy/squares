"""Setup-only snap geometry and editor-group behavior."""

from __future__ import annotations

import math

import pytest

from sqpack.motion_lab.snap import (
    EditorSquare,
    EditorState,
    SnapTargetKind,
    apply_best_snap,
    editor_diagnostics,
    pair_gap,
    release_quench_request,
    reset_editor,
    rotate_group,
    set_snapping,
    translate_group,
)

SNAP_THRESHOLD = 0.08


def _state(*squares: EditorSquare, side: float = 4.0) -> EditorState:
    return EditorState.with_singletons(side=side, squares=squares)


def test_near_square_contact_snaps_exactly_and_merges_editor_groups() -> None:
    state = _state(
        EditorSquare(square_id=0, x=0.9, y=1.0, theta=0.0),
        EditorSquare(square_id=1, x=1.95, y=1.0, theta=0.0),
    )

    snapped, result = apply_best_snap(state, moving_square_id=0, threshold=SNAP_THRESHOLD)

    assert result is not None
    assert result.target_kind is SnapTargetKind.SQUARE
    assert result.target_id == "1"
    assert result.distance == pytest.approx(0.05)
    assert pair_gap(snapped.squares[0], snapped.squares[1]) == pytest.approx(0.0)
    assert snapped.groups == ((0, 1),)


def test_wall_ties_are_deterministic_and_do_not_merge_groups() -> None:
    state = _state(EditorSquare(square_id=0, x=0.55, y=0.55, theta=0.0))

    snapped, result = apply_best_snap(state, moving_square_id=0, threshold=SNAP_THRESHOLD)

    assert result is not None
    assert result.target_kind is SnapTargetKind.WALL
    assert result.target_id == "left"
    assert snapped.squares[0].x == pytest.approx(0.5)
    assert snapped.squares[0].y == pytest.approx(0.55)
    assert snapped.groups == ((0,),)


def test_group_translation_rotation_and_release_preserve_only_pose() -> None:
    initial = EditorState(
        side=4.0,
        squares=(
            EditorSquare(square_id=0, x=1.0, y=1.0, theta=0.0),
            EditorSquare(square_id=1, x=2.0, y=1.0, theta=0.0),
            EditorSquare(square_id=2, x=3.0, y=3.0, theta=0.2),
        ),
        groups=((0, 1), (2,)),
    )
    translated = translate_group(initial, square_id=0, dx=0.25, dy=0.5)
    rotated = rotate_group(translated, square_id=1, delta=math.pi / 2)

    assert [(square.x, square.y) for square in translated.squares[:2]] == [
        (1.25, 1.5),
        (2.25, 1.5),
    ]
    assert rotated.squares[0].x == pytest.approx(1.75)
    assert rotated.squares[0].y == pytest.approx(1.0)
    assert rotated.squares[1].x == pytest.approx(1.75)
    assert rotated.squares[1].y == pytest.approx(2.0)

    request = release_quench_request(rotated, max_sweeps=3, time_budget=2.0)
    assert request.x == pytest.approx((1.75, 1.75, 3.0))
    assert request.y == pytest.approx((1.0, 2.0, 3.0))
    assert request.theta == pytest.approx((0.0, 0.0, 0.2))
    assert "groups" not in request.to_record()


def test_snap_candidate_is_rejected_when_it_leaves_an_overlap() -> None:
    state = _state(
        EditorSquare(square_id=0, x=0.9, y=1.0, theta=0.0),
        EditorSquare(square_id=1, x=1.95, y=1.0, theta=0.0),
        EditorSquare(square_id=2, x=0.9, y=1.8, theta=0.0),
    )

    unchanged, result = apply_best_snap(
        state,
        moving_square_id=0,
        threshold=SNAP_THRESHOLD,
    )

    assert result is None
    assert unchanged == state


def test_rotated_square_snaps_using_separating_axis_geometry() -> None:
    half_diagonal = math.sqrt(2) / 2
    stationary_x = 2.5
    state = _state(
        EditorSquare(
            square_id=0,
            x=stationary_x - half_diagonal - 0.55,
            y=2.0,
            theta=math.pi / 4,
        ),
        EditorSquare(square_id=1, x=stationary_x, y=2.0, theta=0.0),
    )

    snapped, result = apply_best_snap(state, moving_square_id=0, threshold=SNAP_THRESHOLD)

    assert result is not None
    assert result.distance == pytest.approx(0.05)
    assert pair_gap(snapped.squares[0], snapped.squares[1]) == pytest.approx(0.0)


def test_near_vertex_contact_uses_one_deterministic_diagonal_translation() -> None:
    state = _state(
        EditorSquare(square_id=0, x=0.95, y=0.95, theta=0.0),
        EditorSquare(square_id=1, x=2.0, y=2.0, theta=0.0),
    )

    snapped, result = apply_best_snap(state, moving_square_id=0, threshold=SNAP_THRESHOLD)

    assert result is not None
    assert result.distance == pytest.approx(math.sqrt(0.05**2 + 0.05**2))
    assert result.dx == pytest.approx(0.05)
    assert result.dy == pytest.approx(0.05)
    assert pair_gap(snapped.squares[0], snapped.squares[1]) == pytest.approx(0.0)


def test_toggle_diagnostics_and_reset_keep_invalid_editor_input_visible() -> None:
    baseline = _state(
        EditorSquare(square_id=0, x=0.6, y=1.0, theta=0.0),
        EditorSquare(square_id=1, x=1.6, y=1.0, theta=0.0),
    )
    edited = translate_group(baseline, square_id=1, dx=-0.4, dy=0.0)
    edited = translate_group(edited, square_id=0, dx=-0.2, dy=0.0)
    diagnostics = editor_diagnostics(edited)

    assert diagnostics.overlap_pairs == ((0, 1),)
    assert diagnostics.outside_square_ids == (0,)

    disabled = set_snapping(edited, enabled=False)
    unchanged, result = apply_best_snap(
        disabled,
        moving_square_id=0,
        threshold=SNAP_THRESHOLD,
    )
    assert result is None
    assert unchanged == disabled
    assert reset_editor(disabled, baseline) == baseline
