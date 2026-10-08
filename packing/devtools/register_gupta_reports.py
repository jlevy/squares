"""Register Gupta's complete source scope with history-first selected-case adoption.

This stage remains reported. Confirming result integration follows the separately
reviewed full native execution and actual production custody transaction.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import gupta_house_links as houses
from devtools import register_ryxu_reports as previous
from devtools import render_case_verifiers
from devtools.register_refinement_reports import FOOTER, append_rows, dump, save
from sqpack.yamlio import safe_load

REPO = houses.REPO
FRONTIER = REPO / "packing/frontier"
DAY = "2026-10-08"
REPORT = "E-gupta-438-rational-report"
RESULT = "T-127"
SOURCE_ID = "gupta-square-packing-refinements-2026-10-08"
HISTORY = houses.HISTORY
HISTORY_FORMAT = "gupta-438-prior-frontier-and-house-v1"
SECTION = "## The Gupta precision refinement"
REVIEW = "docs/project/reviews/review-2026-10-08-gupta-exact-refinements.md"
PACKET_PATH = "packing/resources/web/gupta-square-packing-refinements-2026-10-08"


def reported_bound(n: int) -> dict[str, Any]:
    certificate = houses.reports.read_fact(n)
    return {
        "value": houses.reports.legacy.ceiling_decimal(certificate.side, 16),
        "exact_form": str(certificate.side),
        "algebraic_degree": 1,
        "minimal_polynomial": None,
        "analytically_optimized": None,
        "catalogue_rigid": "not-stated",
        "construction_method": "unknown",
        "tilt_angles_deg": None,
        "found_by": ["Nate Chaoweeraprasit (itsnaka)"],
        "found_year": 2026,
        "improved_by": ["Siddharth Gupta"],
        "catalogue_pictured": False,
        "source_key": houses.reports.SOURCE_KEY,
        "source_date": DAY,
        "retrieved_date": DAY,
        "witnesses": [f"W-known-best-n{n:03d}"],
        "evidence": [REPORT],
    }


def section(n: int, *, confirmed: bool) -> str:
    bound = reported_bound(n)
    assurance = (
        "Complete dual-route native replay, full-roster controls and separately prompted "
        "source and production review confirm finite feasibility at V3/C3."
        if confirmed
        else "The registered source claim remains V0/C0 pending independent production "
        "custody review and confirming record integration. Drawing admission is separate."
    )
    return (
        f"\n{SECTION}\n\n"
        f"Siddharth Gupta refines the earlier SQUISH construction at exact rational side "
        f"${bound['exact_form']}$, displayed upward as ${bound['value']}$ ({RESULT}). "
        "The [complete factual packet]"
        "(../resources/web/gupta-square-packing-refinements-2026-10-08/README.md) "
        "retains every original certificate, complete comparator and actual deciding "
        "outcome for all seventeen source cases, including three withdrawals.\n\n"
        f"{assurance} The full source poses are converted without dilation or rounding. "
        "The source credits Nate Chaoweeraprasit for SQUISH and Evan Daniel for the "
        "optimizer. No author program is executed here. Feasibility establishes no "
        "optimizer, local-minimum, rigidity, novelty, priority, global-optimality, formal "
        "proof or human-oversight assurance.\n"
    )


def historical_prose(n: int, body: str) -> str:
    """Scope old ceiling and picture comparisons while preserving source names."""
    historical, separator, current = body.partition(SECTION)
    historical = previous.historical_upper_prose(n, historical)
    historical = historical.replace(
        "Previously, nate Chaoweeraprasit", "Previously, Nate Chaoweeraprasit"
    ).replace("the atlas pictures", "the atlas pictured at that intake")
    return historical + separator + current


def validate_prior_house(row: dict[str, Any], case: dict[str, Any]) -> None:
    """Schema-load every original pose, then bind its source and side to the old case."""
    shared = houses.shared
    source_key = case["reported_upper_bound"]["source_key"]
    n = row["n"]
    if source_key == shared.confirmation.reported.SOURCE_KEY:
        source_url = shared.confirmation.reported.source_url(n)
    elif source_key == shared.shared.SOURCE_KEY:
        source_url = shared.shared.source_url(n)
    elif source_key == shared.original.source_key(n):
        source_url = shared.original.source_url(n)
    else:
        raise ValueError("history requires an admitted original SQUISH source")
    if len(row["house"].encode()) > shared.original.MAX_RECEIPT_BYTES:
        raise ValueError("history prior house exceeds the existing witness ceiling")
    try:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "original-house.yaml"
            path.write_text(row["house"])
            witness = shared.bounded_house(path)
        identity_matches = (
            witness["n"] == n
            and witness["id"] == f"W-known-best-n{n:03d}"
            and witness["source"]["key"] == source_key
            and witness["source"]["url"] == source_url
            and Fraction(witness["side"])
            == Fraction(case["reported_upper_bound"]["exact_form"])
        )
    except (ValueError, KeyError, TypeError, AttributeError) as error:
        raise ValueError("complete original prior house witness required") from error
    if not identity_matches:
        raise ValueError("complete original prior house identity/source/side required")


def validate_history(value: Any) -> list[dict[str, Any]]:
    """Validate the same complete original boundary before its first save or a retry."""
    if (
        type(value) is not dict
        or set(value) != {"format", "cases"}
        or value["format"] != HISTORY_FORMAT
        or type(value["cases"]) is not list
        or any(
            type(row) is not dict
            or set(row) != {"n", "frontier", "house"}
            or type(row["n"]) is not int
            or type(row["frontier"]) is not str
            or type(row["house"]) is not str
            for row in value["cases"]
        )
        or [row["n"] for row in value["cases"]] != list(houses.NUMBERS)
    ):
        raise ValueError("complete immutable previous Gupta frontier/house roster required")
    for row in value["cases"]:
        case = safe_load(row["frontier"].split("---\n", 2)[1])["packing"]
        if (
            case["n"] != row["n"]
            or case["reported_upper_bound"]["source_key"] == houses.reports.SOURCE_KEY
        ):
            raise ValueError("history requires every original pre-adoption source")
        validate_prior_house(row, case)
    return value["cases"]


def read_history() -> list[dict[str, Any]]:
    houses.reports.ensure_private(HISTORY)
    return validate_history(houses.reports.kernel.read_xz(HISTORY))


def record_cases() -> None:
    """Preflight all fourteen cases, atomically retain originals, then write any case.

    An interrupted run resumes from this complete original frontier/house roster;
    a subset or changed original cannot replace its immutable history.
    """
    houses.reports.check_certification()
    retained = read_history() if HISTORY.exists() else None
    originals = {} if retained is None else {row["n"]: row for row in retained}
    prior = []
    plan = []
    for n in houses.NUMBERS:
        path = FRONTIER / f"n-{n:03d}.md"
        houses.reports.ensure_private(path)
        current = path.read_text()
        _, front, body = current.split("---\n", 2)
        document = safe_load(front)
        case = document["packing"]
        if case["n"] != n:
            raise ValueError("case count differs from selected source scope")
        if case["reported_upper_bound"]["source_key"] == houses.reports.SOURCE_KEY:
            if retained is None or case["reported_upper_bound"] != reported_bound(n):
                raise ValueError("selected case lacks its complete original custody boundary")
            continue
        original = current if retained is None else originals[n]["frontier"]
        if current != original:
            raise ValueError("refuse changed historical source before any case write")
        certificate = houses.reports.read_fact(n)
        for lane in ("reported_upper_bound", "verified_upper_bound"):
            if certificate.side >= Fraction(case[lane]["exact_form"]):
                raise ValueError(f"n={n}: offered exact side is not smaller than both lanes")
        if case["conjectured_optimum"] is not None:
            raise ValueError("existing optimum conjecture requires an explicit disposition")
        prior.append(
            originals[n]
            if retained is not None
            else {"n": n, "frontier": current, "house": houses.house_path(n).read_text()}
        )
        old = copy.deepcopy(case["reported_upper_bound"])
        case["reported_upper_bound"] = reported_bound(n)
        case["rigidity"] = None
        case["source_reviewed"] = DAY
        if REPORT not in case["evidence"]:
            case["evidence"].append(REPORT)
        case["resources"].insert(
            0,
            {
                "key": houses.reports.SOURCE_KEY,
                "role": "upper-bound-report",
                "local": "web/gupta-square-packing-refinements-2026-10-08",
                "url": f"{houses.reports.SOURCE}/tree/{houses.reports.REVISION}",
                "retrieved": True,
            },
        )
        case["priority_notes"].append(
            {
                "claim": f"Earlier source ceiling {old['value']} from {old['source_key']}; "
                "the complete original frontier and house remain retained in the packet.",
                "claimed_by": old["found_by"],
                "published": old["source_date"],
                "year": old["found_year"],
            }
        )
        body = historical_prose(n, body).replace(
            FOOTER, section(n, confirmed=False) + "\n" + FOOTER
        )
        plan.append((path, "---\n" + dump(document) + "---\n" + body))
    if not plan:
        return
    if retained is None:
        boundary = {"format": HISTORY_FORMAT, "cases": prior}
        validate_history(boundary)
        houses.reports.save_xz(HISTORY, boundary)
    for path, text in plan:
        save(path, text)


def adopt_case(n: int, existing: str, generated: str) -> str:
    """Retain the selected source upper lane while ordinary lower lanes regenerate."""
    if n not in houses.NUMBERS:
        return generated
    _, front, body = existing.split("---\n", 2)
    document = safe_load(front)
    case = document["packing"]
    if case["reported_upper_bound"]["source_key"] != houses.reports.SOURCE_KEY:
        return generated
    houses.check_houses([n])
    old = next(row for row in read_history() if row["n"] == n)
    confirmed = houses.reports.EXACT_EVIDENCE in case["verified_upper_bound"]["evidence"]
    case["reported_upper_bound"] = reported_bound(n)
    case["verified_upper_bound"] = (
        houses.reports.confirmed_bound(n)
        if confirmed
        else safe_load(old["frontier"].split("---\n", 2)[1])["packing"]["verified_upper_bound"]
    )
    draft = safe_load(generated.split("---\n", 2)[1])["packing"]
    for field in ("reported_lower_bound", "verified_lower_bound", "reported_status", "status"):
        case[field] = draft[field]
    lower_pattern = r"\n## The lower bound\n.*?(?=\n<!-- BEGIN verification code)"
    lower = re.search(lower_pattern, generated.split("---\n", 2)[2], re.DOTALL)
    if lower is None:
        raise ValueError("generated lower-bound section missing")
    body, count = re.subn(lower_pattern, lambda _m: lower.group(), body, flags=re.DOTALL)
    if count != 1:
        raise ValueError("one retained lower-bound section required")
    pattern = rf"\n{SECTION}\n.*?(?=\n## |\n<!-- This document follows)"
    body, count = re.subn(
        pattern, lambda _m: section(n, confirmed=confirmed), body, flags=re.DOTALL
    )
    if count != 1:
        raise ValueError("one Gupta source construction section required")
    return render_case_verifiers.refresh("---\n" + dump(document) + "---\n" + body)


def register() -> None:
    record_cases()
    append_rows(
        FRONTIER / "evidence.yaml",
        "evidence",
        [
            {
                "id": REPORT,
                "claim": "upper-bound",
                "scope": {"n_values": list(houses.reports.NUMBERS)},
                "assurance": "reported",
                "reported_method": "exact-algebraic",
                "performed_by": "source-author",
                "relationship_to_generator": "same-implementation",
                "origin": "external",
                "novelty": "previously-published",
                "source_key": houses.reports.SOURCE_KEY,
                "certificate": PACKET_PATH
                + "/facts/complete-certificates-and-comparators.json.xz",
                "replay_status": "not-attempted",
                "verifiers": [],
                "source_reviewed": DAY,
                "limitations": "Seventeen complete originals; fourteen improve both "
                "current exact upper lanes, three withdrawn certificates remain retained. "
                "No optimizer, optimality, rigidity, priority or novelty is established.",
            }
        ],
        "id",
    )
    append_rows(
        FRONTIER / "results.yaml",
        "results",
        [
            {
                "id": RESULT,
                "kind": "upper-bound",
                "registered": DAY,
                "headline": "Fourteen rational refinements, seventeen complete source cases",
                "claim": "Seventeen complete rational source certificates are retained, "
                "three withdrawals; fourteen offer strictly smaller exact construction sides "
                "than both prior upper lanes. No lower bound or optimum is established.",
                "scope": {"n_values": list(houses.reports.NUMBERS)},
                "verification": "V0",
                "confirmation": "C0",
                "significance": {
                    "score": 3,
                    "rationale": "Fourteen strict finite upper-bound improvements; "
                    "no solved case or lower-bound theorem.",
                    "scored": DAY,
                    "by": "think-q3pd Gupta refinement import",
                },
                "novelty": "previously-published",
                "attribution": {"source_keys": [houses.reports.SOURCE_KEY], "published": DAY},
                "evidence": [REPORT],
                "artifacts": [
                    PACKET_PATH + "/README.md",
                    PACKET_PATH + "/facts/",
                    "packing/devtools/gupta_refinement_reports.py",
                ],
                "next_rung": "Native outcomes, source/house binding, independent review and "
                "actual private-worker custody are required before confirmation.",
                "notes": "SQUISH credit remains with Nate Chaoweeraprasit; source credits "
                "Evan Daniel's optimizer and Siddharth Gupta's precision refinements. "
                "Only factual inputs are copied; unlicensed programs/prose are hash-pinned.",
            }
        ],
        "id",
    )
    claims = {
        "results": [
            {
                "n": n,
                "offered_side": reported_bound(n)["value"],
                "exact_side": reported_bound(n)["exact_form"],
            }
            for n in houses.reports.NUMBERS
        ]
    }
    save(houses.reports.PACKET / "acquisition/claims.json", json.dumps(claims, indent=2) + "\n")
    append_rows(
        FRONTIER / "source-coverage.yaml",
        "sources",
        [
            {
                "id": SOURCE_ID,
                "title": "Gupta rational precision refinements, issue438",
                "role": "source-repository",
                "url": f"{houses.reports.SOURCE}/tree/{houses.reports.REVISION}",
                "local": "resources/web/gupta-square-packing-refinements-2026-10-08/",
                "source_key": houses.reports.SOURCE_KEY,
                "scope": {"n_values": list(houses.reports.NUMBERS)},
                "reviewed": DAY,
                "source_date": DAY,
                "disposition": "current-report",
                "replay_disposition": "case-specific",
                "represented_by": [f"frontier/n-{n:03d}.md" for n in houses.reports.NUMBERS],
                "claims_record": "resources/web/gupta-square-packing-refinements-2026-10-08/"
                "acquisition/claims.json",
                "evidence": [REPORT],
                "notes": "All seventeen originals and comparators retained; "
                "fourteen selected, three withdrawn after smaller ry-xu ceilings. "
                "Finite feasibility only.",
            }
        ],
        "id",
    )
    path = FRONTIER / "source-coverage.yaml"
    coverage = safe_load(path.read_text())
    for row in list(coverage["selected_overrides"]):
        if row["n"] not in houses.NUMBERS or row["source_id"] == SOURCE_ID:
            continue
        coverage["superseded_reports"].append(
            {
                "n": row["n"],
                "source_id": row["source_id"],
                "value": row["value"],
                "superseded_by": SOURCE_ID,
                "reason": "Complete Gupta source certificate is strictly smaller.",
            }
        )
        coverage["selected_overrides"].remove(row)
    for row in coverage["superseded_reports"]:
        if row["n"] in houses.NUMBERS:
            row["superseded_by"] = SOURCE_ID
    for n in houses.NUMBERS:
        if not any(row["n"] == n for row in coverage["selected_overrides"]):
            coverage["selected_overrides"].append(
                {
                    "n": n,
                    "source_id": SOURCE_ID,
                    "value": reported_bound(n)["value"],
                    "evidence": REPORT,
                    "reason": "The complete rational precision refinement is strictly "
                    "smaller than both previous exact upper lanes.",
                }
            )
    selected = {row["n"]: row for row in coverage["selected_overrides"]}
    for n in houses.reports.NUMBERS:
        if n in houses.NUMBERS or any(
            row["n"] == n and row["source_id"] == SOURCE_ID
            for row in coverage["superseded_reports"]
        ):
            continue
        coverage["superseded_reports"].append(
            {
                "n": n,
                "source_id": SOURCE_ID,
                "value": reported_bound(n)["value"],
                "superseded_by": selected[n]["source_id"],
                "reason": "The withdrawn Gupta rational certificate is larger than "
                "the selected ry-xu construction; its complete source and replay "
                "remain retained.",
            }
        )
    coverage["selected_overrides"].sort(key=lambda row: row["n"])
    save(path, dump(coverage))


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    register()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
