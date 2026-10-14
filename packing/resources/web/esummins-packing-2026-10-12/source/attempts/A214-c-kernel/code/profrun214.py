"""A214 -- run one A211 page under cProfile with isolated cert / results dirs (A213's profrun213 without the
rebuild recorder: the replay jsonl A214 tests against is A213's, already recorded).
   python code/profrun214.py <tag> <nid> [--wall 900] [--pads zero]
Writes logs/profile/<tag>_<nid>.prof and results/run_<tag>/.  The flag A214_CKERNEL (read by mbpatch213 through
coarse211.install_a213) selects the vertex kernel; A213_INTCORE / A213_INTCLIP select A213's own layers."""
import cProfile
import os
import runpy
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
A214 = os.path.abspath(os.path.join(HERE, ".."))
A211 = os.path.abspath(os.path.join(HERE, "..", "..", "A211-coarse-tree", "code"))
sys.path.insert(0, A211)
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(v, "1")

tag, nid = sys.argv[1], sys.argv[2]
rest = sys.argv[3:]
PROF = os.path.join(A214, "logs", "profile", "%s_%s.prof" % (tag, nid))
RUN = os.path.join(A214, "results", "run_%s" % tag)
os.makedirs(RUN, exist_ok=True)
os.makedirs(os.path.dirname(PROF), exist_ok=True)


def belownormal():
    try:
        import ctypes
        k = ctypes.windll.kernel32
        k.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint]
        k.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
        k.GetPriorityClass.argtypes = [ctypes.c_void_p]
        h = ctypes.c_void_p(-1)
        k.SetPriorityClass(h, 0x00004000)
        k.SetProcessAffinityMask(h, 0xFFFF)
        print("   priority class %d (16384 = BelowNormal)" % k.GetPriorityClass(h), flush=True)
    except Exception as e:                                     # noqa: BLE001
        print("   belownormal failed: %r" % (e,), flush=True)


belownormal()
sys.argv = [os.path.join(A211, "run211.py"), "page", nid, "--cert-dir", RUN, "--results",
            os.path.join(RUN, "rows.jsonl"), "--no-fig", "--force"] + rest
print("A214 profrun: tag %s nid %s A214_CKERNEL=%r A213_INTCORE=%r A213_INTCLIP=%r argv %s" % (
    tag, nid, os.environ.get("A214_CKERNEL"), os.environ.get("A213_INTCORE"),
    os.environ.get("A213_INTCLIP"), sys.argv[1:]), flush=True)
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
        sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "A213-int-polycore", "code")))
        import mbpatch213 as M
        print("A214 profrun: mbpatch213 %s" % (M.rep(),), flush=True)
        import ckernel214 as K
        print("A214 profrun: kernel %s" % (K.rep(),), flush=True)
    except Exception as e:                                     # noqa: BLE001
        print("A214 profrun: no kernel report (%r)" % (e,), flush=True)
    print("A214 profrun: %.1f s total; profile %s" % (time.time() - t0, PROF), flush=True)
