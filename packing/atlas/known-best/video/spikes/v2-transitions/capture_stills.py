"""The revision-6 to revision-9 review stills, 1920x1080.

    packing/.venv/bin/python3 capture_stills.py [name ...]
    packing/.venv/bin/python3 capture_stills.py --workbench
    packing/.venv/bin/python3 capture_stills.py --r9

A shot names the n it wants, the instant, and a setup snippet run after the pair is selected.
Where the n is not in `index.html` the shot is taken from `index-all.html` instead.

`--workbench` takes the revision-8 shots instead, from `workbench.html` and with the chrome
*showing*: the point of those is the workbench itself — the controls and where they sit against the
stage — so capture preview, which hides all of it, is exactly the wrong mode for them. Each is a
single snippet driven through the API, so the frame is a pure function of what the snippet does.

`--r9` takes the revision-9 shots the same way. Four of the five show the chrome, because they are
of the workbench; the fifth is in capture preview on purpose — it is the proof that nothing
explaining the page survives into a captured frame.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
REVIEW = HERE / "review"

# name -> (n, seconds, setup called with the pair index)
SHOTS = {
    "feat-desat-100-mid": (100, 1.7, "atlasTransitions.setStyle('bodies');"),
    "feat-nosnap-100-end": (100, 2.8, "atlasTransitions.setStyle('bodies'); atlasTransitions.setSnap(false);"),
    "feat-blind-100-end": (100, 2.8, "atlasTransitions.setStyle('bodies'); atlasTransitions.setBlind(true);"),
    # The first frame after a pair boundary under continuous play: the beat is the sequence's own
    # (0.8 + 1.2 + 0.3), the panel has rolled to 101 and the bar has stepped on.
    "feat-playall-boundary": (101, 0.02, "atlasTransitions.setStyle('bodies'); atlasTransitions.playAll(); atlasTransitions.pause();"),
    # Revision 7. The scale at the left end and at the right end of the movie; the annealing dial at
    # its loudest, mid move; the live gap readout with the snap off.
    "r7-scale-100": (100, 1.7, "atlasTransitions.setStyle('bodies');"),
    "r7-scale-324": (323, 2.8, "atlasTransitions.setStyle('bodies');"),
    # at level 10 the move is 1.7 times as long (1.0 to 3.38 s), so its middle is 2.19 s.
    "r7-anneal-10-mid": (100, 2.19, "atlasTransitions.setStyle('bodies'); atlasTransitions.setAnneal(10);"),
    "r7-gap-readout": (100, 2.1, "atlasTransitions.setStyle('bodies'); atlasTransitions.setSnap(false);"),
}


# Revision 8. The workbench, chrome and all, from `workbench.html`. Each value is the whole setup:
# the API is `A` and the shot is taken as the snippet leaves the page.
WB_SHOTS = {
    # The single-step tab as it opens, settled on 17: the step label, the chooser, the quick picks,
    # and the gap bar with the record met and the check green.
    "wb-single-17": "A.setTab('single'); A.setStepN(17); A.seek(A.duration());",
    # The same n with the physics let off the leash: the hand rests where style C actually landed,
    # short of the record, and the check is empty.
    "wb-single-17-gapbar": "A.setTab('single'); A.setStepN(17); A.setStyle('bodies'); A.setSnap(false);"
    " A.seek(A.schedule().moveEnd);",
    # The sequence tab at the head of its default range: the from and to boxes, the run's length,
    # and the progress bar's scale spanning 1 to 100 rather than 1 to 324.
    "wb-sequence-1-100": "A.setTab('sequence'); A.setRange(1, 100); A.playRange(); A.pause(); A.seek(0.5);",
    # And in the middle of that run: step 43 of 99, the fill and the riding n scoped to the range.
    "wb-sequence-running": "A.setTab('sequence'); A.setRange(1, 100); A.playRange(); A.pause();"
    " A.goTo(43); A.seek(1.6);",
}


# Revision 9. The single view, the three starts, the open-ended run and the hand. `capture` says
# whether the shot is taken with the chrome hidden; only the last one is, and that is its whole point.
R9_SHOTS = {
    # The one view as it opens: one control set, the range collapsed on 17, the transport glyphs,
    # the speed slider, the start chooser and Optimize, and a stage with no instructions on it.
    "r9-single-view": (False, "A.setStepN(17); A.seek(A.duration());"),
    # The random start, put on the stage the moment it is chosen and waiting to be optimised.
    "r9-initial-random": (False, "A.setStepN(17); A.setInitial('random');"),
    # The same run 20 simulated seconds in: the walls closed, and the panel reporting the clock, the
    # step count, the smallest box it has held them in and the overlap in it.
    "r9-optimize-running": (False, "A.setStepN(17); A.setInitial('grid'); A.optimizeStep(2400);"),
    # A square held away from the packing while the run pushes its neighbours around: the readout
    # jumps to the side the hand is asking for, and the run is marked hand-edited.
    "r9-drag": (False, "A.setStepN(17); A.setInitial('grid'); A.optimizeStep(600);"
                " A.grab(A.pickAt(0.5, 0.5), 0.5, 0.5); A.dragTo(6.2, 3.4, false); A.optimizeStep(120);"),
    # Capture preview, mid motion, with everything that could narrate turned on: the picture and its
    # facts, and not one line telling the viewer what to think.
    "r9-capture-clean": (True, "A.setStepN(17); A.setStyle('bodies'); A.setSnap(false); A.setAnneal(10);"
                         " A.setCapture(true); A.seek(2.2);"),
}


def shots(page, table, errors) -> None:
    for name, (capture, setup) in table.items():
        page.evaluate(
            "([setup, capture]) => { const A = window.atlasTransitions;"
            " A.stopAll(); A.setCapture(false); A.setStyle('tween'); A.setSnap(true); A.setBlind(false);"
            " A.setDesaturate(true); A.setAnneal(3); A.setSpeed(1); A.setInitial('previous');"
            " A.setRange(17, 17); A.seek(0); (new Function('A', setup))(A); }",
            [setup, capture],
        )
        page.wait_for_timeout(250)
        page.screenshot(path=str(REVIEW / f"{name}.png"))
        print(f"{name}.png")


def revision9() -> int:
    """The revision-9 stills, from the workbench."""
    REVIEW.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        errors: list[str] = []
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(f"file://{HERE / 'workbench.html'}")
        page.wait_for_timeout(900)
        shots(page, R9_SHOTS, errors)
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
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(f"file://{HERE / 'workbench.html'}")
        page.wait_for_timeout(900)
        for name, setup in WB_SHOTS.items():
            page.evaluate(
                "(setup) => { const A = window.atlasTransitions;"
                " A.stopAll(); A.setCapture(false); A.setStyle('tween'); A.setSnap(true); A.setBlind(false);"
                " A.setDesaturate(true); A.setAnneal(3); A.setTab('single'); (new Function('A', setup))(A); }",
                setup,
            )
            page.wait_for_timeout(250)
            page.screenshot(path=str(REVIEW / f"{name}.png"))
            print(f"{name}.png")
        print("ERRORS:", errors or "none")
        browser.close()
    return 0


def main() -> int:
    if "--r9" in sys.argv[1:]:
        return revision9()
    if "--workbench" in sys.argv[1:]:
        return workbench()
    wanted = sys.argv[1:] or list(SHOTS)
    REVIEW.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        errors: list[str] = []
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(f"file://{HERE / 'index.html'}")
        page.wait_for_timeout(900)
        index_of = {q["n"]: q["index"] for q in page.evaluate("atlasTransitions.pairs()")}
        for name in wanted:
            if name not in SHOTS:
                continue
            n, t, setup = SHOTS[name]
            page.evaluate(
                "([i, setup, t]) => { const A = window.atlasTransitions;"
                " A.stopAll(); A.setStyle('tween'); A.setSnap(true); A.setBlind(false); A.setDesaturate(true); A.setAnneal(3);"
                " A.setCapture(true); A.select(i); (new Function(setup))(); A.seek(t); }",
                [index_of[n], setup, t],
            )
            page.wait_for_timeout(250)
            page.screenshot(path=str(REVIEW / f"{name}.png"))
            print(f"{name}.png  n={n} t={t}  note={page.evaluate('document.getElementById(chr(0))')}" if False else f"{name}.png  n={n} t={t}")
        print("ERRORS:", errors or "none")
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
