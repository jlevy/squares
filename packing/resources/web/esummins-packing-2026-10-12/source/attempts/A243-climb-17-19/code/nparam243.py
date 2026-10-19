"""A243 -- the n-PARAMETRISATION of the k5 toolkit (A171 ... A230), WRAPPED, never edited.

setup(n) imports the LIVE toolkit (path243's order: A211's live copies first, A212 never), every lazily imported
module up front, and then rebinds -- in memory, in this process only -- every n = 11 constant the toolkit reads:

  (1) module globals equal to s0 = 969271/250000 (Fraction or float) and to the window floor 3.82 = 191/50  ->  s_hi,
      s_lo of the new window (lanelib.SHAT = 3.8770835900 is defined and never read: left alone);
  (2) the constants DERIVED from them at import (classes178.LAM_MAX, multibox.LAM_MAX_A168 / W0_RAT / C_WIDEN,
      polylane.LAM_MAX / W0, lane.LAM_MAX, quick200.LAM_MAX / PADS["window"]) recomputed from the new window;
  (3) function DEFAULTS (module functions and class methods): s-type defaults equal to an old value -> the new one,
      a parameter named `n` with default 11 -> n;
  (4) the n = 11 literals in function BODIES that are reached: tree209.noroom_at (m = 11 - len(roles), n=11 passed
      explicitly) -> noroom_at243 below; the k >= 9 GATES (tree205b / tree209 / tree211 / quick200
      `len(pg.roles) >= 9`) are cost gates, not lemmas: noroom_at243 returns UNDECIDED at once unless m = n - k <= 2,
      which is exactly the gate k >= n - 2 they encode at n = 11;
  (5) the CLASS layer (classes178 name table / pins / scoreboard / forced cells, strata224's FULL prefix, clip207's
      certified basins) -> classtab243's census + verdict table (n != 11 only; at n = 11 the A53 / A56 originals stay).
report() returns every rebinding made (notes/climb243.md); scan() lists every remaining 11 / s0 literal in the
loaded sources so each is either generalised here or recorded as unreachable."""
import inspect
import math
import os
import re
import sys
import time
import types
from fractions import Fraction as Fr

import path243

OLD_S = Fr(969271, 250000)
OLD_SHAT = 3.877083590022814
OLD_WLO = Fr(382, 100)
OLD_W0 = 0.025509194                      # polylane.W0 at n = 11 (captured as a default by corner_cell / lane_corner)
LAZY = ("geo178b", "geo178c", "fast30b", "cert203", "count203", "csp203b", "snap224", "strata224",
        "polycore_vec", "ckernel214", "chordlane", "polylane", "fastclip211")
CFG = dict(n=11, s_hi=OLD_S, s_lo=OLD_WLO, done=False, extra=set())
REP = []


def _att_modules():
    out = []
    for name, m in list(sys.modules.items()):
        f = getattr(m, "__file__", None) or ""
        if m is not None and os.path.abspath(f).startswith(path243.ATT) and "A243-climb" not in f:
            out.append((name, m))
    return out


def _new_value(v, s_hi, s_lo):
    if isinstance(v, bool) or not isinstance(v, (Fr, float)):
        return None
    if isinstance(v, Fr):
        if v == OLD_S:
            return s_hi
        if v == OLD_WLO:
            return s_lo
        return None
    if abs(v - float(OLD_S)) < 1e-12:                     # (lanelib.SHAT is defined, never read: left alone)
        return float(s_hi)
    if abs(v - 3.82) < 1e-12:
        return float(s_lo)
    return None


def _patch_defaults(fn, where, n, s_hi, s_lo):
    code = getattr(fn, "__code__", None)
    if code is None:
        return
    if fn.__defaults__:
        names = code.co_varnames[:code.co_argcount][-len(fn.__defaults__):]
        new = list(fn.__defaults__)
        for k, (pn, v) in enumerate(zip(names, new)):
            nv = _new_value(v, s_hi, s_lo)
            if nv is None and pn == "n" and type(v) is int and v == 11:
                nv = n
            if nv is not None and nv != v:
                new[k] = nv
                REP.append(("default", where + "." + fn.__name__, pn, str(v), str(nv)))
        fn.__defaults__ = tuple(new)
    if fn.__kwdefaults__:
        for pn, v in list(fn.__kwdefaults__.items()):
            nv = _new_value(v, s_hi, s_lo)
            if nv is None and pn == "n" and type(v) is int and v == 11:
                nv = n
            if nv is not None and nv != v:
                fn.__kwdefaults__[pn] = nv
                REP.append(("kwdefault", where + "." + fn.__name__, pn, str(v), str(nv)))


def _walk(mname, m, n, s_hi, s_lo):
    for gname, v in list(vars(m).items()):
        nv = _new_value(v, s_hi, s_lo)
        if nv is not None and nv != v:
            setattr(m, gname, nv)
            REP.append(("global", mname + "." + gname, "", str(v), str(nv)))
        if isinstance(v, types.FunctionType) and v.__module__ == m.__name__:
            _patch_defaults(v, mname, n, s_hi, s_lo)
        elif inspect.isclass(v) and v.__module__ == m.__name__:
            for an, av in list(vars(v).items()):
                fn = av.__func__ if isinstance(av, (staticmethod, classmethod)) else av
                if isinstance(fn, types.FunctionType):
                    _patch_defaults(fn, mname + "." + v.__name__, n, s_hi, s_lo)


def setup(n, s_hi=None, s_lo=None, classes=True):
    """import the toolkit and rebind it to n squares on the window [s_lo, s_hi].  One n per process."""
    if CFG["done"]:
        assert CFG["n"] == n, "nparam243: one n per process"
        return CFG
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    import census243 as CEN
    if s_hi is None:
        s_lo, s_hi = CEN.WINDOWS[n][0], CEN.WINDOWS[n][1]
    s_hi, s_lo = Fr(s_hi), Fr(s_lo)
    path243.fix()
    import stage209, tree211, run211                              # noqa: F401,E401  the LIVE stack (A211)
    path243.fix()
    import tree209 as _N9
    for loader in (_N9.NR, _N9.N221):                             # A189 / A221 (their dirs are added by the loaders)
        try:
            loader()
        except Exception as e:                                    # noqa: BLE001
            REP.append(("lazy-import-failed", loader.__name__, "", repr(e)[:80], ""))
    for name in LAZY:
        try:
            __import__(name)
        except Exception as e:                                    # noqa: BLE001
            REP.append(("lazy-import-failed", name, "", repr(e)[:80], ""))
    path243.fix()
    bad = path243.check()
    assert not bad, "A243: shared modules from the wrong attempt: %s" % (bad,)
    lam = s_hi / s_lo
    for mname, m in _att_modules():
        _walk(mname, m, n, s_hi, s_lo)
    import classes178 as CL
    import multibox as MB
    import quick200 as QP
    MB.LAM_MAX_A168 = s_hi / MB.WLO_A168                          # WLO_A168 was rebound to s_lo by the walk
    MB.W0_RAT = (MB.LAM_MAX_A168 - 1) * (1 + 1 / MB.SQ2_LO)
    MB.C_WIDEN = 1 + MB.W0_RAT
    CL.LAM_MAX = float(s_hi) / float(s_lo)
    QP.LAM_MAX = lam
    QP.PADS = {"window": lam, "zero": Fr(1)}
    for mod in ("polylane", "lane"):
        M = sys.modules.get(mod)
        if M is None:
            continue
        M.LAM_MAX = float(s_hi) / float(s_lo)
        if hasattr(M, "W0"):
            M.W0 = (M.LAM_MAX - 1.0) * (1.0 + 1.0 / math.sqrt(2.0))
            for fn in vars(M).values():
                if isinstance(fn, types.FunctionType) and fn.__defaults__:
                    fn.__defaults__ = tuple(M.W0 if (isinstance(v, float) and abs(v - OLD_W0) < 1e-6) else v for v in fn.__defaults__)
    REP.append(("derived", "multibox.C_WIDEN/W0_RAT/LAM_MAX_A168; classes178.LAM_MAX; quick200.LAM_MAX/PADS; polylane.LAM_MAX/W0; lane.LAM_MAX",
                "", "s0/3.82", "%s/%s" % (s_hi, s_lo)))
    import tree209 as N9
    N9.noroom_at = noroom_at243
    REP.append(("body", "tree209.noroom_at", "", "m = 11 - len(roles); n=11", "noroom_at243 (n = %d; attempted iff m <= 2)" % n))
    CFG.update(n=n, s_hi=s_hi, s_lo=s_lo, lam=lam, done=True, N9=N9)
    if n != 11 and classes:
        install_classes(n)
    return CFG


def install_classes(n):
    """the class layer at a new n (classes178 / strata224 / clip207 are read through these names at call time)."""
    import classtab243 as CT
    import classes178 as CL
    import strata224 as ST
    import clip207 as C7
    import geo178 as G
    tab = CT.table(n)
    CFG["tab"] = tab
    CL.name_to_slots = lambda: {k: tuple(sorted((round(a, 5), round(b, 5)) for a, b in tab.pins_of(k))) for k in tab.rows}
    CL.class_of = lambda pts: tab.name_of(list(pts))
    CL.pins_of = tab.pins_of
    CL.scoreboard_status = tab.status
    CL.forced_cells = lambda cls, s=None, max_off=None: CT.forced_cells(tab, cls, CL.S0 if s is None else s, max_off, CFG["extra"])
    ST.FULL_PREFIX = CT.FULL_PREFIX
    ST.SCOREBOARD = "attempts/A243-climb-17-19/results/verdicts243_n%d.jsonl (this n's window table; Lemma K1)" % n
    C7.load_basins = lambda cls, pad, lam: []                     # certified basins exist only at n = 11 (A207 / A83)
    G.class_of_record = lambda rec: tab.name_of([(p["kx"], p["ky"]) for p in rec["pins"]]) or "n%d_k00_0000" % n
    REP.append(("class-layer", "classes178 / strata224 / clip207 / geo178.class_of_record", "", "A53 + A56 scoreboard",
                "census243 + verdicts243_n%d" % n))


def set_extra(cells):
    """the climb's hypothesis: these cells are met by two non-pin squares (Theorem FC's first horn, ASSUMED)."""
    CFG["extra"] = set(cells)


def noroom_at243(pg, wall_left, log=print, deadline=None, parent_pockets=None):
    """tree209.noroom_at with n threaded through: m = n - k, attempted only when m <= 2 (the n = 11 gate k >= 9 is
    k >= n - 2); otherwise UNDECIDED at once (sound: no claim)."""
    n, N9 = CFG["n"], CFG["N9"]
    k = len(pg.roles)
    m = n - k
    if m > 2:
        pg.T.test("NOROOM", k=k, m=m, verdict="UNDECIDED", clip=None, bound=None, cn_bound=None, n_pockets=0, seconds=0.0)
        return dict(k=k, m=m, verdict="UNDECIDED", clip=None, reason="not attempted: m = n - k = %d > 2 (gate k >= n - 2)" % m,
                    bound=None, pockets=[], cn_bound=None, bisect=None, lanes=None, seconds=0.0)
    roles = {kk: tuple(float(v) for v in b) for kk, b in pg.roles.items()}
    t0 = time.time()
    bud = dict(total_deadline=max(60.0, min(900.0, wall_left - 30)) if deadline is None else float(deadline))
    if m >= 2:
        bud["max_pocket_area"] = 0.0
    try:
        if N9.A221 and parent_pockets:
            out = N9.N221().noroom_child(roles, parent_pockets, budget=bud, name=pg.name, n=n)
        elif N9.A221:
            out = N9.N221().noroom(roles, s0=None, budget=bud, name=pg.name, n=n)
        else:
            out = N9.NR().noroom(roles, s0=None, budget=bud, name=pg.name, n=n)
    except Exception as e:                                        # noqa: BLE001
        out = dict(verdict="ERROR", reason=repr(e)[:200])
    res = dict(k=k, m=m, verdict=out.get("verdict"), clip=None, reason=str(out.get("reason"))[:300], bound=out.get("bound"),
               pockets=out.get("pockets") or [], cn_bound=None, bisect=out.get("bisect"), lanes=out.get("lanes"),
               seconds=round(time.time() - t0, 1))
    if res["verdict"] == "DEAD":
        res["clip"] = out.get("clip") or ("NOROOM" if out.get("leaf") != "EmptyBox (A171 pair leaf)" else "EmptyBox")
    elif res["verdict"] == "UNDECIDED" and res["pockets"]:
        g, ok = N9.cn_groups(res["pockets"])
        if ok:
            res["cn_bound"] = g
            if g < m:
                res.update(verdict="DEAD", clip="NOROOM-CN", reason="pocket CN bound %d < %d free squares (Lemma CN)" % (g, m))
    pg.T.test("NOROOM", k=k, m=m, verdict=res["verdict"], clip=res["clip"], bound=res["bound"], cn_bound=res["cn_bound"],
              n_pockets=len(res["pockets"]), seconds=res["seconds"])
    log("   no-room (k=%d, m=%d, n=%d): %s%s in %.0f s" % (k, m, n, res["verdict"], (" by " + res["clip"]) if res["clip"] else "", res["seconds"]))
    return res


PAT = re.compile(r"969271|3\.877|3\.82\b|191/50|\bn=11\b|\b11 - |\b11\)|range\(11\)|== *11\b|>= *9\b|< *9\b|>= *10\b")


def scan():
    """every remaining n = 11 / s0 literal in the loaded toolkit sources (the notes' reachability table)."""
    out = []
    for name, m in sorted(_att_modules(), key=lambda t: t[0]):
        f = getattr(m, "__file__", "")
        try:
            src = open(f, encoding="utf-8", errors="replace").read().splitlines()
        except Exception:                                         # noqa: BLE001
            continue
        for i, ln in enumerate(src):
            t = ln.split("#")[0]
            if PAT.search(t):
                out.append((os.path.relpath(f, path243.ROOT).replace("\\", "/"), i + 1, ln.strip()[:150]))
    return out


def report():
    return list(REP)
