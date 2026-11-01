#!/usr/bin/env python3
"""Count the merges whose two sides conflicted, and the top-level block each conflict hit.

Parallel pull requests pay for a shared hunk at every merge of `main` into the others: a
re-merge, a hand resolution and a fresh CI cycle each. Which file, and which block of it,
costs that is a measurement, not a recollection, so this recomputes each retained merge
with `git merge-tree --write-tree` from its two parents and reads the conflict markers Git
writes. Nothing is checked out and the working tree is never touched.

A conflict hunk is attributed to the nearest top-level line above it: in Python the name
the statement binds (`RELEASE_NO_PUBLIC_CHANGES`), elsewhere the line itself, cut short.
Each merge is charged to the pull request whose first-parent merge into `--ref` brings it
in, so a branch that merged `main` three times shows three merges under its number.

From `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.merge_conflicts \\
        --since 2026-10-30 --path packing/src/sqpack/release.py

Written for think-nrp6, the efficiency block that moved the no-public-change records out
of one tuple in `release.py`; rerun it over a later window to see whether the block still
conflicts.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
_PULL_REQUEST = re.compile(r"^Merge pull request #(\d+)\b")
_PYTHON_NAME = re.compile(r"^(?:async def |def |class )?([A-Za-z_]\w*)")
_CLOSERS = tuple(")]}")
_MARKERS = ("<<<<<<< ", "=======", ">>>>>>> ", "||||||| ")


@dataclass(frozen=True)
class Conflict:
    """One recomputed merge that conflicted, and where."""

    merge: str
    date: str
    subject: str
    pull_request: int | None
    blocks: tuple[tuple[str, str, int], ...]
    """(path, block, hunks) for every conflicted path the filter keeps."""
    union: tuple[tuple[str, str], ...] = ()
    """With `--union`, (path, verdict) for what a `merge=union` driver would have made of
    each conflicted path: `resolution` when it equals what the merge committed, `parses`
    when it differs but is still valid Python, `broken` when it is not, and `differs` for
    a path that is not Python."""


@dataclass(frozen=True)
class Census:
    """Every merge examined in the window and the ones that conflicted."""

    ref: str
    since: str
    merges: int
    pull_requests: int
    conflicts: tuple[Conflict, ...]


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    """Git's output as bytes: a conflicted file can be binary, and one undecodable file
    must not stop the census (review A of #873)."""
    result = subprocess.run(["git", *args], cwd=repo, capture_output=True, check=False)
    if check and result.returncode:
        raise ValueError(f"git {args[0]} failed: {_text(result.stderr).strip()}")
    return result


def _text(output: bytes) -> str:
    """Output as text, every undecodable byte kept, so a path read here names its file."""
    return output.decode("utf-8", errors="surrogateescape")


def _label(path: str, line: str) -> str | None:
    """The block a top-level line opens, or None for a line that opens none."""
    python = path.endswith(".py")
    if not line.strip() or line[0].isspace() or line.startswith(_MARKERS):
        return None
    if line.startswith(_CLOSERS) or (python and line.startswith(("#", "@"))):
        return None
    match = _PYTHON_NAME.match(line) if python else None
    return match.group(1) if match else line.strip()[:60]


def block_of(path: str, lines: Sequence[str], index: int) -> str:
    """The block a conflict hunk whose `<<<<<<<` marker is line `index` falls in.

    A top-level line on the hunk's own side names it, since a statement the hunk starts
    is the one in conflict; otherwise the nearest top-level line above it does.
    """
    for line in lines[index + 1 :]:
        if line.startswith(("=======", "||||||| ")):
            break
        if (label := _label(path, line)) is not None:
            return label
    for line in reversed(lines[:index]):
        if (label := _label(path, line)) is not None:
            return label
    return "(top of file)"


def conflicted_blocks(
    repo: Path, first: str, second: str, paths: Sequence[str] = ()
) -> tuple[tuple[str, str, int], ...]:
    """Recompute one merge and attribute its conflict hunks; empty when it merges clean."""
    result = _git(
        repo,
        "merge-tree",
        "--write-tree",
        "--name-only",
        "--no-messages",
        first,
        second,
        check=False,
    )
    if result.returncode == 0:
        return ()
    if result.returncode != 1:
        raise ValueError(f"git merge-tree failed: {_text(result.stderr).strip()}")
    tree, *names = [line for line in _text(result.stdout).splitlines() if line]
    counted: dict[tuple[str, str], int] = defaultdict(int)
    for name in dict.fromkeys(names):
        if paths and name not in paths:
            continue
        shown = _git(repo, "cat-file", "-p", f"{tree}:{name}", check=False)
        lines = _text(shown.stdout).splitlines() if shown.returncode == 0 else []
        starts = [index for index, line in enumerate(lines) if line.startswith("<<<<<<< ")]
        if not starts:
            # A modify/delete or binary conflict leaves no markers in the file.
            counted[name, "(whole file)"] += 1
        for index in starts:
            counted[name, block_of(name, lines, index)] += 1
    return tuple((path, block, hunks) for (path, block), hunks in sorted(counted.items()))


def union_verdict(repo: Path, merge: str, first: str, second: str, path: str) -> str:
    """What `git merge-file --union` makes of `path` against the committed resolution.

    A union driver keeps both sides of every conflicting hunk, with no markers. That is
    the right answer only where both sides' lines belong in the file in that order.
    """
    base = _text(_git(repo, "merge-base", first, second).stdout).split()[0]
    with tempfile.TemporaryDirectory() as scratch:
        sides = []
        for name, revision in (("ours", first), ("base", base), ("theirs", second)):
            shown = _git(repo, "show", f"{revision}:{path}", check=False)
            side = Path(scratch) / name
            side.write_bytes(shown.stdout if shown.returncode == 0 else b"")
            sides.append(str(side))
        union = _git(repo, "merge-file", "--union", "-p", *sides, check=False).stdout
    resolved = _git(repo, "show", f"{merge}:{path}", check=False).stdout
    if union == resolved:
        return "resolution"
    if not path.endswith(".py"):
        return "differs"
    try:
        # Compiled, not only parsed: two records fused into one call repeat a keyword,
        # which the parser accepts and the compiler refuses.
        compile(union, path, "exec", dont_inherit=True)
    except SyntaxError, ValueError:
        return "broken"
    return "parses"


def census(
    repo: Path = REPO,
    *,
    ref: str = "origin/main",
    since: str,
    paths: Sequence[str] = (),
    union: bool = False,
) -> Census:
    """Recompute every two-parent merge reachable from `ref` since `since`."""
    owner: dict[str, int] = {}
    first_parent = _git(
        repo, "log", "--first-parent", "--merges", f"--since={since}", "--format=%H %s", ref
    ).stdout
    for line in _text(first_parent).splitlines():
        commit, _, subject = line.partition(" ")
        match = _PULL_REQUEST.match(subject)
        if match is None:
            continue
        number = int(match.group(1))
        owner[commit] = number
        inside = _git(repo, "log", "--merges", "--format=%H", f"{commit}^1..{commit}^2")
        for merge in _text(inside.stdout).split():
            owner.setdefault(merge, number)
    listed = _git(
        repo, "log", "--merges", f"--since={since}", "--format=%H%x09%P%x09%as%x09%s", ref
    ).stdout
    rows = _text(listed).splitlines()
    conflicts = []
    for row in rows:
        commit, parents, date, subject = row.split("\t", 3)
        sides = parents.split()
        if len(sides) != 2:
            continue
        first, second = sides
        blocks = conflicted_blocks(repo, first, second, paths=paths)
        if not blocks:
            continue
        verdicts = (
            tuple(
                (path, union_verdict(repo, commit, first, second, path))
                for path in dict.fromkeys(path for path, _block, _hunks in blocks)
            )
            if union
            else ()
        )
        conflicts.append(Conflict(commit, date, subject, owner.get(commit), blocks, verdicts))
    return Census(ref, since, len(rows), len(set(owner.values())), tuple(conflicts))


def summary(report: Census) -> list[str]:
    """Per path and block: the merges that conflicted there, how many conflicted nowhere
    else (the merges a fix to that block alone would have made clean), and their PRs."""
    merges: dict[tuple[str, str], list[Conflict]] = defaultdict(list)
    for conflict in report.conflicts:
        for path, block, _hunks in conflict.blocks:
            merges[path, block].append(conflict)
    lines = [
        (
            f"{report.merges} merges reachable from {report.ref} since {report.since}, in "
            f"{report.pull_requests} pull requests; {len(report.conflicts)} conflicted"
        )
    ]
    for (path, block), found in sorted(merges.items(), key=lambda item: -len(item[1])):
        numbers = sorted({c.pull_request for c in found if c.pull_request is not None})
        sole = sum(len(conflict.blocks) == 1 for conflict in found)
        lines.append(
            f"{path} :: {block}: {len(found)} merges ({sole} conflicting nowhere else) "
            f"in {len(numbers)} PRs ({', '.join(f'#{number}' for number in numbers)})"
        )
    verdicts: dict[str, Counter[str]] = defaultdict(Counter)
    alone: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for conflict in report.conflicts:
        for path, verdict in conflict.union:
            verdicts[path][verdict] += 1
            # The merges a block was the only conflict in are the ones a driver for that
            # block alone would have had to get right (review A of #873, finding 8).
            if len(conflict.blocks) == 1 and conflict.blocks[0][0] == path:
                alone[path, conflict.blocks[0][1]][verdict] += 1

    def counts(counted: Counter[str]) -> str:
        return ", ".join(f"{verdict} {count}" for verdict, count in sorted(counted.items()))

    lines += [
        f"{path} under merge=union: {counts(counted)}"
        for path, counted in sorted(verdicts.items())
    ]
    lines += [
        f"{path} :: {block}, where it was the only conflict, under merge=union: "
        + counts(counted)
        for (path, block), counted in sorted(alone.items())
    ]
    return lines


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", required=True, help="Earliest merge date, as git reads it")
    parser.add_argument("--ref", default="origin/main")
    parser.add_argument(
        "--path", action="append", default=[], help="Keep only these conflicted paths"
    )
    parser.add_argument(
        "--union",
        action="store_true",
        help="Also say what a merge=union driver would have made of each conflicted path",
    )
    parser.add_argument("--json", action="store_true")
    options = parser.parse_args(argv)
    try:
        report = census(
            ref=options.ref, since=options.since, paths=options.path, union=options.union
        )
    except ValueError as error:
        print(f"merge conflicts: {error}", file=sys.stderr)
        return 1
    if options.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print("\n".join(summary(report)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
