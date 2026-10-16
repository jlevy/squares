"""Folding batch replay receipts of Hosono's rectangle certificates into one packet receipt.

The batches are cut from the September 27 packet's own replay receipt, so every case is a
real 201-angle replay of a retained certificate; each test then alters one thing.
"""

from __future__ import annotations

import dataclasses
import gzip
import json
import shutil
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_wand125_rectangles as audit
from devtools.audit_wand125_rectangles import (
    HOST_FIELDS,
    KIND,
    PACKETS,
    SCOPE,
    SEPTEMBER_27,
    SEPTEMBER_28,
    Packet,
    check_receipt,
    matches_upstream,
    merge,
    store_receipt,
)
from devtools.retained_data import (
    LINE_THRESHOLD,
    compress,
    compressed_path,
    describe,
    is_deterministic_gzip,
    read_retained_bytes,
    read_retained_text,
)

#: The three replays the September 27 receipt held before any batch was merged.
FIRST, REST = (27,), (31, 32)


def _batch(root: Path, counts: Iterable[int], packet: Packet = SEPTEMBER_27) -> Path:
    """A receipt as one ``--replay`` run on another host writes it, holding ``counts``."""
    replays = packet.directory / "receipts/replay"
    record = json.loads(read_retained_text(replays / "audit.json"))
    cases = [case for case in record["cases"] if case["n"] in counts]
    host = cases[0]["replay"].get("host") or {key: record[key] for key in HOST_FIELDS}
    root.mkdir(parents=True)
    batch = {
        "kind": KIND,
        "source_revision": packet.revision,
        "source": f"/elsewhere/{packet.source.relative_to(packet.root)}",
        "python": host["python"],
        "scope": SCOPE,
        "cases": [
            case | {"replay": {k: v for k, v in case["replay"].items() if k != "host"}}
            for case in cases
        ],
        "provenance": record["provenance"],
        "platform": host["platform"],
        "compiler": host["compiler"],
        "status": "PASS",
    }
    (root / "audit.json").write_text(json.dumps(batch, indent=2) + "\n")
    for case in cases:
        shutil.copytree(replays / case["certificate"], root / case["certificate"])
    return root


def _snapshot(directory: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(directory)): path.read_bytes()
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


def _edit(batch: Path, change: Callable[[dict[str, Any]], None]) -> None:
    record = json.loads((batch / "audit.json").read_text())
    change(record)
    (batch / "audit.json").write_text(json.dumps(record, indent=2) + "\n")


def _rows(batch: Path, name: str) -> tuple[Path, list[dict[str, Any]]]:
    path = batch / name / "verified_angles.jsonl"
    return path, [json.loads(line) for line in path.read_text().splitlines()]


def _write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))


def test_batches_fold_in_count_order_and_a_rerun_writes_the_same_bytes(tmp_path: Path) -> None:
    first = _batch(tmp_path / "a", FIRST)
    rest = _batch(tmp_path / "b", REST)
    out = tmp_path / "out"
    result = merge(SEPTEMBER_27, out, [rest, first])
    assert [item["n"] for item in result["added"]] == [*FIRST, *REST]
    assert all(item["matches_upstream_angles"] for item in result["added"])
    record = json.loads((out / "audit.json").read_text())
    assert [case["n"] for case in record["cases"]] == [*FIRST, *REST]
    assert record["status"] == "PASS"
    assert record["source"] == str(SEPTEMBER_27.source.relative_to(SEPTEMBER_27.root))
    # Each case names its own host; the receipt as a whole names none.
    assert not set(HOST_FIELDS) & set(record)
    assert all(set(case["replay"]["host"]) == set(HOST_FIELDS) for case in record["cases"])
    assert set(check_receipt(SEPTEMBER_27, out)) == {*FIRST, *REST}
    snapshot = _snapshot(out)
    again = merge(SEPTEMBER_27, out, [first, rest, out])
    assert (again["added"], again["held"]) == ([], [*FIRST, *REST])
    assert _snapshot(out) == snapshot
    # One batch at a time, in the other order, ends in the same bytes.
    other = tmp_path / "other"
    merge(SEPTEMBER_27, other, [rest])
    merge(SEPTEMBER_27, other, [first])
    assert _snapshot(other) == snapshot


def test_a_dry_run_writes_nothing(tmp_path: Path) -> None:
    result = merge(SEPTEMBER_27, tmp_path / "out", [_batch(tmp_path / "a", FIRST)], write=False)
    assert [item["n"] for item in result["added"]] == list(FIRST)
    assert not (tmp_path / "out").exists()


def test_a_receipt_of_another_revision_is_refused(tmp_path: Path) -> None:
    batch = _batch(tmp_path / "a", FIRST)
    with pytest.raises(ValueError, match=r"the 2026-09-27 packet.*not of the 2026-09-28"):
        merge(SEPTEMBER_28, tmp_path / "out", [batch])
    _edit(batch, lambda record: record.update(source_revision=SEPTEMBER_28.revision))
    with pytest.raises(ValueError, match="not of the 2026-09-27 packet"):
        merge(SEPTEMBER_27, tmp_path / "out", [batch])
    assert not (tmp_path / "out").exists()


def _drop_stdout(batch: Path, name: str) -> None:
    (batch / name / "stdout.log").unlink()


def _alter_summary(batch: Path, name: str) -> None:
    path = batch / name / "verification_summary.json"
    path.write_text(path.read_text().replace('"nodes": ', '"nodes": 1', 1))


def _truncate_stdout(batch: Path, name: str) -> None:
    path = batch / name / "stdout.log"
    path.write_text(path.read_text().removesuffix("}\n") + "\n")


def _change_a_row(batch: Path, name: str) -> None:
    path, rows = _rows(batch, name)
    rows[0]["nodes"] += 1
    _write_rows(path, rows)


def _rebind_the_input(batch: Path, _name: str) -> None:
    _edit(batch, lambda record: record["cases"][0].update(input_sha256="0" * 64))


@pytest.mark.parametrize(
    ("alter", "message"),
    [
        (_drop_stdout, "missing stdout.log"),
        (_alter_summary, "verification_summary.json differs from the receipt"),
        (_truncate_stdout, "stdout.log does not end with the run's summary"),
        (_change_a_row, "not the summary's accepted angles"),
        (_rebind_the_input, "differs from the packet's own preflight"),
    ],
    ids=lambda value: value.__name__[1:] if callable(value) else None,
)
def test_a_missing_or_altered_file_refuses_the_receipt_and_writes_nothing(
    alter: Callable[[Path, str], None], message: str, tmp_path: Path
) -> None:
    out = tmp_path / "out"
    merge(SEPTEMBER_27, out, [_batch(tmp_path / "held", REST)])
    before = _snapshot(out)
    batch = _batch(tmp_path / "a", FIRST)
    alter(batch, SEPTEMBER_27.cases[FIRST[0]][0])
    with pytest.raises(ValueError, match=message):
        merge(SEPTEMBER_27, out, [batch])
    assert _snapshot(out) == before


def test_a_duplicate_that_disagrees_is_refused_and_one_that_agrees_is_kept_once(
    tmp_path: Path,
) -> None:
    name = SEPTEMBER_27.cases[FIRST[0]][0]
    held = _batch(tmp_path / "held", FIRST)
    # The same results at other timings agree, whichever receipt comes first.
    slower = _batch(tmp_path / "slower", FIRST)
    path, rows = _rows(slower, name)
    rows[0]["seconds"] *= 2
    _write_rows(path, rows)
    _edit(
        slower,
        lambda record: record["cases"][0]["replay"].update(
            elapsed_seconds_including_compile=1.0
        ),
    )
    one, two = tmp_path / "one", tmp_path / "two"
    assert len(merge(SEPTEMBER_27, one, [held, slower])["agreeing_duplicates"]) == 1
    merge(SEPTEMBER_27, two, [slower, held])
    assert _snapshot(one) == _snapshot(two)
    # A replay whose own record is consistent but whose angle results differ does not.
    other = _batch(tmp_path / "other", FIRST)
    path, rows = _rows(other, name)
    least = min(row["lower_bound"] for row in rows)
    row = next(row for row in rows if row["lower_bound"] > least)
    row["lower_bound"] += 1e-9
    _write_rows(path, rows)
    assert set(check_receipt(SEPTEMBER_27, other)) == set(FIRST)
    before = _snapshot(one)
    with pytest.raises(ValueError, match=rf"n = {FIRST[0]}: .* disagrees"):
        merge(SEPTEMBER_27, one, [other])
    assert _snapshot(one) == before


def _fail(record: dict[str, Any]) -> None:
    record.update(status="FAIL", error="upstream replay exited 1")


def _preflight_only(record: dict[str, Any]) -> None:
    del record["cases"][0]["replay"]


def _fewer_angles(record: dict[str, Any]) -> None:
    record["cases"][0]["replay"]["summary"]["angle_cases"] = 200


@pytest.mark.parametrize(
    ("alter", "message"),
    [
        (_fail, "status 'FAIL': upstream replay exited 1"),
        (_preflight_only, "is not a passed replay of all 201 angles"),
        (_fewer_angles, "is not a passed replay of all 201 angles"),
    ],
    ids=lambda value: value.__name__[1:] if callable(value) else None,
)
def test_a_failed_or_partial_receipt_is_refused(
    alter: Callable[[dict[str, Any]], None], message: str, tmp_path: Path
) -> None:
    batch = _batch(tmp_path / "a", FIRST)
    _edit(batch, alter)
    with pytest.raises(ValueError, match=message):
        merge(SEPTEMBER_27, tmp_path / "out", [batch])
    assert not (tmp_path / "out").exists()


def test_a_receipt_missing_an_angle_is_refused(tmp_path: Path) -> None:
    batch = _batch(tmp_path / "a", FIRST)
    path, rows = _rows(batch, SEPTEMBER_27.cases[FIRST[0]][0])
    _write_rows(path, rows[1:])
    with pytest.raises(ValueError, match="not the summary's accepted angles"):
        merge(SEPTEMBER_27, tmp_path / "out", [batch])


def test_an_interrupted_run_contributes_the_cases_it_finished(tmp_path: Path) -> None:
    """A run records its status only at the end, and lists a case only once it passed."""
    batch = _batch(tmp_path / "a", REST)
    _edit(batch, lambda record: record.pop("status"))
    assert [item["n"] for item in merge(SEPTEMBER_27, tmp_path / "out", [batch])["added"]] == [
        *REST
    ]


def test_compressed_inputs_are_read_and_large_receipts_are_stored_compressed(
    tmp_path: Path,
) -> None:
    batch = _batch(tmp_path / "a", FIRST)
    name = SEPTEMBER_27.cases[FIRST[0]][0]
    for path in (batch / "audit.json", batch / name / "verified_angles.jsonl"):
        compress(path)
    out = tmp_path / "out"
    merge(SEPTEMBER_27, out, [batch])
    assert (out / name / "verified_angles.jsonl").is_file()
    assert not compressed_path(out / "audit.json").exists()
    data = b"{}\n" * (LINE_THRESHOLD + 1)
    stored = store_receipt(tmp_path / "big.json", data)
    assert stored is not None
    assert stored == compressed_path(tmp_path / "big.json")
    assert not (tmp_path / "big.json").exists()
    assert is_deterministic_gzip(stored.read_bytes())
    assert gzip.decompress(stored.read_bytes()) == read_retained_bytes(tmp_path / "big.json")
    assert store_receipt(tmp_path / "big.json", b"{}\n") is None
    assert not stored.exists()


def test_a_receipt_past_the_threshold_is_stored_compressed_with_its_table_row(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The packet copied to scratch, with the threshold lowered so three cases cross it."""
    packet = dataclasses.replace(SEPTEMBER_27, root=tmp_path / "repo")
    shutil.copytree(SEPTEMBER_27.directory, packet.directory)
    shutil.rmtree(packet.directory / "receipts/replay")
    monkeypatch.setattr(audit, "LINE_THRESHOLD", 100)
    out = packet.directory / "receipts/replay"
    result = merge(packet, out, [_batch(tmp_path / "a", (*FIRST, *REST))])
    stored = compressed_path(out / "audit.json")
    assert stored.is_file()
    assert not (out / "audit.json").exists()
    assert is_deterministic_gzip(stored.read_bytes())
    # Each case's 201 per-angle rows cross the lowered threshold as well.
    angles = [
        compressed_path(out / SEPTEMBER_27.cases[n][0] / "verified_angles.jsonl")
        for n in (*FIRST, *REST)
    ]
    assert result["compressed_rows"] == [
        describe(packet.directory, path, "receipt").markdown() for path in [*angles, stored]
    ]
    assert result["compressed_rows"][-1].startswith("| `receipts/replay/audit.json.gz` |")
    assert set(check_receipt(packet, out)) == {*FIRST, *REST}
    snapshot = _snapshot(out)
    merge(packet, out, [out])
    assert _snapshot(out) == snapshot


@pytest.mark.parametrize(
    "date",
    [
        date
        for date, packet in PACKETS.items()
        if (packet.directory / "receipts/replay").is_dir()
    ],
)
def test_every_retained_replay_receipt_passes_the_merge_checks(date: str) -> None:
    """Each case reproduces the upstream accepting run's results, angle by angle."""
    packet = PACKETS[date]
    receipt = packet.directory / "receipts/replay"
    cases = check_receipt(packet, receipt)
    assert cases
    assert all(matches_upstream(packet, item) for item in cases.values())
    result = merge(packet, receipt, [receipt], write=False)
    assert result["added"] == []
    assert result["held"] == sorted(cases)
