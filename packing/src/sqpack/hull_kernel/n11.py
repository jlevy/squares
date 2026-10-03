"""The n11 frame and packet adapters, read from n11's published cover and field packet.

The constants are n11's: the cap `U = 387708359002281417731/10^20`, the field side
`L = 191/50`, sixteen cells given in the normalised square `[0, 1]^2` and mapped to the
physical centre box by `1/2 + (U - 1) v`, eleven squares, and the half-turn
`j -> 15 - j`. The adapters only translate and check the inputs' shape; the source
objects' identities are pinned by the frozen checkers that load them, and are not
re-pinned here.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from sqpack.hull_kernel.counting import CountingPacket, MajorityFeature
from sqpack.hull_kernel.frame import HALF_TURN_ACTIONS, Frame, make_frame
from sqpack.hull_kernel.geometry import Point, area2, require
from sqpack.hull_kernel.rational import Q

N11_CAP = Q(387708359002281417731, 10**20)
N11_LENGTH = Q(191, 50)
N11_CELLS = 16
N11_OCCUPANCY = 11


def _point(value: Any) -> Point:
    require(isinstance(value, list) and len(value) == 2, "expected a two-coordinate point")
    return Q(value[0]), Q(value[1])


def frame_from_cover(cover: Mapping[str, Any], *, provenance: str = "") -> Frame:
    """The n11 frame; refuses unless the cover's involution and canonical masks agree."""
    raw = cover["cells"]
    require(isinstance(raw, list) and len(raw) == N11_CELLS, "cover cell count changed")
    cells: list[list[Point]] = []
    for number, cell in enumerate(raw):
        vertices = [_point(v) for v in cell["vertices"]]
        require(len(vertices) >= 3 and area2(vertices) > 0, f"cell {number}: degenerate cover")
        cells.append(
            [(Q(1, 2) + (N11_CAP - 1) * x, Q(1, 2) + (N11_CAP - 1) * y) for x, y in vertices]
        )
    frame = make_frame(
        name="n11-half-turn-16",
        cap=N11_CAP,
        length=N11_LENGTH,
        cells=cells,
        cell_names=tuple(str(number) for number in range(N11_CELLS)),
        occupancy=N11_OCCUPANCY,
        action_names=HALF_TURN_ACTIONS,
        provenance=provenance,
    )
    require(
        list(frame.actions[1].permutation) == cover["symmetry_cell_involution"],
        "the cover's involution is not the geometric half-turn",
    )
    require(
        [list(state) for state in frame.representatives]
        == cover["canonical_eleven_cell_subsets"],
        "the frame's orbit representatives differ from the cover's canonical masks",
    )
    return frame


def packet_from_field(frame: Frame, packet: Mapping[str, Any]) -> CountingPacket:
    """A counting packet from n11's field-packet JSON, in field coordinates."""
    cert = packet["certificate"]
    require(Q(packet["parent_Uplus"]) == frame.cap, "U premise changed")
    require(Q(cert["L"]) == frame.length, "field scale changed")
    denominator = cert["coordinate_denominator"]
    require(type(denominator) is int and denominator > 0, "invalid coordinate denominator")
    raw_sites = cert["sites"]
    require(
        isinstance(raw_sites, list)
        and all(
            isinstance(site, list)
            and len(site) == 2
            and all(type(value) is int for value in site)
            for site in raw_sites
        ),
        "field sites must be integer pairs",
    )
    sites = tuple((Q(x, denominator), Q(y, denominator)) for x, y in raw_sites)
    require(cert["point_weights"] == [0] * len(sites), "point weights are not lifted")
    features = cert["features"]
    require(
        isinstance(features, list)
        and len(features) == 1
        and features[0].get("kind") == "majority_hull",
        "exactly one majority feature is lifted",
    )
    feature = features[0]
    owners = tuple(packet["conditional_owner_support"])
    require(all(type(owner) is int for owner in owners), "owners must be cell indices")
    groups = packet["ownership_points_field"]
    require(isinstance(groups, list) and len(groups) == len(frame.cells), "owner inventory")
    return CountingPacket(
        owners=owners,
        owned_points={
            owner: tuple(_point(value) for value in groups[owner]) for owner in owners
        },
        sites=sites,
        feature=MajorityFeature(
            tuple(feature["indices"]), feature["threshold"], feature["weight"]
        ),
        thresholds=tuple(packet["threshold_units"]),
        budget=cert["budget_units"],
    )


def rows_from_audit(audit: Mapping[str, Any]) -> list[tuple[int, tuple[Q, Q]]]:
    """The proposed `(cell, interval)` rows of an n11 field audit, shape-checked."""
    raw = audit["independent_row_proofs"]
    require(isinstance(raw, list), "row proposals must be a list")
    rows: list[tuple[int, tuple[Q, Q]]] = []
    for row in raw:
        cell, interval = row["cell"], row["interval"]
        require(type(cell) is int, "row cell must be an index")
        require(isinstance(interval, list) and len(interval) == 2, "malformed row interval")
        rows.append((cell, (Q(interval[0]), Q(interval[1]))))
    return rows
