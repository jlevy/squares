"""The #973 import's replay of Khalili and Gharabaghi's k^2 - 5 board, from its receipts.

``devtools.replay_k2m5_family`` ran the source's own programs on the retained bytes on 14
November 2026 and kept every receipt in the packet's ``receipts/``. These tests read the
retained files only; nothing here runs ``zmx2``, ``qx2_zm.py`` or the Tight-Tile checker.
They hold what the record says those runs showed: the source's fast ``verify.sh`` passed,
each sampled ``zmx2`` column and the root-9632 dump equal the source's records, root 9632
closes, and the source's mutated covers are refused where the published board is not.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from devtools import replay_k2m5_family as replay
from devtools.retained_data import read_retained_bytes

RECEIPTS = replay.PACKET / "receipts"


def _text(name: str) -> str:
    return read_retained_bytes(RECEIPTS / name).decode("utf-8")


def test_patch_is_one_line_in_zmx2() -> None:
    text = (replay.TREE / replay.PATCH).read_text(encoding="utf-8")
    files, removed, added = replay.patch_lines(text)
    assert files == ["b/verify2/src/bin/zmx2.rs"]
    assert removed == ["        for ub in r.uncert.iter().take(40) {"]
    assert len(added) == 2
    assert "ZMX2_PRINT_ALL" in added[0]


def test_columns_parse() -> None:
    assert replay.columns("0-2,15,43") == [0, 1, 2, 15, 43]
    with pytest.raises(SystemExit):
        replay.columns("54-55")


@pytest.fixture(scope="module")
def tree(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("k2m5")
    for path in (
        replay.BOARD,
        "verification/r9632/c9632.txt",
        "verification/controls/c9632_scale0999.txt",
    ):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(read_retained_bytes(replay.TREE / path))
    return root


def test_cropped_covers_are_subsets_of_the_board(tree: Path) -> None:
    real = replay.cropped(tree, "verification/r9632/c9632.txt")
    assert real["segments"] == 632
    assert real["all_in_board"]
    assert real["distinct"]
    assert real["header_equal"]
    assert real["tail_equal"]
    scaled = replay.cropped(tree, "verification/controls/c9632_scale0999.txt")
    assert not scaled["all_in_board"]


def test_a_changed_weight_leaves_the_board(tree: Path) -> None:
    lines = (tree / "verification/r9632/c9632.txt").read_text(encoding="utf-8").splitlines()
    index = next(i for i, line in enumerate(lines) if len(line.split()) == 5)
    fields = lines[index].split()
    fields[4] = str(int(fields[4]) + 1)
    lines[index] = " ".join(fields)
    mutated = tree / "verification/r9632/mutated.txt"
    mutated.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert not replay.cropped(tree, "verification/r9632/mutated.txt")["all_in_board"]


def test_fast_verify_passed() -> None:
    text = _text("verify_fast.log")
    for line in (
        "SANITY-OK",
        "LOCALITY OK",
        "ZMX2-AUDIT-OK",
        "ROOT-9632-CLOSED",
        "COVERAGE-OK",
        "fast checks done",
    ):
        assert line in text
    assert "; exit 0;" in text


def test_sampled_columns_equal_the_source() -> None:
    compare = json.loads(_text("compare.json"))
    columns = compare["zmx2"]
    assert {"cert0", "col15", "col43"} <= set(columns)
    for name, entry in columns.items():
        assert entry["equal"], name
        census = entry["ours"]["census"]
        assert census is not None, name
        if name == "cert0":
            assert census == [2500, 2500, 2500, 0]
        else:
            assert census[0] == 220, name
            assert census[1] == 0, name


def test_root_9632_closes_on_this_run() -> None:
    compare = json.loads(_text("compare.json"))["r9632"]
    assert compare["dump_equal"]
    assert compare["dump_uncert"] == 6850
    assert compare["qx2_equal"]
    assert compare["zm_unc_equal"]
    assert compare["check"] == "ROOT-9632-CLOSED"
    dump = replay.zmx2_summary(_text("r9632/dump.log"))
    assert dump["census"] == [1, 0, 168563, 77432, 0, 6850, 40]


def test_controls_are_refused() -> None:
    real = replay.zmx2_summary(_text("controls/zmx2-real-x15y36.log"))
    assert str(real["verdict"]).startswith("REGION CLEAN")
    for name in ("zmx2-scale0999-x15y36", "zmx2-scale0993-x15y36"):
        summary = replay.zmx2_summary(_text(f"controls/{name}.log"))
        assert str(summary["verdict"]).startswith("NOT VERIFIED"), name
    assert "ROOT-9632-NOT-CLOSED" in _text("controls/check_9632_scale0999.log")
    controls = json.loads(_text("compare.json"))["controls"]
    for name in ("zmx2-real-x15y36", "zmx2-scale0999-x15y36", "zmx2-scale0993-x15y36",
                 "qx2-scale0999-r9632"):  # fmt: skip
        assert controls[name]["equal"], name


def test_locality_and_tight_tile_controls_are_refused() -> None:
    assert "LOCALITY FAILED" in _text("controls/locality-onemutation.log")
    assert "without an integer-translate in mu_11: 176" in _text(
        "controls/locality-onemutation.log"
    )
    real = _text("controls/tight-ctl-rise-real.log")
    assert "refused cells 0 ;" in real
    mutant = _text("controls/tight-ctl-rise.log")
    assert "refused cells 443 ; of which containing the face point (1, 1): 6" in mutant


def test_tight_tile_sample_equals_the_source() -> None:
    tight = json.loads(_text("compare.json"))["tight"]
    assert len(tight) == 26
    for name, entry in tight.items():
        assert entry["equal"], name
        assert entry["final"] == {"final": "ALL-OK"}, name


def test_receipts_equal_the_source_records() -> None:
    logs = replay.TREE / "verification/logs/zmx2_box11"
    for receipt in sorted((RECEIPTS / "zmx2").glob("c*.log")):
        if receipt.name.endswith("_roots.log"):
            continue
        record = logs / ("cert0.txt" if receipt.stem == "cert0" else f"{receipt.stem}.out")
        ours = replay.zmx2_summary(_text(f"zmx2/{receipt.name}"))
        assert ours == replay.zmx2_summary(read_retained_bytes(record).decode("utf-8")), (
            receipt.stem
        )
    for receipt in sorted((RECEIPTS / "tight").glob("*.log")):
        record = replay.TREE / "tight_tile/out" / f"{receipt.stem}.out"
        assert replay.tt_lines(_text(f"tight/{receipt.name}")) == replay.tt_lines(
            read_retained_bytes(record).decode("utf-8")
        ), receipt.stem
