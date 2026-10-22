"""Coverage reports distinguish exact join gaps from unprofiled labels and unregistered work."""

from __future__ import annotations

from dataclasses import replace

import pytest

from devtools.profile_coverage import coverage_report
from sqpack.contributor_occurrences import CreditOccurrence, CreditOrigin
from sqpack.contributors import ContributorRegistry, load_contributors

BIBLIOGRAPHY = "packing/resources/bibliography.yaml"


@pytest.fixture(scope="module")
def profiles() -> ContributorRegistry:
    return load_contributors()


def span(key: str, field: str, label: str, *, person: str | None = None) -> CreditOccurrence:
    return CreditOccurrence(
        CreditOrigin(BIBLIOGRAPHY, key, field),
        label,
        0,
        len(label),
        label,
        "source-author" if field.startswith("/authors/") else "prerequisite",
        "resolved" if person else "unresolved",
        person,
        ("byline",) if person else (),
    )


def test_exact_alias_candidates_remain_join_gaps_and_unknown_authors_remain_unassigned(
    profiles: ContributorRegistry,
) -> None:
    occurrences = [
        span("original", "/authors/0", "Stromquist", person="walter-stromquist"),
        span("modern", "/credit", "Stromquist"),
        span("modern", "/authors/0", "Unprofiled Author"),
        span("other", "/credit", "Kearney"),
    ]
    records = [
        {
            "id": "T-high",
            "significance": {"score": 5},
            "attribution": {"source_keys": ["modern"]},
            "builds_on": {"source_keys": ["original"]},
        }
    ]
    report = coverage_report(
        profiles,
        occurrences,
        records,
        {"original": {"year": 2003}},
        {},
        source_coverage=[],
        pending_pdf_paths=[],
    )
    labels = {row["label"]: row for row in report["pending_identity_labels"]}
    assert labels["Stromquist"]["occurrence_count"] == 1
    assert labels["Stromquist"]["candidate_ids"] == ["walter-stromquist"]
    assert labels["Stromquist"]["related_result_ids"] == ["T-high"]
    assert labels["Unprofiled Author"]["candidate_ids"] == []
    gap = report["missing_joins"][0]
    assert gap["label"] == "Stromquist"
    assert gap["candidate_ids"] == ["walter-stromquist"]
    assert gap["disposition"] == "unresolved"
    assert gap["origin"]["field"] == "/credit"
    assert gap["high_significance_relations"] == [
        {
            "result_id": "T-high",
            "significance": 5,
            "relation": "credited-source",
        }
    ]
    missing = report["missing_profile_candidates"]
    assert len(missing) == 1
    assert missing[0]["label"] == "Unprofiled Author"
    assert missing[0]["candidate_ids"] == []
    assert missing[0]["high_significance_relations"][0]["relation"] == "primary-source-author"
    person = next(row for row in report["profiles"] if row["id"] == "walter-stromquist")
    assert person["activity_years"] == [2003]
    assert person["primary_results"] == person["credited_results"] == []
    assert report["authored_sources_without_primary_results"] == [
        {
            "source_key": "original",
            "reviewed_author_ids": ["walter-stromquist"],
            "year": 2003,
            "basis_for": ["T-high"],
            "source_coverage_disposition": None,
            "source_scope": None,
            "source_id": None,
            "represented_by": [],
            "claims_record": None,
            "beyond_horizon_claims": [],
            "tracking_status": "bibliography-only",
            "status": "primary-result-projection-review",
        }
    ]


def test_pdf_inventory_prioritizes_explicit_packets_without_claiming_inspection(
    profiles: ContributorRegistry,
) -> None:
    records = [
        {
            "id": "T-high",
            "significance": {"score": 4},
            "attribution": {"source_keys": ["high"]},
        },
        {"id": "T-low", "significance": {"score": 3}, "attribution": {"source_keys": ["low"]}},
    ]
    coverage = [
        {"source_key": "high", "local": "resources/web/high/"},
        {"source_key": "low", "local": "resources/web/low/"},
    ]
    paths = ["packing/resources/web/high/proof.pdf", "packing/resources/web/low/proof.pdf"]
    report = coverage_report(
        profiles, [], records, {}, {}, source_coverage=coverage, pending_pdf_paths=paths
    )
    assert [row["id"] for row in report["high_significance_results"]] == ["T-high"]
    high, low = report["pending_pdf_inspections"]
    assert high["status"] == low["status"] == "pending-full-credit-inspection"
    assert high["high_significance_relations"] == [
        {
            "result_id": "T-high",
            "source_key": "high",
            "relation": "retained-source-packet",
            "significance": 4,
        }
    ]
    assert low["high_significance_relations"] == []


def test_proposed_fields_and_basis_citations_do_not_become_reviewed_personal_credits(
    profiles: ContributorRegistry,
) -> None:
    proposed = replace(span("old", "/authors/0", "Stromquist"), disposition="unreviewed")
    report = coverage_report(
        profiles,
        [],
        [{"id": "T-high", "significance": {"score": 5}, "builds_on": {"source_keys": ["old"]}}],
        {},
        {},
        source_coverage=[],
        pending_pdf_paths=[],
        unreviewed=[proposed],
    )
    assert report["missing_joins"][0]["disposition"] == "unreviewed"
    assert (
        report["missing_joins"][0]["high_significance_relations"][0]["relation"]
        == "basis-publication"
    )
    assert report["primary_result_count"] == report["credited_person_result_count"] == 0


def test_existing_source_and_beyond_horizon_claim_records_are_not_missing_registration(
    profiles: ContributorRegistry,
) -> None:
    claim = {
        "source_id": "source-one",
        "n": 400,
        "claim": "upper-bound",
        "value": "19.99",
        "assurance": "reported",
        "disposition": "tracked-outside-case-corpus",
    }
    report = coverage_report(
        profiles,
        [span("source", "/authors/0", "Stromquist", person="walter-stromquist")],
        [],
        {"source": {"year": 2003}},
        {},
        source_coverage=[
            {
                "id": "source-one",
                "source_key": "source",
                "disposition": "current-report",
                "scope": {"n_values": [400]},
                "claims_record": "resources/source/claims.json",
                "represented_by": ["resources/source/README.md"],
            }
        ],
        pending_pdf_paths=[],
        beyond_horizon_claims=[claim],
    )
    (row,) = report["authored_sources_without_primary_results"]
    assert row["tracking_status"] == "beyond-case-corpus-recorded"
    assert row["beyond_horizon_claims"] == [claim]
    assert row["claims_record"] == "resources/source/claims.json"
    assert row["represented_by"] == ["resources/source/README.md"]
    assert row["status"] == "primary-result-projection-review"
    assert report["primary_result_count"] == 0


def test_manual_json_credit_is_retained_without_inventing_result_associations(
    profiles: ContributorRegistry,
) -> None:
    manual = replace(
        span("$", "/lower_bounds/contributors/12/name", "Unprofiled Author"),
        origin=CreditOrigin(
            "packing/atlas/known-best/credit-attributions.json",
            "$",
            "/lower_bounds/contributors/12/name",
        ),
        role="credited-contributor",
    )
    report = coverage_report(
        profiles, [manual], [], {}, {}, source_coverage=[], pending_pdf_paths=[]
    )
    (row,) = report["missing_profile_candidates"]
    assert row["origin"]["path"].endswith("credit-attributions.json")
    assert row["origin"]["field"] == "/lower_bounds/contributors/12/name"
    assert row["high_significance_relations"] == []
    assert report["credited_person_result_count"] == 0
