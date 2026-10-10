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


LATER = "example-later-release-2026-01-03"


def _later(source: tuple[Path, Path, Path, bytes]) -> tuple[Path, str]:
    """A later packet of the same tree that pins the gzip as the earlier packet's copy."""
    packet, _checkout, repository, _raw = source
    twin = (packet / "source/original.json.gz").relative_to(repository).as_posix()
    later = packet.with_name(LATER)
    (later / "acquisition").mkdir(parents=True)
    declaration = json.loads((packet / acquisition.DECLARATION).read_text())
    del declaration["original_gzip"]
    declaration["pinned_only"] = [
        {
            "match": "original.json.gz",
            "reason": "unchanged; the earlier packet retains it as original gzip",
            "identical_to": twin,
        }
    ]
    (later / acquisition.DECLARATION).write_text(json.dumps(declaration))
    (later / "README.md").write_text("# Later release\n")
    return later, twin


def test_identical_to_binds_an_original_gzip_by_its_stored_bytes(
    source: tuple[Path, Path, Path, bytes],
) -> None:
    _acquire(source)
    _packet, checkout, repository, raw = source
    later, twin = _later(source)
    entry = acquisition.acquire(later, checkout, repository)
    (item,) = entry["pinned_only"]
    assert item.get("identical_to") == twin
    assert item["sha256"] == hashlib.sha256(raw).hexdigest()
    assert acquisition.check(later, repository) == []


def test_an_original_gzip_twin_is_not_compared_decompressed(
    source: tuple[Path, Path, Path, bytes],
) -> None:
    _acquire(source)
    packet, checkout, repository, raw = source
    later, twin = _later(source)
    acquisition.acquire(later, checkout, repository)
    # The same content recompressed: equal once decompressed, different as stored.
    recompressed = gzip.compress(gzip.decompress(raw), mtime=0)
    (packet / "source/original.json.gz").write_bytes(recompressed)
    assert acquisition.check(later, repository) == [
        f"{LATER}: pinned-only original.json.gz is not the bytes of {twin}"
    ]
    with pytest.raises(ValueError, match="is not the bytes of"):
        acquisition.acquire(later, checkout, repository)


def test_only_the_custody_table_makes_a_twin_original_gzip(
    source: tuple[Path, Path, Path, bytes],
) -> None:
    """A ``.gz`` twin its packet does not list as original gzip is read decompressed."""
    _acquire(source)
    packet, checkout, repository, _raw = source
    later, _twin = _later(source)
    (packet / "README.md").write_text("# Source\n")
    with pytest.raises(ValueError, match="is not the bytes of"):
        acquisition.acquire(later, checkout, repository)


def test_ryu_v11_binds_every_certificate_the_v10_packet_retains() -> None:
    """The three certificates v1.0 keeps as original gzip bind v1.1's; the hosted two don't."""
    v10 = acquisition.WEB / "squarepacker-k2-minus-c-upper-2026-10-09"
    v11 = acquisition.WEB / "squarepacker-k2-minus-c-upper-v11-2026-10-10"
    (earlier,) = json.loads((v10 / acquisition.RECORD).read_text())["sources"]
    (later,) = json.loads((v11 / acquisition.RECORD).read_text())["sources"]
    certificates = {
        item["path"]: item for item in later["pinned_only"] if "/stair_k" in item["path"]
    }
    assert len(certificates) == 5
    retained = {path.removeprefix("source/"): path for path in earlier["original_gzip"]}
    hosted = {item["path"] for item in earlier["pinned_only"]}
    assert certificates.keys() == retained.keys() | hosted
    for path, stored in retained.items():
        assert (
            certificates[path]["identical_to"]
            == f"{v10.relative_to(acquisition.REPO)}/{stored}"
        )
    assert all("identical_to" not in certificates[path] for path in hosted)
    assert acquisition.check(v11, acquisition.REPO) == []
