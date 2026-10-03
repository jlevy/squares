"""The capture pilot's scorer: the review's falsifier read from logs, receipts and checkpoints.

The runs are synthetic: the round summaries are built by the pilot's own `round_summary`
from made-up owner measurements, and the logs by its `round_line`, so the scorer reads the
shapes the pilot writes. One test runs a real one-round pilot on a small box and scores
what it prints.
"""

from __future__ import annotations

import json
import math
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import pilot_n17_capture as pilot
from devtools import score_n17_capture as score
from sqpack.hull_kernel.rational import Q

CONTRACTING = {0: "corner-SW", 1: "side-N2"}
COARSE = (2, "side-S2")
LABELS = {"corner-SW": 1, "side-N2": 16}
TURNS = {"corner-SW": 0.0, "side-N2": 0.9315906698566871}
BOX = 2.0**-9

# One owner's state in a round: (widest-row ratio, x extent, y extent).
Owner = tuple[float, float, float]


def measured(cell: str, ratio: float, x: float, y: float, live: int) -> dict[str, Any]:
    """An owner measurement with the keys `measure_owner` returns, centred extents."""
    extent = {"x": x, "y": y}
    widest = 2.0**-12
    return {
        "label": LABELS.get(cell, 6),
        "cell": cell,
        "rows": live,
        "live_rows": live,
        "live_width": live * widest,
        "widest_live_row": widest,
        "widest_live_row_turn": ratio * max(x, y),
        "turn_range": [-1e-3, 1e-3],
        "extent": extent,
        "position_extent": max(x, y),
        "row_to_extent": ratio,
        "residual_volume": 1e-9,
        "deviation": {key: value / 2 for key, value in extent.items()},
        "range": {key: [-value / 2, value / 2] for key, value in extent.items()},
        "turn_deviation": 1e-3,
        "position_deviation": max(x, y) / 2,
        "endpoint_row_position_deviation": 0.0,
        "inside_guard": False,
        "owned_hull_vertices": 4,
        "owned_hull_area": 0.9,
    }


def build(spec: Sequence[Sequence[Owner]], live: int = 8) -> list[dict[str, Any]]:
    """Round summaries, round 0 first, as `run_pilot` appends them."""
    rounds: list[dict[str, Any]] = []
    previous = None
    for index, owners in enumerate(spec):
        now = {
            owner: measured(cell, *owners[owner], live) for owner, cell in CONTRACTING.items()
        }
        now[COARSE[0]] = measured(COARSE[1], 1.0, 0.5, 0.5, 4)
        summary = pilot.round_summary(index, now, previous, list(CONTRACTING))
        rounds.append({**summary, **({"complete": True} if index else {}), "splits": 2})
        previous = now
    return rounds


def log_text(
    rounds: Sequence[dict[str, Any]], *, start: float = 0.0, step_seconds: float = 10.0
) -> str:
    """The stderr lines a process prints for these rounds, from `start` seconds."""
    lines = ["warning: not JSON, skipped"]
    seconds, step = start, 0
    for entry in rounds:
        if entry["round"] == 0:
            continue
        for cell in CONTRACTING.values():
            seconds += step_seconds
            lines.append(json.dumps(step_line(entry["round"], step, cell, seconds)))
            step += 1
        lines.append(json.dumps(pilot.round_line(entry, entry["splits"])))
    return "\n".join(lines) + "\n"


def step_line(number: int, step: int, cell: str, seconds: float) -> dict[str, Any]:
    return {
        "round": number,
        "step": step,
        "cell": cell,
        "rows": 10,
        "live_rows": 8,
        "splits": 1,
        "producer": 1.0,
        "checker": 1.0,
        "seconds": seconds,
    }


def scored(rounds: list[dict[str, Any]], *, exact: bool = True) -> dict[str, Any]:
    run = score.merge([score.parse_log(log_text(rounds), "a.log")])
    by_round = {entry["round"]: entry for entry in rounds} if exact else {}
    return score.score_run(run, by_round, labels=LABELS, turns=TURNS)


def test_three_fine_and_flat_rounds_meet_the_falsifier() -> None:
    rounds = build([[(1.0, BOX, BOX)] * 2] + [[(0.04, BOX, BOX)] * 2] * 4)
    result = scored(rounds)
    reading = result["falsifier"]
    assert reading["state"] == "MET"
    assert reading["met_rounds"] == [1, 2, 3]
    assert "the architecture is wrong" in reading["reason"]
    assert [row["state"] for row in result["rounds"]] == ["UNDECIDED"] * 3 + ["MET"] * 2
    assert pilot.falsifier_reading(rounds)["falsified"] is True
    assert scored(rounds, exact=False)["falsifier"]["state"] == "MET"


def test_a_tenth_off_the_worst_extent_clears_it() -> None:
    rounds = build(
        [
            [(1.0, BOX, BOX)] * 2,
            [(0.08, BOX, BOX)] * 2,
            [(0.08, BOX, BOX)] * 2,
            [(0.16, BOX / 2, BOX / 2)] * 2,
            [(0.32, BOX / 4, BOX / 4)] * 2,
        ]
    )
    reading = scored(rounds)["falsifier"]
    assert reading["state"] == "CLEARED"
    assert reading["contraction_start"]["round"] == 3
    assert reading["contraction_start"]["max_ratio_before"] == pytest.approx(0.08)
    assert reading["g_worst_extent_from_start"] == pytest.approx([0.5, 0.5])
    assert pilot.falsifier_reading(rounds)["contraction_start"]["round"] == 3
    assert "positions contract" in reading["reason"]


def test_rows_above_a_twentieth_leave_it_undecided_and_say_why() -> None:
    stuck = [(0.03, BOX, BOX), (0.1003, BOX, BOX)]
    rounds = build([[(1.0, BOX, BOX)] * 2, stuck, stuck, stuck, stuck])
    result = scored(rounds)
    reading = result["falsifier"]
    assert reading["state"] == "UNDECIDED"
    assert reading["reason"].startswith("ratio 0.1003 > 1/20 at side-N2 in round 4")
    assert "precondition is not reached at this row cap" in reading["reason"]
    assert result["rounds"][-1]["binding"] == "side-N2"
    assert result["rounds"][-1]["under_twentieth"] == 1
    logs_only = scored(rounds, exact=False)
    assert logs_only["falsifier"]["state"] == "UNDECIDED"
    assert logs_only["rounds"][-1]["binding"] == "side-N2"


def test_fine_rows_with_a_falling_side_are_not_flat() -> None:
    falling = [[(0.04, BOX, BOX * 0.8**index), (0.04, BOX, BOX)] for index in range(1, 5)]
    rounds = build([[(1.0, BOX, BOX)] * 2, *falling])
    reading = scored(rounds)["falsifier"]
    assert reading["state"] == "UNDECIDED"
    assert reading["contraction_start"] is None
    assert "corner-SW y fell to 0.8000" in reading["reason"]
    assert "not flat" in reading["reason"]


def test_a_resumed_run_spans_logs_and_supersedes_the_abandoned_round() -> None:
    rounds = build([[(1.0, BOX, BOX)] * 2] + [[(0.5, BOX, BOX)] * 2] * 4)
    first = log_text(rounds[:3]) + json.dumps(step_line(3, 4, "corner-SW", 99.0)) + "\n"
    second = log_text(rounds[3:], start=5.0, step_seconds=20.0)
    second += json.dumps(step_line(5, 8, "corner-SW", 90.0)) + "\n"
    run = score.merge([score.parse_log(first, "a.log"), score.parse_log(second, "b.log")])
    assert sorted(run.rounds) == [1, 2, 3, 4]
    assert run.missing == []
    assert run.segments[0]["superseded"] == {
        "by": "b.log",
        "from_round": 3,
        "steps": 1,
        "round_lines": [],
    }
    assert run.rounds[2].wall == pytest.approx(20.0)
    assert run.rounds[3].wall == pytest.approx(45.0)
    assert run.rounds[4].wall == pytest.approx(40.0)
    assert run.in_progress == {
        "round": 5,
        "steps": 1,
        "cells": ["corner-SW"],
        "wall_so_far": pytest.approx(5.0),
    }
    result = score.score_run(run, {entry["round"]: entry for entry in rounds})
    assert [row["round"] for row in result["rounds"]] == [0, 1, 2, 3, 4]
    assert [row.get("disagreements") for row in result["rounds"]] == [None, [], [], [], []]


def test_the_round_line_carries_the_flags_the_rounded_ratio_cannot() -> None:
    rounds = build([[(1.0, BOX, BOX)] * 2] + [[(0.049996, BOX, BOX)] * 2] * 3)
    line = pilot.round_line(rounds[1], 2)
    assert line["row_to_extent"] == 0.05
    assert line["binding"] == "corner-SW"
    assert line["fine"] is True
    assert line["flat"] is True
    run = score.merge([score.parse_log(log_text(rounds), "a.log")])
    assert score.score_run(run, {})["falsifier"]["state"] == "MET"
    old = {key: value for key, value in line.items() if key not in {"fine", "flat"}}
    logged = score.LogRound(1, old, 0, 2, 1.0, 1.0)
    assert score.round_score(1, logged, None)["fine"] is False


def test_a_checkpoint_is_read_only_up_to_its_rounds(tmp_path: Path) -> None:
    rounds = build([[(1.0, BOX, BOX)] * 2] + [[(0.5, BOX, BOX)] * 2] * 2)
    path = tmp_path / "checkpoint-round-002.json.gz"
    record = {
        "schema": f"{pilot.SCHEMA}/checkpoint",
        "fine_rounds": 0,
        "groups": {"0": ["1/2,1/2"]},
        "initial": {"groups": {}, "cell_references": {}},
        "provenance": {"files": {}},
        "round": 2,
        "rounds": rounds,
        "rows": {"0": [{"interval": ["0", "1"]}]},
        "steps": ["x" * 4096] * 1024,
        "updates": [],
    }
    pilot.write_checkpoint(path, record)
    text = json.dumps(rounds, sort_keys=True, separators=(",", ":"), default=str)
    assert score.checkpoint_rounds(path, limit=len(text) + score.CHUNK) == json.loads(text)
    assert score.load_rounds([path])[2] == json.loads(text)[2]
    with pytest.raises(ValueError, match="exceed"):
        score.checkpoint_rounds(path, limit=len(text) // 2)
    partial = tmp_path / "run.partial.json"
    partial.write_text(json.dumps({"rounds": rounds[:2]}), encoding="utf-8")
    merged = score.load_rounds([partial, path])
    assert sorted(merged) == [0, 1, 2]


def test_target_factors_name_the_local_radius_coordinates() -> None:
    rounds = build([[(1.0, BOX, BOX)] * 2, [(0.5, BOX, BOX / 2)] * 2])
    table = score.coordinate_table(rounds[1], rounds[0])
    assert table["side-N2"]["y"]["fall"] == pytest.approx(0.5)
    assert table["side-N2"]["turn"]["extent"] == pytest.approx(2e-3)
    radii = {"xi16": Fraction(1, 1216), "eta16": Fraction(1, 1216), "omega16": Fraction(1, 500)}
    factors = score.target_factors(table, LABELS, radii)
    by_name = {row["name"]: row for row in factors["coordinates"]}
    assert set(by_name) == {"xi16", "eta16", "omega16"}
    assert by_name["xi16"]["side_factor"] == pytest.approx(BOX / 2 * 1216)
    assert by_name["xi16"]["extent_factor"] == pytest.approx(BOX / 2 * 1216)
    assert by_name["omega16"]["side_factor"] == pytest.approx(0.5)
    assert factors["inside"] == 2
    assert factors["unmatched_radii"] == []


def test_rows_needed_count_bisection_levels_where_the_rows_lie() -> None:
    assert score.halvings(0.1003, pilot.FINE_ROWS) == 2
    assert score.halvings(0.05, pilot.FINE_ROWS) == 1
    assert score.halvings(0.04, pilot.FINE_ROWS) == 0
    assert score.halvings(math.inf, pilot.FINE_ROWS) is None
    # Near t = 0 a chart row of width 2^-11 turns by just under 2^-10.
    assert score.chart_rows([(0.0, 2 * math.atan(2.0**-6) - 1e-12)], 2.0**-10) == 32
    # Pilot 2's side-N2 at round 12 of the 256-row run: below chart t = 1/2 its rows need
    # two more levels to pass a twentieth of the box, above it one.
    pieces = score.chart_pieces(TURNS["side-N2"], -0.02806760209862924, 0.0015553359402750155)
    assert score.chart_rows(pieces, BOX / 20) == 544
    assert score.chart_pieces(0.0, -1e-3, 2e-3) == [
        (0.0, 2e-3),
        (pilot.QUARTER - 1e-3, pilot.QUARTER),
    ]
    rounds = build([[(1.0, BOX, BOX)] * 2, [(0.03, BOX, BOX), (0.1003, BOX, BOX)]], live=64)
    needed = score.rows_needed(rounds[1], TURNS)
    own = needed["owners"]["side-N2"]
    assert own["halvings_twentieth"] == 2
    assert own["rows_twentieth"] == 256
    assert own["rows_twentieth_continuous"] == 129
    assert own["rows_twentieth_chart"] == math.ceil(
        score.chart_rows(score.chart_pieces(TURNS["side-N2"], -1e-3, 1e-3), BOX / 20)
        * own["live_share"]
    )
    assert needed["owners"]["corner-SW"]["rows_twentieth"] == 64
    assert needed["coarse_live_rows"] == 4


def test_a_narrowing_live_range_is_extrapolated_to_the_cap() -> None:
    widths = [{"live_width": {"side-N2": 8.0 / 2**index}} for index in range(5)]
    assert score.narrowing(widths, "side-N2") == pytest.approx(0.5)
    assert score.narrowing(widths[:1], "side-N2") is None
    assert score.rounds_to_fit(544, 256, 0.955) == 17
    assert score.rounds_to_fit(200, 256, 0.9) == 0
    assert score.rounds_to_fit(300, 256, 1.0) is None
    stuck = [(0.03, BOX, BOX), (0.1003, BOX, BOX)]
    result = scored(build([[(1.0, BOX, BOX)] * 2, stuck, stuck, stuck]))
    own = result["rows_needed"]["owners"]["side-N2"]
    assert own["narrowing"] == pytest.approx(1.0)
    assert own["rounds_to_fit_cap"] is None
    assert own["rounds_to_fit_cap_tenth"] is None
    assert "never fit 8" in result["falsifier"]["reason"]


def test_round_cost_is_fitted_and_scaled_from_the_step_lines() -> None:
    lives = [100, 200, 400, 800, 1600]
    rounds = [
        score.LogRound(index + 1, {"live": live}, 0, 2, 0.5 * live**1.5, 0.0)
        for index, live in enumerate(lives)
    ]
    fit = score.fit_wall(rounds)
    assert fit is not None
    assert fit["usable"] is True
    assert fit["rounds"] == [2, 3, 4, 5]
    assert fit["alpha"] == pytest.approx(1.5)
    narrow = score.fit_wall(rounds[-1:])
    assert narrow is not None
    assert narrow["usable"] is False
    assert narrow["alpha"] is None
    run = score.Run(
        [{"path": "a.log", "superseded": None}], {r.round: r for r in rounds}, None, 8, []
    )
    result = score.cost(run, None, [16], rss_mb=1000.0)
    projection = result["projections"][0]
    assert projection["live"] == 32
    assert projection["wall_seconds"] == pytest.approx(0.5 * 32**1.5)
    assert projection["rss_mb_if_proportional"] == pytest.approx(20.0)


def test_the_command_line_writes_the_score(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    stuck = [(0.03, BOX, BOX), (0.1003, BOX, BOX)]
    rounds = build([[(1.0, BOX, BOX)] * 2, stuck, stuck])
    log = tmp_path / "run.log"
    log.write_text(log_text(rounds), encoding="utf-8")
    partial = tmp_path / "run.partial.json"
    partial.write_text(json.dumps({"rounds": rounds}), encoding="utf-8")
    target = tmp_path / "radii.json"
    target.write_text(
        json.dumps({"radii": {"xi1": "1/1216", "omega16": "1/1216"}}), encoding="utf-8"
    )
    output = tmp_path / "score.json"
    assert (
        score.main(
            [str(log), "--rounds", str(partial), "--target", str(target), "--json", str(output)]
        )
        == 0
    )
    printed = capsys.readouterr().out
    assert "falsifier: UNDECIDED" in printed
    assert "target at round 2: 0 of 2 coordinates inside [-r, r]" in printed
    written = json.loads(output.read_text(encoding="utf-8"))
    assert written["schema"] == score.SCHEMA
    assert written["falsifier"]["state"] == "UNDECIDED"
    assert written["target"]["coordinates"][0]["name"] == "omega16"


def test_a_real_pilot_round_prints_what_the_scorer_reads(
    capsys: pytest.CaptureFixture[str],
) -> None:
    endpoint = pilot.load_endpoint(pilot.capture_frame(None))
    frame = pilot.capture_frame(endpoint.capture_cap)
    boxed, renumbered = pilot.box_frame(frame, endpoint, Q(1, 64))
    run = pilot.run_pilot(
        boxed,
        renumbered,
        bins=2,
        max_rounds=1,
        max_live=4,
        min_width=Q(1, 64),
        hull_limit=16,
        max_seconds=120,
    )
    assert run.endpoint_lost is None
    segment = score.parse_log(capsys.readouterr().err, "pilot")
    assert len(segment.steps) == 16
    line = segment.lines[1]
    assert {"binding", "fine", "flat"} <= set(line)
    labels, turns = score.n17_owners()
    result = score.score_run(
        score.merge([segment]),
        {entry["round"]: entry for entry in run.rounds},
        labels=labels,
        turns=turns,
    )
    first = result["rounds"][1]
    assert first["disagreements"] == []
    assert first["binding"] == line["binding"]
    assert set(result["rows_needed"]["owners"]) == set(run.rounds[1]["row_to_extent"])
