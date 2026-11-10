"""Decide a Witness/v2 corner file (and optionally its JSON twin) with both methods.

Run: python -I -B l77_check.py WITNESS.yaml [TWIN.json] OUT.json
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l77_checker as C  # noqa: E402


def sha(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main() -> int:
    args = sys.argv[1:]
    if len(args) not in (2, 3):
        print(__doc__)
        return 2
    path, out = args[0], args[-1]
    twin = args[1] if len(args) == 3 else None
    t0 = time.process_time()
    receipt: dict = {
        "program": "l77_check.py",
        "program_sha256": sha(__file__),
        "checker_sha256": sha(os.path.join(HERE, "l77_checker.py")),
        "file": os.path.basename(path),
    }
    try:
        w = C.read_witness(path)
    except C.Refused as e:
        receipt.update(verdict="REFUSE", reader="refused", reason=str(e))
        json.dump(receipt, open(out, "w"), indent=1)
        print("REFUSE (reader)", e)
        return 1
    receipt.update(
        sha256=w["sha256"],
        bytes=w["bytes"],
        ends_with_newline=w["ends_with_newline"],
        witness_id=w["id"],
        n=w["n"],
        ids_in_order=w["ids_in_order"],
        scalars_read=1 + 8 * w["n"],
    )
    if twin is not None:
        try:
            j = C.read_witness_json(twin)
            receipt["twin"] = {
                "file": os.path.basename(twin),
                "sha256": j["sha256"],
                "bytes": j["bytes"],
                "ends_with_newline": j["ends_with_newline"],
                "same_plain_tree": j["plain"] == w["plain"],
                "same_side_and_corners": j["side"] == w["side"] and j["corners"] == w["corners"]
                and j["ids"] == w["ids"],
            }
        except C.Refused as e:
            receipt["twin"] = {"file": os.path.basename(twin), "refused": str(e)}
    r = C.decide(w["side"], w["corners"], w["ids"])
    receipt.update(r)
    receipt["cpu_seconds"] = round(time.process_time() - t0, 1)
    with open(out, "w") as fh:
        json.dump(receipt, fh, indent=1)
        fh.write("\n")
    print(receipt["verdict"], "n", r["n"], "pairs", r["pairs_decided"], "cpu", receipt["cpu_seconds"])
    return 0 if r["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main())
