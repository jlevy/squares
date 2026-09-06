"""Checkpoint archives stay paired with their manifests, and the tool that pairs them.

The standing drift guard (test_committed_manifests_verify) runs `check` against every
committed manifest under `benchmarks/validation-efficiency/checkpoints/` and fails when
an archive or its manifest drifts. The tool tests (pack and check round-trip) use
fabricated fixtures so they cannot rot when the committed archives change.
"""

# _check_one is the unit under test; reaching for it rather than shelling out to the CLI
# is the same pattern test_gate_budgets.py uses for coverage_problems.
# pyright: reportPrivateUsage=false
from __future__ import annotations

import json
from pathlib import Path

import pytest

from devtools.checkpoint_manifest import _check_one, pack

CHECKPOINTS = (
    Path(__file__).resolve().parents[1] / "benchmarks" / "validation-efficiency" / "checkpoints"
)


def _fake_directory(tmp_path: Path) -> Path:
    """A minimal checkpoint directory with a run receipt, two step receipts, and junk."""
    d = tmp_path / "source"
    d.mkdir()

    run = {
        "available_cpus": 4,
        "commit": "abc123",
        "dirty_diff_sha256": "0" * 64,
        "inner_jobs": 1,
        "jobs": 1,
        "platform": "Linux-test",
        "python": "3.14.0",
        "run_id": "deadbeef",
        "started_at": "2026-01-01T00:00:00+00:00",
    }
    (d / "run-deadbeef.json").write_text(json.dumps(run), encoding="utf-8")

    for i in range(2):
        step = {"status": "passed", "name": f"step-{i}"}
        (d / f"step-{i:04d}.json").write_text(json.dumps(step), encoding="utf-8")

    (d / "command-aaaa.log").write_text("ok\n", encoding="utf-8")
    # Junk that pack must skip.
    (d / "._junk").write_text("resource fork", encoding="utf-8")
    (d / ".DS_Store").write_bytes(b"\x00\x00\x00\x01")
    return d


def test_pack_produces_archive_and_manifest(tmp_path: Path) -> None:
    """Pack on a fabricated directory produces a clean archive and a valid manifest."""
    source = _fake_directory(tmp_path)
    archive = tmp_path / "out.tar.gz"

    pack(
        source,
        archive,
        scope="test scope",
        wall_seconds=10.0,
        wall_seconds_source="test",
        failure=None,
        force=False,
    )

    manifest_path = tmp_path / "out.manifest.json"
    assert archive.is_file()
    assert manifest_path.is_file()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "._junk" not in manifest["files"]
    assert ".DS_Store" not in manifest["files"]
    assert manifest["file_count"] == len(manifest["files"])
    assert manifest["outcome"]["passed"] == 2
    assert manifest["outcome"]["steps"] == 2
    assert manifest["scope"] == "test scope"
    assert manifest["provenance"]["commit"] == "abc123"

    # check must pass on the pair.
    assert _check_one(manifest_path) == []


def test_pack_is_byte_reproducible(tmp_path: Path) -> None:
    """Two packs of the same directory produce identical archives."""
    source = _fake_directory(tmp_path)
    a1 = tmp_path / "a1.tar.gz"
    a2 = tmp_path / "a2.tar.gz"

    pack(
        source,
        a1,
        scope="s",
        wall_seconds=1.0,
        wall_seconds_source="t",
        failure=None,
        force=False,
    )
    pack(
        source,
        a2,
        scope="s",
        wall_seconds=1.0,
        wall_seconds_source="t",
        failure=None,
        force=False,
    )

    assert a1.read_bytes() == a2.read_bytes()


def test_check_catches_corrupted_archive(tmp_path: Path) -> None:
    """A single flipped byte in the archive makes check fail and name the problem."""
    source = _fake_directory(tmp_path)
    archive = tmp_path / "bad.tar.gz"
    pack(
        source,
        archive,
        scope="s",
        wall_seconds=1.0,
        wall_seconds_source="t",
        failure=None,
        force=False,
    )

    # Corrupt one byte near the end of the archive.
    data = bytearray(archive.read_bytes())
    data[-20] ^= 0xFF
    archive.write_bytes(bytes(data))

    problems = _check_one(tmp_path / "bad.manifest.json")
    assert len(problems) > 0
    assert any("SHA-256" in p or "sha256" in p or "cannot read" in p for p in problems)


def test_check_catches_missing_file(tmp_path: Path) -> None:
    """Removing a file from the manifest makes check fail."""
    source = _fake_directory(tmp_path)
    archive = tmp_path / "missing.tar.gz"
    pack(
        source,
        archive,
        scope="s",
        wall_seconds=1.0,
        wall_seconds_source="t",
        failure=None,
        force=False,
    )

    manifest_path = tmp_path / "missing.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    # Remove one file from the manifest.
    removed = min(manifest["files"].keys())
    del manifest["files"][removed]
    manifest["file_count"] -= 1
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )

    problems = _check_one(manifest_path)
    assert any(removed in p for p in problems)


def test_pack_refuses_overwrite_without_force(tmp_path: Path) -> None:
    """Retained evidence is not silently overwritten."""
    source = _fake_directory(tmp_path)
    archive = tmp_path / "guard.tar.gz"
    pack(
        source,
        archive,
        scope="s",
        wall_seconds=1.0,
        wall_seconds_source="t",
        failure=None,
        force=False,
    )

    with pytest.raises(SystemExit, match="already exists"):
        pack(
            source,
            archive,
            scope="s",
            wall_seconds=1.0,
            wall_seconds_source="t",
            failure=None,
            force=False,
        )


def _committed_manifests() -> list[Path]:
    return sorted(CHECKPOINTS.glob("*.manifest.json"))


@pytest.mark.parametrize(
    "manifest",
    _committed_manifests(),
    ids=[p.name for p in _committed_manifests()],
)
def test_committed_manifests_verify(manifest: Path) -> None:
    """Standing drift guard: every committed manifest passes check."""
    problems = _check_one(manifest)
    assert problems == [], "\n".join(problems)
