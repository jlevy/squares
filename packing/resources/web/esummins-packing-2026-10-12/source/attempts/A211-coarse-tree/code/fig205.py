"""A205 -- the page: per pad, the ROOT panel (the node after the root cascade) and one panel per CLOSED branch of the clip
tree (its last cascade snapshot), drawn from certs/cliptree205_<nid>.json after the root cascade and after every closed
branch; the tree as a text table (branch -> verdict -> seconds) beside the panels.  Drawing rules as A204's fig204.panel
(pins as pins; a role's pieces thin, its certified K' filled; the hypothesis square only at an admissible pose; alive
cells grey stipple never green; a note under every panel saying what it IS and the seconds).
      python fig205.py <nid> | gallery"""
import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CERTS = os.path.join(HERE, "..", "certs")
OUTD = os.path.join(ROOT, "docs", "residue_map", "campaigns", "A205-cliptree")
sys.path.insert(0, HERE)
import fig204 as F4                                            # noqa: E402  (the A204 copy: panel / text / defs)

S0, text, defs, panel = F4.S0, F4.text, F4.defs, F4.panel
MAXP = 12


def wrap(body, x, y, lines, w=95):
    for t, sz, c, b in lines:
        t = str(t)
        while True:
            body.append(text(x, y, t[:w], sz, c, b))
            y += sz + 2
            t = t[w:]
            if not t:
                break
    return y


def node_note(n):
    col = "#c62828" if n.get("verdict") == "DEAD" else ("#2e7d32" if n.get("verdict") == "ALIVE" else "#333")
    what = "ROOT: the node after the root cascade" if n.get("label") == "R" else "branch %s (depth %d): %s <- rows %s (%s%s)" % (
        n.get("label"), n.get("depth", 0), n.get("slot"), n.get("rows"), n.get("kind"), "; unit propagation" if n.get("unit") else "")
    L = [("PANEL = %s; pins + H + instantiated roles after this node's cascade (%s rounds, %s s; t = %s s of the pad's wall)" % (
        what, n.get("n_rounds"), n.get("seconds"), n.get("t")), 6.5, "#000", True)]
    if n.get("verdict") == "DEAD":
        L.append(("DEAD by %s at round %s: %s" % (n.get("clip"), n.get("killed_round"), str(n.get("leaf") or "")[:300]), 6.5, col, True))
    elif n.get("verdict") == "ALIVE":
        L.append(("ALIVE (undecided leaf): %s" % str(n.get("reason") or "")[:300], 6.5, col, True))
    else:
        L.append(("INTERNAL: branched on %s over %s" % (n.get("branch_slot"), n.get("branch_rows")), 6.5, col, False))
    L.append(("roles (slots) %s; forced H %s; kept %s; alive cells %s" % (
        n.get("role_slots"), n.get("forced_H"), {k: v for k, v in (n.get("kept") or {}).items() if not k.startswith("P")},
        {p.replace("(", "").replace(")", "").replace(",", ""): len(v) for p, v in (n.get("alive_cells") or {}).items()}), 6, "#333", False))
    if n.get("sclip"):
        L.append(("rule-S clip between roles dropped %s" % [s.get("dropped") for s in n["sclip"]], 6, "#333", False))
    if n.get("hc_dead"):
        L.append(("Lemma HC rows dead: %d (first %s)" % (len(n["hc_dead"]), n["hc_dead"][:3]), 6, "#333", False))
    return L


def side(doc, pad, body, x, y):
    d = doc["pads"].get(pad) or {}
    col = "#c62828" if d.get("verdict") == "DEAD" else ("#2e7d32" if d.get("verdict") == "ALIVE" else "#555")
    L = [("%s  pad %s  A205 CLIP TREE: %s  (%s s; %s nodes, depth %s; %s dead / %s alive leaves%s)" % (
        doc["nid"], pad, d.get("verdict"), d.get("seconds"), d.get("n_nodes"), d.get("max_depth"), d.get("dead_leaves"), d.get("alive_leaves"),
        "; WALL" if d.get("wall") else ""), 11, col, True)]
    if d.get("leaf"):
        L.append((str(d["leaf"])[:400], 7.5, col, False))
    st = d.get("start") or {}
    L.append(("start = %s (%s): H box %s, forced H %s, H units %s alive of %s; cfg %s" % (
        st.get("source"), st.get("file"), st.get("H_box"), st.get("forced_H"), st.get("n_units_alive"), st.get("n_units"), d.get("cfg")), 7, "#333", False))
    L.append(("verdict label %s" % d.get("verifier"), 6.5, "#555", False))
    L.append(("label        depth  slot      <- rows          kind   verdict   clip     round  seconds  t", 8, "#000", True))
    for n in d.get("nodes") or []:
        c = "#c62828" if n.get("verdict") == "DEAD" else ("#2e7d32" if n.get("verdict") == "ALIVE" else "#333")
        L.append(("%-12s %-6s %-9s %-16s %-6s %-9s %-8s %-6s %-8s %s%s" % (
            n.get("label"), n.get("depth"), n.get("slot") or "root", str(n.get("rows") or ""), n.get("kind") or "", n.get("verdict"), n.get("clip") or "-",
            n.get("killed_round") or "-", n.get("seconds"), n.get("t"), ("  " + str(n.get("reason"))[:70]) if n.get("reason") else ""), 7, c, False))
    L.append(("window pending: %s; lam %s; rendered %s" % (d.get("window_pending"), d.get("lam"), time.strftime("%Y-%m-%d %H:%M:%S")), 7, "#555", False))
    return wrap(body, x, y, L, 150)


def page_svg(doc):
    S = 80
    PW = int(S0 * S) + 20
    NH = 84
    ncol = 4
    body = [text(20, 22, "%s%s -- A205 cliptree205: the CLIP TREE (branch on a forced slot's remaining meeter rows, instantiate, A204's cascade + rule-S clip at every node, the count with A203's pair table; a branch dies by EmptyBox / S-CLIP / FC / REACH / COUNT / NOROOM / S-PAIR; NO LP)" % (doc["nid"], (" [EXTENDED run %s: its own wall / caps, not the 900 s row]" % doc["tag"]) if doc.get("tag") else ""), 12, "#000", True),
            text(20, 36, "per pad (g1 = the page's window, then pad 0 = s0-only, WINDOW-PENDING): the ROOT panel, then one panel per closed branch (first %d); blue = pins; black = H (thin = pieces, filled = certified K'); coloured = instantiated meeters (forced by Theorem FC or by the branch); grey stipple = alive cells of the anonymous option table (never green); yellow = the count's witness" % MAXP, 8, "#444"),
            text(20, 48, "read-only from certs/cliptree205_%s.json; rendered %s" % (doc["nid"], time.strftime("%Y-%m-%d %H:%M:%S")), 8, "#444")]
    y = 64
    for pad in ("g1", "zero"):
        d = doc["pads"].get(pad)
        if not d:
            continue
        nodes = [n for n in (d.get("nodes") or []) if n.get("snapshot")]
        show = nodes[:1] + [n for n in nodes[1:] if n.get("verdict") in ("DEAD", "ALIVE")][:MAXP - 1]
        nrow = max(1, (len(show) + ncol - 1) // ncol)
        ys = side(doc, pad, body, 20 + ncol * PW + 10, y + 12)
        for k, n in enumerate(show):
            ox, oy = 20 + (k % ncol) * PW, y + (k // ncol) * (S0 * S + NH + 12)
            panel(doc, dict(n["snapshot"], pad=pad), body, ox, oy, S, small=False)
            wrap(body, ox, oy + S0 * S + 10, node_note(n), 80)
        y = max(y + nrow * (S0 * S + NH + 12) + 30, ys + 20)
    W = 20 + ncol * PW + 10 + 1000
    return "\n".join(['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="Segoe UI, sans-serif" style="background:#fff">' % (W, y + 20), defs()] + body + ["</svg>"])


def render(doc):
    os.makedirs(OUTD, exist_ok=True)
    p = os.path.join(OUTD, "cliptree205_%s%s.svg" % (doc["nid"], doc.get("tag") or ""))
    open(p, "w", encoding="utf-8").write(page_svg(doc))
    return p


def gallery():
    S = 52
    PW = int(S0 * S) + 16
    PH = PW + 34
    ncol = 6
    docs = []
    for f in sorted(glob.glob(os.path.join(CERTS, "cliptree205_*.json"))):
        try:
            docs.append(json.load(open(f, encoding="utf-8")))
        except Exception:
            continue
    body = [text(16, 20, "A205 cliptree205 -- the clip tree over A204's survivors, one thumbnail per page (the root node at the g1 pad; red = DEAD at some pad, green = ALIVE with undecided leaves); rendered %s" % time.strftime("%Y-%m-%d %H:%M:%S"), 12, "#000", True)]
    for k, doc in enumerate(docs):
        d = doc["pads"].get("g1") or {}
        nodes = [n for n in (d.get("nodes") or []) if n.get("snapshot")]
        ox, oy = 16 + (k % ncol) * PW, 40 + (k // ncol) * PH
        if nodes:
            panel(doc, dict(nodes[0]["snapshot"], pad="g1"), body, ox, oy, S, small=True)
        dead = [(p, v) for p, v in doc["pads"].items() if v.get("verdict") == "DEAD"]
        body.append(text(ox, oy + S0 * S + 11, doc["nid"].replace("_interior", ""), 8, "#000", True))
        body.append(text(ox, oy + S0 * S + 21, ("DEAD pad %s: %s nodes" % (dead[0][0], dead[0][1].get("n_nodes"))) if dead else
                         "ALIVE (%s)" % ", ".join("%s %sn %sd/%sa" % (p, v.get("n_nodes"), v.get("dead_leaves"), v.get("alive_leaves")) for p, v in doc["pads"].items()),
                         7, "#c62828" if dead else "#2e7d32"))
    nrow = max(1, (len(docs) + ncol - 1) // ncol)
    os.makedirs(OUTD, exist_ok=True)
    p = os.path.join(OUTD, "cliptree205_gallery.svg")
    open(p, "w", encoding="utf-8").write("\n".join(['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="Segoe UI, sans-serif" style="background:#fff">' % (ncol * PW + 32, 40 + nrow * PH), defs()] + body + ["</svg>"]))
    return p


if __name__ == "__main__":
    if sys.argv[1] == "gallery":
        print(gallery())
    else:
        print(render(json.load(open(os.path.join(CERTS, "cliptree205_%s.json" % sys.argv[1]), encoding="utf-8"))))
