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
page digest, for anyone who has the video without the receipt.

What this does NOT yet do is play a PackingStrategy document: the workbench animates the
retained corpus, and the strategy documents `workbench_tools.ascent`
(`squares-workbench-ascent`) writes reach the renderer by the SVG path instead. Wiring the two
together is `think-883t`, and until it lands the receipt names records rather than strategy
documents.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m workbench_tools.capture_video --to 24
    uv run --frozen --all-extras --group dev python -m workbench_tools.capture_video \
        --from 100 --to 110 --fps 60 --height 2160 --out site/workbench/ascent-4k.mp4
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
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

#: The frames' file names, numbered from zero without gaps, which is what ffmpeg's image
#: sequence reader requires.
FRAME_PATTERN = "f%07d.png"

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


def pricing_commands(first: int, last: int) -> list[list[Any]]:
    """The commands that put the page on the beat it plays a range at, with the clock stopped.

    Animate is the mode that plays a range and `playRange` is how it plays one: it turns
    continuous play on, which is what prices a static append at its short beat. Pausing in
    the same browser turn stops the clock before a frame of it runs, so the capture seeks
    through the range on that beat rather than watching it play.
    """
    return [["setMode", "animate"], ["setRange", first, last], ["playRange"], ["pause"]]


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
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Capture an imported v1 animation at the document's declared duration."""
    imported = _control(
        page,
        prepare=True,
        commands=[["importAnimation", source]],
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


def metadata_comment(page_sha256: str) -> str:
    """The MP4 comment: the receipt's statement and the page digest, for a video on its own."""
    return (
        f"intermediate_frames: {INTERMEDIATE_FRAMES}. Transitions are illustrative, not "
        f"packings: frames between checked records are tweens. page sha256 {page_sha256}"
    )


def encode_arguments(
    ffmpeg: str,
    frames_dir: Path,
    fps: int,
    out: Path,
    *,
    page_sha256: str,
    title: str,
) -> list[str]:
    """The ffmpeg command that encodes the frames to an H.264 MP4 anything will play.

    `yuv420p` and the even-dimension scale are not taste: without them QuickTime and most
    browsers refuse the file outright, which would make an unplayable "uploadable" video.
    `+faststart` puts the index first so a browser can start playing before the download
    ends. `-n` rather than `-y`: the output is a fresh temporary beside the destination, and
    ffmpeg overwriting anything would mean it was not.
    """
    return [
        ffmpeg,
        "-n",
        "-framerate",
        str(fps),
        "-i",
        str(frames_dir / FRAME_PATTERN),
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-vf",
        "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        "-movflags",
        "+faststart",
        "-metadata",
        f"title={title}",
        "-metadata",
        f"comment={metadata_comment(page_sha256)}",
        "-f",
        "mp4",
        str(out),
    ]


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
    encoder: list[str],
    capture_seconds: float,
    animation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """The receipt written beside a video: what it shows, what made it, and what it is not."""
    frames = sum(int(step["frames"]) for step in steps)
    missed = [step["n"] for step in steps if step.get("landed_on_record") is False]
    drawn = [float(step["ms_per_frame"]) for step in steps]
    worst = max(drawn)
    return {
        "page": page,
        "page_sha256": page_sha256,
        "video": video,
        "video_sha256": video_sha256,
        "range": [first, last],
        **(animation or {}),
        "fps": fps,
        "size": list(size),
        "frames": frames,
        "seconds": round(frames / fps, 3),
        "steps_off_record": missed,
        "transitions_are_packings": False,
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
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--height", type=int, default=1080, choices=sorted(HEIGHTS))
    ap.add_argument(
        "--animation",
        type=Path,
        help="capture this PackingAnimation/v1 document instead of the retained catalogue",
    )
    ap.add_argument("--out", type=Path, default=PACKING / "site/workbench/ascent.mp4")
    ap.add_argument("--keep-frames", action="store_true", help="leave the PNGs for inspection")
    o = ap.parse_args()

    if not o.page.exists():
        raise SystemExit(f"{o.page} is not built: run `squares-workbench-build` first")
    ffmpeg = _encoder()
    scale = HEIGHTS[o.height]
    started_all = time.monotonic()
    # Digested before it is loaded, so the receipt names the page the frames came from rather
    # than whatever sits at that path once the capture is over.
    page_sha256 = _digest(o.page)
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
            page.goto(o.page.resolve().as_uri(), wait_until="load")
            page.evaluate(probe("capture/fonts-ready"))
            # Capture preview, applied by `prepare`, is what hides the chrome.
            if o.animation is None:
                _control(page, prepare=True, commands=pricing_commands(o.first, o.last))
                steps = _steps(page, o.first, o.last)
                durations = _price(page, steps)
                print(
                    f"{len(steps)} steps, n = {o.first} to {o.last}, "
                    f"{math.fsum(durations):.2f} s, {o.fps} fps at {o.height}p"
                )
                receipt = _capture(page, steps, durations, o.fps, frames_dir)
                animation = None
                title = f"Square packing ascent, n = {o.first} to {o.last}"
            else:
                source = o.animation.read_text(encoding="utf-8")
                receipt, animation = _capture_animation(page, source, o.fps, frames_dir)
                title = str(animation.get("name") or o.animation.stem)
                print(
                    f"animation {o.animation.name}, {receipt[0]['seconds']} s, "
                    f"{o.fps} fps at {o.height}p"
                )
            browser.close()
        encode_into_place(
            lambda partial: encode_arguments(
                ffmpeg, frames_dir, o.fps, partial, page_sha256=page_sha256, title=title
            ),
            o.out,
        )
    finally:
        if o.keep_frames:
            print(f"  frames left in {frames_dir}")
        else:
            shutil.rmtree(holder, ignore_errors=True)

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
            Path(ffmpeg).name,
            Path("frames"),
            o.fps,
            Path(o.out.name),
            page_sha256=page_sha256,
            title=title,
        ),
        capture_seconds=time.monotonic() - started_all,
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
