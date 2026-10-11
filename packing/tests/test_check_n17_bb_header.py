"""Header-only receipts cannot stand in for full BB tree verification."""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
import subprocess
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n17_bb_header as tool


def fixture() -> tuple[dict[str, Any], tool.full.Cells]:
    polygon = [["0/1", "0/1"], ["1/1", "0/1"], ["1/1", "1/1"], ["0/1", "1/1"]]
    data = {
        "schema": "n17-subpattern-bb-certificate/v1",
        "header": {
            "cap": "3/1",
            "pattern": ["toy"],
            "cells": [polygon],
            "pairs": [],
            "root_angles": [["0/1", "2/1"]],
            "root_boxes": [["0/1", "1/1", "0/1", "1/1"]],
            "half_pi_multiples": {"0": ["0/1", "0/1"]},
        },
        "trig": "absent-trig",
        "chunks": ["absent-tree"],
    }
    cells = tool.full.Cells(
        {"toy": tuple((Q(x), Q(y)) for x, y in polygon)},
        Q(3),
        {"kind": "synthetic"},
    )
    return data, cells


def save(tmp_path: Path, data: dict[str, Any]) -> tuple[Path, str, str]:
    raw = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    compressed = gzip.compress(raw, mtime=0)
    p = tmp_path / "manifest.json.gz"
    _ = p.write_bytes(compressed)
    return p, hashlib.sha256(compressed).hexdigest(), hashlib.sha256(raw).hexdigest()


def run(tmp_path: Path, data: dict[str, Any], cells: tool.full.Cells) -> dict[str, Any]:
    p, digest, identity = save(tmp_path, data)
    return tool.check(p, digest, identity, time.monotonic() + 30, cells=cells)


def test_real_standing_header_only_does_not_read_missing_tree_or_trig(tmp_path: Path) -> None:
    data, cells = fixture()
    receipt = run(tmp_path, data, cells)
    assert receipt["status"] == "HEADER_ONLY_PASS"
    assert receipt["mode"] == "HEADER_ONLY"
    assert receipt["counts"] == {"header": 1}
    for key in (
        "full_verification_passed",
        "tree_verification_performed",
        "trig_verification_performed",
        "ordinary_exclusion_admitted",
        "census_admission",
        "global_bound_changed",
    ):
        assert receipt[key] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("cap", "4/1"),
        ("pattern", ["missing"]),
        ("pairs", [[0, 0]]),
        ("root_angles", [["0/1", "1/1"]]),
        ("root_boxes", [["0/1", "1/2", "0/1", "1/1"]]),
        ("half_pi_multiples", {"1": ["0/1", "1/1"]}),
        ("settings", {"taylor": True, "taylor_k": "0/1"}),
    ],
)
def test_header_domain_changes_are_refused(
    tmp_path: Path,
    field: str,
    value: Any,
) -> None:
    data, cells = fixture()
    data["header"][field] = value
    with pytest.raises(ValueError, match=r"cap|source|pairs|narrower|box|enclose|schema"):
        _ = run(tmp_path, data, cells)


def test_duplicate_pattern_and_incomplete_angle_roster_refuse(tmp_path: Path) -> None:
    data, cells = fixture()
    data["header"]["root_angles"] = []
    with pytest.raises(ValueError, match="roster"):
        _ = run(tmp_path, data, cells)
    data["header"]["pattern"] = ["toy", "toy"]
    with pytest.raises(ValueError, match="unique"):
        _ = run(tmp_path, data, cells)


def test_changed_canonical_or_compressed_identity_refuses(tmp_path: Path) -> None:
    data, cells = fixture()
    p, digest, identity = save(tmp_path, data)
    with pytest.raises(ValueError, match="bytes"):
        _ = tool.check(p, "0" * 64, identity, time.monotonic() + 30, cells=cells)
    with pytest.raises(ValueError, match="canonical"):
        _ = tool.check(p, digest, "0" * 64, time.monotonic() + 30, cells=cells)


def test_private_snapshot_and_postcheck_refuse_original_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data, cells = fixture()
    p, digest, identity = save(tmp_path, data)
    original = tool.full.Verifier.check_header

    def mutate(verifier: tool.full.Verifier, frame: tool.full.Cells) -> None:
        assert verifier.directory != p.parent
        assert list(verifier.directory.iterdir()) == [
            verifier.directory / f"{identity}.json.gz"
        ]
        original(verifier, frame)
        _ = p.write_bytes(b"mutated")

    monkeypatch.setattr(tool.full.Verifier, "check_header", mutate)
    with pytest.raises(ValueError, match="changed"):
        _ = tool.check(p, digest, identity, time.monotonic() + 30, cells=cells)


def test_compressed_and_decoded_limits(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    data, cells = fixture()
    p, digest, identity = save(tmp_path, data)
    monkeypatch.setattr(tool, "COMPRESSED_LIMIT", 1)
    with pytest.raises(tool.IncompleteError, match="compressed"):
        _ = tool.check(p, digest, identity, time.monotonic() + 30, cells=cells)
    monkeypatch.setattr(tool, "COMPRESSED_LIMIT", 1 << 20)
    monkeypatch.setattr(tool, "DECODED_LIMIT", 1)
    with pytest.raises(tool.IncompleteError, match="decoded"):
        _ = tool.check(p, digest, identity, time.monotonic() + 30, cells=cells)


def test_used_oversize_incomplete_unused_opaque_preserved(tmp_path: Path) -> None:
    data, cells = fixture()
    data["header"]["unrelated"] = "1e999999999"
    assert run(tmp_path, data, cells)["header_checks_passed"]
    data["header"]["cap"] = f"{1 << 4096}/1"
    with pytest.raises(tool.IncompleteError, match="bit"):
        _ = run(tmp_path, data, cells)
    data["header"]["cap"] = "1e999999999"
    with pytest.raises(ValueError, match="rational"):
        _ = run(tmp_path, data, cells)


def test_constants_and_deadline_refuse(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    data, cells = fixture()
    p, digest, identity = save(tmp_path, data)
    with pytest.raises(tool.IncompleteError, match="wall"):
        _ = tool.check(p, digest, identity, time.monotonic() - 1, cells=cells)
    monkeypatch.setattr(tool.full, "constants_hold", lambda: False)
    with pytest.raises(ValueError, match="Machin"):
        _ = tool.check(p, digest, identity, time.monotonic() + 30, cells=cells)


def test_cli_synthetic_default_frame_and_exclusive_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data, cells = fixture()
    p, digest, identity = save(tmp_path, data)
    monkeypatch.setattr(tool.full, "cover_cells", lambda: cells)
    output = tmp_path / "receipt.json"
    argv = [
        "--manifest",
        str(p),
        "--compressed-sha256",
        digest,
        "--manifest-id",
        identity,
        "--output",
        str(output),
    ]
    assert tool.main(argv) == 0
    assert json.loads(output.read_bytes())["mode"] == "HEADER_ONLY"
    with pytest.raises(FileExistsError):
        _ = tool.main(argv)
    altered = copy.deepcopy(data)
    altered["header"]["pairs"] = [[0, 0]]
    p, digest, identity = save(tmp_path, altered)
    argv[3], argv[5], argv[-1] = digest, identity, str(tmp_path / "refused.json")
    assert tool.main(argv) == 1
    refusal = json.loads((tmp_path / "refused.json").read_bytes())
    assert refusal["status"] == "HEADER_REFUSED"
    assert refusal["full_verification_passed"] is False


def test_final_deadline_and_output_caps(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    data, cells = fixture()
    p, digest, identity = save(tmp_path, data)
    original = tool.full.Verifier.check_header

    def expire(verifier: tool.full.Verifier, frame: tool.full.Cells) -> None:
        original(verifier, frame)
        monkeypatch.setattr(tool.time, "monotonic", lambda: 100)

    monkeypatch.setattr(tool.full.Verifier, "check_header", expire)
    with pytest.raises(tool.IncompleteError, match="wall"):
        _ = tool.check(p, digest, identity, 99, cells=cells)
    monkeypatch.setattr(tool, "OUTPUT_LIMIT", 1)
    with pytest.raises(tool.IncompleteError, match="output"):
        _ = tool.encode({"status": "HEADER_ONLY_PASS"})


@pytest.mark.parametrize("value", ["nan", "inf", "0"])
def test_nonfinite_or_zero_cli_wall_refuses(tmp_path: Path, value: str) -> None:
    with pytest.raises(SystemExit, match="2"):
        _ = tool.main(
            [
                "--manifest",
                "unused",
                "--manifest-id",
                "0" * 64,
                "--compressed-sha256",
                "0" * 64,
                "--output",
                str(tmp_path / "unused"),
                "--max-seconds",
                value,
            ]
        )


def test_two_clean_processes_same_header_receipt(tmp_path: Path) -> None:
    data, _ = fixture()
    p, digest, identity = save(tmp_path, data)
    script = """
import json, sys, time
from fractions import Fraction as Q
from pathlib import Path
from devtools import check_n17_bb_header as h
forbidden = ('scipy', 'sqpack.hull_kernel', 'devtools.pilot_n17')
assert not any(n.startswith(forbidden) for n in sys.modules)
polygon = ((Q(0),Q(0)),(Q(1),Q(0)),(Q(1),Q(1)),(Q(0),Q(1)))
cells = h.full.Cells({'toy': polygon},Q(3),{'kind':'synthetic'})
r = h.check(Path(sys.argv[1]), sys.argv[2], sys.argv[3], time.monotonic()+30, cells=cells)
Path(sys.argv[4]).write_text(json.dumps(r, sort_keys=True))
"""
    outputs = [tmp_path / "first.json", tmp_path / "fresh.json"]
    for output in outputs:
        result = subprocess.run(
            [sys.executable, "-c", script, str(p), digest, identity, str(output)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        assert result.returncode == 0, result.stderr
    assert json.loads(outputs[0].read_bytes()) == json.loads(outputs[1].read_bytes())


def test_star_order_passes_old_local_turns_but_new_enclosure_refuses(tmp_path: Path) -> None:
    data, _ = fixture()
    source = ((Q(0), Q(0)), (Q(2), Q(0)), (Q(3), Q(2)), (Q(1), Q(3)), (Q(-1), Q(2)))
    star = [source[index] for index in (0, 2, 4, 1, 3)]
    data["header"]["cells"] = [[[f"{x}/1", f"{y}/1"] for x, y in star]]
    data["header"]["root_boxes"] = [["-1/1", "3/1", "0/1", "3/1"]]
    cells = tool.full.Cells({"toy": source}, Q(3), {"kind": "synthetic-pentagon"})
    p, _, identity = save(tmp_path, data)
    _ = (tmp_path / f"{identity}.json.gz").write_bytes(p.read_bytes())
    verifier = tool.full.Verifier(tmp_path, identity)
    verifier.check_header(cells)
    assert not verifier.failures  # Set equality plus positive local turns is insufficient.
    assert all(
        tool.full.cross(star[i], star[(i + 1) % 5], star[(i + 2) % 5]) > 0 for i in range(5)
    )
    with pytest.raises(ValueError, match="does not enclose original"):
        _ = run(tmp_path, data, cells)


def test_cyclic_source_rotation_still_encloses_every_vertex(tmp_path: Path) -> None:
    data, cells = fixture()
    vertices = data["header"]["cells"][0]
    data["header"]["cells"][0] = vertices[1:] + vertices[:1]
    assert run(tmp_path, data, cells)["complete_original_cell_halfplane_enclosure_checked"]


def test_duplicate_vertices_refused_by_new_enclosure(tmp_path: Path) -> None:
    data, cells = fixture()
    p, _, identity = save(tmp_path, data)
    _ = (tmp_path / f"{identity}.json.gz").write_bytes(p.read_bytes())
    verifier = tool.full.Verifier(tmp_path, identity)
    verifier.cells[0].append(verifier.cells[0][0])
    with pytest.raises(ValueError, match="duplicate declared"):
        tool.check_original_enclosure(verifier, cells)
