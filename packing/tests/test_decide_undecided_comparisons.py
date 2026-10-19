"""The ledger's undecided PR #574 comparisons are decided exactly, and the receipt holds.

``devtools.decide_undecided_comparisons`` decides a rational against a polynomial root by
Sturm isolation and one sign, and a number-field side against a closed form by exact
arithmetic. These tests check the polynomial reader, the Sturm count, both rules on
small known cases, a second route by mpmath at the cheap rows of the receipt, and, in
the deep surface, the whole receipt against a fresh decision.
"""

from __future__ import annotations

import json
from fractions import Fraction

import mpmath as mp
import pytest

from devtools import decide_undecided_comparisons as tool


def test_parse_polynomial_reads_braced_and_bare_powers() -> None:
    assert tool.parse_polynomial("s^6-24s^5+212s^4-812s^3+1025s^2+882s-1615=0") == [
        1,
        -24,
        212,
        -812,
        1025,
        882,
        -1615,
    ]
    assert tool.parse_polynomial("4775s^{18}-2631254953=0")[:2] == [4775, 0]
    with pytest.raises(tool.DecisionError, match="repeated term"):
        tool.parse_polynomial("s^2+s^2-1")
    with pytest.raises(tool.DecisionError, match="not a polynomial"):
        tool.parse_polynomial("x^2-1")


def test_parse_polynomial_refuses_a_right_hand_side_other_than_zero() -> None:
    cubic = [1, 0, -1, 0]
    assert tool.parse_polynomial("s^3 - s = 0") == tool.parse_polynomial("s^3 - s") == cubic
    for text in ("s^3 - s = 1", "s^3 = s", "s^2 - 2 = 0 = 1"):
        with pytest.raises(tool.DecisionError, match="right-hand side is not 0"):
            tool.parse_polynomial(text)


def test_sturm_count_and_squarefree_refusal() -> None:
    assert tool.root_count([1, 0, -2], Fraction(1), Fraction(2)) == 1
    assert tool.root_count([1, 0, -2], Fraction(-2), Fraction(2)) == 2
    assert tool.root_count([1, 0, 0, -2], Fraction(-5), Fraction(5)) == 1
    with pytest.raises(tool.DecisionError, match="not squarefree"):
        tool.sturm_chain([1, -2, 1])
    with pytest.raises(tool.DecisionError, match="holds 2 roots"):
        tool.Root.isolate([1, 0, -2], Fraction(-2), Fraction(2))


def test_a_rational_against_a_root_is_one_sign() -> None:
    root2 = tool.Root.isolate([1, 0, -2], Fraction(1), Fraction(2))
    assert root2.compare(Fraction(141, 100)) == -1
    assert root2.compare(Fraction(142, 100)) == 1
    three_halves = tool.Root.isolate([2, -3], Fraction(1), Fraction(2))
    assert three_halves.compare(Fraction(3, 2)) == 0
    decided = tool.decide_rational(Fraction(99, 70), root2)
    assert decided["relation"] == "above"
    low, high = (float(decided["margin_bounds"][k]) for k in ("low", "high"))
    assert low <= 99 / 70 - 2**0.5 <= high


def test_the_closed_form_is_its_quartic_root() -> None:
    field, value = tool.closed_form("7 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))")
    field.refine_to(30)
    low, high = field.enclose(value)
    exact = mp.mpf(7) - mp.sqrt(2) / 2 + mp.sqrt(1 + mp.sqrt(2))
    assert float(low) <= float(exact) <= float(high)
    with pytest.raises(tool.DecisionError, match="not the closed form"):
        tool.closed_form("7 + sqrt(3)")


def test_a_field_side_equal_to_the_closed_form_and_one_that_is_not() -> None:
    side = {
        "minimal_polynomial": ["4", "0", "-12", "16", "-7"],
        "isolating_interval": ["4233/5000", "4234/5000"],
        "coefficients": ["7", "1"],
    }
    equal = tool.decide_fields(
        tool.field_side(side), tool.closed_form("7 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))"), side
    )
    assert equal["relation"] == "equal"
    shifted = side | {"coefficients": ["7", "1001/1000"]}
    above = tool.decide_fields(
        tool.field_side(shifted),
        tool.closed_form("7 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))"),
        shifted,
    )
    assert above["relation"] == "above"


def _receipt_rows() -> dict[int, dict[str, object]]:
    receipt = json.loads(tool.RESOLVED.read_text(encoding="utf-8"))
    return {row["n"]: row for row in receipt["rows"]}


@pytest.mark.parametrize("n", [17, 28, 37, 39, 54, 107, 178, 177])
def test_cheap_rows_of_the_receipt_redecide(n: int) -> None:
    sides = json.loads(tool.SIDES.read_text(encoding="utf-8"))
    assert tool.decide_row(n, sides) == _receipt_rows()[n]


@pytest.mark.parametrize("n", [28, 37, 39])
def test_a_second_route_agrees_on_the_margin(n: int) -> None:
    sides = json.loads(tool.SIDES.read_text(encoding="utf-8"))
    record, _ = tool.record_side(n)
    row = _receipt_rows()[n]
    with mp.workdps(300):
        poly = [int(c) for c in tool.parse_polynomial(_minimal_polynomial(n))]
        root = mp.findroot(lambda s: mp.polyval(poly, s), mp.mpf(record["print"]))
        value = Fraction(sides["sides"][str(n)]["value"])
        margin = mp.mpf(value.numerator) / value.denominator - root
        bounds = row["margin_bounds"]
        assert isinstance(bounds, dict)
        assert mp.mpf(bounds["low"]) <= margin <= mp.mpf(bounds["high"])


def _minimal_polynomial(n: int) -> str:
    lane = tool.parse_case(tool.FRONTIER / f"n-{n:03d}.md")["reported_upper_bound"]
    return str(lane["minimal_polynomial"])


def test_the_gated_rows_are_the_four_without_an_exact_record_side() -> None:
    receipt = json.loads(tool.RESOLVED.read_text(encoding="utf-8"))
    assert [row["n"] for row in receipt["gated"]] == [29, 55, 71, 83]
    assert len(receipt["rows"]) == 17
    for n in (29, 55, 71, 83):
        with pytest.raises(tool.DecisionError, match="no exact side"):
            tool.record_side(n)


def test_only_the_downloaded_certificate_is_named_by_its_digest() -> None:
    # OR-16: a file this repository's branches hold is named by its commit and path, so
    # re-indenting the sides file or rewriting a lane file changes no decision's receipt.
    sides = json.loads(tool.SIDES.read_text(encoding="utf-8"))
    digested = {name for name, entry in sides["files"].items() if "sha256" in entry}
    assert digested == {"n017.cert.json"}
    for name, entry in sides["files"].items():
        if name != "n017.cert.json":
            assert entry["commit"] in (tool.LANE_COMMIT, tool.PR_COMMIT)
    receipt = json.loads(tool.RESOLVED.read_text(encoding="utf-8"))
    assert [key for key in receipt if "sha256" in key] == []


@pytest.mark.slow
def test_the_whole_receipt_is_current() -> None:
    receipt = tool.resolved_receipt(json.loads(tool.SIDES.read_text(encoding="utf-8")))
    text = json.dumps(receipt, indent=1, ensure_ascii=False) + "\n"
    assert tool.RESOLVED.read_text(encoding="utf-8") == text
