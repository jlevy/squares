"""The shared angle classes the angle-stable colour contract holds exact, without a browser.

`animate_view_contract.colours` once admitted one split: two frames' classes within the
colourer's tolerance either side of a five-degree band edge, as n = 29's 64.9387 and T-151's
65.2889 at n = 272 were (#553 C1). The colourer now takes each frame's classes from centres the
whole atlas shares, drawn by `build_candidate.atlas_angle_centres`, and the contract requires
every shared angle in one slot (#554). These are the properties of those centres that make an
exact check possible.
"""

from __future__ import annotations

import itertools

from workbench_tools.animate_view_contract import angle_gap
from workbench_tools.build_candidate import atlas_angle_centres

TOLERANCE = 0.5


def witness(*angles: float) -> dict:
    return {"squares": [(0.0, 0.0, angle) for angle in angles]}


def test_the_most_frequent_tilt_leads_its_class_and_the_pins_are_left_out() -> None:
    witnesses = {
        29: witness(64.7413, 65.0374, 0.2, 44.7),
        272: witness(64.5234, 65.1017, 65.3157, 65.396, 89.9, 45.3),
        100: witness(65.3157, 65.3157, 10.0),
    }
    centres = atlas_angle_centres(witnesses, TOLERANCE)
    # 65.3157 is drawn three times, so it leads, and 65.0374 to 65.396 join it. The rest are
    # drawn once each and go by angle: 10.0 leads, then 64.5234, 0.79 from 65.3157, which
    # 64.7413 joins. The pins are never centres.
    assert centres == [10.0, 64.5234, 65.3157]


def test_every_atlas_tilt_meets_a_centre_and_no_two_centres_meet() -> None:
    angles = [round(20 + 0.137 * k, 4) for k in range(120)] + [-24.7111, 154.9387, 359.6]
    centres = atlas_angle_centres({1: witness(*angles)}, TOLERANCE)
    assert centres == sorted(centres)
    assert all(0 <= centre < 90 for centre in centres)
    assert all(angle_gap(a, b) > TOLERANCE for a, b in itertools.combinations(centres, 2))
    for angle in angles:
        if angle_gap(angle, 0) > TOLERANCE and angle_gap(angle, 45) > TOLERANCE:
            assert min(angle_gap(angle, centre) for centre in centres) <= TOLERANCE, angle
    # A quarter turn on, a tilt is the same tilt: -24.7111 and 154.9387 fold to 65.2889 and
    # 64.9387, and 359.6 to 89.6, a pin.
    assert all(angle_gap(centre, 0) > TOLERANCE for centre in centres)
