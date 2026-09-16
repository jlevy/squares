"""Report the computed typography used by visible text in HTML or SVG.

Run against the explainer or one of its SVG assets. Both screen and print styles
are inspected. SVG effective sizes include the viewport transform; external SVG
images must be inspected separately. Supporting-text checks compare captions and
endnotes with their shared role, figure labels with theirs, and detect intersecting
inline SVG label boxes.

`--check-supporting` also asks the provenance question, in both media: whether every
run of text on the page is drawn from a face the page ships. That is the on-screen half
of the guard `render_explainer_pdf --check-artifact` holds the exported file to, and the two
share one list of what is shipped and one list of the host faces a kpress bead is on
its way to replacing. It is one flag rather than two because the second question is not
optional either: a run set in the reader's own font is a different page for every
reader, whatever else about it is consistent.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
from typing import Literal, NotRequired, TypedDict

from devtools.check_print_layout import PRINT_VIEWPORT
from devtools.render_explainer import MATH_WRAPPERS
from devtools.render_explainer_pdf import (
    BROWSER_OVERRIDE,
    PAGE,
    READY,
    SETTLED,
    host_font_bead,
    shipped,
)
from sqpack.probes import probe as load_probe

#: The probes this module hands the page, one file each under `probes/`.
PROBES = Path(__file__).resolve().parent / "probes"


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
    math: NotRequired[dict[str, list[MathContext]]]
    code: NotRequired[dict[str, list[InlineCodeContext]]]
    findings: NotRequired[list[str]]


class Probe(TypedDict):
    """Inventory and optional check results from one browser pass."""

    fonts: list[FontUse]
    findings: list[str]


class MathContext(TypedDict):
    """The outer math em compared with its surrounding text, excluding script sizes."""

    role: str
    source: str
    size: float
    context_size: float
    family: str
    context_family: str
    weight: str
    context_weight: str
    text_rendering: str
    context_text_rendering: str
    baseline_offset: NotRequired[float | None]
    unboxed_baseline_offset: NotRequired[float | None]
    baseline_prepared: NotRequired[bool]
    display_math: NotRequired[bool]
    caption: NotRequired[str]


class InlineCodeContext(TypedDict):
    """Inline code's layout baseline and flat-bottomed ink relative to its context."""

    role: str
    source: str
    family: str
    context_family: str
    weight: str
    color: str
    context_color: str
    size: float
    context_size: float
    background_color: str
    border_styles: list[str]
    border_widths: list[float]
    white_space: str
    overflow_wrap: str
    word_break: str
    baseline_offset: float
    ink_bottom: float
    context_ink_bottom: float
    padding_top: float
    padding_bottom: float


#: Inline code against the text around it: baseline, ink, paint, type and wrapping.
_CODE_CONTEXTS = load_probe(PROBES, "inspect_explainer_typography/code_contexts")


def code_baseline_findings(rows: list[InlineCodeContext]) -> list[str]:
    """Inline code shares the surrounding baseline, independent of glyph height."""
    return [
        f"inline code {row['source']!r}: baseline differs from surrounding text "
        f"by {row['baseline_offset']:.4f}px"
        for row in rows
        if not math.isfinite(row["baseline_offset"]) or abs(row["baseline_offset"]) > 1 / 16
    ]


def code_print_style_findings(
    screen: list[InlineCodeContext], printed: list[InlineCodeContext]
) -> list[str]:
    """Print drops code-chip paint while keeping its typography and line behavior."""
    findings: list[str] = []
    for medium, rows in (("screen", screen), ("print", printed)):
        roles = {row["role"] for row in rows}
        findings.extend(
            f"no visible {role} inline code to verify in {medium}"
            for role in ("prose", "support")
            if role not in roles
        )
    findings.extend(
        f"screen inline code {row['source']!r}: chip decoration is missing"
        for row in screen
        if row["background_color"] == "rgba(0, 0, 0, 0)"
        or all(
            style == "none" or width == 0
            for style, width in zip(row["border_styles"], row["border_widths"], strict=True)
        )
    )
    screen_rows = {(row["role"], row["source"]): row for row in screen}
    for row in printed:
        if row["background_color"] != "rgba(0, 0, 0, 0)":
            findings.append(
                f"print inline code {row['source']!r}: background is {row['background_color']}"
            )
        if any(
            style != "none" and width != 0
            for style, width in zip(row["border_styles"], row["border_widths"], strict=True)
        ):
            findings.append(f"print inline code {row['source']!r}: border remains visible")
        if "Planetaire Mono Text" not in row["family"]:
            findings.append(f"print inline code {row['source']!r}: family is {row['family']!r}")
        screen_row = screen_rows.get((row["role"], row["source"]))
        if screen_row is None:
            findings.append(f"print inline code {row['source']!r}: no screen counterpart")
            continue
        if row["family"] != screen_row["family"] or row["weight"] != screen_row["weight"]:
            findings.append(f"print inline code {row['source']!r}: font changed")
        screen_ratio = screen_row["size"] / screen_row["context_size"]
        print_ratio = row["size"] / row["context_size"]
        if abs(screen_ratio - print_ratio) > 0.001:
            findings.append(f"print inline code {row['source']!r}: relative size changed")
        wrapping = ("white_space", "overflow_wrap", "word_break")
        if any(row[name] != screen_row[name] for name in wrapping):
            findings.append(f"print inline code {row['source']!r}: wrapping changed")
    return findings


def math_size_findings(rows: list[MathContext], *, require_roles: bool = False) -> list[str]:
    """Every root formula follows its context; KaTeX still sizes scripts internally."""
    findings = [
        f"{row['role']} math {row['source']!r}: size {row['size']}px "
        f"differs from surrounding text {row['context_size']}px"
        for row in rows
        if row["size"] <= 0
        or row["context_size"] <= 0
        or abs(row["size"] - row["context_size"]) > 0.01
    ]
    if require_roles:
        present = {row["role"] for row in rows}
        findings.extend(
            f"no visible {role} math to verify"
            for role in ("inline", "display", "caption")
            if role not in present
        )
    return findings


def math_baseline_findings(rows: list[MathContext]) -> list[str]:
    """Compare inline caption baselines, allowing four Chromium layout units of rounding."""
    findings = []
    for row in rows:
        if row["role"] != "caption" or row.get("display_math", False):
            continue
        offset = row.get("baseline_offset")
        if offset is None or not math.isfinite(offset):
            findings.append(f"caption math {row['source']!r}: no measured baseline")
        elif abs(offset) > 1 / 16:
            findings.append(
                f"caption math {row['source']!r}: baseline differs from surrounding text "
                f"by {offset:.4f}px"
            )
    return findings


#: Every visible formula's outer em against its context, and caption baselines.
_MATH_CONTEXTS = load_probe(PROBES, "inspect_explainer_typography/math_contexts")


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


#: The computed typography of every visible run, and the supporting-text checks.
_PROBE = load_probe(PROBES, "inspect_explainer_typography/typography")

#: The screen theme forced as the reader's toggle would, and the crop markers cleared.
_FORCE_THEME = load_probe(PROBES, "inspect_explainer_typography/force_theme")
_CLEAR_CROP_MARKERS = load_probe(PROBES, "inspect_explainer_typography/clear_crop_markers")

#: The self-test's changes to its fixtures: known violations put in, a caption removed or
#: hidden, and the real-KaTeX baseline fixture built, prepared, broken and restored.
_RAISE_CODE = load_probe(PROBES, "inspect_explainer_typography/raise_code")
_BREAK_SUPPORTING_FIXTURE = load_probe(
    PROBES, "inspect_explainer_typography/break_supporting_fixture"
)
_REMOVE_ELEMENT = load_probe(PROBES, "inspect_explainer_typography/remove_element")
_HIDE_ELEMENT = load_probe(PROBES, "inspect_explainer_typography/hide_element")
_RENDER_BASELINE_FIXTURE = load_probe(
    PROBES, "inspect_explainer_typography/render_baseline_fixture"
)
_APPLY_FRAGMENTS = load_probe(PROBES, "inspect_explainer_typography/apply_fragments")
_RESTORE_ORIGINAL_STRUTS = load_probe(
    PROBES, "inspect_explainer_typography/restore_original_struts"
)
_SET_INNER_HTML = load_probe(PROBES, "inspect_explainer_typography/set_inner_html")


def inspect(
    path: Path,
    selector: str | None = None,
    *,
    theme: Literal["light", "dark"] | None = None,
    width: int = 1280,
    check_supporting: bool = False,
    check_math: bool = False,
    math_crops: Path | None = None,
) -> Inspection:
    """Inspect settled text in both media without changing the source document."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    report: Inspection = {"screen": [], "print": [], "math": {}, "code": {}}
    findings: list[str] = []
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            page = browser.new_page(
                reduced_motion="reduce",
                viewport={"width": width, "height": 720},
                device_scale_factor=2 if math_crops else 1,
            )
            if theme:
                page.emulate_media(color_scheme=theme)
            page.goto(path.resolve().as_uri(), wait_until="load")
            if page.locator(".cert-page").count():
                page.wait_for_selector(READY, timeout=60_000)
            if theme:
                page.evaluate(_FORCE_THEME, theme)
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
                rows: list[MathContext] = page.evaluate(
                    _MATH_CONTEXTS, {"wrappers": MATH_WRAPPERS, "crops": bool(math_crops)}
                )
                report["math"][medium] = rows
                report["code"][medium] = page.evaluate(_CODE_CONTEXTS, bool(math_crops))
                if check_supporting:
                    findings.extend(
                        f"{medium}: {finding}"
                        for finding in code_baseline_findings(report["code"][medium])
                    )
                if check_math:
                    findings.extend(
                        f"{medium}: {finding}"
                        for finding in (
                            math_size_findings(rows, require_roles=True)
                            + math_baseline_findings(rows)
                        )
                    )
                if math_crops:
                    math_crops.mkdir(parents=True, exist_ok=True)
                    for role in ("inline", "display", "caption"):
                        crop = page.locator(f'[data-squares-typography-crop="{role}"]')
                        if crop.count():
                            crop.screenshot(path=math_crops / f"{medium}-{role}.png")
                    for role in ("prose", "support"):
                        crop = page.locator(f'[data-squares-code-crop="{role}"]')
                        if crop.count():
                            crop.screenshot(path=math_crops / f"{medium}-code-{role}.png")
                    page.evaluate(_CLEAR_CROP_MARKERS)
                if check_supporting:
                    findings.extend(
                        f"{medium}: {finding}" for finding in provenance_findings(page)
                    )
            if check_supporting:
                findings.extend(
                    code_print_style_findings(report["code"]["screen"], report["code"]["print"])
                )
            if check_supporting or check_math:
                report["findings"] = findings
            return report
        finally:
            browser.close()


def self_test(path: Path = PAGE) -> None:
    """Check that the browser gate accepts agreement and rejects known defects."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    fixture = """<!doctype html><html><head><style>
      .cert-page { font-family: Arial, sans-serif; font-size: 17.575px; color: #666; }
      .kpress-figcaption, .kpress-footnotes { font-size: 17px; }
      a { color: inherit; text-decoration: none; }
      svg text { font-family: Arial, sans-serif; font-size: 35.15px; fill: #666; }
    </style></head><body><div class="cert-page">
      <figcaption class="kpress-figcaption">Reference caption</figcaption>
      <p class="kpress-footnotes" id="footnote">Supporting footnote</p>
      <p class="mass-line">Reference figure label</p>
      <p>Text with <code>Hnx-010</code> aligned on its baseline.</p>
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
            code_rows: list[InlineCodeContext] = page.evaluate(_CODE_CONTEXTS, arg=False)
            if len(code_rows) != 1 or code_baseline_findings(code_rows):
                raise SystemExit("code-baseline self-test rejected the aligned fixture")
            page.locator("code").evaluate(_RAISE_CODE)
            raised_code: list[InlineCodeContext] = page.evaluate(_CODE_CONTEXTS, arg=False)
            if not code_baseline_findings(raised_code):
                raise SystemExit("code-baseline self-test missed raised inline code")
            page.evaluate(_BREAK_SUPPORTING_FIXTURE)
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
            page.locator(".kpress-figcaption").evaluate(_REMOVE_ELEMENT)
            no_caption: Probe = page.evaluate(_PROBE, arguments)
            if not any(
                finding.startswith("no visible caption") for finding in no_caption["findings"]
            ):
                raise SystemExit("typography self-test accepted a fixture without a caption")
            page.set_content("""<style>
              .cert-page {font-size:18px} .katex {font-size:inherit}
              figcaption {font-size:17px} .script {font-size:.7em}
              </style><div class="cert-page">
              <p>Inline <span class="tex"><span class="katex">x
              <span class="script">2</span></span></span></p>
              <div class="tex-d"><span class="katex-display">
              <span class="katex">x</span></span></div>
              <figcaption class="kpress-figcaption">Caption
              <span class="tex"><span class="katex">x</span></span></figcaption>
              </div>""")
            math_args = {"wrappers": MATH_WRAPPERS, "crops": False}
            correct: list[MathContext] = page.evaluate(_MATH_CONTEXTS, math_args)
            if {row["role"] for row in correct} != {
                "inline",
                "display",
                "caption",
            } or math_size_findings(correct):
                raise SystemExit(
                    "math-size self-test rejected contextual sizes or script scaling"
                )
            page.add_style_tag(content=".katex {font-size:1.1em}")
            enlarged: list[MathContext] = page.evaluate(_MATH_CONTEXTS, math_args)
            if len(math_size_findings(enlarged)) != 3:
                raise SystemExit(
                    "math-size self-test missed enlarged inline, display, or caption math"
                )
            page.locator("figcaption").evaluate(_HIDE_ELEMENT)
            hidden: list[MathContext] = page.evaluate(_MATH_CONTEXTS, math_args)
            if "no visible caption math to verify" not in math_size_findings(
                hidden, require_roles=True
            ):
                raise SystemExit("math-size self-test accepted a hidden caption role")
            # Use the real publication's fonts and the same preparation operation;
            # punctuation and nested layouts must survive scaling to print size too.
            from devtools.prepare_explainer_math import (  # noqa: PLC0415
                _MATH_ATTRIBUTES,  # pyright: ignore[reportPrivateUsage]
                _MEASURE_MATH,  # pyright: ignore[reportPrivateUsage]
            )

            page.goto(path.resolve().as_uri(), wait_until="load")
            page.wait_for_selector(READY, timeout=60_000)
            page.evaluate(SETTLED)
            sources = [
                ".",
                ",",
                r"\cdot",
                r"x^2",
                r"\frac{x+1}{2}",
                r"\sqrt{x_2}",
                r"\displaystyle\sum_{i=1}^{n} x_i",
                r"\smash{x}",
                r"\quad",
            ]
            page.evaluate(_RENDER_BASELINE_FIXTURE, sources)
            fragments = page.evaluate(_MEASURE_MATH, sorted(_MATH_ATTRIBUTES))
            page.evaluate(_APPLY_FRAGMENTS, fragments)
            for medium in ("screen", "print"):
                page.emulate_media(media=medium)
                page.evaluate(SETTLED)
                baselines: list[MathContext] = page.evaluate(_MATH_CONTEXTS, math_args)
                failures = math_baseline_findings(baselines)
                if failures:
                    raise SystemExit(
                        f"{medium} baseline self-test rejected valid math: {failures}"
                    )
                if not set(sources) <= {row["source"] for row in baselines}:
                    raise SystemExit("baseline self-test did not observe every real KaTeX case")
            fixture_caption = page.locator("[data-baseline-fixture]")
            prepared_fixture = fixture_caption.inner_html()
            fixture_caption.evaluate(_RESTORE_ORIGINAL_STRUTS)
            old_strut: list[MathContext] = page.evaluate(_MATH_CONTEXTS, math_args)
            if not math_baseline_findings(old_strut):
                raise SystemExit("baseline self-test accepted the original font-line-strut bug")
            fixture_caption.evaluate(_SET_INNER_HTML, prepared_fixture)
            page.add_style_tag(
                content="[data-baseline-fixture] .base { transform: translateY(-2px) }"
            )
            shifted: list[MathContext] = page.evaluate(_MATH_CONTEXTS, math_args)
            if len(math_baseline_findings(shifted)) != len(sources):
                raise SystemExit("baseline self-test missed an upward shift of caption math")
        finally:
            browser.close()
    print(
        "typography self-test passed: supporting text, contextual sizes, "
        f"{len(sources)} math baseline cases, inline code, "
        "original-strut and raised-glyph controls"
    )


def main() -> None:
    """Print a JSON typography inventory for a rendered page or SVG."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", nargs="?", type=Path, default=PAGE)
    parser.add_argument("--selector", help="Inspect only text within matching CSS elements")
    parser.add_argument("--theme", choices=("light", "dark"), help="Force the screen theme")
    parser.add_argument(
        "--check-math",
        action="store_true",
        help="Require contextual math size and aligned inline caption baselines",
    )
    parser.add_argument(
        "--math-crops",
        type=Path,
        help="Save matched 2x crops of inline, display, and caption math plus inline code",
    )
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
        self_test(args.page)
        return
    if args.width <= 0:
        parser.error("--width must be positive")
    report = inspect(
        args.page,
        args.selector,
        theme=args.theme,
        width=args.width,
        check_supporting=args.check_supporting,
        check_math=args.check_math,
        math_crops=args.math_crops,
    )
    print(json.dumps(report, indent=2))
    if report.get("findings"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
