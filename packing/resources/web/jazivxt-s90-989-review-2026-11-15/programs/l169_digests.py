"""Lane L169 digests (after the freeze): the frozen digests, a rerun, and the packet's files.

Usage: l169_digests.py PACKET CERT SCRATCH OUT_JSON

It decides nothing about the certificate. It
1. checks every digest in `frozen/*.txt` against the bytes kept in the packet (the
   source certificate, named `179fcba:n90.cert`, against CERT);
2. reruns the frozen chain into SCRATCH with this interpreter (self-test, check, plan
   facts, plan, controls against the kept plan, description) and compares each receipt
   with the kept one, ignoring only `cpu_seconds` and the plan's `stated_at`;
3. lists the SHA-256 of every file in the packet but OUT_JSON.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

IGNORE = {"cpu_seconds", "stated_at"}


def sha(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def strip(x):
    if isinstance(x, dict):
        return {k: strip(v) for k, v in x.items() if k not in IGNORE}
    if isinstance(x, list):
        return [strip(v) for v in x]
    return x


def main(argv: list[str]) -> int:
    R, cert, X, out_path = (os.path.abspath(a) for a in argv[1:5])
    os.makedirs(X, exist_ok=True)
    out: dict = {"program": "l169_digests.py"}
    checks = []
    for name in sorted(os.listdir(os.path.join(R, "frozen"))):
        if not name.endswith(".txt"):
            continue
        for line in open(os.path.join(R, "frozen", name)):
            if line.startswith("#") or not line.strip():
                continue
            digest, path = line.split(None, 1)
            path = path.strip()
            if path.startswith("179fcba:"):
                target = cert
            elif "/" in path:
                target = os.path.join(R, path)
            else:
                target = os.path.join(R, "programs", path)
            checks.append({"list": name, "path": path, "holds": os.path.exists(target) and sha(target) == digest})
    out["frozen_digests"] = checks
    out["all_frozen_digests_hold"] = all(c["holds"] for c in checks)
    P = os.path.join(R, "programs")
    py = [sys.executable, "-I", "-B"]
    expected = "88c93b2f1d1f3061d1e6815f790d13f3d8f174dd3431f50d8d4d9d4383b3d466"
    runs = [
        ([*py, f"{P}/l169_selftest.py", f"{X}/selftest.json"], "out/selftest.json", "selftest.json"),
        ([*py, f"{P}/l169_check.py", cert, expected, f"{X}/check-n90.json"], "out/check-n90.json", "check-n90.json"),
        ([*py, f"{P}/l169_plan_facts.py", cert, f"{X}/check-n90.json", f"{X}/plan-facts-n90.json"], "out/plan-facts-n90.json", "plan-facts-n90.json"),
        ([*py, f"{P}/l169_make_plan.py", f"{X}/check-n90.json", f"{X}/plan-facts-n90.json", f"{X}/controls-plan.json"], "programs/controls-plan.json", "controls-plan.json"),
        ([*py, f"{P}/l169_controls.py", cert, f"{P}/controls-plan.json", f"{X}/plan-facts-n90.json", f"{X}/check-n90.json", f"{X}/controls-n90.json"], "out/controls-n90.json", "controls-n90.json"),
        ([*py, f"{P}/l169_describe.py", cert, f"{X}/check-n90.json", f"{X}/describe-n90.json"], "out/describe-n90.json", "describe-n90.json"),
    ]
    rerun = []
    for cmd, kept, new in runs:
        r = subprocess.run(cmd, capture_output=True, text=True)
        a = strip(json.load(open(os.path.join(R, kept))))
        b = strip(json.load(open(os.path.join(X, new))))
        rerun.append({"receipt": kept, "exit": r.returncode, "equal_but_cpu_and_time": a == b})
    out["rerun"] = rerun
    out["rerun_reproduces_every_receipt"] = all(x["equal_but_cpu_and_time"] for x in rerun)
    files = []
    for root, _dirs, names in os.walk(R):
        for name in sorted(names):
            p = os.path.join(root, name)
            if os.path.abspath(p) == out_path:
                continue
            files.append([os.path.relpath(p, R), sha(p)])
    out["files"] = sorted(files)
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print("ALL_FROZEN_DIGESTS_HOLD" if out["all_frozen_digests_hold"] else "SOME_FROZEN_DIGEST_DIFFERS",
          f"({len(checks)} digests)")
    print("RERUN_REPRODUCES_EVERY_RECEIPT" if out["rerun_reproduces_every_receipt"] else "RERUN_DIFFERS", rerun)
    return 0 if out["all_frozen_digests_hold"] and out["rerun_reproduces_every_receipt"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
