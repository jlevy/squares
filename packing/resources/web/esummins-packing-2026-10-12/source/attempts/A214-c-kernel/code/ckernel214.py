"""A214 -- the ctypes front end for the C kernel (build/ckernel214.dll) and the graceful fallback to A213's
Python-int path.  No Python.h, no extension module: a plain DLL of pure C functions.

`install()` replaces, IN MEMORY only, two names of A213's modules:
    polycore_int.vertex_ok_h  -> the C scalar kernel  (so certify_h / vertex_ok / pieces_poly / axis_core_pieces /
                                 A135's exactcore all route through C without knowing it),
    polycore_vec.certify_verts -> the C batch kernel  (nv vertices x nb boxes in one call).
Nothing is edited on disk; A213's functions stay the reference, and every route back to them is taken whenever the
kernel cannot prove its answer:

FALLBACK PROTOCOL (three gates, each one falling back to the Python-int path of A213):
  (1) no DLL / a different machine / a load error  -> AVAILABLE is False, install() does nothing at all;
  (2) an input outside the envelope the C code is proved for (|X|, |Y|, W, |CX|, |CY|, CW >= 2^60, |T0|, |T1|, E
      >= 2^31, or a coefficient >= 2^93 -- e.g. the axis-core corners, whose W = den aden Q can reach 2^110) ->
      the C function returns UNDECIDED and the caller runs polycore_int's unbounded-int test;
  (3) a t0 / t1 / corner that is not an exact double -> the float filter's error model does not apply, so the
      batch is not offered to C at all (the same guard polycore_vec._compile makes).
So the kernel returns only OK / BAD / "ask Python"; it can never decide a pair it cannot prove.
"""
import ctypes
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
A213 = os.path.abspath(os.path.join(HERE, "..", "..", "A213-int-polycore", "code"))
for _p in (HERE, A213):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import polycore_int as PI                                      # noqa: E402  (A213 -- the reference and the fallback)

DLL = os.environ.get("A214_DLL") or os.path.abspath(os.path.join(HERE, "..", "build", "ckernel214.dll"))
FLAG = os.environ.get("A214_CKERNEL", "1") != "0"
VERIFY = os.environ.get("A214_VERIFY") == "1"
LIM60 = 1 << 60
LIM31 = 1 << 31
# A228 (input guard, gate (2') of the FALLBACK PROTOCOL): `a214_cert_batch` addresses its output with
# `int i0 = i * nb`, a C int -- at nv * nb >= 2^31 that product overflows, i0 goes negative and the kernel writes
# OUTSIDE the ctypes buffer (an access violation, or silent heap corruption, which is worse).  The Python caller
# is the only place that knows the real product, so it refuses the batch there and runs A213's unbounded-int path,
# exactly as it does for a box outside the coefficient envelope.  The C code is untouched.
LIM_PAIRS = 1 << 30
STATS = dict(scalar=0, scalar_py=0, batch=0, pairs=0, undecided=0, exact_c=0, punt=0, batch_py=0, verified=0)
_PY_VOK = PI.vertex_ok_h                                       # the reference, captured before any patching


def _PY_CERT(hv, ibs):
    """polycore_int.certify_h with the ORIGINAL Python-int test (PI.certify_h itself resolves the patched name)."""
    bad = []
    for i, (X, Y, W) in enumerate(hv):
        for ib in ibs:
            if not _PY_VOK(X, Y, W, ib):
                bad.append(i)
                break
    return bad


class CBox(ctypes.Structure):
    _fields_ = [("bx", ctypes.c_double * 4), ("by", ctypes.c_double * 4),
                ("t0", ctypes.c_double), ("t1", ctypes.c_double),
                ("cx", ctypes.c_longlong * 4), ("cy", ctypes.c_longlong * 4),
                ("cw", ctypes.c_longlong), ("t0i", ctypes.c_longlong),
                ("t1i", ctypes.c_longlong), ("e", ctypes.c_longlong)]


def _load():
    try:
        lib = ctypes.CDLL(DLL)
        i64, d, P = ctypes.c_longlong, ctypes.c_double, ctypes.POINTER
        lib.a214_version.restype = ctypes.c_int
        lib.a214_self_test.restype = ctypes.c_int
        lib.a214_sizeof_box.restype = ctypes.c_int
        lib.a214_vertex_ok.argtypes = [d, d, i64, i64, i64, P(CBox)]
        lib.a214_vertex_ok.restype = ctypes.c_int
        lib.a214_vertex_ok_exact.argtypes = [i64, i64, i64, P(CBox)]
        lib.a214_vertex_ok_exact.restype = ctypes.c_int
        lib.a214_vertex_filter.argtypes = [d, d, P(CBox)]
        lib.a214_vertex_filter.restype = ctypes.c_int
        lib.a214_cert_batch.argtypes = [ctypes.c_int, ctypes.c_int, P(d), P(d), P(i64), P(i64), P(i64),
                                        P(CBox), P(ctypes.c_ubyte), P(i64)]
        lib.a214_cert_batch.restype = i64
        lib.a214_counters.argtypes = [P(i64)]
        lib.a214_counters.restype = None
        assert lib.a214_version() == 1, "unexpected kernel version"
        assert lib.a214_sizeof_box() == ctypes.sizeof(CBox), "CBox layout mismatch"
        assert lib.a214_self_test() == 0, "kernel self-test failed"
        return lib
    except Exception as e:                                     # noqa: BLE001  -- any failure = no kernel, no harm
        global LOAD_ERROR
        LOAD_ERROR = "%s: %s" % (type(e).__name__, e)
        return None


LOAD_ERROR = None
LIB = _load() if FLAG else None
AVAILABLE = LIB is not None
CSTATS = (ctypes.c_longlong * 4)()


# ------------------------------------------------------------------------------------ the box compilation (cached)
_CBC = {}


def _exact_d(n, d):
    """the double n/d, or None when n/d is not exactly a double (then the float filter's model does not apply)."""
    v = n / d
    if v != v or v in (float("inf"), float("-inf")):
        return None
    fn, fd = v.as_integer_ratio()
    return v if fn * d == n * fd else None


def cbox_of(ib):
    """the C struct for a polycore_int.IBox, or None when it is outside the kernel's envelope."""
    key = id(ib)
    hit = _CBC.get(key)
    if hit is not None and hit[0] is ib:
        return hit[1]
    cb = None
    cw, e = ib.cw, ib.e
    if 0 < cw < LIM60 and 0 < e < LIM31 and -LIM31 < ib.t0 < LIM31 and -LIM31 < ib.t1 < LIM31 \
            and all(-LIM60 < c < LIM60 for c in ib.cx + ib.cy):
        t0 = _exact_d(ib.t0, e)
        t1 = _exact_d(ib.t1, e)
        bx = [_exact_d(c, cw) for c in ib.cx]
        by = [_exact_d(c, cw) for c in ib.cy]
        if t0 is not None and t1 is not None and None not in bx and None not in by:
            cb = CBox((ctypes.c_double * 4)(*bx), (ctypes.c_double * 4)(*by), t0, t1,
                      (ctypes.c_longlong * 4)(*ib.cx), (ctypes.c_longlong * 4)(*ib.cy), cw, ib.t0, ib.t1, e)
    if len(_CBC) >= 4096:
        _CBC.clear()
    _CBC[key] = (ib, cb)                                       # the IBox is kept alive so its id stays this entry's
    return cb


def _in_env(X, Y, W):
    return 0 < W < LIM60 and -LIM60 < X < LIM60 and -LIM60 < Y < LIM60


# ------------------------------------------------------------------------------------ the drop-ins
def vertex_ok_h(X, Y, W, ib):
    """drop-in for polycore_int.vertex_ok_h: the C kernel, the Python-int test wherever C cannot prove its answer."""
    cb = cbox_of(ib)
    if cb is None or not _in_env(X, Y, W):
        STATS["scalar_py"] += 1
        return _PY_VOK(X, Y, W, ib)
    STATS["scalar"] += 1
    r = LIB.a214_vertex_ok(X / W, Y / W, X, Y, W, ctypes.byref(cb))
    if r < 0:
        STATS["scalar_py"] += 1
        return _PY_VOK(X, Y, W, ib)
    out = r == 1
    if VERIFY:
        STATS["verified"] += 1
        assert out == _PY_VOK(X, Y, W, ib), "A214 VERIFY vertex_ok_h %r %r" % ((X, Y, W), out)
    return out


def certify_h(hv, ibs):
    """drop-in for polycore_int.certify_h: one C call for the whole (vertex, box) grid."""
    nv, nb = len(hv), len(ibs)
    if nv == 0 or nb == 0:
        return []
    if nv * nb >= LIM_PAIRS:                                   # A228: `int i * nb` in the kernel would overflow
        STATS["batch_py"] += 1
        STATS["batch_pairs_guard"] = STATS.get("batch_pairs_guard", 0) + 1
        return _PY_CERT(hv, ibs)
    cbs = [cbox_of(ib) for ib in ibs]
    if None in cbs or not all(_in_env(*p) for p in hv):
        STATS["batch_py"] += 1
        return _PY_CERT(hv, ibs)
    STATS["batch"] += 1
    d, i64 = ctypes.c_double, ctypes.c_longlong
    vx = (d * nv)(*[p[0] / p[2] for p in hv])
    vy = (d * nv)(*[p[1] / p[2] for p in hv])
    VX = (i64 * nv)(*[p[0] for p in hv])
    VY = (i64 * nv)(*[p[1] for p in hv])
    VW = (i64 * nv)(*[p[2] for p in hv])
    boxes = (CBox * nb)(*cbs)
    out = (ctypes.c_ubyte * (nv * nb))()
    LIB.a214_cert_batch(nv, nb, vx, vy, VX, VY, VW, boxes, out, CSTATS)
    bad = []
    for i in range(nv):
        row = out[i * nb:(i + 1) * nb]
        if 1 in row:
            bad.append(i)
            continue
        if 2 in row:                                           # the kernel handed this pair back: finish in Python
            j = row.index(2)
            X, Y, W = hv[i]
            for k in range(j, nb):
                STATS["punt"] += 1
                if not _PY_VOK(X, Y, W, ibs[k]):
                    bad.append(i)
                    break
    if VERIFY:
        STATS["verified"] += 1
        assert bad == _PY_CERT(hv, ibs), "A214 VERIFY certify_h %r" % (bad,)
    return bad


def certify_verts(verts, boxes):
    """drop-in for multibox.certify_verts / polycore_vec.certify_verts."""
    ibs = [PI.ibox_of(pb, pt0, pt1) for (pb, pt0, pt1) in boxes]
    return certify_h([PI.hom(x, y) for (x, y) in verts], ibs)


# ------------------------------------------------------------------------------------ install / report
INSTALLED = [False]
_ORIG_CERT_H = PI.certify_h


def install():
    """route A213's integer kernel through C (idempotent, in memory only).  False = the Python path is untouched."""
    if not AVAILABLE or INSTALLED[0]:
        return INSTALLED[0]
    PI.vertex_ok_h = vertex_ok_h                               # certify_h / vertex_ok / axis_core_pieces use it
    PI.certify_h = certify_h
    try:
        import polycore_vec as PV
        PV.certify_verts = certify_verts
    except Exception:                                          # noqa: BLE001  (numpy absent: the scalar path is enough)
        pass
    INSTALLED[0] = True
    return True


def uninstall():
    PI.vertex_ok_h, PI.certify_h = _PY_VOK, _ORIG_CERT_H
    INSTALLED[0] = False


def counters():
    """the kernel's coverage counters: quadratics decided exactly / endpoint negative / interior minimum entered
    (the discriminant: the widest arithmetic) / discriminant negative / envelope guard refused."""
    if not AVAILABLE:
        return {}
    c = (ctypes.c_longlong * 5)()
    LIB.a214_counters(c)
    return dict(exact_quads=c[0], endpoint_neg=c[1], interior=c[2], disc_neg=c[3], guard=c[4])


def rep():
    return dict(available=AVAILABLE, installed=INSTALLED[0], flag=FLAG, verify=VERIFY, dll=DLL,
                load_error=LOAD_ERROR, c_pairs=CSTATS[0], c_undecided=CSTATS[1], c_exact=CSTATS[2],
                c_punt=CSTATS[3], cover=counters(), **STATS)
