#!/usr/bin/env python3
"""Capture the workbench's animation to a video file, with a receipt for what it shows.

The end product is a file the owner can upload. Frames come from the built workbench page
driven in a headless browser through the page's own clock, so a captured frame is the frame
the page draws at that instant rather than a second rendering that happens to agree -- which
is what makes "the video matches the workbench" a fact rather than a hope.

**The clock is the one the page plays a range on.** A range plays under continuous play, and
continuous play prices each step by its own beat: a static append is shorter than a matched
pair. So the capture puts the page on that beat before it asks how long a step lasts, and
checks the steps add up to the page's own duration for the range. The frames are one clock
over the whole range, each instant sampled once, so a step boundary is one frame rather than
a step's end and the next step's start drawing the same picture twice, and the video lasts
the range's duration to the nearest frame.

Capture preview is on for every frame: the controls and everything else that explains the
page are hidden, so nothing that is scaffolding survives into the file. Nothing is drawn on
the frames to say what they are either -- the owner removed the page's kind tag, and the
capture does not put one back. The stage is 1920x1080 in its own coordinates, so a 1080p
capture is one page pixel per video pixel and 4K is the same page at a device scale of two.

**The receipt is not optional.** A video of a packing search is a claim about what was
reached, and a file on its own cannot be checked. The receipt written beside it, after the
video is in place, names the page it came from by digest (taken before the page is loaded),
the commit and whether the tree was dirty, the Playwright, browser and ffmpeg versions, the
encoder's arguments, the range and the frame rate, and, per step, the record the step was
aiming at and whether it actually landed on it. It states `transitions_are_packings: false`
and `intermediate_frames: illustrative-tween`, with the reason: the frames between checked
records are tweens, not packings. The MP4's own `comment` metadata says the same, with the
shared version and the page digest, for anyone who has the video without the receipt.

**Citations are a setting of the cut** (think-jwly). `--citations` turns on the stage's CITATION
section, which names where each bound comes from; the receipt says whether it was on, the
sha256 of the citation file the page was built from, and the shared version the stage draws,
all read from the page itself. A page built without a citation file has nothing to cite, so a
cut that asks for citations from one is refused rather than cut plain under a cited name.

**The grid-fill speed-up is a setting of the cut too** (think-gr3j). A step that only fills the
last row of an axis-aligned grid plays sped up, and how much faster is the page's own factor,
which `--simple-speed` overrides. The cut always states it, so the receipt's `simple_speed`
names the clock the step lengths below it were measured on; a factor the page declines -- one
outside its control's range -- is refused rather than cut at whatever the page settled for.

What this does NOT yet do is play a PackingStrategy document: the workbench animates the
retained corpus, and the strategy documents `workbench_tools.ascent`
(`squares-workbench-ascent`) writes reach the renderer by the SVG path instead. Wiring the two
together is `think-883t`, and until it lands the receipt names records rather than strategy
documents.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m workbench_tools.capture_video --to 24
    uv run --frozen --all-extras --group dev python -m workbench_tools.capture_video \
        --from 2 --to 100 --profile social --out site/workbench/ascent-excerpt.mp4
    uv run --frozen --all-extras --group dev python -m workbench_tools.capture_video \
        --from 100 --to 110 --fps 30 --height 2160 --out site/workbench/ascent-4k.mp4
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import re
import shutil
import subprocess
import tempfile
import time
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass
from itertools import accumulate
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from workbench_tools.browser_page import open_page
from workbench_tools.delivery import (
    DEFAULT_PROFILE,
    FRAME_PATTERN,
    PROFILES,
    DeliveredVideo,
    DeliveryProfile,
    conformance,
    encode_arguments,
    measure,
    report,
)
from workbench_tools.probes import probe

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
REPO = PACKAGE_ROOT.parents[1]
PACKING = REPO / "packing"
PAGE = PACKING / "site/workbench/index.html"

#: The stage's own coordinates. Every capture is this shape, scaled: the page lays itself out
#: in these units and a capture that changed the aspect would be cropping the poster, not
#: resizing it.
STAGE_WIDTH = 1920
STAGE_HEIGHT = 1080

#: What `--height` may ask for. A device scale below one resamples the page down and blurs the
#: 28 px type the panel is built around, which is the whole reason the type scale has a floor.
HEIGHTS = {1080: 1, 2160: 2}

#: Plan D9's statement of what a frame between two records is.
INTERMEDIATE_FRAMES = "illustrative-tween"

#: How far the priced steps may drift from the page's own figure for the range, in seconds.
BEAT_TOLERANCE = 1e-9

TRANSITIONS_REASON = (
    "Intermediate frames are illustrative tweens between checked records, not packings: only "
    "a step's settled end is a record, and steps_off_record names any step whose end did not "
    "land on one."
)
ANIMATION_TRANSITIONS_REASON = (
    "Frames between the animation document's own frames are illustrative tweens, not "
    "packings; the document's frames carry their own checks."
)

Runner = Callable[..., subprocess.CompletedProcess[str]]

#: The page's data block, as `tools/check-candidate-corpus.ts` finds it.
DATA_BLOCK = re.compile(
    r'<script\s+id="atlas-data"\s+type="application/json"(?P<attrs>[^>]*)>(?P<data>.*?)</script>',
    re.DOTALL,
)


@dataclass(frozen=True, slots=True)
class PageEdition:
    """What a built page says about the data it draws: the shared version on its stage, and the
    sha256 of the citation file its CITATION section was built from, or None without one."""

    version: str
    citations_sha256: str | None


def page_edition(page: str, *, page_path: Path | None = None) -> PageEdition:
    """The edition a page's own data states, read from its text rather than asked of a browser,
    so the receipt names what the bytes it digested carry."""
    blocks = list(DATA_BLOCK.finditer(page))
    if len(blocks) != 1:
        raise SystemExit(f"the page has {len(blocks)} data blocks, not one")
    # The builder writes `</` as `<\/`, which JSON reads as the same two characters.
    block = blocks[0]
    linked = re.search(r'data-src="([^"]+)"', block.group("attrs"))
    if linked:
        name = linked.group(1)
        digest = re.fullmatch(r"data/corpus\.([0-9a-f]{16})\.json", name)
        if page_path is None or digest is None:
            raise SystemExit("a linked corpus needs the page path and a local hashed data URL")
        payload = (page_path.parent / name).read_bytes()
        if hashlib.sha256(payload).hexdigest()[:16] != digest.group(1):
            raise SystemExit("the linked corpus does not match its content-addressed name")
        data = json.loads(payload)
    else:
        data = json.loads(block.group("data"))
    citations = data.get("citations") or {}
    version = data.get("version")
    if not isinstance(version, str):
        raise SystemExit("the page carries no shared version: rebuild it")
    return PageEdition(version=version, citations_sha256=citations.get("sha256"))


def citation_commands(*, citations: bool, edition: PageEdition) -> list[list[Any]]:
    """The command that sets the CITATION section for the cut, after the baseline turned it off.

    Refused where the cut asks for citations the page does not carry: its frames would be the
    plain cut's, with a receipt saying they were cited.
    """
    if citations and edition.citations_sha256 is None:
        raise SystemExit(
            "--citations asks for the CITATION section, and this page was built without a "
            "citation file: build it with packing/atlas/known-best/bound-citations.json present"
        )
    return [["setCitations", citations]]


def simple_speed_commands(requested: float | None, opened: dict[str, Any]) -> list[list[Any]]:
    """The command that states the factor the cut's grid fills play at.

    A cut states its clock rather than inheriting one: the command goes in whether or not
    `--simple-speed` was given, so the receipt's figure is a setting of the capture and the page
    is put on it in the same browser turn as the range. Without the option the factor is the
    page's own, read from the page rather than written here, so the default keeps one spelling.

    The page clamps what it is handed and snaps it to its control's step, so what this asks for
    is checked against what the page reports before a frame is drawn.
    """
    speed = float(opened["simpleSpeed"]) if requested is None else float(requested)
    return [["setSimpleSpeed", speed]]


@dataclass(frozen=True, slots=True)
class FrameSample:
    """One frame of the video: its number, the step it belongs to, and the step's clock."""

    index: int
    step: int
    at: float


@dataclass(frozen=True, slots=True)
class Provenance:
    """What produced a capture, beyond the page: plan D9's commit and tool versions."""

    commit: str | None
    dirty: bool | None
    playwright_version: str
    browser_version: str
    ffmpeg_version: str


def _control(
    page: Any,
    *,
    commands: list[list[Any]] | None = None,
    read: list[str] | None = None,
    prepare: bool = False,
) -> dict[str, Any]:
    """Drive and inspect the page through the strict capture controller."""
    request: dict[str, Any] = {}
    if commands:
        request["commands"] = commands
    if read:
        request["read"] = read
    if prepare:
        request.update({"prepare": True, "capture": True})
    return page.evaluate(probe("capture/control"), request)


def _encoder() -> str:
    """The ffmpeg to encode with, or an error saying how to get one."""
    found = shutil.which("ffmpeg")
    if found is None:
        raise SystemExit(
            "no ffmpeg on PATH: install one (`brew install ffmpeg`) or put it on PATH. "
            "The frames are captured either way; only the encode step needs it."
        )
    return found


def animation_defaults(state: dict[str, Any]) -> list[list[Any]]:
    """The commands that put the page's own animation character back after `prepare()`.

    `prepare()` is the capture tools' shared baseline and it reduces two settings for a
    checker's benefit: a fixed `tween` style and a shake of 3, so that a still or a contract
    test is cheap and repeatable. A video is the other kind of product -- it is meant to show
    what the page shows anyone who opens it -- and for these two the difference is the whole
    character of the motion. `tween` is a pure block interpolation, and `annealSpan()` returns
    1 under it whatever the level, so the shake does not merely soften: it disappears.

    Taken from the page's own state rather than written down here, because a default written
    in two places is a default that drifts.
    """
    return [
        ["setStyle", state["style"]],
        ["setAnneal", state["anneal"]],
    ]


def pricing_commands(first: int, last: int) -> list[list[Any]]:
    """The commands that put the page on the beat it plays a range at, with the clock stopped.

    Animate is the mode that plays a range and `playRange` is how it plays one: it turns
    continuous play on, which is what prices a static append at its short beat. Pausing in
    the same browser turn stops the clock before a frame of it runs, so the capture seeks
    through the range on that beat rather than watching it play.

    The style and the shake are already set by the time this runs, and they have to be: the
    annealed styles stretch a pair's move and correction by `annealSpan()`, so a range priced
    before them is priced on a clock the page will not play.
    """
    return [["setMode", "animate"], ["setRange", first, last], ["playRange"], ["pause"]]


def price_report(
    steps: list[dict[str, Any]], durations: list[float], earlier: list[dict[str, Any]]
) -> list[str]:
    """How this page prices each kind of step against an earlier capture's receipt.

    A range that got longer between two cuts is a property of some kind of step, and this says
    which: per kind, how many steps, their total then and now, and the largest change in one.
    """
    before = {int(step["n"]): float(step["seconds"]) for step in earlier}
    kinds: dict[str, list[tuple[float, float]]] = {}
    for step, seconds in zip(steps, durations, strict=True):
        n = int(step["n"]) + 1
        if n in before:
            kinds.setdefault(str(step["kind"]), []).append((before[n], seconds))
    lines = []
    for kind, pairs in sorted(kinds.items()):
        then = math.fsum(p[0] for p in pairs)
        now = math.fsum(p[1] for p in pairs)
        widest = max(pairs, key=lambda p: abs(p[1] - p[0]))
        lines.append(
            f"  {kind}: {len(pairs)} steps, {then:.2f} s then, {now:.2f} s now "
            f"({now - then:+.2f}); one step went {widest[0]:.3f} -> {widest[1]:.3f} s"
        )
    total_then = math.fsum(p[0] for pairs in kinds.values() for p in pairs)
    total_now = math.fsum(p[1] for pairs in kinds.values() for p in pairs)
    lines.append(
        f"  all: {total_then:.2f} s then, {total_now:.2f} s now ({total_now - total_then:+.2f})"
    )
    return lines


def price_steps(
    steps: Sequence[dict[str, Any]], durations: Sequence[float], beat: dict[str, Any]
) -> list[float]:
    """The seconds each step lasts, checked against what the page says the range plays.

    `beat` is what `capture/beat` reads: whether continuous play is on, and the page's range.
    Off, a step's duration is the single-step beat, which runs a static append about twice
    as long as the page plays it; and steps that do not add up to the range's own duration
    were priced on some other clock. Either way the video would not be the page.
    """
    if beat.get("continuous") is not True:
        raise SystemExit(
            "the page is not on its continuous beat, so step durations are the single-step "
            "timing rather than what the range plays at"
        )
    span = beat["range"]
    indices = [int(step["index"]) for step in steps]
    if indices != list(range(int(span["first"]), int(span["last"]) + 1)):
        raise SystemExit(
            f"the steps (pairs {indices}) are not the page's range "
            f"(pairs {span['first']} to {span['last']})"
        )
    if len(durations) != len(steps):
        raise SystemExit(f"{len(durations)} durations for {len(steps)} steps")
    if not all(math.isfinite(seconds) and seconds > 0 for seconds in durations):
        raise SystemExit(f"a step's duration is not a positive number of seconds: {durations}")
    total = math.fsum(durations)
    expected = float(span["duration"])
    if not math.isclose(total, expected, rel_tol=BEAT_TOLERANCE, abs_tol=BEAT_TOLERANCE):
        raise SystemExit(
            f"the steps price to {total} s but the page's range plays in {expected} s"
        )
    return list(durations)


def frame_schedule(durations: Sequence[float], fps: int) -> tuple[FrameSample, ...]:
    """Which instant of which step each frame shows, over one clock for the whole run.

    The run is `round(total * fps)` frames, and frame `k` shows the instant at the end of its
    own interval, `total * (k + 1) / count`. So every instant is sampled once, the first
    frame is one frame into the opening dwell, and the last is the settled end of the run. A
    step owns the instants after its start up to and including its end, so a step whose end
    falls on the frame grid ends on its own settled packing.
    """
    if fps <= 0:
        raise ValueError(f"fps must be positive, got {fps}")
    if not durations:
        raise ValueError("a schedule needs at least one step")
    if not all(math.isfinite(seconds) and seconds >= 0 for seconds in durations):
        raise ValueError(f"step durations must be finite and nonnegative, got {durations}")
    ends = list(accumulate(durations))
    total = ends[-1]
    if not total > 0:
        raise ValueError("the steps must last a positive time")
    count = max(1, round(total * fps))
    last_step = len(durations) - 1
    samples: list[FrameSample] = []
    step = 0
    for index in range(count):
        at_run = total if index == count - 1 else total * (index + 1) / count
        while step < last_step and at_run > ends[step]:
            step += 1
        if at_run >= ends[step]:
            at = float(durations[step])
        else:
            at = min(float(durations[step]), max(0.0, at_run - (ends[step] - durations[step])))
        samples.append(FrameSample(index=index, step=step, at=at))
    return tuple(samples)


def frames_per_step(schedule: Sequence[FrameSample], steps: int) -> list[int]:
    """How many of the schedule's frames each step owns."""
    counts = [0] * steps
    for sample in schedule:
        counts[sample.step] += 1
    return counts


def _steps(page: Any, first: int, last: int) -> list[dict[str, Any]]:
    """The pairs the range covers, as the page reports them.

    A pair is named by the n it steps *into*, which is how the workbench's own range control
    reads, so `--from 2 --to 24` is the ascent that ends with the 24-square packing.
    """
    pairs = _control(page, read=["pairs"])["pairs"]
    chosen = [p for p in pairs if first <= p["n"] + 1 <= last]
    if not chosen:
        have = f"{pairs[0]['n'] + 1} to {pairs[-1]['n'] + 1}"
        raise SystemExit(f"no steps in {first}..{last}: the page carries {have}")
    return chosen


def _price(page: Any, steps: list[dict[str, Any]]) -> list[float]:
    """Each step's duration on the continuous beat, read from the page and checked."""
    durations = [
        float(
            _control(page, commands=[["select", step["index"]]], read=["duration"])["duration"]
        )
        for step in steps
    ]
    return price_steps(steps, durations, page.evaluate(probe("capture/beat")))


def priced_range(
    page_path: Path,
    first: int,
    last: int,
    fps: int,
    *,
    citations: bool = False,
    simple_speed: float | None = None,
) -> list[dict[str, Any]]:
    """The steps a capture of `first..last` makes and the frames each gets, without capturing.

    Priced from the page exactly as `main` prices a capture, through the same defaults, the
    same commands and the same frame schedule, so a check can place any frame of a cut that has
    no receipt -- one the profile refused -- in its step. `citations` is the cut's setting,
    which changes what a frame draws and not when; `simple_speed` changes when, so a caller that
    prices a cut made at another factor has to say so.
    """
    from playwright.sync_api import sync_playwright  # noqa: PLC0415  (optional dev dependency)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": STAGE_WIDTH, "height": STAGE_HEIGHT})
        open_page(page, page_path)
        page.evaluate(probe("capture/fonts-ready"))
        opened = _control(page, commands=[["setMode", "animate"]], read=["state"])["state"]
        _control(
            page,
            prepare=True,
            commands=[
                *animation_defaults(opened),
                ["setCitations", citations],
                *simple_speed_commands(simple_speed, opened),
                *pricing_commands(first, last),
            ],
        )
        steps = _steps(page, first, last)
        durations = _price(page, steps)
        browser.close()
    counts = [0] * len(steps)
    for sample in frame_schedule(durations, fps):
        counts[sample.step] += 1
    return [
        {"n": int(step["n"]) + 1, "kind": str(step["kind"]), "frames": count}
        for step, count in zip(steps, counts, strict=True)
    ]


def render_frames(
    page_path: Path,
    first: int,
    last: int,
    fps: int,
    indices: Sequence[int],
    *,
    citations: bool = False,
    simple_speed: float | None = None,
) -> dict[int, bytes]:
    """Draw the named frames of a capture of `first..last` again, as PNG bytes, from the page.

    Each is drawn exactly as `_capture` draws it -- the same defaults and preparation, citations
    as the cut had them, the step selected, the page seeked to the frame's own instant from
    `frame_schedule` -- so a kept frame that differs from its re-render was not the page's frame
    at that instant.
    """
    from playwright.sync_api import sync_playwright  # noqa: PLC0415  (optional dev dependency)

    wanted = set(indices)
    drawn: dict[int, bytes] = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": STAGE_WIDTH, "height": STAGE_HEIGHT})
        open_page(page, page_path)
        page.evaluate(probe("capture/fonts-ready"))
        opened = _control(page, commands=[["setMode", "animate"]], read=["state"])["state"]
        _control(
            page,
            prepare=True,
            commands=[
                *animation_defaults(opened),
                ["setCitations", citations],
                *simple_speed_commands(simple_speed, opened),
                *pricing_commands(first, last),
            ],
        )
        steps = _steps(page, first, last)
        for sample in frame_schedule(_price(page, steps), fps):
            if sample.index not in wanted:
                continue
            _control(page, commands=[["select", steps[sample.step]["index"]]])
            _control(page, commands=[["seek", sample.at]])
            drawn[sample.index] = page.screenshot(type="png")
        browser.close()
    return drawn


def _capture(
    page: Any,
    steps: list[dict[str, Any]],
    durations: list[float],
    fps: int,
    frames_dir: Path,
) -> list[dict[str, Any]]:
    """Every frame of the range, to numbered PNGs. Returns what each step reached."""
    schedule = frame_schedule(durations, fps)
    owned: list[list[FrameSample]] = [[] for _ in steps]
    for sample in schedule:
        owned[sample.step].append(sample)
    receipt = []
    for step, seconds, samples in zip(steps, durations, owned, strict=True):
        _control(page, commands=[["select", step["index"]]])
        started = time.monotonic()
        for sample in samples:
            _control(page, commands=[["seek", sample.at]])
            page.screenshot(path=str(frames_dir / (FRAME_PATTERN % sample.index)), type="png")
        drawing = time.monotonic() - started
        # The bar holds still through the motion and catches up when the picture settles, so it
        # is asked to redraw at the step's end before it is read: what goes in the receipt is
        # the settled answer, whichever step the boundary frame itself belonged to.
        settled = _control(
            page,
            commands=[["seek", seconds], ["refreshGap"]],
            read=["gap"],
        )
        bar = settled["gap"]
        receipt.append(
            {
                "n": bar["n"],
                "kind": step["kind"],
                "seconds": round(seconds, 4),
                "frames": len(samples),
                "record": bar["record"],
                "reached": bar["side"],
                "landed_on_record": bool(bar["met"]),
                "excess": bar["excess"],
                # What this step cost to draw. A capture is the slowest thing built here -- a
                # screenshot per frame through a real browser -- and it is the first place an
                # algorithm that got slower would show as the film taking twice as long to make.
                # Recorded per step rather than as a total so a step that is slow says which.
                "ms_per_frame": round(1000 * drawing / max(1, len(samples)), 1),
            }
        )
    return receipt


def _capture_animation(
    page: Any,
    source: str,
    fps: int,
    frames_dir: Path,
    defaults: list[list[Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Capture an imported v1 animation at the document's declared duration."""
    imported = _control(
        page,
        prepare=True,
        commands=[*defaults, ["importAnimation", source]],
        read=["animation", "exportAnimation"],
    )
    state = imported["animation"]
    if not state["active"]:
        raise ValueError("the imported animation did not become active")
    document = json.loads(imported["exportAnimation"])
    duration = float(state["durationSeconds"])
    if not 0 < duration < float("inf"):
        raise ValueError(f"animation duration must be positive and finite, got {duration!r}")
    schedule = frame_schedule([duration], fps)
    started = time.monotonic()
    last: dict[str, Any] = state
    for sample in schedule:
        last = _control(
            page,
            commands=[["seekAnimation", sample.at / duration]],
            read=["animation"],
        )["animation"]
        page.screenshot(path=str(frames_dir / (FRAME_PATTERN % sample.index)), type="png")
    drawing = time.monotonic() - started
    return (
        [
            {
                "n": last["n"],
                "seconds": duration,
                "frames": len(schedule),
                "guided": last["guided"],
                "valid": last["valid"],
                "ms_per_frame": round(1000 * drawing / len(schedule), 1),
            }
        ],
        document,
    )


def capture_comment() -> str:
    """Plan D9's statement, which the MP4 carries for anyone holding the video alone."""
    return (
        f"intermediate_frames: {INTERMEDIATE_FRAMES}. Transitions are illustrative, not "
        "packings: frames between checked records are tweens."
    )


def encode_into_place(
    command_for: Callable[[Path], list[str]],
    out: Path,
    *,
    run: Runner = subprocess.run,
) -> list[str]:
    """Encode to a temporary file beside `out` and rename it into place. Returns the command.

    A failed or interrupted encode removes its partial file and leaves whatever was at `out`
    untouched, so the destination only ever holds a whole video.
    """
    with atomic_output_file(out, make_parents=True, tmp_suffix=".partial.mp4") as partial:
        command = command_for(partial)
        try:
            done = run(command, capture_output=True, text=True, check=False)
        except BaseException:
            partial.unlink(missing_ok=True)
            raise
        if done.returncode != 0:
            partial.unlink(missing_ok=True)
            raise SystemExit(f"ffmpeg failed:\n{done.stderr[-2000:]}")
    return command


def ffmpeg_version(banner: str) -> str:
    """The version from `ffmpeg -version`'s first line, without the copyright."""
    first = banner.strip().splitlines()[0] if banner.strip() else ""
    return first.split(" Copyright", 1)[0].strip()


def repository_state(repo: Path) -> tuple[str | None, bool | None]:
    """The commit checked out at `repo` and whether the tree differs from it, if git can say."""
    git = shutil.which("git")
    if git is None:
        return None, None
    head = subprocess.run(
        [git, "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=False
    )
    status = subprocess.run(
        [git, "-C", str(repo), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )
    if head.returncode != 0 or status.returncode != 0:
        return None, None
    return head.stdout.strip(), bool(status.stdout.strip())


def capture_receipt(
    *,
    page: str,
    page_sha256: str,
    video: str,
    video_sha256: str,
    first: int,
    last: int,
    fps: int,
    size: tuple[int, int],
    steps: list[dict[str, Any]],
    provenance: Provenance,
    profile: DeliveryProfile,
    delivered: DeliveredVideo,
    encoder: list[str],
    capture_seconds: float,
    edition: PageEdition,
    citations: bool,
    simple_speed: float | None = None,
    animation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """The receipt written beside a video: what it shows, what made it, and what it is not.

    `edition` is what the page says it draws -- the shared version every frame carries and the
    citation file's digest -- and `citations` whether the cut drew its CITATION section.
    `simple_speed` is the factor the page reported for its grid fills, which is what makes the
    step lengths below reproducible: the same range at another factor is another set of them.
    An animation capture has no catalogue steps to speed up, so it carries no factor.
    """
    frames = sum(int(step["frames"]) for step in steps)
    missed = [step["n"] for step in steps if step.get("landed_on_record") is False]
    drawn = [float(step["ms_per_frame"]) for step in steps]
    worst = max(drawn)
    return {
        "page": page,
        "page_sha256": page_sha256,
        # The data the frames are drawn from, as the page states it, beside the page itself.
        "version": edition.version,
        "citations": citations,
        "citations_sha256": edition.citations_sha256,
        "video": video,
        "video_sha256": video_sha256,
        "range": [first, last],
        **({} if simple_speed is None else {"simple_speed": simple_speed}),
        **(animation or {}),
        "fps": fps,
        "size": list(size),
        "frames": frames,
        "seconds": round(frames / fps, 3),
        "steps_off_record": missed,
        "transitions_are_packings": False,
        # What the file is, beside what it shows: the profile asked for and the stream that
        # came out, so a reader can answer "will this upload" without re-probing the file.
        "profile": profile.name,
        "delivered": asdict(delivered),
        "intermediate_frames": INTERMEDIATE_FRAMES,
        "reason": ANIMATION_TRANSITIONS_REASON if animation else TRANSITIONS_REASON,
        **asdict(provenance),
        # The run's own cost, beside what it produced.
        "capture_seconds": round(capture_seconds, 1),
        "ms_per_frame": {
            "mean": round(sum(drawn) / len(drawn), 1),
            "worst": worst,
            "worst_at_n": steps[drawn.index(worst)]["n"],
        },
        "encoder": encoder,
        "steps": steps,
    }


def write_receipt(path: Path, document: dict[str, Any]) -> None:
    """Write a receipt through a temporary file, so a torn receipt never sits beside a video."""
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--page", type=Path, default=PAGE, help="the built workbench page")
    ap.add_argument("--from", dest="first", type=int, default=2, help="the n to start at")
    ap.add_argument("--to", dest="last", type=int, default=24, help="the n to end on")
    # 60, not 30: the owner compared the two cuts of n = 1..100 and 60 reads better, for
    # 14.9 MB against 11.7 over the same 111.4 s. Twice the frames cost 28 per cent more bytes
    # because the tweens are smooth enough to encode cheaply. It does roughly double the
    # capture, which is a screenshot per frame through a real browser.
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--height", type=int, default=1080, choices=sorted(HEIGHTS))
    ap.add_argument(
        "--animation",
        type=Path,
        help="capture this PackingAnimation/v1 document instead of the retained catalogue",
    )
    ap.add_argument(
        "--profile",
        default=DEFAULT_PROFILE,
        choices=sorted(PROFILES),
        help=(
            "the delivery profile the file is encoded to and then checked against; "
            "`social` adds the ceilings an X post imposes"
        ),
    )
    ap.add_argument(
        "--citations",
        action="store_true",
        help="draw the CITATION section under PROVEN, which names each bound's source",
    )
    ap.add_argument(
        "--simple-speed",
        type=float,
        default=None,
        help=(
            "how many times faster the grid fills play; the page's own setting by default, "
            "and refused where the page will not take the factor asked for"
        ),
    )
    ap.add_argument("--out", type=Path, default=PACKING / "site/workbench/ascent.mp4")
    ap.add_argument("--keep-frames", action="store_true", help="leave the PNGs for inspection")
    ap.add_argument(
        "--price-against",
        type=Path,
        metavar="RECEIPT",
        help="price the range, compare each kind of step with an earlier receipt, and stop",
    )
    o = ap.parse_args()

    if not o.page.exists():
        raise SystemExit(f"{o.page} is not built: run `squares-workbench-build` first")
    profile = PROFILES[o.profile]
    ffmpeg = _encoder()
    scale = HEIGHTS[o.height]
    started_all = time.monotonic()
    # Digested before it is loaded, so the receipt names the page the frames came from rather
    # than whatever sits at that path once the capture is over.
    page_sha256 = _digest(o.page)
    edition = page_edition(o.page.read_text(encoding="utf-8"), page_path=o.page)
    if o.citations and o.animation is not None:
        raise SystemExit(
            "--citations draws the catalogue's CITATION section, not an animation's"
        )
    if o.simple_speed is not None and o.animation is not None:
        raise SystemExit(
            "--simple-speed sets the catalogue's grid-fill clock; an animation document "
            "carries its own frame times"
        )
    cited = citation_commands(citations=o.citations, edition=edition)
    commit, dirty = repository_state(REPO)
    banner = subprocess.run([ffmpeg, "-version"], capture_output=True, text=True, check=False)

    from playwright.sync_api import sync_playwright  # noqa: PLC0415  (optional dev dependency)

    holder = Path(tempfile.mkdtemp(prefix="capture-video-"))
    frames_dir = holder / "frames"
    frames_dir.mkdir()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            browser_version = browser.version
            page = browser.new_page(
                viewport={"width": STAGE_WIDTH, "height": STAGE_HEIGHT},
                device_scale_factor=scale,
            )
            open_page(page, o.page)
            page.evaluate(probe("capture/fonts-ready"))
            # The page's own defaults, read before `prepare` reduces them. `atlasTransitions`
            # answers only while the catalogue owns the page, so Animate is entered first.
            opened = _control(page, commands=[["setMode", "animate"]], read=["state"])["state"]
            defaults = animation_defaults(opened)
            # Capture preview, applied by `prepare`, is what hides the chrome.
            if o.animation is None:
                sped = simple_speed_commands(o.simple_speed, opened)
                prepared = _control(
                    page,
                    prepare=True,
                    commands=[*defaults, *cited, *sped, *pricing_commands(o.first, o.last)],
                    read=["state"],
                )
                # What the receipt says is what the page reports, not what was asked of it.
                if prepared["state"]["citations"] is not o.citations:
                    raise SystemExit(
                        f"asked for citations {o.citations}, and the page shows "
                        f"{prepared['state']['citations']}"
                    )
                # The page clamps a factor outside its control's range and snaps it to the
                # control's step, so a cut that asked for one it declined would be timed by a
                # clock its receipt does not name. Refuse it instead.
                simple_speed = float(prepared["state"]["simpleSpeed"])
                if simple_speed != float(sped[0][1]):
                    raise SystemExit(
                        f"asked for a grid-fill speed-up of {sped[0][1]}, and the page plays "
                        f"{simple_speed}"
                    )
                steps = _steps(page, o.first, o.last)
                durations = _price(page, steps)
                print(
                    f"{len(steps)} steps, n = {o.first} to {o.last}, "
                    f"{math.fsum(durations):.2f} s, {o.fps} fps at {o.height}p, "
                    f"{opened['style']} at shake {opened['anneal']}, "
                    f"grid fills at {simple_speed}x"
                )
                if o.price_against is not None:
                    earlier = json.loads(o.price_against.read_text(encoding="utf-8"))["steps"]
                    print("\n".join(price_report(steps, durations, earlier)))
                    return 0
                receipt = _capture(page, steps, durations, o.fps, frames_dir)
                animation = None
                title = f"Square packing ascent, n = {o.first} to {o.last}"
            else:
                simple_speed = None
                source = o.animation.read_text(encoding="utf-8")
                receipt, animation = _capture_animation(
                    page, source, o.fps, frames_dir, defaults
                )
                title = str(animation.get("name") or o.animation.stem)
                print(
                    f"animation {o.animation.name}, {receipt[0]['seconds']} s, "
                    f"{o.fps} fps at {o.height}p"
                )
            browser.close()
        encode_into_place(
            lambda partial: encode_arguments(
                profile,
                ffmpeg,
                frames_dir,
                o.fps,
                partial,
                page_sha256=page_sha256,
                title=title,
                comment=capture_comment(),
                version=edition.version,
            ),
            o.out,
        )
    finally:
        if o.keep_frames:
            print(f"  frames left in {frames_dir}")
        else:
            shutil.rmtree(holder, ignore_errors=True)

    delivered = measure(o.out)
    seconds = sum(int(step["frames"]) for step in receipt) / o.fps
    failures = conformance(
        profile,
        delivered,
        fps=o.fps,
        width=STAGE_WIDTH * scale,
        height=STAGE_HEIGHT * scale,
        seconds=seconds,
    )
    print(report(profile, delivered, failures))
    if failures:
        raise SystemExit(
            f"the encoded file does not meet the {profile.name} profile, so no receipt was "
            "written. The frames are still on disk if --keep-frames was given."
        )

    document = capture_receipt(
        page=str(o.page.relative_to(PACKING) if o.page.is_relative_to(PACKING) else o.page),
        page_sha256=page_sha256,
        video=o.out.name,
        video_sha256=_digest(o.out),
        first=o.first,
        last=o.last,
        fps=o.fps,
        size=(STAGE_WIDTH * scale, STAGE_HEIGHT * scale),
        steps=receipt,
        profile=profile,
        delivered=delivered,
        provenance=Provenance(
            commit=commit,
            dirty=dirty,
            playwright_version=importlib.metadata.version("playwright"),
            browser_version=browser_version,
            ffmpeg_version=ffmpeg_version(banner.stdout),
        ),
        # The arguments as they amount to: the frames directory and the final name, rather
        # than a temporary directory and a partial file that no longer exist.
        encoder=encode_arguments(
            profile,
            Path(ffmpeg).name,
            Path("frames"),
            o.fps,
            Path(o.out.name),
            page_sha256=page_sha256,
            title=title,
            comment=capture_comment(),
            version=edition.version,
        ),
        capture_seconds=time.monotonic() - started_all,
        edition=edition,
        citations=o.citations,
        simple_speed=simple_speed,
        animation=(
            {
                "animation": str(o.animation),
                "animation_sha256": _digest(o.animation),
                "animation_contract": animation["contract"],
            }
            if o.animation is not None and animation is not None
            else None
        ),
    )
    receipt_path = o.out.with_suffix(".receipt.json")
    write_receipt(receipt_path, document)

    size_mb = o.out.stat().st_size / 1e6
    summary = (
        f"{document['frames']} frames, {document['seconds']}s, {size_mb:.1f} MB "
        f"in {document['capture_seconds']:.0f}s"
    )
    print(f"  {o.out}: {summary}")
    print(f"  {receipt_path}")
    missed = document["steps_off_record"]
    if missed:
        print(f"  {len(missed)} step(s) did not land on the record: n = {missed[:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
