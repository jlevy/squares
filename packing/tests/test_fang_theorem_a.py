"""Kevin Fang's Theorem A checked exactly from the note, with mutation controls (#797)."""

from __future__ import annotations

import json
import shutil
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from cases.asymptotic import fang_theorem_a as theorem


def test_the_bound_lemma_two_and_the_limit_hold_on_a_range() -> None:
    checks = theorem.check_bound(6, 1500)
    assert all(check.holds for check in checks), [c for c in checks if not c.holds]
    assert checks[0].value.startswith("1521 (k, b) decided")


def test_both_odd_widths_are_tried_where_sqrt_2k_is_an_even_integer() -> None:
    ties = [k for k in range(6, 1000) if len(theorem.odd_widths(k)) > 1]
    assert ties == [2 * m * m for m in range(2, 23)]
    assert theorem.odd_widths(8) == (3, 5)
    assert [theorem.witness(8, b).waste for b in (3, 5)] == [12, 14]


def test_the_identities_carry_the_limit_below_the_bound_at_every_k() -> None:
    checks = theorem.check_identities()
    assert all(check.holds for check in checks), [c for c in checks if not c.holds]
    # Too few points no longer decide a polynomial identity of degree 6.
    assert not theorem.check_identities(range(3, 17, 2))[0].holds


def test_every_square_is_placed_validly_at_small_k() -> None:
    (check,) = theorem.check_geometry(range(6, 17))
    assert check.holds, check.value
    assert check.value.startswith("12 packings")


def test_each_mutant_is_refused() -> None:
    for k in (6, 7, 11, 18):
        b = theorem.odd_widths(k)[0]
        packing = theorem.build(k, b, theorem.witness(k, b).t)
        assert theorem.defects(packing) == []
        for name, squares in theorem.mutants(packing).items():
            assert theorem.overlaps(squares, 1), (k, name)


def test_a_square_outside_the_box_and_a_side_of_k_are_refused() -> None:
    packing = theorem.build(9, 5, theorem.witness(9, 5).t)
    first, *rest = packing.squares
    moved = theorem.shifted(first, packing.side, Fraction(0))
    assert "a vertex outside [0, S]^2" in theorem.defects(
        replace(packing, squares=(moved, *rest))
    )
    assert "S >= k" in theorem.defects(replace(packing, side=Fraction(9)))
    found = theorem.defects(replace(packing, squares=(*packing.squares, first)))
    assert any("the formula gives" in item for item in found)


def test_the_limiting_angle_itself_gives_no_packing_below_k() -> None:
    at_limit = theorem.construct(20, 7, Fraction(1, 7))
    assert at_limit is not None
    assert at_limit.side == 20
    # B(k), the note's limit of H(t), is H at t0 = 1/b (review A7 on #801).
    assert at_limit.lemma_bound == theorem.limit(20, 7)
    for k in range(6, 400):
        for b in theorem.odd_widths(k):
            assert theorem.limit(k, b) == theorem.lemma_bound(k, b, Fraction(1, b)), (k, b)
    assert theorem.limit(20, 7) != theorem.lemma_bound(
        20, 7, Fraction(1, 7) + Fraction(1, 10**6)
    )
    assert theorem.witness(20, 7).side < 20


def test_the_bound_is_decided_exactly_at_its_edge() -> None:
    # 4 sqrt(2 * 8) + 2 = 18 exactly.
    assert not theorem.below_bound(18, 8)
    assert theorem.below_bound(Fraction(35, 2), 8)
    assert theorem.theorem_a(8) == 16
    assert [theorem.theorem_a(k) for k in (6, 7, 50, 101)] == [14, 15, 40, 57]


def test_the_construction_is_sharp_and_a_smaller_constant_fails() -> None:
    checks = theorem.check_sharpness()
    assert all(check.holds for check in checks), [c for c in checks if not c.holds]
    assert theorem.sharp_k(11) == 59
    assert theorem.witness(59, 11).waste == 44


def test_each_shipped_certificate_is_the_construction_at_its_k() -> None:
    (check,) = theorem.check_certificates()
    assert check.holds, check.value
    assert check.value.startswith("36 certificates")


def test_a_certificate_whose_header_differs_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    copy = tmp_path / "certs"
    shutil.copytree(theorem.CERTS, copy)
    path = copy / "k006.cert"
    path.write_bytes(path.read_bytes().replace(b"b=3 n=26 waste=10", b"b=3 n=26 waste=9 ", 1))
    monkeypatch.setattr(theorem, "CERTS", copy)
    (check,) = theorem.check_certificates((6, 7))
    assert not check.holds
    assert "k = 6: header" in check.value


def test_the_comparisons_on_a_short_range() -> None:
    found = theorem.comparisons(3000, (42, 3000))
    assert found["A_vs_ryu_theorem_1_4"] == {
        "smaller": [[6, 6], [9, 2999]],
        "tied": [[7, 7]],
        "larger": [[8, 8]],
    }
    assert found["A_vs_t163"] == {
        "smaller": [[42, 5000]],
        "tied": [[40, 41]],
        "larger": [[15, 39]],
    }
    assert found["daniel_vs_t163"]["tied"] == [[34, 34], [39, 39]]
    assert found["A_vs_daniel"]["largest_difference_from_89"] == 2
    assert len(found["A_vs_daniel"]["k_below_89_daniel_smaller_by_3_or_more"]) == 17
    tails = (
        found["A_vs_ryu_theorem_1_4_tail_from_16"],
        found["A_vs_ryu_theorem_1_3_tail_from_47"],
        found["A_vs_t163_tail_from_43"],
        found["A_vs_daniel"]["tail_from_100_differs_by_at_most_2"],
        *found["daniel_tails"].values(),
    )
    assert all(tails)
    assert found["case_records"]["theorem_a"]["case_bound_not_below_k"] == []
    assert found["case_records"]["daniel"]["case_bound_not_below_k"] == []


def test_the_retained_comparisons_are_what_the_code_computes() -> None:
    """The register cites the receipt as CHECKED BY COMPUTATION HERE, so the full-range
    comparisons (about 3 s) are recomputed and held to it, every key (review A3 on #801)."""
    receipt = json.loads((theorem.RECEIPTS / "comparisons.json").read_text(encoding="utf-8"))
    assert json.loads(json.dumps(theorem.comparisons())) == receipt
    counts = receipt["A_vs_daniel"]
    assert (counts["A_smaller"], counts["tied"], counts["daniel_smaller"]) == (
        495_210,
        249_568,
        255_215,
    )
    assert receipt["A_strictly_least_in_window"]["strictly_least"] == 346_919


def test_the_daniel_tail_starts_at_100_and_not_before() -> None:
    """sqrt(2k) + sqrt(2k - 7) >= 28 first at k = 100 (review A1 on #801): the check
    decides the inequality it names, so it fails at 99 and at 70."""
    assert theorem.daniel_tail_holds(100)
    assert not theorem.daniel_tail_holds(99)
    assert not theorem.daniel_tail_holds(70)
    assert all(theorem.daniel_tail_holds(k) for k in range(100, 2000))
    for k in range(7, 2000):
        # The float sum agrees with the exact decision wherever it is not near 28.
        total = (2 * k) ** 0.5 + (2 * k - 7) ** 0.5
        if abs(total - 28) > 1e-9:
            assert theorem.daniel_tail_holds(k) == (total >= 28), k
    found = theorem.comparisons(3000, (42, 3000))
    for k in range(100, 3000):
        assert abs(theorem.theorem_a(k) - (4 * theorem.ceil_sqrt(2 * k - 7) - 1)) <= 2
    assert found["A_vs_daniel"]["tail_from_100_differs_by_at_most_2"]


def test_the_retained_construction_report_covers_the_notes_ranges() -> None:
    report = json.loads(theorem.CONSTRUCTION_RECEIPT.read_text(encoding="utf-8"))
    assert report["passed"]
    assert report["bound_through"] == theorem.NOTE_BOUND
    assert report["geometry_through"] == 40
    assert all(check["holds"] for check in report["checks"])
    least = next(c for c in report["checks"] if c["name"].startswith("least B(k) - w for k"))
    assert least["value"] == "8019401/78023840599 at k = 19705"


def test_the_replay_receipt_is_admitted_and_k6_decides_again_alike() -> None:
    assert theorem.check_replay([6]) == []


def test_a_receipt_stating_another_certificate_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    receipt = json.loads(theorem.REPLAY_RECEIPT.read_text(encoding="utf-8"))
    receipt["rows"][0]["exact_side"] = "6"
    receipt["rows"][1]["controls_refused"] = False
    forged = tmp_path / "certificate-replay.json"
    forged.write_text(json.dumps(receipt), encoding="utf-8")
    monkeypatch.setattr(theorem, "REPLAY_RECEIPT", forged)
    problems = theorem.check_replay()
    assert "k = 6: the receipt states another certificate" in problems
    assert "k = 7: the receipt does not show it accepted with its controls" in problems
