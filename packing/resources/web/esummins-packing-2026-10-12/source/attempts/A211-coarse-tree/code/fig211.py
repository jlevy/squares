"""A211 (fig209 adapted) -- the page (A206's fig206 layout on A209's certificate): the stage-0 line per pad, then per RUN the root panel and
one panel per closed branch, the tree as a text table beside them, the pad-0 verdict printed beside the window verdict;
drawing rules as A204/A205/A206 (fig204.panel).        python fig209.py <nid> | gallery"""
import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CERTS = os.path.join(HERE, "..", "certs")
OUTD = os.path.join(ROOT, "docs", "residue_map", "campaigns", "A211-coarsetree")
sys.path.insert(0, HERE)
import fig204 as F4                                            # noqa: E402
import fig205 as F5                                            # noqa: E402
import fig206 as F6                                            # noqa: E402
import pstats211 as PS                                         # noqa: E402  (A225: the PROGRESS block)

S0, text, defs, panel, wrap = F4.S0, F4.text, F4.defs, F4.panel, F5.wrap
MAXP = 12


def node_note(n):
    kind = str(n.get("kind") or "")
    if kind == "pocket":
        col = "#c62828" if n.get("verdict") == "DEAD" else ("#2e7d32" if n.get("verdict") == "ALIVE" else "#333")
        L = [("PANEL = Lemma POCKET branch %s (depth %d): the 10th square's centre in pocket %s (diameter %s) instantiated as %s; pins + H + roles after this node's cascade (%s rounds, %s s; t = %s s)" % (
            n.get("label"), n.get("depth", 0), n.get("pocket"), n.get("diam"), n.get("pocket_role"), n.get("n_rounds"), n.get("seconds"), n.get("t")), 6.5, "#000", True)]
    elif kind == "inherited":
        return [("%s: DEAD INHERITED (Lemma INHERIT) from %s %s -- %s" % (n.get("label"), n.get("source_camp"), n.get("source_label"), n.get("source_cert")), 6.5, "#777", True),
                (str(n.get("leaf"))[:300], 6.5, "#777", False)]
    else:
        L = F6.node_note(n)
        col = "#c62828" if n.get("verdict") == "DEAD" else "#2e7d32"
    if kind == "rsplit":
        L = [("PANEL = Lemma ROLE-SPLIT branch %s (depth %d): the role %s bisected, this half %s (the parent's no-room was UNDECIDED and the role's box was wide; the two halves are exhaustive, notes/coarse_tree.md s.5); pins + H + roles after this node's cascade (%s rounds, %s s; t = %s s)" % (
            n.get("label"), n.get("depth", 0), n.get("slot"), (n.get("rows") or [""])[0], n.get("n_rounds"), n.get("seconds"), n.get("t")), 6.5, col, True)]
    if kind == "exact":
        L = [("PANEL = the EXACT cascade (leaf rule e: nsub 4 / refine 2, lonely clip, basins, %s rounds) at the fully named leaf %s after the coarse rules; %s s; t = %s s" % (n.get("n_rounds"), n.get("label"), n.get("seconds"), n.get("t")), 6.5, col, True)]
    if n.get("coarse"):
        L.append(("COARSE node: pieces re-binned to <= 96 units per role %s, refine 1, <= 2 mutual passes, no lonely clip, reach depth 2 (a SUPERSET of the exact node: sound); n_pieces %s" % (n.get("rebin") and [(r["role"], r["n_before"], r["n_after"]) for r in n["rebin"]], n.get("n_pieces")), 6.5, "#555", False))
    if n.get("clip") == "CC":
        L.append(("DEAD by rule CC (Lemma CORNER-COVER) at slot %s, corner square %s: %s" % (n.get("cc_slot"), n.get("cc_role"), str(n.get("leaf") or "")[:300]), 6.5, "#c62828", True))
    if n.get("noroom"):
        r = n["noroom"]
        L.append(("NO-ROOM leaf (A189 Lemma 1 on the role boxes, k=%s, m=%s): %s%s; %s pockets; %s s" % (r.get("k"), r.get("m"), r.get("verdict"), (" by " + r["clip"]) if r.get("clip") else "", r.get("n_pockets"), r.get("seconds")), 6.5, col, True))
    if n.get("rsplit"):
        r = n["rsplit"]
        L.append(("Lemma ROLE-SPLIT here: %s bisected on %s at %s (extents x %s / y %s, tilt %s deg; core %s; split %s of %s) -- both halves below" % (
            r.get("role"), r.get("dim"), r.get("m"), (r.get("extents") or {}).get("x"), (r.get("extents") or {}).get("y"), (r.get("extents") or {}).get("tilt"),
            "EMPTY" if r.get("core_empty") else "non-empty", (r.get("n_splits") or 0) + 1, 4), 6.5, "#1565c0", True))
    if kind == "pocket" and n.get("verdict") == "DEAD":
        L.append(("DEAD by %s at round %s: %s" % (n.get("clip"), n.get("killed_round"), str(n.get("leaf") or "")[:300]), 6.5, col, True))
    return L


def stage_lines(doc):
    L = []
    for pad, s in (doc.get("stage0") or {}).items():
        col = "#c62828" if s.get("verdict") == "DEAD" else "#2e7d32"
        L.append(("STAGE 0 (%s pad): %s -- %s [%s; kills %s; CSP units alive %s/%s; %s s]%s" % (
            pad, s.get("verdict"), s.get("source"), s.get("file"), s.get("kills"), s.get("n_units_alive"), s.get("n_units"), s.get("seconds"), ("; " + str(s.get("leaf"))[:160]) if s.get("leaf") else ""), 8, col, True))
    v = doc.get("verdicts") or {}
    L.append(("VERDICTS: window pad (g1, lam = 1.004) = %s | pad 0 (lam = 1, s0-only, WINDOW-PENDING) = %s   (a page is KILLED only by a DEAD g1 verdict; every kill [C: closed-form / library clip trace + the leaf lemma (CORNER-COVER / A189 Lemma 1 / Lemma CN / Lemma BASIN)], no verifier clause)" % (
        v.get("g1", "not run"), v.get("zero", "not run")), 9, "#000", True))
    return L


def run_head(doc, key, d):
    col = "#c62828" if d.get("verdict") == "DEAD" else ("#2e7d32" if d.get("verdict") == "ALIVE" else "#555")
    L = [("RUN %s: the COARSE tree from %s -- coarse internal nodes (one round, re-binned pieces, refine 1, no lonely clip), the leaf rules at every fully named leaf: rule CC -> no-room + pockets -> basin clip (basins %s) -> Rule NS -> Lemma ROLE-SPLIT -> the exact cascade; verdict %s in %s s; %s nodes, depth %s, %s CC kills, %s exact leaf cascades, %s NS splits, %s pocket splits, %s role splits, %s inherited kills" % (
        key, d.get("source"), [(b.get("cell"), b.get("r_c")) for b in (d.get("basins") or [])] or "none certified", d.get("verdict"), d.get("seconds"), d.get("n_nodes"), d.get("max_depth"), d.get("cc_kills"), d.get("exact_rounds"), d.get("ns_splits"), d.get("pocket_splits"), d.get("rsplits"), len(d.get("inherited") or {})), 9, col, True)]
    if d.get("leaf"):
        L.append((str(d["leaf"])[:600], 7, col, False))
    return L


def progress_lines(nid, pad):
    """A225 (the PI 2026-09-14 23:40: "how many top-level nodes are left ... how deep it's going"):
    the PROGRESS block -- the START NODES of this run (the alive leaves inherited from the previous run),
    one line each with its verdict / nodes / depth reached / seconds, then the cumulative line over every
    run of this page at this pad, then the one-line estimate.  Read from results/coarsetree211.jsonl only."""
    try:
        st = PS.page_stats(nid, pad)
    except Exception as e:                                       # a figure never fails on a bad jsonl line
        return [("PROGRESS: unavailable (%s)" % e, 7, "#777", False)]
    if not st:
        return [("PROGRESS: no run of %s at the %s pad is recorded in results/coarsetree211.jsonl" % (nid, pad), 7, "#777", False)]
    hot = "#c62828" if st["left"] else "#2e7d32"
    L = [(PS.fmt_head(st), 9, hot, True),
         ("start node        steps  verdict   nodes  depth (abs)   seconds   -- the top-level branches of THIS run, in the order the run took them", 7.5, "#000", True)]
    for s in st["starts"]:
        c = "#c62828" if s["verdict"] == "DEAD" else ("#2e7d32" if s["verdict"] == "ALIVE" else "#888")
        L.append(("%-34s %-6s %-9s %-6s %-2s (abs %-3s) %8.1f%s" % (
            s["label"], s["n_steps"], s["verdict"], s["n_nodes"] or "-", s["depth"], s["abs_depth"], s["seconds"],
            "   PENDING -- the wall ran out before this start node ran" if not s["reached"] else
            ("   still ALIVE at the wall: it becomes a start node of the next run" if s["verdict"] != "DEAD" else "")), 7, c, False))
    L.append((PS.fmt_cum(st), 8, "#000", True))
    L.append((PS.fmt_est(st), 7.5, "#555", False))
    L.append(("(a start node is an alive leaf of the previous run, Lemma INHERIT; depth abs = the start node's own path "
              "length + the depth this run added below it; the node table below lists every node of this run)", 6.5, "#777", False))
    return L


def side(doc, pad, body, x, y):
    """A205's side table with the INHERITED rows in GREY, each citing the certificate that closed the branch."""
    d = doc["pads"].get(pad) or {}
    col = "#c62828" if d.get("verdict") == "DEAD" else ("#2e7d32" if d.get("verdict") == "ALIVE" else "#555")
    inh = d.get("inherit") or {}
    L = progress_lines(doc["nid"], pad) + [("", 6, "#000", False)]
    L += [("%s  pad %s  A211 COARSE TREE from the MERGED prior state: %s  (%s s; %s nodes, depth %s; %s dead / %s alive leaves%s)" % (
        doc["nid"], pad, d.get("verdict"), d.get("seconds"), d.get("n_nodes"), d.get("max_depth"), d.get("dead_leaves"), d.get("alive_leaves"),
        "; WALL" if d.get("wall") else ""), 11, col, True),
        ("Lemma INHERIT (notes/coarse_tree.md s.4): %s prior tree(s) %s merged on the path key; %s branch(es) inherited DEAD (FINAL, grey below, each with its certificate); %s start node(s) run here: %s" % (
            inh.get("n_trees"), [t.get("camp") for t in (inh.get("trees") or [])], d.get("inherited_dead"), d.get("inherited_alive"),
            [(s.get("label"), s.get("camp"), s.get("anc_label"), s.get("steps")) for s in (d.get("start_nodes") or [])][:10]), 7, "#555", False)]
    if d.get("leaf"):
        L.append((str(d["leaf"])[:500], 7.5, col, False))
    st = d.get("start") or {}
    L.append(("start = %s (%s): H box %s, forced H %s, H units %s alive of %s; cfg %s" % (
        st.get("source"), st.get("file"), st.get("H_box"), st.get("forced_H"), st.get("n_units_alive"), st.get("n_units"), d.get("cfg")), 7, "#333", False))
    L.append(("verdict label %s" % d.get("verifier"), 6.5, "#555", False))
    L.append(("label        depth  slot      <- rows          kind   verdict   clip     round  seconds  t     source", 8, "#000", True))
    for n in d.get("nodes") or []:
        c = "#777" if n.get("kind") == "inherited" else ("#c62828" if n.get("verdict") == "DEAD" else ("#2e7d32" if n.get("verdict") == "ALIVE" else "#333"))
        tail = ("  <- %s %s [%s] %s" % (n.get("source_camp"), n.get("source_label"), n.get("source_rule"),
                                        os.path.basename(str(n.get("source_cert"))))) if n.get("kind") == "inherited" else (
            ("  " + str(n.get("reason"))[:70]) if n.get("reason") else "")
        L.append(("%-12s %-6s %-9s %-16s %-6s %-9s %-8s %-6s %-8s %s%s" % (
            n.get("label"), n.get("depth"), n.get("slot") or "root", str(n.get("rows") or ""), n.get("kind") or "", n.get("verdict"), n.get("clip") or "-",
            n.get("killed_round") or "-", n.get("seconds"), n.get("t"), tail), 7, c, False))
    for n in d.get("nodes") or []:
        if n.get("kind") == "inherited":
            L.append(("INHERITED %-12s %s<-%s  FINAL by %s %s [%s]%s: %s" % (
                n.get("label"), n.get("slot"), n.get("rows"), n.get("source_camp"), n.get("source_label"), n.get("source_rule"),
                ("  ledger " + str(n.get("source_ledger"))) if n.get("source_ledger") else "", n.get("source_cert")), 6.5, "#777", False))
    for r in d.get("runs_started") or d.get("runs") or []:
        if isinstance(r, dict) and r.get("label"):
            L.append(("start run %-12s %s in %s s (from %s %s; steps applied %s)" % (
                r.get("label"), r.get("verdict"), r.get("seconds"), r.get("cert"), r.get("anc"), r.get("applied")), 7, "#333", False))
    L.append(("window pending: %s; lam %s; rendered %s" % (d.get("window_pending"), d.get("lam"), time.strftime("%Y-%m-%d %H:%M:%S")), 7, "#555", False))
    return wrap(body, x, y, L, 150)


def page_svg(doc):
    S = 80
    PW = int(S0 * S) + 20
    NH = 110
    ncol = 4
    body = [text(20, 22, "%s -- A211 coarsetree211: the COARSE tree (cheap coarse internal nodes; at every fully named leaf: rule CC -> no-room + pockets -> basin clip -> Rule NS -> Lemma ROLE-SPLIT -> the exact cascade last; pad 0 first); NO LP" % doc["nid"], 12, "#000", True),
            text(20, 36, "per run: the ROOT panel, then one panel per closed branch (first %d); blue = pins; black = H (thin = pieces, filled = certified K'); coloured = instantiated meeters; grey stipple = alive cells of the anonymous option table (never green); yellow = the count's witness" % MAXP, 8, "#444"),
            text(20, 48, "read-only from certs/coarsetree211_%s.json (record %s); rendered %s" % (doc["nid"], doc.get("record"), time.strftime("%Y-%m-%d %H:%M:%S")), 8, "#444")]
    y = wrap(body, 20, 62, stage_lines(doc), 300) + 4
    for key, d in (doc.get("runs") or {}).items():
        pad = d.get("pad")
        nodes = [n for n in (d.get("nodes") or []) if n.get("snapshot")]
        show = nodes[:1] + [n for n in nodes[1:] if n.get("verdict") in ("DEAD", "ALIVE")][:MAXP - 1]
        nrow = max(1, (len(show) + ncol - 1) // ncol)
        y = wrap(body, 20, y + 10, run_head(doc, key, d), 300) + 4
        ys = side(dict(doc, pads={pad: d}), pad, body, 20 + ncol * PW + 10, y + 12)
        for k, n in enumerate(show):
            ox, oy = 20 + (k % ncol) * PW, y + (k // ncol) * (S0 * S + NH + 12)
            panel(doc, dict(n["snapshot"], pad=pad), body, ox, oy, S, small=False)
            wrap(body, ox, oy + S0 * S + 10, node_note(n), 80)
        y = max(y + nrow * (S0 * S + NH + 12) + 30, ys + 20)
    W = 20 + ncol * PW + 10 + 1000
    return "\n".join(['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="Segoe UI, sans-serif" style="background:#fff">' % (W, y + 20), defs()] + body + ["</svg>"])


def render(doc):
    os.makedirs(OUTD, exist_ok=True)
    p = os.path.join(OUTD, "coarsetree211_%s.svg" % doc["nid"])
    open(p, "w", encoding="utf-8").write(page_svg(doc))
    return p


def gallery():
    S = 52
    PW = int(S0 * S) + 16
    PH = PW + 54                                                 # A225: + the PROGRESS line
    ncol = 6
    docs = []
    for f in sorted(glob.glob(os.path.join(CERTS, "coarsetree211_*.json"))):
        try:
            docs.append(json.load(open(f, encoding="utf-8")))
        except Exception:
            continue
    body = [text(16, 20, "A211 coarsetree211 -- the coarse tree over the alive k5 pages and the k5 frontier, one thumbnail per node (red = DEAD at the window pad, green = ALIVE; the pad-0 verdict beside it); rendered %s" % time.strftime("%Y-%m-%d %H:%M:%S"), 12, "#000", True),
            text(16, 33, "A225 PROGRESS, last line of each still-alive thumbnail: START NODES LEFT (the top-level branches of the current run not yet closed) / ALIVE LEAVES now (the next run's start nodes) / MAX DEPTH reached (absolute)", 8, "#c62828")]
    for k, doc in enumerate(docs):
        runs = doc.get("runs") or {}
        v = doc.get("verdicts") or {}
        first = next(iter(runs.values()), {}) if runs else {}
        nodes = [n for n in (first.get("nodes") or []) if n.get("snapshot")]
        ox, oy = 16 + (k % ncol) * PW, 52 + (k // ncol) * PH
        if nodes:
            panel(doc, dict(nodes[0]["snapshot"], pad=first.get("pad")), body, ox, oy, S, small=True)
        dead = v.get("g1") == "DEAD"
        body.append(text(ox, oy + S0 * S + 11, doc["nid"].replace("_interior", ""), 8, "#000", True))
        body.append(text(ox, oy + S0 * S + 21, ("g1 %s | pad0 %s" % (v.get("g1", "-"), v.get("zero", "-")))[:60], 6.5, "#c62828" if dead else "#2e7d32"))
        body.append(text(ox, oy + S0 * S + 31, ("stage %s; %s nodes" % (doc.get("stage_reached"), sum(int(r.get("n_nodes") or 0) for r in runs.values())))[:60], 6.5, "#555"))
        # A225 PROGRESS: on a page still ALIVE somewhere, how much of the top level is left and how deep it went
        pr = ""
        for p in ("g1", "zero"):
            try:
                s = PS.page_stats(doc["nid"], p)
            except Exception:
                s = None
            if s and s.get("verdict") != "DEAD":
                pr = "%s: %s" % (p, PS.fmt_short(s))
                break
        body.append(text(ox, oy + S0 * S + 41, pr[:60], 6.5, "#c62828" if pr else "#555"))
    nrow = max(1, (len(docs) + ncol - 1) // ncol)
    os.makedirs(OUTD, exist_ok=True)
    p = os.path.join(OUTD, "coarsetree211_gallery.svg")
    open(p, "w", encoding="utf-8").write("\n".join(['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="Segoe UI, sans-serif" style="background:#fff">' % (ncol * PW + 32, 52 + nrow * PH), defs()] + body + ["</svg>"]))
    return p


if __name__ == "__main__":
    if sys.argv[1] == "gallery":
        print(gallery())
    else:
        print(render(json.load(open(os.path.join(CERTS, "coarsetree211_%s.json" % sys.argv[1]), encoding="utf-8"))))
