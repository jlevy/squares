"""Exact side arithmetic for the L70 review: sides, prints, gaps against the record.

Reads each certificate's header through the frozen reader and compares, exactly:

* the side with the author's prints (PACKINGS.md's table and prose, and
  packing-certificates.json's side_exact, side_decimal and improvement);
* the side with the standing value at its count on ``main`` ``ef1af4933``: T-277 at
  299, T-278 at 303, T-259 at 130 (their retained certificates), and beyond the
  horizon the current row (its printed value in source-coverage.yaml and the exact
  side of the certificate the record retains for it).

Usage: python -I l70_sides.py --src SRC --repo REPO --out sides.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import l70_check as C  # noqa: E402
import l70_reader as R  # noqa: E402

BH = (553, 599, 600, 601, 602, 604, 645, 647, 648, 699, 700)
WEB = "packing/resources/web"


def side_of(pk: R.Packing) -> F:
    return F(pk.side[0], pk.side[1])


def terminates(q: int) -> bool:
    for p in (2, 5):
        while q % p == 0:
            q //= p
    return q == 1


def nearest_places(x: F, k: int) -> str:
    v = x * 10**k
    r = (2 * v.numerator + v.denominator) // (2 * v.denominator)  # round half up
    s = str(r).rjust(k + 1, "0")
    return f"{s[:-k]}.{s[-k:]}"


def decimal_relation(exact: F, printed: str) -> str:
    """How a printed decimal relates to the exact value: equal, truncation, ceiling, nearest, other."""
    m = re.fullmatch(r"(\d+)\.(\d+)", printed)
    if not m:
        return "unparsed"
    k = len(m.group(2))
    p = F(printed)
    if p == exact:
        return f"exact ({k} places)"
    rel = []
    if printed == C.floor_places(exact, k):
        rel.append("floor")
    if printed == C.ceil_places(exact, k):
        rel.append("ceiling")
    if printed == nearest_places(exact, k):
        rel.append("nearest")
    return f"{'/'.join(rel) or 'other'} at {k} places"


def sci(x: F, digits: int = 13) -> str:
    return f"{float(x):.{digits}e}" if x != 0 else "0"


def ulp_at(x: F) -> float:
    import math

    return math.ulp(float(x))


def describe(x: F) -> dict[str, Any]:
    return {
        "exact": C.frac_str(x),
        "denominator_digits": len(str(x.denominator)),
        "terminates": terminates(x.denominator),
        "floor_40": C.floor_places(x, 40),
        "ceil_12": C.ceil_places(x, 12),
        "ceil_16": C.ceil_places(x, 16),
        "floor_12": C.floor_places(x, 12),
    }


def gap(record: F, new: F) -> dict[str, Any]:
    g = record - new
    return {
        "record_minus_new": C.frac_str(g),
        "float": float(g),
        "sci": sci(g),
        "relative": float(g / record),
        "units_of_12th_place": float(g * 10**12),
        "binary64_spacings_at_side": float(g) / ulp_at(new),
        "same_12_place_ceiling": C.ceil_places(record, 12) == C.ceil_places(new, 12),
        "new_ceil_12": C.ceil_places(new, 12),
        "record_ceil_12": C.ceil_places(record, 12),
    }


def packings_md_table(text: str) -> dict[int, str]:
    out = {}
    for line in text.splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*\[n\d+\.cert\]\(n\d+\.cert\)\s*\|\s*([0-9.]+)\s*\|", line)
        if m:
            out[int(m.group(1))] = m.group(2)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args()
    src = Path(ns.src)
    repo = Path(ns.repo)
    head = src / "ac14112"
    import yaml

    meta = json.loads((head / "packing-certificates.json").read_text())
    by_n = {c["n"]: c for c in meta["certificates"]}
    table = packings_md_table((head / "PACKINGS.md").read_text())
    table_first = packings_md_table((src / "78eb9ea" / "PACKINGS.md").read_text())
    meta_first = json.loads((src / "78eb9ea" / "packing-certificates.json").read_text())
    by_n_first = {c["n"]: c for c in meta_first["certificates"]}
    cov = yaml.load((repo / "packing/frontier/source-coverage.yaml").read_text(), Loader=yaml.CSafeLoader)
    out: dict[str, Any] = {"program": "l70_sides.py", "program_digests": C.file_digests(C.CHECKER_FILES + ("l70_sides.py",))}

    houses = {
        299: ("T-277", R.read_corners_yaml(repo / WEB / "ozden-s299-upper-bound-2026-11-09/source/n-299-candidate.yaml")),
        303: ("T-278", R.read_corners_yaml(repo / WEB / "ozden-s303-upper-bound-2026-11-09/source/n-303-candidate.yaml")),
        130: ("T-259", R.read_cert(repo / WEB / "mishapolk-issue846-2026-10-30/source/certificates/0000-0999/n130.cert")),
    }
    entries: dict[str, Any] = {}
    for n in (299, 303, 130):
        pk = R.read_cert(head / f"n{n}.cert")
        s = side_of(pk)
        tid, hpk = houses[n]
        hs = side_of(hpk)
        m = by_n[n]
        e = {
            "file": f"n{n}.cert",
            "sha256": pk.meta["sha256"],
            "side": describe(s),
            "author_table_print": table.get(n),
            "author_table_print_relation": decimal_relation(s, table[n]) if n in table else None,
            "json_side_exact_equal": F(m["side_exact"]) == s,
            "json_side_decimal_relation": decimal_relation(s, m["side_decimal"]),
            "house": tid,
            "house_sha256": hpk.meta["sha256"],
            "json_source_sha256_equal": m.get("source_sha256") == hpk.meta["sha256"],
            "house_side": describe(hs),
            "json_source_exact_side_equal": F(m["source_exact_side"]) == hs,
            "gap": gap(hs, s),
        }
        imp = m.get("exact_side_improvement_decimal")
        if imp:
            mant, exp = imp.split("E")
            digits = mant.replace(".", "").lstrip("0")
            e["json_improvement"] = imp
            g = hs - s
            # the printed mantissa times 10^exp, against the exact gap; and its relation at the
            # printed number of significant digits (scaled so the mantissa is a decimal)
            pv = F(mant) * F(10) ** int(exp)
            e["json_improvement_minus_exact"] = sci(pv - g)
            e["json_improvement_digits"] = len(digits)
            e["json_improvement_relation"] = decimal_relation(g * F(10) ** (-int(exp)), mant)
        entries[f"yim-n{n}"] = e
    # the first n303 (78eb9ea)
    pk = R.read_cert(src / "78eb9ea" / "n303.cert")
    s = side_of(pk)
    hs = side_of(houses[303][1])
    m = by_n_first[303]
    entries["yim-n303-first"] = {
        "file": "78eb9ea:n303.cert",
        "sha256": pk.meta["sha256"],
        "side": describe(s),
        "author_table_print_78eb9ea": table_first.get(303),
        "author_table_print_relation": decimal_relation(s, table_first[303]) if 303 in table_first else None,
        "json_side_exact_equal": F(m["side_exact"]) == s,
        "json_side_decimal_relation": decimal_relation(s, m["side_decimal"]),
        "house": "T-278",
        "gap": gap(hs, s),
    }
    # beyond the horizon
    rows = cov["beyond_horizon_claims"]
    for n in BH:
        pk = R.read_cert(head / f"n{n}.cert")
        s = side_of(pk)
        current = [r for r in rows if r["n"] == n and r["disposition"] != "superseded"]
        cur = current[0] if len(current) == 1 else None
        if n == 604:
            cpath = repo / WEB / "couzo-43f666c-2026-10-24/source/certificates/best/n604.cert"
        else:
            cpath = repo / WEB / f"couzo-issue763-2026-10-23/source/certificates/best/n{n}.cert"
        cpk = R.read_cert(cpath)
        cs = side_of(cpk)
        m = by_n[n]
        printed = F(cur["value"]) if cur else None
        entries[f"yim-n{n}"] = {
            "file": f"n{n}.cert",
            "sha256": pk.meta["sha256"],
            "side": describe(s),
            "author_table_print": table.get(n),
            "author_table_print_relation": decimal_relation(s, table[n]) if n in table else None,
            "json_side_exact_equal": F(m["side_exact"]) == s,
            "json_side_decimal_relation": decimal_relation(s, m["side_decimal"]),
            "current_rows": current,
            "row_print": cur["value"] if cur else None,
            "row_print_relation_to_certificate": decimal_relation(cs, cur["value"]) if cur else None,
            "couzo_certificate": str(cpath.relative_to(repo)),
            "couzo_sha256": cpk.meta["sha256"],
            "couzo_side": describe(cs),
            "gap_to_certificate": gap(cs, s),
            "gap_to_print": {"float": float(printed - s), "sci": sci(printed - s)} if printed is not None else None,
            "below_print": bool(printed is not None and s < printed),
        }
    out["entries"] = entries
    Path(ns.out).write_text(json.dumps(out, indent=1) + "\n")
    for k, v in entries.items():
        g = v.get("gap") or v.get("gap_to_certificate")
        print(k, v["side"]["ceil_12"], "gap", g["sci"], "same print" if g["same_12_place_ceiling"] else "print differs", "| table", v.get("author_table_print_relation") or v.get("author_table_print_relation"), "| json decimal", v["json_side_decimal_relation"], "| json exact", v["json_side_exact_equal"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
