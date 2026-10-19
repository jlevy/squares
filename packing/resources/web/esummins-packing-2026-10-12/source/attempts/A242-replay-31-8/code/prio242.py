"""A242 -- run one reviewed script of the pinned external clone IN THIS PROCESS (runpy), at BelowNormal with
affinity 0xFFFF.  No extra process is spawned.  Refuses anything outside ext/repo and the scripts on the reviewed
allow-list (prepare_secondary.py / replay_secondary_parallel.py / verify.py are excluded: they fetch the R038
upstream file over the network or call node).

    python code/prio242.py <script.py> [args...]      (cwd is switched to ext/repo; the numba stand-in is on path)
"""
import os, runpy, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', 'ext', 'repo'))
SHIM = os.path.abspath(os.path.join(HERE, '..', 'ext', 'shim'))
ALLOWED = {'check_integrity.py', 'verify_threshold_algebra.py', 'independent_controls.py', 'exact_mixed.py'}


def lower_priority():
    try:
        import ctypes
        k32 = ctypes.windll.kernel32
        h = k32.GetCurrentProcess()
        k32.SetPriorityClass(h, 0x00004000)
        k32.SetProcessAffinityMask(h, 0xFFFF)
    except Exception:
        pass


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ALLOWED:
        raise SystemExit('prio242: script not on the reviewed allow-list: %r' % sys.argv[1:2])
    if not __debug__:
        raise SystemExit('prio242: assertions required')
    lower_priority()
    os.chdir(REPO)
    sys.path[:0] = [REPO, SHIM]
    script = os.path.join(REPO, sys.argv[1])
    sys.argv = [script] + sys.argv[2:]
    runpy.run_path(script, run_name='__main__')


if __name__ == '__main__':
    main()
