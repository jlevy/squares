"""Lemma 10's three replacement-set certificates, against the corrected reading.

Lemma 10 (audited in `lemma10_audit`; the printed `(1, 1.74)` is transposed) needs:
for each replacement point `P` in `{(1.12, 1), (1.74, 1), (1.87, 0.76)}`, the set
`(Figure 2 minus A) union {P}` is unavoidable. Each certificate below reuses the
Figure 2 complex outside the bottom-left zone and retiles that zone around its
replacement point; every cell premise is decided exactly by `verify_cover.certify`.

Two structural facts carry the retilings, and both corroborate the corrected
reading against the paper's own Section 1: the two Lemma 5 quadrilaterals needed
here sit at `a = 0.88, b = 0.914` and `a = 0.956, b = 0.76` -- inside exactly the
two parameter families Bentz lists for Lemma 5 use (`a <= 0.89, 0.6 < b <= 0.921`
and `a = 0.96, b = 0.76`). The margin and near cells discharge the strip the
lemmas do not reach: no box centre lies within `1/2` of a wall, and a box contains
any point within `1/2` of its whole cell.

Usage, from `packing/`:
    uv run --frozen python -m cases.bentz13.lemma10_replacements
"""

from __future__ import annotations

import time
from fractions import Fraction

from cases.bentz13.packing import BOUNDARY, NEAR, CellPlan, Face, Point, Rat, build
from cases.bentz13.verify_cover import certify

#: The corrected replacement points of Lemma 10.
REPLACEMENTS: dict[str, tuple[Fraction, Fraction]] = {
    "r1": (Fraction(28, 25), Fraction(1)),
    "r2": (Fraction(87, 50), Fraction(1)),
    "r3": (Fraction(187, 100), Fraction(19, 25)),
}


def _base_without_a1() -> tuple[dict[str, Point], dict[str, Point], dict[str, CellPlan]]:
    set_points, vertices, plan = build()
    del set_points["a1"]
    for name in ("rb1", "t_c1", "t_e1"):
        del plan[name]
    pent = plan["pent_bl"]
    plan["pent_bl"] = CellPlan(face=pent.face, kind=pent.kind, corner=pent.corner, outs=("b1",))
    return set_points, vertices, plan


def _split_rb2(vertices: dict[str, Point], plan: dict[str, CellPlan]) -> None:
    """Insert the collinear vertex (2, 1/2) into rb2's left edge for edge pairing."""
    vertices["v25"] = (Rat.of(2), Rat.of(Fraction(1, 2)))
    rb2 = plan["rb2"]
    face = rb2.face
    index = face.index("c3")
    new_face = (*face[: index + 1], "v25", *face[index + 1 :])
    plan["rb2"] = CellPlan(
        face=new_face, kind=rb2.kind, wall=rb2.wall, outs=rb2.outs, rect=rb2.rect
    )


def build_replacement(
    key: str,
) -> tuple[dict[str, Point], dict[str, Point], dict[str, CellPlan], int, Face]:
    """Return (set_points, vertices, plan, expected_faces, boundary)."""
    px, py = REPLACEMENTS[key]
    set_points, vertices, plan = _base_without_a1()
    point = (Rat.of(px), Rat.of(py))
    set_points["p"] = point
    vertices["p"] = point
    vertices["v1"] = (Rat.of(px), Rat.of(0))
    at = BOUNDARY.index("w20")
    boundary: Face = (*BOUNDARY[:at], "v1", *BOUNDARY[at:])

    if key == "r1":
        plan["g1"] = CellPlan(
            face=("w10", "v1", "p", "b1", "a1"),
            kind="lemma4",
            wall="bottom",
            outs=("b1", "p"),
            rect=(NEAR, px, Fraction(0), Fraction(1)),
        )
        plan["q1"] = CellPlan(
            face=("v1", "w20", "c3", "p"),
            kind="lemma5",
            wall="bottom",
            outs=("p", "c3"),
            quad=(px, Fraction(2) - px, NEAR),
        )
    else:
        _split_rb2(vertices, plan)
        vertices["v2"] = (Rat.of(px), Rat.of(Fraction(1, 2)))
        plan["m0"] = CellPlan(face=("v1", "w20", "v25", "v2"), kind="margin", wall="bottom")
        plan["n0"] = CellPlan(face=("v2", "v25", "c3", "p"), kind="near", outs=("c3",))
        if key == "r2":
            plan["g2"] = CellPlan(
                face=("w10", "v1", "v2", "p", "b1", "a1"),
                kind="lemma4",
                wall="bottom",
                outs=("b1", "p"),
                rect=(NEAR, px, Fraction(0), Fraction(1)),
            )
        else:  # r3
            plan["q3"] = CellPlan(
                face=("w10", "v1", "v2", "p", "b1", "a1"),
                kind="lemma5",
                wall="bottom",
                outs=("b1", "p"),
                quad=(NEAR, px - NEAR, py),
            )
    plan["t_r1"] = CellPlan(face=("b1", "p", "d1"), kind="lemma2", outs=("b1", "p", "d1"))
    plan["t_r2"] = CellPlan(face=("p", "c3", "d1"), kind="lemma2", outs=("p", "c3", "d1"))
    return set_points, vertices, plan, len(plan), boundary


def certify_replacement(key: str) -> dict[str, object]:
    set_points, vertices, plan, expected, boundary = build_replacement(key)
    record = certify(
        set_points=set_points,
        vertices=vertices,
        plan=plan,
        expected_faces=expected,
        boundary=boundary,
    )
    px, py = REPLACEMENTS[key]
    record["replacement_point"] = f"({px}, {py})"
    return record


def main() -> int:
    started = time.monotonic()
    for key in REPLACEMENTS:
        record = certify_replacement(key)
        thresholds = record["lemma5_thresholds"]
        bound = (
            thresholds[0]["decimal_for_display_only"]  # type: ignore[index]
            if thresholds
            else "none needed"
        )
        print(
            f"{key}: replacement {record['replacement_point']} certified -- "
            f"{record['cells']}, lemma 5 bound {bound}"
        )
    elapsed = time.monotonic() - started
    print("Lemma 10 holds with the corrected reading: all three replacement sets certify")
    print(f"wall: {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
