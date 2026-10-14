# ruff: noqa: RUF001 -- these tests read case-record prose, whose typography uses curly
# apostrophes, as the layer that writes it does.
"""The regularized views registered as verified upper bounds (T-155, T-156).

`devtools.register_regularized_bounds` retains each view whose exact side lies below its
case's verified upper bound, decides it on both maintained exact routes, makes three
controls of it, and writes the case records' verified upper lane. These tests hold the
committed receipts, the retained views and the case records to each other, the layer to
its own output, and the controls' construction to the outcomes it promises. The first
batch (T-155) is Evan Daniel's regularizer's views; the second (T-156) is the grid-slack
view of n = 290, held to the same receipts in its own words.
"""

from __future__ import annotations

import dataclasses
import gzip
import json
import re
from collections.abc import Callable
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import apply_exact_ceilings, render_case_verifiers
from devtools import register_regularized_bounds as registered
from devtools.apply_upper_bound_packets import normalized
from sqpack.assurance import bounds_agree_at_declared_precision


def _held() -> dict[int, dict[str, Any]]:
    """The first batch's rows whose case record this layer still writes: a count a later
    house adoption holds keeps the view as history (`registered.readopted`)."""
    return {n: row for n, row in registered.committed().items() if not registered.readopted(n)}


def test_the_receipts_the_views_and_the_records_agree() -> None:
    assert registered.problems() == []


def test_no_held_or_rehoused_count_is_registered() -> None:
    selection = json.loads(registered.FIRST.selection.read_text(encoding="utf-8"))
    assert 17 not in registered.committed()
    assert not set(registered.committed()) & registered.EXCLUDED
    assert set(selection["registered"]) == set(selection["candidates"]) - registered.EXCLUDED
    assert len(registered.REHOUSED) == 42


def test_each_side_lies_below_the_bound_it_replaced_and_at_or_below_t101s_side() -> None:
    """The registered side is below the ceiling the record held, never above the side of
    the earlier exact certificate of the same packing, and above the catalogue's closed
    form wherever it prints one: a ceiling of the same packing, not a smaller one."""
    for n, row in registered.committed().items():
        side = Fraction(row["side"])
        earlier = apply_exact_ceilings.bound_value(row["earlier_verified"])
        assert side < earlier, n
        if row["t101_side"] is not None:
            assert side <= Fraction(row["t101_side"]), n
        if row["printed_exact_form"]:
            assert row["above_exact_side_by"] > 0, n
        assert Fraction(Decimal(row["value"])) >= side, n


def test_prose_writes_a_side_exactly_where_it_ends_and_rounded_up_where_it_does_not() -> None:
    assert registered.side_text(Fraction(11, 2)) == "5.5"
    assert registered.side_text(Fraction(1, 3)) == "0." + "3" * 35 + "4"
    assert registered.side_text(Fraction(1, 2**40)) == format(
        registered.ceiling_decimal(Fraction(1, 2**40), registered.DISPLAY_PLACES), "f"
    )


def test_the_printed_value_stays_unless_it_would_fall_below_the_side() -> None:
    assert registered.printed_value("6.59861960924437", Fraction("6.598619609244360116")) == (
        "6.59861960924437",
        False,
    )
    assert registered.printed_value("6.59861960924436", Fraction("6.598619609244360116")) == (
        "6.59861960924437",
        True,
    )


def test_each_record_prints_its_earlier_decimal_beside_the_exact_side() -> None:
    """The value is the decimal the record printed before, an upper display of the new
    exact form; no count needed it raised, and agreement with the report is unchanged."""
    for n, row in _held().items():
        upper = registered.case_front(n)["verified_upper_bound"]
        assert upper["value"] == row["earlier_verified"]["value"], n
        assert not row["value_raised"], n
        assert Fraction(Decimal(upper["value"])) >= Fraction(upper["exact_form"]), n
        assert Fraction(upper["exact_form"]) == Fraction(row["side"]), n


@pytest.mark.parametrize("n", [28, 29, 37, 50, 204, 290, 300])
def test_the_records_are_the_layer_applied_to_themselves(n: int) -> None:
    path = registered.FRONTIER / f"n-{n:03d}.md"
    text = path.read_text(encoding="utf-8")
    rendered = render_case_verifiers.refresh(registered.apply_case(n, text))
    assert normalized(rendered) == normalized(text)


@pytest.mark.parametrize("n", [28, 50, 69, 300])
def test_the_t101_layer_leaves_a_record_this_layer_owns(n: int) -> None:
    path = registered.FRONTIER / f"n-{n:03d}.md"
    text = path.read_text(encoding="utf-8")
    assert apply_exact_ceilings.apply_case(n, text) == text


def test_each_record_says_whether_its_bound_agrees_with_the_report() -> None:
    """A bound that disagrees with the report at the declared precision carries the
    ceiling section and a `mathematics` blocker; one that agrees carries neither."""
    for n, row in _held().items():
        case = registered.case_front(n)
        agrees = bounds_agree_at_declared_precision(
            case["reported_upper_bound"], case["verified_upper_bound"]
        )
        assert agrees == row["agrees_with_report"], n
        body = (registered.FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
        assert (registered.CEILING_HEADING in body) != agrees, n
        assert registered.SECTION in body, n
        assert registered.FIRST.dated in body, n


def test_a_count_a_later_house_holds_keeps_the_view_as_history() -> None:
    """At n = 264 issue 528's packing (T-158) was adopted on 12 October 2026, below T-155's
    view: the record's verified upper bound is the house's, this layer leaves the record as
    it is, and the view's dated paragraph and section say it held until that day."""
    assert [n for n in registered.committed() if registered.readopted(n)] == [264]
    assert registered.readopted_by(264, "T-155")
    assert not registered.readopted_by(264, "T-156")
    row = registered.committed()[264]
    assert Fraction(registered.case_front(264)["verified_upper_bound"]["exact_form"]) < (
        Fraction(row["side"])
    )
    text = (registered.FRONTIER / "n-264.md").read_text(encoding="utf-8")
    assert registered.apply_case(264, text) == text
    flat = _flat(264)
    assert registered.FIRST.dated in flat
    assert "The verified upper bound was that side exactly until 12 October 2026" in flat
    assert (
        "That side was the exact form of the case’s `verified_upper_bound` until 12 October "
        "2026, which cited both certificates (T-101, T-155)"
    ) in flat


def test_every_control_reached_its_outcome_on_both_routes() -> None:
    receipt = json.loads(registered.FIRST.controls.read_text(encoding="utf-8"))
    assert receipt["all_as_expected"]
    by_count: dict[int, set[str]] = {}
    for row in receipt["rows"]:
        by_count.setdefault(row["n"], set()).add(row["control"])
        if row["expect"] == "refused":
            assert not row["exact_verify"], row
            assert not row["independent"], row
    assert set(by_count) == set(registered.committed())
    assert all(len(kinds) == 3 for kinds in by_count.values())


def _two_squares(side: Fraction) -> dict[str, object]:
    """Two touching axis-parallel unit squares on the floor of a box of `side`."""
    return {
        "id": "W-control-pair",
        "n": 2,
        "side": registered.literal(side),
        "square_size": "1",
        "representation": "center-basis",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {"id": 1, "center": ["1/2", "1/2"], "basis": ["1", "0"]},
            {"id": 2, "center": ["3/2", "1/2"], "basis": ["1", "0"]},
        ],
        "claim": {
            "coordinate_provenance": "verified",
            "method": "exact-algebraic",
            "limitations": "A test fixture.",
        },
    }


def test_the_controls_refuse_an_overlap_and_a_shrink_and_accept_one_unit() -> None:
    view = _two_squares(Fraction(23, 10))
    assert registered.decide_view(view)["exact_verify"]["passed"]
    from sqpack.witness import exact_verify  # noqa: PLC0415

    outcomes = []
    for mutant, row in registered.control_views(view):
        first, _report = exact_verify(mutant)
        side, corners = registered.corners_of(mutant)
        second = registered.independent.check_squares(corners, side)
        outcomes.append(
            (
                row["control"],
                row["expect"],
                first["verification_passed"],
                second["verification_passed"],
            )
        )
    assert outcomes == [
        ("tightest-pair-overlapped", "refused", False, False),
        ("side-shrunk-past-clearance", "refused", False, False),
        ("side-shrunk-one-unit", "accepted", True, True),
    ]


def test_a_trailing_blocker_names_the_gap_and_what_would_close_it() -> None:
    row = {
        "side": "5.824444616674059297016873205016",
        "side_text": "5.824444616674059297016873205016",
        "t101_side": None,
        "value": "5.824444616674059297016873205016",
        "printed_side": "5.82444461667405",
        "printed_exact_form": None,
        "printed_exact_form_degree": None,
        "above_exact_side_by": None,
    }
    blocker = registered.trailing_blocker(row, ["E-kingbird-upper-register"])
    assert blocker["kind"] == "mathematics"
    assert "9.297016873205016e-15" in blocker["detail"]
    assert blocker["evidence"] == ["E-kingbird-upper-register"]


def test_t101s_replays_stay_cited_where_they_prove_the_same_side() -> None:
    """At the 33 counts whose registered side is exactly the side of Evan Daniel's earlier
    certificate (T-101), T-101's replays prove the same bound, the independent one among
    them, so the lane cites them first and this layer's decision after; elsewhere this
    layer's decision alone proves the side (PR #549, review B2)."""
    same = [n for n, row in registered.committed().items() if registered.at_t101_side(row)]
    assert len(same) == 33
    replays = [apply_exact_ceilings.EXACT_REPLAY, apply_exact_ceilings.SOURCE_REPLAY]
    for n in _held():
        evidence = registered.case_front(n)["verified_upper_bound"]["evidence"]
        assert evidence == (
            [*replays, registered.EVIDENCE] if n in same else [registered.EVIDENCE]
        ), n


def _flat(n: int) -> str:
    """A record's text with the formatter's line breaks folded into spaces."""
    return " ".join((registered.FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8").split())


def test_prose_calls_a_side_exact_only_where_its_decimal_is_the_side() -> None:
    """Where the side's decimal never ends within the places prose writes, the decimal is
    the side rounded up and is never called the side exactly, its exact side or the exact
    form; where it ends, the ceiling section still says exactly (review B3)."""
    rounded = []
    for n, row in registered.committed().items():
        text, shown = _flat(n), re.escape(row["side_text"])
        if registered.rounded_up(Fraction(row["side"])):
            rounded.append(n)
            assert not re.search(rf"{shown}\$?, exactly", text), n
            assert not re.search(rf"exact side, {shown}", text), n
            assert not re.search(
                rf"{shown}\$?, the verified upper bound \(T-155\), the exact", text
            ), n
            assert f"{row['side_text']}$ (rounded up at 36 places)" in text, n
            assert "the verified upper bound (T-155) rounded up at 36 places" in text, n
        else:
            assert "rounded up at 36 places" not in text, n
            if not row["agrees_with_report"]:
                assert re.search(rf"{shown}\$, exactly", text), n
    assert rounded == [41, 53, 54, 71, 128, 178, 300]


def test_a_trailing_blocker_of_a_rounded_side_does_not_call_it_exact() -> None:
    row = {
        "side": "22/3",
        "side_text": registered.side_text(Fraction(22, 3)),
        "t101_side": None,
        "value": "7.33333333333334",
        "printed_side": "7.33333333333333",
        "printed_exact_form": None,
        "printed_exact_form_degree": None,
        "above_exact_side_by": None,
    }
    detail = registered.trailing_blocker(row, ["E-kingbird-upper-register"])["detail"]
    assert f"exact side, {row['side_text']}," not in detail
    assert f"({row['side_text']} rounded up at 36 places)" in detail


def test_a_view_not_paired_with_its_witness_is_not_called_its_arrangement() -> None:
    """Where nearest centres do not pair the view's squares one to one with the witness's,
    its identity with the credited packing is undecided, and the dated paragraph says the
    view was made from the witness, not that it is the arrangement (review B5)."""
    for n, row in registered.committed().items():
        text = _flat(n)
        paired = row["identity"]["one_to_one"]
        assert ("exact rational packing of this arrangement" in text) == paired, n
        assert ("exact rational packing from that witness" in text) == (not paired), n
    assert [
        n for n, row in registered.committed().items() if not row["identity"]["one_to_one"]
    ] == [204, 299]


@pytest.mark.parametrize(
    ("n", "sentence", "reworded"),
    [
        (
            28,
            r"the\s+verified\s+upper\s+bound\s+from\s+6\s+to\s+12\s+October\s+2026\s+\(T-101\)",
            "a ceiling then (T-101)",
        ),
        (
            28,
            r"the\s+verified\s+upper\s+bound\s+until\s+12\s+October\s+2026:",
            "a ceiling then:",
        ),
        (
            28,
            r"Its\s+rounded-up\s+side\s+and\s+the\s+printed\s+side\s+agree\s+to\s+one",
            "They agree to one",
        ),
        (29, r"own\s+interval\s+certificate\s+verified", "own interval certificate showed"),
    ],
)
def test_a_reworded_earlier_sentence_is_refused_rather_than_left_present(
    n: int, sentence: str, reworded: str
) -> None:
    """An earlier layer's sentence this layer puts in the past must be found in one tense or
    the other; reworded past both, the record is refused, since a sentence no longer
    matched would keep calling a superseded ceiling the verified upper bound (review A3)."""
    text = (registered.FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    changed, count = re.subn(sentence, reworded, text)
    assert count == 1
    with pytest.raises(registered.RegistrationError, match=f"n={n}: neither"):
        registered.apply_case(n, changed)


def test_the_least_row_three_view_is_registered_and_its_choice_checked() -> None:
    """`select` keeps every row-3 output's side beside the one it takes, the least, and
    `problems` holds a row to it; a row of the first selection, which records no such
    sides, is held to the same-side view's side, the witness's own (review A4)."""
    report = {
        "decisions": {"same": {"row": 3}, "solved": {"row": 3}},
        "outputs": {"same": {"side_exact": "7/2"}, "solved": {"side_exact": "13/4"}},
    }
    assert registered.least_output(report) == ("solved", {"same": "7/2", "solved": "13/4"})
    base = {"side": "13/4", "output": "solved", "outputs_at_row_3": ["same", "solved"]}
    assert (
        registered.least_view_problems(
            1, {**base, "row_three_sides": {"same": "7/2", "solved": "13/4"}}
        )
        == []
    )
    assert registered.least_view_problems(
        1,
        {
            **base,
            "side": "7/2",
            "output": "same",
            "row_three_sides": {"same": "7/2", "solved": "13/4"},
        },
    ) == ["n=1: the registered view is not the least row-3 output"]
    assert registered.least_view_problems(1, {**base, "witness_side": "7/2"}) == []
    assert registered.least_view_problems(1, {**base, "witness_side": "3"}) == [
        "n=1: the registered view lies above the same-side view"
    ]
    # A grid-slack row keys its sides by run, not by output (PR #587, review A5).
    grid = {"side": "13/4", "output": "same", "witness_side": "13/4"}
    assert (
        registered.least_view_problems(
            1, {**grid, "runs_at_row_3": ["a", "b"], "run_sides": {"a": "13/4", "b": "7/2"}}
        )
        == []
    )
    assert registered.least_view_problems(
        1, {**grid, "runs_at_row_3": ["a", "b"], "run_sides": {"a": "13/4", "b": "3"}}
    ) == ["n=1: the registered view is not the least row-3 output"]
    assert registered.least_view_problems(
        1, {**grid, "runs_at_row_3": ["a"], "run_sides": {"a": "13/4", "b": "7/2"}}
    ) == ["n=1: the recorded sides are not the row-3 views'"]


def test_the_controls_are_151_distinct_mutants() -> None:
    """At a same-side view the least top or right clearance is 0, so the box shrunk past it
    is the box shrunk by one unit: the 177 decisions are of 151 distinct mutants, as the
    evidence entry and the package README say (review B6)."""
    receipt = json.loads(registered.FIRST.controls.read_text(encoding="utf-8"))
    touching = {
        row["n"]
        for row in receipt["rows"]
        if row["control"] == "side-shrunk-past-clearance" and row["clearance"] == 0
    }
    assert touching == {
        n for n, row in registered.committed().items() if row["output"] == "same"
    }
    assert receipt["controls"] - len(touching) == 151


# --------------------------------------------------------------------------------------
# The second batch: the grid-slack view of n = 290 (T-156)
# --------------------------------------------------------------------------------------


def test_the_second_batch_receipts_view_and_record_agree() -> None:
    assert registered.problems(registered.GRID) == []
    assert registered.counts(registered.GRID) == (290,)
    assert not set(registered.committed()) & set(registered.committed(registered.GRID))
    assert registered.batch_of(290) == registered.GRID
    assert registered.batch_of(291) == registered.FIRST


def test_n290_is_registered_at_the_witnesss_side_below_t101s_and_draws_nothing_new() -> None:
    """The owner's rule of 13 October 2026: a new upper bound is a result. The view at
    n = 290 is the witness's own side, 2.4e-15 below the ceiling the record held and
    below the side of Evan Daniel's certificate of the same packing (T-101), above the
    catalogue's closed form, and it draws no change before registration or after."""
    row = registered.committed(registered.GRID)[290]
    side = Fraction(row["side"])
    assert side == Fraction(row["witness_side"])
    assert side == Fraction("70142135623730950488016887242097/4000000000000000000000000000000")
    assert side < apply_exact_ceilings.bound_value(row["earlier_verified"])
    assert side < Fraction(row["t101_side"])
    assert row["above_exact_side_by"] > 0
    assert row["decided"]["row"] == 3
    assert row["drawing"] == row["after_registration"]["decision"] == "no-change"
    assert row["identity"]["one_to_one"]
    assert row["identity"]["moved"] == 0
    assert row["regularization"]["of"] == "T-101"
    assert set(row["run_sides"]) == set(row["runs_at_row_3"])
    upper = registered.case_front(290)["verified_upper_bound"]
    assert upper == {
        "value": "17.53553390593274",
        "exact_form": row["side"],
        "evidence": [registered.GRID.evidence],
    }


def test_the_second_batchs_record_names_its_result_and_its_generator() -> None:
    text = _flat(290)
    assert registered.GRID.dated in text
    assert registered.FIRST.dated not in text
    assert "the verified upper bound (T-156)" in text
    # T-155 is named only where the record says its n = 291 certificate implied the bound:
    # the dated paragraph, the section and the regularization note (review C1).
    assert text.count("T-155") == 3
    assert "grid-slack regularizer" in text
    assert "the verified upper bound from 6 to 13 October 2026 (T-101)" in text
    assert f"]({registered.GRID.link})" in text


def test_the_second_batchs_controls_reached_their_outcomes() -> None:
    receipt = json.loads(registered.GRID.controls.read_text(encoding="utf-8"))
    assert receipt["all_as_expected"]
    assert {row["control"] for row in receipt["rows"]} == {
        "tightest-pair-overlapped",
        "side-shrunk-past-clearance",
        "side-shrunk-one-unit",
    }
    # The view touches the top or right wall, so the one-unit shrink is refused too.
    assert all(not row["exact_verify"] and not row["independent"] for row in receipt["rows"])


def test_the_grid_batch_refuses_a_count_the_first_batch_registers(tmp_path: Path) -> None:
    with pytest.raises(registered.RegistrationError, match="registered by T-155"):
        registered.select_grid([tmp_path], [291])
    with pytest.raises(registered.RegistrationError, match="held"):
        registered.select_grid([tmp_path], [17])
    with pytest.raises(registered.RegistrationError, match="no named run reports"):
        registered.select_grid([tmp_path], [290])


def test_n290s_bound_already_followed_from_t155s_certificate_at_n291() -> None:
    """`s(290) ≤ s(291)`, and T-155 certified n = 291 at exactly the side T-156 registers,
    so the bound was not new; the owner kept T-156 as the certificate of 290's own packing
    and the record says both (PR #587, review B1)."""
    row = registered.committed(registered.GRID)[290]
    side = Fraction(row["side"])
    implied = {
        "n": 291,
        "side": row["side"],
        "evidence": [registered.EVIDENCE],
        "results": ["T-155"],
    }
    assert row["implied_by"] == implied
    assert registered.implied_by(290, side) == implied
    assert registered.implied_by(290, side - Fraction(1, 10**40)) is None
    assert Fraction(registered.committed()[291]["side"]) == side
    text = _flat(290)
    assert (
        "The bound was not new: the certificate registered at $n = 291$ (T-155), at the "
        "same side, already proved it by monotonicity; this one certifies this count’s own "
        "packing."
    ) in text
    assert "and $s(290) \\le s(291)$, since deleting a square from a packing of 291" in text
    # The first batch's rows record no implication, and their records say none.
    assert not any("implied_by" in each for each in registered.committed().values())
    # T-156 cites the evidence of the ceiling that implies its bound, as T-002 and T-016
    # cite their parents', so its derived route is in the register (review C2).
    assert registered.results_holding(290, implied["evidence"]) == ["T-156"]


def test_a_second_grid_slack_batch_is_written_in_grid_slack_words(tmp_path: Path) -> None:
    """What a batch writes follows its generator kind, not its identity: a later
    grid-slack batch gets the grid-slack prose, its own result and date, and no KeyError
    (PR #587, review A1)."""
    later = dataclasses.replace(
        registered.GRID,
        name="grid-slack-2",
        result="T-999",
        evidence="E-later-grid-slack",
        registered="2026-10-20",
        date_words="20 October 2026",
        package=tmp_path,
        anchor="",
    )
    row = registered.committed(registered.GRID)[290]
    dated = registered.dated_paragraph(290, row, later)
    assert dated.startswith(
        "**Exact regularized certificate, 2026-10-20.** This project’s grid-slack regularizer"
    )
    assert "the verified upper bound (T-999)" in dated
    written = registered.section(290, row, later)
    assert "for this count on 20 October 2026" in written
    assert "Evan Daniel’s exact solver and regularizer" not in written
    assert "regularization pass of" not in written
    assert later.command("select").endswith("select --batch grid-slack-2")
    # Its select refuses a count another batch registers, naming that batch's result.
    with pytest.raises(registered.RegistrationError, match="registered by T-156"):
        registered.select_grid([tmp_path], [290], later)


@pytest.mark.parametrize(
    "argv",
    [
        ["select", "--run-dir", "RUN", "--n", "290"],
        ["decide", "--n", "290"],
        ["controls", "--batch", "grid-slack", "--run-dir", "RUN"],
        ["--check", "--n", "290"],
    ],
)
def test_run_dirs_and_counts_are_refused_outside_their_select(
    argv: list[str], tmp_path: Path
) -> None:
    """`--n` names a grid-slack batch's counts and `--run-dir` its runs: given to the first
    batch's `select` or to any other command, they are refused rather than ignored, and
    nothing runs (PR #587, review A3)."""
    with pytest.raises(SystemExit) as raised:
        registered.main([str(tmp_path) if each == "RUN" else each for each in argv])
    assert raised.value.code == 2


# --------------------------------------------------------------------------------------
# The grid batch's refusals, on synthetic run directories built from the retained view.
# `select_grid` writes nothing, so none of these touches the checkout (review B6).
# --------------------------------------------------------------------------------------


def _retained() -> bytes:
    return gzip.decompress(registered.view_path(290, registered.GRID).read_bytes())


def _grid_report() -> dict[str, object]:
    """A grid-slack report of n = 290 carrying what `select_grid` reads, at the view's
    side, decided at row 3 against the record's earlier bound."""
    row = registered.committed(registered.GRID)[290]
    return {
        "n": 290,
        "generator": "regularize_grid_slack/1",
        "settings": dict(row["generator"]["settings"]),
        "seconds": 1.0,
        "straightened": [],
        "attempts": [
            {
                "exact": {
                    "side": row["side"],
                    "relation": "same",
                    "verdicts": {
                        "exact_verify": {"passed": True},
                        "independent": {"passed": True},
                    },
                }
            }
        ],
        "measured": {
            "identity": {"one_to_one": True, "max_move": "6e-31", "unnamed_turns": []},
            "shades": {"regressions": []},
            "visible_change": False,
            "totals_fall": False,
        },
    }


def _grid_run(root: Path, name: str, report: object, view: bytes) -> Path:
    directory = root / name / "n-290"
    directory.mkdir(parents=True)
    (directory / "report.json").write_text(json.dumps(report), encoding="utf-8")
    (directory / "view.yaml.gz").write_bytes(gzip.compress(view, mtime=0))
    return directory.parent


def _side_above(report: dict, view: bytes) -> tuple[dict, bytes]:
    row = registered.committed(registered.GRID)[290]
    above = Fraction(row["side"]) + Fraction(1, 10**20)
    report["attempts"][0]["exact"]["side"] = registered.literal(above)
    text = view.decode("utf-8")
    stated = f"  side: {row['side']}\n"
    assert text.count(stated) == 1
    return report, text.replace(stated, f"  side: {registered.literal(above)}\n").encode()


def _derived_elsewhere(report: dict, view: bytes) -> tuple[dict, bytes]:
    text = view.decode("utf-8")
    assert text.count("derived_from: W-known-best-n290") == 1
    return report, text.replace(
        "derived_from: W-known-best-n290", "derived_from: W-known-best-n291"
    ).encode()


def _labelled_bound(report: dict, view: bytes) -> tuple[dict, bytes]:
    report["attempts"][0]["exact"]["relation"] = "bound"
    return report, view


def _other_generator(report: dict, view: bytes) -> tuple[dict, bytes]:
    report["generator"] = "regularize_evand/3"
    return report, view


def _route_refused(report: dict, view: bytes) -> tuple[dict, bytes]:
    report["attempts"][0]["exact"]["verdicts"]["independent"]["passed"] = False
    return report, view


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            _derived_elsewhere,
            (
                "n=290: the view was derived from W-known-best-n291, not the checkout's "
                "witness W-known-best-n290"
            ),
        ),
        (_side_above, "n=290: the view's side is not the checkout witness's own s_W"),
        (_labelled_bound, "n=290: the run labels its row-3 view 'bound', not the same-side"),
        (_other_generator, "n=290: run holds a view of regularize_evand/3, not of"),
        # A route the run refused demotes the view below row 3 (review B7).
        (_route_refused, "n=290: no named run's view is decided at row 3"),
    ],
)
def test_the_grid_batch_refuses_each_view_it_cannot_register(
    tmp_path: Path,
    mutate: Callable[[dict, bytes], tuple[dict, bytes]],
    message: str,
) -> None:
    """Each refusal the package README promises, one field changed at a time from a run
    directory that is otherwise the retained view's (PR #587, review B2); each message
    names its own cause (review B4)."""
    report, view = mutate(_grid_report(), _retained())
    run = _grid_run(tmp_path, "run", report, view)
    with pytest.raises(registered.RegistrationError, match=re.escape(message)):
        registered.select_grid([run], [290])


def test_the_grid_batch_refuses_two_runs_of_one_name(tmp_path: Path) -> None:
    first = _grid_run(tmp_path / "a", "same", _grid_report(), _retained())
    second = _grid_run(tmp_path / "b", "same", _grid_report(), _retained())
    with pytest.raises(registered.RegistrationError, match="two runs share a name"):
        registered.select_grid([first, second], [290])


def _no_writes(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fail the test on any write through the registrar's two writers, which `retain`, the
    receipts and the case records all go through: rewriting a view with the same bytes
    leaves the files as they were, so comparing bytes cannot see it (review C3, B6)."""

    def refused(*args: object, **_kwargs: object) -> None:
        raise AssertionError(f"select wrote {args[0] if args else 'a file'}")

    monkeypatch.setattr(registered, "atomic_output_file", refused)
    monkeypatch.setattr(registered, "write_json", refused)


#: The row facts `select_grid` rebuilds from a run directory holding the retained view.
_REBUILT = (
    "side",
    "value",
    "earlier_verified",
    "below_earlier_by",
    "implied_by",
    "t101_side",
    "below_t101_side_by",
    "witness_side",
    "witness_frame",
    "above_exact_side_by",
    "agrees_with_report",
    "identity",
    "regularization",
)


def _reproduce(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """`select_grid` on a run directory holding the retained view: the committed row's
    facts, the view's bytes for `retain`, and nothing written."""
    selection = registered.GRID.selection.read_bytes()
    retained = registered.view_path(290, registered.GRID).read_bytes()
    run = _grid_run(tmp_path, "deg5-1013-a", _grid_report(), _retained())
    _no_writes(monkeypatch)
    receipt, views = registered.select_grid([run], [290])
    assert views == {290: _retained()}
    row, committed = receipt["rows"][0], registered.committed(registered.GRID)[290]
    for key in _REBUILT:
        assert row[key] == committed[key], key
    assert registered.GRID.selection.read_bytes() == selection
    assert registered.view_path(290, registered.GRID).read_bytes() == retained


def test_the_grid_batch_reproduces_its_row_and_writes_nothing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """From a run directory holding the retained view, `select_grid` rebuilds the
    committed row's facts, the identity measured again included, and returns the view's
    bytes for `retain`, writing nothing. The identity measurement took 5 to 6 s when
    review C5 marked this slow; with `arrangement_gap`'s nearest-centre search it is 0.65
    to 0.70 s of call (14 October 2026), under the 2 s threshold, so it runs on the
    pull-request surface."""
    _reproduce(monkeypatch, tmp_path)


def test_the_grid_batch_rebuilds_its_row_and_writes_nothing_on_the_quick_lane(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The reproduction above with the identity measurement taken as committed, so every
    other fact of the row and that nothing is written are held apart from the
    measurement; the measurement's own refusals are tested directly (PR #587, review
    C5)."""
    committed = registered.committed(registered.GRID)[290]["identity"]
    measured: list[int] = []

    def measure(n: int, *_args: object) -> dict[str, object]:
        measured.append(n)
        return dict(committed)

    monkeypatch.setattr(registered, "measure_identity", measure)
    _reproduce(monkeypatch, tmp_path)
    assert measured == [290]


def test_problems_names_a_count_both_batches_register(monkeypatch: pytest.MonkeyPatch) -> None:
    """The batches are disjoint, and `problems` says so where they are not; `batch_of` then
    returns the first batch that holds the count (PR #587, review B2)."""
    real = registered.committed

    def overlapping(batch: registered.Batch = registered.FIRST) -> dict[int, dict]:
        rows = dict(real(batch))
        if batch == registered.GRID:
            rows[291] = real(registered.FIRST)[291]
        return rows

    monkeypatch.setattr(registered, "committed", overlapping)
    assert "T-156 and T-155 both register [291]" in registered.problems(registered.GRID)
    assert registered.batch_of(291) == registered.FIRST


@pytest.mark.parametrize(
    ("witness", "message"),
    [
        (
            ("W-known-best-n290", Fraction(1, 2)),
            "n=290: the side the row records is not the checkout witness's own s_W",
        ),
        (
            ("W-rehoused-n290", None),
            (
                "n=290: the view was derived from W-known-best-n290, not the checkout's "
                "W-rehoused-n290"
            ),
        ),
    ],
)
def test_the_check_reads_the_witness_again(
    monkeypatch: pytest.MonkeyPatch, witness: tuple[str, Fraction | None], message: str
) -> None:
    """`witness_side` is read from the witness at `select`, and `--check` reads the
    checkout witness again, so a re-housed or corrected witness at n = 290 fails the
    check instead of leaving the record calling the view its packing (review B3)."""
    identity, side = witness
    row = registered.committed(registered.GRID)[290]
    found = side if side is not None else Fraction(row["side"])
    monkeypatch.setattr(registered, "checkout_witness", lambda _n: (identity, found))
    assert message in registered.problems(registered.GRID)


def test_the_grid_batch_refuses_a_view_above_a_larger_counts_ceiling(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Where the next count's verified upper bound lies below the view's side, the record
    already proves more than the view, and registering the view would leave the case
    record a weaker ceiling than the register proves: `select_grid` refuses it and says to
    register the count by monotonicity (PR #587, review C4)."""
    row = registered.committed(registered.GRID)[290]
    below = Fraction(row["side"]) - Fraction(1, 10**20)
    monkeypatch.setattr(
        registered,
        "next_count_ceiling",
        lambda _n: {"bound": below, "evidence": [registered.EVIDENCE]},
    )
    run = _grid_run(tmp_path, "run", _grid_report(), _retained())
    with pytest.raises(
        registered.RegistrationError,
        match=(
            re.escape(
                f"n=290: the record already proves s(290) ≤ {registered.side_text(below)}"
            )
            + re.escape(" by monotonicity from T-155; register the count by monotonicity")
        ),
    ):
        registered.select_grid([run], [290])


def _with_implied(monkeypatch: pytest.MonkeyPatch, implied: dict[str, object]) -> None:
    """`committed` with the grid batch's row at n = 290 recording `implied` as the ceiling
    that implies its bound."""
    real = registered.committed

    def rows(batch: registered.Batch = registered.FIRST) -> dict[int, dict]:
        found = dict(real(batch))
        if batch == registered.GRID:
            found[290] = {**found[290], "implied_by": implied}
        return found

    monkeypatch.setattr(registered, "committed", rows)


def test_problems_names_a_row_whose_implied_ceiling_lies_below_its_side(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A committed row whose next-count ceiling lies below its own side is the record
    `select_grid` now refuses to write, and `--check` names it (PR #587, review C4)."""
    row = registered.committed(registered.GRID)[290]
    below = registered.literal(Fraction(row["side"]) - Fraction(1, 10**20))
    _with_implied(monkeypatch, {**row["implied_by"], "side": below})
    assert (
        "n=290: the ceiling at n = 291 lies below the side, so the record would carry a "
        "weaker ceiling than the register proves"
    ) in registered.problems(registered.GRID)


def test_the_grid_batch_refuses_a_run_whose_reports_differ_in_settings(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A run's reports must share their settings, and the refusal comes before anything is
    written: with every row built, `select_grid` still writes nothing when it refuses
    (PR #587, review C3, B6)."""
    first, second = _grid_report(), _grid_report()
    second["n"] = 1
    second["settings"] = {"near_axis_degrees": 0.5}
    run = tmp_path / "run"
    monkeypatch.setattr(
        registered,
        "grid_reports",
        lambda _runs, _numbers: {
            1: [("run", run / "n-001", second)],
            290: [("run", run / "n-290", first)],
        },
    )
    monkeypatch.setattr(
        registered, "grid_selection_row", lambda n, _found, _batch: ({"n": n}, b"view")
    )
    _no_writes(monkeypatch)
    with pytest.raises(
        registered.RegistrationError, match="run: its reports differ in their settings"
    ):
        registered.select_grid([run], [1, 290])


@pytest.mark.parametrize(
    ("source", "message"),
    [
        (
            {"id": "W-known-best-n291"},
            (
                "n=290: the run read witness W-known-best-n291, not the checkout's "
                "W-known-best-n290"
            ),
        ),
        (
            {"id": "W-known-best-n290", "s_W_exact": "1/2"},
            (
                "n=290: the run read its witness at another side than the checkout "
                "witness's own s_W"
            ),
        ),
    ],
)
def test_the_identity_measurement_refuses_a_run_of_another_witness(
    source: dict[str, str], message: str
) -> None:
    """`measure_identity` measures a view against the checkout witness only where the run
    read that witness, by its id and its exact side `s_W`; the first batch's `select`
    reaches these refusals from a report's `source` (PR #587, review C3, B4)."""
    row = registered.committed(registered.GRID)[290]
    found = {"s_W_exact": row["witness_side"], **source}
    with pytest.raises(registered.RegistrationError, match=re.escape(message)):
        registered.measure_identity(290, registered.read_view(290, registered.GRID), [], found)


@pytest.mark.parametrize(
    "change",
    [
        pytest.param({"n": 290}, id="the same count"),
        pytest.param({"n": 289}, id="a smaller count"),
        pytest.param({"side": "18"}, id="above the side"),
    ],
)
def test_problems_names_a_row_whose_implied_ceiling_does_not_imply_its_bound(
    monkeypatch: pytest.MonkeyPatch, change: dict[str, object]
) -> None:
    """The ceiling a row says implies its bound must be a larger count's, at or below the
    row's side; `--check` names one that is not (PR #587, review C3)."""
    row = registered.committed(registered.GRID)[290]
    _with_implied(monkeypatch, {**row["implied_by"], **change})
    assert "n=290: the ceiling the row says implies the bound does not" in registered.problems(
        registered.GRID
    )


def test_an_implied_ceiling_no_registered_result_holds_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A next-count ceiling at or below the side is named by the results that hold it; one
    that no registered result holds cannot be named, and `implied_by` refuses it rather
    than recording an implication from nothing (PR #587, review C3)."""
    row = registered.committed(registered.GRID)[290]
    monkeypatch.setattr(registered, "results_holding", lambda _n, _evidence: [])
    with pytest.raises(
        registered.RegistrationError,
        match="n=291: no registered result holds the verified bound",
    ):
        registered.implied_by(290, Fraction(row["side"]))
