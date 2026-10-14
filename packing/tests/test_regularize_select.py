"""The owner's choice rule of 13 October 2026, on rows whose exact work is done by fiat.

A view is adoptable when both exact routes accept it, its side is at most `U` and at most
today's drawn side, row 10 admits it, its run draws it, and it is worse than today's
drawing on no measure (light, uneven and near-axis squares, angle classes and hues, house
and stage sides) while better on one or drawn at a smaller side, unless it replaces a
numerically checked witness. Each refusal is named. Among adoptable views the first in
preference order (Evan Daniel's, then grid-slack by rising threshold) that no other
dominates is chosen, and the `layer` commands admit exactly the chosen views: a driver
run whose stored report `layer` would read differently, such as one written before a
same-side view above `U` was set aside, is copied and the copy reclassified first. One
real count (n = 18, drawn from Evan Daniel's view) checks that today's drawing is
measured from the layer a tree holds, and every view the committed layer draws is held to
`U` but at the seven counts policy section 9, question 13 names.
"""

from __future__ import annotations

import gzip
import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from devtools import census_drawing_regularity as census
from devtools import regularize_axis_components as axis
from devtools import regularize_evand as drive
from devtools import regularize_select as select
from sqpack.yamlio import load_yaml
from tests.test_regularize_evand import both_outputs

TODAY = {
    "side": "3",
    "light_axis": 4,
    "uneven_axis": 6,
    "near_axis": 2,
    "classes": 6,
    "hues": 6,
    "house_total": 100,
    "stage_total": 110,
    "house": [0, 0, 0, 0, 25],
    "stage": [0, 0, 0, 0, 25],
    "drawing": {"kind": "regularized-view"},
    "verified": True,
}


def _row(source: str = "grid:a", **overrides: Any) -> dict[str, Any]:
    """A decided candidate: both routes pass, at `U`, admitted, as good as today's."""
    kind = "evand" if source.startswith("evand") else "grid"
    row: dict[str, Any] = {
        "n": 7,
        "source": source,
        "kind": kind,
        "run": f"/runs/{source.split(':')[1]}",
        "rank": 0,
        "output": "solved" if kind == "evand" else "grid",
        "threshold": None if kind == "evand" else 0.5,
        "governing": True,
        "view": True,
        "why": None,
        "routes": {"exact_verify": True, "independent": True},
        "side": "3",
        "upper": "3",
        "s_W": "3",
        "row": 10,
        "decision": "admit",
        "reason": "every admission condition holds",
        "measured": True,
        "measures": {key: TODAY[key] for key in select.MEASURES},
        "measured_against": {"house": TODAY["house"], "stage": TODAY["stage"]},
    }
    measures = overrides.pop("measures", {})
    row.update(overrides)
    row["measures"] = {**row["measures"], **measures}
    return row


def _judged(source: str = "grid:a", **overrides: Any) -> dict[str, Any]:
    return select.judge(_row(source, **overrides), TODAY)


def test_fewer_light_squares_and_more_shared_sides_are_better() -> None:
    view = {**TODAY, "light_axis": 3, "near_axis": 5, "house_total": 101, "stage_total": 109}
    gains, worse = select.compare(view, TODAY)
    assert gains == ["light_axis", "house_total"]
    assert worse == ["near_axis", "stage_total"]


def test_a_measure_either_side_lacks_is_not_compared() -> None:
    gains, worse = select.compare({**TODAY, "house_total": None, "stage_total": 0}, TODAY)
    assert (gains, worse) == ([], ["stage_total"])


def test_dominance_needs_a_gain_and_no_loss() -> None:
    plain = _row()
    better = _row(measures={"house_total": 120})
    mixed = _row(measures={"house_total": 120, "light_axis": 5})
    assert select.dominates(better, plain)
    assert not select.dominates(plain, better)
    assert not select.dominates(mixed, plain)
    assert not select.dominates(plain, plain)


def test_a_view_better_on_one_measure_and_worse_on_none_is_adoptable() -> None:
    judged = _judged(measures={"near_axis": 0})
    assert judged["gains"] == ["near_axis"]
    assert judged["adoptable"]
    assert judged["refusals"] == []


def test_a_view_at_a_smaller_side_is_adoptable_without_a_gain() -> None:
    judged = _judged(side="29/10", upper="29/10")
    assert judged["smaller"]
    assert judged["minus_drawn"] == pytest.approx(-0.1)
    assert judged["adoptable"]


@pytest.mark.parametrize(
    ("overrides", "reason"),
    [
        ({"view": False, "why": "same/False: penetrated"}, "no view: same/False: penetrated"),
        ({"routes": {"exact_verify": True, "independent": False}}, "refused by independent"),
        ({"side": "31/10", "measures": {"near_axis": 0}}, "above U"),
        ({"upper": None, "measures": {"near_axis": 0}}, "U is unknown"),
        (
            {"side": "31/10", "upper": "31/10", "measures": {"near_axis": 0}},
            "above today's drawing's",
        ),
        (
            {
                "row": 7,
                "decision": "review",
                "reason": "for review",
                "measures": {"near_axis": 0},
            },
            "row 7 review: for review",
        ),
        ({"governing": False, "measures": {"near_axis": 0}}, "not the view its run draws"),
        (
            {"measured": False, "measures": {"house_total": None, "stage_total": None}},
            "its contacts were not measured",
        ),
        (
            {"measures": {"near_axis": 0, "stage_total": 109}},
            "worse than today's drawing on stage_total",
        ),
        ({}, "neither better on a measure nor at a smaller side"),
    ],
)
def test_each_reason_a_view_is_refused_is_named(overrides: dict[str, Any], reason: str) -> None:
    judged = _judged(**overrides)
    assert not judged["adoptable"]
    assert any(reason in refusal for refusal in judged["refusals"]), judged["refusals"]


def test_a_closed_form_bound_is_held_exactly_and_not_read_as_unknown() -> None:
    """`regularize_evand.upper_bound` gives `U` only where it is rational. A closed form,
    n = 5's 2 + (1/2)sqrt(2), is stated as the case record writes it and compared with the
    side exactly, as the driver holds it, on either side of it."""
    form = select.stated_bound(5)
    assert form == "2 + (1/2)sqrt(2)"
    below = _judged(side="2707/1000", upper=form, s_W="2707/1000", measures={"near_axis": 0})
    above = _judged(side="2708/1000", upper=form, s_W="2708/1000", measures={"near_axis": 0})
    assert below["below_U"]
    assert below["minus_U"] == pytest.approx(2.707 - (2 + 2**0.5 / 2))
    assert any("register it first" in reason for reason in below["refusals"])
    assert not above["at_most_U"]
    assert any("above U" in reason for reason in above["refusals"])
    assert not any("unknown" in reason for reason in [*below["refusals"], *above["refusals"]])


def test_one_more_hue_at_otherwise_equal_measures_is_worse() -> None:
    """n = 236: two squares turned 0.000537 degrees off their group drew seven hues where
    today's drawing has six, and the other five measures tied."""
    judged = _judged(measures={"classes": 7, "hues": 7, "house_total": 101})
    assert judged["worse"] == ["classes", "hues"]
    assert not judged["adoptable"]
    fewer = _judged(measures={"hues": 5})
    assert fewer["gains"] == ["hues"]
    assert fewer["adoptable"]


def test_a_numerically_checked_witness_is_replaced_by_an_exact_view_with_no_gain() -> None:
    unverified = {**TODAY, "verified": False, "side": None}
    at_u = _row(side="31/10", upper="31/10")
    judged = select.judge(at_u, unverified)
    assert judged["adoptable"]
    assert not judged["smaller"]
    assert judged["minus_drawn"] is None
    assert any("numerically checked witness" in note for note in judged["notes"])
    # Still worse on no measure, and still at most U.
    assert not select.judge({**at_u, "measures": {**at_u["measures"], "hues": 7}}, unverified)[
        "adoptable"
    ]
    assert not select.judge({**at_u, "upper": "3"}, unverified)["adoptable"]
    # Against an exactly verified drawing at a smaller side, the same view is refused.
    assert not select.judge(at_u, TODAY)["adoptable"]


def test_a_run_measured_against_another_drawing_is_noted() -> None:
    other = {"house": [1, 0, 0, 0, 24], "stage": TODAY["stage"]}
    judged = _judged(measured_against=other, measures={"near_axis": 0})
    assert judged["adoptable"]
    assert any("another drawing" in note for note in judged["notes"])


def test_the_first_view_no_other_dominates_is_chosen_in_preference_order() -> None:
    evand = _judged("evand:bound:solved", measures={"house_total": 105})
    half = _judged("grid:half", threshold=0.5, measures={"house_total": 110})
    five = _judged("grid:five", threshold=5.0, measures={"house_total": 110, "near_axis": 0})
    assert select.choose([five, half, evand]) is five
    # A grid view better on one measure and worse on another dominates nothing, so
    # Evan Daniel's comes first.
    mixed = _judged("grid:half", measures={"house_total": 110, "light_axis": 5})
    assert select.choose([mixed, evand]) is evand
    # Among grid-slack views none dominates, the lowest threshold is first.
    one = _judged("grid:one", threshold=1.0, measures={"near_axis": 0, "light_axis": 5})
    assert select.choose([one, half]) is half


def test_a_view_that_is_not_adoptable_neither_wins_nor_dominates() -> None:
    evand = _judged("evand:bound:solved", measures={"near_axis": 0})
    held = _judged("grid:half", row=7, decision="review", measures={"house_total": 200})
    assert select.choose([held, evand]) is evand
    assert select.choose([held]) is None


def test_preference_puts_evand_first_then_grid_slack_by_rising_threshold() -> None:
    rows = [
        _row("grid:five", threshold=5.0),
        _row("grid:half-b", threshold=0.5, rank=1),
        _row("evand:bound:solved", rank=1),
        _row("grid:half-a", threshold=0.5, rank=0),
        _row("evand:atU:solved", rank=0),
    ]
    ordered = [row["source"] for row in sorted(rows, key=select.preference)]
    assert ordered == [
        "evand:atU:solved",
        "evand:bound:solved",
        "grid:half-a",
        "grid:half-b",
        "grid:five",
    ]


def test_register_candidates_are_exactly_verified_views_below_u() -> None:
    below = _judged(side="29/10", measures={"near_axis": 0})
    refused = _judged(side="29/10", routes={"exact_verify": False, "independent": True})
    at_u = _judged()
    assert any("register it first" in reason for reason in below["refusals"])
    listed = select.register_candidates([below, refused, at_u])
    assert [row["source"] for row in listed] == ["grid:a"]
    assert listed[0]["minus_U"] == pytest.approx(-0.1)


def _evand(n: int, run: str, *, decision: str = "admit", stale: bool = False) -> dict[str, Any]:
    return {
        "n": n,
        "kind": "evand",
        "run": run,
        "governing_decision": decision,
        "stored_decision": decision,
        "stale": stale,
    }


def test_layer_commands_admit_exactly_the_chosen_views() -> None:
    rows = [_evand(87, "/r/a"), _evand(110, "/r/a"), _evand(301, "/r/b"), _evand(5, "/r/c")]
    chosen = [
        {"n": 87, "kind": "evand", "run": "/r/a"},
        {"n": 301, "kind": "evand", "run": "/r/b"},
        {"n": 146, "kind": "grid", "run": "/r/deg5", "threshold": 5.0},
        {"n": 176, "kind": "grid", "run": "/r/deg5", "threshold": 5.0},
        {"n": 271, "kind": "grid", "run": "/r/deg05", "threshold": 0.5},
    ]
    layer = "python -m devtools.regularize_evand layer"
    empty = '--run-dir "$(mktemp -d)" --repo-root ..'
    assert select.layer_commands(chosen, rows) == [
        f"{layer} --run-dir /r/a /r/b --repo-root .. --exclude 110",
        f"{layer} {empty} --grid-run /r/deg05 --grid-counts 271",
        f"{layer} {empty} --grid-run /r/deg5 --grid-counts 146 176",
    ]


def test_a_count_two_evand_runs_report_is_admitted_run_by_run() -> None:
    """`layer` lets a later run's report of a count replace an earlier one's, admitted or
    not, so runs that share a chosen count are admitted one by one."""
    layer = "python -m devtools.regularize_evand layer"
    reclassify = "python -m devtools.regularize_evand reclassify"
    chosen = [
        {"n": 87, "kind": "evand", "run": "/r/a", "rank": 0},
        {"n": 301, "kind": "evand", "run": "/r/b", "rank": 1},
    ]
    admitted = [_evand(87, "/r/a"), _evand(87, "/r/b"), _evand(301, "/r/b", stale=True)]
    # The stale run is copied, the copy decided again and admitted from.
    assert select.layer_commands(chosen, admitted) == [
        'copies="$(mktemp -d)"',
        'mkdir "$copies/0" && cp -R /r/b "$copies/0/b"',
        f'{reclassify} --run-dir "$copies/0/b" --refresh-bounds',
        f"{layer} --run-dir /r/a --repo-root ..",
        f'{layer} --run-dir "$copies/0/b" --repo-root .. --exclude 87',
    ]
    held = [_evand(87, "/r/a"), _evand(87, "/r/b", decision="review"), _evand(301, "/r/b")]
    assert select.layer_commands(chosen, held) == [
        f"{layer} --run-dir /r/a --repo-root ..",
        f"{layer} --run-dir /r/b --repo-root ..",
    ]


BOUND_FACTS = {
    "verified_upper_bound": "5.62",
    "exact_form": None,
    "reported": "5.62",
    "found_by": [],
    "improved_by": [],
    "source_key": None,
}


def _written_before_the_yield(tmp_path: Path) -> Path:
    """A driver run of n = 26 as the driver wrote it before `yield_to_bound`: the
    same-side view, above `U`, decided and admitted, and the view at exactly `U` measured
    beside it (`test_regularize_evand.both_outputs`; #580 review B1)."""
    report = both_outputs(same_side="563/100", solved_side="281/50", bound="5.62")
    beside = report["outputs"]["solved"]
    for measured in (report, beside):
        # As the driver writes them: a decimal largest move and the regressions found.
        measured["identity"] = {**measured["identity"], "max_move": "0.1"}
        measured["shades"] = {**measured["shades"], "regressions": []}
    report["regularize"] = {"level": 2}
    report["source"] = {**report["source"], "provenance": {"source_key": None}}
    same = drive.measured_from_report(report, "same")
    drive.decide(report, drive.measured_from_report(report, "solved"), same)
    report["regularization"] = drive.regularization_record(report)
    run = tmp_path / "evand-1012"
    (run / "n-026").mkdir(parents=True)
    (run / "n-026" / "report.json").write_text(json.dumps(report), encoding="utf-8")
    receipt = {"counts": [drive.receipt_row(report)], "cost": {"cpu_seconds": 1.0}}
    (run / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
    return run


def test_a_run_written_before_the_yield_is_reclassified_on_a_copy_before_layer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The selection decides a count as `reclassify --refresh-bounds` would, and `layer`
    reads the stored report: where they would draw different views, the printed commands
    copy the run, reclassify the copy and admit from it, so `layer` draws the chosen view
    and the run stays as it was decided."""
    monkeypatch.setattr(drive, "case_facts", lambda _n: dict(BOUND_FACTS))
    run = _written_before_the_yield(tmp_path / "runs")
    stored = drive.read_json(run / "n-026" / "report.json")
    assert (stored["decision"]["row"], stored["decision"]["decision"]) == (10, "admit")
    assert drive.layer_candidate(stored, "admitted") == "same"

    rows = select.evand_candidates(select.Job("evand", run, 26, 0))
    assert {row["governing_output"] for row in rows} == {"solved"}
    assert {row["governing_decision"] for row in rows} == {"admit"}
    assert all(row["stale"] for row in rows)
    chosen = [{"n": 26, "kind": "evand", "run": str(run), "rank": 0}]
    commands = select.layer_commands(chosen, rows)
    prefix = "python -m devtools.regularize_evand"
    copy = '"$copies/0/evand-1012"'
    assert commands == [
        'copies="$(mktemp -d)"',
        f'mkdir "$copies/0" && cp -R {run} {copy}',
        f"{prefix} reclassify --run-dir {copy} --refresh-bounds",
        f"{prefix} layer --run-dir {copy} --repo-root ..",
    ]
    # The copy keeps the run's name, which `layer` records it by, however it is spelled.
    assert select.copy_of(1, "/r/my run") == "\"$copies/1/\"'my run'"

    # What the commands do: the copy, decided again, admits the view the selection chose.
    before = (run / "n-026" / "report.json").read_bytes()
    copied = tmp_path / "copies" / "0" / run.name
    shutil.copytree(run, copied)
    drive.reclassify(copied, refresh_bounds=True)
    redone = drive.read_json(copied / "n-026" / "report.json")
    assert drive.layer_candidate(redone, "admitted") == "solved"
    assert (run / "n-026" / "report.json").read_bytes() == before


def test_a_run_decided_as_the_table_now_decides_is_admitted_as_it_stands(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(drive, "case_facts", lambda _n: dict(BOUND_FACTS))
    run = _written_before_the_yield(tmp_path)
    drive.reclassify(run, refresh_bounds=True)
    rows = select.evand_candidates(select.Job("evand", run, 26, 0))
    assert not any(row["stale"] for row in rows)
    chosen = [{"n": 26, "kind": "evand", "run": str(run), "rank": 0}]
    assert select.layer_commands(chosen, rows) == [
        f"python -m devtools.regularize_evand layer --run-dir {run} --repo-root .."
    ]


def test_today_is_the_view_a_tree_draws_measured_like_a_candidate() -> None:
    drawn = select.today((select.REPO, 18, census.read_index(select.REPO)))
    assert drawn["drawing"]["kind"] == "regularized-view"
    assert drawn["side"] is not None
    assert drawn["house_total"] == sum(k * count for k, count in enumerate(drawn["house"]))
    assert drawn["verified"]
    assert drawn["hues"] >= 1
    assert drawn["classes"] >= drawn["hues"]


def test_every_drawn_view_is_at_most_the_bound_but_the_named_exceptions() -> None:
    """Owner, 13 October 2026: a drawn view is exactly verified at a side no larger than
    `U` (question 13). Each drawn view's side is read from its view file, exactly as both
    routes decide it, and held to `U` exactly as the driver holds it, a closed form as the
    root it is. The views above it are the exceptions question 13 names (#580 review B2),
    which `--check-atlas` also holds the layer to: the one list, `axis.ABOVE_U`."""
    index = drive.read_json(drive.LAYER_INDEX)
    above: dict[int, float] = {}
    for entry in index["entries"]:
        if entry["status"] != "regularized":
            continue
        n = int(entry["n"])
        text = gzip.decompress((select.REPO / entry["view"]["path"]).read_bytes())
        side, _placements, _corners = drive.view_geometry(load_yaml(text.decode())["witness"])
        bound = drive.verified_bound(drive.case_facts(n))
        assert bound is not None, f"n={n}: U is unknown"
        order = bound.compare(side)
        assert order is not None, f"n={n}: U is not read exactly: {bound.unread}"
        if order > 0:
            above[n] = bound.difference(side)
    assert sorted(above) == sorted(axis.ABOVE_U) == [18, 26, 66, 85, 110, 241, 297], above
    # A rounding sliver above the best known side at each, never another packing's side.
    assert max(above.values()) < 1e-10
