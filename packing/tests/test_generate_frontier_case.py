#!/usr/bin/env python3
"""The generator's rules must be the rules the hand-written register already follows.

`devtools/generate_frontier_case.py` drafts a `SquarePackingCase/v2` record for an `n`
the register does not yet cover. Nothing about that is checkable by reading the output:
a record can validate, read fluently, and still carry a bound rule that the first hundred
cases do not use. So the generator is pointed back at cases a person wrote and asked to
reproduce them **field by field**, on the same inputs.

Seven cases, chosen so that every branch of the generator is exercised by a record whose
correctness someone already argued:

- `n = 100` and `n = 64` -- perfect squares. The lower bound is the area bound, the
  resource block drops Nagamochi, and the roll-up carries four evidence ids.
- `n = 99` and `n = 98` -- `m^2 - 1` and `m^2 - 2`. Proved on Nagamochi's exact branch,
  reported as the integer, with the three-resource block.
- `n = 50` -- open, catalogue-sourced, with a certified ceiling that trails the report
  and the `mathematics` blocker that gap requires.
- `n = 68` and `n = 69` -- open, and sourced from the UnitSquare release rather than the
  catalogue: a forty-five figure reported side, a `source-evidence` blocker instead of a
  `mathematics` one, a fourth resource, and a null `conjectured_optimum`. They are the
  only two records of that shape at `n <= 100`, and `n = 103, 105, 110` and `131` will be
  generated from the same branch.

**Nothing is skipped quietly.** Every key of the front matter is compared. The three
kinds of mismatch a reader would want to know about are named separately:

- `GENERATOR_OWNS` -- must be byte-equal. A difference here is a failure.
- `SUPPLIED` -- values this test hands the generator rather than letting it derive: the
  two dates, which no source carries, and the three credit-line facts, which the
  injected-facts path passes in so that the comparison tests assembly rather than
  parsing. The test reports that it did, so nobody reads their agreement as a
  derivation.
- `NOT_REPRODUCED` -- fields the generator deliberately leaves for a later step, which
  is `rigidity` and, for three cases, a hand-written body.

`test_reports_what_the_adapter_cannot_derive` is the same comparison run through the real
catalogue parser instead of injected facts. All three credit-line fields are now read off
`CatalogueEntry.credit_line`, `improved_by` included, and at `n = 50` all three
reproduce: the rule reads the page's dated "Improved by" sentences, of which `n = 50` has
none, and deliberately does not read the "Optimized by" sentence the hand pass read at
`n = 29` and ignored at `n = 39, 41, 50, 51, 71`.
"""

from __future__ import annotations

import math
import re
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

from devtools import validate_schemas
from devtools.check_basic_bounds import check_case_basic_bounds
from devtools.check_case_prose import check_case_file
from devtools.generate_frontier_case import (
    CATALOGUE_CLASSIFICATION,
    GRID_CLASSIFICATION,
    GRID_COMPLETENESS_EVIDENCE,
    KINGBIRD_EVIDENCE,
    UNITSQUARE_AVAILABILITY_KEY,
    UNITSQUARE_EVIDENCE,
    UNITSQUARE_SOURCE_KEY,
    CatalogueFacts,
    GenerationError,
    SourceAvailability,
    analytically_optimized_from_credit,
    build_payload,
    construction_method_from_credit,
    credited_surnames,
    facts_from_catalogue_entry,
    generate_record,
    grid_ceiling,
    load_availability,
    load_unitsquare_release,
    main,
    method_summary,
    record_path,
    refuse_reason,
    without_rigidity,
    write_record,
)
from sqpack.assurance import check_case_semantics
from sqpack.yamlio import safe_load

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTIER = PROJECT_ROOT / "frontier"
SCHEMA = FRONTIER / "square-packing-case.schema.yaml"

GOLDEN_CASES = (100, 99, 98, 69, 68, 64, 50)

#: Front-matter paths the generator derives from its inputs and must reproduce exactly.
#: Everything not named in the two sets below falls here, so a field added to the schema
#: is compared by default rather than forgotten.
SUPPLIED = {
    "packing.source_reviewed": "the review date is an argument; no source carries it",
    "packing.reported_upper_bound.retrieved_date": (
        "the fetch date is an argument; the catalogue does not date itself"
    ),
    "packing.reported_upper_bound.construction_method": (
        "injected here from the record itself; the generator reads it off the catalogue's "
        "credit line, which test_reports_what_the_adapter_cannot_derive exercises"
    ),
    "packing.reported_upper_bound.analytically_optimized": (
        "injected from the same place, and read off the same credit line"
    ),
    "packing.reported_upper_bound.improved_by": (
        "injected here from the record itself; the generator reads the page's dated "
        "'Improved by' sentences, which test_reports_what_the_adapter_cannot_derive and "
        "test_the_improvement_rule_reproduces_the_hand_transcription exercise"
    ),
}
NOT_REPRODUCED = {
    "packing.rigidity": (
        "left null on purpose: the translation-escape screen and the rigidity assessment "
        "write this field later in the promotion path"
    ),
}
#: Cases whose prose is bespoke rather than templated, and why.
BODY_NOT_REPRODUCED = {
    100: "an editorial section about the edge of the corpus, written for this one case",
    68: (
        "one figure: the body prints the Nagamochi lower bound to five places where every "
        "other record in the corpus, and the generator, print six"
    ),
    69: (
        "a sentence about the parent's degree-82 polynomial being dropped, written for "
        "this one case, and a shorter paraphrase of the release's verification claims"
    ),
}

#: How the source map would classify a record the register already carries.
GRID = "grid"
CATALOGUE = "catalogue"
UNITSQUARE = "unitsquare"


def _source_kind(payload: Mapping[str, Any]) -> str:
    reported = payload["reported_upper_bound"]
    if reported["source_key"] == UNITSQUARE_SOURCE_KEY:
        return UNITSQUARE
    return GRID if reported["construction_method"] == "trivial-grid" else CATALOGUE


def _availability(n: int, kind: str) -> SourceAvailability:
    if kind == GRID:
        return SourceAvailability(
            n, GRID_CLASSIFICATION, "catalogue-trivial-grid-rule", grid_ceiling(n)
        )
    if kind == UNITSQUARE:
        return SourceAvailability(
            n, CATALOGUE_CLASSIFICATION, UNITSQUARE_AVAILABILITY_KEY, None
        )
    return SourceAvailability(n, CATALOGUE_CLASSIFICATION, "kingbird-current-catalogue", None)


def _parsed_facts(n: int) -> CatalogueFacts:
    """The catalogue entry for `n` as the real parser reads it."""
    catalogue = pytest.importorskip("sqpack.kingbird_catalogue")
    return facts_from_catalogue_entry(catalogue.parse_catalogue()[n], n=n)


def _committed(n: int) -> tuple[dict[str, Any], str]:
    """The committed record's front matter document and body."""
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    _, front, body = text.split("---\n", 2)
    return safe_load(front), body


def _injected_facts(n: int) -> CatalogueFacts:
    """A `CatalogueFacts` built from the values the committed record transcribes.

    This is the catalogue entry as a person read it, credit line included, so the
    comparison tests the generator's assembly rather than the parser's reading.
    """
    reported = _committed(n)[0]["packing"]["reported_upper_bound"]
    return CatalogueFacts(
        n=n,
        side_decimal=str(reported["value"]),
        exact_form=reported["exact_form"],
        algebraic_degree=reported["algebraic_degree"],
        minimal_polynomial=reported["minimal_polynomial"],
        found_by=tuple(reported["found_by"]),
        found_year=reported["found_year"],
        catalogue_rigid=reported["catalogue_rigid"],
        catalogue_pictured=reported["catalogue_pictured"],
        construction_method=reported["construction_method"],
        analytically_optimized=reported["analytically_optimized"],
        improved_by=tuple(reported["improved_by"]),
    )


def _regenerate(n: int, *, facts: CatalogueFacts | None = None) -> str:
    """Draft `n` on the same inputs and dates the committed record declares."""
    document, _ = _committed(n)
    payload = document["packing"]
    kind = _source_kind(payload)
    if facts is None and kind == CATALOGUE:
        facts = _injected_facts(n)
    if facts is None and kind == UNITSQUARE:
        # A release case takes no bound from the catalogue, but its prose names the
        # parent the release improved on, and the catalogue's credit chain is where
        # those authors are written down. So this one comes from the real parser.
        facts = _parsed_facts(n)
    return generate_record(
        n,
        availability={n: _availability(n, kind)},
        catalogue=None if facts is None else {n: facts},
        review_date=str(payload["source_reviewed"]),
        retrieved_date=str(payload["reported_upper_bound"]["retrieved_date"]),
    )


def _flatten(value: object, prefix: str = "") -> dict[str, object]:
    """Dotted paths to leaf values; lists are leaves, since these are short and ordered."""
    if not isinstance(value, Mapping):
        return {prefix: value}
    flat: dict[str, object] = {}
    for key, item in value.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        flat.update(_flatten(item, path))
    return flat


def _compare(n: int) -> tuple[dict[str, object], list[str]]:
    """Every front-matter path, with a verdict, plus the paths that failed."""
    committed_document, _ = _committed(n)
    generated_document = safe_load(_regenerate(n).split("---\n", 2)[1])
    committed = _flatten(committed_document)
    generated = _flatten(generated_document)

    verdicts: dict[str, object] = {}
    failures: list[str] = []
    for path in sorted(set(committed) | set(generated)):
        left = committed.get(path, "<absent>")
        right = generated.get(path, "<absent>")
        if path in SUPPLIED or any(path.startswith(f"{key}.") for key in SUPPLIED):
            verdicts[path] = "supplied"
            if left != right:
                failures.append(f"{path}: supplied {right!r} but the record says {left!r}")
        elif path in NOT_REPRODUCED or any(
            path.startswith(f"{key}.") for key in NOT_REPRODUCED
        ):
            verdicts[path] = "not reproduced"
        elif left == right:
            verdicts[path] = "reproduced"
        else:
            verdicts[path] = "MISMATCH"
            failures.append(f"{path}: record {left!r}, generated {right!r}")
    return verdicts, failures


@pytest.mark.parametrize("n", GOLDEN_CASES)
def test_regenerates_a_hand_written_record_field_by_field(n: int) -> None:
    verdicts, failures = _compare(n)
    counts = {
        verdict: sum(1 for value in verdicts.values() if value == verdict)
        for verdict in ("reproduced", "supplied", "not reproduced", "MISMATCH")
    }
    print(f"n={n}: {counts}")
    for path, verdict in verdicts.items():
        if verdict != "reproduced":
            print(f"  {verdict}: {path}")
    assert failures == [], "\n".join(failures)
    # The allowlists are not a place to hide a growing set of exceptions: exactly one
    # front-matter block is left for a later step, and it is `rigidity`.
    unreproduced = [path for path, verdict in verdicts.items() if verdict == "not reproduced"]
    assert unreproduced, "the rigidity block should be reported, not silently absent"
    assert all(path.startswith("packing.rigidity") for path in unreproduced), unreproduced


@pytest.mark.parametrize("n", GOLDEN_CASES)
def test_regenerates_the_prose_a_person_wrote(n: int) -> None:
    committed_body = _committed(n)[1]
    generated_body = _regenerate(n).split("---\n", 2)[2]
    if n in BODY_NOT_REPRODUCED:
        print(f"n={n}: body not reproduced -- {BODY_NOT_REPRODUCED[n]}")
        assert generated_body != committed_body
        return
    assert generated_body == committed_body


@pytest.mark.parametrize("n", GOLDEN_CASES)
def test_the_whole_record_is_byte_identical_apart_from_the_allowlist(n: int) -> None:
    """The only textual differences are the ones the two allowlists already named."""
    committed = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    generated = _regenerate(n)
    if n in BODY_NOT_REPRODUCED:
        return
    # Drop the rigidity block from the committed record and the `rigidity: null` line
    # from the generated one; nothing else may differ. The generator's own `--check`
    # makes exactly this allowance, and uses this function to make it.
    stripped = without_rigidity(committed)
    assert without_rigidity(generated) == stripped


def test_reports_what_the_adapter_cannot_derive() -> None:
    """The same comparison through the real parser, so the gap is named rather than assumed.

    `n = 50`'s credit line reads "Found by Thomas Schadt in December 2025, using a
    simulated annealing program he wrote, starting from randomness. Optimized by David
    Ellsworth." All three credit-line fields fall out of that: the method, the absence of
    the "Not yet analytically optimized" disclaimer, and an empty `improved_by`, because
    the page carries no dated "Improved by" sentence and the "Optimized by" form is the
    one the hand pass read inconsistently and the rule therefore does not read.
    """
    facts = _parsed_facts(50)
    generated = safe_load(_regenerate(50, facts=facts).split("---\n", 2)[1])
    committed, _ = _committed(50)

    generated_upper = generated["packing"]["reported_upper_bound"]
    committed_upper = committed["packing"]["reported_upper_bound"]
    credit_fields = {
        key: (committed_upper[key], generated_upper[key])
        for key in ("construction_method", "analytically_optimized", "improved_by")
    }
    print(f"n=50 through the real parser, credit-line fields: {credit_fields}")
    assert generated_upper["construction_method"] == "simulated-annealing"
    assert generated_upper["analytically_optimized"] is True
    assert generated_upper["improved_by"] == []
    for key in ("value", "exact_form", "algebraic_degree", "minimal_polynomial"):
        assert generated_upper[key] == committed_upper[key], key
    for key in ("found_by", "found_year", "catalogue_rigid", "catalogue_pictured"):
        assert generated_upper[key] == committed_upper[key], key
    for key in ("construction_method", "analytically_optimized"):
        assert generated_upper[key] == committed_upper[key], key


@pytest.mark.parametrize("n", GOLDEN_CASES)
def test_a_regenerated_record_validates_and_replays(n: int, tmp_path: Path) -> None:
    """Schema, cross-field assurance, bound instantiation and prose, on generated bytes."""
    shutil.copy(SCHEMA, tmp_path / SCHEMA.name)
    path = record_path(tmp_path, n)
    write_record(_regenerate(n), path)
    assert validate_schemas.check(path) == []

    payload = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
    assert check_case_semantics(payload, _evidence()) == []
    assert check_case_basic_bounds(payload) == []
    assert [finding.render() for finding in check_case_file(path)] == []


def _catalogue_facts() -> dict[int, CatalogueFacts]:
    catalogue_module = pytest.importorskip("sqpack.kingbird_catalogue")
    return {
        n: facts_from_catalogue_entry(entry, n=n)
        for n, entry in catalogue_module.parse_catalogue().items()
    }


def _regenerate_in_range(n: int) -> str:
    """Draft a case past the hand-authored range, on the register's own review date."""
    return generate_record(
        n,
        availability=load_availability(),
        catalogue=_catalogue_facts(),
        review_date="2026-09-07",
        retrieved_date="2026-09-07",
    )


def _evidence() -> dict[str, Any]:
    return {
        record["id"]: record
        for record in safe_load((FRONTIER / "evidence.yaml").read_text(encoding="utf-8"))[
            "evidence"
        ]
    }


#: The one finding the register's own evidence still produces above `n = 100`, and the
#: only reason a generated case is allowed to report anything at all.
#: `E-basic-area-lower` was left scoped `1..100` when the other three widened to 324, so
#: the eight perfect squares in range cite a record that does not reach them. Tolerated
#: rather than asserted: this passes both before and after that scope moves.
AREA_LOWER_SCOPE_GAP = "evidence E-basic-area-lower does not cover"


def test_generated_cases_past_the_register_validate(tmp_path: Path) -> None:
    """A sample of the new range, over all three source branches and both statuses."""
    availability = load_availability()
    catalogue = _catalogue_facts()
    evidence = _evidence()
    shutil.copy(SCHEMA, tmp_path / SCHEMA.name)
    for n in (101, 105, 111, 119, 121, 123, 179, 324):
        path = record_path(tmp_path, n)
        write_record(
            generate_record(
                n,
                availability=availability,
                catalogue=catalogue,
                review_date="2026-09-07",
                retrieved_date="2026-09-07",
            ),
            path,
        )
        assert validate_schemas.check(path) == [], n
        payload = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
        assert check_case_basic_bounds(payload) == [], n
        assert [finding.render() for finding in check_case_file(path)] == [], n
        # The three evidence records the generator leans on are scoped to 324 now, so a
        # generated case has to satisfy the cross-record checks the register enforces --
        # every one of them but the area-bound scope named above.
        findings = check_case_semantics(payload, evidence)
        remaining = [error for error in findings if AREA_LOWER_SCOPE_GAP not in error]
        assert remaining == [], (n, findings)
        if findings:
            print(f"n={n}: still open on the evidence side -- {findings}")
        assert payload["rigidity"] is None


def test_the_new_range_proves_exactly_the_twenty_four_cases_the_plan_names() -> None:
    """`k^2`, `k^2 - 1` and `k^2 - 2` for `k = 11..18`, and nothing else in 101..324."""
    availability = load_availability()
    catalogue = _catalogue_facts()
    proved: list[int] = []
    for n in sorted(availability):
        text = generate_record(
            n,
            availability=availability,
            catalogue=catalogue,
            review_date="2026-09-07",
            retrieved_date="2026-09-07",
        )
        payload = safe_load(text.split("---\n")[1])["packing"]
        if payload["status"] == "proved":
            proved.append(n)
    expected = sorted(
        n for k in range(11, 19) for n in (k * k, k * k - 1, k * k - 2) if 101 <= n <= 324
    )
    print(f"proved in 101..324: {proved}")
    assert proved == expected
    assert len(proved) == 24


def test_an_unpictured_grid_case_cites_whichever_kingbird_item_covers_it() -> None:
    """The register below 100, the completeness statement above it, and never both.

    The two items divide the catalogue between them: `E-kingbird-upper-register` is its
    pictured entries, and above 100 its own `limitations` field says so;
    `E-kingbird-grid-completeness` is its statement about the ones it does not picture,
    scoped `101..324`. An unpictured grid case cites the one that reaches it.
    """
    availability = load_availability()
    for n in (111, 121, 324):
        payload = safe_load(
            generate_record(
                n,
                availability=availability,
                catalogue=None,
                review_date="2026-09-07",
                retrieved_date="2026-09-07",
            ).split("---\n")[1]
        )["packing"]
        reported = payload["reported_upper_bound"]
        assert reported["catalogue_pictured"] is False, n
        assert reported["evidence"] == [GRID_COMPLETENESS_EVIDENCE], n
        assert KINGBIRD_EVIDENCE not in payload["evidence"], n
        assert payload["evidence"][0] == GRID_COMPLETENESS_EVIDENCE, n

    # The hand-written unpictured grid cases keep citing the register, which is what the
    # byte-identical golden above already holds; asserted here so the rule reads whole.
    for n in (91, 100):
        committed, _ = _committed(n)
        assert committed["packing"]["reported_upper_bound"]["evidence"] == [KINGBIRD_EVIDENCE]


def test_a_unitsquare_case_takes_its_bound_and_its_blocker_from_the_release() -> None:
    """The four cases in `101..324` the release serves, built like `n = 68` and `n = 69`."""
    availability = load_availability()
    catalogue = _catalogue_facts()
    release = load_unitsquare_release()
    for n in (103, 105, 110, 131):
        assert availability[n].is_unitsquare, n
        payload = safe_load(
            generate_record(
                n,
                availability=availability,
                catalogue=catalogue,
                review_date="2026-09-07",
                retrieved_date="2026-09-07",
            ).split("---\n")[1]
        )["packing"]
        reported = payload["reported_upper_bound"]
        assert reported["value"] == release[n].offered_side, n
        assert reported["source_key"] == UNITSQUARE_SOURCE_KEY, n
        assert reported["source_date"] == "2026-07-29", n
        assert reported["found_by"] == ["UnitSquare Project"], n
        assert reported["found_year"] == 2026, n
        assert reported["evidence"] == [UNITSQUARE_EVIDENCE], n
        assert reported["analytically_optimized"] is False, n
        assert reported["construction_method"] == "unknown", n
        assert reported["witnesses"] == [f"W-known-best-n{n:03d}"], n
        # A release that publishes no certificate blocks on evidence, not on mathematics.
        assert all(blocker["kind"] == "source-evidence" for blocker in payload["blockers"]), n
        assert payload["blockers"][0]["evidence"] is reported["evidence"], n
        if n == 103:
            assert payload["blockers"][1]["evidence"] == ["E-green-ds7-theorem9-reported-lower"]
        else:
            assert len(payload["blockers"]) == 1
        assert payload["conjectured_optimum"] is None, n
        assert [resource["key"] for resource in payload["resources"]] == [
            "[Kingbird]",
            UNITSQUARE_SOURCE_KEY,
            "[Nagamochi 2005]",
            "[Friedman DS7]",
        ], n
        assert payload["evidence"][0] == UNITSQUARE_EVIDENCE, n


def test_the_unitsquare_prose_names_the_parent_the_release_improved_on() -> None:
    """The one sentence of that paragraph the release itself does not carry."""
    assert credited_surnames(_parsed_facts(68).credit_line) == (
        "Brendberg",
        "Schadt",
        "Ellsworth",
    )
    assert credited_surnames(_parsed_facts(69).credit_line) == ("Morandi", "Cantrell")
    # Compared with the wrapping collapsed: the formatter breaks lines where it likes.
    body = re.sub(r"\s+", " ", _regenerate(68).split("---\n", 2)[2])
    assert (
        "The UnitSquare Project’s 29 July 2026 release improves the public "  # noqa: RUF001
        "Brendberg-Schadt-Ellsworth parent by `0.0000768618004216131`." in body
    )


@pytest.mark.parametrize(
    ("phrase", "expected"),
    [
        ("[Explore group](squares_in_squares__Göbel_strips.html)", "diagonal-strip"),
        ("[Explore group](squares_in_squares__Göbel_squares.html)", "hand-construction"),
        ("simulated annealing", "simulated-annealing"),
        ("Extends the", "extension"),
        ("Unextends the", "extension"),
    ],
)
def test_each_credit_phrase_maps_to_the_enum_the_transcription_used(
    phrase: str, expected: str
) -> None:
    """One case per substring row of the table in the generator's docstring."""
    assert construction_method_from_credit(f"Found by A. Name in 1979. {phrase}") == expected


@pytest.mark.parametrize(
    ("credit", "expected"),
    [
        ('Adds two "L"s to the $s(65)$ found by A. Name in early 1979.', "extension"),
        ('Adds an "L" to the $s(148)$ that continues a pattern.', "extension"),
        ("Combines two copies of the $s(65)$ that continues a pattern.", "composition"),
        (
            "Found by A. Name in December 2025, by combining two copies of the $s(50)$.",
            "composition",
        ),
        # The n = 82 shape: the page names a human finder first and adds the augmentation
        # afterwards, so the opening-sentence rule does not reach it and the hand record's
        # `hand-construction` stands.
        ('Found by Frits Göbel in early 1979. Adds two "L"s to $s(65)$.', "unknown"),
    ],
)
def test_the_two_structural_rules_read_only_the_opening_sentence(
    credit: str, expected: str
) -> None:
    """The opening sentence is the one describing the packing the entry is about."""
    assert construction_method_from_credit(credit) == expected


def test_a_method_named_inside_a_parenthesis_belongs_to_the_ancestor() -> None:
    """`n = 171` and `n = 198`, the two entries whose only annealing is two packings up."""
    catalogue = _catalogue_facts()
    assert catalogue[171].construction_method == "composition"
    assert catalogue[198].construction_method == "extension"
    assert "simulated annealing program" in (catalogue[171].credit_line or "")
    assert "simulated annealing program" in (catalogue[198].credit_line or "")
    # And the scoping takes nothing else with it: the other in-range matches stand in a
    # finder's or a dated improver's own sentence.
    annealed = sorted(
        n
        for n, facts in catalogue.items()
        if n > 100 and facts.construction_method == "simulated-annealing"
    )
    print(f"simulated-annealing in range: {len(annealed)}")
    assert len(annealed) == 34


def test_the_improvement_rule_reproduces_the_hand_transcription() -> None:
    """Measured over every catalogue-sourced pictured record below the register.

    The rule reads a sentence-initial, dated "Improved by <names> in <month> <year>" and
    nothing else. It reproduces 45 of the 46 records; the miss is `n = 29`, where the
    hand pass read an "Optimized by" sentence as an improvement and five sibling records
    read the same sentence as nothing.
    """
    catalogue = _catalogue_facts()
    disagreed: dict[int, tuple[list[str], list[str]]] = {}
    compared = 0
    for n in range(1, 101):
        facts = catalogue.get(n)
        committed, _ = _committed(n)
        reported = committed["packing"]["reported_upper_bound"]
        if facts is None or reported["source_key"] != "[Kingbird]":
            continue
        if not reported["catalogue_pictured"]:
            continue
        compared += 1
        if list(facts.improved_by) != list(reported["improved_by"]):
            disagreed[n] = (list(reported["improved_by"]), list(facts.improved_by))
    print(f"compared {compared} record(s); the rule disagrees at {sorted(disagreed)}")
    assert compared == 46
    assert set(disagreed) == {29}


def test_an_entry_with_two_lineages_credits_the_packing_the_decimal_is_of() -> None:
    """The pictured alternative takes its own finder; the conversion names nobody."""
    catalogue = _catalogue_facts()
    for n, finder, year in ((170, "Károly Hajba", 2024), (257, "David Ellsworth", 2025)):
        facts = catalogue[n]
        assert list(facts.found_by) == [finder], n
        assert facts.found_year == year, n
        assert [note.claimed_by for note in facts.priority_notes] == [("Frits Göbel",)], n
    for n, original, year in ((240, "Károly Hajba", 2015), (272, "Lars Cleemann", None)):
        facts = catalogue[n]
        assert facts.found_by == (), n
        assert facts.found_year is None, n
        assert [note.claimed_by for note in facts.priority_notes] == [(original,)], n
        assert [note.year for note in facts.priority_notes] == [year], n
    # And nowhere else: five entries in range carry a second lineage, and no others.
    carried = sorted(n for n, facts in catalogue.items() if facts.priority_notes)
    assert carried == [170, 240, 257, 260, 272]


def test_a_pending_improvement_leaves_analytic_optimization_unstated() -> None:
    """`D-354`: a page that says it is still moving has not said this side is finished."""
    catalogue = _catalogue_facts()
    unstated = sorted(
        n for n, facts in catalogue.items() if facts.analytically_optimized is None
    )
    assert unstated == [102, 130, 172, 199, 228, 259, 269, 292, 302]
    # `n = 88`'s "Improvement by Thomas Schadt pending" is a different sentence.
    assert catalogue[88].analytically_optimized is True


def test_an_arslanov_credit_cites_the_retained_paper() -> None:
    """The seven entries the page credits to all three authors, and no others."""
    catalogue = _catalogue_facts()
    availability = load_availability()
    cited: list[int] = []
    for n in sorted(availability):
        facts = catalogue.get(n)
        if facts is None or availability[n].is_grid:
            continue
        payload = build_payload(
            n,
            source=availability[n],
            facts=facts,
            review_date="2026-09-07",
            retrieved_date="2026-09-07",
        )
        keys = [str(resource["key"]) for resource in payload["resources"]]
        if "[Arslanov et al.]" in keys:
            cited.append(n)
            assert keys[1] == "[Arslanov et al.]", n
            assert facts.found_year == 2019, n
    assert cited == [132, 156, 182, 210, 241, 273, 307]


def test_the_packing_paragraph_keeps_the_finder_and_the_method_apart() -> None:
    """The defect the template used to carry, at the case that showed it worst.

    `n = 132` was found by Arslanov, Mustafin and Shangitbayev in March 2019 and last
    improved by an annealing run in January 2026; the old single sentence credited the
    2019 construction with the 2026 method.
    """
    body = _regenerate_in_range(132).split("---\n", 2)[2]
    packing = re.sub(r"\s+", " ", body.split("## The packing\n\n")[1].split("\n\n## ")[0])
    assert packing == (
        "Found by M.Z. Arslanov, S.A. Mustafin and Z.K. Shangitbayev in 2019. "
        "Improved by David W. Cantrell in March 2025. "
        "Improved by David Ellsworth in January 2026, via simulated annealing."
    )
    # And where the method belongs to no credit at all, it is written with no owner.
    ownerless = re.sub(r"\s+", " ", _regenerate_in_range(301).split("---\n", 2)[2]).split(
        "## The packing "
    )[1]
    assert ownerless.startswith(
        "Found by David Ellsworth in 2025. The recorded construction method is "
        "simulated annealing."
    )


def test_an_unrecognised_credit_line_stays_unknown() -> None:
    """Including the shape that looks most like a hand construction and is not one.

    `n = 68`'s catalogue entry credits a person, names no method this table reads, and
    describes a computer search. Nothing here infers `hand-construction` from the absence
    of a keyword.
    """
    assert construction_method_from_credit(None) == "unknown"
    assert construction_method_from_credit("") == "unknown"
    assert (
        construction_method_from_credit(
            "Found by Sigvart Brendberg in June 2023, using a computer program he wrote "
            "followed by manual optimization."
        )
        == "unknown"
    )


def test_a_credit_phrase_broken_across_lines_still_reads() -> None:
    """The transcription wraps where the page wrapped, and a rule must not care."""
    assert (
        construction_method_from_credit(
            "Found by A. Name\nin 1979.\n[Explore group](squares_in_squares__Göbel_strips.html)"
        )
        == "diagonal-strip"
    )
    assert credited_surnames("Found by Maurizio Morandi\nin June 2010.") == ("Morandi",)


def test_the_credit_rules_reproduce_the_hand_transcription_below_the_register() -> None:
    """Measured, not asserted: wherever a rule fires below the register, it fires correctly.

    The comparison runs over the pictured entries at `n <= 100` that a person transcribed
    from the catalogue. Where a rule fires it must agree with what they wrote -- 22 cases,
    and no disagreement anywhere. Where none fires the case stays `unknown`, and those are
    reported rather than checked: a rule that fired there would be an invention, and the
    count is what a reviewer inherits.
    """
    catalogue = _catalogue_facts()
    fired: dict[int, tuple[str, str]] = {}
    silent: dict[int, str] = {}
    for n in range(1, 101):
        facts = catalogue.get(n)
        committed, _ = _committed(n)
        reported = committed["packing"]["reported_upper_bound"]
        if facts is None or reported["source_key"] != "[Kingbird]":
            continue
        if facts.construction_method == "unknown":
            silent[n] = str(reported["construction_method"])
            continue
        fired[n] = (str(reported["construction_method"]), facts.construction_method)
    disagreed = {n: pair for n, pair in fired.items() if pair[0] != pair[1]}
    print(f"rules fired at {len(fired)} case(s), silent at {len(silent)}: {sorted(silent)}")
    print(f"what the hand transcription called the silent ones: {sorted(set(silent.values()))}")
    assert disagreed == {}
    assert len(fired) == 22
    assert all(catalogue[n].analytically_optimized is True for n in fired)
    # Every case no rule reaches is one a person called `hand-construction`, `trivial-grid`
    # or `unknown` -- never one of the four methods the rules are for, which is what makes
    # `unknown` a gap in the table rather than a wrong answer from it.
    assert set(silent.values()) <= {"hand-construction", "trivial-grid", "unknown"}


def test_analytically_optimized_is_the_catalogues_own_disclaimer() -> None:
    """`false` where the page says so, `true` where it does not, `null` with no line."""
    assert analytically_optimized_from_credit("Not yet analytically optimized.") is False
    assert analytically_optimized_from_credit("Found by A. Name in 1979.") is True
    assert analytically_optimized_from_credit(None) is None

    catalogue = _catalogue_facts()
    stated = sorted(
        n for n, facts in catalogue.items() if facts.analytically_optimized is False
    )
    print(f"catalogue entries carrying the disclaimer: {len(stated)}")
    assert 179 in stated
    assert all(n > 100 for n in stated)


def test_a_stale_printed_form_is_dropped_and_typed_as_a_conflict() -> None:
    """`n = 179`: the page prints a form its own decimal contradicts, and says so by date.

    The catalogue's entry pairs a January-2025 closed form with a January-2026 decimal it
    does not equal. Recording the form would put a number in `exact_form` that no source
    currently claims, so the three algebraic fields go null and the disagreement is
    carried as a `stale-source` conflict quoting both printed values.
    """
    catalogue_module = pytest.importorskip("sqpack.kingbird_catalogue")
    entry = catalogue_module.parse_catalogue()[179]
    assert entry.exact_form == "(25/2) + sqrt(2)"
    assert not catalogue_module.exact_form_matches_decimal(entry)

    facts = facts_from_catalogue_entry(entry, n=179)
    assert facts.exact_form is None
    assert facts.stale_exact_form == "(25/2) + sqrt(2)"
    payload = safe_load(
        generate_record(
            179,
            availability=load_availability(),
            catalogue={179: facts},
            review_date="2026-09-07",
            retrieved_date="2026-09-07",
        ).split("---\n")[1]
    )["packing"]
    reported = payload["reported_upper_bound"]
    assert reported["value"] == entry.side_decimal
    assert reported["exact_form"] is None
    assert reported["algebraic_degree"] is None
    assert reported["minimal_polynomial"] is None
    conflicts = payload["conflicts"]
    assert [conflict["kind"] for conflict in conflicts] == ["stale-source"]
    assert "`(25/2) + sqrt(2)`" in conflicts[0]["detail"]
    assert f"`{entry.side_decimal}`" in conflicts[0]["detail"]
    assert conflicts[0]["evidence"] == [KINGBIRD_EVIDENCE]

    # Every other entry in range agrees with its own decimal, so 179 is the only conflict.
    catalogue = _catalogue_facts()
    stale = sorted(n for n, facts in catalogue.items() if facts.stale_exact_form is not None)
    assert stale == [179]


def test_the_summary_counts_the_methods_and_names_what_is_left_unknown() -> None:
    """A run says which cases it is handing a reviewer, rather than burying them."""
    availability = load_availability()
    catalogue = _catalogue_facts()
    lines = method_summary(sorted(availability), availability, catalogue)
    print("\n".join(lines))
    counts = {
        line.removeprefix("construction_method ").split(": ")[0]: int(line.rsplit(": ", 1)[1])
        for line in lines
        if line.startswith("construction_method ")
    }
    assert sum(counts.values()) == 224
    assert counts["trivial-grid"] == 97
    assert counts["unknown"] == 49
    # The L-augmentation family and the two "Combines two copies" entries, which used to
    # land in the unknown roll and now have rules of their own.
    assert counts["extension"] == 27
    assert counts["composition"] == 3
    unresolved = next(line for line in lines if line.startswith("unresolved "))
    assert "101" not in unresolved
    assert "103" in unresolved


def test_reported_green_bound_preserves_the_verified_nagamochi_precision() -> None:
    """The source lane can improve without changing the certified theorem's digits."""
    payload = safe_load(_regenerate(50).split("---\n")[1])["packing"]
    assert payload["reported_lower_bound"]["value"] == "7.317426011159"
    assert payload["reported_lower_bound"]["evidence"] == [
        "E-green-ds7-theorem9-reported-lower"
    ]
    assert payload["verified_lower_bound"]["value"] == "7.0827625303"
    assert (
        payload["verified_lower_bound"]["exact_form"] == "sqrt(50 - 2*floor(sqrt(50)) + 1) + 1"
    )


def test_the_verified_upper_bound_is_the_grid_ceiling_and_says_so() -> None:
    """`verified_upper_bound` is `ceil(sqrt(n))`, never a reading of the reported side."""
    availability = load_availability()
    for n in (111, 121, 324):
        payload = safe_load(
            generate_record(
                n,
                availability=availability,
                catalogue=None,
                review_date="2026-09-07",
                retrieved_date="2026-09-07",
            ).split("---\n")[1]
        )["packing"]
        side = math.isqrt(n) if math.isqrt(n) ** 2 == n else math.isqrt(n) + 1
        assert payload["verified_upper_bound"] == {
            "value": str(side),
            "exact_form": str(side),
            "evidence": ["E-basic-grid-upper"],
        }


def test_refuses_to_touch_the_hand_authored_range_or_overwrite_a_record(
    tmp_path: Path,
) -> None:
    assert refuse_reason(50, FRONTIER, force=False) is not None
    assert "hand-authored" in str(refuse_reason(50, FRONTIER, force=False))
    # The same n is allowed into a scratch directory, which is what the golden test needs.
    assert refuse_reason(50, tmp_path, force=False) is None
    assert refuse_reason(325, tmp_path, force=False) is not None

    target = record_path(tmp_path, 111)
    target.write_text("placeholder\n", encoding="utf-8")
    assert refuse_reason(111, tmp_path, force=False) is not None
    assert refuse_reason(111, tmp_path, force=True) is None


def test_a_catalogue_case_without_facts_refuses_rather_than_guesses() -> None:
    with pytest.raises(GenerationError):
        generate_record(
            101,
            availability=load_availability(),
            catalogue=None,
            review_date="2026-09-07",
            retrieved_date="2026-09-07",
        )
    with pytest.raises(GenerationError):
        generate_record(
            999,
            availability=load_availability(),
            catalogue=None,
            review_date="2026-09-07",
            retrieved_date="2026-09-07",
        )


def test_the_cli_writes_a_range_and_then_checks_it(tmp_path: Path) -> None:
    out = str(tmp_path)
    assert main(["--range", "111", "118", "--out", out, "--review-date", "2026-09-07"]) == 0
    assert sorted(path.name for path in tmp_path.glob("n-*.md")) == [
        f"n-{n}.md" for n in range(111, 119)
    ]
    # A second write refuses, and --check on what was written reports no drift even
    # though today's default review date is not the one the records carry.
    assert main(["--n", "111", "--out", out]) == 1
    assert main(["--range", "111", "118", "--out", out, "--check"]) == 0

    edited = record_path(tmp_path, 112)
    edited.write_text(
        edited.read_text(encoding="utf-8").replace("conjectured_optimum: integer", ""),
        encoding="utf-8",
    )
    assert main(["--range", "111", "118", "--out", out, "--check"]) == 1


def test_the_module_runs_as_a_devtool() -> None:
    """The documented invocation is the one that works."""
    completed = subprocess.run(
        [sys.executable, "-m", "devtools.generate_frontier_case", "--n", "50"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 1
    assert "hand-authored" in completed.stdout


def test_a_pictured_integer_side_case_is_recorded_as_the_trivial_grid() -> None:
    """ "119, 120 ... s = 11, Proved by Nagamochi" is a grid the catalogue pictures for its
    proof credit. The register records such cases as `n = 47, 48, 98, 99` are recorded:
    trivial grid, nobody credited, not pictured, the register item as evidence."""
    catalogue = pytest.importorskip("sqpack.kingbird_catalogue")
    entries = catalogue.parse_catalogue()
    facts = {n: facts_from_catalogue_entry(entries[n], n=n) for n in (119, 120, 142)}
    availability = load_availability()
    for n in (119, 120, 142):
        text = generate_record(
            n,
            availability=availability,
            catalogue=facts,
            review_date="2026-09-07",
            retrieved_date="2026-09-07",
        )
        payload = safe_load(text.split("---\n")[1])["packing"]
        upper = payload["reported_upper_bound"]
        assert upper["construction_method"] == "trivial-grid"
        assert upper["found_by"] == []
        assert upper["found_year"] is None
        assert upper["catalogue_pictured"] is False
        assert upper["analytically_optimized"] is None
        assert upper["evidence"] == ["E-kingbird-upper-register"]
        assert payload["status"] == "proved"
