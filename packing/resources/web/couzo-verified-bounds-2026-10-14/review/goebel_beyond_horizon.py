"""Beyond-horizon rows against Göbel's classical constructions, exactly.

Göbel's side at a count m is the least side of any member of the three closed-form
families the Kingbird catalogue states, archived in this repository, at a count n >= m
(a packing of n squares, less n - m of them, packs m):

- Göbel squares ([Kingbird-Göbel-squares], packing/resources/web/
  kingbird-squares-in-squares-gobel-squares.md): for positive integers a, b with
  a - 1 < b sqrt(2)/2 < a + 1, n = 2(a + 1)a + b^2 at side a + 1 + (b/2) sqrt(2);
- Göbel strips ([Kingbird-Göbel-strips], kingbird-squares-in-squares-gobel-strips.md):
  for a positive integer a and b = 1 + floor((a - 1) sqrt(2)), n = (a + 1)a + 2 + b at
  side a + 1 + sqrt(2)/2;
- the strip type the same page states "starting at s(18)", with the strip touching the
  two corner squares: n = (a + 1)a + 3 + b at side 2 + (b + 1) sqrt(2)/2, the same b,
  for every n >= 18.

The families generalize Frits Göbel's constructions ([Göbel 1979]), as the pages say.
Every side is held exactly as p + q sqrt(2) with p, q rational, and a rational side S is
compared with it by exact sign: S - p against q sqrt(2), squaring only when both sides
are non-negative. floor((a - 1) sqrt(2)) is math.isqrt(2 (a - 1)^2). No construction is
re-verified here; the catalogue states them, and the source's 58a7833 reports an exact
Q(sqrt 2) check of every one it uses through n = 1024 (its gobel_bounds.json).

The rows compared, each at its exact side:

- franciscouzo@487b058, the 296 certificates this packet pins
  (review/beyond-horizon-comparison.json);
- issue #607's 22 rows beyond 324 at 43ac7d2 (submissions/2026-10-14/manifest.json);
- the 4e4c8ce index's 341 rows below both 487b058's index and #607
  (certificates/best/manifest.json at 4e4c8ce, against upper_bounds.json at 487b058);
- the record's current beyond-horizon rows on main (frontier/source-coverage.yaml), each
  at its packet's exact side where its claim record states one, else at its print within
  one unit of the last place.

Run from ``packing/`` with the project interpreter::

    python -I resources/web/couzo-verified-bounds-2026-10-14/review/goebel_beyond_horizon.py \\
        --repo REPO --sub-607 SUB.json --index-4e4c8ce MANIFEST.json --index-487b058 UB.json \\
        --out .../review/goebel-beyond-horizon.json

SUB.json, MANIFEST.json and UB.json are read from franciscouzo/square-packing at the
commits named above.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import NamedTuple

import yaml

PACKET = Path("packing/resources/web/couzo-verified-bounds-2026-10-14")
LIMIT = 1100


class Form(NamedTuple):
    """A side p + q sqrt(2), the family that gives it, and the count it packs."""

    p: Fraction
    q: Fraction
    family: str
    count: int

    def text(self) -> str:
        return f"{self.p} + {self.q}*sqrt(2)"

    def margin(self, side: Fraction) -> float:
        """side - (p + q sqrt 2), with sqrt 2 to 60 places, then rounded to a float."""
        root = Fraction(math.isqrt(2 * 10**120), 10**60)
        return float(side - self.p - self.q * root)


def sign(s: Fraction, form: Form) -> int:
    """The sign of s - (p + q sqrt 2), exactly."""
    d, q = s - form.p, form.q
    if q == 0:
        return (d > 0) - (d < 0)
    if q > 0:
        if d <= 0:
            return -1
        lhs, rhs = d * d, 2 * q * q
        return (lhs > rhs) - (lhs < rhs)
    if d >= 0:
        return 1
    lhs, rhs = d * d, 2 * q * q
    return (rhs > lhs) - (rhs < lhs)


def less(x: Form, y: Form) -> bool:
    """Whether x < y, exactly."""
    dp, dq = y.p - x.p, x.q - y.q  # x < y iff dq sqrt 2 < dp
    if dq == 0:
        return dp > 0
    if dq > 0:
        return dp > 0 and 2 * dq * dq < dp * dp
    return dp >= 0 or 2 * dq * dq > dp * dp


def families(limit: int) -> list[Form]:
    forms = []
    half = Fraction(1, 2)
    for a in range(1, 40):
        for b in range(1, 80):
            # a - 1 < b sqrt(2)/2 < a + 1, i.e. 2(a - 1)^2 < b^2 < 2(a + 1)^2 for a >= 1.
            if 2 * (a - 1) ** 2 < b * b < 2 * (a + 1) ** 2:
                n = 2 * (a + 1) * a + b * b
                if n <= limit:
                    forms.append(Form(Fraction(a + 1), half * b, "Göbel square", n))
        b = 1 + math.isqrt(2 * (a - 1) ** 2)
        n = (a + 1) * a + 2 + b
        if n <= limit:
            forms.append(Form(Fraction(a + 1), half, "Göbel strip", n))
        n = (a + 1) * a + 3 + b
        if 18 <= n <= limit:
            forms.append(Form(Fraction(2), half * (b + 1), "corner-touching Göbel strip", n))
    return forms


def goebel_at(m: int, forms: list[Form]) -> Form | None:
    best = None
    for form in forms:
        if form.count >= m and (best is None or less(form, best)):
            best = form
    return best


def compare(label: str, rows: list[tuple[int, Fraction, str]], forms: list[Form]) -> dict:
    out = []
    for n, side, note in rows:
        g = goebel_at(n, forms)
        if g is None:
            continue
        s = sign(side, g)
        relation = {1: "above", 0: "equal", -1: "below"}[s]
        out.append({
            "n": n,
            "side": f"{side.numerator}/{side.denominator}",
            "goebel": g.text(),
            "goebel_family": g.family,
            "goebel_from_count": g.count,
            "relation": relation,
            "margin": g.margin(side),
            "note": note,
        })
    tally = {r: sum(1 for x in out if x["relation"] == r) for r in ("above", "equal", "below")}
    return {"set": label, "rows": len(out), "tally": tally,
            "above": [x["n"] for x in out if x["relation"] == "above"], "detail": out}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--sub-607", required=True)
    ap.add_argument("--index-4e4c8ce", required=True)
    ap.add_argument("--index-487b058", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    repo = Path(a.repo)
    forms = families(LIMIT)

    comparison = json.loads((repo / PACKET / "review/beyond-horizon-comparison.json").read_text())
    rows_487 = [(r["n"], Fraction(r["side"]), r["verdict"]) for r in comparison["rows"]]

    sub = json.loads(Path(a.sub_607).read_text())["certificates"]
    rows_607 = [
        (int(c["n"]), Fraction(c["rational_side"]), c.get("group", ""))
        for c in sub
        if int(c["n"]) > 324
    ]
    side_607 = {n: s for n, s, _ in rows_607}

    index = json.loads(Path(a.index_4e4c8ce).read_text())["witnesses"]
    previous = json.loads(Path(a.index_487b058).read_text())["entries"]
    rows_4e = []
    for k, w in index.items():
        n = int(k)
        if n <= 324 or not w.get("bound"):
            continue
        try:
            side = Fraction(w["bound"])
        except ValueError:
            continue
        earlier = [Fraction(previous[k]["verified"]["bound"])] if k in previous else []
        earlier += [side_607[n]] if n in side_607 else []
        if earlier and side < min(earlier):
            category = (w.get("provenance") or {}).get("category") or w.get("kind")
            rows_4e.append((n, side, f"{w.get('credit')}; {category}"))

    coverage = yaml.safe_load((repo / "packing/frontier/source-coverage.yaml").read_text())
    exact = {}
    for path in (repo / "packing/resources/web").glob("*/acquisition/*claims.json"):
        d = json.loads(path.read_text())
        if isinstance(d, dict) and isinstance(d.get("results"), list):
            for r in d["results"]:
                if isinstance(r.get("n"), int) and r["n"] > 324 and r.get("exact_side"):
                    try:
                        exact[(path.parts[-3], r["n"])] = Fraction(r["exact_side"])
                    except ValueError:
                        pass
    rows_record = []
    for row in coverage["beyond_horizon_claims"]:
        if row.get("disposition") == "superseded":
            continue
        key = (row["source_id"], row["n"])
        side = exact.get(key, Fraction(str(row["value"])))
        note = row["source_id"] + ("" if key in exact else " (print)")
        rows_record.append((row["n"], side, note))

    report = {
        "format": "goebel-beyond-horizon-v1",
        "families": [
            "Göbel square: n = 2(a+1)a + b^2, s = a + 1 + (b/2) sqrt 2, a - 1 < b sqrt(2)/2 < a + 1",
            "Göbel strip: n = (a+1)a + 2 + b, s = a + 1 + sqrt(2)/2, b = 1 + floor((a-1) sqrt 2)",
            "corner-touching strip: n = (a+1)a + 3 + b, s = 2 + (b+1) sqrt(2)/2, same b, n >= 18",
        ],
        "sources": ["[Kingbird-Göbel-squares]", "[Kingbird-Göbel-strips]", "[Göbel 1979]"],
        "deletion": "Göbel's side at m is the least side of any member at a count n >= m",
        "sets": [
            compare("franciscouzo@487b058 (this packet)", rows_487, forms),
            compare("#607 at 43ac7d2", rows_607, forms),
            compare("4e4c8ce index, below 487b058 and #607", rows_4e, forms),
            compare("record's current beyond-horizon rows (main)", rows_record, forms),
        ],
    }
    head = {k: v for k, v in report.items() if k != "sets"}
    lines = ["{"] + [f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}," for k, v in head.items()]
    lines.append('  "sets": [')
    blocks = []
    for s in report["sets"]:
        inner = {k: v for k, v in s.items() if k != "detail"}
        body = ",\n".join("      " + json.dumps(x, ensure_ascii=False) for x in s["detail"])
        text = "    {\n" + "".join(
            f"      {json.dumps(k)}: {json.dumps(v)},\n" for k, v in inner.items()
        )
        blocks.append(text + '      "detail": [\n' + body + "\n      ]\n    }")
    lines.append(",\n".join(blocks))
    lines.append("  ]\n}")
    Path(a.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    for s in report["sets"]:
        print(s["set"], s["rows"], s["tally"], "above:", s["above"])


if __name__ == "__main__":
    main()
