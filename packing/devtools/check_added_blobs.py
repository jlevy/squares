"""Refuse bulk Git blobs before commit and on a pull request's actual base/head.

Git object IDs identify storage being measured here; they never identify scientific
inputs or decide research verdicts. Existing unchanged base history is grandfathered.

Sizes are OR-18's. A blob counts as Git stores it, its object compressed by zlib at the
default level (`devtools.git_storage`). A set counts as what it adds to the repository:
the thin pack of its new objects against the base, deltas included, which is what a fetch
of the branch downloads and what history keeps. The two ceilings are data, in
devtools/added-blobs.yaml, so changing one is a visible policy diff. Against them the
guard checks:

  per blob  every blob version new to history, plus tip or index additions that copy a
            base blob or restore one from older base history. A path whose blob at
            BASE is already over the per-blob ceiling is grandfathered: changing it is
            the status quo, not added bulk data. A new path, a copy or an edited
            rename is not.
  in total  the bytes of `git pack-objects --revs --thin` over the objects new to
            history, commits and trees included, with the index's additions in
            --staged mode. Versions the head deleted or reverted, each version of a
            path edited many times and a grandfathered path's rewrites are all in it,
            but a version that differs a little from another is a small delta, so
            rewriting a large text register many times costs about its edits. Until
            2026-10-22 the total was the sum of each new version's own stored size,
            which charged #578's register churn 59.17 MiB against a 2.39 MiB pack.
  LFS       a Git LFS pointer is refused: this repository does not use LFS, and a
            pointer would carry bulk data past the gate.

A version is new to history when it is reachable from HEAD, or from the index, and not
from BASE's tree or from the trees where the branch meets BASE's history: Git's own
reading of a range's new objects (rev-list --objects-edge-aggressive). A blob restored
verbatim from deeper in BASE's history is counted again, which errs toward refusing.
Exact renames, mode-only changes and gitlinks add nothing. Tip changes are read from
the merge base of BASE and HEAD, so a branch behind its base is not charged for the
base's newer files.

Sizing a version means compressing its content, so each checked blob is streamed through
zlib once and never held whole, and one check reads at most MAX_CONTENT_BYTES of it. The
pack is streamed too and only counted, with one delta-search thread, so a clone gives
the same figure on every run. Git reuses the deltas its object store already holds, so
clones packed differently give different figures. The reference is CI's: the pull
request's check runs in a fresh full clone of GitHub's packs. On the ranges measured in
reviews K and L of #406, CI read 12% (#578: about 2.7 MiB against 2.39) to 37% (#406's
own range: 232,934 bytes against 169,790) more than a working clone on text-heavy
ranges, and 0 to 2.4% more on bulk-dominated ones.
Recomputing every delta would make the figure nearly clone-independent, but #461's pack
alone then takes 25.6 s. A working clone also packs its loose objects afresh, so `--push`
on a large branch before `git gc` is slower: #474's 1,191 loose objects took 17.8 s
against about 10 s packed. One deadline, MAX_SECONDS, bounds the whole check, parsing
and packing included, and each metadata query also has its own, MAX_QUERY_SECONDS.

Exit 0 is PASS and 1 is REJECT_ADDED_STORAGE. Exit 2 is GUARD_REFUSED, never a pass: a
base this clone lacks (fetch it; a force-pushed base clears when the pull request
re-synchronizes), shallow history (fetch it), a range too long or too large for the gate,
a check past its deadline, malformed Git metadata, a failed query or an unreadable
ceilings file.

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
import select
import selectors
import subprocess
import sys
import time
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from dataclasses import KW_ONLY, dataclass, replace
from pathlib import Path
from typing import NamedTuple

import yaml

from devtools.git_storage import StoredSize, stored_size_bound
from sqpack.yamlio import load_yaml

POLICY = Path(__file__).with_name("added-blobs.yaml")
MAX_METADATA_BYTES = 64 * 1024**2
METADATA_READ_BYTES = 64 * 1024
# Blob content one check reads and compresses. Every merge into main to 2026-10-22 is
# under it, the largest being #461 at 446 MiB, which took 18 s with its pack on a shared
# 4-CPU host.
MAX_CONTENT_BYTES = 512 * 1024**2
MAX_SECONDS = 30
MAX_QUERY_SECONDS = 10
# How many parsed entries pass between deadline checks.
DEADLINE_STRIDE = 4096
# Git's own defaults for the pack that sizes the total, pinned so that a local
# configuration cannot move the measure. Bitmaps and the sparse walk are off so the
# object set is exactly rev-list's: with a bitmap, Git would leave out a blob the branch
# restores from deeper in BASE's history, which the inventory charges (review L2 of
# #406). Delta search runs on one thread with no window memory limit: with a thread per
# CPU, #578 packed to anything from 2,803,938 to 3,186,775 bytes from one run to the
# next in CI's clone, and with one it gave the same bytes every time, for at most 1.5 s
# more on #474 (review K1 of #406).
PACK_CONFIG = (
    "core.compression=-1",
    "pack.compression=-1",
    "core.bigFileThreshold=512m",
    "pack.window=10",
    "pack.depth=50",
    "pack.windowMemory=0",
    "pack.threads=1",
    "pack.useBitmaps=false",
)
# The LFS specification keeps pointers small; git-lfs never reads a larger blob as one.
LFS_POINTER_BYTES = 1024
LFS_POINTER_PREFIXES = (
    b"version https://git-lfs.github.com/spec/",
    b"version https://hawser.github.com/spec/",
)
OBJECT_ID = re.compile(rb"[0-9a-f]{40}(?:[0-9a-f]{24})?")
RAW_STATUS = re.compile(rb"[ADMT]|[RC][0-9]{1,3}")
RAW_MODE = re.compile(rb"000000|100644|100755|120000|160000|040000")
PULL_REQUEST_MERGE = re.compile(r"Merge pull request #([0-9]+)")
# A `cat-file --batch` header is an object ID, a type and a size; anything longer is not one.
MAX_HEADER_BYTES = 128


class MetadataError(ValueError):
    """Incomplete Git metadata cannot certify the branch."""


class GitExitError(MetadataError):
    """Git itself refused a query, as it does for a revision this clone lacks."""


@dataclass(frozen=True)
class Ceilings:
    """The byte ceilings `devtools/added-blobs.yaml` declares, as Git stores a blob."""

    per_blob: int
    total: int


class Change(NamedTuple):
    """One raw change; a tuple, since a long log builds hundreds of thousands."""

    before: bytes
    after: bytes
    status: bytes
    path: str
    mode: bytes


@dataclass(frozen=True)
class Blob:
    """One checked blob version, sized as Git stores it (`stored`) and in a checkout."""

    object_id: str
    stored: int
    paths: tuple[str, ...]
    _: KW_ONLY
    checkout: int
    # New to history, so counted toward the total. False for a tip or index addition of a
    # blob BASE's history already stores, a copy or a restored version, which is held to
    # the per-blob ceiling only.
    charged: bool = True
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
    added: int = 0


def _mib(value: float) -> str:
    return f"{value / 1024**2:.2f} MiB"


def _deadline() -> float:
    return time.monotonic() + MAX_SECONDS


def _within(deadline: float) -> None:
    """Refuse once the check has run past its one deadline."""
    if time.monotonic() >= deadline:
        raise MetadataError(
            f"the check exceeded its {MAX_SECONDS}-second deadline: check a shorter range, "
            "or in a working clone pack its loose objects with `git gc` first"
        )


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


def _capture_git(
    child: subprocess.Popen[bytes],
    *,
    deadline: float,
    data: bytes | None,
    sink: Callable[[bytes], None] | None = None,
) -> tuple[bytes, bytes]:
    """Drain both output pipes while feeding stdin, retaining at most each byte cap.

    With a `sink`, standard output is handed to it chunk by chunk and nothing of it is
    retained; the sink bounds what it accepts.
    """
    assert child.stdout is not None
    assert child.stderr is not None
    stdout, stderr = child.stdout.fileno(), child.stderr.fileno()
    output = {stdout: bytearray(), stderr: bytearray()}
    pending = memoryview(data or b"")
    with selectors.DefaultSelector() as selector:
        for descriptor in output:
            os.set_blocking(descriptor, False)
            selector.register(descriptor, selectors.EVENT_READ)
        if child.stdin is not None:
            if pending:
                descriptor = child.stdin.fileno()
                os.set_blocking(descriptor, False)
                selector.register(descriptor, selectors.EVENT_WRITE)
            else:
                child.stdin.close()
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise subprocess.TimeoutExpired(child.args, MAX_QUERY_SECONDS)
            ready = selector.select(remaining)
            if time.monotonic() >= deadline:
                raise subprocess.TimeoutExpired(child.args, MAX_QUERY_SECONDS)
            for key, _events in ready:
                if key.fd in output:
                    buffer = output[key.fd]
                    streamed = sink is not None and key.fd == stdout
                    # The extra byte detects excess without ever retaining excess output.
                    chunk = os.read(
                        key.fd,
                        METADATA_READ_BYTES
                        if streamed
                        else min(METADATA_READ_BYTES, MAX_METADATA_BYTES + 1 - len(buffer)),
                    )
                    if not chunk:
                        selector.unregister(key.fd)
                        continue
                    if streamed:
                        assert sink is not None
                        sink(chunk)
                        continue
                    if len(buffer) + len(chunk) > MAX_METADATA_BYTES:
                        raise MetadataError(
                            "one Git query returned more than "
                            f"{MAX_METADATA_BYTES / 1024**2:g} "
                            "MiB: the range is too long for this gate and nothing is missing "
                            "to fetch, so check a shorter range "
                            "(the inventory was not truncated)"
                        )
                    buffer.extend(chunk)
                else:
                    assert child.stdin is not None
                    try:
                        written = os.write(key.fd, pending[: select.PIPE_BUF])
                    except BrokenPipeError:
                        pending = memoryview(b"")
                    else:
                        pending = pending[written:]
                    if not pending:
                        selector.unregister(key.fd)
                        child.stdin.close()
        child.wait(timeout=max(0, deadline - time.monotonic()))
    return bytes(output[stdout]), bytes(output[stderr])


def _git(
    repo: Path,
    *arguments: str,
    deadline: float,
    data: bytes | None = None,
    sink: Callable[[bytes], None] | None = None,
) -> bytes:
    """One Git query under the check's deadline and, unless it streams content, its own.

    A streamed content read (`sink`) has no deadline of its own: its cost is the content
    it compresses, which MAX_CONTENT_BYTES bounds, and the check's deadline still holds.
    """
    _within(deadline)
    query_deadline = (
        deadline if sink is not None else min(deadline, time.monotonic() + MAX_QUERY_SECONDS)
    )
    environment = dict(os.environ)
    environment.update(
        GIT_NO_LAZY_FETCH="1", GIT_NO_REPLACE_OBJECTS="1", GIT_TERMINAL_PROMPT="0"
    )
    try:
        with subprocess.Popen(
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
            stdin=subprocess.PIPE if data is not None else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        ) as child:
            try:
                stdout, stderr = _capture_git(
                    child, deadline=query_deadline, data=data, sink=sink
                )
            finally:
                if child.poll() is None:
                    child.kill()
                child.wait()
    except subprocess.TimeoutExpired as error:
        _within(deadline)
        raise MetadataError(
            f"one Git metadata query exceeded {MAX_QUERY_SECONDS} seconds"
        ) from error
    except OSError as error:
        raise MetadataError(f"Git metadata unavailable: {error}") from error
    if child.returncode:
        raise GitExitError(stderr[:300].decode("utf-8", errors="replace").strip())
    _within(deadline)
    return stdout


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


def _changes(raw: bytes, deadline: float | None = None) -> Iterator[Change]:
    """Read raw -z grammar lazily, preserving spaces, Unicode and newlines in paths.

    Nothing but the current entry is built, so a long log costs its raw bytes and no
    more, and the check's deadline is held while it is read.
    """
    if raw and not raw.endswith(b"\0"):
        raise MetadataError("unterminated Git raw metadata")
    position, size, parsed = 0, len(raw), 0
    while position < size:
        stop = raw.index(b"\0", position)
        header = raw[position:stop].lstrip(b"\n")
        position = stop + 1
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
        if not RAW_STATUS.fullmatch(status):
            raise MetadataError("unknown Git raw change status")
        if status.startswith((b"R", b"C")) and int(status[1:]) > 100:
            raise MetadataError("invalid Git similarity score")
        if any(not RAW_MODE.fullmatch(mode) for mode in (columns[0][1:], columns[1])):
            raise MetadataError("invalid Git raw file mode")
        name = b""
        for _ in range(2 if status.startswith((b"R", b"C")) else 1):
            stop = raw.index(b"\0", position) if position < size else position
            if stop == position:
                raise MetadataError("missing path in Git raw change")
            name, position = raw[position:stop], stop + 1
        parsed += 1
        if deadline is not None and parsed % DEADLINE_STRIDE == 0:
            _within(deadline)
        yield Change(before, after, status, os.fsdecode(name), columns[1])


def parse_changes(raw: bytes) -> list[Change]:
    """Read raw -z grammar, preserving spaces, Unicode and newlines in paths."""
    return list(_changes(raw))


def _null(identifier: bytes) -> bool:
    return set(identifier) == {ord("0")}


def _object_sizes(
    repo: Path, identifiers: Sequence[bytes], deadline: float
) -> dict[bytes, tuple[bytes, int]]:
    """Each object's type and size in a checkout, in one `cat-file --batch-check`."""
    metadata = _git(
        repo,
        "cat-file",
        "--batch-check=%(objectname) %(objecttype) %(objectsize)",
        deadline=deadline,
        data=b"\n".join(identifiers) + b"\n",
    ).splitlines()
    if len(metadata) != len(identifiers):
        raise MetadataError("object-size inventory is incomplete")
    sizes: dict[bytes, tuple[bytes, int]] = {}
    for parsed, (expected, line) in enumerate(zip(identifiers, metadata, strict=True)):
        columns = line.split()
        if len(columns) != 3 or columns[0] != expected or not columns[2].isdigit():
            raise MetadataError("object-size metadata is missing or malformed")
        if columns[1] not in (b"blob", b"tree", b"commit", b"tag"):
            raise MetadataError("unknown Git object type")
        sizes[expected] = (columns[1], int(columns[2]))
        if parsed % DEADLINE_STRIDE == 0:
            _within(deadline)
    return sizes


class _ContentReader:
    """Reads `cat-file --batch` output as it arrives, holding one chunk at a time.

    For each expected blob, in order, it records the size as Git stores it and whether the
    content is a Git LFS pointer, and it refuses output that is missing, malformed,
    truncated or longer than what was asked for.
    """

    def __init__(self, expected: Sequence[tuple[bytes, int]]) -> None:
        self._expected = expected
        self._index = 0
        self._header = bytearray()
        self._measure: StoredSize | None = None
        self._remaining = 0
        self._small = bytearray()
        self._terminator = False
        self.measured: dict[bytes, tuple[int, bool]] = {}

    def feed(self, chunk: bytes) -> None:
        view = memoryview(chunk)
        while view:
            if self._terminator:
                if view[0] != ord("\n"):
                    raise MetadataError("object content inventory is truncated")
                view = view[1:]
                self._finish_blob()
            elif self._measure is None:
                view = self._read_header(view)
            else:
                take = min(self._remaining, len(view))
                piece = view[:take]
                self._measure.update(piece)
                if self._expected[self._index][1] <= LFS_POINTER_BYTES:
                    self._small.extend(piece)
                self._remaining -= take
                view = view[take:]
                self._terminator = self._remaining == 0

    def _read_header(self, view: memoryview) -> memoryview:
        if self._index >= len(self._expected):
            raise MetadataError("object content inventory has unexpected trailing data")
        end = bytes(view[: MAX_HEADER_BYTES + 1]).find(b"\n")
        if end < 0:
            self._header.extend(view)
            if len(self._header) > MAX_HEADER_BYTES:
                raise MetadataError("object content metadata is missing or malformed")
            return view[len(view) :]
        self._header.extend(view[:end])
        identifier, size = self._expected[self._index]
        if bytes(self._header).split() != [identifier, b"blob", b"%d" % size]:
            raise MetadataError("object content metadata is missing or malformed")
        self._header.clear()
        self._measure = StoredSize(size)
        self._remaining = size
        self._terminator = size == 0
        return view[end + 1 :]

    def _finish_blob(self) -> None:
        assert self._measure is not None
        identifier, _size = self._expected[self._index]
        self.measured[identifier] = (
            self._measure.result(),
            bytes(self._small).startswith(LFS_POINTER_PREFIXES),
        )
        self._measure, self._terminator = None, False
        self._small.clear()
        self._index += 1

    def finish(self) -> dict[bytes, tuple[int, bool]]:
        if self._index != len(self._expected) or self._header or self._measure is not None:
            raise MetadataError("object content inventory is truncated")
        return self.measured


def _content_room(sizes: Mapping[bytes, int]) -> None:
    """Refuse, before reading any, content past what one check compresses."""
    volume = sum(sizes.values())
    if volume > MAX_CONTENT_BYTES:
        raise MetadataError(
            f"sizing these blobs means compressing {_mib(volume)} of content, more than "
            f"the {_mib(MAX_CONTENT_BYTES)} this gate reads: the range is too large for it "
            "and nothing is missing to fetch, so check a shorter range"
        )


def _measure(
    repo: Path, sizes: Mapping[bytes, int], deadline: float
) -> dict[bytes, tuple[int, bool]]:
    """Each blob's size as Git stores it and whether it is an LFS pointer.

    The content is streamed through zlib, one chunk held at a time, and a request for more
    than MAX_CONTENT_BYTES is refused before anything is read.
    """
    if not sizes:
        return {}
    _content_room(sizes)
    identifiers = sorted(sizes)
    reader = _ContentReader([(identifier, sizes[identifier]) for identifier in identifiers])
    _git(
        repo,
        "cat-file",
        "--batch",
        deadline=deadline,
        data=b"".join(identifier + b"\n" for identifier in identifiers),
        sink=reader.feed,
    )
    return reader.finish()


class Range(NamedTuple):
    """A check's base and head commits, and the blobs the tip or index adds by path."""

    start: str
    end: str
    tip: dict[bytes, set[str]]


def _range(repo: Path, base: str, head: str, *, staged: bool, deadline: float) -> Range:
    """Resolve the range a check measures, refusing shallow history and missing commits."""
    if staged and head != "HEAD":
        raise MetadataError("staged mode uses the current HEAD/index")
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
    tip_arguments = ["diff", "--raw", "-z", "--no-abbrev", "--no-ext-diff", "-M100%"]
    tip_arguments.extend(["--cached", fork] if staged else [fork, end])
    tip: dict[bytes, set[str]] = {}
    for change in _changes(_git(repo, *tip_arguments, "--", deadline=deadline), deadline):
        # A gitlink, a deletion, a mode-only change or an exact rename adds no blob.
        if change.mode == b"160000" or _null(change.after) or change.before == change.after:
            continue
        tip.setdefault(change.after, set()).add(change.path)
    return Range(start, end, tip)


def inventory(
    repo: Path,
    base: str,
    *,
    head: str = "HEAD",
    staged: bool = False,
    deadline: float | None = None,
    resolved: Range | None = None,
) -> list[Blob]:
    """Every blob version the branch adds to history, and every tip or index addition.

    `resolved` is the range `_range` already resolved for this check, so that the
    inventory and the pack measure the same commits however `base` moves meanwhile.
    """
    deadline = _deadline() if deadline is None else deadline
    start, end, tip = resolved or _range(repo, base, head, staged=staged, deadline=deadline)
    # New to history: reachable from HEAD, or the index's additions given on stdin, and
    # from neither BASE's tree nor an edge's. Edge commits print with a leading "-".
    new: set[bytes] = set()
    for line in _git(
        repo,
        "rev-list",
        "--objects",
        "--objects-edge-aggressive",
        "--no-object-names",
        "--filter=object:type=blob",
        "--stdin",
        f"{start}..{end}",
        deadline=deadline,
        data=b"".join(identifier + b"\n" for identifier in sorted(tip)),
    ).splitlines():
        if not OBJECT_ID.fullmatch(line.removeprefix(b"-")):
            raise MetadataError("invalid object inventory")
        if not line.startswith(b"-"):
            new.add(line)
    identifiers = sorted(new | tip.keys())
    if not identifiers:
        _within(deadline)
        return []
    sizes = {
        identifier: size
        for identifier, (kind, size) in _object_sizes(repo, identifiers, deadline).items()
        if kind == b"blob"
    }
    _content_room(sizes)
    paths: dict[bytes, set[str]] = {}
    for change in _changes(
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
        ),
        deadline,
    ):
        if change.after in new and change.after in sizes:
            paths.setdefault(change.after, set()).add(change.path)
    for identifier, names in tip.items():
        paths.setdefault(identifier, set()).update(names)
    if any(not paths.get(identifier) for identifier in sizes):
        raise MetadataError("new blob lacks its historical path inventory")
    measured = _measure(repo, sizes, deadline)
    blobs = [
        Blob(
            identifier.decode("ascii"),
            measured[identifier][0],
            tuple(sorted(paths[identifier])),
            checkout=sizes[identifier],
            charged=identifier in new,
            lfs_pointer=measured[identifier][1],
        )
        for identifier in sorted(sizes)
    ]
    _within(deadline)
    return blobs


def added_bytes(
    repo: Path,
    base: str,
    *,
    head: str = "HEAD",
    staged: bool = False,
    deadline: float | None = None,
    resolved: Range | None = None,
) -> int:
    """What the branch adds to the repository: the thin pack of its new objects.

    `git pack-objects --revs --thin --shallow` packs every commit, tree and blob reachable
    from HEAD and from none of BASE's trees or the trees where the branch meets BASE's
    history (the same reading as `inventory`), with deltas against each other and
    against those trees' objects. In --staged mode the index's additions join it; one in
    BASE's tree adds nothing, while one restored from deeper in BASE's history is packed
    again, as the inventory charges it. The pack is counted as it streams and never held;
    an empty range packs to nothing and counts 0. `resolved` is as for `inventory`.
    """
    deadline = _deadline() if deadline is None else deadline
    start, end, tip = resolved or _range(repo, base, head, staged=staged, deadline=deadline)
    revisions = [end.encode("ascii"), b"^" + start.encode("ascii")]
    if staged:
        revisions.extend(sorted(tip))
    counted = [0]

    def count(chunk: bytes) -> None:
        counted[0] += len(chunk)

    configuration = [option for setting in PACK_CONFIG for option in ("-c", setting)]
    _git(
        repo,
        *configuration,
        "pack-objects",
        "--revs",
        "--thin",
        "--shallow",
        "--no-sparse",
        "--delta-base-offset",
        "--non-empty",
        "--stdout",
        "-q",
        deadline=deadline,
        data=b"".join(revision + b"\n" for revision in revisions),
        sink=count,
    )
    return counted[0]


def grandfathered(
    repo: Path,
    base: str,
    *,
    per_blob: int,
    paths: Iterable[str] | None = None,
    deadline: float | None = None,
) -> dict[str, int]:
    """Paths whose blob at `base` is already over `per_blob` as Git stores it, with that size.

    `paths` limits the answer to the paths a judgement asks about, so that only their base
    blobs are read; without it every base blob that could be over the ceiling is.
    """
    deadline = _deadline() if deadline is None else deadline
    listing = _git(
        repo,
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        _commit(repo, base, deadline),
        deadline=deadline,
    )
    if listing and not listing.endswith(b"\0"):
        raise MetadataError("unterminated Git tree listing")
    wanted = None if paths is None else set(paths)
    found: dict[str, bytes] = {}
    for parsed, entry in enumerate(listing.split(b"\0")[:-1]):
        header, tab, name = entry.partition(b"\t")
        columns = header.split()
        if not tab or not name or len(columns) != 3:
            raise MetadataError("malformed Git tree listing")
        if parsed % DEADLINE_STRIDE == 0:
            _within(deadline)
        if columns[1] != b"blob":
            continue
        if not OBJECT_ID.fullmatch(columns[2]):
            raise MetadataError("malformed object identifier in Git tree listing")
        path = os.fsdecode(name)
        if wanted is None or path in wanted:
            found[path] = columns[2]
    if not found:
        _within(deadline)
        return {}
    # A blob whose bound is under the ceiling cannot be over it, so it is not read.
    candidates = {
        identifier: size
        for identifier, (kind, size) in _object_sizes(
            repo, sorted(set(found.values())), deadline
        ).items()
        if kind == b"blob" and stored_size_bound(size) > per_blob
    }
    measured = _measure(repo, candidates, deadline)
    sizes = {
        path: measured[identifier][0]
        for path, identifier in sorted(found.items())
        if identifier in measured and measured[identifier][0] > per_blob
    }
    _within(deadline)
    return sizes


def _exempt(blob: Blob, per_blob: int, exempt: Mapping[str, int]) -> bool:
    """Over the per-blob ceiling only at paths already over it at the base."""
    return (
        blob.stored > per_blob
        and bool(blob.paths)
        and all(path in exempt for path in blob.paths)
    )


def _charged(blobs: Sequence[Blob]) -> dict[str, Blob]:
    """The checked blob versions that are new to history, each object once."""
    return {blob.object_id: blob for blob in blobs if blob.charged}


def violations(
    blobs: Sequence[Blob],
    *,
    per_blob: int,
    total: int,
    added: int,
    exempt: Mapping[str, int] | None = None,
) -> list[str]:
    """The per-blob and LFS failures of `blobs`, and the total's for `added` pack bytes."""
    if type(per_blob) is not int or type(total) is not int or min(per_blob, total) <= 0:
        raise MetadataError("byte ceilings must be positive integers")
    if type(added) is not int or added < 0:
        raise MetadataError("the added pack size must be a nonnegative integer")
    if any(
        type(size) is not int or size < 0
        for blob in blobs
        for size in (blob.stored, blob.checkout)
    ):
        raise MetadataError("blob byte sizes must be nonnegative integers")
    exempt = exempt or {}
    failures = [
        f"{blob.stored} bytes exceeds {per_blob} as Git stores them: {blob.paths!r} "
        f"({blob.object_id}, {blob.checkout} bytes in a checkout)"
        for blob in blobs
        if blob.stored > per_blob and not _exempt(blob, per_blob, exempt)
    ]
    failures.extend(
        f"Git LFS pointer, and this repository does not use LFS: {blob.paths!r} "
        f"({blob.object_id})"
        for blob in blobs
        if blob.lfs_pointer
    )
    if added > total:
        failures.append(
            f"the range adds {added} bytes to the repository, as a thin pack of its new "
            f"objects against the base, exceeding {total}"
        )
    return failures


def judge(
    repo: Path,
    base: str,
    blobs: Sequence[Blob],
    ceilings: Ceilings,
    *,
    added: int,
    deadline: float | None = None,
) -> tuple[dict[str, int], list[str]]:
    """The failures, with the paths grandfathered at `base` exempted.

    Grandfathering only ever removes a per-blob failure, so the base tree is listed only
    for a blob over that ceiling, and only that blob's paths are measured at the base.
    The total is judged on `added`, the range's thin pack from `added_bytes`.
    """
    deadline = _deadline() if deadline is None else deadline
    over = sorted(
        {path for blob in blobs if blob.stored > ceilings.per_blob for path in blob.paths}
    )
    exempt = (
        grandfathered(repo, base, per_blob=ceilings.per_blob, paths=over, deadline=deadline)
        if over
        else {}
    )
    failures = violations(
        blobs, per_blob=ceilings.per_blob, total=ceilings.total, added=added, exempt=exempt
    )
    _within(deadline)
    return exempt, failures


def census(repo: Path, ref: str, count: int, *, ceilings: Ceilings) -> list[CensusRow]:
    """Replay the gate over the last `count` first-parent merges into `ref`."""
    deadline = _deadline()
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
        # Each replay is one check, with the deadline a pull request's check would have.
        replay = _deadline()
        line = _git(
            repo, "log", "-1", "--format=%P%x00%s", merge.decode("ascii"), deadline=replay
        ).decode("utf-8", errors="replace")
        parents, _, subject = line.rstrip("\n").partition("\0")
        row = CensusRow(merge.decode("ascii"), subject)
        if len(parents.split()) != 2:
            rows.append(replace(row, refusal="not a two-parent merge"))
            continue
        first, second = parents.split()
        try:
            resolved = _range(repo, first, second, staged=False, deadline=replay)
            blobs = inventory(repo, first, head=second, deadline=replay, resolved=resolved)
            added = added_bytes(repo, first, head=second, deadline=replay, resolved=resolved)
            exempt, failures = judge(repo, first, blobs, ceilings, added=added, deadline=replay)
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
                added=added,
            )
        )
    return rows


def _label(row: CensusRow) -> str:
    number = PULL_REQUEST_MERGE.match(row.subject)
    return f"{row.merge[:9]} {'#' + number.group(1) if number else '(no PR)'}"


def print_census(rows: Sequence[CensusRow], ref: str, ceilings: Ceilings) -> None:
    print(
        f"CENSUS: {len(rows)} first-parent merges into {ref}; ceilings "
        f"{ceilings.per_blob}/blob as Git stores it and {ceilings.total} total as a thin pack"
    )
    for row in rows:
        label = _label(row)
        if row.refusal:
            print(f"  {label} GUARD_REFUSED: {row.refusal}")
            continue
        exempt = dict(row.exempt)
        charged = _charged(row.blobs)
        largest = max(row.blobs, key=lambda blob: blob.stored, default=None)
        detail = (
            f"{_mib(row.added)} added as a thin pack; {len(row.blobs)} blobs checked, "
            f"{len(charged)} new versions, "
            f"{_mib(sum(blob.stored for blob in charged.values()))} summed as stored "
            f"({_mib(sum(blob.checkout for blob in charged.values()))} in a checkout)"
        )
        if largest is not None:
            detail += f", largest {_mib(largest.stored)} {largest.paths[0]}"
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
                blob.stored > ceilings.per_blob
                and not _exempt(blob, ceilings.per_blob, dict(row.exempt))
            )
            for blob in row.blobs
        )
    )
    refused = sum(1 for row in rows if row.refusal)
    passed = [row for row in rows if not row.refusal and not row.failures]
    largest_pass = max(passed, key=lambda row: row.added, default=None)
    print(
        f"SUMMARY: {len(rejected)} of {len(rows)} merges rejected, {aggregate_only} of them "
        f"by the total alone; {refused} guard refusals; "
        + (
            f"largest passing total {_mib(largest_pass.added)} ({_label(largest_pass)}); "
            if largest_pass is not None
            else ""
        )
        + f"{sum(row.seconds for row in rows):.1f} s"
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
        # One deadline for the whole check: inventory, the pack, grandfathering and the
        # verdict.
        deadline = _deadline()
        # Resolved once, so the inventory and the pack measure the same commits.
        resolved = _range(
            Path.cwd(), args.base, args.head, staged=args.staged, deadline=deadline
        )
        blobs = inventory(
            Path.cwd(),
            args.base,
            head=args.head,
            staged=args.staged,
            deadline=deadline,
            resolved=resolved,
        )
        added = added_bytes(
            Path.cwd(),
            args.base,
            head=args.head,
            staged=args.staged,
            deadline=deadline,
            resolved=resolved,
        )
        exempt, failures = judge(
            Path.cwd(), args.base, blobs, ceilings, added=added, deadline=deadline
        )
    except MetadataError as error:
        print(f"GUARD_REFUSED: {error}", file=sys.stderr)
        return 2
    for blob in blobs:
        if _exempt(blob, ceilings.per_blob, exempt):
            print(
                f"GRANDFATHERED: {blob.stored} bytes as Git stores them at {blob.paths!r} "
                f"({blob.object_id}); each path was already over the per-blob ceiling at "
                "the base"
            )
    if failures:
        for failure in failures:
            print(f"REJECT_ADDED_STORAGE: {failure}")
        return 1
    charged = _charged(blobs)
    print(
        f"PASS: {added} bytes added as a thin pack; {len(blobs)} unique checked blobs, "
        f"{len(charged)} new versions "
        f"({sum(blob.checkout for blob in charged.values())} bytes in a checkout); "
        f"ceilings {ceilings.per_blob}/blob as Git stores it and {ceilings.total} total, "
        f"{ceilings.total - added} bytes under it in this clone; a fresh clone, as CI uses, "
        "can read more"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
