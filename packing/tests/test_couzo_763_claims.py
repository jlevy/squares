"""Issue #763's claims, re-derived from the indexes its packet retains.

`devtools.couzo_763_claims` applies the source README's selection rule to
``certified_bounds.json`` and ``public_bounds.json`` at 964ee2bd. These tests hold the
rule's two thresholds at their edges with synthetic entries (each refused one step past
the edge), the exact sign of ``r + s*sqrt(2)`` near a tie, and the retained receipt to a
fresh derivation that reproduces every count the issue states.
"""

from __future__ import annotations

import json
from fractions import Fraction
from typing import Any

import pytest

from devtools import couzo_763_claims as claims

PRINT_UNIT = Fraction(1, 10**12)


def _entry(n: int, bound: Fraction, credit: str = "Francisco Couzo") -> dict[str, Any]:
    return {
        "n": n,
        "kind": "certificate",
        "certificate": f"certificates/best/n{n}.cert",
        "certificate_sha256": "0" * 64,
        "source_n": n,
        "deleted_squares": 0,
        "bound": f"{bound.numerator}/{bound.denominator}",
        "credit": credit,
    }


def _public(
    bound: Fraction, credit: str, source: str = "https://example.org"
) -> dict[str, Any]:
    return {
        "bound": f"{bound.numerator}/{bound.denominator}",
        "exact_bound": {"rational": str(bound), "sqrt2": "0"},
        "credit": credit,
        "source": source,
    }


def _select(side: Fraction, comparison: Fraction, credit: str) -> bool:
    found = claims.claim_map({"5": _entry(5, side)}, {"5": _public(comparison, credit)})
    return [item["n"] for item in found["claims"]] == [5]


def test_another_author_s_bound_must_be_beaten_by_more_than_1e_10() -> None:
    """Exactly 1e-10 below another author's bound is not a claim; a hair more is."""
    other = Fraction(3)
    assert not _select(other - claims.TOLERANCE, other, "Mykhailo Polkovskyi")
    assert _select(other - claims.TOLERANCE - Fraction(1, 10**30), other, "Mykhailo Polkovskyi")


def test_couzo_s_own_bound_needs_only_a_lower_12_place_print() -> None:
    """Against his own bound, one unit lower in the 12th place is enough, and the same print
    is not, however far below the side lies within it."""
    own = Fraction(3) + PRINT_UNIT / 2
    assert _select(Fraction(3), own, "Francisco Couzo; earlier credits retained")
    assert not _select(own - PRINT_UNIT / 3, own, "Francisco Couzo")


def test_another_author_s_packing_in_the_index_is_no_claim() -> None:
    """The index holds notebook packings by other authors; the issue does not request them."""
    entry = _entry(5, Fraction(2), credit='kyleluecke, Kaggle notebook "inos"')
    found = claims.claim_map({"5": entry}, {"5": _public(Fraction(3), "Kingbird")})
    assert found["claims"] == []
    assert found["unrequested"] == []


def test_the_leaderboard_is_replaced_by_the_bound_it_superseded() -> None:
    """The per-puzzle leaderboard's packings are not public: the comparison is the reviewed
    bound it replaced, and a side below the leaderboard is still a claim."""
    public = _public(Fraction(2), "a Kaggle team", source=claims.LEADERBOARD)
    public["superseded_review"] = {"bound": "3", "credit": "Evan Daniel", "source": "#728"}
    found = claims.claim_map({"5": _entry(5, Fraction(5, 2))}, {"5": public})
    (item,) = found["claims"]
    assert item["comparison"]["replaces_leaderboard"]
    assert item["comparison"]["bound"] == "3"
    assert item["leaderboard"]["below_side"]


def test_the_sentence_s_rule_adds_the_unrequested_rows() -> None:
    """The print rule alone lists a side within 1e-10 of another author's bound; the README
    leaves it out, so it is unrequested."""
    other = Fraction(3)
    found = claims.claim_map(
        {"5": _entry(5, other - PRINT_UNIT)}, {"5": _public(other, "Mykhailo Polkovskyi")}
    )
    assert found["claims"] == []
    assert [item["n"] for item in found["unrequested"]] == [5]


@pytest.mark.parametrize(
    ("rational", "root", "sign"),
    [
        # 99/70 = 1.4142857... lies above sqrt 2 = 1.4142135..., 140/99 = 1.4141414... below.
        (Fraction(-99, 70), Fraction(1), -1),
        (Fraction(-140, 99), Fraction(1), 1),
        (Fraction(99, 70), Fraction(-1), 1),
        (Fraction(140, 99), Fraction(-1), -1),
        (Fraction(0), Fraction(0), 0),
        (Fraction(-1), Fraction(0), -1),
        (Fraction(0), Fraction(-3), -1),
    ],
)
def test_the_sign_of_a_quadratic_irrational_is_decided_exactly(
    rational: Fraction, root: Fraction, sign: int
) -> None:
    assert claims.sign_sqrt2(rational, root) == sign


def test_a_bound_with_a_root_rounds_up_exactly() -> None:
    """``1 + sqrt 2`` rounds up to 2.414213562374 at 12 places (sqrt 2 = 1.4142135623730...)."""
    assert claims.Bound(Fraction(1), Fraction(1)).ceiling() == "2.414213562374"
    assert claims.Bound(Fraction(5, 2)).ceiling() == "2.500000000000"


def test_the_receipt_is_a_fresh_derivation_with_the_issue_s_counts() -> None:
    """The retained receipt is the derivation from the packet's retained indexes, and the
    derivation gives every count the issue states: 436 rows, 203 at or below 1024 and 233
    above, 196 certificate rows, deletions at 683, 1646 and 1727. The legend's 345 and the
    leaderboard's 180 are stated beside the 351 and 182 the index gives."""
    assert claims.check() == []
    record = json.loads(claims.RECEIPT.read_text(encoding="utf-8"))
    summary = record["summary"]
    assert claims.control_problems(record) == []
    assert summary["in_corpus"] == [268, 303]
    assert summary["kinds"] == {"certificate": 194, "construction": 240, "deletion": 2}
    assert (summary["refines_another_author"], summary["leaderboard_smaller"]) == (351, 182)
    assert summary["issue_states"] == claims.STATED_ONLY
    assert summary["unrequested"] == [
        204,
        335,
        339,
        344,
        379,
        380,
        421,
        452,
        490,
        507,
        535,
        792,
        800,
        935,
        998,
    ]


def test_a_derivation_that_misses_the_issue_s_counts_is_refused() -> None:
    """A control the derivation does not meet is named, not forced."""
    record = json.loads(claims.RECEIPT.read_text(encoding="utf-8"))
    record["summary"] = {**record["summary"], "rows": 435}
    assert claims.control_problems(record) == ["the derivation gives rows = 435, the issue 436"]
