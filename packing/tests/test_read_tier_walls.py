"""Reading a tier's cost out of a hosted job log, on a recorded excerpt of one.

A record in `gate-budgets.yaml` is a hosted reading, and for nine days the only way to
take one was to open a log and copy a number. Nobody did: `checks` and `sweeps` ran on
every pull request with `measured_seconds: null` from 2026-09-07 to 2026-09-15 while the
gate printed the line to write on every run. `devtools.read_tier_walls` is that reading as
a tool, and this is its parser held to the log it parses -- the `validate` job of run
34997018168, trimmed to the four things a reading is made of: the command, which names the
tier through the CLI's own parser; the step table; the verdict; and the step count that
says which tier the reading is of.
"""

from __future__ import annotations

import math
from pathlib import Path

import pytest

from devtools.read_tier_walls import geometric_mean, growth, parse_log, step_means

EXCERPT = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "tier-walls"
    / "validate-34997018168-excerpt.log"
)


def excerpt() -> str:
    return EXCERPT.read_text(encoding="utf-8")


def test_the_tier_and_its_wall_are_read_from_the_log() -> None:
    """The tier comes from the command, not from the job's name.

    A job name is a label someone chose; the command is what ran. `validate` runs
    `--checks`, and the two have never been the same word.
    """
    (reading,) = parse_log(excerpt())
    assert reading.tier == "checks"
    assert reading.wall_seconds == 135.71
    assert reading.enforced
    assert reading.steps == "49 of 74"


def test_a_reading_off_the_reference_shape_is_not_counted() -> None:
    """The gate itself says when it did not enforce a band, and a mean must respect that.

    Wall time is not comparable across shapes, so a reading the gate reported rather than
    enforced is listed for the reader and left out of the record.
    """
    reported = excerpt().replace(
        "note: no cost is recorded",
        "note: within the declared band, but this run's shape (2 cpus, 2 jobs, 1 inner) is "
        "not the checks tier's reference (4 cpus, --jobs 3 --inner-jobs 1), so the band was "
        "reported and not enforced\n2026-09-15T16:48:26.9922197Z   note: no cost is recorded",
    )
    (reading,) = parse_log(reported)
    assert not reading.enforced


def test_a_scoped_command_is_not_a_tier_reading() -> None:
    """`--only` selects a slice, and a slice has no declared cost (`D-466`)."""
    scoped = excerpt().replace(
        "packing-validate --checks --jobs 3", 'packing-validate --only "lint floor" --jobs 3'
    )
    assert parse_log(scoped) == []


def test_the_step_table_is_read_for_attribution() -> None:
    """A raised record must name what grew, and this is where those numbers come from."""
    (reading,) = parse_log(excerpt())
    assert reading.step_seconds["exact verification"] == 116.00
    assert reading.step_seconds["type floor (basedpyright)"] == 79.22
    assert "TOTAL (wall)" not in reading.step_seconds
    assert len(reading.step_seconds) == 8


def test_growth_pairs_two_groups_of_readings_by_step() -> None:
    """A step outside a run's eight slowest reads as zero there, which bounds it.

    The log prints the eight slowest steps, so a step that was cheap before and dear now
    shows its whole cost as growth, and one that was dear before and cheap now shows its
    whole cost as a fall. That is the right direction to be wrong in for a rule that asks
    what grew, and the tool says so where it prints the table.
    """
    (before,) = parse_log(excerpt())
    (after,) = parse_log(
        excerpt().replace("116.00s  exact verification", "150.00s  exact verification")
    )
    rows = growth([before], [after])
    name, was, now = rows[0]
    assert name == "exact verification"
    assert (was, now) == pytest.approx((116.00, 150.00))
    assert all(earlier == pytest.approx(later) for _, earlier, later in rows[1:])


def test_a_mean_over_readings_is_geometric_and_per_step() -> None:
    """The register's convention: the centre of the band, not one reading and not a max."""
    (one,) = parse_log(excerpt())
    (two,) = parse_log(excerpt().replace("135.71s", "271.42s"))
    assert two.wall_seconds == 271.42
    assert math.isclose(
        geometric_mean([one.wall_seconds, two.wall_seconds]), math.sqrt(135.71 * 271.42)
    )
    means = step_means([one, two])
    assert means["exact verification"] == pytest.approx(116.00)
