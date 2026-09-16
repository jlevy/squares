"""Reserve the published page's math geometry using its actual fonts and cascade.

KaTeX's HTML has measured vertical struts, but its glyph runs still have intrinsic
width. A hidden TeX or MathML fallback therefore cannot reserve the final layout.
The publication build typesets each supported font preference in pinned Chromium and
measures each unbreakable ``.base`` separately. The host requires linear glyph advances,
using ``geometricPrecision`` except where macOS provides them with native hinting.
A second measurement at 16
times the font size checks that the saved em width scales within one CSS pixel.
Its fixed outer box keeps that width,
height, and baseline while
the selectable HTML inside waits for its fonts. Keeping separate bases preserves
KaTeX's line-break opportunities and leaves glyph ink free to overhang the box.

Only selected math slots are copied back into the pristine source. Canvas state,
tooltips, observer mutations, and the browser's serialization of the page stay out of
the published file. The caller is the only writer; ordinary ``render()`` needs no
browser, while ``render_explainer --prepare-math`` produces the publication artifact.

The shared font and hydration contract is documented at
``vendor/kpress/docs/project/architecture/arch-2026-09-08-font-and-math-loading.md``
(repository-relative). This module adds only the host's measured publication geometry.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import json
import os
import re
import sys
import time
from contextlib import suppress
from dataclasses import dataclass
from datetime import UTC, datetime
from html import escape
from html.parser import HTMLParser
from io import BytesIO
from itertools import pairwise
from pathlib import Path
from typing import TYPE_CHECKING, Any, NotRequired, TypedDict, cast, override

if TYPE_CHECKING:
    from playwright.async_api import Route

from devtools.check_math_loading import MATH_LIBRARY, OBSERVATION_MS
from devtools.render_explainer_pdf import BROWSER_OVERRIDE, PAGE, READY, SETTLED
from sqpack.probes import applied, probe

_MATH_CLASSES = frozenset({"tex", "tex-d", "kpress-math"})
_READOUT_ID = re.compile(r"(?:mv|md|kval|s-(?:phi|theta|d|D|B|prod))-\d+-\d+\Z")
_VOID_TAGS = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
)
_MATH_ATTRIBUTES = frozenset(
    {
        "data-kpress-math-source",
        "data-kpress-math-display",
        "data-kpress-math-profile",
        "data-kpress-math-prepared",
        "data-kpress-math-face",
        "data-kpress-math-rendered",
    }
)
_MARKER = "data-squares-math-key"
_FONT_CONTEXTS = tuple(
    (font_set, prose_font)
    for font_set in ("custom", "system")
    for prose_font in ("serif", "sans")
)

#: The probes this module hands the page, one file each under `probes/`.
PROBES = Path(__file__).resolve().parent / "probes"


@dataclass(frozen=True)
class MathSlot:
    """Source offsets let the browser replace math without reserializing its context."""

    start: int
    content_start: int
    content_end: int
    end: int


class PreparedFragment(TypedDict):
    key: int
    html: str
    attributes: dict[str, str]


class _MathSlots(HTMLParser):
    def __init__(self, source: str) -> None:
        super().__init__(convert_charrefs=False)
        self.source = source
        self.line_offsets = [0, *[match.end() for match in re.finditer("\n", source)]]
        self.stack: list[tuple[str, tuple[int, int] | None]] = []
        self.slots: list[MathSlot] = []

    def absolute_offset(self) -> int:
        line, column = self.getpos()
        return self.line_offsets[line - 1] + column

    @override
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _VOID_TAGS:
            return
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        identifier = attributes.get("id") or ""
        selected = bool(classes & _MATH_CLASSES or _READOUT_ID.fullmatch(identifier))
        outer_selected = any(slot is not None for _, slot in self.stack)
        slot = None
        if selected and not outer_selected:
            start = self.absolute_offset()
            slot = (start, start + len(self.get_starttag_text() or ""))
        self.stack.append((tag, slot))

    @override
    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # A self-closing MathML/SVG child cannot own one of the selected HTML slots.
        pass

    @override
    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] != tag:
                continue
            _, slot = self.stack[index]
            del self.stack[index:]
            if slot is not None:
                start, content_start = slot
                content_end = self.absolute_offset()
                end = self.source.index(">", content_end) + 1
                self.slots.append(MathSlot(start, content_start, content_end, end))
            return


def math_slots(source: str) -> list[MathSlot]:
    """Find top-level formula/readout slots, ignoring examples inside scripts."""
    parser = _MathSlots(source)
    parser.feed(source)
    parser.close()
    if any(slot is not None for _, slot in parser.stack):
        raise ValueError("an explainer math slot has no closing tag")
    return sorted(parser.slots, key=lambda slot: slot.start)


def prepared_html(source: str, slots: list[MathSlot], fragments: list[PreparedFragment]) -> str:
    """Apply a complete, math-only extraction to the original HTML."""
    keyed = {fragment["key"]: fragment for fragment in fragments}
    if len(keyed) != len(fragments) or set(keyed) != set(range(len(slots))):
        raise ValueError("the browser must return every math slot exactly once")
    result = source
    for index in reversed(range(len(slots))):
        slot, fragment = slots[index], keyed[index]
        unknown = fragment["attributes"].keys() - _MATH_ATTRIBUTES
        if unknown:
            raise ValueError(
                f"the math extraction returned a non-math attribute: {sorted(unknown)}"
            )
        opening = source[slot.start : slot.content_start]
        additions = "".join(
            f' {name}="{escape(value, quote=True)}"'
            for name, value in sorted(fragment["attributes"].items())
        )
        replacement = opening[:-1] + additions + ">" + fragment["html"]
        replacement += source[slot.content_end : slot.end]
        result = result[: slot.start] + replacement + result[slot.end :]
    return result


#: A reference probe: it returns the slot measurement, which carries its measurement of one
#: base as `linearGeometry`. A probe that needs either takes a handle to it in its argument.
_MEASURE_MATH_REFERENCE = probe(PROBES, "prepare_explainer_math/measure_math")

#: The slot measurement itself, called with the sorted math attribute names.
_MEASURE_MATH = applied(_MEASURE_MATH_REFERENCE)


_COMBINE_MATH_VARIANTS = probe(PROBES, "prepare_explainer_math/combine_math_variants")
_FONT_PREFERENCES = probe(PROBES, "prepare_explainer_math/font_preferences")
_REVEAL_CERTIFICATES = probe(PROBES, "prepare_explainer_math/reveal_certificates")


def font_preference_html(source: str, *, prose_font: str, font_set: str) -> str:
    """Set the same pre-paint attributes as saved preferences in a fresh browser."""
    if (font_set, prose_font) not in _FONT_CONTEXTS:
        raise ValueError("unsupported explainer font preferences")
    return _head_script(
        source, applied(_FONT_PREFERENCES, {"proseFont": prose_font, "fontSet": font_set})
    )


def prepare_math_html(source: str) -> str:
    """Return publication HTML with measured math boxes; never write an artifact."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    slots = math_slots(source)
    if any(
        re.search(
            r"\bdata-kpress-math-prepared\s*=\s*[\"\']true[\"\']",
            source[slot.start : slot.end],
        )
        for slot in slots
    ):
        raise ValueError("math preparation expects pristine renderer output")
    if not slots:
        raise ValueError("the explainer contains no math slots to prepare")
    instrumented = source
    for key in reversed(range(len(slots))):
        position = slots[key].content_start - 1
        instrumented = instrumented[:position] + f' {_MARKER}="{key}"' + instrumented[position:]
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            contexts: list[dict[str, object]] = []
            page = None
            for font_set, prose_font in _FONT_CONTEXTS:
                if page is not None:
                    page.close()
                page = browser.new_page(viewport={"width": 1280, "height": 960})
                page.emulate_media(
                    media="screen", reduced_motion="reduce", color_scheme="light"
                )
                page.route("**/*", lambda route: route.abort())
                page.set_content(
                    font_preference_html(
                        instrumented, prose_font=prose_font, font_set=font_set
                    ),
                    wait_until="load",
                )
                page.wait_for_selector(READY, timeout=60_000)
                page.evaluate(_REVEAL_CERTIFICATES)
                page.evaluate(SETTLED)
                contexts.append(
                    {
                        "name": f"{font_set}-{prose_font}",
                        "fragments": page.evaluate(_MEASURE_MATH, sorted(_MATH_ATTRIBUTES)),
                    }
                )
            assert page is not None
            fragments = cast(
                "list[PreparedFragment]",
                page.evaluate(
                    _COMBINE_MATH_VARIANTS,
                    {"contexts": contexts, "attributeNames": sorted(_MATH_ATTRIBUTES)},
                ),
            )
        finally:
            browser.close()
    return prepared_html(source, slots, fragments)


class GeometryBox(TypedDict):
    key: int
    group: int
    x: float
    y: float
    width: float
    height: float
    baseline: float
    intrinsic_width: float
    hidden: bool
    text: NotRequired[str]
    font_size: NotRequired[float]
    text_rendering: NotRequired[str]
    native_linear_metrics: NotRequired[bool]


class GeometryReport(TypedDict):
    browser: str
    width: int
    medium: str
    alternate_certificate: bool
    prose_font: str
    font_set: str
    held_fonts: int
    font_timing: FontHoldTiming
    visibility_after: NotRequired[dict[str, object]]
    before: list[GeometryBox]
    after: list[GeometryBox]
    early_visible: list[ReadyMathBox]
    coverage_before: MathCoverage
    coverage_after: MathCoverage
    environment: BrowserEnvironment
    source_identity: PageIdentity
    findings: list[str]


class MathFontRejection(TypedDict):
    source: str
    elapsed_ms: float
    reason: str


class FontRequestTrace(TypedDict):
    time_origin_ms: float
    first_math_request_ms: float | None
    root_watchdog_paused: bool
    rejections: list[MathFontRejection]


class FontHoldTiming(TypedDict):
    first_math_request_ms: float | None
    first_font_request_ms: float | None
    root_watchdog_paused: bool
    release_started_ms: float
    release_completed_ms: float
    held_ms: float | None
    release_ms: float
    rejections: list[MathFontRejection]


class MathCoverage(TypedDict):
    targets: int
    formulas: int
    bases: int
    missing: list[str]
    unreserved: list[str]
    variant_errors: list[str]
    duplicate_ids: list[str]


class BrowserEnvironment(TypedDict):
    browser: str
    browser_version: str
    viewport: dict[str, int]
    media: str
    recorded_at: str


class PageIdentity(TypedDict):
    title: str
    publication_date: str | None
    revision_url: str | None


class LoadedFace(TypedDict):
    family: str
    status: str


class DeclaredFace(LoadedFace):
    style: str
    weight: str
    unicode_range: str


class GlyphRequest(TypedDict):
    spec: str
    text: str
    check: bool
    faces: list[LoadedFace]
    declared_faces: list[DeclaredFace]


class ReadyMathBox(TypedDict):
    key: int
    source: str
    requests: list[GlyphRequest]


def geometry_findings(
    before: list[GeometryBox],
    after: list[GeometryBox],
    *,
    root_watchdog_paused: bool,
    tolerance: float = 1.0,
    early_ready: frozenset[int] = frozenset(),
    exposed_early: frozenset[int] | None = None,
) -> list[str]:
    """Compare the same boxes and their line breaks across actual font arrival.

    `exposed_early` and `early_ready` describe the same observation: the boxes visible
    when their font evidence was gathered. Keeping those sets together prevents a later
    probe state from changing the exposure question. The root-watchdog flag separately
    proves that the artificial setup did not consume the page's recovery timeout.
    """
    findings: list[str] = []
    if not root_watchdog_paused:
        findings.append("the geometry probe did not pause the root math watchdog")
    old = {box["key"]: box for box in before}
    new = {box["key"]: box for box in after}
    if not old or old.keys() != new.keys():
        findings.append("prepared math boxes disappeared or were never measured")
    exposed = (
        exposed_early
        if exposed_early is not None
        else frozenset(box["key"] for box in before if not box["hidden"])
    )
    if before and exposed - early_ready:
        findings.append("math was exposed while its font requests were held")
    if before and not any(box["hidden"] for box in before):
        findings.append("no hidden prepared math was observed before fonts arrived")
    if not after or any(box["hidden"] for box in after):
        findings.append("prepared math did not become visible after fonts arrived")
    for box in after:
        rendering = box.get("text_rendering", "geometricPrecision").lower()
        if rendering != "geometricprecision" and not (
            rendering == "auto" and box.get("native_linear_metrics", False)
        ):
            findings.append(f"base {box['key']}: math does not use linear glyph metrics")
        delta = abs(box["width"] - box["intrinsic_width"])
        if delta > tolerance:
            findings.append(
                f"base {box['key']}: reserved width differs from glyphs by {delta:.3f}px"
            )
    for key in old.keys() & new.keys():
        for dimension in ("x", "y", "width", "height", "baseline"):
            delta = abs(float(new[key][dimension]) - float(old[key][dimension]))
            if delta > tolerance:
                findings.append(f"base {key}: {dimension} moved {delta:.3f}px")
    for group in {box["group"] for box in before}:
        previous = [box for box in before if box["group"] == group]
        current = [box for box in after if box["group"] == group]
        old_breaks = [
            abs(b["baseline"] - a["baseline"]) > tolerance for a, b in pairwise(previous)
        ]
        new_breaks = [
            abs(b["baseline"] - a["baseline"]) > tolerance for a, b in pairwise(current)
        ]
        if old_breaks != new_breaks:
            findings.append(f"formula {group}: line wrapping changed")
    return findings


_FONT_BLOCK = re.compile(r"@font-face\s*\{[^}]*\}", re.IGNORECASE)
_FONT_DATA = re.compile(r"data:[^;,]+;base64,([A-Za-z0-9+/=]+)")
_FONT_URL = "https://squares-math.invalid/"


def held_math_fonts(source: str) -> tuple[str, dict[str, bytes]]:
    """Make only math-font transfers controllable; prose fonts keep their real bytes."""
    fonts: dict[str, bytes] = {}

    def replace(block: re.Match[str]) -> str:
        css = block.group()
        family = re.search(r"font-family\s*:\s*([^;]+)", css, re.IGNORECASE)
        if not family:
            return css
        name = family.group(1).strip().strip("\"'")
        if not name.startswith(("KaTeX_", "KPress Math Text")):
            return css

        def externalize(data: re.Match[str]) -> str:
            url = f"{_FONT_URL}{len(fonts)}.woff2"
            fonts[url] = base64.b64decode(data.group(1), validate=True)
            return url

        return _FONT_DATA.sub(externalize, css)

    return _FONT_BLOCK.sub(replace, source), fonts


_GEOMETRY_SETUP = probe(PROBES, "prepare_explainer_math/geometry_setup")


def carrier_font_css(source: str) -> str:
    """Reuse shipped glyphs with different strut metrics, including in WebKit.

    WebKit lacks the FontFace ascent/descent override API. Changing only the metrics
    in an in-memory font copy makes the same control available in every engine.
    These bytes are temporary test input and never enter the publication artifact.
    """
    from fontTools.ttLib import TTFont  # noqa: PLC0415

    for block in _FONT_BLOCK.finditer(source):
        css = block.group()
        if not re.search(r"font-family:\s*[\"']?PT Serif[\"']?\s*;", css):
            continue
        if not re.search(r"font-style:\s*normal\s*;", css):
            continue
        data = _FONT_DATA.search(css)
        if data is None:
            continue
        font = TTFont(BytesIO(base64.b64decode(data.group(1), validate=True)))
        # FontTools creates these fields while decompiling each table; its table
        # types do not declare them. Keep untyped access at this font boundary.
        head: Any = font["head"]
        vertical: Any = font["hhea"]
        os2: Any = font["OS/2"]
        units = int(head.unitsPerEm)
        ascent, descent = round(1.8 * units), round(0.2 * units)
        vertical.ascent, vertical.descent, vertical.lineGap = ascent, -descent, 0
        os2.sTypoAscender, os2.sTypoDescender, os2.sTypoLineGap = ascent, -descent, 0
        os2.usWinAscent, os2.usWinDescent = ascent, descent
        output = BytesIO()
        font.save(output)
        encoded = base64.b64encode(output.getvalue()).decode("ascii")
        return (
            '@font-face{font-family:"Squares Carrier Control";font-style:normal;'
            'font-weight:400;src:url("data:font/woff2;base64,' + encoded + '")}'
        )
    raise ValueError("no shipped prose face for the carrier-metrics control")


_GEOMETRY_SNAPSHOT = probe(PROBES, "prepare_explainer_math/geometry_snapshot")


_MATH_COVERAGE = probe(PROBES, "prepare_explainer_math/math_coverage")


def coverage_findings(coverage: MathCoverage) -> list[str]:
    """A surviving subset of boxes cannot establish coverage of the page's math."""
    findings: list[str] = []
    if not coverage["targets"] or not coverage["formulas"] or not coverage["bases"]:
        findings.append("no complete prepared mathematics was covered")
    if coverage["missing"]:
        findings.append(f"visible mathematics has no prepared formula: {coverage['missing']}")
    if coverage["unreserved"]:
        findings.append(f"visible math bases lack reservations: {coverage['unreserved']}")
    if coverage["variant_errors"]:
        findings.append(f"CSS selected the wrong math variants: {coverage['variant_errors']}")
    if coverage["duplicate_ids"]:
        findings.append(f"prepared page has duplicate IDs: {coverage['duplicate_ids']}")
    return findings


_GEOMETRY_EARLY_READY = probe(PROBES, "prepare_explainer_math/geometry_early_ready")


#: Installed in the head: holds the math runtime's calls until the before snapshot.
_GEOMETRY_FONT_TRACE = applied(probe(PROBES, "prepare_explainer_math/geometry_font_trace"))


_MATH_VISIBILITY_STATE = probe(PROBES, "prepare_explainer_math/math_visibility_state")


#: Installed in the head: holds the host's batches until released.
_QUEUE_WATCHDOG_HOLD = applied(probe(PROBES, "prepare_explainer_math/queue_watchdog_hold"))

_QUEUE_WATCHDOG_OBSERVE = probe(PROBES, "prepare_explainer_math/queue_watchdog_observe")
_MATH_NOT_PENDING = probe(PROBES, "prepare_explainer_math/math_not_pending")
_RELEASE_QUEUE = probe(PROBES, "prepare_explainer_math/release_queue")
_QUEUED_COUNT = probe(PROBES, "prepare_explainer_math/queued_count")
_UNREADABLE_AFTER = probe(PROBES, "prepare_explainer_math/unreadable_after")


class QueueObservation(TypedDict):
    delayed_batches: int
    root_pending: bool
    unsubmitted_formulas: int
    observed_ms: float
    frames: NotRequired[int]
    target_classes: dict[str, int]
    exposed: list[str]


class QueueWatchdogReport(TypedDict):
    before: QueueObservation
    held_fonts: int
    queued_remaining: int
    unreadable_after: list[str]
    environment: BrowserEnvironment
    findings: list[str]


def check_queue_watchdog(
    source: str,
    *,
    browser_name: str = "chromium",
    width: int = 1280,
    prose_font: str = "serif",
    font_set: str = "custom",
    break_queue: bool = False,
) -> QueueWatchdogReport:
    """Exercise actual watchdog expiry separately from normal font-arrival geometry.

    Issued readouts may legitimately recover to fallback after three seconds. The
    initial static producer stays delayed, so its queued wrappers must remain safe
    until they can acquire the runtime's per-node readiness protection.
    """
    return asyncio.run(
        _check_queue_watchdog_async(
            source,
            browser_name=browser_name,
            width=width,
            prose_font=prose_font,
            font_set=font_set,
            break_queue=break_queue,
        )
    )


async def _check_queue_watchdog_async(
    source: str,
    *,
    browser_name: str,
    width: int,
    prose_font: str,
    font_set: str,
    break_queue: bool,
) -> QueueWatchdogReport:
    from playwright.async_api import async_playwright  # noqa: PLC0415

    instrumented, font_data = held_math_fonts(
        font_preference_html(
            _head_script(source, _QUEUE_WATCHDOG_HOLD),
            prose_font=prose_font,
            font_set=font_set,
        )
    )
    held: list[Route] = []
    released = False

    async def route_font(route: Route) -> None:
        if released:
            await release_held_fonts([route], font_data)
        else:
            held.append(route)

    async with async_playwright() as driver:
        browser_type = getattr(driver, browser_name)
        executable = os.environ.get(BROWSER_OVERRIDE) if browser_name == "chromium" else None
        browser = await browser_type.launch(executable_path=executable)
        browser_version = browser.version
        try:
            page = await browser.new_page(viewport={"width": width, "height": 960})
            await page.emulate_media(reduced_motion="reduce", color_scheme="light")
            await page.route(f"{_FONT_URL}*", route_font)
            await page.set_content(instrumented, wait_until="domcontentloaded")
            await page.wait_for_function(_MATH_NOT_PENDING, timeout=5000)
            before = cast(
                "QueueObservation",
                await page.evaluate(
                    _QUEUE_WATCHDOG_OBSERVE,
                    {
                        "broken": break_queue,
                        "math": await page.evaluate_handle(MATH_LIBRARY),
                        "observationMs": OBSERVATION_MS,
                    },
                ),
            )
            held_count = len(held)
            released = True
            await release_held_fonts(held, font_data)
            await page.evaluate(_RELEASE_QUEUE)
            await page.wait_for_selector(READY)
            await page.evaluate(SETTLED)
            queued_remaining = cast("int", await page.evaluate(_QUEUED_COUNT))
            unreadable_after = cast(
                "list[str]",
                await page.evaluate(
                    _UNREADABLE_AFTER, {"math": await page.evaluate_handle(MATH_LIBRARY)}
                ),
            )
        finally:
            await browser.close()
    findings: list[str] = []
    if not held_count:
        findings.append("the queue watchdog control held no actual math-font transfers")
    if not before["delayed_batches"] or not before["unsubmitted_formulas"]:
        findings.append("the queue watchdog control held no unsubmitted formulas")
    if before["root_pending"]:
        findings.append("the queue watchdog control did not observe watchdog expiry")
    if before["exposed"]:
        findings.append(f"math exposed while queued after watchdog: {before['exposed']}")
    if queued_remaining or unreadable_after:
        findings.append("queued math did not recover after font transfers resumed")
    return {
        "before": before,
        "held_fonts": held_count,
        "queued_remaining": queued_remaining,
        "unreadable_after": unreadable_after,
        "findings": findings,
        "environment": {
            "browser": browser_name,
            "browser_version": browser_version,
            "viewport": {"width": width, "height": 960},
            "media": "screen",
            "recorded_at": datetime.now(UTC).isoformat(),
        },
    }


async def release_held_fonts(held: list[Route], font_data: dict[str, bytes]) -> None:
    """Start every response together, without serial browser acknowledgements."""
    await asyncio.gather(
        *(
            route.fulfill(
                body=font_data[route.request.url],
                content_type="font/woff2",
                headers={"access-control-allow-origin": "*"},
            )
            for route in held
        )
    )


_CLICK = probe(PROBES, "prepare_explainer_math/click")
_MATH_SUBMITTED = probe(PROBES, "prepare_explainer_math/math_submitted")
_PROSE_FONTS_SETTLED = probe(PROBES, "prepare_explainer_math/prose_fonts_settled")
_REMOVE_FIRST_RESERVATION = probe(PROBES, "prepare_explainer_math/remove_first_reservation")
_SOURCE_IDENTITY = probe(PROBES, "prepare_explainer_math/source_identity")
_WIDEN_FIRST_RESERVATION = probe(PROBES, "prepare_explainer_math/widen_first_reservation")
_CARRIER_FONT_LOADED = probe(PROBES, "prepare_explainer_math/carrier_font_loaded")
_BREAK_FIRST_RESERVATION = probe(PROBES, "prepare_explainer_math/break_first_reservation")
_REMOVE_NODE = probe(PROBES, "prepare_explainer_math/remove_node")
_RESTORE_FIRST_RESERVATION = probe(PROBES, "prepare_explainer_math/restore_first_reservation")
_MARK_BEFORE_SNAPSHOT_COMPLETE = probe(
    PROBES, "prepare_explainer_math/mark_before_snapshot_complete"
)
_RELEASE_GEOMETRY_FONT_GATE = probe(PROBES, "prepare_explainer_math/release_geometry_font_gate")
_GEOMETRY_BOXES_VISIBLE = probe(PROBES, "prepare_explainer_math/geometry_boxes_visible")
_GEOMETRY_FONT_TRACE_REPORT = probe(PROBES, "prepare_explainer_math/geometry_font_trace_report")


def check_geometry(
    source: str,
    *,
    browser_name: str = "chromium",
    width: int = 1280,
    medium: str = "screen",
    break_reservation: bool = False,
    wrong_reservation: bool = False,
    missing_reservation: bool = False,
    alternate_certificate: bool = False,
    prose_font: str = "serif",
    font_set: str = "custom",
) -> GeometryReport:
    """Keep the synchronous CLI boundary while releasing font transfers concurrently."""
    return asyncio.run(
        _check_geometry_async(
            source,
            browser_name=browser_name,
            width=width,
            medium=medium,
            break_reservation=break_reservation,
            wrong_reservation=wrong_reservation,
            missing_reservation=missing_reservation,
            alternate_certificate=alternate_certificate,
            prose_font=prose_font,
            font_set=font_set,
        )
    )


async def _check_geometry_async(
    source: str,
    *,
    browser_name: str = "chromium",
    width: int = 1280,
    medium: str = "screen",
    break_reservation: bool = False,
    wrong_reservation: bool = False,
    missing_reservation: bool = False,
    alternate_certificate: bool = False,
    prose_font: str = "serif",
    font_set: str = "custom",
) -> GeometryReport:
    """Hold real math-font responses, change intrinsic glyph advances, then reveal.

    Temporary monospace glyphs and a carrier face with different ascent/descent make
    the before-state advances and line struts distinct on every host platform.
    The negative control removes one reservation during that phase; the checker must
    reject it. Neither test alteration reaches the artifact on disk.
    """
    from playwright.async_api import (  # noqa: PLC0415
        TimeoutError as PlaywrightTimeoutError,
    )
    from playwright.async_api import async_playwright  # noqa: PLC0415

    instrumented, font_data = held_math_fonts(
        font_preference_html(
            _head_script(source, _GEOMETRY_FONT_TRACE),
            prose_font=prose_font,
            font_set=font_set,
        )
    )
    held: list[Route] = []
    released = False
    first_request: float | None = None
    first_held_request = asyncio.Event()

    async def route_font(route: Route) -> None:
        nonlocal first_request
        if first_request is None:
            first_request = time.time() * 1000
        if released:
            await route.fulfill(
                body=font_data[route.request.url],
                content_type="font/woff2",
                headers={"access-control-allow-origin": "*"},
            )
        else:
            held.append(route)
            first_held_request.set()

    async with async_playwright() as driver:
        browser_type = getattr(driver, browser_name)
        executable = os.environ.get(BROWSER_OVERRIDE) if browser_name == "chromium" else None
        browser = await browser_type.launch(executable_path=executable)
        browser_version = browser.version
        try:
            page = await browser.new_page(viewport={"width": width, "height": 960})
            await page.emulate_media(
                media=medium, reduced_motion="reduce", color_scheme="light"
            )
            await page.route(f"{_FONT_URL}*", route_font)
            await page.set_content(instrumented, wait_until="domcontentloaded")
            if alternate_certificate:
                await page.locator('.cert-toggle button[aria-pressed="false"]').first.evaluate(
                    _CLICK
                )
            # Every queued hydration must inspect the real computed font before the
            # temporary monospace override below. Submission does not wait for the
            # font responses held here; older artifacts submitted synchronously.
            await page.evaluate(_MATH_SUBMITTED)
            await page.evaluate(_PROSE_FONTS_SETTLED)
            if missing_reservation:
                await page.evaluate(_REMOVE_FIRST_RESERVATION)
            coverage_before = cast("MathCoverage", await page.evaluate(_MATH_COVERAGE))
            await page.evaluate(_GEOMETRY_SETUP)
            source_identity = cast("PageIdentity", await page.evaluate(_SOURCE_IDENTITY))
            early_visible = cast(
                "list[ReadyMathBox]", await page.evaluate(_GEOMETRY_EARLY_READY)
            )
            if wrong_reservation:
                await page.evaluate(_WIDEN_FIRST_RESERVATION)
            carrier_style = await page.add_style_tag(content=carrier_font_css(source))
            await page.evaluate(_CARRIER_FONT_LOADED)
            substitution = await page.add_style_tag(
                content=(
                    '.katex, .katex-html { font-family: "Squares Carrier Control" '
                    "!important; } "
                    ".squares-math-box > .base, .squares-math-box > .base * "
                    "{ font-family: monospace !important; }"
                )
            )
            if break_reservation:
                await page.evaluate(_BREAK_FIRST_RESERVATION)
            before = cast("list[GeometryBox]", await page.evaluate(_GEOMETRY_SNAPSHOT))
            await substitution.evaluate(_REMOVE_NODE)
            await carrier_style.evaluate(_REMOVE_NODE)
            if break_reservation:
                await page.evaluate(_RESTORE_FIRST_RESERVATION)
            # The trace gate keeps KPress's production timeout clock stopped while
            # this probe constructs and measures its deliberately altered before
            # state. Start the real runtime only after those test styles are gone.
            await page.evaluate(_MARK_BEFORE_SNAPSHOT_COMPLETE)
            await page.evaluate(_RELEASE_GEOMETRY_FONT_GATE)
            await asyncio.wait_for(first_held_request.wait(), timeout=5)
            held_count = len(held)
            released = True
            release_started = time.time() * 1000
            await release_held_fonts(held, font_data)
            release_completed = time.time() * 1000
            await page.wait_for_selector(READY, timeout=60_000)
            await page.evaluate(SETTLED)
            # Font promises settle before every engine applies inherited paint
            # styles. Observe the actual visible frame rather than a promise turn.
            # Keep a failing after-state in the raw report; hidden boxes still
            # fail the unchanged geometry predicate below.
            with suppress(PlaywrightTimeoutError):
                await page.wait_for_function(_GEOMETRY_BOXES_VISIBLE, timeout=5000)
            after = cast("list[GeometryBox]", await page.evaluate(_GEOMETRY_SNAPSHOT))
            visibility_after = cast(
                "dict[str, object]",
                await page.evaluate(
                    _MATH_VISIBILITY_STATE, {"math": await page.evaluate_handle(MATH_LIBRARY)}
                ),
            )
            coverage_after = cast("MathCoverage", await page.evaluate(_MATH_COVERAGE))
            font_trace = cast(
                "FontRequestTrace", await page.evaluate(_GEOMETRY_FONT_TRACE_REPORT)
            )
        finally:
            await browser.close()
    early_ready = frozenset(
        box["key"]
        for box in early_visible
        if box["requests"]
        and all(
            request["check"]
            and request["faces"]
            and all(face["status"] == "loaded" for face in request["faces"])
            for request in box["requests"]
        )
    )
    findings = geometry_findings(
        before,
        after,
        early_ready=early_ready,
        root_watchdog_paused=font_trace["root_watchdog_paused"],
        # `_GEOMETRY_EARLY_READY` skips hidden boxes, so its keys are exactly what was
        # visible when it weighed each box's faces -- the one observation the exposure
        # rule and its exemptions can share.
        exposed_early=frozenset(box["key"] for box in early_visible),
    )
    findings.extend(coverage_findings(coverage_before))
    findings.extend(coverage_findings(coverage_after))
    if not held_count:
        findings.append("no actual math-font request was held")
    old = {box["key"]: box for box in before}
    changes = [
        abs(old[box["key"]]["intrinsic_width"] - box["intrinsic_width"])
        for box in after
        if box["key"] in old
    ]
    if not changes or max(changes) <= 1:
        findings.append("the font control did not produce distinct intrinsic glyph advances")
    result: GeometryReport = {
        "browser": browser_name,
        "width": width,
        "medium": medium,
        "alternate_certificate": alternate_certificate,
        "prose_font": prose_font,
        "font_set": font_set,
        "held_fonts": held_count,
        "visibility_after": visibility_after,
        "font_timing": {
            "first_math_request_ms": font_trace["first_math_request_ms"],
            "first_font_request_ms": (
                first_request - font_trace["time_origin_ms"]
                if first_request is not None
                else None
            ),
            "root_watchdog_paused": font_trace["root_watchdog_paused"],
            "release_started_ms": release_started - font_trace["time_origin_ms"],
            "release_completed_ms": release_completed - font_trace["time_origin_ms"],
            "held_ms": release_started - first_request if first_request is not None else None,
            "release_ms": release_completed - release_started,
            "rejections": font_trace["rejections"],
        },
        "before": before,
        "after": after,
        "early_visible": early_visible,
        "coverage_before": coverage_before,
        "coverage_after": coverage_after,
        "environment": {
            "browser": browser_name,
            "browser_version": browser_version,
            "viewport": {"width": width, "height": 960},
            "media": medium,
            "recorded_at": datetime.now(UTC).isoformat(),
        },
        "source_identity": source_identity,
        "findings": findings,
    }
    return result


class HostMathReport(TypedDict):
    print_visible: list[str]
    heat_draws: list[str]
    rejected_requests: int
    native_fallbacks: int
    findings: list[str]


#: Installed in the head: records the heat-map canvases drawn into.
_HEAT_DRAW_PROBE = applied(probe(PROBES, "prepare_explainer_math/heat_draws"))

#: Installed in the head: every required math face fails to load.
_REQUIRED_FONT_FAILURE = applied(probe(PROBES, "prepare_explainer_math/required_font_failure"))
_CLEAR_HEAT_DRAWS = probe(PROBES, "prepare_explainer_math/clear_heat_draws")
_DISPATCH_BEFOREPRINT = probe(PROBES, "prepare_explainer_math/dispatch_beforeprint")
_VISIBLE_HEAT_CANVASES = probe(PROBES, "prepare_explainer_math/visible_heat_canvases")
_HEAT_DRAWS_REPORT = probe(PROBES, "prepare_explainer_math/heat_draws_report")
_REJECTED_FONTS = probe(PROBES, "prepare_explainer_math/rejected_fonts")
_NATIVE_FALLBACKS = probe(PROBES, "prepare_explainer_math/native_fallbacks")
_PREPARATION_METRICS = probe(PROBES, "prepare_explainer_math/preparation_metrics")


def _head_script(source: str, script: str) -> str:
    head = re.search(r"<head(?:\s[^>]*)?>", source)
    if head is None:
        raise ValueError("the explainer has no head for the browser control")
    return source[: head.end()] + f"<script>{script}</script>" + source[head.end() :]


def check_host_math(source: str, *, browser_name: str = "chromium") -> HostMathReport:
    """Check alternate-certificate printing and semantic fallback on face failure."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    findings: list[str] = []
    with sync_playwright() as driver:
        browser_type = getattr(driver, browser_name)
        executable = os.environ.get(BROWSER_OVERRIDE) if browser_name == "chromium" else None
        browser = browser_type.launch(executable_path=executable)
        try:
            page = browser.new_page()
            page.set_content(_head_script(source, _HEAT_DRAW_PROBE), wait_until="load")
            page.wait_for_selector(READY)
            page.evaluate(SETTLED)
            page.locator('.cert-toggle button[aria-pressed="false"]').first.click()
            page.evaluate(SETTLED)
            page.emulate_media(media="print")
            page.evaluate(SETTLED)
            # Exclude any screen task already queued before the media change. The
            # explicit print event must repaint the canvas CSS actually puts on paper.
            page.evaluate(_CLEAR_HEAT_DRAWS)
            page.evaluate(_DISPATCH_BEFOREPRINT)
            page.evaluate(SETTLED)
            visible = cast("list[str]", page.evaluate(_VISIBLE_HEAT_CANVASES))
            drawn = cast("list[str]", page.evaluate(_HEAT_DRAWS_REPORT))
            if not visible or set(visible) != set(drawn):
                findings.append("print heat map does not match the CSS-visible certificate")
            page.close()
            page = browser.new_page()
            page.set_content(_head_script(source, _REQUIRED_FONT_FAILURE), wait_until="load")
            page.wait_for_selector(READY)
            rejected = cast("int", page.evaluate(_REJECTED_FONTS))
            fallbacks = cast("list[bool]", page.evaluate(_NATIVE_FALLBACKS))
            if not rejected or len(fallbacks) != 3 or not all(fallbacks):
                findings.append("required-font failure did not restore native semantic MathML")
        finally:
            browser.close()
    return {
        "print_visible": visible,
        "heat_draws": drawn,
        "rejected_requests": rejected,
        "native_fallbacks": sum(fallbacks),
        "findings": findings,
    }


def check_preparation_metrics(*, browser_name: str = "chromium") -> dict[str, object]:
    """Exercise the build's scaling oracle on real linear and fixed-pixel geometry."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with sync_playwright() as driver:
        browser = getattr(driver, browser_name).launch(
            executable_path=os.environ.get(BROWSER_OVERRIDE)
            if browser_name == "chromium"
            else None
        )
        try:
            page = browser.new_page()
            page.set_content(
                '<span id="base" style="display:inline-block;white-space:nowrap;'
                'font:18px monospace;text-rendering:geometricPrecision">mmmmiiii</span>'
            )
            result = cast(
                "dict[str, object]",
                page.evaluate(
                    _PREPARATION_METRICS,
                    {"measureMath": page.evaluate_handle(_MEASURE_MATH_REFERENCE)},
                ),
            )
            return {"browser": browser_name, "browser_version": browser.version, **result}
        finally:
            browser.close()


def main(argv: list[str] | None = None) -> int:
    """Check prepared geometry; publication remains the renderer CLI's one write."""
    from devtools.check_math_startup import instrument_provenance  # noqa: PLC0415

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", type=Path, nargs="?", default=PAGE)
    parser.add_argument(
        "--browser", choices=("chromium", "firefox", "webkit"), default="chromium"
    )
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--prose-font", choices=("serif", "sans"), default="serif")
    parser.add_argument("--font-set", choices=("custom", "system"), default="custom")
    parser.add_argument("--print", action="store_true", dest="print_media")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--host-check", action="store_true")
    parser.add_argument(
        "--queue-watchdog",
        action="store_true",
        help="expire the startup marker while later batches and real fonts are held",
    )
    parser.add_argument("--alternate-certificate", action="store_true")
    parser.add_argument("--output", type=Path, help="write the JSON report to this path")
    args = parser.parse_args(argv)
    if args.width < 1:
        parser.error("viewport width must be positive")
    if args.output and args.output.resolve() == args.page.resolve():
        parser.error("the JSON report must not overwrite its input HTML")
    source = args.page.read_text(encoding="utf-8")
    report = check_geometry(
        source,
        browser_name=args.browser,
        width=args.width,
        medium="print" if args.print_media else "screen",
        alternate_certificate=args.alternate_certificate,
        prose_font=args.prose_font,
        font_set=args.font_set,
    )
    controls: dict[str, object] = {}
    preparation: dict[str, object] | None = None
    queue_positive: QueueWatchdogReport | None = None
    if args.self_test:
        preparation = check_preparation_metrics(browser_name=args.browser)
        metric_controls = cast("dict[str, dict[str, object]]", preparation["controls"])
        for name, expected in (
            ("hinted_metrics", "requires geometricPrecision"),
            ("nonlinear_scaling", "does not scale linearly"),
        ):
            error = metric_controls[name].get("error")
            rejected = isinstance(error, str) and expected in error
            controls[name] = {
                "rejected": rejected,
                "report": {
                    **metric_controls[name],
                    "findings": [error] if error else [],
                    "environment": report["environment"],
                },
            }
            if not rejected:
                report["findings"].append(f"the {name} negative control was not rejected")
        control = check_geometry(
            source,
            browser_name=args.browser,
            width=args.width,
            medium="print" if args.print_media else "screen",
            break_reservation=True,
            alternate_certificate=args.alternate_certificate,
            prose_font=args.prose_font,
            font_set=args.font_set,
        )
        rejected = any("moved" in finding for finding in control["findings"])
        controls["removed_width"] = {"rejected": rejected, "report": control}
        if not rejected:
            report["findings"].append("the missing-width negative control was not rejected")
        wrong = check_geometry(
            source,
            browser_name=args.browser,
            width=args.width,
            medium="print" if args.print_media else "screen",
            wrong_reservation=True,
            alternate_certificate=args.alternate_certificate,
            prose_font=args.prose_font,
            font_set=args.font_set,
        )
        rejected = any("reserved width differs" in finding for finding in wrong["findings"])
        controls["stable_wrong_width"] = {"rejected": rejected, "report": wrong}
        if not rejected:
            report["findings"].append(
                "the stable wrong-width negative control was not rejected"
            )
        missing = check_geometry(
            source,
            browser_name=args.browser,
            width=args.width,
            medium="print" if args.print_media else "screen",
            missing_reservation=True,
            alternate_certificate=args.alternate_certificate,
            prose_font=args.prose_font,
            font_set=args.font_set,
        )
        rejected = any("lack reservations" in finding for finding in missing["findings"])
        controls["missing_reservation"] = {"rejected": rejected, "report": missing}
        if not rejected:
            report["findings"].append(
                "the missing-reservation negative control was not rejected"
            )
        # Restore the otherwise invisible inline strut while keeping every
        # measured base intact. Width-only reservations must fail this control.
        unreserved_carrier = source.replace(
            "</head>",
            '<style>html .kpress [data-kpress-math-prepared="true"] .katex,'
            'html .kpress [data-kpress-math-prepared="true"] .katex-html'
            "{line-height:1.2!important}</style></head>",
            1,
        )
        carrier = check_geometry(
            unreserved_carrier,
            browser_name=args.browser,
            width=args.width,
            medium="print" if args.print_media else "screen",
            alternate_certificate=args.alternate_certificate,
            prose_font=args.prose_font,
            font_set=args.font_set,
        )
        rejected = any("baseline moved" in finding for finding in carrier["findings"])
        controls["unreserved_carrier"] = {"rejected": rejected, "report": carrier}
        if not rejected:
            report["findings"].append(
                "the unreserved-carrier negative control was not rejected"
            )
        queue_positive = check_queue_watchdog(
            source,
            browser_name=args.browser,
            width=args.width,
            prose_font=args.prose_font,
            font_set=args.font_set,
        )
        report["findings"].extend(
            f"queue watchdog: {finding}" for finding in queue_positive["findings"]
        )
        queue_broken = check_queue_watchdog(
            source,
            browser_name=args.browser,
            width=args.width,
            prose_font=args.prose_font,
            font_set=args.font_set,
            break_queue=True,
        )
        rejected = any(
            "exposed while queued" in finding for finding in queue_broken["findings"]
        )
        controls["unprotected_queue"] = {"rejected": rejected, "report": queue_broken}
        if not rejected:
            report["findings"].append("the unprotected-queue negative control was not rejected")
    if args.queue_watchdog and queue_positive is None:
        queue_positive = check_queue_watchdog(
            source,
            browser_name=args.browser,
            width=args.width,
            prose_font=args.prose_font,
            font_set=args.font_set,
        )
        report["findings"].extend(
            f"queue watchdog: {finding}" for finding in queue_positive["findings"]
        )
    output: dict[str, object] = {
        "schema_version": 1,
        "measurement": "prepared-math-geometry",
        **report,
        "requested_source": str(args.page.resolve()),
        "instrument": {
            **instrument_provenance([dict(report)]),
            "entry_point": "devtools.prepare_explainer_math",
            "command_arguments": argv if argv is not None else sys.argv[1:],
        },
        "controls": controls,
    }
    if preparation is not None:
        output["preparation_metrics"] = preparation
    if queue_positive is not None:
        output["queue_watchdog"] = queue_positive
    if args.host_check:
        host_source = font_preference_html(
            source, prose_font=args.prose_font, font_set=args.font_set
        )
        host = check_host_math(host_source, browser_name=args.browser)
        output["host"] = host
        report["findings"].extend(host["findings"])
        if args.self_test:
            # The former host branches are retained as actual browser controls. A
            # source refactor must update their construction instead of silently
            # turning either regression back into a positive-only assertion.
            broken = host_source.replace(
                "pv.getClientRects().length", "!pv.closest('.cert-figure').hidden"
            )
            if (
                broken == host_source
                or "else delete el.dataset.kpressMathRendered;" not in broken
            ):
                report["findings"].append("the host negative controls could not be constructed")
            else:
                broken = broken.replace("else delete el.dataset.kpressMathRendered;", "")
                control = check_host_math(broken, browser_name=args.browser)
                print_rejected = any(
                    "print heat map" in finding for finding in control["findings"]
                )
                fallback_rejected = any(
                    "semantic MathML" in finding for finding in control["findings"]
                )
                controls["host_regressions"] = {
                    "print_rejected": print_rejected,
                    "native_fallback_rejected": fallback_rejected,
                    "report": control,
                }
                if not print_rejected:
                    report["findings"].append(
                        "the hidden-certificate print control was not rejected"
                    )
                if not fallback_rejected:
                    report["findings"].append("the native fallback control was not rejected")
    encoded = json.dumps(output, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
        print(f"Wrote {args.output}")
        for finding in report["findings"]:
            print(f"FAIL: {finding}")
    else:
        print(encoded, end="")
    return int(bool(report["findings"]))


if __name__ == "__main__":
    raise SystemExit(main())
