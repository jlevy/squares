#!/usr/bin/env python3
"""Drive the workbench through the steps that have broken, and hold them to the contract.

`transition_contract` says what a step may look like; this runs the page, samples every frame
of each declared step through `probes/transitions/sweep.js`, and applies it. The steps are the
ones that shipped a fault, chosen so a regression of any of them is caught where it happened:

- 8, 9 and 10: grid fills, where the whole packing once flashed olive, and where the new
  square crossed from scarlet in two frames while its neighbors snapped a shade darker.
- 11: the step into a non-integer side, where the view once shrank and grew, and a square
  came back from grey in its old hue before turning to its new one.
- 49 to 53: matched steps, where the arriving square's red once vanished and a crossing
  thrashed red, green, red.
- 96 to 102: a run of grid fills, including a crossing from one room to the next.

Consecutive steps are also checked across their boundary, since a view that is smooth inside
each step can still jump between them.

`check_frontend` runs the declared steps on every pull request, in about five seconds.
`--all` runs every step in the corpus, and `--trace N --square ID` prints one square through
one step, frame by frame, with the schedule it ran on.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev squares-workbench-check-transitions
    uv run --frozen --all-extras --group dev squares-workbench-check-transitions --all
    uv run --frozen --all-extras --group dev squares-workbench-check-transitions \\
        --trace 11 --square 5
"""

from __future__ import annotations

import argparse
import os
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from itertools import pairwise
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright

from workbench_tools.browser_page import open_page
from workbench_tools.probes import probe
from workbench_tools.transition_contract import (
    Finding,
    boundary_jerk,
    box_growth,
    chroma_bumps,
    hue_turns,
    lightness_jumps,
    merge_window,
    oklch,
    red_frames,
    still_recolors,
    summarize,
    third_hues,
    unsampled,
    view_jerks,
)

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
PAGE = PACKAGE_ROOT.parents[1] / "packing" / "site" / "workbench" / "index.html"

#: The steps that have broken, by the n they go into. See the module docstring for which fault
#: each one carried.
STEPS = (8, 9, 10, 11, 49, 50, 51, 52, 53, 96, 97, 98, 99, 100, 101, 102)

#: The rate the steps are sampled at: the rate the videos are cut at.
FPS = 60

#: How many frames the arriving square must be opaque and saturated scarlet. Two: a grid fill
#: at the speed-up is a few dozen frames at 60 fps, and one frame of red is a flicker rather
#: than a square arriving.
MIN_RED_FRAMES = 2

#: The kinds of pair on which nothing rearranges, as `pairs()` reports them.
STILL_KINDS = frozenset({"prefix", "shared-picture"})


def arriving_identity(sweep: dict[str, Any]) -> int:
    """The square that is drawn at the step's end and was not at its start."""
    first = {int(row[0]) for row in sweep["frames"][0]["squares"]}
    last = {int(row[0]) for row in sweep["frames"][-1]["squares"]}
    new = last - first
    return max(new) if new else max(last)


def judge(sweep: dict[str, Any], *, still: bool) -> tuple[list[Finding], int]:
    """Every finding one step produces, and how many frames its new square is red."""
    n = int(sweep["n"])
    frames = sweep["frames"]
    arriving = arriving_identity(sweep)
    findings = [
        *unsampled(n, frames),
        *third_hues(n, frames),
        *hue_turns(n, frames),
        *lightness_jumps(
            n,
            frames,
            arriving,
            None if still else merge_window(sweep["schedule"], sweep["fade"]),
        ),
        *chroma_bumps(n, frames),
        *view_jerks(n, [float(f["view"]) for f in frames]),
        *box_growth(
            n,
            [float(f["box"]) for f in frames],
            [float(f["t"]) for f in frames],
            float(sweep["moveStart"]),
        ),
    ]
    if still:
        findings.extend(still_recolors(n, frames, arriving))
    red = red_frames(frames, arriving)
    if red < MIN_RED_FRAMES:
        findings.append(
            Finding(
                "arriving square not red",
                n,
                0,
                f"square {arriving} is saturated scarlet in {red} frames, "
                f"fewer than {MIN_RED_FRAMES}",
            )
        )
    return findings, red


@contextmanager
def _opened(page_path: Path) -> Iterator[Any]:
    """The built page in headless Chromium at the stage's size, fonts loaded."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True, executable_path=os.environ.get("SQUARES_BROWSER_EXECUTABLE")
        )
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        open_page(page, page_path, wait_until="load")
        page.evaluate(probe("capture/fonts-ready"))
        try:
            yield page
        finally:
            browser.close()


def sweep_steps(page: Any, steps: Sequence[int] | None) -> list[tuple[dict[str, Any], bool]]:
    """Sample each step, with whether it is a still pair; None samples every step."""
    pairs = page.evaluate(probe("capture/control"), {"read": ["pairs"]})["pairs"]
    kind = {int(p["n"]) + 1: str(p["kind"]) for p in pairs}
    out = []
    for n in sorted(kind) if steps is None else steps:
        sweep = page.evaluate(
            probe("transitions/sweep"),
            {"n": n, "fps": FPS, "style": "physics", "anneal": 9, "hold": False},
        )
        out.append((sweep, kind.get(n) in STILL_KINDS))
    return out


def measure(page_path: Path, steps: Sequence[int] | None = STEPS) -> tuple[str, list[Finding]]:
    """Run the contract over `steps`, or every step if None; return a summary and findings."""
    with _opened(page_path) as page:
        sweeps = sweep_steps(page, steps)
    findings: list[Finding] = []
    reds: list[int] = []
    for sweep, still in sweeps:
        found, red = judge(sweep, still=still)
        findings.extend(found)
        reds.append(red)
    for (left, _), (right, _) in pairwise(sweeps):
        if int(right["n"]) == int(left["n"]) + 1:
            findings.extend(
                boundary_jerk(
                    int(right["n"]),
                    float(left["frames"][-1]["view"]),
                    float(right["frames"][0]["view"]),
                )
            )
    frames = sum(len(sweep["frames"]) for sweep, _ in sweeps)
    summary = (
        f"{len(sweeps)} steps, {frames} frames at {FPS} fps; the new square is red in "
        f"{min(reds)} to {max(reds)} frames"
    )
    return summary, findings


def check(page_path: Path) -> str:
    """The declared steps, as `check_frontend` runs them; raise with every finding if any."""
    summary, findings = measure(page_path)
    if findings:
        raise ValueError(
            f"transition contract: {len(findings)} findings -- {summarize(findings)}\n  "
            + "\n  ".join(str(finding) for finding in findings)
        )
    return f"transitions: {summary}"


def trace(page_path: Path, n: int, identity: int | None) -> list[str]:
    """One step, frame by frame: the view, the box, and one square's fill as OKLCH.

    `identity` None traces the arriving square.
    """
    with _opened(page_path) as page:
        (sweep, _), *_ = sweep_steps(page, [n])
    who = arriving_identity(sweep) if identity is None else identity
    timing = ", ".join(f"{k} {float(v):.3f}" for k, v in sweep["schedule"].items())
    fade = ", ".join(f"{k} {float(v):.2f}" for k, v in sweep["fade"].items())
    lines = [f"step into {n}, square {who}", f"  schedule: {timing}", f"  color fade: {fade}"]
    for index, frame in enumerate(sweep["frames"]):
        fill = next((row[1] for row in frame["squares"] if int(row[0]) == who), "")
        opacity = next((row[2] for row in frame["squares"] if int(row[0]) == who), 0)
        color = ""
        if fill:
            lightness, chroma, hue = oklch(str(fill))
            color = f"{fill} L{lightness:.3f} C{chroma:.3f} h{hue:5.1f} op{float(opacity):.2f}"
        lines.append(
            f"{index:4d} t{float(frame['t']):6.3f} view {float(frame['view']):.4f} "
            f"box {float(frame['box']):.4f} ink {float(frame['boxInk']):.2f}  {color}"
        )
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--page", type=Path, default=PAGE, help="the built workbench page")
    scope = ap.add_mutually_exclusive_group()
    scope.add_argument("--steps", type=int, nargs="+", default=list(STEPS))
    scope.add_argument("--all", action="store_true", help="every step in the corpus")
    ap.add_argument("--verbose", action="store_true", help="print every finding")
    ap.add_argument("--trace", type=int, metavar="N", help="print one step frame by frame")
    ap.add_argument("--square", type=int, help="with --trace: the identity to follow")
    o = ap.parse_args()
    if not o.page.exists():
        raise SystemExit(f"{o.page} is not built: run `squares-workbench-build` first")
    if o.trace is not None:
        print("\n".join(trace(o.page, o.trace, o.square)))
        return 0
    summary, findings = measure(o.page, None if o.all else o.steps)
    print(summary)
    if not findings:
        print("OK: every step keeps the transition contract")
        return 0
    print(f"FAIL: {len(findings)} findings -- {summarize(findings)}")
    for finding in findings if o.verbose else findings[:12]:
        print(f"  {finding}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
