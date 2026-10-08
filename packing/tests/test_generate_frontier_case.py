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
- `n = 68` and `n = 69` -- open, and once both sourced from the UnitSquare release rather
  than the catalogue: a forty-five figure reported side, a `source-evidence` blocker
  instead of a `mathematics` one, a fourth resource, and a null `conjectured_optimum`.
  `n = 103, 105, 110` and `131` are generated from the same branch. Since the #227 intake
  Couzo's certified packing holds `n = 68`'s upper lane, which
  `devtools.apply_upper_bound_packets` writes over the release draft, so `n = 68` is
  regenerated as that draft with the intake applied. Since 2026-10-05 `n = 69` reports the
  catalogue's side for David Ellsworth's optimization of the release's packing (T-088), so
  it is regenerated from the catalogue branch, with an `n <= 100` record's degree lock and
  polynomial, and its lower-bound promotion carried as everywhere else; its verified upper
  lane and blocker are the exact certificate's, which `devtools.catalogue_upper_bounds`
  writes over the draft as the packet intake does at `n = 68`.

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

import argparse
import functools
import math
import re
import shutil
import subprocess
import sys
from collections.abc import Mapping
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
import yaml

from devtools import source_supersession, validate_schemas
from devtools import squish_followup_packets as update
from devtools import squish_second_update_packets as second
from devtools.apply_upper_bound_packets import PREVIOUS_HEADING, earlier_reports, normalized
from devtools.backfill_algebraic_facts import backfilled
from devtools.check_basic_bounds import check_case_basic_bounds
from devtools.check_case_prose import check_case_file
from devtools.check_source_coverage import COVERAGE, pending_intake_blocker, record_catalogue
from devtools.generate_frontier_case import (
    AI_STATEMENT,
    CATALOGUE_CLASSIFICATION,
    GRID_CLASSIFICATION,
    GRID_COMPLETENESS_EVIDENCE,
    KINGBIRD_EVIDENCE,
    UNITSQUARE_AVAILABILITY_KEY,
    UNITSQUARE_EVIDENCE,
    UNITSQUARE_SOURCE_KEY,
    CatalogueFacts,
    GenerationError,
    LowerBoundPromotion,
    PreservedListItem,
    SourceAvailability,
    adopt_upper_bound_packet,
    ai_statements_from_credit,
    analytically_optimized_from_credit,
    build_payload,
    check_records,
    construction_method_from_credit,
    credited_surnames,
    drafting_capture,
    facts_from_catalogue_entry,
    generate_record,
    grid_ceiling,
    load_availability,
    load_catalogue,
    load_drafting_catalogue,
    load_unitsquare_release,
    lower_bound_promotion_from_records,
    main,
    method_summary,
    packet_adopted_counts,
    record_path,
    redraft,
    refresh_records,
    refuse_reason,
    render_record,
    with_rigidity_of,
    without_rigidity,
    write_record,
)
from sqpack.assurance import check_case_semantics
from sqpack.exact_values import CATALOGUE as CATALOGUE_SOURCE
from sqpack.exact_values import DERIVED_FROM_EXACT_FORM, format_polynomial
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
        "the lower-bound prose: wand125's two intake paragraphs, and the n68 floor deduced "
        "from wand125's n69 certificate, in place of the Nagamochi opener and section; the "
        "packing section, which the #227 intake writes over the release draft, reproduces"
    ),
    69: (
        "the 2026-10-05 catalogue intake (T-088), which names the release it overtook and "
        "keeps the release's paragraph as the previous best known packing, and wand125's "
        "lower-bound intake paragraphs"
    ),
    50: (
        "the 2026-09-28 intake of wand125's reported 37/5, whose replay was still running, "
        "and the history of Green's DS7 report it displaced from the reported lane"
    ),
}

#: How the source map would classify a record the register already carries.
GRID = "grid"
CATALOGUE = "catalogue"
UNITSQUARE = "unitsquare"


def _source_kind(payload: Mapping[str, Any]) -> str:
    n = int(payload["n"])
    if n in packet_adopted_counts():
        # A certified packet's intake writes over the draft of the report it replaced, and
        # names that report: the release's where the release had this count.
        return UNITSQUARE if "unitsquare" in earlier_reports()[n] else CATALOGUE
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
    """The catalogue entry for `n` as the parser reads it, from the capture `n` drafts from."""
    catalogue = pytest.importorskip("sqpack.kingbird_catalogue")
    kind = _source_kind(_committed(n)[0]["packing"])
    source = _availability(n, kind)
    return facts_from_catalogue_entry(
        catalogue.parse_catalogue(drafting_capture(n, source))[n], n=n
    )


@functools.cache
def _pre_ryxu_records() -> dict[int, dict[str, Any]]:
    """Complete retained originals for tests of sources displaced by later imports."""
    from devtools import register_gupta_reports as gupta  # noqa: PLC0415
    from devtools.register_ryxu_reports import read_history  # noqa: PLC0415

    rows = {row["n"]: row for row in read_history()}
    if gupta.HISTORY.exists():
        for row in gupta.read_history():
            rows.setdefault(row["n"], row)
    return rows


def _before_ryxu(n: int, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> str:
    history = _pre_ryxu_records()
    if n not in history:
        return record_path(FRONTIER, n).read_text()
    original = history[n]["frontier"]
    key = safe_load(original.split("---\n", 2)[1])["packing"]["reported_upper_bound"][
        "source_key"
    ]
    coverage = safe_load(source_supersession.COVERAGE.read_text())
    source = next(row for row in coverage["sources"] if row["source_key"] == key)
    selected = next(row for row in coverage["selected_overrides"] if row["n"] == n)
    selected["source_id"] = source["id"]
    historical_coverage = tmp_path / "historical-source-selection.yaml"
    historical_coverage.write_text(yaml.safe_dump(coverage, sort_keys=False))
    monkeypatch.setattr(source_supersession, "COVERAGE", historical_coverage)
    if n == 105:
        from devtools import refinement_house_links as houses  # noqa: PLC0415

        custody = tmp_path / "historical-refinement"
        custody.mkdir()
        house_path = custody / "n-105.yaml"
        house_path.write_text(history[n]["house"])
        metadata = custody / houses.METADATA.name
        metadata.write_bytes(houses.METADATA.read_bytes())
        monkeypatch.setattr(houses, "REPO", tmp_path)
        monkeypatch.setattr(houses, "METADATA", metadata)
        monkeypatch.setattr(houses, "house_path", lambda _n: house_path)
    return original


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
    # The catalogue prints a degree and polynomial only where the record says it did; a
    # derived pair is the generator's own to compute from the closed form.
    printed = reported.get("algebraic_source") == CATALOGUE_SOURCE
    return CatalogueFacts(
        n=n,
        side_decimal=str(reported["value"]),
        exact_form=reported["exact_form"],
        algebraic_degree=reported["algebraic_degree"] if printed else None,
        minimal_polynomial=reported["minimal_polynomial"] if printed else None,
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
    arguments = {
        "availability": {n: _availability(n, kind)},
        "catalogue": None if facts is None else {n: facts},
        "review_date": str(payload["source_reviewed"]),
        "retrieved_date": str(payload["reported_upper_bound"]["retrieved_date"]),
    }
    generated = generate_record(n, **arguments)
    generated_payload = safe_load(generated.split("---\n", 2)[1])["packing"]
    promotion = lower_bound_promotion_from_records(payload, generated_payload)
    drafted = generate_record(n, **arguments, lower_bound_promotion=promotion)
    historical = adopt_upper_bound_packet(n, drafted)
    existing = (FRONTIER / f"n-{n:03d}.md").read_text()
    return source_supersession.adopt_selected_report(n, existing, historical)


PROMOTED_LOWER_CASES = (
    11,
    17,
    26,
    27,
    28,
    29,
    30,
    31,
    39,
    40,
    41,
    52,
    53,
    55,
    56,
    68,
    69,
    70,
    71,
    72,
)


@pytest.mark.parametrize("n", PROMOTED_LOWER_CASES)
def test_preserves_reviewed_lower_bound_promotions_as_case_bound_deltas(n: int) -> None:
    """Reviewed enrichment survives without treating copied fields as a derivation."""
    document, _ = _committed(n)
    reviewed = document["packing"]
    kind = _source_kind(reviewed)
    facts = None if kind == GRID else _injected_facts(n)
    arguments = {
        "availability": {n: _availability(n, kind)},
        "catalogue": None if facts is None else {n: facts},
        "review_date": str(reviewed["source_reviewed"]),
        "retrieved_date": str(reviewed["reported_upper_bound"]["retrieved_date"]),
    }
    baseline = safe_load(generate_record(n, **arguments).split("---\n", 2)[1])["packing"]
    promotion = lower_bound_promotion_from_records(reviewed, baseline)
    assert promotion is not None
    assert promotion.source_n == n

    preserved = safe_load(
        generate_record(n, **arguments, lower_bound_promotion=promotion).split("---\n", 2)[1]
    )["packing"]
    assert preserved["reported_lower_bound"] == reviewed["reported_lower_bound"]
    assert preserved["verified_lower_bound"] == reviewed["verified_lower_bound"]
    for addition in promotion.evidence_additions:
        assert preserved["evidence"][addition.index] == addition.value
    for addition in promotion.resource_additions:
        assert preserved["resources"][addition.index] == addition.value


def test_a_lower_bound_promotion_cannot_move_to_another_case() -> None:
    promotion = LowerBoundPromotion(
        source_n=68,
        reported_lower_bound=None,
        verified_lower_bound={
            "value": "8.41",
            "exact_form": "841/100",
            "evidence": ["E-wand125-n068-derived-lower"],
        },
        evidence_additions=(),
        resource_additions=(),
    )
    with pytest.raises(GenerationError, match="for n=68 cannot be applied to n=69"):
        generate_record(
            69,
            availability={69: _availability(69, UNITSQUARE)},
            catalogue={69: _injected_facts(69)},
            review_date="2026-09-22",
            retrieved_date="2026-09-22",
            lower_bound_promotion=promotion,
        )


def test_a_changed_value_without_new_lower_evidence_is_drift() -> None:
    """A Nagamochi typo is not converted into a preserved editorial promotion."""
    n = 111
    text = generate_record(
        n,
        availability=load_availability(),
        catalogue=None,
        review_date="2026-09-07",
        retrieved_date="2026-09-07",
    )
    generated = safe_load(text.split("---\n", 2)[1])["packing"]
    reviewed = dict(generated)
    reviewed["verified_lower_bound"] = {
        **generated["verified_lower_bound"],
        "value": "10.5",
    }
    assert lower_bound_promotion_from_records(reviewed, generated) is None


def test_check_preserves_a_promotion_but_catches_generator_owned_drift(tmp_path: Path) -> None:
    """Editorial lower-bound evidence survives; a changed upper bound still fails check."""
    n = 111
    availability = load_availability()
    arguments = {
        "availability": availability,
        "catalogue": None,
        "review_date": "2026-09-07",
        "retrieved_date": "2026-09-07",
    }
    baseline = safe_load(generate_record(n, **arguments).split("---\n", 2)[1])["packing"]
    verified = dict(baseline["verified_lower_bound"])
    verified["evidence"] = ["E-reviewed-lower-promotion"]
    promotion = LowerBoundPromotion(
        source_n=n,
        reported_lower_bound=None,
        verified_lower_bound=verified,
        evidence_additions=(PreservedListItem(index=0, value="E-reviewed-lower-promotion"),),
        resource_additions=(
            PreservedListItem(
                index=0,
                value={
                    "key": "[reviewed lower promotion]",
                    "role": "lower-bound-proof",
                    "local": "web/reviewed-lower-promotion",
                    "url": "https://example.com/reviewed-lower-promotion",
                    "retrieved": True,
                },
            ),
        ),
    )
    path = record_path(tmp_path, n)
    write_record(generate_record(n, **arguments, lower_bound_promotion=promotion), path)
    check_args = argparse.Namespace(
        out=tmp_path,
        review_date="2026-09-22",
        retrieved_date="2026-09-22",
    )
    assert check_records([n], check_args, availability, None) == 0

    path.write_text(
        path.read_text(encoding="utf-8").replace("value: '11.0'", "value: '11.1'", 1),
        encoding="utf-8",
    )
    assert check_records([n], check_args, availability, None) == 1

    baseline_payload = safe_load(generate_record(n, **arguments).split("---\n", 2)[1])[
        "packing"
    ]
    write_record(render_record(baseline_payload), path)
    assert check_records([n], check_args, availability, None) == 0
    baseline_payload["verified_lower_bound"]["value"] = "10.5"
    write_record(render_record(baseline_payload), path)
    assert check_records([n], check_args, availability, None) == 1


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
    # A blocker declaring a pending catalogue intake is the coverage register's to add and
    # remove (`check_source_coverage.pending_intake_errors`), never a draft's: `n = 69`
    # carries one while David Ellsworth's September 2026 side waits to be registered.
    packing = committed_document["packing"]
    packing["blockers"] = [
        blocker
        for blocker in packing.get("blockers", [])
        if pending_intake_blocker({"blockers": [blocker]}) is None
    ]
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


@pytest.mark.parametrize("n", [68, 105, 292])
def test_refinement_redraft_repairs_both_ceilings_from_complete_admitted_inputs(
    n: int, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    existing = _before_ryxu(n, monkeypatch, tmp_path)
    _, front, body = existing.split("---\n", 2)
    document = safe_load(front)
    expected = document["packing"]
    report = expected["reported_upper_bound"].copy()
    verified = expected["verified_upper_bound"].copy()
    expected["reported_upper_bound"].update(value="99", exact_form="99/1")
    expected["verified_upper_bound"].update(value="98", exact_form="98/1")
    body, count = re.subn(
        r"(at exact side\s+)\$[0-9]+/[0-9]+\$(,\s+whose complete terminating decimal is\s+)"
        r"\$[0-9.]+\$",
        lambda match: f"{match[1]}$99/1${match[2]}$99$",
        body,
    )
    assert count == 1
    edited = "---\n" + yaml.safe_dump(document, sort_keys=False) + "---\n" + body
    restored = source_supersession.adopt_selected_report(n, edited, existing)
    actual = safe_load(restored.split("---\n", 2)[1])["packing"]
    assert actual["reported_upper_bound"] == report
    assert actual["verified_upper_bound"] == verified
    assert f"${report['exact_form']}$" in restored
    assert actual["status"] == "open"
    assert actual["rigidity"] is None


@pytest.mark.parametrize("n", [68, 105, 292])
def test_refinement_redraft_refuses_unmapped_confirmation(
    n: int, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    existing = _before_ryxu(n, monkeypatch, tmp_path)
    _, front, body = existing.split("---\n", 2)
    document = safe_load(front)
    document["packing"]["verified_upper_bound"]["evidence"] = ["E-unreviewed-promotion"]
    edited = "---\n" + yaml.safe_dump(document, sort_keys=False) + "---\n" + body
    with pytest.raises(ValueError, match="lacks its complete confirming evidence"):
        source_supersession.adopt_selected_report(n, edited, existing)


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


def _record_facts() -> dict[int, CatalogueFacts]:
    """What each record transcribes: the current capture, or at a count pending intake the
    capture of 2026-08-22, exactly as `check_source_coverage` reconciles them."""
    catalogue_module = pytest.importorskip("sqpack.kingbird_catalogue")
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))
    pending = coverage.get("pending_catalogue_intake", [])
    entries = record_catalogue(catalogue_module.parse_catalogue(), pending)
    return {n: facts_from_catalogue_entry(entry, n=n) for n, entry in entries.items()}


def _regenerate_in_range(n: int) -> str:
    """Draft a case past the hand-authored range, from the capture the register reads."""
    availability = load_availability()
    return generate_record(
        n,
        availability=availability,
        catalogue=load_drafting_catalogue([n], availability),
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
            "[Karakuş 2026]",
        ], n
        assert payload["evidence"][0] == UNITSQUARE_EVIDENCE, n


def test_the_unitsquare_prose_names_the_parent_the_release_improved_on() -> None:
    """The one sentence of that paragraph the release itself does not carry.

    Since the #227 intake that paragraph describes `n = 68`'s previous best known packing:
    Couzo's certified packing replaced the release's, and the intake keeps the release
    draft's paragraph under its own heading, in the regeneration and the record alike.
    """
    assert credited_surnames(_parsed_facts(68).credit_line) == (
        "Brendberg",
        "Schadt",
        "Ellsworth",
    )
    # n = 69 reports the catalogue since its 2026-10-05 intake (T-088); the release's
    # paragraph stays as its previous best known packing, still naming the parent the
    # capture of 2026-08-22 credits.
    catalogue = pytest.importorskip("sqpack.kingbird_catalogue")
    earlier = catalogue.parse_catalogue(drafting_capture(69, _availability(69, UNITSQUARE)))
    assert credited_surnames(facts_from_catalogue_entry(earlier[69], n=69).credit_line) == (
        "Morandi",
        "Cantrell",
    )
    assert "Morandi-Cantrell parent" in re.sub(r"\s+", " ", _committed(69)[1])
    sentence = (
        "The UnitSquare Project’s 29 July 2026 release improves the public "  # noqa: RUF001
        "Brendberg-Schadt-Ellsworth parent by $0.0000768618004216131$."
    )
    for text in (_regenerate(68).split("---\n", 2)[2], _committed(68)[1]):
        # Compared with the wrapping collapsed: the formatter breaks lines where it likes.
        body = re.sub(r"\s+", " ", text)
        assert sentence in body[body.index(PREVIOUS_HEADING) :]


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

    The rule reads a sentence-initial, dated "Improved by <names> in <month> <year>", or
    "Improved and optimized by", and nothing else. It reproduces 39 of the 42 currently
    selected catalogue records; the other pictured records have later selected sources. One
    miss is `n = 29`, where the hand pass read an "Optimized by" sentence as an
    improvement and five sibling records read the same sentence as nothing; the other two
    are `n = 69` and `83`, whose records were transcribed on 2026-10-05 from drafts, which
    also credit the optimizer the line names nowhere else (T-088, T-089).
    """
    catalogue = _record_facts()
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
    assert compared == 42
    assert set(disagreed) == {29, 69, 83}
    for n in (69, 83):
        assert disagreed[n][0] == [*disagreed[n][1], *catalogue[n].uncredited_optimizers], n


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
    # `n = 102` left the list on 2026-09-30: the page now prints Cantrell's January 2025
    # improvement that its "Further improvement pending" was waiting on.
    assert unstated == [130, 172, 199, 228, 259, 269, 292, 302]
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
    from the catalogue, and `n = 69`, transcribed from a draft since its 2026-10-05 intake
    (T-088). Where a rule fires it must agree with what they wrote -- 20 cases, and no
    disagreement anywhere. Where none fires the case stays `unknown`, and those are
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
    assert len(fired) == 20
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
    # n = 179 dropped it when it was optimized in June 2026, and n = 126 took it with its
    # August 2026 packing; below the register only n = 68's latest improvement carries it.
    assert 126 in stated
    assert 179 not in stated
    assert [n for n in stated if n <= 100] == [68]


def test_a_stale_printed_form_is_dropped_and_typed_as_a_conflict() -> None:
    """`n = 179`: the page prints a form its own decimal contradicts, and says so by date.

    The capture of 2026-08-22 pairs a January-2025 closed form with a January-2026 decimal
    it does not equal. Recording the form would put a number in `exact_form` that no
    source currently claims, so the three algebraic fields go null and the disagreement is
    carried as a `stale-source` conflict quoting both printed values. The capture of
    2026-09-30 prints a consistent root there, so the rule is exercised on the earlier one.
    """
    catalogue_module = pytest.importorskip("sqpack.kingbird_catalogue")
    entry = catalogue_module.parse_catalogue(catalogue_module.intake_catalogue_path())[179]
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

    # Every other entry agreed with its own decimal, so 179 was the only conflict; in the
    # current capture there is none.
    earlier = load_catalogue(catalogue_module.intake_catalogue_path())
    stale = sorted(n for n, facts in earlier.items() if facts.stale_exact_form is not None)
    assert stale == [179]
    catalogue = _catalogue_facts()
    assert [n for n, facts in catalogue.items() if facts.stale_exact_form is not None] == []


def test_a_count_an_intake_replaced_drafts_from_the_capture_the_intake_read() -> None:
    """What a record says the replaced packing was does not move with a new capture.

    `n = 155` is Couzo's (T-056) and keeps the 2026-08-22 catalogue entry as its previous
    best known packing; `n = 69` is the release's and names the parent the release
    improved on; `n = 126` is the catalogue's own and follows the current capture.
    """
    availability = load_availability()
    release = _availability(69, UNITSQUARE)
    assert drafting_capture(155, availability[155]) is not None
    assert drafting_capture(69, release) is not None
    assert drafting_capture(126, availability[126]) is None

    facts = load_drafting_catalogue([126, 155], availability)
    assert facts[155].side_decimal == "12.95851388606690"
    assert facts[126].side_decimal == "11.77473513240654"


def test_the_register_agrees_with_its_drafts_where_the_capture_moved() -> None:
    """The refreshed records, and a packet count whose catalogue entry moved, draft as held."""
    cases = [126, 155, 179]
    availability = load_availability()
    args = argparse.Namespace(out=FRONTIER, review_date="2026-09-30", retrieved_date=None)
    catalogue = load_drafting_catalogue(cases, availability)

    assert check_records(cases, args, availability, catalogue) == 0


def test_a_refresh_keeps_the_assessment_and_rewrites_only_what_moved(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The draft's `rigidity: null` would drop an assessed record out of the assessed set."""
    availability = load_availability()
    catalogue = load_drafting_catalogue([179], availability)
    committed = _before_ryxu(179, monkeypatch, tmp_path)
    report = safe_load(committed.split("---\n", 2)[1])["packing"]["reported_upper_bound"]
    stale = committed.replace(f"value: '{report['value']}'", "value: '99.0'", 1)
    assert stale != committed
    record_path(tmp_path, 179).write_text(stale, encoding="utf-8")
    args = argparse.Namespace(
        out=tmp_path, review_date="2026-09-30", retrieved_date="2026-09-30", force=False
    )

    assert refresh_records([179], args, availability, catalogue) == 0

    refreshed = record_path(tmp_path, 179).read_text(encoding="utf-8")
    # Since 2026-10-06 the count's verified upper lane is T-101's, a layer the formatter
    # reflows, so the refresh is compared as `check_records` compares an adopted count:
    # whitespace collapsed.
    assert normalized(refreshed) == normalized(committed)
    assert (
        safe_load(refreshed.split("---\n", 2)[1])["packing"]["rigidity"]
        == (safe_load(committed.split("---\n", 2)[1])["packing"]["rigidity"])
    )
    drafted = redraft(
        179,
        committed,
        availability=availability,
        catalogue=catalogue,
        review_date="2026-09-30",
        retrieved_date="2026-09-30",
    )
    assert "  rigidity: null\n" in drafted
    assert normalized(with_rigidity_of(committed, drafted)) == normalized(committed)


@pytest.mark.parametrize("n", [108, 126, 130, 153, 155])
def test_selected_squish_report_refreshes_geometry_and_lower_lanes_without_losing_review(
    n: int, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    availability = load_availability()
    catalogue = load_drafting_catalogue([n], availability)
    committed = _before_ryxu(n, monkeypatch, tmp_path)
    args = argparse.Namespace(
        out=tmp_path, review_date="2026-10-07", retrieved_date="2026-10-07", force=False
    )
    path = record_path(tmp_path, n)
    path.write_text(committed)
    assert check_records([n], args, availability, catalogue) == 0
    drafted = redraft(
        n,
        committed,
        availability=availability,
        catalogue=catalogue,
        review_date="2026-10-07",
        retrieved_date="2026-10-07",
    )
    assert "  rigidity: null\n" in drafted
    assert normalized(with_rigidity_of(committed, drafted)) == normalized(committed)


@pytest.mark.parametrize("n", [108, 126, 130, 153, 155])
def test_selected_squish_report_restores_stale_geometry_and_lower_lanes(
    n: int, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Refuse, repair and freshly admit each independently corrupted source record."""
    availability = load_availability()
    catalogue = load_drafting_catalogue([n], availability)
    committed = _before_ryxu(n, monkeypatch, tmp_path)
    payload = safe_load(committed.split("---\n", 2)[1])["packing"]
    args = argparse.Namespace(
        out=tmp_path, review_date="2026-10-07", retrieved_date="2026-10-07", force=False
    )
    path = record_path(tmp_path, n)
    # A stale display and fraction must not become a self-fulfilling draft. The body
    # declaration and the ordinary verified lower lane are independently regenerated.
    report = payload["reported_upper_bound"]
    stale = committed.replace(f"value: '{report['value']}'", "value: '99.0'", 1)
    stale = stale.replace(f"exact_form: {report['exact_form']}", "exact_form: 99/1", 1)
    stale = stale.replace("S_n = \\frac{", "S_n = \\frac{999", 1)
    lower = payload["verified_lower_bound"]["value"]
    stale = stale.replace(f"value: '{lower}'", "value: '1.0'", 1)
    path.write_text(stale)
    assert check_records([n], args, availability, catalogue) == 1
    assert refresh_records([n], args, availability, catalogue) == 0
    assert normalized(path.read_text()) == normalized(committed)
    assert check_records([n], args, availability, catalogue) == 0


def test_confirmed_squish_draft_rebuilds_and_requires_both_displays(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The confirmation phase has a ceiling and a separate original source quotation."""
    from fractions import Fraction  # noqa: PLC0415

    from yaml import safe_dump  # noqa: PLC0415

    from devtools import source_supersession, squish_upper_bound_packets  # noqa: PLC0415

    n = 130
    existing = _before_ryxu(n, monkeypatch, tmp_path)
    _, front, body = existing.split("---\n", 2)
    document = safe_load(front)
    case = document["packing"]
    case["verified_upper_bound"]["evidence"] = ["E-squish-ten-packings-2026-10-07-exact-replay"]
    case["reported_upper_bound"]["value"] = "99.0"
    case["verified_upper_bound"]["value"] = "99.0"
    label = "The source" + chr(0x2019) + "s original finite decimal display is"
    body, source_displays = re.subn(
        rf"(?:Its decimal display is|{re.escape(label)})\s+\$[0-9.]+\$",
        lambda _match: f"{label} $99.0$",
        body,
    )
    assert source_displays == 1
    # Both reported and already confirmed records are valid starting states. Replace
    # their display declarations rather than appending a second confirmation clause.
    body = re.sub(r"The verified display is\s+\$[0-9.]+\$", "", body)
    body = body.replace(
        "## Earlier Packing", "The verified display is $99.0$.\n\n## Earlier Packing"
    )
    edited = "---\n" + safe_dump(document, sort_keys=False, allow_unicode=True) + "---\n" + body
    availability = load_availability()
    historical = adopt_upper_bound_packet(
        n,
        generate_record(
            n,
            availability=availability,
            catalogue=load_drafting_catalogue([n], availability),
            review_date="2026-10-07",
            retrieved_date="2026-10-07",
        ),
    )
    refreshed = source_supersession.adopt_selected_report(n, edited, historical)
    fact = squish_upper_bound_packets.read_fact(n)
    assert f"{label} ${fact['printed_side']}$" in refreshed
    value = squish_upper_bound_packets.verified_value(
        Fraction(fact["side"]), fact["printed_side"]
    )
    assert f"The verified display is ${value}$" in refreshed
    assert "## The verified upper bound is a ceiling" not in refreshed
    assert "  rigidity: null\n" in refreshed
    with pytest.raises(ValueError, match="exactly one verified-display"):
        source_supersession.adopt_selected_report(
            n, edited.replace("The verified display is", "Stale display is"), historical
        )
    with pytest.raises(ValueError, match="exactly one generated lower-bound"):
        source_supersession.adopt_selected_report(
            n, edited.replace("## The lower bound", "## Deleted lower bound"), historical
        )
    # Coverage selecting a later source does not authorize assigning that source's
    # facts to an earlier draft's evidence, resources or body before intake.
    assert source_supersession.adopt_selected_report(n, historical, historical) == historical


@pytest.mark.parametrize(
    "n",
    [
        88,
        108,
        123,
        126,
        129,
        130,
        153,
        154,
        155,
        179,
        180,
        199,
        207,
        208,
        209,
        236,
        237,
        238,
        239,
        258,
        263,
        302,
        303,
    ],
)
def test_selected_rational_metadata_survives_refresh_and_backfill(n: int) -> None:
    """Rebuilding a selected certificate restores its primitive rational identity."""
    committed = record_path(FRONTIER, n).read_text()
    _, front, body = committed.split("---\n", 2)
    document = safe_load(front)
    case = document["packing"]
    report = case["reported_upper_bound"]
    rational = Fraction(report["exact_form"])
    expected = {
        "algebraic_degree": 1,
        "minimal_polynomial": format_polynomial((rational.denominator, -rational.numerator)),
        "algebraic_source": DERIVED_FROM_EXACT_FORM,
    }
    assert {field: report[field] for field in expected} == expected
    verified = case["verified_upper_bound"]
    status = (case["reported_status"], case["status"])
    report["minimal_polynomial"] = None
    stale = (
        "---\n" + yaml.safe_dump(document, sort_keys=False, allow_unicode=True) + "---\n" + body
    )
    availability = load_availability()
    if n == 88:
        availability[n] = _availability(n, CATALOGUE)
    refreshed = redraft(
        n,
        stale,
        availability=availability,
        catalogue=load_drafting_catalogue([n], availability),
        review_date="2026-10-07",
        retrieved_date="2026-10-07",
    )
    rebuilt = safe_load(refreshed.split("---\n", 2)[1])["packing"]
    regenerated = rebuilt["reported_upper_bound"]
    assert {field: regenerated[field] for field in expected} == expected
    assert regenerated["exact_form"] == report["exact_form"]
    assert regenerated["source_key"] == report["source_key"]
    assert regenerated["evidence"] == report["evidence"]
    assert rebuilt["verified_upper_bound"] == verified
    assert (rebuilt["reported_status"], rebuilt["status"]) == status
    assert backfilled(refreshed, n) == refreshed
    assert backfilled(backfilled(stale, n), n) == backfilled(stale, n)


def test_selected_squish_publication_admits_integer_rational_sides(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from devtools import source_supersession, squish_upper_bound_packets  # noqa: PLC0415

    n = 130
    existing = _before_ryxu(n, monkeypatch, tmp_path)
    availability = load_availability()
    historical = adopt_upper_bound_packet(
        n,
        generate_record(
            n,
            availability=availability,
            catalogue=load_drafting_catalogue([n], availability),
            review_date="2026-10-07",
            retrieved_date="2026-10-07",
        ),
    )
    fact = squish_upper_bound_packets.read_fact(n)
    fact.update(side="11", printed_side="11.0000000000000000")
    monkeypatch.setattr(squish_upper_bound_packets, "read_fact", lambda _n: fact)
    adapted = source_supersession.adopt_selected_report(n, existing, historical)
    assert r"S_n = \frac{11}{1}" in adapted
    assert (
        safe_load(adapted.split("---\n", 2)[1])["packing"]["reported_upper_bound"]["exact_form"]
        == "11"
    )


def test_an_optimizer_the_line_credits_nowhere_else_is_credited_and_dated() -> None:
    """`n = 179`'s side is Tej Stead's June 2026 optimization; `n = 129`'s optimizer is
    its finder, already credited, so only the dated sentence is added there."""
    facts = _catalogue_facts()
    assert facts[179].uncredited_optimizers == ("Tej Stead",)
    assert facts[129].uncredited_optimizers == ()
    # The "Improved by" rule the hand transcription is measured against is unchanged.
    assert "Tej Stead" not in facts[179].improved_by

    draft = _regenerate_in_range(179)
    payload = safe_load(draft.split("---\n", 2)[1])["packing"]
    assert payload["reported_upper_bound"]["improved_by"] == ["David Ellsworth", "Tej Stead"]
    body = re.sub(r"\s+", " ", _regenerate_in_range(129).split("---\n", 2)[2])
    assert "Optimized by David Ellsworth in January 2026." in body


def test_the_catalogue_s_ai_statement_is_quoted_whole_in_the_packing_paragraph() -> None:
    """epistemics.md: an AI statement goes into the record in the source's own terms."""
    body = re.sub(r"\s+", " ", _regenerate_in_range(126).split("---\n", 2)[2])
    assert (
        "In the catalogue’s words: “Found by Joost de Winter in August 2026, working with "  # noqa: RUF001
        "unspecified AI, using an evolutionary beam search with simulated annealing, "
        "starting from the latest s(105) as of December 2025.”"
    ) in body
    # Quoted once, not also as a plain "Optimized by" line.
    body_179 = re.sub(r"\s+", " ", _regenerate_in_range(179).split("---\n", 2)[2])
    assert body_179.count("Optimized by Tej Stead in June 2026") == 1
    assert ai_statements_from_credit(None) == ()
    assert AI_STATEMENT.search("Found by A. Name in 1979, via simulated annealing.") is None


def test_a_refresh_refuses_the_hand_authored_range_and_a_missing_record(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    availability = load_availability()
    into_register = argparse.Namespace(
        out=FRONTIER, review_date="2026-09-30", retrieved_date=None, force=False
    )
    assert refresh_records([83], into_register, availability, None) == 1
    assert "hand-authored" in capsys.readouterr().out

    elsewhere = argparse.Namespace(
        out=tmp_path, review_date="2026-09-30", retrieved_date=None, force=False
    )
    assert refresh_records([126], elsewhere, availability, None) == 1
    assert "does not exist" in capsys.readouterr().out


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


def test_reported_green_bound_preserves_the_verified_theorem_precision() -> None:
    """The source lane can improve without changing the certified theorem's digits.

    Read from the generator's own draft, before the reviewed promotion is applied: since
    2026-09-28 the committed record's reported lane carries wand125's 37/5, a promotion
    the generator preserves rather than derives. The certified theorem is Karakuş's general
    bound since 2026-10-02; it was Nagamochi's closed form, `7.0827625303`, until then.
    """
    committed = _committed(50)[0]["packing"]
    arguments = {
        "availability": {50: _availability(50, _source_kind(committed))},
        "catalogue": {50: _injected_facts(50)},
        "review_date": str(committed["source_reviewed"]),
        "retrieved_date": str(committed["reported_upper_bound"]["retrieved_date"]),
    }
    payload = safe_load(generate_record(50, **arguments).split("---\n")[1])["packing"]
    assert payload["reported_lower_bound"]["value"] == "7.317426011159"
    assert payload["reported_lower_bound"]["evidence"] == [
        "E-green-ds7-theorem9-reported-lower"
    ]
    assert payload["verified_lower_bound"]["value"] == "7.07647321898"
    assert (
        payload["verified_lower_bound"]["exact_form"]
        == "1/2 + sqrt(50 - floor(sqrt(50)) + 1/4)"
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


@pytest.mark.parametrize(
    "n", [n for n in update.NUMBERS if n != 153 and n not in second.NUMBERS]
)
def test_selected_update_repairs_both_lanes_without_rewriting_history(
    n: int, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    existing = _before_ryxu(n, monkeypatch, tmp_path)
    _, front, body = existing.split("---\n", 2)
    document = safe_load(front)
    case = document["packing"]
    expected_verified = case["verified_upper_bound"].copy()
    case["reported_upper_bound"].update(value="99.0", exact_form="99/1")
    case["verified_upper_bound"].update(value="98.0", exact_form="98/1")
    case["verified_lower_bound"]["value"] = "1.0"
    body, count = re.subn(
        rf"\$s\({n}\) \\le [0-9.]+\$,\s+with exact side\s+\$[0-9]+(?:/[0-9]+)?\$",
        lambda _match: f"$s({n}) \\le 99.0$, with exact side $99/1$",
        body,
    )
    assert count == 1
    body, count = re.subn(r"source print\s+\$[0-9.]+\$", "source print $99.0$", body)
    assert count == 1
    if n in update.REPLACEMENTS:
        body, count = re.subn(
            r"S_n = \\frac\{[0-9]+\}\{[0-9]+\}",
            lambda _match: r"S_n = \frac{999}{1}",
            body,
        )
        assert count == 1
    stale = (
        "---\n" + yaml.safe_dump(document, sort_keys=False, allow_unicode=True) + "---\n" + body
    )
    assert stale != existing
    availability = load_availability()
    catalogue = load_drafting_catalogue([n], availability)
    refreshed = redraft(
        n,
        stale,
        availability=availability,
        catalogue=catalogue,
        review_date="2026-10-07",
        retrieved_date="2026-10-07",
    )
    payload = safe_load(refreshed.split("---\n", 2)[1])["packing"]
    assert payload["verified_upper_bound"] == expected_verified
    assert payload["reported_upper_bound"]["source_key"] == update.SOURCE_KEY
    assert payload["reported_upper_bound"]["evidence"] == ["E-squish-update-2026-10-07-report"]
    assert payload["rigidity"] is None
    assert re.sub(r"\s+", " ", with_rigidity_of(existing, refreshed)) == re.sub(
        r"\s+", " ", existing
    )


@pytest.mark.parametrize("declaration", ["with exact side", "source print", "S_n = "])
def test_selected_update_refuses_missing_geometry_declarations(
    declaration: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    n = 126
    existing = _before_ryxu(n, monkeypatch, tmp_path)
    assert existing.count(declaration) == 1
    stale = existing.replace(declaration, "Missing declaration ", 1)
    availability = load_availability()
    with pytest.raises(GenerationError, match=r"exactly one .*side/display declaration"):
        redraft(
            n,
            stale,
            availability=availability,
            catalogue=load_drafting_catalogue([n], availability),
            review_date="2026-10-07",
            retrieved_date="2026-10-07",
        )


@pytest.mark.parametrize("mutation", ["missing", "duplicate"])
def test_confirmed_update_refuses_missing_or_duplicate_assurance(
    mutation: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    n = 126
    existing = _before_ryxu(n, monkeypatch, tmp_path)
    declaration = re.search(
        r"This update is\s+confirmed at V3/C3.*?been established\.",
        existing,
        re.DOTALL,
    )
    assert declaration is not None
    assurance = declaration.group()
    replacement = "Missing assurance." if mutation == "missing" else assurance + assurance
    stale = existing.replace(assurance, replacement, 1)
    availability = load_availability()
    with pytest.raises(GenerationError, match="assurance declaration"):
        redraft(
            n,
            stale,
            availability=availability,
            catalogue=load_drafting_catalogue([n], availability),
            review_date="2026-10-07",
            retrieved_date="2026-10-07",
        )


@pytest.mark.parametrize("n", [126, 179])
def test_update_refresh_refuses_unmapped_confirmation_evidence(
    n: int, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    existing = _before_ryxu(n, monkeypatch, tmp_path)
    _, front, body = existing.split("---\n", 2)
    document = safe_load(front)
    case = document["packing"]
    case["verified_upper_bound"] = {
        "value": case["reported_upper_bound"]["value"],
        "exact_form": case["reported_upper_bound"]["exact_form"],
        "evidence": ["E-squish-update-unmapped-exact-replay"],
    }
    confirmed = (
        "---\n" + yaml.safe_dump(document, sort_keys=False, allow_unicode=True) + "---\n" + body
    )
    availability = load_availability()
    with pytest.raises(GenerationError, match="unmapped confirmed SQUISH update evidence"):
        redraft(
            n,
            confirmed,
            availability=availability,
            catalogue=load_drafting_catalogue([n], availability),
            review_date="2026-10-07",
            retrieved_date="2026-10-07",
        )


@pytest.mark.parametrize("n", second.NUMBERS)
def test_second_update_rebuilds_current_and_historical_geometry_from_their_own_packets(
    n: int,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Each selected pose and its earlier certificate survive real historical drafting."""
    committed = _before_ryxu(n, monkeypatch, tmp_path)
    _, front, body = committed.split("---\n", 2)
    document = safe_load(front)
    case = document["packing"]
    verified = case["verified_upper_bound"].copy()
    case["reported_upper_bound"].update(value="99.0", exact_form="99/1")
    if "E-squish-second-update-2026-10-07-exact-replay" not in verified["evidence"]:
        # The reported owner reconstructs earlier lanes. Confirmed lanes must first
        # match their complete admitted evidence; a forged value is refused separately.
        case["verified_upper_bound"].update(value="98.0", exact_form="98/1")
    case["verified_lower_bound"]["value"] = "1.0"
    body, count = re.subn(
        rf"\$s\({n}\) \\le [0-9.]+\$,\s+with exact side\s+\$[0-9]+(?:/[0-9]+)?\$",
        lambda _: f"$s({n}) \\le 99.0$, with exact side $99/1$",
        body,
    )
    assert count == (2 if n in (179, 263) else 1)
    body, count = re.subn(r"source print\s+\$[0-9.]+\$", "source print $99.0$", body)
    assert count == (2 if n in (179, 263) else 1)
    if n in (108, 180):
        body, count = re.subn(
            r"S_n = \\frac\{[0-9]+\}\{[0-9]+\}", lambda _: r"S_n = \frac{999}{1}", body
        )
        assert count == 1
        body, count = re.subn(
            r"The source[\u2019']s original finite decimal display is\s+\$[0-9.]+\$",
            "The source's original finite decimal display is $99.0$",
            body,
        )
        assert count == 1
        body, count = re.subn(
            r"The verified display is\s+\$[0-9.]+\$", "The verified display is $99.0$", body
        )
        assert count == 1
    stale = (
        "---\n" + yaml.safe_dump(document, sort_keys=False, allow_unicode=True) + "---\n" + body
    )
    availability = load_availability()
    if n == 88:
        availability[n] = _availability(n, CATALOGUE)
    refreshed = redraft(
        n,
        stale,
        availability=availability,
        catalogue=load_drafting_catalogue([n], availability),
        review_date="2026-10-07",
        retrieved_date="2026-10-07",
    )
    rebuilt = safe_load(refreshed.split("---\n", 2)[1])["packing"]
    assert rebuilt["verified_upper_bound"] == verified
    assert rebuilt["reported_upper_bound"]["source_key"] == second.SOURCE_KEY
    assert rebuilt["reported_upper_bound"]["evidence"] == [second.EVIDENCE_ID]
    assert rebuilt["rigidity"] is None
    assert normalized(with_rigidity_of(committed, refreshed)) == normalized(committed)
