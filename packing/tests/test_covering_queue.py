"""The sequential covering-queue walker skips finished probes and halts on mass < n."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from devtools.run_covering_queue import (
    EXIT_DONE,
    EXIT_FREEZE_BELOW,
    EXIT_STOP,
    Probe,
    colgen_command,
    freeze_mass_below_n,
    load_queue,
    parse_stop_at,
    remain_seconds,
    walk_queue,
)

QUEUE = """
probes:
  - id: n12-done
    n: 12
    side: '397/100'
    grid_counts: '28,38,46,54'
    seed_certificate: cases/n12_fractional_certificate/certificate.json
    seed_windows: 7
    deadline_seconds: 1200
    bead: think-h02v
  - id: n17-open
    n: 17
    side: '23/5'
    grid_counts: '34,45,56,64'
    seed_certificate: cases/n17_fractional_certificate/certificate.json
    seed_windows: 8
    deadline_seconds: 1200
"""


def test_load_queue_reads_named_fields(tmp_path: Path) -> None:
    path = tmp_path / "queue.yaml"
    path.write_text(QUEUE, encoding="utf-8")
    probes = load_queue(path)
    assert [probe.id for probe in probes] == ["n12-done", "n17-open"]
    assert probes[0].n == 12
    assert probes[0].grid_counts == "28,38,46,54"
    assert probes[1].seed_windows == 8
    assert probes[0].seed_certificate is not None


def test_freeze_mass_compare(tmp_path: Path) -> None:
    below = tmp_path / "below.json"
    below.write_text(json.dumps({"total_mass": "48534459/4000000"}), encoding="utf-8")
    assert freeze_mass_below_n(13, below)
    assert not freeze_mass_below_n(12, below)
    missing = tmp_path / "none.json"
    missing.write_text(json.dumps({"objective": 12.1}), encoding="utf-8")
    assert not freeze_mass_below_n(12, missing)


def test_walk_skips_existing_run_json(tmp_path: Path) -> None:
    started: list[str] = []
    (tmp_path / "n12-done-run.json").write_text("{}", encoding="utf-8")
    probes = [
        Probe("n12-done", 12, "397/100", "28,38,46,54", "cert.json", 7, 1200),
        Probe("n17-open", 17, "23/5", "34,45,56,64", "cert.json", 8, 1200),
    ]

    def fake(probe: Probe, prefix: Path) -> int:
        started.append(probe.id)
        Path(f"{prefix}-run.json").write_text("{}", encoding="utf-8")
        return 0

    rc = walk_queue(
        probes,
        tmp_path,
        parse_stop_at("2099-01-01T00:00:00Z"),
        tmp_path / "waiter.log",
        runner=fake,
    )
    assert rc == EXIT_DONE
    assert started == ["n17-open"]


def test_walk_halts_when_freeze_mass_is_below_n(tmp_path: Path) -> None:
    probe = Probe("n18-hit", 18, "467/100", "auto", "cert.json", 5, 1200)

    def fake(_probe: Probe, prefix: Path) -> int:
        Path(f"{prefix}-run.json").write_text(
            json.dumps({"total_mass": "17/1"}), encoding="utf-8"
        )
        Path(f"{prefix}-certificate.json").write_text("{}", encoding="utf-8")
        return 0

    rc = walk_queue(
        [probe],
        tmp_path,
        parse_stop_at("2099-01-01T00:00:00Z"),
        tmp_path / "waiter.log",
        runner=fake,
    )
    assert rc == EXIT_FREEZE_BELOW


def test_walk_stops_when_the_budget_is_gone(tmp_path: Path) -> None:
    probe = Probe("n19-late", 19, "481/100", "34,45,56", "cert.json", 6, 1200)
    rc = walk_queue(
        [probe],
        tmp_path,
        datetime(2020, 1, 1, tzinfo=UTC),
        tmp_path / "waiter.log",
        runner=lambda _probe, _prefix: 0,
    )
    assert rc == EXIT_STOP


def test_remain_and_command_use_the_project_interpreter() -> None:
    stop = parse_stop_at("2099-01-01T00:00:00Z")
    assert remain_seconds(stop, now=datetime(2098, 12, 31, 23, 59, 0, tzinfo=UTC)) == 60
    probe = Probe("n20", 20, "973/200", "34,46,56,64", "cases/n20.json", 7, 1200)
    command = colgen_command(probe, Path("/tmp/n20"))
    assert command[1:3] == ["-m", "devtools.run_fractional_colgen"]
    assert "--n" in command
    assert "20" in command
    assert "python3" not in Path(command[0]).name
    assert "--seed-certificate" in command


def test_session_140_queue_files_parse() -> None:
    """The live leftover and second-wave lists must stay walker-readable."""

    agenda = (
        Path(__file__).resolve().parent.parent
        / "campaign/series/series-000-smoke-and-calibration/results/agenda-038"
    )
    leftover = load_queue(agenda / "leftover-queue.yaml")
    second = load_queue(agenda / "second-wave-queue.yaml")
    assert leftover[0].n == 19
    assert leftover[0].side == "241/50"
    assert leftover[1].n == 17
    assert leftover[1].side == "461/100"
    assert leftover[2].n == 20
    assert leftover[2].side == "971/200"
    assert leftover[3].n == 12
    assert leftover[4].n == 18
    assert leftover[4].side == "1871/400"
    assert second[0].seed_certificate is None
    assert second[0].n == 32


def test_omitted_seed_certificate_drops_the_seed_flags(tmp_path: Path) -> None:
    path = tmp_path / "queue.yaml"
    path.write_text(
        """
probes:
  - id: n32-auto
    n: 32
    side: '29/5'
    grid_counts: auto
    seed_windows: 5
    deadline_seconds: 1200
""",
        encoding="utf-8",
    )
    probe = load_queue(path)[0]
    assert probe.seed_certificate is None
    command = colgen_command(probe, tmp_path / "n32-auto")
    assert "--seed-certificate" not in command
    assert "--seed-map" not in command
    assert command[command.index("--seed-windows") + 1] == "5"
