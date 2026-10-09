#!/usr/bin/env python3
"""Coverage and source-adapter checks for the retained known-best atlas."""

from __future__ import annotations

import base64
import copy
import hashlib
import io
import json
import lzma
import re
import subprocess
import sys
import zlib
from collections import Counter
from collections.abc import Iterator, Sequence
from dataclasses import replace
from datetime import date
from decimal import Decimal
from functools import partial
from itertools import pairwise
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import cairocffi as cairo
import cairosvg
import jsonschema
import pytest
import yaml
from fontTools.ttLib import TTFont

from devtools import (
    atlas_credit_attributions,
    atlas_print_font,
    build_bound_citations,
    build_composite_figure_data,
    render_composite_pdf,
    rigidity_status,
)
from devtools import build_known_best_atlas as known_best_builder
from devtools import evand_arrangement_houses as evand_houses
from devtools import evand_arrangement_reports as evand_reports
from devtools import gupta_house_links as gupta_houses
from devtools import refinement_house_links as refinement_houses
from devtools import refinement_packets as refinement_sources
from devtools import ryxu_arrangement_reports as ryxu_reports
from devtools import ryxu_house_links as ryxu_houses
from devtools import ryxu_radical_n51 as ryxu_radical
from devtools.atlas_legend import AtlasLegendCounts, atlas_legend
from devtools.result_status import RecentContributions, recent_contributions_by_case
from sqpack.known_best import (
    ATLAS_SAMPLE_STRIDE,
    COMPOSITE_PDF_EDITION_DATE,
    CompositeSpec,
    CorpusRange,
    SourceGeometryError,
    catalogue_source_map,
    composite_pdf_name,
    parse_kingbird_svg,
    parse_unitsquare_svg,
    sampled_sequence,
)
from sqpack.release import (
    COMPOSITES_MAY_TRAIL,
    DATA_PATHS,
    PUBLICATION_VERSION,
    data_pathspec,
    edition_at,
)
from sqpack.render.color import ANGLE_CLASS_CONTRACT
from sqpack.render.model import RenderSpec
from sqpack.render.style import FIRST_PARTY_ACCENT_COLOR
from sqpack.render.svg import PRINT_FONT_MARKER, element, serialize_svg, sub
from sqpack.witness import load_witness
from sqpack.workers import worker_count
from sqpack.yamlio import safe_load

#: Catalogue-derived witnesses above the hand-audited hundred, per corpus (think-93on).
#: The first SQUISH update moved n = 179 and 258 onto packet-derived facts;
#: the second also moved n = 88. Complete evand and ry-xu packets now supersede
#: earlier catalogue sources. These inventory counts follow the current corpus.
GOLDEN_DERIVED_ABOVE_100: dict[str, int] = {"n=1..100": 0, "n=1..200": 23, "n=1..324": 50}
#: The cases whose retained upstream rendering is the UnitSquare release, per corpus.
GOLDEN_UNITSQUARE: dict[str, set[int]] = {
    # 68, 103, 105, 110 and 131 moved onto Francisco Couzo's packet on 2026-09-29, and 69
    # onto the catalogue's later side for the same packing on 2026-10-05 (T-088).
    "n=1..100": set(),
    "n=1..200": set(),
    "n=1..324": set(),
}
#: How the corpus splits by source kind at each corpus; a case switching kind fails here.
GOLDEN_SOURCE_KINDS: dict[str, dict[str, int]] = {
    "n=1..100": {
        "exact-grid": 64,
        "kingbird-derived-facts": 30,
        "packet-derived-facts": 6,
    },
    "n=1..200": {
        "exact-grid": 114,
        "kingbird-derived-facts": 53,
        "packet-derived-facts": 33,
    },
    "n=1..324": {
        "exact-grid": 176,
        "kingbird-derived-facts": 80,
        "packet-derived-facts": 68,
    },
}

#: What the poster's vector may cost a clone. Eight mebibytes is the ceiling the
#: encoding was chosen against; the house encoding would have spent 24 MB on the same
#: 52,650 squares. A ceiling rather than a golden size, because the exact figure follows
#: from the corpus's geometry and a witness gaining a digit may move it.
POSTER_SVG_BUDGET_BYTES = 8 * 1024 * 1024

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = ROOT.parent
ATLAS = ROOT / "atlas/known-best"
SOURCES = ROOT / "resources/web/known-best-packings"
WITNESSES = ROOT / "witnesses/known-best"
SCHEMA = ROOT / "witnesses/witness.schema.yaml"
UNITSQUARE_RESULTS = ROOT / "resources/web/unitsquare-release1-2026/results.json"
SVG = {"svg": "http://www.w3.org/2000/svg"}


def _assert_poster_text_clears_cards(
    information: ET.Element, canvas: known_best_builder.CompositeCanvas
) -> None:
    text_width = known_best_builder._text_width  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    positions = [canvas.card_position(n) for n in canvas.spec.numbers]
    for node in information.iter(f"{{{SVG['svg']}}}text"):
        x, y = Decimal(node.attrib["x"]), Decimal(node.attrib["y"])
        size = Decimal(node.attrib["font-size"])
        content = "".join(node.itertext())
        extent = text_width(content, str(size))
        extent += Decimal(node.attrib.get("letter-spacing", "0")) * max(len(content) - 1, 0)
        extent += sum((Decimal(span.attrib.get("dx", "0")) for span in node), Decimal(0))
        anchor = node.attrib.get("text-anchor", "start")
        left = x - extent if anchor == "end" else x - extent / 2 if anchor == "middle" else x
        right = left + extent
        for position in positions:
            assert (
                y + size * Decimal("0.3") <= position.top
                or y - size >= position.top + 242
                or right <= position.left
                or left >= position.left + 216
            ), (node.attrib.get("data-feature"), position)


@pytest.fixture
def isolated_atlas_build_cache():
    """For tests that repoint a source root.

    The builder memoizes the hundred cases so one process builds them once.
    A test that points UNITSQUARE_ROOT at a corrupted copy must neither read a
    memo built against the real root nor leave its own behind. Only those tests
    need this; clearing for every test would rebuild repeatedly and cost more
    than the memo saves.
    """
    known_best_builder.clear_build_caches()
    yield
    known_best_builder.clear_build_caches()


def test_catalogue_map_and_retained_unitsquare_geometry() -> None:
    source_page = ROOT / "resources/web/kingbird-squares-in-squares.html"
    catalogue = catalogue_source_map(source_page)
    assert catalogue[11] == ("square-11.svg", 11, (11,))
    assert catalogue[47] == ("square-48.svg", 48, (47, 48))

    prospective = catalogue_source_map(source_page, first_n=101, last_n=324)
    assert len(prospective) == 127
    assert len({record[0] for record in prospective.values()}) == 114
    assert prospective[119] == ("square-120.svg", 120, (119, 120))
    assert 111 not in prospective

    with pytest.raises(ValueError, match="nonempty and positive"):
        catalogue_source_map(source_page, first_n=324, last_n=101)

    release = json.loads(UNITSQUARE_RESULTS.read_text(encoding="utf-8"))
    release_by_n = {record["n"]: record for record in release["results"]}
    for n in (68, 69):
        geometry = parse_unitsquare_svg(
            (SOURCES / "unitsquare" / f"n{n:03d}.svg").read_text(encoding="utf-8"),
            expected_n=n,
        )
        assert len(geometry.squares) == n
        assert (
            geometry.upstream_declared_parent_content_sha256 == release_by_n[n]["record_sha256"]
        )


def test_kingbird_sources_are_metadata_only_derived_facts() -> None:
    assert not (SOURCES / "kingbird").exists()

    source_index = json.loads((SOURCES / "sources.json").read_text(encoding="utf-8"))
    assert source_index["contract"] == "packing.squares:KnownBestSourceInventory/v1"
    kingbird = [
        record
        for record in source_index["sources"]
        if record["kind"] == "kingbird-derived-facts"
    ]
    expected_n = {
        5,
        10,
        11,
        17,
        18,
        19,
        26,
        27,
        28,
        29,
        37,
        38,
        39,
        40,
        41,
        50,
        52,
        53,
        54,
        55,
        65,
        66,
        67,
        69,
        71,
        82,
        83,
        85,
        87,
        89,
    }
    # The hand-audited hundred stay a literal; above it the count of derived records is
    # pinned per corpus, so a case silently switching source kind still fails.
    assert {record["n"] for record in kingbird if record["n"] <= 100} == expected_n
    above = sorted(record["n"] for record in kingbird if record["n"] > 100)
    assert len(above) == GOLDEN_DERIVED_ABOVE_100[known_best_builder.CORPUS.label]
    assert len(kingbird) == len(expected_n) + len(above)
    for record in kingbird:
        assert record["attribution"].startswith("SVG and high-precision updates")
        # Above the hundred a catalogue picture can serve two sizes (147 is the 148
        # picture with a square removed), so the record names the picture's own n.
        assert record["n"] in record["listed_n"]
        assert record["source_n"] == max(record["listed_n"])
        if record["n"] <= 100:
            assert record["listed_n"] == [record["n"]]
        assert record["raw_asset_retained"] is False
        assert record["license_status"] == "no-express-reuse-terms-found"
        assert record["retention_policy"] == "metadata-and-derived-numerical-facts-only"
        assert {"bytes", "path", "sha256"}.isdisjoint(record)

    unitsquare = [
        record for record in source_index["sources"] if record["kind"] == "unitsquare-rendering"
    ]
    release = json.loads(UNITSQUARE_RESULTS.read_text(encoding="utf-8"))
    release_by_n = {record["n"]: record for record in release["results"]}
    assert {record["n"] for record in unitsquare} == GOLDEN_UNITSQUARE[
        known_best_builder.CORPUS.label
    ]
    for record in unitsquare:
        assert record["raw_asset_retained"] is True
        assert record["bytes"] > 0
        assert record["upstream_declared_sha256"] == release_by_n[record["n"]]["svg_sha256"]
        assert "sha256" not in record
        path = ROOT / record["path"]
        assert path.is_file()
        assert (
            hashlib.sha256(path.read_bytes()).hexdigest() == record["upstream_declared_sha256"]
        )


def _packet_acquisition(packet: Path) -> tuple[str, dict[str, str]]:
    """The revision a packet acquired its source at, and each upstream file's SHA-256 by
    its path in the source tree, read from the packet's own acquisition record."""
    acquisition = packet / "acquisition"
    inputs = acquisition / "upstream-factual-inputs.json"
    if inputs.is_file():
        record = json.loads(inputs.read_text(encoding="utf-8"))
        return record["revision"], {row["path"]: row["sha256"] for row in record["files"]}
    (source,) = json.loads((acquisition / "sources.json").read_text(encoding="utf-8"))[
        "sources"
    ]
    manifest = (acquisition / "upstream-subtree.sha256").read_text(encoding="utf-8")
    digests = {}
    for line in manifest.splitlines():
        digest, name = line.split(maxsplit=1)
        digests[name.removeprefix("./")] = digest
    return source["source_commit"], digests


def _retained_container(path: Path) -> dict[str, Any]:
    assert path.name.endswith(".json.xz"), path
    return json.loads(lzma.decompress(path.read_bytes()))


def _assert_container_retains(
    row: dict[str, Any], container: dict[str, Any], acquisition: tuple[str, dict[str, str]]
) -> None:
    """The container's one entry for the row's `url` is the upstream file's exact text."""
    revision, digests = acquisition
    assert container["revision"] == revision, row["url"]
    entries = [
        entry
        for entry in container["cases"]
        if f"{container['source']}/blob/{revision}/{entry['source_path']}" == row["url"]
    ]
    assert len(entries) == 1, row["url"]
    (entry,) = entries
    assert entry["n"] == row["source_n"], row["url"]
    retained = hashlib.sha256(entry["source_certificate"].encode("utf-8")).hexdigest()
    assert retained == digests[entry["source_path"]], row["url"]


def test_every_retained_packet_source_holds_its_upstream_bytes() -> None:
    """A packet row marked `raw_asset_retained` keeps the file its `url` names, byte for
    byte: the builder marks a row so when its `path` is a complete-certificate container
    (`build_known_best_atlas._source_index`), and the container's entry for that url
    carries the SHA-256 the packet's acquisition record pinned upstream."""
    source_index = json.loads((SOURCES / "sources.json").read_text(encoding="utf-8"))
    rows = [
        record
        for record in source_index["sources"]
        if record["kind"] == "packet-derived-facts" and record["raw_asset_retained"]
    ]
    assert rows
    containers: dict[str, dict[str, Any]] = {}
    for row in rows:
        path = ROOT / row["path"]
        if row["path"] not in containers:
            containers[row["path"]] = _retained_container(path)
        _assert_container_retains(
            row, containers[row["path"]], _packet_acquisition(path.parent.parent)
        )


@pytest.mark.parametrize("change", ["edited text", "other revision"])
def test_a_retained_source_row_refuses_a_copy_that_is_not_upstream(change: str) -> None:
    path = ryxu_reports.fact_path()
    container = _retained_container(path)
    acquisition = _packet_acquisition(path.parent.parent)
    url = ryxu_houses.source_url(70)
    row = {"path": path.relative_to(ROOT).as_posix(), "source_n": 70, "url": url}
    _assert_container_retains(row, container, acquisition)
    if change == "edited text":
        entry = next(entry for entry in container["cases"] if entry["n"] == 70)
        edited = entry["source_certificate"].replace("1", "2", 1)
        assert edited != entry["source_certificate"]
        entry["source_certificate"] = edited
    else:
        row["url"] = url.replace(ryxu_reports.REVISION, "0" * 40)
    with pytest.raises(AssertionError):
        _assert_container_retains(row, container, acquisition)


@pytest.mark.usefixtures("isolated_atlas_build_cache")
def test_known_best_rejects_corrupted_retained_unitsquare_svg(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # No case reports the release since n = 69 moved to the catalogue (T-088), so the
    # guard is driven through a plan for a record that would: the corpus build no longer
    # reaches it, and a corrupted retained rendering must still be refused.
    source = SOURCES / "unitsquare/n069.svg"
    monkeypatch.setattr(known_best_builder, "UNITSQUARE_ROOT", tmp_path)
    (tmp_path / "n069.svg").write_bytes(source.read_bytes() + b"\n")
    plan = _plan_for(_case(69, "8.8272055078159206568807", "[UnitSquare 2026]"))
    assert plan.path == tmp_path / "n069.svg"

    with pytest.raises(ValueError, match="upstream-declared SVG SHA-256"):
        known_best_builder._source_index({69: plan})  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001


@pytest.mark.parametrize(
    ("svg", "kind"),
    [
        (
            (
                '<svg xmlns="http://www.w3.org/2000/svg">'
                '<rect id="outer" width="2" height="3" fill="none"/>'
                "</svg>"
            ),
            "outer-frame-not-square",
        ),
        (
            (
                '<svg xmlns="http://www.w3.org/2000/svg">'
                '<rect id="outer" width="2" height="2" fill="none"/>'
                '<path d="M0 0 C0 1 1 1 1 0 Z"/>'
                "</svg>"
            ),
            "unsupported-path",
        ),
    ],
)
def test_kingbird_adapter_rejects_unsupported_source_geometry(svg: str, kind: str) -> None:
    with pytest.raises(SourceGeometryError) as captured:
        parse_kingbird_svg(svg)

    assert captured.value.kind == kind


def test_kingbird_adapter_uses_first_duplicate_id_in_tree_order() -> None:
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<defs><rect id="outer" width="3" height="3" fill="none"/>'
        '<rect id="one" width="1" height="1"/>'
        '<g id="two"><rect id="one" width="2" height="1"/></g></defs>'
        '<use href="#one"/><use href="#one" x="1"/><use href="#one" x="2"/>'
        "</svg>"
    )

    geometry = parse_kingbird_svg(svg, expected_n=3)

    assert len(geometry.poses) == 3


@pytest.mark.parametrize(
    "href", ["missing", "#missing", "packing.svg#one", "https://example/one"]
)
def test_kingbird_adapter_rejects_nonlocal_or_unresolved_use(href: str) -> None:
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<defs><rect id="outer" width="2" height="2" fill="none"/>'
        '<rect id="one" width="1" height="1"/></defs>'
        f'<use href="{href}"/>'
        "</svg>"
    )

    with pytest.raises(SourceGeometryError) as captured:
        parse_kingbird_svg(svg)

    assert captured.value.kind == "broken-reference"


def test_kingbird_adapter_ignores_bare_local_use_only_after_count_reconciliation() -> None:
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<defs><rect id="outer" width="2" height="2" fill="none"/></defs>'
        '<g id="corner"><rect width="2" height="1"/></g>'
        '<use href="corner" y="1"/>'
        "</svg>"
    )

    with pytest.raises(SourceGeometryError) as missing_count:
        parse_kingbird_svg(svg)
    with pytest.raises(SourceGeometryError) as wrong_count:
        parse_kingbird_svg(svg, expected_n=4)
    geometry = parse_kingbird_svg(svg, expected_n=2)

    assert missing_count.value.kind == "broken-reference"
    assert wrong_count.value.kind == "broken-reference"
    assert len(geometry.poses) == 2


def test_known_best_atlas_covers_every_frontier_case() -> None:
    document = json.loads((ATLAS / "manifest.json").read_text(encoding="utf-8"))
    release = json.loads(UNITSQUARE_RESULTS.read_text(encoding="utf-8"))
    release_by_n = {record["n"]: record for record in release["results"]}
    assert document["softschema"]["contract"] == "packing.squares:KnownBestAtlas/v1"
    entries = document["atlas"]["entries"]
    # A list, because the corpus can publish more than one composite of itself. The
    # values are the golden ones for this figure: every number here is computed from
    # `known_best_builder.PRIMARY_COMPOSITE`, and these are what the formulas return.
    assert document["atlas"]["composites"] == [
        {
            "columns": 10,
            "layout": "10 by 10, row-major n=1..100",
            "png_high_resolution": {
                "derived_from": "atlas/known-best/known-best-1-100.svg",
                "height": 8046,
                "path": "atlas/known-best/known-best-1-100@2x.png",
                "scale": 2,
                "width": 4520,
            },
            "png_link_preview_card": {
                "derived_from": "atlas/known-best/known-best-1-100.svg",
                "height": 1256,
                "path": "atlas/known-best/known-best-1-100-card.png",
                "scale": 1,
                "top_crop": True,
                "width": 2260,
            },
            "png_preview": {
                "derived_from": "atlas/known-best/known-best-1-100.svg",
                "height": 4023,
                "path": "atlas/known-best/known-best-1-100.png",
                "scale": 1,
                "width": 2260,
            },
            "range": {"count": 100, "first_n": 1, "last_n": 100},
            "renderer": "sqpack deterministic composite renderer",
            "rows": 10,
            "square_count": 5050,
            "stem": "known-best-1-100",
            "svg": {
                "height": 4023,
                "path": "atlas/known-best/known-best-1-100.svg",
                "width": 2260,
            },
        },
        # Eighteen complete rows share a right edge at the retained drawing scale.
        # One raster and no link-preview crop; the PDF carries detail at any zoom.
        {
            "columns": 35,
            "layout": "35 by 18, right-aligned square-bound triangle n=1..324",
            "png_preview": {
                "derived_from": "atlas/known-best/known-best-1-324.svg",
                "height": 5701,
                "path": "atlas/known-best/known-best-1-324.png",
                "scale": 1,
                "width": 7871,
            },
            "range": {"count": 324, "first_n": 1, "last_n": 324},
            "renderer": "sqpack deterministic composite renderer",
            "rows": 18,
            "square_count": 52650,
            "stem": "known-best-1-324",
            "svg": {
                "height": 5701,
                "path": "atlas/known-best/known-best-1-324.svg",
                "width": 7871,
            },
        },
    ]
    corpus = known_best_builder.CORPUS
    assert document["atlas"]["range"] == {
        "count": corpus.count,
        "first_n": corpus.first_n,
        "last_n": corpus.last_n,
    }
    assert [entry["n"] for entry in entries] == list(corpus.numbers)
    assert (
        Counter(entry["source"]["kind"] for entry in entries)
        == GOLDEN_SOURCE_KINDS[corpus.label]
    )

    # The record-level checks reach every case; the witness files themselves, which are
    # the expensive part (a schema-validated load of a 30 KB YAML each, 8 s of call time
    # over 324 on this host and past the quick lane's 12 s ceiling on the hosted
    # runner), are opened on the atlas sample's own stride here and on every case in
    # the slow twin below -- the same split the gate makes for the atlas rebuild.
    sampled = set(sampled_sequence([entry["n"] for entry in entries], ATLAS_SAMPLE_STRIDE))
    for entry in entries:
        n = entry["n"]
        assert (ROOT / entry["witness"]["path"]).is_file()
        assert (ROOT / entry["rendering"]["path"]).is_file()
        frontier = (ROOT / entry["frontier_path"]).read_text(encoding="utf-8")
        case = safe_load(frontier.split("---\n", 2)[1])["packing"]
        assert entry["witness"]["id"] in case["reported_upper_bound"]["witnesses"]
        if n in sampled:
            _assert_witness_agrees_with_entry(entry, release_by_n)

    n29_frontier = (ROOT / "frontier/n-029.md").read_text(encoding="utf-8")
    assert "    - W-n029-kingbird\n" in n29_frontier


def _assert_witness_agrees_with_entry(entry: dict, release_by_n: dict) -> None:
    n = entry["n"]
    if n in ryxu_houses.NUMBERS and entry["source"]["url"] == ryxu_houses.source_url(n):
        assert ROOT / entry["witness"]["path"] == ryxu_houses.house_path(n)
    witness = load_witness(ROOT / entry["witness"]["path"], fallback_schema=SCHEMA)
    assert witness["n"] == n
    assert witness["id"] == entry["witness"]["id"]
    assert len(witness["squares"]) == n
    if entry["source"]["kind"] == "kingbird-derived-facts":
        assert entry["source"]["path"] == ("resources/web/known-best-packings/sources.json")
        assert witness["source"]["key"] == "Kingbird derived numerical facts"
        assert witness["source"]["path"] == entry["source"]["path"]
        assert "not a legal conclusion" in witness["claim"]["limitations"]
    elif entry["source"]["kind"] == "packet-derived-facts":
        assert entry["source"]["path"].startswith("resources/web/")
        evand_url = (
            f"{evand_reports.SOURCE}/blob/{evand_reports.REVISION}/{evand_reports.source_path(n)}"
            if n in evand_houses.NUMBERS
            else None
        )
        source = refinement_houses.source(n) if n in refinement_houses.NUMBERS else None
        if (
            n in gupta_houses.NUMBERS
            and witness["source"]["key"] == gupta_houses.reports.SOURCE_KEY
        ):
            assert ROOT / entry["witness"]["path"] == gupta_houses.house_path(n)
            assert (
                entry["source"]["path"]
                == gupta_houses.reports.fact_path().relative_to(ROOT).as_posix()
            )
            assert witness["source"]["path"] == entry["source"]["path"]
            gupta_houses.check_houses([n])
        elif n in ryxu_houses.NUMBERS and entry["source"]["url"] == ryxu_houses.source_url(n):
            # Complete rational and number-field records retain all poses and deciding
            # inputs. Admit their entire house; a matching path alone is insufficient.
            facts = ryxu_radical.fact_path() if n == 51 else ryxu_reports.fact_path()
            assert entry["source"]["path"] == facts.relative_to(ROOT).as_posix()
            assert witness == ryxu_houses.check_houses([n])[n]
            assert witness["source"]["path"] == entry["source"]["path"]
        elif entry["source"]["url"] == evand_url:
            assert (
                entry["witness"]["path"]
                == evand_houses.house_path(n).relative_to(ROOT).as_posix()
            )
            assert (
                entry["source"]["path"]
                == evand_reports.fact_path().relative_to(ROOT).as_posix()
            )
            assert witness["source"]["path"] == "packing/" + entry["source"]["path"]
            evand_houses.check_houses([n])
        elif source is not None and entry["source"]["url"] == source.url(n):
            assert entry["source"]["path"].endswith(
                (f"/facts/n-{n:03d}.yaml", f"/facts/n-{n:03d}.json.gz")
            )
            # New source facts use repository-relative custody paths. Admit the whole
            # imported house, not merely an accepted alternative path spelling.
            assert witness["source"] == refinement_sources.to_witness(source, n)["source"]
            assert witness["source"]["path"] == "packing/" + entry["source"]["path"]
            refinement_houses.check_houses([n])
        else:
            assert entry["source"]["path"].endswith(
                (f"/facts/n-{n:03d}.yaml", f"/facts/n-{n:03d}.json.gz")
            )
            assert witness["source"]["path"] == entry["source"]["path"]
            assert "not a legal conclusion" in witness["claim"]["limitations"]
        assert witness["source"]["url"] == entry["source"]["url"]
    elif entry["source"]["kind"] == "unitsquare-rendering":
        assert witness["source"]["revision"] == (
            f"upstream-declared parent-content SHA-256 {release_by_n[n]['record_sha256']}"
        )


@pytest.mark.parametrize("n", [51, 70])
def test_ryxu_manifest_refuses_a_noncanonical_house_path(n: int) -> None:
    document = json.loads((ATLAS / "manifest.json").read_text(encoding="utf-8"))
    entry = next(row for row in document["atlas"]["entries"] if row["n"] == n)
    changed = {**entry, "witness": {**entry["witness"], "path": "witnesses/other-house.yaml"}}
    with pytest.raises(AssertionError):
        _assert_witness_agrees_with_entry(changed, {})


@pytest.mark.slow
def test_every_known_best_witness_agrees_with_its_manifest_entry() -> None:
    """The whole-corpus copy of the sampled check above, on the slow lane."""
    document = json.loads((ATLAS / "manifest.json").read_text(encoding="utf-8"))
    release = json.loads(UNITSQUARE_RESULTS.read_text(encoding="utf-8"))
    release_by_n = {record["n"]: record for record in release["results"]}
    for entry in document["atlas"]["entries"]:
        _assert_witness_agrees_with_entry(entry, release_by_n)


def test_known_best_v1_schema_accepts_a_manifest_without_the_new_composite() -> None:
    atlas = json.loads((ATLAS / "manifest.json").read_text(encoding="utf-8"))["atlas"]
    atlas.pop("composites")
    schema = yaml.safe_load(
        (ATLAS / "known-best-atlas.schema.yaml").read_text(encoding="utf-8")
    )

    jsonschema.validate(atlas, schema)


def test_known_best_schema_accepts_current_poster_dimensions_and_rejects_drift() -> None:
    atlas = json.loads((ATLAS / "manifest.json").read_text(encoding="utf-8"))["atlas"]
    schema = yaml.safe_load(
        (ATLAS / "known-best-atlas.schema.yaml").read_text(encoding="utf-8")
    )
    validator = jsonschema.Draft202012Validator(schema)
    atlas["composites"] = [
        known_best_builder._composite_record(canvas)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        for canvas in known_best_builder.resolved_composites(atlas["entries"])
    ]
    validator.validate(atlas)
    changed_layout = copy.deepcopy(atlas)
    poster = next(
        composite
        for composite in changed_layout["composites"]
        if composite["stem"] == "known-best-1-324"
    )
    poster["layout"] = "35 by 18, left-aligned square-bound triangle n=1..324"
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(changed_layout)
    for export in ("svg", "png_preview"):
        for dimension in ("width", "height"):
            changed = copy.deepcopy(atlas)
            poster = next(
                composite
                for composite in changed["composites"]
                if composite["stem"] == "known-best-1-324"
            )
            poster[export][dimension] -= 1
            with pytest.raises(jsonschema.ValidationError):
                validator.validate(changed)


def _committed_composite_svg() -> str:
    """The retained composite vector, read the way its drift checks compare it.

    Four tests below ask what the composite *contains* or what an export was drawn
    *from*, and a valid composite answers both; none of them needs a freshly built one.
    Building it costs about 80s on CI's two-core runner and was billed to whichever of
    them ran first in each xdist worker, which is why two of them reported 82.00s and
    78.78s against a 5s per-test ceiling (run for `c1120c44`, job 101371257966). `BC-214`
    deferred the neighbour that used to pay it; `BC-218` measured that the cost belongs
    to the build rather than to any test, so no marker can place it.

    `read_text(encoding="utf-8")` rather than the bytes, deliberately: it is what
    `test_known_best_composite_contains_every_case_and_square` compares below and what
    `build_known_best_atlas.check()` compares in the full gate, so what those two pin is
    exactly the string these tests read, and the substitution composes rather than
    nearly composes.
    """
    return (ATLAS / "known-best-1-100.svg").read_text(encoding="utf-8")


#: The cases the retained `n = 1..100` poster prints as an exact value: the 45 of its
#: drawing. A poster trails the data until the next version redraws it
#: (`sqpack.release.COMPOSITES_MAY_TRAIL`), so when it is redrawn this pin fails and moves
#: to `REBUILT_EQUALITIES`.
RETAINED_EQUALITIES = frozenset(
    {
        *range(1, 12),
        *range(13, 17),
        *range(21, 26),
        *range(32, 37),
        *range(45, 50),
        *range(59, 65),
        *range(77, 82),
        *range(97, 101),
    }
)
#: What a rebuild from the current records prints: the same 45, including the five cases
#: proved here on 2026-10-02 by replayed mixed covers, s(59) = s(60) = s(61) = 8 and
#: s(77) = s(78) = 9, and s(97) = 10, proved on 2026-10-03 as the case k = 10 of T-064's
#: s(k^2 - 3) = k, the one count up to 100 that family adds.
REBUILT_EQUALITIES = RETAINED_EQUALITIES


def _assert_current_composite_equalities(bounds: list[str], expected: frozenset[int]) -> None:
    assert len(bounds) == 100
    assert all(re.fullmatch(r"s\(\d+\) [=≤] .+", bound) for bound in bounds)
    assert all(bound.startswith(f"s({n}) ") for n, bound in enumerate(bounds, 1))
    equalities = {n for n, bound in enumerate(bounds, 1) if " = " in bound}
    assert equalities == expected
    assert bounds[10] == "s(11) = 3.877084"
    figure = json.loads((ATLAS / "composite-figure.json").read_text(encoding="utf-8"))["figure"]
    n11 = next(entry for entry in figure["entries"] if entry["n"] == 11)
    assert n11["optimality"]["status"] == "proved"
    assert n11["lower"]["evidence"] == ["E-n011-global-optimality-independent"]


def test_retained_composite_equalities_match_classified_cases() -> None:
    root = ET.fromstring(_committed_composite_svg())
    bounds = [
        "".join(node.itertext())
        for node in root.findall(".//svg:text[@data-feature='side-bound']", SVG)
    ]
    _assert_current_composite_equalities(bounds, RETAINED_EQUALITIES)


def test_a_pool_worker_builds_the_same_bytes_as_this_process() -> None:
    """The corpus is built across processes, and every derived byte must be unmoved.

    `build_known_best_atlas` gained a pool on 2026-09-07 because the widened corpus made
    its check 691.19s; four workers took that to 184.34s. What a pool can quietly cost is
    a differently rounded output, because a `spawn` child inherits none of this process's
    global arithmetic state -- and the failure would be silent, since a witness rounded
    at a different precision is still a witness.

    So the comparison is on bytes rather than on a status, and it is over a range that
    reaches all three source layers: an exact grid (n=4), a Kingbird-derived record
    (n=11) and a UnitSquare rendering (n=68). `built_cases` is called directly, because
    what needs checking is the path the tool takes rather than a re-implementation of it.

    Not marked `slow`: three cases is a second or two, and the property is one a pull
    request should learn about rather than a merge.
    """
    numbers = (4, 11, 68)
    serial = known_best_builder.built_cases(numbers, 1)
    pooled = known_best_builder.built_cases(numbers, 2)

    assert [item.frontier.n for item in serial] == list(numbers)
    assert [item.witness_text for item in pooled] == [item.witness_text for item in serial]
    assert [item.rendering_text for item in pooled] == [item.rendering_text for item in serial]
    assert [item.witness for item in pooled] == [item.witness for item in serial]


@pytest.mark.slow
@pytest.mark.pool_heavy
def test_known_best_composite_contains_every_case_and_square() -> None:
    # Pooled rather than serial, and the count comes from the same policy every other
    # pool-backed step reads: `PACK_JOBS` where a gate has capped it, the machine where
    # nothing has. This is the one test that pays the whole corpus build, and at
    # `n=1..324` that is 691.19s serial against 348.15s at two workers -- the deep gate
    # runs the slow lane at `--inner-jobs 2`, so this is what it costs there. The build is
    # memoized on the worker count, so the serial memo the corrupted-source test above
    # builds is untouched by this one.
    workers = worker_count(known_best_builder.CORPUS.count)
    outputs, _manifest = known_best_builder.expected_outputs(workers)
    composite_path = ATLAS / "known-best-1-100.svg"
    canvas = known_best_builder.PRIMARY_COMPOSITE
    assert canvas.svg_path == composite_path

    # The composites are not part of the data layer `--update` writes: they are drawn
    # apart, under the record of the data each was drawn from, and redrawn on demand.
    assert not any(item.svg_path in outputs for item in known_best_builder.COMPOSITES)
    retained = composite_path.read_text(encoding="utf-8")
    identity = known_best_builder.retained_identity(retained)
    rebuilt = known_best_builder.expected_composite(canvas, identity, workers)

    # A composite is drawn from the retained witnesses, which costs seconds where this
    # rebuild costs minutes. That is sound exactly when the two drawings are one, which
    # is held here for the figure and by `--check` for every witness it is drawn from.
    cards = known_best_builder.retained_cases(canvas.spec.numbers)
    assert known_best_builder.render_known_best_summary_svg(cards, canvas, identity) == rebuilt

    # The pin the quick lane's four composite tests stand on: they read the retained
    # vector, and this is where "retained" and "built" are made one thing inside pytest.
    # Free here -- the build above is already paid -- and checked again from the other
    # side by the full gate's `known-best n=1..324 atlas rebuild` step. A composite that
    # trails the pin may differ from the rebuild (`sqpack.release`, rule 5), and then the
    # quick lane's tests describe the drawing as it was released.
    if identity.current or not COMPOSITES_MAY_TRAIL:
        assert retained == rebuilt

    root = ET.fromstring(rebuilt)
    metadata = {
        node.attrib["name"]: node.text or ""
        for node in root.iter()
        if node.tag.endswith("}value") and "name" in node.attrib
    }
    spec = RenderSpec()
    expected_color_metadata = {
        "angle-class-contract": ANGLE_CLASS_CONTRACT,
        "color-angle-tolerance-radians": str(spec.angle_tolerance_radians),
        "color-full-side-contact-tolerance": str(spec.full_side_contact_tolerance),
        "color-hue-count": str(spec.hue_count),
        "color-hue-scheme": spec.hue_scheme.value,
        "color-shade-lightness-span": str(spec.shade_lightness_span),
        "color-shade-scheme": spec.shade_scheme.value,
        "color-shades-per-hue": str(spec.shades_per_hue),
    }
    assert expected_color_metadata.items() <= metadata.items()
    cards = root.findall(".//svg:g[@data-n]", SVG)
    assert [int(card.attrib["data-n"]) for card in cards] == list(range(1, 101))
    assert len(root.findall(".//svg:polygon[@data-feature='square-fill']", SVG)) == 5050
    assert [card.attrib["data-row"] for card in cards[:10]] == ["0"] * 10
    assert [card.attrib["data-column"] for card in cards[:10]] == [
        str(column) for column in range(10)
    ]

    labels = [
        node.text for node in root.findall(".//svg:text[@data-feature='packing-label']", SVG)
    ]
    # The bound is split into tspans so the variable s can be italic, so join
    # the runs rather than reading the element's own text.
    bounds = [
        "".join(node.itertext())
        for node in root.findall(".//svg:text[@data-feature='side-bound']", SVG)
    ]
    assert labels == [str(n) for n in range(1, 101)]
    # The slow rebuild and the quick retained-vector control share the same contract, each
    # against its own data: the rebuild reads the current records, and the retained poster
    # may trail them until the next version.
    _assert_current_composite_equalities(bounds, REBUILT_EQUALITIES)


def test_known_best_composite_png_is_derived_from_current_svg() -> None:
    svg_text = _committed_composite_svg()
    png = (ATLAS / "known-best-1-100.png").read_bytes()

    assert known_best_builder.png_summary_receipt(png) == (
        2260,
        4023,
        hashlib.sha256(svg_text.encode("utf-8")).hexdigest(),
    )


def test_known_best_composite_high_resolution_png_is_derived_from_current_svg() -> None:
    """The 2x export is pinned to the same canvas and the same source as the preview.

    It exists so the atlas can be attached or downscaled without going back to the
    vector, which means it is the copy most likely to be handed to someone who cannot
    check it. Pinning the exact pixel count matters as much as pinning the receipt:
    4520 by 8046 is twice 2260 by 4023, and the whole-number scale is what keeps the
    file small. A fractional scale puts every edge on a fractional pixel boundary, and
    the antialiasing shades the rasteriser then invents cost more bytes than the extra
    pixels do -- a 4096-wide export of this drawing is 11% larger than this one while
    carrying 27% fewer pixels.
    """
    svg_text = _committed_composite_svg()
    png = (ATLAS / "known-best-1-100@2x.png").read_bytes()

    assert known_best_builder.png_summary_receipt(png) == (
        4520,
        8046,
        hashlib.sha256(svg_text.encode("utf-8")).hexdigest(),
    )


def test_known_best_composite_exports_all_carry_one_source_receipt() -> None:
    """Every export of the composite names the same SVG, so they cannot disagree.

    The vector, both rasters and the PDF are one family drawn in one `--update` run.
    What makes "the PNG matches the PDF" checkable rather than asserted is that all
    four receipts are the digest of the same source: two rasterisers of one drawing
    differ only in how they antialias an edge, whereas two drawings differ in what
    they show. This is the pin that would fail if an export were refreshed alone.
    """
    svg_text = _committed_composite_svg()
    expected = hashlib.sha256(svg_text.encode("utf-8")).hexdigest()

    receipts = {
        export.path.name: known_best_builder.png_summary_receipt(export.path.read_bytes())[2]
        for export in known_best_builder.PRIMARY_COMPOSITE.rasters
    }
    receipts["square-packings-100-20261008.pdf"] = render_composite_pdf.pdf_receipt(
        (ATLAS / "square-packings-100-20261008.pdf").read_bytes()
    )

    assert set(receipts) == {
        "known-best-1-100.png",
        "known-best-1-100@2x.png",
        "known-best-1-100-card.png",
        "square-packings-100-20261008.pdf",
    }
    assert set(receipts.values()) == {expected}


def test_known_best_composite_rasters_scale_the_one_canvas_by_whole_numbers() -> None:
    """Every raster is a whole multiple of the canvas, in width always and in height
    unless it declares a crop.

    The dimensions are derived from the composite's own canvas rather than stored, so a
    resized canvas moves every export together. This pins the facts that derivation
    relies on: the scales are integers, no two exports collide on one path or on one
    manifest key, and a cropped export is shorter than the canvas rather than a
    differently scaled drawing -- the link-preview card is the top of the same picture,
    not a second one.
    """
    canvas = known_best_builder.PRIMARY_COMPOSITE
    exports = canvas.rasters

    assert sorted(export.scale for export in exports) == [1, 1, 2]
    assert len({export.path for export in exports}) == len(exports)
    assert len({export.manifest_key for export in exports}) == len(exports)
    for export in exports:
        assert (export.canvas_width, export.canvas_height) == (canvas.width, canvas.height)
        assert export.width == canvas.width * export.scale
        if export.crop_units is None:
            assert export.height == canvas.height * export.scale
            continue
        assert export.height == export.crop_units * export.scale
        assert 0 < export.crop_units < canvas.height
    # Exactly one crop, and it is the card the page's link preview names.
    cropped = [export for export in exports if export.crop_units is not None]
    assert [export.path.name for export in cropped] == ["known-best-1-100-card.png"]


def test_the_1_100_canvas_is_what_its_specification_computes() -> None:
    """Pin content-derived footer geometry without moving the ten-by-ten drawing grid.

    The black definition is 26.125 units; body text is 19 units. The three shared
    credit paragraphs use ink-measured section gaps and give a 4023-unit page height.
    Literal baselines hold the maintained derivation to the published drawing.
    """
    canvas = known_best_builder.PRIMARY_COMPOSITE
    composite = canvas.spec

    assert (composite.first_n, composite.last_n, composite.columns) == (1, 100, 10)
    assert (composite.count, composite.rows, composite.square_count) == (100, 10, 5050)
    assert composite.layout == "10 by 10, row-major n=1..100"
    assert composite.card_units == 1256
    assert (canvas.width, canvas.height) == (2260, 4023)
    assert canvas.grid_bottom == 3244
    assert float(canvas.legend_baseline) == pytest.approx(3409.53936767578125)
    assert float(canvas.explainer_baseline) == pytest.approx(3292.930419921875)
    assert canvas.citations_baseline == 114
    assert float(canvas.credit_baseline) == pytest.approx(3965.13165283203125)
    assert float(canvas.stamp_baseline) == pytest.approx(3993.63165283203125)
    assert (composite.svg_name, composite.pdf_name) == (
        "known-best-1-100.svg",
        "square-packings-100-20261008.pdf",
    )
    assert composite.raster_name(1) == "known-best-1-100.png"
    assert composite.raster_name(2) == "known-best-1-100@2x.png"
    assert composite.card_png_name == "known-best-1-100-card.png"


def test_published_pdf_paths_use_fixed_edition_names_and_generic_stems_keep_their_name(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert COMPOSITE_PDF_EDITION_DATE == "20261008"
    monkeypatch.setattr(render_composite_pdf, "ATLAS_ROOT", tmp_path)
    for canvas, expected in zip(
        known_best_builder.COMPOSITES,
        ("square-packings-100-20261008.pdf", "square-packings-324-20261008.pdf"),
        strict=True,
    ):
        assert composite_pdf_name(canvas.spec.stem) == canvas.spec.pdf_name == expected
        assert render_composite_pdf.composite_pdf(canvas.spec.stem) == tmp_path / expected
        assert canvas.spec.svg_name == f"{canvas.spec.stem}.svg"
    generic = CompositeSpec(1, 1, 1, "synthetic")
    assert composite_pdf_name(generic.stem) == generic.pdf_name == "synthetic.pdf"
    assert render_composite_pdf.composite_pdf(generic.stem) == tmp_path / "synthetic.pdf"


def test_the_poster_canvas_is_what_its_specification_computes() -> None:
    """The poster's numbers, as the golden answer to the same formulas.

    Eighteen complete rows retain the figure's card scale and share a right edge.
    The thirty-five-column envelope has 120-unit outside margins and shares the
    same 307-unit row pitch as the primary figure.
    """
    canvas = known_best_builder.resolved_composites()[1]
    composite = canvas.spec

    assert (composite.first_n, composite.last_n, composite.columns) == (1, 324, 35)
    assert (composite.count, composite.rows, composite.square_count) == (324, 18, 52650)
    assert composite.square_count == 324 * 325 // 2
    assert composite.layout == "35 by 18, right-aligned square-bound triangle n=1..324"
    assert composite.cases.label == "n=1..324"
    assert (canvas.width, canvas.height) == (7871, 5701)
    assert (canvas.physical_columns, canvas.physical_rows) == (35, 18)
    assert canvas.grid_top == 120
    assert canvas.grid_bottom == 120 + 18 * 307 == 5646
    assert canvas.height == 120 + 17 * 307 + 242 + 120 == 5701
    assert (canvas.information_left, canvas.information_right) == (204, 2804)
    assert float(canvas.legend_baseline) == pytest.approx(778.7511853125)
    assert float(canvas.explainer_baseline) == pytest.approx(484.16015625)
    # Two lower-bound and four optimality-credit lines precede the closing anchors.
    # The default canvas reserves the deepest possible date descender.
    assert float(canvas.citations_baseline) == pytest.approx(2443.3058728125)
    assert float(canvas.credit_baseline) == pytest.approx(2182.3527478125)
    assert float(canvas.stamp_baseline) == pytest.approx(2254.3527478125)
    assert (composite.svg_name, composite.pdf_name) == (
        "known-best-1-324.svg",
        "square-packings-324-20261008.pdf",
    )
    assert composite.raster_name(1) == "known-best-1-324.png"
    # One raster and no crop: the export set is part of the specification.
    assert composite.card_units is None
    assert [export.manifest_key for export in canvas.rasters] == ["png_preview"]
    assert composite.stem in known_best_builder.SUMMARY_PROSE


def test_layout_record_refresh_preserves_facts_and_refuses_unrelated_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    canvas = known_best_builder.CompositeCanvas(CompositeSpec(1, 1, 1, "synthetic"))
    entries = [{"n": 1, "reported_side": "1"}]
    current_manifest = known_best_builder._manifest_document(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        entries,
        [known_best_builder._composite_record(canvas)],  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    )
    current_figure = {
        "figure": {
            "entries": [{"n": 1, "side": {"display": "s(1) = 1"}}],
            "composites": [
                {
                    "stem": "synthetic",
                    "columns": 1,
                    "rows": 1,
                    "layout": canvas.spec.layout,
                    "totals": {"proved_optimal": 1},
                }
            ],
        }
    }
    old_manifest = copy.deepcopy(current_manifest)
    old_manifest["atlas"]["composites"][0]["columns"] = 2
    old_manifest["atlas"]["composites"][0]["svg"]["width"] = 576
    old_figure = copy.deepcopy(current_figure)
    old_figure["figure"]["composites"][0]["columns"] = 2
    manifest_path, figure_path = tmp_path / "manifest.json", tmp_path / "composite-figure.json"
    manifest_text = json.dumps(old_manifest)
    manifest_path.write_text(manifest_text)
    monkeypatch.setattr(known_best_builder, "MANIFEST", manifest_path)
    monkeypatch.setattr(known_best_builder, "COMPOSITES", (canvas,))
    monkeypatch.setattr(build_composite_figure_data, "RECORD", figure_path)
    monkeypatch.setattr(build_composite_figure_data, "build_record", lambda: current_figure)
    monkeypatch.setattr(
        known_best_builder, "_retained_problems", lambda **_kwargs: ([], entries)
    )
    monkeypatch.setattr(known_best_builder, "retained_cases", lambda _numbers: [entries[0]])
    monkeypatch.setattr(known_best_builder, "_manifest_entry", lambda case: case)
    for envelope, location, key, wrong in (
        ("figure", "entries", "side", {"display": "s(1) = 2"}),
        ("figure", "composites", "totals", {"proved_optimal": 0}),
        ("atlas", "entries", "reported_side", "2"),
    ):
        unrelated_manifest, unrelated_figure = (
            copy.deepcopy(old_manifest),
            copy.deepcopy(old_figure),
        )
        unrelated = unrelated_figure if envelope == "figure" else unrelated_manifest
        unrelated[envelope][location][0][key] = wrong
        manifest_text, figure_text = (
            json.dumps(unrelated_manifest),
            json.dumps(unrelated_figure),
        )
        manifest_path.write_text(manifest_text)
        figure_path.write_text(figure_text)
        with pytest.raises(ValueError, match="unrelated"):
            known_best_builder.update_composite_records()
        assert manifest_path.read_text() == manifest_text
        assert figure_path.read_text() == figure_text
    manifest_path.write_text(json.dumps(old_manifest))
    figure_path.write_text(json.dumps(old_figure))
    assert known_best_builder.main(["--update-composite-records"]) == 0
    assert json.loads(manifest_path.read_text()) == current_manifest
    assert json.loads(figure_path.read_text()) == current_figure


def test_poster_preserves_logical_square_bound_row_coordinates() -> None:
    poster = known_best_builder.resolved_composites()[1].spec
    positions = []
    for k in range(1, 19):
        numbers = range((k - 1) ** 2 + 1, k**2 + 1)
        expected = [(k - 1, column) for column in range(len(numbers))]
        observed = [poster.card_position(n) for n in numbers]
        assert observed == expected, k
        positions.extend(observed)
    assert len(set(positions)) == 324
    figure = known_best_builder.PRIMARY_COMPOSITE.spec
    assert [figure.card_position(n) for n in (1, 10, 11, 100)] == [
        (0, 0),
        (0, 9),
        (1, 0),
        (9, 9),
    ]


def test_retained_poster_preserves_triangle_card_sizes_and_positions() -> None:
    root = ET.fromstring(_committed_poster_svg())
    cards = [card for card in root if card.attrib.get("data-feature") == "packing-card"]
    transitions = known_best_builder.resolved_composites()[1].transitions
    by_row = {transition.row: transition for transition in transitions}
    assert [int(card.attrib["data-n"]) for card in cards] == list(range(1, 325))
    for card in cards:
        n = int(card.attrib["data-n"])
        k = next(k for k in range(1, 19) if n <= k**2)
        row, column = k - 1, n - (k - 1) ** 2 - 1
        assert (int(card.attrib["data-row"]), int(card.attrib["data-column"])) == (
            row,
            column,
        ), n
        outline = card.find('svg:rect[@data-feature="container-outline"]', SVG)
        assert outline is not None
        position = known_best_builder.resolved_composites()[1].card_position(n, by_row[k])
        assert int(card.attrib["data-physical-row"]) == position.physical_row
        assert card.attrib["data-segment"] == position.segment
        assert (Decimal(outline.attrib["x"]), Decimal(outline.attrib["y"])) == (
            position.left + 24,
            position.top + 12,
        ), n
        assert (outline.attrib["width"], outline.attrib["height"]) == ("158", "158"), n
        for feature, baseline, font_size in (
            ("packing-label", 203, "29"),
            ("side-bound", 220, "14"),
        ):
            label = card.find(f'svg:text[@data-feature="{feature}"]', SVG)
            assert label is not None
            assert Decimal(label.attrib["y"]) == position.top + baseline, n
            assert label.attrib["font-size"] == font_size, n


def test_poster_complete_rows_share_a_right_edge_and_leave_room_for_left_information() -> None:
    canvas = known_best_builder.resolved_composites()[1]
    resolve = known_best_builder._poster_grid_transitions  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    transitions = {transition.row: transition for transition in resolve(canvas)}
    positions = [
        canvas.card_position(n, transitions[canvas.spec.card_position(n)[0] + 1])
        for n in canvas.spec.numbers
    ]
    assert {position.physical_row for position in positions} == set(range(18))
    for position in positions:
        assert position.physical_row == position.row
        assert position.top == 120 + 307 * position.row
    assert (
        min(position.left for position in positions),
        min(position.top for position in positions),
        max(position.left + 216 for position in positions),
        max(position.top + 242 for position in positions),
    ) == (180, 120, 7751, 5581)
    for n, position in zip(canvas.spec.numbers, positions, strict=True):
        transition = transitions[position.row + 1]
        gap = 79 if n in transition.grid.numbers and not transition.non_grid.empty else 0
        # Independent complete-row calculation: right-align the whole row before
        # inserting the retained prefix/grid separator, rather than either segment alone.
        row_left = 7871 - 120 - 216 - 214 * (2 * transition.row - 2)
        if transition.has_irregular_prefix:
            row_left -= 79
        assert position.left == row_left + 214 * position.column + gap
        assert position.left + 216 <= canvas.width - 120
        assert position.top + 242 <= canvas.height - 120
    for row, top, prefix_left, first_grid_left in (
        (17, 5032, 608, 4325),
        (18, 5339, 180, 4111),
    ):
        transition = transitions[row]
        non_grid, grid = canvas.segment_lines(transition)
        assert (non_grid.kind, grid.kind) == ("non-grid", "grid")
        assert non_grid.numbers == transition.non_grid
        assert grid.numbers == transition.grid
        assert (non_grid.top, grid.top, non_grid.left, grid.left) == (
            top,
            top,
            prefix_left,
            first_grid_left,
        )
        assert grid.physical_row == non_grid.physical_row == row - 1
    assert {
        canvas.card_position(transition.last_n, transition).left + 24 + 158
        for transition in transitions.values()
    } == {7717}
    assert canvas.information_left == canvas.card_left(290, transitions[18]) + 24 == 204
    assert canvas.information_right == 2804
    assert canvas.width - 7751 == 120
    assert canvas.height - 5581 == 120
    assert canvas.grid_top == 120
    assert known_best_builder.POSTER_INFORMATION_TOP == 120
    primary = known_best_builder.PRIMARY_COMPOSITE
    assert (primary.width, primary.height, primary.row_pitch) == (2260, 4023, 307)
    assert primary.card_left(1) == 60
    assert primary.grid_top == 174
    assert Decimal("1.38") <= Decimal(canvas.width) / canvas.height <= Decimal("1.39")


def test_poster_grid_transition_gap_uses_the_retained_group_and_preserves_card_scale() -> None:
    canvas = known_best_builder.resolved_composites()[1]
    resolve = known_best_builder._poster_grid_transitions  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    transitions = resolve(canvas)
    by_row = {transition.row: transition for transition in transitions}
    assert canvas.card_left(211, by_row[15]) == 4460
    assert canvas.card_left(212, by_row[15]) == 4753
    assert canvas.card_left(213, by_row[15]) - canvas.card_left(212, by_row[15]) == 214
    assert [canvas.card_left(n, by_row[2]) for n in (2, 3, 4)] == [7107, 7321, 7535]
    assert (
        known_best_builder.POSTER_GRID_GAP == known_best_builder.SUMMARY_PACKING_SIZE / 2 == 79
    )
    root = ET.Element("svg")
    append_card = known_best_builder._append_summary_card  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    for case in known_best_builder.retained_cases((5, 6, 7)):
        append_card(
            root,
            case,
            spec=RenderSpec(overlays=frozenset()),
            canvas=canvas,
            grid_transition=by_row[3],
        )
    cards = root.findall("svg:g[@data-feature='packing-card']", SVG)
    outlines = [card.find("svg:rect[@data-feature='container-outline']", SVG) for card in cards]
    assert all(outline is not None for outline in outlines)
    assert [Decimal(outline.attrib["x"]) for outline in outlines if outline is not None] == [
        6624,
        6917,
        7131,
    ]
    for outline in outlines:
        assert outline is not None
        assert (outline.attrib["width"], outline.attrib["height"], outline.attrib["y"]) == (
            "158",
            "158",
            "746",
        )
    labels = [card.find("svg:text[@data-feature='packing-label']", SVG) for card in cards]
    assert len(labels) == 3
    for label in labels:
        assert label is not None
        assert label.attrib["font-size"] == "29"


def test_poster_grid_markers_fit_the_separator_or_the_all_grid_margin() -> None:
    canvas = known_best_builder.resolved_composites()[1]
    resolve = known_best_builder._poster_grid_transitions  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    append = known_best_builder._append_grid_transition_marker  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    root = ET.Element("svg")
    transitions = resolve(canvas)
    for transition in transitions:
        append(root, transition, canvas=canvas)
    markers = root.findall("svg:g[@data-feature='grid-transition']", SVG)
    assert len(markers) == 18
    assert [int(marker.attrib["data-first-grid-n"]) for marker in markers] == [
        transition.first_grid_n for transition in transitions
    ]
    atlas_print_font.register_print_fonts()
    atlas_print_font.verify_cairo_face()
    context = cairo.Context(cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None))
    options = cairo.FontOptions()
    options.set_hint_metrics(cairo.HINT_METRICS_OFF)
    context.set_font_options(options)
    context.select_font_face(
        atlas_print_font.FAMILY, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD
    )
    context.set_font_size(15)
    for marker, transition in zip(markers, transitions, strict=True):
        assert "data-n" not in marker.attrib
        has_inline_gap = transition.has_irregular_prefix
        assert Decimal(marker.attrib["data-extra-gap"]) == (79 if has_inline_gap else 0)
        position = canvas.card_position(transition.first_grid_n, transition)
        drawing_left, drawing_top = position.left + 24, position.top + 12
        assert int(marker.attrib["data-physical-row"]) == position.physical_row
        assert marker.attrib["data-gap-axis"] == ("horizontal" if has_inline_gap else "none")
        labels = marker.findall("svg:text", SVG)
        assert [label.text for label in labels] == [
            f"{transition.row}\u00d7{transition.row} GRID"
        ]
        assert [Decimal(label.attrib["y"]) for label in labels] == [0]
        assert marker.attrib["data-grid-side"] == str(transition.row)
        assert marker.attrib["aria-label"].endswith(f"n={transition.first_grid_n}")
        assert marker.attrib["aria-label"].startswith(
            f"{transition.row}\u00d7{transition.row} grid "
        )
        assert marker.attrib["data-rotation"] == "-90"
        match = re.fullmatch(
            r"translate\(([-\d.]+) ([-\d.]+)\) rotate\(-90\)", marker.attrib["transform"]
        )
        assert match is not None
        center_x, center_y = map(float, match.groups())
        actual = []
        for node in labels:
            assert node.attrib["font-size"] == "15"
            assert node.attrib["font-family"] == atlas_print_font.FAMILY
            assert node.attrib["text-anchor"] == "start"
            x, y = float(node.attrib["x"]), float(node.attrib["y"])
            left, top, width, height, _advance, _dy = context.text_extents(node.text or "")
            actual.append(
                (
                    center_x + y + top,
                    center_y - x - left - width,
                    center_x + y + top + height,
                    center_y - x - left,
                )
            )
        bounds = (
            min(box[0] for box in actual),
            min(box[1] for box in actual),
            max(box[2] for box in actual),
            max(box[3] for box in actual),
        )
        recorded = tuple(
            float(marker.attrib[f"data-{edge}"]) for edge in ("left", "top", "right", "bottom")
        )
        assert bounds == pytest.approx(recorded, abs=1.0)
        assert max(120, position.left - (79 if has_inline_gap else 60)) <= bounds[0]
        assert bounds[2] < drawing_left
        assert Decimal(marker.attrib["data-drawing-clearance"]) == Decimal("49.365")
        assert float(drawing_left) - 0.575 - bounds[2] == pytest.approx(49.365, abs=1.0)
        assert drawing_top <= bounds[1] < bounds[3] <= drawing_top + 158
        assert (bounds[1] + bounds[3]) / 2 == pytest.approx(float(drawing_top + 79), abs=1.0)
    assert resolve(known_best_builder.PRIMARY_COMPOSITE) == ()


def test_print_arrangements_share_measured_outline_and_annotation_clearances() -> None:
    append = known_best_builder._append_summary_card  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    gaps = []
    for canvas in known_best_builder.resolved_composites():
        next_n = 17 if canvas.information_in_corner else 22
        root = ET.Element("svg")
        for case in known_best_builder.retained_cases((12, 13, next_n)):
            append(root, case, spec=RenderSpec(overlays=frozenset()), canvas=canvas)
        cards = [
            root.find(f"svg:g[@data-feature='packing-card'][@data-n='{n}']", SVG)
            for n in (12, 13, next_n)
        ]
        assert all(card is not None for card in cards)
        outlines = [
            card.find("svg:rect[@data-feature='container-outline']", SVG)
            for card in cards
            if card is not None
        ]
        assert all(outline is not None for outline in outlines)
        first, adjacent, below = [outline for outline in outlines if outline is not None]
        stroke = Decimal(first.attrib["stroke-width"])
        horizontal = (
            Decimal(adjacent.attrib["x"])
            - Decimal(first.attrib["x"])
            - Decimal(first.attrib["width"])
            - stroke
        )
        card = cards[0]
        assert card is not None
        bottom = max(_print_text_ink_bounds(node)[1] for node in card.findall("svg:text", SVG))
        next_outline = Decimal(below.attrib["y"]) - stroke / 2
        gaps.append((float(horizontal), float(next_outline) - bottom))
        assert float(horizontal) / 68.85 == pytest.approx(0.8, abs=0.005)
        assert (float(next_outline) - bottom) / 131.5197265625 == pytest.approx(0.6, abs=0.005)
    assert gaps[0] == pytest.approx(gaps[1])


def test_triangle_bound_captions_round_safely_and_clear_every_degree() -> None:
    format_caption = known_best_builder._composite_bound_display  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    text_width = known_best_builder._text_width  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    entries = _figure_entries()
    before = copy.deepcopy(entries)
    canvas = known_best_builder.resolved_composites()[1]
    assert format_caption("s(11) = 3.877084", canvas, degree=2) == "s(11) = 3.87708"
    assert format_caption("s(211) ≤ 14.997961", canvas) == "s(211) ≤ 14.99797"
    assert format_caption("s(211) ≥ 14.544571", canvas) == "s(211) ≥ 14.54457"
    assert format_caption("s(146) ≤ 12.600908", canvas, degree=16) == "s(146) ≤ 12.6010"
    for entry in entries.values():
        degree = entry["exactness"]["degree"]
        for field in ("side", "lower"):
            if field == "lower" and not entry[field]["shown"]:
                continue
            original = entry[field]["display"]
            caption = format_caption(
                original, canvas, degree=degree if field == "side" else None
            )
            assert (
                format_caption(original, known_best_builder.PRIMARY_COMPOSITE, degree=degree)
                == original
            )
            value = Decimal(caption.rsplit(" ", 1)[1])
            stored = Decimal(original.rsplit(" ", 1)[1])
            decimals = len(caption.partition(".")[2]) if "." in caption else 0
            assert decimals <= 5
            if " ≤ " in caption:
                assert value >= stored
            elif " ≥ " in caption:
                assert value <= stored
            else:
                assert abs(value - stored) <= Decimal(1).scaleb(-decimals) / 2
            if field == "side" and degree is not None and degree >= 2:
                extent = (
                    text_width(caption, "14")
                    + Decimal(14) * known_best_builder.SUMMARY_ITALIC_KERN
                    + text_width(f"deg {degree}", "14")
                )
                assert extent + 5 <= 158, entry["n"]
    assert entries == before


def test_triangle_fast_label_check_requires_the_compact_caption() -> None:
    canvas = known_best_builder.resolved_composites()[1]
    format_caption = known_best_builder._composite_bound_display  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    check = known_best_builder._composite_label_problems  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    root = ET.Element(f"{{{SVG['svg']}}}svg")
    for n, entry in _figure_entries().items():
        card = ET.SubElement(
            root, f"{{{SVG['svg']}}}g", {"data-feature": "packing-card", "data-n": str(n)}
        )
        labels = {
            "packing-label": str(n),
            "side-bound": format_caption(
                entry["side"]["display"], canvas, degree=entry["exactness"]["degree"]
            ),
        }
        if entry["lower"]["shown"]:
            labels["lower-bound"] = format_caption(entry["lower"]["display"], canvas)
        for feature, label in labels.items():
            ET.SubElement(card, f"{{{SVG['svg']}}}text", {"data-feature": feature}).text = label
    assert check(canvas, root) == []
    upper = root.find("svg:g[@data-n='211']/svg:text[@data-feature='side-bound']", SVG)
    assert upper is not None
    upper.text = "s(211) ≤ 14.997961"
    assert check(canvas, root) == [
        (
            "atlas/known-best/known-best-1-324.svg n=211 side-bound is "
            "('s(211) ≤ 14.997961',); expected ('s(211) ≤ 14.99797',)"
        )
    ]


def test_triangle_crop_resolves_complete_records_and_row_major_skips_grid_preflight(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    resolve = known_best_builder._poster_grid_transitions  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    crop = known_best_builder.CompositeCanvas(
        CompositeSpec(
            1,
            5,
            5,
            "triangle-crop",
            placement=known_best_builder.CompositePlacement.square_bound_triangle,
        )
    )
    assert [transition.first_grid_n for transition in resolve(crop)] == [1, 2, 6]
    selected = crop.with_transitions(known_best_builder.resolved_composites()[1].transitions)
    assert [transition.row for transition in selected.transitions] == [1, 2, 3]
    assert selected.physical_rows == 3
    assert [
        (line.kind, list(line.numbers.numbers))
        for line in selected.segment_lines(resolve(crop)[-1])
    ] == [("non-grid", [5])]
    prefix_crop = known_best_builder.CompositeCanvas(
        CompositeSpec(
            1,
            211,
            29,
            "prefix-crop",
            placement=known_best_builder.CompositePlacement.square_bound_triangle,
        )
    )
    prefix_crop = prefix_crop.with_transitions(resolve(prefix_crop))
    assert prefix_crop.physical_rows == 15
    assert prefix_crop.height == 4780
    assert [
        (line.kind, line.numbers.count)
        for line in prefix_crop.segment_lines(prefix_crop.transitions[-1])
    ] == [("non-grid", 15)]
    split_crop = known_best_builder.CompositeCanvas(
        CompositeSpec(
            1,
            212,
            29,
            "split-crop",
            placement=known_best_builder.CompositePlacement.square_bound_triangle,
        )
    )
    split_crop = split_crop.with_transitions(resolve(split_crop))
    assert split_crop.physical_rows == 15
    assert split_crop.height == 4780
    non_grid, grid = split_crop.segment_lines(split_crop.transitions[-1])
    assert grid.numbers.count == 1
    assert grid.top == non_grid.top
    for last_n, physical_rows, expected_height in ((273, 17, 5394), (274, 17, 5394)):
        wrapped_crop = known_best_builder.CompositeCanvas(
            CompositeSpec(
                1,
                last_n,
                33,
                "wrapped-crop",
                placement=known_best_builder.CompositePlacement.square_bound_triangle,
            )
        )
        wrapped_crop = wrapped_crop.with_transitions(resolve(wrapped_crop))
        assert wrapped_crop.physical_rows == physical_rows
        assert wrapped_crop.height == expected_height
        selected_lines = wrapped_crop.segment_lines(wrapped_crop.transitions[-1])
        if last_n == 273:
            assert [(line.kind, line.numbers.count) for line in selected_lines] == [
                ("non-grid", 17)
            ]
        else:
            non_grid, grid = selected_lines
            assert grid.numbers.count == 1
            assert grid.top == non_grid.top
    monkeypatch.setattr(known_best_builder, "MANIFEST", tmp_path / "absent.json")
    assert resolve(known_best_builder.PRIMARY_COMPOSITE) == ()
    assert (
        known_best_builder.PRIMARY_COMPOSITE.width,
        known_best_builder.PRIMARY_COMPOSITE.height,
    ) == (2260, 4023)


def test_poster_enlarges_information_type_without_changing_card_geometry() -> None:
    canvas = known_best_builder.resolved_composites()[1]
    root = ET.Element("svg")
    spec = RenderSpec(overlays=frozenset())
    append_information = known_best_builder._append_composite_information  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    append_card = known_best_builder._append_summary_card  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    append_information(
        root,
        spec=spec,
        canvas=canvas,
        identity=known_best_builder.retained_identity(_committed_poster_svg()),
    )
    baseline_sizes = {
        "poster-title": 48,
        "legend-label": 19,
        "explainer": 19,
        "problem-explainer": 19,
        "credit": 19,
        "release-stamp": 19,
        "packing-credit-line": 19,
        "lower-bound-credit-line": 19,
        "optimality-credit-line": 19,
    }
    block = root.find("svg:g[@data-feature='poster-information']", SVG)
    assert block is not None
    assert block.find("svg:text[@data-feature='release']", SVG) is None
    assert block.find("svg:g[@data-feature='release-star']", SVG) is None
    assert "Including new results" not in "".join(block.itertext())
    assert block.find("svg:text[@data-feature='poster-details']", SVG) is None
    assert block.find("svg:text[@data-feature='grid-explainer']", SVG) is None
    assert "GRID marks the first regular grid packing" not in "".join(block.itertext())
    assert "52,650 unit squares" not in "".join(block.itertext())
    information_text = list(block.iter(f"{{{SVG['svg']}}}text"))
    assert baseline_sizes.keys() <= {
        node.attrib.get("data-feature") for node in information_text
    }
    body_features = {
        "legend-label",
        "packing-credit-line",
        "lower-bound-credit-line",
        "optimality-credit-line",
        "credit",
        "release-stamp",
        "citations",
        "repository",
    }
    body_lines = [
        node for node in information_text if node.attrib.get("data-feature") in body_features
    ]
    assert len(body_lines) == 15 + sum(
        len(lines)
        for lines in known_best_builder._print_attribution_lines()  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    )
    assert {
        (node.attrib["font-family"], node.attrib["font-size"], node.attrib["font-weight"])
        for node in body_lines
    } == {(known_best_builder.POSTER_BODY_FONT, "48", "700")}
    assert all(
        node.attrib["fill"]
        == (
            "#000000"
            if node.attrib["data-feature"] in {"citations", "repository"}
            else known_best_builder.SUMMARY_SMALL_FILL
        )
        for node in body_lines
    )
    marks = [
        node
        for node in information_text
        if node not in body_lines
        and node.attrib.get("data-feature")
        not in {"poster-title", "explainer", "problem-explainer"}
    ]
    assert marks
    assert all(
        node.attrib["font-family"] == known_best_builder.POSTER_BODY_FONT for node in marks
    )
    assert all(node.attrib["font-weight"] == "700" for node in marks)
    for node in information_text:
        feature = node.attrib.get("data-feature", "")
        size = Decimal(node.attrib["font-size"])
        if feature in {"citations", "repository"}:
            assert size == 48
            assert node.attrib["font-weight"] == "700"
            assert node.attrib["font-family"] == known_best_builder.POSTER_BODY_FONT
        elif feature == "poster-title":
            assert size == baseline_sizes[feature] * 3
        elif feature in {"explainer", "problem-explainer"}:
            assert size == Decimal(known_best_builder.POSTER_PROBLEM_SIZE) == 66
        elif feature in baseline_sizes:
            assert size == 48
            assert size >= baseline_sizes[feature] * 2
        else:
            assert Decimal(29) < size < Decimal(38)
    problem = [
        block.find(f"svg:text[@data-feature='{feature}']", SVG)
        for feature in ("explainer", "problem-explainer")
    ]
    assert all(node is not None for node in problem)
    problem_baselines = [Decimal(node.attrib["y"]) for node in problem if node is not None]
    assert (problem_baselines[1] - problem_baselines[0]) / 66 == Decimal("1.50")
    columns = block.findall("svg:g/svg:g[@data-feature='legend-column']", SVG)
    for column in columns:
        nodes = column.findall("svg:text[@data-feature='legend-label']", SVG)
        assert len(nodes) == 4
        assert all(
            (Decimal(b.attrib["y"]) - Decimal(a.attrib["y"])) / 48 == Decimal("1.50")
            for a, b in pairwise(nodes)
        )
    credit_nodes = block.findall("svg:g/svg:text[@data-feature='packing-credit-line']", SVG)
    assert len(credit_nodes) == 3
    assert all(
        (Decimal(b.attrib["y"]) - Decimal(a.attrib["y"])) / 48 == Decimal("1.50")
        for a, b in pairwise(credit_nodes)
    )
    closing = list(block)[-4:]
    assert (Decimal(closing[1].attrib["y"]) - Decimal(closing[0].attrib["y"])) / 48 == Decimal(
        "1.50"
    )
    assert (Decimal(closing[3].attrib["y"]) - Decimal(closing[2].attrib["y"])) / 48 == Decimal(
        "1.50"
    )
    assert _print_text_ink_bounds(closing[2])[0] - _print_text_ink_bounds(closing[1])[
        1
    ] == pytest.approx(144, abs=1)
    assert (canvas.width, canvas.height) == (7871, 5701)
    assert (canvas.grid_top, canvas.grid_bottom) == (120, 5646)
    for case in known_best_builder.retained_cases((11, 12)):
        append_card(root, case, spec=spec, canvas=canvas)
        card = root.find(
            f"svg:g[@data-feature='packing-card'][@data-n='{case.frontier.n}']", SVG
        )
        assert card is not None
        outline = card.find("svg:rect[@data-feature='container-outline']", SVG)
        assert outline is not None
        assert (outline.attrib["x"], outline.attrib["y"]) == (
            str(6410 if case.frontier.n == 11 else 6703),
            "1053",
        )
        assert (outline.attrib["width"], outline.attrib["height"]) == ("158", "158")
        for node in card.iter(f"{{{SVG['svg']}}}text"):
            feature = node.attrib.get("data-feature", "")
            expected_size = "29" if feature == "packing-label" else "14" if feature else "15"
            assert node.attrib["font-size"] == expected_size
        for badge in card.findall("svg:rect[@data-feature='evidence-badge']", SVG):
            assert (badge.attrib["width"], badge.attrib["height"]) == ("19", "19")


def test_poster_math_variables_are_italic_above_its_legend_and_degree_ends_the_legend() -> None:
    root = ET.Element(f"{{{SVG['svg']}}}svg", {"width": "7871", "height": "5701"})
    append = known_best_builder._append_composite_information  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    append(
        root,
        spec=RenderSpec(overlays=frozenset()),
        canvas=known_best_builder.resolved_composites()[1],
        identity=known_best_builder.retained_identity(_committed_poster_svg()),
    )
    block = root.find("svg:g[@data-feature='poster-information']", SVG)
    assert block is not None
    first = block.find("svg:text[@data-feature='explainer']", SVG)
    assert first is not None
    assert block.find("svg:text[@data-feature='degree-explainer']", SVG) is None
    column = block.find("svg:g/svg:g[@data-column='right']", SVG)
    assert column is not None
    second = column.findall("svg:text[@data-feature='legend-label']", SVG)[-1]
    continuation = block.find("svg:text[@data-feature='problem-explainer']", SVG)
    assert continuation is not None
    assert " ".join("".join(line.itertext()) for line in (first, continuation)) == (
        "The square packing problem asks for the side s(n) of the smallest square that can "
        "hold n unit squares, where the squares are free to rotate but cannot overlap"
    )
    assert "".join(second.itertext()) == "deg is the algebraic degree of that side length"
    spans = [*first, *continuation]
    assert [(span.text, span.attrib.get("font-style", "normal")) for span in spans] == [
        ("The square packing problem asks for the side ", "normal"),
        ("s", "italic"),
        ("(", "normal"),
        ("n", "italic"),
        (") of the smallest square that can", "normal"),
        ("hold ", "normal"),
        ("n", "italic"),
        (" unit squares, where the squares are free to rotate but cannot overlap", "normal"),
    ]
    assert all(
        span.attrib["font-family"] == known_best_builder.POSTER_ITALIC_FONT
        for span in spans
        if span.attrib.get("font-style") == "italic"
    )
    text_width = known_best_builder._text_width  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    for line in (first, continuation):
        extent = text_width("".join(line.itertext()), line.attrib["font-size"])
        extent += sum((Decimal(span.attrib.get("dx", "0")) for span in line), Decimal(0))
        assert Decimal(line.attrib["x"]) == 204
        assert Decimal(line.attrib["x"]) + extent <= 2804
    assert second.attrib["text-anchor"] == "start"
    assert second.attrib["font-size"] == "48"
    assert Decimal(second.attrib["x"]) == Decimal(column.attrib["data-left"])
    assert (
        Decimal(second.attrib["y"])
        == known_best_builder.resolved_composites()[1].legend_baseline + 3 * 72
    )
    features = (
        "explainer",
        "problem-explainer",
        "credit",
        "release-stamp",
        "citations",
        "repository",
    )
    lines = [block.find(f"svg:text[@data-feature='{feature}']", SVG) for feature in features]
    assert all(line is not None for line in lines)
    baselines = [Decimal(line.attrib["y"]) for line in lines if line is not None]
    canvas = known_best_builder.resolved_composites()[1]
    layout = known_best_builder._information_layout(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        canvas, known_best_builder.retained_identity(_committed_poster_svg())
    )
    assert baselines == [
        *layout.problem_baselines,
        layout.diagram_baseline,
        layout.stamp_baseline,
        layout.project_baseline,
        layout.repository_baseline,
    ]
    assert _print_text_ink_bounds(continuation)[1] < float(canvas.legend_baseline - 60)
    assert not any(node.attrib.get("data-evidence") == second.text for node in column)
    line_bounds = [
        (Decimal(line.attrib["y"]), Decimal(line.attrib["font-size"]))
        for line in lines
        if line is not None
    ]
    assert all(
        above + above_size * Decimal("0.3") <= below - below_size
        for (above, above_size), (below, below_size) in pairwise(line_bounds)
    )
    final_line = lines[-1]
    assert final_line is not None
    assert _print_text_ink_bounds(final_line)[1] <= float(layout.bottom) + 1
    _assert_poster_text_clears_cards(block, known_best_builder.resolved_composites()[1])
    atlas_print_font.register_print_fonts()
    pdf = cairosvg.svg2pdf(bytestring=ET.tostring(root))
    assert isinstance(pdf, bytes)
    fonts = re.findall(rb"/FontName\s*/([^\s/>]+)", pdf)
    assert any(b"italic" in font.lower() or b"oblique" in font.lower() for font in fonts)
    assert any(
        b"italic" not in font.lower() and b"oblique" not in font.lower() for font in fonts
    )
    assert {font.split(b"+", 1)[-1] for font in fonts} == {
        b"SquaresAtlasPrint-Bold",
        b"SquaresAtlasPrint-BoldItalic",
    }


def test_poster_packing_credits_name_every_retained_construction_author_and_source() -> None:
    register = build_bound_citations.load_register()
    manifest = json.loads((ATLAS / "manifest.json").read_text())
    expected_names: set[str] = set()
    expected_sources: set[str] = set()
    for entry in manifest["atlas"]["entries"]:
        if entry["source"]["kind"] == "exact-grid":
            continue
        reported = build_bound_citations.load_case(entry["n"])["reported_upper_bound"]
        expected_sources.add(reported["source_key"])
        expected_names.update(
            register.names[name]
            for name in [
                *(reported.get("found_by") or []),
                *(reported.get("improved_by") or []),
            ]
        )
    root = ET.Element("svg")
    append = known_best_builder._append_composite_information  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    append(
        root,
        spec=RenderSpec(overlays=frozenset()),
        canvas=known_best_builder.resolved_composites()[1],
        identity=known_best_builder.retained_identity(_committed_poster_svg()),
    )
    information = root.find("svg:g[@data-feature='poster-information']", SVG)
    assert information is not None
    credit_block = information.find("svg:g[@data-feature='packing-credits']", SVG)
    assert credit_block is not None
    assert len(expected_names) == 22
    assert len(expected_sources) == 10
    assert set(json.loads(credit_block.attrib["data-credited-names"])) == expected_names
    assert set(json.loads(credit_block.attrib["data-source-keys"])) == expected_sources
    assert credit_block.find("svg:text[@data-feature='packing-credits-heading']", SVG) is None
    lines = credit_block.findall("svg:text[@data-feature='packing-credit-line']", SVG)
    assert len(lines) == 3
    body = " ".join(line.text or "" for line in lines)
    assert body.startswith("Best packings due to Göbel, Trump, Wainwright,")
    assert all(any(name in (line.text or "") for line in lines) for name in expected_names)
    printed_names = body.removeprefix("Best packings due to ").removesuffix(".").split(", ")
    assert len(printed_names) == len(expected_names)
    assert set(printed_names) == expected_names
    assert printed_names == [
        "Göbel",
        "Trump",
        "Wainwright",
        "Hämäläinen",
        "Stenlund",
        "Friedman",
        "Bidwell",
        "Cantrell",
        "Morandi",
        "Ellsworth",
        "Hajba",
        "Schadt",
        "Chaoweeraprasit",
        "Couzo",
        "Daniel",
        "de Winter",
        "Rehwaldt",
        "Gupta",
        "ry-xu",
        "Chang",
        "DeVincentis",
        "hmbelvedere",
    ]
    assert all(body.count(name) == 1 for name in expected_names)
    assert "et al." not in body
    assert "…" not in body
    assert "evand" not in body
    assert "franciscouzo" not in body
    assert "[" not in body
    assert "]" not in body
    text_width = known_best_builder._text_width  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    widths = [text_width(line.text or "", "48") for line in lines]
    assert min(widths) >= max(widths) * Decimal("0.9")
    layout = known_best_builder._information_layout(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        known_best_builder.resolved_composites()[1],
        known_best_builder.retained_identity(_committed_poster_svg()),
    )
    assert not body.endswith(".")
    for node, baseline in zip(lines, layout.credit_baselines, strict=True):
        assert node.attrib["font-size"] == "48"
        assert node.attrib["text-anchor"] == "start"
        assert Decimal(node.attrib["x"]) == 204
        assert Decimal(node.attrib["y"]) == baseline
        assert Decimal(204) + text_width(node.text or "", "48") <= 2804
        assert baseline + Decimal("17.1") <= layout.bottom
    ending = list(information)[-4:]
    assert [line.attrib["data-feature"] for line in ending] == [
        "credit",
        "release-stamp",
        "citations",
        "repository",
    ]
    assert [line.text for line in ending] == [
        "Diagram by Joshua Levy",
        known_best_builder.retained_identity(_committed_poster_svg()).poster_stamp,
        "The Squares Project",
        "github.com/jlevy/squares",
    ]
    identity = known_best_builder.retained_identity(_committed_poster_svg())
    stamp_text = ending[1].text
    assert isinstance(stamp_text, str)
    assert stamp_text == f"{identity.formatted_date} · {identity.stamp}"
    assert text_width(stamp_text, "48") <= 2600
    assert [line.attrib["font-size"] for line in ending] == ["48"] * 4
    assert [line.attrib["fill"] for line in ending[2:]] == ["#000000"] * 2
    for attribute in ("font-family", "font-size", "font-weight", "fill"):
        assert ending[-2].attrib[attribute] == ending[-1].attrib[attribute]
    assert ending[-1].attrib["font-weight"] == "700"
    assert ending[-1].attrib["font-family"] == known_best_builder.POSTER_BODY_FONT
    assert information.find(".//svg:a", SVG) is None
    assert all(not key.endswith("href") for node in information.iter() for key in node.attrib)
    assert ending[-1].text == (ending[-1].text or "").strip()
    assert all(line.attrib["text-anchor"] == "start" for line in ending)
    assert all(Decimal(line.attrib["x"]) == 204 for line in ending)
    assert [Decimal(line.attrib["y"]) for line in ending] == [
        layout.diagram_baseline,
        layout.stamp_baseline,
        layout.project_baseline,
        layout.repository_baseline,
    ]
    assert (
        sum(
            node.text == "github.com/jlevy/squares"
            for node in information.iter(f"{{{SVG['svg']}}}text")
        )
        == 1
    )
    assert known_best_builder.SUMMARY_CITATIONS not in "".join(information.itertext())
    proof_lines = information.findall(
        "svg:g/svg:text[@data-feature='optimality-credit-line']", SVG
    )
    assert _print_text_ink_bounds(ending[0])[0] - _print_text_ink_bounds(proof_lines[-1])[
        1
    ] == pytest.approx(144, abs=1)
    assert _print_text_ink_bounds(ending[2])[0] - _print_text_ink_bounds(ending[1])[
        1
    ] == pytest.approx(144, abs=1)
    # Measure every actual text line against the right-aligned cards, rather than
    # treating empty information-block space as ink.
    canvas = known_best_builder.resolved_composites()[1]
    assert Decimal(ending[2].attrib["y"]) + Decimal("17.1") < canvas.card_position(82).top
    _assert_poster_text_clears_cards(information, canvas)


def test_poster_packing_credit_wrap_refuses_an_overwide_name() -> None:
    wrap = known_best_builder._poster_credit_lines  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    credit = known_best_builder.PackingCredit(("W" * 100,), ("[source]",), "[source 2026]")
    with pytest.raises(ValueError, match="three-line information block"):
        wrap((credit,))


def _pdf_fill_colors(svg: ET.Element) -> set[tuple[float, float, float]]:
    atlas_print_font.register_print_fonts()
    pdf = cairosvg.svg2pdf(bytestring=ET.tostring(svg))
    assert isinstance(pdf, bytes)
    streams: list[bytes] = []
    for start in re.finditer(rb"stream\r?\n", pdf):
        end = pdf.find(b"endstream", start.end())
        try:
            streams.append(zlib.decompress(pdf[start.end() : end]))
        except zlib.error:
            continue
    return {
        (float(red), float(green), float(blue))
        for stream in streams
        for red, green, blue in re.findall(rb"([-0-9.]+) ([-0-9.]+) ([-0-9.]+) rg", stream)
    }


def test_poster_accents_recent_contributions_independently_in_svg_and_pdf() -> None:
    flags = recent_contributions_by_case()
    assert flags[11] == RecentContributions(upper=False, lower=True, optimal=True)
    assert flags[211] == RecentContributions(upper=True, lower=True, optimal=False)
    canvas = known_best_builder.resolved_composites()[1]
    root = ET.Element(f"{{{SVG['svg']}}}svg", {"width": "7871", "height": "5701"})
    append = known_best_builder._append_summary_card  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    for case in known_best_builder.retained_cases((11, 211)):
        append(
            root,
            case,
            spec=RenderSpec(overlays=frozenset()),
            canvas=canvas,
            recent=flags[case.frontier.n],
        )
    cards = {int(card.attrib["data-n"]): card for card in root}
    optimal = cards[11].find("svg:rect[@data-evidence='proved optimal']", SVG)
    assert optimal is not None
    assert optimal.attrib["fill"] == FIRST_PARTY_ACCENT_COLOR
    upper = cards[11].find("svg:text[@data-feature='side-bound']", SVG)
    assert upper is not None
    assert "".join(upper.itertext()) == "s(11) = 3.87708"
    assert all(span.attrib.get("fill") != FIRST_PARTY_ACCENT_COLOR for span in upper)
    assert cards[11].find("svg:text[@data-feature='lower-bound']", SVG) is None
    for feature in ("side-bound", "lower-bound"):
        line = cards[211].find(f"svg:text[@data-feature='{feature}']", SVG)
        assert line is not None
        assert "".join(line.itertext()) == (
            "s(211) ≤ 14.99797" if feature == "side-bound" else "s(211) ≥ 14.54457"
        )
        colored = [span for span in line if span.attrib.get("fill") == FIRST_PARTY_ACCENT_COLOR]
        assert len(colored) == 1
        assert re.fullmatch(r"[0-9.]+", colored[0].text or "")
    # Isolate the actual emblem and upper caption before rasterization: the recent
    # star cannot satisfy the PDF accent assertion on behalf of an unaccented emblem.
    emblem_svg = ET.Element(f"{{{SVG['svg']}}}svg", root.attrib)
    emblem_svg.append(copy.deepcopy(optimal))
    caption_svg = ET.Element(f"{{{SVG['svg']}}}svg", root.attrib)
    caption_svg.append(copy.deepcopy(upper))
    accent = tuple(
        int(FIRST_PARTY_ACCENT_COLOR[index : index + 2], 16) / 255 for index in (1, 3, 5)
    )
    assert any(
        all(
            abs(actual - expected) < 1e-6
            for actual, expected in zip(color, accent, strict=True)
        )
        for color in _pdf_fill_colors(emblem_svg)
    )
    assert not any(
        all(
            abs(actual - expected) < 1e-6
            for actual, expected in zip(color, accent, strict=True)
        )
        for color in _pdf_fill_colors(caption_svg)
    )


@pytest.mark.parametrize("upper_only", [False, True], ids=["actual-n11", "upper-only"])
def test_primary_composite_routes_contributions_to_cards_and_legend(
    monkeypatch: pytest.MonkeyPatch, *, upper_only: bool
) -> None:
    canvas = known_best_builder.PRIMARY_COMPOSITE
    actual = recent_contributions_by_case()
    contributions = {
        n: RecentContributions(upper=False, lower=False, optimal=False)
        if upper_only
        else actual[n]
        for n in canvas.spec.numbers
    }
    if upper_only:
        contributions[11] = RecentContributions(upper=True, lower=False, optimal=False)
    else:
        assert contributions[11] == RecentContributions(upper=False, lower=True, optimal=True)
    lookups: list[bool] = []

    def contribution_lookup() -> dict[int, RecentContributions]:
        lookups.append(True)
        return contributions

    monkeypatch.setattr(known_best_builder, "recent_contributions_by_case", contribution_lookup)
    record = copy.deepcopy(known_best_builder.load_figure_record())
    for composite in record["composites"]:
        composite["totals"]["lower_bound_recent_result"] = 0
    monkeypatch.setattr(known_best_builder, "load_figure_record", lambda: record)
    root = ET.fromstring(
        known_best_builder.render_known_best_summary_svg(
            known_best_builder.retained_cases(canvas.spec.numbers),
            canvas,
            known_best_builder.CompositeIdentity("1" * 40, "2026-09-28"),
        )
    )
    assert lookups == [True]
    assert (root.attrib["width"], root.attrib["height"], root.attrib["viewBox"]) == (
        "2260",
        "4023",
        "0 0 2260 4023",
    )
    entries = {entry["n"]: entry for entry in record["entries"]}
    assert [
        n for n in canvas.spec.numbers if entries[n]["exactness"]["state"] == "numeric-only"
    ] == [29, 55, 71]
    degrees = {
        n: entries[n]["exactness"]["degree"]
        for n in canvas.spec.numbers
        if entries[n]["exactness"]["degree"] is not None
        and entries[n]["exactness"]["degree"] >= 2
    }
    displayed_degrees = {
        int(item.attrib["data-n"]): label.text
        for item in root.findall("svg:g[@data-feature='packing-card']", SVG)
        if (label := item.find("svg:text[@data-feature='algebraic-degree']", SVG)) is not None
    }
    assert sorted(degrees) == [
        5,
        10,
        11,
        17,
        18,
        19,
        26,
        27,
        28,
        37,
        38,
        39,
        40,
        41,
        51,
        52,
        53,
        54,
        65,
        66,
        67,
        69,
        82,
        83,
        85,
        87,
        89,
    ]
    assert displayed_degrees == {n: f"deg {degree}" for n, degree in degrees.items()}
    assert entries[68]["exactness"]["degree"] == 1
    assert 68 not in displayed_degrees
    card = root.find("svg:g[@data-n='11']", SVG)
    assert card is not None
    optimal = card.find("svg:rect[@data-evidence='proved optimal']", SVG)
    assert optimal is not None
    assert (optimal.attrib["fill"] == FIRST_PARTY_ACCENT_COLOR) is contributions[11].optimal
    upper = card.find("svg:text[@data-feature='side-bound']", SVG)
    assert upper is not None
    assert "".join(upper.itertext()) == "s(11) = 3.877084"
    marked = [span for span in upper if span.attrib.get("fill") == FIRST_PARTY_ACCENT_COLOR]
    assert len(marked) == int(contributions[11].upper)
    if marked:
        assert marked[0].text == "3.877084"
    for node, expected_accent in (
        (optimal, contributions[11].optimal),
        (upper, contributions[11].upper),
    ):
        isolated = ET.Element(f"{{{SVG['svg']}}}svg", root.attrib)
        isolated.append(copy.deepcopy(node))
        accent = tuple(
            int(FIRST_PARTY_ACCENT_COLOR[index : index + 2], 16) / 255 for index in (1, 3, 5)
        )
        assert (
            any(
                all(
                    abs(actual - expected) < 1e-6
                    for actual, expected in zip(color, accent, strict=True)
                )
                for color in _pdf_fill_colors(isolated)
            )
            is expected_accent
        )
    expected_recent = sum(flags.any for flags in contributions.values())
    starred = {
        int(item.attrib["data-n"])
        for item in root.findall("svg:g[@data-feature='packing-card']", SVG)
        if item.find("svg:polygon[@data-feature='legend-star']", SVG) is not None
    }
    assert starred == {n for n, flags in contributions.items() if flags.any}
    legend = root.find(".//svg:g[@data-feature='evidence-legend']", SVG)
    assert legend is not None
    assert f"recent result, since August, 2026 ({expected_recent} of 100)" in [
        node.text for node in legend.findall(".//svg:text[@data-feature='legend-label']", SVG)
    ]


def test_poster_single_dark_r_retains_verified_and_catalogue_metadata() -> None:
    canvas = known_best_builder.resolved_composites()[1]
    root = ET.Element("svg")
    append = known_best_builder._append_summary_card  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    entries = _figure_entries()
    for case in known_best_builder.retained_cases((11, 28, 52)):
        append(
            root,
            case,
            spec=RenderSpec(overlays=frozenset()),
            canvas=canvas,
            recent=RecentContributions(upper=True, lower=True, optimal=True),
        )
    cards = {int(card.attrib["data-n"]): card for card in root}
    for n, card in cards.items():
        assert json.loads(card.attrib["data-rigidity"]) == entries[n]["rigidity"]
        assert (
            card.attrib["data-known-rigid"]
            == str(entries[n]["rigidity"]["known_rigid"]).lower()
        )
        badges = card.findall("svg:rect[@data-evidence='known rigid']", SVG)
        assert len(badges) == (1 if n in {11, 28} else 0)
        for badge in badges:
            assert badge.attrib["fill"] == known_best_builder.PAPER_THEME.muted
            assert badge.attrib["fill"] != FIRST_PARTY_ACCENT_COLOR
    assert entries[11]["rigidity"]["state"] == "established"
    assert entries[28]["rigidity"]["state"] == "not-established"
    assert entries[28]["rigidity"]["basis"] == "catalogue-annotation"
    assert entries[52]["rigidity"]["known_rigid"] is False


def test_direct_card_helpers_do_not_resolve_canonical_contribution_flags(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unexpected_lookup() -> None:
        raise AssertionError("a direct card helper must not load the canonical corpus")

    monkeypatch.setattr(known_best_builder, "recent_contributions_by_case", unexpected_lookup)
    root = ET.Element("svg")
    append = known_best_builder._append_summary_card  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    append(
        root,
        known_best_builder.retained_cases((11,))[0],
        spec=RenderSpec(overlays=frozenset()),
        canvas=known_best_builder.PRIMARY_COMPOSITE,
    )
    assert len(root) == 1


def test_print_legend_spells_counts_without_changing_web_fractions() -> None:
    descriptor = atlas_legend(AtlasLegendCounts(77, 292, 32, 22, 297, 324))
    counted = [item for item in descriptor.items if item.count is not None]
    assert [item.formatted_text(count_style="words") for item in counted] == [
        "proved optimal (77 of 324)",
        "exact value known (292 of 324)",
        "only known numerically (32 of 324)",
        "rigid (22 of 324)",
        "recent result, since August, 2026 (297 of 324)",
    ]
    assert descriptor.left[0].text == "proved optimal (77/324)"
    assert descriptor.right[-1].formatted_text(count_style="words") == descriptor.right[-1].text


def test_shared_atlas_legend_has_the_same_eight_items_in_four_and_four_rows() -> None:
    descriptor = atlas_legend(AtlasLegendCounts(77, 292, 32, 22, 297, 324))
    assert [item.marker for item in descriptor.left] == ["O", "=", "≈", "R"]
    assert [item.marker for item in descriptor.right] == ["star", "angles", "shades", None]
    assert [item.text for item in descriptor.items] == [
        "proved optimal (77/324)",
        "exact value known (292/324)",
        "only known numerically (32/324)",
        "rigid (22/324)",
        "recent result, since August, 2026 (297/324)",
        "colors indicate distinct tilt angles",
        "shade indicates number of full-side contacts",
        "deg is the algebraic degree of that side length",
    ]
    assert [item.key for item in descriptor.right] == ["recent", "angles", "contacts", "degree"]
    assert descriptor.right[3].marker_values == ()
    assert descriptor.right[1].marker_values == (0, 1, 2, 3)
    assert descriptor.right[1].marker_labels == ("90°", "45°", "", "")
    assert descriptor.right[2].marker_values == (4, 3, 2, 1, 0)
    assert descriptor.right[2].marker_labels == ()


def test_poster_legend_columns_align_left_and_count_upper_only_recent_results(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    canvas = known_best_builder.resolved_composites()[1]
    monkeypatch.setattr(
        known_best_builder,
        "load_figure_record",
        lambda: {
            "composites": [
                {
                    "stem": canvas.spec.stem,
                    "totals": {
                        "proved_optimal": 77,
                        "exact_value_known": 292,
                        "only_known_numerically": 32,
                        "rigidity_known": 22,
                        "lower_bound_recent_result": 0,
                    },
                }
            ]
        },
    )
    contributions = {
        n: RecentContributions(upper=False, lower=False, optimal=False)
        for n in canvas.spec.numbers
    }
    contributions[11] = RecentContributions(upper=True, lower=False, optimal=False)
    root = ET.Element("svg")
    append = known_best_builder._append_summary_legend  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    append(
        root, spec=RenderSpec(overlays=frozenset()), canvas=canvas, contributions=contributions
    )
    columns = root.findall("svg:g/svg:g[@data-feature='legend-column']", SVG)
    assert [column.attrib["data-column"] for column in columns] == ["left", "right"]
    labels = [
        column.findall("svg:text[@data-feature='legend-label']", SVG) for column in columns
    ]
    assert [len(column) for column in labels] == [4, 4]
    assert labels[1][0].text == "recent result, since August, 2026 (1 of 324)"
    description = known_best_builder.SUMMARY_PROSE[canvas.spec.stem][1]
    assert all(
        role in description
        for role in (
            "construction giving an upper bound",
            "proof of a lower bound",
            "optimality proof",
        )
    )
    assert "since August 2026" in description
    assert "common right edge" in description
    assert "eighteen physical lines" in description
    assert "thirty-five-column envelope" in description
    assert "left-aligned information block" in description
    assert "upper-left corner" in description
    assert "Wrapped" not in description
    assert known_best_builder.POSTER_PROBLEM in description
    primary_description = known_best_builder.SUMMARY_PROSE["known-best-1-100"][1]
    assert all(
        role in primary_description
        for role in (
            "construction giving an upper bound",
            "proof of a lower bound",
            "optimality proof",
        )
    )
    assert "since August 2026" in primary_description
    assert [Decimal(node.attrib["y"]) for node in labels[0]] == [
        canvas.legend_baseline + 72 * index for index in range(4)
    ]
    assert [Decimal(node.attrib["y"]) for node in labels[1]] == [
        canvas.legend_baseline + 72 * index for index in range(4)
    ]
    text_width = known_best_builder._text_width  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    for column, nodes in zip(columns, labels, strict=True):
        start = Decimal(column.attrib["data-left"])
        right = start + Decimal(column.attrib["data-width"])
        assert 204 <= start < right <= 2804
        for node in nodes:
            assert node.attrib["text-anchor"] == "start"
            assert node.attrib["font-size"] == "48"
            x = Decimal(node.attrib["x"])
            assert start <= x
            assert (x == start) == (node is nodes[-1] and column is columns[1])
            assert x + text_width(node.text or "", "48") <= right
    assert (
        Decimal(columns[1].attrib["data-left"])
        - Decimal(columns[0].attrib["data-left"])
        - Decimal(columns[0].attrib["data-width"])
        == 180
    )
    rigid = columns[0].find("svg:rect[@data-evidence='rigid']", SVG)
    assert rigid is not None
    assert rigid.attrib["fill"] == known_best_builder.PAPER_THEME.muted
    assert len(root.findall(".//svg:rect[@data-evidence='rigid']", SVG)) == 1


@pytest.mark.parametrize("index", [0, 1])
def test_both_pdf_legends_label_only_the_first_two_angle_swatches(index: int) -> None:
    canvas = known_best_builder.COMPOSITES[index]
    root = ET.Element("svg")
    append = known_best_builder._append_summary_legend  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    append(root, spec=RenderSpec(overlays=frozenset()), canvas=canvas)
    labels = root.findall(".//svg:text[@data-swatch-label]", SVG)
    assert [node.text for node in labels] == ["90°", "45°", "4", "3", "2", "1", "0"]
    text_width = known_best_builder._text_width  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    expected_size = (
        "11.5"
        if index == 0
        else known_best_builder.format_svg_number(
            Decimal("11.5") * known_best_builder.POSTER_LEGEND_TYPE_SCALE
        )
    )
    for parent in root.iter():
        children = list(parent)
        for position, label in enumerate(children):
            if label.attrib.get("data-swatch-label") is None:
                continue
            swatch = children[position - 1]
            assert swatch.attrib["data-feature"] == "legend-swatch"
            assert label.attrib["font-size"] == expected_size
            assert label.attrib["text-anchor"] == "middle"
            width = Decimal(swatch.attrib["width"])
            left = Decimal(swatch.attrib["x"])
            center = Decimal(label.attrib["x"])
            extent = text_width(label.text or "", expected_size)
            assert center == left + width / 2
            assert left < center - extent / 2 < center + extent / 2 < left + width
            if label.text in {"90°", "45°"}:
                assert label.attrib["fill"] == "#000000"
            else:
                assert label.attrib["fill"] in {
                    known_best_builder.PAPER_THEME.background,
                    known_best_builder.PAPER_THEME.ink,
                }
            assert label.attrib["fill"] != swatch.attrib["fill"]
    assert len(root.findall(".//svg:rect[@data-feature='legend-swatch']", SVG)) == 9
    degree_labels = [
        node
        for node in root.iter(f"{{{SVG['svg']}}}text")
        if node.text == "deg is the algebraic degree of that side length"
    ]
    assert len(degree_labels) == 1
    for column in root.findall("svg:g/svg:g[@data-feature='legend-column']", SVG):
        for node in column.findall("svg:text[@data-feature='legend-label']", SVG):
            left = Decimal(node.attrib["x"])
            right = left + text_width(node.text or "", node.attrib["font-size"])
            assert 0 < left < right < canvas.width
    pitch = 72 if index else Decimal("28.5")
    assert Decimal(degree_labels[0].attrib["y"]) == canvas.legend_baseline + 3 * pitch


def test_poster_documentation_refuses_overlapping_lines(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(known_best_builder, "POSTER_BODY_LINE_PITCH", Decimal(40))
    append = known_best_builder._append_composite_information  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    with pytest.raises(ValueError, match="documentation lines overlap"):
        append(
            ET.Element("svg"),
            spec=RenderSpec(overlays=frozenset()),
            canvas=known_best_builder.resolved_composites()[1],
            identity=known_best_builder.retained_identity(_committed_poster_svg()),
        )


def test_poster_closing_block_refuses_a_long_line_overlapping_cards(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    canvas = known_best_builder.resolved_composites()[1]
    layout = known_best_builder._information_layout(canvas)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    size = Decimal(known_best_builder.POSTER_BODY_SIZE)
    baseline = canvas.card_position(canvas.spec.last_n).top + size
    # The line stays inside its information block and intersects the final card row.
    monkeypatch.setattr(
        known_best_builder,
        "_information_layout",
        lambda _canvas, _identity=None: replace(
            layout, diagram_baseline=baseline, bottom=baseline + size
        ),
    )
    append = known_best_builder._append_composite_information  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    with pytest.raises(ValueError, match="credit line overlaps a packing card"):
        append(
            ET.Element("svg"),
            spec=RenderSpec(overlays=frozenset()),
            canvas=known_best_builder.resolved_composites()[1],
            identity=known_best_builder.retained_identity(_committed_poster_svg()),
        )


def test_poster_information_is_complete_left_aligned_and_clear_of_cards() -> None:
    root = ET.fromstring(_committed_poster_svg())
    block = root.find('svg:g[@data-feature="poster-information"]', SVG)
    assert block is not None
    left, right, top, bottom = (
        Decimal(block.attrib[f"data-{edge}"]) for edge in ("left", "right", "top", "bottom")
    )
    layout = known_best_builder._information_layout(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        known_best_builder.resolved_composites()[1],
        known_best_builder.retained_identity(_committed_poster_svg()),
    )
    assert (left, right, top) == (204, 2804, 120)
    assert bottom == Decimal(known_best_builder.format_svg_number(layout.bottom))
    cards = [card for card in root if card.attrib.get("data-feature") == "packing-card"]
    card_text = {node for card in cards for node in card.iter(f"{{{SVG['svg']}}}text")}
    information_text = set(block.iter(f"{{{SVG['svg']}}}text"))
    marker_text = {
        node
        for marker in root.findall("svg:g[@data-feature='grid-transition']", SVG)
        for node in marker.iter(f"{{{SVG['svg']}}}text")
    }
    assert set(root.iter(f"{{{SVG['svg']}}}text")) - card_text - marker_text == information_text
    features = {node.attrib.get("data-feature") for node in information_text}
    assert "poster-details" not in features
    assert "release" not in features
    assert "release-star" not in features
    assert "Including new results" not in "".join(block.itertext())
    assert "52,650 unit squares" not in "".join(block.itertext())
    assert {
        "poster-title",
        "repository",
        "legend-label",
        "explainer",
        "problem-explainer",
        "citations",
        "credit",
        "release-stamp",
        "packing-credit-line",
    } <= features
    labels = [
        node for node in information_text if node.attrib.get("data-feature") == "legend-label"
    ]
    assert len(labels) == 8
    assert {
        "proved optimal",
        "exact value known",
        "only known numerically",
        "rigid",
        known_best_builder.RECENT_LABEL,
        "colors indicate distinct tilt angles",
        "shade indicates number of full-side contacts",
        "deg is the algebraic degree of that side length",
    } == {((node.text or "").rsplit(" (", 1)[0]) for node in labels}
    text_width = known_best_builder._text_width  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    for node in information_text:
        x, y = Decimal(node.attrib["x"]), Decimal(node.attrib["y"])
        size = Decimal(node.attrib["font-size"])
        content = "".join(node.itertext())
        extent = text_width(content, str(size))
        extent += Decimal(node.attrib.get("letter-spacing", "0")) * max(len(content) - 1, 0)
        extent += sum((Decimal(child.attrib.get("dx", "0")) for child in node), Decimal(0))
        anchor = node.attrib.get("text-anchor", "start")
        text_left = (
            x - extent if anchor == "end" else x - extent / 2 if anchor == "middle" else x
        )
        text_right = text_left + extent
        assert left <= text_left <= text_right <= right
        assert top <= y - size
        assert _print_text_ink_bounds(node)[1] <= float(bottom) + 1
        if node.attrib.get("data-feature") in {
            "explainer",
            "problem-explainer",
        }:
            assert text_left == left
        elif node.attrib.get("data-feature") == "legend-label":
            assert anchor == "start"
        elif node.attrib.get("data-feature"):
            assert anchor == "start"
            assert text_left == left
            assert x == left
    _assert_poster_text_clears_cards(block, known_best_builder.resolved_composites()[1])


def test_poster_information_refuses_a_line_that_would_clip(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(known_best_builder, "POSTER_DIAGRAM_CREDIT", "W" * 300)
    append = known_best_builder._append_composite_information  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    with pytest.raises(ValueError, match="credit line exceeds"):
        append(
            ET.Element("svg"),
            spec=RenderSpec(overlays=frozenset()),
            canvas=known_best_builder.resolved_composites()[1],
            identity=known_best_builder.retained_identity(_committed_composite_svg()),
        )


def test_every_composite_footer_says_where_the_citations_are() -> None:
    for canvas in known_best_builder.COMPOSITES:
        root = ET.fromstring(canvas.svg_path.read_text(encoding="utf-8"))
        information = root.find("svg:g[@data-feature='poster-information']", SVG)
        assert information is not None
        stamp = information.find("svg:text[@data-feature='release-stamp']", SVG)
        assert stamp is not None
        assert (
            stamp.text
            == known_best_builder.retained_identity(canvas.svg_path.read_text()).poster_stamp
        )
        if canvas.information_in_corner:
            lines = [
                information.find(f"svg:text[@data-feature='{feature}']", SVG)
                for feature in ("citations", "repository")
            ]
            assert all(line is not None for line in lines)
            assert [line.text for line in lines if line is not None] == [
                "The Squares Project",
                "github.com/jlevy/squares",
            ]
        else:
            reference = root.find("svg:text[@data-feature='project-reference']", SVG)
            assert reference is not None
            assert reference.text == "The Squares Project · github.com/jlevy/squares"
            assert information.find("svg:text[@data-feature='citations']", SVG) is None
            assert information.find("svg:text[@data-feature='repository']", SVG) is None
        assert not root.findall(".//svg:a", SVG)
        description = root.find("svg:desc", SVG)
        assert description is not None
        assert description.text is not None
        assert description.text.endswith(" The Squares Project: github.com/jlevy/squares.")


def test_a_second_composite_is_a_specification_and_not_a_second_set_of_constants() -> None:
    """The same card metrics govern both arrangements and their canvas dimensions.

    The triangle widens by whole column pitches and its height follows its rows, with
    information in the corner. A row-major third figure still follows the original
    title-and-footer policy.
    """
    poster = known_best_builder.resolved_composites()[1]
    figure = known_best_builder.PRIMARY_COMPOSITE

    extra_columns = poster.physical_columns - figure.spec.columns
    widening = extra_columns * known_best_builder.SUMMARY_COLUMN_PITCH
    assert poster.width == figure.width + widening + 79 + 182
    assert poster.grid_bottom == poster.grid_top + poster.physical_rows * poster.row_pitch
    assert poster.height == (
        poster.grid_bottom
        - poster.row_pitch
        + known_best_builder.SUMMARY_CARD_HEIGHT
        + known_best_builder.POSTER_OUTER_MARGIN
    )

    # Unhydrated triangle helpers retain their ordinary layout without canonical I/O.
    plain_poster = known_best_builder.CompositeCanvas(poster.spec)
    assert (plain_poster.width, plain_poster.height, plain_poster.physical_rows) == (
        7871,
        5701,
        18,
    )

    # And a third would be a third specification: one declared here, never rendered,
    # measured while its cards do not exist.
    third = known_best_builder.CompositeCanvas(CompositeSpec(1, 400, 20, "known-best-1-400"))
    assert (third.spec.rows, third.spec.square_count) == (20, 80200)
    assert third.width == figure.width + 10 * known_best_builder.SUMMARY_COLUMN_PITCH
    assert third.height == figure.height + 10 * known_best_builder.SUMMARY_ROW_PITCH
    assert third.spec.stem not in known_best_builder.SUMMARY_PROSE


def _committed_poster_svg() -> str:
    """The retained poster, read the way its drift checks compare it."""
    return (ATLAS / "known-best-1-324.svg").read_text(encoding="utf-8")


def test_the_poster_stays_inside_its_byte_budget() -> None:
    """The file a clone pays for, measured against the budget the encoding was chosen for.

    The house encoding spends 490 bytes on one of these squares, measured. At 52,650 of
    them that is a 24.6 MB file, not something to commit, so the poster drops three costs
    the figure keeps: the per-square `data-*` facts, the stroke repeated on every
    polygon, and coordinates carried to 28 significant digits. Each is asserted here from
    the drawing rather than from the specification, because what a reader downloads is
    the drawing. `build_known_best_atlas --report` prints the same numbers on demand.

    The budget is a ceiling, not a golden size: the corpus's geometry decides the exact
    figure and a witness gaining a digit may move it. What must not happen is the file
    quietly returning to an encoding nobody measured.
    """
    text = _committed_poster_svg()
    size = (ATLAS / "known-best-1-324.svg").stat().st_size
    composite = known_best_builder.resolved_composites()[1].spec

    assert size == len(text.encode("utf-8"))
    assert size < POSTER_SVG_BUDGET_BYTES
    assert size / composite.square_count < 200

    root = ET.fromstring(text)
    squares = known_best_builder.summary_square_polygons(root)
    assert len(squares) == composite.square_count == 52650
    # No per-square data attribute survives, and that is the first lever.
    assert not [
        name for square in squares for name in square.attrib if name.startswith("data-")
    ]
    assert {tuple(sorted(square.attrib)) for square in squares} == {("fill", "points")}
    # The second lever: the stroke is stated once per card, on the group.
    groups = [node for node in root.iter() if node.attrib.get("data-feature") == "square-fills"]
    assert len(groups) == composite.count
    assert {group.attrib["stroke-width"] for group in groups} == {"0.42"}
    assert {group.attrib["stroke-linejoin"] for group in groups} == {"round"}
    # The third: every coordinate is rounded to the declared number of decimals.
    decimals = composite.coordinate_decimals
    assert decimals == 3
    lengths = {
        len(number.partition(".")[2])
        for square in squares
        for pair in square.attrib["points"].split(" ")
        for number in pair.split(",")
    }
    assert max(lengths) <= decimals
    # And the drawing says all three in its own metadata, so a copy of the file that
    # travels alone still carries what was left out of it and why.
    metadata = {
        node.attrib["name"]: node.text or ""
        for node in root.iter()
        if node.tag.endswith("}value") and "name" in node.attrib
    }
    assert metadata["physical-columns"] == "35"
    assert metadata["physical-rows"] == "18"
    assert "grid-suffix-second-line-from-row" not in metadata
    assert metadata["grid-suffix-layout"] == "inline"
    assert metadata["physical-row-pitch"] == "307"
    assert metadata["physical-column-pitch"] == "214"
    assert metadata["grid-transition-label-layout"] == "single-line"
    assert metadata["grid-transition-marker-clearance-ratio"] == "0.9"
    assert metadata["grid-transition-marker-outline-gap"] == "49.365"
    assert metadata["square-coordinate-decimals"] == "3"
    assert "atlas/known-best/rendering/n-NNN.svg" in metadata["square-data-attributes"]
    assert "52650" in metadata["square-stroke"]
    # The published figure keeps every one of them, which is what makes the poster's
    # departure a budget decision rather than a change of house style.
    figure_root = ET.fromstring(_committed_composite_svg())
    figure_squares = known_best_builder.summary_square_polygons(figure_root)
    assert len(figure_squares) == 5050
    assert all("data-hue-index" in square.attrib for square in figure_squares)
    # And says nothing about an encoding, because it departs from none: the three keys
    # below appear only on a drawing that had to leave something out. `square-count` is
    # not one of them -- every composite states how many squares it draws.
    figure_metadata = {
        node.attrib["name"] for node in figure_root.iter() if "name" in node.attrib
    }
    assert "square-count" in figure_metadata
    assert figure_metadata.isdisjoint(
        {"square-data-attributes", "square-stroke", "square-coordinate-decimals"}
    )


def test_the_poster_exports_carry_the_source_receipt() -> None:
    """The poster's raster and PDF name the SVG they were drawn from, as the figure's do.

    One raster rather than three, and the same rule: a receipt that is the digest of the
    one drawing is what makes "the PNG matches the PDF" checkable rather than asserted.
    """
    svg_text = _committed_poster_svg()
    expected = hashlib.sha256(svg_text.encode("utf-8")).hexdigest()
    exports = known_best_builder.resolved_composites()[1].rasters

    assert [export.path.name for export in exports] == ["known-best-1-324.png"]
    assert known_best_builder.png_summary_receipt(exports[0].path.read_bytes()) == (
        7871,
        5701,
        expected,
    )
    assert (
        render_composite_pdf.pdf_receipt(
            (ATLAS / "square-packings-324-20261008.pdf").read_bytes()
        )
        == expected
    )


def test_the_poster_badges_every_perfect_square_and_counts_them_in_its_legend() -> None:
    """`k = 11..18` join the tiling argument, and the legend counts its own cases.

    The badge is derived, never read from the catalogue's flag: `k**2` unit squares
    exactly tile a `k` by `k` container, so nothing can move. The eight new perfect
    squares are the first cases above 100 to earn it, and they earn the solid glyph --
    the one that means this repository established the property -- while the catalogue's
    two annotations keep the muted one they have on the figure.
    """
    root = ET.fromstring(_committed_poster_svg())
    cards = {
        int(card.attrib["data-n"]): card for card in root.findall(".//svg:g[@data-n]", SVG)
    }

    assert sorted(cards) == list(range(1, 325))
    solid_rigid = sorted(
        n
        for n, card in cards.items()
        for badge in card.findall(".//svg:rect[@data-feature='evidence-badge']", SVG)
        if badge.attrib["data-evidence"] == "known rigid" and badge.attrib["fill"] != "none"
    )
    assert solid_rigid == sorted([k * k for k in range(1, 19)] + [5, 11, 28, 40])
    assert set(solid_rigid) >= {121, 144, 169, 196, 225, 256, 289, 324}

    # The legend counts the poster's own 324 cases, not the corpus and not the figure's
    # hundred. Read the labels by their feature; the poster aligns them at the right
    # edge while the badge glyphs stay centred.
    legend = root.find(".//svg:g[@data-feature='evidence-legend']", SVG)
    assert legend is not None
    labels = [
        node.text for node in legend.findall(".//svg:text[@data-feature='legend-label']", SVG)
    ]
    assert labels == [
        "proved optimal (77 of 324)",
        "exact value known (295 of 324)",
        "only known numerically (29 of 324)",
        "rigid (22 of 324)",
        "recent result, since August, 2026 (297 of 324)",
        "colors indicate distinct tilt angles",
        "shade indicates number of full-side contacts",
        "deg is the algebraic degree of that side length",
    ]
    # The grid figure uses the same label construction and counts its own hundred cases.
    figure_legend = ET.fromstring(_committed_composite_svg()).find(
        ".//svg:g[@data-feature='evidence-legend']", SVG
    )
    assert figure_legend is not None
    assert [
        node.text
        for node in figure_legend.findall(".//svg:text[@data-feature='legend-label']", SVG)
    ][:5] == [
        "proved optimal (45 of 100)",
        "exact value known (97 of 100)",
        "only known numerically (3 of 100)",
        "rigid (14 of 100)",
        "recent result, since August, 2026 (81 of 100)",
    ]


def test_the_poster_left_the_published_figure_byte_for_byte_where_it_was() -> None:
    """The 1-100 family is not touched, and this is what says so inside pytest.

    The plan's acceptance criterion for the whole expansion is that the published
    figure is byte-identical after it, so the comparison is against the committed
    bytes rather than against a rebuild: a rebuild would agree with a builder that had
    changed the figure in the same way twice.

    Digests rather than the bytes, because the failure has to be readable: two 2.3 MB
    strings compared directly print a diff nobody can use, and what a reader needs to
    know is that the file moved, not where.
    """
    figure = ATLAS / "known-best-1-100.svg"
    committed = subprocess.run(
        ["git", "show", f"HEAD:packing/atlas/known-best/{figure.name}"],
        cwd=ROOT.parent,
        capture_output=True,
        check=False,
    )
    if committed.returncode != 0:  # pragma: no cover - only outside a git checkout
        pytest.skip("the published figure is not readable from git here")

    working = figure.read_bytes()
    assert (len(working), hashlib.sha256(working).hexdigest()) == (
        len(committed.stdout),
        hashlib.sha256(committed.stdout).hexdigest(),
    ), "the published 1-100 figure differs from the committed one"


@pytest.mark.parametrize("scale", [1, 2])
def test_known_best_composite_png_refuses_a_raster_of_the_wrong_size(
    scale: int, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The receipt names the canvas, so a raster drawn at another size cannot be written.

    The rasters and the PDF are drawn from the same SVG by the same rasteriser, and the
    only thing standing between a resized canvas and a stale export is this check. It
    runs for both scales because the guard compares against the export's own size, and
    a guard that only ever saw the 1x canvas would pass a 2x export that ignored it.
    """
    export = known_best_builder.RasterExport(
        path=tmp_path / f"summary-{scale}x.png",
        scale=scale,
        role="preview",
        manifest_key="png_preview",
        canvas_width=64,
        canvas_height=64,
    )
    wrong_size = cairosvg.svg2png(
        bytestring=b'<svg xmlns="http://www.w3.org/2000/svg" width="8" height="8"/>',
        output_width=8,
        output_height=8,
        background_color="white",
    )
    assert isinstance(wrong_size, bytes)
    monkeypatch.setattr(cairosvg, "svg2png", lambda **_kwargs: wrong_size)

    with pytest.raises(ValueError, match="PNG preview dimensions are 8x8"):
        known_best_builder._update_png_export(export, "<svg/>\n")  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert not export.path.exists()


def test_known_best_atlas_check_reports_the_pdf_export_too(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """One `--check` covers the whole composite family, the PDF included.

    `render_composite_pdf` owns the page and keeps its own check, but a reader who
    runs the atlas check should not be told three of four exports are current and
    left to discover the fourth by running a second command. The three states that
    matter are pinned here: absent, present with a receipt naming another SVG, and
    present with the right one.
    """
    svg_text = "<svg/>\n"
    digest = hashlib.sha256(svg_text.encode("utf-8")).hexdigest()
    canvas = known_best_builder.PRIMARY_COMPOSITE
    monkeypatch.setattr(render_composite_pdf, "ATLAS_ROOT", tmp_path)
    pdf = render_composite_pdf.composite_pdf(canvas.spec.stem)
    assert pdf == tmp_path / "square-packings-100-20261008.pdf"
    report = known_best_builder._composite_pdf_problems  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001

    def problems(text: str) -> list[str]:
        return report(canvas, text)

    assert problems(svg_text) == ["missing atlas/known-best/square-packings-100-20261008.pdf"]

    pdf.write_bytes(
        b"%PDF-1.5\n%%EOF\n%" + render_composite_pdf.PDF_SOURCE_KEY + b": " + b"0" * 64 + b"\n"
    )
    assert problems(svg_text) == [
        "missing or stale atlas/known-best/square-packings-100-20261008.pdf export receipt"
    ]

    pdf.write_bytes(
        b"%PDF-1.5\n%%EOF\n%"
        + render_composite_pdf.PDF_SOURCE_KEY
        + b": "
        + digest.encode("ascii")
        + b"\n"
    )
    assert problems(svg_text) == []


def _figure_entries() -> dict[int, dict]:
    record = json.loads(
        (ROOT / "atlas/known-best/composite-figure.json").read_text(encoding="utf-8")
    )
    return {entry["n"]: entry for entry in record["figure"]["entries"]}


def _frontier_rigidity(n: int) -> dict | None:
    text = (ROOT / f"frontier/n-{n:03d}.md").read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---", 2)[1])["packing"]["rigidity"]


def test_the_figure_never_claims_a_rigidity_its_record_does_not_carry() -> None:
    """`D-385`: the figure decided this from `n` and never opened the record.

    A module-level set of the four packings the catalogue annotates "Rigid." earned the
    same solid glyph as the ten derived from an exact tiling, so a source's word and a
    first-party argument rendered identically. This is `D-354`'s split failing to reach
    the figure lane, and the assertion below is the line that was missing.
    """
    for n, entry in _figure_entries().items():
        established = entry["rigidity"]["state"] == "established"
        block = _frontier_rigidity(n)
        carried = block is not None and block["property"] == "locally-rigid"
        assert established == carried, (
            f"n={n}: figure says {entry['rigidity']['state']} while the frontier record "
            f"says {None if block is None else block['property']}"
        )


def test_known_rigid_keeps_verified_and_catalogue_assurance_distinct_in_metadata() -> None:
    """The one dark R keeps the source assertion distinct from a verified proof.

    Existing established/catalogue totals remain separate assurance metadata while the
    printed known-rigid count includes both. An undetermined repository assessment is
    never restated as an independently verified local-rigidity proof.
    """
    record = json.loads(
        (ROOT / "atlas/known-best/composite-figure.json").read_text(encoding="utf-8")
    )
    entries = {entry["n"]: entry for entry in record["figure"]["entries"]}
    annotated = sorted(
        n for n, e in entries.items() if e["rigidity"]["basis"] == "catalogue-annotation"
    )

    assert annotated == [28, 40]
    assert record["figure"]["totals"]["rigidity_catalogue_annotated"] == len(annotated)
    # The 1-100 figure's legend counts its own cases, whatever the corpus has grown to.
    composite = next(
        c for c in record["figure"]["composites"] if c["stem"] == "known-best-1-100"
    )
    assert composite["totals"]["rigidity_catalogue_annotated"] == len(annotated)
    assert composite["totals"]["rigidity_established"] == 12
    assert composite["totals"]["rigidity_known"] == 14
    assert record["figure"]["totals"]["rigidity_known"] == 22
    for n in annotated:
        entry = entries[n]
        assert entry["rigidity"]["state"] == "not-established"
        rigid_badges = [badge for badge in entry["badges"] if badge["glyph"] == "R"]
        assert entry["rigidity"]["known_rigid"] is True
        assert [badge["style"] for badge in rigid_badges] == ["solid"]
        assert [badge["meaning"] for badge in rigid_badges] == ["known rigid"]

    # n=11 is the case the old rule under-credited: its rigidity is ours, not Kingbird's.
    assert entries[11]["rigidity"]["basis"] == "first-party-argument"
    assert [b["style"] for b in entries[11]["badges"] if b["glyph"] == "R"] == ["solid"]


def test_only_the_bound_numeral_carries_the_new_result_accent() -> None:
    """The star marks the case; the accent marks what is new about it.

    A first-party lower bound is new in the number it reaches, not in the function it
    bounds, so `s(n) >=` keeps the caption colour every other card sets it in and the
    numeral alone takes the accent that matches the star in the badge row above. The
    record decides which cases are starred; this decides how a starred one is set, and
    reads it off the drawing rather than the record so the two must agree.

    The separating space is asserted too. It is the one part of the line that a split
    into coloured runs can silently drop, and losing it would leave the drawing right
    and every reader that takes the text rather than the ink wrong.
    """
    root = ET.fromstring(_committed_composite_svg())
    record = json.loads((ATLAS / "composite-figure.json").read_text(encoding="utf-8"))

    accented: list[str] = []
    plain: list[str] = []
    for node in root.findall(".//svg:text[@data-feature='lower-bound']", SVG):
        assert node.attrib["fill"] == known_best_builder.SUMMARY_SMALL_FILL
        marked = [
            span
            for span in node.findall("svg:tspan", SVG)
            if span.attrib.get("fill") == FIRST_PARTY_ACCENT_COLOR
        ]
        assert len(marked) <= 1
        line = "".join(node.itertext())
        assert re.fullmatch(r"s\(\d+\) \u2265 [0-9.]+", line), line
        if not marked:
            plain.append(line)
            continue
        accented.append(line)
        value = marked[0].text or ""
        assert re.fullmatch(r"[0-9.]+", value), value
        assert line.endswith(" " + value), line

    # A starred case that is proved, s(32) = 6 among them, says so in the equality above
    # and draws no lower-bound line to accent; its star is still on the card.
    drawn = [
        entry
        for entry in record["figure"]["entries"]
        if entry["n"] <= 100 and entry["lower"]["shown"]
    ]
    expected_accented = [
        entry["lower"]["display"] for entry in drawn if entry["lower"]["recent_result"]
    ]
    expected_plain = [
        entry["lower"]["display"] for entry in drawn if not entry["lower"]["recent_result"]
    ]
    # The count is the current record's, so it is held while the figure shows the pinned
    # data. A figure that trails the pin shows the count of the data it was drawn from
    # (`sqpack.release`, rule 5), and `--check-composites` lists the cards that differ.
    identity = known_best_builder.retained_identity(_committed_composite_svg())
    if identity.current or not COMPOSITES_MAY_TRAIL:
        assert len(accented) == len(expected_accented)
        assert set(accented) == set(expected_accented)
        assert len(plain) == len(expected_plain)
        assert set(plain) == set(expected_plain)


def test_fast_composite_check_rejects_a_stale_bound_label(monkeypatch) -> None:
    canvas = known_best_builder.CompositeCanvas(
        CompositeSpec(first_n=18, last_n=18, columns=1, stem="synthetic")
    )
    expected_lower = "s(18) ≥ 4.679"
    monkeypatch.setattr(
        known_best_builder,
        "_figure_entries",
        lambda: {
            18: {
                "side": {"display": "s(18) ≤ 4.822876"},
                "lower": {"display": expected_lower, "shown": True},
            }
        },
    )
    root = ET.fromstring(
        """<svg xmlns="http://www.w3.org/2000/svg">
        <g data-feature="packing-card" data-n="18">
          <text data-feature="packing-label">18</text>
          <text data-feature="side-bound">s(18) ≤ 4.822876</text>
          <text data-feature="lower-bound">s(18) ≥ 4.67</text>
        </g>
        </svg>"""
    )

    expected = (
        "atlas/known-best/synthetic.svg n=18 lower-bound is "
        "('s(18) ≥ 4.67',); expected ('s(18) ≥ 4.679',)"
    )
    problems = known_best_builder._composite_label_problems(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        canvas, root
    )
    assert problems == [expected]

    lower = next(
        node
        for node in root.iter("{http://www.w3.org/2000/svg}text")
        if node.attrib.get("data-feature") == "lower-bound"
    )
    lower.text = expected_lower
    assert not known_best_builder._composite_label_problems(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        canvas, root
    )


def test_fast_composite_check_rejects_a_stamp_that_is_not_the_composites_own() -> None:
    """A composite's footer and dateline are held to the record of what it was drawn from.

    They used to be held to the pin, which is why re-pinning the data revision meant
    redrawing the posters. The record is the drawing's own, so a re-pin leaves both
    right, and a footer naming any other data is still caught without a rebuild.
    """
    canvas = known_best_builder.CompositeCanvas(
        CompositeSpec(first_n=18, last_n=18, columns=1, stem="synthetic")
    )
    identity = known_best_builder.CompositeIdentity("1" * 40, "2026-09-28")
    assert identity.dateline == "Including new results (September 28, 2026)"
    assert identity.stamp == edition_at("1" * 40)
    assert not identity.current
    root = ET.fromstring(
        f"""<svg xmlns="http://www.w3.org/2000/svg">
        <text data-feature="release-stamp">{PUBLICATION_VERSION}-000000</text>
        </svg>"""
    )

    problems = known_best_builder._composite_edition_problems(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        canvas, root, identity
    )
    expected = (
        f"atlas/known-best/synthetic.svg release-stamp is ('{PUBLICATION_VERSION}-000000',); "
        f"expected ({identity.poster_stamp!r},)"
    )
    assert problems == [expected]

    footer = next(
        node
        for node in root.iter("{http://www.w3.org/2000/svg}text")
        if node.attrib.get("data-feature") == "release-stamp"
    )
    footer.text = identity.poster_stamp
    assert not known_best_builder._composite_edition_problems(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        canvas, root, identity
    )


@pytest.mark.parametrize("triangle", [False, True])
@pytest.mark.parametrize(
    ("data_date", "formatted_date"),
    [("2026-10-08", "October 8, 2026"), ("2026-09-28", "September 28, 2026")],
)
def test_composite_identity_checks_each_modes_visible_date_and_edition(
    *, triangle: bool, data_date: str, formatted_date: str
) -> None:
    placement = (
        known_best_builder.CompositePlacement.square_bound_triangle
        if triangle
        else known_best_builder.CompositePlacement.row_major
    )
    canvas = known_best_builder.CompositeCanvas(
        CompositeSpec(1, 1, 1, "synthetic", placement=placement)
    )
    identity = known_best_builder.CompositeIdentity("1" * 40, data_date)
    assert identity.formatted_date == formatted_date
    assert identity.poster_stamp == f"{formatted_date} · {identity.stamp}"
    root = ET.Element(f"{{{SVG['svg']}}}svg")
    footer = ET.SubElement(root, f"{{{SVG['svg']}}}text", {"data-feature": "release-stamp"})
    correct = identity.poster_stamp
    footer.text = correct
    check = known_best_builder._composite_edition_problems  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert check(canvas, root, identity) == []
    root.remove(footer)
    assert any("release-stamp is ()" in problem for problem in check(canvas, root, identity))
    root.append(footer)
    duplicate = ET.SubElement(root, f"{{{SVG['svg']}}}text", {"data-feature": "release-stamp"})
    duplicate.text = correct
    assert any("release-stamp" in problem for problem in check(canvas, root, identity))
    root.remove(duplicate)
    footer.text = (
        f"{identity.stamp} · January 1, 2000"
        if triangle
        else f"{identity.stamp} · {formatted_date}"
    )
    assert any("release-stamp" in problem for problem in check(canvas, root, identity))
    footer.text = correct
    ET.SubElement(
        root, f"{{{SVG['svg']}}}text", {"data-feature": "release"}
    ).text = identity.dateline
    assert len(check(canvas, root, identity)) == 1
    assert "expected ()" in check(canvas, root, identity)[0]


def test_the_version_leaves_out_the_stamped_composites_the_video_code_and_docs() -> None:
    """What `sqpack.release` does not count as data is what the stamp would chase.

    Each composite and every export drawn from it carries the version, so each must be
    outside the data or re-stamping it would be a data commit; anything else left out
    is data the version stops seeing. Two other kinds are left out, and neither is data:
    the video spikes, which are code, and the prose on how a record is written or drawn --
    the registers' own READMEs and the figure playbook. `e560571f2` edited
    `frontier/README.md` alone and moved the version every artifact prints (2026-09-22),
    and `6f6bc89ec` did the same with the playbook's legend counts; each would have
    re-stamped the atlas over a documentation change.
    """

    def tracked(*pathspec: str) -> set[str]:
        listed = subprocess.run(
            ("git", "-C", str(REPOSITORY), "ls-files", "--", *pathspec),
            capture_output=True,
            text=True,
            check=False,
        )
        if listed.returncode != 0:
            pytest.skip(listed.stderr.strip() or "git cannot list tracked files here")
        return set(listed.stdout.split())

    left_out = tracked(*DATA_PATHS) - tracked(*data_pathspec())
    family = set()
    for canvas in known_best_builder.COMPOSITES:
        stem = canvas.spec.stem
        family.add(canvas.svg_path)
        family.update(export.path for export in canvas.rasters)
        family.add(render_composite_pdf.composite_pdf(stem))
    stamped = {path.resolve().relative_to(REPOSITORY).as_posix() for path in family}
    video = "packing/atlas/known-best/video/"
    docs = {
        "packing/frontier/README.md",
        "packing/atlas/known-best/README.md",
        "packing/atlas/known-best/FIGURE-PLAYBOOK.md",
    }
    assert {path for path in left_out if not path.startswith(video) and path not in docs} == (
        stamped
    )
    assert any(path.startswith(video) for path in left_out)
    # The three are tracked, so leaving them out is a rule about them and not a typo.
    assert docs <= left_out


def _unitsquare_digests() -> dict[int, str]:
    release = json.loads(UNITSQUARE_RESULTS.read_text(encoding="utf-8"))
    return {int(record["n"]): str(record["svg_sha256"]) for record in release["results"]}


def _case(n: int, side: str, source_key: str) -> known_best_builder.FrontierCase:
    return known_best_builder.FrontierCase(
        n=n,
        side=side,
        path=ROOT / f"frontier/n-{n:03d}.md",
        text="",
        reported_source_key=source_key,
    )


def _plan_for(
    case: known_best_builder.FrontierCase,
    catalogue: dict[int, tuple[str, int, tuple[int, ...]]] | None = None,
) -> known_best_builder.SourcePlan:
    """The builder's own source selection, which is what these three cases are about."""
    select = (
        known_best_builder._source_plan  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    )
    return select(case, catalogue or {}, _unitsquare_digests())


def test_a_unitsquare_case_is_chosen_by_its_record_rather_than_by_its_number() -> None:
    # The selector used to be the literal set {68, 69}. It is now what the record says
    # its bound came from, so a case joins the UnitSquare layer by being sourced there.
    # n = 103 is one of the four the prospective collection already retains, and it has
    # to resolve to those retained bytes rather than to a copy under this collection.
    plans = {
        n: _plan_for(_case(n, side, "[UnitSquare 2026]"))
        for n, side in ((68, "8.8033830747161083"), (103, "10.4783914611164"))
    }

    assert {n: plan.kind for n, plan in plans.items()} == {
        68: "unitsquare-rendering",
        103: "unitsquare-rendering",
    }
    assert plans[68].path == ROOT / "resources/web/known-best-packings/unitsquare/n068.svg"
    assert plans[103].path == ROOT / "resources/web/prospective-packings/unitsquare/n103.svg"
    assert plans[103].upstream_declared_sha256 == _unitsquare_digests()[103]


def test_a_packet_case_is_drawn_from_the_packets_retained_facts() -> None:
    # n = 211 was the grid until Joost de Winter's packing; a record naming his packet's
    # key moves the case onto that packet's facts, and a count the packet does not hold
    # is refused rather than sent back to the catalogue.
    key = "[de Winter n211 2026-09-16]"
    plan = _plan_for(_case(211, "14.99796070496771500150", key))
    assert plan.kind == "packet-derived-facts"
    assert plan.path == (
        ROOT / "resources/web/de-winter-square-packing-211-2026-09-16/facts/n-211.yaml"
    )
    assert plan.url.endswith("/n211__record.json")
    with pytest.raises(ValueError, match="retains no facts"):
        _plan_for(_case(212, "14.99", key))


def test_a_record_naming_the_release_the_release_does_not_carry_is_refused() -> None:
    with pytest.raises(ValueError, match="omits its SVG digest"):
        _plan_for(_case(107, "10.84666719284348", "[UnitSquare 2026]"))


def test_a_catalogue_case_is_unaffected_by_the_unitsquare_selector() -> None:
    catalogue = {71: ("square-71.svg", 71, (71,))}

    plan = _plan_for(_case(71, "8.9440715575703155", "[Kingbird 2026]"), catalogue)

    assert plan.kind == "kingbird-derived-facts"
    assert plan.url == "https://kingbird.myphotos.cc/packing/square-71.svg"


@pytest.mark.parametrize("n", refinement_houses.NUMBERS)
def test_each_refinement_atlas_source_binds_full_private_custody(n: int) -> None:
    entry = next(
        row
        for row in json.loads(known_best_builder.MANIFEST.read_text())["atlas"]["entries"]
        if row["n"] == n
    )
    _assert_witness_agrees_with_entry(entry, {})


@pytest.mark.parametrize(
    "scenario",
    [
        "unselected-source",
        "unselected-figure",
        "missing-figure-entry",
        "duplicate-figure-entry",
        "selected-build",
        "serialization",
        "success",
    ],
)
def test_selected_refresh_publishes_only_after_all_preflight_checks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, scenario: str
) -> None:
    packing = tmp_path / "packing"
    witness_root = packing / "witnesses/known-best"
    render_root = packing / "atlas/known-best/rendering"
    manifest_path = packing / "atlas/known-best/manifest.json"
    source_path = packing / "atlas/known-best/sources.json"
    figure_path = packing / "atlas/known-best/composite-figure.json"
    plans = {
        n: known_best_builder.SourcePlan("exact-grid", packing / "grids", "", n, (n,))
        for n in range(1, 5)
    }
    cases: dict[int, known_best_builder.BuiltCase] = {}
    manifest_entries = []
    for case in known_best_builder.retained_cases(range(1, 5)):
        n = case.frontier.n
        frontier = known_best_builder.FrontierCase(
            n, case.frontier.side, packing / f"frontier/n-{n:03d}.md", case.frontier.text, ""
        )
        cases[n] = known_best_builder.BuiltCase(
            frontier, plans[n], case.witness, case.witness_text, case.rendering_text
        )
        manifest_entries.append(
            {
                "n": n,
                "reported_side": frontier.side,
                "source": {"kind": "exact-grid", "path": "grids"},
            }
        )
        for path, text in (
            (frontier.path, frontier.text),
            (witness_root / f"n-{n:03d}.yaml", case.witness_text),
            (render_root / f"n-{n:03d}.svg", case.rendering_text),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    figure = {
        "figure": {
            "generated_by": "retained",
            "entries": [
                {"n": n, "side": {"display": cases[n].frontier.side}} for n in range(1, 5)
            ],
        }
    }
    manifest_path.write_text(json.dumps({"atlas": {"entries": manifest_entries}}))
    source_path.write_text('{"sources": "retained"}')
    figure_path.write_text(json.dumps(figure))
    before = {path: path.read_bytes() for path in packing.rglob("*") if path.is_file()}
    prospective = copy.deepcopy(figure)
    prospective["figure"]["generated_by"] = "refreshed-global-header"
    prospective["figure"]["entries"][0]["selected_update"] = True
    if scenario == "unselected-source":
        plans[2] = known_best_builder.SourcePlan(
            "packet-derived-facts", packing / "grids", "", 2, (2,)
        )
    if scenario == "unselected-figure":
        prospective["figure"]["entries"][1]["side"]["display"] = "1.999"
    if scenario == "missing-figure-entry":
        prospective["figure"]["entries"].pop()
    if scenario == "duplicate-figure-entry":
        prospective["figure"]["entries"][-1]["n"] = 3
    monkeypatch.setattr(known_best_builder, "CORPUS", CorpusRange(1, 4))
    monkeypatch.setattr(known_best_builder, "ROOT", packing)
    monkeypatch.setattr(known_best_builder, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(known_best_builder, "MANIFEST", manifest_path)
    monkeypatch.setattr(known_best_builder, "SOURCE_MANIFEST", source_path)
    monkeypatch.setattr(known_best_builder, "WITNESS_ROOT", witness_root)
    monkeypatch.setattr(known_best_builder, "RENDER_ROOT", render_root)
    monkeypatch.setattr(known_best_builder, "clear_build_caches", lambda: None)
    monkeypatch.setattr(known_best_builder, "source_plans", lambda: plans)
    monkeypatch.setattr(known_best_builder, "_frontier_case", lambda n: cases[n].frontier)
    monkeypatch.setattr(known_best_builder, "resolved_composites", lambda _entries: ())
    monkeypatch.setattr(
        known_best_builder, "_source_index", lambda _plans: {"sources": "updated"}
    )
    monkeypatch.setattr(build_composite_figure_data, "RECORD", figure_path)
    monkeypatch.setattr(
        build_composite_figure_data, "build_record", lambda **_kwargs: prospective
    )

    def selected_build(
        numbers: Sequence[int], workers: int
    ) -> list[known_best_builder.BuiltCase]:
        assert list(numbers) == [1]
        assert workers == 1
        if scenario == "selected-build":
            raise ValueError("selected witness is invalid")
        original = cases[1]
        witness = copy.deepcopy(original.witness)
        witness["id"] = "selected-rebuilt"
        return [
            known_best_builder.BuiltCase(
                original.frontier,
                original.source,
                witness,
                original.witness_text + "\n# refreshed selected witness\n",
                original.rendering_text + "\n<!-- refreshed selected rendering -->\n",
            )
        ]

    monkeypatch.setattr(known_best_builder, "built_cases", selected_build)
    if scenario == "serialization":

        def reject_frontier(case: known_best_builder.FrontierCase, witness_id: str) -> str:
            assert case.n == 1
            assert witness_id == "selected-rebuilt"
            raise ValueError("selected frontier serialization failed")

        monkeypatch.setattr(known_best_builder, "_frontier_with_witness", reject_frontier)
    if scenario != "success":
        messages = {
            "unselected-source": "unselected n=2 changed",
            "unselected-figure": "unselected figure n=2 changed",
            "missing-figure-entry": "requires a complete derived figure corpus",
            "duplicate-figure-entry": "requires a complete derived figure corpus",
            "selected-build": "selected witness is invalid",
            "serialization": "selected frontier serialization failed",
        }
        with pytest.raises(ValueError, match=messages[scenario]):
            known_best_builder.update_selected([1])
        after = {path: path.read_bytes() for path in packing.rglob("*") if path.is_file()}
        assert after == before
    else:
        known_best_builder.update_selected([1])
        after = {path: path.read_bytes() for path in packing.rglob("*") if path.is_file()}
        changed = {path for path in after if after[path] != before[path]}
        assert changed == {
            figure_path,
            manifest_path,
            source_path,
            cases[1].frontier.path,
            witness_root / "n-001.yaml",
            render_root / "n-001.svg",
        }
        assert json.loads(figure_path.read_text()) == prospective
        entries = json.loads(manifest_path.read_text())["atlas"]["entries"]
        assert entries[1:] == manifest_entries[1:]
        assert entries[0]["witness"]["id"] == "selected-rebuilt"


def test_poster_credits_order_supported_author_dates_without_redating_inherited_finders(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sources = {
        "recent": build_bound_citations.Source(
            "recent", ("Recent",), 2026, "GitHub", dated=date(2026, 10, 7)
        ),
        "day": build_bound_citations.Source(
            "day", ("Day",), 2026, "GitHub", dated=date(2026, 1, 2)
        ),
        "year": build_bound_citations.Source("year", ("Year",), 2026, "Catalogue"),
        "other": build_bound_citations.Source(
            "other", ("Unrelated",), 2026, "GitHub", dated=date(2026, 10, 8)
        ),
        "fallback": build_bound_citations.Source(
            "fallback", ("Fallback",), 1995, "GitHub", dated=date(1995, 3, 1)
        ),
    }
    cases = {
        1: {
            "found_by": ["Old"],
            "found_year": 1979,
            "improved_by": ["Recent"],
            "source_key": "recent",
        },
        2: {"found_by": ["Day"], "found_year": 2026, "source_key": "day"},
        3: {"found_by": ["Year"], "found_year": 2026, "source_key": "year"},
        4: {"found_by": ["Unknown"], "source_key": "other"},
        5: {"source_key": "fallback"},
        6: {
            "found_by": ["Old"],
            "found_year": 1980,
            "source_key": "other",
            "retrieved": "2099-12-31",
        },
    }
    register = build_bound_citations.Register(
        evidence={},
        results=[],
        sources=sources,
        names={name: name for name in ("Old", "Recent", "Day", "Year", "Unknown")},
    )
    monkeypatch.setattr(build_bound_citations, "load_register", lambda: register)
    monkeypatch.setattr(
        build_bound_citations, "load_case", lambda n: {"reported_upper_bound": cases[n]}
    )
    monkeypatch.setattr(
        build_bound_citations,
        "upper_citation",
        lambda n, _case, _register: {
            "source_key": cases[n]["source_key"],
            "text": "retained citation",
        },
    )
    read_credits = known_best_builder._poster_packing_credits  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    wrap = known_best_builder._poster_credit_lines  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    read_credits.cache_clear()
    try:
        packing_credits = read_credits(1, 6)
        dates = {
            name: supported for credit in packing_credits for name, supported in credit.dates
        }
        assert {
            supported
            for credit in packing_credits
            for name, supported in credit.dates
            if name == "Old"
        } == {1979, 1980}
        assert dates["Recent"] == date(2026, 10, 7)
        assert dates["Day"] == 2026
        assert dates["Year"] == 2026
        assert dates["Fallback"] == date(1995, 3, 1)
        assert "Unknown" not in dates
        printed = (
            " ".join(wrap(packing_credits))
            .removeprefix("Best packings due to ")
            .removesuffix(".")
        )
        assert printed.split(", ") == ["Old", "Fallback", "Day", "Recent", "Year", "Unknown"]
    finally:
        read_credits.cache_clear()


@pytest.fixture
def prospective_atlas(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    """Copy three real grid cases; only the selected case's display spelling will change."""
    packing = tmp_path / "packing"
    corpus = CorpusRange(12, 14)
    retained_manifest = json.loads(known_best_builder.MANIFEST.read_text())
    retained_manifest["atlas"]["entries"] = [
        entry for entry in retained_manifest["atlas"]["entries"] if entry["n"] in corpus.numbers
    ]
    retained_figure = json.loads(build_composite_figure_data.RECORD.read_text())
    retained_figure["figure"]["entries"] = [
        entry for entry in retained_figure["figure"]["entries"] if entry["n"] in corpus.numbers
    ]
    copies = {
        packing / "atlas/known-best/manifest.json": json.dumps(retained_manifest),
        packing / "atlas/known-best/composite-figure.json": json.dumps(retained_figure),
        packing / "resources/web/known-best-packings/sources.json": (
            known_best_builder.SOURCE_MANIFEST.read_text()
        ),
    }
    for n in corpus.numbers:
        for relative in (
            f"frontier/n-{n:03d}.md",
            f"witnesses/known-best/n-{n:03d}.yaml",
            f"atlas/known-best/rendering/n-{n:03d}.svg",
        ):
            copies[packing / relative] = (known_best_builder.ROOT / relative).read_text()
    for path, text in copies.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    for module in (known_best_builder, build_composite_figure_data):
        monkeypatch.setattr(module, "CORPUS", corpus)
        monkeypatch.setattr(module, "COMPOSITES", ())
        monkeypatch.setattr(module, "ROOT", packing)
        monkeypatch.setattr(module, "FRONTIER", packing / "frontier")
    monkeypatch.setattr(known_best_builder, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(
        known_best_builder, "MANIFEST", packing / "atlas/known-best/manifest.json"
    )
    monkeypatch.setattr(
        known_best_builder,
        "SOURCE_MANIFEST",
        packing / "resources/web/known-best-packings/sources.json",
    )
    monkeypatch.setattr(known_best_builder, "WITNESS_ROOT", packing / "witnesses/known-best")
    monkeypatch.setattr(
        known_best_builder, "RENDER_ROOT", packing / "atlas/known-best/rendering"
    )
    monkeypatch.setattr(
        build_composite_figure_data,
        "RECORD",
        packing / "atlas/known-best/composite-figure.json",
    )
    monkeypatch.setattr(rigidity_status, "MANIFEST", known_best_builder.MANIFEST)
    monkeypatch.setattr(
        known_best_builder,
        "composite_findings",
        lambda: known_best_builder.CompositeFindings((), ()),
    )
    rigidity_status.load_context.cache_clear()
    known_best_builder.clear_build_caches()
    try:
        yield packing
    finally:
        rigidity_status.load_context.cache_clear()
        known_best_builder.clear_build_caches()


@pytest.mark.parametrize("selected", [False, True], ids=["complete", "selected"])
@pytest.mark.parametrize("defect", [None, "geometry", "assessment", "catalogue"])
def test_refresh_uses_prospective_geometry_before_publishing_any_record(
    prospective_atlas: Path, *, selected: bool, defect: str | None
) -> None:
    packing = prospective_atlas
    retained_context = rigidity_status.load_context()
    assert retained_context.entries[13]["reported_side"] == "4.0"
    frontier = packing / "frontier/n-013.md"
    text = frontier.read_text()
    old = "  reported_upper_bound:\n    value: '4.0'"
    assert text.count(old) == 1
    text = text.replace(old, "  reported_upper_bound:\n    value: '4'")
    if defect == "geometry":
        text = text.replace(
            "  reported_upper_bound:\n    value: '4'",
            ("  reported_upper_bound:\n    value: '3.5'"),
        )
    elif defect == "assessment":
        text = text.replace("    property: not-rigid", "    property: locally-rigid")
        text = text.replace("    assurance: numerically-checked", "    assurance: verified")
        text = text.replace(
            "    method: numerical-multiprecision", "    method: exact-algebraic"
        )
    elif defect == "catalogue":
        text = text.replace("    catalogue_rigid: not-stated", "    catalogue_rigid: rigid")
    frontier.write_text(text)
    before = {path: path.read_bytes() for path in packing.rglob("*") if path.is_file()}

    refresh = (
        partial(known_best_builder.update_selected, [13])
        if selected
        else known_best_builder.update
    )
    if defect is not None:
        expected = {
            "geometry": "source side 4 disagrees with frontier 3.5",
            "assessment": "verified rigidity requires at least one verified evidence",
            "catalogue": "no source assertion matching the selected geometry",
        }
        with pytest.raises(ValueError, match=expected[defect]):
            refresh()
        assert {
            path: path.read_bytes() for path in packing.rglob("*") if path.is_file()
        } == before
        assert rigidity_status.load_context() is retained_context
        return

    refresh()
    manifest = json.loads(known_best_builder.MANIFEST.read_text())
    entries = {entry["n"]: entry for entry in manifest["atlas"]["entries"]}
    assert entries[13]["reported_side"] == "4"
    figure = json.loads(build_composite_figure_data.RECORD.read_text())["figure"]
    figures = {entry["n"]: entry for entry in figure["entries"]}
    assert figures[13]["side"]["value"] == "4"
    assert figures[13]["rigidity"]["assessed_geometry"]["reported_side"] == "4"
    old_figure = json.loads(before[build_composite_figure_data.RECORD])["figure"]
    old_figures = {entry["n"]: entry for entry in old_figure["entries"]}
    assert figures[13]["rigidity"]["assessments"] == old_figures[13]["rigidity"]["assessments"]
    assert not figures[13]["rigidity"]["known_rigid"]
    assert figures[13]["lower"] == old_figures[13]["lower"]
    assert figures[13]["exactness"] == old_figures[13]["exactness"]
    assert figures[13]["optimality"] == old_figures[13]["optimality"]
    for n in (12, 13, 14):
        for relative in (
            f"witnesses/known-best/n-{n:03d}.yaml",
            f"atlas/known-best/rendering/n-{n:03d}.svg",
        ):
            path = packing / relative
            assert path.read_bytes() == before[path]
        if n != 13:
            assert entries[n] == retained_context.entries[n]
            assert figures[n] == old_figures[n]
            path = packing / f"frontier/n-{n:03d}.md"
            assert path.read_bytes() == before[path]
    fresh_context = rigidity_status.load_context()
    assert fresh_context is not retained_context
    assert fresh_context.entries[13]["reported_side"] == "4"
    assert rigidity_status.rigidity_metadata(
        13, yaml.safe_load(frontier.read_text().split("---", 2)[1])["packing"]
    ) == {
        key: figures[13]["rigidity"][key]
        for key in ("known_rigid", "assessed_geometry", "assessments")
    }


def _print_text_ink_bounds(node: ET.Element) -> tuple[float, float]:
    atlas_print_font.register_print_fonts()
    atlas_print_font.verify_cairo_face()
    context = cairo.Context(cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None))
    options = cairo.FontOptions()
    options.set_hint_metrics(cairo.HINT_METRICS_OFF)
    context.set_font_options(options)
    context.select_font_face(
        node.attrib["font-family"].split(",")[0],
        cairo.FONT_SLANT_NORMAL,
        cairo.FONT_WEIGHT_BOLD,
    )
    context.set_font_size(float(node.attrib["font-size"]))
    _x, top, _width, height, _advance, _dy = context.text_extents("".join(node.itertext()))
    baseline = float(node.attrib["y"])
    return baseline + top, baseline + top + height


@pytest.fixture
def without_host_arial(monkeypatch: pytest.MonkeyPatch) -> None:
    """Simulate missing host Arial/Helvetica while retaining the real native renderer."""
    select = cairo.Context.select_font_face

    def unavailable_host_font(context, family, slant, weight):
        if family in {"Arial", "Helvetica"}:
            family = "Unprovisioned Atlas Host Font"
        return select(context, family, slant, weight)

    monkeypatch.setattr(cairo.Context, "select_font_face", unavailable_host_font)


@pytest.mark.parametrize("data_date", ["2026-10-08", "2026-08-08"])
@pytest.mark.usefixtures("without_host_arial")
def test_print_information_shares_content_style_and_measured_block_gaps(data_date: str) -> None:
    append = known_best_builder._append_composite_information  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    blocks = []
    for canvas in known_best_builder.resolved_composites():
        root = ET.Element("svg")
        append(
            root,
            spec=RenderSpec(overlays=frozenset()),
            canvas=canvas,
            identity=replace(
                known_best_builder.retained_identity(canvas.svg_path.read_text()),
                data_date=data_date,
            ),
        )
        block = root.find("svg:g[@data-feature='poster-information']", SVG)
        assert block is not None
        blocks.append(block)
        problem = [
            block.find(f"svg:text[@data-feature='{feature}']", SVG)
            for feature in ("explainer", "problem-explainer")
        ]
        assert all(node is not None for node in problem)
        problem_nodes = [node for node in problem if node is not None]
        assert (
            " ".join("".join(node.itertext()) for node in problem_nodes)
            == known_best_builder.POSTER_PROBLEM
        )
        legend = block.find("svg:g[@data-feature='evidence-legend']", SVG)
        credit_block = block.find("svg:g[@data-feature='packing-credits']", SVG)
        closing = [
            block.find(f"svg:text[@data-feature='{feature}']", SVG)
            for feature in ("credit", "release-stamp")
        ]
        assert legend is not None
        assert credit_block is not None
        attribution_blocks = [
            block.find(f"svg:g[@data-feature='{key}-credits']", SVG)
            for key in ("lower-bound", "optimality")
        ]
        assert all(node is not None for node in attribution_blocks)
        assert all(node is not None for node in closing)
        assert len(legend.findall("svg:g[@data-feature='legend-column']", SVG)) == 2
        assert len(legend.findall(".//svg:text[@data-feature='legend-label']", SVG)) == 8
        size = 48 if canvas.information_in_corner else 19
        body = [
            node
            for node in block.iter(f"{{{SVG['svg']}}}text")
            if node.attrib.get("data-feature")
            in {
                "legend-label",
                "packing-credit-line",
                "lower-bound-credit-line",
                "optimality-credit-line",
                "credit",
                "release-stamp",
                "citations",
                "repository",
            }
        ]
        assert all(node.attrib["fill"] == "#000000" for node in body)
        assert all(
            node.attrib["font-family"] == known_best_builder.POSTER_BODY_FONT for node in body
        )
        assert all(float(node.attrib["font-size"]) == size for node in body)
        assert block.find(".//svg:a", SVG) is None
        groups = [
            problem_nodes,
            list(legend.iter(f"{{{SVG['svg']}}}text")),
            list(credit_block.iter(f"{{{SVG['svg']}}}text")),
            *(
                list(node.iter(f"{{{SVG['svg']}}}text"))
                for node in attribution_blocks
                if node is not None
            ),
            [node for node in closing if node is not None],
        ]
        bounds = [
            (
                min(_print_text_ink_bounds(node)[0] for node in group),
                max(_print_text_ink_bounds(node)[1] for node in group),
            )
            for group in groups
        ]
        rectangles = legend.findall(".//svg:rect", SVG)
        bounds[1] = (
            min(bounds[1][0], *(float(node.attrib["y"]) for node in rectangles)),
            max(
                bounds[1][1],
                *(
                    float(node.attrib["y"]) + float(node.attrib["height"])
                    for node in rectangles
                ),
            ),
        )
        gaps = [below[0] - above[1] for above, below in pairwise(bounds)]
        assert gaps == pytest.approx([size * 3] * 5, abs=1.0)
        if canvas.information_in_corner:
            title = block.find("svg:text[@data-feature='poster-title']", SVG)
            assert title is not None
            assert title.attrib["fill"] == "#000000"
            assert _print_text_ink_bounds(problem_nodes[0])[0] - _print_text_ink_bounds(title)[
                1
            ] == pytest.approx(size * 3, abs=1.0)
            assert block.find("svg:text[@data-feature='release']", SVG) is None
            reference = block.find("svg:text[@data-feature='citations']", SVG)
            stamp = block.find("svg:text[@data-feature='release-stamp']", SVG)
            assert reference is not None
            assert stamp is not None
            assert _print_text_ink_bounds(reference)[0] - _print_text_ink_bounds(stamp)[
                1
            ] == pytest.approx(size * 3, abs=1.0)
        else:
            assert bounds[0][0] > float(
                canvas.card_position(100).top + known_best_builder.SUMMARY_CARD_HEIGHT
            )
            reference = root.find("svg:text[@data-feature='project-reference']", SVG)
            assert reference is not None
            assert reference.text == "The Squares Project · github.com/jlevy/squares"
            assert reference.attrib["fill"] == "#000000"
            assert block.find("svg:text[@data-feature='repository']", SVG) is None
            assert root.find("svg:text[@data-feature='release']", SVG) is None
        assert all(node.attrib["fill"] == "#000000" for node in problem_nodes)
        problem_size = 66 if canvas.information_in_corner else 66 * 19 / 48
        assert all(
            float(node.attrib["font-size"]) == pytest.approx(problem_size)
            for node in problem_nodes
        )
        assert ["".join(node.itertext()) for node in problem_nodes] == [
            "The square packing problem asks for the side s(n) of the smallest square that can",
            "hold n unit squares, where the squares are free to rotate but cannot overlap",
        ]
    credit_text = [
        " ".join(
            node.text or ""
            for node in block.findall(
                "svg:g/svg:text[@data-feature='packing-credit-line']", SVG
            )
        )
        for block in blocks
    ]
    assert credit_text[0] == credit_text[1]
    assert (
        len(credit_text[0].removeprefix("Best packings due to ").removesuffix(".").split(", "))
        == 22
    )


@pytest.mark.usefixtures("without_host_arial")
def test_print_boxed_glyph_ink_is_centered_at_card_and_legend_scales() -> None:
    append = known_best_builder._append_badge  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    for scale in (Decimal(1), known_best_builder.POSTER_LEGEND_TYPE_SCALE):
        for glyph in ("O", "=", "≈", "R"):
            root = ET.Element("svg")
            append(root, glyph, "solid", glyph, x=Decimal(0), top=Decimal(0), type_scale=scale)
            node = root.find("svg:text", SVG)
            box = root.find("svg:rect", SVG)
            assert node is not None
            assert box is not None
            top, bottom = _print_text_ink_bounds(node)
            context = cairo.Context(cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None))
            options = cairo.FontOptions()
            options.set_hint_metrics(cairo.HINT_METRICS_OFF)
            context.set_font_options(options)
            context.select_font_face(
                node.attrib["font-family"].split(",")[0],
                cairo.FONT_SLANT_NORMAL,
                cairo.FONT_WEIGHT_BOLD,
            )
            context.set_font_size(float(node.attrib["font-size"]))
            bearing, _y, width, _height, advance, _dy = context.text_extents(glyph)
            left = (
                float(node.attrib["x"])
                + bearing
                - (advance / 2 if node.attrib.get("text-anchor") == "middle" else 0)
            )
            center = float(box.attrib["width"]) / 2
            assert (left + width / 2, (top + bottom) / 2) == pytest.approx(
                (center, center), abs=0.25
            )


def test_print_card_math_uses_the_retained_italic_face_in_native_pdf() -> None:
    canvas = known_best_builder.PRIMARY_COMPOSITE
    position = canvas.card_position(11)
    width, height = (
        known_best_builder.SUMMARY_CARD_WIDTH,
        known_best_builder.SUMMARY_CARD_HEIGHT,
    )
    root = element(
        "svg",
        {
            "width": str(width),
            "height": str(height),
            "viewBox": f"{position.left} {position.top} {width} {height}",
        },
    )
    append = known_best_builder._append_summary_card  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    append(
        root,
        known_best_builder.retained_cases((11,))[0],
        spec=RenderSpec(overlays=frozenset()),
        canvas=canvas,
    )
    caption = root.find("svg:g/svg:text[@data-feature='side-bound']", SVG)
    assert caption is not None
    assert "".join(caption.itertext()) == "s(11) = 3.877084"
    atlas_print_font.register_print_fonts()
    pdf = cairosvg.svg2pdf(bytestring=ET.tostring(root))
    assert isinstance(pdf, bytes)
    fonts = re.findall(rb"/FontName\s*/([^\s/>]+)", pdf)
    # Quartz can render FAMILY + font-style=italic upright. The PDF's actual
    # embedded face proves that the card caption selected the retained companion.
    assert {font.split(b"+", 1)[-1] for font in fonts} == {
        b"SquaresAtlasPrint-Bold",
        b"SquaresAtlasPrint-BoldItalic",
    }
    italic = caption.find("svg:tspan[@font-style='italic']", SVG)
    assert italic is not None
    assert italic.attrib["font-family"] == atlas_print_font.ITALIC_FAMILY


def test_print_font_embeds_the_retained_faces_and_their_full_license() -> None:
    css = atlas_print_font.embedded_css()
    embedded = re.findall(r"data:font/ttf;base64,([^\"]+)", css)
    assert len(embedded) == 2
    license_text = atlas_print_font.LICENSE_PATH.read_text()
    assert license_text in css
    for encoded, path in zip(embedded, atlas_print_font.FONT_PATHS, strict=True):
        content = base64.b64decode(encoded)
        assert content == path.read_bytes()
        with TTFont(io.BytesIO(content)) as font:
            assert font["name"].getDebugName(1) == atlas_print_font.FAMILY
            assert font["name"].getDebugName(5) == "Version 2.1.5"
            assert font["name"].getDebugName(13) == license_text
            assert font["OS/2"].usWeightClass == 700  # pyright: ignore[reportAttributeAccessIssue]


def test_native_print_font_refuses_fallback_and_provisions_a_fresh_process() -> None:
    command = [sys.executable, "-B", "-m", "devtools.atlas_print_font"]
    # The unique family is never installed on the host. In a fresh process, Cairo's
    # fallback must be rejected rather than passing an ink measurement accidentally.
    missing = subprocess.run(
        [*command, "--verify-only"], capture_output=True, text=True, check=False
    )
    assert missing.returncode != 0
    assert "Cairo substituted the retained atlas print face" in missing.stderr
    provisioned = subprocess.run(command, capture_output=True, text=True, check=False)
    assert provisioned.returncode == 0, provisioned.stderr
    assert (
        "Cairo resolved retained Squares Atlas Print 2.1.5 bold and bold italic"
        in provisioned.stdout
    )


def test_print_font_css_requires_an_explicit_safe_serializer_path() -> None:
    root = element("svg")
    css = atlas_print_font.embedded_css()
    sub(root, "style", {"data-sqpack-style": PRINT_FONT_MARKER}).text = css
    with pytest.raises(ValueError, match="arbitrary CSS"):
        serialize_svg(root)
    serialized = serialize_svg(root, embedded_print_fonts=css)
    style = ET.fromstring(serialized).find("svg:style", SVG)
    assert style is not None
    assert style.text == css


@pytest.mark.parametrize(
    "unsafe_change",
    [
        lambda css: css.replace("data:font/ttf;base64,", "https://example.com/font.ttf#"),
        lambda css: css.replace("data:font/ttf;base64,", "data:image/svg+xml;base64,"),
        lambda css: css.replace("font-weight: 700", "font-weight: 400"),
        lambda css: css.replace('format("truetype")', 'format("opentype")'),
        lambda css: css.replace("font-style: italic", "font-style: normal"),
        lambda css: css.replace("Squares Atlas Print", "Host Arial"),
        lambda css: css + "\n@import url(https://example.com/style.css);",
        lambda css: css + "\ntext { fill: red; }",
        lambda css: css.split("*/", 1)[1],
        lambda css: re.sub(
            r"data:font/ttf;base64,[^\"]+", "data:font/ttf;base64,c2NyaXB0", css
        ),
        lambda css: re.sub(r"data:font/ttf;base64,[^\"]+", "data:font/ttf;base64,AAEAAA=", css),
    ],
)
def test_print_font_css_refuses_external_fonts_and_generic_css(unsafe_change) -> None:
    root = element("svg")
    css = unsafe_change(atlas_print_font.embedded_css())
    sub(root, "style", {"data-sqpack-style": PRINT_FONT_MARKER}).text = css
    with pytest.raises(ValueError, match="print font"):
        serialize_svg(root, embedded_print_fonts=css)


def test_print_credit_chronology_preserves_precision_and_unknown_priority() -> None:
    names = atlas_credit_attributions.chronological_names(
        {
            "Undated": None,
            "First": 1979,
            "Last": 2026,
            "DayLate": date(2002, 12, 1),
            "DayEarly": date(2002, 1, 1),
            "YearOnly": 2002,
            "TimestampLater": "2026-09-12T06:46:15-06:00",
            "TimestampEarlier": "2026-09-12T11:46:15Z",
        }
    )
    assert names[0] == "First"
    assert names[-1] == "Undated"
    assert names.index("DayEarly") < names.index("DayLate")
    assert names.index("DayLate") < names.index("TimestampEarlier")
    assert names.index("TimestampEarlier") < names.index("TimestampLater")
    # A year-only date can overlap either day: alphabetical ties express no priority.
    assert names.index("YearOnly") < names.index("TimestampEarlier")
    with pytest.raises(ValueError, match="timezone"):
        atlas_credit_attributions.chronological_names({"Unqualified": "2026-09-12T12:00:00"})


def test_shared_print_attributions_preserve_full_roles_sources_and_corpus_scope() -> None:
    expected_lower = [
        "Göbel",
        "Stromquist",
        "Kearney",
        "Shiu",
        "Bentz",
        "Daniel",
        "Vlasenko",
        "Guzhou0806",
        "Hosono",
        "Ahmed",
        "Karakuş",
        "Ryu",
    ]
    expected_optimal = [
        "Göbel",
        "Stromquist",
        "Friedman",
        "El Moumni",
        "Kearney",
        "Shiu",
        "Bentz",
        "Vlasenko",
        "Levy",
        "Daniel",
        "Hosono",
        "Ahmed",
        "Karakuş",
    ]
    attributions = known_best_builder._print_attributions()  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    lower, optimal = attributions.paragraphs
    assert list(lower.names) == expected_lower
    assert list(optimal.clauses[0].names) == expected_optimal
    assert set(optimal.clauses[1].names) == {"Gurevitch", "Guzhou0806"}
    assert set(optimal.clauses[2].names) == {"Lewis", "Julian-JJ", "EvolvingPrograms"}
    assert len(optimal.names) == len(set(optimal.names)) == 18
    assert "Nagamochi" not in optimal.names
    assert attributions.normalize_name("wand125") == "Hosono"
    assert attributions.normalize_name("chelokot") == "Vlasenko"
    assert attributions.normalize_name("unverified-handle") == "unverified-handle"
    rendered = []
    for canvas in known_best_builder.resolved_composites():
        root = ET.Element("svg")
        known_best_builder._append_composite_information(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
            root,
            spec=RenderSpec(overlays=frozenset()),
            canvas=canvas,
            identity=known_best_builder.retained_identity(canvas.svg_path.read_text()),
        )
        block = root.find("svg:g[@data-feature='poster-information']", SVG)
        assert block is not None
        assert block.attrib["data-credit-scope"] == known_best_builder.CORPUS.label
        assert block.attrib["data-depicted-range"] == canvas.spec.cases.label
        paragraphs = [
            block.find(f"svg:g[@data-feature='{key}-credits']", SVG)
            for key in ("packing", "lower-bound", "optimality")
        ]
        texts = []
        for paragraph in paragraphs:
            assert paragraph is not None
            assert paragraph.attrib["data-credit-scope"] == known_best_builder.CORPUS.label
            text = " ".join(node.text or "" for node in paragraph.findall("svg:text", SVG))
            assert not text.endswith(".")
            assert "[" not in text
            assert "]" not in text
            texts.append(text)
        rendered.append(texts)
        node = block.find("svg:metadata[@data-feature='credit-attributions']", SVG)
        assert node is not None
        assert node.text is not None
        assert "/Volumes/" not in node.text
        assert "/Users/" not in node.text
        metadata = json.loads(node.text)
        assert len(metadata["lower_bounds"]["contributors"]) == 20
        assert sorted(
            n for group in metadata["lower_bounds"]["case_groups"] for n in group["cases"]
        ) == list(range(1, 325))
        assert len(metadata["optimality"]["sources"]) == 31
        assert len(metadata["optimality"]["cases"]) == 77
        assert sum(case["n"] <= 100 for case in metadata["optimality"]["cases"]) == 45
        assert [case["n"] for case in metadata["construction"]["cases"]] == list(range(1, 325))
        method = next(
            person
            for person in metadata["lower_bounds"]["contributors"]
            if person["name"] == "Friedman"
        )
        assert "explicit-method-or-prerequisite-acknowledgment" in method["roles"]
        proof_sources = {source["id"]: source for source in metadata["optimality"]["sources"]}
        for case in metadata["optimality"]["cases"]:
            assert all(
                "defect" not in proof_sources[key]["status"]
                for key in case["direct_accepted_proof_ids"]
            )
        assert all("primary_sources" in source for source in proof_sources.values())
    assert rendered[0] == rendered[1]
    assert rendered[0][1].startswith("Lower bounds due to Göbel, Stromquist,")
    assert "formalization contributions by" in rendered[0][2]
    assert "verification infrastructure and execution by" in rendered[0][2]


def test_print_construction_credits_normalize_aliases_before_deduplicating() -> None:
    paragraph = known_best_builder._poster_credit_lines(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        (
            known_best_builder.PackingCredit(
                names=("wand125", "Hiroaki Hosono", "Hosono"),
                source_keys=("source",),
                citation="retained",
                dates=(("wand125", date(2026, 9, 28)), ("Hiroaki Hosono", date(2026, 9, 22))),
            ),
        )
    )
    assert paragraph == ("Best packings due to Hosono",)


def test_curated_print_credits_match_current_case_and_citation_associations() -> None:
    """A changed citation, proof case or source author requires re-auditing the input."""
    curated = json.loads((ATLAS / "credit-attributions.json").read_text())
    register = build_bound_citations.load_register()
    assert curated["credit_scope"] == [
        known_best_builder.CORPUS.first_n,
        known_best_builder.CORPUS.last_n,
    ]
    cases = {n: build_bound_citations.load_case(n) for n in known_best_builder.CORPUS.numbers}
    lower = {
        n: group for group in curated["lower_bounds"]["case_groups"] for n in group["cases"]
    }
    assert set(lower) == set(cases), "curated lower-bound credit coverage is stale"
    for n, case in cases.items():
        citation = build_bound_citations.lower_citation(n, case, register)
        expected = (
            {
                key: value
                for key, value in citation.items()
                if key not in {"value", "text", "note"}
            }
            if citation
            else None
        )
        assert lower[n]["citation_attribution"] == expected, (
            f"curated lower citation for n={n} is stale"
        )
        assert lower[n]["verified_evidence_ids"] == case["verified_lower_bound"].get(
            "evidence", []
        ), f"curated lower source associations for n={n} are stale"
        reported = case["reported_lower_bound"]
        assert lower[n]["reported_attribution"] == {
            "proved_by": reported.get("proved_by", []),
            "proved_year": reported.get("proved_year"),
            "source_key": reported.get("source_key"),
            "evidence": reported.get("evidence", []),
        }, f"curated reported lower credits for n={n} are stale"
    for source in curated["lower_bounds"]["sources"]:
        canonical = register.sources[source["source_key"]]
        assert source["authors_raw"] == list(canonical.authors), (
            f"curated lower authors for {canonical.key} are stale"
        )
        assert source["bibliography_record"] == {
            "key": canonical.key,
            "authors": list(canonical.authors),
            "year": canonical.year,
            "venue": canonical.venue,
            "credit": canonical.credit,
            "lineage": canonical.lineage,
            "dated": canonical.dated.isoformat() if canonical.dated else None,
        }, f"curated lower source citation for {canonical.key} is stale"
    optimal = {case["n"]: case for case in curated["optimality"]["cases"]}
    assert set(optimal) == {n for n, case in cases.items() if case["status"] == "proved"}, (
        "curated optimality case coverage is stale"
    )
    for n, attribution in optimal.items():
        assert attribution["canonical_status"] == cases[n]["status"]
        assert attribution["all_attached_evidence_ids"] == cases[n].get("evidence", []), (
            f"curated proof/source associations for n={n} are stale"
        )
    for citation in curated["optimality"]["canonical_citations"]:
        source = register.sources[citation["source_key"]]
        assert citation == {
            "source_key": source.key,
            "authors": list(source.authors),
            "year": source.year,
            "venue": source.venue,
            "credit": source.credit,
            "dated": source.dated.isoformat() if source.dated else None,
        }, f"curated optimality source credits for {source.key} are stale"
    proof_sources = curated["optimality"]["sources"]
    audit_only = set(curated["optimality"]["audit_only_citation_labels"])
    assert audit_only.isdisjoint(register.sources), (
        "historical audit citation gained a canonical row; refresh credit input"
    )
    assert {key for source in proof_sources for key in source["source_keys"]} == audit_only | {
        citation["source_key"] for citation in curated["optimality"]["canonical_citations"]
    }
    assert all(
        key in register.evidence for source in proof_sources for key in source["evidence_ids"]
    )
    assert all(
        key in {result["id"] for result in register.results}
        for source in proof_sources
        for key in source["result_ids"]
    )


def test_print_attribution_paragraphs_share_the_balanced_packing_measure() -> None:
    """Three complete credit paragraphs use one visual measure in both print layouts."""
    packing = known_best_builder._print_credit_lines()  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    paragraphs = known_best_builder._print_attributions().paragraphs  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    attributed = known_best_builder._print_attribution_lines()  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    width = known_best_builder._text_width  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    measure = max(width(line, known_best_builder.POSTER_BODY_SIZE) for line in packing)
    assert len(packing) == 3
    assert [len(lines) for lines in attributed] == [2, 4]
    for paragraph, lines in zip(paragraphs, attributed, strict=True):
        assert " ".join(lines) == " ".join(paragraph.atoms)
        assert (
            max(width(line, known_best_builder.POSTER_BODY_SIZE) for line in lines) <= measure
        )
        assert all(any(atom in line for line in lines) for atom in paragraph.atoms)
    for canvas in known_best_builder.resolved_composites():
        root = ET.Element("svg")
        known_best_builder._append_composite_information(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
            root,
            spec=RenderSpec(overlays=frozenset()),
            canvas=canvas,
            identity=known_best_builder.retained_identity(canvas.svg_path.read_text()),
        )
        block = root.find("svg:g[@data-feature='poster-information']", SVG)
        assert block is not None
        for key, expected in zip(
            ("packing", "lower-bound", "optimality"), (packing, *attributed), strict=True
        ):
            actual = tuple(
                node.text or ""
                for node in block.findall(
                    f"svg:g/svg:text[@data-feature='{key}-credit-line']", SVG
                )
            )
            assert actual == expected
        if canvas.information_in_corner:
            _assert_poster_text_clears_cards(block, canvas)


def test_print_attribution_wrap_refuses_an_atom_wider_than_the_shared_measure() -> None:
    """A long indivisible credited name cannot silently expand the shared paragraph width."""
    paragraph = known_best_builder.atlas_credit_attributions.CreditParagraph(
        "lower-bound",
        (
            known_best_builder.atlas_credit_attributions.CreditClause(
                "Lower bounds due to", ("W" * 100,)
            ),
        ),
    )
    with pytest.raises(ValueError, match="information block"):
        known_best_builder._balanced_credit_lines(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
            paragraph, measure=Decimal(1000)
        )
