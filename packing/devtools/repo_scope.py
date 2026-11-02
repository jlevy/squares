"""Which files and trees in the checkout are this repository's to be answerable for.

Two sweeps ask that question of a tree and used to answer it separately.
`check_svg_rendering` named `vendor` in a frozenset; `check_documentation` did not sweep
vendored prose at all, and instead carried a `vendor/**/*.md` exclusion in the document
map. The map's loader requires every exclusion to match at least one file, so on a plain
`git clone` -- `vendor/kpress` present as an empty directory, no submodule checked out --
the docs check failed with `document exclusion is empty` (think-5e7k). Both workflows
pass `submodules: true`, which is the only reason CI never saw it.

Both are now `is_vendored` below, and the vendored set is read from `.gitmodules`
rather than typed, so a second submodule is excluded by being declared (think-f4vl).
A directory that is not checked out is still vendored: the answer comes from the
declaration, not from what happens to be on disk.

`tracked_files` asks it of a file, for a sweep that reads bytes: what this repository
holds is what git tracks, not what happens to be sitting in the working directory. A
sweep that walks the filesystem instead reads the reader's scratch -- one JSON dropped
into `attic/`, the directory `AGENTS.md` names for transient files and `.gitignore`
excludes, was enough to fail `check_class_record_claims` in a records-tier run, whose
step is reused across runs precisely because it was believed to be a function of the
tracked tree (PR 207).
"""

from __future__ import annotations

import os
import re
import subprocess
from collections.abc import Mapping, Sequence
from functools import cache
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[2]

#: `path = <value>` inside a `[submodule "..."]` stanza. The file is INI-shaped but not
#: `configparser`-shaped: git allows tabs, repeated sections and comment forms that
#: module rejects, and only one key here is wanted.
_SUBMODULE_PATH = re.compile(r"^\s*path\s*=\s*(.+?)\s*$", re.MULTILINE)


@cache
def vendored_directories(root: Path = REPO) -> frozenset[str]:
    """Every submodule path `root`'s `.gitmodules` declares, root-relative and POSIX.

    Read once per root and cached: the sweeps call it per candidate path, and the file
    does not change under a running check. `root` is this repository unless a caller
    asks the question of another checkout -- `check_readme` asks it of the `tmp_path`
    repository its tests build, since a declared submodule is a top-level entry the
    README must draw and `tracked_files` cannot report one.
    """
    gitmodules = root / ".gitmodules"
    if not gitmodules.is_file():
        return frozenset()
    declared = _SUBMODULE_PATH.findall(gitmodules.read_text(encoding="utf-8"))
    return frozenset(Path(path).as_posix() for path in declared)


def is_vendored(path: Path) -> bool:
    """Whether `path` is inside a declared submodule.

    Compared on path parts rather than on the string, so `vendor/kpress-notes` is not
    matched by a declared `vendor/kpress`.
    """
    parts = path.resolve().relative_to(REPO).parts
    prefixes = {"/".join(parts[:length]) for length in range(1, len(parts) + 1)}
    return bool(prefixes & vendored_directories())


def tracked_files(
    root: Path,
    pathspec: str,
    *,
    environment: Mapping[str, str] | None = None,
    untracked: bool = False,
) -> list[Path] | None:
    """Every file `root` tracks that matches the git `pathspec`, or `None` with no index here.

    `None` means "there is no index to ask here", not "nothing matched": `root` is not the
    top of its own work tree, or git is not runnable. The two are different answers and a
    caller that also runs outside a checkout -- a `tmp_path` fixture, a negative-control
    worker's source snapshot, which carries no `.git` -- has to be able to tell them apart
    before falling back to a walk. A tracked file that matches nothing returns `[]`.

    The toplevel is compared rather than assumed, so a directory sitting inside someone
    else's checkout answers `None` rather than listing that checkout's files as if they
    were its own.

    `-z` because with `core.quotePath` at its default a non-ASCII path arrives C-quoted,
    quotes included, and because it is the one separator no filename contains. Entries the
    index holds but the working tree no longer does -- a deletion that has not been staged
    -- are dropped, since a sweep over this list goes on to read bytes.

    Files inside a submodule are not listed: git reports the gitlink, and the submodule's
    own index is its own. That matches `is_vendored` above, which excludes them too.

    A caller constructing an isolated worker can supply its sanitized environment;
    both Git queries then use it without changing the process environment.

    `untracked` adds every file git does not ignore and does not yet track, which is what
    a tool that walks the working tree respecting `.gitignore` reads -- the Markdown
    formatter in the commit hook (review A1 of #882). A sweep that must be a function of
    the tracked tree leaves it off.
    """
    try:
        top = subprocess.run(
            ("git", "-C", str(root), "rev-parse", "--show-toplevel"),
            check=True,
            capture_output=True,
            env=environment,
        ).stdout
    except OSError, subprocess.CalledProcessError:
        return None
    if Path(os.fsdecode(top).strip()).resolve() != root.resolve():
        return None
    others = ("--others", "--exclude-standard") if untracked else ()
    listed = subprocess.run(
        ("git", "-C", str(root), "ls-files", "-z", "--cached", *others, "--", pathspec),
        check=True,
        capture_output=True,
        env=environment,
    ).stdout
    found = (root / os.fsdecode(name) for name in listed.split(b"\0") if name)
    return sorted(path for path in found if path.is_file())


#: What a walk skips when there is no git index to ask: never this repository's prose.
UNTRACKED_PARTS = frozenset({".git", ".venv", "node_modules", "__pycache__", "site"})


def tracked_markdown(repo: Path, *, untracked: bool = False) -> list[str]:
    """Every tracked Markdown file, repository-relative; a walk where there is no index.
    With `untracked`, every file git does not ignore as well (`tracked_files`)."""
    tracked = tracked_files(repo, "*.md", untracked=untracked)
    if tracked is None:
        tracked = [
            path
            for path in repo.rglob("*.md")
            if path.is_file() and not UNTRACKED_PARTS & set(path.relative_to(repo).parts)
        ]
    return sorted(path.relative_to(repo).as_posix() for path in tracked)


def flowmark_exclusions(repo: Path) -> list[str]:
    """The patterns `.flowmarkignore` lists: the Markdown the formatter never rewrites."""
    source = repo / ".flowmarkignore"
    if not source.is_file():
        return []
    lines = (line.strip() for line in source.read_text(encoding="utf-8").splitlines())
    return [line for line in lines if line and not line.startswith("#")]


@cache
def _exclusion(
    patterns: tuple[str, ...],
) -> tuple[tuple[str, ...], frozenset[str], tuple[str, ...]]:
    """`patterns` sorted once into directory prefixes, plain paths and globs: a plain path
    full-matches only itself, and `full_match` over every pattern for every file was most
    of a sweep's time."""
    prefixes = tuple(pattern for pattern in patterns if pattern.endswith("/"))
    files = [pattern for pattern in patterns if not pattern.endswith("/")]
    globs = tuple(pattern for pattern in files if set(pattern) & set("*?["))
    return prefixes, frozenset(files).difference(globs), globs


def excluded_by(path: str, patterns: Sequence[str]) -> bool:
    """Whether a pattern names `path`: a directory prefix, a file, or a glob."""
    prefixes, files, globs = _exclusion(tuple(patterns))
    return (
        path.startswith(prefixes)
        or path in files
        or any(PurePosixPath(path).full_match(pattern) for pattern in globs)
    )
