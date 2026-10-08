"""Propose only the reviewed finite Gupta confirmation from complete actual receipts.

The scientific campaign and hosted private custody ran separately. This explicit
writer freshly admits their source, full results, houses and history; it neither
runs geometry nor earns a rung from admission, a drawing or a review marker alone.
"""

from __future__ import annotations

import argparse
import copy
import re
from fractions import Fraction
from pathlib import Path
from typing import Any

from jsonschema_rs import Draft202012Validator

from devtools import register_gupta_reports as register
from devtools import run_negative_controls as controls
from devtools import source_supersession, verifier_registry
from devtools.register_refinement_reports import dump, save
from sqpack import assurance
from sqpack.yamlio import safe_load

houses = register.houses
REVIEW = register.REVIEW
EXACT = houses.reports.EXACT_EVIDENCE
CUSTODY = "V-gupta-complete-custody"


def admit_confirmation() -> dict[int, Any]:
    """Admit complete scientific inputs anew after the mapped replay/custody closure."""
    review = (register.REPO / REVIEW).read_text()
    closure = review.split("## Full Production Integration", 1)
    if len(closure) != 2 or any(
        marker not in closure[1]
        for marker in (
            "**Decision: accepted.**",
            "**G1, closed:",
            "**G2, closed:",
            "**G3, closed:",
        )
    ):
        raise ValueError("accepted mapped native and actual custody review is required")
    positives = houses.reports.check_certification()
    houses.check_houses()
    register.read_history()
    if controls.snapshot_source_bytes() > controls.SNAPSHOT_MAX_BYTES:
        raise ValueError("complete inputs exceed the unchanged private snapshot cap")
    return positives


def custody_verifier() -> dict[str, Any]:
    return {
        "id": CUSTODY,
        "program": "devtools.gupta_house_links",
        "author": "Squares Project (Levy)",
        "provenance": "first-party",
        "language": ["Python"],
        "methods": ["exact-algebraic"],
        "role": "premises",
        "source": [
            "packing/devtools/gupta_refinement_reports.py",
            "packing/devtools/gupta_house_links.py",
            "packing/devtools/evand_arrangement_reports.py",
        ],
        "summary": "Admits all seventeen pinned originals and comparators, all 51 complete "
        "actual input/result jobs, required controls and fourteen complete selected houses.",
        "note": "Reconciles retained executions and ordinary private scientific inputs. "
        "No geometric predicate runs and admission alone confers no confirmation rung.",
    }


def confirming_evidence() -> dict[str, Any]:
    return {
        "id": EXACT,
        "claim": "upper-bound",
        "scope": {"n_values": list(houses.reports.NUMBERS)},
        "assurance": "verified",
        "method": "exact-algebraic",
        "performed_by": "repository",
        "relationship_to_generator": "independent-implementation",
        "origin": "replayed-here",
        "novelty": "previously-published",
        "source_key": houses.reports.SOURCE_KEY,
        "certificate": register.PACKET_PATH
        + "/facts/complete-certificates-and-comparators.json.xz",
        "replay": "From packing with project Python 3.14 and external TMPDIR: python -m "
        'devtools.gupta_refinement_reports certify --jobs-dir "$TMPDIR/gupta-native-jobs" '
        "--workers 2. This executes all 51 complete jobs through both native routes; "
        "check admits the retained full outcomes without repeating geometry.",
        "replay_status": "passed",
        "verifiers": ["V-sqpack-verify", "V-check-rational-witness-independent", CUSTODY],
        "independence_record": REVIEW,
        "limitations": "All seventeen complete rational source certificates pass both "
        "routes. All 34 full-roster duplicate and outside controls fail both routes, "
        "covering 3017 poses and 1714956 pair decisions in the original 255.692986-second "
        "two-worker campaign. Fourteen sides are selected; the three withdrawn offers "
        "108/123/129 retain complete inputs and results without current upper-bound credit. "
        "First-party deciding geometry is independently re-implemented from the theorem "
        "and certificate format; no author program runs. Both repository routes share "
        "certificate parsing, rational half-angle conversion, Fraction arithmetic, source "
        "inputs and the SAT method. Their separate deciding implementations do not make "
        "them independent of those shared premises. The recorded source-code relationship "
        "is to the author's solver verification, not to the other repository route. No "
        "dilation or rounding changes source geometry. The "
        "actual hosted private-worker transaction passed in 15.224 seconds with all four "
        "ordinary inputs, live native/input/original/comparator refusals and restorations, "
        "producer guards and the unchanged 45-second child. That transaction forbids "
        "geometric deciders; offline admission is not a fresh native replay. Only finite "
        "feasibility enters: no lower bound, optimum, optimizer, local-minimum theorem, "
        "rigidity, novelty, priority, formal proof or human oversight is established.",
        "external_review": {
            "state": "informally-verified",
            "date": register.DAY,
            "reviewed_by": "GPT-6 Astra source/native reviewer and separately prompted "
            "project custody and record reviewers",
            "note": "Accepted complete finite rational feasibility and actual production "
            "custody only; no human oversight or higher-rung claim.",
        },
        "source_reviewed": register.DAY,
    }


def update_row(text: str, field: str, row: dict[str, Any]) -> str:
    """Plan one id-keyed registry change while preserving all unrelated source bytes."""
    rows = safe_load(text)[field]
    matching = [item for item in rows if item["id"] == row["id"]]
    if len(matching) > 1:
        raise ValueError("unique owned registry id required")
    if matching == [row]:
        return text
    existing = source_supersession.coverage_list_span(text, field, identifier=row["id"])
    if existing is None:
        full = source_supersession.coverage_list_span(text, field)
        first = source_supersession.coverage_list_span(text, field, identifier=rows[0]["id"])
        if full is None or first is None:
            raise ValueError("existing nonempty registry list required")
        start = end = full[1]
        line = text[first[0] :].splitlines()[0]
    else:
        start, end = existing
        line = text[start:].splitlines()[0]
    indent = line[: len(line) - len(line.lstrip(" "))]
    rendered = "".join(indent + part for part in dump([row]).splitlines(keepends=True))
    return text[:start] + rendered + text[end:]


def case_plan(positives: dict[int, Any]) -> list[tuple[Path, str]]:
    """Build every selected case before any registry or frontier write."""
    plan = []
    history = {row["n"]: row for row in register.read_history()}
    for n in houses.NUMBERS:
        path = register.FRONTIER / f"n-{n:03d}.md"
        houses.reports.ensure_private(path)
        original = path.read_text()
        prefix, front, body = original.split("---\n", 2)
        document = safe_load(front)
        case = document["packing"]
        if case["n"] != n or case["reported_upper_bound"] != register.reported_bound(n):
            raise ValueError("selected upper lane differs from complete admitted source facts")
        side = positives[n]["checker_input"]["side"]
        verified = {
            "value": houses.reports.legacy.ceiling_decimal(Fraction(side), 16),
            "exact_form": side,
            "evidence": [EXACT],
        }
        previous = safe_load(history[n]["frontier"].split("---\n", 2)[1])["packing"]
        if case["verified_upper_bound"] not in (previous["verified_upper_bound"], verified):
            raise ValueError("selected verified upper lane differs from retained history")
        case["verified_upper_bound"] = verified
        if EXACT not in case["evidence"]:
            case["evidence"].append(EXACT)
        case["blockers"] = [
            block
            for block in case["blockers"]
            if not (
                block["kind"] == "source-evidence"
                and block["evidence"] == [register.REPORT]
                and block["detail"].startswith("All 51 complete dual-route native jobs passed;")
            )
        ]
        pattern = rf"\n{register.SECTION}\n.*?(?=\n## |\n<!-- This document follows)"
        body, count = re.subn(
            pattern,
            lambda match, n=n: register.preserve_prose_rendering(
                register.section(n, confirmed=True), match.group()
            ),
            body,
            flags=re.DOTALL,
        )
        if count != 1:
            raise ValueError("one selected complete Gupta construction section required")
        body = register.ceiling_prose(n, case, body)
        plan.append((path, prefix + "---\n" + dump(document) + "---\n" + body))
    return plan


def validate_records(plan: list[tuple[Path, str]]) -> None:
    """Validate declared input/output contracts before a transaction writes anything."""
    validators = {}
    for path, text in plan:
        document = safe_load(text.split("---\n", 2)[1] if path.suffix == ".md" else text)
        metadata = document["softschema"]
        if metadata["status"] != "enforced":
            raise ValueError("enforced current record contract required")
        schema_path = path.parent / metadata["schema"]
        houses.reports.ensure_private(schema_path)
        if schema_path not in validators:
            validators[schema_path] = Draft202012Validator(safe_load(schema_path.read_text()))
        payload = (
            document[metadata["envelope"]]
            if metadata.get("envelope")
            else {key: value for key, value in document.items() if key != "softschema"}
        )
        if not validators[schema_path].is_valid(payload):
            raise ValueError(f"record schema contract differs: {path.name}")


def confirmation_plan(positives: dict[int, Any]) -> list[tuple[Path, str]]:
    """Preflight cases, all registry rows and verifier rendering before the first write."""
    cases = case_plan(positives)
    paths = {
        name: register.FRONTIER / f"{name}.yaml"
        for name in ("verifiers", "evidence", "results")
    }
    for path in paths.values():
        houses.reports.ensure_private(path)
    texts = {name: path.read_text() for name, path in paths.items()}
    coverage_path = register.FRONTIER / "source-coverage.yaml"
    houses.reports.ensure_private(coverage_path)
    validate_records(
        [
            *((path, path.read_text()) for path, _ in cases),
            *((paths[name], text) for name, text in texts.items()),
            (coverage_path, coverage_path.read_text()),
        ]
    )
    texts["verifiers"] = update_row(texts["verifiers"], "verifiers", custody_verifier())
    texts["evidence"] = update_row(texts["evidence"], "evidence", confirming_evidence())
    results = safe_load(texts["results"])["results"]
    result = copy.deepcopy(next(row for row in results if row["id"] == register.RESULT))
    if result["scope"] != {"n_values": list(houses.reports.NUMBERS)}:
        raise ValueError("complete seventeen-case result scope required")
    result.update(
        verification="V3",
        confirmation="C3",
        claim="Independently re-implemented exact verification confirms finite feasibility "
        "of all seventeen rational source certificates; fourteen strictly improve both "
        "prior finite upper lanes. Three withdrawn offers remain fully retained. No "
        "lower bound, optimum or local-minimum theorem is established.",
        next_rung="V4/C4 requires two distinct accepted adversarial reviews and a retained "
        "human oversight record; none is supplied by drawing, admission or AI review alone.",
    )
    result.pop("activity", None)
    if EXACT not in result["evidence"]:
        result["evidence"].append(EXACT)
    for field, additions in (
        ("artifacts", [register.PACKET_PATH + "/receipts/exact-certification.json.xz"]),
        (
            "controls",
            [
                register.PACKET_PATH + "/receipts/exact-certification.json.xz",
                "packing/tests/test_gupta_refinement_reports.py",
                "packing/tests/test_negative_controls.py",
            ],
        ),
    ):
        retained = result.setdefault(field, [])
        for item in additions:
            if item not in retained:
                retained.append(item)
    result.setdefault("reviews", [])
    review_row = {
        "path": REVIEW,
        "kind": "adversarial",
        "reviewer": "GPT-6 Astra source/native review with separate project custody review",
        "reviewer_kind": "ai",
        "relation": "project",
        "date": register.DAY,
        "scope": "All seventeen full source/native geometries and controls, fourteen "
        "selected houses, actual private scientific custody and finite upper bounds only.",
        "verdict": "accepted",
        "covers": [register.RESULT],
    }
    if review_row not in result["reviews"]:
        result["reviews"].append(review_row)
    texts["results"] = update_row(texts["results"], "results", result)
    coverage_text = coverage_path.read_text()
    coverage = safe_load(coverage_text)
    source = copy.deepcopy(
        next(row for row in coverage["sources"] if row["id"] == register.SOURCE_ID)
    )
    if source["scope"] != {"n_values": list(houses.reports.NUMBERS)}:
        raise ValueError("complete seventeen-case coverage source required")
    if EXACT not in source["evidence"]:
        source["evidence"].append(EXACT)
    source["notes"] = (
        "All seventeen complete originals and comparators, 51 actual native "
        "jobs and full controls retained; fourteen selected finite upper bounds confirmed by "
        "independently re-implemented deciding code, three withdrawn offers fully retained. "
        "Actual private custody passed without geometric deciders. No optimality claim."
    )
    coverage_text = update_row(coverage_text, "sources", source)
    evidence = {row["id"]: row for row in safe_load(texts["evidence"])["evidence"]}
    verifiers = verifier_registry.load(paths["verifiers"])
    row = custody_verifier()
    verifiers[CUSTODY] = verifier_registry.Verifier(
        id=CUSTODY,
        program=row["program"],
        author=row["author"],
        provenance=row["provenance"],
        role=row["role"],
        record=row,
    )
    rendered_cases = []
    for path, text in cases:
        case = safe_load(text.split("---\n", 2)[1])["packing"]
        errors = assurance.check_case_semantics(case, evidence)
        if errors:
            raise ValueError("proposed case semantics differ: " + "; ".join(errors))
        section = register.render_case_verifiers.section(case, evidence, verifiers)
        rendered = register.render_case_verifiers.place(text, section)
        rendered_cases.append((path, rendered))
    plan = [
        *((paths[name], text) for name, text in texts.items()),
        (coverage_path, coverage_text),
        *rendered_cases,
    ]
    validate_records(plan)
    return plan


def confirm() -> None:
    plan = confirmation_plan(admit_confirmation())
    for path, text in plan:
        if path.read_text() != text:
            save(path, text)


def main() -> None:
    argparse.ArgumentParser(description=__doc__, allow_abbrev=False).parse_args()
    confirm()


if __name__ == "__main__":
    main()
