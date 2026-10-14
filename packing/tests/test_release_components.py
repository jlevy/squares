"""Independent public editions and release-impact decisions."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from sqpack import release


def test_component_histories_resolve_retained_editions_and_preserve_draft_labels() -> None:
    assert release.component_history("site") is release.PUBLICATION_HISTORY
    assert release.component_history("infographics") is release.INFOGRAPHIC_HISTORY
    assert release.INFOGRAPHIC_HISTORY[0].version == release.INFOGRAPHIC_VERSION
    assert release.INFOGRAPHIC_HISTORY[-1].version == "v0.5.0"
    assert release.INFOGRAPHIC_HISTORY[-1].first_published == "October 2, 2026"
    assert (
        release.component_history("paper:n11-lower-bounds-explainer")
        is release.EXPLAINER_HISTORY
    )
    assert (
        release.component_history("paper:n11-optimality-review")
        is release.OPTIMALITY_REVIEW_HISTORY
    )
    assert (
        release.component_history("paper:n11-threshold-bound-review")
        is release.THRESHOLD_REVIEW_HISTORY
    )
    assert (
        release.component_history("paper:square-packing-methods-survey")
        is release.PACKING_METHODS_HISTORY
    )
    assert release.OPTIMALITY_REVIEW_EDITION.startswith("Draft ")
    assert release.THRESHOLD_REVIEW_EDITION.startswith("Draft ")
    with pytest.raises(ValueError, match="unknown release component"):
        release.component_history("paper:unknown")


@pytest.mark.parametrize(("impact", "expected"), [("patch", "v0.5.4"), ("minor", "v0.6.0")])
def test_impact_selects_one_successor_for_the_complete_batch(
    impact: release.ReleaseImpact, expected: str
) -> None:
    assert release.successor_version("v0.5.3", impact) == expected


def test_new_cuts_require_owned_impact_decisions_and_untouched_papers_do_not(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    previous = release.component_version("site")
    version = release.successor_version(previous, "minor")
    entry = release.PublicationHistoryEntry(version, "October 13, 2026", "Add a capability.")
    monkeypatch.setattr(release, "PUBLICATION_HISTORY", (entry, *release.PUBLICATION_HISTORY))
    with pytest.raises(ValueError, match="needs a release-impact decision"):
        release.validate_release_impacts()
    decision = release.ReleaseImpactDecision(
        "site", previous, version, "minor", "Add a capability."
    )
    decisions = [decision, *release.RELEASE_IMPACTS]
    release.validate_release_impacts(decisions, externally_changed=["site"])
    release.validate_release_impacts(
        decisions,
        externally_changed=["site"],
        previous_versions={"site": previous},
    )
    with pytest.raises(ValueError, match="needs a successor to"):
        release.validate_release_impacts(
            decisions,
            externally_changed=["site"],
            previous_versions={"site": version},
        )
    assert (
        release.component_version("paper:n11-optimality-review")
        == release.OPTIMALITY_REVIEW_VERSION
    )
    with pytest.raises(ValueError, match="requires its patch successor"):
        release.validate_release_impacts(
            [decision._replace(impact="patch"), *release.RELEASE_IMPACTS]
        )
    with pytest.raises(ValueError, match="unretained edition"):
        release.validate_release_impacts(
            [decision._replace(component="infographics"), *release.RELEASE_IMPACTS]
        )
    without_infographics = [item for item in decisions if item.component != "infographics"]
    with pytest.raises(ValueError, match=r"infographics.*needs.*release-impact decision"):
        release.validate_release_impacts(
            without_infographics, externally_changed=["infographics"]
        )


def test_retained_policy_era_cuts_all_have_owned_impact_decisions() -> None:
    release.validate_release_impacts()


def test_published_infographic_baseline_reads_main_without_executing_prior_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = (
        'PUBLICATION_HISTORY = (PublicationHistoryEntry(version="v0.5.0"),)\n'
        'raise RuntimeError("prior source must never execute")\n'
    )

    def git(args: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        assert args[-1] == "origin/main:packing/src/sqpack/release.py"
        return subprocess.CompletedProcess(args, 0, stdout=source, stderr="")

    monkeypatch.setattr(release.subprocess, "run", git)
    assert release.published_infographic_version(Path("/in-memory-repository")) == "v0.5.0"
    source += 'INFOGRAPHIC_HISTORY = (PublicationHistoryEntry(version="v0.6.0"),)\n'
    assert release.published_infographic_version(Path("/in-memory-repository")) == "v0.6.0"
    source += "INFOGRAPHIC_HISTORY = ()\n"
    with pytest.raises(ValueError, match="literal published infographic"):
        release.published_infographic_version(Path("/in-memory-repository"))
