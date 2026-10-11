"""Controls for the current-ledger partition and conservative receipt joins."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import pytest

from devtools import census_n17_certified as census
from devtools import select_n17_sub_patterns as selector
from devtools import stratify_n17_certified_residue as tool
from devtools.check_n17_capacity_one_cover import U


def small_cover() -> census.Cover:
    names = [f"side-{index}" for index in range(6)]
    square = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
    geometry = selector.make_geometry(
        [square + index for index in range(6)],
        names,
        group=[tuple(range(6)), tuple(reversed(range(6)))],
        actions=["r0", "f0"],
    )
    return census.Cover(geometry, 0b001101, selector.all_states(6, 3))


def receipt(cover: census.Cover, mask: int, **fields: object) -> dict[str, object]:
    return {
        "cells": [cover.geometry.names[index] for index in selector.cells_of(mask)],
        "frame": census.KERNEL_FRAME,
        "cap": str(U),
        "status": "PASS_CERTIFIED_STALL",
        "producer_outcome": "stalled",
        **fields,
    }


def write_receipt(path: Path, document: dict[str, object]) -> Path:
    _ = path.write_text(json.dumps(document), encoding="utf-8")
    return path


def test_admitted_population_and_strata_match_independent_orbit_enumeration() -> None:
    cover = small_cover()
    admitted = census.Entry("ban-pair", 0b11, "admitted", "kernel", {})
    pending = census.Entry("pending-endpoint", cover.endpoint_state, "pending", "kernel", {})
    record = tool.partition(cover, [admitted, pending])
    expected = [
        sum(1 << index for index in cells)
        for cells in itertools.combinations(range(6), 3)
        if not {0, 1} <= set(cells) and not {4, 5} <= set(cells)
    ]
    group = cover.geometry.group
    representatives = sorted({min(selector.orbit(mask, group)) for mask in expected})
    assert [row["mask"] for row in record["orbits"]] == representatives
    assert record["certified"] == {
        "admitted": 1,
        "surviving_states": len(expected),
        "orbits": len(representatives),
        "endpoint_survives": True,
    }
    assert sum(row["states"] for row in record["strata"].values()) == len(expected)
    assert (
        sorted(mask for row in record["strata"].values() for mask in row["masks"])
        == representatives
    )
    endpoint = min(selector.orbit(cover.endpoint_state, group))
    assert record["strata"]["endpoint"]["masks"] == [endpoint]
    with pytest.raises(census.RefusedError, match="excludes the endpoint"):
        tool.partition(
            cover, [census.Entry("bad", cover.endpoint_state, "admitted", "kernel", {})]
        )


def test_receipts_join_symmetry_images_and_keep_missing_identity_unknown(
    tmp_path: Path,
) -> None:
    cover = small_cover()
    record = tool.partition(cover, [])
    mask = next(row["mask"] for row in record["orbits"] if row["stratum"] != "endpoint")
    reflected = max(selector.orbit(mask, cover.geometry.group))
    paths = [
        write_receipt(tmp_path / "fixed.json", receipt(cover, reflected, producer_seconds=2.0)),
        write_receipt(
            tmp_path / "cap.json", receipt(cover, mask, producer_outcome="round_cap")
        ),
        write_receipt(tmp_path / "wrong-cap.json", receipt(cover, mask, cap="4")),
        write_receipt(tmp_path / "no-frame.json", receipt(cover, mask, frame=None)),
        write_receipt(tmp_path / "incomplete.json", {"status": "INCOMPLETE"}),
    ]
    tool.join_receipts(record, cover, [*paths, paths[0]])
    row = next(row for row in record["orbits"] if row["mask"] == mask)
    assert sorted(item["outcome"] for item in row["attempts"]) == ["fixed_point", "round_cap"]
    assert row["test_status"] == "tested_in_supplied_receipts"
    assert row["owner_diagnostics"] == "unavailable"
    assert len(row["unjoined_receipts"]) == 2
    assert len(record["unjoined_inputs"]) == 3
    assert any("different_cap" in item["reasons"] for item in record["unjoined_inputs"])
    assert all("reported_attempt" in item for item in record["unjoined_inputs"])
    assert all(
        row["test_status"] == "untested_in_supplied_receipts"
        for row in record["orbits"]
        if row["mask"] != mask
    )


def test_unadmitted_closure_does_not_remove_an_orbit_and_bad_timings_stay_missing(
    tmp_path: Path,
) -> None:
    cover = small_cover()
    record = tool.partition(cover, [])
    before = dict(record["certified"])
    mask = record["orbits"][0]["mask"]
    path = write_receipt(
        tmp_path / "closed.json",
        receipt(
            cover,
            mask,
            status="PASS_CERTIFIED_CLOSED",
            producer_seconds=-1,
            checker_seconds=True,
            process_cpu_seconds=float("nan"),
            final_extents=[{"cell": cover.geometry.names[0], "live_rows": 1}],
        ),
    )
    tool.join_receipts(record, cover, [path])
    assert record["certified"] == before
    row = record["orbits"][0]
    assert row["attempts"][0]["outcome"] == "closed_unadmitted"
    assert all(value is None for value in row["attempts"][0]["timings"].values())
    assert row["owner_diagnostics"] == "extents_available_support_unavailable"


def test_unbound_receipts_are_unknown_and_malformed_identity_cannot_join(
    tmp_path: Path,
) -> None:
    cover = small_cover()
    record = tool.partition(cover, [])
    mask = record["orbits"][0]["mask"]
    unknown = receipt(cover, mask)
    del unknown["frame"]
    del unknown["cap"]
    paths = [
        write_receipt(tmp_path / "unbound.json", unknown),
        write_receipt(
            tmp_path / "malformed.json", receipt(cover, mask, cells=[{}, "side-1", "side-2"])
        ),
    ]
    tool.join_receipts(record, cover, paths)
    assert record["orbits"][0]["test_status"] == "outcome_unavailable"
    assert record["orbits"][0]["attempts"] == []
    assert len(record["unjoined_inputs"]) == 2
    assert "invalid_cells" in record["unjoined_inputs"][0]["reasons"]
    assert tool.attempt({"status": []}, paths[0])["outcome"] == "outcome_unavailable"
    assert (
        tool.attempt({"status": "PASS_CERTIFIED_STALL", "producer_outcome": []}, paths[0])[
            "outcome"
        ]
        == "stall_reason_unavailable"
    )


def test_identified_receipt_without_outcome_does_not_claim_tested(tmp_path: Path) -> None:
    cover = small_cover()
    record = tool.partition(cover, [])
    mask = record["orbits"][0]["mask"]
    path = write_receipt(tmp_path / "unknown.json", receipt(cover, mask, status=None))
    tool.join_receipts(record, cover, [path])
    assert record["orbits"][0]["test_status"] == "outcome_unavailable"
    assert record["orbits"][0]["attempts"][0]["outcome"] == "outcome_unavailable"


def test_cli_validates_ledger_and_publishes_complete_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(census, "cover_context", small_cover)
    ledger = tmp_path / "ledger.yaml"
    document = {"schema": census.LEDGER_SCHEMA, "design": census.DESIGN, "entries": []}
    _ = ledger.write_text(json.dumps(document), encoding="utf-8")
    output = tmp_path / "report.json"
    arguments = ["--root", str(tmp_path), "--ledger", "ledger.yaml", "--output", str(output)]
    assert tool.main(arguments) == 0
    result = json.loads(output.read_text())
    assert result == json.loads(capsys.readouterr().out)
    assert result["certified"]["surviving_states"] == 20
    assert (
        sum(row["orbits"] for row in result["strata"].values()) == result["certified"]["orbits"]
    )
    _ = ledger.write_text("{}", encoding="utf-8")
    previous = output.read_bytes()
    assert tool.main(arguments) == 2
    assert "refused" in json.loads(capsys.readouterr().out)
    assert output.read_bytes() == previous
