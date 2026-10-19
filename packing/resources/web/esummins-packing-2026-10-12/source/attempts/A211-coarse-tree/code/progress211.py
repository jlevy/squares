"""A211 (A209 copy) -- results/progress.md: the table (page, pad, stage reached, verdict, seconds) over every node run so far, the
gallery block first; the frontier PRICE (mean / median wall seconds per node over the first 20 frontier nodes) and the
PROJECTION over the remaining census; writes logs/STOP when the projection exceeds 200 CPU-h (the workers then exit).
Run after every node by the worker (and so at least hourly while anything runs)."""
import collections
import json
import os
import statistics
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import load211 as L                                            # noqa: E402
import pstats211 as PS                                         # noqa: E402  (A225: the PROGRESS numbers)

RES = os.path.join(HERE, "..", "results", "coarsetree211.jsonl")
OUT = os.path.join(HERE, "..", "results", "progress.md")
STOP = os.path.join(HERE, "..", "logs", "STOP")
CAP_CPUH = 200.0


def alive_block(L2, per, gnodes):
    """A225 (the PI 2026-09-14 23:40: "how many top-level nodes are left ... how deep it's going"): where the
    still-alive pages stand.  A run starts from the ALIVE leaves of the previous run (Lemma INHERIT): the work
    left on a page is the start nodes it has not closed; the depth is absolute (start-node path + this run's depth)."""
    alive = [n for n in gnodes if (per[n].get("g1") or {}).get("verdict") != "DEAD"]
    L2.append("## Where the alive k5 gallery pages stand (A225 PROGRESS: start nodes left / alive leaves / depth)")
    L2.append("")
    L2.append("A *start node* is an alive leaf the run inherited from the previous run (Lemma INHERIT, notes/coarse_tree.md s.4) -- "
              "the top-level branches of the current run.  *Left* = alive at the wall + never reached.  *Alive leaves* = the start "
              "nodes of the NEXT run.  *Depth* = absolute (the start node's own path length + the depth the run added below it).")
    L2.append("")
    L2.append("| page | pad | start nodes | dead this run | alive at wall | not reached | **left** | alive leaves | max depth | runs | wall (CPU-h) | estimate (CPU-h) | last run |")
    L2.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    tot = dict(left=0, leaves=0, wall=0.0, runs=0, est=0.0, depth=0)
    for n in alive:
        for pad in ("g1", "zero"):
            st = PS.page_stats(n, pad)
            if not st:
                continue
            L2.append("| %s | %s | %d | %d | %d | %d | **%d** | %d | %d | %d | %.2f | %.2f | %s%s |" % (
                n, pad, st["n_start"], st["dead"], st["alive"], st["unreached"], st["left"], st["alive_leaves"],
                st["max_abs_ever"], st["n_runs"], st["wall_total"] / 3600.0, st["est_s"] / 3600.0,
                st["when"], "" if st["verdict"] != "DEAD" else " (**this pad is now DEAD**)"))
            if pad == "g1":
                tot["left"] += st["left"]
                tot["leaves"] += st["alive_leaves"]
                tot["est"] += st["est_s"] / 3600.0
                tot["depth"] = max(tot["depth"], st["max_abs_ever"])
            tot["wall"] += st["wall_total"] / 3600.0
            tot["runs"] += st["n_runs"]
    L2.append("")
    L2.append("**TOTAL over the %d alive k5 gallery pages (g1 pad = A57's G1 slab (3.861637, s0], s-hat incl. -- NOT the window; A270):** %d start nodes left, %d alive leaves (the next runs' "
              "start nodes), deepest branch %d, %d run(s) over both pads for %.2f CPU-h spent; ESTIMATE (not a bound) %.2f CPU-h "
              "to close the start nodes now open at the g1 pad -- an UNDER-estimate: the start nodes still alive are the ones "
              "that already survived a full wall, and each survivor splits into several new start nodes."
              % (len(alive), tot["left"], tot["leaves"], tot["depth"], tot["runs"], tot["wall"], tot["est"]))
    L2.append("")


def main():
    rows = L.jl(RES)
    gal = set(L.gallery_nids())
    per = collections.OrderedDict()                              # nid -> {pad: row}
    for d in rows:
        if d.get("mode") != "page" or not d.get("nid"):
            continue
        per.setdefault(d["nid"], {})[d.get("pad")] = d
    gnodes = [n for n in per if n in gal]
    fnodes = [n for n in per if n not in gal]
    census = L.census()
    remaining = [c for c in census if c["nid"] not in per]
    L2 = ["# A211 progress -- %s" % time.strftime("%Y-%m-%d %H:%M:%S"), "",
          "The COARSE tree (notes/coarse_tree.md): A202 stage 0 + A203 CSP; coarse internal nodes (re-binned pieces <= 96 units, refine 1, no lonely clip, reach depth 2; ONE round; branch at once); "
          "at every fully named leaf: rule CC (Lemma CORNER-COVER) -> A208 no-room + pocket CN bound (pockets branched at k = 9) -> A207 basin clip -> A206 Rule NS (MAX_FRAC 0.5) -> the exact cascade + sharp round.  "
          "Pad 0 FIRST then the g1 pad (lam = s0/3.861637: A57's G1 slab (3.861637, s0], s-hat included -- NOT the window [3.82, s0]; A270); wall 1800 s per pad per page; depth cap 6; node cap 600; every kill [C: closed-form / library clip trace + the leaf lemma], no verifier clause.", ""]

    def table(nodes, title):
        L2.append("## %s (%d nodes)" % (title, len(nodes)))
        L2.append("")
        L2.append("| page | pad | stage reached | verdict | seconds |")
        L2.append("|---|---|---|---|---|")
        tot = 0.0
        for n in nodes:
            for pad in ("g1", "zero"):
                d = per[n].get(pad)
                if d is None:
                    continue
                st = "0" if d.get("stage0_kill") or (d.get("n_nodes") in (None, 0) and str(d.get("leaf", "")).startswith("stage 0")) else "2 (tree: %s nodes, depth %s, CC %s, exact %s, NS %s, pockets %s)" % (d.get("n_nodes"), d.get("max_depth"), d.get("cc_kills"), d.get("exact_rounds"), d.get("ns_splits"), d.get("pocket_splits"))
                v = d.get("verdict")
                if v == "DEAD" and pad == "zero":
                    v = "DEAD (s0-only, WINDOW-PENDING)"
                sec = float(d.get("seconds") or 0)
                tot += sec
                L2.append("| %s | %s | %s | %s%s | %.0f |" % (n, pad, st, v, " (wall)" if d.get("wall") else "", sec))
            v = (per[n].get("g1") or {}).get("verdicts") or {}
            if v.get("zero", "").startswith("not run"):
                L2.append("| %s | zero | - | %s | 0 |" % (n, v["zero"]))
        L2.append("")
        L2.append("CPU-h in this block: %.2f" % (tot / 3600))
        L2.append("")
        return tot

    alive_block(L2, per, gnodes)
    tg = table(gnodes, "The 19 alive k5 gallery pages")
    tf = table(fnodes, "The k5 frontier (A57 census, deepest-first)")
    secs = [sum(float(d.get("seconds") or 0) for d in per[n].values()) for n in fnodes]
    kills_g = sum(1 for n in gnodes if (per[n].get("g1") or {}).get("verdict") == "DEAD")
    kills_f = sum(1 for n in fnodes if (per[n].get("g1") or {}).get("verdict") == "DEAD")
    L2.append("## Price and projection")
    L2.append("")
    L2.append("* gallery: %d / %d pages DEAD at the g1 pad (the G1 slab only), %.2f CPU-h" % (kills_g, len(gnodes), tg / 3600))
    if fnodes:
        first = secs[:20]
        mean, med = statistics.mean(first), statistics.median(first)
        proj = mean * len(remaining) / 3600
        L2.append("* frontier: %d nodes run (%d DEAD at the g1 pad: dead on G1 = (3.861637, s0], s-hat incl.; nothing below it), %.2f CPU-h; the census has %d alive nodes, %d remaining" % (len(fnodes), kills_f, tf / 3600, len(census), len(remaining)))
        L2.append("* PRICE over the first %d frontier nodes: mean %.0f s, median %.0f s per node (both pads); PROJECTION for the remaining %d: %.1f CPU-h (cap %.0f)" % (len(first), mean, med, len(remaining), proj, CAP_CPUH))
        if len(first) >= 20 and proj > CAP_CPUH and not os.path.exists(os.path.join(HERE, "..", "logs", "FRONTIER_STOPPED")):
            # the frontier STOP fired once (2026-09-13 20:22, projection 236 CPU-h); the marker keeps it from re-firing
            # on every later gallery-pass node (coordinator, 2026-09-14) -- the frontier queue itself is not re-run
            L2.append("* **STOP: the projection exceeds the cap -- the workers exit after their current node**")
            os.makedirs(os.path.dirname(STOP), exist_ok=True)
            open(os.path.join(HERE, "..", "logs", "FRONTIER_STOPPED"), "w").write("frontier stop recorded")
            open(STOP, "w").write("projection %.1f CPU-h > %.0f at %s\n" % (proj, CAP_CPUH, time.strftime("%Y-%m-%d %H:%M:%S")))
    else:
        L2.append("* frontier: not started; the census has %d alive nodes (%s)" % (len(census), dict(collections.Counter(c["tree"] for c in census))))
    L2.append("")
    # A270 (2026-09-23): the per-slab line.  load211.census() reads A57 tree ROWS only: a cover box whose shard never
    # reached it has no row, and a gallery page moved to killed/ by a pad-0 (s0-only) kill counts as closed there.
    b270 = os.path.join(HERE, "..", "..", "A270-k5-lower-slabs", "results", "slabs270_board.md")
    if os.path.exists(b270):
        L2.append("## Per slab (A270) -- what is certified for k5_11 / k5_16 on G1-G4")
        L2.append("")
        L2.append("\"census 0 alive\" above is over A57 tree ROWS: A57's G1 cover has 290 level-1 boxes with NO row at all (the unfinished "
                  "shard tails: k5_11 136, k5_16 154, plus 6 T5 trim pieces of closed untrimmed rows -- attempts/A270-k5-lower-slabs/results/cover270.json) and two k5_16 pages "
                  "(Y1117, Y0436) closed only by pad-0 kills (s0 only); a g1-pad DEAD is a statement on G1 only.")
        L2.append("")
        L2 += open(b270, encoding="utf-8").read().splitlines()
        L2.append("")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L2) + "\n")
    print("progress: %d gallery, %d frontier nodes; %.1f CPU-h" % (len(gnodes), len(fnodes), (tg + tf) / 3600))


if __name__ == "__main__":
    main()
