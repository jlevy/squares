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
that the packet does not pin, whose header size differs from a size the source states, or
whose bytes do not have the SHA-256 the packet pins; it bounds the shard's unpacked total
(`MAX_UNPACKED`), and after the last shard it refuses a pinned file no shard holds. Each
member is written beside the shards' directory, in ``DIR-members/``, only once its digest
holds, and only into a directory Git ignores; `read` reads one back and holds it to its pin
again.

From ``packing/`` nothing here reads the network: `sqpack.hosted_data.fetch` does that.
"""

from __future__ import annotations

import hashlib
import tarfile
from collections.abc import Iterator, Mapping
from pathlib import Path, PurePosixPath

from strif import atomic_output_file

from sqpack import hosted_data

#: The most a shard may unpack to: #732's nine shards hold about 273 MB together.
MAX_UNPACKED = 2 * 1024**3
#: Where a manifest's members are unpacked: beside its shards' directory, never in it, so a
#: later ``hosted_data stage`` of that directory names only the shards.
MEMBERS = "-members"


class ShardError(ValueError):
    """A shard, a member or a read the custody chain does not admit."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ShardError(message)


def members(
    shard: Path,
    pinned: Mapping[str, str],
    *,
    sizes: Mapping[str, int] | None = None,
    max_unpacked: int = MAX_UNPACKED,
) -> Iterator[tuple[str, bytes]]:
    """Each member of a ``tar.xz`` shard, by its path, once it holds: a regular file, inside
    the shard, not repeated, pinned by the packet (``pinned``, path to SHA-256), of the size
    the source states where it states one (``sizes``), with the pinned digest; the shard's
    unpacked total at most ``max_unpacked``."""
    seen: set[str] = set()
    total = 0
    with tarfile.open(shard, "r:xz") as archive:
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
            if sizes is not None and name in sizes:
                _require(
                    member.size == sizes[name],
                    f"{where}: {member.size} bytes in its header, the source states "
                    f"{sizes[name]}",
                )
            stream = archive.extractfile(member)
            _require(stream is not None, f"{where}: no bytes")
            assert stream is not None
            data = stream.read()
            _require(len(data) == member.size, f"{where}: truncated")
            _require(
                hashlib.sha256(data).hexdigest() == pinned[name],
                f"{where}: its bytes are not the ones the packet pins",
            )
            yield name, data


def members_directory(manifest: hosted_data.Manifest, repo: Path) -> Path:
    """Where a manifest's members are unpacked: ``DIR-members/`` beside ``DIR``, the
    directory of its first shard."""
    _require(bool(manifest.objects), "the manifest names no shard")
    shards = Path(manifest.objects[0].path).parent
    return repo / shards.with_name(shards.name + MEMBERS)


def unpack(
    manifest_path: Path,
    pinned: Mapping[str, str],
    repo: Path,
    *,
    sizes: Mapping[str, int] | None = None,
    max_unpacked: int = MAX_UNPACKED,
) -> Path:
    """Unpack every shard a manifest names into its members directory, each shard through
    `sqpack.hosted_data.require` and each member through `members`; refused unless the
    shards together hold every pinned file exactly once and the directory is one Git
    ignores. Returns the directory."""
    manifest = hosted_data.load_manifest(manifest_path)
    target = members_directory(manifest, repo)
    relative = target.relative_to(repo).as_posix()
    _require(
        relative in hosted_data.git_ignored(repo, [relative]),
        f"{relative} is not ignored by Git, so its members could be committed",
    )
    held: set[str] = set()
    for item in manifest.objects:
        local = hosted_data.require(item.path, manifest_path, repo=repo)
        for name, data in members(local, pinned, sizes=sizes, max_unpacked=max_unpacked):
            _require(name not in held, f"{name}: in two shards")
            held.add(name)
            path = target / name
            path.parent.mkdir(parents=True, exist_ok=True)
            with atomic_output_file(path, make_parents=True) as temporary:
                temporary.write_bytes(data)
    missing = sorted(set(pinned) - held)
    _require(not missing, f"no shard holds {len(missing)} pinned files, {missing[:3]}")
    return target


def read(manifest_path: Path, pinned: Mapping[str, str], path: str, repo: Path) -> bytes:
    """One pinned file's bytes from the unpacked members, unpacking first if it is not
    there, and held to its pin on every read."""
    _require(path in pinned, f"{path}: the packet does not pin it")
    target = members_directory(hosted_data.load_manifest(manifest_path), repo) / path
    if not target.is_file():
        unpack(manifest_path, pinned, repo)
    data = target.read_bytes()
    _require(
        hashlib.sha256(data).hexdigest() == pinned[path],
        f"{path}: the unpacked bytes are not the ones the packet pins",
    )
    return data
