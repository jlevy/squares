"""Self-test of the r1050 checkers on synthetic inputs only (never the source's data).

Usage: python -I r1050_selftest.py --scratch DIR --out selftest.json

Each case states the outcome the checker must give; the test fails if any differs.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

RACKS = {
    "one-mark-small-box": ('{"cap": "6/5", "orbits": [[1000, 1000]], "scale": 2000, '
                           '"erosion": "1/100000", "depth": 1, "marks": 1}', 0, "COVERED"),
    "one-mark-large-box": ('{"cap": "11/5", "orbits": [[1000, 1000]], "scale": 2000, '
                           '"erosion": "1/100000", "depth": 1, "marks": 1}', 1,
                           "UNCOVERED_POSE_FOUND"),
    "five-marks-box-2": ('{"cap": "2", "orbits": [[500, 500], [1000, 1000]], "scale": 2000, '
                         '"erosion": "1/100000", "depth": 1, "marks": 5}', 1,
                         "UNCOVERED_POSE_FOUND"),
}
CONSTRUCTIONS = {
    # 2x2 grid in a box of side 2: valid, but the side is not H, so the verdict refuses it.
    "grid-2x2": ('{"field": "sqrt(7)", "side": ["2", "0"], "centers": [[1, 0, ["1/2","0"], '
                 '["1/2","0"]], [2, 0, ["3/2","0"], ["1/2","0"]], [3, 0, ["1/2","0"], '
                 '["3/2","0"]], [4, 0, ["3/2","0"], ["3/2","0"]]]}', True, 6, 8),
    # Two overlapping squares.
    "overlap": ('{"field": "sqrt(7)", "side": ["2", "0"], "centers": [[1, 0, ["1/2","0"], '
                '["1/2","0"]], [2, 0, ["5/4","0"], ["1/2","0"]]]}', False, 0, 3),
    # A tile in the source's tilted frame, centred at (2, 2) in a box of side 3.
    "tilted": ('{"field": "sqrt(7)", "side": ["3", "0"], "centers": [[1, 0, ["1/2","0"], '
               '["1/2","0"]], [2, 1, ["2","0"], ["2","0"]]]}', True, 0, 2),
}


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-I", *args], capture_output=True, text=True,
                          check=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    d = a.scratch / "r1050-selftest"
    d.mkdir(parents=True, exist_ok=True)
    fails: list[str] = []
    for name, (text, code, verdict) in RACKS.items():
        (d / f"{name}.json").write_text(text)
        r = run([str(HERE / "r1050_rack.py"), "--rack", str(d / f"{name}.json"),
                 "--out", str(d / f"{name}.out.json")])
        got = json.loads((d / f"{name}.out.json").read_text())["verdict"]
        if r.returncode != code or got != verdict:
            fails.append(f"rack {name}: {got} exit {r.returncode}")
    for name, (text, valid, contacts, walls) in CONSTRUCTIONS.items():
        (d / f"{name}.json").write_text(text)
        run([str(HERE / "r1050_construction.py"), "--construction", str(d / f"{name}.json"),
             "--out", str(d / f"{name}.out.json")])
        chk = json.loads((d / f"{name}.out.json").read_text())["check"]
        if (chk["valid"], len(chk["pair_contacts"]), len(chk["wall_contacts"])) != (
                valid, contacts, walls):
            fails.append(f"construction {name}: {chk['valid']} {len(chk['pair_contacts'])}")
    r = run([str(HERE / "r1050_orbits.py"), "--rack", str(d / "five-marks-box-2.json"),
             "--out", str(d / "orbits5.json")])
    o = json.loads((d / "orbits5.json").read_text())
    if (o["orbits"], o["burnside"], o["subsets"]) != (3, 3, 10):
        fails.append(f"orbits: {o['orbits']} {o['burnside']}")
    (d / "rack201.json").write_text('{"cap": "201/100", "orbits": [[500, 500], [1000, 1000]], '
                                    '"scale": 2000, "erosion": "1/100000", "depth": 1, '
                                    '"marks": 5}')
    run([str(HERE / "r1050_orbits.py"), "--rack", str(d / "rack201.json"), "--construction",
         str(d / "grid-2x2.json"), "--witness-out", str(d / "w.json")])
    w = json.loads((d / "w.json").read_text())
    if w["witness_orbits"] != [[[1000, 1000]]] or len(w["loose_moves"]) != 4:
        fails.append(f"witness: {w['witness_orbits']} {len(w['loose_moves'])}")
    rep = {"program": "r1050_selftest.py", "fails": fails,
           "verdict": "PASS" if not fails else "FAIL"}
    a.out.write_text(json.dumps(rep, indent=1) + "\n")
    print(rep["verdict"], fails)
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
