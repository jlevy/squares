"""Retained data stored as deterministic gzip reads back as the upstream bytes."""

from __future__ import annotations

import csv
import gzip
import json
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import acquire_source
from devtools import audit_tokoharu_density as tokoharu
from devtools.retained_data import (
    LINE_THRESHOLD,
    candidates,
    check_packet,
    compressed_path,
    git_blob,
    is_deterministic_gzip,
    read_retained_bytes,
    read_table,
    write_retained,
)

WEB = Path(__file__).resolve().parents[1] / "resources" / "web"
#: Packets whose large data files are stored compressed, each with a README table.
PACKETS = (
    "evand-square-packing-2026-09-26",
    "evand-square-packing-2026-09-28",
    "n17-kleddamag-4640020-2026-09-26",
    "n17-kleddamag-466001-2026-09-27",
    "n17-guzhou-r068-2026-09-28",
    "wand125-rectangle-certificates-2026-09-27",
    "wand125-rectangle-certificates-2026-09-28",
    "wand125-rectangle-certificates-2026-10-01",
    "wand125-point-and-mixed-2026-09-28",
    "wand125-point-and-mixed-2026-10-01",
    "franciscouzo-square-packing-2026-09-27",
    "casson-square-packing-2026-09-23",
    "wang-li-n11-2026-09-29",
    "n11-optimality-gpt6-pro-review-2026-10-03",
    # The two-strip family's decisions receipts (think-rsqv): #799's version 2 and #836's
    # version 5, written by `devtools.two_strip_checker` through `write_retained`.
    "karimi-two-strip-2026-10-24",
    "karimi-records-2026-10-31",
)


@pytest.mark.parametrize("packet", PACKETS)
def test_every_compressed_file_matches_its_table_row(packet: str) -> None:
    assert read_table(WEB / packet / "README.md")
    assert check_packet(WEB / packet) == []


@pytest.mark.parametrize("packet", PACKETS)
def test_no_large_data_file_is_left_plain(packet: str) -> None:
    assert candidates(WEB / packet) == []


def test_plain_and_compressed_copies_read_alike(tmp_path: Path) -> None:
    data = b'{"a": 1}\n' * 3
    plain = tmp_path / "x.json"
    compressed_path(plain).write_bytes(gzip.compress(data, mtime=0))
    assert read_retained_bytes(plain) == data
    assert read_retained_bytes(compressed_path(plain)) == data
    plain.write_bytes(data)
    assert read_retained_bytes(plain) == data
    plain.write_bytes(data + b"\n")
    with pytest.raises(ValueError, match="differs from its compressed copy"):
        read_retained_bytes(plain)


def test_missing_and_oversized_files_are_refused(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_retained_bytes(tmp_path / "absent.json")
    path = tmp_path / "big.txt"
    compressed_path(path).write_bytes(gzip.compress(b"0" * 4096, mtime=0))
    with pytest.raises(ValueError, match="exceeds"):
        read_retained_bytes(path, limit=1024)


def test_a_retained_write_is_plain_below_the_threshold_and_reproducible_gzip_above(
    tmp_path: Path,
) -> None:
    """think-rsqv: a writer keeps one form of a retained file, plain at or below
    `LINE_THRESHOLD` lines and ``gzip -9n`` above it, so the same bytes are stored the
    same way whenever they are written; the other form is removed, and readers read
    either."""
    path = tmp_path / "receipts" / "decisions.json"
    small = b'{"a": 1}\n' * LINE_THRESHOLD
    large = small + b'{"b": 2}\n'
    assert write_retained(path, small) == path
    assert path.read_bytes() == small
    assert not compressed_path(path).exists()
    stored = write_retained(path, large)
    assert stored == compressed_path(path)
    assert not path.exists()
    first = stored.read_bytes()
    assert is_deterministic_gzip(first)
    assert read_retained_bytes(path) == large
    assert write_retained(path, large).read_bytes() == first
    assert write_retained(path, small) == path
    assert not compressed_path(path).exists()
    assert read_retained_bytes(path) == small
    source = tmp_path / "large.py"
    assert write_retained(source, large) == source


def test_a_retained_write_makes_its_gzip_in_process_and_keeps_an_equal_one(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review A4 of #869: the archive is made by Python's gzip (mtime 0, no file name),
    not a gzip program, so what is guaranteed is the decompressed bytes, not one deflate
    stream across zlib builds; and a stored file whose bytes already decompress to the
    data is kept, so writing again churns nothing."""

    def refuse(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("write_retained ran a program")

    monkeypatch.setattr(subprocess, "run", refuse)
    path = tmp_path / "decisions.json"
    data = b'{"row": 1}\n' * (LINE_THRESHOLD + 1)
    stored = write_retained(path, data)
    assert is_deterministic_gzip(stored.read_bytes())
    assert gzip.decompress(stored.read_bytes()) == data
    other = gzip.compress(data, compresslevel=1, mtime=0)
    stored.write_bytes(other)
    assert write_retained(path, data) == stored
    assert stored.read_bytes() == other
    assert write_retained(path, data + b"{}\n") == stored
    assert gzip.decompress(stored.read_bytes()) == data + b"{}\n"


def _row(stored: str, origin: str, blob: str = "", sha256: str = "") -> str:
    return f"| `{stored}` | {origin} | {f'`{blob}`' if blob else ''} | " + (
        f"`{sha256}` |" if sha256 else " |"
    )


def _packet(tmp_path: Path, *rows: str) -> Path:
    packet = tmp_path / "packet"
    (packet / "receipts").mkdir(parents=True)
    table = "\n".join(rows)
    (packet / "README.md").write_text(
        "# A packet\n\n## Compressed Files\n\n| Stored file | Origin | Git blob | SHA-256 |\n"
        f"| --- | --- | --- | --- |\n{table}\n",
        encoding="utf-8",
    )
    return packet


def test_a_receipt_row_may_name_no_digest(tmp_path: Path) -> None:
    """Review A2 of #869 (OR-16): a receipt the repository writes again, with new
    timings at every run, is not pinned by digest; Git keeps its bytes. Its row names the
    file and its origin, and the check asks that it is listed, carries no name or
    timestamp, and decompresses. An upstream row still states both digests."""
    receipt = "receipts/decisions.json.gz"
    packet = _packet(tmp_path, _row(receipt, "receipt"))
    (packet / receipt).write_bytes(gzip.compress(b"{}\n", mtime=0))
    assert check_packet(packet) == []
    (packet / receipt).write_bytes(gzip.compress(b"{}\n", mtime=7))
    assert check_packet(packet) == [
        "packet: receipts/decisions.json.gz carries a name or timestamp"
    ]
    (packet / receipt).write_bytes(gzip.compress(b"{}\n", mtime=0)[:-6])
    assert check_packet(packet) == ["packet: receipts/decisions.json.gz does not decompress"]
    upstream = _packet(tmp_path / "up", _row("receipts/data.json.gz", "upstream"))
    (upstream / "receipts/data.json.gz").write_bytes(gzip.compress(b"{}\n", mtime=0))
    assert check_packet(upstream) == [
        "packet: receipts/data.json.gz is an upstream row and must state its digests"
    ]


@pytest.mark.parametrize(
    ("packet", "receipt"),
    [
        ("karimi-two-strip-2026-10-24", "receipts/two-strip-decisions-v2.json"),
        ("karimi-records-2026-10-31", "receipts/two-strip-decisions-v5.json"),
    ],
)
def test_a_decide_all_rerun_leaves_the_two_strip_packets_green(
    tmp_path: Path, packet: str, receipt: str
) -> None:
    """Review A2 of #869: a rerun of `decide-all` writes new `cpu_seconds`, and with the
    receipts pinned by digest `check_packet` and `acquire_source --check` then failed
    until someone edited a Git blob and a SHA-256 by hand. In a copy of each packet, the
    receipt written again with another time still checks."""
    root = tmp_path / "repo"
    copy = root / "packing" / "resources" / "web" / packet
    shutil.copytree(WEB / packet, copy)
    value = json.loads(read_retained_bytes(copy / receipt))
    value["cpu_seconds"] = value.get("cpu_seconds", 0) + 0.5
    write_retained(copy / receipt, _dumps(value))
    assert check_packet(copy) == []
    if (copy / "acquisition" / "declaration.json").is_file():
        assert acquire_source.check(copy, root) == []


def _dumps(value: Any) -> bytes:
    from sqpack.retained_json import dumps  # noqa: PLC0415

    return dumps(value, sort_keys=True).encode("utf-8")


def test_header_and_blob_helpers() -> None:
    assert is_deterministic_gzip(gzip.compress(b"x", mtime=0))
    assert not is_deterministic_gzip(gzip.compress(b"x", mtime=1))
    # `git hash-object /dev/null`.
    assert git_blob(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"


def test_evand_october_source_manifest() -> None:
    """Pinned source blobs survive retention, including the local gzip transforms."""
    packet = WEB / "evand-square-packing-2026-10-01"
    with (packet / "source-manifest.tsv").open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == 77
    assert len({row["upstream_path"] for row in rows}) == len(rows)
    for row in rows:
        upstream = row["upstream_path"]
        stored = row["stored_path"]
        assert stored in {f"source/{upstream}", f"source/{upstream}.gz"}
        data = (packet / stored).read_bytes()
        if stored == f"source/{upstream}.gz":
            data = gzip.decompress(data)
        assert len(data) == int(row["upstream_bytes"]), upstream
        assert git_blob(data) == row["upstream_git_blob"], upstream


def test_tokoharu_packet_on_main_still_reads_plain_files() -> None:
    """The 2026-09-22 packet keeps its candidates plain, and `load_json` reads them so."""
    case = tokoharu.SOURCE / "certificates" / tokoharu.CASES[29] / "certified_candidate.json"
    assert case.is_file()
    assert not compressed_path(case).exists()
    assert tokoharu.load_json(case) == json.loads(
        case.read_text(), parse_float=Fraction, object_pairs_hook=dict
    )
