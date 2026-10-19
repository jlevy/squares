"""A211b -- load a START NODE of the merged prior state (inherit211) as a CoarsePage: load206's semantics (the recorded
node's LAST snapshot, every piece padded OUTWARD, so the loaded node is a SUPERSET of the recorded one -- sound) on any
of the campaign certificate formats (A205 doc['pads'][pad], A206 / A209 / A211 doc['runs'][run]), then the remaining
branch steps of the start node's path applied with the tree's own apply_branch / apply_ns / apply_pocket.
Each applied step is the child hypothesis of a branch list a prior certificate proved EXHAUSTIVE (Lemma INHERIT), so
the page arrives at exactly the start node's hypothesis, over-approximated."""
import json
import os

import poly204 as P
import tree205b as TB
import tree206 as N6
import tree209 as N9
import rsplit211 as RS
import coarse211 as C11
import load206 as L6
import inherit211 as INH

FP = P.FP
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def run_doc(doc, run, pad):
    if run.startswith("pad_") and doc.get("pads"):
        return doc["pads"][run[4:]]
    if doc.get("runs") and run in doc["runs"]:
        return doc["runs"][run]
    for d in (doc.get("runs") or {}).values():
        if d.get("pad") == pad:
            return d
    raise KeyError("run %s not in the certificate" % run)


def find(doc, run, pad, label, want_round=None):
    """the record `label` in this run whose snapshot is COMPLETE (A211h; `want_round` is the round inherit211 saw --
    the certificate on disk may have been rewritten since the merge read it)."""
    d = run_doc(doc, run, pad)
    hits = [n for n in (d.get("nodes") or []) if n.get("label") == label and n.get("snapshot")]
    if want_round is None:
        hits.reverse()
    else:
        hits.sort(key=lambda n: (n.get("snapshot") or {}).get("round") != want_round)
    if not hits:
        raise KeyError("node %s carries no snapshot" % label)
    for n in hits:
        if INH.snap_complete(n):
            return n
    raise ValueError("node %s: every snapshot recorded there is capped: cannot load soundly" % label)


def fill(pg, node):
    """the recorded roles / names onto the page, every piece padded outward (load206.pad_piece: a superset)."""
    snap = node["snapshot"]
    loaded = {}
    for k, v in snap["roles"].items():
        if k.startswith("P"):
            continue
        if v.get("n_pieces", 0) > len(v.get("pieces") or []):
            raise ValueError("role %s: the snapshot holds %d of %d pieces (capped): cannot load soundly" % (k, len(v["pieces"]), v["n_pieces"]))
        pcs = [L6.pad_piece(p6) for p6 in v["pieces"]]
        pg.pieces[k] = pcs
        pg.roles[k] = P.hull_box(pcs)
        pg.vol_record[k] = P.vol(pcs)
        loaded[k] = dict(n_pieces=len(pcs), box=FP.rect_f(pg.roles[k]))
    pg.forced_H = set(node.get("forced_H") or [])
    pg.role_slots = {k: tuple(v) for k, v in (node.get("role_slots") or {}).items()}
    pg.role_cell = {k: int(v) for k, v in (node.get("role_cell") or {}).items()}
    pg.cell_role = {ci: r for r, ci in pg.role_cell.items() if ci >= 0}
    pg.role_corner = {}
    for k, S in pg.role_slots.items():
        for p in S:
            if pg.item[p]["is_corner"]:
                pg.role_corner[k] = pg.item[p]["corner"]
    pg.miss = {k: frozenset(v) for k, v in (node.get("miss") or {}).items()}
    return loaded


def apply_step(pg, br, log=print):
    if str(br.get("kind") or "").startswith("ns-"):
        N6.apply_ns(pg, br)
        return "NS %s %s at %s" % (br.get("role"), br["kind"][3:], br.get("slot"))
    if br.get("kind") == "rsplit":                                # Lemma ROLE-SPLIT (notes/coarse_tree.md s.5)
        n = RS.apply_rsplit(pg, br)                               # ValueError (empty half) propagates: the caller
        return "RSPLIT %s %s%s%s (%d pieces)" % (                 # leaves the start node undecided rather than guess
            br["role"], br["dim"], "<=" if br["side"] == "lo" else ">=", br.get("m_f"), n)
    if br.get("kind") == "pocket":
        role = N9.apply_pocket(pg, [float(v) for v in br["pocket"]], (br.get("rows") or [0])[0])
        return "POCKET %s as %s" % ([round(float(v), 4) for v in br["pocket"]], role)
    TB.apply_branch(pg, br)
    return "%s <- %s" % (br.get("slot"), br.get("rows"))


def fresh_clock(T, wall):
    """A211g -- the start node must run on the RUN's own clock.  The recorded snapshot carries the elapsed time `t` of
    the run that produced it (and a resumed page carries a spent certificate): if any of that reached pg.T the loaded
    node would be out of time the instant it is built, and every start node would come back "undecided (wall) at the
    fully named leaf" in seconds.  So: T is the caller's fresh Trace, T.wall is the run's wall, and the snapshot's `t`
    is kept in meta as PROVENANCE only."""
    if wall is None:
        return
    if T.wall is None or abs(float(T.wall) - float(wall)) > 1e-6:
        raise ValueError("startload211: the Trace carries wall %r, not the run's wall %r" % (T.wall, wall))
    if T.out_of_time():
        raise ValueError("startload211: the Trace handed in is already spent (%.1f s of %.1f s): it belongs to an "
                         "earlier run -- a start node needs a FRESH Trace for this run's wall" % (T.now(), float(wall)))


def cands_of(sn):
    """A211h -- the ancestors this start node may be loaded from, deepest first (inherit211.cands_of puts the page's
    A203 stage-0 root last).  A start node from an older certificate carries only the one chosen ancestor."""
    cs = list(sn.get("cands") or [])
    if not cs:
        cs = [dict(cert=sn.get("cert"), run=sn.get("run"), camp=sn.get("camp"), anc_label=sn.get("anc_label"),
                   anc_steps=sn.get("anc_steps"), snapshot_round=sn.get("snapshot_round"), steps=sn.get("steps") or [])]
    return cs


def one(sn, cd, rec, cls, nid, T, pad, start, basins, rounds, log):
    """load the single ancestor `cd` and replay its steps -> (page, node record or None, loaded roles, applied)."""
    pg = C11.CoarsePage(rec, cls, nid, T, pad=pad, start=start, basins=basins)
    node, loaded = None, {}
    if cd.get("cert"):                                        # else: the A203 stage-0 root itself -- every step replayed
        doc = json.load(open(os.path.join(ROOT, cd["cert"]), encoding="utf-8"))
        node = find(doc, cd["run"], pad, cd["anc_label"], cd.get("snapshot_round"))
        loaded = fill(pg, node)
    applied, steps = [], cd.get("steps") or []
    for j, br in enumerate(steps):
        if pg.dead:
            break
        N6.cascade(pg, rounds, log=log)                       # the option table / nd the apply needs (coarse: one round)
        if pg.dead:
            break
        applied.append(apply_step(pg, br, log=log))
        log("   start %s: applied step %d/%d -- %s" % (sn["label"], j + 1, len(steps), applied[-1]))
    return pg, node, loaded, applied


def load(sn, rec, cls, nid, T, pad, start, basins, rounds=1, wall=None, log=print):
    """-> (CoarsePage at the start node, meta).  pg.dead is set when the replay's own coarse cascade already kills it.
    A211h: when the chosen ancestor cannot be loaded soundly (its snapshot was written at the 300-piece cap, or the
    certificate on disk no longer carries it -- A211 rewrites its own certificate per node), CLIMB to the next
    complete ancestor and replay the extra steps, the A203 stage-0 root last.  Lemma INHERIT (notes/coarse_tree.md
    s.4): a higher ancestor is a PREFIX of the same path key, so its pose set is a superset of the start node's
    parent, and every replayed step is a child of a branch list a prior certificate certified exhaustive -- the page
    still arrives at exactly the start node's hypothesis, over-approximated.  Never a silent subset."""
    fresh_clock(T, wall)
    cands, tried, err = cands_of(sn), [], None
    for cd in cands:
        try:
            pg, node, loaded, applied = one(sn, cd, rec, cls, nid, T, pad, start, basins, rounds, log)
        except Exception as e:                                # noqa: BLE001  -- a capped / missing / unreplayable ancestor
            err = e
            tried.append(dict(cert=cd.get("cert"), run=cd.get("run"), anc_label=cd.get("anc_label"),
                              anc_steps=cd.get("anc_steps"), why=repr(e)))
            log("   start %s: ancestor %s (%s) refused (%r) -- climbing to the next complete ancestor"
                % (sn["label"], cd.get("anc_label") or "A203 root", cd.get("cert") or "-", e))
            continue
        meta = dict(cert=cd["cert"], run=cd["run"], camp=cd["camp"], anc_label=cd["anc_label"], anc_steps=cd["anc_steps"],
                    label=sn["label"], path=sn["path"], n_steps=sn["n_steps"], loaded=loaded, applied=applied,
                    padding=dict(rect=float(L6.EPS_R), tilt_deg=L6.EPS_D), snapshot_round=((node or {}).get("snapshot") or {}).get("round"),
                    recorded=dict(verdict=(node or {}).get("verdict"), depth=(node or {}).get("depth"),
                                  seconds=(node or {}).get("seconds"), t=(node or {}).get("t")),   # A211g: PROVENANCE ONLY,
                    clock=dict(wall=T.wall, spent_at_load=round(T.now(), 2)),   # never the running clock (fresh_clock)
                    loaded_from=dict(mode="snapshot" if node is not None else "a203_root", cert=cd["cert"], run=cd["run"],
                                     camp=cd["camp"], anc_label=cd["anc_label"], anc_steps=cd["anc_steps"],
                                     snapshot_round=cd.get("snapshot_round"), n_replayed=len(cd.get("steps") or []),
                                     n_steps=sn["n_steps"], climbed=len(tried), refused=tried, n_cands=len(cands),
                                     rule="Lemma INHERIT (notes/coarse_tree.md s.4): a prefix of the path key, loaded "
                                          "with the pieces padded outward, then the remaining certified branch steps "
                                          "replayed -- a superset of the start node"),
                    dead_on_replay=pg.dead)
        return pg, meta
    raise err
