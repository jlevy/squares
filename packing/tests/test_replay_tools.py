"""Tests for the replay receipt writer, the zmx2 replay driver and the dominance planner."""

from __future__ import annotations

import hashlib
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
