"""A211 -- leaf rule (a): rule CC (A210's Lemma CORNER-COVER, notes/corner_cover.md; the copy cc210.py / leaves210.py)
applied to the LIVE fully named node of the coarse tree instead of to a certificate: for every corner slot p and every
non-pin role near that corner, CC1's band of each of the role's pose classes (the node's CURRENT pieces -- coarse
units at an internal node, which only over-state the slack: CC'(a), sound) and CC'(b) on every candidate second
meeter (the alive anonymous cells of p's option table, the other roles' hull boxes).  DEAD when a role the node
hypothesises at p cannot reach the band, or when every pose class of the pushed-in role leaves no second meeter.
The option table must be FRESH (a round with no instantiation: Lemma CT's proviso) -- the tree calls this only at
a node where `candidates()` returned None.  Verdicts [C: closed-form trace; Lemma CORNER-COVER], no verifier clause."""
import math
import os
import sys

import cc210 as CC
import leaves210 as L10
import poly204 as P

FP = P.FP
SQ2 = math.sqrt(2.0)


def node_rows(nid, pad, lam, s, cells, slots, node):
    """leaves210.node_rows with the container side `s` of the page (S0 on a gallery page; a tree record's own)."""
    roles = {k: v for k, v in (node.get("roles") or {}).items() if not k.startswith("P")}
    rslots = node.get("role_slots") or {}
    alive = node.get("alive_cells") or {}
    out = []
    for p in slots:
        if not L10.is_corner_slot(p):
            continue
        corner = L10.corner_of(p)
        for name, box in sorted(roles.items()):
            bands = CC.piece_bands(L10.role_pieces(node, name, box), corner, s, lam)
            if not bands:
                continue
            near = [(k, ws) for k, ws in bands if k[2] <= CC.NEAR and k[3] <= CC.NEAR]
            if not near or p not in alive:
                continue
            all_near = len(near) == len(bands)
            allb = [w for _, ws in bands for w in ws]
            cand_cells = {int(ci): tuple(float(v) for v in cells[int(ci)]) for ci in (alive.get(p) or [])}
            others = {k: (tuple(float(v) for v in b[:4]), L10.wmax_of(b)) for k, b in roles.items() if k != name}
            dead_cells = [ci for ci, r in cand_cells.items() if not CC.reaches(r, SQ2, allb, lam)] if all_near else []
            dead_roles = [k for k, (r, w) in others.items() if not CC.reaches(r, w, allb, lam)] if all_near else []
            dead_classes = []
            for k, ws in near:
                if any(CC.reaches(r, SQ2, ws, lam) for r in cand_cells.values()) or any(CC.reaches(r, w, ws, lam) for r, w in others.values()):
                    continue
                dead_classes.append(k)
            named_at_p = [r for r in rslots if p in (rslots.get(r) or []) and r != name]
            contra = [r for r in named_at_p if r in dead_roles]
            verdict, why = "ALIVE", None
            if contra:
                verdict = "DEAD"
                why = ("rule CC: %s is a corner square at %s (Lemma CORNER-COVER), so every other meeter of %s has an interior point in the "
                       "wall wedges; the node's hypothesised meeter(s) %s cannot reach them" % (name, corner, p, contra))
            elif all_near and len(dead_classes) == len(near):
                verdict = "DEAD"
                why = ("rule CC: every pose class of %s at the %s corner (%d of %d) covers the slot cell except the wall wedges, and no "
                       "second non-pin meeter of %s can reach them (%d anonymous cell(s), %d other role(s) excluded) -- Theorem FC demands 2"
                       % (name, corner, len(dead_classes), len(bands), p, len(dead_cells), len(dead_roles)))
            out.append(dict(nid=nid, pad=pad, lam=lam, label=node.get("label"), slot=p, corner=corner, role=name, all_near=all_near,
                            role_box=[round(float(v), 6) for v in box], n_classes=len(bands), n_near=len(near), dead_classes=len(dead_classes),
                            n_band=len(allb), band=[[round(v, 6) for v in w] for w in allb[:24]], cells_before=sorted(cand_cells),
                            cells_killed=sorted(dead_cells), cells_left=sorted(set(cand_cells) - set(dead_cells)), roles_excluded=sorted(dead_roles),
                            named_meeters=sorted(named_at_p), verdict=verdict, why=why,
                            verifier="[C: closed-form trace; Lemma CORNER-COVER (attempts/A210-corner-cover/notes/corner_cover.md)] -- no verifier clause"))
    return out


def live_node(pg, label):
    """the node dict rule CC reads, from the live page: hull boxes, role slots (H's = forced_H), the FRESH option
    table's alive cells per slot, and every role's current pieces as the pose classes."""
    single = (pg.rounds[-1].get("single") or {}) if pg.rounds else {}
    rs = {k: list(v) for k, v in pg.role_slots.items()}
    rs[pg.H] = sorted(pg.forced_H)
    snap = {k: dict(pieces=[P.piece6(b, r) for b, r in (pg.pieces.get(k) or [])]) for k in pg.roles if not k.startswith("P")}
    return dict(label=label, roles={k: [float(v) for v in b] for k, b in pg.roles.items()}, role_slots=rs,
                alive_cells={p: sorted(int(c) for c in single.get(p, {})) for p in pg.slots}, snapshot=dict(roles=snap))


def snap_eval(pg, label, log=None):
    """A224 leaf rule (0), Rule SNAP -- the entry point beside cc_rows (the logic is attempts/A224-snap-rule/code/
    snap224.py, which wraps A161 / A178 read-only).  Returns None when the flag A224_SNAP is off or the rule makes no
    claim; otherwise a record with verdict DEAD (SNAP / SNAP-DIAG), HANDOFF, or None.  Unlike rule CC this does NOT
    need a fresh option table: its hypothesis is the roles' own pose sets, not the anonymous rows."""
    import snap224 as S224                                      # A224 (flag-gated; import is cheap and pure)
    if not S224.ON:
        return None
    r = S224.evaluate(pg, label, log=log)
    if r is not None:
        pg.T.test("SNAP-ROWS", label=label, n_cands=r.get("n_cands"), n_anon=r.get("n_anon"),
                  cands=r.get("cands"), verdict=r.get("verdict"))
    return r


EPS_ON = (os.environ.get("A230_EPS") or os.environ.get("A227_EPS") or "").strip().lower() in ("1", "on", "yes")
EPS_WEDGE_CAP = int(os.environ.get("A230_WEDGE_CAP") or 1)     # NS-at-wedge splits of ONE (slot, role) pair along a path


def eps_eval(pg, label, log=None, skip=None):
    """A230 leaf rule (0'), Rule EPS -- beside snap_eval (the logic is attempts/A230-eps-branch/code/epsns230.py +
    eps230.py, which wrap A227 / A224 / A161 / A171 read-only; docs/proofs/lemma_eps.md).  None when the flag
    A230_EPS (or A227_EPS) is off or no role is near-simple at a forced cell; otherwise a record with verdict DEAD
    (FC+EPS: the cell is left with fewer than two possible non-pin meeters) or None with the survivors, the wedge
    targets they reach and -- when exactly one survives -- the NS-at-wedge split `wedge_ns`.  Like SNAP it does not
    need a fresh option table for the NAMED roles; the anonymous clause uses the fresh row exactly as rule CC does."""
    if not EPS_ON:
        return None
    r = _e230().evaluate(pg, label, log=log, skip=skip)                     # A230 (flag-gated; the import is cheap and pure)
    if r is not None:
        pg.T.test("EPS-ROWS", label=label, n_cands=r.get("n_cands"), n_added=r.get("n_added"),
                  n_anon=r.get("n_anon"), verdict=r.get("verdict"), wedge_ns=bool(r.get("wedge_ns")))
    return r


def _e230():
    root = os.path.dirname(os.path.abspath(__file__))
    while root and os.path.basename(root) != "attempts":
        root = os.path.dirname(root)
    for d in (os.path.join(root, "A227-lemma-eps", "code"), os.path.join(root, "A230-eps-branch", "code")):
        if d not in sys.path:
            sys.path.insert(0, d)
    import epsns230
    return epsns230


def eps_branches(w):
    """the two children of the NS-at-wedge split (A230): "M meets W" / "M misses W", exhaustive by Theorem FC + EPS."""
    return _e230().branches(w)


def eps_apply(pg, br):
    """the MEETS child: M's pieces clipped to the poses that reach W (exact; ValueError when nothing is left)."""
    return _e230().apply_wedge(pg, br)


def cc_rows(pg, label):
    if not pg.rounds or pg.rounds[-1].get("instantiated"):
        return []                                                # not a fresh table: no claim (Lemma CT's proviso)
    cells = [FP.rect_f(c["rect"]) for c in pg.cells]
    lam = 1.0 if pg.pad == "zero" else float(pg.lam)
    rows = node_rows(pg.name, pg.pad, lam, float(pg.s), cells, list(pg.slots), live_node(pg, label))
    for r in rows:
        pg.T.test("CC", label=label, slot=r["slot"], role=r["role"], verdict=r["verdict"], all_near=r["all_near"], n_near=r["n_near"],
                  dead_classes=r["dead_classes"], cells_killed=r["cells_killed"], roles_excluded=r["roles_excluded"])
    return rows
