"""Generic controls: no H-124 constructor, retained square, or target side is evaluated."""

from __future__ import annotations

import copy
import json
from dataclasses import replace
from fractions import Fraction
from typing import Any

import pytest

from cases.stromquist.restricted_orientation import Cell, Stratum, project, unproject
from devtools import full_square_compatibility as screen
from sqpack.field import NumberField


@pytest.fixture(autouse=True)
def forbid_scientific_inputs(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: object, **_kwargs: object) -> Any:
        raise AssertionError(
            "scientific constructor, source inventory and retained packet are forbidden"
        )

    monkeypatch.setattr(screen, "target_input", forbidden)
    monkeypatch.setattr(screen, "load_packet", forbidden)
    monkeypatch.setattr(screen, "point_sets", forbidden)


def test_canonical_clip_recomputes_strict_witness_and_keeps_closed_seam() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    zero, one = field.zero, field.one
    cell = Cell(
        Stratum(zero, 4 * one),
        Stratum(zero, 2 * one),
        ((zero, zero), (4 * one, zero), (4 * one, 2 * one), (zero, 2 * one)),
        (2 * one, one),
        0,
    )
    clipped = screen.clip_canonical_cell(3 * one, (one, zero), cell)
    assert clipped is not None
    assert clipped.witness == (5 * one / 4, one / 2)
    assert clipped.witness != cell.witness
    assert set(clipped.polygon) == {
        (one, zero),
        (3 * one / 2, zero),
        (3 * one / 2, one),
        (one, one),
    }
    seam = screen.clip_canonical_cell(2 * one, (one, zero), cell)
    assert seam is not None
    assert seam.witness == (one, one / 2)


def toy_input() -> screen.ScreenInput:
    field = NumberField((1, 0, -2), ("1", "2"))
    frame = field.one, field.zero
    center = 3 * field.one, 3 * field.one
    fixed = screen.FixedSquare(
        "toy-axis", Fraction(0), frame, center, screen.square_corners(center, frame)
    )
    p10 = tuple((field.rational(10 + i), field.rational(10)) for i in range(10))
    p9 = tuple((field.rational(10 + i), field.rational(12)) for i in range(9))
    return screen.ScreenInput(4 * field.one, "toy-axis", frame, fixed, p10, p9, "toy-source")


def test_clip_discards_open_stratum_collapsed_onto_excluded_boundary() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    zero, one = field.zero, field.one
    polygon = ((zero, zero), (one, zero), (one, one), (zero, one))
    open_cell = Cell(Stratum(zero, one), Stratum(zero, one), polygon, (one / 2, one / 2), 0)
    assert screen.clip_canonical_cell(4 * one, (one, zero), open_cell) is None
    closed_cell = Cell(
        Stratum(one, one), Stratum(zero, one), ((one, zero), (one, one)), (one, one / 2), 0
    )
    assert screen.clip_canonical_cell(4 * one, (one, zero), closed_cell) == closed_cell


def test_rotated_clip_and_algebraic_mixture_preserve_every_constraint() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    zero, one = field.zero, field.one
    frame = field.rational("3/5"), field.rational("-4/5")
    polygon = tuple(
        project(point, frame)
        for point in ((zero, zero), (4 * one, zero), (4 * one, 4 * one), (zero, 4 * one))
    )
    cell = Cell(
        Stratum(-4 * one, 4 * one),
        Stratum(zero, 6 * one),
        polygon,
        project((2 * one, 2 * one), frame),
        0,
    )
    clipped = screen.clip_canonical_cell(4 * one, frame, cell)
    assert clipped is not None
    assert unproject(clipped.witness, frame) == (3 * one / 2, one / 2)
    for point in clipped.polygon:
        x, y = unproject(point, frame)
        assert 1 <= x <= 2
        assert 0 <= y <= 1
    cosine, sine = frame
    mixed = screen.positive_cell_point(clipped, (cosine, -sine, field.alpha + one / 4))
    assert mixed is not None
    x, y = unproject(mixed, frame)
    assert field.alpha + one / 4 < x <= 2
    assert 0 <= y <= 1
    assert clipped.u.contains(mixed[0])
    assert clipped.v.contains(mixed[1])


def test_true_pair_witness_checks_canonical_domain_and_all_closed_walls() -> None:
    data = toy_input()
    result = screen.scan_frame(data.side, data.frame, data.fixed_square, data.p10, data.p9)
    witness = result.witness
    assert witness is not None
    assert not result.complete
    assert (
        0
        < result.uncovered_cells_checked
        <= result.canonical_cells_checked
        <= result.cells_checked
    )
    assert 1 <= witness.center[0] <= 2
    assert 0 <= witness.center[1] <= 1
    corners = screen.square_corners(witness.center, data.frame)
    assert all(
        0 <= value <= 4 for point in (*corners, *data.fixed_square.corners) for value in point
    )
    direct = min(screen.dot(witness.axis, point) for point in corners) - max(
        screen.dot(witness.axis, point) for point in data.fixed_square.corners
    )
    assert witness.gap == direct
    assert direct > 0


def test_negative_sine_fixed_square_and_nonaxis_candidate() -> None:
    data = toy_input()
    field = data.side.field
    q_frame = field.rational("3/5"), field.rational("4/5")
    s_frame = field.rational("3/5"), field.rational("-4/5")
    fixed = replace(
        data.fixed_square,
        frame=s_frame,
        corners=screen.square_corners(data.fixed_square.center, s_frame),
    )
    result = screen.scan_frame(data.side, q_frame, fixed, data.p10, data.p9)
    assert result.witness is not None
    corners = screen.square_corners(result.witness.center, q_frame)
    assert all(0 <= value <= 4 for point in (*corners, *fixed.corners) for value in point)
    assert (
        screen.separation_gap(
            result.witness.center, q_frame, fixed.corners, result.witness.axis
        )
        > 0
    )


def test_all_eight_signed_affine_gaps_match_direct_corner_projections() -> None:
    data = toy_input()
    field = data.side.field
    frame = field.alpha / 2, field.alpha / 2
    fixed_frame = field.rational("3/5"), field.rational("-4/5")
    fixed = screen.square_corners(data.fixed_square.center, fixed_frame)
    center = field.rational("3/2"), field.rational("3/4")
    corners = screen.square_corners(center, frame)
    axes = screen.signed_axes(frame, fixed)
    assert len(axes) == 8
    assert all(
        axes[index + 1] == (-axes[index][0], -axes[index][1]) for index in range(0, 8, 2)
    )
    projected = project(center, frame)
    for axis in axes:
        a, b = screen.dot(axis, frame), screen.dot(axis, (-frame[1], frame[0]))
        bound = (screen.absolute(a) + screen.absolute(b)) / 2 + max(
            screen.dot(axis, point) for point in fixed
        )
        direct = min(screen.dot(axis, point) for point in corners) - max(
            screen.dot(axis, point) for point in fixed
        )
        assert direct == a * projected[0] + b * projected[1] - bound
        assert direct == screen.separation_gap(center, frame, fixed, axis)


def test_closed_tangency_is_no_witness_and_small_strict_shift_is_witness() -> None:
    data = toy_input()
    one = data.side.field.one
    center = one, 3 * one / 2
    tangent = replace(
        data.fixed_square, center=center, corners=screen.square_corners(center, data.frame)
    )
    result = screen.scan_frame(data.side, data.frame, tangent, (), ())
    assert result.complete
    assert result.witness is None
    shifted_center = one, 3 * one / 2 + one / 100
    shifted = replace(
        tangent,
        center=shifted_center,
        corners=screen.square_corners(shifted_center, data.frame),
    )
    positive = screen.scan_frame(data.side, data.frame, shifted, (), ())
    assert positive.witness is not None
    assert positive.witness.gap > 0


def test_fixed_square_closed_mark_and_supporting_line_extension_differ() -> None:
    data = toy_input()
    field = data.side.field
    closed_edge = field.rational("7/2"), field.rational(3)
    with pytest.raises(ValueError, match="closed marked point"):
        screen.scan_frame(data.side, data.frame, data.fixed_square, (), (closed_edge,))
    extension = closed_edge[0], field.zero
    assert (
        screen.scan_frame(data.side, data.frame, data.fixed_square, (), (extension,)).witness
        is not None
    )
    mark = field.rational("3/2"), field.rational("3/4")
    blocked = screen.scan_frame(data.side, data.frame, data.fixed_square, (mark,), ())
    assert blocked.witness is None
    assert blocked.complete
    assert blocked.uncovered_cells_checked == 0
    extended_mark = mark[0], field.rational(3)
    assert (
        screen.scan_frame(
            data.side, data.frame, data.fixed_square, (extended_mark,), ()
        ).witness
        is not None
    )


def test_invalid_square_frame_field_and_inventory_refuse() -> None:
    data = toy_input()
    field = data.side.field
    with pytest.raises(ValueError, match="unit length"):
        screen.scan_frame(data.side, (field.one, field.one), data.fixed_square, (), ())
    with pytest.raises(ValueError, match="CCW"):
        screen.scan_frame(
            data.side,
            data.frame,
            replace(data.fixed_square, corners=tuple(reversed(data.fixed_square.corners))),
            (),
            (),
        )
    center = 4 * field.one, 4 * field.one
    with pytest.raises(ValueError, match="containment"):
        screen.scan_frame(
            data.side,
            data.frame,
            replace(
                data.fixed_square,
                center=center,
                corners=screen.square_corners(center, data.frame),
            ),
            (),
            (),
        )
    foreign = NumberField((1, 0, -2), ("1", "2"))
    with pytest.raises(ValueError, match="one exact field"):
        screen.scan_frame(data.side, (foreign.one, foreign.zero), data.fixed_square, (), ())
    for changed in (
        replace(data, p10=data.p10[:-1]),
        replace(data, p9=data.p9[:-1]),
        replace(data, p10=(data.p10[0],) * 10),
    ):
        with pytest.raises(ValueError, match="distinct points"):
            screen.run_screen(changed)


def toy_source_packet(data: screen.ScreenInput) -> dict[str, Any]:
    witness = screen.fixed_square_packet(data.fixed_square)
    witness.update(
        {
            "q": screen.scalar_packet(data.side),
            "points": [
                {"id": name, "xy": screen.point_packet(point)}
                for name, point in zip(screen.POINT_IDS, data.p9, strict=True)
            ],
            "diamond": [],
            "axis": screen.point_packet(data.frame),
            "gap": ["1", "0"],
        }
    )
    return {
        "kind": "diamond-cover-screen/v1",
        "status": "witness",
        "field": screen.FIELD_PACKET,
        "frames": [],
        "witness": witness,
    }


def test_generic_retained_source_parser_copies_only_exact_fixed_square() -> None:
    data = toy_input()
    raw = toy_source_packet(data)
    assert screen.parse_fixed_source(raw, data.side, data.p9) == data.fixed_square
    for name, replacement in (
        ("q", ["3", "0"]),
        ("offset", 0),
        ("cos", ["1.0", "0"]),
        ("sin", [False, "0"]),
        ("corners", []),
        ("points", []),
    ):
        changed = copy.deepcopy(raw)
        changed["witness"][name] = replacement
        with pytest.raises((ValueError, TypeError)):
            screen.parse_fixed_source(changed, data.side, data.p9)
    for changed in (
        {**raw, "extra": 1},
        {**raw, "status": "no_witness"},
        {**raw, "witness": None},
    ):
        with pytest.raises(ValueError, match="retained source"):
            screen.parse_fixed_source(changed, data.side, data.p9)


def test_packet_mocked_cli_and_early_stop_are_source_free(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    data = toy_input()
    monkeypatch.setattr(screen, "target_input", lambda: data)
    original = screen.event_cells_for_frame

    def cells(*args: Any) -> Any:
        yield from original(*args)
        raise AssertionError("an early witness must not exhaust the event stream")

    monkeypatch.setattr(screen, "event_cells_for_frame", cells)
    assert screen.main(["--target-h124"]) == 0
    raw = json.loads(capsys.readouterr().out)
    assert set(raw) == {
        "kind",
        "status",
        "field",
        "source",
        "frame",
        "domain",
        "p10",
        "p9",
        "fixed_square",
        "summary",
        "witness",
    }
    assert raw["status"] == "witness"
    assert raw["summary"]["complete"] is False
    assert raw["fixed_square"] == screen.fixed_square_packet(data.fixed_square)
    assert [point["id"] for point in raw["p10"]] == list(screen.P10_IDS)
    assert [point["id"] for point in raw["p9"]] == list(screen.POINT_IDS)
    assert set(raw["witness"]) == {"center", "corners", "axis", "gap"}


def test_no_witness_packet_cannot_claim_continuous_compatibility() -> None:
    data = toy_input()
    one = data.side.field.one
    center = one, 3 * one / 2
    fixed = replace(
        data.fixed_square, center=center, corners=screen.square_corners(center, data.frame)
    )
    packet = screen.run_screen(replace(data, fixed_square=fixed))
    assert packet["status"] == "no_witness"
    assert packet["witness"] is None
    summary = packet["summary"]
    assert isinstance(summary, dict)
    assert summary["complete"] is True


def test_cli_refusals_do_not_emit_partial_success(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    for arguments in ([], ["--target-h124", "--timeout", "100"]):
        with pytest.raises(SystemExit) as refusal:
            screen.main(arguments)
        assert refusal.value.code == 2
    capsys.readouterr()
    data = toy_input()
    monkeypatch.setattr(screen, "target_input", lambda: replace(data, p9=()))
    assert screen.main(["--target-h124"]) == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert "refused" in output.err

    def unreadable() -> screen.ScreenInput:
        raise OSError("retained source unavailable")

    monkeypatch.setattr(screen, "target_input", unreadable)
    assert screen.main(["--target-h124"]) == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert "retained source unavailable" in output.err
