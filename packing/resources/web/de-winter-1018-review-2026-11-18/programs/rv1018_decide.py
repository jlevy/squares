"""Decide rotated directions of a format M certificate with this lane's own branch and bound.

Lane r108-1118, blind review of jlevy/squares#1018. For each requested net index r >= 1
it prepares the exact inputs for rv1018_bnb.c (cosine and sine of 2 arctan(r D) with a
bound on their float error, the half-side rounded both ways, the quadrant [L/2, U_r]^2
rounded outward, every rectangle rounded inward and outward, densities and masses rounded
down), compiles and runs the C program, and confirms any counterexample candidate in exact
rational arithmetic. Verdicts per direction:

- DECIDED: every leaf box accepted; the capture is at least the threshold on the quadrant.
- REFUSED_EXACT: an exact capture below the threshold at a centre of the quadrant.
- UNDECIDED: a candidate that exact arithmetic does not confirm, an unresolved box at the
  depth limit, or the node budget exhausted. It proves nothing either way.

Imports nothing from jlevy/squares or the source.

Usage:
  python -I rv1018_decide.py --measure M.json.gz --directions 1,2,400 --out OUT.json
      [--factor 99/100] [--threshold 1] [--node-cap 4e8] [--scratch DIR]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import struct
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1018_common as cm  # noqa: E402

HERE = Path(__file__).resolve().parent
C_SOURCE = HERE / "rv1018_bnb.c"
GCC_FLAGS = ["-O2", "-ffp-contract=off", "-fno-fast-math", "-std=c11"]
EPS = 2.0**-52
DELTA = 1e-12
TAU = 1e-11
MAXD = 72
RING_PIECES = 8


def f_down(q: Fraction) -> float:
    f = float(q)
    return math.nextafter(f, -math.inf) if Fraction(f) > q else f


def f_up(q: Fraction) -> float:
    f = float(q)
    return math.nextafter(f, math.inf) if Fraction(f) < q else f


def build(scratch: Path) -> tuple[Path, dict[str, str]]:
    scratch.mkdir(parents=True, exist_ok=True)
    exe = scratch / "rv1018_bnb"
    subprocess.run(["gcc", *GCC_FLAGS, "-o", str(exe), str(C_SOURCE), "-lm"], check=True)
    ver = subprocess.run(["gcc", "--version"], capture_output=True, text=True, check=True)
    return exe, {
        "c_source_sha256": hashlib.sha256(C_SOURCE.read_bytes()).hexdigest(),
        "binary_sha256": hashlib.sha256(exe.read_bytes()).hexdigest(),
        "compiler": ver.stdout.splitlines()[0],
        "flags": " ".join(GCC_FLAGS),
    }


def rect_records(rects: list, factor: Fraction) -> list[tuple[float, ...]]:
    out = []
    for x0, y0, x1, y1, mass, dens in rects:
        out.append(
            (
                f_up(x0),
                f_up(y0),
                f_down(x1),
                f_down(y1),
                f_down(x0),
                f_down(y0),
                f_up(x1),
                f_up(y1),
                f_down(dens * factor),
                f_down(mass * factor),
            )
        )
    return out


def direction_header(
    r: int,
    step: Fraction,
    side_b: Fraction,
    side: Fraction,
    threshold: Fraction,
    node_cap: float,
    ring_pieces: int = RING_PIECES,
) -> tuple[list[float], dict[str, object]]:
    c, s = cm.cos_sin(r * step)
    cf, sf = float(c), float(s)
    epscs = 2.0 * max(float(abs(Fraction(cf) - c)), float(abs(Fraction(sf) - s)), 2.0**-1074)
    h = side_b / 2
    upper = cm.domain_upper(r, step, side)
    zmax = 12.0
    eg = 256.0 * EPS * (1.0 + zmax) / min(sf, cf)
    hdr = [
        1018.0,
        0.0,  # K, filled by the caller
        cf,
        sf,
        epscs,
        f_down(h),
        f_up(h),
        DELTA,
        TAU,
        eg,
        f_up(threshold),
        f_down(side / 2),
        f_up(upper),
        f_down(side / 2),
        f_up(upper),
        float(MAXD),
        float(node_cap),
        0.0,
        float(ring_pieces),
    ]
    info = {
        "r": r,
        "tangent": str(r * step),
        "cos": str(c),
        "sin": str(s),
        "domain_upper": str(upper),
        "eps_cs": epscs,
        "eg": eg,
    }
    return hdr, info


def write_input(path: Path, hdr: list[float], recs: list[tuple[float, ...]], boxes=()) -> None:
    hdr = list(hdr)
    hdr[1] = float(len(recs))
    with path.open("wb") as fh:
        fh.write(struct.pack("<19d", *hdr))
        for rec in recs:
            fh.write(struct.pack("<10d", *rec))
        for bx in boxes:
            fh.write(struct.pack("<4d", *bx))


def parse_output(text: str) -> dict[str, object]:
    out: dict[str, object] = {}
    for line in text.splitlines():
        key, _, rest = line.partition(" ")
        parts = rest.split()
        if key == "verdict":
            out["engine_verdict"] = parts[0]
        elif key in ("nodes", "leaves", "straddler_evaluations"):
            out[key] = int(float(parts[0]))
        elif key in ("max_depth", "unresolved"):
            out[key] = int(parts[0])
        elif key == "min_bound":
            out["min_bound"] = float.fromhex(parts[0])
        elif key == "min_box":
            out["min_box"] = [float.fromhex(p) for p in parts]
        elif key == "candidate":
            out["candidate"] = [float.fromhex(parts[0]), float.fromhex(parts[1]), float(parts[2])]
        elif key == "cpu_seconds":
            out["cpu_seconds"] = float(parts[0])
    return out


def box_bounds(
    exe: Path, scratch: Path, hdr: list[float], recs: list, boxes: list[tuple[float, ...]]
) -> list[tuple[float, float]]:
    """Mode 1: the bound and the centre estimate for each listed box (for the self-test)."""
    hdr = list(hdr)
    hdr[17] = 1.0
    path = scratch / f"boxtest-{os.getpid()}-{random.getrandbits(32)}.bin"
    write_input(path, hdr, recs, boxes)
    res = subprocess.run([str(exe), str(path)], capture_output=True, text=True, check=True)
    path.unlink()
    vals = []
    for line in res.stdout.splitlines():
        _, a, b = line.split()
        vals.append((float.fromhex(a), float.fromhex(b)))
    return vals


def decide_direction(
    exe: Path,
    scratch: Path,
    rects: list,
    rects_q: list,
    r: int,
    step: Fraction,
    side_b: Fraction,
    side: Fraction,
    factor: Fraction,
    threshold: Fraction,
    node_cap: float,
    ring: int = RING_PIECES,
) -> dict[str, object]:
    hdr, info = direction_header(r, step, side_b, side, threshold, node_cap, ring)
    recs = rect_records(rects, factor)
    path = scratch / f"dir-{r}-{os.getpid()}.bin"
    write_input(path, hdr, recs)
    t0 = time.process_time()
    res = subprocess.run([str(exe), str(path)], capture_output=True, text=True, check=True)
    path.unlink()
    out = parse_output(res.stdout)
    out.update(info)
    ev = out["engine_verdict"]
    if ev == "DECIDED" and out["min_bound"] >= float(threshold):
        out["verdict"] = "DECIDED"
    elif ev == "CANDIDATE":
        cx, cy, _ = out["candidate"]
        exact = cm.capture_exact(rects_q, r, step, side_b, Fraction(cx), Fraction(cy))
        out["candidate_exact"] = cm.mpq_to_float_str(exact, 20)
        upper = cm.domain_upper(r, step, side)
        inside = side / 2 <= Fraction(cx) <= upper and side / 2 <= Fraction(cy) <= upper
        out["candidate_in_quadrant"] = inside
        if exact < cm._q(threshold) and inside:
            out["verdict"] = "REFUSED_EXACT"
        else:
            out["verdict"] = "UNDECIDED"
    else:
        out["verdict"] = "UNDECIDED"
    out["driver_cpu_seconds"] = time.process_time() - t0
    return out


def parse_dirs(spec: str, last: int) -> list[int]:
    if spec == "all":
        return list(range(1, last + 1))
    return [int(x) for x in spec.split(",") if x]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", required=True)
    ap.add_argument("--directions", help="'all', or a comma-separated list")
    ap.add_argument("--directions-from", help="a rv1018_sample.py output: its sample")
    ap.add_argument("--out", required=True)
    ap.add_argument("--factor", default="1")
    ap.add_argument("--threshold", default="1")
    ap.add_argument("--node-cap", type=float, default=4e8)
    ap.add_argument("--ring", type=int, default=RING_PIECES)
    ap.add_argument("--scratch", default=os.environ.get("TMPDIR", "/tmp"))
    args = ap.parse_args()
    meas = cm.read_measure(args.measure)
    factor, threshold = Fraction(args.factor), Fraction(args.threshold)
    rects = cm.expand(meas["rows"], meas["L"])
    rects_q = cm.to_mpq_rects(rects, factor)
    scratch = Path(args.scratch) / f"rv1018-decide-{os.getpid()}"
    exe, build_info = build(scratch)
    results = []
    if args.directions_from:
        dirs = json.loads(Path(args.directions_from).read_text())["sample"]["all"]
    else:
        dirs = parse_dirs(args.directions, meas["last"])
    for r in dirs:
        res = decide_direction(
            exe,
            scratch,
            rects,
            rects_q,
            r,
            meas["step"],
            meas["B"],
            meas["L"],
            factor,
            threshold,
            args.node_cap,
            args.ring,
        )
        results.append(res)
        print(
            f"r={r} {res['verdict']} nodes={res.get('nodes')} min_bound={res.get('min_bound')!r} "
            f"cpu={res.get('cpu_seconds')}",
            flush=True,
        )
    verdicts = sorted({x["verdict"] for x in results})
    summary = {
        "program": "rv1018_decide.py",
        "measure_json_sha256": meas["json_sha256"],
        "factor": str(factor),
        "threshold": str(threshold),
        "ring_pieces": args.ring,
        "node_cap": args.node_cap,
        "build": build_info,
        "directions": len(results),
        "verdicts": {v: sum(1 for x in results if x["verdict"] == v) for v in verdicts},
        "nodes": sum(x.get("nodes", 0) for x in results),
        "cpu_seconds": round(sum(x.get("cpu_seconds", 0.0) for x in results), 3),
        "results": results,
    }
    if all(x["verdict"] == "DECIDED" for x in results):
        summary["verdict"] = "ALL_SAMPLED_DIRECTIONS_DECIDED"
    elif any(x["verdict"] == "REFUSED_EXACT" for x in results):
        summary["verdict"] = "REFUSED_WITH_EXACT_WITNESS"
    else:
        summary["verdict"] = "NOT_DECIDED"
    Path(args.out).write_text(json.dumps(summary, separators=(",", ":")) + "\n")
    print(summary["verdict"], summary["verdicts"], f"cpu={summary['cpu_seconds']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
