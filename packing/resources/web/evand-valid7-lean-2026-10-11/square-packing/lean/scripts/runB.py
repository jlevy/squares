#!/usr/bin/env python3
"""Phase B: the kernel checks of the root modules, with a bounded number of `lean` processes (the
kernel needs ~8 GB per process on top of the shared imports; `lake` has no job limit).

For each root (`Sqpack/V7/R?????.lean` and its directory, from `emit_v7.py --chunk`): the leaf
modules, then their row groups, then the root module, each `lean -o … -i …` into `.lake/build`.
Prints one JSON line per root (`ok`, seconds, the failing modules).

    runB.py --lo I --hi J [--jobs N] [--mod M --rem R]     (run from s12/lean after `lake build` of the common modules)
"""
import argparse, glob, json, os, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
LIB = os.path.join(ROOT, '.lake', 'build', 'lib', 'lean')


def lean_path():
    out = subprocess.run(['lake', 'env', 'printenv', 'LEAN_PATH'], cwd=ROOT, capture_output=True, text=True)
    return out.stdout.strip()


def meminfo(key):
    for line in open('/proc/meminfo'):
        if line.startswith(key + ':'):
            return int(line.split()[1]) / 2 ** 20
    return 0.0


def rss(pid):
    try:
        for line in open(f'/proc/{pid}/status'):
            if line.startswith('VmRSS:'):
                return int(line.split()[1]) / 2 ** 20
    except OSError:
        pass
    return 0.0


class MemBudget:
    """the running `lean`s, each charged max(its estimate, its resident memory now), within `gb`; no
    new `lean` while `MemAvailable` is below `floor`; below `guard`, the youngest `lean` is killed (its
    module is run again later, charged 1.5 times the peak it reached)"""
    def __init__(self, gb, floor, guard, maxn=10 ** 6):
        self.gb, self.floor, self.guard, self.maxn = gb, floor, guard, maxn
        self.cv = threading.Condition()
        self.run = {}        # pid -> [estimate, start time, peak rss, killed]
        threading.Thread(target=self.watch, daemon=True).start()

    def used(self):
        return sum(max(r[0], r[2]) for r in self.run.values())

    def acquire(self, c):
        with self.cv:
            while self.run and (self.used() + c > self.gb or meminfo('MemAvailable') < self.floor
                                or len(self.run) >= self.maxn):
                self.cv.wait(5)

    def start(self, pid, c):
        with self.cv:
            self.run[pid] = [c, time.time(), rss(pid), False]

    def finish(self, pid):
        with self.cv:
            r = self.run.pop(pid, [0, 0, 0.0, False])
            self.cv.notify_all()
            return r

    def watch(self):
        while True:
            time.sleep(3)
            with self.cv:
                for pid in [p for p in self.run if not os.path.exists(f'/proc/{p}')]:
                    del self.run[pid]      # exited (an adopted lean is never waited for)
                for pid, r in self.run.items():
                    r[2] = max(r[2], rss(pid))
                if self.run and meminfo('MemAvailable') < self.guard:
                    pid, r = max(((p, r) for p, r in self.run.items() if not r[3]),
                                 key=lambda x: x[1][1], default=(None, None))
                    if pid is not None:
                        r[3] = True
                        try:
                            os.kill(pid, 9)
                        except OSError:
                            pass
                self.cv.notify_all()


def adopt():
    """the `lean -o` already running (left by an earlier run): source path -> pid"""
    out = {}
    for d in os.listdir('/proc'):
        if d.isdigit():
            try:
                argv = open(f'/proc/{d}/cmdline').read().split('\0')
            except OSError:
                continue
            if argv and os.path.basename(argv[0]) == 'lean' and '-o' in argv and len(argv) > 1:
                src = [x for x in argv if x.endswith('.lean')]
                if src:
                    out[os.path.normpath(os.path.join(ROOT, src[-1]))] = int(d)
    return out


ADOPTED = {}
BUDGET = None
EST = 12.0          # GB, the default estimate of one module
KILLED = []         # (module, peak GB) of the lean killed for memory


def compile_mod(src, env):
    """`lean -o` one module within the memory budget; returns (ok, seconds, tail of the log)"""
    rel = os.path.relpath(src, ROOT)[:-5]
    olean = os.path.join(LIB, rel + '.olean'); ilean = os.path.join(LIB, rel + '.ilean')
    os.makedirs(os.path.dirname(olean), exist_ok=True)
    pid = ADOPTED.get(os.path.normpath(src))
    if pid:      # an earlier run's lean on this module: wait for it
        while os.path.exists(f'/proc/{pid}'):
            time.sleep(10)
        BUDGET.finish(pid)
    if os.path.exists(ilean) and os.path.getmtime(ilean) >= os.path.getmtime(src):
        return True, 0.0, ''     # done by an earlier run (the .ilean is written after the .olean)
    c = EST
    t = time.time()
    while True:
        BUDGET.acquire(c)
        t1 = time.time()
        p = subprocess.Popen(['lean', '-o', olean, '-i', ilean, src], cwd=ROOT, env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        BUDGET.start(p.pid, c)
        out, _ = p.communicate()
        est, _, peak, killed = BUDGET.finish(p.pid)
        if p.returncode == -9:       # the watcher may have dropped the entry before `finish`
            killed, peak = True, max(peak, c)
        if not killed:
            break
        KILLED.append((rel, round(peak, 1)))
        print(json.dumps(dict(killed=rel, peak=round(peak, 1))), file=sys.stderr, flush=True)
        for f in (olean, ilean):
            if os.path.exists(f):
                os.remove(f)
        c = max(c, 1.5 * peak)
    ok = p.returncode == 0
    print(json.dumps(dict(mod=rel, sec=round(time.time() - t1, 1), peak=round(peak, 1), ok=ok)),
          file=sys.stderr, flush=True)
    return ok, time.time() - t, '' if ok else out[-2000:]


def root_job(idx, pool, env):
    """the modules of one root, in dependency order; the futures of each stage run on the pool"""
    t0 = time.time()
    d = os.path.join(ROOT, 'Sqpack', 'V7', f'R{idx:05d}')
    leaves = sorted(f for f in glob.glob(os.path.join(d, '*.lean')) if not re.search(r'_g\d+\.lean$', f))
    groups = sorted(glob.glob(os.path.join(d, '*_g*.lean')))
    fails = []
    for stage in (leaves, groups, [os.path.join(ROOT, 'Sqpack', 'V7', f'R{idx:05d}.lean')]):
        res = list(pool.map(lambda f: (f, compile_mod(f, env)), stage))
        fails += [(os.path.basename(f), r[2]) for f, r in res if not r[0]]
        if fails:
            break
    return dict(root=idx, ok=not fails, sec=round(time.time() - t0, 1), fails=[f for f, _ in fails],
                log=fails[0][1] if fails else '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lo', type=int, default=0)
    ap.add_argument('--hi', type=int, default=10 ** 6)
    ap.add_argument('--jobs', type=int, default=8)
    ap.add_argument('--mod', type=int, default=1, help='only the roots with index %% MOD == REM')
    ap.add_argument('--rem', type=int, default=0)
    ap.add_argument('--mem', type=float, default=440, help='GB budget over max(estimate, resident) of the leans')
    ap.add_argument('--floor', type=float, default=80, help='GB of MemAvailable below which no lean starts')
    ap.add_argument('--guard', type=float, default=30, help='GB of MemAvailable below which the youngest lean is killed')
    ap.add_argument('--list', help='a file of root indices, run in this order (instead of lo..hi)')
    ap.add_argument('--roots', type=int, default=4, help='roots in flight at once')
    a = ap.parse_args()
    global BUDGET
    BUDGET = MemBudget(a.mem, a.floor, a.guard, a.jobs)     # the adopted leans count toward --jobs
    ADOPTED.update(adopt())
    for pid in ADOPTED.values():
        BUDGET.start(pid, EST)
    print(json.dumps(dict(adopted=len(ADOPTED))), flush=True)
    env = dict(os.environ, LEAN_PATH=lean_path())
    order = [int(x) for x in open(a.list).read().split()] if a.list else range(a.lo, a.hi)
    idxs = [i for i in order if i % a.mod == a.rem and os.path.exists(os.path.join(ROOT, 'Sqpack', 'V7', f'R{i:05d}.lean'))
            and not os.path.exists(os.path.join(LIB, 'Sqpack', 'V7', f'R{i:05d}.olean'))]
    print(json.dumps(dict(todo=len(idxs))), flush=True)
    with ThreadPoolExecutor(a.jobs) as pool, ThreadPoolExecutor(a.roots) as outer:
        for f in as_completed([outer.submit(root_job, i, pool, env) for i in idxs]):
            print(json.dumps(f.result()), flush=True)


if __name__ == '__main__':
    main()
