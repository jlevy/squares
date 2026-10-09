"""Soundness artifact selection, with synthetic engines and no search or LP solves."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Self

import pytest

from devtools import check_soundness_perimeter as tool


def test_external_executable_keeps_the_search_recipe_and_best_chain(tmp_path: Path) -> None:
    engine = tmp_path / "external-cargo" / "release" / "sqsearch"
    engine.parent.mkdir(parents=True)
    engine.write_text(
        f"#!{sys.executable}\n"
        "import json,sys\n"
        "assert sys.argv[1:]==['--n','5','--seed','1','--chains','4',"
        "'--budget-moves','4000000']\n"
        "print(json.dumps({'kind':'metadata'}))\n"
        "print(json.dumps({'kind':'chain','best_side':3}))\n"
        "print(json.dumps({'kind':'chain','best_side':2}))\n"
    )
    engine.chmod(0o755)
    assert tool.anneal(5, 1, engine) == {"kind": "chain", "best_side": 2}


def test_explicit_missing_binary_refuses_before_any_configuration_work(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        tool.subprocess, "run", lambda *_a, **_k: pytest.fail("configuration work started")
    )
    with pytest.raises(SystemExit) as stopped:
        tool.main(["--binary", str(tmp_path / "missing")])
    assert stopped.value.code == 2


@pytest.mark.parametrize("mode", ["default_present", "default_missing", "external"])
def test_main_selects_the_artifact_and_keeps_all_engine_oracle_cells(
    mode: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    default, external = tmp_path / "default-engine", tmp_path / "external-engine"
    if mode != "default_missing":
        (external if mode == "external" else default).touch()
    monkeypatch.setattr(tool, "BIN", default)
    engine_calls: list[int] = []
    units_seen: list[Any] = []

    def run(command: list[str], **_options: Any) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["-m", "cases.trump11.export_seed"]:
            value = {"x": [0], "y": [0], "t": [0], "side": 1}
        else:
            expected = external if mode == "external" else default
            assert command[0] == str(expected)
            n = int(command[2])
            engine_calls.append(n)
            assert command[3:] == ["--seed", "1", "--chains", "4", "--budget-moves", "4000000"]
            value = {
                "kind": "chain",
                "x": list(range(n)),
                "y": [0] * n,
                "t": [0] * n,
                "best_side": n,
            }
        return subprocess.CompletedProcess(command, 0, stdout=json.dumps(value))

    class Pool:
        def __enter__(self) -> Self:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def map(self, fn: Any, units: Any) -> list[tuple[list[str], int]]:
            assert fn.__name__ == "_quench_unit"
            units_seen.extend(units)
            return [([], 1) for _ in units_seen]

    monkeypatch.setattr(tool.subprocess, "run", run)
    monkeypatch.setattr(tool, "ProcessPoolExecutor", lambda **_kwargs: Pool())
    arguments = ["--binary", str(external)] if mode == "external" else []
    assert tool.main(arguments) == 0
    assert len(units_seen) == 18
    assert [unit[0] for unit in units_seen] == [
        "solve_to_fixed_point",
        "quench",
        "quench_bracket",
    ] * 6
    assert engine_calls == ([] if mode == "default_missing" else [5, 10, 11])
    captured = capsys.readouterr()
    assert ("skipping engine cells" in captured.err) == (mode == "default_missing")
    assert f"{19 if mode == 'default_missing' else 22} configurations" in captured.out
