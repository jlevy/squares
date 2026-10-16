"""Tests for the replay receipt writer, the zmx2 replay driver and the dominance planner."""

from __future__ import annotations

import hashlib
import shlex
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import plan_replay_dominance, replay_evand_zmx2, replay_receipt


def test_receipt_records_header_output_and_footer(tmp_path: Path) -> None:
    receipt = tmp_path / "r.log"
    fields = replay_receipt.run(
        ["sh", "-c", "echo hello; echo oops >&2"],
        receipt=receipt,
        cwd_label="scratch",
        python_note="not used by this command",
        chdir=tmp_path,
    )
    lines = receipt.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "# command: sh -c 'echo hello; echo oops >&2'"
    assert lines[1] == "# cwd: scratch"
    assert lines[3].startswith("# host: ")
    assert "started" in lines[3]
    assert {"hello", "oops"} <= set(lines[4:6])
    assert lines[-1].startswith("# finished ")
    assert "; exit 0; wall " in lines[-1]
    assert fields["exit"] == 0


def test_receipt_keeps_a_failed_command_failed(tmp_path: Path) -> None:
    status = replay_receipt.main(
        ["--receipt", str(tmp_path / "r.log"), "--cwd-label", "x", "--", "sh", "-c", "exit 3"]
    )
    assert status == 3
    assert "; exit 3; " in (tmp_path / "r.log").read_text(encoding="utf-8")


def test_receipt_stops_a_run_at_its_time_limit(tmp_path: Path) -> None:
    fields = replay_receipt.run(
        ["sleep", "30"],
        receipt=tmp_path / "r.log",
        cwd_label="x",
        python_note="not used by this command",
        chdir=None,
        time_limit=0.5,
    )
    assert fields["exit"] == replay_receipt.TIME_LIMIT_EXIT
    text = (tmp_path / "r.log").read_text(encoding="utf-8")
    assert "# stopped at the time limit of 0.5 s" in text
    assert float(str(fields["wall_seconds"])) < 10


def test_driver_refuses_a_checker_whose_digest_differs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "zmx2.rs"
    source.write_text("fn main() {}\n", encoding="utf-8")
    monkeypatch.setitem(replay_evand_zmx2.CHECKERS, "bad", (source, "0" * 64))
    with pytest.raises(replay_evand_zmx2.DigestError, match=r"zmx2\.rs"):
        replay_evand_zmx2.build("bad", tmp_path / "work")
    assert not (tmp_path / "work/bad/verify2/src/bin/zmx2.rs").exists()


def test_driver_digests_match_the_retained_inputs() -> None:
    for relative, retained, expected in replay_evand_zmx2.CRATE_FILES:
        assert hashlib.sha256(retained.read_bytes()).hexdigest() == expected, relative
    for source, digest in replay_evand_zmx2.CHECKERS.values():
        assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
    for case in replay_evand_zmx2.CASES.values():
        assert case.cover.is_file(), case.cover
        assert case.checker in replay_evand_zmx2.CHECKERS


@pytest.mark.parametrize("n", [76, 95])
def test_a_split_cover_runs_with_its_source_uncert_cap_and_the_retained_name(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, n: int
) -> None:
    """``run`` passes the source's ``--uncert-cap``, so the roots left to zm_mixed.py are
    listed in full, under the name the packet's replay receipt has; ``control`` does not."""
    calls: list[tuple[list[str], Path]] = []

    def fake_run(argv: list[str], *, receipt: Path, **_: object) -> dict[str, object]:
        calls.append((list(argv), receipt))
        return {"exit": 0}

    binary = tmp_path / "6b7f0f79/verify2/target/release/zmx2"
    monkeypatch.setattr(replay_evand_zmx2, "build", lambda _checker, _work: binary)
    monkeypatch.setattr(replay_evand_zmx2.replay_receipt, "run", fake_run)
    out = tmp_path / "out"
    work = tmp_path / "work"
    assert (
        replay_evand_zmx2.run_case(n, "d4", work=work, out=out, threads=1, x=None, y=None) == 0
    )
    assert (
        replay_evand_zmx2.control_case(n, "drop-heaviest-point", work=work, out=out, threads=1)
        == 0
    )
    (run, receipt), (control, control_receipt) = calls
    assert receipt.name == f"n{n}_zmx2_d4.log"
    assert run[run.index("--uncert-cap") + 1] == "200000"
    assert run[run.index("--log") + 1] == str(out / f"n{n}_zmx2_d4_roots.log")
    assert "--uncert-cap" not in control
    region = replay_evand_zmx2.CONTROLS[(n, "drop-heaviest-point")]
    assert control_receipt.name == (
        f"n{n}_control_drop-heaviest-point_zmx2_d4_x{region.x}_y{region.y}.log"
    )
    # The packet's replay ran the same zmx2 command, by its own script, from scratch paths.
    retained = PACKETS[n] / "receipts" / receipt.name
    ran, built = _flags(_command(retained)), _flags(run)
    for host_choice in ("--threads", "--log"):  # the root log was renamed when retained
        assert ran.pop(host_choice)
        assert built.pop(host_choice)
    assert ran == built


#: The packet holding each split cover and its intake's replay receipts.
PACKETS = {
    76: replay_evand_zmx2.WEB / "bengreff-s76-certificate-2026-10-14",
    95: replay_evand_zmx2.WEB / "bengreff-s95-certificate-2026-10-15",
}


def _command(receipt: Path) -> list[str]:
    first = receipt.read_text(encoding="utf-8").splitlines()[0]
    return shlex.split(first.removeprefix("# command: "))


def _flags(argv: list[str]) -> dict[str, str]:
    """A command's program, subcommand, input and flags, each path by its file name."""
    named = {"argv0": Path(argv[0]).name, "what": argv[1], "input": Path(argv[2]).name}
    rest = argv[3:]
    for i, token in enumerate(rest):
        if token.startswith("--"):
            value = (
                rest[i + 1] if i + 1 < len(rest) and not rest[i + 1].startswith("--") else ""
            )
            named[token] = Path(value).name if value.startswith("/") else value
    return named


def _plain(argv: list[str]) -> list[str]:
    """Each absolute or staged path by its file name; flags and fractions as they are."""
    return [Path(t).name if t.startswith(("/", "stage/", "out/")) else t for t in argv]


@pytest.mark.parametrize("n", [76, 95])
def test_the_zm_mixed_runner_builds_the_command_every_retained_job_ran(n: int) -> None:
    jobs = replay_evand_zmx2.zm_mixed_jobs(n)
    receipts = PACKETS[n] / f"receipts/n{n}_zm_mixed"
    assert sorted(p.name for p in receipts.glob("j*.log")) == [f"j{job}.log" for job, _ in jobs]
    cover = replay_evand_zmx2.CASES[n].cover.name.removesuffix(".gz")
    for job, bounds in jobs:
        receipt = receipts / f"j{job}.log"
        built = replay_evand_zmx2.zm_mixed_command(
            "python3", Path("stage"), Path("stage") / cover, bounds, Path(f"out/j{job}.jsonl")
        )
        assert _plain(_command(receipt)) == _plain(built), receipt
        text = receipt.read_text(encoding="utf-8")
        assert "zm_mixed.py ee3e2915, mixed_cover.py bb89de15, zeromargin.py 640fe453" in text
        assert "\nVERIFIED-D4 (PARTIAL)\n" in text
        assert "; exit 0; " in text


def test_the_zm_mixed_runner_stages_the_pinned_files_and_names_each_job(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[list[str], Path]] = []

    def fake_run(argv: list[str], *, receipt: Path, **_: object) -> dict[str, object]:
        calls.append((list(argv), receipt))
        return {"exit": 0}

    monkeypatch.setattr(replay_evand_zmx2.replay_receipt, "run", fake_run)
    work, out = tmp_path / "work", tmp_path / "out"
    code = replay_evand_zmx2.zm_mixed_case(76, work=work, out=out, only=["000", "063"])
    assert code == 0
    assert [receipt.name for _, receipt in calls] == ["j000.log", "j063.log"]
    for name, _, digest in replay_evand_zmx2.ZM_MIXED_FILES:
        assert hashlib.sha256((work / "zm_mixed" / name).read_bytes()).hexdigest() == digest
    staged = work / "zm_mixed/s76_cover_v5.txt"
    assert hashlib.sha256(staged.read_bytes()).hexdigest() == replay_evand_zmx2.CASES[76].sha256
    argv, _ = calls[0]
    assert argv[argv.index("--resume") + 1] == str(out / "n76_zm_mixed/j000.jsonl")
    with pytest.raises(SystemExit):
        replay_evand_zmx2.zm_mixed_case(76, work=work, out=out, only=["999"])


def test_driver_region_must_lie_in_the_root_grid() -> None:
    span = replay_evand_zmx2.root_span
    assert span(None, 90) == (0, 89)
    assert span("45-89", 90) == (45, 89)
    for bad in ("0-90", "50-40"):
        with pytest.raises(SystemExit):
            span(bad, 90)


def test_planner_skips_only_dominated_certificates() -> None:
    queue = {60: Fraction(397, 50), 61: Fraction(199, 25), 67: Fraction(1691, 200)}
    verified = {60: Decimal("7.8"), 58: Decimal("7.79")}
    rows = {
        row["n"]: row
        for row in plan_replay_dominance.plan(
            queue, verified, {59: Fraction(8)}, include_queue=False
        )
    }
    assert rows[60]["action"] == "skip"
    assert rows[60]["rests_on_assumption"]
    assert rows[61]["action"] == "skip"
    assert rows[67]["action"] == "replay"
    assert not any(
        row["action"] == "skip"
        for row in plan_replay_dominance.plan(queue, verified, {}, include_queue=False)
    )


def test_planner_counts_the_queue_only_below_each_count() -> None:
    queue = {84: Fraction(47, 5), 86: Fraction(9), 87: Fraction(10)}
    rows = plan_replay_dominance.plan(queue, {}, {}, include_queue=True)
    actions = {row["n"]: row["action"] for row in rows}
    assert actions == {84: "replay", 86: "skip", 87: "replay"}
