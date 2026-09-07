"""Unrelated exact pair controls; scientific constructors and retained S are forbidden."""

from __future__ import annotations

import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_full_square_compatibility as reader


@pytest.fixture(autouse=True)
def forbid_science(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: object) -> reader.Expected:
        raise AssertionError("scientific target/source constructor is forbidden in controls")

    monkeypatch.setattr(reader, "load_target", forbidden)
    read_json = reader.read_json

    def source_free_read(path: Path) -> Any:
        assert path.resolve() != (reader.REPO / reader.SOURCE).resolve()
        return read_json(path)

    monkeypatch.setattr(reader, "read_json", source_free_read)


def scalar(value: Any) -> list[str]:
    return [str(coefficient) for coefficient in value.coeffs]


def point(value: reader.Point) -> list[list[str]]:
    return [scalar(coordinate) for coordinate in value]


def toy_fixture(chart: str = "axis", offset: Fraction = Fraction(1, 10000)) -> reader.Expected:
    field = reader.make_field()
    q = field.rational(8)
    fixed_frame = reader.offset_frame(field, chart, offset)
    fixed_center = field.rational(6), field.rational(6)
    fixed = reader.Square(
        f"{chart}-{'negative' if offset < 0 else 'positive'}",
        offset,
        fixed_frame,
        fixed_center,
        reader.square_corners(fixed_center, fixed_frame),
    )
    p10 = tuple(
        (name, (field.rational(Fraction(index, 10)), field.rational(4)))
        for index, name in enumerate(reader.P10_IDS, start=1)
    )
    p9 = tuple(
        (name, (field.rational(Fraction(index, 10)), field.rational(3)))
        for index, name in enumerate(reader.P9_IDS, start=1)
    )
    return reader.Expected(
        field,
        "unrelated-toy-source.json",
        q,
        (field.alpha / 2, field.alpha / 2),
        p10,
        p9,
        fixed,
    )


def packet(expected: reader.Expected, center: reader.Point | None = None) -> dict[str, Any]:
    field, fixed = expected.field, expected.fixed_square
    center = center or (field.rational(2), field.one)
    corners = reader.square_corners(center, expected.frame)
    axis = -field.one, field.zero
    return {
        "kind": "full-square-compatibility/v1",
        "status": "witness",
        "field": reader.FIELD,
        "source": expected.source,
        "frame": {
            "id": "exact45",
            "cos": scalar(expected.frame[0]),
            "sin": scalar(expected.frame[1]),
        },
        "domain": {
            "q": scalar(expected.q),
            "x": point((field.one, expected.q / 2)),
            "y": point((field.zero, field.one)),
        },
        "p10": [{"id": name, "xy": point(xy)} for name, xy in expected.p10],
        "p9": [{"id": name, "xy": point(xy)} for name, xy in expected.p9],
        "fixed_square": {
            "frame_id": fixed.frame_id,
            "offset": str(fixed.offset),
            "cos": scalar(fixed.frame[0]),
            "sin": scalar(fixed.frame[1]),
            "center": point(fixed.center),
            "corners": [point(xy) for xy in fixed.corners],
        },
        "summary": {
            "cells_checked": 3,
            "canonical_cells_checked": 2,
            "uncovered_cells_checked": 1,
            "complete": False,
        },
        "witness": {
            "center": point(center),
            "corners": [point(xy) for xy in corners],
            "axis": point(axis),
            "gap": scalar(reader.signed_gap(corners, fixed.corners, axis)),
        },
    }


def test_oriented_edges_include_boundary_and_strictly_exclude_outside() -> None:
    field = reader.make_field()
    square = reader.square_corners((field.zero, field.zero), (field.one, field.zero))
    reader.validate_unit_square(square)
    assert all(value >= 0 for value in reader.determinants(square, (field.one / 2, field.zero)))
    assert any(value < 0 for value in reader.determinants(square, (field.one, field.zero)))
    with pytest.raises(reader.GuardError):
        reader.validate_unit_square(tuple(reversed(square)))


def test_separating_axis_requires_positive_gap_not_tangency() -> None:
    field = reader.make_field()
    frame = field.one, field.zero
    left = reader.square_corners((field.zero, field.zero), frame)
    touching = reader.square_corners((field.one, field.zero), frame)
    apart = reader.square_corners((field.rational(Fraction(3, 2)), field.zero), frame)
    assert reader.separating_axis(left, touching) is None
    result = reader.separating_axis(left, apart)
    assert result is not None
    assert result[1] > 0


@pytest.mark.parametrize("chart", ["axis", "near45"])
@pytest.mark.parametrize("offset", [Fraction(-1, 10000), Fraction(1, 10000)])
def test_complete_unrelated_pair_both_s_charts_and_angle_signs(
    chart: str, offset: Fraction
) -> None:
    expected = toy_fixture(chart, offset)
    result = reader.check_packet(packet(expected), expected=expected)
    assert result["status"] == "verified_pair"
    assert result["complete"] is True
    assert result["strict_disjointness"] is True
    assert result["Q_points_checked"] == 10
    assert result["S_points_checked"] == 9
    assert result["coordinate_wall_checks"] == 16
    assert result["wall_inequalities_checked"] == 32
    assert result["edge_determinants_checked"] == 76
    assert len(result["point_checks"]) == 19
    assert len(result["wall_slacks"]) == 16
    assert result["unresolved"] == []


def test_point_roles_are_not_accidentally_strengthened_to_both_sets_per_square() -> None:
    expected = toy_fixture()
    q_center = expected.field.rational(2), expected.field.one
    changed = replace(
        expected,
        p10=((reader.P10_IDS[0], expected.fixed_square.center), *expected.p10[1:]),
        p9=((reader.P9_IDS[0], q_center), *expected.p9[1:]),
    )
    assert reader.check_packet(packet(changed), expected=changed)["status"] == "verified_pair"


def test_required_point_on_boundary_is_not_strictly_avoided() -> None:
    expected = toy_fixture()
    q_corners = reader.square_corners(
        (expected.field.rational(2), expected.field.one), expected.frame
    )
    changed_q = replace(expected, p10=(*expected.p10[:-1], (reader.P10_IDS[-1], q_corners[0])))
    changed_s = replace(
        expected, p9=(*expected.p9[:-1], (reader.P9_IDS[-1], expected.fixed_square.corners[0]))
    )
    for changed in (changed_q, changed_s):
        with pytest.raises(reader.GuardError, match="contains a required avoided mark"):
            reader.check_packet(packet(changed), expected=changed)


def test_canonical_and_containment_boundaries_are_exact() -> None:
    expected = toy_fixture()
    field = expected.field
    for center in (
        (field.one, field.one),
        (expected.q / 2, field.one),
        (field.rational(2), field.alpha / 2),
    ):
        assert (
            reader.check_packet(packet(expected, center), expected=expected)["canonical_Q"]
            is True
        )
    for center in (
        (field.one - Fraction(1, 1000), field.one),
        (field.rational(2), field.one + Fraction(1, 1000)),
        (field.rational(2), field.zero),
    ):
        with pytest.raises(reader.GuardError):
            reader.check_packet(packet(expected, center), expected=expected)


def test_overlap_and_tangency_refuse_a_positive_pair_receipt() -> None:
    expected = toy_fixture()
    field, frame = expected.field, expected.frame
    center = field.rational(2), field.one
    # A generic S at a tiny actual near45 offset cannot be declared an overlapping pair.
    fixed = replace(
        expected.fixed_square,
        center=center,
        corners=reader.square_corners(center, expected.fixed_square.frame),
    )
    overlapping = replace(expected, fixed_square=fixed)
    with pytest.raises(reader.GuardError, match="separating gap"):
        reader.check_packet(packet(overlapping), expected=overlapping)
    # Exact tangent squares also exercise the independent SAT kernel in a rotated frame.
    left = reader.square_corners(center, frame)
    right = reader.square_corners((center[0] + frame[0], center[1] + frame[1]), frame)
    assert reader.separating_axis(left, right) is None


def test_source_fixed_square_and_complete_inventory_binding() -> None:
    expected = toy_fixture()
    cases = []
    raw = packet(expected)
    raw["source"] = "different-source.json"
    cases.append(raw)
    raw = packet(expected)
    raw["fixed_square"]["center"][0] = ["5", "0"]
    cases.append(raw)
    for role in ("p10", "p9"):
        raw = packet(expected)
        raw[role].pop()
        cases.append(raw)
        raw = packet(expected)
        raw[role][1] = raw[role][0]
        cases.append(raw)
        raw = packet(expected)
        raw[role][0]["xy"] = raw[role][1]["xy"]
        cases.append(raw)
    for raw in cases:
        with pytest.raises(reader.GuardError):
            reader.check_packet(raw, expected=expected)


def test_unit_corner_order_center_angle_and_gap_mutations_are_refused() -> None:
    expected = toy_fixture()
    cases = []
    raw = packet(expected)
    raw["witness"]["corners"].reverse()
    cases.append(raw)
    raw = packet(expected)
    raw["witness"]["center"][0] = ["3", "0"]
    cases.append(raw)
    raw = packet(expected)
    raw["witness"]["corners"][0][0] = ["999", "0"]
    cases.append(raw)
    for key, value in (
        ("gap", ["0", "0"]),
        ("gap", ["1", "0"]),
        ("axis", [["0", "0"], ["0", "0"]]),
        ("axis", [["1", "0"], ["0", "0"]]),
    ):
        raw = packet(expected)
        raw["witness"][key] = value
        cases.append(raw)
    for raw in cases:
        with pytest.raises(reader.GuardError):
            reader.check_packet(raw, expected=expected)
    changed = toy_fixture(offset=Fraction(1, 100))
    with pytest.raises(reader.GuardError, match="angle sufficient guard"):
        reader.check_packet(packet(changed), expected=changed)
    changed = replace(expected, frame=(expected.field.one, expected.field.zero))
    with pytest.raises(reader.GuardError, match="positive45"):
        reader.check_packet(packet(changed), expected=changed)
    fixed = replace(expected.fixed_square, frame=(expected.field.one, expected.field.zero))
    changed = replace(expected, fixed_square=fixed)
    with pytest.raises(reader.GuardError, match="frame disagrees"):
        reader.check_packet(packet(changed), expected=changed)


def test_malformed_or_foreign_receipts_refuse_before_scientific_loader() -> None:
    expected = toy_fixture()
    cases: list[Any] = [None, [], {}, packet(expected)]
    for key, value in (
        ("field", {"minimal_polynomial": ["1", "0", "-3"], "isolating_interval": ["1", "2"]}),
        ("status", "no_witness"),
        ("witness", None),
        ("p10", []),
    ):
        raw = packet(expected)
        raw[key] = value
        cases.append(raw)
    raw = packet(expected)
    raw["summary"]["cells_checked"] = True
    cases.append(raw)
    raw = packet(expected)
    raw["frame"]["cos"] = ["2/2", "0"]
    cases.append(raw)
    raw = packet(expected)
    raw["domain"]["q"] = ["1/0", "0"]
    cases.append(raw)
    for raw in cases:
        with pytest.raises(reader.GuardError):
            reader.check_target_packet(raw)


def test_cli_records_complete_pair_or_explicit_refusal_without_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    expected = toy_fixture()
    monkeypatch.setattr(
        reader, "check_target_packet", lambda raw: reader.check_packet(raw, expected=expected)
    )
    path = tmp_path / "unrelated.json"
    path.write_text(json.dumps(packet(expected)), encoding="utf-8")
    assert reader.main(["--input", str(path)]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out)["status"] == "verified_pair"
    assert not captured.err
    for text in (
        '{"kind":',
        '{"kind":1,"kind":1}',
        " " * (reader.MAX_PACKET_BYTES + 1),
        json.dumps({**packet(expected), "status": "no_witness"}),
    ):
        path.write_text(text, encoding="utf-8")
        assert reader.main(["--input", str(path)]) == 2
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result["status"] == "unresolved"
        assert result["complete"] is False
        assert captured.err
