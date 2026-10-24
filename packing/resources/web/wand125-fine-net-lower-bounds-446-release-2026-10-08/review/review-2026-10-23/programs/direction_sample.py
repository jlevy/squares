"""A stratified sample of rotated net directions: independent minimisation, exact values.

This decides nothing about coverage between the points it evaluates. It is a
falsification test and a measurement. At each sampled direction r of each certificate it

1. searches for the least capture over the per-bin quadrant [L/2, U_r]^2 by itself: a
   49 x 49 grid with both ends, then a compass search (8 directions, halving the step to
   1e-12) from the best grid point of each of the 16 blocks of a 4 x 4 partition of the
   quadrant; one more start at the source's least-bound box centre is run and reported
   apart, so that the independent result never depends on it;
2. evaluates the capture exactly (rational clipping, t233lib) at every search's end point;
3. checks that every exact value is at least 1 (any value below 1 is a counterexample to
   the certificate), and at least the source's certified bound for the direction (which
   is a lower bound over the whole quadrant, so it must not exceed any value found);
4. reports whether the 99/100 mutant would have an exact witness there (0.99 F < 1), the
   whole-net control's requirement, and the gap between the least value found and the
   source's certified bound.

Directions: index 1, the last index, the source's least-certified direction, the
direction whose least-bound centre had the least exact capture (receipts_check), and one
seeded index in each of 28 equal strata of 1..last (seed: the candidate's SHA-256).

    OPENBLAS_NUM_THREADS=1 python3 -I direction_sample.py --packet PACKET \
        --receipts outputs/receipts-check.json --out outputs/direction-sample.json
"""

from __future__ import annotations

import argparse
import gzip
import json
import random
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from t233lib import (  # noqa: E402
    CERTS,
    cos_sin,
    domain_upper,
    exact_capture,
    expand,
    float_capture,
    loose_json,
    read_candidate,
)

GRID = 49
BLOCKS = 4
STRATA = 28
MIN_STEP = 1e-12
MAX_EVALS = 600


def compass(f, x: float, y: float, lo: float, hi: float, step: float) -> tuple[float, float, float, int]:
    best = f(x, y)
    evals = 1
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    while step > MIN_STEP and evals < MAX_EVALS:
        cand = None
        for dx, dy in dirs:
            nx = min(max(x + dx * step, lo), hi)
            ny = min(max(y + dy * step, lo), hi)
            if (nx, ny) == (x, y):
                continue
            v = f(nx, ny)
            evals += 1
            if v < best and (cand is None or v < cand[0]):
                cand = (v, nx, ny)
        if cand is None:
            step /= 2
        else:
            best, x, y = cand
    return best, x, y, evals


def sample_directions(cand, run_rows: list[dict], least_exact_r: int | None) -> list[tuple[int, str]]:
    last = cand.last
    picks: dict[int, str] = {1: "first rotated", last: "last"}
    rot = [r for r in run_rows if r.get("r", 0) >= 1 and "min_certified_lower_bound" in r]
    least = min(rot, key=lambda r: r["min_certified_lower_bound"])["r"]
    picks.setdefault(least, "source's least certified")
    if least_exact_r is not None:
        picks.setdefault(least_exact_r, "least exact capture at a least-bound centre")
    rng = random.Random(int(cand.raw_sha256[:16], 16))
    for b in range(STRATA):
        a = 1 + (b * last) // STRATA
        z = ((b + 1) * last) // STRATA
        r = rng.randint(a, z)
        picks.setdefault(r, f"stratum {b + 1} of {STRATA} [{a}, {z}]")
    return sorted(picks.items())


def run_case(packet: Path, n: int, least_exact_r: int | None) -> dict:
    cand = read_candidate(packet, n)
    meas = expand(cand)
    name = CERTS[n][0]
    path = packet / "release" / "certificates" / name / "check2" / "run.jsonl.gz"
    with gzip.open(path, "rb") as fh:
        rows = [loose_json(line) for line in fh.read().splitlines() if line.strip()]
    by_r = {r["r"]: r for r in rows if "r" in r}
    h = cand.B / 2
    hf = float(h)
    results = []
    for r, why in sample_directions(cand, rows, least_exact_r):
        c, s = cos_sin(cand.step, r)
        cf, sf = float(c), float(s)
        lo = float(cand.L / 2)
        hi_exact = domain_upper(cand.L, cand.step, r)
        hi = float(hi_exact)
        if Fraction(hi) > hi_exact:  # keep every searched point inside the closed quadrant
            hi = float(hi_exact - Fraction(1, 10**15))

        def f(x: float, y: float, cf: float = cf, sf: float = sf) -> float:
            return float_capture(meas, x, y, cf, sf, hf)

        pts = [lo + (hi - lo) * i / (GRID - 1) for i in range(GRID)]
        grid = [(f(x, y), i, j) for i, x in enumerate(pts) for j, y in enumerate(pts)]
        spacing = (hi - lo) / (GRID - 1)
        best_in_block: dict[tuple[int, int], tuple[float, int, int]] = {}
        for v, i, j in grid:
            key = (min(i * BLOCKS // GRID, BLOCKS - 1), min(j * BLOCKS // GRID, BLOCKS - 1))
            if key not in best_in_block or v < best_in_block[key][0]:
                best_in_block[key] = (v, i, j)
        ends = []
        for _v, i, j in sorted(best_in_block.values()):
            ends.append(("grid", compass(f, pts[i], pts[j], lo, hi, spacing)))
        box = by_r[r]["least_bound_box"]
        bx = min(max(box["x"], lo), hi)
        by = min(max(box["y"], lo), hi)
        ends.append(("source box centre", compass(f, bx, by, lo, hi, max(box["dx"], box["dy"]))))
        exact = []
        for origin, (_v, x, y, evals) in ends:
            val, _i, _b = exact_capture(meas, Fraction(x), Fraction(y), c, s, h)
            exact.append({"origin": origin, "x": x, "y": y, "exact": val, "evals": evals})
        indep = [e for e in exact if e["origin"] == "grid"]
        best_ind = min(indep, key=lambda e: e["exact"])
        best_all = min(exact, key=lambda e: e["exact"])
        bound = by_r[r]["min_certified_lower_bound"]
        results.append({
            "r": r,
            "why": why,
            "domain": [lo, hi],
            "least_exact_independent": float(best_ind["exact"]),
            "least_exact_independent_point": [best_ind["x"], best_ind["y"]],
            "least_exact_with_box_start": float(best_all["exact"]),
            "every_exact_value_at_least_1": all(e["exact"] >= 1 for e in exact),
            "every_exact_value_at_least_source_bound": all(e["exact"] >= Fraction(bound) for e in exact),
            "source_certified_bound": bound,
            "gap_least_found_minus_source_bound": float(best_all["exact"] - Fraction(bound)),
            "mutant_99_100_witness_found": best_all["exact"] * Fraction(99, 100) < 1,
            "distance_to_source_box_centre": max(abs(best_all["x"] - box["x"]), abs(best_all["y"] - box["y"])),
            "evaluations": GRID * GRID + sum(e["evals"] for e in exact),
            "points": [
                {"origin": e["origin"], "x": e["x"], "y": e["y"], "exact": float(e["exact"])}
                for e in exact
            ],
        })
        print(n, r, why, "least", float(best_all["exact"]), "indep", float(best_ind["exact"]),
              "bound", bound, flush=True)
    return {
        "certificate": name,
        "directions": results,
        "sampled": len(results),
        "least_exact_found": min(d["least_exact_with_box_start"] for d in results),
        "all_at_least_1": all(d["every_exact_value_at_least_1"] for d in results),
        "all_at_least_source_bound": all(d["every_exact_value_at_least_source_bound"] for d in results),
        "mutant_witnesses": sum(1 for d in results if d["mutant_99_100_witness_found"]),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--packet", type=Path, required=True)
    ap.add_argument("--receipts", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--only", type=int, action="append")
    args = ap.parse_args()
    t0 = time.perf_counter()
    least_exact: dict[str, int] = {}
    if args.receipts:
        rc = json.loads(args.receipts.read_text())
        for k, v in rc["cases"].items():
            least_exact[k] = v["run"]["least_exact_margin_at_those_centres"]["r"]
    out: dict[str, object] = {"kind": "t233-review-direction-sample/v1", "cases": {}}
    ok = True
    for n in CERTS:
        if args.only and n not in args.only:
            continue
        c0 = resource.getrusage(resource.RUSAGE_SELF)
        res = run_case(args.packet, n, least_exact.get(str(n)))
        c1 = resource.getrusage(resource.RUSAGE_SELF)
        res["cpu_seconds"] = round(c1.ru_utime + c1.ru_stime - c0.ru_utime - c0.ru_stime, 3)
        ok = ok and res["all_at_least_1"] and res["all_at_least_source_bound"]
        out["cases"][str(n)] = res
        print(n, "sampled", res["sampled"], "least exact", res["least_exact_found"],
              "mutant witnesses", res["mutant_witnesses"], "cpu", res["cpu_seconds"], flush=True)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out["verdict"] = "NO_COUNTEREXAMPLE_IN_SAMPLE" if ok else "SAMPLE_REFUTES"
    out["cpu_seconds"] = round(usage.ru_utime + usage.ru_stime, 3)
    out["wall_seconds"] = round(time.perf_counter() - t0, 3)
    args.out.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(out["verdict"], "cpu", out["cpu_seconds"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
