"""Synthetic controls for the unit-parent derived-domain adapter candidate."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from typing import Literal, TypedDict, cast

import pytest

import devtools.wall_owner_parent_compatibility as parent
from devtools.owner_footprints import (
    CORE_SIDE,
    HALF_CORE,
    OUTER_SIDE,
    DirectionSource,
    Point,
    full_owner_direction_manifest,
    owner_branch_manifest,
    point_in_closed_convex_polygon,
)
from devtools.wall_owner_containment import AffineMap
from devtools.wall_owner_escape_compatibility import FrameExtremum
from devtools.wall_owner_footprints import (
    OwnerFrameFootprint,
    RetainedOwnerFrame,
    centre_set_dimension,
    closed_centre_set,
    support_rectangle,
)
from devtools.wall_owner_parent_compatibility import (
    GLOBAL_PARENT_RULE,
    GLOBAL_TANGENT_BOUND,
    ParentCentreRule,
    ParentClassCompatibility,
    angular_extent_lower,
    bound_expected_owner_frames,
    check_residual_parent_centre,
    closed_parent_box,
    evaluate_parent_class,
    intersect_parent_box,
    literal_frame_signed_slacks,
    parent_frame_extremum,
    restrict_owner_centres,
    unit_parent_extent_lower,
    validate_bound_frames,
    validate_global_rule,
)

F = Fraction
AXIS = (F(1), F(0))
OBLIQUE = (F(3, 5), F(4, 5))
SOURCE_A = DirectionSource(3, reflected=False)
SOURCE_B = DirectionSource(7, reflected=True)


class _UniversalReplayArguments(TypedDict):
    owner_mark: Point
    transform: AffineMap
    residual_centre: Point
    residual_u: Point
    rule: ParentCentreRule
    deadline: float
    clock: parent.Clock


def _map(name: str = "I") -> AffineMap:
    if name == "I":
        return AffineMap(name, 1, 0, 0, 1, F(0), F(0), 0, (0, 1, 2, 3))
    if name == "H":
        return AffineMap(
            name,
            -1,
            0,
            0,
            1,
            OUTER_SIDE,
            F(0),
            0,
            (1, 0, 3, 2),
        )
    if name == "V":
        return AffineMap(
            name,
            1,
            0,
            0,
            -1,
            F(0),
            OUTER_SIDE,
            0,
            (2, 3, 0, 1),
        )
    raise AssertionError(name)


def _dot(left: Point, right: Point) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def _turn(point: Point) -> Point:
    return -point[1], point[0]


def _frame(
    mark: Point,
    ray: Point = AXIS,
    *,
    sources: tuple[DirectionSource, ...] = (SOURCE_A, SOURCE_B),
    index: int = 0,
    quarter_turn: int = 0,
) -> OwnerFrameFootprint:
    centre_set = closed_centre_set(
        mark,
        ray,
        outer_side=OUTER_SIDE,
        half=HALF_CORE,
    )
    retained = RetainedOwnerFrame(ray, index, quarter_turn, sources)
    dimension = centre_set_dimension(centre_set)
    if dimension == -1:
        return OwnerFrameFootprint(retained, (), -1, None, None, None, "empty")
    rectangle, support_r, support_jr = support_rectangle(
        centre_set,
        ray,
        half=HALF_CORE,
    )
    return OwnerFrameFootprint(
        retained,
        centre_set,
        cast(Literal[-1, 0, 1, 2], dimension),
        support_r,
        support_jr,
        rectangle,
        "allowed",
    )


def test_exact_formula_axes_oblique_signs_exchange_and_zero_bound() -> None:
    d = GLOBAL_TANGENT_BOUND
    expected = (F(7, 5) - F(1, 5) * d) / (2 + d * d)
    assert angular_extent_lower(OBLIQUE, d) == expected
    assert unit_parent_extent_lower(OBLIQUE, d) == max(HALF_CORE * F(7, 5), F(1, 2), expected)
    assert angular_extent_lower(OBLIQUE, F(0)) == F(7, 10)
    assert angular_extent_lower(AXIS, F(0)) == F(1, 2)
    for ray in (
        OBLIQUE,
        (F(-3, 5), F(4, 5)),
        (F(4, 5), F(3, 5)),
        (F(-4, 5), F(-3, 5)),
    ):
        assert unit_parent_extent_lower(ray, d) == unit_parent_extent_lower(OBLIQUE, d)


def test_exact_scalar_and_global_rule_refusals() -> None:
    for ray in ((F(0), F(0)), (F(1), F(1)), (1, 0), [F(1), F(0)]):
        with pytest.raises(parent.ParentCompatibilityError):
            angular_extent_lower(ray, GLOBAL_TANGENT_BOUND)
    for value in (F(-1, 100), F(1), F(3, 2), 0.1):
        with pytest.raises(parent.ParentCompatibilityError):
            angular_extent_lower(AXIS, value)
    with pytest.raises(parent.ParentCompatibilityError, match="exact Fraction"):
        closed_parent_box(F(4), 1)
    validate_global_rule(GLOBAL_PARENT_RULE)
    with pytest.raises(parent.ParentCompatibilityError, match="global-D"):
        validate_global_rule(replace(GLOBAL_PARENT_RULE, mode="local-cell"))
    with pytest.raises(parent.ParentCompatibilityError, match="global-D"):
        validate_global_rule(replace(GLOBAL_PARENT_RULE, tangent_bound=F(1, 1000)))
    with pytest.raises(parent.ParentCompatibilityError, match="global-D"):
        validate_global_rule(replace(GLOBAL_PARENT_RULE, outer_side=F(4)))


def test_undersized_bound_counterexample_and_old_b_box_are_visible() -> None:
    parent_extent = F(6997993, 10000010)
    too_small = F(1, 1000)
    large = F(2000, 999999)
    assert angular_extent_lower(OBLIQUE, too_small) > parent_extent
    assert angular_extent_lower(OBLIQUE, large) <= parent_extent
    assert angular_extent_lower(OBLIQUE, GLOBAL_TANGENT_BOUND) <= parent_extent
    old_extent = HALF_CORE * F(7, 5)
    assert old_extent > F(1, 2)
    assert not point_in_closed_convex_polygon(
        (F(3, 5), F(2)),
        closed_parent_box(OUTER_SIDE, old_extent),
    )
    assert point_in_closed_convex_polygon(
        (F(3, 5), F(2)),
        closed_parent_box(OUTER_SIDE, F(1, 2)),
    )


def test_closed_parent_box_preserves_square_singleton_and_empty() -> None:
    square = closed_parent_box(F(4), F(1))
    singleton = closed_parent_box(F(4), F(2))
    empty = closed_parent_box(F(4), F(20001, 10000))
    assert centre_set_dimension(square) == 2
    assert singleton == ((F(2), F(2)),)
    assert centre_set_dimension(singleton) == 0
    assert empty == ()
    assert centre_set_dimension(empty) == -1


def test_derived_domains_rebuild_zb_and_keep_all_dimensions() -> None:
    gap = F(1, 2) - HALF_CORE
    fixtures = (
        ((F(1), F(1)), 2),
        ((gap, F(1)), 1),
        ((gap, gap), 0),
        ((F(0), F(0)), -1),
    )
    for mark, expected_dimension in fixtures:
        original = _frame(mark)
        derived = restrict_owner_centres(original, owner_mark=mark)
        assert derived.restricted.centre_dimension == expected_dimension
        assert derived.restricted.frame == original.frame
        if expected_dimension == -1:
            assert derived.restricted.disposition == "empty"
            assert derived.restricted.support_r is None
            assert derived.restricted.common_rectangle is None
        else:
            assert derived.restricted.disposition == "allowed"
            assert derived.restricted.centre_set
            assert derived.restricted.support_r is not None
            assert derived.restricted.support_jr is not None
            assert derived.restricted.common_rectangle is not None
            assert all(
                point_in_closed_convex_polygon(point, derived.parent_box)
                for point in derived.restricted.centre_set
            )


def test_original_geometry_and_supports_cannot_be_stale() -> None:
    mark = (F(1), F(1))
    source = _frame(mark)
    moved = replace(source, centre_set=((F(9, 8), F(9, 8)),))
    with pytest.raises(parent.ParentCompatibilityError, match="original Z_B"):
        restrict_owner_centres(moved, owner_mark=mark)
    stale = replace(source, support_r=(F(0), F(0)))
    with pytest.raises(parent.ParentCompatibilityError, match="stale support"):
        restrict_owner_centres(stale, owner_mark=mark)


def test_frame_manifest_binds_full_provenance_and_rejects_omissions() -> None:
    mark = (F(1), F(1))
    frame = _frame(mark)
    validate_bound_frames((frame,), (frame.frame,))
    missing_source = replace(frame.frame, sources=(SOURCE_A,))
    with pytest.raises(parent.ParentCompatibilityError, match="provenance"):
        validate_bound_frames((replace(frame, frame=missing_source),), (frame.frame,))
    with pytest.raises(parent.ParentCompatibilityError, match="missing"):
        validate_bound_frames((), (frame.frame,))
    duplicate = (frame.frame, frame.frame)
    with pytest.raises(parent.ParentCompatibilityError, match="duplicate"):
        validate_bound_frames((frame, frame), duplicate)


def test_frozen_manifest_reconstruction_retains_all_source_identities() -> None:
    manifest = full_owner_direction_manifest()
    owner_class = owner_branch_manifest(manifest).classes[0]
    frames = bound_expected_owner_frames(owner_class, manifest)
    assert len(frames) == 181
    assert all(frame.sources for frame in frames)
    identities = {(frame.ray, frame.orientation_index, frame.quarter_turn) for frame in frames}
    assert len(identities) == 181
    assert all(len(set(frame.sources)) == len(frame.sources) for frame in frames)


def test_reflections_exchange_ordered_axes_and_literal_replay_checks_eight_signs() -> None:
    mark = (F(1), F(1))
    derived = restrict_owner_centres(_frame(mark, OBLIQUE), owner_mark=mark)
    row = parent_frame_extremum(
        derived.restricted,
        frame_index=0,
        transform=_map("H"),
        residual_centre=(F(3), F(3)),
        residual_u=AXIS,
        half=HALF_CORE,
        deadline=100,
        clock=lambda: 0,
    )
    assert row.owner_u == (F(4, 5), F(3, 5))
    assert row.owner_v == (F(-3, 5), F(4, 5))
    assert row.axes_checked == 8
    slacks = literal_frame_signed_slacks(
        derived.restricted,
        transform=_map("H"),
        residual_centre=(F(3), F(3)),
        residual_u=AXIS,
        half=HALF_CORE,
    )
    assert tuple(label for label, _ in slacks) == parent.SIGNED_AXIS_LABELS
    assert max(value for _, value in slacks) == row.maximum.slack

    canonical = derived.restricted.centre_set[0]
    canonical_displacement = (canonical[0] - mark[0], canonical[1] - mark[1])
    canonical_coordinates = (
        _dot(canonical_displacement, OBLIQUE),
        _dot(canonical_displacement, _turn(OBLIQUE)),
    )
    transported = parent.transform_owner_frame(derived.restricted, _map("H"))
    transported_mark = _map("H").point(mark)
    transported_displacement = (
        transported.centre_set[0][0] - transported_mark[0],
        transported.centre_set[0][1] - transported_mark[1],
    )
    transported_coordinates = (
        _dot(transported_displacement, transported.owner_u),
        _dot(transported_displacement, transported.owner_v),
    )
    assert transported_coordinates == tuple(reversed(canonical_coordinates))
    assert transported.source.frame == derived.restricted.frame

    vertical = parent.transform_owner_frame(derived.restricted, _map("V"))
    assert vertical.owner_u == (F(-4, 5), F(-3, 5))
    assert vertical.owner_v == (F(3, 5), F(-4, 5))


def test_minimum_projection_drives_maximum_and_reversal_changes_the_answer() -> None:
    mark = (F(1), F(1))
    derived = restrict_owner_centres(_frame(mark), owner_mark=mark)
    row = parent_frame_extremum(
        derived.restricted,
        frame_index=0,
        transform=_map(),
        residual_centre=(F(3), F(3)),
        residual_u=AXIS,
        half=HALF_CORE,
        deadline=100,
        clock=lambda: 0,
    )
    minimum = min(point[0] for point in derived.restricted.centre_set)
    maximum = max(point[0] for point in derived.restricted.centre_set)
    assert row.maximum.minimum_owner_projection == minimum
    correct = F(3) - minimum - 2 * HALF_CORE
    reversed_extremum = F(3) - maximum - 2 * HALF_CORE
    assert row.maximum.slack >= correct
    assert correct > reversed_extremum


def test_positive_replay_reconstructs_restricted_domain() -> None:
    mark = (F(1, 10), F(1, 10))
    original = _frame(mark)
    result = evaluate_parent_class(
        (original,),
        (original.frame,),
        owner_mark=mark,
        transform=_map(),
        residual_centre=(F(3), F(3)),
        residual_u=AXIS,
        deadline=100,
        clock=lambda: 0,
    )
    assert result.status == "compatible"
    assert result.positive_witness is not None
    assert len(result.derived_frames) == result.expected_frames == 1
    witness = cast(FrameExtremum, result.positive_witness)
    parent.replay_positive_parent_witness(
        witness,
        original=original,
        owner_mark=mark,
        transform=_map(),
        residual_centre=(F(3), F(3)),
        residual_u=AXIS,
    )
    old_domain_row = replace(witness, source=original)
    with pytest.raises(parent.ParentCompatibilityError, match="derived domain"):
        parent.replay_positive_parent_witness(
            old_domain_row,
            original=original,
            owner_mark=mark,
            transform=_map(),
            residual_centre=(F(3), F(3)),
            residual_u=AXIS,
        )


def test_universal_mixed_and_all_empty_dispositions_are_distinct() -> None:
    mark = (F(1, 10), F(1, 10))
    allowed = _frame(mark)
    empty = _frame(mark, OBLIQUE, index=1)
    mixed = evaluate_parent_class(
        (allowed, empty),
        (allowed.frame, empty.frame),
        owner_mark=mark,
        transform=_map(),
        residual_centre=(F(3, 4), F(3, 4)),
        residual_u=AXIS,
        deadline=100,
        clock=lambda: 0,
    )
    assert mixed.status == "incompatible"
    assert [row.restricted.disposition for row in mixed.derived_frames] == [
        "allowed",
        "empty",
    ]
    assert len(mixed.frame_extrema) == 1
    assert mixed.frame_extrema[0].frame_index == 0

    empty_at_same_mark = _frame((F(0), F(0)))
    impossible = evaluate_parent_class(
        (empty_at_same_mark,),
        (empty_at_same_mark.frame,),
        owner_mark=(F(0), F(0)),
        transform=_map(),
        residual_centre=(F(1), F(1)),
        residual_u=AXIS,
        deadline=100,
        clock=lambda: 0,
    )
    assert impossible.status == "impossible"
    assert impossible.global_maximum_slack is None
    assert impossible.observed_maximum_slack is None
    assert impossible.derived_frames[0].restricted.disposition == "empty"


def test_universal_nonpositive_replays_each_nonempty_frame() -> None:
    mark = (F(1), F(1))
    axis = _frame(mark)
    oblique = _frame(mark, OBLIQUE, index=1)
    result = evaluate_parent_class(
        (axis, oblique),
        (axis.frame, oblique.frame),
        owner_mark=mark,
        transform=_map(),
        residual_centre=(F(3, 2), F(3, 2)),
        residual_u=AXIS,
        deadline=100,
        clock=lambda: 0,
    )
    assert result.status == "incompatible"
    assert len(result.derived_frames) == 2
    assert len(result.frame_extrema) == 2
    assert result.global_maximum_slack is not None
    assert result.global_maximum_slack <= 0
    parent.replay_parent_universal(
        result,
        owner_mark=mark,
        transform=_map(),
        residual_centre=(F(3, 2), F(3, 2)),
        residual_u=AXIS,
        rule=GLOBAL_PARENT_RULE,
        deadline=100,
        clock=lambda: 0,
    )


# Mutation controls contributed by the 2026-09-10 independent source review.
def _independent_universal_replay_fixture() -> tuple[
    OwnerFrameFootprint,
    ParentClassCompatibility,
    _UniversalReplayArguments,
]:
    mark = (F(1, 10), F(1, 10))
    original = _frame(mark, sources=(DirectionSource(0, reflected=False),))
    arguments: _UniversalReplayArguments = {
        "owner_mark": mark,
        "transform": _map(),
        "residual_centre": (F(3, 4), F(3, 4)),
        "residual_u": AXIS,
        "rule": GLOBAL_PARENT_RULE,
        "deadline": 100.0,
        "clock": lambda: 0,
    }
    result = evaluate_parent_class(
        (original,),
        (original.frame,),
        **arguments,
    )
    assert result.status == "incompatible"
    assert result.global_maximum_slack == F(-7477, 10000)
    assert original != result.derived_frames[0].restricted
    parent.replay_parent_universal(result, **arguments)
    return original, result, arguments


def test_universal_replay_rejects_old_domain_as_extremum_source() -> None:
    original, result, arguments = _independent_universal_replay_fixture()
    altered = replace(
        result,
        frame_extrema=(replace(result.frame_extrema[0], source=original),),
    )
    with pytest.raises(parent.ParentCompatibilityError, match="reconstructed evidence"):
        parent.replay_parent_universal(altered, **arguments)


def test_universal_replay_rejects_duplicate_extremum_rows() -> None:
    _, result, arguments = _independent_universal_replay_fixture()
    altered = replace(result, frame_extrema=result.frame_extrema * 2)
    with pytest.raises(parent.ParentCompatibilityError, match="duplicate"):
        parent.replay_parent_universal(altered, **arguments)


def test_universal_replay_requires_exact_nonempty_extremum_indices() -> None:
    _, result, arguments = _independent_universal_replay_fixture()
    missing = replace(result, frame_extrema=())
    extraneous = replace(
        result,
        frame_extrema=(replace(result.frame_extrema[0], frame_index=1),),
    )
    for altered in (missing, extraneous):
        with pytest.raises(parent.ParentCompatibilityError, match="nonempty derived frames"):
            parent.replay_parent_universal(altered, **arguments)


def test_closed_tangency_is_a_universal_nonpositive_result_without_margin() -> None:
    mark = (F(1, 10), F(1, 10))
    frame = _frame(mark)
    tangent_coordinate = F(1, 2) + CORE_SIDE
    result = evaluate_parent_class(
        (frame,),
        (frame.frame,),
        owner_mark=mark,
        transform=_map(),
        residual_centre=(tangent_coordinate, tangent_coordinate),
        residual_u=AXIS,
        deadline=100,
        clock=lambda: 0,
    )
    assert result.status == "incompatible"
    assert result.global_maximum_slack == 0
    assert result.positive_witness is None


def test_missing_frame_and_deadline_after_final_replay_remain_unresolved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mark = (F(1), F(1))
    frame = _frame(mark)
    missing = evaluate_parent_class(
        (),
        (frame.frame,),
        owner_mark=mark,
        transform=_map(),
        residual_centre=(F(3, 2), F(3, 2)),
        residual_u=AXIS,
        deadline=100,
        clock=lambda: 0,
    )
    assert missing.status == "unresolved"
    assert missing.global_maximum_slack is None
    assert "missing" in cast(str, missing.error)

    expired = False
    real_replay = parent.replay_parent_universal

    def replay_then_expire(
        replay_result: ParentClassCompatibility,
        *,
        owner_mark: object,
        transform: AffineMap,
        residual_centre: object,
        residual_u: object,
        rule: ParentCentreRule,
        deadline: float,
        clock: parent.Clock,
    ) -> None:
        nonlocal expired
        real_replay(
            replay_result,
            owner_mark=owner_mark,
            transform=transform,
            residual_centre=residual_centre,
            residual_u=residual_u,
            rule=rule,
            deadline=deadline,
            clock=clock,
        )
        expired = True

    monkeypatch.setattr(parent, "replay_parent_universal", replay_then_expire)
    result = evaluate_parent_class(
        (frame,),
        (frame.frame,),
        owner_mark=mark,
        transform=_map(),
        residual_centre=(F(3, 2), F(3, 2)),
        residual_u=AXIS,
        deadline=1,
        clock=lambda: 2 if expired else 0,
    )
    assert result.status == "unresolved"
    assert result.global_maximum_slack is None
    assert "after universal acceptance replay" in cast(str, result.error)


def test_expiry_during_replay_and_before_all_empty_verdict_stays_partial(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mark = (F(1), F(1))
    frame = _frame(mark)
    complete = evaluate_parent_class(
        (frame,),
        (frame.frame,),
        owner_mark=mark,
        transform=_map(),
        residual_centre=(F(3, 2), F(3, 2)),
        residual_u=AXIS,
        deadline=100,
        clock=lambda: 0,
    )
    assert complete.status == "incompatible"
    with pytest.raises(parent.ParentCompatibilityDeadlineError, match="during"):
        parent.replay_parent_universal(
            complete,
            owner_mark=mark,
            transform=_map(),
            residual_centre=(F(3, 2), F(3, 2)),
            residual_u=AXIS,
            rule=GLOBAL_PARENT_RULE,
            deadline=1,
            clock=lambda: 2,
        )

    real_require_time = parent._require_time  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]

    def expire_at_empty(deadline: float, clock: parent.Clock, message: str) -> None:
        if "before all-empty disposition" in message:
            raise parent.ParentCompatibilityDeadlineError("synthetic all-empty expiry")
        real_require_time(deadline, clock, message)

    monkeypatch.setattr(parent, "_require_time", expire_at_empty)
    empty_mark = (F(0), F(0))
    empty = _frame(empty_mark)
    partial = evaluate_parent_class(
        (empty,),
        (empty.frame,),
        owner_mark=empty_mark,
        transform=_map(),
        residual_centre=(F(1), F(1)),
        residual_u=AXIS,
        deadline=100,
        clock=lambda: 0,
    )
    assert partial.status == "unresolved"
    assert partial.global_maximum_slack is None
    assert partial.derived_frames[0].restricted.disposition == "empty"
    assert partial.error == "synthetic all-empty expiry"


def test_residual_parent_check_is_separate_and_has_no_owner_displacement() -> None:
    sources = (SOURCE_A, SOURCE_B)
    inside = check_residual_parent_centre(
        (F(2), F(2)),
        OBLIQUE,
        sources,
        sources,
    )
    outside = check_residual_parent_centre(
        (F(1, 10), F(2)),
        OBLIQUE,
        sources,
        sources,
    )
    assert inside.status == "inside-parent-box"
    assert outside.status == "outside-parent-box"
    with pytest.raises(parent.ParentCompatibilityError, match="provenance"):
        check_residual_parent_centre(
            (F(2), F(2)),
            OBLIQUE,
            (SOURCE_A,),
            sources,
        )


def test_generalized_parent_singleton_intersection_is_exact() -> None:
    source = ((F(1), F(1)), (F(3), F(1)), (F(3), F(3)), (F(1), F(3)))
    assert intersect_parent_box(source, ((F(2), F(2)),)) == ((F(2), F(2)),)
    assert intersect_parent_box(source, ((F(4), F(4)),)) == ()
