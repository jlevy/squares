"""The panel's stacked lines must sit on their own rows and end above the progress bar, and the
bar's own scale must never collide with the n riding the fill's leading edge.

    packing/.venv/bin/python3 check_legend.py [index.html]
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent


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
        page.evaluate("atlasTransitions.setCapture(true)")
        for n in (100, 110, 307):
            if n not in index_of:
                continue
            for style in ("tween", "physics", "bodies"):
                for mode in ("snap", "free", "blind"):
                    # Both ends of the annealing dial: away from the default level the style line
                    # carries the level too, and it still has to fit on its own row.
                    for level in (3, 10):
                        page.evaluate(
                            "([i, s, m, L]) => { const A = window.atlasTransitions; A.select(i); A.setStyle(s);"
                            " A.setSnap(m !== 'free'); A.setBlind(m === 'blind'); A.setAnneal(L); A.seek(2.8); }",
                            [index_of[n], style, mode, level],
                        )
                        r = page.evaluate(
                            "() => { const s = document.getElementById('stage').getBoundingClientRect();"
                            " const k = s.width / 1920;"
                            " const box = (sel) => { const b = document.querySelector(sel).getBoundingClientRect();"
                            "   return {top: (b.top - s.top) / k, bottom: (b.bottom - s.top) / k, right: (b.right - s.left) / k, text: document.querySelector(sel).textContent}; };"
                            " return {a: box('.legend:not(.legend-style):not(.legend-note)'), b: box('#legend-style'), c: box('#legend-note'),"
                            "  d: box('#gap-a'), e: box('#gap-b'),"
                            "  spark: (document.getElementById('gap-spark').getBoundingClientRect().left - s.left) / k,"
                            "  sparkShown: getComputedStyle(document.getElementById('gap-spark')).visibility !== 'hidden',"
                            "  bar: (document.getElementById('progress').getBoundingClientRect().top - s.top) / k,"
                            "  pn: (document.getElementById('p-n').getBoundingClientRect().top - s.top) / k,"
                            "  right: (document.getElementById('facts').getBoundingClientRect().right - s.left) / k}; }"
                        )
                        label = f"n={n} {style}/{mode} anneal {level}"
                        # The whole stack: three legend lines then the two live-gap rows.
                        lines = [r["a"], r["b"], r["c"], r["d"], r["e"]]
                        if r["sparkShown"] and r["d"]["right"] > r["spark"] - 6:
                            bad.append(f"{label}: the gap line runs into the trace ({r['d']['right']:.0f} vs {r['spark']:.0f}): {r['d']['text']!r}")
                        for ln in lines:
                            if ln["text"] and ln["bottom"] > r["bar"] - 0.5:
                                bad.append(f"{label}: a panel row reaches the progress bar ({ln['bottom']:.0f} vs {r['bar']:.0f}): {ln['text']!r}")
                        for i in range(len(lines) - 1):
                            if lines[i]["text"] and lines[i + 1]["text"] and lines[i]["bottom"] > lines[i + 1]["top"] + 0.5:
                                bad.append(f"{label}: legend line {i} (bottom {lines[i]['bottom']:.0f}) overlaps line {i + 1} (top {lines[i + 1]['top']:.0f}): {lines[i]['text']!r}")
                        for i, ln in enumerate(lines):
                            if ln["text"] and ln["bottom"] > r["pn"] - 0.5:
                                bad.append(f"{label}: legend line {i} reaches the progress bar ({ln['bottom']:.0f} vs {r['pn']:.0f}): {ln['text']!r}")
                            if ln["text"] and ln["right"] > r["right"] + 0.5:
                                bad.append(f"{label}: legend line {i} runs past the panel ({ln['right']:.0f} vs {r['right']:.0f})")
        # The progress bar's scale (revision 7): at every n the page carries, and at the ends of the
        # sequence, the riding n must not touch a scale numeral and the scale must stay on the stage.
        page.evaluate("atlasTransitions.setAnneal(3); atlasTransitions.stopAll()")
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
        "OK: three legend lines and the two live-gap rows, no overlap, clear of the trace, the progress bar "
        "and the panel edge, over 54 combinations "
        "of pair, style, mode and annealing level; "
        "the bar's scale keeps clear of the riding n and stays on the stage at every n probed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
