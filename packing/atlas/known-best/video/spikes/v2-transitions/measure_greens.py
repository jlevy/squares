"""How many distinguishable greens the identity scheme generates, measured off the page.

    packing/.venv/bin/python3 measure_greens.py [workbench.html] [--identities N]

Revision 12 makes a square's colour a property of its identity, from a ramp of greens the page
generates itself out of the two ends of the teal-to-citron sweep. Two numbers say whether that ramp
is any good, and this is where both of them come from:

  * the **resolution** of the ramp — the smallest OkLab distance between any two of its greens,
    which is how far apart the two most confusable squares on a stage can be;
  * the **neighbour separation** — the smallest distance between the greens of two consecutive
    identities, which is what the co-prime stride is for.

Distances are plain Euclidean OkLab, which is the space the page mixes and drains colour in. An
OkLab distance of about 0.02 is one just-noticeable step for two large patches side by side, so the
count reported as *distinguishable* is the number of greens whose pairwise distances all clear a
threshold, 0.02 by default.
"""

import math
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
JND = 0.02


def oklab(hex_colour: str) -> tuple[float, float, float]:
    """An sRGB hex colour in OkLab, as the page's own `hexToLab` computes it."""
    def linear(channel: int) -> float:
        c = channel / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (linear(int(hex_colour[i : i + 2], 16)) for i in (1, 3, 5))
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def hue(hex_colour: str) -> float:
    _, a, b = oklab(hex_colour)
    return (math.degrees(math.atan2(b, a)) + 360) % 360


def distance(x: str, y: str) -> float:
    return math.dist(oklab(x), oklab(y))


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    page_path = (HERE / args[0]) if args else HERE / "workbench.html"
    identities = 324
    if "--identities" in sys.argv:
        identities = int(sys.argv[sys.argv.index("--identities") + 1])

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(f"file://{page_path}")
        page.wait_for_timeout(900)
        book = page.evaluate("atlasTransitions.colour()")
        ramp: list[str] = book["greens"]
        stride: int = book["greenStride"]
        by_identity: list[str] = page.evaluate(f"atlasTransitions.identityFills({identities})")
        browser.close()

    period = len(ramp)
    print(f"the ramp: {period} greens, stride {stride}, {len(set(ramp))} of them distinct")
    hues = [hue(h) for h in ramp]
    print(f"hue band: {min(hues):.1f} to {max(hues):.1f} degrees (teal is 174.6, citron 109.4)")

    pairs = [(distance(ramp[i], ramp[j]), ramp[i], ramp[j], i, j)
             for i in range(period) for j in range(i + 1, period)]
    pairs.sort()
    closest = pairs[0]
    print(f"resolution: the closest two are {closest[0]:.4f} apart in OkLab "
          f"({closest[1]} at index {closest[3]}, {closest[2]} at index {closest[4]})")
    for threshold in (0.015, 0.02, 0.025, 0.03, 0.04):
        keep: list[str] = []
        for colour in ramp:
            if all(distance(colour, other) >= threshold for other in keep):
                keep.append(colour)
        marker = "  <- the JND used below" if abs(threshold - JND) < 1e-9 else ""
        print(f"  at a threshold of {threshold:.3f}: {len(keep)} mutually distinguishable{marker}")

    neighbours = [(distance(by_identity[i], by_identity[i + 1]), i + 1, i + 2)
                  for i in range(len(by_identity) - 1)]
    neighbours.sort()
    print(f"neighbours: identities {neighbours[0][1]} and {neighbours[0][2]} are the closest "
          f"consecutive pair, {neighbours[0][0]:.4f} apart")
    repeats = len(by_identity) / period
    print(f"over {len(by_identity)} identities the ramp turns {repeats:.1f} times; "
          f"identity k and identity k + {period} share a colour and nothing else does")
    all_ok = all(d >= JND for d, *_ in pairs)
    print(f"every pair clears the {JND} just-noticeable step: {'yes' if all_ok else 'no'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
