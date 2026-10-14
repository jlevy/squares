"""A213b differential test 1 -- REPLAY the recorded rectangle-obstacle clips of a real run
(results/clips_<tag>_<nid>.jsonl, written by code/profclip213.py: the clip memo's MISSES -- obstacle, tilt bin, rect)
through the library and through the integer-space clip; assert the same rect, the same `stats` delta and the same
value the run recorded.  Times both, and measures the integer widths actually reached (the bit bound of notes/).
   python tests/replay_clip213.py results/clips_b4clip_<nid>.jsonl [--limit N] [--filter]
"""
import json
import os
import sys
import time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.abspath(os.path.join(HERE, "..", "code"))
sys.path.insert(0, CODE)
import pinclip_int as PI                                       # noqa: E402
import multibox as MB                                          # noqa: E402

_BINS, _OBS = {}, {}


def mkbin(a, b):
    k = (a, b)
    if k not in _BINS:
        _BINS[k] = MB.Bin(Fr(a), Fr(b))
    return _BINS[k]


def mkobs(rec):
    k = (rec["kind"], tuple(tuple(v) for v in rec["verts"]))
    o = _OBS.get(k)
    if o is None:
        o = _OBS[k] = MB.Obstacle([(Fr(a), Fr(b)) for (a, b) in rec["verts"]],
                                  name=rec.get("name", ""), kind=rec["kind"])
    return o


def rect_of(v):
    return None if v is None else tuple(Fr(x) for x in v)


def bits(rec, ic):
    """the widths the integer kernel actually reaches on this record (the empirical bit bound)."""
    x0, x1, y0, y1 = rect_of(rec["rect"])
    b = dict(vd=ic.vd.bit_length(), G=max(ic.G0.bit_length(), ic.G1.bit_length()),
             EA=max(v.bit_length() for v in ic.EA) if ic.EA else 0,
             EU=max(max(abs(v).bit_length() for v in ic.EU), max(abs(v).bit_length() for v in ic.EL)) if ic.EA else 0)
    w = 0
    for (px, py) in ((x0, y0), (x1, y1)):
        CX, CY, CW = PI.hom(px, py)
        b["CW"] = max(b.get("CW", 0), CW.bit_length())
        EUc, ELc, VXc, VYc, Msq, MG0, MG1 = ic.at(CW)
        w = max(w, Msq.bit_length(), MG0.bit_length(), MG1.bit_length())
        for k in range(ic.nE):
            w = max(w, ((ic.NX[k] * CX + ic.NY[k] * CY) * ic.EA[k]).bit_length(), abs(EUc[k]).bit_length())
        cxv, cyv = CX * ic.vd, CY * ic.vd
        for i in range(ic.nV):
            pn, qn = VXc[i] - cxv, VYc[i] - cyv
            w = max(w, (4 * (pn * pn + qn * qn)).bit_length(),
                    abs((pn * ic.C0 + qn * ic.S0) * ic.G1).bit_length())
    b["product"] = w
    return b


def main():
    path = sys.argv[1]
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    recs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    if limit:
        recs = recs[:limit]
    print("A213b replay: %d recorded clips from %s" % (len(recs), os.path.basename(path)))
    pre = [(mkobs(r), mkbin(r["t0"], r["t1"]), rect_of(r["rect"])) for r in recs]
    for (obs, bn, _r) in pre:                                   # the library's radii, warmed for both paths
        bn.radii(obs)

    def run(fn):
        out, st = [], []
        t = time.perf_counter()
        for (obs, bn, rect) in pre:
            s = {"exact_calls": 0, "backoffs": 0}
            out.append(fn(rect, obs, bn, s))
            st.append(s)
        return out, st, time.perf_counter() - t

    o1, s1, t1 = run(MB._clip_rect_obstacle)
    o2, s2, t2 = run(PI.clip_rect_obstacle)                     # cold: one IPair compiled per sampled clip
    _o, _s, t2w = run(PI.clip_rect_obstacle)                    # warm: the pair cached, as in a real run
    bad = rec_bad = 0
    for i, r in enumerate(recs):
        if o1[i] != o2[i] or s1[i] != s2[i]:
            bad += 1
            if bad <= 5:
                print("  MISMATCH %d: lib %r %r vs int %r %r" % (r["i"], o1[i], s1[i], o2[i], s2[i]))
        if o1[i] != rect_of(r["out"]) or sorted((k, v) for k, v in s1[i].items() if v) != [tuple(x) for x in r["delta"]]:
            rec_bad += 1
            if rec_bad <= 5:
                print("  RECORD DIFF %d: run %r %r vs replay %r %r" % (r["i"], r["out"], r["delta"], o1[i], s1[i]))
    B = {}
    for i, (obs, bn, _r) in enumerate(pre[:400]):
        for k, v in bits(recs[i], PI.pair(obs, bn)).items():
            B[k] = max(B.get(k, 0), v)
    n = max(len(recs), 1)
    print("A213b replay: %d clips, %d obstacles, %d bins -- %d mismatches, %d record-vs-replay differences"
          % (len(recs), len(_OBS), len(_BINS), bad, rec_bad))
    print("  clip per call:  library %.3f ms   integer space %.3f ms cold / %.3f ms warm   x%.1f / x%.1f   "
          "(run recorded %.3f ms, under cProfile)"
          % (1e3 * t1 / n, 1e3 * t2 / n, 1e3 * t2w / n, t1 / max(t2, 1e-12), t1 / max(t2w, 1e-12),
             1e3 * sum(r["seconds"] for r in recs) / n))
    print("  exact_calls %d / backoffs %d (identical both paths)"
          % (sum(s["exact_calls"] for s in s1), sum(s["backoffs"] for s in s1)))
    print("  bit widths reached (first 400 clips): %r" % (B,))
    print("  pinclip_int.rep() %r" % (PI.rep(),))
    if "--filter" in sys.argv:
        PI.FILTER = True
        PI.STATS["filt"] = PI.STATS["fallback"] = 0
        o3, s3, t3 = run(PI.clip_rect_obstacle)
        PI.FILTER = False
        f = 1 if o3 != o1 or s3 != s1 else 0
        print("  PHASE 2 float filter on family A (warm): %.3f ms per call (x%.2f vs the exact integer path, "
              "x%.1f vs the library), %d filtered / %d exact fallbacks, %d mismatches"
              % (1e3 * t3 / n, t2w / max(t3, 1e-12), t1 / max(t3, 1e-12), PI.STATS["filt"], PI.STATS["fallback"], f))
        bad += f
    return 1 if (bad or rec_bad) else 0


if __name__ == "__main__":
    sys.exit(main())
