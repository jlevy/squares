"""Measure how Animate introduces a step's new square, from the drawn stage.

    uv run --frozen --all-extras --group dev python -m workbench_tools.arrival_frames \\
        [--page PATH] [--json PATH] [--frames DIR]

Each case configures one step (its n, style, phase, beat and simple-transition speed-up)
and seeks the built page through it at 60 Hz and at every instant of its schedule. From
the drawn stage it reports when the picture shrinks (the view growing to hold the
bigger container) and when the box grows, when the new square first shows and when it
is fully in, the gap between the end of that growth and the first visible frame, the
scales the square was drawn at while visible, and the largest opacity change between
60 Hz samples. The order and gap are read from frames rather than from the schedule,
so a renderer that disagrees with its schedule is caught.

`--frames DIR` also writes PNG stills of the stage at the schedule's instants, and a strip
of them side by side, for the default step and the step into 10, for review.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import Any

from PIL import Image
from playwright.sync_api import Page, sync_playwright

from workbench_tools.browser_page import open_page
from workbench_tools.probes import probe

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
REPO = PACKAGE_ROOT.parents[1]
PAGE = REPO / "packing/site/workbench/index.html"

#: Samples per second of the step's own clock, the rate a viewer's display draws at.
RATE = 60
#: How far apart two drawn sizes or opacities must be to count as a change.
TOLERANCE = 1e-9
#: The height of one still in the review strip, in pixels.
STRIP_HEIGHT = 320


@dataclass(frozen=True)
class Case:
    """One step as the page plays it."""

    label: str
    n: int = 11
    style: str = "tween"
    phase: str = "add-then-move"
    continuous: bool = True
    fast_simple: bool = True


#: The default is what pressing play in Animate shows: the continuous beat, style A, add then
#: move, with simple transitions sped up. The rest vary one thing at a time. The step into 11
#: rearranges and grows its container; into 7 is a simple grid fill; into 10 changes the
#: container without rearranging.
CASES = (
    Case("default: continuous tween into 11"),
    Case("single-step tween into 11", continuous=False),
    Case("continuous physics into 11", style="physics"),
    Case("continuous bodies into 11", style="bodies"),
    Case("move-then-add tween into 11", phase="move-then-add"),
    Case("simultaneous tween into 11", phase="simultaneous"),
    Case("simple into 7, fastSimple on", n=7),
    Case("simple into 7, fastSimple off", n=7, fast_simple=False),
    Case("physics simple into 7", n=7, style="physics"),
    Case("container step into 10", n=10),
    Case("container step into 10, physics", n=10, style="physics"),
)


def _first(
    samples: list[list[float]], predicate: Any, after: float = -math.inf
) -> float | None:
    for sample in samples:
        if sample[0] >= after and predicate(sample):
            return sample[0]
    return None


def _growth(moving: list[list[float]], column: int) -> dict[str, float] | None:
    """When one drawn size first grows past its resting value in the move, peaks, and settles.

    A physical container breathes: it opens past its target and shuts again, so the size can
    peak before it settles. The resize is over when it settles, which is what the gap is from.
    """
    if not moving:
        return None
    resting = moving[0][column]
    peak = max(sample[column] for sample in moving)
    if peak <= resting + TOLERANCE:
        return None
    began = _first(moving, lambda s: s[column] > resting + TOLERANCE)
    peaked = _first(moving, lambda s: s[column] >= peak - TOLERANCE)
    if began is None or peaked is None:
        return None
    # The last instant still at the resting size is where the growth starts, and the first
    # instant from which the size no longer changes is where it settles.
    still = [sample[0] for sample in moving if sample[0] < began]
    final = moving[-1][column]
    settled = moving[-1][0]
    for sample in reversed(moving):
        if abs(sample[column] - final) > TOLERANCE:
            break
        settled = sample[0]
    return {
        "start": still[-1] if still else began,
        "peak": peaked,
        "end": settled,
        "from": resting,
        "to": peak,
        "final": final,
    }


def summarise(trace: dict[str, Any]) -> dict[str, Any]:
    """The shrink, the arrival and the gap between them, from one case's samples."""
    samples: list[list[float]] = trace["samples"]
    schedule = trace["schedule"]
    # The move, not the settle, where the box contracts and a physical view refits.
    moving = [s for s in samples if schedule["moveStart"] <= s[0] < schedule["moveEnd"]]
    view = _growth(moving, 4)
    box = _growth(moving, 5)
    ends = [growth["end"] for growth in (view, box) if growth is not None]
    appear = _first(samples, lambda s: s[1] > TOLERANCE)
    full = (
        None
        if appear is None
        else _first(samples, lambda s: s[1] >= 1 - TOLERANCE, after=appear)
    )
    visible = [s for s in samples if s[1] > TOLERANCE]
    uniform = [s for s in samples if abs(s[0] * RATE - round(s[0] * RATE)) < 1e-6]
    steps = [abs(b[1] - a[1]) for a, b in pairwise(uniform)]
    return {
        "viewGrows": view,
        "boxGrows": box,
        "shrinkEnd": max(ends) if ends else None,
        "appear": appear,
        "full": full,
        "gapAfterShrink": None if not ends or appear is None else appear - max(ends),
        "scaleWhileVisible": (
            [min(s[2] for s in visible), max(s[2] for s in visible)] if visible else None
        ),
        "opacityAtFirstVisible": visible[0][1] if visible else None,
        "largestOpacityStepAt60Hz": max(steps, default=0.0),
    }


def trace_case(page: Page, case: Case) -> dict[str, Any]:
    """Configure one case on the page and sample it."""
    duration = float(
        page.evaluate(
            probe("animate/arrival-trace"),
            {
                "n": case.n,
                "style": case.style,
                "phase": case.phase,
                "continuous": case.continuous,
                "fastSimple": case.fast_simple,
                "times": [],
            },
        )["duration"]
    )
    count = math.floor(duration * RATE + TOLERANCE)
    times = [k / RATE / duration for k in range(count + 1)] if duration > 0 else [0.0]
    return page.evaluate(
        probe("animate/arrival-trace"),
        {
            "n": case.n,
            "style": case.style,
            "phase": case.phase,
            "continuous": case.continuous,
            "fastSimple": case.fast_simple,
            "times": [*times, 1.0],
        },
    )


def _seconds(value: float | None) -> str:
    return "none" if value is None else f"{value:.3f} s"


def _growth_text(growth: dict[str, float] | None) -> str:
    if growth is None:
        return "none"
    return (
        f"from {growth['start']:.3f} s, peak {growth['to']:.4f} at {growth['peak']:.3f} s, "
        f"settled at {growth['final']:.4f} by {growth['end']:.3f} s (from {growth['from']:.4f})"
    )


def report(case: Case, trace: dict[str, Any], summary: dict[str, Any]) -> str:
    """One case as readable lines."""
    schedule = trace["schedule"]
    lines = [
        (
            f"{case.label} (kind {trace['kind']}, style {case.style}, phase {case.phase}, "
            f"continuous {case.continuous}, fastSimple {case.fast_simple})"
        ),
        "  schedule: "
        + ", ".join(f"{key} {value:.3f}" for key, value in schedule.items())
        + f", duration {trace['duration']:.3f}",
        f"  view grows (the picture shrinks): {_growth_text(summary['viewGrows'])}",
        f"  box grows: {_growth_text(summary['boxGrows'])}",
        (
            f"  new square: first visible {_seconds(summary['appear'])}"
            f" (opacity {summary['opacityAtFirstVisible']}), "
            f"fully in {_seconds(summary['full'])}"
        ),
        (
            "  gap from the end of the shrink and box growth to first visible: "
            f"{_seconds(summary['gapAfterShrink'])}"
        ),
        f"  scale while visible: {summary['scaleWhileVisible']}",
        (
            "  largest opacity step between 60 Hz samples: "
            f"{summary['largestOpacityStepAt60Hz']:.4f}"
        ),
    ]
    return "\n".join(lines)


#: The cases `--frames` draws, each into its own directory: the default step, whose box grows
#: without the view changing, and the step into 10, where the whole picture visibly shrinks.
FRAME_CASES = {"default-into-11": CASES[0], "container-into-10": CASES[9]}


def stills(page: Page, trace: dict[str, Any], directory: Path) -> list[Path]:
    """PNG stills of the stage at the schedule's instants, and a strip of them.

    A page built before the schedule named its resize has no `containerStart`; its stills are
    taken at the arrival's instants alone.
    """
    directory.mkdir(parents=True, exist_ok=True)
    schedule = trace["schedule"]
    summary = summarise(trace)
    resize = (
        (
            schedule["containerStart"],
            (schedule["containerStart"] + schedule["containerEnd"]) / 2,
            schedule["containerEnd"],
        )
        if "containerStart" in schedule
        else ()
    )
    growth = [g["end"] for g in (summary["viewGrows"], summary["boxGrows"]) if g is not None]
    instants = sorted(
        {
            round(value, 4)
            for value in (
                schedule["moveStart"],
                *resize,
                *growth,
                schedule["arrive"],
                (schedule["arrive"] + schedule["arrived"]) / 2,
                schedule["arrived"],
                trace["duration"],
                *(v for v in (summary["appear"],) if v is not None),
            )
        }
    )
    stage = page.locator("#packing-svg")
    written: list[Path] = []
    for index, seconds in enumerate(instants):
        page.evaluate(probe("candidate/seek"), {"t": seconds})
        path = directory / f"still-{index:02d}-{seconds:06.3f}s.png"
        stage.screenshot(path=str(path))
        written.append(path)
    images = [Image.open(path) for path in written]
    scaled = [
        image.resize((round(image.width * STRIP_HEIGHT / image.height), STRIP_HEIGHT))
        for image in images
    ]
    strip = Image.new("RGB", (sum(image.width for image in scaled), STRIP_HEIGHT), "white")
    offset = 0
    for image in scaled:
        strip.paste(image, (offset, 0))
        offset += image.width
    path = directory / "strip.png"
    strip.save(path)
    written.append(path)
    return written


def main() -> int:
    """Measure every case on a built page and print the order each one draws."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", type=Path, default=PAGE, help="a built index.html")
    parser.add_argument("--json", type=Path, help="also write every sample and summary here")
    parser.add_argument(
        "--frames", type=Path, help="write stills of the default and the step into 10 here"
    )
    args = parser.parse_args()
    errors: list[str] = []
    results: list[dict[str, Any]] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True, executable_path=os.environ.get("SQUARES_BROWSER_EXECUTABLE")
        )
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.on("pageerror", lambda error: errors.append(str(error)))
        open_page(page, args.page)
        page.evaluate(probe("capture/fonts-ready"))
        page.evaluate(probe("capture/control"), {"prepare": True, "capture": True})
        for case in CASES:
            trace = trace_case(page, case)
            summary = summarise(trace)
            print(report(case, trace, summary))
            results.append({"case": case.__dict__, "trace": trace, "summary": summary})
        if args.frames is not None:
            for slug, case in FRAME_CASES.items():
                trace = trace_case(page, case)
                for path in stills(page, trace, args.frames / slug):
                    print(f"wrote {path}")
        browser.close()
    if args.json is not None:
        args.json.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    if errors:
        print("page errors:", errors)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
