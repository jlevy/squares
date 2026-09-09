"""The revision-6 to revision-9 review stills, 1920x1080.

    packing/.venv/bin/python3 capture_stills.py [name ...]
    packing/.venv/bin/python3 capture_stills.py --workbench
    packing/.venv/bin/python3 capture_stills.py --r9
    packing/.venv/bin/python3 capture_stills.py --r11
    packing/.venv/bin/python3 capture_stills.py --r12

A shot names the n it wants, the instant, and a setup snippet run after the pair is selected.
Where the n is not in `index.html` the shot is taken from `index-all.html` instead.

`--workbench` takes the revision-8 shots instead, from `workbench.html` and with the chrome
*showing*: the point of those is the workbench itself — the controls and where they sit against the
stage — so capture preview, which hides all of it, is exactly the wrong mode for them. Each is a
single snippet driven through the API, so the frame is a pure function of what the snippet does.

`--r9` takes the revision-9 shots the same way. Four of the five show the chrome, because they are
of the workbench; the fifth is in capture preview on purpose — it is the proof that nothing
explaining the page survives into a captured frame.

`--r11` takes the revision-11 shots: the angle colouring, the force law and its plot, the
relationship graph with its mask drawn, and growth run out. All show the chrome, because every one
of them is about a control as much as about the picture.
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


# Revision 11. The colouring, the force law and its plot, the relationship graph and its mask, and
# growth. All show the chrome: every one of them is about a control as much as about the picture.
R11_SHOTS = {
    # The angle map at n = 29, settled on the retained frame: five angle classes taking four palette
    # families, each shaded by the square's own full-side contact count.
    "r11-angle-colour-n29": (False, "A.setStepN(29); A.seek(A.duration());"),
    # A law that is nothing like the default: a hard knee and a long, strong pull, so the plot shows
    # a steep wall on the left of zero and a deep hump on the right of it.
    "r11-force-curve": (False, "A.setStepN(17); A.setLaw({rigidity: 0.02, repulsion: 5000,"
                        " attraction: 320, range: 0.45}); A.setInitial('grid'); A.optimizeStep(600);"),
    # The same case under two very different laws, settled the same number of steps.
    "r11-rigid": (False, "A.setStepN(17); A.setLawPreset('rigid'); A.setInitial('grid'); A.optimizeStep(2400);"),
    "r11-sticky": (False, "A.setStepN(17); A.setLawPreset('sticky'); A.setInitial('grid'); A.optimizeStep(2400);"),
    # The contact relationship with the mask drawn: faint lines on the pairs the attraction reaches.
    "r11-contact-bias": (False, "A.setStepN(29); A.setLawPreset('sticky'); A.setRelationship('contact');"
                         " A.setOverlay(true); A.setInitial('grid'); A.optimizeStep(2400);"),
    # Growth run out: the squares have reached a unit side and the walls have taken over again.
    "r11-grow-done": (False, "A.setStepN(17); A.setGrowth({size: 0.3, rate: 0.05, rule: 'clean', on: true});"
                      " A.setInitial('grid'); A.optimizeStep(7200);"),
}


# Revision 12. Colour is the square's identity by default, the controls do not reflow, Pack has no
# position bar, and a contact graph can be drawn by hand between squares. All show the chrome.
R12_SHOTS = {
    # The default, settled: n = 29 in its identity greens, every square its own colour and nothing
    # about the colouring reading off the angles.
    "r12-identity-default": (False, "A.setColorScheme('identity'); A.setStepN(29); A.seek(A.duration());"),
    # The same case in motion, with the desaturation off so the fills are *literally* the ones the
    # settled frame shows: the squares turn and slide and not one of them changes colour.
    "r12-identity-moving": (False, "A.setColorScheme('identity'); A.setStepN(29); A.setStyle('bodies');"
                            " A.setSnap(false); A.setDesaturate(false); A.seek(A.duration() * 0.62);"),
    # And the same case under revision 11's angle map, for comparison: the tilts are legible, but
    # two squares of the same tilt are one colour and a square that turns changes colour.
    "r12-angle-stable": (False, "A.setColorScheme('angle-stable'); A.setStepN(29); A.seek(A.duration());"),
    # Pack, with no position bar: one fixed n has nothing to say about a corpus-wide scale.
    "r12-pack-no-bar": (False, "A.setMode('pack'); A.setStepN(17); A.seek(A.duration());"),
    # A contact graph drawn by hand — a ring joining each square to the next — on the retained
    # frame of 11: the edges already in contact are solid and white, the ones only wanted are
    # dashed and dark, and the readout counts the first kind.
    "r12-drawn-graph": (False, "A.setColorScheme('identity'); A.setStepN(11); A.seek(A.duration());"
                        " A.setDrawing(true);"
                        " A.setEdges(Array.from({length: 11}, (_, i) => [i, (i + 1) % 11]));"
                        " A.setRelationship('contact');"),
    # The same graph after an Optimize run from the ordered fill: the fraction in the readout is
    # what the bias actually reached.
    "r12-drawn-optimized": (False, "A.setColorScheme('identity'); A.setStepN(11);"
                            " A.setDrawing(true);"
                            " A.setEdges(Array.from({length: 11}, (_, i) => [i, (i + 1) % 11]));"
                            " A.setRelationship('contact'); A.setLawPreset('sticky');"
                            " A.setInitial('grid'); A.optimizeStep(2400);"),
}


def shots(page, table, errors) -> None:
    for name, (capture, setup) in table.items():
        page.evaluate(
            "([setup, capture]) => { const A = window.atlasTransitions;"
            " A.stopAll(); A.setCapture(false); A.setStyle('tween'); A.setSnap(true); A.setBlind(false);"
            " A.setDesaturate(true); A.setAnneal(3); A.setSpeed(1); A.setInitial('previous');"
            " if (A.reset) A.reset(); if (A.setOverlay) A.setOverlay(false);"
            # revision 12: the scheme, the drawing mode and any drawn edges are reset between
            # shots so one shot cannot leak into the next.
            " if (A.setDrawing) { A.setDrawing(false); A.clearEdges(); }"
            " if (A.setColorScheme) A.setColorScheme('identity');"
            " if (A.setMode) A.setMode('pack');"
            " A.setRange(17, 17); A.seek(0); (new Function('A', setup))(A); }",
            [setup, capture],
        )
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
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(f"file://{HERE / 'workbench.html'}")
        page.wait_for_timeout(900)
        shots(page, table, errors)
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
        return from_workbench(R9_SHOTS)
    if "--r11" in sys.argv[1:]:
        return from_workbench(R11_SHOTS)
    if "--r12" in sys.argv[1:]:
        return from_workbench(R12_SHOTS)
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
