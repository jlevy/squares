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
from textwrap import dedent
from typing import TYPE_CHECKING, Any, NotRequired, TypedDict, cast, override

if TYPE_CHECKING:
    from playwright.async_api import Route

from devtools.check_math_loading import ACTIVE_MATH_VARIANT, EXPOSED, OBSERVATION_MS
from devtools.render_explainer_pdf import BROWSER_OVERRIDE, PAGE, READY, SETTLED

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


_LINEAR_BASE_GEOMETRY = dedent("""
    (base) => {
      const style = getComputedStyle(base);
      const fontSize = parseFloat(style.fontSize);
      const width = base.getBoundingClientRect().width;
      const native = document.documentElement.dataset.squaresNativeMathMetrics === 'true';
      if (style.textRendering.toLowerCase() !== 'geometricprecision'
          && !(native && style.textRendering === 'auto')) {
        throw new Error('math preparation requires geometricPrecision '
          + 'or native linear metrics, got '
          + style.textRendering + ': ' + base.textContent);
      }
      const scale = 16;
      // A fresh same-parent sample keeps selector context and leaves the live
      // formula and its layout untouched.
      const probe = base.cloneNode(true);
      probe.style.setProperty('font-size', (fontSize * scale) + 'px', 'important');
      probe.style.position = 'absolute';
      probe.style.visibility = 'hidden';
      base.after(probe);
      let linearWidth, scaledFontSize;
      try {
        scaledFontSize = parseFloat(getComputedStyle(probe).fontSize);
        linearWidth = probe.getBoundingClientRect().width / scale;
      } finally {
        probe.remove();
      }
      if (!(fontSize > 0 && width > 0 && linearWidth > 0)) {
        throw new Error('empty or hidden linear math geometry: ' + base.textContent);
      }
      if (Math.abs(scaledFontSize - fontSize * scale) > 0.01) {
        throw new Error('math scaling sample did not use the requested font size: '
          + scaledFontSize + 'px instead of ' + (fontSize * scale) + 'px');
      }
      if (Math.abs(width - linearWidth) > 1) {
        throw new Error('math width does not scale linearly: ' + width + 'px at '
          + fontSize + 'px versus ' + linearWidth + 'px normalized from '
          + scaledFontSize + 'px: ' + base.textContent);
      }
      return {fontSize, width, linearWidth, textRendering: style.textRendering};
    }
""")


_MEASURE_MATH = dedent(r"""
    (attributeNames) => {
      const linearGeometry = __LINEAR_BASE_GEOMETRY__;
      const fixed = value => {
        if (!Number.isFinite(value)) throw new Error('non-finite math geometry');
        return Number(value.toFixed(8)) + 'em';
      };
      const result = [];
      for (const target of document.querySelectorAll('[data-squares-math-key]')) {
        const clone = target.cloneNode(true);
        const actualNodes = element => element.matches('.kpress-math')
          ? [element.querySelector('.kpress-math-render')]
          : element.id.startsWith('kval-')
            ? [...element.querySelectorAll('.math-item')]
            : [element];
        const nodes = actualNodes(target), copies = actualNodes(clone);
        if (!nodes.length || nodes.length !== copies.length) {
          throw new Error('missing initial parameter math: ' + target.outerHTML.slice(0, 200));
        }
        for (let index = 0; index < nodes.length; index++) {
          const node = nodes[index], copy = copies[index];
          if (!node || !copy || !node.querySelector('.katex')
              || !node.hasAttribute('data-kpress-math-source')) {
            throw new Error('math did not finish preparing: ' + target.outerHTML.slice(0, 200));
          }
          const bases = [...node.querySelectorAll('.katex-html > .base')];
          const clonedBases = [...copy.querySelectorAll('.katex-html > .base')];
          if (!bases.length) throw new Error('KaTeX emitted no measurable base');
          for (let part = 0; part < bases.length; part++) {
            const base = bases[part], child = clonedBases[part];
            const measured = linearGeometry(base);
            const fontSize = measured.fontSize;
            const parentSize = parseFloat(getComputedStyle(base.parentElement).fontSize);
            const marker = document.createElement('span');
            marker.style.cssText = 'display:inline-block;width:0;height:0;padding:0;margin:0;'
              + 'border:0;line-height:0;vertical-align:baseline;';
            base.append(marker);
            const rect = base.getBoundingClientRect();
            const baseline = marker.getBoundingClientRect().top;
            marker.remove();
            if (!(rect.width > 0 && rect.height > 0 && fontSize > 0 && parentSize > 0)) {
              throw new Error('empty or hidden math geometry: ' + node.textContent);
            }
            const box = document.createElement('span');
            box.className = 'squares-math-box';
            box.style.cssText = 'display:inline-block;position:relative;'
              + 'font-size:' + fixed(fontSize / parentSize) + ';'
              + 'width:' + fixed(rect.width / fontSize) + ';'
              + 'height:' + fixed(rect.height / fontSize) + ';'
              + 'vertical-align:' + fixed((baseline - rect.bottom) / fontSize) + ';';
            // The same em strut must anchor the actual glyphs and their reserved
            // box. A font's line strut rounds differently at print sizes; keep
            // its measured extent explicitly, including short punctuation bases.
            const strut = child.querySelector(':scope > .strut');
            if (!strut) throw new Error('KaTeX emitted no baseline strut');
            strut.style.height = fixed(rect.height / fontSize);
            strut.style.verticalAlign = fixed((baseline - rect.bottom) / fontSize);
            child.replaceWith(box);
            box.append(child);
            child.style.position = 'absolute';
            child.style.left = '0';
            child.style.top = '0';
          }
          copy.dataset.kpressMathPrepared = 'true';
          delete copy.dataset.squaresMathReady;
          delete copy.dataset.done;
        }
        clone.removeAttribute('data-squares-math-key');
        const attributes = {};
        for (const name of attributeNames) {
          if (clone.hasAttribute(name)) attributes[name] = clone.getAttribute(name);
        }
        result.push({
          key: Number(target.dataset.squaresMathKey), html: clone.innerHTML, attributes
        });
      }
      return result;
    }
""").replace("__LINEAR_BASE_GEOMETRY__", _LINEAR_BASE_GEOMETRY)


_COMBINE_MATH_VARIANTS = dedent("""
    ({contexts, attributeNames}) => {
      const actualNodes = element => element.matches('.kpress-math')
        ? [element.querySelector('.kpress-math-render')]
        : element.id.startsWith('kval-')
          ? [...element.querySelectorAll('.math-item')]
          : [element];
      const attributes = node => Object.fromEntries(attributeNames.filter(name =>
        node.hasAttribute(name)).map(name => [name, node.getAttribute(name)]));
      return contexts[0].fragments.map((fragment, slot) => {
        const original = document.querySelector('[data-squares-math-key="' + slot + '"]');
        const copies = contexts.map(context => {
          const measured = context.fragments[slot];
          if (measured.key !== fragment.key) throw new Error('math variant keys differ');
          const copy = original.cloneNode(false);
          for (const name of attributeNames) copy.removeAttribute(name);
          for (const [name, value] of Object.entries(measured.attributes)) {
            copy.setAttribute(name, value);
          }
          copy.innerHTML = measured.html;
          return copy;
        });
        const nodes = copies.map(actualNodes);
        for (let index = 0; index < nodes[0].length; index++) {
          const versions = new Map();
          contexts.forEach((context, offset) => {
            const node = nodes[offset][index];
            if (!node) throw new Error('math variant nodes differ');
            const signature = JSON.stringify([attributes(node), node.innerHTML]);
            const version = versions.get(signature) || {node, contexts: []};
            version.contexts.push(context.name);
            versions.set(signature, version);
          });
          if (versions.size === 1) continue;
          const parent = nodes[0][index];
          const variants = [...versions.values()].map(({node, contexts}) => {
            const variant = document.createElement('span');
            variant.className = 'squares-math-variant';
            variant.dataset.squaresMathContexts = contexts.join(' ');
            for (const [name, value] of Object.entries(attributes(node))) {
              variant.setAttribute(name, value);
            }
            variant.innerHTML = node.innerHTML;
            return variant;
          });
          // The source stays on the original host target. Font/profile state belongs
          // to the selected child, so an inactive serif ancestor cannot override it.
          for (const name of ['data-kpress-math-face', 'data-kpress-math-profile',
              'data-kpress-math-prepared']) parent.removeAttribute(name);
          parent.replaceChildren(...variants);
        }
        return {key: fragment.key, html: copies[0].innerHTML,
          attributes: attributes(copies[0])};
      });
    }
""")


def font_preference_html(source: str, *, prose_font: str, font_set: str) -> str:
    """Set the same pre-paint attributes as saved preferences in a fresh browser."""
    if (font_set, prose_font) not in _FONT_CONTEXTS:
        raise ValueError("unsupported explainer font preferences")
    # set_content() has no persistent origin. Assign the attributes in the head,
    # before the normal bootstrap and body; do not change them after math renders.
    return _head_script(
        source,
        f'document.documentElement.dataset.kpressProseFont = "{prose_font}";'
        f'document.documentElement.dataset.kpressFontSet = "{font_set}";',
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
                # Hidden certificate copies need their own measured context too.
                page.evaluate(
                    "document.querySelectorAll('.cert-figure').forEach(el => el.hidden = false)"
                )
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
    rejections: list[MathFontRejection]


class FontHoldTiming(TypedDict):
    first_math_request_ms: float | None
    first_font_request_ms: float | None
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
    tolerance: float = 1.0,
    early_ready: frozenset[int] = frozenset(),
) -> list[str]:
    """Compare the same boxes and their line breaks across actual font arrival."""
    findings: list[str] = []
    old = {box["key"]: box for box in before}
    new = {box["key"]: box for box in after}
    if not old or old.keys() != new.keys():
        findings.append("prepared math boxes disappeared or were never measured")
    if before and any(not box["hidden"] and box["key"] not in early_ready for box in before):
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


_GEOMETRY_SETUP = dedent("""
    () => {
      let group = 0;
      for (const formula of document.querySelectorAll('.katex-html')) {
        for (const box of formula.querySelectorAll(':scope > .squares-math-box')) {
          box.dataset.squaresGeometryGroup = String(group);
        }
        group++;
      }
      globalThis.__squaresGeometryBoxes = [...document.querySelectorAll('.squares-math-box')]
        .filter(box => box.getBoundingClientRect().width > 0);
      globalThis.__squaresGeometryBoxes.forEach((box, key) => {
        box.dataset.squaresGeometryKey = String(key);
      });
    }
""")


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


_GEOMETRY_SNAPSHOT = dedent("""
    () => globalThis.__squaresGeometryBoxes.filter(box => box.isConnected).map(box => {
      const rect = box.getBoundingClientRect(), style = getComputedStyle(box);
      const base = box.firstElementChild, baseStyle = getComputedStyle(base);
      return {key: Number(box.dataset.squaresGeometryKey),
        group: Number(box.dataset.squaresGeometryGroup), x: rect.x, y: rect.y,
        width: rect.width, height: rect.height,
        baseline: rect.bottom + parseFloat(style.verticalAlign),
        intrinsic_width: base.getBoundingClientRect().width,
        text: base.textContent, font_size: parseFloat(baseStyle.fontSize),
        text_rendering: baseStyle.textRendering,
        native_linear_metrics:
          document.documentElement.dataset.squaresNativeMathMetrics === 'true',
        hidden: style.visibility === 'hidden'};
    })
""")


_MATH_COVERAGE = dedent("""
    () => {
      const root = document.documentElement.dataset;
      const preference = (root.kpressFontSet === 'system' ? 'system' : 'custom') + '-'
        + (root.kpressProseFont === 'sans' ? 'sans' : 'serif');
      const parents = new Set([...document.querySelectorAll('.squares-math-variant')]
        .map(node => node.parentElement));
      const variant_errors = [];
      for (const parent of parents) {
        const displayed = [...parent.querySelectorAll(':scope > .squares-math-variant')]
          .filter(node => getComputedStyle(node).display !== 'none');
        if (displayed.length !== 1 || !displayed[0].dataset.squaresMathContexts
            ?.split(/\\s+/).includes(preference)) {
          variant_errors.push(parent.dataset.kpressMathSource || parent.id);
        }
      }
      const ids = new Set(), duplicate_ids = [];
      for (const node of document.querySelectorAll('[id]')) {
        if (ids.has(node.id)) duplicate_ids.push(node.id);
        ids.add(node.id);
      }
      const targets = [...document.querySelectorAll('[data-kpress-math-source]')]
        .filter(node => node.getClientRects().length);
      const formulas = [...new Set(targets.flatMap(node =>
        [...node.querySelectorAll('.katex-html')].filter(formula =>
          formula.getClientRects().length)))];
      const missing = targets.filter(node => !formulas.some(formula => node.contains(formula)))
        .map(node => node.dataset.kpressMathSource);
      const unreserved = [];
      let bases = 0;
      for (const formula of formulas) {
        const parts = [...formula.querySelectorAll('.base')];
        if (!parts.length) missing.push(formula.textContent);
        for (const base of parts) {
          bases++;
          const box = base.parentElement;
          if (!box.classList.contains('squares-math-box') || box.parentElement !== formula) {
            unreserved.push(formula.closest('[data-kpress-math-source]')
              ?.dataset.kpressMathSource || formula.textContent);
          }
        }
      }
      return {targets: targets.length, formulas: formulas.length, bases, missing, unreserved,
        variant_errors, duplicate_ids};
    }
""")


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


_GEOMETRY_EARLY_READY = dedent("""
    async () => {
      const result = [];
      const familyName = name => name.trim().replace(/^["']|["']$/g, '');
      for (const box of globalThis.__squaresGeometryBoxes) {
        if (getComputedStyle(box).visibility === 'hidden') continue;
        const requests = new Map();
        const walker = document.createTreeWalker(box, NodeFilter.SHOW_TEXT);
        for (let text = walker.nextNode(); text; text = walker.nextNode()) {
          if (!text.textContent || !text.parentElement) continue;
          const style = getComputedStyle(text.parentElement);
          const spec = `${style.fontStyle} ${style.fontWeight} `
            + `${style.fontSize} ${style.fontFamily}`;
          const request = requests.get(spec) || {text: '',
            families: style.fontFamily.split(',').map(familyName)};
          request.text += text.textContent;
          requests.set(spec, request);
        }
        const evidence = [];
        for (const [spec, request] of requests) {
          const {text, families} = request;
          const check = document.fonts.check(spec, text);
          const declared = [...document.fonts]
            .filter(face => families.includes(familyName(face.family)))
            .map(face => ({family: face.family, status: face.status,
              style: face.style, weight: face.weight, unicode_range: face.unicodeRange}));
          let faces = [], timer;
          if (check) {
            // A reported-ready glyph must resolve to an actually loaded declared
            // face, without releasing any transfer held by the geometry probe.
            try {
              faces = await Promise.race([
                document.fonts.load(spec, text),
                new Promise(resolve => { timer = setTimeout(() => resolve([]), 500); })
              ]);
            } finally { clearTimeout(timer); }
          }
          evidence.push({spec, text, check, declared_faces: declared,
            faces: faces.map(face => ({family: face.family, status: face.status}))});
        }
        result.push({key: Number(box.dataset.squaresGeometryKey),
          source: box.closest('[data-kpress-math-source]')?.dataset.kpressMathSource || '',
          requests: evidence});
      }
      return result;
    }
""")


_GEOMETRY_FONT_TRACE = dedent("""
    (() => {
      const trace = globalThis.__squaresGeometryFontTrace = {
        time_origin_ms: performance.timeOrigin, first_math_request_ms: null,
        before_snapshot_complete: false, queued_calls: 0, rejections: []
      };
      const waiting = [];
      let released = false;
      globalThis.__squaresMarkGeometryBeforeSnapshotComplete = () => {
        trace.before_snapshot_complete = true;
      };
      globalThis.__squaresReleaseGeometryFontGate = () => {
        if (!trace.before_snapshot_complete) {
          throw new Error('geometry font gate released before the before snapshot');
        }
        if (released) return;
        released = true;
        for (const invoke of waiting.splice(0)) invoke();
      };
      const invoke = (original, receiver, args) => {
        const start = performance.now();
        trace.first_math_request_ms ??= start;
        let result;
        try {
          result = original.apply(receiver, args);
        } catch (error) {
          trace.rejections.push({source: String(args[0]),
            elapsed_ms: performance.now() - start, reason: String(error)});
          throw error;
        }
        Promise.resolve(result).then(undefined, error => {
          trace.rejections.push({source: String(args[0]),
            elapsed_ms: performance.now() - start, reason: String(error)});
        });
        return result;
      };
      let runtime;
      Object.defineProperty(globalThis, 'kpressMathText', {
        configurable: true,
        get() { return runtime; },
        set(api) {
          runtime = api;
          for (const name of ['render', 'hydrate']) {
            const original = api[name];
            api[name] = function(...args) {
              const receiver = this;
              if (released) return invoke(original, receiver, args);
              return new Promise((resolve, reject) => {
                trace.queued_calls++;
                waiting.push(() => {
                  try {
                    Promise.resolve(invoke(original, receiver, args)).then(resolve, reject);
                  } catch (error) {
                    reject(error);
                  }
                });
              });
            };
          }
        }
      });
    })();
""")


_MATH_VISIBILITY_STATE = dedent("""
    () => {
      const active = __ACTIVE__;
      const maths = [...document.querySelectorAll('.katex,.squares-math-box')].filter(active)
        .filter(node => node.getClientRects().length);
      const hidden = maths.filter(node => getComputedStyle(node).visibility === 'hidden');
      return {at_ms: performance.now(), root: {...document.documentElement.dataset},
        queued: document.querySelectorAll('[data-squares-math-queued]').length,
        pending: document.querySelectorAll('[data-kpress-math-pending]').length,
        hidden: hidden.length,
        fonts: [...document.fonts].map(face => ({family: face.family,
          weight: face.weight, style: face.style, status: face.status})),
        samples: hidden.slice(0, 3).map(math => {
          const chain = [];
          for (let node = math; node && node !== document.body; node = node.parentElement) {
            const style = getComputedStyle(node);
            chain.push({classes: node.className, style: node.getAttribute('style'),
              data: {...node.dataset}, visibility: style.visibility, family: style.fontFamily});
          }
          return {text: math.textContent.slice(0, 100), chain};
        })};
    }
""").replace("__ACTIVE__", ACTIVE_MATH_VARIANT)


_QUEUE_WATCHDOG_HOLD = dedent("""
    (() => {
      let runtime;
      const posted = [];
      globalThis.__squaresQueueControl = {
        get count() { return posted.length; },
        release() { for (const post of posted.splice(0)) post(); }
      };
      // Delay the public producer before its first static job. The host must
      // protect every queued wrapper before handing any work to the scheduler.
      Object.defineProperty(globalThis, 'squaresMath', {
        configurable: true,
        get() { return runtime; },
        set(api) {
          runtime = api;
          const batch = api.batch;
          api.batch = function(jobs) {
            return new Promise((resolve, reject) => {
              posted.push(() => Promise.resolve(batch.call(this, jobs)).then(resolve, reject));
            });
          };
        }
      });
    })();
""")

_QUEUE_WATCHDOG_OBSERVE = (
    dedent("""
    async broken => {
      // The real head watchdog has expired while initial work and font
      // transfers remain held. Its fallback must not expose queued math.
      if (broken) for (const node of document.querySelectorAll('[data-squares-math-queued]')) {
        delete node.dataset.squaresMathQueued;
      }
      const active = __ACTIVE__;
      const exposed = __EXPOSED__;
      const waiting = [...document.querySelectorAll('.tex, .tex-d, .kpress-math')]
        .filter(node => {
          const box = node.classList.contains('kpress-math')
            ? node.querySelector('.kpress-math-render') : node;
          return box && !box.dataset.done && node.getClientRects().length
            && !box.matches('[data-kpress-math-pending]')
            && !box.querySelector('[data-kpress-math-pending]');
        });
      globalThis.__squaresQueuedControlNodes = waiting;
      const visible = new Set();
      const end = performance.now() + __OBSERVATION_MS__;
      let frames = 0;
      do {
        await new Promise(done => requestAnimationFrame(done));
        frames++;
        for (const node of waiting) {
          const formulas = [...node.querySelectorAll('.katex,.kpress-math-semantic')]
            .filter(active);
          if (formulas.some(exposed)) visible.add(node);
        }
      } while (performance.now() < end);
      return {delayed_batches: __squaresQueueControl.count,
        root_pending: document.documentElement.hasAttribute('data-kpress-math-pending'),
        unsubmitted_formulas: waiting.length, observed_ms: performance.now(),
        frames,
        target_classes: Object.fromEntries(['tex', 'tex-d', 'kpress-math'].map(name =>
          [name, waiting.filter(node => node.classList.contains(name)).length])),
        exposed: [...visible].map(node =>
          node.dataset.kpressMathSource || node.querySelector('.kpress-math-render')
            ?.dataset.kpressMathSource || node.textContent.trim().slice(0, 100))};
    }
""")
    .replace("__ACTIVE__", ACTIVE_MATH_VARIANT)
    .replace("__EXPOSED__", EXPOSED)
    .replace("__OBSERVATION_MS__", str(OBSERVATION_MS))
)


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
            await page.wait_for_function(
                "!document.documentElement.hasAttribute('data-kpress-math-pending')",
                timeout=5000,
            )
            before = cast(
                "QueueObservation", await page.evaluate(_QUEUE_WATCHDOG_OBSERVE, break_queue)
            )
            held_count = len(held)
            released = True
            await release_held_fonts(held, font_data)
            await page.evaluate("__squaresQueueControl.release()")
            await page.wait_for_selector(READY)
            await page.evaluate(SETTLED)
            queued_remaining = cast(
                "int",
                await page.evaluate(
                    "document.querySelectorAll('[data-squares-math-queued]').length"
                ),
            )
            unreadable_after = cast(
                "list[str]",
                await page.evaluate(
                    "() => { const exposed = "
                    + EXPOSED
                    + "; const active = "
                    + ACTIVE_MATH_VARIANT
                    + "; return __squaresQueuedControlNodes.filter(node => {"
                    " const formulas = [...node.querySelectorAll("
                    " '.katex,.kpress-math-semantic')]"
                    " .filter(active); return formulas.length ? !formulas.some(exposed)"
                    " : !node.textContent.trim() || !exposed(node);"
                    " }).map(node => node.dataset.kpressMathSource"
                    " || node.textContent.slice(0,80)); }"
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
                    "button => button.click()"
                )
            # Every queued hydration must inspect the real computed font before the
            # temporary monospace override below. Submission does not wait for the
            # font responses held here; older artifacts submitted synchronously.
            await page.evaluate("() => globalThis.squaresMath?.submitted?.()")
            # Reading fonts can change ordinary prose widths too. Settle those first,
            # without waiting for the math requests deliberately held by this probe.
            await page.evaluate(
                dedent("""
                async () => {
                  await Promise.all([...document.fonts].filter(face =>
                    !/^(?:["']?KaTeX_|["']?KPress Math Text)/.test(face.family)
                  ).map(face => face.load()));
                  await new Promise(done => requestAnimationFrame(() =>
                    requestAnimationFrame(done)));
                }
            """)
            )
            if missing_reservation:
                # Remove a complete reservation before discovery. A checker that
                # measures only surviving boxes would silently accept this subset.
                await page.evaluate(
                    "const box = [...document.querySelectorAll('.squares-math-box')]"
                    ".find(node => node.getBoundingClientRect().width > 0);"
                    "const base = box.firstElementChild; base.style.position = '';"
                    "box.replaceWith(base)"
                )
            coverage_before = cast("MathCoverage", await page.evaluate(_MATH_COVERAGE))
            await page.evaluate(_GEOMETRY_SETUP)
            source_identity = cast(
                "PageIdentity",
                await page.evaluate(
                    dedent("""
                    () => ({title: document.title,
                      publication_date: document.querySelector(
                        '.publication-date')?.textContent || null,
                      revision_url: document.querySelector(
                        'a[href*="github.com/jlevy/squares/blob/"]')?.href || null})
                """)
                ),
            )
            early_visible = cast(
                "list[ReadyMathBox]", await page.evaluate(_GEOMETRY_EARLY_READY)
            )
            if wrong_reservation:
                await page.evaluate(
                    "const box = globalThis.__squaresGeometryBoxes[0]; "
                    "box.style.width = (box.getBoundingClientRect().width + 12) + 'px'"
                )
            carrier_style = await page.add_style_tag(content=carrier_font_css(source))
            await page.evaluate(
                """async () => {
                  const faces = await document.fonts.load('16px "Squares Carrier Control"');
                  if (faces.length !== 1 || faces[0].status !== 'loaded') {
                    throw new Error('the carrier-metrics control did not load');
                  }
                }"""
            )
            substitution = await page.add_style_tag(
                content=(
                    '.katex, .katex-html { font-family: "Squares Carrier Control" '
                    "!important; } "
                    ".squares-math-box > .base, .squares-math-box > .base * "
                    "{ font-family: monospace !important; }"
                )
            )
            if break_reservation:
                await page.evaluate(
                    dedent("""
                    () => {
                      const box = globalThis.__squaresGeometryBoxes[0];
                      globalThis.__brokenGeometry = [box, box.style.cssText,
                        box.firstElementChild.style.cssText];
                      box.style.width = 'auto';
                      box.firstElementChild.style.position = 'relative';
                    }
                """)
                )
            before = cast("list[GeometryBox]", await page.evaluate(_GEOMETRY_SNAPSHOT))
            await substitution.evaluate("node => node.remove()")
            await carrier_style.evaluate("node => node.remove()")
            if break_reservation:
                await page.evaluate(
                    dedent("""
                    () => {
                      const [box, style, childStyle] = globalThis.__brokenGeometry;
                      box.style.cssText = style;
                      box.firstElementChild.style.cssText = childStyle;
                    }
                """)
                )
            # The trace gate keeps KPress's production timeout clock stopped while
            # this probe constructs and measures its deliberately altered before
            # state. Start the real runtime only after those test styles are gone.
            await page.evaluate("__squaresMarkGeometryBeforeSnapshotComplete()")
            await page.evaluate("__squaresReleaseGeometryFontGate()")
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
                await page.wait_for_function(
                    "__squaresGeometryBoxes.filter(box => box.isConnected).every("
                    "box => getComputedStyle(box).visibility !== 'hidden')",
                    timeout=5000,
                )
            after = cast("list[GeometryBox]", await page.evaluate(_GEOMETRY_SNAPSHOT))
            visibility_after = cast(
                "dict[str, object]", await page.evaluate(_MATH_VISIBILITY_STATE)
            )
            coverage_after = cast("MathCoverage", await page.evaluate(_MATH_COVERAGE))
            font_trace = cast(
                "FontRequestTrace", await page.evaluate("__squaresGeometryFontTrace")
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
    findings = geometry_findings(before, after, early_ready=early_ready)
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


_HEAT_DRAW_PROBE = dedent("""
    (() => {
      const draw = CanvasRenderingContext2D.prototype.drawImage;
      globalThis.__squaresHeatDraws = [];
      CanvasRenderingContext2D.prototype.drawImage = function(...args) {
        if (this.canvas.id.startsWith('prove-')) __squaresHeatDraws.push(this.canvas.id);
        return draw.apply(this, args);
      };
    })();
""")

_REQUIRED_FONT_FAILURE = dedent("""
    (() => {
      const fonts = Object.getPrototypeOf(document.fonts);
      const check = fonts.check, load = fonts.load;
      const required = spec => /KPress Math Text|KaTeX_/.test(spec);
      globalThis.__squaresRejectedFonts = 0;
      fonts.check = function(spec, text) {
        return required(spec) ? false : check.call(this, spec, text);
      };
      fonts.load = function(spec, text) {
        if (!required(spec)) return load.call(this, spec, text);
        __squaresRejectedFonts++;
        return Promise.reject(new Error('required math-font failure control'));
      };
    })();
""")


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
            page.evaluate("__squaresHeatDraws.length = 0")
            page.evaluate("dispatchEvent(new Event('beforeprint'))")
            page.evaluate(SETTLED)
            visible = cast(
                "list[str]",
                page.evaluate(
                    "[...document.querySelectorAll('canvas[id^=prove-]')]"
                    ".filter(node => node.getClientRects().length).map(node => node.id)"
                ),
            )
            drawn = cast("list[str]", page.evaluate("__squaresHeatDraws"))
            if not visible or set(visible) != set(drawn):
                findings.append("print heat map does not match the CSS-visible certificate")
            page.close()
            page = browser.new_page()
            page.set_content(_head_script(source, _REQUIRED_FONT_FAILURE), wait_until="load")
            page.wait_for_selector(READY)
            rejected = cast("int", page.evaluate("__squaresRejectedFonts"))
            fallbacks = cast(
                "list[bool]",
                page.evaluate(
                    dedent("""
                    [...document.querySelectorAll('.kpress-math')].slice(0, 3).map(node => {
                      const semantic = node.querySelector('.kpress-math-semantic');
                      if (!semantic) return false;
                      const style = getComputedStyle(semantic);
                      const box = semantic.getBoundingClientRect();
                      return !node.dataset.kpressMathRendered && !node.querySelector('.katex')
                        && style.clipPath === 'none' && style.visibility !== 'hidden'
                        && box.width > 1 && box.height > 1;
                    })
                """)
                ),
            )
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
                    dedent("""
                    () => {
                      const measure = __LINEAR_BASE_GEOMETRY__;
                      const base = document.querySelector('#base');
                      const positive = measure(base);
                      const controls = {};
                      for (const [name, property, value] of [
                        ['hinted_metrics', 'textRendering', 'auto'],
                        ['nonlinear_scaling', 'paddingLeft', '8px']
                      ]) {
                        const old = base.style[property];
                        base.style[property] = value;
                        try {
                          controls[name] = {measurement: measure(base), error: null};
                        } catch (error) {
                          controls[name] = {error: String(error)};
                        } finally {
                          base.style[property] = old;
                        }
                      }
                      return {positive, controls};
                    }
                    """).replace("__LINEAR_BASE_GEOMETRY__", _LINEAR_BASE_GEOMETRY)
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
