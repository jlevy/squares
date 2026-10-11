"""Contribution accents date the displayed construction and verified proof separately."""

from __future__ import annotations

from dataclasses import replace
from datetime import timedelta
from typing import Any

import pytest

from devtools import build_bound_citations as citations
from devtools.result_status import (
    RecentContributions,
    recent_contributions,
    recent_contributions_by_case,
)


def _register() -> citations.Register:
    return citations.Register(
        evidence={
            "E-upper": {
                "claim": "upper-bound",
                "assurance": "verified",
                "novelty": "previously-published",
                "performed_by": "source",
                "source_key": "old",
            },
            "E-lower": {
                "claim": "lower-bound",
                "assurance": "verified",
                "novelty": "previously-published",
                "performed_by": "source",
                "source_key": "old",
            },
            "E-grid": {"novelty": "common-knowledge"},
        },
        results=(),
        sources={
            "old": citations.Source("old", ("Original Author",), 1979, "paper"),
            "recent": citations.Source(
                "recent", ("New Author",), 2026, "paper", dated=citations.RECENT_SINCE
            ),
        },
        names={},
    )


def _case() -> dict[str, Any]:
    return {
        "status": "proved",
        "reported_upper_bound": {
            "value": "4",
            "evidence": ["E-upper"],
            "source_key": "old",
        },
        "verified_upper_bound": {"value": "4", "evidence": ["E-upper"]},
        "verified_lower_bound": {"value": "4", "evidence": ["E-lower"]},
    }


def test_recent_verification_does_not_redate_a_historical_construction() -> None:
    register = _register()
    certificate = {
        **register.evidence["E-upper"],
        "source_key": "recent",
        "performed_by": "repository",
        "novelty": "confirmed-novel",
        "replay_status": "passed",
    }
    register = replace(register, evidence={**register.evidence, "E-certificate": certificate})
    case = _case()
    case["verified_upper_bound"]["evidence"] = ["E-certificate"]
    flags = recent_contributions(12, case, register)
    assert flags == RecentContributions(upper=False, lower=False, optimal=False)
    assert not flags.any


@pytest.mark.parametrize(("days", "expected"), [(-1, False), (0, True), (1, True)])
def test_upper_uses_the_shared_inclusive_source_date_cutoff(
    *, days: int, expected: bool
) -> None:
    register = _register()
    source = replace(
        register.sources["recent"], dated=citations.RECENT_SINCE + timedelta(days=days)
    )
    register = replace(register, sources={**register.sources, "recent": source})
    case = _case()
    case["reported_upper_bound"]["source_key"] = "recent"
    # Recency does not upgrade a reported construction's assurance or establish a proof.
    case["reported_upper_bound"]["value"] = "3.9"
    case["status"] = "open"
    assert recent_contributions(12, case, register) == RecentContributions(
        upper=expected, lower=False, optimal=False
    )


def test_a_novel_first_party_construction_is_recent_without_redating_its_certificate() -> None:
    register = _register()
    upper = {
        **register.evidence["E-upper"],
        "performed_by": "repository",
        "novelty": "apparently-novel",
    }
    register = replace(register, evidence={**register.evidence, "E-upper": upper})
    flags = recent_contributions(12, _case(), register)
    assert flags == RecentContributions(upper=True, lower=False, optimal=False)
    assert flags.any


def test_common_knowledge_grid_does_not_inherit_a_recent_catalogue_date() -> None:
    case = _case()
    case["reported_upper_bound"]["source_key"] = "recent"
    case["verified_upper_bound"]["evidence"] = ["E-grid"]
    case["verified_lower_bound"]["evidence"] = ["E-grid"]
    assert recent_contributions(16, case, _register()) == RecentContributions(
        upper=False, lower=False, optimal=False
    )


@pytest.mark.parametrize(("status", "optimal"), [("proved", True), ("open", False)])
def test_a_recent_verified_lower_proof_contributes_only_declared_optimality(
    *, status: str, optimal: bool
) -> None:
    register = _register()
    lower = {**register.evidence["E-lower"], "claim": "exact-value", "source_key": "recent"}
    register = replace(register, evidence={**register.evidence, "E-lower": lower})
    case = _case()
    case["status"] = status
    # Both lanes have the same printed number in either case. Only the declared proof
    # status permits an optimality mark; equality alone does not.
    assert recent_contributions(12, case, register) == RecentContributions(
        upper=False, lower=True, optimal=optimal
    )


@pytest.mark.parametrize(
    "unsupported",
    [{"assurance": "reported"}, {"replay_status": "failed"}, {"claim": "upper-bound"}],
)
def test_a_recent_source_without_a_valid_lower_proof_cannot_accent_optimality(
    unsupported: dict[str, str],
) -> None:
    register = _register()
    lower = {**register.evidence["E-lower"], "source_key": "recent", **unsupported}
    register = replace(register, evidence={**register.evidence, "E-lower": lower})
    assert recent_contributions(12, _case(), register) == RecentContributions(
        upper=False, lower=False, optimal=False
    )


def test_recent_reproof_preserves_the_original_lower_proof_date() -> None:
    register = _register()
    replay = {
        **register.evidence["E-lower"],
        "source_key": "recent",
        "performed_by": "repository",
        "replay_status": "passed",
    }
    register = replace(register, evidence={**register.evidence, "E-replay": replay})
    case = _case()
    case["verified_lower_bound"]["evidence"].append("E-replay")
    assert recent_contributions(12, case, register) == RecentContributions(
        upper=False, lower=False, optimal=False
    )


def test_an_unverified_report_does_not_replace_the_displayed_verified_lower_proof() -> None:
    case = _case()
    case["reported_lower_bound"] = {
        "value": "4",
        "source_key": "recent",
        "evidence": ["E-report"],
    }
    assert recent_contributions(12, case, _register()) == RecentContributions(
        upper=False, lower=False, optimal=False
    )


def test_missing_construction_provenance_is_an_error_not_an_old_result() -> None:
    case = _case()
    case["reported_upper_bound"]["source_key"] = "missing"
    with pytest.raises(ValueError, match="n=12: upper construction has no bibliography source"):
        recent_contributions(12, case, _register())


def test_live_corpus_separates_the_new_n11_proof_from_the_historical_upper() -> None:
    flags = recent_contributions_by_case()
    assert set(flags) == set(citations.CORPUS.numbers)
    assert flags[11] == RecentContributions(upper=False, lower=True, optimal=True)
    assert flags[211] == RecentContributions(upper=True, lower=True, optimal=False)
    assert flags[153].upper
    assert flags[16] == RecentContributions(upper=False, lower=False, optimal=False)
    # The new helper preserves the citation module's established lower-bound meaning
    # across the corpus while adding independently usable upper and optimality flags.
    assert {
        n for n, contribution in flags.items() if contribution.lower
    } == citations.recent_lower_bounds()
