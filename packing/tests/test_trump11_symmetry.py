"""No symmetry of the container maps Trump's eleven-square packing to itself.

T-112 counts the optimal packings of eleven squares as exactly eight unlabelled
configurations, the images of Trump's packing under the eight symmetries of the
container. That count needs the packing's stabiliser in that group to be trivial,
which this checks exactly in the packing's number field: each square is the set of its
four corners, and an element of the group fixes the packing only if it maps the set of
eleven squares onto itself (think-d1bd).
"""

from __future__ import annotations

from collections.abc import Callable

from cases.trump11.packing import build


def test_only_the_identity_maps_trumps_packing_onto_itself() -> None:
    squares, side, _ = build()

    def symmetries() -> dict[str, Callable]:
        return {
            "identity": lambda x, y: (x, y),
            "quarter turn": lambda x, y: (side - y, x),
            "half turn": lambda x, y: (side - x, side - y),
            "three-quarter turn": lambda x, y: (y, side - x),
            "vertical axis": lambda x, y: (side - x, y),
            "horizontal axis": lambda x, y: (x, side - y),
            "diagonal": lambda x, y: (y, x),
            "anti-diagonal": lambda x, y: (side - y, side - x),
        }

    packing = {frozenset((x, y) for x, y in square) for square in squares}
    assert len(packing) == 11
    fixed = {}
    for name, act in symmetries().items():
        image = {frozenset(act(x, y) for x, y in square) for square in packing}
        fixed[name] = len(image & packing)
    assert fixed.pop("identity") == 11
    assert all(count < 11 for count in fixed.values()), fixed
