"""Nothing on the stage explains the stage, and what is left sits on its own row.

Revision 8 called this the legend check: three stacked lines under the Open group naming the
scarlet convention, the active style and what a free or blind run was doing. Revision 9 removed all
three, so this is now the check that they stayed removed — no instruction survives a capture — and
that the rows that remain (the live gap readout) keep clear of each other, of the progress bar and
of the panel's edge. The bar's own scale must still never collide with the n riding the fill.

    packing/.venv/bin/python3 check_legend.py [index.html]
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent

# Revision 12 hides the position bar in Pack, where a corpus-wide scale says nothing about one
# fixed n. A hidden element has a zero rect, so the band it *would* occupy is read off the
# stylesheet instead: the readout is held to the same line whether the bar is drawn or not, which
# is the property that keeps a switch to Sweep from putting the two on top of each other.
BAR_TOP = """(() => { const e = document.getElementById('progress');
     const b = e.getBoundingClientRect();
     return b.height > 0 ? (b.top - s.top) / k : parseFloat(getComputedStyle(e).top); })()"""
RIDER_TOP = """(() => { const e = document.getElementById('p-n');
     const b = e.getBoundingClientRect();
     if (b.height > 0) return (b.top - s.top) / k;
     const bar = document.getElementById('progress');
     return parseFloat(getComputedStyle(bar).top) + parseFloat(getComputedStyle(e).top); })()"""

# The lines revision 9 removed, by id and by the wording each carried. A page that grows any of
# them back fails here rather than in a still nobody looks at twice.
GONE_IDS = ("legend-style", "legend-note", "pair-info")
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


def main() -> int:
    page_path = (HERE / sys.argv[1]) if len(sys.argv) > 1 else HERE / "index.html"
    bad = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.on("pageerror", lambda e: bad.append(f"pageerror: {e}"))
        page.goto(f"file://{page_path}")
        page.wait_for_timeout(700)
        index_of = {q["n"]: q["index"] for q in page.evaluate("atlasTransitions.pairs()")}
        for ident in GONE_IDS:
            if page.evaluate(f"document.getElementById({ident!r}) !== null"):
                bad.append(f"the removed line #{ident} is back in the page")
        if page.evaluate("document.querySelectorAll('.legend').length") != 0:
            bad.append("the legend stack is back on the stage")
        page.evaluate("atlasTransitions.setCapture(true)")
        for n in (100, 110, 307):
            if n not in index_of:
                continue
            for style in ("tween", "physics", "bodies"):
                for mode in ("snap", "free", "blind"):
                    # Both ends of the annealing dial, at rest and in the middle of the move: no
                    # wording anywhere on the stage, and the rows that remain stay on their rows.
                    for level in (3, 10):
                        for at in (2.0, 2.8):
                            page.evaluate(
                                "([i, s, m, L, t]) => { const A = window.atlasTransitions; A.select(i); A.setStyle(s);"
                                " A.setSnap(m !== 'free'); A.setBlind(m === 'blind'); A.setAnneal(L); A.seek(t); }",
                                [index_of[n], style, mode, level, at],
                            )
                            label = f"n={n} {style}/{mode} anneal {level} at {at}"
                            # The stage's whole text, as a viewer would read it off a still.
                            stage_text = page.evaluate(
                                "() => document.getElementById('stage').innerText.replace(/\\s+/g, ' ')"
                            )
                            for word in GONE_WORDS:
                                if word.lower() in stage_text.lower():
                                    bad.append(f"{label}: the stage still says {word!r}")
                            r = page.evaluate(
                                "() => { const s = document.getElementById('stage').getBoundingClientRect();"
                                " const k = s.width / 1920;"
                                " const box = (sel) => { const b = document.querySelector(sel).getBoundingClientRect();"
                                "   return {top: (b.top - s.top) / k, bottom: (b.bottom - s.top) / k, right: (b.right - s.left) / k, text: document.querySelector(sel).textContent}; };"
                                " return {open: box('.open'), d: box('#gap-a'), e: box('#gap-b'),"
                                "  bar: " + BAR_TOP + ","
                                "  pn: " + RIDER_TOP + ","
                                "  right: (document.getElementById('facts').getBoundingClientRect().right - s.left) / k}; }"
                            )
                            lines = [r["d"], r["e"]]
                            if r["open"]["bottom"] > lines[0]["top"] + 0.5:
                                bad.append(f"{label}: the Open group runs into the readout ({r['open']['bottom']:.0f} vs {lines[0]['top']:.0f})")
                            for i in range(len(lines) - 1):
                                if lines[i]["text"] and lines[i + 1]["text"] and lines[i]["bottom"] > lines[i + 1]["top"] + 0.5:
                                    bad.append(f"{label}: readout row {i} (bottom {lines[i]['bottom']:.0f}) overlaps row {i + 1} (top {lines[i + 1]['top']:.0f})")
                            for i, ln in enumerate(lines):
                                if ln["text"] and ln["bottom"] > r["pn"] - 0.5:
                                    bad.append(f"{label}: readout row {i} reaches the progress bar ({ln['bottom']:.0f} vs {r['pn']:.0f}): {ln['text']!r}")
                                if ln["text"] and ln["bottom"] > r["bar"] - 0.5:
                                    bad.append(f"{label}: readout row {i} reaches the bar's band ({ln['bottom']:.0f} vs {r['bar']:.0f})")
                                if ln["text"] and ln["right"] > r["right"] + 0.5:
                                    bad.append(f"{label}: readout row {i} runs past the panel ({ln['right']:.0f} vs {r['right']:.0f})")
        # The two rows an open-ended run adds, at both n the demo carries and every start.
        for n in (17, 100, 307):
            if n not in index_of:
                continue
            for kind in ("grid", "random", "previous"):
                page.evaluate(
                    "([n, k]) => { const A = window.atlasTransitions; A.setStepN(n); A.setInitial(k);"
                    "  if (k === 'previous') { A.optimize(true); A.pause(); } A.optimizeStep(1200); }",
                    [n, kind],
                )
                label = f"optimize n={n} from {kind}"
                stage_text = page.evaluate("() => document.getElementById('stage').innerText.replace(/\\s+/g, ' ')")
                for word in GONE_WORDS:
                    if word.lower() in stage_text.lower():
                        bad.append(f"{label}: the stage still says {word!r}")
                r = page.evaluate(
                    "() => { const s = document.getElementById('stage').getBoundingClientRect();"
                    " const k = s.width / 1920;"
                    " const box = (sel) => { const b = document.querySelector(sel).getBoundingClientRect();"
                    "   return {top: (b.top - s.top) / k, bottom: (b.bottom - s.top) / k, right: (b.right - s.left) / k, text: document.querySelector(sel).textContent}; };"
                    " return {rows: ['#gap-a', '#gap-b', '#gap-c', '#gap-d'].map(box),"
                    "  open: box('.open'),"
                    "  bar: " + BAR_TOP + ","
                    "  right: (document.getElementById('facts').getBoundingClientRect().right - s.left) / k}; }"
                )
                rows = r["rows"]
                if r["open"]["bottom"] > rows[0]["top"] + 0.5:
                    bad.append(f"{label}: the Open group runs into the readout")
                for i, ln in enumerate(rows):
                    if not ln["text"]:
                        continue
                    if ln["bottom"] > r["bar"] - 0.5:
                        bad.append(f"{label}: readout row {i} reaches the bar ({ln['bottom']:.0f}): {ln['text']!r}")
                    if ln["right"] > r["right"] + 0.5:
                        bad.append(f"{label}: readout row {i} runs past the panel ({ln['right']:.0f} vs {r['right']:.0f}): {ln['text']!r}")
                    if i and rows[i - 1]["text"] and rows[i - 1]["bottom"] > ln["top"] + 0.5:
                        bad.append(f"{label}: readout row {i - 1} overlaps row {i}")
                if not rows[2]["text"] or not rows[3]["text"]:
                    bad.append(f"{label}: the run reports nothing: {[q['text'] for q in rows]}")
        page.evaluate("atlasTransitions.setInitial('previous'); atlasTransitions.setCapture(false)")
        # The progress bar's scale (revision 7): at every n the page carries, and at the ends of the
        # sequence, the riding n must not touch a scale numeral and the scale must stay on the stage.
        # Revision 9 makes the scale span the range, so this is the corpus range: the shipped bar.
        page.evaluate(
            "atlasTransitions.setAnneal(3); atlasTransitions.stopAll();"
            " atlasTransitions.setRange(atlasTransitions.range().min, atlasTransitions.range().max)"
        )
        probe = (
            "() => { const s = document.getElementById('stage').getBoundingClientRect();"
            " const k = s.width / 1920;"
            " const box = (el) => { const b = el.getBoundingClientRect();"
            "   return {left: (b.left - s.left) / k, right: (b.right - s.left) / k,"
            "           top: (b.top - s.top) / k, bottom: (b.bottom - s.top) / k, text: el.textContent}; };"
            " const rider = box(document.getElementById('p-n'));"
            " const nums = Array.from(document.querySelectorAll('#p-scale .p-num'))"
            "   .filter(e => getComputedStyle(e).visibility !== 'hidden').map(box);"
            " return {rider, nums, bar: box(document.getElementById('progress')),"
            "         fill: parseFloat(document.getElementById('p-fill').style.width),"
            "         cursor: (document.getElementById('p-cursor').getBoundingClientRect().left - s.left) / k}; }"
        )
        for n, at_end in ((1, False), (100, False), (147, False), (300, False), (323, True)):
            if n not in index_of:
                continue
            page.evaluate(
                "([i, end]) => { const A = window.atlasTransitions; A.setStyle('tween'); A.select(i);"
                " A.seek(end ? A.duration() : 0.2); }",
                [index_of[n], at_end],
            )
            r = page.evaluate(probe)
            label = f"scale at n={r['rider']['text']}"
            for q in r["nums"]:
                if q["left"] < r["rider"]["right"] + 2 and q["right"] > r["rider"]["left"] - 2:
                    bad.append(f"{label}: the riding n overlaps the scale numeral {q['text']!r}")
                if q["left"] < 0 or q["right"] > 1920:
                    bad.append(f"{label}: the scale numeral {q['text']!r} runs off the stage ({q['left']:.0f}..{q['right']:.0f})")
            if r["rider"]["left"] < 0 or r["rider"]["right"] > 1920:
                bad.append(f"{label}: the riding n runs off the stage")
            if r["bar"]["bottom"] > 1080.5:
                bad.append(f"{label}: the bar reaches past the stage ({r['bar']['bottom']:.0f})")
            if len(r["nums"]) < 11:
                bad.append(f"{label}: only {len(r['nums'])} scale numerals are showing")
            # The cursor sits on the fill's leading edge, which is the same pure function of the clock.
            if abs(r["cursor"] - (100 + r["fill"])) > 2.5:
                bad.append(f"{label}: the cursor ({r['cursor']:.1f}) is not on the fill's edge ({100 + r['fill']:.1f})")
        browser.close()
    if bad:
        print("FAILED")
        for b in dict.fromkeys(bad):
            print(" -", b)
        return 1
    print(
        "OK: no legend, style line, miss note, block-matching sentence or key hint anywhere on the "
        "stage over 108 combinations of pair, style, mode, annealing level and instant, nor over an "
        "open-ended run from each of the three starts; the live gap rows and the two an optimize run "
        "adds clear of the Open group, of each other, of the progress bar and of the panel edge; "
        "the bar's scale keeps clear of the riding n and stays on the stage at every n probed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
