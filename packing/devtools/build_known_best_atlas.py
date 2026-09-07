#!/usr/bin/env python3
"""Acquire, normalize, validate, and render the known-best atlas and its composites."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import struct
import time
import urllib.error
import urllib.request
import zlib
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from functools import cache
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET

import mpmath as mp
from strif import atomic_output_file

from devtools import build_composite_figure_data, render_composite_pdf
from devtools.build_composite_figure_data import load_record as load_figure_record
from sqpack.known_best import (
    KINGBIRD_ATTRIBUTION,
    KINGBIRD_BASE_URL,
    KINGBIRD_LICENSE_STATUS,
    KINGBIRD_RETENTION_POLICY,
    KNOWN_BEST_COMPOSITES,
    KNOWN_BEST_CORPUS,
    RETRIEVED_DATE,
    UNITSQUARE_BASE_URL,
    CompositeSpec,
    CorpusRange,
    catalogue_source_map,
    exact_grid_witness,
    kingbird_derived_witness,
    parse_unitsquare_svg,
    rational_integer,
    unitsquare_witness,
)
from sqpack.release import PUBLICATION_DATE, PUBLICATION_EDITION
from sqpack.render import render_packing_svg
from sqpack.render.color import (
    ANGLE_CLASS_CONTRACT,
    assign_square_colors,
    hex_oklch,
    square_fill_palette,
)
from sqpack.render.model import (
    CheckKind,
    CheckSummary,
    EvidenceTier,
    PackingFrame,
    Point2,
    RenderSpec,
    SquareGeometry,
)
from sqpack.render.numbers import (
    emission_precision,
    format_svg_number,
    scalar_from_decimal,
    scalar_from_fraction,
)
from sqpack.render.style import FIRST_PARTY_ACCENT_COLOR, LABEL_MUTED_COLOR, PAPER_THEME
from sqpack.render.svg import (
    append_metadata,
    append_title_desc,
    element,
    serialize_svg,
    sub,
)
from sqpack.witness import (
    check_witness_semantics,
    load_witness,
    materialize_witness,
    witness_document,
)
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY_ROOT = ROOT.parent
FRONTIER = ROOT / "frontier"
CATALOGUE = ROOT / "resources/web/kingbird-squares-in-squares.html"
SOURCE_ROOT = ROOT / "resources/web/known-best-packings"
UNITSQUARE_ROOT = SOURCE_ROOT / "unitsquare"
UNITSQUARE_RESULTS = ROOT / "resources/web/unitsquare-release1-2026/results.json"
SOURCE_MANIFEST = SOURCE_ROOT / "sources.json"
WITNESS_ROOT = ROOT / "witnesses/known-best"
KINGBIRD_RAW_ROOT = SOURCE_ROOT / "kingbird"
WITNESS_SCHEMA = ROOT / "witnesses/witness.schema.yaml"
ATLAS_ROOT = ROOT / "atlas/known-best"
RENDER_ROOT = ATLAS_ROOT / "rendering"
MANIFEST = ATLAS_ROOT / "manifest.json"
GENERATOR = "python -m devtools.build_known_best_atlas"
USER_AGENT = "thinking-scratchpad-known-best-atlas/1.0"

#: The cases this build covers, end to end: sources, witnesses, house renderings,
#: frontier back-links and manifest entries.
CORPUS: CorpusRange = KNOWN_BEST_CORPUS
#: Every composite drawn from that corpus. One today; the geometry below is computed
#: from each specification rather than written down, so a second is a second entry.
COMPOSITE_SPECS: tuple[CompositeSpec, ...] = KNOWN_BEST_COMPOSITES

SUMMARY_GRID_LEFT = Decimal(60)
SUMMARY_GRID_TOP = Decimal(174)
SUMMARY_COLUMN_PITCH = Decimal(228)
SUMMARY_ROW_PITCH = Decimal(252)
#: The margin either side of the grid. One column pitch is a card plus its gutter, so
#: the trailing gutter falls into the right margin and the two read the same.
SUMMARY_SIDE_MARGIN = SUMMARY_GRID_LEFT
SUMMARY_CARD_WIDTH = Decimal(216)
SUMMARY_CARD_HEIGHT = Decimal(242)
SUMMARY_PACKING_SIZE = Decimal(158)
SUMMARY_PACKING_INSET_X = Decimal(24)
SUMMARY_PACKING_INSET_Y = Decimal(12)
SUMMARY_LABEL_BASELINE = Decimal(203)
SUMMARY_BOUND_BASELINE = Decimal(220)
# The certified floor, one line of house leading under the upper bound. The row pitch
# above carries the extra 17px, so the whitespace between a caption and the packing
# below it is what it always was.
SUMMARY_LOWER_BASELINE = Decimal(237)
# A five-pointed star, apex up, drawn as a polygon about its own centre. Not a glyph:
# Helvetica and its metric substitutes have no star, and the PNG and PDF rasterisers
# both render U+2605 as a replacement box, which would ship tofu in two of the three
# formats.
SUMMARY_STAR_POINTS = (
    (Decimal(0), Decimal(-6)),
    (Decimal("1.411"), Decimal("-1.942")),
    (Decimal("5.706"), Decimal("-1.854")),
    (Decimal("2.283"), Decimal("0.742")),
    (Decimal("3.527"), Decimal("4.854")),
    (Decimal(0), Decimal("2.4")),
    (Decimal("-3.527"), Decimal("4.854")),
    (Decimal("-2.283"), Decimal("0.742")),
    (Decimal("-5.706"), Decimal("-1.854")),
    (Decimal("-1.411"), Decimal("-1.942")),
)
SUMMARY_STAR_INSET = Decimal(6)
#: The star's reference size: the size of the caption it was drawn for, so a star beside
#: larger type scales by the ratio and stays the same weight against its text.
SUMMARY_STAR_REFERENCE_SIZE = Decimal(14)
SUMMARY_STAR_TEXT_INSET = Decimal(17)
SUMMARY_BADGE_SIZE = Decimal(19)
#: Air between the bottom of the grid and the first legend row's baseline.
SUMMARY_LEGEND_GAP = Decimal(38)
#: Air between the last legend row and the explainer, which opens the footer block.
SUMMARY_FOOTER_GAP = Decimal(44)
#: Leading inside the footer block: explainer, credit, edition stamp.
SUMMARY_FOOTER_LINE_PITCH = Decimal(30)
#: Air under the last footer line, which is where the canvas ends.
SUMMARY_BOTTOM_MARGIN = Decimal(32)
#: The footer gloss, as runs of (text, italic). The variables are set in italic like the
#: ones on the cards; `deg` is a function name and stays upright.
SUMMARY_EXPLAINER_RUNS = (
    ("s", True),
    ("(", False),
    ("n", True),
    (") is the side of the smallest square holding ", False),
    ("n", True),
    (" unit squares; deg is the algebraic degree of that side length", False),
)
SUMMARY_EXPLAINER = "".join(text for text, _italic in SUMMARY_EXPLAINER_RUNS)
# Cap height as a fraction of font size, used to sit the badges flush with the
# top of the card number rather than on its baseline.
SUMMARY_LABEL_CAP_RATIO = Decimal("0.70")
# One size for every small grey label: the bound, the degree, the legend and the
# credit line, so they cannot drift apart.
SUMMARY_SMALL_SIZE = "14"
# The footer block -- legend, explainer, credit -- reads at arm's length rather
# than beside a packing, so it sits larger than the card labels and takes bold.
# Helvetica has no semibold, so bold is the only heavier face available.
SUMMARY_FOOTER_SIZE = "19"
# Helvetica-Bold advance widths in units of 1/1000 em, for the characters the
# figure actually sets. A uniform per-character estimate cannot center a mixed
# string: it put the two legend rows 107px and 189px off center, in opposite
# amounts, because their character mixes differ.
_HELVETICA_BOLD_WIDTHS = {
    " ": 278,
    "(": 333,
    ")": 333,
    ",": 278,
    "-": 333,
    ".": 278,
    "/": 278,
    ":": 333,
    "=": 584,
    "\u2264": 584,
    "\u2265": 584,
    "\u2248": 584,
    "\u00b0": 400,
    "a": 556,
    "b": 611,
    "c": 556,
    "d": 611,
    "e": 556,
    "f": 333,
    "g": 611,
    "h": 611,
    "i": 278,
    "j": 278,
    "k": 556,
    "l": 278,
    "m": 889,
    "n": 611,
    "o": 611,
    "p": 611,
    "q": 611,
    "r": 389,
    "s": 556,
    "t": 333,
    "u": 611,
    "v": 556,
    "w": 778,
    "x": 556,
    "y": 556,
    "z": 500,
    "A": 722,
    "B": 722,
    "C": 722,
    "D": 722,
    "E": 667,
    "F": 611,
    "G": 778,
    "H": 722,
    "I": 278,
    "J": 556,
    "K": 722,
    "L": 611,
    "M": 833,
    "N": 722,
    "O": 778,
    "P": 667,
    "Q": 778,
    "R": 722,
    "S": 667,
    "T": 611,
    "U": 722,
    "V": 667,
    "W": 944,
    "X": 667,
    "Y": 667,
    "Z": 611,
}
_DEFAULT_ADVANCE = 556


def _text_width(text: str, size: str) -> Decimal:
    """Advance width of a string set in Helvetica Bold at this size."""
    units = sum(_HELVETICA_BOLD_WIDTHS.get(ch, _DEFAULT_ADVANCE) for ch in text)
    return Decimal(units) * Decimal(size) / Decimal(1000)


SUMMARY_FOOTER_WEIGHT = "700"
SUMMARY_LEGEND_ROW_PITCH = Decimal(28)
# Helvetica offers regular and bold and nothing between, so there is no semibold
# to ask for: the card labels take bold, the only heavier face available, over a
# darker grey. The footer block stays regular so the two do not compete.
SUMMARY_SMALL_WEIGHT = "700"
SUMMARY_SMALL_FILL = LABEL_MUTED_COLOR
# Letters sit on their cap height, math symbols on the math axis, so a single
# baseline cannot center both inside the badge box. Offsets are from the box top.
SUMMARY_BADGE_FONT_SIZE = Decimal(15)
#: Where a math symbol sits in a badge. `=` and `≈` centre on the math axis rather than
#: on the cap line, so they are placed by measurement rather than by the rule below.
SUMMARY_MATH_GLYPH_BASELINE = Decimal(14)
#: How much of the badge box the star fills. A five-pointed star reads smaller than a
#: filled square of the same span, so it is drawn larger to carry the same weight in the
#: row beside the lettered badges.
SUMMARY_BADGE_STAR_SPAN = Decimal("0.92")
SUMMARY_CREDIT = "Diagram by Joshua Levy with assistance from Claude and Codex"
#: The edition stamp, last of the footer lines and in the same voice as the rest of it.
#: Taken whole from `sqpack.release` rather than assembled here: this line and the
#: explainer's credits are the two places an edition is stamped, and they used to build
#: the same string from the same parts in two files.
SUMMARY_RELEASE_STAMP = PUBLICATION_EDITION
SUMMARY_REPOSITORY = "github.com/jlevy/squares"
# Set a step above the other small labels so the URL reads as part of the
# heading block rather than as another footnote.
#: One size for the two lines under the title: the release line and the repository.
SUMMARY_SUBTITLE_SIZE = "26"
SUMMARY_REPOSITORY_SIZE = SUMMARY_SUBTITLE_SIZE
SUMMARY_RELEASE_BASELINE = Decimal(114)
SUMMARY_RELEASE_SIZE = SUMMARY_SUBTITLE_SIZE
SUMMARY_RELEASE_TEXT = f"Including new results ({PUBLICATION_DATE})"
SUMMARY_RELEASE_GAP = Decimal(11)
SUMMARY_SUBTITLE_BASELINE = Decimal(148)
# Helvetica, with Arial as the metric-compatible stand-in where Helvetica is
# absent. No webfont is referenced, so nothing is fetched at render time and the
# figure is the same family everywhere it is opened.
SUMMARY_FONT = "Helvetica, Arial, sans-serif"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
# The one failure this catches: the committed PNG was exported from an older SVG.
# --check rebuilds the SVG and compares it in full, but nothing otherwise ties the
# export to it, and re-rendering a 25x26in page on every gate run to compare bytes
# costs far more than reading a tEXt chunk. Not a tamper check; a staleness link.
PNG_SOURCE_KEY = b"sqpack-source-svg-sha256"
PNG_RENDER_TIMEOUT_SECONDS = 120


@dataclass(frozen=True)
class FrontierCase:
    n: int
    side: str
    path: Path
    text: str


@dataclass(frozen=True)
class SourcePlan:
    kind: str
    path: Path
    url: str
    source_n: int
    listed_n: tuple[int, ...]
    upstream_declared_sha256: str | None = None


@dataclass(frozen=True)
class BuiltCase:
    frontier: FrontierCase
    source: SourcePlan
    witness: dict
    witness_text: str
    rendering_text: str


@dataclass(frozen=True)
class RasterExport:
    """One PNG export of a composite, at a whole multiple of the drawing's units.

    ``width`` and ``height`` are computed from the canvas this export was made for
    rather than stored, so a resized canvas moves every export with it and cannot
    leave one behind at the old size.
    """

    path: Path
    scale: int
    role: str
    #: What the manifest calls this export. Named alongside the role rather than
    #: derived from the scale, so two exports of one composite cannot collide on a key.
    manifest_key: str
    #: The composite's canvas, in drawing units. Carried on the export because the
    #: receipt written into the PNG names the size, which is what refuses a raster
    #: drawn against a canvas that has since moved.
    canvas_width: int
    canvas_height: int
    #: Drawing units kept from the top, or None for the whole canvas. A cropped
    #: export is rendered from a copy of the SVG whose viewport is this tall, so the
    #: rasteriser draws the band directly rather than drawing the canvas and
    #: discarding most of it, and no image library enters the pipeline.
    crop_units: int | None = None

    @property
    def width(self) -> int:
        return self.canvas_width * self.scale

    @property
    def height(self) -> int:
        return (self.crop_units or self.canvas_height) * self.scale

    @property
    def name(self) -> str:
        return f"atlas/known-best/{self.path.name}"


# What each whole-number scale is called, in a drift report and in the manifest. The
# scales themselves are a property of the composite; these are the names, and a
# composite that publishes a third scale names it here rather than being given a
# derived one that could collide with another export's key.
#
# The scales are whole numbers on purpose, and the reason is measured rather than
# aesthetic: a fractional scale puts every edge in the drawing on a fractional pixel
# boundary, so the rasteriser invents an antialiasing shade for each one and PNG loses
# the flat runs it compresses. Rendered from the 1-100 composite, a 4096-pixel-wide
# export (a scale of 4096/2400) carries 48,456 distinct colours in 1,440,555 bytes,
# while its 2x export carries 32,201 in 1,294,115 -- 37% more pixels for 10% fewer
# bytes. The obvious round number is the more expensive one, so it is not used.
#
# 2x rather than 3x because 3x costs 2,150,682 bytes for detail past what the
# 1x preview already resolves, and this is a binary paid for on every clone.
SUMMARY_RASTER_NAMES: dict[int, tuple[str, str]] = {
    1: ("preview", "png_preview"),
    2: ("high-resolution export", "png_high_resolution"),
}
#: The crop is its own export rather than another scale: it is the top of the same
#: drawing, at 1x, and what makes it a card is the viewport rather than the size.
SUMMARY_CARD_NAMES = ("link-preview card", "png_link_preview_card")


def _whole_units(value: Decimal, what: str) -> int:
    """A canvas dimension, refused unless it lands on a whole drawing unit."""
    if value != value.to_integral_value():
        raise ValueError(f"{what} is {value}, which is not a whole number of units")
    return int(value)


@dataclass(frozen=True)
class CompositeCanvas:
    """Where every part of one composite sits, computed from its specification.

    Nothing here is an absolute constant. The canvas is the grid the specification asks
    for, plus the margins, the legend and the footer, so a composite of another size
    moves all of them together instead of leaving a baseline behind at a number chosen
    for a canvas that no longer exists. The 1-100 figure's 2400 by 2896 canvas, its
    legend at 2732 and its footer at 2804/2834/2864 are what these formulas return for
    ten columns of ten.
    """

    spec: CompositeSpec

    @property
    def width(self) -> int:
        """A side margin either side of `columns` cells of one column pitch each."""
        return _whole_units(
            SUMMARY_SIDE_MARGIN * 2 + SUMMARY_COLUMN_PITCH * self.spec.columns,
            f"{self.spec.stem} width",
        )

    @property
    def grid_bottom(self) -> Decimal:
        """One row pitch below the last row's top, where the footer block begins."""
        return SUMMARY_GRID_TOP + SUMMARY_ROW_PITCH * self.spec.rows

    @property
    def legend_baseline(self) -> Decimal:
        """The first legend row; the second sits one legend pitch under it."""
        return self.grid_bottom + SUMMARY_LEGEND_GAP

    @property
    def explainer_baseline(self) -> Decimal:
        return self.legend_baseline + SUMMARY_LEGEND_ROW_PITCH + SUMMARY_FOOTER_GAP

    @property
    def credit_baseline(self) -> Decimal:
        return self.explainer_baseline + SUMMARY_FOOTER_LINE_PITCH

    @property
    def stamp_baseline(self) -> Decimal:
        return self.credit_baseline + SUMMARY_FOOTER_LINE_PITCH

    @property
    def height(self) -> int:
        return _whole_units(
            self.stamp_baseline + SUMMARY_BOTTOM_MARGIN, f"{self.spec.stem} height"
        )

    @property
    def svg_path(self) -> Path:
        return ATLAS_ROOT / self.spec.svg_name

    @property
    def rasters(self) -> tuple[RasterExport, ...]:
        """Every PNG of this composite, drawn in one run and from one SVG."""
        exports = [
            RasterExport(
                path=ATLAS_ROOT / self.spec.raster_name(scale),
                scale=scale,
                role=SUMMARY_RASTER_NAMES[scale][0],
                manifest_key=SUMMARY_RASTER_NAMES[scale][1],
                canvas_width=self.width,
                canvas_height=self.height,
            )
            for scale in self.spec.raster_scales
        ]
        if self.spec.card_units is not None:
            role, key = SUMMARY_CARD_NAMES
            exports.append(
                RasterExport(
                    path=ATLAS_ROOT / self.spec.card_png_name,
                    scale=1,
                    role=role,
                    manifest_key=key,
                    canvas_width=self.width,
                    canvas_height=self.height,
                    crop_units=self.spec.card_units,
                )
            )
        return tuple(exports)


#: Every composite this build draws, laid out.
COMPOSITES: tuple[CompositeCanvas, ...] = tuple(
    CompositeCanvas(spec) for spec in COMPOSITE_SPECS
)
#: The composite the explainer, the README and the rendering checks name by path.
#: Every other one is reached through `COMPOSITES`.
PRIMARY_COMPOSITE = COMPOSITES[0]
SUMMARY_SVG = PRIMARY_COMPOSITE.svg_path

#: The accessible title and description, per composite. Prose about a particular range
#: is written rather than computed -- nothing spells "one through one hundred" from two
#: integers -- so it is recorded per stem, and a composite with no entry here cannot be
#: rendered rather than being given another figure's words.
SUMMARY_PROSE: dict[str, tuple[str, str]] = {
    "known-best-1-100": (
        "Best known packings of one through one hundred unit squares",
        (
            "A ten-by-ten atlas of the retained best known unit-square packings for "
            "n equals 1 through 100. Each tile is normalized to its own container and "
            "labeled with n, the best known upper bound on the container side and, where "
            "the value is not yet settled, the best proved lower bound beneath it. A star "
            "in crimson marks a lower bound first proved by this project. Badges mark "
            "which side lengths are proved optimal, and whether a side length is pinned "
            "exactly by a radical or a minimal polynomial rather than only by a decimal."
        ),
    ),
}


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _plural(count: int) -> str:
    """The `s` a count of one does not take, so a report reads for either count."""
    return "" if count == 1 else "s"


def _frontier_case(n: int) -> FrontierCase:
    path = FRONTIER / f"n-{n:03d}.md"
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path.name}: missing frontmatter")
    metadata = safe_load(text.split("---\n", 2)[1])
    packing = metadata["packing"]
    if packing["n"] != n:
        raise ValueError(f"{path.name}: frontier identity mismatch")
    return FrontierCase(n, str(packing["reported_upper_bound"]["value"]), path, text)


def _source_plan(
    case: FrontierCase,
    catalogue: dict[int, tuple[str, int, tuple[int, ...]]],
    unitsquare_svg_digests: dict[int, str],
) -> SourcePlan:
    integer_side = rational_integer(case.side)
    if integer_side is not None and integer_side * integer_side >= case.n:
        return SourcePlan("exact-grid", case.path, "", case.n, (case.n,))
    if case.n in {68, 69}:
        filename = f"n{case.n:03d}.svg"
        upstream_digest = unitsquare_svg_digests.get(case.n)
        if upstream_digest is None:
            raise ValueError(f"n={case.n}: UnitSquare release omits its SVG digest")
        return SourcePlan(
            "unitsquare-rendering",
            UNITSQUARE_ROOT / filename,
            f"{UNITSQUARE_BASE_URL}/{filename}",
            case.n,
            (case.n,),
            upstream_digest,
        )
    if case.n not in catalogue:
        raise ValueError(f"n={case.n}: non-grid frontier value has no catalogue geometry")
    filename, source_n, listed_n = catalogue[case.n]
    return SourcePlan(
        "kingbird-derived-facts",
        WITNESS_ROOT / f"n-{case.n:03d}.yaml",
        f"{KINGBIRD_BASE_URL}/{filename}",
        source_n,
        listed_n,
    )


def clear_build_caches() -> None:
    """Drop the memoized source plans and built cases.

    Only source_plans() needs clearing. It reads the module-level source roots,
    so a caller that repoints one -- the negative controls do, to corrupt a
    retained SVG on purpose -- would otherwise read or leave a plan set built
    against the other root. _build_case() is keyed on the plan itself, which
    carries the source path and its declared digest, so a corrupted source is a
    different key and cannot collide with the real one.
    """
    source_plans.cache_clear()
    _expected_outputs.cache_clear()


@cache
def source_plans() -> dict[int, SourcePlan]:
    catalogue = catalogue_source_map(CATALOGUE)
    release = json.loads(UNITSQUARE_RESULTS.read_text(encoding="utf-8"))
    unitsquare_svg_digests = {
        int(record["n"]): str(record["svg_sha256"]) for record in release["results"]
    }
    return {
        n: _source_plan(_frontier_case(n), catalogue, unitsquare_svg_digests)
        for n in CORPUS.numbers
    }


def _check_upstream_svg_digest(plan: SourcePlan, content: bytes) -> None:
    expected = plan.upstream_declared_sha256
    if plan.kind != "unitsquare-rendering" or expected is None:
        raise ValueError(f"n={plan.source_n}: UnitSquare SVG digest declaration is missing")
    if hashlib.sha256(content).hexdigest() != expected:
        raise ValueError(
            f"n={plan.source_n}: retained UnitSquare SVG differs from the "
            "upstream-declared SVG SHA-256"
        )


def _fetch_one(plan: SourcePlan, *, refresh: bool) -> str:
    if plan.kind == "exact-grid":
        return "grid"
    if plan.kind == "kingbird-derived-facts":
        if not plan.path.is_file():
            raise FileNotFoundError(
                f"retained Kingbird derived facts are missing: {_relative(plan.path)}"
            )
        return "derived"
    if plan.path.is_file() and not refresh:
        _check_upstream_svg_digest(plan, plan.path.read_bytes())
        return "retained"
    request = urllib.request.Request(plan.url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                content = response.read()
        except (OSError, urllib.error.HTTPError, urllib.error.URLError) as error:
            last_error = error
            if attempt < 2:
                time.sleep(2**attempt)
        else:
            if b"<svg" not in content[:100_000]:
                raise ValueError(f"upstream response is not SVG: {plan.url}")
            _check_upstream_svg_digest(plan, content)
            plan.path.parent.mkdir(parents=True, exist_ok=True)
            with atomic_output_file(plan.path) as temporary:
                temporary.write_bytes(content)
            return "fetched"
    raise RuntimeError(f"failed to fetch {plan.url}: {last_error}")


def fetch_sources(*, refresh: bool) -> None:
    plans = source_plans()
    unique = {plan.path: plan for plan in plans.values() if plan.kind == "unitsquare-rendering"}
    counts = {"fetched": 0, "retained": 0}
    for index, plan in enumerate(sorted(unique.values(), key=lambda item: item.url), start=1):
        result = _fetch_one(plan, refresh=refresh)
        counts[result] += 1
        print(f"  [{index:02d}/{len(unique):02d}] {result:8} {plan.path.name}")
        if result == "fetched":
            time.sleep(0.15)
    print(f"sources ready: {counts['fetched']} fetched, {counts['retained']} retained")


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _source_index(plans: dict[int, SourcePlan]) -> dict:
    sources = []
    for n, plan in sorted(plans.items()):
        if plan.kind == "exact-grid":
            continue
        if plan.kind == "kingbird-derived-facts":
            sources.append(
                {
                    "attribution": KINGBIRD_ATTRIBUTION,
                    "kind": plan.kind,
                    "license_status": KINGBIRD_LICENSE_STATUS,
                    "listed_n": list(plan.listed_n),
                    "n": n,
                    "raw_asset_retained": False,
                    "retention_policy": KINGBIRD_RETENTION_POLICY,
                    "retrieved": RETRIEVED_DATE,
                    "source_n": plan.source_n,
                    "url": plan.url,
                }
            )
            continue
        if not plan.path.is_file():
            raise FileNotFoundError(f"retained source is missing: {_relative(plan.path)}")
        content = plan.path.read_bytes()
        _check_upstream_svg_digest(plan, content)
        sources.append(
            {
                "bytes": len(content),
                "kind": plan.kind,
                "listed_n": list(plan.listed_n),
                "n": n,
                "path": _relative(plan.path),
                "raw_asset_retained": True,
                "retrieved": RETRIEVED_DATE,
                "source_n": plan.source_n,
                "upstream_declared_sha256": plan.upstream_declared_sha256,
                "url": plan.url,
            }
        )
    return {
        "contract": "packing.squares:KnownBestSourceInventory/v1",
        "retrieved": RETRIEVED_DATE,
        "sources": sources,
    }


def _assert_side_matches(case: FrontierCase, actual: str) -> None:
    with mp.workdps(120):
        difference = abs(mp.mpf(case.side) - mp.mpf(actual))
        tolerance = max(mp.mpf("1e-8"), abs(mp.mpf(case.side)) * mp.mpf("1e-12"))
    if difference > tolerance:
        raise ValueError(
            f"n={case.n}: source side {actual} disagrees with frontier {case.side}"
        )


def _build_witness(case: FrontierCase, plan: SourcePlan) -> dict:
    frontier_path = _relative(case.path)
    if plan.kind == "exact-grid":
        side = rational_integer(case.side)
        if side is None:
            raise ValueError(f"n={case.n}: grid plan has noninteger side")
        return exact_grid_witness(case.n, side, frontier_path=frontier_path)
    try:
        if plan.kind == "kingbird-derived-facts":
            retained = load_witness(plan.path, fallback_schema=WITNESS_SCHEMA)
            _assert_side_matches(case, str(retained["side"]))
            return kingbird_derived_witness(
                case.n,
                retained,
                source_n=plan.source_n,
                source_path=_relative(SOURCE_MANIFEST),
                source_url=plan.url,
            )
        source_text = plan.path.read_text(encoding="utf-8")
        source_path = _relative(plan.path)
        geometry = parse_unitsquare_svg(source_text, expected_n=case.n)
        _assert_side_matches(case, geometry.side)
        return unitsquare_witness(
            case.n,
            geometry,
            source_path=source_path,
            source_url=plan.url,
        )
    except (ValueError, TypeError) as error:
        raise ValueError(f"n={case.n} from {_relative(plan.path)}: {error}") from error


def _projection_text(value: object, digits: int = 70) -> str:
    return str(
        mp.nstr(
            value,
            digits,
            strip_zeros=True,
            min_fixed=-10_000,
            max_fixed=10_000,
        )
    )


def _scalar(value: str, *, rational: bool):
    return scalar_from_fraction(Fraction(value)) if rational else scalar_from_decimal(value)


def frame_from_witness(witness: dict) -> PackingFrame:
    rational = witness["scalar"]["kind"] == "rational"
    side = _scalar(str(witness["side"]), rational=rational)
    if witness["representation"] == "corners":
        source_squares = [
            [(str(x), str(y)) for x, y in square["corners"]] for square in witness["squares"]
        ]
    else:
        projected, _projected_side = materialize_witness(witness, digits=80)
        source_squares = [
            [(_projection_text(x), _projection_text(y)) for x, y in square]
            for square in projected
        ]
        rational = False
    squares = tuple(
        SquareGeometry(
            square_id=f"square-{index:03d}",
            corners=tuple(
                Point2(_scalar(x, rational=rational), _scalar(y, rational=rational))
                for x, y in corners
            ),
            label=str(index),
        )
        for index, corners in enumerate(source_squares, start=1)
    )
    claim = witness["claim"]
    # The tier states what this drawn packing establishes, which is exactly what
    # coordinate_provenance answers: exact coordinates make the frame a certified
    # upper bound, checked decimals make it numerically checked. Optimality is not
    # on this ladder and is not readable from a witness; a figure that wants to say
    # "proved" reads packing.status from frontier/n-NNN.md instead.
    if claim["coordinate_provenance"] == "verified":
        evidence = EvidenceTier.CERTIFIED_UPPER_BOUND
        check = CheckSummary(
            passed=True,
            kind=CheckKind.FORMAL,
            method=str(claim["method"]),
            detail=str(claim["limitations"]),
        )
    else:
        result = witness.get("certificate", {}).get("result", {})
        if not result.get("check_passed"):
            raise ValueError(f"{witness['id']}: numerical receipt is absent or failed")
        precision = claim["precision"]
        evidence = EvidenceTier.NUMERICALLY_CHECKED
        check = CheckSummary(
            passed=True,
            kind=CheckKind.NUMERICAL,
            method=str(claim["method"]),
            arithmetic="mpmath arbitrary precision",
            precision=f"{precision['decimal_digits']} decimal digits",
            rounding=str(precision["rounding"]),
            tolerance=str(claim["tolerance"]),
            detail=str(claim["limitations"]),
        )
    source = witness.get("source", {})
    return PackingFrame(
        container_side=side,
        squares=squares,
        evidence=evidence,
        check=check,
        label=f"n={witness['n']} known best",
        source_id=str(witness["id"]),
        source_url=str(source.get("url", "")),
    )


def _render(witness: dict) -> str:
    n = witness["n"]
    return render_packing_svg(
        frame_from_witness(witness),
        spec=RenderSpec(
            overlays=frozenset(),
            title=f"Known-best packing of {n} unit squares",
            description=(
                f"The retained known-best n={n} construction, normalized to Witness/v2 "
                "and rendered with the repository's deterministic house renderer."
            ),
        ),
    )


def _summary_points(
    square: SquareGeometry,
    *,
    container_side: Decimal,
    x: Decimal,
    y: Decimal,
    scale: Decimal,
) -> str:
    return " ".join(
        (
            f"{format_svg_number(x + point.x.projected * scale)},"
            f"{format_svg_number(y + (container_side - point.y.projected) * scale)}"
        )
        for point in square.corners
    )


def _append_summary_card(
    root: ET.Element, built: BuiltCase, *, spec: RenderSpec, canvas: CompositeCanvas
) -> None:
    n = built.frontier.n
    row, column = divmod(n - canvas.spec.first_n, canvas.spec.columns)
    card_x = SUMMARY_GRID_LEFT + SUMMARY_COLUMN_PITCH * column
    card_y = SUMMARY_GRID_TOP + SUMMARY_ROW_PITCH * row
    packing_x = card_x + SUMMARY_PACKING_INSET_X
    packing_y = card_y + SUMMARY_PACKING_INSET_Y
    frame = frame_from_witness(built.witness)
    side = frame.container_side.projected
    scale = SUMMARY_PACKING_SIZE / side
    colors = assign_square_colors(frame, spec)

    card = sub(
        root,
        "g",
        {
            "data-feature": "packing-card",
            "data-n": str(n),
            "data-row": str(row),
            "data-column": str(column),
            "data-source-id": frame.source_id,
        },
    )
    sub(
        card,
        "rect",
        {
            "data-feature": "container-outline",
            "x": format_svg_number(packing_x),
            "y": format_svg_number(packing_y),
            "width": format_svg_number(SUMMARY_PACKING_SIZE),
            "height": format_svg_number(SUMMARY_PACKING_SIZE),
            "fill": PAPER_THEME.background,
            # Stroke widths here are in user units and scale with the drawing, deliberately.
            # `vector-effect="non-scaling-stroke"` used to be set on both this outline and the
            # square fills below, and it was doing nothing useful and one bad thing. cairosvg
            # ignores the attribute outright -- measured at scale 1, 2 and 4, the rendered
            # stroke is identical with it and without -- so no PNG or PDF this repository
            # builds has ever been affected by it. Chromium does honour it, and resolves it
            # against the size the figure is displayed at rather than the size it was drawn at.
            # The explainer shows this 2400-unit figure in a column about 620px wide, so the
            # 1.15 stayed 1.15 device pixels instead of shrinking with everything around it:
            # the container box printed about 3.8 times heavier, relative to its own cell, than
            # the same file rendered standalone. One artifact, two line weights, depending on
            # who drew it.
            "stroke": PAPER_THEME.container,
            "stroke-width": "1.15",
        },
    )
    for square in frame.squares:
        color = colors[square.square_id]
        polygon = sub(
            card,
            "polygon",
            {
                "data-feature": "square-fill",
                "data-square": f"n-{n:03d}-{square.square_id}",
                "data-hue-index": str(color.hue_index),
                "data-shade-index": str(color.shade_index),
                "data-contact-sides": str(color.contact_sides),
                "data-orientation-radians": str(color.orientation_radians),
                "points": _summary_points(
                    square,
                    container_side=side,
                    x=packing_x,
                    y=packing_y,
                    scale=scale,
                ),
                "fill": color.fill,
                "stroke": PAPER_THEME.container,
                "stroke-width": "0.42",
                "stroke-linejoin": "round",
            },
        )
        if color.angle_class is not None:
            polygon.set("data-angle-class", str(color.angle_class))

    sub(
        card,
        "text",
        {
            "data-feature": "packing-label",
            "x": format_svg_number(packing_x),
            "y": format_svg_number(card_y + SUMMARY_LABEL_BASELINE),
            "font-family": SUMMARY_FONT,
            "font-size": "29",
            "font-weight": "700",
            "letter-spacing": "-0.5",
            "fill": PAPER_THEME.ink,
        },
    ).text = str(n)

    badges = _case_badges(built)
    left = packing_x
    right = packing_x + SUMMARY_PACKING_SIZE
    top_row = card_y + SUMMARY_LABEL_BASELINE
    bottom_row = card_y + SUMMARY_BOUND_BASELINE

    badge_top = top_row - Decimal(29) * SUMMARY_LABEL_CAP_RATIO
    cursor = right - SUMMARY_BADGE_SIZE
    for glyph, style, label in reversed(badges):
        _append_badge(card, glyph, style, label, x=cursor, top=badge_top)
        cursor -= SUMMARY_BADGE_SIZE + Decimal(4)
    bound = sub(
        card,
        "text",
        {
            "data-feature": "side-bound",
            "x": format_svg_number(left),
            "y": format_svg_number(bottom_row),
            "font-family": SUMMARY_FONT,
            "font-size": SUMMARY_SMALL_SIZE,
            "font-weight": SUMMARY_SMALL_WEIGHT,
            "fill": SUMMARY_SMALL_FILL,
        },
    )
    # Only the function name is italic, as in ordinary mathematical setting: the
    # parentheses, the argument, the relation and the numeral stay upright.
    _append_function_text(bound, _figure_entries()[n]["side"]["display"], SUMMARY_SMALL_SIZE)

    # The record carries a degree for all 95 known cases, but printing "deg 1"
    # on the 65 integer sides is noise: a whole number is self-evidently
    # rational. Show the degree only where it says something.
    degree = _figure_entries()[n]["exactness"]["degree"]
    if degree is not None and degree >= 2:
        sub(
            card,
            "text",
            {
                "data-feature": "algebraic-degree",
                "x": format_svg_number(right),
                "y": format_svg_number(bottom_row),
                "text-anchor": "end",
                "font-family": SUMMARY_FONT,
                "font-size": SUMMARY_SMALL_SIZE,
                "font-weight": SUMMARY_SMALL_WEIGHT,
                "fill": SUMMARY_SMALL_FILL,
            },
        ).text = f"deg {degree}"

    _append_lower_bound(card, n, left=left, baseline=card_y + SUMMARY_LOWER_BASELINE)


def _append_lower_bound(card: ET.Element, n: int, *, left: Decimal, baseline: Decimal) -> None:
    """The certified floor, under the best known side.

    A proved case says `s(n) = ...` on the line above and gets nothing here. Where the
    project proved the floor itself, the accent falls on the numeral alone, the same
    colour as the star in the badge row above it: what is new about the case is the
    bound, not the function it bounds, so the `s(n) >=` that introduces it stays in the
    caption colour it carries on every other card. The legend counts how many there are.
    """
    entry = _figure_entries()[n]["lower"]
    if not entry["shown"]:
        return
    lower = sub(
        card,
        "text",
        {
            "data-feature": "lower-bound",
            "x": format_svg_number(left),
            "y": format_svg_number(baseline),
            "font-family": SUMMARY_FONT,
            "font-size": SUMMARY_SMALL_SIZE,
            "font-weight": SUMMARY_SMALL_WEIGHT,
            "fill": SUMMARY_SMALL_FILL,
        },
    )
    _append_function_text(
        lower,
        entry["display"],
        SUMMARY_SMALL_SIZE,
        accent=FIRST_PARTY_ACCENT_COLOR if entry["first_proved_here"] else None,
    )


@cache
def _figure_entries() -> dict[int, dict]:
    """The figure record, keyed by n.

    Every claim the figure states is decided in
    devtools/build_composite_figure_data.py and validated against
    composite-figure.schema.yaml. Nothing is re-derived here, so the drawing and
    the record cannot disagree.
    """
    return {entry["n"]: entry for entry in load_figure_record()["entries"]}


def _case_badges(built: BuiltCase) -> tuple[tuple[str, str, str], ...]:
    """The card's icons, the new-result star first where the case carries one.

    The star reads as one of the badges rather than as punctuation on the bound line,
    so it sits with them; being first in the row puts it leftmost, since the row is
    laid out from the right.
    """
    entry = _figure_entries()[built.frontier.n]
    badges = [(badge["glyph"], badge["style"], badge["meaning"]) for badge in entry["badges"]]
    if entry["lower"]["first_proved_here"]:
        badges.insert(0, ("", "star", "lower bound first proved here"))
    return tuple(badges)


#: How far to push the text after an italic `s`, as a fraction of the font size. An
#: italic letter leans into whatever follows it, and `s(` sets the parenthesis against
#: the terminal of the s; a thin space is the typesetter's answer, expressed here as an
#: offset so it does not depend on a font carrying U+2009.
SUMMARY_ITALIC_KERN = Decimal("0.055")


def _append_function_text(
    parent: ET.Element, display: str, size: str, *, accent: str | None = None
) -> None:
    """Set `s(n) ...`: the function name italic, the rest upright, kerned apart.

    Only the function name is italic, as in ordinary mathematical setting: the
    parentheses, the argument, the relation and the numeral stay upright.

    `accent` colours the value alone -- the run after the last space -- and leaves the
    function, its argument and the relation in the parent's fill.

    The separating space stays in the text, at the end of the run before the value.
    Carrying it as a `dx` advance instead would draw the same picture and cost the
    space in everything that reads the text rather than the ink: selection, copy, and
    a screen reader. Measured on 2026-09-05 in both renderers this figure passes
    through, cairosvg and Chromium: against the unsplit line, the split places the
    value at the same x to within a hundredth of a unit and sets the same total width,
    so neither trims the space at the seam.
    """
    sub(parent, "tspan", {"font-style": "italic"}).text = display[0]
    kern = {"dx": format_svg_number(Decimal(size) * SUMMARY_ITALIC_KERN)}
    rest = display[1:]
    head, separator, value = rest.rpartition(" ")
    if accent is None or not separator:
        sub(parent, "tspan", kern).text = rest
        return
    sub(parent, "tspan", kern).text = head + separator
    sub(parent, "tspan", {"fill": accent}).text = value


def _star_center_y(baseline: Decimal, size: str) -> Decimal:
    """Half a cap height above the baseline: where a mark sits level with its text.

    Aligning by eye drifts as soon as a line changes size, so both the height and the
    scale come from the type. Helvetica's cap height is `SUMMARY_LABEL_CAP_RATIO` of the
    em, and a glyph reads as level with a line of capitals when its own centre is at
    half of that above the baseline.
    """
    return baseline - Decimal(size) * SUMMARY_LABEL_CAP_RATIO / 2


def _star_scale(size: str) -> Decimal:
    """How much to grow the star for type larger than the caption it was drawn for."""
    return Decimal(size) / SUMMARY_STAR_REFERENCE_SIZE


def _append_star(
    parent: ET.Element,
    *,
    center_x: Decimal,
    center_y: Decimal,
    feature: str,
    label: str = "",
    scale: Decimal = Decimal(1),
) -> None:
    """Draw the new-result star about a centre, in the figure's one accent colour."""
    attributes = {
        "data-feature": feature,
        "points": " ".join(
            f"{format_svg_number(center_x + dx * scale)},"
            f"{format_svg_number(center_y + dy * scale)}"
            for dx, dy in SUMMARY_STAR_POINTS
        ),
        "fill": FIRST_PARTY_ACCENT_COLOR,
    }
    if label:
        attributes["data-evidence"] = label
    sub(parent, "polygon", attributes)


def _badge_baseline(glyph: str) -> Decimal:
    """Where a badge's glyph sits, so every badge centres its mark the same way.

    A letter is centred on its cap height: the box is `SUMMARY_BADGE_SIZE` tall and the
    caps are `SUMMARY_LABEL_CAP_RATIO` of the font, so the baseline sits half a cap
    below the box's middle. Deriving it rather than tabulating it is what keeps `R`
    level with `O`; `R` used to fall through to the math baseline and rode high.
    """
    if not glyph.isalpha():
        return SUMMARY_MATH_GLYPH_BASELINE
    cap = SUMMARY_BADGE_FONT_SIZE * SUMMARY_LABEL_CAP_RATIO
    return (SUMMARY_BADGE_SIZE + cap) / 2


def _append_badge(
    parent: ET.Element, glyph: str, style: str, label: str, *, x: Decimal, top: Decimal
) -> None:
    """Draw one badge at an explicit box top.

    Callers position the box rather than passing a text baseline, so the card can
    sit its badges flush with the top of the big number.
    """
    if style == "star":
        # The legend's star is the same polygon the cards carry, centred in a badge box
        # so the row lays out as if it were one. `glyph` is unused: there is no star to
        # typeset, which is the point.
        _append_star(
            parent,
            center_x=x + SUMMARY_BADGE_SIZE / 2,
            center_y=top + SUMMARY_BADGE_SIZE / 2,
            feature="legend-star",
            label=label,
            scale=SUMMARY_BADGE_SIZE * SUMMARY_BADGE_STAR_SPAN / (SUMMARY_STAR_INSET * 2),
        )
        return
    fill, stroke, glyph_fill = {
        "solid": (PAPER_THEME.muted, "none", PAPER_THEME.background),
        "ink": ("none", PAPER_THEME.muted, PAPER_THEME.muted),
        "muted": ("none", PAPER_THEME.muted, PAPER_THEME.muted),
    }[style]
    sub(
        parent,
        "rect",
        {
            "data-feature": "evidence-badge",
            "data-evidence": label,
            "x": format_svg_number(x),
            "y": format_svg_number(top),
            "width": format_svg_number(SUMMARY_BADGE_SIZE),
            "height": format_svg_number(SUMMARY_BADGE_SIZE),
            "rx": "4.5",
            "fill": fill,
            "stroke": stroke,
            "stroke-width": "1.2",
        },
    )
    sub(
        parent,
        "text",
        {
            "x": format_svg_number(x + SUMMARY_BADGE_SIZE / 2),
            "y": format_svg_number(top + _badge_baseline(glyph)),
            "text-anchor": "middle",
            "font-family": SUMMARY_FONT,
            "font-size": format_svg_number(SUMMARY_BADGE_FONT_SIZE),
            "font-weight": "650",
            "fill": glyph_fill,
        },
    ).text = glyph


def _legend_row(
    legend: ET.Element,
    entries: list[tuple[object, str]],
    *,
    baseline: Decimal,
    canvas_width: int,
) -> None:
    """Lay one centerd legend row, centered on a canvas this wide.

    Each entry is (mark, label), where mark is either a badge triple or a run of
    swatches. Widths are estimated from the label length because the renderer
    holds no font metrics, so widths come from the Helvetica advance table.
    """
    top = baseline - SUMMARY_BADGE_SIZE + Decimal(4)

    def mark_width(mark: object) -> Decimal:
        if isinstance(mark, tuple):
            return SUMMARY_BADGE_SIZE
        return SUMMARY_BADGE_SIZE * Decimal(len(mark))  # pyright: ignore[reportArgumentType]

    gap = Decimal(34)
    widths = [
        mark_width(mark) + Decimal(8) + _text_width(label, SUMMARY_FOOTER_SIZE)
        for mark, label in entries
    ]
    cursor = (
        Decimal(canvas_width) - sum(widths, Decimal(0)) - gap * Decimal(len(entries) - 1)
    ) / 2
    for (mark, label), width in zip(entries, widths, strict=True):
        if isinstance(mark, tuple):
            glyph, style, name = mark
            _append_badge(legend, glyph, style, name, x=cursor, top=top)
            run_end = cursor + SUMMARY_BADGE_SIZE
        else:
            run_end = cursor
            for fill, numeral in mark:  # pyright: ignore[reportGeneralTypeIssues]
                sub(
                    legend,
                    "rect",
                    {
                        "data-feature": "legend-swatch",
                        "x": format_svg_number(run_end),
                        "y": format_svg_number(top),
                        "width": format_svg_number(SUMMARY_BADGE_SIZE),
                        "height": format_svg_number(SUMMARY_BADGE_SIZE),
                        "fill": fill,
                        "stroke": PAPER_THEME.container,
                        "stroke-width": "0.8",
                    },
                )
                if numeral:
                    sub(
                        legend,
                        "text",
                        {
                            "x": format_svg_number(run_end + SUMMARY_BADGE_SIZE / 2),
                            "y": format_svg_number(top + Decimal("13.4")),
                            "text-anchor": "middle",
                            "font-family": SUMMARY_FONT,
                            "font-size": "11.5",
                            "font-weight": "650",
                            "fill": PAPER_THEME.background
                            if hex_oklch(fill)[0] < 0.62
                            else PAPER_THEME.ink,
                        },
                    ).text = numeral
                run_end += SUMMARY_BADGE_SIZE
        sub(
            legend,
            "text",
            {
                "x": format_svg_number(run_end + Decimal(8)),
                "y": format_svg_number(baseline),
                "font-family": SUMMARY_FONT,
                "font-size": SUMMARY_FOOTER_SIZE,
                "font-weight": SUMMARY_FOOTER_WEIGHT,
                "fill": SUMMARY_SMALL_FILL,
            },
        ).text = label
        cursor += width + gap


def _append_summary_legend(
    root: ET.Element, *, spec: RenderSpec, canvas: CompositeCanvas
) -> None:
    """Two rows: what the badges assert, then what color and shade encode."""
    totals = load_figure_record()["totals"]
    tally = {
        "lower bound first proved here": totals["lower_bound_first_proved_here"],
        "proved optimal": totals["proved_optimal"],
        "exact value known": totals["exact_value_known"],
        "only known numerically": totals["only_known_numerically"],
        "rigid (established here)": totals["rigidity_established"],
        "annotated rigid by the catalogue": totals["rigidity_catalogue_annotated"],
    }
    palette = square_fill_palette(
        hue_count=spec.hue_count,
        shades_per_hue=spec.shades_per_hue,
        lightness_span=spec.shade_lightness_span,
    )
    middle = spec.shades_per_hue // 2
    legend = sub(root, "g", {"data-feature": "evidence-legend"})
    badges = [
        ("O", "solid", "proved optimal"),
        ("=", "solid", "exact value known"),
        ("\u2248", "muted", "only known numerically"),
        ("R", "solid", "rigid (established here)"),
        # The muted twin is the point of D-385: one glyph used to cover both, so a
        # source's annotation was rendered indistinguishable from an argument of ours.
        ("R", "muted", "annotated rigid by the catalogue"),
        ("", "star", "lower bound first proved here"),
    ]
    _legend_row(
        legend,
        [(badge, f"{badge[2]} ({tally.get(badge[2], 0)})") for badge in badges],
        baseline=canvas.legend_baseline,
        canvas_width=canvas.width,
    )
    # Color carries the tilt angle, shade the contact count. Four hues stand in
    # for the twenty; the citron ramp illustrates the shades because that family
    # shows every contact count in the atlas.
    hue_run = [(palette[index][middle], "") for index in range(4)]
    shade_run = [
        (fill, str(spec.shades_per_hue - 1 - index)) for index, fill in enumerate(palette[1])
    ]
    _legend_row(
        legend,
        [
            (hue_run, "colors indicate distinct tilt angles"),
            (shade_run, "shade indicates number of full-side contacts"),
        ],
        baseline=canvas.legend_baseline + SUMMARY_LEGEND_ROW_PITCH,
        canvas_width=canvas.width,
    )


@emission_precision()
def render_known_best_summary_svg(built: list[BuiltCase], canvas: CompositeCanvas) -> str:
    """Render a complete, zoomable overview of one composite's range of cases.

    The pin covers the per-card scale and corner arithmetic in `_append_summary_card`
    and `_summary_points`, which is its own Decimal work rather than the house
    renderer's, and so would otherwise track whatever precision the process was left in.
    """
    composite = canvas.spec
    numbers = [item.frontier.n for item in built]
    if numbers != list(composite.numbers):
        raise ValueError(
            f"the {composite.stem} composite requires exactly "
            f"{composite.cases.label} in order"
        )
    accessible_title, accessible_description = SUMMARY_PROSE[composite.stem]
    width, height = canvas.width, canvas.height
    spec = RenderSpec(overlays=frozenset())
    root = element(
        "svg",
        {
            "width": str(width),
            "height": str(height),
            "viewBox": f"0 0 {width} {height}",
            "role": "img",
            "aria-labelledby": "figure-title figure-description",
        },
    )
    append_title_desc(root, accessible_title, accessible_description)
    append_metadata(
        root,
        {
            "angle-class-contract": ANGLE_CLASS_CONTRACT,
            "color-angle-tolerance-radians": str(spec.angle_tolerance_radians),
            "color-full-side-contact-tolerance": str(spec.full_side_contact_tolerance),
            "color-hue-count": str(spec.hue_count),
            "color-hue-scheme": spec.hue_scheme.value,
            "color-shade-lightness-span": str(spec.shade_lightness_span),
            "color-shade-scheme": spec.shade_scheme.value,
            "color-shades-per-hue": str(spec.shades_per_hue),
            "columns": str(composite.columns),
            "first-n": str(composite.first_n),
            "generated-by": GENERATOR,
            "last-n": str(composite.last_n),
            "rows": str(composite.rows),
            "square-count": str(composite.square_count),
        },
    )
    sub(
        root,
        "rect",
        {
            "width": str(width),
            "height": str(height),
            "fill": PAPER_THEME.background,
        },
    )
    heading_x = str(width // 2)
    sub(
        root,
        "text",
        {
            "x": heading_x,
            "y": "76",
            "text-anchor": "middle",
            "font-family": SUMMARY_FONT,
            "font-size": "48",
            "font-weight": "700",
            "letter-spacing": "1.5",
            "fill": PAPER_THEME.ink,
        },
    ).text = f"{composite.count} BEST KNOWN SQUARE PACKINGS"
    release_width = _text_width(SUMMARY_RELEASE_TEXT, SUMMARY_RELEASE_SIZE)
    release_scale = _star_scale(SUMMARY_RELEASE_SIZE)
    star_span = SUMMARY_STAR_INSET * 2 * release_scale
    group_width = star_span + SUMMARY_RELEASE_GAP + release_width
    group_left = (Decimal(width) - group_width) / 2
    _append_star(
        root,
        center_x=group_left + star_span / 2,
        center_y=_star_center_y(SUMMARY_RELEASE_BASELINE, SUMMARY_RELEASE_SIZE),
        feature="release-star",
        scale=release_scale,
    )
    sub(
        root,
        "text",
        {
            "data-feature": "release",
            "x": format_svg_number(group_left + star_span + SUMMARY_RELEASE_GAP),
            "y": format_svg_number(SUMMARY_RELEASE_BASELINE),
            "font-family": SUMMARY_FONT,
            "font-size": SUMMARY_RELEASE_SIZE,
            "font-weight": "700",
            "fill": PAPER_THEME.ink,
        },
    ).text = SUMMARY_RELEASE_TEXT
    sub(
        root,
        "text",
        {
            "data-feature": "repository",
            "x": heading_x,
            "y": format_svg_number(SUMMARY_SUBTITLE_BASELINE),
            "text-anchor": "middle",
            "font-family": SUMMARY_FONT,
            "font-size": SUMMARY_REPOSITORY_SIZE,
            "font-weight": "700",
            # Where the figure came from reads as part of the title, not as a caption.
            "fill": PAPER_THEME.ink,
        },
    ).text = SUMMARY_REPOSITORY
    _append_summary_legend(root, spec=spec, canvas=canvas)
    kern_width = Decimal(SUMMARY_FOOTER_SIZE) * SUMMARY_ITALIC_KERN
    kern = format_svg_number(kern_width)
    line_width = sum(
        (_text_width(text, SUMMARY_FOOTER_SIZE) for text, _italic in SUMMARY_EXPLAINER_RUNS),
        Decimal(0),
    ) + kern_width * Decimal(
        sum(
            1
            for index, (_text, italic) in enumerate(SUMMARY_EXPLAINER_RUNS)
            if index and not italic and SUMMARY_EXPLAINER_RUNS[index - 1][1]
        )
    )
    explainer = sub(
        root,
        "text",
        {
            "data-feature": "explainer",
            # Anchored from the left rather than centred: a centred run made of several
            # tspans is not laid out as one chunk by every renderer, and the parts stack
            # on the same centre. Measuring the line and starting it is unambiguous.
            "x": format_svg_number((Decimal(width) - line_width) / 2),
            "y": format_svg_number(canvas.explainer_baseline),
            "font-family": SUMMARY_FONT,
            "font-size": SUMMARY_FOOTER_SIZE,
            "font-weight": SUMMARY_SMALL_WEIGHT,
            "fill": SUMMARY_SMALL_FILL,
        },
    )
    previous_italic = False
    for text, italic in SUMMARY_EXPLAINER_RUNS:
        attributes: dict[str, str] = {"font-style": "italic"} if italic else {}
        # An upright run following an italic one needs the same thin space the cards use.
        if previous_italic and not italic:
            attributes["dx"] = kern
        sub(explainer, "tspan", attributes).text = text
        previous_italic = italic
    sub(
        root,
        "text",
        {
            "data-feature": "credit",
            "x": heading_x,
            "y": format_svg_number(canvas.credit_baseline),
            "text-anchor": "middle",
            "font-family": SUMMARY_FONT,
            "font-size": SUMMARY_FOOTER_SIZE,
            "font-weight": SUMMARY_SMALL_WEIGHT,
            "fill": SUMMARY_SMALL_FILL,
        },
    ).text = SUMMARY_CREDIT
    sub(
        root,
        "text",
        {
            "data-feature": "release-stamp",
            "x": heading_x,
            "y": format_svg_number(canvas.stamp_baseline),
            "text-anchor": "middle",
            "font-family": SUMMARY_FONT,
            "font-size": SUMMARY_FOOTER_SIZE,
            "font-weight": SUMMARY_SMALL_WEIGHT,
            "fill": SUMMARY_SMALL_FILL,
        },
    ).text = SUMMARY_RELEASE_STAMP
    for item in built:
        _append_summary_card(root, item, spec=spec, canvas=canvas)
    return serialize_svg(root)


def _png_chunks(content: bytes) -> list[tuple[bytes, bytes]]:
    if not content.startswith(PNG_SIGNATURE):
        raise ValueError("known-best composite preview is not a PNG")
    chunks: list[tuple[bytes, bytes]] = []
    offset = len(PNG_SIGNATURE)
    while offset < len(content):
        if offset + 12 > len(content):
            raise ValueError("known-best composite PNG has a truncated chunk")
        length = int.from_bytes(content[offset : offset + 4], "big")
        chunk_type = content[offset + 4 : offset + 8]
        end = offset + 12 + length
        if end > len(content):
            raise ValueError("known-best composite PNG has a truncated payload")
        payload = content[offset + 8 : offset + 8 + length]
        expected_crc = int.from_bytes(content[offset + 8 + length : end], "big")
        actual_crc = zlib.crc32(chunk_type + payload) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise ValueError("known-best composite PNG has a corrupt chunk")
        chunks.append((chunk_type, payload))
        offset = end
        if chunk_type == b"IEND":
            break
    if not chunks or chunks[-1][0] != b"IEND" or offset != len(content):
        raise ValueError("known-best composite PNG has an invalid ending")
    return chunks


def _png_chunk(chunk_type: bytes, payload: bytes) -> bytes:
    return (
        struct.pack(">I", len(payload))
        + chunk_type
        + payload
        + struct.pack(">I", zlib.crc32(chunk_type + payload) & 0xFFFFFFFF)
    )


def _png_with_summary_source(content: bytes, svg_sha256: str) -> bytes:
    chunks = [
        (chunk_type, payload)
        for chunk_type, payload in _png_chunks(content)
        if not (chunk_type == b"tEXt" and payload.partition(b"\0")[0] == PNG_SOURCE_KEY)
    ]
    tagged: list[tuple[bytes, bytes]] = []
    for chunk_type, payload in chunks:
        tagged.append((chunk_type, payload))
        if chunk_type == b"IHDR":
            tagged.append((b"tEXt", PNG_SOURCE_KEY + b"\0" + svg_sha256.encode("ascii")))
    return PNG_SIGNATURE + b"".join(
        _png_chunk(chunk_type, payload) for chunk_type, payload in tagged
    )


def png_summary_receipt(content: bytes) -> tuple[int, int, str | None]:
    chunks = _png_chunks(content)
    ihdr = next((payload for chunk_type, payload in chunks if chunk_type == b"IHDR"), None)
    if ihdr is None or len(ihdr) != 13:
        raise ValueError("known-best composite PNG has no valid IHDR")
    width, height = struct.unpack(">II", ihdr[:8])
    source_sha256 = next(
        (
            payload.partition(b"\0")[2].decode("ascii")
            for chunk_type, payload in chunks
            if chunk_type == b"tEXt" and payload.partition(b"\0")[0] == PNG_SOURCE_KEY
        ),
        None,
    )
    return width, height, source_sha256


def _png_matches_summary(export: RasterExport, svg_text: str) -> bool:
    if not export.path.is_file():
        return False
    try:
        width, height, source_sha256 = png_summary_receipt(export.path.read_bytes())
    except UnicodeDecodeError, ValueError:
        return False
    expected_sha256 = hashlib.sha256(svg_text.encode("utf-8")).hexdigest()
    return (width, height, source_sha256) == (
        export.width,
        export.height,
        expected_sha256,
    )


def _cropped_svg(svg_text: str, export: RasterExport) -> str:
    """The SVG an export is drawn from: the drawing itself, or a shortened viewport.

    An SVG viewport clips, so narrowing `viewBox` and `height` on the root is the whole
    crop: the rasteriser draws the band and never draws what falls outside it. Only the
    root is touched, and only for an export that asks, so the receipt stamped into every
    raster still names the sha256 of the one drawing all three come from.
    """
    if export.crop_units is None:
        return svg_text
    root = ET.fromstring(svg_text)
    root.set("height", str(export.crop_units))
    root.set("viewBox", f"0 0 {export.canvas_width} {export.crop_units}")
    return ET.tostring(root, encoding="unicode")


def _update_png_export(export: RasterExport, svg_text: str) -> None:
    """Draw one raster from the SVG, with the same rasteriser that draws the PDF.

    ImageMagick used to draw the preview, and its own SVG renderer restarts each
    `tspan` at its parent's `x`, which set the italic `s` on top of the `(` in every
    bound line. The SVG and the PDF were always right; only the preview carried it.
    cairosvg is a declared dependency and already draws the PDF in this same command,
    so every raster of one drawing now agrees, and no external tool has to be
    installed.

    The size guard is what stops a resized canvas from leaving a stale export behind:
    the receipt names the canvas, so a raster drawn at another size is refused rather
    than written.
    """
    if _png_matches_summary(export, svg_text):
        return
    # SVG construction and receipt checks do not need the native Cairo library.
    import cairosvg  # noqa: PLC0415

    content = cairosvg.svg2png(
        bytestring=_cropped_svg(svg_text, export).encode("utf-8"),
        output_width=export.width,
        output_height=export.height,
        background_color="white",
    )
    if not isinstance(content, bytes):  # pragma: no cover - cairosvg returns bytes here
        raise TypeError("cairosvg returned no PNG bytes")
    stamped = _png_with_summary_source(
        content, hashlib.sha256(svg_text.encode("utf-8")).hexdigest()
    )
    width, height, _source_sha256 = png_summary_receipt(stamped)
    if (width, height) != (export.width, export.height):
        raise ValueError(
            f"PNG {export.role} dimensions are {width}x{height}; expected "
            f"{export.width}x{export.height}"
        )
    with atomic_output_file(export.path, make_parents=True) as temporary:
        temporary.write_bytes(stamped)


def _update_png_exports(canvas: CompositeCanvas, svg_text: str) -> None:
    """Redraw every raster of one composite from the SVG this run produced."""
    for export in canvas.rasters:
        _update_png_export(export, svg_text)


def _composite_pdf_problems(canvas: CompositeCanvas, svg_text: str) -> list[str]:
    """Report one composite's PDF export against the SVG this build produced.

    The PDF is written by `render_composite_pdf`, which owns the page geometry and
    keeps its own `--check`. This reads the receipt that module writes so the atlas
    check reports the whole family, rather than passing three of four exports and
    leaving the reader to run a second command to learn about the fourth.
    """
    pdf = render_composite_pdf.composite_pdf(canvas.spec.stem)
    name = f"atlas/known-best/{pdf.name}"
    if not pdf.is_file():
        return [f"missing {name}"]
    try:
        recorded = render_composite_pdf.pdf_receipt(pdf.read_bytes())
    except ValueError:
        return [f"{name} is not a readable PDF"]
    if recorded != hashlib.sha256(svg_text.encode("utf-8")).hexdigest():
        return [f"missing or stale {name} export receipt"]
    return []


@cache
def _build_case(n: int, plan: SourcePlan) -> BuiltCase:
    case = _frontier_case(n)
    witness = _build_witness(case, plan)
    problems = check_witness_semantics(witness)
    if problems:
        raise ValueError(f"{witness['id']}: {problems[0]}")
    witness_text = witness_document(witness, schema="../witness.schema.yaml")
    return BuiltCase(case, plan, witness, witness_text, _render(witness))


def _frontier_with_witness(case: FrontierCase, witness_id: str) -> str:
    prefix, frontmatter, body = case.text.split("---\n", 2)
    del prefix
    lines = frontmatter.splitlines()
    start = next(
        (index for index, line in enumerate(lines) if line.startswith("    witnesses:")), None
    )
    if start is None:
        raise ValueError(f"{case.path.name}: reported upper bound has no witnesses field")
    end = start + 1
    while end < len(lines) and not lines[end].startswith("    evidence:"):
        end += 1
    existing = safe_load("\n".join(lines[start:end]))["witnesses"] or []
    if not isinstance(existing, list) or not all(isinstance(item, str) for item in existing):
        raise ValueError(f"{case.path.name}: witnesses must be a list of identifiers")
    witnesses = [*existing]
    if witness_id not in witnesses:
        witnesses.append(witness_id)
    lines[start:end] = ["    witnesses:", *(f"    - {item}" for item in witnesses)]
    return "---\n" + "\n".join(lines) + "\n---\n" + body


def _manifest_entry(built: BuiltCase) -> dict:
    n = built.frontier.n
    plan = built.source
    if plan.kind == "exact-grid":
        derivation = "canonical row-major subset of an exact integer grid"
    elif plan.kind == "kingbird-derived-facts":
        derivation = "deterministic reuse of retained Witness/v2 numerical center/angle facts"
    elif n == plan.source_n:
        derivation = "direct normalization of complete source geometry"
    else:
        derivation = (
            f"documented subpacking of n={plan.source_n}; retained the first {n} "
            "source-order squares"
        )
    claim = built.witness["claim"]
    source = {
        "kind": plan.kind,
        "path": _relative(
            SOURCE_MANIFEST if plan.kind == "kingbird-derived-facts" else plan.path
        ),
        "source_n": plan.source_n,
        "listed_n": list(plan.listed_n),
        "derivation": derivation,
    }
    if plan.url:
        source["url"] = plan.url
    return {
        "n": n,
        "frontier_path": _relative(built.frontier.path),
        "reported_side": built.frontier.side,
        "source": source,
        "witness": {
            "id": built.witness["id"],
            "path": f"witnesses/known-best/n-{n:03d}.yaml",
            "coordinate_provenance": claim["coordinate_provenance"],
            "method": claim["method"],
            **({"tolerance": claim["tolerance"]} if "tolerance" in claim else {}),
        },
        "rendering": {
            "path": f"atlas/known-best/rendering/n-{n:03d}.svg",
            "renderer": "sqpack deterministic house renderer",
        },
        "chunk_annotation": {
            "status": "calibration",
            "path": "atlas/known-best/chunk-partitions.json",
            "note": (
                "Derived bounded lattice-partition calibration; no H-044 verdict. "
                "Recompute after the complete grammar and prospective split are frozen."
            ),
        },
    }


def expected_outputs() -> tuple[dict[Path, str], dict]:
    """Every derived artifact, and the manifest describing them.

    Callers get copies so the memo cannot be mutated underneath them.
    """
    outputs, manifest = _expected_outputs()
    return dict(outputs), copy.deepcopy(manifest)


def range_record(cases: CorpusRange) -> dict:
    """A closed range, as the records state it.

    `count` is written out rather than left to the reader because it is what a consumer
    checks against the number of entries; it is derived here, so the two cannot drift.
    """
    return {"first_n": cases.first_n, "last_n": cases.last_n, "count": cases.count}


def _raster_record(export: RasterExport, derived_from: str) -> dict:
    record = {
        "derived_from": derived_from,
        "height": export.height,
        "path": export.name,
        "scale": export.scale,
        "width": export.width,
    }
    if export.crop_units is not None:
        record["top_crop"] = True
    return record


def _composite_record(canvas: CompositeCanvas) -> dict:
    """One composite, as the manifest describes it.

    Every number here is computed from the specification, so the record cannot claim a
    canvas or an export size the drawing does not have.
    """
    composite = canvas.spec
    svg_path = f"atlas/known-best/{composite.svg_name}"
    record = {
        "stem": composite.stem,
        "range": range_record(composite.cases),
        "columns": composite.columns,
        "rows": composite.rows,
        "layout": composite.layout,
        "renderer": "sqpack deterministic composite renderer",
        "square_count": composite.square_count,
        "svg": {
            "height": canvas.height,
            "path": svg_path,
            "width": canvas.width,
        },
    }
    for export in canvas.rasters:
        record[export.manifest_key] = _raster_record(export, svg_path)
    return record


@cache
def _expected_outputs() -> tuple[dict[Path, str], dict]:
    plans = source_plans()
    source_index = _source_index(plans)
    built = [_build_case(n, plans[n]) for n in CORPUS.numbers]
    outputs: dict[Path, str] = {SOURCE_MANIFEST: _json_text(source_index)}
    for item in built:
        n = item.frontier.n
        outputs[WITNESS_ROOT / f"n-{n:03d}.yaml"] = item.witness_text
        outputs[RENDER_ROOT / f"n-{n:03d}.svg"] = item.rendering_text
        outputs[item.frontier.path] = _frontier_with_witness(
            item.frontier, str(item.witness["id"])
        )
    for canvas in COMPOSITES:
        cards = [item for item in built if item.frontier.n in canvas.spec.numbers]
        outputs[canvas.svg_path] = render_known_best_summary_svg(cards, canvas)
    manifest = {
        "softschema": {
            "contract": "packing.squares:KnownBestAtlas/v1",
            "schema": "known-best-atlas.schema.yaml",
            "envelope": "atlas",
            "status": "enforced",
        },
        "atlas": {
            "range": range_record(CORPUS),
            "generated_by": GENERATOR,
            "policy": {
                "source_layer": (
                    "exact canonical grids, retained Kingbird derived numerical facts, "
                    "or immutable UnitSquare renderings"
                ),
                "witness_layer": "lossless where possible; limitations explicit otherwise",
                "rendering_layer": "repository deterministic house renderer",
                "annotation_layer": "derived and excluded from grammar validation until frozen",
            },
            # A list rather than a single record: the corpus publishes one composite
            # today and the geometry of a second is a second specification, so the shape
            # that describes them does not change when one is added.
            "composites": [_composite_record(canvas) for canvas in COMPOSITES],
            "entries": [_manifest_entry(item) for item in built],
        },
    }
    outputs[MANIFEST] = _json_text(manifest)
    return outputs, manifest


def update() -> None:
    # The figure record decides every claim the drawing states, so refresh it
    # first and drop the memo, or the render would use a stale one.
    build_composite_figure_data.update()
    _figure_entries.cache_clear()
    clear_build_caches()
    outputs, _manifest = expected_outputs()
    for path, content in sorted(outputs.items(), key=lambda item: item[0].as_posix()):
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.is_file() and path.read_text(encoding="utf-8") == content:
            continue
        with atomic_output_file(path) as temporary:
            temporary.write_text(content, encoding="utf-8")
    # Each composite ships as one family drawn from one SVG in one run: the vector
    # itself, every PNG raster, and the PDF. Splitting the exports across commands
    # is what would let four of the five be current and the fifth be last week's.
    rasters = 0
    for canvas in COMPOSITES:
        _update_png_exports(canvas, outputs[canvas.svg_path])
        render_composite_pdf.update(canvas.spec.stem)
        rasters += len(canvas.rasters)
    print(
        f"known-best atlas updated: {CORPUS.count} witnesses, {CORPUS.count} house "
        f"renderings, {len(COMPOSITES)} composite{_plural(len(COMPOSITES))} "
        f"(SVG, {rasters} PNG rasters, PDF), {CORPUS.count} frontier links"
    )


def check() -> None:
    outputs, manifest = expected_outputs()
    problems = []
    for path, expected in sorted(outputs.items(), key=lambda item: item[0].as_posix()):
        if not path.is_file():
            problems.append(f"missing {_relative(path)}")
        elif path.read_text(encoding="utf-8") != expected:
            problems.append(f"stale {_relative(path)}")
    expected_witnesses = {f"n-{n:03d}.yaml" for n in CORPUS.numbers}
    expected_renderings = {f"n-{n:03d}.svg" for n in CORPUS.numbers}
    if WITNESS_ROOT.is_dir():
        unexpected = {path.name for path in WITNESS_ROOT.glob("*.yaml")} - expected_witnesses
        problems.extend(
            f"unexpected witnesses/known-best/{name}" for name in sorted(unexpected)
        )
    if RENDER_ROOT.is_dir():
        unexpected = {path.name for path in RENDER_ROOT.glob("*.svg")} - expected_renderings
        problems.extend(
            f"unexpected atlas/known-best/rendering/{name}" for name in sorted(unexpected)
        )
    if KINGBIRD_RAW_ROOT.exists():
        problems.append("raw Kingbird source directory must not be retained")
    # One --check covers every composite family, not just the vectors: the rasters and
    # the PDF are exports of one SVG each, and each carries a receipt naming the SVG it
    # was drawn from. Reading four receipts costs nothing next to redrawing a
    # 25-by-30-inch page, and a report that lists every stale export at once beats
    # finding them one command at a time.
    for canvas in COMPOSITES:
        svg_text = outputs[canvas.svg_path]
        problems.extend(
            f"missing or stale {export.name} {export.role} receipt"
            for export in canvas.rasters
            if not _png_matches_summary(export, svg_text)
        )
        problems.extend(_composite_pdf_problems(canvas, svg_text))
    atlas = manifest["atlas"]
    # The count the schema no longer pins as a constant is pinned here instead, against
    # the range the same record states: a case that went missing between the frontier
    # and the manifest cannot leave both halves agreeing.
    stated = atlas["range"]
    if stated != range_record(CORPUS) or stated["count"] != (
        stated["last_n"] - stated["first_n"] + 1
    ):
        problems.append(f"manifest range is not a consistent {CORPUS.label}")
    entries = atlas["entries"]
    if [entry["n"] for entry in entries] != list(CORPUS.numbers):
        problems.append(f"manifest entries are not exactly {CORPUS.label}")
    if problems:
        raise ValueError("known-best atlas drift:\n  " + "\n  ".join(problems[:20]))
    print(
        f"known-best atlas check passed: {CORPUS.count} sources/plans, witnesses, "
        f"renders, {len(COMPOSITES)} composite{_plural(len(COMPOSITES))}, and links"
    )


def smoke_in_temporary_directory() -> None:
    """Exercise generation without retaining outputs; useful while diagnosing a source."""
    with TemporaryDirectory() as directory:
        destination = Path(directory)
        outputs, _manifest = expected_outputs()
        for path, content in outputs.items():
            if path in {MANIFEST, SOURCE_MANIFEST} or path.is_relative_to(WITNESS_ROOT):
                relative = path.relative_to(ROOT)
                target = destination / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
        print(f"temporary corpus generation passed at {destination}")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--fetch", action="store_true", help="acquire missing retained upstream assets"
    )
    mode.add_argument("--update", action="store_true", help="regenerate all retained outputs")
    mode.add_argument(
        "--check", action="store_true", help="compare retained outputs to a rebuild"
    )
    mode.add_argument(
        "--smoke", action="store_true", help="build corpus into a temporary directory"
    )
    command.add_argument(
        "--refresh",
        action="store_true",
        help="with --fetch, replace already retained assets from their recorded URLs",
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.refresh and not args.fetch:
        raise SystemExit("--refresh requires --fetch")
    if args.fetch:
        fetch_sources(refresh=args.refresh)
    elif args.update:
        update()
    elif args.check:
        check()
    else:
        smoke_in_temporary_directory()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
