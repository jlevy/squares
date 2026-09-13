"""Adversarial controls for the target-free BC329 fixed-core instrument."""

# The retained-record parsers are deliberately tested below their public ``load_result``
# composition so adversarial fixtures can use a three-direction miniature packet.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from collections.abc import Callable, Sequence
from concurrent.futures import Future
from contextlib import suppress
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from typing import cast
from unittest.mock import patch

import pytest

from devtools import fixed_core_packet
from devtools.fixed_core_packet import (
    INTERVAL_DIRECTIONS,
    PROJECT_RUNTIME_PATHS,
    RAW_DIRECTIONS,
    RAW_THRESHOLD,
    RUNTIME_ATTESTATION_SCOPE,
    SOURCE_BLOB,
    SOURCE_PATH,
    SOURCE_SHA256,
    T026_BLOB,
    T026_PATH,
    T026_SHA256,
    ExactReaderDisagreementError,
    ExactRoute,
    IntervalRoute,
    PackageRuntimeObservation,
    PacketDeadlineError,
    PacketError,
    PacketOperationalError,
    RawMinimum,
    RuntimeObservation,
    _direction_digest,
    _reconstruct_dilation_directions,
    _reconstruct_exact_directions,
    _reconstruct_interval_directions,
    _reconstruct_raw_directions,
    _record_external_timeout,
    _strict_json_bytes,
    discover_implementation_paths,
    execute_packet,
    load_packet_source,
    load_result,
    load_t026_reference,
    main,
    normalized_record,
    raw_decision,
    run_exact_route,
    run_raw_sweep,
    run_worker,
    runtime_binding,
    source_manifest,
    supervise_worker,
    validate_result_document,
)
from sqpack.fractional.threshold import ThresholdCertificate

REPOSITORY = Path(__file__).resolve().parents[2]
SOURCE = (REPOSITORY / SOURCE_PATH).read_bytes()
T026_BYTES = (REPOSITORY / T026_PATH).read_bytes()
T026 = cast(dict[str, object], json.loads(T026_BYTES))
REVISION = "a" * 40
MANIFEST = sorted(
    [
        {
            "path": SOURCE_PATH,
            "git_blob": SOURCE_BLOB,
            "sha256": SOURCE_SHA256,
        },
        {
            "path": T026_PATH,
            "git_blob": T026_BLOB,
            "sha256": T026_SHA256,
        },
        *[
            {
                "path": path,
                "git_blob": f"{index:040x}",
                "sha256": f"{index:064x}",
            }
            for index, path in enumerate(PROJECT_RUNTIME_PATHS, start=1)
        ],
    ],
    key=lambda row: row["path"],
)
RUNTIME = {
    "python": {
        "implementation": "cpython",
        "version": "3.14.7",
        "abi": "cpython-314t-test",
        "gil_enabled": False,
        "environment": "/project/packing/.venv",
        "executable": "/project/packing/.venv/bin/python",
        "resolved_executable": "/project/packing/.venv/bin/python3.14",
        "build": "3.14.7 free-threaded test build",
    },
    "packages": {"numpy": "2.5.2", "strif": "3.1.0"},
    "attestation_scope": RUNTIME_ATTESTATION_SCOPE,
}


@pytest.fixture(autouse=True)
def _portable_runtime_binding(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(fixed_core_packet, "runtime_binding", lambda _repository: RUNTIME)


def _raw(minimum: Fraction):
    def run(*_args, **_kwargs) -> RawMinimum:
        return RawMinimum(minimum, 0, (Fraction(1), Fraction(1)), RAW_DIRECTIONS)

    return run


def _exact(*_args, **_kwargs) -> ExactRoute:
    return ExactRoute(Fraction(1), 0, (Fraction(1), Fraction(1)), RAW_DIRECTIONS, 0)


def _interval(*_args, **_kwargs) -> IntervalRoute:
    return IntervalRoute(Fraction(1), Fraction(1), INTERVAL_DIRECTIONS, 0, 0, accepted=True)


def _dilation(path: Path, *, workers: int, **_kwargs: object) -> dict[str, object]:
    del workers
    old = cast(dict[str, object], T026["conclusion"])
    return {
        "source": {"sha256": hashlib.sha256(path.read_bytes()).hexdigest()},
        "conclusion": {
            "bounded_side": "synthetic",
            "bounded_side_squared": str(Fraction(cast(str, old["bounded_side_squared"])) + 1),
        },
    }


def _execute(tmp_path: Path, minimum: Fraction, **overrides):
    output = tmp_path / "result"
    output.mkdir()
    arguments = {
        "revision": REVISION,
        "manifest": MANIFEST,
        "runtime": RUNTIME,
        "output_dir": output,
        "workers": 1,
        "scientific_seconds": 10.0,
        "external_seconds": 20.0,
        "grace_seconds": 2.0,
        "process_deadline": 100.0,
        "clock": lambda: 0.0,
        "raw_runner": _raw(minimum),
        "exact_runner": _exact,
        "interval_runner": _interval,
        "dilation_runner": _dilation,
        "raw_witness_replay": lambda _certificate, result: (result.minimum, True),
    }
    arguments.update(overrides)
    with patch("devtools.fixed_core_packet._direction_digest", return_value="0" * 64):
        return output, execute_packet(SOURCE, T026_BYTES, **arguments)


def _write_row(directory: Path, label: str, row: dict[str, object]) -> None:
    directory.mkdir(exist_ok=True)
    (directory / f"{label}.json").write_text(json.dumps(row) + "\n")


def _bind_direction_digest(
    receipt: dict[str, object], directory: Path, labels: Sequence[str]
) -> dict[str, object]:
    receipt["directions_sha256"] = _direction_digest(
        tuple(directory / f"{label}.json" for label in labels)
    )
    return receipt


class _ControlledExecutor:
    """Make completion order explicit without starting scientific worker processes."""

    def __init__(self, completion_batches: Sequence[Sequence[int]]) -> None:
        self._completion_batches = iter(completion_batches)
        self._pending: dict[Future[object], tuple[Callable[[int], object], int]] = {}
        self.max_workers = 0
        self.max_pending = 0
        self.submitted: list[int] = []
        self.shutdown_called = False
        self.terminated = False

    def factory(self, *, max_workers: int, **_kwargs: object) -> _ControlledExecutor:
        self.max_workers = max_workers
        return self

    def submit(self, function: Callable[[int], object], index: int) -> Future[object]:
        future: Future[object] = Future()
        self._pending[future] = (function, index)
        self.submitted.append(index)
        self.max_pending = max(self.max_pending, len(self._pending))
        return future

    def wait(
        self,
        futures: Sequence[Future[object]],
        **_kwargs: object,
    ) -> tuple[set[Future[object]], set[Future[object]]]:
        requested = set(futures)
        indices = set(next(self._completion_batches, ()))
        done: set[Future[object]] = set()
        for future in tuple(requested):
            function, index = self._pending[future]
            if index not in indices:
                continue
            try:
                future.set_result(function(index))
            except Exception as error:  # noqa: BLE001 -- emulate a failed future
                future.set_exception(error)
            del self._pending[future]
            done.add(future)
        assert len(done) == len(indices)
        return done, requested - done

    def shutdown(self, **_kwargs: object) -> None:
        self.shutdown_called = True

    def terminate_workers(self) -> None:
        self.terminated = True


def _install_controlled_executor(
    monkeypatch: pytest.MonkeyPatch,
    completion_batches: Sequence[Sequence[int]],
) -> _ControlledExecutor:
    executor = _ControlledExecutor(completion_batches)
    monkeypatch.setattr(fixed_core_packet, "ProcessPoolExecutor", executor.factory)
    monkeypatch.setattr(fixed_core_packet, "wait", executor.wait)
    return executor


def _missing_group_on_probe(_pid: int, signal_number: int) -> None:
    if signal_number == 0:
        raise ProcessLookupError


def _repository_with_sources(root: Path, *extra_files: tuple[str, bytes]) -> tuple[Path, str]:
    repository = root / "repository"
    for relative, data in (
        (SOURCE_PATH, SOURCE),
        (T026_PATH, T026_BYTES),
        *extra_files,
    ):
        path = repository / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    subprocess.run(("git", "init", "-q", str(repository)), check=True)
    subprocess.run(("git", "-C", str(repository), "add", "."), check=True)
    subprocess.run(
        (
            "git",
            "-C",
            str(repository),
            "-c",
            "user.name=Fixed Core Test",
            "-c",
            "user.email=fixed-core@example.invalid",
            "commit",
            "-qm",
            "fixture",
        ),
        check=True,
    )
    revision = subprocess.run(
        ("git", "-C", str(repository), "rev-parse", "HEAD"),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return repository, revision


def _raw_receipt(
    completed: int,
    minimum: str,
    argmin: int,
    witness: list[str],
    *,
    completed_directions: Sequence[int] | None = None,
) -> dict[str, object]:
    return {
        "directions_completed": completed,
        "completed_directions": list(
            range(completed) if completed_directions is None else completed_directions
        ),
        "observed_minimum_upper_bound": minimum,
        "observed_argmin": argmin,
        "observed_witness": witness,
        "raw_minimum": minimum if completed == 3 else None,
    }


def test_raw_readback_reconstructs_stable_argmin_from_every_retained_row(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "raw"
    for index, charge, witness in (
        (0, "1", ["2", "3"]),
        (1, "1", ["4", "5"]),
        (2, "2", ["6", "7"]),
    ):
        _write_row(
            directory,
            str(index),
            {"direction": index, "charge": charge, "witness": witness},
        )
    result = _reconstruct_raw_directions(
        directory,
        _bind_direction_digest(_raw_receipt(3, "1", 0, ["2", "3"]), directory, ("0", "1", "2")),
        expected=3,
        complete=True,
    )
    assert result == RawMinimum(Fraction(1), 0, (Fraction(2), Fraction(3)), 3)

    forged = _bind_direction_digest(
        _raw_receipt(3, "1", 1, ["4", "5"]), directory, ("0", "1", "2")
    )
    with pytest.raises(PacketError, match="disagree"):
        _reconstruct_raw_directions(directory, forged, expected=3, complete=True)


def test_raw_direction_digest_detects_a_nonminimum_witness_change(tmp_path: Path) -> None:
    directory = tmp_path / "raw"
    for index, charge in enumerate(("1", "2")):
        _write_row(
            directory,
            str(index),
            {"direction": index, "charge": charge, "witness": ["2", "3"]},
        )
    receipt = _bind_direction_digest(_raw_receipt(2, "1", 0, ["2", "3"]), directory, ("0", "1"))
    row = json.loads((directory / "1.json").read_text())
    row["witness"] = ["5", "7"]
    _write_row(directory, "1", row)
    with pytest.raises(PacketError, match="digest"):
        _reconstruct_raw_directions(directory, receipt, expected=2, complete=True)


@pytest.mark.parametrize("fault", ["missing", "extra", "label", "schema", "noncanonical"])
def test_raw_readback_refuses_filename_and_row_tampering(tmp_path: Path, fault: str) -> None:
    directory = tmp_path / "raw"
    for index in range(3):
        _write_row(
            directory,
            str(index),
            {"direction": index, "charge": "1", "witness": ["2", "3"]},
        )
    if fault == "missing":
        (directory / "1.json").unlink()
    elif fault == "extra":
        _write_row(directory, "3", {"direction": 3, "charge": "1", "witness": ["2", "3"]})
    elif fault == "label":
        row = json.loads((directory / "1.json").read_text())
        row["direction"] = 2
        _write_row(directory, "1", row)
    elif fault == "schema":
        row = json.loads((directory / "1.json").read_text())
        row["unchecked"] = True
        _write_row(directory, "1", row)
    else:
        row = json.loads((directory / "1.json").read_text())
        row["charge"] = "2/2"
        _write_row(directory, "1", row)
    receipt = _raw_receipt(3, "1", 0, ["2", "3"])
    receipt["directions_sha256"] = "0" * 64
    with pytest.raises(PacketError):
        _reconstruct_raw_directions(
            directory,
            receipt,
            expected=3,
            complete=True,
        )


def test_readback_ignores_only_a_valid_strif_temp_after_interrupted_atomic_write(
    tmp_path: Path,
) -> None:
    def interrupt_between_write_and_replace(path: Path, text: str) -> None:
        path.with_name(f"{path.name}{'a' * 13}.partial").write_text(text)
        raise KeyboardInterrupt

    with (
        patch(
            "devtools.fixed_core_packet.atomic_write_text",
            side_effect=interrupt_between_write_and_replace,
        ),
        pytest.raises(KeyboardInterrupt),
    ):
        fixed_core_packet._write_direction(  # noqa: SLF001 -- injected atomic boundary
            tmp_path,
            0,
            {"direction": 0, "charge": "1", "witness": ["2", "3"]},
        )
    receipt: dict[str, object] = {
        "directions_completed": 0,
        "completed_directions": [],
        "observed_minimum_upper_bound": None,
        "observed_argmin": None,
        "observed_witness": None,
        "raw_minimum": None,
    }
    assert _reconstruct_raw_directions(tmp_path, receipt, expected=1, complete=False) is None

    (tmp_path / "0.json-short.partial").write_text("incomplete")
    with pytest.raises(PacketError, match="unexpected retained direction entry"):
        _reconstruct_raw_directions(tmp_path, receipt, expected=1, complete=False)


def _exact_receipt(*, disagreements: int = 1) -> dict[str, object]:
    return {
        "status": "complete",
        "directions_completed": 2,
        "completed_directions": [0, 1],
        "minimum": "1",
        "argmin": 0,
        "witness": ["2", "3"],
        "dense_slab_disagreements": disagreements,
    }


def test_exact_readback_recomputes_witness_only_disagreement(tmp_path: Path) -> None:
    directory = tmp_path / "exact"
    _write_row(
        directory,
        "0",
        {
            "direction": 0,
            "dense": "1",
            "slab": "1",
            "agree": False,
            "witness": ["2", "3"],
            "slab_witness": ["2", "4"],
        },
    )
    _write_row(
        directory,
        "1",
        {
            "direction": 1,
            "dense": "2",
            "slab": "2",
            "agree": True,
            "witness": ["5", "6"],
            "slab_witness": ["5", "6"],
        },
    )
    result = _reconstruct_exact_directions(
        directory,
        _bind_direction_digest(_exact_receipt(), directory, ("0", "1")),
        expected=2,
        complete=True,
    )
    assert result == ExactRoute(Fraction(1), 0, (Fraction(2), Fraction(3)), 2, 1)

    forged = json.loads((directory / "0.json").read_text())
    forged["agree"] = True
    _write_row(directory, "0", forged)
    with pytest.raises(PacketError, match="agreement flag"):
        _reconstruct_exact_directions(
            directory,
            _bind_direction_digest(_exact_receipt(), directory, ("0", "1")),
            expected=2,
            complete=True,
        )


def test_exact_readback_accepts_a_sparse_completed_disagreement(tmp_path: Path) -> None:
    directory = tmp_path / "exact"
    _write_row(
        directory,
        "0",
        {
            "direction": 0,
            "dense": "1/2",
            "slab": "1/2",
            "agree": True,
            "witness": ["1", "1"],
            "slab_witness": ["1", "1"],
        },
    )
    _write_row(
        directory,
        "1",
        {
            "direction": 1,
            "dense": "1",
            "slab": "1",
            "agree": False,
            "witness": ["2", "3"],
            "slab_witness": ["2", "4"],
        },
    )
    receipt: dict[str, object] = {
        "status": "invalid",
        "directions_completed": 1,
        "completed_directions": [1],
        "observed_minimum_upper_bound": "1",
        "argmin": 1,
        "witness": ["2", "3"],
        "reader_disagreement": {
            "direction": 1,
            "dense": "1",
            "dense_witness": ["2", "3"],
            "slab": "1",
            "slab_witness": ["2", "4"],
        },
    }

    assert _reconstruct_exact_directions(
        directory, receipt, expected=3, complete=False
    ) == ExactRoute(Fraction(1), 1, (Fraction(2), Fraction(3)), 1, 1)


def test_exact_runner_retains_both_reader_witnesses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    certificate = cast(
        ThresholdCertificate,
        SimpleNamespace(directions=(object(),), atoms=(), threshold_atoms=()),
    )
    monkeypatch.setattr(
        fixed_core_packet,
        "_dense_and_slab",
        lambda _certificate, _index: (
            (Fraction(1), (Fraction(2), Fraction(3))),
            (Fraction(1), (Fraction(2), Fraction(4))),
        ),
    )
    monkeypatch.setattr(fixed_core_packet, "_placement_membership", lambda *_args: ())
    monkeypatch.setattr(fixed_core_packet, "exact_charge", lambda *_args: Fraction(1))
    try:
        with pytest.raises(ExactReaderDisagreementError) as raised:
            run_exact_route(
                certificate,
                workers=1,
                deadline=0.0,
                clock=lambda: 1.0,
                progress=lambda *_args: None,
                log=tmp_path,
            )
    finally:
        fixed_core_packet.SHARED_PACKET.certificate = None
    row = json.loads((tmp_path / "0.json").read_text())
    assert row["witness"] == ["2", "3"]
    assert row["slab_witness"] == ["2", "4"]
    assert raised.value.direction == 0
    assert raised.value.completed == 1


def test_parallel_raw_scheduler_bounds_submission_and_selects_lowest_tied_index(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    certificate = cast(
        ThresholdCertificate,
        SimpleNamespace(directions=(object(),) * 6, atoms=(), threshold_atoms=()),
    )
    executor = _install_controlled_executor(monkeypatch, ((3,), (2,), (1,), (0,), (5,), (4,)))
    monkeypatch.setattr(
        fixed_core_packet,
        "_raw_direction",
        lambda index: (index, Fraction(1), (Fraction(index), Fraction(index + 1))),
    )

    result = run_raw_sweep(
        certificate,
        workers=2,
        deadline=10.0,
        clock=lambda: 0.0,
        progress=lambda *_args: None,
        log=tmp_path,
    )

    assert executor.max_workers == 2
    assert executor.max_pending == 4
    assert executor.submitted == list(range(6))
    assert result == RawMinimum(Fraction(1), 0, (Fraction(0), Fraction(1)), 6)
    assert {path.name for path in tmp_path.iterdir()} == {
        "0.json",
        "1.json",
        "2.json",
        "3.json",
        "4.json",
        "5.json",
    }
    assert executor.shutdown_called
    assert not executor.terminated


def test_parallel_exact_surfaces_fast_disagreement_ahead_of_slow_prefix_and_deadline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    certificate = cast(
        ThresholdCertificate,
        SimpleNamespace(directions=(object(),) * 4, atoms=(), threshold_atoms=()),
    )
    executor = _install_controlled_executor(monkeypatch, ((1,),))

    def exact(index: int):
        dense = (Fraction(1), (Fraction(index), Fraction(index + 1)))
        slab = dense if index != 1 else (Fraction(1), (Fraction(7), Fraction(8)))
        return index, dense, slab

    monkeypatch.setattr(fixed_core_packet, "_exact_direction", exact)

    with pytest.raises(ExactReaderDisagreementError) as raised:
        run_exact_route(
            certificate,
            workers=2,
            deadline=0.0,
            clock=lambda: 1.0,
            progress=lambda *_args: None,
            log=tmp_path,
        )

    assert raised.value.direction == 1
    assert raised.value.completed == 1
    assert raised.value.completed_directions == (1,)
    assert (tmp_path / "1.json").is_file()
    assert not (tmp_path / "0.json").exists()
    assert executor.terminated


def test_parallel_raw_deadline_retains_every_completed_row(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    certificate = cast(
        ThresholdCertificate,
        SimpleNamespace(directions=(object(),) * 4, atoms=(), threshold_atoms=()),
    )
    executor = _install_controlled_executor(monkeypatch, ((2, 3),))
    monkeypatch.setattr(
        fixed_core_packet,
        "_raw_direction",
        lambda index: (index, Fraction(index + 1), (Fraction(index), Fraction(index))),
    )
    readings = iter((0.0, 10.0, 10.0))

    with pytest.raises(PacketDeadlineError, match="during raw sweep"):
        run_raw_sweep(
            certificate,
            workers=2,
            deadline=10.0,
            clock=lambda: next(readings),
            progress=lambda *_args: None,
            log=tmp_path,
        )

    assert {path.name for path in tmp_path.iterdir()} == {"2.json", "3.json"}
    assert executor.terminated


def test_parallel_raw_worker_exception_retains_successful_peer_completion(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    certificate = cast(
        ThresholdCertificate,
        SimpleNamespace(directions=(object(),) * 4, atoms=(), threshold_atoms=()),
    )
    executor = _install_controlled_executor(monkeypatch, ((1, 2),))

    def raw(index: int):
        if index == 2:
            raise RuntimeError("synthetic worker failure")
        return index, Fraction(index + 1), (Fraction(index), Fraction(index))

    monkeypatch.setattr(fixed_core_packet, "_raw_direction", raw)

    with pytest.raises(RuntimeError, match="synthetic worker failure"):
        run_raw_sweep(
            certificate,
            workers=2,
            deadline=10.0,
            clock=lambda: 0.0,
            progress=lambda *_args: None,
            log=tmp_path,
        )

    assert (tmp_path / "1.json").is_file()
    assert not (tmp_path / "2.json").exists()
    assert executor.terminated


def test_parallel_raw_progress_failure_is_not_swallowed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    class ProgressError(RuntimeError):
        pass

    certificate = cast(
        ThresholdCertificate,
        SimpleNamespace(directions=(object(),) * 4, atoms=(), threshold_atoms=()),
    )
    executor = _install_controlled_executor(monkeypatch, ((0,), (2, 3)))
    monkeypatch.setattr(
        fixed_core_packet,
        "_raw_direction",
        lambda index: (index, Fraction(index + 1), (Fraction(index), Fraction(index))),
    )

    checkpoint: dict[str, object] = {}

    def fail_progress(
        completed: int,
        completed_directions: tuple[int, ...],
        observed: Fraction,
        argmin: int,
        witness: tuple[Fraction, Fraction],
    ) -> None:
        if not checkpoint:
            checkpoint.update(
                _raw_receipt(
                    completed,
                    str(observed),
                    argmin,
                    [str(witness[0]), str(witness[1])],
                    completed_directions=completed_directions,
                )
            )
            return
        raise ProgressError("synthetic progress failure")

    with pytest.raises(ProgressError, match="synthetic progress failure"):
        run_raw_sweep(
            certificate,
            workers=2,
            deadline=10.0,
            clock=lambda: 0.0,
            progress=fail_progress,
            log=tmp_path,
        )

    assert {path.name for path in tmp_path.iterdir()} == {"0.json", "2.json", "3.json"}
    assert _reconstruct_raw_directions(
        tmp_path, checkpoint, expected=4, complete=False
    ) == RawMinimum(Fraction(1), 0, (Fraction(0), Fraction(0)), 1)
    assert executor.terminated


def test_exact_reader_disagreement_is_published_as_invalid(tmp_path: Path) -> None:
    def disagreement(_certificate, *, log, **_kwargs):
        _write_row(
            log,
            "0",
            {
                "direction": 0,
                "dense": "1",
                "slab": "1",
                "agree": False,
                "witness": ["2", "3"],
                "slab_witness": ["2", "4"],
            },
        )
        raise ExactReaderDisagreementError(
            completed=1,
            completed_directions=(0,),
            minimum=Fraction(1),
            argmin=0,
            witness=(Fraction(2), Fraction(3)),
            direction=0,
            dense=(Fraction(1), (Fraction(2), Fraction(3))),
            slab=(Fraction(1), (Fraction(2), Fraction(4))),
        )

    output, result = _execute(
        tmp_path,
        RAW_THRESHOLD + Fraction(1, 10**9),
        exact_runner=disagreement,
    )
    assert result["status"] == "invalid"
    assert result["outcome"] == "reader-disagreement"
    assert result["scientific_decision"] == "unresolved"
    exact = cast(dict[str, object], cast(dict[str, object], result["routes"])["exact"])
    assert exact["status"] == "invalid"
    assert cast(dict[str, object], exact["reader_disagreement"])["direction"] == 0
    rebuilt = _reconstruct_exact_directions(
        output / "normalized-exact-directions",
        exact,
        expected=RAW_DIRECTIONS,
        complete=False,
    )
    assert rebuilt is not None
    assert rebuilt.disagreements == 1
    _record_external_timeout(output / "result.json", "later external timeout", 12.0)
    retained = json.loads((output / "result.json").read_text())
    assert retained["outcome"] == "reader-disagreement"


def test_exact_readback_compares_recomputed_disagreement_count_to_receipt(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "exact"
    for index in range(2):
        _write_row(
            directory,
            str(index),
            {
                "direction": index,
                "dense": str(index + 1),
                "slab": str(index + 1),
                "agree": True,
                "witness": ["2", "3"],
                "slab_witness": ["2", "3"],
            },
        )
    with pytest.raises(PacketError, match="disagreement count"):
        _reconstruct_exact_directions(
            directory,
            _bind_direction_digest(_exact_receipt(disagreements=1), directory, ("0", "1")),
            expected=2,
            complete=True,
        )

    forged = _bind_direction_digest(_exact_receipt(disagreements=0), directory, ("0", "1"))
    forged["minimum"] = "2"
    forged["argmin"] = 1
    with pytest.raises(PacketError, match="disagree"):
        _reconstruct_exact_directions(directory, forged, expected=2, complete=True)


def test_exact_direction_digest_detects_a_nonminimum_witness_change(tmp_path: Path) -> None:
    directory = tmp_path / "exact"
    for index in range(2):
        _write_row(
            directory,
            str(index),
            {
                "direction": index,
                "dense": str(index + 1),
                "slab": str(index + 1),
                "agree": True,
                "witness": ["2", "3"],
                "slab_witness": ["2", "3"],
            },
        )
    receipt = _bind_direction_digest(_exact_receipt(disagreements=0), directory, ("0", "1"))
    row = json.loads((directory / "1.json").read_text())
    row["witness"] = row["slab_witness"] = ["5", "7"]
    _write_row(directory, "1", row)
    with pytest.raises(PacketError, match="digest"):
        _reconstruct_exact_directions(directory, receipt, expected=2, complete=True)


def _interval_row_for(
    label: str,
    *,
    lower: int = 10,
    upper: int = 10,
    stalled: int = 0,
    budget_exhausted: bool = False,
) -> dict[str, object]:
    return {
        "label": label,
        "status": "certified" if not stalled and not budget_exhausted else "undecided",
        "lower": lower,
        "upper": upper,
        "witness": [1.25, 2.5],
        "boxes": max(stalled, 1),
        "stalled": stalled,
        "budget_exhausted": budget_exhausted,
    }


def test_interval_readback_reconstructs_enclosure_counts_and_acceptance(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "interval"
    labels = ("0", "1", "1'")
    for label, lower, upper in (("0", 12, 14), ("1", 10, 11), ("1'", 13, 15)):
        _write_row(directory, label, _interval_row_for(label, lower=lower, upper=upper))
    receipt: dict[str, object] = {
        "status": "complete",
        "directions_completed": 3,
        "enclosure": ["1", "11/10"],
        "stalled": 0,
        "budget_exhausted": 0,
        "accepted": True,
    }
    _bind_direction_digest(receipt, directory, labels)
    result = _reconstruct_interval_directions(
        directory, receipt, labels=labels, scale=10, complete=True
    )
    assert result is not None
    assert result.enclosure == (Fraction(1), Fraction(11, 10))
    assert result.accepted is True

    for field, forged in (
        ("enclosure", ["11/10", "11/10"]),
        ("stalled", 1),
        ("budget_exhausted", 1),
        ("accepted", False),
    ):
        saved = receipt[field]
        receipt[field] = forged
        with pytest.raises(PacketError, match="disagree"):
            _reconstruct_interval_directions(
                directory, receipt, labels=labels, scale=10, complete=True
            )
        receipt[field] = saved


def test_interval_direction_digest_detects_a_witness_change(tmp_path: Path) -> None:
    directory = tmp_path / "interval"
    labels = ("0", "1")
    for label in labels:
        _write_row(directory, label, _interval_row_for(label))
    receipt: dict[str, object] = {
        "status": "complete",
        "directions_completed": 2,
        "enclosure": ["1", "1"],
        "stalled": 0,
        "budget_exhausted": 0,
        "accepted": True,
    }
    _bind_direction_digest(receipt, directory, labels)
    row = json.loads((directory / "1.json").read_text())
    row["witness"] = [3.0, 4.0]
    _write_row(directory, "1", row)
    with pytest.raises(PacketError, match="digest"):
        _reconstruct_interval_directions(
            directory, receipt, labels=labels, scale=10, complete=True
        )


def test_interval_readback_refuses_missing_extra_and_mislabeled_rows(tmp_path: Path) -> None:
    labels = ("0", "1", "1'")
    for fault in ("missing", "extra", "label"):
        directory = tmp_path / fault
        for label in labels:
            _write_row(directory, label, _interval_row_for(label))
        if fault == "missing":
            (directory / "1.json").unlink()
        elif fault == "extra":
            _write_row(directory, "2", _interval_row_for("2"))
        else:
            row = json.loads((directory / "1.json").read_text())
            row["label"] = "0"
            _write_row(directory, "1", row)
        receipt: dict[str, object] = {
            "status": "complete",
            "directions_completed": 3,
            "enclosure": ["1", "1"],
            "stalled": 0,
            "budget_exhausted": 0,
            "accepted": True,
            "directions_sha256": "0" * 64,
        }
        with pytest.raises(PacketError):
            _reconstruct_interval_directions(
                directory, receipt, labels=labels, scale=10, complete=True
            )


def test_partial_interval_readback_binds_a_sparse_set_and_validates_unpublished_tail(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "interval"
    labels = ("0", "1", "1'", "2", "2'")
    for label in ("0", "1'", "2"):
        _write_row(directory, label, _interval_row_for(label))
    receipt: dict[str, object] = {
        "status": "partial",
        "directions_completed": 2,
        "completed_directions": ["0", "2"],
        "last": _interval_row_for("2"),
    }

    assert (
        _reconstruct_interval_directions(
            directory, receipt, labels=labels, scale=10, complete=False
        )
        is None
    )

    tail = json.loads((directory / "1'.json").read_text())
    tail["status"] = "forged"
    _write_row(directory, "1'", tail)
    with pytest.raises(PacketError, match="status"):
        _reconstruct_interval_directions(
            directory, receipt, labels=labels, scale=10, complete=False
        )


@pytest.mark.parametrize(
    "completed_directions",
    [
        ["0"],
        ["0", "0"],
        ["2", "0"],
        ["0", "missing"],
    ],
)
def test_partial_interval_readback_refuses_noncanonical_or_mismatched_direction_sets(
    tmp_path: Path, completed_directions: list[str]
) -> None:
    directory = tmp_path / "interval"
    labels = ("0", "1", "2")
    for label in labels:
        _write_row(directory, label, _interval_row_for(label))
    receipt: dict[str, object] = {
        "status": "partial",
        "directions_completed": 2,
        "completed_directions": completed_directions,
        "last": _interval_row_for("0"),
    }

    with pytest.raises(PacketError, match="completed directions"):
        _reconstruct_interval_directions(
            directory, receipt, labels=labels, scale=10, complete=False
        )


def test_partial_interval_last_row_must_belong_to_the_published_set(tmp_path: Path) -> None:
    directory = tmp_path / "interval"
    labels = ("0", "1", "2")
    for label in labels:
        _write_row(directory, label, _interval_row_for(label))
    receipt: dict[str, object] = {
        "status": "partial",
        "directions_completed": 2,
        "completed_directions": ["0", "1"],
        "last": _interval_row_for("2"),
    }

    with pytest.raises(PacketError, match="published direction"):
        _reconstruct_interval_directions(
            directory, receipt, labels=labels, scale=10, complete=False
        )


def test_partial_interval_readback_refuses_a_missing_published_row_hidden_by_tail(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "interval"
    labels = ("0", "1", "2")
    for label in ("0", "1"):
        _write_row(directory, label, _interval_row_for(label))
    receipt: dict[str, object] = {
        "status": "partial",
        "directions_completed": 2,
        "completed_directions": ["0", "2"],
        "last": _interval_row_for("0"),
    }

    with pytest.raises(PacketError, match="were not retained"):
        _reconstruct_interval_directions(
            directory, receipt, labels=labels, scale=10, complete=False
        )


def _dilation_row(index: int, label: str) -> dict[str, object]:
    return {"direction": index, "label": label, "minimum": "1"}


def test_partial_dilation_readback_binds_sparse_labels_and_validates_unpublished_tail(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "dilation"
    labels = ("zero", "one", "two", "three")
    for index in (0, 1, 3):
        _write_row(directory, str(index), _dilation_row(index, labels[index]))
    receipt: dict[str, object] = {
        "status": "partial",
        "directions_completed": 2,
        "completed_directions": ["zero", "three"],
        "last": _dilation_row(3, "three"),
    }

    _reconstruct_dilation_directions(directory, receipt, labels=labels, complete=False)

    tail = json.loads((directory / "1.json").read_text())
    tail["minimum"] = "01"
    _write_row(directory, "1", tail)
    with pytest.raises(PacketError, match="canonical exact form"):
        _reconstruct_dilation_directions(directory, receipt, labels=labels, complete=False)


@pytest.mark.parametrize(
    "completed_directions",
    [
        ["zero"],
        ["zero", "zero"],
        ["three", "zero"],
        ["zero", "missing"],
    ],
)
def test_partial_dilation_readback_refuses_noncanonical_or_mismatched_direction_sets(
    tmp_path: Path, completed_directions: list[str]
) -> None:
    directory = tmp_path / "dilation"
    labels = ("zero", "one", "two", "three")
    for index, label in enumerate(labels):
        _write_row(directory, str(index), _dilation_row(index, label))
    receipt: dict[str, object] = {
        "status": "partial",
        "directions_completed": 2,
        "completed_directions": completed_directions,
        "last": _dilation_row(0, "zero"),
    }

    with pytest.raises(PacketError, match="completed directions"):
        _reconstruct_dilation_directions(directory, receipt, labels=labels, complete=False)


def test_partial_dilation_last_row_must_belong_to_the_published_set(tmp_path: Path) -> None:
    directory = tmp_path / "dilation"
    labels = ("zero", "one", "two")
    for index, label in enumerate(labels):
        _write_row(directory, str(index), _dilation_row(index, label))
    receipt: dict[str, object] = {
        "status": "partial",
        "directions_completed": 2,
        "completed_directions": ["zero", "one"],
        "last": _dilation_row(2, "two"),
    }

    with pytest.raises(PacketError, match="published direction"):
        _reconstruct_dilation_directions(directory, receipt, labels=labels, complete=False)


def test_partial_dilation_readback_refuses_a_missing_published_row_hidden_by_tail(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "dilation"
    labels = ("zero", "one", "two")
    for index in (0, 1):
        _write_row(directory, str(index), _dilation_row(index, labels[index]))
    receipt: dict[str, object] = {
        "status": "partial",
        "directions_completed": 2,
        "completed_directions": ["zero", "two"],
        "last": _dilation_row(0, "zero"),
    }

    with pytest.raises(PacketError, match="were not retained"):
        _reconstruct_dilation_directions(directory, receipt, labels=labels, complete=False)


def test_partial_readback_uses_named_checkpoint_and_ignores_valid_unpublished_tail(
    tmp_path: Path,
) -> None:
    raw_directory = tmp_path / "raw"
    for index in range(2):
        _write_row(
            raw_directory,
            str(index),
            {"direction": index, "charge": str(index + 1), "witness": ["2", "3"]},
        )
    receipt = _raw_receipt(1, "1", 0, ["2", "3"])
    assert _reconstruct_raw_directions(
        raw_directory, receipt, expected=3, complete=False
    ) == RawMinimum(Fraction(1), 0, (Fraction(2), Fraction(3)), 1)

    (raw_directory / "1.json").rename(raw_directory / "2.json")
    row = json.loads((raw_directory / "2.json").read_text())
    row["direction"] = 2
    _write_row(raw_directory, "2", row)
    assert _reconstruct_raw_directions(
        raw_directory, receipt, expected=3, complete=False
    ) == RawMinimum(Fraction(1), 0, (Fraction(2), Fraction(3)), 1)


def test_partial_readback_accepts_a_fully_reported_sparse_completion_set(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "raw"
    for index in range(4):
        _write_row(
            directory,
            str(index),
            {
                "direction": index,
                "charge": str(index + 1),
                "witness": [str(index), str(index + 1)],
            },
        )
    receipt = _raw_receipt(2, "3", 2, ["2", "3"], completed_directions=(2, 3))

    assert _reconstruct_raw_directions(
        directory, receipt, expected=4, complete=False
    ) == RawMinimum(Fraction(3), 2, (Fraction(2), Fraction(3)), 2)


@pytest.mark.parametrize(
    ("completed", "indices"),
    [(1, []), (2, [0, 0]), (2, [1, 0]), (2, [0, 3])],
)
def test_partial_readback_refuses_forged_completed_direction_indices(
    tmp_path: Path, completed: int, indices: list[int]
) -> None:
    directory = tmp_path / "raw"
    for index in range(3):
        _write_row(
            directory,
            str(index),
            {"direction": index, "charge": str(index + 1), "witness": ["2", "3"]},
        )
    receipt = _raw_receipt(completed, "1", 0, ["2", "3"])
    receipt["completed_directions"] = indices

    with pytest.raises(PacketError, match="completed directions"):
        _reconstruct_raw_directions(directory, receipt, expected=3, complete=False)


def test_load_result_reads_a_retained_partial_prefix_without_promoting_it(
    tmp_path: Path,
) -> None:
    def interrupted(_certificate, *, progress, log, **_kwargs):
        _write_row(
            log,
            "0",
            {"direction": 0, "charge": "7/8", "witness": ["1", "1"]},
        )
        progress(1, (0,), Fraction(7, 8), 0, (Fraction(1), Fraction(1)))
        raise PacketDeadlineError("synthetic retained-prefix timeout")

    output, result = _execute(tmp_path, RAW_THRESHOLD + 1, raw_runner=interrupted)
    with patch("devtools.fixed_core_packet.source_manifest", return_value=MANIFEST):
        readback = load_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            require_supervision=False,
        )
    assert readback == result
    assert readback["status"] == "partial"
    assert readback["scientific_decision"] == "unresolved"


def test_public_readback_refuses_a_direct_unsupervised_worker_receipt(
    tmp_path: Path,
) -> None:
    output, _result = _execute(tmp_path, RAW_THRESHOLD)
    with pytest.raises(PacketError, match="parent supervisor"):
        load_result(output, repository=REPOSITORY, expected_revision=REVISION)


def test_readback_refuses_a_different_runtime_identity(tmp_path: Path) -> None:
    output, _result = _execute(tmp_path, RAW_THRESHOLD)
    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    runtime = cast(dict[str, object], cast(dict[str, object], saved["sources"])["runtime"])
    cast(dict[str, object], runtime["packages"])["numpy"] = "2.5.1"
    (output / "result.json").write_text(json.dumps(saved, indent=2) + "\n")
    with (
        patch("devtools.fixed_core_packet.source_manifest", return_value=MANIFEST),
        pytest.raises(PacketError, match="runtime differs"),
    ):
        load_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            require_supervision=False,
        )


def test_load_result_refuses_complete_acceptance_without_all_retained_rows(
    tmp_path: Path,
) -> None:
    output, _result = _execute(tmp_path, RAW_THRESHOLD + Fraction(1, 10**9))
    with (
        patch("devtools.fixed_core_packet.source_manifest", return_value=MANIFEST),
        pytest.raises(PacketError, match="missing or extra filenames"),
    ):
        load_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            require_supervision=False,
        )


def test_threshold_equality_rejects_before_normalization(tmp_path: Path) -> None:
    output, result = _execute(tmp_path, RAW_THRESHOLD)
    assert raw_decision(RAW_THRESHOLD) == "rejected"
    assert result["status"] == "complete"
    assert result["outcome"] == "raw-threshold-rejected"
    assert result["scientific_decision"] == "rejected"
    assert result["normalized"] is None
    assert not (output / "candidate.json").exists()


def test_real_final_raw_progress_waits_for_witness_replay_before_global_promotion(
    tmp_path: Path,
) -> None:
    def final_callback(_certificate, *, progress, **_kwargs):
        result = RawMinimum(
            RAW_THRESHOLD,
            0,
            (Fraction(1), Fraction(1)),
            RAW_DIRECTIONS,
        )
        progress(
            result.completed,
            tuple(range(result.completed)),
            result.minimum,
            result.direction,
            result.witness,
        )
        return result

    _output, result = _execute(tmp_path, RAW_THRESHOLD, raw_runner=final_callback)
    raw = cast(dict[str, object], result["raw"])
    assert result["status"] == "complete"
    assert result["outcome"] == "raw-threshold-rejected"
    assert raw["directions_completed"] == RAW_DIRECTIONS
    assert raw["raw_minimum"] == str(RAW_THRESHOLD)
    assert raw["witness_replay_charge"] == str(RAW_THRESHOLD)


def test_final_exact_progress_does_not_publish_an_impossible_partial_route(
    tmp_path: Path,
) -> None:
    def final_callback(_candidate, *, progress, **_kwargs):
        result = ExactRoute(
            Fraction(1),
            0,
            (Fraction(1), Fraction(1)),
            RAW_DIRECTIONS,
            0,
        )
        progress(
            result.completed,
            tuple(range(result.completed)),
            result.minimum,
            result.direction,
            result.witness,
        )
        return result

    _output, result = _execute(
        tmp_path,
        RAW_THRESHOLD + Fraction(1, 10**9),
        exact_runner=final_callback,
    )

    exact = cast(dict[str, object], cast(dict[str, object], result["routes"])["exact"])
    assert exact["status"] == "complete"
    assert exact["directions_completed"] == RAW_DIRECTIONS
    assert exact["completed_directions"] == list(range(RAW_DIRECTIONS))


def test_incomplete_exact_return_preserves_the_callback_completion_set(
    tmp_path: Path,
) -> None:
    def sparse_callback(_candidate, *, progress, **_kwargs):
        result = ExactRoute(
            Fraction(1),
            2,
            (Fraction(2), Fraction(3)),
            2,
            0,
        )
        progress(
            result.completed,
            (2, 3),
            result.minimum,
            result.direction,
            result.witness,
        )
        return result

    _output, result = _execute(
        tmp_path,
        RAW_THRESHOLD + Fraction(1, 10**9),
        exact_runner=sparse_callback,
    )

    exact = cast(dict[str, object], cast(dict[str, object], result["routes"])["exact"])
    assert result["status"] == "partial"
    assert exact["status"] == "partial"
    assert exact["directions_completed"] == 2
    assert exact["completed_directions"] == [2, 3]


def test_normalization_is_strict_explicit_and_uniquely_identified() -> None:
    _packet, source = load_packet_source(SOURCE)
    with pytest.raises(PacketError, match="complete raw minimum"):
        normalized_record(source, RAW_THRESHOLD, source_revision=REVISION)
    minimum = RAW_THRESHOLD + Fraction(1, 10**9)
    record = normalized_record(source, minimum, source_revision=REVISION)
    assert record["least_cell_charge"] == "1"
    assert record["id"] == "C-n011-threshold-191-50-bc329-B9981-10000-net2880"
    assert record["direction_steps"] == 2880
    assert record["square_side"] == "9981/10000"
    provenance = cast(dict[str, object], record["provenance"])
    assert provenance["derived_from"] == SOURCE_PATH
    assert provenance["normalization"] == f"every weight multiplied by {1 / minimum}"
    bc329 = cast(dict[str, object], provenance["bc329"])
    assert bc329 == {
        "source_path": SOURCE_PATH,
        "source_revision": REVISION,
        "source_git_blob": SOURCE_BLOB,
        "source_sha256": SOURCE_SHA256,
        "raw_minimum": str(minimum),
        "weight_scale": str(1 / minimum),
        "weight_transformation": (
            "multiply every point-atom and threshold-atom weight by weight_scale"
        ),
        "relative_weight_ratios_preserved": True,
        "core_side": "9981/10000",
        "direction_steps": 2880,
    }


def test_all_three_readers_bind_the_same_normalized_bytes(tmp_path: Path) -> None:
    output, result = _execute(tmp_path, RAW_THRESHOLD + Fraction(1, 10**9))
    candidate = (output / "candidate.json").read_bytes()
    digest = hashlib.sha256(candidate).hexdigest()
    assert result["status"] == "complete"
    assert result["scientific_decision"] == "accepted"
    normalized = cast(dict[str, object], result["normalized"])
    routes = cast(dict[str, object], result["routes"])
    assert normalized["sha256"] == digest
    assert cast(dict[str, object], routes["exact"])["minimum"] == "1"
    interval = cast(dict[str, object], routes["reflected_interval"])
    dilation = cast(dict[str, object], routes["dilation"])
    assert interval["enclosure"] == ["1", "1"]
    assert dilation["source_sha256"] == digest
    assert "completed_directions" not in interval
    assert "completed_directions" not in dilation


def test_route_disagreement_is_invalid_but_scientifically_unresolved(tmp_path: Path) -> None:
    def disagreement(*_args, **_kwargs) -> IntervalRoute:
        return IntervalRoute(Fraction(2), Fraction(2), INTERVAL_DIRECTIONS, 0, 0, accepted=True)

    _output, result = _execute(
        tmp_path,
        RAW_THRESHOLD + Fraction(1, 10**9),
        interval_runner=disagreement,
    )
    assert result["status"] == "invalid"
    assert result["outcome"] == "reader-disagreement"
    assert result["scientific_decision"] == "unresolved"


def test_complete_zero_width_interval_failure_is_reader_disagreement(tmp_path: Path) -> None:
    def complete_failure(*_args, **_kwargs) -> IntervalRoute:
        return IntervalRoute(
            Fraction(0), Fraction(0), INTERVAL_DIRECTIONS, 0, 0, accepted=False
        )

    _output, result = _execute(
        tmp_path,
        RAW_THRESHOLD + Fraction(1, 10**9),
        interval_runner=complete_failure,
    )
    assert result["status"] == "invalid"
    assert result["outcome"] == "reader-disagreement"
    assert result["scientific_decision"] == "unresolved"


def test_interval_stall_is_incomplete_and_scientifically_unresolved(tmp_path: Path) -> None:
    def stalled(*_args, **_kwargs) -> IntervalRoute:
        return IntervalRoute(
            Fraction(1), Fraction(2), INTERVAL_DIRECTIONS, 1, 0, accepted=False
        )

    _output, result = _execute(
        tmp_path,
        RAW_THRESHOLD + Fraction(1, 10**9),
        interval_runner=stalled,
    )
    assert result["status"] == "partial"
    assert result["outcome"] == "incomplete"
    assert result["scientific_decision"] == "unresolved"


def test_interval_progress_publishes_canonical_completed_labels(tmp_path: Path) -> None:
    def interrupted(_candidate, *, progress, log: Path, **_kwargs):
        for label in ("2'", "0"):
            outcome = fixed_core_packet.DirectionOutcome(
                label,
                "certified",
                10,
                10,
                (1.25, 2.5),
                1,
                0,
                budget_exhausted=False,
            )
            _write_row(log, label, _interval_row_for(label))
            progress(outcome)
        raise PacketDeadlineError("synthetic interval timeout")

    _output, result = _execute(
        tmp_path,
        RAW_THRESHOLD + Fraction(1, 10**9),
        interval_runner=interrupted,
    )
    assert result["status"] == "partial"
    assert result["phase"] == "timeout"
    interval = cast(
        dict[str, object], cast(dict[str, object], result["routes"])["reflected_interval"]
    )
    assert interval["directions_completed"] == 2
    assert interval["completed_directions"] == ["0", "2'"]
    assert cast(dict[str, object], interval["last"])["label"] == "0"


def test_dilation_progress_is_retained_before_a_deadline(tmp_path: Path) -> None:
    def interrupted(_path: Path, *, progress, **_kwargs):
        progress(2, Fraction(1), "2")
        progress(0, Fraction(1), "0")
        raise PacketDeadlineError("synthetic dilation timeout")

    output, result = _execute(
        tmp_path,
        RAW_THRESHOLD + Fraction(1, 10**9),
        dilation_runner=interrupted,
    )
    assert result["status"] == "partial"
    assert result["phase"] == "timeout"
    dilation = cast(dict[str, object], cast(dict[str, object], result["routes"])["dilation"])
    assert dilation["directions_completed"] == 2
    assert dilation["completed_directions"] == ["0", "2"]
    assert cast(dict[str, object], dilation["last"])["direction"] == 0
    row = json.loads((output / "dilation-directions" / "2.json").read_text())
    assert row == {"direction": 2, "label": "2", "minimum": "1"}


def test_raw_argmin_must_match_exact_admissible_membership_replay(tmp_path: Path) -> None:
    _output, result = _execute(
        tmp_path,
        RAW_THRESHOLD,
        raw_witness_replay=lambda _certificate, _result: (RAW_THRESHOLD + 1, True),
    )
    assert result["status"] == "invalid"
    assert result["scientific_decision"] == "unresolved"
    assert "membership replay" in cast(str, result["error"])


def test_partial_observed_minimum_never_becomes_global_or_sets_alpha(tmp_path: Path) -> None:
    def interrupted(_certificate, *, progress, **_kwargs):
        progress(1, (0,), Fraction(7, 8), 0, (Fraction(1), Fraction(1)))
        raise PacketDeadlineError("synthetic raw timeout")

    output, result = _execute(tmp_path, RAW_THRESHOLD + 1, raw_runner=interrupted)
    raw = cast(dict[str, object], result["raw"])
    assert result["status"] == "partial"
    assert result["scientific_decision"] == "unresolved"
    assert raw["directions_completed"] == 1
    assert raw["observed_minimum_upper_bound"] == "7/8"
    assert raw["raw_minimum"] is None
    assert result["normalized"] is None
    assert not (output / "candidate.json").exists()


@pytest.mark.parametrize("candidate_state", ["absent", "unpublished"])
def test_readback_accepts_the_raw_to_normalized_checkpoint_gap(
    tmp_path: Path, candidate_state: str
) -> None:
    minimum = RAW_THRESHOLD + Fraction(1, 10**9)
    output, result = _execute(tmp_path, minimum)
    result.update(
        {
            "status": "partial",
            "outcome": "incomplete",
            "scientific_decision": "unresolved",
            "phase": "raw-sweep",
            "normalized": None,
            "routes": {"exact": None, "reflected_interval": None, "dilation": None},
            "error": "normalization receipt has not been published",
        }
    )
    (output / "dilation.json").unlink()
    if candidate_state == "absent":
        (output / "candidate.json").unlink()
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")

    retained = RawMinimum(minimum, 0, (Fraction(1), Fraction(1)), RAW_DIRECTIONS)
    with (
        patch("devtools.fixed_core_packet.source_manifest", return_value=MANIFEST),
        patch(
            "devtools.fixed_core_packet._reconstruct_raw_directions",
            return_value=retained,
        ),
        patch(
            "devtools.fixed_core_packet.replay_raw_witness",
            return_value=(minimum, True),
        ) as replay,
    ):
        assert (
            load_result(
                output,
                repository=REPOSITORY,
                expected_revision=REVISION,
                require_supervision=False,
            )
            == result
        )
    replay.assert_called_once()
    assert replay.call_args.args[1] == retained


def test_readback_refuses_an_invalid_unpublished_candidate_tail(tmp_path: Path) -> None:
    minimum = RAW_THRESHOLD + Fraction(1, 10**9)
    output, result = _execute(tmp_path, minimum)
    result.update(
        {
            "status": "partial",
            "outcome": "incomplete",
            "scientific_decision": "unresolved",
            "phase": "timeout",
            "normalized": None,
            "routes": {"exact": None, "reflected_interval": None, "dilation": None},
            "error": "synthetic checkpoint gap",
        }
    )
    (output / "candidate.json").write_bytes(b"{}\n")
    (output / "dilation.json").unlink()
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")

    retained = RawMinimum(minimum, 0, (Fraction(1), Fraction(1)), RAW_DIRECTIONS)
    with (
        patch("devtools.fixed_core_packet.source_manifest", return_value=MANIFEST),
        patch(
            "devtools.fixed_core_packet._reconstruct_raw_directions",
            return_value=retained,
        ),
        patch(
            "devtools.fixed_core_packet.replay_raw_witness",
            return_value=(minimum, True),
        ),
        pytest.raises(PacketError, match="unpublished candidate"),
    ):
        load_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            require_supervision=False,
        )


def test_schema_refuses_normalization_gap_for_a_complete_acceptance(tmp_path: Path) -> None:
    _output, result = _execute(tmp_path, RAW_THRESHOLD + Fraction(1, 10**9))
    result.update(
        {
            "normalized": None,
            "routes": {"exact": None, "reflected_interval": None, "dilation": None},
        }
    )

    with pytest.raises(PacketError, match="not a checkpoint gap"):
        validate_result_document(result)


@pytest.mark.parametrize("candidate_state", ["absent", "unpublished", "corrupt"])
def test_normalization_failure_publishes_an_invalid_readable_raw_checkpoint(
    tmp_path: Path, candidate_state: str
) -> None:
    minimum = RAW_THRESHOLD + Fraction(1, 10**9)
    with patch(
        "devtools.fixed_core_packet.normalized_bytes",
        side_effect=PacketError("synthetic normalization failure"),
    ):
        output, result = _execute(tmp_path, minimum)

    assert result["status"] == "invalid"
    assert result["outcome"] == "invalid"
    assert result["scientific_decision"] == "unresolved"
    assert result["phase"] == "invalid"
    assert result["normalized"] is None
    assert result["routes"] == {
        "exact": None,
        "reflected_interval": None,
        "dilation": None,
    }

    candidate_path = output / "candidate.json"
    if candidate_state == "unpublished":
        _packet, source_record = load_packet_source(SOURCE)
        candidate_path.write_bytes(
            fixed_core_packet.normalized_bytes(
                source_record,
                minimum,
                source_revision=REVISION,
            )
        )
    elif candidate_state == "corrupt":
        candidate_path.write_bytes(b"{}\n")

    retained = RawMinimum(minimum, 0, (Fraction(1), Fraction(1)), RAW_DIRECTIONS)
    with (
        patch("devtools.fixed_core_packet.source_manifest", return_value=MANIFEST),
        patch(
            "devtools.fixed_core_packet._reconstruct_raw_directions",
            return_value=retained,
        ),
        patch(
            "devtools.fixed_core_packet.replay_raw_witness",
            return_value=(minimum, True),
        ),
    ):
        if candidate_state == "corrupt":
            with pytest.raises(PacketError, match="unpublished candidate"):
                load_result(
                    output,
                    repository=REPOSITORY,
                    expected_revision=REVISION,
                    require_supervision=False,
                )
        else:
            assert (
                load_result(
                    output,
                    repository=REPOSITORY,
                    expected_revision=REVISION,
                    require_supervision=False,
                )
                == result
            )


def test_source_manifest_refuses_a_stale_revision() -> None:
    with (
        patch(
            "devtools.fixed_core_packet.discover_implementation_paths",
            return_value=(SOURCE_PATH, T026_PATH),
        ),
        patch("devtools.fixed_core_packet._validate_loaded_modules"),
        patch("devtools.fixed_core_packet._git", return_value="b" * 40),
        pytest.raises(PacketError, match="current Git revision"),
    ):
        source_manifest(REPOSITORY, REVISION)


def test_git_execution_failure_has_operational_provenance() -> None:
    failure = subprocess.CompletedProcess(
        ("git", "status"),
        returncode=128,
        stdout="",
        stderr="synthetic repository failure\n",
    )
    with (
        patch("devtools.fixed_core_packet.subprocess.run", return_value=failure),
        pytest.raises(
            PacketOperationalError,
            match="git status failed with status 128: synthetic repository failure",
        ),
    ):
        fixed_core_packet._git(REPOSITORY, "status")  # noqa: SLF001 -- taxonomy boundary


@pytest.mark.parametrize("index_flag", ["--assume-unchanged", "--skip-worktree"])
def test_source_manifest_refuses_implementation_drift_hidden_from_git_status(
    tmp_path: Path, index_flag: str
) -> None:
    helper = "packing/devtools/source_guard.py"
    repository, revision = _repository_with_sources(tmp_path, (helper, b"VALUE = 1\n"))
    subprocess.run(
        ("git", "-C", str(repository), "update-index", index_flag, "--", helper),
        check=True,
        capture_output=True,
    )
    (repository / helper).write_bytes(b"VALUE = 2\n")
    assert (
        subprocess.run(
            ("git", "-C", str(repository), "status", "--porcelain"),
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        == ""
    )

    with (
        patch(
            "devtools.fixed_core_packet.discover_implementation_paths",
            return_value=(SOURCE_PATH, T026_PATH, helper),
        ),
        patch("devtools.fixed_core_packet._validate_loaded_modules"),
        pytest.raises(PacketError, match="bytes differ from the frozen Git blob"),
    ):
        source_manifest(repository, revision)


@pytest.mark.parametrize("relative_result", ["result", "nested/result", "*"])
def test_source_manifest_uses_a_literal_result_directory_exclusion(
    tmp_path: Path, relative_result: str
) -> None:
    repository, revision = _repository_with_sources(tmp_path)
    result_directory = repository / relative_result
    result_directory.mkdir(parents=True)
    (result_directory / "result.json").write_text("preflight\n")

    with (
        patch(
            "devtools.fixed_core_packet.discover_implementation_paths",
            return_value=(SOURCE_PATH, T026_PATH),
        ),
        patch("devtools.fixed_core_packet._validate_loaded_modules"),
    ):
        manifest = source_manifest(
            repository,
            revision,
            result_directory=result_directory,
        )
        assert {row["path"] for row in manifest} == {SOURCE_PATH, T026_PATH}

        (repository / "unrelated.txt").write_text("dirty\n")
        with pytest.raises(PacketError, match="checkout must be clean"):
            source_manifest(
                repository,
                revision,
                result_directory=result_directory,
            )


@pytest.mark.parametrize(
    ("tracked_path", "relative_result"),
    [
        ("reserved/result.json", "reserved"),
        ("reserved", "reserved"),
        ("reserved", "reserved/result"),
    ],
)
def test_source_manifest_refuses_a_result_directory_overlapping_tracked_output(
    tmp_path: Path, tracked_path: str, relative_result: str
) -> None:
    repository, revision = _repository_with_sources(
        tmp_path, (tracked_path, b"tracked output\n")
    )
    tracked = repository / tracked_path
    tracked.unlink()
    for parent in tracked.parents:
        if parent == repository or any(parent.iterdir()):
            break
        parent.rmdir()
    result_directory = repository / relative_result
    result_directory.mkdir(parents=True, exist_ok=True)
    (result_directory / "result.json").write_text("preflight\n")

    with (
        patch(
            "devtools.fixed_core_packet.discover_implementation_paths",
            return_value=(SOURCE_PATH, T026_PATH),
        ),
        patch("devtools.fixed_core_packet._validate_loaded_modules"),
        pytest.raises(PacketError, match="overlaps a path tracked"),
    ):
        source_manifest(
            repository,
            revision,
            result_directory=result_directory,
        )


def test_output_guard_rejects_normal_and_linked_worktree_git_data(tmp_path: Path) -> None:
    repository, revision = _repository_with_sources(tmp_path / "source")
    linked = tmp_path / "linked"
    subprocess.run(
        ("git", "-C", str(repository), "worktree", "add", "--detach", str(linked), revision),
        check=True,
        capture_output=True,
    )
    normal_git = Path(
        subprocess.run(
            ("git", "-C", str(repository), "rev-parse", "--absolute-git-dir"),
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    )
    linked_git = Path(
        subprocess.run(
            ("git", "-C", str(linked), "rev-parse", "--absolute-git-dir"),
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    )

    for checkout, destination in (
        (repository, normal_git / "refs" / "heads" / "forged"),
        (linked, linked_git / "nested"),
        (linked, normal_git / "worktrees" / "forged"),
    ):
        with pytest.raises(PacketError, match="Git administrative data"):
            fixed_core_packet.prepare_output_dir(destination, checkout)
        assert not destination.exists()


def test_output_guard_rejects_separate_git_directory(tmp_path: Path) -> None:
    checkout = tmp_path / "separate-checkout"
    administrative = tmp_path / "separate-admin"
    subprocess.run(
        ("git", "init", "-q", "--separate-git-dir", str(administrative), str(checkout)),
        check=True,
    )
    destination = administrative / "refs" / "heads" / "forged"

    with pytest.raises(PacketError, match="Git administrative data"):
        fixed_core_packet.prepare_output_dir(destination, checkout)
    assert not destination.exists()


def test_parent_output_guard_bounds_git_and_preserves_fresh_output(tmp_path: Path) -> None:
    output = tmp_path / "result"
    with (
        patch("devtools.fixed_core_packet.time.perf_counter", return_value=10.0),
        patch(
            "devtools.fixed_core_packet.subprocess.run",
            side_effect=subprocess.TimeoutExpired(("git", "rev-parse"), 2.0),
        ) as git,
        patch("devtools.fixed_core_packet.supervise_worker") as supervisor,
        pytest.raises(PacketDeadlineError, match="Git deadline reached"),
    ):
        main(
            [
                "--repository",
                str(REPOSITORY),
                "--expect-implementation-revision",
                REVISION,
                "--output-dir",
                str(output),
                "--scientific-seconds",
                "1",
                "--external-seconds",
                "2",
            ]
        )
    assert git.call_args.kwargs["timeout"] == 2.0
    supervisor.assert_not_called()
    assert not output.exists()


@pytest.mark.parametrize("readings", [[13.0], [10.0, 13.0]])
def test_output_guard_refuses_git_outside_its_deadline(
    tmp_path: Path, readings: list[float]
) -> None:
    output = tmp_path / "result"
    with (
        patch("devtools.fixed_core_packet.time.perf_counter", side_effect=readings),
        patch(
            "devtools.fixed_core_packet.subprocess.run",
            return_value=subprocess.CompletedProcess(
                ("git", "rev-parse"), 0, stdout=str(REPOSITORY / ".git"), stderr=""
            ),
        ) as git,
        pytest.raises(PacketDeadlineError, match="Git deadline reached"),
    ):
        fixed_core_packet.prepare_output_dir(output, REPOSITORY, deadline=12.0)
    assert git.call_count == len(readings) - 1
    assert not output.exists()


def test_scientific_readback_cannot_hide_unrelated_state_with_a_metachar_output(
    tmp_path: Path,
) -> None:
    packet_root = tmp_path / "packet"
    packet_root.mkdir()
    output, result = _execute(packet_root, RAW_THRESHOLD)
    repository, revision = _repository_with_sources(tmp_path / "fixture")
    result_directory = repository / "*"
    output.rename(result_directory)
    sources = cast(dict[str, object], result["sources"])
    sources["implementation_revision"] = revision
    (result_directory / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    (repository / "unrelated.txt").write_text("dirty\n")

    with (
        patch(
            "devtools.fixed_core_packet.discover_implementation_paths",
            return_value=(SOURCE_PATH, T026_PATH),
        ),
        patch("devtools.fixed_core_packet._validate_loaded_modules"),
        pytest.raises(PacketError, match="checkout must be clean"),
    ):
        load_result(
            result_directory,
            repository=repository,
            expected_revision=revision,
            require_supervision=False,
        )


@pytest.mark.parametrize("constant", ["NaN", "Infinity", "-Infinity"])
def test_strict_json_refuses_nonstandard_numeric_constants(constant: str) -> None:
    with pytest.raises(PacketError, match="nonstandard JSON constant"):
        _strict_json_bytes(f'{{"value": {constant}}}'.encode(), "synthetic result")


@pytest.mark.parametrize(
    ("scientific", "external", "grace"),
    [
        ("inf", "inf", "2"),
        ("1", "inf", "2"),
        ("1", "2", "nan"),
    ],
)
def test_cli_refuses_nonfinite_deadlines_before_source_work(
    tmp_path: Path, scientific: str, external: str, grace: str
) -> None:
    with pytest.raises(PacketError, match="must be finite"):
        main(
            [
                "--repository",
                str(REPOSITORY),
                "--expect-implementation-revision",
                REVISION,
                "--output-dir",
                str(tmp_path / "result"),
                "--scientific-seconds",
                scientific,
                "--external-seconds",
                external,
                "--grace-seconds",
                grace,
            ]
        )


def test_direct_worker_requires_parent_deadline_attestation(tmp_path: Path) -> None:
    with pytest.raises(PacketError, match="parent deadline attestation"):
        main(
            [
                "--worker",
                "--repository",
                str(REPOSITORY),
                "--expect-implementation-revision",
                REVISION,
                "--output-dir",
                str(tmp_path / "result"),
                "--scientific-seconds",
                "1",
                "--external-seconds",
                "2",
            ]
        )


def test_parent_launches_supervised_preflight_before_source_or_runtime_work(
    tmp_path: Path,
) -> None:
    output = tmp_path / "result"
    with (
        patch(
            "devtools.fixed_core_packet.source_manifest",
            side_effect=AssertionError("parent ran source preflight"),
        ),
        patch(
            "devtools.fixed_core_packet.runtime_binding",
            side_effect=AssertionError("parent ran runtime preflight"),
        ),
        patch("devtools.fixed_core_packet.supervise_worker", return_value=1) as supervisor,
    ):
        assert (
            main(
                [
                    "--repository",
                    str(REPOSITORY),
                    "--expect-implementation-revision",
                    REVISION,
                    "--output-dir",
                    str(output),
                    "--scientific-seconds",
                    "10",
                    "--external-seconds",
                    "20",
                ]
            )
            == 1
        )

    command = supervisor.call_args.args[0]
    assert "--worker" in command
    receipt = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    fixed_core_packet.validate_preflight_document(receipt)
    assert receipt["status"] == "partial"
    assert receipt["outcome"] == "preflight-pending"
    assert receipt["scientific_decision"] == "unresolved"
    with pytest.raises(PacketError, match="closed packet schema"):
        load_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
        )


def test_readback_refuses_changed_candidate_bytes(tmp_path: Path) -> None:
    output, result = _execute(tmp_path, RAW_THRESHOLD + Fraction(1, 10**9))
    candidate_path = output / "candidate.json"
    candidate = cast(dict[str, object], json.loads(candidate_path.read_bytes()))
    provenance = cast(dict[str, object], candidate["provenance"])
    cast(dict[str, object], provenance["bc329"])["source_revision"] = "b" * 40
    candidate_bytes = (json.dumps(candidate, indent=1) + "\n").encode()
    candidate_path.write_bytes(candidate_bytes)
    cast(dict[str, object], result["normalized"])["sha256"] = hashlib.sha256(
        candidate_bytes
    ).hexdigest()
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    with (
        patch("devtools.fixed_core_packet.source_manifest", return_value=MANIFEST),
        patch(
            "devtools.fixed_core_packet.replay_raw_witness",
            side_effect=lambda _certificate, result: (result.minimum, True),
        ),
        patch(
            "devtools.fixed_core_packet._reconstruct_raw_directions",
            return_value=RawMinimum(
                RAW_THRESHOLD + Fraction(1, 10**9),
                0,
                (Fraction(1), Fraction(1)),
                RAW_DIRECTIONS,
            ),
        ),
        pytest.raises(PacketError, match="normalized bytes"),
    ):
        load_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            require_supervision=False,
        )


def test_readback_rederives_dilation_instead_of_trusting_larger_saved_summary(
    tmp_path: Path,
) -> None:
    output, result = _execute(tmp_path, RAW_THRESHOLD + Fraction(1, 10**9))
    dilation_path = output / "dilation.json"
    dilation = cast(dict[str, object], json.loads(dilation_path.read_text()))
    conclusion = cast(dict[str, object], dilation["conclusion"])
    forged_squared = Fraction(cast(str, conclusion["bounded_side_squared"])) + 100
    conclusion["bounded_side_squared"] = str(forged_squared)
    dilation_bytes = (json.dumps(dilation, indent=2) + "\n").encode()
    dilation_path.write_bytes(dilation_bytes)
    route = cast(dict[str, object], cast(dict[str, object], result["routes"])["dilation"])
    route["bounded_side_squared"] = str(forged_squared)
    route["record_sha256"] = hashlib.sha256(dilation_bytes).hexdigest()
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    with (
        patch("devtools.fixed_core_packet.source_manifest", return_value=MANIFEST),
        patch(
            "devtools.fixed_core_packet.replay_raw_witness",
            side_effect=lambda _certificate, raw: (raw.minimum, True),
        ),
        patch(
            "devtools.fixed_core_packet._reconstruct_raw_directions",
            return_value=RawMinimum(
                RAW_THRESHOLD + Fraction(1, 10**9),
                0,
                (Fraction(1), Fraction(1)),
                RAW_DIRECTIONS,
            ),
        ),
        patch("devtools.fixed_core_packet._reconstruct_exact_directions"),
        patch("devtools.fixed_core_packet._reconstruct_interval_directions"),
        patch("devtools.fixed_core_packet._reconstruct_dilation_directions"),
        pytest.raises(PacketError, match=r"dilation record fields|rederived exact limit"),
    ):
        load_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            require_supervision=False,
        )


def test_outer_deadline_reaps_the_worker_process_group(tmp_path: Path) -> None:
    result = tmp_path / "missing-result.json"

    class Process:
        pid = 4321

        def __init__(self) -> None:
            self.waits = 0

        def wait(self, timeout: float | None = None) -> int:
            self.waits += 1
            if self.waits < 3:
                raise subprocess.TimeoutExpired("worker", timeout or 0)
            return -9

    process = Process()
    with (
        patch("devtools.fixed_core_packet.subprocess.Popen", return_value=process) as popen,
        patch(
            "devtools.fixed_core_packet.os.killpg",
            side_effect=_missing_group_on_probe,
        ) as killpg,
    ):
        assert (
            supervise_worker(("worker",), result, external_seconds=1.0, grace_seconds=0.1) == 1
        )
    popen.assert_called_once_with(("worker",), start_new_session=True)
    assert [call.args for call in killpg.call_args_list] == [
        (4321, 15),
        (4321, 9),
        (4321, 0),
    ]


def test_supervisor_deducts_parent_prelaunch_time_from_external_deadline(
    tmp_path: Path,
) -> None:
    waits: list[float | None] = []

    class Process:
        pid = 4321

        def wait(self, timeout: float | None = None) -> int:
            waits.append(timeout)
            return 0

    with (
        patch("devtools.fixed_core_packet.subprocess.Popen", return_value=Process()),
        patch(
            "devtools.fixed_core_packet.time.perf_counter",
            side_effect=[12.0, 13.0, 14.0],
        ),
        patch(
            "devtools.fixed_core_packet.os.killpg",
            side_effect=_missing_group_on_probe,
        ),
    ):
        assert (
            supervise_worker(
                ("worker",),
                tmp_path / "missing.json",
                external_seconds=10.0,
                grace_seconds=1.0,
                invocation_started=10.0,
                external_deadline=20.0,
            )
            == 0
        )
    assert waits == [7.0]


def test_supervisor_terminates_a_worker_when_launch_consumes_the_deadline(
    tmp_path: Path,
) -> None:
    result = tmp_path / "result.json"
    fixed_core_packet.write_result(
        result,
        fixed_core_packet.initial_preflight_document(
            REVISION,
            workers=1,
            scientific_seconds=5.0,
            external_seconds=10.0,
            grace_seconds=1.0,
        ),
    )

    class Process:
        pid = 4321

        def wait(self, timeout: float | None = None) -> int:
            assert timeout == 1.0
            return -signal.SIGTERM

    with (
        patch("devtools.fixed_core_packet.subprocess.Popen", return_value=Process()),
        patch(
            "devtools.fixed_core_packet.time.perf_counter",
            side_effect=[12.0, 21.0, 22.0, 22.0],
        ),
        patch(
            "devtools.fixed_core_packet.os.killpg",
            side_effect=_missing_group_on_probe,
        ) as killpg,
    ):
        assert (
            supervise_worker(
                ("worker",),
                result,
                external_seconds=10.0,
                grace_seconds=1.0,
                invocation_started=10.0,
                external_deadline=20.0,
            )
            == 1
        )
    assert [call.args for call in killpg.call_args_list] == [
        (4321, signal.SIGTERM),
        (4321, signal.SIGKILL),
        (4321, 0),
    ]
    receipt = cast(dict[str, object], json.loads(result.read_text()))
    assert receipt["outcome"] == "preflight-timeout"
    assert cast(dict[str, object], receipt["supervision"]) == {
        "status": "deadline-terminated",
        "worker_exit_status": -signal.SIGTERM,
        "supervisor_signal": None,
    }


def test_supervisor_refuses_to_launch_after_parent_deadline(tmp_path: Path) -> None:
    output, _result = _execute(tmp_path, RAW_THRESHOLD)
    with (
        patch("devtools.fixed_core_packet.subprocess.Popen") as popen,
        patch("devtools.fixed_core_packet.time.perf_counter", side_effect=[21.0, 21.0]),
    ):
        assert (
            supervise_worker(
                ("worker",),
                output / "result.json",
                external_seconds=10.0,
                grace_seconds=1.0,
                invocation_started=10.0,
                external_deadline=20.0,
            )
            == 1
        )
    popen.assert_not_called()
    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    assert saved["status"] == "partial"
    assert cast(dict[str, object], saved["supervision"])["status"] == ("deadline-before-launch")


def test_preflight_launch_failure_is_retained_as_operational_and_unresolved(
    tmp_path: Path,
) -> None:
    result = tmp_path / "result.json"
    fixed_core_packet.write_result(
        result,
        fixed_core_packet.initial_preflight_document(
            REVISION,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
        ),
    )
    with (
        patch(
            "devtools.fixed_core_packet.subprocess.Popen",
            side_effect=OSError("synthetic launch failure"),
        ),
        patch("devtools.fixed_core_packet.time.perf_counter", side_effect=[11.0, 12.0]),
    ):
        assert (
            supervise_worker(
                ("worker",),
                result,
                external_seconds=20.0,
                grace_seconds=2.0,
                invocation_started=10.0,
                external_deadline=30.0,
            )
            == 1
        )

    receipt = cast(dict[str, object], json.loads(result.read_text()))
    fixed_core_packet.validate_preflight_document(receipt)
    assert receipt["status"] == "partial"
    assert receipt["outcome"] == "preflight-failed"
    assert receipt["scientific_decision"] == "unresolved"
    assert receipt["error"] == "worker process launch failed: synthetic launch failure"
    assert cast(dict[str, object], receipt["supervision"]) == {
        "status": "launch-failed",
        "worker_exit_status": None,
        "supervisor_signal": None,
    }


def test_non_oserror_launch_failure_retains_type_message_and_returns_one(
    tmp_path: Path,
) -> None:
    result = tmp_path / "result.json"
    fixed_core_packet.write_result(
        result,
        fixed_core_packet.initial_preflight_document(
            REVISION,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
        ),
    )
    with (
        patch(
            "devtools.fixed_core_packet.subprocess.Popen",
            side_effect=MemoryError("synthetic host allocation failure"),
        ),
        patch("devtools.fixed_core_packet.time.perf_counter", side_effect=[11.0, 12.0]),
    ):
        status = supervise_worker(
            ("worker",),
            result,
            external_seconds=20.0,
            grace_seconds=2.0,
            invocation_started=10.0,
            external_deadline=30.0,
        )

    receipt = cast(dict[str, object], json.loads(result.read_text()))
    assert status == 1
    assert receipt["error"] == (
        "worker process launch failed: MemoryError: synthetic host allocation failure"
    )
    assert cast(dict[str, object], receipt["supervision"]) == {
        "status": "launch-failed",
        "worker_exit_status": None,
        "supervisor_signal": None,
    }


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX process groups are required")
def test_stalled_preflight_process_group_termination_reaps_a_grandchild(
    tmp_path: Path,
) -> None:
    pids = tmp_path / "pids"
    result = tmp_path / "result.json"
    fixed_core_packet.write_result(
        result,
        fixed_core_packet.initial_preflight_document(
            REVISION,
            workers=1,
            scientific_seconds=0.25,
            external_seconds=0.5,
            grace_seconds=2.0,
        ),
    )
    program = (
        "import os,signal,subprocess,sys; from pathlib import Path; "
        "child=subprocess.Popen([sys.executable,'-c','import signal; signal.pause()']); "
        f"Path({str(pids)!r}).write_text(f'{{os.getpid()}} {{child.pid}}'); "
        "signal.signal(signal.SIGTERM,lambda *_: (child.wait(),sys.exit(0))); "
        "signal.pause()"
    )
    assert (
        supervise_worker(
            (sys.executable, "-c", program),
            result,
            external_seconds=0.5,
            grace_seconds=2.0,
        )
        == 1
    )
    leader, child = (int(value) for value in pids.read_text().split())
    for pid in (leader, child):
        with pytest.raises(ProcessLookupError):
            os.kill(pid, 0)
    receipt = cast(dict[str, object], json.loads(result.read_text()))
    fixed_core_packet.validate_preflight_document(receipt)
    assert receipt["status"] == "partial"
    assert receipt["outcome"] == "preflight-timeout"
    assert receipt["scientific_decision"] == "unresolved"
    assert "external deadline" in cast(str, receipt["error"])
    assert cast(dict[str, object], receipt["supervision"])["status"] == ("deadline-terminated")


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX process groups are required")
def test_nonzero_leader_exit_reaps_a_sigterm_ignoring_grandchild(
    tmp_path: Path,
) -> None:
    child_pid_path = tmp_path / "grandchild-pid"
    child_program = f"""
import os
import signal
from pathlib import Path

signal.signal(signal.SIGTERM, signal.SIG_IGN)
Path({str(child_pid_path)!r}).write_text(str(os.getpid()))
signal.pause()
"""
    leader_program = f"""
import subprocess
import sys
import time
from pathlib import Path

child = subprocess.Popen([sys.executable, "-c", {child_program!r}])
ready = Path({str(child_pid_path)!r})
deadline = time.monotonic() + 5
while not ready.exists() and time.monotonic() < deadline:
    time.sleep(0.01)
sys.exit(1 if ready.exists() else 2)
"""
    child_pid: int | None = None
    try:
        assert (
            supervise_worker(
                (sys.executable, "-c", leader_program),
                tmp_path / "missing.json",
                external_seconds=5.0,
                grace_seconds=1.0,
            )
            == 1
        )
        child_pid = int(child_pid_path.read_text())
        with pytest.raises(ProcessLookupError):
            os.kill(child_pid, 0)
    finally:
        if child_pid is None and child_pid_path.exists():
            child_pid = int(child_pid_path.read_text())
        if child_pid is not None:
            with suppress(ProcessLookupError):
                os.kill(child_pid, signal.SIGKILL)


def test_recursive_import_closure_contains_each_retaining_reader() -> None:
    paths = discover_implementation_paths(REPOSITORY)
    assert "packing/devtools/fixed_core_packet.py" in paths
    assert "packing/devtools/decide_threshold_certificate.py" in paths
    assert "packing/devtools/dilation_corollary.py" in paths
    assert "packing/src/sqpack/fractional/threshold_interval.py" in paths
    assert SOURCE_PATH in paths
    assert T026_PATH in paths
    assert set(PROJECT_RUNTIME_PATHS) <= set(paths)


def test_runtime_binding_validates_the_project_environment_and_lock(tmp_path: Path) -> None:
    packing = tmp_path / "packing"
    environment = packing / ".venv"
    executable = environment / "bin" / "python"
    numpy_origin = environment / "lib" / "numpy" / "__init__.py"
    strif_origin = environment / "lib" / "strif" / "__init__.py"
    for path in (executable, numpy_origin, strif_origin):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"")
    (packing / ".python-version").write_text("3.14.7\n")
    (packing / "uv.lock").write_text(
        'version = 1\n[[package]]\nname = "numpy"\nversion = "2.5.2"\n'
        '[[package]]\nname = "strif"\nversion = "3.1.0"\n'
    )
    observation = RuntimeObservation(
        implementation="cpython",
        version="3.14.7",
        abi="cpython-314t-test",
        gil_enabled=False,
        environment=environment.resolve(),
        executable=executable.resolve(),
        resolved_executable=executable.resolve(),
        build="3.14.7 free-threaded test build",
        packages=(
            PackageRuntimeObservation("numpy", "2.5.2", "2.5.2", numpy_origin.resolve()),
            PackageRuntimeObservation("strif", "3.1.0", "3.1.0", strif_origin.resolve()),
        ),
    )
    binding = runtime_binding(tmp_path, observer=lambda: observation)
    assert binding["packages"] == {"numpy": "2.5.2", "strif": "3.1.0"}
    assert cast(dict[str, object], binding["python"])["environment"] == str(
        environment.resolve()
    )

    wrong_environment = RuntimeObservation(
        implementation=observation.implementation,
        version=observation.version,
        abi=observation.abi,
        gil_enabled=observation.gil_enabled,
        environment=tmp_path,
        executable=observation.executable,
        resolved_executable=observation.resolved_executable,
        build=observation.build,
        packages=observation.packages,
    )
    with pytest.raises(PacketError, match=r"repository packing/\.venv"):
        runtime_binding(tmp_path, observer=lambda: wrong_environment)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("bounded_side_squared", "1"),
        ("relation", ">"),
        ("endpoint_certificate", True),
    ],
)
def test_t026_semantics_are_strict(field: str, value: object) -> None:
    forged = cast(dict[str, object], json.loads(T026_BYTES))
    cast(dict[str, object], forged["conclusion"])[field] = value
    with pytest.raises(PacketError, match="published lower-bound claim"):
        load_t026_reference(json.dumps(forged).encode())


def test_nested_tampering_and_impossible_complete_state_are_refused(tmp_path: Path) -> None:
    output, result = _execute(tmp_path, RAW_THRESHOLD)
    result["scientific_decision"] = "unresolved"
    with pytest.raises(PacketError, match="complete result"):
        validate_result_document(result)

    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    settings = cast(dict[str, object], saved["settings"])
    settings["direction_steps"] = 1440
    with pytest.raises(PacketError, match="settings"):
        validate_result_document(saved)

    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    sources = cast(dict[str, object], saved["sources"])
    sources["source_path"] = "/tmp/source.json"
    with pytest.raises(PacketError, match="source paths"):
        validate_result_document(saved)

    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    settings = cast(dict[str, object], saved["settings"])
    settings["normalization"] = "alpha chosen after inspection"
    with pytest.raises(PacketError, match="settings"):
        validate_result_document(saved)

    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    sources = cast(dict[str, object], saved["sources"])
    assert sources["source_git_blob"] == SOURCE_BLOB
    assert sources["t026_git_blob"] == T026_BLOB
    sources["source_git_blob"] = "f" * 40
    with pytest.raises(PacketError, match="source identities"):
        validate_result_document(saved)

    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    runtime = cast(dict[str, object], cast(dict[str, object], saved["sources"])["runtime"])
    cast(dict[str, object], runtime["packages"])["scipy"] = "1.0"
    with pytest.raises(PacketError, match="runtime"):
        validate_result_document(saved)

    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    sources = cast(dict[str, object], saved["sources"])
    manifest = cast(list[dict[str, str]], sources["manifest"])
    sources["manifest"] = [row for row in manifest if row["path"] != "packing/pyproject.toml"]
    with pytest.raises(PacketError, match="incomplete"):
        validate_result_document(saved)


def test_executed_source_bytes_must_match_the_prevalidated_manifest(tmp_path: Path) -> None:
    output = tmp_path / "race"
    output.mkdir()
    with pytest.raises(PacketError, match="executed T-026 bytes"):
        execute_packet(
            SOURCE,
            T026_BYTES + b" ",
            revision=REVISION,
            manifest=MANIFEST,
            runtime=RUNTIME,
            output_dir=output,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
            process_deadline=100.0,
            clock=lambda: 0.0,
            raw_runner=_raw(RAW_THRESHOLD),
            exact_runner=_exact,
            interval_runner=_interval,
            dilation_runner=_dilation,
            raw_witness_replay=lambda _certificate, result: (result.minimum, True),
        )


@pytest.mark.parametrize("kind", ["invalid", "partial"])
def test_nonzero_worker_exit_preserves_valid_receipt_classification(
    tmp_path: Path, kind: str
) -> None:
    if kind == "invalid":

        def disagreement(*_args, **_kwargs) -> IntervalRoute:
            return IntervalRoute(
                Fraction(2), Fraction(2), INTERVAL_DIRECTIONS, 0, 0, accepted=True
            )

        output, result = _execute(
            tmp_path,
            RAW_THRESHOLD + Fraction(1, 10**9),
            interval_runner=disagreement,
        )
        exit_status = 2
    else:

        def interrupted(_certificate, *, progress, **_kwargs):
            progress(1, (0,), Fraction(7, 8), 0, (Fraction(1), Fraction(1)))
            raise PacketDeadlineError("precise synthetic timeout")

        output, result = _execute(
            tmp_path,
            RAW_THRESHOLD + 1,
            raw_runner=interrupted,
        )
        exit_status = 1

    class Process:
        pid = 4321

        def wait(self, timeout: float | None = None) -> int:
            del timeout
            return exit_status

    with (
        patch("devtools.fixed_core_packet.subprocess.Popen", return_value=Process()),
        patch(
            "devtools.fixed_core_packet.os.killpg",
            side_effect=_missing_group_on_probe,
        ),
    ):
        assert (
            supervise_worker(
                ("worker",),
                output / "result.json",
                external_seconds=1.0,
                grace_seconds=0.1,
            )
            == exit_status
        )
    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    assert saved["status"] == kind
    assert saved["outcome"] == result["outcome"]
    supervision = cast(dict[str, object], saved["supervision"])
    assert supervision == {
        "status": "observed-exit",
        "worker_exit_status": exit_status,
        "supervisor_signal": None,
    }


def test_external_kill_replaces_a_stale_partial_phase_with_timeout(tmp_path: Path) -> None:
    def interrupted(_certificate, *, progress, **_kwargs):
        progress(1, (0,), Fraction(7, 8), 0, (Fraction(1), Fraction(1)))
        raise PacketDeadlineError("synthetic raw timeout")

    output, result = _execute(tmp_path, RAW_THRESHOLD + 1, raw_runner=interrupted)
    result["phase"] = "raw-sweep"
    result["error"] = "raw sweep is incomplete"
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")

    class Process:
        pid = 4321

        def __init__(self) -> None:
            self.waits = 0

        def wait(self, timeout: float | None = None) -> int:
            self.waits += 1
            if self.waits == 1:
                raise subprocess.TimeoutExpired("worker", timeout or 0)
            return -15

    with (
        patch("devtools.fixed_core_packet.subprocess.Popen", return_value=Process()),
        patch(
            "devtools.fixed_core_packet.os.killpg",
            side_effect=_missing_group_on_probe,
        ) as killpg,
    ):
        assert (
            supervise_worker(
                ("worker",),
                output / "result.json",
                external_seconds=1.0,
                grace_seconds=0.1,
            )
            == 1
        )
    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    assert saved["status"] == "partial"
    assert saved["phase"] == "timeout"
    assert "external deadline" in cast(str, saved["error"])
    assert [call.args for call in killpg.call_args_list] == [
        (4321, 15),
        (4321, 9),
        (4321, 0),
    ]
    clocks = cast(dict[str, object], saved["clocks"])
    assert cast(float, clocks["external_lifetime_seconds"]) >= 0


def test_parent_interruption_reaps_group_and_retains_partial_receipt(tmp_path: Path) -> None:
    output, _result = _execute(tmp_path, RAW_THRESHOLD)

    class Process:
        pid = 4321

        def __init__(self) -> None:
            self.waits = 0

        def wait(self, timeout: float | None = None) -> int:
            del timeout
            self.waits += 1
            if self.waits == 1:
                raise KeyboardInterrupt
            return -15

    with (
        patch("devtools.fixed_core_packet.subprocess.Popen", return_value=Process()),
        patch(
            "devtools.fixed_core_packet.os.killpg",
            side_effect=_missing_group_on_probe,
        ) as killpg,
        pytest.raises(KeyboardInterrupt),
    ):
        supervise_worker(
            ("worker",),
            output / "result.json",
            external_seconds=1.0,
            grace_seconds=0.1,
        )
    assert [call.args for call in killpg.call_args_list] == [
        (4321, 15),
        (4321, 9),
        (4321, 0),
    ]
    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    assert saved["status"] == "partial"
    assert saved["phase"] == "incomplete"
    assert "KeyboardInterrupt" in cast(str, saved["error"])
    assert cast(dict[str, object], saved["supervision"])["status"] == ("supervisor-interrupted")


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX signals are required")
@pytest.mark.parametrize(
    ("signal_number", "delivery_phase"),
    [(signal.SIGTERM, "waiting"), (signal.SIGHUP, "launch"), (signal.SIGINT, "launch")],
)
def test_posix_signal_reaps_a_live_worker_and_closes_the_preflight_receipt(
    tmp_path: Path, signal_number: signal.Signals, delivery_phase: str
) -> None:
    result = tmp_path / "result.json"
    ready_path = tmp_path / "supervisor-ready"
    fixed_core_packet.write_result(
        result,
        fixed_core_packet.initial_preflight_document(
            REVISION,
            workers=1,
            scientific_seconds=20.0,
            external_seconds=30.0,
            grace_seconds=1.0,
        ),
    )
    worker_program = "import signal; signal.pause()"
    supervisor_program = "\n".join(
        (
            "import os, signal, subprocess, sys, time",
            "from pathlib import Path",
            "from devtools import fixed_core_packet as packet",
            "real_popen = subprocess.Popen",
            f"command = (sys.executable, '-c', {worker_program!r})",
            f"result = Path({str(result)!r})",
            f"ready = Path({str(ready_path)!r})",
            f"during_launch = {delivery_phase == 'launch'!r}",
            f"signal_number = {int(signal_number)!r}",
            "def launch(command, *, start_new_session):",
            "    process = real_popen(command, start_new_session=start_new_session)",
            "    temporary = ready.with_suffix('.partial')",
            "    temporary.write_text(str(process.pid))",
            "    temporary.replace(ready)",
            "    if during_launch:",
            "        os.kill(os.getpid(), signal_number)",
            "        time.sleep(0.05)",
            "    return process",
            "packet.subprocess.Popen = launch",
            "packet.supervise_worker(command, result, external_seconds=30., grace_seconds=1.)",
        )
    )
    supervisor = subprocess.Popen((sys.executable, "-c", supervisor_program))
    worker_pid: int | None = None
    try:
        deadline = time.monotonic() + 5.0
        while not ready_path.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        worker_pid = int(ready_path.read_text())
        if delivery_phase == "waiting":
            os.kill(supervisor.pid, signal_number)
        assert supervisor.wait(timeout=5.0) == -signal_number
        deadline = time.monotonic() + 1.0
        while time.monotonic() < deadline:
            try:
                os.kill(worker_pid, 0)
            except ProcessLookupError:
                break
            time.sleep(0.01)
        with pytest.raises(ProcessLookupError):
            os.kill(worker_pid, 0)
    finally:
        if supervisor.poll() is None:
            supervisor.terminate()
            try:
                supervisor.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                supervisor.kill()
                supervisor.wait(timeout=2.0)
        if worker_pid is None and ready_path.exists():
            worker_pid = int(ready_path.read_text())
        if worker_pid is not None:
            with suppress(ProcessLookupError):
                os.kill(worker_pid, signal.SIGKILL)

    receipt = cast(dict[str, object], json.loads(result.read_text()))
    fixed_core_packet.validate_preflight_document(receipt)
    assert receipt["status"] == "partial"
    assert receipt["outcome"] == "preflight-failed"
    assert receipt["scientific_decision"] == "unresolved"
    assert receipt["error"] == (
        f"supervisor interrupted by {signal_number.name} ({signal_number.value})"
    )
    assert cast(dict[str, object], receipt["supervision"]) == {
        "status": "supervisor-interrupted",
        "worker_exit_status": -signal.SIGTERM,
        "supervisor_signal": signal_number,
    }


def test_signal_handler_delivery_during_cleanup_cannot_abandon_the_group(
    tmp_path: Path,
) -> None:
    result = tmp_path / "result.json"
    fixed_core_packet.write_result(
        result,
        fixed_core_packet.initial_preflight_document(
            REVISION,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=1.0,
        ),
    )
    previous_handler = signal.getsignal(signal.SIGTERM)

    class Process:
        pid = 4321

        def __init__(self) -> None:
            self.waits = 0

        def wait(self, timeout: float | None = None) -> int:
            del timeout
            self.waits += 1
            handler = signal.getsignal(signal.SIGTERM)
            assert callable(handler)
            # A signal received by another eligible thread can queue Python's
            # main-thread handler even while the main thread masks that signal.
            handler(signal.SIGTERM, None)
            return -signal.SIGTERM

    process = Process()
    with (
        patch("devtools.fixed_core_packet.subprocess.Popen", return_value=process),
        patch(
            "devtools.fixed_core_packet.os.killpg", side_effect=_missing_group_on_probe
        ) as killpg,
        patch("devtools.fixed_core_packet.signal.raise_signal") as reraised,
    ):
        assert (
            supervise_worker(("worker",), result, external_seconds=20.0, grace_seconds=1.0)
            == 128 + signal.SIGTERM
        )
    assert process.waits == 2
    assert [call.args for call in killpg.call_args_list] == [
        (process.pid, signal.SIGTERM),
        (process.pid, signal.SIGKILL),
        (process.pid, 0),
    ]
    reraised.assert_called_once_with(signal.SIGTERM)
    assert signal.getsignal(signal.SIGTERM) == previous_handler
    receipt = cast(dict[str, object], json.loads(result.read_text()))
    assert receipt["outcome"] == "preflight-failed"
    assert cast(dict[str, object], receipt["supervision"]) == {
        "status": "supervisor-interrupted",
        "worker_exit_status": -signal.SIGTERM,
        "supervisor_signal": signal.SIGTERM,
    }


def test_unexpected_worker_failure_preserves_completed_direction_files(
    tmp_path: Path,
) -> None:
    def interrupted(_certificate, *, progress, log, **_kwargs):
        _write_row(
            log,
            "0",
            {"direction": 0, "charge": "7/8", "witness": ["1", "1"]},
        )
        progress(1, (0,), Fraction(7, 8), 0, (Fraction(1), Fraction(1)))
        raise PacketDeadlineError("synthetic retained-prefix timeout")

    output, _result = _execute(tmp_path, RAW_THRESHOLD + 1, raw_runner=interrupted)
    with (
        patch("devtools.fixed_core_packet.source_manifest", return_value=MANIFEST),
        patch("devtools.fixed_core_packet.execute_packet", side_effect=MemoryError("oom")),
        patch("devtools.fixed_core_packet.time.perf_counter", side_effect=[10.0, 11.0]),
    ):
        status = run_worker(
            REPOSITORY,
            REVISION,
            output,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
        )
    assert status == 1
    assert (output / "raw-directions" / "0.json").is_file()
    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    assert saved["status"] == "partial"
    assert saved["scientific_decision"] == "unresolved"
    assert "MemoryError: oom" in cast(str, saved["error"])


def test_child_source_race_reclassifies_the_seed_as_invalid(tmp_path: Path) -> None:
    def interrupted(_certificate, *, progress, **_kwargs):
        progress(1, (0,), Fraction(7, 8), 0, (Fraction(1), Fraction(1)))
        raise PacketDeadlineError("synthetic raw timeout")

    output, _result = _execute(tmp_path, RAW_THRESHOLD + 1, raw_runner=interrupted)
    with (
        patch(
            "devtools.fixed_core_packet.source_manifest",
            side_effect=PacketError("synthetic source race"),
        ),
        patch("devtools.fixed_core_packet.time.perf_counter", side_effect=[10.0, 11.0]),
    ):
        status = run_worker(
            REPOSITORY,
            REVISION,
            output,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
        )
    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    assert status == 2
    assert saved["status"] == "invalid"
    assert saved["outcome"] == "invalid"
    assert saved["scientific_decision"] == "unresolved"
    assert saved["phase"] == "invalid"
    assert saved["error"] == "synthetic source race"
    clocks = cast(dict[str, object], saved["clocks"])
    assert clocks["process_seconds"] == 1.0


def test_preflight_source_failure_is_retained_without_a_packet_receipt(
    tmp_path: Path,
) -> None:
    output = tmp_path / "preflight-source-failure"
    output.mkdir()
    fixed_core_packet.write_result(
        output / "result.json",
        fixed_core_packet.initial_preflight_document(
            REVISION,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
        ),
    )
    with (
        patch(
            "devtools.fixed_core_packet.source_manifest",
            side_effect=PacketError("synthetic source preflight failure"),
        ),
        patch("devtools.fixed_core_packet.time.perf_counter", side_effect=[10.0, 11.0]),
    ):
        status = run_worker(
            REPOSITORY,
            REVISION,
            output,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
        )

    assert status == 2
    receipt = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    fixed_core_packet.validate_preflight_document(receipt)
    assert receipt["status"] == "invalid"
    assert receipt["outcome"] == "preflight-invalid"
    assert receipt["scientific_decision"] == "unresolved"
    assert receipt["error"] == "synthetic source preflight failure"
    assert receipt["clocks"] == {
        "process_seconds": 1.0,
        "external_lifetime_seconds": None,
    }


@pytest.mark.parametrize(
    "failure",
    [
        OSError("synthetic source I/O failure"),
        PacketOperationalError("synthetic Git execution failure"),
    ],
)
def test_operational_preflight_failure_remains_partial_and_unresolved(
    tmp_path: Path, failure: Exception
) -> None:
    output = tmp_path / "operational-preflight-failure"
    output.mkdir()
    fixed_core_packet.write_result(
        output / "result.json",
        fixed_core_packet.initial_preflight_document(
            REVISION,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
        ),
    )
    with (
        patch("devtools.fixed_core_packet.source_manifest", side_effect=failure),
        patch("devtools.fixed_core_packet.time.perf_counter", side_effect=[10.0, 11.0]),
    ):
        status = run_worker(
            REPOSITORY,
            REVISION,
            output,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
        )

    assert status == 1
    receipt = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    fixed_core_packet.validate_preflight_document(receipt)
    assert receipt["status"] == "partial"
    assert receipt["outcome"] == "preflight-failed"
    assert receipt["scientific_decision"] == "unresolved"
    assert receipt["error"] == (
        f"operational preflight failure: {type(failure).__name__}: {failure}"
    )
    with pytest.raises(PacketError, match="closed packet schema"):
        load_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            require_supervision=False,
        )


def test_uv_lock_read_oserror_stays_operational_through_worker_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "uv-lock-io"
    output.mkdir()
    fixed_core_packet.write_result(
        output / "result.json",
        fixed_core_packet.initial_preflight_document(
            REVISION,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
        ),
    )
    original_read_text = Path.read_text
    monkeypatch.setattr(fixed_core_packet, "runtime_binding", runtime_binding)

    def read_text(
        path: Path,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> str:
        if path.resolve() == (REPOSITORY / "packing" / "uv.lock").resolve():
            raise OSError("synthetic uv.lock I/O failure")
        return original_read_text(path, encoding=encoding, errors=errors, newline=newline)

    with (
        patch("devtools.fixed_core_packet.source_manifest", return_value=MANIFEST),
        patch.object(Path, "read_text", read_text),
        patch("devtools.fixed_core_packet.time.perf_counter", side_effect=[10.0, 11.0]),
    ):
        status = run_worker(
            REPOSITORY,
            REVISION,
            output,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
        )

    receipt = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    assert status == 1
    assert receipt["status"] == "partial"
    assert receipt["outcome"] == "preflight-failed"
    assert receipt["scientific_decision"] == "unresolved"
    assert receipt["error"] == (
        "operational preflight failure: PacketOperationalError: "
        "could not read the bound uv.lock: OSError: synthetic uv.lock I/O failure"
    )


def test_worker_republishes_complete_receipt_after_readback_with_end_to_end_clock(
    tmp_path: Path,
) -> None:
    output, complete = _execute(tmp_path, RAW_THRESHOLD)
    with (
        patch("devtools.fixed_core_packet.source_manifest", return_value=MANIFEST),
        patch("devtools.fixed_core_packet.execute_packet", return_value=complete),
        patch("devtools.fixed_core_packet.load_result", return_value=complete) as readback,
        patch("devtools.fixed_core_packet.time.perf_counter", side_effect=[10.0, 12.0, 12.0]),
    ):
        status = run_worker(
            REPOSITORY,
            REVISION,
            output,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
        )
    readback.assert_called_once()
    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    assert status == 0
    assert saved["status"] == "complete"
    clocks = cast(dict[str, object], saved["clocks"])
    assert clocks["scientific_seconds"] == 2.0
    assert clocks["process_seconds"] == 2.0


def test_readback_finishing_past_scientific_deadline_revokes_acceptance(
    tmp_path: Path,
) -> None:
    output, complete = _execute(tmp_path, RAW_THRESHOLD)
    with (
        patch("devtools.fixed_core_packet.source_manifest", return_value=MANIFEST),
        patch("devtools.fixed_core_packet.execute_packet", return_value=complete),
        patch("devtools.fixed_core_packet.load_result", return_value=complete),
        patch("devtools.fixed_core_packet.time.perf_counter", side_effect=[10.0, 21.0]),
    ):
        status = run_worker(
            REPOSITORY,
            REVISION,
            output,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
        )
    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    assert status == 1
    assert saved["status"] == "partial"
    assert saved["scientific_decision"] == "unresolved"
    assert saved["phase"] == "timeout"
    assert "independent readback" in cast(str, saved["error"])


def test_final_receipt_publication_past_scientific_deadline_revokes_acceptance(
    tmp_path: Path,
) -> None:
    output, complete = _execute(tmp_path, RAW_THRESHOLD)
    now = 19.0
    writes = 0
    original_write = fixed_core_packet.write_result

    def write_result(path: Path, document: dict[str, object]) -> None:
        nonlocal now, writes
        original_write(path, document)
        writes += 1
        if writes == 1:
            now = 21.0

    with (
        patch("devtools.fixed_core_packet.source_manifest", return_value=MANIFEST),
        patch("devtools.fixed_core_packet.execute_packet", return_value=complete),
        patch("devtools.fixed_core_packet.load_result", return_value=complete),
        patch("devtools.fixed_core_packet.time.perf_counter", side_effect=lambda: now),
        patch("devtools.fixed_core_packet.write_result", side_effect=write_result),
    ):
        status = run_worker(
            REPOSITORY,
            REVISION,
            output,
            workers=1,
            scientific_seconds=10.0,
            external_seconds=20.0,
            grace_seconds=2.0,
            invocation_started=10.0,
        )
    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    assert status == 1
    assert writes == 2
    assert saved["status"] == "partial"
    assert saved["scientific_decision"] == "unresolved"
    assert saved["phase"] == "timeout"
    assert "final receipt publication" in cast(str, saved["error"])
    assert cast(dict[str, object], saved["clocks"])["scientific_seconds"] == 11.0


@pytest.mark.parametrize("clock", ["scientific_seconds", "process_seconds"])
def test_complete_receipt_refuses_an_elapsed_scientific_budget(
    tmp_path: Path, clock: str
) -> None:
    _output, complete = _execute(tmp_path, RAW_THRESHOLD)
    cast(dict[str, object], complete["clocks"])[clock] = 10.0
    with pytest.raises(PacketError, match="complete receipt exceeds its scientific deadline"):
        validate_result_document(complete)


def test_raw_completion_past_the_scientific_budget_stays_unresolved(tmp_path: Path) -> None:
    now = 0.0
    raw_runner = _raw(RAW_THRESHOLD)

    def finish_late(certificate: ThresholdCertificate, **kwargs) -> RawMinimum:
        nonlocal now
        result = raw_runner(certificate, **kwargs)
        now = 11.0
        return result

    output, result = _execute(
        tmp_path, RAW_THRESHOLD, clock=lambda: now, raw_runner=finish_late
    )
    assert result["status"] == "partial"
    assert result["scientific_decision"] == "unresolved"
    assert result["phase"] == "timeout"
    assert "scientific deadline reached" in cast(str, result["error"])
    assert cast(dict[str, object], json.loads((output / "result.json").read_text())) == result


def test_unexpected_nonzero_worker_exit_revokes_a_complete_receipt(tmp_path: Path) -> None:
    output, _complete = _execute(tmp_path, RAW_THRESHOLD)

    class Process:
        pid = 4321

        def wait(self, timeout: float | None = None) -> int:
            del timeout
            return 3

    with (
        patch("devtools.fixed_core_packet.subprocess.Popen", return_value=Process()),
        patch(
            "devtools.fixed_core_packet.os.killpg",
            side_effect=_missing_group_on_probe,
        ),
    ):
        assert (
            supervise_worker(
                ("worker",),
                output / "result.json",
                external_seconds=1.0,
                grace_seconds=0.1,
            )
            == 3
        )
    saved = cast(dict[str, object], json.loads((output / "result.json").read_text()))
    assert saved["status"] == "partial"
    assert saved["outcome"] == "incomplete"
    assert saved["scientific_decision"] == "unresolved"
    assert "unexpectedly with status 3" in cast(str, saved["error"])
