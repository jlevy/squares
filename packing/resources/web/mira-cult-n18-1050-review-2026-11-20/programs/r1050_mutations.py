"""C7 (after the freeze): mutated inputs the source's own replay must refuse.

Usage: python -I r1050_mutations.py --replay DIR --scratch DIR --out mutations.json [--workers N]

Each mutation is made in a fresh copy of the source's replay folder and only the source
script that consumes the mutated input runs there, with the project interpreter as
`python -S`, the way verify_exact_18.py runs it. A mutation is refused when that script
exits non-zero. The plan's five mutations:
  M1 a construction coordinate changed (tile 1's x from 1/2 to 499/1000);
  M2 a rack point moved ((1000,716) to (1000,640)), rack verifier alone;
  M3 a case key deleted from the base cover;
  M4 the case-53 slab terminal that holds the exact construction relabelled 'empty';
  M5 a slab edge of case 55 moved by 10^-6 so consecutive slabs no longer meet.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


def mutate_json(path: Path, fn) -> None:  # noqa: ANN001
    data = json.loads(path.read_text())
    fn(data)
    path.write_text(json.dumps(data))


def m1(d: dict) -> None:
    for row in d["centers"]:
        if row[0] == 1:
            row[2] = ["499/1000", "0"]


def m2(d: dict) -> None:
    d["orbits"] = [[x, y] if [x, y] != [1000, 716] else [1000, 640] for x, y in d["orbits"]]


def m3(d: dict) -> None:
    del d["1ffbf6"]


def m4(rows: list) -> None:
    first = rows[0]
    assert first[0] is None and first[1] == 3250000
    first[2][0][2] = ["empty"]


def m5(rows: list) -> None:
    rows[0][1] += 1  # the next slab still starts at the old edge


MUTATIONS = [
    ("M1", "six-tilt18.json", m1, ["six_tilt18.py"]),
    ("M2", "stabs18-endpoint-window.json", m2, ["check_stabs.py", "stabs18-endpoint-window.json"]),
    ("M3", "n18-482-base.json", m3, ["verify_six_endpoint_classes.py", "--workers", "{w}"]),
    ("M4", "full-endpoint-mask-cases.json", m4, ["verify_full_endpoint_mask.py", "--workers", "{w}"]),
    ("M5", "second-endpoint-mask-cases.json", m5, ["verify_second_endpoint_mask.py", "--workers", "{w}"]),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay", type=Path, required=True)
    ap.add_argument("--scratch", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--python", default=sys.executable)
    a = ap.parse_args()
    results = []
    for name, target, fn, cmd in MUTATIONS:
        d = a.scratch / f"mutation-{name}"
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(a.replay, d)
        mutate_json(d / target, fn)
        argv = [a.python, "-S", *[c.replace("{w}", str(a.workers)) for c in cmd]]
        t0 = time.monotonic()
        r = subprocess.run(argv, cwd=d, capture_output=True, text=True, check=False)
        tail = (r.stdout.strip().splitlines() or [""])[-1][:300]
        err = (r.stderr.strip().splitlines() or [""])[-1][:300]
        refused = r.returncode != 0 or "UNRESOLVED" in r.stdout
        results.append({"mutation": name, "file": target, "command": " ".join(cmd),
                        "exit": r.returncode, "refused": refused, "stdout_tail": tail,
                        "stderr_tail": err, "wall_seconds": round(time.monotonic() - t0, 1)})
        print(name, "REFUSED" if refused else "ACCEPTED", r.returncode, tail[:120], err[:160],
              flush=True)
    rep = {"program": "r1050_mutations.py", "results": results,
           "verdict": "ALL_MUTATIONS_REFUSED" if all(x["refused"] for x in results)
           else "SOME_MUTATION_ACCEPTED"}
    a.out.write_text(json.dumps(rep, indent=1) + "\n")
    print(rep["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
