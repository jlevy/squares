"""Lane L180: decide de Winter's n = 90 certificate and its twin, every square, wall and pair.

Written for the blind stage 4 review of issue #996 as a clean-room implementation.
It imports nothing from this repository or the source, and reuses no code of any
earlier review.

Usage: l180_check.py JSON SHA256 TWIN SHA256 OUT

It refuses files whose SHA-256 is not the one stated, reads both strictly, decides
that the twin holds exactly the JSON's packing, then decides the packing by method A
(the JSON's poses) and method B (the twin's corners), and writes the receipt.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l180_decide as D  # noqa: E402
import l180_reader as R  # noqa: E402


def sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(__doc__)
        return 2
    jpath, jsha, tpath, tsha, out = argv[1:]
    t0 = time.process_time()
    got = {"json": sha256(jpath), "twin": sha256(tpath)}
    if got["json"] != jsha or got["twin"] != tsha:
        print(f"DIGEST MISMATCH {got}")
        return 1
    r = R.read_json(jpath)
    t = R.read_twin(tpath)
    twin = R.compare_twin(r, t)
    corners = list(t.corners)
    d = D.decide(r.n, r.side, r.poses, corners)
    s = D.summary(d)
    verdict = "ACCEPT" if (d.verdict == "ACCEPT" and twin["agree"]) else "REFUSE"
    receipt = {
        "program": "l180_check.py",
        "lane": "L180",
        "inputs": {"json": {"path": os.path.basename(jpath), "sha256": got["json"]}, "twin": {"path": os.path.basename(tpath), "sha256": got["twin"]}},
        "verdict": verdict,
        "reading": {
            "n": r.n,
            "side": r.side_text,
            "format": r.format_text,
            "json_scalars": 2 + 4 * r.n,
            "twin_scalars": 1 + 8 * t.n,
            "twin_envelope": t.envelope,
            "twin_header": t.header,
        },
        "twin": twin,
        "decision": s,
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=False)
        fh.write("\n")
    ls = s.get("least_positive_margin", {})
    print(
        f"{verdict}: n={r.n}, twin agree={twin['agree']}, pairs={s.get('pairs')}, "
        f"classes A={s.get('pair_classes', {}).get('A')}, walls A={s.get('wall_classes', {}).get('A')}, "
        f"least positive margin {ls.get('approx')} at {ls.get('pair')}, wall contacts {s.get('wall_contacts')}"
    )
    return 0 if verdict == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
