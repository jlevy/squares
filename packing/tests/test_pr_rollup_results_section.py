"""A pull request says what the run established, not only what it committed to.

Agenda 016 registered `T-014`, `T-015` and `T-016`, scored all three at `S3`, and then
published a description in which the only significance a reader could find was one
`V3/C5/S3` that happened to sit inside a `BC-153` row. Two of the three results carried
no score at all and the rubric's wording for `S3` appeared nowhere, so the page could not
tell a reviewer which result to read first or what the score meant. The dispositions
table cannot repair that on its own: it is keyed on commitments, and a result is a
different object in a different register.

These tests hold the join and its placement -- `OR-9` keeps what the branch cost first,
so the results section sits between that block and the dispositions -- and the two
directions that keep it honest: a result scored outside the run's wall is not this run's
news, and a run that registered nothing prints no heading implying it did.
"""

from __future__ import annotations

from datetime import date

import pytest

import devtools.render_pr_rollup as renderer
from devtools import significance

COST = "## What this branch cost\n\nstub\n"


def _result(identifier: str, *, score: int = 3, scored: str = "2026-09-03") -> dict:
    return {
        "id": identifier,
        "claim": (
            "s(17) >= 9/2, by a fractional unavoidable-set certificate. "
            "A second sentence, which the one-line cell drops."
        ),
        "scope": {"n_values": [17]},
        "verification": "V4",
        "confirmation": "C3",
        "significance": {
            "score": score,
            "rationale": (
                "Moves the verified lower bound at n = 17 for the first time since 2005, "
                "on evidence this repository replayed rather than only read."
            ),
            "scored": scored,
            "by": "BC-151 independent review",
        },
        "novelty": "previously-published",
    }


def _agenda(*, updated: str = "2026-09-03", bead: str = "think-only") -> dict:
    return {
        "id": "agenda-999",
        "updated": updated,
        "items": [
            {
                "id": "BC-999",
                "bead": bead,
                "outcomes": [
                    {
                        "scope": "one exact certificate",
                        "classification": "achieved",
                        "result": "The certificate replayed exactly.",
                        "evidence": ["A passing replay."],
                        "disposition": "retire-success",
                        "follow_up": None,
                    }
                ],
            }
        ],
        "closeout": {
            "changes": [
                {
                    "name": "adoption",
                    "result": "Installed the reviewed packet.",
                    "paths": ["packing/cases/example.py"],
                }
            ],
            "validation": [
                {"scope": "focused", "status": "passed", "evidence": "Three tests."}
            ],
            "documentation_review": [
                {"path": "README.md", "decision": "updated", "reason": "New bound."}
            ],
            "replanning": {
                "operator_input": {"status": "unchanged", "note": "No revision."},
                "candidates": [
                    {
                        "priority": 0,
                        "bead": "think-next",
                        "workflow": "research-loop",
                        "rationale": "The remaining rung.",
                    }
                ],
                "selected": {
                    "bead": "think-next",
                    "workflow": "research-loop",
                    "rationale": "Highest-ranked valid continuation.",
                },
            },
        },
    }


def _fixed(
    monkeypatch: pytest.MonkeyPatch,
    *,
    results: list[dict],
    sessions: list[dict] | None = None,
) -> None:
    """Pin the two records the section joins, leaving the live rubric alone."""
    monkeypatch.setattr(significance, "load", lambda: results)
    monkeypatch.setattr(renderer, "session_payloads", lambda: sessions or [])


def test_the_results_section_sits_below_the_cost_block_and_above_the_dispositions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Placement is the whole point, and only one of the three orders is allowed.

    `OR-9` requires the description to lead with what the branch cost, so the results
    cannot go first however much a reader wants them there. They cannot go last either:
    below the dispositions they are the same 400 lines down that made the synopsis
    unreadable. One position satisfies both, and this pins it.
    """
    _fixed(monkeypatch, results=[_result("T-900")])
    monkeypatch.setattr(renderer, "render", lambda _branch, _session=None: COST)
    monkeypatch.setattr(renderer, "agenda_payload", lambda _agenda_id: _agenda())

    rendered = renderer.render_description("claude/example", "agenda-999")

    assert (
        rendered.index("## What this branch cost")
        < rendered.index("## New Results and Their Significance")
        < rendered.index("## Results and Dispositions")
    )


def test_a_result_scored_inside_the_wall_arrives_with_the_rubrics_own_words(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The score, the rubric's wording for it, and the reviewer's assessment, whole.

    A bare `S3` is not a reading: it tells a reviewer nothing about what the project
    means by the number. The anchor is quoted from `epistemics.md` through the shared
    helper rather than restated here, so the pin below is the one place a reworded
    rubric has to be re-read -- and it fails loudly instead of letting a stale copy
    keep describing the policy.
    """
    anchor = significance.anchors()[3]
    assert anchor == "A substantive case result or machine audit"
    _fixed(monkeypatch, results=[_result("T-900")])

    rendered = renderer.render_agenda_results(_agenda())

    assert "## New Results and Their Significance" in rendered
    assert "| `T-900` | 17 | `V4` | `C3` | `S3` | `previously-published` |" in rendered
    assert "s(17) >= 9/2, by a fractional unavoidable-set certificate." in rendered
    assert f"**`T-900` — `S3`: {anchor}.**" in rendered
    assert "Scored 2026-09-03 by BC-151 independent review." in rendered
    # The rationale is the assessment a reviewer wrote, so it is quoted, not summarized.
    assert (
        "> Moves the verified lower bound at n = 17 for the first time since 2005, "
        "on evidence this repository replayed rather than only read." in rendered
    )
    # And the reader is told what the score is not, in the policy's own sentence.
    assert '"The score guides reading order and never changes validation behavior."' in rendered


def test_a_result_scored_outside_the_wall_is_not_this_runs_news(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The register is cumulative and a pull request is not.

    Fifteen results predate this branch. Presenting them under a heading a reviewer
    reads as "what this run established" would make every description look like the
    whole frontier, which is exactly the noise that buries the three rows that are new.
    """
    _fixed(
        monkeypatch,
        results=[_result("T-900"), _result("T-800", scored="2026-08-31")],
    )

    rendered = renderer.render_agenda_results(_agenda())

    assert "`T-900`" in rendered
    assert "T-800" not in rendered


def test_a_run_that_registered_nothing_renders_no_heading(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An empty table under a heading is a claim, and it would be the wrong one.

    Most runs register no result; agenda-015 is one of them. A heading with nothing
    under it reads as "results were assessed and here they are", which overstates a
    record that simply has no row to show.
    """
    _fixed(monkeypatch, results=[_result("T-800", scored="2026-08-31")])
    monkeypatch.setattr(renderer, "render", lambda _branch, _session=None: COST)
    monkeypatch.setattr(renderer, "agenda_payload", lambda _agenda_id: _agenda())

    assert renderer.render_agenda_results(_agenda()) == ""
    rendered = renderer.render_description("claude/example", "agenda-999")
    assert "New Results and Their Significance" not in rendered
    assert rendered.index("## What this branch cost") < rendered.index(
        "## Results and Dispositions"
    )


def test_the_window_is_the_wall_of_the_sessions_that_ran_this_agendas_commitments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No agenda records a wall, so the rule that reconstructs one has to be pinned.

    An agenda's only date is `updated`, and a ten-hour run can cross midnight UTC --
    session-061 did. The window therefore extends over the sessions that executed this
    agenda's commitments, joined on `bead`. A bead can be carried into a later agenda,
    so a session holding the same bead whose wall had already closed belongs to the
    earlier run and must not drag the window back over its results.
    """
    overnight = {
        "id": "session-900",
        "primary_bead": "think-only",
        "started_at": "2026-09-02T22:28:00Z",
        "deadline_at": "2026-09-03T02:58:00Z",
    }
    earlier_run = {
        "id": "session-800",
        "primary_bead": "think-only",
        "started_at": "2026-08-31T05:00:00Z",
        "deadline_at": "2026-08-31T15:00:00Z",
    }
    unrelated = {
        "id": "session-700",
        "primary_bead": "think-elsewhere",
        "started_at": "2026-09-01T05:00:00Z",
        "deadline_at": "2026-09-05T15:00:00Z",
    }
    agenda = _agenda(updated="2026-09-02")
    _fixed(
        monkeypatch,
        results=[
            _result("T-900", scored="2026-09-03"),
            _result("T-800", scored="2026-08-31"),
        ],
        sessions=[overnight, earlier_run, unrelated],
    )

    assert renderer.agenda_window(agenda) == (
        date(2026, 9, 2),
        date(2026, 9, 3),
    )

    rendered = renderer.render_agenda_results(agenda)

    assert "between 2026-09-02 and 2026-09-03" in rendered
    assert "`T-900`" in rendered
    assert "T-800" not in rendered


def test_agenda_016_presents_every_result_it_registered() -> None:
    """The live regression: three results were scored that day and one was shown.

    This renders from the records themselves, so it also checks the join those records
    actually support -- an agenda's beads to the sessions that ran them to the wall
    they declared -- rather than the synthetic shape the tests above construct.
    """
    agenda = renderer.agenda_payload("agenda-016")

    rendered = renderer.render_agenda_results(agenda)

    for identifier in ("T-014", "T-015", "T-016"):
        assert f"**`{identifier}` — `S3`: " in rendered
    assert rendered.count("A substantive case result or machine audit") == 3
    # T-014 leads: same score, higher confirmation, which is `RESULTS.md`'s own order.
    assert rendered.index("`T-014`") < rendered.index("`T-015`")
    # Nothing scored before the run's wall is presented as its news. Cited is not
    # presented: T-015's rationale measures itself against T-001, which is why this
    # asks about rows and blocks rather than about the bare identifier.
    for identifier in ("T-001", "T-012", "T-013"):
        assert f"| `{identifier}` |" not in rendered
        assert f"**`{identifier}` —" not in rendered
