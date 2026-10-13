"""The R067 and R068 packet holds the pinned bytes, and its claims re-derive from them.

The certificates are Guzhou0806's continuations of Overbeck's 4.66001 charge. These
tests read the retained files only: the pinned packages against their own manifests and
publication records, what each certificate changes relative to 4.66001, and the
published and fresh interval ledgers row by row. No sweep runs here; the full paired
replays are the packet's receipts.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_guzhou_r068 as audit
from devtools.retained_data import candidates, check_packet, read_retained_bytes

RECEIPTS = audit.PACKET / "receipts"
#: Root files R068's commit edited after R067's publication record described them.
EDITED_BY_R068 = frozenset(
    {
        "CHANGELOG.md",
        "CITATION.cff",
        "NOTICE.md",
        "README.md",
        "RESULTS.md",
        "docs/EVIDENCE_MAP.md",
        "docs/RELEASE_NOTES.md",
        "docs/REPRODUCIBILITY.md",
        "scripts/check_release_hashes.py",
    }
)
#: The canonical ledger digest the 4.66001 packet's receipts record for its replays.
KLEDDAMAG_466001_ROWS_SHA256 = (
    "19952dbbcacd03eff37ed1e74acf1042a0e5020c8867989e168b73cc1fefdbb4"
)


def _matches(path: Path, item: dict[str, Any]) -> bool:
    data = read_retained_bytes(path)
    return len(data) == item["bytes"] and hashlib.sha256(data).hexdigest() == item["sha256"]


@pytest.fixture(scope="module")
def structures() -> dict[str, dict[str, Any]]:
    return {name: audit.structure(name) for name in audit.RELEASES}


def test_compressed_files_match_their_table() -> None:
    assert check_packet(audit.PACKET) == []
    assert candidates(audit.PACKET) == []


@pytest.mark.parametrize("name", sorted(audit.RELEASES))
def test_each_package_matches_its_manifest(name: str) -> None:
    package = audit.RELEASES[name].package
    files = json.loads(read_retained_bytes(package / "MANIFEST.json"))["files"]
    stored = {
        str(path.relative_to(package)).removesuffix(".gz")
        for path in package.rglob("*")
        if path.is_file()
    }
    assert stored - set(files) == {"MANIFEST.json"}
    assert all(_matches(package / entry, item) for entry, item in files.items())


def test_publication_records_describe_the_retained_bytes() -> None:
    root = audit.SOURCE_ROOT
    r068 = json.loads((root / "R068_PUBLICATION.json").read_text(encoding="utf-8"))["files"]
    assert all(_matches(root / name, item) for name, item in r068.items())
    r067 = json.loads((root / "R067_PUBLICATION.json").read_text(encoding="utf-8"))["files"]
    stale = {name for name, item in r067.items() if not _matches(root / name, item)}
    assert stale == EDITED_BY_R068


def test_r068_moves_one_site_orbit_and_adds_one(structures: dict[str, dict[str, Any]]) -> None:
    shape = structures["R068"]
    moved, added = shape["point_orbit_changes"]
    assert moved["index"] == 1480
    assert moved["delta"] == [0, -800000]
    assert moved["weight"] == 0
    assert moved["same_image_order"]
    assert moved["rule_orbits_referencing"] == 1
    assert added["new"] == [13400000000, 13400000000, 11734]
    assert added["images"] == 4
    assert added["budget_units"] == 4 * 11734
    assert shape["rule_orbits_unchanged"]
    assert shape["budget_units"] == 17000402008 + 4 * 11734 == 17000448944
    assert shape["budget_delta_accounted"]
    assert shape["angle_chain"]["new_intervals"] == 4991
    assert shape["angle_chain"]["original_intervals"] == 2168


def test_r067_keeps_the_charge_and_bisects_640_intervals(
    structures: dict[str, dict[str, Any]],
) -> None:
    shape = structures["R067"]
    assert shape["point_orbit_changes"] == []
    assert shape["rule_orbits_unchanged"]
    assert shape["budget_delta_units"] == 0
    assert shape["angle_chain"]["pieces_per_original"] == {"1": 1528, "2": 640}
    assert shape["angle_chain"]["exact_bisections"] == 640


@pytest.mark.parametrize("name", sorted(audit.RELEASES))
def test_structure_receipts_are_current(
    name: str, structures: dict[str, dict[str, Any]]
) -> None:
    recorded = json.loads((RECEIPTS / name.lower() / "structure.json").read_text())
    assert recorded == structures[name]


#: Per release: surplus, summed cells, C++ sites and signed terms, the triples digest and
#: the least strict margin, as the 2026-09-28 review of R067 and R068 states them.
PUBLISHED = {
    "R067": (
        54340,
        1249459677392,
        20856,
        49204,
        "5fe449f6b2740278cb8d1e36e84ca639df0790c1e70e68bdee340e2c2c342d00",
        (
            "392478867597353819118463778084255632092881/"
            "392474616038972119614931587776706448092881000000000000"
        ),
    ),
    "R068": (
        7404,
        2210145745763,
        20860,
        49208,
        "d2c47f4adcce9a3fa64dd280a0ea4ed04bbb37d8b3347a471e560980de937407",
        (
            "952933981168979477888243189701088457479269241/"
            "952933310781657455908355581458029346772069241000000000000"
        ),
    ),
}


@pytest.mark.parametrize("name", sorted(audit.RELEASES))
def test_published_ledgers_agree_row_by_row(name: str) -> None:
    surplus, cells, sites, terms, triples, margin = PUBLISHED[name]
    published = audit.RELEASES[name].published
    result = audit.compare(name, published, published)
    assert result["mismatches"] == 0
    assert result["minimum_units"] == 1000026844
    assert result["intervals_at_minimum"] == audit.RELEASES[name].intervals
    assert result["surplus_units"] == surplus
    assert result["cells"] == cells
    assert set(result["triples_sha256"].values()) == {triples}
    header = result["cpp_headers"]["published"]
    assert (header["sites"], header["signed_terms"]) == (sites, terms)
    assert header["minimum_strict_margin"] == margin


@pytest.mark.parametrize("name", sorted(audit.RELEASES))
def test_fresh_replay_ledgers_equal_the_published_ones(name: str) -> None:
    fresh = RECEIPTS / name.lower() / "replay"
    result = audit.compare(name, fresh)
    assert result["mismatches"] == 0
    assert len(set(result["canonical_rows_sha256"].values())) == 1
    assert set(result["triples_sha256"].values()) == {PUBLISHED[name][4]}
    assert result["cpp_headers"]["fresh"] == result["cpp_headers"]["published"]
    recorded = json.loads((RECEIPTS / name.lower() / "compare.json").read_text())
    assert recorded["canonical_rows_sha256"] == result["canonical_rows_sha256"]
    theorem = json.loads((fresh / "THEOREM.json").read_text())
    assert theorem["status"] == "PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION"
    assert int(theorem["surplus"]) == result["surplus_units"]


def test_canonical_form_reproduces_the_466001_digest() -> None:
    evidence = audit.BASELINE.parent / "evidence/publication"
    rows: list[dict[str, int]] = []
    for index in range(3):
        record = json.loads(read_retained_bytes(evidence / f"node-{index}.json"))
        rows.extend(
            {
                "interval": int(row["interval"]),
                "minimum_units": int(row["minimum_units"]),
                "cells": int(row["cells"]),
            }
            for row in record["rows"]
        )
    assert audit.canonical_sha256(rows) == KLEDDAMAG_466001_ROWS_SHA256


def test_a_changed_row_is_reported(tmp_path: Path) -> None:
    published = audit.RELEASES["R068"].published
    for kind in ("cpp", "node"):
        for index in range(2):
            name = f"{kind}-{index}.json"
            (tmp_path / name).write_bytes(read_retained_bytes(published / name))
    record = json.loads((tmp_path / "node-1.json").read_text())
    record["rows"][7]["cells"] += 1
    (tmp_path / "node-1.json").write_text(json.dumps(record))
    result = audit.compare("R068", tmp_path, published)
    assert result["mismatches"] == 1
    assert result["first_mismatches"][0]["ledger"] == "fresh-node"
    assert result["first_mismatches"][0]["interval"] == record["rows"][7]["interval"]


def test_a_missing_partition_is_refused(tmp_path: Path) -> None:
    published = audit.RELEASES["R068"].published
    for name in ("cpp-0.json", "cpp-1.json", "node-0.json"):
        (tmp_path / name).write_bytes(read_retained_bytes(published / name))
    with pytest.raises(ValueError, match="node rows do not cover every interval"):
        audit.compare("R068", tmp_path, published)
