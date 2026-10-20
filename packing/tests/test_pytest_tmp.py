"""pytest's temporary directories stay bounded: failed-only retention, killed sessions reaped.

Each nested session runs under its own `PYTEST_DEBUG_TEMPROOT`, so the numbered
directories it creates and prunes are this test's and never another session's.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

from devtools import pytest_tmp

PACKING = Path(__file__).resolve().parents[1]


def _project_pytest_options() -> dict[str, object]:
    document = tomllib.loads((PACKING / "pyproject.toml").read_text(encoding="utf-8"))
    return document["tool"]["pytest"]["ini_options"]


def _write_suite(
    directory: Path, source: str, *, policy: str, count: int, budget: str | None = None
) -> Path:
    directory.mkdir()
    (directory / "pytest.ini").write_text(
        f"[pytest]\ntmp_path_retention_policy = {policy}\ntmp_path_retention_count = {count}\n"
        + ("" if budget is None else f"{pytest_tmp.BUDGET_OPTION} = {budget}\n"),
        encoding="utf-8",
    )
    (directory / "test_suite.py").write_text(source, encoding="utf-8")
    return directory


def _session(
    suite: Path, temproot: Path, *, plugin: bool, extra: tuple[str, ...] = ()
) -> subprocess.CompletedProcess[str]:
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("PYTEST_", "PACKING_REACHABLE_TEST_"))
    }
    environment["PYTEST_DEBUG_TEMPROOT"] = str(temproot)
    environment["TMPDIR"] = str(temproot)
    environment["PYTHONPATH"] = os.pathsep.join(
        (str(PACKING), os.environ.get("PYTHONPATH", ""))
    )
    return subprocess.run(
        (
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-c",
            str(suite / "pytest.ini"),
            "--rootdir",
            str(suite),
            "-p",
            "no:cacheprovider",
            "-p",
            "no:xdist",
            *(("-p", "devtools.pytest_tmp") if plugin else ()),
            *extra,
            str(suite),
        ),
        cwd=suite,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )


def _numbered(temproot: Path) -> list[str]:
    return sorted(
        entry.name
        for root in temproot.glob("pytest-of-*")
        for entry in root.iterdir()
        if entry.name.startswith(("pytest-", "garbage-")) and not entry.is_symlink()
    )


def test_project_config_keeps_only_failures_and_loads_the_plugin() -> None:
    options = _project_pytest_options()
    assert options["tmp_path_retention_policy"] == "failed"
    assert int(str(options["tmp_path_retention_count"])) >= 1
    assert float(str(options[pytest_tmp.BUDGET_OPTION])) > 0
    addopts = options["addopts"]
    assert isinstance(addopts, list)
    assert ["-p", "devtools.pytest_tmp"] in [addopts[i : i + 2] for i in range(len(addopts))]


def test_passing_session_leaves_nothing_and_a_failing_one_only_its_failure(
    tmp_path: Path,
) -> None:
    options = _project_pytest_options()
    suite = _write_suite(
        tmp_path / "suite",
        "import pytest\n"
        "def test_pass(tmp_path):\n"
        "    (tmp_path / 'blob').write_bytes(bytes(1 << 20))\n"
        "@pytest.mark.parametrize('fail', [False, True])\n"
        "def test_maybe(tmp_path, fail):\n"
        "    (tmp_path / 'blob').write_bytes(bytes(1 << 20))\n"
        "    assert not fail\n",
        policy=str(options["tmp_path_retention_policy"]),
        count=int(str(options["tmp_path_retention_count"])),
    )
    temproot = tmp_path / "temproot"
    temproot.mkdir()

    passing = _session(suite, temproot, plugin=True, extra=("-k", "not True"))
    assert passing.returncode == 0, passing.stdout + passing.stderr
    assert _numbered(temproot) == []

    failing = _session(suite, temproot, plugin=True)
    assert failing.returncode == 1, failing.stdout + failing.stderr
    [session] = [
        path for path in temproot.glob("pytest-of-*/pytest-*") if not path.is_symlink()
    ]
    kept = sorted(entry.name for entry in session.iterdir() if not entry.is_symlink())
    assert kept == ["test_maybe_True_0"]


def test_a_killed_session_is_reclaimed_once_newer_sessions_retire_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Count 1 keeps the demonstration to three sessions; the lock rule is the same at any
    # count, and the project's own count is checked above.
    suite = _write_suite(
        tmp_path / "suite",
        "import os, signal\n"
        "def test_outcome(tmp_path):\n"
        "    (tmp_path / 'blob').write_bytes(bytes(1 << 20))\n"
        "    if os.environ.get('OUTCOME') == 'killed':\n"
        "        os.kill(os.getpid(), signal.SIGKILL)\n"
        "    assert os.environ.get('OUTCOME') != 'failed'\n",
        policy="failed",
        count=1,
    )
    temproot = tmp_path / "temproot"
    temproot.mkdir()

    monkeypatch.setenv("OUTCOME", "killed")
    killed = _session(suite, temproot, plugin=True)
    assert killed.returncode == -9
    assert _numbered(temproot) == ["pytest-0"]
    [lock] = temproot.glob("pytest-of-*/pytest-0/.lock")
    assert not pytest_tmp.process_exists(int(lock.read_text(encoding="ascii")))

    # Negative control: a newer retained session puts pytest-0 beyond the count, and
    # stock pytest still keeps it, honouring the dead process's lock for three days.
    monkeypatch.setenv("OUTCOME", "failed")
    stock = _session(suite, temproot, plugin=False)
    assert stock.returncode == 1, stock.stdout + stock.stderr
    assert _numbered(temproot) == ["pytest-0", "pytest-1"]

    monkeypatch.setenv("OUTCOME", "passed")
    reclaimed = _session(suite, temproot, plugin=True)
    assert reclaimed.returncode == 0, reclaimed.stdout + reclaimed.stderr
    assert _numbered(temproot) == ["pytest-1"]


def test_a_test_whose_tmp_path_outgrows_the_budget_errors_at_teardown(tmp_path: Path) -> None:
    suite = _write_suite(
        tmp_path / "suite",
        "import pytest\n"
        "@pytest.mark.parametrize('mib', [1, 3])\n"
        "def test_writes(tmp_path, mib):\n"
        "    (tmp_path / 'blob').write_bytes(bytes(mib << 20))\n",
        policy="failed",
        count=1,
        budget="2",
    )
    temproot = tmp_path / "temproot"
    temproot.mkdir()

    result = _session(suite, temproot, plugin=True, extra=("-rA",))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "PASSED test_suite.py::test_writes[1]" in result.stdout
    assert "ERROR test_suite.py::test_writes[3]" in result.stdout
    assert "tmp_path held 3.0 MiB in 1 files at teardown, over the 2.0 MiB" in result.stdout
    # The call passed, so failed-only retention still removed the oversized directory.
    assert not list(temproot.glob("pytest-of-*/pytest-*/test_writes_3_0"))


def _dead_pid() -> int:
    process = subprocess.Popen((sys.executable, "-c", "pass"))
    process.wait()
    return process.pid


def _locked(root: Path, name: str, content: str | None) -> Path:
    directory = root / name
    directory.mkdir(parents=True)
    if content is not None:
        (directory / ".lock").write_text(content, encoding="ascii")
    return directory


def test_only_locks_naming_an_exited_process_are_released(tmp_path: Path) -> None:
    dead = _dead_pid()
    live = subprocess.Popen((sys.executable, "-c", "import time; time.sleep(60)"))
    try:
        released = {
            _locked(tmp_path, "pytest-1", str(dead)),
            _locked(tmp_path, "garbage-1f2e", str(dead)),
        }
        kept = [
            _locked(tmp_path, "pytest-2", str(live.pid)),
            _locked(tmp_path, "pytest-3", str(os.getpid())),
            _locked(tmp_path, "pytest-4", ""),  # half-written by a starting session
            _locked(tmp_path, "pytest-5", "not a pid"),
            _locked(tmp_path, "unrelated-6", str(dead)),
        ]
        (tmp_path / "pytest-current").symlink_to(tmp_path / "pytest-1")

        assert set(pytest_tmp.release_dead_locks(tmp_path)) == released
    finally:
        live.kill()
        live.wait()
    assert all(not (directory / ".lock").exists() for directory in released)
    assert all((directory / ".lock").exists() for directory in kept)
    assert all(directory.is_dir() for directory in [*released, *kept])


def test_a_session_given_basetemp_leaves_the_shared_root_alone(tmp_path: Path) -> None:
    suite = _write_suite(tmp_path / "suite", "def test_ok(): pass\n", policy="failed", count=1)
    temproot = tmp_path / "temproot"
    stale = _locked(temproot / pytest_tmp.numbered_root().name, "pytest-0", str(_dead_pid()))

    given = _session(suite, temproot, plugin=True, extra=("--basetemp", str(tmp_path / "bt")))
    assert given.returncode == 0, given.stdout + given.stderr
    assert (stale / ".lock").exists()


_SCOPED = (
    "import pytest\n"
    "from devtools import pytest_tmp\n"
    "@pytest.fixture(scope='module')\n"
    "def site(request, tmp_path_factory):\n"
    "    with pytest_tmp.scoped_tmp_path(request, tmp_path_factory, '{name}') as root:\n"
    "        (root / 'page').write_bytes(bytes(1 << 20))\n"
    "        yield root\n"
    "def test_reads(site):\n"
    "    assert {outcome}\n"
)


@pytest.mark.parametrize("policy", ["failed", "all"])
def test_a_scoped_directory_goes_with_its_module_unless_a_test_failed(
    tmp_path: Path, policy: str
) -> None:
    suite = _write_suite(
        tmp_path / "suite",
        # pytest's own behaviour, for contrast: a module-scoped factory directory stays.
        "import pytest\n"
        "@pytest.fixture(scope='module')\n"
        "def site(tmp_path_factory):\n"
        "    return tmp_path_factory.mktemp('plain')\n"
        "def test_reads(site):\n"
        "    assert site.is_dir()\n",
        policy=policy,
        count=1,
    )
    (suite / "test_passing.py").write_text(
        _SCOPED.format(name="passing", outcome="site.is_dir()"), encoding="utf-8"
    )
    (suite / "test_failing.py").write_text(
        _SCOPED.format(name="failing", outcome="not site.is_dir()"), encoding="utf-8"
    )
    temproot = tmp_path / "temproot"
    temproot.mkdir()
    basetemp = tmp_path / "basetemp"

    result = _session(suite, temproot, plugin=True, extra=("--basetemp", str(basetemp)))
    assert result.returncode == 1, result.stdout + result.stderr
    kept = {entry.name for entry in basetemp.iterdir() if not entry.is_symlink()}
    expected = {"failing0", "plain0"} | ({"passing0"} if policy == "all" else set())
    assert kept == expected


def test_tmp_usage_reports_tests_session_directories_and_peak(tmp_path: Path) -> None:
    suite = _write_suite(
        tmp_path / "suite",
        "import pytest\n"
        "@pytest.fixture(scope='session')\n"
        "def shared(tmp_path_factory):\n"
        "    directory = tmp_path_factory.mktemp('shared-site')\n"
        "    (directory / 'page').write_bytes(bytes(3 << 20))\n"
        "    return directory\n"
        "def test_large(tmp_path, shared):\n"
        "    (tmp_path / 'blob').write_bytes(bytes(2 << 20))\n"
        "def test_small(tmp_path):\n"
        "    (tmp_path / 'note').write_text('x')\n"
        "def test_none():\n"
        "    pass\n",
        policy="failed",
        count=1,
    )
    temproot = tmp_path / "temproot"
    temproot.mkdir()
    report = tmp_path / "usage.jsonl"

    result = _session(
        suite,
        temproot,
        plugin=True,
        extra=("--tmp-usage", str(report), "--tmp-usage-interval", "0.05"),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    rows = pytest_tmp.read_report(report)
    tests = {
        str(row["nodeid"]).rsplit("::", 1)[1]: row for row in rows if row["event"] == "test"
    }
    assert set(tests) == {"test_large", "test_small"}
    assert int(tests["test_large"]["bytes"]) >= 2 << 20
    assert int(tests["test_small"]["files"]) == 1
    [residue] = [row for row in rows if row["event"] == "residue"]
    assert str(residue["name"]).startswith("shared-site")
    assert int(residue["bytes"]) >= 3 << 20
    [session] = [row for row in rows if row["event"] == "session"]
    assert int(session["samples"]) >= 2
    owners = dict(session["peak_owners"])
    assert any(
        name.startswith("shared-site") and size >= 3 << 20 for name, size in owners.items()
    )

    summary = pytest_tmp.summarize(rows, top=1)
    assert "test_suite.py::test_large" in summary
    assert "test_small" not in summary
    assert "shared-site" in summary


def test_tmp_usage_survives_tests_that_patch_what_it_measures_with(tmp_path: Path) -> None:
    # The measurement runs before a test's monkeypatches are undone, and beside the test
    # on its sampler thread. Tests here inject `os.write` failures and guard `os.scandir`.
    suite = _write_suite(
        tmp_path / "suite",
        "import os, time\n"
        "def test_patched(tmp_path, monkeypatch):\n"
        "    (tmp_path / 'blob').write_bytes(bytes(1 << 16))\n"
        "    def refuse(*args, **kwargs):\n"
        "        raise OSError('injected')\n"
        "    monkeypatch.setattr(os, 'write', refuse)\n"
        "    monkeypatch.setattr(os, 'scandir', refuse)\n"
        "    monkeypatch.setattr(time, 'monotonic', refuse)\n"
        "    time.sleep(0.3)\n",
        policy="failed",
        count=1,
    )
    temproot = tmp_path / "temproot"
    temproot.mkdir()
    report = tmp_path / "usage.jsonl"

    result = _session(
        suite,
        temproot,
        plugin=True,
        extra=("--tmp-usage", str(report), "--tmp-usage-interval", "0.05"),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    rows = pytest_tmp.read_report(report)
    [test] = [row for row in rows if row["event"] == "test"]
    assert int(test["bytes"]) >= 1 << 16
    [session] = [row for row in rows if row["event"] == "session"]
    assert int(session["samples"]) >= 3


def test_report_rows_from_another_tool_are_refused(tmp_path: Path) -> None:
    report = tmp_path / "usage.jsonl"
    report.write_text(json.dumps({"schema": "other", "event": "test"}) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="not a pytest-tmp-usage-v1 row"):
        pytest_tmp.read_report(report)
