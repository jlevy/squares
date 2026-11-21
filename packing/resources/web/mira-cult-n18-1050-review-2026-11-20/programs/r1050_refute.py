"""C5 driver: build case instances, compile and run r1050_refute.cpp, draw the sample.

Usage:
  python -I r1050_refute.py selftest --scratch DIR --out selftest-refute.json
  python -I r1050_refute.py sample --rack R --orbits orbits.json --witness witness.json \
      --scratch DIR --out sample.json [--seconds 1200]
  python -I r1050_refute.py case --rack R --free "x,y;x,y;x,y" --scratch DIR --out o.json
      [--cap P/Q] [--seconds S]

The sample is fixed by the plan: the 187 canonical forms sorted ascending, minus the
witness orbits of C4, then random.Random(1050).sample(..., 6).
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from r1050_rack import load_rack  # noqa: E402

HERE = Path(__file__).resolve().parent
K_SLICES = 32
MAX_ROUNDS = 60


def build(scratch: Path) -> Path:
    exe = scratch / "r1050_refute"
    subprocess.run(["g++", "-O2", "-std=c++17", "-ffp-contract=off", "-o", str(exe),
                    str(HERE / "r1050_refute.cpp")], check=True)
    return exe


def run(exe: Path, cap: float, marks: list[tuple[float, float, int]], tiles: list[int],
        nodes: int, seconds: float) -> dict[str, object]:
    lines = [f"{cap!r} {K_SLICES} {MAX_ROUNDS} {nodes} {seconds}", str(len(marks))]
    lines += [f"{x!r} {y!r} {o}" for x, y, o in marks]
    lines += [str(len(tiles))] + [str(t) for t in tiles]
    t0 = time.process_time()
    r = subprocess.run([str(exe)], input="\n".join(lines) + "\n", capture_output=True,
                       text=True, check=False)
    words = r.stdout.split()
    return {"verdict": words[0] if words else "ERROR", "stdout": r.stdout.strip(),
            "cpu_seconds": round(time.process_time() - t0 + 0.0, 1)}


def case_instance(lattice: list[tuple[int, int]], scale: int, cap: Fraction,
                  free: list[tuple[int, int]]) -> tuple[list[tuple[float, float, int]], list[int]]:
    marks = []
    tiles = []
    for k, (x, y) in enumerate(lattice):
        occ = 0 if (x, y) in free else 1
        marks.append((float(Fraction(x) * cap / scale), float(Fraction(y) * cap / scale), occ))
        if occ:
            tiles.append(k)
    return marks, tiles


SYNTH = [
    # name, box side, marks, expected
    ("two-in-19/10", 1.9, [(0.7, 0.95), (1.2, 0.95)], "REFUTED"),
    ("four-in-199/100", 1.99, [(0.4975, 0.4975), (1.4925, 0.4975), (0.4975, 1.4925),
                               (1.4925, 1.4925)], "REFUTED"),
    # Below s(5) = 2 + 1/sqrt 2 = 2.7071...: a global squeeze.
    ("five-in-27/10", 2.7, [(0.5, 0.5), (2.2, 0.5), (1.35, 1.35), (0.5, 2.2), (2.2, 2.2)],
     "REFUTED"),
    ("two-in-2001/1000", 2.001, [(0.5, 0.5), (1.5, 1.5)], "UNDECIDED"),
    ("four-in-2001/1000", 2.001, [(0.5, 0.5), (1.5, 0.5), (0.5, 1.5), (1.5, 1.5)], "UNDECIDED"),
    # Feasible: four corner squares and one at 45 degrees about the centre.
    ("five-in-271/100", 2.71, [(0.5, 0.5), (2.21, 0.5), (1.355, 1.355), (0.5, 2.21), (2.21, 2.21)],
     "UNDECIDED"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["selftest", "sample", "case"])
    ap.add_argument("--rack", type=Path)
    ap.add_argument("--orbits", type=Path)
    ap.add_argument("--witness", type=Path)
    ap.add_argument("--free", default=None)
    ap.add_argument("--cap", default=None)
    ap.add_argument("--scratch", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--seconds", type=float, default=1200.0)
    ap.add_argument("--nodes", type=int, default=10**9)
    a = ap.parse_args()
    a.scratch.mkdir(parents=True, exist_ok=True)
    exe = build(a.scratch)
    rep: dict[str, object] = {"program": "r1050_refute.py", "mode": a.mode, "slices": K_SLICES,
                              "max_rounds": MAX_ROUNDS}
    if a.mode == "selftest":
        res = []
        for name, side, pts, want in SYNTH:
            budget = 120.0 if want == "REFUTED" else 20.0
            r = run(exe, side, [(x, y, 1) for x, y in pts], list(range(len(pts))), a.nodes, budget)
            res.append({"instance": name, "expected": want, **r})
        rep["results"] = res
        rep["unsound"] = [r["instance"] for r in res
                          if r["expected"] == "UNDECIDED" and r["verdict"] == "REFUTED"]
        rep["weak"] = [r["instance"] for r in res
                       if r["expected"] == "REFUTED" and r["verdict"] != "REFUTED"]
    else:
        assert a.rack is not None
        cap, scale, _eps, lattice, _n = load_rack(a.rack)
        if a.cap is not None:
            cap = Fraction(a.cap)
        rep["cap"] = str(cap)
        if a.mode == "case":
            assert a.free is not None
            free = [tuple(int(v) for v in p.split(",")) for p in a.free.split(";")]
            todo = [("case", free)]
        else:
            assert a.orbits is not None and a.witness is not None
            forms = [tuple(tuple(p) for p in f)
                     for f in json.loads(a.orbits.read_text())["canonical_forms"]]
            wit = {tuple(tuple(p) for p in f)
                   for f in json.loads(a.witness.read_text())["witness_orbits"]}
            pool = [f for f in sorted(forms) if f not in wit]
            sample = random.Random(1050).sample(pool, 6)
            rep["sample"] = [[list(p) for p in f] for f in sample]
            todo = [("sample", list(f)) for f in sample] + [("witness", list(f)) for f in sorted(wit)]
        res = []
        for kind, free in todo:
            marks, tiles = case_instance(lattice, scale, cap, [tuple(p) for p in free])
            r = run(exe, float(cap), marks, tiles, a.nodes, a.seconds)
            res.append({"kind": kind, "free": [list(p) for p in free], **r})
            print(kind, free, r["stdout"], flush=True)
        rep["results"] = res
    a.out.write_text(json.dumps(rep, indent=1) + "\n")
    print(json.dumps({k: v for k, v in rep.items() if k != "results"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
