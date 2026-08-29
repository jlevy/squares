#!/usr/bin/env python3
"""Known-answer and refusal contract for contact extraction.

`n = 11` is the calibration: its coordinates are exact, so every contact is certified
rather than measured, and the counts, the orientation split, and the absence of any
ambiguity are all known before the extractor runs.  An extractor that cannot reproduce a
known structure has no business being pointed at one nobody has published.

`n = 29` is the target, and its check is different in kind.  Nothing here proves the
`n = 29` structure correct -- it is measured, not certified -- so what is asserted is the
measurement: the counts the source's own reconstruction reports, and the ninety-seven
decades between the worst contact and the smallest strict separation that make the
declared floor a safe place to cut.
"""

from __future__ import annotations

from pathlib import Path

import mpmath as mp

from cases.kingbird29.verify_svg import materialise_svg
from cases.kingbird29.verify_svg import sign as kingbird_sign
from cases.trump11.packing import build as build_trump11
from sqpack.promote.contacts import (
    ContactExtractionError,
    extract_contacts,
    require_decided,
)
from sqpack.verify import exact_sign, verify_packing

ROOT = Path(__file__).resolve().parent.parent
PROVENANCE = ROOT / "resources/papers/kingbird-square-29-provenance.svg"
FLOOR = "1e-80"
RATIO = "1e10"


def require_refusal(call, kind: str, label: str) -> None:
    try:
        call()
    except ContactExtractionError as error:
        assert error.kind == kind, f"{label}: expected {kind}, got {error.kind}"
        return
    raise AssertionError(f"{label}: expected a {kind} refusal and got a structure")


def trump11_known_answer() -> None:
    squares, side, _field = build_trump11()
    report = verify_packing(squares, side, sign=exact_sign)
    structure = require_decided(extract_contacts(squares, side, sign=exact_sign))

    assert len(structure.pair_contacts) == report.touching_pairs == 14
    assert len(structure.wall_contacts) == report.container_contacts == 20
    assert structure.incidence_count == 34
    assert structure.pairs_tested == 55

    # Trump's layout is six axis-aligned squares plus a block of five rotated by `a`.
    sizes = sorted(len(item.members) for item in structure.angle_classes)
    assert sizes == [5, 6], f"expected a 6 + 5 orientation split, got {sizes}"

    # Exact arithmetic decides zero, so there is no band to be uncertain in.
    assert structure.ambiguous == ()
    assert structure.floor == "0"


def kingbird29_measurement() -> None:
    mp.mp.dps = 160
    _raw, _entities, side, squares = materialise_svg(PROVENANCE)
    report = verify_packing(squares, side, sign=kingbird_sign)
    structure = require_decided(
        extract_contacts(squares, side, sign=kingbird_sign, floor=FLOOR, ambiguity_ratio=RATIO)
    )

    assert len(structure.pair_contacts) == report.touching_pairs == 52
    assert len(structure.wall_contacts) == report.container_contacts == 37
    assert structure.incidence_count == 89
    assert len(structure.angle_classes) == 6, "the source declares six orientation classes"
    assert structure.ambiguous == ()

    # The floor is safe because of the gap around it, not because of its value.
    assert structure.separation_decades is not None
    assert mp.mpf(structure.separation_decades) > 90


def synthetic_pose(gap):
    """Two unit squares side by side in a side-two container, `gap` apart."""
    left = [
        (mp.mpf(0), mp.mpf(0)),
        (mp.mpf(1), mp.mpf(0)),
        (mp.mpf(1), mp.mpf(1)),
        (mp.mpf(0), mp.mpf(1)),
    ]
    right = [(mp.mpf(1) + gap + dx, dy) for dx, dy in ((0, 0), (1, 0), (1, 1), (0, 1))]
    return [left, [(mp.mpf(x), mp.mpf(y)) for x, y in right]], mp.mpf(2) + gap


def perturbation_control() -> None:
    """A margin displaced into the ambiguous band must produce a typed refusal.

    This runs on a two-square pose built here rather than on a retained source, because
    the negative-control harness excludes `resources/` from its snapshot and a control
    that cannot run in the harness is not a control.
    """
    mp.mp.dps = 160
    touching, side = synthetic_pose(mp.mpf(0))
    decided = require_decided(
        extract_contacts(touching, side, sign=kingbird_sign, floor=FLOOR, ambiguity_ratio=RATIO)
    )
    assert len(decided.pair_contacts) == 1, "the two squares should touch exactly once"

    # 1e-75 sits above the 1e-80 floor and below the 1e-70 ceiling: neither a contact
    # nor a separation this extractor is allowed to claim it can tell apart.
    straddling, straddling_side = synthetic_pose(mp.mpf("1e-75"))
    structure = extract_contacts(
        straddling, straddling_side, sign=kingbird_sign, floor=FLOOR, ambiguity_ratio=RATIO
    )
    assert structure.ambiguous, "displacing a square into the band produced no ambiguity"
    require_refusal(
        lambda: require_decided(structure), "undecidable-incidence", "perturbed margin"
    )


def bad_requests() -> None:
    require_refusal(
        lambda: extract_contacts([], 1, sign=exact_sign), "bad-request", "no squares"
    )


def main() -> int:
    perturbation_control()
    bad_requests()
    trump11_known_answer()
    kingbird29_measurement()
    print("contact extraction contract selftest passed")
    return 0


def test_promote_contacts() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
