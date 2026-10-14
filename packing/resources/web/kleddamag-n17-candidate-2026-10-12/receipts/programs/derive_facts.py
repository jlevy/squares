"""Derive the exact facts the packet keeps from the edition, without retaining its bytes.

    packing/.venv/bin/python3 -I derive_facts.py EDITION_ROOT OUT.json

Reads as data: STATEMENT.md (parsed by compare_statement.Parser, no eval), OBLIGATIONS.json,
the capture plan, the frozen tree-checker record and the stored tree results. Writes the
numbers, polynomial coefficients, counts and identifiers the record needs, each with the
SHA-256 of the file it was read from. Nothing in the edition is executed.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare_statement import statement_facts, terms  # noqa: E402

BK = "research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/"
CAP = "research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/"
RERUN = "local-research/claude-20261002/results/rerun_trees_20261011/"
WX = "research/window-extension-20261008/"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    st_path = root / "STATEMENT.md"
    st = statement_facts(st_path.read_text(encoding="utf-8"))
    ob_path = root / BK / "OBLIGATIONS.json"
    ob = json.loads(ob_path.read_text(encoding="utf-8"))
    kinds = Counter(r["kind"] for r in ob["rows"])
    premises = [r["id"] for r in ob["rows"] if r["kind"] == "mathematical premise"]
    roots = [r["id"] for r in ob["rows"] if r["kind"] == "whole local root"]
    alg = next(r for r in ob["rows"] if r["id"] == "ALGEBRAIC_ENDPOINT")["claim"]
    consts = dict(re.findall(r"\b([RCU])=([0-9/^]+)", alg))
    g20s = next(r for r in ob["rows"] if r["id"] == "G20S_PHYSICAL")["claim"]
    ratio = re.search(r"(\d+)\s*/\s*(\d+)", g20s)
    plan_path = root / CAP / "checker_sources/PLAN_MANIFEST.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    statements = plan["statements"]
    rows_total = sum(s["total_intervals"] for s in statements)
    slices_total = sum(len(s["slices"]) for s in statements)
    row_counts = Counter(s["total_intervals"] for s in statements)
    res_path = root / RERUN / "results.tsv"
    with res_path.open(encoding="utf-8") as f:
        tree_rows = [r for r in csv.reader(f, delimiter="\t") if r]
    trees = sorted({r[0] for r in tree_rows})
    frozen_path = root / WX / "acceptance/FROZEN_30.json"
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    facts = {
        "schema": "k17-statement-facts/v1",
        "derived_by": "lane K1 of jlevy/squares#557, from the edition at 653b9589d0f8a152f01adc56b1d48ba53d49abc3",
        "statement": {
            "from": {"path": "STATEMENT.md", "sha256": sha(st_path)},
            "t0": str(st["t0"]),
            "b0": str(st["b0"]),
            "isolating_rectangle_radius": str(st["radius"]),
            "F_terms_t_b_coefficient": terms(st["F"]),
            "G_terms_t_b_coefficient": terms(st["G"]),
            "side_map": "L = (6 + 4 t*)/(1 + 2 t* - t*^2)",
            "L_enclosure_open": [st["L_lower_text"], st["L_upper_text"]],
            "claim": "a packing of seventeen unit squares exists at side L, and a packing at side S >= 0 implies L <= S; uniqueness not claimed",
        },
        "obligations": {
            "from": {"path": BK + "OBLIGATIONS.json", "sha256": sha(ob_path)},
            "total": len(ob["rows"]),
            "by_kind": dict(sorted(kinds.items())),
            "premises": premises,
            "local_roots": roots,
            "algebraic_endpoint_constants": consts,
            "rigidity_contraction_ratio": f"{ratio.group(1)}/{ratio.group(2)}" if ratio else None,
        },
        "capture": {
            "from": {"path": CAP + "checker_sources/PLAN_MANIFEST.json", "sha256": sha(plan_path)},
            "statements": len(statements),
            "rows_per_checker": rows_total,
            "slices_per_checker": slices_total,
            "statements_by_row_count": {str(k): v for k, v in sorted(row_counts.items())},
            "checkers": ["python exact_classes.py", "node verify_classes.js (file verify_classes_wb.js)"],
            "container_side_C": consts.get("C"),
        },
        "trees": {
            "from": {"path": RERUN + "results.tsv", "sha256": sha(res_path)},
            "count": len(trees),
            "names": trees,
            "checkers": {
                "C1": frozen["C1"],
                "C2": frozen["C2"],
                "SPEC": frozen["SPEC"],
                "frozen_on": frozen.get("frozen_on"),
            },
            "frozen_record": {"path": WX + "acceptance/FROZEN_30.json", "sha256": sha(frozen_path)},
        },
        "five_steps": [
            "upper bound: the known packing at side L, 68 wall and 136 pair conditions, exact",
            "capture: 98 weighted counting certificates at side at most C, leaving 11 cases",
            "admission: each case in one of 11 explicit root regions",
            "local trees: 13 tree certificates; ten regions hold no packing below L, the eleventh only packings in a tube around the known packing",
            "rigidity: a finite exact stage of 17 rounds and a contraction of ratio below 1 contradict a side below L",
        ],
    }
    out.write_text(json.dumps(facts, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in facts["obligations"].items() if k != "from"}, indent=1))
    print(json.dumps({k: v for k, v in facts["capture"].items() if k != "from"}))
    print(facts["trees"]["count"], facts["trees"]["names"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
