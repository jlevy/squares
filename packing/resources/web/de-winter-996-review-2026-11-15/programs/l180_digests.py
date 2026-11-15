"""Lane L180, after the freeze: hold the frozen digests, rerun the frozen chain, list the packet.

Written for the blind stage 4 review of issue #996. It decides nothing about the bound.

1. Every digest in ``frozen/*.txt`` is checked against the bytes kept here (and the
   source files against the clone).
2. The frozen chain (self-test, check, plan facts, plan, controls, description) is rerun
   into SCRATCH with the kept programs, the controls reading the kept plan, and each
   receipt is compared with the kept one, CPU seconds aside (the rerun plan is compared
   with the kept plan too).
3. The SHA-256 of every file in the packet is listed.

Usage: l180_digests.py PACKET SOURCE_N90_DIR SCRATCH OUT
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from typing import Any


def sha(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def strip_cpu(path: str) -> Any:
    with open(path, encoding="utf-8") as fh:
        obj = json.load(fh)

    def walk(o: Any) -> Any:
        if isinstance(o, dict):
            return {k: walk(v) for k, v in o.items() if k != "cpu_seconds"}
        if isinstance(o, list):
            return [walk(v) for v in o]
        return o

    return walk(obj)


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(__doc__)
        return 2
    pk, src, scratch, out = argv[1:]
    os.makedirs(scratch, exist_ok=True)
    res: dict[str, Any] = {"program": "l180_digests.py", "lane": "L180"}
    held: dict[str, bool] = {}
    for name in sorted(os.listdir(os.path.join(pk, "frozen"))):
        if not name.endswith(".txt"):
            continue
        with open(os.path.join(pk, "frozen", name), encoding="utf-8") as fh:
            for line in fh:
                m = re.fullmatch(r"([0-9a-f]{64})  (\S+)\n?", line)
                if not m:
                    continue
                digest, rel = m.groups()
                if rel.startswith("64d5ee7:n90/"):
                    path = os.path.join(src, rel.split("/", 1)[1])
                elif "/" in rel:
                    path = os.path.join(pk, rel)
                else:
                    path = os.path.join(pk, "programs", rel)
                held[f"{name}: {rel}"] = os.path.exists(path) and sha(path) == digest
    res["frozen_digests"] = held
    res["all_frozen_digests_hold"] = all(held.values())
    py = [sys.executable, "-I", "-B"]
    pg = os.path.join(pk, "programs")
    j = os.path.join(src, "n90_exact.json")
    t = os.path.join(src, "n90_witness.yaml")
    s = scratch
    steps = [
        [f"{pg}/l180_selftest.py", f"{s}/selftest.json"],
        [f"{pg}/l180_check.py", j, sha(j), t, sha(t), f"{s}/check-n90.json"],
        [f"{pg}/l180_plan_facts.py", j, t, f"{s}/check-n90.json", f"{s}/plan-facts-n90.json"],
        [f"{pg}/l180_make_plan.py", f"{s}/check-n90.json", f"{s}/plan-facts-n90.json", f"{s}/controls-plan.json"],
        [f"{pg}/l180_controls.py", j, t, f"{pg}/controls-plan.json", f"{s}/plan-facts-n90.json", f"{s}/check-n90.json", f"{s}/controls-n90.json"],
        [f"{pg}/l180_describe.py", j, f"{s}/check-n90.json", f"{s}/describe-n90.json"],
    ]
    runs = []
    for step in steps:
        p = subprocess.run([*py, *step], capture_output=True, text=True, check=False)
        runs.append({"program": os.path.basename(step[0]), "exit": p.returncode})
    res["rerun_exits"] = runs
    same: dict[str, bool] = {}
    for name in ("selftest.json", "check-n90.json", "plan-facts-n90.json", "controls-n90.json", "describe-n90.json"):
        same[name] = strip_cpu(os.path.join(pk, "out", name)) == strip_cpu(os.path.join(s, name))
    same["controls-plan.json"] = sha(os.path.join(pk, "programs", "controls-plan.json")) == sha(os.path.join(s, "controls-plan.json"))
    res["rerun_equals_kept"] = same
    res["rerun_reproduces_every_receipt"] = all(same.values()) and all(r["exit"] == 0 for r in runs)
    listing = {}
    for root, _dirs, files in os.walk(pk):
        for f in sorted(files):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, pk)
            if rel == os.path.join("out", "program-digests.json"):
                continue
            listing[rel] = sha(full)
    res["packet_files"] = dict(sorted(listing.items()))
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(
        f"{'ALL_FROZEN_DIGESTS_HOLD' if res['all_frozen_digests_hold'] else 'A FROZEN DIGEST FAILS'} ({len(held)} digests); "
        f"{'RERUN_REPRODUCES_EVERY_RECEIPT' if res['rerun_reproduces_every_receipt'] else 'RERUN DIFFERS'} {same}"
    )
    return 0 if res["all_frozen_digests_hold"] and res["rerun_reproduces_every_receipt"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
