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
as every formula's digits changing font on load (`think-q5df`). An init script samples
the first CSS-visible `.katex` node and records the status of every embedded math face;
each one has to be loaded already. Hidden staging nodes do not count as visible
formulas. The separate delayed-font checker also verifies that native MathML and early
interactive renders stay hidden during this wait.

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

from devtools.check_math_loading import FIRST_PAINT_SCRIPT, page_url
from devtools.check_print_layout import PRINT_VIEWPORT
from devtools.render_explainer import MATH_WRAPPERS
from devtools.render_explainer_pdf import BROWSER_OVERRIDE, PAGE, READY, SETTLED

#: The faces the composites draw their Latin and digits from, by the prefix Blink answers
#: `CSS.getPlatformFontsForNode` with. A variable face comes back as the instance it is at
#: (`Source Sans 3 ExtraLight`), and a static instance under its own name, so both sides
#: are prefixes rather than exact names.
SANS_FACE = "Source Sans 3"
PROSE_FACE = "PT Serif"

#: kpress's math markup, which the walk climbs through to find the words. The list is the
#: renderer's, since the init walks the same wrappers for the same reason.
PROBE_ARGUMENTS: dict[str, object] = {
    "wrappers": MATH_WRAPPERS,
}


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


#: The walk. Returns one `{ nodes, marked, tables, findings }` per medium.
#:
#: The face of the WORDS around an expression is read off the nearest ancestor that is not
#: part of the math markup. kpress's `.kpress-math` and `.kpress-math-render` wrappers
#: declare the prose face themselves, and `.katex` is where `katex-text-face.css` puts the
#: composite, so asking any of those would answer with the choice already made rather than
#: with the sentence the formula sits in.
#:
#: Sans or prose is decided by comparing that container's computed `font-family` against
#: both of the tokens in scope on it, `--kpress-font-sans` and `--kpress-font-prose`. Both
#: sides come from the same medium's computed values, so the test reads the print stack
#: under print and the screen stack on screen without naming either, and a container that
#: matches neither is reported rather than guessed at.
#:
#: The re-typeset comparison recovers each expression's own TeX from the annotation KaTeX
#: writes into its MathML copy, so it needs no source of its own and covers whatever the
#: page happens to contain. The probe span is appended to the same container, so it
#: inherits the same font stack and the same size, and it is removed again; nothing here
#: leaves a mark on the page beyond the marks the page itself made.
PROBE = r"""({ wrappers }) => {
  const findings = [];
  const boldAdvances = [];
  const nodes = [...document.querySelectorAll('.katex')];
  const sans = (node) => !!node.closest('[data-kpress-math-face="sans"]');
  const marked = nodes.filter(sans);
  const first = (value) => (value || '').split(',')[0].trim().replace(/^["']|["']$/g, '');

  const container = (node) => {
    let el = node.parentElement;
    while (el && el.matches(wrappers)) el = el.parentElement;
    return el;
  };
  const where = (el) => {
    const parts = [];
    for (let e = el; e && e !== document.body; e = e.parentElement) {
      const cls = typeof e.className === 'string' && e.className.trim()
        ? '.' + e.className.trim().split(/\s+/).join('.') : '';
      parts.unshift(e.tagName.toLowerCase() + cls);
      if (parts.length > 3) break;
    }
    return parts.join(' > ');
  };

  const seam = globalThis.kpressMathText;
  if (!seam || typeof seam.installTablesFor !== 'function') {
    findings.push('the page installed no math text seam; its init did not run');
    return { nodes: nodes.length, marked: marked.length, tables: [],
      bold_advances: boldAdvances, findings };
  }
  if (nodes.length === 0) findings.push('the page rendered no mathematics at all');

  for (const node of nodes) {
    const words = container(node);
    if (!words) continue;
    const style = getComputedStyle(words);
    const drawn = first(style.fontFamily);
    const isSans = drawn === first(style.getPropertyValue('--kpress-font-sans'));
    const isProse = drawn === first(style.getPropertyValue('--kpress-font-prose'));
    const at = where(node) + ' [' + drawn + ']';
    if (!isSans && !isProse) {
      findings.push('mathematics in words set in neither the sans nor the prose: ' + at);
    } else if (isSans && !sans(node)) {
      findings.push('sans words, serif mathematics: ' + at);
    } else if (isProse && !isSans && sans(node)) {
      findings.push('serif words, sans mathematics: ' + at);
    }
  }

  /* Read the emitted declarations, not the renderer's pruning table: a saved sans
     preference moves prose's bold mathematics into this family too. CSS can synthesize
     a missing bold slot without reporting a font load failure, but the resulting glyphs
     no longer match KaTeX's 650 metrics. `.textbf` requests upstream's 700, which CSS
     matches to the composite's pinned 650 slot. */
  const sansSlots = new Set([...document.fonts]
    .filter(face => first(face.family) === 'KPress Math Text Sans')
    .map(face => face.style + ' ' + face.weight));
  for (const node of marked) {
    for (const run of node.querySelectorAll('.mathbf, .boldsymbol, .textbf')) {
      const style = getComputedStyle(run);
      const slot = style.fontStyle + ' 650';
      if (!sansSlots.has(slot)) {
        findings.push('sans mathematics requests an undeclared ' + slot + ' slot: '
          + where(run));
      }
      /* A declared family alone cannot tell a real 650 instance from synthetic bold.
         Compare a visible upright Latin glyph with the 650 advance in KPress's table.
         Blink rounds inline advances to 1/64px; larger disagreement is a wrong face. */
      if (style.fontStyle === 'normal' && /^[A-Za-z]$/.test(run.textContent)
          && run.checkVisibility({ visibilityProperty: true })) {
        const table = globalThis.kpressKatexTextMetrics?.sans?.['Main-Bold'];
        const metric = table?.[run.textContent.codePointAt(0)];
        if (!metric) {
          findings.push('no 650 metric for sans bold ' + run.textContent);
          continue;
        }
        const actual = run.getBoundingClientRect().width;
        const expected = metric[4] * parseFloat(style.fontSize);
        boldAdvances.push(run.textContent + ': ' + actual + 'px | 650: ' + expected + 'px');
        if (Math.abs(actual - expected) > 1 / 64) {
          findings.push('sans bold glyph does not match its 650 metrics: '
            + run.textContent + ' draws ' + actual + 'px, expected ' + expected + 'px');
        }
      }
    }
  }

  /* One expression of each kind, re-typeset from its own source under both sets. */
  const tables = [];
  const source = (node) => {
    const tex = node.querySelector('annotation[encoding="application/x-tex"]');
    return tex ? tex.textContent : null;
  };
  const geometry = (el) =>
    [...el.querySelectorAll('.vlist')].map((v) => v.style.height).join('|');
  const under = (node, host) => {
    const probe = document.createElement('span');
    probe.style.position = 'absolute';
    probe.style.visibility = 'hidden';
    container(node).appendChild(probe);
    /* The seam picks the set from the element it is handed, so it is handed one that
       lives where the set under test does; `probe` then only has to be somewhere the
       size and the stack are the node's own. */
    seam.installTablesFor(host, globalThis.squaresMath?.context);
    try {
      katex.render(source(node), probe, { throwOnError: false });
    } catch (error) {
      probe.textContent = '';
    }
    const measured = geometry(probe);
    probe.remove();
    return measured;
  };

  /* Detached control hosts select either table without inheriting the reader's global
     preference. The measured formula itself stays attached under its actual cascade. */
  const sansHost = document.createElement('span');
  sansHost.className = 'sans-text';
  const proseHost = document.createElement('span');
  const contexts = [
    ['supporting', marked.filter(node => !node.closest('.kpress-prose > p'))],
    ['prose', nodes.filter(node => node.closest('.kpress-prose > p'))],
  ];
  for (const [label, pool] of contexts) {
    const node = pool.find((n) => n.querySelector('.vlist') && source(n));
    if (!node) {
      findings.push('no ' + label + ' fraction to check the metric table on');
      continue;
    }
    const live = geometry(node);
    const asSans = under(node, sansHost);
    const asProse = under(node, proseHost);
    tables.push(label + ': live ' + live + ' | sans ' + asSans + ' | prose ' + asProse);
    if (asSans === asProse) {
      findings.push(label + ': the two metric sets lay this expression out identically, '
        + 'so the comparison proves nothing');
    } else if (live !== (sans(node) ? asSans : asProse)) {
      findings.push(label + ': laid out from the wrong metric table -- live ' + live
        + ', sans ' + asSans + ', prose ' + asProse);
    }
  }
  seam.restore();

  /* The self-contained page must decode its math faces before exposing any formula. */
  const paint = globalThis.__mathFirstPaint;
  if (!paint) {
    findings.push('nothing recorded the first mathematics node; the init script did not run');
  } else {
    const late = paint.faces
      .filter((face) => (face.family.startsWith('KaTeX_')
        || face.family.startsWith('KPress Math Text')) && face.status !== 'loaded')
      .map((face) => face.family + ' ' + face.style + ' ' + face.weight
        + ' (' + face.status + ')');
    if (late.length) {
      findings.push('mathematics was painted before ' + late.length + ' of its faces: '
        + late.join(', '));
    }
  }
  return { nodes: nodes.length, marked: marked.length, tables,
    bold_advances: boldAdvances, findings };
}"""


def _run(page: object, findings: list[str], medium: str) -> Report:
    """One pass of the probe, with its findings prefixed by the medium."""
    from playwright.sync_api import Page  # noqa: PLC0415

    assert isinstance(page, Page)
    page.evaluate(SETTLED)
    page.evaluate(
        "globalThis.__mathLoadingState && (globalThis.__mathLoadingState.stop = true)"
    )
    probe: Report = page.evaluate(PROBE, PROBE_ARGUMENTS)
    findings.extend(f"{medium}: {finding}" for finding in probe["findings"])
    return probe


#: One letter or digit of a formula, marked so CDP can find it. The composite claims the
#: Latin ranges and the digits and nothing else, so a run of operators or Greek would
#: answer with a KaTeX face whichever composite is in force and prove nothing.
_MARK = """({ scope, mark }) => {
  for (const node of document.querySelectorAll(scope)) {
    if (!node.checkVisibility({ visibilityProperty: true })) continue;
    for (const run of node.querySelectorAll('.mord')) {
      if (run.children.length === 0 && /^[0-9A-Za-z.]+$/.test(run.textContent.trim())) {
        run.id = mark;
        return run.textContent.trim();
      }
    }
  }
  return null;
}"""


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
    text = page.evaluate(_MARK, {"scope": scope, "mark": mark})
    if text is None:
        return None, []
    try:
        root = session.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
        node = session.send("DOM.querySelector", {"nodeId": root, "selector": f"#{mark}"})
        fonts = session.send("CSS.getPlatformFontsForNode", {"nodeId": node["nodeId"]})
        return text, [str(font["familyName"]) for font in fonts.get("fonts", [])]
    finally:
        page.evaluate(
            "mark => { const el = document.getElementById(mark);"
            " if (el) el.removeAttribute('id'); }",
            mark,
        )


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
            is_print = page.evaluate("matchMedia('print').matches")
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
                    page.add_init_script(
                        f"localStorage.setItem('kpress.proseFont', {json.dumps(prose_font)});"
                    )
                    page.add_init_script(FIRST_PAINT_SCRIPT)
                    page.goto(page_url(path), wait_until="load")
                    page.wait_for_selector(READY, timeout=60_000)
                    selected = page.evaluate("document.documentElement.dataset.kpressProseFont")
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
                    paint = page.evaluate(
                        "() => globalThis.__mathFirstPaint && { "
                        "at: globalThis.__mathFirstPaint.at, "
                        "faces: globalThis.__mathFirstPaint.faces.length }"
                    )
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


def self_test() -> None:
    """Check that the walk objects to each disagreement it exists to find."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    arguments = PROBE_ARGUMENTS
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            page = browser.new_page()
            page.set_content(SELF_TEST_FIXTURE)
            bare: Report = page.evaluate(PROBE, arguments)
            if not any("its init did not run" in f for f in bare["findings"]):
                raise SystemExit("math face self-test accepted a page with no init")
            # With a seam in place, the sans paragraph's unmarked formula is the defect.
            page.evaluate(
                "() => { globalThis.kpressMathText = "
                "{ installTablesFor: () => null, restore: () => undefined }; }"
            )
            unmarked: Report = page.evaluate(PROBE, arguments)
            if not any("sans words, serif mathematics" in f for f in unmarked["findings"]):
                raise SystemExit("math face self-test accepted serif math under sans words")
            page.evaluate(
                "() => { document.querySelector('#a').dataset.kpressMathFace = 'sans'; "
                "document.querySelector('#b').dataset.kpressMathFace = 'sans'; }"
            )
            marked: Report = page.evaluate(PROBE, arguments)
            if not any("serif words, sans mathematics" in f for f in marked["findings"]):
                raise SystemExit("math face self-test accepted sans math under serif words")
            page.evaluate(
                """() => {
                  const bold = document.createElement('span');
                  bold.className = 'mathbf';
                  document.querySelector('#b .katex').appendChild(bold);
                }"""
            )
            bold: Report = page.evaluate(PROBE, arguments)
            if not any("undeclared normal 650 slot" in f for f in bold["findings"]):
                raise SystemExit("math face self-test accepted bold math in a sans context")
            page.evaluate(
                """() => {
                  document.fonts.add(new FontFace('KPress Math Text Sans', 'local(Arial)',
                    {weight: '650'}));
                  document.body.style.setProperty('--kpress-font-prose',
                    '\"Source Sans 3 Variable\", sans-serif');
                  document.querySelector('#a').className = 'sans';
                }"""
            )
            supported: Report = page.evaluate(PROBE, arguments)
            if any(
                "undeclared" in f or "serif words, sans mathematics" in f
                for f in supported["findings"]
            ):
                raise SystemExit("math face self-test rejected the supported sans reading face")
            page.evaluate(
                """() => {
                  const bold = document.querySelector('.mathbf');
                  bold.textContent = 'D';
                  const advance = bold.getBoundingClientRect().width
                    / parseFloat(getComputedStyle(bold).fontSize);
                  globalThis.kpressKatexTextMetrics = {
                    sans: {'Main-Bold': {68: [0, 0, 0, 0, advance]}}
                  };
                }"""
            )
            matching_advance: Report = page.evaluate(PROBE, arguments)
            if not matching_advance.get("bold_advances") or any(
                "does not match its 650 metrics" in finding
                for finding in matching_advance["findings"]
            ):
                raise SystemExit("math face self-test rejected matching bold glyph metrics")
            page.evaluate("globalThis.kpressKatexTextMetrics.sans['Main-Bold'][68][4] += 0.25")
            wrong_advance: Report = page.evaluate(PROBE, arguments)
            if not any(
                "does not match its 650 metrics" in finding
                for finding in wrong_advance["findings"]
            ):
                raise SystemExit(
                    "math face self-test accepted a declared face at wrong metrics"
                )
            page.evaluate(
                """() => {
                  document.body.classList.add('kpress-prose');
                  document.querySelector('#b').parentElement.classList.add('kpress-figcaption');
                  document.querySelectorAll('.katex').forEach(node => {
                    node.innerHTML = '<span class="mord">x</span>';
                  });
                }"""
            )
            page.emulate_media(media="print")
            sampled_findings: list[str] = []
            samples = _check_drawn(page, sampled_findings, "print")
            if (
                len(samples) != 2
                or any("font sampled in" in f for f in sampled_findings)
                or not page.evaluate("matchMedia('print').matches")
            ):
                raise SystemExit("math face self-test lost print emulation across font samples")
        finally:
            browser.close()
    print("math face self-test passed: init, face/slot mismatches, print font sampling")


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
