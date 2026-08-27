#!/usr/bin/env python3
"""Coverage and source-adapter checks for the retained known-best atlas."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

import jsonschema
import pytest
import yaml

from devtools import build_known_best_atlas as known_best_builder
from sqpack.known_best import (
    SourceGeometryError,
    catalogue_source_map,
    parse_kingbird_svg,
    parse_unitsquare_svg,
)
from sqpack.render.color import ANGLE_CLASS_CONTRACT
from sqpack.render.model import RenderSpec
from sqpack.witness import load_witness

ROOT = Path(__file__).resolve().parent.parent
ATLAS = ROOT / "atlas/known-best"
SOURCES = ROOT / "resources/web/known-best-packings"
WITNESSES = ROOT / "witnesses/known-best"
SCHEMA = ROOT / "witnesses/witness.schema.yaml"
UNITSQUARE_RESULTS = ROOT / "resources/web/unitsquare-release1-2026/results.json"
SVG = {"svg": "http://www.w3.org/2000/svg"}


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
        51,
        52,
        53,
        54,
        55,
        65,
        66,
        67,
        70,
        71,
        82,
        83,
        84,
        85,
        86,
        87,
        88,
        89,
    }
    assert {record["n"] for record in kingbird} == expected_n
    assert len(kingbird) == len(expected_n)
    for record in kingbird:
        assert record["attribution"].startswith("SVG and high-precision updates")
        assert record["source_n"] == record["n"]
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
    assert {record["n"] for record in unitsquare} == {68, 69}
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


def test_known_best_rejects_corrupted_retained_unitsquare_svg(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    isolated_atlas_build_cache: None,
) -> None:
    source = SOURCES / "unitsquare/n068.svg"
    monkeypatch.setattr(known_best_builder, "UNITSQUARE_ROOT", tmp_path)
    (tmp_path / "n068.svg").write_bytes(source.read_bytes() + b"\n")

    with pytest.raises(ValueError, match="upstream-declared SVG SHA-256"):
        known_best_builder.expected_outputs()


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
    "href", ("missing", "#missing", "packing.svg#one", "https://example/one")
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
    assert document["atlas"]["composite"] == {
        "layout": "10 by 10, row-major n=1..100",
        "png_preview": {
            "derived_from": "atlas/known-best/known-best-1-100.svg",
            "height": 2516,
            "path": "atlas/known-best/known-best-1-100.png",
            "width": 2400,
        },
        "renderer": "sqpack deterministic composite renderer",
        "square_count": 5050,
        "svg": {
            "height": 2516,
            "path": "atlas/known-best/known-best-1-100.svg",
            "width": 2400,
        },
    }
    assert [entry["n"] for entry in entries] == list(range(1, 101))
    assert Counter(entry["source"]["kind"] for entry in entries) == {
        "exact-grid": 64,
        "kingbird-derived-facts": 34,
        "unitsquare-rendering": 2,
    }

    for entry in entries:
        n = entry["n"]
        witness_path = ROOT / entry["witness"]["path"]
        witness = load_witness(witness_path, fallback_schema=SCHEMA)
        assert witness["n"] == n
        assert witness["id"] == entry["witness"]["id"]
        assert len(witness["squares"]) == n
        if entry["source"]["kind"] == "kingbird-derived-facts":
            assert entry["source"]["path"] == ("resources/web/known-best-packings/sources.json")
            assert witness["source"]["key"] == "Kingbird derived numerical facts"
            assert witness["source"]["path"] == entry["source"]["path"]
            assert "not a legal conclusion" in witness["claim"]["limitations"]
        elif entry["source"]["kind"] == "unitsquare-rendering":
            assert witness["source"]["revision"] == (
                f"upstream-declared parent-content SHA-256 {release_by_n[n]['record_sha256']}"
            )
        assert (ROOT / entry["rendering"]["path"]).is_file()
        frontier = (ROOT / entry["frontier_path"]).read_text(encoding="utf-8")
        assert f"    - {witness['id']}\n" in frontier

    n29_frontier = (ROOT / "frontier/n-029.md").read_text(encoding="utf-8")
    assert "    - W-n029-kingbird\n" in n29_frontier


def test_known_best_v1_schema_accepts_a_manifest_without_the_new_composite() -> None:
    atlas = json.loads((ATLAS / "manifest.json").read_text(encoding="utf-8"))["atlas"]
    atlas.pop("composite")
    schema = yaml.safe_load(
        (ATLAS / "known-best-atlas.schema.yaml").read_text(encoding="utf-8")
    )

    jsonschema.validate(atlas, schema)


def test_known_best_composite_contains_every_case_and_square() -> None:
    outputs, _manifest = known_best_builder.expected_outputs()
    composite_path = ATLAS / "known-best-1-100.svg"

    root = ET.fromstring(outputs[composite_path])
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
    assert len(bounds) == 100
    assert all(bound.startswith("s ≤ ") for bound in bounds)


def test_known_best_composite_png_is_derived_from_current_svg() -> None:
    outputs, _manifest = known_best_builder.expected_outputs()
    svg_text = outputs[ATLAS / "known-best-1-100.svg"]
    png = (ATLAS / "known-best-1-100.png").read_bytes()

    assert known_best_builder.png_summary_receipt(png) == (
        2400,
        2516,
        hashlib.sha256(svg_text.encode("utf-8")).hexdigest(),
    )


def test_known_best_composite_png_reports_renderer_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    summary_svg = tmp_path / "summary.svg"
    monkeypatch.setattr(known_best_builder, "SUMMARY_SVG", summary_svg)
    monkeypatch.setattr(known_best_builder, "SUMMARY_PNG", tmp_path / "summary.png")
    monkeypatch.setattr(
        known_best_builder,
        "expected_outputs",
        lambda: ({summary_svg: "<svg/>\n"}, {}),
    )
    monkeypatch.setattr(known_best_builder.shutil, "which", lambda _name: "/usr/bin/false")

    with pytest.raises(RuntimeError, match="PNG preview renderer exited 1"):
        known_best_builder.update()
