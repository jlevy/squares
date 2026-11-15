"""Lane L182: hold every frozen digest, rerun the addendum's chain, list the addendum's files.

Written for the addendum to lane L180's blind stage 4 review of issue #996, on #997's
replacement certificate. It decides nothing about the bound.

1. Every digest in L180's three frozen lists (``../frozen/*.txt``) is checked against the
   bytes kept in L180's packet, and its two source files against #996's certificate
   (64d5ee7); every digest in this addendum's plan list (``frozen/controls-plan-digest.txt``)
   against the bytes kept here, and its source files against #997's certificate
   (fa53fb0).
2. The addendum's chain (L180's self-test, check, controls and description, unchanged;
   L182's plan facts and plan; L182's comparison and arithmetic) is rerun into SCRATCH,
   the controls reading the kept plan, and each receipt is compared with the kept one,
   CPU seconds aside; the rerun plan is compared byte for byte.
3. The SHA-256 of every file under ``programs/``, ``out/`` and ``frozen/`` here is listed.

Usage: l182_digests.py ADDENDUM SOURCE_997_N90 SOURCE_996_N90 FRONTIER HOUSE SCRATCH OUT
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


def hold(listing: str, base: str, sources: dict[str, str]) -> dict[str, bool]:
    held: dict[str, bool] = {}
    with open(listing, encoding="utf-8") as fh:
        for line in fh:
            m = re.fullmatch(r"([0-9a-f]{64})  (\S+)\n?", line)
            if not m:
                continue
            digest, rel = m.groups()
            prefix = next((p for p in sources if rel.startswith(p)), None)
            if prefix is not None:
                path = os.path.join(sources[prefix], rel[len(prefix) :])
            elif "/" in rel:
                path = os.path.normpath(os.path.join(base, rel))
            else:
                path = os.path.join(base, "programs", rel)
            held[f"{os.path.basename(listing)}: {rel}"] = os.path.exists(path) and sha(path) == digest
    return held


def main(argv: list[str]) -> int:
    if len(argv) != 8:
        print(__doc__)
        return 2
    ad, src7, src6, frontier, house, scratch, out = argv[1:]
    os.makedirs(scratch, exist_ok=True)
    l180 = os.path.normpath(os.path.join(ad, ".."))
    res: dict[str, Any] = {"program": "l182_digests.py", "lane": "L182"}
    held: dict[str, bool] = {}
    for name in sorted(os.listdir(os.path.join(l180, "frozen"))):
        if name.endswith(".txt"):
            held.update(hold(os.path.join(l180, "frozen", name), l180, {"64d5ee7:n90/": src6}))
    held_l180 = dict(held)
    held.update(hold(os.path.join(ad, "frozen", "controls-plan-digest.txt"), ad, {"fa53fb0:n90/": src7}))
    res["frozen_digests"] = held
    res["l180_frozen_digests_hold"] = all(held_l180.values()) and len(held_l180) > 0
    res["all_frozen_digests_hold"] = all(held.values())

    py = [sys.executable, "-I", "-B"]
    lp = os.path.join(l180, "programs")
    pg = os.path.join(ad, "programs")
    o = os.path.join(ad, "out")
    j, t = os.path.join(src7, "n90_exact.json"), os.path.join(src7, "n90_witness.yaml")
    j6 = os.path.join(src6, "n90_exact.json")
    s = scratch
    steps = [
        [f"{lp}/l180_selftest.py", f"{s}/selftest.json"],
        [f"{lp}/l180_check.py", j, sha(j), t, sha(t), f"{s}/check-n90-997.json"],
        [f"{pg}/l182_plan_facts.py", j, t, f"{s}/check-n90-997.json", f"{s}/plan-facts-l180-rules.json", f"{s}/plan-facts-n90-997.json"],
        [f"{pg}/l182_make_plan.py", f"{s}/check-n90-997.json", f"{s}/plan-facts-n90-997.json", f"{lp}/controls-plan.json", f"{s}/controls-plan-l180-rules.json", f"{s}/controls-plan-997.json"],
        [f"{lp}/l180_controls.py", j, t, f"{pg}/controls-plan-997.json", f"{s}/plan-facts-n90-997.json", f"{s}/check-n90-997.json", f"{s}/controls-n90-997.json"],
        [f"{lp}/l180_describe.py", j, f"{s}/check-n90-997.json", f"{s}/describe-n90-997.json"],
        [f"{pg}/l182_compare.py", j, j6, f"{s}/check-n90-997.json", f"{l180}/out/check-n90.json", f"{s}/compare-997-996.json"],
        [
            f"{pg}/l182_sides.py", j, j6, f"{s}/describe-n90-997.json", frontier, house,
            f"{o}/contraction-t303-house-n90-997.json", f"{o}/contraction-new-n90-997.json", f"{o}/contraction-996-against-997.json", f"{s}/sides-997.json",
        ],
    ]
    runs = []
    for step in steps:
        p = subprocess.run([*py, *step], capture_output=True, text=True, check=False)
        runs.append({"program": os.path.basename(step[0]), "exit": p.returncode})
    res["rerun_exits"] = runs
    same: dict[str, bool] = {}
    for name in ("selftest.json", "check-n90-997.json", "plan-facts-n90-997.json", "controls-n90-997.json", "describe-n90-997.json", "compare-997-996.json", "sides-997.json"):
        same[name] = strip_cpu(os.path.join(o, name)) == strip_cpu(os.path.join(s, name))
    same["controls-plan-997.json"] = sha(os.path.join(pg, "controls-plan-997.json")) == sha(os.path.join(s, "controls-plan-997.json"))
    res["rerun_equals_kept"] = same
    res["rerun_reproduces_every_receipt"] = all(same.values()) and all(r["exit"] == 0 for r in runs)
    listing = {}
    for sub in ("programs", "out", "frozen"):
        for f in sorted(os.listdir(os.path.join(ad, sub))):
            rel = f"{sub}/{f}"
            if rel in ("out/addendum-digests.json", "frozen/addendum-frozen-digests.txt"):
                continue
            listing[rel] = sha(os.path.join(ad, rel))
    res["addendum_files"] = listing
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(
        f"{'ALL_FROZEN_DIGESTS_HOLD' if res['all_frozen_digests_hold'] else 'A FROZEN DIGEST FAILS'} ({len(held)} digests, L180's {len(held_l180)}); "
        f"{'RERUN_REPRODUCES_EVERY_RECEIPT' if res['rerun_reproduces_every_receipt'] else 'RERUN DIFFERS'} {same} {runs}"
    )
    return 0 if res["all_frozen_digests_hold"] and res["rerun_reproduces_every_receipt"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
