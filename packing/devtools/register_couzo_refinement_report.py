"""Register all eight #451 source claims without changing selected cases or assurance.

Complete native outcomes and actual private-worker custody are retained artifacts.
Historical source-house integration and record review remain required before adoption.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from jsonschema_rs import Draft202012Validator

from devtools import couzo_refinement_reports as reports
from devtools.register_refinement_reports import FOOTER, dump, save
from devtools.source_supersession import coverage_list_span
from sqpack.yamlio import safe_load

REPO = reports.REPO
DAY = "2026-10-08"
RESULT = "T-128"
REPORT = "E-couzo-451-rational-report"
SOURCE_ID = "couzo-451-exact-refinements"
PACKET_PATH = reports.PACKET.relative_to(REPO).as_posix()
DISCLOSURE = (
    "The source author copied this repository's sqpack verifier, so the exact_verify "
    "route overlaps that source checker. The second maintained rational-geometry "
    "route is a separate deciding implementation; both routes share certificate "
    "parsing, half-angle conversion, Fraction arithmetic and the separating-axis "
    "method. No two independent methods, human oversight or optimality is claimed."
)


def rows() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    scope = {"n_values": list(reports.NUMBERS)}
    evidence = {
        "id": REPORT,
        "claim": "upper-bound",
        "scope": scope,
        "assurance": "reported",
        "reported_method": "exact-algebraic",
        "performed_by": "source-author",
        "relationship_to_generator": "same-implementation",
        "origin": "external",
        "novelty": "previously-published",
        "source_key": reports.SOURCE_KEY,
        "certificate": PACKET_PATH + "/facts/complete-certificates-and-decimal-poses.json.xz",
        "replay_status": "not-attempted",
        "verifiers": [],
        "source_reviewed": DAY,
        "limitations": (
            "This atom records the source author's report. A separate complete "
            "repository replay is retained: eight positives and sixteen controls "
            "on both routes passed their required outcomes in 398.40 seconds. "
            "Actual production private-worker custody passed all complete-input and "
            "mutation-restoration checks without geometric deciders. Historical "
            "source-house integration and confirmation remain pending. " + DISCLOSURE
        ),
    }
    result = {
        "id": RESULT,
        "kind": "upper-bound",
        "registered": DAY,
        "headline": "Eight complete rational refinements from Francisco Couzo",
        "claim": (
            "Eight complete rational source certificates report finite upper-bound "
            "improvements at 105,108,127,131,155,180,228,306. Complete native feasibility "
            "outcomes are retained separately; selected standing cases are unchanged "
            "pending historical source-house integration and record review."
        ),
        "scope": scope,
        "verification": "V0",
        "confirmation": "C0",
        "significance": {
            "score": 3,
            "rationale": "Eight smaller finite construction sides; no lower bound or optimum.",
            "scored": DAY,
            "by": "think-edo8 Couzo refinement import",
        },
        "novelty": "previously-published",
        "attribution": {"source_keys": [reports.SOURCE_KEY], "published": DAY},
        "evidence": [REPORT],
        "artifacts": [
            PACKET_PATH + "/README.md",
            PACKET_PATH + "/acquisition/case-inputs.json",
            PACKET_PATH + "/facts/complete-certificates-and-decimal-poses.json.xz",
            PACKET_PATH + "/receipts/exact-certification.json.xz",
            PACKET_PATH + "/receipts/exact-replay-incomplete-62268899-v1.json.xz",
            PACKET_PATH + "/receipts/execution-attempts.json",
            PACKET_PATH + "/receipts/private-custody-668cc1a-v1.json",
            "packing/devtools/couzo_refinement_reports.py",
        ],
        "controls": [
            "packing/tests/test_couzo_refinement_reports.py",
            "packing/tests/test_couzo_custody.py",
            "packing/tests/test_negative_controls.py",
        ],
        "notes": (
            "All sixteen complete original factual files and all 24 native jobs are "
            "retained. The first two-worker attempt was incomplete after 181.19 seconds; "
            "the fresh serial attempt passed in 398.40 seconds (6.64 wall minutes, "
            "4.1025 CPU minutes) with unchanged 45-second children.\n\nThe actual private "
            "worker passed complete stored-input admission, six late mutations and "
            "restoration checks without geometric deciders: 8.91 seconds call, "
            "26.72 seconds setup and 38.36 seconds total. The call fits the unchanged "
            "12-second fast ceiling; the child deadline remains 45 seconds.\n\n" + DISCLOSURE
        ),
        "next_rung": (
            "Preserve and validate each complete historical source house before any "
            "selected-house replacement, then independently review source-specific "
            "adoption and confirming records. Final exact-head CI remains required."
        ),
    }
    source = {
        "id": SOURCE_ID,
        "title": "Francisco Couzo's eight rational refinements, issue451",
        "role": "source-repository",
        "url": reports.SOURCE + "/tree/" + reports.REVISION,
        "local": reports.PACKET.relative_to(REPO / "packing").as_posix(),
        "source_key": reports.SOURCE_KEY,
        "scope": scope,
        "reviewed": DAY,
        "source_date": DAY,
        "disposition": "current-report",
        "replay_disposition": "case-specific",
        "represented_by": [
            "frontier/results.yaml",
            reports.fact_path().relative_to(REPO / "packing").as_posix(),
        ],
        "evidence": [REPORT],
        "notes": (
            "All eight complete claims and their exact sides remain in pinned factual "
            "inputs; T-128 records the aggregate source report. All 24 native jobs "
            "have full outcomes. No selected override or superseded claim is created "
            "at this source-only stage; current cases and earlier source ownership "
            "remain unchanged. Actual private-worker custody passed; historical owner "
            "integration, adoption and confirmation remain pending."
        ),
    }
    request = {
        "number": 451,
        "title": "105, 108, 127, 131, 155, 180, 228, 306: registration request",
        "author": "franciscouzo",
        "opened": DAY,
        "state": "open",
        "kind": "result-report",
        "triage": "done",
        "summary": (
            "All eight complete source certificates and decimal context poses are "
            "retained. The complete 24-job native finite-feasibility replay passed; "
            "actual private-worker custody passed without geometric deciders. "
            "Historical source-house integration and confirmation remain pending."
        ),
        "read_through": "2026-10-08T15:53:07Z",
        "results": [
            {
                "key": "eight-rational-refinements",
                "claim": result["claim"],
                "source": "body",
                "register": [RESULT],
            }
        ],
        "asks": [
            {
                "what": (
                    "Credit the constructions and refinement tools identified by the source."
                ),
                "state": "done",
                "note": (
                    "Complete source lineage is retained in the packet, T-128 notes and "
                    "bibliography; current selected construction credits remain unchanged."
                ),
            }
        ],
        "beads": ["think-edo8"],
        "answer_bead": "think-edo8",
        "replies": [],
        "close_when": (
            "The supported import and disposition are on main and the owner posts "
            "the resulting state; optimizer and local/global optimality remain separate claims."
        ),
    }
    return evidence, result, source, request


def append(text: str, field: str, row: dict[str, Any], key: str) -> str:
    """Append one row after parsed list content without changing prior rows or comments."""
    existing = safe_load(text)[field]
    matches = [item for item in existing if item[key] == row[key]]
    if len(matches) > 1:
        raise ValueError("duplicate existing source/report identity")
    if matches:
        if key == "id" and matches[0].get("scope") != row.get("scope"):
            raise ValueError("existing source/report scope differs")
        return text
    span = coverage_list_span(text, field)
    if span is None:
        raise ValueError("required registry list missing")
    start, end = span
    block = text[start:end]
    first = re.search(r"^([ ]*)- ", block, re.MULTILINE)
    if first is None:
        raise ValueError("existing nonempty block registry list required")
    indent = first.group(1)
    addition = "".join(
        indent + line if line.strip() else line
        for line in dump([row]).splitlines(keepends=True)
    )
    return text[:end].rstrip() + "\n" + addition + text[end:]


def validate(path: Path, text: str) -> None:
    reports.ensure_private(path)
    doc = safe_load(text)
    meta = doc["softschema"]
    schema = path.parent / meta["schema"]
    reports.ensure_private(schema)
    if meta["status"] != "enforced":
        raise ValueError("enforced source record contract required")
    payload = {key: value for key, value in doc.items() if key != "softschema"}
    if not Draft202012Validator(safe_load(schema.read_text())).is_valid(payload):
        raise ValueError("source-report output schema differs: " + path.name)


def plan() -> list[tuple[Path, str]]:
    """Admit complete inputs and every proposed record before the first write."""
    reports.check_certification()
    evidence, result, source, request = rows()
    items = []
    for relative, field, row, key in (
        ("packing/frontier/evidence.yaml", "evidence", evidence, "id"),
        ("packing/frontier/results.yaml", "results", result, "id"),
        ("packing/frontier/source-coverage.yaml", "sources", source, "id"),
        ("packing/campaign/result-requests.yaml", "issues", request, "number"),
        (
            "packing/resources/bibliography.yaml",
            "sources",
            {
                "key": reports.SOURCE_KEY,
                "authors": ["Couzo"],
                "year": 2026,
                "venue": "GitHub",
                "dated": DAY,
                "lineage": "builds-on-project",
                "credit": "Couzo after Xu, Chaoweeraprasit, Gupta, Ellsworth, Daniel",
                "short_credit": "Couzo after Xu et al.",
                "note": (
                    "Eight complete certificates and decimal context poses at "
                    + reports.REVISION
                    + "; source credits and tools are attributed. "
                    "No optimizer/local/global claims. "
                    "Unlicensed programs/prose are pinned rather than copied."
                ),
            },
            "key",
        ),
    ):
        path = REPO / relative
        reports.ensure_private(path)
        text = append(path.read_text(), field, row, key)
        validate(path, text)
        items.append((path, text))
    index = REPO / "packing/resources/README.md"
    reports.ensure_private(index)
    text = index.read_text()
    marker = "**" + reports.SOURCE_KEY + "**"
    if marker not in text:
        if text.count(FOOTER) != 1:
            raise ValueError("one resources guideline footer required")
        entry = (
            "- " + marker + " — Francisco Couzo's eight complete rational certificates "
            "and separate decimal context poses; T-128 remains V0/C0 pending historical "
            "source-house integration and confirmation. All 24 native jobs completed "
            "their finite-feasibility "
            "and control outcomes in 6.64 wall minutes; actual private-worker custody "
            "passed complete stored-input and mutation-restoration checks. [Factual packet]"
            "(web/couzo-exact-refinements-2026-10-08/README.md). "
            "Ryan Xu, Nate Chaoweeraprasit, Siddharth Gupta, David Ellsworth and Evan Daniel "
            "receive the source's construction/refinement credits; "
            "no optimality is asserted.\n\n"
        )
        text = text.replace(FOOTER, entry + FOOTER)
    items.append((index, text))
    return items


def register() -> None:
    proposed = plan()
    for path, text in proposed:
        if path.read_text() != text:
            save(path, text)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    register()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
