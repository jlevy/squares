#!/usr/bin/env python3
"""Record the day each register entry reached `main`, its `landed` date.

`registered` is the day a lane wrote an entry. The entry reaches `main`, and the site
built from it, when its pull request merges: on the register of 14 October 2026, 67 of
160 entries the same day, 69 a day later and 24 two days later (#514's review A,
finding A1). The results page's "Added in the Last Seven Days" and its table's Added
filters read `landed`, so "added" means the day a reader could first see the result.

Every entry carries `landed`; `results.schema.yaml` requires it. A lane writes it with
the entry, as the day it registers it, and the merge step re-dates the entries a records
pull request adds to the day it merges. No gate reads Git: the schema holds the field's
presence and `problems` its form and order, both on the tree alone (OR-18; #514's review
B, finding B3). A pull request whose re-date is forgotten reads a day or two early, the
lag A1 measured, and nothing turns red; `--audit` finds it.

Modes, from `packing/`:

- The default is the merge step. It lists the entries `origin/main`'s register does not
  hold, the ones this branch adds, and `--apply` re-dates each to `--date`, today in UTC
  unless given. Run it, with its re-pin, as the last commits before a records pull
  request merges (`campaign/result-import.md`, Stage 5, Before merge). Run again after a
  re-merge, or when the merge slipped past midnight UTC, it re-dates them again. So
  `landed` is the day of the stamp, which is the merge day when the stamp is the last
  step before the merge.
- `--audit` compares the `landed` of every entry `origin/main` holds with `main`'s
  first-parent history: the UTC day of the first commit whose register holds the entry,
  for a merged pull request the merge. It lists each that differs, and `--apply`
  corrects them. It gates nothing; the intake sweep runs it, and its corrections ride
  the next records pull request.
- `--backfill` dates each entry that has no `landed` the same way. It ran once, when the
  field was introduced.

History is read only here, by a tool, and its answer is written into the record; nothing
that renders a page or gates a change reads Git (OR-18).

The tool rewrites an entry's `landed:` line, or inserts one after its `registered:` line,
and leaves every other byte of the file alone. The ids are the parsed register's and must
match a scan of its `- id:` lines, so an entry the scan cannot see fails loudly rather than
going unstamped (#514's review B, finding B7).

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.stamp_landed
    uv run --frozen --all-extras --group dev python -m devtools.stamp_landed --apply
    uv run --frozen --all-extras --group dev python -m devtools.stamp_landed --audit
    uv run --frozen --all-extras --group dev python -m devtools.stamp_landed --audit --apply
"""

from __future__ import annotations

import argparse
import re
import subprocess
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
#: The branch whose register says which entries a branch adds, and whose first-parent
#: history says when each entry landed.
MAIN = "origin/main"

#: The first line of an entry, as the register writes it, its id bare or quoted.
_ID_LINE = re.compile(
    r"""^(?P<indent>\s*)- id: (?P<quote>['"]?)(?P<id>[^'"\s]+)(?P=quote)\s*$"""
)
_REGISTERED = re.compile(r"^(?P<indent>\s*)registered:")
_LANDED = re.compile(r"^\s*landed:")


def register_ids(text: str) -> list[str]:
    """The ids a register's text holds, in its order: the parsed register's, which a scan
    of its `- id:` lines must find the same, so that `set_landed` can reach every one."""
    parsed = [str(entry["id"]) for entry in safe_load(text)["results"]]
    scanned = [match["id"] for line in text.splitlines() if (match := _ID_LINE.match(line))]
    if parsed != scanned:
        missed = sorted(set(parsed) - set(scanned)) or sorted(set(scanned) - set(parsed))
        raise ValueError(
            "the register's `- id:` lines do not match its parsed entries"
            f"{': ' + ', '.join(missed) if missed else ', in order'}"
        )
    return parsed


def recorded(text: str) -> dict[str, str | None]:
    """Each entry's `landed` as the register records it, or None where it has none."""
    register_ids(text)
    return {
        str(entry["id"]): (str(entry["landed"]) if "landed" in entry else None)
        for entry in safe_load(text)["results"]
    }


def set_landed(text: str, dates: Mapping[str, str]) -> str:
    """The register text with each entry `dates` names landed on its date: its `landed:`
    line rewritten, or one inserted after its `registered:` line. Every other byte is
    kept."""
    register_ids(text)
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    current: str | None = None
    for index, line in enumerate(lines):
        if match := _ID_LINE.match(line):
            current = match["id"]
            out.append(line)
            continue
        registered = _REGISTERED.match(line)
        if current is None or registered is None or current not in dates:
            out.append(line)
            continue
        out.append(line)
        following = lines[index + 1] if index + 1 < len(lines) else ""
        stamp = f"{registered['indent']}landed: '{dates[current]}'\n"
        if _LANDED.match(following):
            lines[index + 1] = stamp
        else:
            out.append(stamp)
        current = None
    return "".join(out)


def branch_entries(text: str, main_text: str) -> list[str]:
    """The ids a branch's register holds that `main`'s does not: the entries it adds."""
    on_main = set(register_ids(main_text))
    return [result_id for result_id in register_ids(text) if result_id not in on_main]


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


def audit(
    dates: Mapping[str, str | None], history: Mapping[str, str], on_main: Iterable[str]
) -> dict[str, str]:
    """The entries on `main` whose recorded `landed` differs from the day its first-parent
    history gives, with that day."""
    return {
        result_id: history[result_id]
        for result_id in on_main
        if result_id in dates
        and result_id in history
        and dates[result_id] != history[result_id]
    }


def problems(register: Mapping[str, Any]) -> list[str]:
    """What keeps the register's `landed` dates whole, read from the tree alone: an entry
    without one, a malformed date, or a date before the entry's `registered`."""
    found: list[str] = []
    for entry in register["results"]:
        result_id = str(entry["id"])
        if "landed" not in entry:
            found.append(f"{result_id} carries no `landed` date")
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
    mode.add_argument("--audit", action="store_true", help=f"compare with {MAIN}'s history")
    mode.add_argument("--backfill", action="store_true", help="date entries that have none")
    parser.add_argument("--date", help="the merge step's day, YYYY-MM-DD (default: today, UTC)")
    parser.add_argument("--apply", action="store_true", help="write the dates in place")
    options = parser.parse_args(argv)
    text = RESULTS.read_text(encoding="utf-8")
    current = recorded(text)
    if options.audit or options.backfill:
        history = first_landings()
        if options.audit:
            on_main = register_ids(_git("show", f"{MAIN}:{RESULTS_PATH}"))
            dates = audit(current, history, on_main)
            for result_id, day in dates.items():
                print(f"{result_id} records {current[result_id]}; {MAIN} took it in on {day}")
            print(f"landed audit: {len(dates)} of {len(on_main)} entries on {MAIN} differ")
        else:
            dates = {
                result_id: history[result_id]
                for result_id, day in current.items()
                if day is None and result_id in history
            }
            for result_id, day in dates.items():
                print(f"{result_id} {day}")
    else:
        day = options.date or datetime.now(UTC).date().isoformat()
        date.fromisoformat(day)
        dates = dict.fromkeys(branch_entries(text, _git("show", f"{MAIN}:{RESULTS_PATH}")), day)
        for result_id in dates:
            print(f"{result_id} {current[result_id] or 'none'} -> {day}")
        if not dates:
            print(f"this branch adds no entry to {MAIN}'s register; nothing to stamp")
    if options.apply and dates:
        with atomic_output_file(RESULTS) as temporary:
            temporary.write_text(set_landed(text, dates), encoding="utf-8")
        print(f"wrote {RESULTS.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
