"""Issue432 source custody and complete native decisions on a small fixture."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from devtools import ryxu_arrangement_reports as reports


@pytest.fixture
def packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    monkeypatch.setattr(reports, "REPO", tmp_path)
    monkeypatch.setattr(reports, "PACKET", tmp_path / "packet")
    monkeypatch.setattr(reports, "NUMBERS", (3,))
    source = {
        "n": 3,
        "s_exact": "10",
        "s_decimal_ceiling": "0.1",
        "dilation_eps": "1/10^12",
        "angle_param": "t = tan(theta/2); cos = (1-t^2)/(1+t^2), sin = 2t/(1+t^2)",
        "squares": [{"x": str(i + 1), "y": "1", "t": "0"} for i in range(3)],
    }
    raw = json.dumps(source).encode()
    monkeypatch.setattr(reports, "SOURCE_SHA256", {3: hashlib.sha256(raw).hexdigest()})
    path = tmp_path / "upstream" / reports.source_path(3)
    path.parent.mkdir(parents=True)
    path.write_bytes(raw)
    reports.acquire(tmp_path / "upstream")
    fact = reports.read_fact(3)
    receipt = {
        "format": reports.RECEIPT_FORMAT,
        "routes": list(reports.ROUTES),
        "cases": [reports.run_case(fact, control) for control in reports.JOBS],
        "batch_wall_seconds": 0.1,
    }
    reports.save(reports.receipt_path(), receipt)
    return receipt


def test_exact_side_and_both_full_roster_controls(packet: dict[str, Any]) -> None:
    assert reports.confirmed_bound(3)["exact_form"] == "10"
    assert reports.check_certification(replay=True)
    for row in packet["cases"]:
        assert len(row["checker_input"]["poses"]) == 3
        for route in reports.ROUTES:
            assert row[route]["pairs_tested"] == 3
            assert row[route]["verification_passed"] is (row["control"] == "positive")


@pytest.mark.parametrize(
    "mutation", ["revision", "source", "last-pose", "missing-case", "path"]
)
def test_original_source_custody(packet: dict[str, Any], mutation: str) -> None:
    assert len(packet["cases"]) == 3
    record = reports.kernel.read_xz(reports.fact_path())
    if mutation in {"revision", "source"}:
        record[mutation] = "other"
    elif mutation == "missing-case":
        record["cases"].pop()
    elif mutation == "path":
        record["cases"][0]["source_path"] = "../other.json"
    else:
        source = json.loads(record["cases"][0]["source_certificate"])
        source["squares"][-1]["x"] = "9"
        record["cases"][0]["source_certificate"] = json.dumps(source)
    reports.save(reports.fact_path(), record)
    with pytest.raises(ValueError, match=r"namespace|roster|identity|acquired"):
        reports.read_facts()


@pytest.mark.parametrize(
    "mutation",
    ["missing-control", "extra-job", "namespace", "partial-pairs", "bool-wall", "native-field"],
)
def test_complete_native_receipt(packet: dict[str, Any], mutation: str) -> None:
    changed = copy.deepcopy(packet)
    if mutation == "missing-control":
        changed["cases"].pop()
    elif mutation == "extra-job":
        changed["cases"].append(changed["cases"][0])
    elif mutation == "namespace":
        changed["format"] = "other"
    elif mutation == "bool-wall":
        changed["batch_wall_seconds"] = True
    elif mutation == "partial-pairs":
        changed["cases"][0]["exact_verify"]["pairs_tested"] = 2
    else:
        changed["cases"][0]["exact_verify"].pop("verification_passed")
    reports.save(reports.receipt_path(), changed)
    with pytest.raises(ValueError, match=r"receipt|namespace|measurement|native|pairs|result"):
        reports.check_certification()


def test_duplicate_source_keys() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        reports.parse('{"n":51,"n":51}', 51)
