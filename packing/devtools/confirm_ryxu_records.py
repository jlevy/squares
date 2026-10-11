"""Integrate accepted #432 finite-feasibility confirmation from retained executions.

This explicit record writer runs after scoped production custody review. It admits
complete actual inputs/results, never reruns a geometric decision or assigns a rung
from a drawing, checksum, structural check or publication alone.
"""

from __future__ import annotations

import argparse
import copy
import re
from pathlib import Path
from typing import Any

from devtools import register_ryxu_reports as register
from devtools import run_negative_controls as controls
from devtools import ryxu_house_links as houses
from devtools import verifier_registry
from devtools.confirm_refinement_records import replace_row
from devtools.register_refinement_reports import append_rows, dump, save
from sqpack.yamlio import safe_load

REVIEW = "docs/project/reviews/review-2026-10-08-ryxu-rational-radical-packets.md"
RATIONAL = houses.reports.EXACT_EVIDENCE
RADICAL = register.RADICAL_EXACT
INDEPENDENT_Q2 = "V-ryxu-undilated-n51-independent"
CUSTODY = "V-ryxu-complete-custody"


def admit_confirmation() -> None:
    """Require the recorded review and all its admitted private scientific inputs."""
    review = (register.REPO / REVIEW).read_text()
    section = review.split("## Full Production Integration", 1)
    if (
        len(section) != 2
        or "**Decision: accepted.**" not in section[1]
        or "**R3, closed:**" not in section[1]
    ):
        raise ValueError("accepted independent production/custody review is required")
    # Complete house admission already admits all 75 rational and three radical jobs.
    houses.check_houses()
    register.read_history()
    if controls.snapshot_source_bytes() > controls.SNAPSHOT_MAX_BYTES:
        raise ValueError("complete worker inputs exceed the unchanged source snapshot cap")


def verifier_rows() -> list[dict[str, Any]]:
    return [
        {
            "id": INDEPENDENT_Q2,
            "program": "devtools.ryxu_radical_n51.independent",
            "author": "Squares Project (Levy)",
            "provenance": "first-party",
            "language": ["Python"],
            "methods": ["exact-algebraic"],
            "role": "decides",
            "source": ["packing/devtools/ryxu_radical_n51.py"],
            "summary": (
                "Decides all 51 undilated coefficient poses in Q(sqrt2), unit-square "
                "identities, containment and all 1275 unordered pairs."
            ),
            "note": (
                "Rational-pair scalar order and direct axis/diamond corners are distinct "
                "from native number-field materialization and geometry. The reviewed source "
                "input is shared. Complete positive, duplicate and outside outcomes are "
                "retained; 119 touching and 1156 strict pairs are observed, while the "
                "source's 191-touching-pair assertion remains unconfirmed."
            ),
        },
        {
            "id": CUSTODY,
            "program": "devtools.ryxu_house_links",
            "author": "Squares Project (Levy)",
            "provenance": "first-party",
            "language": ["Python"],
            "methods": ["exact-algebraic"],
            "role": "premises",
            "source": [
                "packing/devtools/ryxu_arrangement_reports.py",
                "packing/devtools/ryxu_radical_n51.py",
                "packing/devtools/ryxu_house_links.py",
                "packing/devtools/evand_arrangement_reports.py",
            ],
            "summary": (
                "Admits complete pinned source facts, all 75 rational and three radical "
                "actual input/result jobs, required controls and all 18 complete houses."
            ),
            "note": (
                "Admission reconciles retained executions and private-worker scientific "
                "inputs. It executes no geometric predicate and does not itself confer "
                "a confirmation rung."
            ),
        },
    ]


def confirming_evidence(*, radical: bool) -> dict[str, Any]:
    return {
        "id": RADICAL if radical else RATIONAL,
        "claim": "upper-bound",
        "scope": {"n_values": [51] if radical else list(houses.reports.NUMBERS)},
        "assurance": "verified",
        "method": "exact-algebraic",
        "performed_by": "repository",
        "relationship_to_generator": "independent-implementation",
        "origin": "replayed-here",
        "novelty": "previously-published",
        "source_key": houses.SOURCE_KEY,
        "certificate": (
            "packing/resources/web/ry-xu-new-packings-2026-10-08/facts/"
            + ("n051-undilated-record.json.xz" if radical else "complete-certificates.json.xz")
        ),
        "replay": (
            "From packing with project Python 3.14: python -m devtools.ryxu_radical_n51 "
            "check --replay. This runs all three complete native and independent jobs and "
            "compares full results with retained actual outcomes."
            if radical
            else (
                "From packing with project Python 3.14: python -m "
                "devtools.ryxu_arrangement_reports check --replay. This runs all 75 complete "
                "jobs through both native routes and compares full retained outcomes."
            )
        ),
        "replay_status": "passed",
        "verifiers": [
            "V-sqpack-verify",
            INDEPENDENT_Q2 if radical else "V-check-rational-witness-independent",
            CUSTODY,
        ],
        "independence_record": REVIEW,
        "limitations": (
            (
                "All three full 51-square jobs accept the positive and reject duplicate "
                "and outside controls in both routes; 7650 pair decisions, original batch "
                "wall 18.707450165995397s. A scoped independent review repeated complete "
                "inputs and outcomes. The admitted exact side is (16+5sqrt(2))/3, with "
                "polynomial 9s^2-96s+206=0, a feasible construction ceiling. Native and "
                "independent routes observe 119 touching/1156 strict pairs; the source's "
                "191 assertion remains unconfirmed."
                if radical
                else (
                    "All 25 complete rational source certificates pass both routes. Eight "
                    "rational certificates are non-selected in the current atlas, including "
                    "the separate rational n51; all remain retained. Each of 50 duplicate and "
                    "outside full-roster controls fails both. The 75-job batch retained "
                    "2078082 pair decisions and wall 330.19143345800694s. Shared exact "
                    "half-angle conversion was independently reviewed; deciding geometry "
                    "implementations are distinct. The source dilation is already baked "
                    "into each rational input; no further dilation or rounding is applied. "
                    "Rational n51 is separate from the selected undilated radical witness."
                )
            )
            + (
                " Complete source/result/house binding, private-worker copied inputs, "
                "mutation refusals, producer guards and original-frontier recovery were "
                "independently reviewed. Offline admission is not a fresh deciding replay. "
                "Only finite feasibility enters: no optimality, lower bound, local-minimum "
                "theorem, rigidity, novelty, formal proof or human oversight is established."
            )
        ),
        "external_review": {
            "state": "informally-verified",
            "date": register.DAY,
            "reviewed_by": "GPT-6 Astra separately prompted ry-xu integration review",
            "note": "Accepted finite scientific feasibility and production custody only.",
        },
        "source_reviewed": register.DAY,
    }


def case_plan() -> list[tuple[Path, str]]:
    """Prepare the complete case roster before any registry or frontier write."""
    plan = []
    for n in houses.NUMBERS:
        path = register.FRONTIER / f"n-{n:03d}.md"
        houses.reports.ensure_private(path)
        prefix, front, body = path.read_text().split("---\n", 2)
        document = safe_load(front)
        case = document["packing"]
        if case["n"] != n or case["reported_upper_bound"] != register.reported_bound(n):
            raise ValueError("selected source upper lane differs from complete admitted facts")
        confirming = RADICAL if n == 51 else RATIONAL
        case["verified_upper_bound"] = houses.bound(n)
        if confirming not in case["evidence"]:
            case["evidence"].append(confirming)
        reported = register.RADICAL_REPORT if n == 51 else register.REPORT
        case["blockers"] = [
            block
            for block in register.remaining_blockers(case)
            if not (
                reported in block["evidence"] and "Issue432 remains V0/C0" in block["detail"]
            )
        ]
        pattern = rf"\n{register.SECTION}\n.*?(?=\n## |\n<!-- This document follows)"
        body, count = re.subn(
            pattern,
            lambda _match, n=n: register.section(n, confirmed=True),
            body,
            flags=re.DOTALL,
        )
        if count != 1:
            raise ValueError(
                "selected case needs exactly one source-bound construction section"
            )
        body = register.historical_upper_prose(n, body)
        plan.append((path, prefix + "---\n" + dump(document) + "---\n" + body))
    return plan


def publish(path: Path, text: str) -> None:
    """Keep an admitted idempotent retry from rewriting unchanged retained records."""
    if path.read_text() != text:
        save(path, text)


def replace_coverage_source(row: dict[str, Any]) -> None:
    """Replace one source without consuming the following top-level coverage sections."""
    from devtools.source_supersession import coverage_list_span  # noqa: PLC0415

    path = register.FRONTIER / "source-coverage.yaml"
    text = path.read_text()
    span = coverage_list_span(text, "sources", identifier=row["id"])
    if span is None:
        raise ValueError("expected retained ry-xu coverage source")
    start, end = span
    first_line = text[start:].splitlines()[0]
    indent = first_line[: len(first_line) - len(first_line.lstrip(" "))]
    rendered = "".join(indent + line for line in dump([row]).splitlines(keepends=True))
    publish(path, text[:start] + rendered + text[end:])


def confirm() -> None:
    admit_confirmation()
    plan = case_plan()
    append_rows(register.FRONTIER / "verifiers.yaml", "verifiers", verifier_rows(), "id")
    for radical, result_id in ((False, "T-125"), (True, "T-126")):
        evidence = confirming_evidence(radical=radical)
        evidence_path = register.FRONTIER / "evidence.yaml"
        append_rows(evidence_path, "evidence", [evidence], "id")
        retained = next(
            row
            for row in safe_load(evidence_path.read_text())["evidence"]
            if row["id"] == evidence["id"]
        )
        if retained != evidence:
            replace_row(evidence_path, "evidence", evidence)
        rows = safe_load((register.FRONTIER / "results.yaml").read_text())["results"]
        result = next(row for row in rows if row["id"] == result_id)
        original = copy.deepcopy(result)
        result.update(verification="V3", confirmation="C3")
        if not radical:
            result["significance"]["rationale"] = (
                "Rational certificates improve the pre-intake ceilings at 18 counts; "
                "17 are currently selected alongside separate radical n51. No solved "
                "case or lower-bound theorem."
            )
        result["claim"] = (
            "Complete independently reviewed exact replay confirms the undilated "
            "51-square construction ceiling s(51) <= (16+5sqrt(2))/3. This is finite "
            "feasibility, not equality with the optimum or the unconfirmed source "
            "contact count."
            if radical
            else (
                "Complete independently reviewed exact replay confirms finite feasibility "
                "of all 25 rational source certificates. Superseded configurations retain "
                "their complete inputs and outcomes; no optimality or local-minimum theorem."
            )
        )
        if evidence["id"] not in result["evidence"]:
            result["evidence"].append(evidence["id"])
        result["controls"] = [
            "packing/resources/web/ry-xu-new-packings-2026-10-08/receipts/"
            + ("n051-radical-positive.json.xz" if radical else "exact-certification.json.xz"),
            "packing/tests/test_ryxu_house_links.py",
            "packing/tests/test_ryxu_radical_n51.py"
            if radical
            else "packing/tests/test_ryxu_arrangement_reports.py",
        ]
        result["reviews"] = [
            {
                "path": REVIEW,
                "kind": "adversarial",
                "reviewer": "GPT-6 Astra ry-xu integration reviewer",
                "reviewer_kind": "ai",
                "relation": "project",
                "date": register.DAY,
                "scope": (
                    "Complete finite geometry, actual deciding inputs/results, required "
                    "controls, exact presentation, private-worker custody and safe adoption."
                ),
                "verdict": "accepted",
                "covers": [result_id],
            }
        ]
        result["next_rung"] = (
            "C4 requires two distinct accepted confirming adversarial reviews and an actual "
            "human oversight record; neither drawing nor admission supplies them."
        )
        if result != original:
            replace_row(register.FRONTIER / "results.yaml", "results", result)
    evidence_rows = {
        row["id"]: row
        for row in safe_load((register.FRONTIER / "evidence.yaml").read_text())["evidence"]
    }
    verifiers = verifier_registry.load(register.FRONTIER / "verifiers.yaml")
    for path, text in plan:
        case = safe_load(text.split("---\n", 2)[1])["packing"]
        section = register.render_case_verifiers.section(case, evidence_rows, verifiers)
        publish(path, register.render_case_verifiers.place(text, section))
    coverage = register.FRONTIER / "source-coverage.yaml"
    text = coverage.read_text()
    value = safe_load(text)
    for source in value["sources"]:
        if source["id"] not in {houses.SOURCE_ID, houses.RADICAL_SOURCE_ID}:
            continue
        if source["id"] == houses.SOURCE_ID:
            source["notes"] = (
                "All 25 full rational source geometries retained. The current atlas "
                "selects 17 rational certificates plus the separate undilated radical "
                "n51 construction; eight rational certificates are non-selected. "
                "No 191-contact assertion admitted."
            )
        confirming = RADICAL if source["id"] == houses.RADICAL_SOURCE_ID else RATIONAL
        if confirming not in source["evidence"]:
            source["evidence"].append(confirming)
        replace_coverage_source(source)
    value = safe_load(coverage.read_text())
    start = coverage.read_text().index("selected_overrides:")
    end = coverage.read_text().index("superseded_reports:", start)
    for row in value["selected_overrides"]:
        if row["source_id"] not in {houses.SOURCE_ID, houses.RADICAL_SOURCE_ID}:
            continue
        row["evidence"] = register.RADICAL_REPORT if row["n"] == 51 else register.REPORT
        row["reason"] = (
            "Smaller exact finite construction confirmed after scoped replay/custody review."
        )
    rendered = "".join(
        "  " + line for line in dump(value["selected_overrides"]).splitlines(keepends=True)
    )
    text = coverage.read_text()
    publish(coverage, text[:start] + "selected_overrides:\n" + rendered + text[end:])


def main() -> None:
    argparse.ArgumentParser(description=__doc__, allow_abbrev=False).parse_args()
    confirm()


if __name__ == "__main__":
    main()
