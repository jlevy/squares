"""Lane L186, after the freeze: the author's printed outputs against this lane's receipts.

Usage: python -I -B l186_author_outputs.py VERIFY.txt CHECK_OUTPUT.txt OUT.json CHECK_n127.json ...

Reads `packing-witness-verify.txt` and `check-output.txt` as text (the author's outputs,
not run here) and compares each count's printed side, verdict and pair count with this
lane's check receipts. Decides nothing.
"""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction
from typing import Any


def main() -> None:
    verify_path, check_out_path, out_path = sys.argv[1:4]
    receipts = {}
    for p in sys.argv[4:]:
        with open(p) as fh:
            r = json.load(fh)
        receipts[str(r["reader"]["n"])] = r
    verify = open(verify_path, encoding="utf-8").read()
    blocks = re.split(r"^\$ packing-witness verify ", verify, flags=re.M)[1:]
    vrows: dict[str, Any] = {}
    for b in blocks:
        n = re.search(r"^  n: (\d+)$", b, re.M)
        side = re.search(r"^  side: (\S+)$", b, re.M)
        pairs = re.search(r"^  pairs tested: (\d+)$", b, re.M)
        first = b.splitlines()[1].strip() if len(b.splitlines()) > 1 else ""
        if n and side and pairs:
            vrows[n.group(1)] = {"verdict": first, "side": side.group(1), "pairs": int(pairs.group(1))}
    crow: dict[str, Any] = {}
    for line in open(check_out_path, encoding="utf-8"):
        m = re.match(r"(VALID|INVALID) n-(\d+)-candidate\.yaml: n \d+, side (\S+) .*?, (\d+) pairs", line)
        if m:
            crow[m.group(2)] = {"verdict": m.group(1), "side_float": m.group(3), "pairs": int(m.group(4))}
    out: dict[str, Any] = {}
    for n, r in receipts.items():
        S = Fraction(r["side"]["exact"])
        v = vrows.get(n, {})
        c = crow.get(n, {})
        out[n] = {
            "verify_verdict": v.get("verdict"),
            "verify_side_equals_exact_side": v.get("side") is not None and Fraction(v["side"]) == S,
            "verify_pairs": v.get("pairs"),
            "check_py_verdict": c.get("verdict"),
            "check_py_side_float": c.get("side_float"),
            "check_py_side_float_equals_float_of_side": c.get("side_float") is not None
            and float(c["side_float"]) == float(S),
            "check_py_pairs": c.get("pairs"),
            "pairs_here": r["decision"]["pairs"]["decided"],
        }
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    for n, v in out.items():
        print(n, v)


if __name__ == "__main__":
    main()
