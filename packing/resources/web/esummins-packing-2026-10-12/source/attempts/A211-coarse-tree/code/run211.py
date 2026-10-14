"""A211 driver -- ONE runner for the COARSE tree on one node (a gallery page or an A57 tree record):
   python run211.py page <nid> [--wall 1800] [--pads zero,g1] [--depth 6] [--nodes 600] [--force] [--no-resume]
                              [--start LABEL[,LABEL...]] [--cert-suffix TAG]      # A229: ONE SHARD of the page
Per pad, PAD 0 FIRST (a pad-0 kill is s0-only, WINDOW-PENDING; the window pad follows): stage 0 (A202 closed form +
A203 CSP, cached), then the coarse tree (tree211: cheap coarse internal nodes, the leaf rules at every fully named
leaf: rule CC -> no-room + pockets -> basin clip -> Rule NS -> the exact cascade last).  One certificate per node
certs/coarsetree211_<nid>.json (every node with its seconds), one slim row per (pad) run in
results/coarsetree211.jsonl, the page docs/residue_map/campaigns/A211-coarsetree/coarsetree211_<nid>.svg; the pad-0
verdict printed beside the window verdict.  Copied from A209's run209.py (the chain's driver) and changed here only."""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CERTS = os.path.abspath(os.path.join(HERE, "..", "certs"))
RES = os.path.abspath(os.path.join(HERE, "..", "results", "coarsetree211.jsonl"))
sys.path.insert(0, HERE)
import load211                                                 # noqa: E402
load211.install()
import stage209                                                # noqa: E402
import poly204 as P                                            # noqa: E402
import tree206 as N6                                           # noqa: E402
import clip207 as C                                            # noqa: E402
import coarse211 as C11                                        # noqa: E402
import tree211 as N11                                          # noqa: E402
import inherit211 as INH                                       # noqa: E402
import startload211 as SL                                      # noqa: E402
import noroommemo211 as NRM                                    # noqa: E402
import fig211                                                  # noqa: E402

C11.install()
FP, QP, MB = P.FP, P.QP, P.MB
A206CERTS = os.path.join(ROOT, "attempts", "A206-named-split", "certs")
VERIFIER = ("[C: closed-form / library clip trace + the leaf lemma (Lemma CORNER-COVER / A189 Lemma 1 / Lemma CN / Lemma BASIN) + Lemma INHERIT] A211 coarse tree "
            "(notes/coarse_tree.md): A202 stage 0 + A203 CSP; coarse internal nodes (re-binned pieces, refine 1, no lonely clip, shallow reach: supersets); "
            "at every fully named leaf rule CC (A210), A208 no-room + pocket CN bound (pockets branched at k = 9), A207 basin clip, A206 Rule NS (MAX_FRAC 0.5), "
            "then the exact A204/A205 cascade (nsub 4 / refine 2, lonely clip, sharp round); started from the MERGED state of every prior certificate "
            "(Lemma INHERIT: branches closed by A205 / A206 / A209 / A210 / A208 / A207 are FINAL and cited; the tree runs only the remaining start nodes, "
            "loaded from the recorded snapshot with the pieces padded outward); DEAD iff every branch DEAD (Lemma CT); no verifier clause")
if N11.SNAP.ON:                                                   # A224: the flag is ON for this run -- say so in the clause
    VERIFIER += ("  [A224 Rule SNAP is ON as leaf rule (0) and after the coarse round at internal nodes: a node killed by SNAP / "
                 "SNAP-DIAG carries its OWN verifier clause (exact separating-axis miss certificates + Lemma SWAP / teleport + "
                 "Theorem FC Step 2 + the target stratum's FULL scoreboard row); docs/proofs/snap_rule.md]")


def belownormal():
    """A210's WORKING fix: c_void_p(-1) + argtypes (the lab's old snippet silently no-ops)."""
    try:
        import ctypes
        k = ctypes.windll.kernel32
        k.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint]
        k.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
        k.GetPriorityClass.argtypes = [ctypes.c_void_p]
        h = ctypes.c_void_p(-1)
        k.SetPriorityClass(h, 0x00004000)
        k.SetProcessAffinityMask(h, 0xFFFF)
        print("   priority class %d (16384 = BelowNormal), affinity 0xFFFF" % k.GetPriorityClass(h), flush=True)
    except Exception as e:                                        # noqa: BLE001
        print("   belownormal failed: %r" % (e,), flush=True)


def save(doc, cert):
    os.makedirs(os.path.dirname(cert), exist_ok=True)
    tmp = cert + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1, default=str)
    for k in range(8):
        try:
            os.replace(tmp, cert)
            return
        except PermissionError:
            time.sleep(2 + 3 * k)
    with open(cert, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1, default=str)


NOFIG = False


def draw(doc):
    if NOFIG:
        return
    try:
        return fig211.render(doc)
    except Exception as e:                                        # noqa: BLE001
        import traceback
        traceback.print_exc()
        print("   fig211 failed: %r" % (e,), flush=True)


def closed_subtree(nodes, label):
    sub = [n for n in nodes if n["label"] == label or (n["label"].startswith(label) and n["label"][len(label)] in ".rusx")]
    return bool(sub) and all(n.get("verdict") != "ALIVE" for n in sub) and any(n.get("verdict") == "DEAD" for n in sub)


def a206_inherited(nid, pad, source):
    """(slot, rows) -> the A206 whole-tree run's closed depth-1 branch on the same page, pad and A203 start (A209's rule)."""
    f = os.path.join(A206CERTS, "namedsplit206_%s.json" % nid)
    out = {}
    if not os.path.exists(f):
        return out
    try:
        doc = json.load(open(f, encoding="utf-8"))
    except Exception:
        return out
    for key, d in (doc.get("runs") or {}).items():
        if d.get("mode") != "tree" or d.get("pad") != pad or d.get("source") != source:
            continue
        nodes = d.get("nodes") or []
        for n in nodes:
            if n.get("depth") != 1 or n.get("rows") is None or str(n.get("kind") or "").startswith("ns-") or n.get("kind") in ("refresh", "sharp") or "." not in n["label"]:
                continue
            if closed_subtree(nodes, n["label"]):
                out[(n.get("slot"), tuple(n["rows"]))] = dict(run=key, label=n["label"], cert=os.path.relpath(f, ROOT).replace("\\", "/"), leaf=n.get("leaf") or n.get("reason"))
    return out


def wall_limited(d):
    """A211g -- the pad's recorded run stopped on the WALL (or a node cap), so a fresh wall can still make progress:
    the re-run inherits this certificate's own DEAD branches (inherit211 ranks A211 highest) and restarts exactly at
    the alive frontier.  A DEAD pad and a stage-0 kill are FINAL: those stay cached.
    A211h -- a pad left ALIVE because a start node "could not be loaded soundly" is ALSO re-runnable: that refusal was
    the LOADER's, not the geometry's, and startload211 now climbs to the nearest COMPLETE ancestor (the page's A203
    stage-0 root at worst) instead of refusing."""
    if not isinstance(d, dict) or d.get("stage0_kill") or d.get("verdict") == "DEAD":
        return False
    if d.get("wall"):
        return True
    if any(("wall" in str(u.get("reason") or "")) or ("node cap" in str(u.get("reason") or ""))
           or ("could not be loaded soundly" in str(u.get("reason") or "")) for u in (d.get("undecided") or [])):
        return True
    # PI 2026-09-14: a leaf left "every forced slot has two named meeters ... no-room UNDECIDED (k=10, m=1)" is now
    # decidable by Lemma POCKET at m = 1 (the 11th square branched into the pockets): re-run such pads too
    # A229: a SHARD run (--start) leaves the start nodes it was not given as "SKIPPED (filter)" -- that refusal is the
    # FILTER's, not the geometry's, so the shard is always re-runnable on a fresh wall (its cert lives in its own file)
    if any("SKIPPED (filter)" in str(u.get("reason") or "") for u in (d.get("undecided") or [])):
        return True
    return any(("no-room UNDECIDED" in str(u.get("reason") or "")) or ("undecided leaf" in str(u.get("reason") or ""))
               or ("every forced slot has two named meeters" in str(u.get("reason") or ""))
               for u in (d.get("undecided") or []))


def page_doc(doc, pg):
    doc.setdefault("cells", [FP.rect_f(c["rect"]) for c in pg.cells])
    doc.setdefault("slots", list(pg.slots))
    doc.setdefault("wbox", {p: FP.rect_f(pg.item[p]["wb"]) for p in pg.slots})
    doc.setdefault("wbox_pad", {})[pg.pad] = {p: FP.rect_f(pg.item[p]["wb"]) for p in pg.slots}
    doc.setdefault("H_record", [round(v, 6) for v in pg.record_H])


def brief_nodes(nodes):
    return [dict(label=n["label"], depth=n.get("depth"), verdict=n.get("verdict"), clip=n.get("clip"), kind=n.get("kind"), seconds=n.get("seconds"),
                 coarse=n.get("coarse"), n_roles=len(n.get("roles") or {}), reason=str(n.get("reason") or "")[:80]) for n in nodes]


def row_of(doc, key, cert):
    d = doc["runs"][key]
    slim = dict(nid=doc["nid"], cls=doc.get("cls"), record=doc.get("record"), tree=doc.get("tree"), applies_to_tags=[doc.get("tree")] if doc.get("tree") else [],
                run=key, pad=d.get("pad"), mode="page", source=d.get("source"), cfg=d.get("cfg"), lam=d.get("lam"), verdict=d.get("verdict"), leaf=d.get("leaf"),
                n_nodes=d.get("n_nodes"), n_records=d.get("n_records"), max_depth=d.get("max_depth"), alive_leaves=d.get("alive_leaves"), dead_leaves=d.get("dead_leaves"),
                ns_splits=d.get("ns_splits"), pocket_splits=d.get("pocket_splits"), cc_kills=d.get("cc_kills"), exact_rounds=d.get("exact_rounds"), basin_kills=d.get("basin_kills"),
                rsplits=d.get("rsplits"), rsplit_kills=d.get("rsplit_kills"),
                snap=dict(runs=d.get("snap_runs"), kills=d.get("snap_kills"), handoffs=d.get("snap_handoffs"),
                          partial=d.get("snap_partial"), cands=d.get("snap_cands"), seconds=d.get("snap_seconds"),
                          first_kill_t=d.get("snap_first"), rows=(d.get("snap_rows") or [])[-20:]),
                noroom=[dict(label=r["label"], k=r["k"], verdict=r["verdict"], clip=r["clip"], seconds=r["seconds"]) for r in (d.get("noroom_runs") or [])],
                inherited=d.get("inherited"), inherited_dead=d.get("inherited_dead"), inherited_alive=d.get("inherited_alive"), n_inherited=d.get("n_inherited"),
                inherit_sources=[dict(camp=e.get("camp"), label=e.get("label"), rule=e.get("rule"), cert=e.get("cert"), ledger=e.get("ledger"))
                                 for e in ((d.get("inherit") or {}).get("inherited_dead") or [])],
                start_nodes=d.get("start_nodes"), start_runs=d.get("runs"), basins=d.get("basins"), killing=d.get("killing"), undecided=d.get("undecided"), seconds=d.get("seconds"), root=d.get("root"),
                wall=d.get("wall"), window_pending=d.get("window_pending"), stage0=doc.get("stage0"), verdicts=doc.get("verdicts"), stage_reached=doc.get("stage_reached"),
                nodes_brief=brief_nodes(d.get("nodes") or []), verifier=VERIFIER, cert=os.path.relpath(cert, ROOT).replace("\\", "/"), when=time.strftime("%Y-%m-%d %H:%M:%S"))
    if d.get("start_filter") or d.get("cert_suffix"):             # A229: this row is ONE SHARD of the page, not the page
        slim.update(shard=True, start_filter=d.get("start_filter"), cert_suffix=d.get("cert_suffix"),
                    start_skipped=[u.get("label") for u in (d.get("undecided") or []) if "SKIPPED (filter)" in str(u.get("reason") or "")])
    os.makedirs(os.path.dirname(RES), exist_ok=True)
    with open(RES, "a", encoding="utf-8") as f:
        f.write(json.dumps(slim, default=str) + "\n")
    return slim


def inherited_rows(M):
    """the branches every prior certificate already closed, as FINAL grey rows on the page (Lemma INHERIT)."""
    rows = []
    for e in M["info"]["inherited_dead"]:
        p = e["path"]
        rows.append(dict(label=e["label"], depth=e["n_steps"], slot=(p[-1][1] if p else None), kind="inherited", rows=(p[-1][2] if p else None),
                         named=None, verdict="DEAD", clip="INHERIT", killed_round=None, seconds=0.0, t=0.0, n_rounds=0, snapshot=None,
                         source_cert=e["cert"], source_label=e["label"], source_camp=e["camp"], source_rule=e["rule"], source_ledger=e.get("ledger"),
                         source_path=["%s<-%s" % (s[1], s[2]) for s in p], path_key=e.get("key"),
                         reason="inherited DEAD (final) from %s %s" % (e["camp"], e["cert"]),
                         leaf="Lemma INHERIT (notes/coarse_tree.md s.4): the hypothesis %s is refuted by %s [%s] -- %s" % (
                             "; ".join("%s<-%s" % (s[1], s[2]) for s in p), e["camp"], e["rule"], e["cert"]),
                         verifier="[C: library clip trace] inherited (Lemma INHERIT): %s" % e["cert"]))
    return rows


def run_tree(doc, a, pad, cert, log=print):
    """PAD's run = the MERGED prior state: the inherited dead branches (final, cited) + one coarse tree per START NODE."""
    T = FP.Trace(wall=a.wall)                                     # A211g: ONE fresh clock per pad run, started HERE --
    assert T.left() is not None and abs(T.left() - a.wall) < 1.0  # never a Trace carried over from a previous run or
    rec, cls, row = FP.load_page(a.nid)                           # reconstructed from a snapshot's `t` (provenance only)
    start = stage209.start_of(a.nid, pad)
    basins = C.load_basins(cls, pad, QP.PADS[pad]) if pad != "zero" else []
    key = "%s_page" % pad
    M = None if a.no_inherit else INH.merge(a.nid, pad, start.get("file"), log=log)
    base = C11.CoarsePage(rec, cls, a.nid, T, pad=pad, start=start, basins=basins)
    page_doc(doc, base)
    rows = inherited_rows(M) if M else []
    starts = list((M or {}).get("starts") or [])
    dead_paths = (M or {}).get("dead_paths") or {}
    d = doc["runs"][key] = dict(pad=pad, mode="page", source=start.get("file"), lam=float(base.lam), start=start, verdict="RUNNING", nodes=list(rows),
                                basins=[C.basin_json(b) for b in basins], verifier=VERIFIER, inherit=(M["info"] if M else None),
                                inherited_dead=len(rows), inherited_alive=len(starts), start_nodes=[INH.brief(s) for s in starts],
                                cfg=dict(rounds=a.rounds, depth_cap=a.depth, node_cap=a.nodes, wall=a.wall, inherit=not a.no_inherit,
                                         coarse=dict(grid=[C11.NX, C11.NY, C11.NB], cap=C11.CAP, refine=C11.REFINE, max_iter=C11.MAX_ITER,
                                                     nsub=C11.NSUB, depth=C11.DEPTH, jdepth=C11.JDEPTH, kmode=C11.KMODE, n_grid=C11.NGRID,
                                                     conditional=dict(parent_seconds=C11.COARSE_SECONDS, roles=C11.COARSE_ROLES,
                                                                      fallback=dict(kmode="pieces", n_grid=C11.NGRID_FALL))),
                                         exact=C11.EXACT, exact_rounds=N11.EXACT_ROUNDS, noroom_cap=N11.NOROOM_CAP, soft_all=N6.SOFT_ALL, max_frac=N6.MAX_FRAC,
                                         a220=dict(exact_first=N11.EXACT_FIRST, budget=N11.BUDGET, rounds=N11.EXACT_FIRST_ROUNDS, small_ext=N11.SMALL_EXT,
                                                   noroom_inherit=N11.NOROOM_INHERIT, child_cap=N11.NOROOM_CHILD_CAP, shrink=N11.NR_SHRINK),
                                         a224=dict(snap=N11.SNAP.ON, eps=N11.SNAP.EPS_C, deg=N11.SNAP.DEG)))
    if getattr(a, "start_only", None) or getattr(a, "cert_suffix", None):
        d.update(start_filter=sorted(a.start_only or []), cert_suffix=a.cert_suffix,
                 shard="A229: ONE SHARD of this page -- only the start nodes in start_filter were run; the others are "
                       "recorded SKIPPED (filter) and are the sibling shards' work.  This certificate is merged with "
                       "the page certificate (and every sibling shard's) on the PATH KEY by Lemma INHERIT file-wise "
                       "(attempts/A229-start-parallel/notes/parallel229.md).")
    log("== %s page pad %s: start %s; basins %s; INHERIT %d dead branches (final) + %d start nodes %s; H %s; forced H %s; %d slots; free squares %d" % (
        a.nid, pad, start.get("file"), [(b["cell"], float(b["rc"])) for b in basins], len(rows), len(starts), [s["label"] for s in starts][:10],
        [round(v, 3) for v in base.roles[base.H]], sorted(base.forced_H), len(base.slots), base.n_free))
    for r in rows:
        log("   INHERITED DEAD %-12s %s<-%s  [%s %s] %s" % (r["label"], r["slot"], r["rows"], r["source_camp"], r["source_rule"], r["source_cert"]))
    agg = run_starts(doc, d, a, pad, cert, T, rec, cls, start, basins, rows, starts, dead_paths, base, M is not None, log=log)
    agg["wall"] = T.out_of_time()
    agg["window_pending"] = (pad == "zero") and agg["verdict"] == "DEAD"
    agg["leaf"] = None
    if agg["verdict"] == "DEAD":
        agg["leaf"] = "every branch DEAD (%d inherited from prior certificates + %d proved here): " % (len(rows), len(agg["killing"]) - len(rows)) + "; ".join(
            "%s %s<-%s by %s" % (k["label"], k.get("slot") or "root", k.get("rows"), k["clip"]) for k in agg["killing"][:40])
        if agg["window_pending"]:
            agg["leaf"] += " [pad 0: s0-only, WINDOW-PENDING]"
    agg["tests"], agg["steps"], agg["seconds"] = T.tests[-4000:], T.steps[-2000:], round(T.now(), 1)
    d.update(agg)
    log("   => %s (%s) in %.1f s: %d start runs, %d nodes, depth %d, %d CC kills, %d exact leaf cascades, %d NS splits, %d pocket splits, "
        "%d role splits (%d empty-half kills), %d inherited dead (%d up front + %d in tree), %d dead / %d alive leaves%s" % (
            agg["verdict"], key, agg["seconds"], len(starts), agg["n_nodes"], agg["max_depth"], agg["cc_kills"], agg["exact_rounds"], agg["ns_splits"],
            agg["pocket_splits"], agg["rsplits"], agg["rsplit_kills"], agg["n_inherited"], len(rows), agg["n_inherited"] - len(rows), agg["dead_leaves"],
            agg["alive_leaves"], " (WALL)" if agg["wall"] else ""))
    log("   A224 Rule SNAP [%s]: %d evaluation(s), %d candidate(s), %d KILL(s), %d hand-off(s), %d partial (anonymous squares left), %.2f s; first kill at t = %s s" % (
        "ON" if N11.SNAP.ON else "OFF (flag A224_SNAP)", agg.get("snap_runs") or 0, agg.get("snap_cands") or 0, agg.get("snap_kills") or 0,
        agg.get("snap_handoffs") or 0, agg.get("snap_partial") or 0, agg.get("snap_seconds") or 0.0, agg.get("snap_first")))
    log("   A220: exact-first %d run(s), %d kill(s), %d timeout(s), %.1f s; short no-room cap %d time(s) [flags %s]" % (
        agg.get("ef_runs") or 0, agg.get("ef_kills") or 0, agg.get("ef_timeouts") or 0, agg.get("ef_seconds") or 0.0, agg.get("nr_short") or 0,
        d["cfg"]["a220"]))
    log("   per node: " + "; ".join("%s d%s %s%s %ss%s" % (n["label"], n.get("depth"), n.get("verdict"), (" " + n["clip"]) if n.get("clip") else "",
                                                           n.get("seconds"), "" if n.get("coarse", True) else " [exact]") for n in d["nodes"]))
    return key, agg["verdict"]


def run_starts(doc, d, a, pad, cert, T, rec, cls, start, basins, rows, starts, dead_paths, base, have_merge, log=print):
    """one coarse tree per start node (the shared wall); the pad is DEAD iff every start node's tree is DEAD."""
    agg = dict(verdict="DEAD", n_nodes=0, n_records=len(rows), max_depth=0, alive_leaves=0, dead_leaves=len(rows), ns_splits=0, pocket_splits=0,
               cc_kills=0, exact_rounds=0, basin_kills=0, rsplits=0, rsplit_kills=0, n_inherited=len(rows),
               ef_runs=0, ef_kills=0, ef_timeouts=0, ef_seconds=0.0, nr_short=0,
               snap_runs=0, snap_kills=0, snap_handoffs=0, snap_partial=0, snap_cands=0, snap_seconds=0.0,
               snap_first=None, snap_rows=[], killing=list(
                   dict(label=r["label"], slot=r["slot"], rows=r["rows"], clip="INHERIT", round=None, seconds=0.0, cert=r["source_cert"]) for r in rows),
               undecided=[], noroom_runs=[], inherited={}, runs=[], root=None, basin_clips=[])
    done = []
    if have_merge and not starts:                                 # every branch of the merged trie is already closed
        log("   every branch of the merged prior state is DEAD: nothing left to run (Lemma INHERIT (c))")
    only = set(getattr(a, "start_only", None) or [])
    if only:                                                      # A229: say exactly which of the asked-for labels exist NOW
        have = set((s or {}).get("label", "R") for s in (starts if have_merge else [None]))
        miss = sorted(only - have)
        log("   A229 SHARD: --start %s -- %d of them are start nodes of this page/pad right now (%d start nodes in all)%s"
            % (",".join(sorted(only)), len(only & have), len(have),
               ("; NOT PRESENT (already dead, or the queue is stale -- re-run queue229.py): %s" % ",".join(miss)) if miss else ""))
    for sn in (starts if have_merge else [None]):
        if only and (sn or {}).get("label", "R") not in only:      # A229: this shard was given other start nodes
            agg["verdict"] = "ALIVE"
            agg["undecided"].append(dict(label=(sn or {}).get("label", "R"),
                                         reason="undecided: SKIPPED (filter) -- this run is the shard --start %s of the page; "
                                                "this start node belongs to a sibling shard of the same pass" % ",".join(sorted(only))))
            log("   start %s: SKIPPED (filter)" % (sn or {}).get("label", "R"))
            continue
        if T.out_of_time():
            agg["verdict"] = "ALIVE"
            agg["undecided"].append(dict(label=(sn or {}).get("label", "R"), reason="undecided: the wall ran out before this start node ran"))
            log("   start %s: SKIPPED (wall)" % (sn or {}).get("label", "R"))
            continue
        try:
            pg, meta = (SL.load(sn, rec, cls, a.nid, T, pad, start, basins, rounds=a.rounds, wall=a.wall, log=log) if sn else
                        (C11.CoarsePage(rec, cls, a.nid, T, pad=pad, start=start, basins=basins), dict(label="R", path=[], steps=[], applied=[])))
        except Exception as e:                                    # noqa: BLE001
            agg["verdict"] = "ALIVE"
            agg["undecided"].append(dict(label=(sn or {}).get("label", "R"), reason="undecided: the start node could not be loaded soundly (%r)" % (e,)))
            log("   start %s: NOT LOADED (%r) -- the pad stays ALIVE" % ((sn or {}).get("label", "R"), e))
            continue
        lab = (sn or {}).get("label", "R")

        def on_node(tree):
            d["nodes"] = rows + done + tree.nodes
            d.update(n_nodes=agg["n_nodes"] + tree.n_nodes, seconds=round(T.now(), 1))
            save(doc, cert)
            draw(doc)

        tree = N11.Tree211(pg, dead_paths=dead_paths, path0=INH.path_tuple(sn) if sn else (), rounds=a.rounds, depth_cap=a.depth,
                           node_cap=a.nodes, on_node=on_node, log=log, root_label=lab)
        out = tree.run()
        for n in tree.nodes[:1]:
            n.update(start_node=lab, start_cert=(sn or {}).get("cert"), start_camp=(sn or {}).get("camp"), start_path=(sn or {}).get("path"),
                     start_anc=(sn or {}).get("anc_label"), start_meta=meta, path_key=(sn or {}).get("key") or [])
        done += tree.nodes
        agg["runs"].append(dict(label=lab, verdict=out["verdict"], n_nodes=out["n_nodes"], seconds=round(T.now(), 1), cert=(sn or {}).get("cert"),
                                anc=(sn or {}).get("anc_label"), applied=meta.get("applied"), loaded_from=meta.get("loaded_from"),
                                leaf=out.get("leaf"), wall=T.out_of_time()))
        if agg["root"] is None:
            r0 = tree.nodes[0] if tree.nodes else {}
            agg["root"] = dict(verdict=r0.get("verdict"), clip=r0.get("clip"), seconds=r0.get("seconds"), n_rounds=r0.get("n_rounds"), kept=r0.get("kept"),
                               forced_H=r0.get("forced_H"), role_slots=r0.get("role_slots"), alive_cells=r0.get("alive_cells"))
        for k in ("n_nodes", "n_records", "alive_leaves", "dead_leaves", "ns_splits", "pocket_splits", "cc_kills", "exact_rounds", "basin_kills",
                  "rsplits", "rsplit_kills", "n_inherited", "ef_runs", "ef_kills", "ef_timeouts", "ef_seconds", "nr_short",
                  "snap_runs", "snap_kills", "snap_handoffs", "snap_partial", "snap_cands", "snap_seconds"):
            agg[k] = agg.get(k, 0) + (out.get(k) or 0)
        agg["snap_rows"] += out.get("snap_rows") or []                     # A224: the per-node SNAP records
        if out.get("snap_first") is not None and agg.get("snap_first") is None:
            agg["snap_first"] = out["snap_first"]
        agg["max_depth"] = max(agg["max_depth"], out.get("max_depth") or 0)
        agg["killing"] += out.get("killing") or []
        agg["undecided"] += out.get("undecided") or []
        agg["noroom_runs"] += out.get("noroom_runs") or []
        agg["inherited"].update(out.get("inherited") or {})
        agg["basin_clips"] += list(pg.basin_rep)[-20:]
        if out["verdict"] != "DEAD":
            agg["verdict"] = "ALIVE"
        log("   start %-12s => %s (%d nodes; t = %.0f s of %s)" % (lab, out["verdict"], out["n_nodes"], T.now(), a.wall))
    d["nodes"] = rows + done
    agg["n_records"] = len(d["nodes"])
    return agg


def run_page(doc, a, cert, log=print):
    rec, cls, row = FP.load_page(a.nid)
    doc.update(cls=cls, record=(row.get("record") or "").replace("\\", "/"), tree=row.get("tree") or ("%s_interior_G1" % cls), level=row.get("level"))
    doc.setdefault("stage0", {})
    doc.setdefault("verdicts", {})
    for pad in a.pads.split(","):
        if pad in doc["verdicts"] and not a.force:
            prev = (doc.get("runs") or {}).get("%s_page" % pad) or {}
            if not (not a.no_resume and doc["verdicts"][pad] != "DEAD" and wall_limited(prev)):
                log("   pad %s: cached %s" % (pad, doc["verdicts"][pad]))
                continue
            log("   pad %s: cached %s was WALL-limited (%d undecided) -- RESUMING with a FRESH wall of %.0f s (A211g)"
                % (pad, doc["verdicts"][pad], len(prev.get("undecided") or []), a.wall))
            doc["verdicts"].pop(pad, None)
        s0 = stage209.stage0(a.nid, pad, log=log)
        doc["stage0"][pad] = s0
        doc["stage_reached"] = "0"
        if s0["verdict"] == "DEAD":
            doc["verdicts"][pad] = "DEAD (stage 0)"
            save(doc, cert)
            draw(doc)
            doc["runs"].setdefault("%s_page" % pad, dict(pad=pad, mode="page", source=s0["file"], verdict="DEAD", leaf="stage 0: %s" % s0.get("leaf"), n_nodes=0, seconds=s0.get("seconds"),
                                                            window_pending=(pad == "zero"), verifier=s0["verifier"], stage0_kill=True, nodes=[]))
            row_of(doc, "%s_page" % pad, cert)
            continue
        save(doc, cert)
        draw(doc)
        key, v = run_tree(doc, a, pad, cert, log=log)
        doc["verdicts"][pad] = v
        doc["stage_reached"] = "2 (tree)"
        save(doc, cert)
        draw(doc)
        row_of(doc, key, cert)
    log("== %s: g1 %s | pad0 %s   (pad-0 verdict beside the window verdict; a page is killed only by a DEAD g1)" % (a.nid, doc["verdicts"].get("g1"), doc["verdicts"].get("zero")))


if __name__ == "__main__":
    belownormal()
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("page",))
    ap.add_argument("nid")
    ap.add_argument("--pads", default="zero,g1")           # pad 0 FIRST
    ap.add_argument("--wall", type=float, default=1800)
    ap.add_argument("--rounds", type=int, default=1)       # the coarse node: ONE cascade round
    ap.add_argument("--depth", type=int, default=6)
    ap.add_argument("--nodes", type=int, default=600)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-resume", dest="no_resume", action="store_true",
                    help="A211g: keep a cached WALL-limited ALIVE verdict instead of re-running the pad on a fresh wall")
    ap.add_argument("--no-inherit", dest="no_inherit", action="store_true", help="ignore the prior certificates and run the page from its A203 root")
    ap.add_argument("--start", dest="start_only", default=None,
                    help="A229: run ONLY these start nodes of the page (comma separated labels, exactly as queue229.py / "
                         "pstats211 print them); every other start node is recorded SKIPPED (filter), NOT (wall).  The pad "
                         "verdict of such a run is ALIVE unless the filter happened to cover every start node left.")
    ap.add_argument("--cert-suffix", dest="cert_suffix", default=None,
                    help="A229: write this run's certificate to coarsetree211_<nid>__<TAG>.json (the page certificate is "
                         "left untouched, so sibling shards of the same page never write the same file).  Letters, digits, "
                         "'.', '_' and '-' only.  Implies --no-fig: a shard holds only part of the page.")
    ap.add_argument("--cert-dir", dest="cert_dir", default=CERTS, help="where the certificate goes (a TEST run points this away from certs/)")
    ap.add_argument("--results", default=RES, help="the jsonl the row is appended to (a TEST run points this away from results/)")
    ap.add_argument("--no-fig", dest="no_fig", action="store_true", help="do not write the SVG page (a TEST run beside the running workers)")
    a = ap.parse_args()
    a.start_only = [x for x in (a.start_only or "").replace(";", ",").split(",") if x.strip()] or None
    if a.start_only:
        a.start_only = [x.strip() for x in a.start_only]
    if a.cert_suffix:
        import re as _re
        if not _re.fullmatch(r"[A-Za-z0-9._-]+", a.cert_suffix):
            ap.error("--cert-suffix: letters, digits, '.', '_' and '-' only (it becomes part of a file name)")
    RES, NOFIG = os.path.abspath(a.results), bool(a.no_fig) or bool(a.cert_suffix)
    cert = os.path.join(os.path.abspath(a.cert_dir),
                        "coarsetree211_%s%s.json" % (a.nid, ("__" + a.cert_suffix) if a.cert_suffix else ""))
    doc = dict(nid=a.nid, runs={})
    if os.path.exists(cert) and not a.force:
        try:
            doc = json.load(open(cert, encoding="utf-8"))
        except Exception:
            doc = dict(nid=a.nid, runs={})
    run_page(doc, a, cert)
    import fastclip211 as FC211
    print("   caches (A211d, pure: same results, same test counts): K' %s; clip %s" % (FC211.rebuild_rep(), FC211.memo_rep()), flush=True)
    print("   coarse core (A211e, S2': union-hull K' on a coarse tilt grid at internal nodes): %s" % (C11.grid_rep(),), flush=True)
    print("   no-room memo (A211f, pure: A189 build_node / bisect_free across parent and children): %s" % (NRM.rep(),), flush=True)
    if not NOFIG:
        try:
            print("   gallery: %s" % fig211.gallery(), flush=True)
        except Exception as e:                                    # noqa: BLE001
            print("   gallery failed: %r" % (e,), flush=True)
