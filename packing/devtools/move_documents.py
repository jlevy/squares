#!/usr/bin/env python3
"""Move tracked documents and repoint every reference to them, dry-run by default.

A lifecycle move such as ``specs/active/`` to ``specs/done/`` breaks references in
shapes that a search for the old path misses. Bare-filename and ``./`` links between
sibling specs resolve against the linking file, ``../`` links between lifecycle folders
lack the ``specs/`` prefix, and the moved file's own relative links break because it
now stands somewhere else. This rewrites all of them from one move list:

- every Markdown link, inline or reference-style, in any tracked Markdown file, whose
  target resolves to a moved file, and every relative link inside a moved file;
- every repository-relative occurrence of a moved path in any tracked text file, which
  covers ``document-map.yaml``, declared ``recorded_in`` paths and code constants.

Frozen records keep the paths they recorded: the literature archive, bead
reconciliation receipts and patches are excluded, and ``--exclude`` adds more. Bead
``spec_path`` values live in the tracker, not the tree; repoint them with ``tbd``.
"""

from __future__ import annotations

import argparse
import fnmatch
import posixpath
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
#: Records that keep the paths they recorded, and trees that are not this repository's.
DEFAULT_EXCLUDES = (
    "packing/resources/*",
    "docs/project/reviews/review-*-bead-reconciliation-*.json",
    "*.patch",
    "vendor/*",
)
TEXT_SUFFIXES = frozenset(
    {".md", ".yaml", ".yml", ".json", ".py", ".ts", ".js", ".toml", ".txt", ".html"}
)
INLINE_LINK = re.compile(r"(!?\[[^\]]*\]\()(<?)([^)\s>]+)(>?)((?:\s+\"[^\"]*\")?\))")
REFERENCE_LINK = re.compile(r"^(\s{0,3}\[[^\]]+\]:\s*)(<?)(\S+?)(>?)(\s|$)", re.MULTILINE)
PATH_CHARACTER = r"[A-Za-z0-9_.\-/]"


@dataclass
class Plan:
    """What a move list would change, before anything is written."""

    moves: dict[str, str]
    rewrites: dict[str, str] = field(default_factory=dict)
    counts: dict[str, int] = field(default_factory=dict)
    problems: list[str] = field(default_factory=list)


def tracked(repo: Path) -> list[str]:
    listed = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z"], check=True, capture_output=True
    ).stdout
    return sorted(path for path in listed.decode().split("\0") if path)


def excluded(path: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def _relink(target: str, source_old: str, source_new: str, moves: dict[str, str]) -> str:
    """The target rewritten for the source's new place, or unchanged when nothing moved."""
    if re.match(r"^[a-z][a-z0-9+.\-]*:", target) or target.startswith(("/", "#")):
        return target
    path, hash_mark, fragment = target.partition("#")
    if not path:
        return target
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source_old), path))
    destination = moves.get(resolved, resolved)
    if source_old == source_new and destination == resolved:
        return target
    rewritten = posixpath.relpath(destination, posixpath.dirname(source_new) or ".")
    if path.startswith("./") and not rewritten.startswith("../"):
        rewritten = f"./{rewritten}"
    return f"{rewritten}{hash_mark}{fragment}"


def rewrite(text: str, source_old: str, moves: dict[str, str]) -> tuple[str, int]:
    """Repoint the links and repository paths in one file's text, with a change count."""
    source_new = moves.get(source_old, source_old)
    changes = 0

    def link(match: re.Match[str]) -> str:
        nonlocal changes
        prefix, opening, target, closing, suffix = match.groups()
        relinked = _relink(target, source_old, source_new, moves)
        changes += relinked != target
        return f"{prefix}{opening}{relinked}{closing}{suffix}"

    if source_old.endswith(".md"):
        text = INLINE_LINK.sub(link, text)
        text = REFERENCE_LINK.sub(link, text)
    for old, new in moves.items():
        pattern = re.compile(rf"(?<!{PATH_CHARACTER}){re.escape(old)}(?!{PATH_CHARACTER})")
        text, count = pattern.subn(new, text)
        changes += count
    return text, changes


def plan(moves: dict[str, str], repo: Path, excludes: tuple[str, ...]) -> Plan:
    result = Plan(moves=moves)
    files = tracked(repo)
    present = set(files)
    for old, new in moves.items():
        if old not in present:
            result.problems.append(f"source is not a tracked file: {old}")
        if (repo / new).exists():
            result.problems.append(f"target already exists: {new}")
    if result.problems:
        return result
    for path in files:
        if Path(path).suffix not in TEXT_SUFFIXES or excluded(path, excludes):
            continue
        try:
            text = (repo / path).read_text(encoding="utf-8")
        except OSError, UnicodeDecodeError:
            continue
        updated, count = rewrite(text, path, moves)
        if updated != text:
            result.rewrites[path] = updated
            result.counts[path] = count
    return result


def apply(result: Plan, repo: Path) -> None:
    for path, text in result.rewrites.items():
        (repo / path).write_text(text, encoding="utf-8")
    for old, new in result.moves.items():
        (repo / new).parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "-C", str(repo), "mv", old, new], check=True)


def parse_moves(pairs: list[str]) -> dict[str, str]:
    moves: dict[str, str] = {}
    for pair in pairs:
        old, sep, new = pair.partition("=")
        if not sep or not old or not new:
            raise ValueError(f"expected OLD=NEW, got {pair!r}")
        moves[posixpath.normpath(old)] = posixpath.normpath(new)
    return moves


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Move tracked documents and repoint every reference to them."
    )
    parser.add_argument("moves", nargs="+", metavar="OLD=NEW", help="repo-relative paths")
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--exclude", action="append", default=[], metavar="GLOB")
    parser.add_argument("--apply", action="store_true", help="write and git mv")
    args = parser.parse_args(argv)
    try:
        moves = parse_moves(args.moves)
    except ValueError as error:
        parser.error(str(error))
    result = plan(moves, args.repo, (*DEFAULT_EXCLUDES, *args.exclude))
    for problem in result.problems:
        print(f"refused: {problem}", file=sys.stderr)
    if result.problems:
        return 1
    for old, new in moves.items():
        print(f"move {old} -> {new}")
    for path, count in sorted(result.counts.items()):
        print(f"  {count:3d} reference(s) in {path}")
    if args.apply:
        apply(result, args.repo)
        print(f"applied {len(moves)} move(s), rewrote {len(result.rewrites)} file(s)")
    else:
        print(f"dry run: {len(moves)} move(s), {len(result.rewrites)} file(s); --apply writes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
