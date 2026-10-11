"""Lossless complete SQUISH receipts, legacy plain packets, and fresh admission."""

from __future__ import annotations

import copy
import gzip
import json
import shutil
from pathlib import Path
from typing import Any, Self

import pytest

from devtools import squish_upper_bound_packets as packet


def write_json(path: Path, value: object) -> None:
    data = json.dumps(value).encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(data, mtime=0) if path.suffix == ".gz" else data)


@pytest.mark.parametrize("physical", [False, True])
def test_plain_gzip_twins_are_compared_even_for_physical_paths(
    tmp_path: Path, *, physical: bool
) -> None:
    logical = tmp_path / "certification.json"
    packed = logical.with_name(logical.name + ".gz")
    write_json(logical, {"cases": []})
    packed.write_bytes(gzip.compress(logical.read_bytes(), mtime=0))
    selected = packed if physical else logical
    assert packet.read_json(selected) == {"cases": []}
    write_json(logical, {"cases": [1]})
    with pytest.raises(packet.PacketError, match="differs from its compressed copy"):
        packet.read_json(selected)
    logical.unlink()
    assert packet.read_json(selected) == {"cases": []}


def test_gzip_decoded_and_ordinary_json_ceilings_stay_separate(tmp_path: Path) -> None:
    assert packet.MAX_RECEIPT_BYTES == 4_000_000
    assert packet.MAX_SOURCE_BYTES == 1_000_000
    value = {"complete_input": "x" * (packet.MAX_SOURCE_BYTES + 1)}
    receipt = tmp_path / "certification.json.gz"
    write_json(receipt, value)
    assert packet.read_json(receipt) == value
    ordinary = tmp_path / "ordinary.json.gz"
    ordinary.write_bytes(receipt.read_bytes())
    with pytest.raises(packet.PacketError, match="byte ceiling"):
        packet.read_json(ordinary)
    write_json(receipt, {"complete_input": "x" * packet.MAX_RECEIPT_BYTES})
    with pytest.raises(packet.PacketError, match="byte ceiling"):
        packet.read_json(receipt)


@pytest.mark.parametrize("bad", [b"not gzip", gzip.compress(b"{}", mtime=0)[:-3]])
def test_corrupt_gzip_is_a_clean_refusal(tmp_path: Path, bad: bytes) -> None:
    path = tmp_path / "certification.json.gz"
    path.write_bytes(bad)
    with pytest.raises(packet.PacketError, match="gzip integrity failure"):
        packet.read_json(path)


@pytest.mark.parametrize("compressed", [False, True, None])
def test_partial_producer_preserves_complete_previous_roster(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, compressed: bool | None
) -> None:
    original = packet.read_json(packet.receipt_path())
    local = tmp_path / "packet"
    monkeypatch.setattr(packet, "PACKET", local)
    monkeypatch.setattr(packet, "REPO", tmp_path)
    path = local / (
        "receipts/certification.json.gz"
        if compressed is not False
        else "receipts/certification.json"
    )
    if compressed is not None:
        write_json(path, original)
    selected = original["cases"][-1]["n"]
    replacement = copy.deepcopy(original["cases"][-1])
    replacement["selected_producer_regression"] = True

    class InlinePool:
        def __init__(self, *, max_workers: int) -> None:
            assert max_workers == 1

        def __enter__(self) -> Self:
            return self

        def __exit__(self, *_args: object) -> None:
            pass

        def map(self, fn: Any, counts: list[int]) -> list[Any]:
            return [fn(n) for n in counts]

    monkeypatch.setattr(packet, "ProcessPoolExecutor", InlinePool)
    previous_rows = {row["n"]: row for row in original["cases"]}
    monkeypatch.setattr(
        packet, "certify_one", lambda n: replacement if n == selected else previous_rows[n]
    )
    monkeypatch.setattr(packet, "negative_controls", lambda: {"fixture": True})
    packet.certify([selected] if compressed is not None else list(packet.NUMBERS), workers=1)
    result = packet.read_json(path)
    assert result["cases"][:-1] == original["cases"][:-1]
    assert result["cases"][-1] == replacement
    assert len(result["cases"]) == len(packet.NUMBERS)
    assert packet.receipt_path() == path
    assert not path.with_name(
        "certification.json" if compressed is not False else "certification.json.gz"
    ).exists()
    for label in ("release", "supplement"):
        claims = packet.read_json(local / f"acquisition/{label}-normalized-claims.json")
        assert claims["certificate_receipt"] == path.relative_to(tmp_path).as_posix()


@pytest.mark.parametrize("bad", ["twins", "duplicate", "truncated", "object"])
def test_bad_previous_receipt_refuses_before_any_producer_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, bad: str
) -> None:
    original = packet.read_json(packet.receipt_path())
    local = tmp_path / "packet"
    path = local / "receipts/certification.json.gz"
    if bad == "duplicate":
        original["cases"].append(original["cases"][0])
    write_json(path, [] if bad == "object" else original)
    if bad == "twins":
        plain = path.with_suffix("")
        plain.write_bytes(gzip.decompress(path.read_bytes()))
    elif bad == "truncated":
        path.write_bytes(path.read_bytes()[:-3])
    monkeypatch.setattr(packet, "PACKET", local)

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        pytest.fail("producer started before previous receipt admission")

    monkeypatch.setattr(packet, "ProcessPoolExecutor", forbidden)
    with pytest.raises(packet.PacketError, match=r"representation|roster|gzip integrity"):
        packet.certify([packet.NUMBERS[-1]], workers=1)


def test_complete_real_receipt_refuses_mutations_and_restores(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original_read = packet.read_json
    path = tmp_path / "certification.json.gz"
    path.write_bytes(packet.receipt_path().read_bytes())
    before = path.read_bytes()
    original_path = packet.receipt_path()
    # Redirect only the physical receipt read to the independently mutable copy;
    # every ordinary source, claim and certificate admission remains unchanged.
    monkeypatch.setattr(
        packet,
        "read_json",
        lambda selected: original_read(path if selected == original_path else selected),
    )
    packet.check(list(packet.NUMBERS), replay=False)
    for mutant in ("native", "input"):
        value = original_read(path)
        if mutant == "native":
            value["cases"][0]["exact_verify"]["verification_passed"] = False
        else:
            value["cases"][0]["checker_input"]["squares"][0]["corners"][0][0] = "-1"
        write_json(path, value)
        with pytest.raises(packet.PacketError, match=r"checker coverage|semantic mismatch"):
            packet.check([packet.NUMBERS[0]], replay=False)
        path.write_bytes(before)
        packet.check(list(packet.NUMBERS), replay=False)


def test_complete_packet_admits_agreeing_twins_and_refuses_changed_plain_copy(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    private = tmp_path / "checkout"
    local_packet = private / packet.PACKET.relative_to(packet.REPO)
    local_witnesses = private / packet.WITNESSES.relative_to(packet.REPO)
    shutil.copytree(packet.PACKET, local_packet)
    shutil.copytree(packet.WITNESSES, local_witnesses)
    monkeypatch.setattr(packet, "REPO", private)
    monkeypatch.setattr(packet, "PACKET", local_packet)
    monkeypatch.setattr(packet, "WITNESSES", local_witnesses)
    packed = packet.receipt_path()
    plain = packed.with_suffix("")
    decoded = gzip.decompress(packed.read_bytes())
    plain.write_bytes(decoded)
    assert packet.receipt_path() == packed
    packet.check([packet.NUMBERS[0]], replay=False)
    # Even semantically identical JSON whitespace cannot hide divergent twins.
    plain.write_bytes(decoded + b" ")
    with pytest.raises(packet.PacketError, match="differs from its compressed copy"):
        packet.check([packet.NUMBERS[0]], replay=False)
    plain.write_bytes(decoded)
    packet.check([packet.NUMBERS[0]], replay=False)
