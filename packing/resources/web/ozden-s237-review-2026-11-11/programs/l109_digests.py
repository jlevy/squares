"""Lane L109's digest check: every program and receipt against the kept bytes and freezes.

Usage: python -I -B l109_digests.py PACKET_DIR OUT.json

Decides nothing about the packing. Checks that each file the three frozen lists name
still has the digest the list recorded (the receipts' later reruns aside: the frozen
receipts are compared as kept); that every receipt recording its programs' SHA-256 names
the bytes kept here; and lists the SHA-256 of every file in the directory. It prints
ALL_RECEIPTS_MATCH when everything holds.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys


def sha(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def frozen_list(path: str, base: str) -> list[tuple[str, str]]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            digest, name = line.split(None, 1)
            name = name.strip()
            full = os.path.normpath(os.path.join(base, name))
            rows.append((digest, full))
    return rows


def main() -> int:
    packet, out = sys.argv[1], sys.argv[2]
    prog = os.path.join(packet, "programs")
    problems: list[str] = []
    checked = 0
    for lst, base in (
        ("frozen/checker-frozen-digests.txt", prog),
        ("frozen/controls-plan-digest.txt", packet),
        ("frozen/findings-frozen-digest.txt", packet),
    ):
        for digest, full in frozen_list(os.path.join(packet, lst), base):
            checked += 1
            if sha(full) != digest:
                problems.append(f"{lst}: {os.path.relpath(full, packet)} differs")
    receipts = {}
    for name in sorted(os.listdir(os.path.join(packet, "out"))):
        path = os.path.join(packet, "out", name)
        receipts[name] = sha(path)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            continue
        for pname, digest in (data.get("programs_sha256") or {}).items():
            checked += 1
            if sha(os.path.join(prog, pname)) != digest:
                problems.append(f"out/{name}: {pname} is not the kept program")
    programs = {name: sha(os.path.join(prog, name)) for name in sorted(os.listdir(prog))}
    frozen = {name: sha(os.path.join(packet, "frozen", name)) for name in sorted(os.listdir(os.path.join(packet, "frozen")))}
    verdict = "ALL_RECEIPTS_MATCH" if not problems else "MISMATCH"
    receipt = {
        "program": "l109_digests.py",
        "verdict": verdict,
        "checks": checked,
        "problems": problems,
        "programs": programs,
        "receipts": receipts,
        "frozen": frozen,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=1)
        f.write("\n")
    print(verdict, f"{checked} checks", problems[:5])
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
