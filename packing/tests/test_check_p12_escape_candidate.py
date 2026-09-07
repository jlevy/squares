"""Source-free controls: the frozen H-110 constructor is never a fixture."""

from __future__ import annotations

import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_p12_escape_candidate as reader


@pytest.fixture(autouse=True)
def forbid_scientific_constructor(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden() -> reader.Candidate:
        raise AssertionError("frozen H-110 geometry must not run in source-free tests")

    monkeypatch.setattr(reader, "reconstruct_target", forbidden)


def toy_candidate() -> reader.Candidate:
    # An unrelated square, twelve unrelated marks, and a different near-axis angle.
    cosine, sine = Fraction(359999, 360001), Fraction(1200, 360001)
    center = (Fraction(2), Fraction(2))
    corners = tuple(
        (center[0] + a * cosine - b * sine, center[1] + a * sine + b * cosine)
        for a, b in (
            (Fraction(-1, 2), Fraction(-1, 2)),
            (Fraction(1, 2), Fraction(-1, 2)),
            (Fraction(1, 2), Fraction(1, 2)),
            (Fraction(-1, 2), Fraction(1, 2)),
        )
    )
    points = tuple(
        (name, (Fraction(i, 100), Fraction(0))) for i, name in enumerate(reader.POINT_IDS)
    )
    return reader.Candidate(
        Fraction(5), Fraction(1, 600), cosine, sine, center, corners, points
    )


def packet(candidate: reader.Candidate, status: str = "escaped") -> dict[str, Any]:
    return {
        "kind": "p12-escape-candidate/v1",
        "q": str(candidate.q),
        "t": str(candidate.t),
        "cos": str(candidate.cosine),
        "sin": str(candidate.sine),
        "center": [str(value) for value in candidate.center],
        "corners": [[str(value) for value in point] for point in candidate.corners],
        "points": [
            {"id": name, "xy": [str(value) for value in point]}
            for name, point in candidate.points
        ],
        "status": status,
    }


def test_oriented_edges_distinguish_closed_membership_from_a_line_zero() -> None:
    corners = (
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(1)),
    )
    assert reader.edge_determinants(corners, (Fraction(0), Fraction(0))) == (0, 1, 1, 0)
    assert reader.closed_membership(corners, (Fraction(1, 2), Fraction(0)))
    assert reader.closed_membership(corners, (Fraction(1, 2), Fraction(1, 2)))
    assert not reader.closed_membership(corners, (Fraction(2), Fraction(0)))
    assert reader.edge_determinants(corners, (Fraction(2), Fraction(0))) == (0, -1, 1, 2)


def test_generic_frame_center_and_strip_gap_identities() -> None:
    for tangent in (
        Fraction(-1, 3),
        Fraction(0),
        Fraction(1, 7),
        Fraction(1, 5),
        Fraction(1, 3),
    ):
        cosine, sine = reader.rational_frame(tangent)
        assert cosine > 0
        assert cosine**2 + sine**2 == 1
        center = reader.alternate_center(Fraction(4), cosine, sine)
        projected_a = -sine + cosine
        projected_g = -Fraction(4, 5) * sine + 2 * cosine
        assert -sine * center[0] + cosine * center[1] == (projected_a + projected_g) / 2
        gap = cosine + sine / 5 - 1
        assert gap == 2 * tangent * (Fraction(1, 5) - tangent) / (1 + tangent**2)
        if tangent in (0, Fraction(1, 5)):
            assert gap == 0
        elif 0 < tangent < Fraction(1, 5):
            assert gap > 0
        else:
            assert gap < 0
    with pytest.raises(reader.GuardError, match="positive cosine"):
        reader.alternate_center(Fraction(4), Fraction(0), Fraction(1))


def test_rotated_unit_square_has_exact_boundary_and_strict_escape() -> None:
    corners = (
        (Fraction(21, 10), Fraction(13, 10)),
        (Fraction(27, 10), Fraction(21, 10)),
        (Fraction(19, 10), Fraction(27, 10)),
        (Fraction(13, 10), Fraction(19, 10)),
    )
    assert (
        reader.square_corners((Fraction(2), Fraction(2)), Fraction(3, 5), Fraction(4, 5))
        == corners
    )
    reader.validate_unit_square(corners)
    assert reader.closed_membership(corners, corners[0])
    assert reader.closed_membership(corners, (Fraction(12, 5), Fraction(17, 10)))
    assert not reader.closed_membership(corners, (Fraction(3), Fraction(5, 2)))
    assert min(reader.edge_determinants(corners, (Fraction(3), Fraction(5, 2)))) < 0
    for bad in (corners[:-1], corners[::-1], (corners[0],) * 4):
        with pytest.raises(reader.GuardError):
            reader.validate_unit_square(bad)


def test_complete_toy_packet_checks_all_points_and_edges() -> None:
    candidate = toy_candidate()
    result = reader.check_packet(packet(candidate), expected=candidate)
    assert result["status"] == "escaped"
    assert result["guard_status"] == "passed"
    assert result["complete"] is True
    assert result["points_checked"] == 12
    assert result["edge_determinants_checked"] == 48
    assert result["corners_checked"] == 4
    assert result["contained"] is True
    assert result["contained_points"] == []
    assert result["unresolved"] == []


def test_contained_mark_and_outside_container_are_complete_negative_results() -> None:
    candidate = toy_candidate()
    marked = replace(candidate, points=(("A1", candidate.center), *candidate.points[1:]))
    result = reader.check_packet(packet(marked, "not_escaped"), expected=marked)
    assert result["status"] == "not_escaped"
    assert result["complete"] is True
    assert result["contained_points"] == ["A1"]
    outside = replace(candidate, q=Fraction(1))
    result = reader.check_packet(packet(outside, "not_escaped"), expected=outside)
    assert result["status"] == "not_escaped"
    assert result["contained"] is False
    assert result["guard_status"] == "passed"


def test_closed_boundary_failure_differs_from_arbitrarily_small_strict_escape() -> None:
    candidate = toy_candidate()
    corner = candidate.corners[0]
    boundary = replace(candidate, points=(("A1", corner), *candidate.points[1:]))
    result = reader.check_packet(packet(boundary, "not_escaped"), expected=boundary)
    assert result["contained_points"] == ["A1"]
    epsilon = Fraction(1, 10**40)
    escaped_point = (
        corner[0] - epsilon * candidate.cosine,
        corner[1] - epsilon * candidate.sine,
    )
    escaped = replace(candidate, points=(("A1", escaped_point), *candidate.points[1:]))
    assert reader.check_packet(packet(escaped), expected=escaped)["status"] == "escaped"


def test_container_boundary_is_closed_but_a_tiny_outward_shift_fails() -> None:
    candidate = toy_candidate()
    half_width = (candidate.cosine + candidate.sine) / 2
    center = (half_width, Fraction(2))
    boundary = replace(
        candidate,
        center=center,
        corners=reader.square_corners(center, candidate.cosine, candidate.sine),
    )
    result = reader.check_packet(packet(boundary), expected=boundary)
    assert result["contained"] is True
    assert min(Fraction(row[0]) for row in result["corner_wall_slacks"]) == 0
    center = (half_width - Fraction(1, 10**40), Fraction(2))
    outside = replace(
        candidate,
        center=center,
        corners=reader.square_corners(center, candidate.cosine, candidate.sine),
    )
    result = reader.check_packet(packet(outside, "not_escaped"), expected=outside)
    assert result["contained"] is False
    assert result["complete"] is True


def test_inventory_and_exact_receipt_identity_cannot_be_weakened() -> None:
    candidate = toy_candidate()
    mutations = []
    for key, value in (
        ("q", "6"),
        ("cos", "1"),
        ("sin", "0"),
        ("center", ["0", "0"]),
        ("corners", []),
        ("points", []),
        ("status", "not_escaped"),
    ):
        raw = packet(candidate)
        raw[key] = value
        mutations.append(raw)
    raw = packet(candidate)
    raw["points"][1] = raw["points"][0]
    mutations.append(raw)
    raw = packet(candidate)
    raw["points"].reverse()
    mutations.append(raw)
    raw = packet(candidate)
    raw["points"][0]["xy"] = ["4", "4"]
    mutations.append(raw)
    raw = packet(candidate)
    raw["corners"].reverse()
    mutations.append(raw)
    for raw in mutations:
        with pytest.raises(reader.GuardError):
            reader.check_packet(raw, expected=candidate)


def test_malformed_and_refused_packets_never_reconstruct_the_target() -> None:
    candidate = toy_candidate()
    malformed: list[Any] = [None, [], {}, {"kind": "wrong"}]
    for key, value in (
        ("q", 5),
        ("q", "5.0"),
        ("q", "10/2"),
        ("q", "1/0"),
        ("q", True),
        ("t", "NaN"),
        ("status", "unresolved"),
        ("status", "proved"),
        ("kind", "other/v1"),
        ("center", ["0"]),
    ):
        raw = packet(candidate)
        raw[key] = value
        malformed.append(raw)
    raw = packet(candidate)
    raw["unexpected"] = "field"
    malformed.append(raw)
    malformed.append(packet(candidate))  # well-formed but not the frozen identity
    for failure in ("unresolved", "missing-point"):
        raw = packet(candidate)
        raw["q"], raw["t"] = reader.TARGET_Q_TEXT, reader.TARGET_T_TEXT
        if failure == "unresolved":
            raw["status"] = "unresolved"
        else:
            raw["points"].pop()
        malformed.append(raw)
    for raw in malformed:
        with pytest.raises(reader.GuardError):
            reader.check_target_packet(raw)


def test_failed_sufficient_angle_guard_is_not_a_mathematical_rejection() -> None:
    candidate = toy_candidate()
    for tangent in (Fraction(0), Fraction(1, 480), Fraction(1, 5), Fraction(-1, 600)):
        cosine = (1 - tangent * tangent) / (1 + tangent * tangent)
        sine = 2 * tangent / (1 + tangent * tangent)
        changed = replace(
            candidate,
            t=tangent,
            cosine=cosine,
            sine=sine,
            corners=reader.square_corners(candidate.center, cosine, sine),
        )
        with pytest.raises(reader.GuardError, match="sufficient angle guard"):
            reader.check_packet(packet(changed), expected=changed)


def test_cli_json_and_exit_codes_distinguish_negative_from_guard_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    candidate = toy_candidate()
    marked = replace(candidate, points=(("A1", candidate.center), *candidate.points[1:]))
    monkeypatch.setattr(
        reader, "check_target_packet", lambda raw: reader.check_packet(raw, expected=marked)
    )
    source = tmp_path / "toy.json"
    source.write_text(json.dumps(packet(marked, "not_escaped")), encoding="utf-8")
    assert reader.main(["--input", str(source)]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out)["status"] == "not_escaped"
    assert captured.err == ""
    source.write_text('{"kind":', encoding="utf-8")
    assert reader.main(["--input", str(source)]) == 2
    captured = capsys.readouterr()
    refused = json.loads(captured.out)
    assert refused["status"] == "unresolved"
    assert refused["guard_status"] == "failed"
    assert refused["complete"] is False
    assert captured.err
    source.write_text(json.dumps(packet(marked, "escaped")), encoding="utf-8")
    assert reader.main(["--input", str(source)]) == 2
    captured = capsys.readouterr()
    assert json.loads(captured.out)["guard_status"] == "failed"
    assert "disagrees" in captured.err


def test_cli_missing_oversized_and_duplicate_key_input_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "absent.json"
    assert reader.main(["--input", str(missing)]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "unresolved"
    source = tmp_path / "malformed.json"
    for content in (
        '{"kind":"x","kind":"x"}',
        " " * (reader.MAX_PACKET_BYTES + 1),
        "[" * 2000 + "]" * 2000,
    ):
        source.write_text(content, encoding="utf-8")
        assert reader.main(["--input", str(source)]) == 2
        assert json.loads(capsys.readouterr().out)["guard_status"] == "failed"
