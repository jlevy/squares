"""Measure what a run that is not snapped to the record, or a blind run, actually reaches.

    packing/.venv/bin/python3 measure_modes.py [free|blind] [n ...]
        [--anneal 0,3,6,10] [--page index-all.html]

With `--anneal` the same measurement is taken at each annealing level, which is what says
whether shaking harder gets the physics closer to the record or only further from it.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent


def note_console(errors: list[str], message) -> None:
    """Keep the console errors and ignore everything else the page says."""
    if message.type == "error":
        errors.append(f"console.{message.type}: {message.text}")


def main() -> int:
    args = sys.argv[1:]
    levels: list[int] = []
    page_name = "index.html"
    while "--anneal" in args:
        i = args.index("--anneal")
        levels = [int(v) for v in args[i + 1].split(",")]
        del args[i : i + 2]
    while "--page" in args:
        i = args.index("--page")
        page_name = args[i + 1]
        del args[i : i + 2]
    mode = args[0] if args else "free"
    ns = [int(a) for a in args[1:]] or [100, 110, 272]
    if levels:
        return sweep(page_name, mode, ns, levels)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        errors: list[str] = []
        page.on("console", lambda m: note_console(errors, m))
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(f"file://{HERE / 'index.html'}")
        page.wait_for_timeout(600)
        index_of = {q["n"]: q["index"] for q in page.evaluate("atlasTransitions.pairs()")}
        print("| pair | style | max centre | max angle | side reached | record | excess |")
        print("| --- | --- | ---: | ---: | ---: | ---: | ---: |")
        for n in ns:
            for style in ("physics", "bodies"):
                r = page.evaluate(
                    "([i, s, m]) => { const r = atlasTransitions.physics(i, s, m);"
                    " return {miss: r.miss, ms: r.ms, bodies: r.bodies,"
                    " pen: r.maxPenetration, penLate: r.maxPenetrationLate}; }",
                    [index_of[n], style, mode],
                )
                m = r["miss"]
                print(
                    f"| {n} → {n + 1} | {style} | {m['centre']:.3f} | {m['angle']:.2f}° | "
                    f"{m['side']:.3f} | {m['record']:.3f} | {m['excess']:+.2f}% |  "
                    f"({r['ms']:.0f} ms, {r['bodies']} bodies, "
                    f"overlap {max(r['pen'], r['penLate']):.2f})"
                )
        print("ERRORS:", errors or "none")
        browser.close()
    return 0


def sweep(page_name: str, mode: str, ns: list[int], levels: list[int]) -> int:
    """The annealing sweep: the final miss at each level, for both physical styles."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        errors: list[str] = []
        page.on("console", lambda m: note_console(errors, m))
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(f"file://{HERE / page_name}")
        page.wait_for_timeout(700)
        index_of = {q["n"]: q["index"] for q in page.evaluate("atlasTransitions.pairs()")}
        print(
            "| pair | style | level | shake | decay | span | max centre | max angle |"
            " side reached | excess | deepest overlap |"
        )
        print("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for n in ns:
            if n not in index_of:
                print(f"(n={n} is not on {page_name})")
                continue
            for style in ("physics", "bodies"):
                for level in levels:
                    r = page.evaluate(
                        "([i, s, m, L]) => { const A = window.atlasTransitions;"
                        " A.setStyle(s); A.setAnneal(L);"
                        " const r = A.physics(i, s, m); const a = A.anneal();"
                        " return {miss: r.miss, ms: r.ms,"
                        " pen: Math.max(r.maxPenetration, r.maxPenetrationLate),"
                        "         steps: r.steps, amp: a.amplitude, dec: a.decayPower,"
                        " span: a.span}; }",
                        [index_of[n], style, mode, level],
                    )
                    m = r["miss"]
                    print(
                        f"| {n} → {n + 1} | {style} | {level} | "
                        f"×{r['amp']:.2f} | ^{r['dec']:.2f} | "  # noqa: RUF001
                        f"{r['span']:.2f} | "
                        f"{m['centre']:.3f} | {m['angle']:.2f}° | {m['side']:.3f} | "
                        f"{m['excess']:+.2f}% | {r['pen']:.2f} |"
                        f"  ({r['steps']} steps, {r['ms']:.0f} ms)"
                    )
        page.evaluate("atlasTransitions.setAnneal(3)")
        print("ERRORS:", errors or "none")
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
