"""Synthetic named/D4 metadata joins; no scientific tree or catalogue evaluation."""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest

from devtools import inspect_n17_subpattern_relevance as tool

NAMES = [f"cell-{i}" for i in range(24)]
ACTIONS = {"identity": list(range(24)), "swap": [1, 0, *range(2, 24)]}


def deadline() -> float:
    return time.monotonic() + 30


def rows() -> list[dict[str, Any]]:
    return [
        {"mask": sum(1 << i for i in cells), "orbit_size": size, "distance": distance}
        for cells, size, distance in [
            (list(range(17)), 1, 2),
            (list(range(1, 18)), 2, 4),
            (list(range(7, 24)), 1, 2),
        ]
    ]


def sources() -> list[dict[str, Any]]:
    return [{"id": "A", "source_mask": 1}, {"id": "B", "source_mask": 1 << 23}]


def test_d4_actions_weighted_marginal_union_and_overlap() -> None:
    result = tool.project(NAMES, ACTIONS, rows(), sources(), deadline())
    a, b = result["candidates"]
    assert a["potential_current_residue"] == {"orbits": 2, "states": 3}
    assert a["potential_distance_two"] == {"orbits": 1, "states": 1}
    assert a["matched_orbits"][1]["action"] == "swap"
    assert a["matched_orbits"][1]["image_cells"] == ["cell-1"]
    assert b["potential_current_residue"] == {"orbits": 1, "states": 1}
    assert result["union_potential_current_residue"] == {"orbits": 3, "states": 4}
    assert result["pairwise_overlap"][0]["current_residue"] == {"orbits": 0, "states": 0}
    assert result["D4_subset_comparisons"] == 12
    duplicated = tool.project(
        NAMES,
        ACTIONS,
        rows(),
        [sources()[0], {"id": "alias", "source_mask": 1 << 1}],
        deadline(),
    )
    assert duplicated["union_potential_current_residue"] == {"orbits": 2, "states": 3}
    assert duplicated["pairwise_overlap"][0]["current_residue"] == {"orbits": 2, "states": 3}


def test_exact_subset_not_intersection_or_cardinality() -> None:
    result = tool.project(
        NAMES, ACTIONS, rows(), [{"id": "two", "source_mask": (1 << 0) | (1 << 23)}], deadline()
    )
    assert result["union_potential_current_residue"] == {"orbits": 0, "states": 0}
    assert result["D4_subset_comparisons"] == 6


def packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    partition = tmp_path / "partition.json"
    partition.write_text(json.dumps({"orbits": rows()}))
    accepted = tmp_path / "accepted.json"
    accepted.write_text(
        json.dumps(
            {"schema": tool.old.CONTEXT_SCHEMA, "partition": str(partition), "d4": ACTIONS}
        )
    )
    data = {
        "schema": "n17-subpattern-bb-certificate/v1",
        "header": {
            "cap": str(tool.old.U),
            "pattern": NAMES[:7],
            "pairs": [[i, j] for i in range(7) for j in range(i + 1, 7)],
            "root_angles": [["opaque", "opaque"]] * 7,
            "root_boxes": [["unverified"]] * 7,
            "settings": {"unverified_guard": True},
        },
    }
    native = tmp_path / "manifest.json.gz"
    raw = gzip.compress(tool.finite.canonical(data))
    native.write_bytes(raw)
    monkeypatch.setattr(
        tool.old, "intake", lambda *_: ([], NAMES, [], {partition: partition.read_bytes()})
    )
    return {
        "schema": tool.CONTEXT_SCHEMA,
        "accepted_descriptor": str(accepted),
        "accepted_descriptor_sha256": hashlib.sha256(accepted.read_bytes()).hexdigest(),
        "candidates": [
            {
                "id": "C",
                "manifest": str(native),
                "compressed_sha256": hashlib.sha256(raw).hexdigest(),
                "manifest_id": tool.finite.identity(data),
            }
        ],
    }


def test_generate_scope_missing_frame_angles_and_cell_enclosure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    result = tool.generate(packet(tmp_path, monkeypatch), deadline())
    c = result["candidates"][0]
    assert c["complete_pair_roster_present"]
    assert c["explicit_B"] is None
    assert c["explicit_frame"] is None
    assert c["settings"] == {"unverified_guard": True}
    assert c["full_shifted_closed_angle_cover_checked"] is False
    assert c["complete_cell_enclosure_checked"] is False
    assert c["hidden_conditioning_absence_checked"] is False
    assert c["full_tree_verification_performed"] is False
    assert all(
        result[k] is False
        for k in [
            "certificate_admission_performed",
            "ordinary_assignment_exclusion_proved",
            "census_admission_proved",
            "global_bound_proved",
        ]
    )
    assert "scipy" not in sys.modules


@pytest.mark.parametrize(
    "key", ["compressed_sha256", "manifest_id", "accepted_descriptor_sha256"]
)
def test_changed_generated_input_identity_refused(
    key: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    descriptor = packet(tmp_path, monkeypatch)
    target = descriptor if key == "accepted_descriptor_sha256" else descriptor["candidates"][0]
    target[key] = "0" * 64
    with pytest.raises(ValueError, match="differ"):
        tool.generate(descriptor, deadline())


@pytest.mark.parametrize("change", ["cap", "unknown", "duplicate"])
def test_wrong_original_cap_or_named_cells_refused(change: str) -> None:
    data = {
        "schema": "n17-subpattern-bb-certificate/v1",
        "header": {"cap": str(tool.old.U), "pattern": NAMES[:7]},
    }
    if change == "cap":
        data["header"]["cap"] = "4"
    elif change == "unknown":
        data["header"]["pattern"][0] = "unknown"
    else:
        data["header"]["pattern"][1] = NAMES[0]
    with pytest.raises(ValueError, match="original"):
        tool.candidate(data, {"id": "C", "manifest_id": "0" * 64}, NAMES)


def test_precharged_comparison_cap_and_deadline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tool, "COMPARISON_LIMIT", 1)
    with pytest.raises(tool.finite.IncompleteError, match="comparison"):
        tool.project(NAMES, ACTIONS, rows(), sources(), deadline())
    with pytest.raises(tool.finite.IncompleteError, match="wall"):
        tool.project(NAMES, ACTIONS, rows(), sources(), 0)


@pytest.mark.parametrize("kind", ["compressed", "decoded"])
def test_compact_manifest_limits(
    kind: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    d = packet(tmp_path, monkeypatch)
    monkeypatch.setattr(tool, "MANIFEST_LIMIT" if kind == "compressed" else "DECODED_LIMIT", 1)
    with pytest.raises(tool.finite.IncompleteError, match="ceiling"):
        tool.generate(d, deadline())


def test_posthash_mutation_and_alias_conflict(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    d = packet(tmp_path, monkeypatch)
    original = tool.project

    def mutate(*args, **kwargs):
        result = original(*args, **kwargs)
        Path(d["candidates"][0]["manifest"]).write_bytes(b"changed")
        return result

    monkeypatch.setattr(tool, "project", mutate)
    with pytest.raises(ValueError, match="changed"):
        tool.generate(d, deadline())
    with pytest.raises(ValueError, match="alias"):
        tool.hold({Path("x"): b"a"}, Path("x"), b"b", hashlib.sha256(b"b").hexdigest())


def test_cli_fresh_payload_refusal_output_and_exclusive_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    d = packet(tmp_path, monkeypatch)
    p, cert, replay = [tmp_path / n for n in ("d.json", "c.json", "r.json")]
    p.write_text(json.dumps(d))
    assert tool.main(["--descriptor", str(p), "--output", str(cert)]) == 0
    assert (
        tool.main(["--descriptor", str(p), "--certificate", str(cert), "--output", str(replay)])
        == 0
    )
    assert json.loads(replay.read_text())["verification_passed"]
    with pytest.raises(FileExistsError):
        tool.main(["--descriptor", str(p), "--output", str(cert)])
    saved = json.loads(cert.read_text())
    saved["union_potential_current_residue"]["states"] += 1
    cert.write_text(json.dumps(saved))
    refused = tmp_path / "refused.json"
    assert (
        tool.main(
            ["--descriptor", str(p), "--certificate", str(cert), "--output", str(refused)]
        )
        == 1
    )
    assert json.loads(refused.read_text())["status"] == "refused"


def test_clean_two_processes_without_scipy() -> None:
    script = """
import json,sys,time
from devtools import inspect_n17_subpattern_relevance as t
names=[str(i) for i in range(24)]
r=t.project(names,{'e':list(range(24))},[{'mask':(1<<17)-1,'orbit_size':1,'distance':2}],[{'id':'C','source_mask':3}],time.monotonic()+10)
assert not any(k=='scipy' or k.startswith('scipy.') for k in sys.modules)
print(json.dumps(r,sort_keys=True))
"""
    outputs = [
        subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        ).stdout
        for _ in range(2)
    ]
    assert outputs[0] == outputs[1]


def test_descriptor_keyset_and_nonfinite_cli(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    d = packet(tmp_path, monkeypatch)
    changed = copy.deepcopy(d) | {"unexpected": True}
    with pytest.raises(ValueError, match="descriptor"):
        tool.generate(changed, deadline())
    with pytest.raises(SystemExit):
        tool.main(["--descriptor", "d", "--output", "o", "--max-seconds", "nan"])
