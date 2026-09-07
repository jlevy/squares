"""Source-free controls; no H-122 frame or scientific constructor is evaluated."""

from __future__ import annotations

import json
from fractions import Fraction

import pytest

from cases.stromquist import restricted_orientation as source
from devtools import diamond_cover_screen as screen
from sqpack.field import NumberField


@pytest.fixture(autouse=True)
def forbid_target(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden() -> screen.ScreenInput:
        raise AssertionError("H-122 constructor and its scientific frames are forbidden")

    monkeypatch.setattr(screen, "target_input", forbidden)


def test_generic_event_cells_keep_negative_sine_and_original_wrapper() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    side = field.rational(2)
    frame = (field.rational("3/5"), field.rational("-4/5"))
    cells = list(source.event_cells_for_frame(side, frame, ()))
    assert {cell.dimension for cell in cells} == {1, 2}
    for cell in cells:
        assert cell.u.contains(cell.witness[0])
        assert cell.v.contains(cell.witness[1])
        center = source.unproject(cell.witness, frame)
        assert all(
            field.rational("7/10") <= value <= field.rational("13/10") for value in center
        )
        assert cell.covered == 0
    points = ((field.one, field.one),)
    for angle in (0, 45):
        assert list(source.event_cells(side, angle, points)) == list(
            source.event_cells_for_frame(side, source.direction(side, angle), points)
        )


def test_fixed_frame_screen_returns_a_strictly_disjoint_true_witness() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    diamond = tuple(
        (field.rational(x), field.rational(y))
        for x, y in (("13/10", "3/2"), ("3/2", "17/10"), ("17/10", "3/2"), ("3/2", "13/10"))
    )
    frame = (field.one, field.zero)
    result = screen.scan_frame(field.rational(3), frame, diamond, ())
    assert result.witness is not None
    assert result.witness.gap > 0
    assert result.cells_checked > 0
    assert result.uncovered_cells_checked > 0
    assert not result.complete
    assert screen.separation_gap(result.witness.center, frame, diamond, result.witness.axis) > 0


def test_positive_closure_mix_preserves_open_strata_and_exact_gap() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    zero, one = field.zero, field.one
    cell = source.Cell(
        source.Stratum(zero, one),
        source.Stratum(zero, one),
        ((zero, zero), (one, zero), (one, one), (zero, one)),
        (one / 2, one / 2),
        0,
    )
    point = screen.positive_cell_point(cell, (one, zero, field.rational("3/4")))
    assert point is not None
    assert point == (field.rational("7/8"), field.rational("1/8"))
    assert cell.u.contains(point[0])
    assert cell.v.contains(point[1])
    algebraic = screen.positive_cell_point(cell, (one, zero, field.alpha / 2))
    assert algebraic is not None
    assert algebraic[0] > field.alpha / 2
    assert any(value.coeffs[1] for value in algebraic)
    assert screen.positive_cell_point(cell, (one, zero, one)) is None
    singleton = source.Cell(
        source.Stratum(one, one), source.Stratum(zero, zero), ((one, zero),), (one, zero), 0
    )
    assert screen.positive_cell_point(singleton, (one, zero, zero)) == (one, zero)


def toy_diamond(field: NumberField, left: str = "1") -> source.Polygon:
    x = field.rational(left)
    half = field.rational("1/2")
    return ((x, half), (x + half, field.one), (x + 1, half), (x + half, field.zero))


def test_closed_tangency_is_not_a_witness_and_strict_shift_is() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    frame = field.one, field.zero
    tangent = screen.scan_frame(field.one, frame, toy_diamond(field), ())
    assert tangent == screen.FrameResult(1, 1, complete=True, witness=None)
    separated = screen.scan_frame(field.one, frame, toy_diamond(field, "1001/1000"), ())
    assert separated.witness is not None
    assert separated.witness.gap > 0
    covered = screen.scan_frame(
        field.one, frame, toy_diamond(field, "2"), ((field.one / 2, field.one / 2),)
    )
    assert covered == screen.FrameResult(1, 0, complete=True, witness=None)


def test_negative_sine_screen_checks_all_closed_walls() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    frame = field.rational("3/5"), field.rational("-4/5")
    result = screen.scan_frame(field.rational(2), frame, toy_diamond(field, "4"), ())
    assert result.witness is not None
    corners = screen.square_corners(result.witness.center, frame)
    assert all(0 <= coordinate <= 2 for point in corners for coordinate in point)
    e0 = corners[1][0] - corners[0][0], corners[1][1] - corners[0][1]
    e1 = corners[2][0] - corners[1][0], corners[2][1] - corners[1][1]
    assert e0[0] * e1[1] - e0[1] * e1[0] == 1


def test_invalid_frames_and_obstacles_refuse() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    with pytest.raises(ValueError, match="unit"):
        list(source.event_cells_for_frame(field.rational(2), (field.one, field.one), ()))
    with pytest.raises(ValueError, match="four"):
        screen.signed_axes((field.one, field.zero), ())
    with pytest.raises(ValueError, match="area"):
        screen.signed_axes((field.one, field.zero), ((field.zero, field.zero),) * 4)
    second_field = NumberField((1, 0, -2), ("1", "2"))
    with pytest.raises(ValueError, match="one exact field"):
        screen.scan_frame(
            field.one, (second_field.one, second_field.zero), toy_diamond(field), ()
        )


def toy_input() -> screen.ScreenInput:
    field = NumberField((1, 0, -2), ("1", "2"))
    frame = screen.FrameSpec("toy", Fraction(0), (field.one, field.zero))
    points = tuple((field.rational(10 + i), field.rational(10)) for i in range(9))
    return screen.ScreenInput(field.one, (frame,), toy_diamond(field, "2"), points)


def test_packet_and_mocked_cli_are_complete_and_source_free(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    data = toy_input()
    monkeypatch.setattr(screen, "target_input", lambda: data)
    assert screen.main(["--target-h122"]) == 0
    packet = json.loads(capsys.readouterr().out)
    assert set(packet) == {"kind", "status", "field", "frames", "witness"}
    assert packet["status"] == "witness"
    witness = packet["witness"]
    assert set(witness) == {
        "frame_id",
        "offset",
        "q",
        "cos",
        "sin",
        "center",
        "corners",
        "diamond",
        "points",
        "axis",
        "gap",
    }
    assert [point["id"] for point in witness["points"]] == list(screen.POINT_IDS)
    assert witness["q"] == ["1", "0"]
    assert len(witness["corners"]) == 4
    assert packet["frames"][0]["complete"] is False


def test_first_witness_stops_before_later_frame() -> None:
    data = toy_input()
    frames = (
        *data.frames,
        screen.FrameSpec("not-visited", Fraction(0), (data.side, data.side)),
    )
    packet = screen.run_screen(screen.ScreenInput(data.side, frames, data.diamond, data.points))
    assert packet["status"] == "witness"
    summaries = packet["frames"]
    assert isinstance(summaries, list)
    assert len(summaries) == 1


def test_no_witness_never_claims_continuous_cover_and_bad_inventory_refuses() -> None:
    data = toy_input()
    packet = screen.run_screen(
        screen.ScreenInput(data.side, data.frames, toy_diamond(data.side.field), data.points)
    )
    assert packet["status"] == "no_witness"
    assert packet["witness"] is None
    with pytest.raises(ValueError, match="nine"):
        screen.run_screen(
            screen.ScreenInput(data.side, data.frames, data.diamond, data.points[:-1])
        )


def test_cli_missing_or_extra_flag_does_not_dispatch() -> None:
    for arguments in ([], ["--target-h122", "--another-target"]):
        with pytest.raises(SystemExit) as failure:
            screen.main(arguments)
        assert failure.value.code == 2


def test_mark_on_closed_edge_is_covered_but_extended_line_is_not() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    frame = field.one, field.zero
    diamond = toy_diamond(field, "2")
    edge = screen.scan_frame(field.one, frame, diamond, ((field.one, field.one / 2),))
    assert edge.witness is None
    assert edge.uncovered_cells_checked == 0
    extended = screen.scan_frame(field.one, frame, diamond, ((field.one, field.rational(2)),))
    assert extended.witness is not None


def test_mocked_cli_refusal_emits_no_partial_success(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    data = toy_input()
    monkeypatch.setattr(
        screen,
        "target_input",
        lambda: screen.ScreenInput(data.side, (), data.diamond, data.points),
    )
    assert screen.main(["--target-h122"]) == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert "refused" in output.err
