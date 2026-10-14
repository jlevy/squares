"""A211 (A225) -- PROGRESS statistics per page and pad, read from results/coarsetree211.jsonl ONLY.

The PI (2026-09-14 23:40): "show how many top-level nodes are left, so I can better judge progress /
work remaining / see how deep it's going."  A run of the coarse tree starts from the ALIVE leaves the
previous run left (Lemma INHERIT, notes/coarse_tree.md s.4) -- those are the START NODES.  A run walks
them in order until the wall; each is DEAD, ALIVE at the wall, or never reached (SKIPPED).  So the work
left on a page is (alive + not reached) start nodes, and the depth reached is the ABSOLUTE depth
(the start node's own path length + the depth the run added below it).

Stdlib only, no cert loads, no runs: fig211.py, progress211.py and docs/shadows/status_gallery.py all
read the same numbers from here.  Nothing here writes anything.

    from pstats211 import page_stats
    st = page_stats("k5_16_interior_Y1056", "g1")
"""
import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.abspath(os.path.join(HERE, "..", "results", "coarsetree211.jsonl"))
_CACHE = {}


def _jl(path):
    out = []
    if not os.path.exists(path):
        return out
    for ln in open(path, encoding="utf-8"):
        ln = ln.strip()
        if ln:
            try:
                out.append(json.loads(ln))
            except Exception:
                pass
    return out


def rows(path=None):
    """every mode='page' row of the jsonl, in file (chronological) order; cached on mtime."""
    path = os.path.abspath(path or RES)
    key = (path, os.path.getmtime(path) if os.path.exists(path) else 0)
    if _CACHE.get("key") != key:
        _CACHE["key"] = key
        _CACHE["rows"] = [d for d in _jl(path) if d.get("mode") == "page" and d.get("nid")]
    return _CACHE["rows"]


def history(nid, pad, path=None):
    """every run of this page at this pad, oldest first."""
    return [d for d in rows(path) if d.get("nid") == nid and d.get("pad") == pad]


def _owns(label, start):
    """does node `label` lie in the subtree the run grew under start node `start`?"""
    return label == start or label.startswith(start + ".") or label.startswith(start + "r")


def run_stats(r):
    """one run -> {starts: [per start node], n_start, dead, alive, unreached, max_abs, ...}."""
    starts = list(r.get("start_nodes") or [])
    runs = list(r.get("start_runs") or r.get("runs_started") or [])
    nb = list(r.get("nodes_brief") or r.get("nodes") or [])
    steps = {}
    for s in starts:
        if s.get("label"):
            steps[s["label"]] = int(s.get("n_steps") or 0)
    labels = sorted(steps, key=len, reverse=True)
    # relative depth reached under each start node; absolute depth over the whole merged tree
    rel = dict((s, 0) for s in steps)
    max_abs = 0
    for n in nb:
        lbl, dep = str(n.get("label") or ""), int(n.get("depth") or 0)
        if n.get("kind") == "inherited":                         # inherited depth is already absolute
            max_abs = max(max_abs, dep)
            continue
        for s in labels:
            if _owns(lbl, s):
                rel[s] = max(rel[s], dep)
                max_abs = max(max_abs, steps[s] + dep)
                break
        else:
            max_abs = max(max_abs, dep)                          # a run rooted at R (no inheritance)
    out, prev = [], 0.0
    for k, x in enumerate(runs):
        lbl = x.get("label")
        sec = float(x.get("seconds") or 0.0)                     # cumulative wall t of the run
        d = sec - prev if sec >= prev else sec
        prev = max(prev, sec)
        out.append({"label": lbl, "verdict": x.get("verdict"), "n_nodes": x.get("n_nodes"),
                    "depth": rel.get(lbl, 0), "abs_depth": steps.get(lbl, 0) + rel.get(lbl, 0),
                    "n_steps": steps.get(lbl, 0), "seconds": round(d, 1), "reached": True,
                    "wall": bool(x.get("wall"))})
    done = set(x.get("label") for x in runs)
    for s in starts:
        if s.get("label") not in done:
            out.append({"label": s.get("label"), "verdict": "SKIPPED", "n_nodes": 0, "depth": 0,
                        "abs_depth": int(s.get("n_steps") or 0), "n_steps": int(s.get("n_steps") or 0),
                        "seconds": 0.0, "reached": False, "wall": False})
    dead = [x for x in out if x["verdict"] == "DEAD"]
    alive = [x for x in out if x["reached"] and x["verdict"] != "DEAD"]
    unreached = [x for x in out if not x["reached"]]
    return {"starts": out, "n_start": len(starts) or (1 if out else 0), "dead": len(dead),
            "alive": len(alive), "unreached": len(unreached), "max_abs": max_abs,
            "dead_secs": [x["seconds"] for x in dead if x["seconds"] > 0],
            "seconds": float(r.get("seconds") or 0.0), "verdict": r.get("verdict"),
            "when": r.get("when"), "wall": bool(r.get("wall")),
            "dead_leaves": int(r.get("dead_leaves") or 0),
            "alive_leaves": len(r.get("undecided") or []) or int(r.get("alive_leaves") or 0),
            "inherited_dead": int(r.get("inherited_dead") or 0)}


def page_stats(nid, pad, path=None):
    """the PROGRESS block's numbers for one page at one pad, or None if the page never ran."""
    hist = history(nid, pad, path)
    if not hist:
        return None
    per = [run_stats(r) for r in hist]
    cur = per[-1]
    killed = [s for p in per for s in p["dead_secs"]]
    med = statistics.median(killed) if killed else 0.0
    left = cur["alive"] + cur["unreached"]
    st = dict(cur)
    st.update({"nid": nid, "pad": pad, "n_runs": len(hist),
               "wall_total": sum(p["seconds"] for p in per),
               "max_abs_ever": max([p["max_abs"] for p in per] + [0]),
               "left": left, "median_kill_s": round(med, 1),
               "est_s": round(left * med, 1), "n_killed_sample": len(killed),
               "runs": per})
    return st


def fmt_head(st):
    """the PROGRESS headline: start nodes = N: D dead this run, A alive at the wall, U not reached."""
    return ("PROGRESS -- pad %s: START NODES (the alive leaves this run inherited from the previous run) = %d: "
            "%d DEAD this run, %d ALIVE at the wall, %d NOT REACHED (SKIPPED); %d of this run's list still open"
            % (st["pad"], st["n_start"], st["dead"], st["alive"], st["unreached"], st["left"]))


def fmt_cum(st):
    """the cumulative line: runs so far, wall spent, dead / alive leaves now, max depth so far."""
    return ("CUMULATIVE over %d run(s) of this page at this pad: %.2f CPU-h of wall spent; %d dead leaves / "
            "%d alive leaves now (the next run's start nodes); MAX DEPTH so far %d (absolute: start-node path + "
            "the depth this run added); this run %s%s"
            % (st["n_runs"], st["wall_total"] / 3600.0, st["dead_leaves"], st["alive_leaves"],
               st["max_abs_ever"], st["verdict"], " at the WALL" if st["wall"] else ""))


def fmt_est(st):
    """the one-line ESTIMATE (not a bound)."""
    if not st["n_killed_sample"]:
        return "ESTIMATE: no start node has been killed yet on this page/pad -- no price to project from"
    hard = sum(x["seconds"] for x in st["starts"] if x["reached"] and x["verdict"] != "DEAD")
    return ("ESTIMATE (not a bound): %d start node(s) left x %.0f s median per KILLED start node (%d samples over "
            "%d run(s)) = %.1f CPU-h, i.e. about %.1f more run(s) at the 1800 s wall -- an UNDER-estimate: the "
            "start node(s) still alive have already absorbed %.0f s without closing, and each one that survives "
            "splits into several new start nodes"
            % (st["left"], st["median_kill_s"], st["n_killed_sample"], st["n_runs"], st["est_s"] / 3600.0,
               st["est_s"] / 1800.0, hard))


def fmt_short(st):
    """the three numbers for a board row / a table cell."""
    return "%d start nodes left, %d alive leaves, depth %d" % (st["left"], st["alive_leaves"], st["max_abs_ever"])


if __name__ == "__main__":
    import sys
    for nid in sys.argv[1:] or ["k5_16_interior_Y1056"]:
        for pad in ("g1", "zero"):
            s = page_stats(nid, pad)
            if not s:
                continue
            print(nid, pad, fmt_short(s))
            print("  ", fmt_head(s))
            print("  ", fmt_cum(s))
            print("  ", fmt_est(s))
            for x in s["starts"]:
                print("     %-22s %-8s nodes %-4s depth %s (abs %s)  %.1f s" % (
                    x["label"], x["verdict"], x["n_nodes"], x["depth"], x["abs_depth"], x["seconds"]))
