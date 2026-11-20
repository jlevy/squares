"""Lane rR1-lower: the exact premises of all 77 standalone certificates, and the premise
controls P1 to P5 of the frozen plan.

Usage: rr1_premises.py --root SRC_FOLDER --scratch DIR --out FILE [--control-label 1042/n136]
"""

from __future__ import annotations

import argparse
import copy
import csv
import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rr1_common as C  # noqa: E402
import rr1_search as S  # noqa: E402


def claimed(root: Path) -> dict:
    out = {}
    with open(root / "lower_bounds.csv") as f:
        for row in csv.DictReader(f):
            out[f"1041/n{row['n']}"] = F(row["new_exact"])
    with open(root / "followup/best_by_count.csv") as f:
        for row in csv.DictReader(f):
            if row["method"] == "standalone certificate":
                out[f"1042/n{row['n']}"] = F(row["exact"])
    return out


def premises(cert: dict, claim: F | None) -> dict:
    probs: list[str] = []
    man = cert["manifest"]
    n = int(man["n"])
    side = C.rat(man["side"])
    base = cert["base"]
    rows = base["rows"]
    L = base["L"]
    for lv in cert["levels"]:
        m = lv["measure"]
        if m["n"] != n:
            probs.append(f"level {lv['K']}: n {m['n']} != {n}")
        if m["L"] != side:
            probs.append(f"level {lv['K']}: L != side")
        if m["points"]:
            probs.append(f"level {lv['K']}: points present")
        if m["rows"] != rows:
            probs.append(f"level {lv['K']}: rows differ from the first level")
        if m["net_keys"] != ["last", "step"]:
            probs.append(f"level {lv['K']}: proof_net keys {m['net_keys']}")
        if m["total_mass"] != base["total_mass"]:
            probs.append(f"level {lv['K']}: total_mass differs")
        if len(set(lv["rs"])) != len(lv["rs"]):
            probs.append(f"level {lv['K']}: repeated r")
        if any(r < 0 or r > m["last"] for r in lv["rs"]):
            probs.append(f"level {lv['K']}: r outside [0, last]")
        if m["last"] != lv["K"]:
            probs.append(f"level {lv['K']}: last {m['last']} != K")
    zero = 0
    for i, (x0, y0, x1, y1, m) in enumerate(rows):
        if not (0 <= x0 < x1 <= L and 0 <= y0 < y1 <= L):
            probs.append(f"row {i} not a rectangle inside the board")
        if m < 0:
            probs.append(f"row {i} negative mass")
        if m == 0:
            zero += 1
    total = sum((r[4] for r in rows), F(0))
    if base["total_mass"] is not None and total != base["total_mass"]:
        probs.append("sum of masses != total_mass")
    if "target_total_mass" in man and C.rat(man["target_total_mass"]) != total:
        probs.append("sum of masses != manifest target_total_mass")
    if not total < n:
        probs.append(f"total mass {total} not below n = {n}")
    merged = C.expand(rows, L)
    mtot = sum(merged.values(), F(0))
    if mtot != total:
        probs.append("expanded mass != total")
    for key, m in merged.items():
        for im in C.images(key, L):
            if merged.get(im) != m:
                probs.append("expansion not D4-invariant")
                break
        else:
            continue
        break
    bins = C.bins_of(cert)
    gaps = C.coverage_gaps(bins)
    if gaps:
        probs.append(f"angle coverage gaps {[(str(a), str(b)) for a, b in gaps]}")
    if claim is not None and claim != side:
        probs.append(f"claimed {claim} != side {side}")
    rho_max = max(m / ((k[2] - k[0]) * (k[3] - k[1])) for k, m in merged.items())
    iv = sorted((max(l, F(0)), h) for _, _, l, h in bins)
    overlap = sum((max(F(0), min(iv[i][1], iv[i + 1][1]) - iv[i + 1][0]) for i in range(len(iv) - 1)), F(0))
    return {
        "ok": not probs,
        "problems": probs,
        "n": n,
        "side": str(side),
        "kernel": man.get("kernel"),
        "rows": len(rows),
        "zero_mass_rows": zero,
        "merged_rectangles": len(merged),
        "total_mass": str(total),
        "n_minus_total": str(n - total),
        "n_minus_total_float": float(n - total),
        "rho_max": float(rho_max),
        "coordinate_lcm": C.lcm_den([v for k in merged for v in k] + [L / 2]),
        "bins": len(bins),
        "levels": [[lv["K"], str(lv["measure"]["step"]), len(lv["rs"])] for lv in cert["levels"]],
        "bin_overlap_length": str(overlap),
        "last_bin_end": str(max(h for _, _, _, h in bins)),
        "claim": str(claim) if claim is not None else None,
        "measure_sha256_raw": [lv["measure"]["sha256_raw"] for lv in cert["levels"]],
    }


def controls(cert: dict, claim: F | None) -> list[dict]:
    out = []
    base = cert["base"]
    n = base["n"]

    def mutated(fn):
        c2 = copy.deepcopy(cert)
        fn(c2)
        c2["base"] = c2["levels"][0]["measure"]
        return premises(c2, claim)

    def p1(c):
        for lv in c["levels"]:
            r = list(lv["measure"]["rows"])
            tot = sum((x[4] for x in r), F(0))
            x0, y0, x1, y1, m = r[0]
            r[0] = (x0, y0, x1, y1, m + (n - tot))
            lv["measure"]["rows"] = r
            lv["measure"]["total_mass"] = F(n)

    def p2(c):
        for lv in c["levels"]:
            r = list(lv["measure"]["rows"])
            x0, y0, x1, y1, m = r[0]
            r[0] = (x0, y0, x1, y1, -m)
            lv["measure"]["rows"] = r

    def p3(c):
        lv = c["levels"][-1]
        lv["rs"] = lv["rs"][: len(lv["rs"]) // 2] + lv["rs"][len(lv["rs"]) // 2 + 1:]

    def p4(c):
        for lv in c["levels"]:
            r = list(lv["measure"]["rows"])
            x0, y0, x1, y1, m = r[0]
            r[0] = (x0, y0, lv["measure"]["L"] + F(1, 1000), y1, m)
            lv["measure"]["rows"] = r

    def p5(c):
        for lv in c["levels"]:
            lv["measure"]["points"] = [{"point": ["1", "1"], "mass": "1/1000"}]

    for cid, fn in (("P1", p1), ("P2", p2), ("P3", p3), ("P4", p4), ("P5", p5)):
        r = mutated(fn)
        out.append({"id": cid, "refused": not r["ok"], "problems": r["problems"][:3]})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--control-label", default="1042/n136")
    a = ap.parse_args()
    t0 = time.process_time()
    root = Path(a.root)
    cl = claimed(root)
    res = {}
    for lab in S.all_labels(root):
        cert = C.load_certificate(S.folder_of(root, lab))
        res[lab] = premises(cert, cl.get(lab))
        print(lab, "ok" if res[lab]["ok"] else res[lab]["problems"][:2], flush=True)
    cert = C.load_certificate(S.folder_of(root, a.control_label))
    ctl = controls(cert, cl.get(a.control_label))
    summary = {
        "program": "rr1_premises.py",
        "verdict": "PREMISES_HOLD" if all(r["ok"] for r in res.values()) else "PREMISE_PROBLEMS",
        "certificates": len(res),
        "failing": [k for k, r in res.items() if not r["ok"]],
        "controls_label": a.control_label,
        "controls": ctl,
        "controls_as_planned": all(c["refused"] for c in ctl),
        "cpu_seconds": round(time.process_time() - t0, 2),
        "results": res,
    }
    Path(a.out).write_text(json.dumps(summary, indent=1) + "\n")
    print(summary["verdict"], "controls as planned:", summary["controls_as_planned"], "cpu", summary["cpu_seconds"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
