"""Controls for the column-generation driver.

`devtools.run_fractional_colgen` exists because every generator run in the
record before it was made from a script that was not kept, and the covering
values register says so in as many words: for the `n = 12` rung at `99/25`,
"the record names no site set and retains no site, row or round count". A
driver only earns that if two things hold. Its `auto` site density has to be
BC-191's and not a second opinion, and the bytes it freezes have to be the
bytes a retained case package reads back -- otherwise a candidate it writes
cannot be decided by the gate or replayed by anything.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from cases.n12_fractional_certificate.replay import CERTIFICATE_PATH, snapshot
from devtools.run_fractional_colgen import (
    RunSettings,
    certificate_json,
    counts_for,
    round_table_from,
    run,
)
from sqpack.fractional.colgen import site_counts_for_side

SIDE = Fraction(399, 100)
SHRINK = Fraction(9977, 10000)


def test_auto_counts_are_bc191s_site_density_and_nothing_else() -> None:
    assert counts_for("auto", SIDE, SHRINK) == site_counts_for_side(SIDE, SHRINK)
    assert counts_for("23,31,39", SIDE, SHRINK) == (23, 31, 39)


def test_frozen_bytes_replay_as_the_certificate_they_came_from() -> None:
    """Re-emitting a retained certificate reproduces the object, key for key.

    The retained file is the contract: a candidate this driver freezes has to
    parse through the same `replay._from_record` and carry the same
    declarations, or the case package's own gate cannot read it.
    """

    certificate, declared, _ = snapshot(CERTIFICATE_PATH)
    emitted = json.loads(certificate_json(certificate, declared["least_cell_mass"]))
    retained = json.loads(CERTIFICATE_PATH.read_text())
    assert set(emitted) == set(retained)
    for key in (
        "n",
        "claim",
        "outer_side",
        "square_side",
        "angle_limit",
        "direction_steps",
        "total_mass",
        "least_cell_mass",
        "symmetry",
    ):
        assert emitted[key] == retained[key], key
    assert emitted["atoms"] == retained["atoms"]


def test_a_candidate_with_no_verdict_declares_no_least_cell_mass() -> None:
    """Freezing is not deciding: the field stays null until something sweeps."""

    certificate, _, _ = snapshot(CERTIFICATE_PATH)
    assert json.loads(certificate_json(certificate, None))["least_cell_mass"] is None


def test_the_run_reports_a_row_per_round_and_freezes_what_it_found(tmp_path: Path) -> None:
    """One small end-to-end pass: the table, the summary and the frozen bytes.

    ``n = 1`` in a container two shrunk squares wide is the cheapest setting the
    loop still does real work at -- one direction, a three-by-three seed -- and
    it is here for the driver's plumbing, not for its arithmetic.
    """

    settings = RunSettings(
        n=1,
        outer_side=Fraction(2),
        square_side=Fraction(1),
        grid_counts=(3,),
        inset=Fraction(1, 2),
        angle_limit=Fraction(1, 10),
        direction_steps=1,
        scale=1000,
        column_rounds=1,
        max_rounds=4,
        rows_per_direction=2,
    )
    freeze = tmp_path / "candidate.json"
    result = run(settings, log_path=tmp_path / "run.log", freeze=freeze, verify_serial=False)

    assert result["settings"] == settings.as_dict()
    rounds = result["rounds"]
    assert isinstance(rounds, list) and rounds
    assert round_table_from(result).count("\n") == len(rounds) + 1
    for entry in rounds:
        assert entry["seconds"] >= 0.0
        assert entry["sites"] >= 3
    if result["converged"]:
        # A converged loop leaves no placement short of mass one, and that is
        # the number the record reports beside the objective.
        least_covered = result["least_covered"]
        assert isinstance(least_covered, float)
        assert least_covered >= 1 - 1e-6
        assert freeze.exists()
        assert json.loads(freeze.read_text())["least_cell_mass"] is None
        assert result["total_mass"] is not None
