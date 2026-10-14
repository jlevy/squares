"""A213 -- run one A211 page (isolated cert / results, --no-fig) under cProfile while RECORDING every library-level
`MBox.rebuild` (the K' memo's misses: the exact piece set + parameters + the result) to a jsonl for the replay test.
   python profrun213.py <tag> <nid> [--wall 900] [--pads zero]
Writes logs/profile/<tag>_<nid>.{prof,log}, results/replay_<tag>_<nid>.jsonl; certs under results/run_<tag>/.
The flag A213_INTCORE (read by mbpatch213 through coarse211.install) selects the build under test."""
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
REC = os.path.join(A213, "results", "replay_%s_%s.jsonl" % (tag, nid))
PROF = os.path.join(A213, "logs", "profile", "%s_%s.prof" % (tag, nid))
RUN = os.path.join(A213, "results", "run_%s" % tag)
os.makedirs(RUN, exist_ok=True)

import poly204                                                 # noqa: E402  (sets up the whole chain + mbpatch178)
import mbpatch178 as M8                                        # noqa: E402
import multibox as MB                                          # noqa: E402

_LIB = M8._orig_rebuild
_N = [0, 0.0]


def _s(v):
    return str(v)


def recorder(self, *a, **kw):
    pieces = [[_s(bn.t0), _s(bn.t1), [_s(x) for x in r]] for (bn, r) in self.pieces]
    rec = dict(name=self.name, kmode=self.kmode, args=[_s(x) for x in a], kw={k: _s(v) for k, v in kw.items()},
               pieces=pieces)
    t = time.perf_counter()
    try:
        out = _LIB(self, *a, **kw)
    except Exception as e:                                     # noqa: BLE001  (EmptyBox / no certified polygon)
        rec["error"] = "%s: %s" % (type(e).__name__, e)
        rec["seconds"] = time.perf_counter() - t
        with open(REC, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        raise
    rec["seconds"] = time.perf_counter() - t
    _N[0] += 1
    _N[1] += rec["seconds"]
    rec["k_source"] = self.k_source
    rec["k_info"] = {k: _s(v) for k, v in self.k_info.items()}
    rec["verts"] = [[_s(x), _s(y)] for (x, y) in getattr(self.pc, "verts", ())]
    c = self.core
    rec["core"] = None if c is None else [_s(c.kx), _s(c.ky), _s(c.tm), _s(c.a)]
    with open(REC, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    return out


M8._orig_rebuild = recorder
sys.argv = [os.path.join(A211, "run211.py"), "page", nid, "--cert-dir", RUN, "--results",
            os.path.join(RUN, "rows.jsonl"), "--no-fig", "--force"] + rest
print("A213 profrun: tag %s nid %s flag A213_INTCORE=%r argv %s" % (tag, nid, os.environ.get("A213_INTCORE"), sys.argv[1:]), flush=True)
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
    print("A213 profrun: %d library rebuilds recorded, %.1f s inside rebuild, %.1f s total; profile %s" % (
        _N[0], _N[1], time.time() - t0, PROF), flush=True)
