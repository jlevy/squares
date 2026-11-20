"""The lower-bound report-order walk: standing against the lanes, monotonicity, order."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import lower_bound_claims as walk

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "campaign/issue-intake/lower-bounds-de-winter-20261120"


def _lane(value: str) -> dict[str, Any]:
    return {"value": value, "exact_form": value}


@pytest.fixture
def lanes(monkeypatch: pytest.MonkeyPatch) -> None:
    """Three counts whose lanes are 1, 2 and 2 (verified) and 1, 2, 3 (reported)."""
    table = {
        1: {"verified": _lane("1"), "reported": _lane("1")},
        2: {"verified": _lane("2"), "reported": _lane("2")},
        3: {"verified": _lane("2"), "reported": _lane("3")},
    }
    monkeypatch.setattr(walk, "lanes", lambda n: table[n])


def _verdicts(data: dict[str, Any]) -> list[tuple[str, int, str]]:
    return [(r["report"], r["n"], r["order_verdict"]) for r in walk.classify(data)["rows"]]


@pytest.mark.usefixtures("lanes")
def test_report_order_records_each_stronger_report_and_marks_the_last_current() -> None:
    data = {
        "reports": [
            {"id": "a", "reported_at": "t1", "claims": [{"n": 3, "rational": "31/10"}]},
            {"id": "b", "reported_at": "t2", "claims": [{"n": 3, "rational": "32/10"}]},
            {"id": "c", "reported_at": "t3", "claims": [{"n": 3, "rational": "32/10"}]},
        ]
    }
    assert _verdicts(data) == [("a", 3, "superseded"), ("b", 3, "current"), ("c", 3, "weaker")]


@pytest.mark.usefixtures("lanes")
def test_a_claim_at_or_below_a_lane_or_the_monotone_floor_is_no_improvement() -> None:
    data = {
        "reports": [
            {
                "id": "a",
                "reported_at": "t1",
                "claims": [
                    {"n": 3, "rational": "3"},  # equal to the reported lane
                    {"n": 2, "sqrt": "4"},  # the square root of 4 is the lane, 2
                ],
            }
        ]
    }
    assert _verdicts(data) == [("a", 3, "not-an-improvement"), ("a", 2, "not-an-improvement")]


@pytest.mark.usefixtures("lanes")
def test_monotonicity_rows_are_consequences_and_an_earlier_smaller_count_weakens() -> None:
    data = {
        "reports": [
            {
                "id": "a",
                "reported_at": "t1",
                "claims": [
                    {"n": 2, "rational": "33/10"},
                    {"n": 3, "rational": "33/10", "from_n": 2},
                ],
            },
            {"id": "b", "reported_at": "t2", "claims": [{"n": 3, "rational": "32/10"}]},
        ]
    }
    rows = walk.classify(data)["rows"]
    assert [r["order_verdict"] for r in rows] == ["current", "consequence", "weaker"]
    assert rows[1]["consequence_of"] == "a at 2"


def test_a_square_root_is_compared_by_squares() -> None:
    assert walk.against("sqrt", Fraction(5), Fraction(2), Fraction(2)) == walk.ABOVE
    assert walk.against("sqrt", Fraction(4), Fraction(2), Fraction(2)) == walk.EQUAL
    assert walk.decimal("sqrt", Fraction(2), 6) == "1.414213"


def test_the_retained_receipt_is_current() -> None:
    claims = walk.safe_load((INTAKE / "claims.yaml").read_text(encoding="utf-8"))
    receipt = (INTAKE / "classification.json").read_text(encoding="utf-8")
    assert walk.render(walk.classify(claims)) == receipt
