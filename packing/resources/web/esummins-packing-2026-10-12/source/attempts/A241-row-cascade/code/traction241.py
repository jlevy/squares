"""A241 -- results/traction241.md: the traction check, A241's rows against A238's blind run.

    python traction241.py [--out results/traction241.md]

A238's blind run on k3_02's 20 A100 head-to-head level-1 cover cells: 0 DEAD / 20 ALIVE, mean 4.3 s,
`kills_by_rule = {}`, max depth 0 on every node -- the toolkit had NOTHING to act on, because every
one of k3_02's six forced cells extends into a class with no full-window row.  This table is the same
20 cells re-run after the row cascade, cell by cell, and the same cells' A100 LP rows beside them.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
A241 = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(A241, "..", ".."))
A238 = os.path.join(ROOT, "attempts", "A238-k4-benchmark")
BEFORE = os.path.join(A238, "results", "bench238.jsonl")
AFTER = os.path.join(A241, "results", "traction241.jsonl")


def rows(f, pred):
    out = {}
    if os.path.exists(f):
        for ln in open(f, encoding="utf-8", errors="replace"):
            ln = ln.strip()
            if not ln:
                continue
            try:
                r = json.loads(ln)
            except Exception:                                                   # noqa: BLE001
                continue
            if pred(r):
                out[r["nid"]] = r                                               # last row wins
    return out


def usable_now():
    sys.path.insert(0, HERE)
    import load_cl241 as L
    CL = L.classes()
    CL._SB = None
    out = {}
    for c in ("k3_01", "k3_02", "k3_03", "k3_04", "k3_05", "k2_00", "k2_01", "k2_02", "k1_00"):
        cells = CL.forced_cells(c)
        out[c] = (sum(1 for r in cells if r["usable"]), len(cells),
                  [(r["cell"], r["extension"]) for r in cells if r["usable"]])
    return out


def md():
    b = rows(BEFORE, lambda r: str(r.get("nid", "")).startswith("k3_02_c0_Y") and r.get("a100"))
    a = rows(AFTER, lambda r: str(r.get("nid", "")).startswith("k3_02_c0_Y"))
    u = usable_now()
    L = ["# A241 -- the traction check: k3_02's 20 A100 head-to-head cells, before and after the rows", "",
         "A238's blind run is the baseline: **0 DEAD / 20 ALIVE**, mean 4.3 s, `kills_by_rule = {}`, max depth 0 --",
         "the toolkit's rules (rule CC, A208 no-room + Lemma POCKET, A206 Rule NS, A230 Rule EPS, A224 Rule SNAP)",
         "all act on Theorem FC's forced cells, and k3_02 had none usable.  Same code, same pages, same wall.", "",
         "## usable forced cells now (the row cascade's output)", "",
         "| class | usable / forced | the usable extensions |", "|---|---|---|"]
    for c, (n, tot, ex) in u.items():
        L.append("| `%s` | **%d** / %d | %s |" % (c, n, tot, ", ".join("%s→%s" % e for e in ex) or "—"))
    nd = sum(1 for r in a.values() if r.get("verdict") == "DEAD")
    L += ["", "## the 20 cells", "",
          "| cell | A100 | A238 blind | A241 with rows | A241 s | killed by | nodes | depth |",
          "|---|---|---|---|---|---|---|---|"]
    for nid in sorted(b):
        rb, ra = b[nid], a.get(nid)
        L.append("| `%s` | %s | %s | %s | %s | %s | %s | %s |" % (
            nid.replace("k3_02_", ""), (rb.get("a100") or {}).get("verdict", "-"),
            rb.get("verdict"), "**%s**" % ra.get("verdict") if ra else "_pending_",
            (ra or {}).get("seconds", "-"),
            ", ".join("%s x%s" % kv for kv in sorted((ra or {}).get("kills_by_rule", {}).items())) or "—",
            (ra or {}).get("n_nodes", "-"), (ra or {}).get("max_depth", "-")))
    L += ["", "**Score: A238 blind 0 DEAD / 20 ALIVE  ->  A241 with rows %d DEAD / %d ALIVE (%d of 20 decided).**"
          % (nd, sum(1 for r in a.values() if r.get("verdict") == "ALIVE"), len(a)), ""]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(A241, "results", "traction241.md"))
    a = ap.parse_args(argv)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(md())
    print("-> %s" % os.path.relpath(a.out, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
