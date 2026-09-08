"""Reserve the published page's math geometry using its actual fonts and cascade.

KaTeX's HTML has measured vertical struts, but its glyph runs still have intrinsic
width. A hidden TeX or MathML fallback therefore cannot reserve the final layout.
The publication build typesets each supported font preference in pinned Chromium and
measures each unbreakable ``.base`` separately. Its fixed outer box keeps that width,
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
import base64
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from html import escape
from html.parser import HTMLParser
from itertools import pairwise
from pathlib import Path
from textwrap import dedent
from typing import TypedDict, cast, override

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


_MEASURE_MATH = dedent(r"""
    (attributeNames) => {
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
            const fontSize = parseFloat(getComputedStyle(base).fontSize);
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
""")


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


class GeometryReport(TypedDict):
    browser: str
    width: int
    medium: str
    alternate_certificate: bool
    prose_font: str
    font_set: str
    held_fonts: int
    before: list[GeometryBox]
    after: list[GeometryBox]
    early_visible: list[ReadyMathBox]
    coverage_before: MathCoverage
    coverage_after: MathCoverage
    environment: BrowserEnvironment
    source_identity: PageIdentity
    findings: list[str]


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

_GEOMETRY_SNAPSHOT = dedent("""
    () => globalThis.__squaresGeometryBoxes.filter(box => box.isConnected).map(box => {
      const rect = box.getBoundingClientRect(), style = getComputedStyle(box);
      return {key: Number(box.dataset.squaresGeometryKey),
        group: Number(box.dataset.squaresGeometryGroup), x: rect.x, y: rect.y,
        width: rect.width, height: rect.height,
        baseline: rect.bottom + parseFloat(style.verticalAlign),
        intrinsic_width: box.firstElementChild.getBoundingClientRect().width,
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
    """Hold real math-font responses, change intrinsic glyph advances, then reveal.

    The temporary monospace substitution makes the before-state advances distinct
    even on a browser whose fallback happens to resemble the supplied math face.
    The negative control removes one reservation during that phase; the checker must
    reject it. Neither test alteration reaches the artifact on disk.
    """
    from playwright.sync_api import Route, sync_playwright  # noqa: PLC0415

    instrumented, font_data = held_math_fonts(
        font_preference_html(source, prose_font=prose_font, font_set=font_set)
    )
    held: list[Route] = []
    released = False

    def route_font(route: Route) -> None:
        if released:
            route.fulfill(
                body=font_data[route.request.url],
                content_type="font/woff2",
                headers={"access-control-allow-origin": "*"},
            )
        else:
            held.append(route)

    with sync_playwright() as driver:
        browser_type = getattr(driver, browser_name)
        executable = os.environ.get(BROWSER_OVERRIDE) if browser_name == "chromium" else None
        browser = browser_type.launch(executable_path=executable)
        browser_version = browser.version
        try:
            page = browser.new_page(viewport={"width": width, "height": 960})
            page.emulate_media(media=medium, reduced_motion="reduce", color_scheme="light")
            page.route(f"{_FONT_URL}*", route_font)
            page.set_content(instrumented, wait_until="domcontentloaded")
            if alternate_certificate:
                page.locator('.cert-toggle button[aria-pressed="false"]').first.evaluate(
                    "button => button.click()"
                )
            # Reading fonts can change ordinary prose widths too. Settle those first,
            # without waiting for the math requests deliberately held by this probe.
            page.evaluate(
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
                page.evaluate(
                    "const box = [...document.querySelectorAll('.squares-math-box')]"
                    ".find(node => node.getBoundingClientRect().width > 0);"
                    "const base = box.firstElementChild; base.style.position = '';"
                    "box.replaceWith(base)"
                )
            coverage_before = cast("MathCoverage", page.evaluate(_MATH_COVERAGE))
            page.evaluate(_GEOMETRY_SETUP)
            source_identity = cast(
                "PageIdentity",
                page.evaluate(
                    dedent("""
                    () => ({title: document.title,
                      publication_date: document.querySelector(
                        '.publication-date')?.textContent || null,
                      revision_url: document.querySelector(
                        'a[href*="github.com/jlevy/squares/blob/"]')?.href || null})
                """)
                ),
            )
            early_visible = cast("list[ReadyMathBox]", page.evaluate(_GEOMETRY_EARLY_READY))
            if wrong_reservation:
                page.evaluate(
                    "const box = globalThis.__squaresGeometryBoxes[0]; "
                    "box.style.width = (box.getBoundingClientRect().width + 12) + 'px'"
                )
            substitution = page.add_style_tag(
                content=(
                    ".squares-math-box > .base, .squares-math-box > .base * "
                    "{ font-family: monospace !important; }"
                )
            )
            if break_reservation:
                page.evaluate(
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
            before = cast("list[GeometryBox]", page.evaluate(_GEOMETRY_SNAPSHOT))
            substitution.evaluate("node => node.remove()")
            if break_reservation:
                page.evaluate(
                    dedent("""
                    () => {
                      const [box, style, childStyle] = globalThis.__brokenGeometry;
                      box.style.cssText = style;
                      box.firstElementChild.style.cssText = childStyle;
                    }
                """)
                )
            held_count = len(held)
            released = True
            for route in held:
                route.fulfill(
                    body=font_data[route.request.url],
                    content_type="font/woff2",
                    headers={"access-control-allow-origin": "*"},
                )
            page.wait_for_selector(READY, timeout=60_000)
            page.evaluate(SETTLED)
            after = cast("list[GeometryBox]", page.evaluate(_GEOMETRY_SNAPSHOT))
            coverage_after = cast("MathCoverage", page.evaluate(_MATH_COVERAGE))
        finally:
            browser.close()
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
    return {
        "browser": browser_name,
        "width": width,
        "medium": medium,
        "alternate_certificate": alternate_certificate,
        "prose_font": prose_font,
        "font_set": font_set,
        "held_fonts": held_count,
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
    if args.self_test:
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
