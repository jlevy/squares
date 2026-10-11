"""Fail-closed controls for the resident exact-geometry process boundary."""

from __future__ import annotations

import hashlib
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from sqpack import rectangle_density
from sqpack.rectangle_density import (
    CandidateError,
    DensityRectangle,
    RectangleDensityCandidate,
    load_candidate,
    verify_candidate,
)
from sqpack.rust_rectangle_geometry import RustRectangleGeometry

if TYPE_CHECKING:
    import subprocess

PACKING = Path(__file__).resolve().parents[1]
ANALYTIC = PACKING / "resources/web/wand125-tools-2026-09-29/native-analytic-control.json"


def _fake_server(tmp_path: Path, mode: str) -> Path:
    binary = tmp_path / f"fake-{mode}"
    source = f"""#!{sys.executable}
import hashlib
import json
import sys
import time

mode = {mode!r}
opening = sys.stdin.buffer.readline().rstrip(b"\\n")
digest = hashlib.sha256(opening).hexdigest()
count = len(json.loads(opening)["rectangles"])
ready = {{"version": 1, "status": "ready", "table_sha256": digest, "rectangle_count": count}}
sys.stdout.write(json.dumps(ready) + "\\n")
sys.stdout.flush()
if mode == "rebuild":
    with open({str(binary)!r}, "a", encoding="utf-8") as rebuilt:
        rebuilt.write("# rebuilt while the verifier ran\\n")
for line in sys.stdin.buffer:
    query = json.loads(line)
    if mode == "partial":
        sys.stdout.write('{{"version":')
        sys.stdout.flush()
        time.sleep(5)
    response = {{"version": 1, "sequence": query["sequence"], "table_sha256": digest,
                "coverages": ["1"] * len(query["polygons"])}}
    if mode == "wrong_sequence":
        response["sequence"] += 1
    if mode == "duplicate_key":
        sys.stdout.write('{{"version":1,"version":1}}\\n')
    else:
        sys.stdout.write(json.dumps(response) + "\\n")
    sys.stdout.flush()
    if mode in ("wrong_sequence", "duplicate_key"):
        break
if mode == "extra_output":
    sys.stdout.write('unsolicited\\n')
    sys.stdout.flush()
if mode == "shutdown_hang":
    time.sleep(5)
"""
    binary.write_text(source, encoding="utf-8")
    binary.chmod(0o700)
    return binary


def _candidate() -> RectangleDensityCandidate:
    return load_candidate(ANALYTIC, n=3, expected_side=Fraction(3, 2))


@pytest.mark.pool_heavy
@pytest.mark.parametrize(
    ("mode", "reason"),
    [
        ("wrong_sequence", "Rust response identity or result count changed"),
        ("duplicate_key", "duplicate Rust response key: version"),
        ("extra_output", "Rust process emitted unsolicited output"),
    ],
)
def test_invalid_resident_response_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mode: str, reason: str
) -> None:
    # Reach the malformed protocol response independently of snapshot/startup time.
    # Real select waits keep their two-second bound; the timeout controls below keep
    # the real clock.
    monkeypatch.setattr(time, "monotonic", lambda: 0.0)
    with pytest.raises(CandidateError, match="Rust exact geometry refused") as refused:
        verify_candidate(
            _candidate(),
            angle_indices=(0,),
            max_nodes_per_angle=1 if mode != "extra_output" else 0,
            max_seconds=2,
            backend="rust",
            rust_binary=_fake_server(tmp_path, mode),
        )
    assert str(refused.value) == f"Rust exact geometry refused: {reason}", refused.getrepr(
        style="long"
    )


@pytest.mark.pool_heavy
def test_partial_line_timeout_retains_unresolved_event_census(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    class ObservedGeometry(RustRectangleGeometry):
        @property
        def process(self) -> subprocess.Popen[bytes] | None:
            return self._process

        @property
        def partial_response(self) -> bytes:
            return bytes(self._buffer)

    start = time.monotonic()
    candidate = _candidate()
    binary = _fake_server(tmp_path, "partial")
    # Validate genuine readiness before the response-phase deadline starts. Startup
    # still counts toward the original two-second outer bound; all clocks, pipes
    # and select waits remain real.
    with ObservedGeometry(candidate.rectangles, binary, deadline=start + 2) as engine:
        process = engine.process
        assert process is not None
        constructor_calls = 0

        def prepared_engine(
            rectangles: tuple[DensityRectangle, ...], binary_path: Path, *, deadline: float
        ) -> RustRectangleGeometry:
            nonlocal constructor_calls
            constructor_calls += 1
            assert constructor_calls == 1
            assert rectangles == candidate.rectangles
            assert binary_path == binary
            assert 0 < deadline - time.monotonic() <= 0.5
            engine.deadline = deadline
            return engine

        monkeypatch.setattr(rectangle_density, "RustRectangleGeometry", prepared_engine)
        report = verify_candidate(
            candidate,
            angle_indices=(0,),
            max_seconds=0.5,
            backend="rust",
            rust_binary=binary,
        )
    assert time.monotonic() - start < 2
    assert report.status == "INCONCLUSIVE"
    assert report.backend_timeout
    assert len(report.angles) == 1
    assert report.angles[0].nodes == 0
    assert report.angles[0].unresolved_leaves > 0
    assert report.angles[0].stop_cause == "time_limit"
    assert constructor_calls == 1
    assert report.rust_binary_sha256 == engine.binary_sha256
    assert report.rust_table_sha256 == engine.table_sha256
    assert engine.partial_response == b'{"version":'
    assert process.poll() is not None
    assert engine.process is None


@pytest.mark.pool_heavy
def test_shutdown_timeout_cannot_promote_completed_angles(tmp_path: Path) -> None:
    report = verify_candidate(
        _candidate(),
        angle_indices=(0,),
        max_seconds=0.5,
        backend="rust",
        rust_binary=_fake_server(tmp_path, "shutdown_hang"),
    )
    assert report.status == "INCONCLUSIVE"
    assert report.backend_timeout
    assert len(report.angles) == 1
    assert report.angles[0].status == "VERIFIED"
    assert report.angles[0].nodes > 0


@pytest.mark.pool_heavy
def test_a_rebuild_during_verification_keeps_the_bytes_that_ran(tmp_path: Path) -> None:
    """The child runs from a private snapshot, so the source path may change mid-run.

    Nothing re-hashes the snapshot or the source (OR-16): the report names the bytes
    that were read once and run, and a rebuild of the source cannot reach them.
    """
    binary = _fake_server(tmp_path, "rebuild")
    ran = hashlib.sha256(binary.read_bytes()).hexdigest()
    report = verify_candidate(
        _candidate(),
        angle_indices=(0,),
        max_seconds=2,
        backend="rust",
        rust_binary=binary,
    )
    assert binary.read_text(encoding="utf-8").endswith("# rebuilt while the verifier ran\n")
    assert report.status == "PARTIAL"
    assert not report.backend_timeout
    assert report.rust_binary_sha256 == ran


def test_unsupported_mixed_bound_is_refused_before_child_start(tmp_path: Path) -> None:
    with pytest.raises(CandidateError, match="common-core only"):
        verify_candidate(
            _candidate(),
            angle_indices=(1,),
            bound_mode="corner-min",
            backend="rust",
            rust_binary=_fake_server(tmp_path, "shutdown_hang"),
        )
