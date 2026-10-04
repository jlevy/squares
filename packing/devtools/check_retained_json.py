#!/usr/bin/env python3
"""A large retained JSON file is written in `sqpack.retained_json`'s layout.

`json.dumps(..., indent=2)` puts every scalar on its own line, and a retained result
written that way is mostly brackets and indentation: `atlas/known-best/chunk-components.json`
was 365,916 lines. `sqpack.retained_json.dumps` writes a value on one line when that line
fits in its width and opens it otherwise, so a record is a line and a long vector a block of
full lines. Converting the writers does not hold the convention on its own: the next tool
written with `indent=2` brings the next hundred thousand lines back, and nothing says so.
This sweep does.

**The rule.** Every JSON file the repository tracks with more lines than the policy's
`threshold_lines` must equal its own re-layout -- `retained_json.dumps` of its parsed value,
with `ensure_ascii` read off the bytes -- unless the policy exempts it. The comparison is
exact, so a file re-laid by hand, or written by a writer that passes the wrong arguments,
fails as surely as one written with `indent=2`. Files at or under the threshold are not
read past their line count, which is what keeps the sweep about a second over the whole
tree. Two kinds of tracked JSON are not retained results and are never swept: hand-written
schemas (`*.schema.json`) and the JSON Biome formats, named by `biome.json` itself.

**The exemptions** are in `devtools/retained-json.yaml`, each with its reason and what
binds its bytes: archived source, which is never edited; a file whose bytes a record, test
or verifier names by SHA-256 or Git blob; the certificate family; frozen historical output;
an owner's open decision; and a conversion still pending, which names its bead. A stale
exemption fails the sweep too, so the list only shrinks: an entry that covers no tracked
file over the threshold, and a pending conversion whose file is already in the layout.

**Re-laying an existing file never re-runs what produced it.** `--fix PATH...` writes each
file's re-layout in place and refuses unless the value is unchanged, compared as canonical
compact JSON -- `json.dumps` with no whitespace, keys in file order, non-ASCII unescaped.
That is a stricter test than `==`, which takes `1`, `1.0` and `True` for one another, and
the parse that feeds it refuses a duplicate key, which `json.loads` would otherwise drop
without a word. It refuses an exempt file whose reason is anything but `pending`.

Usage, from `packing/`, each after `uv run --frozen --all-extras --group dev`:
    python -m devtools.check_retained_json
    python -m devtools.check_retained_json PATH...
    python -m devtools.check_retained_json --fix PATH...
    python -m devtools.check_retained_json --inventory

With paths and no `--fix`, only those files are checked, and the exemptions are not
judged for staleness; a negative control uses that form, since its worker's snapshot omits
some exempt files on purpose.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.repo_scope import tracked_files
from sqpack import retained_json
from sqpack.yamlio import safe_load

#: Resolved from this file, so a negative control that corrupts a snapshot's copy of the
#: policy or of a retained file is checking the snapshot's copies.
ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
POLICY = ROOT / "devtools" / "retained-json.yaml"

REASONS = frozenset(
    {"archive", "digest-bound", "certificate", "frozen", "owner-decision", "pending"}
)
#: Directories the fallback walk skips, where there is no index to ask.
SKIP = frozenset({".venv", ".git", "node_modules", "__pycache__", ".mypy_cache", ".ruff_cache"})
#: Hand-written schemas are documents a person edits, not results a tool retains.
SCHEMA_SUFFIX = ".schema.json"


@dataclass(frozen=True, slots=True)
class Exemption:
    """One policy entry: an exact repository-relative path, or a glob over such paths."""

    pattern: str
    is_glob: bool
    reason: str
    bound_by: str
    bead: str | None

    def matches(self, relative: str) -> bool:
        if self.is_glob:
            return _glob(self.pattern).fullmatch(relative) is not None
        return relative == self.pattern


@dataclass(frozen=True, slots=True)
class Policy:
    threshold_lines: int
    exemptions: tuple[Exemption, ...]

    def exemption(self, relative: str) -> Exemption | None:
        return next((entry for entry in self.exemptions if entry.matches(relative)), None)


@dataclass(frozen=True, slots=True)
class Candidate:
    """A swept file over the threshold: its path, line count and bytes."""

    relative: str
    lines: int
    data: bytes


@cache
def _glob(pattern: str) -> re.Pattern[str]:
    """A repository-relative glob: `**` crosses directories, `*` and `?` do not."""
    parts: list[str] = []
    index = 0
    while index < len(pattern):
        if pattern.startswith("**/", index):
            parts.append("(?:.*/)?")
            index += 3
        elif pattern.startswith("**", index):
            parts.append(".*")
            index += 2
        elif pattern[index] == "*":
            parts.append("[^/]*")
            index += 1
        elif pattern[index] == "?":
            parts.append("[^/]")
            index += 1
        else:
            parts.append(re.escape(pattern[index]))
            index += 1
    return re.compile("".join(parts))


def load_policy(path: Path = POLICY) -> Policy:
    """The policy file, refused whole if any entry is malformed."""
    document = safe_load(path.read_text(encoding="utf-8"))
    threshold = document.get("threshold_lines")
    if not isinstance(threshold, int) or threshold < 1:
        raise ValueError(f"{path.name}: threshold_lines must be a positive integer")
    entries: list[Exemption] = []
    for index, raw in enumerate(document.get("exempt") or ()):
        where = f"{path.name}: exempt[{index}]"
        if not isinstance(raw, dict):
            raise TypeError(f"{where} is not a mapping")
        keys = set(raw)
        if len(keys & {"path", "glob"}) != 1:
            raise ValueError(f"{where} needs exactly one of path or glob")
        unknown = keys - {"path", "glob", "reason", "bound_by", "bead"}
        if unknown:
            raise ValueError(f"{where} has unknown keys {sorted(unknown)}")
        reason = raw.get("reason")
        if reason not in REASONS:
            raise ValueError(
                f"{where}: reason must be one of {sorted(REASONS)}, not {reason!r}"
            )
        bound_by = raw.get("bound_by")
        if not isinstance(bound_by, str) or not bound_by.strip():
            raise ValueError(f"{where} needs a bound_by naming what holds its bytes")
        bead = raw.get("bead")
        if (reason == "pending") != (bead is not None):
            raise ValueError(f"{where}: a pending conversion, and only one, names its bead")
        is_glob = "glob" in raw
        pattern = raw["glob" if is_glob else "path"]
        entries.append(
            Exemption(
                str(pattern),
                is_glob,
                str(reason),
                bound_by,
                None if bead is None else str(bead),
            )
        )
    patterns = [entry.pattern for entry in entries]
    duplicated = sorted({pattern for pattern in patterns if patterns.count(pattern) > 1})
    if duplicated:
        raise ValueError(f"{path.name}: listed twice: {duplicated}")
    return Policy(threshold, tuple(entries))


def biome_owned(root: Path = REPO) -> tuple[re.Pattern[str], ...]:
    """The JSON globs `biome.json` includes: Biome formats those files, so they are not
    results a Python writer lays out."""
    config = root / "biome.json"
    if not config.is_file():
        return ()
    includes = (
        json.loads(config.read_text(encoding="utf-8")).get("files", {}).get("includes", [])
    )
    return tuple(
        _glob(pattern)
        for pattern in includes
        if isinstance(pattern, str)
        and not pattern.startswith("!")
        and pattern.endswith(".json")
    )


def is_retained(relative: str, biome: Iterable[re.Pattern[str]]) -> bool:
    """Whether a tracked JSON file is a retained result the sweep holds to the layout."""
    if relative.endswith(SCHEMA_SUFFIX):
        return False
    return not any(pattern.fullmatch(relative) for pattern in biome)


def _json_files(root: Path) -> list[Path]:
    found = tracked_files(root, "*.json")
    if found is None:
        found = sorted(path for path in root.rglob("*.json") if not SKIP & set(path.parts))
    return found


def candidates(
    root: Path,
    paths: Iterable[Path],
    threshold: int,
    *,
    unread: Callable[[str], bool] | None = None,
) -> list[Candidate]:
    """The retained files among `paths` with more than `threshold` lines.

    A file of N lines holds at least N bytes, so one no larger than the threshold is
    passed over without being read, and so is any file `unread` declines; that is most of
    the tree.
    """
    biome = biome_owned(root)
    top = root.resolve()
    found: list[Candidate] = []
    for path in paths:
        relative = path.resolve().relative_to(top).as_posix()
        if not is_retained(relative, biome) or path.stat().st_size <= threshold:
            continue
        if unread is not None and unread(relative):
            continue
        data = path.read_bytes()
        lines = data.count(b"\n")
        if lines > threshold:
            found.append(Candidate(relative, lines, data))
    return found


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _ in pairs]
    if len(keys) != len(set(keys)):
        repeated = sorted({key for key in keys if keys.count(key) > 1})
        raise ValueError(f"duplicate keys {repeated[:3]}")
    return dict(pairs)


def parse(text: str) -> Any:
    """The JSON value of `text`, refusing a duplicate key rather than dropping one."""
    return json.loads(text, object_pairs_hook=_pairs)


def canonical(value: Any) -> str:
    """Compact JSON, keys in the order they stand: equal exactly when the values are
    equal as JSON, which `==` is not -- it takes 1, 1.0 and True for one another."""
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


def relayout(text: str) -> str:
    """`text` in the retained layout, with `ensure_ascii` read off the bytes: a file with
    any raw non-ASCII character was written with it off, and one without reads the same
    either way."""
    return retained_json.dumps(parse(text), ensure_ascii=text.isascii())


def check(
    root: Path = REPO, *, paths: Sequence[Path] | None = None, policy: Policy | None = None
) -> tuple[list[str], int]:
    """Every failure, and how many files over the threshold were held to the layout.

    With `paths`, only those files are swept and stale exemptions are not judged. The
    policy is `root`'s own unless one is given.
    """
    policy = policy or _policy_of(root)
    swept = _json_files(root) if paths is None else list(paths)
    # A glob needs one file over the threshold to be live; past that, the files it
    # exempts -- the whole archive, mostly -- need not be read at all.
    witnessed: set[Exemption] = set()

    def unread(relative: str) -> bool:
        entry = policy.exemption(relative)
        return entry is not None and entry.is_glob and entry in witnessed

    failures: list[str] = []
    held = 0
    exempt_over: dict[str, Candidate] = {}
    for candidate in candidates(root, swept, policy.threshold_lines, unread=unread):
        entry = policy.exemption(candidate.relative)
        if entry is not None:
            exempt_over[candidate.relative] = candidate
            if entry.is_glob:
                witnessed.add(entry)
            continue
        held += 1
        text = candidate.data.decode("utf-8")
        try:
            laid = relayout(text)
        except ValueError as error:
            failures.append(f"{candidate.relative}: not JSON the layout can hold ({error})")
            continue
        if laid != text:
            failures.append(
                f"{candidate.relative}: not in the retained layout ({candidate.lines:,} lines; "
                f"laid out, {laid.count(chr(10)):,}); write it with "
                "sqpack.retained_json.dumps and re-lay it with "
                f"`python -m devtools.check_retained_json --fix {_from_packing(candidate)}`"
            )
    if paths is None:
        failures.extend(_stale(root, policy, exempt_over))
    return failures, held


def _policy_of(root: Path) -> Policy:
    return load_policy(root / POLICY.relative_to(REPO))


def _from_packing(candidate: Candidate) -> str:
    prefix = "packing/"
    relative = candidate.relative
    return relative[len(prefix) :] if relative.startswith(prefix) else f"../{relative}"


def _stale(root: Path, policy: Policy, exempt_over: dict[str, Candidate]) -> list[str]:
    """Every exemption that no longer exempts anything.

    Any entry is stale when it covers no file over the threshold. A pending conversion is
    stale too once its file is already in the layout; the other reasons name what holds a
    file's bytes, which a re-layout would break somewhere else first, so they are not
    re-laid here to ask.
    """
    failures: list[str] = []
    for entry in policy.exemptions:
        if entry.is_glob:
            if not any(entry.matches(relative) for relative in exempt_over):
                failures.append(
                    f"{entry.pattern}: the exemption ({entry.reason}) matches no tracked "
                    f"JSON over {policy.threshold_lines:,} lines; drop it"
                )
            continue
        candidate = exempt_over.get(entry.pattern)
        if candidate is None:
            path = root / entry.pattern
            state = "is gone" if not path.is_file() else "is not over the threshold"
            failures.append(
                f"{entry.pattern}: exempt ({entry.reason}) but {state}; drop the entry"
            )
            continue
        if entry.reason != "pending":
            continue
        text = candidate.data.decode("utf-8")
        try:
            in_layout = relayout(text) == text
        except ValueError:
            in_layout = False
        if in_layout:
            failures.append(
                f"{entry.pattern}: pending ({entry.bead}) but already in the retained "
                "layout; drop the entry"
            )
    return failures


def fix(paths: Sequence[Path], root: Path = REPO, *, policy: Policy | None = None) -> list[str]:
    """Re-lay each file in place, refusing any change to its value. Returns refusals."""
    policy = policy or _policy_of(root)
    refusals: list[str] = []
    for path in paths:
        relative = path.resolve().relative_to(root.resolve()).as_posix()
        entry = policy.exemption(relative)
        if entry is not None and entry.reason != "pending":
            refusals.append(
                f"{relative}: exempt ({entry.reason}: {entry.bound_by}); not re-laid"
            )
            continue
        text = path.read_text(encoding="utf-8")
        try:
            before = canonical(parse(text))
            laid = relayout(text)
            after = canonical(parse(laid))
        except ValueError as error:
            refusals.append(f"{relative}: {error}; not re-laid")
            continue
        if after != before:
            refusals.append(f"{relative}: the re-layout changes its value; not re-laid")
            continue
        if laid == text:
            print(f"{relative}: already in the retained layout")
            continue
        with atomic_output_file(path) as temporary:
            temporary.write_text(laid, encoding="utf-8")
        print(
            f"{relative}: {text.count(chr(10)):,} -> {laid.count(chr(10)):,} lines, "
            f"{len(text.encode()):,} -> {len(laid.encode()):,} bytes, longest line "
            f"{max(map(len, laid.split(chr(10)))):,}; value unchanged"
        )
    return refusals


def inventory(root: Path = REPO, *, policy: Policy | None = None) -> list[str]:
    """Every swept file over the threshold: its lines now, in the layout, and its status."""
    policy = policy or _policy_of(root)
    rows: list[str] = []
    for candidate in sorted(
        candidates(root, _json_files(root), policy.threshold_lines),
        key=lambda item: (-item.lines, item.relative),
    ):
        text = candidate.data.decode("utf-8")
        try:
            laid = relayout(text)
        except ValueError as error:
            rows.append(
                f"{candidate.lines:>9,}  {'?':>9}  unreadable ({error})  {candidate.relative}"
            )
            continue
        entry = policy.exemption(candidate.relative)
        if entry is not None:
            status = f"exempt: {entry.reason}"
        else:
            status = "in layout" if laid == text else "NOT IN LAYOUT"
        laid_lines = laid.count("\n")
        rows.append(
            f"{candidate.lines:>9,}  {laid_lines:>9,}  {status:<24}  {candidate.relative}"
        )
    return rows


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--fix", action="store_true", help="re-lay the named files in place")
    mode.add_argument(
        "--inventory", action="store_true", help="list every swept file over the threshold"
    )
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args(argv)
    if args.inventory:
        if args.paths:
            parser.error("--inventory sweeps the tracked tree and takes no paths")
        print(f"{'lines':>9}  {'laid out':>9}  {'status':<24}  path")
        for row in inventory():
            print(row)
        return 0
    if args.fix:
        if not args.paths:
            parser.error("--fix needs the files to re-lay")
        refusals = fix(args.paths)
        for line in refusals:
            print(line, file=sys.stderr)
        return 1 if refusals else 0
    failures, held = check(paths=args.paths or None)
    for line in failures:
        print(line)
    policy = load_policy()
    print(
        f"retained JSON layout: {held} file(s) over {policy.threshold_lines:,} lines held "
        f"to the layout, {len(policy.exemptions)} exemption(s), {len(failures)} failure(s)"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
