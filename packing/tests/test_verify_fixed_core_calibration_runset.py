"""Synthetic mutation controls for retained BC329 run-set evidence plumbing."""

# These tests exercise the verifier's retained-byte seams without a calibration run.
# ruff: noqa: SLF001
# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import io
import json
import subprocess
import tarfile
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest

from devtools import run_fixed_core_calibration_profiles as coordinator
from devtools import verify_fixed_core_calibration_runset as verifier

EXECUTION = "a" * 40
READER = "b" * 40


def _write_json(path: Path, value: object) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, sort_keys=True, allow_nan=False) + "\n").encode()
    path.write_bytes(data)
    return data


def _identity(revision: str, order: int) -> dict[str, object]:
    return {
        "implementation_revision": revision,
        "requested_workers": 4,
        "calibration_seconds": 5400,
        "external_seconds": 7200,
        "termination_grace_seconds": 2,
        "monotonic_origin": float(order),
        "calibration_deadline_monotonic": float(order + 5400),
        "external_deadline_monotonic": float(order + 7200),
        "run_order": order,
        "cache_observation": "warm",
        "background_load": "idle",
    }


def _root(base: Path, revision: str = EXECUTION) -> tuple[Path, Path, Path, dict[str, object]]:
    repository = base / "repository"
    repository.mkdir(parents=True)
    run_root = base / "run"
    review_root = base / "review"
    run_root.mkdir()
    review_root.mkdir()
    runs: list[dict[str, object]] = []
    for order in verifier.RUN_ORDERS:
        profile = run_root / f"profile-{order}"
        profile.mkdir()
        (profile / "raw-directions").mkdir()
        (profile / "raw-directions" / "0.json").write_bytes(b"{}\n")
        receipt = _write_json(profile / "result.json", {"sources": {}})
        (run_root / f"profile-{order}-run.json").write_bytes(b"{}\n")
        for stem in (
            f"profile-{order}",
            f"profile-{order}-producer-readback",
            f"profile-{order}-inventory-readback",
        ):
            argv = ("synthetic-command", stem)
            coordinator._write_command_output(
                run_root,
                stem,
                argv,
                subprocess.CompletedProcess(argv, 0, f"{stem}\n".encode(), b""),
            )
        runs.append(
            {
                "run_order": order,
                "profile_directory": str(profile),
                "invocation_identity": _identity(revision, order),
                "calibration_receipt": {
                    "path": "result.json",
                    "bytes": len(receipt),
                    "sha256": hashlib.sha256(receipt).hexdigest(),
                },
                "command_wall_seconds": 1.0,
                "inventory": {},
            }
        )
    summary: dict[str, object] = {
        "schema": verifier.SUMMARY_SCHEMA,
        "evidence_scope": "target-free synthetic control",
        "execution_revision": revision,
        "frozen_tuple": {},
        "settings": {},
        "runs": runs,
        "metrics": {},
    }
    _write_json(run_root / verifier.SUMMARY_NAME, summary)
    (review_root / "coordinator.status").write_bytes(b"0\n")
    verifier.snapshot_run_root(
        run_root=run_root, review_root=review_root, execution_revision=revision
    )
    return repository, run_root, review_root, summary


def _proof(run: dict[str, object], order: int, revision: str = EXECUTION) -> dict[str, object]:
    return {
        "schema": verifier.READER_SCHEMA,
        "status": "accepted",
        "evidence_scope": "source-distinct synthetic control",
        "execution_revision": revision,
        "reader_revision": READER,
        "run_order": order,
        "profile_directory": run["profile_directory"],
        "invocation_identity": run["invocation_identity"],
        "receipt": run["calibration_receipt"],
        "fixture": {},
        "route_digests": {},
        "interval_boxes_observed": 1,
        "resources": {},
        "worker_topology": {},
        "artifacts": {},
        "limitations": "synthetic control",
    }


def _read_all(
    repository: Path,
    run_root: Path,
    review_root: Path,
    summary: dict[str, object],
    revision: str = EXECUTION,
) -> None:
    runs = cast(list[dict[str, object]], summary["runs"])
    for order, run in zip(verifier.RUN_ORDERS, runs, strict=True):
        proof = _proof(run, order, revision)
        output = (json.dumps(proof, sort_keys=True) + "\n").encode()
        status = verifier.run_reader(
            repository=repository,
            run_root=run_root,
            review_root=review_root,
            execution_revision=revision,
            reader_revision=READER,
            run_order=order,
            runner=lambda argv, data=output: subprocess.CompletedProcess(argv, 0, data, b""),
        )
        assert status == 0


def _reseal_proof(review_root: Path, order: int, data: bytes) -> None:
    command_name, stdout_name, _, _ = verifier._reader_names(order)
    (review_root / stdout_name).write_bytes(data)
    command_path = review_root / command_name
    command = json.loads(command_path.read_text())
    command["stdout"] = {
        "path": stdout_name,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    _write_json(command_path, command)


def _join(
    repository: Path, run_root: Path, review_root: Path, revision: str = EXECUTION
) -> dict[str, object]:
    return verifier.join_reader_proofs(
        repository=repository,
        run_root=run_root,
        review_root=review_root,
        execution_revision=revision,
        reader_revision=READER,
    )


def _complete_review_root(review_root: Path) -> None:
    for name in verifier.REVIEW_NAMES:
        path = review_root / name
        if not path.exists():
            path.write_bytes(b"synthetic observation\n")


def test_reader_join_and_retention_preserve_exact_run_root(tmp_path: Path) -> None:
    repository, run_root, review_root, summary = _root(tmp_path)
    top_level = {path.name for path in run_root.iterdir() if path.is_file()}
    assert len(top_level) == 22
    assert top_level == verifier.COORDINATOR_TOP_LEVEL_FILES
    _read_all(repository, run_root, review_root, summary)
    admission = _join(repository, run_root, review_root)
    assert admission["status"] == "accepted"
    assert [row["run_order"] for row in cast(list[dict[str, object]], admission["runs"])] == [
        1,
        2,
        3,
    ]
    _complete_review_root(review_root)
    evidence_root = tmp_path / "evidence"
    retained = verifier.retain_run_root(
        run_root=run_root,
        review_root=review_root,
        evidence_root=evidence_root,
        execution_revision=EXECUTION,
    )
    assert retained["status"] == "accepted"
    assert (evidence_root / verifier.SUMMARY_NAME).read_bytes() == (
        run_root / verifier.SUMMARY_NAME
    ).read_bytes()
    assert (evidence_root / verifier.INVENTORY_NAME).read_bytes() == (
        review_root / verifier.INVENTORY_NAME
    ).read_bytes()


def test_snapshot_refuses_shared_invalid_invocation_identity(tmp_path: Path) -> None:
    for field, value in (
        ("requested_workers", True),
        ("requested_workers", 5),
        ("calibration_seconds", False),
        ("monotonic_origin", -1),
        ("cache_observation", " "),
    ):
        _, run_root, review_root, summary = _root(tmp_path / f"{field}-{value}")
        identity = cast(list[dict[str, object]], summary["runs"])[0]["invocation_identity"]
        cast(dict[str, object], identity)[field] = value
        _write_json(run_root / verifier.SUMMARY_NAME, summary)
        (review_root / verifier.INVENTORY_NAME).unlink()
        with pytest.raises(verifier.RunSetRefusalError, match="identity"):
            verifier.snapshot_run_root(
                run_root=run_root,
                review_root=review_root,
                execution_revision=EXECUTION,
            )


def test_snapshot_refuses_extra_top_level_coordinator_artifacts(tmp_path: Path) -> None:
    for name in ("profile-4-run.json", "unexpected.log"):
        _, run_root, review_root, _ = _root(tmp_path / name)
        (run_root / name).write_bytes(b"{}\n")
        (review_root / verifier.INVENTORY_NAME).unlink()
        with pytest.raises(verifier.RunSetRefusalError, match="top-level"):
            verifier.snapshot_run_root(
                run_root=run_root,
                review_root=review_root,
                execution_revision=EXECUTION,
            )


def test_snapshot_refuses_missing_coordinator_command_log(tmp_path: Path) -> None:
    _, run_root, review_root, _ = _root(tmp_path)
    (run_root / "profile-2-inventory-readback.stderr.log").unlink()
    (review_root / verifier.INVENTORY_NAME).unlink()
    with pytest.raises(verifier.RunSetRefusalError, match="top-level"):
        verifier.snapshot_run_root(
            run_root=run_root,
            review_root=review_root,
            execution_revision=EXECUTION,
        )


def test_retention_refuses_review_proof_change_at_copy_boundary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository, run_root, review_root, summary = _root(tmp_path)
    _read_all(repository, run_root, review_root, summary)
    _join(repository, run_root, review_root)
    _complete_review_root(review_root)
    evidence_root = tmp_path / "evidence"
    original = verifier._atomic_new

    def change_after_admission_copy(path: Path, data: bytes) -> None:
        original(path, data)
        if path == evidence_root / verifier.ADMISSION_NAME:
            _reseal_proof(review_root, 1, b"{}\n")

    monkeypatch.setattr(verifier, "_atomic_new", change_after_admission_copy)
    with pytest.raises(verifier.RunSetRefusalError, match="review artifact"):
        verifier.retain_run_root(
            run_root=run_root,
            review_root=review_root,
            evidence_root=evidence_root,
            execution_revision=EXECUTION,
        )


def test_retention_refuses_changed_coordinator_status(tmp_path: Path) -> None:
    repository, run_root, review_root, summary = _root(tmp_path)
    _read_all(repository, run_root, review_root, summary)
    _join(repository, run_root, review_root)
    _complete_review_root(review_root)
    (review_root / "coordinator.status").write_bytes(b"2\n")
    with pytest.raises(verifier.RunSetRefusalError, match="coordinator"):
        verifier.retain_run_root(
            run_root=run_root,
            review_root=review_root,
            evidence_root=tmp_path / "evidence",
            execution_revision=EXECUTION,
        )


def test_retention_refuses_status_change_between_check_and_digest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository, run_root, review_root, summary = _root(tmp_path)
    _read_all(repository, run_root, review_root, summary)
    _join(repository, run_root, review_root)
    _complete_review_root(review_root)
    status_path = review_root / "coordinator.status"
    original = verifier._regular_bytes
    changed = False

    def change_after_first_status_read(path: Path, label: str) -> bytes:
        nonlocal changed
        data = original(path, label)
        if path == status_path and not changed:
            changed = True
            status_path.write_bytes(b"2\n")
        return data

    monkeypatch.setattr(verifier, "_regular_bytes", change_after_first_status_read)
    evidence_root = tmp_path / "evidence"
    with pytest.raises(verifier.RunSetRefusalError, match="coordinator status"):
        verifier.retain_run_root(
            run_root=run_root,
            review_root=review_root,
            evidence_root=evidence_root,
            execution_revision=EXECUTION,
        )
    assert changed
    assert not evidence_root.exists()


def test_retention_refuses_copied_status_change_at_final_boundary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository, run_root, review_root, summary = _root(tmp_path)
    _read_all(repository, run_root, review_root, summary)
    _join(repository, run_root, review_root)
    _complete_review_root(review_root)
    evidence_root = tmp_path / "evidence"
    original = verifier._atomic_new

    def change_after_digest_file(path: Path, data: bytes) -> None:
        original(path, data)
        if path == evidence_root / "run-root.tar.gz.sha256":
            (evidence_root / "coordinator.status").write_bytes(b"2\n")

    monkeypatch.setattr(verifier, "_atomic_new", change_after_digest_file)
    with pytest.raises(verifier.RunSetRefusalError, match="coordinator status"):
        verifier.retain_run_root(
            run_root=run_root,
            review_root=review_root,
            evidence_root=evidence_root,
            execution_revision=EXECUTION,
        )


def test_join_cli_refuses_oversized_json_integer(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repository, run_root, review_root, summary = _root(tmp_path)
    _read_all(repository, run_root, review_root, summary)
    _reseal_proof(review_root, 1, b'{"n":' + b"9" * 5000 + b"}\n")
    assert (
        verifier.main(
            [
                "join",
                "--run-root",
                str(run_root),
                "--review-root",
                str(review_root),
                "--expect-execution-revision",
                EXECUTION,
                "--expect-reader-revision",
                READER,
            ]
        )
        == 2
    )
    assert "REFUSED: reader 1 proof" in capsys.readouterr().err
    assert not (review_root / verifier.ADMISSION_NAME).exists()


def test_snapshot_cli_publishes_once_and_refuses_overwrite(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _, run_root, review_root, _ = _root(tmp_path)
    (review_root / verifier.INVENTORY_NAME).unlink()
    argv = [
        "snapshot",
        "--run-root",
        str(run_root),
        "--review-root",
        str(review_root),
        "--expect-execution-revision",
        EXECUTION,
    ]
    assert verifier.main(argv) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "accepted"
    assert (
        output["inventory_sha256"]
        == hashlib.sha256((review_root / verifier.INVENTORY_NAME).read_bytes()).hexdigest()
    )
    assert verifier.main(argv) == 2
    assert "already exists" in capsys.readouterr().err


def test_reader_command_refusal_leaves_exact_record_and_stops(tmp_path: Path) -> None:
    repository, run_root, review_root, _ = _root(tmp_path)
    status = verifier.run_reader(
        repository=repository,
        run_root=run_root,
        review_root=review_root,
        execution_revision=EXECUTION,
        reader_revision=READER,
        run_order=1,
        runner=lambda argv: subprocess.CompletedProcess(argv, 2, b"", b"refused\n"),
    )
    assert status == 2
    command = json.loads((review_root / verifier._reader_names(1)[0]).read_text())
    assert command["argv"] == verifier._reader_argv(repository, run_root, EXECUTION, READER, 1)
    assert command["exit_status"] == 2
    with pytest.raises(verifier.RunSetRefusalError):
        _join(repository, run_root, review_root)


def test_join_refuses_missing_extra_and_mutated_proofs(tmp_path: Path) -> None:
    for mutation in (
        "missing",
        "extra",
        "duplicate",
        "nonfinite",
        "argv",
        "python-path",
        "order",
        "profile-path",
        "identity",
        "receipt-bytes",
        "nonzero-status",
    ):
        repository, run_root, review_root, summary = _root(tmp_path / mutation)
        _read_all(repository, run_root, review_root, summary)
        command_name, stdout_name, _, status_name = verifier._reader_names(1)
        command_path = review_root / command_name
        stdout_path = review_root / stdout_name
        if mutation == "missing":
            stdout_path.unlink()
        elif mutation == "extra":
            (review_root / "profile-4-source-distinct.stdout.json").write_bytes(b"{}")
        elif mutation == "duplicate":
            data = stdout_path.read_bytes().replace(
                b'"status": "accepted"', b'"status": "accepted", "status": "accepted"'
            )
            _reseal_proof(review_root, 1, data)
        elif mutation == "nonfinite":
            data = stdout_path.read_bytes().replace(
                b'"interval_boxes_observed": 1', b'"interval_boxes_observed": NaN'
            )
            _reseal_proof(review_root, 1, data)
        elif mutation in ("order", "profile-path", "identity", "receipt-bytes"):
            proof = json.loads(stdout_path.read_text())
            if mutation == "order":
                proof["run_order"] = 2
            elif mutation == "profile-path":
                proof["profile_directory"] = str(run_root / "profile-2")
            elif mutation == "identity":
                proof["invocation_identity"]["requested_workers"] = True
            else:
                proof["receipt"]["bytes"] += 1
            _reseal_proof(review_root, 1, (json.dumps(proof) + "\n").encode())
        else:
            command = json.loads(command_path.read_text())
            if mutation == "argv":
                command["argv"][5] = "--wrong-revision-flag"
            elif mutation == "python-path":
                command["argv"][0] = "/unexpected/python"
            else:
                command["exit_status"] = 2
                (review_root / status_name).write_bytes(b"2\n")
            _write_json(command_path, command)
        with pytest.raises((OSError, verifier.RunSetRefusalError)):
            _join(repository, run_root, review_root)


def test_inventory_refuses_mutation_of_any_run_artifact(tmp_path: Path) -> None:
    for mutation in (
        "top-level-edit",
        "added-file",
        "removed-file",
        "empty-directory",
        "symlink-replacement",
    ):
        repository, run_root, review_root, _ = _root(tmp_path / mutation)
        del repository
        if mutation == "top-level-edit":
            (run_root / "profile-1-run.json").write_bytes(b'{"changed":true}\n')
        elif mutation == "added-file":
            (run_root / "profile-1" / "extra.txt").write_bytes(b"extra")
        elif mutation == "removed-file":
            (run_root / "profile-1" / "raw-directions" / "0.json").unlink()
        elif mutation == "empty-directory":
            (run_root / "profile-1" / "empty").mkdir()
        else:
            path = run_root / "profile-1" / "result.json"
            path.unlink()
            path.symlink_to(run_root / "profile-2" / "result.json")
        with pytest.raises(verifier.RunSetRefusalError):
            verifier._baseline(run_root, review_root, EXECUTION)


def test_archive_reader_refuses_duplicate_traversal_and_changed_bytes(tmp_path: Path) -> None:
    _, run_root, review_root, _ = _root(tmp_path)
    _, baseline = verifier._baseline(run_root, review_root, EXECUTION)
    for mutation in ("duplicate", "traversal", "changed", "type"):
        archive_path = tmp_path / f"{mutation}.tar.gz"
        with tarfile.open(archive_path, "w:gz") as archive:
            info = tarfile.TarInfo(run_root.name)
            info.type = tarfile.DIRTYPE
            archive.addfile(info)
            for relative in cast(list[str], baseline["directories"]):
                info = tarfile.TarInfo(f"{run_root.name}/{relative}")
                info.type = tarfile.DIRTYPE
                archive.addfile(info)
            for row in cast(list[dict[str, object]], baseline["files"]):
                relative = cast(str, row["path"])
                data = (run_root / relative).read_bytes()
                if mutation == "changed" and relative == verifier.SUMMARY_NAME:
                    data += b"!"
                info = tarfile.TarInfo(f"{run_root.name}/{relative}")
                if mutation == "type" and relative == verifier.SUMMARY_NAME:
                    info.type = tarfile.SYMTYPE
                    info.linkname = "other"
                    archive.addfile(info)
                else:
                    info.size = len(data)
                    archive.addfile(info, io.BytesIO(data))
            if mutation in ("duplicate", "traversal"):
                name = (
                    f"{run_root.name}/{verifier.SUMMARY_NAME}"
                    if mutation == "duplicate"
                    else f"{run_root.name}/../outside"
                )
                info = tarfile.TarInfo(name)
                info.size = 1
                archive.addfile(info, io.BytesIO(b"x"))
        with pytest.raises(verifier.RunSetRefusalError):
            verifier._verify_archive(archive_path, run_root, baseline)


def _git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        ("git", *arguments), cwd=repository, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def _source_repository(repository: Path) -> tuple[str, list[dict[str, object]]]:
    files = {
        "packing/devtools/__init__.py": b"",
        "packing/devtools/calibrate_fixed_core_packet.py": b"from . import helper\n",
        "packing/devtools/helper.py": b"from sqpack import mathutil\n",
        "packing/src/sqpack/__init__.py": b"",
        "packing/src/sqpack/mathutil.py": b"ANSWER = 2\n",
        verifier.FIXTURE_PATH: b"{}\n",
        "packing/.python-version": b"3.14\n",
        "packing/pyproject.toml": b"[project]\nname = 'synthetic'\n",
        "packing/uv.lock": b"version = 1\n",
    }
    for relative, data in files.items():
        path = repository / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    _git(repository, "init")
    _git(repository, "add", ".")
    _git(
        repository,
        "-c",
        "user.name=Synthetic",
        "-c",
        "user.email=synthetic@example.test",
        "commit",
        "-m",
        "synthetic source",
    )
    revision = _git(repository, "rev-parse", "HEAD")
    manifest: list[dict[str, object]] = []
    for path in sorted(files):
        data = files[path]
        manifest.append(
            {
                "path": path,
                "git_blob": _git(repository, "rev-parse", f"HEAD:{path}"),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    return revision, manifest


def _retain_profiles(
    tmp_path: Path, revision: str, manifest: list[dict[str, object]]
) -> tuple[Path, Path]:
    _, run_root, review_root, summary = _root(tmp_path / "evidence", revision)
    for order in verifier.RUN_ORDERS:
        receipt = {
            "sources": {
                "implementation_revision": revision,
                "manifest": deepcopy(manifest),
                "runtime": {},
            }
        }
        data = _write_json(run_root / f"profile-{order}" / "result.json", receipt)
        run = cast(list[dict[str, object]], summary["runs"])[order - 1]
        run["calibration_receipt"] = {
            "path": "result.json",
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    _write_json(run_root / verifier.SUMMARY_NAME, summary)
    (review_root / verifier.INVENTORY_NAME).unlink()
    verifier.snapshot_run_root(
        run_root=run_root, review_root=review_root, execution_revision=revision
    )
    return run_root, review_root


def test_source_closure_reports_code_and_environment_drift_without_refusing(
    tmp_path: Path,
) -> None:
    """The run set is bound to its execution revision; later changes are only reported.

    Code, fixture, `.python-version` and `uv.lock` changes, a removed module and an
    added import all leave the evidence admissible and are named in `drift`.
    """
    repository = tmp_path / "source-repository"
    repository.mkdir()
    revision, manifest = _source_repository(repository)
    run_root, review_root = _retain_profiles(tmp_path, revision, manifest)

    def check(candidate: str) -> dict[str, object]:
        return verifier.verify_source_closure(
            repository=repository,
            run_root=run_root,
            review_root=review_root,
            execution_revision=revision,
            candidate_tree=candidate,
        )

    accepted = check(_git(repository, "write-tree"))
    assert accepted["schema"] == verifier.CLOSURE_SCHEMA
    assert accepted["drift"] == []
    assert [row["path"] for row in cast(list[dict[str, object]], accepted["sources"])] == [
        row["path"] for row in manifest
    ]
    assert check(revision)["drift"] == []
    for relative in (
        "packing/devtools/helper.py",
        "packing/src/sqpack/__init__.py",
        verifier.FIXTURE_PATH,
        "packing/.python-version",
        "packing/uv.lock",
    ):
        path = repository / relative
        path.write_bytes(path.read_bytes() + b"# changed\n")
        _git(repository, "add", relative)
        result = check(_git(repository, "write-tree"))
        assert (result["status"], result["drift"]) == ("accepted", [relative])
        _git(repository, "reset", "--hard", "HEAD")
    helper = "packing/devtools/helper.py"
    _git(repository, "rm", helper)
    assert helper in cast(list[str], check(_git(repository, "write-tree"))["drift"])
    with pytest.raises(verifier.RunSetRefusalError, match="index"):
        check(revision)
    _git(repository, "reset", "--hard", "HEAD")
    (repository / helper).write_bytes(b"# unstaged, so not part of the evidence commit\n")
    assert check(_git(repository, "write-tree"))["drift"] == []
    _git(repository, "reset", "--hard", "HEAD")
    producer = repository / "packing/devtools/calibrate_fixed_core_packet.py"
    producer.write_bytes(b"from . import helper, added\n")
    (repository / "packing/devtools/added.py").write_bytes(b"VALUE = 3\n")
    _git(repository, "add", ".")
    assert check(_git(repository, "write-tree"))["drift"] == [
        "packing/devtools/added.py",
        "packing/devtools/calibrate_fixed_core_packet.py",
    ]


def test_source_closure_keeps_recorded_digests_and_checks_the_closure_paths(
    tmp_path: Path,
) -> None:
    """Row blob ids and digests are the runs' record, kept and not compared; the
    manifests must still name the execution revision's import closure, path for path."""
    repository = tmp_path / "source-repository"
    repository.mkdir()
    revision, manifest = _source_repository(repository)
    recorded = deepcopy(manifest)
    recorded[0]["git_blob"] = "0" * 40
    recorded[0]["sha256"] = "1" * 64
    run_root, review_root = _retain_profiles(tmp_path / "recorded", revision, recorded)
    accepted = verifier.verify_source_closure(
        repository=repository,
        run_root=run_root,
        review_root=review_root,
        execution_revision=revision,
        candidate_tree=revision,
    )
    assert accepted["sources"] == recorded
    missing = [row for row in manifest if row["path"] != "packing/devtools/helper.py"]
    run_root, review_root = _retain_profiles(tmp_path / "missing", revision, missing)
    with pytest.raises(verifier.RunSetRefusalError, match="complete source closure"):
        verifier.verify_source_closure(
            repository=repository,
            run_root=run_root,
            review_root=review_root,
            execution_revision=revision,
            candidate_tree=revision,
        )
