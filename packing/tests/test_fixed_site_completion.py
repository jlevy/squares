"""Toy controls for retained row-completion outcomes and their persistence boundary."""

from __future__ import annotations

import json
import os
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from devtools import run_fixed_site_completion as runner
from devtools.declare_least_cell_mass import load_candidate
from sqpack.fractional.certificate import verify
from sqpack.fractional.colgen import LpSolution, RoundTiming, Rows, site_set_from_grids

SIDE = Fraction(2)
CORE = Fraction(2, 3)
NET = (Fraction(0), Fraction(207107, 500000))


def toy_state(path: Path) -> dict[str, Any]:
    sites = site_set_from_grids(SIDE, (9,), Fraction(0))
    record = {
        "outer_side": str(SIDE),
        "square_side": str(CORE),
        "half_tangents": [str(value) for value in NET],
        "sites": [[str(x), str(y)] for x, y in sites.positions()],
        "rows": [],
    }
    path.write_text(json.dumps(record))
    return record


def execute(state: Path, output: Path, **changes: Any) -> int:
    options: dict[str, Any] = {
        "n": 12,
        "side": SIDE,
        "core": CORE,
        "half_tangents": NET,
        "rows_rounds": 8,
        "rows_per_direction": 3,
        "deadline_seconds": 10.0,
        "scale": 1000,
    }
    options.update(changes)
    return runner.run(state, output, **options)


def test_positive_candidate_and_unconverged_receipt_keep_inputs(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    source = toy_state(state)
    original = state.read_bytes()
    output = tmp_path / "positive"
    assert execute(state, output) == 0
    record = json.loads((output / "receipt.json").read_text())
    assert record["status"] == "candidate-unverified"
    assert record["input"]["sites"] == source["sites"]
    assert record["input"]["half_tangents"] == source["half_tangents"]
    assert record["row_solution"]["converged"]
    assert len(record["row_solution"]["dual"]) == len(record["oracle_rows"])
    assert len(record["snapped_solution"]["primal"]) == len(record["site_orbits"])
    assert record["exact_verification"] == "not-run"
    assert record["finite_site_dual_verification"] == "not-implemented"
    certificate, _ = load_candidate(output / "candidate.json")
    assert 9 <= certificate.total_mass < 12
    assert verify(certificate, workers=1).accepted
    assert state.read_bytes() == original

    deadline_output = tmp_path / "deadline"
    assert execute(state, deadline_output, deadline_seconds=0.0) == 1
    stopped = json.loads((deadline_output / "receipt.json").read_text())
    assert stopped["status"] == "unresolved"
    assert "deadline" in stopped["stop_reason"]
    assert stopped["row_solution"]["objective"] is None
    assert not (deadline_output / "candidate.json").exists()

    overweight_output = tmp_path / "overweight"
    assert execute(state, overweight_output, n=9) == 1
    overweight = json.loads((overweight_output / "receipt.json").read_text())
    assert overweight["status"] == "unresolved"
    assert Fraction(overweight["rational_mass"]) >= 9
    assert not (overweight_output / "candidate.json").exists()


def test_exception_preserves_added_rows_timings_and_both_streams(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = tmp_path / "state.json"
    toy_state(state)

    def fail(sites: Any, _core: Any, _net: Any, rows: Rows, **kwargs: Any) -> LpSolution:
        row = np.zeros(len(sites.orbits))
        row[0] = 1
        rows.add(0, (1.0, 1.0), row)
        kwargs["timings"].append(RoundTiming(0, 0.1, 0.2, 1, 1, 1, 3.0))
        print("python stdout retained")
        os.write(2, b"native stderr retained\n")
        raise RuntimeError("injected solver failure")

    monkeypatch.setattr(runner, "solve_rows", fail)
    output = tmp_path / "failed"
    assert execute(state, output) == 2
    record = json.loads((output / "receipt.json").read_text())
    assert record["status"] == "technical-failure"
    assert record["row_solution"] is None
    assert record["vectors_unavailable_reason"]
    assert record["exact_rows"] == [[0, "1", "1"]]
    assert record["round_timings"][0]["rows_added"] == 1
    assert "python stdout retained" in (output / "stdout.log").read_text()
    assert "native stderr retained" in (output / "stderr.log").read_text()
    assert "injected solver failure" in (output / "stderr.log").read_text()


def test_identity_refusals_and_output_collision_never_start_solver(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = tmp_path / "state.json"
    source = toy_state(state)

    def forbidden(*_args: Any, **_kwargs: Any) -> LpSolution:
        raise AssertionError("input refusal must precede the solver")

    monkeypatch.setattr(runner, "solve_rows", forbidden)
    for index, changes in enumerate(
        ({"side": Fraction(3)}, {"half_tangents": (Fraction(0), Fraction(1, 4))})
    ):
        output = tmp_path / str(index)
        assert execute(state, output, **changes) == 2
        assert json.loads((output / "receipt.json").read_text())["status"] == "refused"
        original = (output / "receipt.json").read_bytes()
        assert execute(state, output) == 2
        assert (output / "receipt.json").read_bytes() == original
    source["sites"].pop()
    state.write_text(json.dumps(source))
    assert execute(state, tmp_path / "changed-sites") == 2


def test_nonfinite_converged_result_cannot_publish_candidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = tmp_path / "state.json"
    toy_state(state)

    def nonfinite(sites: Any, *_args: Any, **_kwargs: Any) -> LpSolution:
        return LpSolution(
            np.ones(len(sites.orbits)),
            np.zeros(0),
            float("nan"),
            stopped="converged: synthetic",
            least_covered=1.0,
        )

    monkeypatch.setattr(runner, "solve_rows", nonfinite)
    output = tmp_path / "nonfinite"
    assert execute(state, output) == 2
    record = json.loads((output / "receipt.json").read_text())
    assert record["status"] == "refused"
    assert record["row_solution"]["objective"] is None
    assert not (output / "candidate.json").exists()


def test_nonuniform_net_is_refused_before_input_or_solver_access(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> LpSolution:
        raise AssertionError("nonuniform net must be refused before the solver")

    monkeypatch.setattr(runner, "solve_rows", forbidden)
    output = tmp_path / "nonuniform"
    assert (
        execute(
            tmp_path / "absent-state.json",
            output,
            half_tangents=(Fraction(0), Fraction(1, 10), Fraction(2, 5)),
        )
        == 2
    )
    record = json.loads((output / "receipt.json").read_text())
    assert record["status"] == "refused"
    assert "uniformly spaced" in record["stop_reason"]
    assert not (output / "input.json").exists()
    assert not (output / "candidate.json").exists()


def test_round_cap_retains_returned_vectors_without_a_second_row_solve(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = tmp_path / "state.json"
    toy_state(state)
    calls = []

    def limited(sites: Any, _core: Any, _net: Any, rows: Rows, **kwargs: Any) -> LpSolution:
        calls.append(kwargs["max_rounds"])
        row = np.ones(len(sites.orbits))
        rows.add(0, (1.0, 1.0), row)
        kwargs["timings"].append(RoundTiming(0, 0.1, 0.2, 1, 1, 1, 3.0))
        return LpSolution(
            np.ones(len(sites.orbits)),
            np.array([3.0]),
            3.0,
            rounds=1,
            rows=1,
            stopped="round limit 8 reached",
            least_covered=0.5,
        )

    monkeypatch.setattr(runner, "solve_rows", limited)
    output = tmp_path / "round-cap"
    assert execute(state, output) == 1
    record = json.loads((output / "receipt.json").read_text())
    assert calls == [8]
    assert record["row_solution"]["dual"] == [3.0]
    assert record["vectors_unavailable_reason"] is None
    assert record["exact_rows"] == [[0, "1", "1"]]
    assert record["additional_rows"] == 1
    assert record["snapped_solution"] is None


def test_terminal_publication_failure_preserves_started_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = tmp_path / "state.json"
    toy_state(state)
    publish = runner.atomic_write_text

    def fail_terminal(path: Path, text: str) -> None:
        if path.name == "receipt.json" and json.loads(text)["status"] != "started":
            raise OSError("injected before publication")
        publish(path, text)

    monkeypatch.setattr(runner, "atomic_write_text", fail_terminal)
    output = tmp_path / "publication"
    assert execute(state, output, deadline_seconds=0.0) == 2
    record = json.loads((output / "receipt.json").read_text())
    assert record["status"] == "started"


def test_failed_later_lp_identifies_the_last_solved_dual_prefix(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = tmp_path / "state.json"
    toy_state(state)

    def failed_lp(sites: Any, _core: Any, _net: Any, rows: Rows, **_kwargs: Any) -> LpSolution:
        first = np.zeros(len(sites.orbits))
        first[0] = 1
        second = np.zeros(len(sites.orbits))
        second[1] = 1
        rows.add(0, (1.0, 1.0), first)
        rows.add(0, (1.1, 1.0), second)
        return LpSolution(
            np.ones(len(sites.orbits)),
            np.array([3.0]),
            3.0,
            stopped="linear program refused the generated rows",
        )

    monkeypatch.setattr(runner, "solve_rows", failed_lp)
    output = tmp_path / "failed-later-lp"
    assert execute(state, output) == 1
    record = json.loads((output / "receipt.json").read_text())
    assert len(record["oracle_rows"]) == 2
    assert len(record["exact_rows"]) == 2
    assert record["row_solution"]["dual_row_count"] == 1
    assert record["row_solution"]["dual"] == [3.0]
    assert "shorter prefix" in record["row_solution"]["basis"]
    assert record["snapped_solution"] is None
    assert not (output / "candidate.json").exists()


def test_cli_binds_legacy_state_to_an_explicitly_declared_net(tmp_path: Path) -> None:
    state = tmp_path / "legacy.json"
    source = toy_state(state)
    del source["half_tangents"]
    state.write_text(json.dumps(source))
    output = tmp_path / "cli"
    assert (
        runner.main(
            [
                "--state",
                str(state),
                "--output",
                str(output),
                "--n",
                "12",
                "--side",
                "2",
                "--core",
                "2/3",
                "--angle-limit",
                "207107/500000",
                "--steps",
                "1",
                "--rows-rounds",
                "3",
                "--rows-per-direction",
                "2",
                "--deadline-seconds",
                "0",
                "--scale",
                "777",
            ]
        )
        == 1
    )
    record = json.loads((output / "receipt.json").read_text())
    assert record["net_binding"] == "caller-declared; source state does not contain its net"
    assert record["parameters"]["half_tangents"] == [str(value) for value in NET]
    assert record["parameters"]["rows_rounds"] == 3
    assert record["parameters"]["rows_per_direction"] == 2
    assert record["parameters"]["scale"] == 777
    assert "deadline" in record["stop_reason"]
