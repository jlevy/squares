#!/usr/bin/env python3
"""The s(59) kernel run: per batch of root cells (batches.json), the generator (gen_zmmtree_s59.py),
then `lean -o` of each Part file, then the batch's Roots.lean, all into LEAN_DIR/.lake/build.
Restartable: a task is done when its marker in WORK/done/ exists (written after rc 0 and fsync).

    run_s59.py LEAN_DIR COVER BATCHES WORK [--slots N] [--share I/K]

LEAN_DIR is the `lean/` directory of evand/square-packing at commit 1718a58 with this folder's
`scripts/` and `Sqpack/S59T/Pts.lean` added and `lake build Sqpack.S59T.Pts Sqpack.Attain` done.
`--share I/K` takes the batches with index % K == I (one share per machine).
A task starts only when MemAvailable > 10 GB (a Part file needs about 2.6 GB on top of the
shared imports, 9.8 GB resident at most in the recorded run).
Log: WORK/logs/tasks.jsonl (one line per finished task), WORK/logs/<task>.log.
"""
import argparse, json, os, subprocess, time

ap = argparse.ArgumentParser()
ap.add_argument('lean_dir'); ap.add_argument('cover'); ap.add_argument('batches'); ap.add_argument('work')
ap.add_argument('--slots', type=int, default=os.cpu_count())
ap.add_argument('--share', default='0/1')
a = ap.parse_args()
L = os.path.abspath(a.lean_dir)
B = f"{L}/.lake/build/lib/lean"
W = os.path.abspath(a.work)
DONE, LOGS, PKL = f"{W}/done", f"{W}/logs", f"{W}/pkl"
COVER = os.path.abspath(a.cover)
for d in (DONE, LOGS, PKL):
    os.makedirs(d, exist_ok=True)
batches = json.load(open(a.batches))
si, sk = map(int, a.share.split('/'))
mine = [int(k) for k in sorted(batches, key=int) if int(k) % sk == si]
env = dict(os.environ)
env["LEAN_PATH"] = subprocess.run(['lake', 'env', 'printenv', 'LEAN_PATH'], cwd=L, capture_output=True,
                                  text=True, check=True).stdout.strip()


def done(t):
    return os.path.exists(f"{DONE}/{t}")


def olean_of(t):
    k, rest = t[1:].split("_", 1)
    name = f"Part{rest[1:]}" if rest.startswith("P") else "Roots"
    return f"{B}/Sqpack/S59T/B{k}/{name}.olean"


def fsync_path(p):
    fd = os.open(p, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def mark(t):
    if t.startswith("gen_"):
        d = f"{L}/Sqpack/S59T/B{t[5:]}"
        for f in os.listdir(d):
            fsync_path(f"{d}/{f}")
    elif not t.startswith("ALL"):
        fsync_path(olean_of(t))
    with open(f"{DONE}/{t}", "w") as f:
        os.fsync(f.fileno())


def lean_ok(p, k):
    """a generated file is complete: it ends with the batch's `end`"""
    try:
        with open(p, "rb") as f:
            f.seek(max(0, os.path.getsize(p) - 64))
            return f.read().rstrip().endswith(f"end SquarePacking.S59T.B{k}".encode())
    except OSError:
        return False


def olean_ok(p):
    try:
        with open(p, "rb") as f:
            return f.read(5) == b"olean"
    except OSError:
        return False


def check_markers():
    """after a hard stop, a marker can outlive its file: drop the markers whose files are bad"""
    bad = []
    for t in os.listdir(DONE):
        if t.startswith("ALL"):
            continue
        if t.startswith("gen_"):
            k = t[5:]
            d = f"{L}/Sqpack/S59T/B{k}"
            fs = [f for f in os.listdir(d) if f.endswith(".lean")] if os.path.isdir(d) else []
            ok = "Roots.lean" in fs and all(lean_ok(f"{d}/{f}", k) for f in fs)
        else:
            ok = olean_ok(olean_of(t))
        if not ok:
            bad.append(t)
            os.remove(f"{DONE}/{t}")
    log(dict(task="CHECK_MARKERS", dropped=bad))


def log(rec):
    rec["at"] = int(time.time())
    with open(f"{LOGS}/tasks.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")


def avail_gb():
    for line in open("/proc/meminfo"):
        if line.startswith("MemAvailable"):
            return int(line.split()[1]) / 2 ** 20
    return 0


def gen_cmd(k):
    out = f"Sqpack/S59T/B{k}"
    cells = ";".join(batches[str(k)])
    return (f"rm -rf {out} && python3 scripts/gen_zmmtree_s59.py {COVER} --n 59 --pitch 1/20 --ubins 16 "
            f"--depth 40 --cells '{cells}' --name S59T --outdir {out} --chunk-cost 600 --batch {k} "
            f"--save {PKL}/B{k}.pkl && test -s {out}/Roots.lean")


def lean_cmd(mod):
    p = mod.replace(".", "/")
    os.makedirs(os.path.dirname(f"{B}/{p}"), exist_ok=True)
    return f"lean -o {B}/{p}.olean {p}.lean"


def parts_of(k):
    d = f"{L}/Sqpack/S59T/B{k}"
    return sorted(int(f[4:-5]) for f in os.listdir(d) if f.startswith("Part") and f.endswith(".lean"))


def ready():
    gens, leans = [], []
    for k in mine:
        g = f"gen_B{k}"
        if not done(g):
            if g not in running and g not in failed:
                gens.append((g, gen_cmd(k)))
            continue
        allp = True
        for p in parts_of(k):
            t = f"B{k}_P{p}"
            if not done(t):
                allp = False
                if t not in running and t not in failed:
                    leans.append((t, lean_cmd(f"Sqpack.S59T.B{k}.Part{p}")))
        r = f"B{k}_R"
        if allp and not done(r) and r not in running and r not in failed:
            leans.append((r, lean_cmd(f"Sqpack.S59T.B{k}.Roots")))
    return gens, leans


def start(t, cmd):
    lg = open(f"{LOGS}/{t}.log", "w")
    full = f"cd {L} && exec nice -n 10 /usr/bin/time -f 'TIME %e %M' bash -c \"{cmd}\""
    running[t] = (subprocess.Popen(full, shell=True, env=env, stdout=lg, stderr=subprocess.STDOUT,
                                   stdin=subprocess.DEVNULL), time.time())


check_markers()
running = {}   # task -> (Popen, t0)
failed = set()
while True:
    for t, (p, t0) in list(running.items()):
        if p.poll() is None:
            continue
        del running[t]
        tl = ""
        try:
            tl = [x for x in open(f"{LOGS}/{t}.log") if x.startswith("TIME ")][-1].split()
        except Exception:
            pass
        log(dict(task=t, rc=p.returncode, wall=round(time.time() - t0, 1),
                 sec=float(tl[1]) if tl else None, maxrss_kb=int(tl[2]) if tl else None))
        if p.returncode == 0:
            mark(t)
        else:
            failed.add(t)
    gens, leans = ready()
    if not gens and not leans and not running:
        break
    while len(running) < a.slots and (gens or leans) and avail_gb() > 10:
        t, cmd = (gens or leans).pop(0)
        start(t, cmd)
        time.sleep(0.2)
    time.sleep(5)
log(dict(task="RUN_END", failed=sorted(failed)))
if not failed:
    mark(f"ALL_{si}_{sk}")
