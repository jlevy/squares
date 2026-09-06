"""New archives preserve raw evidence; frozen legacy manifests remain verifiable."""

# pyright: reportPrivateUsage=false
from __future__ import annotations

import hashlib
import io
import json
import os
import tarfile
from pathlib import Path

import pytest

from devtools import checkpoint_manifest
from devtools.checkpoint_manifest import _check_one, pack

CHECKPOINTS = (
    Path(__file__).resolve().parents[1] / "benchmarks/validation-efficiency/checkpoints"
)


def _source(tmp_path: Path) -> Path:
    source = tmp_path / "source"
    source.mkdir()
    (source / "run-example.json").write_text(
        json.dumps(
            {
                "commit": "abc123",
                "started_at": "2026-01-01T00:00:00+00:00",
            }
        )
    )
    (source / "command-example.log").write_bytes(b"raw evidence\n")
    (source / "._junk").write_bytes(b"resource fork")
    (source / ".DS_Store").write_bytes(b"metadata")
    return source


def test_pack_preserves_receipts_without_hashes_or_sidecars(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = _source(tmp_path)
    archive = tmp_path / "out.tar.gz"

    def refuse_hash(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("pack must not construct hashes")

    monkeypatch.setattr(checkpoint_manifest.hashlib, "sha256", refuse_hash)
    pack(source, archive, force=False)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["out.tar.gz", "source"]
    with tarfile.open(archive, "r:gz") as tar:
        assert tar.getnames() == ["command-example.log", "run-example.json"]
        for member in tar.getmembers():
            reader = tar.extractfile(member)
            assert reader is not None
            assert reader.read() == (source / member.name).read_bytes()
            assert member.uid == member.gid == 0
            assert member.uname == member.gname == ""


def test_pack_is_reproducible_and_force_is_explicit(tmp_path: Path) -> None:
    source = _source(tmp_path)
    first, second = tmp_path / "first.tar.gz", tmp_path / "second.tar.gz"
    pack(source, first, force=False)
    pack(source, second, force=False)
    expected = first.read_bytes()
    assert second.read_bytes() == expected
    with pytest.raises(SystemExit, match="already exists"):
        pack(source, first, force=False)
    pack(source, first, force=True)
    assert first.read_bytes() == expected


@pytest.mark.parametrize("kind", ["directory", "symlink", "fifo", "metadata-symlink"])
def test_pack_rejects_nonregular_entries_before_writing(tmp_path: Path, kind: str) -> None:
    source = _source(tmp_path)
    entry = source / ("._linked" if kind == "metadata-symlink" else "invalid")
    if kind == "directory":
        entry.mkdir()
        (entry / "lost.log").write_text("must not silently omit")
    elif kind in {"symlink", "metadata-symlink"}:
        entry.symlink_to(source / "command-example.log")
    else:
        os.mkfifo(entry)
    archive = tmp_path / "invalid.tar.gz"
    with pytest.raises(SystemExit, match="regular file"):
        pack(source, archive, force=False)
    assert not archive.exists()


def test_pack_cli_needs_only_source_and_archive(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = _source(tmp_path)
    archive = tmp_path / "cli.tar.gz"
    monkeypatch.setattr("sys.argv", ["checkpoint_manifest", "pack", str(source), str(archive)])
    assert checkpoint_manifest.main() == 0
    assert archive.is_file()
    assert not list(tmp_path.glob("*.manifest.json"))


def _legacy(tmp_path: Path, members: list[tuple[str, bytes]]) -> Path:
    """Create legacy fixtures independently of the archive-only pack command."""
    archive = tmp_path / "legacy.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        for name, kind in members:
            info = tarfile.TarInfo(name)
            info.type = kind
            info.linkname = "payload.log" if kind in {tarfile.SYMTYPE, tarfile.LNKTYPE} else ""
            info.size = 2 if kind == tarfile.REGTYPE else 0
            tar.addfile(info, io.BytesIO(b"ok") if info.size else None)
    files = {
        Path(name).name: {"bytes": 2, "sha256": hashlib.sha256(b"ok").hexdigest()}
        for name, kind in members
        if kind == tarfile.REGTYPE
    }
    manifest = tmp_path / "legacy.manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "archive": archive.name,
                "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
                "files": files,
                "file_count": len(files),
                "uncompressed_bytes": 2 * len(files),
            }
        )
    )
    return manifest


def test_legacy_checker_accepts_old_root_and_dot_prefixed_files(tmp_path: Path) -> None:
    manifest = _legacy(tmp_path, [(".", tarfile.DIRTYPE), ("./payload.log", tarfile.REGTYPE)])
    assert _check_one(manifest) == []


@pytest.mark.parametrize(
    ("name", "kind", "message"),
    [
        ("alias", tarfile.SYMTYPE, "nonregular"),
        ("alias", tarfile.LNKTYPE, "nonregular"),
        ("pipe", tarfile.FIFOTYPE, "nonregular"),
        ("nested", tarfile.DIRTYPE, "nonregular"),
        ("nested/payload.log", tarfile.REGTYPE, "flat"),
        ("../payload.log", tarfile.REGTYPE, "flat"),
        ("/payload.log", tarfile.REGTYPE, "flat"),
    ],
)
def test_legacy_checker_rejects_unrepresented_members(
    tmp_path: Path, name: str, kind: bytes, message: str
) -> None:
    assert any(message in p for p in _check_one(_legacy(tmp_path, [(name, kind)])))


@pytest.mark.parametrize(
    "members",
    [
        [("payload.log", tarfile.REGTYPE), ("./payload.log", tarfile.REGTYPE)],
        [(".", tarfile.DIRTYPE), ("./", tarfile.DIRTYPE)],
    ],
)
def test_legacy_checker_rejects_duplicate_normalized_members(
    tmp_path: Path, members: list[tuple[str, bytes]]
) -> None:
    assert any("duplicate" in p for p in _check_one(_legacy(tmp_path, members)))


def test_legacy_checker_still_catches_checksum_and_file_set_drift(tmp_path: Path) -> None:
    manifest = _legacy(tmp_path, [("payload.log", tarfile.REGTYPE)])
    document = json.loads(manifest.read_text())
    document["archive_sha256"] = "incorrect"
    document["files"] = {}
    manifest.write_text(json.dumps(document))
    problems = _check_one(manifest)
    assert any("SHA-256 mismatch" in p for p in problems)
    assert any("does not list" in p for p in problems)


@pytest.mark.parametrize(
    "manifest", sorted(CHECKPOINTS.glob("*.manifest.json")), ids=lambda p: p.name
)
def test_committed_manifests_verify_without_modification(manifest: Path) -> None:
    before = manifest.read_bytes()
    archive = manifest.parent / json.loads(before)["archive"]
    archive_before = archive.read_bytes()
    assert _check_one(manifest) == []
    assert manifest.read_bytes() == before
    assert archive.read_bytes() == archive_before
