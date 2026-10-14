"""A241 -- the WINDOW statement for A55's exact k <= 4 kills.

A55 certified k3_00 and eight k4 classes with `case-measure-certificate-v1` PASSes AT s0.
`closed_disjoint_bridge.md` B.2 is brutal about what that buys: the corpus containment margin is
rho ~ 1.0e-9 with A = 5/2, so (H') reads s''/m - 1 < 4.0e-10 -- an s0-only certificate kills at NO
side of the window [3.82, s-hat].  That is exactly why `classes178.forced_cells` refuses to use the
eight k4 kills and why every k <= 3 class has 0 usable forced cells (A238 results/forced238.md).

So the window statement is NOT bookkeeping: it is A56's parametric layer, re-run on A55's base
certificates.  This module is the campaign runner, one class at a time (>= 2 of my own python
processes is the ops cap, and the driver is one of them):

    make_param   base -> parametric-kill-certificate-v1 (nearest-wall anchoring; --beta-mid retry)
    stage 0      specialise at 191/50, run the UNMODIFIED A53 verify_case.py  (the cheap gate: a
                 certificate that fails at the far endpoint cannot transfer with that anchoring)
    4D           verify_param.py over [191/50, 969271/250000]
    canary C2    verify_case.py on the specialisations at 191/50, midpoint, s0 -- all three PASS

A row counts as TRANSFERRED (i.e. is allowed onto the scoreboard by rowcascade241.py) only with
stage0 PASS + 4D PASS + C2 3/3.  Resume-safe: every row is appended to results/param241.jsonl as
soon as it is known and a finished class is never re-run.

    python param241.py [--only k4_07,k4_10] [--depth 48] [--wall 5400] [--force]
"""
import argparse
import json
import os
import subprocess
import sys
import time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
A241 = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(A241, "..", ".."))
ATT = os.path.join(ROOT, "attempts")
A56 = os.path.join(ATT, "A56-sparametric", "code")
MAKE_PARAM = os.path.join(A56, "make_param.py")
SPECIALIZE = os.path.join(A56, "specialize.py")
VERIFY_PARAM = os.path.join(A56, "verify_param.py")
VERIFY_CASE = os.path.join(ATT, "A53-simple-strata", "code", "verify_case.py")
CERTS = os.path.join(A241, "certs")
RESULTS = os.path.join(A241, "results")
LOGS = os.path.join(A241, "logs")
ROWS = os.path.join(RESULTS, "param241.jsonl")

S0 = F(969271, 250000)
S_LO = F(191, 50)
S_MID = (S0 + S_LO) / 2

A55 = os.path.join(ATT, "A55-k4-sweep")
# (class, base certificate, the A55 provenance line that the scoreboard row will cite)
TARGETS = [
    ("k4_07", os.path.join(A55, "certs", "k4_07.json"), "A55 certs/k4_07.json (PASS, 12 atoms)"),
    ("k4_10", os.path.join(A55, "certs", "k4_10.json"), "A55 certs/k4_10.json (PASS, 13 atoms)"),
    ("k4_12", os.path.join(A55, "certs", "k4_12.json"), "A55 certs/k4_12.json (PASS, 77 atoms)"),
    ("k4_02", os.path.join(A55, "certs", "k4_02.json"), "A55 certs/k4_02.json (PASS, 185 atoms)"),
    ("k4_04", os.path.join(A55, "certs", "k4_04.json"), "A55 certs/k4_04.json (PASS, 205 atoms)"),
    ("k4_00", os.path.join(A55, "certs", "k4_00.json"), "A55 certs/k4_00.json (PASS, 433 atoms)"),
    ("k4_01", os.path.join(A55, "certs", "k4_01.json"), "A55 certs/k4_01.json (PASS, 501 atoms)"),
    ("k4_09", os.path.join(A55, "certs", "k4_09.json"), "A55 certs/k4_09.json (PASS, 531 atoms)"),
    ("k3_00", os.path.join(A55, "k3_ext", "certs", "k3_00.json"), "A55/k3_ext certs/k3_00.json (PASS, 579 atoms)"),
]


def be_polite(mask=0xFFFF):
    """BelowNormal + affinity on THIS process; on Windows a child inherits both, so every
    verify_case / verify_param subprocess below is launched polite without touching it."""
    try:
        import ctypes
        h = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.kernel32.SetPriorityClass(h, 0x00004000)                  # BELOW_NORMAL
        ctypes.windll.kernel32.SetProcessAffinityMask(h, mask)
    except Exception as e:                                                      # noqa: BLE001
        print("be_polite: %r" % (e,), flush=True)


def sh(cmd, log, timeout=None):
    os.makedirs(os.path.dirname(log), exist_ok=True)
    t0 = time.time()
    with open(log, "a", encoding="utf-8") as fh:
        fh.write("\n$ " + " ".join(str(c) for c in cmd) + "\n")
        fh.flush()
        try:
            rc = subprocess.run([str(c) for c in cmd], stdout=fh, stderr=subprocess.STDOUT,
                                timeout=timeout).returncode
        except subprocess.TimeoutExpired:
            fh.write("*** TIMEOUT after %ss\n" % timeout)
            rc = 124
    return rc, round(time.time() - t0, 1)


def done():
    out = {}
    if os.path.exists(ROWS):
        for ln in open(ROWS, encoding="utf-8"):
            ln = ln.strip()
            if ln:
                r = json.loads(ln)
                out[r["name"]] = r
    return out


def emit(row):
    os.makedirs(RESULTS, exist_ok=True)
    with open(ROWS, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


# A56 sweep.py's anchoring ladder (soundness.md P3: the anchoring is a COMPLETENESS choice only,
# never soundness -- a bad anchoring can only make the verification FAIL).
LADDER = [("gap", ["--beta-gap", "19/10,27/10"]),
          ("nearest-wall", []),
          ("mid-band", ["--beta-mid"])]


def one(name, base, prov, depth, wall):
    log = os.path.join(LOGS, "%s.log" % name)
    rep = os.path.join(CERTS, "%s.param.report.json" % name)
    row = dict(name=name, base=os.path.relpath(base, ROOT), provenance=prov,
               window=[str(S_LO), str(S0)], depth=depth, started=time.strftime("%Y-%m-%dT%H:%M:%S"),
               stage0=[], anchoring_tried=[])
    ok = []
    for anchoring, extra in LADDER:                                             # the cheap far-endpoint gate
        par = os.path.join(CERTS, "%s.%s.param.json" % (name, anchoring))
        rc, t = sh([sys.executable, MAKE_PARAM, base, "-o", par, "--name", name] + extra, log)
        if rc:
            row["stage0"].append(dict(anchoring=anchoring, result="MAKE-FAIL", rc=rc))
            continue
        sp = os.path.join(CERTS, "%s.%s.at_slo.json" % (name, anchoring))
        rc, _ = sh([sys.executable, SPECIALIZE, par, "--s", str(S_LO), "-o", sp], log)
        if rc:
            row["stage0"].append(dict(anchoring=anchoring, result="SPECIALIZE-FAIL"))
            continue
        rc, t = sh([sys.executable, VERIFY_CASE, sp, "--depth", depth], log, timeout=wall)
        row["stage0"].append(dict(anchoring=anchoring, result="PASS" if rc == 0 else "FAIL",
                                  rc=rc, time_s=t))
        if rc == 0:
            ok.append((anchoring, par))
    if not ok:
        row.update(result="ANCHORING-OPEN",
                   note="fails already at the far endpoint s = 191/50 with every anchoring")
        return row
    for anchoring, par in ok:                                                   # the real 4D run
        rc, t = sh([sys.executable, VERIFY_PARAM, par, "--slo", str(S_LO), "--shi", str(S0),
                    "--depth", depth, "--report", rep], log, timeout=wall)
        row["anchoring_tried"].append(dict(anchoring=anchoring, rc=rc, time_s=t))
        if rc == 0:
            row.update(anchoring=anchoring, param_rc=0, param_time_s=t,
                       parametric_cert=os.path.relpath(par, ROOT))
            break
    else:
        last = row["anchoring_tried"][-1]
        row.update(result={1: "PARAM-FAIL", 124: "PARAM-TIMEOUT"}.get(last["rc"], "PARAM-ERR"),
                   param_time_s=sum(a["time_s"] for a in row["anchoring_tried"]))
        if os.path.exists(rep):
            try:
                r = json.load(open(rep, encoding="utf-8"))
                row["witness_s_range"] = r.get("witness_s_range")
                row["param_stats"] = r.get("stats")
            except Exception:                                                   # noqa: BLE001
                pass
        return row
    par = os.path.join(CERTS, "%s.%s.param.json" % (name, row["anchoring"]))
    if os.path.exists(rep):
        try:
            row["param_stats"] = json.load(open(rep, encoding="utf-8")).get("stats")
        except Exception:                                                       # noqa: BLE001
            pass
    c2 = []
    for s in (S_LO, S_MID, S0):
        sp = os.path.join(CERTS, "%s.at_%s.json" % (name, str(s).replace("/", "_")))
        rc0, _ = sh([sys.executable, SPECIALIZE, par, "--s", str(s), "-o", sp], log)
        rc1, t1 = sh([sys.executable, VERIFY_CASE, sp, "--depth", depth], log, timeout=wall)
        c2.append(dict(s=str(s), s_float=round(float(s), 6), result="PASS" if (rc0 == 0 and rc1 == 0) else "FAIL",
                       time_s=t1))
    row["c2"] = c2
    row["result"] = "TRANSFERRED" if all(c["result"] == "PASS" for c in c2) else "C2-FAIL"
    return row


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    ap.add_argument("--depth", default="48")
    ap.add_argument("--wall", type=int, default=5400)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    be_polite()
    os.makedirs(CERTS, exist_ok=True)
    os.makedirs(LOGS, exist_ok=True)
    want = set(a.only.split(",")) if a.only else None
    have = {} if a.force else done()
    for name, base, prov in TARGETS:
        if want and name not in want:
            continue
        if name in have and have[name].get("result") == "TRANSFERRED":
            print("%-7s already TRANSFERRED" % name, flush=True)
            continue
        if not os.path.exists(base):
            emit(dict(name=name, result="NO-BASE", base=base))
            continue
        t0 = time.time()
        row = one(name, base, prov, a.depth, a.wall)
        row["wall_s"] = round(time.time() - t0, 1)
        emit(row)
        print("%-7s %-14s %6.0fs" % (name, row["result"], row["wall_s"]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
