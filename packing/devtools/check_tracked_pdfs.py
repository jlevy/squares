"""Reject PDFs larger than 5 MiB in the Git index or a requested revision.

The index is the default because a working file may be smaller than the bytes already
staged. `--revision HEAD` audits the complete committed tree. Both modes enumerate all
paths, then select `.pdf` without case sensitivity: Git tree pathspecs do not expand a
shell-style `*.pdf` glob into nested directories. Only object metadata is read, never
PDF contents or history. Oversized originals belong in a release named by a manifest
under `packing/hosted/`; this check has no exemptions.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAX_PDF_BYTES = 5 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class Pdf:
    path: str
    size: int


def _git(repo: Path, *arguments: str, data: bytes | None = None) -> bytes:
    return subprocess.run(
        ("git", "-C", str(repo), *arguments),
        input=data,
        check=True,
        capture_output=True,
    ).stdout


def inventory(repo: Path = REPO, *, revision: str | None = None) -> tuple[Pdf, ...]:
    """Every indexed or committed PDF and its Git blob size, ordered by path."""
    if revision is not None:
        tree = _git(repo, "rev-parse", "--verify", "--end-of-options", f"{revision}^{{tree}}")
        listed = _git(
            repo, "ls-tree", "--full-tree", "-r", "-l", "-z", tree.decode("ascii").strip()
        )
        found = []
        for entry in listed.split(b"\0"):
            if not entry:
                continue
            fields, name = entry.split(b"\t", 1)
            _mode, kind, _object_id, size = fields.split()
            if kind == b"blob" and name.lower().endswith(b".pdf"):
                found.append(Pdf(os.fsdecode(name), int(size)))
        return tuple(sorted(found, key=lambda pdf: pdf.path))

    # `:/` enumerates the whole index even if --repo names a directory below its root.
    listed = _git(repo, "ls-files", "--cached", "--stage", "--full-name", "-z", "--", ":/")
    objects: dict[str, str] = {}
    for entry in listed.split(b"\0"):
        if not entry:
            continue
        fields, name = entry.split(b"\t", 1)
        mode, object_id, stage = fields.split()
        if mode == b"160000" or not name.lower().endswith(b".pdf"):
            continue
        path = os.fsdecode(name)
        if stage != b"0":
            raise ValueError(f"{path!r}: unresolved PDF merge; resolve it before checking")
        objects[path] = object_id.decode("ascii")
    if not objects:
        return ()
    ids = sorted(set(objects.values()))
    metadata = _git(
        repo,
        "cat-file",
        "--batch-check=%(objectname) %(objecttype) %(objectsize)",
        data=("\n".join(ids) + "\n").encode("ascii"),
    )
    sizes: dict[str, int] = {}
    for line in metadata.splitlines():
        fields = line.split()
        if len(fields) != 3 or fields[1] != b"blob":
            raise ValueError("the index names a PDF whose blob metadata is unavailable")
        sizes[fields[0].decode("ascii")] = int(fields[2])
    return tuple(Pdf(path, sizes[object_id]) for path, object_id in sorted(objects.items()))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--repo", type=Path, default=REPO, help="checkout directory")
    parser.add_argument(
        "--revision", help="audit this revision's complete tree instead of the index"
    )
    args = parser.parse_args(argv)
    try:
        pdfs = inventory(args.repo, revision=args.revision)
    except subprocess.CalledProcessError as error:
        detail = os.fsdecode(error.stderr or b"").strip()
        print(f"cannot inspect tracked PDFs: {detail}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as error:
        print(f"cannot inspect tracked PDFs: {error}", file=sys.stderr)
        return 1
    oversized = [pdf for pdf in pdfs if pdf.size > MAX_PDF_BYTES]
    for pdf in oversized:
        print(
            f"{pdf.path!r}: {pdf.size} bytes exceeds {MAX_PDF_BYTES} bytes (5 MiB); "
            "host the original through a packing/hosted/ manifest before staging it",
            file=sys.stderr,
        )
    where = "index" if args.revision is None else f"revision {args.revision}"
    print(
        f"{where}: {len(pdfs)} tracked PDFs, {sum(pdf.size for pdf in pdfs)} bytes; "
        f"{len(oversized)} exceed the 5 MiB cap"
    )
    return 1 if oversized else 0


if __name__ == "__main__":
    raise SystemExit(main())
