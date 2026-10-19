# pyright: reportPrivateUsage=false
"""The push selector keeps code-like strings and real repository walkers conservative."""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools import reachable_tests


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("# Path('repo').rglob('*')\n", False),
        ("from importlib.metadata import version\nversion('sqpack')\n", False),
        ("from importlib.metadata import version as package_version\n", True),
        ("attack = \"__import__('os')\"\n", True),
        ("payload = b\"__import__('x')\"\n", True),
        ("from pathlib import Path\nPath('repo').rglob('*')\n", True),
        ("rglob('repo')\n", True),
        ("iterdir('repo')\n", True),
        ("my_rglob('repo')\n", True),
        ("repo_listdir('repo')\n", True),
        ("from os import listdir\nlistdir('repo')\n", True),
        ("import importlib.util\n", True),
        ("from helper_importlib_adapter import version\n", True),
        ("__import__('module')\n", True),
        ("import builtins\nbuiltins.__import__('module')\n", True),
        ("from helper import importlib\nimportlib.import_module(name)\n", True),
        ("def f():\n    global importlib_cache\n", True),
        ("try: pass\nexcept Exception as __import__error: pass\n", True),
        ("import subprocess as sp\nsp.run(['python', '-c', \"__import__('x')\"])\n", True),
        ("def run_code(script): pass\nrun_code(\"__import__('x')\")\n", True),
        ("script = f\"__import__('pathlib').Path({1!r})\"\n", True),
        ("def broken(:\n", True),
    ],
)
def test_walker_evidence_discards_comments_but_keeps_executable_inputs(
    tmp_path: Path, source: str, *, expected: bool
) -> None:
    # Failed-only tmp retention may reuse a passed case's directory. Production scans
    # one static tree, but each parameter here writes new source at the same path.
    reachable_tests._walker_evidence.cache_clear()  # noqa: SLF001
    test = tmp_path / "test_walker.py"
    test.write_text(source, encoding="utf-8")
    assert reachable_tests._walker_evidence(test) is expected  # noqa: SLF001


@pytest.fixture(scope="module")
def static_tree() -> None:
    """The static tree `select_tests` parses and memoizes for the life of the process,
    paid in setup, as `test_reachable_tests` pays it: called first, the parse held this
    test past the 12 s per-test rule (12.18 s on run 37383614128) while the selection
    itself takes under a second."""
    reachable_tests.select_tests(["packing/src/sqpack/cli/validate.py"])


@pytest.mark.usefixtures("static_tree")
def test_benign_metadata_import_no_longer_expands_an_unrelated_frontier_change() -> None:
    selection = reachable_tests.select_tests(["packing/frontier/n-011.md"])
    assert not selection.everything
    assert "packing/tests/test_command_help.py" not in selection.tests
    assert "packing/tests/test_verified_upper_bound_contract.py" in selection.tests
    # The parser attack literal remains in the conservative walker set.
    assert "packing/tests/test_audit_ds7_lower_bounds.py" in selection.tests


def test_import_scan_keeps_nested_suites_and_ignores_literal_code(tmp_path: Path) -> None:
    source = tmp_path / "imports.py"
    source.write_text(
        "payload = ['import imaginary.module', {'nested': 'from fake import thing'}]\n"
        "async def f():\n"
        "    try:\n"
        "        import genuine.module\n"
        "    except Exception:\n"
        "        from error_path import handler\n"
        "    match payload:\n"
        "        case []:\n"
        "            from match_path import leaf\n",
        encoding="utf-8",
    )
    assert reachable_tests._imports_of(source) == {  # noqa: SLF001
        "genuine.module",
        "error_path",
        "error_path.handler",
        "match_path",
        "match_path.leaf",
    }
