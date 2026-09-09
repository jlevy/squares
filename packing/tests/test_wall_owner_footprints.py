"""Target-blind exact controls for wall-aware owner-footprint construction."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Literal

import pytest

import devtools.wall_owner_footprints as wall
from devtools.owner_footprints import (
    OwnerClass,
    Polygon,
    convex_polygon_intersection,
    full_owner_direction_manifest,
    owner_branch_manifest,
    polygon_area_twice,
    signed_axis_rays,
)
from devtools.wall_owner_footprints import (
    OwnerFrameFootprint,
    RetainedOwnerFrame,
    WallFootprintDeadlineError,
    WallFootprintError,
    centre_set_dimension,
    closed_centre_set,
    combine_frame_footprints,
    literal_support_interval,
    physical_container_centres,
    retained_owner_frames,
    support_rectangle,
    validate_output_path,
    validate_owner_manifest,
)

F = Fraction


def _rectangle(x0: Fraction, y0: Fraction, x1: Fraction, y1: Fraction) -> Polygon:
    return ((x0, y0), (x1, y0), (x1, y1), (x0, y1))


def test_closed_intersection_preserves_polygon_segment_point_and_empty() -> None:
    container = _rectangle(F(0), F(0), F(1), F(1))
    fixtures = (
        (container, container, 2),
        (
            _rectangle(F(1), F(0), F(2), F(1)),
            ((F(1), F(0)), (F(1), F(1))),
            1,
        ),
        (_rectangle(F(1), F(1), F(2), F(2)), ((F(1), F(1)),), 0),
        (_rectangle(F(2), F(0), F(3), F(1)), (), -1),
    )
    for clipping, expected, dimension in fixtures:
        result = convex_polygon_intersection(container, clipping)
        assert result == expected
        assert centre_set_dimension(result) == dimension


def test_physical_wrapper_retains_a_whole_face_cut() -> None:
    ray = (F(1), F(0))
    assert physical_container_centres(ray, outer_side=F(4), half=F(1)) == _rectangle(
        F(1), F(1), F(3), F(3)
    )
    centres = closed_centre_set((F(1, 2), F(1)), ray, outer_side=F(4), half=F(1))
    assert centres == _rectangle(F(1), F(1), F(3, 2), F(2))
    rectangle, support_r, support_jr = support_rectangle(centres, ray, half=F(1))
    assert support_r == (F(1, 2), F(2))
    assert support_jr == (F(1), F(2))
    assert rectangle == _rectangle(F(1, 2), F(1), F(2), F(2))


def test_physical_wrapper_preserves_point_and_segment_centre_sets() -> None:
    ray = (F(1), F(0))
    point = closed_centre_set((F(0), F(0)), ray, outer_side=F(4), half=F(1))
    segment = closed_centre_set((F(0), F(1)), ray, outer_side=F(4), half=F(1))
    assert point == ((F(1), F(1)),)
    assert centre_set_dimension(point) == 0
    assert segment == ((F(1), F(1)), (F(1), F(2)))
    assert centre_set_dimension(segment) == 1


def test_point_and_segment_use_literal_oblique_support_extrema() -> None:
    ray = (F(3, 5), F(4, 5))
    point = ((F(1), F(2)),)
    rectangle, support_r, support_jr = support_rectangle(point, ray, half=F(1))
    assert support_r == (F(6, 5), F(16, 5))
    assert support_jr == (F(-3, 5), F(7, 5))
    assert polygon_area_twice(rectangle) == F(8)

    segment = ((F(0), F(0)), ray)
    rectangle, support_r, support_jr = support_rectangle(segment, ray, half=F(1))
    assert support_r == (F(0), F(1))
    assert support_jr == (F(-1), F(1))
    assert polygon_area_twice(rectangle) == F(4)
    assert literal_support_interval(segment, ray, half=F(1)) == (F(0), F(1))


def test_corner_only_cut_can_leave_both_support_extrema_unchanged() -> None:
    ray = (F(3, 5), F(4, 5))
    mark = (F(1), F(1))
    displacement = (
        mark,
        (F(8, 5), F(9, 5)),
        (F(4, 5), F(12, 5)),
        (F(1, 5), F(8, 5)),
    )
    centres = convex_polygon_intersection(displacement, _rectangle(F(0), F(0), F(2), F(2)))
    assert set(centres) == {
        mark,
        (F(8, 5), F(9, 5)),
        (F(4, 3), F(2)),
        (F(1, 2), F(2)),
        (F(1, 5), F(8, 5)),
    }
    rectangle, support_r, support_jr = support_rectangle(centres, ray, half=F(1))
    assert support_r == (F(7, 5), F(12, 5))
    assert support_jr == (F(-1, 5), F(4, 5))
    assert set(rectangle) == set(displacement)


def _owner() -> OwnerClass:
    return OwnerClass(
        class_id="synthetic:m:j0",
        mark_id="m",
        mark=(F(0), F(0)),
        sector=0,
        reflected_class_id="synthetic",
        representative=True,
    )


def _frame(
    centre_set: Polygon,
    rectangle: Polygon | None,
    dimension: Literal[-1, 0, 1, 2],
    disposition: Literal["allowed", "empty"],
) -> OwnerFrameFootprint:
    retained = RetainedOwnerFrame((F(1), F(0)), 0, 0, ())
    if rectangle is None:
        return OwnerFrameFootprint(retained, centre_set, -1, None, None, None, "empty")
    return OwnerFrameFootprint(
        retained,
        centre_set,
        dimension,
        (F(0), F(1)),
        (F(0), F(1)),
        rectangle,
        disposition,
    )


def test_class_completion_keeps_degenerate_frames_and_distinguishes_impossible() -> None:
    old = _rectangle(F(0), F(0), F(1), F(1))
    empty = _frame((), None, -1, "empty")
    point = _frame(((F(0), F(0)),), _rectangle(F(0), F(0), F(2), F(1)), 0, "allowed")
    segment = _frame(
        ((F(0), F(0)), (F(1), F(0))),
        _rectangle(F(0), F(0), F(1), F(2)),
        1,
        "allowed",
    )
    possible = combine_frame_footprints(_owner(), (empty, point, segment), old)
    assert possible.disposition == "possible"
    assert possible.polygon == old
    assert possible.proper_inclusion is False
    assert [item.centre_dimension for item in possible.frames] == [-1, 0, 1]

    impossible = combine_frame_footprints(_owner(), (empty,), old)
    assert impossible.disposition == "impossible"
    assert impossible.polygon is None
    assert impossible.proper_inclusion is None


def test_class_completion_requires_exact_nesting_and_positive_area() -> None:
    old = _rectangle(F(0), F(0), F(1), F(1))
    too_small = _frame(((F(0), F(0)),), _rectangle(F(0), F(0), F(1, 2), F(1, 2)), 0, "allowed")
    with pytest.raises(WallFootprintError, match="nesting"):
        combine_frame_footprints(_owner(), (too_small,), old)
    with pytest.raises(WallFootprintError, match="empty retained-frame"):
        combine_frame_footprints(_owner(), (), old)


def test_frozen_manifests_and_full_signed_frame_provenance_are_exact() -> None:
    manifest = full_owner_direction_manifest()
    branch = owner_branch_manifest(manifest)
    validate_owner_manifest(manifest, branch)
    all_rays = set(signed_axis_rays(manifest.directions))
    assert len(all_rays) == 1444
    by_index = {item.index: item for item in manifest.orientations}
    selected_union = set()
    for owner_class in branch.classes:
        frames = retained_owner_frames(owner_class, manifest)
        assert frames
        assert len({frame.ray for frame in frames}) == len(frames)
        selected_union.update(frame.ray for frame in frames)
        for frame in frames:
            assert frame.orientation_index in by_index
            assert frame.sources == by_index[frame.orientation_index].sources
            assert len((frame.orientation_index,)) == 1
    assert selected_union == all_rays

    first = retained_owner_frames(branch.classes[1], manifest)
    adjacent = retained_owner_frames(branch.classes[2], manifest)
    assert len({frame.ray for frame in first} & {frame.ray for frame in adjacent}) == 1


def test_diagonal_reflection_uses_s_of_jr_and_resolves_target_provenance() -> None:
    manifest = full_owner_direction_manifest()
    branch = owner_branch_manifest(manifest)
    source = branch.classes[0]
    target = next(item for item in branch.classes if item.class_id == source.reflected_class_id)
    source_frames = retained_owner_frames(source, manifest)
    target_by_ray = {frame.ray: frame for frame in retained_owner_frames(target, manifest)}
    by_index = {item.index: item for item in manifest.orientations}
    for frame in source_frames:
        ray = frame.ray
        reflected = (ray[0], -ray[1])  # S(Jr), not S(r)
        resolved = target_by_ray[reflected]
        assert resolved.sources == by_index[resolved.orientation_index].sources


def test_manifest_mutations_are_invalid() -> None:
    manifest = full_owner_direction_manifest()
    branch = owner_branch_manifest(manifest)
    with pytest.raises(WallFootprintError, match="frozen generator"):
        validate_owner_manifest(
            replace(manifest, orientations=manifest.orientations[:-1]), branch
        )
    wrong_class = replace(branch.classes[0], mark=(F(0), F(0)))
    with pytest.raises(WallFootprintError, match="frozen branch"):
        validate_owner_manifest(
            manifest, replace(branch, classes=(wrong_class, *branch.classes[1:]))
        )


def test_all_class_driver_preserves_partial_prefix_without_evaluating_geometry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = full_owner_direction_manifest()
    branch = owner_branch_manifest(manifest)
    calls = 0

    def controlled(*_args: object, **_kwargs: object) -> wall.WallOwnerFootprint:
        nonlocal calls
        calls += 1
        raise WallFootprintDeadlineError("synthetic deadline")

    monkeypatch.setattr(wall, "wall_owner_footprint", controlled)
    result = wall.build_wall_owner_manifest(
        source_revision="synthetic",
        deadline_seconds=10,
        directions=manifest,
        branch=branch,
    )
    assert calls == 1
    assert result.status == "partial"
    assert result.classes == ()
    assert result.expected_classes == 16


def test_output_guard_requires_fresh_json_outside_code(tmp_path: Path) -> None:
    assert validate_output_path(tmp_path / "fresh.json", tmp_path) == tmp_path / "fresh.json"
    existing = tmp_path / "existing.json"
    existing.write_text("{}\n", encoding="utf-8")
    with pytest.raises(WallFootprintError, match="fresh JSON"):
        validate_output_path(existing, tmp_path)
    code = tmp_path / "packing" / "devtools" / "receipt.json"
    with pytest.raises(WallFootprintError, match="project code"):
        validate_output_path(code, tmp_path)
