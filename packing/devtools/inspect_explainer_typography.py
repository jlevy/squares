"""Report the computed typography used by visible text in HTML or SVG.

Run against the explainer or one of its SVG assets. Both screen and print styles
are inspected. SVG effective sizes include the viewport transform; external SVG
images must be inspected separately. Supporting-text checks compare ordinary text
with the first visible caption and detect intersecting inline SVG label boxes.

`--check-supporting` also asks the provenance question, in both media: whether every
run of text on the page is drawn from a face the page ships. That is the on-screen half
of the guard `render_explainer_pdf --check` holds the exported file to, and the two
share one list of what is shipped and one list of the host faces a kpress bead is on
its way to replacing. It is one flag rather than two because the second question is not
optional either: a run set in the reader's own font is a different page for every
reader, whatever else about it is consistent.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Literal, NotRequired, TypedDict

from devtools.check_print_layout import PRINT_VIEWPORT
from devtools.render_explainer_pdf import (
    BROWSER_OVERRIDE,
    PAGE,
    READY,
    SETTLED,
    host_font_bead,
    shipped,
)


class FontUse(TypedDict):
    """One computed family, weight, and style, with sizes and example text nodes."""

    family: str
    weight: str
    style: str
    color: str
    sizes: list[float]
    effective_sizes: list[float]
    samples: list[str]


class Inspection(TypedDict):
    """Inventories retain their original shape; checks add optional findings."""

    screen: list[FontUse]
    print: list[FontUse]
    findings: NotRequired[list[str]]


class Probe(TypedDict):
    """Inventory and optional check results from one browser pass."""

    fonts: list[FontUse]
    findings: list[str]


SUPPORTING_SELECTOR = (
    ".kpress-figcaption, .kpress-footnotes, .mass-line, .line-fig, .chart, .tip-panel, .panel"
)

#: What the provenance check covers: the document, not the reader's interface around it.
PROVENANCE_SCOPE = ".cert-page"

#: Elements whose text nodes are not the page's text: the four the tree walk would
#: otherwise read as content, and `math`, which is the machine-readable copy KaTeX writes
#: beside every expression it renders. That copy is clipped to a pixel and never seen; a
#: screen reader is what consumes it, in whatever face it prefers, and Blink still reports
#: platform fonts for it -- Times and STIX Two Math, from the reader's machine, 121 times
#: over. The same subtree is what `_PROBE` skips, for the same reason.
PROVENANCE_SKIP = ("SCRIPT", "STYLE", "TITLE", "DESC", "MATH")


def _attributes(node: dict[str, object]) -> dict[str, str]:
    """One node's attributes, which `DOM.getDocument` returns as a flat name/value list."""
    flat = node.get("attributes")
    if not isinstance(flat, list):
        return {}
    return {str(k): str(v) for k, v in zip(flat[::2], flat[1::2], strict=False)}


def _children(node: dict[str, object]) -> list[dict[str, object]]:
    """One node's child nodes, which `DOM.getDocument` returns as an untyped list."""
    kids = node.get("children")
    if not isinstance(kids, list):
        return []
    return [child for child in kids if isinstance(child, dict)]


def _element_label(node: dict[str, object], index: int) -> str:
    """One step of a path: the tag, its classes, and its place among its siblings."""
    classes = "".join(f".{name}" for name in _attributes(node).get("class", "").split())
    return f"{str(node.get('nodeName', '?')).lower()}{classes}[{index}]"


def _platform_fonts(session: object, node_id: int) -> list[dict[str, object]]:
    """The platform faces Blink drew one element's own text nodes with.

    Asked per element rather than once over the document, and the reason is a measurement:
    `CSS.getPlatformFontsForNode` is documented as answering for the child text nodes of a
    node, and on this page `body` answers with nothing at all while `.cert-page` inside it
    answers with four faces. The viewport kpress wraps the document in is a containment
    boundary, and the aggregate does not cross it. A walk that trusted an empty answer at
    the root would report a clean page without having looked at it.
    """
    from playwright.sync_api import CDPSession  # noqa: PLC0415

    assert isinstance(session, CDPSession)
    fonts = session.send("CSS.getPlatformFontsForNode", {"nodeId": node_id}).get("fonts")
    if not isinstance(fonts, list):
        return []
    return [entry for entry in fonts if isinstance(entry, dict)]


def _unshipped(fonts: list[dict[str, object]]) -> list[str]:
    """The families in one answer that the page did not ship and no bead expects.

    A face is the page's when the document carries its bytes and it is one of the families
    the page declares. Both halves are needed: kpress's `LocalPunct` is a real
    `@font-face`, so Blink calls it a custom font, and its source is `local("Georgia")` --
    the reader's own serif, under a name the page chose.
    """
    seen: list[str] = []
    for entry in fonts:
        family = str(entry.get("familyName", ""))
        if not family or family in seen:
            continue
        if entry.get("isCustomFont") and shipped(family):
            continue
        if host_font_bead(family) is not None:
            continue
        seen.append(family)
    return seen


def _text_bearing(node: dict[str, object], trail: list[str]) -> list[tuple[int, str]]:
    """Every element under this one that holds visible text directly, with its path.

    Text is attributed to the element it sits in rather than to an ancestor, so a finding
    names the run and not the section it is in. An element with no layout -- hidden, or
    inside a `hidden` block -- reports no platform font at all, which is how the hidden
    copies of the mathematics stay out of this without a visibility test of their own.
    """
    found: list[tuple[int, str]] = []
    # Upper-cased before the comparison: an HTML element reports its tag in capitals and
    # a MathML or SVG one reports its local name as written, so `math` and `MATH` are the
    # same element seen through two namespaces.
    if str(node.get("nodeName", "")).upper() in PROVENANCE_SKIP:
        return found
    children = _children(node)
    if any(
        child.get("nodeType") == 3 and str(child.get("nodeValue", "")).strip()
        for child in children
    ):
        found.append((int(str(node.get("nodeId") or 0)), " > ".join(trail[-4:])))
    for index, child in enumerate(child for child in children if child.get("nodeType") == 1):
        found.extend(_text_bearing(child, [*trail, _element_label(child, index)]))
    return found


def provenance_findings(page: object) -> list[str]:
    """Every run on the page drawn from a face the page does not ship.

    The 100-best atlas figure needs no exception here and gets none: its labels are inside
    `known-best-1-100.svg`, referenced as an `<img>`, so they are not text nodes of this
    document and Blink never reports them. The exception for its Helvetica lives in the PDF
    guard, which sees the figure's own fonts because the export embeds them.

    Scoped to the document rather than to the whole page. kpress's chrome around it -- the
    tooltip, the theme control, the footnote navigation -- is set in `system-ui` on
    purpose, because it is the reader's interface and not the paper; none of it prints, and
    what the PDF guard sees is exactly what this scope covers.
    """
    from playwright.sync_api import Page  # noqa: PLC0415

    assert isinstance(page, Page)
    session = page.context.new_cdp_session(page)
    try:
        session.send("DOM.enable")
        session.send("CSS.enable")
        document = session.send("DOM.getDocument", {"depth": -1})
        found = session.send(
            "DOM.querySelector",
            {"nodeId": int(str(document["root"]["nodeId"])), "selector": PROVENANCE_SCOPE},
        )
        scope = _node(document["root"], int(str(found.get("nodeId") or 0)))
        if scope is None:
            return [f"the page has no {PROVENANCE_SCOPE} to check"]
        findings: list[str] = []
        for node_id, path in _text_bearing(scope, [PROVENANCE_SCOPE]):
            offenders = _unshipped(_platform_fonts(session, node_id))
            if offenders:
                named = ", ".join(offenders)
                is_are = "is not a face" if len(offenders) == 1 else "are not faces"
                findings.append(f"{path}: {named} {is_are} the page ships")
        return findings
    finally:
        session.detach()


def _node(tree: dict[str, object], node_id: int) -> dict[str, object] | None:
    """One node of a `DOM.getDocument` tree, by its id."""
    if not node_id:
        return None
    if int(str(tree.get("nodeId") or 0)) == node_id:
        return tree
    for child in _children(tree):
        if (found := _node(child, node_id)) is not None:
            return found
    return None


_PROBE = r"""({selector, supporting, check}) => {
  const groups = new Map();
  const findings = new Set();
  let checked = 0;
  const visible = el => getComputedStyle(el).visibility === 'visible'
    && el.getClientRects().length && !el.closest('[hidden]');
  const caption = [...document.querySelectorAll('.kpress-figcaption')].find(visible);
  const expected = caption ? getComputedStyle(caption) : null;
  const exceptions = 'a, .katex, math, .tex, .tex-d, code, pre, '
    + 'h1, h2, h3, h4, h5, h6, .verdict, .hi, .mass-val, .tag';
  if (check && !expected) findings.add('no visible caption to establish supporting typography');
  const round = x => Math.round(x * 10000) / 10000;
  const walker = document.createTreeWalker(document.documentElement, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode, el = node.parentElement;
    const text = node.textContent.replace(/\s+/g, ' ').trim();
    if (!text || !el) continue;
    if (selector && !el.closest(selector)) continue;
    if (el.closest('script, style, title, desc, .kpress-math-semantic')) continue;
    const css = getComputedStyle(el);
    if (!visible(el)) continue;
    const svgText = el.closest('svg text');
    const color = svgText ? css.fill : css.color;
    const size = Number.parseFloat(css.fontSize);
    // The transformed vertical em measures displayed letter size, even where
    // the SVG has a rotated or non-uniformly scaled coordinate system.
    const ctm = svgText ? el.getScreenCTM() : null;
    const effective = round(size * (ctm ? Math.hypot(ctm.c, ctm.d) : 1));
    const key = [css.fontFamily, css.fontWeight, css.fontStyle, color].join('|');
    if (!groups.has(key)) groups.set(key, {
      family: css.fontFamily, weight: css.fontWeight, style: css.fontStyle, color,
      sizes: [], effective_sizes: [], samples: [],
    });
    const group = groups.get(key);
    if (!group.sizes.includes(size)) group.sizes.push(size);
    if (!group.effective_sizes.includes(effective)) group.effective_sizes.push(effective);
    const sample = `${el.tagName.toLowerCase()}: ${text.slice(0, 100)}`;
    if (group.samples.length < 5 && !group.samples.includes(sample)) group.samples.push(sample);
    if (check && expected && el.closest(supporting) && !el.closest(exceptions)) {
      checked++;
      const differences = [];
      if (Math.abs(effective - Number.parseFloat(expected.fontSize)) > 0.1)
        differences.push(`size ${effective}px (expected ${expected.fontSize})`);
      if (css.fontFamily !== expected.fontFamily)
        differences.push(`family ${css.fontFamily} (expected ${expected.fontFamily})`);
      if (color !== expected.color && !el.closest('button[aria-pressed="true"]'))
        differences.push(`color ${color} (expected ${expected.color})`);
      if (differences.length) findings.add(`${sample}: ${differences.join('; ')}`);
    }
  }
  if (check && expected && !checked)
    findings.add('no ordinary supporting text matched the requested selector');
  if (check) {
    for (const link of document.querySelectorAll('.cert-page a')) {
      if (visible(link) && getComputedStyle(link).textDecorationLine !== 'none')
        findings.add(`persistent link decoration: ${link.textContent.trim().slice(0, 80)}`);
    }
    for (const svg of document.querySelectorAll('.line-fig svg, .chart svg')) {
      if (!visible(svg) || (selector && !svg.closest(selector) && !svg.querySelector(selector)))
        continue;
      const labels = [...svg.querySelectorAll('text')].filter(visible);
      for (let i = 0; i < labels.length; i++) {
        const a = labels[i].getBoundingClientRect();
        for (let j = i + 1; j < labels.length; j++) {
          const b = labels[j].getBoundingClientRect();
          const width = Math.min(a.right, b.right) - Math.max(a.left, b.left);
          const height = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
          if (width > 1 && height > 1) findings.add('SVG label boxes overlap: '
            + `${labels[i].textContent.trim()} / ${labels[j].textContent.trim()} `
            + `(${round(width)} x ${round(height)}px)`);
        }
      }
    }
  }
  return {
    fonts: [...groups.values()].map(g => ({...g,
      sizes: g.sizes.sort((a, b) => a - b),
      effective_sizes: g.effective_sizes.sort((a, b) => a - b),
    })).sort((a, b) => a.family.localeCompare(b.family)
      || Number(a.weight) - Number(b.weight) || a.color.localeCompare(b.color)),
    findings: [...findings],
  };
}"""


def inspect(
    path: Path,
    selector: str | None = None,
    *,
    theme: Literal["light", "dark"] | None = None,
    width: int = 1280,
    check_supporting: bool = False,
) -> Inspection:
    """Inspect settled text in both media without changing the source document."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    report: Inspection = {"screen": [], "print": []}
    findings: list[str] = []
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            page = browser.new_page(
                reduced_motion="reduce", viewport={"width": width, "height": 720}
            )
            if theme:
                page.emulate_media(color_scheme=theme)
            page.goto(path.resolve().as_uri(), wait_until="load")
            if page.locator(".cert-page").count():
                page.wait_for_selector(READY, timeout=60_000)
            if theme:
                page.evaluate(
                    """theme => {
                      document.documentElement.dataset.kpressTheme = theme;
                      const scopes = document.querySelectorAll('[data-kpress-resolved-theme]');
                      for (const el of scopes)
                        el.dataset.kpressResolvedTheme = theme;
                    }""",
                    theme,
                )
            for medium in ("screen", "print"):
                if medium == "print":
                    page.emulate_media(media="print")
                    page.set_viewport_size(PRINT_VIEWPORT)
                page.evaluate(SETTLED)
                probe: Probe = page.evaluate(
                    _PROBE,
                    {
                        "selector": selector,
                        "supporting": SUPPORTING_SELECTOR,
                        "check": check_supporting,
                    },
                )
                if medium == "screen":
                    report["screen"] = probe["fonts"]
                else:
                    report["print"] = probe["fonts"]
                findings.extend(f"{medium}: {finding}" for finding in probe["findings"])
                if check_supporting:
                    findings.extend(
                        f"{medium}: {finding}" for finding in provenance_findings(page)
                    )
            if check_supporting:
                report["findings"] = findings
            return report
        finally:
            browser.close()


def self_test() -> None:
    """Check that the browser gate accepts agreement and rejects known defects."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    fixture = """<!doctype html><html><head><style>
      .cert-page { font-family: Arial, sans-serif; font-size: 17.575px; color: #666; }
      a { color: inherit; text-decoration: none; }
      svg text { font-family: Arial, sans-serif; font-size: 35.15px; fill: #666; }
    </style></head><body><div class="cert-page">
      <figcaption class="kpress-figcaption">Reference caption</figcaption>
      <p class="kpress-footnotes" id="footnote">Supporting footnote</p>
      <a href="#footnote">Reference link</a>
      <div class="line-fig"><svg viewBox="0 0 400 120" width="200" height="60">
        <text x="10" y="40">Alpha</text><text x="200" y="100">Beta</text>
      </svg></div>
    </div></body></html>"""
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            page = browser.new_page()
            page.set_content(fixture)
            arguments = {
                "selector": None,
                "supporting": SUPPORTING_SELECTOR,
                "check": True,
            }
            valid: Probe = page.evaluate(_PROBE, arguments)
            if valid["findings"]:
                raise SystemExit(
                    f"typography self-test rejected valid fixture: {valid['findings']}"
                )
            page.evaluate(
                """() => {
                  const footnote = document.querySelector('#footnote');
                  footnote.style.fontSize = '24px';
                  footnote.style.color = '#f00';
                  document.querySelector('a').style.textDecoration = 'underline';
                  const labels = document.querySelectorAll('svg text');
                  labels[1].setAttribute('x', '10');
                  labels[1].setAttribute('y', '40');
                }"""
            )
            invalid: Probe = page.evaluate(_PROBE, arguments)
            required = (
                "size 24px",
                "color rgb(255, 0, 0)",
                "persistent link decoration:",
                "SVG label boxes overlap:",
            )
            missing = [
                marker
                for marker in required
                if not any(marker in finding for finding in invalid["findings"])
            ]
            if missing:
                raise SystemExit(f"typography self-test missed known violations: {missing}")
            page.set_content(fixture)
            page.locator(".kpress-figcaption").evaluate("el => el.remove()")
            no_caption: Probe = page.evaluate(_PROBE, arguments)
            if not any(
                finding.startswith("no visible caption") for finding in no_caption["findings"]
            ):
                raise SystemExit("typography self-test accepted a fixture without a caption")
        finally:
            browser.close()
    print("typography self-test passed: valid, inconsistent, and missing-caption fixtures")


def main() -> None:
    """Print a JSON typography inventory for a rendered page or SVG."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", nargs="?", type=Path, default=PAGE)
    parser.add_argument("--selector", help="Inspect only text within matching CSS elements")
    parser.add_argument("--theme", choices=("light", "dark"), help="Force the screen theme")
    parser.add_argument(
        "--width", type=int, default=1280, help="Screen viewport width in CSS px"
    )
    parser.add_argument(
        "--check-supporting",
        action="store_true",
        help="Fail on inconsistent supporting typography",
    )
    parser.add_argument(
        "--self-test", action="store_true", help="Exercise the gate with known browser fixtures"
    )
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.width <= 0:
        parser.error("--width must be positive")
    report = inspect(
        args.page,
        args.selector,
        theme=args.theme,
        width=args.width,
        check_supporting=args.check_supporting,
    )
    print(json.dumps(report, indent=2))
    if report.get("findings"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
