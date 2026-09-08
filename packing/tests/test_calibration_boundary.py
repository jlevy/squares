#!/usr/bin/env python3
"""The calibration layers stay at `n = 1..100` while the corpus widens around them.

`D4` of the atlas expansion draws a line the type system cannot: the chunk census, the
partition atlas, the taxonomy, the evidence profile and the contact-overlay gallery were
designed while their authors were looking at the first hundred cases, so they are
calibration instruments and the range beyond them has to stay unseen to be usable as a
holdout later. Every one of them finds its witnesses by iterating the known-best
manifest, and the manifest is about to grow to `n = 1..324`. Without a gate they would
all widen silently -- no error, no diff, just an instrument quietly spending the corpus
it was going to be tested on.

So each of those tools now selects its entries through one function, and this file feeds
every one of those functions a manifest that runs past the boundary and checks what comes
back. The fake manifest is deliberately five cases too long: a filter that is really a
no-op passes a 100-entry fixture and fails this one.

The sound screens are the deliberate exception and are checked here too, from the other
side: a replayed slide and an exact tiling are certificates rather than instruments, so
they follow `KNOWN_BEST_CORPUS` and must NOT be pinned.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pytest

from devtools import (
    census_chunk_taxonomy,
    census_known_best_chunks,
    certify_assembly_coverage,
    profile_known_best_chunks,
    render_known_best_contact_overlays,
)
from devtools.assess_frontier_rigidity import tiling_cases
from sqpack.known_best import (
    CALIBRATION_CORPUS,
    KNOWN_BEST_CORPUS,
    calibration_entries,
    declared_calibration_label,
    require_calibration_label,
)
from sqpack.yamlio import safe_load

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ATLAS = PROJECT_ROOT / "atlas/known-best"
OVERSHOOT = 5
"""How far past the calibration boundary the fake manifest runs."""


def _fake_manifest(path: Path, last_n: int) -> Path:
    """A manifest shaped like the real one and longer than the calibration corpus."""
    entries = [
        {
            "n": n,
            "source": {"kind": "exact-grid"},
            "witness": {"path": f"witnesses/known-best/n-{n:03d}.yaml"},
        }
        for n in range(1, last_n + 1)
    ]
    document = {
        "atlas": {
            "range": {"first_n": 1, "last_n": last_n, "count": last_n},
            "entries": entries,
        }
    }
    path.write_text(json.dumps(document), encoding="utf-8")
    return path


@pytest.fixture
def widened_manifest(tmp_path: Path) -> Path:
    return _fake_manifest(tmp_path / "manifest.json", CALIBRATION_CORPUS.last_n + OVERSHOOT)


def test_the_fixture_really_is_wider_than_the_boundary(widened_manifest: Path) -> None:
    """Guard the guard: a fixture that stopped at 100 would make every test below vacuous."""
    atlas = json.loads(widened_manifest.read_text(encoding="utf-8"))["atlas"]
    assert len(atlas["entries"]) == CALIBRATION_CORPUS.count + OVERSHOOT


def test_chunk_census_reads_only_the_calibration_corpus(widened_manifest: Path) -> None:
    entries = census_known_best_chunks.atlas_entries(widened_manifest)
    assert [entry["n"] for entry in entries] == list(CALIBRATION_CORPUS.numbers)


def test_evidence_profile_reads_only_the_calibration_corpus(widened_manifest: Path) -> None:
    entries = profile_known_best_chunks.manifest_entries(widened_manifest)
    assert [entry["n"] for entry in entries] == list(CALIBRATION_CORPUS.numbers)


def test_contact_overlays_read_only_the_calibration_corpus(widened_manifest: Path) -> None:
    entries = render_known_best_contact_overlays.corpus_entries(widened_manifest)
    assert [entry["n"] for entry in entries] == list(CALIBRATION_CORPUS.numbers)


def test_chunk_taxonomy_reads_only_the_calibration_corpus(widened_manifest: Path) -> None:
    entries = census_chunk_taxonomy.manifest(widened_manifest)
    assert sorted(entries) == list(CALIBRATION_CORPUS.numbers)


def test_assembly_coverage_inherits_the_taxonomy_boundary() -> None:
    """`certify_assembly_coverage` has no manifest reader of its own, and must not grow one."""
    assert certify_assembly_coverage.manifest is census_chunk_taxonomy.manifest


def test_a_manifest_short_of_the_calibration_corpus_is_refused(tmp_path: Path) -> None:
    """The other direction. A shortfall must be an error, not a smaller aggregate."""
    short = json.loads(
        _fake_manifest(tmp_path / "short.json", CALIBRATION_CORPUS.last_n - 1).read_text(
            encoding="utf-8"
        )
    )["atlas"]
    with pytest.raises(ValueError, match="not fully present"):
        calibration_entries(short["entries"])


def test_the_retained_schemas_still_pin_the_calibration_range() -> None:
    """The record and the constant say the same thing, and the tools refuse if they stop.

    These constants are the calibration record. Keeping them and keeping
    `CALIBRATION_CORPUS` is not redundancy: the schema is what a reader of the retained
    document sees, and the constant is what the tool actually read.
    """
    profile_schema = safe_load(
        (ATLAS / "chunk-evidence-profile.schema.yaml").read_text(encoding="utf-8")
    )
    assert (
        profile_schema["properties"]["scope"]["properties"]["range"]["const"]
        == CALIBRATION_CORPUS.label
    )
    grammar_schema = safe_load(
        (ATLAS / "contact-assembly-grammar.schema.yaml").read_text(encoding="utf-8")
    )
    assert (
        grammar_schema["properties"]["evaluation_split"]["properties"]["calibration"]["const"]
        == CALIBRATION_CORPUS.label
    )
    grammar = safe_load((ATLAS / "contact-assembly-grammar.yaml").read_text(encoding="utf-8"))
    assert grammar["grammar"]["evaluation_split"]["calibration"] == CALIBRATION_CORPUS.label


def test_a_disagreeing_schema_constant_stops_the_tool() -> None:
    """Refuse, rather than emit a document whose declared scope is not the scope read."""
    require_calibration_label(CALIBRATION_CORPUS.label, source="a schema that agrees")
    with pytest.raises(ValueError, match="registered decision"):
        require_calibration_label("n=1..324", source="a schema that has moved")


def test_a_widened_census_reaches_its_readers_as_an_error() -> None:
    """The gallery and the taxonomy read the census, so the census's scope is theirs."""
    census: dict[str, Any] = {"corpus": "atlas/known-best/manifest.json; inspected n=1..324"}
    label = declared_calibration_label(census["corpus"], source="a widened census")
    assert label == "n=1..324"
    with pytest.raises(ValueError, match="registered decision"):
        require_calibration_label(label, source="a widened census")
    with pytest.raises(ValueError, match="declares no calibration range"):
        declared_calibration_label("no range here at all", source="a census without a scope")


def test_the_retained_census_declares_the_calibration_range() -> None:
    census = json.loads((ATLAS / "chunk-components.json").read_text(encoding="utf-8"))
    partitions = json.loads((ATLAS / "chunk-partitions.json").read_text(encoding="utf-8"))
    for corpus, name in (
        (census["corpus"], "chunk-components.json"),
        (partitions["atlas"]["corpus"], "chunk-partitions.json"),
    ):
        assert declared_calibration_label(corpus, source=name) == CALIBRATION_CORPUS.label


def test_the_sound_screens_are_not_pinned_to_the_calibration_corpus() -> None:
    """`D4`'s exception, from the other side.

    A certified slide and an exact tiling are certificates about one configuration, not
    instruments calibrated on the cases they were designed against, so they extend with
    the corpus. The tiling set is derived here rather than listed, which is what makes
    `k = 11..18` arrive on their own when the corpus reaches them.
    """
    assert tiling_cases() == tuple(
        n for n in KNOWN_BEST_CORPUS.numbers if math.isqrt(n) ** 2 == n
    )
