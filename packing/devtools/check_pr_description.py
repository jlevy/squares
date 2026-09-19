#!/usr/bin/env python3
"""Refuse a pull-request description that is a session log instead of the template.

OR-9 already says the page leads with cost and then reports results, dispositions,
grouped changes, validation, replanning, and limits. `.github/PULL_REQUEST_TEMPLATE.md`
is that order. Agents still paste a chronology: Session-141's first #201 draft, and the
Session-139/#199 and Session-140/#200 descriptions, opened with a cost sentence and a
probe list. #196 and #197 filled the template. The difference is scannable from the
headings alone.

This check is that heading contract plus the Cost grain. Template mode asks only
that the file still carries the required sections and table columns. Filled mode
also asks for one data row in each table, a selected next entry, Local and Hosted
validation, a Limits section that is not empty, and a Cost that is not a probe
list. Extra headings are allowed; the required ones must appear in order, and the
first `##` heading must be the cost block.

The first #201 rewrite had the headings and still opened Cost with every covering
wall. #196 and #197 open Cost with what the slice is and what it does not do.
Filled mode refuses the former.

Usage, from `packing/`:

```
uv run --frozen --all-extras --group dev python -m devtools.check_pr_description
uv run --frozen --all-extras --group dev python -m devtools.check_pr_description --file BODY.md
```
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TEMPLATE = REPO / ".github" / "PULL_REQUEST_TEMPLATE.md"

COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
HEADING = re.compile(r"^## (.+)$", re.MULTILINE)
TABLE_ROW = re.compile(r"^\|(.+)\|\s*$", re.MULTILINE)
EXPERIMENT = re.compile(r"\bexp-\d+\b")
WALL_BULLET = re.compile(
    r"^[-*]\s+.*(?:\bexp-\d+\b|\b\d{1,2}:\d{2}Z\b|\b\d+\s*s\b)",
    re.MULTILINE,
)
MAX_COST_EXPERIMENTS = 3
MAX_COST_WALL_BULLETS = 3

REQUIRED_HEADINGS = (
    "What this branch cost",
    "Results and Dispositions",
    "Changes by Purpose",
    "Validation",
    "Documentation and Replanning",
    "Limits",
)
DISPOSITION_COLUMNS = (
    "Work or result",
    "What was established",
    "Evidence",
    "Why it stopped",
    "Disposition and follow-up",
)
CHANGE_COLUMNS = ("Area", "Result", "Principal files or interfaces")


def strip_comments(text: str) -> str:
    """Drop HTML comments so placeholder guidance is not mistaken for content."""
    return COMMENT.sub("", text)


def headings(text: str) -> list[str]:
    return [match.group(1).strip() for match in HEADING.finditer(text)]


def _cells(row: str) -> list[str]:
    return [cell.strip() for cell in row.split("|")]


def table_after(text: str, heading: str) -> list[list[str]] | None:
    """The first pipe table after `heading`, or None if that heading is missing."""
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        return None
    rest = text[start + len(marker) :]
    next_heading = rest.find("\n## ")
    block = rest if next_heading < 0 else rest[:next_heading]
    rows = [_cells(match.group(1)) for match in TABLE_ROW.finditer(block)]
    return rows or None


def _columns_match(row: list[str], expected: Sequence[str]) -> bool:
    return tuple(row) == tuple(expected)


def _data_rows(rows: list[list[str]]) -> list[list[str]]:
    """Skip the header and the markdown separator; keep rows with a first cell."""
    data: list[list[str]] = []
    for index, row in enumerate(rows):
        if not row:
            continue
        if index == 0:
            continue
        if row and set(row[0]) <= {"-", ":"}:
            continue
        if any(cell for cell in row):
            data.append(row)
    return data


def _section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        return ""
    rest = text[start + len(marker) :]
    next_heading = rest.find("\n## ")
    return rest if next_heading < 0 else rest[:next_heading]


def check(text: str, *, filled: bool) -> list[str]:
    """Problems in `text`. Empty means the description matches the contract."""
    body = strip_comments(text)
    found = headings(body)
    problems: list[str] = []

    if not found:
        return ["no `##` headings; the description is not the pull-request template"]
    if found[0] != REQUIRED_HEADINGS[0]:
        problems.append(f"first heading is {found[0]!r}, not {REQUIRED_HEADINGS[0]!r}")

    required_seen = [heading for heading in found if heading in REQUIRED_HEADINGS]
    missing = [heading for heading in REQUIRED_HEADINGS if heading not in found]
    if missing:
        problems.append("missing heading " + ", ".join(repr(item) for item in missing))
    elif required_seen != list(REQUIRED_HEADINGS):
        problems.append(
            "required headings are out of order: "
            + ", ".join(repr(item) for item in required_seen)
        )

    disposition = table_after(body, "Results and Dispositions")
    if disposition is None:
        problems.append("Results and Dispositions has no table")
    elif not _columns_match(disposition[0], DISPOSITION_COLUMNS):
        problems.append(
            "Results and Dispositions columns are "
            f"{disposition[0]!r}, not {list(DISPOSITION_COLUMNS)!r}"
        )
    elif filled and not _data_rows(disposition):
        problems.append("Results and Dispositions has no data row")

    changes = table_after(body, "Changes by Purpose")
    if changes is None:
        problems.append("Changes by Purpose has no table")
    elif not _columns_match(changes[0], CHANGE_COLUMNS):
        problems.append(
            f"Changes by Purpose columns are {changes[0]!r}, not {list(CHANGE_COLUMNS)!r}"
        )
    elif filled and not _data_rows(changes):
        problems.append("Changes by Purpose has no data row")

    if filled:
        problems.extend(_cost_problems(_section(body, REQUIRED_HEADINGS[0])))
        validation = _section(body, "Validation")
        if not re.search(r"\bLocal\b", validation):
            problems.append("Validation does not name Local")
        if not re.search(r"\bHosted\b", validation):
            problems.append("Validation does not name Hosted")
        replanning = _section(body, "Documentation and Replanning")
        if not re.search(r"Selected next entry", replanning, re.IGNORECASE):
            problems.append("Documentation and Replanning has no Selected next entry")
        limits = _section(body, "Limits").strip()
        if not limits:
            problems.append("Limits is empty")

    return problems


def _cost_problems(cost: str) -> list[str]:
    """A Cost that lists every experiment is the chronology dump under a heading."""
    problems: list[str] = []
    named = EXPERIMENT.findall(cost)
    if len(named) > MAX_COST_EXPERIMENTS:
        problems.append(
            f"Cost names {len(named)} experiments; summarize the wall "
            f"(at most {MAX_COST_EXPERIMENTS} ids) and put the probes in "
            "Results and Dispositions"
        )
    bullets = WALL_BULLET.findall(cost)
    if len(bullets) > MAX_COST_WALL_BULLETS:
        problems.append(
            "Cost is a probe list; write 2-4 sentences of what the branch "
            "is, what it cost, and what it does not do"
        )
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--file",
        type=Path,
        help="filled description to check (default: the in-tree template)",
    )
    parser.add_argument(
        "--template",
        action="store_true",
        help="treat --file as a template even if it has empty rows",
    )
    args = parser.parse_args(argv)

    path = args.file if args.file is not None else TEMPLATE
    filled = args.file is not None and not args.template
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    problems = check(text, filled=filled)
    label = path if path != TEMPLATE else "pull-request template"
    if problems:
        for problem in problems:
            print(f"  FAIL {problem}")
        print(f"  {label} is not the OR-9 description")
        return 1
    kind = "filled description" if filled else "template"
    print(f"  ok  {kind} carries the OR-9 headings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
