"""Nothing on the stage explains the stage, and nothing on it is apparatus.

Revision 8 called this the legend check: three stacked lines under the Open group naming the
scarlet convention, the active style and what a free or blind run was doing. Revision 9 removed all
three, so this became the check that they stayed removed — no instruction survives a capture.
Revision 16 removed the rest of the apparatus for the same reason: the live gap readout under the
stage, and the position bar along its foot with its scale, fill, cursor and riding n. The owner
found them distracting, and the stage carries facts about the packing rather than instruments for
the playback.

So the rows this file used to hold apart are gone, and with them the geometry that held them:
most of what it measured was the drawing, not the property. What is left is the same question
asked of more elements — that none of them grew back, and that no wording survives a capture —
which is the part a still can still fail. The figures those rows carried are now read from the
API that filled them, in `check_workbench.py`, which is where a number belongs.

    packing/.venv/bin/python3 check_legend.py [index.html]
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent

# The lines revision 9 removed and the apparatus revision 16 removed, by id. A page that grows any
# of them back fails here rather than in a still nobody looks at twice.
GONE_IDS = (
    "legend-style",
    "legend-note",
    "pair-info",
    # Revision 16: the live gap readout under the stage, and each of its rows.
    "gap-read",
    "gap-a",
    "gap-b",
    "gap-c",
    "gap-d",
    "gap-e",
    # Revision 16: the position bar along the stage's foot, and everything drawn on it.
    "progress",
    "p-scale",
    "p-fill",
    "p-cursor",
    "p-n",
)

# The same two, by the class each stack was drawn with, so a rebuilt row without its id is caught.
GONE_CLASSES = (".legend", ".gap-line", ".p-num")

GONE_WORDS = (
    "the arriving square is scarlet",
    "style A, tween",
    "style B, physics",
    "style C, bodies",
    "no snap:",
    "blind run",
    "style A interpolates",
    "Tweens are illustrative",
    "block-aware matching",
    "Keys:",
)

STAGE_TEXT = "() => document.getElementById('stage').innerText.replace(/\\s+/g, ' ')"


def main() -> int:
    page_path = (HERE / sys.argv[1]) if len(sys.argv) > 1 else HERE / "index.html"
    bad = []
    combinations = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.on("pageerror", lambda e: bad.append(f"pageerror: {e}"))
        page.goto(f"file://{page_path}")
        page.wait_for_timeout(700)
        index_of = {q["n"]: q["index"] for q in page.evaluate("atlasTransitions.pairs()")}
        for ident in GONE_IDS:
            if page.evaluate(f"document.getElementById({ident!r}) !== null"):
                bad.append(f"the removed element #{ident} is back in the page")
        for sel in GONE_CLASSES:
            if page.evaluate(f"document.querySelectorAll({sel!r}).length") != 0:
                bad.append(f"the removed stack {sel} is back on the stage")
        page.evaluate("atlasTransitions.setCapture(true)")
        for n in (100, 110, 307):
            if n not in index_of:
                continue
            for style in ("tween", "physics", "bodies"):
                for mode in ("snap", "free", "blind"):
                    # Both ends of the annealing dial, at rest and in the middle of the move: no
                    # wording anywhere on the stage, whatever the page is doing.
                    for level in (3, 10):
                        for at in (2.0, 2.8):
                            page.evaluate(
                                "([i, s, m, L, t]) => { const A = window.atlasTransitions; A.select(i); A.setStyle(s);"
                                " A.setSnap(m !== 'free'); A.setBlind(m === 'blind'); A.setAnneal(L); A.seek(t); }",
                                [index_of[n], style, mode, level, at],
                            )
                            combinations += 1
                            label = f"n={n} {style}/{mode} anneal {level} at {at}"
                            # The stage's whole text, as a viewer would read it off a still.
                            stage_text = page.evaluate(STAGE_TEXT)
                            for word in GONE_WORDS:
                                if word.lower() in stage_text.lower():
                                    bad.append(f"{label}: the stage still says {word!r}")
        # And an open-ended run, at both n the demo carries and from every start: it reports its
        # figures through the API now, so the stage stays silent here too.
        for n in (17, 100, 307):
            if n not in index_of:
                continue
            for kind in ("grid", "random", "previous"):
                page.evaluate(
                    "([n, k]) => { const A = window.atlasTransitions; A.setStepN(n); A.setInitial(k);"
                    "  if (k === 'previous') { A.optimize(true); A.pause(); } A.optimizeStep(1200); }",
                    [n, kind],
                )
                combinations += 1
                label = f"optimize n={n} from {kind}"
                stage_text = page.evaluate(STAGE_TEXT)
                for word in GONE_WORDS:
                    if word.lower() in stage_text.lower():
                        bad.append(f"{label}: the stage still says {word!r}")
        page.evaluate("atlasTransitions.setInitial('previous'); atlasTransitions.setCapture(false)")
        browser.close()
    if bad:
        print("FAILED")
        for b in dict.fromkeys(bad):
            print(" -", b)
        return 1
    print(
        f"OK: no legend, style line, miss note, block-matching sentence or key hint anywhere on "
        f"the stage over {combinations} combinations of pair, style, mode, annealing level and "
        f"instant, including an open-ended run from each of the three starts; and none of the "
        f"{len(GONE_IDS)} removed elements, nor any of the three stacks they were drawn with, is "
        f"back in the page"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
