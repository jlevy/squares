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
  covers ``document-map.yaml``, ``.flowmarkignore``, declared ``recorded_in`` paths and
  code constants. A file is text when it decodes as UTF-8 and holds no NUL byte,
  whatever its name; a tracked file that is not text but names a moved path is reported.

Fenced code in Markdown is left as it stands, and a moved path inside it is reported
for a decision by hand; code spans are not links, so only their exact repository paths
change. Footnote definitions are not links. ``math-markup.yaml`` is kept sorted. Line
endings are kept byte for byte.

Frozen records keep the paths they recorded: the literature archive, every
reconciliation record under ``docs/project/reviews/``, run receipts and logs
(``*.jsonl``) and patches are excluded, and ``--exclude`` adds more. A file whose Git
blob a tracked tool pins (a replay binding its sources byte for byte, such as
``devtools.replay_bc303_t1_witness``) is kept as it stands and reported, since any edit
breaks that binding. Tracked symbolic links are never written through. Bead
``spec_path`` values live in the tracker, not the tree; repoint them with ``tbd``.

The whole move list is validated before anything is written: every path stays inside
the repository, targets are distinct, new and not another move's source, and no parent
of a target is a file. ``--apply`` then moves every file with ``git mv`` and writes each
rewrite at its new place; if any step fails, every move is undone and every file is
restored before the error is raised.
"""

from __future__ import annotations

import argparse
import fnmatch
import functools
import posixpath
import re
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]
#: Records that keep the paths they recorded, and trees that are not this repository's.
DEFAULT_EXCLUDES = (
    "packing/resources/*",
    "docs/project/reviews/review-*.json",
    "*.jsonl",
    "*.patch",
    "vendor/*",
)
INLINE_LINK = re.compile(
    r"(!?\[[^\]]*\]\()(<?)([^)\s>]+)(>?)"
    r"((?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\))"
)
#: A reference definition; ``[^…]:`` is a footnote, whose text is prose, not a target.
REFERENCE_LINK = re.compile(
    r"^([ \t]{0,3}\[(?!\^)[^\]]+\]:[ \t]*)(<?)(\S+?)(>?)(\s|$)", re.MULTILINE
)
FENCE_OPEN = re.compile(r"^[ \t]*(`{3,}|~{3,})(.*)$")
FENCE_CLOSE = re.compile(r"^[ \t]*(`{3,}|~{3,})[ \t]*$")
#: A code span: matched backtick runs, never across a blank line; a backslash-escaped
#: backtick opens none.
CODE_SPAN = re.compile(r"(?<![`\\])(`+)(?!`)((?:(?!\n[ \t]*\r?\n).)+?)(?<!`)\1(?!`)", re.DOTALL)
#: A path character before a match, and after it; a period ends a path unless a path
#: character follows it, so a path that ends a sentence still matches.
PATH_BEFORE = r"(?<![A-Za-z0-9_.\-/])"
PATH_AFTER = r"(?![A-Za-z0-9_\-/]|\.[A-Za-z0-9_\-/])"
MASK = "\0"
#: Where tools that pin a file's Git blob live; a pinned blob freezes that file's bytes.
PINNING_TOOLS = "packing/devtools/*.py"
BLOB = re.compile(r"\b[0-9a-f]{40}\b")
#: The math-markup register, whose ``migrated`` and ``exempt`` lists the check
#: requires sorted by path.
MATH_MARKUP = "packing/devtools/math-markup.yaml"
REGULAR_MODES = frozenset({"100644", "100755"})
GITLINK_MODE = "160000"


@dataclass
class Plan:
    """What a move list would change, before anything is written."""

    moves: dict[str, str]
    rewrites: dict[str, str] = field(default_factory=dict)
    counts: dict[str, int] = field(default_factory=dict)
    problems: list[str] = field(default_factory=list)
    kept: list[str] = field(default_factory=list)
    #: Tracked files that name a moved path but are not text, so were not rewritten.
    skipped: list[str] = field(default_factory=list)
    #: Markdown files with a moved path left inside fenced code, and how many.
    fenced: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class Entry:
    """One tracked path's index mode and staged blob."""

    mode: str
    blob: str


def entries(repo: Path) -> dict[str, Entry]:
    """Every tracked path with its mode and staged blob hash."""
    listed = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-s", "-z"], check=True, capture_output=True
    ).stdout
    found: dict[str, Entry] = {}
    for entry in listed.decode().split("\0"):
        if entry:
            meta, _, path = entry.partition("\t")
            mode, blob, _ = meta.split(maxsplit=2)
            found[path] = Entry(mode, blob)
    return found


def tracked(repo: Path) -> list[str]:
    return sorted(entries(repo))


def blobs(repo: Path) -> dict[str, str]:
    """Each tracked path's staged blob hash."""
    return {path: entry.blob for path, entry in entries(repo).items()}


def pinned_blobs(repo: Path, files: list[str]) -> frozenset[str]:
    """Blob hashes that a tracked tool names, which freeze the files that carry them."""
    pinned: set[str] = set()
    for path in files:
        if fnmatch.fnmatch(path, PINNING_TOOLS):
            pinned.update(BLOB.findall((repo / path).read_text(encoding="utf-8")))
    return frozenset(pinned)


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
    if path.endswith("/") and not rewritten.endswith("/"):
        rewritten += "/"
    if path.startswith("./") and not rewritten.startswith("../"):
        rewritten = f"./{rewritten}"
    return f"{rewritten}{hash_mark}{fragment}"


def fenced_ranges(text: str) -> list[tuple[int, int]]:
    """The character ranges of fenced code blocks; an unclosed fence runs to the end."""
    ranges: list[tuple[int, int]] = []
    offset = start = 0
    fence = ""
    for line in text.splitlines(keepends=True):
        bare = line.rstrip("\r\n")
        if not fence:
            if (opening := FENCE_OPEN.match(bare)) and not (
                opening.group(1)[0] == "`" and "`" in opening.group(2)
            ):
                fence, start = opening.group(1), offset
        elif (closing := FENCE_CLOSE.match(bare)) and (
            closing.group(1)[0] == fence[0] and len(closing.group(1)) >= len(fence)
        ):
            ranges.append((start, offset + len(line)))
            fence = ""
        offset += len(line)
    if fence:
        ranges.append((start, len(text)))
    return ranges


def _masked(text: str, ranges: list[tuple[int, int]]) -> str:
    """The text with each range's characters, other than line breaks, masked out."""
    pieces: list[str] = []
    last = 0
    for start, end in ranges:
        pieces.append(text[last:start])
        pieces.append(re.sub(r"[^\r\n]", MASK, text[start:end]))
        last = end
    pieces.append(text[last:])
    return "".join(pieces)


def _substitute(
    text: str,
    masked: str,
    pattern: re.Pattern[str],
    replace: Callable[[tuple[str, ...]], str],
    guarded: int = 0,
) -> tuple[str, int]:
    """Replace each match of ``pattern`` whose ``guarded`` group is not masked out.

    Matching runs on the masked text, which has the same length as the text, and each
    group is read back from the text itself, so a link whose label is a code span keeps
    its label.
    """
    pieces: list[str] = []
    last = changes = 0
    for match in pattern.finditer(masked):
        if MASK in match.group(guarded):
            continue
        groups = tuple(
            text[start:end] if start >= 0 else ""
            for start, end in (match.span(index) for index in range(pattern.groups + 1))
        )
        replacement = replace(groups)
        if replacement != groups[0]:
            pieces.append(text[last : match.start()])
            pieces.append(replacement)
            last = match.end()
            changes += 1
    pieces.append(text[last:])
    return "".join(pieces), changes


def _link(
    groups: tuple[str, ...], source_old: str, source_new: str, moves: dict[str, str]
) -> str:
    _, prefix, opening, target, closing, suffix = groups
    return f"{prefix}{opening}{_relink(target, source_old, source_new, moves)}{closing}{suffix}"


def _path(groups: tuple[str, ...], moves: dict[str, str]) -> str:
    return moves[groups[0]]


@functools.lru_cache(maxsize=8)
def _path_pattern(olds: tuple[str, ...]) -> re.Pattern[str]:
    """One pattern for every moved path, longest first, so a file is read once."""
    alternatives = "|".join(re.escape(old) for old in sorted(olds, key=len, reverse=True))
    return re.compile(rf"{PATH_BEFORE}(?:{alternatives}){PATH_AFTER}")


def _code(text: str) -> list[tuple[int, int]]:
    """Fenced blocks and code spans, which hold no links."""
    fences = fenced_ranges(text)
    spans = [match.span() for match in CODE_SPAN.finditer(_masked(text, fences))]
    return sorted([*fences, *spans])


def rewrite(text: str, source_old: str, moves: dict[str, str]) -> tuple[str, int]:
    """Repoint the links and repository paths in one file's text, with a change count."""
    source_new = moves.get(source_old, source_old)
    changes = 0
    markdown = source_old.endswith(".md")
    if markdown:
        relink = functools.partial(
            _link, source_old=source_old, source_new=source_new, moves=moves
        )
        for pattern in (INLINE_LINK, REFERENCE_LINK):
            masked = _masked(text, _code(text))
            text, count = _substitute(text, masked, pattern, relink, guarded=3)
            changes += count
    if moves:
        masked = _masked(text, fenced_ranges(text)) if markdown else text
        replace = functools.partial(_path, moves=moves)
        text, count = _substitute(text, masked, _path_pattern(tuple(moves)), replace)
        changes += count
    return text, changes


def left_in_fences(text: str, moves: dict[str, str]) -> int:
    """How many moved paths a Markdown text keeps inside fenced code."""
    pattern = _path_pattern(tuple(moves))
    return sum(len(pattern.findall(text[start:end])) for start, end in fenced_ranges(text))


def sort_math_markup(text: str) -> str:
    """Re-sort the register's ``migrated`` paths and ``exempt`` entries, keeping comments.

    Each top-level list is cut into entries at its ``- `` lines, and each entry keeps its
    indented continuation lines. Blank and comment lines after the last entry stay
    there; a list with such a line between its entries is left as it stands.
    """
    sections: list[tuple[str, list[str]]] = [("", [])]
    for line in text.splitlines(keepends=True):
        if re.match(r"^[A-Za-z_]+:\s*$", line):
            sections.append((line.split(":", 1)[0], [line]))
        else:
            sections[-1][1].append(line)
    out: list[str] = []
    for name, block in sections:
        out.extend(_sorted_list(block, name) if name in {"migrated", "exempt"} else block)
    return "".join(out)


def _sorted_list(block: list[str], name: str) -> list[str]:
    head, body = block[:1], block[1:]
    tail: list[str] = []
    while body and (not body[-1].strip() or body[-1].startswith("#")):
        tail.insert(0, body.pop())
    items: list[list[str]] = []
    for line in body:
        if line.startswith("- "):
            items.append([line])
        elif items and line[:1].isspace() and line.strip():
            items[-1].append(line)
        else:
            return block

    def key(item: list[str]) -> str:
        loaded = safe_load("".join(item))
        value = loaded[0] if isinstance(loaded, list) and loaded else None
        if name == "exempt" and isinstance(value, dict):
            return str(value.get("path", ""))
        return str(value)

    return [*head, *(line for item in sorted(items, key=key) for line in item), *tail]


def _inside(repo: Path, path: str) -> bool:
    if posixpath.isabs(path) or path == "." or path.split("/", 1)[0] == "..":
        return False
    root = repo.resolve()
    return (root / path).resolve().is_relative_to(root)


def validate(moves: dict[str, str], repo: Path, index: dict[str, Entry]) -> list[str]:
    """Every reason the whole move list cannot run, before anything is written."""
    problems: list[str] = []
    targets: dict[str, str] = {}
    for old, new in moves.items():
        outside = [path for path in (old, new) if not _inside(repo, path)]
        problems.extend(f"path is outside the repository: {path}" for path in outside)
        if outside:
            continue
        if old not in index:
            problems.append(f"source is not a tracked file: {old}")
        elif index[old].mode not in REGULAR_MODES:
            problems.append(f"source is not a regular file: {old}")
        if old == new:
            problems.append(f"source and target are the same: {old}")
        if new in targets:
            problems.append(f"two moves share one target: {targets[new]} and {old} -> {new}")
        targets.setdefault(new, old)
        if new in moves:
            problems.append(f"target is another move's source: {new}")
        elif (repo / new).exists() or (repo / new).is_symlink():
            problems.append(f"target already exists: {new}")
        parent = posixpath.dirname(new)
        while parent:
            if parent in index and index[parent].mode == GITLINK_MODE:
                problems.append(f"target is inside a submodule: {new}")
                break
            if parent in moves.values() or (
                (repo / parent).exists() and not (repo / parent).is_dir()
            ):
                problems.append(f"target's parent is a file: {new}")
                break
            parent = posixpath.dirname(parent)
    return problems


def plan(moves: dict[str, str], repo: Path, excludes: tuple[str, ...]) -> Plan:
    result = Plan(moves=moves)
    index = entries(repo)
    result.problems = validate(moves, repo, index)
    if result.problems:
        return result
    files = sorted(index)
    frozen = pinned_blobs(repo, files)
    names = re.compile("|".join(re.escape(posixpath.basename(old)) for old in moves))
    needles = [old.encode() for old in moves]
    for path in files:
        entry = index[path]
        if entry.mode not in REGULAR_MODES or excluded(path, excludes):
            continue
        try:
            data = (repo / path).read_bytes()
        except OSError:
            continue
        if b"\0" in data:
            text = None
        else:
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                text = None
        if text is None:
            if any(needle in data for needle in needles):
                result.skipped.append(path)
            continue
        if path not in moves and not names.search(text):
            continue
        updated, count = rewrite(text, path, moves)
        if path.endswith(".md") and (left := left_in_fences(updated, moves)):
            result.fenced[path] = left
        if updated != text and path == MATH_MARKUP:
            updated = sort_math_markup(updated)
        if updated != text and entry.blob in frozen:
            result.kept.append(path)
        elif updated != text:
            result.rewrites[path] = updated
            result.counts[path] = count
    return result


def git_mv(repo: Path, old: str, new: str) -> None:
    subprocess.run(["git", "-C", str(repo), "mv", "--", old, new], check=True)


def apply(result: Plan, repo: Path) -> None:
    """Move every file, then write every rewrite at its new place; undo all on failure."""
    originals = {path: (repo / path).read_bytes() for path in result.rewrites}
    moved: list[tuple[str, str]] = []
    created: list[Path] = []
    try:
        for old, new in result.moves.items():
            parent = (repo / new).parent
            missing = [parent, *parent.parents]
            created.extend(
                reversed(
                    [path for path in missing if not path.exists() and repo in path.parents]
                )
            )
            parent.mkdir(parents=True, exist_ok=True)
            git_mv(repo, old, new)
            moved.append((old, new))
        for path, text in result.rewrites.items():
            (repo / result.moves.get(path, path)).write_bytes(text.encode("utf-8"))
    except BaseException:
        for old, new in reversed(moved):
            git_mv(repo, new, old)
        for path, data in originals.items():
            (repo / path).write_bytes(data)
        for directory in reversed(created):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()
        raise


def parse_moves(pairs: list[str]) -> dict[str, str]:
    moves: dict[str, str] = {}
    for pair in pairs:
        old, sep, new = pair.partition("=")
        if not sep or not old or not new:
            raise ValueError(f"expected OLD=NEW, got {pair!r}")
        source = posixpath.normpath(old)
        if source in moves:
            raise ValueError(f"{source} is moved twice")
        moves[source] = posixpath.normpath(new)
    return moves


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Move tracked documents and repoint every reference to them."
    )
    parser.add_argument("moves", nargs="+", metavar="OLD=NEW", help="repo-relative paths")
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--exclude", action="append", default=[], metavar="GLOB")
    parser.add_argument("--apply", action="store_true", help="git mv and write")
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

    def place(path: str) -> str:
        """A moved file by both paths, so a report still points at it after --apply."""
        return f"{path} -> {moves[path]}" if path in moves else path

    for path, count in sorted(result.counts.items()):
        print(f"  {count:3d} reference(s) in {place(path)}")
    for path in result.kept:
        print(f"  kept, its blob is pinned by a tool: {place(path)}")
    for path in result.skipped:
        print(f"  skipped, not text: {place(path)}")
    for path, count in sorted(result.fenced.items()):
        print(f"  left in fenced code, decide by hand: {place(path)} ({count})")
    if args.apply:
        apply(result, args.repo)
        print(f"applied {len(moves)} move(s), rewrote {len(result.rewrites)} file(s)")
    else:
        print(f"dry run: {len(moves)} move(s), {len(result.rewrites)} file(s); --apply writes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
