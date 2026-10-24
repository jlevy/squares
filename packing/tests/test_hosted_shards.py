"""Certificates read from hosted ``tar.xz`` shards, each member held to the packet's pin.

`devtools.hosted_shards` is the reader think-llit's plan names for #732's certificates
above 1024 (Hosted Custody, N3). The refusals come first: an absent, altered or truncated
shard (`sqpack.hosted_data.require`); a member that is altered, larger than a member may
be, missing, extra, repeated, a link, outside the shard, or past the unpacked bound; a pax
or long-name record that decompresses past the bound before any member is seen (#793's
review C, C1); a members directory shared by two manifests (C2), beside a shard at the
root (C3) or reached through a symbolic link out of the repository (C4); and a member whose
digest fails as it is copied, which leaves no file behind (A7). The positive reads back,
byte for byte, shards built from certificates of #732's pin 17cc220 that its packet retains.
"""

from __future__ import annotations

import hashlib
import io
import lzma
import subprocess
import tarfile
from collections.abc import Mapping, Sequence
from pathlib import Path

import pytest

from devtools import hosted_shards as shards
from devtools.retained_data import read_retained_bytes
from sqpack import hosted_data

PACKET = Path(__file__).resolve().parents[1] / "resources/web/mishapolk-issue732-2026-10-22"
FOLDER = "certificates/0000-0999"


def _sample(count: int = 6) -> dict[str, bytes]:
    """Certificates of 17cc220 the #732 packet retains, by their source paths."""
    names = sorted(
        path.name.removesuffix(".gz") for path in (PACKET / "source" / FOLDER).iterdir()
    )
    return {
        f"{FOLDER}/{name}": read_retained_bytes(PACKET / "source" / FOLDER / name)
        for name in names[:count]
    }


def _pins(files: Mapping[str, bytes]) -> dict[str, str]:
    return {path: hashlib.sha256(data).hexdigest() for path, data in files.items()}


def _shard(path: Path, files: Sequence[tuple[str, bytes]], **kinds: str) -> Path:
    """A ``tar.xz`` shard of ``files``, sorted, regular, with fixed metadata; ``kinds`` adds
    a member of another kind by name (``symlink`` or ``directory``)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(path, "w:xz") as archive:
        for name, data in files:
            info = tarfile.TarInfo(name)
            info.size, info.mtime, info.mode = len(data), 0, 0o644
            archive.addfile(info, io.BytesIO(data))
        for name, kind in kinds.items():
            info = tarfile.TarInfo(name)
            if kind == "symlink":
                info.type, info.linkname = tarfile.SYMTYPE, "elsewhere"
            else:
                info.type = tarfile.DIRTYPE
            archive.addfile(info)
    return path


def _repo(tmp_path: Path) -> Path:
    """A Git checkout that ignores ``hosted/``, where the shards and members live."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitignore").write_text("hosted/\n", encoding="utf-8")
    return tmp_path


def _manifest(repo: Path, shard_dir: Path) -> Path:
    path = repo / "manifests/test.yaml"
    hosted_data.stage(path, shard_dir, repo, repository="jlevy/squares", tag="data/test-v1")
    return path


def test_a_member_that_breaks_custody_is_refused(tmp_path: Path) -> None:
    """Each member must be a regular file inside the shard, not repeated, pinned, of the
    size the source states, with the pinned digest; the shard unpacks within its bound."""
    files = _sample(3)
    pins = _pins(files)
    first, data = next(iter(files.items()))
    cases: list[tuple[str, list[tuple[str, bytes]], dict[str, str], str]] = [
        ("altered", [(first, data + b"\n")], {}, "not the ones the packet pins"),
        ("extra", [(f"{FOLDER}/n9.cert", data)], {}, "the packet does not pin"),
        ("repeated", [(first, data), (first, data)], {}, "repeats"),
        ("escaping", [(f"../{first}", data)], {}, "escapes the shard"),
        ("absolute", [(f"/{first}", data)], {}, "escapes the shard"),
        ("link", [], {first: "symlink"}, "not a regular file"),
        ("directory", [], {FOLDER: "directory"}, "not a regular file"),
    ]
    for name, members, kinds, message in cases:
        shard = _shard(tmp_path / f"{name}.tar.xz", members, **kinds)
        with pytest.raises(shards.ShardError, match=message):
            list(shards.members(shard, pins))
    shard = _shard(tmp_path / "sized.tar.xz", sorted(files.items()))
    with pytest.raises(shards.ShardError, match="more than a member may hold"):
        list(shards.members(shard, pins, max_member=len(data) - 1))
    with pytest.raises(shards.ShardError, match="unpacks past"):
        list(shards.members(shard, pins, max_unpacked=len(data)))
    assert dict(shards.members(shard, pins)) == files


def test_an_absent_altered_or_truncated_shard_is_refused(tmp_path: Path) -> None:
    """`sqpack.hosted_data.require` holds each shard to its manifest before a member is
    read: absent, it names the fetch; altered or truncated, it refuses the bytes."""
    repo = _repo(tmp_path)
    files = _sample(3)
    shard = _shard(repo / "hosted/shards/sample.tar.xz", sorted(files.items()))
    manifest = _manifest(repo, shard.parent)
    original = shard.read_bytes()
    shard.unlink()
    with pytest.raises(hosted_data.HostedDataMissingError, match="hosted_data fetch"):
        shards.unpack(manifest, _pins(files), repo)
    shard.write_bytes(original[:-1] + bytes([original[-1] ^ 1]))
    with pytest.raises(hosted_data.HostedDataError, match="differs from its manifest"):
        shards.unpack(manifest, _pins(files), repo)
    shard.write_bytes(original[:-7])
    with pytest.raises(hosted_data.HostedDataError, match="differs from its manifest"):
        shards.unpack(manifest, _pins(files), repo)


def test_a_pinned_file_no_shard_holds_or_a_member_in_two_is_refused(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    files = _sample(4)
    names = sorted(files)
    _shard(repo / "hosted/shards/a.tar.xz", [(name, files[name]) for name in names[:2]])
    _shard(repo / "hosted/shards/b.tar.xz", [(name, files[name]) for name in names[1:3]])
    manifest = _manifest(repo, repo / "hosted/shards")
    with pytest.raises(shards.ShardError, match="in two shards"):
        shards.unpack(manifest, _pins(files), repo)
    _shard(repo / "hosted/shards/b.tar.xz", [(names[2], files[names[2]])])
    manifest = _manifest(repo, repo / "hosted/shards")
    with pytest.raises(shards.ShardError, match="no shard holds 1 pinned files"):
        shards.unpack(manifest, _pins(files), repo)


def test_members_unpack_only_where_git_ignores_them(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    (repo / ".gitignore").write_text("hosted/shards/*.tar.xz\n", encoding="utf-8")
    files = _sample(2)
    shard = _shard(repo / "hosted/shards/sample.tar.xz", sorted(files.items()))
    manifest = _manifest(repo, shard.parent)
    with pytest.raises(shards.ShardError, match="is not ignored by Git"):
        shards.unpack(manifest, _pins(files), repo)


def test_shards_of_17cc220_s_certificates_read_back_byte_for_byte(tmp_path: Path) -> None:
    """Two shards built from certificates of 17cc220 the #732 packet retains: every member
    reads back as the retained bytes, each held to its pin again on every read, and an
    unpacked member changed afterwards is refused rather than read."""
    repo = _repo(tmp_path)
    files = _sample(8)
    names = sorted(files)
    _shard(repo / "hosted/shards/one.tar.xz", [(name, files[name]) for name in names[:5]])
    _shard(repo / "hosted/shards/two.tar.xz", [(name, files[name]) for name in names[5:]])
    manifest = _manifest(repo, repo / "hosted/shards")
    pins = _pins(files)
    for name in names:
        assert shards.read(manifest, pins, name, repo) == files[name]
    target = shards.members_directory(manifest, repo) / names[0]
    target.write_bytes(files[names[0]] + b" ")
    with pytest.raises(shards.ShardError, match=r"unpacked bytes are not the ones.*read again"):
        shards.read(manifest, pins, names[0], repo)
    with pytest.raises(shards.ShardError, match="the packet does not pin it"):
        shards.read(manifest, pins, f"{FOLDER}/n9.cert", repo)


def _bomb(path: Path, kind: str, payload: int, good: tuple[str, bytes]) -> Path:
    """A shard whose first record is ``payload`` bytes that `tarfile` reads whole before it
    yields a member, a pax ``comment`` or a GNU long name, followed by a good member; each
    is streamed through the compressor, so a large payload costs little to build (as the
    proofs of concept of #793's review C, C1)."""
    name, data = good
    member = tarfile.TarInfo(name)
    member.size, member.mtime = len(data), 0
    if kind == "pax-comment":
        body = len(" comment=") + payload + 1
        length = body + len(str(body))
        length += len(str(length)) - len(str(body))
        record = tarfile.TarInfo("././@PaxHeader")
        record.type, record.size, record.mtime = tarfile.XHDTYPE, length, 0
        head, fill, tail = f"{length} comment=".encode(), b"a", b"\n"
    else:
        length = payload
        record = tarfile.TarInfo("././@LongLink")
        record.type, record.size, record.mtime = tarfile.GNUTYPE_LONGNAME, length, 0
        head, fill, tail = b"", b"\0", b""
    compressor = lzma.LZMACompressor(format=lzma.FORMAT_XZ, preset=0)
    pad = b"\0" * (-length % 512)
    with path.open("wb") as out:
        out.write(compressor.compress(record.tobuf(format=tarfile.GNU_FORMAT) + head))
        chunk, left = fill * (1 << 20), payload
        while left:
            out.write(compressor.compress(chunk[: min(left, len(chunk))]))
            left -= min(left, len(chunk))
        trailer = member.tobuf(format=tarfile.GNU_FORMAT) + data + b"\0" * (-len(data) % 512)
        out.write(compressor.compress(tail + pad + trailer + b"\0" * 1024))
        out.write(compressor.flush())
    return path


def test_a_record_that_decompresses_past_the_bound_is_refused(tmp_path: Path) -> None:
    """Review C, C1: `tarfile` reads a pax record or a GNU long name whole before it yields
    the member it describes, so a bound on the members' sizes alone admitted a shard of a
    few kilobytes that decompressed to gigabytes, and a pax comment was accepted with the
    pinned bytes. Everything the decompressor yields is now bounded: each record of 4 MiB is
    refused under a 1 MiB allowance, and the good member alone reads under the same one."""
    name, data = next(iter(_sample(1).items()))
    pins = _pins({name: data})
    bounds = {"max_unpacked": 1 << 20, "max_headers": 1 << 20}
    for kind in ("pax-comment", "longname"):
        shard = _bomb(tmp_path / f"{kind}.tar.xz", kind, 4 << 20, (name, data))
        assert shard.stat().st_size < 64 * 1024
        with pytest.raises(shards.ShardError, match="decompresses past 2097152 bytes"):
            list(shards.members(shard, pins, **bounds))
    small = _bomb(tmp_path / "small-comment.tar.xz", "pax-comment", 100, (name, data))
    assert dict(shards.members(small, pins, **bounds)) == {name: data}
    good = _shard(tmp_path / "good.tar.xz", [(name, data)])
    assert dict(shards.members(good, pins, **bounds)) == {name: data}
    garbage = tmp_path / "garbage.tar.xz"
    garbage.write_bytes(b"not xz")
    with pytest.raises(shards.ShardError, match=r"not a tar\.xz shard"):
        list(shards.members(garbage, pins))


def test_two_manifests_sharing_a_shard_directory_keep_their_own_members(
    tmp_path: Path,
) -> None:
    """Review C, C2: two manifests whose shards share a directory unpack into members
    directories of their own, so neither overwrites the other's members at a path both
    hold with other bytes."""
    repo = _repo(tmp_path)
    name, data = next(iter(_sample(1).items()))
    other = data + b"# another pin\n"
    directory = repo / "hosted/shards"
    _shard(directory / "a.tar.xz", [(name, data)])
    first = repo / "manifests/first.yaml"
    hosted_data.stage(first, directory, repo, repository="jlevy/squares", tag="data/a-v1")
    (directory / "a.tar.xz").rename(repo / "a.tar.xz.kept")
    _shard(directory / "b.tar.xz", [(name, other)])
    second = repo / "manifests/second.yaml"
    hosted_data.stage(second, directory, repo, repository="jlevy/squares", tag="data/b-v1")
    (repo / "a.tar.xz.kept").rename(directory / "a.tar.xz")
    assert shards.members_directory(first, repo) != shards.members_directory(second, repo)
    assert shards.read(first, _pins({name: data}), name, repo) == data
    assert shards.read(second, _pins({name: other}), name, repo) == other
    assert shards.read(first, _pins({name: data}), name, repo) == data


def test_a_shard_at_the_root_or_a_members_link_out_of_the_repository_is_refused(
    tmp_path: Path,
) -> None:
    """Review C, C3 and C4: a manifest whose first shard sits at the repository root has no
    directory to unpack beside, refused as a `ShardError`; and a members directory reached
    through an untracked symbolic link that leaves the repository is refused, though Git
    ignores it, so no member is written outside."""
    repo = _repo(tmp_path / "repo")
    name, data = next(iter(_sample(1).items()))
    root = _shard(repo / "root.tar.xz", [(name, data)])
    item = hosted_data.HostedObject(
        "root.tar.xz",
        "root.tar.xz",
        root.stat().st_size,
        hashlib.sha256(root.read_bytes()).hexdigest(),
    )
    at_root = repo / "manifests/root.yaml"
    at_root.parent.mkdir(parents=True)
    at_root.write_text(
        hosted_data.render_manifest(
            hosted_data.Manifest("jlevy/squares", "data/root-v1", (item,)), at_root
        ),
        encoding="utf-8",
    )
    with pytest.raises(shards.ShardError, match="first shard is not in a directory"):
        shards.read(at_root, _pins({name: data}), name, repo)
    _shard(repo / "hosted/shards/one.tar.xz", [(name, data)])
    manifest = _manifest(repo, repo / "hosted/shards")
    outside = tmp_path / "outside"
    outside.mkdir()
    members = shards.members_directory(manifest, repo)
    members.parent.mkdir(parents=True)
    members.symlink_to(outside, target_is_directory=True)
    with pytest.raises(shards.ShardError, match="resolves outside the repository"):
        shards.read(manifest, _pins({name: data}), name, repo)
    assert list(outside.iterdir()) == []


def test_a_member_whose_digest_fails_leaves_nothing_behind(tmp_path: Path) -> None:
    """Review A, A7: each member is copied and hashed in chunks into a temporary file, which
    is published only once its digest holds. A member with other bytes than its pin is
    refused, and neither it nor a temporary file is left in the members directory; the
    member before it, which held, stays."""
    repo = _repo(tmp_path)
    files = _sample(2)
    (good, data), (bad, other) = sorted(files.items())
    _shard(repo / "hosted/shards/one.tar.xz", [(good, data), (bad, other + b" ")])
    manifest = _manifest(repo, repo / "hosted/shards")
    with pytest.raises(shards.ShardError, match="not the ones the packet pins"):
        shards.unpack(manifest, _pins(files), repo)
    directory = shards.members_directory(manifest, repo)
    left = sorted(
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*")
        if path.is_file()
    )
    assert left == [good]
