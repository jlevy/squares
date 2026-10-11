"""Adopt #399's separately certified poses while preserving every historical import layer."""

from __future__ import annotations

import argparse
import copy
import json
import re
from decimal import Decimal
from typing import Any

from devtools import evand_arrangement_reports as reports
from devtools import register_refinement_reports as registry
from devtools.check_case_prose import sentence_spans
from sqpack.yamlio import safe_load

REPO = reports.REPO
FRONTIER = REPO / "packing/frontier"
REPORT_EVIDENCE = "E-evand-399-new-arrangements-report"
RESULT = "T-119"
DAY = "2026-10-07"
REVIEW = "docs/project/reviews/review-2026-10-08-evand-new-arrangements.md"


def adopt_case(n: int, existing: str, generated: str | None = None) -> str:
    """Keep historical pose claims separate; ordinary lower lanes follow their generator."""
    certificate = reports.read_fact(n)
    verified = reports.confirmed_bound(n)
    document = safe_load(existing.split("---\n", 2)[1])
    body = existing.split("---\n", 2)[2]
    case = document["packing"]
    selected = case["reported_upper_bound"]["source_key"] == reports.SOURCE_KEY
    if not selected:
        heading = re.search(r"^# .*\n", body, re.MULTILINE)
        if heading is None:
            raise reports.ReportError("case requires its existing title")
        header, body = body[: heading.end()], body[heading.end() :]
        old = copy.deepcopy(case["reported_upper_bound"])
        case["priority_notes"].append(
            {
                "claim": (
                    f"Earlier reported ceiling {old['value']} from {old['source_key']}; "
                    "its finder, polynomial, poses, certificates and rigidity screen remain "
                    "historical, separately preserved in the #399 prior-state archive."
                ),
                "claimed_by": old["found_by"],
                "published": old["source_date"],
                "year": old["found_year"],
            }
        )
        case["rigidity"] = None
        case["conjectured_optimum"] = None
        case["resources"].insert(
            0,
            {
                "key": reports.SOURCE_KEY,
                "role": "formal-certificate",
                "local": "web/evand-new-arrangements-2026-10-07",
                "url": f"{reports.SOURCE}/tree/{reports.REVISION}",
                "retrieved": True,
            },
        )
        for start, end in reversed(sentence_spans(body)):
            sentence = body[start:end]
            if re.search(rf"s\({n}\)\s*\\le\s*[0-9.]+", sentence):
                leading = len(sentence) - len(sentence.lstrip())
                body = (
                    body[:start]
                    + sentence[:leading]
                    + "Previously, "
                    + sentence[leading:]
                    + body[end:]
                )
        body = re.sub(
            r"`verified_upper_bound`\s+for\s+this\s+case\s+is",
            "the earlier verified ceiling was",
            body,
        )
        body = re.sub(
            r"[Tt]he verified upper bound is", "The earlier verified ceiling was", body
        )
        body = body.replace("\n## The packing\n", "\n## The earlier packing\n")
        opening = (
            f"\n**New exact construction, 7 October 2026.** The complete #399 certificate "
            f"proves $s({n}) \\le {verified['value']}$ ({RESULT}). "
            "The display is the least upward sixteen-place ceiling of the full rational side. "
            "It replaces the atlas pose; earlier source reports and certifications below "
            "describe their original, different geometries.\n\n"
        )
        body = header + opening + body
        section = (
            "\n## The three new arrangements\n\n"
            "Evan Daniel supplies this complete rational centre/half-angle packing "
            "at exact side "
            f"${reports.legacy.literal(certificate.side)}$. "
            "Both independent project implementations accept every square, wall and pair; "
            "both reject complete-roster duplicate-square and outside-container controls. "
            "The full inputs and native results are retained in the "
            "[separate packet](../resources/web/evand-new-arrangements-2026-10-07/README.md). "
            "A separately prompted mathematical review independently reran all nine jobs. "
            "This establishes feasible upper bounds at V3/C3. Arrangement novelty, KKT, "
            "local minimality, rigidity, global optimality and human "
            "oversight are not established. "
            "The earlier #375 source namespace and T-098/T-101 certificates remain unchanged.\n"
        )
        body = body.replace(registry.FOOTER, section + "\n" + registry.FOOTER)
    body = body.replace("Previously, The", "Previously, the").replace(
        "Previously, That", "Previously, that"
    )
    body = body.replace("\n## The exact certificate\n", "\n## The earlier exact certificate\n")
    body = body.replace("\n## The exact optimum\n", "\n## The earlier exact optimum\n")
    body = body.replace(
        "The verified upper bound and the printed side now agree",
        "For the earlier packing, its verified upper bound and printed side agree",
    )
    body = body.replace(
        "known-best witness this record lists is that binary64 pose",
        "earlier known-best witness was that binary64 pose",
    ).replace(
        "The known-best\nwitness this record lists is that binary64 pose",
        "The earlier known-best\nwitness was that binary64 pose",
    )
    case["reported_upper_bound"].update(
        value=reports.legacy.terminating_decimal(certificate.side),
        exact_form=reports.legacy.literal(certificate.side),
        algebraic_degree=1,
        minimal_polynomial=None,
        analytically_optimized=None,
        catalogue_rigid="not-stated",
        construction_method="unknown",
        tilt_angles_deg=None,
        found_by=["Evan Daniel"],
        found_year=2026,
        improved_by=[],
        catalogue_pictured=False,
        source_key=reports.SOURCE_KEY,
        source_date=DAY,
        retrieved_date=DAY,
        witnesses=[f"W-known-best-n{n:03d}"],
        evidence=[REPORT_EVIDENCE, reports.EXACT_EVIDENCE],
    )
    case["verified_upper_bound"] = verified
    case["source_reviewed"] = "2026-10-08"
    for evidence in (REPORT_EVIDENCE, reports.EXACT_EVIDENCE):
        if evidence not in case["evidence"]:
            case["evidence"].insert(0, evidence)
    if generated is not None:
        draft_front, draft_body = generated.split("---\n", 2)[1:]
        draft = safe_load(draft_front)["packing"]
        for field in (
            "reported_lower_bound",
            "verified_lower_bound",
            "reported_status",
            "status",
        ):
            case[field] = draft[field]
        lower = re.search(
            r"\n## The lower bound\n.*?(?=\n<!-- BEGIN verification code)",
            draft_body,
            re.DOTALL,
        )
        if lower is None:
            raise reports.ReportError("generated lower-bound section missing")
        body, count = re.subn(
            r"\n## The lower bound\n.*?(?=\n<!-- BEGIN verification code)",
            lambda _match: lower.group(),
            body,
            flags=re.DOTALL,
        )
        if count != 1:
            raise reports.ReportError("existing lower-bound section missing")
    from devtools import render_case_verifiers  # noqa: PLC0415

    return render_case_verifiers.refresh("---\n" + registry.dump(document) + "---\n" + body)


def read_history() -> list[dict[str, Any]]:
    """Admit the complete original case roster before any producer mutation."""
    path = reports.PACKET / "acquisition/prior-state.json.xz"
    if not path.resolve().is_relative_to(reports.REPO.resolve()):
        raise reports.ReportError("history must remain inside the repository")
    value = reports.read_xz(path)
    if (
        type(value) is not list
        or any(
            type(row) is not dict
            or set(row) != {"n", "complete_case"}
            or type(row["n"]) is not int
            or type(row["complete_case"]) is not str
            for row in value
        )
        or [row["n"] for row in value] != list(reports.NUMBERS)
    ):
        raise reports.ReportError("complete immutable previous case roster required")
    for row in value:
        original = safe_load(row["complete_case"].split("---\n", 2)[1])["packing"]
        if (
            original["n"] != row["n"]
            or original["reported_upper_bound"]["source_key"] == reports.SOURCE_KEY
        ):
            raise reports.ReportError("history must contain every original pre-adoption source")
    return value


def record_cases() -> None:
    """Preflight the full roster, retain immutable originals, then publish cases.

    An interrupted write resumes against the complete original history and never
    replaces that history with the remaining subset. Unrelated source changes refuse.
    """
    reports.check_certification()
    history = reports.PACKET / "acquisition/prior-state.json.xz"
    if not history.resolve().is_relative_to(reports.REPO.resolve()):
        raise reports.ReportError("history must remain inside the repository")
    retained = read_history() if history.exists() else None
    historical = {} if retained is None else {row["n"]: row for row in retained}
    prior = []
    plan = []
    for n in reports.NUMBERS:
        path = FRONTIER / f"n-{n:03d}.md"
        if not path.resolve().is_relative_to(reports.REPO.resolve()):
            raise reports.ReportError("case output must remain inside the repository")
        current = path.read_text()
        case = safe_load(current.split("---\n", 2)[1])["packing"]
        if case["n"] != n:
            raise reports.ReportError("case count differs from the complete selected roster")
        if case["reported_upper_bound"]["source_key"] == reports.SOURCE_KEY:
            if retained is None:
                raise reports.ReportError("selected case lacks complete original history")
            continue
        original = current if retained is None else historical[n]["complete_case"]
        if current != original:
            raise reports.ReportError(
                "refuse a changed historical source before any case write"
            )
        bound = reports.confirmed_bound(n)
        if Decimal(bound["value"]) >= Decimal(case["reported_upper_bound"]["value"]):
            raise reports.ReportError(
                f"n={n}: selected display is not smaller than current bound"
            )
        prior.append({"n": n, "complete_case": original})
        plan.append((path, adopt_case(n, original)))
    if not plan:
        return
    if retained is None:
        # Full-roster admission and every transformation completed before this boundary.
        reports.save_xz(history, prior)
        read_history()
    for path, text in plan:
        registry.save(path, text)


def register() -> None:
    record_cases()
    registry.append_rows(
        FRONTIER / "evidence.yaml",
        "evidence",
        [
            {
                "id": REPORT_EVIDENCE,
                "claim": "upper-bound",
                "scope": {"n_values": list(reports.NUMBERS)},
                "assurance": "reported",
                "reported_method": "exact-algebraic",
                "performed_by": "source-author",
                "relationship_to_generator": "same-implementation",
                "replay_status": "not-attempted",
                "verifiers": [],
                "source_key": reports.SOURCE_KEY,
                "origin": "external",
                "novelty": "previously-published",
                "certificate": (
                    "packing/resources/web/evand-new-arrangements-2026-10-07/"
                    "facts/complete-certificates.json.xz"
                ),
                "limitations": (
                    "Author-reported new arrangements. Novelty, KKT, local/global "
                    "optimality and rigidity remain unestablished."
                ),
                "source_reviewed": "2026-10-08",
            },
            {
                "id": reports.EXACT_EVIDENCE,
                "claim": "upper-bound",
                "scope": {"n_values": list(reports.NUMBERS)},
                "assurance": "verified",
                "method": "exact-algebraic",
                "performed_by": "repository",
                "relationship_to_generator": "independent-implementation",
                "replay_status": "passed",
                "source_key": reports.SOURCE_KEY,
                "origin": "audited-here",
                "novelty": "previously-published",
                "certificate": (
                    "packing/resources/web/evand-new-arrangements-2026-10-07/"
                    "receipts/exact-certification.json.xz"
                ),
                "replay": (
                    "From packing/, python -m devtools.evand_arrangement_reports "
                    "check --replay; all nine complete jobs and both exact routes are"
                    " repeated."
                ),
                "verifiers": [
                    "V-sqpack-verify",
                    "V-check-rational-witness-independent",
                    "V-evand-arrangement-receipts",
                ],
                "independence_record": REVIEW,
                "external_review": {
                    "state": "informally-verified",
                    "date": "2026-10-08",
                    "reviewed_by": "GPT-6 Astra independent mathematical reviewer",
                    "note": (
                        "Fresh nine-job replay agrees with all18 complete native outcomes"
                        " apart from measured timing;650496 pair decisions."
                    ),
                },
                "limitations": (
                    "Two independently implemented exact routes share the strict "
                    "lossless half-angle conversion and Python rational arithmetic. "
                    "Feasible upper bounds only; no novelty, local/global optimality,"
                    " rigidity or human-oversight assurance."
                ),
                "source_reviewed": "2026-10-08",
            },
        ],
        "id",
    )
    registry.append_rows(
        FRONTIER / "verifiers.yaml",
        "verifiers",
        [
            {
                "id": "V-evand-arrangement-receipts",
                "program": "devtools.evand_arrangement_reports",
                "author": "Squares Project (Levy)",
                "provenance": "first-party",
                "language": ["Python"],
                "methods": ["exact-algebraic"],
                "role": "premises",
                "summary": (
                    "Binds all three complete source certificates and all nine full "
                    "deciding inputs/native results; explicit replay repeats both "
                    "project geometric deciders."
                ),
                "source": ["packing/devtools/evand_arrangement_reports.py"],
            },
        ],
        "id",
    )
    packet = "packing/resources/web/evand-new-arrangements-2026-10-07"
    registry.append_rows(
        FRONTIER / "results.yaml",
        "results",
        [
            {
                "id": RESULT,
                "kind": "upper-bound",
                "registered": DAY,
                "headline": (
                    "Three exact feasible upper bounds at n=266,270,272 from new "
                    "source arrangements"
                ),
                "claim": (
                    "Complete rational packings establish "
                    "s(266)<=16.8230287507564760, s(270)<=16.9378072284460292 and "
                    "s(272)<=16.9681101457696006. All displays are upward ceilings of"
                    " exact rational sides; arrangement novelty remains "
                    "author-reported."
                ),
                "scope": {"n_values": list(reports.NUMBERS)},
                "verification": "V3",
                "confirmation": "C3",
                "significance": {
                    "score": 3,
                    "rationale": (
                        "Three strictly smaller exact feasible ceilings with complete "
                        "changed poses; no solved case or optimality claim."
                    ),
                    "scored": DAY,
                    "by": "think-hh48 #399 import",
                },
                "novelty": "previously-published",
                "attribution": {"source_keys": [reports.SOURCE_KEY], "published": DAY},
                "evidence": [REPORT_EVIDENCE, reports.EXACT_EVIDENCE],
                "artifacts": [
                    f"{packet}/README.md",
                    f"{packet}/facts/complete-certificates.json.xz",
                    f"{packet}/receipts/exact-certification.json.xz",
                    "packing/devtools/evand_arrangement_reports.py",
                    *[f"packing/frontier/n-{n:03d}.md" for n in reports.NUMBERS],
                ],
                "reviews": [
                    {
                        "path": REVIEW,
                        "kind": "adversarial",
                        "reviewer": "GPT-6 Astra mathematical reviewer",
                        "reviewer_kind": "ai",
                        "relation": "project",
                        "date": "2026-10-08",
                        "scope": (
                            "All three complete sources, exact half-angle conversion and full"
                            " nine-job/18-result replay;650496 pair decisions."
                        ),
                        "verdict": "accepted",
                        "covers": [RESULT],
                    }
                ],
                "controls": [
                    f"{packet}/receipts/exact-certification.json.xz",
                    "packing/tests/test_evand_arrangement_reports.py",
                ],
                "composition": (
                    "Full-roster source admission precedes exact rational conversion;"
                    " both independent routes inspect every wall and pair. Every "
                    "complete input and native verdict is retained. Private worker "
                    "inputs bind only three explicitly guarded atlas read links."
                ),
                "notes": (
                    "Historical #375 source13ee36e, T-098/T-101 certificates, credits"
                    " and original poses remain unchanged. Source new-arrangement and"
                    " KKT/local-minimum assertions are not promoted by feasibility."
                ),
                "next_rung": (
                    "V4/C4 requires accountable human review. V5/C5 requires "
                    "proof-assistant verification; this replay establishes neither."
                ),
            },
        ],
        "id",
    )

    result_path = FRONTIER / "results.yaml"
    results = result_path.read_text()
    pattern = re.compile(r"^  - id: T-119\n.*?(?=^  - id: |\Z)", re.MULTILINE | re.DOTALL)
    block = pattern.search(results)
    if block is None:
        raise reports.ReportError("new-arrangement result registration missing")
    without = results[: block.start()] + results[block.end() :]
    successor = re.search(r"^  - id: T-(?:1[2-9][0-9]|[2-9][0-9]{2})\n", without, re.MULTILINE)
    if successor is not None:
        registry.save(
            result_path,
            without[: successor.start()]
            + block.group().rstrip()
            + "\n\n"
            + without[successor.start() :],
        )
    registry.append_rows(
        REPO / "docs/project/document-map.yaml",
        "documents",
        [{"path": REVIEW, "role": "review", "authority": "record", "lifecycle": "retained"}],
        "path",
    )


def register_sources() -> None:
    identifier = "evand-new-arrangements-2026-10-07"
    claims = {
        "results": [
            {
                "n": n,
                "offered_side": reports.legacy.terminating_decimal(reports.read_fact(n).side),
                "exact_side": reports.legacy.literal(reports.read_fact(n).side),
            }
            for n in reports.NUMBERS
        ]
    }
    registry.save(
        reports.PACKET / "acquisition/claims.json", json.dumps(claims, indent=2) + "\n"
    )
    coverage_path = FRONTIER / "source-coverage.yaml"
    registry.append_rows(
        coverage_path,
        "sources",
        [
            {
                "id": identifier,
                "title": "Daniel's three new rational arrangements, issue399",
                "role": "source-repository",
                "url": f"{reports.SOURCE}/tree/{reports.REVISION}",
                "local": "resources/web/evand-new-arrangements-2026-10-07/",
                "source_key": reports.SOURCE_KEY,
                "scope": {"n_values": list(reports.NUMBERS)},
                "reviewed": "2026-10-08",
                "source_date": DAY,
                "disposition": "current-report",
                "replay_disposition": "case-specific",
                "represented_by": [f"frontier/n-{n:03d}.md" for n in reports.NUMBERS],
                "claims_record": (
                    "resources/web/evand-new-arrangements-2026-10-07/acquisition/claims.json"
                ),
                "evidence": [REPORT_EVIDENCE, reports.EXACT_EVIDENCE],
                "notes": (
                    "All three complete source poses and full rational sides are "
                    "separately certified. Historical #375 source13ee36e and "
                    "T-098/T-101 receipts remain unchanged; novelty and "
                    "optimality are not promoted."
                ),
            }
        ],
        "id",
    )
    original = coverage_path.read_text()
    coverage = safe_load(original)
    for row in coverage["superseded_reports"]:
        if row["n"] in reports.NUMBERS:
            if row["superseded_by"] != identifier:
                row["reason"] += (
                    " The separately certified #399 arrangement is now strictly smaller."
                )
            row["superseded_by"] = identifier
    for row in list(coverage["selected_overrides"]):
        if row["n"] not in reports.NUMBERS or row["source_id"] == identifier:
            continue
        coverage["superseded_reports"].append(
            {
                "n": row["n"],
                "source_id": row["source_id"],
                "value": row["value"],
                "superseded_by": identifier,
                "reason": (
                    "The complete #399 construction has a strictly smaller side; "
                    "the earlier report and its full certificates remain "
                    "historical."
                ),
            }
        )
        coverage["selected_overrides"].remove(row)
    selected = {row["n"] for row in coverage["selected_overrides"]}
    for n in reports.NUMBERS:
        if n not in selected:
            coverage["selected_overrides"].append(
                {
                    "n": n,
                    "source_id": identifier,
                    "value": reports.legacy.terminating_decimal(reports.read_fact(n).side),
                    "evidence": REPORT_EVIDENCE,
                    "reason": (
                        "Complete changed source poses establish a smaller exact "
                        "rational ceiling; both independent project routes and "
                        "full-roster controls pass."
                    ),
                }
            )
    for field in ("selected_overrides", "superseded_reports"):
        pattern = re.compile(rf"^{field}:[^\n]*\n.*?(?=^[a-z_]+:|\Z)", re.MULTILINE | re.DOTALL)
        match = pattern.search(original)
        if match is None:
            raise reports.ReportError("missing coverage list")
        roster = {(row["n"], row["source_id"]): row for row in coverage[field]}
        chunks = re.split(r"(?=^  - )", match.group(), flags=re.MULTILINE)
        kept = [chunks[0]]
        for chunk in chunks[1:]:
            (row,) = safe_load("rows:\n" + chunk)["rows"]
            key = row["n"], row["source_id"]
            replacement = roster.pop(key, None)
            if row["n"] not in reports.NUMBERS:
                kept.append(chunk)
            elif replacement is not None:
                kept.append(
                    "".join(
                        "  " + line
                        for line in registry.dump([replacement]).splitlines(keepends=True)
                    )
                )
        kept.extend(
            "".join("  " + line for line in registry.dump([row]).splitlines(keepends=True))
            for row in roster.values()
        )
        block = "".join(kept)
        original = pattern.sub(lambda _match, replacement=block: replacement, original, count=1)
    registry.save(coverage_path, original)
    registry.append_rows(
        REPO / "packing/resources/bibliography.yaml",
        "sources",
        [
            {
                "key": reports.SOURCE_KEY,
                "authors": ["Daniel"],
                "year": 2026,
                "venue": "GitHub",
                "dated": DAY,
                "credit": "Daniel after Levy, Ellsworth, Couzo, Stead",
                "short_credit": "Daniel after Levy et al.",
                "lineage": "builds-on-project",
                "note": (
                    "Issue399 supplies three complete changed rational packings "
                    "at266,270,272. Pinned7eef24f source MIT licences and "
                    "original lineage remain retained. Exact feasibility is "
                    "certified independently; source arrangement novelty and "
                    "local/global optimality are unestablished."
                ),
            }
        ],
        "key",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--atlas", action="store_true", help="rebuild only the three adopted atlas cases"
    )
    args = parser.parse_args()
    if args.atlas:
        from devtools.build_known_best_atlas import update_selected  # noqa: PLC0415

        update_selected(list(reports.NUMBERS), workers=2)
    else:
        register()
        register_sources()


if __name__ == "__main__":
    main()
