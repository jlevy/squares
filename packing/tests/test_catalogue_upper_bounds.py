"""The exact certificates of the catalogue's packings at n = 69, 83 and 87 (T-088, T-089).

Since 2026-10-06 Evan Daniel's exact certificates of the same packings (T-101) hold those
counts' verified upper lanes, a layer `devtools.apply_exact_ceilings` writes over this one;
since 2026-10-12, where a regularized view's exact side lies below that, the layer
`devtools.register_regularized_bounds` (T-155) writes over both.
"""

from __future__ import annotations

import json
from fractions import Fraction

from devtools import apply_exact_ceilings as exact_ceilings
from devtools import catalogue_upper_bounds as catalogue
from devtools import register_regularized_bounds as regularized
from devtools import upper_bound_packets as packets
from devtools.apply_upper_bound_packets import normalized
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.witness import load_witness
from sqpack.yamlio import safe_load


def test_the_certificates_and_receipts_agree() -> None:
    assert catalogue.fast_problems() == []


def test_each_certificate_is_its_witness_promoted_and_lies_above_the_printed_side() -> None:
    """The printed sides are truncated decimals, so every certificate is above its own."""
    for n, row in catalogue.certification().items():
        certificate = load_witness(
            catalogue.certificate_path(n), fallback_schema=catalogue.WITNESS_SCHEMA
        )
        assert certificate["id"] == f"W-known-best-n{n:03d}-rational", n
        assert certificate["certificate"]["derived_from"] == f"W-known-best-n{n:03d}", n
        assert certificate["source"]["path"] == f"witnesses/known-best/n-{n:03d}.yaml", n
        side = Fraction(row["certified_side"])
        assert Fraction(row["printed_side"]) < Fraction(row["witness_side"]) < side, n
        assert side - Fraction(row["printed_side"]) < Fraction(1, 10**12), n
        assert row["units_above_printed"] > 1, n
        assert row["witness_revision"].startswith("evand/square-packing@"), n


def test_both_negative_controls_are_refused_by_both_checkers() -> None:
    """Two mutations of the n = 69 certificate, decided again here rather than read back."""
    text = catalogue.certificate_path(catalogue.CONTROL_N).read_text(encoding="utf-8")
    assert packets.independent_check(text)["verification_passed"]
    shrunk = packets.shrink_side(text)
    moved = packets.shift_square(text, catalogue.CONTROL_SHIFT_SQUARE, Fraction(1, 10**6))
    for mutated, failure in ((shrunk, "container penetration"), (moved, "overlapping")):
        verdict = packets.independent_check(mutated)
        assert not verdict["verification_passed"]
        assert failure in verdict["failures"][0]
        assert not catalogue.exact_verify_passed(mutated)
    recorded = json.loads(catalogue.CONTROLS.read_text(encoding="utf-8"))["controls"]
    assert [row["control"] for row in recorded] == [
        "side-shrunk-1e-15",
        f"square-{catalogue.CONTROL_SHIFT_SQUARE}-shifted-1e-6",
    ]


def test_each_receipts_verified_value_trails_the_printed_side_and_was_superseded() -> None:
    """Each certificate's verified value trails the printed side, at all three; since
    2026-10-06 Evan Daniel's exact certificate of the same packing (T-101) holds the
    verified lane below it, or since 2026-10-12 a regularized view below that (T-155), and
    the record keeps the reported side these receipts print."""
    for n, row in catalogue.certification().items():
        text = (catalogue.ROOT / "frontier" / f"n-{n:03d}.md").read_text(encoding="utf-8")
        case = safe_load(text.split("---\n")[1])["packing"]
        ours = {"value": row["verified_value"], "exact_form": row["exact_form"]}
        assert case["reported_upper_bound"]["value"] == row["printed_side"], n
        assert not bounds_agree_at_declared_precision(case["reported_upper_bound"], ours), n
        assert n in exact_ceilings.certificates.CEILINGS, n
        assert Fraction(case["verified_upper_bound"]["exact_form"]) < Fraction(
            row["exact_form"]
        ), n
        # T-155's view lies exactly at T-101's side at all three, so the lane cites T-101's
        # replays, which prove that side, and T-155's decision after them.
        later = (
            regularized.verified_block(regularized.committed()[n])["evidence"]
            if n in regularized.committed()
            else [exact_ceilings.EXACT_REPLAY, exact_ceilings.SOURCE_REPLAY]
        )
        assert case["verified_upper_bound"]["evidence"] == later, n


def test_apply_case_writes_each_committed_records_upper_lane_and_blockers() -> None:
    """Applied to a committed record with the later layers on top, as the generator applies
    them, the adoption step changes nothing in it."""
    for n in catalogue.RESULTS:
        text = (catalogue.ROOT / "frontier" / f"n-{n:03d}.md").read_text(encoding="utf-8")
        applied = regularized.apply_case(
            n, exact_ceilings.apply_case(n, catalogue.apply_case(n, text))
        )
        assert safe_load(applied.split("---\n")[1]) == safe_load(text.split("---\n")[1]), n
        assert normalized(applied.split("---\n", 2)[2]) == normalized(
            text.split("---\n", 2)[2]
        ), n
    assert catalogue.apply_case(68, "---\npacking: {}\n---\nbody\n") == (
        "---\npacking: {}\n---\nbody\n"
    )
