"""A203 -- A202's union caps and the certificate (moved verbatim from the copy of fast30b.py at d13f7420; the
certificate carries the CSP records, the CSP letters and path "csp203")."""
import math

import fastprop as FP                                          # READ-ONLY (A198)
import quick200 as Q                                           # READ-ONLY (A200)
import rules202 as R

INF = 99
S_RAT = FP.S_RAT


def chords_of(st, pcs):
    import fast30b
    return fast30b.chords_of(st, pcs)


def union_caps(st, single):
    caps, urec = {}, {}
    for p in st.slots:
        pcs = st.alive[p]
        n_cells = len(single[p])
        rec = dict(slot=p, n_pieces=len(pcs), n_cells=n_cells)
        if not pcs:
            rec.update(cap=0, why="no surviving piece")
        elif n_cells <= 1:
            rec.update(cap=1, why="A1: 1 alive cell")
        else:
            u = Q.union_stats([(None, r) for r in {pc[1] for pc in pcs}])
            mc = chords_of(st, pcs)
            rowsum = {L: st.base_ch[L] + 2 * mc[L] for L in st.lines}
            Lb = max(st.lines, key=lambda L: rowsum[L])
            rec.update(bbox=R.fr(u["bbox"]), diam=round(math.sqrt(float(u["diam2"])), 5), linf=round(float(u["linf"]), 5),
                       chord_line="%s=%.4f" % (Lb[0], float(Lb[1])), chord_fixed=round(float(st.base_ch[Lb]), 4),
                       chord_min=round(float(mc[Lb]), 4), chord_row=round(float(rowsum[Lb]), 4))
            if u["diam2"] < 1:
                rec.update(cap=1, why="CN: union diameter %.4f < 1" % rec["diam"])
            elif u["linf"] <= FP.SQ2H_LO:
                rec.update(cap=1, why="A1-U: union l-inf %.4f < 1/sqrt2" % rec["linf"])
            elif rowsum[Lb] > S_RAT:
                rec.update(cap=1, why="CHORD-U: fixed %.4f + 2 x %.4f > s on %s" % (rec["chord_fixed"], rec["chord_min"], rec["chord_line"]))
            else:
                rec.update(cap=INF, why="no union exclusion fires")
        caps[p], urec[p] = rec["cap"], rec
        st.T.test("UNION", **rec)
    return caps, urec



def certificate(st):
    tests = [dict(test="CELL", cell=ci, rect=FP.rect_f(c["rect"])) for ci, c in enumerate(st.cells)]
    alive_rects = {}
    for k, p in enumerate(st.slots):
        for pc in st.alive[p]:
            alive_rects.setdefault(pc[2], set()).add(k)
    subrects = []
    for (ci, si), (rf, rr) in sorted(st.sub.items()):
        inside = [r for r in alive_rects if rr[0] <= r[0] and r[1] <= rr[1] and rr[2] <= r[2] and r[3] <= rr[3]]
        if inside:
            status = ""
        else:
            ws = [st.letters.get((ci, rf, b.t0)) for b in st.bins]
            ws = [w for w in ws if w]
            status = max(set(ws), key=ws.count) if len(ws) == st.nbins else st.letters_csp.get((ci, rf[1]), "R")
        subrects.append([ci, si, list(rr), status, []])
    roles = {k: FP.rect_f(v) for k, v in st.pins.items()}
    hh = st.h_hull()
    roles[st.H] = FP.rect_f(hh) if hh else FP.rect_f(st.base[st.H])
    for k, v in st.other_h.items():
        roles[k] = FP.rect_f(v)
    out = dict(nid=st.nid, cls=st.cls, pad=st.pad, lam=float(Q.PADS[st.pad]), stage=0, verdict="DEAD" if st.verdict_leaf else "ALIVE",
               leaf=st.verdict_leaf, step_killed=("stage0" if st.verdict_leaf else None), rounds=st.rounds, forced_H=sorted(st.forced_H),
               roles=roles, H_record=FP.rect_f(st.base[st.H]), H_hull_raw=(list(hh) if hh else None), role_slots={}, role_cells={},
               witness=[(who, o[0], sorted(o[1]), FP.rect_f(o[3])) for who, o in (getattr(st, "witness", None) or [])],
               caps={p: (None if c >= INF else c) for p, c in getattr(st, "caps_last", {}).items()},
               kills={k: dict(kills=v["kills"], ms=round(v["ms"], 1)) for k, v in st.kills.items()},
               seconds=round(st.T.now(), 3), steps=st.T.steps, tests=tests + st.T.tests, subrects=subrects,
               alive_rects=[[list(r), sorted(v)] for r, v in alive_rects.items()],
               slots=st.slots, wbox={p: list(v) for p, v in st.wbox.items()}, n_pieces=len(st.coarse), n_bins=st.nbins, nsub=st.nsub,
               depth=st.depth, n_alive={p: len(v) for p, v in st.alive.items()}, n_hpieces=len(st.hpieces),
               window_pending=(st.pad == "zero") and bool(st.verdict_leaf), path="csp203",
               verifier="[C: closed-form trace] -- no verifier clause exists yet",
               csp=st.csp, ud=st.ud, sat_step=st.sat_step,
               row=dict(family=st.row.get("family"), camp=st.row.get("camp"), tau=st.row.get("tau")),
               record=(st.row.get("record") or "").replace(chr(92), "/"))
    try:
        out["prior_tau"] = float(st.row.get("tau"))
    except (TypeError, ValueError):
        out["prior_tau"] = None
    if out["window_pending"]:
        out["leaf"] += " [pad 0: s0-only, WINDOW-PENDING]"
    return out
