"""The n11 ownership kernel, parametrised by a frame so that it runs on n11 and n17.

The kernel's arithmetic is copied from the frozen native n11 checkers under
`packing/devtools/`, which stay byte-pinned by their receipts and are never edited. What
was a module constant there (the cap, the field side and scale, the cells, the symmetry
group, the state size) is a `Frame` here; everything else is the same exact rational
arithmetic in the same order. `docs/project/reviews/` holds the adaptation spec
(`review-2026-10-02-n17-kernel-adaptation-spec.md`).

Lifted so far, each module naming the frozen file it copies:

* `geometry`: clipping, areas, the half-angle chart, quadratic envelopes;
* `sweep`: the exact vertical-sweep union cover (the reference);
* `covers`: the fast and indexed forms of that sweep, and the closed point-or-segment
  cover;
* `ownership`: strict capture of a field point over a cell and every angle;
* `counting`: the counting mode (mask 0's packet): row envelope and strict core, the
  majority median strip, one row, the row partition, transfer and the packet replay;
* `induction`: mode A's row geometry: hull normal forms, wall lines, the vertex-quadratic
  strict core, Minkowski forbidden regions, common-core planes, convex combinations;
* `node`: mode A's node grammar: the wall seed, the header, one row, compression, the
  sequential replay, the final state and the terminal contradiction;
* `collision`: self-hull cuts, universal collision (rational and integer), the support
  outer domain and the common-core output check of a capture row;
* `frame`: frames, the centred legal box, symmetry actions, orbit representatives and
  the containment-plus-symmetry transfer;
* `n11` and `n17`: the two frame adapters.

Every wall clip goes through `Frame.centre_bounds`, which is n11's `[h, U - h]` exactly
when no capture cap is set. The method controls are `devtools/check_hull_kernel_mask0.py`
(the counting path) and `devtools/check_hull_kernel_case2095.py` (the induction path),
which replay n11's mask 0 and case 2095 through this package and refuse unless they match
the frozen checkers and their retained receipts exactly.
"""

from sqpack.hull_kernel.counting import (
    CountingPacket,
    MajorityFeature,
    counting_row,
    partition_rows,
    replay_counting_packet,
    row_envelope,
    transferred_states,
)
from sqpack.hull_kernel.frame import Frame, SymmetryAction, make_frame, orbit_representatives
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError
from sqpack.hull_kernel.ownership import ownership
from sqpack.hull_kernel.sweep import exact_union_cover

__all__ = [
    "Budget",
    "CountingPacket",
    "Frame",
    "IncompleteError",
    "MajorityFeature",
    "RefusalError",
    "SymmetryAction",
    "counting_row",
    "exact_union_cover",
    "make_frame",
    "orbit_representatives",
    "ownership",
    "partition_rows",
    "replay_counting_packet",
    "row_envelope",
    "transferred_states",
]
