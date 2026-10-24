"""Certificates read from hosted ``tar.xz`` shards, each member held to the packet's pin.

`devtools.hosted_shards` is the reader think-llit's plan names for #732's certificates
above 1024 (Hosted Custody, N3). The refusals come first: an absent, altered or truncated
shard (`sqpack.hosted_data.require`), and a member that is altered, of another size than
the source states, missing, extra, repeated, a link, outside the shard, or past the
unpacked bound. The positive reads back, byte for byte, shards built from certificates of
#732's pin 17cc220 that its packet retains.
"""

from __future__ import annotations

import hashlib
import io
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
    with pytest.raises(shards.ShardError, match="bytes in its header, the source states"):
        list(shards.members(shard, pins, sizes={first: len(data) + 1}))
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
    target = shards.members_directory(hosted_data.load_manifest(manifest), repo) / names[0]
    target.write_bytes(files[names[0]] + b" ")
    with pytest.raises(shards.ShardError, match="unpacked bytes are not the ones"):
        shards.read(manifest, pins, names[0], repo)
    with pytest.raises(shards.ShardError, match="the packet does not pin it"):
        shards.read(manifest, pins, f"{FOLDER}/n9.cert", repo)
