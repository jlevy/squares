"""A243 -- the PAGES (docs/residue_map/campaigns/A243-climb-17-19/), drawn from the table and the records, no toolkit:
  climb243_n<N>_root.svg    the four-corner root: pins, its candidate cells coloured by the extension's verdict
                            (green = DEAD: a Theorem FC forced cell; amber = open: Theorem FC's first horn ASSUMED on
                            the spine, the k + 1 branch otherwise), the spine verdict and its kills;
  climb243_n<N>_record.svg  the record (A226 survey226, exact Ellsworth coordinates): its slot squares (the class),
                            the tilted band, the candidate cells around the class, the record class's verdict;
  climb243_n<N>_census.svg  the census per k: classes, DEAD / REDUCES / ALIVE / pending bars.
    python pages243.py [17 19]"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
A243 = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(A243, "..", ".."))
OUT = os.path.join(ROOT, "docs", "residue_map", "campaigns", "A243-climb-17-19")
sys.path.insert(0, HERE)
_A178 = os.path.join(ROOT, "attempts", "A178-gallery-geometry", "code")
if _A178 not in sys.path:
    sys.path.append(_A178)
import census243 as CEN                                         # noqa: E402
import classtab243 as CT                                        # noqa: E402
import climb243 as CL                                           # noqa: E402

COL = dict(DEAD="#2e7d32", REDUCES="#ef6c00", ALIVE="#c62828", PENDING="#9e9e9e", ERROR="#6a1b9a")


def sq(x, y, t, s, sc, fill, stroke="#222", op=0.85):
    c, sn = math.cos(t), math.sin(t)
    pts = [(x + 0.5 * (a * c - b * sn), y + 0.5 * (a * sn + b * c)) for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
    return '<polygon points="%s" fill="%s" fill-opacity="%.2f" stroke="%s" stroke-width="1"/>' % (
        " ".join("%.1f,%.1f" % (20 + sc * px, 20 + sc * (s - py)) for px, py in pts), fill, op, stroke)


def frame(s, sc, title, lines):
    W = int(40 + sc * s)
    head = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="sans-serif">' % (W + 360, W + 20),
            '<rect width="100%" height="100%" fill="white"/>',
            '<rect x="20" y="20" width="%.1f" height="%.1f" fill="none" stroke="#000" stroke-width="2"/>' % (sc * s, sc * s)]
    txt = ['<text x="%d" y="%d" font-size="14" font-weight="bold">%s</text>' % (W + 10, 34, title)]
    txt += ['<text x="%d" y="%d" font-size="11">%s</text>' % (W + 10, 54 + 15 * i, l.replace("&", "&amp;").replace("<", "&lt;")) for i, l in enumerate(lines)]
    return head, txt


def cells_of(tab, cls):
    """the class's candidate cells (s passed explicitly: never touches classes178.S0 of a live worker)."""
    return CT.forced_cells(tab, cls, float(tab.s_hi), None, ())


def page_root(n, tab, summ):
    cls = CL.ROOT4[n]
    s, sc = float(tab.s_hi), 110
    v = tab.verdicts.get(cls) or {}
    lines = ["n = %d, window [%s, %s]" % (n, tab.s_lo, tab.s_hi), "class %s (%s)" % (cls, ", ".join(tab.rows[cls]["labels"])),
             "spine verdict: %s" % (v.get("verdict") or "PENDING"), "kills: %s" % (v.get("kills_by_rule") or {}),
             "nodes %s, %s s" % (v.get("n_nodes"), v.get("seconds")), "cells: green = extension DEAD (FC forced)",
             "amber = extension open (first horn assumed)"]
    body = []
    for c in cells_of(tab, cls):
        x, y = CT.CEN.centre(c["corner"], c["i"], c["j"], tab.s_hi)
        col = COL["DEAD"] if tab.dead(c["extension"]) else COL["REDUCES"]
        body.append(sq(float(x), float(y), 0.0, s, sc, col, "#555", 0.35))
        lines.append("  %s -> %s: %s" % (c["cell"], c["extension"], tab.verdict(c["extension"]) or "PENDING"))
    for x, y in tab.pins_of(cls):
        body.append(sq(x, y, 0.0, s, sc, "#1565c0"))
    head, txt = frame(s, sc, "A243 four-corner root, n = %d" % n, lines)
    return "\n".join(head + body + txt + ["</svg>"])


def page_record(n, tab, summ):
    r = [json.loads(l) for l in open(os.path.join(ROOT, "attempts", "A226-one-flush", "results", "survey226.jsonl"), encoding="utf-8")
         if json.loads(l).get("label") == "square-%d" % n][0]
    s, sc = r["side"], 110
    cls = CL.RECORD[n]
    v = tab.verdicts.get(cls) or {}
    body = []
    n_slot = 0
    for x, y, t in r["squares"]:
        upright = min(abs(t) % (math.pi / 2), math.pi / 2 - abs(t) % (math.pi / 2)) < 1e-6
        slot = upright and all(min(abs((u - 0.5) - round(u - 0.5)), abs((s - u - 0.5) - round(s - u - 0.5))) < 1e-6 for u in (x, y))
        n_slot += 1 if slot else 0
        body.append(sq(x, y, t, s, sc, "#1565c0" if slot else ("#90a4ae" if upright else "#ffb300")))
    rig = {}
    f = os.path.join(A243, "results", "rigid243_n%d.json" % n)
    if os.path.exists(f):
        rig = json.load(open(f, encoding="utf-8"))
    lines = ["%s, side %.10f" % (r.get("source"), s), "slot squares (blue) %d = class %s" % (n_slot, cls),
             "tilted (amber) %d, upright off-lattice (grey) %d" % (r["n_tilted"], len(r["squares"]) - n_slot - r["n_tilted"]),
             "class verdict: %s %s" % (v.get("verdict") or "PENDING", ("-> " + ", ".join(v.get("targets") or [])) if v.get("targets") else ""),
             "rigidity [M]: contacts %s, first-order motion LP %s" % (rig.get("n_contacts"), (rig.get("lp") or {}).get("max_l1")),
             "  moving squares %s, rattlers %s" % ((rig.get("lp") or {}).get("moving"), rig.get("rattlers"))]
    head, txt = frame(s, sc, "A243 record class, n = %d" % n, lines)
    return "\n".join(head + body + txt + ["</svg>"])


def page_census(n, summ):
    ks = sorted((int(k) for k in summ["census_by_k"]), reverse=True)
    W, H = 760, 40 + 26 * len(ks) + 40
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="sans-serif">' % (W, H),
           '<rect width="100%" height="100%" fill="white"/>',
           '<text x="10" y="22" font-size="14" font-weight="bold">A243 census n = %d: per k, DEAD / REDUCES / ALIVE / pending (%s CPU-h)</text>' % (n, summ["cpu_h"])]
    mx = max(summ["census_by_k"][str(k)]["classes"] for k in ks)
    for i, k in enumerate(ks):
        d = summ["census_by_k"][str(k)]
        y, x = 40 + 26 * i, 70
        out.append('<text x="10" y="%d" font-size="12">k=%d (%d)</text>' % (y + 14, k, d["classes"]))
        for key, col in (("DEAD", COL["DEAD"]), ("REDUCES", COL["REDUCES"]), ("ALIVE", COL["ALIVE"]), ("ERROR", COL["ERROR"]), ("pending", COL["PENDING"])):
            w = 600.0 * d.get(key, 0) / mx
            if w > 0:
                out.append('<rect x="%.1f" y="%d" width="%.1f" height="18" fill="%s"/>' % (x, y, w, col))
                x += w
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for n in [int(a) for a in sys.argv[1:]] or [17, 19]:
        tab = CT.table(n).reload()
        summ = CL.summary(n)
        for name, svg in (("root", page_root(n, tab, summ)), ("record", page_record(n, tab, summ)), ("census", page_census(n, summ))):
            open(os.path.join(OUT, "climb243_n%d_%s.svg" % (n, name)), "w", encoding="utf-8").write(svg)
        print("pages n=%d written to %s" % (n, os.path.relpath(OUT, ROOT)))
