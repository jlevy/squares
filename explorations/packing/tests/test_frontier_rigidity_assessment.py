#!/usr/bin/env python3
"""The corpus now states what it can prove about rigidity, and only that.

`rigidity: null` means "not assessed", and it sat on 99 of 100 records while the
evidence to settle 94 of them was already committed. Two sound arguments were available:
a hit in the translation escape screen exhibits a motion and so certifies NOT rigid, and
a perfect square is an exact tiling with no slack and so is rigid outright.

The direction of the screen is the whole point. A hit is strong and a miss is weak, so
these tests hold the asymmetry in place: no record may claim rigidity on a miss, and the
four packings the catalogue calls "Rigid." stay `undetermined` as OUR finding, because
promoting a source's word to a first-party claim is the conflation the field split was
built to prevent.
"""

from __future__ import annotations

import math
from pathlib import Path

import pytest
import yaml
from mpmath import mp

import devtools.assess_frontier_rigidity as assess
from devtools.assess_frontier_rigidity import (
    ESCAPE_EVIDENCE,
    TILING_EVIDENCE,
    plan,
    screen_cases,
)
from devtools.screen_translation_escape import PRIMARY_TOLERANCE, load_record, translated
from sqpack.assurance import check_case_semantics
from sqpack.verify import float_sign, verify_packing

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
CATALOGUE_RIGID = (5, 11, 28, 40)


def _case(n: int) -> dict:
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---", 2)[1])["packing"]


def _rigidity(n: int) -> dict:
    block = _case(n)["rigidity"]
    assert block is not None, f"n={n} still carries rigidity: null"
    return block


def _by_property() -> dict[str, list[int]]:
    grouped: dict[str, list[int]] = {}
    for n in range(1, 101):
        grouped.setdefault(_rigidity(n)["property"], []).append(n)
    return grouped


def test_every_record_now_carries_an_assessment() -> None:
    """Null meant "not assessed". Nothing is unassessed any more."""
    grouped = _by_property()
    assert sum(len(v) for v in grouped.values()) == 100
    assert sorted(grouped) == ["locally-rigid", "not-rigid", "undetermined"]
    assert len(grouped["not-rigid"]) == 84
    assert len(grouped["locally-rigid"]) == 11  # ten tilings plus n=11's own argument
    assert grouped["undetermined"] == [5, 28, 40, 68, 69]


def test_rigid_records_are_exactly_the_tilings_plus_n11() -> None:
    """Rigidity is claimed only where an argument exists, never from a screen miss."""
    perfect = [n for n in range(1, 101) if math.isqrt(n) ** 2 == n]
    assert _by_property()["locally-rigid"] == sorted([*perfect, 11])
    for n in perfect:
        assert _rigidity(n)["evidence"] == [TILING_EVIDENCE]
        assert _rigidity(n)["assurance"] == "verified"
    # n=11 rests on the tangent-cone work, not on anything this assessment derived.
    assert TILING_EVIDENCE not in _rigidity(11)["evidence"]
    assert ESCAPE_EVIDENCE not in _rigidity(11)["evidence"]


def test_no_record_claims_rigidity_from_a_screen_miss() -> None:
    """The asymmetry that makes the screen sound: hits prove, misses do not."""
    for n in range(1, 101):
        block = _rigidity(n)
        if ESCAPE_EVIDENCE in block["evidence"]:
            assert block["property"] in {"not-rigid", "undetermined"}, (
                f"n={n} claims {block['property']} on escape-screen evidence"
            )


def test_the_catalogues_rigid_annotation_is_not_promoted_to_our_finding() -> None:
    """The conflation the split exists to prevent, held in place by a test."""
    for n in CATALOGUE_RIGID:
        assert _case(n)["reported_upper_bound"]["catalogue_rigid"] == "rigid"
    for n in (5, 28, 40):
        assert _rigidity(n)["property"] == "undetermined", (
            f"n={n}: the catalogue's word became our claim"
        )


def test_the_immobile_records_are_exactly_the_tilings_and_the_annotated_four() -> None:
    """An independent partition that agrees with the catalogue's own four.

    The screen knows nothing about the catalogue. That it finds no movable square in
    exactly the ten tilings plus n = 5, 11, 28, 40 is a real cross-check on both.
    """
    cases, _excluded = screen_cases()
    immobile = sorted(n for n, case in cases.items() if case["movable_square_count"] == 0)
    perfect = [n for n in range(1, 101) if math.isqrt(n) ** 2 == n]
    assert immobile == sorted([*perfect, *CATALOGUE_RIGID])


@pytest.mark.parametrize("n", [10, 17, 31, 47, 73])
def test_the_exhibited_motion_is_real(n: int) -> None:
    cases, _excluded = screen_cases()
    assert _rigidity(n)["property"] == "not-rigid"
    certificate = cases[n]["movable_squares"][0]
    squares, side, _ids = load_record(n)
    direction = (
        mp.mpf(certificate["direction"]["x"]),
        mp.mpf(certificate["direction"]["y"]),
    )
    moved = translated(
        squares, certificate["square_index"], direction, mp.mpf(certificate["slide_distance"])
    )
    report = verify_packing(
        moved,
        side,
        sign=float_sign(mp.mpf(PRIMARY_TOLERANCE)),
        check_shapes=False,
        bucket=True,
    )
    assert report.valid, f"n={n}: the motion this record calls a certificate does not replay"


def test_the_scope_names_the_square_it_moved() -> None:
    """A claim a reader cannot check is not evidence."""
    cases, _excluded = screen_cases()
    for n, case in cases.items():
        if case["movable_square_count"] == 0:
            continue
        index = case["movable_squares"][0]["square_index"]
        assert f"Square {index} of the retained witness" in _rigidity(n)["scope"]


def test_rigidity_evidence_must_resolve_and_cover_its_case() -> None:
    """Until this check existed, rigidity refs were the one kind nothing resolved."""
    case = _case(31)
    covered = {
        ESCAPE_EVIDENCE: {"scope": {"n_values": [31]}},
        "E-other": {"scope": {"n_values": [7]}},
    }
    assert not [e for e in check_case_semantics(case, covered) if "rigidity" in e]

    case["rigidity"]["evidence"] = ["E-does-not-exist"]
    assert any("rigidity: unknown evidence" in e for e in check_case_semantics(case, covered))

    case["rigidity"]["evidence"] = ["E-other"]
    assert any(
        "rigidity: evidence E-other does not cover" in e
        for e in check_case_semantics(case, covered)
    )


def test_the_assessment_is_reproducible() -> None:
    """--check must fail on a hand edit rather than accepting it."""
    assert not [n for n, _p, text, desired in plan() if text != desired]


@pytest.mark.parametrize(
    ("label", "record"),
    [
        (
            "side above k",
            {
                "verified_upper_bound": {"value": "3.0001"},
                "verified_lower_bound": {"value": "3"},
            },
        ),
        (
            "side below k",
            {"verified_upper_bound": {"value": "3"}, "verified_lower_bound": {"value": "2.9"}},
        ),
        ("no verified bounds", {}),
        ("reported but not verified", {"reported_upper_bound": {"value": "3.0"}}),
    ],
)
def test_the_tiling_claim_refuses_when_the_side_is_not_pinned_at_k(label, record) -> None:
    """The tiling argument rests on the side, not on `n`.

    A perfect square `n` is necessary for the tiling argument and not sufficient: what
    makes the packing a tiling is that the side is exactly `k`, which is a property of
    the record. The first version of the assessor read only `math.isqrt(n)` and never
    opened the record, so a perfect-square case whose retained side had regressed above
    `k` would still have been stamped `verified` `locally-rigid` with scope text
    asserting "no slack anywhere". The claims were all true at the time; nothing checked
    them, and `--check` could not have caught it either, because it regenerates from the
    same assumption. This is the check that can fail.
    """
    cases, excluded = assess.screen_cases()
    with pytest.raises(assess.RigidityAssessmentError, match="do not pin the side"):
        assess.rigidity_for(9, cases, excluded, record)


def test_the_tiling_claim_is_written_when_the_side_is_pinned() -> None:
    """The positive half, so the test above is not passing for a trivial reason."""
    cases, excluded = assess.screen_cases()
    pinned = {
        "verified_upper_bound": {"value": "3"},
        "verified_lower_bound": {"value": "3"},
    }
    block = assess.rigidity_for(9, cases, excluded, pinned)
    assert block is not None
    assert block["property"] == "locally-rigid"
    assert block["assurance"] == "verified"
    assert "verified above and below at exactly 3" in block["scope"]
