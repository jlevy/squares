#!/usr/bin/env python3
"""Headless smoke test and capture-pipeline prototype for index.html.

    packing/.venv/bin/python3 smoke_capture.py            # stills of several pairs and instants
    packing/.venv/bin/python3 smoke_capture.py --review   # the review stills, to review/
    packing/.venv/bin/python3 smoke_capture.py --ink      # measure the panel's ink edges (headline alignment)
    packing/.venv/bin/python3 smoke_capture.py --video 100 --fps 30   # every frame of 100->101, then ffmpeg

Uses the repository's pinned Playwright 1.62.0 and the chromium headless shell already
in the host cache; the virtual clock is driven through window.atlasTransitions.seek, so
frame k is rendered at exactly k / fps seconds regardless of how long the screenshot takes.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE = HERE / "index.html"
FFMPEG = "/opt/homebrew/bin/ffmpeg"

STILLS = [
    # (pair n, seconds, colour rule, overlay); the pair is 2.8 s: dwell to 1.0, move to 2.4, settle to 2.8
    (4, 0.0, "continuous", False),
    (4, 1.7, "continuous", False),
    (4, 2.8, "continuous", False),
    (10, 1.7, "continuous", True),
    (100, 0.0, "continuous", False),
    (100, 1.6, "continuous", False),
    (100, 2.1, "continuous", False),
    (100, 2.5, "continuous", False),
    (100, 2.8, "continuous", False),
    (100, 1.7, "house", False),
    (100, 1.7, "continuous", True),
    (110, 1.7, "continuous", False),
    (147, 2.8, "continuous", False),
    (260, 1.7, "continuous", False),
    (260, 1.7, "house", False),
    (272, 1.7, "continuous", False),
    (272, 2.8, "house", False),
]

# The review set, written to review/<name>.png in capture preview, in the default motion
# (add, then move: the new square arrives over the first 30% of the move, the blocks move over
# the rest). The instants are named rather than numbered: dwell 0.5 s, arrival 1.42 s (the new
# square fully in, nothing else moved yet), mid-block 1.91 s (the blocks half way), move-end
# 2.4 s, settle 2.8 s (the pair's end, the fill at rest and the outline thinned). Pairs not
# embedded in index.html are taken from index-all.html.
ARRIVAL = 1.0 + 1.4 * 0.3
MID_BLOCK = ARRIVAL + 1.4 * 0.7 / 2
REVIEW = [
    # (name, pair n, seconds)
    ("100-dwell", 100, 0.5),
    ("100-arrival", 100, ARRIVAL),
    ("100-mid-block", 100, MID_BLOCK),
    ("100-move-end", 100, 2.4),
    ("100-settle", 100, 2.8),
    ("101-dwell", 101, 0.5),
    ("110-arrival", 110, ARRIVAL),
    ("110-mid-block", 110, MID_BLOCK),
    ("307-mid-block", 307, MID_BLOCK),
    ("260-mid-block", 260, MID_BLOCK),
    ("004-settle", 4, 2.8),
    ("147-settle", 147, 2.8),
    ("017-dwell", 17, 0.5),
    ("103-dwell", 103, 0.5),
    ("028-dwell", 28, 0.5),
]


# The panel's text slots, as template.html places them (stage y ranges), for the ink measurement.
# Revision 4's slots; the bands end where the next slot's box begins.
INK_BANDS = [
    ("eyebrow", 200, 250),
    ("n-line", 250, 300),
    ("numeral", 300, 424),
    ("side", 424, 488),
    ("exact", 488, 552),
    ("lower", 552, 598),
    ("lower-note", 598, 646),
    ("badges", 660, 708),
    ("open", 740, 816),
    ("legend", 854, 900),
]
INK_X0, INK_X1 = 1100, 1900   # the panel's columns; the packing ends at x = 1060
INK_THRESHOLD = 160           # a pixel darker than this (mean of R, G, B) is ink
INK_PAIRS = [(103, 0.5), (28, 0.5), (17, 0.5), (100, 0.5), (147, 2.8)]


def measure_ink(driver) -> None:
    """Leftmost and vertical ink extents of each panel slot, from a capture-preview screenshot.

    Reports, per n, where the ink of the `n =` line, the numeral and the s(n) lines begins, so
    the headline's left alignment is a measured number rather than an eyeballed one.
    """
    from io import BytesIO  # noqa: PLC0415

    from PIL import Image  # noqa: PLC0415

    browser = driver.chromium.launch(executable_path=os.environ.get("SQPACK_CHROMIUM"))
    try:
        pages: dict[Path, object] = {}

        def page_for(path: Path):
            if path not in pages:
                page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
                page.goto(path.resolve().as_uri(), wait_until="load")
                page.evaluate("document.fonts.ready")
                page.evaluate("window.atlasTransitions.setCapture(true)")
                pages[path] = page
            return pages[path]

        small = page_for(PAGE)
        embedded = {n: i for i, n in enumerate(small.evaluate("window.atlasTransitions.pairs().map(p => p.n)"))}
        print(f"{'n':>4} {'instant':>7} | " + " | ".join(f"{name:>10}" for name, _, _ in INK_BANDS))
        print("     ink left x, ink rows (stage pixels); '-' for an empty slot")
        for n, seconds in INK_PAIRS:
            if n in embedded:
                page, index = small, embedded[n]
            elif (HERE / "index-all.html").exists():
                page, index = page_for(HERE / "index-all.html"), n - 1
            else:
                print(f"skip {n}: not embedded and index-all.html is absent")
                continue
            page.evaluate(f"window.atlasTransitions.select({index})")
            page.evaluate(f"window.atlasTransitions.seek({seconds})")
            image = Image.open(BytesIO(page.screenshot(type="png"))).convert("L")
            pixels = image.load()
            cells = []
            for _name, y0, y1 in INK_BANDS:
                left, top, bottom = None, None, None
                for y in range(y0, y1):
                    for x in range(INK_X0, INK_X1):
                        if pixels[x, y] < INK_THRESHOLD:
                            left = x if left is None else min(left, x)
                            top = y if top is None else top
                            bottom = y
                            break
                cells.append("-" if left is None else f"{left} {top}-{bottom}")
            shown = n + 1 if seconds >= 1.933 else n
            print(f"{shown:>4} {seconds:>6.1f}s | " + " | ".join(f"{c:>10}" for c in cells))
    finally:
        browser.close()


def capture_review(driver, out: Path) -> list[str]:
    """Write the review stills; returns any console errors or page errors seen."""
    errors: list[str] = []
    out.mkdir(parents=True, exist_ok=True)
    browser = driver.chromium.launch(executable_path=os.environ.get("SQPACK_CHROMIUM"))
    pages: dict[Path, object] = {}
    try:
        def page_for(path: Path):
            if path not in pages:
                page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
                page.on("console", lambda msg: errors.append(f"console.{msg.type}: {msg.text}") if msg.type in ("error", "warning") else None)
                page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
                page.goto(path.resolve().as_uri(), wait_until="load")
                page.evaluate("document.fonts.ready")
                page.evaluate("window.atlasTransitions.setCapture(true)")
                pages[path] = page
            return pages[path]

        small = page_for(PAGE)
        embedded = {n: i for i, n in enumerate(small.evaluate("window.atlasTransitions.pairs().map(p => p.n)"))}
        for name, n, seconds in REVIEW:
            if n in embedded:
                page, index = small, embedded[n]
            elif (HERE / "index-all.html").exists():
                page = page_for(HERE / "index-all.html")
                index = n - 1
            else:
                print(f"skip {name}: pair {n} is not embedded and index-all.html is absent")
                continue
            page.evaluate(f"window.atlasTransitions.select({index})")
            page.evaluate(f"window.atlasTransitions.seek({seconds})")
            page.screenshot(path=str(out / f"{name}.png"), type="png")
            print("wrote", out / f"{name}.png")
    finally:
        browser.close()
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=int, help="capture every frame of the pair n->n+1 and encode it")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--out", type=Path, default=HERE / "frames")
    parser.add_argument("--page", type=Path, default=PAGE, help="which built page to load (index.html or index-all.html)")
    parser.add_argument("--review", action="store_true", help="write the review stills to review/ and stop")
    parser.add_argument("--ink", action="store_true", help="measure the panel's ink edges for the headline alignment and stop")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    page_path = args.page.resolve()

    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    errors: list[str] = []
    started = time.perf_counter()
    if args.ink:
        with sync_playwright() as driver:
            measure_ink(driver)
        print(f"total {time.perf_counter() - started:.1f} s")
        return 0
    if args.review:
        with sync_playwright() as driver:
            errors = capture_review(driver, HERE / "review")
        print(f"total {time.perf_counter() - started:.1f} s")
        if errors:
            print("browser reported:")
            for line in errors:
                print(" ", line)
            return 1
        print("no console errors or page errors")
        return 0
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get("SQPACK_CHROMIUM"))
        try:
            page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
            page.on("console", lambda msg: errors.append(f"console.{msg.type}: {msg.text}") if msg.type in ("error", "warning") else None)
            page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
            t_load = time.perf_counter()
            page.goto(page_path.as_uri(), wait_until="load")
            print(f"loaded {page_path.name} ({page_path.stat().st_size} bytes) in {time.perf_counter() - t_load:.2f} s")
            page.evaluate("document.fonts.ready")
            page.evaluate("window.atlasTransitions.setCapture(true)")
            pairs = page.evaluate("window.atlasTransitions.pairs().map(p => p.n)")
            index_of = {n: i for i, n in enumerate(pairs)}
            duration = page.evaluate("window.atlasTransitions.duration()")
            print(f"page loaded: {len(pairs)} pairs, duration per pair {duration:.3f} s")

            if args.video is not None:
                n = args.video
                page.evaluate(f"window.atlasTransitions.select({index_of[n]})")
                frames = int(round(duration * args.fps))
                frame_dir = args.out / f"video-{n:03d}"
                frame_dir.mkdir(exist_ok=True)
                t0 = time.perf_counter()
                for k in range(frames + 1):
                    page.evaluate(f"window.atlasTransitions.seek({k / args.fps})")
                    page.screenshot(path=str(frame_dir / f"{k:05d}.png"), type="png")
                elapsed = time.perf_counter() - t0
                print(f"captured {frames + 1} frames of {n}->{n + 1} in {elapsed:.1f} s ({elapsed / (frames + 1) * 1000:.0f} ms per frame)")
                mp4 = args.out / f"transition-{n:03d}.mp4"
                cmd = [
                    FFMPEG, "-y", "-loglevel", "error", "-framerate", str(args.fps),
                    "-i", str(frame_dir / "%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
                    "-movflags", "+faststart", str(mp4),
                ]
                t0 = time.perf_counter()
                subprocess.run(cmd, check=True)
                print(f"encoded {mp4.name}: {mp4.stat().st_size} bytes in {time.perf_counter() - t0:.1f} s")
            else:
                for n, seconds, rule, overlay in STILLS:
                    if n not in index_of:
                        print(f"skip {n}: not embedded")
                        continue
                    page.evaluate(f"window.atlasTransitions.select({index_of[n]})")
                    page.evaluate(f"window.atlasTransitions.setColorRule('{rule}')")
                    page.evaluate(f"window.atlasTransitions.setOverlay({'true' if overlay else 'false'})")
                    page.evaluate(f"window.atlasTransitions.seek({seconds})")
                    name = f"{n:03d}-{seconds:.2f}s-{rule}{'-overlay' if overlay else ''}.png"
                    page.screenshot(path=str(args.out / name), type="png")
                    print("wrote", name)
                # Determinism of a rendered instant: same seek, same DOM.
                page.evaluate(f"window.atlasTransitions.select({index_of[100]})")
                page.evaluate("window.atlasTransitions.setColorRule('continuous')")
                page.evaluate("window.atlasTransitions.setOverlay(false)")
                page.evaluate("window.atlasTransitions.seek(2.2)")
                first = page.evaluate("document.getElementById('packing-svg').outerHTML")
                page.evaluate("window.atlasTransitions.seek(0.3)")
                page.evaluate("window.atlasTransitions.seek(2.2)")
                second = page.evaluate("document.getElementById('packing-svg').outerHTML")
                print("seek is idempotent:", first == second)
                # Play for a moment on the real rAF clock, then confirm the clock only moved while playing.
                page.evaluate("window.atlasTransitions.seek(0)")
                page.evaluate("window.atlasTransitions.play()")
                page.wait_for_timeout(400)
                page.evaluate("window.atlasTransitions.pause()")
                t_after = page.evaluate("window.atlasTransitions.state().t")
                page.wait_for_timeout(200)
                t_later = page.evaluate("window.atlasTransitions.state().t")
                print(f"played 0.4 s of wall time: virtual clock at {t_after:.3f} s, still {t_later:.3f} s after pausing")
        finally:
            browser.close()
    print(f"total {time.perf_counter() - started:.1f} s")
    if errors:
        print("browser reported:")
        for line in errors:
            print(" ", line)
        return 1
    print("no console errors or page errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
