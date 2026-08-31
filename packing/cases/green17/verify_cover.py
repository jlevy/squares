"""Exact certificate: sixteen points make `[0, 17/4]^2` unavoidable — `s(17) >= 17/4`.

Every decision routes through the shared Section 3 certifier
(`cases.bentz13.verify_cover.certify`) over exact rationals: the 36-cell partition
of the container, the Lemma 4 strips with their wall-vertex ends, the three
left-wall Lemma 5 quadrilaterals with the rigorous threshold bound, the margin
band and near-slabs, and the eighteen Lemma 2 triangles. The conclusion — every
box contains one of the sixteen points, so at most sixteen disjoint boxes fit,
so seventeen unit squares cannot pack below side 17/4 (nor can eighteen) — moves
the verified lower lane at `n = 17, 18` above Nagamochi's closed form (about
4.1623) for the first time since 2005. Green's unadoptable 4.4452 remains the
stretch target; the near-slab corner bound `(t - 4)^2 + (433/1000)^2 <= 1/4` is
what pins this construction to exactly `t = 17/4`.

Held unresolved with needs_review per the run's unattended rules; adoption into
the frontier record is a reviewed evidence-contract change.

Usage, from `packing/`:
    uv run --frozen python -m cases.green17.verify_cover
"""

from __future__ import annotations

import time

from cases.bentz13.verify_cover import certify
from cases.green17.packing import EXPECTED_POINTS, SIDE, build


def build_certificate() -> dict[str, object]:
    set_points, vertices, plan, boundary = build()
    record = certify(
        set_points=set_points,
        vertices=vertices,
        plan=plan,
        expected_faces=len(plan),
        boundary=boundary,
        container_side=SIDE,
    )
    record["theorem"] = (
        "s(17) >= 17/4 and s(18) >= 17/4: sixteen unavoidable points in [0, 17/4]^2"
    )
    record["standing_comparison"] = {
        "nagamochi_closed_form_n17": "about 4.1623",
        "this_certificate": "17/4 = 4.25 exactly",
        "green_unpublished_n17": "(40 sqrt 2 + 19)/17, about 4.4452 (no primary source)",
    }
    return record


def main() -> int:
    started = time.monotonic()
    certificate = build_certificate()
    elapsed = time.monotonic() - started
    print(f"partition: {certificate['partition']['face_count']} faces certified")  # type: ignore[index]
    print(f"cells: {certificate['cells']}")
    print(f"points charged: {certificate['set_point_count']} of {EXPECTED_POINTS}")
    print(certificate["theorem"])
    print(f"wall: {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
