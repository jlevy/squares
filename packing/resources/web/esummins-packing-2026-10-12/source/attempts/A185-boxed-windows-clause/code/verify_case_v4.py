#!/usr/bin/env python3
"""
verify_case_v4.py -- A185.  The frozen case verifier v1 (`attempts/A57-shadow-trees/code/verify_case.py`,
sha 521cb01f...) PLUS A135's polygon-core clause (`verify_case_v3.py`, sha f578a8c9...) PLUS ONE new clause:
the per-square POSE WINDOW (`hypotheses.windows`), Theorem W of `docs/proofs/boxed_windows.md`.

v1 AND v3 ARE FROZEN AND UNTOUCHED: both are IMPORTED (shas asserted at import), never copied.  On a
certificate with no `windows` field the behaviour is v3's = v1's byte-for-byte (A185 regression: identical
verdict and identical box-tree statistics on 100 v1 certificates).

WHAT IS PROVED (Theorem W).  With m cores, r windows of which r_c name a core (injectively), a PASS certifies
  (V1) [free clause, run iff f = n - r - (m - r_c) > 0]  every admissible closed unit square Q that is not
       EXEMPT (v1/v3 exemption: NO-family, meets a core or a polygon core) has mu(Q) >= 1 + margin;
  (V2) [window clause]  for every window i, every admissible Q whose pose lies in a piece of W_i and that is
       not EXEMPT_i (NO-family, or meets a core ATTACHED TO ANOTHER window, or a polygon core refining one)
       has mu(Q) >= 1 + margin;
  (V3) [re-derived, HARD REJECT otherwise]  the four corners of cores[kappa(i)] (and every vertex of every
       polygon core refining it) lie in EVERY pose of EVERY piece of window i  (A135 `point_in_all_poses`);
  (V4) total < b4 = n - m + r_c.
Then no packing satisfies the node hypothesis (an injective assignment of windows to packed squares, every
unattached core inside some square, no square in a NO-family) -- the node is DEAD [C under v4 ONLY].

The window walk is v1's own tree: each piece, rounded OUTWARD to the integer grid (a superset), is clipped to
the admissible region, tested for exemption with the reduced core list, covered or bisected to --depth.  This
is CHEAPER than the container walk: the pieces are small.

Guard lines (A144 `notes/spec.md` sec. 4): NOT implemented here -- a certificate carrying `guardlines` is
refused (exit 2) with the pointer; A144's `guardline.minchord_box` exists, the emitters do not emit the field.

USAGE  python verify_case_v4.py CERT.json [--depth D] [--jobs J] [--split k] [--report [path]] [--replay]
       [--quiet] [--max-witnesses K] [--max-witnesses-per-box k] [--strict-margin m] [--scale-weights r] [--n N]
exit 0 = PASS, 1 = FAIL, 2 = malformed / total >= budget / guardlines present.
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ATT = os.path.abspath(os.path.join(HERE, "..", ".."))
V1_DIR = os.path.join(ATT, "A57-shadow-trees", "code")
V3_DIR = os.path.join(ATT, "A135-polycore-verifier", "code")
V1_SHA = "521cb01fe656707cf134864b75227c6051d43a97253749f50ecd1eb37cbef7af"
V3_SHA = "f578a8c9346c17f1050445725b2e8af95ad9d344f8f281a42e2fbd84782f7a1e"


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


for _p in (V3_DIR, V1_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
assert _sha(os.path.join(V1_DIR, "verify_case.py")) == V1_SHA, "frozen v1 verify_case.py is NOT the frozen one"
assert _sha(os.path.join(V3_DIR, "verify_case_v3.py")) == V3_SHA, "A135 verify_case_v3.py is NOT the frozen one"
import verify_case as vc                                        # noqa: E402  FROZEN v1 (imported)
import verify_case_v3 as v3                                     # noqa: E402  FROZEN v3 (imported)

ONE, ZERO = F(1), F(0)


# ===================================================================== the window hypothesis
class WindowH:
    """One `windows` entry, CERTIFIED at construction ((V3) for its attached core and polygon cores)."""

    def __init__(self, i, d, cores, polycores):
        self.idx = i
        self.name = str(d.get("name", "w%d" % i))
        self.core = None if d.get("core") is None else int(d["core"])
        self.pieces = []
        for p in d["pieces"]:
            x0, x1 = vc._rat(p["x0"]), vc._rat(p["x1"])
            y0, y1 = vc._rat(p["y0"]), vc._rat(p["y1"])
            t0, t1 = vc._rat(p["t0"]), vc._rat(p["t1"])
            if not (x0 <= x1 and y0 <= y1 and 0 <= t0 <= t1 <= 1):
                raise ValueError("window %s: malformed piece" % self.name)
            self.pieces.append((x0, x1, y0, y1, t0, t1))
        if not (1 <= len(self.pieces) <= 4096):
            raise ValueError("window %s: %d pieces" % (self.name, len(self.pieces)))
        if self.core is not None:
            if not (0 <= self.core < len(cores)):
                raise ValueError("window %s: core index out of range" % self.name)
            k = cores[self.core]
            pts = []
            for i_, j_ in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
                pts.append((k.kx + k.a * (i_ * k.cm - j_ * k.sm), k.ky + k.a * (i_ * k.sm + j_ * k.cm)))
            for pc in polycores:
                if pc.core == self.core:
                    pts.extend(pc.verts)
            for (vx, vy) in pts:
                for (x0, x1, y0, y1, t0, t1) in self.pieces:
                    if not v3.point_in_all_poses(vx, vy, x0, x1, y0, y1, t0, t1):
                        raise ValueError("window %s: core %d is NOT inside every pose of the window (V3)"
                                         % (self.name, self.core))

    def to_json(self):
        return dict(name=self.name, core=self.core, pieces=len(self.pieces))


def load_certificate_v4(path, n_override=None):
    d, s, n, atoms, weights, total = v3.load_certificate_v3(path, n_override)
    hyp = d.get("hypotheses") or {}
    if hyp.get("guardlines"):
        raise ValueError("guardlines clause not implemented in v4 (A144 notes/spec.md sec. 4)")
    raw = hyp.get("windows") or []
    wins = [WindowH(i, e, d["_cores"], d["_polycores"]) for i, e in enumerate(raw)]
    att = [w.core for w in wins if w.core is not None]
    if len(set(att)) != len(att):
        raise ValueError("windows: core attachment is not injective")
    m, r, rc = len(d["_cores"]), len(wins), len(att)
    d["_windows"], d["_attached"] = wins, set(att)
    d["_budget4"] = n - m + rc
    d["_free"] = n - r - (m - rc)
    return d, s, n, atoms, weights, total


# ===================================================================== verifiers per clause
def make_verifier(kind, idx, P):
    """kind 'free': v3's verifier (all cores, all polycores).  kind 'win': cores = the cores attached to OTHER
    windows, polycores = those refining such a core; NO-families always."""
    cores, pcs = P["cores"], P["polycores"]
    if kind == "win":
        w = P["windows"][idx]
        keep = set(k for k in P["attached"] if k != w.core)
        cores = [c for k, c in enumerate(P["cores"]) if k in keep]
        pcs = [p for p in P["polycores"] if p.core in keep]
    return v3.VerifierV3(P["s"], P["atoms"], P["weights"], margin=P["margin"], depth=P["depth"],
                         tscale=P["tscale"], use_float=P["use_float"], max_witnesses=P["max_w"],
                         verbose=False, cores=cores, nofams=P["nofams"], polycores=pcs,
                         use_float_poly=P["use_float"])


def window_boxes(v, w):
    """the pieces of window w as v1 integer boxes, rounded OUTWARD (a superset), clamped to the root."""
    out = []
    r, D = v.T_ROOT, v.D
    lo, hi = D >> 1, v.SD - (D >> 1)
    for (x0, x1, y0, y1, t0, t1) in w.pieces:
        T0, T1 = max(0, math.floor(t0 * r)), min(r, math.ceil(t1 * r))
        X0, X1 = max(lo, math.floor(x0 * D)), min(hi, math.ceil(x1 * D))
        Y0, Y1 = max(lo, math.floor(y0 * D)), min(hi, math.ceil(y1 * D))
        if T0 > T1 or X0 > X1 or Y0 > Y1:
            continue                                            # no admissible centre: vacuous piece
        out.append((0, T0, T1, X0, X1, Y0, Y1, (), 0))
    return out


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


# ===================================================================== driver
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cert", nargs="?")
    ap.add_argument("--depth", type=int, default=48)
    ap.add_argument("--strict-margin", type=str, default="0")
    ap.add_argument("--report", nargs="?", const="__auto__", default=None)
    ap.add_argument("--witness-file", type=str, default=None)
    ap.add_argument("--max-witnesses", type=int, default=200)
    ap.add_argument("--max-witnesses-per-box", type=int, default=8)
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--split", type=int, default=3)
    ap.add_argument("--scale-weights", type=str, default="1")
    ap.add_argument("--tscale", type=str, default="2")
    ap.add_argument("--no-float-prepass", action="store_true")
    ap.add_argument("--replay", action="store_true")
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    if not a.cert:
        ap.error("certificate path required")
    if a.replay:
        a.no_float_prepass, a.jobs = True, 1
    t_start = time.time()
    try:
        d, s, n, atoms, weights, total = load_certificate_v4(a.cert, a.n)
    except Exception as e:                                      # noqa: BLE001
        print(f"MALFORMED certificate: {e}")
        return 2
    margin, scale = F(a.strict_margin), F(a.scale_weights)
    if scale != 1:
        weights = [w * scale for w in weights]
        total = sum(weights, ZERO)
    cores, nofams, pcs, wins = d["_cores"], d["_nofams"], d["_polycores"], d["_windows"]
    budget, free = d["_budget4"], d["_free"]
    print(f"certificate: {a.cert}")
    print(f"s = {s} (~{float(s):.10f}), n = {n}, atoms = {len(atoms)}, total mass = {total} "
          f"(~{float(total):.10f}), margin = {margin}")
    print(f"hypotheses: {len(cores)} cores, {len(nofams)} NO-families, {len(pcs)} polycores, {len(wins)} windows "
          f"({len(d['_attached'])} attached; (V3) re-derived), v1 budget = {d['_budget']}, "
          f"v4 budget = {budget}, free squares >= {free}" + ("  [REPLAY]" if a.replay else ""))
    if total >= budget:
        print(f"FAIL: total mass {float(total):.6f} >= budget = {budget}: certificate proves nothing")
        return 2
    if s < 1:
        print("s < 1: no unit square fits; vacuous PASS")
        return 0
    use_float = not a.no_float_prepass
    P = dict(s=s, atoms=atoms, weights=weights, margin=margin, depth=a.depth, tscale=F(a.tscale),
             use_float=use_float, max_w=a.max_witnesses, cores=cores, nofams=nofams, polycores=pcs,
             windows=wins, attached=d["_attached"], cap=a.max_witnesses_per_box)
    v0 = make_verifier("free", -1, P)
    tasks = []                                                   # windows FIRST (the new, cheaper clause)
    for w in wins:
        tasks += [("win", w.idx, b) for b in window_boxes(v0, w)]
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
        # one `run` call per clause instance, exactly v1/v3's single-process flow (same witness caps)
        groups = []
        for w in wins:
            groups.append(("win", w, [b for k, i, b in tasks if k == "win" and i == w.idx]))
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
        print(f"{tag}: boxes = {st['boxes']}  covered = {st['covered']}  vacuous = {st['vacuous']}  "
              f"exempt = {st.get('exempt', 0)} (core {st.get('exempt_core', 0)}, nofam {st.get('exempt_nofam', 0)}, "
              f"poly {st.get('exempt_poly', 0)})  split = {st['split']}  exact atom checks = "
              f"{st['exact_atom_checks']}  max depth = {st['max_depth']}")
    print(f"time = {elapsed:.1f}s")
    if passed:
        print(f"PASS: (V1) every NON-EXEMPT admissible closed unit square in [0,{s}]^2 and (V2) every non-exempt_i "
              f"pose of each of the {len(wins)} windows has mass >= {ONE + margin}; total {total} < v4 budget "
              f"{budget}  ==>  no packing of {n} unit squares in side <= {s} satisfies the hypotheses "
              f"(node DEAD under v4 [C under v4 ONLY; the frozen v1 chain is untouched])")
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
            json.dump({"cert": a.cert, "s": str(s), "depth": a.depth, "margin": str(margin),
                       "verifier": "v4", "witnesses": witnesses}, fh, indent=1)
        print(f"  witnesses written to {wf}")
    if a.report is not None:
        rp = a.report if a.report != "__auto__" else os.path.splitext(a.cert)[0] + ".report.json"
        with open(rp, "w") as fh:
            json.dump({"cert": a.cert, "verifier": "verify_case_v4 (A185) over frozen verify_case sha "
                                                   f"{V1_SHA[:8]}... and verify_case_v3 sha {V3_SHA[:8]}...",
                       "claim_label": "[C] under v4 only", "replay": bool(a.replay), "s": str(s), "n": n,
                       "atoms": len(atoms), "total": str(total), "total_float": float(total),
                       "budget_v1": d["_budget"], "budget_v4": budget, "free_squares_ge": free,
                       "depth": a.depth, "jobs": a.jobs, "split": a.split, "float_prepass": use_float,
                       "windows": [w.to_json() for w in wins], "polycores": [p.to_json() for p in pcs],
                       "result": "PASS" if passed else "FAIL", "time_s": elapsed, "stats": stats,
                       "witnesses_preview": witnesses[:20]}, fh, indent=1)
        print(f"  report written to {rp}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
