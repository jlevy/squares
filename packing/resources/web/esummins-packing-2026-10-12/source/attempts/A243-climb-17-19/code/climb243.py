"""A243 task 2 -- the FC CLIMB as a tree over slot sets, read off the window table (descend243 runs the nodes).

Lemma K1 run forward (notes/climb243.md s.3).  Node = a class S (slot set, D4-reduced).  For every candidate cell p
of S (Young-completable, unclipped), Theorem FC splits the packings of S into
    (A) p is met by two non-pin squares of the dilate      -- the SPINE hypothesis, all cells at once;
    (B) p has <= 1 non-pin meeter: the teleport (Lemma SLOT-CROWD) gives a packing at the same side containing the
        pins of T = S + p                                   -- the k + 1 branch.
So  dead(S)  <=  dead(S__spine)  and  dead(T_p) for every p.  The climb's tree: the root is the four-corner class;
a node's verdict is its spine tree's; a REDUCES node (spine DEAD) has the children T_p whose class is not DEAD
(a DEAD T_p is CITED from the table -- Lemma K1 -- not re-solved); the depth is capped at the record's k.
A DEAD branch is a theorem about that slot-set hypothesis on the window; ALIVE = the spine tree did not close.
    python climb243.py all | 17 | 19   -> results/climb243_tree_n<N>.jsonl + results/climb243_n<N>.json"""
import json
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
A243 = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import census243 as CEN                                         # noqa: E402
import classtab243 as CT                                        # noqa: E402

ROOT4 = {17: "n17_k04_0016", 19: "n19_k04_0016"}
RECORD = {17: "n17_k08_0156", 19: "n19_k11_0236"}


def subset_of(tab, a, b):
    """class a contained in class b up to D4."""
    P = set(tab.rows[b]["_pts"])
    return any(all(f(x, y, tab.s_hi) in P for x, y in tab.rows[a]["_pts"]) for f in CEN.D4)


def tree(n):
    tab = CT.table(n).reload()
    k_rec = CEN.K_REC[n]
    nodes, seen = [], {}

    def visit(cls, path, depth):
        v = tab.verdicts.get(cls) or {}
        verdict = v.get("verdict") or "PENDING"
        nd = dict(path="/".join(path + [cls]), cls=cls, k=tab.rows[cls]["k"], depth=depth, verdict=verdict,
                  labels=tab.rows[cls]["labels"], targets=v.get("targets") or [], kills_by_rule=v.get("kills_by_rule"),
                  stage0=v.get("stage0"), n_nodes=v.get("n_nodes"), seconds=v.get("seconds"), why=(v.get("why") or "")[:160],
                  record=(cls == RECORD[n]), contains_record=subset_of(tab, RECORD[n], cls) if tab.rows[cls]["k"] >= k_rec else None,
                  in_record=subset_of(tab, cls, RECORD[n]))
        nodes.append(nd)
        seen[cls] = seen.get(cls, 0) + 1
        if verdict == "REDUCES" and tab.rows[cls]["k"] < k_rec:
            for t in nd["targets"]:
                if t in tab.rows:
                    visit(t, path + [cls], depth + 1)
        elif verdict == "REDUCES":
            nd["capped"] = True                                   # the record's k: the climb stops here
    visit(ROOT4[n], [], 0)
    return tab, nodes, seen


def canaries(tab, n):
    """soundness canaries: the record's class and every class it contains (up to D4) are realised by the record packing
    at a side inside the window, so none of them may be DEAD."""
    bad = []
    for cls, v in tab.verdicts.items():
        if v.get("verdict") == "DEAD" and subset_of(tab, cls, RECORD[n]):
            bad.append(cls)
    return bad


def summary(n):
    tab, nodes, seen = tree(n)
    rows = list(tab.verdicts.values())
    byk = {}
    for nm, r in tab.rows.items():
        c4 = all(x in r["labels"] for x in ("BL(0,0)", "BR(0,0)", "TR(0,0)", "TL(0,0)"))
        d = byk.setdefault(r["k"], dict(classes=0, corners4=0, DEAD=0, REDUCES=0, ALIVE=0, ERROR=0, pending=0, root_dead=0, stage0_dead=0, seconds=0.0))
        d["classes"] += 1
        d["corners4"] += 1 if c4 else 0
        v = tab.verdicts.get(nm)
        if not v:
            d["pending"] += 1
            continue
        d[v["verdict"]] = d.get(v["verdict"], 0) + 1
        d["seconds"] += float(v.get("seconds") or 0)
        if v["verdict"] in ("DEAD", "REDUCES") and (v.get("stage0") == "DEAD" or (v.get("n_nodes") or 0) <= 1):
            d["root_dead"] += 1
        if v.get("stage0") == "DEAD":
            d["stage0_dead"] += 1
    rules = {}
    for v in rows:
        for k, c in (v.get("kills_by_rule") or {}).items():
            rules[k] = rules.get(k, 0) + c
        if v.get("stage0") == "DEAD":
            rules["STAGE0"] = rules.get("STAGE0", 0) + 1
    leaves = [nd for nd in nodes if nd["verdict"] != "REDUCES" or nd.get("capped")]
    rec = tab.verdicts.get(RECORD[n]) or {}
    out = dict(n=n, window=[str(tab.s_lo), str(tab.s_hi)], root=ROOT4[n], record=RECORD[n], record_verdict=rec.get("verdict"),
               record_targets=rec.get("targets"), census_by_k={str(k): byk[k] for k in sorted(byk, reverse=True)},
               cpu_h=round(sum(float(v.get("seconds") or 0) for v in rows) / 3600.0, 2), n_done=len(rows),
               rules=rules, canary_dead_in_record=canaries(tab, n),
               climb=dict(n_nodes=len(nodes), n_classes=len(seen), max_depth=max([nd["depth"] for nd in nodes] or [0]),
                          leaves={v: sum(1 for nd in leaves if nd["verdict"] == v) for v in ("DEAD", "ALIVE", "PENDING", "REDUCES", "ERROR")},
                          root=(nodes[0] if nodes else None),
                          alive_leaves=[dict(path=nd["path"], k=nd["k"], record=nd["record"], in_record=nd["in_record"]) for nd in leaves if nd["verdict"] in ("ALIVE", "REDUCES")][:40],
                          reaches_record=any(nd["record"] for nd in nodes)))
    with open(os.path.join(A243, "results", "climb243_tree_n%d.jsonl" % n), "w", encoding="utf-8") as f:
        for nd in nodes:
            f.write(json.dumps(nd) + "\n")
    json.dump(out, open(os.path.join(A243, "results", "climb243_n%d.json" % n), "w", encoding="utf-8"), indent=1)
    return out


if __name__ == "__main__":
    ns = (17, 19) if (len(sys.argv) < 2 or sys.argv[1] == "all") else (int(sys.argv[1]),)
    for n in ns:
        s = summary(n)
        print("n=%d done %d classes, %.2f CPU-h; record %s: %s; canary %s; climb %s" % (
            n, s["n_done"], s["cpu_h"], s["record"], s["record_verdict"], s["canary_dead_in_record"] or "OK",
            {k: v for k, v in s["climb"].items() if k in ("n_nodes", "max_depth", "leaves", "reaches_record")}))
