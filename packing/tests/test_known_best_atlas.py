#!/usr/bin/env python3
"""Coverage and source-adapter checks for the retained known-best atlas."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

import cairosvg
import jsonschema
import pytest
import yaml

from devtools import build_known_best_atlas as known_best_builder
from devtools import render_composite_pdf
from sqpack.known_best import (
    CompositeSpec,
    SourceGeometryError,
    catalogue_source_map,
    parse_kingbird_svg,
    parse_unitsquare_svg,
)
from sqpack.render.color import ANGLE_CLASS_CONTRACT
from sqpack.render.model import RenderSpec
from sqpack.render.style import FIRST_PARTY_ACCENT_COLOR
from sqpack.witness import load_witness
from sqpack.workers import worker_count

#: Catalogue-derived witnesses above the hand-audited hundred, per corpus (think-93on).
GOLDEN_DERIVED_ABOVE_100: dict[str, int] = {"n=1..100": 0, "n=1..200": 46, "n=1..324": 107}
#: The cases whose retained upstream rendering is the UnitSquare release, per corpus.
GOLDEN_UNITSQUARE: dict[str, set[int]] = {
    "n=1..100": {68, 69},
    "n=1..200": {68, 69, 103, 105, 110, 131},
    "n=1..324": {68, 69, 103, 105, 110, 131},
}
#: How the corpus splits by source kind at each corpus; a case switching kind fails here.
GOLDEN_SOURCE_KINDS: dict[str, dict[str, int]] = {
    "n=1..100": {"exact-grid": 64, "kingbird-derived-facts": 34, "unitsquare-rendering": 2},
    "n=1..200": {"exact-grid": 114, "kingbird-derived-facts": 80, "unitsquare-rendering": 6},
    "n=1..324": {"exact-grid": 177, "kingbird-derived-facts": 141, "unitsquare-rendering": 6},
}

#: What the poster's vector may cost a clone. Eight mebibytes is the ceiling the
#: encoding was chosen against; the house encoding would have spent 24 MB on the same
#: 52,650 squares. A ceiling rather than a golden size, because the exact figure follows
#: from the corpus's geometry and a witness gaining a digit may move it.
POSTER_SVG_BUDGET_BYTES = 8 * 1024 * 1024

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


@pytest.mark.usefixtures("isolated_atlas_build_cache")
def test_known_best_rejects_corrupted_retained_unitsquare_svg(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
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
                "height": 5792,
                "path": "atlas/known-best/known-best-1-100@2x.png",
                "scale": 2,
                "width": 4800,
            },
            "png_link_preview_card": {
                "derived_from": "atlas/known-best/known-best-1-100.svg",
                "height": 1256,
                "path": "atlas/known-best/known-best-1-100-card.png",
                "scale": 1,
                "top_crop": True,
                "width": 2400,
            },
            "png_preview": {
                "derived_from": "atlas/known-best/known-best-1-100.svg",
                "height": 2896,
                "path": "atlas/known-best/known-best-1-100.png",
                "scale": 1,
                "width": 2400,
            },
            "range": {"count": 100, "first_n": 1, "last_n": 100},
            "renderer": "sqpack deterministic composite renderer",
            "rows": 10,
            "square_count": 5050,
            "stem": "known-best-1-100",
            "svg": {
                "height": 2896,
                "path": "atlas/known-best/known-best-1-100.svg",
                "width": 2400,
            },
        },
        # The poster: the same card scale over eighteen columns of eighteen, one raster
        # and no link-preview crop. Its absence of a `png_high_resolution` key is part of
        # the golden answer, not an omission -- a 2x of a 20.7-megapixel canvas is about
        # five megabytes on every clone for detail the PDF already carries.
        {
            "columns": 18,
            "layout": "18 by 18, row-major n=1..324",
            "png_preview": {
                "derived_from": "atlas/known-best/known-best-1-324.svg",
                "height": 4912,
                "path": "atlas/known-best/known-best-1-324.png",
                "scale": 1,
                "width": 4224,
            },
            "range": {"count": 324, "first_n": 1, "last_n": 324},
            "renderer": "sqpack deterministic composite renderer",
            "rows": 18,
            "square_count": 52650,
            "stem": "known-best-1-324",
            "svg": {
                "height": 4912,
                "path": "atlas/known-best/known-best-1-324.svg",
                "width": 4224,
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
    atlas.pop("composites")
    schema = yaml.safe_load(
        (ATLAS / "known-best-atlas.schema.yaml").read_text(encoding="utf-8")
    )

    jsonschema.validate(atlas, schema)


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
def test_known_best_composite_contains_every_case_and_square() -> None:
    # Pooled rather than serial, and the count comes from the same policy every other
    # pool-backed step reads: `PACK_JOBS` where a gate has capped it, the machine where
    # nothing has. This is the one test that pays the whole corpus build, and at
    # `n=1..324` that is 691.19s serial against 348.15s at two workers -- the deep gate
    # runs the slow lane at `--inner-jobs 2`, so this is what it costs there. The build is
    # memoized on the worker count, so the serial memo the corrupted-source test above
    # builds is untouched by this one.
    outputs, _manifest = known_best_builder.expected_outputs(
        worker_count(known_best_builder.CORPUS.count)
    )
    composite_path = ATLAS / "known-best-1-100.svg"

    # The pin the quick lane's four composite tests stand on: they read the retained
    # vector, and this is where "retained" and "built" are made one thing inside pytest.
    # Free here -- the build above is already paid -- and checked again from the other
    # side by the full gate's `known-best n=1..324 atlas rebuild` step.
    assert composite_path.read_text(encoding="utf-8") == outputs[composite_path]

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
    # A proved optimum is stated as an equality, a best-known bound as <=.
    assert all(re.fullmatch(r"s\(\d+\) [=≤] .+", bound) for bound in bounds)
    assert sum(" = " in bound for bound in bounds) == 35


def test_known_best_composite_png_is_derived_from_current_svg() -> None:
    svg_text = _committed_composite_svg()
    png = (ATLAS / "known-best-1-100.png").read_bytes()

    assert known_best_builder.png_summary_receipt(png) == (
        2400,
        2896,
        hashlib.sha256(svg_text.encode("utf-8")).hexdigest(),
    )


def test_known_best_composite_high_resolution_png_is_derived_from_current_svg() -> None:
    """The 2x export is pinned to the same canvas and the same source as the preview.

    It exists so the atlas can be attached or downscaled without going back to the
    vector, which means it is the copy most likely to be handed to someone who cannot
    check it. Pinning the exact pixel count matters as much as pinning the receipt:
    4800 by 5792 is twice 2400 by 2896, and the whole-number scale is what keeps the
    file small. A fractional scale puts every edge on a fractional pixel boundary, and
    the antialiasing shades the rasteriser then invents cost more bytes than the extra
    pixels do -- a 4096-wide export of this drawing is 11% larger than this one while
    carrying 27% fewer pixels.
    """
    svg_text = _committed_composite_svg()
    png = (ATLAS / "known-best-1-100@2x.png").read_bytes()

    assert known_best_builder.png_summary_receipt(png) == (
        4800,
        5792,
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
    receipts["known-best-1-100.pdf"] = render_composite_pdf.pdf_receipt(
        (ATLAS / "known-best-1-100.pdf").read_bytes()
    )

    assert set(receipts) == {
        "known-best-1-100.png",
        "known-best-1-100@2x.png",
        "known-best-1-100-card.png",
        "known-best-1-100.pdf",
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
    """The published figure's numbers, as the golden answer to the formulas.

    2400 by 2896, a legend at 2732 and a footer at 2804/2834/2864 were absolute
    constants until the layout was parameterized, and they are what
    `CompositeCanvas` returns for ten columns of ten. Pinning them literally here is
    what makes the derivation checkable: a formula that quietly stopped agreeing with
    the drawing would fail this before it reached a byte comparison.
    """
    canvas = known_best_builder.PRIMARY_COMPOSITE
    composite = canvas.spec

    assert (composite.first_n, composite.last_n, composite.columns) == (1, 100, 10)
    assert (composite.count, composite.rows, composite.square_count) == (100, 10, 5050)
    assert composite.layout == "10 by 10, row-major n=1..100"
    assert composite.card_units == 1256
    assert (canvas.width, canvas.height) == (2400, 2896)
    assert canvas.grid_bottom == 2694
    assert canvas.legend_baseline == 2732
    assert canvas.explainer_baseline == 2804
    assert canvas.credit_baseline == 2834
    assert canvas.stamp_baseline == 2864
    assert (composite.svg_name, composite.pdf_name) == (
        "known-best-1-100.svg",
        "known-best-1-100.pdf",
    )
    assert composite.raster_name(1) == "known-best-1-100.png"
    assert composite.raster_name(2) == "known-best-1-100@2x.png"
    assert composite.card_png_name == "known-best-1-100-card.png"


def test_the_poster_canvas_is_what_its_specification_computes() -> None:
    """The poster's numbers, as the golden answer to the same formulas.

    Written as literals for the same reason the figure's are: 4224 by 4912, a legend at
    4748 and a footer at 4820/4850/4880 are what `CompositeCanvas` returns for eighteen
    columns of eighteen, and a formula that quietly stopped agreeing with the drawing
    should fail here rather than in a byte comparison.
    """
    canvas = known_best_builder.COMPOSITES[1]
    composite = canvas.spec

    assert (composite.first_n, composite.last_n, composite.columns) == (1, 324, 18)
    assert (composite.count, composite.rows, composite.square_count) == (324, 18, 52650)
    assert composite.square_count == 324 * 325 // 2
    assert composite.layout == "18 by 18, row-major n=1..324"
    assert composite.cases.label == "n=1..324"
    assert (canvas.width, canvas.height) == (4224, 4912)
    assert canvas.grid_bottom == 4710
    assert canvas.legend_baseline == 4748
    assert canvas.explainer_baseline == 4820
    assert canvas.credit_baseline == 4850
    assert canvas.stamp_baseline == 4880
    assert (composite.svg_name, composite.pdf_name) == (
        "known-best-1-324.svg",
        "known-best-1-324.pdf",
    )
    assert composite.raster_name(1) == "known-best-1-324.png"
    # One raster and no crop: the export set is part of the specification.
    assert composite.card_units is None
    assert [export.manifest_key for export in canvas.rasters] == ["png_preview"]
    assert composite.stem in known_best_builder.SUMMARY_PROSE


def test_a_second_composite_is_a_specification_and_not_a_second_set_of_constants() -> None:
    """Nothing in the poster's geometry is absolute; all of it is the figure's, shifted.

    This is the whole point of the parameterization, and it is asserted as differences
    rather than as literals -- the literals are the test above -- because what is being
    checked here is that no constant was edited by hand: eight more columns is eight more
    column pitches of width, and eight more rows moves the legend and all three footer
    lines by eight row pitches.
    """
    poster = known_best_builder.COMPOSITES[1]
    figure = known_best_builder.PRIMARY_COMPOSITE

    extra_columns = poster.spec.columns - figure.spec.columns
    extra_rows = poster.spec.rows - figure.spec.rows
    widening = extra_columns * known_best_builder.SUMMARY_COLUMN_PITCH
    shift = extra_rows * known_best_builder.SUMMARY_ROW_PITCH
    assert poster.width == figure.width + widening
    assert poster.grid_bottom == figure.grid_bottom + shift
    assert poster.legend_baseline == figure.legend_baseline + shift
    assert poster.explainer_baseline == figure.explainer_baseline + shift
    assert poster.credit_baseline == figure.credit_baseline + shift
    assert poster.stamp_baseline == figure.stamp_baseline + shift
    assert poster.height == figure.height + shift

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
    composite = known_best_builder.COMPOSITES[1].spec

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
    exports = known_best_builder.COMPOSITES[1].rasters

    assert [export.path.name for export in exports] == ["known-best-1-324.png"]
    assert known_best_builder.png_summary_receipt(exports[0].path.read_bytes()) == (
        4224,
        4912,
        expected,
    )
    assert (
        render_composite_pdf.pdf_receipt((ATLAS / "known-best-1-324.pdf").read_bytes())
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
        if badge.attrib["data-evidence"] == "rigid (established here)"
        and badge.attrib["fill"] != "none"
    )
    assert solid_rigid == sorted([k * k for k in range(1, 19)] + [5, 11])
    assert set(solid_rigid) >= {121, 144, 169, 196, 225, 256, 289, 324}

    # The legend counts the poster's own 324 cases, not the corpus and not the figure's
    # hundred. Read off the drawing: a badge's glyph is centred and a label is not, so
    # the labels are the runs that carry no anchor.
    legend = root.find(".//svg:g[@data-feature='evidence-legend']", SVG)
    assert legend is not None
    labels = [
        node.text
        for node in legend.findall("svg:text", SVG)
        if node.attrib.get("text-anchor") is None
    ]
    assert labels == [
        "proved optimal (59)",
        "exact value known (287)",
        "only known numerically (37)",
        "rigid (established here) (20)",
        "annotated rigid by the catalogue (2)",
        "lower bound first proved here (7)",
        "colors indicate distinct tilt angles",
        "shade indicates number of full-side contacts",
    ]
    # The published figure's legend is unmoved by any of it.
    figure_legend = ET.fromstring(_committed_composite_svg()).find(
        ".//svg:g[@data-feature='evidence-legend']", SVG
    )
    assert figure_legend is not None
    assert [
        node.text
        for node in figure_legend.findall("svg:text", SVG)
        if node.attrib.get("text-anchor") is None
    ][:5] == [
        "proved optimal (35)",
        "exact value known (95)",
        "only known numerically (5)",
        "rigid (established here) (12)",
        "annotated rigid by the catalogue (2)",
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
    assert pdf == tmp_path / "known-best-1-100.pdf"
    report = known_best_builder._composite_pdf_problems  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001

    def problems(text: str) -> list[str]:
        return report(canvas, text)

    assert problems(svg_text) == ["missing atlas/known-best/known-best-1-100.pdf"]

    pdf.write_bytes(
        b"%PDF-1.5\n%%EOF\n%" + render_composite_pdf.PDF_SOURCE_KEY + b": " + b"0" * 64 + b"\n"
    )
    assert problems(svg_text) == [
        "missing or stale atlas/known-best/known-best-1-100.pdf export receipt"
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


def test_a_catalogue_annotation_is_shown_but_never_counted() -> None:
    """Dropping the annotation would lose a fact; merging it was the defect.

    The figure keeps it, as a muted badge on a `not-established` entry, and the totals
    count the two separately. `n = 5` was the case that made this earn its keep, because
    `X-007` established more about it than the catalogue ever said and still not local
    rigidity. It left the annotated set on 2026-09-03, when `T-014` proved local rigidity
    at fixed side and moved the entry to a first-party basis, which is the transition
    this separation exists to make visible: the catalogue's claim is still carried on the
    entry, and it is still not what the total counts.
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
    for n in annotated:
        entry = entries[n]
        assert entry["rigidity"]["state"] == "not-established"
        rigid_badges = [badge for badge in entry["badges"] if badge["glyph"] == "R"]
        assert [badge["style"] for badge in rigid_badges] == ["muted"]

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

    assert len(accented) == record["figure"]["totals"]["lower_bound_first_proved_here"]
    assert len(plain) > len(accented)


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


def test_a_record_naming_the_release_the_release_does_not_carry_is_refused() -> None:
    with pytest.raises(ValueError, match="omits its SVG digest"):
        _plan_for(_case(107, "10.84666719284348", "[UnitSquare 2026]"))


def test_a_catalogue_case_is_unaffected_by_the_unitsquare_selector() -> None:
    catalogue = {71: ("square-71.svg", 71, (71,))}

    plan = _plan_for(_case(71, "8.9440715575703155", "[Kingbird 2026]"), catalogue)

    assert plan.kind == "kingbird-derived-facts"
    assert plan.url == "https://kingbird.myphotos.cc/packing/square-71.svg"
