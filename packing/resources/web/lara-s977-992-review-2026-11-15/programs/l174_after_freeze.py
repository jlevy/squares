"""Lane L174, after the freeze: three related constructions, and Göbel's families with L-borders.

Usage (from ``packing/``): ``python -I -B l174_after_freeze.py OUTDIR``

Written after the findings were frozen (2026-11-15T07:15:34Z, pushed as ``56ea1fd3c``).
It changes nothing that was frozen: it builds three more construction files with the
frozen ``l174_construct.build`` and leaves deciding them to the frozen ``l174_decide.py``.

* ``A981``: K0 and one upright square centred at the middle of each side's outer row,
  (C, 1/2), (L - 1/2, C), (C, L - 1/2), (1/2, C).  Expected: a packing, no new touching
  pair, 124 wall contacts.
* ``G982``: Göbel's square member (a, b) = (15, 21) (921 squares at 16 + 21/sqrt 2: the
  21 x 21 diamond and four corner triangles of rows 15, 14, ..., 1), translated by (1, 1),
  with Friedman's L-border: 31 squares along the bottom, 30 up the left.  982 squares at
  17 + 21/sqrt 2.  Expected: a packing.
* ``G985``: Göbel's (a, b) = (16, 21) taken literally (985 squares at 17 + 21/sqrt 2: corner
  triangles of rows 16, ..., 1), outside the family's window a - 1 < b/sqrt 2.  Expected:
  not a packing, exactly four overlapping pairs, the two bottom-row ends meeting on each
  side: (BL(15,0), BR(0,15)) and its three quarter-turn images.

It also writes ``goebel-with-borders.json``: from ``devtools.goebel_construction``'s
families (the maintained module, read after the freeze), every member with up to three
L-border layers (side s + k, count n + sum_{j<k} (2 floor(s + j) + 1), Friedman's
"n + 2s(n) + 1"), and the least side reaching each count from 970 to 990, against the
module's own side there.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(Path.cwd()))

from devtools import goebel_construction as goebel  # noqa: E402
from l174_construct import SIDE, Spec, build, q_add, q_half, q_sub, rat  # noqa: E402

F = Fraction


def enc(p: tuple[Fraction, Fraction]) -> list[str]:
    return [str(p[0]), str(p[1])]


def add_square(data: dict, label: str, family: str, cx, cy) -> None:  # noqa: ANN001
    squares = data["squares"]
    squares.append(
        {
            "id": len(squares),
            "label": label,
            "family": family,
            "cx": enc(cx),
            "cy": enc(cy),
            "angle": 0,
            "size": "1",
        }
    )
    data["n"] = len(squares)


def a981() -> dict:
    data = build(Spec("A981", "K0 plus the middle square of each side's outer row"))
    data["name"] = "A981"
    c = q_half(SIDE)
    h = rat(F(1, 2))
    add_square(data, "M(bottom)", "border-middle", c, h)
    add_square(data, "M(right)", "border-middle", q_sub(SIDE, h), c)
    add_square(data, "M(top)", "border-middle", c, q_sub(SIDE, h))
    add_square(data, "M(left)", "border-middle", h, c)
    return data


def g982() -> dict:
    inner = (F(16), F(21, 2))
    data = build(
        Spec("G982", "Göbel (15, 21) translated by (1, 1) plus an L-border", side=inner,
             widths=tuple(range(15, 0, -1)))
    )
    one = rat(1)
    for row in data["squares"]:
        row["cx"] = enc(q_add((F(row["cx"][0]), F(row["cx"][1])), one))
        row["cy"] = enc(q_add((F(row["cy"][0]), F(row["cy"][1])), one))
    data["name"] = "G982"
    data["construction_side"] = enc(SIDE)
    data["container"] = enc(SIDE)
    width = SIDE[0] + SIDE[1] * Fraction(math.isqrt(2 * 10**40), 10**20)  # floor only
    bottom = math.floor(width)  # 31
    for k in range(bottom):
        add_square(data, f"Lb({k})", "L-border", rat(F(k) + F(1, 2)), rat(F(1, 2)))
    for k in range(bottom - 1):  # 30, from y = 1
        add_square(data, f"Ll({k})", "L-border", rat(F(1, 2)), rat(F(k) + F(3, 2)))
    return data


def g985() -> dict:
    data = build(
        Spec("G985", "Göbel (16, 21) taken literally", side=SIDE, widths=tuple(range(16, 0, -1)))
    )
    return data


def borders() -> dict:
    forms = goebel.families(2000)
    extended: list[tuple[goebel.Form, str]] = []
    for f in forms:
        assert f.p.denominator == 1 and f.q >= 0
        # floor(p + q sqrt 2) = p + isqrt(floor(2 q^2)), exactly, for integer p and q >= 0
        s_floor = int(f.p) + math.isqrt(math.floor(2 * f.q * f.q))
        n = f.count
        for k in range(4):
            label = f"{f.family} n={f.count} side {f.text()}" + (f" + {k} L" if k else "")
            extended.append((goebel.Form(f.p + k, f.q, f.family, n), label))
            n += 2 * (s_floor + k) + 1
    out: dict[str, object] = {}
    for m in range(970, 991):
        best: tuple[goebel.Form, str] | None = None
        for form, lab in extended:
            if form.count >= m and (best is None or goebel.less(form, best[0])):
                best = (form, lab)
        assert best is not None
        mod = goebel.side(m)
        out[str(m)] = {
            "least_with_L_borders": best[1],
            "its_side": best[0].text(),
            "its_value": float(best[0].p) + float(best[0].q) * math.sqrt(2),
            "its_count": best[0].count,
            "module_side": mod.text(),
            "module_family": mod.family,
            "module_count": mod.count,
            "module_value": float(mod.p) + float(mod.q) * math.sqrt(2),
        }
    return out


def main(argv: list[str]) -> int:
    out = Path(argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for data in (a981(), g982(), g985()):
        path = out / f"construction-{data['name']}.json"
        path.write_text(json.dumps(data, indent=0) + "\n", encoding="utf-8")
        print(f"{path.name}: n={data['n']}")
    (out.parent / "goebel-with-borders.json").write_text(
        json.dumps(borders(), indent=1) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
