"""A213 differential test 1 -- REPLAY every library-level MBox.rebuild of a recorded run (results/replay_*.jsonl,
written by code/profrun213.py) through the library build and the integer-space build; assert identical vertices,
cores, k_source and k_info (and the same exception where the library raised); time both.  Then the primitives on the
same inputs: polycore.build per piece box, intersect, certify (lib / int / vec / obj), axis core.
   python tests/replay213.py results/replay_before_<nid>.jsonl [--limit N]"""
import json
import os
import sys
import time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.abspath(os.path.join(HERE, "..", "code"))
sys.path.insert(0, CODE)
os.environ["A213_INTCORE"] = "1"
import polycore_int as PI                                      # noqa: E402
import polycore_vec as PV                                      # noqa: E402
import mbpatch213 as M                                         # noqa: E402
import multibox as MB                                          # noqa: E402
import polycore as PC                                          # noqa: E402

_BINS = {}


def mkbin(a, b):
    k = (a, b)
    if k not in _BINS:
        _BINS[k] = MB.Bin(a, b)
    return _BINS[k]


def mbox_of(rec):
    mb = MB.MBox.__new__(MB.MBox)
    mb.name, mb.kmode = rec["name"], rec["kmode"]
    mb.pieces = [(mkbin(Fr(t0), Fr(t1)), tuple(Fr(x) for x in r)) for (t0, t1, r) in rec["pieces"]]
    mb.pc = mb.core = mb.obs = mb.k_source = mb._obs_cache = mb.box0 = None
    mb.k_info, mb._pcache, mb.trace = {}, {}, []
    return mb


def kwargs_of(rec):
    kw = {}
    for k, v in rec["kw"].items():
        kw[k] = None if v == "None" else (v if k == "kmode" else int(v))
    a = [int(x) for x in rec["args"]]
    return a, kw


def run_one(rec, fn):
    mb = mbox_of(rec)
    a, kw = kwargs_of(rec)
    t = time.perf_counter()
    try:
        fn(mb, *a, **kw)
    except Exception as e:                                     # noqa: BLE001
        return dict(error="%s: %s" % (type(e).__name__, e)), time.perf_counter() - t, mb
    dt = time.perf_counter() - t
    c = mb.core
    out = dict(k_source=mb.k_source, k_info={k: str(v) for k, v in mb.k_info.items()},
               verts=[[str(x), str(y)] for (x, y) in getattr(mb.pc, "verts", ())],
               core=None if c is None else [str(c.kx), str(c.ky), str(c.tm), str(c.a)])
    return out, dt, mb


def main():
    path = sys.argv[1]
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    recs = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    if limit:
        recs = recs[:limit]
    lib = MB.MBox.rebuild
    n = mism = rec_mism = 0
    tl = ti = trec = 0.0
    kinds = {}
    prim = dict(build=[0, 0.0, 0.0], inter=[0, 0.0, 0.0], cert=[0, 0.0, 0.0, 0.0, 0.0], axis=[0, 0.0, 0.0])
    for rec in recs:
        M.uninstall()
        r0, dt0, mb0 = run_one(rec, lib)
        M.install(verify=False)
        r1, dt1, _mb1 = run_one(rec, lib)
        n += 1
        tl += dt0
        ti += dt1
        kinds[rec.get("k_source", "error")] = kinds.get(rec.get("k_source", "error"), 0) + 1
        if r0 != r1:
            mism += 1
            print("MISMATCH", rec["name"], json.dumps(r0)[:300], "\n   vs", json.dumps(r1)[:300])
        recd = {k: rec.get(k) for k in ("k_source", "k_info", "verts", "core")} if "error" not in rec else dict(error=rec["error"])
        if recd != r0:
            rec_mism += 1
            print("RECORD differs from the library replay:", rec["name"], json.dumps(recd)[:200], json.dumps(r0)[:200])
        # --- the primitives on this piece set (a per-piece build, then the pieces-mode chain)
        boxes = [MB.piece_box(bn, r) for (bn, r) in mb0.pieces]
        a, kw = kwargs_of(rec)
        ng = kw.get("n_grid", a[0] if a else 97)
        polys = []
        for (pb, _t0, _t1) in boxes[:8]:
            M.uninstall()
            t = time.perf_counter()
            try:
                p0 = M.ORIG["build"](pb, n_grid=ng, max_v=16)
            except RuntimeError:
                p0 = None
            prim["build"][1] += time.perf_counter() - t
            M.install(verify=False)
            t = time.perf_counter()
            try:
                p1 = PC.build(pb, n_grid=ng, max_v=16)
            except RuntimeError:
                p1 = None
            prim["build"][2] += time.perf_counter() - t
            prim["build"][0] += 1
            assert (p0 is None) == (p1 is None) and (p0 is None or (p0.verts == p1.verts and p0.shrink == p1.shrink)), "build mismatch %r" % pb
            if p0 is not None:
                polys.append(p0.verts)
        if len(polys) >= 2:
            t = time.perf_counter()
            P0 = MB.intersect_frac(polys, max_v=16)
            prim["inter"][1] += time.perf_counter() - t
            t = time.perf_counter()
            P1 = PI.intersect_h([[PI.hom(x, y) for (x, y) in V] for V in polys], max_v=16)
            prim["inter"][2] += time.perf_counter() - t
            prim["inter"][0] += 1
            assert [(x, y) for (x, y) in P0] == [(Fr(X, W), Fr(Y, W)) for (X, Y, W) in P1], "intersect mismatch"
        # --- the hot loop: the FULL rebuild's certified polygon against EVERY piece (no early exit: all pass)
        if r0.get("k_source") == "pieces" and mb0.pc is not None and len(mb0.pc.verts) >= 3:
            V = list(mb0.pc.verts)
            M.uninstall()                                      # the library certify calls PC.vertex_ok by name
            t = time.perf_counter()
            b0 = M.ORIG["certify_verts"](V, boxes)
            prim["cert"][1] += time.perf_counter() - t
            M.install(verify=False)
            t = time.perf_counter()
            b1 = PI.certify_verts(V, boxes)
            prim["cert"][2] += time.perf_counter() - t
            t = time.perf_counter()
            b2 = PV.certify_verts(V, boxes)
            prim["cert"][3] += time.perf_counter() - t
            t = time.perf_counter()
            b3 = PV.certify_verts_obj(V, boxes)
            prim["cert"][4] += time.perf_counter() - t
            prim["cert"][0] += 1
            assert b0 == b1 == b2 == b3 == [], "certify mismatch %r %r %r %r" % (b0, b1, b2, b3)
            tm = mb0.core.tm if mb0.core is not None else Fr(1, 3)
            M.uninstall()
            t = time.perf_counter()
            c0 = M.ORIG["axis_core_pieces"](V, boxes, tm)
            prim["axis"][1] += time.perf_counter() - t
            M.install(verify=False)
            t = time.perf_counter()
            c1 = PI.axis_core_pieces(V, boxes, tm)
            prim["axis"][2] += time.perf_counter() - t
            prim["axis"][0] += 1
            assert c0 == c1, "axis core mismatch %r %r" % (c0, c1)
        trec += float(rec.get("seconds", 0.0))
    print("REPLAY %s: %d rebuilds, %d mismatches (int vs lib), %d record-vs-replay differences; kinds %s" % (
        os.path.basename(path), n, mism, rec_mism, kinds))
    print("rebuild per call: lib %.3f s  int %.3f s  (x%.1f); totals %.1f s -> %.1f s (recorded in the run: %.1f s)" % (
        tl / n, ti / n, tl / max(ti, 1e-9), tl, ti, trec))
    b = prim["build"]
    print("PC.build per call (%d): lib %.1f ms  fast %.1f ms (x%.1f)" % (b[0], 1e3 * b[1] / max(b[0], 1), 1e3 * b[2] / max(b[0], 1), b[1] / max(b[2], 1e-9)))
    b = prim["inter"]
    print("intersect per call (%d): lib %.1f ms  int %.1f ms (x%.1f)" % (b[0], 1e3 * b[1] / max(b[0], 1), 1e3 * b[2] / max(b[0], 1), b[1] / max(b[2], 1e-9)))
    b = prim["cert"]
    print("certify per call (%d): lib %.1f ms  int %.1f ms (x%.1f)  vec-filter %.2f ms (x%.1f)  obj %.1f ms (x%.1f); vec stats %s" % (
        b[0], 1e3 * b[1] / max(b[0], 1), 1e3 * b[2] / max(b[0], 1), b[1] / max(b[2], 1e-9), 1e3 * b[3] / max(b[0], 1), b[1] / max(b[3], 1e-9),
        1e3 * b[4] / max(b[0], 1), b[1] / max(b[4], 1e-9), PV.rep()))
    b = prim["axis"]
    print("axis core per call (%d): lib %.1f ms  int %.1f ms (x%.1f)" % (b[0], 1e3 * b[1] / max(b[0], 1), 1e3 * b[2] / max(b[0], 1), b[1] / max(b[2], 1e-9)))
    return mism


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
