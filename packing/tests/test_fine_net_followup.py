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


def release(
    tmp_path: Path, *, embedded: bool = False, schema: str = "fine-net-check2-receipt/v1"
) -> tuple[Path, Path, bytes]:
    """A two-square check2 asset and its documents, laid out as the source's are.

    ``embedded`` gives the pre-publication receipt the ``fine-net-check2-receipt/v1``
    shape of 10 October's n = 30 certificate, or the other ``schema`` given: the very run
    record the check2 receipt embeds, with ``verifier`` in place of ``build`` and a
    control with tries.
    """
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
    record = {
        "schema": schema,
        "status": "VERIFIED",
        "verdict": "PASS",
        "directions_verified": 2073,
        "directions_expected": 2073,
        "candidate_digest": semantic,
        "file_sha256": digest(raw),
        "input_sha256": digest(raw),
        "verifier": build,
        "seconds": 1,
        "control": {
            "refused": True,
            "tries": [{"factor": "197/200", "status": "REFUSED", "exit": 1, "refused": 32}],
        },
    }
    receipt = dumps(
        ({"receipt": record} if embedded else {})
        | {
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
        record
        if embedded
        else {
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
    assert receipt["prepublication"]["shape"] == "build"
    assert receipt["prepublication"]["check2_embeds_a_run_record"] is False
    assert receipt["prepublication"]["identical_to_the_embedded_run_record"] is False


def test_the_premises_of_an_asset_with_the_n30_receipt_shape_hold(tmp_path: Path) -> None:
    """The n = 30 shape, ``fine-net-check2-receipt/v1``: the check2 reader takes the build
    from ``verifier`` and the control's refused directions from its one try."""
    asset, documents, data = release(tmp_path, embedded=True)
    assert followup.main(premises_argv(tmp_path, asset, documents, data)) == 0
    receipt = json.loads((tmp_path / "premises.json").read_text())
    assert receipt["status"] == "EXACT_PREMISES_HOLD"
    check = receipt["check2_audit"]["prepublication_check"]
    assert check["target"] == "x86_64-unknown-linux-gnu"
    assert check["control_refused_directions"] == 32
    assert receipt["prepublication"]["shape"] == "fine-net-check2-receipt/v1"
    assert receipt["prepublication"]["check2_embeds_a_run_record"] is True
    assert receipt["prepublication"]["identical_to_the_embedded_run_record"] is True


def test_a_receipt_shape_the_check2_reader_does_not_take_is_recorded_refused(
    tmp_path: Path,
) -> None:
    """A schema the reader does not know: its refusal is recorded in the receipt, not a
    crash, and the custody checks still run."""
    asset, documents, data = release(
        tmp_path, embedded=True, schema="fine-net-check2-receipt/v2"
    )
    assert followup.main(premises_argv(tmp_path, asset, documents, data)) == 1
    receipt = json.loads((tmp_path / "premises.json").read_text())
    assert receipt["status"] == followup.CHECK2_READER_REFUSED
    assert receipt["check2_audit"]["refusal"] == (
        "AuditError: no reader for pre-publication schema fine-net-check2-receipt/v2"
    )
    assert receipt["claim"] == "s(2) >= 3/1"
    assert receipt["sealed_bundle"]["listed_hashes_matching"] == 6
    assert receipt["prepublication"]["shape"] == "fine-net-check2-receipt/v2"
    assert receipt["prepublication"]["check2_embeds_a_run_record"] is True
    assert receipt["prepublication"]["identical_to_the_embedded_run_record"] is True


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


def test_a_work_directory_the_tool_did_not_make_is_never_cleared(tmp_path: Path) -> None:
    asset, documents, data = release(tmp_path)
    argv = premises_argv(tmp_path, asset, documents, data)
    work = Path(argv[argv.index("--work") + 1])
    work.mkdir()
    keep = work / "uncommitted.txt"
    keep.write_text("someone's work")
    assert followup.main(argv) == 1
    assert keep.read_text() == "someone's work"
    keep.unlink()
    assert followup.main(argv) == 0
    assert (work / followup.WORK_MARKER).is_file()
    assert followup.main(argv) == 0


def test_a_direction_that_runs_past_its_timeout_is_killed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    binary = tmp_path / "hangs"
    binary.write_text(f"#!{sys.executable}\nimport time\ntime.sleep(60)\n")
    binary.chmod(binary.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setattr(followup, "DIRECTION_TIMEOUT", 0.2)
    with pytest.raises(followup.AuditError, match="ran past"):
        followup.direction(binary, tmp_path / "candidate.json", 2, "3", 0)


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


# --------------------------------------------------------------------------- linear

LINEAR = "mixed_n3_L4"
PROOF = "n3-L4-proof-bundle.tar.gz"


def linear_release(tmp_path: Path, *, bundles: int = 1) -> tuple[Path, Path, bytes]:
    """A linear asset (candidate, certificate, proof bundle) and its pinned documents."""
    outer = {"candidate.json": b"{}", "certificate.json": dumps({"results": {}})}
    for k in range(bundles):
        name = PROOF if k == 0 else f"extra{k}-proof-bundle.tar.gz"
        outer[name] = tarball({f"{name.removesuffix('.tar.gz')}/summary.json": b"{}"})
    asset = tarball({f"certificates/{LINEAR}/{k}": v for k, v in outer.items()})
    documents = tmp_path / "documents"
    for name in ("README.md", "manifest.json", "completion-audit.json", "code/checker.cpp"):
        (documents / name).parent.mkdir(parents=True, exist_ok=True)
        (documents / name).write_bytes(name.encode())
    path = tmp_path / "linear.tar.gz"
    path.write_bytes(asset)
    return path, documents, asset


def linear_argv(tmp_path: Path, asset: Path, documents: Path, data: bytes) -> list[str]:
    return [
        *("--asset", str(asset), "--sha256", digest(data), "--bytes", str(len(data))),
        *("--documents", str(documents), "--name", LINEAR, "--n", "3", "--side", "4"),
        *("--orbits", "1,2,3", "--candidate-digest", "c" * 64, "--bundle", PROOF),
        *("--work", str(tmp_path / "work"), "--out", str(tmp_path / "linear.json")),
    ]


def test_a_linear_asset_is_prepared_with_every_digest_by_upstream_path(
    tmp_path: Path,
) -> None:
    asset, documents, data = linear_release(tmp_path)
    directory, asset_files, laid, tree, bundle = followup.linear_prepare(
        asset,
        sha256=digest(data),
        size=len(data),
        documents=documents,
        name=LINEAR,
        work=tmp_path / "work",
    )
    assert asset_files == ["candidate.json", "certificate.json", PROOF]
    assert laid == ["README.md", "code/checker.cpp", "completion-audit.json", "manifest.json"]
    assert bundle == PROOF
    root = Path("certificates", LINEAR)
    assert set(tree) == {root / name for name in (*asset_files, *laid)}
    assert tree[root / "code/checker.cpp"] == digest(b"code/checker.cpp")
    assert tree[root / PROOF] == followup.file_digest(directory / PROOF)


def test_a_linear_asset_with_two_proof_bundles_is_refused(tmp_path: Path) -> None:
    asset, documents, data = linear_release(tmp_path, bundles=2)
    with pytest.raises(followup.AuditError, match="2 proof bundles"):
        followup.linear_prepare(
            asset,
            sha256=digest(data),
            size=len(data),
            documents=documents,
            name=LINEAR,
            work=tmp_path / "work",
        )


def test_linear_premises_hand_the_maintained_readers_the_asset_and_documents(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The T-080 route's readers get the five files, every digest and all 201 angles;
    their verdicts are theirs, so they are stubbed here and tested with the route."""
    calls: dict[str, Any] = {}

    def certificate(stated: Any, files: dict[str, bytes], tree: dict[Path, str]) -> Any:
        calls["certificate"] = (stated, sorted(files), tree)
        return {"status": "read"}

    def unpack(_stated: Any, archive: Path, into: Path) -> Path:
        calls["unpack"] = archive.name
        return into

    def bindings(*_args: Any) -> dict[str, Any]:
        return {"status": "BUNDLE_BOUND_TO_PACKET", "files": 1}

    def inputs(_root: Path, sha: str, indices: Any, _shipped: Any) -> dict[str, Any]:
        calls["inputs"] = (sha, list(indices))
        return {"status": "ALL_INPUTS_ENCLOSE_THE_CANDIDATE"}

    monkeypatch.setattr(followup.linear, "linear_certificate", certificate)
    monkeypatch.setattr(followup.mixed, "unpack_bundle", unpack)
    monkeypatch.setattr(followup.linear, "bundle_bindings", bindings)
    monkeypatch.setattr(followup.linear, "check_inputs", inputs)
    asset, documents, data = linear_release(tmp_path)
    argv = ["linear-premises", *linear_argv(tmp_path, asset, documents, data)]
    assert followup.main(argv) == 0
    receipt = json.loads((tmp_path / "linear.json").read_text())
    assert receipt["status"] == "EXACT_PREMISES_HOLD"
    assert receipt["claim"] == "s(3) >= 4/1"
    stated, names, tree = calls["certificate"]
    counts = (stated.n, stated.side, stated.points, stated.segments, stated.rectangles)
    assert counts == (3, Fraction(4), 1, 2, 3)
    assert names == sorted(followup.mixed.MIXED_FILES)
    assert len(names) == 5
    assert Path("certificates", LINEAR, "code/checker.cpp") in tree
    assert calls["unpack"] == PROOF
    assert calls["inputs"] == (digest(b"{}"), list(range(201)))
    assert receipt["bundle"]["sha256"] == tree[Path("certificates", LINEAR, PROOF)]


def test_a_linear_asset_shipping_another_bundle_than_stated_is_refused(
    tmp_path: Path,
) -> None:
    asset, documents, data = linear_release(tmp_path)
    argv = linear_argv(tmp_path, asset, documents, data)
    argv[argv.index("--bundle") + 1] = "n3-L5-proof-bundle.tar.gz"
    assert followup.main(["linear-premises", *argv]) == 1
    assert not (tmp_path / "linear.json").exists()


def test_a_linear_sample_off_the_net_or_with_three_workers_is_refused(
    tmp_path: Path,
) -> None:
    asset, documents, data = linear_release(tmp_path)
    for directions, workers in (("201", "1"), ("37", "3")):
        argv = ["linear-sample", *linear_argv(tmp_path, asset, documents, data)]
        argv += ["--directions", directions, "--workers", workers]
        assert followup.main(argv) == 1
    assert not (tmp_path / "work").exists()


def test_the_linear_price_takes_the_larger_estimate_and_the_costliest_angle() -> None:
    rows = [{"index": 1, "cpu_seconds": 2.0}, {"index": 2, "cpu_seconds": 4.0}]
    seconds = {0: 10.0, 1: 1.0, 2: 2.0, 3: 3.0}
    nodes = {0: 100, 1: 10, 2: 20, 3: 5}
    price = followup.linear_price(rows, seconds, nodes, 2)
    assert price["ratio_to_source"] == 2.0
    assert price["full_replay_cpu_seconds_by_ratio"] == 32.0
    assert price["full_replay_cpu_seconds_by_nodes"] == 27.0
    assert price["full_replay_cpu_seconds"] == 32.0
    assert price["control_angle"] == 3
    assert price["control_cpu_seconds"] == 18.0
    assert price["total_cpu_seconds"] == 50.0
    assert price["costliest_angle"] == 0
    assert price["total_wall_seconds_at_workers"] == 25.0
    assert price["full_replay_within_limit"] is True


def retained_asset(tmp_path: Path) -> tuple[Path, bytes]:
    """An asset with one member of each kind `retain` distinguishes."""
    lines = b"".join(b'{"row": %d}\n' % index for index in range(1200))
    members = {
        "candidate.json": lines,
        "check2/receipt.json": dumps({"status": "VERIFIED"}),
        "check2/run.jsonl.gz": gzip.compress(b'{"r":0}\n', mtime=0),
        "check2/src/sqverify-proof-net-fe12e036c.tar.gz": tarball({"src/lib.rs": b"//\n"}),
        f"{BUNDLE}.tar.gz": tarball({f"{BUNDLE}/README.md": b"# sealed\n"}),
    }
    data = tarball({f"certificates/{NAME}/{k}": v for k, v in members.items()})
    path = tmp_path / f"certificates__{NAME}.tar.gz"
    path.write_bytes(data)
    return path, data


def retain_argv(tmp_path: Path, asset: Path, data: bytes, packet: Path) -> list[str]:
    return [
        "retain",
        *("--asset", str(asset), "--sha256", digest(data), "--bytes", str(len(data))),
        *("--name", NAME, "--packet", str(packet), "--work", str(tmp_path / "work")),
        *("--release", "lower-bounds-v1", "--repository", "someone/square-packing"),
    ]


def test_retain_keeps_the_data_members_and_pins_the_verifier_and_the_bundle(
    tmp_path: Path,
) -> None:
    asset, data = retained_asset(tmp_path)
    packet = tmp_path / "packet"
    assert followup.main(retain_argv(tmp_path, asset, data, packet)) == 0
    stored = packet / "release/certificates" / NAME
    assert sorted(
        p.relative_to(stored).as_posix() for p in stored.rglob("*") if p.is_file()
    ) == [
        "candidate.json.gz",
        "check2/receipt.json",
        "check2/run.jsonl.gz",
    ]
    record = json.loads((packet / followup.RETAINED_RECORD).read_text())
    (entry,) = record["assets"]
    forms = {row["path"].split(f"{NAME}/")[1]: row.get("form") for row in entry["members"]}
    assert forms == {
        "candidate.json": "gzip",
        "check2/receipt.json": "plain",
        "check2/run.jsonl.gz": "original-gzip",
        "check2/src/sqverify-proof-net-fe12e036c.tar.gz": None,
        f"{BUNDLE}.tar.gz": None,
    }
    assert all("pinned_only" in row for row in entry["members"] if row.get("form") is None)
    assert gzip.decompress((stored / "candidate.json.gz").read_bytes()).count(b"\n") == 1200
    assert followup.check_retained(packet) == []
    # Retaining the same asset again changes nothing.
    before = (packet / followup.RETAINED_RECORD).read_bytes()
    assert followup.main(retain_argv(tmp_path, asset, data, packet)) == 0
    assert (packet / followup.RETAINED_RECORD).read_bytes() == before


def test_check_retained_reports_changed_stray_and_misnamed_members(tmp_path: Path) -> None:
    asset, data = retained_asset(tmp_path)
    packet = tmp_path / "packet"
    assert followup.main(retain_argv(tmp_path, asset, data, packet)) == 0
    stored = packet / "release/certificates" / NAME
    (stored / "check2/receipt.json").write_bytes(b"{}\n")
    (stored / "stray.json").write_bytes(b"{}\n")
    document = packet / "upstream/certificates" / NAME / "ASSET.json"
    document.parent.mkdir(parents=True)
    named = {"asset": asset.name, "size": len(data), "sha256": "0" * 64}
    document.write_text(json.dumps({"assets": [named]}))
    problems = followup.check_retained(packet)
    assert any("check2/receipt.json differs" in problem for problem in problems)
    assert any("stray.json is not in" in problem for problem in problems)
    assert any("is not the asset" in problem for problem in problems)
    assert followup.main(["check-retained", str(packet)]) == 1


def test_retain_refuses_an_asset_that_is_not_the_pinned_one(tmp_path: Path) -> None:
    asset, data = retained_asset(tmp_path)
    packet = tmp_path / "packet"
    argv = retain_argv(tmp_path, asset, data, packet)
    argv[argv.index("--sha256") + 1] = "f" * 64
    assert followup.main(argv) == 1
    assert not (packet / followup.RETAINED_RECORD).exists()


@pytest.mark.parametrize(
    "linked", ["release", "acquisition", f"release/certificates/{NAME}/check2"]
)
def test_retain_refuses_linked_parents_before_any_member_publication(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], linked: str
) -> None:
    asset, data = retained_asset(tmp_path)
    packet, outside = tmp_path / "packet", tmp_path / "outside"
    packet.mkdir()
    outside.mkdir()
    (outside / "sentinel").write_bytes(b"outside bytes must survive")
    if linked == "acquisition":
        (outside / "release-assets.json").write_text(
            json.dumps(
                {
                    "format": followup.RETAINED_FORMAT,
                    "repository": "someone/square-packing",
                    "release": "lower-bounds-v1",
                    "retained_dir": "release",
                    "assets": [],
                }
            )
        )
    parent = packet / linked
    parent.parent.mkdir(parents=True, exist_ok=True)
    parent.symlink_to(outside, target_is_directory=True)
    before = {p.relative_to(outside): p.read_bytes() for p in outside.rglob("*")}

    assert followup.main(retain_argv(tmp_path, asset, data, packet)) == 1
    assert {p.relative_to(outside): p.read_bytes() for p in outside.rglob("*")} == before
    assert not [p for p in packet.rglob("*") if p.is_file()]
    assert parent.is_symlink()
    output = capsys.readouterr()
    assert "symlink" in output.err
    assert "members retained" not in output.out


@pytest.mark.parametrize(
    "linked", ["release", "acquisition", f"release/certificates/{NAME}/check2"]
)
def test_check_retained_refuses_linked_parents(tmp_path: Path, linked: str) -> None:
    asset, data = retained_asset(tmp_path)
    packet, outside = tmp_path / "packet", tmp_path / "outside"
    assert followup.main(retain_argv(tmp_path, asset, data, packet)) == 0
    parent = packet / linked
    parent.rename(outside)
    parent.symlink_to(outside, target_is_directory=True)
    before = {p.relative_to(outside): p.read_bytes() for p in outside.rglob("*") if p.is_file()}

    problems = followup.check_retained(packet)
    assert any("symlink" in problem for problem in problems), problems
    assert {
        p.relative_to(outside): p.read_bytes() for p in outside.rglob("*") if p.is_file()
    } == before


def test_retain_refuses_a_linked_packet_root_before_extraction(tmp_path: Path) -> None:
    asset, data = retained_asset(tmp_path)
    packet, outside = tmp_path / "packet", tmp_path / "outside"
    outside.mkdir()
    (outside / "sentinel").write_bytes(b"untouched")
    packet.symlink_to(outside, target_is_directory=True)

    assert followup.main(retain_argv(tmp_path, asset, data, packet)) == 1
    assert sorted(p.name for p in outside.iterdir()) == ["sentinel"]
    assert (outside / "sentinel").read_bytes() == b"untouched"
    assert not (tmp_path / "work").exists()


def test_member_publication_rechecks_the_manifest_parent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    asset, data = retained_asset(tmp_path)
    packet, outside = tmp_path / "packet", tmp_path / "outside"
    outside.mkdir()
    (outside / "sentinel").write_bytes(b"untouched")
    compress = followup.compress

    def link_manifest_parent(path: Path) -> Path:
        result = compress(path)
        (packet / "acquisition").symlink_to(outside, target_is_directory=True)
        return result

    monkeypatch.setattr(followup, "compress", link_manifest_parent)
    assert followup.main(retain_argv(tmp_path, asset, data, packet)) == 1
    assert sorted(p.name for p in outside.iterdir()) == ["sentinel"]
    assert (outside / "sentinel").read_bytes() == b"untouched"
    assert not list((packet / "release").rglob("*.json*"))
    assert not list((packet / "release").rglob(".retain-*"))


@pytest.mark.parametrize("collision", ["plain", "matching-plain", "gzip", "both", "receipt"])
def test_retain_refuses_collisions_before_writing_any_packet_member(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], collision: str
) -> None:
    asset, data = retained_asset(tmp_path)
    packet = tmp_path / "packet"
    stored = packet / "release/certificates" / NAME
    stored.mkdir(parents=True)
    plain = stored / "candidate.json"
    packed = stored / "candidate.json.gz"
    with tarfile.open(asset) as archive:
        stream = archive.extractfile(f"certificates/{NAME}/candidate.json")
        assert stream is not None
        candidate = stream.read()
    if collision in {"plain", "both"}:
        plain.write_bytes(b"previous candidate")
    elif collision == "matching-plain":
        plain.write_bytes(candidate)
    if collision in {"gzip", "both"}:
        packed.write_bytes(
            gzip.compress(candidate if collision == "both" else b"previous candidate", mtime=0)
        )
    if collision == "receipt":
        receipt = stored / "check2/receipt.json"
        receipt.parent.mkdir()
        receipt.write_bytes(b"previous receipt")
    before = {p.relative_to(packet): p.read_bytes() for p in packet.rglob("*") if p.is_file()}

    assert followup.main(retain_argv(tmp_path, asset, data, packet)) == 1
    assert {
        p.relative_to(packet): p.read_bytes() for p in packet.rglob("*") if p.is_file()
    } == before
    assert not (packet / followup.RETAINED_RECORD).exists()
    output = capsys.readouterr()
    assert "members retained" not in output.out
    assert (
        "move it aside" if "plain" in collision or collision == "both" else "other bytes"
    ) in output.err


def test_interrupted_manifest_publication_preserves_the_previous_complete_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    asset, data = retained_asset(tmp_path)
    packet = tmp_path / "packet"
    assert followup.main(retain_argv(tmp_path, asset, data, packet)) == 0
    record = packet / followup.RETAINED_RECORD
    before = record.read_bytes()
    capsys.readouterr()
    renamed = asset.with_name("another-asset.tar.gz")
    asset.rename(renamed)
    write_text = Path.write_text

    def interrupted(path: Path, text: str, *args: Any, **kwargs: Any) -> int:
        if path.name.startswith(record.name):
            write_text(path, '{"assets":', *args, **kwargs)
            raise OSError("injected interrupted manifest publication")
        return write_text(path, text, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(Path, "write_text", interrupted)
        with pytest.raises(OSError, match="injected interrupted manifest"):
            followup.main(retain_argv(tmp_path, renamed, data, packet))
    assert record.read_bytes() == before
    assert len(json.loads(record.read_bytes())["assets"]) == 1
    assert followup.check_retained(packet) == []
    assert "members retained" not in capsys.readouterr().out
    # The failed publication remains retryable without losing the older asset's row.
    assert followup.main(retain_argv(tmp_path, renamed, data, packet)) == 0
    assert len(json.loads(record.read_bytes())["assets"]) == 2


def test_interrupted_compression_leaves_no_candidate_or_staging_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    asset, data = retained_asset(tmp_path)
    packet = tmp_path / "packet"

    def interrupted(path: Path) -> Path:
        path.with_name(path.name + ".gz").write_bytes(b"incomplete gzip")
        raise OSError("injected interrupted compression")

    monkeypatch.setattr(followup, "compress", interrupted)
    with pytest.raises(OSError, match="injected interrupted compression"):
        followup.main(retain_argv(tmp_path, asset, data, packet))
    assert not list((packet / "release").rglob("*.json*"))
    assert not list((packet / "release").rglob(".retain-*"))
    assert not (packet / followup.RETAINED_RECORD).exists()
    assert "members retained" not in capsys.readouterr().out


@pytest.mark.parametrize("suffix", [".json", ".json.gz"])
def test_a_candidate_appearing_during_compression_is_never_replaced(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    suffix: str,
) -> None:
    asset, data = retained_asset(tmp_path)
    packet = tmp_path / "packet"
    target = packet / "release/certificates" / NAME / f"candidate{suffix}"
    compress = followup.compress

    def competing_write(path: Path) -> Path:
        target.write_bytes(b"another writer's candidate")
        return compress(path)

    monkeypatch.setattr(followup, "compress", competing_write)
    assert followup.main(retain_argv(tmp_path, asset, data, packet)) == 1
    assert target.read_bytes() == b"another writer's candidate"
    assert not list(target.parent.glob(".retain-*"))
    assert not (packet / followup.RETAINED_RECORD).exists()
    output = capsys.readouterr()
    assert "appeared while retaining" in output.err
    assert "members retained" not in output.out


@pytest.mark.parametrize("kind", ["directory", "symlink", "broken-symlink"])
def test_retain_refuses_a_nonregular_manifest_before_publishing_members(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], kind: str
) -> None:
    asset, data = retained_asset(tmp_path)
    packet = tmp_path / "packet"
    record = packet / followup.RETAINED_RECORD
    record.parent.mkdir(parents=True)
    other = tmp_path / "other.json"
    if kind == "directory":
        record.mkdir()
    else:
        if kind == "symlink":
            other.write_bytes(b"another record")
        record.symlink_to(other)
    assert followup.main(retain_argv(tmp_path, asset, data, packet)) == 1
    assert not (packet / "release").exists()
    assert record.is_dir() if kind == "directory" else record.is_symlink()
    if kind == "symlink":
        assert other.read_bytes() == b"another record"
    output = capsys.readouterr()
    assert "not a regular file; move it aside" in output.err
    assert "members retained" not in output.out
