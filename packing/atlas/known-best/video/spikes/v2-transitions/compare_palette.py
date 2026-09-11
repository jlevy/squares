"""What the workbench paints against what the atlas paints, in OkLCh.

    packing/.venv/bin/python3 compare_palette.py [workbench.html] [--pairs N]

The claim this settles is "the workbench looks brighter than the SVGs". Brightness is
two numbers in OkLCh and they move independently: **lightness**, how pale a patch is, and
**chroma**, how far from grey. A fill can be brighter in either sense, and saying which is
the difference between lowering the ramp and desaturating it.

The atlas side is read from the rendered SVGs themselves rather than from the palette
constants, because what a square is actually painted is a *shade* of its hue and the shade
ramp is where the lightness and saturation policy lives. The workbench side is read off the
page for the same reason: its greens are generated at run time from the two ends of a sweep.

Both sides exclude what is not a square: the paper, the ink of the boundary, the labels,
and the scarlet accent, which is a mark rather than a member of a family.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
PACKING = HERE.parents[4]
RENDERINGS = PACKING / "atlas/known-best/rendering"
DEFAULT_PAGE = PACKING / "site/workbench/index.html"

#: A square in a rendering says so: every drawn square carries `data-feature="square-fill"`,
#: with its hue and shade indices beside it. Selecting on that rather than on a list of colours
#: to ignore is what keeps a real fill from being mistaken for furniture -- `#3fa8f1` reads like
#: a pointer and is in fact hue 3's lightest shade, on `n = 17`'s square 16.
SQUARE_FILL = re.compile(
    r'data-feature="square-fill"[^>]*?\bfill="(#[0-9a-fA-F]{6})"'
    r'|fill="(#[0-9a-fA-F]{6})"[^>]*?data-feature="square-fill"'
)


#: What the stage is actually painting, read off the DOM: the page has no accessor that
#: reports the frame's fills, and reading the elements is the only answer that cannot
#: disagree with what a viewer sees.
DRAWN_FILLS = """() => Array.from(document.querySelectorAll('#squares g[data-identity]'))
  .filter((g) => g.style.display !== 'none')
  .map((g) => g.firstElementChild.getAttribute('fill'))"""


def oklch(hex_colour: str) -> tuple[float, float, float]:
    """(lightness, chroma, hue in degrees) of an sRGB hex colour."""

    def linear(channel: int) -> float:
        c = channel / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (linear(int(hex_colour[i : i + 2], 16)) for i in (1, 3, 5))
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    lightness = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return lightness, math.hypot(a, bb), (math.degrees(math.atan2(bb, a)) + 360) % 360


def atlas_fills() -> dict[str, int]:
    """Every square fill the rendered atlas uses, with how many squares carry it."""
    tally: dict[str, int] = {}
    for svg in sorted(RENDERINGS.glob("n-*.svg")):
        for before, after in SQUARE_FILL.findall(svg.read_text(encoding="utf-8")):
            key = (before or after).lower()
            tally[key] = tally.get(key, 0) + 1
    if not tally:
        raise SystemExit(f"no square fills under {RENDERINGS}: is the atlas rendered?")
    return tally


def workbench_fills(page_path: Path, pairs: int) -> dict[str, dict[str, int]]:
    """Every fill the page paints at rest, under each colouring it offers.

    Sampled at the settled instant of evenly spaced pairs, in Animate -- which is the mode
    the film and the video are captured in, and the one whose resting frame is repainted.
    """
    out: dict[str, dict[str, int]] = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(page_path.resolve().as_uri(), wait_until="load")
        page.evaluate("document.fonts.ready")
        page.evaluate("window.atlasTransitions.setMode('animate')")
        page.evaluate("window.atlasTransitions.setCapture(true)")
        # The stage trims chroma to compensate for drawing one packing where the atlas draws a page
        # of them. Set to 1 here: the claim being checked is that the stage's colours ARE the
        # atlas's, and the trim is a presentation setting on top of that rather than a palette.
        page.evaluate("window.atlasTransitions.setStageChroma(1)")
        count = page.evaluate("window.atlasTransitions.pairs().length")
        picks = sorted({round(i * (count - 1) / max(1, pairs - 1)) for i in range(pairs)})
        for scheme in page.evaluate("window.atlasTransitions.colorSchemes()"):
            page.evaluate(f"window.atlasTransitions.setColorScheme({json.dumps(scheme)})")
            tally: dict[str, int] = {}
            for index in picks:
                page.evaluate(f"window.atlasTransitions.select({index})")
                page.evaluate("window.atlasTransitions.seek(window.atlasTransitions.duration())")
                for fill in page.evaluate(DRAWN_FILLS):
                    key = str(fill).lower()
                    tally[key] = tally.get(key, 0) + 1
            out[scheme] = tally
        browser.close()
    return out


def per_n(page_path: Path, wanted: list[int]) -> None:
    """The atlas's fills for one n against the page's, square for square.

    The band comparison says whether the two ramps sit in the same place; this says whether
    a given packing is painted the same way, which is the claim that actually matters. The
    comparison is on the multiset of fills, not on square order: the page numbers its squares
    by identity and the rendering by the witness, and the two need not agree.
    """
    print("\n== one packing at a time: the rendering against the page ==")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(page_path.resolve().as_uri(), wait_until="load")
        page.evaluate("document.fonts.ready")
        page.evaluate("window.atlasTransitions.setMode('animate')")
        page.evaluate("window.atlasTransitions.setCapture(true)")
        # The stage trims chroma to compensate for drawing one packing where the atlas draws a page
        # of them. Set to 1 here: the claim being checked is that the stage's colours ARE the
        # atlas's, and the trim is a presentation setting on top of that rather than a palette.
        page.evaluate("window.atlasTransitions.setStageChroma(1)")
        pairs = page.evaluate("window.atlasTransitions.pairs().map((p) => p.n)")
        for n in wanted:
            svg = RENDERINGS / f"n-{n:03d}.svg"
            if not svg.exists() or (n - 1) not in pairs:
                print(f"  n = {n:<4} not on both surfaces")
                continue
            want: dict[str, int] = {}
            for before, after in SQUARE_FILL.findall(svg.read_text(encoding="utf-8")):
                key = (before or after).lower()
                want[key] = want.get(key, 0) + 1
            page.evaluate(f"window.atlasTransitions.select({pairs.index(n - 1)})")
            page.evaluate("window.atlasTransitions.seek(window.atlasTransitions.duration())")
            got: dict[str, int] = {}
            for fill in page.evaluate(DRAWN_FILLS):
                key = str(fill).lower()
                got[key] = got.get(key, 0) + 1
            if want == got:
                print(f"  n = {n:<4} same {sum(want.values())} squares, same fills")
                continue
            only_svg = sorted(set(want) - set(got))
            only_page = sorted(set(got) - set(want))
            print(f"  n = {n:<4} DIFFERENT")
            print(f"      rendering: {'  '.join(f'{c} x{want[c]}' for c in sorted(want))}")
            print(f"      page:      {'  '.join(f'{c} x{got[c]}' for c in sorted(got))}")
            if only_svg or only_page:
                print(f"      only in the rendering: {only_svg}   only on the page: {only_page}")
        browser.close()


def band(name: str, tally: dict[str, int]) -> None:
    """The lightness and chroma the fills actually occupy, weighted by how many squares."""
    if not tally:
        print(f"{name:<22} (nothing)")
        return
    weighted = [(oklch(fill), n) for fill, n in tally.items()]
    squares = sum(tally.values())

    def spread(index: int) -> tuple[float, float, float]:
        values = sorted(v[index] for v, _ in weighted)
        mean = sum(v[index] * n for v, n in weighted) / squares
        return values[0], mean, values[-1]

    lo_l, mean_l, hi_l = spread(0)
    lo_c, mean_c, hi_c = spread(1)
    print(
        f"{name:<22} {len(tally):>4} fills {squares:>6} squares   "
        f"L {lo_l:.3f}-{hi_l:.3f} mean {mean_l:.3f}   C {lo_c:.3f}-{hi_c:.3f} mean {mean_c:.3f}"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("page", nargs="?", type=Path, default=DEFAULT_PAGE)
    ap.add_argument("--pairs", type=int, default=24, help="how many pairs to sample")
    ap.add_argument("--per-n", type=int, nargs="*", help="compare these n square for square")
    o = ap.parse_args()

    atlas = atlas_fills()
    print("== what each surface paints a square, in OkLCh ==")
    band("atlas renderings", atlas)
    for scheme, tally in workbench_fills(o.page, o.pairs).items():
        band(f"workbench {scheme}", tally)

    if o.per_n is not None:
        per_n(o.page, o.per_n or [5, 11, 17, 26, 29, 100])

    print("\n== the atlas's own ramp, by hue family ==")
    families: dict[int, list[tuple[float, float, str]]] = {}
    for fill, _ in sorted(atlas.items(), key=lambda kv: -kv[1]):
        lightness, chroma, hue = oklch(fill)
        families.setdefault(round(hue / 20) * 20, []).append((lightness, chroma, fill))
    for hue in sorted(families):
        members = sorted(families[hue])
        shown = " ".join(f"{fill}({l:.2f}/{c:.2f})" for l, c, fill in members[:6])
        print(f"  hue ~{hue:>3}  {len(members):>2} shades  {shown}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
