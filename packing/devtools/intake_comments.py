"""Draft an intake pass's report-order verdict comments from its ledger; it never posts.

`devtools.intake_ledger` writes the verdicts of the owner's report-order rule to an intake
directory's ``ledger.json``. This module turns them into one comment per result issue,
for an agent or the owner to post by hand when ``campaign/result-import.md`` (stage 7,
Report-Order Verdict Comments) allows it. It reads only ``ledger.json`` and a small
comments file, ``comments.yaml``, which holds everything one pass says that another
would not: which issues get a comment and who wrote them, which reports each covers, the
issues skipped and why, the records pull request, how a holder or handle the ledger
prints is named, and each comment's own sentences.

Every comment opens with ``@author,``, a thank-you and the rule, gives a table of the
counts the issue claims (the side rounded up at 12 places, the verdict, and what holds
the count now), states what the YAML adds in its own paragraphs, and ends with a pointer
to the records pull request and the Claude Code footer. A comment over many counts can
lead with a summary (``layout: by-count`` or ``by-finder``) and fold the table into a
``<details>`` block. The drafts are refused, and nothing is written, when one names a
``T-NNN`` (an id is quoted to no author until it is on ``main``) or holds any ``tree/``
or ``blob/`` link, into ``main`` as well as into a branch, or when a result issue of the
ledger has neither a comment nor a stated skip.

From ``packing/``, with the project interpreter::

    python -m devtools.intake_comments COMMENTS.yaml --out DIR
    python -m devtools.intake_comments COMMENTS.yaml --check DIR

``--out`` writes ``<issue>.md`` for each comment and an ``INDEX.md`` to a directory,
normally a scratch one: the drafts are not part of the record. ``--check`` compares a
directory of drafts with what would be written and exits 1 on a difference. The ledger
is the one the YAML's ``ledger`` names, as a repository-relative path, or else the
``ledger.json`` beside the YAML.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools.check_requests import FOOTER
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
LEDGER_FORMAT = "intake-ledger-verdicts-v1"
INDEX = "INDEX.md"

#: The rule, as every comment states it after the thank-you.
RULE = (
    "At each count, a report is recorded when its side is decidably below every side "
    "reported before it (and below the record on main); a tie stays with the earlier "
    "report. Sides are rounded up at 12 places."
)

#: The last paragraph before the footer; ``{records_pr}`` is the YAML's records pull request.
FOLLOW = (
    "The registrations are in the records pull request {records_pr}, and a follow-up "
    "with the result ids and rungs will come once it is on main."
)

#: The default opening; a comment's ``opening`` replaces it whole.
OPENING = (
    "@{author}, thank you; this is the report-order evaluation of every open report at "
    "the counts {ref} claims."
)

#: Wording a comments file may override, for the whole pass or for one comment. A claim
#: that refines its own finder's packing reads ``self_refinement``, with ``{finder}`` the
#: finder's name and ``{via}`` the report that gives the refined packing, when that is
#: not a register entry.
WORDING = {"self_refinement": "a refinement of the finder's own packing{via}"}

LAYOUTS = ("table", "by-count", "by-finder")
BY_FINDER_HEADINGS = ("recorded", "equal", "above", "undecided")
COMMENTED_KINDS = frozenset({"issue", "comment", "pull-request"})

#: What a draft may not contain: an id that is not yet on main, or any tree/ or blob/
#: link, main's included.
REFUSED = (
    (re.compile(r"\bT-\d+"), "a T-NNN id"),
    (re.compile(r"tree/|blob/"), "a tree/ or blob/ link"),
)
TRAILING_HANDLE = re.compile(r" \([^)]*\)$")
HANDLE_IN_PARENTHESES = re.compile(r" \([A-Za-z0-9_-]+\)")
#: The ledger's difference (`intake_ledger._difference`): a direction, then a distance
#: that may carry the qualifier ``at least`` or ``about``, kept before the number.
DIFFERENCE = re.compile(r"(below|above) by ((?:at least |about )?)(\S+)")


class CommentsError(ValueError):
    """A comments file or a ledger the drafts cannot be written from."""


@dataclass(frozen=True)
class Comment:
    """One comment, as the comments file declares it."""

    name: str
    author: str
    reports: frozenset[str]
    ref: str
    opening: str
    index: str
    layout: str
    notes: tuple[str, ...]
    wording: Mapping[str, str]
    headings: Mapping[str, str]
    undecided_note: str


@dataclass
class Intake:
    """The comments file and the ledger it reads, with the lookups every comment shares."""

    ledger: Mapping[str, Any]
    records_pr: str
    names: Mapping[str, str]
    handles: Mapping[str, str]
    drop_handles: Sequence[str]
    labels: Mapping[str, str]
    comments: list[Comment]
    skipped: Mapping[str, str]
    counts: dict[int, Mapping[str, Any]] = field(init=False)
    holders: dict[str, str] = field(init=False)

    def __post_init__(self) -> None:
        self.counts = {int(count["n"]): count for count in self.ledger["counts"]}
        self.holders = {
            report["report"]: TRAILING_HANDLE.sub("", report["holders"])
            for report in self.ledger["reports"]
        }

    # Names -------------------------------------------------------------------------

    def _named(self, text: str) -> str:
        """``text`` with each declared handle that stands as a name replaced by the name.

        A handle inside a path, a URL, a repository name or a mention (``ry-xu/``,
        ``/ry-xu``, ``@ry-xu``) is an identifier and stays as it is.
        """
        for handle, name in self.handles.items():
            text = re.sub(rf"(?<![\w/.@`-]){re.escape(handle)}(?![\w/.@`-])", name, text)
        return text

    def clean_holders(self, holders: str) -> str | None:
        """How a holder list reads in a comment, or None where the ledger names only ids."""
        text = self.names.get(holders, holders)
        text = self._named(HANDLE_IN_PARENTHESES.sub("", text))
        if re.fullmatch(r"T-\d+(, T-\d+)*", text):
            return None
        return text

    def detag(self, text: str) -> str:
        """A ledger note with the ids and lane names a comment may not carry taken out."""
        text = re.sub(r"\(the author's own T-\d+\)", "(the author's own, on main)", text)
        text = re.sub(r"\(T-\d+\)", "(on main)", text)
        text = re.sub(r"the record T-\d+", "the record on main", text)
        text = re.sub(r"T-\d+'s", "that entry's", text)
        text = re.sub(r" \(the [a-z0-9]+ lane's README\)", "", text)
        text = text.replace("the reported lane's", "the record's")
        text = self._named(text)
        for handle in self.drop_handles:
            text = text.replace(f" ({handle})", "")
        return text

    # Labels ------------------------------------------------------------------------

    def describe(self, label: str, n: int) -> str:
        """What a ledger label is, in a sentence: a record, a report, a publication."""
        if label in self.labels:
            return self.labels[label]
        if label.startswith(("record ", "register ")):
            return self._lane(label, n)
        if label.startswith("beyond-horizon row"):
            return "the row on main"
        if label == "the grid":
            start = {item["label"]: item for item in self.counts[n]["start"]}
            return f"the grid bound {start[label]['side']}"
        return self._report(label, n)

    def _lane(self, label: str, n: int) -> str:
        """A start the ledger read from the record: a case lane or a pending register entry."""
        count = self.counts[n]
        start = {item["label"]: item for item in count["start"]}
        holders = self.clean_holders(start[label]["holders"]) if label in start else None
        if label.startswith("register "):
            entry = "a register entry pending adoption"
        else:
            entry = "the record on main"
            if holders is None:
                # A lane named by ids alone: the other lane's holders say whose it is.
                others = [self.clean_holders(item["holders"]) for item in count["start"]]
                holders = next((other for other in others if other), None)
        return f"{entry} ({holders})" if holders else entry

    def _report(self, label: str, n: int) -> str:
        """A report: an issue or pull request, an update comment, or a publication."""
        if label not in self.holders:
            raise CommentsError(f"n = {n}: the ledger has no report {label!r}")
        if match := re.fullmatch(r"(#\d+) comment \d+", label):
            return f"{self.holders[label]}'s update comment on {match.group(1)}"
        if "@" in label:
            return f"{self.holders[label]}'s publication `{label}`"
        return f"{label} ({self.holders[label]})"

    def describe_list(self, labels: Iterable[str], n: int) -> str:
        return " and ".join(dict.fromkeys(self.describe(label, n) for label in labels))

    # Verdicts ----------------------------------------------------------------------

    def verdict(self, step: Mapping[str, Any], n: int, comment: Comment) -> str:
        """One table cell: the verdict, what the claim is, and its margin."""
        against = self.describe_list(step["decided_against"], n)
        kind = step["verdict"]
        if kind == "recorded":
            return f"{self._recorded(step, comment)}; {_margin(step, n)} below {against}"
        if kind == "not recorded":
            if step["reason"] == "equal":
                first = (
                    ""
                    if step["decided_against"][0].startswith("record")
                    else ", reported first"
                )
                text = f"not recorded: equal to {against}{first}"
            else:
                text = f"not recorded: {_margin(step, n)} above {against}"
            if step.get("restates"):
                text += f"; {self.detag(step['restates'])}"
            return text
        if kind == "undecided":
            text = f"undecided against {against} at print precision"
            if step.get("decide_by"):
                text += f"; decided by {self.detag(step['decide_by'])}"
            return text
        raise CommentsError(f"n = {n}, {step['report']}: no wording for the verdict {kind!r}")

    def _recorded(self, step: Mapping[str, Any], comment: Comment) -> str:
        packing = step.get("packing")
        if packing is None:
            return "recorded; the source does not say new packing or refinement"
        if packing["kind"] == "refinement":
            whose = TRAILING_HANDLE.sub("", packing["packing_of"])
            via = f" as {packing['entry']} gives it" if packing["entry"].startswith("#") else ""
            finder = self.holders.get(step["report"], "")
            if finder and whose.startswith(finder):
                wording = comment.wording["self_refinement"]
                return "recorded: " + wording.format(finder=finder, via=via)
            return (
                f"recorded: a refinement of {whose}'s packing{via}; "
                f"credited to this report's finder, after {whose}"
            )
        text = "recorded: a new packing"
        if packing.get("continues"):
            text += f", continuing {self.detag(packing['continues'])}"
        return text

    def best_now(self, n: int, mine: frozenset[str]) -> str:
        best = list(self.counts[n]["best_now"])
        if len(best) > 1 and all(item["label"].startswith("record ") for item in best):
            best = best[:1]
        parts = [
            ("this report" if item["label"] in mine else self.describe(item["label"], n))
            + f" {item['side']}"
            for item in best
        ]
        return "undecided: " + " or ".join(parts) if len(parts) > 1 else parts[0]

    # Comments ----------------------------------------------------------------------

    def steps(self, comment: Comment) -> list[tuple[int, Mapping[str, Any]]]:
        return [
            (n, step)
            for n in sorted(self.counts)
            for step in self.counts[n]["steps"]
            if step["report"] in comment.reports
        ]

    def table(self, comment: Comment, steps: Sequence[tuple[int, Mapping[str, Any]]]) -> str:
        lines = ["| n | Side | Verdict | Best now |", "| ---: | --- | --- | --- |"]
        lines += [
            f"| {n} | {step['side']} | {self.verdict(step, n, comment)} "
            f"| {self.best_now(n, comment.reports)} |"
            for n, step in steps
        ]
        return "\n".join(lines)

    def by_count(
        self, comment: Comment, steps: Sequence[tuple[int, Mapping[str, Any]]]
    ) -> list[str]:
        """Each recorded and each tied count on its own line; the rest grouped by holder."""
        lines = [
            f"- **{n}:** {step['side']}, {self.verdict(step, n, comment)}."
            for n, step in steps
            if step["verdict"] == "recorded"
        ]
        lines += [
            f"- **{n}:** {step['side']}, {self.verdict(step, n, comment)}."
            for n, step in steps
            if step["reason"] == "equal"
        ]
        above: dict[str, list[int]] = {}
        for n, step in steps:
            if step["verdict"] == "not recorded" and step["reason"] != "equal":
                above.setdefault(self.describe_list(step["decided_against"], n), []).append(n)
        lines += [
            f"- **Not recorded, above {holder}:** {ranges(ns)}."
            for holder, ns in sorted(above.items(), key=lambda item: item[1][0])
        ]
        undecided = [n for n, step in steps if step["verdict"] == "undecided"]
        if undecided:
            lines.append(f"- **Undecided at print precision:** {ranges(undecided)}.")
        return lines

    def by_finder(
        self, comment: Comment, steps: Sequence[tuple[int, Mapping[str, Any]]]
    ) -> list[str]:
        """Recorded refinements grouped by whose packing each refines; then ties, the
        claims above the record or a register entry pending adoption, and the undecided
        ones, each as one line."""
        groups: dict[str, list[int]] = {}
        equal: list[int] = []
        above: list[str] = []
        undecided: list[int] = []
        for n, step in steps:
            if step["verdict"] == "recorded":
                packing = step.get("packing") or {}
                if packing.get("kind") != "refinement":
                    raise CommentsError(
                        f"{comment.name}: n = {n} is recorded but not as a refinement; "
                        "layout by-finder groups refinements only, so use by-count"
                    )
                groups.setdefault(TRAILING_HANDLE.sub("", packing["packing_of"]), []).append(n)
            elif step["verdict"] == "undecided":
                undecided.append(n)
            else:
                if not all(
                    label.startswith(("record ", "register "))
                    for label in step["decided_against"]
                ):
                    raise CommentsError(
                        f"{comment.name}: n = {n} is held by another report, not the record; "
                        "layout by-finder states ties and claims above the record or a "
                        "pending register entry only"
                    )
                if step["reason"] == "equal":
                    equal.append(n)
                else:
                    held = self.describe(step["decided_against"][0], n)
                    margin = step["difference"].removeprefix("above by ")
                    above.append(f"{n}, {margin} above {held}")
        heading = comment.headings
        lines: list[str] = []
        if groups:
            lines.append(f"- **{heading['recorded']}:**")
            lines += [
                f"  - {whose}: {ranges(ns)}"
                for whose, ns in sorted(groups.items(), key=lambda item: item[1][0])
            ]
        if equal:
            lines.append(f"- **{heading['equal']}:** {ranges(equal)}.")
        if above:
            lines.append(f"- **{heading['above']}:** {'; '.join(above)}.")
        if undecided:
            note = f"; {comment.undecided_note}" if comment.undecided_note else ""
            lines.append(f"- **{heading['undecided']}:** {ranges(undecided)}{note}.")
        return lines

    def render(self, comment: Comment) -> str:
        steps = self.steps(comment)
        if not steps:
            raise CommentsError(
                f"{comment.name}: the ledger has no claim by {sorted(comment.reports)}"
            )
        lines = [comment.opening, "", RULE, ""]
        table = self.table(comment, steps)
        if comment.layout == "table":
            lines += [table, ""]
        else:
            summary = self.by_count if comment.layout == "by-count" else self.by_finder
            lines += [*summary(comment, steps), ""]
        for note in comment.notes:
            lines += [note, ""]
        if comment.layout != "table":
            lines += [
                "<details><summary>Every count</summary>",
                "",
                table,
                "",
                "</details>",
                "",
            ]
        lines.append(FOLLOW.format(records_pr=self.records_pr))
        return "\n".join(lines).rstrip() + "\n\n" + FOOTER + "\n"

    def summarize(self, comment: Comment) -> str:
        steps = self.steps(comment)
        parts = []
        for verdict in ("recorded", "not recorded", "undecided"):
            ns = [n for n, step in steps if step["verdict"] == verdict]
            if ns:
                parts.append(f"{verdict} at {ranges(ns)}")
        return "; ".join(parts)

    def uncovered(self) -> list[str]:
        """The ledger's result issues, comments and pull requests no comment or skip names."""
        covered = set().union(*(comment.reports for comment in self.comments)) | set(
            self.skipped
        )
        return [
            report["report"]
            for report in self.ledger["reports"]
            if report["kind"] in COMMENTED_KINDS and report["report"] not in covered
        ]


def _margin(step: Mapping[str, Any], n: int) -> str:
    match = DIFFERENCE.match(step["difference"])
    if match is None:
        raise CommentsError(f"n = {n}, {step['report']}: no margin in {step['difference']!r}")
    return f"{match.group(2)}{match.group(3)}"


def ranges(ns: Iterable[int]) -> str:
    """``[1, 2, 3, 5]`` as ``1-3, 5``."""
    ordered = sorted(ns)
    out: list[str] = []
    i = 0
    while i < len(ordered):
        j = i
        while j + 1 < len(ordered) and ordered[j + 1] == ordered[j] + 1:
            j += 1
        out.append(str(ordered[i]) if i == j else f"{ordered[i]}-{ordered[j]}")
        i = j + 1
    return ", ".join(out)


def _strings(value: Any, where: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise CommentsError(f"{where} must be a list of strings")
    return list(value)


def _mapping(value: Any, where: str) -> dict[str, str]:
    if not isinstance(value, dict) or not all(
        isinstance(key, str) and isinstance(item, str) for key, item in value.items()
    ):
        raise CommentsError(f"{where} must map strings to strings")
    return dict(value)


def _author(holders: Mapping[str, str], reports: Iterable[str], raw: Mapping[str, Any]) -> str:
    """The comment's ``author``, or the handle the ledger gives its first report's holder."""
    if raw.get("author"):
        return str(raw["author"])
    for report in reports:
        match = re.search(r"\(([^)]*)\)$", holders.get(report, ""))
        if match:
            return match.group(1)
    raise CommentsError(
        f"comment {raw.get('issue')}: no author, and the ledger names no handle"
    )


def _comment(raw: Any, wording: Mapping[str, str], holders: Mapping[str, str]) -> Comment:
    if not isinstance(raw, dict) or "issue" not in raw:
        raise CommentsError("each comment needs an `issue`")
    name = str(raw["issue"])
    where = f"comment {name}"
    reports = _strings(raw.get("reports", [f"#{name}"]), f"{where}: reports")
    ref = str(raw.get("ref", reports[0]))
    layout = str(raw.get("layout", "table"))
    if layout not in LAYOUTS:
        raise CommentsError(f"{where}: layout {layout!r} is not one of {', '.join(LAYOUTS)}")
    headings = _mapping(raw.get("headings", {}), f"{where}: headings")
    if layout == "by-finder" and (missing := set(BY_FINDER_HEADINGS) - set(headings)):
        raise CommentsError(f"{where}: layout by-finder needs headings {sorted(missing)}")
    author = _author(holders, reports, raw)
    return Comment(
        name=name,
        author=author,
        reports=frozenset(reports),
        ref=ref,
        opening=str(raw.get("opening") or OPENING.format(author=author, ref=ref)),
        index=str(raw.get("index", ref)),
        layout=layout,
        notes=tuple(_strings(raw.get("notes", []), f"{where}: notes")),
        wording={**wording, **_mapping(raw.get("wording", {}), f"{where}: wording")},
        headings=headings,
        undecided_note=str(raw.get("undecided_note", "")),
    )


def load(path: Path) -> Intake:
    """Read a comments file and the ledger it names."""
    raw = safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise CommentsError(f"{path}: not a mapping")
    ledger_path = REPO / raw["ledger"] if raw.get("ledger") else path.parent / "ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    if ledger.get("format") != LEDGER_FORMAT:
        raise CommentsError(f"{ledger_path}: not an {LEDGER_FORMAT} ledger")
    if not raw.get("records_pr"):
        raise CommentsError(f"{path}: `records_pr` names the records pull request")
    holders = {report["report"]: report["holders"] for report in ledger["reports"]}
    wording = {**WORDING, **_mapping(raw.get("wording", {}), "wording")}
    skipped: dict[str, str] = {}
    for item in raw.get("skip", []):
        if not isinstance(item, dict) or not item.get("report") or not item.get("reason"):
            raise CommentsError(f"{path}: each skip names a `report` and a `reason`")
        skipped[str(item["report"])] = str(item["reason"])
    return Intake(
        ledger=ledger,
        records_pr=str(raw["records_pr"]),
        names=_mapping(raw.get("names", {}), "names"),
        handles=_mapping(raw.get("handles", {}), "handles"),
        drop_handles=_strings(raw.get("drop_handles", []), "drop_handles"),
        labels=_mapping(raw.get("labels", {}), "labels"),
        comments=[_comment(item, wording, holders) for item in raw.get("comments", [])],
        skipped=skipped,
    )


def drafts(intake: Intake) -> dict[str, str]:
    """Every draft and the index, by file name; refused when a rule above is broken."""
    if uncovered := intake.uncovered():
        raise CommentsError(
            "these result reports have no comment and no stated skip: " + ", ".join(uncovered)
        )
    out = {f"{comment.name}.md": intake.render(comment) for comment in intake.comments}
    refusals = [
        f"{name}: {what}"
        for name, text in out.items()
        for pattern, what in REFUSED
        if pattern.search(text)
    ]
    if refusals:
        raise CommentsError("refused: " + "; ".join(refusals))
    index = [
        "# Report-order evaluation comment drafts",
        "",
        "| File | Target | Verdicts |",
        "| --- | --- | --- |",
    ]
    index += [
        f"| {comment.name}.md | {comment.index} | {intake.summarize(comment)} |"
        for comment in sorted(intake.comments, key=lambda item: int(item.name))
    ]
    out[INDEX] = "\n".join(index) + "\n"
    return out


def check(expected: Mapping[str, str], directory: Path) -> list[str]:
    """How a directory of drafts differs from ``expected``; empty when it does not."""
    problems: list[str] = []
    for name, text in expected.items():
        path = directory / name
        if not path.exists():
            problems.append(f"{name}: missing")
            continue
        found = path.read_text(encoding="utf-8")
        if found != text:
            diff = difflib.unified_diff(
                found.splitlines(),
                text.splitlines(),
                f"{name} (found)",
                f"{name} (drafted)",
                lineterm="",
            )
            problems.append("\n".join(diff))
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m devtools.intake_comments",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _ = parser.add_argument("comments", type=Path, help="the pass's comments.yaml")
    mode = parser.add_mutually_exclusive_group(required=True)
    _ = mode.add_argument("--out", type=Path, help="write the drafts to this directory")
    _ = mode.add_argument("--check", type=Path, help="compare this directory's drafts")
    arguments = parser.parse_args(argv)
    try:
        expected = drafts(load(arguments.comments))
    except (CommentsError, KeyError, OSError, json.JSONDecodeError) as error:
        print(f"intake_comments: {error}", file=sys.stderr)
        return 2
    if arguments.check is not None:
        problems = check(expected, arguments.check)
        others = sorted(
            path.name for path in arguments.check.glob("*.md") if path.name not in expected
        )
        for problem in problems:
            print(problem)
        if others:
            print(f"not drafted by this tool, and not compared: {', '.join(others)}")
        verdict = "differ" if problems else "match"
        print(f"{len(expected)} drafts {verdict} in {arguments.check}")
        return 1 if problems else 0
    arguments.out.mkdir(parents=True, exist_ok=True)
    for name, text in expected.items():
        atomic_write_text(arguments.out / name, text, encoding="utf-8")
    print(f"wrote {len(expected) - 1} drafts and {INDEX} to {arguments.out}; nothing is posted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
