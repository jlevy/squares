# ruff: noqa: RUF001 -- generated record prose follows the project's typography.
"""Register issue #432's two finite-feasibility claims and adopt only smaller source sides.

The initial layer is reported. Confirmation is a separate explicit integration after
scoped review and full private-worker admission; this writer runs no geometry solver.
"""

from __future__ import annotations

import argparse
import copy
import re
from decimal import Decimal
from typing import Any

from devtools import render_case_verifiers
from devtools import ryxu_house_links as houses
from devtools.register_refinement_reports import FOOTER, append_rows, dump, save
from sqpack.yamlio import safe_load

REPO = houses.REPO
FRONTIER = REPO / "packing/frontier"
DAY = houses.RETRIEVED
REPORT = "E-ryxu-432-rational-report"
RADICAL_REPORT = "E-ryxu-432-radical-n51-report"
RADICAL_EXACT = "E-ryxu-432-radical-n51-feasibility"
HISTORY = houses.reports.PACKET / "acquisition/frontier-prior-state.json.xz"
SECTION = "## The ry-xu construction"


def reported_bound(n: int) -> dict[str, Any]:
    bound = houses.bound(n)
    return {
        **bound,
        "algebraic_degree": 2 if n == 51 else 1,
        "minimal_polynomial": "9s^2-96s+206=0" if n == 51 else None,
        "analytically_optimized": None,
        "catalogue_rigid": "not-stated",
        "construction_method": "unknown",
        "tilt_angles_deg": None,
        "found_by": ["ry-xu"],
        "found_year": 2026,
        "improved_by": [],
        "catalogue_pictured": False,
        "source_key": houses.SOURCE_KEY,
        "source_date": DAY,
        "retrieved_date": DAY,
        "witnesses": [f"W-known-best-n{n:03d}"],
        "evidence": [RADICAL_REPORT if n == 51 else REPORT],
    }


def section(n: int, *, confirmed: bool) -> str:
    bound = houses.bound(n)
    side = r"(16+5\sqrt{2})/3" if n == 51 else bound["exact_form"]
    identity = (
        r"This is the undilated construction over $\mathbb{Q}(\sqrt{2})$, using all 51 "
        "source coefficient poses. It is distinct from the source’s rational certificate, "
        "which already includes its stated dilation."
        if n == 51
        else "The complete rational source certificate already includes the source’s stated "
        "dilation. No additional dilation or coordinate rounding is applied here."
    )
    assurance = (
        "Complete native replay, required full-roster controls and scoped independent "
        "review confirm finite feasibility at V3/C3."
        if confirmed
        else "This result remains reported at V0/C0 while scoped independent review and "
        "production custody admission are completed. Drawing admission is separate."
    )
    result = "T-126" if n == 51 else "T-125"
    return (
        f"\n{SECTION}\n\n"
        f"ry-xu reports ({result}) a construction at exact side ${side}$, displayed upward "
        f"as ${bound['value']}$. The [pinned factual packet]"
        "(../resources/web/ry-xu-new-packings-2026-10-08/README.md) retains the entire "
        "source input and complete actual deciding outcomes.\n\n"
        f"{identity}\n\n{assurance} The source discloses LLM assistance. "
        "No global optimum, local-minimum theorem, rigidity or novelty is established. "
        "The source’s 191-touching-pair assertion for n51 is unconfirmed and is not admitted.\n"
    )


def _historical_prose(body: str) -> str:
    """Keep previous source assertions, explicitly scoped before this adoption."""
    replacements = (
        (
            "Open. The best known published packing",
            "Previously, the best known published packing",
        ),
        ("The best known published packing", "Previously, the best known published packing"),
        ("Open. The best known packing gives", "The earlier packing gave"),
        ("The best known packing gives", "The earlier packing gave"),
        ("the atlas pictures", "the atlas then pictured"),
        ("the atlas\npictures", "the atlas\nthen pictured"),
        (
            "witness this record lists is that binary64 pose",
            "witness this record listed then was that binary64 pose",
        ),
        ("## The exact optimum\n", "## The earlier exact packing\n"),
        ("the verified upper bound:", "the verified upper bound at that intake:"),
        ("the verified upper bound;", "the verified upper bound at that intake;"),
    )
    for before, after in replacements:
        body = body.replace(before, after)
    return body


def adopt_case(n: int, existing: str, generated: str) -> str:
    """Rebuild the selected exact upper lane; ordinary lower lanes belong to the draft."""
    if n not in houses.NUMBERS:
        return generated
    _, front, body = existing.split("---\n", 2)
    document = safe_load(front)
    case = document["packing"]
    if case["n"] != n or case["reported_upper_bound"]["source_key"] != houses.SOURCE_KEY:
        return generated
    expected_evidence = houses.bound(n)["evidence"]
    own = [
        item for item in case["verified_upper_bound"]["evidence"] if item.startswith("E-ryxu-")
    ]
    confirmed = bool(own)
    if own and case["verified_upper_bound"]["evidence"] != expected_evidence:
        raise ValueError("selected ry-xu case has unmapped confirming evidence")
    # Source and complete results are admitted regardless of the registered rung.
    houses.reports.check_certification()
    houses.radical.check_certification()
    houses.check_houses([n])
    case["reported_upper_bound"] = reported_bound(n)
    draft = safe_load(generated.split("---\n", 2)[1])["packing"]
    for field in ("reported_lower_bound", "verified_lower_bound", "reported_status", "status"):
        case[field] = draft[field]
    if confirmed:
        case["verified_upper_bound"] = houses.bound(n)
    else:
        prior = houses.reports.kernel.read_xz(HISTORY)
        if prior["format"] != "ryxu-432-prior-frontier-and-house-v1":
            raise ValueError("unknown retained previous upper-bound boundary")
        row = next(item for item in prior["cases"] if item["n"] == n)
        old_case = safe_load(row["frontier"].split("---\n", 2)[1])["packing"]
        case["verified_upper_bound"] = copy.deepcopy(old_case["verified_upper_bound"])
    case["rigidity"] = None
    case["conjectured_optimum"] = None
    case["source_reviewed"] = DAY
    lower_pattern = r"\n## The lower bound\n.*?(?=\n<!-- BEGIN verification code)"
    lower = re.search(lower_pattern, generated.split("---\n", 2)[2], re.DOTALL)
    if lower is None:
        raise ValueError("historical draft has no generated lower-bound section")
    body, count = re.subn(lower_pattern, lambda _match: lower.group(), body, flags=re.DOTALL)
    if count != 1:
        raise ValueError("selected ry-xu case needs one generated lower-bound section")
    pattern = rf"\n{SECTION}\n.*?(?=\n## |\n<!-- This document follows)"
    body, count = re.subn(
        pattern, lambda _match: section(n, confirmed=confirmed), body, flags=re.DOTALL
    )
    body = _historical_prose(body)
    if count != 1:
        raise ValueError("selected ry-xu case needs one source-bound construction section")
    return render_case_verifiers.refresh("---\n" + dump(document) + "---\n" + body)


def record_cases() -> list[dict[str, Any]]:
    """Preserve complete previous frontmatter and geometry before updating current counts."""
    prior = []
    for n in houses.NUMBERS:
        path = FRONTIER / f"n-{n:03d}.md"
        original = path.read_text()
        _, front, body = original.split("---\n", 2)
        document = safe_load(front)
        case = document["packing"]
        if case["reported_upper_bound"]["source_key"] == houses.SOURCE_KEY:
            continue
        bound = houses.bound(n)
        if Decimal(bound["value"]) >= Decimal(case["reported_upper_bound"]["value"]):
            raise ValueError(f"n={n}: selected ry-xu display is not smaller than current bound")
        prior.append({"n": n, "frontier": original, "house": houses.house_path(n).read_text()})
        old = copy.deepcopy(case["reported_upper_bound"])
        case["reported_upper_bound"] = reported_bound(n)
        case["rigidity"] = None
        case["conjectured_optimum"] = None
        case["source_reviewed"] = DAY
        evidence = RADICAL_REPORT if n == 51 else REPORT
        if evidence not in case["evidence"]:
            case["evidence"].append(evidence)
        case["resources"].insert(
            0,
            {
                "key": houses.SOURCE_KEY,
                "role": "upper-bound-report",
                "local": "web/ry-xu-new-packings-2026-10-08",
                "url": f"{houses.reports.SOURCE}/tree/{houses.reports.REVISION}",
                "retrieved": True,
            },
        )
        case["priority_notes"].append(
            {
                "claim": (
                    f"Earlier source ceiling {old['value']} from {old['source_key']}; "
                    "full prior geometry and record remain retained in the packet."
                ),
                "claimed_by": old["found_by"],
                "published": None,
                "year": old["found_year"],
            }
        )
        case["blockers"].append(
            {
                "kind": "mathematics",
                "detail": (
                    "Issue432 remains V0/C0 pending independent scoped review and "
                    "production custody admission."
                ),
                "evidence": [evidence],
            }
        )
        body = _historical_prose(body)
        body = body.replace(FOOTER, section(n, confirmed=False) + "\n" + FOOTER)
        save(path, "---\n" + dump(document) + "---\n" + body)
    if prior:
        if HISTORY.exists():
            raise ValueError(
                "do not overwrite the retained previous frontier/geometry boundary"
            )
        houses.reports.save(
            HISTORY, {"format": "ryxu-432-prior-frontier-and-house-v1", "cases": prior}
        )
    return prior


def _register_records() -> None:
    for result, ns, evidence, headline, claim in (
        (
            "T-125",
            list(houses.reports.NUMBERS),
            REPORT,
            "Complete rational construction reports at 25 counts",
            (
                "The source reports finite rational feasible ceilings for all 25 "
                "complete certificates retained in the factual packet. Eighteen "
                "improve the current source displays; seven are superseded and "
                "retained. This claim establishes no optimality or local-minimum "
                "theorem."
            ),
        ),
        (
            "T-126",
            [51],
            RADICAL_REPORT,
            "Undilated n51 construction over Q(sqrt2)",
            (
                "The 51 exact coefficient poses give the construction upper bound "
                "s(51) <= (16+5sqrt(2))/3. This does not assert equality with "
                "s(51), optimality, rigidity or the unconfirmed 191-touching-pair "
                "source claim."
            ),
        ),
    ):
        append_rows(
            FRONTIER / "evidence.yaml",
            "evidence",
            [
                {
                    "id": evidence,
                    "claim": "upper-bound",
                    "scope": {"n_values": ns},
                    "assurance": "reported",
                    "reported_method": "exact-algebraic",
                    "performed_by": "source-author",
                    "relationship_to_generator": "same-implementation",
                    "origin": "external",
                    "novelty": "previously-published",
                    "source_key": houses.SOURCE_KEY,
                    "certificate": "packing/resources/web/ry-xu-new-packings-2026-10-08/facts/",
                    "replay_status": "not-attempted",
                    "verifiers": [],
                    "limitations": claim,
                    "source_reviewed": DAY,
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
                    "headline": headline,
                    "claim": claim,
                    "scope": {"n_values": ns},
                    "verification": "V0",
                    "confirmation": "C0",
                    "significance": {
                        "score": 3,
                        "rationale": (
                            "Current feasible construction ceilings improve at 18 counts, "
                            "without a solved case or lower-bound theorem."
                        )
                        if result == "T-125"
                        else (
                            "A simpler degree-two exact construction ceiling at 51; no optimum "
                            "established."
                        ),
                        "scored": DAY,
                        "by": "think-1cvf source integration",
                    },
                    "novelty": "previously-published",
                    "attribution": {"source_keys": [houses.SOURCE_KEY], "published": DAY},
                    "evidence": [evidence],
                    "artifacts": [
                        "packing/resources/web/ry-xu-new-packings-2026-10-08/README.md",
                        "packing/devtools/ryxu_arrangement_reports.py"
                        if result == "T-125"
                        else "packing/devtools/ryxu_radical_n51.py",
                    ],
                    "next_rung": (
                        "Complete native replay admission, required controls, scoped "
                        "independent review and private-worker custody are required "
                        "before confirmation."
                    ),
                    "notes": (
                        "Credit to ry-xu with disclosed LLM assistance. All 25 source "
                        "inputs retained; no upstream code executed. Exact finite "
                        "feasibility only."
                    ),
                }
            ],
            "id",
        )


def register() -> None:
    houses.reports.check_certification()
    houses.radical.check_certification()
    prior = record_cases()
    if not prior:
        retained = houses.reports.kernel.read_xz(HISTORY)
        if retained["format"] != "ryxu-432-prior-frontier-and-house-v1":
            raise ValueError("unknown retained previous-record boundary")
        prior = retained["cases"]
    _register_records()
    append_rows(
        FRONTIER / "source-coverage.yaml",
        "sources",
        [
            {
                "id": houses.SOURCE_ID,
                "title": "ry-xu new square constructions, issue #432",
                "role": "source-repository",
                "url": f"{houses.reports.SOURCE}/tree/{houses.reports.REVISION}",
                "local": "resources/web/ry-xu-new-packings-2026-10-08/",
                "source_key": houses.SOURCE_KEY,
                "scope": {"n_values": list(houses.reports.NUMBERS)},
                "reviewed": DAY,
                "source_date": DAY,
                "disposition": "current-report",
                "replay_disposition": "case-specific",
                "represented_by": [f"frontier/n-{n:03d}.md" for n in houses.NUMBERS],
                "evidence": [REPORT, RADICAL_REPORT],
                "claims_record": (
                    "resources/web/ry-xu-new-packings-2026-10-08/facts/"
                    "complete-certificates.json.xz"
                ),
                "notes": (
                    "All 25 full source geometries retained. Eighteen current "
                    "improvements; canonical n51 is the separate undilated radical "
                    "construction. No 191-contact assertion admitted."
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
                "id": houses.RADICAL_SOURCE_ID,
                "title": "ry-xu undilated n51 exact construction",
                "role": "source-repository",
                "url": houses.source_url(51),
                "local": "resources/web/ry-xu-new-packings-2026-10-08/",
                "source_key": houses.SOURCE_KEY,
                "scope": {"n_values": [51]},
                "reviewed": DAY,
                "source_date": DAY,
                "disposition": "current-report",
                "replay_disposition": "case-specific",
                "represented_by": ["frontier/n-051.md"],
                "evidence": [RADICAL_REPORT],
                "claims_record": (
                    "resources/web/ry-xu-new-packings-2026-10-08/facts/"
                    "n051-undilated-record.json.xz"
                ),
                "notes": (
                    "Separate undilated complete 51 poses over Q(sqrt2); "
                    "no optimality or 191-contact claim."
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
        start = text.index("selected_overrides:")
        end = text.index("superseded_reports:", start)
        selected_text = text[start:end]
        found = re.search(pattern, selected_text, re.DOTALL)
        new = {
            "n": n,
            "source_id": houses.RADICAL_SOURCE_ID if n == 51 else houses.SOURCE_ID,
            "value": houses.bound(n)["value"],
            "evidence": RADICAL_REPORT if n == 51 else REPORT,
            "reason": (
                "Smaller exact source construction; reported pending scoped "
                "review and private admission."
            ),
        }
        rendered = "".join("  " + line for line in dump([new]).splitlines(keepends=True))
        if found is None:
            text = text[:end].rstrip() + "\n" + rendered + text[end:]
        else:
            previous = safe_load(found.group())[0]
            if previous["source_id"] == new["source_id"]:
                text = text[: start + found.start()] + rendered + text[start + found.end() :]
                continue
            text = text[: start + found.start()] + rendered + text[start + found.end() :]
            previous.pop("reason", None)
            previous.pop("evidence", None)
            previous.update(
                superseded_by=houses.RADICAL_SOURCE_ID if n == 51 else houses.SOURCE_ID,
                reason=(
                    "Historical source ceiling superseded by a smaller exact ry-xu "
                    "construction."
                ),
            )
            start = text.index("beyond_horizon_claims:")
            old_rendered = "".join(
                "  " + line for line in dump([previous]).splitlines(keepends=True)
            )
            text = text[:start].rstrip() + "\n" + old_rendered + text[start:]
    covered = safe_load(text)
    selected = {row["n"]: row for row in covered["selected_overrides"]}
    for row in covered["superseded_reports"]:
        if row["n"] in houses.NUMBERS and row["source_id"] != selected[row["n"]]["source_id"]:
            row["superseded_by"] = selected[row["n"]]["source_id"]
    existing = {(row["n"], row["source_id"]) for row in covered["superseded_reports"]}
    facts = houses.reports.read_facts()
    for n in houses.reports.NUMBERS:
        if n in houses.NUMBERS and n != 51:
            continue
        identity = (n, houses.SOURCE_ID)
        if identity in existing:
            continue
        owner = selected[n]["source_id"] if n in selected else "kingbird-current"
        covered["superseded_reports"].append(
            {
                "n": n,
                "source_id": houses.SOURCE_ID,
                "value": houses.reports.legacy.ceiling_decimal(facts[n].side, 16),
                "superseded_by": owner,
                "reason": (
                    "Complete rational certificate retained; "
                    "the current exact construction is smaller."
                ),
            }
        )
    # Rewrite only this list, preserving comments elsewhere in the coverage record.
    start = text.index("superseded_reports:")
    end = text.index("beyond_horizon_claims:", start)
    rendered = "".join(
        "  " + line for line in dump(covered["superseded_reports"]).splitlines(keepends=True)
    )
    text = text[:start] + "superseded_reports:\n" + rendered + text[end:]
    save(coverage, text)
    append_rows(
        REPO / "packing/resources/bibliography.yaml",
        "sources",
        [
            {
                "key": houses.SOURCE_KEY,
                "authors": ["ry-xu"],
                "year": 2026,
                "venue": "GitHub",
                "dated": DAY,
                "lineage": "independent",
                "note": (
                    "The retained factual source certificates "
                    "at 8dc415296f697f5140caea27c7a0193d52deb4e6 identify ry-xu and "
                    "disclose LLM assistance; no unrestricted optimality or "
                    "contact-count theorem is admitted."
                ),
            }
        ],
        "key",
    )
    bibliography = REPO / "packing/resources/bibliography.yaml"
    if "  ry-xu: ry-xu\n" not in bibliography.read_text():
        save(
            bibliography,
            bibliography.read_text().replace(
                "credited_names:\n", "credited_names:\n  ry-xu: ry-xu\n"
            ),
        )


def main() -> None:
    argparse.ArgumentParser(description=__doc__, allow_abbrev=False).parse_args()
    register()


if __name__ == "__main__":
    main()
