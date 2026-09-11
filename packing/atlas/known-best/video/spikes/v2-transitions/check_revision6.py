"""The revision-6 checks: desaturation, the snap, the blind run and continuous play.

Everything here is a property of the built page, driven through `window.atlasTransitions`
in the pinned headless shell. It complements `test_candidate.py` (the record and the
shell) and `smoke_styles.py` (the two physical styles) rather than repeating them.

    packing/.venv/bin/python3 check_revision6.py [index.html]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent


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
        for name in ("setDesaturate", "setSnap", "setBlind", "setBlindInflate", "playAll", "stopAll", "continuous", "goTo", "setContinuous"):
            check(name in api, f"the API lacks {name}")
        index_of = {q["n"]: q["index"] for q in page.evaluate("atlasTransitions.pairs()")}
        n = 100 if 100 in index_of else sorted(index_of)[len(index_of) // 2]

        # ---- feature 1: desaturation drains the fills while moving and locks them back in.
        st = page.evaluate("atlasTransitions.state()")
        check(st["desaturate"] is True, "desaturation is not on by default")
        for style in ("tween", "physics", "bodies"):
            r = page.evaluate(
                """([i, style]) => {
                  const A = window.atlasTransitions;
                  A.stopAll(); A.select(i); A.setStyle(style); A.setSnap(true); A.setBlind(false);
                  const fills = () => Array.from(document.querySelectorAll('#squares g'))
                    .filter(g => g.style.display !== 'none').map(g => g.firstElementChild.getAttribute('fill'));
                  A.setDesaturate(true);
                  A.seek(0.5); const dwellOn = fills();
                  A.seek(1.7); const midOn = fills();
                  A.seek(A.duration()); const restOn = fills();
                  A.setDesaturate(false);
                  A.seek(0.5); const dwellOff = fills();
                  A.seek(1.7); const midOff = fills();
                  A.seek(A.duration()); const restOff = fills();
                  A.setDesaturate(true);
                  return {dwellOn, midOn, restOn, dwellOff, midOff, restOff};
                }""",
                [index_of[n], style],
            )
            check(r["dwellOn"] == r["dwellOff"], f"{style}: the dwell frame is not the same with and without desaturation")
            check(r["restOn"] == r["restOff"], f"{style}: the resting frame is not the same with and without desaturation")
            check(r["midOn"] != r["midOff"], f"{style}: desaturation changes nothing mid move")

            def chroma(hexes: list[str]) -> float:
                out = []
                for h in hexes:
                    r_, g_, b_ = (int(h[k:k + 2], 16) / 255 for k in (1, 3, 5))
                    out.append(max(r_, g_, b_) - min(r_, g_, b_))
                return sum(out) / len(out)

            check(chroma(r["midOn"]) < 0.6 * chroma(r["midOff"]), f"{style}: mid-move chroma is not visibly drained")

        # ---- feature 2: the snap.
        for style in ("physics", "bodies"):
            r = page.evaluate(
                """([i, style]) => {
                  const A = window.atlasTransitions;
                  A.select(i); A.setStyle(style); A.setBlind(false);
                  const snap = A.physics(i, style, 'snap'), free = A.physics(i, style, 'free');
                  A.setSnap(false); A.seek(A.duration());
                  const note = String(A.gapBar().side);
                  const poses = Array.from(document.querySelectorAll('#squares g')).filter(g => g.style.display !== 'none')
                    .map(g => g.getAttribute('transform'));
                  A.setSnap(true); A.seek(A.duration());
                  const snapped = Array.from(document.querySelectorAll('#squares g')).filter(g => g.style.display !== 'none')
                    .map(g => g.getAttribute('transform'));
                  return {snapMiss: snap.miss, freeMiss: free.miss, note, same: JSON.stringify(poses) === JSON.stringify(snapped)};
                }""",
                [index_of[n], style],
            )
            check(r["snapMiss"]["centre"] < 1e-9 and r["snapMiss"]["angle"] < 1e-9, f"{style}: the snapped run does not end on the record")
            check(r["freeMiss"]["centre"] > 0.01, f"{style}: the free run ends on the record exactly, which cannot be right")
            check(not r["same"], f"{style}: the snap makes no difference to the resting frame")
            # Revision 9 took the sentence off the stage; the live readout carries the same figure.
            check(r["note"].startswith("side "), f"{style}: the panel does not report the side reached: {r['note']!r}")
        r = page.evaluate(
            "([i]) => { const A = window.atlasTransitions; A.select(i); A.setStyle('tween'); A.setSnap(false);"
            " A.seek(A.duration()); const free = Array.from(document.querySelectorAll('#squares g'))"
            "  .filter(g => g.style.display !== 'none').map(g => g.getAttribute('transform'));"
            " A.setSnap(true); A.seek(A.duration()); const snap = Array.from(document.querySelectorAll('#squares g'))"
            "  .filter(g => g.style.display !== 'none').map(g => g.getAttribute('transform'));"
            " return JSON.stringify(free) === JSON.stringify(snap); }",
            [index_of[n]],
        )
        check(r is True, "style A is not the same with the snap off")

        # ---- feature 3: the blind run.
        r = page.evaluate(
            """() => {
              const A = window.atlasTransitions;
              A.setStyle('bodies'); A.setSnap(true);
              const out = [];
              for (const q of A.pairs()) {
                const t = A.physics(q.index, 'bodies', 'blind');
                out.push({n: q.n, kind: q.kind, miss: t.miss, squeezeDone: t.squeezeDone, side0: t.side0});
              }
              return out;
            }"""
        )
        for row in r:
            m = row["miss"]
            check(m["side"] == m["side"] and m["side"] > 0, f"blind {row['n']}: the side reached is {m['side']}")
            check(m["excess"] > -0.001, f"blind {row['n']}: the blind run beat the record by {-m['excess']:.2f}%, which cannot be right")
            check(m["excess"] < 25, f"blind {row['n']}: the blind run is {m['excess']:.1f}% worse, which looks broken")
        note = page.evaluate(
            "([i]) => { const A = window.atlasTransitions; A.select(i); A.setStyle('bodies'); A.setBlind(true);"
            " A.seek(A.duration()); return {read: String(A.gapBar().side),"
            "   miss: A.physics(i, 'bodies', 'blind').miss}; }",
            [index_of[n]],
        )
        # Revision 9 took the sentence off the stage; the two numbers it spelled out are the live
        # readout's own, and the miss is on the API.
        check(note["read"].startswith("side "), f"the blind readout reads {note['read']!r}")
        check(note["miss"]["side"] > note["miss"]["record"], f"the blind run did not lose: {note['miss']}")
        det = page.evaluate(
            "([i]) => { const A = window.atlasTransitions; const a = A.physics(i, 'bodies', 'blind').miss.side;"
            " A.setBlindInflate(1.25); const b = A.physics(i, 'bodies', 'blind').miss.side;"
            " A.setBlindInflate(1.12); const c = A.physics(i, 'bodies', 'blind').miss.side; return [a, b, c]; }",
            [index_of[n]],
        )
        check(det[0] == det[2], "the blind run is not reproducible at the same inflation")
        check(det[0] != det[1], "the inflation factor changes nothing")
        page.evaluate("atlasTransitions.setBlind(false)")

        # ---- feature 4: continuous play and the jump to n.
        c = page.evaluate("atlasTransitions.continuous()")
        check(c["on"] is False, "continuous play is on before it is asked for")
        check((c["dwell"], c["move"], c["settle"], c["staticDwell"]) == (0.8, 1.2, 0.3, 0.5), f"continuous beat is {c}")
        r = page.evaluate(
            """() => {
              const A = window.atlasTransitions;
              A.goTo(A.pairs()[0].n); A.playAll(); A.pause();
              const beats = {};
              for (const q of A.pairs()) { A.select(q.index); (beats[q.kind] = beats[q.kind] || new Set()).add(A.duration()); }
              const out = {};
              for (const k in beats) out[k] = Array.from(beats[k]);
              A.setContinuous({fullBeat: true});
              const full = {};
              for (const q of A.pairs()) { A.select(q.index); (full[q.kind] = full[q.kind] || new Set()).add(A.duration()); }
              const outFull = {};
              for (const k in full) outFull[k] = Array.from(full[k]);
              A.setContinuous({fullBeat: false}); A.stopAll();
              return {out, outFull};
            }"""
        )
        for kind, beats in r["out"].items():
            want = [0.5] if kind in ("prefix", "shared-picture") else [2.3]
            check([round(b, 3) for b in beats] == want, f"continuous beat for {kind} pairs is {beats}, expected {want}")
        for kind, beats in r["outFull"].items():
            check([round(b, 3) for b in beats] == [2.3], f"full-beat duration for {kind} pairs is {beats}")
        first, last = page.evaluate("[atlasTransitions.pairs()[0].n, atlasTransitions.pairs().slice(-1)[0].n]")
        check(page.evaluate("atlasTransitions.goTo(1e9)") == last, "goTo past the end does not clamp to the last pair")
        check(page.evaluate("atlasTransitions.goTo(-5)") == first, "goTo before the start does not clamp to the first pair")
        check(page.evaluate(f"atlasTransitions.goTo({n})") == n, f"goTo({n}) does not select it")
        # Revision 9 dropped the jump-to-n box: one n spine, and `goTo` stays on the API.
        check(page.evaluate("atlasTransitions.state().n") == n, "goTo did not move the stage to n")
        # A run really does cross pair boundaries, keeping the style and the settings.
        r = page.evaluate(
            """() => new Promise((resolve) => {
              const A = window.atlasTransitions;
              A.goTo(A.pairs()[0].n); A.setStyle('bodies'); A.setDesaturate(false); A.playAll();
              const start = A.state().pair;
              const step = () => {
                const s = A.state();
                if (s.pair >= start + 3 || !s.playing) { A.stopAll(); resolve({pair: s.pair, start, style: s.style, desaturate: s.desaturate}); }
                else requestAnimationFrame(step);
              };
              requestAnimationFrame(step);
            })"""
        )
        check(r["pair"] >= r["start"] + 3, f"continuous play stopped at pair {r['pair']} from {r['start']}")
        check(r["style"] == "bodies" and r["desaturate"] is False, "continuous play did not keep the settings")
        page.evaluate("atlasTransitions.setDesaturate(true)")
        browser.close()

    if failures:
        print("FAILED")
        for f in dict.fromkeys(failures):
            print(" -", f)
        return 1
    print(
        "OK: desaturation drains the move and leaves the dwell and the resting frame byte-identical under all three styles; "
        "the snap ends on the record and the free run does not, with the miss on the panel and style A unaffected; "
        "every blind run reaches a side worse than the record and says so, reproducibly, and the inflation moves it; "
        "the continuous beat is 0.8 + 1.2 + 0.3 with static appends at 0.5 and no move, the full beat evens them out, "
        "goTo clamps and follows, and a run crosses pair boundaries keeping its settings."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
