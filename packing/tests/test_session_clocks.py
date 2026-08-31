"""A session may not declare a start time it could not have read.

`D-358` is an unattended run that misread its own clock by a factor of four and whose
`regression` field said "None automatic". These assertions are that regression, written
after the same session family made the same mistake a second time: `session-045` declared
two phases starting at `10:16Z` and `11:10Z` while the clock read `09:52Z`.

The point of the tests below is the *line* rather than the check. A future start cannot be
true and is refused; a phase starting before the one above it in the file can be true --
`session-044`'s phase 7 is a delegated lane run in a worktree -- and is reported instead.
Getting that line wrong in either direction is how a guard stops being one.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from devtools.check_session_clocks import phases, remarks, violations

NOW = datetime(2026, 8, 30, 12, 0, tzinfo=UTC)


def _record(
    *starts: str | None, session: str = "2026-08-30T09:00:00Z", **kwargs: object
) -> dict:
    return {
        "started_at": session,
        "workflow_phases": [
            {
                "workflow": f"phase-{index}",
                "status": "completed",
                "started_at": start,
                "budget_minutes": 30,
                **kwargs,
            }
            for index, start in enumerate(starts)
        ],
    }


def test_a_start_in_the_future_is_refused() -> None:
    """The exact shape of both occurrences, and the only thing that cannot be true."""
    found = violations("s.md", _record("2026-08-30T09:30:00Z", "2026-08-30T13:00:00Z"), NOW)

    assert len(found) == 1
    assert "ahead of now" in found[0]
    assert "D-358" in found[0]


def test_a_session_that_has_not_started_is_refused() -> None:
    """A phase can be mistimed; a session that begins tomorrow is a different error."""
    record = _record("2026-08-30T09:30:00Z", session="2026-08-31T09:00:00Z")

    assert any("session starts at" in problem for problem in violations("s.md", record, NOW))


def test_a_deadline_that_is_not_after_its_start_is_refused() -> None:
    """No run fits in it, so the budget it states is not a budget."""
    record = _record("2026-08-30T09:30:00Z")
    record["workflow_phases"][0]["deadline_at"] = "2026-08-30T09:30:00Z"

    assert any("no run fits it" in problem for problem in violations("s.md", record, NOW))


def test_a_phase_starting_before_its_session_is_refused() -> None:
    record = _record("2026-08-30T08:00:00Z")

    assert any("before the session" in problem for problem in violations("s.md", record, NOW))


def test_backwards_phases_are_reported_and_not_refused() -> None:
    """The distinction this file exists to hold.

    `session-044`'s phase 7 starts thirteen minutes before phase 6 because it ran as a
    delegated lane against a worktree and was integrated afterwards. Position in the file
    is authoring order, not wall-clock order. Refusing it would fail a true record, which
    is the failure mode a guard is least able to survive.
    """
    record = _record("2026-08-30T10:00:00Z", "2026-08-30T09:30:00Z")

    assert violations("s.md", record, NOW) == []
    assert len(remarks("s.md", record)) == 1
    assert "delegated lane" in remarks("s.md", record)[0]


def test_a_phase_without_a_clock_is_neither_refused_nor_reported() -> None:
    """`started_at` is nullable and most sessions before 2026-08-29 leave it so."""
    record = _record(None, "2026-08-30T09:30:00Z")

    assert violations("s.md", record, NOW) == []
    assert remarks("s.md", record) == []
    assert [phase.started_at is None for phase in phases(record)] == [True, False]


@pytest.mark.parametrize("ahead", [timedelta(seconds=1), timedelta(days=365)])
def test_the_refusal_has_no_grace_period(ahead: timedelta) -> None:
    """A second into the future is the same kind of claim as a year into it.

    A tolerance here would be a licence to round, and rounding is how a clock drifts by a
    factor of four one estimate at a time.
    """
    start = (NOW + ahead).isoformat().replace("+00:00", "Z")

    assert violations("s.md", _record(start), NOW)


def test_the_real_corpus_is_clean() -> None:
    """The check is worth nothing if it is only ever exercised on fixtures."""
    from devtools.check_session_clocks import SESSIONS, session_record  # noqa: PLC0415

    now = datetime.now(UTC)
    paths = sorted(SESSIONS.glob("session-[0-9][0-9][0-9]-*.md"))

    assert len(paths) >= 45
    for path in paths:
        assert violations(path.name, session_record(path), now) == [], path.name
