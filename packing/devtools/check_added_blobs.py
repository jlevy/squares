"""Refuse bulk Git blobs before commit and on a pull request's actual base/head.

Git object IDs identify storage being measured here; they never identify scientific
inputs or decide research verdicts. Existing unchanged base history is grandfathered.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

MAX_BLOB_BYTES = 5 * 1024**2
MAX_TOTAL_BYTES = 20 * 1024**2
MAX_METADATA_BYTES = 4 * 1024**2
MAX_SECONDS = 30
OBJECT_ID = re.compile(rb"[0-9a-f]{40}(?:[0-9a-f]{24})?")


class MetadataError(ValueError):
    """Incomplete Git metadata cannot certify the branch."""


@dataclass(frozen=True)
class Change:
    before: bytes
    after: bytes
    status: bytes
    path: str
    mode: bytes


@dataclass(frozen=True)
class Blob:
    object_id: str
    size: int
    paths: tuple[str, ...]


def _git(repo: Path, *arguments: str, deadline: float, data: bytes | None = None) -> bytes:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise MetadataError("Git metadata protocol exceeded 30 seconds")
    environment = dict(os.environ)
    environment.update(
        GIT_NO_LAZY_FETCH="1", GIT_NO_REPLACE_OBJECTS="1", GIT_TERMINAL_PROMPT="0"
    )
    try:
        result = subprocess.run(
            [
                "git",
                "--no-pager",
                "-c",
                "core.fsmonitor=false",
                "-c",
                "diff.relative=false",
                "-c",
                "log.showSignature=false",
                *arguments,
            ],
            cwd=repo,
            env=environment,
            input=data,
            capture_output=True,
            timeout=min(remaining, 10),
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise MetadataError("Git metadata query timed out") from error
    except OSError as error:
        raise MetadataError(f"Git metadata unavailable: {error}") from error
    if result.returncode:
        raise MetadataError(result.stderr[:300].decode("utf-8", errors="replace").strip())
    if len(result.stdout) > MAX_METADATA_BYTES or len(result.stderr) > MAX_METADATA_BYTES:
        raise MetadataError("Git metadata exceeds 4 MiB; inventory was not truncated")
    if time.monotonic() >= deadline:
        raise MetadataError("Git metadata protocol exceeded 30 seconds")
    return result.stdout


def _commit(repo: Path, revision: str, deadline: float) -> str:
    value = _git(
        repo,
        "rev-parse",
        "--verify",
        "--end-of-options",
        f"{revision}^{{commit}}",
        deadline=deadline,
    ).strip()
    if not OBJECT_ID.fullmatch(value):
        raise MetadataError("Git returned an invalid commit identifier")
    return value.decode("ascii")


def parse_changes(raw: bytes) -> list[Change]:
    """Read raw -z grammar, preserving spaces, Unicode and newlines in paths."""
    if raw and not raw.endswith(b"\0"):
        raise MetadataError("unterminated Git raw metadata")
    fields = raw.split(b"\0")
    changes = []
    position = 0
    while position < len(fields):
        header = fields[position].lstrip(b"\n")
        position += 1
        if not header:
            continue
        columns = header.split()
        if len(columns) != 5 or not columns[0].startswith(b":"):
            raise MetadataError("malformed Git raw change header")
        before, after, status = columns[2:]
        if not OBJECT_ID.fullmatch(before) or not OBJECT_ID.fullmatch(after):
            raise MetadataError("invalid object identifier in Git raw change")
        if status == b"U":
            raise MetadataError("unmerged index cannot be certified")
        if not re.fullmatch(rb"[ADMT]|[RC][0-9]{1,3}", status):
            raise MetadataError("unknown Git raw change status")
        if status.startswith((b"R", b"C")) and int(status[1:]) > 100:
            raise MetadataError("invalid Git similarity score")
        if any(
            not re.fullmatch(rb"(?:000000|100644|100755|120000|160000|040000)", mode)
            for mode in (columns[0][1:], columns[1])
        ):
            raise MetadataError("invalid Git raw file mode")
        count = 2 if status.startswith((b"R", b"C")) else 1
        if position + count > len(fields) or not all(fields[position : position + count]):
            raise MetadataError("missing path in Git raw change")
        path = os.fsdecode(fields[position + count - 1])
        position += count
        changes.append(Change(before, after, status, path, columns[1]))
    return changes


def inventory(repo: Path, base: str, *, head: str = "HEAD", staged: bool = False) -> list[Blob]:
    if staged and head != "HEAD":
        raise MetadataError("staged mode uses the current HEAD/index")
    deadline = time.monotonic() + MAX_SECONDS
    if (
        _git(repo, "rev-parse", "--is-shallow-repository", deadline=deadline).strip()
        != b"false"
    ):
        raise MetadataError("shallow history: fetch the explicit base/history before checking")
    start, end = _commit(repo, base, deadline), _commit(repo, head, deadline)
    objects = _git(
        repo, "rev-list", "--objects", "--no-object-names", f"{start}..{end}", deadline=deadline
    ).splitlines()
    if any(not OBJECT_ID.fullmatch(value) for value in objects):
        raise MetadataError("invalid object inventory")
    paths: dict[bytes, set[str]] = {value: set() for value in objects}
    history = parse_changes(
        _git(
            repo,
            "log",
            "--raw",
            "-z",
            "--format=",
            "--no-abbrev",
            "--no-renames",
            "--diff-merges=first-parent",
            "--root",
            f"{start}..{end}",
            "--",
            deadline=deadline,
        )
    )
    for change in history:
        if change.after in paths:
            paths[change.after].add(change.path)
    tip_arguments = ["diff", "--raw", "-z", "--no-abbrev", "--no-ext-diff", "-M100%"]
    tip_arguments.extend(["--cached", start] if staged else [start, end])
    for change in parse_changes(_git(repo, *tip_arguments, "--", deadline=deadline)):
        if change.mode == b"160000" or set(change.after) == {ord("0")}:
            continue
        # An unchanged base blob moved to another path adds no blob or extra copy.
        if (
            change.status == b"R100"
            and change.before == change.after
            and change.after not in paths
        ):
            continue
        paths.setdefault(change.after, set()).add(change.path)
    if not paths:
        return []
    identifiers = sorted(paths)
    metadata = _git(
        repo,
        "cat-file",
        "--batch-check=%(objectname) %(objecttype) %(objectsize)",
        deadline=deadline,
        data=b"\n".join(identifiers) + b"\n",
    ).splitlines()
    if len(metadata) != len(identifiers):
        raise MetadataError("object-size inventory is incomplete")
    blobs = []
    for expected, line in zip(identifiers, metadata, strict=True):
        columns = line.split()
        if len(columns) != 3 or columns[0] != expected or not columns[2].isdigit():
            raise MetadataError("object-size metadata is missing or malformed")
        kind = columns[1]
        if kind not in (b"blob", b"tree", b"commit", b"tag"):
            raise MetadataError("unknown Git object type")
        if kind == b"blob":
            if not paths[expected]:
                raise MetadataError("new blob lacks its historical path inventory")
            blobs.append(
                Blob(expected.decode("ascii"), int(columns[2]), tuple(sorted(paths[expected])))
            )
    return blobs


def violations(
    blobs: Sequence[Blob], *, per_blob: int = MAX_BLOB_BYTES, total: int = MAX_TOTAL_BYTES
) -> list[str]:
    if type(per_blob) is not int or type(total) is not int or min(per_blob, total) <= 0:
        raise MetadataError("byte ceilings must be positive integers")
    if any(type(blob.size) is not int or blob.size < 0 for blob in blobs):
        raise MetadataError("blob byte sizes must be nonnegative integers")
    failures = [
        f"{blob.size} bytes exceeds {per_blob}: {blob.paths!r} ({blob.object_id})"
        for blob in blobs
        if blob.size > per_blob
    ]
    amount = sum(blob.size for blob in blobs)
    if amount > total:
        failures.append(f"unique checked blobs total {amount} bytes exceeds {total}")
    return failures


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base", required=True, help="actual lower branch/base commit, not always main"
    )
    parser.add_argument(
        "--head", default="HEAD", help="actual PR head, not its synthetic merge"
    )
    parser.add_argument(
        "--staged", action="store_true", help="include the current index before commit"
    )
    args = parser.parse_args(argv)
    if args.staged and args.head != "HEAD":
        parser.error(
            "--staged checks the current HEAD/index; it cannot name a different --head"
        )
    try:
        blobs = inventory(Path.cwd(), args.base, head=args.head, staged=args.staged)
        failures = violations(blobs)
    except MetadataError as error:
        print(f"GUARD_REFUSED: {error}", file=sys.stderr)
        return 2
    if failures:
        for failure in failures:
            print(f"REJECT_ADDED_STORAGE: {failure}")
        return 1
    print(
        f"PASS: {len(blobs)} unique checked blobs, {sum(blob.size for blob in blobs)} bytes; "
        f"ceilings {MAX_BLOB_BYTES}/blob and {MAX_TOTAL_BYTES} total"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
