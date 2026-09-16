"""The probe checker resolves every name a checker hands to the probe loader."""

from __future__ import annotations

from pathlib import Path

from workbench_tools.check_probes import name_faults, names_used


def _checker(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "check_sample.py"
    path.write_text(
        "from workbench_tools.probes import probe\n\n" + body,
        encoding="utf-8",
    )
    return path


def test_a_loaded_name_in_a_group_that_does_not_exist_fails(tmp_path: Path) -> None:
    """The reproduction from #125 F9: `newgroup/zz_missing` passed because no probe
    directory is called `newgroup`, so the name did not look like a probe."""
    caller = _checker(tmp_path, 'page.evaluate(probe("newgroup/zz_missing"))\n')
    have = {"stage/visible-count"}
    faults = name_faults(*names_used([caller]), have)
    assert "newgroup/zz_missing: named by a checker, no such file" in faults


def test_a_name_handed_to_a_wrapper_of_the_loader_is_resolved(tmp_path: Path) -> None:
    body = (
        "def look(probe_name, /, **argument):\n"
        "    return page.evaluate(probe(probe_name), argument or None)\n\n"
        'look("elsewhere/zz_missing", n=3)\n'
        'look("stage/visible-count")\n'
    )
    caller = _checker(tmp_path, body)
    faults = name_faults(*names_used([caller]), {"stage/visible-count"})
    assert faults == ["elsewhere/zz_missing: named by a checker, no such file"]


def test_a_path_that_is_not_handed_to_the_loader_is_not_a_probe(tmp_path: Path) -> None:
    body = 'PAGE = "packing/site/workbench/index.html"\nprobe("stage/visible-count")\n'
    caller = _checker(tmp_path, body)
    assert name_faults(*names_used([caller]), {"stage/visible-count"}) == []


def test_an_unnamed_probe_and_a_missing_name_in_a_known_group_still_fail(
    tmp_path: Path,
) -> None:
    caller = _checker(tmp_path, 'NAMES = ("stage/zz_missing",)\n')
    faults = name_faults(*names_used([caller]), {"stage/visible-count"})
    assert faults == [
        "stage/zz_missing: named by a checker, no such file",
        "stage/visible-count: no checker names it",
    ]
