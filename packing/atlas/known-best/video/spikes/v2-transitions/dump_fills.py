"""Dump every visible square's fill at chosen instants, for the rest-colour identity check.

    packing/.venv/bin/python3 dump_fills.py OUT.json [PAGE]
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
PAIRS = [1, 4, 10, 17, 100, 110, 272, 307, 323]
STYLES = ["tween", "physics", "bodies"]
RULES = ["continuous", "house"]


def main() -> int:
    out = Path(sys.argv[1])
    page_path = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "index.html"
    snap = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        errors: list[str] = []
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(f"file://{page_path}")
        page.wait_for_timeout(800)
        index_of = {p_["n"]: p_["index"] for p_ in page.evaluate("atlasTransitions.pairs()")}
        for n in PAIRS:
            if n not in index_of:
                continue
            for style in STYLES:
                for rule in RULES:
                    page.evaluate(
                        "([i, s, r]) => { atlasTransitions.select(i); atlasTransitions.setStyle(s); atlasTransitions.setColorRule(r); }",
                        [index_of[n], style, rule],
                    )
                    for label, t in (("dwell", 0.5), ("start", 0.0), ("end", None)):
                        tt = page.evaluate("atlasTransitions.duration()") if t is None else t
                        page.evaluate("t => atlasTransitions.seek(t)", tt)
                        fills = page.evaluate(
                            "Array.from(document.querySelectorAll('#squares g')).filter(g => g.style.display !== 'none')"
                            ".map(g => [g.dataset.identity, g.firstElementChild.getAttribute('fill')])"
                        )
                        snap[f"{n}/{style}/{rule}/{label}"] = fills
        if errors:
            print("ERRORS:", errors)
        browser.close()
    out.write_text(json.dumps(snap, indent=0, sort_keys=True))
    print(f"{len(snap)} instants, {sum(len(v) for v in snap.values())} fills -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
