#!/usr/bin/env python3
"""Contract for interval-enclosure witnesses, and the independent audit of the n = 29 one.

Two things live here.

**The contract.** An `interval-certified` witness must replay through the public checker,
and must be refused when the thing that makes it meaningful is missing: a root that was
not proved unique, geometry that is not enclosures, an enclosure written backwards.

**The audit.** The certificate is checked against implementations that share none of its
code -- the numeric SVG walk that predates this route, and the float separating-axis
verifier -- plus the structural prediction that the relaxation's cost is `eps` times the
largest centre coordinate. Agreement with itself would prove nothing.

The precision check is the one that would have caught the real bug. Parsing a 40-digit
enclosure at mpmath's default 15 digits widens it by about `1e-14`, which swamps a
relaxation of `1e-20`; the first replay of this witness reported exactly 52 undecided
pairs, the packing's contact count, from ambient precision alone. A replay whose verdict
depends on the caller's precision is not a replay.
"""

from __future__ import annotations

import copy
from pathlib import Path

import mpmath as mp

from cases.kingbird29 import system as k29
from cases.kingbird29.layout import DEFAULT_SOURCE, squares_at
from cases.kingbird29.verify_svg import materialise_svg
from sqpack.promote.interval import Dual, carrier, interval, midpoint
from sqpack.promote.krawczyk import PoseBox, certify
from sqpack.promote.refine import refine
from sqpack.promote.relax import certified_upper_bound, relax
from sqpack.verify import float_sign, verify_packing
from sqpack.witness import WitnessError, exact_verify, load_witness

ROOT = Path(__file__).resolve().parent.parent
WITNESS = ROOT / "witnesses/kingbird-n029-2026-interval.yaml"

#: The bound this witness records, and the ceiling it would tighten if promoted.
CERTIFIED_BOUND = "5.93383346267692918974379895098"
STANDING_CEILING = "5.93388579981302587863645209"


def require_refusal(call, kind: str, label: str) -> None:
    try:
        call()
    except WitnessError as error:
        assert error.kind == kind, f"{label}: expected {kind}, got {error.kind}"
        return
    raise AssertionError(f"{label}: expected a {kind} refusal and got a result")


def the_witness_replays() -> None:
    witness = load_witness(WITNESS)
    result, report = exact_verify(witness)
    assert result["verification_passed"], result["refusal"]
    assert report.valid
    assert result["method"] == "interval-certified"
    assert result["n"] == 29
    assert result["pairs_tested"] == 406
    assert result["separated_pairs"] == 406
    assert result["undecided_pairs"] == 0
    assert result["overlapping_pairs"] == 0
    assert result["root_unique"] is True
    assert result["relaxation"] == "1e-20"
    # The limitation text is part of the claim, not decoration: the bound is an upper
    # bound at a stated relaxation and must never read as the optimum.
    assert "Not the optimum" in result["limitations"]


def the_replay_does_not_inherit_the_caller_precision() -> None:
    """The bug this file exists for: ambient precision must not decide the verdict."""
    witness = load_witness(WITNESS)
    saved = mp.iv.dps, mp.mp.dps
    try:
        for ambient in (15, 30, 200):
            mp.iv.dps = mp.mp.dps = ambient
            result, _ = exact_verify(witness)
            assert result["verification_passed"], (
                f"the witness failed to replay at ambient precision {ambient}; the "
                "checker is reading the caller's precision instead of the witness's"
            )
            assert result["undecided_pairs"] == 0
    finally:
        mp.iv.dps, mp.mp.dps = saved


def refusals_that_keep_the_claim_honest() -> None:
    base = load_witness(WITNESS)

    without_uniqueness = copy.deepcopy(base)
    without_uniqueness["scalar"]["enclosure"]["unique"] = False
    require_refusal(
        lambda: exact_verify(without_uniqueness),
        "root-not-unique",
        "a box holding possibly two roots identifies no pose",
    )

    wrong_kind = copy.deepcopy(base)
    wrong_kind["scalar"] = {"kind": "decimal"}
    require_refusal(
        lambda: exact_verify(wrong_kind),
        "formal-certificate-missing",
        "an interval-certified claim over decimal geometry",
    )

    backwards = copy.deepcopy(base)
    low, high = backwards["squares"][0]["corners"][0][0]
    backwards["squares"][0]["corners"][0][0] = [high, low]
    require_refusal(
        lambda: exact_verify(backwards),
        "malformed-enclosure",
        "an enclosure written with its endpoints reversed",
    )


def the_bound_sits_where_it_claims() -> None:
    saved = mp.mp.dps
    mp.mp.dps = 60
    try:
        bound = mp.mpf(CERTIFIED_BOUND)
        assert bound < mp.mpf(STANDING_CEILING), (
            "the certificate no longer tightens the standing verified ceiling"
        )
        # Above the construction's own value, which a relaxation of a packing must be.
        assert bound > mp.mpf("5.9338334626769291896894606163")
    finally:
        mp.mp.dps = saved


def audit_against_implementations_that_share_no_code() -> None:
    """Three cross-checks the certification path cannot make of itself."""
    saved = mp.iv.dps, mp.mp.dps
    mp.iv.dps = mp.mp.dps = 80
    try:
        refinement = refine(k29.equations, k29.seed(DEFAULT_SOURCE), 60, names=k29.UNKNOWNS)
        root = certify(
            k29.equations,
            PoseBox.around(k29.UNKNOWNS, refinement.values, "1e-30"),
            digits=45,
        )
        boxes = [
            [
                (
                    x.value if isinstance(x, Dual) else interval(x),
                    y.value if isinstance(y, Dual) else interval(y),
                )
                for x, y in square
            ]
            for square in squares_at(DEFAULT_SOURCE, [carrier(v) for v in root.box.intervals()])
        ]

        # 1. The enclosures must contain the corners the independent numeric walk gives.
        _raw, _entities, _side, published = materialise_svg(DEFAULT_SOURCE)
        outside = 0
        for mine, theirs in zip(boxes, published, strict=True):
            for (box_x, box_y), (point_x, point_y) in zip(mine, theirs, strict=True):
                for box, point in ((box_x, point_x), (box_y, point_y)):
                    if not (mp.mpf(box.a) <= point <= mp.mpf(box.b)):
                        outside += 1
        assert outside == 0, (
            f"{outside} coordinates of the independent walk fall outside the enclosures "
            "this route certified; the two are not describing the same packing"
        )

        # 2. A loosely relaxed variant must satisfy the pre-existing float verifier, whose
        #    tolerance is far below the margin that relaxation opens.
        loose = relax(boxes, "1e-6")
        points = [
            [(float(midpoint(x)), float(midpoint(y))) for x, y in square] for square in loose
        ]
        side = max(max(value for pair in square for value in pair) for square in points)
        report = verify_packing(
            points, side * (1 + 1e-15), sign=float_sign(1e-12), check_shapes=False
        )
        assert report.valid and report.strict_pairs == 406, (
            "the independent float verifier rejects a packing this route certifies"
        )

        # 3. The relaxation's cost is structural, not fitted: the bound exceeds the true
        #    side by eps times the largest centre coordinate, which for a square flush
        #    against the far wall is side - 1/2.
        true_side = mp.mpf(refinement.values[0])
        ratios = []
        for epsilon in ("1e-6", "1e-12", "1e-20"):
            excess = mp.mpf(certified_upper_bound(boxes, epsilon=epsilon).bound) - true_side
            ratios.append(excess / mp.mpf(epsilon))
        for ratio in ratios:
            assert abs(ratio - (true_side - mp.mpf("0.5"))) < mp.mpf("1e-6"), (
                f"the relaxation cost {ratio} is not eps times the largest centre "
                "coordinate; the construction is not behaving as derived"
            )
        assert abs(ratios[0] - ratios[-1]) < mp.mpf("1e-6"), (
            "the cost is not linear in eps across fourteen orders of magnitude"
        )
    finally:
        mp.iv.dps, mp.mp.dps = saved


def main() -> int:
    the_witness_replays()
    the_replay_does_not_inherit_the_caller_precision()
    refusals_that_keep_the_claim_honest()
    the_bound_sits_where_it_claims()
    audit_against_implementations_that_share_no_code()
    print("interval witness contract and n=29 audit selftest passed")
    return 0


def test_witness_interval() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
