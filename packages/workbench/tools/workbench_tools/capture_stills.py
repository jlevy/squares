"""Capture maintained catalogue and imported-animation review stills at 1920x1080.

    packing/.venv/bin/python3 capture_stills.py [name ...]
    packing/.venv/bin/python3 capture_stills.py --workbench
    packing/.venv/bin/python3 capture_stills.py --r9
    packing/.venv/bin/python3 capture_stills.py --r11
    packing/.venv/bin/python3 capture_stills.py --r12

A shot names the n it wants, the instant, and typed API commands applied after selection.

`--workbench` takes the revision-8 shots instead, from `workbench.html` and with the
chrome *showing*: the point of those is the workbench itself — the controls and where
they sit against the stage — so capture preview, which hides all of it, is exactly the
wrong mode for them. Each is a single snippet driven through the API, so the frame is a
pure function of what the snippet does.

`--r9` takes the revision-9 shots the same way. Four of the five show the chrome, because
they are of the workbench; the fifth is in capture preview on purpose — it is the proof
that nothing explaining the page survives into a captured frame.

`--r11` takes the revision-11 shots: the angle colouring, the force law and its plot, the
relationship graph with its mask drawn, and growth run out. All show the chrome, because
every one of them is about a control as much as about the picture.
"""

import argparse
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright

from workbench_tools.probes import probe

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
REPO = PACKAGE_ROOT.parents[1]
PAGE = REPO / "packing/site/workbench/index.html"
REVIEW = PACKAGE_ROOT / "dist/review"

Command = list[Any]


def control(
    page: Any,
    *,
    commands: list[Command] | None = None,
    read: list[str] | None = None,
    prepare: bool = False,
    capture: bool = True,
) -> dict[str, Any]:
    """Drive and inspect the page through the checked capture controller."""
    request: dict[str, Any] = {}
    if commands:
        request["commands"] = commands
    if read:
        request["read"] = read
    if prepare:
        request.update({"prepare": True, "capture": capture})
    return page.evaluate(probe("capture/control"), request)


# name -> (n, seconds, commands applied after the pair is selected)
SHOTS = {
    "feat-desat-100-mid": (100, 1.7, [["setStyle", "bodies"]]),
    "feat-nosnap-100-end": (
        100,
        2.8,
        [["setStyle", "bodies"], ["setSnap", False]],
    ),
    "feat-blind-100-end": (
        100,
        2.8,
        [["setStyle", "bodies"], ["setBlind", True]],
    ),
    # The first frame after a pair boundary under continuous play: the beat is the
    # sequence's own (0.8 + 1.2 + 0.3), the panel has rolled to 101 and the bar has
    # stepped on.
    "feat-playall-boundary": (
        101,
        0.02,
        [["setStyle", "bodies"], ["playAll"], ["pause"]],
    ),
    # Revision 7. The scale at the left end and at the right end of the movie; the
    # annealing dial at its loudest, mid move; the live gap readout with the snap off.
    "r7-scale-100": (100, 1.7, [["setStyle", "bodies"]]),
    "r7-scale-324": (323, 2.8, [["setStyle", "bodies"]]),
    # at level 10 the move is 1.7 times as long (1.0 to 3.38 s), so its middle is 2.19 s.
    "r7-anneal-10-mid": (
        100,
        2.19,
        [["setStyle", "bodies"], ["setAnneal", 10]],
    ),
    "r7-gap-readout": (
        100,
        2.1,
        [["setStyle", "bodies"], ["setSnap", False]],
    ),
}


# Revision 8. The workbench, chrome and all, from `workbench.html`. Each value is the
# whole setup: the API is `A` and the shot is taken as the snippet leaves the page.
WB_SHOTS = {
    # The single-step tab as it opens, settled on 17: the step label, the chooser, the
    # quick picks, and the gap bar with the record met and the check green.
    "wb-single-17": [["setStepN", 17], ["seekStepFraction", 1]],
    # The same n with the physics let off the leash: the hand rests where style C actually
    # landed, short of the record, and the check is empty.
    "wb-single-17-gapbar": [
        ["setStepN", 17],
        ["setStyle", "bodies"],
        ["setSnap", False],
        ["seekScheduleMoveEnd"],
    ],
    # The sequence tab at the head of its default range: the from and to boxes, the run's
    # length, and the progress bar's scale spanning 1 to 100 rather than 1 to 324.
    "wb-sequence-1-100": [
        ["setMode", "animate"],
        ["setRange", 1, 100],
        ["playRange"],
        ["pause"],
        ["seek", 0.5],
    ],
    # And in the middle of that run: step 43 of 99, the fill and the riding n scoped to
    # the range.
    "wb-sequence-running": [
        ["setMode", "animate"],
        ["setRange", 1, 100],
        ["playRange"],
        ["pause"],
        ["goTo", 43],
        ["seek", 1.6],
    ],
}


# Revision 9. The single view, the three starts, the open-ended run and the hand.
# `capture` says whether the shot is taken with the chrome hidden; only the last one is,
# and that is its whole point.
R9_SHOTS = {
    # The one view as it opens: one control set, the range collapsed on 17, the transport
    # glyphs, the speed slider, the start chooser and Optimize, and a stage with no
    # instructions on it.
    "r9-single-view": (False, [["setStepN", 17], ["seekStepFraction", 1]]),
    # The random start, put on the stage the moment it is chosen and waiting to be optimised.
    "r9-initial-random": (False, [["setStepN", 17], ["setInitial", "random"]]),
    # The same run 20 simulated seconds in: the walls closed, and the panel reporting the
    # clock, the step count, the smallest box it has held them in and the overlap in it.
    "r9-optimize-running": (
        False,
        [["setStepN", 17], ["setInitial", "grid"], ["optimizeStep", 2400]],
    ),
    # A square held away from the packing while the run pushes its neighbours around: the
    # readout jumps to the side the hand is asking for, and the run is marked hand-edited.
    "r9-drag": (
        False,
        [
            ["setStepN", 17],
            ["setInitial", "grid"],
            ["optimizeStep", 600],
            ["grabAt", 0.5, 0.5],
            ["dragTo", 6.2, 3.4, False],
            ["optimizeStep", 120],
        ],
    ),
    # Capture preview, mid motion, with everything that could narrate turned on: the
    # picture and its facts, and not one line telling the viewer what to think.
    "r9-capture-clean": (
        True,
        [
            ["setStepN", 17],
            ["setStyle", "bodies"],
            ["setSnap", False],
            ["setAnneal", 10],
            ["setCapture", True],
            ["seek", 2.2],
        ],
    ),
}


# Revision 11. The colouring, the force law and its plot, the relationship graph and its
# mask, and growth. All show the chrome: every one of them is about a control as much as
# about the picture.
R11_SHOTS = {
    # The angle map at n = 29, settled on the retained frame: five angle classes taking
    # four palette families, each shaded by the square's own full-side contact count.
    "r11-angle-colour-n29": (False, [["setStepN", 29], ["seekStepFraction", 1]]),
    # A law that is nothing like the default: a hard knee and a long, strong pull, so the
    # plot shows a steep wall on the left of zero and a deep hump on the right of it.
    "r11-force-curve": (
        False,
        [
            ["setStepN", 17],
            [
                "setLaw",
                {"rigidity": 0.02, "repulsion": 5000, "attraction": 320, "range": 0.45},
            ],
            ["setInitial", "grid"],
            ["optimizeStep", 600],
        ],
    ),
    # The same case under two very different laws, settled the same number of steps.
    "r11-rigid": (
        False,
        [
            ["setStepN", 17],
            ["setLawPreset", "rigid"],
            ["setInitial", "grid"],
            ["optimizeStep", 2400],
        ],
    ),
    "r11-sticky": (
        False,
        [
            ["setStepN", 17],
            ["setLawPreset", "sticky"],
            ["setInitial", "grid"],
            ["optimizeStep", 2400],
        ],
    ),
    # The contact relationship with the mask drawn: faint lines on the pairs the
    # attraction reaches.
    "r11-contact-bias": (
        False,
        [
            ["setStepN", 29],
            ["setLawPreset", "sticky"],
            ["setRelationship", "contact"],
            ["setOverlay", True],
            ["setInitial", "grid"],
            ["optimizeStep", 2400],
        ],
    ),
    # Growth run out: the squares have reached a unit side and the walls have taken over
    # again.
    "r11-grow-done": (
        False,
        [
            ["setStepN", 17],
            ["setGrowth", {"size": 0.3, "rate": 0.05, "rule": "clean", "on": True}],
            ["setInitial", "grid"],
            ["optimizeStep", 7200],
        ],
    ),
}


# Revision 12. Colour is the square's identity by default, the controls do not reflow,
# Pack has no position bar, and a contact graph can be drawn by hand between squares. All
# show the chrome.
R12_SHOTS = {
    # The default, settled: n = 29 in its identity greens, every square its own colour and
    # nothing about the colouring reading off the angles.
    "r12-identity-default": (
        False,
        [["setColorScheme", "identity"], ["setStepN", 29], ["seekStepFraction", 1]],
    ),
    # The same case in motion, with the desaturation off so the fills are *literally* the
    # ones the settled frame shows: the squares turn and slide and not one of them changes
    # colour.
    "r12-identity-moving": (
        False,
        [
            ["setColorScheme", "identity"],
            ["setStepN", 29],
            ["setStyle", "bodies"],
            ["setSnap", False],
            ["setDesaturate", False],
            ["seekStepFraction", 0.62],
        ],
    ),
    # And the same case under revision 11's angle map, for comparison: the tilts are
    # legible, but two squares of the same tilt are one colour and a square that turns
    # changes colour.
    "r12-angle-stable": (
        False,
        [["setColorScheme", "angle-stable"], ["setStepN", 29], ["seekStepFraction", 1]],
    ),
    # Pack, with no position bar: one fixed n has nothing to say about a corpus-wide scale.
    "r12-pack-no-bar": (
        False,
        [["setMode", "pack"], ["setStepN", 17], ["seekStepFraction", 1]],
    ),
    # A contact graph drawn by hand — a ring joining each square to the next — on the retained
    # frame of 11: the edges already in contact are solid and white, the ones only wanted are
    # dashed and dark, and the readout counts the first kind.
    "r12-drawn-graph": (
        False,
        [
            ["setColorScheme", "identity"],
            ["setStepN", 11],
            ["seekStepFraction", 1],
            ["setDrawing", True],
            ["setEdges", [[i, (i + 1) % 11] for i in range(11)]],
            ["setRelationship", "contact"],
        ],
    ),
    # The same graph after an Optimize run from the ordered fill: the fraction in the
    # readout is what the bias actually reached.
    "r12-drawn-optimized": (
        False,
        [
            ["setColorScheme", "identity"],
            ["setStepN", 11],
            ["setDrawing", True],
            ["setEdges", [[i, (i + 1) % 11] for i in range(11)]],
            ["setRelationship", "contact"],
            ["setLawPreset", "sticky"],
            ["setInitial", "grid"],
            ["optimizeStep", 2400],
        ],
    ),
}


def shots(page, table) -> None:
    for name, (capture, commands) in table.items():
        control(page, prepare=True, capture=capture, commands=commands)
        page.wait_for_timeout(250)
        page.screenshot(path=str(REVIEW / f"{name}.png"))
        print(f"{name}.png")


def from_workbench(table) -> int:
    """Drive one table of shots against the workbench, chrome and all."""
    REVIEW.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        errors: list[str] = []
        page.on(
            "console",
            lambda m: (
                errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None
            ),
        )
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(PAGE.resolve().as_uri())
        page.evaluate(probe("capture/fonts-ready"))
        page.wait_for_timeout(900)
        shots(page, table)
        print("ERRORS:", errors or "none")
        browser.close()
    return 0


def workbench() -> int:
    """The revision-8 stills, with the controls visible."""
    REVIEW.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        errors: list[str] = []
        page.on(
            "console",
            lambda m: (
                errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None
            ),
        )
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(PAGE.resolve().as_uri())
        page.evaluate(probe("capture/fonts-ready"))
        page.wait_for_timeout(900)
        for name, commands in WB_SHOTS.items():
            control(page, prepare=True, capture=False, commands=commands)
            page.wait_for_timeout(250)
            page.screenshot(path=str(REVIEW / f"{name}.png"))
            print(f"{name}.png")
        print("ERRORS:", errors or "none")
        browser.close()
    return 0


def animation_stills(animation: Path, instants: list[float]) -> int:
    """Capture an imported document at explicit seconds on its declared clock."""
    REVIEW.mkdir(parents=True, exist_ok=True)
    source = animation.read_text(encoding="utf-8")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(PAGE.resolve().as_uri())
        page.evaluate(probe("capture/fonts-ready"))
        imported = control(
            page,
            prepare=True,
            commands=[["importAnimation", source]],
            read=["animation"],
        )
        duration = float(imported["animation"]["durationSeconds"])
        chosen = instants or [0, duration / 2, duration]
        for seconds in chosen:
            if not 0 <= seconds <= duration:
                raise ValueError(
                    f"animation instant {seconds} is outside 0..{duration} seconds"
                )
            control(page, commands=[["seekAnimation", seconds / duration]])
            name = f"animation-{seconds:07.3f}s.png"
            page.screenshot(path=str(REVIEW / name), type="png")
            print(name)
        browser.close()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="*", help="named catalogue stills")
    parser.add_argument("--workbench", action="store_true")
    parser.add_argument("--r9", action="store_true")
    parser.add_argument("--r11", action="store_true")
    parser.add_argument("--r12", action="store_true")
    parser.add_argument("--animation", type=Path)
    parser.add_argument(
        "--at",
        type=float,
        action="append",
        default=[],
        help="animation instant in seconds; repeatable (default: start, midpoint, end)",
    )
    options = parser.parse_args()
    if options.animation is not None:
        return animation_stills(options.animation, options.at)
    if options.r9:
        return from_workbench(R9_SHOTS)
    if options.r11:
        return from_workbench(R11_SHOTS)
    if options.r12:
        return from_workbench(R12_SHOTS)
    if options.workbench:
        return workbench()
    wanted = options.names or list(SHOTS)
    REVIEW.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        errors: list[str] = []
        page.on(
            "console",
            lambda m: (
                errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None
            ),
        )
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(PAGE.resolve().as_uri())
        page.evaluate(probe("capture/fonts-ready"))
        page.wait_for_timeout(900)
        pairs = control(page, read=["pairs"])["pairs"]
        index_of = {pair["n"]: pair["index"] for pair in pairs}
        for name in wanted:
            if name not in SHOTS:
                continue
            n, t, commands = SHOTS[name]
            control(
                page,
                prepare=True,
                capture=True,
                commands=[["select", index_of[n]], *commands, ["seek", t]],
            )
            page.wait_for_timeout(250)
            page.screenshot(path=str(REVIEW / f"{name}.png"))
            print(f"{name}.png  n={n} t={t}")
        print("ERRORS:", errors or "none")
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
