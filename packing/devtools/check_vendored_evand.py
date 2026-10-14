#!/usr/bin/env python3
"""Hold the vendored copy of Evan Daniel's regularizer to its manifest, and that to upstream.

`vendor/evand-regularize/` is a subset of evand/square-packing copied byte for byte at one
pinned commit: the exact solver and its two checkers under `search/exact/`, the
regularizer under `search/regularize/`, and the inputs and lists they read. It is the
generator behind the regularized drawing layer, and it decides nothing: every view it
produces is decided by this project's exact checkers. The directory's `README.md` says
what each file is for, how the credit is written and how the copy is forked or re-pinned;
`vendored.yaml` is the manifest this module reads.

**Two checks, and what each one holds.**

- *Offline* (the default, in the edit tier and on every pull request): the copy against
  `vendored.yaml`. It catches accidental edits only: a stray run output, a dropped file,
  an edit someone forgot to record. It cannot catch a deliberate one, because the
  expected values come from the manifest, which the same change can edit.
- *`--upstream`*: the manifest against upstream. It first fetches the commits of every
  branch and tag of `UPSTREAM_URL`, without trees or blobs, and requires one of them to
  hold the pin: GitHub serves any pull request's head by id through the base
  repository's URL, so a fetch by id alone would take a third party's unmerged commit
  for upstream's. It then fetches the pinned commit's trees, without blobs, into a
  temporary bare repository, and requires the commit's tree, date and subject to be the
  ones the manifest records, every pristine file's Git blob id to be upstream's at the
  pin (`git hash-object` against `git ls-tree`, so the identity is Git's own), every
  pinned mode to be upstream's, and every file here to be in upstream's tree unless it
  is a recorded addition. With the offline check passing, that makes every pinned
  SHA-256 the digest of upstream's bytes. It needs the network, so it is run by hand at
  a re-pin and by whoever reviews a change to the vendored directory; no gate runs it
  yet (`think-vwlm`), and no offline tier ever will.

**Why a digest here, against OR-16's default.** The rule reserves checksums for a real
trust boundary, and requires three answers beside one:

- *The boundary*: third-party code downloaded from another repository. Its bytes did not
  come from this project, and the point of vendoring it is that a reader can say exactly
  which upstream bytes ran.
- *The independently supplied expected value*: each file's SHA-256 as the upstream blob at
  the pinned commit, recorded at the re-pin and re-derived from the upstream repository,
  without trusting this one, by `--upstream`, at a commit one of upstream's own branches
  or tags holds.
- *The failure it detects*: an in-place edit of the vendored code that is not recorded as
  a reviewed local change (a silent fork, after which the credit and the pin would both
  misdescribe what ran), a vendored file dropped, an unrecorded file added beside them,
  or a re-pin that left the manifest describing the old bytes. Offline, only the
  accidental forms; with `--upstream`, the manifest's own values too.

Nothing else may refuse anything on these digests. No tool that runs the generator reads
them, and a mismatch here fails this check alone; it never blocks a regularization run or
invalidates a result, whose soundness rests on the exact checkers, not on the generator.

**What passes offline.** Every pinned file is present with its size, SHA-256 and
executable bit, unless the manifest's `local_changes` records it: `modified` (present, no
longer the pinned bytes, and for code a header comment naming
`vendor/evand-regularize/README.md`), `removed` (absent), `added` (a file upstream never
had, present), or `replica` (a patch applied only to a scratch replica of the copy, so the
file here stays the pinned bytes, and the patch, a unified diff at the repository-relative
`patch` path, still applies to them exactly). The README's Local Changes section names
each recorded change's path, and a replica patch's file name, so the prose account and
the manifest cannot drift apart; the section alone counts, since the
README's role table names every file. The licence file is never a local change: the MIT
grant requires its notice with every copy. Nothing else is in the directory besides its
`README.md` and `vendored.yaml`, the project's own two files. No path in it is a symbolic
link, and no module file in it takes the name of a standard-library module, of a
dependency the vendored scripts import (`DEPENDENCIES`), or of a module a dependency
looks up as it loads (`LOADED_BY_DEPENDENCIES`): five of them put `search/regularize/`
first on `sys.path`, so a `numpy.py` there would run in numpy's place, and mpmath tries
`gmpy2` at load, so a `gmpy2.py` beside `exactsolve.py` would run silently.
Whether a file is in upstream's tree at all is knowable only from upstream, so a file
declared in the manifest under any other name is `--upstream`'s to refuse. What the
directory holds is asked of git -- tracked files and untracked files git would commit, so
a stray run output is a finding before it is staged and a gitignored `__pycache__` is not
-- and walked from the filesystem only where there is no index to ask.

**Re-pinning** is `--write`: from a clean upstream checkout at the new pin, after the
vendored files have been replaced with the new pin's bytes, it compares every vendored
file with the checkout's blob at that commit, byte for byte and mode for mode, and
rewrites the manifest. `--commit` is the full 40-digit id. It refuses while local changes
are recorded, because a re-pin must start from the pristine copy (the README,
"Re-pinning"), and it refuses a checkout whose `origin` is not `UPSTREAM_URL` or a commit
none of upstream's branches or tags holds, which it fetches as `--upstream` does, so it
needs the network too. Run `--upstream` after it.

Usage, from `packing/`, each after `uv run --frozen --all-extras --group dev`:
    python -m devtools.check_vendored_evand
    python -m devtools.check_vendored_evand --upstream
    python -m devtools.check_vendored_evand --write \
        --checkout ../attic/evand-square-packing --commit <40-hex id>

It runs under the project interpreter (`except A, B:` parses on 3.14 only, `D-397`).
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import stat
import subprocess
import sys
import tempfile
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib.machinery import all_suffixes
from pathlib import Path
from typing import Any

from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]
VENDORED = REPO / "vendor" / "evand-regularize"
MANIFEST_NAME = "vendored.yaml"
#: The repository the copy is taken from. `--upstream` fetches only from here, so a
#: manifest that names another source is refused rather than compared with it.
UPSTREAM_URL = "https://github.com/evand/square-packing"
#: The provenance document: this project's, the directory's conventional readme.
DOCUMENT = "README.md"
#: This project's own files in the vendored directory. The manifest cannot list its own
#: digest, and the provenance document is ours to edit.
OWN_FILES = frozenset({DOCUMENT, MANIFEST_NAME})
#: What a patched or added script's header comment names, so a reader of the file finds
#: the record of the change.
HEADER_MARK = "vendor/evand-regularize/README.md"
FORMAT = "vendored-source-v1"
#: `replica` is a patch applied to a scratch replica only (`devtools.regularize_evand`), so
#: the vendored file stays the pinned bytes and the patch is checked to apply to them.
KINDS = ("modified", "added", "removed", "replica")
#: A patched or added file of these kinds carries a header comment pointing here.
COMMENTED_SUFFIXES = frozenset({".py", ".sh"})
HEADER_LINES = 20
#: The README heading under which each recorded local change is described. Only the text
#: from it to the next heading of any level names a change: the role table names them all.
LOCAL_CHANGES = "### Local Changes"
#: The third-party top-level modules the vendored scripts import, as the README's
#: Dependencies paragraph lists them; a test re-reads the vendored imports to keep it
#: whole. With the standard library and the two startup hooks, no vendored module file
#: may take one of these names.
DEPENDENCIES = frozenset({"matplotlib", "mpmath", "numpy", "scipy", "sympy", "yaml"})
#: The top-level modules the dependencies themselves look up while the vendored scripts
#: import them. Most are optional and a failed import falls back quietly, so a file of one
#: of these names on `sys.path` would run unseen: mpmath tries `gmpy2`, then `gmpy`, at
#: load. A test measures the set, once with every optional module the environment has and
#: once with all of them hidden, so each fallback is tried; it must stay inside this one.
#: Three groups are not measured and are named by hand: `sage`, which mpmath tries only
#: when `SAGE_ROOT` or `MPMATH_SAGE` is set; matplotlib's required packages by import
#: name, since matplotlib is not installed here; and CPython's own `_sysconfigdata_*`
#: modules, whose names carry the platform (`RESERVED_PREFIXES`).
LOADED_BY_DEPENDENCIES = frozenset(
    {
        "charset_normalizer",
        "cython",
        "flint",
        "gmpy",
        "gmpy2",
        "sage",
        "scikits",
        "sksparse",
        "uarray",
        # matplotlib's requirements, read from its metadata rather than measured.
        "PIL",
        "contourpy",
        "cycler",
        "dateutil",
        "fontTools",
        "kiwisolver",
        "packaging",
        "pyparsing",
    }
)
RESERVED_MODULES = (
    frozenset(sys.stdlib_module_names)
    | DEPENDENCIES
    | LOADED_BY_DEPENDENCIES
    | {"sitecustomize", "usercustomize"}
)
#: Reserved by prefix: CPython's build-configuration modules, named for the platform.
RESERVED_PREFIXES = ("_sysconfigdata_",)
#: Git's modes for a regular file and an executable one; the copy holds nothing else.
REGULAR = "100644"
EXECUTABLE = "100755"
_IMPORTABLE = tuple(all_suffixes())
_HEADING = re.compile(r"^ {0,3}#{1,6}(?:[ \t]|$)")
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_COMMIT = re.compile(r"^[0-9a-f]{40}$")
_HEX256 = re.compile(r"^[0-9a-f]{64}$")
_DAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_BEAD = re.compile(r"^think-[a-z0-9]{4}$")
_HUNK = re.compile(r"^@@ -\d+(?:,(\d+))? \+\d+(?:,(\d+))? @@")
#: Directories the fallback walk skips: interpreter caches, never content.
_SKIP = frozenset({"__pycache__", ".git"})

#: Written above the generated manifest, so `--write` reproduces the file it replaces.
HEADER = """\
# The manifest of vendor/evand-regularize: Evan Daniel's evand/square-packing, a subset
# copied byte for byte at one commit. README.md beside it is the prose: what each file
# is for, the credit, the licence, how a fork is recorded and how to re-pin.
#
# Checked by `python -m devtools.check_vendored_evand` from packing/ (edit tier), which
# also writes this file on a re-pin (`--write --checkout DIR --commit ID`); edit
# `local_changes` by hand, never the pinned digests or modes.
#
# Why SHA-256 here (OR-16): these bytes cross a real trust boundary -- they were
# downloaded from another party's repository. The expected value of each digest is the
# upstream blob at `source_commit`. The offline check holds the copy to this file, so it
# catches accidental edits only: an edit made here together with this file passes it.
# `--upstream` holds this file to upstream, at a commit one of upstream's branches or tags
# holds, comparing Git blob ids and modes at the pin. It needs the network, so it is run
# by hand at a re-pin and by whoever reviews a change to this directory; no gate runs it
# yet (think-vwlm). Nothing but these checks reads the digests: no tool refuses to run
# the generator, and no result is invalidated, on a mismatch.
"""


class ManifestError(ValueError):
    """The manifest is not in the shape this check reads."""


class PatchError(ValueError):
    """A replica patch that does not apply exactly."""


@dataclass(frozen=True, slots=True)
class Pinned:
    """One upstream file at the pin."""

    path: str
    size: int
    sha256: str
    executable: bool = False


@dataclass(frozen=True, slots=True)
class Change:
    """One reviewed local change to the vendored copy."""

    path: str
    kind: str
    day: str
    bead: str
    reason: str
    #: A `replica` change's unified diff, repository-relative; None for the other kinds.
    patch: str | None = None


@dataclass(frozen=True, slots=True)
class Manifest:
    source_url: str
    source_commit: str
    git_tree: str
    committed: str
    subject: str
    license_file: str
    files: dict[str, Pinned]
    changes: dict[str, Change]


# ---------------------------------------------------------------------------
# Reading the manifest
# ---------------------------------------------------------------------------


def _text(record: Mapping[str, Any], key: str, where: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        msg = f"{where}: `{key}` must be a non-empty string"
        raise ManifestError(msg)
    return value


def _relative(path: str, where: str) -> str:
    parts = path.split("/")
    if (
        path.startswith("/")
        or "\\" in path
        or any(part in {"", ".", ".."} for part in parts)
        or any(ord(character) < 0x20 for character in path)
    ):
        msg = f"{where}: `{path}` is not a plain relative POSIX path"
        raise ManifestError(msg)
    return path


def _pinned(entry: object, place: int) -> Pinned:
    where = f"files[{place}]"
    if not isinstance(entry, dict):
        msg = f"{where}: each file is a mapping"
        raise ManifestError(msg)
    record: dict[str, Any] = entry
    path = _relative(_text(record, "path", where), where)
    size = record.get("bytes")
    if not isinstance(size, int) or isinstance(size, bool) or size < 0:
        msg = f"{where} ({path}): `bytes` must be a non-negative integer"
        raise ManifestError(msg)
    sha256 = _text(record, "sha256", where)
    if not _HEX256.match(sha256):
        msg = f"{where} ({path}): `sha256` must be 64 lowercase hex digits"
        raise ManifestError(msg)
    executable = record.get("executable", False)
    if not isinstance(executable, bool):
        msg = f"{where} ({path}): `executable` is `true` or absent"
        raise ManifestError(msg)
    if path in OWN_FILES:
        msg = f"{where}: {path} is this project's own file, not an upstream one"
        raise ManifestError(msg)
    return Pinned(path, size, sha256, executable)


def _change(entry: object, place: int) -> Change:
    where = f"local_changes[{place}]"
    if not isinstance(entry, dict):
        msg = f"{where}: each local change is a mapping"
        raise ManifestError(msg)
    record: dict[str, Any] = entry
    path = _relative(_text(record, "path", where), where)
    kind = _text(record, "kind", where)
    if kind not in KINDS:
        msg = f"{where} ({path}): `kind` is one of {', '.join(KINDS)}, not {kind!r}"
        raise ManifestError(msg)
    day = str(record.get("date", ""))
    if not _DAY.match(day):
        msg = f"{where} ({path}): `date` must be YYYY-MM-DD"
        raise ManifestError(msg)
    bead = _text(record, "bead", where)
    if not _BEAD.match(bead):
        msg = f"{where} ({path}): `bead` must name the bead that tracks it (think-xxxx)"
        raise ManifestError(msg)
    patch = _relative(_text(record, "patch", where), where) if kind == "replica" else None
    return Change(path, kind, day, bead, _text(record, "reason", where), patch)


def parse_manifest(document: object) -> Manifest:
    """The manifest's fields, refused with a `ManifestError` naming what is wrong."""
    if not isinstance(document, dict):
        msg = "the manifest is a mapping"
        raise ManifestError(msg)
    record: dict[str, Any] = document
    if record.get("format") != FORMAT:
        msg = f"`format` must be {FORMAT!r}"
        raise ManifestError(msg)
    for key in ("source_url", "committed", "subject", "license", "copyright"):
        _text(record, key, "manifest")
    commit = _text(record, "source_commit", "manifest")
    if not _COMMIT.match(commit):
        msg = "`source_commit` must be the full 40-digit commit id"
        raise ManifestError(msg)
    tree = _text(record, "git_tree", "manifest")
    if not _COMMIT.match(tree):
        msg = "`git_tree` must be the full 40-digit tree id"
        raise ManifestError(msg)
    if not _DAY.match(str(record.get("retrieved", ""))):
        msg = "`retrieved` must be YYYY-MM-DD"
        raise ManifestError(msg)
    entries = record.get("files")
    if not isinstance(entries, list) or not entries:
        msg = "`files` must be a non-empty list"
        raise ManifestError(msg)
    files: dict[str, Pinned] = {}
    for place, entry in enumerate(entries):
        pinned = _pinned(entry, place)
        if pinned.path in files:
            msg = f"files[{place}]: {pinned.path} is listed twice"
            raise ManifestError(msg)
        files[pinned.path] = pinned
    recorded = record.get("local_changes")
    if not isinstance(recorded, list):
        msg = "`local_changes` must be a list, `[]` when the copy is pristine"
        raise ManifestError(msg)
    changes: dict[str, Change] = {}
    for place, entry in enumerate(recorded):
        change = _change(entry, place)
        if change.path in changes:
            msg = f"local_changes[{place}]: {change.path} is recorded twice"
            raise ManifestError(msg)
        changes[change.path] = change
    license_file = _text(record, "license_file", "manifest")
    if license_file not in files:
        msg = f"`license_file` {license_file} is not among the pinned files"
        raise ManifestError(msg)
    return Manifest(
        source_url=_text(record, "source_url", "manifest"),
        source_commit=commit,
        git_tree=tree,
        committed=_text(record, "committed", "manifest"),
        subject=_text(record, "subject", "manifest"),
        license_file=license_file,
        files=files,
        changes=changes,
    )


def load_manifest(path: Path) -> Manifest:
    return parse_manifest(safe_load(path.read_text(encoding="utf-8")))


# ---------------------------------------------------------------------------
# What the directory holds
# ---------------------------------------------------------------------------


def _git_listed(directory: Path) -> set[str] | None:
    """Tracked and untracked-but-unignored files under `directory`, or None with no index.

    Asked from the work tree's top so that a directory git ignores as a whole answers
    `None` (no index speaks for it) rather than an empty listing that would read as every
    file missing. A symbolic link is listed whatever it points at, so the check can
    refuse it.
    """
    try:
        top = subprocess.run(
            ("git", "-C", str(directory), "rev-parse", "--show-toplevel"),
            check=True,
            capture_output=True,
        ).stdout
    except OSError, subprocess.CalledProcessError:
        return None
    root = Path(os.fsdecode(top).strip()).resolve()
    inside = directory.resolve().relative_to(root).as_posix()
    ignored = subprocess.run(
        ("git", "-C", str(root), "check-ignore", "-q", "--", inside),
        capture_output=True,
        check=False,
    )
    if inside != "." and ignored.returncode == 0:
        return None
    listed = subprocess.run(
        (
            "git",
            "-C",
            str(root),
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            inside,
        ),
        check=True,
        capture_output=True,
    ).stdout
    prefix = "" if inside == "." else inside + "/"
    names = (os.fsdecode(name) for name in listed.split(b"\0") if name)
    return {
        name.removeprefix(prefix)
        for name in names
        if (root / name).is_file() or (root / name).is_symlink()
    }


def _walked(directory: Path) -> set[str]:
    found: set[str] = set()
    for here, names, files in os.walk(directory):
        # A linked directory is not descended into; it is a finding in its own right.
        found.update(
            (Path(here) / name).relative_to(directory).as_posix()
            for name in names
            if (Path(here) / name).is_symlink()
        )
        names[:] = [name for name in names if name not in _SKIP]
        found.update(
            (Path(here) / name).relative_to(directory).as_posix()
            for name in files
            if not name.endswith(".pyc")
        )
    return found


def present_files(directory: Path) -> set[str]:
    """Every file `directory` holds, relative to it: git's answer, else a walk."""
    listed = _git_listed(directory)
    return _walked(directory) if listed is None else listed


# ---------------------------------------------------------------------------
# Replica patches
# ---------------------------------------------------------------------------


def _hunks(diff: str) -> list[tuple[str, str]]:
    """Each hunk of a unified diff as its text before and after; lines outside hunks are
    the diff's own prose and headers. A hunk is read by the line counts its header gives."""
    lines = diff.splitlines(keepends=True)
    hunks: list[tuple[str, str]] = []
    place = 0
    while place < len(lines):
        header = _HUNK.match(lines[place])
        place += 1
        if header is None:
            continue
        old, new = int(header.group(1) or 1), int(header.group(2) or 1)
        before: list[str] = []
        after: list[str] = []
        while len(before) < old or len(after) < new:
            if place == len(lines):
                msg = "a hunk ends before the line counts its header gives"
                raise PatchError(msg)
            line = lines[place]
            place += 1
            # An empty context line may have lost its leading space to an editor.
            tag, body = (" ", line) if line in {"\n", "\r\n"} else (line[:1], line[1:])
            if tag in {" ", "-"}:
                before.append(body)
            if tag in {" ", "+"}:
                after.append(body)
            if tag not in {" ", "-", "+", "\\"}:
                msg = f"a line in a hunk starts with neither ' ', '-' nor '+': {line!r}"
                raise PatchError(msg)
        hunks.append(("".join(before), "".join(after)))
    if not hunks:
        msg = "the patch has no hunk"
        raise PatchError(msg)
    return hunks


def apply_patch(text: str, diff: str) -> str:
    """`text` with each hunk of the unified `diff` applied by its exact text before.

    Line numbers are not trusted and nothing is fuzzed: each hunk's context and removed
    lines must occur exactly once in the text as the hunks before it left it, as whole
    lines and counting occurrences that overlap, so a patch that no longer fits the bytes
    it was written against, or could land in two places, is refused, never half applied.
    """
    for before, after in _hunks(diff):
        lines, block = _lines(text), _lines(before)
        width = len(block)
        found = [
            start
            for start in range(len(lines) - width + 1)
            if width and lines[start : start + width] == block
        ]
        if len(found) != 1:
            where = "is not in the text" if not found else f"occurs {len(found)} times"
            first = block[0] if block else ""
            msg = f"the hunk beginning {first.strip()!r} {where}"
            raise PatchError(msg)
        start = found[0]
        text = "".join([*lines[:start], after, *lines[start + width :]])
    return text


def _lines(text: str) -> list[str]:
    """`text` as its lines, each with its newline: only a newline ends a line, as in a diff."""
    return [line for line in re.split(r"(?<=\n)", text) if line]


def project_root(directory: Path) -> Path:
    """The repository that holds a vendored directory at `vendor/<name>`."""
    return directory.resolve().parents[1]


def _replica_problems(directory: Path, path: str, change: Change) -> list[str]:
    """A replica patch's file is there and still applies to the vendored file."""
    if change.patch is None:  # parse_manifest gives every replica change its patch
        return [f"{path}: a replica change names no patch"]
    patch = project_root(directory) / change.patch
    if not patch.is_file():
        return [f"{path}: its replica patch {change.patch} is missing"]
    try:
        apply_patch(
            (directory / path).read_text(encoding="utf-8"), patch.read_text(encoding="utf-8")
        )
    except PatchError as refusal:
        return [f"{path}: its replica patch {change.patch} does not apply: {refusal}"]
    return []


# ---------------------------------------------------------------------------
# The check
# ---------------------------------------------------------------------------


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _mode(path: Path) -> str:
    """Git's mode for a regular file: executable when its owner may execute it."""
    return EXECUTABLE if path.stat().st_mode & stat.S_IXUSR else REGULAR


def _pinned_mode(pinned: Pinned) -> str:
    return EXECUTABLE if pinned.executable else REGULAR


def _names_vendored(path: Path) -> bool:
    with path.open(encoding="utf-8", errors="replace") as stream:
        head = [stream.readline() for _ in range(HEADER_LINES)]
    return any(HEADER_MARK in line for line in head)


def local_changes_text(prose: str) -> str:
    """The README text under `LOCAL_CHANGES`, up to the next heading of any level.

    Empty when the heading is absent. A `#` line inside a fenced code block is code, not a
    heading, so it does not end the section.
    """
    section: list[str] | None = None
    fence = ""
    for line in prose.splitlines():
        opened = _FENCE.match(line)
        if fence:
            marker = opened.group(1) if opened else ""
            if marker[:1] == fence[0] and len(marker) >= len(fence):
                fence = ""
        elif opened:
            fence = opened.group(1)
        elif _HEADING.match(line):
            if section is not None:
                break
            if line.strip() == LOCAL_CHANGES:
                section = []
            continue
        if section is not None:
            section.append(line)
    return "\n".join(section or ())


def link_in(directory: Path, path: str) -> str | None:
    """The first component of `path` under `directory` that is a symbolic link, if any."""
    parts = path.split("/")
    for end in range(1, len(parts) + 1):
        prefix = "/".join(parts[:end])
        if (directory / prefix).is_symlink():
            return prefix
    return None


def shadowed_module(path: str) -> str | None:
    """The reserved module `path` would be imported as from its directory, if any.

    A module file binds the name before its first dot; an `__init__` file binds its
    directory's name. Either shadows the real module once the directory is on `sys.path`.
    """
    parts = path.split("/")
    if not parts[-1].endswith(_IMPORTABLE):
        return None
    name = parts[-1].split(".", 1)[0]
    if name == "__init__":
        name = parts[-2] if len(parts) > 1 else ""
    reserved = name in RESERVED_MODULES or name.startswith(RESERVED_PREFIXES)
    return name if reserved else None


def _pinned_problems(
    directory: Path, manifest: Manifest, present: set[str], linked: set[str]
) -> list[str]:
    problems: list[str] = []
    for path, pinned in sorted(manifest.files.items()):
        change = manifest.changes.get(path)
        where = directory / path
        if change is not None and change.kind == "added":
            problems.append(f"{path}: recorded as added, but upstream has it at the pin")
        elif change is not None and change.kind == "removed":
            if path in present:
                problems.append(f"{path}: recorded as removed, but it is still here")
        elif path in linked:
            continue  # refused as a link; its bytes are not this copy's to compare
        elif path not in present:
            problems.append(f"{path}: pinned, but missing from the vendored copy")
        else:
            if change is not None and change.kind == "replica":
                # A replica patch changes only the scratch replica: the file here is pristine.
                problems += _replica_problems(directory, path, change)
                change = None
            mode = _mode(where)
            if mode != _pinned_mode(pinned):
                problems.append(
                    f"{path}: mode {mode}, not the pinned {_pinned_mode(pinned)}; the copy "
                    "keeps upstream's modes"
                )
            problems += _content_problems(where, path, pinned, change)
    return problems


def _content_problems(
    where: Path, path: str, pinned: Pinned, change: Change | None
) -> list[str]:
    if change is None:
        size = where.stat().st_size
        if size != pinned.size:
            return [
                (
                    f"{path}: {size} bytes, not the pinned {pinned.size}; an edit to "
                    "vendored code is a local change, recorded in vendored.yaml "
                    "(README.md, Forking)"
                )
            ]
        if _sha256(where) != pinned.sha256:
            return [
                (
                    f"{path}: not the pinned bytes; an edit to vendored code is a local "
                    "change, recorded in vendored.yaml (README.md, Forking)"
                )
            ]
        return []
    if _sha256(where) == pinned.sha256:
        return [f"{path}: recorded as modified, but it is still the pinned bytes"]
    if where.suffix in COMMENTED_SUFFIXES and not _names_vendored(where):
        return [
            (
                f"{path}: modified, but its first {HEADER_LINES} lines carry no comment "
                f"naming {HEADER_MARK}"
            )
        ]
    return []


def check(directory: Path, manifest: Manifest, present: Iterable[str]) -> list[str]:
    """Every way the vendored copy at `directory` disagrees with `manifest`."""
    held = set(present)
    links = {
        found
        for found in (link_in(directory, path) for path in held | set(manifest.files))
        if found is not None
    }
    linked = {
        path
        for path in held | set(manifest.files)
        if any(path == link or path.startswith(link + "/") for link in links)
    }
    problems = [
        f"{name}: this project's file is missing from the vendored directory"
        for name in sorted(OWN_FILES - held)
    ]
    problems += [
        f"{link}: a symbolic link; the vendored copy holds regular files only"
        for link in sorted(links)
    ]
    if manifest.license_file in manifest.changes:
        problems.append(
            f"{manifest.license_file}: the licence file is never a local change; the MIT "
            "grant requires its notice with every copy"
        )
    problems += _pinned_problems(directory, manifest, held, linked)
    for path, change in sorted(manifest.changes.items()):
        if path in manifest.files:
            continue
        if change.kind != "added":
            problems.append(f"{path}: recorded as {change.kind}, but upstream has no such file")
        elif path not in held:
            problems.append(f"{path}: recorded as added, but it is not here")
        elif (
            path not in linked
            and (directory / path).suffix in COMMENTED_SUFFIXES
            and not _names_vendored(directory / path)
        ):
            problems.append(
                f"{path}: added, but its first {HEADER_LINES} lines carry no comment "
                f"naming {HEADER_MARK}"
            )
    problems += [
        f"{path}: would be imported in place of the `{module}` module the vendored scripts "
        "or their dependencies load, since the scripts put its directory on sys.path"
        for path, module in sorted((path, shadowed_module(path)) for path in held - OWN_FILES)
        if module is not None
    ]
    document = directory / DOCUMENT
    prose = document.read_text(encoding="utf-8") if document.is_file() else ""
    described = local_changes_text(prose)
    problems += [
        f"{path}: recorded as a local change, but README.md's Local Changes does not name it"
        for path in sorted(manifest.changes)
        if path not in described
    ]
    problems += [
        f"{path}: its replica patch {Path(change.patch).name} is not named in README.md's "
        "Local Changes"
        for path, change in sorted(manifest.changes.items())
        if change.patch is not None and Path(change.patch).name not in described
    ]
    expected = set(manifest.files) | set(manifest.changes) | OWN_FILES | linked
    problems += [
        f"{path}: not in the manifest; vendored code changes only by a recorded local "
        "change, and run outputs belong in a scratch directory, not here"
        for path in sorted(held - expected)
    ]
    return problems


def source_problems(manifest: Manifest) -> list[str]:
    """The manifest names the upstream this tool fetches from, or it is refused."""
    if manifest.source_url == UPSTREAM_URL:
        return []
    return [
        (
            f"vendored.yaml: `source_url` is {manifest.source_url}, not {UPSTREAM_URL}; "
            "a new upstream is a change to this tool, reviewed as such"
        )
    ]


# ---------------------------------------------------------------------------
# Upstream: the manifest against the pinned commit
# ---------------------------------------------------------------------------


#: Variables that would aim git at another repository than the one `-C` names.
_GIT_LOCATORS = frozenset(
    {
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_COMMON_DIR",
        "GIT_DIR",
        "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_WORK_TREE",
    }
)


def _git(repository: Path, *arguments: str, stdin: bytes | None = None) -> bytes:
    """Git in `repository` (a work tree, or a bare repository), with no hooks to run."""
    environment = {key: value for key, value in os.environ.items() if key not in _GIT_LOCATORS}
    return subprocess.run(
        ("git", "-C", str(repository), "-c", "core.hooksPath=/dev/null", *arguments),
        check=True,
        capture_output=True,
        input=stdin,
        env={**environment, "GIT_TERMINAL_PROMPT": "0"},
    ).stdout


def tree_entries(repository: Path, commit: str) -> dict[str, tuple[str, str]]:
    """Every file in `commit`'s tree, as path -> (mode, object id); reads trees only."""
    listed = _git(repository, "ls-tree", "-r", "-z", "--full-tree", "--end-of-options", commit)
    entries: dict[str, tuple[str, str]] = {}
    for record in listed.split(b"\0"):
        if record:
            head, _, name = record.partition(b"\t")
            mode, _, oid = head.decode().split(" ")
            entries[os.fsdecode(name)] = (mode, oid)
    return entries


def _commit_fields(repository: Path, commit: str) -> list[str]:
    """`commit`'s id, tree, committer date and subject, or a refusal."""
    try:
        answer = _git(
            repository, "log", "-1", "--format=%H%n%T%n%cI%n%s", "--end-of-options", commit
        )
    except subprocess.CalledProcessError as failure:
        detail = os.fsdecode(failure.stderr).strip()
        msg = f"{commit} is not a commit in {repository}: {detail}"
        raise ManifestError(msg) from failure
    fields = answer.decode().split("\n")
    if len(fields) < 4 or fields[0] != commit:
        msg = f"git answered {answer.decode()!r} for commit {commit}, not its four fields"
        raise ManifestError(msg)
    return fields[:4]


#: Every branch and tag of upstream, as the temporary repository holds them. A pull
#: request's head (`refs/pull/N/head`) is neither, and is never fetched.
UPSTREAM_REFS = ("+refs/heads/*:refs/remotes/origin/*", "+refs/tags/*:refs/tags/*")


def fetch_refs(url: str, into: Path) -> Path:
    """A bare repository at `into` holding the commits of every branch and tag of `url`.

    `--filter=tree:0` leaves out every tree and blob, so this is the history alone: about
    1 s and 520 KB for upstream on 2026-10-13. Nothing is checked out and no hook runs.
    """
    _git(into.parent, "init", "-q", "--bare", "--", str(into))
    _git(into, "remote", "add", "--", "origin", url)
    _git(
        into,
        "fetch",
        "-q",
        "--filter=tree:0",
        "--no-tags",
        "--end-of-options",
        "origin",
        *UPSTREAM_REFS,
    )
    return into


def _ref_name(ref: str) -> str:
    if ref.startswith("refs/tags/"):
        return f"tag {ref.removeprefix('refs/tags/')}"
    return f"branch {ref.removeprefix('refs/remotes/origin/')}"


def containing_refs(repository: Path, commit: str) -> list[str]:
    """The branches and tags in `repository` whose history holds `commit`, by short name.

    Membership is read from the history the refs reach, never by looking `commit` up: in
    a partial clone a missing object is fetched on demand, and GitHub would serve a pull
    request's head that way as readily as a branch's.
    """
    if commit not in set(_git(repository, "rev-list", "--all").decode().split()):
        return []
    listed = _git(
        repository,
        "for-each-ref",
        f"--contains={commit}",
        "--format=%(refname)",
        "refs/remotes/origin",
        "refs/tags",
    )
    return [_ref_name(ref) for ref in listed.decode().split()]


def upstream_refs(commit: str) -> list[str]:
    """The branches and tags of `UPSTREAM_URL` whose history holds `commit`.

    Fetched into a temporary directory, removed afterwards; it needs the network.
    """
    with tempfile.TemporaryDirectory(prefix="evand-upstream-") as scratch:
        return containing_refs(fetch_refs(UPSTREAM_URL, Path(scratch) / "refs.git"), commit)


def _held_by(refs: Sequence[str]) -> str:
    """`refs` for a message: up to three by name, then how many more."""
    shown = [*refs[:3], f"{len(refs) - 3} more"] if len(refs) > 3 else list(refs)
    return shown[0] if len(shown) == 1 else f"{', '.join(shown[:-1])} and {shown[-1]}"


def _on_no_ref(commit: str) -> str:
    return (
        f"{commit[:12]} is on no branch or tag of {UPSTREAM_URL}, so it is not upstream's "
        "commit, though GitHub serves it by id (a pull request's or a fork's head is served "
        "that way); pin a commit one of upstream's branches or tags holds"
    )


def fetch_pin(url: str, commit: str, into: Path) -> Path:
    """A bare repository at `into` holding `commit` and its trees, fetched without blobs.

    A blob is fetched on demand only if one is read, which `compare_upstream` does just
    for a recorded local change. Nothing is checked out and no hook runs.
    """
    _git(into.parent, "init", "-q", "--bare", "--", str(into))
    _git(into, "remote", "add", "--", "origin", url)
    _git(
        into,
        "fetch",
        "-q",
        "--filter=blob:none",
        "--depth=1",
        "--no-tags",
        "--end-of-options",
        "origin",
        commit,
    )
    return into


def compare_upstream(
    directory: Path, manifest: Manifest, present: Iterable[str], repository: Path
) -> list[str]:
    """Every way `manifest` disagrees with its commit, held in the bare `repository`.

    The commit's tree, date and subject are the manifest's; each pinned path is a regular
    file in that tree with the pinned mode; each pristine file here is upstream's blob, by
    Git's own blob id; a recorded modification or removal keeps a pinned size and SHA-256
    that are the upstream blob's; and every other file here is in the tree unless it is a
    recorded addition, which must not be.
    """
    held = set(present)
    commit = manifest.source_commit
    short = commit[:7]
    _, tree, committed, subject = _commit_fields(repository, commit)
    problems = [
        f"vendored.yaml: `{key}` is {recorded!r}, but {short}'s is {actual!r}"
        for key, recorded, actual in (
            ("git_tree", manifest.git_tree, tree),
            ("committed", manifest.committed, committed),
            ("subject", manifest.subject, subject),
        )
        if recorded != actual
    ]
    entries = tree_entries(repository, commit)
    pristine: list[tuple[str, str]] = []
    for path, pinned in sorted(manifest.files.items()):
        entry = entries.get(path)
        if entry is None:
            problems.append(f"{path}: pinned, but upstream's tree at {short} has no such file")
            continue
        mode, oid = entry
        if mode not in {REGULAR, EXECUTABLE}:
            problems.append(f"{path}: upstream holds mode {mode} there, not a regular file")
            continue
        if mode != _pinned_mode(pinned):
            problems.append(
                f"{path}: vendored.yaml pins mode {_pinned_mode(pinned)}, upstream's is {mode}"
            )
        change = manifest.changes.get(path)
        if change is None or change.kind == "replica":
            # A replica patch leaves the file here pristine, so it is held to upstream's blob.
            if path in held and link_in(directory, path) is None:
                pristine.append((path, oid))
        elif change.kind != "added":
            blob = _git(repository, "cat-file", "blob", oid)
            if len(blob) != pinned.size or hashlib.sha256(blob).hexdigest() != pinned.sha256:
                problems.append(
                    f"{path}: the pinned size and SHA-256 are not upstream's blob at {short}"
                )
    if pristine:
        named = "".join(f"{directory / path}\n" for path, _ in pristine)
        ids = _git(
            repository, "hash-object", "--no-filters", "--stdin-paths", stdin=named.encode()
        )
        problems += [
            f"{path}: Git blob {blob}, not upstream's {oid} at {short}"
            for (path, oid), blob in zip(pristine, ids.decode().split(), strict=True)
            if blob != oid
        ]
    for path in sorted(held - OWN_FILES - set(manifest.files)):
        change = manifest.changes.get(path)
        if change is not None and change.kind == "added":
            if path in entries:
                problems.append(f"{path}: recorded as added, but upstream has it at {short}")
        elif path not in entries:
            problems.append(f"{path}: not in upstream's tree at {short}")
    return problems


# ---------------------------------------------------------------------------
# Re-pinning
# ---------------------------------------------------------------------------


def _quoted(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def render_manifest(
    *, metadata: Mapping[str, str], files: Sequence[Pinned], retrieved: str
) -> str:
    """The manifest's text: `HEADER`, the pin, and one flow mapping per file."""
    lines = [
        HEADER.rstrip("\n"),
        "",
        f"format: {FORMAT}",
        f"source_url: {metadata['source_url']}",
        f"source_commit: {metadata['source_commit']}",
        f"git_tree: {metadata['git_tree']}",
        f"committed: {_quoted(metadata['committed'])}",
        f"subject: {_quoted(metadata['subject'])}",
        f"retrieved: {_quoted(retrieved)}",
        "license: MIT",
        "license_file: LICENSE",
        f"copyright: {_quoted(metadata['copyright'])}",
        "",
        "# Reviewed patches to the vendored copy, each {path, kind: modified | added |",
        "# removed | replica, date, bead, reason}, and a replica patch's `patch` file. A",
        "# modified file keeps its pinned entry below, so the pristine bytes stay",
        "# reconstructible from the upstream pin; a replica patch leaves them as they are.",
        "local_changes: []",
        "",
        f"# {len(files)} files, {sum(item.size for item in files)} bytes.",
        "files:",
    ]
    lines.extend(
        f"  - {{path: {item.path}, bytes: {item.size}, sha256: {item.sha256}"
        + (", executable: true}" if item.executable else "}")
        for item in files
    )
    return "\n".join(lines) + "\n"


def repin(directory: Path, checkout: Path, *, commit: str, retrieved: str) -> str:
    """The manifest for `directory` as a copy of `checkout` at `commit`, or a refusal.

    Each vendored file is compared byte for byte with the checkout's blob at the commit,
    read from the checkout's object store, so a modified working tree there is harmless,
    and its mode with the tree's. `commit` is a full commit id, never a name git could
    read as an option.
    """
    if not _COMMIT.match(commit):
        msg = f"--commit must be the full 40-digit commit id, not {commit!r}"
        raise ManifestError(msg)
    if not _DAY.match(retrieved):
        msg = f"--retrieved must be YYYY-MM-DD, not {retrieved!r}"
        raise ManifestError(msg)
    manifest_path = directory / MANIFEST_NAME
    if manifest_path.is_file() and load_manifest(manifest_path).changes:
        msg = (
            "local changes are recorded; restore the pristine copy, re-pin, then re-apply "
            "each change and record it again (README.md, Re-pinning)"
        )
        raise ManifestError(msg)
    fields = _commit_fields(checkout, commit)
    url = _git(checkout, "remote", "get-url", "origin").decode().strip().removesuffix(".git")
    if url != UPSTREAM_URL:
        msg = (
            f"the checkout's origin is {url}, not {UPSTREAM_URL}; a re-pin is taken from "
            "upstream, and a new upstream is a change to this tool, reviewed as such"
        )
        raise ManifestError(msg)
    try:
        held = upstream_refs(commit)
    except subprocess.CalledProcessError as failure:
        detail = os.fsdecode(failure.stderr).strip()
        msg = f"could not read upstream's branches and tags from {UPSTREAM_URL}: {detail}"
        raise ManifestError(msg) from failure
    if not held:
        raise ManifestError(_on_no_ref(commit))
    licence = (directory / "LICENSE").read_text(encoding="utf-8")
    holder = next(line for line in licence.splitlines() if line.startswith("Copyright"))
    metadata = {
        "source_url": url,
        "source_commit": fields[0],
        "git_tree": fields[1],
        "committed": fields[2],
        "subject": fields[3],
        "copyright": holder,
    }
    entries = tree_entries(checkout, commit)
    pinned: list[Pinned] = []
    mismatched: list[str] = []
    for path in sorted(present_files(directory) - OWN_FILES):
        if link_in(directory, path) is not None:
            mismatched.append(f"{path}: a symbolic link; the vendored copy holds files only")
            continue
        entry = entries.get(path)
        if entry is None:
            mismatched.append(f"{path}: upstream has no such file at {commit[:12]}")
            continue
        mode, oid = entry
        if mode not in {REGULAR, EXECUTABLE}:
            mismatched.append(f"{path}: upstream holds mode {mode} there, not a file")
            continue
        data = (directory / path).read_bytes()
        if _git(checkout, "cat-file", "blob", oid) != data:
            mismatched.append(f"{path}: not upstream's bytes at {commit[:12]}")
            continue
        if _mode(directory / path) != mode:
            mismatched.append(f"{path}: not upstream's mode {mode} at {commit[:12]}")
            continue
        pinned.append(
            Pinned(path, len(data), hashlib.sha256(data).hexdigest(), mode == EXECUTABLE)
        )
    if mismatched:
        raise ManifestError("; ".join(mismatched))
    return render_manifest(metadata=metadata, files=pinned, retrieved=retrieved)


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------


def upstream_problems(
    directory: Path, manifest: Manifest, present: set[str]
) -> tuple[list[str], list[str]]:
    """Every way `manifest` disagrees with upstream, and the upstream refs holding the pin.

    The pin must be on one of upstream's branches or tags (`upstream_refs`) before it is
    fetched and held to the manifest (`compare_upstream`), each in a temporary directory.
    """
    if source_problems(manifest):
        return [], []  # never fetched from a source this tool was not written for
    commit = manifest.source_commit
    pin = f"{UPSTREAM_URL}@{commit[:7]}"
    try:
        held = upstream_refs(commit)
        if not held:
            return [f"vendored.yaml: `source_commit` {_on_no_ref(commit)}"], []
        with tempfile.TemporaryDirectory(prefix="evand-upstream-") as scratch:
            repository = fetch_pin(UPSTREAM_URL, commit, Path(scratch) / "pin.git")
            return compare_upstream(directory, manifest, present, repository), held
    except subprocess.CalledProcessError as failure:
        detail = os.fsdecode(failure.stderr).strip()
        return [f"could not read {pin} from upstream: {detail}"], []
    except ManifestError as refusal:
        return [str(refusal)], []


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    parser.add_argument("--directory", type=Path, default=VENDORED)
    parser.add_argument(
        "--upstream",
        action="store_true",
        help="also hold the manifest to upstream at the pin (fetches; needs the network)",
    )
    parser.add_argument(
        "--write", action="store_true", help="rewrite the manifest from an upstream checkout"
    )
    parser.add_argument("--checkout", type=Path, help="upstream checkout, for --write")
    parser.add_argument("--commit", help="the pin's full 40-digit commit id, for --write")
    parser.add_argument(
        "--retrieved",
        default=datetime.now(tz=UTC).date().isoformat(),
        help="retrieval date, for --write",
    )
    args = parser.parse_args(argv)
    directory: Path = args.directory
    try:
        if args.write:
            if args.checkout is None or args.commit is None:
                parser.error("--write needs --checkout and --commit")
            text = repin(directory, args.checkout, commit=args.commit, retrieved=args.retrieved)
            (directory / MANIFEST_NAME).write_text(text, encoding="utf-8")
            written = load_manifest(directory / MANIFEST_NAME)
            print(
                f"wrote {MANIFEST_NAME}: {len(written.files)} files at "
                f"{written.source_commit}, which one of upstream's branches or tags holds; "
                "run --upstream to hold it to upstream"
            )
            return 0
        manifest = load_manifest(directory / MANIFEST_NAME)
    except ManifestError as refusal:
        print(f"check_vendored_evand: {refusal}", file=sys.stderr)
        return 1
    present = present_files(directory)
    problems = source_problems(manifest) + check(directory, manifest, present)
    refs: list[str] = []
    if args.upstream:
        found, refs = upstream_problems(directory, manifest, present)
        problems += found
    for problem in problems:
        print(f"check_vendored_evand: {problem}", file=sys.stderr)
    if problems:
        return 1
    held = (
        f"and vendored.yaml matches upstream at that commit, on upstream's "
        f"{_held_by(refs)}, by tree, Git blob ids and modes"
        if args.upstream
        else "not compared with upstream (--upstream does that)"
    )
    print(
        f"vendored copy check passed: {len(manifest.files)} files match vendored.yaml "
        f"(pinned at {manifest.source_url}@{manifest.source_commit[:7]}, "
        f"{len(manifest.changes)} local change(s) recorded), {held}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
