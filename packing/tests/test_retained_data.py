"""Retained data stored as deterministic gzip reads back as the upstream bytes."""

from __future__ import annotations

import csv
import gzip
import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import audit_tokoharu_density as tokoharu
from devtools.retained_data import (
    candidates,
    check_packet,
    compressed_path,
    git_blob,
    is_deterministic_gzip,
    read_retained_bytes,
    read_table,
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
    # The candidates and linear files retained on 11 October for stage 4
    # (`devtools.retain_wand125_release`).
    "wand125-linear-n122-2026-10-10",
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
