"""Original upstream gzip is explicit raw custody, separate from archive compression."""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path

import pytest

from devtools import acquire_source as acquisition
from devtools.retained_data import describe_original_gzip, is_deterministic_gzip


@pytest.fixture
def source(tmp_path: Path) -> tuple[Path, Path, Path, bytes]:
    checkout, repository = tmp_path / "upstream", tmp_path / "repository"
    checkout.mkdir()
    raw = gzip.compress(b'{"complete": "original candidate bytes"}\n', mtime=1234)
    (checkout / "original.json.gz").write_bytes(raw)
    for arguments in (("init", "-q"), ("add", "."), ("commit", "-q", "-m", "source")):
        subprocess.run(
            (
                "git",
                "-C",
                str(checkout),
                "-c",
                "user.name=fixture",
                "-c",
                "user.email=fixture@example.invalid",
                *arguments,
            ),
            env={
                **os.environ,
                "GIT_AUTHOR_DATE": "2026-01-03T04:05:00Z",
                "GIT_COMMITTER_DATE": "2026-01-03T04:05:00Z",
            },
            check=True,
            capture_output=True,
        )
    commit = subprocess.run(
        ("git", "-C", str(checkout), "rev-parse", "HEAD"),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    packet = repository / "packing/resources/web/example-original-gzip-2026-01-03"
    (packet / "acquisition").mkdir(parents=True)
    declaration = {
        "format": acquisition.DECLARATION_FORMAT,
        "id": "example",
        "source_url": "https://example.invalid/upstream",
        "source_ref": "main",
        "source_commit": commit,
        "retrieved_at_utc": "2026-01-03T04:05:00Z",
        "git_scope": "One original input",
        "archived_dir": "source",
        "license": "MIT",
        "claims": ["Original gzip custody"],
        "scope": ["original.json.gz"],
        "pinned_only": [],
        "original_gzip": ["original.json.gz"],
    }
    (packet / acquisition.DECLARATION).write_text(json.dumps(declaration))
    return packet, checkout, repository, raw


def _acquire(source: tuple[Path, Path, Path, bytes]) -> None:
    packet, checkout, repository, _raw = source
    entry = acquisition.acquire(packet, checkout, repository)
    assert "original_gzip" in entry
    rows = [
        describe_original_gzip(packet, packet / path).markdown()
        for path in entry["original_gzip"]
    ]
    (packet / "README.md").write_text(
        "# Source\n\n## Original Gzip Files\n\n"
        "| Stored file | Origin | Git blob | SHA-256, raw |\n"
        "| --- | --- | --- | --- |\n" + "\n".join(rows) + "\n"
    )


def test_original_gzip_retains_raw_header_and_blob(
    source: tuple[Path, Path, Path, bytes],
) -> None:
    _acquire(source)
    packet, _checkout, repository, raw = source
    assert not is_deterministic_gzip(raw)
    assert (packet / "source/original.json.gz").read_bytes() == raw
    record = json.loads((packet / acquisition.RECORD).read_text())["sources"][0]
    assert record["compressed"] == []
    assert record["original_gzip"] == ["source/original.json.gz"]
    assert record["retained_total_bytes"] == len(raw)
    assert hashlib.sha256(raw).hexdigest() in (packet / acquisition.MANIFEST).read_text()
    assert acquisition.check(packet, repository) == []


def test_default_still_refuses_original_gzip(source: tuple[Path, Path, Path, bytes]) -> None:
    packet, checkout, repository, _raw = source
    declaration = json.loads((packet / acquisition.DECLARATION).read_text())
    del declaration["original_gzip"]
    (packet / acquisition.DECLARATION).write_text(json.dumps(declaration))
    with pytest.raises(ValueError, match="can be pinned but not retained"):
        acquisition.acquire(packet, checkout, repository)


@pytest.mark.parametrize("changed", ["bytes", "blob", "record", "declaration"])
def test_original_custody_mutations_are_refused(
    source: tuple[Path, Path, Path, bytes], changed: str
) -> None:
    _acquire(source)
    packet, _checkout, repository, raw = source
    if changed == "bytes":
        (packet / "source/original.json.gz").write_bytes(
            gzip.compress(gzip.decompress(raw), mtime=0)
        )
    elif changed == "blob":
        row = describe_original_gzip(packet, packet / "source/original.json.gz")
        readme = packet / "README.md"
        readme.write_text(readme.read_text().replace(row.blob, "0" * 40))
    else:
        path = packet / (acquisition.RECORD if changed == "record" else acquisition.DECLARATION)
        value = json.loads(path.read_text())
        (value["sources"][0] if changed == "record" else value)["original_gzip"] = []
        path.write_text(json.dumps(value))
    assert acquisition.check(packet, repository)


@pytest.mark.parametrize(
    "paths",
    [["../original.json.gz"], ["/original.json.gz"], ["original.json.gz", "original.json.gz"]],
)
def test_original_paths_are_exact_and_unique(
    source: tuple[Path, Path, Path, bytes], paths: list[str]
) -> None:
    packet, checkout, repository, _raw = source
    declaration = json.loads((packet / acquisition.DECLARATION).read_text())
    declaration["original_gzip"] = paths
    (packet / acquisition.DECLARATION).write_text(json.dumps(declaration))
    with pytest.raises(ValueError, match="original_gzip"):
        acquisition.acquire(packet, checkout, repository)
