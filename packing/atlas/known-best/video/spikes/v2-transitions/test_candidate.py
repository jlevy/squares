#!/usr/bin/env python3
"""Checks for the v2 transition candidate. Run with packing/.venv/bin/python3.

    packing/.venv/bin/python3 test_candidate.py

Asserts byte-identical regeneration on two runs, that every correspondence is a
bijection from n into n+1 with exactly one unmatched square, that the five
shared-picture pairs and every grid-to-grid pair are recognised as such, and that
index.html never references the network.

Revision 2 adds: the facts carry the poster's badges (only its vocabulary), the star
and the open list exactly as the composite record states them; each pair knows the
square that arrived in the pair before; the star polygon matches the atlas source;
scarlet is defined once in the page; and, in the headless shell, the progress bar is
a pure function of the clock, the two facts layers are never visible together, and
the scarlet mark sits where the requests put it.

Revision 3 adds: the `n =` line sits above the numeral (132 px) and shares its left
edge; the lower-bound line reads `s(n) ≥ value` for every open n with its note directly
below and is empty at fixed height for a proved n, the value taken from the record's
`lower.display`; KaTeX_Main is embedded as "Atlas Symbols" with the relation range and
size-adjust, and the headless shell confirms through CDP that `≤`, `≥` and `√` are set
in it; the `≈` badge is that face's outline; and every fill the page draws, over every
frame of index-all.html at rest, at the arrival and mid block motion, is an entry of the
20 x 5 shade table revision 11 colours by — the table being the atlas's own
`square_fill_palette(hue_count=20, shades_per_hue=5)`, compared here against it.

Revision 4 adds the type scale: the numeral is PT Serif Regular (weight 400) at 96 px
and its box offset is the one the build derives from the regular face's digit bearings
(recomputed here from the fonts); over every embedded pair, no text on the stage is
below 28 px, at most four distinct sizes appear (28 / 34 / 44 / 96), the numeral is at
most 4.5 times the smallest; and, at the start and the end of every embedded pair, the
panel's lowest text sits above the riding n and the progress bar, nothing runs past the
panel's right edge, and every slot's top and height are the same. The badge glyphs are
SVG marks in the poster's boxes and are not counted as stage text.

Revision 5 adds the identity chain (composed here from all 323 maps and compared with
the record's: every identity born at step k is in every frame from k to 324 exactly
once), the block statistics on every pair with each block's members rigid up to its
stated residual, the new-square rule and tie set on every pair, the arrival overlap
census, and in the headless shell: one DOM element per identity that is created once
and never re-keyed, the five motion modes reachable with `add-then-move` the default,
the new square fully in before anything moves in that mode and the blocks at their
final poses before it appears in `move-then-add`, and a block's members keeping their
mutual distances half way through the block motion.

Styles B (physics) and C (bodies) add one smoke check in the shell: the three styles cycle
through the API, each physical style renders 100->101 mid-move with finite poses and its
cached trajectory ends exactly on n+1's poses (C with fewer bodies than squares, the blocks
being rigid), and the tween is left showing.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PYTHON = Path(sys.executable)
SHARED_PICTURE_PAIRS = {147, 232, 264, 290, 295}
REPO = Path("/Users/levy/wrk/github/squares/.claude/worktrees/squares-viz-explanations-4ae624")
MANIFEST = REPO / "packing/atlas/known-best/manifest.json"
COMPOSITE = REPO / "packing/atlas/known-best/composite-figure.json"
ATLAS_SOURCE = REPO / "packing/devtools/build_known_best_atlas.py"
KATEX_MAIN = REPO / "vendor/kpress/src/kpress/format/static/katex/fonts/KaTeX_Main-Regular.woff2"
FONTS = REPO / "vendor/kpress/src/kpress/format/static/fonts"
TIMING = {"dwell": 1.0, "move": 1.4, "settle": 0.4}
# Revision 5's staging: the new square arrives over the first 30% of the move by default.
ARRIVAL_FRACTION = 0.3
PHASES = ["add-then-move", "move-then-add", "simultaneous", "rotate-first", "slide-first"]
NEW_RULES = {
    "prefix: square n+1 is appended",
    "shared picture: the catalogue's removed square",
    "lowest cost",
    "lowest cost, fewest contacts",
    "lowest cost, fewest contacts, highest position",
}
# Revision 4's type scale on the 1920 x 1080 stage, and the headline's face.
TYPE_SCALE = [28, 34, 44, 96]
# The headline is one line at one size: `n =` and the numeral both at 96 px, the numeral a
# HEADLINE_GAP_PX ink gap past the line. N_LINE_PX was 34 while the label sat above the
# number as a caption; it matches the numeral now, and this copy is read independently of
# the build so a change to one side has to be made on both.
NUMERAL_PX, NUMERAL_WEIGHT, N_LINE_PX, N_LINE_LEFT_PX = 96, 400, 96, 6
HEADLINE_GAP_PX = 16
NUMERAL_RATIO_MAX = 4.5
BADGE_VOCABULARY = {("O", "solid"), ("=", "solid"), ("≈", "muted"), ("R", "solid"), ("R", "muted")}
SYMBOL_RANGE = "U+2208, U+221A, U+2248, U+2264-2265, U+2308-230B"
SIDE_DISPLAY = re.compile(r"^s\((\d+)\) ([=≤≥]) (.+)$")
# Revision 11's colouring, which replaced the teal-to-citron sweep: one map, always on, no rule
# to choose. Hue is a function of the angle alone — the quarter turn cut into the two pinned
# tilts and eighteen five-degree bands — and shade is the square's full-side contact count, over
# the table `square_fill_palette(hue_count=20, shades_per_hue=5)` derives in
# sqpack/render/color.py. The two colours the page reserves and no square may ever take: the
# scarlet of the new-square mark and the one green that means "the best known arrangement".
SHADE_HUES, SHADE_STEPS = 20, 5
RESERVED_COLOURS = {"#a3123f", "#17794a"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(out: Path) -> None:
    # Nothing in the build is a BLAS call, and on a loaded host OpenBLAS's idle thread pool
    # roughly doubles the wall time; one thread costs nothing and changes no byte.
    subprocess.run(
        [str(PYTHON), str(HERE / "build_candidate.py"), "--out", str(out)],
        check=True,
        capture_output=True,
        env={**os.environ, "OPENBLAS_NUM_THREADS": "1"},
    )


def payload_of(html: str) -> dict:
    match = re.search(r'<script id="atlas-data" type="application/json">(.*?)</script>', html, re.S)
    assert match is not None, "index.html carries no atlas-data block"
    return json.loads(match.group(1).replace("<\\/", "</"))


def atlas_star_points() -> list[tuple[float, float]]:
    """SUMMARY_STAR_POINTS as the atlas source states it, parsed rather than imported."""
    text = ATLAS_SOURCE.read_text()
    block = re.search(r"SUMMARY_STAR_POINTS = \((.*?)\n\)", text, re.S).group(1)
    pairs = re.findall(r"\(Decimal\(\"?(-?[\d.]+)\"?\), Decimal\(\"?(-?[\d.]+)\"?\)\)", block)
    return [(float(x), float(y)) for x, y in pairs]


def open_items(entry: dict) -> list[str]:
    items = []
    if entry["optimality"]["status"] == "open":
        items.append("optimality")
    if entry["exactness"]["state"] not in ("closed-form", "minimal-polynomial"):
        items.append("exact value")
    if entry["rigidity"]["state"] == "not-established":
        items.append("rigidity")
    return items


def katex_approx_bounds() -> tuple[int, float, float]:
    """(advance, ink yMin, ink yMax) of U+2248 in KaTeX_Main, read independently of the build."""
    from fontTools.pens.boundsPen import BoundsPen  # noqa: PLC0415
    from fontTools.ttLib import TTFont  # noqa: PLC0415

    font = TTFont(KATEX_MAIN)
    glyph_set = font.getGlyphSet()
    name = font.getBestCmap()[ord("≈")]
    pen = BoundsPen(glyph_set)
    glyph_set[name].draw(pen)
    _x0, y0, _x1, y1 = pen.bounds
    return glyph_set[name].width, round(y0, 1), round(y1, 1)


def digit_bearing_px() -> float:
    """The median digit's left side bearing at the numeral's size, in the regular face, read
    from the woff2 hmtx tables independently of the build.

    The headline is one line now, so the numeral's box left is not a stamped constant: the page
    measures the `n =` line the numeral sits beside and puts the numeral `headline_gap_px` past
    it, less this bearing, so the gap is ink to ink rather than box to box. What is checked below
    is that relationship on the rendered page, which is a stronger claim than two computations of
    one formula agreeing with each other."""
    from fontTools.ttLib import TTFont  # noqa: PLC0415

    def bearing(path: Path, char: str) -> float:
        font = TTFont(path)
        return font["hmtx"][font.getBestCmap()[ord(char)]][1] / font["head"].unitsPerEm

    digits = sorted(bearing(FONTS / f"pt-serif-latin-{NUMERAL_WEIGHT}-normal.woff2", d) for d in "0123456789")
    return round((digits[4] + digits[5]) / 2 * NUMERAL_PX, 2)


def witness_centres(n: int) -> list[tuple[float, float]]:
    """Square centres of witness n, read independently of the build (corners averaged, or the
    centre-angle form's centres)."""
    import yaml  # noqa: PLC0415
    from fractions import Fraction  # noqa: PLC0415

    data = yaml.load((REPO / f"packing/witnesses/known-best/n-{n:03d}.yaml").read_text(), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))["witness"]
    centres = []
    for square in data["squares"]:
        if data["representation"] == "center-angle":
            centres.append((float(Fraction(square["center"][0])), float(Fraction(square["center"][1]))))
        else:
            xs = [float(Fraction(x)) for x, _ in square["corners"]]
            ys = [float(Fraction(y)) for _, y in square["corners"]]
            centres.append((sum(xs) / 4, sum(ys) / 4))
    return centres


def type_and_fit_sweep(browser, page_path: Path, check, expected_gap: float) -> tuple[list, int]:
    """Revision 4, over every pair of the page in one evaluate: the census of computed font
    sizes of every visible text-bearing HTML element on the stage (the badge glyphs are SVG
    marks and are left out), and at t = 0 and t = duration the visible layer's extent against
    the riding n, the bar and the panel's right edge, with each slot's top and height."""
    page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    page.goto(page_path.as_uri(), wait_until="load")
    page.evaluate("document.fonts.ready")
    result = page.evaluate(
        """(() => {
          const api = window.atlasTransitions;
          api.setCapture(true);
          const stage = document.getElementById('stage');
          const facts = document.getElementById('facts');
          const d = api.duration();
          const sizes = new Map();
          let svgGlyphs = 0;
          const census = () => {
            const walker = document.createTreeWalker(stage, NodeFilter.SHOW_TEXT);
            let node;
            while ((node = walker.nextNode())) {
              if (!node.textContent.trim()) continue;
              const el = node.parentElement;
              if (!(el instanceof HTMLElement)) { svgGlyphs++; continue; }
              const cs = getComputedStyle(el);
              if (cs.display === 'none' || cs.visibility === 'hidden' || el.getClientRects().length === 0) continue;
              const size = parseFloat(cs.fontSize);
              if (!sizes.has(size)) sizes.set(size, new Set());
              sizes.get(size).add(el.id || el.className || el.tagName.toLowerCase());
            }
          };
          const SLOTS = ['.numeral', '.head-proved', '.side', '.lower', '.star-line', '.exact', '.badges', '.head-open', '.open-items'];
          const fits = [];
          const count = api.pairs().length;
          for (let i = 0; i < count; i++) {
            api.select(i);
            for (const [t, layer, other] of [[0, 'facts-a', 'facts-b'], [d, 'facts-b', 'facts-a']]) {
              api.seek(t);
              census();
              const root = document.getElementById(layer);
              let bottom = 0, right = 0;
              const walker = document.createTreeWalker(facts, NodeFilter.SHOW_TEXT);
              let node;
              while ((node = walker.nextNode())) {
                if (!node.textContent.trim()) continue;
                const el = node.parentElement;
                if (el.closest('#' + other)) continue;
                const r = el.getBoundingClientRect();
                if (r.width === 0) continue;
                bottom = Math.max(bottom, r.bottom);
                right = Math.max(right, r.right);
              }
              root.querySelectorAll('svg').forEach((s) => {
                const r = s.getBoundingClientRect();
                bottom = Math.max(bottom, r.bottom);
                right = Math.max(right, r.right);
              });
              const slots = SLOTS.map((sel) => {
                const r = root.querySelector(sel).getBoundingClientRect();
                return [sel, Math.round(r.top * 100) / 100, Math.round(r.height * 100) / 100];
              });
              // The headline: the numeral against the `n =` line it shares a row with. Read
              // through `offset*` rather than `getBoundingClientRect`, because the numeral
              // carries the roll's transform and a client rect would measure that instead of
              // the layout. The line is constant and lives OUTSIDE both fading layers, so it
              // is found on the document rather than in `root`.
              const numeralEl = root.querySelector('.numeral');
              const nlineEl = document.querySelector('.nline');
              fits.push({ n: api.state().n + (t > 0 ? 1 : 0), t, bottom, right, slots,
                          numeralLeft: numeralEl.offsetLeft, numeralTop: numeralEl.offsetTop,
                          nlineRight: nlineEl.offsetLeft + nlineEl.offsetWidth,
                          nlineTop: nlineEl.offsetTop });
            }
          }
          // Revision 12 hides the position bar in Pack, where a corpus-wide scale says nothing
          // about one fixed n. A hidden element has a zero rect, so where it is not drawn the band
          // it *would* occupy is read off the stylesheet: the panel is held to the same line
          // whether the bar is drawn or not, which is what keeps a switch to Sweep from putting
          // the two on top of each other.
          const barEl = document.getElementById('progress');
          const pnEl = document.getElementById('p-n');
          const stageBox = document.getElementById('stage').getBoundingClientRect();
          const drawn = barEl.getBoundingClientRect().height > 0;
          const barTop = drawn ? barEl.getBoundingClientRect().top
                               : stageBox.top + parseFloat(getComputedStyle(barEl).top);
          const pnTop = drawn ? pnEl.getBoundingClientRect().top
                              : barTop + parseFloat(getComputedStyle(pnEl).top);
          const box = facts.getBoundingClientRect();
          return { sizes: Array.from(sizes, ([s, k]) => [s, Array.from(k).sort()]).sort((a, b) => a[0] - b[0]),
                   svgGlyphs, fits, pnTop, barTop, factsLeft: box.left, factsRight: box.right };
        })()"""
    )
    page.close()
    sizes = result["sizes"]
    check(len(sizes) <= 4, f"{page_path.name}: {len(sizes)} distinct stage font sizes: {sizes}")
    check([s for s, _ in sizes] == TYPE_SCALE, f"{page_path.name}: stage font sizes are {sizes}, expected {TYPE_SCALE}")
    check(all(s >= 28 for s, _ in sizes), f"{page_path.name}: stage text below 28 px: {[k for s, k in sizes if s < 28]}")
    check(max(s for s, _ in sizes) / min(s for s, _ in sizes) <= NUMERAL_RATIO_MAX, f"{page_path.name}: the numeral is more than {NUMERAL_RATIO_MAX} times the smallest size")
    numeral_sizes = [s for s, keys in sizes if "n-val" in keys]
    check(numeral_sizes == [NUMERAL_PX], f"{page_path.name}: the numeral is set at {numeral_sizes}")
    check(result["svgGlyphs"] > 0, f"{page_path.name}: no SVG badge glyphs seen, the census walked the wrong tree")
    fits = result["fits"]
    check(len(fits) >= 2, f"{page_path.name}: fit sweep saw {len(fits)} instants")
    low = [f for f in fits if not (f["bottom"] < result["pnTop"] and f["bottom"] < result["barTop"])]
    check(not low, f"{page_path.name}: panel text reaches the progress bar (riding n at {result['pnTop']}, bar at {result['barTop']}): {[(f['n'], f['bottom']) for f in low][:6]}")
    wide = [f for f in fits if f["right"] > result["factsRight"] + 1e-6]
    check(not wide, f"{page_path.name}: panel text runs past the panel's right edge {result['factsRight']}: {[(f['n'], f['right']) for f in wide][:6]}")
    slot_sets = {json.dumps(f["slots"]) for f in fits}
    check(len(slot_sets) == 1, f"{page_path.name}: slot positions differ between n: {sorted(slot_sets)[:3]}")
    off = [f for f in fits if abs(f["numeralLeft"] - f["nlineRight"] - expected_gap) > 0.55]
    check(
        not off,
        f"{page_path.name}: the numeral does not start {expected_gap} px after the `n =` line: "
        f"{[(f['n'], round(f['numeralLeft'] - f['nlineRight'], 2)) for f in off][:4]}",
    )
    rows = [f for f in fits if f["numeralTop"] != f["nlineTop"]]
    check(not rows, f"{page_path.name}: the numeral is not on the `n =` line's row: {[(f['n'], f['numeralTop'], f['nlineTop']) for f in rows][:4]}")
    return fits[0]["slots"] if fits else [], len(fits)


def platform_font_checks(browser, page_path: Path, index_of: dict[int, int], duration: float, check) -> None:
    """Which faces Chromium actually drew the panel's text with, through CDP.

    `CSS.getPlatformFontsForNode` names the font that rendered each glyph run, so this is
    proof of the glyph's source rather than an inference from widths. It runs on its own
    page without the console listener: enabling the CSS domain makes the inspector fetch
    the document's own `file:` URL for the inline stylesheet's source, which Chromium logs
    as an "Unsafe attempt to load URL" console error under its unique-origin rule for
    `file:` pages. The page itself never logs one (the main page's listener stays clean).
    """
    page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    errors: list[str] = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(page_path.as_uri(), wait_until="load")
    page.evaluate("document.fonts.ready")
    page.evaluate("window.atlasTransitions.setCapture(true)")
    cdp = page.context.new_cdp_session(page)
    cdp.send("DOM.enable")
    cdp.send("CSS.enable")

    def fonts_of(selector: str) -> list[str]:
        document = cdp.send("DOM.getDocument", {"depth": -1})
        node = cdp.send("DOM.querySelector", {"nodeId": document["root"]["nodeId"], "selector": selector})
        fonts = cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node["nodeId"]})["fonts"]
        return [f["familyName"] for f in fonts if f["glyphCount"] > 0]

    page.evaluate(f"window.atlasTransitions.select({index_of[103]})")
    check(fonts_of("#facts .nline .n-var") == ["PT Serif"] and fonts_of("#facts-a .n-val") == ["PT Serif"], "the headline is not set in PT Serif")
    check(fonts_of("#facts-a .side .rel") == ["KaTeX_Main"], f"≤ is set in {fonts_of('#facts-a .side .rel')}")
    check(fonts_of("#facts-a .lower .rel") == ["KaTeX_Main"], f"≥ is set in {fonts_of('#facts-a .lower .rel')}")
    check(fonts_of("#facts-a .lower .val") == ["PT Serif"] and fonts_of("#facts-a .side .val") == ["PT Serif"], "the bound values are not set in PT Serif")
    page.evaluate(f"window.atlasTransitions.select({index_of[147]})")
    page.evaluate(f"window.atlasTransitions.seek({duration})")
    form = page.evaluate("document.querySelector('#facts-b .exact .form').textContent")
    check("√" in form and "KaTeX_Main" in fonts_of("#facts-b .exact .form"), f"the radical in n=148's closed form {form!r} is not set in KaTeX_Main")
    check(all("Georgia" not in f for f in fonts_of("#facts-b .exact .form") + fonts_of("#facts-b .side")), "a panel glyph falls back to Georgia")
    check(not errors, f"page errors on the font-check page: {errors}")
    page.close()


def colour_sweep(browser, page_path: Path, check) -> tuple[int, int]:
    """Every fill the page draws over every pair, at rest, at the arrival instant and mid block
    motion, in one evaluate; returns (distinct fills, hue families reached).

    Revision 11 replaced the teal-to-citron sweep with one map that is always on: the hue is the
    palette slot of the square's angle and the shade is its full-side contact count, so every fill
    on the stage must be an entry of the page's own 20 x 5 shade table — which is checked here
    against the generator that produced it, `square_fill_palette` in sqpack/render/color.py.

    Revision 12 made that map an *option* and the square's own identity the default, so the sweep
    selects `angle-stable` before it starts: what is under test here is still the angle map, and
    the identity greens are a different scheme with their own checks in `check_workbench.py`.

    The arriving square is left out: its fill leans toward scarlet on purpose (it is identity
    n + 1 of the pair), and so are the hidden pool elements of later identities. Revision 6's
    desaturation is turned off for the sweep — it drains a fill's chroma while the pair moves, and
    with it left on the same sweep puts 66 further colours on the stage that are nobody's palette
    entry. The drain is a separate feature with its own checks; what is under test here is the map.
    """
    page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    page.goto(page_path.as_uri(), wait_until="load")
    page.evaluate("document.fonts.ready")
    swept = page.evaluate(
        """(() => {
          const api = window.atlasTransitions;
          api.setCapture(true);
          api.setDesaturate(false);
          // Revision 12: the angle map is one of three schemes now, and not the default.
          if (api.setColorScheme) api.setColorScheme('angle-stable');
          const seen = new Set();
          const collect = () => {
            const n = api.state().n;
            document.querySelectorAll('#squares g[data-identity]').forEach((g) => {
              if (Number(g.dataset.identity) <= n) seen.add(g.firstElementChild.getAttribute('fill'));
            });
          };
          const count = api.pairs().length;
          for (let i = 0; i < count; i++) {
            api.select(i);
            const sc = api.schedule();
            for (const t of [0, sc.arrived, (sc.blocksStart + sc.blocksEnd) / 2, 2.8]) { api.seek(t); collect(); }
          }
          const colour = api.colour();
          const token = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
          return {
            fills: Array.from(seen), shades: colour.shades, palette: colour.palette,
            reserved: [token('--new'), token('--met')],
          };
        })()"""
    )
    page.close()
    fills, shades, palette = swept["fills"], swept["shades"], swept["palette"]

    # 1. The table the page carries is the atlas's own, not a hand-typed copy that has drifted.
    try:
        from sqpack.render.color import square_fill_palette  # noqa: PLC0415

        generated = [list(family) for family in square_fill_palette(hue_count=SHADE_HUES, shades_per_hue=SHADE_STEPS)]
        check(shades == generated, f"the page's shade table is not square_fill_palette({SHADE_HUES}, {SHADE_STEPS})")
    except ImportError:  # pragma: no cover - the project venv has sqpack importable
        # Without sqpack the generator is out of reach, so only the table's shape can be checked,
        # against the hue palette the page reports beside it: one family of five a palette slot.
        check(
            len(palette) == SHADE_HUES and [len(f) for f in shades] == [SHADE_STEPS] * SHADE_HUES,
            f"the page carries {len(palette)} hues and shade families {[len(f) for f in shades]}",
        )
        print("  (sqpack is not importable: the shade table was checked for shape against the page's palette only)")

    # 2. Every fill drawn is in the table, and the sweep sees a good spread of it. Measured:
    # index-all.html's 323 pairs at four instants each draw 66 of the table's 100 shades and reach
    # all 20 hue families; the 25-pair index.html draws 56 and reaches all 20. The floor is pinned
    # under the smaller of the two. Not all 100 are reachable — three and four full-side contacts
    # are rare away from the pinned tilts, so most families are only seen at their light end.
    table = {shade for family in shades for shade in family}
    stray = sorted(fill for fill in fills if fill not in table)
    check(not stray, f"fills drawn that are in no shade family: {stray[:8]}")
    families = sum(1 for family in shades if any(fill in family for fill in fills))
    check(len(fills) >= 50, f"the colour sweep saw only {len(fills)} distinct fills")
    check(families == len(shades), f"the sweep reached {families} of {len(shades)} hue families")

    # 3. The two colours the page reserves are never a square's fill.
    reserved = {colour.lower() for colour in swept["reserved"]}
    check(reserved == RESERVED_COLOURS, f"the page's reserved colours are {sorted(reserved)}, expected {sorted(RESERVED_COLOURS)}")
    taken = sorted(fill for fill in fills if fill.lower() in RESERVED_COLOURS)
    check(not taken, f"a square is filled with a reserved colour (the scarlet mark or the met green): {taken}")
    return len(fills), families


def staging_checks(page, api: str, index_of: dict[int, int], duration: float, check) -> None:
    """Revision 5 in the headless shell: the identity pool, the five motion modes, the two
    staged orders, and a block's rigidity half way through its motion."""
    poses = "Array.from(document.querySelectorAll('#squares g[data-identity]')).filter(g => Number(g.dataset.identity) <= " + api + ".state().n).map(g => [g.dataset.identity, g.getAttribute('transform')])"
    visible = "Array.from(document.querySelectorAll('#squares g[data-identity]')).filter(g => g.style.display !== 'none').length"
    total = "document.querySelectorAll('#squares g[data-identity]').length"

    # The pool: one element per identity, created once, never re-keyed, hidden beyond n + 1.
    shown = ("Array.from(document.querySelectorAll('#squares g[data-identity]'))"
             ".filter(g => g.style.display !== 'none').map(g => Number(g.dataset.identity)).sort((a, b) => a - b)")
    page.evaluate(f"{api}.select({index_of[4]})")
    check(page.evaluate(shown) == [1, 2, 3, 4, 5], "pair 4->5 does not show exactly identities 1..5")
    check(page.evaluate(total) >= 5, "pair 4->5 has no pool at all")
    page.evaluate("document.querySelector('#squares g[data-identity=\"5\"]').dataset.probe = 'born-at-5'")
    page.evaluate(f"{api}.select({index_of[100]})")
    check(page.evaluate(total) == 101 and page.evaluate(visible) == 101, "pair 100->101 does not show exactly identities 1..101")
    check(page.evaluate("document.querySelector('#squares g[data-identity=\"5\"]').dataset.probe") == "born-at-5", "identity 5's element was re-created between pairs")
    ids = page.evaluate("Array.from(document.querySelectorAll('#squares g[data-identity]')).map(g => Number(g.dataset.identity))")
    check(ids == list(range(1, 102)), "pool elements are not in birth order")
    page.evaluate(f"{api}.select({index_of[323]})")
    check(page.evaluate(total) == 324, "pair 323->324 does not create identities up to 324")
    page.evaluate(f"{api}.select({index_of[4]})")
    check(page.evaluate(total) == 324 and page.evaluate(visible) == 5, "returning to 4->5 does not hide identities beyond 5")
    check(page.evaluate("document.querySelector('#squares g[data-identity=\"5\"]').dataset.probe") == "born-at-5", "identity 5's element was re-created on return")
    ident = page.evaluate(f"{api}.identities()")
    check(sorted(ident["from"]) == [1, 2, 3, 4] and sorted(ident["to"]) == [1, 2, 3, 4, 5], f"identities of 4->5 are {ident}")
    new = page.evaluate(f"{api}.newSquare()")
    check(new["identity"] == 5 and ident["to"][new["index"]] == 5, f"the new square of 4->5 is {new}")

    # The five motion modes, add-then-move the default.
    check(page.evaluate(f"{api}.phases()") == PHASES, "the motion modes are not the five expected")
    check(page.evaluate(f"{api}.state().phase") == "add-then-move", "the default motion mode is not add-then-move")
    for phase in PHASES:
        page.evaluate(f"{api}.setPhase('{phase}')")
        check(page.evaluate(f"{api}.state().phase") == phase, f"motion mode {phase} is not reachable")
    check(page.evaluate("Array.from(document.querySelectorAll('#phase-seg button')).map(b => b.dataset.phase)") == PHASES, "the motion buttons do not offer the five modes")

    # add-then-move at 100->101: the new square fully in and the container grown before anything moves.
    page.evaluate(f"{api}.select({index_of[100]})")
    page.evaluate(f"{api}.setPhase('add-then-move')")
    sc = page.evaluate(f"{api}.schedule()")
    check(abs(sc["arrive"] - TIMING["dwell"]) < 1e-9 and abs(sc["arrived"] - (TIMING["dwell"] + ARRIVAL_FRACTION * TIMING["move"])) < 1e-9, f"add-then-move arrival instants are {sc}")
    check(abs(sc["blocksStart"] - sc["arrived"]) < 1e-9 and abs(sc["blocksEnd"] - (TIMING["dwell"] + TIMING["move"])) < 1e-9, f"add-then-move block instants are {sc}")
    page.evaluate(f"{api}.seek(0)")
    rest = page.evaluate(poses)
    page.evaluate(f"{api}.seek({sc['arrived']})")
    at_arrival = page.evaluate(poses)
    check(at_arrival == rest, "add-then-move: an existing square has moved by the arrival instant")
    new_state = "[Number(document.querySelector('#squares g[data-identity=\"101\"]').getAttribute('opacity')), document.getElementById('mark').getAttribute('opacity'), document.getElementById('mark').firstElementChild.getAttribute('stroke-width'), parseFloat(document.getElementById('container').getAttribute('width'))]"
    opacity, mark_opacity, mark_width, side = page.evaluate(new_state)
    check(opacity == 1.0 and float(mark_opacity) == 1.0 and float(mark_width) == 4.0, f"add-then-move: at arrival the new square is {opacity}, mark {mark_opacity} at {mark_width}px")
    side_to = page.evaluate("JSON.parse(document.getElementById('atlas-data').textContent).frames['101'].side")
    check(abs(side - side_to) < 1e-6, f"add-then-move: at arrival the container is {side}, not {side_to}")
    mid = (sc["blocksStart"] + sc["blocksEnd"]) / 2
    page.evaluate(f"{api}.seek({mid})")
    at_mid = page.evaluate(poses)
    check(sum(1 for a, b in zip(at_mid, rest, strict=True) if a != b) > 50, "add-then-move: the squares are not moving mid block motion")
    page.evaluate(f"{api}.seek({duration})")
    end = page.evaluate(poses)

    # A block turns as one body: its rigid members keep their mutual distances at mid motion,
    # up to twice the residual the record states for the block.
    blocks = page.evaluate(f"{api}.blocks()")
    check(len(blocks) >= 2, f"100->101 carries {len(blocks)} blocks")
    ident_from = page.evaluate(f"{api}.identities().from")
    ident_to = page.evaluate(f"{api}.identities().to")
    stats_blocks = json.loads((HERE / "transition-stats.json").read_text())["pairs"][99]["blocks"]
    # The turning block (the diamond, 45 degrees), not the largest: the strips are bigger but only slide.
    biggest = max(range(len(blocks)), key=lambda k: (abs(blocks[k]["turn"]), len(blocks[k]["members"])))
    members = blocks[biggest]["members"]
    residual = stats_blocks[biggest]["residual_max"]
    page.evaluate(f"{api}.seek({mid})")
    centre = "(() => { const g = document.querySelector('#squares g[data-identity=\"' + arguments[0] + '\"]'); const m = /translate\\(([-\\d.e]+) ([-\\d.e]+)\\)/.exec(g.getAttribute('transform')); return [parseFloat(m[1]), parseFloat(m[2])]; })"
    mid_centres = page.evaluate("(ids) => ids.map(id => { const g = document.querySelector('#squares g[data-identity=\"' + id + '\"]'); const m = /translate\\(([-\\d.e]+) ([-\\d.e]+)\\)/.exec(g.getAttribute('transform')); return [parseFloat(m[1]), parseFloat(m[2])]; })", [ident_from[i] for i in members])
    page.evaluate(f"{api}.seek(0)")
    rest_centres = page.evaluate("(ids) => ids.map(id => { const g = document.querySelector('#squares g[data-identity=\"' + id + '\"]'); const m = /translate\\(([-\\d.e]+) ([-\\d.e]+)\\)/.exec(g.getAttribute('transform')); return [parseFloat(m[1]), parseFloat(m[2])]; })", [ident_from[i] for i in members])
    worst = 0.0
    for a in range(len(members)):
        for b in range(a + 1, len(members)):
            d0 = math.dist(rest_centres[a], rest_centres[b])
            d1 = math.dist(mid_centres[a], mid_centres[b])
            worst = max(worst, abs(d1 - d0))
    check(worst <= 2 * residual + 1e-6, f"100->101: the largest block's members drift apart by {worst:.4f} mid motion (residual {residual})")
    check(abs(blocks[biggest]["turn"]) > 40 and len(members) >= 12, f"100->101's turning block turns {blocks[biggest]['turn']} degrees with {len(members)} members, expected about 45 with a dozen or more")
    moved = [i for i in members if any(abs(x - y) > 1e-6 for x, y in zip(rest_centres[members.index(i)], mid_centres[members.index(i)], strict=True))]
    check(len(moved) == len(members), "100->101: a member of the turning block is not moving mid motion")

    # move-then-add: the blocks at their final poses before the new square appears.
    page.evaluate(f"{api}.setPhase('move-then-add')")
    sc = page.evaluate(f"{api}.schedule()")
    check(abs(sc["blocksEnd"] - sc["arrive"]) < 1e-9 and abs(sc["arrived"] - (TIMING["dwell"] + TIMING["move"])) < 1e-9, f"move-then-add instants are {sc}")
    page.evaluate(f"{api}.seek({sc['blocksEnd']})")
    check(page.evaluate(poses) == end, "move-then-add: the squares are not at their final poses when the blocks end")
    opacity, mark_opacity, _, _ = page.evaluate(new_state)
    check(opacity == 0.0 and float(mark_opacity) == 0.0, f"move-then-add: the new square shows before the blocks end (opacity {opacity}, mark {mark_opacity})")
    page.evaluate(f"{api}.seek({sc['arrived']})")
    opacity, mark_opacity, _, _ = page.evaluate(new_state)
    check(opacity == 1.0 and float(mark_opacity) == 1.0, "move-then-add: the new square is not in at the move's end")
    page.evaluate(f"{api}.setPhase('add-then-move')")
    # The arrival-instant overlap census is on the record for this pair.
    stats_pair = json.loads((HERE / "transition-stats.json").read_text())["pairs"][99]
    check(stats_pair["arrival_overlaps"] == len(stats_pair["arrival_overlap_ids"]) and stats_pair["arrival_overlaps"] > 0, "100->101's arrival overlap census is missing or empty")


def style_checks(page, api: str, index_of: dict, check) -> None:
    """Styles B and C, a smoke check: the styles cycle, each physical style renders 100->101 mid-move
    with finite poses and its trajectory ends exactly on the n + 1 poses, and the tween is left showing."""
    check(page.evaluate(f"{api}.styles()") == ["tween", "physics", "bodies"], "the styles are not tween, physics, bodies")
    index = index_of[100]
    page.evaluate(f"{api}.select({index})")
    for style, letter in (("physics", "B"), ("bodies", "C")):
        page.evaluate(f"{api}.setStyle('{style}')")
        check(page.evaluate(f"{api}.state().style") == style, f"setStyle('{style}') did not take")
        check(page.evaluate("document.getElementById('style-select').value") == style,
              f"the style select does not follow setStyle('{style}') (style {letter})")
        page.evaluate(f"{api}.seek(1.7)")
        bad = page.evaluate(
            "Array.from(document.querySelectorAll('#squares g')).filter(g => g.style.display !== 'none')"
            ".map(g => g.getAttribute('transform') || '').filter(t => /NaN|Infinity/.test(t)).length"
        )
        check(bad == 0, f"{style}: {bad} non-finite transforms at 100->101 mid-move")
        result = page.evaluate(
            f"""(() => {{
              const data = JSON.parse(document.getElementById('atlas-data').textContent);
              const info = {api}.physics({index}, '{style}');
              const pair = data.pairs[{index}];
              const target = data.frames[String(pair.n + 1)].squares;
              let maxPos = 0, maxAng = 0;
              info.final.forEach((f, i) => {{
                const t = i < pair.n ? target[pair.map[i]] : target[pair.new];
                maxPos = Math.max(maxPos, Math.hypot(f[0] - t[0], f[1] - t[1]));
                const d = ((f[2] - t[2]) % 90 + 90) % 90;
                maxAng = Math.max(maxAng, Math.min(d, 90 - d));
              }});
              return {{ maxPos, maxAng, bodies: info.bodies, squares: pair.n + 1 }};
            }})()"""
        )
        check(result["maxPos"] < 1e-6 and result["maxAng"] < 1e-6, f"{style}: 100->101 ends {result['maxPos']:.2e} units / {result['maxAng']:.2e} degrees off the n+1 poses")
        if style == "bodies":
            check(0 < result["bodies"] < result["squares"], f"bodies: 100->101 has {result['bodies']} bodies for {result['squares']} squares; the blocks are not rigid bodies")
        else:
            check(result["bodies"] == result["squares"], f"physics: 100->101 has {result['bodies']} bodies for {result['squares']} squares")
    page.evaluate(f"{api}.setStyle('tween')")
    check(page.evaluate(f"{api}.state().style") == "tween", "the tween is not showing after the style checks")


def browser_checks(page_path: Path, check) -> None:
    """DOM-level checks in the pinned headless shell, driven through the virtual clock."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get("SQPACK_CHROMIUM"))
        try:
            errors: list[str] = []
            page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
            page.goto(page_path.as_uri(), wait_until="load")
            page.evaluate("document.fonts.ready")
            api = "window.atlasTransitions"
            page.evaluate(f"{api}.setCapture(true)")
            rect = lambda selector: page.evaluate(f"(() => {{ const b = document.querySelector('{selector}').getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; }})()")
            text_of = lambda selector: page.evaluate(f"document.querySelector('{selector}').textContent")
            index_of = {n: i for i, n in enumerate(page.evaluate(f"{api}.pairs().map(p => p.n)"))}
            duration = page.evaluate(f"{api}.duration()")
            check(abs(duration - sum(TIMING.values())) < 1e-9, f"page duration is {duration}, not {sum(TIMING.values())}")

            # Revision 5: the identity pool, the motion modes and the staged orders.
            staging_checks(page, api, index_of, duration, check)
            check(not errors, f"browser errors during the staging checks: {errors}")
            # Styles B and C: the smoke check.
            style_checks(page, api, index_of, check)
            check(not errors, f"browser errors during the style checks: {errors}")

            # The progress bar is a pure function of the pair and the clock, on the 1..324 range.
            # Revision 9 makes the bar span the chosen range, so the corpus range is what makes that
            # the 1..324 bar; the page itself opens on a one-step range.
            page.evaluate(f"{api}.setRange({api}.range().min, {api}.range().max)")
            page.evaluate(f"{api}.select({index_of[100]})")
            for t, expected in ((0.0, 99 / 323), (duration, 100 / 323), (1.4, (99 + 0.5) / 323)):
                page.evaluate(f"{api}.seek({t})")
                position = page.evaluate(f"{api}.progress().position")
                width = page.evaluate("parseFloat(document.getElementById('p-fill').style.width)")
                check(abs(position - expected) < 1e-9, f"progress at t={t} is {position}, expected {expected}")
                # The style serialises to a thousandth of a pixel.
                check(abs(width - expected * 1720) < 1e-3, f"fill width at t={t} is {width}px, expected {expected * 1720}")
            page.evaluate(f"{api}.seek(0.5)")
            check(page.evaluate("document.getElementById('p-n').textContent") == "100", "progress label at the dwell is not 100")
            page.evaluate(f"{api}.seek({duration})")
            check(page.evaluate("document.getElementById('p-n').textContent") == "101", "progress label at the settle is not 101")

            # Seeking is idempotent: the same instant renders the same stage.
            page.evaluate(f"{api}.seek(2.3)")
            first = page.evaluate("document.getElementById('stage').innerHTML")
            page.evaluate(f"{api}.seek(0.2)")
            page.evaluate(f"{api}.seek(2.3)")
            check(first == page.evaluate("document.getElementById('stage').innerHTML"), "seek is not idempotent")

            # The panel's text never cross-dissolves over itself: at no instant are both layers visible.
            # Checked in the default staging and in the unstaged mode, whose roll starts later.
            for phase in ("add-then-move", "simultaneous"):
                page.evaluate(f"{api}.setPhase('{phase}')")
                schedule = page.evaluate(f"{api}.schedule()")
                samples = 60
                for k in range(samples + 1):
                    t = schedule["arrive"] - 0.05 + (schedule["roll"] + 0.1) * k / samples
                    page.evaluate(f"{api}.seek({t})")
                    a, b = page.evaluate(
                        "[parseFloat(document.getElementById('facts-a').style.opacity), parseFloat(document.getElementById('facts-b').style.opacity)]"
                    )
                    check(min(a, b) == 0.0, f"{phase}: both facts layers visible at t={t:.3f}: {a:.3f} and {b:.3f}")
                page.evaluate(f"{api}.seek({schedule['arrive'] - 0.01})")
                check(page.evaluate("document.querySelector('#facts-a .n-val').textContent") == "100", "layer A does not read 100")
                check(page.evaluate("document.querySelector('#facts-b .n-val').textContent") == "101", "layer B does not read 101")

            # The scarlet mark in the unstaged mode: absent mid-move, on the arriving square at the settle,
            # retained through the next pair's dwell, gone once the next move is under way. Scarlet comes
            # from the stylesheet.
            page.evaluate(f"{api}.setPhase('simultaneous')")
            scarlet = page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--new').trim()")
            check(scarlet == "#a3123f", f"--new is {scarlet!r}")
            mark_state = "[document.getElementById('mark').getAttribute('opacity'), document.getElementById('mark').firstElementChild.getAttribute('stroke-width'), getComputedStyle(document.getElementById('mark').firstElementChild).stroke]"
            page.evaluate(f"{api}.seek(1.7)")
            opacity, _, _ = page.evaluate(mark_state)
            check(float(opacity) == 0.0, f"mark visible mid-move (opacity {opacity})")
            page.evaluate(f"{api}.seek({duration})")
            opacity, width, stroke = page.evaluate(mark_state)
            check(float(opacity) == 1.0 and float(width) == 2.0, f"mark at the settle: opacity {opacity}, width {width}")
            check(stroke == "rgb(163, 18, 63)", f"mark stroke is {stroke}")
            check(float(page.evaluate("document.querySelector('#squares g[data-identity=\"101\"]').getAttribute('opacity')")) == 1.0, "new square not fully in at the settle")
            page.evaluate(f"{api}.select({index_of[101]})")
            page.evaluate(f"{api}.seek(0.5)")
            opacity, width, _ = page.evaluate(mark_state)
            check(float(opacity) == 1.0 and float(width) == 2.0, f"mark not retained through the next dwell: opacity {opacity}, width {width}")
            page.evaluate(f"{api}.seek({TIMING['dwell'] + 0.15 * TIMING['move'] + 0.01})")
            opacity, _, _ = page.evaluate(mark_state)
            check(float(opacity) == 0.0, f"mark still visible once the next move is under way (opacity {opacity})")
            page.evaluate(f"{api}.setPhase('add-then-move')")

            # The badges are the poster's marks, and the star is drawn, not typeset.
            page.evaluate(f"{api}.select({index_of[17]})")
            page.evaluate(f"{api}.seek(0.0)")
            labels = page.evaluate("Array.from(document.querySelectorAll('#facts-a .badge-item .label')).map(e => e.textContent)")
            check(labels == ["new lower bound", "exact"], f"badge labels for n=17 are {labels}")
            check(page.evaluate("document.querySelectorAll('#facts-a .badge-star polygon').length") == 1, "n=17 has no star polygon")
            check(page.evaluate("document.querySelector('#facts-a .exact .note').textContent") == "algebraic · degree 18", "n=17 degree note")
            opens = page.evaluate("Array.from(document.querySelectorAll('#facts-a .open-item .label')).map(e => e.textContent)")
            check(opens == ["optimality", "rigidity"], f"open items for n=17 are {opens}")
            page.evaluate(f"{api}.select({index_of[103]})")
            check(page.evaluate("document.getElementById('progress').getBoundingClientRect().bottom") <= 1080, "progress bar is not inside the stage")

            # Revision 3, the headline: `n =` is one static line above the numeral, italic n and upright
            # equals in PT Serif, muted, sharing the numeral's left edge (the numeral's box starts a
            # few px earlier to absorb a digit's side bearing). Revision 4: the numeral is 96 px, PT
            # Serif Regular, and the n-line 34 px.
            check(text_of("#facts .nline") == "n=", f"the n-line reads {text_of('#facts .nline')!r}")
            n_line, numeral = rect("#facts .nline"), rect("#facts-a .numeral")
            check(n_line[1] + n_line[3] <= numeral[1], f"the n-line (bottom {n_line[1] + n_line[3]}) is not above the numeral (top {numeral[1]})")
            check(0 <= n_line[0] - numeral[0] <= 8, f"the n-line's left ({n_line[0]}) does not share the numeral's ({numeral[0]})")
            check(page.evaluate("document.querySelectorAll('#facts-a .numeral .n-var, #facts-a .numeral .n-eq').length") == 0, "the numeral still carries n and =")
            styles = page.evaluate(
                "[getComputedStyle(document.querySelector('#facts .nline .n-var')).fontStyle, getComputedStyle(document.querySelector('#facts .nline .n-eq')).fontStyle, getComputedStyle(document.querySelector('#facts .nline')).color, getComputedStyle(document.querySelector('#facts-a .n-val')).fontSize, getComputedStyle(document.querySelector('#facts-a .n-val')).fontWeight, getComputedStyle(document.querySelector('#facts .nline')).fontSize]"
            )
            check(styles == ["italic", "normal", "rgb(92, 102, 115)", f"{NUMERAL_PX}px", str(NUMERAL_WEIGHT), f"{N_LINE_PX}px"], f"headline styles are {styles}")
            check(page.evaluate("getComputedStyle(document.getElementById('kind-tag')).display") == "none", "the review kind tag is shown in capture preview")

            # The lower bound: `s(n) ≥ value` for an open n with its note on the line directly below,
            # left-aligned and never to its right; both slots empty, at the same fixed heights, for a proved n.
            check(text_of("#facts-a .lower") == "s(103)≥10.165151", f"n=103 lower line reads {text_of('#facts-a .lower')!r}")
            check(text_of("#facts-a .lower-note .note") == "proved lower bound", "n=103 lacks the proved-lower-bound note")
            lower, note = rect("#facts-a .lower"), rect("#facts-a .lower-note")
            check(note[1] >= lower[1] + lower[3] - 0.5 and abs(note[0] - lower[0]) < 0.5, f"the note is not directly below the lower line: {lower} vs {note}")
            slot = lambda selector: tuple(rect(selector)[i] for i in (0, 1, 3))   # left, top, height: the row's width follows its content
            badges_open, open_group_open = slot("#facts-a .badges"), slot("#facts-a .open")
            page.evaluate(f"{api}.select({index_of[100]})")
            check(text_of("#facts-a .lower") == "" and text_of("#facts-a .lower-note") == "", "n=100 (proved) shows a lower-bound line")
            proved_lower, proved_note = rect("#facts-a .lower"), rect("#facts-a .lower-note")
            check((proved_lower[1], proved_lower[3]) == (lower[1], lower[3]) and (proved_note[1], proved_note[3]) == (note[1], note[3]), "the empty lower-bound slots are not at the fixed heights")
            check((slot("#facts-a .badges"), slot("#facts-a .open")) == (badges_open, open_group_open), "the badge row or the open group moves between an open and a proved n")
            page.evaluate(f"{api}.select({index_of[17]})")
            check(text_of("#facts-a .lower") == "s(17)≥4.59", f"n=17 lower line reads {text_of('#facts-a .lower')!r}")
            check(page.evaluate("getComputedStyle(document.querySelector('#facts-a .lower .val')).color") == "rgb(23, 32, 42)", "n=17: the first-proved-here digits are coloured")
            page.evaluate(f"{api}.select({index_of[147]})")
            page.evaluate(f"{api}.seek({duration})")
            check("√" in text_of("#facts-b .exact .form"), "n=148's closed form carries no radical")

            # The symbols face is loaded with the relation range and the size adjustment.
            faces = page.evaluate("Array.from(document.fonts).map(f => [f.family.replace(/\"/g, ''), f.status, f.unicodeRange, f.sizeAdjust])")
            symbols = [f for f in faces if f[0] == "Atlas Symbols"]
            check(len(symbols) == 1 and symbols[0][1] == "loaded" and symbols[0][3] == "102.5%", f"Atlas Symbols face: {symbols}")
            check(symbols and symbols[0][2].replace("U+", "").replace(" ", "") == SYMBOL_RANGE.replace("U+", "").replace(" ", ""), f"Atlas Symbols range is {symbols and symbols[0][2]}")
            check(len(faces) == 5, f"{len(faces)} faces loaded, expected 5")

            # The approximately-equal badge is one path, KaTeX_Main's outline, placed on its own ink.
            page.evaluate(f"{api}.select({index_of[103]})")
            approx = page.evaluate("Array.from(document.querySelectorAll('#facts-a .badge-muted .glyph-path')).map(p => [p.getAttribute('d'), p.getAttribute('transform'), p.getAttribute('stroke-width')])")
            check(len(approx) == 1, f"n=103 draws {len(approx)} approximately-equal paths, expected one")
            if approx:
                metrics = page.evaluate("JSON.parse(document.getElementById('atlas-data').textContent).metrics.approx")
                k = metrics["font_size"] / 1000
                expected = f"translate({(9.5 - metrics['advance'] * k / 2):.3f} {(9.5 + (metrics['y0'] + metrics['y1']) / 2 * k):.3f}) scale({k:.4f} -{k:.4f})"
                check(approx[0] == [metrics["d"], expected, str(metrics["stroke_units"])], f"approximately-equal path is {approx[0][1:]} not {expected}")
            check(not errors, f"browser errors: {errors}")

            # Which faces drew the glyphs, on a page of its own (see platform_font_checks).
            platform_font_checks(browser, page_path, index_of, duration, check)

            # Revision 4: the type scale and the panel's fit, over every embedded pair of index.html
            # and, when it is present, of index-all.html (every n from 1 to 324).
            expected_gap = HEADLINE_GAP_PX - digit_bearing_px()
            slots, instants = type_and_fit_sweep(browser, page_path, check, expected_gap)
            print(f"type and fit sweep over {page_path.name}: {instants} instants; slots (top, height): " + ", ".join(f"{s[0]} {s[1]:g}/{s[2]:g}" for s in slots))
            if (HERE / "index-all.html").exists():
                _, instants_all = type_and_fit_sweep(browser, HERE / "index-all.html", check, expected_gap)
                print(f"type and fit sweep over index-all.html: {instants_all} instants")

            # Revision 11's colouring over the whole corpus, from the all-pairs page when it is present.
            sweep_page = HERE / "index-all.html" if (HERE / "index-all.html").exists() else page_path
            distinct, families = colour_sweep(browser, sweep_page, check)
            print(f"colour sweep over {sweep_page.name}: {distinct} distinct fills, every one in the {SHADE_HUES}x{SHADE_STEPS} shade table, {families} hue families reached")
        finally:
            browser.close()


def record_checks(stats: dict, check) -> None:
    """Revision 5's record: the identity chain, the block statistics, the new-square rule and
    the arrival overlap census, on every pair."""
    pairs = stats["pairs"]
    by_n = {pair["n"]: pair for pair in pairs}
    identities = {int(k): v for k, v in stats["identities"].items()}
    check(sorted(identities) == list(range(1, 325)), "the record does not carry identities for every n from 1 to 324")
    # Compose the maps independently and compare; then the presence rule.
    composed = {1: [1]}
    for n in range(1, 324):
        pair = by_n[n]
        nxt = [0] * (n + 1)
        for i, j in enumerate(pair["map"]):
            nxt[j] = composed[n][i]
        nxt[pair["new_index"]] = n + 1
        composed[n + 1] = nxt
    check(all(composed[n] == identities[n] for n in range(1, 325)), "the record's identity chain is not the composition of its maps")
    for n in range(1, 325):
        check(sorted(identities[n]) == list(range(1, n + 1)), f"frame {n} does not carry identities 1..{n} exactly once")
    for k in (1, 5, 17, 101, 148, 261, 324):
        present = [n for n in range(1, 325) if identities[n].count(k) == 1]
        check(present == list(range(k, 325)), f"identity {k} is not in every frame from {k} to 324 exactly once")
    check(all(identities[n].count(k) == 0 for n in range(1, 325) for k in (n + 1,)), "an identity appears before it is born")

    for pair in pairs:
        n = pair["n"]
        for key in ("block_count", "in_block", "rigid_members", "riders", "individual", "moving", "moving_in_block", "moving_individually",
                    "stationary", "block_residual_mean", "block_residual_max", "rider_drift_max", "blocks", "block_of",
                    "new_rule", "new_tied", "new_index_hungarian", "new_choice_differs", "arrival_overlaps", "arrival_overlap_ids",
                    "clusters_from", "clusters_to", "links_found", "alone_hops"):
            check(key in pair, f"pair {n}: no {key} in the record")
        check(pair["new_rule"] in NEW_RULES, f"pair {n}: new-square rule {pair['new_rule']!r} is not in the vocabulary")
        check(pair["new_tied"] >= 1, f"pair {n}: tie set of {pair['new_tied']}")
        check(pair["new_choice_differs"] == (pair["new_index"] != pair["new_index_hungarian"]), f"pair {n}: new_choice_differs disagrees")
        check(len(pair["block_of"]) == n and all(-1 <= k < pair["block_count"] for k in pair["block_of"]), f"pair {n}: block_of is malformed")
        check(pair["block_count"] == len(pair["blocks"]), f"pair {n}: block_count disagrees with the blocks")
        check(pair["moving"] == pair["moving_in_block"] + pair["moving_individually"], f"pair {n}: moving counts do not add up")
        check(pair["in_block"] == pair["rigid_members"] + pair["riders"] == sum(1 for k in pair["block_of"] if k >= 0), f"pair {n}: block membership counts disagree")
        check(pair["moving"] + pair["stationary"] == n, f"pair {n}: moving plus stationary is not n")
        check(pair["arrival_overlaps"] == len(pair["arrival_overlap_ids"]), f"pair {n}: overlap census disagrees with its ids")
        for k, block in enumerate(pair["blocks"]):
            check(len(block["members"]) >= 2, f"pair {n}: block {k} has {len(block['members'])} members")
            check(all(pair["block_of"][i] == k for i in block["members"] + block["riders"]), f"pair {n}: block {k}'s members are not tagged with it")
            # The turn is a Procrustes fit, so it can overshoot the clusters' tilt difference by a
            # few degrees (10->11 has a block at -47); the pivot travels at most 1.5 and every rigid
            # member lands within 0.35 of its target under the block's transform, by construction.
            check(len(block["from"]) == 2 and len(block["to"]) == 2 and abs(block["turn"]) <= 60, f"pair {n}: block {k}'s transform is malformed")
            check(math.dist(block["from"], block["to"]) <= 1.5 + 1e-6, f"pair {n}: block {k}'s pivot travels {math.dist(block['from'], block['to'])}")
            check(block["residual_max"] <= 0.35 + 1e-9, f"pair {n}: block {k}'s rigid residual is {block['residual_max']}")
            check(block["drift_max"] <= 0.75 + 1e-9, f"pair {n}: block {k}'s rider drift is {block['drift_max']}")
        if pair["kind"] != "matched":
            check(pair["block_count"] == 0 and pair["moving"] == 0 and pair["arrival_overlaps"] == 0, f"pair {n} ({pair['kind']}): a static append with motion or overlap")
            check(pair["new_rule"].startswith(pair["kind"].replace("-", " ")), f"pair {n}: rule {pair['new_rule']!r} for a {pair['kind']} pair")
        else:
            check(pair["new_rule"].startswith("lowest cost"), f"pair {n}: rule {pair['new_rule']!r} for a matched pair")
            check((pair["new_tied"] > 1) == (pair["new_rule"] != "lowest cost"), f"pair {n}: tie set {pair['new_tied']} but rule {pair['new_rule']!r}")
    # Blocks are rigid up to their stated residual: members keep their mutual distances between
    # the two frames. Checked on the showcases from the witnesses themselves.
    for n in (100, 110, 260, 307):
        pair = by_n[n]
        src, dst = witness_centres(n), witness_centres(n + 1)
        for k, block in enumerate(pair["blocks"]):
            members = block["members"]
            worst = 0.0
            for a in range(len(members)):
                for b in range(a + 1, len(members)):
                    d0 = math.dist(src[members[a]], src[members[b]])
                    d1 = math.dist(dst[pair["map"][members[a]]], dst[pair["map"][members[b]]])
                    worst = max(worst, abs(d1 - d0))
            check(worst <= 2 * block["residual_max"] + 1e-6, f"pair {n}: block {k} is not rigid up to its residual ({worst:.4f} vs {block['residual_max']})")
    matched = [p for p in pairs if p["kind"] == "matched"]
    check(len(matched) == 158, f"{len(matched)} matched pairs")
    check(sum(1 for p in matched if p["moving"] and p["moving_in_block"] >= 0.5 * p["moving"]) >= 120, "fewer than 120 matched pairs move at least half in blocks")
    check(all(p["arrival_overlaps"] > 0 for p in matched), "a matched pair has no square under the new square at arrival")
    check(by_n[100]["block_count"] >= 2 and any(abs(b["turn"]) > 40 for b in by_n[100]["blocks"]), "100->101 has no turning block")
    check(by_n[110]["block_count"] >= 3 and any(abs(b["turn"]) > 20 for b in by_n[110]["blocks"]), "110->111 has no block turning back")
    print(f"record: identity chain composed over 323 maps; {sum(p['moving_in_block'] for p in matched)} of {sum(p['moving'] for p in matched)} moving squares in blocks; "
          f"new square by cost on {sum(1 for p in matched if p['new_rule'] == 'lowest cost')} pairs, by tie-break on {sum(1 for p in matched if p['new_tied'] > 1)}; "
          f"arrival overlaps on {sum(1 for p in pairs if p['arrival_overlaps'])} pairs")


def main() -> int:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    with tempfile.TemporaryDirectory(prefix="spike-v2-") as tmp:
        first = Path(tmp) / "one"
        second = Path(tmp) / "two"
        build(first)
        build(second)
        for name in ("index.html", "transition-stats.json"):
            check(digest(first / name) == digest(second / name), f"{name} differs between two runs")
        retained = HERE / "index.html"
        if retained.exists():
            check(digest(retained) == digest(first / "index.html"), "retained index.html differs from a fresh build")
        if (HERE / "transition-stats.json").exists():
            check(digest(HERE / "transition-stats.json") == digest(first / "transition-stats.json"), "retained transition-stats.json differs from a fresh build")
        stats = json.loads((first / "transition-stats.json").read_text())
        html = (first / "index.html").read_text()

    pairs = stats["pairs"]
    check(len(pairs) == 323, f"expected 323 pairs, found {len(pairs)}")
    for pair in pairs:
        n = pair["n"]
        mapping = pair["map"]
        check(len(mapping) == n, f"pair {n}: map has {len(mapping)} entries, not {n}")
        check(len(set(mapping)) == n, f"pair {n}: map is not injective")
        check(all(0 <= j <= n for j in mapping), f"pair {n}: map leaves the range 0..{n}")
        unmatched = set(range(n + 1)) - set(mapping)
        check(len(unmatched) == 1, f"pair {n}: {len(unmatched)} unmatched squares, not one")
        check(unmatched == {pair["new_index"]}, f"pair {n}: new_index disagrees with the unmatched square")

    manifest = json.loads(MANIFEST.read_text())["atlas"]["entries"]
    kind_by_n = {entry["n"]: entry["source"]["kind"] for entry in manifest}
    by_n = {pair["n"]: pair for pair in pairs}
    for n in SHARED_PICTURE_PAIRS:
        check(by_n[n]["kind"] == "shared-picture", f"pair {n}->{n + 1} is not recognised as a shared picture")
    shared_found = {pair["n"] for pair in pairs if pair["kind"] == "shared-picture"}
    check(shared_found == SHARED_PICTURE_PAIRS, f"shared-picture set is {sorted(shared_found)}")
    grid_pairs = [n for n in range(1, 324) if kind_by_n[n] == "exact-grid" and kind_by_n[n + 1] == "exact-grid"]
    check(len(grid_pairs) == 160, f"expected 160 grid-to-grid pairs, found {len(grid_pairs)}")
    for n in grid_pairs:
        check(by_n[n]["kind"] == "prefix", f"grid pair {n}->{n + 1} is not recognised as a prefix")
        check(by_n[n]["map"] == list(range(n)), f"grid pair {n}->{n + 1} does not keep every square in place")
    prefix_found = {pair["n"] for pair in pairs if pair["kind"] == "prefix"}
    check(prefix_found == set(grid_pairs), "prefix pairs are not exactly the grid-to-grid pairs")

    check("http://" not in html and "https://" not in html, "index.html references the network")
    check("Date.now" not in html and "Math.random" not in html, "index.html uses a wall clock or randomness")
    check("window.atlasTransitions" in html, "index.html does not expose the review API")
    for n in (4, 9, 10, 17, 99, 100, 110, 147, 260, 272, 307, stats["largest_max_displacement_pair"], stats["largest_rotation_count_pair"]):
        check(n in stats["embedded_pairs"], f"required pair {n}->{n + 1} is not embedded")
    embedded = set(stats["embedded_pairs"])
    check(
        any(all(k in embedded for k in range(start, start + 5)) for start in range(101, 116)),
        "no run of five consecutive pairs in 101..120 is embedded",
    )

    # Revision 5: the record.
    record_checks(stats, check)
    check(stats["motion_phases"] == PHASES and stats["arrival_fraction"] == ARRIVAL_FRACTION, "the record does not state the motion modes or the arrival fraction")
    check(stats["block_matching"]["new_square_rule"].startswith("lowest total matching cost"), "the record does not state the new-square rule")

    # Revision 2: the page's data.
    payload = payload_of(html)
    check(payload["timing"] == TIMING, f"timing defaults are {payload['timing']}")
    check(payload["n_max"] == 324, "n_max is not 324")
    check(stats["timing"] == TIMING, "transition-stats.json timing disagrees with the page")
    check(payload["motion_phases"] == PHASES and payload["arrival_fraction"] == ARRIVAL_FRACTION, "the page's motion modes or arrival fraction differ from the record")
    for pair in payload["pairs"]:
        n = pair["n"]
        expected = by_n[n - 1]["new_index"] if n > 1 else None
        check(pair["prev_new"] == expected, f"pair {n}: prev_new is {pair['prev_new']}, expected {expected}")
        frame_from, frame_to = payload["frames"][str(n)], payload["frames"][str(n + 1)]
        check(frame_from["ident"] == stats["identities"][str(n)] and frame_to["ident"] == stats["identities"][str(n + 1)], f"pair {n}: the page's identities differ from the record")
        check(all(frame_to["ident"][j] == frame_from["ident"][i] for i, j in enumerate(pair["map"])), f"pair {n}: the page's map does not carry identities")
        check(frame_to["ident"][pair["new"]] == n + 1, f"pair {n}: the page's new square is not identity {n + 1}")
        check(pair["prev_new"] is None or frame_from["ident"][pair["prev_new"]] == n, f"pair {n}: prev_new is not identity {n}")
        check(pair["blocks"] == [{k: v for k, v in b.items() if k not in ("residual_mean", "residual_max")} for b in by_n[n]["blocks"]], f"pair {n}: the page's blocks differ from the record")
        check(pair["block_of"] == by_n[n]["block_of"] and pair["new_rule"] == by_n[n]["new_rule"] and pair["new_tied"] == by_n[n]["new_tied"], f"pair {n}: the page's block or rule data differ from the record")
        for key in ("block_count", "moving", "moving_in_block", "moving_individually", "block_residual_mean", "block_residual_max", "arrival_overlaps"):
            check(pair["stats"][key] == by_n[n][key], f"pair {n}: the page's {key} differs from the record")
    record = {entry["n"]: entry for entry in json.loads(COMPOSITE.read_text())["figure"]["entries"]}
    for key, fact in payload["facts"].items():
        entry = record[int(key)]
        check(
            [(b["glyph"], b["style"], b["meaning"]) for b in fact["badges"]]
            == [(b["glyph"], b["style"], b["meaning"]) for b in entry["badges"]],
            f"n={key}: badges differ from the record",
        )
        check(all((b["glyph"], b["style"]) in BADGE_VOCABULARY for b in fact["badges"]), f"n={key}: badge outside the vocabulary")
        check(fact["star"] == entry["lower"]["first_proved_here"], f"n={key}: star disagrees with first_proved_here")
        check(fact["open"] == open_items(entry), f"n={key}: open list is {fact['open']}, expected {open_items(entry)}")
    check(payload["facts"]["100"]["open"] == [], "n=100 should leave nothing open")
    check(payload["facts"]["101"]["open"] == ["optimality", "rigidity"], "n=101 should leave optimality and rigidity open")
    check(payload["facts"]["17"]["star"] is True and payload["facts"]["100"]["star"] is False, "star flags for 17 and 100")
    check([tuple(p) for p in payload["star_points"]] == atlas_star_points(), "star polygon differs from the atlas source")
    metrics = payload["metrics"]
    check(all(0 < v < 19 for v in metrics["badge_baseline"].values()), f"badge baselines look wrong: {metrics['badge_baseline']}")
    check("n_var_raise" not in metrics and "n_eq_raise" not in metrics, "the revision-2 headline raises are still emitted")
    check((metrics["numeral_px"], metrics["n_line_px"], metrics["numeral_weight"]) == (NUMERAL_PX, N_LINE_PX, NUMERAL_WEIGHT), f"headline sizes are {metrics['numeral_px']}, {metrics['n_line_px']} at weight {metrics['numeral_weight']}")
    check(metrics["type_scale"] == TYPE_SCALE, f"type scale is {metrics['type_scale']}")
    check("numeral_left_px" not in metrics, "the stacked headline's numeral offset is still emitted")
    check(metrics["headline_gap_px"] == HEADLINE_GAP_PX, f"headline gap is {metrics['headline_gap_px']}, expected {HEADLINE_GAP_PX}")
    check(metrics["digit_bearing_px"] == digit_bearing_px(), f"digit bearing is {metrics['digit_bearing_px']} px, the fonts say {digit_bearing_px()}")
    advance, y0, y1 = katex_approx_bounds()
    approx = metrics["approx"]
    check((approx["advance"], approx["y0"], approx["y1"]) == (advance, y0, y1), f"approximately-equal metrics {approx['advance']}, {approx['y0']}, {approx['y1']} differ from KaTeX_Main")
    check(approx["d"].startswith("M") and approx["d"].endswith("Z") and (approx["font_size"], approx["stroke_units"]) == (13, 26), "approximately-equal outline looks wrong")

    # Revision 3: the lower bound is read from the record's own display, for every open n and no proved n.
    for key, fact in payload["facts"].items():
        entry = record[int(key)]
        shown = entry["lower"]["shown"]
        check(shown == (entry["optimality"]["status"] == "open"), f"n={key}: lower.shown disagrees with the optimality status")
        if shown:
            match = SIDE_DISPLAY.match(entry["lower"]["display"])
            check(match is not None and match.group(2) == "≥" and fact["lower"] == match.group(3), f"n={key}: lower is {fact['lower']!r} against display {entry['lower']['display']!r}")
        else:
            check(fact["lower"] is None, f"n={key}: proved, yet carries a lower bound {fact['lower']!r}")
    check(payload["facts"]["103"]["lower"] == "10.165151" and payload["facts"]["100"]["lower"] is None, "lower bounds for 103 and 100")

    # Revision 2: the page's text. Scarlet is defined once (the --new token) and nothing about
    # proof or optimality is coloured with it; the new elements are present.
    check(html.lower().count("a3123f") == 1, f"scarlet appears {html.lower().count('a3123f')} times, expected once")
    check("--accent" not in html and "proved optimal'" not in html, "the old scarlet status line survives")
    # The panel's lines are built by script, so their classes appear as script strings.
    for needle in ('id="progress"', 'id="mark"', "badge-query", 'class="nline"', ".lower-note {", "'lower-note'", "'proved lower bound'",
                   "data-identity", "data-phase=\"add-then-move\"", "data-phase=\"move-then-add\"", 'id="style-select"'):
        check(needle in html, f"index.html lacks {needle}")
    # Revision 9 removed the legend line that named the scarlet convention, and three of its
    # companions were flipped from presence to absence then. This one was left asserting the prose,
    # and because it fires before the browser tier it gated the whole tier off for two revisions.
    # Flipped here for the same reason the others were: the page is meant not to explain itself.
    check("scarlet marks the new square" not in html, "the scarlet legend line is back on the stage")
    # Revision 9: nothing on the stage explains the stage. The three legend lines, the sentence that
    # narrated the block matching and the keyboard hint are gone, and `check_legend.py` drives the
    # rendered page to prove none of their wording comes back at any setting.
    for gone in ('class="legend"', 'id="legend-style"', 'id="legend-note"', 'id="pair-info"',
                 "Tweens are illustrative", "the arriving square is scarlet", "Keys: "):
        check(gone not in html, f"index.html still carries the removed line {gone}")
    check('id="newsq"' not in html, "the pre-identity new-square element survives")

    # Revision 3: KaTeX_Main is embedded as the symbols face, after PT Serif in the serif stack,
    # with the relation range and the size adjustment; and the two-tilde drawing is gone.
    katex_b64 = base64.b64encode(KATEX_MAIN.read_bytes()).decode("ascii")
    check(katex_b64 in html, "KaTeX_Main-Regular.woff2 is not embedded")
    face = re.search(r"@font-face\{font-family:'Atlas Symbols';[^}]*\}", html)
    check(face is not None, "no Atlas Symbols @font-face")
    if face:
        check("size-adjust:102.5%;" in face.group(0) and f"unicode-range:{SYMBOL_RANGE};" in face.group(0), "Atlas Symbols face lacks the range or the size adjustment")
    check(re.search(r'--serif:\s*"PT Serif",\s*"Atlas Symbols"', html) is not None, "Atlas Symbols does not follow PT Serif in the serif stack")
    check(html.count("unicode-range:") == 5, f"{html.count('unicode-range:')} faces carry a unicode-range, expected 5")
    check("tildePath" not in html, "the two-tilde approximately-equal drawing survives")

    # Revision 11: one colouring and no rule to choose. The angle map is in the page — the half-degree
    # class tolerance, the slot a tilt takes, the eighteen free slots the quarter turn is cut into and
    # the contact count's shade — and the teal-to-citron sweep it replaced is not.
    for needle in ("const ANGLE_TOL = 0.5;", "function slotForAngle(", "const FREE_SLOTS = PALETTE.length - 2;", "function shadeForContacts("):
        check(needle in html, f"index.html lacks the angle map's {needle}")
    check("LONG_ARC" not in html and "Math.min(angle, 90 - angle)" not in html, "the old teal-to-citron sweep survives in the page")

    if not failures:
        browser_checks(HERE / "index.html", check)

    if failures:
        print("FAILED")
        for failure in failures:
            print(" -", failure)
        return 1
    print(
        "OK: 2 identical builds; 323 bijective correspondences; 160 prefix, 5 shared-picture, 158 matched; "
        "identity chain composed and present; blocks rigid up to their residuals, statistics and the new-square rule on every pair, "
        "overlap census present; index.html offline; badges, star, open list and lower bounds match the record; scarlet defined once; "
        "KaTeX_Main embedded and setting the relations; browser: one element per identity created once, five motion modes with "
        "add-then-move the default, styles B and C ending on n+1's poses, the new square in before anything moves, blocks rigid mid motion, n-line above the numeral, "
        f"lower-bound slots fixed, progress bar clock-pure, facts layers never overlap, scarlet mark on schedule, every fill in the {SHADE_HUES}x{SHADE_STEPS} angle-map shade table; "
        f"type scale {'/'.join(map(str, TYPE_SCALE))}, numeral {NUMERAL_PX} px at weight {NUMERAL_WEIGHT}, "
        "panel above the bar and every slot fixed over every embedded pair."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
