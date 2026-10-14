#!/usr/bin/env python3
"""Backfill each register entry's `registered` date from the history of `results.yaml`.

A result's registration date is the author date of the first commit that added its
`id: T-NNN` line to the register, which `git log --reverse -m -S` finds. The `-m` is
load-bearing: `T-032` entered the register in a merge's conflict resolution, and a
pickaxe that skips merge diffs finds no commit for it at all. The Pages build
cannot read history (its checkout is sparse and shallow), so the date is written into
the record once, here, and reviewed as data like any other field; afterwards a new
entry carries its date from the start and this tool has nothing left to do.

It inserts a `registered:` line after the `id:`, `kind:` and optional `proves_kind:`
lines of every entry that
lacks one and leaves every other byte of the file alone, so the diff is the backfill and
nothing else. An entry the history does not know yet (added in the working tree and not
committed) is dated today. An entry that already carries a date is never rewritten.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.backfill_result_registration
    uv run --frozen --all-extras --group dev python -m devtools.backfill_result_registration \\
        --apply
"""

from __future__ import annotations

import argparse
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from strif import atomic_output_file

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
RESULTS = ROOT / "frontier" / "results.yaml"

#: The first line of an entry, as the register writes it.
_ID_LINE = re.compile(r"^(?P<indent>\s*)- id: (?P<id>T-\d{3})\s*$")
_REGISTERED = re.compile(r"^\s*registered:")
#: The line an entry writes right after its `id:`, which a backfilled date follows.
_KIND = re.compile(r"^\s*(?:kind|proves_kind):")


def first_added(result_id: str, path: Path = RESULTS) -> str | None:
    """The author date of the first commit that added `id: <result_id>` to the register."""
    found = subprocess.run(
        [
            "git",
            "log",
            "--reverse",
            "-m",
            "-S",
            f"id: {result_id}",
            "--format=%as",
            "--",
            str(path.relative_to(REPO)),
        ],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.split()
    return found[0] if found else None


def insert_dates(text: str, dates: dict[str, str]) -> str:
    """The register text with a `registered:` line in each undated entry, after its
    `id:`, `kind:` and any `proves_kind:` that follows them."""
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    entry: re.Match[str] | None = None
    for index, line in enumerate(lines):
        out.append(line)
        entry = _ID_LINE.match(line) or entry
        if entry is None:
            continue
        following = lines[index + 1] if index + 1 < len(lines) else ""
        if _KIND.match(following):
            continue
        if not _REGISTERED.match(following):
            indent = " " * (len(entry["indent"]) + 2)
            out.append(f"{indent}registered: '{dates[entry['id']]}'\n")
        entry = None
    return "".join(out)


def backfill(text: str, today: str) -> tuple[str, dict[str, str]]:
    """The backfilled text and the dates chosen, by id."""
    ids = [match["id"] for line in text.splitlines() if (match := _ID_LINE.match(line))]
    dates = {result_id: first_added(result_id) or today for result_id in ids}
    return insert_dates(text, dates), dates


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write the dates in place")
    options = parser.parse_args()
    text = RESULTS.read_text(encoding="utf-8")
    updated, dates = backfill(text, datetime.now(UTC).date().isoformat())
    for result_id, when in dates.items():
        print(f"{result_id} {when}")
    if options.apply and updated != text:
        with atomic_output_file(RESULTS) as temporary:
            temporary.write_text(updated, encoding="utf-8")
        print(f"wrote {RESULTS.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
