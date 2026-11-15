"""Lane L174 reader: the one component both deciding methods share.

A construction file is JSON written by ``l174_construct.py``.  Every number in it is an
element ``a + b*sqrt(2)`` of Q(sqrt 2), written as a two-item list of canonical fraction
strings ``["p/q", "p/q"]`` (or integers).  A square is a centre ``(cx, cy)``, an angle in
degrees (0 or 45, counterclockwise, ``y`` up) and a side ``size`` (a plain rational).
The container is the closed square ``[0, W]^2`` with ``W`` the file's ``container``.

The reader refuses anything else: an unknown angle, a non-canonical fraction, a count
that differs from the list, a duplicated id or label.  It decides nothing geometric.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

Q2 = tuple[Fraction, Fraction]


@dataclass(frozen=True)
class Square:
    sid: int
    label: str
    family: str
    cx: Q2
    cy: Q2
    angle: int
    size: Fraction


@dataclass(frozen=True)
class Construction:
    name: str
    container: Q2
    squares: tuple[Square, ...]


def _frac(text: object) -> Fraction:
    if isinstance(text, int) and not isinstance(text, bool):
        return Fraction(text)
    if not isinstance(text, str):
        msg = f"not a fraction string: {text!r}"
        raise TypeError(msg)
    value = Fraction(text)
    canonical = str(value)
    if canonical != text.strip():
        msg = f"non-canonical fraction {text!r} (canonical {canonical!r})"
        raise ValueError(msg)
    return value


def _q2(item: object) -> Q2:
    if not isinstance(item, list) or len(item) != 2:  # pyright: ignore[reportUnknownArgumentType]
        msg = f"not an [a, b] pair: {item!r}"
        raise ValueError(msg)
    return (_frac(item[0]), _frac(item[1]))  # pyright: ignore[reportUnknownArgumentType]


def read(path: Path) -> Construction:
    data = json.loads(path.read_text(encoding="utf-8"))
    squares: list[Square] = []
    seen_ids: set[int] = set()
    seen_labels: set[str] = set()
    for row in data["squares"]:
        angle = int(row["angle"])
        if angle not in {0, 45}:
            msg = f"angle {angle} is neither 0 nor 45"
            raise ValueError(msg)
        sid = int(row["id"])
        label = str(row["label"])
        if sid in seen_ids or label in seen_labels:
            msg = f"duplicate id or label {sid} {label}"
            raise ValueError(msg)
        seen_ids.add(sid)
        seen_labels.add(label)
        size = _frac(row["size"])
        if size <= 0:
            msg = f"non-positive size {size}"
            raise ValueError(msg)
        squares.append(
            Square(
                sid=sid,
                label=label,
                family=str(row["family"]),
                cx=_q2(row["cx"]),
                cy=_q2(row["cy"]),
                angle=angle,
                size=size,
            )
        )
    if int(data["n"]) != len(squares):
        msg = f"header n={data['n']} but {len(squares)} squares"
        raise ValueError(msg)
    if [s.sid for s in squares] != list(range(len(squares))):
        msg = "ids are not 0..n-1 in order"
        raise ValueError(msg)
    return Construction(name=str(data["name"]), container=_q2(data["container"]), squares=tuple(squares))
