"""Lane L174: compare the author's floating-point CSV with the exact construction.

Usage: ``python -I -B l174_csv_check.py N977_COORDINATES.csv K0.json C7.json OUT.json``

Numerical only; it decides nothing about the bound.  The CSV gives centres (x, y) and an
angle in radians.  Each row is matched to the nearest square of the same orientation in
three exact references evaluated to 50 digits:

* C7: the construction rebuilt at side 637/20 = 31.85 (unit squares, re-centred);
* K0: the construction at its exact side 17 + 21/sqrt 2;
* K0 scaled: K0's centres multiplied by 31.85 / (17 + 21/sqrt 2).

It reports whether the match is one to one, the largest centre deviation, and the
largest deviation of the angles from 0 and pi/4.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 50
ROOT2 = Decimal(2).sqrt()
PI4 = Decimal("0.78539816339744830961566084581987572104929234984378")


def qdec(pair: list[str]) -> Decimal:
    def frac(text: str) -> Decimal:
        if "/" in text:
            p, q = text.split("/")
            return Decimal(p) / Decimal(q)
        return Decimal(text)

    return frac(pair[0]) + frac(pair[1]) * ROOT2


def load_ref(path: Path, factor: Decimal = Decimal(1)) -> list[tuple[str, int, Decimal, Decimal]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [
        (s["label"], s["angle"], qdec(s["cx"]) * factor, qdec(s["cy"]) * factor)
        for s in data["squares"]
    ]


def match(rows: list[dict[str, object]], ref: list[tuple[str, int, Decimal, Decimal]]) -> dict[str, object]:
    by_angle: dict[int, list[tuple[str, float, float, Decimal, Decimal]]] = {0: [], 45: []}
    for label, ang, x, y in ref:
        by_angle[ang].append((label, float(x), float(y), x, y))
    used: dict[str, int] = {}
    worst = Decimal(0)
    worst_row = -1
    for row in rows:
        ang = int(row["cls"])  # pyright: ignore[reportArgumentType]
        fx, fy = float(row["x"]), float(row["y"])  # pyright: ignore[reportArgumentType]
        best = min(by_angle[ang], key=lambda c: (c[1] - fx) ** 2 + (c[2] - fy) ** 2)
        used[best[0]] = used.get(best[0], 0) + 1
        dev = max(abs(best[3] - row["x"]), abs(best[4] - row["y"]))  # pyright: ignore[reportOperatorIssue]
        if dev > worst:
            worst, worst_row = dev, int(row["id"])  # pyright: ignore[reportArgumentType]
        row.setdefault("matches", {})
        row["matches"][len(row["matches"])] = best[0]  # pyright: ignore[reportIndexIssue]
    one_to_one = len(used) == len(rows) and all(v == 1 for v in used.values())
    return {
        "one_to_one": one_to_one,
        "max_centre_deviation": f"{worst:.3E}",
        "at_row": worst_row,
    }


def main(argv: list[str]) -> int:
    csv_path, k0_path, c7_path, out_path = (Path(a) for a in argv[1:5])
    raw = csv_path.read_bytes()
    rows: list[dict[str, object]] = []
    max_dev_45 = Decimal(0)
    max_dev_0 = Decimal(0)
    header: list[str] = []
    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        header = list(reader.fieldnames or [])
        for rec in reader:
            ang = Decimal(rec["angle"])
            cls = 45 if abs(ang - PI4) < Decimal("1e-9") else (0 if abs(ang) < Decimal("1e-9") else -1)
            if cls == 45:
                max_dev_45 = max(max_dev_45, abs(ang - PI4))
            elif cls == 0:
                max_dev_0 = max(max_dev_0, abs(ang))
            rows.append(
                {
                    "id": int(rec["id"]),
                    "n": int(rec["n"]),
                    "square_id": int(rec["square_id"]),
                    "x": Decimal(rec["x"]),
                    "y": Decimal(rec["y"]),
                    "cls": cls,
                }
            )
    side = Decimal(17) + Decimal(21) / 2 * ROOT2
    refs = {
        "C7_rebuilt_at_31.85": load_ref(c7_path),
        "K0_exact_side": load_ref(k0_path),
        "K0_scaled_to_31.85": load_ref(k0_path, Decimal("31.85") / side),
    }
    results = {name: match(rows, ref) for name, ref in refs.items()}
    c7_labels = [row["matches"][0] for row in rows]  # pyright: ignore[reportIndexIssue]
    out = {
        "csv_sha256": hashlib.sha256(raw).hexdigest(),
        "header": header,
        "rows": len(rows),
        "n_column": sorted({row["n"] for row in rows}),  # pyright: ignore[reportArgumentType]
        "ids_in_order": [row["id"] for row in rows] == list(range(len(rows))),
        "square_ids_in_order": [row["square_id"] for row in rows] == list(range(len(rows))),
        "angle_classes": {
            "45": sum(1 for r in rows if r["cls"] == 45),
            "0": sum(1 for r in rows if r["cls"] == 0),
            "other": sum(1 for r in rows if r["cls"] == -1),
        },
        "max_angle_deviation_from_pi_4": f"{max_dev_45:.3E}",
        "max_angle_deviation_from_0": f"{max_dev_0:.3E}",
        "box_extent": {
            "x_min_centre": f"{min(r['x'] for r in rows)}",  # pyright: ignore[reportArgumentType]
            "x_max_centre": f"{max(r['x'] for r in rows)}",  # pyright: ignore[reportArgumentType]
        },
        "references": results,
        "row_order_vs_C7": {
            "first_rows": c7_labels[:3],
            "rows_441_443": c7_labels[441:444],
            "same_order_as_l174_ids": c7_labels
            == [s[0] for s in refs["C7_rebuilt_at_31.85"]],
        },
    }
    Path(out_path).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
