"""Full-input custody, exact decimal comparison and three read-only leaf controls."""

from __future__ import annotations

import copy
import gzip
import json
import lzma
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import refinement_custody as custody
from devtools import refinement_house_links as houses
from devtools import refinement_packets as packets
from devtools import run_negative_controls as controls

SOURCE = packets.REPO


@pytest.fixture
def private(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    repo = tmp_path / "private"
    for source in packets.SOURCES.values():
        relative = source.packet.relative_to(SOURCE)
        shutil.copytree(source.packet, repo / relative)
    witness_root = repo / "packing/witnesses/known-best"
    witness_root.mkdir(parents=True)
    for n in houses.NUMBERS:
        (witness_root / f"n-{n:03d}.yaml").symlink_to(houses.house_path(n))
    monkeypatch.setattr(packets, "REPO", repo)
    monkeypatch.setattr(houses, "REPO", repo)
    monkeypatch.setattr(custody, "REPO", repo)
    monkeypatch.setattr(houses.house.confirmation, "REPO", repo)
    monkeypatch.setattr(houses, "METADATA", repo / houses.METADATA.relative_to(SOURCE))
    monkeypatch.setattr(custody, "INDEX", repo / custody.INDEX.relative_to(SOURCE))
    return repo


@pytest.mark.parametrize("n", houses.NUMBERS)
@pytest.mark.parametrize("field", ["side", "x", "source_metadata"])
def test_validly_shaped_source_fact_change_is_refused(
    private: Path, n: int, field: str
) -> None:
    assert private == packets.REPO
    source = houses.source(n)
    fact = packets.read_fact(source, n)
    if field == "side":
        fact["side"] = str(Fraction(fact["side"]) + 1)
    elif field == "x":
        fact["squares"][0]["x"] = str(Fraction(fact["squares"][0]["x"]) + 1)
    else:
        fact["source_metadata"]["method"] += " changed"
    packets.fact_path(source, n).write_bytes(gzip.compress(packets.json_bytes(fact), mtime=0))
    with pytest.raises(ValueError, match="independently pinned"):
        packets.read_fact(source, n)
    with pytest.raises(ValueError, match="independently pinned"):
        packets.to_witness(source, n)


def test_full_n68_decimal_preserves_the_improvement() -> None:
    side = Fraction(packets.read_fact(packets.N68, 68)["side"])
    older = Fraction("4399397618609141951332334459697/500000000000000000000000000000")
    assert Fraction(packets.exact_decimal(str(side))) == side < older
    assert Fraction("8.798795237218283903") > older


def test_all_deciding_inputs_bind_without_a_new_predicate(private: Path) -> None:
    assert private == packets.REPO
    value = json.loads(lzma.decompress(custody.INDEX.read_bytes()))
    custody.check_index(value)
    assert len(value["couzo_jobs"]) == 10
    assert len(value["n68_jobs"]) == 3
    houses.check_houses()


@pytest.mark.parametrize(
    "mutation",
    ["input", "missing", "pairs", "tiny-wall", "tiny-pair", "n68-route", "n68-input"],
)
def test_compact_admission_refuses_changed_full_protocol(private: Path, mutation: str) -> None:
    assert private == packets.REPO
    value = copy.deepcopy(json.loads(lzma.decompress(custody.INDEX.read_bytes())))
    if mutation == "input":
        value["couzo_jobs"][0]["input_sha256"] = "0" * 64
    elif mutation == "missing":
        value["couzo_jobs"].pop()
    elif mutation == "pairs":
        value["couzo_jobs"][0]["verdict"]["routes"]["independent"]["pairs_tested"] -= 1
    elif mutation == "tiny-wall":
        value["couzo_jobs"][4]["verdict"]["routes"]["exact_verify"][
            "minimum_containment_clearance"
        ] = "-1"
    elif mutation == "tiny-pair":
        value["couzo_jobs"][3]["verdict"]["routes"]["exact_verify"]["failures"] = []
    elif mutation == "n68-route":
        value["n68_jobs"][0]["routes"].pop()
    else:
        value["n68_jobs"][2]["input_sha256"] = "0" * 64
    with pytest.raises(ValueError, match=r"differs|required|lacks|admission"):
        custody.check_index(value)


def test_linked_house_producer_refuses_before_writing(private: Path) -> None:
    assert private == packets.REPO
    original = houses.house_path(105).read_bytes()
    with pytest.raises(ValueError, match="escapes"):
        houses.guard_house_outputs([105])
    assert houses.house_path(105).read_bytes() == original


def test_linked_house_changed_result_is_refused(private: Path) -> None:
    assert private == packets.REPO
    rows = json.loads(lzma.decompress(houses.METADATA.read_bytes()))
    rows[1]["metadata"]["certificate"]["result"]["minimum_best_pair_gap"] = "1"
    houses.METADATA.write_bytes(lzma.compress(packets.json_bytes(rows)))
    with pytest.raises(ValueError, match="actual complete replay"):
        houses.check_houses([105])


def test_linked_house_changed_complete_geometry_is_refused(
    private: Path, tmp_path: Path
) -> None:
    assert private == packets.REPO
    leaf = houses.house_path(292)
    changed = tmp_path / "changed.yaml"
    text = leaf.read_text()
    old = packets.to_witness(packets.COUZO, 292)["squares"][0]["corners"][0][0]
    changed.write_text(text.replace(old, str(Fraction(old) + 1), 1))
    leaf.unlink()
    leaf.symlink_to(changed)
    with pytest.raises(ValueError, match="complete refinement geometry"):
        houses.check_houses([292])


@pytest.mark.parametrize("change", ["limitations", "extra"])
def test_n68_certificate_result_cannot_claim_more(private: Path, change: str) -> None:
    assert private == packets.REPO
    rows = json.loads(lzma.decompress(houses.METADATA.read_bytes()))
    result = rows[0]["metadata"]["certificate"]["result"]
    if change == "limitations":
        result["limitations"] = "Global optimality has been proved."
    else:
        result["global_optimality"] = True
    with pytest.raises(ValueError, match="metadata differs"):
        houses.validate_metadata(68, rows[0]["metadata"])


@pytest.mark.slow
def test_production_snapshot_copies_complete_refinement_custody(tmp_path: Path) -> None:
    carried = {*controls.COPY_SEPARATELY, *controls.snapshot_pruned_targets()}
    assert set(houses.private_input_paths()) <= carried
    tree = tmp_path / "worker"
    controls.clone_tree(tree)
    for path in houses.private_input_paths():
        copied = tree / path.relative_to(SOURCE)
        assert copied.is_file()
        assert not copied.is_symlink()
        assert copied.read_bytes() == path.read_bytes()
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from devtools.refinement_house_links import check_houses; check_houses()",
        ],
        cwd=tree / controls.HERE,
        env=controls.control_environment(tree, tmp_path / "pycache"),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert controls.snapshot_source_bytes() <= controls.SNAPSHOT_MAX_BYTES
