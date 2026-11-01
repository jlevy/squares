#!/usr/bin/env python3
"""Every row of both filled-end deposits held to the lemma by this review's own code,
and compared with the lane's decisions receipts (stage 4 review, PR #870).

Standard library only; the construction and the hypotheses are `fe_independent`'s. The
receipts are read as data (gzip JSON) and decide nothing here: for each row this program
computes the capacity, each part's count, each band's rows, layers and free length, both
fit slacks and the least layer slack, and holds each to the receipt's value. It also
measures what the write-up quotes and what a reviewer asks of the edges: the decimal
side against the exact one, lifts at 0 and at F, the least lift room, fit and layer
slacks, the tilt range, whether a_i is ever clipped at 0, and whether the counts ever
have a zero inside them.

Given `fe_independent --all`'s two receipts (V2.0's, then V1.0's), it reads them as data
too and holds each row's placed squares to the decisions receipt's capacity.

    python -I fe_all_rows.py PACKET OUT.json [GEOMETRY_V2.json GEOMETRY_V1.json]
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import platform
import sys
import time
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fe_independent as fe  # noqa: E402

RECEIPTS = {"2": "filled-end-decisions-v2.json.gz", "1": "filled-end-decisions-v1.json.gz"}
COMPARED = (
    "capacity",
    "grid",
    "v_band",
    "h_band",
    "v_rows",
    "h_rows",
    "v_layers",
    "h_layers",
    "v_slack",
    "h_slack",
    "v_free",
    "h_free",
    "layer_slack",
    "surplus",
    "side",
    "k",
)


def lit(value: Q | None) -> str | None:
    return fe.literal(value)


def decimal_relation(row: dict) -> tuple[str, Q]:
    """How the author's decimal side stands to the exact side, and the gap in units of
    its last place (positive when the decimal is above)."""
    text = row["side_decimal"]
    places = len(text.split(".")[1])
    gap = (Q(text) - row["S"]) * 10**places
    relation = "equal" if gap == 0 else ("above" if gap > 0 else "below")
    return relation, gap


def deposit(packet: Path, version: str) -> dict:
    text, digest = fe.deposit_text(packet, version)
    rows = fe.read_rows(text)
    receipt = json.loads(gzip.decompress((packet / "receipts" / RECEIPTS[version]).read_bytes()))
    stored = {item["n"]: item for item in receipt["rows"]}
    mismatches: list[str] = []
    relations = {"equal": 0, "above": 0, "below": 0}
    worst_gap = Q(0)
    nearest = ceiling = 0
    extremes: dict[str, tuple[Q, int]] = {}
    counts = {
        "hypotheses_hold": 0,
        "side_is_K_minus_bV_plus_WV": 0,
        "side_below_K": 0,
        "K_is_ceil_sqrt_n": 0,
        "yV_zero": 0,
        "yH_zero": 0,
        "yV_at_F": 0,
        "yH_at_F": 0,
        "layer_slack_zero": 0,
        "zero_inside_counts": 0,
        "a_clipped_at_zero": 0,
        "levels_bound_above_L": 0,
    }

    def least(name: str, value: Q | None, n: int) -> None:
        if value is None:
            return
        if name not in extremes or (value, n) < extremes[name]:
            extremes[name] = (value, n)

    def most(name: str, value: Q, n: int) -> None:
        if name not in extremes or (-value, n) < (-extremes[name][0], extremes[name][1]):
            extremes[name] = (value, n)

    for row in rows:
        n, k = row["n"], row["K"]
        found = fe.hypotheses(row)
        if found["holds"]:
            counts["hypotheses_hold"] += 1
        else:
            mismatches.append(f"n={n}: a hypothesis fails: {found['hypotheses']}")
            continue
        counts["side_is_K_minus_bV_plus_WV"] += found["side_is_construction_side"]
        counts["side_below_K"] += row["S"] < k
        counts["K_is_ceil_sqrt_n"] += k == math.isqrt(n - 1) + 1
        mine = {
            "capacity": found["capacity"],
            "grid": found["grid"],
            "v_band": found["v_band"],
            "h_band": found["h_band"],
            "v_rows": found["v_rows"],
            "h_rows": found["h_rows"],
            "v_layers": found["v_layers"],
            "h_layers": found["h_layers"],
            "v_slack": lit(found["v_slack"]),
            "h_slack": lit(found["h_slack"]),
            "v_free": lit(found["v_free"]),
            "h_free": lit(found["h_free"]),
            "layer_slack": lit(found["layer_slack"]),
            "surplus": found["capacity"] - n,
            "side": lit(row["S"]),
            "k": k,
        }
        kept = stored.get(n)
        if kept is None:
            mismatches.append(f"n={n}: not in the receipt")
        else:
            for key in COMPARED:
                if mine[key] != kept.get(key):
                    mismatches.append(f"n={n}: {key} mine {mine[key]!r} receipt {kept.get(key)!r}")
            if kept.get("verdict") != "decided" or kept.get("controls_refused") != 11:
                mismatches.append(f"n={n}: the receipt does not decide it with 11 controls refused")
        relation, gap = decimal_relation(row)
        relations[relation] += 1
        worst_gap = max(worst_gap, abs(gap))
        nearest += abs(gap) <= Q(1, 2)
        ceiling += Q(0) <= gap < 1
        v, h = fe.bands(row)
        counts["yV_zero"] += row["yV"] == 0
        counts["yH_zero"] += row["yH"] == 0
        counts["yV_at_F"] += row["yV"] == v.free
        counts["yH_at_F"] += row["yH"] == h.free
        counts["layer_slack_zero"] += found["layer_slack"] == 0
        for band, lift in ((v, row["yV"]), (h, row["yH"])):
            for counts_at, at in ((band.near, lift), (band.far, band.free - lift)):
                if 0 in counts_at:
                    counts["zero_inside_counts"] += 1
                if band.s + (1 - at) * band.c / band.s <= 0:
                    counts["a_clipped_at_zero"] += 1
                if math.floor(at + band.width * band.s) + 1 > band.length:
                    counts["levels_bound_above_L"] += 1
        least("V lift room", found["v_lift_room"], n)
        least("H lift room", found["h_lift_room"], n)
        least("H fit slack", found["h_slack"], n)
        least("V fit slack", found["v_slack"], n)
        least("layer slack", found["layer_slack"], n)
        least("V length minus h", v.length - v.deep, n)
        least("H length minus h", h.length - h.deep, n)
        least("tV", row["tV"], n)
        least("tH", row["tH"], n)
        most("tV largest", row["tV"], n)
        most("tH largest", row["tH"], n)
        least("V rows", Q(v.rows), n)
        least("H rows", Q(h.rows), n)
        most("surplus largest", Q(found["capacity"] - n), n)
    zero_lift = min((r["n"] for r in rows if r["yV"] == 0 or r["yH"] == 0), default=None)
    return {
        "deposit": f"V{version}.0",
        "table_sha256": digest,
        "receipt": f"receipts/{RECEIPTS[version]}",
        "receipt_sha256_decompressed": hashlib.sha256(
            gzip.decompress((packet / "receipts" / RECEIPTS[version]).read_bytes())
        ).hexdigest(),
        "rows": len(rows),
        "receipt_rows": len(stored),
        "fields_compared": list(COMPARED),
        "mismatches": mismatches[:50],
        "mismatch_count": len(mismatches),
        "counts": counts,
        "decimal_side": {
            "relations": relations,
            "within_half_unit_of_last_place": nearest,
            "rounded_up_within_one_unit": ceiling,
            "largest_gap_in_units_of_last_place": f"{float(worst_gap):.6f}",
            "below_exact_examples": [
                {"n": r["n"], "decimal": r["side_decimal"], "exact": lit(r["S"])}
                for r in rows
                if decimal_relation(r)[0] == "below"
            ][:3],
        },
        "smallest_count_with_a_zero_lift": zero_lift,
        "extremes": {
            name: {"value": lit(value), "approx": f"{float(value):.6e}", "n": n}
            for name, (value, n) in sorted(extremes.items())
        },
    }


def geometry(path: Path, packet: Path, version: str) -> dict:
    """`fe_independent --all`'s receipt for a deposit, read as data and held to the lane's
    decisions receipt: one row per count, each verified, each placing exactly the
    receipt's capacity; with the ranges the review cites."""
    found = json.loads(path.read_text(encoding="utf-8"))
    receipt = json.loads(gzip.decompress((packet / "receipts" / RECEIPTS[version]).read_bytes()))
    capacity = {item["n"]: item["capacity"] for item in receipt["rows"]}
    rows = [row for group in found["by_K"] for row in group["rows"]]
    problems = []
    if sorted(row[0] for row in rows) != sorted(capacity):
        problems.append("the geometry receipt's counts are not the decisions receipt's")
    problems += [f"n={row[0]}: not verified" for row in rows if not row[2]]
    problems += [
        f"n={row[0]}: places {row[1]}, the receipt's capacity is {capacity.get(row[0])}"
        for row in rows
        if row[1] != capacity.get(row[0])
    ]
    return {
        "receipt": path.name,
        "receipt_program_sha256": found["program_sha256"],
        "table_sha256": found["table_sha256"],
        "rows": len(rows),
        "problems": problems[:20],
        "problem_count": len(problems),
        "squares": found["squares"],
        "pairs_decided": found["pairs_decided"],
        "touching_pairs_per_row": [min(row[4] for row in rows), max(row[4] for row in rows)],
        "wall_contacts_per_row": [min(row[5] for row in rows), max(row[5] for row in rows)],
        "denominator_digits": [min(row[6] for row in rows), max(row[6] for row in rows)],
        "cpu_seconds_rows": found["cpu_seconds_rows"],
        "wall_seconds": found["wall_seconds"],
    }


def main() -> int:
    packet = Path(sys.argv[1])
    started = time.process_time()
    found = [deposit(packet, version) for version in ("2", "1")]
    shapes = [
        geometry(Path(name), packet, version)
        for name, version in zip(sys.argv[3:5], ("2", "1"), strict=False)
    ]
    receipt = {
        "program": "fe_all_rows.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "uses": "fe_independent.py",
        "uses_sha256": hashlib.sha256(Path(fe.__file__).read_bytes()).hexdigest(),
        "environment": {"python": platform.python_version(), "machine": platform.machine()},
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cpu_seconds": round(time.process_time() - started, 1),
        "deposits": found,
        "geometry_receipts": shapes,
    }
    Path(sys.argv[2]).write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    for item in found:
        print(item["deposit"], item["rows"], "mismatches", item["mismatch_count"], item["counts"])
    for item in shapes:
        print({key: item[key] for key in item if key not in ("problems",)})
    return (
        0
        if all(item["mismatch_count"] == 0 for item in found)
        and all(item["problem_count"] == 0 for item in shapes)
        else 1
    )


if __name__ == "__main__":
    sys.exit(main())
