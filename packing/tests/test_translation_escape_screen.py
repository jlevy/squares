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
import pytest
import yaml

from devtools import screen_translation_escape
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
    check_sample,
    identity_errors,
    load_record,
    manifest_entries,
    schema_errors,
    screen_corpus,
    screen_errors,
    screen_record,
    shape_residual,
    translated,
)
from sqpack.known_best import KNOWN_BEST_CORPUS, parse_unitsquare_svg, unitsquare_witness
from sqpack.verify import float_sign, verify_packing
from sqpack.witness import witness_document

FRONTIER = ROOT / "frontier"
GOLDEN_SCREENED = {"n=1..100": 100, "n=1..200": 200, "n=1..324": 324}
#: The UnitSquare renderings expose six-decimal polygon coordinates, so their shape
#: residual exceeds the screen's limit and they are excluded by measurement (think-ecqk).
#: n = 68, 103, 105, 110 and 131 were excluded the same way until their records moved to
#: Couzo's binary64 packings (T-056) on 2026-09-29, and n = 69, the last, until its record
#: moved to the catalogue's packing (T-088) on 2026-10-05. None is excluded now; the
#: retained rendering of n = 69 is still what the exclusion is tested on.
GOLDEN_EXCLUDED: dict[str, list[int]] = {
    "n=1..100": [],
    "n=1..200": [],
    "n=1..324": [],
}
#: The retained UnitSquare rendering the exclusion controls are built from.
RENDERING = ROOT / "resources/web/known-best-packings/unitsquare/n069.svg"


def _rendering_entry(directory: Path) -> dict[str, Any]:
    """A manifest entry for the n = 69 rendering's witness, written where the test says.

    The corpus no longer draws on a rendering, so the control the screen's exclusion needs
    is built from the retained bytes, exactly as the atlas built n = 69 until 2026-10-05.
    """
    geometry = parse_unitsquare_svg(RENDERING.read_text(encoding="utf-8"), expected_n=69)
    witness = unitsquare_witness(
        69, geometry, source_path=str(RENDERING), source_url="https://example.invalid/n069.svg"
    )
    path = directory / "n-069-rendering.yaml"
    path.write_text(
        witness_document(witness, schema="../witness.schema.yaml"), encoding="utf-8"
    )
    return {
        "n": 69,
        "reported_side": geometry.side,
        "witness": {"path": str(path)},
        "source": {"kind": "unitsquare-rendering"},
    }


#: Cases whose movable-square count differs between the screen's four tolerances; each
#: still carries a replayed hit at the primary tolerance. Couzo's and de Winter's poses
#: carry binary64 coordinates, so a contact gap near the tightest tolerance moves more
#: of them than it moved the 28-digit records they replaced.
GOLDEN_UNSTABLE = {
    "n=1..100": [68, 70, 84, 86, 88],
    "n=1..200": [
        68,
        70,
        84,
        86,
        88,
        102,
        103,
        105,
        106,
        108,
        110,
        123,
        126,
        127,
        129,
        130,
        131,
        132,
        146,
        154,
        155,
        172,
        175,
        177,
        179,
        180,
        199,
    ],
    "n=1..324": [
        68,
        70,
        84,
        86,
        88,
        102,
        103,
        105,
        106,
        108,
        110,
        123,
        126,
        127,
        129,
        130,
        131,
        132,
        146,
        154,
        155,
        172,
        175,
        177,
        179,
        180,
        199,
        206,
        207,
        209,
        210,
        211,
        228,
        236,
        238,
        239,
        241,
        258,
        259,
        261,
        263,
        266,
        267,
        268,
        269,
        271,
        272,
        273,
        292,
        295,
        297,
        301,
        302,
        303,
        304,
        305,
        306,
        307,
    ],
}

"""Records screened at a corpus whose result has actually been looked at.

The count itself is derived below -- the corpus less the shape-residual exclusions -- so
widening the corpus does not falsify this test. What this pins is the one corpus whose
number someone has checked, so a change *at* `n = 1..100` still fails."""
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
    # The screen covers the whole corpus less whatever its own shape-residual limit
    # excluded, so the count follows `KNOWN_BEST_CORPUS` rather than a literal.
    screened = KNOWN_BEST_CORPUS.count - len(screen["excluded"])
    assert screen["aggregate"]["records_screened"] == screened
    golden = GOLDEN_SCREENED.get(KNOWN_BEST_CORPUS.label)
    assert golden is None or screened == golden
    # Every hit is replayed at the primary tolerance, so a case whose hit count moves
    # between tolerances is still soundly not-rigid; it is listed rather than hidden, and
    # the list is pinned per corpus so a new one cannot arrive unnoticed.
    unstable = sorted(
        case["n"] for case in screen["cases"] if not case["stable_across_tolerances"]
    )
    assert unstable == GOLDEN_UNSTABLE.get(KNOWN_BEST_CORPUS.label, unstable)
    assert screen["aggregate"]["tolerance_disagreement_ns"] == unstable


def test_small_records_rescreen_to_the_retained_result() -> None:
    """Recompute a few records from the witnesses, not from the retained file."""
    cases = _cases()
    entries = {entry["n"]: entry for entry in manifest_entries()}
    for n in (5, 10, 11, 27):
        screened = screen_translation_escape._screen_entry(entries[n])  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        assert screened == (True, cases[n])


@pytest.mark.slow
def test_squish_n108_retains_its_replayed_tolerance_instability() -> None:
    entry = next(row for row in manifest_entries() if row["n"] == 108)
    screened = screen_translation_escape._screen_entry(entry)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert screened == (True, _cases()[108])
    assert screened[1]["stable_across_tolerances"] is False


def test_every_retained_result_names_the_record_the_manifest_holds() -> None:
    entries = {entry["n"]: entry for entry in manifest_entries()}
    assert identity_errors(_screen(), entries) == []


def test_the_sampled_check_refuses_a_record_replaced_under_the_screen(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Run 37268431203: T-092 replaced n = 208, 209, 228, 263, 272, 303 and 306 without a
    # re-screen, none of the seven is on the sampled stride, and only the deferred
    # re-screen after the merge saw it. A replaced record now fails the sampled check.
    retained = _cases()[208]["reported_side"]
    replaced = [
        {**entry, "reported_side": "14.9"} if entry["n"] == 208 else entry
        for entry in manifest_entries()
    ]
    monkeypatch.setattr(screen_translation_escape, "manifest_entries", lambda: replaced)
    with pytest.raises(ValueError, match=f"n=208: screened on the record of side {retained}"):
        # A stride longer than the corpus replays n = 1 alone; the identity check covers
        # every record whatever the stride.
        check_sample(stride=KNOWN_BEST_CORPUS.count)


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


def test_exclusions_are_measured_rather_than_asserted(tmp_path: Path) -> None:
    """A rendering is dropped by a measurement, and it is not a close call."""
    excluded = _screen()["excluded"]
    assert [item["n"] for item in excluded] == GOLDEN_EXCLUDED[KNOWN_BEST_CORPUS.label]
    for item in excluded:
        assert item["bead"] == "think-ecqk"
        assert mp.mpf(item["shape_residual"]) > mp.mpf("1e-9")
    screened, exclusion = screen_translation_escape._screen_entry(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        _rendering_entry(tmp_path)
    )
    assert screened is False
    assert exclusion["bead"] == "think-ecqk"
    assert mp.mpf(exclusion["shape_residual"]) > mp.mpf("1e-9")
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


def test_a_pool_worker_screens_at_the_same_precision_as_this_process(tmp_path: Path) -> None:
    """The corpus is screened across processes, and the precision is per-process state.

    `mp.mp.dps` is a global that a `forkserver` or `spawn` child does not inherit, and a
    worker left at mpmath's default of 15 digits does not raise.  It returns a
    differently rounded case, which is the one failure this screen cannot afford: the
    output would read as a result rather than as a bug.

    Two derivations, and a control that stops them agreeing vacuously.  The control
    screens one record's already-materialized geometry at 15 digits and requires the
    published decimals to move, so the working precision is load bearing here rather
    than decorative.  The comparison then requires a real two-process run, over a
    screened case and an excluded record, to reproduce the single-process result exactly
    -- through `screen_corpus` itself, so what is checked is the path the tool takes.
    """
    squares, side, square_ids = load_record(10)
    mp.mp.dps = DIGITS
    at_working_precision = screen_record(10, squares, side, square_ids)
    mp.mp.dps = 15
    try:
        lowered = screen_record(10, squares, side, square_ids)
    finally:
        mp.mp.dps = DIGITS
    assert lowered != at_working_precision

    entries = [entry for entry in manifest_entries() if entry["n"] == 10]
    entries.append(_rendering_entry(tmp_path))
    original = screen_translation_escape.manifest_entries
    screen_translation_escape.manifest_entries = lambda: entries
    try:
        serial = screen_corpus(1)
        pooled = screen_corpus(2)
    finally:
        screen_translation_escape.manifest_entries = original

    assert [case["n"] for case in serial[0]] == [10]
    assert [item["n"] for item in serial[1]] == [69]
    assert pooled == serial
