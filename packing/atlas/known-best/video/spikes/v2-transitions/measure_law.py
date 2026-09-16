"""What the force law, the relationship graph and growth actually do to a settle.

    packing/.venv/bin/python3 measure_law.py            # the whole table
    packing/.venv/bin/python3 measure_law.py --laws     # the force law only
    packing/.venv/bin/python3 measure_law.py --graphs   # the relationship graph only
    packing/.venv/bin/python3 measure_law.py --grow     # growth only
    packing/.venv/bin/python3 measure_law.py --drawn    # a hand-drawn contact graph only
    packing/.venv/bin/python3 measure_law.py --n 17 29  # restrict the sizes

A tool, not a one-off: every number the notes quote about revision 11 comes out of here, and the
run is deterministic in the step count, so re-running it on any host gives the same table.

Progress is measured in *steps*, never in wall time: `optimizeStep(k)` advances the
open-ended run by exactly k fixed steps with no clock in it, so the arrangement after k
steps is the same arrangement on any machine. Wall time is reported separately, as a cost.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from sqpack.probes import probe

HERE = Path(__file__).resolve().parent
#: The JavaScript this runs in the page, as files (`sqpack.probes`).
PROBES = HERE / "probes"
PAGE = HERE.parents[4] / "site/workbench/index.html"
STEPS = 2400
SIZES = (17, 29)


def settle(
    page, n: int, *, law: str, start: str, relationship: str = "general", steps: int = STEPS
) -> dict:
    """Run one open-ended settle and report what it reached."""
    return page.evaluate(
        probe(PROBES, "measure_law/settle"),
        {"n": n, "law": law, "start": start, "relationship": relationship, "steps": steps},
    )


def law_table(page, sizes) -> list[dict]:
    rows = []
    for n in sizes:
        for law in ("default", "rigid", "soft", "sticky"):
            for start in ("grid",):
                t0 = time.perf_counter()
                row = settle(page, n, law=law, start=start)
                row["ms"] = round((time.perf_counter() - t0) * 1000)
                rows.append(row)
    return rows


def graph_table(page, sizes) -> list[dict]:
    return [
        settle(page, n, law=law, start="grid", relationship=rel)
        for n in sizes
        for rel in ("general", "groups", "contact")
        for law in ("sticky", "default")
    ]


# ------------------------------------------------- the hand-drawn contact graph (revision 12)
# Three graphs a hand could plausibly draw, generated rather than typed so the same graph can be
# asked for at any n and the numbers are reproducible:
#   ring   0-1-2-...-(n-1)-0, every square joined to the next. n edges.
#   chain  the same without the closing edge. n - 1 edges.
#   record the record's own contact graph, drawn by hand rather than derived — the
#          control, which has to give exactly the run the record-derived target gives.
DRAWN_GRAPHS = ("ring", "chain", "record")


def drawn_graph(page, kind: str, n: int) -> list[list[int]]:
    if kind == "record":
        flat = page.evaluate(probe(PROBES, "measure_law/record-graph"), {"n": n})
        return [[flat[i], flat[i + 1]] for i in range(0, len(flat), 2)]
    edges = [[i, i + 1] for i in range(n - 1)]
    if kind == "ring" and n > 2:
        edges.append([0, n - 1])
    return edges


def drawn_table(page, sizes, steps: int = STEPS) -> list[dict]:
    """What fraction of a hand-drawn contact graph an Optimize run realises."""
    rows = []
    for n in sizes:
        for kind in DRAWN_GRAPHS:
            graph = drawn_graph(page, kind, n)
            rows.append(
                page.evaluate(
                    probe(PROBES, "measure_law/drawn"),
                    {"n": n, "kind": kind, "graph": graph, "steps": steps},
                )
            )
    return rows


def grow_table(page, sizes) -> list[dict]:
    return [
        page.evaluate(probe(PROBES, "measure_law/grow"), {"n": n, "rule": rule})
        for n in sizes
        for rule in ("constant", "clean")
    ]


def show(title: str, rows: list[dict]) -> None:
    print(f"\n## {title}")
    if not rows:
        return
    keys = list(rows[0].keys())
    widths = {k: max(len(k), *(len(fmt(r.get(k))) for r in rows)) for k in keys}
    print("  ".join(k.rjust(widths[k]) for k in keys))
    for r in rows:
        print("  ".join(fmt(r.get(k)).rjust(widths[k]) for k in keys))


def fmt(v) -> str:
    if v is None:
        return "-"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, float):
        return f"{v:.4g}"
    return str(v)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--laws", action="store_true")
    ap.add_argument("--graphs", action="store_true")
    ap.add_argument("--grow", action="store_true")
    ap.add_argument("--drawn", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--n", type=int, nargs="*", default=list(SIZES))
    ap.add_argument("--page", type=Path, default=PAGE, help="the built workbench page")
    args = ap.parse_args()
    everything = not (args.laws or args.graphs or args.grow or args.drawn)
    out: dict[str, list[dict]] = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        errors: list[str] = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(args.page.resolve().as_uri(), wait_until="load")
        page.wait_for_timeout(400)
        if everything or args.laws:
            out["the force law"] = law_table(page, args.n)
        if everything or args.graphs:
            out["the relationship graph"] = graph_table(page, args.n)
        if everything or args.grow:
            out["growth"] = grow_table(page, args.n)
        if everything or args.drawn:
            out["a hand-drawn contact graph"] = drawn_table(page, args.n)
        browser.close()
    if args.json:
        print(json.dumps(out, indent=1))
    else:
        for title, rows in out.items():
            show(title, rows)
    if errors:
        print("\nPAGE ERRORS:", errors)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
