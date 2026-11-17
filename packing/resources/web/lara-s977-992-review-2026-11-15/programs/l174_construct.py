"""Lane L174 clean-room construction of #992's packing, and of the controls' variants.

Built from the construction argument of ``certificates/n977_certificate.md`` alone:

* side ``L = 17 + 21/sqrt(2)``, centre ``C = L/2``;
* a k x k array (k = 21) of unit squares turned 45 degrees counterclockwise, square (i, j)
  with ``u = i - (k-1)/2``, ``v = j - (k-1)/2`` centred at
  ``(C + (u - v)/sqrt 2, C + (u + v)/sqrt 2)``;
* the bottom-left staircase of axis-parallel unit cells with lower-left corner (c, r),
  ``0 <= r < 15``, ``0 <= c < w_r``, widths 15 15 14 13 ... 2;
* the other three staircases as its images under rotation by 90, 180 and 270 degrees
  counterclockwise about (C, C): ``(x, y) -> (L - y, x)``, ``(L - x, L - y)``,
  ``(y, L - x)``.

Every coordinate is exact in Q(sqrt 2), held as a pair of Fractions (a, b) = a + b sqrt 2.
The variants (controls) change one parameter each; see ``SPECS``.

Usage: ``python -I -B l174_construct.py OUTDIR`` writes ``construction-<name>.json``.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

Q2 = tuple[Fraction, Fraction]
F = Fraction

WIDTHS: tuple[int, ...] = (15, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2)
SIDE: Q2 = (F(17), F(21, 2))  # 17 + 21/sqrt 2 = 17 + (21/2) sqrt 2
DELTA = F(1, 10**6)


def q_add(p: Q2, q: Q2) -> Q2:
    return (p[0] + q[0], p[1] + q[1])


def q_sub(p: Q2, q: Q2) -> Q2:
    return (p[0] - q[0], p[1] - q[1])


def q_half(p: Q2) -> Q2:
    return (p[0] / 2, p[1] / 2)


def rat(x: Fraction | int) -> Q2:
    return (F(x), F(0))


@dataclass(frozen=True)
class Spec:
    name: str
    note: str
    side: Q2 = SIDE
    container: Q2 | None = None
    diamond_k: int = 21
    diamond_scale: Fraction = F(1)
    widths: tuple[int, ...] = WIDTHS
    moves: tuple[tuple[str, Q2, Q2], ...] = field(default=())


def build(spec: Spec) -> dict[str, object]:
    side = spec.side
    centre = q_half(side)
    rows: list[dict[str, object]] = []

    def emit(label: str, family: str, cx: Q2, cy: Q2, angle: int, size: Fraction) -> None:
        rows.append(
            {
                "id": len(rows),
                "label": label,
                "family": family,
                "cx": cx,
                "cy": cy,
                "angle": angle,
                "size": size,
            }
        )

    k = spec.diamond_k
    half = F(k - 1, 2)
    s = spec.diamond_scale
    for i in range(k):
        for j in range(k):
            u = F(i) - half
            v = F(j) - half
            # (u - v)/sqrt 2 = ((u - v)/2) sqrt 2, scaled about the centre by s.
            cx = q_add(centre, (F(0), (u - v) * s / 2))
            cy = q_add(centre, (F(0), (u + v) * s / 2))
            emit(f"D({i},{j})", "diamond", cx, cy, 45, s)

    cells = [(c, r) for r, w in enumerate(spec.widths) for c in range(w)]
    half_unit = F(1, 2)
    images = {
        "BL": lambda x, y: (x, y),
        "BR": lambda x, y: (q_sub(side, y), x),
        "TR": lambda x, y: (q_sub(side, x), q_sub(side, y)),
        "TL": lambda x, y: (y, q_sub(side, x)),
    }
    for corner, image in images.items():
        for c, r in cells:
            x0 = rat(F(c) + half_unit)
            y0 = rat(F(r) + half_unit)
            cx, cy = image(x0, y0)
            emit(f"{corner}({c},{r})", f"stair-{corner}", cx, cy, 0, F(1))

    by_label = {row["label"]: row for row in rows}
    for label, dx, dy in spec.moves:
        row = by_label[label]
        row["cx"] = q_add(row["cx"], dx)  # pyright: ignore[reportArgumentType]
        row["cy"] = q_add(row["cy"], dy)  # pyright: ignore[reportArgumentType]

    def enc(p: Q2) -> list[str]:
        return [str(p[0]), str(p[1])]

    container = spec.container if spec.container is not None else side
    return {
        "name": spec.name,
        "note": spec.note,
        "construction_side": enc(side),
        "container": enc(container),
        "n": len(rows),
        "squares": [
            {
                "id": row["id"],
                "label": row["label"],
                "family": row["family"],
                "cx": enc(row["cx"]),  # pyright: ignore[reportArgumentType]
                "cy": enc(row["cy"]),  # pyright: ignore[reportArgumentType]
                "angle": row["angle"],
                "size": str(row["size"]),
            }
            for row in rows
        ],
    }


ZERO: Q2 = (F(0), F(0))

SPECS: tuple[Spec, ...] = (
    Spec("K0", "the construction as the certificate states it, side 17 + 21/sqrt 2"),
    Spec(
        "C1",
        "K0's squares unchanged in the container of side L - 10^-6",
        container=q_sub(SIDE, rat(DELTA)),
    ),
    Spec(
        "C2",
        "the construction rebuilt at side L - 10^-6 (centre and corners moved with it)",
        side=q_sub(SIDE, rat(DELTA)),
    ),
    Spec(
        "C3",
        "K0 with bottom-left cell BL(14,1) moved by (+10^-6, 0)",
        moves=(("BL(14,1)", rat(DELTA), ZERO),),
    ),
    Spec(
        "C4",
        "K0 with the central diamond square D(10,10) moved by (+10^-6, 0)",
        moves=(("D(10,10)", rat(DELTA), ZERO),),
    ),
    Spec("C5", "the diamond enlarged to a 22 x 22 array at the same side", diamond_k=22),
    Spec(
        "C6",
        "the diamond enlarged by the factor 1 + 10^-6 about the centre (squares and spacing)",
        diamond_scale=1 + DELTA,
    ),
    Spec(
        "C7",
        "the construction rebuilt at the CSV's relaxed side 31.85 = 637/20",
        side=rat(F(637, 20)),
    ),
)


def main(argv: list[str]) -> int:
    out = Path(argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for spec in SPECS:
        data = build(spec)
        path = out / f"construction-{spec.name}.json"
        path.write_text(json.dumps(data, indent=0, sort_keys=False) + "\n", encoding="utf-8")
        print(f"{path.name}: n={data['n']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
