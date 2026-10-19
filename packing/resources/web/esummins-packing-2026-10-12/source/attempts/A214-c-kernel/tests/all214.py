"""A214 -- every differential test, each in its own BelowNormal subprocess so the A214_CKERNEL flag can be flipped:
   tests/diff214.py            the C kernel against A213's Python-int reference, layer by layer;
   A213 tests/replay213.py     the 441 recorded rebuilds of the Y0202 pad-0 run, ONCE WITH THE KERNEL OFF and once
                               with it ON -- both legs assert against the library build, and the pair is the
                               per-call table (Python-int vs C);
   A213 tests/fuzz213.py       150 random piece sets + 2,700 vertex tests + the polygon primitives, kernel ON.
   python tests/all214.py [--quick]"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
A214 = os.path.abspath(os.path.join(HERE, ".."))
A213 = os.path.abspath(os.path.join(HERE, "..", "..", "A213-int-polycore"))
REC = os.path.join(A213, "results", "replay_before_k5_11_interior_Y0202.jsonl")
QUICK = "--quick" in sys.argv

ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUNBUFFERED="1", OMP_NUM_THREADS="1",
           OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", NUMEXPR_NUM_THREADS="1", A213_INTCORE="1")
PRIO = ["-c", "import ctypes,runpy,sys\n"
              "k=ctypes.windll.kernel32\n"
              "k.SetPriorityClass.argtypes=[ctypes.c_void_p,ctypes.c_uint]\n"
              "k.SetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.c_size_t]\n"
              "h=ctypes.c_void_p(-1)\nk.SetPriorityClass(h,0x4000)\nk.SetProcessAffinityMask(h,0xFFFF)\n"
              "sys.argv=sys.argv[1:]\nrunpy.run_path(sys.argv[0],run_name='__main__')\n"]


def run(label, script, argv, ckernel):
    print("\n===== %s  (A214_CKERNEL=%s)  %s %s" % (label, ckernel, os.path.basename(script), " ".join(argv)),
          flush=True)
    t = time.time()
    env = dict(ENV, A214_CKERNEL=ckernel)
    p = subprocess.run([sys.executable] + PRIO + [script] + argv, env=env, capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    if p.stderr.strip():
        sys.stdout.write("STDERR:\n" + p.stderr[-4000:])
    print("===== %s done rc=%d in %.1f s" % (label, p.returncode, time.time() - t), flush=True)
    return p.returncode


if __name__ == "__main__":
    rc = 0
    rc += run("diff214", os.path.join(HERE, "diff214.py"), ["60" if QUICK else "300", "214"], "1")
    lim = ["--limit", "40"] if QUICK else []
    rc += run("replay213 KERNEL OFF", os.path.join(A213, "tests", "replay213.py"), [REC] + lim, "0")
    rc += run("replay213 KERNEL ON", os.path.join(A213, "tests", "replay213.py"), [REC] + lim, "1")
    rc += run("fuzz213 KERNEL ON", os.path.join(A213, "tests", "fuzz213.py"), ["40" if QUICK else "150", "213"], "1")
    print("\nALL214 rc=%d" % rc, flush=True)
    sys.exit(1 if rc else 0)
