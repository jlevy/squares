"""Target-blind controls for saved-escape snapped-owner compatibility."""

from __future__ import annotations

import copy
import time
from fractions import Fraction
from typing import Literal, cast

import pytest

import devtools.wall_owner_escape_compatibility as compatibility
from cases.n11_five_dot_cover.independent_union import (
    DeadlineError,
    FrozenInput,
    full_direction_manifest,
)
from devtools.owner_footprints import (
    ANGLE_LIMIT,
    CORE_SIDE,
    HALF_CORE,
    OUTER_SIDE,
    Point,
    Polygon,
)
from devtools.wall_owner_containment import (
    CLASS_IDS,
    AffineMap,
    ContainmentError,
    WallClass,
    WallInput,
    parse_frame_record,
)
from devtools.wall_owner_escape_compatibility import (
    AxisExtremum,
    ClassCompatibility,
    EscapeCompatibilityError,
    FrameExtremum,
    evaluate_class,
    frame_separation_extremum,
    replay_positive_witness,
    run_escape_compatibility,
    transform_owner_frame,
)
from devtools.wall_owner_footprints import (
    OwnerFrameFootprint,
    RetainedOwnerFrame,
    centre_set_dimension,
    closed_centre_set,
    support_rectangle,
)
from devtools.wall_owner_selected_cover import (
    DirectionResult,
    SelectedCoverError,
    SelectedCoverEvidence,
    SelectedCoverResult,
    extract_selected_escape,
    parse_selected_cover_evidence,
    replay_selected_cover_evidence,
    select_four_footprints,
)
from devtools.wall_owner_selected_cover import (
    result_document as selected_result_document,
)

F = Fraction
EIGHT = F(8)
ONE = F(1)


def _rectangle(x0: Fraction, y0: Fraction, x1: Fraction, y1: Fraction) -> Polygon:
    return ((x0, y0), (x1, y0), (x1, y1), (x0, y1))


def _dot(left: Point, right: Point) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def _map(name: str = "I", *, q: Fraction = EIGHT) -> AffineMap:
    if name == "I":
        return AffineMap(name, 1, 0, 0, 1, F(0), F(0), 0, (0, 1, 2, 3))
    if name == "H":
        return AffineMap(name, -1, 0, 0, 1, q, F(0), 0, (1, 0, 3, 2))
    if name == "V":
        return AffineMap(name, 1, 0, 0, -1, F(0), q, 0, (2, 3, 0, 1))
    raise AssertionError(name)


def _frame(
    ray: Point,
    centre_set: Polygon,
    *,
    index: int = 0,
    half: Fraction = ONE,
) -> OwnerFrameFootprint:
    retained = RetainedOwnerFrame(ray, index, 0, ())
    dimension = centre_set_dimension(centre_set)
    rectangle, support_r, support_jr = support_rectangle(centre_set, ray, half=half)
    return OwnerFrameFootprint(
        retained,
        centre_set,
        cast(Literal[-1, 0, 1, 2], dimension),
        support_r,
        support_jr,
        rectangle,
        "allowed",
    )


def _class(frames: tuple[OwnerFrameFootprint, ...]) -> WallClass:
    return WallClass(
        CLASS_IDS[0],
        _rectangle(F(0), F(0), F(1), F(1)),
        "possible",
        _rectangle(F(0), F(0), F(1), F(1)),
        frames,
    )


def test_exact_minimum_projection_and_strict_boundary() -> None:
    frame = _frame((F(1), F(0)), _rectangle(F(2), F(2), F(3), F(3)))
    positive = frame_separation_extremum(
        frame,
        frame_index=0,
        transform=_map(),
        residual_centre=(F(9, 2), F(5, 2)),
        residual_u=(F(1), F(0)),
        half=F(1),
    )
    assert positive.maximum.label == "+owner-u"
    assert positive.maximum.minimum_owner_projection == 2
    assert positive.maximum.canonical_owner_centre == (F(2), F(2))
    assert positive.maximum.slack == F(1, 2)
    replay_positive_witness(
        positive,
        owner_mark=(F(2), F(2)),
        transform=_map(),
        residual_centre=(F(9, 2), F(5, 2)),
        residual_u=(F(1), F(0)),
        outer_side=F(8),
        half=F(1),
    )

    tangency = frame_separation_extremum(
        frame,
        frame_index=0,
        transform=_map(),
        residual_centre=(F(4), F(5, 2)),
        residual_u=(F(1), F(0)),
        half=F(1),
    )
    overlap = frame_separation_extremum(
        frame,
        frame_index=0,
        transform=_map(),
        residual_centre=(F(39, 10), F(5, 2)),
        residual_u=(F(1), F(0)),
        half=F(1),
    )
    assert tangency.maximum.slack == 0
    assert overlap.maximum.slack == F(-1, 10)
    with pytest.raises(EscapeCompatibilityError, match="nonpositive"):
        replay_positive_witness(
            tangency,
            owner_mark=(F(2), F(2)),
            transform=_map(),
            residual_centre=(F(4), F(5, 2)),
            residual_u=(F(1), F(0)),
            outer_side=F(8),
            half=F(1),
        )


def test_oblique_reflections_swap_the_displacement_axes() -> None:
    ray = (F(3, 5), F(4, 5))
    centre = (F(5, 3), F(8, 3))
    frame = _frame(ray, (centre,))
    horizontal = transform_owner_frame(frame, _map("H"))
    vertical = transform_owner_frame(frame, _map("V"))
    assert horizontal.owner_u == (F(4, 5), F(3, 5))
    assert horizontal.owner_v == (F(-3, 5), F(4, 5))
    assert horizontal.centre_set == ((F(19, 3), F(8, 3)),)
    assert vertical.owner_u == (F(-4, 5), F(-3, 5))
    assert vertical.owner_v == (F(3, 5), F(-4, 5))
    assert horizontal.owner_v == (-horizontal.owner_u[1], horizontal.owner_u[0])
    assert vertical.owner_v == (-vertical.owner_u[1], vertical.owner_u[0])

    mark = (F(2), F(2))
    displacement = (centre[0] - mark[0], centre[1] - mark[1])
    assert (F(1, 3), F(2, 3)) == (
        displacement[0] * ray[0] + displacement[1] * ray[1],
        displacement[0] * -ray[1] + displacement[1] * ray[0],
    )
    world_displacement = (
        horizontal.centre_set[0][0] - _map("H").point(mark)[0],
        horizontal.centre_set[0][1] - _map("H").point(mark)[1],
    )
    assert (F(2, 3), F(1, 3)) == (
        _dot(world_displacement, horizontal.owner_u),
        _dot(world_displacement, horizontal.owner_v),
    )


def test_final_frame_witness_prevents_false_universal_exclusion() -> None:
    mark = (F(2), F(2))
    first = _frame((F(1), F(0)), _rectangle(F(2), F(2), F(3), F(3)))
    oblique_ray = (F(4, 5), F(3, 5))
    listed_centres = {
        (F(2), F(2)),
        (F(14, 5), F(13, 5)),
        (F(11, 5), F(17, 5)),
        (F(7, 5), F(14, 5)),
    }
    second_centres = closed_centre_set(
        mark,
        oblique_ray,
        outer_side=F(8),
        half=F(1),
    )
    assert set(second_centres) == listed_centres
    second = _frame(oblique_ray, second_centres, index=1)
    result = evaluate_class(
        _class((first, second)),
        owner_mark=mark,
        corner_index=0,
        class_index=0,
        transform=_map(),
        residual_centre=(F(4), F(4)),
        residual_u=(F(1), F(0)),
        expected_frames=2,
        outer_side=F(8),
        half=F(1),
        deadline=time.perf_counter() + 30,
    )
    assert result.status == "compatible"
    assert len(result.frame_extrema) == 2
    assert result.frame_extrema[0].maximum.slack == 0
    assert result.frame_extrema[1].maximum.slack == F(2, 5)
    assert result.positive_witness == result.frame_extrema[1]

    with pytest.raises(EscapeCompatibilityError, match="complete frame list"):
        evaluate_class(
            _class((first,)),
            owner_mark=mark,
            corner_index=0,
            class_index=0,
            transform=_map(),
            residual_centre=(F(4), F(4)),
            residual_u=(F(1), F(0)),
            expected_frames=2,
            outer_side=F(8),
            half=F(1),
            deadline=time.perf_counter() + 30,
        )


def test_universal_negative_and_degenerate_centre_sets() -> None:
    mark = (F(2), F(2))
    first = _frame((F(1), F(0)), _rectangle(F(2), F(2), F(3), F(3)))
    ray = (F(4, 5), F(3, 5))
    second = _frame(
        ray,
        closed_centre_set(mark, ray, outer_side=F(8), half=F(1)),
        index=1,
    )
    result = evaluate_class(
        _class((first, second)),
        owner_mark=mark,
        corner_index=0,
        class_index=0,
        transform=_map(),
        residual_centre=(F(5, 2), F(5, 2)),
        residual_u=(F(1), F(0)),
        expected_frames=2,
        outer_side=F(8),
        half=F(1),
        deadline=time.perf_counter() + 30,
    )
    assert result.status == "incompatible"
    assert result.global_maximum_slack == F(-13, 10)
    assert all(row.axes_checked == 8 for row in result.frame_extrema)

    point = _frame((F(1), F(0)), ((F(1), F(1)),))
    segment = _frame((F(1), F(0)), ((F(1), F(2)), (F(1), F(3))))
    point_touch = frame_separation_extremum(
        point,
        frame_index=0,
        transform=_map(),
        residual_centre=(F(3), F(3)),
        residual_u=(F(1), F(0)),
        half=F(1),
    )
    segment_touch = frame_separation_extremum(
        segment,
        frame_index=0,
        transform=_map(),
        residual_centre=(F(3), F(5, 2)),
        residual_u=(F(1), F(0)),
        half=F(1),
    )
    assert point_touch.maximum.slack == segment_touch.maximum.slack == 0
    point_positive = frame_separation_extremum(
        point,
        frame_index=0,
        transform=_map(),
        residual_centre=(F(31, 10), F(3)),
        residual_u=(F(1), F(0)),
        half=F(1),
    )
    segment_positive = frame_separation_extremum(
        segment,
        frame_index=0,
        transform=_map(),
        residual_centre=(F(31, 10), F(5, 2)),
        residual_u=(F(1), F(0)),
        half=F(1),
    )
    assert point_positive.maximum.slack == segment_positive.maximum.slack == F(1, 10)


def _frame_record(frame: OwnerFrameFootprint) -> dict[str, object]:
    return {
        "ray": [str(value) for value in frame.frame.ray],
        "orientation_index": frame.frame.orientation_index,
        "quarter_turn": frame.frame.quarter_turn,
        "sources": [],
        "centre_dimension": frame.centre_dimension,
        "centre_set": [[str(value) for value in point] for point in frame.centre_set],
        "disposition": frame.disposition,
        "support_r": [str(value) for value in cast(tuple[Fraction, Fraction], frame.support_r)],
        "support_jr": [
            str(value) for value in cast(tuple[Fraction, Fraction], frame.support_jr)
        ],
        "common_rectangle": [
            [str(value) for value in point] for point in cast(Polygon, frame.common_rectangle)
        ],
    }


def test_typed_frame_parser_reconstructs_points_segments_and_exact_sets() -> None:
    ray = (F(1), F(0))
    retained = RetainedOwnerFrame(ray, 0, 0, ())
    for mark in ((F(0), F(0)), (F(0), F(2))):
        centres = closed_centre_set(mark, ray, outer_side=OUTER_SIDE, half=HALF_CORE)
        frame = _frame(ray, centres, half=HALF_CORE)
        parsed = parse_frame_record(
            _frame_record(frame), retained, label="control", owner_mark=mark
        )
        assert parsed.centre_set == centres
        assert parsed.centre_dimension in (0, 1)

        changed = copy.deepcopy(_frame_record(frame))
        raw_centres = cast(list[list[str]], changed["centre_set"])
        raw_centres[0][0] = str(F(raw_centres[0][0]) + F(1, 100))
        changed_centre_set = tuple(
            (F(point[0]), F(point[1])) for point in cast(list[list[str]], changed["centre_set"])
        )
        changed_frame = _frame(ray, changed_centre_set, half=HALF_CORE)
        changed = _frame_record(changed_frame)
        with pytest.raises(ContainmentError, match="exact centre set"):
            parse_frame_record(changed, retained, label="control", owner_mark=mark)


def _source(revision: str) -> FrozenInput:
    directions = tuple(item.direction for item in full_direction_manifest(ANGLE_LIMIT, 180))
    patch = _rectangle(F(0), F(0), F(1, 10), F(1, 10))
    return FrozenInput(
        "endpoint.json",
        revision,
        "cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19",
        OUTER_SIDE,
        CORE_SIDE,
        ANGLE_LIMIT,
        180,
        (patch,) * 4,
        (
            (F(73, 75), F(187, 90)),
            (F(793, 450), F(43, 15)),
            (F(48, 25), F(48, 25)),
            (F(187, 90), F(73, 75)),
            (F(43, 15), F(793, 450)),
        ),
        F(1),
        F(5),
        directions,
    )


def _wall(revision: str) -> WallInput:
    classes = tuple(
        WallClass(
            class_id,
            _rectangle(F(0), F(0), F(index + 1, 100), F(1, 10)),
            "possible",
            _rectangle(F(0), F(0), F(index + 1, 100), F(1, 10)),
        )
        for index, class_id in enumerate(CLASS_IDS)
    )
    return WallInput("wall.json", revision, "b" * 40, "c" * 40, classes)


def _selected_document(
    source: FrozenInput, wall: WallInput, revision: str
) -> tuple[dict[str, object], SelectedCoverEvidence]:
    selected = select_four_footprints(source, wall)
    escape = extract_selected_escape(source, selected, 0)
    result = SelectedCoverResult(
        "complete",
        "uncovered",
        (DirectionResult(0, source.directions[0].label, F(2), F(1), F(1), 41),),
        escape,
        selected,
        0.1,
    )
    document = selected_result_document(
        result,
        source=source,
        wall=wall,
        implementation_revision=revision,
        process_seconds=0.2,
    )
    evidence = parse_selected_cover_evidence(
        document,
        source_path="selected.json",
        git_commit="d" * 40,
        git_blob="e" * 40,
        expected_source=revision,
        source=source,
        wall=wall,
    )
    return document, evidence


def test_selected_receipt_binding_and_saved_escape_replay() -> None:
    revision = "a" * 40
    source, wall = _source(revision), _wall(revision)
    document, evidence = _selected_document(source, wall, revision)
    replay_selected_cover_evidence(evidence, source=source, deadline=time.perf_counter() + 30)
    assert evidence.direction.uncovered_area == 1
    assert evidence.escape.orientation_index == 0

    changed = copy.deepcopy(document)
    settings = cast(dict[str, object], changed["settings"])
    settings["candidate"] = [0, 0, 0, 0]
    with pytest.raises(SelectedCoverError, match="frozen settings"):
        parse_selected_cover_evidence(
            changed,
            source_path="selected.json",
            git_commit="d" * 40,
            git_blob="e" * 40,
            expected_source=revision,
            source=source,
            wall=wall,
        )

    changed = copy.deepcopy(document)
    sources = cast(dict[str, object], changed["sources"])
    endpoint = cast(dict[str, object], sources["endpoint"])
    endpoint["git_blob"] = "f" * 40
    with pytest.raises(SelectedCoverError, match="endpoint source"):
        parse_selected_cover_evidence(
            changed,
            source_path="selected.json",
            git_commit="d" * 40,
            git_blob="e" * 40,
            expected_source=revision,
            source=source,
            wall=wall,
        )


def test_driver_quantifiers_and_deadline_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    revision = "a" * 40
    source, wall = _source(revision), _wall(revision)
    _, evidence = _selected_document(source, wall, revision)
    monkeypatch.setattr(compatibility, "replay_selected_cover_evidence", lambda *_a, **_k: None)

    calls: list[int] = []

    def incompatible_first(
        *_args: object,
        corner_index: int,
        class_index: int,
        transform: AffineMap,
        **_kwargs: object,
    ) -> ClassCompatibility:
        calls.append(corner_index)
        return ClassCompatibility(
            corner_index,
            class_index,
            transform,
            "incompatible",
            1,
            (),
            F(0),
            F(0),
        )

    monkeypatch.setattr(compatibility, "evaluate_class", incompatible_first)
    result = run_escape_compatibility(
        source, wall, evidence, deadline_seconds=30, expected_frames=1
    )
    assert result.outcome == "incompatible-class"
    assert calls == [3]

    def expired_final(_deadline: float, _message: str) -> None:
        raise DeadlineError("synthetic final expiry")

    monkeypatch.setattr(compatibility, "_deadline", expired_final)
    result = run_escape_compatibility(
        source, wall, evidence, deadline_seconds=30, expected_frames=1
    )
    assert result.status == "partial"
    assert result.outcome == "incomplete"
    assert len(result.classes) == 1
    assert result.error == "synthetic final expiry"
    monkeypatch.undo()
    monkeypatch.setattr(compatibility, "replay_selected_cover_evidence", lambda *_a, **_k: None)

    def compatible(
        *_args: object,
        corner_index: int,
        class_index: int,
        transform: AffineMap,
        **_kwargs: object,
    ) -> ClassCompatibility:
        maximum = AxisExtremum(
            "+owner-u",
            (F(1), F(0)),
            F(0),
            F(1),
            F(1),
            F(1),
            (F(0), F(0)),
            (F(0), F(0)),
        )
        frame = _frame((F(1), F(0)), ((F(1), F(1)),))
        row = FrameExtremum(0, frame, (F(1), F(0)), (F(0), F(1)), maximum)
        return ClassCompatibility(
            corner_index,
            class_index,
            transform,
            "compatible",
            1,
            (row,),
            F(1),
            None,
        )

    monkeypatch.setattr(compatibility, "evaluate_class", compatible)
    result = run_escape_compatibility(
        source, wall, evidence, deadline_seconds=30, expected_frames=1
    )
    assert result.outcome == "all-selected-classes-compatible"
    assert [row.corner_index for row in result.classes] == [3, 0, 1, 2]

    expired = evaluate_class(
        _class((_frame((F(1), F(0)), _rectangle(F(2), F(2), F(3), F(3))),)),
        owner_mark=(F(2), F(2)),
        corner_index=0,
        class_index=0,
        transform=_map(),
        residual_centre=(F(4), F(4)),
        residual_u=(F(1), F(0)),
        expected_frames=1,
        outer_side=F(8),
        half=F(1),
        deadline=time.perf_counter() - 1,
    )
    assert expired.status == "partial"
    assert expired.frame_extrema == ()
    assert expired.global_maximum_slack is None
