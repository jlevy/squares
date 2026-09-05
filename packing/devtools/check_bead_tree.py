#!/usr/bin/env python3
"""Check the bead tree for the two shapes that made D-025 unreadable.

The beads are the work list. They live outside this directory -- on the `tbd-sync`
branch, not in the working tree -- so nothing in the gate could see them, and the one
time the tree went inconsistent it was found by a person reading `tbd list --spec` and
noticing two epics with the same title.

Two invariants are cheap and catch that whole class:

1. **No open bead sits under a closed parent.** A closed epic is a statement that its
   line of work is over; an open child under it is work nobody will list. This is
   exactly what D-025's first fix left behind -- it re-parented seven of eight children
   and reported "seven".
2. **No two open beads under one parent share a title.** Merging two trees that both
   modelled the same phase is how the duplicate arose; the duplicate is invisible in any
   view that shows one epic at a time.

Neither needs the `tbd` binary. The beads are Markdown-with-frontmatter files, and this
reads them straight out of git, preferring the local sync worktree so it works offline.

A third shape is reported and never failed on, because the agenda layer and the bead
tree are edited by different hands at different times and the gap between them is a
fact to read, not a violation to block a push on. An in-progress bead named only by
terminal agenda cells (`complete` or `stopped`) is work the agenda has finished with and
the tree still calls live; an in-progress bead named by no cell at all is work tracked
outside the agenda layer. Both lists are printed with their bead ids. Cells name beads
through the agenda's `bead` field, a `think-` alias that the store's `mappings/ids.yml`
resolves to the bead's id.

Run with `--json` for machine-readable output. Exits 0 when clean, 1 on a violation,
and 0 with a loud skip when no bead store can be found -- a checkout without the
`tbd-sync` branch is a normal state, not a failure.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]
ISSUES = ".tbd/data-sync/issues"
# The store's alias table: short code -> the ULID tail of the bead's id. An agenda's
# `bead: think-rh18` names the bead whose id ends in the table's entry for `rh18`.
MAPPINGS = ".tbd/data-sync/mappings/ids.yml"
# `tbd` materializes the sync branch here; using it keeps the check offline.
WORKTREE = REPO / ".git" / "tbd" / "data-sync-worktree" / ISSUES
REFS = ("tbd-sync", "origin/tbd-sync")
AGENDAS = REPO / "packing" / "campaign" / "agendas"
# The agenda schema's `bead` pattern is `^think-[a-z0-9]+$`; the part after the prefix
# is the alias table's key.
ALIAS_PREFIX = "think-"
IN_PROGRESS = "in_progress"
TERMINAL_STATES = frozenset({"complete", "stopped"})


def _parse(text: str) -> dict[str, Any] | None:
    """Pull the YAML frontmatter off one bead file."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    front = safe_load(text[4:end])
    return front if isinstance(front, dict) and "id" in front else None


def parse_aliases(text: str) -> dict[str, str]:
    """The alias table, short code -> ULID tail.

    Read line by line rather than as YAML: a four-character code such as `1e10`, `null`
    or `true` is a float, None or bool to a YAML loader and a key to `tbd`.
    """
    aliases: dict[str, str] = {}
    for line in text.splitlines():
        short, sep, tail = line.partition(":")
        if sep and not line.lstrip().startswith("#") and short.strip() and tail.strip():
            aliases[short.strip()] = tail.strip()
    return aliases


def _from_worktree() -> tuple[list[dict[str, Any]], str, dict[str, str]] | None:
    if not WORKTREE.is_dir():
        return None
    beads = []
    for f in sorted(WORKTREE.glob("is-*.md")):
        b = _parse(f.read_text(encoding="utf-8"))
        if b:
            beads.append(b)
    if not beads:
        return None
    try:
        where = str(WORKTREE.relative_to(REPO))
    except ValueError:  # a store outside the repo, as the fault-injection tests use
        where = str(WORKTREE)
    mapping = WORKTREE.parent / "mappings" / "ids.yml"
    aliases = parse_aliases(mapping.read_text(encoding="utf-8")) if mapping.is_file() else {}
    return beads, where, aliases


def _from_git() -> tuple[list[dict[str, Any]], str, dict[str, str]] | None:
    for ref in REFS:
        try:
            listing = subprocess.run(
                ["git", "ls-tree", "-r", "--name-only", ref, ISSUES],
                cwd=REPO,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.split()
        except subprocess.CalledProcessError, OSError:
            continue
        names = [n for n in listing if Path(n).name.startswith("is-")]
        if not names:
            continue
        beads = []
        for name in names:
            blob = subprocess.run(
                ["git", "show", f"{ref}:{name}"],
                cwd=REPO,
                capture_output=True,
                text=True,
                check=False,
            )
            if blob.returncode == 0:
                b = _parse(blob.stdout)
                if b:
                    beads.append(b)
        if beads:
            table = subprocess.run(
                ["git", "show", f"{ref}:{MAPPINGS}"],
                cwd=REPO,
                capture_output=True,
                text=True,
                check=False,
            )
            aliases = parse_aliases(table.stdout) if table.returncode == 0 else {}
            return beads, ref, aliases
    return None


def load() -> tuple[list[dict[str, Any]], str, dict[str, str]] | None:
    return _from_worktree() or _from_git()


def agenda_cells(agendas: Path = AGENDAS) -> list[dict[str, str]]:
    """Every agenda cell as (id, agenda, state, bead), read from the agendas' frontmatter."""
    cells: list[dict[str, str]] = []
    for path in sorted(agendas.glob("agenda-*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        agenda = (safe_load(text[4 : text.index("\n---", 4)]) or {}).get("agenda") or {}
        cells.extend(
            {
                "id": str(item["id"]),
                "agenda": str(agenda.get("id", path.name)),
                "state": str(item.get("state", "")),
                "bead": str(item.get("bead", "")),
            }
            for item in agenda.get("items") or []
        )
    return cells


def staleness(
    beads: list[dict[str, Any]],
    aliases: dict[str, str],
    cells: list[dict[str, str]],
) -> dict[str, list[dict[str, Any]]]:
    """In-progress beads the agenda layer has lost track of, in the two shapes reported.

    `stale`: every cell naming the bead is terminal. `untracked`: no cell names it. A
    bead with at least one live naming cell is in neither. Each entry carries the bead's
    alias when the table has one, its id otherwise, its title, and the naming cells with
    their states, so the printed report needs no second lookup.
    """
    bead_by_tail = {str(b["id"]).rpartition("-")[2]: str(b["id"]) for b in beads}
    alias_of = {
        bead_by_tail[tail]: f"{ALIAS_PREFIX}{short}"
        for short, tail in aliases.items()
        if tail in bead_by_tail
    }
    naming: dict[str, list[dict[str, str]]] = defaultdict(list)
    for cell in cells:
        tail = aliases.get(cell["bead"].removeprefix(ALIAS_PREFIX))
        bead_id = bead_by_tail.get(tail or "")
        if bead_id:
            naming[bead_id].append(cell)
    report: dict[str, list[dict[str, Any]]] = {"stale": [], "untracked": []}
    for b in beads:
        if b.get("status") != IN_PROGRESS:
            continue
        bead_id = str(b["id"])
        named_by = naming.get(bead_id, [])
        entry = {
            "bead": alias_of.get(bead_id, bead_id),
            "title": str(b.get("title", "")),
            "cells": [f"{c['id']} {c['state']}" for c in named_by],
        }
        if not named_by:
            report["untracked"].append(entry)
        elif all(c["state"] in TERMINAL_STATES for c in named_by):
            report["stale"].append(entry)
    return report


def check(beads: list[dict[str, Any]]) -> list[dict[str, str]]:
    by_id = {b["id"]: b for b in beads}
    problems: list[dict[str, str]] = []

    for b in beads:
        parent = by_id.get(b.get("parent_id") or "")
        if b.get("status") == "open" and parent and parent.get("status") == "closed":
            problems.append(
                {
                    "kind": "open_under_closed",
                    "bead": str(b.get("title", b["id"])),
                    "parent": str(parent.get("title", parent["id"])),
                }
            )

    siblings: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for b in beads:
        if b.get("status") == "open":
            siblings[(str(b.get("parent_id") or ""), str(b.get("title", "")))].append(b)
    for (parent_id, title), group in sorted(siblings.items()):
        if len(group) > 1:
            parent = by_id.get(parent_id)
            problems.append(
                {
                    "kind": "duplicate_title",
                    "bead": title,
                    "parent": str(parent.get("title", parent_id)) if parent else "(root)",
                }
            )
    return problems


def main() -> int:
    as_json = "--json" in sys.argv
    found = load()
    if found is None:
        msg = "SKIP no bead store found (no tbd-sync worktree or branch); bead tree unchecked"
        print(json.dumps({"status": "skipped"}) if as_json else msg)
        return 0

    beads, source, aliases = found
    problems = check(beads)
    report = staleness(beads, aliases, agenda_cells() if AGENDAS.is_dir() else [])
    if as_json:
        print(
            json.dumps(
                {
                    "status": "fail" if problems else "ok",
                    "source": source,
                    "beads": len(beads),
                    "problems": problems,
                    "staleness": report,
                }
            )
        )
        return 1 if problems else 0

    print(f"  {len(beads)} beads from {source}")
    for p in problems:
        if p["kind"] == "open_under_closed":
            print(f"  FAIL open bead {p['bead']!r} sits under closed parent {p['parent']!r}")
        else:
            print(f"  FAIL two open beads titled {p['bead']!r} under {p['parent']!r}")
    # Reported, never failed on: see the module docstring for why.
    stale, untracked = report["stale"], report["untracked"]
    print(f"  report {len(stale)} in-progress bead(s) named only by terminal agenda cells")
    for entry in stale:
        print(f"    {entry['bead']}  {', '.join(entry['cells'])}  {entry['title']}")
    print(f"  report {len(untracked)} in-progress bead(s) named by no agenda cell")
    for entry in untracked:
        print(f"    {entry['bead']}  {entry['title']}")
    if problems:
        print(f"FAIL {len(problems)} bead-tree problem(s); see D-025", file=sys.stderr)
        return 1
    print("  ok  no open bead under a closed parent, no duplicate open siblings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
