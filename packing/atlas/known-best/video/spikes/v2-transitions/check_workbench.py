"""The revision-9 checks: one view, the chooser for n, the range spine, the gap bar.

Everything here is a property of the built page, driven through `window.atlasTransitions` in the
pinned headless shell. It complements `check_revision6.py` (desaturation, snap, blind, continuous
play) and `check_revision7.py` (the bar scale, the annealing dial, the live gap) rather than
repeating them. The workbench needs pairs the 25-pair demo does not carry, so it defaults to the
all-pairs build.

Revision 9 folded revision 8's two tabs into one view: the range is the spine, its two ends are
values of n stepped *into*, and setting them equal is the old Single step tab. So the tab checks
below became checks that the tabs are *gone* and that `setTab` / `tab` survive as no-ops.

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

        # ---- step 1: one view, no tabs.
        api = set(page.evaluate("Object.keys(window.atlasTransitions)"))
        for name in ("setTab", "tab", "setStepN", "stepN", "setRange", "range", "playRange", "gapBar"):
            check(name in api, f"the API lacks {name}")
        # The tab bar and the two tab panels are gone from the page; the API keeps the two calls.
        gone = page.evaluate(
            "() => ['tabbar', 'tab-single', 'tab-sequence', 'panel-single', 'panel-sequence']"
            "  .filter(id => document.getElementById(id) !== null)"
        )
        check(gone == [], f"the tab machinery is still in the page: {gone}")
        check(page.evaluate("document.querySelectorAll('[role=tab], [role=tablist], [role=tabpanel]').length") == 0,
              "the page still carries tab roles")
        check(page.evaluate("atlasTransitions.tab()") == "single", "tab() is not the 'single' no-op")
        check(page.evaluate("atlasTransitions.setTab('sequence')") == "single", "setTab is not a no-op")
        check(page.evaluate("document.getElementById('panel') !== null"), "there is no single control panel")
        # One control set: every setting is reachable without switching anything.
        for ident in ("range-from", "range-to", "range-all", "step-chips", "range-duration",
                      "range-position", "play", "scrub", "style-select", "anneal"):
            check(page.evaluate(f"document.getElementById({ident!r}) !== null"), f"the one view lacks #{ident}")
        # The controls may not push the stage off the window.
        fits = page.evaluate(
            "() => { const s = document.getElementById('stage').getBoundingClientRect();"
            " return {top: s.top, bottom: s.bottom, h: window.innerHeight}; }"
        )
        check(fits["top"] >= -0.5 and fits["bottom"] <= fits["h"] + 0.5,
              f"the stage does not fit above the controls: {fits}")

        # ---- step 2: the chooser for n, which is the range collapsed onto one value.
        check(page.evaluate("atlasTransitions.stepN()") == 17, "the workbench does not open on n = 17")
        opened = page.evaluate("atlasTransitions.range()")
        check(opened["from"] == 17 and opened["to"] == 17 and opened["steps"] == 1,
              f"the workbench does not open on the one-step range 17 to 17: {opened}")
        st = page.evaluate("atlasTransitions.state()")
        check(st["n"] == 16, f"n = 17 does not show the step 16 -> 17 (the pair starts at {st['n']})")
        label = page.evaluate("document.getElementById('step-label').textContent")
        check("16" in label and "17" in label, f"the step label does not name both ends: {label!r}")
        for want in (5, 10, 11, 26, 29, 100, 110, 272):
            got = page.evaluate(f"atlasTransitions.setStepN({want})")
            check(got == want, f"setStepN({want}) landed on {got}")
            check(page.evaluate("atlasTransitions.state().n") == want - 1, f"n = {want} does not show the step {want - 1} -> {want}")
            r = page.evaluate("atlasTransitions.range()")
            check(r["from"] == want and r["to"] == want, f"choosing n = {want} did not set both ends of the range: {r}")
        # A chip is the same thing through the DOM.
        clicked = page.evaluate(
            "() => { document.querySelector('#step-chips button[data-n=\"110\"]').click();"
            "  return atlasTransitions.range(); }"
        )
        check(clicked["from"] == 110 and clicked["to"] == 110, f"a chip does not set both ends: {clicked}")
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

        # ---- step 3: the range spine. Guarded so a page built before this feature reports the
        # missing calls above rather than dying on the first one.
        if not {"setRange", "range", "playRange"} <= api:
            browser.close()
            print("FAILED")
            for failure in dict.fromkeys(failures):
                print(" -", failure)
            print(" - the range and the gap bar were not driven: the API is not there yet")
            return 1
        first = page.evaluate("atlasTransitions.pairs()[0].n + 1")
        last = page.evaluate("atlasTransitions.pairs().slice(-1)[0].n + 1")
        # One click widens the range to the whole corpus.
        page.evaluate("document.getElementById('range-all').click()")
        rng = page.evaluate("atlasTransitions.range()")
        check(rng["from"] == first and rng["to"] == last, f"the corpus button does not widen to {first}..{last}: {rng}")
        check(rng["steps"] == page.evaluate("atlasTransitions.pairs().length"),
              f"the corpus range is {rng['steps']} steps, not every pair the page carries")
        check(rng["duration"] > 60, f"the corpus run's duration reads {rng['duration']}, which is not minutes")
        # The scale spans the range, read from the n it steps from through the n it steps into, so the
        # whole corpus is the shipped 1..324 bar.
        scale = page.evaluate(
            "() => Array.from(document.querySelectorAll('#p-scale .p-num')).map(e => Number(e.textContent))"
        )
        check(scale and scale[0] == first - 1 and scale[-1] == last, f"the corpus scale does not span {first - 1}..{last}: {scale}")
        # Clamped to what the page carries, and to from <= to.
        r = page.evaluate("atlasTransitions.setRange(-10, 100000)")
        check(r["from"] == first and r["to"] == last, f"the range does not clamp to what the page carries: {r}")
        r = page.evaluate("atlasTransitions.setRange(80, 20)")
        check(r["from"] <= r["to"], f"the range allows from > to: {r}")
        # A one-step range is the old Single step tab: the two readouts collapse with it.
        r = page.evaluate("atlasTransitions.setRange(17, 17)")
        check(r["steps"] == 1 and r["from"] == 17 and r["to"] == 17, f"17 to 17 is not one step: {r}")
        check(page.evaluate("atlasTransitions.state().n") == 16, "17 to 17 does not show the step 16 -> 17")
        check(page.evaluate("document.getElementById('range-position').textContent").strip() == "",
              "the position readout is drawn for a one-step range")
        single_scale = page.evaluate(
            "() => Array.from(document.querySelectorAll('#p-scale .p-num')).map(e => Number(e.textContent))"
        )
        check(single_scale == [16, 17], f"a one-step range's scale is {single_scale}, not 16..17")
        # A range of more than one step: the run is scoped to it and both readouts come back.
        r = page.evaluate("atlasTransitions.setRange(2, 100)")
        check(r["steps"] == 99, f"2..100 is {r['steps']} steps, expected 99")
        scale = page.evaluate(
            "() => Array.from(document.querySelectorAll('#p-scale .p-num')).map(e => Number(e.textContent))"
        )
        check(scale and scale[0] == 1 and scale[-1] == 100, f"the bar's scale does not span 1..100: {scale}")
        check(len(scale) >= 5, f"the range scale carries only {len(scale)} numerals")
        page.evaluate("atlasTransitions.setStyle('tween'); atlasTransitions.playRange(); atlasTransitions.pause()")
        check(page.evaluate("atlasTransitions.state().n") == 1, "playRange does not start at the range's first step")
        pos = page.evaluate("atlasTransitions.range()")
        check(pos["step"] == 1, f"the position readout says step {pos['step']} at the start of the run")
        readout = page.evaluate("document.getElementById('range-position').textContent")
        check("1" in readout and "99" in readout, f"the position readout does not read as step k of 99: {readout!r}")
        duration_readout = page.evaluate("document.getElementById('range-duration').textContent")
        check("99 steps" in duration_readout, f"the duration readout does not price 99 steps: {duration_readout!r}")
        page.evaluate("atlasTransitions.goTo(99)")
        check(page.evaluate("atlasTransitions.range().step") == 99, "the last step of 2..100 is not step 99")
        end = page.evaluate(
            """() => { const A = window.atlasTransitions;
              A.setRange(2, 4); A.playRange(); A.pause();
              // Walk the scope by hand: the run must not carry past the range's last pair.
              A.goTo(3); A.seek(A.duration() - 0.001);
              return {n: A.state().n, last: A.range().to}; }"""
        )
        check(end["n"] == 3 and end["last"] == 4, f"the range's last step is not 3 -> 4: {end}")
        page.evaluate("atlasTransitions.stopAll(); atlasTransitions.setRange(17, 17)")

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
        check(geom["shown"], "the gap bar is not drawn")
        check(geom["bottom"] < geom["eyebrow"] - 0.5, f"the gap bar reaches the eyebrow: {geom}")
        check(geom["right"] <= geom["panelRight"] + 0.5, f"the gap bar runs past the panel: {geom}")

        # ---- step 5 (revision 9): the bar stops animating. The sparkline is gone, the hand holds
        # still through the motion, and it catches up when the picture settles.
        check(page.evaluate("document.getElementById('gap-spark') === null"), "the per-frame sparkline is still in the page")
        check("refreshGap" in api, "the API lacks refreshGap")
        # n = 101, not 100: 99 -> 100 is a grid prefix where nothing moves, so the bar would be on the
        # record for the whole step and "it held still" would prove nothing.
        page.evaluate(
            "atlasTransitions.setStepN(101); atlasTransitions.setStyle('bodies');"
            " atlasTransitions.setSnap(false); atlasTransitions.setTiming({dwell: 0.4, move: 2.5, settle: 0.4})"
        )
        page.evaluate(
            """() => { window.__samples = []; const A = window.atlasTransitions;
              A.seek(0); A.play();
              const id = setInterval(() => { const st = A.state();
                window.__samples.push([st.t, A.gapBar().x, document.getElementById('gap-b').textContent]);
                if (!st.playing) clearInterval(id); }, 60); }"""
        )
        page.wait_for_timeout(4500)
        samples = page.evaluate("window.__samples")
        mid = [r for r in samples if 0.6 < r[0] < 2.6]
        check(len(mid) >= 10, f"the run gave only {len(mid)} samples in the middle of the move")
        hands = {round(r[1], 9) for r in mid}
        rows = {r[2] for r in mid}
        check(len(hands) == 1, f"the gap bar's hand moved {len(hands)} times mid-motion: it should hold still")
        check(len(rows) > 5, f"the live readout froze with the bar ({len(rows)} distinct rows over {len(mid)} samples)")
        settled = page.evaluate("atlasTransitions.gapBar().x")
        check(abs(settled - mid[0][1]) > 1e-6, "the bar never caught up once the motion settled")
        # On demand, mid-motion, with nothing else touched.
        held = page.evaluate(
            """() => { const A = window.atlasTransitions; A.pause(); A.seek(1.2);
              const before = A.gapBar().x; A.seek(2.2);
              // A seek marks the bar dirty on purpose, so drive the frame clock instead.
              return {before, after: A.gapBar().x, demand: A.refreshGap().x}; }"""
        )
        check(abs(held["demand"] - held["after"]) < 1e-9, f"refreshGap does not read the current frame: {held}")
        page.evaluate(
            "atlasTransitions.setTiming({dwell: 1.0, move: 1.4, settle: 0.4});"
            " atlasTransitions.setSnap(true); atlasTransitions.setStyle('tween'); atlasTransitions.setStepN(17)"
        )

        # ---- step 6 (revision 9): initial conditions and the open-ended Optimize run.
        for name in ("setInitial", "initial", "optimize", "optimizeState", "optimizeStep", "setSpeed", "speed"):
            check(name in api, f"the API lacks {name}")
        check(page.evaluate("atlasTransitions.initials()") == ["previous", "random", "grid"],
              "the three initial conditions are not previous / random / grid")
        check(page.evaluate("atlasTransitions.initial()") == "previous", "the default start is not the previous packing")
        # The snap checkbox is gone from the page; the call stays on the API.
        check(page.evaluate("document.getElementById('snap-toggle') === null"),
              "the snap-to-best-known checkbox is still a visible control")
        check("setSnap" in api, "setSnap was removed from the API rather than only from the controls")
        check(page.evaluate("document.getElementById('initial-seg') !== null"), "there is no initial-conditions chooser")
        check(page.evaluate("document.getElementById('optimize') !== null"), "there is no Optimize button")
        page.evaluate("atlasTransitions.setStepN(17)")
        record17 = page.evaluate("atlasTransitions.optimizeState(), Number(JSON.parse(document.getElementById('atlas-data').textContent).facts['17'].side)")
        starts = {}
        for kind in ("random", "grid", "previous"):
            page.evaluate(
                "(k) => { const A = window.atlasTransitions; A.setInitial(k);"
                "  if (k === 'previous') { A.optimize(true); A.pause(); } }",
                kind,
            )
            st = page.evaluate("atlasTransitions.optimizeState()")
            starts[kind] = st
            check(st["on"] and st["initial"] == kind, f"the {kind} start did not arm a run: {st}")
            check(st["n"] == 17, f"the {kind} start built {st['n']} squares, not 17")
            check(st["steps"] == 0, f"the {kind} start is already {st['steps']} steps in")
        # Random and grid have no correspondence to the record, so they run without target springs;
        # the previous packing with the blind box off does have one.
        check(not starts["random"]["springs"] and not starts["grid"]["springs"],
              "a random or grid start was given the record's poses to spring at")
        check(starts["previous"]["springs"], "the previous start lost its target springs")
        # The grid start is the trivial grid: axis-aligned, in a box of side ceil(sqrt(n)).
        check(abs(starts["grid"]["side"] - 5) < 1e-9, f"the grid start's box is {starts['grid']['side']}, not 5 for n = 17")
        check(starts["random"]["side"] > record17, "the random start's box is not larger than the record")
        # Random is deterministic: the same n and the same kind give the same arrangement.
        again = page.evaluate(
            "() => { const A = window.atlasTransitions; A.setInitial('previous'); A.setInitial('random');"
            "  return A.optimizeState().required; }"
        )
        check(abs(again - starts["random"]["required"]) < 1e-12,
              f"the random start is not reproducible: {again} vs {starts['random']['required']}")
        # An open-ended run advances state rather than reading a cache, and keeps going.
        run = page.evaluate(
            """() => { const A = window.atlasTransitions; A.setStepN(17); A.setInitial('grid');
              const a = A.optimizeState(); A.optimizeStep(1200);
              const b = A.optimizeState(); A.optimizeStep(1200);
              const c = A.optimizeState(); return {a, b, c}; }"""
        )
        check(run["b"]["steps"] == 1200 and run["c"]["steps"] == 2400, f"the run does not accumulate steps: {run}")
        check(run["c"]["time"] > run["b"]["time"] > 0, f"simulated time does not advance: {run}")
        check(run["c"]["side"] < run["a"]["side"] - 1e-3, f"the walls never closed on the grid start: {run}")
        check(run["c"]["required"] < run["a"]["required"] - 1e-3,
              f"the run made the arrangement no smaller: {run['a']['required']} -> {run['c']['required']}")
        check(run["c"]["best"] is not None and run["c"]["bestPenetration"] is not None,
              f"the run reports no smallest box and no overlap beside it: {run['c']}")
        # And it reports all four figures on the stage.
        rows = page.evaluate("() => [document.getElementById('gap-c').textContent, document.getElementById('gap-d').textContent]")
        check("optimize" in rows[0] and " s " in rows[0] and "steps" in rows[0],
              f"the run does not report its clock and step count: {rows[0]!r}")
        check("smallest box" in rows[1] and "overlap" in rows[1] and "record" in rows[1],
              f"the run does not report its box, its overlap and the record: {rows[1]!r}")
        # Play resumes and pause stops it where it stands.
        held = page.evaluate(
            """() => { const A = window.atlasTransitions; A.setSpeed(1); A.play();
              return {playing: A.state().playing, steps: A.optimizeState().steps}; }"""
        )
        page.wait_for_timeout(700)
        after = page.evaluate("() => { const A = window.atlasTransitions; A.pause(); return A.optimizeState(); }")
        check(held["playing"], "play did not resume the run")
        check(after["steps"] > held["steps"], f"the run did not advance while playing: {held} -> {after}")
        page.wait_for_timeout(300)
        stopped = page.evaluate("atlasTransitions.optimizeState()")
        check(stopped["steps"] == after["steps"], f"the run kept going after pause: {after['steps']} -> {stopped['steps']}")
        # Seeking is how the timeline is come back to.
        page.evaluate("atlasTransitions.seek(0)")
        check(not page.evaluate("atlasTransitions.state().optimizing"), "a seek did not leave the open-ended run")
        check(page.evaluate("document.getElementById('gap-c').textContent") == "",
              "the run's readout survived leaving the run")
        page.evaluate("atlasTransitions.setInitial('previous'); atlasTransitions.setStepN(17)")

        # ---- step 7 (revision 9): the hand.
        for name in ("pickAt", "grab", "dragTo", "release", "hand"):
            check(name in api, f"the API lacks {name}")
        # Grabbing from the timeline hands the picture to an open-ended run seeded where it stood.
        page.evaluate("atlasTransitions.setStepN(17); atlasTransitions.setStyle('tween'); atlasTransitions.seek(0)")
        grabbed = page.evaluate(
            """() => { const A = window.atlasTransitions;
              const before = A.state().optimizing;
              const i = A.pickAt(2.5, 2.5);
              const g = A.grab(i, 2.5, 2.5);
              return {before, i, g, optimizing: A.state().optimizing, edited: A.hand().edited}; }"""
        )
        check(grabbed["i"] >= 0, "nothing was picked at the middle of the packing")
        check(grabbed["g"] == grabbed["i"] and not grabbed["before"] and grabbed["optimizing"],
              f"a grab from the timeline did not start an open-ended run: {grabbed}")
        check(grabbed["edited"], "a dragged run is not marked hand-edited")
        check("hand-edited" in page.evaluate("document.getElementById('gap-c').textContent"),
              "the stage does not say the run was hand-edited")
        page.evaluate("atlasTransitions.release()")
        # Pinned: the held square follows the cursor exactly and its neighbours are pushed aside.
        pin = page.evaluate(
            """() => { const A = window.atlasTransitions;
              A.setStepN(17); A.setInitial('grid'); A.optimizeStep(400);
              const i = A.pickAt(0.5, 0.5);
              A.grab(i, 0.5, 0.5);
              A.dragTo(1.2, 0.5, false);
              const neighbour = A.pickAt(1.9, 0.5);
              A.optimizeStep(300);
              const out = {i, held: A.hand().held, stillThere: A.pickAt(1.2, 0.5) === i,
                           neighbourMoved: A.pickAt(1.9, 0.5) !== neighbour};
              out.dropped = A.release();
              out.after = A.hand().held;
              return out; }"""
        )
        check(pin["held"] == pin["i"], f"the square was not held through the drag: {pin}")
        check(pin["stillThere"], "the held square did not stay exactly where the cursor left it")
        check(pin["neighbourMoved"], "the run did not push the held square's neighbour aside")
        check(pin["after"] == -1, "the square was not dropped on release")
        # Shift turns it about its own centre.
        turn = page.evaluate(
            """() => { const A = window.atlasTransitions;
              A.setStepN(17); A.setInitial('grid');
              const j = A.pickAt(0.5, 0.5);
              A.grab(j, 1.0, 0.5);
              const a = A.dragTo(1.0, 0.5, true);
              const b = A.dragTo(0.5, 1.0, true);
              A.release();
              return {a, b}; }"""
        )
        check(abs(turn["a"]["angle"]) < 1e-6, f"the first shifted move already turned the square: {turn['a']}")
        check(abs(turn["b"]["angle"] - 90) < 1e-6, f"a quarter turn of the cursor did not turn it 90 degrees: {turn['b']}")
        check(abs(turn["b"]["x"] - turn["a"]["x"]) < 1e-9 and abs(turn["b"]["y"] - turn["a"]["y"]) < 1e-9,
              f"a shifted drag moved the square's centre: {turn}")
        # The readout follows the drag at once.
        moved = page.evaluate(
            """() => { const A = window.atlasTransitions;
              A.setStepN(17); A.setInitial('grid');
              const before = document.getElementById('gap-b').textContent;
              const k = A.pickAt(0.5, 0.5);
              A.grab(k, 0.5, 0.5); A.dragTo(7.5, 0.5, false);
              const after = document.getElementById('gap-b').textContent;
              A.release();
              return {before, after}; }"""
        )
        check(moved["before"] != moved["after"], f"the live readout did not follow the drag: {moved}")
        # And a drag while a run is playing leaves it playing.
        live = page.evaluate(
            """() => { const A = window.atlasTransitions;
              A.setInitial('previous'); A.setStepN(17); A.seek(0); A.play();
              const m = A.pickAt(2.5, 2.5); A.grab(m, 2.5, 2.5);
              const out = {held: A.hand().held, playing: A.state().playing, optimizing: A.state().optimizing};
              A.release(); A.pause(); return out; }"""
        )
        check(live["held"] >= 0 and live["playing"] and live["optimizing"],
              f"a grab during playback did not carry on running: {live}")
        # No keyboard control regressed.
        page.evaluate("atlasTransitions.setInitial('previous'); atlasTransitions.setStepN(17); atlasTransitions.seek(0)")
        page.keyboard.press("ArrowRight")
        check(page.evaluate("atlasTransitions.stepN()") == 18, "the right arrow no longer steps n")
        page.keyboard.press("ArrowLeft")
        check(page.evaluate("atlasTransitions.stepN()") == 17, "the left arrow no longer steps n")
        page.keyboard.press("p")
        check(page.evaluate("atlasTransitions.state().style") == "physics", "the p key no longer cycles the style")
        page.keyboard.press("p")
        page.keyboard.press("p")
        page.keyboard.press(" ")
        check(page.evaluate("atlasTransitions.state().playing"), "the space bar no longer plays")
        page.keyboard.press(" ")
        check(not page.evaluate("atlasTransitions.state().playing"), "the space bar no longer pauses")
        browser.close()

    if failures:
        print("FAILED")
        for failure in dict.fromkeys(failures):
            print(" -", failure)
        return 1
    print(
        "OK: one view with no tab machinery left and setTab/tab surviving as no-ops, every control in "
        "one panel and the stage still fitting; the chooser opening on n = 17 as the one-step range 17 "
        "to 17, nine quick picks each setting both ends, clamped both ways; the range widening to the "
        "whole corpus in one click, clamped, collapsing to one step, and scoping the run and the bar's "
        "scale; the gap bar reading the panel's own s(n) bounds, sweeping to the record under style A, "
        "missing under a free run, alive in blind mode, and clear of the eyebrow and the panel edge; "
        "the bar holding still through the motion and catching up when it settles, with the per-frame "
        "sparkline gone and refreshGap redrawing it on demand; three initial conditions, the random "
        "one reproducible and the grid one the trivial grid, an open-ended run that accumulates "
        "steps, closes the walls, reports its box beside its overlap, and resumes and stops with the "
        "transport, with the snap checkbox gone from the page and setSnap still on the API; and a "
        "hand that picks the topmost square, pins it against its neighbours, turns it on shift, "
        "moves the readout as it goes, marks the run hand-edited and regresses no key."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
