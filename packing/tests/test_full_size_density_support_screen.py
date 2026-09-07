"""Readiness controls use side-two supports; target optimization is never invoked."""

from __future__ import annotations

import json
import subprocess
from copy import deepcopy
from fractions import Fraction
from pathlib import Path

import pytest

from devtools.check_full_size_density_support_ceiling import load_packet, replay_packet
from devtools.check_full_size_density_support_ceiling import main as check_main
from devtools.run_full_size_density_support_screen import load_source, source_control
from devtools.run_full_size_density_support_screen import main as run_main
from sqpack.exact_lp import ExactLPError
from sqpack.field import NumberField
from sqpack.full_size_density.support_ceiling import (
    SupportError,
    build_control_support,
    necessary_row,
)
from sqpack.full_size_density.support_screen import (
    bind_source,
    check_fallback_direction,
    extend_rows,
    extension_points,
    initial_rows,
    make_packet,
    solve_screen,
)


def test_source_preimages_and_initial_sequence_are_exact_and_deterministic() -> None:
    seeds, side = load_source("toy-rational-v1")
    bound = bind_source(seeds, side)
    assert bound.support.sizes == (4,)
    assert bound.original_counts == (1,)
    assert bound.baseline == (Fraction(1, 4),)
    assert [len(preimages) for _, preimages in bound.preimages] == [2] * 4
    rows, receipt = initial_rows(bound.support)
    assert len(rows) == 1
    assert receipt[0].trial == 4  # center is on other supporting lines
    assert receipt[0].skipped == (0,)
    assert rows[0].coefficients == (4,)
    points = extension_points(side)
    assert len(points) == 36
    assert [(k, i, j) for k, i, j, _ in points[:3]] == [(1, 1, 1), (2, 1, 1), (2, 1, 2)]
    assert points == extension_points(side)


@pytest.mark.parametrize("source", ["toy-rational-v1", "toy-algebraic-v1"])
def test_toy_packet_round_trip_and_strict_refusals(
    tmp_path: Path, source: str, capsys: pytest.CaptureFixture[str]
) -> None:
    seeds, side = load_source(source)
    bound = bind_source(seeds, side)
    result = solve_screen(bound, threshold=Fraction(1))
    packet = make_packet(source, bound, result)
    path = tmp_path / "upper.json"
    path.write_text(json.dumps(packet), encoding="utf-8")
    assert replay_packet(load_packet(path)) == 1
    assert check_main([str(path), "--timeout-seconds", "60"]) == 0
    assert json.loads(capsys.readouterr().out)["finite_row_optimum"] == "1"
    for key, value in (("bound", "0"), ("multipliers", [True]), ("extra", 1)):
        mutated = deepcopy(packet)
        mutated[key] = value
        with pytest.raises(SupportError):
            replay_packet(mutated)
    for key, value in (("solve_pivots", [65]), ("solve_pivots", [0, 0, 0]), ("primal", [0.25])):
        mutated = deepcopy(packet)
        mutated[key] = value
        with pytest.raises(SupportError):
            replay_packet(mutated)
    mutated = deepcopy(packet)
    mutated["dispositions"][0]["trial"] = 5
    with pytest.raises(SupportError, match="dispositions"):
        replay_packet(mutated)
    mutated = deepcopy(packet)
    mutated["support"]["preimages"][0]["labels"].pop()
    with pytest.raises(SupportError, match="metadata"):
        replay_packet(mutated)
    path.write_text('{"version": 1, "version": 1}', encoding="utf-8")
    with pytest.raises(SupportError, match="duplicate"):
        load_packet(path)
    path.write_text('{"value": 1.0}', encoding="utf-8")
    with pytest.raises(SupportError, match="floating"):
        load_packet(path)
    path.write_text("x" * (2 * 1024 * 1024 + 1), encoding="utf-8")
    with pytest.raises(SupportError, match="size"):
        load_packet(path)
    link = tmp_path / "link.json"
    link.symlink_to(path)
    with pytest.raises(SupportError, match="symlink"):
        load_packet(link)


def test_source_control_has_no_solver_dependency(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args, **_kwargs):
        raise AssertionError("source control must never solve an LP")

    monkeypatch.setattr("sqpack.full_size_density.support_screen.solve_control_lp", forbidden)
    receipt = source_control("toy-rational-v1")
    assert receipt["uniform_mass"] == "1"
    assert receipt["target_outcome"] == "unresolved"


def test_nonparallel_guard_refuses_an_exact_parallel_unit_edge() -> None:
    field = NumberField((1, 0, -5), ("2", "3"))
    ex, ey = 1 / field.alpha, 2 / field.alpha
    fx, fy = -ey, ex
    corner = (field.one - (ex + fx) / 2, field.one - (ey + fy) / 2)
    x, y = corner
    seed = (corner, (x + ex, y + ey), (x + ex + fx, y + ey + fy), (x + fx, y + fy))
    support = build_control_support((seed,), field.rational(2))
    with pytest.raises(SupportError, match="parallel"):
        check_fallback_direction(support)


def test_fixed_extension_deduplicates_rows_and_reuses_an_exact_optimum() -> None:
    seeds, side = load_source("toy-rational-v1")
    bound = bind_source(seeds, side)
    initial, _ = initial_rows(bound.support)
    rows, dispositions = extend_rows(bound.support, initial)
    assert len(dispositions) == 36
    assert len({row.coefficients for row in rows}) == len(rows)
    assert [row.coefficients for row in rows] == [(4,), (1,), (2,), (0,)]
    result = solve_screen(bound, threshold=Fraction(0))
    assert len(result.solve_pivots) == 1
    assert result.solution.bound == 1
    assert result.solution.multipliers[1:] == (0,) * (len(rows) - 1)
    packet = make_packet("toy-rational-v1", bound, result)
    assert replay_packet(packet) == 1
    packet["rows"][1], packet["rows"][2] = packet["rows"][2], packet["rows"][1]
    with pytest.raises(SupportError, match="row order"):
        replay_packet(packet)


def test_second_solve_and_pivot_refusal_do_not_select_another_solver(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seeds, side = load_source("toy-rational-v1")
    bound = bind_source(seeds, side)
    weak = necessary_row(
        bound.support, (side.field.rational("1/2"), side.field.rational("1/2"))
    )
    strong = necessary_row(bound.support, (side.field.one, side.field.one))
    monkeypatch.setattr(
        "sqpack.full_size_density.support_screen.initial_rows", lambda _support: ((weak,), ())
    )
    monkeypatch.setattr(
        "sqpack.full_size_density.support_screen.extend_rows",
        lambda _support, _rows: ((weak, strong), ()),
    )
    result = solve_screen(bound, threshold=Fraction(1))
    assert len(result.solve_pivots) == 2
    assert result.solution.bound == 1

    def exhausted(*_args, **_kwargs):
        raise ExactLPError("pivot-budget", "control refusal")

    monkeypatch.setattr("sqpack.full_size_density.support_screen.solve_control_lp", exhausted)
    with pytest.raises(ExactLPError) as caught:
        solve_screen(bound)
    assert caught.value.kind == "pivot-budget"


def test_cli_requires_an_explicit_mode_and_preserves_deadline_refusals(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    for arguments in (
        [],
        ["--source-control", "--timeout-seconds", "61"],
        ["--solve-target", "--source", "toy-rational-v1"],
    ):
        with pytest.raises(SystemExit) as caught:
            run_main(arguments)
        assert caught.value.code == 2

    def expired(command, **kwargs):
        assert kwargs["timeout"] == 1
        raise subprocess.TimeoutExpired(command, 1)

    monkeypatch.setattr("devtools.run_full_size_density_support_screen.subprocess.run", expired)
    assert (
        run_main(["--source-control", "--source", "toy-rational-v1", "--timeout-seconds", "1"])
        == 1
    )
    assert "unresolved" in capsys.readouterr().err
