#!/usr/bin/env python3
"""ValidTilt9 on one machine: per root, the certificate (run_v7.py, rows' minima), the Lean modules
(emit_v7.py, --chunk 20), then `lean -o` of the leaf modules, their row groups and the root module.
Restartable: a task is done when its marker in ~/v9/done/ exists (written after rc 0 and fsync).
Started by memory, measured: a task starts when MemAvailable, less ALPHA times the growth still ahead of
the running tasks (their peak private size less their present anonymous memory), keeps FLOOR GB free after
its own peak; leaf starts are at least GAP s apart, so their peaks are staggered.  Below FLOOR
the youngest task is killed.  A task killed by the driver or by the kernel (signal 9) is run again; after
its second kill it runs alone under the nominal booking (each running task books NEED, the import once).

    run9.py MACHINE [SLOTS]      (MACHINE: a or b; root i goes to a when i % 2 == 0)

Log: ~/v9/logs/tasks.jsonl, ~/v9/logs/<task>.log.  Stop file: ~/v9/STOP (no new tasks).
"""
import json, os, re, signal, subprocess, sys, time

H = os.path.expanduser("~/v9")
SC = f"{H}/v9/lean/scripts"
L = f"{H}/lean"
B = f"{L}/.lake/build/lib/lean"
DONE, LOGS, CERT = f"{H}/done", f"{H}/logs", f"{H}/cert"
SRC = f"{L}/Sqpack/V9"
for d in (DONE, LOGS, CERT, SRC):
    os.makedirs(d, exist_ok=True)
me = sys.argv[1]
slots = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
NROOTS = 16200
roots = [i for i in range(NROOTS) if (i % 2 == 0) == (me == "a")]
if os.environ.get("V9_ONLY"):   # a test: only these roots
    roots = [int(x) for x in os.environ["V9_ONLY"].split(",")]
TOOLS = os.path.expanduser("~/.elan/toolchains/leanprover--lean4---v4.33.1")
P = os.path.expanduser("~/s59/sp/lean/.lake/packages")
env = dict(os.environ)
env["PATH"] = f"{TOOLS}/bin:" + env["PATH"]
env["LEAN_PATH"] = ":".join([B] + [f"{P}/{p}/.lake/build/lib/lean" for p in sorted(os.listdir(P))])
NEED = dict(cert=2, emit=2, def_=15, grp=3, root=2)   # GB, private
SHARED, RESERVE = 7, 8
MEMT = [int(l.split()[1]) / 2 ** 20 for l in open("/proc/meminfo") if l.startswith("MemTotal")][0]
# measured peaks of the anonymous memory (GB; leaf p99 15.4, max 16; group p99 5, max 14.6; root max 9)
PEAK = dict(cert=2, emit=2, def_=15, grp=6, root=9)
ALPHA = float(os.environ.get("V9_ALPHA", "0.5"))
FLOOR = float(os.environ.get("V9_FLOOR", "40"))
GAP = float(os.environ.get("V9_GAP", "2"))   # s between leaf starts
PAGE = os.sysconf("SC_PAGE_SIZE") / 2 ** 30


DONESET, DONE_AT = set(), 0.0


MANUAL = set()   # roots whose certificate is made by hand (~/v9/manual_certs, one root per line)


def refresh_done():
    """the markers, read from disk (at start, every 10 minutes, and when the previous driver has ended:
    markers can also be written by hand), and the roots left to hand-made certificates"""
    global DONESET, DONE_AT, MANUAL
    DONESET = set(os.listdir(DONE))
    DONE_AT = time.time()
    try:
        MANUAL = {int(x) for x in open(f"{H}/manual_certs").read().split()}
    except (OSError, ValueError):
        pass


def done(t):
    return t in DONESET


def fsync_path(p):
    fd = os.open(p, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def olean_ok(p):
    try:
        with open(p, "rb") as f:
            return f.read(5) == b"olean"
    except OSError:
        return False


def rd(i):
    return f"R{i:05d}"


def outputs(t):
    """the files a task leaves behind"""
    kind, i, rest = t.split(":", 2) if t.count(":") == 2 else (*t.split(":"), "")
    i = int(i)
    if kind == "cert":
        return [f"{CERT}/{rd(i)}.pkl"]
    if kind == "emit":
        d = f"{SRC}/{rd(i)}"
        return [f"{SRC}/{rd(i)}.lean"] + ([f"{d}/{f}" for f in os.listdir(d)] if os.path.isdir(d) else [])
    if kind == "root":
        return [f"{B}/Sqpack/V9/{rd(i)}.olean"]
    return [f"{B}/Sqpack/V9/{rd(i)}/{rest}.olean"]


def mark(t):
    for p in ([] if t.startswith("ALL_") else outputs(t)):
        fsync_path(p)
    with open(f"{DONE}/{t}", "w") as f:
        os.fsync(f.fileno())
    DONESET.add(t)


def check_markers():
    """after a hard stop, a marker can outlive its file: drop the markers whose files are bad.
    Outputs are fsync'ed before their marker, so only markers of the last 6 hours are read (a full check
    reads every output's header: half an hour on a cold disk after a preemption); V9_FULLCHECK=1 reads all."""
    bad = []
    recent = 0 if os.environ.get("V9_FULLCHECK") else time.time() - 6 * 3600
    for t in os.listdir(DONE):
        if t.startswith("ALL_"):
            continue
        if os.stat(f"{DONE}/{t}").st_mtime < recent:
            continue
        kind = t.split(":")[0]
        fs = outputs(t)
        if kind in ("cert", "emit"):
            ok = all(os.path.exists(p) and os.path.getsize(p) > 0 for p in fs)
        else:
            ok = all(olean_ok(p) for p in fs)
        if not ok:
            bad.append(t)
            os.remove(f"{DONE}/{t}")
    log(dict(task="CHECK_MARKERS", dropped=bad))


def log(rec):
    rec["at"] = int(time.time())
    with open(f"{LOGS}/tasks.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")


def avail_gb():
    for l in open("/proc/meminfo"):
        if l.startswith("MemAvailable"):
            return int(l.split()[1]) / 2 ** 20
    return 0


def anon_by_group():
    """anonymous memory (GB) of each process group: a task runs in its own session (its pgid is its pid);
    resident less shared (file and shmem) pages, from /proc/*/stat and statm"""
    out = {}
    for d in os.listdir("/proc"):
        if not d.isdigit():
            continue
        try:
            with open(f"/proc/{d}/stat") as f:
                st = f.read()
            pg = int(st[st.rindex(")") + 2:].split()[2])
            if pg not in GROUPS:
                continue
            with open(f"/proc/{d}/statm") as f:
                m = f.read().split()
            out[pg] = out.get(pg, 0) + (int(m[1]) - int(m[2])) * PAGE
        except (OSError, ValueError, IndexError):
            pass
    return out


GROUPS = set()


def lean_cmd(mod):
    p = mod.replace(".", "/")
    return f"cd {L} && lean -o {B}/{p}.olean {p}.lean"


def cert_cmd(i):
    """rows' minima first; where a leaf still fails, again with mixed chains (V7_MIXED_CH), then with
    mixed chains and leaf depth 12 (root 4262), then depth 18, ten levels of splitting and a finer angle
    grid (roots 11397, 11827)"""
    run = f"python3 run_v7.py --lo {i} --hi {i + 1} --nproc 1 --out {CERT}"
    ok = f"test -s {CERT}/{rd(i)}.pkl"
    return (f"cd {SC} && (V7_SUBM=1 {run}; {ok} || V7_SUBM=1 V7_MIXED_CH=1 {run}; "
            f"{ok} || V7_SUBM=1 V7_MIXED_CH=1 V7_MAXDEPTH=12 {run}; "
            f"{ok} || V7_SUBM=1 V7_MIXED_CH=1 V7_MAXDEPTH=18 V7_SPLIT=10 V7_RSHIFT=3 {run}) && {ok}")


def emit_cmd(i):
    return (f"cd {SC} && V7_X=1 python3 emit_v7.py --cert {CERT} --out {SRC} --lo {i} --hi {i + 1} --chunk 20 "
            f"&& test -s {SRC}/{rd(i)}.lean")


GRP = re.compile(r"^(r\d{5}l\d+)_g\d+$")


MODS = {}   # root -> (defs, grps); fixed once the root is emitted


def modules(i):
    if i in MODS:
        return MODS[i]
    d = f"{SRC}/{rd(i)}"
    fs = sorted(f[:-5] for f in os.listdir(d) if f.endswith(".lean")) if os.path.isdir(d) else []
    defs = [f for f in fs if not GRP.match(f)]
    grps = [(f, GRP.match(f).group(1)) for f in fs if GRP.match(f)]
    MODS[i] = (defs, grps)
    return defs, grps


CAP = 4 * slots   # at most this many waiting leaf/group tasks are listed per pass


def ready():
    """tasks in priority order: roots, groups, leaf definitions, emits, certificates"""
    out = {k: [] for k in ("root", "grp", "def_", "emit", "cert")}
    for i in roots:
        r = f"root:{i}"
        if done(r):
            continue
        if not done(f"cert:{i}"):
            if i not in MANUAL:   # a hand-made one counts once its marker is written
                out["cert"].append((f"cert:{i}", "cert", cert_cmd(i)))
            continue
        if not done(f"emit:{i}"):
            out["emit"].append((f"emit:{i}", "emit", emit_cmd(i)))
            continue
        defs, grps = modules(i)
        allm = True
        for f in defs:
            t = f"def:{i}:{f}"
            if not done(t):
                allm = False
                if len(out["def_"]) < CAP:
                    out["def_"].append((t, "def_", lean_cmd(f"Sqpack.V9.{rd(i)}.{f}")))
        for f, base in grps:
            t = f"grp:{i}:{f}"
            if not done(t):
                allm = False
                if done(f"def:{i}:{base}") and len(out["grp"]) < CAP:
                    out["grp"].append((t, "grp", lean_cmd(f"Sqpack.V9.{rd(i)}.{f}")))
        if allm:
            out["root"].append((r, "root", lean_cmd(f"Sqpack.V9.{rd(i)}")))
    return [x for k in ("root", "grp", "def_", "emit", "cert") for x in out[k]]


check_markers()
refresh_done()
# taking over from a running driver (V9_AFTER=its pid): wait until its lean and emit tasks are done, then
# leave the certificates alone while it lives (it marks the ones it still runs, then exits on its STOP)
AFTER = int(os.environ.get("V9_AFTER", "0"))


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def busy(pat):
    return subprocess.run(["pgrep", "-f", pat], capture_output=True).returncode == 0


if AFTER:
    while alive(AFTER) and (busy("^lean -o") or busy("emit_v7.py")):
        time.sleep(5)
    log(dict(task="TAKEOVER", after=AFTER, old_alive=alive(AFTER)))
running = {}   # task -> (Popen, t0, kind)
old_gone = False
failed = set()
kills = {}         # task -> times killed (by the kernel or by the driver)
strict = set()     # killed twice: run alone, under the nominal booking
killed_by_me = set()
last_start = last_kill = last_gate = 0.0
n_oom = 0


def start(t, kind, cmd):
    m = re.search(r"-o (\S+)", cmd)
    if m:
        os.makedirs(os.path.dirname(m.group(1)), exist_ok=True)
    log_ = open(f"{LOGS}/{t.replace(':', '_')}.log", "w")
    full = f"exec nice -n 10 /usr/bin/time -f 'TIME %e %M' bash -c \"{cmd}\""
    p = subprocess.Popen(full, shell=True, env=env, stdout=log_, stderr=subprocess.STDOUT,
                         stdin=subprocess.DEVNULL, start_new_session=True)
    GROUPS.add(p.pid)
    running[t] = (p, time.time(), kind)


def gate_status(mode, av, grow):
    """for the dashboard probe: ~/v9/gate.json (written every 30 s)"""
    ks = {}
    for _, _, k in running.values():
        ks[k] = ks.get(k, 0) + 1
    rec = dict(at=int(time.time()), mode=mode, avail=round(av, 1), grow=round(grow, 1), floor=FLOOR,
               alpha=ALPHA, running=len(running), kinds=ks, oom=n_oom, strict=sorted(strict))
    with open(f"{H}/gate.json.tmp", "w") as f:
        json.dump(rec, f)
    os.replace(f"{H}/gate.json.tmp", f"{H}/gate.json")


while True:
    for t, (p, t0, kind) in list(running.items()):
        if p.poll() is None:
            continue
        del running[t]
        GROUPS.discard(p.pid)
        tl, txt = "", ""
        try:
            txt = open(f"{LOGS}/{t.replace(':', '_')}.log", errors="replace").read()
            tl = [l for l in txt.splitlines() if l.startswith("TIME ")][-1].split()
        except Exception:
            pass
        rc = p.returncode
        rec = dict(task=t, rc=rc, wall=round(time.time() - t0, 1),
                   sec=float(tl[1]) if tl else None, maxrss_kb=int(tl[2]) if tl else None)
        oom = rc != 0 and (t in killed_by_me or rc in (137, -9) or "signal 9" in txt[-2000:])
        if oom:
            n_oom += 1
            kills[t] = kills.get(t, 0) + 1
            by = "driver" if t in killed_by_me else "kernel"
            if kills[t] >= 3:
                rec["oom_final"], rec["by"] = 1, by   # killed again while run alone: a failure
            else:
                rec["oom"], rec["by"] = kills[t], by  # run again (after the second kill: alone, nominal)
        killed_by_me.discard(t)
        log(rec)
        if rc == 0:
            mark(t)
        elif oom and kills[t] < 3:
            if kills[t] == 2:
                strict.add(t)
        else:
            failed.add(t)
    stop = os.path.exists(f"{H}/STOP2" if AFTER else f"{H}/STOP")
    old = AFTER and alive(AFTER)
    if time.time() - DONE_AT > 600 or (AFTER and not old and not old_gone):
        refresh_done()           # the previous driver has just ended: read the certificates it marked
        if AFTER and not old and not old_gone:
            old_gone = True
            if os.path.exists(f"{H}/STOP"):
                os.remove(f"{H}/STOP")   # its stop file; a later plain restart uses STOP again
    todo = [] if stop else [x for x in ready() if x[0] not in running and x[0] not in failed
                            and not (old and x[1] == "cert")]
    if not todo and not running and not old:
        break
    todo.sort(key=lambda x: x[0] not in strict)   # twice-killed tasks first
    now = time.time()
    av = avail_gb()
    an = anon_by_group() if running else {}
    grow = sum(max(0.0, PEAK[k] - an.get(p.pid, 0.0)) for p, _, k in running.values())
    if av < FLOOR and now - last_kill > 3:
        # below the floor: kill the youngest lean task (least work lost, most growth still ahead)
        cand = [(t0, t) for t, (p, t0, k) in running.items() if t not in strict and k in ("def_", "grp", "root")]
        if cand:
            v = max(cand)[1]
            try:
                os.killpg(running[v][0].pid, signal.SIGKILL)
                killed_by_me.add(v)
            except OSError:
                pass
            last_kill = now
            log(dict(task="KILL", victim=v, avail=round(av, 1), grow=round(grow, 1)))
    nominal = any(t in strict for t in running) or any(x[0] in strict for x in todo)
    booked = SHARED + RESERVE + sum(NEED[k] for _, _, k in running.values())
    for t, kind, cmd in todo:
        if len(running) >= slots or av < FLOOR:
            break
        if nominal:
            # a twice-killed task waits (and holds back the others) until it fits the nominal booking,
            # alone: no other twice-killed task runs beside it
            if t in strict and any(s in strict for s in running):
                continue
            if booked + NEED[kind] > MEMT:
                break
            start(t, kind, cmd)
            booked += NEED[kind]
        else:
            if av - ALPHA * grow < FLOOR + PEAK[kind]:
                continue
            if kind == "def_":
                if now - last_start < GAP:
                    continue
                last_start = now
            start(t, kind, cmd)
            grow += PEAK[kind]
        time.sleep(0.05)
    if now - last_gate > 30:
        gate_status("nominal" if nominal else "measured", av, grow)
        last_gate = now
    time.sleep(1)
STOPF = f"{H}/STOP2" if AFTER else f"{H}/STOP"
refresh_done()
left = [i for i in roots if not done(f"root:{i}")]   # e.g. the roots waiting for hand-made certificates
log(dict(task="RUN_END", failed=sorted(failed), stop=os.path.exists(STOPF), left=left))
if not failed and not left and not os.path.exists(STOPF):
    mark(f"ALL_{me}")
