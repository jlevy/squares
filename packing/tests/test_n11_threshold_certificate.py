"""Controls for the retained `n = 11` threshold certificate, `T-025`.

The gate's own controls live in `test_decide_threshold_certificate.py`; these are about
the retained artifact and about the two gaps the 2026-09-09 adversarial review left open.

`F11`: no positive control exercised a *floored* budget, so nothing in the suite would
have noticed a budget rule that charged a threshold atom `w |S| / k` instead of
`w floor(|S| / k)`. `test_the_floor_is_what_lets_the_two_of_three_atoms_fit` is that
control: a certificate accepted at `n = 34` whose every wrong rule puts it above 34.

`F9`: two forgeries a wrong budget rule would admit, on the retained bytes themselves.
Lowering every threshold to 1 leaves each atom charging its three points separately, and
the budget rises to `15.554605328`, which Condition 2' refuses in closed form. Raising
every threshold to 3 leaves the budget alone -- `floor(3/3) = floor(3/2) = 1` -- and takes
the charge away instead: at the direction that carries the least charge the forgery covers
`0.794018124`, which Condition 5' refuses. A checker that read only the budget would admit
the second; a checker that read only the charge would admit the first.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from cases.n11_threshold_certificate.__main__ import main as replay_main
from cases.n11_threshold_certificate.replay import (
    CERTIFICATE_PATH,
    FROZEN_SHA256,
    budget,
    certificate,
    declared,
    digest,
)
from devtools.check_rung_figures import load_certificate
from devtools.decide_threshold_certificate import decide, load
from sqpack.fractional.threshold import (
    DENSE_CELL_LIMIT,
    ThresholdCertificate,
    closed_form_threshold_conditions,
    minimum_charge,
)
from tests.test_decide_threshold_certificate import write
from tests.test_fractional_threshold_interval import tight_certificate

PACKING = Path(__file__).resolve().parent.parent
CANDIDATE = (
    PACKING
    / "campaign/series/series-000-smoke-and-calibration/results/agenda-034"
    / "lane-b-threshold-candidate-191-50.json"
)
PROOF = PACKING / "cases/n11_threshold_certificate/t-025-threshold-certificate-proof.md"

#: The direction the least cell charge is attained at, in the retained record's own net.
WITNESS_DIRECTION = 69
LEAST_CELL_CHARGE = Fraction(100000203, 100000000)


def forged(threshold: int) -> dict[str, Any]:
    """The retained record with every threshold rewritten to `threshold`.

    The declared `total_budget` goes with it: it describes the retained atoms, and a
    forgery that kept it would be refused for the declaration rather than for the thing
    the control is about.
    """
    record: dict[str, Any] = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    for atom in record["threshold_atoms"]:
        atom["threshold"] = threshold
    record.pop("total_budget", None)
    return record


def loaded_forgery(threshold: int) -> ThresholdCertificate:
    return load(json.dumps(forged(threshold)).encode())[0]


def test_the_retained_bytes_are_the_candidate_the_record_names() -> None:
    """One artifact, one digest: the case copy is the frozen lane-B candidate."""
    assert digest() == FROZEN_SHA256
    assert CERTIFICATE_PATH.read_bytes() == CANDIDATE.read_bytes()
    assert declared() == {
        "claim": "s(11) >= 191/50",
        "variant": "threshold",
        "total_budget": "685457679/62500000",
    }


def test_the_frozen_premises_are_recomputed_from_the_bytes() -> None:
    """Every figure the proof packet's premises table states, read from the certificate.

    The packet is what a stranger reads, so its table is checked against the object it
    describes rather than against the log that produced it.
    """
    retained = certificate()
    assert (retained.n, retained.outer_side, retained.square_side) == (
        11,
        Fraction(191, 50),
        Fraction(9977, 10000),
    )
    assert (len(retained.atoms), len(retained.threshold_atoms)) == (584, 320)
    assert retained.point_mass == Fraction(271052551, 31250000)
    assert retained.threshold_budget == Fraction(143352577, 62500000)
    assert budget() == Fraction(685457679, 62500000) < 11
    assert {(len(a.points), a.threshold) for a in retained.threshold_atoms} == {(3, 2)}

    text = PROOF.read_text(encoding="utf-8")
    for figure in (
        FROZEN_SHA256,
        "`L = 191/50`, `B = 9977/10000`",
        "`271052551/31250000 = 8.673681632`",
        "`143352577/62500000 = 2.293641232`",
        "`685457679/62500000 = 10.967322864 < 11`",
        "`100000203/100000000 = 1.000002030`",
    ):
        assert figure in text, figure


def test_the_figure_checker_reads_the_budget_and_not_the_point_mass() -> None:
    """`check_rung_figures` recomputes the floored budget for a threshold certificate.

    Reading only the point atoms would have it check every quoted total and margin
    against `8.673682`, a number the record does not claim, and `T-025`'s own prose
    would then be measured against the wrong quantity.
    """
    figures = load_certificate(CERTIFICATE_PATH)
    assert figures is not None
    assert figures.outer_side == Fraction(191, 50)
    assert figures.mass == budget()
    assert figures.stored_mass == budget()
    assert figures.atom_count == 584 + 320
    assert figures.margin == 11 - budget()


def test_the_exact_sweep_reproduces_the_registered_least_cell_charge() -> None:
    """The one direction the registered figure comes from, swept again here.

    The whole 181-direction sweep is the case package's own replay; what belongs on the
    pull-request surface is the number the record quotes, at the direction it quotes it
    at, recomputed from the frozen bytes.
    """
    retained = certificate()
    value, _ = minimum_charge(
        retained.atoms,
        retained.threshold_atoms,
        retained.directions[WITNESS_DIRECTION],
        retained.outer_side,
        retained.square_side,
        dense_cell_limit=DENSE_CELL_LIMIT,
    )
    assert value == LEAST_CELL_CHARGE > 1


def test_the_floor_is_what_lets_the_two_of_three_atoms_fit(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`F11`'s missing positive control: a certificate accepted only by `w floor(|S|/k)`.

    The cluster fixture carries sixteen `2`-of-`3` orbit images among its atoms, each
    costing `w` under the theorem's rule and `3w/2` under the ratio a linear relaxation
    would charge. At `n = 34` the certificate is retained by both routes; every wrong
    rule -- the ratio `w |S| / k`, the pigeonhole `w (|S| - k + 1)`, the whole set
    `w |S|` -- puts the budget at or above 34, and `n = 33` shows the acceptance is
    tight against the floored budget rather than roomy.
    """
    fixture = tight_certificate()
    shapes = [(len(a.points), a.threshold) for a in fixture.threshold_atoms]
    assert shapes.count((3, 2)) == 16

    floored = fixture.total_budget
    ratio = fixture.point_mass + sum(
        (
            atom.weight * Fraction(len(atom.points), atom.threshold)
            for atom in fixture.threshold_atoms
        ),
        start=Fraction(0),
    )
    pigeonhole = fixture.point_mass + sum(
        (
            atom.weight * (len(atom.points) - atom.threshold + 1)
            for atom in fixture.threshold_atoms
        ),
        start=Fraction(0),
    )
    whole_set = fixture.point_mass + sum(
        (atom.weight * len(atom.points) for atom in fixture.threshold_atoms),
        start=Fraction(0),
    )
    assert floored == Fraction(100, 3)
    assert min(ratio, pigeonhole, whole_set) >= 34 > floored

    def restate(n: int) -> Callable[[dict[str, object]], None]:
        def edit(record: dict[str, object]) -> None:
            record["n"] = n
            record["claim"] = f"s({n}) >= {fixture.outer_side}"

        return edit

    assert decide(write(tmp_path, fixture, restate(34)), workers=1) is True
    assert "RETAINABLE" in capsys.readouterr().out
    assert decide(write(tmp_path, fixture, restate(33)), workers=1) is False
    assert "Condition 2' total budget below n failed" in capsys.readouterr().out


def test_a_forged_threshold_of_one_is_refused_by_the_budget(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`F9`'s first forgery: three separate points cost three times as much."""
    path = tmp_path / "threshold-one.json"
    path.write_text(json.dumps(forged(1)), encoding="utf-8")
    assert decide(path, workers=1) is False
    out = capsys.readouterr().out
    assert "972162833/62500000" in out
    assert "Condition 2' total budget below n failed" in out
    assert "RETAINABLE" not in out
    assert loaded_forgery(1).total_budget == Fraction(972162833, 62500000)


def test_a_forged_threshold_of_three_keeps_the_budget_and_loses_the_charge() -> None:
    """`F9`'s second forgery, and the reason a budget check alone decides nothing.

    Demanding all three points of every atom leaves `floor(3/3) = floor(3/2) = 1`, so the
    budget, the symmetry, the net and the containment are all exactly the retained ones
    and every closed-form condition still holds. What goes is Condition 5': at the
    direction carrying the least charge the forgery covers `0.794018124`, a quarter short
    of the 1 the counting proof needs.
    """
    forgery = loaded_forgery(3)
    retained = certificate()
    assert forgery.total_budget == retained.total_budget
    assert all(report.holds for report in closed_form_threshold_conditions(forgery))

    value, _ = minimum_charge(
        forgery.atoms,
        forgery.threshold_atoms,
        forgery.directions[WITNESS_DIRECTION],
        forgery.outer_side,
        forgery.square_side,
        dense_cell_limit=DENSE_CELL_LIMIT,
    )
    assert value == Fraction(198504531, 250000000) < 1


@pytest.mark.slow
def test_the_case_package_replays_the_retained_bytes_by_the_interval_route(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The package's own entry point, on the interval route, over the whole doubled net.

    The two-route gate is the retention decision and takes about ninety seconds on three
    workers, which is a command in the proof packet rather than a test. This runs the
    route that is independent of the sweep the fast lane samples above, so between them
    the suite exercises both.
    """
    assert replay_main(["--quick", "--workers", "1"]) == 0
    out = capsys.readouterr().out
    assert "361 directions" in out
    assert f"least point charge {LEAST_CELL_CHARGE} at" in out
    assert "NOT ENOUGH TO RETAIN" in out
