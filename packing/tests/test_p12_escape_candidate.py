"""Source-free controls: the scientific constructor must never run in this suite."""

from __future__ import annotations

import json
from dataclasses import replace
from fractions import Fraction
from typing import cast

import pytest

from devtools import p12_escape_candidate as producer


@pytest.fixture(autouse=True)
def forbid_scientific_constructor(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden() -> producer.Candidate:
        raise AssertionError("scientific constructor is forbidden in source-free controls")

    monkeypatch.setattr(producer, "target_candidate", forbidden)


def test_rational_frame_and_strip_midpoint_identities() -> None:
    q = Fraction(4)
    for t in (Fraction(-1, 10), Fraction(0), Fraction(1, 10), Fraction(1, 5), Fraction(1, 4)):
        cosine, sine = producer.half_angle_frame(t)
        assert cosine * cosine + sine * sine == 1
        assert 1 + t * t > 0
        assert cosine > 0
        x, y = producer.strip_midpoint_center(q, t)
        h = (cosine + sine) / 2
        lower = -sine + cosine * (q - 3)
        upper = -Fraction(4, 5) * sine + cosine * (q - 2)
        assert x == h
        assert -sine * x + cosine * y == (lower + upper) / 2
        gap = upper - lower - 1
        assert gap == 2 * t * (Fraction(1, 5) - t) / (1 + t * t)
        if 0 < t < Fraction(1, 5):
            assert gap > 0
        elif t in (0, Fraction(1, 5)):
            assert gap == 0
        else:
            assert gap < 0


def test_unit_corners_and_closed_membership_have_no_tolerance() -> None:
    center = (Fraction(2), Fraction(2))
    cosine, sine = Fraction(3, 5), Fraction(4, 5)
    corners = producer.ccw_corners(center, cosine, sine)
    assert corners == (
        (Fraction(21, 10), Fraction(13, 10)),
        (Fraction(27, 10), Fraction(21, 10)),
        (Fraction(19, 10), Fraction(27, 10)),
        (Fraction(13, 10), Fraction(19, 10)),
    )
    for i, corner in enumerate(corners):
        edge = tuple(corners[(i + 1) % 4][j] - corner[j] for j in range(2))
        next_edge = tuple(corners[(i + 2) % 4][j] - corners[(i + 1) % 4][j] for j in range(2))
        assert sum(value * value for value in edge) == 1
        assert sum(a * b for a, b in zip(edge, next_edge, strict=True)) == 0
        assert edge[0] * next_edge[1] - edge[1] * next_edge[0] == 1
        assert producer.closed_contains(center, cosine, sine, corner)
    one, zero = Fraction(1), Fraction(0)
    boundary = (Fraction(5, 2), Fraction(3, 2))
    extended_support = (Fraction(3), Fraction(3, 2))
    assert producer.closed_contains(center, one, zero, boundary)
    assert not producer.closed_contains(center, one, zero, extended_support)
    assert not producer.closed_contains(
        center, one, zero, (Fraction(5, 2) + Fraction(1, 10**30), Fraction(2))
    )


def test_containment_keeps_closed_walls_and_both_sine_signs() -> None:
    epsilon = Fraction(1, 10**30)
    for sine in (Fraction(4, 5), Fraction(-4, 5)):
        cosine = Fraction(3, 5)
        center = (Fraction(7, 10), Fraction(7, 10))
        assert producer.contained_in_box(Fraction(7, 5), center, cosine, sine)
        assert not producer.contained_in_box(Fraction(7, 5) - epsilon, center, cosine, sine)
        assert not producer.contained_in_box(
            Fraction(4), (center[0] - epsilon, center[1]), cosine, sine
        )


def test_actual_angle_guard_is_sufficient_not_the_outer_proof_interval() -> None:
    assert producer.actual_angle_guard(Fraction(1, 2000))
    for t in (Fraction(-1, 2000), Fraction(0), Fraction(1, 480), Fraction(1, 470)):
        assert not producer.actual_angle_guard(t)


def _toy_candidate() -> producer.Candidate:
    return producer.Candidate(
        q=Fraction(4),
        t=Fraction(1, 2000),
        center=(Fraction(2), Fraction(2)),
        points=tuple(
            producer.Mark(name, (Fraction(i, 20), Fraction(0)))
            for i, name in enumerate(producer.POINT_IDS)
        ),
    )


def test_complete_packet_classifies_escape_hit_and_failed_guard() -> None:
    candidate = _toy_candidate()
    packet = producer.make_packet(candidate)
    assert set(packet) == {
        "kind",
        "q",
        "t",
        "cos",
        "sin",
        "center",
        "corners",
        "points",
        "status",
    }
    assert packet["kind"] == "p12-escape-candidate/v1"
    assert packet["status"] == "escaped"
    assert packet["q"] == "4"
    assert packet["t"] == "1/2000"
    assert packet["center"] == ["2", "2"]
    assert [point["id"] for point in packet["points"]] == list(producer.POINT_IDS)
    assert len(packet["corners"]) == 4
    covered = replace(
        candidate,
        points=(producer.Mark("A1", candidate.center), *candidate.points[1:]),
    )
    assert producer.make_packet(covered)["status"] == "not_escaped"
    outside = replace(candidate, center=(Fraction(0), Fraction(2)))
    assert producer.make_packet(outside)["status"] == "not_escaped"
    assert producer.make_packet(replace(candidate, t=Fraction(0)))["status"] == "unresolved"


def test_a_hit_at_any_inventory_position_blocks_escape_including_boundary_hits() -> None:
    candidate = _toy_candidate()
    cosine, sine = producer.half_angle_frame(candidate.t)
    boundary = producer.ccw_corners(candidate.center, cosine, sine)[0]
    for i, mark in enumerate(candidate.points):
        points = (
            *candidate.points[:i],
            producer.Mark(mark.id, boundary),
            *candidate.points[i + 1 :],
        )
        assert (
            producer.make_packet(replace(candidate, points=points))["status"] == "not_escaped"
        )


def test_zero_projected_gap_does_not_claim_full_point_membership() -> None:
    for t in (Fraction(0), Fraction(1, 5)):
        cosine, sine = producer.half_angle_frame(t)
        center = producer.strip_midpoint_center(Fraction(4), t)
        # This point is on a V-supporting line but outside the square's U interval.
        point = (
            center[0] + 2 * cosine - sine / 2,
            center[1] + 2 * sine + cosine / 2,
        )
        dx, dy = point[0] - center[0], point[1] - center[1]
        assert -sine * dx + cosine * dy == Fraction(1, 2)
        assert not producer.closed_contains(center, cosine, sine, point)


def test_incomplete_reordered_or_duplicate_inventory_cannot_look_like_escape() -> None:
    candidate = _toy_candidate()
    for points in (
        (),
        candidate.points[:-1],
        tuple(reversed(candidate.points)),
        (candidate.points[0], *candidate.points[:-1]),
        (producer.Mark("A1", candidate.points[1].xy), *candidate.points[1:]),
    ):
        with pytest.raises(ValueError, match=r"inventory|distinct"):
            replace(candidate, points=points)


def test_nonexact_scalars_and_bad_frame_fail_before_arithmetic() -> None:
    candidate = _toy_candidate()
    for bad in (True, 0.5, float("nan"), "1/2"):
        with pytest.raises(TypeError, match="Fraction"):
            replace(candidate, t=cast("Fraction", bad))
        with pytest.raises(TypeError, match="Fraction"):
            replace(candidate, center=(cast("Fraction", bad), Fraction(2)))
    with pytest.raises(ValueError, match="positive"):
        replace(candidate, q=Fraction(0))
    with pytest.raises(ValueError, match="unit length"):
        producer.ccw_corners(candidate.center, Fraction(1), Fraction(1))
    for t in (Fraction(-2), Fraction(-1), Fraction(1), Fraction(2)):
        with pytest.raises(ValueError, match="positive cosine"):
            producer.strip_midpoint_center(Fraction(4), t)


def test_cli_dispatch_serializes_only_mocked_generic_input(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    candidate = _toy_candidate()
    calls = 0

    def toy_target() -> producer.Candidate:
        nonlocal calls
        calls += 1
        return candidate

    monkeypatch.setattr(producer, "target_candidate", toy_target)
    assert producer.main(["--target-h110"]) == 0
    assert calls == 1
    captured = capsys.readouterr()
    assert captured.err == ""
    assert json.loads(captured.out) == producer.make_packet(candidate)


def test_cli_no_selection_help_and_overrides_never_call_target(
    capsys: pytest.CaptureFixture[str],
) -> None:
    for args in (
        [],
        ["--target"],
        ["--target-h110", "--q", "4"],
        ["--target-h110", "--t", "0"],
    ):
        with pytest.raises(SystemExit) as error:
            producer.main(args)
        assert error.value.code == 2
        assert capsys.readouterr().err
    with pytest.raises(SystemExit) as error:
        producer.main(["--help"])
    assert error.value.code == 0
    assert "--target-h110" in capsys.readouterr().out


def test_cli_failed_guard_and_constructor_failure_are_nonzero(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    unresolved = replace(_toy_candidate(), t=Fraction(0))
    monkeypatch.setattr(producer, "target_candidate", lambda: unresolved)
    assert producer.main(["--target-h110"]) == 2
    captured = capsys.readouterr()
    assert json.loads(captured.out)["status"] == "unresolved"
    assert "guard" in captured.err

    def broken_constructor() -> producer.Candidate:
        raise ArithmeticError("injected construction failure")

    monkeypatch.setattr(producer, "target_candidate", broken_constructor)
    assert producer.main(["--target-h110"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "injected construction failure" in captured.err


def test_cli_complete_negative_is_a_completed_determination(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    candidate = _toy_candidate()
    covered = replace(
        candidate, points=(*candidate.points[:-1], producer.Mark("J", candidate.center))
    )
    monkeypatch.setattr(producer, "target_candidate", lambda: covered)
    assert producer.main(["--target-h110"]) == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    assert json.loads(captured.out)["status"] == "not_escaped"
