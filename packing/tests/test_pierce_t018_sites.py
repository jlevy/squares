"""CLI behaviour for the T-018 M3 piercing tool. No full 37-net IP."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

import devtools.pierce_t018_sites as pierce
from devtools.pierce_t018_sites import RECEIPT_NAME, check_sites, main
from sqpack.fractional.integral_piercing import (
    CoverEncoding,
    load_unique_sites,
    t018_certificate_path,
)


def test_check_reports_the_certificate_unique_site_count(
    capsys: pytest.CaptureFixture[str],
) -> None:
    sites = load_unique_sites()
    count, loaded = check_sites(t018_certificate_path())
    assert count == len(sites)
    assert loaded == sites
    assert main(["--check"]) == 0
    captured = capsys.readouterr()
    assert f"T-018 unique sites: {count}" in captured.out


def test_check_writes_nothing(tmp_path: Path) -> None:
    assert main(["--check", "--output-dir", str(tmp_path)]) == 0
    assert list(tmp_path.iterdir()) == []


def test_default_receipt_does_not_run_the_optimizer(tmp_path: Path) -> None:
    argv = ["--side", "19/5", "--direction-steps", "36", "--output-dir", str(tmp_path)]
    assert main(argv) == 0
    record = json.loads((tmp_path / RECEIPT_NAME).read_text(encoding="utf-8"))
    assert record["optimizer_ran"] is False
    assert record["piercing"] is None
    assert record["m3_verdict"] == "unresolved"
    assert record["search_status"] == "encoding_ready"
    assert record["float_lp_used"] is False
    assert record["using_unit_squares"] is True
    assert record["unique_sites"] == len(load_unique_sites())
    assert record["certificate"] == "packing/cases/n11_fractional_certificate/certificate.json"
    assert (t018_certificate_path()).is_file()


def test_search_on_a_one_site_synthetic(tmp_path: Path) -> None:
    certificate = tmp_path / "tiny.json"
    certificate.write_text(
        json.dumps({"atoms": [["1", "1", "1"]]}) + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "out"
    assert (
        main(
            [
                "--certificate",
                str(certificate),
                "--side",
                "2",
                "--direction-steps",
                "1",
                "--time-limit-s",
                "5",
                "--search",
                "--output-dir",
                str(output),
            ]
        )
        == 0
    )
    record = json.loads((output / RECEIPT_NAME).read_text(encoding="utf-8"))
    assert record["optimizer_ran"] is True
    assert record["search_status"] == "feasible"
    assert record["piercing"] == 1
    assert record["m3_verdict"] == "eleven_candidate"
    assert record["interval_audit"]["ran"] is False
    assert record["float_lp_used"] is False


def test_search_does_not_solve_when_encoding_consumed_the_wall(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    certificate = tmp_path / "tiny.json"
    certificate.write_text(
        json.dumps({"atoms": [["1", "1", "1"]]}) + "\n",
        encoding="utf-8",
    )
    encoding = CoverEncoding(
        rows=np.eye(1, dtype=np.uint8),
        reachable_cells=1,
        direction_count=1,
        site_count=1,
        truncated=False,
    )
    monkeypatch.setattr(pierce, "encode_event_cell_covers", lambda *_args, **_kwargs: encoding)
    clock = iter((100.0, 200.0))
    monkeypatch.setattr(pierce.time, "monotonic", lambda: next(clock))

    def fail_solve(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("milp must not run after the encoding wall")

    monkeypatch.setattr(pierce, "solve_integral_set_cover", fail_solve)
    output = tmp_path / "out"
    assert (
        main(
            [
                "--certificate",
                str(certificate),
                "--side",
                "2",
                "--direction-steps",
                "1",
                "--time-limit-s",
                "5",
                "--search",
                "--output-dir",
                str(output),
            ]
        )
        == 0
    )
    record = json.loads((output / RECEIPT_NAME).read_text(encoding="utf-8"))
    assert record["optimizer_ran"] is False
    assert record["search_status"] == "timeout"
    assert record["m3_verdict"] == "unresolved"
    assert record["cover_rows"] == 1
    assert record["reachable_cells"] == 1
