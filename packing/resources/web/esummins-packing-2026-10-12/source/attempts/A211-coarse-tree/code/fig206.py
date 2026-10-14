"""A209 COPY of A206 fig206 (df5aebc9, unchanged; node_note reused). A206 -- the page: per RUN (a loaded A205 leaf under Rule NS, or the whole tree), the root panel (the node after its
refresh cascade) and one panel per closed branch, the tree as a text table beside them; drawing rules as A204/A205
(fig204.panel: pins as pins, a role's pieces thin, its certified K' filled, alive cells grey stipple, a note under every
panel saying what it IS and the seconds).        python fig206.py <nid> | gallery"""
import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CERTS = os.path.join(HERE, "..", "certs")
OUTD = os.path.join(ROOT, "docs", "residue_map", "campaigns", "A206-namedsplit")
sys.path.insert(0, HERE)
import fig204 as F4                                            # noqa: E402  (the A204 copy)
import fig205 as F5                                            # noqa: E402  (the A205 copy: side table, node notes, wrap)

S0, text, defs, panel, wrap = F4.S0, F4.text, F4.defs, F4.panel, F5.wrap
MAXP = 12


def node_note(n):
    kind = str(n.get("kind") or "")
    if not kind.startswith("ns-"):
        return F5.node_note(n)
    col = "#c62828" if n.get("verdict") == "DEAD" else ("#2e7d32" if n.get("verdict") == "ALIVE" else "#333")
    L = [("PANEL = Rule NS branch %s (depth %d): [%s %s %s] (meeting fraction %s; alive anonymous rows %s); pins + H + roles after this node's cascade (%s rounds, %s s; t = %s s)" % (
        n.get("label"), n.get("depth", 0), n.get("role"), "MEETS" if kind == "ns-meets" else "MISSES", n.get("slot"), n.get("frac"), n.get("alive_rows"),
        n.get("n_rounds"), n.get("seconds"), n.get("t")), 6.5, "#000", True)]
    if n.get("verdict") == "DEAD":
        L.append(("DEAD by %s at round %s: %s" % (n.get("clip"), n.get("killed_round"), str(n.get("leaf") or "")[:300]), 6.5, col, True))
    elif n.get("verdict") == "ALIVE":
        L.append(("ALIVE (undecided leaf): %s" % str(n.get("reason") or "")[:300], 6.5, col, True))
    else:
        L.append(("INTERNAL: branched on %s %s" % (n.get("branch_slot"), ("[Rule NS on %s]" % n.get("branch_role")) if n.get("branch_role") else ("over %s" % n.get("branch_rows"))), 6.5, col, False))
    L.append(("roles (slots) %s; forced H %s; misses %s; kept %s; alive cells %s" % (
        n.get("role_slots"), n.get("forced_H"), n.get("miss"), {k: v for k, v in (n.get("kept") or {}).items() if not k.startswith("P")},
        {p.replace("(", "").replace(")", "").replace(",", ""): len(v) for p, v in (n.get("alive_cells") or {}).items()}), 6, "#333", False))
    if n.get("miss_rep"):
        L.append(("MISS-CLIP dropped %s" % [(m.get("role"), m.get("dropped")) for m in n["miss_rep"]], 6, "#333", False))
    if n.get("sclip"):
        L.append(("rule-S clip between roles dropped %s" % [s.get("dropped") for s in n["sclip"]], 6, "#333", False))
    return L


def run_head(doc, key, d):
    col = "#c62828" if d.get("verdict") == "DEAD" else ("#2e7d32" if d.get("verdict") == "ALIVE" else "#555")
    rec = d.get("recorded") or {}
    L = [("RUN %s: %s" % (key, ("A205 leaf %s of %s (recorded %s: %s; roles %s), loaded from its last snapshot (pieces padded outward %s)" % (
        d.get("leaf_label"), d.get("source"), rec.get("verdict"), str(rec.get("reason") or "")[:90], rec.get("roles") and list(rec["roles"]), (d.get("cfg") or {}).get("padding") or "1e-6 / 1e-3 deg"))
        if d.get("mode") == "leaf" else "the WHOLE clip tree of the page under Rule NS from A203's start"), 9, col, True)]
    if d.get("path"):
        L.append(("path to the leaf in A205's tree: %s" % [(p["label"], p["slot"], p["rows"]) for p in d["path"]], 7, "#333", False))
    return L


def page_svg(doc):
    S = 80
    PW = int(S0 * S) + 20
    NH = 96
    ncol = 4
    body = [text(20, 22, "%s -- A206 namedsplit206: Rule NS at the clip tree's fully named leaves (a soft-named role r at a forced slot p is SPLIT: [r meets p] = the exact reach clip at p; [r misses p] = r leaves p's row set, MISS-CLIP; A204's cascade + A205's clips at every node; DEAD iff both branches DEAD; NO LP)" % doc["nid"], 12, "#000", True),
            text(20, 36, "per run: the ROOT panel (the loaded node after its refresh cascade), then one panel per closed branch (first %d); blue = pins; black = H (thin = pieces, filled = certified K'); coloured = instantiated meeters; grey stipple = alive cells of the anonymous option table (never green); yellow = the count's witness" % MAXP, 8, "#444"),
            text(20, 48, "read-only from certs/namedsplit206_%s.json; rendered %s" % (doc["nid"], time.strftime("%Y-%m-%d %H:%M:%S")), 8, "#444")]
    y = 64
    for key, d in (doc.get("runs") or {}).items():
        pad = d.get("pad")
        nodes = [n for n in (d.get("nodes") or []) if n.get("snapshot")]
        show = nodes[:1] + [n for n in nodes[1:] if n.get("verdict") in ("DEAD", "ALIVE")][:MAXP - 1]
        nrow = max(1, (len(show) + ncol - 1) // ncol)
        y = wrap(body, 20, y + 10, run_head(doc, key, d), 260) + 4
        ys = F5.side(dict(doc, pads={pad: d}), pad, body, 20 + ncol * PW + 10, y + 12)
        for k, n in enumerate(show):
            ox, oy = 20 + (k % ncol) * PW, y + (k // ncol) * (S0 * S + NH + 12)
            panel(doc, dict(n["snapshot"], pad=pad), body, ox, oy, S, small=False)
            wrap(body, ox, oy + S0 * S + 10, node_note(n), 80)
        y = max(y + nrow * (S0 * S + NH + 12) + 30, ys + 20)
    W = 20 + ncol * PW + 10 + 1000
    return "\n".join(['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="Segoe UI, sans-serif" style="background:#fff">' % (W, y + 20), defs()] + body + ["</svg>"])


def render(doc):
    os.makedirs(OUTD, exist_ok=True)
    p = os.path.join(OUTD, "namedsplit206_%s.svg" % doc["nid"])
    open(p, "w", encoding="utf-8").write(page_svg(doc))
    return p


def gallery():
    S = 52
    PW = int(S0 * S) + 16
    PH = PW + 44
    ncol = 6
    docs = []
    for f in sorted(glob.glob(os.path.join(CERTS, "namedsplit206_*.json"))):
        try:
            docs.append(json.load(open(f, encoding="utf-8")))
        except Exception:
            continue
    body = [text(16, 20, "A206 namedsplit206 -- Rule NS at the clip tree's fully named leaves, one thumbnail per page (the first run's root node; red = a run DEAD, green = ALIVE with undecided leaves); rendered %s" % time.strftime("%Y-%m-%d %H:%M:%S"), 12, "#000", True)]
    for k, doc in enumerate(docs):
        runs = doc.get("runs") or {}
        first = next(iter(runs.values()), {}) if runs else {}
        nodes = [n for n in (first.get("nodes") or []) if n.get("snapshot")]
        ox, oy = 16 + (k % ncol) * PW, 40 + (k // ncol) * PH
        if nodes:
            panel(doc, dict(nodes[0]["snapshot"], pad=first.get("pad")), body, ox, oy, S, small=True)
        dead = [(key, v) for key, v in runs.items() if v.get("verdict") == "DEAD"]
        body.append(text(ox, oy + S0 * S + 11, doc["nid"].replace("_interior", ""), 8, "#000", True))
        body.append(text(ox, oy + S0 * S + 21, ("DEAD %s" % ", ".join("%s (%sn)" % (key, v.get("n_nodes")) for key, v in dead))[:60] if dead else
                         ("ALIVE %s" % ", ".join("%s %sn %sd/%sa" % (key, v.get("n_nodes"), v.get("dead_leaves"), v.get("alive_leaves")) for key, v in runs.items()))[:60],
                         6.5, "#c62828" if dead else "#2e7d32"))
        body.append(text(ox, oy + S0 * S + 31, "NS splits %s" % sum(int(v.get("ns_splits") or 0) for v in runs.values()), 6.5, "#555"))
    nrow = max(1, (len(docs) + ncol - 1) // ncol)
    os.makedirs(OUTD, exist_ok=True)
    p = os.path.join(OUTD, "namedsplit206_gallery.svg")
    open(p, "w", encoding="utf-8").write("\n".join(['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="Segoe UI, sans-serif" style="background:#fff">' % (ncol * PW + 32, 40 + nrow * PH), defs()] + body + ["</svg>"]))
    return p


if __name__ == "__main__":
    if sys.argv[1] == "gallery":
        print(gallery())
    else:
        print(render(json.load(open(os.path.join(CERTS, "namedsplit206_%s.json" % sys.argv[1]), encoding="utf-8"))))
