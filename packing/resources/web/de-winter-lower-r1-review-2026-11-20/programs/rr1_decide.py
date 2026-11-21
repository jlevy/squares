"""Lane rR1-lower: the clean-room decider's driver.

For each bin t in [l, h] of the certificate's partition it builds a lattice polygon P
inside every unit square of the bin (each vertex verified exactly, rr1_common.bin_polygon),
the quadrant [L/2, L - w(l)]^2 rounded outward, and runs rr1_decide.c, whose accepted
bounds are exact integer arithmetic.  A failing bin gets an exact witness search; without
a witness it is split in three, at most --split-depth times, else UNDECIDED.

Usage: rr1_decide.py --root SRC_FOLDER --label 1042/n136 [--bins all|least|K:r,...]
       [--factor 99/100] [--stretch 1001/1000] [--threshold 1] [--widen 0] [--no-split]
       [--procs 2] --scratch DIR --out FILE
"""

from __future__ import annotations

import argparse
import json
import math
import resource
import subprocess
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rr1_common as C  # noqa: E402
import rr1_search as S  # noqa: E402

NMAX = 1_000_000
MINW = 1 << 10


def prepare(root: Path, label: str, factor: F, stretch: F) -> dict:
    cert = C.load_certificate(S.folder_of(root, label))
    base = cert["base"]
    L = base["L"] * stretch
    rows = [(x0 * stretch, y0 * stretch, x1 * stretch, y1 * stretch, m) for x0, y0, x1, y1, m in base["rows"]]
    merged = C.expand(rows, L, factor)
    lat = C.lattice(merged, L)
    return {"cert": cert, "L": L, "merged": merged, "lat": lat, "n": base["n"]}


def bin_record(prep: dict, K: int, r: int, l: F, h: F, tag: str, threshold: F, mutant_domain_hi: bool = False) -> dict:
    Q = prep["lat"]["Q"]
    P = C.bin_polygon(l, h, Q)
    X0, X1 = C.domain(prep["L"], P["hi"] if mutant_domain_hi else P["lo"], Q)
    T = math.ceil(threshold * 2**C.W_BITS)
    return {"id": tag, "K": K, "r": r, "l": l, "h": h, "P": P, "X0": X0, "X1": X1, "T": T}


def write_bins(recs: list[dict], path: Path, nmax: int, minw: int) -> None:
    with open(path, "w") as f:
        f.write(f"BINS {len(recs)}\n")
        for b in recs:
            v = b["P"]["verts"]
            f.write(f"{b['id']} {b['X0']} {b['X1']} {b['X0']} {b['X1']} {b['T']} {nmax} {minw}\n{len(v)}\n")
            for x, y in v:
                f.write(f"{x} {y}\n")


def run_bins(exe: Path, rects: Path, recs: list[dict], scratch: Path, procs: int, nmax: int, minw: int,
             env: dict | None = None) -> dict:
    chunks = [recs[i::procs] for i in range(procs)]
    ps = []
    for i, ch in enumerate(chunks):
        if not ch:
            continue
        bf = scratch / f"bins-{i}.txt"
        write_bins(ch, bf, nmax, minw)
        ps.append(subprocess.Popen([str(exe), "decide", str(rects), str(bf)], stdout=subprocess.PIPE, text=True,
                                   env=env))
    out = {}
    for p in ps:
        so, _ = p.communicate()
        if p.returncode != 0:
            raise RuntimeError("rr1_decide decide failed")
        for line in so.splitlines():
            d = json.loads(line)
            out[d["id"]] = d
    return out


def witness(exe: Path, rects: Path, prep: dict, b: dict, res: dict, threshold: F, scratch: Path) -> dict | None:
    """Exact captures of true unit squares near the failing box and from a bin-wide search."""
    Q = prep["lat"]["Q"]
    L = prep["L"]
    lo, hi = b["P"]["lo"], b["P"]["hi"]
    ts = [lo, (lo + hi) / 2, hi]
    tried = []
    if "fail_box" in res:
        xa, xb, ya, yb = res["fail_box"]
        for cx, cy in ((xa, ya), (xb, ya), (xa, yb), (xb, yb)):
            for t in ts:
                c = (F(cx, Q), F(cy, Q))
                if C.admissible(c, t, L):
                    cap = C.exact_capture(prep["merged"], C.square_vertices(c, t))
                    tried.append({"cx": str(c[0]), "cy": str(c[1]), "t": str(t), "capture": str(cap)})
                    if cap < threshold:
                        return {"pose": tried[-1], "tried": len(tried)}
    found = S.fsearch(exe, rects, scratch, Q, L, ts, 21, 6)
    found.sort(key=lambda r: r[3])
    for x, y, t, _v in found[:4]:
        e = S.exact_pose(prep["merged"], L, x, y, t)
        tried.append(e)
        if F(e["capture"]) < threshold:
            return {"pose": e, "tried": len(tried)}
    return None


def decide(exe: Path, prep: dict, bins: list[tuple[int, int, F, F]], threshold: F, scratch: Path, procs: int,
           split_depth: int, nmax: int = NMAX, minw: int = MINW, env: dict | None = None,
           mutant_domain_hi: bool = False) -> list[dict]:
    rects = scratch / "rects.txt"
    C.write_rects(prep["lat"], rects)
    recs = [bin_record(prep, K, r, l, h, f"K{K}r{r}", threshold, mutant_domain_hi) for K, r, l, h in bins]
    results = []
    pending = [(rec, 0) for rec in recs]
    while pending:
        res = run_bins(exe, rects, [p for p, _ in pending], scratch, procs, nmax, minw, env)
        nxt = []
        for rec, depth in pending:
            r = res[rec["id"]]
            item = {
                "id": rec["id"], "K": rec["K"], "r": rec["r"], "l": str(rec["l"]), "h": str(rec["h"]),
                "depth": depth, "verdict": r["verdict"], "nodes": r["nodes"], "clips": r["clips"],
                "tree_depth": r["depth"], "seconds": r["seconds"],
                "min_accepted": r["min_accepted"], "polygon_vertices": len(rec["P"]["verts"]),
                "polygon_area": float(F(C.poly_area(rec["P"]["verts"]), 2 * prep["lat"]["Q"] ** 2)),
                "domain": [rec["X0"], rec["X1"]],
            }
            if r["verdict"] == "ACCEPT":
                item["verdict"] = "ACCEPT"
                results.append(item)
                continue
            item["fail_box"] = r.get("fail_box")
            item["fail_bound"] = r.get("fail_bound")
            item["fail_corners"] = r.get("fail_corners")
            w = witness(exe, rects, prep, rec, r, threshold, scratch)
            if w is not None:
                item["verdict"] = "REFUSED_EXACT"
                item["witness"] = w
                results.append(item)
                continue
            if depth >= split_depth:
                item["verdict"] = "UNDECIDED"
                results.append(item)
                continue
            item["verdict"] = "SPLIT"
            results.append(item)
            lo, hi = rec["l"], rec["h"]
            for i in range(3):
                sl, sh = lo + (hi - lo) * i / 3, lo + (hi - lo) * (i + 1) / 3
                if sh <= 0 or max(sl, F(0)) >= C.TSTAR:
                    continue
                sub = bin_record(prep, rec["K"], rec["r"], sl, sh, f"{rec['id']}s{depth + 1}{i}", threshold,
                                 mutant_domain_hi)
                nxt.append((sub, depth + 1))
        pending = nxt
    return results


def summarize(results: list[dict]) -> str:
    v = {r["verdict"] for r in results if r["verdict"] != "SPLIT"}
    if "REFUSED_EXACT" in v:
        return "REFUSED_EXACT"
    if "UNDECIDED" in v:
        return "UNDECIDED"
    return "DECIDED"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--bins", default="all")
    ap.add_argument("--factor", default="1")
    ap.add_argument("--stretch", default="1")
    ap.add_argument("--threshold", default="1")
    ap.add_argument("--widen", default="0")
    ap.add_argument("--no-split", action="store_true")
    ap.add_argument("--procs", type=int, default=2)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    t0 = time.process_time()
    w0 = time.time()
    root = Path(a.root)
    scratch = Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    exe = C.build_c(scratch)
    prep = prepare(root, a.label, F(a.factor), F(a.stretch))
    allb = C.bins_of(prep["cert"])
    if a.bins == "all":
        sel = allb
    else:
        want = {tuple(int(u) for u in s.split(":")) for s in a.bins.split(",")}
        sel = [b for b in allb if (b[0], b[1]) in want]
        if len(sel) != len(want):
            raise SystemExit("unknown bin requested")
    widen = int(a.widen)
    if widen:
        sel = [(K, r, l - widen * (h - l), h + widen * (h - l)) for K, r, l, h in sel]
    gaps = C.coverage_gaps(allb)
    res = decide(exe, prep, sel, F(a.threshold), scratch, a.procs, 0 if a.no_split else 2)
    ch = resource.getrusage(resource.RUSAGE_CHILDREN)
    summary = {
        "program": "rr1_decide.py",
        "label": a.label,
        "n": prep["n"],
        "L": str(prep["L"]),
        "factor": a.factor,
        "stretch": a.stretch,
        "threshold": a.threshold,
        "widen": widen,
        "bins_requested": "all" if a.bins == "all" else a.bins,
        "partition_gaps": [[str(x), str(y)] for x, y in gaps],
        "lattice_Q": prep["lat"]["Q"],
        "lattice_rounded": prep["lat"]["rounded"],
        "G": prep["lat"]["G"],
        "rectangles": len(prep["lat"]["rects"]),
        "verdict": summarize(res),
        "bins_decided": sum(1 for r in res if r["verdict"] == "ACCEPT" and r["depth"] == 0),
        "bins_split": sum(1 for r in res if r["verdict"] == "SPLIT"),
        "nodes": sum(r["nodes"] for r in res),
        "c_seconds": round(sum(r["seconds"] for r in res), 3),
        "cpu_seconds": round(time.process_time() - t0 + ch.ru_utime + ch.ru_stime, 3),
        "wall_seconds": round(time.time() - w0, 3),
        "results": res,
    }
    if a.bins == "all" and gaps:
        summary["verdict"] = "PARTITION_GAP"
    Path(a.out).write_text(json.dumps(summary, indent=1) + "\n")
    print(a.label, summary["verdict"], "bins", len(res), "nodes", summary["nodes"], "cpu", summary["cpu_seconds"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
