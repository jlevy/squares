"""Controls for the sites-1 retain-or-refuse command.

think-3xbr needs an in-tree producer for the A6 sites-1 matrix. The matrix is
not in the repository, the original driver is a ``.py.txt`` record, and
``run_fractional_colgen`` cannot emit it. These tests hold the command to that
fact: missing inputs refuse, ``--check`` writes no checkpoint, and the module
embeds no JavaScript.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from devtools import check_no_embedded_js as guard
from devtools.regenerate_sites1_checkpoint import (
    SITES1,
    CheckpointSpec,
    default_layout,
    inspect,
    main,
    producer_ready,
)

MODULE = Path(__file__).resolve().parents[1] / "devtools/regenerate_sites1_checkpoint.py"
TINY = CheckpointSpec(
    outer_side=Fraction(1),
    square_side=Fraction(1, 2),
    n=2,
    rows=2,
    sites=3,
    site_orbits=2,
    atom_orbits=1,
)


def _write_checkpoint(
    directory: Path,
    *,
    names: tuple[str, str, str] = ("sites.json", "atoms.json", "rows.json"),
    spec: CheckpointSpec = TINY,
) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    sites = [[["0", "0"]], [["1", "0"], ["0", "1"]]]
    assert len(sites) == spec.site_orbits
    assert sum(len(orbit) for orbit in sites) == spec.sites
    (directory / names[0]).write_text(json.dumps(sites) + "\n", encoding="utf-8")
    atoms = {
        "outer_side": str(spec.outer_side),
        "atoms": [
            {
                "points": [["0", "0"], ["1", "0"], ["0", "1"]],
                "threshold": 2,
                "orbit_size": 1,
            }
        ],
    }
    (directory / names[1]).write_text(json.dumps(atoms) + "\n", encoding="utf-8")
    rows = [[0, "1/2", "1/2"], [1, "1/4", "3/4"]]
    assert len(rows) == spec.rows
    (directory / names[2]).write_text(json.dumps(rows) + "\n", encoding="utf-8")


def test_the_repository_does_not_hold_the_sites1_matrix() -> None:
    receipt = inspect(default_layout())
    assert receipt.spec == SITES1
    assert receipt.checkpoint_in_repo is False
    assert receipt.status == "missing-inputs"
    assert receipt.rows_complete is False
    assert receipt.producer_ready is False
    assert producer_ready() is False
    assert any("lp-run4-sites" in item for item in receipt.missing)
    assert "sepcore.FamilyGeometry.vertex_candidates" in receipt.missing
    assert "lp383.HighsLP" in receipt.missing


def test_missing_inputs_refuse(tmp_path: Path, capsys) -> None:
    output = tmp_path / "out"
    receipt_path = output / "sites-1-receipt.json"
    code = main(
        [
            "--output-dir",
            str(output),
            "--lp-run4",
            str(tmp_path / "no-lp-run4"),
            "--state",
            str(tmp_path / "missing-state.json"),
            "--receipt",
            str(receipt_path),
            "--log",
            str(output / "sites-1.log"),
        ]
    )
    captured = capsys.readouterr()
    assert code == 2
    assert not (output / "sites-1-sites.json").exists()
    assert not (output / "sites-1-atoms.json").exists()
    assert not (output / "sites-1-rows.json").exists()
    assert "missing-inputs" in captured.err
    assert "lp-run4-sites" in captured.err
    payload = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert payload["status"] == "missing-inputs"
    assert payload["rows_complete"] is False
    assert payload["checkpoint_in_repo"] is False
    assert "generate_adaptive" in payload["in_tree_colgen"]


def test_check_does_not_write_a_fake_checkpoint(tmp_path: Path) -> None:
    output = tmp_path / "out"
    code = main(
        [
            "--check",
            "--output-dir",
            str(output),
            "--lp-run4",
            str(tmp_path / "no-lp-run4"),
            "--state",
            str(tmp_path / "missing-state.json"),
            "--receipt",
            str(output / "sites-1-receipt.json"),
            "--log",
            str(output / "sites-1.log"),
        ]
    )
    assert code == 2
    assert not output.exists()


def test_check_does_not_write_a_count_mismatch_as_sites1(tmp_path: Path) -> None:
    resume = tmp_path / "resume"
    _write_checkpoint(resume)
    output = tmp_path / "out"
    code = main(
        [
            "--check",
            "--resume",
            str(resume),
            "--output-dir",
            str(output),
            "--lp-run4",
            str(tmp_path / "no-lp-run4"),
            "--state",
            str(tmp_path / "missing-state.json"),
            "--receipt",
            str(output / "sites-1-receipt.json"),
            "--log",
            str(output / "sites-1.log"),
        ]
    )
    assert code == 2
    assert not output.exists()


def test_matching_checkpoint_is_retained_without_solving(tmp_path: Path) -> None:
    resume = tmp_path / "resume"
    _write_checkpoint(resume)
    layout = default_layout(
        state=tmp_path / "state.json",
        lp_run4=tmp_path / "lp-run4",
        output_dir=tmp_path / "out",
        resume=resume,
        receipt=tmp_path / "out" / "sites-1-receipt.json",
        log=tmp_path / "out" / "sites-1.log",
    )
    receipt = inspect(layout, spec=TINY)
    assert receipt.status == "retained"
    assert receipt.stop_reason == "retained-existing-checkpoint"
    assert receipt.rows_complete is False
    assert receipt.missing == ()
    assert receipt.observed is not None
    assert receipt.observed.sites == 3
    assert not (tmp_path / "out" / "sites-1-sites.json").exists()


def test_lp_run4_without_the_in_tree_producer_still_refuses(tmp_path: Path, capsys) -> None:
    run4 = tmp_path / "lp-run4"
    _write_checkpoint(run4, spec=TINY)
    state = tmp_path / "state.json"
    state.write_text(
        json.dumps({"outer_side": "191/50", "sites": [], "rows": []}) + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "out"
    code = main(
        [
            "--output-dir",
            str(output),
            "--lp-run4",
            str(run4),
            "--state",
            str(state),
            "--receipt",
            str(output / "sites-1-receipt.json"),
            "--log",
            str(output / "sites-1.log"),
        ]
    )
    captured = capsys.readouterr()
    assert code == 2
    payload = json.loads((output / "sites-1-receipt.json").read_text(encoding="utf-8"))
    assert payload["status"] == "missing-producer"
    assert payload["rows_complete"] is False
    assert "sepcore.FamilyGeometry.vertex_candidates" in captured.err
    assert not (output / "sites-1-sites.json").exists()


def test_the_command_embeds_no_javascript() -> None:
    policy = guard.load_policy()
    source = MODULE.read_text(encoding="utf-8")
    assert guard.scan_source(MODULE.name, source, policy) == []
    tests = Path(__file__).read_text(encoding="utf-8")
    assert guard.scan_source(Path(__file__).name, tests, policy) == []
