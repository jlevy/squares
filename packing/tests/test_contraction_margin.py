"""`devtools.contraction_margin`: a certificate's padding, measured exactly (OR-1).

Negative controls first: a certificate that is no packing at its own side, by an
overlapping pair or by a square outside its box, an unknown kind and a count that differs
are each refused, by the reader and by the command. Then two packings whose answers are
known by construction, two upright squares a tenth apart and an upright square beside one
turned by half-angle tangent 1/2, whose contractions both maintained routes accept at exact
contact, the second against a later side below its contracted one. Last, the retained program it
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
#: Two squares apart, the second outside a box of side 1 (the senior review's probe).
OUTSIDE = "2 1\n1/2 1/2 0\n8/5 1/2 0\n"
#: An upright square and one at half-angle tangent 1/2, (cos, sin) = (3/5, 4/5), centres 2
#: apart along x. On every normal of the pair ``T = (1 + 3/5 + 4/5) / 2 = 6/5`` and the
#: largest reach is 2, so ``lambda* = 3/5``: the rotated square's corner at height -1/10
#: meets the upright square's right edge. Boxed with half-widths 1/2 and 7/10, the side
#: falls from 16/5 to 12/5.
ROTATED = "2 16/5\n1/2 7/10 0\n5/2 7/10 1/2\n"
#: Two upright squares at side 2, below the rotated pair's contracted side.
TIGHT = "2 2\n1/2 1/2 0\n3/2 1/2 0\n"
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


def test_refuses_a_square_outside_its_box(tmp_path: Path) -> None:
    outside = _cert(tmp_path, "outside.cert", OUTSIDE)
    with pytest.raises(cm.ContractionError, match="square 2 outside the box"):
        cm.margin(cm.read_certificate(outside, 2), routes=False)
    with pytest.raises(cm.ContractionError, match="square 2 outside the box"):
        cm.margin(cm.read_certificate(outside, 2))
    assert cm.main(["--n", "2", outside]) == 2
    two = _cert(tmp_path, "two.cert", TWO)
    assert cm.main(["--n", "2", "--no-routes", two, "--against", outside]) == 2


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
    assert all(verdict["passed"] for verdict in record["certificate_routes"].values())


def test_a_rotated_pair_contracts_to_its_known_contact(tmp_path: Path) -> None:
    record = cm.margin(
        cm.read_certificate(_cert(tmp_path, "rotated.cert", ROTATED), 2),
        against=cm.read_certificate(_cert(tmp_path, "tight.cert", TIGHT), 2),
    )
    assert Fraction(record["lambda_star"]) == Fraction(3, 5)
    assert record["binding_pair"] == [1, 2]
    assert Fraction(record["contracted_side"]) == Fraction(12, 5)
    assert Fraction(record["margin"]) == Fraction(4, 5)
    assert record["routes_accept"] is True
    assert {verdict["gap"] for verdict in record["routes"].values()} == {"0"}
    # The later side, 2, lies below the contracted 12/5: a gain of 6/5, 1.5 margins.
    against = record["against"]
    assert Fraction(against["gain"]) == Fraction(6, 5)
    assert against["gain_over_margin"] == "1.5000"
    assert against["within_margin"] is False


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


def test_an_l_step_carries_its_base_margin_where_the_whole_certificate_has_none() -> None:
    """T-284 (#938) is T-282 with one L step, so its own margin is 0: two grid squares
    touch. Read through ``l-base``, its padding is T-282's own retained margin, and #939's
    base (lane L78) gains 1.0399 of it, as the retained receipts state."""
    web = reports.WEB
    t282 = json.loads(
        (web / "ozden-s172-upper-bound-2026-11-09/measure/contraction-n172-own.json").read_text(
            encoding="utf-8"
        )
    )
    packet = web / "de-winter-s199-upper-bound-2026-11-09/measure"
    retained = json.loads((packet / "contraction-n172-base.json").read_text(encoding="utf-8"))
    whole = json.loads((packet / "contraction-n199.json").read_text(encoding="utf-8"))
    assert (whole["margin"], whole["binding_pair"]) == ("0", [173, 174])
    record = cm.margin(
        cm.read_certificate("T-284=l-base:packet:ozden-s199-upper-bound-2026-11-09", 172),
        routes=False,
        against=cm.read_certificate(
            "#939=l-base:packet:de-winter-s199-upper-bound-2026-11-09", 172
        ),
    )
    assert record["margin"] == t282["margin"] == retained["margin"]
    assert record["lambda_star"] == t282["lambda_star"]
    assert record["against"] == retained["against"]
    assert record["against"]["gain_over_margin"] == "1.0399"
    assert record["against"]["within_margin"] is False


def test_a_one_step_base_against_a_certificate_at_its_own_count_is_compared_directly(
    tmp_path: Path,
) -> None:
    """The s172 packet's retained command, #939's base against #946 at 172, writes its
    receipt again: the rival is read at ``--n`` and compared with the base itself, and a
    one-step ``l-base:packet:`` receipt carries no ``construction`` (review A2 of #1030)."""
    packet = reports.WEB / "de-winter-s172-upper-bound-2026-11-10/measure"
    retained = json.loads(
        (packet / "contraction-n172-against-939-base.json").read_text(encoding="utf-8")
    )
    out = tmp_path / "receipt.json"
    command = [
        "--n",
        "172",
        "#939=l-base:packet:de-winter-s199-upper-bound-2026-11-09",
        "--against",
        "#946=packet:de-winter-s172-upper-bound-2026-11-10",
        "--no-routes",
        "--out",
        str(out),
    ]
    assert cm.main(command) == 0
    record = json.loads(out.read_text(encoding="utf-8"))
    assert record["against"] == retained["against"]
    assert "construction" not in record
    assert "construction" not in retained


def test_a_one_step_base_compares_a_rival_through_its_step_only_when_asked(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """T-284's base, T-282's packing, against #939's certificate at 199: with
    ``--through`` the rival is read at the extended count and compared with T-284
    contracted through its one L step, a gain of 1.0399 of the margin it carries, as the
    s199 packet's base receipt states; without it the packet's 199 is not read at 172,
    and the refusal says so (review A2 of #1030)."""
    record = cm.margin(
        cm.read_certificate("T-284=l-base:packet:ozden-s199-upper-bound-2026-11-09", 172),
        routes=False,
        against=cm.read_certificate("#939=packet:de-winter-s199-upper-bound-2026-11-09", 199),
        through=True,
    )
    against = record["against"]
    assert against["compared"].startswith("through the construction")
    assert (against["n"], against["gain_over_margin"], against["within_margin"]) == (
        199,
        "1.0399",
        False,
    )
    assert record["construction"]["margin_through"] == record["margin"]
    command = [
        "--n",
        "172",
        "T-284=l-base:packet:ozden-s199-upper-bound-2026-11-09",
        "--against",
        "#939=packet:de-winter-s199-upper-bound-2026-11-09",
        "--no-routes",
        "--out",
        str(tmp_path / "receipt.json"),
    ]
    assert cm.main(command) == 2
    assert "pass --through" in capsys.readouterr().err
