"""The worst frame the viewer sees at a pair boundary during continuous play.

A probe on requestAnimationFrame records the timestamp and the pair at every frame of a
30-pair run; the boundary stall is the frame delta across a frame where the pair changed,
which is where the next pair's DOM is built and, without the prefetch, its physics run.

    packing/.venv/bin/python3 measure_stall.py [--page index-all.html] [--start 100]
                              [--pairs 30] [--styles bodies,physics] [--no-prefetch]
"""

import argparse
import statistics
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent

PROBE = """
([startN, style, prefetch]) => {
  const A = window.atlasTransitions;
  A.stopAll(); A.setStyle(style); A.goTo(startN); A.setContinuous({prefetch});
  window.__frames = [];
  const token = (window.__token = (window.__token || 0) + 1);
  const probe = (ts) => {
    if (window.__token !== token) return;   // one probe per run: an earlier loop stops here
    const s = A.state();
    window.__frames.push([ts, s.pair, s.t, A.schedule().moveStart]);
    requestAnimationFrame(probe);
  };
  requestAnimationFrame(probe);
  A.playAll();
  return A.state().pair;
}
"""


def note_console(errors: list[str], message) -> None:
    """Keep the console errors and ignore everything else the page says."""
    if message.type == "error":
        errors.append(f"console.{message.type}: {message.text}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", default="index-all.html")
    ap.add_argument("--start", type=int, default=100)
    ap.add_argument("--pairs", type=int, default=30)
    ap.add_argument("--styles", default="physics,bodies")
    ap.add_argument("--no-prefetch", action="store_true")
    args = ap.parse_args()
    page_path = HERE / args.page

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        errors: list[str] = []
        page.on("console", lambda m: note_console(errors, m))
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(f"file://{page_path}")
        page.wait_for_timeout(900)
        for style in args.styles.split(","):
            first = page.evaluate(PROBE, [args.start, style, not args.no_prefetch])
            target = first + args.pairs
            page.wait_for_function(
                "t => atlasTransitions.state().pair >= t || !atlasTransitions.state().playing",
                arg=target,
                timeout=300000,
                polling=200,
            )
            page.evaluate("atlasTransitions.stopAll()")
            frames = page.evaluate("window.__frames")
            # Each frame delta is classified by what happened across it: the pair changed
            # (the DOM of the next pair is built there), the move began (where an
            # unprefetched simulation runs), or neither.
            classes: dict[str, list[float]] = {
                "boundary": [],
                "move start": [],
                "elsewhere": [],
            }
            for i in range(1, len(frames)):
                (t0, p0, c0, _m0), (t1, p1, c1, m1) = frames[i - 1], frames[i]
                d = t1 - t0
                if p1 != p0:
                    classes["boundary"].append(d)
                elif c0 < m1 <= c1:
                    classes["move start"].append(d)
                else:
                    classes["elsewhere"].append(d)
            worst = {k: (max(v) if v else 0.0) for k, v in classes.items()}
            print(
                f"{style:>8} {args.page} n={args.start}..{args.start + args.pairs}, "
                f"prefetch={not args.no_prefetch}: "
                f"{len(frames)} frames, {len(classes['boundary'])} pair changes, "
                f"{len(classes['move start'])} move starts; "
                f"worst frame at a pair change {worst['boundary']:.1f} ms, "
                f"at a move start {worst['move start']:.1f} ms, "
                f"elsewhere {worst['elsewhere']:.1f} ms; median frame "
                f"{statistics.median(classes['elsewhere']):.1f} ms"
            )
        print("ERRORS:", errors or "none")
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
