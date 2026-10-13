"""A project document's place and name say what kind of document it is (think-mv16)."""

from __future__ import annotations

import pytest

from devtools import check_documentation
from devtools.check_documentation import _layout_problems

LOOSE = "sits loose in docs/project/; put it in the directory for its kind"
NOT_KEBAB = "is not named in lowercase kebab-case"
#: The pending list as the check was written, 2026-10-12. A finished move removes its
#: entry; nothing is added, which is what keeps the list a record of the backlog.
PENDING_AT_START = frozenset(
    {
        "SYNOPSIS.md",
        "TUTORIAL.md",
        "docs/project/site-urls.md",
        "packing/frontier/CERTIFICATE-REACH.md",
        "packing/frontier/INVENTORY.md",
        "packing/frontier/RESULTS.md",
        "packing/frontier/STATUS.md",
        "packing/frontier/VERIFIERS.md",
        "packing/sqverify_fast/INDEPENDENCE.md",
        "packing/sqverify_fast/SOUNDNESS.md",
    }
)
PENDING = check_documentation.LAYOUT_PENDING

# Exercise the rule directly; a whole document-map fixture would hide the case.
# pyright: reportPrivateUsage=false


@pytest.fixture(autouse=True)
def nothing_pending(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(check_documentation, "LAYOUT_PENDING", frozenset())


def test_documents_in_their_places_pass() -> None:
    assert (
        _layout_problems(
            {
                "README.md",
                "docs/project/README.md",
                "docs/project/guides/verification-tooling.md",
                "docs/project/policies/regularization-policy.md",
                "docs/project/handoffs/handoff-2026-09-04-block-close.md",
                "docs/project/reviews/README.md",
                "docs/project/reviews/review-2026-10-04-n11-optimality-paper-v0.1.4-changes.md",
                "docs/project/specs/active/spike-2026-08-25-n5-motion-lab.md",
                "packing/campaign/hypotheses/H-093-n11-scalar-61-16-certificate.md",
                "packing/campaign/explorations/X048-session-171-raw-row-support/d1-report.md",
            }
        )
        == []
    )


def test_a_loose_project_document_is_refused() -> None:
    """The case that prompted the rule: a new handoff beside the directories."""
    loose = "docs/project/handoff-2026-10-10-polynomial-pr-stack.md"
    assert _layout_problems({loose}) == [f"{loose}: {LOOSE}"]


def test_a_project_document_needs_a_directory_for_its_kind() -> None:
    notes = "docs/project/notes/anything.md"
    capitalized = "docs/project/Guides/tutorial.md"
    assert _layout_problems({notes, capitalized}) == [
        f"{capitalized}: is in docs/project/Guides/, which is not a directory for a kind",
        f"{notes}: is in docs/project/notes/, which is not a directory for a kind",
    ]


def test_a_dated_directory_wants_its_kind_and_a_real_date() -> None:
    undated = "docs/project/reviews/stromquist-helper-arguments-math-review.md"
    misfiled = "docs/project/handoffs/review-2026-09-07-misfiled.md"
    impossible = "docs/project/handoffs/handoff-2026-99-99-x.md"
    plan = "docs/project/specs/active/plan-2026-10-11-documentation-organization.md"
    assert _layout_problems({undated, misfiled, impossible, plan}) == [
        f"{impossible}: is not named handoff-YYYY-MM-DD-topic.md",
        f"{misfiled}: is not named handoff-YYYY-MM-DD-topic.md",
        f"{undated}: is not named review-YYYY-MM-DD-topic.md",
    ]


def test_a_name_is_lowercase_kebab_case_or_a_registered_id() -> None:
    playbook = "packing/atlas/known-best/FIGURE-PLAYBOOK.md"
    report = "packing/campaign/explorations/X048-session-171-raw-row-support/D1_REPORT.md"
    snake = "packing/devtools/foo_bar.md"
    unregistered = "packing/foo/README-1-x.md"
    exploration = "packing/campaign/explorations/X-015-the-map-and-the-three-programs.md"
    experiment = "packing/benchmarks/validation-efficiency/VE-001-fast-gate.md"
    named = {"AGENTS.md", playbook, report, snake, unregistered, exploration, experiment}
    assert _layout_problems(named) == [
        f"{playbook}: {NOT_KEBAB}",
        f"{report}: {NOT_KEBAB}",
        f"{snake}: {NOT_KEBAB}",
        f"{unregistered}: {NOT_KEBAB}",
    ]


def test_a_pending_entry_is_excused_until_it_moves(monkeypatch: pytest.MonkeyPatch) -> None:
    """An entry is excused while it breaks the rule, and refused once it no longer does."""
    monkeypatch.setattr(
        check_documentation, "LAYOUT_PENDING", frozenset({"SYNOPSIS.md", "TUTORIAL.md"})
    )
    assert _layout_problems({"SYNOPSIS.md", "TUTORIAL.md"}) == []
    assert _layout_problems({"SYNOPSIS.md", "docs/project/guides/tutorial.md"}) == [
        "layout allowlist entry no longer needed: TUTORIAL.md"
    ]


def test_the_pending_list_only_shrinks() -> None:
    assert PENDING <= PENDING_AT_START, sorted(PENDING - PENDING_AT_START)
