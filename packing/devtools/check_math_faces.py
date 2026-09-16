#!/usr/bin/env python3
"""Check the explainer's mathematics: the right face, the right table, and painted once.

Three questions the rendered HTML cannot answer, all of them about the built page in a
browser.

**Which face draws each expression.** kpress ships two math text composites --
`KPress Math Text`, which draws the letters and digits of mathematics from PT Serif, and
`KPress Math Text Sans`, which draws them from Source Sans wherever the words around them
are sans -- and the stylesheet applies the second one on the `data-kpress-math-face="sans"`
mark the page's init stamps. So the mark is the whole of the decision, and it can be
wrong in two directions: a caption formula left unmarked is set in PT Serif inside a
sans caption, and a prose formula marked by mistake is set in Source Sans inside a PT
Serif paragraph. This walks every `.katex` on the page and compares the mark against the
face the words around it actually resolve to, in both media and with both saved prose
font preferences. A sans reading preference also moves the prose's bold mathematics into
the sans composite, so its declarations must cover those requests.

**Which metric table laid it out.** KaTeX lays out from a table baked into its own
bundle, so a page that swaps the drawn glyphs alone leaves fraction boxes, script
positions and italic corrections computed for Computer Modern. The tables are a KaTeX
singleton, and the page's init installs the set matching each node's context immediately
before rendering it. That is checked by measurement rather than by reading the code: an
expression is re-typeset from its own TeX source under each set in turn, and the live
geometry has to match the set its context asks for and to differ from the other. If the
two sets happened to lay out identically there would be nothing to check, and the check
says so rather than passing.

**Whether it was painted once.** KaTeX renders into the live DOM, so an expression is
painted in whatever faces have decoded by then, and each composite's slots are separate
`@font-face` rules fetched only when a formula first asks for them. Rendering as soon as
the DOM is ready therefore paints the digits from the next family in the stack and
repaints them a moment later, which the owner saw on the built page and on the live site
as every formula's digits changing font on load (`think-q5df`). An init script checks
the glyph fonts required by each formula when it first becomes CSS-visible, retaining
the first formula's observations and any later failures. Unused faces may remain
unloaded. Hidden staging nodes do not count as visible formulas. The separate
delayed-font checker also verifies native MathML and early interactive renders.

A fourth thing falls out of the first: the page's init has to have RUN. It is one
`(() => { ... })()` inlined into the page, and a reference error inside it leaves the
whole page working, looking almost right, and drawing every formula from the serif
composite with the serif tables -- which is exactly what happened once while this branch
was being written, with every other gate green. `--self-test` exercises the walk against
fixtures whose answers are known, the way the typography check does.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.check_math_faces
    uv run --frozen --all-extras --group dev python -m devtools.check_math_faces --self-test
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Literal, NotRequired, TypedDict

from devtools.check_math_loading import (
    FIRST_PAINT_SCRIPT,
    MATH_LIBRARY,
    MATH_LIBRARY_INIT,
    page_url,
)
from devtools.check_print_layout import PRINT_VIEWPORT
from devtools.render_explainer import MATH_WRAPPERS
from devtools.render_explainer_pdf import BROWSER_OVERRIDE, PAGE, READY, SETTLED
from sqpack.probes import applied, probe

#: The probes this module hands the page, one file each under `probes/`.
PROBES = Path(__file__).resolve().parent / "probes"

#: The faces the composites draw their Latin and digits from, by the prefix Blink answers
#: `CSS.getPlatformFontsForNode` with. A variable face comes back as the instance it is at
#: (`Source Sans 3 ExtraLight`), and a static instance under its own name, so both sides
#: are prefixes rather than exact names.
SANS_FACE = "Source Sans 3"
PROSE_FACE = "PT Serif"

#: A 4096px sample bounds a whole pixel's rounding error below 0.00025em. This
#: tolerance also covers rounding in the font metric table, while staying about 29
#: times below the D advance difference between the wrong 400 and required 650 slots.
BOLD_ADVANCE_TOLERANCE_EM = 0.0005

#: kpress's math markup, which the walk climbs through to find the words. The list is the
#: renderer's, since the init walks the same wrappers for the same reason.
PROBE_ARGUMENTS: dict[str, object] = {
    "wrappers": MATH_WRAPPERS,
    "advance_tolerance": BOLD_ADVANCE_TOLERANCE_EM,
}


#: A reference probe returning the measurement of one run's advance, in em.
FONT_ADVANCE = probe(PROBES, "check_math_faces/font_advance")


class Report(TypedDict):
    """What one run saw, and what it objects to."""

    nodes: int
    marked: int
    tables: list[str]
    drawn: NotRequired[list[str]]
    first_paint: NotRequired[dict[str, object]]
    prose_fonts: NotRequired[list[str]]
    bold_advances: NotRequired[list[str]]
    findings: list[str]


#: The walk (`probes/check_math_faces/faces.js`), for the medium the page is in.
PROBE = probe(PROBES, "check_math_faces/faces")
_STOP_LOADING_SAMPLER = probe(PROBES, "check_math_faces/stop_loading_sampler")
_MARK_LATIN_RUN = probe(PROBES, "check_math_faces/mark_latin_run")
_UNMARK_RUN = probe(PROBES, "check_math_faces/unmark_run")
_PRINT_MATCHES = probe(PROBES, "check_math_faces/print_matches")
_SAVE_PROSE_FONT = probe(PROBES, "check_math_faces/save_prose_font")
_PROSE_FONT_SELECTED = probe(PROBES, "check_math_faces/prose_font_selected")
_FIRST_PAINT_SUMMARY = probe(PROBES, "check_math_faces/first_paint_summary")


def _walk(page: object, arguments: dict[str, object]) -> Report:
    """Run the walk on the page as it is, with the math helpers it takes as handles."""
    from playwright.sync_api import Page  # noqa: PLC0415

    assert isinstance(page, Page)
    return page.evaluate(
        PROBE,
        {
            **arguments,
            "math": page.evaluate_handle(MATH_LIBRARY),
            "fontAdvance": page.evaluate_handle(FONT_ADVANCE),
        },
    )


def _run(page: object, findings: list[str], medium: str) -> Report:
    """One pass of the probe, with its findings prefixed by the medium."""
    from playwright.sync_api import Page  # noqa: PLC0415

    assert isinstance(page, Page)
    page.evaluate(SETTLED)
    page.evaluate(_STOP_LOADING_SAMPLER)
    probe: Report = _walk(page, PROBE_ARGUMENTS)
    findings.extend(f"{medium}: {finding}" for finding in probe["findings"])
    return probe


def _drawn_face(page: object, session: object, *, scope: str) -> tuple[str | None, list[str]]:
    """The face Blink actually draws one Latin run of a formula from, and its text.

    `CSS.getPlatformFontsForNode` is the only answer that is not a restatement of the
    cascade: it names the face the glyphs came out of, after matching, `unicode-range` and
    every fallback. That is what makes it worth a CDP session here -- the in-page walk can
    only compare one declaration against another.
    """
    from playwright.sync_api import CDPSession, Page  # noqa: PLC0415

    assert isinstance(page, Page)
    assert isinstance(session, CDPSession)
    mark = "kpress-math-face-probe"
    text = page.evaluate(
        _MARK_LATIN_RUN,
        {"scope": scope, "mark": mark, "math": page.evaluate_handle(MATH_LIBRARY)},
    )
    if text is None:
        return None, []
    try:
        root = session.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
        node = session.send("DOM.querySelector", {"nodeId": root, "selector": f"#{mark}"})
        fonts = session.send("CSS.getPlatformFontsForNode", {"nodeId": node["nodeId"]})
        return text, [str(font["familyName"]) for font in fonts.get("fonts", [])]
    finally:
        page.evaluate(_UNMARK_RUN, mark)


def _check_drawn(
    page: object,
    findings: list[str],
    medium: Literal["screen", "print"],
    *,
    prose_font: str = "serif",
) -> list[str]:
    """Sample actual captions, prose, and an interactive readout in each medium."""
    from playwright.sync_api import Page  # noqa: PLC0415

    assert isinstance(page, Page)
    drawn: list[str] = []
    sans_prefix = SANS_FACE if medium == "screen" else "KPress Print Sans"
    # The sans reading preference makes the bold prose slot reachable. Sample that
    # expression so the browser proves the newly retained print instance actually draws.
    prose_scope = ".kpress-prose > p .katex"
    if prose_font == "sans":
        prose_scope += ":has(.mathbf)"
    contexts = [
        ("caption", ".kpress-figcaption .katex", sans_prefix),
        (
            "prose",
            prose_scope,
            sans_prefix if prose_font == "sans" else PROSE_FACE,
        ),
    ]
    # The interactive panels are intentionally omitted from the printed paper.
    if medium == "screen":
        contexts.append(("readout", '[id^="s-phi-"] .katex', sans_prefix))
    # Detaching a CDP session resets Chromium's emulated medium. One session per
    # glyph sample therefore checked only the first print sample in print; the serif
    # prose default concealed that reset. Keep the session through the whole medium
    # and restore its setting after detachment for the caller's subsequent work.
    session = page.context.new_cdp_session(page)
    try:
        session.send("DOM.enable")
        session.send("CSS.enable")
        for kind, scope, wanted in contexts:
            is_print = page.evaluate(_PRINT_MATCHES)
            actual_medium = "print" if is_print else "screen"
            if actual_medium != medium:
                findings.append(f"{medium}: {kind} font sampled in {actual_medium} mode")
            text, faces = _drawn_face(page, session, scope=scope)
            if text is None:
                findings.append(f"{medium}: no {kind} formula with a Latin run to draw from")
                continue
            drawn.append(f"{medium} {kind}: {text!r} from {', '.join(faces) or 'nothing'}")
            if not any(face.startswith(wanted) for face in faces):
                findings.append(
                    f"{medium}: {kind} mathematics is drawn from {faces or 'nothing'}, "
                    f"not from {wanted}"
                )
    finally:
        session.detach()
        page.emulate_media(media=medium)
    return drawn


def check(path: Path | str = PAGE, *, width: int = 1280) -> Report:
    """Check both saved reading faces in both media, including their actual font slots."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    findings: list[str] = []
    report: Report = {
        "nodes": 0,
        "marked": 0,
        "tables": [],
        "drawn": [],
        "first_paint": {},
        "prose_fonts": [],
        "bold_advances": [],
        "findings": findings,
    }
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            for prose_font in ("serif", "sans"):
                page = browser.new_page(
                    reduced_motion="reduce", viewport={"width": width, "height": 720}
                )
                try:
                    errors: list[str] = []
                    page.on("pageerror", lambda error, errors=errors: errors.append(str(error)))
                    page.add_init_script(applied(_SAVE_PROSE_FONT, {"proseFont": prose_font}))
                    page.add_init_script(MATH_LIBRARY_INIT)
                    page.add_init_script(FIRST_PAINT_SCRIPT)
                    page.goto(page_url(path), wait_until="load")
                    page.wait_for_selector(READY, timeout=60_000)
                    selected = page.evaluate(_PROSE_FONT_SELECTED)
                    if selected != prose_font:
                        findings.append(
                            f"{prose_font}: saved reading preference was not applied"
                        )
                    report["prose_fonts"].append(prose_font)
                    screen = _run(page, findings, f"{prose_font} screen")
                    report["nodes"] += screen["nodes"]
                    report["marked"] += screen["marked"]
                    report["tables"].extend(
                        f"{prose_font}: {table}" for table in screen["tables"]
                    )
                    for medium in ("screen", "print"):
                        if medium == "print":
                            page.emulate_media(media="print")
                            page.set_viewport_size(PRINT_VIEWPORT)
                            probe = _run(page, findings, f"{prose_font} print")
                        else:
                            probe = screen
                        advances = probe.get("bold_advances", [])
                        report["bold_advances"].extend(
                            f"{prose_font} {medium}: {advance}" for advance in advances
                        )
                        if prose_font == "sans" and not advances:
                            findings.append(
                                f"sans {medium}: no bold mathematics measured at the 650 slot"
                            )
                        drawn_findings: list[str] = []
                        report["drawn"].extend(
                            f"{prose_font} {drawn}"
                            for drawn in _check_drawn(
                                page, drawn_findings, medium, prose_font=prose_font
                            )
                        )
                        findings.extend(f"{prose_font} {finding}" for finding in drawn_findings)
                    paint = page.evaluate(_FIRST_PAINT_SUMMARY)
                    report["first_paint"][prose_font] = paint or {}
                    # A reference error can leave a plausible page with the wrong tables.
                    findings.extend(f"{prose_font} page error: {error}" for error in errors)
                finally:
                    page.close()
            return report
        finally:
            browser.close()


#: Two paragraphs with a formula each, and the two font tokens the walk reads them by.
#: The tokens are what the page carries, so the fixture states the same thing the cascade
#: does on the real page rather than a simplification of it.
SELF_TEST_FIXTURE = f"""<!doctype html><html><head><style>
  body {{
    --kpress-font-sans: "{SANS_FACE} Variable", sans-serif;
    --kpress-font-prose: "{PROSE_FACE}", serif;
  }}
  .sans {{ font-family: var(--kpress-font-sans); }}
  .prose {{ font-family: var(--kpress-font-prose); }}
</style></head><body>
  <p class="prose"><span id="a"><span class="katex">x</span></span></p>
  <p class="sans"><span id="b"><span class="katex">y</span></span></p>
</body></html>"""


_INSTALL_SEAM_STUB = probe(PROBES, "check_math_faces/install_seam_stub")
_ADD_DORMANT_AND_HIDDEN_MATH = probe(PROBES, "check_math_faces/add_dormant_and_hidden_math")
_MARK_BOTH_SANS = probe(PROBES, "check_math_faces/mark_both_sans")
_ADD_BOLD_RUN = probe(PROBES, "check_math_faces/add_bold_run")
_FAKE_FIRST_PAINT = probe(PROBES, "check_math_faces/fake_first_paint")
_UNREADY_FIRST_REQUIRED = probe(PROBES, "check_math_faces/unready_first_required")
_LATE_FORMULA_FAILURE = probe(PROBES, "check_math_faces/late_formula_failure")
_CLEAR_UNREADY_MATH = probe(PROBES, "check_math_faces/clear_unready_math")
_SUPPORT_SANS_BOLD = probe(PROBES, "check_math_faces/support_sans_bold")
_MATCHING_BOLD_METRIC = probe(PROBES, "check_math_faces/matching_bold_metric")
_WIDEN_BOLD_METRIC = probe(PROBES, "check_math_faces/widen_bold_metric")
_PRINT_SAMPLING_FIXTURE = probe(PROBES, "check_math_faces/print_sampling_fixture")


def self_test() -> None:
    """Check that the walk objects to each disagreement it exists to find."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    arguments = PROBE_ARGUMENTS
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            page = browser.new_page()
            page.set_content(SELF_TEST_FIXTURE)
            bare: Report = _walk(page, arguments)
            if not any("its init did not run" in f for f in bare["findings"]):
                raise SystemExit("math face self-test accepted a page with no init")
            # With a seam in place, the sans paragraph's unmarked formula is the defect.
            page.evaluate(_INSTALL_SEAM_STUB)
            page.evaluate(_ADD_DORMANT_AND_HIDDEN_MATH)
            unmarked: Report = _walk(page, arguments)
            if unmarked["nodes"] != 3:
                raise SystemExit(
                    "math face self-test lost hidden certificate math "
                    "or included a dormant variant"
                )
            if not any("sans words, serif mathematics" in f for f in unmarked["findings"]):
                raise SystemExit("math face self-test accepted serif math under sans words")
            page.evaluate(_MARK_BOTH_SANS)
            marked: Report = _walk(page, arguments)
            if not any("serif words, sans mathematics" in f for f in marked["findings"]):
                raise SystemExit("math face self-test accepted sans math under serif words")
            page.evaluate(_ADD_BOLD_RUN)
            bold: Report = _walk(page, arguments)
            if not any("undeclared normal 650 slot" in f for f in bold["findings"]):
                raise SystemExit("math face self-test accepted bold math in a sans context")
            page.evaluate(_FAKE_FIRST_PAINT)
            unused: Report = _walk(page, arguments)
            if any("was painted before" in f for f in unused["findings"]):
                raise SystemExit("math face self-test rejected an unused unloaded font")
            page.evaluate(_UNREADY_FIRST_REQUIRED)
            required: Report = _walk(page, arguments)
            if not any("was painted before" in f for f in required["findings"]):
                raise SystemExit("math face self-test accepted an unavailable required font")
            page.evaluate(_LATE_FORMULA_FAILURE)
            later: Report = _walk(page, arguments)
            if not any("a formula appeared before" in f for f in later["findings"]):
                raise SystemExit("math face self-test missed a later formula's font failure")
            page.evaluate(_CLEAR_UNREADY_MATH)
            page.evaluate(_SUPPORT_SANS_BOLD)
            supported: Report = _walk(page, arguments)
            if any(
                "undeclared" in f or "serif words, sans mathematics" in f
                for f in supported["findings"]
            ):
                raise SystemExit("math face self-test rejected the supported sans reading face")
            page.evaluate(
                _MATCHING_BOLD_METRIC, {"fontAdvance": page.evaluate_handle(FONT_ADVANCE)}
            )
            matching_advance: Report = _walk(page, arguments)
            if not matching_advance.get("bold_advances") or any(
                "does not match its 650 metrics" in finding
                for finding in matching_advance["findings"]
            ):
                raise SystemExit("math face self-test rejected matching bold glyph metrics")
            page.evaluate(_WIDEN_BOLD_METRIC)
            wrong_advance: Report = _walk(page, arguments)
            if not any(
                "does not match its 650 metrics" in finding
                for finding in wrong_advance["findings"]
            ):
                raise SystemExit(
                    "math face self-test accepted a declared face at wrong metrics"
                )
            page.evaluate(_PRINT_SAMPLING_FIXTURE)
            page.emulate_media(media="print")
            sampled_findings: list[str] = []
            samples = _check_drawn(page, sampled_findings, "print")
            if (
                len(samples) != 2
                or any("font sampled in" in f for f in sampled_findings)
                or not page.evaluate(_PRINT_MATCHES)
            ):
                raise SystemExit("math face self-test lost print emulation across font samples")
        finally:
            browser.close()
    print(
        "math face self-test passed: init, face/slot mismatches, "
        "first-visible glyph readiness, print font sampling"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "page", nargs="?", default=str(PAGE), help="Local HTML or live page URL"
    )
    parser.add_argument(
        "--width", type=int, default=1280, help="Screen viewport width in CSS px"
    )
    parser.add_argument(
        "--self-test", action="store_true", help="Exercise the walk with known fixtures"
    )
    args = parser.parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    if args.width <= 0:
        parser.error("--width must be positive")
    report = check(args.page, width=args.width)
    print(json.dumps(report, indent=2))
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
