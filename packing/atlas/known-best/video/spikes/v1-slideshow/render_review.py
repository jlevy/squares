#!/usr/bin/env python3
"""Headless review of the candidate: layout bounds for every n, then screenshots.

    render_review.py [--shots N,N,...] [--fade N] [--out DIR] [--prefix P] [--skip-measure]

Measures, for every n at its dwell, the facts panel's bottom and right edges, any
intrusion of a value line into the note under it, the baseline of the exact line,
the top of the lower-bound line, which value line the degree note sits under, the
computed font size, family and weight of every text-bearing element on the stage,
the faces the document declares, and the footer's fit; then checks them against
the stage budget: the panel ends above the footer (which is above the progress
bar), inside x = 1830; no stage text is smaller than 28px and at most four sizes
are in use; the lower-bound line is at one y for every n; the degree note is
directly under the exact form where there is one and under the side value
otherwise; nothing serif resolves to a weight other than 400 and no PT Serif 700
face is declared; the bar never moves backwards and the cursor reads n. Then renders 1920x1080
captures (`?capture=1`) of the named n at their dwell and one mid-fade instant
into review/<prefix>n<NNN>.png, and measures the headline's ink so the `n =`
line is checked by pixels: above the numeral, flush left with it.

`survey()` and `check()` are importable; test_candidate.py runs them when
Playwright is available.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PANEL_RIGHT_LIMIT = 1830  # the stage's right margin
MIN_FONT_PX = 28
MAX_DISTINCT_SIZES = 4
MAX_SIZE_RATIO = 4.5

# The two measurement scripts below are JavaScript source handed to the browser. Their
# line lengths are the script's own formatting, not Python's, so E501 is waived for each
# literal as a whole rather than rewrapping code the page has to parse.
MEASURE_JS = """() => {
  const facts = document.querySelector('#facts .facts');
  const r = facts.getBoundingClientRect();
  let right = 0, bottom = 0;
  facts.querySelectorAll('*').forEach((el) => {
    // The drawn radical's <use> reports the geometry of its 400000-unit path, not
    // the clipped box it is drawn in; the box itself (the svg element) is measured.
    if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') return;
    const b = el.getBoundingClientRect();
    if (b.width === 0 && b.height === 0) return;
    if (b.right > right) right = b.right;
    if (b.bottom > bottom) bottom = b.bottom;
  });
  // How far the deepest ink of a value line reaches into the note line under it:
  // positive means the two overlap. The note's cap top sits about 6px below the
  // top of its 30px line; the radical box and the fraction box are measured as
  // boxes, which is where their ink ends.
  let intrusion = -999;
  facts.querySelectorAll('.line').forEach((line) => {
    const sub = line.nextElementSibling;
    if (!sub || !sub.classList.contains('sub') || !sub.textContent) return;
    let deepest = line.getBoundingClientRect().top;
    line.querySelectorAll('*').forEach((el) => {
      if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') return;
      const b = el.getBoundingClientRect();
      if (b.height && b.bottom > deepest) deepest = b.bottom;
    });
    const d = deepest - (sub.getBoundingClientRect().top + 6);
    if (d > intrusion) intrusion = d;
  });
  // The exact line's baseline, via its equals sign, when the line is not empty.
  const eq = facts.querySelector('.line.exact .eqsign');
  const eqTop = eq ? eq.getBoundingClientRect().top : null;
  // The lower-bound line's top, which must not depend on the order of the exact
  // slot and the degree note above it; and the degree note's seat: the value line
  // directly above it and its distance from that line's bottom (0, or the 5px a
  // nested radical's line is lifted by).
  const exact = facts.querySelector('.line.exact');
  const lowerTop = facts.querySelector('.line.lower').getBoundingClientRect().top;
  const degree = facts.querySelector('.sub .degree');
  let degreeUnder = null, degreeGap = null;
  if (degree) {
    const sub = degree.parentElement;
    const above = sub.previousElementSibling;
    degreeUnder = above.classList.contains('side') ? 'side' : above.classList.contains('exact') ? 'exact' : above.className;
    degreeGap = sub.getBoundingClientRect().top - above.getBoundingClientRect().bottom;
  }
  // Every element on the stage that directly holds text: its computed size, and
  // its computed family and weight (the first family of the stack is the one the
  // rule asks for; PT Serif is embedded at 400 only, so any other weight on a
  // serif element would be synthesised).
  const sizes = new Set();
  const serifWeights = new Set();
  const weights = new Set();
  document.querySelectorAll('#stage *').forEach((el) => {
    for (const node of el.childNodes) {
      if (node.nodeType === 3 && node.textContent.trim()) {
        const cs = getComputedStyle(el);
        sizes.add(parseFloat(cs.fontSize));
        const family = cs.fontFamily.split(',')[0].replace(/"/g, '').trim();
        weights.add(family + ' ' + cs.fontWeight);
        if (family === 'PT Serif') serifWeights.add(cs.fontWeight);
        break;
      }
    }
  });
  // The faces the document declares, whatever their load state.
  const faces = [];
  document.fonts.forEach((f) => faces.push(f.family.replace(/"/g, '') + '|' + f.style + '|' + f.weight));
  const footer = document.querySelector('.stage-footer');
  const spans = footer.querySelectorAll(':scope > span');
  const fb = footer.getBoundingClientRect();
  return {
    intrusion, eqTop, lowerTop, degreeUnder, degreeGap,
    exactEmpty: exact.classList.contains('empty'), exactTall: exact.classList.contains('tall'),
    serifWeights: Array.from(serifWeights).sort(), weights: Array.from(weights).sort(), faces: faces.sort(),
    top: r.top, bottom: Math.max(r.bottom, bottom), right: Math.max(r.right, right),
    badges: facts.querySelectorAll('.status .badge').length,
    open: facts.querySelectorAll('.open li').length,
    record: facts.querySelectorAll('.record div').length,
    recordHeight: facts.querySelector('.record').getBoundingClientRect().height,
    fill: document.getElementById('progress-fill').style.width,
    cursor: document.getElementById('progress-cursor').textContent,
    cursorGap: (() => {
      const c = document.getElementById('progress-cursor').getBoundingClientRect();
      const lo = document.querySelector('#progress .end.lo').getBoundingClientRect();
      const hi = document.querySelector('#progress .end.hi').getBoundingClientRect();
      return Math.min(c.left - lo.right, hi.left - c.right);
    })(),
    sizes: Array.from(sizes).sort((a, b) => a - b),
    footerTop: fb.top,
    footerGap: spans.length === 2 ? spans[1].getBoundingClientRect().left - spans[0].getBoundingClientRect().right : null,
    footerOverflow: footer.scrollWidth - footer.clientWidth,
    barTop: document.getElementById('progress').getBoundingClientRect().top,
    trackTop: document.querySelector('#progress .track').getBoundingClientRect().top,
  };
}"""  # noqa: E501

HEADLINE_JS = """() => {
  const f = document.querySelector('#facts');
  const box = (sel) => { const b = f.querySelector(sel).getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; };
  return { lead: box('.lead'), var: box('.lead .var'), eq: box('.lead .eq'), headline: box('.headline'), nval: box('.headline .nval') };
}"""  # noqa: E501


def ink_box(image, x0: int, y0: int, x1: int, y1: int) -> tuple[int, int, int, int] | None:
    """Bounding box (left, top, right, bottom) of non-white ink inside the window,
    in page pixels.
    """
    px = image.load()
    left = top = right = bottom = None
    for y in range(y0, y1):
        for x in range(x0, x1):
            if sum(px[x, y][:3]) < 600:
                left = x if left is None or x < left else left
                right = x if right is None or x > right else right
                top = y if top is None else top
                bottom = y
    # All four are set together in the loop above; naming that lets the checker see it.
    if left is None or top is None or right is None or bottom is None:
        return None
    return (left, top, right, bottom)


def survey(
    page_url: str,
    shots: list[int],
    fade: int,
    out: Path | None,
    prefix: str,
    *,
    measure: bool = True,
) -> dict:
    """Seek every n, measure, and (when `out` is given) write the captures."""
    # Playwright is an optional extra: importing it here keeps the module importable,
    # and `check()` usable on a recorded result, without it. PLC0415 waived for that.
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    result: dict = {"measures": {}, "shots": {}, "headline": {}}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        page.goto(page_url)
        page.evaluate("atlasVideo.ready")
        timing = page.evaluate("atlasVideo.timing()")
        count = page.evaluate("atlasVideo.count")
        slot = timing["dwell"] + timing["fade"]
        result["count"] = count

        def dwell_time(n: int) -> float:
            return (n - 1) * slot + timing["dwell"] / 2

        if measure:
            for n in range(1, count + 1):
                page.evaluate(f"atlasVideo.seek({dwell_time(n)})")
                result["measures"][n] = page.evaluate(MEASURE_JS)

        if out is not None:
            out.mkdir(parents=True, exist_ok=True)
            for n in shots:
                state = page.evaluate(f"atlasVideo.seek({dwell_time(n)})")
                path = out / f"{prefix}n{n:03d}.png"
                page.screenshot(path=str(path))
                result["shots"][n] = (path, state)
                result["headline"][n] = page.evaluate(HEADLINE_JS)
            fade_time = (fade - 1) * slot + timing["dwell"] + timing["fade"] * 0.5
            state = page.evaluate(f"atlasVideo.seek({fade_time})")
            path = out / f"{prefix}fade-{fade:03d}-{fade + 1:03d}.png"
            page.screenshot(path=str(path))
            result["shots"]["fade"] = (path, state)
        browser.close()
    return result


def check(result: dict, *, verbose: bool = True) -> list[str]:
    """The layout rules over every measured n. Returns the failures (empty is a pass)."""
    failures: list[str] = []
    measures = result["measures"]
    if not measures:
        return failures
    say = print if verbose else (lambda *_a, **_k: None)

    worst_bottom = sorted(((m["bottom"], n) for n, m in measures.items()), reverse=True)
    worst_right = sorted(((m["right"], n) for n, m in measures.items()), reverse=True)
    worst_intrusion = sorted(((m["intrusion"], n) for n, m in measures.items()), reverse=True)
    footer_top = min(m["footerTop"] for m in measures.values())
    bar_top = min(m["barTop"] for m in measures.values())
    say("panel bottom, worst 8:", [(round(b), n) for b, n in worst_bottom[:8]])
    say("panel right, worst 5:", [(round(r), n) for r, n in worst_right[:5]])
    say(
        "value-into-note intrusion, worst 5 (px, <0 is clear):",
        [(round(d, 1), n) for d, n in worst_intrusion[:5]],
    )
    say(
        f"footer top {footer_top:.0f}, progress bar top {bar_top:.0f}, "
        f"track top {measures[1]['trackTop']:.0f}"
    )
    if worst_bottom[0][0] > footer_top:
        failures.append(
            f"panel runs to y={worst_bottom[0][0]:.0f} at n={worst_bottom[0][1]} "
            f"(footer at {footer_top:.0f})"
        )
    if worst_bottom[0][0] > bar_top:
        failures.append(f"panel runs under the progress bar at n={worst_bottom[0][1]}")
    if worst_right[0][0] > PANEL_RIGHT_LIMIT + 0.5:
        failures.append(
            f"panel runs to x={worst_right[0][0]:.0f} at n={worst_right[0][1]} "
            f"(limit {PANEL_RIGHT_LIMIT})"
        )
    if worst_intrusion[0][0] > 0:
        failures.append(
            f"a value line reaches {worst_intrusion[0][0]:.1f}px into its note "
            f"at n={worst_intrusion[0][1]}"
        )

    last_fill = -1.0
    for n, m in measures.items():
        fill = float(m["fill"].rstrip("%"))
        if fill < last_fill:
            failures.append(f"n={n}: bar went backwards {last_fill} -> {fill}")
        last_fill = fill
        if m["cursor"] != str(n):
            failures.append(f"n={n}: cursor label {m['cursor']!r}")
        if m["open"] < 1:
            failures.append(f"n={n}: open group has no rows")
        if m["footerOverflow"] > 0:
            failures.append(f"n={n}: footer overflows by {m['footerOverflow']}px")
    say(f"bar at the last dwell: {last_fill}%")
    tightest = min((m["cursorGap"], n) for n, m in measures.items())
    say(f"riding n to the nearest end label, tightest: {tightest[0]:.0f}px at n={tightest[1]}")
    if tightest[0] < 8:
        failures.append(
            f"the riding n is {tightest[0]:.0f}px from an end label at n={tightest[1]}"
        )
    gaps = [m["footerGap"] for m in measures.values() if m["footerGap"] is not None]
    say(f"footer: gap between its two sentences {min(gaps):.0f}px")
    if min(gaps) < 40:
        failures.append(f"footer sentences are {min(gaps):.0f}px apart")

    # The exact line's baseline is the same wherever the line is filled.
    eq_tops = sorted(
        {round(m["eqTop"], 1) for m in measures.values() if m["eqTop"] is not None}
    )
    say(f"exact line's equals-sign top across n: {eq_tops}")
    if eq_tops and eq_tops[-1] - eq_tops[0] > 1.0:
        failures.append(f"the exact line's baseline moves between n: tops {eq_tops}")

    # The lower-bound line does not move between n, whichever way the exact slot
    # and the degree note are ordered above it.
    lower_tops = sorted({round(m["lowerTop"], 1) for m in measures.values()})
    say(f"lower-bound line's top across n: {lower_tops}")
    if lower_tops[-1] - lower_tops[0] > 0.5:
        failures.append(f"the lower-bound line moves between n: tops {lower_tops}")
    # The degree note sits directly under the value it annotates: the exact form
    # where there is one, the side value otherwise.
    under = {"side": 0, "exact": 0}
    for n, m in measures.items():
        if m["degreeUnder"] is None:
            continue
        want = "side" if m["exactEmpty"] else "exact"
        under[want] += 1
        lift = 5 if m["exactTall"] and not m["exactEmpty"] else 0
        if m["degreeUnder"] != want:
            failures.append(
                f"n={n}: the degree note sits under the {m['degreeUnder']} line, "
                f"not the {want}"
            )
        elif abs(m["degreeGap"] - lift) > 0.5:
            failures.append(
                f"n={n}: the degree note is {m['degreeGap']:.1f}px below the {want} line"
            )
    say(
        f"degree notes: {under['exact']} under an exact form, "
        f"{under['side']} under the side value"
    )
    # The faces: PT Serif at 400 only, and nothing serif on the stage asks for another
    # weight (the browser would synthesise a bold the page does not carry).
    serif_weights = sorted({w for m in measures.values() for w in m["serifWeights"]})
    weights = sorted({w for m in measures.values() for w in m["weights"]})
    faces = sorted({f for m in measures.values() for f in m["faces"]})
    say(f"computed family and weight over all n: {weights}")
    say(f"faces the document declares: {faces}")
    if serif_weights != ["400"]:
        failures.append(f"PT Serif elements resolve to weights {serif_weights}")
    if any(f.startswith("PT Serif|") and f.endswith("|700") for f in faces):
        failures.append("a PT Serif 700 face is declared")

    # The type scale, as computed by the browser over every text-bearing element.
    sizes = sorted({s for m in measures.values() for s in m["sizes"]})
    say(f"computed font sizes on the stage over all n: {sizes}")
    if sizes[0] < MIN_FONT_PX:
        failures.append(f"stage text at {sizes[0]}px, below {MIN_FONT_PX}")
    if len(sizes) > MAX_DISTINCT_SIZES:
        failures.append(f"{len(sizes)} distinct sizes on the stage: {sizes}")
    if sizes[-1] > MAX_SIZE_RATIO * sizes[0]:
        failures.append(
            f"largest size {sizes[-1]} is more than {MAX_SIZE_RATIO} x "
            f"the smallest {sizes[0]}"
        )
    lines = sorted(
        ((m["recordHeight"], m["record"], n) for n, m in measures.items()), reverse=True
    )
    say(
        "record block, tallest 5 (height px, rows, n):",
        [(round(h), r, n) for h, r, n in lines[:5]],
    )
    return failures


def check_headline(result: dict, *, verbose: bool = True) -> list[str]:
    """The `n =` line sits above the numeral and flush left with it, by the pixels.

    Each mark's ink is looked for in its own columns and its block's rows (a span's
    own box is the font's content area, which for the 96px numeral reaches up into
    the `n =` line); the band between the two inks, in the numeral's columns, must
    be blank.
    """
    try:
        # Pillow is an optional extra, and the pixel check is skipped without it; the
        # import stays inside the try for that reason, so PLC0415 is waived.
        from PIL import Image  # noqa: PLC0415
    except ImportError:
        return []
    failures: list[str] = []
    for n, boxes in result["headline"].items():
        path, _state = result["shots"][n]
        image = Image.open(path).convert("RGB")
        lead_rows = (round(boxes["lead"][1]), round(boxes["lead"][3]))
        head_rows = (round(boxes["headline"][1]), round(boxes["headline"][3]))
        var_cols = (round(boxes["var"][0]), round(boxes["var"][2]))
        eq_cols = (round(boxes["eq"][0]), round(boxes["eq"][2]))
        nval_cols = (round(boxes["nval"][0]), round(boxes["nval"][2]))
        var_ink = ink_box(image, var_cols[0], lead_rows[0], var_cols[1], lead_rows[1])
        eq_ink = ink_box(image, eq_cols[0], lead_rows[0], eq_cols[1], lead_rows[1])
        num_ink = ink_box(image, nval_cols[0], head_rows[0], nval_cols[1], head_rows[1])
        if not (var_ink and eq_ink and num_ink):
            failures.append(f"n={n}: headline ink not found {var_ink, eq_ink, num_ink}")
            continue
        lead_bottom = max(var_ink[3], eq_ink[3])
        band = ink_box(image, nval_cols[0], lead_bottom + 1, nval_cols[1], num_ink[1])
        gap = num_ink[1] - lead_bottom
        offset = var_ink[0] - num_ink[0]
        box_offset = boxes["lead"][0] - boxes["headline"][0]
        if verbose:
            print(
                f"n={n}: `n =` ink y {min(var_ink[1], eq_ink[1])}..{lead_bottom}, "
                f"numeral ink y {num_ink[1]}..{num_ink[3]} "
                f"(gap {gap}px, band {'blank' if band is None else 'inked'}); "
                f"n ink left {var_ink[0]}, numeral ink left {num_ink[0]} "
                f"(offset {offset}px, boxes {box_offset:.1f}px)"
            )
        if gap < 4 or band is not None:
            failures.append(
                f"n={n}: the `n =` line is not clear above the numeral (gap {gap}px)"
            )
        if abs(box_offset) > 0.5:
            failures.append(
                f"n={n}: the `n =` line is not flush left with the numeral "
                f"({box_offset:.1f}px)"
            )
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shots", default="5,11,28,147,268,323")
    parser.add_argument(
        "--fade",
        type=int,
        default=147,
        help="n whose fade into n+1 is captured at its midpoint",
    )
    parser.add_argument("--out", type=Path, default=HERE / "review")
    parser.add_argument("--prefix", default="r4-")
    parser.add_argument("--skip-measure", action="store_true")
    args = parser.parse_args(argv)
    page_url = (HERE / "index.html").as_uri() + "?capture=1"
    shots = [int(s) for s in args.shots.split(",") if s]

    result = survey(
        page_url, shots, args.fade, args.out, args.prefix, measure=not args.skip_measure
    )
    failures = check(result)
    for path, state in result["shots"].values():
        print(f"{path.name}: {state}")
    failures += check_headline(result)
    for failure in failures:
        print("FAIL:", failure)
    print("review:", "FAILED" if failures else "ok")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
