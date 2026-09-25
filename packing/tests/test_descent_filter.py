"""The full-pose descent filter and the H-238 census mode built on it.

The filter's two promises are checked on packings whose status is known: Trump's is a
strict local minimum and must not be rejected; a Trump pose with one angle released and
its centres re-optimised is a fixed-angle optimum but not a local minimum, and must be
rejected with an exact rational witness. The census bookkeeping is checked on synthetic
records, since a real census is an hour of wall time.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from devtools.run_basin_hopping import (
    CENSUS_KILL_SIDE,
    census_carried,
    census_summary,
    main,
    trump_11_pose,
)
from sqpack.research.descent_filter import (
    STROMQUIST_11_SIDE,
    DescentFilterConfig,
    class_summary,
    descent_filter,
    exact_witness,
    min_pair_gap,
    rattling_squares,
    stromquist_11_pose,
)
from sqpack.research.quench import solve_to_fixed_point

# Fewer probes than the census uses: the tests check the verdicts, not the budget.
QUICK = DescentFilterConfig(cone_probes=2, random_probes=2, time_budget=120.0)


def test_stromquist_pose_is_the_family_value() -> None:
    x, y, theta = stromquist_11_pose()
    got = solve_to_fixed_point(theta, x, y, 11)
    assert got.settled
    assert abs(got.side - STROMQUIST_11_SIDE) < 1e-12
    assert min_pair_gap(x, y, theta) > -1e-12
    assert class_summary(theta)["multiplicities"] == [6, 5]


def test_exact_witness_of_trump_is_valid_and_tight() -> None:
    x, y, theta, u_side = trump_11_pose()
    witness = exact_witness(x, y, theta)
    assert witness.valid
    assert witness.side is not None
    assert 0.0 <= float(witness.side) - u_side < 1e-10


def test_exact_witness_refuses_an_overlap_it_may_not_repair() -> None:
    x, y, theta, _ = trump_11_pose()
    x = list(x)
    x[0] += 0.01  # square 0 pushed into its neighbour
    assert min_pair_gap(x, y, theta) < 0.0
    witness = exact_witness(x, y, theta, margin=1e-12, max_attempts=1)
    assert not witness.valid


def test_trump_is_descent_stable() -> None:
    x, y, theta, u_side = trump_11_pose()
    result = descent_filter(x, y, theta, reference_side=u_side, config=QUICK)
    assert result.status == "stable"
    assert not result.rejected
    assert abs(result.terminal_side - u_side) < 1e-10


def test_released_trump_is_rejected_with_a_witness() -> None:
    x, y, theta, u_side = trump_11_pose()
    turned = list(theta)
    turned[10] += 0.02
    start = solve_to_fixed_point(turned, x, y, 11)
    assert start.settled
    assert start.side > u_side + 1e-4
    result = descent_filter(start.x, start.y, turned, reference_side=start.side, config=QUICK)
    assert result.rejected
    assert result.certificate is not None
    assert result.certificate.valid
    assert result.certificate.side is not None
    assert float(result.certificate.side) < start.side - QUICK.certify_tol
    assert result.status == "stable"
    assert abs(result.terminal_side - u_side) < 1e-9


def test_rattlers_are_found_at_stromquist_and_absent_at_trump() -> None:
    x, y, theta, u_side = trump_11_pose()
    assert rattling_squares(x, y, theta, u_side) == []
    sx, sy, st = stromquist_11_pose()
    assert 7 in rattling_squares(sx, sy, st, STROMQUIST_11_SIDE)


def _record(side: float, sizes: list[int], *, rejected: bool, witness: float) -> dict[str, Any]:
    return {
        "base": "trump",
        "index": 0,
        "quench": {"converged": True, "side": side, "classes": {"classes": len(sizes)}},
        "filter": {
            "status": "stable",
            "rejected": rejected,
            "terminal_side": side,
            "terminal_witness": {"valid": True, "side": witness},
            "terminal_classes": {"classes": len(sizes), "multiplicities": sizes},
        },
    }


def test_census_verdict_follows_the_frozen_threshold() -> None:
    below = _record(3.88, [6, 4, 1], rejected=False, witness=3.88)
    minima = [
        {"classes": 3, "witness_side_min": 3.88, "multiplicities": [6, 4, 1]},
    ]
    assert census_summary([below], minima)["verdict"].startswith("KILL")
    # Stromquist's own value is above the threshold, so a three-class member of its
    # family (a rattler turned off 45 degrees) does not kill.
    at_family = [
        {"classes": 3, "witness_side_min": STROMQUIST_11_SIDE, "multiplicities": [5, 5, 1]},
    ]
    assert STROMQUIST_11_SIDE > CENSUS_KILL_SIDE
    assert census_summary([below], at_family)["verdict"].startswith("SUPPORT")
    two_class = [{"classes": 2, "witness_side_min": 3.877, "multiplicities": [6, 5]}]
    assert census_summary([below], two_class)["verdict"].startswith("SUPPORT")


def test_stock_parser_is_unchanged_and_census_is_a_subcommand() -> None:
    for argv, code in ((["--help"], 0), ([], 2), (["census", "--help"], 0)):
        try:
            main(argv)
        except SystemExit as exc:
            assert exc.code == code
        else:
            raise AssertionError(f"{argv} did not exit")
    assert math.isclose(STROMQUIST_11_SIDE, 2 + 4 * math.sqrt(2) / 3)


def test_resume_carries_matching_records_and_refuses_foreign_ones(tmp_path: Path) -> None:
    tasks = [
        {"base": "trump", "index": 0, "rng_seed": 11},
        {"base": "stromquist", "index": 0, "rng_seed": 12},
    ]
    good = tmp_path / "good.jsonl"
    good.write_text('{"base": "trump", "index": 0, "rng_seed": 11}\n')
    assert [r["index"] for r in census_carried(good, tasks)] == [0]
    assert census_carried(None, tasks) == []
    foreign = tmp_path / "foreign.jsonl"
    foreign.write_text('{"base": "trump", "index": 0, "rng_seed": 99}\n')
    try:
        census_carried(foreign, tasks)
    except SystemExit as exc:
        assert "not a task" in str(exc.code)
    else:
        raise AssertionError("a record from another census was carried")
