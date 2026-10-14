"""The regularized views registered as verified upper bounds (T-155).

`devtools.register_regularized_bounds` retains each view whose exact side lies below its
case's verified upper bound, decides it on both maintained exact routes, makes three
controls of it, and writes the case records' verified upper lane. These tests hold the
committed receipts, the retained views and the case records to each other, the layer to
its own output, and the controls' construction to the outcomes it promises.
"""

from __future__ import annotations

import json
import re
from decimal import Decimal
from fractions import Fraction

import pytest

from devtools import apply_exact_ceilings, render_case_verifiers
from devtools import register_regularized_bounds as registered
from devtools.apply_upper_bound_packets import normalized
from sqpack.assurance import bounds_agree_at_declared_precision


def test_the_receipts_the_views_and_the_records_agree() -> None:
    assert registered.problems() == []


def test_no_held_or_rehoused_count_is_registered() -> None:
    selection = json.loads(registered.SELECTION.read_text(encoding="utf-8"))
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
    for n, row in registered.committed().items():
        upper = registered.case_front(n)["verified_upper_bound"]
        assert upper["value"] == row["earlier_verified"]["value"], n
        assert not row["value_raised"], n
        assert Fraction(Decimal(upper["value"])) >= Fraction(upper["exact_form"]), n
        assert Fraction(upper["exact_form"]) == Fraction(row["side"]), n


@pytest.mark.parametrize("n", [28, 29, 37, 50, 204, 300])
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
    for n, row in registered.committed().items():
        case = registered.case_front(n)
        agrees = bounds_agree_at_declared_precision(
            case["reported_upper_bound"], case["verified_upper_bound"]
        )
        assert agrees == row["agrees_with_report"], n
        body = (registered.FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
        assert (registered.CEILING_HEADING in body) != agrees, n
        assert registered.SECTION in body, n
        assert registered.DATED in body, n


def test_every_control_reached_its_outcome_on_both_routes() -> None:
    receipt = json.loads(registered.CONTROLS.read_text(encoding="utf-8"))
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
    for n in registered.committed():
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


def test_the_controls_are_151_distinct_mutants() -> None:
    """At a same-side view the least top or right clearance is 0, so the box shrunk past it
    is the box shrunk by one unit: the 177 decisions are of 151 distinct mutants, as the
    evidence entry and the package README say (review B6)."""
    receipt = json.loads(registered.CONTROLS.read_text(encoding="utf-8"))
    touching = {
        row["n"]
        for row in receipt["rows"]
        if row["control"] == "side-shrunk-past-clearance" and row["clearance"] == 0
    }
    assert touching == {
        n for n, row in registered.committed().items() if row["output"] == "same"
    }
    assert receipt["controls"] - len(touching) == 151
