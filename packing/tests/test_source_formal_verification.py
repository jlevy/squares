"""A retained producer build can verify a formal theorem without confirming it here."""

from __future__ import annotations

import gzip
import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from devtools import check_results, verifier_registry
from devtools.check_results import derive_confirmation, derive_verification
from devtools.validate_schemas import source_build_file_problems
from sqpack.assurance import (
    check_case_semantics,
    check_evidence_semantics,
    conditional_problems,
)
from sqpack.yamlio import safe_load


def source_build() -> dict:
    return {
        "id": "E-source-formal-build",
        "claim": "exact-value",
        "scope": {"n_values": [17]},
        "assurance": "verified",
        "method": "proof-assistant-checked",
        "origin": "external",
        "performed_by": "source-author",
        "relationship_to_generator": "same-implementation",
        "certificate": "Theorem.lean",
        "replay": "Pinned Lean toolchain: lake build Theorem; lake env lean Axioms.lean",
        "replay_status": "passed",
        "build_receipt": "source-build.json",
        "axioms_receipt": "source-axioms.log",
        "independence": {"coverage": {"extent": "full", "unit": "theorem import closure"}},
        "proof": {
            "source": "Theorem.lean",
            "theorem": "packing_iff",
            "scope": "Exactly the stated packing problem.",
            "pinpoints": "Theorem.lean:12",
            "assumptions": ["Pinned kernel, native compiler and standard axioms."],
            "audit_record": "source-build-audit.md",
        },
        "external_review": {
            "state": "informally-verified",
            "date": "2026-10-15",
            "reviewed_by": "Receipt and statement reviewer",
            "note": "Read the source's complete build receipt; no replay here.",
        },
    }


def test_source_formal_build_is_verification_without_confirmation() -> None:
    entry = source_build()
    assert check_evidence_semantics(entry) == []
    assert derive_verification([entry]) == "V3"
    assert derive_confirmation([entry]) == "C1"
    report = {**entry, "assurance": "reported", "reported_method": entry["method"]}
    del report["method"]
    report["replay_status"] = "not-attempted"
    assert derive_verification([report]) == "V0"
    assert derive_confirmation([report]) == "C1"


def test_source_build_receipts_and_audit_must_resolve_inside_the_repository(
    tmp_path: Path,
) -> None:
    entry = source_build()
    repo = tmp_path / "repo"
    repo.mkdir()
    for name in [
        "Theorem.lean",
        "source-build.json",
        "source-axioms.log",
        "source-build-audit.md",
    ]:
        (repo / name).write_text("Retained fixture")
    assert source_build_file_problems(entry, repo) == []
    (repo / "source-axioms.log").unlink()
    assert any(
        "axioms_receipt" in problem for problem in source_build_file_problems(entry, repo)
    )
    (tmp_path / "outside.json").write_text("Outside repository")
    (repo / "escaped.json").symlink_to(tmp_path / "outside.json")
    for bad in [
        "missing.json",
        str(repo / "source-build.json"),
        "../outside.json",
        "escaped.json",
    ]:
        entry["build_receipt"] = bad
        assert any(
            "build_receipt" in problem for problem in source_build_file_problems(entry, repo)
        )


@pytest.mark.parametrize(
    "missing",
    ["build_receipt", "axioms_receipt", "proof", "external_review", "independence"],
)
def test_source_formal_build_refuses_missing_support(missing: str) -> None:
    entry = source_build()
    del entry[missing]
    assert check_evidence_semantics(entry)
    assert derive_verification([entry]) == "V0"


def test_source_formal_build_refuses_samples_and_unread_receipts() -> None:
    entry = source_build()
    entry["independence"]["coverage"] = {
        "extent": "sample",
        "unit": "modules",
        "checked": 18,
        "of": 4951,
    }
    assert check_evidence_semantics(entry)
    assert derive_verification([entry]) == "V0"
    entry = source_build()
    entry["external_review"]["state"] = "not-reviewed"
    assert check_evidence_semantics(entry)
    assert derive_verification([entry]) == "V0"


def test_deeper_source_review_changes_v_without_claiming_a_confirming_build() -> None:
    entry = source_build()
    ai = {
        "kind": "adversarial",
        "reviewer_kind": "ai",
        "verdict": "accepted",
        "relation": "source",
        "date": "2026-10-15",
    }
    reviews: list[dict] = [{**ai, "reviewer": "A"}, {**ai, "reviewer": "B"}]
    assert derive_verification([entry], reviews) == "V3"
    reviews.append(
        {
            "kind": "oversight",
            "reviewer_kind": "human",
            "reviewer": "Owner",
            "relation": "source",
            "date": "2026-10-15",
            "verdict": "accepted",
            "checked": ["trust-boundary", "certificate-meaning", "ai-findings"],
        }
    )
    assert derive_verification([entry], reviews) == "V4"
    expert = {
        "kind": "formalization",
        "reviewer_kind": "human",
        "reviewer": "Expert",
        "relation": "project",
        "date": "2026-10-15",
        "verdict": "accepted",
        "independent_of_author": True,
        "checked": ["statement-fidelity", "definitions", "axioms", "build"],
    }
    reviews.append(expert)
    assert derive_verification([entry], reviews) == "V5"
    assert derive_confirmation([entry], reviews, open_review=True) == "C1"
    without_receipt = deepcopy(entry)
    del without_receipt["build_receipt"]
    assert derive_verification([without_receipt], reviews) == "V0"


def test_live_n17_source_receipt_supports_v_only_and_binds_its_axiom_log() -> None:
    """Authenticate retained producer bytes, without claiming their execution here."""
    evidence = safe_load(check_results.EVIDENCE.read_text())["evidence"]
    entries = {entry["id"]: entry for entry in evidence}
    entry = entries["E-n017-fitzharding-lean-source-build"]
    receipt = json.loads((check_results.REPO / entry["build_receipt"]).read_text())
    log = gzip.decompress((check_results.REPO / entry["axioms_receipt"]).read_bytes())
    assert receipt["status"] == "CLEAN_SOURCE_BUILD_ACCEPTED"
    assert receipt["theorem"] == "Sq17.square17_optimality"
    assert receipt["project_modules_rebuilt"] == 4951
    assert receipt["project_prebuilt_oleans_used"] is False
    assert receipt["unexpected_axioms"] == []
    assert receipt["native_decide_facts"] == 13343
    assert hashlib.sha256(log).hexdigest() == receipt["final_log_sha256"]
    record = next(
        row
        for row in safe_load(check_results.RESULTS.read_text())["results"]
        if row["id"] == "T-154"
    )
    cited = [entries[ref] for ref in record["evidence"]]
    assert derive_verification(cited, record["reviews"], record=record) == "V3"
    assert derive_confirmation(cited, record["reviews"], record=record) == "C1"
    report = entries["E-n017-fitzharding-lean-report"]
    assert report["assurance"] == "reported"
    assert report["replay_status"] == "not-attempted"
    assert derive_verification([report], record["reviews"], record=record) == "V0"


ONE_CASE = {"kind": "optimality", "scope": {"n_values": [17]}}


def premise_build() -> dict:
    entry = source_build()
    entry.update(id="E-premise", claim="derived-structure")
    return entry


def requires(entry: dict, *refs: str) -> dict:
    entry["proof"]["conditional_on"] = [{"hypothesis": "H", "discharged_by": list(refs)}]
    return entry


def confirming(entry: dict) -> dict:
    entry.update(origin="independently-external", performed_by="independent-external")
    return entry


@pytest.mark.parametrize("origin", sorted(check_results.CONFIRMING_ORIGINS))
def test_changing_only_producer_origin_cannot_create_confirmation(origin: str) -> None:
    entry = source_build()
    entry["origin"] = origin
    assert check_evidence_semantics(entry)
    assert derive_verification([entry], record=ONE_CASE) == "V0"
    assert derive_confirmation([entry], record=ONE_CASE) in {"C0", "C1"}
    assert verifier_registry.confirming_runs([entry]) == []
    assert verifier_registry.run_label(entry) == "the source\u2019s own run"
    assert check_results.confirmation_code(ONE_CASE, [entry]) is None
    assert check_results.distinct_methods([entry]) == 0
    assert not check_results.third_party_replayed([entry])


def test_unresolved_implication_is_legal_but_does_not_prove_its_conclusion() -> None:
    entry = requires(source_build())
    assert check_evidence_semantics(entry) == []
    assert conditional_problems({entry["id"]: entry}) == []
    assert derive_verification([entry], record=ONE_CASE) == "V0"
    assert derive_confirmation([entry], record=ONE_CASE) == "C1"


def test_source_premise_discharges_verification_without_confirming_execution() -> None:
    premise = premise_build()
    entry = requires(source_build(), premise["id"])
    entries = [entry, premise]
    assert conditional_problems({row["id"]: row for row in entries}) == []
    assert derive_verification(entries, record=ONE_CASE) == "V3"
    assert derive_confirmation(entries, record=ONE_CASE) == "C1"
    confirming(entry)
    assert derive_verification(entries, record=ONE_CASE) == "V3"
    assert derive_confirmation(entries, record=ONE_CASE) == "C1"
    assert check_results.confirmation_code(ONE_CASE, entries) is None
    confirming(premise)
    assert derive_confirmation(entries, record=ONE_CASE) == "C3"
    assert check_results.confirmation_code(ONE_CASE, entries) == "same-implementation"


@pytest.mark.parametrize(
    "defect", ["missing", "sample", "narrow", "reported", "pending", "nested", "self", "cycle"]
)
def test_a_premise_cannot_bypass_full_acyclic_claim_support(defect: str) -> None:
    premise = premise_build()
    entry = requires(source_build(), premise["id"])
    if defect == "sample":
        premise["independence"]["coverage"]["extent"] = "sample"
    elif defect == "narrow":
        premise["scope"] = {"n_values": [11]}
    elif defect == "reported":
        premise["assurance"] = "reported"
        premise["reported_method"] = premise.pop("method")
    elif defect == "pending":
        premise["replay_status"] = "not-attempted"
    elif defect == "nested":
        requires(premise)
    elif defect == "self":
        requires(entry, entry["id"])
    elif defect == "cycle":
        requires(premise, entry["id"])
    entries = [entry] if defect == "missing" else [entry, premise]
    assert derive_verification(entries, record=ONE_CASE) == "V0"
    assert derive_confirmation(entries, record=ONE_CASE) == "C1"
    assert conditional_problems({row["id"]: row for row in entries})


def test_recursive_source_premises_use_the_weakest_proof_rung() -> None:
    premise = premise_build()
    leaf = premise_build()
    leaf["id"] = "E-leaf"
    entry = requires(source_build(), premise["id"])
    requires(premise, leaf["id"])
    entries = [entry, premise, leaf]
    expert = {
        "kind": "formalization",
        "reviewer_kind": "human",
        "reviewer": "Expert",
        "relation": "source",
        "date": "2026-10-15",
        "verdict": "accepted",
        "independent_of_author": True,
        "checked": ["statement-fidelity", "definitions", "axioms", "build"],
    }
    assert conditional_problems({row["id"]: row for row in entries}) == []
    assert derive_verification(entries, [expert], record=ONE_CASE) == "V5"
    assert derive_confirmation(entries, [expert], record=ONE_CASE) == "C1"
    leaf["method"] = "exact-algebraic"
    assert derive_verification(entries, [expert], record=ONE_CASE) == "V3"


def test_existing_conditional_families_keep_their_whole_claim_rungs() -> None:
    evidence = {
        row["id"]: row for row in safe_load(check_results.EVIDENCE.read_text())["evidence"]
    }
    records = {
        row["id"]: row for row in safe_load(check_results.RESULTS.read_text())["results"]
    }
    for rid, v, c in [("T-064", "V3", "C3"), ("T-081", "V0", "C1")]:
        record = records[rid]
        cited = [evidence[ref] for ref in record["evidence"]]
        assert derive_verification(cited, record["reviews"], record=record) == v
        assert derive_confirmation(cited, record["reviews"], record=record) == c


def live_case(n: int) -> dict:
    path = check_results.ROOT / "frontier" / f"n-{n:03d}.md"
    return safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]


def test_a_producer_build_cannot_carry_the_live_n17_verified_lane() -> None:
    """Source execution verifies T-154 and leaves the case's verified bounds alone."""
    evidence = {
        row["id"]: row for row in safe_load(check_results.EVIDENCE.read_text())["evidence"]
    }
    case = live_case(17)
    assert check_case_semantics(case, evidence) == []
    promoted = deepcopy(case)
    upper = promoted["verified_upper_bound"]
    promoted["verified_lower_bound"] = {
        "value": upper["value"],
        "exact_form": upper["exact_form"],
        "evidence": ["E-n017-fitzharding-lean-source-build"],
    }
    promoted["status"] = "proved"
    problems = check_case_semantics(promoted, evidence)
    assert any(
        "E-n017-fitzharding-lean-source-build is the producer's own machine run" in problem
        for problem in problems
    ), problems
    replayed = deepcopy(evidence["E-n017-fitzharding-lean-source-build"])
    replayed.update(origin="replayed-here", performed_by="repository")
    assert not any(
        "producer's own machine run" in problem
        for problem in check_case_semantics(promoted, {**evidence, replayed["id"]: replayed})
    )


def test_a_producer_build_cannot_back_verified_rigidity() -> None:
    entry = source_build()
    entry["claim"] = "derived-structure"
    case = {
        "n": 17,
        "rigidity": {
            "property": "rigid",
            "assurance": "verified",
            "method": "proof-assistant-checked",
            "scope": "the optimum",
            "evidence": [entry["id"]],
        },
    }
    problems = check_case_semantics(case, {entry["id"]: entry})
    assert any("executed beyond the producer" in problem for problem in problems), problems
    entry.update(origin="replayed-here", performed_by="repository")
    assert not any(
        "executed beyond the producer" in problem
        for problem in check_case_semantics(case, {entry["id"]: entry})
    )


def exact_replay(entry_id: str = "E-exact-replay", claim: str = "exact-value") -> dict:
    return {
        "id": entry_id,
        "claim": claim,
        "scope": {"n_values": [17]},
        "assurance": "verified",
        "method": "exact-algebraic",
        "origin": "replayed-here",
        "performed_by": "repository",
        "relationship_to_generator": "same-implementation",
        "certificate": "certificate.json",
        "replay": "python -m check certificate.json",
        "replay_status": "passed",
    }


@pytest.mark.parametrize(
    "actor", ["source-author", "unknown-historical", "independent-external", None]
)
def test_a_confirming_origin_needs_the_actor_it_names_for_every_method(
    actor: str | None,
) -> None:
    entry = exact_replay()
    assert derive_confirmation([entry], record=ONE_CASE) == "C3"
    if actor is None:
        del entry["performed_by"]
    else:
        entry["performed_by"] = actor
    assert derive_confirmation([entry], record=ONE_CASE) == "C0"
    assert derive_verification([entry], record=ONE_CASE) == "V3"
    assert verifier_registry.confirming_runs([entry]) == []
    assert check_results.distinct_methods([entry]) == 0
