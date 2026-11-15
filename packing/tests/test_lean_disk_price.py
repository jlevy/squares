"""devtools.lean_disk_price: a toolchain's size from its stream, and a disk plan's verdict."""

from __future__ import annotations

import hashlib
import io
import json
import random
import tarfile
from pathlib import Path

import pytest

from devtools import lean_disk_price as price

FILES = {
    "lean-9.9.9-linux/lib/lean/Init.olean": b"o" * 3000,
    "lean-9.9.9-linux/lib/lean/Lean/Elab.olean": b"e" * 2000,
    "lean-9.9.9-linux/bin/lean": b"b" * 700,
    "lean-9.9.9-linux/LICENSE": b"l" * 11,
}


def _archive() -> bytes:
    """A small toolchain-shaped ``.tar.zst``, written in memory."""
    out = io.BytesIO()
    with tarfile.open(fileobj=out, mode="w:zst") as archive:
        for name, data in FILES.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    return out.getvalue()


def test_sizes_and_digest_come_from_the_stream() -> None:
    blob = _archive()
    record = price.measure_toolchain(
        io.BytesIO(blob),
        label="test",
        expect_bytes=len(blob),
    )
    assert record["compressed_bytes"] == len(blob)
    assert record["sha256"] == hashlib.sha256(blob).hexdigest()
    assert record["files"] == 4
    assert record["unpacked_bytes"] == sum(len(data) for data in FILES.values())
    assert record["by_directory"] == {"lib/lean": 5000, "bin": 700, ".": 11}


def test_a_stream_of_another_length_is_refused() -> None:
    with pytest.raises(price.PriceRefusedError, match="expected 1"):
        price.measure_toolchain(io.BytesIO(_archive()), label="test", expect_bytes=1)


def test_a_cut_off_archive_is_refused_and_not_priced_small() -> None:
    blob = _archive()
    with pytest.raises(price.PriceRefusedError, match="does not read to its end"):
        price.measure_toolchain(io.BytesIO(blob[: len(blob) // 2]), label="test")


def test_a_stream_cut_inside_a_member_header_is_refused() -> None:
    rng = random.Random(0)
    out = io.BytesIO()
    with tarfile.open(fileobj=out, mode="w:zst") as archive:
        for i in range(3):
            data = rng.randbytes(50_000)
            info = tarfile.TarInfo(f"lean-9.9.9-linux/lib/lean/M{i}.olean")
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    blob = out.getvalue()
    for cut in range(50_000, 52_000, 13):
        with pytest.raises(price.PriceRefusedError):
            price.measure_toolchain(io.BytesIO(blob[:cut]), label="test")


def test_the_command_writes_its_receipt(tmp_path: Path) -> None:
    source = tmp_path / "lean.tar.zst"
    source.write_bytes(_archive())
    receipt = tmp_path / "toolchain.json"
    assert (
        price.main(["toolchain", str(source), "--label", "test", "--json", str(receipt)]) == 0
    )
    record = json.loads(receipt.read_text(encoding="utf-8"))
    assert record["kind"] == price.TOOLCHAIN_KIND
    assert record["unpacked_bytes"] == 5711


def test_the_plan_refuses_a_total_over_the_cap_or_the_free_disk() -> None:
    items = [("toolchain", 3_000, "measured: r.json"), ("mathlib", 6_500, "stated")]
    assert price.price_plan(items, cap=10_000, free=20_000)["verdict"] == "FITS"
    over_cap = price.price_plan(items, cap=9_000, free=20_000)
    assert over_cap["verdict"] == "DOES-NOT-FIT"
    assert over_cap["margin_to_cap_bytes"] == -500
    assert price.price_plan(items, cap=20_000, free=9_400)["verdict"] == "DOES-NOT-FIT"


def test_the_plan_takes_a_measured_item_from_a_receipt_only(tmp_path: Path) -> None:
    receipt = tmp_path / "toolchain.json"
    fields = {
        "kind": price.TOOLCHAIN_KIND,
        "label": "lean",
        "sha256": "ab",
        "unpacked_bytes": 42,
    }
    receipt.write_text(json.dumps(fields), encoding="utf-8")
    assert price.parse_item(f"toolchain=@{receipt}") == (
        "toolchain",
        42,
        "measured: lean, sha256 ab",
    )
    assert price.parse_item("mathlib=6500") == ("mathlib", 6500, "stated")
    other = tmp_path / "other.json"
    other.write_text(
        json.dumps({"kind": "something-else", "unpacked_bytes": 1}), encoding="utf-8"
    )
    for bad in (f"toolchain=@{other}", "mathlib=6.5GB", "mathlib=-1", "6500"):
        with pytest.raises(price.PriceRefusedError):
            price.parse_item(bad)


def test_the_plan_command_exits_two_when_it_does_not_fit(tmp_path: Path) -> None:
    verdict = tmp_path / "plan.json"
    args = [
        "plan",
        "--item",
        "a=10",
        "--item",
        "b=5",
        "--disk",
        str(tmp_path),
        "--json",
        str(verdict),
    ]
    assert price.main([*args, "--cap", "14"]) == 2
    assert json.loads(verdict.read_text(encoding="utf-8"))["verdict"] == "DOES-NOT-FIT"
    assert price.main([*args, "--cap", "15"]) == 0
