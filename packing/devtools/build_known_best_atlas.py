#!/usr/bin/env python3
"""Acquire, normalize, validate, and render the known-best ``n = 1..100`` atlas."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zlib
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
    RETRIEVED_DATE,
    UNITSQUARE_BASE_URL,
    catalogue_source_map,
    exact_grid_witness,
    kingbird_derived_witness,
    parse_unitsquare_svg,
    rational_integer,
    unitsquare_witness,
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
    emission_precision,
    format_svg_number,
    scalar_from_decimal,
    scalar_from_fraction,
)
from sqpack.render.style import LABEL_MUTED_COLOR, PAPER_THEME
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
SUMMARY_SVG = ATLAS_ROOT / "known-best-1-100.svg"
SUMMARY_PNG = ATLAS_ROOT / "known-best-1-100.png"
GENERATOR = "python -m devtools.build_known_best_atlas"
USER_AGENT = "thinking-scratchpad-known-best-atlas/1.0"

SUMMARY_WIDTH = 2400
SUMMARY_HEIGHT = 2676
SUMMARY_FIRST_N = 1
SUMMARY_LAST_N = 100
SUMMARY_COLUMNS = 10
SUMMARY_ROWS = 10
SUMMARY_SQUARE_COUNT = sum(range(SUMMARY_FIRST_N, SUMMARY_LAST_N + 1))
SUMMARY_GRID_LEFT = Decimal(60)
SUMMARY_GRID_TOP = Decimal(152)
SUMMARY_COLUMN_PITCH = Decimal(228)
SUMMARY_ROW_PITCH = Decimal(235)
SUMMARY_CARD_WIDTH = Decimal(216)
SUMMARY_CARD_HEIGHT = Decimal(225)
SUMMARY_PACKING_SIZE = Decimal(158)
SUMMARY_PACKING_INSET_X = Decimal(24)
SUMMARY_PACKING_INSET_Y = Decimal(12)
SUMMARY_LABEL_BASELINE = Decimal(203)
SUMMARY_BOUND_BASELINE = Decimal(220)
SUMMARY_BADGE_SIZE = Decimal(19)
SUMMARY_EXPLAINER_BASELINE = Decimal(2614)
SUMMARY_CREDIT_BASELINE = Decimal(2652)
SUMMARY_EXPLAINER = (
    "s(n) is the side of the smallest square holding n unit squares; "
    "deg is the algebraic degree of that side length"
)
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
SUMMARY_LEGEND_ROW_PITCH = Decimal(32)
# Helvetica offers regular and bold and nothing between, so there is no semibold
# to ask for: the card labels take bold, the only heavier face available, over a
# darker grey. The footer block stays regular so the two do not compete.
SUMMARY_SMALL_WEIGHT = "700"
SUMMARY_SMALL_FILL = LABEL_MUTED_COLOR
# Letters sit on their cap height, math symbols on the math axis, so a single
# baseline cannot center both inside the badge box. Offsets are from the box top.
SUMMARY_BADGE_FONT_SIZE = Decimal(15)
SUMMARY_GLYPH_BASELINE = {"O": Decimal("14.9")}
SUMMARY_MATH_GLYPH_BASELINE = Decimal(14)
SUMMARY_CREDIT = "Diagram by Joshua Levy with assistance from Claude and Codex"
SUMMARY_REPOSITORY = "github.com/jlevy/squares"
# Set a step above the other small labels so the URL reads as part of the
# heading block rather than as another footnote.
SUMMARY_REPOSITORY_SIZE = "26"
SUMMARY_SUBTITLE_BASELINE = Decimal(126)
SUMMARY_LEGEND_BASELINE = Decimal(2540)
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


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


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
        for n in range(1, 101)
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


def _append_summary_card(root: ET.Element, built: BuiltCase, *, spec: RenderSpec) -> None:
    n = built.frontier.n
    row, column = divmod(n - SUMMARY_FIRST_N, SUMMARY_COLUMNS)
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
            "stroke": PAPER_THEME.container,
            "stroke-width": "1.15",
            "vector-effect": "non-scaling-stroke",
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
                "vector-effect": "non-scaling-stroke",
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
    display = _figure_entries()[n]["side"]["display"]
    sub(bound, "tspan", {"font-style": "italic"}).text = "s"
    sub(bound, "tspan", {}).text = display[1:]

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
    entry = _figure_entries()[built.frontier.n]
    return tuple(
        (badge["glyph"], badge["style"], badge["meaning"]) for badge in entry["badges"]
    )


def _append_badge(
    parent: ET.Element, glyph: str, style: str, label: str, *, x: Decimal, top: Decimal
) -> None:
    """Draw one badge at an explicit box top.

    Callers position the box rather than passing a text baseline, so the card can
    sit its badges flush with the top of the big number.
    """
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
            "y": format_svg_number(
                top + SUMMARY_GLYPH_BASELINE.get(glyph, SUMMARY_MATH_GLYPH_BASELINE)
            ),
            "text-anchor": "middle",
            "font-family": SUMMARY_FONT,
            "font-size": format_svg_number(SUMMARY_BADGE_FONT_SIZE),
            "font-weight": "650",
            "fill": glyph_fill,
        },
    ).text = glyph


def _legend_row(
    legend: ET.Element, entries: list[tuple[object, str]], *, baseline: Decimal
) -> None:
    """Lay one centerd legend row.

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
        Decimal(SUMMARY_WIDTH) - sum(widths, Decimal(0)) - gap * Decimal(len(entries) - 1)
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
    root: ET.Element, built: list[BuiltCase], *, spec: RenderSpec
) -> None:
    """Two rows: what the badges assert, then what color and shade encode."""
    totals = load_figure_record()["totals"]
    tally = {
        "proved optimal": totals["proved_optimal"],
        "exact value known": totals["exact_value_known"],
        "only known numerically": totals["only_known_numerically"],
        "rigid (established)": totals["rigidity_established"],
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
        ("R", "solid", "rigid (established)"),
    ]
    _legend_row(
        legend,
        [(badge, f"{badge[2]} ({tally.get(badge[2], 0)})") for badge in badges],
        baseline=SUMMARY_LEGEND_BASELINE,
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
        baseline=SUMMARY_LEGEND_BASELINE + SUMMARY_LEGEND_ROW_PITCH,
    )


@emission_precision()
def render_known_best_summary_svg(built: list[BuiltCase]) -> str:
    """Render a complete, zoomable 10 by 10 overview of ``n = 1..100``.

    The pin covers the per-card scale and corner arithmetic in `_append_summary_card`
    and `_summary_points`, which is its own Decimal work rather than the house
    renderer's, and so would otherwise track whatever precision the process was left in.
    """
    numbers = [item.frontier.n for item in built]
    if numbers != list(range(SUMMARY_FIRST_N, SUMMARY_LAST_N + 1)):
        raise ValueError("known-best summary requires exactly n=1..100 in order")
    spec = RenderSpec(overlays=frozenset())
    root = element(
        "svg",
        {
            "width": str(SUMMARY_WIDTH),
            "height": str(SUMMARY_HEIGHT),
            "viewBox": f"0 0 {SUMMARY_WIDTH} {SUMMARY_HEIGHT}",
            "role": "img",
            "aria-labelledby": "figure-title figure-description",
        },
    )
    append_title_desc(
        root,
        "Best known packings of one through one hundred unit squares",
        (
            "A ten-by-ten atlas of the retained best known unit-square packings for "
            "n equals 1 through 100. Each tile is normalized to its own container and "
            "labeled with n and the best known upper bound on the container side. Badges "
            "mark which side lengths are proved optimal, and whether a side length is "
            "pinned exactly by a radical or a minimal polynomial rather than only by a "
            "decimal."
        ),
    )
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
            "columns": str(SUMMARY_COLUMNS),
            "first-n": str(SUMMARY_FIRST_N),
            "generated-by": GENERATOR,
            "last-n": str(SUMMARY_LAST_N),
            "rows": str(SUMMARY_ROWS),
            "square-count": str(SUMMARY_SQUARE_COUNT),
        },
    )
    sub(
        root,
        "rect",
        {
            "width": str(SUMMARY_WIDTH),
            "height": str(SUMMARY_HEIGHT),
            "fill": PAPER_THEME.background,
        },
    )
    heading_x = str(SUMMARY_WIDTH // 2)
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
    ).text = "100 BEST KNOWN SQUARE PACKINGS"
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
            "fill": PAPER_THEME.muted,
        },
    ).text = SUMMARY_REPOSITORY
    _append_summary_legend(root, built, spec=spec)
    sub(
        root,
        "text",
        {
            "data-feature": "explainer",
            "x": str(SUMMARY_WIDTH // 2),
            "y": format_svg_number(SUMMARY_EXPLAINER_BASELINE),
            "text-anchor": "middle",
            "font-family": SUMMARY_FONT,
            "font-size": SUMMARY_FOOTER_SIZE,
            "font-weight": SUMMARY_SMALL_WEIGHT,
            "fill": SUMMARY_SMALL_FILL,
        },
    ).text = SUMMARY_EXPLAINER
    sub(
        root,
        "text",
        {
            "data-feature": "credit",
            "x": str(SUMMARY_WIDTH // 2),
            "y": format_svg_number(SUMMARY_CREDIT_BASELINE),
            "text-anchor": "middle",
            "font-family": SUMMARY_FONT,
            "font-size": SUMMARY_FOOTER_SIZE,
            "font-weight": SUMMARY_SMALL_WEIGHT,
            "fill": SUMMARY_SMALL_FILL,
        },
    ).text = SUMMARY_CREDIT
    for item in built:
        _append_summary_card(root, item, spec=spec)
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


def _png_matches_summary(path: Path, svg_text: str) -> bool:
    if not path.is_file():
        return False
    try:
        width, height, source_sha256 = png_summary_receipt(path.read_bytes())
    except UnicodeDecodeError, ValueError:
        return False
    expected_sha256 = hashlib.sha256(svg_text.encode("utf-8")).hexdigest()
    return (width, height, source_sha256) == (
        SUMMARY_WIDTH,
        SUMMARY_HEIGHT,
        expected_sha256,
    )


def _update_png_preview(svg_text: str) -> None:
    if _png_matches_summary(SUMMARY_PNG, svg_text):
        return
    sips = shutil.which("sips") if sys.platform == "darwin" else None
    renderer = sips or shutil.which("magick")
    if renderer is None:
        raise RuntimeError("PNG preview generation requires sips or ImageMagick")
    with TemporaryDirectory() as directory:
        temporary_png = Path(directory) / SUMMARY_PNG.name
        if Path(renderer).name == "sips":
            command = [
                renderer,
                "-s",
                "format",
                "png",
                str(SUMMARY_SVG),
                "--out",
                str(temporary_png),
            ]
        else:
            command = [
                renderer,
                str(SUMMARY_SVG),
                "-background",
                "white",
                "-alpha",
                "remove",
                "-alpha",
                "off",
                f"PNG24:{temporary_png}",
            ]
        try:
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=PNG_RENDER_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as error:
            raise RuntimeError(
                f"PNG preview renderer timed out after {PNG_RENDER_TIMEOUT_SECONDS} seconds"
            ) from error
        except subprocess.CalledProcessError as error:
            detail = (error.stderr or error.stdout or "no diagnostic output").strip()
            raise RuntimeError(
                f"PNG preview renderer exited {error.returncode}: {detail[-2000:]}"
            ) from error
        content = _png_with_summary_source(
            temporary_png.read_bytes(), hashlib.sha256(svg_text.encode("utf-8")).hexdigest()
        )
        width, height, _source_sha256 = png_summary_receipt(content)
        if (width, height) != (SUMMARY_WIDTH, SUMMARY_HEIGHT):
            raise ValueError(
                f"PNG preview dimensions are {width}x{height}; expected "
                f"{SUMMARY_WIDTH}x{SUMMARY_HEIGHT}"
            )
        with atomic_output_file(SUMMARY_PNG, make_parents=True) as temporary:
            temporary.write_bytes(content)


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


@cache
def _expected_outputs() -> tuple[dict[Path, str], dict]:
    plans = source_plans()
    source_index = _source_index(plans)
    built = [_build_case(n, plans[n]) for n in range(1, 101)]
    outputs: dict[Path, str] = {SOURCE_MANIFEST: _json_text(source_index)}
    for item in built:
        n = item.frontier.n
        outputs[WITNESS_ROOT / f"n-{n:03d}.yaml"] = item.witness_text
        outputs[RENDER_ROOT / f"n-{n:03d}.svg"] = item.rendering_text
        outputs[item.frontier.path] = _frontier_with_witness(
            item.frontier, str(item.witness["id"])
        )
    outputs[SUMMARY_SVG] = render_known_best_summary_svg(built)
    manifest = {
        "softschema": {
            "contract": "packing.squares:KnownBestAtlas/v1",
            "schema": "known-best-atlas.schema.yaml",
            "envelope": "atlas",
            "status": "enforced",
        },
        "atlas": {
            "range": {"first_n": 1, "last_n": 100, "count": 100},
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
            "composite": {
                "layout": "10 by 10, row-major n=1..100",
                "png_preview": {
                    "derived_from": "atlas/known-best/known-best-1-100.svg",
                    "height": SUMMARY_HEIGHT,
                    "path": "atlas/known-best/known-best-1-100.png",
                    "width": SUMMARY_WIDTH,
                },
                "renderer": "sqpack deterministic composite renderer",
                "square_count": SUMMARY_SQUARE_COUNT,
                "svg": {
                    "height": SUMMARY_HEIGHT,
                    "path": "atlas/known-best/known-best-1-100.svg",
                    "width": SUMMARY_WIDTH,
                },
            },
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
    _update_png_preview(outputs[SUMMARY_SVG])
    render_composite_pdf.update()
    print(
        "known-best atlas updated: 100 witnesses, 100 house renderings, "
        "1 composite, 100 frontier links"
    )


def check() -> None:
    outputs, manifest = expected_outputs()
    problems = []
    for path, expected in sorted(outputs.items(), key=lambda item: item[0].as_posix()):
        if not path.is_file():
            problems.append(f"missing {_relative(path)}")
        elif path.read_text(encoding="utf-8") != expected:
            problems.append(f"stale {_relative(path)}")
    expected_witnesses = {f"n-{n:03d}.yaml" for n in range(1, 101)}
    expected_renderings = {f"n-{n:03d}.svg" for n in range(1, 101)}
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
    if not _png_matches_summary(SUMMARY_PNG, outputs[SUMMARY_SVG]):
        problems.append(
            "missing or stale atlas/known-best/known-best-1-100.png preview receipt"
        )
    entries = manifest["atlas"]["entries"]
    if [entry["n"] for entry in entries] != list(range(1, 101)):
        problems.append("manifest entries are not exactly n=1..100")
    if problems:
        raise ValueError("known-best atlas drift:\n  " + "\n  ".join(problems[:20]))
    print(
        "known-best atlas check passed: 100 sources/plans, witnesses, renders, "
        "1 composite, and links"
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


def main(argv: list[str] | None = None) -> int:
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
