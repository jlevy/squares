"""Controls for `devtools.freeze_cutting_primal`, the cutting loop's covering bridge.

The loop retains sites and rows and freezes only its packing family; the bridge
is the missing path from a row-converged covering objective to bytes the gate
can decide. The positive control is the smallest instance the exact sweep
accepts on the coarse two-direction net: ``B = 2/3`` in side 2, where the
containment condition ``B(1 + D) < 1`` still holds at the net's 22.5-degree
half gap and a nine-point grid covers every placement. Nine disjoint
``B``-squares fit, so the covering value is at least 9: the bridge must freeze
a candidate below 12 and refuse to freeze anything for ``n = 9``. An
unconverged row loop and an existing output path are refused before any bytes
are written.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools.declare_least_cell_mass import load_candidate
from devtools.freeze_cutting_primal import RefusalError, bridge, main
from sqpack.fractional.certificate import verify
from sqpack.fractional.colgen import Rows, site_set_from_grids
from sqpack.fractional.cutting import cutting_plane_loop

B = Fraction(2, 3)
LIMIT = Fraction(207107, 500000)
COARSE = (Fraction(0), LIMIT)
TWO = Fraction(2)


@pytest.fixture
def state(tmp_path: Path) -> Path:
    """One cutting iteration at side 2, saved the way the driver saves it."""

    path = tmp_path / "state.json"
    log = cutting_plane_loop(
        12,
        TWO,
        B,
        COARSE,
        sites=site_set_from_grids(TWO, (9,), Fraction(0)),
        rows=Rows(),
        exact_rows=[],
        cap=20,
        max_iterations=1,
        state_path=path,
    )
    assert log.iterations, log.stopped
    return path


def test_the_bridge_freezes_a_candidate_the_exact_sweep_accepts(state: Path) -> None:
    certificate, receipt = bridge(state, n=12, half_tangents=COARSE, scale=1000)
    assert str(receipt["rows_stopped"]).startswith("converged")
    assert receipt["total_mass"] == str(certificate.total_mass)
    # Nine disjoint B-squares fit in side 2, so no cover weighs less than 9.
    assert 9 <= certificate.total_mass < 12
    verdict = verify(certificate, workers=1)
    assert verdict.accepted, verdict.failures
    assert verdict.minimum_cell_mass is not None
    assert verdict.minimum_cell_mass >= 1


def test_the_frozen_bytes_are_the_retained_shape_with_no_declaration(
    state: Path, tmp_path: Path
) -> None:
    frozen = tmp_path / "out" / "candidate.json"
    receipt = tmp_path / "out" / "receipt.json"
    arguments = [
        "--n", "12", "--state", str(state), "--angle-limit", str(LIMIT), "--steps", "1",
        "--scale", "1000", "--freeze", str(frozen), "--json", str(receipt),
    ]  # fmt: skip
    assert main(arguments) == 0
    record = json.loads(frozen.read_text())
    assert record["least_cell_mass"] is None
    assert record["claim"] == "s(12) >= 2"
    assert record["direction_steps"] == 1
    certificate, _ = load_candidate(frozen)
    assert str(certificate.total_mass) == record["total_mass"]
    written = json.loads(receipt.read_text())
    assert written["frozen"] == str(frozen)
    assert written["atoms"] == len(record["atoms"])
    # A candidate is never overwritten: the second run refuses before touching it.
    before = frozen.read_bytes()
    assert main(arguments) == 1
    assert frozen.read_bytes() == before


def test_a_total_at_or_above_n_is_no_candidate(state: Path) -> None:
    with pytest.raises(RefusalError, match="not below 9"):
        bridge(state, n=9, half_tangents=COARSE, scale=1000)


def test_an_unconverged_row_loop_is_refused_before_any_program_is_read(state: Path) -> None:
    with pytest.raises(RefusalError, match="did not converge"):
        bridge(state, n=12, half_tangents=COARSE, scale=1000, deadline_seconds=0.0)
    with pytest.raises(RefusalError, match="positive"):
        bridge(state, n=0, half_tangents=COARSE)
