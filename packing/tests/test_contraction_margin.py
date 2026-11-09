"""`devtools.contraction_margin`: a certificate's padding, measured exactly (OR-1).

Negative controls first: a certificate that is no packing at its own side, an unknown
kind and a count that differs are each refused, by the reader and by the command. Then a
packing whose answer is known by construction, two upright squares a tenth apart, whose
contraction both maintained routes accept at exact contact. Last, the retained program it
replaces: the think-ruu2 review's contracted side at 130 (Polkovskyi's T-259 certificate,
`review/out/contract.json`), reproduced exactly, with Kaelan Yim's 130 envelope variant
measured against it. Every test reads retained files only.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import contraction_margin as cm
from devtools import upper_bound_reports as reports

ROOT = reports.ROOT
#: Two upright unit squares in a box of side 21/10, a tenth apart along x.
TWO = "2 21/10\n1/2 1/2 0\n8/5 1/2 0\n"
#: The same two squares overlapping by a tenth.
OVERLAP = "2 2\n1/2 1/2 0\n7/5 1/2 0\n"
REVIEW = ROOT / "cases/register_candidates/think-ruu2-2026-10-31/review/out/contract.json"


def _cert(tmp_path: Path, name: str, text: str) -> str:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return f"evand-cert:{path}"


def test_refuses_a_certificate_that_is_no_packing(tmp_path: Path) -> None:
    read = cm.read_certificate(_cert(tmp_path, "overlap.cert", OVERLAP), 2)
    with pytest.raises(cm.ContractionError, match="no packing at its own side"):
        cm.margin(read, routes=False)
    assert cm.main(["--n", "2", "--no-routes", _cert(tmp_path, "o.cert", OVERLAP)]) == 2


def test_refuses_an_unknown_kind_and_another_count(tmp_path: Path) -> None:
    with pytest.raises(cm.ContractionError, match="unknown kind"):
        cm.read_certificate("nonsense:x", 2)
    with pytest.raises(cm.ContractionError):
        cm.read_certificate(_cert(tmp_path, "two.cert", TWO), 3)


def test_two_squares_contract_to_contact(tmp_path: Path) -> None:
    record = cm.margin(cm.read_certificate(_cert(tmp_path, "two.cert", TWO), 2))
    assert Fraction(record["lambda_star"]) == Fraction(10, 11)
    assert record["binding_pair"] == [1, 2]
    assert Fraction(record["contracted_side"]) == 2
    assert Fraction(record["margin"]) == Fraction(1, 10)
    assert record["routes_accept"] is True
    assert {verdict["gap"] for verdict in record["routes"].values()} == {"0"}


def test_reproduces_the_review_at_130_and_measures_a_later_certificate() -> None:
    review = json.loads(REVIEW.read_text(encoding="utf-8"))["house130"]
    record = cm.margin(
        cm.read_certificate("T-259=packet:mishapolk-issue846-2026-10-30", 130),
        against=cm.read_certificate("YIM=packet:yim-certificates-2026-11-09", 130),
    )
    assert record["contracted_side"] == review["contracted_side"]
    assert record["lambda_star"] == review["lambda_star"]
    assert record["binding_pair"] == review["binding_pair"]
    assert record["routes_accept"] is True
    against = record["against"]
    assert against["within_margin"] is True
    assert Fraction(against["gain"]) < Fraction(record["margin"])
