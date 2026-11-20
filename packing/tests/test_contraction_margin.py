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
from devtools import measure_identity as identity
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


def test_a_binary64_packing_is_boxed_at_its_own_extent(tmp_path: Path) -> None:
    """A float text packing (#1012's 109 against Samanyu-dev's) is read exactly, boxed at
    its exact extent whatever side it prints and wherever its centres sit: two upright
    squares a tenth apart, shifted off the origin and printed at a wrong side, contract as
    TWO does; a square left upright beside one turned 90 degrees is the same square."""
    path = tmp_path / "two.xyd"
    path.write_text("2 9\n5.5 -2.5 0\n6.6 -2.5 90\n", encoding="utf-8")
    read = cm.read_certificate(f"binary64-xyd:{path}", 2)
    assert read.certificate.side == Fraction(6.6) - Fraction(9, 2)
    assert read.certificate.poses[0].x == Fraction(1, 2)
    assert read.certificate.poses[0].y == Fraction(1, 2)
    assert {pose.t for pose in read.certificate.poses} == {0}
    record = cm.margin(read)
    assert record["binding_pair"] == [1, 2]
    assert Fraction(record["contracted_side"]) == 2
    assert record["routes_accept"] is True
    overlap = tmp_path / "overlap.xyd"
    overlap.write_text("2 2\n0.5 0.5 0\n1.4 0.5 0\n", encoding="utf-8")
    with pytest.raises(cm.ContractionError, match="no packing at its own side"):
        cm.margin(cm.read_certificate(f"binary64-xyd:{overlap}", 2), routes=False)


#: A Kaggle submission of counts 1 and 2: count 2 is TWO's pair, centred off the origin,
#: the second square turned a quarter (radians), which folds to upright.
KAGGLE = (
    "id,n,square_id,x,y,angle\n"
    "0,1,0,0.0,0.0,0.0\n"
    "1,2,0,-0.55,0.0,0.0\n"
    "2,2,1,0.55,0.0,1.5707963267948966\n"
)


def test_a_kaggle_submission_reads_its_count_boxed(tmp_path: Path) -> None:
    """#1012's float sources, Kodaj's rows and Samanyu-dev's submission, are Kaggle CSVs:
    the count's rows are read exactly and boxed, and a wrong header, a row out of order or
    a missing row is refused."""
    path = tmp_path / "submission.csv"
    path.write_text(KAGGLE, encoding="utf-8")
    read = cm.read_certificate(f"kaggle-csv:{path}", 2)
    assert read.certificate.side == Fraction(0.55) - Fraction(-0.55) + 1
    assert [pose.t for pose in read.certificate.poses] == [0, 0]
    assert Fraction(cm.margin(read)["contracted_side"]) == 2
    one = identity.read_packing(f"kaggle-csv:{path}", 1)
    assert one.side == 1
    assert one.squares == ((Fraction(1, 2), Fraction(1, 2), Fraction(1), Fraction(0)),)
    for text, message in (
        (KAGGLE.replace("angle", "deg"), "header"),
        (KAGGLE.replace("2,2,1,", "2,2,3,"), "out of order"),
        (KAGGLE.rsplit("2,2,1", 1)[0], "1 rows of count 2"),
    ):
        path.write_text(text, encoding="utf-8")
        with pytest.raises(identity.MeasureError, match=message):
            identity.read_packing(f"kaggle-csv:{path}", 2)


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
