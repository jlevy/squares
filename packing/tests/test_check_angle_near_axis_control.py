"""Continuous rational toy controls; never construct the fixed-side target."""

from __future__ import annotations

import json
from copy import deepcopy
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any

import pytest

from devtools import check_angle_near_axis_control as reader


@pytest.fixture(autouse=True)
def _forbid_target_construction(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden():
        raise AssertionError("author controls must not construct the fixed-side target")

    monkeypatch.setattr(reader, "target_input", forbidden)


def _packet() -> dict[str, Any]:
    return {
        "version": 1,
        "kind": "fixed-side-near-axis-ten-cover-grid",
        "side": "1939/500",
        "grid": [6, 3],
        "half_angle_slabs": [[str(a), str(b)] for a, b in reader.SLABS],
        "assignments": [list(row) for row in reader.ASSIGNMENTS],
        "status": "proved",
        "inequalities_checked": 864,
        "unresolved": [],
    }


def _toy_input() -> tuple[Fraction, tuple[reader.Point, ...]]:
    return Fraction(3, 2), tuple((Fraction(145 + i, 200), Fraction(3, 4)) for i in range(10))


def test_bernstein_transform_reconstructs_quartics_on_a_shifted_interval() -> None:
    coefficients = tuple(map(Fraction, (3, -2, 5, -7, 11)))
    left, right = Fraction(-2, 3), Fraction(4, 5)
    bernstein = reader.bernstein_coefficients(coefficients, left, right)
    for unit in (Fraction(0), Fraction(1, 7), Fraction(1, 2), Fraction(1)):
        angle = left + (right - left) * unit
        expected = sum(value * angle**power for power, value in enumerate(coefficients))
        actual = sum(
            value * comb(4, index) * unit**index * (1 - unit) ** (4 - index)
            for index, value in enumerate(bernstein)
        )
        assert actual == expected


def test_corner_polynomials_equal_direct_rotated_square_margins_on_both_slabs() -> None:
    side = Fraction(5, 2)
    point = (Fraction(7, 6), Fraction(9, 8))
    normalized = (Fraction(2, 3), Fraction(1, 3))
    for sign in (-1, 1):
        polynomials = reader.corner_polynomials(side, point, normalized, sign)
        for tangent in (Fraction(0), sign * Fraction(1, 100), sign * Fraction(1, 20)):
            denominator = 1 + tangent * tangent
            cosine = (1 - tangent * tangent) / denominator
            sine = 2 * tangent / denominator
            radius = (cosine + abs(sine)) / 2
            center = tuple(radius + (side - 2 * radius) * z for z in normalized)
            dx, dy = point[0] - center[0], point[1] - center[1]
            u, v = cosine * dx + sine * dy, -sine * dx + cosine * dy
            expected = tuple(Fraction(1, 2) - value for value in (u, -u, v, -v))
            for polynomial, margin in zip(polynomials, expected, strict=True):
                found = sum(value * tangent**power for power, value in enumerate(polynomial))
                assert found == 2 * denominator**2 * margin


def test_complete_closed_slabs_preserve_seams_contacts_and_tiny_escapes() -> None:
    zero = Fraction(0)
    slabs = ((Fraction(-1, 10), zero), (zero, Fraction(1, 10)))
    assignments = ((0,) * 6,) * 3
    result = reader.check_closed_slabs(
        Fraction(2), ((Fraction(1), Fraction(1)),), assignments, slabs
    )
    assert result.proved
    assert result.rectangles_checked == 36
    assert result.corners_checked == 144
    assert result.inequalities_checked == 576
    displaced = reader.check_closed_slabs(
        Fraction(2), ((1 - Fraction(1, 2**200), Fraction(1)),), assignments, slabs
    )
    assert not displaced.proved
    assert displaced.inequalities_checked == 576
    assert displaced.uncertified


def test_bernstein_proof_checks_interiors_and_keeps_zero_contacts() -> None:
    zero, one = Fraction(0), Fraction(1)
    contact = (Fraction(1, 4), Fraction(-1), one)
    assert reader.certifies_nonnegative(contact, zero, one)
    assert reader.certifies_nonnegative((zero,) * 5, zero, one)
    interior_failure = (Fraction(1, 4) - Fraction(1, 100), Fraction(-1), one)
    assert not reader.certifies_nonnegative(interior_failure, zero, one)
    assert not reader.certifies_nonnegative((Fraction(-1, 2**200),), zero, one)


def test_fixed_packet_binds_source_and_refuses_partial_positive_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = []

    def toy_source():
        calls.append(1)
        return _toy_input()

    monkeypatch.setattr(reader, "target_input", toy_source)
    packet = _packet()
    receipt = reader.check_packet(packet)
    assert receipt["decision"] == "proved"
    assert receipt["inequalities_checked"] == 576
    assert calls == [1]
    for key, value in (
        ("version", True),
        ("kind", "original-source-axis-ten-cover-grid"),
        ("side", "3878/1000"),
        ("side", 3.878),
        ("grid", [6, 3.0]),
        ("grid", [6, 4]),
        ("half_angle_slabs", [["0", "0"], ["0", "0"]]),
        ("half_angle_slabs", [["-110880/50803079", 0], ["0", "110880/50803079"]]),
        ("assignments", [[0] * 6] * 3),
        ("assignments", [[True] * 6] * 3),
        ("assignments", packet["assignments"][:2]),
        ("inequalities_checked", True),
        ("inequalities_checked", 863),
        ("inequalities_checked", 865),
        ("unresolved", [[0, 0, 0, 0, 0, 0]]),
        ("status", "accepted"),
    ):
        with pytest.raises(ValueError, match=r"packet|invalid|positive|assignments"):
            reader.check_packet({**packet, key: value})
    with pytest.raises(ValueError, match="keys"):
        reader.check_packet({**packet, "timing": 0})
    missing = deepcopy(packet)
    del missing["side"]
    with pytest.raises(ValueError, match="keys"):
        reader.check_packet(missing)
    assert calls == [1]


@pytest.mark.parametrize(
    "payload",
    [
        b'{"version":1,"version":1}',
        b'{"value":1.0}',
        b'{"value":NaN}',
        b"\xff",
        b"{",
        b" " * 262145,
    ],
)
def test_file_admission_refuses_invalid_bytes_before_geometry(
    payload: bytes, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "packet.json"
    source.write_bytes(payload)
    assert reader.main([str(source), "--target-control"]) == 2
    captured = capsys.readouterr()
    assert json.loads(captured.out)["decision"] == "refused"
    costs = json.loads(captured.err)
    assert costs["exit_code"] == 2
    assert costs["wall_cap_seconds"] == 10


def test_reader_refuses_symlink_missing_file_and_missing_dispatch(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "packet.json"
    source.write_text(json.dumps(_packet()))
    link = tmp_path / "link.json"
    link.symlink_to(source)
    for path in (link, tmp_path / "missing.json"):
        assert reader.main([str(path), "--target-control"]) == 2
        assert json.loads(capsys.readouterr().out)["decision"] == "refused"
    for args in (
        [str(source)],
        ["relative.json", "--target-control"],
        [str(source), "--target-control", "--timeout-seconds", "20"],
    ):
        with pytest.raises(SystemExit) as failure:
            reader.main(args)
        assert failure.value.code == 2


def test_complete_file_replay_uses_mocked_geometry_and_retains_costs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "packet.json"
    source.write_text(json.dumps(_packet()))
    monkeypatch.setattr(reader, "target_input", _toy_input)
    assert reader.main([str(source), "--target-control"]) == 0
    captured = capsys.readouterr()
    proof, cost = json.loads(captured.out), json.loads(captured.err)
    assert proof["decision"] == "proved"
    assert proof["rectangles_checked"] == 36
    assert proof["corners_checked"] == 144
    assert proof["inequalities_checked"] == 576
    assert proof["h036_outcome"] == "unresolved"
    assert cost["exit_code"] == 0
    assert cost["wall_seconds"] >= 0
    assert cost["cpu_seconds"] >= 0


def test_incomplete_producer_never_constructs_geometry(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "packet.json"
    for count, failures in ((0, []), (1, [[0, 0, 0, 0, 0, 0]]), (864, [])):
        payload = _packet() | {
            "status": "unresolved",
            "inequalities_checked": count,
            "unresolved": failures,
        }
        source.write_text(json.dumps(payload))
        assert reader.main([str(source), "--target-control"]) == 1
        assert json.loads(capsys.readouterr().out)["decision"] == "unresolved"


def test_alarm_refuses_partial_work_and_restores_previous_handler(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "packet.json"
    alarms: list[int] = []
    previous = reader.signal.getsignal(reader.signal.SIGALRM)
    monkeypatch.setattr(reader.signal, "alarm", alarms.append)

    def interrupted(*_args: object, **_kwargs: object) -> Any:
        raise TimeoutError("toy admission interruption")

    monkeypatch.setattr(reader, "load_packet", interrupted)
    assert reader.main([str(source), "--target-control"]) == 1
    captured = capsys.readouterr()
    assert json.loads(captured.out)["decision"] == "unresolved"
    assert json.loads(captured.err)["exit_code"] == 1
    assert alarms == [10, 0]
    assert reader.signal.getsignal(reader.signal.SIGALRM) == previous


def test_failure_inventory_refuses_reordered_duplicate_or_unchecked_entries() -> None:
    base = _packet() | {"status": "unresolved", "inequalities_checked": 2}
    for failures in (
        [[0, 0, 0, 0, 0, 2]],
        [[0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
        [[False, 0, 0, 0, 0, 0]],
    ):
        with pytest.raises(ValueError, match="unresolved"):
            reader.check_packet(base | {"unresolved": failures})
