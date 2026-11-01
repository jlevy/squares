"""The replay of Evan Daniel's gradec.py on the 233 grade-C configurations (think-mtah).

`devtools.evand_gradec_replay` runs the source's checker on every count the release's
grade-C archive certifies and compares each certificate it writes with the published one.
This holds its reading of the archive to the release's own figures (233 counts and the
38,026 s of build time its logs print), its schedule and log comparison to what they say,
and its judging to a stand-in checker: a certificate that matches passes, one that differs
fails and names the fields, and a control passes only when the checker refuses. The
project interpreter has no python-flint, so nothing here runs gradec.py itself; the
receipt of the run is checked by the tests below it once it is retained.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

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
print(base + ": 36 rows")
print("  => grade C certificate VALID: local minimum (3 s)")
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


def stub_release(published: bytes) -> replay.Release:
    log = "minpoly/solve/n-10: 36 rows\n  => grade C certificate VALID: local minimum (6 s)\n"
    return replay.Release({10: b"{}"}, {10: published}, {10: log})


def run_stub(tmp_path: Path, run: replay.Run, mode: str, out: bytes, published: bytes) -> dict:
    modules = tmp_path / "modules"
    modules.mkdir(exist_ok=True)
    (modules / "gradec.py").write_text(STUB)
    (modules / "mode.txt").write_text(mode)
    (modules / "out.json").write_bytes(out)
    return replay.execute(
        run,
        python=sys.executable,
        modules=modules,
        work=tmp_path / "work",
        release=stub_release(published),
        timeout=60,
    )


def test_a_matching_certificate_passes_and_a_differing_one_fails(tmp_path: Path) -> None:
    published = json.dumps({"n": 10, "dim_F": 2, "valid": True}).encode()
    record = run_stub(tmp_path, replay.Run(10), "valid", published, published)
    assert record["passed"]
    assert record["identical_to_published"]
    assert record["valid"]
    assert record["log_matches_release"] is True
    assert record["release_build_seconds"] == 6
    other = json.dumps({"n": 10, "dim_F": 3, "valid": True}).encode()
    record = run_stub(tmp_path, replay.Run(10), "valid", other, published)
    assert not record["passed"]
    assert record["differing_keys"] == ["dim_F"]


def test_a_control_passes_only_when_the_checker_refuses(tmp_path: Path) -> None:
    published = json.dumps({"n": 10, "valid": True}).encode()
    control = replay.Run(10, "tight")
    record = run_stub(tmp_path, control, "refuse", published, published)
    assert record["refused"]
    assert record["passed"]
    assert record["exit_code"] != 0
    assert record["last_lines"][-1].startswith("AssertionError")
    record = run_stub(tmp_path, control, "valid", published, published)
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


@pytest.mark.skipif(not RECEIPT.exists(), reason="the replay's receipt is not retained yet")
def test_the_retained_receipt_reproduces_every_certificate() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    summary = receipt["summary"]
    assert receipt["route"] == "same-implementation"
    assert receipt["complete"]
    assert summary["all_passed"]
    assert summary["replays_run"] == 233
    assert summary["identical_to_published"] == summary["valid"] == 233
    assert summary["controls_refused"] == summary["controls_run"] == 3
    assert summary["cpu_seconds_total"] < receipt["environment"]["cpu_cap_hours"] * 3600
    assert [r["n"] for r in receipt["replays"]] == replay.read_counts()
    for record in receipt["replays"]:
        assert record["env"] == ({"GRADEC_DROPZERO": "1"} if record["n"] in (230, 261) else {})
    assert receipt["environment"]["python-flint"] == "0.9.0"
