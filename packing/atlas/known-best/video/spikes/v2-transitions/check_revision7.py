"""The revision-7 checks: the bar's scale, the annealing dial, and the live gap to the record.

Everything here is a property of the built page, driven through `window.atlasTransitions` in
the pinned headless shell. It complements `check_revision6.py` (the earlier features),
`check_legend.py` (where the panel's rows and the bar's scale must sit) and `smoke_styles.py`
(the two physical styles).

    packing/.venv/bin/python3 check_revision7.py [index.html]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent

# What revision 6 measured at the default annealing, from NOTES.md: the default level has to be
# the shipped simulation to the last digit, or every earlier measurement has quietly moved.
#: What a FREE run -- no snap, so the simulation's own answer -- misses the record by, as centre
#: distance, angle in degrees, and the side it comes to rest at.
#:
#: These were revision 6's numbers and they have moved, because revision 16 added a tightening
#: window before the lock-in: between the push-apart fading and the blend beginning, the spring
#: toward the target stiffens, with its damping scaled to match. The point of that phase was to stop
#: the picture jumping into place at the end, and its effect here is the same effect measured from
#: the other side. Recorded before and after:
#:
#:     physics 100   1.149 / 42.96 / 10.619   ->   0.001 / 0.03 / 10.536
#:     bodies  100   1.244 / 43.04 / 10.621   ->   0.000 / 0.02 / 10.536
#:     physics 110   1.540 / 16.87 / 11.116   ->   0.001 / 0.00 / 11.000
#:     bodies  110   1.706 / 28.33 / 11.074   ->   0.372 / 2.63 / 11.198
#:
#: Three of the four now land essentially on the record without the snap at all. The fourth, bodies
#: at 110, is the style whose whole point is a louder shake, and it still misses -- which is the
#: honest result rather than a tuned one.
FREE_MISS = {
    ("physics", 100): (0.001, 0.03, 10.536),
    ("bodies", 100): (0.000, 0.02, 10.536),
    ("physics", 110): (0.001, 0.00, 11.000),
    ("bodies", 110): (0.372, 2.63, 11.198),
}


def main() -> int:
    page_path = (HERE / sys.argv[1]) if len(sys.argv) > 1 else HERE / "index.html"
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
        api = set(page.evaluate("Object.keys(window.atlasTransitions)"))
        for name in ("setAnneal", "anneal"):
            check(name in api, f"the API lacks {name}")
        index_of = {q["n"]: q["index"] for q in page.evaluate("atlasTransitions.pairs()")}
        n = 100 if 100 in index_of else sorted(index_of)[len(index_of) // 2]
        n_max = page.evaluate("atlasTransitions.pairs().slice(-1)[0].n") + 1

        # ---- feature 1: where the sequence stands, as a number.
        # Revision 7 drew this as a bar with a scale along the bottom of the stage, and most of this
        # section measured that drawing: the numerals it laid out, the ticks between them, the fill's
        # width, and the riding n suppressing whichever numeral it would touch. Revision 16 removed
        # the whole band -- the owner found it distracting, and the stage carries facts about the
        # packing rather than apparatus about the playback -- so what is left to check is the number
        # it was drawing, which `progress()` still reports and the transport still uses.
        # Checked as properties rather than against a formula, which would only restate the page's
        # own arithmetic: it starts at nothing, ends at everything, and never goes backwards.
        page.evaluate("atlasTransitions.setRange(atlasTransitions.range().min, atlasTransitions.range().max)")
        walk = page.evaluate(
            """() => { const A = window.atlasTransitions; const out = [];
              const pairs = A.pairs();
              for (const i of [0, Math.floor(pairs.length / 2), pairs.length - 1]) {
                A.select(i);
                for (const u of [0, 0.5, 1]) { A.seek(A.duration() * u); out.push(A.progress().position); }
              }
              return out; }"""
        )
        check(abs(walk[0]) < 1e-9, f"the first step does not start the sequence at 0: {walk[0]}")
        check(abs(walk[-1] - 1) < 1e-9, f"the last step does not end the sequence at 1: {walk[-1]}")
        check(all(b >= a - 1e-12 for a, b in zip(walk, walk[1:], strict=False)),
              f"the sequence's position goes backwards: {walk}")
        check(page.evaluate("document.getElementById('progress') === null"),
              "the position bar is still in the page")

        # ---- feature 2: the annealing dial.
        a = page.evaluate("atlasTransitions.anneal()")
        check((a["level"], a["min"], a["max"], a["dflt"]) == (3, 0, 10, 3), f"the dial reports {a}")
        check(abs(a["amplitude"] - 1) < 1e-12 and abs(a["span"] - 1) < 1e-12, "the default level is not the shipped shake")
        levels = page.evaluate(
            """([i]) => {
              const A = window.atlasTransitions;
              A.setStyle('bodies'); A.setSnap(false); A.setBlind(false);
              const out = {};
              for (const L of [0, 3, 6, 10]) {
                A.setAnneal(L);
                const a = A.anneal(), r = A.physics(i, 'bodies', 'free');
                out[L] = {amp: a.amplitude, decay: a.decayPower, span: a.span, steps: r.steps,
                          move: a.move, miss: r.miss, first: r.final[0]};
              }
              A.setAnneal(3);
              return out;
            }""",
            [index_of[n]],
        )
        check(abs(levels["0"]["amp"]) < 1e-12, "level 0 still shakes")
        check(abs(levels["10"]["amp"] - 3) < 1e-9, f"level 10's amplitude is {levels['10']['amp']}, not three times the default")
        check(levels["0"]["steps"] == levels["3"]["steps"], "level 0 does not run the default length")
        check(levels["10"]["steps"] > levels["3"]["steps"] * 1.6, f"level 10 runs {levels['10']['steps']} steps against {levels['3']['steps']}")
        check(abs(levels["10"]["move"] / levels["3"]["move"] - 1.7) < 1e-6, "the move on the clock does not lengthen with the run")
        # 120 steps a second of the annealed move at every level: the sub-steps are at the same dt.
        for L in ("0", "3", "6", "10"):
            check(abs(levels[L]["steps"] / levels[L]["move"] - 120) < 0.5, f"level {L} runs {levels[L]['steps']} steps over {levels[L]['move']} s")
        check(levels["0"]["first"] != levels["3"]["first"], "level 0 and level 3 give the same trajectory")
        check(levels["10"]["first"] != levels["3"]["first"], "level 10 and level 3 give the same trajectory")
        # Deterministic, and cached per level rather than per anything else.
        det = page.evaluate(
            "([i]) => { const A = window.atlasTransitions; A.setAnneal(7); const a = A.physics(i, 'bodies', 'free').final[0];"
            " A.setAnneal(2); A.physics(i, 'bodies', 'free'); A.setAnneal(7);"
            " const b = A.physics(i, 'bodies', 'free').final[0]; A.setAnneal(3); return [a, b]; }",
            [index_of[n]],
        )
        check(det[0] == det[1], "the same annealing level does not reproduce its trajectory")
        # The default reproduces the recorded free-run misses to the digits above.
        for (style, pair_n), (centre, angle, side) in FREE_MISS.items():
            if pair_n not in index_of:
                continue
            m = page.evaluate(
                "([i, s]) => window.atlasTransitions.physics(i, s, 'free').miss",
                [index_of[pair_n], style],
            )
            check(abs(m["centre"] - centre) < 5e-4 and abs(m["angle"] - angle) < 5e-3 and abs(m["side"] - side) < 5e-4,
                  f"at the default level {style} {pair_n} misses by {m['centre']:.3f}/{m['angle']:.2f}/{m['side']:.3f}, "
                  f"not the recorded {centre}/{angle}/{side}")
        # The dial works under the snap and under the blind run too.
        for mode in ("snap", "blind"):
            r = page.evaluate(
                "([i, m]) => { const A = window.atlasTransitions; A.setAnneal(9);"
                " const r = A.physics(i, 'physics', m); A.setAnneal(3); return {miss: r.miss, steps: r.steps}; }",
                [index_of[n], mode],
            )
            # The step count is `stepsPerSecond x move x span`, so it moved with the beat: revision
            # 16 made the move 0.8 s where it was 1.4, which is 154 steps at level 9's span rather
            # than the 200-odd this was written against. What the dial has to do is lengthen the run,
            # and that is what is checked -- against the same run at the default level, not against a
            # number that a change to the beat invalidates.
            base = page.evaluate(
                "([i, m]) => { const A = window.atlasTransitions; A.setAnneal(3);"
                " return A.physics(i, 'physics', m).steps; }",
                [index_of[n], mode],
            )
            check(r["steps"] > base, f"{mode} at level 9 runs {r['steps']} steps, no more than the default's {base}")
            if mode == "snap":
                check(r["miss"]["centre"] < 1e-9, "a snapped run at level 9 does not end on the record")
            else:
                check(r["miss"]["excess"] > -0.001, "a blind run at level 9 beat the record")

        # ---- feature 3: the live gap, at all times.
        # Revision 7 printed this as rows under the stage and most of this section read their text.
        # Revision 16 dropped the rows; the measurement did not go with them, and is read here from
        # `gapBar()` -- which is where it always came from, and where `grade_motion.py` and the
        # capture receipt read it too.
        for style in ("tween", "physics", "bodies"):
            r = page.evaluate(
                """([i, style]) => {
                  const A = window.atlasTransitions;
                  A.stopAll(); A.select(i); A.setStyle(style); A.setSnap(true); A.setBlind(false); A.setAnneal(3);
                  const read = () => { const g = A.gapBar(); return {side: g.side, record: g.record, met: g.met}; };
                  const out = {};
                  A.seek(0); out.dwell = read();
                  A.seek(A.duration()); out.rest = read();
                  A.setSnap(false); A.seek(A.duration()); out.free = read();
                  A.setSnap(true);
                  return out;
                }""",
                [index_of[n], style],
            )
            # At the dwell the stage shows the previous packing and the bar describes it, so the two
            # agree: revision 16 keyed the bar to the n on the panel rather than the n being stepped
            # into, which is what stopped a smaller packing reading as better than the best known.
            check(r["dwell"]["met"], f"{style}: the dwell does not sit on its own record: {r['dwell']}")
            check(r["rest"]["met"], f"{style}: the snapped run does not reach the record: {r['rest']}")
            if style != "tween":
                check(not r["free"]["met"] or r["free"]["side"] >= r["free"]["record"] - 1e-9,
                      f"{style}: the free run reads better than the record: {r['free']}")
        # The measurement agrees with what the trajectory itself says it reached.
        agree = page.evaluate(
            "([i]) => { const A = window.atlasTransitions; A.select(i); A.setStyle('bodies'); A.setSnap(false);"
            " A.seek(A.duration()); const g = A.gapBar();"
            " const m = A.physics(i, 'bodies', 'free').miss; A.setSnap(true);"
            " return [g.side, m.side]; }",
            [index_of[n]],
        )
        check(abs(agree[0] - agree[1]) < 5e-3, f"the bar says {agree[0]} where the trajectory says {agree[1]}")
        # The trace is built once per combination and only its head moves; the per-frame cost is what
        # the feature has to justify.
        cost = page.evaluate(
            """([i]) => {
              const A = window.atlasTransitions;
              A.select(i); A.setStyle('bodies'); A.setSnap(true); A.seek(1.7);
              const t0 = performance.now();
              for (let k = 0; k < 200; k++) A.seek(1.2 + (k % 100) * 0.01);
              const per = (performance.now() - t0) / 200;
              return {per, spark: document.getElementById('gap-spark') !== null, side: A.gapBar().side};
            }""",
            [index_of[n]],
        )
        # Revision 9 removed the per-frame sparkline: the motion is already visible in the packing.
        check(not cost["spark"], "the per-frame sparkline is back")
        check(cost["side"] > 0, "the bar stopped measuring a side")
        print(f"  a whole frame at n={n} under style C: {cost['per']:.2f} ms")
        browser.close()

    if failures:
        print("FAILED")
        for f in dict.fromkeys(failures):
            print(" -", f)
        return 1
    print(
        "OK: where the sequence stands is a number that starts at nothing, ends at everything and never "
        "goes backwards, with the bar it used to be drawn on gone from the page; the annealing dial runs "
        "0..10 from no shake to three times the default with the run stretched to 1.7 moves at 120 steps a "
        "second throughout, deterministic, cached per level, and the default reproduces the recorded "
        "free-run misses; and the live gap, read from `gapBar()` rather than from rows that no longer "
        "exist, sits on its own record at the dwell, reaches the record under the snap, never reads better "
        "than the record on a free run, agrees with what the trajectory says it reached, and is built once "
        "per combination with no per-frame sparkline."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
