"""Toy geometry and mocked source admission only; the original source is never built."""

from __future__ import annotations

import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

import pytest

from devtools import check_angle_grid_source_control as reader
from devtools.check_angle_grid_source_control import check_rectangles
from devtools.check_full_size_density_support_ceiling import PACKET_BYTES, load_packet
from sqpack.field import NumberField
from sqpack.full_size_density.support_ceiling import SupportError


@pytest.fixture(autouse=True)
def _forbid_unmocked_source(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden():
        raise AssertionError("author tests must not construct the original source")

    monkeypatch.setattr(reader, "original_source", forbidden)


def toy_packet() -> dict[str, Any]:
    return {
        "version": 1,
        "kind": "original-source-axis-ten-cover-grid",
        "grid": [6, 3],
        "angle_slab": ["0", "0"],
        "assignments": [[0] * 6 for _ in range(3)],
        "status": "proved",
        "inequalities_checked": 432,
        "unresolved": [],
    }


def test_closed_rational_grid_retains_every_rectangle_corner() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    labels = ((0,) * 6,) * 3
    result = check_rectangles(q(2), ((q(1), q(1)),), labels)
    assert result.proved
    assert result.corners_checked == 72
    assert result.inequalities_checked == 288
    displaced = check_rectangles(q(2), ((q("1/2"), q("1/2")),), labels)
    assert not displaced.proved
    assert displaced.inequalities_checked == 288
    assert displaced.failures


def test_quadratic_toy_uses_exact_order_and_closed_coordinate_comparisons() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    alpha = field.alpha
    result = check_rectangles(alpha, ((alpha / 2, alpha / 2),), ((0,) * 6,) * 3)
    assert result.proved
    # A negative displacement below float resolution still fails a closed wall hit.
    q = field.rational
    tiny = Fraction(1, 2**1024)
    moved = check_rectangles(q(2), ((q(1 - tiny), q(1)),), ((0,) * 6,) * 3)
    assert not moved.proved


def test_fixed_packet_admission_is_strict_and_cannot_replace_geometry_with_a_flag(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    calls = []

    def toy_source():
        calls.append(1)
        return q(2), ((q(1), q(1)),)

    monkeypatch.setattr(reader, "original_source", toy_source)
    packet = toy_packet()
    assert reader.check_packet(packet)["decision"] == "proved"
    assert calls == [1]
    for key, value in (
        ("version", True),
        ("version", "1"),
        ("grid", [6, True]),
        ("grid", [6, 4]),
        ("angle_slab", [0, 0]),
        ("angle_slab", ["0", "1/100"]),
        ("assignments", [[0] * 6] * 2),
        ("assignments", [[False] * 6] * 3),
        ("assignments", [[10] * 6] * 3),
        ("assignments", [[0] * 5] * 3),
        ("inequalities_checked", True),
        ("inequalities_checked", 431),
        ("unresolved", [[0, 0, 0, 0, 0]]),
        ("status", "certified"),
        ("kind", "target-cover"),
    ):
        altered = {**packet, key: value}
        with pytest.raises(
            ValueError, match=r"version|grid|slab|assignment|label|status|source"
        ):
            reader.check_packet(altered)
    extra = {**packet, "target_side": "1939/500"}
    with pytest.raises(ValueError, match="keys"):
        reader.check_packet(extra)
    missing = deepcopy(packet)
    del missing["grid"]
    with pytest.raises(ValueError, match="keys"):
        reader.check_packet(missing)
    assert calls == [1]
    monkeypatch.setattr(reader, "original_source", lambda: (q(2), ((q("1/2"), q("1/2")),)))
    with pytest.raises(ValueError, match="corner"):
        reader.check_packet(packet)


def test_shared_json_loader_can_tighten_but_never_widen_its_default_cap(tmp_path: Path) -> None:
    path = tmp_path / "toy.json"
    payload = b'{"value":1}'
    path.write_bytes(payload)
    assert load_packet(path) == {"value": 1}
    assert load_packet(path, max_bytes=len(payload)) == {"value": 1}
    with pytest.raises(SupportError, match="size cap"):
        load_packet(path, max_bytes=len(payload) - 1)
    for invalid in (0, -1, True, 1.5, "10", PACKET_BYTES + 1):
        with pytest.raises(SupportError, match="byte limit"):
            load_packet(path, max_bytes=cast(int, invalid))


def test_cli_keeps_source_admission_timeout_and_costs_separate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    packet = tmp_path / "toy.json"
    output, log = tmp_path / "receipt.json", tmp_path / "replay.log"
    packet.write_text(json.dumps(toy_packet()))
    for args in (
        [str(packet)],
        [str(packet), "--target"],
        [str(packet), "--source-control", "--timeout-seconds", "11"],
        [str(packet), "--source-control", "--side", "2"],
    ):
        with pytest.raises(SystemExit) as rejected:
            reader.main(args)
        assert rejected.value.code == 2
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    calls = []

    def toy_source():
        calls.append(1)
        return q(2), ((q(1), q(1)),)

    alarms = []
    monkeypatch.setattr(reader, "original_source", toy_source)
    monkeypatch.setattr(reader.signal, "alarm", alarms.append)
    args = [str(packet), "--source-control", "--output", str(output), "--log", str(log)]
    assert reader.main(args) == 0
    assert calls == [1]
    assert alarms == [10, 0]
    receipt = json.loads(output.read_text())
    assert receipt["decision"] == "proved"
    assert receipt["h036_outcome"] == "unresolved"
    assert "wall_seconds" not in receipt
    costs = json.loads(log.read_text())
    assert costs["exit_code"] == 0
    assert costs["wall_seconds"] >= 0
    assert costs["cpu_seconds"] >= 0
    assert json.loads(capsys.readouterr().out)["decision"] == "proved"

    def timeout():
        calls.append(1)
        raise TimeoutError("toy exact arithmetic interrupted")

    monkeypatch.setattr(reader, "original_source", timeout)
    assert reader.main(args) == 1
    assert calls == [1, 1]
    assert json.loads(output.read_text())["decision"] == "unresolved"
    assert json.loads(output.read_text())["h036_outcome"] == "unresolved"
    assert json.loads(log.read_text())["exit_code"] == 1
    assert alarms == [10, 0, 10, 0]


def test_partial_and_failed_prefixes_stay_unresolved_without_source_construction() -> None:
    packet = {**toy_packet(), "status": "unresolved", "inequalities_checked": 1}
    assert reader.check_packet(packet)["decision"] == "unresolved"
    failed = {**packet, "unresolved": [[0, 0, 0, 0, 0]]}
    assert reader.check_packet(failed)["decision"] == "unresolved"
    complete_failure = {**failed, "inequalities_checked": 432}
    assert reader.check_packet(complete_failure)["decision"] == "unresolved"
    for failures in (
        [[0, 0, 0, 0, 1]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, False]],
        [[-1, 0, 0, 0, 0]],
        [[0, 0, 2, 0, 0]],
        [[0, 0, 0, 3, 0]],
        [[0, 0, 0, 0, 4]],
        [[0, 0, 0, 0]],
    ):
        with pytest.raises(ValueError, match="unresolved"):
            reader.check_packet({**packet, "unresolved": failures})
    with pytest.raises(ValueError, match="prefix"):
        reader.check_packet(
            {**complete_failure, "unresolved": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 0]]}
        )
    with pytest.raises(ValueError, match="status"):
        reader.check_packet({**complete_failure, "unresolved": []})


def test_malformed_toy_geometry_cannot_gain_a_closed_cover() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    other = NumberField((1, 0, -2), ("1", "2"))
    labels = ((0,) * 6,) * 3
    for side, points in (
        (q(1), ((q("1/2"), q("1/2")),)),
        (q(2), ()),
        (q(2), ((q(1), other.one),)),
        (q(2), ((q(-1), q(1)),)),
        (q(2), ((q(1), q(1)), (q(1), q(1)))),
        (q(2), ((q(1), q(1)), (q("1/2"), q(1)))),
    ):
        with pytest.raises(ValueError, match=r"box|inventory|field|outside|distinct"):
            check_rectangles(side, points, labels)


def test_file_admission_preserves_loader_refusals_and_the_tighter_cap(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "toy.json"
    for payload in (
        b'{"x":1,"x":2}',
        b'{"x":1.0}',
        b'{"x":NaN}',
        b'{"x":1e999999}',
        b"\xff",
        b"{",
        b" " * (reader.PACKET_BYTE_CAP + 1),
    ):
        path.write_bytes(payload)
        assert reader.main([str(path), "--source-control"]) == 2
        assert json.loads(capsys.readouterr().out)["decision"] == "refused"
    path.write_text(json.dumps(toy_packet()))
    link = tmp_path / "linked.json"
    link.symlink_to(path)
    assert reader.main([str(link), "--source-control"]) == 2
    assert "symlink" in json.loads(capsys.readouterr().out)["reason"]
    assert reader.main([str(tmp_path), "--source-control"]) == 2
    assert "regular file" in json.loads(capsys.readouterr().out)["reason"]
    for args in (
        [str(path), "--source-control", "--output", str(path)],
        [str(path), "--source-control", "--output", str(link)],
        [
            str(path),
            "--source-control",
            "--output",
            str(tmp_path / "same"),
            "--log",
            str(tmp_path / "same"),
        ],
    ):
        with pytest.raises(SystemExit) as rejected:
            reader.main(args)
        assert rejected.value.code == 2


def test_reader_lower_cap_refuses_valid_json_that_the_shared_default_accepts(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "oversized-valid.json"
    text = "x" * reader.PACKET_BYTE_CAP
    path.write_text(json.dumps(text))
    assert load_packet(path) == text
    assert reader.main([str(path), "--source-control"]) == 2
    assert "size cap" in json.loads(capsys.readouterr().out)["reason"]
