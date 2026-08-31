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

ROOT = Path(__file__).resolve().parent.parent


def _record() -> dict:
    return json.loads(RECORD.read_text(encoding="utf-8"))


def test_no_component_the_grammar_misses_is_tilted() -> None:
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

    assert tilted_and_unexpressed == []
    angles = {
        str(component["angle_degrees"])
        for entry in band()
        for component in entry["components"]
        if component["shape"] == "other-polyomino"
    }
    assert angles == {"0"}


def test_the_residue_is_two_populations_and_nothing_between() -> None:
    """A grid record that is one polyomino, and a corner block inside a real packing.

    The wall seating separates them completely: 4 for a subset of an integer grid, which
    spans the container, and 2 for a block seated in a corner of a packing that is
    otherwise tilted. No residue component touches one wall or three.
    """
    residue = _record()["residue"]

    assert residue["walls_touched"] == {"2": 65, "4": 44}
    assert residue["by_source"] == {"exact-grid": 44, "kingbird-derived-facts": 65}
    assert residue["tilted"] == 0
    assert residue["whole_record"] == 44

    for item in residue["detail"]:
        if item["source"] == "exact-grid":
            assert item["is_the_whole_record"], item
            assert item["walls_touched"] == 4, item
        else:
            assert item["walls_touched"] == 2, item


def test_the_strata_are_not_three_samples_of_one_population() -> None:
    """Why stratifying was the thing worth doing.

    Two thirds of the corpus is a row-major grid subset with no tilt anywhere in it, and
    every tilted component in the repository lives in the other third plus the two excluded
    renderings.
    """
    strata = _record()["strata"]

    assert strata["exact-grid"]["records"] == 64
    assert strata["exact-grid"]["tilted_components"] == 0
    assert strata["exact-grid"]["components"] == 64  # one connected component per record
    assert strata["kingbird-derived-facts"]["tilted_components"] > 0
    assert strata["unitsquare-rendering"]["shapes"] == {"singleton": 137}


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
