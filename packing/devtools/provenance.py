"""Which code wrote a receipt: recorded for the reader, never compared to refuse.

Git is the integrity boundary for the files this repository owns (OR-16), so a receipt
names its code by revision and path, not by a digest that something later checks.
`provenance` reads the named files when it is called, which for a module-level constant is
at import, so the record describes the bytes the process actually ran. For each file it
gives the repository-relative path and the Git blob id of those bytes (what `git
hash-object` would print), and for the set it gives the revision checked out and whether
any of the files differ from that revision. Without Git, or outside a checkout, the
revision and the dirty flag are None. Nothing in the repository reads these back to refuse
a receipt, a checkpoint or a resume: code that changed since a result was written is
information for the reader.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]


def git_blob(data: bytes) -> str:
    """Git's blob id of some bytes, computed without Git."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data, usedforsecurity=False).hexdigest()


def repository_path(path: Path) -> str:
    """The path relative to the repository when it lies inside it, as records name paths."""
    resolved = path.resolve()
    return resolved.relative_to(REPO).as_posix() if resolved.is_relative_to(REPO) else str(path)


def _git(*arguments: str) -> str | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(REPO), *arguments],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
    except OSError, subprocess.SubprocessError:
        return None
    return completed.stdout if completed.returncode == 0 else None


def provenance(*paths: Path) -> dict[str, Any]:
    """`{"revision", "dirty", "files"}` for the files as they are read now.

    `files` maps each file's repository-relative path (absolute when it lies outside the
    repository) to the Git blob id of its bytes. `dirty` is true when any of those blobs is
    not the one the revision holds at that path, an untracked file included.
    """
    files: dict[str, str] = {}
    for path in paths:
        resolved = path.resolve()
        name = (
            resolved.relative_to(REPO).as_posix()
            if resolved.is_relative_to(REPO)
            else str(resolved)
        )
        files[name] = git_blob(resolved.read_bytes())
    inside = [name for name in files if not Path(name).is_absolute()]
    head = _git("rev-parse", "HEAD")
    listed = None if head is None else _git("ls-tree", "HEAD", "--", *inside)
    committed: dict[str, str] = {}
    for line in (listed or "").splitlines():
        meta, _, name = line.partition("\t")
        committed[name] = meta.split()[2]
    return {
        "revision": None if head is None else head.strip(),
        "dirty": None
        if listed is None
        else any(committed.get(name) != blob for name, blob in files.items()),
        "files": files,
    }
