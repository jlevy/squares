"""The revision-6 checks: desaturation, the snap, the blind run and continuous play.

Everything here is a property of the built page, driven through `window.atlasTransitions`
in the pinned headless shell. It complements `test_candidate.py` (the record and the
shell) and `smoke_styles.py` (the two physical styles) rather than repeating them.

    packing/.venv/bin/python3 check_revision6.py [index.html]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from probes import probe

HERE = Path(__file__).resolve().parent


def main() -> int:
    page_path = (HERE / sys.argv[1]) if len(sys.argv) > 1 else HERE / "index.html"
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:  # noqa: FBT001 - the assertion, not a flag
        if not condition:
            failures.append(message)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.on(
            "console",
            lambda m: (
                failures.append(f"console.{m.type}: {m.text}") if m.type == "error" else None
            ),
        )
        page.on("pageerror", lambda e: failures.append(f"pageerror: {e}"))
        page.goto(f"file://{page_path}")
        page.wait_for_timeout(900)
        api = set(page.evaluate(probe("revision6/api_names")))
        for name in (
            "setDesaturate",
            "setSnap",
            "setBlind",
            "setBlindInflate",
            "playAll",
            "stopAll",
            "continuous",
            "goTo",
            "setContinuous",
        ):
            check(name in api, f"the API lacks {name}")
        index_of = {q["n"]: q["index"] for q in page.evaluate(probe("revision6/pairs"))}
        n = 100 if 100 in index_of else sorted(index_of)[len(index_of) // 2]

        # ---- feature 1: desaturation drains the fills while moving and locks them back in.
        st = page.evaluate(probe("revision6/state"))
        check(st["desaturate"] is True, "desaturation is not on by default")
        for style in ("tween", "physics", "bodies"):
            r = page.evaluate(
                probe("revision6/desaturation"), {"index": index_of[n], "style": style}
            )
            check(
                r["dwellOn"] == r["dwellOff"],
                f"{style}: the dwell frame is not the same with and without desaturation",
            )
            check(
                r["restOn"] == r["restOff"],
                f"{style}: the resting frame is not the same with and without desaturation",
            )
            check(r["midOn"] != r["midOff"], f"{style}: desaturation changes nothing mid move")

            def chroma(hexes: list[str]) -> float:
                out = []
                for h in hexes:
                    r_, g_, b_ = (int(h[k : k + 2], 16) / 255 for k in (1, 3, 5))
                    out.append(max(r_, g_, b_) - min(r_, g_, b_))
                return sum(out) / len(out)

            check(
                chroma(r["midOn"]) < 0.6 * chroma(r["midOff"]),
                f"{style}: mid-move chroma is not visibly drained",
            )

        # ---- feature 2: the snap.
        for style in ("physics", "bodies"):
            r = page.evaluate(probe("revision6/snap"), {"index": index_of[n], "style": style})
            check(
                r["snapMiss"]["centre"] < 1e-9 and r["snapMiss"]["angle"] < 1e-9,
                f"{style}: the snapped run does not end on the record",
            )
            check(
                r["freeMiss"]["centre"] > 0.01,
                f"{style}: the free run ends on the record exactly, which cannot be right",
            )
            check(not r["same"], f"{style}: the snap makes no difference to the resting frame")
            # Revision 9 took the sentence off the stage; the live readout carries the same
            # figure.
            check(
                r["note"].startswith("side "),
                f"{style}: the panel does not report the side reached: {r['note']!r}",
            )
        r = page.evaluate(probe("revision6/tween_rests_alike"), {"index": index_of[n]})
        check(r is True, "style A is not the same with the snap off")

        # ---- feature 3: the blind run.
        r = page.evaluate(probe("revision6/blind_sweep"))
        for row in r:
            m = row["miss"]
            check(
                m["side"] == m["side"] and m["side"] > 0,
                f"blind {row['n']}: the side reached is {m['side']}",
            )
            check(
                m["excess"] > -0.001,
                f"blind {row['n']}: the blind run beat the record by {-m['excess']:.2f}%, "
                f"which cannot be right",
            )
            check(
                m["excess"] < 25,
                f"blind {row['n']}: the blind run is {m['excess']:.1f}% worse, "
                f"which looks broken",
            )
        note = page.evaluate(probe("revision6/blind_readout"), {"index": index_of[n]})
        # Revision 9 took the sentence off the stage; the two numbers it spelled out are the
        # live readout's own, and the miss is on the API.
        check(note["read"].startswith("side "), f"the blind readout reads {note['read']!r}")
        check(
            note["miss"]["side"] > note["miss"]["record"],
            f"the blind run did not lose: {note['miss']}",
        )
        det = page.evaluate(probe("revision6/blind_inflation"), {"index": index_of[n]})
        check(det[0] == det[2], "the blind run is not reproducible at the same inflation")
        check(det[0] != det[1], "the inflation factor changes nothing")
        page.evaluate(probe("revision6/set_blind"), {"on": False})

        # ---- feature 4: continuous play and the jump to n.
        c = page.evaluate(probe("revision6/continuous"))
        check(c["on"] is False, "continuous play is on before it is asked for")
        check(
            (c["dwell"], c["move"], c["settle"], c["staticDwell"]) == (0.8, 1.2, 0.3, 0.5),
            f"continuous beat is {c}",
        )
        r = page.evaluate(probe("revision6/beats"))
        for kind, beats in r["out"].items():
            want = [0.5] if kind in ("prefix", "shared-picture") else [2.3]
            check(
                [round(b, 3) for b in beats] == want,
                f"continuous beat for {kind} pairs is {beats}, expected {want}",
            )
        for kind, beats in r["outFull"].items():
            check(
                [round(b, 3) for b in beats] == [2.3],
                f"full-beat duration for {kind} pairs is {beats}",
            )
        first, last = page.evaluate(probe("revision6/first_last_n"))
        go_to = probe("revision6/go_to")
        check(
            page.evaluate(go_to, {"n": 1e9}) == last,
            "goTo past the end does not clamp to the last pair",
        )
        check(
            page.evaluate(go_to, {"n": -5}) == first,
            "goTo before the start does not clamp to the first pair",
        )
        check(page.evaluate(go_to, {"n": n}) == n, f"goTo({n}) does not select it")
        # Revision 9 dropped the jump-to-n box: one n spine, and `goTo` stays on the API.
        check(
            page.evaluate(probe("revision6/state_n")) == n, "goTo did not move the stage to n"
        )
        # A run really does cross pair boundaries, keeping the style and the settings.
        r = page.evaluate(probe("revision6/continuous_run"))
        check(
            r["pair"] >= r["start"] + 3,
            f"continuous play stopped at pair {r['pair']} from {r['start']}",
        )
        check(
            r["style"] == "bodies" and r["desaturate"] is False,
            "continuous play did not keep the settings",
        )
        page.evaluate(probe("revision6/set_desaturate"), {"on": True})
        browser.close()

    if failures:
        print("FAILED")
        for f in dict.fromkeys(failures):
            print(" -", f)
        return 1
    print(
        "OK: desaturation drains the move and leaves the dwell and the resting frame "
        "byte-identical under all three styles; the snap ends on the record and the free run "
        "does not, with the miss on the panel and style A unaffected; every blind run reaches "
        "a side worse than the record and says so, reproducibly, and the inflation moves it; "
        "the continuous beat is 0.8 + 1.2 + 0.3 with static appends at 0.5 and no move, the "
        "full beat evens them out, goTo clamps and follows, and a run crosses pair boundaries "
        "keeping its settings."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
