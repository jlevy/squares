"""A rough Calibrate run: sweep the workbench's own mechanisms against known records.

Deliberately not a claim about search quality. Every arm starts from an arrangement that
is NOT the record (random or the trivial grid), runs open-ended, and is scored by the
container it needs against the record's. A run that reports a side below the record has
not found anything: it is overlapping, and the overlap column is printed beside every
number so that cannot be read as a win.
"""
import json, sys, itertools
from playwright.sync_api import sync_playwright

PAGE = sys.argv[1]
STEPS = int(sys.argv[2]) if len(sys.argv) > 2 else 2400
CASES = [5, 10, 11, 17, 26, 29]          # non-grid cases, small enough to sweep
ARMS = [
    # label                start     law overrides                                    anneal
    ("plain",              "grid",   {},                                               3),
    ("rigid",              "grid",   {"rigidity": 0.01, "repulsion": 4000},             3),
    ("soft",               "grid",   {"rigidity": 0.35, "repulsion": 400},              3),
    ("sticky",             "grid",   {"attraction": 150, "range": 0.25},                3),
    ("shaken",             "grid",   {},                                              10),
    ("quiet",              "grid",   {},                                               0),
    ("plain/random",       "random", {},                                               3),
    ("shaken/random",      "random", {},                                              10),
]

def main():
    rows = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1400, "height": 900})
        pg.goto(f"file://{PAGE}"); pg.wait_for_timeout(2000)
        pg.evaluate("atlasTransitions.setMode('pack')")
        for n, (label, start, law, anneal) in itertools.product(CASES, ARMS):
            pg.evaluate(f"atlasTransitions.setStepN({n})"); pg.wait_for_timeout(250)
            pg.evaluate("atlasTransitions.setLawPreset('default')")
            if law: pg.evaluate(f"atlasTransitions.setLaw({json.dumps(law)})")
            pg.evaluate(f"atlasTransitions.setAnneal({anneal})")
            pg.evaluate(f"atlasTransitions.setInitial('{start}'); atlasTransitions.optimize()")
            pg.wait_for_timeout(120)
            pg.evaluate(f"atlasTransitions.optimizeStep({STEPS})")
            st = pg.evaluate("atlasTransitions.optimizeState()")
            rec, side, pen = st.get("record"), st.get("side"), st.get("penetration")
            if rec and side is not None:
                rows.append({"n": n, "arm": label, "record": rec, "side": side,
                             "pen": pen, "excess": 100 * (side - rec) / rec})
        b.close()
    print(f"{'n':>4} {'arm':<16} {'record':>9} {'reached':>9} {'excess':>8} {'overlap':>9}  verdict")
    for r in rows:
        v = "OVERLAPPING" if (r["pen"] or 0) > 1e-4 and r["side"] < r["record"] else ""
        print(f"{r['n']:>4} {r['arm']:<16} {r['record']:>9.5f} {r['side']:>9.5f}"
              f" {r['excess']:>7.2f}% {r['pen']:>9.5f}  {v}")
    print()
    best = {}
    for r in rows:
        clean = (r["pen"] or 0) <= 1e-4
        key = r["arm"]
        best.setdefault(key, []).append(r["excess"] if clean else None)
    print("arm summary (mean excess over cases, clean runs only):")
    for arm, vals in best.items():
        ok = [v for v in vals if v is not None]
        print(f"  {arm:<16} clean {len(ok)}/{len(vals)}"
              + (f"  mean excess {sum(ok)/len(ok):+.2f}%" if ok else "  no clean run"))
    json.dump(rows, open(sys.argv[3] if len(sys.argv) > 3 else "/dev/null", "w"), indent=1)

main()
