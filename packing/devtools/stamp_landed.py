#!/usr/bin/env python3
"""Record the day each register entry reached `main`, its `landed` date.

`registered` is the day a lane wrote an entry. The entry reaches `main`, and the site
built from it, when its pull request merges, which on the register as it stood on 14
October 2026 was the same day for 67 of 156 entries, a day later for 69 and two days
later for 20 (#514's review A, finding A1). The results page's "Added in the Last Seven
Days" and its table's Added filter read `landed`, so "added" means the day a reader
could first see the result there.

Three modes, from `packing/`:

- The default lists the entries that carry no `landed`; `--apply` stamps each with
  `--date`, today in UTC unless given. The merge step runs it on a records pull
  request's branch as the last commit before the merge, so the entries the branch adds
  carry the day they reach `main` (`campaign/result-import.md`, Stage 7).
- `--backfill` dates each entry without `landed` by the first commit on `origin/main`'s
  first-parent history whose register holds its id: the UTC day of that commit's
  committer date, which for a merged pull request is the merge. It ran once, when the
  field was introduced. History is read here, and the date is written into the record;
  nothing that renders a page reads Git (OR-18).
- `--check` holds every entry that `origin/main`'s register holds to a `landed` date no
  earlier than its `registered`. An entry a branch adds may lack one until the merge
  step stamps it; on `main` itself every entry is held, so a merge that skipped the
  stamp fails the next check there.

The tool inserts a `landed:` line after an entry's `registered:` line and leaves every
other byte of the file alone, so the diff is the stamp and nothing else. An entry that
already carries a date is never rewritten.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.stamp_landed
    uv run --frozen --all-extras --group dev python -m devtools.stamp_landed --apply
    uv run --frozen --all-extras --group dev python -m devtools.stamp_landed --check
    uv run --frozen --all-extras --group dev python -m devtools.stamp_landed --backfill --apply
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections.abc import Iterable, Mapping, Sequence
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
RESULTS = ROOT / "frontier" / "results.yaml"
#: The register's path from the repository root, as Git names it.
RESULTS_PATH = "packing/frontier/results.yaml"
#: The branch whose register every entry must be stamped against.
MAIN = "origin/main"

#: The first line of an entry, as the register writes it.
_ID_LINE = re.compile(r"^(?P<indent>\s*)- id: (?P<id>T-\d{3})\s*$")
_REGISTERED = re.compile(r"^(?P<indent>\s*)registered:")
_LANDED = re.compile(r"^\s*landed:")


def register_ids(text: str) -> list[str]:
    """The ids a register's text holds, in its order."""
    return [match["id"] for line in text.splitlines() if (match := _ID_LINE.match(line))]


def unstamped(text: str) -> list[str]:
    """The ids of the entries that carry no `landed` line, in the register's order."""
    lines = text.splitlines()
    missing: list[str] = []
    current: str | None = None
    for index, line in enumerate(lines):
        if match := _ID_LINE.match(line):
            current = match["id"]
        elif current and _REGISTERED.match(line):
            following = lines[index + 1] if index + 1 < len(lines) else ""
            if not _LANDED.match(following):
                missing.append(current)
            current = None
    return missing


def stamp(text: str, dates: Mapping[str, str]) -> str:
    """The register text with `landed: '<date>'` after the `registered:` line of each
    entry `dates` names that carries none."""
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    current: str | None = None
    for index, line in enumerate(lines):
        out.append(line)
        if match := _ID_LINE.match(line):
            current = match["id"]
            continue
        registered = _REGISTERED.match(line)
        if current is None or registered is None:
            continue
        following = lines[index + 1] if index + 1 < len(lines) else ""
        if current in dates and not _LANDED.match(following):
            out.append(f"{registered['indent']}landed: '{dates[current]}'\n")
        current = None
    return "".join(out)


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout


def first_landings(ref: str = MAIN, path: str = RESULTS_PATH) -> dict[str, str]:
    """Each id `ref`'s register has ever held, with the UTC day of the first commit on
    `ref`'s first-parent history whose register holds it."""
    landed: dict[str, str] = {}
    log = _git("log", "--first-parent", "--reverse", "--format=%H %cI", ref, "--", path)
    for line in log.splitlines():
        commit, when = line.split()
        day = datetime.fromisoformat(when).astimezone(UTC).date().isoformat()
        for result_id in register_ids(_git("show", f"{commit}:{path}")):
            landed.setdefault(result_id, day)
    return landed


def problems(register: Mapping[str, Any], on_main: Iterable[str]) -> list[str]:
    """What keeps the register's `landed` dates from being whole: an entry `main` holds
    without one, a malformed date, or a date before the entry's `registered`."""
    entries: dict[str, Mapping[str, Any]] = {
        str(entry["id"]): entry for entry in register["results"]
    }
    found: list[str] = []
    for result_id in on_main:
        entry = entries.get(result_id)
        if entry is not None and "landed" not in entry:
            found.append(f"{result_id} is on {MAIN} and carries no `landed` date")
    for result_id, entry in entries.items():
        if "landed" not in entry:
            continue
        try:
            landed = date.fromisoformat(str(entry["landed"]))
        except ValueError:
            found.append(f"{result_id}: `landed` {entry['landed']!r} is not a date")
            continue
        if landed < date.fromisoformat(str(entry["registered"])):
            found.append(
                f"{result_id} landed on {landed} before it was registered on "
                f"{entry['registered']}"
            )
    return found


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail on a missing or bad date")
    mode.add_argument("--backfill", action="store_true", help=f"date from {MAIN}'s history")
    parser.add_argument("--date", help="the day to stamp, YYYY-MM-DD (default: today, UTC)")
    parser.add_argument("--apply", action="store_true", help="write the dates in place")
    options = parser.parse_args(argv)
    text = RESULTS.read_text(encoding="utf-8")
    if options.check:
        found = problems(safe_load(text), register_ids(_git("show", f"{MAIN}:{RESULTS_PATH}")))
        for problem in found:
            print(f"  {problem}", file=sys.stderr)
        if found:
            print(f"landed dates: {len(found)} problem(s)", file=sys.stderr)
            return 1
        print(f"landed dates: every entry on {MAIN} carries one, none before registration")
        return 0
    missing = unstamped(text)
    if options.backfill:
        history = first_landings()
        dates = {result_id: history[result_id] for result_id in missing if result_id in history}
    else:
        day = options.date or datetime.now(UTC).date().isoformat()
        date.fromisoformat(day)
        dates = dict.fromkeys(missing, day)
    for result_id, day in dates.items():
        print(f"{result_id} {day}")
    if left := [result_id for result_id in missing if result_id not in dates]:
        print(f"not on {MAIN} yet, left for the merge step: {' '.join(left)}")
    if options.apply and dates:
        with atomic_output_file(RESULTS) as temporary:
            temporary.write_text(stamp(text, dates), encoding="utf-8")
        print(f"wrote {RESULTS.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
