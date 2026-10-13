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
    render_results,
    render_verifiers,
    result_status,
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
    entry = replay_entry(verifiers=["V-audit-evand-mixed-covers"])
    (problem,) = verifier_registry.evidence_problems([entry], VERIFIERS)
    assert "names no program that decides" in problem


def test_a_new_independent_implementation_names_what_its_authors_read() -> None:
    entry = replay_entry(
        relationship_to_generator="independent-implementation",
        verifiers=["V-sqpack-verify"],
    )
    (problem,) = verifier_registry.evidence_problems([entry], VERIFIERS)
    assert "record of what its authors read" in problem
    entry["independence_record"] = "packing/devtools/check_rational_witness_independent.py"
    assert verifier_registry.evidence_problems([entry], VERIFIERS) == []
    # A deciding program whose registry entry carries the record also answers it.
    named = replay_entry(
        relationship_to_generator="independent-implementation",
        verifiers=["V-check-rational-witness-independent"],
    )
    assert verifier_registry.evidence_problems([named], VERIFIERS) == []


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
    record = {"kind": "optimality"}
    lower = run("lower-bound", "same-implementation")
    upper = run("upper-bound", "independent-implementation")
    assert check_results.confirmation_code(record, [lower, upper]) == "same-implementation"
    lower_again = run("lower-bound", "independent-implementation")
    assert (
        check_results.confirmation_code(record, [lower, lower_again, upper])
        == "independent-implementation"
    )


def test_a_bound_reads_the_runs_of_its_own_claim() -> None:
    record = {"kind": "lower-bound"}
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
    # Kleddamag's n = 11 certificate, decided again by the native parent-core coverage.
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
    row = "| `E-k2m3-wand125-valid7-independent` | replayed here | independent | T-064 |"
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
