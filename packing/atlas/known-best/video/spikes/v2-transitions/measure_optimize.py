"""What an open-ended Optimize run achieves, per second of wall clock and per second simulated.

Two measurements, because they answer different questions and only one of them is a
property of the machine this runs on:

  throughput  how many fixed steps of the run a second of wall clock buys at this n, from
              a real playing run through `requestAnimationFrame` in the pinned headless
              shell. This is the one that moves with the host.
  progress    what the run reaches after a fixed number of steps: the smallest box it has
              held the squares in without overlapping them (`best`), against the record.
              Deterministic — the state after k steps is exact — so it is the same on any
              host.

    packing/.venv/bin/python3 measure_optimize.py [--page workbench.html] [--steps 2400] [n ...]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
KINDS = ("previous", "random", "grid")


def main() -> int:
    argv = sys.argv[1:]
    page_name = "workbench.html"
    steps = 2400
    ns: list[int] = []
    i = 0
    while i < len(argv):
        if argv[i] == "--page":
            page_name = argv[i + 1]
            i += 2
        elif argv[i] == "--steps":
            steps = int(argv[i + 1])
            i += 2
        else:
            ns.append(int(argv[i]))
            i += 1
    if not ns:
        ns = [17, 100]
    page_path = HERE / page_name

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        errs: list[str] = []
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.goto(f"file://{page_path}")
        page.wait_for_timeout(900)
        print(f"{page_name}, {steps} steps per progress run\n")
        print(f"{'n':>4} {'start':<9} {'steps/s':>8} {'sim s/s':>8} {'ms/step':>8} "
              f"{'start side':>10} {'best':>8} {'record':>8} {'excess':>8} {'overlap':>8}")
        for n in ns:
            for kind in KINDS:
                # Throughput: a real playing run for 2 s of wall clock.
                page.evaluate(
                    "([n, k]) => { const A = window.atlasTransitions;"
                    " A.setStepN(n); A.setSpeed(2);"
                    "  A.setInitial(k); A.optimize(true); }",
                    [n, kind],
                )
                page.wait_for_timeout(2000)
                live = page.evaluate(
                    "() => { const A = window.atlasTransitions; A.pause();"
                    " return A.optimizeState(); }"
                )
                # Progress: the same start, driven by exact step counts with no clock in it.
                page.evaluate(
                    "([n, k]) => { const A = window.atlasTransitions;"
                    " A.setStepN(n); A.setInitial(k);"
                    "  A.optimize(true); A.pause(); }",
                    [n, kind],
                )
                start = page.evaluate("atlasTransitions.optimizeState()")
                done = page.evaluate("(k) => atlasTransitions.optimizeStep(k)", steps)
                best = done["best"]
                excess = (best / done["record"] - 1) * 100 if best else float("nan")
                print(
                    f"{n:>4} {kind:<9} {live['steps'] / 2.0:>8.0f} {live['time'] / 2.0:>8.2f} "
                    f"{live['msPerStep']:>8.3f} {start['required']:>10.3f} "
                    f"{(best or float('nan')):>8.3f} {done['record']:>8.3f} "
                    f"{excess:>7.2f}% {(done['penetration'] or 0):>8.4f}"
                )
        page.evaluate("atlasTransitions.setSpeed(1); atlasTransitions.setInitial('previous')")
        browser.close()
        if errs:
            print("\nPAGE ERRORS:", errs)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
