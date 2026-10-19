"""A214 differential test -- the C kernel against A213's Python-int reference (polycore_int.vertex_ok_h), on
   (a) the EXACT 192-bit path alone (a214_vertex_ok_exact: every sample, so the big arithmetic is exercised whether
       or not the float filter would have decided it),
   (b) the FLOAT FILTER alone (a214_vertex_filter: every decided answer must be the reference's -- an undecided one
       is allowed and counted),
   (c) the full scalar kernel (filter + exact + the Python fallback) and the BATCH kernel, against the reference.
Samples: random rational points on the 1e-9 grid against random boxes, and BOUNDARY points (exactly half a side
from a corner along the tilted axes at t0, and +- 1e-12) where the filter must fall through to the exact path, and
OUT-OF-ENVELOPE points (W ~ 2^70, the axis-core shape) where the kernel must return UNDECIDED rather than an answer.
   python tests/diff214.py [n_boxes=300] [seed=214]"""
import os
import random
import sys
import time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.abspath(os.path.join(HERE, "..", "code"))
A213 = os.path.abspath(os.path.join(HERE, "..", "..", "A213-int-polycore", "code"))
sys.path.insert(0, CODE)
sys.path.insert(0, A213)
import ctypes                                                  # noqa: E402
import ckernel214 as K                                         # noqa: E402
import polycore_int as PI                                      # noqa: E402
import multibox as MB                                          # noqa: E402
import polycore as PC                                          # noqa: E402
from caselp import Box, t_lo, t_hi                             # noqa: E402

VDEN = PC.VDEN
REF = K._PY_VOK                                                # polycore_int.vertex_ok_h, unpatched


def rand_box(rng):
    x0, y0 = rng.uniform(0.5, 3.0), rng.uniform(0.5, 3.0)
    b = Box(x0, x0 + rng.uniform(0.0, 0.3), y0, y0 + rng.uniform(0.0, 0.3), rng.uniform(0, 89), 0)
    b.th1 = min(90.0, b.th0 + rng.choice([0.0, 0.5, 5.0, 30.0]))
    return b, t_lo(b.th0), t_hi(b.th1)


BIGDEN = 1 << 37                                               # W up to 2^37: with CW = 2^53 the coefficients
                                                               # reach ~2^91, the endpoint value ~2^141, the
                                                               # discriminant ~2^182 -- the full 192-bit width


def points_for(b, t0, rng, n):
    """three classes: `grid` (the 1e-9 grid of a real build), `wide` (W ~ 2^37: the widest in-envelope arithmetic,
    including near-boundary points where the filter must fall through), `far` (the exact tilted-axis boundary
    points, whose W is ~2^80 -- outside the envelope, so the kernel must hand them back)."""
    out = []
    for _ in range(n):
        out.append(("grid", (Fr(round(rng.uniform(b.x0 - 0.7, b.x1 + 0.7) * VDEN), VDEN),
                             Fr(round(rng.uniform(b.y0 - 0.7, b.y1 + 0.7) * VDEN), VDEN))))
    c, s = MB._cs_at(t0)                                       # the exact tilted axes: boundary points
    for (cx, cy) in ((b.x0, b.y0), (b.x1, b.y1), (b.x0, b.y1)):
        for (u, w) in ((Fr(1, 2), Fr(0)), (Fr(1, 2), Fr(1, 3)), (Fr(-1, 2), Fr(-1, 2)), (Fr(0), Fr(1, 2))):
            px, py = Fr(cx) + u * c - w * s, Fr(cy) + u * s + w * c
            for e in (0, Fr(1, 10 ** 12), -Fr(1, 10 ** 12)):
                out.append(("far", (px + e, py)))
                out.append(("far", (px, py + e)))
            for d in (BIGDEN, BIGDEN - 1, 3 ** 21):            # the same boundary, ROUNDED into the envelope
                out.append(("wide", (Fr(round(px * d), d), Fr(round(py * d), d))))
    for _ in range(n):                                         # random points over a wide denominator
        d = rng.randrange(1 << 30, BIGDEN)
        out.append(("wide", (Fr(round(rng.uniform(b.x0 - 0.5, b.x1 + 0.5) * d), d),
                             Fr(round(rng.uniform(b.y0 - 0.5, b.y1 + 0.5) * d), d))))
    return out


def main():
    n_boxes = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 214)
    if not K.AVAILABLE:
        print("A214 kernel NOT available: %s" % K.LOAD_ERROR)
        return 1
    n = nt = exact_mism = filt_mism = full_mism = batch_mism = 0
    klass = {}
    filt_undec = exact_undec = 0
    tc = tp = 0.0
    for _ in range(n_boxes):
        b, t0, t1 = rand_box(rng)
        ib = PI.ibox_of(b, t0, t1)
        cb = K.cbox_of(ib)
        assert cb is not None, "a normal piece box must compile to the C envelope"
        pts = points_for(b, t0, rng, 24)
        hv = [PI.hom(x, y) for (_k, (x, y)) in pts]
        for (kind, (X, Y, W)) in zip([k for (k, _p) in pts], hv):
            n += 1
            klass[kind] = klass.get(kind, 0) + 1
            ref = REF(X, Y, W, ib)
            r = K.LIB.a214_vertex_ok_exact(X, Y, W, ctypes.byref(cb))       # (a) the 192-bit path, always
            if r < 0:
                exact_undec += 1
            elif (r == 1) != ref:
                exact_mism += 1
                print("EXACT MISMATCH", X, Y, W, r, ref)
            f = K.LIB.a214_vertex_filter(X / W, Y / W, ctypes.byref(cb))    # (b) the filter alone
            if f == 0:
                filt_undec += 1
            elif (f == 1) != ref:
                filt_mism += 1
                print("FILTER MISMATCH", X, Y, W, f, ref)
            t = time.perf_counter()                                          # (c) the full scalar kernel
            got = K.vertex_ok_h(X, Y, W, ib)
            dt = time.perf_counter() - t
            t = time.perf_counter()
            REF(X, Y, W, ib)
            dp = time.perf_counter() - t
            if kind != "far":                                                # time the kernel where it is used
                nt += 1
                tc += dt
                tp += dp
            if got != ref:
                full_mism += 1
                print("KERNEL MISMATCH", X, Y, W, got, ref)
        # --- the batch against the reference, on a grid of these vertices x a few boxes
        ibs = [ib] + [PI.ibox_of(*rand_box(rng)) for _ in range(rng.randint(1, 5))]
        hin = [p for (k, p) in zip([k for (k, _p) in pts], hv) if k != "far"]
        got = K.certify_h(hin, ibs)
        ref = K._PY_CERT(hin, ibs)
        if got != ref:
            batch_mism += 1
            print("BATCH MISMATCH", got[:8], ref[:8])
    print("A214 diff: %d (vertex, box) samples over %d boxes; classes %s" % (n, n_boxes, klass))
    print("  exact 192-bit path : %d mismatches, %d undecided (guard)" % (exact_mism, exact_undec))
    print("  float filter       : %d mismatches, %d undecided (-> exact)" % (filt_mism, filt_undec))
    print("  full scalar kernel : %d mismatches;  C %.2f us/call   Python-int %.2f us/call  (x%.1f)"
          % (full_mism, 1e6 * tc / max(nt, 1), 1e6 * tp / max(nt, 1), tp / max(tc, 1e-12)))
    print("  batch kernel       : %d mismatches over %d grids" % (batch_mism, n_boxes))
    # --- out of the envelope: the kernel must say UNDECIDED, and the drop-in must still answer correctly
    b, t0, t1 = rand_box(rng)
    ib = PI.ibox_of(b, t0, t1)
    cb = K.cbox_of(ib)
    big = 0
    for _ in range(200):
        W = rng.randrange(1 << 61, 1 << 70)
        X = round(rng.uniform(b.x0, b.x1) * W)
        Y = round(rng.uniform(b.y0, b.y1) * W)
        if K.vertex_ok_h(X, Y, W, ib) != REF(X, Y, W, ib):
            big += 1
        Xs, Ys, Ws = (ctypes.c_longlong(X & ((1 << 63) - 1)), ctypes.c_longlong(Y & ((1 << 63) - 1)),
                      ctypes.c_longlong(W))
        if K.LIB.a214_vertex_ok_exact(Xs, Ys, Ws, ctypes.byref(cb)) >= 0 and W >= (1 << 60):
            big += 1
            print("ENVELOPE: the kernel answered outside its envelope", W)
    print("  out-of-envelope    : %d failures of 200 (W ~ 2^61..2^70 -> Python-int)" % big)
    # --- throughput on the shape the hot path really has: a certified polygon (16 vertices) against the N piece
    # boxes it was built from -- every pair passes, so all 16 x 12 = 192 pairs (3,072 quadratic tests) are evaluated
    bb, bt0, bt1 = rand_box(rng)
    boxes, cx, cy = [], 0.5 * (bb.x0 + bb.x1), 0.5 * (bb.y0 + bb.y1)
    for _ in range(12):
        b2 = Box(bb.x0, bb.x1, bb.y0, bb.y1, bb.th0, 0)
        b2.th1 = bb.th1
        boxes.append(PI.ibox_of(b2, bt0, bt1))
    cbs = (K.CBox * 12)(*[K.cbox_of(b) for b in boxes])
    hv = [PI.hom(Fr(round((cx + rng.uniform(-1e-4, 1e-4)) * VDEN), VDEN),
                 Fr(round((cy + rng.uniform(-1e-4, 1e-4)) * VDEN), VDEN)) for _ in range(16)]
    d, i64 = ctypes.c_double, ctypes.c_longlong
    vx, vy = (d * 16)(*[p[0] / p[2] for p in hv]), (d * 16)(*[p[1] / p[2] for p in hv])
    VX, VY, VW = ((i64 * 16)(*[p[0] for p in hv]), (i64 * 16)(*[p[1] for p in hv]), (i64 * 16)(*[p[2] for p in hv]))
    outb = (ctypes.c_ubyte * 192)()
    reps = 2000
    t = time.perf_counter()
    for _ in range(reps):
        K.LIB.a214_cert_batch(16, 12, vx, vy, VX, VY, VW, cbs, outb, None)
    dtc = (time.perf_counter() - t) / reps
    t = time.perf_counter()
    for _ in range(50):
        K._PY_CERT(hv, boxes)
    dtp = (time.perf_counter() - t) / 50
    t = time.perf_counter()
    for _ in range(200):
        K.certify_h(hv, boxes)
    dtw = (time.perf_counter() - t) / 200
    npair = sum(1 for v in outb if v != 3)
    print("  batch throughput   : 16 verts x 12 boxes = %d pairs evaluated -- C call %.1f us (%.0f ns/pair),"
          " +ctypes/Python wrapper %.1f us, Python-int reference %.0f us"
          % (npair, 1e6 * dtc, 1e9 * dtc / max(npair, 1), 1e6 * dtw, 1e6 * dtp))
    print("  kernel stats: %s" % K.rep())
    return exact_mism + filt_mism + full_mism + batch_mism + big


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
