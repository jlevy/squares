"""Synthetic controls for the explicit wall-owner selected-cover adapter."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

import devtools.wall_owner_selected_cover as selected_cover
from cases.n11_five_dot_cover.independent_union import (
    FrozenInput,
    UnionMeasure,
    full_direction_manifest,
)
from devtools.owner_footprints import ANGLE_LIMIT, CORE_SIDE, OUTER_SIDE, Polygon
from devtools.wall_owner_containment import CLASS_IDS, WallClass, WallInput
from devtools.wall_owner_selected_cover import (
    SELECTED_TUPLE,
    extract_selected_escape,
    result_document,
    run_selected_cover,
    select_four_footprints,
)

F = Fraction


def _rectangle(x0: Fraction, y0: Fraction, x1: Fraction, y1: Fraction) -> Polygon:
    return ((x0, y0), (x1, y0), (x1, y1), (x0, y1))


def _source() -> FrozenInput:
    directions = tuple(item.direction for item in full_direction_manifest(ANGLE_LIMIT, 180))
    patch = _rectangle(F(0), F(0), F(1, 10), F(1, 10))
    return FrozenInput(
        "endpoint.json",
        "endpoint-revision",
        selected_cover.RETAINED_ENDPOINT_BLOB,
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


def _wall() -> WallInput:
    classes = tuple(
        WallClass(
            class_id,
            _rectangle(F(0), F(0), F(index + 1, 100), F(1, 10)),
            "possible",
            _rectangle(F(0), F(0), F(index + 1, 100), F(1, 10)),
        )
        for index, class_id in enumerate(CLASS_IDS)
    )
    return WallInput("wall.json", "wall-revision", "wall-blob", "constructor", classes)


def test_selected_footprints_use_actual_classes_and_outer_side() -> None:
    selected = select_four_footprints(_source(), _wall())
    assert SELECTED_TUPLE == (0, 0, 0, 7)
    assert tuple(len(polygon) for polygon in selected) == (4, 4, 4, 4)
    assert max(x for x, _ in selected[3]) == OUTER_SIDE
    assert min(x for x, _ in selected[3]) == OUTER_SIDE - F(2, 25)


def test_complete_zero_cover_visits_all_directions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    def zero_measure(
        _source: FrozenInput, direction: object, *, max_subsets: int, deadline: float
    ) -> UnionMeasure:
        assert max_subsets == 511
        assert deadline > 0
        calls.append(str(direction))
        return UnionMeasure(F(1), F(1), 1)

    monkeypatch.setattr(selected_cover, "measure_direction", zero_measure)
    result = run_selected_cover(_source(), _wall(), deadline_seconds=30)
    assert result.status == "complete"
    assert result.outcome == "covered"
    assert len(result.directions) == len(calls) == 361


def test_first_deficit_stops_and_has_strict_selected_escape(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0

    def deficit(
        _source: FrozenInput, _direction: object, *, max_subsets: int, deadline: float
    ) -> UnionMeasure:
        nonlocal calls
        assert max_subsets == 511
        assert deadline > 0
        calls += 1
        return UnionMeasure(F(0), F(1), 0)

    monkeypatch.setattr(selected_cover, "measure_direction", deficit)
    result = run_selected_cover(_source(), _wall(), deadline_seconds=30)
    assert result.status == "complete"
    assert result.outcome == "uncovered"
    assert calls == len(result.directions) == 1
    assert result.escape == extract_selected_escape(_source(), result.selected_footprints, 0)


def test_deadline_before_final_success_is_partial(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    def clock() -> float:
        nonlocal calls
        calls += 1
        return 0.0 if calls <= 362 else 2.0

    monkeypatch.setattr(selected_cover.time, "perf_counter", clock)
    monkeypatch.setattr(
        selected_cover,
        "measure_direction",
        lambda *_args, **_kwargs: UnionMeasure(F(1), F(1), 1),
    )
    result = run_selected_cover(_source(), _wall(), deadline_seconds=1)
    assert result.status == "partial"
    assert result.outcome == "incomplete"
    assert len(result.directions) == 361


def test_receipt_provenance_and_cli_source_refusal(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    source, wall = _source(), _wall()
    monkeypatch.setattr(
        selected_cover,
        "measure_direction",
        lambda *_args, **_kwargs: UnionMeasure(F(1), F(1), 1),
    )
    result = run_selected_cover(source, wall, deadline_seconds=30)
    receipt = result_document(
        result,
        source=source,
        wall=wall,
        implementation_revision="implementation",
        process_seconds=1.0,
    )
    sources = receipt["sources"]
    settings = receipt["settings"]
    assert isinstance(sources, dict)
    assert isinstance(settings, dict)
    wall_source = sources["wall"]
    assert isinstance(wall_source, dict)
    assert wall_source["git_blob"] == "wall-blob"
    assert settings["selected_classes"] == [CLASS_IDS[index] for index in SELECTED_TUPLE]

    output = tmp_path / "invalid.json"
    monkeypatch.setattr(
        selected_cover,
        "validate_own_revision",
        lambda _revision: (tmp_path, "implementation"),
    )
    monkeypatch.setattr(
        selected_cover,
        "validate_output_path",
        lambda candidate, _repository, _inputs: candidate,
    )
    code = selected_cover.main(
        [
            "endpoint.json",
            "wall.json",
            "--expect-endpoint-blob",
            "0" * 40,
            "--expect-wall-blob",
            "wall-blob",
            "--expect-wall-source",
            "wall-source",
            "--expect-git-revision",
            "implementation",
            "--output",
            str(output),
        ]
    )
    assert code == 2
    assert json.loads(output.read_text())["status"] == "invalid"
