"""A213b -- run one A211 page (isolated cert / results dirs, --no-fig) under cProfile, optionally RECORDING a stride
sample of the library-level `_clip_rect_obstacle` calls (the clip memo's MISSES: obstacle, tilt bin, rect -> rect and
the stats delta) to a jsonl for tests/replay_clip213.py.
   python profclip213.py <tag> <nid> [--wall 900] [--pads zero]
env:  A213_RECCLIP=1 record (BEFORE run only), A213_RECSTRIDE=53, A213_RECCAP=6000
      A213_INTCLIP=0/1 selects the clip under test, A213_INTCORE=0/1 the K' build (A213).
Writes logs/profile/<tag>_<nid>.{prof,log}, results/clips_<tag>_<nid>.jsonl; certs under results/run_<tag>/."""
import cProfile
import json
import os
import runpy
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
A213 = os.path.abspath(os.path.join(HERE, ".."))
A211 = os.path.abspath(os.path.join(HERE, "..", "..", "A211-coarse-tree", "code"))
sys.path.insert(0, A211)
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

tag, nid = sys.argv[1], sys.argv[2]
rest = sys.argv[3:]
REC = os.path.join(A213, "results", "clips_%s_%s.jsonl" % (tag, nid))
PROF = os.path.join(A213, "logs", "profile", "%s_%s.prof" % (tag, nid))
RUN = os.path.join(A213, "results", "run_%s" % tag)
os.makedirs(RUN, exist_ok=True)
os.makedirs(os.path.dirname(PROF), exist_ok=True)

import poly204                                                 # noqa: E402,F401  (sets up the whole chain)
import multibox as MB                                          # noqa: E402

RECORD = os.environ.get("A213_RECCLIP") == "1"
STRIDE = int(os.environ.get("A213_RECSTRIDE", "53"))
CAP = int(os.environ.get("A213_RECCAP", "6000"))
_LIB = MB._clip_rect_obstacle
_N = [0, 0, 0.0]                                               # calls, recorded, seconds


def _s(v):
    return None if v is None else [str(x) for x in v]


def recorder(rect, obs, bn, stats, trace=None, tag=""):
    i = _N[0]
    _N[0] += 1
    if trace is not None or i % STRIDE or _N[1] >= CAP:
        return _LIB(rect, obs, bn, stats, trace=trace, tag=tag)
    before = dict(stats)
    t = time.perf_counter()
    out = _LIB(rect, obs, bn, stats, trace=trace, tag=tag)
    dt = time.perf_counter() - t
    _N[1] += 1
    _N[2] += dt
    rec = dict(i=i, kind=obs.kind, name=obs.name,
               verts=[[str(a), str(b)] for (a, b) in obs.verts],
               t0=str(bn.t0), t1=str(bn.t1), rect=_s(rect), out=_s(out), seconds=dt,
               delta=sorted((k, stats[k] - before.get(k, 0)) for k in stats if stats[k] != before.get(k, 0)))
    with open(REC, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    return out


if RECORD:
    MB._clip_rect_obstacle = recorder                          # BEFORE fastclip211 imports: it becomes the memo's miss path

sys.argv = [os.path.join(A211, "run211.py"), "page", nid, "--cert-dir", RUN, "--results",
            os.path.join(RUN, "rows.jsonl"), "--no-fig", "--force"] + rest
print("A213b profclip: tag %s nid %s A213_INTCLIP=%r A213_INTCORE=%r record=%r argv %s"
      % (tag, nid, os.environ.get("A213_INTCLIP"), os.environ.get("A213_INTCORE"), RECORD, sys.argv[1:]), flush=True)
pr = cProfile.Profile()
t0 = time.time()
pr.enable()
try:
    runpy.run_path(sys.argv[0], run_name="__main__")
except SystemExit:
    pass
finally:
    pr.disable()
    pr.dump_stats(PROF)
    try:
        import mbpatch213 as M213
        print("   mbpatch213.rep() %r" % (M213.rep(),), flush=True)
        import pinclip_int as PIC
        print("   pinclip_int.rep() %r" % (PIC.rep(),), flush=True)
    except Exception as e:                                     # noqa: BLE001
        print("   (no mbpatch213: %r)" % (e,), flush=True)
    print("A213b profclip: %d library clips, %d recorded (%.1f s inside them), %.1f s total; profile %s"
          % (_N[0], _N[1], _N[2], time.time() - t0, PROF), flush=True)
