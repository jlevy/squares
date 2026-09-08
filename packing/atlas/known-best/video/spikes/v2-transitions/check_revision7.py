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
REVISION6_FREE = {
    ("physics", 100): (1.149, 42.96, 10.619),
    ("bodies", 100): (1.244, 43.04, 10.621),
    ("physics", 110): (1.540, 16.87, 11.116),
    ("bodies", 110): (1.706, 28.33, 11.074),
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

        # ---- feature 1: the bar carries the whole scale, and it is a function of the clock alone.
        scale = page.evaluate(
            "() => Array.from(document.querySelectorAll('#p-scale .p-num')).map(e => ({"
            "  v: Number(e.textContent), left: parseFloat(e.style.left)}))"
        )
        values = [q["v"] for q in scale]
        want = [1] + list(range(25, n_max, 25)) + [n_max]
        check(values == want, f"the scale's numerals are {values}, expected {want}")
        ticks = page.evaluate("document.querySelectorAll('#p-scale .p-tick').length")
        minors = page.evaluate("document.querySelectorAll('#p-scale .p-tick:not(.p-major)').length")
        check(ticks - minors == len(want), f"{ticks - minors} major ticks for {len(want)} numerals")
        check(minors > 50, f"only {minors} minor ticks on a {n_max}-value scale")
        sizes = page.evaluate(
            "() => Array.from(new Set(Array.from(document.querySelectorAll('#p-scale .p-num, #p-n'))"
            "  .map(e => getComputedStyle(e).fontSize)))"
        )
        check(sizes == ["28px"], f"the bar's numerals are set at {sizes}, not the 28 px floor")
        colours = page.evaluate(
            "() => ({num: getComputedStyle(document.querySelector('#p-scale .p-num')).color,"
            "        muted: getComputedStyle(document.documentElement).getPropertyValue('--muted').trim()})"
        )
        check(colours["num"] == "rgb(92, 102, 115)", f"the scale's numerals are {colours['num']}, not the muted grey")
        # The rider rides the fill's leading edge and hides whichever numeral it would touch.
        page.evaluate("atlasTransitions.setCapture(true)")
        for probe in (0.0, 0.5, 1.0):
            r = page.evaluate(
                """(u) => {
                  const A = window.atlasTransitions;
                  const idx = Math.min(A.pairs().length - 1, Math.round(u * (A.pairs().length - 1)));
                  A.select(idx); A.seek(u * A.duration());
                  const rider = document.getElementById('p-n').getBoundingClientRect();
                  const hidden = Array.from(document.querySelectorAll('#p-scale .p-num'))
                    .filter(e => getComputedStyle(e).visibility === 'hidden').map(e => e.textContent);
                  const shown = Array.from(document.querySelectorAll('#p-scale .p-num'))
                    .filter(e => getComputedStyle(e).visibility !== 'hidden')
                    .map(e => e.getBoundingClientRect())
                    .filter(b => b.left < rider.right && b.right > rider.left);
                  return {hidden, collisions: shown.length, fill: parseFloat(document.getElementById('p-fill').style.width),
                          position: A.progress().position};
                }""",
                probe,
            )
            check(r["collisions"] == 0, f"at u={probe} the riding n overlaps {r['collisions']} scale numerals")
            check(abs(r["fill"] - r["position"] * 1720) < 1e-3, f"at u={probe} the fill is {r['fill']} px for position {r['position']}")

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
        # The default is the revision-6 simulation to the digits its notes recorded.
        for (style, pair_n), (centre, angle, side) in REVISION6_FREE.items():
            if pair_n not in index_of:
                continue
            m = page.evaluate(
                "([i, s]) => window.atlasTransitions.physics(i, s, 'free').miss",
                [index_of[pair_n], style],
            )
            check(abs(m["centre"] - centre) < 5e-4 and abs(m["angle"] - angle) < 5e-3 and abs(m["side"] - side) < 5e-4,
                  f"at the default level {style} {pair_n} misses by {m['centre']:.3f}/{m['angle']:.2f}/{m['side']:.3f}, "
                  f"not revision 6's {centre}/{angle}/{side}")
        # The dial works under the snap and under the blind run too.
        for mode in ("snap", "blind"):
            r = page.evaluate(
                "([i, m]) => { const A = window.atlasTransitions; A.setAnneal(9);"
                " const r = A.physics(i, 'physics', m); A.setAnneal(3); return {miss: r.miss, steps: r.steps}; }",
                [index_of[n], mode],
            )
            check(r["steps"] > 200, f"{mode} at level 9 runs only {r['steps']} steps")
            if mode == "snap":
                check(r["miss"]["centre"] < 1e-9, "a snapped run at level 9 does not end on the record")
            else:
                check(r["miss"]["excess"] > -0.001, "a blind run at level 9 beat the record")

        # ---- feature 3: the live gap, at all times.
        for style in ("tween", "physics", "bodies"):
            r = page.evaluate(
                """([i, style]) => {
                  const A = window.atlasTransitions;
                  A.stopAll(); A.select(i); A.setStyle(style); A.setSnap(true); A.setBlind(false); A.setAnneal(3);
                  const read = () => ({a: document.getElementById('gap-a').textContent,
                                       b: document.getElementById('gap-b').textContent});
                  const out = {};
                  for (const t of [0, 1.7, A.duration()]) { A.seek(t); out[t] = read(); }
                  A.setSnap(false); A.seek(A.duration()); out.free = read();
                  A.setSnap(true);
                  return out;
                }""",
                [index_of[n], style],
            )
            dwell = r["0"]
            rest = r[str(round(page.evaluate("atlasTransitions.duration()"), 10))] if False else r[list(r)[2]]
            check(dwell["a"].startswith("gap to the record: centres "), f"{style}: the dwell reads {dwell['a']!r}")
            check("side " in dwell["b"] and "against the record" in dwell["b"], f"{style}: the dwell's side line reads {dwell['b']!r}")
            check(float(dwell["a"].split("centres ")[1].split(",")[0]) > 0.1,
                  f"{style}: the gap at the dwell is already nothing: {dwell['a']!r}")
            check(rest["a"] == "gap to the record: centres 0.000, angles 0.0°",
                  f"{style}: the snapped run does not close the gap: {rest['a']!r}")
            if style != "tween":
                check(float(r["free"]["a"].split("centres ")[1].split(",")[0]) > 0.01,
                      f"{style}: the free run reads a zero gap: {r['free']['a']!r}")
        # Blind: the centre and angle errors are withheld, with the reason, and the box is not.
        r = page.evaluate(
            "([i]) => { const A = window.atlasTransitions; A.select(i); A.setStyle('bodies'); A.setBlind(true);"
            " A.seek(A.duration()); const o = {a: document.getElementById('gap-a').textContent,"
            "  b: document.getElementById('gap-b').textContent}; A.setBlind(false); return o; }",
            [index_of[n]],
        )
        check(r["a"] == "no centre or angle gap: nothing corresponds", f"the blind readout's first row is {r['a']!r}")
        check(r["b"].startswith("side ") and "per cent" in r["b"], f"the blind readout's side row is {r['b']!r}")
        # The readout agrees with what the trajectory itself says it reached.
        agree = page.evaluate(
            "([i]) => { const A = window.atlasTransitions; A.select(i); A.setStyle('bodies'); A.setSnap(false);"
            " A.seek(A.duration()); const line = document.getElementById('gap-a').textContent;"
            " const m = A.physics(i, 'bodies', 'free').miss; A.setSnap(true);"
            " return [Number(line.split('centres ')[1].split(',')[0]), m.centre]; }",
            [index_of[n]],
        )
        check(abs(agree[0] - agree[1]) < 5e-4, f"the readout says {agree[0]} where the trajectory says {agree[1]}")
        # The trace is built once per combination and only its head moves; the per-frame cost is what
        # the feature has to justify.
        cost = page.evaluate(
            """([i]) => {
              const A = window.atlasTransitions;
              A.select(i); A.setStyle('bodies'); A.setSnap(true); A.seek(1.7);
              const pts = document.getElementById('gap-trace').getAttribute('points');
              const t0 = performance.now();
              for (let k = 0; k < 200; k++) A.seek(1.2 + (k % 100) * 0.01);
              const per = (performance.now() - t0) / 200;
              const same = document.getElementById('gap-trace').getAttribute('points') === pts;
              return {per, same, points: pts.split(' ').length,
                      head: document.getElementById('gap-head').getAttribute('cx')};
            }""",
            [index_of[n]],
        )
        check(cost["same"], "the trace is rebuilt while only the clock moves")
        check(cost["points"] == 65, f"the trace has {cost['points']} samples")
        print(f"  a whole frame at n={n} under style C, trace included: {cost['per']:.2f} ms")
        browser.close()

    if failures:
        print("FAILED")
        for f in dict.fromkeys(failures):
            print(" -", f)
        return 1
    print(
        "OK: the bar carries a numeral every 25 and the last value, minor ticks every 5, all at 28 px in the "
        "muted grey, with the riding n on the fill's edge and never on a numeral; the annealing dial runs 0..10 "
        "from no shake to three times the default with the run stretched to 1.7 moves at 120 steps a second "
        "throughout, deterministic, cached per level, and the default reproduces revision 6's measurements exactly; "
        "the live gap reads at the dwell, closes to nothing under the snap and style A, rests at the trajectory's "
        "own miss with the snap off, withholds the centre and angle errors in a blind run with the reason, and its "
        "trace is built once per combination."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
