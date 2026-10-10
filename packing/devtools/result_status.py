"""A result's status: how far this project's own workflow has taken it.

`epistemics.md` (Status) owns the vocabulary. A status is one word, derived from the
register and the evidence it cites and never stored, so it cannot drift from the rungs:

- **recorded**: registered here from its source; no read and no replay is on file (`C0`);
- **reviewed**: a qualifying, dated read of the argument is on file and no replay has
  passed (`C1`);
- **confirmed**: a confirming replay has passed, here or by a third party whose replay
  is retained (`C2` and up);
- **incomplete**: the record holds an open defect against the entry (`open_issues`),
  which wins over the other three.

The first three are the confirmation ladder read in three words, so a status never
competes with `C`: it is the reader's summary of it. `incomplete` is the one value the
ladder cannot give.

Two more things sit beside a status and are not part of it. Whether a result is
*superseded*, and by what, is its position on the frontier: derived from the case
records for a bound (`render_recent_results.standing`, `superseding`), and declared in
its entry for a result of another kind that a later result implies, wholly or in part
(`superseded_by`, `render_recent_results.supersessions`). Its `activity` is who has the
next move: this project, with work under way (`in analysis`), or another party, with a
request on file (`waiting on …`). An activity is the one hand-recorded fact here, so it
is dated, names the record that shows it, and expires (`activity_problems`).

Provisional: the vocabulary, the rung at which a result is `confirmed`, and whether the
two activities are marks beside the status or statuses of their own are the owner's to
confirm (plan-2026-10-01-result-status).
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from functools import cache
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from devtools.build_bound_citations import Register

REPO = Path(__file__).resolve().parents[2]

RECORDED = "recorded"
REVIEWED = "reviewed"
CONFIRMED = "confirmed"
INCOMPLETE = "incomplete"
#: The four statuses, in workflow order, the blocked one last.
STATUSES = (RECORDED, REVIEWED, CONFIRMED, INCOMPLETE)

#: The lowest confirmation rung at which a replay has passed (epistemics.md,
#: Confirmation): `C2`, a replay without a machine certificate. Below it a result is
#: recorded (`C0`) or reviewed (`C1`).
CONFIRMED_FROM = 2
REVIEWED_AT = 1

#: A read that found a defect, the evidence schema's `external_review.state`.
DEFECT_FOUND = "defect-found"
#: The review verdicts that leave a defect standing (the register schema's `verdict`).
OPEN_VERDICTS = frozenset({"defect-open", "refuted"})
#: A replay that ran and did not pass (the evidence schema's `replay_status`).
FAILED_REPLAY = "failed"

IN_ANALYSIS = "in-analysis"
WAITING = "waiting"
ACTIVITY_STATES = (IN_ANALYSIS, WAITING)
#: Who a result may wait on: its source's authors, this project's owner, or anyone else.
PARTIES = ("source", "owner", "third-party")
#: How long an activity may stand unrevised, in days before the register's
#: `last_reviewed`. Provisional: long enough for a multi-day replay, short enough that
#: "in analysis" cannot outlive the work by a month.
ACTIVITY_MAX_AGE = 30

#: What an activity's `link` may be: a bead, a GitHub issue or pull request, a branch of
#: this repository, or a repository-relative file.
_BEAD = re.compile(r"[a-z]+-[a-z0-9]{4}")
_GITHUB = re.compile(r"https://github\.com/[\w.-]+/[\w.-]+/(?:issues|pull|tree)/[\w./-]+")


def _rank(rung: object) -> int:
    return int(str(rung)[1])


Record = Mapping[str, Any]
Evidence = Mapping[str, Mapping[str, Any]]


@dataclass(frozen=True, slots=True)
class RecentContributions:
    """Which displayed contributions originate within the shared recent-result window.

    These flags date contributions, not their subsequent verification. An upper flag
    leaves the construction's reported/verified status alone; lower and optimal refer
    to the verified proof lane. Renderers can therefore accent each bound and the
    optimality mark independently.
    """

    upper: bool
    lower: bool
    optimal: bool

    @property
    def any(self) -> bool:
        return self.upper or self.lower or self.optimal


def recent_contributions(n: int, case: Record, register: Register) -> RecentContributions:
    """Date the current construction and proof from their original typed provenance.

    The citation module owns the date cutoff and the proof-origin rule. In particular,
    a new replay of a historical proof retains the original source's date. Upper
    recency likewise follows the reported construction, never a new certificate of it.
    A recent lower proof also contributes optimality only when the frontier explicitly
    declares the case proved; rounded equality is not an optimality certificate.
    """
    from devtools import build_bound_citations as citations  # noqa: PLC0415
    from sqpack.assurance import bounds_agree_at_declared_precision  # noqa: PLC0415

    reported = case["reported_upper_bound"]
    verified = case["verified_upper_bound"]
    certificate = citations.own_evidence(verified["evidence"], register)
    is_grid = not certificate and bounds_agree_at_declared_precision(reported, verified)
    construction = citations.own_evidence(reported["evidence"], register)
    if is_grid or not construction:
        upper = False
    elif any(
        citations.is_novel_first_party(register.evidence[item], "upper-bound")
        for item in construction
    ):
        upper = True
    else:
        source_key = reported.get("source_key")
        if source_key not in register.sources:
            raise ValueError(
                f"n={n}: upper construction has no bibliography source: {source_key}"
            )
        upper = citations.is_recent(register.sources[source_key])

    origin = citations.lower_origin(n, case["verified_lower_bound"], register)
    lower = bool(
        origin
        and origin.recent
        and all(
            register.evidence[item].get("assurance") == "verified"
            and register.evidence[item].get("claim") in {"lower-bound", "exact-value"}
            and register.evidence[item].get("replay_status") != FAILED_REPLAY
            for item in origin.own
        )
    )
    return RecentContributions(
        upper=upper, lower=lower, optimal=lower and case["status"] == "proved"
    )


@cache
def recent_contributions_by_case() -> Mapping[int, RecentContributions]:
    """The atlas corpus's contribution flags, loaded once for a renderer invocation."""
    from devtools import build_bound_citations as citations  # noqa: PLC0415

    register = citations.load_register()
    return MappingProxyType(
        {
            n: recent_contributions(n, citations.load_case(n), register)
            for n in citations.CORPUS.numbers
        }
    )


def open_issues(record: Record, evidence: Evidence) -> list[str]:
    """Why an entry is incomplete, each reason a fact the record holds, or none.

    - A read found a defect and nothing here has replayed past it: a cited entry's
      `external_review.state` is `defect-found` while the result stands below `C2`. A
      defect a replay has since passed over is dispositioned by that replay, which is
      why `T-005`, whose subject is the defect in Bentz's Lemma 10, is not incomplete.
    - The latest review of the result leaves a defect open or refutes it.
    - A cited replay ran and failed.
    """
    reasons: list[str] = []
    cited = [(ref, evidence[ref]) for ref in record["evidence"] if ref in evidence]
    if _rank(record["confirmation"]) < CONFIRMED_FROM:
        for ref, entry in cited:
            review = entry.get("external_review") or {}
            if review.get("state") == DEFECT_FOUND:
                reasons.append(
                    f"the read of {review.get('date')} found a defect in {ref}, and no "
                    "replay here has passed"
                )
    latest = latest_review(list(record.get("reviews") or []))
    if latest is not None and latest.get("verdict") in OPEN_VERDICTS:
        reasons.append(
            f"the review of {latest.get('date')} ends {latest.get('verdict')}: "
            f"{latest.get('path')}"
        )
    reasons.extend(
        f"the replay of {ref} failed"
        for ref, entry in cited
        if entry.get("replay_status") == FAILED_REPLAY
    )
    return reasons


def latest_review(reviews: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    """The latest-dated review, and of reviews dated the same day the one listed last.

    A `reviews` list is in the order its documents were written, and a review and the
    check of its fixes can share a date: T-098's adversarial review and the check that
    dispositions its findings were both written on 2026-10-06. `max` alone keeps the
    first of a tie, which would read the defect the later document resolved as open.
    """
    latest: Mapping[str, Any] | None = None
    for review in reviews:
        if latest is None or str(review.get("date", "")) >= str(latest.get("date", "")):
            latest = review
    return latest


def status(record: Record, evidence: Evidence) -> str:
    """The one status of a result: `incomplete` where the record holds an open defect
    against it, else the confirmation rung read as recorded, reviewed or confirmed."""
    if open_issues(record, evidence):
        return INCOMPLETE
    rank = _rank(record["confirmation"])
    if rank >= CONFIRMED_FROM:
        return CONFIRMED
    return REVIEWED if rank >= REVIEWED_AT else RECORDED


def decided_by(record: Record, evidence: Evidence) -> str:
    """The fact in the record that decides a result's status, in words."""
    issues = open_issues(record, evidence)
    if issues:
        return "; ".join(issues)
    return f"{record['confirmation']}"


def activity_label(activity: Mapping[str, Any] | None) -> str:
    """An activity as a reader is told it: `in analysis`, or `waiting on source`."""
    if not activity:
        return ""
    if activity.get("state") == IN_ANALYSIS:
        return "in analysis"
    return f"waiting on {str(activity.get('party', '')).replace('-', ' ')}"


def status_line(
    record: Record, evidence: Evidence, position: Sequence[str] = (), how: str = ""
) -> str:
    """A result's status as one cell of a Markdown table: the status, then its activity
    and `superseded` or `superseded in part` where it is one, with what supersedes it
    (`render_recent_results.position_marks`), the marks the site draws as chips beside
    it. A confirmed result says how, in `how`, as the mark after the status: reproduced
    with the producer's code, or re-implemented (epistemics.md, Confirmation). The status
    stays the first mark, so the cell reads the same way whatever follows it."""
    held = status(record, evidence)
    qualifier = how if held == CONFIRMED else ""
    marks = [held, qualifier, activity_label(record.get("activity")), *position]
    return ", ".join(mark for mark in marks if mark)


def _link_problem(link: str) -> str | None:
    if _BEAD.fullmatch(link) or _GITHUB.fullmatch(link):
        return None
    pure = PurePosixPath(link)
    if pure.is_absolute() or ".." in pure.parts or not (REPO / pure).exists():
        return "is not a bead, a GitHub issue, pull request or branch, or a repository path"
    return None


def activity_problems(record: Mapping[str, Any], last_reviewed: str) -> list[str]:
    """What is wrong with a result's `activity`, the one hand-recorded workflow fact.

    It names a state, who the result waits on when it waits, what on, since when, and
    the record that shows it. It may not be dated after the register's last review, and
    it expires: one older than `ACTIVITY_MAX_AGE` days at that review is re-dated with
    what happened since, or removed. The check reads the register's own date and never
    the clock, so two runs over one tree agree.
    """
    activity = record.get("activity")
    if activity is None:
        return []
    rid = record["id"]
    problems: list[str] = []
    state = activity.get("state")
    if state not in ACTIVITY_STATES:
        problems.append(f"{rid}: activity.state is not one of {', '.join(ACTIVITY_STATES)}")
    party = activity.get("party")
    if state == WAITING and party not in PARTIES:
        problems.append(f"{rid}: a waiting activity names who, one of {', '.join(PARTIES)}")
    if state == IN_ANALYSIS and party is not None:
        problems.append(f"{rid}: an activity in analysis is this project's and names no party")
    problems.extend(
        f"{rid}: activity.{key} is required"
        for key in ("what", "link")
        if not str(activity.get(key) or "").strip()
    )
    if activity.get("link") and (problem := _link_problem(str(activity["link"]))):
        problems.append(f"{rid}: activity.link {problem}: {activity['link']}")
    try:
        since = date.fromisoformat(str(activity.get("since")))
        reviewed = date.fromisoformat(str(last_reviewed))
    except ValueError:
        problems.append(f"{rid}: activity.since is not a calendar date")
        return problems
    age = (reviewed - since).days
    if age < 0:
        problems.append(
            f"{rid}: activity.since {since.isoformat()} is after the register's "
            f"last_reviewed {reviewed.isoformat()}"
        )
    elif age > ACTIVITY_MAX_AGE:
        problems.append(
            f"{rid}: its activity is {age} days old at the register's last review, over "
            f"the {ACTIVITY_MAX_AGE} it may stand; re-date it with what happened since, "
            "or remove it"
        )
    return problems


def listing() -> list[str]:
    """Every result's status as a Markdown table, in id order: the standing it had, the
    status, the fact that decides it, whether it is superseded and by what, and its
    activity."""
    # `render_recent_results` reads `check_results`, which reads this module.
    from devtools.render_recent_results import (  # noqa: PLC0415
        load_records,
        position_marks,
        standing,
    )

    records = load_records()
    evidence = records.register.evidence
    lines = [
        "| id | standing | status | decided by | position | activity |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for record in records.register.results:
        stands = standing(record, records)
        activity = record.get("activity") or {}
        doing = activity_label(activity)
        if doing:
            doing = f"{doing}: since {activity['since']}, {activity['link']}"
        lines.append(
            f"| {record['id']} | {stands} | {status(record, evidence)} "
            f"| {decided_by(record, evidence)} "
            f"| {', '.join(position_marks(record, stands, records))} "
            f"| {doing} |"
        )
    return lines


def counts() -> dict[str, int]:
    """How many results carry each status, in `STATUSES` order."""
    from devtools.render_recent_results import load_records  # noqa: PLC0415

    register = load_records().register
    held = [status(record, register.evidence) for record in register.results]
    return {name: held.count(name) for name in STATUSES}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Each registered result's status, derived from the register."
    )
    parser.add_argument("--list", action="store_true", help="every result's status, as a table")
    options = parser.parse_args(argv)
    if options.list:
        print("\n".join(listing()))
    print(", ".join(f"{count} {name}" for name, count in counts().items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
