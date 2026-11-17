"""Run the frozen L70 controls addendum (S4'c, S4'p, S7') on one certificate.

Written after controls-plan-addendum.json was frozen (frozen/controls-plan-digests.txt,
second block). The constructions are l70_controls.py's own (imported unchanged); only
the expectations differ, as the addendum states them.

Usage: python -I l70_controls_addendum.py --src SRC --addendum controls-plan-addendum.json --label LABEL --out RECEIPT
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import l70_check as C  # noqa: E402
import l70_controls as K  # noqa: E402
import l70_reader as R  # noqa: E402

EPS = F(1, 10**30)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--addendum", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args()
    t_start = time.process_time()
    plan = json.loads(Path(ns.addendum).read_text())["files"][ns.label]
    raw = (Path(ns.src) / plan["input"]).read_bytes()
    pk = R.parse_cert_bytes(raw)
    if pk.meta["sha256"] != plan["input_sha256"]:
        raise SystemExit("input differs from the addendum's")
    rows = list(pk.squares)
    idx = {s: k for k, s in enumerate(pk.ids)}
    s4c = next(c for c in plan["controls"] if c["id"] == "S4'c")
    pair_i, pair_j = s4c["what"].split("(")[1].split(")")[0].split(", ")  # S4'p closes the same pair
    results = []
    for ctl in plan["controls"]:
        t0 = time.process_time()
        exp = ctl["expect"]
        cid = ctl["id"]
        if cid in ("S4'c", "S4'p"):
            i, j = pair_i, pair_j
            ri, rj = K.row_xyt(rows[idx[i]]), K.row_xyt(rows[idx[j]])
            lam = K.contact_factor(ri, rj)
            if cid == "S4'p":
                lam *= 1 - EPS
            new_rows = list(rows)
            new_rows[idx[j]] = K.closed_row(ri, rj, lam)
            got = K.summarize(C.decide(K.with_rows(pk, new_rows), keep_near=False))
            ok = (
                got["verdict"] == exp["verdict"]
                and got["agree"]
                and got["touching_A"] == exp["touching_pairs"] == got["touching_B"]
                and got["overlapping_A"] == exp["overlapping_pairs"] == got["overlapping_B"]
                and got["outside_A"] == exp["outside"] == got["outside_B"]
            )
        else:
            si = ctl["what"].split("square ")[1].split(" ")[0]
            corners_rows = []
            for k, r in enumerate(rows):
                x, y, t = K.row_xyt(r)
                c, s = K.basis(t)
                pts = [(x - c / 2 + s / 2, y - s / 2 - c / 2), (x + c / 2 + s / 2, y + s / 2 - c / 2), (x + c / 2 - s / 2, y + s / 2 + c / 2), (x - c / 2 - s / 2, y - s / 2 + c / 2)]
                if pk.ids[k] == si:
                    g = 1 + EPS
                    pts = [(x + g * (px - x), y + g * (py - y)) for px, py in pts]
                v: list[int] = []
                for px, py in pts:
                    v.extend(K.ints(px) + K.ints(py))
                corners_rows.append(tuple(v))
            cpk = R.Packing(n=pk.n, side=pk.side, kind="corners", squares=tuple(corners_rows), ids=pk.ids)
            got = K.summarize(C.decide(cpk, keep_near=False))
            ok = (
                got["verdict"] == "REFUSE"
                and got["not_unit_A"] == exp["not_unit"] == got["not_unit_B"]
                and got["outside_A"] == exp["outside_A"]
                and got["outside_B"] == exp["outside_B"]
                and got["overlapping_A"] == [] == got["overlapping_B"]
            )
        results.append({"id": cid, "what": ctl["what"], "expect": exp, "got": got, "as_stated": bool(ok), "cpu_seconds": round(time.process_time() - t0, 3)})
        print(ns.label, cid, "AS STATED" if ok else "MISSED", flush=True)
    out = {
        "program": "l70_controls_addendum.py",
        "program_digests": C.file_digests(C.CHECKER_FILES + ("l70_controls.py", "l70_controls_addendum.py", "controls-plan-addendum.json")),
        "label": ns.label,
        "input_sha256": pk.meta["sha256"],
        "controls": results,
        "every_control_as_stated": all(r["as_stated"] for r in results),
        "cpu_seconds": round(time.process_time() - t_start, 3),
    }
    Path(ns.out).write_text(json.dumps(out, indent=1) + "\n")
    print(ns.label, "EVERY_CONTROL_AS_STATED" if out["every_control_as_stated"] else "MISSED", "cpu", out["cpu_seconds"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
