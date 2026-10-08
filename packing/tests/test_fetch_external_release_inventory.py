"""Generic inbound assets remain identity-bound and cannot issue proof receipts."""

from __future__ import annotations

import copy
import hashlib
import json
import threading
import time
from pathlib import Path
from typing import Any, cast

import pytest

from devtools import fetch_external_release_inventory as tool
from sqpack.hosted_data import HostedDataError, ReleaseClient


class FakeClient:
    def __init__(self, payloads: dict[str, bytes]) -> None:
        self.payloads = payloads
        self.calls: list[str] = []

    def download(self, repository: str, tag: str, asset: str, destination: Path) -> None:
        assert repository == "example/proofs"
        assert tag == "legacy-public-tag"
        self.calls.append(asset)
        _ = destination.write_bytes(self.payloads[asset])


def fixture(count: int = 2) -> tuple[dict[str, Any], FakeClient]:
    payloads = {f"object-{i}.json.gz": f"bytes-{i}".encode() for i in range(count)}
    rows = [
        {
            "path": "bundle/" + name,
            "asset": name,
            "size": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "url": "https://github.com/example/proofs/releases/download/legacy-public-tag/"
            + name,
        }
        for name, raw in payloads.items()
    ]
    return {
        "schema": tool.SCHEMA,
        "repository": "example/proofs",
        "tag": "legacy-public-tag",
        "objects": rows,
        "object_count": count,
        "compressed_bytes": sum(len(raw) for raw in payloads.values()),
    }, FakeClient(payloads)


def save(tmp_path: Path, data: dict[str, Any]) -> tuple[Path, str]:
    p = tmp_path / "inventory.json"
    raw = json.dumps(data).encode()
    _ = p.write_bytes(raw)
    return p, hashlib.sha256(raw).hexdigest()


def acquire(tmp_path: Path, data: dict[str, Any], client: FakeClient) -> dict[str, Any]:
    p, digest = save(tmp_path, data)
    return tool.acquire(
        p,
        digest,
        tmp_path / "cache",
        1 << 20,
        deadline=time.monotonic() + 30,
        client=cast(ReleaseClient, client),
        external_root=tmp_path,
    )


def test_legacy_tag_exact_atomic_assets_and_present_resume(tmp_path: Path) -> None:
    data, client = fixture()
    receipt = acquire(tmp_path, data, client)
    assert receipt["status"] == "ACQUIRED"
    assert receipt["HostedData_v1_conforming"] is False
    assert receipt["full_verification_passed"] is False
    assert [r["path"] for r in receipt["actions"]] == [r["path"] for r in data["objects"]]
    assert all(r["action"] == "fetched" for r in receipt["actions"])
    again = acquire(tmp_path, data, client)
    assert all(r["action"] == "present" for r in again["actions"])
    assert len(client.calls) == 2


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("path", "../escape"),
        ("path", "/escape"),
        ("path", "bundle//bad"),
        ("asset", "../bad"),
        ("size", True),
        ("sha256", "not-a-sha"),
        ("url", "https://elsewhere.invalid/data"),
    ],
)
def test_bad_object_rosters_refuse_before_any_download(
    tmp_path: Path,
    field: str,
    value: Any,
) -> None:
    data, client = fixture()
    data["objects"][0][field] = value
    with pytest.raises(ValueError, match=r"path|asset|size|SHA|URL"):
        _ = acquire(tmp_path, data, client)
    assert not client.calls


def test_duplicate_count_total_and_budget_refuse(tmp_path: Path) -> None:
    data, _ = fixture()
    duplicate = copy.deepcopy(data)
    duplicate["objects"][1] = duplicate["objects"][0]
    with pytest.raises(ValueError, match="duplicate"):
        _ = tool.manifest(duplicate, tmp_path, 100)
    for key in ("object_count", "compressed_bytes"):
        changed = copy.deepcopy(data)
        changed[key] += 1
        with pytest.raises(ValueError, match="differ"):
            _ = tool.manifest(changed, tmp_path, 100)
    with pytest.raises(ValueError, match="byte ceiling"):
        _ = tool.manifest(data, tmp_path, 1)


def test_safe_external_root_and_symlink_escape(tmp_path: Path) -> None:
    data, client = fixture()
    p, digest = save(tmp_path, data)
    with pytest.raises(ValueError, match="outside external"):
        _ = tool.acquire(
            p,
            digest,
            tmp_path.parent / "escape",
            100,
            deadline=time.monotonic() + 30,
            client=cast(ReleaseClient, client),
            external_root=tmp_path,
        )
    cache = tmp_path / "cache"
    cache.mkdir()
    (cache / "bundle").symlink_to(tmp_path.parent, target_is_directory=True)
    with pytest.raises(ValueError, match="symlink"):
        _ = tool.manifest(data, cache, 100)
    assert not client.calls


def test_size_or_sha_failure_never_installs_bad_asset(tmp_path: Path) -> None:
    data, client = fixture(1)
    client.payloads["object-0.json.gz"] = b"bad"
    with pytest.raises(HostedDataError, match="refused"):
        _ = acquire(tmp_path, data, client)
    assert not (tmp_path / "cache/bundle/object-0.json.gz").exists()
    cache_file = tmp_path / "cache/bundle/object-0.json.gz"
    _ = cache_file.write_bytes(b"unique-existing-evidence")
    with pytest.raises(HostedDataError, match="present but differs"):
        _ = acquire(tmp_path, data, client)
    assert cache_file.read_bytes() == b"unique-existing-evidence"


def test_inventory_identity_changes_refuse(tmp_path: Path) -> None:
    data, client = fixture(1)
    p, digest = save(tmp_path, data)
    with pytest.raises(ValueError, match="inventory bytes"):
        _ = tool.read_inventory(p, "0" * 64)

    class Mutator(FakeClient):
        def download(self, repository: str, tag: str, asset: str, destination: Path) -> None:
            super().download(repository, tag, asset, destination)
            _ = p.write_bytes(b"changed")

    with pytest.raises(ValueError, match="inventory bytes"):
        _ = tool.acquire(
            p,
            digest,
            tmp_path / "cache",
            100,
            deadline=time.monotonic() + 30,
            client=cast(ReleaseClient, Mutator(client.payloads)),
            external_root=tmp_path,
        )


def test_four_workers_parallel_different_atomic_destinations(tmp_path: Path) -> None:
    data, client = fixture(4)
    barrier = threading.Barrier(4)

    class Parallel(FakeClient):
        def download(self, repository: str, tag: str, asset: str, destination: Path) -> None:
            _ = barrier.wait(timeout=5)
            super().download(repository, tag, asset, destination)

    result = acquire(tmp_path, data, Parallel(client.payloads))
    assert result["objects"] == 4
    assert result["acquisition_workers"] == 4


def test_wall_free_space_and_inventory_caps(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    data, client = fixture()
    p, digest = save(tmp_path, data)
    with pytest.raises(ValueError, match="wall ceiling"):
        _ = tool.acquire(
            p,
            digest,
            tmp_path / "cache",
            100,
            deadline=time.monotonic() - 1,
            client=cast(ReleaseClient, client),
            external_root=tmp_path,
        )
    monkeypatch.setattr(tool, "MIN_FREE_RESERVE", 1 << 100)
    with pytest.raises(ValueError, match="free-space"):
        _ = acquire(tmp_path, data, client)
    monkeypatch.setattr(tool, "INPUT_LIMIT", 1)
    with pytest.raises(ValueError, match="inventory byte"):
        _ = tool.read_inventory(p, digest)
    assert not client.calls


@pytest.mark.parametrize("workers", [0, 5, True])
def test_worker_ceiling_before_download(tmp_path: Path, workers: Any) -> None:
    data, client = fixture()
    p, digest = save(tmp_path, data)
    with pytest.raises(ValueError, match="one to four"):
        _ = tool.acquire(
            p,
            digest,
            tmp_path / "cache",
            100,
            deadline=time.monotonic() + 30,
            client=cast(ReleaseClient, client),
            external_root=tmp_path,
            workers=workers,
        )
    assert not client.calls


def test_cli_existing_output_refuses_before_network(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data, client = fixture(1)
    p, digest = save(tmp_path, data)
    monkeypatch.setattr(tool, "GhClient", lambda: cast(ReleaseClient, client))
    output = tmp_path / "receipt.json"
    args = [
        "--inventory",
        str(p),
        "--inventory-sha256",
        digest,
        "--cache-root",
        str(tmp_path / "cache"),
        "--external-root",
        str(tmp_path),
        "--max-bytes",
        "100",
        "--output",
        str(output),
    ]
    assert tool.main(args) == 0
    assert json.loads(output.read_bytes())["full_verification_passed"] is False
    with pytest.raises(ValueError, match="already exists"):
        _ = tool.main(args)
    assert len(client.calls) == 1
