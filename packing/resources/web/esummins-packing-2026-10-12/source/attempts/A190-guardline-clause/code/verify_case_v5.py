#!/usr/bin/env python3
"""
verify_case_v5.py -- A190.  A185's verify_case_v4 (windows clause, Theorem W; sha b36acb01...) PLUS ONE new clause:
the GUARD LINES (`hypotheses.guardlines`, A144 notes/spec.md sec. 3-4; docs/proofs/guardline_clause.md Theorem G).

v1 (sha 521cb01f...), v3 (f578a8c9...) AND v4 ARE FROZEN AND UNTOUCHED: all three are IMPORTED (shas asserted),
never copied.  On a certificate with no `guardlines` field the behaviour is v4's = v3's = v1's byte-for-byte
(A190 regression: identical verdicts and box-tree statistics on 100 v1 certificates and on every A185 v4 one).

WHAT IS NEW (Theorem G).  The measure is mu = SUM_k w_k delta_{p_k} + SUM_l z_l H^1|_l (atoms plus a density z_l
on each declared axis-parallel line l inside the container).  A PASS certifies (V1)/(V2)/(V3) of Theorem W with
THIS mu -- the box walk lower-bounds mu(Q) on a (t, c)-box by atom mass + SUM_l z_l * minchord(box, l) (G3), the
same exact five-point primitive on the verifier's own sub-box -- and (V4') the total
    SUM_k w_k + SUM_l z_l * min(rhs_l, rhs*_l)  <  b4 = n - m + r_c ,
where rhs*_l = s - SUM_{j unattached core, chord_lo > 0} chord_lo(j, l) is RE-DERIVED (G1) from the certificate's
own cores (and their optional rational `pbox`, bound to the core by A135's `point_in_all_poses` on its corners),
the contributing cores provably in pairwise distinct, non-window squares (HARD REJECT otherwise).  Bridge: the
counted squares (window squares + free squares) have chords summing to <= s minus the uncounted squares' chords
(Lemma LINE-1), so SUM_counted mu(Q) <= SUM w + SUM z rhs* < b4 <= #counted, contradiction.  A windowed square's
chord enters ONLY through (G3) on its window walk (it is counted); an unattached core's square enters ONLY through
rhs* (it is uncounted); an attached core's square is counted by its window and enters rhs* not at all.

USAGE  python verify_case_v5.py CERT.json [--depth D] [--jobs J] [--split k] [--report [path]] [--replay] [--quiet]
       [--max-witnesses K] [--max-witnesses-per-box k] [--strict-margin m] [--scale-weights r] [--n N]
exit 0 = PASS, 1 = FAIL, 2 = malformed / total >= budget / a guard line whose rhs or distinctness does not re-derive.
"""
import argparse
import hashlib
import json
import os
import sys
import time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ATT = os.path.abspath(os.path.join(HERE, "..", ".."))
V4_DIR = os.path.join(ATT, "A185-boxed-windows-clause", "code")
V4_SHA = "b36acb012f42998cf854a0fc3b55d90732485fe905b9ae2d9deb429db7409e9d"
for _p in (V4_DIR, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
assert hashlib.sha256(open(os.path.join(V4_DIR, "verify_case_v4.py"), "rb").read()).hexdigest() == V4_SHA, \
    "A185 verify_case_v4.py is NOT the frozen one"
import verify_case_v4 as v4                                     # noqa: E402  FROZEN v4 (asserts v1, v3 shas)
import guardlines_v5 as GL                                      # noqa: E402  the exact primitives
vc, v3 = v4.vc, v4.v3
ONE, ZERO, HALF = F(1), F(0), F(1, 2)


# ===================================================================== loader
def _pbox(j, d):
    b = d.get("pbox")
    if not b:
        return None
    x0, x1, y0, y1 = (vc._rat(b[k]) for k in ("x0", "x1", "y0", "y1"))
    t0, t1 = vc._rat(b["t0"]), vc._rat(b["t1"])
    if not (x0 <= x1 and y0 <= y1 and 0 <= t0 <= t1 <= 1):
        raise ValueError("core %d: malformed pbox" % j)
    return (x0, x1, y0, y1, t0, t1)


def load_certificate_v5(path, n_override=None):
    d, s, n, atoms, weights, total = v3.load_certificate_v3(path, n_override)
    hyp = d.get("hypotheses") or {}
    raw = hyp.get("windows") or []
    wins = [v4.WindowH(i, e, d["_cores"], d["_polycores"]) for i, e in enumerate(raw)]
    att = [w.core for w in wins if w.core is not None]
    if len(set(att)) != len(att):
        raise ValueError("windows: core attachment is not injective")
    m, r, rc = len(d["_cores"]), len(wins), len(att)
    d["_windows"], d["_attached"] = wins, set(att)
    d["_budget4"] = n - m + rc
    d["_free"] = n - r - (m - rc)
    # ---- guard lines: the cores' pose boxes (bound to the cores), then every rhs re-derived
    pboxes = [_pbox(j, cj) for j, cj in enumerate(hyp.get("cores") or [])]
    for j, (k, pb) in enumerate(zip(d["_cores"], pboxes)):
        if pb is None:
            continue
        for (vx, vy) in GL.core_corners(k):
            if not v3.point_in_all_poses(vx, vy, *pb):
                raise ValueError("core %d is NOT inside every pose of its declared pbox" % j)
    lines = [GL.GuardLineH(i, e, s, vc._rat) for i, e in enumerate(hyp.get("guardlines") or [])]
    GL.rederive(lines, d["_cores"], pboxes, wins, d["_attached"], s)
    d["_pboxes"], d["_lines"] = pboxes, lines
    d["_line_total"] = sum((L.z * L.rhs_eff for L in lines), ZERO)
    return d, s, n, atoms, weights, total


# ===================================================================== the verifier: (G3) in `covered`
class VerifierV5(v3.VerifierV3):
    """v3's verifier (v1's tree, `covered`, witnesses; v3's exemption) with the line mass added to every box's
    lower bound.  `covered` is the FROZEN one: it is called with NEED lowered by floor(line_mass * WD), which is
    exactly `atom_mass + line_mass >= need` in v1's integer scale (conservative floor)."""

    def __init__(self, *args, lines=(), **kw):
        super().__init__(*args, **kw)
        self.lines = [L for L in lines if L.z > 0]
        self.NEED0, self.fneed0 = self.NEED, self.fneed
        self.n_line_boxes = self.n_line_only = 0

    def reset_stats(self):
        super().reset_stats()
        self.n_line_boxes = self.n_line_only = 0

    def line_mass(self, T0, T1, X0, X1, Y0, Y1):
        r, D = self.T_ROOT, self.D
        t0, t1 = F(T0, r), F(T1, r)
        x0, x1, y0, y1 = F(X0, D), F(X1, D), F(Y0, D), F(Y1, D)
        return sum((L.z * L.minchord(t0, t1, x0, x1, y0, y1) for L in self.lines), ZERO)

    def covered(self, T0, T1, X0, X1, Y0, Y1, known, kmass):
        if not self.lines:
            return super().covered(T0, T1, X0, X1, Y0, Y1, known, kmass)
        Lm = self.line_mass(T0, T1, X0, X1, Y0, Y1)
        if Lm <= 0:
            return super().covered(T0, T1, X0, X1, Y0, Y1, known, kmass)
        self.n_line_boxes += 1
        LI = (Lm.numerator * self.WD) // Lm.denominator             # floor(Lm * WD) <= Lm * WD
        if LI >= self.NEED0:
            self.n_line_only += 1
            return True, None, None
        if kmass + LI >= self.NEED0:
            # the atoms already certified for a parent box plus the (larger) line mass of this sub-box suffice;
            # the frozen loop compares with NEED only after adding a NEW atom, so this case is decided here
            return True, None, None
        self.NEED, self.fneed = self.NEED0 - LI, self.fneed0 - float(Lm)
        try:
            return super().covered(T0, T1, X0, X1, Y0, Y1, known, kmass)
        finally:
            self.NEED, self.fneed = self.NEED0, self.fneed0

    def exact_mass_at(self, t, cx, cy):
        m = super().exact_mass_at(t, cx, cy)
        for L in self.lines:
            m += L.z * GL.chord_at(HALF, t, abs(L.off - (cy if L.orient == "h" else cx)))
        return m

    def stats(self):
        st = super().stats()
        st["line_boxes"] = self.n_line_boxes
        st["line_only_covers"] = self.n_line_only
        return st


def make_verifier(kind, idx, P):
    cores, pcs = P["cores"], P["polycores"]
    if kind == "win":
        w = P["windows"][idx]
        keep = set(k for k in P["attached"] if k != w.core)
        cores = [c for k, c in enumerate(P["cores"]) if k in keep]
        pcs = [p for p in P["polycores"] if p.core in keep]
    return VerifierV5(P["s"], P["atoms"], P["weights"], margin=P["margin"], depth=P["depth"], tscale=P["tscale"],
                      use_float=P["use_float"], max_witnesses=P["max_w"], verbose=False, cores=cores,
                      nofams=P["nofams"], polycores=pcs, use_float_poly=P["use_float"], lines=P["lines"])


_G = {}


def _worker_init(P):
    _G["P"], _G["v"] = P, {}


def _worker(task):
    kind, idx, box = task
    P = _G["P"]
    v = _G["v"].get((kind, idx))
    if v is None:
        v = _G["v"][(kind, idx)] = make_verifier(kind, idx, P)
    v.reset_stats()
    v.run([box], per_box_cap=P["cap"])
    for w in v.witnesses:
        w["clause"] = kind if kind == "free" else "window:%s" % P["windows"][idx].name
    return kind, v.stats(), v.witnesses


# ===================================================================== driver (v4's flow, v5's loader/verifier)
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cert", nargs="?")
    for nm, kw in (("--depth", dict(type=int, default=48)), ("--strict-margin", dict(type=str, default="0")),
                   ("--report", dict(nargs="?", const="__auto__", default=None)), ("--witness-file", dict(default=None)),
                   ("--max-witnesses", dict(type=int, default=200)), ("--max-witnesses-per-box", dict(type=int, default=8)),
                   ("--jobs", dict(type=int, default=1)), ("--split", dict(type=int, default=3)),
                   ("--scale-weights", dict(type=str, default="1")), ("--tscale", dict(type=str, default="2")),
                   ("--no-float-prepass", dict(action="store_true")), ("--replay", dict(action="store_true")),
                   ("--n", dict(type=int, default=None)), ("--quiet", dict(action="store_true"))):
        ap.add_argument(nm, **kw)
    a = ap.parse_args(argv)
    if not a.cert:
        ap.error("certificate path required")
    if a.replay:
        a.no_float_prepass, a.jobs = True, 1
    t_start = time.time()
    try:
        d, s, n, atoms, weights, total = load_certificate_v5(a.cert, a.n)
    except Exception as e:                                      # noqa: BLE001
        print(f"MALFORMED certificate: {e}")
        return 2
    margin, scale = F(a.strict_margin), F(a.scale_weights)
    lines = d["_lines"]
    if scale != 1:
        weights = [w * scale for w in weights]
        total = sum(weights, ZERO)
        for L in lines:
            L.z = L.z * scale
    line_total = sum((L.z * L.rhs_eff for L in lines), ZERO)
    total5 = total + line_total
    cores, nofams, pcs, wins = d["_cores"], d["_nofams"], d["_polycores"], d["_windows"]
    budget, free = d["_budget4"], d["_free"]
    print(f"certificate: {a.cert}")
    print(f"s = {s} (~{float(s):.10f}), n = {n}, atoms = {len(atoms)}, atom mass = {total} (~{float(total):.10f}), "
          f"guard lines = {len(lines)} (line part {float(line_total):.10f}), total = {float(total5):.10f}, margin = {margin}")
    for L in lines:
        print(f"  guard line {L.idx}: {L.orient} = {float(L.off):.6f}  z = {float(L.z):.6f}  rhs declared {float(L.rhs):.6f}"
              f"  rhs* {float(L.rhs_star):.6f} (terms {[(j, round(float(c), 6)) for j, c in L.terms]})  uses {float(L.rhs_eff):.6f}")
    print(f"hypotheses: {len(cores)} cores ({sum(1 for p in d['_pboxes'] if p)} with pbox), {len(nofams)} NO-families, "
          f"{len(pcs)} polycores, {len(wins)} windows ({len(d['_attached'])} attached; (V3) re-derived), v1 budget = "
          f"{d['_budget']}, v4 budget = {budget}, free squares >= {free}" + ("  [REPLAY]" if a.replay else ""))
    if total5 >= budget:
        print(f"FAIL: total mass {float(total5):.6f} >= budget = {budget}: certificate proves nothing")
        return 2
    if s < 1:
        print("s < 1: no unit square fits; vacuous PASS")
        return 0
    use_float = not a.no_float_prepass
    P = dict(s=s, atoms=atoms, weights=weights, margin=margin, depth=a.depth, tscale=F(a.tscale), use_float=use_float,
             max_w=a.max_witnesses, cores=cores, nofams=nofams, polycores=pcs, windows=wins, attached=d["_attached"],
             cap=a.max_witnesses_per_box, lines=lines)
    v0 = make_verifier("free", -1, P)
    tasks = []
    for w in wins:
        tasks += [("win", w.idx, b) for b in v4.window_boxes(v0, w)]
    if free > 0:
        tasks += [("free", -1, b) for b in v0.root_boxes(a.split)]
    stats, witnesses = {"free": {}, "win": {}}, []
    if a.jobs > 1:
        import multiprocessing as mp
        with mp.Pool(a.jobs, initializer=_worker_init, initargs=(P,)) as pool:
            for kind, st, ws in pool.imap_unordered(_worker, tasks):
                vc.merge_stats(stats[kind], st)
                witnesses.extend(ws)
                if len(witnesses) >= a.max_witnesses:
                    pool.terminate()
                    break
    else:
        groups = [("win", w, [b for k, i, b in tasks if k == "win" and i == w.idx]) for w in wins]
        if free > 0:
            groups.append(("free", v0, [b for k, i, b in tasks if k == "free"]))
        for kind, obj, boxes in groups:
            v = obj if kind == "free" else make_verifier("win", obj.idx, P)
            v.max_witnesses = max(1, a.max_witnesses - len(witnesses))
            v.run(boxes, per_box_cap=a.max_witnesses_per_box)
            for wt in v.witnesses:
                wt["clause"] = kind if kind == "free" else "window:%s" % obj.name
            vc.merge_stats(stats[kind], v.stats())
            witnesses.extend(v.witnesses)
            if len(witnesses) >= a.max_witnesses:
                break
    elapsed = time.time() - t_start
    passed = len(witnesses) == 0
    for kind, tag in (("win", "window clause"), ("free", "free clause")):
        st = stats[kind]
        if not st:
            why = ("no windows" if kind == "win" else "no free squares") if (
                (kind == "win" and not wins) or (kind == "free" and free <= 0)) else "not reached: witness cap hit earlier"
            print(f"{tag}: skipped ({why})")
            continue
        print(f"{tag}: boxes = {st['boxes']}  covered = {st['covered']}  vacuous = {st['vacuous']}  exempt = {st.get('exempt', 0)} "
              f"(core {st.get('exempt_core', 0)}, nofam {st.get('exempt_nofam', 0)}, poly {st.get('exempt_poly', 0)})  split = "
              f"{st['split']}  exact atom checks = {st['exact_atom_checks']}  line boxes = {st.get('line_boxes', 0)} "
              f"(line-only covers {st.get('line_only_covers', 0)})  max depth = {st['max_depth']}")
    print(f"time = {elapsed:.1f}s")
    if passed:
        print(f"PASS: with mu = atoms + {len(lines)} guard-line densities, (V1) every NON-EXEMPT admissible closed unit square in "
              f"[0,{s}]^2 and (V2) every non-exempt_i pose of each of the {len(wins)} windows has mass >= {ONE + margin}; total "
              f"{total5} < v4 budget {budget}  ==>  no packing of {n} unit squares in side <= {s} satisfies the hypotheses "
              f"(node DEAD under v5 [C under v5 ONLY; the frozen v1 chain and A185's v4 are untouched])")
    else:
        holes = [w for w in witnesses if w.get("kind") == "hole"]
        byc = {}
        for w in witnesses:
            byc[w.get("clause")] = byc.get(w.get("clause"), 0) + 1
        print(f"FAIL: {len(witnesses)} witness boxes at depth {a.depth} ({len(holes)} HOLES) by clause: {byc}")
        pick = min(witnesses, key=lambda w: w.get("float_mass", 9e9))
        if pick.get("placement"):
            p = pick["placement"]
            print(f"  worst witness [{pick.get('clause')}]: theta = {p['theta_deg']:.6f} deg, centre = "
                  f"({p['cx_float']:.9f}, {p['cy_float']:.9f}), exact mass = {pick['exact_mass']}")
        wf = a.witness_file or (os.path.splitext(a.cert)[0] + ".witnesses.json")
        with open(wf, "w") as fh:
            json.dump({"cert": a.cert, "s": str(s), "depth": a.depth, "margin": str(margin), "verifier": "v5",
                       "witnesses": witnesses}, fh, indent=1)
        print(f"  witnesses written to {wf}")
    if a.report is not None:
        rp = a.report if a.report != "__auto__" else os.path.splitext(a.cert)[0] + ".report.json"
        with open(rp, "w") as fh:
            json.dump({"cert": a.cert, "verifier": "verify_case_v5 (A190) over A185 verify_case_v4 sha %s..., frozen verify_case "
                                              "sha %s... and verify_case_v3 sha %s..." % (V4_SHA[:8], v4.V1_SHA[:8], v4.V3_SHA[:8]),
                       "claim_label": "[C] under v5 only", "replay": bool(a.replay), "s": str(s), "n": n, "atoms": len(atoms),
                       "total": str(total5), "total_float": float(total5), "atom_total": str(total), "line_total": str(line_total),
                       "budget_v1": d["_budget"], "budget_v4": budget, "free_squares_ge": free, "depth": a.depth, "jobs": a.jobs,
                       "split": a.split, "float_prepass": use_float, "guardlines": [L.to_json() for L in lines],
                       "windows": [w.to_json() for w in wins], "polycores": [p.to_json() for p in pcs],
                       "result": "PASS" if passed else "FAIL", "time_s": elapsed, "stats": stats,
                       "witnesses_preview": witnesses[:20]}, fh, indent=1)
        print(f"  report written to {rp}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
