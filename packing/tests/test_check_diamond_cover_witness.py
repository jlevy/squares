"""Unrelated exact toys only; scientific H-122 reconstruction is forbidden."""

from __future__ import annotations

import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_diamond_cover_witness as reader


@pytest.fixture(autouse=True)
def forbid_target(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: object) -> reader.Domain:
        raise AssertionError("H-122 target geometry is forbidden in source-free tests")

    monkeypatch.setattr(reader, "reconstruct_target", forbidden)


def toy_domain(chart: str = "axis", offset: Fraction = Fraction(1, 600)) -> reader.Domain:
    field = reader.make_field()
    rational = field.rational
    cosine, sine = reader.offset_frame(field, chart, offset)
    diamond = tuple(
        (rational(x), rational(y))
        for x, y in (
            (0, 0),
            (Fraction(1, 4), Fraction(1, 4)),
            (Fraction(1, 2), 0),
            (Fraction(1, 4), Fraction(-1, 4)),
        )
    )
    points = tuple(
        (name, (rational(i / Fraction(100)), rational(0)))
        for i, name in enumerate(reader.POINT_IDS)
    )
    suffix = "positive" if offset > 0 else "negative"
    return reader.Domain(
        field, rational(6), f"{chart}-{suffix}", offset, cosine, sine, diamond, points
    )


def packet(
    domain: reader.Domain,
    center: reader.Point | None = None,
    *,
    axis: reader.Point | None = None,
) -> dict[str, Any]:
    center = center or (domain.field.rational(3), domain.field.rational(3))
    corners = reader.square_corners(center, domain.cosine, domain.sine)
    axis = axis or (domain.field.one, domain.field.zero)
    gap = reader.projection_gap(corners, domain.diamond, axis)
    number = reader.coefficients

    def point(xy: reader.Point) -> list[list[str]]:
        return [number(value) for value in xy]

    return {
        "kind": "diamond-cover-screen/v1",
        "status": "witness",
        "field": {"minimal_polynomial": ["1", "0", "-2"], "isolating_interval": ["1", "2"]},
        "frames": [],
        "witness": {
            "frame_id": domain.frame_id,
            "offset": str(domain.offset),
            "q": number(domain.q),
            "cos": number(domain.cosine),
            "sin": number(domain.sine),
            "center": point(center),
            "corners": [point(xy) for xy in corners],
            "diamond": [point(xy) for xy in domain.diamond],
            "points": [{"id": name, "xy": point(xy)} for name, xy in domain.points],
            "axis": point(axis),
            "gap": number(gap),
        },
    }


def test_vertex_projection_separation_requires_a_strict_gap() -> None:
    field = reader.make_field()
    rational = field.rational
    square = tuple((rational(x), rational(y)) for x, y in ((0, 0), (1, 0), (1, 1), (0, 1)))
    touching = tuple((rational(x), rational(y)) for x, y in ((1, 0), (2, 0), (2, 1), (1, 1)))
    separated = tuple((x + field.alpha, y) for x, y in touching)
    assert reader.strict_separation(square, touching) is None
    witness = reader.strict_separation(square, separated)
    assert witness is not None
    assert witness[1] > 0
    reverse = reader.strict_separation(separated, square)
    assert reverse is not None
    assert reverse[1] > 0


def test_diamond_edge_normal_detects_separation_that_square_axes_miss() -> None:
    field = reader.make_field()
    rational = field.rational
    square = tuple((rational(x), rational(y)) for x, y in ((0, 0), (1, 0), (1, 1), (0, 1)))
    diamond = tuple(
        (rational(x), rational(y))
        for x, y in (
            (Fraction(9, 10), 2),
            (2, Fraction(31, 10)),
            (Fraction(31, 10), 2),
            (2, Fraction(9, 10)),
        )
    )
    assert reader.projection_gap(square, diamond, (field.one, field.zero)) < 0
    assert reader.projection_gap(square, diamond, (field.zero, field.one)) < 0
    separation = reader.strict_separation(square, diamond)
    assert separation is not None
    assert separation[1] > 0


def test_generic_signed_frames_and_exact_corner_membership() -> None:
    field = reader.make_field()
    center = (field.rational(2), field.rational(2))
    for chart in ("axis", "near45"):
        for offset in (Fraction(-1, 7), Fraction(1, 7)):
            cosine, sine = reader.offset_frame(field, chart, offset)
            assert cosine**2 + sine**2 == 1
            corners = reader.square_corners(center, cosine, sine)
            reader.validate_unit_square(corners)
            assert all(value >= 0 for value in reader.edge_determinants(corners, corners[0]))
            beyond = (corners[0][0] - cosine / 100, corners[0][1] - sine / 100)
            assert any(value < 0 for value in reader.edge_determinants(corners, beyond))
    one, zero = field.one, field.zero
    corners = reader.square_corners(center, one, zero)
    extended = (field.rational(3), field.rational(Fraction(3, 2)))
    values = reader.edge_determinants(corners, extended)
    assert any(value == 0 for value in values)
    assert any(value < 0 for value in values)
    with pytest.raises(reader.GuardError):
        reader.validate_unit_square(corners[::-1])


def test_complete_unrelated_witness_uses_nine_marks_and_36_edge_signs() -> None:
    for chart in ("axis", "near45"):
        for offset in (Fraction(-1, 600), Fraction(1, 600)):
            domain = toy_domain(chart, offset)
            result = reader.check_packet(packet(domain), expected=domain)
            assert result["status"] == "verified_counterexample"
            assert result["guard_status"] == "passed"
            assert result["points_checked"] == 9
            assert result["edge_determinants_checked"] == 36
            assert result["strictly_disjoint"] is True
            assert result["contained"] is True
            assert result["complete"] is True


def test_geometric_failures_do_not_accept_the_cover_or_refute_a_validity_guard() -> None:
    domain = toy_domain()
    center = (domain.field.rational(3), domain.field.rational(3))
    boundary = reader.square_corners(center, domain.cosine, domain.sine)[0]
    for i, (name, _) in enumerate(domain.points):
        marked_point = boundary if i % 2 else center
        points = (*domain.points[:i], (name, marked_point), *domain.points[i + 1 :])
        marked = replace(domain, points=points)
        result = reader.check_packet(packet(marked), expected=marked)
        assert result["status"] == "not_a_counterexample"
        assert result["contained_points"] == [name]
        assert result["guard_status"] == "passed"
    outside = (domain.field.rational(7), domain.field.rational(3))
    result = reader.check_packet(packet(domain, outside), expected=domain)
    assert result["status"] == "not_a_counterexample"
    assert result["contained"] is False


def test_closed_container_contact_and_strictly_outside_shift() -> None:
    for chart in ("axis", "near45"):
        for offset in (Fraction(-1, 600), Fraction(1, 600)):
            domain = toy_domain(chart, offset)
            sine_abs = domain.sine if domain.sine >= 0 else -domain.sine
            half_width = (domain.cosine + sine_abs) / 2
            center = (half_width, domain.field.rational(3))
            axis = (domain.field.zero, domain.field.one)
            result = reader.check_packet(packet(domain, center, axis=axis), expected=domain)
            assert result["status"] == "verified_counterexample"
            epsilon = domain.field.rational(Fraction(1, 10**35))
            outside = (half_width - epsilon, center[1])
            result = reader.check_packet(packet(domain, outside, axis=axis), expected=domain)
            assert result["status"] == "not_a_counterexample"
            assert result["contained"] is False


def test_diamond_tangency_and_overlap_are_not_disjointness() -> None:
    domain = toy_domain()
    center = (domain.field.rational(3), domain.field.rational(3))
    corners = reader.square_corners(center, domain.cosine, domain.sine)
    rightmost = max(x for x, _ in corners)
    rational = domain.field.rational
    obstacle = tuple(
        (x + rightmost, y + 3)
        for x, y in (
            (rational(0), rational(0)),
            (rational(1), rational(1)),
            (rational(2), rational(0)),
            (rational(1), rational(-1)),
        )
    )
    # Match the square's extreme vertex, rather than merely its supporting line.
    extreme = next(point for point in corners if point[0] == rightmost)
    obstacle = tuple((x, y + extreme[1] - 3) for x, y in obstacle)
    touching = replace(domain, diamond=obstacle)
    result = reader.check_packet(packet(touching), expected=touching)
    assert result["status"] == "not_a_counterexample"
    assert result["strictly_disjoint"] is False
    epsilon = rational(Fraction(1, 10**35))
    moved = replace(domain, diamond=tuple((x + epsilon, y) for x, y in obstacle))
    assert (
        reader.check_packet(packet(moved), expected=moved)["status"]
        == "verified_counterexample"
    )
    overlap = replace(domain, diamond=corners)
    assert reader.check_packet(packet(overlap), expected=overlap)["strictly_disjoint"] is False


def test_field_and_exact_geometry_identity_refusals_never_reconstruct_target() -> None:
    domain = toy_domain()
    malformed: list[Any] = [None, {}, [], {"kind": "other"}, packet(domain)]
    for name, value in (
        ("kind", "other/v1"),
        ("status", "no_witness"),
        ("field", {"minimal_polynomial": ["1", "0", "-3"], "isolating_interval": ["1", "2"]}),
        ("field", {"minimal_polynomial": ["1", "0", "-2"], "isolating_interval": ["-2", "-1"]}),
    ):
        raw = packet(domain)
        raw[name] = value
        malformed.append(raw)
    for name, value in (
        ("frame_id", "unknown"),
        ("offset", "1/500.0"),
        ("points", []),
        ("cos", ["1"]),
        ("sin", [True, "0"]),
        ("q", ["6.0", "0"]),
        ("gap", ["1/0", "0"]),
        ("corners", []),
    ):
        raw = packet(domain)
        raw["witness"][name] = value
        malformed.append(raw)
    for raw in malformed:
        with pytest.raises(reader.GuardError):
            reader.check_target_packet(raw)


def test_wrong_inventory_corners_axes_and_gap_are_receipt_failures() -> None:
    domain = toy_domain()
    malformed = []
    for name, value in (
        ("cos", ["1", "0"]),
        ("diamond", []),
        ("axis", [["0", "0"], ["0", "0"]]),
        ("gap", ["1", "0"]),
    ):
        raw = packet(domain)
        raw["witness"][name] = value
        malformed.append(raw)
    raw = packet(domain)
    raw["witness"]["points"].reverse()
    malformed.append(raw)
    raw = packet(domain)
    raw["witness"]["points"][1] = raw["witness"]["points"][0]
    malformed.append(raw)
    raw = packet(domain)
    raw["witness"]["corners"].reverse()
    malformed.append(raw)
    for raw in malformed:
        with pytest.raises(reader.GuardError):
            reader.check_packet(raw, expected=domain)


def test_failed_sufficient_angle_guard_leaves_domain_unresolved() -> None:
    for offset in (Fraction(0), Fraction(1, 480), Fraction(-1, 470)):
        domain = toy_domain(offset=offset)
        with pytest.raises(reader.GuardError, match="sufficient angle guard"):
            reader.check_packet(packet(domain), expected=domain)


def test_cli_result_and_refusal_paths_without_scientific_geometry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    domain = toy_domain()
    monkeypatch.setattr(
        reader, "check_target_packet", lambda raw: reader.check_packet(raw, expected=domain)
    )
    source = tmp_path / "toy.json"
    source.write_text(json.dumps(packet(domain)), encoding="utf-8")
    assert reader.main(["--input", str(source)]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "verified_counterexample"
    outside = (domain.field.rational(7), domain.field.rational(3))
    source.write_text(json.dumps(packet(domain, outside)), encoding="utf-8")
    assert reader.main(["--input", str(source)]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "not_a_counterexample"
    for content in ('{"kind":', '{"kind":"x","kind":"x"}', " " * (reader.MAX_PACKET_BYTES + 1)):
        source.write_text(content, encoding="utf-8")
        assert reader.main(["--input", str(source)]) == 2
        captured = capsys.readouterr()
        assert json.loads(captured.out)["status"] == "unresolved"
        assert captured.err


def test_no_witness_is_not_a_positive_proof(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    raw = packet(toy_domain())
    raw["status"], raw["witness"] = "no_witness", None
    source = tmp_path / "screen.json"
    source.write_text(json.dumps(raw), encoding="utf-8")
    assert reader.main(["--input", str(source)]) == 2
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "unresolved"
    assert result["complete"] is False
    assert "no witness" in result["unresolved"][0]
