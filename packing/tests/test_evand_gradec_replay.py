"""The replay of Evan Daniel's gradec.py on the 233 grade-C configurations (think-mtah).

`devtools.evand_gradec_replay` runs the source's checker on every count the release's
grade-C archive certifies and compares each certificate it writes with the published one.
This holds its reading of the archive to the release's own figures (233 counts and the
38,026 s of build time its logs print), its schedule and log comparison to what they say,
and its judging to a stand-in checker: a certificate that matches passes, one that differs
fails and names the fields, and a control passes only when the checker refuses. It holds
the driver's guards too (review A of #868): running runs count toward the CPU cap, each
child is held to its CPU and wall limits, one invocation holds the work directory, the
ledger is held to one environment and adopts the 1 November run's records once, a torn
line is cut and a damaged one refused, and the receipt is replaced whole. The project
interpreter has no python-flint, so nothing here runs gradec.py itself; the receipt of the
run is checked by the tests below it once it is retained.
"""

from __future__ import annotations

import json
import resource
import sys
import threading
from pathlib import Path
from typing import Any

import pytest

from devtools import evand_gradec_replay as replay

RECEIPT = replay.DATA_PACKET / "receipts/gradec-replay-233.json"

STUB = """\
import pathlib, sys
here = pathlib.Path(__file__).parent
base = sys.argv[1]
assert pathlib.Path(base + ".contacts.json").is_file()
assert pathlib.Path(base + ".minpoly.json").is_file()
mode = (here / "mode.txt").read_text().strip()
if mode == "refuse":
    raise AssertionError("row not tight at the record")
print((here / "log.txt").read_text().replace("BASE", base), end="")
pathlib.Path(base + ".gradec.json").write_bytes((here / "out.json").read_bytes())
"""


@pytest.fixture(scope="module")
def release() -> replay.Release:
    return replay.read_release(replay.read_counts())


def test_the_archive_holds_the_233_counts_and_their_logs(release: replay.Release) -> None:
    counts = replay.read_counts()
    assert len(counts) == 233
    assert set(release.certificates) == set(release.contacts) == set(counts)
    seconds = [replay.release_seconds(release.logs[n]) for n in counts]
    assert None not in seconds
    # The release README's price of the replay: 38,026 s in all, at most 1,741 s (n = 313).
    assert sum(s or 0.0 for s in seconds) == 38_026
    assert max(s or 0.0 for s in seconds) == 1_741
    # The two zero-force counts are compared with the logs of their GRADEC_DROPZERO runs.
    for n in replay.DROPZERO:
        assert "dropped 24 zero-force rows" in release.logs[n]


def test_the_schedule_runs_the_controls_then_the_longest_first(
    release: replay.Release,
) -> None:
    runs = replay.schedule(replay.read_counts(), release)
    assert [run.control for run in runs[:3]] == list(replay.CONTROLS)
    assert all(run.n == replay.CONTROL_COUNT for run in runs[:3])
    assert [run.n for run in runs[3:5]] == [313, 276]
    assert len({run.key for run in runs}) == 236
    assert replay.Run(230).env == {"GRADEC_DROPZERO": "1"}
    assert replay.Run(10, "tight").env == {"GRADEC_MUTATE": "tight"}
    assert replay.Run(19).env == {}


def test_a_log_is_compared_without_its_path_or_timings(release: replay.Release) -> None:
    published = release.logs[10]
    ours = published.replace("minpoly/solve/n-10", "/scratch/runs/n-10/n-10")
    ours = ours.replace("(6 s)", "(1 s)").replace("(0.0 s)", "(0.3 s)")
    theirs = replay.normalized_log(published, "minpoly/solve/n-10", 10)
    assert replay.normalized_log(ours, "/scratch/runs/n-10/n-10", 10) == theirs
    assert theirs[0].startswith("n-10: 36 rows")
    changed = ours.replace("min 0.0625", "min 0.0626")
    assert replay.normalized_log(changed, "/scratch/runs/n-10/n-10", 10) != theirs


def run_stub(
    tmp_path: Path,
    run: replay.Run,
    mode: str,
    *,
    out: bytes,
    published: bytes,
    log: str,
) -> dict:
    """Run a stand-in gradec.py that prints the release's n = 10 log at its own path, with
    other build times, and writes ``out``; the release it is judged against publishes
    ``published`` with the release's own log."""
    modules = tmp_path / "modules"
    modules.mkdir(exist_ok=True)
    (modules / "gradec.py").write_text(STUB)
    (modules / "mode.txt").write_text(mode)
    (modules / "out.json").write_bytes(out)
    ours = log.replace("minpoly/solve/n-10", "BASE").replace("(0 s)", "(3 s)")
    (modules / "log.txt").write_text(ours)
    return replay.execute(
        run,
        python=sys.executable,
        modules=modules,
        work=tmp_path / "work",
        release=replay.Release({10: b"{}"}, {10: published}, {10: log}),
        timeout=60,
    )


def test_a_matching_certificate_passes_and_a_differing_one_fails(
    tmp_path: Path, release: replay.Release
) -> None:
    log = release.logs[10]
    published = json.dumps({"n": 10, "dim_F": 2, "valid": True}).encode()
    record = run_stub(
        tmp_path, replay.Run(10), "valid", out=published, published=published, log=log
    )
    assert record["passed"]
    assert record["identical_to_published"]
    assert record["valid"]
    assert record["log_matches_release"] is True
    assert record["release_build_seconds"] == 0
    other = json.dumps({"n": 10, "dim_F": 3, "valid": True}).encode()
    record = run_stub(
        tmp_path, replay.Run(10), "valid", out=other, published=published, log=log
    )
    assert not record["passed"]
    assert record["differing_keys"] == ["dim_F"]


def test_a_control_passes_only_when_the_checker_refuses(
    tmp_path: Path, release: replay.Release
) -> None:
    log = release.logs[10]
    published = json.dumps({"n": 10, "valid": True}).encode()
    control = replay.Run(10, "tight")
    record = run_stub(tmp_path, control, "refuse", out=published, published=published, log=log)
    assert record["refused"]
    assert record["passed"]
    assert record["exit_code"] != 0
    assert record["last_lines"][-1].startswith("AssertionError")
    record = run_stub(tmp_path, control, "valid", out=published, published=published, log=log)
    assert not record["passed"]


def test_the_receipt_writer_keeps_one_run_a_line(tmp_path: Path) -> None:
    runs = [replay.Run(10, "tight"), replay.Run(10)]
    records = {
        "control-tight-n-10": {
            "control": "tight",
            "n": 10,
            "passed": True,
            "cpu_seconds": 1,
            "started_utc": "2026-11-01T15:48:30+00:00",
        },
        "n-10": {
            "control": None,
            "n": 10,
            "passed": True,
            "cpu_seconds": 2,
            "valid": True,
            "identical_to_published": True,
            "log_matches_release": True,
            "release_build_seconds": 0.0,
            "started_utc": "2026-11-01T15:48:31+00:00",
        },
    }
    receipt = replay.summarize(runs, records, {"format": "evand-gradec-replay/1"})
    out = tmp_path / "receipt.json"
    replay.write_receipt(out, receipt)
    assert json.loads(out.read_text()) == json.loads(json.dumps(receipt))
    assert receipt["complete"]
    assert receipt["summary"]["all_passed"]
    assert len(out.read_text().splitlines()) < 30


# ----------------------------------------------------------- the driver's guards (#868)

#: One record of the ledger the 1 November 2026 run wrote before records carried their
#: environment, as it wrote it (``runs.jsonl``, its ``n-276`` line, last lines cut).
LEGACY_RECORD = (
    '{"key": "n-276", "n": 276, "control": null, "env": {}, "started_utc": '
    '"2026-11-01T15:48:31+00:00", "wall_seconds": 3380.0, "cpu_seconds": 1653.0, '
    '"max_rss_mb": 2501.5, "exit_code": 0, "timed_out": false, "last_lines": ["  => grade '
    'C certificate VALID: local minimum, strict modulo the 212-dim flat family (3379 s)"], '
    '"output_bytes": 32466, "valid": true, "identical_to_published": true, '
    '"log_matches_release": true, "release_build_seconds": 1633.0, "passed": true}'
)

IDENTITY = {
    "python": "3.13.18",
    "numpy": "2.4.2",
    "python-flint": "0.9.0",
    "platform": "Linux x86_64",
}


def fake_record(run: replay.Run, cpu: float, *, passed: bool = True) -> dict[str, Any]:
    return {
        "key": run.key,
        "n": run.n,
        "control": run.control,
        "cpu_seconds": cpu,
        "wall_seconds": cpu,
        "passed": passed,
        "started_utc": "2026-11-01T15:48:31+00:00",
    }


def drive(
    runs: list[replay.Run],
    *,
    cap: float,
    worst: float,
    cpu: float,
    records: dict[str, dict[str, Any]] | None = None,
    retry_failed: bool = False,
) -> tuple[list[str], list[dict[str, Any]], replay.Budget]:
    """Run ``runs`` through the driver's loop with a stand-in that records ``cpu`` each,
    checking at every start that the recorded CPU and the running runs' worst cases fit."""
    budget = replay.Budget(cap=cap, worst=worst)
    appended: list[dict[str, Any]] = []
    lock = threading.Lock()

    def start(run: replay.Run) -> dict[str, Any]:
        with budget.condition:
            assert budget.spent + budget.reserved <= budget.cap
        return fake_record(run, cpu)

    def append(record: dict[str, Any]) -> None:
        with lock:
            appended.append(record)

    not_started = replay.run_all(
        runs,
        {} if records is None else records,
        start=start,
        budget=budget,
        jobs=2,
        append=append,
        children=replay.Children(),
        retry_failed=retry_failed,
    )
    return not_started, appended, budget


def test_running_runs_count_toward_the_cpu_cap() -> None:
    """Finding 4 of review A: a run starts only if its worst case fits beside the worst
    case of every run still going, so the recorded CPU cannot pass the cap."""
    runs = [replay.Run(n) for n in (10, 19, 230, 313)]
    # Each run may take 10 s; with 15 s of cap only one may ever be going, and once it
    # has spent 8 s no other fits. The old start gate (finished CPU < cap) started two at
    # once and a third if one finished first, ending at 16 s or 24 s against the 15.
    not_started, appended, budget = drive(runs, cap=15, worst=10, cpu=8)
    assert len(appended) == 1
    assert sorted(not_started) == sorted(run.key for run in runs[1:])
    assert budget.spent == 8
    assert budget.reserved == 0
    not_started, appended, budget = drive(runs, cap=100, worst=10, cpu=8)
    assert not not_started
    assert len(appended) == 4
    assert budget.spent == 32


def test_a_stopping_driver_records_nothing_more() -> None:
    runs = [replay.Run(n) for n in (10, 19, 230)]
    children = replay.Children()
    appended: list[dict[str, Any]] = []

    def start(run: replay.Run) -> dict[str, Any]:
        children.kill_all()
        return fake_record(run, 1)

    replay.run_all(
        runs,
        {},
        start=start,
        budget=replay.Budget(cap=100, worst=10),
        jobs=1,
        append=appended.append,
        children=children,
    )
    assert appended == []


def test_a_retry_keeps_both_attempts_and_counts_their_cpu() -> None:
    run = replay.Run(19)
    failed = fake_record(run, 5, passed=False)
    _, appended, _ = drive([run], cap=100, worst=10, cpu=3, records={run.key: failed})
    assert appended == []
    retried = {run.key: failed}
    _, appended, _ = drive([run], cap=100, worst=10, cpu=3, records=retried, retry_failed=True)
    assert [record["passed"] for record in appended] == [True]
    assert retried[run.key]["passed"]
    receipt = replay.summarize([run], retried, {}, [failed, *appended])
    assert receipt["summary"]["superseded_attempts"] == 1
    assert receipt["summary"]["cpu_seconds_total"] == 8
    assert receipt["summary"]["all_passed"]


def busy_stub(tmp_path: Path, body: str, *, timeout: float, cpu_limit: float) -> dict:
    modules = tmp_path / "modules"
    modules.mkdir(exist_ok=True)
    (modules / "gradec.py").write_text(body)
    return replay.execute(
        replay.Run(10),
        python=sys.executable,
        modules=modules,
        work=tmp_path / "work",
        release=replay.Release({10: b"{}"}, {10: b"{}"}, {10: ""}),
        timeout=timeout,
        cpu_limit=cpu_limit,
    )


@pytest.mark.skipif(not hasattr(resource, "prlimit"), reason="no RLIMIT_CPU of a child here")
def test_a_child_is_held_to_its_cpu_limit(tmp_path: Path) -> None:
    record = busy_stub(tmp_path, "while True:\n    pass\n", timeout=60, cpu_limit=1)
    assert record["cpu_limit_seconds"] == 1
    assert record["cpu_limited"]
    assert not record["timed_out"]
    assert not record["passed"]
    assert record["cpu_seconds"] < 10


def test_a_child_is_killed_at_its_wall_limit(tmp_path: Path) -> None:
    record = busy_stub(tmp_path, "import time\ntime.sleep(60)\n", timeout=1, cpu_limit=60)
    assert record["timed_out"]
    assert not record["passed"]
    assert record["wall_seconds"] < 30


def test_each_attempt_has_a_directory_of_its_own(tmp_path: Path) -> None:
    work = tmp_path / "work"
    first = replay.attempt_directory(work, replay.Run(10))
    first.mkdir(parents=True)
    (first / "n-10.gradec.json").write_text("an orphan's output")
    second = replay.attempt_directory(work, replay.Run(10))
    assert second != first
    assert second.parent == first.parent
    assert not first.exists()


def test_one_invocation_holds_the_work_directory(tmp_path: Path) -> None:
    with (
        replay.locked(tmp_path),
        pytest.raises(SystemExit, match="in use"),
        replay.locked(tmp_path),
    ):
        pass
    with replay.locked(tmp_path):
        assert "pid" in (tmp_path / replay.LOCK).read_text()


def test_the_ledger_is_held_to_one_environment(tmp_path: Path) -> None:
    """Finding 5(a) of review A: a resumed invocation under another interpreter or other
    packages is refused before it runs, so one receipt never merges two environments."""
    header = replay.check_environment(tmp_path, IDENTITY, [], adopt_unstamped=False)
    assert header["interpreter"] == IDENTITY
    assert header["adopted_unstamped"] == []
    stamped = {"key": "n-19", "interpreter": dict(IDENTITY)}
    assert replay.check_environment(tmp_path, IDENTITY, [stamped], adopt_unstamped=False)
    other = {**IDENTITY, "numpy": "2.5.2"}
    with pytest.raises(SystemExit, match=r"numpy: 2\.4\.2 -> 2\.5\.2"):
        replay.check_environment(tmp_path, other, [stamped], adopt_unstamped=False)
    foreign = {"key": "n-19", "interpreter": other}
    with pytest.raises(SystemExit, match="another environment"):
        replay.check_environment(tmp_path, IDENTITY, [foreign], adopt_unstamped=False)


def test_the_live_ledgers_records_are_adopted_once(tmp_path: Path) -> None:
    """The 1 November run's ledger has records without an environment and no header: it
    is refused until ``--adopt-unstamped`` records this one for them, once."""
    ledger = tmp_path / replay.LEDGER
    ledger.write_text(LEGACY_RECORD + "\n")
    attempts = replay.load_attempts(ledger)
    assert [record["key"] for record in attempts] == ["n-276"]
    with pytest.raises(SystemExit, match="--adopt-unstamped"):
        replay.check_environment(tmp_path, IDENTITY, attempts, adopt_unstamped=False)
    header = replay.check_environment(tmp_path, IDENTITY, attempts, adopt_unstamped=True)
    assert header["adopted_unstamped"] == ["n-276"]
    assert "adopted_basis" in header
    assert json.loads((tmp_path / replay.ENVIRONMENT).read_text()) == header
    assert replay.check_environment(tmp_path, IDENTITY, attempts, adopt_unstamped=False)
    late = {**json.loads(LEGACY_RECORD), "key": "n-313"}
    with pytest.raises(SystemExit, match="older driver"):
        replay.check_environment(tmp_path, IDENTITY, [*attempts, late], adopt_unstamped=False)
    receipt = replay.summarize([replay.Run(276)], {"n-276": attempts[0]}, {}, attempts)
    assert receipt["complete"]
    assert receipt["summary"]["all_passed"]
    assert receipt["summary"]["cpu_seconds_total"] == 1653.0


def test_a_torn_last_line_is_cut_and_a_damaged_one_refused(tmp_path: Path) -> None:
    ledger = tmp_path / replay.LEDGER
    good = json.dumps(fake_record(replay.Run(19), 1))
    ledger.write_text(f"{LEGACY_RECORD}\n{good}\n" + good[:20])
    assert [record["key"] for record in replay.load_attempts(ledger)] == ["n-276", "n-19"]
    assert replay.repair_torn_tail(ledger)
    assert ledger.read_text() == f"{LEGACY_RECORD}\n{good}\n"
    assert not replay.repair_torn_tail(ledger)
    ledger.write_text(f"{LEGACY_RECORD}\n{good[:20]}\n{good}\n")
    with pytest.raises(SystemExit, match=":2: not a record"):
        replay.load_attempts(ledger)


def test_the_receipt_is_replaced_whole(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    out = tmp_path / "receipt.json"
    receipt = replay.summarize([], {}, {"format": replay.RECEIPT_FORMAT})
    replay.write_receipt(out, receipt)
    before = out.read_text()

    def torn(self: Path, data: str, *_args: object, **_kwargs: object) -> int:
        with self.open("w") as handle:
            handle.write(data[:10])
        raise OSError("disk full")

    monkeypatch.setattr(Path, "write_text", torn)
    with pytest.raises(OSError, match="disk full"):
        replay.write_receipt(out, {**receipt, "complete": False})
    monkeypatch.undo()
    assert out.read_text() == before


#: env.sh's pins (``pip install numpy==2.4.2 scipy==1.17.0 mpmath==1.3.0 sympy==1.14.0
#: python-flint==0.9.0`` into a Python 3.13 virtual environment).
ENV_SH_PINS = {
    "numpy": "2.4.2",
    "scipy": "1.17.0",
    "mpmath": "1.3.0",
    "sympy": "1.14.0",
    "python-flint": "0.9.0",
}


def test_env_sh_pins_what_the_receipt_is_held_to() -> None:
    text = (replay.SCRIPTS_DIR / "env.sh").read_text()
    assert " ".join(f"{name}=={version}" for name, version in ENV_SH_PINS.items()) in text
    assert "python313" in text


@pytest.mark.skipif(not RECEIPT.exists(), reason="the replay's receipt is not retained yet")
def test_the_retained_receipt_reproduces_every_certificate() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    summary = receipt["summary"]
    assert receipt["format"] == replay.RECEIPT_FORMAT
    assert receipt["route"] == "same-implementation"
    assert receipt["complete"]
    assert summary["all_passed"]
    assert summary["replays_run"] == 233
    assert summary["identical_to_published"] == summary["valid"] == 233
    assert summary["controls_refused"] == summary["controls_run"] == 3
    assert summary["cpu_seconds_total"] <= receipt["environment"]["cpu_cap_hours"] * 3600
    assert [r["n"] for r in receipt["replays"]] == replay.read_counts()
    for record in receipt["replays"]:
        assert record["env"] == ({"GRADEC_DROPZERO": "1"} if record["n"] in (230, 261) else {})
    environment = receipt["environment"]
    for name, version in ENV_SH_PINS.items():
        assert environment[name] == version
    assert environment["python"].startswith("3.13.")
    # An adopted environment is asserted, not stamped, and the receipt says on what basis.
    assert bool(environment["adopted_basis"]) == bool(environment["adopted_unstamped"])
    interpreter = {key: environment[key] for key in (*ENV_SH_PINS, "python", "platform")}
    for record in receipt["controls"] + receipt["replays"]:
        stamped = record.get("interpreter")
        assert stamped == interpreter or (
            stamped is None and record["key"] in environment["adopted_unstamped"]
        )
