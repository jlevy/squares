#!/usr/bin/env python3
"""The rigidity register is re-read from the source, not migrated forward.

`reported_upper_bound.rigid` was a boolean that carried two incompatible jobs. It was
non-null exactly where the catalogue pictured the packing, so `false` meant "pictured,
no Rigid annotation" -- absence of a source statement -- while reading as "this packing
is not rigid". Taken literally the corpus denied the rigidity of `n = 1`: one unit
square exactly filling a 1x1 container, which cannot move at all. Nothing wrote the
field and nothing checked it, so when `n = 11`'s annotation was dropped the corpus kept
validating.

The field is now two: `catalogue_rigid`, a three-valued transcription in the source's
own vocabulary, and a case-level `rigidity`, this repository's own finding with an
assurance level and replayable evidence. These tests hold both in place and check the
transcription against the retained catalogue for every n, so a dropped annotation fails
instead of passing silently.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest
import yaml
from jsonschema import Draft202012Validator

from devtools.audit_kingbird_catalogue import (
    CATALOGUE_MARKDOWN,
    NOT_STATED,
    RIGIDITY_STATES,
    CatalogueFormatError,
    audit_rigidity,
    catalogue_entries,
    catalogue_rigidity,
    load_frontier_cases,
)
from devtools.migrate_frontier_v2 import migrate_case
from sqpack.assurance import check_evidence_semantics

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTIER = PROJECT_ROOT / "frontier"

# The catalogue annotates rigidity for exactly these four packings at n <= 100, and
# each is identified by the side value printed above its annotation -- currently at
# lines 44, 80, 163 and 224, though the archive's line numbers are not the contract and
# nothing here matches by position.
ANNOTATED = {
    5: "2.70710678118654",
    11: "3.87708359002281",
    28: "5.82444461667405",
    40: "6.82842712474619",
}


def catalogue_text() -> str:
    return CATALOGUE_MARKDOWN.read_text(encoding="utf-8")


def test_catalogue_annotates_four_packings_and_denies_rigidity_nowhere() -> None:
    entries = catalogue_entries(catalogue_text())
    annotated = {
        n: entry
        for entry in entries
        for n in entry.listed_n
        if entry.rigidity != NOT_STATED and n <= 100
    }
    assert sorted(annotated) == sorted(ANNOTATED)
    for n, printed_side in ANNOTATED.items():
        entry = annotated[n]
        assert entry.rigidity == "rigid"
        assert entry.printed_side == printed_side
        # The annotation sits directly under the side value it qualifies. That
        # adjacency is what makes "the value printed above it" a usable identity.
        assert entry.rigidity_line == entry.side_line + 1

    # The source has no vocabulary for "this packing is not rigid". It annotates or it
    # is silent, which is why `not-stated` and not `false` is the third value.
    lowered = catalogue_text().lower()
    for phrasing in ("not rigid", "non-rigid", "nonrigid"):
        assert phrasing not in lowered


def test_every_record_transcribes_what_the_catalogue_says() -> None:
    assert audit_rigidity() == []


def test_the_audit_fails_on_a_dropped_or_invented_annotation() -> None:
    cases = {n: dict(case) for n, case in load_frontier_cases().items()}

    # n = 11's annotation went missing once and nothing noticed. Now it does.
    dropped = deepcopy(cases)
    upper = cast("dict[str, object]", dropped[11]["reported_upper_bound"])
    upper["catalogue_rigid"] = NOT_STATED
    errors = audit_rigidity(cases=dropped)
    assert any("n=11" in error and "'rigid'" in error for error in errors)

    # And the opposite: a rigidity claim the source never made.
    invented = deepcopy(cases)
    upper = cast("dict[str, object]", invented[1]["reported_upper_bound"])
    upper["catalogue_rigid"] = "rigid"
    assert any("n=1:" in error for error in audit_rigidity(cases=invented))

    # A boolean is no longer a legal value at all.
    legacy = deepcopy(cases)
    upper = cast("dict[str, object]", legacy[5]["reported_upper_bound"])
    upper["catalogue_rigid"] = False
    assert any("not one of" in error for error in audit_rigidity(cases=legacy))


def test_the_audit_matches_by_printed_decimal_rather_than_position() -> None:
    cases = {n: deepcopy(dict(case)) for n, case in load_frontier_cases().items()}
    upper = cast("dict[str, object]", cases[28]["reported_upper_bound"])
    upper["value"] = "5.82444461667000"
    errors = audit_rigidity(cases=cases)
    assert any("re-read the source" in error for error in errors)

    # An annotation belongs to the side value printed above it, wherever that block
    # sits. Two blocks in either order carry their own annotations with them.
    first = _block(7, "1.5", annotated=False)
    second = _block(8, "2.25", annotated=True)
    for listing in (first + second, second + first):
        entries = {entry.printed_side: entry.rigidity for entry in catalogue_entries(listing)}
        assert entries == {"1.5": NOT_STATED, "2.25": "rigid"}


def test_a_parser_that_sees_nothing_fails_instead_of_agreeing() -> None:
    # Silent parse failure would make every record "not-stated" and every comparison
    # pass. That is the failure mode this audit exists to prevent.
    blinded = catalogue_text().replace("squares_in_squares__rigid.html", "squares.html")
    errors = audit_rigidity(catalogue_text=blinded)
    assert any("no rigidity annotation parsed" in error for error in errors)

    with pytest.raises(CatalogueFormatError):
        catalogue_entries("nothing here resembles the catalogue")


def test_catalogue_rigid_is_a_transcription_and_carries_no_judgement() -> None:
    by_n = catalogue_rigidity(catalogue_text())
    for n in range(1, 101):
        case = _case(n)
        recorded = case["reported_upper_bound"]["catalogue_rigid"]
        assert recorded in RIGIDITY_STATES
        assert not isinstance(recorded, bool)
        entry = by_n.get(n)
        assert recorded == (entry.rigidity if entry else NOT_STATED)

    # The trivially rigid grid packings were the plainest casualty of the boolean: one
    # unit square exactly filling a 1x1 container cannot move, and the old field said
    # `false`. `not-stated` now says only that the catalogue is silent about them.
    for n in (1, 4, 9, 16, 25, 36, 49, 64, 81, 100):
        assert _case(n)["reported_upper_bound"]["catalogue_rigid"] == NOT_STATED

    # Silence is not evidence, so a `not-stated` transcription may never appear as a
    # first-party rigidity claim. The first-party field is now populated for every n by
    # devtools/assess_frontier_rigidity.py, which is why this asserts what the block may
    # SAY rather than that it is absent: `not-rigid` and `undetermined` are findings of
    # ours, and neither borrows the catalogue's word.
    for n in range(1, 101):
        recorded = _case(n)["reported_upper_bound"]["catalogue_rigid"]
        rigidity = _case(n)["rigidity"]
        assert rigidity is not None, f"n={n}: rigidity is unassessed"
        if recorded == NOT_STATED and rigidity["property"] == "locally-rigid":
            # Only an argument of our own may claim rigidity where the source is silent.
            assert rigidity["assurance"] == "verified", (
                f"n={n}: claims rigidity the catalogue does not state, without a "
                f"verified first-party argument"
            )
    # And a source that DOES say rigid still never supplies the finding.
    for n in (5, 28, 40):
        assert _case(n)["reported_upper_bound"]["catalogue_rigid"] == "rigid"
        assert _case(n)["rigidity"]["property"] == "undetermined"


def test_the_first_party_finding_for_n11_is_carried_with_its_assurance() -> None:
    rigidity = _case(11)["rigidity"]
    assert rigidity is not None
    assert rigidity["property"] == "locally-rigid"
    assert rigidity["assurance"] == "verified"
    assert rigidity["method"] == "exact-algebraic"
    # The certificate is first order and local. The scope field has to say so, because
    # the catalogue's unqualified "Rigid." does not.
    assert "First order" in rigidity["scope"]
    assert "global optimality" in rigidity["scope"]
    assert (PROJECT_ROOT / rigidity["certificate"]).is_file()

    # A replay nobody can run is not evidence. exp-013's own record still names an
    # entry point that no longer exists, so the module named here is resolved to a
    # file rather than trusted.
    replay = rigidity["replay"].split()
    assert "--replay" in replay
    module = replay[replay.index("-m") + 1]
    assert (PROJECT_ROOT / Path(*module.split("."))).with_suffix(".py").is_file()
    assert (PROJECT_ROOT / replay[replay.index("--replay") + 1]).is_file()

    evidence = {
        record["id"]: record
        for record in yaml.safe_load((FRONTIER / "evidence.yaml").read_text(encoding="utf-8"))[
            "evidence"
        ]
    }
    for reference in rigidity["evidence"]:
        record = evidence[reference]
        assert check_evidence_semantics(record) == []
        assert record["assurance"] == "verified"
        assert record["scope"] == {"n_values": [11]}
        assert reference in _case(11)["evidence"]

    # The catalogue's transcription and the repository's finding are different claims
    # about n = 11 and both are recorded, separately.
    assert _case(11)["reported_upper_bound"]["catalogue_rigid"] == "rigid"


def test_the_v1_migration_emits_the_split_fields() -> None:
    # The migration was the only code that ever touched the old boolean, and it copied
    # it forward unread. It now translates, and leaves the first-party field unasserted.
    legacy = {
        "n": 11,
        "status": "open",
        "upper_bound": {
            "value": 3.87708359002281,
            "value_str": "3.87708359002281",
            "exact_form": None,
            "method": "hand_construction",
            "rigid": True,
            "catalogue_pictured": True,
        },
        "lower_bound": {"value": 3.788854382, "exact_form": None, "kind": "nagamochi"},
        "conjectured_optimum": None,
        "priority_notes": [],
        "resources": [],
    }
    migrated = migrate_case(legacy)
    upper = cast("dict[str, object]", migrated["reported_upper_bound"])
    assert upper["catalogue_rigid"] == "rigid"
    assert "rigid" not in upper
    assert migrated["rigidity"] is None

    silent = deepcopy(legacy)
    cast("dict[str, object]", silent["upper_bound"])["rigid"] = False
    quiet = cast("dict[str, object]", migrate_case(silent)["reported_upper_bound"])
    assert quiet["catalogue_rigid"] == NOT_STATED


def test_the_schema_rejects_the_boolean_and_requires_the_transcription() -> None:
    schema = yaml.safe_load(
        (FRONTIER / "square-packing-case.schema.yaml").read_text(encoding="utf-8")
    )
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    case = _case(5)
    assert list(validator.iter_errors(case)) == []

    revived = deepcopy(case)
    revived["reported_upper_bound"]["rigid"] = True
    assert list(validator.iter_errors(revived))

    dropped = deepcopy(case)
    del dropped["reported_upper_bound"]["catalogue_rigid"]
    assert list(validator.iter_errors(dropped))

    invented = deepcopy(case)
    invented["reported_upper_bound"]["catalogue_rigid"] = "not-rigid"
    assert list(validator.iter_errors(invented))

    missing_rigidity = deepcopy(case)
    del missing_rigidity["rigidity"]
    assert list(validator.iter_errors(missing_rigidity))

    unsupported = deepcopy(case)
    unsupported["rigidity"] = {"property": "locally-rigid"}
    assert list(validator.iter_errors(unsupported))


def _block(n: int, printed_side: str, *, annotated: bool) -> str:
    """One catalogue block in the archive's shape, for order-independence checks."""
    annotation = "[Rigid.](squares_in_squares__rigid.html)  \n" if annotated else ""
    return (
        f"{n}  \n"
        f"[](square-{n}.svg)\n"
        f"\n"
        f"$s = \\Nn{{{printed_side}}}$  \n"
        f"{annotation}"
        f"Found by nobody in particular.\n"
        f"\n"
    )


def _case(n: int) -> dict:
    path = FRONTIER / f"n-{n:03d}.md"
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
