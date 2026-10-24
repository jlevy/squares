#!/usr/bin/env python3
"""Check the bead tree for the shapes that made D-025 unreadable, and who owns each deferral.

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

A third invariant joins the tree to the records:

3. **Every deferral a record declares names a bead that is still open.** A deferral is
   work the record knows it has not done: a Kingbird count pending intake, a
   beyond-horizon claim held as a deferred conflict, a watched repository read past its
   newest packet, an issue still open, a result or ask queued on one, in the
   regularization record a count allowed to stay pending, an exempt count, or a decided
   count whose runs are still owed (`devtools.default_drawings.deferrals`), and a count
   whose house adoption is staged (`devtools.select_houses.deferrals`). Each names its
   owning bead (`deferrals`, `regularization_deferrals`, `adoption_deferrals`), and a bead
   is still open while its state is one `devtools.bead_state.LIVE` holds: `closed` and
   `deferred` are not. The three counts
   pending intake from 2026-09-30 named none, nothing listed them, and the record called
   the older sides best known for five days; a bead closed under a live deferral is the
   same orphan by another route.

   The third reads the bead store, which changes with no tracked change at all, so in
   the gate it fails only a change to a record that declares deferrals: the gate passes
   `--warn-dead-deferrals` otherwise, and a dead deferral is printed as a warning. A
   continuous-integration checkout fetches `origin/tbd-sync`, so closing a bead a record
   names would otherwise turn every pull request and `main` red on a change that touched
   nothing. Closing such a bead therefore takes a record edit in the same change, and
   the next change to the record fails until it has one. Run directly, with no flag, the
   check fails a dead deferral wherever it is, as `devtools.intake_sweep` lists it.

None needs the `tbd` binary. The beads are Markdown-with-frontmatter files, and this
reads them straight out of git, preferring the local sync worktree so it works offline.

One more shape is reported and never failed on, because the agenda layer and the bead
tree are edited by different hands at different times and the gap between them is a
fact to read, not a violation to block a push on. An in-progress bead named only by
terminal agenda cells (`complete` or `stopped`) is work the agenda has finished with and
the tree still calls live; an in-progress bead named by no cell at all is work tracked
outside the agenda layer. Both lists are printed with their bead ids. Cells name beads
through the agenda's `bead` field, a `think-` alias that the store's `mappings/ids.yml`
resolves to the bead's id.

Run with `--json` for machine-readable output, and `--warn-dead-deferrals` to report a
dead deferral without failing on it. Exits 0 when clean, 1 on a violation, and 0 with a
loud skip when no bead store can be found -- a checkout without the `tbd-sync` branch is
a normal state, not a failure.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from devtools.bead_state import ISSUES, LIVE, MAPPINGS, REFS, parse_aliases
from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]
# `tbd` materializes the sync branch here; using it keeps the check offline.
WORKTREE = REPO / ".git" / "tbd" / "data-sync-worktree" / ISSUES
AGENDAS = REPO / "packing" / "campaign" / "agendas"
COVERAGE = REPO / "packing" / "frontier" / "source-coverage.yaml"
REQUESTS = REPO / "packing" / "campaign" / "result-requests.yaml"
INTAKE_WATCH = REPO / "packing" / "campaign" / "intake-watch.yaml"
#: The flag the gate passes when the change touches none of the records declaring
#: deferrals: the three above, `devtools/default_drawings.py` and
#: `devtools/select_houses.py`.
WARN_DEAD_DEFERRALS = "--warn-dead-deferrals"
# The agenda schema's `bead` pattern is `^think-[a-z0-9]+$`; the part after the prefix
# is the alias table's key.
ALIAS_PREFIX = "think-"
#: What a queued result or ask that names no bead is collected with: it defers to no one.
NO_BEAD = "no bead"
IN_PROGRESS = "in_progress"
TERMINAL_STATES = frozenset({"complete", "stopped"})


#: The key under which a parsed bead carries its Markdown body: the description and
#: notes `devtools.intake_sweep` reads for the blocker a bead says it waits on.
BODY = "_body"


def _parse(text: str) -> dict[str, Any] | None:
    """Pull the YAML frontmatter off one bead file, with the body under `BODY`."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    front = safe_load(text[4:end])
    if not isinstance(front, dict) or "id" not in front:
        return None
    front[BODY] = text[end + 5 :]
    return front


def _worktree() -> Path:
    """The sync worktree's issues: under `.git`, or the common directory of a linked
    worktree, where `.git` is a file and reading the branch blob by blob took 17 s."""
    if WORKTREE.is_dir():
        return WORKTREE
    common = subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", "--path-format=absolute", "--git-common-dir"],
        capture_output=True,
        text=True,
        check=False,
    )
    if common.returncode == 0:
        return Path(common.stdout.strip()) / "tbd" / "data-sync-worktree" / ISSUES
    return WORKTREE


def _from_worktree() -> tuple[list[dict[str, Any]], str, dict[str, str]] | None:
    worktree = _worktree()
    if not worktree.is_dir():
        return None
    beads = []
    for f in sorted(worktree.glob("is-*.md")):
        b = _parse(f.read_text(encoding="utf-8"))
        if b:
            beads.append(b)
    if not beads:
        return None
    try:
        where = str(worktree.relative_to(REPO))
    except ValueError:  # a linked worktree's store, or one a fault-injection test made
        where = str(worktree)
    mapping = worktree.parent / "mappings" / "ids.yml"
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


def _records(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    loaded = safe_load(path.read_text(encoding="utf-8"))
    return loaded if isinstance(loaded, dict) else {}


def deferrals(
    coverage: Path = COVERAGE, requests: Path = REQUESTS, watch: Path = INTAKE_WATCH
) -> list[tuple[str, str]]:
    """Every deferral the records declare that names a bead, as (where, the bead alias).

    This check asks whether what is named still owns the work; whether one is named is
    the records' own business. Their schemas require a bead of a pending intake, a
    deferred conflict, an issue's `answer_bead` and, since think-du1e, each queued
    result and ask. A queued item that names none anyway is collected with `NO_BEAD`,
    so a record the schema check did not see still fails here; a read in
    `intake-watch.yaml` without a bead found nothing to import, so it defers nothing.
    """
    named: list[tuple[str, str]] = []
    source = _records(coverage)
    named.extend(
        (
            f"source-coverage.yaml pending_catalogue_intake n={entry.get('n')}",
            str(entry["bead"]),
        )
        for entry in source.get("pending_catalogue_intake") or ()
        if entry.get("bead")
    )
    named.extend(
        (f"source-coverage.yaml deferred conflict n={entry.get('n')}", str(entry["bead"]))
        for entry in source.get("beyond_horizon_claims") or ()
        if entry.get("disposition") == "deferred-conflict" and entry.get("bead")
    )
    for issue in _records(requests).get("issues") or ():
        if issue.get("state") != "open":
            continue
        where = f"result-requests.yaml open issue #{issue.get('number')}"
        if issue.get("answer_bead"):
            named.append((where, str(issue["answer_bead"])))
        named.extend(
            (f"{where} queued result {result.get('key')}", str(result.get("bead") or NO_BEAD))
            for result in issue.get("results") or ()
            if result.get("queued")
        )
        named.extend(
            (f"{where} queued ask", str(ask.get("bead") or NO_BEAD))
            for ask in issue.get("asks") or ()
            if ask.get("state") == "queued"
        )
    named.extend(
        (
            (
                f"intake-watch.yaml {entry.get('url')} read through "
                f"{str(entry.get('read_through'))[:12]}"
            ),
            str(entry["bead"]),
        )
        for entry in _records(watch).get("repositories") or ()
        if entry.get("bead")
    )
    return named


def regularization_deferrals() -> list[tuple[str, str]]:
    """The regularization record's deferrals, as (where, the bead alias): each count
    `default_drawings.PENDING_ALLOWED` allows pending, each exemption and each decision's
    `owed` bead (review A2 of #636). Imported here, not at the top, so that what else
    reads this module (`devtools.intake_sweep`) does not load the measuring code."""
    from devtools import default_drawings  # noqa: PLC0415

    return default_drawings.deferrals()


def adoption_deferrals() -> list[tuple[str, str]]:
    """Each count `select_houses.PENDING_ADOPTION` stages for a later adoption, as (where,
    the bead alias): the bead adopts it, so it stays open while the count is staged."""
    from devtools import select_houses  # noqa: PLC0415

    return select_houses.deferrals()


def deferral_problems(
    beads: list[dict[str, Any]], aliases: dict[str, str], named: list[tuple[str, str]]
) -> list[dict[str, str]]:
    """Each declared deferral whose bead does not exist or no longer owns work."""
    status = {str(b["id"]).rpartition("-")[2]: str(b.get("status")) for b in beads}
    problems: list[dict[str, str]] = []
    for where, alias in named:
        tail = aliases.get(alias.removeprefix(ALIAS_PREFIX))
        found = status.get(tail or "")
        if found in LIVE:
            continue
        problems.append(
            {
                "kind": "dead_deferral",
                "bead": alias,
                "parent": where,
                "status": "unowned" if alias == NO_BEAD else found or "no such bead",
            }
        )
    return problems


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


def main(argv: Sequence[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    as_json = "--json" in arguments
    warn_deferrals = WARN_DEAD_DEFERRALS in arguments
    found = load()
    if found is None:
        msg = "SKIP no bead store found (no tbd-sync worktree or branch); bead tree unchecked"
        print(json.dumps({"status": "skipped"}) if as_json else msg)
        return 0

    beads, source, aliases = found
    dead = deferral_problems(
        beads, aliases, [*deferrals(), *regularization_deferrals(), *adoption_deferrals()]
    )
    problems = check(beads) + ([] if warn_deferrals else dead)
    warnings = dead if warn_deferrals else []
    report = staleness(beads, aliases, agenda_cells() if AGENDAS.is_dir() else [])
    if as_json:
        print(
            json.dumps(
                {
                    "status": "fail" if problems else "ok",
                    "source": source,
                    "beads": len(beads),
                    "problems": problems,
                    "warnings": warnings,
                    "staleness": report,
                }
            )
        )
        return 1 if problems else 0

    print(f"  {len(beads)} beads from {source}")
    for p in problems:
        if p["kind"] == "open_under_closed":
            print(f"  FAIL open bead {p['bead']!r} sits under closed parent {p['parent']!r}")
        elif p["kind"] == "dead_deferral":
            print(
                f"  FAIL {p['parent']} names {p['bead']} ({p['status']}); a deferral names "
                "the open bead that owns it"
            )
        else:
            print(f"  FAIL two open beads titled {p['bead']!r} under {p['parent']!r}")
    for p in warnings:
        print(
            f"  WARN {p['parent']} names {p['bead']} ({p['status']}); the change touches no "
            "record that declares a deferral, so this does not fail it, and the next change "
            "to the record must name an open bead"
        )
    # Reported, never failed on: see the module docstring for why.
    stale, untracked = report["stale"], report["untracked"]
    print(f"  report {len(stale)} in-progress bead(s) named only by terminal agenda cells")
    for entry in stale:
        print(f"    {entry['bead']}  {', '.join(entry['cells'])}  {entry['title']}")
    print(f"  report {len(untracked)} in-progress bead(s) named by no agenda cell")
    for entry in untracked:
        print(f"    {entry['bead']}  {entry['title']}")
    if problems:
        print(
            f"FAIL {len(problems)} bead-tree problem(s); see D-025 and D-519", file=sys.stderr
        )
        return 1
    print(
        "  ok  no open bead under a closed parent, no duplicate open siblings, "
        + (
            f"{len(warnings)} deferral(s) whose bead is not open, reported above"
            if warnings
            else "every deferral owned by an open bead"
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
