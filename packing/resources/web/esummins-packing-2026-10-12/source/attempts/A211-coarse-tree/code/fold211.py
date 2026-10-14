"""A211 (A209 copy) -- fold every window-pad (g1) page kill into A57's closure bookkeeping: results/superseded_by_coarsetree_A211.jsonl,
one row per killed tree id in the supersession-ledger format A137 / A149 use (id, applies_to_tags = the tree, the prior
verdict retained, superseded_by / leaf / cert / source, recorded), plus `closes_subtree` = the alive descendants the kill
closes (Lemma K1: aliveness descends containment).  A57's own files are never written.
    python fold209.py            # rebuild the ledger from results/coarsetree211.jsonl
    python fold209.py --closed <nid>   # exit 0 iff the node (or an ancestor) is already closed by a ledger"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
import load211 as L                                            # noqa: E402

RES = os.path.join(HERE, "..", "results", "coarsetree211.jsonl")
LEDGER = L.LEDGER


def kills():
    """nid -> the DEAD g1 page row (the last one)."""
    out = {}
    for d in L.jl(RES):
        if d.get("mode") == "page" and d.get("pad") == "g1" and d.get("verdict") == "DEAD" and d.get("nid"):
            out[d["nid"]] = d
    return out


def rebuild():
    T = L.trees()
    rows = []
    for nid, d in sorted(kills().items()):
        key, i = L.tree_key(nid)
        v, r = T.get(key, {}).get(i, (None, {}))
        desc = sorted(j for j, (vj, _) in T.get(key, {}).items() if j != i and j.startswith(i + "_D") and vj in ("ALIVE", "FAIL"))
        rows.append(dict(id=i, nid=nid, level=1 + i.count("_D"), cls=d.get("cls"), camp="A57", prior_verdict=v, prior_cert=str(r.get("cert") or "")[:120],
                         superseded_by="A209 coarsetree211 composed chain (A202/A203 stage 0 -> A204 cascade -> A205 clip tree + A206 Rule NS + A207 basin clip -> A208 no-room / pocket branching) at the g1 pad",
                         leaf=("stage 0: %s" % d.get("leaf")) if (d.get("stage0") or {}).get("g1", {}).get("verdict") == "DEAD" and not d.get("n_nodes") else str(d.get("leaf") or "")[:400],
                         cert=d.get("cert"), source="A211-coarse-tree/results/coarsetree211.jsonl", already_dead=False, applies_to_tags=[key], not_applicable_to_tags=[],
                         closes_subtree=desc, verifier=d.get("verifier"), recorded=d.get("when") or time.strftime("%Y-%m-%d %H:%M:%S"),
                         note="prior verdict RETAINED; this node and its subtree (Lemma K1) are a KILL in the tree listed in applies_to_tags; [C: library clip trace], no verifier clause"))
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    with open(LEDGER, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, default=str) + "\n")
    return rows


def closed(nid):
    key, i = L.tree_key(nid)
    return L.is_dead(i, key, L.dead_ids())


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--closed":
        sys.exit(0 if closed(sys.argv[2]) else 1)
    rows = rebuild()
    print("ledger: %d kills, closing %d alive descendants" % (len(rows), sum(len(r["closes_subtree"]) for r in rows)))
