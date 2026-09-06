"""Report the computed typography used by visible text in HTML or SVG.

Run against the explainer or one of its SVG assets. Both screen and print styles
are inspected. SVG effective sizes include the viewport transform; external SVG
images must be inspected separately. Supporting-text checks compare ordinary text
with the first visible caption and detect intersecting inline SVG label boxes.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Literal, NotRequired, TypedDict

from devtools.check_print_layout import PRINT_VIEWPORT
from devtools.render_explainer_pdf import BROWSER_OVERRIDE, PAGE, READY


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
                page.evaluate("document.fonts.ready")
                page.evaluate(
                    "() => new Promise(done => requestAnimationFrame("
                    "() => requestAnimationFrame(done)))"
                )
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
