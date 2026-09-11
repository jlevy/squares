#!/usr/bin/env python3
"""Headless smoke check of styles B (physics) and C (bodies) in index.html.

    packing/.venv/bin/python3 smoke_styles.py

Loads index.html in the pinned headless shell and, under each of the two physical styles,
checks that no console or page error is raised, that the Style select, the `p` key and
setStyle() agree, that seek() at three instants renders finite poses and is idempotent,
that the cached trajectory for 100->101 ends within 1e-6 of the target poses, that the
view is held at n's scale mid-move and refitted by the end of the settle, and that style A
renders the same DOM after a visit to B and C as on a fresh page. It reports the per-pair
precompute cost (performance.now inside the page) for n = 100, 272 and 323 under both
styles, and writes the review stills review/style-*.png at 1920x1080 in capture preview.
"""

from __future__ import annotations

import math
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE = HERE / "index.html"
REVIEW = HERE / "review"

# (file, style, pair n, seconds): dwell to 1.0, move to 2.4, settle to 2.8 at the
# default timing.
STILLS = [
    ("style-B-100-mid", "physics", 100, 1.7),
    ("style-C-100-mid", "bodies", 100, 1.7),
    ("style-C-110-mid", "bodies", 110, 1.7),
    ("style-C-307-mid", "bodies", 307, 1.7),
]
TIMED = [100, 272, 323]
END_TOLERANCE = 1e-6
STYLES = ["tween", "physics", "bodies"]

# The scene as drawn: the view, the container and every shown pool element's pose and
# fill. (The pool keeps hidden elements for every identity ever shown, so the raw
# outerHTML grows with the pairs visited; the picture does not.)
SCENE_JS = (
    "JSON.stringify([document.getElementById('packing-svg').getAttribute('viewBox'),"
    " document.getElementById('container').getAttribute('width'),"
    " Array.from(document.querySelectorAll('#squares g'))"
    ".filter(g => g.style.display !== 'none')"
    "  .map(g => [g.dataset.identity, g.getAttribute('transform'),"
    " g.getAttribute('opacity'), g.firstElementChild.getAttribute('fill')]),"
    " document.getElementById('mark').getAttribute('opacity'),"
    " document.getElementById('mark').getAttribute('transform')])"
)
VIEWBOX_JS = "document.getElementById('packing-svg').getAttribute('viewBox')"
VIEWBOX_WIDTH_JS = (
    "document.getElementById('packing-svg').getAttribute('viewBox').split(' ')[2]"
)
NON_FINITE_JS = (
    "Array.from(document.querySelectorAll('#squares g'))"
    ".map(g => g.getAttribute('transform') || '')"
    ".filter(t => /NaN|Infinity/.test(t)).length"
)


def angle_error(a: float, b: float) -> float:
    """Distance between two angles modulo 90 degrees."""
    d = (a - b) % 90.0
    return min(d, 90.0 - d)


def end_error(page, index: int, style: str) -> tuple[float, float, dict]:
    """(max position error, max angle error in degrees) of the cached final state.

    Measured against the target poses for n+1.
    """
    info = page.evaluate(f"window.atlasTransitions.physics({index}, '{style}')")
    data = page.evaluate("JSON.parse(document.getElementById('atlas-data').textContent)")
    pair = data["pairs"][index]
    target = data["frames"][str(pair["n"] + 1)]["squares"]
    max_pos = 0.0
    max_ang = 0.0
    for i, (x, y, deg) in enumerate(info["final"]):
        tgt = target[pair["map"][i]] if i < pair["n"] else target[pair["new"]]
        max_pos = max(max_pos, math.hypot(x - tgt[0], y - tgt[1]))
        max_ang = max(max_ang, angle_error(deg, tgt[2]))
    return max_pos, max_ang, info


def main() -> int:
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    errors: list[str] = []
    started = time.perf_counter()
    failures = 0

    def check(ok: bool, message: str) -> None:  # noqa: FBT001
        nonlocal failures
        if not ok:
            failures += 1
            print("FAIL:", message)

    REVIEW.mkdir(exist_ok=True)
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get("SQPACK_CHROMIUM"))
        try:
            page = browser.new_page(
                viewport={"width": 1920, "height": 1080}, device_scale_factor=1
            )
            page.on(
                "console",
                lambda msg: errors.append(f"console.{msg.type}: {msg.text}")
                if msg.type in ("error", "warning")
                else None,
            )
            page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
            page.goto(PAGE.resolve().as_uri(), wait_until="load")
            page.evaluate("document.fonts.ready")
            page.evaluate("window.atlasTransitions.setCapture(true)")
            api = "window.atlasTransitions"
            pairs = page.evaluate(f"{api}.pairs().map(p => p.n)")
            index_of = {n: i for i, n in enumerate(pairs)}
            print(f"loaded {PAGE.name} ({PAGE.stat().st_size} bytes): {len(pairs)} pairs")
            check(
                page.evaluate(f"{api}.styles()") == STYLES,
                "styles() is not tween, physics, bodies",
            )
            check(
                page.evaluate(f"{api}.state().style") == "tween",
                "the page does not start in the tween",
            )

            # Style A's frame of 100->101 mid-move on a fresh page, compared at the end
            # with the same frame after visits to B and C.
            page.evaluate(f"{api}.select({index_of[100]})")
            page.evaluate(f"{api}.seek(1.7)")
            tween_fresh = page.evaluate(SCENE_JS)

            # The p key cycles tween -> physics -> bodies -> tween; the select follows.
            for expected in ("physics", "bodies", "tween"):
                page.keyboard.press("p")
                check(
                    page.evaluate(f"{api}.state().style") == expected,
                    f"the p key did not reach {expected}",
                )
            for style, letter in (("physics", "B"), ("bodies", "C")):
                page.evaluate(f"{api}.setStyle('{style}')")
                check(
                    page.evaluate(f"{api}.state().style") == style,
                    f"setStyle('{style}') did not take",
                )
                check(
                    page.evaluate("document.getElementById('style-select').value") == style,
                    f"the select does not show {style}",
                )
                # Revision 9 removed the legend line that named the style; the select is
                # the one place the page says which style is on, and `state()` is the one
                # place the API does.
                check(
                    page.evaluate(f"{api}.state().style") == style,
                    f"state() does not report style {letter}",
                )

            for style in ("physics", "bodies"):
                page.evaluate(f"{api}.setStyle('{style}')")
                page.evaluate(f"{api}.select({index_of[100]})")
                # Three instants render finite poses.
                for seconds in (1.12, 1.7, 2.4):
                    page.evaluate(f"{api}.seek({seconds})")
                    bad = page.evaluate(NON_FINITE_JS)
                    check(bad == 0, f"{style}: {bad} non-finite transforms at t = {seconds}")
                    vb = page.evaluate(VIEWBOX_JS)
                    check(
                        "NaN" not in vb,
                        f"{style}: viewBox is not finite at t = {seconds}: {vb}",
                    )
                # seek is idempotent.
                page.evaluate(f"{api}.seek(1.7)")
                first = page.evaluate(SCENE_JS)
                page.evaluate(f"{api}.seek(0.2)")
                page.evaluate(f"{api}.seek(2.6)")
                page.evaluate(f"{api}.seek(1.7)")
                check(first == page.evaluate(SCENE_JS), f"{style}: seek(1.7) is not idempotent")
                # The held scale: at t = 1.7 the view is n's; at the end of the settle it
                # is n+1's.
                view_mid = float(page.evaluate(VIEWBOX_WIDTH_JS))
                page.evaluate(f"{api}.seek(2.8)")
                view_end = float(page.evaluate(VIEWBOX_WIDTH_JS))
                check(
                    abs(view_mid - 10.9) < 1e-6,
                    f"{style}: the view is not held at n's scale mid-move ({view_mid})",
                )
                check(
                    abs(view_end - 10.535534 * 1.09) < 1e-3,
                    f"{style}: the view did not refit to n+1 by the end of the settle"
                    f" ({view_end})",
                )
                # The trajectory ends on the target poses.
                max_pos, max_ang, info = end_error(page, index_of[100], style)
                print(
                    f"{style} 100->101: {info['bodies']} bodies, {info['steps']} steps,"
                    f" {info['bytes']} bytes, end error {max_pos:.2e} units"
                    f" / {max_ang:.2e} deg, "
                    f"peak speed {info['maxSpeedPerMove']:.1f} units per move,"
                    f" deepest overlap {info['maxPenetration']:.3f} firm,"
                    f" {info['maxPenetrationLate']:.3f} after lock-in"
                )
                check(
                    max_pos < END_TOLERANCE and max_ang < END_TOLERANCE,
                    f"{style}: 100->101 does not end within 1e-6 of the target poses",
                )
                # Precompute cost, per pair, measured inside the page (a fresh simulation
                # each: the cache is keyed by style, pair and step count, and these pairs
                # were not visited yet).
                for n in TIMED:
                    if n == 100 or n not in index_of:
                        continue
                    info = page.evaluate(f"{api}.physics({index_of[n]}, '{style}')")
                    print(
                        f"{style} precompute n = {n}: {info['ms']:.1f} ms"
                        f" for {info['steps']} steps ({info['n'] + 1} squares,"
                        f" {info['bodies']} bodies), "
                        f"peak speed {info['maxSpeedPerMove']:.1f} units per move,"
                        f" deepest overlap {info['maxPenetration']:.3f} firm,"
                        f" {info['maxPenetrationLate']:.3f} after lock-in"
                    )
                info = page.evaluate(f"{api}.physics({index_of[100]}, '{style}')")
                print(f"{style} precompute n = 100: {info['ms']:.1f} ms (cached run above)")

            # The stills.
            for name, style, n, seconds in STILLS:
                if n not in index_of:
                    print(f"skip {name}: pair {n} is not embedded")
                    continue
                page.evaluate(f"{api}.setStyle('{style}')")
                page.evaluate(f"{api}.select({index_of[n]})")
                page.evaluate(f"{api}.seek({seconds})")
                page.screenshot(path=str(REVIEW / f"{name}.png"), type="png")
                print("wrote", REVIEW / f"{name}.png")

            # Style A is untouched by the switches: the same instant renders the same DOM
            # as on the fresh page.
            page.evaluate(f"{api}.setStyle('tween')")
            page.evaluate(f"{api}.select({index_of[100]})")
            page.evaluate(f"{api}.seek(1.7)")
            tween_after = page.evaluate(SCENE_JS)
            check(
                tween_fresh == tween_after,
                "style A renders differently after visits to B and C",
            )
            if tween_fresh != tween_after:
                import difflib  # noqa: PLC0415

                a_parts = tween_fresh.replace("><", ">\n<").split("\n")
                b_parts = tween_after.replace("><", ">\n<").split("\n")
                diff = difflib.unified_diff(
                    a_parts, b_parts, "fresh", "after", lineterm="", n=0
                )
                for line in list(diff)[:20]:
                    print("   ", line[:200])
        finally:
            browser.close()

    print(f"total {time.perf_counter() - started:.1f} s")
    if errors:
        print("browser reported:")
        for line in errors:
            print(" ", line)
        return 1
    if failures:
        print(f"{failures} check(s) failed")
        return 1
    print("no console errors, page errors or failed checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
