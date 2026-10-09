#!/usr/bin/env python3
"""Acquire, normalize, validate, and render the known-best atlas and its composites.

Usage:
    uv run --frozen python -m devtools.build_known_best_atlas --update
    uv run --frozen python -m devtools.build_known_best_atlas --update-composite-records
    uv run --frozen python -m devtools.build_known_best_atlas --update-composites
    uv run --frozen python -m devtools.build_known_best_atlas --check
    uv run --frozen python -m devtools.build_known_best_atlas --check --jobs 4
    uv run --frozen python -m devtools.build_known_best_atlas --check --sample
    uv run --frozen python -m devtools.build_known_best_atlas --check-composites

Two layers, updated apart. `--update` rewrites the data: the witnesses, the house
renderings, the manifest and the frontier links, all text. `--update-composites` redraws
the two posters and their PNG and PDF exports from the retained witnesses, and is run at
a version bump or on demand, never because the data moved: a poster states the data
commit it was drawn from (`CompositeIdentity`) and may trail the pin until the next
version (`sqpack.release`, rules 4 and 5). `--check-composites` holds the retained
posters to that record without rebuilding anything. A layout change first uses
`--update-composite-records` to refresh only the composite geometry in the manifest and
figure record, refusing changed case facts; commit and re-pin those records before
redrawing the posters.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import struct
import subprocess
import time
import urllib.error
import urllib.request
import zlib
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace
from datetime import date
from decimal import ROUND_HALF_EVEN, Decimal
from fractions import Fraction
from functools import cache
from itertools import combinations, pairwise
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Literal
from xml.etree import ElementTree as ET

import mpmath as mp
from strif import atomic_output_file

from devtools import build_bound_citations, build_composite_figure_data, render_composite_pdf
from devtools import evand_arrangement_houses as evand_houses
from devtools import evand_arrangement_reports as evand_reports
from devtools import evand_exact_certificates as evand_certificates
from devtools import refinement_house_links as refinement_houses
from devtools import refinement_packets as refinements
from devtools import squish_followup_packets as squish_followup
from devtools import squish_second_update_house_links as squish_house
from devtools import squish_second_update_packets as squish_second
from devtools import squish_upper_bound_packets as squish_packets
from devtools import upper_bound_packets as packets
from devtools.atlas_legend import AtlasLegendCounts, LegendItem, atlas_legend, recent_label
from devtools.atlas_orientation import orient_atlas_witness
from devtools.build_composite_figure_data import load_record as load_figure_record
from devtools.result_status import RecentContributions, recent_contributions_by_case
from sqpack import retained_json
from sqpack.known_best import (
    ATLAS_SAMPLE_STRIDE,
    KINGBIRD_ATTRIBUTION,
    KINGBIRD_BASE_URL,
    KINGBIRD_LICENSE_STATUS,
    KINGBIRD_RETENTION_POLICY,
    KNOWN_BEST_COMPOSITES,
    KNOWN_BEST_CORPUS,
    RETRIEVED_DATE,
    UNITSQUARE_BASE_URL,
    CompositePlacement,
    CompositeSpec,
    CorpusRange,
    GridTransition,
    PackingSegment,
    catalogue_source_map,
    display_bound_value,
    exact_grid_witness,
    grid_transitions,
    kingbird_derived_witness,
    packet_derived_witness,
    parse_unitsquare_svg,
    rational_integer,
    sampled_numbers,
    unitsquare_witness,
)
from sqpack.release import (
    COMPOSITES_MAY_TRAIL,
    DATA_REVISION,
    PUBLICATION_VERSION,
    commit_date,
    data_pathspec,
    data_revision,
    edition_at,
)
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
    SVG_EMISSION_PRECISION,
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
    svg_tag,
)
from sqpack.witness import (
    check_witness_semantics,
    exact_verify,
    load_witness,
    materialize_witness,
    witness_document,
)
from sqpack.workers import worker_count
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY_ROOT = ROOT.parent
FRONTIER = ROOT / "frontier"
CATALOGUE = ROOT / "resources/web/kingbird-squares-in-squares.html"
SOURCE_ROOT = ROOT / "resources/web/known-best-packings"
UNITSQUARE_ROOT = SOURCE_ROOT / "unitsquare"
#: The other place a retained UnitSquare rendering lives. The prospective collection
#: retained `n = 103, 105, 110, 131` when it audited `101..324`, and those bytes are not
#: moved into the known-best collection as the corpus widens: they are the same
#: upstream files under the same digest declaration, and moving them would break the
#: prospective builder that also reads them. Which root holds a case is therefore a
#: fact about where it was retained, not about which range it falls in.
PROSPECTIVE_UNITSQUARE_ROOT = ROOT / "resources/web/prospective-packings/unitsquare"
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
#: How a frontier record names the UnitSquare release in `reported_upper_bound`. The
#: record is what selects the source layer, so a case moves onto a UnitSquare rendering
#: by having its bound sourced there, never by being listed in a set of case numbers.
UNITSQUARE_SOURCE_KEY = "[UnitSquare 2026]"
#: The source packets that keep derived facts for a case in place of upstream bytes, by
#: the source key a record's reported upper bound names: a case moves onto a packet's
#: facts, as onto a UnitSquare rendering, by having its bound sourced there.
PACKET_SOURCES = {source.key: source for source in packets.CERTIFIED}
PACKET_KIND = "packet-derived-facts"
SQUISH_SOURCE_KEYS = frozenset(squish_packets.source_key(n) for n in squish_packets.NUMBERS)
#: The report that solved 48 known-best packings to their exact optima (T-098). It moves
#: a case's side by at most 5e-11 and keeps its packing, so the atlas pictures the
#: packing from the source that held the count before, which the packet's comparison
#: receipt names (`devtools.evand_exact_certificates compare`).
EXACT_OPTIMA_SOURCE_KEY = "[evand exact optima 2026-10-05]"

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
#: Additional horizontal separation before an inline regular-grid suffix, in drawing units.
POSTER_GRID_GAP = SUMMARY_PACKING_SIZE / 2
#: Later logical rows put the complete grid suffix on a second physical line.
POSTER_INLINE_ROWS = 16
#: Outside air surrounds the cards and the all-grid labels, without scaling either.
POSTER_OUTER_MARGIN = Decimal(120)
POSTER_GRID_LEFT = POSTER_OUTER_MARGIN + SUMMARY_SIDE_MARGIN
POSTER_GRID_MARKER_SIZE = "15"
POSTER_GRID_MARKER_BASELINE = Decimal(87)
POSTER_GRID_MARKER_LINE_PITCH = Decimal(18)
#: One fewer decimal digit in triangle captions, leaving space beside the degree.
POSTER_BOUND_DECIMAL_PLACES = 5
POSTER_BOUND_DEGREE_GAP = Decimal(5)
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
SUMMARY_LEGEND_GAP = Decimal(30)
#: Air between the last legend row and the explainer, which opens the footer block.
SUMMARY_FOOTER_GAP = Decimal(38)
#: Leading inside the footer block: explainer, citations, credit, edition stamp.
SUMMARY_FOOTER_LINE_PITCH = Decimal(27)
#: Air under the last footer line, which is where the canvas ends.
#:
#: These four were 38, 44, 30 and 32 for a three-line footer. The citations line
#: (2026-09-28) was fitted by taking its 27 units out of that air rather than growing the
#: canvas: the canvas size is pinned in `manifest.json` and its schema, which are data
#: under `sqpack.release.DATA_PATHS`, so a taller canvas would have been a data commit
#: and moved the version every artifact prints.
SUMMARY_BOTTOM_MARGIN = Decimal(25)
#: The footer gloss, as runs of (text, italic). The variables are set in italic like
#: the ones on the cards; the shared legend defines `deg` separately.
SUMMARY_EXPLAINER_RUNS = (
    ("s", True),
    ("(", False),
    ("n", True),
    (") is the side of the smallest square holding ", False),
    ("n", True),
    (" unit squares", False),
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
    "\u00d7": 584,
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
SUMMARY_REPOSITORY = "github.com/jlevy/squares"
#: Where the bounds on the cards are cited, under the explainer and above the credit.
#: The cards print numbers and no sources, so the footer says where the sources are
#: (the owner, 2026-09-28).
SUMMARY_CITATIONS = (
    f"Citations for all results are available in the Squares Project: {SUMMARY_REPOSITORY}"
)
POSTER_CITATIONS = "The Squares Project"
POSTER_DIAGRAM_CREDIT = "Diagram by Joshua Levy"
# Set a step above the other small labels so the URL reads as part of the
# heading block rather than as another footnote.
#: One size for the two lines under the title: the release line and the repository.
SUMMARY_SUBTITLE_SIZE = "26"
SUMMARY_REPOSITORY_SIZE = SUMMARY_SUBTITLE_SIZE
SUMMARY_RELEASE_BASELINE = Decimal(114)
SUMMARY_RELEASE_SIZE = SUMMARY_SUBTITLE_SIZE
SUMMARY_RELEASE_GAP = Decimal(11)
SUMMARY_SUBTITLE_BASELINE = Decimal(148)

#: The title and problem keep their enlarged type. Documentation below the problem
#: uses one smaller type step, preserving card scale and the spacious baselines.
POSTER_INFORMATION_TYPE_SCALE = Decimal(3)
POSTER_TITLE_SIZE = "144"
POSTER_FOOTER_SIZE = "48"
# Finite scale keeps the two column edges and their explicit gap exact in Decimal.
POSTER_LEGEND_TYPE_SCALE = (
    Decimal(POSTER_FOOTER_SIZE) / Decimal(SUMMARY_FOOTER_SIZE)
).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
POSTER_PROBLEM_SIZE = "57"
POSTER_PROBLEM_LINE_HEIGHT_RATIO = Decimal("1.50")
POSTER_DOCUMENTATION_LINE_HEIGHT_RATIO = Decimal("1.50")
POSTER_LEGEND_LINE_HEIGHT_RATIO = Decimal("1.60")
POSTER_CLOSING_LINE_HEIGHT_RATIO = Decimal("1.75")
POSTER_PROBLEM_LINE_PITCH = Decimal(POSTER_PROBLEM_SIZE) * POSTER_PROBLEM_LINE_HEIGHT_RATIO
POSTER_INFORMATION_WIDTH = Decimal(2600)
POSTER_INFORMATION_TOP = POSTER_OUTER_MARGIN
POSTER_INFORMATION_BOTTOM = POSTER_INFORMATION_TOP + Decimal(2191)
POSTER_TITLE_BASELINE = POSTER_INFORMATION_TOP + Decimal(144)
POSTER_LEGEND_BASELINE = POSTER_INFORMATION_TOP + Decimal(660)
POSTER_LEGEND_ROW_PITCH = Decimal(POSTER_FOOTER_SIZE) * POSTER_LEGEND_LINE_HEIGHT_RATIO
POSTER_LEGEND_COLUMN_GAP = Decimal(180)
POSTER_EXPLAINER_BASELINE = POSTER_INFORMATION_TOP + Decimal(360)
POSTER_FOOTER_LINE_PITCH = Decimal(POSTER_FOOTER_SIZE) * POSTER_DOCUMENTATION_LINE_HEIGHT_RATIO
POSTER_CLOSING_LINE_PITCH = Decimal(POSTER_FOOTER_SIZE) * POSTER_CLOSING_LINE_HEIGHT_RATIO
POSTER_PACKING_CREDITS_BASELINE = POSTER_INFORMATION_TOP + Decimal(1206)
POSTER_PACKING_CREDITS_LINE_COUNT = 3
POSTER_PACKING_CREDITS_PREFIX = "Best packings due to"
POSTER_PACKING_CREDITS_SECTION_GAP = Decimal(180)
POSTER_PROBLEM = (
    "The square packing problem asks for the side s(n) of the smallest square that can "
    "hold n unit squares, where the squares are free to rotate but cannot overlap."
)
POSTER_EXPLAINER_LINES = (
    (
        ("The square packing problem asks for the side ", False),
        ("s", True),
        ("(", False),
        ("n", True),
        (") of the smallest square", False),
    ),
    (
        ("that can hold ", False),
        ("n", True),
        (" unit squares, where the squares are free to rotate but cannot overlap.", False),
    ),
)
#: Quartz selects upright Helvetica Bold even for italic SVG spans. Arial's italic
#: face embeds correctly in Cairo's PDF and has compatible advances for these letters.
POSTER_ITALIC_FONT = "Arial, Helvetica, sans-serif"
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


#: The two facts a composite records about itself, as its metadata names them.
IDENTITY_REVISION_KEY = "data-revision"
IDENTITY_DATE_KEY = "data-date"


@dataclass(frozen=True)
class CompositeIdentity:
    """What one composite was drawn from: the data commit, and that commit's date.

    A poster is stamped once, when it is drawn, and is not re-stamped when the data
    moves (`sqpack.release`, rule 4). Its visible edition and date are held to this
    record, which the drawing carries in its own metadata, and not to the pin: the
    edition is as it read at this revision, and the date is the day of the data the
    cards show. A poster that travels alone can be traced to its data by
    either. The record is a git revision and a date, nothing a second file has to keep
    in step (`OR-16`).

    It used to be the pin and the release's date. The pin made every data commit rewrite
    eight binaries, and the release's date stood still while the drawing took in results
    registered after it: on 2026-09-30 the posters said "September 28" over cards
    redrawn that morning.
    """

    data_revision: str
    data_date: str

    @property
    def stamp(self) -> str:
        """The footer's last line: the edition as it read at this data revision."""
        return edition_at(self.data_revision)

    @property
    def formatted_date(self) -> str:
        """The data's date, written as a reader reads it."""
        day = date.fromisoformat(self.data_date)
        return f"{day:%B} {day.day}, {day.year}"

    @property
    def dateline(self) -> str:
        """The row-major figure's line under the title, dated by its data."""
        return f"Including new results ({self.formatted_date})"

    @property
    def poster_stamp(self) -> str:
        """The triangle's closing line, joining its edition and authoritative data date."""
        return f"{self.formatted_date} · {self.stamp}"

    @property
    def current(self) -> bool:
        """Whether this is the data every page now prints: the pin has not moved on."""
        return self.data_revision == DATA_REVISION

    def problems(self) -> list[str]:
        """What is wrong with the record as written, before git is asked anything."""
        found = []
        if re.fullmatch(r"[0-9a-f]{40}", self.data_revision) is None:
            found.append(f"{IDENTITY_REVISION_KEY} {self.data_revision!r} is not a full commit")
        try:
            date.fromisoformat(self.data_date)
        except ValueError:
            found.append(f"{IDENTITY_DATE_KEY} {self.data_date!r} is not an ISO date")
        return found


@dataclass(frozen=True)
class FrontierCase:
    n: int
    side: str
    path: Path
    text: str
    #: `reported_upper_bound.source_key`, which is how the record says where its number
    #: came from and so which source layer this build has to read.
    reported_source_key: str


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
class CompositeSegmentLine:
    """One explicit packing segment on a physical line of a logical square-bound row."""

    numbers: PackingSegment
    kind: Literal["non-grid", "grid"]
    physical_row: int
    left: Decimal
    top: Decimal


@dataclass(frozen=True)
class CompositeCardPosition:
    """Logical identity and physical placement, kept separate when a row wraps."""

    row: int
    column: int
    physical_row: int
    left: Decimal
    top: Decimal
    segment: Literal["non-grid", "grid", "unsegmented"]


@dataclass(frozen=True)
class CompositeCanvas:
    """Where every part of one composite sits, computed from its specification.

    The row-major figure reserves a title band and a bottom legend and footer. The
    triangle poster keeps the same card scale and puts that information in its upper
    right, so its height follows the cards and margins alone. The 1-100 figure's 2400
    by 2896 canvas, its legend at 2724 and its footer at 2790/2817/2844/2871 are what
    these formulas return
    for ten columns of ten.
    """

    spec: CompositeSpec
    #: Resolved only at the triangle renderer boundary. Geometry remains pure; a
    #: partial crop can carry full-row thresholds without reading a canonical file.
    transitions: tuple[GridTransition, ...] = ()

    def with_transitions(self, transitions: Sequence[GridTransition]) -> CompositeCanvas:
        """Bind canonical row segments to this pure placement calculation."""
        rows = [transition.row for transition in transitions]
        if len(set(rows)) != len(rows):
            raise ValueError("a composite cannot have duplicate grid-transition rows")
        selected = tuple(
            transition
            for transition in transitions
            if transition.first_n <= self.spec.last_n and transition.last_n >= self.spec.first_n
        )
        return replace(self, transitions=selected)

    @property
    def physical_columns(self) -> int:
        """The inline envelope; later grid suffixes share its right edge."""
        if not self.information_in_corner or not self.transitions:
            return self.spec.columns
        envelope = min(self.spec.columns, 2 * POSTER_INLINE_ROWS - 1)
        return max(
            envelope,
            *(
                segment.count
                for transition in self.transitions
                for segment in self._selected_segments(transition)
            ),
        )

    def _transition(self, row: int) -> GridTransition | None:
        return next(
            (transition for transition in self.transitions if transition.row == row), None
        )

    def _selected_segments(
        self, transition: GridTransition
    ) -> tuple[PackingSegment, PackingSegment]:
        stop = min(transition.last_n, self.spec.last_n) + 1
        first = max(transition.first_n, self.spec.first_n)
        boundary = min(max(transition.grid.first_n, first), stop)
        return PackingSegment(first, boundary), PackingSegment(boundary, stop)

    def split_row(self, row: int, transition: GridTransition | None = None) -> bool:
        if not self.information_in_corner or row <= POSTER_INLINE_ROWS:
            return False
        transition = transition or self._transition(row)
        if transition is None:
            # Direct synthetic geometry has no canonical context and retains its
            # ordinary placement. Production binds all selected row thresholds.
            return False
        non_grid, grid = self._selected_segments(transition)
        return not non_grid.empty and not grid.empty

    def _row_origin(self, row: int) -> tuple[int, Decimal]:
        split_rows = sum(self.split_row(previous) for previous in range(1, row))
        physical_row = row - 1 + split_rows
        return physical_row, self.grid_top + SUMMARY_ROW_PITCH * physical_row

    @property
    def physical_rows(self) -> int:
        return self.spec.rows + sum(self.split_row(row) for row in range(1, self.spec.rows + 1))

    def segment_lines(self, transition: GridTransition) -> tuple[CompositeSegmentLine, ...]:
        """Place selected non-grid and grid segments without changing their logical row."""
        if not self.information_in_corner:
            raise ValueError("square-bound segments require a triangle composite")
        non_grid, grid = self._selected_segments(transition)
        physical_row, top = self._row_origin(transition.row)
        split = self.split_row(transition.row, transition)
        lines = []
        if not non_grid.empty:
            lines.append(
                CompositeSegmentLine(non_grid, "non-grid", physical_row, self.grid_left, top)
            )
        if not grid.empty:
            if split or (transition.row > POSTER_INLINE_ROWS and non_grid.empty):
                left = (
                    Decimal(self.width)
                    - POSTER_OUTER_MARGIN
                    - SUMMARY_CARD_WIDTH
                    - SUMMARY_COLUMN_PITCH * (grid.count - 1)
                )
            else:
                left = self.grid_left + SUMMARY_COLUMN_PITCH * non_grid.count
                if not non_grid.empty:
                    left += POSTER_GRID_GAP
            lines.append(
                CompositeSegmentLine(
                    grid,
                    "grid",
                    physical_row + int(split),
                    left,
                    top + (SUMMARY_ROW_PITCH if split else Decimal(0)),
                )
            )
        return tuple(lines)

    def card_position(
        self, n: int, transition: GridTransition | None = None
    ) -> CompositeCardPosition:
        """Resolve one card from explicit segments, retaining its logical coordinates."""
        row, column = self.spec.card_position(n)
        transition = transition or self._transition(row + 1)
        if transition is not None and transition.row != row + 1:
            raise ValueError("a grid transition must belong to the card's square-bound row")
        if self.information_in_corner and transition is not None:
            line = next(
                line for line in self.segment_lines(transition) if n in line.numbers.numbers
            )
            return CompositeCardPosition(
                row,
                column,
                line.physical_row,
                line.left + SUMMARY_COLUMN_PITCH * (n - line.numbers.first_n),
                line.top,
                line.kind,
            )
        return CompositeCardPosition(
            row,
            column,
            row,
            self.grid_left + SUMMARY_COLUMN_PITCH * column,
            self.grid_top + SUMMARY_ROW_PITCH * row,
            "unsegmented",
        )

    @property
    def width(self) -> int:
        """Outside air around the actual cards, or the legacy row-major pitches."""
        width = (
            self.grid_left
            + SUMMARY_COLUMN_PITCH * (self.physical_columns - 1)
            + POSTER_GRID_GAP
            + SUMMARY_CARD_WIDTH
            + POSTER_OUTER_MARGIN
            if self.information_in_corner
            else SUMMARY_SIDE_MARGIN * 2 + SUMMARY_COLUMN_PITCH * self.spec.columns
        )
        return _whole_units(width, f"{self.spec.stem} width")

    @property
    def information_in_corner(self) -> bool:
        return self.spec.placement == CompositePlacement.square_bound_triangle

    @property
    def grid_left(self) -> Decimal:
        return POSTER_GRID_LEFT if self.information_in_corner else SUMMARY_GRID_LEFT

    @property
    def grid_top(self) -> Decimal:
        return POSTER_OUTER_MARGIN if self.information_in_corner else SUMMARY_GRID_TOP

    def card_left(self, n: int, transition: GridTransition | None = None) -> Decimal:
        """A cell's left edge, with a gap only in a triangle's regular-grid suffix."""
        return self.card_position(n, transition).left

    @property
    def information_right(self) -> Decimal:
        """End poster text at the final drawing's edge, inside the card's caption air."""
        if self.information_in_corner:
            trailing_card_air = (
                SUMMARY_CARD_WIDTH - SUMMARY_PACKING_INSET_X - SUMMARY_PACKING_SIZE
            )
            return Decimal(self.width) - POSTER_OUTER_MARGIN - trailing_card_air
        return Decimal(self.width) - SUMMARY_SIDE_MARGIN

    @property
    def information_left(self) -> Decimal:
        return self.information_right - POSTER_INFORMATION_WIDTH

    @property
    def grid_bottom(self) -> Decimal:
        """One row pitch below the last row's top."""
        return self.grid_top + SUMMARY_ROW_PITCH * self.physical_rows

    @property
    def legend_baseline(self) -> Decimal:
        """The first legend line, in the corner block or below the row-major grid."""
        if self.information_in_corner:
            return POSTER_LEGEND_BASELINE
        return self.grid_bottom + SUMMARY_LEGEND_GAP

    @property
    def explainer_baseline(self) -> Decimal:
        if self.information_in_corner:
            return POSTER_EXPLAINER_BASELINE
        return self.legend_baseline + SUMMARY_LEGEND_ROW_PITCH + SUMMARY_FOOTER_GAP

    @property
    def citations_baseline(self) -> Decimal:
        if self.information_in_corner:
            return self.stamp_baseline + 2 * POSTER_CLOSING_LINE_PITCH
        return self.explainer_baseline + SUMMARY_FOOTER_LINE_PITCH

    @property
    def credit_baseline(self) -> Decimal:
        if self.information_in_corner:
            return (
                POSTER_PACKING_CREDITS_BASELINE
                + POSTER_FOOTER_LINE_PITCH * (POSTER_PACKING_CREDITS_LINE_COUNT - 1)
                + POSTER_PACKING_CREDITS_SECTION_GAP
            )
        return self.citations_baseline + SUMMARY_FOOTER_LINE_PITCH

    @property
    def stamp_baseline(self) -> Decimal:
        pitch = (
            POSTER_CLOSING_LINE_PITCH
            if self.information_in_corner
            else SUMMARY_FOOTER_LINE_PITCH
        )
        return self.credit_baseline + pitch

    @property
    def height(self) -> int:
        bottom = (
            self.grid_top
            + SUMMARY_ROW_PITCH * (self.physical_rows - 1)
            + SUMMARY_CARD_HEIGHT
            + POSTER_OUTER_MARGIN
            if self.information_in_corner
            else self.stamp_baseline + SUMMARY_BOTTOM_MARGIN
        )
        return _whole_units(bottom, f"{self.spec.stem} height")

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
#: The published figure, which the explainer names by path and which several tests
#: compare byte for byte. Every composite, this one included, is reached through
#: `COMPOSITES`; a caller that means "the drawings this corpus publishes" reads that,
#: because a set built from this one called the poster an artifact nobody owned.
PRIMARY_COMPOSITE = COMPOSITES[0]

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
            "in crimson marks a recent construction giving an upper bound, a proof of a "
            "lower bound or an optimality proof since August 2026. Badges mark "
            "which side lengths are proved optimal, and whether a side length is pinned "
            "exactly by a radical or a minimal polynomial rather than only by a decimal. "
            f"{SUMMARY_CITATIONS}."
        ),
    ),
    "known-best-1-324": (
        "Best known packings of one through three hundred twenty-four unit squares",
        (
            "A left-aligned triangular poster of the retained best known unit-square "
            "packings for n equals 1 through 324, the whole audited corpus. Row k holds "
            "n equals (k minus 1) squared plus 1 through k squared, starting in the "
            "leftmost column. Eighteen logical rows end at 324. The last two rows put "
            "their complete grid suffixes on separate right-aligned lines, giving "
            "twenty physical lines within a thirty-one-column envelope. "
            "A k by k grid label marks the first retained regular grid packing "
            "in each row; an extra half-drawing width separates an irregular prefix "
            "from its grid suffix horizontally when inline. Wrapped segments use the "
            "same vertical pitch as every other physical line. "
            f"{POSTER_PROBLEM} "
            "A right-aligned information block in the "
            "upper-right corner "
            "contains the title, complete legend and publication details. Each tile is "
            "normalized to its own container and labeled with n, the best known upper "
            "bound on the container side and, where the value is not yet settled, the "
            "best proved lower bound beneath it. A star in crimson marks a recent "
            "construction giving an upper bound, a proof of a lower bound or an "
            "optimality proof since August 2026. Badges mark which side lengths are proved "
            "optimal, and whether a side length is pinned exactly by a radical or a "
            f"minimal polynomial rather than only by a decimal. "
            f"{POSTER_CITATIONS}: {SUMMARY_REPOSITORY}."
        ),
    ),
}


def _encoding_metadata(composite: CompositeSpec) -> dict[str, str]:
    """What this composite does differently from the house encoding, and why.

    Empty for a figure drawn the house way, which is what keeps the published 1-100
    figure's metadata -- and so its bytes -- exactly what it has always been. A
    composite that departs says so in its own drawing rather than only in a document
    beside it, because the drawing is what travels.
    """
    squares = composite.square_count
    records: dict[str, str] = {}
    if not composite.square_data_attributes:
        records["square-data-attributes"] = (
            f"omitted at {squares} squares, about 153 bytes each; every square's hue "
            "index, shade index, full-side contact count, orientation and angle class "
            "is carried per case by atlas/known-best/rendering/n-NNN.svg and by "
            "atlas/known-best/composite-figure.json"
        )
    if composite.square_stroke_shared:
        records["square-stroke"] = (
            f"set once on each card's square group rather than on all {squares} polygons"
        )
    if composite.coordinate_decimals is not None:
        records["square-coordinate-decimals"] = str(composite.coordinate_decimals)
    return records


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _manifest_text(manifest: object) -> str:
    """The atlas manifest in the retained layout. The source index keeps `_json_text`: it
    lives under `resources/web/`, where an archive's bytes are not re-laid."""
    return retained_json.dumps(manifest, sort_keys=True, ensure_ascii=False)


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
    reported = packing["reported_upper_bound"]
    return FrontierCase(
        n, str(reported["value"]), path, text, str(reported.get("source_key") or "")
    )


def _unitsquare_source_path(n: int) -> Path:
    """Where one UnitSquare case's rendering is retained, or would be fetched to.

    Resolved by looking rather than by range, so widening the corpus moves no bytes and
    re-spells no boundary. Two roots holding the same file is a refusal, because which
    copy is authoritative would otherwise be settled by the order they are listed in.
    Neither holding it is not: `--fetch` acquires an unretained rendering, and this
    collection's own root is where it lands.
    """
    filename = f"n{n:03d}.svg"
    found = [
        root / filename
        for root in (UNITSQUARE_ROOT, PROSPECTIVE_UNITSQUARE_ROOT)
        if (root / filename).is_file()
    ]
    if len(found) > 1:
        where = " and ".join(_relative(path) for path in found)
        raise ValueError(f"n={n}: retained UnitSquare rendering is ambiguous, in {where}")
    return found[0] if found else UNITSQUARE_ROOT / filename


@cache
def _exact_optima_pictured() -> dict[int, str]:
    """The source key each exact optimum's packing is pictured from, by count."""
    receipt = json.loads(evand_certificates.COMPARISON_RECEIPT.read_text(encoding="utf-8"))
    return {int(row["n"]): str(row["earlier_source_key"]) for row in receipt["rows"]}


def pictured_source_key(case: FrontierCase) -> str:
    """The source whose geometry the atlas reads for a case: the record's own, except
    where an exact optimum of a packing reports the side and its finder's source holds
    the pose."""
    if case.reported_source_key != EXACT_OPTIMA_SOURCE_KEY:
        return case.reported_source_key
    pictured = _exact_optima_pictured().get(case.n)
    if pictured is None:
        raise ValueError(f"n={case.n}: no source holds the packing of its exact optimum")
    return pictured


def _source_plan(
    case: FrontierCase,
    catalogue: dict[int, tuple[str, int, tuple[int, ...]]],
    unitsquare_svg_digests: dict[int, str],
) -> SourcePlan:
    integer_side = rational_integer(case.side)
    if integer_side is not None and integer_side * integer_side >= case.n:
        return SourcePlan("exact-grid", case.path, "", case.n, (case.n,))
    if pictured_source_key(case) == UNITSQUARE_SOURCE_KEY:
        # A record naming the release that the release does not carry is a refusal
        # rather than a fall-through to the catalogue: falling through would quietly
        # source a case from Kingbird whose own record says it came from elsewhere.
        upstream_digest = unitsquare_svg_digests.get(case.n)
        if upstream_digest is None:
            raise ValueError(f"n={case.n}: UnitSquare release omits its SVG digest")
        path = _unitsquare_source_path(case.n)
        return SourcePlan(
            "unitsquare-rendering",
            path,
            f"{UNITSQUARE_BASE_URL}/{path.name}",
            case.n,
            (case.n,),
            upstream_digest,
        )
    pictured = pictured_source_key(case)
    modern = _modern_packet_plan(case, pictured)
    if modern is not None:
        return modern
    if pictured in SQUISH_SOURCE_KEYS:
        path = squish_packets.fact_path(case.n)
        if (
            case.n not in squish_packets.NUMBERS
            or pictured != squish_packets.source_key(case.n)
            or not path.is_file()
        ):
            raise ValueError(f"n={case.n}: {pictured} retains no facts for this case")
        return SourcePlan(
            PACKET_KIND, path, squish_packets.source_url(case.n), case.n, (case.n,)
        )
    packet = PACKET_SOURCES.get(pictured)
    if packet is not None:
        # As for the release: a record naming a packet that holds no facts for its `n`
        # is a refusal, never a fall-through to the catalogue.
        upstream = packets.cases(packet).get(case.n)
        if upstream is None or not packet.fact(case.n).is_file():
            raise ValueError(f"n={case.n}: {packet.key} retains no facts for this case")
        return SourcePlan(
            PACKET_KIND,
            packet.fact(case.n),
            packet.blob_url(str(upstream["file"])),
            case.n,
            (case.n,),
        )
    return _catalogue_source_plan(case, catalogue)


def _modern_packet_plan(case: FrontierCase, pictured: str) -> SourcePlan | None:
    if pictured == evand_reports.SOURCE_KEY:
        evand_reports.read_fact(case.n)
        return SourcePlan(
            PACKET_KIND,
            evand_reports.fact_path(),
            f"{evand_reports.SOURCE}/blob/{evand_reports.REVISION}/{evand_reports.source_path(case.n)}",
            case.n,
            (case.n,),
        )
    for source in refinements.SOURCES.values():
        if pictured == source.key:
            path = refinements.fact_path(source, case.n)
            if not path.is_file():
                raise ValueError(f"n={case.n}: refinement source facts are missing")
            return SourcePlan(PACKET_KIND, path, source.url(case.n), case.n, (case.n,))
    for update in (squish_second, squish_followup):
        if pictured == update.SOURCE_KEY:
            if case.n not in update.NUMBERS or (update is squish_followup and case.n == 153):
                raise ValueError(f"n={case.n}: {pictured} retains no new packing for this case")
            path = update.fact_path(case.n)
            if not path.is_file():
                raise ValueError(f"n={case.n}: {pictured} retains no facts for this case")
            return SourcePlan(PACKET_KIND, path, update.source_url(case.n), case.n, (case.n,))
    return None


def _catalogue_source_plan(
    case: FrontierCase, catalogue: dict[int, tuple[str, int, tuple[int, ...]]]
) -> SourcePlan:
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
    _built_corpus.cache_clear()
    _expected_outputs.cache_clear()


@cache
def source_plans() -> dict[int, SourcePlan]:
    catalogue = catalogue_source_map(CATALOGUE, first_n=CORPUS.first_n, last_n=CORPUS.last_n)
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
    if plan.kind in {"kingbird-derived-facts", PACKET_KIND}:
        if not plan.path.is_file():
            raise FileNotFoundError(
                f"retained derived facts are missing: {_relative(plan.path)}"
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
            retained = load_witness(plan.path, fallback_schema=WITNESS_SCHEMA)
            revision = _retained_revision(retained)
            sources.append(
                {
                    "attribution": KINGBIRD_ATTRIBUTION,
                    "kind": plan.kind,
                    "license_status": KINGBIRD_LICENSE_STATUS,
                    "listed_n": list(plan.listed_n),
                    "n": n,
                    "raw_asset_retained": False,
                    "retention_policy": KINGBIRD_RETENTION_POLICY,
                    "retrieved": _retained_retrieval(retained),
                    **({"revision": revision} if revision is not None else {}),
                    "source_n": plan.source_n,
                    "url": plan.url,
                }
            )
            continue
        if plan.kind == PACKET_KIND:
            refinement = _refinement_source(n, plan.path)
            layer = _squish_layer(n, plan.path)
            if plan.path == evand_reports.fact_path() and n in evand_reports.NUMBERS:
                attribution = f"Evan Daniel, {plan.url} at {evand_reports.REVISION}"
                retrieved = "2026-10-07"
            elif refinement is not None:
                attribution = (
                    f"Seth Rehwaldt after Francisco Couzo, {plan.url} at {refinement.revision}"
                )
                retrieved = "2026-10-08"
            elif layer is not None:
                author = squish_packets.AUTHOR
                revision = (
                    "issuecomment-6031977107"
                    if layer is squish_packets and n == 153
                    else layer.REVISION
                )
                attribution = f"{author}, {plan.url} at {revision}"
                retrieved = layer.RETRIEVED
            else:
                packet = next(
                    item for item in packets.CERTIFIED if plan.path.is_relative_to(item.facts)
                )
                attribution = f"{packet.author}, {packet.url} at {packet.revision}"
                retrieved = packet.retrieved
            sources.append(
                {
                    "attribution": attribution,
                    "kind": plan.kind,
                    "license_status": (
                        "MIT"
                        if plan.path == evand_reports.fact_path()
                        else "no-licence-published"
                    ),
                    "listed_n": list(plan.listed_n),
                    "n": n,
                    "path": _relative(plan.path),
                    "raw_asset_retained": plan.path == evand_reports.fact_path(),
                    "retention_policy": (
                        "Complete source certificates and MIT licences retained unchanged."
                        if plan.path == evand_reports.fact_path()
                        else KINGBIRD_RETENTION_POLICY
                    ),
                    "retrieved": retrieved,
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


def _retained_retrieval(retained: Mapping[str, Any]) -> str:
    """When the retained derived facts were read from the catalogue.

    `devtools.derive_kingbird_facts` dates each witness by the pass that read its SVG, so
    a count refreshed from a later capture keeps that later date; the corpus-wide
    `RETRIEVED_DATE` is only the fallback for a witness that records none.
    """
    source = retained.get("source")
    recorded = source.get("retrieved") if isinstance(source, Mapping) else None
    return str(recorded) if recorded else RETRIEVED_DATE


def _retained_revision(retained: Mapping[str, Any], field: str = "revision") -> str | None:
    """The third party's pinned parse the retained facts were read from, if any.

    `devtools.derive_kingbird_facts --from-parse` records it for a count whose SVG this
    repository could not fetch, with the parse file's digest as `revision_sha256`; a
    witness read from the SVG itself records neither, and a rebuild keeps whatever the
    retained witness says.
    """
    source = retained.get("source")
    recorded = source.get(field) if isinstance(source, Mapping) else None
    return str(recorded) if recorded else None


def _squish_layer(n: int, path: Path) -> Any | None:
    """Choose an immutable revision by its canonical fact path and exact roster."""
    for layer in (squish_second, squish_followup, squish_packets):
        if n in layer.NUMBERS and path == layer.fact_path(n):
            return layer
    return None


def _refinement_source(n: int, path: Path) -> refinements.Source | None:
    for source in refinements.SOURCES.values():
        if n in source.numbers and path == refinements.fact_path(source, n):
            return source
    return None


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
                retrieved=_retained_retrieval(retained),
                revision=_retained_revision(retained),
                revision_sha256=_retained_revision(retained, "revision_sha256"),
            )
        if plan.kind == PACKET_KIND:
            refinement = _refinement_source(case.n, plan.path)
            if plan.path == evand_reports.fact_path() and case.n in evand_reports.NUMBERS:
                witness = evand_houses.build_witness(case.n)
                _assert_side_matches(case, str(witness["side"]))
            elif refinement is not None:
                witness = _refinement_derived_witness(case, refinement)
            else:
                witness = None
            if witness is not None:
                return witness
            if _squish_layer(case.n, plan.path) is not None:
                return _squish_derived_witness(case, plan)
            retained = load_witness(plan.path, fallback_schema=WITNESS_SCHEMA)
            _assert_side_matches(case, str(retained["side"]))
            pictured = pictured_source_key(case)
            return packet_derived_witness(
                case.n,
                retained,
                source_key=pictured,
                source_path=_relative(plan.path),
                retrieved=PACKET_SOURCES[pictured].retrieved,
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


def _refinement_derived_witness(case: FrontierCase, source: refinements.Source) -> dict:
    facts = refinements.read_fact(source, case.n)
    if Fraction(case.side) != Fraction(facts["side"]):
        raise ValueError("refinement exact side differs from its current case")
    witness = refinements.to_witness(source, case.n)
    witness["id"] = f"W-known-best-n{case.n:03d}"
    result, report = exact_verify(witness)
    if not report.valid or result["verification_passed"] is not True:
        raise ValueError("refinement drawing failed complete exact feasibility")
    witness["claim"]["coordinate_provenance"] = "verified"
    witness["claim"]["limitations"] = (
        "Exact rational corners from the retained centered source, checked "
        "with exact predicates at the full rational side. Drawing feasibility "
        "does not assign the imported result's confirmation rung. No optimality, "
        "rigidity or human oversight claim."
    )
    witness["certificate"] = {
        "kind": "exact-rational-sat",
        "replay": (
            f"uv run --frozen packing-witness verify witnesses/known-best/n-{case.n:03d}.yaml"
        ),
        "result": result,
    }
    return witness


def _squish_derived_witness(case: FrontierCase, plan: SourcePlan) -> dict:
    """Check exact half-angle facts before the atlas asserts coordinate feasibility.

    The source's finite decimal is a display value; the exact side and corners decide
    feasibility. This check establishes the drawing's geometry, while confirmation of
    the imported result remains the frontier record's separate evidence lane.
    """
    layer = _squish_layer(case.n, plan.path)
    if layer is None:
        raise ValueError("source plan names no retained SQUISH revision")
    fact = layer.read_fact(case.n)
    if layer is not squish_packets:
        if case.side != squish_followup.display(fact["side"]):
            raise ValueError("source display disagrees with the prescribed update ceiling")
    else:
        normalized_side = squish_packets.verified_value(
            Fraction(fact["side"]), fact["printed_side"]
        )
        if Fraction(case.side) not in {
            Fraction(fact["printed_side"]),
            Fraction(normalized_side),
        }:
            raise ValueError("source display disagrees with the reported frontier side")
    if fact["n"] != case.n or len(fact["squares"]) != case.n:
        raise ValueError("derived facts do not contain the requested square count")
    witness = squish_packets.to_witness(fact)
    witness["id"] = f"W-known-best-n{case.n:03d}"
    result, report = exact_verify(witness)
    if not report.valid or not result["verification_passed"]:
        detail = report.failures[0] if report.failures else "unknown failure"
        raise ValueError(f"exact feasibility check failed: {detail}")
    witness["claim"]["limitations"] = (
        "Exact rational corners derived from retained SQUISH center/half-angle facts, "
        "checked with exact predicates at the source's exact rational side. The SVG "
        "rounds only for visualization. Verifies this upper-bound construction, not "
        "optimality or confirmation of the imported result in the frontier register. "
        "The source publishes no licence, so only derived geometry and attributed "
        "metadata are retained; this conservative retention policy is not a legal "
        "conclusion."
    )
    witness["source"] = {
        "key": pictured_source_key(case),
        "path": _relative(plan.path),
        "url": plan.url,
        "retrieved": layer.RETRIEVED,
        "revision": (
            "issuecomment-6031977107"
            if layer is squish_packets and case.n == 153
            else layer.REVISION
        ),
    }
    witness["certificate"] = {
        "kind": "exact-rational-sat",
        "replay": (
            f"uv run --frozen packing-witness verify witnesses/known-best/n-{case.n:03d}.yaml"
        ),
        "result": result,
    }
    return witness


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


def _summary_coordinate(value: Decimal, decimals: int | None) -> str:
    """One emitted coordinate, at the composite's declared rounding.

    `decimals` is None for the house encoding, which emits whatever the projection and
    the pinned `SVG_EMISSION_PRECISION` produce -- 28 significant digits for a source
    that carries them. A composite that declares a rounding gets it here, explicitly and
    from its own specification: `D-359` is about a precision that came from wherever the
    process had been left, and a figure that rounds on purpose is the opposite of that.
    """
    if decimals is not None:
        value = value.quantize(Decimal(1).scaleb(-decimals), rounding=ROUND_HALF_EVEN)
    return format_svg_number(value)


def _summary_points(
    square: SquareGeometry,
    *,
    container_side: Decimal,
    x: Decimal,
    y: Decimal,
    scale: Decimal,
    decimals: int | None = None,
) -> str:
    return " ".join(
        (
            f"{_summary_coordinate(x + point.x.projected * scale, decimals)},"
            f"{_summary_coordinate(y + (container_side - point.y.projected) * scale, decimals)}"
        )
        for point in square.corners
    )


def _poster_grid_transitions(canvas: CompositeCanvas) -> tuple[GridTransition, ...]:
    """Resolve the full retained corpus before selecting a triangle, including a crop.

    The shared contract requires complete square-bound rows. A partial drawing must
    therefore resolve against the complete canonical manifest, not its selected cases.
    Row-major figures and generic geometry readers never enter this preflight.
    """
    if not canvas.information_in_corner:
        return ()
    if canvas.transitions:
        return canvas.transitions
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))["atlas"]["entries"]
    return tuple(
        transition
        for transition in grid_transitions(entries)
        if transition.first_n <= canvas.spec.last_n and transition.last_n >= canvas.spec.first_n
    )


def resolved_composites(
    entries: Sequence[Mapping[str, Any]] | None = None,
) -> tuple[CompositeCanvas, ...]:
    """Bind triangle segment plans at a production boundary, leaving generic geometry pure.

    Data producers pass their complete entry sequence; retained export consumers read
    the canonical manifest through the existing triangle preflight. Neither path asks
    the strict row contract to classify a synthetic row-major or a cropped sequence.
    """
    transitions = (
        grid_transitions(entries)
        if entries is not None and any(canvas.information_in_corner for canvas in COMPOSITES)
        else None
    )
    return tuple(
        canvas.with_transitions(
            tuple(
                transition
                for transition in transitions
                if transition.first_n <= canvas.spec.last_n
                and transition.last_n >= canvas.spec.first_n
            )
            if transitions is not None
            else _poster_grid_transitions(canvas)
        )
        if canvas.information_in_corner
        else canvas
        for canvas in COMPOSITES
    )


def _append_grid_transition_marker(
    root: ET.Element, transition: GridTransition, *, canvas: CompositeCanvas
) -> None:
    """Mark the retained grid dimensions inside the separator or all-grid margin."""
    center = (
        canvas.card_left(transition.grid.first_n, transition) - POSTER_GRID_GAP / 2
        if transition.has_irregular_prefix
        else (POSTER_OUTER_MARGIN + canvas.grid_left) / 2
    )
    grid_position = canvas.card_position(transition.grid.first_n, transition)
    lines = canvas.segment_lines(transition)
    extra_gap = (
        POSTER_GRID_GAP
        if len(lines) == 2 and lines[0].physical_row == lines[1].physical_row
        else Decimal(0)
    )
    row_top = grid_position.top
    dimensions = f"{transition.row}\u00d7{transition.row}"
    labels = (dimensions, "GRID")
    room = (
        POSTER_GRID_GAP
        if transition.has_irregular_prefix
        else canvas.grid_left - POSTER_OUTER_MARGIN
    )
    if any(_text_width(label, POSTER_GRID_MARKER_SIZE) > room for label in labels):
        raise ValueError("a grid transition marker exceeds its separator space")
    marker = sub(
        root,
        "g",
        {
            "data-feature": "grid-transition",
            "data-row": str(transition.row - 1),
            "data-physical-row": str(grid_position.physical_row),
            "data-gap-axis": "horizontal" if extra_gap else "none",
            "data-first-grid-n": str(transition.first_grid_n),
            "data-grid-side": str(transition.row),
            "data-extra-gap": format_svg_number(extra_gap),
            "aria-label": f"{dimensions} grid packings begin at n={transition.first_grid_n}",
        },
    )
    for index, label in enumerate(labels):
        sub(
            marker,
            "text",
            {
                "data-feature": "grid-transition-label",
                "x": format_svg_number(center),
                "y": format_svg_number(
                    row_top
                    + POSTER_GRID_MARKER_BASELINE
                    + POSTER_GRID_MARKER_LINE_PITCH * index
                ),
                "text-anchor": "middle",
                "font-family": SUMMARY_FONT,
                "font-size": POSTER_GRID_MARKER_SIZE,
                "font-weight": "700",
                "fill": SUMMARY_SMALL_FILL,
            },
        ).text = label


def _composite_bound_display(
    display: str, canvas: CompositeCanvas, *, degree: int | None = None
) -> str:
    """Shorten triangle captions without strengthening a stored inequality.

    Five decimals ordinarily fit. A longer degree label can need one fewer digit;
    measure the two captions with their italic kern before accepting either precision.
    """
    if not canvas.information_in_corner:
        return display
    head, separator, numeral = display.rpartition(" ")
    direction: Literal["lower", "upper", "exact"]
    if head.endswith("≥"):
        direction = "lower"
    elif head.endswith("≤"):
        direction = "upper"
    elif head.endswith("="):
        direction = "exact"
    else:
        raise ValueError("a composite bound display lacks a supported relation")
    for decimals in (POSTER_BOUND_DECIMAL_PLACES, POSTER_BOUND_DECIMAL_PLACES - 1):
        caption = (
            head
            + separator
            + display_bound_value(numeral, decimal_places=decimals, direction=direction)
        )
        if degree is None or degree < 2:
            return caption
        extent = (
            _text_width(caption, SUMMARY_SMALL_SIZE)
            + Decimal(SUMMARY_SMALL_SIZE) * SUMMARY_ITALIC_KERN
            + _text_width(f"deg {degree}", SUMMARY_SMALL_SIZE)
        )
        if extent + POSTER_BOUND_DEGREE_GAP <= SUMMARY_PACKING_SIZE:
            return caption
    raise ValueError("a triangle bound caption collides with its algebraic degree")


def _append_summary_card(
    root: ET.Element,
    built: BuiltCase,
    *,
    spec: RenderSpec,
    canvas: CompositeCanvas,
    grid_transition: GridTransition | None = None,
    recent: RecentContributions | None = None,
) -> None:
    n = built.frontier.n
    position = canvas.card_position(n, grid_transition)
    row, column = position.row, position.column
    card_x, card_y = position.left, position.top
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
            **(
                {
                    "data-physical-row": str(position.physical_row),
                    "data-segment": position.segment,
                }
                if canvas.information_in_corner
                else {}
            ),
            "data-source-id": frame.source_id,
            "data-known-rigid": str(_figure_entries()[n]["rigidity"]["known_rigid"]).lower(),
            "data-rigidity": json.dumps(
                _figure_entries()[n]["rigidity"], ensure_ascii=False, separators=(",", ":")
            ),
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
    encoding = canvas.spec
    squares = card
    if encoding.square_stroke_shared:
        # The stroke every square shares, stated once. On a group of its own rather than
        # on the card, because the card also holds text and text that inherits a stroke
        # is drawn outlined; and the group is what names the squares once the polygons
        # inside it no longer carry `data-feature` of their own.
        squares = sub(
            card,
            "g",
            {
                "data-feature": "square-fills",
                "stroke": PAPER_THEME.container,
                "stroke-width": "0.42",
                "stroke-linejoin": "round",
            },
        )
    for square in frame.squares:
        color = colors[square.square_id]
        attributes: dict[str, str] = {}
        if encoding.square_data_attributes:
            attributes |= {
                "data-feature": "square-fill",
                "data-square": f"n-{n:03d}-{square.square_id}",
                "data-hue-index": str(color.hue_index),
                "data-shade-index": str(color.shade_index),
                "data-contact-sides": str(color.contact_sides),
                "data-orientation-radians": str(color.orientation_radians),
            }
        attributes["points"] = _summary_points(
            square,
            container_side=side,
            x=packing_x,
            y=packing_y,
            scale=scale,
            decimals=encoding.coordinate_decimals,
        )
        attributes["fill"] = color.fill
        if not encoding.square_stroke_shared:
            attributes |= {
                "stroke": PAPER_THEME.container,
                "stroke-width": "0.42",
                "stroke-linejoin": "round",
            }
        polygon = sub(squares, "polygon", attributes)
        if encoding.square_data_attributes and color.angle_class is not None:
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

    badges = _case_badges(built, recent=recent)
    left = packing_x
    right = packing_x + SUMMARY_PACKING_SIZE
    top_row = card_y + SUMMARY_LABEL_BASELINE
    bottom_row = card_y + SUMMARY_BOUND_BASELINE

    badge_top = top_row - Decimal(29) * SUMMARY_LABEL_CAP_RATIO
    cursor = right - SUMMARY_BADGE_SIZE
    for glyph, style, label in reversed(badges):
        _append_badge(
            card,
            glyph,
            style,
            label,
            x=cursor,
            top=badge_top,
            accent=FIRST_PARTY_ACCENT_COLOR
            if recent is not None and recent.optimal and glyph == "O"
            else None,
        )
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
    _append_function_text(
        bound,
        _composite_bound_display(
            _figure_entries()[n]["side"]["display"],
            canvas,
            degree=_figure_entries()[n]["exactness"]["degree"],
        ),
        SUMMARY_SMALL_SIZE,
        accent=FIRST_PARTY_ACCENT_COLOR if recent is not None and recent.upper else None,
    )

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

    _append_lower_bound(
        card,
        n,
        left=left,
        baseline=card_y + SUMMARY_LOWER_BASELINE,
        recent=None if recent is None else recent.lower,
        canvas=canvas,
    )


def _append_lower_bound(
    card: ET.Element,
    n: int,
    *,
    left: Decimal,
    baseline: Decimal,
    recent: bool | None = None,
    canvas: CompositeCanvas | None = None,
) -> None:
    """The certified floor, under the best known side.

    A proved case says `s(n) = ...` on the line above and gets nothing here. Where the
    floor is a recent result, the accent falls on the numeral alone, the same
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
        entry["display"]
        if canvas is None
        else _composite_bound_display(entry["display"], canvas),
        SUMMARY_SMALL_SIZE,
        accent=FIRST_PARTY_ACCENT_COLOR
        if (entry["recent_result"] if recent is None else recent)
        else None,
    )


#: What the star means, in the legend and on each card's badge: a recent result, whoever
#: proved it (the owner, 2026-09-27). It used to read "lower bound first proved here", and
#: so went out at n = 11 when Kleddamag's 3.875, developed from T-026, became the bound.
#: The month is read from `RECENT_SINCE`, so the label cannot name another; it is the
#: old label's width.
RECENT_LABEL = recent_label()


@cache
def _figure_entries() -> dict[int, dict]:
    """The figure record, keyed by n.

    Every claim the figure states is decided in
    devtools/build_composite_figure_data.py and validated against
    composite-figure.schema.yaml. These numeric claims and badge meanings come from
    that record; both composites separately receive contribution-recency flags from
    the canonical status helper.
    """
    return {entry["n"]: entry for entry in load_figure_record()["entries"]}


def _case_badges(
    built: BuiltCase, *, recent: RecentContributions | None = None
) -> tuple[tuple[str, str, str], ...]:
    """The card's icons, the new-result star first where the case carries one.

    The star reads as one of the badges rather than as punctuation on the bound line,
    so it sits with them; being first in the row puts it leftmost, since the row is
    laid out from the right.
    """
    entry = _figure_entries()[built.frontier.n]
    badges = [
        (badge["glyph"], badge["style"], badge["meaning"])
        for badge in entry["badges"]
        if badge["glyph"] != "R"
    ]
    if entry["rigidity"]["known_rigid"]:
        badges.append(("R", "solid", "known rigid"))
    if entry["lower"]["recent_result"] if recent is None else recent.any:
        badges.insert(0, ("", "star", RECENT_LABEL))
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
    parent: ET.Element,
    glyph: str,
    style: str,
    label: str,
    *,
    x: Decimal,
    top: Decimal,
    type_scale: Decimal = Decimal(1),
    accent: str | None = None,
) -> None:
    """Draw one badge at an explicit box top.

    Callers position the box rather than passing a text baseline, so the card can
    sit its badges flush with the top of the big number.
    """
    size = SUMMARY_BADGE_SIZE * type_scale
    if style == "star":
        # The legend's star is the same polygon the cards carry, centred in a badge box
        # so the row lays out as if it were one. `glyph` is unused: there is no star to
        # typeset, which is the point.
        _append_star(
            parent,
            center_x=x + size / 2,
            center_y=top + size / 2,
            feature="legend-star",
            label=label,
            scale=size * SUMMARY_BADGE_STAR_SPAN / (SUMMARY_STAR_INSET * 2),
        )
        return
    fill, stroke, glyph_fill = {
        "solid": (PAPER_THEME.muted, "none", PAPER_THEME.background),
        "ink": ("none", PAPER_THEME.muted, PAPER_THEME.muted),
        "muted": ("none", PAPER_THEME.muted, PAPER_THEME.muted),
    }[style]
    if accent is not None:
        if style == "solid":
            fill = accent
        else:
            stroke = glyph_fill = accent
    sub(
        parent,
        "rect",
        {
            "data-feature": "evidence-badge",
            "data-evidence": label,
            "x": format_svg_number(x),
            "y": format_svg_number(top),
            "width": format_svg_number(size),
            "height": format_svg_number(size),
            "rx": format_svg_number(Decimal("4.5") * type_scale),
            "fill": fill,
            "stroke": stroke,
            "stroke-width": format_svg_number(Decimal("1.2") * type_scale),
        },
    )
    sub(
        parent,
        "text",
        {
            "x": format_svg_number(x + size / 2),
            "y": format_svg_number(top + _badge_baseline(glyph) * type_scale),
            "text-anchor": "middle",
            "font-family": SUMMARY_FONT,
            "font-size": format_svg_number(SUMMARY_BADGE_FONT_SIZE * type_scale),
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
    right_edge: Decimal | None = None,
    left_edge: Decimal | None = None,
    type_scale: Decimal = Decimal(1),
    label_size: str | None = None,
) -> None:
    """Lay one legend row centered on the canvas or ending at a right edge.

    Each entry is (mark, label), where mark is a badge triple, a run of
    swatches or None for an unbadged definition. Widths come from the Helvetica
    advance table, because the renderer holds no font metrics.
    """
    badge_size = SUMMARY_BADGE_SIZE * type_scale
    footer_size = label_size or format_svg_number(Decimal(SUMMARY_FOOTER_SIZE) * type_scale)
    mark_gap = Decimal(8) * type_scale
    top = baseline - badge_size + Decimal(4) * type_scale

    def mark_width(mark: object) -> Decimal:
        if mark is None:
            return Decimal(0)
        if isinstance(mark, tuple):
            return badge_size
        return badge_size * Decimal(len(mark))  # pyright: ignore[reportArgumentType]

    gap = Decimal(34) * type_scale
    widths = [
        mark_width(mark)
        + (mark_gap if mark is not None else 0)
        + _text_width(label, footer_size)
        for mark, label in entries
    ]
    row_width = sum(widths, Decimal(0)) + gap * Decimal(len(entries) - 1)
    if (
        right_edge is not None or left_edge is not None
    ) and row_width > POSTER_INFORMATION_WIDTH:
        raise ValueError("a poster legend line exceeds its information block")
    cursor = (
        left_edge
        if left_edge is not None
        else (
            (Decimal(canvas_width) - row_width) / 2
            if right_edge is None
            else right_edge - row_width
        )
    )
    for (mark, label), width in zip(entries, widths, strict=True):
        if mark is None:
            run_end = cursor
        elif isinstance(mark, tuple):
            glyph, style, name = mark
            _append_badge(legend, glyph, style, name, x=cursor, top=top, type_scale=type_scale)
            run_end = cursor + badge_size
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
                        "width": format_svg_number(badge_size),
                        "height": format_svg_number(badge_size),
                        "fill": fill,
                        "stroke": PAPER_THEME.container,
                        "stroke-width": format_svg_number(Decimal("0.8") * type_scale),
                    },
                )
                if numeral:
                    numeral_size = format_svg_number(Decimal("11.5") * type_scale)
                    if _text_width(numeral, numeral_size) > badge_size - type_scale:
                        raise ValueError("a legend swatch label exceeds its square")
                    sub(
                        legend,
                        "text",
                        {
                            "data-swatch-label": numeral,
                            "x": format_svg_number(run_end + badge_size / 2),
                            "y": format_svg_number(top + Decimal("13.4") * type_scale),
                            "text-anchor": "middle",
                            "font-family": SUMMARY_FONT,
                            "font-size": numeral_size,
                            "font-weight": "650",
                            "fill": "#000000"
                            if numeral in {"90°", "45°"}
                            else PAPER_THEME.background
                            if hex_oklch(fill)[0] < 0.62
                            else PAPER_THEME.ink,
                        },
                    ).text = numeral
                run_end += badge_size
        sub(
            legend,
            "text",
            {
                "x": format_svg_number(
                    run_end + (mark_gap if mark is not None else 0)
                    if right_edge is None
                    else cursor + width
                ),
                "y": format_svg_number(baseline),
                **(
                    {"text-anchor": "start", "data-feature": "legend-label"}
                    if left_edge is not None
                    else {"text-anchor": "end", "data-feature": "legend-label"}
                    if right_edge is not None
                    else {}
                ),
                "font-family": SUMMARY_FONT,
                "font-size": footer_size,
                "font-weight": SUMMARY_FOOTER_WEIGHT,
                "fill": SUMMARY_SMALL_FILL,
            },
        ).text = label
        cursor += width + gap


def _append_summary_legend(
    root: ET.Element,
    *,
    spec: RenderSpec,
    canvas: CompositeCanvas,
    contributions: Mapping[int, RecentContributions] | None = None,
) -> None:
    """The shared eight meanings, with renderer-specific marks and positioning."""
    record = load_figure_record()
    totals = next(
        composite["totals"]
        for composite in record["composites"]
        if composite["stem"] == canvas.spec.stem
    )
    recent_count = (
        totals["lower_bound_recent_result"]
        if contributions is None
        else sum(contributions[n].any for n in canvas.spec.numbers)
    )
    descriptor = atlas_legend(
        AtlasLegendCounts(
            proved_optimal=totals["proved_optimal"],
            exact_value_known=totals["exact_value_known"],
            only_known_numerically=totals["only_known_numerically"],
            known_rigid=totals["rigidity_known"],
            recent_results=recent_count,
        )
    )
    palette = square_fill_palette(
        hue_count=spec.hue_count,
        shades_per_hue=spec.shades_per_hue,
        lightness_span=spec.shade_lightness_span,
    )
    middle = spec.shades_per_hue // 2

    def entry(item: LegendItem) -> tuple[object, str]:
        mark: object
        if item.marker is None:
            mark = None
        elif item.marker == "angles":
            labels = item.marker_labels or ("",) * len(item.marker_values)
            mark = [
                (palette[index][middle], label)
                for index, label in zip(item.marker_values, labels, strict=True)
            ]
        elif item.marker == "shades":
            mark = [
                (palette[1][index], str(value))
                for index, value in enumerate(item.marker_values)
            ]
        else:
            mark = (
                "" if item.marker == "star" else item.marker,
                "star" if item.marker == "star" else "muted" if item.marker == "≈" else "solid",
                item.label,
            )
        return mark, item.text

    legend = sub(root, "g", {"data-feature": "evidence-legend"})
    if canvas.information_in_corner:
        badge_size = SUMMARY_BADGE_SIZE * POSTER_LEGEND_TYPE_SCALE
        mark_gap = Decimal(8) * POSTER_LEGEND_TYPE_SCALE

        def row_width(item: LegendItem) -> Decimal:
            if item.marker is None:
                return _text_width(item.text, POSTER_FOOTER_SIZE)
            return (
                badge_size * (len(item.marker_values) if item.marker_values else 1)
                + mark_gap
                + _text_width(item.text, POSTER_FOOTER_SIZE)
            )

        widths = [
            max(row_width(item) for item in column)
            for column in (descriptor.left, descriptor.right)
        ]
        span = sum(widths, Decimal(0)) + POSTER_LEGEND_COLUMN_GAP
        if span > POSTER_INFORMATION_WIDTH:
            raise ValueError("the poster legend columns exceed their information block")
        cursor = canvas.information_right - span
        for name, items, width in zip(
            ("left", "right"), (descriptor.left, descriptor.right), widths, strict=True
        ):
            column = sub(
                legend,
                "g",
                {
                    "data-feature": "legend-column",
                    "data-column": name,
                    "data-left": format_svg_number(cursor),
                    "data-width": format_svg_number(width),
                },
            )
            for index, item in enumerate(items):
                _legend_row(
                    column,
                    [entry(item)],
                    baseline=canvas.legend_baseline + POSTER_LEGEND_ROW_PITCH * index,
                    canvas_width=canvas.width,
                    left_edge=cursor,
                    type_scale=POSTER_LEGEND_TYPE_SCALE,
                    label_size=POSTER_FOOTER_SIZE,
                )
            cursor += width + POSTER_LEGEND_COLUMN_GAP
    else:
        _legend_row(
            legend,
            [entry(item) for item in (*descriptor.left, descriptor.right[0])],
            baseline=canvas.legend_baseline,
            canvas_width=canvas.width,
        )
        _legend_row(
            legend,
            [entry(item) for item in descriptor.right[1:]],
            baseline=canvas.legend_baseline + SUMMARY_LEGEND_ROW_PITCH,
            canvas_width=canvas.width,
        )


def _append_summary_explainer(
    root: ET.Element,
    *,
    baseline: Decimal,
    canvas_width: int,
    right_edge: Decimal | None = None,
    type_scale: Decimal = Decimal(1),
    runs: Sequence[tuple[str, bool]] = SUMMARY_EXPLAINER_RUNS,
    feature: str = "explainer",
    italic_font_family: str | None = None,
) -> None:
    font_size = format_svg_number(Decimal(SUMMARY_FOOTER_SIZE) * type_scale)
    kern_width = Decimal(font_size) * SUMMARY_ITALIC_KERN
    kern = format_svg_number(kern_width)
    line_width = sum(
        (_text_width(text, font_size) for text, _italic in runs),
        Decimal(0),
    ) + kern_width * Decimal(
        sum(
            1
            for index, (_text, italic) in enumerate(runs)
            if index and not italic and runs[index - 1][1]
        )
    )
    if right_edge is not None and line_width > POSTER_INFORMATION_WIDTH:
        raise ValueError("the poster explainer exceeds its information block")
    explainer = sub(
        root,
        "text",
        {
            "data-feature": feature,
            # Anchored from the left rather than centred: a centred run made of several
            # tspans is not laid out as one chunk by every renderer, and the parts stack
            # on the same centre. Measuring the line and starting it is unambiguous.
            "x": format_svg_number(
                (Decimal(canvas_width) - line_width) / 2
                if right_edge is None
                else right_edge - line_width
            ),
            "y": format_svg_number(baseline),
            "font-family": SUMMARY_FONT,
            "font-size": font_size,
            "font-weight": SUMMARY_SMALL_WEIGHT,
            "fill": SUMMARY_SMALL_FILL,
        },
    )
    previous_italic = False
    for text, italic in runs:
        attributes: dict[str, str] = {"font-style": "italic"} if italic else {}
        if italic and italic_font_family is not None:
            attributes["font-family"] = italic_font_family
        # An upright run following an italic one needs the same thin space the cards use.
        if previous_italic and not italic:
            attributes["dx"] = kern
        sub(explainer, "tspan", attributes).text = text
        previous_italic = italic


def _append_summary_information(
    root: ET.Element,
    *,
    spec: RenderSpec,
    canvas: CompositeCanvas,
    identity: CompositeIdentity,
    contributions: Mapping[int, RecentContributions] | None = None,
) -> None:
    width = canvas.width
    composite = canvas.spec
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
    release_width = _text_width(identity.dateline, SUMMARY_RELEASE_SIZE)
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
    ).text = identity.dateline
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
    _append_summary_legend(root, spec=spec, canvas=canvas, contributions=contributions)
    _append_summary_explainer(root, baseline=canvas.explainer_baseline, canvas_width=width)
    sub(
        root,
        "text",
        {
            "data-feature": "citations",
            "x": heading_x,
            "y": format_svg_number(canvas.citations_baseline),
            "text-anchor": "middle",
            "font-family": SUMMARY_FONT,
            "font-size": SUMMARY_FOOTER_SIZE,
            "font-weight": SUMMARY_SMALL_WEIGHT,
            "fill": SUMMARY_SMALL_FILL,
        },
    ).text = SUMMARY_CITATIONS
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
    ).text = identity.stamp


@dataclass(frozen=True, slots=True)
class PackingCredit:
    """Every named contributor to displayed constructions, grouped by source family."""

    names: tuple[str, ...]
    source_keys: tuple[str, ...]
    citation: str
    #: Supported author-attribution dates; an integer retains year-only precision.
    dates: tuple[tuple[str, date | int], ...] = ()


def _credit_date_key(value: date | int | None) -> tuple[int, int, int, int]:
    if isinstance(value, date):
        return value.year, 1, value.month, value.day
    return (value, 0, 0, 0) if value is not None else (0, 0, 0, 0)


@cache
def _poster_packing_credits(first_n: int, last_n: int) -> tuple[PackingCredit, ...]:
    """Read construction credits from typed case fields and the canonical bibliography.

    The ordinary citation can shorten three authors to ``et al.``; this list retains
    every finder and improver. Source families group the metadata, with every complete
    source key retained in the SVG.
    """
    register = build_bound_citations.load_register()
    groups: dict[str, tuple[list[str], list[str], dict[str, date | int]]] = {}
    for n in range(first_n, last_n + 1):
        case = build_bound_citations.load_case(n)
        citation = build_bound_citations.upper_citation(n, case, register)
        if citation is None:
            continue
        reported = case["reported_upper_bound"]
        credited = [*(reported.get("found_by") or []), *(reported.get("improved_by") or [])]
        names = [register.names[name] for name in dict.fromkeys(credited)]
        source_key = citation["source_key"]
        source: build_bound_citations.Source | None = None
        if source_key is None:
            reference = citation["text"]
            names = names or [build_bound_citations.PROJECT_NAME]
            source_keys = []
        else:
            source = register.sources[source_key]
            # Repository handles identify the retained packet, while the bibliography
            # names its author. Group these sources by their canonical author names.
            family = (
                ", ".join(source.authors)
                if source.venue == "GitHub"
                else source.key.removeprefix("[").removesuffix("]").split()[0]
            )
            reference = f"[{family}{f' {source.year}' if source.year is not None else ''}]"
            names = names or list(source.authors)
            source_keys = [source.key]
        group_names, group_sources, group_dates = groups.setdefault(reference, ([], [], {}))
        group_names.extend(name for name in names if name not in group_names)
        group_sources.extend(key for key in source_keys if key not in group_sources)
        found_year = reported.get("found_year")
        dated_names: list[tuple[str, date | int]] = (
            [(register.names[name], found_year) for name in (reported.get("found_by") or [])]
            if isinstance(found_year, int)
            else []
        )
        if source is not None:
            source_date = source.dated or source.year
            if source_date is not None:
                # An improver's publication does not redate inherited finders.
                dated_names.extend(
                    (name, source_date) for name in names if name in source.authors
                )
        for name, supported in dated_names:
            if _credit_date_key(supported) > _credit_date_key(group_dates.get(name)):
                group_dates[name] = supported
    return tuple(
        PackingCredit(tuple(names), tuple(keys), reference, tuple(dates.items()))
        for reference, (names, keys, dates) in groups.items()
    )


def _poster_credit_lines(packing_credits: Sequence[PackingCredit]) -> tuple[str, ...]:
    """Balance complete names across three print lines, each author appearing once.

    Authors are newest first by their latest supported attribution date, with
    year-only precision retained and undated authors last. Only consecutive breaks
    are considered, so balancing cannot rearrange chronology. Source keys remain in
    the SVG metadata.
    """
    names = list(dict.fromkeys(name for credit in packing_credits for name in credit.names))
    latest: dict[str, date | int] = {}
    for credit in packing_credits:
        for name, supported in credit.dates:
            if _credit_date_key(supported) > _credit_date_key(latest.get(name)):
                latest[name] = supported
    names.sort(
        key=lambda name: (
            *(-part for part in _credit_date_key(latest.get(name))),
            name.casefold(),
        )
    )
    if not names:
        return (POSTER_PACKING_CREDITS_PREFIX,)
    line_count = min(POSTER_PACKING_CREDITS_LINE_COUNT, len(names))

    def measure(
        groups: tuple[tuple[int, ...], ...],
    ) -> tuple[tuple[str, ...], tuple[Decimal, ...], Decimal]:
        lines = tuple(
            (f"{POSTER_PACKING_CREDITS_PREFIX} " if index == 0 else "")
            + ", ".join(names[number] for number in group)
            + ("." if index == line_count - 1 else ",")
            for index, group in enumerate(groups)
        )
        widths = tuple(_text_width(line, POSTER_FOOTER_SIZE) for line in lines)
        mean = sum(widths, Decimal(0)) / line_count
        score = sum(((width - mean) ** 2 for width in widths), Decimal(0))
        return lines, widths, score

    best_groups: tuple[tuple[int, ...], ...] | None = None
    best_lines: tuple[str, ...] = ()
    best_score: Decimal | None = None
    for breaks in combinations(range(1, len(names)), line_count - 1):
        boundaries = (0, *breaks, len(names))
        groups = tuple(tuple(range(first, last)) for first, last in pairwise(boundaries))
        lines, widths, score = measure(groups)
        if max(widths) > POSTER_INFORMATION_WIDTH:
            continue
        if best_score is None or score < best_score:
            best_groups, best_lines, best_score = groups, lines, score
    if best_groups is None or best_score is None:
        raise ValueError("poster packing credits exceed their three-line information block")
    return best_lines


def _append_poster_information(
    root: ET.Element,
    *,
    spec: RenderSpec,
    canvas: CompositeCanvas,
    identity: CompositeIdentity,
    contributions: Mapping[int, RecentContributions] | None = None,
) -> None:
    right = canvas.information_right
    packing_credits = _poster_packing_credits(canvas.spec.first_n, canvas.spec.last_n)
    credit_lines = _poster_credit_lines(packing_credits)
    credit_baselines = [
        POSTER_PACKING_CREDITS_BASELINE + POSTER_FOOTER_LINE_PITCH * index
        for index in range(len(credit_lines))
    ]
    explainer_baselines = [
        canvas.explainer_baseline + POSTER_PROBLEM_LINE_PITCH * index
        for index in range(len(POSTER_EXPLAINER_LINES))
    ]
    repository_baseline = canvas.citations_baseline + POSTER_CLOSING_LINE_PITCH
    font_size = Decimal(POSTER_FOOTER_SIZE)
    document_lines = [
        (POSTER_TITLE_BASELINE, Decimal(POSTER_TITLE_SIZE)),
        *((baseline, Decimal(POSTER_PROBLEM_SIZE)) for baseline in explainer_baselines),
        *(
            (canvas.legend_baseline + POSTER_LEGEND_ROW_PITCH * index, font_size)
            for index in range(4)
        ),
        *((baseline, font_size) for baseline in credit_baselines),
        (canvas.credit_baseline, font_size),
        (canvas.stamp_baseline, font_size),
        (canvas.citations_baseline, font_size),
        (repository_baseline, font_size),
    ]
    if any(
        above + above_size * Decimal("0.3") > below - below_size
        for (above, above_size), (below, below_size) in pairwise(document_lines)
    ):
        raise ValueError("poster documentation lines overlap")
    if any(
        baseline - size < POSTER_INFORMATION_TOP
        or baseline + size * Decimal("0.3") > POSTER_INFORMATION_BOTTOM
        for baseline, size in document_lines
    ):
        raise ValueError("poster documentation lies outside its information block")
    block = sub(
        root,
        "g",
        {
            "data-feature": "poster-information",
            "data-left": format_svg_number(canvas.information_left),
            "data-right": format_svg_number(right),
            "data-top": format_svg_number(POSTER_INFORMATION_TOP),
            "data-bottom": format_svg_number(POSTER_INFORMATION_BOTTOM),
        },
    )

    card_positions = tuple(canvas.card_position(n) for n in canvas.spec.numbers)

    def text_line(
        feature: str,
        content: str,
        baseline: Decimal,
        size: str = POSTER_FOOTER_SIZE,
        *,
        parent: ET.Element | None = None,
    ) -> ET.Element:
        spacing = (
            Decimal("1.5") * POSTER_INFORMATION_TYPE_SCALE
            if feature == "poster-title"
            else Decimal(0)
        )
        extent = _text_width(content, size) + spacing * max(len(content) - 1, 0)
        if extent > POSTER_INFORMATION_WIDTH:
            raise ValueError(f"the poster {feature} line exceeds its information block")
        if (
            baseline - Decimal(size) < POSTER_INFORMATION_TOP
            or baseline + Decimal(size) * Decimal("0.3") > POSTER_INFORMATION_BOTTOM
        ):
            raise ValueError(f"the poster {feature} line lies outside its information block")
        text_left = right - extent
        text_top = baseline - Decimal(size)
        text_bottom = baseline + Decimal(size) * Decimal("0.3")
        if any(
            text_left < position.left + SUMMARY_CARD_WIDTH
            and right > position.left
            and text_top < position.top + SUMMARY_CARD_HEIGHT
            and text_bottom > position.top
            for position in card_positions
        ):
            raise ValueError(f"the poster {feature} line overlaps a packing card")
        node = sub(
            block if parent is None else parent,
            "text",
            {
                "data-feature": feature,
                "x": format_svg_number(right),
                "y": format_svg_number(baseline),
                "text-anchor": "end",
                # The two project-reference lines share one plain style. Arial also
                # keeps Quartz's slash advances consistent in the printed address.
                "font-family": POSTER_ITALIC_FONT
                if feature in {"citations", "repository"}
                else SUMMARY_FONT,
                "font-size": size,
                "font-weight": "400" if feature in {"citations", "repository"} else "700",
                "fill": "#000000"
                if feature in {"citations", "repository"}
                else PAPER_THEME.ink
                if feature in {"poster-title", "release"}
                else SUMMARY_SMALL_FILL,
            },
        )
        if spacing:
            node.set("letter-spacing", format_svg_number(spacing))
        node.text = content
        return node

    text_line(
        "poster-title",
        "BEST KNOWN SQUARE PACKINGS",
        POSTER_TITLE_BASELINE,
        POSTER_TITLE_SIZE,
    )
    for index, runs in enumerate(POSTER_EXPLAINER_LINES):
        _append_summary_explainer(
            block,
            baseline=explainer_baselines[index],
            canvas_width=canvas.width,
            right_edge=right,
            type_scale=POSTER_INFORMATION_TYPE_SCALE,
            runs=runs,
            feature=("explainer", "problem-explainer")[index],
            italic_font_family=POSTER_ITALIC_FONT,
        )
    _append_summary_legend(block, spec=spec, canvas=canvas, contributions=contributions)
    credit_block = sub(
        block,
        "g",
        {
            "data-feature": "packing-credits",
            "data-credited-names": json.dumps(
                list(
                    dict.fromkeys(name for credit in packing_credits for name in credit.names)
                ),
                ensure_ascii=False,
            ),
            "data-source-keys": json.dumps(
                list(
                    dict.fromkeys(
                        key for credit in packing_credits for key in credit.source_keys
                    )
                ),
                ensure_ascii=False,
            ),
        },
    )
    for content, baseline in zip(credit_lines, credit_baselines, strict=True):
        text_line("packing-credit-line", content, baseline, parent=credit_block)
    text_line("credit", POSTER_DIAGRAM_CREDIT, canvas.credit_baseline)
    text_line("release-stamp", identity.poster_stamp, canvas.stamp_baseline)
    text_line("citations", POSTER_CITATIONS, canvas.citations_baseline)
    text_line("repository", SUMMARY_REPOSITORY, repository_baseline)


@emission_precision()
def render_known_best_summary_svg(
    built: Sequence[BuiltCase], canvas: CompositeCanvas, identity: CompositeIdentity
) -> str:
    """Render a complete, zoomable overview of one composite's range of cases.

    `identity` is what the drawing says of itself: the data commit it shows, in its
    metadata and its footer, and that commit's date, in its visible date. The caller says
    which: `drawable_identity` for a new drawing, the retained one to check an old one.

    The pin covers the per-card scale and corner arithmetic in `_append_summary_card`
    and `_summary_points`, which is its own Decimal work rather than the house
    renderer's, and so would otherwise track whatever precision the process was left in.
    """
    composite = canvas.spec
    numbers = [item.frontier.n for item in built]
    if numbers != list(composite.numbers):
        raise ValueError(
            f"the {composite.stem} composite requires exactly {composite.cases.label} in order"
        )
    transitions = _poster_grid_transitions(canvas)
    if canvas.information_in_corner:
        canvas = canvas.with_transitions(transitions)
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
            IDENTITY_DATE_KEY: identity.data_date,
            IDENTITY_REVISION_KEY: identity.data_revision,
            "generated-by": GENERATOR,
            "last-n": str(composite.last_n),
            "rows": str(composite.rows),
            "square-count": str(composite.square_count),
            **(
                {
                    "layout": composite.layout,
                    "regular-grid-extra-gap": format_svg_number(POSTER_GRID_GAP),
                    "physical-columns": str(canvas.physical_columns),
                    "physical-rows": str(canvas.physical_rows),
                    "physical-row-pitch": format_svg_number(SUMMARY_ROW_PITCH),
                    "grid-suffix-second-line-from-row": str(POSTER_INLINE_ROWS + 1),
                }
                if composite.placement == CompositePlacement.square_bound_triangle
                else {}
            ),
            **_encoding_metadata(composite),
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
    contributions = recent_contributions_by_case()
    if canvas.information_in_corner:
        _append_poster_information(
            root, spec=spec, canvas=canvas, identity=identity, contributions=contributions
        )
    else:
        _append_summary_information(
            root, spec=spec, canvas=canvas, identity=identity, contributions=contributions
        )
    by_row = {transition.row: transition for transition in transitions}
    for item in built:
        row, _column = composite.card_position(item.frontier.n)
        _append_summary_card(
            root,
            item,
            spec=spec,
            canvas=canvas,
            grid_transition=by_row.get(row + 1),
            recent=contributions.get(item.frontier.n),
        )
    for transition in transitions:
        if transition.grid.first_n in composite.numbers:
            _append_grid_transition_marker(root, transition, canvas=canvas)
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
    stamped = png_export_bytes(export, svg_text)
    with atomic_output_file(export.path, make_parents=True) as temporary:
        temporary.write_bytes(stamped)


def png_export_bytes(export: RasterExport, svg_text: str) -> bytes:
    """One raster of the SVG, with its receipt, as bytes and without writing it.

    Apart from `_update_png_export` so the cost of drawing an export can be measured
    (`devtools.measure_release_assets`) by the code that draws it, without touching the
    retained file.
    """
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
    return stamped


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
    witness = orient_atlas_witness(witness)
    problems = check_witness_semantics(witness)
    if problems:
        raise ValueError(f"{witness['id']}: {problems[0]}")
    witness_text = witness_document(witness, schema="../witness.schema.yaml")
    return BuiltCase(case, plan, witness, witness_text, _render(witness))


def _build_case_unit(unit: tuple[int, SourcePlan]) -> BuiltCase:
    """One case, addressed by value, so `pool.map` can carry the work to a worker.

    `_build_case` takes two arguments and `pool.map` passes one; a lambda or a `partial`
    over a memoized function is not picklable, and a named module-level adapter is.
    """
    return _build_case(*unit)


def built_cases(numbers: Sequence[int], workers: int) -> list[BuiltCase]:
    """Every named case, built in the order given, serially or through a process pool.

    The per-case work is embarrassingly parallel and it is nearly all of this module's
    cost: each case reads its own source, normalizes one witness, checks that witness's
    semantics and renders one house SVG, and no case reads another's output. Measured on
    2026-09-07 at `n=1..324`, `build_known_best_atlas --check` was 691.19s of the 703.28s
    validation step that carries it and of which the other seven subcommands were 12.09s,
    so this loop is the step. The corpus divides well, too: 52,650 squares over 324 units
    whose largest is one 324-square rendering, so no single unit can hold the wall up.

    `workers` is the pool size, and `1` runs in this process rather than through a pool,
    because a one-worker pool is a subprocess and a protocol for no concurrency at all.
    Who chooses the count matters more than the count: the CLI asks
    `sqpack.workers.worker_count`, which reads the `PACK_JOBS` cap the gate exports to
    every step -- the same contract `screen_translation_escape`, `check_golden_basins`
    and `check_soundness_perimeter` use -- while every in-process caller takes the serial
    default, which is what `expected_outputs` exists to keep.

    Order is the corpus's, whichever way it ran. `pool.map` yields by submission index
    rather than by completion, so the outputs are built in the order the serial loop
    built them in, which is what lets `check` compare them byte for byte.
    """
    plans = source_plans()
    units = [(n, plans[n]) for n in numbers]
    count = max(1, min(workers, len(units)))
    if count == 1:
        return [_build_case(n, plan) for n, plan in units]
    with ProcessPoolExecutor(max_workers=count) as pool:
        return list(pool.map(_build_case_unit, units))


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
    elif plan.kind == PACKET_KIND:
        derivation = (
            "exact rational half-angle conversion of retained source facts, checked "
            "with exact predicates"
            if plan.path == evand_reports.fact_path()
            or _squish_layer(n, plan.path) is not None
            or _refinement_source(n, plan.path) is not None
            else "deterministic reuse of a source packet's retained Witness/v2 facts"
        )
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


def expected_outputs(workers: int = 1) -> tuple[dict[Path, str], dict]:
    """Every derived artifact of the data layer, and the manifest describing them.

    The composites are not among them: a composite is drawn under an identity
    (`expected_composite`), on demand, and its retained copy may trail these.

    Callers get copies so the memo cannot be mutated underneath them.

    `workers` defaults to 1 rather than to the shared worker policy, and that is the
    safety property rather than a missing wire-up. A pool worker is a fresh process that
    re-imports this module, so it does not see a module-level source root a caller has
    repointed -- which is exactly what
    `test_known_best_rejects_corrupted_retained_unitsquare_svg` does when it points
    `UNITSQUARE_ROOT` at a corrupted copy and expects the digest check to refuse it. Every
    in-process caller therefore gets the serial build, and only `main` resolves a count
    from `PACK_JOBS`.
    """
    outputs, manifest = _expected_outputs(workers)
    return dict(outputs), copy.deepcopy(manifest)


def _manifest_document(entries: list[dict], composites: list[dict]) -> dict:
    """The manifest, given the per-case entries and the composite records.

    Factored out of `_expected_outputs` so a sampled check can re-derive everything a
    manifest says about itself -- its contract, its declared range, its policy, its
    generator and its composites -- from the retained entries, without rebuilding the 324
    cases those entries describe.
    """
    return {
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
                    "source packets' retained derived facts, or immutable UnitSquare "
                    "renderings"
                ),
                "witness_layer": "lossless where possible; limitations explicit otherwise",
                "rendering_layer": "repository deterministic house renderer",
                "annotation_layer": "derived and excluded from grammar validation until frozen",
            },
            # A list rather than a single record: the corpus publishes one composite
            # today and the geometry of a second is a second specification, so the shape
            # that describes them does not change when one is added.
            "composites": composites,
            "entries": entries,
        },
    }


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

    Logical rows and columns come from the specification; canvas dimensions come from
    its bound segment plan. Production callers resolve that plan before recording it,
    so the record cannot claim an export size the drawing does not have.
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
def _built_corpus(workers: int) -> tuple[BuiltCase, ...]:
    """Every case, built once for a worker count.

    The data layer and the composite comparison both read it, and each would otherwise
    pay the whole corpus build, which is nearly all of this module's cost.
    """
    return tuple(built_cases(CORPUS.numbers, workers))


@cache
def _expected_outputs(workers: int) -> tuple[dict[Path, str], dict]:
    plans = source_plans()
    source_index = _source_index(plans)
    built = _built_corpus(workers)
    outputs: dict[Path, str] = {SOURCE_MANIFEST: _json_text(source_index)}
    for item in built:
        n = item.frontier.n
        outputs[WITNESS_ROOT / f"n-{n:03d}.yaml"] = item.witness_text
        outputs[RENDER_ROOT / f"n-{n:03d}.svg"] = item.rendering_text
        outputs[item.frontier.path] = _frontier_with_witness(
            item.frontier, str(item.witness["id"])
        )
    entries = [_manifest_entry(item) for item in built]
    manifest = _manifest_document(
        entries,
        [_composite_record(canvas) for canvas in resolved_composites(entries)],
    )
    outputs[MANIFEST] = _manifest_text(manifest)
    return outputs, manifest


def _cards(built: Sequence[BuiltCase], canvas: CompositeCanvas) -> list[BuiltCase]:
    """The cases one composite draws, in its order."""
    wanted = set(canvas.spec.numbers)
    return [item for item in built if item.frontier.n in wanted]


def expected_composite(
    canvas: CompositeCanvas, identity: CompositeIdentity, workers: int = 1
) -> str:
    """One composite as a rebuild of the whole corpus draws it, under `identity`.

    This is the expensive drawing, from cases re-derived from their sources, and it is
    what the whole `--check` compares a retained composite with. `workers` is as
    `expected_outputs` has it, and the corpus build is shared with it.
    """
    return render_known_best_summary_svg(
        _cards(_built_corpus(workers), canvas), canvas, identity
    )


def retained_cases(numbers: Sequence[int]) -> list[BuiltCase]:
    """The named cases as the retained records state them, without rebuilding one.

    What a composite is drawn from. The drawing reads a case's number and its witness
    and nothing else, and re-deriving 324 witnesses from their sources was 397 of the
    415 seconds a redraw took (`devtools.measure_release_assets --timings`, 2026-10-01),
    all of it spent proving again what `--check` proves already. Both composites drawn
    from these are byte for byte what the whole rebuild draws, which
    `test_known_best_composite_contains_every_case_and_square` holds.
    """
    scoped = [n for n in numbers if n in squish_second.NUMBERS]
    if scoped:
        squish_house.check_houses(scoped)
    evand_scoped = [n for n in numbers if n in evand_reports.NUMBERS]
    if evand_scoped:
        evand_houses.check_houses(evand_scoped)
    plans = source_plans()
    cases = []
    for n in numbers:
        witness_path = WITNESS_ROOT / f"n-{n:03d}.yaml"
        cases.append(
            BuiltCase(
                _frontier_case(n),
                plans[n],
                dict(load_witness(witness_path, fallback_schema=WITNESS_SCHEMA)),
                witness_path.read_text(encoding="utf-8"),
                (RENDER_ROOT / f"n-{n:03d}.svg").read_text(encoding="utf-8"),
            )
        )
    return cases


def update(workers: int = 1) -> None:
    """Rewrite the data layer: witnesses, renderings, manifest and frontier links.

    The composites are left alone. They are redrawn by `update_composites`, at a
    version bump or on demand, and until then say which data they show; a data change
    that rewrote them was eight binaries and several megabytes a commit.
    """
    squish_house.guard_house_outputs(list(CORPUS.numbers))
    refinement_houses.guard_house_outputs(list(CORPUS.numbers))
    evand_houses.guard_house_outputs(list(CORPUS.numbers))
    # The figure record decides every claim a drawing states, so refresh it first and
    # drop the memo, or the comparison below would read a stale one.
    build_composite_figure_data.update()
    _figure_entries.cache_clear()
    clear_build_caches()
    outputs, _manifest = expected_outputs(workers)
    for path, content in sorted(outputs.items(), key=lambda item: item[0].as_posix()):
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.is_file() and path.read_text(encoding="utf-8") == content:
            continue
        with atomic_output_file(path) as temporary:
            temporary.write_text(content, encoding="utf-8")
    print(
        f"known-best atlas updated: {CORPUS.count} witnesses, {CORPUS.count} house "
        f"renderings, {CORPUS.count} frontier links; the {len(COMPOSITES)} "
        f"composite{_plural(len(COMPOSITES))} are redrawn by --update-composites"
    )
    for note in composite_findings().notes:
        print(note)


def update_selected(numbers: Sequence[int], workers: int = 1) -> None:
    """Refresh selected geometry, refusing any change in the retained remainder.

    Source selection and displayed side must agree with the old manifest outside the
    requested scope. Each selected witness is rebuilt through the ordinary strict
    producer; all other manifest and figure entries and geometry files are preserved.
    Derivation and serialization finish before publishing any file, so a refused scope
    or failed selected build leaves every retained output unchanged.
    """
    squish_house.guard_house_outputs(list(numbers))
    refinement_houses.guard_house_outputs(list(numbers))
    evand_houses.guard_house_outputs(list(numbers))
    selected = set(numbers)
    if not selected or len(selected) != len(numbers) or not selected <= set(CORPUS.numbers):
        raise ValueError("selected atlas refresh requires unique corpus counts")
    clear_build_caches()
    retained: list[dict] = json.loads(MANIFEST.read_text())["atlas"]["entries"]
    if [row["n"] for row in retained] != list(CORPUS.numbers):
        raise ValueError("selected atlas refresh requires a complete retained corpus")
    plans = source_plans()
    for row in retained:
        n = row["n"]
        if n in selected:
            continue
        plan = plans[n]
        expected_path = SOURCE_MANIFEST if plan.kind == "kingbird-derived-facts" else plan.path
        if (
            row["reported_side"] != _frontier_case(n).side
            or row["source"]["kind"] != plan.kind
            or row["source"]["path"]
            != expected_path.relative_to(REPOSITORY_ROOT / "packing").as_posix()
            or row["source"].get("url", "") != plan.url
        ):
            raise ValueError(f"unselected n={n} changed; use the complete atlas producer")
    built = built_cases(numbers, workers)
    prospective_figure = build_composite_figure_data.build_record()
    retained_figure = load_figure_record()
    figure_entries = {}
    for name, figure in (
        ("retained", retained_figure),
        ("derived", prospective_figure["figure"]),
    ):
        rows = figure["entries"]
        if [row["n"] for row in rows] != list(CORPUS.numbers):
            raise ValueError(f"selected atlas refresh requires a complete {name} figure corpus")
        figure_entries[name] = {row["n"]: row for row in rows}
    for n in CORPUS.numbers:
        if n not in selected and figure_entries["retained"][n] != figure_entries["derived"][n]:
            raise ValueError(
                f"unselected figure n={n} changed; use the complete atlas producer"
            )
    replacement: dict[int, dict] = {item.frontier.n: _manifest_entry(item) for item in built}
    entries = [replacement.get(row["n"], row) for row in retained]
    manifest = _manifest_document(
        entries, [_composite_record(canvas) for canvas in resolved_composites(entries)]
    )
    outputs = {
        build_composite_figure_data.RECORD: retained_json.dumps(
            prospective_figure, sort_keys=True, ensure_ascii=False
        ),
        MANIFEST: _manifest_text(manifest),
        SOURCE_MANIFEST: _json_text(_source_index(plans)),
    }
    for item in built:
        n = item.frontier.n
        outputs[WITNESS_ROOT / f"n-{n:03d}.yaml"] = item.witness_text
        outputs[RENDER_ROOT / f"n-{n:03d}.svg"] = item.rendering_text
        outputs[item.frontier.path] = _frontier_with_witness(
            item.frontier, str(item.witness["id"])
        )
    for path, text in outputs.items():
        if path.is_file() and path.read_text(encoding="utf-8") == text:
            continue
        with atomic_output_file(path, make_parents=True) as temporary:
            temporary.write_text(text, encoding="utf-8")
    _figure_entries.cache_clear()
    print(
        f"Selected atlas refreshed: {len(selected)} geometries; "
        f"{CORPUS.count - len(selected)} entries preserved"
    )


def _git_result(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(REPOSITORY_ROOT), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


def drawable_identity() -> CompositeIdentity:
    """What a composite drawn now says of itself, or a refusal to draw one.

    The drawing is stamped with the pinned data revision, so the pin has to be the data
    the working tree holds: git's last data commit, with nothing uncommitted on top of
    it. Otherwise the stamp would name data the cards do not show, which is the one
    thing the stamp is for. Drawing therefore needs a repository, which rendering a page
    never does; a composite is drawn by a person at a desk, not by the deploy.
    """
    try:
        live = data_revision(REPOSITORY_ROOT)
        day = commit_date(REPOSITORY_ROOT, DATA_REVISION)
    except RuntimeError as error:
        raise ValueError(
            f"a composite is stamped with the data commit it shows, and {error}"
        ) from error
    if live != DATA_REVISION:
        raise ValueError(
            f"the data changed at {live[:12]} and release.py still pins "
            f"{DATA_REVISION[:12]}: run `python -m devtools.release_pin --update`, "
            "commit it, then draw"
        )
    dirty = _git_result("status", "--porcelain", "--", *data_pathspec())
    if dirty.returncode or dirty.stdout.strip():
        raise ValueError(
            "the data has uncommitted changes, so a composite drawn now would show data "
            "its stamp does not name; commit them and re-pin first:\n"
            + (dirty.stdout.rstrip() or dirty.stderr.strip())
        )
    return CompositeIdentity(DATA_REVISION, day)


def retained_identity(svg_text: str) -> CompositeIdentity:
    """The record a retained composite carries of what it was drawn from."""
    values = render_composite_pdf.svg_metadata(svg_text)
    missing = [key for key in (IDENTITY_REVISION_KEY, IDENTITY_DATE_KEY) if key not in values]
    if missing:
        raise ValueError(
            f"records no {' or '.join(missing)}: it does not say what data it was drawn "
            "from; redraw it with --update-composites"
        )
    return CompositeIdentity(values[IDENTITY_REVISION_KEY], values[IDENTITY_DATE_KEY])


def _without_composite_geometry(document: dict, envelope: str) -> dict:
    unchanged = copy.deepcopy(document)
    for composite in unchanged[envelope]["composites"]:
        for key in ("columns", "rows", "layout"):
            composite.pop(key, None)
        for key in ("svg", "png_preview", "png_high_resolution", "png_link_preview_card"):
            if key in composite:
                composite[key].pop("width", None)
                composite[key].pop("height", None)
    return unchanged


def update_composite_records() -> None:
    """Refresh layout facts, refusing changes to cases, sources, or legend totals.

    Read retained witnesses instead of re-deriving their feasibility receipts. Both
    documents pass preflight before either is written, so a layout refresh cannot
    silently import a data change or repair unrelated record drift.
    """
    figure_path = build_composite_figure_data.RECORD
    retained_figure = json.loads(figure_path.read_text(encoding="utf-8"))
    retained_manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    problems, entries = _retained_problems(
        composite_records=retained_manifest["atlas"]["composites"]
    )
    if problems or entries is None:
        raise ValueError(
            "unrelated retained atlas discrepancies prevent a layout refresh:\n  "
            + "\n  ".join(problems[:20])
        )
    expected_figure = build_composite_figure_data.build_record()
    expected_entries = [_manifest_entry(case) for case in retained_cases(CORPUS.numbers)]
    expected_manifest = _manifest_document(
        expected_entries,
        [_composite_record(canvas) for canvas in resolved_composites(expected_entries)],
    )
    for envelope, retained, expected in (
        ("figure", retained_figure, expected_figure),
        ("atlas", retained_manifest, expected_manifest),
    ):
        if _without_composite_geometry(retained, envelope) != _without_composite_geometry(
            expected, envelope
        ):
            raise ValueError(
                f"unrelated {envelope} facts differ; a layout refresh changes only geometry"
            )
    outputs = (
        (figure_path, retained_json.dumps(expected_figure, sort_keys=True, ensure_ascii=False)),
        (MANIFEST, _manifest_text(expected_manifest)),
    )
    for path, content in outputs:
        if path.read_text(encoding="utf-8") != content:
            with atomic_output_file(path) as temporary:
                temporary.write_text(content, encoding="utf-8")
    _figure_entries.cache_clear()
    print("known-best composite records refreshed: layout only; case facts preserved")


def update_composites() -> None:
    """Redraw both composites and every export, from the retained witnesses.

    Run at a version bump and on demand, never because the data moved. The drawing is
    made from the retained records, so they are held to their own cheap checks first:
    a composite drawn from a manifest or a figure record that is stale would be stale
    the same way. Whether the retained witnesses are what their sources give is the
    whole `--check`, which is not repeated here.
    """
    identity = drawable_identity()
    build_composite_figure_data.check()
    _figure_entries.cache_clear()
    problems, _entries = _retained_problems()
    if problems:
        raise ValueError(
            "the retained atlas records disagree with each other, so a composite drawn "
            "from them would too; run --update first:\n  " + "\n  ".join(problems[:20])
        )
    cases = retained_cases(CORPUS.numbers)
    rasters = 0
    for canvas in resolved_composites():
        svg_text = render_known_best_summary_svg(_cards(cases, canvas), canvas, identity)
        retained = canvas.svg_path
        if not retained.is_file() or retained.read_text(encoding="utf-8") != svg_text:
            with atomic_output_file(retained, make_parents=True) as temporary:
                temporary.write_text(svg_text, encoding="utf-8")
        # Each composite ships as one family drawn from one SVG in one run: the vector
        # itself, every PNG raster, and the PDF. Splitting the exports across commands
        # is what would let four of the five be current and the fifth be last week's.
        _update_png_exports(canvas, svg_text)
        render_composite_pdf.update(canvas.spec.stem)
        rasters += len(canvas.rasters)
    findings = composite_findings()
    if findings.problems:
        raise ValueError(
            "composite redraw postflight failed:\n  " + "\n  ".join(findings.problems[:20])
        )
    print(
        f"known-best composites redrawn from {identity.stamp}, data of "
        f"{identity.data_date}: {len(COMPOSITES)} SVG, {rasters} PNG rasters, "
        f"{len(COMPOSITES)} PDF"
    )


def check(workers: int = 1) -> None:
    outputs, manifest = expected_outputs(workers)
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
    # One --check covers every composite family, not just the vectors: each retained
    # composite is redrawn from the rebuilt corpus under its own record and compared,
    # and the rasters and the PDF are exports of one SVG each, each carrying a receipt
    # naming the SVG it was drawn from. Reading four receipts costs nothing next to
    # redrawing a 25-by-30-inch page, and a report that lists every stale export at once
    # beats finding them one command at a time.
    findings = composite_findings(
        lambda canvas, identity: expected_composite(canvas, identity, workers)
    )
    problems.extend(findings.problems)
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
    for note in findings.notes:
        print(note)
    print(
        f"known-best atlas check passed: {CORPUS.count} sources/plans, witnesses, "
        f"renders, {len(COMPOSITES)} composite{_plural(len(COMPOSITES))}, and links"
    )


def _retained_problems(
    *, composite_records: Sequence[dict] | None = None
) -> tuple[list[str], list[dict] | None]:
    """Everything the retained data records say about themselves, checked without geometry.

    This is the half of `check` that does not rebuild a case, and at `n=1..324` it is
    almost free next to the half that does. It still re-derives rather than merely
    re-reads: the source index is rebuilt from the frontier and the catalogue and every
    retained upstream SVG is re-hashed against its declared digest; every manifest field
    but the per-case entries is recomputed and compared to the retained bytes; and every
    frontier record is compared against the link the builder would write into it.

    Returns the problems and, when the manifest is readable and covers the declared
    range, its entries. `None` means the sampled half has nothing to compare against and
    must not run: a missing manifest should be reported as a missing manifest rather than
    as whatever the next reader of it raises. A layout refresh supplies the old
    composite records so this preflight still catches every other manifest discrepancy.
    """
    squish_house.check_houses()
    refinement_houses.check_houses()
    if not MANIFEST.is_file():
        return [f"missing {_relative(MANIFEST)}"], None
    retained = MANIFEST.read_text(encoding="utf-8")
    try:
        entries = list(json.loads(retained)["atlas"]["entries"])
        stated = [int(entry["n"]) for entry in entries]
    except KeyError, TypeError, ValueError:
        return [f"{_relative(MANIFEST)} is not a readable known-best manifest"], None
    if stated != list(CORPUS.numbers):
        return [f"manifest entries are not exactly {CORPUS.label}"], None
    problems: list[str] = []
    composites = (
        list(composite_records)
        if composite_records is not None
        else [_composite_record(canvas) for canvas in resolved_composites(entries)]
    )
    rebuilt = _manifest_document(entries, composites)
    if _manifest_text(rebuilt) != retained:
        problems.append(
            f"stale {_relative(MANIFEST)}: everything but its entries is re-derived here"
        )
    plans = source_plans()
    if not SOURCE_MANIFEST.is_file():
        problems.append(f"missing {_relative(SOURCE_MANIFEST)}")
    elif SOURCE_MANIFEST.read_text(encoding="utf-8") != _json_text(_source_index(plans)):
        problems.append(f"stale {_relative(SOURCE_MANIFEST)}")
    for root, suffix, label in (
        (WITNESS_ROOT, "yaml", "witnesses/known-best"),
        (RENDER_ROOT, "svg", "atlas/known-best/rendering"),
    ):
        expected = {f"n-{n:03d}.{suffix}" for n in CORPUS.numbers}
        present = {path.name for path in root.glob(f"*.{suffix}")} if root.is_dir() else set()
        problems.extend(f"missing {label}/{name}" for name in sorted(expected - present))
        problems.extend(f"unexpected {label}/{name}" for name in sorted(present - expected))
    if KINGBIRD_RAW_ROOT.exists():
        problems.append("raw Kingbird source directory must not be retained")
    for entry in entries:
        case = _frontier_case(int(entry["n"]))
        if case.side != str(entry["reported_side"]):
            problems.append(f"manifest reported_side disagrees with {case.path.name}")
        elif case.text != _frontier_with_witness(case, str(entry["witness"]["id"])):
            problems.append(f"stale {_relative(case.path)}")
    return problems, entries


@dataclass(frozen=True)
class CompositeFindings:
    """What a check of the retained composites found.

    `problems` fail the check. `notes` do not: they say which data each composite shows
    and, where a composite trails the pin, which of its claims have since changed.
    """

    problems: tuple[str, ...]
    notes: tuple[str, ...]


#: A card in a serialized composite: one group at the root's indent, named by its case.
_CARD_START = re.compile(r'^  <g data-feature="packing-card" data-n="(\d+)"', re.MULTILINE)


def _composite_parts(svg_text: str) -> dict[str, str]:
    """A serialized composite, cut into its frame and its cards.

    The frame is everything ahead of the first card: the title, the dateline, the
    legend and the footer. Each card runs to the next, and the last carries the closing
    tag. Two drawings are compared part by part so a difference names the cases it is in.
    """
    marks = list(_CARD_START.finditer(svg_text))
    if not marks:
        return {"the frame": svg_text}
    parts = {"the frame": svg_text[: marks[0].start()]}
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(svg_text)
        parts[f"n={mark.group(1)}"] = svg_text[mark.start() : end]
    return parts


def _redraw_differences(retained: str, redrawn: str) -> list[str]:
    """The parts of a retained composite that a redraw under its own record changes."""
    if retained == redrawn:
        return []
    before, after = _composite_parts(retained), _composite_parts(redrawn)
    differing = [name for name in after if before.get(name) != after[name]]
    differing.extend(name for name in before if name not in after)
    return differing or ["its bytes"]


def _identity_git_problems(path: str, identity: CompositeIdentity) -> list[str]:
    """Hold a composite's record to the repository, wherever git can answer.

    The revision has to be a commit in this history that changed the data, and the date
    has to be that commit's. Nothing is reported where git cannot say -- a source
    tarball, or a shallow clone cut above the commit -- as `test_release` skips there.

    A shallow clone can hold the commit and still not hold its history: the pull
    request's record sweeps check out one commit of a partial clone, which fetches the
    named commit when asked for it and has no ancestry to place it in. There the date is
    still the commit's own, and the two questions that walk history are left to a clone
    that has one (`test_the_retained_composites_agree_with_their_own_records`, in the
    behavioral shards, which fetch all of it).
    """
    revision = identity.data_revision
    shallow = _git_result("rev-parse", "--is-shallow-repository")
    cut = shallow.returncode != 0 or shallow.stdout.strip() == "true"
    found = _git_result("cat-file", "-t", f"{revision}^{{commit}}")
    if found.returncode != 0:
        if cut:
            return []
        return [f"{path} names {revision[:12]} as its data, which is not a commit here"]
    problems = []
    try:
        day = commit_date(REPOSITORY_ROOT, revision)
    except RuntimeError:
        return []
    if day != identity.data_date:
        problems.append(
            f"{path} dates its data {identity.data_date}; {revision[:12]} is dated {day}"
        )
    if cut:
        return problems
    last = _git_result("log", "-1", "--format=%H", revision, "--", *data_pathspec())
    if last.returncode == 0 and last.stdout.strip() != revision:
        problems.append(
            f"{path} names {revision[:12]} as its data, which did not change the data"
        )
    if _git_result("merge-base", "--is-ancestor", revision, "HEAD").returncode == 1:
        problems.append(
            f"{path} names {revision[:12]} as its data, which is not in this history"
        )
    return problems


def composite_findings(
    redraw: Callable[[CompositeCanvas, CompositeIdentity], str] | None = None,
) -> CompositeFindings:
    """Every retained composite, held to its own record, the release and its exports.

    Nothing is rebuilt unless `redraw` is given. What is held, for each composite:

    - it records the data commit and date it was drawn from, and where git can answer
      that is a data commit in this history, of that date;
    - its footer is the edition as it read at that commit and its dateline is that date,
      so a composite drawn for an earlier version fails here until it is redrawn;
    - its canvas is the one its specification computes;
    - every claim printed on a card agrees with the current figure record;
    - with `redraw`, the whole `--check`'s rebuild of the corpus, its bytes are what
      that rebuild draws under the composite's own record;
    - each PNG and the PDF carry the receipt of this SVG.

    The two comparisons with current data are where a composite may trail
    (`sqpack.release`, rule 5). While its data revision is the pin they are failures, as
    they always were: the drawing claims the data every page prints and does not show
    it. Once the pin has moved on they are notes, naming the cards, unless
    `COMPOSITES_MAY_TRAIL` is off.
    """
    problems: list[str] = []
    notes: list[str] = []
    for canvas in resolved_composites():
        path = _relative(canvas.svg_path)
        if not canvas.svg_path.is_file():
            problems.append(f"missing {path}")
            continue
        svg_text = canvas.svg_path.read_text(encoding="utf-8")
        root = ET.fromstring(svg_text)
        if (root.get("width"), root.get("height")) != (str(canvas.width), str(canvas.height)):
            problems.append(f"{path} is not the canvas its specification computes")
        identity: CompositeIdentity | None = None
        try:
            identity = retained_identity(svg_text)
        except ValueError as error:
            problems.append(f"{path} {error}")
        if identity is not None and identity.problems():
            problems.extend(f"{path} {problem}" for problem in identity.problems())
            identity = None
        differing = _composite_label_problems(canvas, root)
        if identity is not None:
            problems.extend(_composite_edition_problems(canvas, root, identity))
            problems.extend(_identity_git_problems(path, identity))
            if redraw is not None:
                parts = _redraw_differences(svg_text, redraw(canvas, identity))
                if parts:
                    shown = ", ".join(parts[:12]) + (" ..." if len(parts) > 12 else "")
                    differing.append(
                        f"{path} is not what a rebuild draws under its own record, in "
                        f"{len(parts)} part{_plural(len(parts))}: {shown}"
                    )
            shows = f"{path} shows {identity.stamp}, data of {identity.data_date}"
            if identity.current:
                notes.append(f"{shows}: the data every page prints")
            else:
                notes.append(
                    f"{shows}; the pin has moved to {DATA_REVISION[:12]}, and the composite "
                    "is redrawn at the next version or by --update-composites"
                )
        if differing and identity is not None and not identity.current and COMPOSITES_MAY_TRAIL:
            notes.append(
                f"{path} trails the data in {len(differing)} "
                f"place{_plural(len(differing))}, which fails nothing until the next version:"
            )
            notes.extend(f"  {line}" for line in differing[:20])
        else:
            problems.extend(differing)
        problems.extend(
            f"missing or stale {export.name} {export.role} receipt"
            for export in canvas.rasters
            if not _png_matches_summary(export, svg_text)
        )
        problems.extend(_composite_pdf_problems(canvas, svg_text))
    return CompositeFindings(tuple(problems), tuple(notes))


def check_composites() -> None:
    """Hold the retained composites to their records, without rebuilding anything.

    The half of the atlas check that concerns the posters, on its own and in seconds:
    what to run after a version bump, after `--update-composites`, or to see how far a
    poster trails the data. The pull-request surface runs it inside `--check --sample`.
    """
    findings = composite_findings()
    if findings.problems:
        raise ValueError(
            "known-best composite drift:\n  " + "\n  ".join(findings.problems[:20])
        )
    for note in findings.notes:
        print(note)
    print(
        f"known-best composites check passed: {len(COMPOSITES)} "
        f"composite{_plural(len(COMPOSITES))} against their own records, the figure "
        "record and their exports"
    )


def _composite_label_problems(canvas: CompositeCanvas, root: ET.Element) -> list[str]:
    """Compare the claims printed on each card with the current figure record."""
    path = _relative(canvas.svg_path)
    entries = _figure_entries()
    cards: dict[int, list[ET.Element]] = {}
    problems: list[str] = []
    for card in root.iter(svg_tag("g")):
        if card.attrib.get("data-feature") != "packing-card":
            continue
        raw_n = card.attrib.get("data-n")
        try:
            n = int(raw_n) if raw_n is not None else None
        except ValueError:
            n = None
        if n is None:
            problems.append(f"{path} has a packing card without an integer data-n")
            continue
        cards.setdefault(n, []).append(card)

    expected_numbers = set(canvas.spec.numbers)
    problems.extend(
        f"{path} has an unexpected packing card for n={n}"
        for n in sorted(set(cards) - expected_numbers)
    )
    for n in canvas.spec.numbers:
        matching = cards.get(n, [])
        if len(matching) != 1:
            problems.append(f"{path} has {len(matching)} packing cards for n={n}; expected 1")
            continue
        entry = entries[n]
        expected = {
            "packing-label": (str(n),),
            "side-bound": (
                _composite_bound_display(
                    str(entry["side"]["display"]),
                    canvas,
                    degree=entry.get("exactness", {}).get("degree"),
                ),
            ),
            "lower-bound": (
                (_composite_bound_display(str(entry["lower"]["display"]), canvas),)
                if entry["lower"]["shown"]
                else ()
            ),
        }
        card = matching[0]
        for feature, expected_text in expected.items():
            actual_text = tuple(
                "".join(node.itertext())
                for node in card.iter(svg_tag("text"))
                if node.attrib.get("data-feature") == feature
            )
            if actual_text != expected_text:
                problems.append(
                    f"{path} n={n} {feature} is {actual_text!r}; expected {expected_text!r}"
                )
    return problems


def _composite_edition_problems(
    canvas: CompositeCanvas, root: ET.Element, identity: CompositeIdentity
) -> list[str]:
    """Compare each mode's visible date and edition with the composite's own record.

    Both say which data the drawing shows. They are held to the record the drawing
    carries, not to the pin, so re-pinning the data revision leaves a composite right;
    and the record's stamp is written with the current version, so a composite drawn for
    an earlier one is wrong here until it is redrawn.
    """
    path = _relative(canvas.svg_path)
    problems: list[str] = []
    expected_lines = (
        (("release", ()), ("release-stamp", (identity.poster_stamp,)))
        if canvas.information_in_corner
        else (("release", (identity.dateline,)), ("release-stamp", (identity.stamp,)))
    )
    for feature, expected in expected_lines:
        actual = tuple(
            "".join(node.itertext())
            for node in root.iter(svg_tag("text"))
            if node.attrib.get("data-feature") == feature
        )
        if actual != expected:
            problems.append(f"{path} {feature} is {actual!r}; expected {expected!r}")
            if feature == "release-stamp" and not any(
                PUBLICATION_VERSION in text for text in actual
            ):
                problems.append(
                    f"{path} was drawn for another version than {PUBLICATION_VERSION}; "
                    "redraw it with --update-composites"
                )
    return problems


def _sample_problems(numbers: Sequence[int], retained: list[dict], workers: int) -> list[str]:
    """Where the retained bytes for the sampled cases differ from a fresh build."""
    entries = {int(entry["n"]): entry for entry in retained}
    problems: list[str] = []
    for built in built_cases(numbers, workers):
        n = built.frontier.n
        for path, expected in (
            (WITNESS_ROOT / f"n-{n:03d}.yaml", built.witness_text),
            (RENDER_ROOT / f"n-{n:03d}.svg", built.rendering_text),
        ):
            if not path.is_file():
                problems.append(f"missing {_relative(path)}")
            elif path.read_text(encoding="utf-8") != expected:
                problems.append(f"stale {_relative(path)}")
        if entries.get(n) != _manifest_entry(built):
            problems.append(f"manifest entry for n={n} is not what a rebuild produces")
    return problems


def check_sample(stride: int = ATLAS_SAMPLE_STRIDE, workers: int = 1) -> None:
    """The pull request's stand-in for the whole rebuild, and what it does not cover.

    `check` re-derives all 324 cases and both composites and compares every byte, and at
    the widened corpus that is 691.19s of a 703.28s step -- measured on 2026-09-07 and
    retained in `benchmarks/gate-cost-at-324/`, which is why the whole rebuild moved to
    the deferred surface. This runs all of the cheap half and a sampled slice of the
    expensive one, so a pull request still fails on the drift `D-369` counts -- a
    registry, a generated view or a declared contract going stale -- in the minute it is
    introduced rather than after the merge.

    What it does not cover, stated so nobody has to infer it: the per-case geometry of
    the cases the stride skips, and the composite SVGs' own bytes beyond their canvas,
    visible claim labels, dateline, version stamp and record of the data they were drawn
    from, and export receipts (`composite_findings`). Both are
    covered by `known-best n=1..324 atlas rebuild` on the deferred surface, which is the
    exact complement
    `test_the_deep_gate_runs_exactly_what_the_pull_request_surface_defers` holds.
    """
    numbers = sampled_numbers(CORPUS, stride)
    problems, entries = _retained_problems()
    findings = composite_findings()
    problems.extend(findings.problems)
    if entries is not None:
        problems.extend(_sample_problems(numbers, entries, workers))
    if problems:
        raise ValueError("known-best atlas drift:\n  " + "\n  ".join(problems[:20]))
    for note in findings.notes:
        print(note)
    print(
        f"known-best atlas sample check passed: {len(numbers)} of {CORPUS.count} cases "
        f"rebuilt (every {stride}th from n={CORPUS.first_n}), {CORPUS.count} manifest "
        f"entries, sources, links, and {len(COMPOSITES)} "
        f"composite{_plural(len(COMPOSITES))}"
    )


def summary_square_polygons(root: ET.Element) -> list[ET.Element]:
    """Every square polygon in a composite, under either encoding.

    A composite that carries per-square `data-*` names each polygon `square-fill`; one
    that has dropped them names the group instead, and the polygons inside it are the
    squares. Reading both is what lets one measurement, and one test, cover both
    families rather than one per encoding. The star a card may carry is a polygon too
    and is not a square, which is why this asks what a polygon is rather than counting
    the tag.
    """
    squares = [
        node
        for node in root.iter(svg_tag("polygon"))
        if node.attrib.get("data-feature") == "square-fill"
    ]
    for group in root.iter(svg_tag("g")):
        if group.attrib.get("data-feature") == "square-fills":
            squares.extend(group.iter(svg_tag("polygon")))
    return squares


def _encoding_summary(composite: CompositeSpec) -> str:
    """How one composite encodes a square, in one line of a report."""
    return "; ".join(
        (
            "per-square data-* "
            + ("carried" if composite.square_data_attributes else "omitted"),
            "stroke "
            + ("shared per card" if composite.square_stroke_shared else "per polygon"),
            "coordinates "
            + (
                f"rounded to {composite.coordinate_decimals} decimals"
                if composite.coordinate_decimals is not None
                else f"at the renderer's {SVG_EMISSION_PRECISION} significant digits"
            ),
        )
    )


def report() -> None:
    """Measure what each retained composite costs, rather than estimating it.

    The byte budget is the reason this exists. The house encoding spends about 460 bytes
    on every square it draws, which a figure of five thousand squares carries without
    comment and a poster of fifty-two thousand cannot: the same encoding would have made
    `known-best-1-324.svg` a 24 MB file. Every lever that brought it down was chosen
    against these numbers and can be re-measured against them, which is `OR-1` -- the
    measurement is a command, not a paragraph someone wrote once.

    Retained bytes, deliberately, not a rebuild: this reports the artifacts a clone
    actually pays for. `--check` is what says they are current.
    """
    print(f"known-best composites: {len(COMPOSITES)}")
    for canvas in resolved_composites():
        composite = canvas.spec
        print(f"\n{composite.stem}  {composite.layout}")
        print(f"  encoding: {_encoding_summary(composite)}")
        svg_path = canvas.svg_path
        if not svg_path.is_file():
            print(f"  {'(missing)':>14}  {_relative(svg_path)}")
            continue
        svg_bytes = svg_path.stat().st_size
        polygons = len(summary_square_polygons(ET.fromstring(svg_path.read_text("utf-8"))))
        print(
            f"  {svg_bytes:>14,}  {_relative(svg_path)}  {canvas.width}x{canvas.height} units"
        )
        print(
            f"  {'':>14}  {polygons:,} square polygons, "
            f"{svg_bytes / composite.square_count:.1f} bytes per square"
        )
        if polygons != composite.square_count:
            print(f"  {'':>14}  polygons disagree with {composite.square_count:,} declared")
        for export in canvas.rasters:
            size = f"{export.path.stat().st_size:,}" if export.path.is_file() else "(missing)"
            print(f"  {size:>14}  {export.name}  {export.width}x{export.height} px")
        pdf = render_composite_pdf.composite_pdf(composite.stem)
        size = f"{pdf.stat().st_size:,}" if pdf.is_file() else "(missing)"
        print(f"  {size:>14}  atlas/known-best/{pdf.name}")


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
    mode.add_argument(
        "--update",
        action="store_true",
        help="regenerate the data layer: witnesses, renderings, manifest, frontier links",
    )
    mode.add_argument(
        "--update-composite-records",
        action="store_true",
        help="refresh composite layout records without rebuilding witnesses; "
        "refuse changes to case facts before writing either record",
    )
    mode.add_argument(
        "--update-composites",
        action="store_true",
        help="redraw both composites and their PNG and PDF exports from the retained "
        "witnesses: at a version bump, or on demand",
    )
    mode.add_argument(
        "--check", action="store_true", help="compare retained outputs to a rebuild"
    )
    mode.add_argument(
        "--check-composites",
        action="store_true",
        help="hold the retained composites to their own records, the figure record and "
        "their exports, rebuilding nothing",
    )
    mode.add_argument(
        "--smoke", action="store_true", help="build corpus into a temporary directory"
    )
    mode.add_argument(
        "--report",
        action="store_true",
        help="measure each retained composite: bytes, squares, bytes per square",
    )
    command.add_argument(
        "--refresh",
        action="store_true",
        help="with --fetch, replace already retained assets from their recorded URLs",
    )
    command.add_argument(
        "--sample",
        action="store_true",
        help=(
            f"with --check, re-derive the whole record layer but rebuild only every "
            f"{ATLAS_SAMPLE_STRIDE}th case, which is what the pull-request surface runs"
        ),
    )
    command.add_argument(
        "--n",
        type=int,
        nargs="+",
        metavar="N",
        help="with --update, refresh only these counts and preserve the retained remainder",
    )
    command.add_argument(
        "--jobs",
        type=int,
        metavar="N",
        default=None,
        help=(
            "processes to build the corpus with; the default follows the PACK_JOBS cap "
            "the gate exports, and the whole machine when there is no gate"
        ),
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.refresh and not args.fetch:
        raise SystemExit("--refresh requires --fetch")
    if args.sample and not args.check:
        raise SystemExit("--sample narrows --check")
    if args.n is not None and not args.update:
        raise SystemExit("--n narrows --update")
    if args.jobs is not None and args.jobs < 1:
        raise SystemExit("--jobs must be positive")
    # The count is resolved here and nowhere else: `worker_count` reads the machine when
    # no gate has capped it, and an in-process caller must not inherit that -- see
    # `expected_outputs`.
    workers = worker_count(CORPUS.count) if args.jobs is None else args.jobs
    if args.fetch:
        fetch_sources(refresh=args.refresh)
    elif args.update:
        update_selected(args.n, workers) if args.n is not None else update(workers)
    elif args.update_composite_records:
        update_composite_records()
    elif args.update_composites:
        update_composites()
    elif args.check_composites:
        check_composites()
    elif args.check:
        check_sample(workers=workers) if args.sample else check(workers)
    elif args.report:
        report()
    else:
        smoke_in_temporary_directory()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
