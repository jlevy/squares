"""Lane L163: decide a certificate by both methods, every square, wall and pair.

There is no distance filter: every one of the n(n-1)/2 pairs is decided by method A
(`l163_sat`) and by method B (`l163_clip`), and every square against every wall by both.
The two methods share only the reader's integers. The verdict is ACCEPT only when both
accept every square, wall and pair and their classes agree everywhere.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from fractions import Fraction

import l163_clip as clip
import l163_sat as sat
from gmpy2 import mpq
from l163_reader import Certificate

WALLS = ("left", "bottom", "right", "top")


@dataclass
class Decision:
    n: int
    side: Fraction
    unit_a: list[bool] = field(default_factory=list)  # pyright: ignore[reportUnknownVariableType]
    unit_b: list[bool] = field(default_factory=list)  # pyright: ignore[reportUnknownVariableType]
    ccw_b: list[bool] = field(default_factory=list)  # pyright: ignore[reportUnknownVariableType]
    margins: dict[tuple[int, int], Fraction] = field(default_factory=dict)  # pyright: ignore[reportUnknownVariableType]
    binding: dict[tuple[int, int], int] = field(default_factory=dict)  # pyright: ignore[reportUnknownVariableType]
    class_a: dict[tuple[int, int], str] = field(default_factory=dict)  # pyright: ignore[reportUnknownVariableType]
    class_b: dict[tuple[int, int], str] = field(default_factory=dict)  # pyright: ignore[reportUnknownVariableType]
    area_b: dict[tuple[int, int], mpq] = field(default_factory=dict)  # pyright: ignore[reportUnknownVariableType]
    clear: list[tuple[Fraction, Fraction, Fraction, Fraction]] = field(default_factory=list)  # pyright: ignore[reportUnknownVariableType]
    wall_a: list[list[str]] = field(default_factory=list)  # pyright: ignore[reportUnknownVariableType]
    wall_b: list[list[str]] = field(default_factory=list)  # pyright: ignore[reportUnknownVariableType]
    inside_area_b: list[mpq] = field(default_factory=list)  # pyright: ignore[reportUnknownVariableType]

    def pair_classes_agree(self) -> bool:
        return self.class_a == self.class_b

    def wall_classes_agree(self) -> bool:
        return self.wall_a == self.wall_b

    def containment_agrees(self) -> bool:
        a_in = [all(c >= 0 for c in cl) for cl in self.clear]
        b_in = [ar == 1 for ar in self.inside_area_b]
        return a_in == b_in

    def accepted(self) -> bool:
        return (
            all(self.unit_a)
            and all(self.unit_b)
            and all(self.ccw_b)
            and self.pair_classes_agree()
            and self.wall_classes_agree()
            and self.containment_agrees()
            and all(c != "overlap" for c in self.class_a.values())
            and all(w != "crossing" for ws in self.wall_a for w in ws)
            and all(ar == 1 for ar in self.inside_area_b)
        )

    def overlapping(self) -> list[tuple[int, int]]:
        return sorted(k for k, c in self.class_a.items() if c == "overlap")

    def touching(self) -> list[tuple[int, int]]:
        return sorted(k for k, c in self.class_a.items() if c == "touch")

    def contacts(self) -> list[tuple[int, str]]:
        return [(i + 1, WALLS[w]) for i, ws in enumerate(self.wall_a) for w in range(4) if ws[w] == "contact"]

    def crossings(self) -> list[tuple[int, str]]:
        return [(i + 1, WALLS[w]) for i, ws in enumerate(self.wall_a) for w in range(4) if ws[w] == "crossing"]

    def margin_digest(self) -> str:
        h = hashlib.sha256()
        for (i, j), m in sorted(self.margins.items()):
            h.update(f"{i} {j} {m.numerator}/{m.denominator}\n".encode())
        return h.hexdigest()

    def clearance_multiset_digest(self) -> str:
        """Digest of the sorted list of all 4n clearances (blind to which wall)."""
        vals = sorted(c for cl in self.clear for c in cl)
        h = hashlib.sha256()
        for c in vals:
            h.update(f"{c.numerator}/{c.denominator}\n".encode())
        return h.hexdigest()


def decide(cert: Certificate) -> Decision:
    side = Fraction(*cert.side)
    d = Decision(cert.n, side)
    sq_a = [sat.prepare(r) for r in cert.squares]
    pts = [clip.corners(r) for r in cert.squares]
    side_q = mpq(*cert.side)
    for s in sq_a:
        d.unit_a.append(sat.is_unit(s))
        cl = sat.clearances(s, cert.side)
        d.clear.append(cl)
        d.wall_a.append([sat.wall_class(c) for c in cl])
    for p in pts:
        d.unit_b.append(clip.is_unit_square(p))
        d.ccw_b.append(clip.twice_signed_area(p) == 2)
        cls, inside = clip.wall_classes(p, side_q)
        d.wall_b.append(cls)
        d.inside_area_b.append(inside)
    n = cert.n
    for i in range(n):
        for j in range(i + 1, n):
            g, den = sat.margin_parts(sq_a[i], sq_a[j])
            top = max(g)
            m = Fraction(top, den)
            key = (i + 1, j + 1)
            d.margins[key] = m
            d.binding[key] = sum(1 for x in g if x == top)
            d.class_a[key] = sat.classify(m)
            cls, ar = clip.pair_class(pts[i], pts[j])
            d.class_b[key] = cls
            d.area_b[key] = ar
    return d
