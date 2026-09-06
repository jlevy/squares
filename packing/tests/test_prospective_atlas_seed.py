#!/usr/bin/env python3
"""Coverage and exclusion controls for the prospective atlas seed."""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path

import mpmath as mp
import pytest

from devtools import build_prospective_atlas as prospective
from devtools.build_prospective_atlas import MANIFEST, expected_outputs, seed_errors
from sqpack.witness import load_witness

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "witnesses/witness.schema.yaml"
UNITSQUARE_RESULTS = ROOT / "resources/web/unitsquare-release1-2026/results.json"


@pytest.fixture
def isolated_seed_build_cache():
    """For the test that repoints SOURCE_ROOT; see clear_build_caches."""
    prospective.clear_build_caches()
    yield
    prospective.clear_build_caches()


@pytest.mark.slow
def test_seed_replays_every_safe_source_and_excludes_kingbird() -> None:
    retained = json.loads(MANIFEST.read_text(encoding="utf-8"))
    _outputs, expected = expected_outputs()
    assert retained == expected

    seed = retained["atlas_seed"]
    entries = seed["entries"]
    assert len(entries) == 101
    assert len({entry["n"] for entry in entries}) == 101
    assert Counter(entry["source"]["kind"] for entry in entries) == {
        "exact-generated-grid": 97,
        "unitsquare-rendering": 4,
    }
    assert {
        entry["n"] for entry in entries if entry["source"]["kind"] == "unitsquare-rendering"
    } == {103, 105, 110, 131}
    assert all(entry["annotation_status"] == "prohibited-uncomputed" for entry in entries)
    assert seed["excluded"] == {
        "count": 123,
        "reason": "Kingbird acquisition is deferred pending license review.",
        "source_key": "kingbird-current-catalogue",
    }
    assert "kingbird-svg" not in json.dumps(entries, sort_keys=True)


@pytest.mark.slow
def test_seed_witnesses_and_house_renderings_match_the_manifest() -> None:
    seed = json.loads(MANIFEST.read_text(encoding="utf-8"))["atlas_seed"]
    release = json.loads(UNITSQUARE_RESULTS.read_text(encoding="utf-8"))
    release_by_n = {record["n"]: record for record in release["results"]}
    for entry in seed["entries"]:
        n = entry["n"]
        witness_path = ROOT / entry["witness"]["path"]
        witness = load_witness(witness_path, fallback_schema=SCHEMA)
        assert witness["id"] == f"W-prospective-source-n{n:03d}"
        assert witness["n"] == n
        assert len(witness["squares"]) == n
        if entry["source"]["kind"] == "unitsquare-rendering":
            assert witness["source"]["revision"] == (
                f"upstream-declared parent-content SHA-256 {release_by_n[n]['record_sha256']}"
            )

        rendering = (ROOT / entry["rendering"]["path"]).read_text(encoding="utf-8")
        assert f"Prospective source construction for {n} unit squares" in rendering
        assert f'data-panel="n={n} prospective source construction"' in rendering
        assert "not an optimality or chunk-structure claim" in rendering
        assert 'data-feature="square-fill"' in rendering


def test_seed_sources_retain_attribution_without_local_hashes() -> None:
    seed = json.loads(MANIFEST.read_text(encoding="utf-8"))["atlas_seed"]
    sources = seed["retained_sources"]
    assert [source["n"] for source in sources] == [103, 105, 110, 131]
    assert all(source["creator"] == "UnitSquare Project" for source in sources)
    assert all(source["license"] == "CC-BY-4.0-in-dataset-page-metadata" for source in sources)
    for source in sources:
        assert (ROOT.parent / source["path"]).is_file()
    assert "sha256" not in json.dumps(seed, sort_keys=True)


def test_seed_cross_fields_reject_source_annotation_and_identity_mutations() -> None:
    """`seed_errors` is what the schema cannot say, so every mutation has to be refused.

    The seed under test is the committed manifest, not a fresh build. What this test
    needs is a *valid* seed to break in five specific ways, and the manifest is one --
    checked here in its unmutated form before anything is done to it, which is a
    statement the quick lane did not make before. Rebuilding the seed to obtain it cost
    124.86s on CI's two-core runner (run for `c1120c44`, job 101371257966): 101 witnesses
    and 101 renderings, billed in full to this test since `BC-214` deferred the neighbour
    that used to trigger the module-level memo first. `BC-218` measured that and recorded
    why marking this test `slow` cannot fix it -- in the deep surface the same test costs
    0.01s, because there the neighbour pays the build again.

    Nothing is dropped by reading the file. That the committed manifest *is* the built
    one is asserted by `test_seed_replays_every_safe_source_and_excludes_kingbird` in the
    deep surface's slow lane, and again by the full gate's `prospective n=101..324 source
    map and safe seed` step, which re-derives all 203 artifacts through
    `build_prospective_atlas --check`. The pair covers what one expensive test did.
    """
    seed = json.loads(MANIFEST.read_text(encoding="utf-8"))["atlas_seed"]
    assert not seed_errors(seed)
    mutations = []

    admitted_kingbird = deepcopy(seed)
    admitted_kingbird["entries"][0]["source"]["kind"] = "kingbird-svg"
    mutations.append(admitted_kingbird)

    annotated = deepcopy(seed)
    annotated["entries"][0]["annotation_status"] = "computed"
    mutations.append(annotated)

    aliased_witness = deepcopy(seed)
    aliased_witness["entries"][1]["witness"]["id"] = aliased_witness["entries"][0]["witness"][
        "id"
    ]
    mutations.append(aliased_witness)

    missing_source = deepcopy(seed)
    missing_source["retained_sources"].pop()
    mutations.append(missing_source)

    wrong_source_map = deepcopy(seed)
    wrong_source_map["source_map"]["path"] = "atlas/prospective/other.json"
    mutations.append(wrong_source_map)

    for mutation in mutations:
        assert seed_errors(mutation)


@pytest.mark.usefixtures("isolated_seed_build_cache")
def test_fetch_rejects_corrupted_retained_source_before_use(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(prospective, "SOURCE_ROOT", tmp_path)
    entry = next(
        entry
        for entry in prospective.eligible_entries()
        if entry["source_key"] == "unitsquare-release-1"
    )
    path = tmp_path / f"n{entry['n']:03d}.svg"
    path.write_text("<svg/>", encoding="utf-8")

    with pytest.raises(ValueError, match="hash mismatch against upstream declaration"):
        prospective.fetch(refresh=False)


def test_a_pool_worker_builds_the_same_bytes_as_this_process() -> None:
    """The seed is built across processes, and mpmath precision is per-process state.

    `mp.mp.dps` is a global a `forkserver` child does not inherit: a worker starts at
    mpmath's default of 15 digits whatever the parent set. Where that matters it is
    silent -- arithmetic at the wrong precision does not raise, it publishes different
    decimals into a retained witness, and a wrong decimal there reads as a coordinate
    rather than as a bug. It does not matter here, and measuring that rather than
    assuming it is why `build_cases` takes no pool `initializer`: the generated grid is
    exact rational arithmetic, `unitsquare_witness` sets its own working precision, and
    the renderer brackets what it needs.

    The control is that the precision gap is real and load bearing in the comparison.
    The same two cases are built at mpmath's default and at 300 digits, twenty times the
    precision, and the bytes have to match; the ambient value is checked between them,
    so the two builds demonstrably ran at different precision rather than at the same
    one twice. A second control keeps `==` honest: the two cases must compare unequal,
    so equality here is a measurement rather than a property of the operator.

    Two workers rather than four, because two is what the `sweeps` job exports as
    `--inner-jobs`, and passing the count explicitly is what makes this cover the pool
    even when the gate has capped `PACK_JOBS` at one.

    Both cases are generated grids, which is a cost decision and not a coverage one. A
    UnitSquare witness is 2.2s to build, so a pair of builds carrying one would be over
    the pull-request surface's marking threshold for a path the `sweeps` job already
    runs on every pull request over all 101 cases, byte for byte, at `--inner-jobs 2`.
    What that leaves uncovered here is the retained-source path, and the test below
    covers it directly.
    """
    entries = prospective.eligible_entries()
    selected = [
        entry for entry in entries if entry["source_key"] == "catalogue-trivial-grid-rule"
    ][:2]
    assert len(selected) == 2

    ambient = mp.mp.dps
    try:
        mp.mp.dps = 15
        at_default_precision = prospective.build_cases(selected, 1)
        mp.mp.dps = 300
        serial = prospective.build_cases(selected, 1)
        assert mp.mp.dps == 300
        pooled = prospective.build_cases(selected, 2)
    finally:
        mp.mp.dps = ambient

    assert [entry["n"] for _witness, _rendering, entry in serial] == [
        selected[0]["n"],
        selected[1]["n"],
    ]
    assert serial[0] != serial[1]
    assert serial == at_default_precision
    assert pooled == serial


def test_a_pool_worker_reads_the_retained_source_root_this_process_resolved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The retained source path is resolved here and travels with the unit, not read there.

    `_source_path` reads the module-level `SOURCE_ROOT`, and a `forkserver` worker
    re-imports this module rather than inheriting it, so module state a caller repointed
    does not cross the boundary with the work -- `clear_build_caches` exists for exactly
    such a caller. Left to resolve the root itself, a worker would read the real
    directory while this process read the substituted one and build four UnitSquare
    cases from bytes nobody asked for, without anything raising. `build_cases` resolves
    the path in this process instead and sends it in the payload.

    Failing rather than succeeding is what makes this a test and not a demonstration.
    The root is repointed at a directory holding no SVG at all, so a worker that used the
    payload cannot find the source and says so, naming the substituted directory; a
    worker that resolved `SOURCE_ROOT` for itself would find the real file and build
    successfully. It is also what makes the test cheap: it fails on the missing file,
    before the 2.2s parse a UnitSquare case would otherwise cost.
    """
    substitute = prospective.ROOT / "atlas/prospective"
    monkeypatch.setattr(prospective, "SOURCE_ROOT", substitute)
    entry = next(
        entry
        for entry in prospective.eligible_entries()
        if entry["source_key"] == "unitsquare-release-1"
    )

    with pytest.raises(ValueError, match="missing retained source") as failure:
        prospective.build_cases([entry], 2)

    assert "atlas/prospective" in str(failure.value)
    assert f"n={entry['n']}" in str(failure.value)
