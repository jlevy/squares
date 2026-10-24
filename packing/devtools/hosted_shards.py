"""Read certificates a packet pins and does not retain from hosted ``tar.xz`` shards.

A source too large for Git (OR-18), as #732's certificates above 1024, is kept as hosted
data: a hosted-data manifest (``packing/hosted/NAME.yaml``, `sqpack.hosted_data`) names each
shard by its repository-relative path, size and SHA-256, and each shard holds the source's
files under their own paths (think-llit's plan, Hosted Custody). The packet that records
the source pins every file by SHA-256 (``acquisition/upstream-subtree.sha256``), so the
custody chain runs from the digest the report states for its index, to the index's digest
of each file, to the packet's pin, to each shard member.

`unpack` asks `sqpack.hosted_data.require` for each shard, which refuses one that is absent
(`sqpack.hosted_data.HostedDataMissingError` names the fetch) or whose size or SHA-256 is
not the manifest's, then streams its members with `tarfile` (`members`). It refuses a member
that is not a regular file (a link, a directory), whose path escapes the shard or repeats,
that the packet does not pin, that is larger than a member may be (`MAX_MEMBER`), or whose
bytes do not have the SHA-256 the packet pins. It bounds the shard's member bytes
(`MAX_UNPACKED`) and, separately, everything the decompressor yields: the stream's
allowance starts at `MAX_HEADERS` and grows by each member's padded size only once that
member is admitted, so a pax or GNU long-name record, which `tarfile` reads whole before
it yields the member it describes, is refused past `MAX_HEADERS` whatever the member
budget (#793's reviews C, C1, and D, D1). A shard that ends inside a member is a
`ShardError` too (D2). After the last shard it refuses a pinned file no shard holds. Each
member is copied in chunks, hashed as it is copied, and published only once its digest
holds, beside the shards' directory in ``DIR-members/STEM/``, keyed by the manifest, only
into a directory Git ignores and inside the repository, with no link below it leading out
(D3); `Hosted.read` reads one back and holds it to its pin again. The source states no size
for its files, so a member's size is bounded and not compared.

From ``packing/`` nothing here reads the network: `sqpack.hosted_data.fetch` does that.
"""

from __future__ import annotations

import hashlib
import io
import lzma
import tarfile
from collections.abc import Buffer, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import IO, override

from strif import atomic_output_file

from sqpack import hosted_data

#: The most a shard's members may hold together: #732's nine shards hold about 273 MB.
MAX_UNPACKED = 2 * 1024**3
#: The most one member may hold: a certificate is at most a few MB.
MAX_MEMBER = 64 * 1024**2
#: What the decompressed stream may hold beyond the admitted members' bytes and padding:
#: each member's header, the end-of-archive blocks, and any pax or long-name record, which
#: `tarfile` reads whole before the member it describes is admitted.
MAX_HEADERS = 16 * 1024**2
#: The size of each read when a member is copied and hashed.
CHUNK = 1 << 20
#: Where a manifest's members are unpacked: beside its shards' directory, never in it, so a
#: later ``hosted_data stage`` of that directory names only the shards.
MEMBERS = "-members"


class ShardError(ValueError):
    """A shard, a member or a read the custody chain does not admit."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ShardError(message)


class _Bounded(io.RawIOBase):
    """A decompressed stream that refuses to yield more than ``limit`` bytes, a limit
    that grows only as members are admitted (`allow`)."""

    def __init__(self, raw: IO[bytes], limit: int, where: str) -> None:
        super().__init__()
        self._raw, self._limit, self._where, self._count = raw, limit, where, 0

    def allow(self, more: int) -> None:
        """Raise the limit by ``more`` bytes: an admitted member's padded size."""
        self._limit += more

    @override
    def readable(self) -> bool:
        return True

    @override
    def readinto(self, buffer: Buffer, /) -> int:
        view = memoryview(buffer).cast("B")
        data = self._raw.read(min(len(view), self._limit + 1 - self._count))
        self._count += len(data)
        _require(
            self._count <= self._limit, f"{self._where}: decompresses past {self._limit} bytes"
        )
        view[: len(data)] = data
        return len(data)


#: What a damaged shard raises from `lzma` or `tarfile`, as a header or a member is read.
_DAMAGED = (lzma.LZMAError, tarfile.TarError, EOFError)


@contextmanager
def _archive(shard: Path, limit: int) -> Iterator[tuple[tarfile.TarFile, _Bounded]]:
    """A shard as a ``tar`` stream and its bound, with at most ``limit`` decompressed
    bytes read until the caller allows more (`_Bounded.allow`)."""
    try:
        with lzma.open(shard) as raw:
            bounded = _Bounded(raw, limit, shard.name)
            with tarfile.open(fileobj=io.BufferedReader(bounded), mode="r|") as archive:
                yield archive, bounded
    except _DAMAGED as error:
        raise ShardError(f"{shard.name}: not a tar.xz shard ({error})") from error


def _entries(
    shard: Path,
    pinned: Mapping[str, str],
    *,
    max_unpacked: int,
    max_member: int,
    max_headers: int,
) -> Iterator[tuple[str, IO[bytes], int]]:
    """Each member a shard may hold, as its path, its stream and its size, before its bytes
    are read; the caller copies the stream (`_copy`) before taking the next."""
    seen: set[str] = set()
    total = 0
    with _archive(shard, max_headers) as (archive, bounded):
        for member in archive:
            name = member.name
            where = f"{shard.name}: {name}"
            parts = PurePosixPath(name)
            _require(
                not parts.is_absolute() and ".." not in parts.parts,
                f"{where}: escapes the shard",
            )
            _require(member.isfile(), f"{where}: not a regular file")
            _require(name not in seen, f"{where}: repeats")
            seen.add(name)
            total += member.size
            _require(total <= max_unpacked, f"{shard.name}: unpacks past {max_unpacked} bytes")
            _require(name in pinned, f"{where}: a member the packet does not pin")
            _require(
                member.size <= max_member,
                f"{where}: {member.size} bytes, more than a member may hold ({max_member})",
            )
            bounded.allow(member.size + (-member.size % 512))
            stream = archive.extractfile(member)
            _require(stream is not None, f"{where}: no bytes")
            assert stream is not None
            yield name, stream, member.size


def _copy(stream: IO[bytes], size: int, out: IO[bytes], where: str, digest: str) -> None:
    """Copy ``size`` bytes of a member to ``out`` in chunks, hashing them as they pass;
    refused unless they are all there and have ``digest``."""
    hasher = hashlib.sha256()
    left = size
    while left:
        try:
            chunk = stream.read(min(CHUNK, left))
        except _DAMAGED as error:
            raise ShardError(f"{where}: not a tar.xz shard ({error})") from error
        _require(chunk, f"{where}: truncated")
        hasher.update(chunk)
        out.write(chunk)
        left -= len(chunk)
    _require(
        hasher.hexdigest() == digest, f"{where}: its bytes are not the ones the packet pins"
    )


def members(
    shard: Path,
    pinned: Mapping[str, str],
    *,
    max_unpacked: int = MAX_UNPACKED,
    max_member: int = MAX_MEMBER,
    max_headers: int = MAX_HEADERS,
) -> Iterator[tuple[str, bytes]]:
    """Each member of a ``tar.xz`` shard, by its path, once it holds: a regular file, inside
    the shard, not repeated, pinned by the packet (``pinned``, path to SHA-256), at most
    ``max_member`` bytes, with the pinned digest; the members' bytes at most
    ``max_unpacked``, and everything decompressed at most ``max_headers`` more."""
    for name, stream, size in _entries(
        shard, pinned, max_unpacked=max_unpacked, max_member=max_member, max_headers=max_headers
    ):
        out = io.BytesIO()
        _copy(stream, size, out, f"{shard.name}: {name}", pinned[name])
        yield name, out.getvalue()


def members_directory(manifest_path: Path, repo: Path) -> Path:
    """Where a manifest's members are unpacked: ``DIR-members/STEM/`` beside ``DIR``, the
    directory of its first shard, under the manifest's stem, so two manifests whose shards
    share a directory never share members (#793's review C, C2)."""
    manifest = hosted_data.load_manifest(manifest_path)
    _require(bool(manifest.objects), f"{manifest_path.name}: the manifest names no shard")
    shards = PurePosixPath(manifest.objects[0].path).parent
    _require(
        shards.name,
        f"{manifest_path.name}: its first shard is not in a directory, so there is none to "
        "unpack its members beside",
    )
    return repo / shards.with_name(shards.name + MEMBERS) / manifest_path.stem


def unpack(
    manifest_path: Path,
    pinned: Mapping[str, str],
    repo: Path,
    *,
    max_unpacked: int = MAX_UNPACKED,
    max_member: int = MAX_MEMBER,
    max_headers: int = MAX_HEADERS,
) -> Path:
    """Unpack every shard a manifest names into its members directory, each shard through
    `sqpack.hosted_data.require` and each member through `_entries`, copied and hashed in
    chunks into a temporary file that is published only once its digest holds. Refused
    unless the shards together hold every pinned file exactly once and the directory is one
    Git ignores, inside the repository. Returns the directory."""
    manifest = hosted_data.load_manifest(manifest_path)
    target = members_directory(manifest_path, repo)
    relative = target.relative_to(repo).as_posix()
    _require(
        target.resolve().is_relative_to(repo.resolve()),
        f"{relative} resolves outside the repository, to {target.resolve()}",
    )
    _require(
        relative in hosted_data.git_ignored(repo, [relative]),
        f"{relative} is not ignored by Git, so its members could be committed",
    )
    inside = target.resolve()
    held: set[str] = set()
    for item in manifest.objects:
        local = hosted_data.require(item.path, manifest_path, repo=repo)
        for name, stream, size in _entries(
            local,
            pinned,
            max_unpacked=max_unpacked,
            max_member=max_member,
            max_headers=max_headers,
        ):
            _require(name not in held, f"{name}: in two shards")
            held.add(name)
            _require(
                (target / name).parent.resolve().is_relative_to(inside),
                f"{relative}: a link below it leads {name} out of the members directory",
            )
            with atomic_output_file(target / name, make_parents=True) as temporary:
                try:
                    with temporary.open("wb") as out:
                        _copy(stream, size, out, f"{local.name}: {name}", pinned[name])
                except BaseException:
                    temporary.unlink(missing_ok=True)
                    raise
    missing = sorted(set(pinned) - held)
    _require(not missing, f"no shard holds {len(missing)} pinned files, {missing[:3]}")
    return target


@dataclass(frozen=True, slots=True)
class Hosted:
    """A hosted manifest's members as one caller reads them, its manifest read once
    (`hosted`): many reads cost one manifest parse (#793's review A, A3)."""

    manifest_path: Path
    pinned: Mapping[str, str]
    repo: Path
    directory: Path

    def read(self, path: str) -> bytes:
        """One pinned file's bytes from the unpacked members, unpacking first if it is not
        there, and held to its pin on every read."""
        _require(path in self.pinned, f"{path}: the packet does not pin it")
        target = self.directory / path
        if not target.is_file():
            unpack(self.manifest_path, self.pinned, self.repo)
        data = target.read_bytes()
        _require(
            hashlib.sha256(data).hexdigest() == self.pinned[path],
            f"{path}: the unpacked bytes are not the ones the packet pins; remove "
            f"{self.directory} and read again",
        )
        return data


def hosted(manifest_path: Path, pinned: Mapping[str, str], repo: Path) -> Hosted:
    """A reader of a hosted manifest's members (`Hosted`)."""
    return Hosted(manifest_path, pinned, repo, members_directory(manifest_path, repo))


def read(manifest_path: Path, pinned: Mapping[str, str], path: str, repo: Path) -> bytes:
    """One pinned file's bytes (`Hosted.read`), for a caller that reads one."""
    return hosted(manifest_path, pinned, repo).read(path)
