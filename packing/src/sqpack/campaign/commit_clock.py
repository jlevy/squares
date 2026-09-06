#!/usr/bin/env python3
"""The instant a record gate judges its time-based refusals against.

`D-468`. Several of `packing-ledger check`'s refusals are *anti-monotone* in their
reference instant -- an expired lease, a passed session deadline, a passed workflow-phase
deadline and a passed delegation deadline all become true with time alone. Read against
the wall clock, that makes the gate's verdict a function of when CI happened to run
rather than of the commit, and a green commit does not stay green: on 2026-09-05 PR 83
was green at 20:36Z and red at 21:23Z with one float tolerance between the trees, because
a phase deadline of 20:43Z passed in between.

So the anchor is **HEAD's committer date**, not `now()`. Every commit then has one
verdict, for the life of the branch, however long it sits unmerged, and re-running CI on
it cannot change the answer. What the refusals mean under that anchor is not weaker, it
is sharper: *at the moment you made this commit, this record claimed to be live past its
own deadline*, which is a property of the commit and a thing the author can see and fix
before pushing.

The committer date rather than the author date, deliberately: rebasing or amending
produces a different commit object, which is entitled to a fresh verdict, and the
committer date is the one that moves with it.

**Outside a checkout there is no such instant, and that is reported, not failed.**
`conventions.md` §6 draws this line for recorded engine commits -- a checkout that cannot
resolve a commit is not evidence against it -- and `devtools/check_session_gate.py` draws
it the same way for gate declarations. The negative-control sandbox is a source snapshot
with no `.git`, and so is a source tarball; there, the clock-dependent refusals are
uncheckable, reported by name, and nothing fails on them. Everything else the gate checks
is unaffected, because everything else is a property of the tree alone.

**A commit dated in the future is not a usable anchor either.** The committer date is
whatever the committing environment said it was (`GIT_COMMITTER_DATE` sets it outright),
so anchoring on it without a bound would let one mis-set clock retire all four refusals
for good. Wall time is the only thing that can catch that, and it is safe to use for it
because the comparison runs the *monotone* way: `commit > wall` stops being true as time
passes, so a tree that is checkable today cannot become uncheckable tomorrow, and the
answer is uncheckable rather than a refusal in any case. This is the same direction
`devtools/check_session_clocks.py` documents for its own wall-clock bound.
"""

from __future__ import annotations

import datetime as dt
import subprocess
from dataclasses import dataclass
from pathlib import Path

#: How far ahead of wall time a committer date may sit and still be trusted. Hosts that
#: agree through NTP are within a second of each other; five minutes is the allowance
#: Kerberos and TOTP make for cross-host skew, and it is generous enough that ordinary
#: skew never costs coverage while a mis-set or forged clock is still caught.
SKEW_TOLERANCE = dt.timedelta(minutes=5)

#: A tracked file that exists only in this project's own checkout. `git` searches parent
#: directories for a repository, so a snapshot unpacked below some unrelated repository
#: would otherwise answer with *that* repository's HEAD -- a wrong anchor, which is worse
#: than no anchor. Asking whether the checkout tracks this file is what tells the two
#: apart.
PROJECT_TRACKED_MARKER = "pyproject.toml"


@dataclass(frozen=True, slots=True)
class Clock:
    """The instant time-based refusals are judged against, and where it came from.

    `instant` is `None` when this tree cannot supply one. That is a fact about the
    checkout, never a verdict about a record, so a caller holding an uncheckable clock
    reports what it could not judge and fails nothing on it.
    """

    instant: dt.datetime | None
    source: str

    @property
    def certified(self) -> bool:
        """Whether this clock can decide a deadline at all."""
        return self.instant is not None


def _git(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ("git", "-C", str(root), *arguments),
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:  # git is not installed at all
        return subprocess.CompletedProcess(args=("git",), returncode=127, stdout="", stderr="")


def head_commit_instant(root: Path) -> tuple[dt.datetime | None, str]:
    """HEAD's committer date as an aware UTC instant, or `None` and why not."""
    if _git(root, "rev-parse", "--git-dir").returncode != 0:
        return None, f"no git checkout at {root}"
    if _git(root, "ls-files", "--error-unmatch", PROJECT_TRACKED_MARKER).returncode != 0:
        return None, f"the checkout above {root} does not track this project"
    head = _git(root, "log", "-1", "--format=%cI")
    stamped = head.stdout.strip()
    if head.returncode != 0 or not stamped:
        return None, f"no commit at HEAD in {root}"
    try:
        parsed = dt.datetime.fromisoformat(stamped)
    except ValueError:
        return None, f"HEAD committer date is not an ISO instant: {stamped!r}"
    if parsed.tzinfo is None:
        return None, f"HEAD committer date carries no offset: {stamped!r}"
    return parsed.astimezone(dt.UTC), f"HEAD committed {stamped}"


def commit_clock(*, commit: dt.datetime | None, wall: dt.datetime, reason: str = "") -> Clock:
    """Judge whether a commit instant can anchor a gate, given the wall clock now.

    Pure, so the whole policy is testable without a repository: `head_commit_instant`
    reads Git, this decides what to do with the answer, and `main` composes them.
    """
    if commit is None:
        return Clock(None, reason or "no commit clock available")
    reference = wall.astimezone(dt.UTC)
    if commit > reference + SKEW_TOLERANCE:
        return Clock(
            None,
            f"{reason or 'HEAD'} is dated ahead of this host's clock "
            f"({commit:%Y-%m-%dT%H:%M:%SZ} against {reference:%Y-%m-%dT%H:%M:%SZ}), "
            "so it cannot be trusted to date anything",
        )
    return Clock(commit, reason or f"HEAD committed {commit:%Y-%m-%dT%H:%M:%SZ}")


def project_clock(root: Path, *, wall: dt.datetime | None = None) -> Clock:
    """The clock a gate running over `root` should use. The one call `main` needs."""
    commit, reason = head_commit_instant(root)
    return commit_clock(commit=commit, wall=wall or dt.datetime.now(dt.UTC), reason=reason)
