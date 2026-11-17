"""Decide one count's two certificate files against the issue's digests and claim.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Clean-room.

    python -I -B rv1009_check.py CERT YAML ISSUE.json N OUT.json

Reads the form P file and the form C file of count N, compares their SHA-256 with the
issue's list, and decides the packing twice: method A on the form P rows with method B on
the form C corners, and, crossed, method A on the poses taken from the form C corners
with method B on the corners written from the form P rows. Each file is thereby decided
by both methods, and the two files are compared square by square (the twin relation). It
then compares the issue's claimed side with the 12-place ceiling of the certificate's
side, writes the receipt and prints one line.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1009_files as files  # noqa: E402
import rv1009_issue as issue  # noqa: E402

WALLS = ("left", "bottom", "right", "top")
THRESHOLDS = (-28, -27, -26, -24, -21, -18, -15, -12, -9, -6, -3, -1)


def exact(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def sci(value: Fraction, digits: int = 12) -> str:
    """Truncated scientific print of an exact rational."""
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    mag = abs(value)
    exp = len(str(mag.numerator)) - len(str(mag.denominator))
    while mag >= Fraction(10) ** (exp + 1):
        exp += 1
    while mag < Fraction(10) ** exp:
        exp -= 1
    lead = mag / Fraction(10) ** exp
    scaled = lead.numerator * 10 ** (digits - 1) // lead.denominator
    text = str(scaled)
    return f"{sign}{text[0]}.{text[1:]}e{exp:+03d}"


def fixed(value: Fraction, places: int = 30) -> str:
    """Truncated fixed-point print of a non-negative exact rational."""
    scaled = value.numerator * 10**places // value.denominator
    text = str(scaled).rjust(places + 1, "0")
    return f"{text[:-places]}.{text[-places:]}"


def ceiling_12(value: Fraction) -> int:
    """The least integer k with k/10^12 >= value."""
    return -((-value.numerator * 10**12) // value.denominator)


def below(values: list[Fraction]) -> dict[str, int]:
    """How many positive values lie below each power of ten."""
    return {
        f"1e{p}": sum(1 for v in values if 0 < v < Fraction(10) ** p) for p in THRESHOLDS
    }


def summarize(result: dict, *, margins: bool) -> dict:
    """The facts of one decision, as JSON."""
    if "least_wall" not in result:
        return {"verdict": result["verdict"], "problems": result["problems"]}
    n = result["n"]
    out = {
        "verdict": result["verdict"],
        "problems": result["problems"],
        "squares": n,
        "senses_ccw": sum(1 for s in result["senses"] if s == 1),
        "senses_cw": sum(1 for s in result["senses"] if s == -1),
        "walls": {
            WALLS[w]: {
                "least_clearance": exact(result["least_wall"][w][0]),
                "least_clearance_sci": sci(result["least_wall"][w][0]),
                "at_squares": result["least_wall"][w][1],
            }
            for w in range(4)
        },
        "wall_touching": len(result["wall_touching"]),
        "wall_crossing": len(result["wall_crossing"]),
        "wall_classes_differing": len(result["wall_disagree"]),
        "squares_not_inside_by_area": len(result["not_inside_b"]),
        "area_outside_by_clipping": str(result["area_outside_b"]),
        "pairs": result["pairs"],
        "pair_classes_a": result["pair_counts_a"],
        "pair_classes_b": result["pair_counts_b"],
        "pair_classes_differing": len(result["pair_disagree"]),
        "overlap_area_by_clipping": str(result["overlap_area_b"]),
        "least_margin": exact(result["least_margin"]),
        "least_margin_sci": sci(result["least_margin"]),
        "least_margin_pair": list(result["least_pair"]),
        "margins_sha256": result["margins_sha256"],
    }
    clear = [c for row in result["clearances"] for c in row]
    out["clearances_below"] = below(clear)
    distinct = sorted(set(clear))[:6]
    out["least_clearances"] = [
        {"value": exact(v), "sci": sci(v), "count": sum(1 for c in clear if c == v)}
        for v in distinct
    ]
    if margins and result["margins"] is not None:
        values = result["margins"]
        out["margins_below"] = below(values)
        near = sorted(v for v in values if v < Fraction(1, 10**9))
        out["near_pairs_below_1e-9"] = len(near)
        out["near_pairs_distinct_values"] = len(set(near))
        out["least_margins"] = [
            {"value": exact(v), "sci": sci(v), "count": sum(1 for m in near if m == v)}
            for v in sorted(set(near))[:6]
        ]
        rest = sorted(v for v in values if v >= Fraction(1, 10**9))
        out["next_margin_at_or_above_1e-9"] = sci(rest[0]) if rest else None
    return out


def main(argv: list[str]) -> int:
    cert_path, yaml_path, issue_path, n_text, out_path = argv[1:6]
    n = int(n_text)
    started = time.process_time()
    stated = issue.read_issue(issue_path)
    cert_data = Path(cert_path).read_bytes()
    yaml_data = Path(yaml_path).read_bytes()
    cert_sha = hashlib.sha256(cert_data).hexdigest()
    yaml_sha = hashlib.sha256(yaml_data).hexdigest()
    row = stated["files"][n]
    claim_text = stated["claims"][n]["claim"]

    result = files.decide_files(cert_data, yaml_data, cross=True)
    receipt: dict = {
        "program": "rv1009_check.py",
        "lane": "c-review-1009-1117",
        "n": n,
        "files": {
            "cert": {
                "name": Path(cert_path).name,
                "bytes": len(cert_data),
                "sha256": cert_sha,
                "issue_sha256": row["cert_sha256"],
                "equal": cert_sha == row["cert_sha256"],
            },
            "yaml": {
                "name": Path(yaml_path).name,
                "bytes": len(yaml_data),
                "sha256": yaml_sha,
                "issue_sha256": row["yaml_sha256"],
                "equal": yaml_sha == row["yaml_sha256"],
            },
        },
        "problems": list(result["problems"]),
    }
    digests_ok = cert_sha == row["cert_sha256"] and yaml_sha == row["yaml_sha256"]
    if not digests_ok:
        receipt["problems"].append("a file's SHA-256 is not the issue's")
    count_ok = result.get("n") == n
    if not count_ok:
        receipt["problems"].append(f"the files do not state n = {n}")
    for key in ("read_error_p", "read_error_c"):
        if key in result:
            receipt[key] = result[key]
    if "cert" in result:
        cert = result["cert"]
        wit = result["witness"]
        receipt["reading"] = {
            "cert": {
                "comments": cert["comments"],
                "scalars": cert["scalars"],
                "noncanonical": len(cert["noncanonical"]),
                "side_text": cert["side_text"],
            },
            "yaml": {
                "id": wit["id"],
                "id_style": wit["id_style"],
                "envelope": wit["envelope"],
                "coordinates": wit["coordinates"],
                "claim": wit["claim"],
                "other_keys": wit["other_keys"],
                "scalars": wit["scalars"],
                "noncanonical": len(wit["noncanonical"]),
                "side_text": wit["side_text"],
            },
        }
    if "side" in result:
        side = result["side"]
        ceil12 = ceiling_12(side)
        claim = Fraction(claim_text)
        claim_ok = claim * 10**12 == ceil12
        receipt["side"] = {
            "exact": exact(side),
            "digits": [len(str(side.numerator)), len(str(side.denominator))],
            "to_30_places": fixed(side),
            "side_texts_equal": result["side_texts_equal"],
            "ceiling_12": fixed(Fraction(ceil12, 10**12), 12),
            "issue_claim": claim_text,
            "claim_is_ceiling_12": claim_ok,
            "claim_at_least_side": claim >= side,
            "claim_less_side": exact(claim - side),
            "claim_less_side_sci": sci(claim - side),
        }
        relations: dict[str, int] = {}
        for rel in result["twin_relations"]:
            key = "none" if rel is None else f"offset {rel[0]}, sense {rel[1]:+d}"
            relations[key] = relations.get(key, 0) + 1
        receipt["twin"] = {
            "squares_differing": result["twin_fails"],
            "relations": relations,
        }
    if "native" in result:
        receipt["decision"] = summarize(result["native"], margins=True)
        receipt["decision"]["methods"] = "A on the form P rows, B on the form C corners"
        receipt["decision_crossed"] = summarize(result["crossed"], margins=False)
        receipt["decision_crossed"]["methods"] = (
            "A on the poses taken from the form C corners, B on the corners written from "
            "the form P rows"
        )
        receipt["form_c_squares_without_pose"] = result["form_c_no_pose"]
        receipt["margin_digests_equal"] = result["margin_digests_equal"]
        receipt["clearances_equal"] = result["clearances_equal"]
        least = result["native"].get("least_margin")
        walls = result["native"].get("least_wall")
        if least is not None and walls is not None:
            least_wall = min(w[0] for w in walls)
            receipt["issue_table"] = {
                "stated": row,
                "min_wall_here": f"{float(least_wall):.3e}",
                "min_pair_here": f"{float(least):.3e}",
                "all_pairs_here": n * (n - 1) // 2,
                "min_wall_equal": f"{float(least_wall):.3e}" == row["min_wall"],
                "min_pair_equal": f"{float(least):.3e}" == row["min_pair"],
                "all_pairs_equal": str(n * (n - 1) // 2) == row["all_pairs"],
            }
    # the verdict is of the certificate: the files the issue lists, read, one packing in
    # both forms, accepted by both methods. The claim's arithmetic is reported beside it.
    accept = result["verdict"] == "ACCEPT" and digests_ok and count_ok
    receipt["verdict"] = "ACCEPT" if accept else "REFUSE"
    receipt["cpu_seconds"] = round(time.process_time() - started, 1)
    Path(out_path).write_text(json.dumps(receipt, indent=1) + "\n", encoding="ascii")
    least_text = receipt.get("decision", {}).get("least_margin_sci")
    sys.stdout.write(
        f"n={n} {receipt['verdict']} pairs={n * (n - 1) // 2} least_margin={least_text} "
        f"problems={len(receipt['problems'])} cpu={receipt['cpu_seconds']}s\n"
    )
    return 0 if accept else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
