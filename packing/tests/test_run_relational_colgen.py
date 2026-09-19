"""Controls for the think-gyzw guarded relational colgen command.

H-217 needs a checkpointed replacement-support loop, but the A6 sites-1 matrix
is unretained and ``run_fractional_colgen.generate_adaptive`` is point-atom
only. These tests hold the command to that fact: missing inputs refuse without
covering, a tiny synthetic matrix is acknowledged without covering, ``--check``
writes nothing, the module embeds no JavaScript, and no ``.py.txt`` is imported
or exec'd.
"""

from __future__ import annotations

import ast
import json
from fractions import Fraction
from pathlib import Path

from devtools import check_no_embedded_js as guard
from devtools.regenerate_sites1_checkpoint import SITES1, CheckpointSpec
from devtools.run_relational_colgen import (
    default_colgen_layout,
    inspect_run,
    main,
)

MODULE = Path(__file__).resolve().parents[1] / "devtools/run_relational_colgen.py"
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


def _call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


def test_the_repository_does_not_hold_the_sites1_matrix(capsys) -> None:
    layout = default_colgen_layout()
    receipt = inspect_run(layout)
    payload = receipt.as_dict()
    assert receipt.sites1.spec == SITES1
    assert receipt.status == "missing-inputs"
    assert payload["rows_complete"] is False
    assert payload["covering_ran"] is False
    assert payload["h217_verdict"] is None
    assert receipt.sites1.checkpoint_in_repo is False
    assert any("lp-run4-sites" in item for item in receipt.sites1.missing)
    code = main(["--check"])
    captured = capsys.readouterr()
    assert code == 2
    assert "missing-inputs" in captured.err
    assert not layout.receipt.exists()
    assert not layout.log.exists()


def test_check_writes_nothing(tmp_path: Path) -> None:
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
            str(output / "relational-colgen-receipt.json"),
            "--log",
            str(output / "relational-colgen.log"),
        ]
    )
    assert code == 2
    assert not output.exists()


def test_missing_inputs_refuse_without_covering(tmp_path: Path, capsys) -> None:
    output = tmp_path / "out"
    receipt_path = output / "relational-colgen-receipt.json"
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
            str(output / "relational-colgen.log"),
        ]
    )
    captured = capsys.readouterr()
    assert code == 2
    assert "missing-inputs" in captured.err
    assert "lp-run4-sites" in captured.err
    payload = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert payload["status"] == "missing-inputs"
    assert payload["rows_complete"] is False
    assert payload["covering_ran"] is False
    assert payload["h217_verdict"] is None
    assert payload["status"] in {"missing-inputs", "missing-producer", "refused"}
    assert "generate_adaptive" in payload["in_tree_colgen"]


def test_n_other_than_11_without_a_matrix_still_refuses(tmp_path: Path) -> None:
    output = tmp_path / "out"
    receipt_path = output / "relational-colgen-receipt.json"
    code = main(
        [
            "--n",
            "6",
            "--output-dir",
            str(output),
            "--lp-run4",
            str(tmp_path / "no-lp-run4"),
            "--state",
            str(tmp_path / "missing-state.json"),
            "--receipt",
            str(receipt_path),
            "--log",
            str(output / "relational-colgen.log"),
        ]
    )
    assert code == 2
    payload = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert payload["n"] == 6
    assert payload["status"] == "missing-inputs"
    assert payload["covering_ran"] is False
    assert payload["h217_verdict"] is None


def test_producer_inputs_without_sites1_still_do_not_cover(tmp_path: Path, capsys) -> None:
    run4 = tmp_path / "lp-run4"
    _write_checkpoint(run4, spec=TINY)
    state = tmp_path / "state.json"
    state.write_text(
        json.dumps({"outer_side": "191/50", "sites": [], "rows": []}) + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "out"
    receipt_path = output / "relational-colgen-receipt.json"
    code = main(
        [
            "--output-dir",
            str(output),
            "--lp-run4",
            str(run4),
            "--state",
            str(state),
            "--receipt",
            str(receipt_path),
            "--log",
            str(output / "relational-colgen.log"),
        ]
    )
    captured = capsys.readouterr()
    assert code == 2
    payload = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert payload["status"] == "missing-producer"
    assert payload["covering_ran"] is False
    assert payload["h217_verdict"] is None
    assert "sepcore.FamilyGeometry.vertex_candidates" in captured.err


def test_tiny_matrix_is_present_and_does_not_run_covering(tmp_path: Path) -> None:
    resume = tmp_path / "resume"
    _write_checkpoint(resume)
    layout = default_colgen_layout(
        state=tmp_path / "state.json",
        lp_run4=tmp_path / "lp-run4",
        output_dir=tmp_path / "out",
        resume=resume,
        receipt=tmp_path / "out" / "relational-colgen-receipt.json",
        log=tmp_path / "out" / "relational-colgen.log",
    )
    receipt = inspect_run(layout, spec=TINY, n=2)
    payload = receipt.as_dict()
    assert receipt.status == "matrix-present-no-covering"
    assert payload["covering_ran"] is False
    assert payload["rows_complete"] is False
    assert payload["h217_verdict"] is None
    assert receipt.sites1.checkpoint_in_repo is True
    assert receipt.sites1.observed is not None
    assert receipt.sites1.observed.sites == 3
    assert not (tmp_path / "out" / "relational-colgen-receipt.json").exists()


def test_family_without_sites1_is_a_dry_stub_and_still_refuses(tmp_path: Path) -> None:
    family = tmp_path / "family.json"
    family.write_text("{}\n", encoding="utf-8")
    output = tmp_path / "out"
    receipt_path = output / "relational-colgen-receipt.json"
    code = main(
        [
            "--family",
            str(family),
            "--output-dir",
            str(output),
            "--lp-run4",
            str(tmp_path / "no-lp-run4"),
            "--state",
            str(tmp_path / "missing-state.json"),
            "--receipt",
            str(receipt_path),
            "--log",
            str(output / "relational-colgen.log"),
        ]
    )
    assert code == 2
    payload = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert payload["covering_ran"] is False
    assert payload["h217_verdict"] is None
    assert payload["family_handoff"]["decided"] is False
    assert payload["family_handoff"]["family_present"] is True
    assert payload["family_handoff"]["status"] == "refused"


def test_the_command_embeds_no_javascript() -> None:
    policy = guard.load_policy()
    source = MODULE.read_text(encoding="utf-8")
    assert guard.scan_source(MODULE.name, source, policy) == []
    tests = Path(__file__).read_text(encoding="utf-8")
    assert guard.scan_source(Path(__file__).name, tests, policy) == []


def test_does_not_import_or_exec_py_txt() -> None:
    source = MODULE.read_text(encoding="utf-8")
    tree = ast.parse(source)
    banned_roots = {"sepcore", "lp383", "runpy", "importlib"}
    banned_calls = {
        "exec",
        "eval",
        "run_path",
        "run_module",
        "generate_adaptive",
        "decide",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                assert root not in banned_roots
                assert ".py.txt" not in alias.name
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            root = module.split(".", 1)[0]
            assert root not in banned_roots
            assert ".py.txt" not in module
            imported = {alias.name for alias in node.names}
            assert "generate_adaptive" not in imported
            assert "decide" not in imported
        elif isinstance(node, ast.Call):
            assert _call_name(node) not in banned_calls
