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
# `tbd` materializes the sync branch here; using it keeps the check offline.
WORKTREE = REPO / ".git" / "tbd" / "data-sync-worktree" / ISSUES
REFS = ("tbd-sync", "origin/tbd-sync")


def _parse(text: str) -> dict[str, Any] | None:
    """Pull the YAML frontmatter off one bead file."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    front = safe_load(text[4:end])
    return front if isinstance(front, dict) and "id" in front else None


def _from_worktree() -> tuple[list[dict[str, Any]], str] | None:
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
    return beads, where


def _from_git() -> tuple[list[dict[str, Any]], str] | None:
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
            return beads, ref
    return None


def load() -> tuple[list[dict[str, Any]], str] | None:
    return _from_worktree() or _from_git()


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

    beads, source = found
    problems = check(beads)
    if as_json:
        print(
            json.dumps(
                {
                    "status": "fail" if problems else "ok",
                    "source": source,
                    "beads": len(beads),
                    "problems": problems,
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
    if problems:
        print(f"FAIL {len(problems)} bead-tree problem(s); see D-025", file=sys.stderr)
        return 1
    print("  ok  no open bead under a closed parent, no duplicate open siblings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
