"""Lane rR1-lower: a seeded float search for low captures of true unit squares, each end
point evaluated exactly.  It decides nothing unless an exact capture falls below the
threshold, which refutes the certificate.

Usage: rr1_search.py --root SRC_FOLDER --labels all|L1,L2 --scratch DIR --out FILE
"""

from __future__ import annotations

import argparse
import json
import math
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rr1_common as C  # noqa: E402

ANGLES_T = [F(j, 32) * F(41421356, 10**8) for j in range(33)]


def folder_of(root: Path, label: str) -> Path:
    issue, nn = label.split("/")
    return root / ("proof" if issue == "1041" else "followup/lower") / nn


def all_labels(root: Path) -> list[str]:
    a = ["1041/" + p.name for p in (root / "proof").glob("n[0-9]*") if p.is_dir()]
    b = ["1042/" + p.name for p in (root / "followup/lower").glob("n[0-9]*") if p.is_dir()]
    return sorted(a + b)


def fsearch(exe: Path, rects: Path, scratch: Path, Q: int, L: F, ts: list[F], grid: int, kbest: int) -> list:
    spec = scratch / "fsearch.txt"
    spec.write_text(f"{float(Q)!r}\n{float(L)!r} {grid} {kbest} {len(ts)}\n" + "\n".join(repr(float(t)) for t in ts) + "\n")
    out = C.run_c(exe, ["fsearch", str(rects), str(spec)])
    res = []
    for line in out.splitlines():
        x, y, t, v = (float(u) for u in line.split())
        res.append((x, y, t, v))
    return res


def exact_pose(merged: dict, L: F, x: float, y: float, t: float) -> dict:
    tt = min(max(F(round(t * 2**40), 2**40), F(0)), C.TSTAR)
    w = C.w_of(tt)
    cx = min(max(F(round(x * 10**12), 10**12), w), L - w)
    cy = min(max(F(round(y * 10**12), 10**12), w), L - w)
    assert C.admissible((cx, cy), tt, L)
    cap = C.exact_capture(merged, C.square_vertices((cx, cy), tt))
    return {"cx": str(cx), "cy": str(cy), "t": str(tt), "capture": str(cap), "capture_float": float(cap)}


def search_one(exe: Path, root: Path, label: str, scratch: Path, grid: int = 41, kbest: int = 12, nexact: int = 6) -> dict:
    cert = C.load_certificate(folder_of(root, label))
    base = cert["base"]
    L = base["L"]
    merged = C.expand(base["rows"], L)
    lat = C.lattice(merged, L)
    rects = scratch / "rects.txt"
    C.write_rects(lat, rects)
    found = fsearch(exe, rects, scratch, lat["Q"], L, ANGLES_T, grid, kbest)
    found.sort(key=lambda r: r[3])
    exact = [exact_pose(merged, L, *r[:3]) | {"float": r[3]} for r in found[:nexact]]
    exact.sort(key=lambda e: F(e["capture"]))
    least = exact[0]
    t_least = F(least["t"])
    bins = C.bins_of(cert)
    holding = [(K, r) for K, r, l, h in bins if max(l, F(0)) <= t_least <= h]
    return {
        "label": label,
        "n": base["n"],
        "L": str(L),
        "least": least,
        "poses": exact,
        "below_one": any(F(e["capture"]) < 1 for e in exact),
        "least_times_99_100_below_one": F(least["capture"]) * F(99, 100) < 1,
        "bins_holding_least_t": holding,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--labels", default="all")
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = Path(a.root)
    scratch = Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    exe = C.build_c(scratch)
    labels = all_labels(root) if a.labels == "all" else a.labels.split(",")
    t0 = time.process_time()
    out = []
    for lab in labels:
        r = search_one(exe, root, lab, scratch)
        out.append(r)
        print(lab, r["least"]["capture_float"], r["below_one"], r["least_times_99_100_below_one"], flush=True)
    ch = resource.getrusage(resource.RUSAGE_CHILDREN)
    summary = {
        "program": "rr1_search.py",
        "verdict": "COUNTEREXAMPLE_FOUND" if any(r["below_one"] for r in out) else "NO_COUNTEREXAMPLE_IN_SEARCH",
        "all_99_100_below_one": all(r["least_times_99_100_below_one"] for r in out),
        "count": len(out),
        "cpu_seconds": time.process_time() - t0 + ch.ru_utime + ch.ru_stime,
        "results": out,
    }
    Path(a.out).write_text(json.dumps(summary, indent=1) + "\n")
    print(summary["verdict"], "99/100 all below one:", summary["all_99_100_below_one"], "cpu", round(summary["cpu_seconds"], 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
