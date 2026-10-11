"""Refuse bulk Git blobs before commit and on a pull request's actual base/head.

Git object IDs identify storage being measured here; they never identify scientific
inputs or decide research verdicts. Existing unchanged base history is grandfathered.

The two ceilings are data, in devtools/added-blobs.yaml, so changing one is a visible
policy diff (OR-18). Against them the guard checks:

  per blob  every blob version newly reachable from HEAD and not from BASE, so
            committing then deleting a dump still fails, plus tip or index additions
            that reintroduce older base history. A path whose blob at BASE already
            exceeds the per-blob ceiling is grandfathered: changing it is the status
            quo, not added bulk data. A new path, a copy or an edited rename is not.
  in total  the largest version of each path, each blob object once, so a text file
            edited in twenty commits is charged once rather than once per version Git
            stores as a delta. A grandfathered path is charged only its growth.
  LFS       a Git LFS pointer is refused: this repository does not use LFS, and a
            pointer would carry bulk data past the gate.

Exact renames of current base files and gitlinks add nothing. Tip changes are read from
the merge base of BASE and HEAD, so a branch behind its base is not charged for the
base's newer files.

Exit 0 is PASS and 1 is REJECT_ADDED_STORAGE. Exit 2 is GUARD_REFUSED, never a pass: a
base this clone lacks (fetch it; a force-pushed base clears when the pull request
re-synchronizes), shallow history (fetch it), a range too long for the gate, malformed
Git metadata, a failed query or an unreadable ceilings file.

--census N replays the gate over the last N first-parent merges into --census-ref,
first parent as base and second as head, and prints each verdict with its reasons. That
replay is the measurement the ceilings are set against.

The tool reads no scientific artifact, downloads nothing and changes no Git
configuration.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path

import yaml

from sqpack.yamlio import load_yaml

POLICY = Path(__file__).with_name("added-blobs.yaml")
MAX_METADATA_BYTES = 64 * 1024**2
MAX_SECONDS = 30
MAX_QUERY_SECONDS = 10
# The LFS specification keeps pointers small; git-lfs never reads a larger blob as one.
LFS_POINTER_BYTES = 1024
LFS_POINTER_PREFIXES = (
    b"version https://git-lfs.github.com/spec/",
    b"version https://hawser.github.com/spec/",
)
OBJECT_ID = re.compile(rb"[0-9a-f]{40}(?:[0-9a-f]{24})?")
PULL_REQUEST_MERGE = re.compile(r"Merge pull request #([0-9]+)")


class MetadataError(ValueError):
    """Incomplete Git metadata cannot certify the branch."""


class GitExitError(MetadataError):
    """Git itself refused a query, as it does for a revision this clone lacks."""


@dataclass(frozen=True)
class Ceilings:
    """The byte ceilings `devtools/added-blobs.yaml` declares."""

    per_blob: int
    total: int


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
    lfs_pointer: bool = False


@dataclass(frozen=True)
class CensusRow:
    """One replayed merge: its verdict, or why the gate refused to give one."""

    merge: str
    subject: str
    blobs: tuple[Blob, ...] = ()
    exempt: tuple[tuple[str, int], ...] = ()
    failures: tuple[str, ...] = ()
    refusal: str = ""
    seconds: float = 0.0


def _mib(value: float) -> str:
    return f"{value / 1024**2:.2f} MiB"


def load_ceilings(path: Path | None = None) -> Ceilings:
    """Read the ceilings; a missing or malformed file refuses rather than defaults."""
    path = path or POLICY
    try:
        document: object = load_yaml(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        raise MetadataError(f"cannot read the ceilings in {path.name}: {error}") from error
    if not isinstance(document, dict):
        raise MetadataError(f"{path.name} must be a mapping")
    values: dict[object, object] = dict(document)  # pyright: ignore[reportUnknownArgumentType]
    if set(values) != {"per_blob_bytes", "total_bytes"}:
        raise MetadataError(f"{path.name} must declare exactly per_blob_bytes and total_bytes")
    per_blob, total = values["per_blob_bytes"], values["total_bytes"]
    if type(per_blob) is not int or type(total) is not int or min(per_blob, total) <= 0:
        raise MetadataError("byte ceilings must be positive integers")
    return Ceilings(per_blob, total)


def _git(repo: Path, *arguments: str, deadline: float, data: bytes | None = None) -> bytes:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise MetadataError(f"Git metadata protocol exceeded {MAX_SECONDS} seconds")
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
            timeout=min(remaining, MAX_QUERY_SECONDS),
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise MetadataError(
            f"Git metadata query exceeded {MAX_QUERY_SECONDS} seconds"
        ) from error
    except OSError as error:
        raise MetadataError(f"Git metadata unavailable: {error}") from error
    if result.returncode:
        raise GitExitError(result.stderr[:300].decode("utf-8", errors="replace").strip())
    if len(result.stdout) > MAX_METADATA_BYTES or len(result.stderr) > MAX_METADATA_BYTES:
        raise MetadataError(
            f"one Git query returned more than {MAX_METADATA_BYTES / 1024**2:g} MiB: the "
            "range is too long for this gate and nothing is missing to fetch, so check a "
            "shorter range (the inventory was not truncated)"
        )
    if time.monotonic() >= deadline:
        raise MetadataError(f"Git metadata protocol exceeded {MAX_SECONDS} seconds")
    return result.stdout


def _commit(repo: Path, revision: str, deadline: float) -> str:
    try:
        value = _git(
            repo,
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{revision}^{{commit}}",
            deadline=deadline,
        ).strip()
    except GitExitError as error:
        raise MetadataError(
            f"{revision!r} is not a commit in this clone ({error}): fetch it; a base that "
            "was force-pushed clears when the pull request re-synchronizes"
        ) from error
    if not OBJECT_ID.fullmatch(value):
        raise MetadataError("Git returned an invalid commit identifier")
    return value.decode("ascii")


def _merge_base(repo: Path, start: str, end: str, deadline: float) -> str:
    try:
        value = _git(repo, "merge-base", start, end, deadline=deadline).strip()
    except GitExitError as error:
        raise MetadataError(f"base and head share no history ({error})") from error
    if not OBJECT_ID.fullmatch(value):
        raise MetadataError("Git returned an invalid merge base")
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


def _lfs_pointers(repo: Path, identifiers: Sequence[str], deadline: float) -> set[str]:
    """The identifiers, all of small blobs, whose content is a Git LFS pointer."""
    output = _git(
        repo,
        "cat-file",
        "--batch",
        deadline=deadline,
        data="".join(f"{identifier}\n" for identifier in identifiers).encode("ascii"),
    )
    pointers: set[str] = set()
    position = 0
    for expected in identifiers:
        header_end = output.find(b"\n", position)
        columns = output[position:header_end].split() if header_end >= 0 else []
        if (
            len(columns) != 3
            or columns[0] != expected.encode("ascii")
            or columns[1] != b"blob"
            or not columns[2].isdigit()
        ):
            raise MetadataError("object content metadata is missing or malformed")
        start = header_end + 1
        end = start + int(columns[2])
        if output[end : end + 1] != b"\n":
            raise MetadataError("object content inventory is truncated")
        if output[start:end].startswith(LFS_POINTER_PREFIXES):
            pointers.add(expected)
        position = end + 1
    if position != len(output):
        raise MetadataError("object content inventory has unexpected trailing data")
    return pointers


def inventory(repo: Path, base: str, *, head: str = "HEAD", staged: bool = False) -> list[Blob]:
    if staged and head != "HEAD":
        raise MetadataError("staged mode uses the current HEAD/index")
    deadline = time.monotonic() + MAX_SECONDS
    if (
        _git(repo, "rev-parse", "--is-shallow-repository", deadline=deadline).strip()
        != b"false"
    ):
        raise MetadataError(
            "shallow history: fetch the full history (git fetch --unshallow) and recheck"
        )
    start, end = _commit(repo, base, deadline), _commit(repo, head, deadline)
    # What the branch itself changed, which is what merging it brings in. Diffed against
    # BASE directly, a branch behind it is charged for reverting BASE's newer files.
    fork = _merge_base(repo, start, end, deadline)
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
    tip_arguments.extend(["--cached", fork] if staged else [fork, end])
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
    small = [blob.object_id for blob in blobs if blob.size <= LFS_POINTER_BYTES]
    pointers = _lfs_pointers(repo, small, deadline) if small else set()
    return [replace(blob, lfs_pointer=blob.object_id in pointers) for blob in blobs]


def grandfathered(repo: Path, base: str, *, per_blob: int) -> dict[str, int]:
    """Paths whose blob at `base` already exceeds `per_blob`, with that blob's size."""
    deadline = time.monotonic() + MAX_SECONDS
    listing = _git(
        repo,
        "ls-tree",
        "-r",
        "-l",
        "-z",
        "--full-tree",
        _commit(repo, base, deadline),
        deadline=deadline,
    )
    if listing and not listing.endswith(b"\0"):
        raise MetadataError("unterminated Git tree listing")
    sizes: dict[str, int] = {}
    for entry in listing.split(b"\0")[:-1]:
        header, tab, path = entry.partition(b"\t")
        columns = header.split()
        if not tab or not path or len(columns) != 4:
            raise MetadataError("malformed Git tree listing")
        if columns[1] != b"blob":
            continue
        if not columns[3].isdigit():
            raise MetadataError("malformed blob size in Git tree listing")
        if int(columns[3]) > per_blob:
            sizes[os.fsdecode(path)] = int(columns[3])
    return sizes


def _exempt(blob: Blob, per_blob: int, exempt: Mapping[str, int]) -> bool:
    """Over the per-blob ceiling only at paths already over it at the base."""
    return (
        blob.size > per_blob and bool(blob.paths) and all(path in exempt for path in blob.paths)
    )


def charged_bytes(blobs: Sequence[Blob], exempt: Mapping[str, int] | None = None) -> int:
    """What the aggregate ceiling charges: each path's largest version, each blob once.

    A grandfathered path is charged only what its largest version adds to its base size.
    """
    exempt = exempt or {}
    largest: dict[str, Blob] = {}
    for blob in blobs:
        for path in blob.paths:
            current = largest.get(path)
            if current is None or (blob.size, blob.object_id) > (
                current.size,
                current.object_id,
            ):
                largest[path] = blob
    charges: dict[str, int] = {}
    for path, blob in largest.items():
        amount = max(0, blob.size - exempt[path]) if path in exempt else blob.size
        charges[blob.object_id] = max(charges.get(blob.object_id, 0), amount)
    return sum(charges.values())


def violations(
    blobs: Sequence[Blob],
    *,
    per_blob: int,
    total: int,
    exempt: Mapping[str, int] | None = None,
) -> list[str]:
    if type(per_blob) is not int or type(total) is not int or min(per_blob, total) <= 0:
        raise MetadataError("byte ceilings must be positive integers")
    if any(type(blob.size) is not int or blob.size < 0 for blob in blobs):
        raise MetadataError("blob byte sizes must be nonnegative integers")
    exempt = exempt or {}
    failures = [
        f"{blob.size} bytes exceeds {per_blob}: {blob.paths!r} ({blob.object_id})"
        for blob in blobs
        if blob.size > per_blob and not _exempt(blob, per_blob, exempt)
    ]
    failures.extend(
        f"Git LFS pointer, and this repository does not use LFS: {blob.paths!r} "
        f"({blob.object_id})"
        for blob in blobs
        if blob.lfs_pointer
    )
    amount = charged_bytes(blobs, exempt)
    if amount > total:
        failures.append(
            f"the largest version of each path totals {amount} bytes, exceeding {total}"
        )
    return failures


def judge(
    repo: Path, base: str, blobs: Sequence[Blob], ceilings: Ceilings
) -> tuple[dict[str, int], list[str]]:
    """The failures, with the paths grandfathered at `base` exempted.

    Grandfathering only ever removes a failure, so the base tree is listed only when
    there is one for it to remove, and a branch that passes without it pays nothing.
    """
    failures = violations(blobs, per_blob=ceilings.per_blob, total=ceilings.total)
    if not failures:
        return {}, failures
    exempt = grandfathered(repo, base, per_blob=ceilings.per_blob)
    return exempt, violations(
        blobs, per_blob=ceilings.per_blob, total=ceilings.total, exempt=exempt
    )


def census(repo: Path, ref: str, count: int, *, ceilings: Ceilings) -> list[CensusRow]:
    """Replay the gate over the last `count` first-parent merges into `ref`."""
    deadline = time.monotonic() + MAX_SECONDS
    merges = _git(
        repo,
        "rev-list",
        "--first-parent",
        "--merges",
        f"--max-count={count}",
        _commit(repo, ref, deadline),
        deadline=deadline,
    ).split()
    rows: list[CensusRow] = []
    for merge in merges:
        if not OBJECT_ID.fullmatch(merge):
            raise MetadataError("invalid merge identifier")
        started = time.monotonic()
        line = _git(
            repo,
            "log",
            "-1",
            "--format=%P%x00%s",
            merge.decode("ascii"),
            deadline=started + MAX_SECONDS,
        ).decode("utf-8", errors="replace")
        parents, _, subject = line.rstrip("\n").partition("\0")
        row = CensusRow(merge.decode("ascii"), subject)
        if len(parents.split()) != 2:
            rows.append(replace(row, refusal="not a two-parent merge"))
            continue
        first, second = parents.split()
        try:
            blobs = inventory(repo, first, head=second)
            exempt, failures = judge(repo, first, blobs, ceilings)
        except MetadataError as error:
            rows.append(replace(row, refusal=str(error), seconds=time.monotonic() - started))
            continue
        rows.append(
            replace(
                row,
                blobs=tuple(blobs),
                exempt=tuple(sorted(exempt.items())),
                failures=tuple(failures),
                seconds=time.monotonic() - started,
            )
        )
    return rows


def print_census(rows: Sequence[CensusRow], ref: str, ceilings: Ceilings) -> None:
    print(
        f"CENSUS: {len(rows)} first-parent merges into {ref}; ceilings "
        f"{ceilings.per_blob}/blob and {ceilings.total} total"
    )
    for row in rows:
        number = PULL_REQUEST_MERGE.match(row.subject)
        label = f"{row.merge[:9]} {'#' + number.group(1) if number else '(no PR)'}"
        if row.refusal:
            print(f"  {label} GUARD_REFUSED: {row.refusal}")
            continue
        exempt = dict(row.exempt)
        largest = max(row.blobs, key=lambda blob: blob.size, default=None)
        detail = f"{len(row.blobs)} blobs, {_mib(charged_bytes(row.blobs, exempt))} charged"
        if largest is not None:
            detail += f", largest {_mib(largest.size)} {largest.paths[0]}"
        grandfathered_blobs = sum(
            1 for blob in row.blobs if _exempt(blob, ceilings.per_blob, exempt)
        )
        if grandfathered_blobs:
            detail += f", {grandfathered_blobs} grandfathered"
        print(
            f"  {label} {'REJECT' if row.failures else 'pass'}: {detail}; {row.seconds:.1f} s"
        )
        for failure in row.failures:
            print(f"      {failure}")
    rejected = [row for row in rows if row.failures]
    aggregate_only = sum(
        1
        for row in rejected
        if not any(
            blob.lfs_pointer
            or (
                blob.size > ceilings.per_blob
                and not _exempt(blob, ceilings.per_blob, dict(row.exempt))
            )
            for blob in row.blobs
        )
    )
    refused = sum(1 for row in rows if row.refusal)
    print(
        f"SUMMARY: {len(rejected)} of {len(rows)} merges rejected, {aggregate_only} of them "
        f"by the total alone; {refused} guard refusals; "
        f"{sum(row.seconds for row in rows):.1f} s"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--base",
        help="actual lower branch/base commit, not always main; origin/<base> after git fetch",
    )
    parser.add_argument(
        "--head", default="HEAD", help="actual PR head, not its synthetic merge"
    )
    parser.add_argument(
        "--staged", action="store_true", help="include the current index before commit"
    )
    parser.add_argument(
        "--census",
        type=int,
        metavar="N",
        help="replay the gate over the last N first-parent merges into --census-ref",
    )
    parser.add_argument(
        "--census-ref", default="origin/main", help="the branch --census replays merges into"
    )
    args = parser.parse_args(argv)
    if (args.base is None) == (args.census is None):
        parser.error("give exactly one of --base or --census")
    if args.census is not None and (args.census <= 0 or args.staged or args.head != "HEAD"):
        parser.error("--census takes a positive count and no --head or --staged")
    if args.staged and args.head != "HEAD":
        parser.error(
            "--staged checks the current HEAD/index; it cannot name a different --head"
        )
    try:
        ceilings = load_ceilings()
        if args.census is not None:
            rows = census(Path.cwd(), args.census_ref, args.census, ceilings=ceilings)
            print_census(rows, args.census_ref, ceilings)
            return 0
        blobs = inventory(Path.cwd(), args.base, head=args.head, staged=args.staged)
        exempt, failures = judge(Path.cwd(), args.base, blobs, ceilings)
    except MetadataError as error:
        print(f"GUARD_REFUSED: {error}", file=sys.stderr)
        return 2
    for blob in blobs:
        if _exempt(blob, ceilings.per_blob, exempt):
            print(
                f"GRANDFATHERED: {blob.size} bytes at {blob.paths!r} ({blob.object_id}); "
                "each path was already over the per-blob ceiling at the base"
            )
    if failures:
        for failure in failures:
            print(f"REJECT_ADDED_STORAGE: {failure}")
        return 1
    print(
        f"PASS: {len(blobs)} unique checked blobs, {charged_bytes(blobs, exempt)} bytes "
        f"charged; ceilings {ceilings.per_blob}/blob and {ceilings.total} total"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
