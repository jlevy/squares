"""The driver of Evan Daniel's vendored regularizer, on counts small enough to run here.

The input writer is held to exact digits (a rational witness's centres to fifty
significant digits of its exact values, a decimal witness's strings verbatim, the
algebraic witness's field values) and to upstream's own batch inputs where the witness
has not changed since upstream solved it. The replica builder is held to its boundary:
it copies the seven modules the pipeline runs byte for byte and writes nothing under
`vendor/`. The decision table is run as a pure function over synthetic measurements, one
for each of its eight live rows (6 and 9 retired on 13 October 2026) and one that no row
matches. One count, n = 26, runs end to end
through the real solver and regularizer.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib
import json
import math
import os
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath
import pytest
from jsonschema import Draft202012Validator

from devtools import regularize_axis_components as axis
from devtools import regularize_evand as drive
from devtools.regularize_axis_components import AtlasLayout
from devtools.regularize_evand import Decision, Measured, Options, classify
from devtools.retained_data import git_blob
from sqpack.witness import load_witness, materialize_exact_witness, witness_document
from sqpack.yamlio import load_yaml
from tests.test_regularize_axis_components import PIN_4, decimal_witness, write_witness

ALL_ROUTES = {"exact_verify": True, "independent": True, "half_angle": True}


def witness(n: int) -> dict:
    return load_witness(drive.witness_path(n), fallback_schema=drive.WITNESS_SCHEMA)


def vendor_listing() -> list[tuple[str, int]]:
    """Every file under `vendor/evand-regularize` with its size, for a before-and-after."""
    found: list[tuple[str, int]] = []
    for directory, _subdirectories, files in os.walk(drive.VENDOR):
        for name in files:
            path = Path(directory) / name
            found.append((str(path.relative_to(drive.VENDOR)), path.stat().st_size))
    return sorted(found)


# --------------------------------------------------------------------------------------
# Stage 1: the input
# --------------------------------------------------------------------------------------


def test_decimal_input_carries_the_witness_strings_verbatim() -> None:
    source = witness(26)
    n, side, rows = drive.read_input(drive.input_text(source))
    assert n == 26
    assert side == source["side"]
    expected = [(*square["center"], square["angle"]) for square in source["squares"]]
    assert rows == expected


def test_rational_input_is_its_exact_values_to_fifty_digits() -> None:
    source = witness(70)
    assert source["scalar"]["kind"] == "rational"
    _n, side, rows = drive.read_input(drive.input_text(source))
    squares, exact_side = materialize_exact_witness(source)
    bound = Fraction(1, 10**47)
    assert abs(Fraction(side) - Fraction(exact_side)) < bound
    mpmath.mp.dps = 60
    for (x, y, degrees), corners in zip(rows, squares, strict=True):
        xs = [Fraction(cx) for cx, _ in corners]
        ys = [Fraction(cy) for _, cy in corners]
        assert abs(Fraction(x) - sum(xs, Fraction(0)) / 4) < bound
        assert abs(Fraction(y) - sum(ys, Fraction(0)) / 4) < bound
        c, s = xs[1] - xs[0], ys[1] - ys[0]
        turn = mpmath.mpf(degrees) * mpmath.pi / 180
        assert abs(mpmath.cos(turn) - mpmath.mpf(c.numerator) / c.denominator) < 1e-45
        assert abs(mpmath.sin(turn) - mpmath.mpf(s.numerator) / s.denominator) < 1e-45


def test_algebraic_input_is_the_field_values_at_sixty_digits() -> None:
    source = witness(51)
    assert source["scalar"]["kind"] == "algebraic-number-field"
    n, side, rows = drive.read_input(drive.input_text(source))
    assert n == 51
    assert len(rows) == 51
    mpmath.mp.dps = 60
    exact = (16 + 5 * mpmath.sqrt(2)) / 3
    assert abs(mpmath.mpf(side) - exact) < mpmath.mpf(10) ** -48


@pytest.mark.parametrize("n", [5, 10, 13, 26])
def test_input_agrees_with_upstreams_batch_input(n: int) -> None:
    """Same squares in the same order, agreeing to binary64, angles modulo 90 degrees."""
    mine = drive.read_input(drive.input_text(witness(n)))
    theirs = drive.read_input((drive.UPSTREAM_INPUTS / f"n-{n}.txt").read_text())
    assert mine[0] == theirs[0]
    assert float(mine[1]) == float(theirs[1])
    for (x, y, angle), (u, v, other) in zip(mine[2], theirs[2], strict=True):
        assert math.isclose(float(x), float(u), rel_tol=1e-15, abs_tol=1e-15)
        assert math.isclose(float(y), float(v), rel_tol=1e-15, abs_tol=1e-15)
        turn = abs(float(angle) % 90 - float(other) % 90)
        assert min(turn, 90 - turn) < 1e-12


def test_witness_frame_is_the_exact_pose_at_s_w_to_eighty_digits() -> None:
    """`--frame witness` hands the regularizer the policy's frame: here n = 70's exact pose."""
    source = witness(70)
    frame = drive.source_frame(source)
    assert frame.side is not None
    n, side, rows = drive.read_input(drive.frame_text(source, frame))
    assert n == 70
    assert abs(Fraction(side) - frame.side) < Fraction(1, 10**78)
    for (x, y, _degrees), (cx, cy, _c, _s) in zip(rows, frame.placements, strict=True):
        assert abs(Fraction(x) - cx) < Fraction(1, 10**78)
        assert abs(Fraction(y) - cy) < Fraction(1, 10**78)


# --------------------------------------------------------------------------------------
# Stage 2: the replica
# --------------------------------------------------------------------------------------


def test_replica_copies_the_pipeline_and_writes_nothing_under_vendor(tmp_path: Path) -> None:
    before = vendor_listing()
    rows = [drive.batch_row(n, drive.case_facts(n), witness(n)) for n in (5, 26)]
    replica = drive.build_replica(tmp_path / "run", rows)
    assert vendor_listing() == before
    for directory, names in drive.REPLICA_FILES.items():
        for name in names:
            copied = replica / directory / name
            assert copied.read_bytes() == (drive.VENDOR / directory / name).read_bytes()
    results = json.loads((replica / drive.BATCH / "results.json").read_text())
    assert [row["n"] for row in results] == [5, 26]
    assert all(row["from_"] == "witness" for row in results)
    link = replica / drive.BATCH / "work/n-26"
    assert link.is_symlink()
    assert link.resolve() == (tmp_path / "run/n-026/solve").resolve()


def test_run_directory_inside_the_checkout_is_refused() -> None:
    with pytest.raises(drive.EvandRunError, match="inside the checkout"):
        drive.outside_checkout(drive.VENDOR / "runs")


def test_counts_parse_as_integers_and_ranges() -> None:
    assert drive.parse_counts(["5", "9-11", "10"]) == [5, 9, 10, 11]


# --------------------------------------------------------------------------------------
# Stage 8: the decision table, one synthetic measurement per row
# --------------------------------------------------------------------------------------

SW = Fraction(562, 100)
SAME = Measured(
    "same",
    produced=True,
    routes=ALL_ROUTES,
    relation="same",
    side=SW,
    upper=SW - Fraction(1, 10**20),
    level=2,
    max_move=Fraction(3, 10),
)

ROWS = {
    1: (Measured("solved", produced=False, status="solve timeout"), "generator-failed"),
    2: (
        Measured(
            "solved",
            produced=True,
            routes={**ALL_ROUTES, "half_angle": False},
            relation="solved",
            side=SW,
        ),
        "invalid",
    ),
    3: (
        Measured(
            "solved",
            produced=True,
            routes=ALL_ROUTES,
            relation="solved",
            side=SW,
            upper=SW + Fraction(1, 10**10),
        ),
        None,
    ),
    4: (
        Measured(
            "solved",
            produced=True,
            routes=ALL_ROUTES,
            relation="solved",
            side=SW,
            upper=SW - Fraction(1, 10**10),
        ),
        "dilated-side",
    ),
    5: (replace(SAME, pose_equals_witness=True), None),
    7: (replace(SAME, regressions=2), "regression"),
    8: (replace(SAME, level=3), None),
    10: (SAME, None),
}
EXPECTED = {
    1: ("no-view", None),
    2: ("refuse", "refused"),
    3: ("held", None),
    4: ("held", None),
    5: ("no-change", "unchanged"),
    7: ("review", None),
    8: ("alternate", None),
    10: ("admit", "regularized"),
}


@pytest.mark.parametrize("row", sorted(ROWS))
def test_each_row_of_the_decision_table(row: int) -> None:
    measured, refusal = ROWS[row]
    decided = classify(measured)
    assert decided.row == row
    assert (decided.decision, decided.index_record) == EXPECTED[row]
    assert decided.refusal == refusal


def test_the_first_matching_row_decides() -> None:
    """A view failing a route and below U is invalid (row 2) before it is a candidate."""
    both = Measured(
        "same",
        produced=True,
        routes={"exact_verify": False, "independent": True},
        relation="same",
        side=SW,
        upper=SW + 1,
    )
    assert classify(both).row == 2
    turned = replace(SAME, unnamed_turns=(3,), regressions=1)
    assert classify(turned) == Decision(
        7,
        "review",
        None,
        "regression",
        "1 per-square counts fell while no total did: for review",
    )


@pytest.mark.parametrize(
    ("changed", "named"),
    [
        (replace(SAME, one_to_one=False), "no one-to-one pairing"),
        (
            replace(SAME, unnamed_turns=(3, 7)),
            "squares [3, 7] turned without a recorded angle change",
        ),
        (replace(SAME, max_move=Fraction(6, 10)), "a square moved 0.6 > 1/2"),
    ],
)
def test_a_changed_pose_is_named_and_admitted(changed: Measured, named: str) -> None:
    """Owner, 13 October 2026: "the pose doesn't matter if it changes as long as it's
    optimal and conforms with our regularization guidelines", so rows 6 and 9 are retired:
    the change is named in the reason, and the rows that remain decide the view."""
    decided = classify(changed)
    assert (decided.row, decided.decision, decided.index_record) == (
        10,
        "admit",
        "regularized",
    )
    assert decided.reason == f"every admission condition holds; the pose changes: {named}"
    assert classify(replace(changed, regressions=1)).row == 7
    assert classify(replace(changed, regressions=1, totals_fall=True)).decision == "refuse"
    assert classify(replace(changed, level=3)).row == 8


def test_a_falling_total_is_refused_and_per_square_losses_alone_go_to_review() -> None:
    """Owner, 12 October 2026: trickier cases go to review; a total that falls does not."""
    per_square = classify(replace(SAME, regressions=22))
    assert (per_square.row, per_square.decision, per_square.index_record) == (
        7,
        "review",
        None,
    )
    fell = classify(replace(SAME, regressions=22, totals_fall=True))
    assert (fell.row, fell.decision, fell.index_record, fell.refusal) == (
        7,
        "refuse",
        "refused",
        "regression",
    )


def test_totals_fall_against_the_witness_or_the_current_view() -> None:
    gained = {"before": [0, 1, 12, 6, 7], "after": [0, 0, 13, 5, 8]}
    shaded: dict[str, object] = {"house": gained, "stage": gained, "against_current": None}
    assert not drive.totals_fall(shaded)
    lost = {"before": gained["after"], "after": gained["before"]}
    assert drive.totals_fall({**shaded, "stage": lost})
    richer = {"house": [0, 0, 0, 6, 20], "stage": [0, 0, 13, 5, 8]}
    current = {"view": "v", "regressions": [], "histograms": richer}
    assert drive.totals_fall({**shaded, "against_current": current})
    # A report written before the replaced view's histograms were stored has none to
    # compare with, and decides against the witness alone.
    assert not drive.totals_fall({**shaded, "against_current": {"regressions": [1]}})


def test_a_fewest_merge_is_an_alternate_and_fewest_alone_is_not_admitted() -> None:
    merged = replace(SAME, variant="fewest", determined_merge=True)
    assert classify(merged).row == 8
    plain = replace(SAME, variant="fewest")
    assert classify(plain).row is None
    assert classify(plain).decision == "review"


@pytest.mark.parametrize("row", [3, 4, 7])
def test_a_view_that_draws_the_same_picture_is_no_change_whatever_its_row(row: int) -> None:
    """Owner, 11 October 2026: nothing is refused or held where nothing would change."""
    measured, _refusal = ROWS[row]
    decided = classify(replace(measured, visible_change=False))
    assert decided.row == row
    assert (decided.decision, decided.index_record, decided.refusal) == (
        "no-change",
        "unchanged",
        None,
    )
    assert decided.reason.startswith("nothing visible changes (")


@pytest.mark.parametrize("row", [1, 2])
def test_no_view_and_an_invalid_view_are_reported_as_they_are(row: int) -> None:
    measured, _refusal = ROWS[row]
    decided = classify(replace(measured, visible_change=False))
    assert (decided.decision, decided.index_record) == EXPECTED[row]


def test_visible_change_reads_moves_turns_pairing_and_house_counts() -> None:
    still = {"moved": 0, "turned": [], "one_to_one": True}
    same_counts = {"house": {"before": [0, 1, 2, 3, 4], "after": [0, 1, 2, 3, 4]}}
    assert not drive.visible_change(still, same_counts)
    assert drive.visible_change({**still, "moved": 1}, same_counts)
    assert drive.visible_change({**still, "turned": [3]}, same_counts)
    assert drive.visible_change({**still, "one_to_one": False}, same_counts)
    changed = {"house": {"before": [0, 1, 2, 3, 4], "after": [0, 0, 3, 3, 4]}}
    assert drive.visible_change(still, changed)


def test_a_solved_view_with_no_upper_bound_is_held_and_says_so() -> None:
    measured = Measured("solved", produced=True, routes=ALL_ROUTES, relation="solved", side=SW)
    decided = classify(measured)
    assert decided.row == 4
    assert "U unknown" in decided.reason


def test_a_view_at_exactly_the_bound_is_decided_as_a_same_side_view_is() -> None:
    """Owner, 12 October 2026: a view whose side is the verified upper bound exactly
    is a drawing frame, so rows 5 to 10 decide it (n = 206 in the pilot)."""
    upper = SW - Fraction(1, 10**20)
    assert drive.side_relation(SW, SW, upper) == "same"
    assert drive.side_relation(upper, SW, upper) == "bound"
    assert drive.side_relation(upper, None, upper) == "bound"
    assert drive.side_relation(SW, None, upper) == "solved"
    assert drive.side_relation(SW, None, None) == "solved"
    at_bound = replace(SAME, output="solved", relation="bound", side=upper, upper=upper)
    assert classify(at_bound) == classify(SAME)
    assert classify(replace(at_bound, regressions=1)).row == 7
    unmeasured = replace(at_bound, measured=False)
    assert classify(unmeasured).decision == "review"


def _register_item_validator() -> Draft202012Validator:
    schema = load_yaml((drive.ROOT / "frontier/results.schema.yaml").read_text())
    return Draft202012Validator(
        schema["$defs"]["result"]["properties"]["regularizations"]["items"]
    )


REPORT = {
    "n": 26,
    "source": {
        "path": "packing/witnesses/known-best/n-026.yaml",
        "provenance": {"source_key": "[kingbird]", "found_by": ["Göbel"], "improved_by": []},
    },
    "generator": {
        "pin": "675a5ea",
        "patches": [],
        "variant": "conservative",
        "style": "coincide",
    },
    "regularize": {
        "merged": [[8, -0.0057, 0.0], [23, -44.994, 45.0], [4, 12.0, 30.5]],
        "angle_changes": [["determined-merge", 30.0, 30.7, 2]],
    },
    "outputs": {"same": {"relation": "same"}, "solved": {"relation": "solved"}},
    "identity": {"one_to_one": True, "moved": 1, "max_move": "3.1e-1", "max_turn_deg": "0"},
}


def test_the_regularization_record_is_the_registers_item_once_of_is_resolved() -> None:
    """Owner, 11 October 2026: our regularizations are tracked with the packing's
    provenance, in the register's terms, so admission copies the record unchanged."""
    record = drive.regularization_record(REPORT)
    assert record is not None
    assert record["of_witness"] == "W-known-best-n026"
    assert record["provenance"]["source_key"] == "[kingbird]"
    assert record["by"] == "project"
    assert "evand/square-packing@675a5ea" in record["method"]
    assert record["side"] == "same"
    assert record["changes"] == {
        "merged_rotation_groups_deg": 0.7,
        # Square 8 onto the axis; 23 onto 45 degrees and 4 onto 30.5 are re-angled.
        "straightened": 1,
        "re_angled": 2,
    }
    assert record["identity"]["basis"] == "measured"
    as_item = {
        key: value for key, value in record.items() if key not in {"of_witness", "provenance"}
    }
    errors = list(_register_item_validator().iter_errors({**as_item, "of": "T-001"}))
    assert errors == []


def test_a_view_at_the_bound_is_recorded_as_solved_in_the_registers_terms() -> None:
    at_bound = {**REPORT, "outputs": {"same": None, "solved": {"relation": "bound"}}}
    record = drive.regularization_record(at_bound)
    assert record is not None
    assert record["side"] == "solved"


def test_no_view_has_no_regularization_record() -> None:
    assert drive.regularization_record({**REPORT, "outputs": {}}) is None
    assert drive.regularization_record({**REPORT, "identity": None}) is None


ROUTES_OK = {"exact_verify": True, "independent": True, "half_angle": True}
DECIDED = {
    "n": 26,
    "outputs": {"same": {"relation": "same", "routes": ROUTES_OK}, "solved": None},
    "identity": {"one_to_one": True},
    "shades": {
        "house": {"before": [0, 1, 12, 6, 7], "after": [0, 0, 13, 5, 8]},
        "stage": {"before": [0, 1, 12, 6, 7], "after": [0, 0, 13, 5, 8]},
    },
    "decision": {"row": 10, "decision": "admit"},
}


def test_the_admitted_selection_takes_row_10_alone() -> None:
    assert drive.layer_candidate(DECIDED, "admitted") == "same"
    held = {**DECIDED, "decision": {"row": 4, "decision": "held"}}
    assert drive.layer_candidate(held, "admitted") is None
    for word in ("review", "alternate"):
        decided = {**DECIDED, "decision": {"row": 7, "decision": word}}
        assert drive.layer_candidate(decided, "admitted") is None
    at_bound = {
        **DECIDED,
        "outputs": {"same": None, "solved": {"relation": "bound", "routes": ROUTES_OK}},
    }
    assert drive.layer_candidate(at_bound, "admitted") == "solved"


def test_the_preview_takes_visible_exact_one_to_one_views_that_lose_no_contact() -> None:
    held = {**DECIDED, "decision": {"row": 4, "decision": "held"}}
    assert drive.layer_candidate(held, "preview") == "same"
    for word in ("no-change", "no-view"):
        assert (
            drive.layer_candidate({**DECIDED, "decision": {"decision": word}}, "preview")
            is None
        )
    refused_route = {
        **DECIDED,
        "outputs": {
            "same": {"relation": "same", "routes": {**ROUTES_OK, "independent": False}}
        },
    }
    assert drive.layer_candidate(refused_route, "preview") is None
    assert (
        drive.layer_candidate({**DECIDED, "identity": {"one_to_one": False}}, "preview") is None
    )
    fewer = {"before": [0, 0, 13, 5, 8], "after": [0, 1, 12, 6, 7]}
    lost = {**DECIDED, "shades": {"house": fewer, "stage": DECIDED["shades"]["stage"]}}
    assert drive.layer_candidate(lost, "preview") is None


def both_outputs(*, same_side: str, solved_side: str, bound: str) -> dict[str, Any]:
    """A report whose run measured the same-side view as the drawing and the solved one
    beside it, as `measure` writes one."""
    same_ident = {"of": "same", "one_to_one": True, "moved": 2, "max_move": "1/10"}
    solved_ident = {"of": "solved", "one_to_one": True, "moved": 3, "max_move": "1/10"}
    return {
        **DECIDED,
        "verified_upper_bound": bound,
        "verified_upper_bound_exact_form": None,
        "source": {"s_W_exact": same_side},
        "outputs": {
            "same": {"side_exact": same_side, "relation": "same", "routes": ROUTES_OK},
            "solved": {
                "side_exact": solved_side,
                "relation": "bound",
                "routes": ROUTES_OK,
                "identity": solved_ident,
                "shades": {**DECIDED["shades"], "of": "solved"},
            },
            "same_refusal": None,
        },
        "identity": same_ident,
        "shades": {**DECIDED["shades"], "of": "same"},
    }


def test_a_same_side_view_above_the_bound_yields_to_the_view_at_the_bound() -> None:
    """Owner, 13 October 2026: a valid view has "equal or smaller side", drawn "optimal as
    best as known"; where the witness sits above the bound the solve reached, the view at
    the bound is drawn, and the same-side one is kept with its measurements."""
    report = both_outputs(same_side="563/100", solved_side="281/50", bound="5.62")
    assert drive.yield_to_bound(report)
    outputs = report["outputs"]
    assert outputs["same"] is None
    assert outputs["same_refusal"] == drive.ABOVE_BOUND
    assert outputs["same_above_bound"]["identity"]["of"] == "same"
    assert report["identity"]["of"] == "solved"
    assert report["shades"]["of"] == "solved"
    assert "identity" not in outputs["solved"]
    assert drive.layer_candidate({**report, "decision": {"decision": "admit"}}, "admitted") == (
        "solved"
    )
    assert not drive.yield_to_bound(report)


@pytest.mark.parametrize(
    ("same_side", "solved_side", "bound"),
    [
        # The witness is at the bound: the same-side view is at the best known side.
        ("281/50", "281/50", "5.62"),
        # The solve stopped short of the bound.
        ("563/100", "5621/1000", "5.62"),
        # The witness is below the bound: a register candidate, decided as before.
        ("5619/1000", "281/50", "5.62"),
    ],
)
def test_a_same_side_view_at_or_below_the_bound_stays(
    same_side: str, solved_side: str, bound: str
) -> None:
    report = both_outputs(same_side=same_side, solved_side=solved_side, bound=bound)
    assert not drive.yield_to_bound(report)
    assert report["outputs"]["same"] is not None
    assert report["identity"]["of"] == "same"


def test_a_view_at_the_bound_never_measured_leaves_the_same_side_view() -> None:
    """A run written before views at the bound were measured has nothing to decide on."""
    report = both_outputs(same_side="563/100", solved_side="281/50", bound="5.62")
    del report["outputs"]["solved"]["identity"]
    assert not drive.yield_to_bound(report)
    assert report["outputs"]["same"] is not None


def test_a_report_written_before_bound_existed_is_decided_as_the_table_now_does() -> None:
    block = {"side_exact": "281/50", "relation": "solved", "routes": ROUTES_OK}
    report = {
        **DECIDED,
        "verified_upper_bound": "5.62",
        "verified_upper_bound_exact_form": None,
        "shades": {**DECIDED["shades"], "regressions": []},
        "source": {"s_W_exact": "563/100"},
        "outputs": {"same": None, "solved": block},
        "identity": {"one_to_one": True, "moved": 4, "max_move": "1/10", "turned": [2]},
        "regularize": {"level": 2},
    }
    measured = drive.measured_from_report(report, "solved")
    assert measured.relation == "bound"
    assert classify(measured).decision == "admit"
    # Beside a same-side view the bound view was never measured, and is not admitted.
    same = {**block, "side_exact": "563/100", "relation": "same"}
    beside = {**report, "outputs": {"same": same, "solved": block}}
    assert classify(drive.measured_from_report(beside, "solved")).decision == "review"


def test_a_held_count_says_what_registration_would_lead_to() -> None:
    held: dict[str, Any] = {}
    below = replace(SAME, side=SW - Fraction(1, 10**14), upper=SW)
    drive.decide(held, replace(below, output="solved", relation="solved"), below)
    assert held["decision"]["row"] == 3
    assert held["decision"]["after_registration"]["decision"] == "admit"
    solved_only: dict[str, Any] = {}
    drive.decide(solved_only, replace(below, output="solved", relation="solved"))
    assert solved_only["decision"]["after_registration"]["row"] == 10
    admitted: dict[str, Any] = {}
    drive.decide(admitted, replace(SAME, output="solved", relation="solved", side=SW + 1), SAME)
    assert "after_registration" not in admitted["decision"]


def test_only_the_source_orientation_is_run(tmp_path: Path) -> None:
    options = drive.Options(run_dir=tmp_path, orient="best")
    with pytest.raises(drive.EvandRunError, match="only at --orient 0"):
        drive.run([26], options, 1)


def test_the_review_queue_is_every_count_reported_for_review() -> None:
    rows = [
        {"n": 1, "row": 6, "decision": "review"},
        {"n": 2, "row": 7, "decision": "refuse"},
        {"n": 3, "row": 8, "decision": "alternate"},
        {"n": 4, "row": None, "decision": "review"},
        {"n": 5, "row": 10, "decision": "admit"},
    ]
    assert drive.receipt_lists(rows)["review_queue"] == [1, 3, 4]


def test_only_the_admitted_selection_may_write_into_this_checkout(tmp_path: Path) -> None:
    with pytest.raises(drive.EvandRunError, match="only the admitted selection"):
        drive.write_layer([tmp_path], drive.REPO, "preview")


def scratch_tree(tmp_path: Path) -> tuple[Path, AtlasLayout]:
    """A tree laid out as the checkout is, with one count (the axis tests' row of four
    with slack) and the axis tool's layer built over it."""
    root = tmp_path / "tree"
    packing = root / "packing"
    (packing / "witnesses/known-best").mkdir(parents=True)
    (packing / "atlas/known-best").mkdir(parents=True)
    row = decimal_witness(
        [("0.53", "0.5", "0"), ("1.56", "0.5", "0"), ("2.59", "0.5", "0"), PIN_4],
        "4",
        name="row",
    )
    write_witness(packing / "witnesses/known-best/n-004.yaml", row)
    manifest = packing / "atlas/known-best/manifest.json"
    entries = [{"n": 4, "witness": {"path": "witnesses/known-best/n-004.yaml"}}]
    manifest.write_text(json.dumps({"atlas": {"entries": entries}}), encoding="utf-8")
    layout = drive.layer_layout(root)
    assert axis.main(["--update-atlas"], layout=layout) == 0
    return root, layout


def a_run(root: Path, layout: AtlasLayout, run_dir: Path) -> Path:
    """A finished run that admitted a view of the row at its own side: the axis tool's
    view, written as the driver writes its same-side view, with the report around it and
    the stored regularization's settings beside it, which `layer_refusal` holds it to."""
    view = load_yaml(gzip.decompress(layout.view(4).read_bytes()).decode())["witness"]
    view["certificate"] = {"kind": "same-side-view", "side_relation": "same"}
    directory = run_dir / "n-004"
    directory.mkdir(parents=True)
    (directory / "view-same.yaml").write_text(witness_document(view), encoding="utf-8")
    stored = {"variant": "conservative", "orient": 0, "frame": "kkt", "style": drive.STYLE}
    (directory / "regularize.json").write_text(json.dumps(stored), encoding="utf-8")
    source = root / "packing/witnesses/known-best/n-004.yaml"
    after = drive.histogram(drive.contact_partners(view)["house"])
    stage = drive.histogram(drive.contact_partners(view)["stage"])
    record = {
        "n": 4,
        "of_witness": "W-row",
        "provenance": {"source_key": None, "found_by": [], "improved_by": []},
        "by": "project",
        "method": drive.METHOD.format(
            pin="675a5ea", patches="", variant="conservative", style="coincide"
        ),
        "side": "same",
        "identity": {
            "basis": "measured",
            "measured_in": drive.MEASURED_IN,
            "one_to_one": True,
            "moved": 3,
            "max_move": 0.06,
            "max_turn_deg": 0.0,
        },
    }
    report = {
        "n": 4,
        "status": "ok",
        "source": {
            "id": "W-row",
            "path": "packing/witnesses/known-best/n-004.yaml",
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "kind": "decimal",
            "s_W": "4",
            "s_W_exact": "4",
        },
        "solve": {"status": "KKT local min", "retried_with": ["--dps", "100"]},
        "regularize": {"level": 2, "groups_before": 1, "groups_after": 1},
        "outputs": {
            "solved": None,
            "same": {
                "side_exact": "4",
                "relation": "same",
                "id": view["id"],
                "routes": {"exact_verify": True, "independent": True},
                "minus_s_W": "0.000e+00",
                "minus_U": None,
                "git_blob": git_blob((directory / "view-same.yaml").read_bytes()),
            },
        },
        "identity": {"one_to_one": True, "symmetry": 0},
        "shades": {
            "house": {"before": after, "after": after},
            "stage": {"before": stage, "after": stage},
            "regressions": [],
            "against_current": None,
        },
        "decision": {
            "row": 10,
            "decision": "admit",
            "reason": "every admission condition holds",
        },
        "regularization": record,
    }
    (directory / "report.json").write_text(json.dumps(report), encoding="utf-8")
    receipt = {
        "finished": "2026-10-12T05:00:00Z",
        "generator": {"interpreter": "CPython 3.14.7"},
        "parameters": {"variant": "conservative", "workers": 1, "counts": [4]},
        "counts": [{"n": 4, "decision": "admit"}],
        "cost": {"cpu_seconds": 1.5, "wall_seconds": 2.0, "workers": 1},
    }
    (run_dir / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
    return run_dir


def test_an_admitted_view_enters_the_layer_under_its_contract(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PACK_JOBS", "1")
    root, layout = scratch_tree(tmp_path)
    run_dir = a_run(root, layout, tmp_path / "full")

    # A count left out is not written, whatever was decided there.
    summary = drive.write_layer([run_dir], root, "admitted", exclude={4})
    assert (summary["written"], summary["excluded"]) == ([], [4])

    summary = drive.write_layer([run_dir], root, "admitted")
    assert summary["written"] == [4]
    assert axis.check_atlas(layout) == []
    index = json.loads(layout.index.read_text())
    (entry,) = index["entries"]
    assert entry["generator"] == axis.EVAND_GENERATOR
    assert entry["run"] == {
        "id": "evand-regularize-full",
        "output": "same",
        "retried_with": ["--dps", "100"],
    }
    assert entry["reference"]["generator"] == axis.ALGORITHM
    assert entry["regularization"]["identity"]["measured_in"] == drive.LAYER_INDEX_PATH
    assert entry["decision"]["row"] == 10
    assert index["generators"][axis.EVAND_GENERATOR]["pin"] == "675a5ea"
    assert index["runs"][0]["decisions"] == {"admit": 1}
    view = load_yaml(gzip.decompress(layout.view(4).read_bytes()).decode())["witness"]
    certificate = view["certificate"]
    assert certificate["credit"] == axis.EVAND_CREDIT
    assert certificate["generated"] == {"kind": "same-side-view", "side_relation": "same"}
    # The full check decides the drawn view again on both routes.
    assert axis.main(["--verify-atlas"], layout=layout) == 0


def test_only_an_admitted_grid_view_is_admitted() -> None:
    """The decision table decides a grid-slack view as it decides the driver's own."""
    grid = importlib.import_module("devtools.regularize_grid_slack")
    report: dict[str, Any] = {
        "n": 26,
        "attempts": [
            {
                "exact": {
                    "side": drive.literal(Fraction(source_side(26))),
                    "verdicts": {
                        "exact_verify": {"passed": True},
                        "independent": {"passed": True},
                    },
                }
            }
        ],
        "measured": {
            "identity": {
                "one_to_one": True,
                "unnamed_turns": [],
                "max_move": "1e-1",
                "moved": 1,
            },
            "shades": {"regressions": [], "against_current": {"regressions": []}},
            "visible_change": True,
            "totals_fall": False,
        },
    }
    source = witness(26)
    assert grid.decided(report, source).decision == "admit"
    turned = {
        **report["measured"],
        "identity": {**report["measured"]["identity"], "unnamed_turns": [3]},
    }
    # Rows 6 and 9 are retired (owner, 13 October 2026): a changed pose is named.
    decided = grid.decided({**report, "measured": turned}, source)
    assert (decided.row, decided.decision) == (10, "admit")
    assert "squares [3] turned" in decided.reason
    far = {
        **report["measured"],
        "identity": {**report["measured"]["identity"], "max_move": "0.6"},
    }
    decided = grid.decided({**report, "measured": far}, source)
    assert (decided.row, decided.decision) == (10, "admit")
    assert "moved 0.6 > 1/2" in decided.reason
    lost = {
        **report["measured"],
        "shades": {"regressions": [4], "against_current": {"regressions": []}},
    }
    assert grid.decided({**report, "measured": lost}, source).decision == "review"
    assert grid.decided({"n": 26, "refusal": "no-exact-frame"}, source).decision == "no-view"


def source_side(n: int) -> Fraction:
    frame = drive.source_frame(witness(n))
    assert frame.side is not None
    return frame.side


# --------------------------------------------------------------------------------------
# One count, end to end
# --------------------------------------------------------------------------------------


def test_n26_runs_end_to_end(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    receipt = drive.run([26], Options(run_dir=run_dir), workers=1)
    report = json.loads((run_dir / "n-026/report.json").read_text())
    assert report["status"] == "ok"
    assert report["source"]["path"] == "packing/witnesses/known-best/n-026.yaml"
    assert report["solve"]["status"] == "KKT local min"
    assert report["solve"]["gate"] == "certified"
    assert report["solve"]["free"] == [8, 19, 23]
    # One attempt, so the stage's seconds are that attempt's.
    assert [row["rung"] for row in report["solve"]["attempts"]] == [None]
    assert report["seconds"]["solve"] == report["solve"]["attempts"][0]["seconds"]
    assert report["regularize"]["level"] == 1
    solved = report["outputs"]["solved"]
    assert solved["relation"] == "solved"
    assert solved["routes"] == ALL_ROUTES
    assert Fraction(solved["side_exact"]) > Fraction(report["source"]["s_W_exact"])
    loaded = load_witness(
        run_dir / "n-026/view-solved.yaml", fallback_schema=drive.WITNESS_SCHEMA
    )
    assert loaded["id"] == "W-known-best-n026-regularized"
    assert loaded["certificate"]["derived_from"]["sha256"] == report["source"]["sha256"]
    assert report["identity"]["one_to_one"] is True
    assert sum(report["shades"]["house"]["before"]) == 26
    if report["outputs"]["same"] is None:
        assert report["outputs"]["same_refusal"].startswith("same-side")
        assert report["decision"]["row"] == 4
    else:
        same = report["outputs"]["same"]
        assert same["relation"] == "same"
        assert same["side_exact"] == report["source"]["s_W_exact"]
        assert report["identity"]["of"] == "same"
    row = receipt["counts"][0]
    assert row["n"] == 26
    assert receipt["generator"]["pin"] == "675a5ea"
    assert receipt["generator"]["patches"] == []
    assert receipt["cost"]["cpu_seconds"] > 0
    assert "26" in receipt["solve_outputs"]
    assert "26" in drive.report_table(receipt).splitlines()[1]
    # Deciding again from the written report reproduces the decision and keeps the cost.
    decided = report["decision"]
    again = drive.reclassify(run_dir)
    redone = json.loads((run_dir / "n-026/report.json").read_text())
    assert redone["decision"] == decided
    assert again["cost"] == receipt["cost"]
    assert again["reclassified"]["counts"] == [26]


def test_long_integer_text_lifts_the_digit_limit_for_one_measurement() -> None:
    """At n = 110 `arrangement_gap` wrote an exact squared move past Python's limit."""
    huge = 10**5000
    with pytest.raises(ValueError, match="integer string conversion"):
        str(huge)
    with drive.long_integer_text():
        assert len(str(huge)) == 5001
    with pytest.raises(ValueError, match="integer string conversion"):
        str(huge)


def test_the_retry_ladder_takes_only_failed_solves_and_noise_level_jams() -> None:
    """The no-view study of 12 October 2026: 18 recovers at 100 digits, 152 and 269 with
    `--force-kkt`; the rational witnesses with slack are rightly not jammed."""
    assert drive.retry_rung({"status": "solve failed"}) == drive.RETRY_DIGITS
    noise = {"status": "not jammed", "jam_residual": 1.82e-7, "vv_milp_dS": -4.9e-7}
    assert drive.retry_rung(noise) == drive.FORCE_KKT
    slack = {"status": "not jammed", "jam_residual": 1.5e-2, "vv_milp_dS": -0.42}
    assert drive.retry_rung(slack) is None
    assert drive.retry_rung({**noise, "vv_milp_dS": -2.2e-5}) is None
    for status in ("certificate invalid", "KKT local min", "bound only", "not converged"):
        assert drive.retry_rung({"status": status}) is None
    printed = Fraction(1283, 100)
    assert not drive.polished({"S_exact": str(printed - Fraction(5, 10**12))}, printed)
    assert drive.polished({"S_exact": str(printed - Fraction(1, 10**9))}, printed)
    assert drive.polished({"S_exact": str(printed)}, None)


def test_a_rung_is_never_climbed_twice_and_each_status_has_its_own_rungs() -> None:
    """Rungs 3 and 5a (owner's overnight instruction, 12 October 2026): a timeout is
    solved again with the stall-stop patch, then as a first pass alone (290, 302); a
    failed active-set step after a converged first pass keeps the first pass (258)."""
    timeout = {"status": "timeout"}
    assert drive.retry_rung(timeout) == drive.STALL_STOP
    assert drive.retry_rung(timeout, [drive.STALL_STOP]) == drive.FIRST_PASS
    assert drive.retry_rung(timeout, [drive.STALL_STOP, drive.FIRST_PASS]) is None
    active_set = {"status": "solve failed", "forced_pairs": [[108, 109]]}
    assert drive.retry_rung(active_set) == drive.FIRST_PASS
    assert drive.retry_rung(active_set, [drive.FIRST_PASS]) == drive.RETRY_DIGITS
    first_pass = {"status": "solve failed", "forced_pairs": None}
    assert drive.retry_rung(first_pass) == drive.RETRY_DIGITS
    assert drive.retry_rung(first_pass, [drive.RETRY_DIGITS]) is None


def test_an_attempt_accumulates_the_rungs_climbed_to_it() -> None:
    attempt = drive.PLAIN.climb(drive.STALL_STOP).climb(drive.FIRST_PASS)
    assert attempt.record() == {
        "rungs": ["stall-stop", "first-pass"],
        "arguments": [],
        "patches": ["probe-flat-stall-stop"],
        "first_pass": True,
    }
    digits = drive.PLAIN.climb(drive.FORCE_KKT).climb(drive.RETRY_DIGITS)
    assert digits.arguments == ["--force-kkt", "--dps", "100"]
    assert drive.PLAIN.record() == {
        "rungs": [],
        "arguments": [],
        "patches": [],
        "first_pass": False,
    }


def test_the_relaxed_gate_takes_a_refused_certificate_at_a_local_minimum_only() -> None:
    """Rung 3: 258 and 302 converge to local minima whose own dilated certificates upstream
    refused, and reach the regularizer; 155 is not a local minimum and stops."""
    local = "local minimum of S, strict modulo 68 exact flat motions (PD on the rest)"
    refused = {"status": "certificate invalid", "newton_converged": True, "second_order": local}
    assert drive.solve_gate(refused) == "relaxed"
    assert drive.solve_gate({**refused, "second_order": "PSD with 3 zero modes"}) == "relaxed"
    descent = "NOT a local minimum: first-order descent in the corner-corner branch MILP"
    assert drive.solve_gate({**refused, "second_order": descent}) is None
    assert drive.solve_gate({**refused, "newton_converged": False}) is None
    assert drive.solve_gate({"status": "KKT local min"}) == "certified"
    assert drive.solve_gate({"status": "bound only"}) == "certified"
    for status in ("timeout", "solve failed", "not jammed", "not converged", "error"):
        assert drive.solve_gate({"status": status, "second_order": local}) is None


def _fake_solves(
    outcomes: dict[str, dict[str, Any]], monkeypatch: pytest.MonkeyPatch
) -> list[str]:
    """Stand `solve` in for the solver: each attempt's directory and a canned outcome."""
    called: list[str] = []

    def fake(
        directory: Path,
        _replica: Path,
        _timeout: float,
        attempt: drive.Attempt = drive.PLAIN,
        name: str = "solve",
    ) -> dict[str, Any]:
        called.append(name)
        (directory / name).mkdir(parents=True, exist_ok=True)
        (directory / name / "witness.json").write_text(name)
        block = dict(outcomes[name])
        block["gate"] = drive.solve_gate(block)
        return {**block, "seconds": 1.0, **attempt.record()}

    monkeypatch.setattr(drive, "solve", fake)
    return called


def test_the_ladder_keeps_the_first_attempt_that_reaches_the_regularizer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    local = "local minimum of S, strict modulo 157 exact flat motions"
    called = _fake_solves(
        {
            "solve": {"status": "timeout"},
            "solve-retry-stall-stop": {"status": "solve failed", "forced_pairs": [[111, 114]]},
            "solve-retry-first-pass": {
                "status": "certificate invalid",
                "newton_converged": True,
                "second_order": local,
                "S_exact": "17.7",
            },
        },
        monkeypatch,
    )
    kept = drive.solve_with_retries(tmp_path, tmp_path / "replica", 1800, Fraction(18))
    assert called == ["solve", "solve-retry-stall-stop", "solve-retry-first-pass"]
    assert kept["gate"] == "relaxed"
    assert kept["rungs"] == ["stall-stop", "first-pass"]
    assert kept["patches"] == ["probe-flat-stall-stop"]
    assert [row["rung"] for row in kept["attempts"]] == [None, "stall-stop", "first-pass"]
    assert [row.get("accepted") for row in kept["attempts"]] == [None, False, True]
    assert (tmp_path / "solve/witness.json").read_text() == "solve-retry-first-pass"
    assert (tmp_path / "solve-first/witness.json").read_text() == "solve"
    assert (tmp_path / "solve-retry-stall-stop").is_dir()


def test_a_first_attempt_through_the_relaxed_gate_climbs_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    called = _fake_solves(
        {
            "solve": {
                "status": "certificate invalid",
                "newton_converged": True,
                "second_order": "PD: strict local minimum",
            }
        },
        monkeypatch,
    )
    kept = drive.solve_with_retries(tmp_path, tmp_path / "replica", 600, None)
    assert called == ["solve"]
    assert kept["gate"] == "relaxed"
    assert kept["rungs"] == []
    assert len(kept["attempts"]) == 1


def test_a_forced_solve_that_polishes_ends_the_climb(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    printed = Fraction(1283, 100)
    called = _fake_solves(
        {
            "solve": {"status": "not jammed", "jam_residual": 2e-7, "vv_milp_dS": -5e-7},
            "solve-retry-force-kkt": {
                "status": "KKT local min",
                "S_exact": str(printed - Fraction(1, 10**8)),
            },
        },
        monkeypatch,
    )
    kept = drive.solve_with_retries(tmp_path, tmp_path / "replica", 600, printed)
    assert called == ["solve", "solve-retry-force-kkt"]
    assert kept["status"] == "not jammed"
    assert kept["gate"] is None
    assert kept["attempts"][1]["polished"] is True
    assert not (tmp_path / "solve-first").exists()


def _timed_out_solve(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    """Stand the ladder in for a solve that timed out on both rungs it climbed, and the
    replica's batch status, which `run` builds and these tests do not."""
    attempts = [
        {"rung": None, "status": "timeout", "gate": None, "seconds": 1800.0},
        {"rung": "stall-stop", "status": "timeout", "gate": None, "seconds": 1800.0},
    ]
    block = {"status": "timeout", "gate": None, "seconds": 1800.0, **drive.PLAIN.record()}

    def ladder(*_arguments: object) -> dict[str, Any]:
        return {**block, "attempts": attempts}

    monkeypatch.setattr(drive, "solve_with_retries", ladder)
    monkeypatch.setattr(drive, "record_solve_status", lambda *_arguments: None)
    return attempts


STALE_OUTPUTS = ("view-solved.yaml", "view-same.yaml", "regularize.json", "regularize.cert")


@pytest.mark.parametrize("stage", ["input", "solve"])
def test_a_rerun_that_stops_at_the_solve_leaves_no_earlier_output_behind(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, stage: str
) -> None:
    """The receipt digests `regularize.cert` and the gallery draws a view on disk, so a
    count re-run in its run directory keeps neither from the run before."""
    _timed_out_solve(monkeypatch)
    directory = drive.count_dir(tmp_path, 26)
    directory.mkdir(parents=True)
    (directory / "input.txt").write_text(drive.input_text(witness(26)), encoding="utf-8")
    for name in STALE_OUTPUTS:
        (directory / name).write_text("an earlier run's output", encoding="utf-8")
    report = drive.run_count(26, Options(run_dir=tmp_path, from_stage=stage))
    assert report["status"] == "timeout"
    assert report["outputs"] == {"solved": None, "same": None, "same_refusal": None}
    assert [name for name in STALE_OUTPUTS if (directory / name).exists()] == []
    # Only the exact solve's input is left to name by digest.
    assert list(drive.solve_digests(tmp_path, [26])["26"]) == ["input.txt"]


def test_a_later_stage_rerun_of_a_timed_out_solve_keeps_its_solve_and_decision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A timeout writes no `solve/witness.json`: a re-run from a later stage keeps the
    solve the previous report recorded, attempts and all, and so its decision."""
    attempts = _timed_out_solve(monkeypatch)
    first = drive.run_count(26, Options(run_dir=tmp_path))
    assert first["decision"]["decision"] == "no-view"
    assert not (drive.count_dir(tmp_path, 26) / "solve/witness.json").exists()
    for stage in ("regularize", "import"):
        again = drive.run_count(26, Options(run_dir=tmp_path, from_stage=stage))
        assert (again["status"], again["error"]) == ("timeout", None)
        assert again["solve"]["attempts"] == attempts
        assert again["decision"] == first["decision"]
    # With no input, the count says to run from the input; with no solve and no report
    # to keep it, from the solve.
    unsolved = drive.run_count(27, Options(run_dir=tmp_path, from_stage="regularize"))
    assert unsolved["status"] == "error"
    assert "--from-stage input" in unsolved["error"]
    (drive.count_dir(tmp_path, 27) / "input.txt").write_text(
        drive.input_text(witness(27)), encoding="utf-8"
    )
    unsolved = drive.run_count(27, Options(run_dir=tmp_path, from_stage="regularize"))
    assert unsolved["status"] == "error"
    assert "--from-stage solve" in unsolved["error"]


def test_a_replica_patch_is_applied_to_a_copy_and_never_under_vendor(tmp_path: Path) -> None:
    before = vendor_listing()
    rows = [drive.batch_row(26, drive.case_facts(26), witness(26))]
    replica = drive.build_replica(tmp_path / "run", rows)
    assert drive.solver_tree(replica, []) == replica / "search/exact"
    patched = drive.solver_tree(replica, ["probe-flat-stall-stop"])
    assert patched.parent.parent.parent == replica / "patched"
    assert patched.parent.parent.name.startswith("probe-flat-stall-stop-")
    assert drive.solver_tree(replica, ["probe-flat-stall-stop"]) == patched
    assert vendor_listing() == before
    pristine = (drive.VENDOR / "search/exact/exactsolve.py").read_text()
    assert (replica / "search/exact/exactsolve.py").read_text() == pristine
    text = (patched / "exactsolve.py").read_text()
    assert text != pristine
    assert "vendor/evand-regularize/README.md" in "".join(text.splitlines(keepends=True)[:20])
    assert "nr > prev / 10" in text
    for name in ("geom.py", "verify_cert.py", "verify_cert2.py"):
        vendored = drive.VENDOR / "search/exact" / name
        assert (patched / name).read_bytes() == vendored.read_bytes()
    with pytest.raises(drive.EvandRunError, match="not recorded"):
        drive.solver_tree(replica, ["no-such-patch"])


def test_a_count_solved_with_a_replica_patch_names_it_and_the_receipt_lists_it() -> None:
    applied = drive.applied_patches(["probe-flat-stall-stop"])
    assert applied[0]["kind"] == "replica"
    assert applied[0]["path"] == "search/exact/exactsolve.py"
    assert drive.vendored_pin()["patches"] == []  # a replica patch is not every count's
    patched = {**REPORT, "generator": {**REPORT["generator"], "patches": applied}}
    record = drive.regularization_record(patched)
    assert record is not None
    assert "evand/square-packing@675a5ea+probe-flat-stall-stop," in record["method"]
    rows = [
        {"n": 290, "replica_patches": ["probe-flat-stall-stop"]},
        {"n": 302, "replica_patches": ["probe-flat-stall-stop"]},
        {"n": 258, "replica_patches": []},
    ]
    generator = drive.run_generator(rows)
    assert [patch["name"] for patch in generator["patches"]] == ["probe-flat-stall-stop"]
    assert generator["patches"][0]["counts"] == [290, 302]
    assert drive.run_generator(rows[2:])["patches"] == []


def test_a_first_pass_with_the_stall_stop_patch_certifies_n26_as_the_plain_solve_does(
    tmp_path: Path,
) -> None:
    """The first-pass launcher and the patched solver change neither the point nor the
    certificate where upstream's own solve certifies on its first pass."""
    rows = [drive.batch_row(26, drive.case_facts(26), witness(26))]
    replica = drive.build_replica(tmp_path / "run", rows)
    directory = drive.count_dir(tmp_path / "run", 26)
    drive.write_text(directory / "input.txt", drive.input_text(witness(26)))
    both = drive.PLAIN.climb(drive.STALL_STOP).climb(drive.FIRST_PASS)
    climbed = drive.solve(directory, replica, 300, both, name="solve-both")
    plain = drive.solve(directory, replica, 300)
    assert climbed["gate"] == plain["gate"] == "certified"
    assert climbed["rungs"] == ["stall-stop", "first-pass"]
    assert drive.attempt_of(directory / "solve-both") == both.record()
    for name in ("witness.exact.txt", "witness.cert"):
        assert (directory / "solve-both" / name).read_bytes() == (
            directory / "solve" / name
        ).read_bytes()


def test_a_regularizer_refusal_keeps_its_reason_when_decided_again() -> None:
    report = {
        "n": 303,
        "status": "generator-failed",
        "solve": {"status": "KKT local min"},
        "regularize": {"place": "ok", "cert_ok": False},
        "outputs": {"solved": None, "same": None, "same_refusal": None},
        "decision": {"row": 1, "reason": "no view: solve KKT local min"},
    }
    measured = drive.measured_from_report(report, "solved")
    assert measured.status == "regularize: upstream's checker refused the certificate"
    kept = {**report, "decision": {"row": 1, "reason": "no view: regularize timeout"}}
    assert drive.measured_from_report(kept, "solved").status == "regularize timeout"
    unsolved = {**report, "solve": {"status": "not jammed"}, "regularize": None}
    assert drive.measured_from_report(unsolved, "solved").status == "solve not jammed"
    # A solve through the relaxed gate reached the regularizer as a certified one does.
    relaxed = {
        **report,
        "solve": {
            "status": "certificate invalid",
            "newton_converged": True,
            "second_order": "PD: strict local minimum",
        },
    }
    measured = drive.measured_from_report(relaxed, "solved")
    assert measured.status == "regularize: upstream's checker refused the certificate"


def test_reclassify_refreshes_a_stale_bound_from_the_case_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A run decided before a register result moved `U` holds its view at row 3; read
    again from the case record, which now holds the view's side as its exact form, the
    same measurements admit it, and the receipt names the count whose bound moved."""
    side = Fraction(563, 100)
    run_dir = tmp_path / "run"
    directory = run_dir / "n-026"
    directory.mkdir(parents=True)
    same = {"side_exact": "563/100", "relation": "same", "routes": ROUTES_OK, "minus_U": "x"}
    report = {
        **DECIDED,
        "verified_upper_bound": "5.64",
        "verified_upper_bound_exact_form": "141/25",
        "shades": {**DECIDED["shades"], "regressions": []},
        "source": {"s_W_exact": "563/100", "provenance": {"source_key": None}},
        "outputs": {"same": same, "solved": None, "same_refusal": None},
        "identity": {"one_to_one": True, "moved": 4, "max_move": "0.1", "turned": [2]},
        "regularize": {"level": 2, "changed_angles": [2]},
        "solve": {"status": "KKT local min"},
    }
    (directory / "report.json").write_text(json.dumps(report), encoding="utf-8")
    receipt = {"counts": [{"n": 26}], "cost": {"cpu_seconds": 1.0}}
    (run_dir / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
    monkeypatch.setattr(drive, "_current_histograms", lambda _n, _report: None)

    stale = drive.reclassify(run_dir)
    assert stale["counts"][0]["row"] == 3
    assert "refreshed_bounds" not in stale["reclassified"]

    monkeypatch.setattr(
        drive,
        "case_facts",
        lambda _n: {
            "verified_upper_bound": "5.64",
            "exact_form": str(side),
            "reported": "5.63",
            "found_by": [],
            "improved_by": [],
            "source_key": None,
        },
    )
    fresh = drive.reclassify(run_dir, refresh_bounds=True)
    redone = json.loads((directory / "report.json").read_text(encoding="utf-8"))
    assert redone["verified_upper_bound"] == "5.64"
    assert redone["verified_upper_bound_exact_form"] == "563/100"
    assert redone["outputs"]["same"]["minus_U"] == "0.000e+00"
    assert redone["decision"]["decision"] == "admit"
    assert fresh["counts"][0]["row"] == 10
    assert fresh["cost"] == receipt["cost"]
    assert fresh["reclassified"]["refreshed_bounds"] == [
        {
            "n": 26,
            "before": {"value": "5.64", "exact_form": "141/25"},
            "after": {"value": "5.64", "exact_form": "563/100"},
        }
    ]
    # A second refresh finds the record and the report agreeing, and moves nothing.
    again = drive.reclassify(run_dir, refresh_bounds=True)
    assert again["reclassified"]["refreshed_bounds"] == []


def test_a_run_block_keeps_how_a_receipts_cost_was_measured(tmp_path: Path) -> None:
    measured = tmp_path / "measured"
    measured.mkdir()
    receipt = {"counts": [{"n": 26, "decision": "admit"}], "cost": {"cpu_seconds": 2.5}}
    (measured / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
    assert "note" not in drive.run_block(measured, "measured")["cost"]
    # A run writes how it measured itself; that default is not a note (#559 review A1).
    receipt["cost"] = {"cpu_seconds": 2.5, "measured_by": drive.RUN_MEASURED_BY}
    (measured / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
    assert "note" not in drive.run_block(measured, "measured")["cost"]

    rebuilt = tmp_path / "rebuilt"
    rebuilt.mkdir()
    sentence = "reconstructed after the run: CPU summed from the count reports"
    receipt["cost"] = {"cpu_seconds": 2.5, "wall_seconds": 9.0, "measured_by": sentence}
    (rebuilt / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
    cost = drive.run_block(rebuilt, "rebuilt")["cost"]
    assert cost == {"cpu_seconds": 2.5, "wall_seconds": 9.0, "workers": 1, "note": sentence}


def test_a_run_is_dated_by_its_receipt_and_not_by_its_files_time(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """#548 review B5: Git keeps no modification times, so a copied or restored run
    directory would otherwise be dated the day it was copied."""
    monkeypatch.setenv("PACK_JOBS", "1")
    root, layout = scratch_tree(tmp_path)
    run_dir = a_run(root, layout, tmp_path / "full")
    path = run_dir / "receipt.json"
    os.utime(path, (0, 0))
    assert drive.run_block(run_dir, "evand-regularize-full")["finished"] == "2026-10-12"

    receipt = json.loads(path.read_text(encoding="utf-8"))
    undated = {key: value for key, value in receipt.items() if key != "finished"}
    path.write_text(json.dumps(undated), encoding="utf-8")
    assert drive.run_block(run_dir, "evand-regularize-full")["finished"] is None
    # A run from before the driver recorded the time, never admitted, is refused before
    # the layer is touched...
    before = (layout.index.read_text(encoding="utf-8"), layout.view(4).read_bytes())
    with pytest.raises(drive.EvandRunError, match="records no finish time"):
        drive.write_layer([run_dir], root, "admitted")
    assert (layout.index.read_text(encoding="utf-8"), layout.view(4).read_bytes()) == before
    # ...and one the index already dates keeps that date when it is admitted again.
    path.write_text(json.dumps(receipt), encoding="utf-8")
    assert drive.write_layer([run_dir], root, "admitted")["written"] == [4]
    path.write_text(json.dumps(undated), encoding="utf-8")
    assert drive.write_layer([run_dir], root, "admitted")["written"] == [4]
    (run,) = json.loads(layout.index.read_text(encoding="utf-8"))["runs"]
    assert run["finished"] == "2026-10-12"
    assert axis.check_atlas(layout) == []


def test_a_view_is_credited_to_the_packing_it_redraws() -> None:
    """#548 review B1: at 182, 206, 241, 268 and 297 the case record credits Evan Daniel's
    exact optimum, and the view at the witness's side redraws Francisco Couzo's packing."""
    record = {
        "source_key": "[evand exact optima 2026-10-05]",
        "found_by": ["Francisco Couzo"],
        "improved_by": ["Evan Daniel"],
    }
    couzo = "[franciscouzo square-packing 2026-09-27]"
    assert drive.packing_credit(record, couzo, "bound") == record
    assert drive.packing_credit(record, couzo, "same") == {
        "source_key": couzo,
        "found_by": ["Francisco Couzo"],
        "improved_by": [],
    }
    assert drive.packing_credit(record, record["source_key"], "same") == record
    # A witness that names its source in other words, where the record credits no
    # improvement, is the reported packing.
    kingbird = {"source_key": "[Kingbird]", "found_by": ["Erich Friedman"], "improved_by": []}
    assert (
        drive.packing_credit(kingbird, "Kingbird derived numerical facts", "same") == kingbird
    )
    # A Kingbird-derived witness is the packing the record credits, improvers and all (29,
    # 54 and 87): its label names `[Kingbird]`.
    improved = {
        "source_key": "[Kingbird]",
        "found_by": ["Thomas Schadt"],
        "improved_by": ["David Ellsworth"],
    }
    assert (
        drive.packing_credit(improved, "Kingbird derived numerical facts", "same") == improved
    )
    assert drive.packing_credit(None, couzo, "same") is None


def test_a_drawn_views_credit_is_restated_in_its_entry_and_its_view_together(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PACK_JOBS", "1")
    root, layout = scratch_tree(tmp_path)
    path = root / "packing/witnesses/known-best/n-004.yaml"
    row = load_witness(path, fallback_schema=drive.WITNESS_SCHEMA)
    row["source"]["key"] = "[row finder 2026]"
    write_witness(path, row)
    assert axis.main(["--update-atlas"], layout=layout) == 0
    run_dir = a_run(root, layout, tmp_path / "full")
    report_path = run_dir / "n-004/report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["regularization"]["provenance"] = {
        "source_key": "[exact optima]",
        "found_by": ["Finder"],
        "improved_by": ["Improver"],
    }
    report_path.write_text(json.dumps(report), encoding="utf-8")
    assert drive.write_layer([run_dir], root, "admitted")["written"] == [4]

    assert drive.restate_provenance(root, write=False) == [4]
    assert drive.main(["provenance", "--repo-root", str(root), "--check"]) == 1
    assert drive.restate_provenance(root) == [4]
    (entry,) = json.loads(layout.index.read_text(encoding="utf-8"))["entries"]
    assert entry["regularization"]["provenance"] == {
        "source_key": "[row finder 2026]",
        "found_by": ["Finder"],
        "improved_by": [],
    }
    view = load_yaml(gzip.decompress(layout.view(4).read_bytes()).decode())["witness"]
    assert view["certificate"]["regularization"] == entry["regularization"]
    assert axis.check_atlas(layout) == []
    assert drive.restate_provenance(root) == []


# --------------------------------------------------------------------------------------
# Review B of #511: the bound held exactly, stage reuse, the verdict bound to its bytes
# --------------------------------------------------------------------------------------


def _below_root_of_two_half(side: Fraction) -> bool:
    """Exactly whether `side` < 2 + sqrt(2)/2, n = 5's verified upper bound."""
    gap = side - 2
    return gap < 0 or 4 * gap * gap < 2


def test_a_closed_form_bound_is_held_exactly_and_is_never_a_frame() -> None:
    """B3: a closed form's 60-digit value lies above `U` (by 1.3e-61 at n = 5), so a side
    there was labelled `bound` and row 3 decided against the rounding."""
    from devtools.apply_exact_ceilings import bound_value  # noqa: PLC0415

    facts = drive.case_facts(5)
    bound = drive.verified_bound(facts)
    assert bound is not None
    assert (bound.rational, bound.unread) == (None, None)
    assert drive.upper_bound(facts) is None
    sixty = bound_value(
        {"value": facts["verified_upper_bound"], "exact_form": facts["exact_form"]}
    )
    assert not _below_root_of_two_half(sixty)
    assert bound.compare(sixty) == 1
    assert drive.side_relation(sixty, None, drive.upper_bound(facts)) == "solved"
    for offset in (Fraction(1, 10**59), Fraction(1, 10**62), Fraction(1, 10**90)):
        for side in (sixty - offset, sixty + offset):
            expected = -1 if _below_root_of_two_half(side) else 1
            assert bound.compare(side) == expected
    # Row 3 is decided against the closed form itself.
    below = replace(SAME, side=sixty - Fraction(1, 10**59), upper=None, bound=bound)
    assert classify(below).row == 3
    above = replace(below, side=sixty)
    assert classify(above).decision == "admit"
    # A view at the 60-digit value, decided from a report, is `solved` and held.
    report = {
        **DECIDED,
        "verified_upper_bound": facts["verified_upper_bound"],
        "verified_upper_bound_exact_form": facts["exact_form"],
        "shades": {**DECIDED["shades"], "regressions": []},
        "source": {"s_W_exact": "27/10"},
        "outputs": {
            "same": None,
            "solved": {"side_exact": drive.literal(sixty), "routes": ROUTES_OK},
        },
        "regularize": {"level": 2},
    }
    measured = drive.measured_from_report(report, "solved")
    assert measured.relation == "solved"
    assert classify(measured).row == 4


def test_every_closed_form_bound_is_read_exactly_or_refused() -> None:
    """B3: each frontier bound is a rational, an isolated root, or unread (n = 11's
    `root(P_trump11, ...)`), and an unread bound decides nothing: no admission."""
    unread = []
    for n in range(1, 325):
        facts = drive.case_facts(n)
        bound = drive.verified_bound(facts)
        if bound is None:
            continue
        if bound.unread is not None:
            unread.append(n)
            continue
        if bound.rational is None:
            assert bound.interval is not None
            low, high = bound.interval
            assert high - low <= drive.BOUND_INTERVAL_WIDTH
            assert len(bound.polynomial) >= 3
    assert unread == [11]
    eleven = drive.verified_bound(drive.case_facts(11))
    assert eleven is not None
    assert eleven.compare(Fraction(4)) is None
    decided = classify(replace(SAME, upper=None, bound=eleven))
    assert (decided.row, decided.decision) == (None, "review")
    assert "could not be read exactly" in decided.reason


@pytest.fixture(scope="module")
def n26_run(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """One real run of n = 26, copied by each test that changes it."""
    run_dir = tmp_path_factory.mktemp("n26") / "run"
    drive.run([26], Options(run_dir=run_dir), workers=1)
    return run_dir


def _copy_run(n26_run: Path, tmp_path: Path) -> Path:
    import shutil  # noqa: PLC0415

    return Path(shutil.copytree(n26_run, tmp_path / "run", symlinks=True))


def test_a_stored_fewest_regularization_is_not_reimported_as_conservative(
    n26_run: Path, tmp_path: Path
) -> None:
    """B1: `--from-stage import` decides and labels a stored output by the settings it
    ran with; asked for others, it refuses rather than admit a `fewest` view at row 10."""
    run_dir = _copy_run(n26_run, tmp_path)
    stored = drive.count_dir(run_dir, 26) / "regularize.json"
    document = json.loads(stored.read_text())
    document["variant"] = "fewest"
    stored.write_text(json.dumps(document))
    refused = drive.run_count(26, Options(run_dir=run_dir, from_stage="import"))
    assert refused["status"] == "error"
    assert "--variant fewest" in refused["error"]
    assert "--from-stage regularize" in refused["error"]
    assert "decision" not in refused
    assert drive.layer_candidate(refused, "admitted") is None
    asked = drive.run_count(26, Options(run_dir=run_dir, from_stage="import", variant="fewest"))
    assert asked["status"] == "ok"
    assert asked["generator"]["variant"] == "fewest"
    assert asked["parameters"]["variant"] == "fewest"
    assert asked["decision"]["decision"] != "admit"
    for name in ("view-solved.yaml", "view-same.yaml"):
        view = load_yaml((drive.count_dir(run_dir, 26) / name).read_text())["witness"]
        assert view["certificate"]["variant"] == "fewest"
    # An output written before the frame was recorded started from the KKT point.
    del document["frame"]
    settings = drive.stored_settings(document, Options(run_dir=run_dir, variant="fewest"))
    assert settings.frame == "kkt"
    with pytest.raises(drive.EvandRunError, match="--frame kkt"):
        drive.stored_settings(document, Options(run_dir=run_dir, frame="witness"))


def _moved_witness(tmp_path: Path) -> Path:
    """n = 26's witness with square 1 moved left by 1e-7: another input, same id."""
    text = drive.witness_path(26).read_text()
    old = "    center:\n    - '0.5'\n    - '5.12132034355964257320253308632'"
    assert old in text
    moved = tmp_path / "n-026.yaml"
    moved.write_text(text.replace(old, old.replace("'0.5'", "'0.4999999'"), 1))
    return moved


def test_a_stage_is_not_reused_from_another_witness(
    n26_run: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """B2: the report names the exact solve's input by digest and the witness it was
    written from; a later stage over a changed witness's input is refused."""
    import hashlib  # noqa: PLC0415

    report = json.loads((drive.count_dir(n26_run, 26) / "report.json").read_text())
    directory = drive.count_dir(n26_run, 26)
    assert (
        report["input"]["sha256"]
        == hashlib.sha256((directory / "input.txt").read_bytes()).hexdigest()
    )
    assert report["input"]["written_from"] == {
        "path": report["source"]["path"],
        "sha256": report["source"]["sha256"],
    }
    receipt = json.loads((n26_run / "receipt.json").read_text())
    assert "input.txt" in receipt["solve_outputs"]["26"]
    run_dir = _copy_run(n26_run, tmp_path)
    original = drive.witness_path(26)
    moved = _moved_witness(tmp_path)
    monkeypatch.setattr(drive, "witness_path", lambda n: moved if n == 26 else original)
    for stage in ("solve", "regularize", "import"):
        refused = drive.run_count(26, Options(run_dir=run_dir, from_stage=stage))
        assert refused["status"] == "error"
        assert "--from-stage input" in refused["error"]
        assert "decision" not in refused
        assert not list(drive.count_dir(run_dir, 26).glob("view-*.yaml"))
    # A change that leaves the input as it was reuses the stage, and the report says
    # which witness the input was written from.
    noted = tmp_path / "noted" / "n-026.yaml"
    noted.parent.mkdir()
    noted.write_text(original.read_text() + "# a note that changes no square\n")
    monkeypatch.setattr(drive, "witness_path", lambda n: noted if n == 26 else original)
    again = drive.run_count(26, Options(run_dir=run_dir, from_stage="regularize"))
    assert again["status"] == "ok"
    assert again["input"]["written_from"]["sha256"] == report["source"]["sha256"]
    assert again["source"]["sha256"] != report["source"]["sha256"]
    # A regularization that started from the witness's own pose is reused only from
    # today's pose.
    directory = drive.count_dir(run_dir, 26)
    stored = json.loads((directory / "regularize.json").read_text())
    (directory / "regularize.json").write_text(json.dumps({**stored, "frame": "witness"}))
    framed = directory / "frame-witness/witness.exact.txt"
    framed.parent.mkdir(exist_ok=True)
    today = drive.source_frame(witness(26))
    framed.write_text(drive.frame_text(witness(26), today))
    drive.reused_input(directory, witness(26), today)
    framed.write_text(framed.read_text().replace("26 ", "26  ", 1))
    with pytest.raises(drive.EvandRunError, match="--from-stage regularize"):
        drive.reused_input(directory, witness(26), today)


def test_layer_decides_the_view_it_writes_rather_than_identifying_its_bytes(
    n26_run: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """B5 of review B and C1 of review C: an interrupted re-run leaves no earlier verdict
    beside its views, and `layer` decides the file it writes as it is now. A comment-only
    edit leaves the same valid view and is taken; a view that no longer verifies, another
    view's id, or a report whose settings are not its stored regularization's is refused.
    The Git blob id stays in the report as provenance, and nothing compares it (OR-18)."""
    from devtools.retained_data import git_blob  # noqa: PLC0415

    run_dir = _copy_run(n26_run, tmp_path)
    directory = drive.count_dir(run_dir, 26)
    report = json.loads((directory / "report.json").read_text())
    for name in ("solved", "same"):
        block = report["outputs"][name]
        assert block["git_blob"] == git_blob((directory / block["path"]).read_bytes())

    def killed(**_kwargs: object) -> None:
        raise KeyboardInterrupt

    with monkeypatch.context() as patch:
        patch.setattr(drive, "_measure_view", killed)
        with pytest.raises(KeyboardInterrupt):
            drive.run_count(26, Options(run_dir=run_dir, from_stage="import"))
    assert not (directory / "report.json").exists()

    # Admission (#548's `evand_candidates`, which `layer` writes from) finds no report to
    # admit after the interrupted run, and admits the decided one, deciding its view
    # again as it is now. The blob ids a report records are its provenance and decide
    # nothing (OR-18).
    assert drive.evand_candidates([run_dir])[0] == []
    decided = drive.run_count(26, Options(run_dir=run_dir, from_stage="import"))
    decided["decision"] = {"row": 10, "decision": "admit", "reason": "a fixture"}
    (directory / "report.json").write_text(json.dumps(decided))
    chosen = drive.layer_candidate(decided, "admitted")
    assert chosen == "same"
    view = directory / f"view-{chosen}.yaml"
    pristine = view.read_text()

    def admitted() -> tuple[list[int], dict[str, str]]:
        found, _runs, refused = drive.evand_candidates([run_dir])
        return [item.n for item in found], refused

    assert admitted() == ([26], {})
    # A comment changes the bytes, and with them the Git blob id, but not the view.
    view.write_text(pristine + "# reviewed by hand\n")
    assert git_blob(view.read_bytes()) != decided["outputs"][chosen]["git_blob"]
    assert admitted() == ([26], {})
    # Another view's id is not the view the report decided.
    view.write_text(pristine.replace("-regularized", "-edited", 1))
    found, refused = admitted()
    assert found == []
    assert "view-same.yaml's id is W-known-best-n026-edited" in refused["26"]
    # A square moved onto its neighbour fails both exact routes.
    document = load_yaml(pristine)
    squares = document["witness"]["squares"]
    squares[0] = {**squares[0], **{key: squares[1][key] for key in ("center", "corners")
                                   if key in squares[1]}}  # fmt: skip
    view.write_text(drive.witness_document(document["witness"]))
    found, refused = admitted()
    assert found == []
    assert "fails exact_verify and independent" in refused["26"]
    # A report labelled with other settings than its stored regularization ran with.
    view.write_text(pristine)
    labelled = {**decided, "generator": {**decided["generator"], "variant": "fewest"}}
    (directory / "report.json").write_text(json.dumps(labelled))
    found, refused = admitted()
    assert found == []
    assert "--variant conservative (its report says: fewest)" in refused["26"]
    (directory / "report.json").write_text(json.dumps(decided))
    assert admitted() == ([26], {})


def test_a_receipt_keeps_each_runs_solve_outputs_and_parameters(tmp_path: Path) -> None:
    """B6: a run into a directory that holds an earlier run's rows keeps their digests
    and the settings each row ran with."""
    reports = {}
    for n, variant in ((26, "conservative"), (10, "fewest")):
        directory = drive.count_dir(tmp_path, n)
        directory.mkdir(parents=True)
        (directory / "input.txt").write_text(f"{n} input\n")
        (directory / "regularize.cert").write_text(f"{n} certificate\n")
        options = Options(run_dir=tmp_path, variant=variant)
        reports[n] = {
            "n": n,
            "status": "ok",
            "parameters": drive.run_parameters(options),
            "decision": {"row": 4, "decision": "held"},
        }
    cost = {"cpu_seconds": 1.0, "wall_seconds": 1.0}
    first = drive.write_receipt(tmp_path, {26: reports[26]}, Options(run_dir=tmp_path), 1, cost)
    assert sorted(first["solve_outputs"]) == ["26"]
    # The earlier run's file changes on disk after its receipt named it.
    (drive.count_dir(tmp_path, 26) / "regularize.cert").write_text("changed\n")
    second = drive.write_receipt(
        tmp_path, {10: reports[10]}, Options(run_dir=tmp_path, variant="fewest"), 1, cost
    )
    assert sorted(second["solve_outputs"], key=int) == ["10", "26"]
    assert second["solve_outputs"]["26"] == first["solve_outputs"]["26"]
    variants = {row["n"]: row["parameters"]["variant"] for row in second["counts"]}
    assert variants == {10: "fewest", 26: "conservative"}


def test_a_patched_solver_is_rebuilt_when_its_patch_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """B7: the patched tree is named by what it is built from, so an edited patch never
    runs as the old one."""
    rows = [drive.batch_row(26, drive.case_facts(26), witness(26))]
    replica = drive.build_replica(tmp_path / "run", rows)
    first = drive.solver_tree(replica, ["probe-flat-stall-stop"])
    record = drive.replica_patches()["probe-flat-stall-stop"]
    edited = tmp_path / "edited.patch"
    edited.write_text("an edited patch's prose\n" + (drive.REPO / record["patch"]).read_text())
    monkeypatch.setattr(
        drive,
        "replica_patches",
        lambda: {"probe-flat-stall-stop": {**record, "patch": str(edited)}},
    )
    second = drive.solver_tree(replica, ["probe-flat-stall-stop"])
    assert second != first
    assert (second / "exactsolve.py").read_text() == (first / "exactsolve.py").read_text()


def test_the_same_side_view_names_its_source_by_digest(n26_run: Path) -> None:
    """B8: the driver's provenance wins over the resolver's where both name a field."""
    directory = drive.count_dir(n26_run, 26)
    report = json.loads((directory / "report.json").read_text())
    view = load_yaml((directory / "view-same.yaml").read_text())["witness"]
    certificate = view["certificate"]
    assert certificate["kind"] == "evand-regularized-view"
    assert certificate["relation"] == "same"
    assert certificate["derived_from"] == {
        "path": report["source"]["path"],
        "sha256": report["source"]["sha256"],
    }
    assert certificate["resolver"] == {
        "kind": "same-side-view",
        "derived_from": "W-known-best-n026",
    }
    assert certificate["resolve"]["tool"] == "devtools.regularize_same_side"


def test_reclassify_says_when_a_stored_bound_is_stale(n26_run: Path, tmp_path: Path) -> None:
    """B10: `reclassify` decides on the stored `U` and lists the counts whose case record
    has moved it since."""
    run_dir = _copy_run(n26_run, tmp_path)
    assert drive.reclassify(run_dir)["reclassified"]["stale_bounds"] == []
    path = drive.count_dir(run_dir, 26) / "report.json"
    report = json.loads(path.read_text())
    report["verified_upper_bound"], report["verified_upper_bound_exact_form"] = "5.7", None
    path.write_text(json.dumps(report))
    assert drive.reclassify(run_dir)["reclassified"]["stale_bounds"] == [26]


def test_a_copy_reclassified_under_another_name_is_marked_by_its_receipt(
    n26_run: Path, tmp_path: Path
) -> None:
    """#548 review C, C3: the receipt says which run is a reclassified copy, so the layer
    records its cost once without guessing from equal seconds. Decided again in place, a
    run is its own; on a copy under another name, `reclassified.from` names the run it was
    copied from, a copy of that copy keeps it, and the run block carries the mark."""
    import shutil  # noqa: PLC0415

    original = _copy_run(n26_run, tmp_path)
    assert json.loads((original / "receipt.json").read_text())["run_directory"] == "run"
    assert "from" not in drive.reclassify(original)["reclassified"]
    assert "reclassified_from" not in drive.run_block(original, "evand-regularize-run")
    copy = Path(shutil.copytree(original, tmp_path / "refreshed", symlinks=True))
    assert drive.reclassify(copy)["reclassified"]["from"] == "evand-regularize-run"
    block = drive.run_block(copy, "evand-regularize-refreshed")
    assert block["reclassified_from"] == "evand-regularize-run"
    assert block["cost"] == drive.run_block(original, "evand-regularize-run")["cost"]
    again = Path(shutil.copytree(copy, tmp_path / "again", symlinks=True))
    assert drive.reclassify(again)["reclassified"]["from"] == "evand-regularize-run"
    # A receipt from before it recorded its directory says nothing, and the layer refuses
    # the repeated cost unmarked rather than guess which run is the copy.
    receipt = json.loads((copy / "receipt.json").read_text())
    del receipt["run_directory"], receipt["reclassified"]["from"]
    (copy / "receipt.json").write_text(json.dumps(receipt))
    assert "from" not in drive.reclassify(copy)["reclassified"]
    runs = [
        {**drive.run_block(path, f"evand-regularize-{path.name}"), "finished": "2026-10-14"}
        for path in (copy, original)
    ]
    (problem,) = axis.repeated_costs(runs)
    assert "neither is marked as the other's reclassified copy" in problem
    # A run the index already records as the copy keeps that mark, as an undated run
    # keeps the index's date, so re-admitting it from such a receipt changes nothing.
    held = [{**runs[0], "reclassified_from": "evand-regularize-run"}]
    (kept,) = drive.dated_runs([runs[0]], held)
    assert kept["reclassified_from"] == "evand-regularize-run"
    assert axis.repeated_costs([kept, runs[1]]) == []


def test_reclassify_sends_a_report_mislabelled_before_b1_to_review(
    n26_run: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """C3 of review C: a report written before B1's fix could call a `fewest`
    regularization `conservative` (n = 129 in review B's run). `reclassify` must not
    decide it again from those labels, and so must not bring it back as row 10 `admit`."""
    run_dir = _copy_run(n26_run, tmp_path)
    receipt = drive.reclassify(run_dir)
    assert receipt["reclassified"]["stale_settings"] == []
    report_path = drive.count_dir(run_dir, 26) / "report.json"
    admitted = json.loads(report_path.read_text())
    assert (admitted["decision"]["row"], admitted["decision"]["decision"]) == (10, "admit")
    stored = drive.count_dir(run_dir, 26) / "regularize.json"
    pristine = stored.read_text()
    stored.write_text(json.dumps({**json.loads(pristine), "variant": "fewest"}))
    assert drive.main(["reclassify", "--run-dir", str(run_dir)]) == 0
    assert "sent to review: at [26]" in capsys.readouterr().out
    receipt = json.loads((run_dir / "receipt.json").read_text())
    assert receipt["reclassified"]["stale_settings"] == [26]
    report = json.loads(report_path.read_text())
    assert (report["decision"]["row"], report["decision"]["decision"]) == (None, "review")
    assert "--variant fewest (its report says: conservative)" in report["decision"]["reason"]
    assert report["regularization"] is None
    assert drive.layer_candidate(report, "admitted") is None
    assert 26 in receipt["review_queue"]
    stored.write_text(pristine)
    receipt = drive.reclassify(run_dir)
    assert receipt["reclassified"]["stale_settings"] == []
    report = json.loads(report_path.read_text())
    assert (report["decision"]["row"], report["decision"]["decision"]) == (10, "admit")


def test_a_closed_form_bound_narrower_than_its_evaluation_is_still_read() -> None:
    """SymPy refines sqrt(16 + 10^-40)'s isolating interval to 1.6e-82, below the 80-digit
    value's error, which then fell outside it and left the bound unread; the root is
    matched within that error instead, and a rational side is decided against it."""
    bound = drive.verified_bound(
        {"verified_upper_bound": "4.0", "exact_form": "sqrt(16 + 1/10**40)"}
    )
    assert bound is not None
    assert bound.unread is None
    assert bound.compare(Fraction(4)) == -1
    assert bound.compare(Fraction(4) + Fraction(1, 10**40)) == 1
    assert f"{bound.difference(Fraction(4)):.3e}" == "-1.250e-41"
