"""Acquire identity-bound public release assets; not a HostedData-v1 manifest or proof."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, cast
from urllib.parse import quote

from sqpack import retained_json
from sqpack.hosted_data import Fetched, GhClient, HostedObject, Manifest, ReleaseClient, fetch

SCHEMA = "external-release-acquisition-inventory/v1"
RECEIPT_SCHEMA = "external-release-acquisition/v1"
INPUT_LIMIT, OUTPUT_LIMIT, MAX_OBJECTS = 1 << 20, 1 << 20, 1000
SHA = re.compile(r"[0-9a-f]{64}\Z")
REPOSITORY = re.compile(r"[A-Za-z0-9-]+/[A-Za-z0-9._-]+\Z")
ASSET = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
RELATIVE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9._/-]*\Z")
MIN_FREE_RESERVE = 64 << 20


def require(condition: Any, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_inventory(path: Path, expected_sha256: str) -> tuple[dict[str, Any], bytes]:
    require(bool(SHA.fullmatch(expected_sha256)), "inventory SHA required")
    with path.open("rb") as stream:
        raw = stream.read(INPUT_LIMIT + 1)
    require(len(raw) <= INPUT_LIMIT, "inventory byte ceiling")
    require(hashlib.sha256(raw).hexdigest() == expected_sha256, "inventory bytes differ")
    data = json.loads(raw)
    require(type(data) is dict and data.get("schema") == SCHEMA, "external inventory schema")
    return cast(dict[str, Any], data), raw


def manifest(data: dict[str, Any], cache: Path, max_bytes: int) -> Manifest:
    require(type(max_bytes) is int and 0 < max_bytes <= 1 << 30, "finite acquisition byte cap")
    repository, tag = data["repository"], data["tag"]
    require(type(repository) is str and bool(REPOSITORY.fullmatch(repository)), "repository")
    require(
        type(tag) is str and 0 < len(tag) <= 256 and not any(ord(c) < 32 for c in tag),
        "release tag",
    )
    rows = data["objects"]
    require(type(rows) is list and 1 <= len(rows) <= MAX_OBJECTS, "bounded object roster")
    objects: list[HostedObject] = []
    paths: set[str] = set()
    assets: set[str] = set()
    total = 0
    cache = cache.resolve()
    for row in rows:
        require(type(row) is dict, "object record")
        row = cast(dict[str, Any], row)
        path, asset, size, digest = (row[k] for k in ("path", "asset", "size", "sha256"))
        require(
            type(path) is str
            and 0 < len(path) <= 4096
            and bool(RELATIVE.fullmatch(path))
            and all(part not in ("", ".", "..") for part in path.split("/")),
            "plain relative cache path required",
        )
        require(type(asset) is str and bool(ASSET.fullmatch(asset)), "plain asset name")
        require(type(size) is int and 0 < size < 2 << 30, "bounded object size")
        require(type(digest) is str and bool(SHA.fullmatch(digest)), "object SHA required")
        require(path not in paths and asset not in assets, "duplicate object path or asset")
        require(
            (cache / path).resolve().is_relative_to(cache), "cache path escapes through symlink"
        )
        expected_url = (
            f"https://github.com/{repository}/releases/download/{quote(tag, safe='')}/{asset}"
        )
        require(row.get("url") == expected_url, "release URL differs from repository/tag/asset")
        total += size
        require(total <= max_bytes, "acquisition byte ceiling")
        paths.add(path)
        assets.add(asset)
        objects.append(HostedObject(path, asset, size, digest))
    require(data.get("object_count") == len(objects), "object count differs")
    require(type(data.get("object_count")) is int, "typed object count")
    require(
        type(data.get("compressed_bytes")) is int and data["compressed_bytes"] == total,
        "total bytes differ",
    )
    return Manifest(repository, tag, tuple(objects))


class TimedClient:
    """Cooperative boundaries; the outer supervisor must bound a blocked network call."""

    def __init__(self, client: ReleaseClient, deadline: float) -> None:
        self.client, self.deadline = client, deadline
        self.stopped = threading.Event()

    def download(self, repository: str, tag: str, asset: str, destination: Path) -> None:
        self.tick()
        self.client.download(repository, tag, asset, destination)
        self.tick()

    def tick(self) -> None:
        require(not self.stopped.is_set(), "acquisition stopped after failure")
        require(time.monotonic() < self.deadline, "acquisition cooperative wall ceiling")


def acquire(
    inventory: Path,
    expected_sha256: str,
    cache: Path,
    max_bytes: int,
    *,
    deadline: float,
    client: ReleaseClient,
    external_root: Path,
    workers: int = 4,
) -> dict[str, Any]:
    require(type(workers) is int and 1 <= workers <= 4, "one to four acquisition workers")
    require(external_root.is_dir(), "external scratch root unavailable")
    require(
        cache.resolve().is_relative_to(external_root.resolve()), "cache outside external root"
    )
    data, raw = read_inventory(inventory, expected_sha256)
    declared = manifest(data, cache, max_bytes)
    free = shutil.disk_usage(external_root).free
    require(
        free >= declared.total_size + MIN_FREE_RESERVE,
        "external free-space reserve unavailable",
    )
    observer = TimedClient(client, deadline)
    observer.tick()

    # fetch only uses the client's download method. It validates each existing/new
    # object's size/SHA and atomically installs bytes; no schema/tag rewriting.
    def one(item: HostedObject) -> Fetched:
        observer.tick()
        single = Manifest(declared.repository, declared.tag, (item,))
        result = fetch(
            single, cache.resolve(), cast(ReleaseClient, observer), replace_local=False
        )
        observer.tick()
        return result[0]

    results: dict[int, Fetched] = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(one, item): index for index, item in enumerate(declared.objects)}
        try:
            for future in as_completed(futures):
                results[futures[future]] = future.result()
                observer.tick()
        except BaseException:
            observer.stopped.set()
            for future in futures:
                _ = future.cancel()
            raise
    outcomes = [results[index] for index in range(len(declared.objects))]
    observer.tick()
    _, after = read_inventory(inventory, expected_sha256)
    require(after == raw, "inventory changed during acquisition")
    return {
        "schema": RECEIPT_SCHEMA,
        "status": "ACQUIRED",
        "repository": declared.repository,
        "tag": declared.tag,
        "inventory_sha256": expected_sha256,
        "cache_root": str(cache.resolve()),
        "objects": len(outcomes),
        "compressed_bytes": declared.total_size,
        "acquisition_workers": workers,
        "external_free_bytes_before": free,
        "actions": [{"path": result.path, "action": result.action} for result in outcomes],
        "HostedData_v1_conforming": False,
        "full_verification_passed": False,
        "certificate_admission_performed": False,
        "global_bound_changed": False,
        "network_calls_hard_bounded_internally": False,
        "max_bytes_limits_declared_roster_not_network_stream": True,
        "outer_owned_process_wall_RSS_cleanup_required": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--inventory-sha256", required=True)
    parser.add_argument("--cache-root", type=Path, required=True)
    parser.add_argument("--external-root", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-bytes", type=int, required=True)
    parser.add_argument("--max-seconds", type=int, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    require(not args.output.exists(), "acquisition output already exists")
    if not 0 < args.max_seconds <= 300:
        parser.error("max-seconds must be in (0,300]")
    receipt = acquire(
        args.inventory,
        args.inventory_sha256,
        args.cache_root,
        args.max_bytes,
        deadline=time.monotonic() + args.max_seconds,
        client=GhClient(),
        external_root=args.external_root,
        workers=args.workers,
    )
    encoded = retained_json.dumps(receipt).encode()
    require(len(encoded) <= OUTPUT_LIMIT, "acquisition output ceiling")
    with args.output.open("xb") as stream:
        _ = stream.write(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
