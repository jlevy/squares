"""The corpus's non-expressible residue is axis-aligned, which is the opposite of the guess.

`BC-024` asked which chunk shapes, sizes, tilted counts and wall seatings recur across the
imported `n <= 100` corpus, and what the residue has in common. The answer that would not
have been guessed: **not one** component the grammar fails to express is tilted. Every
tilted component in the corpus is a singleton, a bar, an L or a rectangle -- all of them
expressible. Extending the grammar to cover the residue is therefore a question about
axis-aligned polyominoes, and the tilted structure is already covered.

These assertions exist because that is a load-bearing claim for the partition-instrument
design, and because it is exactly the kind of clean result that should be pinned before it
is relied on.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from devtools.census_chunk_taxonomy import (
    RECORD,
    band,
    is_tilted,
    manifest,
    serialized,
    taxonomy,
    wall_seating,
)
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent


def _record() -> dict:
    return json.loads(RECORD.read_text(encoding="utf-8"))


def test_only_the_new_radical_strip_has_tilted_unexpressed_components() -> None:
    """The finding, stated as sharply as the data allows.

    Checked from the census directly rather than from the taxonomy record, so this fails if
    the underlying corpus changes even when the generated view has not been regenerated.
    """
    tilted_and_unexpressed = [
        (entry["n"], component["angle_degrees"])
        for entry in band()
        for component in entry["components"]
        if component["shape"] == "other-polyomino"
        and is_tilted(str(component["angle_degrees"]))
    ]

    assert tilted_and_unexpressed == [(51, "45"), (51, "45")]
    angles = {
        str(component["angle_degrees"])
        for entry in band()
        if entry["n"] not in (51, 88)
        for component in entry["components"]
        if component["shape"] == "other-polyomino"
    }
    # Axis-aligned to within 1e-9 degrees. The one residual is n = 68's corner block, in
    # Francisco Couzo's numerically optimized pose since 2026-09-29, at 3.2e-10 degrees.
    assert "0" in angles
    assert all(abs(float(angle)) < 1e-9 for angle in angles), angles
    # n = 88's fitted angle class prints 89.999999999 degrees because the class also
    # includes approximate neighbours. Both residue components themselves consist of
    # exactly axis-aligned rational edges; inspect every member, without widening the
    # original residual limit to accommodate the rounded class representative.
    witness = safe_load((ROOT / "witnesses/known-best/n-088.yaml").read_text())
    squares = {str(square["id"]): square for square in witness["witness"]["squares"]}
    residue = [
        component
        for entry in band()
        if entry["n"] == 88
        for component in entry["components"]
        if component["shape"] == "other-polyomino"
    ]
    assert sorted(component["size"] for component in residue) == [16, 25]
    for component in residue:
        assert component["angle_degrees"] == "89.999999999"
        for member in component["members"]:
            corners = squares[member]["corners"]
            dx = Fraction(str(corners[1][0])) - Fraction(str(corners[0][0]))
            dy = Fraction(str(corners[1][1])) - Fraction(str(corners[0][1]))
            assert (dx == 0) != (dy == 0), member


def test_the_residue_is_two_populations_and_nothing_between() -> None:
    """A grid record that is one polyomino, and a corner block inside a real packing.

    The wall seating separates them: 4 for a subset of an integer grid, which spans the
    container, and 2 for a block seated in a corner of a packing that is otherwise
    tilted. Among the catalogue's packings no residue component touches one wall or
    three. The new radical n51 strip adds two tilted interior components. The one-wall
    exception is n = 68, whose record moved on 2026-09-29 from its
    UnitSquare rendering, where every square is a singleton, to Francisco Couzo's packing:
    its five-square block seats against one wall. n = 69 made the same move on 2026-10-05,
    to the catalogue's packing (T-088), and its two blocks, of 21 and 28 squares, are corner
    blocks like the catalogue's others.
    """
    residue = _record()["residue"]

    assert residue["walls_touched"] == {"0": 2, "1": 1, "2": 68, "4": 44}
    assert residue["by_source"] == {
        "exact-grid": 44,
        "kingbird-derived-facts": 57,
        "packet-derived-facts": 14,
    }
    assert residue["tilted"] == 2
    assert residue["whole_record"] == 44

    for item in residue["detail"]:
        if item["source"] == "exact-grid":
            assert item["is_the_whole_record"], item
            assert item["walls_touched"] == 4, item
        elif item["source"] == "packet-derived-facts":
            assert (item["n"], item["size"], item["walls_touched"]) in {
                (51, 5, 0),
                (51, 10, 2),
                (51, 18, 2),
                (68, 5, 1),
                (70, 18, 2),
                (70, 30, 2),
                (84, 6, 2),
                (84, 15, 2),
                (84, 25, 2),
                (86, 22, 2),
                (86, 36, 2),
                (88, 16, 2),
                (88, 25, 2),
            }, item
        else:
            assert item["walls_touched"] == 2, item


def test_the_strata_are_not_three_samples_of_one_population() -> None:
    """Why stratifying was the thing worth doing.

    Two thirds of the corpus is a row-major grid subset with no tilt anywhere in it, and
    every tilted component in the repository lives in the other third. The UnitSquare
    renderings that were a stratum of their own have all left it, n = 68 for Couzo's packet
    on 2026-09-29 and n = 69 for the catalogue on 2026-10-05 (T-088).
    """
    strata = _record()["strata"]

    assert strata["exact-grid"]["records"] == 64
    assert strata["exact-grid"]["tilted_components"] == 0
    assert strata["exact-grid"]["components"] == 64  # one connected component per record
    assert strata["kingbird-derived-facts"]["tilted_components"] > 0
    assert "unitsquare-rendering" not in strata
    assert strata["kingbird-derived-facts"]["records"] == 30
    assert strata["packet-derived-facts"]["records"] == 6
    assert strata["packet-derived-facts"]["tilted_components"] > 0


def test_wall_seating_agrees_with_the_n5_geometry_we_know_exactly() -> None:
    """An independent check on the one packing whose contacts are established exactly.

    `X-007` enumerates n = 5's contacts in `Q(sqrt 2)`: sixteen corner-on-wall contacts
    across the four corner squares, two walls each, and a middle square touching no wall at
    all. If the seating computed here from decimal witness corners disagreed with that, the
    seating would be measuring the witness's precision rather than the packing.
    """
    seated = wall_seating(manifest()[5])
    counts = sorted(len(walls) for walls in seated.values())

    assert counts == [0, 2, 2, 2, 2]
    assert sum(1 for walls in seated.values() if not walls) == 1


def test_the_record_round_trips_through_json() -> None:
    """`--check` compares text, because JSON has no integer keys.

    Written with integer keys, this record would differ from itself the moment it was read
    back, and its own drift check would fail on freshly generated output.
    """
    built = taxonomy()

    assert RECORD.read_text(encoding="utf-8") == serialized(built)
    assert json.loads(serialized(built)) == json.loads(RECORD.read_text(encoding="utf-8"))


def test_the_taxonomy_emits_no_verdict() -> None:
    """Descriptive is a commitment, not a disclaimer.

    `BC-024`'s exit is explicit that no `H-044` verdict is emitted, and the census's own
    `known_gap` says an unexpressed component is not a refutation until the minimal
    partition solver exists. The record has to carry that, because a table of counts reads
    like a conclusion.
    """
    subject = _record()["subject"]

    assert "H-044 is untouched" in subject["emits_no_verdict"]
    assert "not a refutation" in subject["emits_no_verdict"]
