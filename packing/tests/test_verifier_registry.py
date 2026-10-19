"""Which code confirmed each result: the verifier registry, its schema rules, the attribute
beside the rung, the prose rule, the views and the backfill.

`epistemics.md` (Which Code Confirmed It) owns the vocabulary; `devtools.verifier_registry`
holds the cross-record rules, `devtools.check_results.confirmation_code` the attribute,
`devtools.backfill_verifier_relation` the classification, and three renderers the views.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator

from devtools import (
    backfill_verifier_relation as backfill,
)
from devtools import (
    check_results,
    render_case_verifiers,
    render_evidence_inventory,
    render_results,
    render_verifiers,
    result_status,
    validate_schemas,
    verifier_registry,
)
from sqpack.yamlio import safe_load

FRONTIER = Path(__file__).resolve().parent.parent / "frontier"
EVIDENCE_TEXT = (FRONTIER / "evidence.yaml").read_text(encoding="utf-8")
EVIDENCE = {entry["id"]: entry for entry in safe_load(EVIDENCE_TEXT)["evidence"]}
RESULTS = {
    record["id"]: record
    for record in safe_load((FRONTIER / "results.yaml").read_text(encoding="utf-8"))["results"]
}
VERIFIERS = verifier_registry.load()


def evidence_schema() -> Draft202012Validator:
    document = yaml.safe_load(
        (FRONTIER / "frontier-evidence.schema.yaml").read_text(encoding="utf-8")
    )
    Draft202012Validator.check_schema(document)
    return Draft202012Validator(document)


def replay_entry(**changes: Any) -> dict[str, Any]:
    """A complete exact replay of this project's own grid bound."""
    entry: dict[str, Any] = {
        "id": "E-test-replay",
        "claim": "upper-bound",
        "scope": {"n_values": [9]},
        "assurance": "verified",
        "method": "exact-algebraic",
        "performed_by": "repository",
        "relationship_to_generator": "same-implementation",
        "origin": "replayed-here",
        "certificate": "frontier/n-009.md",
        "replay": "uv run --frozen python -m devtools.check_basic_bounds",
        "replay_status": "passed",
        "verifiers": ["V-check-basic-bounds"],
        "limitations": "A test entry.",
        "source_reviewed": "2026-10-02",
    }
    entry.update(changes)
    return {key: value for key, value in entry.items() if value is not None}


def schema_errors(entry: dict[str, Any]) -> list[str]:
    document = {"last_reviewed": "2026-10-02", "evidence": [entry]}
    return [error.message for error in evidence_schema().iter_errors(document)]


# --- The schema --------------------------------------------------------------------------


def test_an_entry_that_runs_code_names_its_programs() -> None:
    assert schema_errors(replay_entry()) == []
    assert schema_errors(replay_entry(verifiers=None))
    # A replay with no program named says nothing about what ran.
    assert schema_errors(replay_entry(verifiers=[]))


def test_a_report_may_hold_none_of_its_sources_code() -> None:
    report = replay_entry(
        assurance="reported",
        method=None,
        reported_method="interval-certified",
        origin="external",
        performed_by="source-author",
        replay=None,
        certificate=None,
        replay_status="public-certificate-missing",
        verifiers=[],
    )
    assert schema_errors(report) == []


def test_a_proof_needs_no_programs() -> None:
    proof = replay_entry(
        method="published-proof",
        origin="external",
        performed_by="source-author",
        relationship_to_generator="not-applicable",
        replay=None,
        certificate=None,
        replay_status="not-attempted",
        verifiers=None,
        proof={
            "source": "a paper",
            "theorem": "a theorem",
            "scope": "n = 9",
            "pinpoints": "p. 1",
            "assumptions": [],
        },
        external_review={"state": "not-reviewed", "date": "2026-10-02"},
    )
    assert schema_errors(proof) == []


def test_shared_components_are_named_and_only_with_that_relation() -> None:
    shared = replay_entry(relationship_to_generator="shared-components")
    assert schema_errors(shared), "shared-components without the list"
    shared["shared_components"] = ["the certificate loader"]
    assert schema_errors(shared) == []
    stray = replay_entry(shared_components=["the certificate loader"])
    assert schema_errors(stray), "a list beside another relation"


# --- The registry's cross-record rules ---------------------------------------------------


def test_the_record_has_no_registry_problem() -> None:
    assert verifier_registry.problems(list(EVIDENCE.values())) == []


def test_an_unknown_program_is_refused() -> None:
    entry = replay_entry(verifiers=["V-no-such-program"])
    problems = verifier_registry.evidence_problems([entry], VERIFIERS)
    assert problems == ["E-test-replay: names unknown verifier V-no-such-program"]


def test_a_premise_check_never_decides_alone() -> None:
    entry = replay_entry(verifiers=["V-audit-evand-mixed-covers"], independence=structured())
    (problem,) = verifier_registry.evidence_problems([entry], VERIFIERS)
    assert "names no program that decides" in problem


def authorship(**changes: Any) -> dict[str, Any]:
    """A complete structured record of who wrote a program and what they read."""
    record: dict[str, Any] = {
        "read": ["mathematics", "certificate-format"],
        "clean_room": True,
        "shares": [],
        "written_by": [
            {
                "kind": "ai",
                "system": "Claude (Anthropic)",
                "setting": "a review lane at the tbd-strong-max tier, reasoning max",
            }
        ],
        "overlaps_producer": {
            "extent": "system-family",
            "separate_prompt": True,
            "separate_code": True,
            "note": "The producer also used Claude.",
        },
    }
    record.update(changes)
    return record


def structured(extent: str = "full", **changes: Any) -> dict[str, Any]:
    """An evidence entry's structured record: its coverage and its authorship."""
    coverage: dict[str, Any] = {"extent": extent, "unit": "rows of the certificate"}
    if extent == "sample":
        coverage.update(checked=6, of=273)
    return {"coverage": coverage, **authorship(**changes)}


def test_a_new_independent_implementation_names_what_its_authors_read() -> None:
    entry = replay_entry(
        relationship_to_generator="independent-implementation",
        verifiers=["V-sqpack-verify"],
        independence=structured(),
    )
    (problem,) = verifier_registry.evidence_problems([entry], VERIFIERS)
    assert "record of what its authors read" in problem
    entry["independence_record"] = "packing/devtools/check_rational_witness_independent.py"
    assert verifier_registry.evidence_problems([entry], VERIFIERS) == []
    # A deciding program whose registry entry carries the record also answers it.
    named = replay_entry(
        relationship_to_generator="independent-implementation",
        verifiers=["V-check-rational-witness-independent"],
        independence=structured(),
    )
    assert verifier_registry.evidence_problems([named], VERIFIERS) == []


# --- The structured independence record --------------------------------------------------


def independent(**changes: Any) -> dict[str, Any]:
    """A new independent-implementation replay whose path record is in place."""
    return replay_entry(
        **{
            "relationship_to_generator": "independent-implementation",
            "verifiers": ["V-check-rational-witness-independent"],
            **changes,
        }
    )


def test_a_new_independent_implementation_states_its_coverage_and_authorship() -> None:
    bare = independent()
    problems = verifier_registry.evidence_problems([bare], VERIFIERS)
    assert len(problems) == 2
    assert "states its coverage" in problems[0]
    assert "who wrote its deciding code" in problems[1]
    # Coverage is the entry's own; the authorship may be its own instead of its program's.
    covered = independent(independence={"coverage": structured()["coverage"]})
    (problem,) = verifier_registry.evidence_problems([covered], VERIFIERS)
    assert "who wrote its deciding code" in problem
    assert (
        verifier_registry.evidence_problems([independent(independence=structured())], VERIFIERS)
        == []
    )
    assert schema_errors(independent(independence=structured())) == []


def test_the_schema_holds_the_record_whole() -> None:
    assert schema_errors(independent(independence={"read": ["mathematics"]}))
    partial = structured()
    del partial["written_by"]
    assert schema_errors(independent(independence=partial)), "authorship comes whole"
    sample = structured("sample")
    del sample["coverage"]["of"]
    assert schema_errors(independent(independence=sample)), "a sample says of how many"
    named = structured()
    named["written_by"] = [{"kind": "ai", "setting": "max"}]
    assert schema_errors(independent(independence=named)), "an AI author names its system"


def test_clean_room_means_the_producers_code_was_neither_read_nor_shared() -> None:
    read = structured(read=["specification", "producer-code"])
    (problem,) = verifier_registry.record_problems("E-x", read)
    assert "read the producer" in problem
    shared = structured(shares=["the certificate loader"])
    shared["overlaps_producer"] = {**shared["overlaps_producer"], "separate_code": False}
    problems = verifier_registry.record_problems("E-x", shared)
    assert [problem.split(": ", 1)[1] for problem in problems] == [
        "its independence record says clean_room, but it shares the producer\u2019s components",
        "its independence record says clean_room, but not separate_code",
    ]
    apart = structured(clean_room=False, shares=["the parser"])
    (problem,) = verifier_registry.record_problems("E-x", apart)
    assert "separate_code" in problem


def test_an_independent_implementation_shares_nothing_of_the_producers_code() -> None:
    entry = independent(independence=structured(clean_room=False, shares=["the parser"]))
    entry["independence"]["overlaps_producer"]["separate_code"] = False
    problems = verifier_registry.evidence_problems([entry], VERIFIERS)
    assert any("makes the relation shared-components" in problem for problem in problems)


def test_a_sample_counts_fewer_than_all_and_full_counts_all() -> None:
    assert verifier_registry.record_problems("E-x", structured("sample")) == []
    whole = structured("sample")
    whole["coverage"]["checked"] = 273
    (problem,) = verifier_registry.record_problems("E-x", whole)
    assert "fewer than all" in problem
    short = structured()
    short["coverage"].update(checked=6, of=273)
    (problem,) = verifier_registry.record_problems("E-x", short)
    assert "checks all" in problem


def test_a_new_first_party_program_that_decides_carries_the_record() -> None:
    document = safe_load((FRONTIER / "verifiers.yaml").read_text(encoding="utf-8"))
    row = {
        "id": "V-test-new-checker",
        "program": "check.py",
        "author": "Squares Project (Levy)",
        "provenance": "first-party",
        "language": ["Python"],
        "methods": ["exact-algebraic"],
        "role": "decides",
        "source": ["packing/devtools/verifier_registry.py"],
        "summary": "A test program.",
    }
    verifiers = {
        **VERIFIERS,
        row["id"]: verifier_registry.Verifier(
            id=row["id"],
            program=row["program"],
            author=row["author"],
            provenance=row["provenance"],
            role=row["role"],
            record=row,
        ),
    }
    ids = [entry["id"] for entry in document["verifiers"]] + [row["id"]]
    (problem,) = verifier_registry.registry_problems(verifiers, ids)
    assert "V-test-new-checker is a first-party program that decides" in problem
    row["independence"] = authorship()
    assert verifier_registry.registry_problems(verifiers, ids) == []
    # A premise check need not carry it.
    row.pop("independence")
    premises = verifier_registry.Verifier(
        id=row["id"],
        program=row["program"],
        author=row["author"],
        provenance=row["provenance"],
        role="premises",
        record={**row, "role": "premises"},
    )
    assert verifier_registry.registry_problems({**VERIFIERS, row["id"]: premises}, ids) == []


def test_the_structured_exemptions_are_removed_when_the_record_is_present() -> None:
    evidence = list(EVIDENCE.values())
    exempt = min(verifier_registry.UNSTRUCTURED_EVIDENCE)
    given = [
        {**entry, "independence": structured()} if entry["id"] == exempt else entry
        for entry in evidence
    ]
    stale = [
        problem for problem in verifier_registry.problems(given) if "UNSTRUCTURED" in problem
    ]
    expected = (
        f"{exempt}: exempt from the structured independence record, but no longer an "
        "independent-implementation entry without one; remove it from UNSTRUCTURED_EVIDENCE"
    )
    assert stale == [expected]
    assert all(
        VERIFIERS[vid].provenance == verifier_registry.FIRST_PARTY and VERIFIERS[vid].decides
        for vid in verifier_registry.UNSTRUCTURED_PROGRAMS
    )


def test_a_sample_derives_no_rung_and_confirms_nothing_whole() -> None:
    sample = independent(independence=structured("sample"))
    assert check_results.derive_verification([sample]) == "V0"
    assert check_results.derive_confirmation([sample]) == "C0"
    assert verifier_registry.confirming_runs([sample]) == []
    whole = independent(independence=structured())
    assert check_results.derive_verification([whole]) == "V3"
    assert check_results.derive_confirmation([whole]) == "C3"
    assert verifier_registry.confirming_runs([whole]) == [whole]


def test_the_ladder_is_per_run_and_ignores_premise_authorship() -> None:
    replay = replay_entry(independence=authorship())
    assert verifier_registry.ladder_level(replay, {}) == "reproduced"
    replay["relationship_to_generator"] = "generator"
    assert verifier_registry.ladder_level(replay, {}) == "reproduced"
    replay["relationship_to_generator"] = "independent-implementation"
    assert verifier_registry.ladder_level(replay, {}) == "clean-room"
    replay["independence"] = authorship(clean_room=False, read=["producer-code"])
    assert verifier_registry.ladder_level(replay, {}) == "after-reading"
    replay["relationship_to_generator"] = "shared-components"
    assert verifier_registry.ladder_level(replay, {}) == "shared"
    line = verifier_registry.independence_line(authorship())
    assert line.startswith("its authors read")
    assert "with its own prompt and code" in line


def test_the_grandfathered_entries_are_exempt_and_only_while_they_need_it() -> None:
    grandfathered = deepcopy(EVIDENCE["E-basic-grid-upper"])
    assert grandfathered["relationship_to_generator"] == "independent-implementation"
    assert verifier_registry.evidence_problems([grandfathered], VERIFIERS) == []
    moved = [
        {**entry, "relationship_to_generator": "same-implementation"}
        if entry["id"] == "E-basic-grid-upper"
        else entry
        for entry in EVIDENCE.values()
    ]
    stale = [
        problem for problem in verifier_registry.problems(moved) if "grandfathered" in problem
    ]
    expected = (
        "E-basic-grid-upper: grandfathered for its independence record, but no longer an "
        "independent-implementation entry; remove it from GRANDFATHERED_INDEPENDENCE"
    )
    assert stale == [expected]


def test_every_external_program_names_the_versions_that_ran() -> None:
    for verifier in VERIFIERS.values():
        if verifier.provenance == verifier_registry.EXTERNAL:
            assert verifier.record.get("versions"), verifier.id


# --- The attribute beside the rung -------------------------------------------------------


def run(claim: str, relation: str) -> dict[str, Any]:
    return replay_entry(claim=claim, relationship_to_generator=relation)


def test_an_exact_value_is_as_independent_as_its_less_independent_half() -> None:
    record = {"kind": "optimality", "scope": {"n_values": [9]}}
    lower = run("lower-bound", "same-implementation")
    upper = run("upper-bound", "independent-implementation")
    assert check_results.confirmation_code(record, [lower, upper]) == "same-implementation"
    lower_again = run("lower-bound", "independent-implementation")
    assert (
        check_results.confirmation_code(record, [lower, lower_again, upper])
        == "independent-implementation"
    )


def test_a_bound_reads_the_runs_of_its_own_claim() -> None:
    record = {"kind": "lower-bound", "scope": {"n_values": [9]}}
    entries = [
        run("lower-bound", "same-implementation"),
        run("upper-bound", "independent-implementation"),
    ]
    assert check_results.confirmation_code(record, entries) == "same-implementation"
    entries.append(run("lower-bound", "shared-components"))
    assert check_results.confirmation_code(record, entries) == "shared-components"


def test_no_confirming_run_reads_as_nothing() -> None:
    report = replay_entry(origin="external", replay_status="not-attempted")
    assert check_results.confirmation_code({"kind": "lower-bound"}, [report]) is None


def test_the_spot_checked_results_read_as_their_records_say() -> None:
    def code(rid: str) -> str | None:
        record = RESULTS[rid]
        return check_results.confirmation_code(
            record, [EVIDENCE[ref] for ref in record["evidence"]]
        )

    # zmx2 re-run on the s(60), s(59), s(77) and s(32) covers: the source's own checker.
    for rid in ("T-062", "T-066", "T-067", "T-051"):
        assert code(rid) == "same-implementation", rid
    # wand125's rectangle certificates replayed with Tokoharu's verify.cpp.
    for rid in ("T-045", "T-070"):
        assert code(rid) == "same-implementation", rid
    # This project's fractional certificates, re-decided by an interval route that reuses
    # the certificate loader.
    for rid in ("T-017", "T-018"):
        assert code(rid) == "shared-components", rid
    # Overbeck's n = 11 certificate, decided again by the native parent-core coverage.
    assert code("T-037") == "independent-implementation"


# --- The prose rule ----------------------------------------------------------------------


def test_confirmed_in_register_prose_says_which_kind() -> None:
    bare = {"id": "T-999", "claim": "The bound is confirmed here by a complete replay."}
    (problem,) = check_results.confirmation_prose_problems(bare)
    assert problem.startswith("T-999: claim says confirmed without saying how")
    for phrase in (
        "reproduced with the producer\u2019s code",
        "with the producer's code",
        "by an independent re-implementation",
        "independently re-implemented",
        "by a re-implementation sharing components with the source",
    ):
        said = {"id": "T-999", "claim": f"The bound is confirmed here, {phrase}."}
        assert check_results.confirmation_prose_problems(said) == [], phrase


def test_confirms_as_a_verb_also_says_which_kind() -> None:
    bare = {"id": "T-999", "claim": "Complete exact replay confirms the bound at n = 68."}
    (problem,) = check_results.confirmation_prose_problems(bare)
    assert problem.startswith("T-999: claim says confirmed without saying how")
    said = {
        "id": "T-999",
        "claim": "Complete exact replay, independently re-implemented, confirms the bound.",
    }
    assert check_results.confirmation_prose_problems(said) == []


def test_the_prose_rule_reads_the_word_and_not_its_neighbours() -> None:
    record = {
        "id": "T-999",
        "claim": "The search is confirmed-novel. This retain confirms H-219.",
        "composition": "The confirmation rung is C3.",
        "notes": "History: it was confirmed by distinct methods.",
    }
    assert check_results.confirmation_prose_problems(record) == []


# --- The views ---------------------------------------------------------------------------


def test_a_confirmed_status_says_how() -> None:
    record = RESULTS["T-062"]
    line = result_status.status_line(
        record, EVIDENCE, how="reproduced with the producer\u2019s code"
    )
    assert line == "confirmed, reproduced with the producer\u2019s code"
    # Any result not yet confirmed, since the register moves results up: T-064 was the
    # example here until its confirmation landed.
    unconfirmed = next(
        record
        for _, record in sorted(RESULTS.items())
        if result_status.status(record, EVIDENCE) != result_status.CONFIRMED
    )
    assert result_status.status_line(
        unconfirmed, EVIDENCE, how="anything"
    ) == result_status.status_line(unconfirmed, EVIDENCE)


def test_results_md_names_the_programs_behind_each_result() -> None:
    text = render_results.render()
    assert "| confirmed, reproduced with the producer\u2019s code |" in text
    assert "## Verification Code" in text
    assert (
        "  - `E-n060-evand-mixed-cover-zmx2-replay`, replayed here, reproduced with the "
        "producer\u2019s code: `V-evand-zmx2` (external); `V-replay-evand-zmx2`, "
        "`V-audit-evand-mixed-covers` (first-party, premises)"
    ) in text
    assert "[`VERIFIERS.md`](VERIFIERS.md)" in text


def test_a_third_partys_report_reads_as_a_report() -> None:
    """A third party's run held here only as their report, origin `external`, confirms
    nothing, so its line says it was not replayed here and names no code relation, whose
    words are a confirmation's. Until 2026-10-06 wand125's run of ValidTilt9 read "a
    third party's run, independently re-implemented" in `RESULTS.md` under T-081."""
    report = EVIDENCE["E-k2m4-wand125-validtilt9-report"]
    assert report["origin"] == "external"
    assert report["performed_by"] == "independent-external"
    assert verifier_registry.run_label(report) == verifier_registry.THIRD_PARTY_REPORT
    line = verifier_registry.entry_line(report, VERIFIERS)
    assert line.startswith(
        "`E-k2m4-wand125-validtilt9-report`, reported by a third party, not replayed here: "
    )
    assert not any(label in line for label in verifier_registry.LABELS.values())
    # A third party's replay retained here is a confirmation, and says how it stands.
    retained = {**report, "origin": "independently-external"}
    assert verifier_registry.run_label(retained) == "replayed by a third party"
    assert "independently re-implemented" in verifier_registry.entry_line(retained, VERIFIERS)
    assert "a third party\u2019s run" not in render_results.render()


def test_the_committed_views_agree_with_the_records() -> None:
    assert render_verifiers.main(["--check"]) == 0
    assert render_case_verifiers.main(["--check"]) == 0
    assert (FRONTIER / "RESULTS.md").read_text(encoding="utf-8") == render_results.render()


def test_verifiers_md_lists_every_program_with_what_it_backs() -> None:
    text = render_verifiers.render()
    for verifier_id in VERIFIERS:
        assert f"### `{verifier_id}`" in text
    row = (
        "| `E-k2m3-wand125-valid7-independent` | replayed here | "
        "independently re-implemented | not recorded | T-064 |"
    )
    assert row in text


def test_a_case_section_sits_before_the_footer_and_is_rewritten_in_place() -> None:
    lines = [
        "<!-- BEGIN verification code: written by devtools.render_case_verifiers -->",
        "x",
        render_case_verifiers.END,
    ]
    footer = "<!-- This document follows common-doc-guidelines.md.\nfooter\n-->\n"
    text = f"# s(9)\n\nProse.\n\n{footer}"
    placed = render_case_verifiers.place(text, lines)
    assert placed.index("x") < placed.index("<!-- This document follows")
    again = render_case_verifiers.place(placed, [*lines[:1], "y", lines[-1]])
    assert "x" not in again
    assert again.count(render_case_verifiers.BEGIN) == 1


# --- The backfill ------------------------------------------------------------------------


def test_the_backfill_is_idempotent_on_the_record() -> None:
    updated, outcome = backfill.backfill(EVIDENCE_TEXT, list(EVIDENCE.values()))
    assert updated == EVIDENCE_TEXT
    assert outcome.written == []
    assert outcome.fixed == []
    assert outcome.unclassified == []


def test_the_backfill_writes_one_line_and_audits_the_relation() -> None:
    text = (
        "evidence:\n"
        "  - id: E-test-replay\n"
        "    claim: lower-bound\n"
        "    relationship_to_generator: independent-implementation\n"
        "    replay: python -m devtools.audit_wand125_rectangles --replay\n"
        "    replay_status: passed\n"
        "    origin: replayed-here\n"
        "    method: interval-certified\n"
        "    limitations: A test entry.\n"
    )
    entries = safe_load(text)["evidence"]
    updated, outcome = backfill.backfill(text, entries)
    assert (
        updated.split("\n")[6]
        == "    verifiers: [V-tokoharu-verify-cpp, V-audit-wand125-rectangles]"
    )
    assert len(updated.split("\n")) == len(text.split("\n")) + 1
    ((eid, why),) = outcome.questions
    assert eid == "E-test-replay"
    assert "reads as same-implementation; the record says independent-implementation" in why


def test_an_unfamiliar_replay_is_left_for_a_person() -> None:
    entry = replay_entry(replay="./some-new-checker --all", verifiers=None)
    assert backfill.classify(entry) is None


@pytest.mark.parametrize(
    ("eid", "programs", "relation"),
    [
        (
            "E-wand125-rectangle-source-replay",
            {"V-tokoharu-verify-cpp", "V-audit-wand125-rectangles"},
            "same-implementation",
        ),
        (
            "E-n059-wand125-mixed-cover-zmx2-replay",
            {"V-evand-zmx2", "V-replay-evand-zmx2", "V-audit-evand-mixed-covers"},
            "same-implementation",
        ),
        (
            "E-n032-evand-zmx2-full-sym-replay",
            {"V-evand-zmx2", "V-replay-evand-zmx2", "V-audit-evand-mixed-covers"},
            "same-implementation",
        ),
        (
            "E-k2m3-wand125-valid7-independent",
            {"V-wand125-valid7-checker", "V-audit-valid7-independent", "V-probe-valid7-fixes"},
            "independent-implementation",
        ),
        ("E-n012-fractional-certificate", {"V-sqpack-fractional-exact"}, "same-implementation"),
        (
            "E-fractional-interval-decision",
            {"V-sqpack-fractional-interval"},
            "shared-components",
        ),
        (
            "E-wand125-point-source-replay",
            {"V-wand125-check-with-sqpack", "V-sqpack-fractional-exact"},
            "same-implementation",
        ),
    ],
)
def test_spot_checked_entries_name_their_programs(
    eid: str, programs: set[str], relation: str
) -> None:
    entry = EVIDENCE[eid]
    assert set(entry["verifiers"]) == programs
    assert entry["relationship_to_generator"] == relation


def test_legacy_exemptions_can_only_shrink() -> None:
    """Fixed 14 October 2026 baseline: new entries cannot bypass the contract."""
    assert {
        "E-basic-area-lower",
        "E-basic-grid-upper",
        "E-bentz13-figure2-audit",
        "E-bentz46-theorem8-audit",
        "E-gobel-family-upper",
        "E-gobel-offcentre-upper",
        "E-gobel-strip-upper",
        "E-lifted-q2-upper",
        "E-lifted-q7-upper",
        "E-n005-gobel-upper",
        "E-n010-gobel-upper",
        "E-n011-h236-rung0-reduction",
        "E-n011-kleddamag-3875-native-parent-core",
        "E-n011-trump-upper",
        "E-n011-wang-li-native-parent-core",
        "E-n012-evand-15680-3951-native-parent-core",
        "E-n012-monotonicity-lower",
        "E-n017-burns-control-decision",
        "E-n017-certified-endpoint",
        "E-n017-guzhou-r012-interval-decision",
        "E-n017-mira-4613-exact-replay",
        "E-n017-mira-4613-interval-decision",
        "E-n029-interval-certified-upper",
        "E-n029-kingbird-numerical",
        "E-n029-orientation-classes",
        "E-n029-schadt-numerical",
        "E-n040-gobel-upper",
        "E-n061-wand125-point-cover-evand-replay-report",
        "E-n082-gobel-l-upper",
        "E-wand125-tools-n11-row-report",
    } >= verifier_registry.GRANDFATHERED_INDEPENDENCE, "legacy exemptions may only shrink"
    assert {
        "V-assess-frontier-rigidity",
        "V-assess-n40-rigidity",
        "V-assess-n5-rigidity",
        "V-audit-clipped-corner-transfer",
        "V-audit-continuous-pose",
        "V-check-basic-bounds",
        "V-check-half-angle-area",
        "V-check-karakus-strip-measure",
        "V-check-nagamochi-lemma1-counterexample",
        "V-check-rational-witness-independent",
        "V-dilation-corollary",
        "V-five-dot-independent-union",
        "V-green17-interval-audit",
        "V-k3-n17-capture-row-checker",
        "V-k3-n17-root-isolation",
        "V-kingbird29-verify-svg",
        "V-n11-optimality-checkers",
        "V-n12-independent-verifier",
        "V-n17-catalogue-polynomial",
        "V-n17-endpoint-checkers",
        "V-n17-weighted-instrument",
        "V-optimal-moduli",
        "V-rectangle-ceiling",
        "V-replay-owner-footprint-cover",
        "V-review-trump-local-theorem",
        "V-ryxu-undilated-n51-independent",
        "V-screen-translation-escape",
        "V-sqpack-cover",
        "V-sqpack-fractional-exact",
        "V-sqpack-fractional-interval",
        "V-sqpack-parent-core-native",
        "V-sqpack-threshold-exact",
        "V-sqpack-threshold-interval",
        "V-sqpack-verify",
        "V-sqverify-fast",
        "V-trump11-fixed-angle-tree-check",
        "V-trump11-isolation-radius",
        "V-trump11-tangent-cones",
        "V-upper-bound-intervals",
        "V-upper-bound-promotion",
        "V-wall-owner-containment",
        "V-wall-owner-footprints",
    } >= verifier_registry.UNSTRUCTURED_PROGRAMS, "legacy exemptions may only shrink"
    assert {
        "E-barnett-505-exact-feasibility",
        "E-basic-area-lower",
        "E-basic-grid-upper",
        "E-bentz13-figure2-audit",
        "E-bentz46-theorem8-audit",
        "E-couzo-451-exact-feasibility",
        "E-couzo-460-followup-exact-feasibility",
        "E-couzo-476-exact-feasibility",
        "E-couzo-488-exact-feasibility",
        "E-couzo-506-exact-feasibility",
        "E-deleeuw-483-exact-feasibility",
        "E-evand-399-exact-feasibility",
        "E-evand-465-record-hunt-exact-feasibility",
        "E-evand-489-exact-feasibility",
        "E-evand-exact-ceilings-2026-10-05-exact-replay",
        "E-evand-exact-optima-2026-10-05-exact-replay",
        "E-evand-regularized-exact-feasibility",
        "E-evand-trio126-exact-feasibility",
        "E-fang-484-exact-feasibility",
        "E-franciscouzo-2026-09-27-exact-replay",
        "E-franciscouzo-2026-09-27-interval-replay",
        "E-franciscouzo-2026-10-03-exact-replay",
        "E-franciscouzo-2026-10-03-interval-replay",
        "E-gobel-family-upper",
        "E-gobel-offcentre-upper",
        "E-gobel-strip-upper",
        "E-green17-interval-audit",
        "E-gupta-438-exact-feasibility",
        "E-k2m3-wand125-valid7-independent",
        "E-k2m4-wand125-validtilt9-report",
        "E-karakus-strip-measure-interval",
        "E-lifted-q2-upper",
        "E-lifted-q7-upper",
        "E-mishapolk-470-exact-feasibility",
        "E-n005-gobel-upper",
        "E-n010-gobel-upper",
        "E-n011-five-dot-independent-union",
        "E-n011-h236-rung0-reduction",
        "E-n011-kleddamag-3875-native-parent-core",
        "E-n011-trump-local-theorem-first-clause",
        "E-n011-trump-upper",
        "E-n011-wang-li-native-parent-core",
        "E-n012-evand-15680-3951-native-parent-core",
        "E-n012-independent-verifier",
        "E-n012-levy-15680000-3949423-native-parent-core",
        "E-n012-monotonicity-lower",
        "E-n012-squarepacker-31360-7901-native-parent-core",
        "E-n012-squarepacker-7943-2000-native-parent-core",
        "E-n017-burns-control-decision",
        "E-n017-certified-endpoint",
        "E-n017-guzhou-r012-interval-decision",
        "E-n017-kleddamag-rational-upper",
        "E-n017-massaccesi-h052-agreement",
        "E-n017-mira-4613-exact-replay",
        "E-n017-mira-4613-interval-decision",
        "E-n017-overbeck-capture-independent-sample",
        "E-n017-overbeck-statement-root-independent",
        "E-n018-wand125-mixed-4704-sqverify-fast-replay",
        "E-n019-wand125-mixed-48229-sqverify-fast-replay",
        "E-n019-wand125-rect-48175-sqverify-fast-replay",
        "E-n020-wand125-rect-48975-sqverify-fast-replay",
        "E-n020-wand125-rect-49-sqverify-fast-replay",
        "E-n026-wand125-rect-55325-sqverify-fast-replay",
        "E-n027-wand125-rect-5635-sqverify-fast-replay",
        "E-n028-wand125-rect-57225-sqverify-fast-replay",
        "E-n029-interval-certified-upper",
        "E-n029-kingbird-numerical",
        "E-n029-orientation-classes",
        "E-n029-schadt-numerical",
        "E-n029-schadt-rational-upper",
        "E-n029-wand125-mixed-581-sqverify-fast-replay",
        "E-n029-wand125-rect-57975-sqverify-fast-replay",
        "E-n030-wand125-rect-5875-sqverify-fast-replay",
        "E-n031-wand125-rect-59525-sqverify-fast-replay",
        "E-n038-wand125-rect-6545-sqverify-fast-replay",
        "E-n039-wand125-rect-6635-sqverify-fast-replay",
        "E-n040-gobel-upper",
        "E-n040-guzhou-clipped-corner-finite-audit",
        "E-n040-guzhou-continuous-pose-crate-axis",
        "E-n040-guzhou-continuous-pose-finite-audit",
        "E-n040-wand125-rect-67-sqverify-fast-replay",
        "E-n041-wand125-rect-676-sqverify-fast-replay",
        "E-n042-wand125-mixed-68475-sqverify-fast-replay",
        "E-n042-wand125-rect-6815-sqverify-fast-replay",
        "E-n042-wand125-rect-68275-sqverify-fast-replay",
        "E-n043-wand125-mixed-69075-sqverify-fast-replay",
        "E-n043-wand125-rect-68875-sqverify-fast-replay",
        "E-n044-wand125-mixed-69725-sqverify-fast-replay",
        "E-n044-wand125-rect-69425-sqverify-fast-replay",
        "E-n051-wand125-mixed-746-sqverify-fast-replay",
        "E-n051-wand125-mixed-747-sqverify-fast-replay",
        "E-n052-wand125-mixed-755-sqverify-fast-replay",
        "E-n053-wand125-mixed-76275-sqverify-fast-replay",
        "E-n053-wand125-rect-76075-sqverify-fast-replay",
        "E-n054-wand125-mixed-7685-sqverify-fast-replay",
        "E-n054-wand125-rect-76725-sqverify-fast-replay",
        "E-n055-wand125-mixed-7728-sqverify-fast-replay",
        "E-n055-wand125-rect-77125-sqverify-fast-replay",
        "E-n056-wand125-mixed-78025-sqverify-fast-replay",
        "E-n056-wand125-rect-77825-sqverify-fast-replay",
        "E-n057-wand125-mixed-78725-sqverify-fast-replay",
        "E-n058-wand125-mixed-7905-sqverify-fast-replay",
        "E-n058-wand125-mixed-7935-sqverify-fast-replay",
        "E-n061-wand125-point-cover-evand-replay-report",
        "E-n066-wand125-mixed-843-sqverify-fast-replay",
        "E-n066-wand125-rect-8385-sqverify-fast-replay",
        "E-n067-wand125-mixed-8475-sqverify-fast-replay",
        "E-n067-wand125-mixed-848-sqverify-fast-replay",
        "E-n068-wand125-rect-851-sqverify-fast-replay",
        "E-n069-ellsworth-2026-09-exact-replay",
        "E-n069-wand125-mixed-8612-sqverify-fast-replay",
        "E-n069-wand125-mixed-862-sqverify-fast-replay",
        "E-n069-wand125-rect-8585-sqverify-fast-replay",
        "E-n070-wand125-mixed-86475-sqverify-fast-replay",
        "E-n070-wand125-mixed-86575-sqverify-fast-replay",
        "E-n070-wand125-rect-8625-sqverify-fast-replay",
        "E-n070-wand125-rect-86275-sqverify-fast-replay",
        "E-n071-wand125-mixed-8705-sqverify-fast-replay",
        "E-n071-wand125-mixed-8721-sqverify-fast-replay",
        "E-n072-wand125-mixed-876-sqverify-fast-replay",
        "E-n073-wand125-mixed-8809-sqverify-fast-replay",
        "E-n073-wand125-mixed-8813-sqverify-fast-replay",
        "E-n074-wand125-mixed-88675-sqverify-fast-replay",
        "E-n074-wand125-rect-88475-sqverify-fast-replay",
        "E-n075-wand125-mixed-892-sqverify-fast-replay",
        "E-n075-wand125-mixed-894-sqverify-fast-replay",
        "E-n075-wand125-rect-89-sqverify-fast-replay",
        "E-n076-wand125-mixed-896-sqverify-fast-replay",
        "E-n076-wand125-mixed-8965-sqverify-fast-replay",
        "E-n076-wand125-rect-8925-sqverify-fast-replay",
        "E-n082-gobel-l-upper",
        "E-n083-chang-2026-09-exact-replay",
        "E-n083-wand125-mixed-937-sqverify-fast-replay",
        "E-n084-wand125-mixed-94075-sqverify-fast-replay",
        "E-n084-wand125-mixed-9411-sqverify-fast-replay",
        "E-n085-wand125-mixed-946-sqverify-fast-replay",
        "E-n086-wand125-mixed-950-sqverify-fast-replay",
        "E-n086-wand125-mixed-9503-sqverify-fast-replay",
        "E-n086-wand125-rect-9365-sqverify-fast-replay",
        "E-n087-chang-2026-09-exact-replay",
        "E-n087-wand125-mixed-948-sqverify-fast-replay",
        "E-n087-wand125-mixed-955-sqverify-fast-replay",
        "E-n087-wand125-mixed-958-sqverify-fast-replay",
        "E-n087-wand125-rect-941-sqverify-fast-replay",
        "E-n088-wand125-mixed-960-sqverify-fast-replay",
        "E-n088-wand125-mixed-96125-sqverify-fast-replay",
        "E-n088-wand125-mixed-962-sqverify-fast-replay",
        "E-n088-wand125-rect-94775-sqverify-fast-replay",
        "E-n089-wand125-mixed-965-sqverify-fast-replay",
        "E-n089-wand125-rect-9565-sqverify-fast-replay",
        "E-n090-wand125-mixed-9725-sqverify-fast-replay",
        "E-n090-wand125-mixed-973-sqverify-fast-replay",
        "E-n090-wand125-rect-95775-sqverify-fast-replay",
        "E-n091-wand125-mixed-970-sqverify-fast-replay",
        "E-n091-wand125-mixed-975-sqverify-fast-replay",
        "E-n091-wand125-mixed-97625-sqverify-fast-replay",
        "E-n092-wand125-mixed-975-sqverify-fast-replay",
        "E-n092-wand125-mixed-977-sqverify-fast-replay",
        "E-n093-wand125-mixed-986-sqverify-fast-replay",
        "E-n093-wand125-mixed-988-sqverify-fast-replay",
        "E-n093-wand125-rect-97225-sqverify-fast-replay",
        "E-n094-wand125-mixed-992-sqverify-fast-replay",
        "E-n094-wand125-mixed-994-sqverify-fast-replay",
        "E-n094-wand125-mixed-995-sqverify-fast-replay",
        "E-n094-wand125-rect-9805-sqverify-fast-replay",
        "E-n095-wand125-mixed-996-sqverify-fast-replay",
        "E-n095-wand125-mixed-9965-sqverify-fast-replay",
        "E-n095-wand125-rect-98518-sqverify-fast-replay",
        "E-n096-wand125-mixed-996-sqverify-fast-replay",
        "E-n096-wand125-mixed-997-sqverify-fast-replay",
        "E-n211-de-winter-exact-replay",
        "E-n211-de-winter-interval-replay",
        "E-nagamochi-lemma1-counterexample",
        "E-ostashev-501-exact-feasibility",
        "E-pingyou-503-exact-feasibility",
        "E-pingyou-504-exact-feasibility",
        "E-rehwaldt-couzo-refinements-2026-10-07-exact-replay",
        "E-ryxu-432-radical-n51-feasibility",
        "E-ryxu-432-rational-feasibility",
        "E-squish-481-exact-feasibility",
        "E-squish-500-exact-feasibility",
        "E-squish-n153-2026-10-07-exact-replay",
        "E-squish-second-update-2026-10-07-exact-replay",
        "E-squish-ten-packings-2026-10-07-exact-replay",
        "E-squish-update-2026-10-07-exact-replay",
        "E-wand125-tools-ceiling-certificates",
        "E-wand125-tools-n11-row-report",
    } >= verifier_registry.UNSTRUCTURED_EVIDENCE, "legacy exemptions may only shrink"
    assert {
        "E-barnett-505-exact-feasibility",
        "E-basic-area-lower",
        "E-basic-grid-upper",
        "E-bentz13-figure2-audit",
        "E-bentz46-theorem8-audit",
        "E-chelokot-square-minus-two-lean",
        "E-couzo-451-exact-feasibility",
        "E-couzo-460-followup-exact-feasibility",
        "E-couzo-476-exact-feasibility",
        "E-couzo-488-exact-feasibility",
        "E-couzo-506-exact-feasibility",
        "E-deleeuw-483-exact-feasibility",
        "E-evand-399-exact-feasibility",
        "E-evand-465-record-hunt-exact-feasibility",
        "E-evand-489-exact-feasibility",
        "E-evand-exact-ceilings-2026-10-05-exact-replay",
        "E-evand-exact-ceilings-2026-10-05-source-replay",
        "E-evand-exact-optima-2026-10-05-exact-replay",
        "E-evand-exact-optima-2026-10-05-source-replay",
        "E-evand-regularized-exact-feasibility",
        "E-evand-trio126-exact-feasibility",
        "E-fang-484-exact-feasibility",
        "E-fractional-interval-decision",
        "E-franciscouzo-2026-09-27-exact-replay",
        "E-franciscouzo-2026-09-27-interval-replay",
        "E-franciscouzo-2026-10-03-exact-replay",
        "E-franciscouzo-2026-10-03-interval-replay",
        "E-gobel-family-upper",
        "E-gobel-offcentre-upper",
        "E-gobel-strip-upper",
        "E-green17-interval-audit",
        "E-green17-sixteen-point-lower",
        "E-gupta-438-exact-feasibility",
        "E-k2m3-evand-bentz-lean-build",
        "E-k2m3-evand-valid7-qx2-replay",
        "E-k2m3-wand125-valid7-independent",
        "E-k2m4-evand-bentz4-lean-build",
        "E-karakus-strip-measure-interval",
        "E-lifted-q2-upper",
        "E-lifted-q7-upper",
        "E-mishapolk-470-exact-feasibility",
        "E-n005-fixed-side-local-rigidity",
        "E-n005-gobel-upper",
        "E-n005-second-order-rigidity",
        "E-n010-gobel-upper",
        "E-n011-corner-class-96-25-exact-decision",
        "E-n011-corner-class-96-25-interval-decision",
        "E-n011-five-dot-full-net",
        "E-n011-five-dot-independent-union",
        "E-n011-fractional-certificate",
        "E-n011-fractional-dilation-limit",
        "E-n011-fractional-net1440-certificate",
        "E-n011-fractional-net1440-dilation-limit",
        "E-n011-fractional-net1440-interval-decision",
        "E-n011-fractional-net720-certificate",
        "E-n011-fractional-net720-dilation-limit",
        "E-n011-global-optimality-independent",
        "E-n011-h236-rung0-reduction",
        "E-n011-kleddamag-3875-native-parent-core",
        "E-n011-kleddamag-3875-source-replay",
        "E-n011-lean-statement-closure-build",
        "E-n011-optimum-uniqueness",
        "E-n011-repaired-lower",
        "E-n011-threshold-certificate",
        "E-n011-threshold-interval-decision",
        "E-n011-threshold-net1440-certificate",
        "E-n011-threshold-net1440-dilation-limit",
        "E-n011-threshold-net1440-interval-decision",
        "E-n011-threshold-net2880-certificate",
        "E-n011-threshold-net2880-dilation-limit",
        "E-n011-threshold-net2880-interval-decision",
        "E-n011-threshold-net720-certificate",
        "E-n011-threshold-net720-dilation-limit",
        "E-n011-trump-isolation-radius",
        "E-n011-trump-local-rigidity",
        "E-n011-trump-local-theorem-first-clause",
        "E-n011-trump-upper",
        "E-n011-wall-owner-containment",
        "E-n011-wall-owner-footprints",
        "E-n011-wang-li-native-parent-core",
        "E-n011-wang-li-source-replay",
        "E-n012-evand-15680-3951-native-parent-core",
        "E-n012-evand-15680-3951-source-replay",
        "E-n012-fractional-certificate",
        "E-n012-independent-verifier",
        "E-n012-levy-15680000-3949423-audit",
        "E-n012-levy-15680000-3949423-generator",
        "E-n012-levy-15680000-3949423-native-parent-core",
        "E-n012-levy-15680000-3949423-source-replay",
        "E-n012-monotonicity-lower",
        "E-n012-squarepacker-31360-7901-native-parent-core",
        "E-n012-squarepacker-31360-7901-source-replay",
        "E-n012-squarepacker-7943-2000-audit",
        "E-n012-squarepacker-7943-2000-native-parent-core",
        "E-n012-squarepacker-7943-2000-source-replay",
        "E-n013-evand-casefree-cover-lean-kernel",
        "E-n013-evand-casefree-cover-zmx2-replay",
        "E-n017-anabologyco-weighted-certificate",
        "E-n017-burns-control-decision",
        "E-n017-burns-source-replay",
        "E-n017-catalogue-polynomial-identity",
        "E-n017-certified-endpoint",
        "E-n017-fort-point-certificate-replay",
        "E-n017-fractional-certificate",
        "E-n017-guzhou-r012-interval-decision",
        "E-n017-guzhou-r012-source-replay",
        "E-n017-guzhou-r052-source-replay",
        "E-n017-guzhou-r067-source-replay",
        "E-n017-guzhou-r068-source-replay",
        "E-n017-guzhou-r071-source-replay",
        "E-n017-kleddamag-461300-99853-source-replay",
        "E-n017-kleddamag-4640020-source-replay",
        "E-n017-kleddamag-466001-source-replay",
        "E-n017-kleddamag-rational-upper",
        "E-n017-massaccesi-h052-agreement",
        "E-n017-massaccesi-source-replay",
        "E-n017-mira-4613-exact-replay",
        "E-n017-mira-4613-interval-decision",
        "E-n017-mira-point-certificate-replay",
        "E-n017-overbeck-candidate-check-py-replay",
        "E-n017-overbeck-statement-root-independent",
        "E-n018-fractional-certificate",
        "E-n018-t028-fractional-certificate",
        "E-n018-t029-fractional-certificate",
        "E-n018-t030-fractional-certificate",
        "E-n018-wand125-mixed-470-source-replay",
        "E-n018-wand125-mixed-4704-source-replay",
        "E-n018-wand125-mixed-4704-sqverify-fast-replay",
        "E-n018-wand125-mixed-4705-sqverify-fast-replay",
        "E-n019-wand125-mixed-48229-sqverify-fast-replay",
        "E-n019-wand125-mixed-4825-sqverify-fast-replay",
        "E-n019-wand125-rect-48175-sqverify-fast-replay",
        "E-n020-fractional-certificate",
        "E-n020-fractional-certificate-97-20",
        "E-n020-wand125-mixed-4905-sqverify-fast-replay",
        "E-n020-wand125-rect-48975-sqverify-fast-replay",
        "E-n020-wand125-rect-49-sqverify-fast-replay",
        "E-n021-evand-5000-1001-source-replay",
        "E-n021-evand-mixed-cover-zmx2-replay",
        "E-n021-fractional-certificate-122-25",
        "E-n021-wand125-point-endpoint-source-replay",
        "E-n026-wand125-mixed-5545-sqverify-fast-replay",
        "E-n026-wand125-rect-55325-sqverify-fast-replay",
        "E-n027-wand125-mixed-56435-sqverify-fast-replay",
        "E-n027-wand125-rect-5635-sqverify-fast-replay",
        "E-n028-wand125-mixed-5735-sqverify-fast-replay",
        "E-n028-wand125-rect-57225-sqverify-fast-replay",
        "E-n029-interval-certified-upper",
        "E-n029-kingbird-numerical",
        "E-n029-orientation-classes",
        "E-n029-schadt-numerical",
        "E-n029-schadt-rational-upper",
        "E-n029-wand125-mixed-581-sqverify-fast-replay",
        "E-n029-wand125-rect-57975-sqverify-fast-replay",
        "E-n030-wand125-mixed-58835-sqverify-fast-replay",
        "E-n030-wand125-rect-5875-sqverify-fast-replay",
        "E-n031-wand125-rect-59525-sqverify-fast-replay",
        "E-n032-evand-closed-cover-source-run",
        "E-n032-evand-closed-cover-zmx2-replay",
        "E-n032-evand-zmx2-full-sym-replay",
        "E-n037-wand125-mixed-644-source-replay",
        "E-n038-wand125-rect-6545-sqverify-fast-replay",
        "E-n039-wand125-mixed-665-sqverify-fast-replay",
        "E-n039-wand125-rect-6635-sqverify-fast-replay",
        "E-n040-first-order-flexibility",
        "E-n040-gobel-upper",
        "E-n040-guzhou-clipped-corner-finite-audit",
        "E-n040-guzhou-clipped-corner-sqverify-fast-replay",
        "E-n040-guzhou-continuous-pose-crate-axis",
        "E-n040-guzhou-continuous-pose-finite-audit",
        "E-n040-guzhou-continuous-pose-kernel-replay",
        "E-n040-wand125-rect-67-sqverify-fast-replay",
        "E-n041-wand125-mixed-6775-sqverify-fast-replay",
        "E-n041-wand125-rect-676-sqverify-fast-replay",
        "E-n042-wand125-mixed-68475-sqverify-fast-replay",
        "E-n042-wand125-rect-6815-sqverify-fast-replay",
        "E-n042-wand125-rect-68275-sqverify-fast-replay",
        "E-n043-wand125-mixed-69075-sqverify-fast-replay",
        "E-n043-wand125-rect-68875-sqverify-fast-replay",
        "E-n044-wand125-mixed-69725-sqverify-fast-replay",
        "E-n044-wand125-rect-69425-sqverify-fast-replay",
        "E-n045-evand-mixed-cover-zmx2-replay",
        "E-n045-wand125-point-cover-source-replay",
        "E-n050-wand125-mixed-740-source-replay",
        "E-n051-wand125-mixed-746-sqverify-fast-replay",
        "E-n051-wand125-mixed-747-sqverify-fast-replay",
        "E-n052-wand125-mixed-755-sqverify-fast-replay",
        "E-n053-wand125-mixed-76275-sqverify-fast-replay",
        "E-n053-wand125-rect-76075-sqverify-fast-replay",
        "E-n054-wand125-mixed-7685-sqverify-fast-replay",
        "E-n054-wand125-rect-76725-sqverify-fast-replay",
        "E-n055-wand125-mixed-7728-sqverify-fast-replay",
        "E-n055-wand125-rect-77125-sqverify-fast-replay",
        "E-n056-wand125-mixed-78025-sqverify-fast-replay",
        "E-n056-wand125-rect-77825-sqverify-fast-replay",
        "E-n057-wand125-mixed-78725-sqverify-fast-replay",
        "E-n058-wand125-mixed-7905-sqverify-fast-replay",
        "E-n058-wand125-mixed-7935-sqverify-fast-replay",
        "E-n059-wand125-mixed-cover-zmx2-replay",
        "E-n060-evand-mixed-cover-zmx2-replay",
        "E-n061-wand125-point-cover-zmx2-replay",
        "E-n065-wand125-mixed-835-source-replay",
        "E-n066-wand125-mixed-842-source-replay",
        "E-n066-wand125-mixed-843-sqverify-fast-replay",
        "E-n066-wand125-rect-8385-sqverify-fast-replay",
        "E-n067-wand125-mixed-8475-sqverify-fast-replay",
        "E-n067-wand125-mixed-848-sqverify-fast-replay",
        "E-n068-wand125-rect-851-sqverify-fast-replay",
        "E-n069-ellsworth-2026-09-exact-replay",
        "E-n069-wand125-mixed-8612-sqverify-fast-replay",
        "E-n069-wand125-mixed-862-sqverify-fast-replay",
        "E-n069-wand125-rect-8585-sqverify-fast-replay",
        "E-n070-wand125-mixed-86475-sqverify-fast-replay",
        "E-n070-wand125-mixed-86575-sqverify-fast-replay",
        "E-n070-wand125-rect-8625-sqverify-fast-replay",
        "E-n070-wand125-rect-86275-sqverify-fast-replay",
        "E-n071-wand125-mixed-8705-sqverify-fast-replay",
        "E-n071-wand125-mixed-8721-sqverify-fast-replay",
        "E-n072-wand125-mixed-876-sqverify-fast-replay",
        "E-n073-wand125-mixed-8809-sqverify-fast-replay",
        "E-n073-wand125-mixed-8813-sqverify-fast-replay",
        "E-n074-wand125-mixed-88675-sqverify-fast-replay",
        "E-n074-wand125-rect-88475-sqverify-fast-replay",
        "E-n075-wand125-mixed-892-sqverify-fast-replay",
        "E-n075-wand125-mixed-894-sqverify-fast-replay",
        "E-n075-wand125-rect-89-sqverify-fast-replay",
        "E-n076-wand125-mixed-894-source-replay",
        "E-n076-wand125-mixed-896-sqverify-fast-replay",
        "E-n076-wand125-mixed-8965-sqverify-fast-replay",
        "E-n076-wand125-rect-8925-sqverify-fast-replay",
        "E-n077-wand125-mixed-cover-zmx2-replay",
        "E-n082-gobel-l-upper",
        "E-n082-wand125-linear-932-source-replay",
        "E-n083-chang-2026-09-exact-replay",
        "E-n083-wand125-linear-935-source-replay",
        "E-n083-wand125-mixed-937-source-replay",
        "E-n083-wand125-mixed-937-sqverify-fast-replay",
        "E-n084-wand125-mixed-940-source-replay",
        "E-n084-wand125-mixed-94075-sqverify-fast-replay",
        "E-n084-wand125-mixed-9411-sqverify-fast-replay",
        "E-n085-wand125-mixed-942-source-replay",
        "E-n085-wand125-mixed-946-source-replay",
        "E-n085-wand125-mixed-946-sqverify-fast-replay",
        "E-n086-wand125-mixed-950-sqverify-fast-replay",
        "E-n086-wand125-mixed-9503-sqverify-fast-replay",
        "E-n086-wand125-rect-9365-sqverify-fast-replay",
        "E-n087-chang-2026-09-exact-replay",
        "E-n087-wand125-mixed-948-source-replay",
        "E-n087-wand125-mixed-948-sqverify-fast-replay",
        "E-n087-wand125-mixed-955-sqverify-fast-replay",
        "E-n087-wand125-mixed-958-sqverify-fast-replay",
        "E-n087-wand125-rect-941-sqverify-fast-replay",
        "E-n088-wand125-mixed-960-sqverify-fast-replay",
        "E-n088-wand125-mixed-96125-sqverify-fast-replay",
        "E-n088-wand125-mixed-962-sqverify-fast-replay",
        "E-n088-wand125-rect-94775-sqverify-fast-replay",
        "E-n089-wand125-mixed-965-sqverify-fast-replay",
        "E-n089-wand125-rect-9565-sqverify-fast-replay",
        "E-n090-wand125-mixed-960-source-replay",
        "E-n090-wand125-mixed-9725-sqverify-fast-replay",
        "E-n090-wand125-mixed-973-sqverify-fast-replay",
        "E-n090-wand125-rect-95775-sqverify-fast-replay",
        "E-n091-wand125-mixed-970-source-replay",
        "E-n091-wand125-mixed-970-sqverify-fast-replay",
        "E-n091-wand125-mixed-975-sqverify-fast-replay",
        "E-n091-wand125-mixed-97625-sqverify-fast-replay",
        "E-n092-wand125-mixed-969-source-replay",
        "E-n092-wand125-mixed-975-source-replay",
        "E-n092-wand125-mixed-975-sqverify-fast-replay",
        "E-n092-wand125-mixed-977-sqverify-fast-replay",
        "E-n093-wand125-mixed-986-sqverify-fast-replay",
        "E-n093-wand125-mixed-988-sqverify-fast-replay",
        "E-n093-wand125-rect-97225-sqverify-fast-replay",
        "E-n094-wand125-mixed-992-sqverify-fast-replay",
        "E-n094-wand125-mixed-994-sqverify-fast-replay",
        "E-n094-wand125-mixed-995-sqverify-fast-replay",
        "E-n094-wand125-rect-9805-sqverify-fast-replay",
        "E-n095-wand125-mixed-996-sqverify-fast-replay",
        "E-n095-wand125-mixed-9965-sqverify-fast-replay",
        "E-n095-wand125-rect-98518-sqverify-fast-replay",
        "E-n096-wand125-mixed-996-source-replay",
        "E-n096-wand125-mixed-996-sqverify-fast-replay",
        "E-n096-wand125-mixed-997-sqverify-fast-replay",
        "E-n101-wand125-linear-1028-source-replay",
        "E-n211-de-winter-exact-replay",
        "E-n211-de-winter-interval-replay",
        "E-nagamochi-lemma1-counterexample",
        "E-ostashev-501-exact-feasibility",
        "E-perfect-square-tiling-rigid",
        "E-pingyou-503-exact-feasibility",
        "E-pingyou-504-exact-feasibility",
        "E-rehwaldt-couzo-refinements-2026-10-07-exact-replay",
        "E-rehwaldt-n68-refinement-2026-10-07-exact-replay",
        "E-ryxu-432-radical-n51-feasibility",
        "E-ryxu-432-rational-feasibility",
        "E-side2-center-lower",
        "E-squish-481-exact-feasibility",
        "E-squish-500-exact-feasibility",
        "E-squish-n153-2026-10-07-exact-replay",
        "E-squish-second-update-2026-10-07-exact-replay",
        "E-squish-ten-packings-2026-10-07-exact-replay",
        "E-squish-update-2026-10-07-exact-replay",
        "E-tokoharu-density-source-replay",
        "E-translation-escape-not-rigid",
        "E-wand125-n052-derived-lower",
        "E-wand125-n068-derived-lower",
        "E-wand125-point-source-replay",
        "E-wand125-rectangle-2026-09-28-source-replay",
        "E-wand125-rectangle-2026-10-01-source-replay",
        "E-wand125-rectangle-2026-10-02-source-replay",
        "E-wand125-rectangle-source-replay",
        "E-wand125-tools-ceiling-certificates",
        "E-wand125-tools-n11-row-replay",
    } >= verifier_registry.UNCOVERED_REPLAYS, "legacy exemptions may only shrink"


@pytest.mark.parametrize("method", ["exact-algebraic", "numerical-f64", "proof-audited"])
def test_samples_are_filtered_before_every_verification_branch(method: str) -> None:
    sample = independent(
        independence=structured("sample"),
        method=method,
        precision={"decimal_digits": 9},
        proof={"source": "a proof"},
        external_review={
            "state": "informally-verified",
            "date": "2026-10-14",
            "reviewed_by": "reviewer",
            "note": "read the argument",
        },
    )
    assert check_results.derive_verification([sample]) == "V0"
    assert check_results.derive_confirmation([sample]) == "C0"
    sample["origin"] = "external"
    assert check_results.derive_confirmation([sample]) == "C0"


@pytest.mark.parametrize(
    "eid",
    [
        "E-n017-overbeck-capture-sample-replay",
        "E-n017-overbeck-capture-independent-sample",
        "E-n017-overbeck-tree-sample-replay",
    ],
)
def test_the_older_samples_have_explicit_non_rung_bearing_coverage(eid: str) -> None:
    entry = EVIDENCE[eid]
    assert verifier_registry.sampled(entry)
    assert check_results.derive_verification([entry]) == "V0"
    assert check_results.derive_confirmation([entry]) == "C0"


@pytest.mark.parametrize("relation", ["same-implementation", "generator", "shared-components"])
def test_every_new_replay_requires_coverage_whatever_its_relation(relation: str) -> None:
    entry = replay_entry(relationship_to_generator=relation)
    assert any(
        "replay states its coverage" in problem
        for problem in verifier_registry.evidence_problems([entry], VERIFIERS)
    )
    entry["independence"] = {"coverage": structured()["coverage"]}
    assert not any(
        "replay states its coverage" in problem
        for problem in verifier_registry.evidence_problems([entry], VERIFIERS)
    )


def test_a_sample_must_have_actually_checked_an_instance() -> None:
    sample = structured("sample")
    sample["coverage"]["checked"] = 0
    assert schema_errors(independent(independence=sample))
    assert verifier_registry.record_problems("E-test", sample) == [
        "E-test: a sample checks at least one instance"
    ]


def test_entry_authorship_cannot_overrule_a_deciding_program() -> None:
    vid = "V-overbeck-review3-upper-at-l"
    entry = independent(verifiers=[vid], independence=structured())
    assert any(
        "clean_room contradicts" in problem
        for problem in verifier_registry.evidence_problems([entry], VERIFIERS)
    )
    entry["relationship_to_generator"] = "shared-components"
    entry["independence"]["clean_room"] = False
    assert any(
        "names no shared deciding component" in problem
        for problem in verifier_registry.evidence_problems([entry], VERIFIERS)
    )


def test_missing_authorship_fields_leave_schema_diagnostics_visible() -> None:
    verifiers = deepcopy(VERIFIERS)
    vid = "V-overbeck-review3-upper-at-l"
    record = verifiers[vid].record["independence"]
    del record["shares"]
    verifier_registry.evidence_problems(
        [independent(verifiers=[vid], independence=structured())], verifiers
    )
    assert "its authors read" in verifier_registry.independence_line(record)
    assert schema_errors(independent(independence={"read": ["mathematics"]}))


def test_sample_coverage_is_visible_in_each_reader_view() -> None:
    eid = "E-n017-fitzharding-native-facts-review2"
    entry = EVIDENCE[eid]
    expected = "sample, 10 of 13,343"
    assert expected in verifier_registry.entry_line(entry, VERIFIERS)
    assert expected in render_verifiers.render()
    inventory = render_evidence_inventory.render()
    assert expected in inventory
    assert "are samples, counted separately" in inventory


@pytest.mark.parametrize("kind", ["optimality", "formalization", "simplification"])
def test_full_component_runs_do_not_establish_a_whole_value(kind: str) -> None:
    record = {"kind": kind, "scope": {"n_values": [17]}}
    if kind in check_results.SECOND_PROOF_KINDS:
        record["proves_kind"] = "optimality"
    parts = [
        entry
        for eid, entry in EVIDENCE.items()
        if eid.startswith("E-n017-overbeck-")
        and eid.endswith("review3")
        and not verifier_registry.sampled(entry)
    ]
    assert len(parts) == 5
    assert check_results.derive_verification(parts, record=record) == "V0"
    assert check_results.derive_confirmation(parts, record=record) == "C0"


def test_value_rungs_require_both_sides_at_each_count_and_take_the_minimum() -> None:
    record = {"kind": "optimality", "scope": {"n_values": [9, 10]}}
    lower = replay_entry(claim="lower-bound", scope={"n_values": [9]})
    upper = replay_entry(claim="upper-bound", scope={"n_values": [10]})
    assert check_results.derive_verification([lower, upper], record=record) == "V0"
    assert check_results.derive_confirmation([lower, upper], record=record) == "C0"
    both = replay_entry(claim="exact-value", scope=record["scope"])
    assert check_results.derive_verification([both], record=record) == "V3"
    assert check_results.derive_confirmation([both], record=record) == "C3"
    lower["scope"] = record["scope"]
    upper["scope"] = record["scope"]
    upper.update(method="numerical-f64", precision={"decimal_digits": 9})
    assert check_results.derive_verification([lower, upper], record=record) == "V1"
    assert check_results.derive_confirmation([lower, upper], record=record) == "C2"


def test_premise_helpers_do_not_limit_or_strengthen_the_deciding_level() -> None:
    entry = replay_entry(
        relationship_to_generator="independent-implementation",
        verifiers=["V-overbeck-review3-root-isolation", "V-overbeck-review3-spec-lemmas"],
    )
    assert verifier_registry.ladder_level(entry, VERIFIERS) == "clean-room"
    entry["verifiers"].append("V-overbeck-review3-upper-at-l")
    assert verifier_registry.ladder_level(entry, VERIFIERS) == "after-reading"


@pytest.mark.parametrize("wrapper", ["formalization", "simplification"])
@pytest.mark.parametrize(
    ("conclusion", "claim"),
    [
        ("lower-bound", "lower-bound"),
        ("upper-bound", "upper-bound"),
        ("rigidity", "derived-structure"),
        ("optimality", "exact-value"),
    ],
)
def test_second_proof_rungs_follow_its_actual_conclusion(
    wrapper: str, conclusion: str, claim: str
) -> None:
    record = {"kind": wrapper, "proves_kind": conclusion, "scope": {"n_values": [17, 18]}}
    own = replay_entry(claim=claim, scope=record["scope"], method=check_results.FORMAL_METHOD)
    assert check_results.derive_verification([own], record=record) == "V3"
    assert check_results.derive_confirmation([own], record=record) == "C3"
    assert check_results.confirmation_code(record, [own]) == "same-implementation"
    own["scope"] = {"n_values": [17]}
    assert check_results.derive_verification([own], record=record) == "V0"
    assert check_results.derive_confirmation([own], record=record) == "C0"
    assert check_results.confirmation_code(record, [own]) is None


def test_legacy_independence_does_not_invent_what_authors_read() -> None:
    entry = replay_entry(
        relationship_to_generator="independent-implementation",
        verifiers=["V-n12-independent-verifier"],
    )
    assert verifier_registry.ladder_level(entry, VERIFIERS) is None
    assert verifier_registry.ladder_label(entry, VERIFIERS) == "independently re-implemented"
    line = verifier_registry.entry_line(entry, VERIFIERS)
    assert "independently re-implemented" in line
    assert "after reading" not in line
    entry["independence"] = authorship(clean_room=False, read=["mathematics"])
    assert verifier_registry.ladder_level(entry, {}) is None
    entry["independence"]["read"].append("producer-code")
    assert verifier_registry.ladder_level(entry, {}) == "after-reading"


@pytest.mark.parametrize("coverage", [["sample"], "sample", 1, None])
def test_malformed_coverage_preserves_schema_diagnostics_without_a_rung(coverage: Any) -> None:
    record = structured()
    record["coverage"] = coverage
    entry = independent(independence=record)
    assert schema_errors(entry)
    verifier_registry.evidence_problems([entry], VERIFIERS)
    assert check_results.derive_verification([entry]) == "V0"
    assert check_results.derive_confirmation([entry]) == "C0"
    assert verifier_registry.confirming_runs([entry]) == []


def test_malformed_coverage_does_not_interrupt_the_schema_gate(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    document = safe_load(EVIDENCE_TEXT)
    entry = next(
        row
        for row in document["evidence"]
        if row["id"] == "E-n017-overbeck-literal-checks-review3"
    )
    entry["independence"]["coverage"] = ["sample"]
    malformed = yaml.safe_dump(document, sort_keys=False)
    original = Path.read_text
    target = FRONTIER / "evidence.yaml"

    def read(path: Path, *args: Any, **kwargs: Any) -> str:
        return malformed if path == target else original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read)
    assert validate_schemas.main() == 1
    diagnostic = capsys.readouterr().err
    assert "FAIL evidence.yaml" in diagnostic
    assert "coverage" in diagnostic
