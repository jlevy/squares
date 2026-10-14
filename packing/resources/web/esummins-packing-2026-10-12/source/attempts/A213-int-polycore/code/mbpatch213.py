"""A213 -- the runtime patch (NO edit on disk of the read-only libraries, the mbpatch178 pattern) that routes the K'
build through integer space:  polycore.build -> polycore_fast.build (the float pipeline, bit-identical, vectorised),
polycore.vertex_ok -> polycore_int.vertex_ok (also what A135 exactcore.a_ok calls), multibox.pieces_poly /
axis_core_pieces / certify_verts -> the polycore_int drop-ins.  `MBox.rebuild` itself is untouched: it looks these
names up in its module at call time, so the memo (fastclip211), the empty-K' handling (mbpatch178) and the coarse grid
(coarse211) stack on top exactly as before.

Flags:  A213_INTCORE=0 turns the patch off (the library runs as before);  A213_VERIFY=1 runs BOTH builds on every
call and asserts the results equal (the differential test, live);  A213_VEC=1 routes the vertex certification through
polycore_vec (Phase 2, itself falling back to the exact integer path wherever the float filter cannot decide);
A214_CKERNEL=0 keeps the vertex test in Python (default ON: the C kernel of A214 under the same integer path).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import polycore_int as PI                                      # noqa: E402
import pinclip_int as PIC                                      # noqa: E402  (A213b: the rectangle-obstacle clip)
import polycore_fast as PF                                     # noqa: E402
import multibox as MB                                          # noqa: E402  READ-ONLY (A171)
import polycore as PC                                          # noqa: E402  READ-ONLY (A132)

FLAG = os.environ.get("A213_INTCORE", "1") != "0"      # default ON: the replay of 441 rebuilds + the fuzz passed with 0 mismatches
VERIFY = os.environ.get("A213_VERIFY") == "1"
VEC = os.environ.get("A213_VEC", "0") == "1"
FLAGC = os.environ.get("A213_INTCLIP", "1") != "0"     # A213b, default ON: the replay (1,882 recorded clips) + the fuzz (450 clips, 3,284 point tests) passed with 0 mismatches
FLAGK = os.environ.get("A214_CKERNEL", "1") != "0"     # A214: the C kernel under the integer path (default ON:
                                                      # the replay + fuzz + tests/diff214.py pass with 0 mismatches)
ORIG = dict(build=PC.build, vertex_ok=PC.vertex_ok, pieces_poly=MB.pieces_poly,
            axis_core_pieces=MB.axis_core_pieces, certify_verts=MB.certify_verts,
            clip=MB._clip_rect_obstacle)
INSTALLED = [False]
CLIP_AT = [None]
_CLIP_PREV = []
STATS = dict(build=0, vertex_ok=0, pieces_poly=0, axis_core=0, certify=0, clip=0, verified=0)


def _same_pc(a, b):
    return (list(getattr(a, "verts", ())) == list(getattr(b, "verts", ())) and getattr(a, "shrink", None) == getattr(b, "shrink", None)
            and getattr(a, "n_grid", None) == getattr(b, "n_grid", None))


def _err(f, *a, **kw):
    try:
        return ("ok", f(*a, **kw))
    except Exception as e:                                     # noqa: BLE001
        return ("err", type(e).__name__, str(e))


def _verified(name, new, old, same):
    def g(*a, **kw):
        r = _err(new, *a, **kw)
        s = _err(old, *a, **kw)
        STATS["verified"] += 1
        ok = (r[0] == s[0]) and (same(r[1], s[1]) if r[0] == "ok" else r[1:] == s[1:])
        assert ok, "A213 VERIFY %s: int %r != lib %r" % (name, r[:3], s[:3])
        if r[0] == "err":
            new(*a, **kw)                                      # re-raise the same exception
        return r[1]
    g.__name__ = name
    return g


def _counted(name, f):
    def g(*a, **kw):
        STATS[name] += 1
        return f(*a, **kw)
    g.__name__ = f.__name__
    return g


def _verified_clip(new, old):
    """the clip's differential wrapper: `stats` and `trace` are MUTATED, so the library gets copies."""
    def g(rect, obs, bn, stats, trace=None, tag=""):
        s2 = dict(stats)
        n0 = 0 if trace is None else len(trace)
        out = new(rect, obs, bn, stats, trace=trace, tag=tag)
        t2 = None if trace is None else []
        ref = old(rect, obs, bn, s2, trace=t2, tag=tag)
        STATS["verified"] += 1
        assert ref == out and s2 == stats and (t2 is None or t2 == trace[n0:]), (
            "A213 VERIFY clip: int %r %r != lib %r %r" % (out, stats, ref, s2))
        return out
    g.__name__ = "clip_rect_obstacle"
    return g


def _lib_clip_slot():
    """the INNERMOST clip slot: the library function itself, under whatever the chain has wrapped around it --
    A178's `obs is None` guard (`mbpatch178._orig_clip`) and A211's memo (`fastclip211._ORIG_CLIP`, the miss path).
    Patching the innermost slot keeps every wrapper above it working exactly as before."""
    M8 = sys.modules.get("mbpatch178")
    if M8 is not None and getattr(M8, "_orig_clip", None) is not None:
        return M8, "_orig_clip", M8._orig_clip
    FC = sys.modules.get("fastclip211")
    if FC is not None and getattr(FC, "_ORIG_CLIP", None) is not None:
        return FC, "_ORIG_CLIP", FC._ORIG_CLIP
    return MB, "_clip_rect_obstacle", MB._clip_rect_obstacle


def install_clip(verify=None):
    """A213b: route `_clip_rect_obstacle` to the integer-space clip, at the innermost slot (idempotent)."""
    if not FLAGC:
        return False
    verify = VERIFY if verify is None else verify
    holder, attr, lib = _lib_clip_slot()
    if getattr(lib, "_a213b", False):
        return True                                            # already routed
    ORIG["clip"] = lib
    clip = PIC.clip_rect_obstacle
    if verify:
        clip = _verified_clip(clip, lib)
    clip = _counted("clip", clip)
    clip._a213b = True
    del _CLIP_PREV[:]
    _CLIP_PREV.append((holder, attr, lib))
    setattr(holder, attr, clip)
    CLIP_AT[0] = "%s.%s" % (getattr(holder, "__name__", holder), attr)
    return True


def uninstall_clip():
    for (o, a, prev) in _CLIP_PREV:
        setattr(o, a, prev)
    del _CLIP_PREV[:]
    CLIP_AT[0] = None


def _pp_same(a, b):
    return a[0] == b[0] and a[1] == b[1] and [(x.x0, x.x1, x.y0, x.y1, y, z) for x, y, z in a[2]] == \
        [(x.x0, x.x1, x.y0, x.y1, y, z) for x, y, z in b[2]]


CKERNEL = [False]


def install_ckernel():
    """A214: route polycore_int's vertex test through the C kernel (build/ckernel214.dll, ctypes).  Bit-exact -- the
    kernel answers only what it can prove and hands every other pair back to the Python-int path, which stays the
    reference and the fallback (no DLL / another machine / outside the proved envelope).  Idempotent."""
    if not FLAGK or CKERNEL[0]:
        return CKERNEL[0]
    try:
        a214 = os.path.abspath(os.path.join(HERE, "..", "..", "A214-c-kernel", "code"))
        if a214 not in sys.path:
            sys.path.insert(0, a214)
        import ckernel214 as CK
        CKERNEL[0] = CK.install()
    except Exception:                                          # noqa: BLE001  -- never let the kernel stop a node
        CKERNEL[0] = False
    return CKERNEL[0]


def install(verify=None, vec=None):
    """route the library's names to the integer-space build (idempotent).  Returns True when installed."""
    verify = VERIFY if verify is None else verify
    install_ckernel()
    vec = VEC if vec is None else vec
    if not FLAG:                                               # A213 off, A213b still available on its own flag
        return install_clip(verify)
    build, vok, pp, ac, cv = PF.build, PI.vertex_ok, PI.pieces_poly, PI.axis_core_pieces, PI.certify_verts
    if vec:
        import polycore_vec as PV
        cv = PV.certify_verts
    if verify:
        build = _verified("build", build, ORIG["build"], _same_pc)
        vok = _verified("vertex_ok", vok, ORIG["vertex_ok"], lambda a, b: a == b)
        pp = _verified("pieces_poly", pp, ORIG["pieces_poly"], _pp_same)
        ac = _verified("axis_core_pieces", ac, ORIG["axis_core_pieces"], lambda a, b: a == b)
        cv = _verified("certify_verts", cv, ORIG["certify_verts"], lambda a, b: a == b)
    PC.build = _counted("build", build)
    PC.vertex_ok = _counted("vertex_ok", vok)
    MB.pieces_poly = _counted("pieces_poly", pp)
    MB.axis_core_pieces = _counted("axis_core", ac)
    MB.certify_verts = _counted("certify", cv)
    install_clip(verify)
    INSTALLED[0] = True
    return True


def uninstall():
    uninstall_clip()
    PC.build, PC.vertex_ok = ORIG["build"], ORIG["vertex_ok"]
    MB.pieces_poly, MB.axis_core_pieces, MB.certify_verts = ORIG["pieces_poly"], ORIG["axis_core_pieces"], ORIG["certify_verts"]
    INSTALLED[0] = False


def rep():
    return dict(installed=INSTALLED[0], flag=FLAG, flag_clip=FLAGC, clip_at=CLIP_AT[0],
                verify=VERIFY, vec=VEC, ckernel=CKERNEL[0], **STATS)
