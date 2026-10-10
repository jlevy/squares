"""Couzo's later n = 375 and 378 reports: derived-only custody and dated supersession."""

from __future__ import annotations

import json
import shutil
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_source_coverage
from devtools import couzo_extended_reports as earlier
from devtools import couzo_extended_updates as updates
from devtools import couzo_followup_reports as followup
from sqpack.yamlio import load_yaml

#: The later sides the 2d32a6e text files print, and the ffd900d sides they beat.
LATER = {375: "19.907024692022954", 378: "19.946861170999796"}
FFD900D = {375: "19.907052698737502", 378: "19.947426312032292"}


def record() -> dict[str, Any]:
    return json.loads((updates.PACKET / "acquisition/sources.json").read_text())["sources"][0]


def source_texts(packet: Path = updates.PACKET) -> dict[int, bytes]:
    """Both source texts, rebuilt from the retained facts alone."""
    return {
        n: updates.reconstructed_text(
            n, (packet / updates.fact_name(n)).read_bytes(), packet / updates.fact_name(n)
        ).encode()
        for n in updates.COUNTS
    }


@pytest.fixture
def copied(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """The retained packet copied into a private tree the checks may read."""
    monkeypatch.setattr(updates, "REPO", tmp_path)
    destination = tmp_path / "packet"
    shutil.copytree(updates.PACKET, destination)
    return destination


def test_the_retained_packet_rebuilds_both_later_reports_byte_for_byte() -> None:
    assert updates.check_packet() == LATER
    source = record()
    _, outside = updates.recorded_identities()
    texts = source_texts()
    for case in source["cases"]:
        n = case["n"]
        assert case["source_blob"] == outside[n]["blob"]
        assert case["side"] == outside[n]["printed_side"] == LATER[n]
        assert case["size"] == len(texts[n])
        assert case["supersedes"]["side"] == FFD900D[n]
        assert Fraction(case["side"]) < Fraction(case["supersedes"]["side"])
    assert sum(len(text) for text in texts.values()) == 54_556
    assert sum(text.count(b"\n") - 3 for text in texts.values()) == 753
    assert source["raw_asset_retained"] is False
    assert len(source["custody"]["tree"]) == 136


def test_the_ffd900d_reports_stay_pinned_and_become_dated_rows() -> None:
    """The earlier packet still prints its sides; the register supersedes, never rewrites."""
    claims = earlier.read_json(earlier.PACKET / "acquisition/sources.json")
    printed = {row["n"]: row["side"] for row in claims["sources"][0]["cases"]}
    assert {n: printed[n] for n in updates.COUNTS} == FFD900D
    coverage = load_yaml(check_source_coverage.COVERAGE.read_text())
    rows = {
        (row["n"], row["source_id"]): row
        for row in coverage["beyond_horizon_claims"]
        if row["n"] in updates.COUNTS
    }
    assert set(rows) == {
        (n, source) for n in updates.COUNTS for source in (earlier.SOURCE_ID, updates.SOURCE_ID)
    }
    for n in updates.COUNTS:
        historical, current = rows[n, earlier.SOURCE_ID], rows[n, updates.SOURCE_ID]
        assert historical["value"] == FFD900D[n]
        assert historical["disposition"] == "superseded"
        assert historical["superseded_by"] == updates.SOURCE_ID
        assert current["value"] == LATER[n]
        assert current["disposition"] == "tracked-outside-case-corpus"
    standing = check_source_coverage.current_beyond_horizon(coverage)
    assert {n: standing[n]["source_id"] for n in updates.COUNTS} == dict.fromkeys(
        updates.COUNTS, updates.SOURCE_ID
    )
    source = check_source_coverage.source_by_id(coverage, updates.SOURCE_ID)
    assert check_source_coverage.load_claims(updates.ROOT / source["claims_record"]) == LATER


def test_an_edited_pose_token_no_longer_rebuilds_its_pinned_blob(copied: Path) -> None:
    path = copied / updates.fact_name(378)
    original = path.read_bytes()
    token = b"'6.28392664176345761e-01'"
    assert token in original
    path.write_bytes(original.replace(token, b"'6.28392664176345772e-01'", 1))
    with pytest.raises(updates.UpdateError, match=r"n378.txt: bytes differ from the pinned"):
        updates.check_packet(copied)
    path.write_bytes(original)
    assert updates.check_packet(copied) == LATER


@pytest.mark.parametrize(
    ("old", "new"),
    [
        (b'"side": "19.907024692022954"', b'"side": "19.907024692022955"'),
        (b'"side": "19.907052698737502"', b'"side": "19.907052698737503"'),
        (b'"sha256": "cdcb176c', b'"sha256": "cdcb176d'),
        (b'"raw_asset_retained": false', b'"raw_asset_retained": true'),
    ],
)
def test_an_edited_record_is_not_the_export_of_the_pinned_reports(
    copied: Path, old: bytes, new: bytes
) -> None:
    path = copied / "acquisition/sources.json"
    original = path.read_bytes()
    assert original.count(old) == 1
    path.write_bytes(original.replace(old, new))
    with pytest.raises(updates.UpdateError, match=r"sources.json differs from the export"):
        updates.check_packet(copied)


def test_the_tree_must_be_the_follow_up_packets_record(copied: Path) -> None:
    path = copied / "acquisition/sources.json"
    document = json.loads(path.read_bytes())
    document["sources"][0]["custody"]["tree"]["README.md"]["size"] += 1
    path.write_text(json.dumps(document, indent=2) + "\n")
    with pytest.raises(updates.UpdateError, match=r"follow-up packet's record"):
        updates.check_packet(copied)


def test_raw_assets_symlinks_and_missing_facts_are_refused(
    copied: Path, tmp_path: Path
) -> None:
    raw = copied / "n375.txt"
    raw.write_bytes(source_texts(copied)[375])
    with pytest.raises(updates.UpdateError, match=r"unexpected or missing"):
        updates.check_packet(copied)
    raw.unlink()
    fact = copied / updates.fact_name(375)
    elsewhere = tmp_path / "outside.yaml"
    shutil.move(fact, elsewhere)
    with pytest.raises(updates.UpdateError, match=r"unexpected or missing"):
        updates.check_packet(copied)
    fact.symlink_to(elsewhere)
    with pytest.raises(updates.UpdateError, match=r"private"):
        updates.check_packet(copied)


def test_export_holds_each_input_to_its_identity_side_and_predecessor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    leaves = record()["custody"]["tree"]
    texts = {f"n{n}.txt": text for n, text in source_texts().items()}
    retained = {
        name: (updates.PACKET / name).read_bytes()
        for name in ("acquisition/sources.json", *map(updates.fact_name, updates.COUNTS))
    }
    assert updates.export_contents(leaves, lambda leaf: texts[leaf["path"]]) == retained

    swapped = {"n375.txt": texts["n378.txt"], "n378.txt": texts["n375.txt"]}
    with pytest.raises(updates.UpdateError, match=r"n375.txt: bytes differ"):
        updates.export_contents(leaves, lambda leaf: swapped[leaf["path"]])

    priors = updates.prior_reports()
    priors[375] = {**priors[375], "side": LATER[375]}
    monkeypatch.setattr(updates, "prior_reports", lambda: priors)
    with pytest.raises(updates.UpdateError, match=r"n=375: .* does not beat the ffd900d"):
        updates.export_contents(leaves, lambda leaf: texts[leaf["path"]])
    monkeypatch.undo()

    tree, outside = updates.recorded_identities()
    outside[378] = {**outside[378], "printed_side": FFD900D[378]}
    monkeypatch.setattr(updates, "recorded_identities", lambda: (tree, outside))
    with pytest.raises(updates.UpdateError, match=r"n378.txt: printed side differs"):
        updates.export_contents(leaves, lambda leaf: texts[leaf["path"]])


def test_acquire_writes_only_a_fresh_packet(tmp_path: Path) -> None:
    with pytest.raises(updates.UpdateError, match=r"fresh derived packet"):
        updates.acquire(tmp_path / "no-object-store", updates.PACKET)
    assert followup.OUTSIDE_HORIZON == updates.COUNTS
