"""The n90 attachment reader binds original data and complete native jobs."""

from __future__ import annotations

import gzip
import json
import lzma
import shutil
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import upper_bound_houses as houses
from devtools import upper_bound_reports as reports

KEY = "[de Winter issue 997 follow-up 2026-11-21]"


def source() -> houses.Source:
    return houses.de_winter_997_followup_source("T-900")


def test_original_geometry_and_native_jobs() -> None:
    incoming = source()
    original = json.loads(gzip.decompress(incoming.stored(90).read_bytes()))
    exact = incoming.certificate(90)
    assert exact.n == 90
    assert exact.side == Fraction(original["side"])
    assert set(incoming.jobs(90, exact)) == set(houses.kernel.JOBS)
    origin = incoming.origin(90)
    assert origin.key == KEY
    assert origin.author == "jazivxt, improved and refined by Joost de Winter"
    assert origin.raw_asset_retained
    assert origin.licence_status == houses.NO_LICENCE
    assert origin.url.endswith("n90-rational.zip#90/candidate.json.gz")
    assert incoming.inputs([90]) == (
        incoming.packet / "acquisition/sources.json",
        incoming.stored(90),
        incoming.receipt(90),
    )
    reading = reports.parse_certificate(
        (incoming.packet / "derived/candidate-reading-copy.json").read_bytes(),
        90,
        "pingyou-json",
    )
    assert exact == reading


@pytest.mark.parametrize("n", [89, 91, True])
def test_other_counts_are_refused(n: int) -> None:
    incoming = source()
    for action in (incoming.certificate, incoming.origin, incoming.stored, incoming.receipt):
        with pytest.raises(houses.HouseError, match="houses only 90"):
            action(n)
    with pytest.raises(houses.HouseError, match="houses only 90"):
        incoming.inputs([n])


def private_copy(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> houses.Source:
    incoming = source()
    packet = tmp_path / "packing/resources/web" / incoming.packet.name
    for path in incoming.inputs([90]):
        target = packet / path.relative_to(incoming.packet)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    monkeypatch.setattr(reports, "REPO", tmp_path)
    monkeypatch.setattr(reports, "WEB", packet.parent)
    return source()


def test_altered_candidate_is_refused(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    incoming = private_copy(tmp_path, monkeypatch)
    original = incoming.stored(90).read_bytes()
    incoming.stored(90).write_bytes(bytes([original[0] ^ 1]) + original[1:])
    with pytest.raises(houses.HouseError, match="differs from its pinned bytes"):
        incoming.certificate(90)


@pytest.mark.parametrize("mutation", ["wrong-comment", "duplicate-member", "wrong-path"])
def test_acquisition_mismatch_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mutation: str
) -> None:
    incoming = private_copy(tmp_path, monkeypatch)
    path = incoming.packet / "acquisition/sources.json"
    record: dict[str, Any] = json.loads(path.read_text())
    row = next(row for row in record["members"] if row["path"] == "90/candidate.json.gz")
    if mutation == "wrong-comment":
        record["comment"] = "https://github.com/jlevy/squares/issues/997#issuecomment-0"
    elif mutation == "duplicate-member":
        record["members"].append(row.copy())
    else:
        row["retained_at"] = "source/90/input.json.gz"
    path.write_text(json.dumps(record))
    with pytest.raises(houses.HouseError):
        incoming.certificate(90)


def test_missing_native_control_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    incoming = private_copy(tmp_path, monkeypatch)
    exact = incoming.certificate(90)
    path = incoming.receipt(90)
    receipt = json.loads(lzma.decompress(path.read_bytes()))
    receipt["cases"].pop()
    path.write_bytes(lzma.compress(json.dumps(receipt).encode()))
    with pytest.raises(houses.HouseError, match="exactly the count's three jobs"):
        incoming.jobs(90, exact)
