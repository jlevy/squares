"""The revision-8 checks: the two tabs, the single-step chooser, the sequence range, the gap bar.

Everything here is a property of the built page, driven through `window.atlasTransitions` in the
pinned headless shell. It complements `check_revision6.py` (desaturation, snap, blind, continuous
play) and `check_revision7.py` (the bar scale, the annealing dial, the live gap) rather than
repeating them. The workbench needs pairs the 25-pair demo does not carry, so it defaults to the
all-pairs build.

    packing/.venv/bin/python3 check_workbench.py [workbench.html]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent


def main() -> int:
    page_path = (HERE / sys.argv[1]) if len(sys.argv) > 1 else HERE / "workbench.html"
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.on("console", lambda m: failures.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: failures.append(f"pageerror: {e}"))
        page.goto(f"file://{page_path}")
        page.wait_for_timeout(900)

        # ---- step 1: the shell and the two tabs.
        api = set(page.evaluate("Object.keys(window.atlasTransitions)"))
        for name in ("setTab", "tab", "setStepN", "stepN", "setRange", "range", "playRange", "gapBar"):
            check(name in api, f"the API lacks {name}")
        check(page.evaluate("atlasTransitions.tab()") == "single", "the workbench does not open on the single-step tab")
        aria = page.evaluate(
            "() => ({single: document.getElementById('tab-single').getAttribute('aria-selected'),"
            "  sequence: document.getElementById('tab-sequence').getAttribute('aria-selected'),"
            "  panelSingle: !document.getElementById('panel-single').hidden,"
            "  panelSeq: !document.getElementById('panel-sequence').hidden,"
            "  tabbable: Array.from(document.querySelectorAll('#tabbar .tab')).map(b => b.tabIndex)})"
        )
        check(aria["single"] == "true" and aria["sequence"] == "false", f"aria-selected is wrong on open: {aria}")
        check(aria["panelSingle"] and not aria["panelSeq"], f"the wrong panel is showing on open: {aria}")
        check(0 in aria["tabbable"], "no tab is reachable by keyboard")
        # The active tab is visually obvious: it takes the paper ground the inactive one does not.
        colours = page.evaluate(
            "() => ({on: getComputedStyle(document.getElementById('tab-single')).backgroundColor,"
            "  off: getComputedStyle(document.getElementById('tab-sequence')).backgroundColor,"
            "  onInk: getComputedStyle(document.getElementById('tab-single')).color,"
            "  offInk: getComputedStyle(document.getElementById('tab-sequence')).color})"
        )
        check(colours["on"] != colours["off"], f"the two tabs share a background: {colours}")
        check(colours["onInk"] != colours["offInk"], f"the two tabs share an ink colour: {colours}")
        # The `t` key toggles, and a switch keeps every global setting.
        page.evaluate("atlasTransitions.setStyle('bodies'); atlasTransitions.setAnneal(7); atlasTransitions.setSnap(false)")
        before = page.evaluate("atlasTransitions.state()")
        page.keyboard.press("t")
        check(page.evaluate("atlasTransitions.tab()") == "sequence", "the t key does not switch to the sequence tab")
        after = page.evaluate("atlasTransitions.state()")
        for key in ("style", "anneal", "snap", "blind", "desaturate", "rule", "phase", "links", "timing"):
            check(before[key] == after[key], f"the {key} setting did not survive the tab switch: {before[key]} -> {after[key]}")
        seq_aria = page.evaluate(
            "() => ({single: document.getElementById('tab-single').getAttribute('aria-selected'),"
            "  sequence: document.getElementById('tab-sequence').getAttribute('aria-selected'),"
            "  panelSingle: !document.getElementById('panel-single').hidden,"
            "  panelSeq: !document.getElementById('panel-sequence').hidden})"
        )
        check(seq_aria["sequence"] == "true" and seq_aria["single"] == "false", f"aria-selected did not follow the switch: {seq_aria}")
        check(seq_aria["panelSeq"] and not seq_aria["panelSingle"], f"the panels did not follow the switch: {seq_aria}")
        page.keyboard.press("t")
        check(page.evaluate("atlasTransitions.tab()") == "single", "the t key does not switch back")
        page.evaluate("atlasTransitions.setStyle('tween'); atlasTransitions.setAnneal(3); atlasTransitions.setSnap(true)")
        # The tab bar is chrome: capture preview leaves the stage alone.
        page.evaluate("atlasTransitions.setCapture(true)")
        check(page.evaluate("getComputedStyle(document.getElementById('tabbar')).display") == "none",
              "the tab bar is still drawn in capture preview")
        page.evaluate("atlasTransitions.setCapture(false)")
        # Neither the tab bar nor the controls may push the stage off the window.
        fits = page.evaluate(
            "() => { const s = document.getElementById('stage').getBoundingClientRect();"
            " return {top: s.top, bottom: s.bottom, h: window.innerHeight}; }"
        )
        check(fits["top"] >= -0.5 and fits["bottom"] <= fits["h"] + 0.5,
              f"the stage does not fit between the tab bar and the controls: {fits}")

        # ---- step 2: the single-step chooser.
        check(page.evaluate("atlasTransitions.stepN()") == 17, "the single-step tab does not default to n = 17")
        st = page.evaluate("atlasTransitions.state()")
        check(st["n"] == 16, f"n = 17 does not show the step 16 -> 17 (the pair starts at {st['n']})")
        label = page.evaluate("document.getElementById('step-label').textContent")
        check("16" in label and "17" in label, f"the step label does not name both ends: {label!r}")
        for want in (5, 10, 11, 26, 29, 100, 110, 272):
            got = page.evaluate(f"atlasTransitions.setStepN({want})")
            check(got == want, f"setStepN({want}) landed on {got}")
            check(page.evaluate("atlasTransitions.state().n") == want - 1, f"n = {want} does not show the step {want - 1} -> {want}")
        chips = page.evaluate("Array.from(document.querySelectorAll('#step-chips button')).map(b => Number(b.dataset.n))")
        check(chips == [5, 10, 11, 17, 26, 29, 100, 110, 272], f"the quick-pick chips are {chips}")
        lo = page.evaluate("atlasTransitions.setStepN(-40)")
        hi = page.evaluate("atlasTransitions.setStepN(100000)")
        check(lo == page.evaluate("atlasTransitions.pairs()[0].n + 1"), f"the chooser does not clamp low (got {lo})")
        check(hi == page.evaluate("atlasTransitions.pairs().slice(-1)[0].n + 1"), f"the chooser does not clamp high (got {hi})")
        page.evaluate("atlasTransitions.setStepN(17)")
        note = page.evaluate("document.getElementById('step-note').textContent")
        check("whole-configuration" in note or "whole configuration" in note,
              f"the n = 17 note does not say what makes 17 worth playing with: {note!r}")

        # ---- step 3: the sequence range. Guarded so a page built before this feature reports the
        # missing calls above rather than dying on the first one.
        if not {"setRange", "range", "playRange"} <= api:
            browser.close()
            print("FAILED")
            for failure in dict.fromkeys(failures):
                print(" -", failure)
            print(" - the sequence range and the gap bar were not driven: the API is not there yet")
            return 1
        page.evaluate("atlasTransitions.setTab('sequence')")
        rng = page.evaluate("atlasTransitions.range()")
        check(rng["from"] == 1 and rng["to"] == 100, f"the sequence range does not default to 1..100: {rng}")
        check(rng["steps"] == 99, f"1..100 is {rng['steps']} steps, expected 99")
        check(rng["duration"] > 60, f"the run's duration reads {rng['duration']}, which is not a couple of minutes")
        # Clamped to the embedded range and to from < to.
        first = page.evaluate("atlasTransitions.pairs()[0].n")
        last = page.evaluate("atlasTransitions.pairs().slice(-1)[0].n + 1")
        r = page.evaluate("atlasTransitions.setRange(-10, 100000)")
        check(r["from"] == first and r["to"] == last, f"the range does not clamp to what the page carries: {r}")
        r = page.evaluate("atlasTransitions.setRange(80, 20)")
        check(r["from"] < r["to"], f"the range allows from >= to: {r}")
        r = page.evaluate("atlasTransitions.setRange(1, 100)")
        # The bar's scale spans the range, not 1..324.
        scale = page.evaluate(
            "() => Array.from(document.querySelectorAll('#p-scale .p-num')).map(e => Number(e.textContent))"
        )
        check(scale and scale[0] == 1 and scale[-1] == 100, f"the bar's scale does not span 1..100: {scale}")
        check(len(scale) >= 5, f"the range scale carries only {len(scale)} numerals")
        # The run is scoped: it starts at the range's first step and stops at its last.
        page.evaluate("atlasTransitions.setStyle('tween'); atlasTransitions.playRange(); atlasTransitions.pause()")
        check(page.evaluate("atlasTransitions.state().n") == 1, "playRange does not start at the range's first step")
        pos = page.evaluate("atlasTransitions.range()")
        check(pos["step"] == 1, f"the position readout says step {pos['step']} at the start of the run")
        readout = page.evaluate("document.getElementById('range-position').textContent")
        check("1" in readout and "99" in readout, f"the position readout does not read as step k of 99: {readout!r}")
        page.evaluate("atlasTransitions.goTo(99)")
        check(page.evaluate("atlasTransitions.range().step") == 99, "the last step of 1..100 is not step 99")
        end = page.evaluate(
            """() => { const A = window.atlasTransitions;
              A.setRange(1, 4); A.playRange(); A.pause();
              // Walk the scope by hand: the run must not carry past the range's last pair.
              A.goTo(3); A.seek(A.duration() - 0.001);
              return {n: A.state().n, last: A.range().to}; }"""
        )
        check(end["n"] == 3 and end["last"] == 4, f"the range's last step is not 3 -> 4: {end}")
        page.evaluate("atlasTransitions.setRange(1, 100); atlasTransitions.stopAll(); atlasTransitions.setTab('single')")

        # ---- step 4: the gap bar. Guarded the same way as step 3.
        if "gapBar" not in api:
            browser.close()
            print("FAILED")
            for failure in dict.fromkeys(failures):
                print(" -", failure)
            print(" - the gap bar was not driven: gapBar is not on the API yet")
            return 1
        page.evaluate("atlasTransitions.setStepN(17); atlasTransitions.setStyle('tween'); atlasTransitions.seek(0)")
        bar = page.evaluate("atlasTransitions.gapBar()")
        facts = page.evaluate("() => JSON.parse(document.getElementById('atlas-data').textContent).facts['17']")
        check(abs(bar["record"] - float(facts["side"])) < 1e-9,
              f"the bar's record {bar['record']} is not the panel's s(17) <= {facts['side']}")
        check(abs(bar["lower"] - float(facts["lower"])) < 1e-9,
              f"the bar's lower bound {bar['lower']} is not the panel's s(17) >= {facts['lower']}")
        check(bar["lo"] <= bar["lower"] + 1e-9, f"the bar's scale starts above the lower bound: {bar}")
        check(bar["hi"] > bar["record"], f"the bar's scale does not reach past the record: {bar}")
        # Under style A the indicator sweeps to the record and the check turns green.
        page.evaluate("atlasTransitions.seek(atlasTransitions.duration())")
        end_bar = page.evaluate("atlasTransitions.gapBar()")
        check(end_bar["met"], f"style A does not reach the record by the end of the step: {end_bar}")
        check(abs(end_bar["excess"]) < 0.05, f"the excess at rest is {end_bar['excess']} per cent")
        tick_colour = page.evaluate("getComputedStyle(document.getElementById('gapbar-check')).fill")
        page.evaluate("atlasTransitions.setStyle('bodies'); atlasTransitions.setSnap(false); atlasTransitions.seek(2.0)")
        mid = page.evaluate("atlasTransitions.gapBar()")
        check(not mid["met"], f"the check reads met in the middle of a free run: {mid}")
        mid_colour = page.evaluate("getComputedStyle(document.getElementById('gapbar-check')).fill")
        check(tick_colour != mid_colour, f"the check does not change colour when the record is met ({tick_colour})")
        check(0 <= mid["x"] <= 1, f"the indicator is off the bar: {mid}")
        # In blind mode the bar still means something: the side comparison is all it needs.
        page.evaluate("atlasTransitions.setBlind(true); atlasTransitions.seek(2.0)")
        blind = page.evaluate("atlasTransitions.gapBar()")
        check(blind["side"] > 0 and 0 <= blind["x"] <= 1, f"the bar loses its indicator in blind mode: {blind}")
        page.evaluate("atlasTransitions.setBlind(false); atlasTransitions.setSnap(true); atlasTransitions.setStyle('tween')")
        # The bar is the single-step tab's, and it must never reach the eyebrow below it.
        geom = page.evaluate(
            "() => { const s = document.getElementById('stage').getBoundingClientRect();"
            " const k = s.width / 1920;"
            " const b = document.getElementById('gapbar').getBoundingClientRect();"
            " const e = document.querySelector('.eyebrow').getBoundingClientRect();"
            " const f = document.getElementById('facts').getBoundingClientRect();"
            " return {bottom: (b.bottom - s.top) / k, top: (b.top - s.top) / k,"
            "         eyebrow: (e.top - s.top) / k, right: (b.right - s.left) / k,"
            "         panelRight: (f.right - s.left) / k,"
            "         shown: getComputedStyle(document.getElementById('gapbar')).display !== 'none'}; }"
        )
        # The bar's own geometry: the shaded open span is a band inside the track, from the lower
        # bound's tick to the record's, and the two numbers do not sit on each other. (The band was
        # 76 px tall on its first build: `height` is a CSS property on an SVG rect, and the class
        # name it had then was the panel's own `.open` slot.)
        parts = page.evaluate(
            "() => { const s = document.getElementById('stage').getBoundingClientRect();"
            " const k = s.width / 1920;"
            " const box = (sel) => { const b = document.querySelector(sel).getBoundingClientRect();"
            "   return {l: (b.left - s.left) / k, r: (b.right - s.left) / k,"
            "           t: (b.top - s.top) / k, b: (b.bottom - s.top) / k}; };"
            " return {track: box('.gapbar-plot .track'), open: box('#gapbar-open'),"
            "         rec: box('#gapbar-record'), low: box('#gapbar-lower'),"
            "         lowLabel: box('#gapbar-lower-label'), recLabel: box('#gapbar-record-label')}; }"
        )
        check(parts["open"]["t"] >= parts["track"]["t"] - 0.5 and parts["open"]["b"] <= parts["track"]["b"] + 0.5,
              f"the shaded open span is not a band inside the track: {parts['open']} against {parts['track']}")
        check(parts["open"]["l"] <= parts["low"]["l"] + 1.5 and abs(parts["open"]["r"] - parts["rec"]["l"]) < 2.5,
              f"the shaded span does not run from the lower bound to the record: {parts}")
        check(parts["lowLabel"]["r"] < parts["recLabel"]["l"] - 0.5,
              f"the bar's two numbers overlap: {parts['lowLabel']} and {parts['recLabel']}")
        check(geom["shown"], "the gap bar is not drawn on the single-step tab")
        check(geom["bottom"] < geom["eyebrow"] - 0.5, f"the gap bar reaches the eyebrow: {geom}")
        check(geom["right"] <= geom["panelRight"] + 0.5, f"the gap bar runs past the panel: {geom}")
        page.evaluate("atlasTransitions.setTab('sequence')")
        check(page.evaluate("getComputedStyle(document.getElementById('gapbar')).display") == "none",
              "the gap bar is still drawn on the sequence tab")
        page.evaluate("atlasTransitions.setTab('single')")
        browser.close()

    if failures:
        print("FAILED")
        for failure in dict.fromkeys(failures):
            print(" -", failure)
        return 1
    print(
        "OK: two tabs with the right aria and a visible active state, t toggling them and every look "
        "and timing setting surviving the switch, the bar hidden in capture preview and the stage still "
        "fitting; the chooser defaulting to n = 17 on the step 16 -> 17, nine quick picks, clamped both "
        "ways; the range defaulting to 1..100 = 99 steps, clamped, scoping the run and the bar's scale; "
        "the gap bar reading the panel's own s(n) bounds, sweeping to the record under style A, missing "
        "under a free run, alive in blind mode, and clear of the eyebrow and the panel edge."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
