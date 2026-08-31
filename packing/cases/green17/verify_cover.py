"""Exact certificate: sixteen points make `[0, 4426213/10^6]^2` unavoidable.

Every decision routes through the shared Section 3 certifier
(`cases.bentz13.verify_cover.certify`) over exact rationals: the 34-cell
partition of the container, the Lemma 4 strips with their wall-vertex ends and
the three right-wall Lemma 4 rectangles, the three left-wall Lemma 5
quadrilaterals with the rigorous threshold bound, and the eighteen Lemma 2
triangles. The conclusion -- every box contains one of the sixteen points, so at
most sixteen disjoint boxes fit, so seventeen unit squares cannot pack below
side `4426213/1000000` (nor can eighteen) -- moves the verified lower lane at
`n = 17, 18` above Nagamochi's closed form (about 4.1623). The side sits within
`6 * 10^-7` of the set's exact ceiling `753/250 + sqrt 2` (the top strips'
`a + 2b <= 2 sqrt 2` becoming equality), a hair below Green's reported but
sourceless `(40 sqrt 2 + 19)/17` (about 4.4452).

The independent companion is `cases/green17/interval_audit.py`: the same claim
proved by exhaustive integer interval branch-and-bound over the full pose
space, sharing the data and nothing else; it certifies this side and refutes
`4427/1000` with an exact escaping pose. `sqpack.falsify.search_escape`
saturates with negative margin at this side as the numerical third leg.

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
        "s(17) >= 4426213/1000000 and s(18) >= 4426213/1000000: "
        "sixteen unavoidable points in [0, 4426213/1000000]^2"
    )
    record["standing_comparison"] = {
        "nagamochi_closed_form_n17": "about 4.1623",
        "this_certificate": "4426213/1000000 = 4.426213 exactly",
        "set_ceiling_exact": "753/250 + sqrt 2, about 4.42621356 (typed follow-on)",
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
