"""A243 driver -- ONE node of the n-general climb / census: stage 0 (A202 + A203 CSP via fast30, n threaded) then A211's
coarse tree with the pass flags A220_NOROOM_INHERIT=1 A221_LANE=1 A224_SNAP=1, NO LP anywhere, pad "window"
(lambda_max = s_hi / s_lo: a statement for every side m of the window).

    python run243.py N NID [--wall 1800] [--depth 6] [--nodes 600] [--force] [--fig]

NID = a census class name ("n17_k08_0156") or with "__spine" (root243's doc).  Certificate certs/climb243_<nid>.json
(A211's page document + the A243 hypothesis), one compact row appended to results/rows243_n<N>.jsonl, and the last
stdout line "ROW243 {json}".  A211 / A203 / A198 / A178 / A171 / A224 are imported READ-ONLY (nparam243 rebinds
their n = 11 constants in this process only)."""
import argparse
import gzip
import json
import os
import sys
import time

for _k in ("A220_NOROOM_INHERIT", "A221_LANE", "A224_SNAP"):
    os.environ.setdefault(_k, "1")
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
A243 = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(A243, "..", ".."))
sys.path.insert(0, HERE)
import root243                                                  # noqa: E402


def counts(doc):
    d = (doc.get("runs") or {}).get("window_page") or {}
    nodes = d.get("nodes") or []
    rules = {}
    for nd in nodes:
        if nd.get("verdict") == "DEAD" and nd.get("clip"):
            rules[nd["clip"]] = rules.get(nd["clip"], 0) + 1
    root = nodes[0] if nodes else {}
    return d, nodes, rules, root


_BASE = {}


def setup(n, fig=False):
    """install the n-general toolkit once per process (nparam243 allows one n per process)."""
    FP = root243.install(n)
    import run211 as RUN
    import stage209
    certs = os.path.join(A243, "certs", "n%d" % n)
    os.makedirs(certs, exist_ok=True)
    stage209.CERTS = certs
    RUN.CERTS = certs
    RUN.RES = os.path.join(A243, "results", "raw211_n%d.jsonl" % n)
    RUN.NOFIG = not fig
    if not _BASE:
        _BASE["verifier"] = RUN.VERIFIER
        RUN.belownormal()
    return FP, RUN, certs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("nid")
    ap.add_argument("--wall", type=float, default=1800)
    ap.add_argument("--depth", type=int, default=6)
    ap.add_argument("--nodes", type=int, default=600)
    ap.add_argument("--rounds", type=int, default=1)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--fig", action="store_true")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    out = run_node(a)
    print("ROW243 " + json.dumps(out, default=str), flush=True)


def node_args(n, nid, wall=1800, depth=6, nodes=600, rounds=1, force=False, fig=False, tag=""):
    return argparse.Namespace(n=n, nid=nid, wall=wall, depth=depth, nodes=nodes, rounds=rounds, force=force, fig=fig, tag=tag)


def run_node(a):
    """ONE node: stage 0 + the coarse tree on pad window; returns the compact row (also appended to rows243_n<N>)."""
    FP, RUN, certs = setup(a.n, a.fig)
    import stage209
    rec, cls, row = FP.load_page(a.nid)
    RUN.VERIFIER = _BASE["verifier"] + ("  [A243: n = %d on the window [%s, %s]; the page hypothesis is root243's (%s).  Theorem FC / Lemma "
                     "SLOT-CROWD / Lemma A1 / CN / POCKET / the multibox clips are n-general; every n = 11 constant of the "
                     "toolkit was rebound by nparam243 (notes/climb243.md s.1).]" % (a.n, root243.NP.CFG["s_lo"], root243.NP.CFG["s_hi"],
                                                                                      rec["hypothesis"][:200]))
    a.pads, a.no_resume, a.no_inherit, a.start_only, a.cert_suffix = "window", False, True, None, None
    cert = os.path.join(certs, "climb243_%s.json" % a.nid)
    doc = dict(nid=a.nid, runs={})
    if not os.path.exists(cert) and os.path.exists(cert + ".gz") and not a.force:
        with gzip.open(cert + ".gz", "rt", encoding="utf-8") as f:
            open(cert, "w", encoding="utf-8").write(f.read())
    if os.path.exists(cert) and not a.force:
        try:
            doc = json.load(open(cert, encoding="utf-8"))
            doc.setdefault("runs", {})
        except Exception:                                         # noqa: BLE001
            doc = dict(nid=a.nid, runs={})
    doc.update(camp="A243", n=a.n, cls=cls, hypothesis=rec["hypothesis"], spine=rec["spine"], assumed=rec["assumed"],
               window=[str(root243.NP.CFG["s_lo"]), str(root243.NP.CFG["s_hi"])], budget=rec["budget"])
    t0 = time.time()
    RUN.run_page(doc, a, cert)
    doc["seconds_total"] = round(time.time() - t0, 1)
    RUN.save(doc, cert)
    d, nodes, rules, root = counts(doc)
    st0 = (doc.get("stage0") or {}).get("window") or {}
    import geo178 as G
    items = G.forced_items(cls, rec)
    verdict = (doc.get("verdicts") or {}).get("window")
    out = dict(nid=a.nid, cls=cls, n=a.n, k=len(rec["pins"]), spine=rec["spine"], assumed=rec["assumed"],
               forced=[it["cell"] for it in items], forced_ext={it["cell"]: it.get("extension") for it in items},
               verdict=verdict, stage0_verdict=st0.get("verdict"), stage0_leaf=str(st0.get("leaf") or "")[:200],
               stage0_kills=st0.get("kills"), stage0_seconds=st0.get("seconds"), tree_seconds=d.get("seconds"),
               seconds_total=doc["seconds_total"], n_nodes=d.get("n_nodes") or 0, max_depth=d.get("max_depth") or 0,
               dead_leaves=d.get("dead_leaves"), alive_leaves=d.get("alive_leaves"), kills_by_rule=rules,
               root_verdict=root.get("verdict"), root_clip=root.get("clip"), wall=d.get("wall"),
               snap=dict(runs=d.get("snap_runs"), kills=d.get("snap_kills"), handoffs=d.get("snap_handoffs")),
               noroom=[dict(k=r.get("k"), m=r.get("m"), verdict=r.get("verdict"), clip=r.get("clip")) for r in (d.get("noroom_runs") or [])][:12],
               undecided=[str(u.get("reason"))[:160] for u in (d.get("undecided") or [])][:6],
               leaf=str(d.get("leaf") or "")[:300], tag=a.tag, wall_s=a.wall,
               cert=os.path.relpath(cert, ROOT).replace("\\", "/") + ".gz", when=time.strftime("%Y-%m-%d %H:%M:%S"))
    with open(os.path.join(A243, "results", "rows243_n%d.jsonl" % a.n), "a", encoding="utf-8") as f:
        f.write(json.dumps(out, default=str) + "\n")
    pack(cert)
    pack(os.path.join(certs, "csp209_%s_window_s0.json" % a.nid))
    return out


def pack(f):
    """the certificate gzipped in place (the lab's .json.gz convention, A125): ~10x smaller in git."""
    if os.path.exists(f):
        with open(f, "rb") as src, gzip.open(f + ".gz", "wb") as dst:
            dst.write(src.read())
        os.remove(f)


if __name__ == "__main__":
    main()
