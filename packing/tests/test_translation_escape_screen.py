#!/usr/bin/env python3
"""Replay, contract, and mutation controls for the single-square translation screen.

The screen's whole value is that a hit is a certificate rather than an opinion, so the
controls here are about whether the certificate could fail: an independent rescreen of
small records, the closed forms the certified slides must equal, the catalogue's own
rigidity flags, and a mutation that must break the replay.  A screen whose replay
accepts an overstated slide is not checking anything.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import mpmath as mp
import yaml

from devtools.screen_translation_escape import (
    DIGITS,
    OUTPUT,
    PRIMARY_TOLERANCE,
    ROOT,
    SEPARATING,
    SHAPE_RESIDUAL_LIMIT,
    SLIDING,
    ActiveContacts,
    RecordGeometry,
    load_record,
    schema_errors,
    screen_errors,
    screen_record,
    shape_residual,
    translated,
)
from sqpack.verify import float_sign, verify_packing

FRONTIER = ROOT / "frontier"
# Closed forms the retained certificates must reproduce, from the geometry of each
# packing rather than from this screen: a corner rattler in a square pocket slides the
# pocket's diagonal.  Evaluated inside the tests, at the screen's working precision.
CLOSED_FORMS = {
    10: lambda: mp.sqrt(2) / 2 - mp.mpf(1) / 2,
    27: lambda: 3 / mp.sqrt(2) - 2,
    38: lambda: 2 * mp.sqrt(2) - mp.mpf(5) / 2,
    67: lambda: 3 * mp.sqrt(2) - 4,
}


def _screen() -> dict[str, Any]:
    mp.mp.dps = DIGITS
    return json.loads(OUTPUT.read_text(encoding="utf-8"))["screen"]


def _cases() -> dict[int, dict[str, Any]]:
    return {case["n"]: case for case in _screen()["cases"]}


def _packing_record(n: int) -> dict[str, Any]:
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---\n")[1])["packing"]


def _rigid_flag(n: int) -> bool | None:
    """Whether the catalogue calls this packing rigid.

    The field was a tri-state boolean (`rigid`) and became a three-valued enum
    (`catalogue_rigid`: rigid / semi-rigid / not-stated), because `false` had meant
    "the catalogue did not say" while reading as "not rigid". Only an explicit
    "rigid" is a positive claim here; "semi-rigid" is not, and neither is silence.
    Both spellings are read so this cross-check cannot go vacuous across the rename.
    """
    bound = _packing_record(n).get("reported_upper_bound", {})
    catalogue = bound.get("catalogue_rigid")
    if catalogue is not None:
        return True if catalogue == "rigid" else None
    value = bound.get("rigid")
    if isinstance(value, dict):
        value = value.get("value")
    return value if isinstance(value, bool) else None


def test_retained_screen_satisfies_its_own_contract() -> None:
    document = json.loads(OUTPUT.read_text(encoding="utf-8"))
    assert document["softschema"]["contract"] == "packing.squares:TranslationEscapeScreen/v1"
    assert document["softschema"]["status"] == "enforced"
    screen = document["screen"]
    assert schema_errors(screen) == []
    assert screen_errors(screen) == []
    assert screen["aggregate"]["records_screened"] == 98
    assert all(case["stable_across_tolerances"] for case in screen["cases"])
    assert screen["aggregate"]["tolerance_disagreement_ns"] == []


def test_small_records_rescreen_to_the_retained_result() -> None:
    """Recompute a few records from the witnesses, not from the retained file."""
    cases = _cases()
    for n in (5, 10, 11, 27):
        squares, side, square_ids = load_record(n)
        assert screen_record(n, squares, side, square_ids) == cases[n]


def test_certified_slides_equal_their_closed_forms() -> None:
    """The four documented rattler pairs, checked against the algebra they come from."""
    cases = _cases()
    for n, closed_form in CLOSED_FORMS.items():
        expected = closed_form()
        case = cases[n]
        separating = [
            item for item in case["movable_squares"] if item["witness_kind"] == SEPARATING
        ]
        assert case["separating_square_count"] == 2
        assert len(separating) == 2
        diagonal = mp.sqrt(2) / 2
        for item in separating:
            x, y = mp.mpf(item["direction"]["x"]), mp.mpf(item["direction"]["y"])
            off_diagonal = f"n={n} does not slide along a 45 degree diagonal"
            assert abs(abs(x) - diagonal) < mp.mpf("1e-20"), off_diagonal
            assert abs(x) == abs(y), off_diagonal
        assert {
            (mp.sign(mp.mpf(item["direction"]["x"])), mp.sign(mp.mpf(item["direction"]["y"])))
            for item in separating
        } == {(1, 1), (-1, -1)}
        for item in separating:
            # The file rounds to 21 significant digits; agreement to 1e-21 is agreement
            # to every digit it publishes.
            assert abs(mp.mpf(item["slide_distance"]) - expected) < mp.mpf("1e-21")


def test_a_proved_optimal_packing_still_has_rattlers() -> None:
    """n=10 is proved optimal and moves anyway: optimality and rigidity are separate."""
    assert _packing_record(10)["status"] == "proved"
    assert _cases()[10]["separating_square_count"] == 2


def test_no_record_the_catalogue_calls_rigid_has_any_play() -> None:
    """The catalogue's rigid flags and this screen must not contradict each other.

    A hit on a record flagged rigid would be a real finding about the catalogue or about
    the witness, so it fails here rather than passing quietly.
    """
    cases = _cases()
    flagged = [n for n in cases if _rigid_flag(n) is True]
    assert flagged, "no record carries a rigidity flag; the cross-check would be vacuous"
    for n in flagged:
        assert cases[n]["movable_square_count"] == 0, f"n={n} is flagged rigid but has play"


def test_exclusions_are_measured_rather_than_asserted() -> None:
    """n=68 and n=69 are dropped by a measurement, and it is not a close call."""
    excluded = _screen()["excluded"]
    assert [item["n"] for item in excluded] == [68, 69]
    for item in excluded:
        assert item["bead"] == "think-ecqk"
        assert mp.mpf(item["shape_residual"]) > mp.mpf("1e-9")
    squares, _, _ = load_record(27)
    assert shape_residual(squares) < SHAPE_RESIDUAL_LIMIT


def test_replay_rejects_an_overstated_slide() -> None:
    """The mutation control: the replay must fail on a distance the geometry forbids.

    Doubling a certified slide drives the square into whatever stopped it.  If the
    replay still accepted the packing, the build-time replay that gates every published
    certificate would be decoration.
    """
    certificate = _cases()[27]["movable_squares"][0]
    squares, side, _ = load_record(27)
    direction = (
        mp.mpf(certificate["direction"]["x"]),
        mp.mpf(certificate["direction"]["y"]),
    )
    distance = mp.mpf(certificate["slide_distance"])
    index = certificate["square_index"]
    tolerance = float_sign(mp.mpf(PRIMARY_TOLERANCE))
    honest = verify_packing(
        translated(squares, index, direction, distance),
        side,
        sign=tolerance,
        check_shapes=False,
        bucket=True,
    )
    overstated = verify_packing(
        translated(squares, index, direction, 2 * distance),
        side,
        sign=tolerance,
        check_shapes=False,
        bucket=True,
    )
    assert honest.valid
    assert not overstated.valid


def _contact_degrees(n: int) -> tuple[list[int], set[int]]:
    """Active blockers per square, and which squares the screen found movable."""
    mp.mp.dps = DIGITS
    squares, side, _ = load_record(n)
    geometry = RecordGeometry(squares, side)
    tolerance = mp.mpf(PRIMARY_TOLERANCE)
    degrees = [
        len(ActiveContacts(geometry, index, tolerance).groups) for index in range(len(squares))
    ]
    return degrees, {item["square_index"] for item in _cases()[n]["movable_squares"]}


def test_no_clearance_or_contact_count_heuristic_would_find_these() -> None:
    """Why the screen is not replaceable by a cheap proxy.

    Every square in every retained record touches something, so free space finds
    nothing; and contact degree does not separate the movable squares either.  In
    n = 57 a movable square and an immovable one carry the same number of active
    blockers, and the degree that is movable in n = 27 is immovable in n = 5.
    """
    for n in (5, 10, 27, 57):
        degrees, _ = _contact_degrees(n)
        assert all(degree > 0 for degree in degrees), f"n={n} has a square touching nothing"

    degrees, movable = _contact_degrees(57)
    moving = {degrees[index] for index in movable}
    fixed = {degrees[index] for index in range(len(degrees)) if index not in movable}
    assert moving & fixed, "contact degree would have separated the movable squares"

    loose, movable = _contact_degrees(27)
    rigid_degrees, no_play = _contact_degrees(5)
    assert not no_play
    assert {loose[index] for index in movable} & set(rigid_degrees)


def test_the_artifact_states_its_own_one_sidedness() -> None:
    """The file has to carry the epistemics, not just this module's docstring."""
    screen = _screen()
    assert "rigidity" in screen["one_sidedness"]
    assert any("cannot establish rigidity" in claim for claim in screen["claim_boundaries"])
    kinds = {
        item["witness_kind"] for case in screen["cases"] for item in case["movable_squares"]
    }
    assert kinds == {SEPARATING, SLIDING}


def test_schema_is_declared_where_the_artifact_says_it_is() -> None:
    document = json.loads(OUTPUT.read_text(encoding="utf-8"))
    declared = Path(OUTPUT).parent / document["softschema"]["schema"]
    assert declared.is_file()
    assert (
        yaml.safe_load(declared.read_text(encoding="utf-8"))["$id"]
        == (document["softschema"]["contract"])
    )
