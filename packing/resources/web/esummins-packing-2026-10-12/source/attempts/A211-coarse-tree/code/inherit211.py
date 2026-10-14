"""A211b -- Lemma INHERIT (notes/coarse_tree.md s.4): the MERGED state of every prior certificate for one (page, pad).

A node of any of the campaign trees is a PATH: the ordered conjunction of the branch steps from the common A203 start
(a row / pair hypothesis at a slot, a Rule-NS meets / misses hypothesis for a role at a slot, a Lemma-POCKET branch).
Two nodes of two different campaigns with the SAME path are the SAME hypothesis, so:
  * a path closed by ANY prior certificate is FINAL (never re-run): its hypothesis is refuted;
  * the branch list a prior certificate recorded at a node is an EXHAUSTIVE disjunction over that node's hypothesis
    (A205 Lemma CT's branching rule, certified there), so the new tree may replay it instead of re-deriving it;
  * the paths that remain (the ALIVE / undecided leaves of the most recent prior tree, minus the closed ones) are the
    only ones the new tree has to decide: the START NODES.
This module reads A205 (cliptree205 + certs/extended), A206 (namedsplit206, runs keyed by leaf label), A209
(k5killer209, both pads), A211's own certs, and the leaf-kill ledgers A210 cornercover210_leaves / A208 noroom208 /
A207 basinclip207, and returns dead_paths (minimal, each with its source certificate) + start_nodes.

A229 -- EVERY A211 certificate of the page is a source, not just the page certificate: the page file
`coarsetree211_<nid>.json` AND every per-start SHARD file `coarsetree211_<nid>__<TAG>.json` that a `run211.py
--start ... --cert-suffix TAG` run wrote (`attempts/A229-start-parallel/notes/parallel229.md`).  They are merged on
the path key exactly as the other campaigns are -- Lemma INHERIT applied FILE-WISE: the same path key is the same
hypothesis whichever file refuted it, so a DEAD branch from any of them is final, and the ALIVE leaves come from the
newest file that recorded a branch list at that path (the A211 files are ranked by mtime, oldest first, so the newest
wins the tie in `trie`).  Set A229_CERT_DIR to read the A211 certificates from somewhere else (an isolated TEST dir).
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ATT = os.path.join(ROOT, "attempts")
SEG = re.compile(r"^(p?\d+)(.*)$")
A211CERTS = os.environ.get("A229_CERT_DIR") or os.path.join(HERE, "..", "certs")
BRANCH_KINDS = ("row", "pair", "ns-meets", "ns-misses", "pocket", "inherited")


def jl(p):
    out = []
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8"):
            ln = ln.strip()
            if ln:
                try:
                    out.append(json.loads(ln))
                except Exception:
                    pass
    return out


def jload(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


# ---------------------------------------------------------------- A229: every A211 certificate of ONE page
def a211_certs(nid):
    """the page certificate coarsetree211_<nid>.json and every per-start SHARD certificate
    coarsetree211_<nid>__<TAG>.json, OLDEST FIRST (mtime).

    Only these two spellings count: the '__' separator keeps `coarsetree211_<nid>_D07.json` -- a DIFFERENT page of the
    A57 tree, whose id merely extends this one -- out of the list.  The order is the merge's tie-break: `trie` keeps the
    branch list of the LAST source of the highest rank it sees, and every A211 file has rank 5, so oldest-first means
    the NEWEST A211 file's branch list wins at a shared path.  DEAD is never a tie-break: a path closed in ANY of them
    is closed (Lemma INHERIT (a), applied file-wise -- notes/parallel229.md).  With only the page certificate present
    this returns exactly the one file the pre-A229 code read."""
    d = os.path.abspath(A211CERTS)
    want, pre = "coarsetree211_%s.json" % nid, "coarsetree211_%s__" % nid
    out = []
    try:
        names = os.listdir(d)
    except OSError:
        names = []
    for f in names:
        if f == want or (f.startswith(pre) and f.endswith(".json") and len(f) > len(pre) + 5):
            out.append(os.path.join(d, f))
    def mt(f):
        try:
            return os.path.getmtime(f)
        except OSError:
            return 0.0
    out.sort(key=lambda f: (mt(f), os.path.basename(f)))
    if not out:                                                   # the pre-A229 path: the (possibly absent) page cert
        out = [os.path.join(d, want)]
    return out


# ---------------------------------------------------------------- the tree sources for one page
def sources(nid):
    """every prior tree for the page as dict(camp, file, run, pad, mode, source, root_label, nodes, rank)."""
    out = []
    a205 = os.path.join(ATT, "A205-clip-tree", "certs")
    files = [("A205", os.path.join(a205, "cliptree205_%s.json" % nid), 1)]
    for f in sorted(os.listdir(os.path.join(a205, "extended"))) if os.path.isdir(os.path.join(a205, "extended")) else []:
        if f.startswith("cliptree205_%s" % nid) and f.endswith(".json"):
            files.append(("A205x", os.path.join(a205, "extended", f), 2))
    for camp, f, rank in files:
        doc = jload(f)
        for pad, d in ((doc or {}).get("pads") or {}).items():
            out.append(dict(camp=camp, file=f, run="pad_%s" % pad, pad=pad, mode="tree", source=d.get("source"),
                            root_label=(d.get("nodes") or [{}])[0].get("label") or "R", nodes=d.get("nodes") or [], rank=rank))
    a211 = [("A211", f, 5) for f in a211_certs(nid)]              # A229: the page cert AND every per-start shard cert
    for camp, f, rank in [("A206", os.path.join(ATT, "A206-named-split", "certs", "namedsplit206_%s.json" % nid), 3),
                          ("A209", os.path.join(ATT, "A209-k5-killer", "certs", "k5killer209_%s.json" % nid), 4)] + a211:
        doc = jload(f)
        for run, d in ((doc or {}).get("runs") or {}).items():
            nodes = d.get("nodes") or []
            out.append(dict(camp=camp, file=os.path.abspath(f), run=run, pad=d.get("pad"), mode=d.get("mode") or "tree", source=d.get("source"),
                            root_label=(d.get("leaf_label") or "R") if d.get("mode") == "leaf" else "R", nodes=nodes, rank=rank))
    return [t for t in out if t["nodes"]]


# ---------------------------------------------------------------- path keys inside one tree
def parse(label, root):
    """-> (canonical label, suffix): 'R.1.1.4u' -> ('R.1.1.4', 'u'); 'R.2s.1r1' with root 'R.2s' -> ('R.2s.1', 'r1')."""
    if not label.startswith(root):
        return None, None
    parts = label[len(root):].split(".")
    idx, suf = [], parts[0]
    for s in parts[1:]:
        m = SEG.match(s)
        if not m:
            return None, None
        idx.append(m.group(1))
        suf = m.group(2)
    return root + "".join("." + i for i in idx), suf


def step_of(n):
    """the hypothesis this record adds, as a hashable key -- None for a refresh / sharp / exact record."""
    kind = str(n.get("kind") or ("row" if n.get("rows") is not None else ""))
    if kind.startswith("ns-"):
        return ("ns", str(n.get("slot")), str(n.get("role") or n.get("ns_role") or "?"), kind)
    if kind == "pocket":
        return ("pocket", tuple(round(float(v), 6) for v in (n.get("pocket") or ())), tuple(n.get("rows") or ()))
    if kind == "rsplit":                                          # a CHILD rsplit record carries only the label:
        return None                                               # its key comes from the parent's branch list
    if n.get("rows") is not None and n.get("slot"):
        return ("row", str(n.get("slot")), tuple(n.get("rows")))
    return None


def br_of(n):
    """the branch dict the tree's apply_* functions want, rebuilt from the record."""
    kind = str(n.get("kind") or "row")
    if kind == "inherited":
        kind = "pair" if len(n.get("rows") or ()) > 1 else "row"
    return dict(slot=n.get("slot"), rows=n.get("rows"), kind=kind, named=n.get("named"), role=n.get("role"),
                frac=n.get("frac"), alive_rows=n.get("alive_rows"), pocket=n.get("pocket"))


def keyed(tree, rootpath):
    """-> dict(root, order, path, own, recs, kids) over the CANONICAL labels of one tree.  A unit-propagation record
    (label + 'u') adds NO step: its hypothesis is DERIVED at the node by sound clips (the slot had one surviving
    branch), so the node keeps the weaker path and a kill there kills the weaker hypothesis too."""
    root = tree["root_label"]
    recs, order = {}, []
    for n in tree["nodes"]:
        c, _suf = parse(n.get("label") or "", root)
        if c is None:
            continue
        recs.setdefault(c, []).append(n)
        if c not in order:
            order.append(c)
    path = {root: tuple(rootpath)}
    for c in order:                                               # an A211 start-run root / inherited row carries its own key
        for n in recs[c]:
            if n.get("path_key") is not None:
                path[c] = tuple(norm(s) for s in n["path_key"])
                break
    kids, changed = {}, True
    while changed:                                                # the CERTIFIED branch list, never the recorded children:
        changed = False                                           # a wall-stopped tree records fewer children than it proved
        for c in order:
            if c not in path or c in kids:
                continue
            n = next((r for r in recs[c] if r.get("branch_rows")), None)
            if n is None:
                continue
            kids[c] = branches_of(n, path[c], c)
            for p, _br, lab in kids[c]:
                if lab not in path:
                    path[lab] = p
                    changed = True
    return dict(root=root, order=order, path=path, recs=recs, kids=kids)


def rsplit_branch(n, rows, i):
    """A211 Lemma ROLE-SPLIT (notes/coarse_tree.md s.5) -> (step key, branch dict).  The PARENT record carries
    `rsplit` = the role spec with `m` stringified (the exact rational); `branch_rows[i]` is only the printable label
    ("t>=53.1301"), and rsplit211.branches emits side 'lo' first, 'hi' second.  The step key is exactly
    tree211.Tree211.step_key's, so a live branch and an inherited one share one path."""
    rs = n.get("rsplit") or {}
    role = str(rs.get("role") or n.get("branch_role") or n.get("branch_slot"))
    dim, m, side = str(rs.get("dim")), str(rs.get("m")), ("lo" if i == 0 else "hi")
    try:
        m_f = float(str(rows).split("=")[-1])
    except ValueError:
        m_f = None
    br = dict(slot=role, role=role, kind="rsplit", rows=[rows], named=None, dim=dim, side=side, m=m, m_f=m_f,
              extents=rs.get("extents"), core_empty=rs.get("core_empty"), box=rs.get("box"))
    return ("rsplit", role, dim, m, side), br


def branches_of(n, base, c):
    """the exhaustive disjunction a record proved at its node -> [(child path, child branch dict, child label)]."""
    slot, role, pk = n.get("branch_slot"), n.get("branch_role"), n.get("pockets") or []
    out = []
    for i, rows in enumerate(n.get("branch_rows") or []):
        lab = "%s.%d" % (c, i + 1)
        if n.get("rsplit") and isinstance(rows, str):             # Lemma ROLE-SPLIT: `rows` is a label, not row indices
            st, br = rsplit_branch(n, rows, i)
            out.append((base + (st,), br, lab))
            continue
        if rows in ("meets", "misses"):
            st = ("ns", str(slot), str(role), "ns-" + rows)
            br = dict(slot=slot, role=role, kind="ns-" + rows, rows=None, named=None, frac=None, alive_rows=None)
        elif slot == "pocket":
            p = [round(float(v), 6) for v in (pk[i] if i < len(pk) else [])]
            st = ("pocket", tuple(p), (i,))
            br = dict(slot="pocket", kind="pocket", rows=[i], pocket=p, named=None, role=None)
            lab = "%s.p%d" % (c, i + 1)
        else:
            st = ("row", str(slot), tuple(rows))
            br = dict(slot=slot, rows=list(rows), kind="pair" if len(rows) > 1 else "row", named=None, role=None)
        out.append((base + (st,), br, lab))
    return out


def closed(K, c, seen=None):
    """the subtree at c is CLOSED: c itself DEAD, or it branched and every branch of the CERTIFIED list is closed."""
    seen = seen or set()
    if c in seen:
        return False
    seen.add(c)
    if any(r.get("verdict") == "DEAD" for r in K["recs"].get(c, [])):
        return True
    ks = K["kids"].get(c) or []
    return bool(ks) and all(k in K["recs"] and closed(K, k, seen) for _p, _b, k in ks)


# ---------------------------------------------------------------- the leaf-kill ledgers (A210 / A208 / A207)
def leaf_kills(nid, pad):
    """-> [(cert file, label, rule, ledger)] for every DEAD leaf kill recorded against a prior node of (page, pad)."""
    out = []
    a209 = os.path.join(ATT, "A209-k5-killer", "certs", "k5killer209_%s.json" % nid)
    for r in jl(os.path.join(ATT, "A210-corner-cover", "results", "cornercover210_leaves.jsonl")):
        if r.get("nid") == nid and r.get("pad") == pad and r.get("verdict") == "DEAD":
            out.append((os.path.abspath(a209), r.get("label"), "CC (A210 Lemma CORNER-COVER)",
                        "attempts/A210-corner-cover/results/cornercover210_leaves.jsonl"))
    for r in jl(os.path.join(ATT, "A208-noroom-leaves", "results", "noroom208.jsonl")):
        run = str(r.get("run") or "")
        if r.get("nid") == nid and r.get("verdict") == "DEAD" and (run.startswith(pad + "_") or run == "pad_%s" % pad):
            out.append((os.path.join(ROOT, r["cert"]), r.get("leaf"), "NO-ROOM (A189 Lemma 1 / Lemma CN)",
                        "attempts/A208-noroom-leaves/results/noroom208.jsonl"))
    for r in jl(os.path.join(ATT, "A207-basin-clip", "results", "basinclip207.jsonl")):
        if r.get("nid") == nid and r.get("pad") == pad and r.get("verdict") == "DEAD" and r.get("leaf_label"):
            out.append((os.path.join(ROOT, r["source"]), r.get("leaf_label"), "BASIN (A207 Lemma BASIN)",
                        "attempts/A207-basin-clip/results/basinclip207.jsonl"))
    return out


# ---------------------------------------------------------------- the merge: ONE trie over every prior tree
def keyed_trees(nid, pad, start_file, log=print):
    """[(tree, keyed)] for every prior tree of (page, pad) whose root the A203 start -- or a resolved leaf -- fixes."""
    K, pending = [], [t for t in sources(nid) if t["pad"] == pad]
    for _ in range(6):
        left = []
        for t in pending:
            if t["mode"] != "leaf" and (start_file is None or t["source"] in (None, start_file)):
                K.append((t, keyed(t, ())))
            elif t["mode"] == "leaf" and t.get("source"):
                src = os.path.abspath(os.path.join(ROOT, t["source"]))
                hit = next(((tt, kk) for tt, kk in K if os.path.abspath(tt["file"]) == src and t["root_label"] in kk["path"]), None)
                if hit is None:
                    left.append(t)
                else:
                    K.append((t, keyed(t, hit[1]["path"][t["root_label"]])))
            else:
                left.append(t)
        if not left or len(left) == len(pending):
            break
        pending = left
    return K


def trie(K, kills):
    """the merged trie: path -> dict(dead, kids, rank, recs).  The branch list at a path is the one the HIGHEST-ranked
    tree recorded there (each is exhaustive on its own, A205 Lemma CT); a path closed anywhere is DEAD (Lemma INHERIT)."""
    G = {}
    for t, kk in sorted(K, key=lambda x: x[0]["rank"]):
        for c in kk["order"]:
            if c not in kk["path"]:
                continue
            p = kk["path"][c]
            g = G.setdefault(p, dict(dead=None, kids=None, rank=-1, recs=[]))
            g["recs"].append((t["rank"], t, kk, c))
            if g["dead"] is None and closed(kk, c):
                g["dead"] = dict(cert=rel(t["file"]), run=t["run"], camp=t["camp"], label=c, rule="tree: %s" % (
                    next((r.get("clip") for r in kk["recs"].get(c, []) if r.get("clip")), "every branch DEAD")))
            ks = kk["kids"].get(c) or []
            if ks and t["rank"] >= g["rank"]:
                g["kids"] = list(ks)
                g["rank"] = t["rank"]
    for cert, label, rule, ledger in kills:
        for t, kk in K:
            if os.path.abspath(t["file"]) == os.path.abspath(cert) and label in kk["path"]:
                g = G.setdefault(kk["path"][label], dict(dead=None, kids=None, rank=-1, recs=[]))
                if g["dead"] is None:
                    g["dead"] = dict(cert=rel(cert), run=t["run"], camp=t["camp"], label=label, rule=rule, ledger=ledger)
                break
    return G


def walk(G, p, dead, starts, BR, depth=0):
    g = G.get(p)
    if g and g["dead"]:
        dead.append((p, g["dead"]))
        return
    if g and g["kids"] and depth < 24:
        for cp, br, lab in g["kids"]:
            BR[cp] = br
            walk(G, cp, dead, starts, BR, depth + 1)
        return
    starts.append(p)


def snap_complete(n):
    """the record's snapshot holds EVERY piece of every named role -- it was not written at the 300-piece cap, so
    startload211.fill can load it (padded outward) as a SUPERSET.  A capped snapshot is a SUBSET of the node's pose
    set: loading it would be unsound, so it never becomes a start node's ancestor (A211h)."""
    snap = n.get("snapshot") or {}
    roles = snap.get("roles") or {}
    for k, v in roles.items():
        if k.startswith("P"):
            continue
        if int(v.get("n_pieces", 0) or 0) > len(v.get("pieces") or []):
            return False
    return bool(roles)


def anc_snapshots(G, p):
    """A211h -- EVERY ancestor of p on p's own chain that carries a COMPLETE snapshot, DEEPEST FIRST.  Each is a
    PREFIX hypothesis of p, so its pose set is a superset -- sound (Lemma INHERIT, "how a start node is loaded").
    A CAPPED snapshot is skipped rather than refused: the loader climbs to the next complete ancestor, and an empty
    list means the start node is replayed from the page's own A203 stage-0 root (still a superset: the root is the
    weakest hypothesis of all)."""
    out = []
    for i in range(len(p), -1, -1):
        best = None
        for rank, t, kk, c in (G.get(p[:i]) or {}).get("recs", []):
            for n in kk["recs"].get(c, []):
                if n.get("snapshot") and snap_complete(n) and (best is None or rank >= best[0]):
                    best = (rank, t, kk, c, n.get("label"), (n.get("snapshot") or {}).get("round"))
        if best is not None:
            out.append((i,) + best)
    return out


def anc_snapshot(G, p):
    """the deepest COMPLETE snapshot on p's own chain (None: p is replayed from the A203 stage-0 root)."""
    a = anc_snapshots(G, p)
    return a[0][:6] if a else None


def cands_of(G, BR, p):
    """A211h -- the ancestors the start node p may be loaded from, BEST (deepest) FIRST, each with the branch steps
    that must be replayed from it; the LAST entry is always the page's own A203 stage-0 root (cert None, every step
    replayed), so a start node is never refused merely because the snapshots on its chain were written at the cap."""
    out = []
    for i, _rank, t, _kk, _c, lab, rnd in anc_snapshots(G, p):
        out.append(dict(cert=rel(t["file"]), run=t["run"], camp=t["camp"], anc_label=lab, anc_steps=i, snapshot_round=rnd,
                        steps=[BR[p[:j + 1]] for j in range(i, len(p))]))
    out.append(dict(cert=None, run=None, camp="A203", anc_label=None, anc_steps=0, snapshot_round=None,
                    steps=[BR[p[:j + 1]] for j in range(0, len(p))]))
    return out


def merge(nid, pad, start_file, log=print):
    """-> dict(dead_paths, starts, info)."""
    K = keyed_trees(nid, pad, start_file, log=log)
    G = trie(K, leaf_kills(nid, pad))
    dead, starts, BR = [], [], {}
    walk(G, (), dead, starts, BR)
    out, n_root = [], 0
    for p in starts:
        cands = cands_of(G, BR, p)
        top = cands[0]
        n_root += top["cert"] is None
        if top["cert"] is None:
            log("   INHERIT: the start path %s carries no COMPLETE ancestor snapshot -- it is replayed from the A203 "
                "stage-0 root (%d steps)" % (list(map(str, p)), len(p)))
        named = sorted((G.get(p) or {}).get("recs", []), key=lambda r: -r[0])
        if named:
            label = named[0][3]
        elif top["anc_label"] and top["anc_steps"] == len(p):
            label = top["anc_label"]
        else:
            label = "%s+%s" % (top["anc_label"] or "R0", "".join("/" + str(s[1]) for s in p[top["anc_steps"]:]))
        rv = next((r.get("verdict") for r in (named[0][2]["recs"].get(named[0][3]) or [])), None) if named else None
        out.append(dict(label=label, path=[list(map(str, s)) for s in p], key=[list(s) for s in p], n_steps=len(p),
                        cert=top["cert"], run=top["run"], camp=top["camp"], anc_label=top["anc_label"],
                        anc_steps=top["anc_steps"], snapshot_round=top["snapshot_round"], steps=top["steps"],
                        cands=cands, n_cands=len(cands), pad=pad, nid=nid,
                        recorded=dict(verdict=rv, depth=len(p))))
    info = dict(nid=nid, pad=pad, start_file=start_file, n_trees=len(K), n_paths=len(G),
                trees=[dict(camp=t["camp"], cert=rel(t["file"]), run=t["run"], mode=t["mode"], n_nodes=len(t["nodes"]),
                            rooted_at=kk["root"], root_steps=len(kk["path"][kk["root"]])) for t, kk in K],
                inherited_dead=[dict(path=[list(map(str, s)) for s in p], key=[list(s) for s in p], n_steps=len(p), **v) for p, v in dead],
                n_inherited_dead=len(dead), n_start_nodes=len(out), n_start_from_root=n_root,
                start_nodes=[dict(brief(s), steps=[dict(b) for b in s["steps"]]) for s in out])
    log("   INHERIT %s pad %s: %d prior trees, %d paths, %d branches inherited DEAD (final, with their certificates), %d start nodes (%d from the A203 root)" % (
        nid, pad, len(K), len(G), len(dead), len(out), n_root))
    return dict(dead_paths={p: v for p, v in dead}, starts=out, info=info)


def brief(s):
    """the start node as it goes into a certificate / a log line: the replay steps and each fallback ancestor COUNTED."""
    return dict(s, steps=len(s["steps"]), cands=[dict(c, steps=len(c["steps"])) for c in (s.get("cands") or [])])


def norm(s):
    return tuple(norm(x) if isinstance(x, (list, tuple)) else x for x in s)


def path_tuple(sn):
    """the start node's path as the hashable key the live tree extends (survives a JSON round trip)."""
    return tuple(norm(s) for s in (sn.get("key") or ()))


def covered(dead_paths, p):
    """-> the certificate info when the path p (or a prefix of it) is already closed by a prior certificate."""
    for i in range(len(p) + 1):
        if p[:i] in dead_paths:
            return dead_paths[p[:i]], p[:i]
    return None, None


if __name__ == "__main__":
    import sys
    r = merge(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "zero", sys.argv[3] if len(sys.argv) > 3 else None)
    if r:
        i = r["info"]
        print(json.dumps(dict(i, start_nodes=[dict(s, steps=len(s["steps"])) for s in i["start_nodes"]]), indent=1, default=str))
