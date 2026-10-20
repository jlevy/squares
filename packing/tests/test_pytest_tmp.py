"""pytest's temporary directories stay bounded: failed-only retention, killed sessions reaped.

Each nested session runs under its own `PYTEST_DEBUG_TEMPROOT`, so the numbered
directories it creates and prunes are this test's and never another session's.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import tomllib
from contextlib import suppress
from pathlib import Path

import pytest

from devtools import pytest_tmp

PACKING = Path(__file__).resolve().parents[1]
#: Killed sessions are released only where a PID scope can be read; a Linux host that
#: cannot read one fails these tests rather than skipping them.
LINUX = pytest.mark.skipif(
    not sys.platform.startswith("linux"), reason="PID scopes are read from Linux's /proc"
)


def _project_pytest_options() -> dict[str, object]:
    document = tomllib.loads((PACKING / "pyproject.toml").read_text(encoding="utf-8"))
    return document["tool"]["pytest"]["ini_options"]


def _write_suite(directory: Path, source: str, *, policy: str, count: int) -> Path:
    directory.mkdir()
    (directory / "pytest.ini").write_text(
        f"[pytest]\ntmp_path_retention_policy = {policy}\ntmp_path_retention_count = {count}\n",
        encoding="utf-8",
    )
    (directory / "test_suite.py").write_text(source, encoding="utf-8")
    return directory


def _session(
    suite: Path,
    temproot: Path,
    *,
    plugin: bool,
    extra: tuple[str, ...] = (),
    xdist: bool = False,
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
            *(() if xdist else ("-p", "no:xdist")),
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
    recorded = [pytest_tmp.OWNER_NAME] if pytest_tmp.pid_scope() else []
    assert kept == [*recorded, "test_maybe_True_0"]


@LINUX
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
    [directory] = temproot.glob("pytest-of-*/pytest-0")
    pid = int((directory / pytest_tmp.LOCK_NAME).read_text(encoding="ascii"))
    assert not pytest_tmp.process_exists(pid)
    assert _owner(directory) == pytest_tmp.owner_record(pid, _scope())

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


@LINUX
def test_a_session_killed_while_its_first_fixture_builds_is_already_recorded(
    tmp_path: Path,
) -> None:
    # The long module-scoped setups are where a command timeout lands; the record must
    # exist from the moment pytest makes the directory, not after the first report.
    suite = _write_suite(
        tmp_path / "suite",
        "import os, signal, pytest\n"
        "@pytest.fixture(scope='module')\n"
        "def snapshot(tmp_path_factory):\n"
        "    tmp_path_factory.mktemp('snapshot')\n"
        "    os.kill(os.getpid(), signal.SIGKILL)\n"
        "def test_reads(snapshot):\n"
        "    pass\n",
        policy="failed",
        count=1,
    )
    temproot = tmp_path / "temproot"
    temproot.mkdir()

    killed = _session(suite, temproot, plugin=True)
    assert killed.returncode == -9, killed.stdout + killed.stderr
    [directory] = temproot.glob("pytest-of-*/pytest-0")
    pid = int((directory / pytest_tmp.LOCK_NAME).read_text(encoding="ascii"))
    assert _owner(directory) == pytest_tmp.owner_record(pid, _scope())


@LINUX
def test_a_killed_xdist_controller_leaves_a_directory_the_next_session_can_release(
    tmp_path: Path,
) -> None:
    # The validation lanes run under xdist, so a deadline kills a controller. Its
    # numbered directory is made before any worker starts, and the record with it.
    suite = _write_suite(
        tmp_path / "suite",
        "import os, signal\n"
        "def test_kill_the_controller(tmp_path):\n"
        "    (tmp_path / 'blob').write_bytes(bytes(1 << 20))\n"
        "    os.kill(os.getppid(), signal.SIGKILL)\n",
        policy="failed",
        count=1,
    )
    temproot = tmp_path / "temproot"
    temproot.mkdir()

    killed = _session(suite, temproot, plugin=True, xdist=True, extra=("-n", "1"))
    assert killed.returncode == -9, killed.stdout + killed.stderr
    [directory] = temproot.glob("pytest-of-*/pytest-0")
    assert (directory / "popen-gw0").is_dir()
    pid = int((directory / pytest_tmp.LOCK_NAME).read_text(encoding="ascii"))
    assert _owner(directory) == pytest_tmp.owner_record(pid, _scope())
    assert pytest_tmp.release_dead_locks(directory.parent, _scope()) == [directory]


def _scope() -> str:
    scope = pytest_tmp.pid_scope()
    assert scope is not None
    return scope


def _other_boot() -> str:
    """This PID namespace on another kernel boot: another machine, or this one restarted."""
    here = _scope()
    boot = here.split()[2]
    return here.replace(boot, "0" * len(boot))


def _owner(directory: Path) -> object:
    return json.loads((directory / pytest_tmp.OWNER_NAME).read_text(encoding="ascii"))


def _dead_pid() -> int:
    process = subprocess.Popen((sys.executable, "-c", "pass"))
    process.wait()
    return process.pid


def _locked(
    root: Path, name: str, content: str | None, *, owner: dict[str, object] | None = None
) -> Path:
    directory = root / name
    directory.mkdir(parents=True)
    if content is not None:
        (directory / pytest_tmp.LOCK_NAME).write_text(content, encoding="ascii")
    if owner is not None:
        (directory / pytest_tmp.OWNER_NAME).write_text(json.dumps(owner), encoding="ascii")
    return directory


@LINUX
def test_only_locks_of_exited_owners_in_this_pid_scope_are_released(tmp_path: Path) -> None:
    here = _scope()
    dead = _dead_pid()
    live = subprocess.Popen((sys.executable, "-c", "import time; time.sleep(60)"))
    try:
        released = {
            _locked(tmp_path, "pytest-1", str(dead), owner=pytest_tmp.owner_record(dead, here)),
            # A deleter killed part-way: nothing live is inside, so no record is needed.
            _locked(tmp_path, "garbage-1f2e", str(dead)),
        }
        kept = [
            _locked(tmp_path, "pytest-2", str(live.pid)),
            _locked(tmp_path, "pytest-3", str(os.getpid())),
            _locked(tmp_path, "pytest-4", ""),  # half-written by a starting session
            _locked(tmp_path, "pytest-5", "not a pid"),
            _locked(tmp_path, "unrelated-6", str(dead)),
            # A session from before the plugin, or one that died before pytest made the
            # directory's record: its PID may mean a process in another namespace.
            _locked(tmp_path, "pytest-7", str(dead)),
            # A container sharing this temporary root, where the PID is another process.
            _locked(
                tmp_path,
                "pytest-8",
                str(dead),
                owner=pytest_tmp.owner_record(dead, here.rsplit(" ", 1)[0] + " pid:[1]"),
            ),
            # The same namespace inode on another kernel: the initial namespace has one
            # inode on every machine, so a shared directory needs the boot to tell them apart.
            _locked(
                tmp_path,
                "pytest-9",
                str(dead),
                owner=pytest_tmp.owner_record(dead, _other_boot()),
            ),
            # A record that does not describe this lock.
            _locked(
                tmp_path, "pytest-10", str(dead), owner=pytest_tmp.owner_record(dead + 1, here)
            ),
            _locked(tmp_path, "pytest-11", str(dead), owner={"pid": dead}),
            _locked(
                tmp_path,
                "pytest-12",
                str(live.pid),
                owner=pytest_tmp.owner_record(live.pid, here),
            ),
            # Digits that are no PID: past os.kill's range, and past int()'s digit limit.
            _locked(tmp_path, "pytest-13", "9" * 25, owner=pytest_tmp.owner_record(dead, here)),
            _locked(tmp_path, "garbage-25", "9" * 25),
            _locked(tmp_path, "garbage-5000", "9" * 5000),
        ]
        (tmp_path / "pytest-current").symlink_to(tmp_path / "pytest-1")

        assert set(pytest_tmp.release_dead_locks(tmp_path, here)) == released
        assert pytest_tmp.release_dead_locks(tmp_path, None) == []
    finally:
        live.kill()
        live.wait()
    assert all(not (directory / ".lock").exists() for directory in released)
    assert all((directory / ".lock").exists() for directory in kept)
    assert all(directory.is_dir() for directory in [*released, *kept])


@LINUX
def test_a_fifo_lock_or_record_is_kept_without_waiting_for_a_writer(tmp_path: Path) -> None:
    # Opening a FIFO for reading blocks until a writer appears; a session must not hang
    # in configure because one sits where a lock or a record should be.
    dead = _dead_pid()
    root = tmp_path / "root"
    root.mkdir(mode=0o700)
    fifos = [
        root / "garbage-fifo" / pytest_tmp.LOCK_NAME,
        root / "pytest-1" / pytest_tmp.LOCK_NAME,
        _locked(root, "pytest-2", str(dead)) / pytest_tmp.OWNER_NAME,
    ]
    for fifo in fifos:
        fifo.parent.mkdir(exist_ok=True)
        os.mkfifo(fifo)
    released: list[list[Path]] = []
    worker = threading.Thread(
        target=lambda: released.append(pytest_tmp.release_dead_locks(root, _scope())),
        daemon=True,
    )
    worker.start()
    worker.join(timeout=10)
    try:
        assert not worker.is_alive(), "release_dead_locks waited on a FIFO"
    finally:
        for fifo in fifos:  # a regression's blocked open returns once a writer opens
            with suppress(OSError):
                os.close(os.open(fifo, os.O_WRONLY | os.O_NONBLOCK))
    assert released == [[]]
    assert all(fifo.exists() for fifo in fifos)
    assert (root / "pytest-2" / pytest_tmp.LOCK_NAME).exists()


def test_an_out_of_range_pid_counts_as_alive() -> None:
    assert pytest_tmp.process_exists(10**25)


@LINUX
def test_without_a_pid_scope_only_garbage_is_released(tmp_path: Path) -> None:
    dead = _dead_pid()
    numbered = _locked(
        tmp_path, "pytest-1", str(dead), owner=pytest_tmp.owner_record(dead, _scope())
    )
    garbage = _locked(tmp_path, "garbage-1f2e", str(dead))
    assert pytest_tmp.release_dead_locks(tmp_path, None) == [garbage]
    assert (numbered / ".lock").exists()


@LINUX
def test_a_root_that_is_not_private_to_this_user_is_left_alone(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dead = _dead_pid()
    root = tmp_path / "root"
    stale = _locked(root, "pytest-1", str(dead), owner=pytest_tmp.owner_record(dead, _scope()))
    garbage = _locked(root, "garbage-1f2e", str(dead))
    root.chmod(0o700)
    (tmp_path / "link").symlink_to(root)

    assert pytest_tmp.release_dead_locks(tmp_path / "link", _scope()) == []
    root.chmod(0o755)
    assert pytest_tmp.release_dead_locks(root, _scope()) == []
    root.chmod(0o700)
    owner = root.stat().st_uid
    with monkeypatch.context() as patch:
        patch.setattr(os, "getuid", lambda: owner + 1)
        assert pytest_tmp.release_dead_locks(root, _scope()) == []
    assert (stale / ".lock").exists()
    assert (garbage / ".lock").exists()
    # Control: the same root, private again, is acted on.
    assert set(pytest_tmp.release_dead_locks(root, _scope())) == {stale, garbage}


@LINUX
def test_a_symlinked_entry_is_never_followed(tmp_path: Path) -> None:
    dead = _dead_pid()
    elsewhere = _locked(
        tmp_path / "elsewhere",
        "target",
        str(dead),
        owner=pytest_tmp.owner_record(dead, _scope()),
    )
    root = tmp_path / "root"
    root.mkdir(mode=0o700)
    (root / "pytest-1").symlink_to(elsewhere)
    (root / "garbage-1f2e").symlink_to(elsewhere)

    assert pytest_tmp.release_dead_locks(root, _scope()) == []
    assert (elsewhere / ".lock").exists()


@LINUX
@pytest.mark.parametrize("interleaving", ["number reused", "relocked in place"])
def test_a_lock_that_changes_after_the_checks_is_not_removed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, interleaving: str
) -> None:
    # Between reading a dead owner's lock and unlinking it, another session can delete
    # the directory and a new session can make one under the same number, or a deleter can
    # lock the same directory again. Neither new lock may go.
    dead = _dead_pid()
    root = tmp_path / "root"
    root.mkdir(mode=0o700)
    entry = _locked(root, "pytest-1", str(dead), owner=pytest_tmp.owner_record(dead, _scope()))
    live = str(os.getppid())

    def interleave(pid: int) -> bool:
        if interleaving == "number reused":
            entry.rename(root / "garbage-deleting")
            _locked(root, "pytest-1", live)
        else:
            (entry / ".lock").unlink()
            (entry / ".lock").write_text(live, encoding="ascii")
        return pid == int(live)

    monkeypatch.setattr(pytest_tmp, "process_exists", interleave)
    released = pytest_tmp.release_dead_locks(root, _scope())
    # A reused number is a new directory: the open one, now being deleted, is released.
    assert released == ([entry] if interleaving == "number reused" else [])
    assert not list(root.rglob(".lock-releasing-*"))
    assert (root / "pytest-1" / ".lock").read_text(encoding="ascii") == live


@LINUX
def test_a_session_given_basetemp_leaves_the_shared_root_alone(tmp_path: Path) -> None:
    suite = _write_suite(tmp_path / "suite", "def test_ok(): pass\n", policy="failed", count=1)
    temproot = tmp_path / "temproot"
    dead = _dead_pid()
    stale = _locked(
        temproot / pytest_tmp.numbered_root().name,
        "pytest-0",
        str(dead),
        owner=pytest_tmp.owner_record(dead, _scope()),
    )
    stale.parent.chmod(0o700)

    given = _session(suite, temproot, plugin=True, extra=("--basetemp", str(tmp_path / "bt")))
    assert given.returncode == 0, given.stdout + given.stderr
    assert (stale / ".lock").exists()
    assert not (tmp_path / "bt" / pytest_tmp.OWNER_NAME).exists()


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
