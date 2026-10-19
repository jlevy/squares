"""A202 -- STAGE 1: A200's exact option table (quick200.QPage: A171 dead test / A161 miss per cell x slot, the union
caps, Theorem FC, the count, the forcing, multibox re-normalisation) run on the cells STAGE 0 left alive only, with
stage 0's clipped H box.  Sound: stage 0 proved that no free meeter of slot p has its centre in a dead cell (every
piece of the cell fails a necessary condition), so Reach(cell, S) is empty for every S containing p; H's clipped box
is the hull of the poses that may meet the slots H was proved forced at.  Stops after the propagation (stages 2-3,
SEAL / pair test / LP, are A200's and A201's)."""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for _p in (os.path.join(ROOT, "attempts", "A198-fastprop", "code"), os.path.join(ROOT, "attempts", "A200-k516-quick", "code")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import fastprop as FP                                          # noqa: E402  READ-ONLY (A198)
import quick200 as Q                                           # noqa: E402  READ-ONLY (A200)


class Stage1(Q.QPage):
    def __init__(self, rec, cls, name, trace, alive0, hbox0, **kw):
        rec = dict(rec)
        rec["H"] = [tuple(hbox0)] + list(rec["H"][1:])
        super().__init__(rec, cls, name, trace, **kw)
        self.alive0 = {p: set(int(c) for c in v) for p, v in alive0.items()}
        self.skipped = 0

    def reach(self, ci, S):
        for p in S:
            if ci not in self.alive0.get(p, ()):
                key = (ci, S)
                if key not in self.reach_cache:
                    self.reach_cache[key] = (0.0, [], 0)
                    self.skipped += 1
                    if self.skipped <= 400:
                        self.T.test("REACH-SKIP", cell=ci, slots=sorted(S), why="stage 0 killed cell %d for %s" % (ci, p))
                return self.reach_cache[key]
        return super().reach(ci, S)


def run_stage1(nid, pad, alive0, hbox0, wall=600, depth=5, joint_depth=2, refine_union=2, log=print):
    T = FP.Trace(wall=wall)
    rec, cls, row = FP.load_page(nid)
    log("== stage 1 %s (%s) at the %s pad: H box %s (record %s); alive cells %s" % (
        nid, cls, pad, [round(v, 4) for v in hbox0], [round(v, 4) for v in rec["H"][0]], {p: len(v) for p, v in alive0.items()}))
    pg = Stage1(rec, cls, nid, T, alive0, hbox0, depth=depth, joint_depth=joint_depth, refine_union=refine_union, pad=pad)
    out = pg.run()
    for rd in out["rounds"]:
        log("   round %d: alive cells %s; caps %s; H reaches %s; forced_H %s; instantiate %s; count %s / chords %s%s" % (
            rd["round"], {p: len(v) for p, v in rd["single"].items()}, rd.get("caps"), rd.get("H_reach"), rd.get("forced_H"),
            rd.get("instantiate"), (rd.get("count_nochord") or {}).get("feasible"), (rd.get("count_chord") or {}).get("feasible"),
            ("; DEAD: " + rd["dead"]) if rd.get("dead") else ""))
    out["stage"] = 1
    out["step_killed"] = "stage1-propagation" if out["verdict"] == "DEAD" else None
    out["pad"] = pad
    out["lam"] = float(Q.PADS[pad])
    out["window_pending"] = (pad == "zero") and out["verdict"] == "DEAD"
    if out["window_pending"]:
        out["leaf"] = (out["leaf"] or "") + " [pad 0: s0-only, WINDOW-PENDING]"
    out["path"] = "fast30-s1"
    out["verifier"] = "[C: exact-test trace (A171 dead test / A161 miss / Lemma CN / A1 / chord rows / Theorem FC) on stage 0's alive cells]"
    out["n_reach_skipped"] = pg.skipped
    out["alive0"] = {p: sorted(v) for p, v in pg.alive0.items()}
    out["H_stage0"] = list(hbox0)
    out["tests"] = T.tests
    out["steps"] = T.steps
    out["seconds"] = round(T.now(), 1)
    out["row"] = dict(family=row.get("family"), camp=row.get("camp"), tau=row.get("tau"))
    out["record"] = (row.get("record") or "").replace(chr(92), "/")
    try:
        out["prior_tau"] = float(row.get("tau"))
    except (TypeError, ValueError):
        out["prior_tau"] = None
    log("   => stage 1 %s in %.1f s (%d exact tests, %d reach tests skipped)%s" % (out["verdict"], out["seconds"], len(T.tests), pg.skipped, ("; " + out["leaf"]) if out["leaf"] else ""))
    return out, pg
