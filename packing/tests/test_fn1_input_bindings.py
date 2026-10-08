"""All eight original compressed inputs bind full old candidate and receipt bytes."""

from __future__ import annotations

import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from devtools import acquire_source as acquisition
from devtools import run_negative_controls as controls
from devtools import wand125_fn1_bindings as fn1
from devtools.retained_data import compressed_path, read_retained_bytes


@pytest.fixture
def custody(tmp_path: Path) -> tuple[Path, Path, Path]:
    repository = tmp_path / "private"
    packet = repository / fn1.PACKET.relative_to(fn1.REPO)
    existing = repository / fn1.EXISTING.relative_to(fn1.REPO)
    shutil.copytree(fn1.PACKET, packet)
    (existing / acquisition.RECORD).parent.mkdir(parents=True)
    shutil.copy2(fn1.EXISTING / acquisition.RECORD, existing / acquisition.RECORD)
    for key in fn1.CERTIFICATE_KEYS:
        name = fn1.declared.CERTIFICATES[key].name
        directory = fn1.EXISTING / "square-packing-bounds/certificates" / name
        for relative in (Path("candidate.json"), Path("check2/receipt.json")):
            for source in (directory / relative, compressed_path(directory / relative)):
                if source.is_file():
                    target = existing / source.relative_to(fn1.EXISTING)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
    assert fn1.verify(packet, existing, repository)["input_count"] == 8
    return packet, existing, repository


def _manifest(packet: Path) -> Path:
    return packet / "square-packing-bounds/verification/fn1/input-bindings.json"


def _old(existing: Path, relative: str) -> Path:
    name = fn1.declared.CERTIFICATES[fn1.CERTIFICATE_KEYS[0]].name
    return existing / "square-packing-bounds/certificates" / name / relative


def _write_old(path: Path, data: bytes) -> None:
    if path.is_file():
        path.write_bytes(data)
    else:
        compressed_path(path).write_bytes(gzip.compress(data, mtime=0))


def test_complete_actual_eight_input_chain(custody: tuple[Path, Path, Path]) -> None:
    packet, existing, repository = custody
    result = fn1.verify(packet, existing, repository)
    assert len(result["entries"]) == result["input_count"] == 8
    assert not result["geometry_replay"]
    assert not result["bounds_changed"]
    for row in result["entries"]:
        raw = (
            packet
            / "square-packing-bounds/certificates"
            / row["certificate"]
            / "check2/recorded-input.json.gz"
        )
        assert not raw.is_symlink()
        assert hashlib.sha256(raw.read_bytes()).hexdigest() == row["compressed_sha256"]


@pytest.mark.parametrize("field", ["input_sha256", "file_sha256", "candidate_digest"])
def test_old_receipt_mutation_is_rejected_on_second_call(
    custody: tuple[Path, Path, Path], field: str
) -> None:
    packet, existing, repository = custody
    path = _old(existing, "check2/receipt.json")
    receipt = json.loads(read_retained_bytes(path))
    target = receipt["verifier_summary"]["premises"] if field == "input_sha256" else receipt
    target[field] = "0" * 64
    _write_old(path, json.dumps(receipt).encode())
    with pytest.raises(fn1.BindingError, match=r"original logged|hash changed|mathematical"):
        fn1.verify(packet, existing, repository)


def test_equivalent_candidate_json_does_not_replace_original_bytes(
    custody: tuple[Path, Path, Path],
) -> None:
    packet, existing, repository = custody
    path = _old(existing, "candidate.json")
    data = read_retained_bytes(path)
    changed = json.dumps(json.loads(data), indent=1).encode()
    assert fn1.declared.semantic_digest(json.loads(changed)) == fn1.declared.semantic_digest(
        json.loads(data)
    )
    assert changed != data
    _write_old(path, changed)
    with pytest.raises(fn1.BindingError, match="retained candidate bytes"):
        fn1.verify(packet, existing, repository)


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "outside", "order"])
def test_rebound_manifest_still_requires_exact_full_roster(
    custody: tuple[Path, Path, Path], mutation: str
) -> None:
    packet, existing, repository = custody
    path = _manifest(packet)
    before = path.read_bytes()
    manifest = json.loads(before)
    entries = manifest["entries"]
    if mutation == "missing":
        entries.pop()
    elif mutation == "duplicate":
        entries[-1] = entries[0]
    elif mutation == "outside":
        entries[0]["input_file"] = "../outside.json.gz"
    else:
        entries.reverse()
    data = (json.dumps(manifest, indent=2) + "\n").encode()
    path.write_bytes(data)
    scope_path = "verification/fn1/input-bindings.json"
    source_manifest = packet / acquisition.MANIFEST
    lines = source_manifest.read_text().splitlines()
    source_manifest.write_text(
        "\n".join(
            f"{hashlib.sha256(data).hexdigest()}  ./{scope_path}"
            if line.endswith(f"  ./{scope_path}")
            else line
            for line in lines
        )
        + "\n"
    )
    record_path = packet / acquisition.RECORD
    record = json.loads(record_path.read_text())
    for field in ("retained_total_bytes", "subtree_total_bytes"):
        record["sources"][0][field] += len(data) - len(before)
    record_path.write_text(json.dumps(record))
    assert acquisition.check(packet, repository) == []
    with pytest.raises(fn1.BindingError, match=r"roster|path changed"):
        fn1.verify(packet, existing, repository)


def test_original_compressed_bytes_cannot_be_recompressed(
    custody: tuple[Path, Path, Path],
) -> None:
    packet, existing, repository = custody
    entry = json.loads(_manifest(packet).read_text())["entries"][0]
    raw_path = packet / "square-packing-bounds" / entry["input_file"]
    original = raw_path.read_bytes()
    replacement = gzip.compress(gzip.decompress(original), mtime=0)
    assert replacement != original
    raw_path.write_bytes(replacement)
    with pytest.raises(fn1.BindingError, match="source acquisition differs"):
        fn1.verify(packet, existing, repository)


@pytest.mark.parametrize("outside", [False, True])
def test_complete_input_cannot_be_replaced_by_a_link(
    custody: tuple[Path, Path, Path], tmp_path: Path, *, outside: bool
) -> None:
    packet, existing, repository = custody
    entry = json.loads(_manifest(packet).read_text())["entries"][0]
    raw = packet / "square-packing-bounds" / entry["input_file"]
    destination = (tmp_path if outside else repository) / "borrowed.json.gz"
    destination.write_bytes(raw.read_bytes())
    raw.unlink()
    raw.symlink_to(destination)
    with pytest.raises(fn1.BindingError, match=r"outside repository|independent private"):
        fn1.verify(packet, existing, repository)


def test_actual_worker_carries_every_input_and_refuses_a_receipt_mutant(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    scientific = fn1.private_input_paths()
    assert set(scientific) <= set(controls.COPY_SEPARATELY)
    assert controls.snapshot_source_bytes() <= controls.SNAPSHOT_MAX_BYTES
    worker = tmp_path / "worker"
    copied: list[Path] = []
    original_copy = controls.shutil.copy2

    def counted_copy(source: Any, target: Any, **kwargs: Any) -> Any:
        path = Path(source)
        if path in scientific:
            copied.append(path)
        return original_copy(source, target, **kwargs)

    monkeypatch.setattr(controls.shutil, "copy2", counted_copy)
    controls.clone_tree(worker)
    assert all(copied.count(path) == 1 for path in scientific)
    for path in scientific:
        private = worker / path.relative_to(fn1.REPO)
        assert private.is_file()
        assert not private.is_symlink()
        assert private.read_bytes() == path.read_bytes()
    env = controls.control_environment(worker, tmp_path / "pycache")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [sys.executable, "-m", "devtools.wand125_fn1_bindings"]
    admitted = subprocess.run(
        command,
        cwd=worker / controls.HERE,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=45,
    )
    assert admitted.returncode == 0, admitted.stdout + admitted.stderr
    assert json.loads(admitted.stdout)["input_count"] == 8
    receipt = worker / _old(fn1.EXISTING, "check2/receipt.json").relative_to(fn1.REPO)
    before = receipt.read_bytes()
    record = json.loads(before)
    record["verifier_summary"]["premises"]["input_sha256"] = "0" * 64
    receipt.write_text(json.dumps(record))
    refused = subprocess.run(
        command,
        cwd=worker / controls.HERE,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=45,
    )
    assert refused.returncode != 0
    assert "original logged bytes" in refused.stderr
    receipt.write_bytes(before)
    restored = subprocess.run(
        command,
        cwd=worker / controls.HERE,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=45,
    )
    assert restored.returncode == 0, restored.stdout + restored.stderr
