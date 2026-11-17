"""Lane L163 digests, after the freeze: the frozen lists against the kept bytes, a rerun
of the frozen chain against the kept receipts, and the digest of every file here.

Usage: l163_digests.py PACKET SOURCE_RUN_DIR RERUN_DIR OUT.json

SOURCE_RUN_DIR is the clone's `runs/2026-11-11_fable-5.2/`, against which the frozen
list's source lines are checked. RERUN_DIR holds the frozen chain's receipts written
again after the freeze; each must equal the kept one in everything but `cpu_seconds`.
Decides nothing.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

CHAIN = [
    "selftest.json",
    "check-n228.json",
    "check-n147.json",
    "plan-facts-n228.json",
    "plan-facts-n147.json",
    "controls-n228.json",
    "controls-n147.json",
    "describe-n228.json",
    "describe-n147.json",
]


def sha(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def strip(x: object) -> object:
    if isinstance(x, dict):
        return {k: strip(v) for k, v in x.items() if k != "cpu_seconds"}  # pyright: ignore[reportUnknownVariableType]
    if isinstance(x, list):
        return [strip(v) for v in x]  # pyright: ignore[reportUnknownVariableType]
    return x


def main() -> None:
    packet, source, rerun, out = sys.argv[1:5]
    rec: dict[str, object] = {"lane": "L163", "program": "l163_digests.py"}
    lists = {}
    bad: list[str] = []
    for name in ("checker-frozen-digests.txt", "controls-plan-digest.txt", "findings-frozen-digest.txt"):
        checked = 0
        for line in open(os.path.join(packet, "frozen", name), encoding="utf-8"):
            if line.startswith("#") or not line.strip():
                continue
            digest, rel = line.split()
            if rel.startswith("fce076f:"):
                path = os.path.join(source, rel.split(":", 1)[1])
            elif "/" in rel:
                path = os.path.join(packet, rel)
            else:
                path = os.path.join(packet, "programs", rel)
            checked += 1
            if sha(path) != digest:
                bad.append(f"{name}: {rel}")
        lists[name] = {"entries": checked, "sha256": sha(os.path.join(packet, "frozen", name))}
    rec["frozen_lists"] = lists
    rec["frozen_mismatches"] = bad
    reruns = {}
    for name in CHAIN:
        kept = json.load(open(os.path.join(packet, "out", name), encoding="utf-8"))
        again = json.load(open(os.path.join(rerun, name), encoding="utf-8"))
        reruns[name] = strip(kept) == strip(again)
    plan_same = sha(os.path.join(rerun, "controls-plan.json")) == sha(os.path.join(packet, "programs", "controls-plan.json"))
    rec["rerun_equal_but_cpu"] = reruns
    rec["rerun_plan_byte_for_byte"] = plan_same
    files = {}
    for root, _, names in os.walk(packet):
        for nm in sorted(names):
            p = os.path.join(root, nm)
            rel = os.path.relpath(p, packet)
            if rel in ("out/program-digests.json", "README.md"):
                continue
            files[rel] = sha(p)
    rec["files"] = dict(sorted(files.items()))
    rec["summary"] = [
        "ALL_FROZEN_DIGESTS_HOLD" if not bad else "SOME_FROZEN_DIGEST_FAILS",
        "RERUN_REPRODUCES_EVERY_RECEIPT" if all(reruns.values()) and plan_same else "RERUN_DIFFERS",
    ]
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1)
    print(rec["summary"], {k: v["entries"] for k, v in lists.items()}, bad, reruns)


if __name__ == "__main__":
    main()
