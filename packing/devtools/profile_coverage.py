"""Read-only profile coverage, prioritizing S5/S4 evidence without assigning identities.

Run `python -m devtools.profile_coverage --minimum-significance 4 --json` from packing.
Candidates are exact existing alias matches for review, never authorization to join.
An authored source absent from primary register attributions may already have source-specific
claim or beyond-horizon records. This is a projection audit, not an instruction to create
duplicate mathematical results. PDF packet links locate inspection work;
they do not say that every PDF in the packet was directly cited by each result.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, replace
from pathlib import Path, PurePosixPath
from typing import Any

from devtools.contributor_census import (
    census,
    needs_boundary_or_non_person_review,
    structured_occurrences,
)
from devtools.site_tallies import person_activity_years, person_credit_stats
from sqpack.contributor_occurrences import CreditOccurrence, load_occurrences, source_document
from sqpack.contributors import PEOPLE_DIR, ContributorRegistry, load_contributors
from sqpack.project import require_project_root
from sqpack.yamlio import load_yaml

BIBLIOGRAPHY = "packing/resources/bibliography.yaml"
REGISTER = "packing/frontier/results.yaml"
_AUTHOR_FIELD = re.compile(r"/authors/[0-9]+")
_CREDIT_FIELD = re.compile(r"/builds_on/credit/[0-9]+")


def _keys(record: Mapping[str, Any], field: str) -> set[str]:
    return set((record.get(field) or {}).get("source_keys", ()))


def _relations(
    item: CreditOccurrence, records: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    related = []
    origin = item.origin
    for record in records:
        relation = None
        if origin.path == BIBLIOGRAPHY:
            if origin.record_key in _keys(record, "attribution"):
                if _AUTHOR_FIELD.fullmatch(origin.field):
                    relation = "primary-source-author"
                elif origin.field == "/credit":
                    relation = "credited-source"
            elif origin.record_key in _keys(record, "builds_on"):
                relation = "basis-publication"
        elif (
            origin.path == REGISTER
            and origin.record_key == str(record["id"])
            and _CREDIT_FIELD.fullmatch(origin.field)
        ):
            relation = "result-credit"
        if relation is not None:
            related.append(
                {
                    "result_id": str(record["id"]),
                    "significance": int(record["significance"]["score"]),
                    "relation": relation,
                }
            )
    return related


def _pdf_relations(
    path: str,
    records: Sequence[Mapping[str, Any]],
    source_coverage: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    coverage = {row["source_key"]: row for row in source_coverage if row.get("source_key")}
    related: dict[tuple[str, str, str], dict[str, Any]] = {}
    for record in records:
        result_id = str(record["id"])
        for key in _keys(record, "attribution") | _keys(record, "builds_on"):
            local = coverage.get(key, {}).get("local")
            if not isinstance(local, str):
                continue
            retained = "packing/" + local.removeprefix("packing/")
            if path == retained or (retained.endswith("/") and path.startswith(retained)):
                related[result_id, key, "retained-source"] = {
                    "result_id": result_id,
                    "source_key": key,
                    "relation": "retained-source-packet",
                    "significance": record["significance"]["score"],
                }
        for raw_artifact in record.get("artifacts", ()):
            artifact = str(raw_artifact)
            if path == artifact:
                related[result_id, artifact, "artifact"] = {
                    "result_id": result_id,
                    "artifact": artifact,
                    "relation": "explicit-artifact",
                    "significance": record["significance"]["score"],
                }
            elif (
                artifact.startswith("packing/resources/web/")
                and PurePosixPath(artifact).name == "README.md"
            ):
                packet = str(PurePosixPath(artifact).parent) + "/"
                if path.startswith(packet):
                    related[result_id, packet, "packet"] = {
                        "result_id": result_id,
                        "artifact": artifact,
                        "relation": "same-retained-packet",
                        "significance": record["significance"]["score"],
                    }
    return list(related.values())


def coverage_report(
    profiles: ContributorRegistry,
    occurrences: Sequence[CreditOccurrence],
    records: Sequence[Mapping[str, Any]],
    bibliography: Mapping[str, Mapping[str, Any]],
    cases: Mapping[str, Mapping[str, Any]],
    *,
    source_coverage: Sequence[Mapping[str, Any]],
    pending_pdf_paths: Iterable[str],
    minimum_significance: int = 4,
    unreviewed: Sequence[CreditOccurrence] = (),
    beyond_horizon_claims: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Project exact coverage gaps without changing evidence status or identity bindings."""
    selected = [
        record for record in records if record["significance"]["score"] >= minimum_significance
    ]
    people = []
    for identifier, person in profiles.by_id.items():
        stats = person_credit_stats(identifier, occurrences, records)
        people.append(
            {
                "id": identifier,
                "name": person.display_name,
                "activity_years": list(
                    person_activity_years(identifier, occurrences, bibliography, cases, records)
                ),
                "primary_results": list(stats.results),
                "credited_results": list(stats.credited_results),
                "reviewed_spans": stats.reviewed_spans,
            }
        )
    missing_joins, missing_profiles = [], []
    for item in (*occurrences, *unreviewed):
        if item.disposition not in {"unresolved", "unreviewed"}:
            continue
        candidates = sorted(person.id for person in profiles.candidates(item.label))
        row = {
            "kind": "missing-join" if candidates else "missing-profile-candidate",
            "origin": asdict(item.origin),
            "start": item.start,
            "end": item.end,
            "expected_text": item.expected_text,
            "label": item.label,
            "role": item.role,
            "disposition": item.disposition,
            "candidate_ids": candidates,
            "boundary_or_non_person_review": needs_boundary_or_non_person_review(item.label),
            "high_significance_relations": _relations(item, selected),
        }
        (missing_joins if candidates else missing_profiles).append(row)
    for pending in (missing_joins, missing_profiles):
        pending.sort(
            key=lambda row: (
                -max(
                    (item["significance"] for item in row["high_significance_relations"]),
                    default=0,
                ),
                row["origin"]["path"],
                row["origin"]["record_key"],
                row["origin"]["field"],
                row["start"],
            )
        )
    pending_labels = []
    for label in sorted({row["label"] for row in (*missing_joins, *missing_profiles)}):
        matches = [row for row in (*missing_joins, *missing_profiles) if row["label"] == label]
        pending_labels.append(
            {
                "label": label,
                "occurrence_count": len(matches),
                "candidate_ids": sorted(
                    {identifier for row in matches for identifier in row["candidate_ids"]}
                ),
                "roles": sorted({row["role"] for row in matches}),
                "boundary_or_non_person_review": any(
                    row["boundary_or_non_person_review"] for row in matches
                ),
                "related_result_ids": sorted(
                    {
                        related["result_id"]
                        for row in matches
                        for related in row["high_significance_relations"]
                    }
                ),
            }
        )
    attributed = {key for record in records for key in _keys(record, "attribution")}
    authored: dict[str, set[str]] = {}
    for item in occurrences:
        if (
            item.disposition == "resolved"
            and item.contributor_id
            and item.role == "source-author"
            and item.origin.path == BIBLIOGRAPHY
            and _AUTHOR_FIELD.fullmatch(item.origin.field)
        ):
            authored.setdefault(item.origin.record_key, set()).add(item.contributor_id)
    source_rows = {row["source_key"]: row for row in source_coverage if row.get("source_key")}
    unregistered = [
        {
            "source_key": key,
            "reviewed_author_ids": sorted(identifiers),
            "year": bibliography.get(key, {}).get("year"),
            "basis_for": [
                str(record["id"]) for record in records if key in _keys(record, "builds_on")
            ],
            "source_coverage_disposition": source_rows.get(key, {}).get("disposition"),
            "source_scope": source_rows.get(key, {}).get("scope"),
            "source_id": source_rows.get(key, {}).get("id"),
            "represented_by": source_rows.get(key, {}).get("represented_by", []),
            "claims_record": source_rows.get(key, {}).get("claims_record"),
            "beyond_horizon_claims": [
                dict(claim)
                for claim in beyond_horizon_claims
                if claim["source_id"] == source_rows.get(key, {}).get("id")
            ],
            "tracking_status": (
                "beyond-case-corpus-recorded"
                if any(
                    claim["source_id"] == source_rows.get(key, {}).get("id")
                    for claim in beyond_horizon_claims
                )
                else "source-claims-recorded"
                if source_rows.get(key, {}).get("claims_record")
                else "source-coverage-recorded"
                if key in source_rows
                else "bibliography-only"
            ),
            "status": "primary-result-projection-review",
        }
        for key, identifiers in sorted(authored.items())
        if key not in attributed
    ]
    pdfs = [
        {
            "path": path,
            "status": "pending-full-credit-inspection",
            "high_significance_relations": _pdf_relations(path, selected, source_coverage),
        }
        for path in sorted(set(pending_pdf_paths))
    ]
    authored_evidence = {
        (item.contributor_id, source_id)
        for item in occurrences
        if item.disposition == "resolved"
        and item.role == "source-author"
        and item.origin.path == BIBLIOGRAPHY
        and _AUTHOR_FIELD.fullmatch(item.origin.field)
        for source_id in item.evidence
    }
    source_evidence_gaps = [
        {
            "profile_id": identifier,
            **asdict(source),
            "status": "source-kind-and-authorship-review",
        }
        for identifier, person in profiles.by_id.items()
        for source in person.sources
        if (identifier, source.id) not in authored_evidence
    ]
    return {
        "minimum_significance": minimum_significance,
        "profile_count": len(people),
        "profiles": people,
        "primary_result_count": len(
            {result for person in people for result in person["primary_results"]}
        ),
        "credited_person_result_count": sum(
            len(person["credited_results"]) for person in people
        ),
        "high_significance_results": [
            {
                "id": str(record["id"]),
                "significance": record["significance"]["score"],
                "primary_profile_ids": [
                    person["id"]
                    for person in people
                    if str(record["id"]) in person["primary_results"]
                ],
                "credited_profile_ids": [
                    person["id"]
                    for person in people
                    if str(record["id"]) in person["credited_results"]
                ],
            }
            for record in selected
        ],
        "pending_identity_labels": pending_labels,
        "missing_joins": missing_joins,
        "missing_profile_candidates": missing_profiles,
        "authored_sources_without_primary_results": unregistered,
        "profile_sources_without_author_join": source_evidence_gaps,
        "pdf_association_limit": (
            "Only explicit source-coverage paths and result artifacts are joined; "
            "transcription siblings and prose citations require inspection."
        ),
        "pending_pdf_inspections": pdfs,
    }


def audit_repository(repo: Path, *, minimum_significance: int = 4) -> dict[str, Any]:
    """Read source records and the retained census without writing files or identity joins."""
    packing = repo / "packing"
    profiles = load_contributors(packing / PEOPLE_DIR, repo=repo)
    registry = load_occurrences(repo=repo, profiles=profiles)
    baseline = census(repo, registry)
    sources = load_yaml((repo / BIBLIOGRAPHY).read_text())["sources"]
    records = load_yaml((repo / REGISTER).read_text())["results"]
    case_paths = {
        item.origin.path
        for item in registry.occurrences
        if item.origin.path.startswith("packing/frontier/n-")
    }
    cases = {path: source_document(repo / path)["packing"] for path in case_paths}
    unreviewed = [
        replace(item, disposition="unreviewed")
        for item in structured_occurrences(repo)
        if item.origin not in registry.by_origin
    ]
    coverage = load_yaml((packing / "frontier/source-coverage.yaml").read_text())
    report = coverage_report(
        profiles,
        registry.occurrences,
        records,
        {row["key"]: row for row in sources},
        cases,
        source_coverage=coverage["sources"],
        beyond_horizon_claims=coverage["beyond_horizon_claims"],
        pending_pdf_paths=baseline["pending_pdf_paths"],
        minimum_significance=minimum_significance,
        unreviewed=unreviewed,
    )
    report["identity_census"] = {
        key: baseline[key] for key in ("dispositions", "pdfs", "manual_origin_count")
    }
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minimum-significance", type=int, choices=range(1, 6), default=4)
    parser.add_argument(
        "--json", action="store_true", help="Print every exact gap and profile metric."
    )
    args = parser.parse_args(argv)
    report = audit_repository(
        require_project_root().parent, minimum_significance=args.minimum_significance
    )
    if args.json:
        output = report
    else:
        output = {
            key: report[key]
            for key in (
                "profile_count",
                "primary_result_count",
                "credited_person_result_count",
                "identity_census",
            )
        }
        output["gaps"] = {
            key: len(report[key])
            for key in (
                "missing_joins",
                "missing_profile_candidates",
                "authored_sources_without_primary_results",
                "pending_pdf_inspections",
            )
        }
        output["pending_identity_labels"] = report["pending_identity_labels"]
        output["high_significance_gap_kinds"] = dict(
            Counter(
                row["kind"]
                for key in ("missing_joins", "missing_profile_candidates")
                for row in report[key]
                if row["high_significance_relations"]
            )
        )
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
