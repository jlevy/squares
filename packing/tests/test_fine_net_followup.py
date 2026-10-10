"""The fine-net follow-up tool, on a small synthetic check2 release asset."""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
import stat
import sys
import tarfile
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import fine_net_followup as followup
from devtools.audit_wand125_declared_net import net_facts, semantic_digest

NAME = "mixed_n2_L3"
BUNDLE = "n2-L3-check2-bundle"
SOURCE = "0" * 64


def dumps(value: Any) -> bytes:
    return json.dumps(value, indent=1).encode()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def add(archive: tarfile.TarFile, name: str, data: bytes) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(data)
    archive.addfile(info, io.BytesIO(data))


def tarball(files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w:gz") as archive:
        for name, data in files.items():
            add(archive, name, data)
    return stream.getvalue()


def release(tmp_path: Path) -> tuple[Path, Path, bytes]:
    """A two-square check2 asset and its documents, laid out as the source's are."""
    candidate = {
        "n": 2,
        "L": "3",
        "B": "4999/5000",
        "proof_net": {"step": "1/5002", "last": 2072},
        "rectangles": [{"rectangle": ["0", "0", "3", "3"], "mass": "199999/100000"}],
        "points": [],
        "total_mass": "199999/100000",
    }
    raw = dumps(candidate)
    semantic = semantic_digest(candidate)
    facts = net_facts(Fraction(4999, 5000), Fraction(1, 5002), 2073)
    build = {"source_sha256": SOURCE, "target": "x86_64-unknown-linux-gnu"}
    receipt = dumps(
        {
            "status": "VERIFIED",
            "directions": 2073,
            "failed": 0,
            "candidate_digest": semantic,
            "file_sha256": digest(raw),
            "verifier": "sqverify-fast",
            "verifier_summary": {
                "status": "VERIFIED",
                "directions": 2073,
                "refused_directions": [],
                "threshold": "1",
                "fault_injected_at_box": None,
                "nodes": 1,
                "direction_cpu_seconds": 1.0,
                "threads": 1,
                "build": build,
                "premises": {
                    "L": "3",
                    "B": "4999/5000",
                    "D": "1/5002",
                    "angle_count": 2073,
                    "mass_exact": "199999/100000",
                    "format": "M",
                    "centre_domain": "per-bin",
                    "input_sha256": digest(raw),
                },
            },
        }
    )
    control = dumps(
        {
            "kind": "every mass times factor",
            "refused": True,
            "tries": [{"factor": "197/200", "status": "REFUSED", "exit": 1}],
        }
    )
    prepublication = dumps(
        {
            "status": "VERIFIED",
            "verdict": "PASS",
            "directions_verified": 2073,
            "directions_expected": 2073,
            "candidate_digest": semantic,
            "file_sha256": digest(raw),
            "input_sha256": digest(raw),
            "build": build,
            "seconds": 1,
            "control": {"status": "REFUSED", "refused_directions": 32},
        }
    )
    run = gzip.compress(b'{"r":0,"cpu_seconds":1.0,"verdict":"verified"}\n', mtime=0)
    bundle = dumps(
        {
            "schema": "fine-net-check2-v1",
            "n": 2,
            "L": "3",
            "B": "4999/5000",
            "proof_net": candidate["proof_net"],
            "angle_count": 2073,
            "total_mass": "199999/100000",
            "candidate_digest": semantic,
            "candidate_sha256": digest(raw),
            "receipt_sha256": digest(receipt),
            "net": {name: str(value) for name, value in facts.items()},
        }
    )
    sealed_readme, later_readme = b"# sealed\n", b"# sealed\n\nA later paragraph.\n"
    data = {
        "candidate.json": raw,
        "check2/control.json": control,
        "check2/receipt.json": receipt,
        "check2/run.jsonl.gz": run,
    }
    listed = {"README.md": digest(sealed_readme), "bundle.json": digest(bundle)}
    listed |= {name: digest(value) for name, value in data.items()}
    manifest = dumps(listed)
    inner = {"README.md": sealed_readme, "bundle.json": bundle, "files-sha256.json": manifest}
    inner |= data
    outer = data | {
        f"{BUNDLE}.tar.gz": tarball({f"{BUNDLE}/{k}": v for k, v in inner.items()}),
        "verification/prepublication-receipt.json": prepublication,
    }
    asset = tarball({f"certificates/{NAME}/{k}": v for k, v in outer.items()})
    documents = tmp_path / "documents"
    for name, value in (
        ("README.md", later_readme),
        ("bundle.json", bundle),
        ("files-sha256.json", manifest),
    ):
        (documents / name).parent.mkdir(parents=True, exist_ok=True)
        (documents / name).write_bytes(value)
    path = tmp_path / "asset.tar.gz"
    path.write_bytes(asset)
    return path, documents, asset


def premises_argv(tmp_path: Path, asset: Path, documents: Path, data: bytes) -> list[str]:
    return [
        "premises",
        *("--asset", str(asset), "--sha256", digest(data), "--bytes", str(len(data))),
        *("--documents", str(documents), "--name", NAME, "--n", "2", "--side", "3"),
        *("--work", str(tmp_path / "work"), "--out", str(tmp_path / "premises.json")),
    ]


def test_the_premises_of_a_complete_asset_hold(tmp_path: Path) -> None:
    asset, documents, data = release(tmp_path)
    assert followup.main(premises_argv(tmp_path, asset, documents, data)) == 0
    receipt = json.loads((tmp_path / "premises.json").read_text())
    assert receipt["status"] == "EXACT_PREMISES_HOLD"
    assert receipt["maintained_input_premises"]["directions"] == 2073
    assert all(receipt["maintained_input_premises"]["checks"].values())
    assert receipt["sealed_bundle"]["listed_hashes_matching"] == 6
    assert receipt["sealed_bundle"]["repeated_payloads"] == [
        "candidate.json",
        "check2/control.json",
        "check2/receipt.json",
        "check2/run.jsonl.gz",
    ]
    assert receipt["readme_editions"]["different"] is True
    assert set(receipt["pinned_only"]) == {
        f"certificates/{NAME}/check2/run.jsonl.gz",
        f"certificates/{NAME}/{BUNDLE}.tar.gz",
    }


def test_an_asset_that_is_not_the_pinned_one_is_refused(tmp_path: Path) -> None:
    asset, documents, data = release(tmp_path)
    argv = premises_argv(tmp_path, asset, documents, data)
    argv[argv.index("--sha256") + 1] = "f" * 64
    assert followup.main(argv) == 1
    assert not (tmp_path / "premises.json").exists()


def test_a_document_the_asset_also_holds_is_refused(tmp_path: Path) -> None:
    asset, documents, data = release(tmp_path)
    (documents / "candidate.json").write_bytes(b"{}")
    assert followup.main(premises_argv(tmp_path, asset, documents, data)) == 1


def test_a_listed_file_that_changed_is_refused(tmp_path: Path) -> None:
    asset, documents, data = release(tmp_path)
    (documents / "bundle.json").write_bytes((documents / "bundle.json").read_bytes() + b" ")
    assert followup.main(premises_argv(tmp_path, asset, documents, data)) == 1


def test_the_price_takes_the_larger_of_its_two_estimates() -> None:
    rows = [{"r": 0, "process_cpu_seconds": 2.0}, {"r": 1, "process_cpu_seconds": 4.0}]
    price = followup.price(rows, {0: 1.0, 1: 2.0, 2: 3.0}, 3, 2)
    assert price["ratio_to_source"] == 2.0
    assert price["full_capture_cpu_seconds_by_ratio"] == 12.0
    assert price["full_capture_cpu_seconds_by_mean"] == 9.0
    assert price["full_capture_cpu_seconds"] == 12.0
    assert price["controls_cpu_seconds"] == 20.0
    assert price["total_cpu_seconds"] == 32.0
    assert price["total_wall_seconds_at_workers"] == 16.0
    assert price["full_capture_within_limit"] is True
    assert followup.price(rows, {}, 2073, 2)["full_capture_within_limit"] is False


FAKE = """\
import json, sys
r = int(sys.argv[sys.argv.index("--directions") + 1])
print(json.dumps({"r": r, "verdict": VERDICT, "cpu_seconds": 0.5, "nodes": 3}))
print(json.dumps({"kind": "sqverify-fast-summary/v1", "status": "PARTIAL", "build": {}}))
sys.exit(0 if VERDICT == "verified" else 1)
"""


def fake_binary(tmp_path: Path, verdict: str) -> Path:
    path = tmp_path / f"fake-{verdict}"
    body = FAKE.replace("VERDICT", repr(verdict))
    path.write_text(f"#!{sys.executable}\n{body}")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


@pytest.mark.parametrize(
    ("verdict", "code"), [("verified", 0), ("counterexample-candidate", 1)]
)
def test_a_sample_is_a_diagnostic_of_the_directions_it_ran(
    tmp_path: Path, verdict: str, code: int
) -> None:
    asset, documents, data = release(tmp_path)
    assert followup.main(premises_argv(tmp_path, asset, documents, data)) == 0
    candidate = tmp_path / "work/certificates" / NAME / "candidate.json"
    out = tmp_path / "sample.json"
    argv = ["sample", "--binary", str(fake_binary(tmp_path, verdict))]
    argv += ["--candidate", str(candidate), "--n", "2", "--side", "3"]
    argv += ["--directions", "2072,0", "--workers", "2", "--out", str(out)]
    assert followup.main(argv) == code
    receipt = json.loads(out.read_text())
    assert receipt["directions"] == [0, 2072]
    assert [row["r"] for row in receipt["rows"]] == [0, 2072]
    assert receipt["status"] == ("DIAGNOSTIC_SAMPLE" if code == 0 else "SAMPLE_REFUSED")
    assert receipt["price"]["net_directions"] == 2073
    assert "not a replay" in receipt["scope"]
    assert os.access(out, os.R_OK)


def test_a_sample_off_the_net_or_with_three_workers_is_refused(tmp_path: Path) -> None:
    asset, documents, data = release(tmp_path)
    assert followup.main(premises_argv(tmp_path, asset, documents, data)) == 0
    candidate = tmp_path / "work/certificates" / NAME / "candidate.json"
    binary = fake_binary(tmp_path, "verified")
    for directions, workers in (("2073", "1"), ("0", "3")):
        argv = ["sample", "--binary", str(binary), "--candidate", str(candidate)]
        argv += ["--n", "2", "--side", "3", "--directions", directions]
        argv += ["--workers", workers, "--out", str(tmp_path / "refused.json")]
        assert followup.main(argv) == 1
