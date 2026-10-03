"""The n17 frame adapter: the H-266 cover's cells at the exclusion cap, with D4.

The frame is `U = L = 1169/250`, so `B = 1` and field coordinates are physical; the
cells are a capacity-one cover's closed polygons, already in the centre box
`[1/2, U - 1/2]^2`; seventeen squares; the D4 action about `(U/2, U/2)`. The cells are
passed in, not built here, because the design lives in
`devtools/check_n17_capacity_one_cover.py` and `sqpack` does not import the tools; the
caller binds the design and its capacity receipt. Only construction and validation are
in scope: no n17 exclusion is run from this module.
"""

from __future__ import annotations

from collections.abc import Sequence

from sqpack.hull_kernel.frame import D4_ACTIONS, Frame, make_frame
from sqpack.hull_kernel.rational import Q, Rational

N17_CAP = Q(1169, 250)
N17_OCCUPANCY = 17


def frame_from_cells(
    cells: Sequence[tuple[str, Sequence[tuple[Rational, Rational]]]],
    *,
    design: str,
    provenance: str = "",
) -> Frame:
    """The n17 frame on named physical cells; refuses unless D4 maps them onto themselves."""
    return make_frame(
        name=f"n17-{design}",
        cap=N17_CAP,
        length=N17_CAP,
        cells=[vertices for _, vertices in cells],
        cell_names=[name for name, _ in cells],
        occupancy=N17_OCCUPANCY,
        action_names=D4_ACTIONS,
        provenance=provenance,
    )
