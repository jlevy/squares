# ruff: noqa: RUF001 -- generated record prose follows the project's typography.
"""Register the pinned #425/#428 finite-witness reports without promoting assurance."""

from __future__ import annotations

import argparse
import copy
import re
from pathlib import Path
from typing import Any

import yaml

from devtools import refinement_packets as packets
from sqpack.yamlio import safe_load

REPO = packets.REPO
FRONTIER = REPO / "packing/frontier"
DAY = "2026-10-07"
RETRIEVED = "2026-10-08"
FOOTER = (
    "<!-- This document follows common-doc-guidelines.md.\n"
    "See github.com/jlevy/practical-prose and review guidelines before editing.\n-->\n"
)


def dump(value: Any) -> str:
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True, width=96)


def save(path: Path, text: str) -> None:
    packets.save(path, text.encode())


def append_rows(path: Path, field: str, rows: list[dict[str, Any]], key: str) -> None:
    """Append new canonical rows while preserving unrelated comments and formatting."""
    text = path.read_text()
    existing = safe_load(text)[field]
    new = [row for row in rows if not any(item[key] == row[key] for item in existing)]
    if not new:
        return
    start = re.search(rf"^{field}:\s*$", text, re.MULTILINE)
    if start is None:
        raise ValueError(f"missing {field} list")
    after = re.search(r"^[a-z_]+:", text[start.end() :], re.MULTILINE)
    end = start.end() + after.start() if after else len(text)
    first = re.search(r"^([ ]*)- ", text[start.end() : end], re.MULTILINE)
    indent = first.group(1) if first is not None else "  "
    rendered = "".join(
        indent + line if line.strip() else line for line in dump(new).splitlines(keepends=True)
    )
    save(path, text[:end].rstrip() + "\n" + rendered + text[end:])


def report_id(source: packets.Source) -> str:
    return f"E-{source.packet_name}-report"


def record_case(source: packets.Source, n: int, result: str) -> dict[str, Any]:
    path = FRONTIER / f"n-{n:03d}.md"
    _prefix, front, body = path.read_text().split("---\n", 2)
    document = safe_load(front)
    case = document["packing"]
    facts = packets.read_fact(source, n)
    value = packets.exact_decimal(facts["side"])
    if case["reported_upper_bound"]["source_key"] == source.key:
        return {}
    prior = {
        "n": n,
        "reported": copy.deepcopy(case["reported_upper_bound"]),
        "verified": copy.deepcopy(case["verified_upper_bound"]),
        "rigidity": copy.deepcopy(case["rigidity"]),
    }
    bound = case["reported_upper_bound"]
    bound.update(
        value=value,
        exact_form=facts["side"],
        algebraic_degree=1,
        minimal_polynomial=None,
        analytically_optimized=None,
        catalogue_rigid="not-stated",
        construction_method="unknown",
        tilt_angles_deg=None,
        found_by=["Francisco Couzo"],
        found_year=2026,
        improved_by=["Seth Rehwaldt"],
        catalogue_pictured=False,
        source_key=source.key,
        source_date=DAY,
        retrieved_date=RETRIEVED,
        witnesses=[f"W-known-best-n{n:03d}"],
        evidence=[report_id(source)],
    )
    case["rigidity"] = None
    case["conjectured_optimum"] = None
    case["source_reviewed"] = RETRIEVED
    case["evidence"].append(report_id(source))
    case["resources"].insert(
        0,
        {
            "key": source.key,
            "role": "upper-bound-report",
            "local": f"web/{source.packet_name}",
            "url": f"https://github.com/{source.repository}/tree/{source.revision}",
            "retrieved": True,
        },
    )
    case["priority_notes"].append(
        {
            "claim": (
                f"Earlier reported ceiling {prior['reported']['value']} "
                f"from {prior['reported']['source_key']}; earlier construction "
                "and exact verification evidence remain historical."
            ),
            "claimed_by": prior["reported"]["found_by"],
            "published": None,
            "year": prior["reported"]["found_year"],
        }
    )
    case["blockers"].append(
        {
            "kind": "mathematics",
            "detail": (
                f"The #{source.issue} refinement remains reported at V0/C0 pending "
                "complete replay admission and scoped mathematical review. "
                "Drawing feasibility is separate from result confirmation."
            ),
            "evidence": [report_id(source)],
        }
    )
    old_heading = re.search(r"\n## ", body)
    if old_heading:
        opening = body[: old_heading.start()]
        body = (
            opening.replace(
                "Open. The best known published packing",
                "Before the 7 October refinement, the best known published packing",
            )
            + body[old_heading.start() :]
        )
    section = (
        f"\n## The 7 October rational refinement\n\n"
        f"Seth Rehwaldt reports the finite rational witness ({result}) at exact side\n"
        f"${facts['side']}$, whose complete terminating decimal is ${value}$.\n"
        f"The [pinned source](../resources/web/{source.packet_name}/README.md) refines\n"
        "Francisco Couzo’s existing construction with disclosed OpenAI Codex assistance.\n"
        "This is a reported feasible ceiling, with local replay admission and scoped review\n"
        "pending. The earlier verified ceiling remains in the verified lane.\n"
        "No unrestricted lower bound, optimality or rigidity claim is added.\n"
        "The earlier rigidity screen belongs to the earlier geometry and is preserved\n"
        "in the packet’s prior-state record; this refinement’s rigidity is unassessed.\n"
    )
    if source.issue == 428:
        section += (
            "\nThe exact side is below Daniel’s retained rational ceiling even though an\n"
            "18-place upward-rounded display is larger. The full rational and terminating\n"
            "decimal, rather than that rounded display, determine this comparison.\n"
        )
    body = body.replace(FOOTER, section + "\n" + FOOTER)
    save(path, "---\n" + dump(document) + "---\n" + body)
    return prior


def register(source: packets.Source, result: str) -> None:
    evidence = report_id(source)
    prior = [record_case(source, n, result) for n in source.numbers]
    prior = [row for row in prior if row]
    if prior:
        save(source.packet / "acquisition/prior-state.json", packets.json_bytes(prior).decode())
    append_rows(
        FRONTIER / "evidence.yaml",
        "evidence",
        [
            {
                "id": evidence,
                "claim": "upper-bound",
                "scope": {"n_values": list(source.numbers)},
                "assurance": "reported",
                "reported_method": "exact-algebraic",
                "performed_by": "source-author",
                "relationship_to_generator": "same-implementation",
                "origin": "external",
                "novelty": "previously-published",
                "source_key": source.key,
                "certificate": f"packing/resources/web/{source.packet_name}/facts/",
                "replay_status": "not-attempted",
                "verifiers": [],
                "limitations": (
                    "Source-reported finite rational witnesses for existing constructions. "
                    "Center-expansion metadata describes repair already applied; no "
                    "additional expansion is performed. Source checker reports are external "
                    "claims. No unrestricted lower-bound, optimality, rigidity or "
                    "human-oversight assurance is admitted."
                ),
                "source_reviewed": RETRIEVED,
            }
        ],
        "id",
    )
    append_rows(
        FRONTIER / "results.yaml",
        "results",
        [
            {
                "id": result,
                "kind": "upper-bound",
                "registered": DAY,
                "headline": (
                    "Exact rational ceiling refinements at n = "
                    f"{', '.join(map(str, source.numbers))}"
                ),
                "claim": (
                    "Seth Rehwaldt reports finite rational upper-bound refinements of "
                    "existing Couzo constructions at n = "
                    f"{', '.join(map(str, source.numbers))}. The complete exact sides "
                    "and ordered rosters are retained as reported; no optimality "
                    "claim is registered."
                ),
                "scope": {"n_values": list(source.numbers)},
                "verification": "V0",
                "confirmation": "C0",
                "significance": {
                    "score": 2,
                    "rationale": (
                        "Certificate refinements of existing constructions; tiny exact "
                        "improvements over newer retrieved certificates, with no solved "
                        "case or new arrangement."
                    ),
                    "scored": DAY,
                    "by": "think-f3dl / think-v42c import lane (repository)",
                },
                "novelty": "previously-published",
                "attribution": {"source_keys": [source.key], "published": DAY},
                "evidence": [evidence],
                "artifacts": [
                    f"packing/resources/web/{source.packet_name}/README.md",
                    "packing/devtools/refinement_packets.py",
                    *[f"packing/frontier/n-{n:03d}.md" for n in source.numbers],
                ],
                "next_rung": (
                    "Complete replay admission, two mutant refusals per accepted checker, "
                    "durable receipts and mapped mathematical review are required before "
                    "confirmation. The current complete-roster drawing check assigns "
                    "no result rung."
                ),
                "notes": (
                    "Refinement work by Seth Rehwaldt with OpenAI Codex assistance; Couzo "
                    "and earlier construction contributors retain credit. All prior "
                    "verified ceilings, sources and receipts remain historical. "
                    "Restricted analytic claims are outside this import."
                ),
                "composition": (
                    "The exact half-angle map gives unit frames; translating each already "
                    "repaired source center by S/2 gives the lower-left frame. The complete "
                    "rational side is authoritative and no coordinate or side is rounded."
                ),
            }
        ],
        "id",
    )
    append_rows(
        FRONTIER / "source-coverage.yaml",
        "sources",
        [
            {
                "id": source.packet_name,
                "title": f"Rehwaldt finite rational refinements, issue {source.issue}",
                "role": "source-repository",
                "url": f"https://github.com/{source.repository}/tree/{source.revision}",
                "local": f"resources/web/{source.packet_name}/",
                "source_key": source.key,
                "scope": {"n_values": list(source.numbers)},
                "reviewed": RETRIEVED,
                "source_date": DAY,
                "disposition": "current-report",
                "replay_disposition": "case-specific",
                "represented_by": [f"frontier/n-{n:03d}.md" for n in source.numbers],
                "evidence": [evidence],
                "claims_record": f"resources/web/{source.packet_name}/acquisition/claims.json",
                "notes": (
                    "Complete terminating displays preserve the full rational strict "
                    "improvement. Only reported assurance is admitted; historical counts "
                    "excluded by the author do not replace smaller ceilings."
                ),
            }
        ],
        "id",
    )
    coverage = FRONTIER / "source-coverage.yaml"
    text = coverage.read_text()
    for old in prior:
        n = old["n"]
        pattern = rf"(?m)^  - n: {n}\n.*?(?=^  - n:|^superseded_reports:)"
        selected = re.search(pattern, text, re.DOTALL)
        if selected is None:
            raise ValueError("expected selected override is missing")
        row = {
            "n": n,
            "source_id": source.packet_name,
            "value": packets.exact_decimal(packets.read_fact(source, n)["side"]),
            "evidence": evidence,
            "reason": (
                "Smaller exact finite rational source ceiling, retained as reported "
                "pending replay admission and review."
            ),
        }
        replacement = "".join("  " + line for line in dump([row]).splitlines(keepends=True))
        text = text[: selected.start()] + replacement + text[selected.end() :]
        old_row = safe_load(selected.group())[0]
        old_row.pop("reason", None)
        old_row.pop("evidence", None)
        old_row.update(
            superseded_by=source.packet_name,
            reason="Historical ceiling; the selected exact rational report is smaller.",
        )
        # Superseded reports need no unique identifier; append before the next field.
        marker = re.search(r"^beyond_horizon_claims:", text, re.MULTILINE)
        if marker is None:
            raise ValueError("coverage lacks its beyond-horizon boundary")
        rendered = "".join("  " + line for line in dump([old_row]).splitlines(keepends=True))
        text = text[: marker.start()].rstrip() + "\n" + rendered + text[marker.start() :]
    save(coverage, text)
    append_rows(
        REPO / "packing/resources/bibliography.yaml",
        "sources",
        [
            {
                "key": source.key,
                "authors": ["Rehwaldt"],
                "year": 2026,
                "venue": "GitHub",
                "dated": DAY,
                "credit": "Rehwaldt after Couzo and earlier contributors",
                "lineage": "independent",
                "note": (
                    f"Seth Rehwaldt’s exact certificate refinement at {source.revision}, "
                    f"issue {source.issue}, with OpenAI Codex assistance. No new arrangement "
                    "or unrestricted optimality claim. Normalized geometric facts and "
                    "attributed source custody are retained; source notices assign "
                    "no blanket licence."
                ),
            }
        ],
        "key",
    )
    bibliography = REPO / "packing/resources/bibliography.yaml"
    if "  Seth Rehwaldt: Rehwaldt\n" not in bibliography.read_text():
        save(
            bibliography,
            bibliography.read_text().replace(
                "credited_names:\n", "credited_names:\n  Seth Rehwaldt: Rehwaldt\n"
            ),
        )


def main() -> None:
    argparse.ArgumentParser(description=__doc__, allow_abbrev=False).parse_args()
    register(packets.COUZO, "T-117")
    register(packets.N68, "T-118")


if __name__ == "__main__":
    main()
