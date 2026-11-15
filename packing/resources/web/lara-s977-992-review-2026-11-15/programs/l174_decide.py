"""Lane L174: decide one construction file by both methods and compare them.

Usage: ``python -I -B l174_decide.py CONSTRUCTION.json RECEIPT.json``

The receipt records, for each method, the counts of apart, touching and overlapping
pairs, the overlapping pairs by label, the wall classes, the unit-square test, and the
SHA-256 of the full per-pair class vector; and whether the two methods agree on every
pair, every wall and every square.  Exit status 0 means the file was decided (whatever
the verdict), not that it is a packing.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
from pathlib import Path

# Run with -I, which leaves the script's own directory off sys.path: put it back, alone.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import l174_method_a as method_a
import l174_method_b as method_b
from l174_reader import read

WALLS = ("left", "bottom", "right", "top")


def _summary(con_labels: list[str], res: dict[str, object]) -> dict[str, object]:
    walls: list[tuple[int, int, int, int]] = res["walls"]  # pyright: ignore[reportAssignmentType]
    crossing = [
        f"{con_labels[i]}:{WALLS[k]}" for i, w in enumerate(walls) for k in range(4) if w[k] < 0
    ]
    touching_w = [
        f"{con_labels[i]}:{WALLS[k]}" for i, w in enumerate(walls) for k in range(4) if w[k] == 0
    ]
    unit: list[bool] = res["unit"]  # pyright: ignore[reportAssignmentType]
    over: list[tuple[int, int]] = res["overlapping_pairs"]  # pyright: ignore[reportAssignmentType]
    touch: list[tuple[int, int]] = res["touching_pairs"]  # pyright: ignore[reportAssignmentType]
    out: dict[str, object] = {
        "method": res["method"],
        "pairs": res["pairs"],
        "apart": res["apart"],
        "touching": res["touching"],
        "overlapping": res["overlapping"],
        "overlapping_pairs": [[con_labels[i], con_labels[j]] for i, j in over],
        "touching_pairs_sha256": hashlib.sha256(
            json.dumps([[i, j] for i, j in touch]).encode()
        ).hexdigest(),
        "pair_class_sha256": res["pair_class_sha256"],
        "wall_class_sha256": res["wall_class_sha256"],
        "wall_touching": len(touching_w),
        "wall_touching_squares": sum(1 for w in walls if 0 in w),
        "wall_crossing": len(crossing),
        "wall_crossing_squares": sum(1 for w in walls if min(w) < 0),
        "wall_crossing_list": crossing,
        "non_unit": [con_labels[i] for i, u in enumerate(unit) if not u],
    }
    if "overlap_areas" in res:
        out["overlap_areas"] = res["overlap_areas"]
    if "inside_by_area" in res:
        inside: list[bool] = res["inside_by_area"]  # pyright: ignore[reportAssignmentType]
        out["not_inside_by_area"] = [con_labels[i] for i, k in enumerate(inside) if not k]
    return out


def decide_file(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    con = read(path)
    labels = [s.label for s in con.squares]
    t0 = time.perf_counter()
    res_a = method_a.decide(con)
    t1 = time.perf_counter()
    res_b = method_b.decide(con)
    t2 = time.perf_counter()
    sum_a = _summary(labels, res_a)
    sum_b = _summary(labels, res_b)
    agree = {
        "pair_classes": res_a["pair_class_sha256"] == res_b["pair_class_sha256"],
        "touching_pairs": res_a["touching_pairs"] == res_b["touching_pairs"],
        "overlapping_pairs": res_a["overlapping_pairs"] == res_b["overlapping_pairs"],
        "walls": res_a["walls"] == res_b["walls"],
        "unit": res_a["unit"] == res_b["unit"],
    }
    n = len(con.squares)
    a_ok = (
        sum_a["overlapping"] == 0
        and sum_a["wall_crossing"] == 0
        and not sum_a["non_unit"]
    )
    b_ok = (
        sum_b["overlapping"] == 0
        and sum_b["wall_crossing"] == 0
        and not sum_b["non_unit"]
        and not sum_b["not_inside_by_area"]
    )
    families: dict[str, int] = {}
    for s in con.squares:
        families[s.family] = families.get(s.family, 0) + 1
    return {
        "file": path.name,
        "file_sha256": hashlib.sha256(raw).hexdigest(),
        "name": con.name,
        "container": [str(con.container[0]), str(con.container[1])],
        "n": n,
        "angles": {
            "0": sum(1 for s in con.squares if s.angle == 0),
            "45": sum(1 for s in con.squares if s.angle == 45),
        },
        "families": families,
        "A": sum_a,
        "B": sum_b,
        "agree": agree,
        "all_agree": all(agree.values()),
        "verdict_A": "packing" if a_ok else "not a packing",
        "verdict_B": "packing" if b_ok else "not a packing",
        "seconds": {"A": round(t1 - t0, 2), "B": round(t2 - t1, 2)},
        "python": platform.python_version(),
    }


def main(argv: list[str]) -> int:
    receipt = decide_file(Path(argv[1]))
    Path(argv[2]).write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    brief = {
        k: receipt[k]
        for k in ("name", "n", "all_agree", "verdict_A", "verdict_B", "seconds")
    }
    brief["A"] = {
        k: receipt["A"][k]  # pyright: ignore[reportIndexIssue]
        for k in ("touching", "overlapping", "wall_touching", "wall_crossing")
    }
    print(json.dumps(brief))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
