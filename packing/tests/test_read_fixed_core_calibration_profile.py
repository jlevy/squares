"""Focused source-distinct controls for one retained n=2 calibration profile."""

# The tests deliberately exercise the reader's independent private reconstruction seams.
# ruff: noqa: SLF001
# pyright: reportPrivateUsage=false

from __future__ import annotations

import ast
import functools
import hashlib
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
from collections.abc import Iterator, Sequence
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

from devtools import read_fixed_core_calibration_profile as reader

REPOSITORY = Path(__file__).resolve().parents[2]
EXECUTION_REVISION = "faa4085db8fb4cf42154afec0022a0585f59196d"
READER_REVISION = "b" * 40
SOURCE_PATHS = (
    "packing/.python-version",
    reader.FIXTURE_PATH,
    "packing/devtools/__init__.py",
    "packing/devtools/calibrate_fixed_core_packet.py",
    "packing/devtools/decide_certificate.py",
    "packing/devtools/decide_threshold_certificate.py",
    "packing/devtools/dilation_corollary.py",
    "packing/devtools/fixed_core_packet.py",
    "packing/devtools/measure_net_refinement.py",
    "packing/devtools/measure_threshold_net_refinement.py",
    "packing/pyproject.toml",
    "packing/src/sqpack/__init__.py",
    "packing/src/sqpack/field.py",
    "packing/src/sqpack/fractional/__init__.py",
    "packing/src/sqpack/fractional/certificate.py",
    "packing/src/sqpack/fractional/interval.py",
    "packing/src/sqpack/fractional/model.py",
    "packing/src/sqpack/fractional/sweep.py",
    "packing/src/sqpack/fractional/threshold.py",
    "packing/src/sqpack/fractional/threshold_interval.py",
    "packing/src/sqpack/verify.py",
    "packing/src/sqpack/workers.py",
    "packing/uv.lock",
)
CONDITION_NAMES = [
    "Condition 1 atoms carry the declared symmetry",
    "Condition 1' threshold atoms carry the declared symmetry",
    "Condition 2' total budget below n",
    "Condition 3 net reaches pi/4",
    "Condition 4 containment B(1 + D) < 1",
]


def _write(path: Path, value: object, *, indent: int | None = None) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, indent=indent, allow_nan=False) + "\n").encode()
    path.write_bytes(data)
    return data


def _candidate() -> dict[str, object]:
    return {
        "id": reader.NORMALIZED_ID,
        "variant": "threshold",
        "n": 2,
        "claim": "s(2) >= 3/4",
        "outer_side": "3/4",
        "square_side": "1/2",
        "angle_limit": "1/2",
        "direction_steps": reader.STEPS,
        "symmetry": "D4",
        "point_mass": "1/4",
        "threshold_budget": "3/4",
        "total_budget": "1",
        "atoms": [["3/8", "3/8", "1/4"]],
        "threshold_atoms": [
            {
                "points": [["3/16", "3/8"], ["3/8", "3/8"], ["9/16", "3/8"]],
                "threshold": 2,
                "weight": "3/8",
            },
            {
                "points": [["3/8", "3/16"], ["3/8", "3/8"], ["3/8", "9/16"]],
                "threshold": 2,
                "weight": "3/8",
            },
        ],
        "provenance": {
            "kind": "normalized synthetic fixed-core packet calibration fixture",
            "construction": reader.FIXTURE_PROVENANCE["construction"],
            "purpose": reader.FIXTURE_PROVENANCE["purpose"],
            "derived_from": reader.FIXTURE_PATH,
            "source_id": reader.FIXTURE_ID,
            "normalization": "every weight multiplied by 1/2 after raw minimum 2",
        },
        "least_cell_charge": "1",
    }


def _dilation(candidate_sha: str) -> dict[str, object]:
    return {
        "schema": reader.DILATION_SCHEMA,
        "source": {
            "certificate": "candidate.json",
            "sha256": candidate_sha,
            "n": 2,
            "outer_side": "3/4",
            "square_side": "1/2",
            "half_gap_tangent": "1/5760",
            "coarse_containment": "5761/11520",
            "total_budget": "1",
            "minimum_cell_charge": "1",
            "accepted_conditions": [
                *CONDITION_NAMES,
                "Condition 5' every reachable cell is charged at least 1",
            ],
            "variant": "threshold",
            "point_atoms": 1,
            "threshold_atoms": 2,
        },
        "sharpened_containment": {
            "identity": "cos(d) + sin(d) = (1 + t) / sqrt(1 + t^2), where t = tan(d)",
            "gap_domain": "0 <= t <= D = 1/5760 < 1",
            "monotonicity_identity": (
                "(1 + D)^2(1 + t^2) - (1 + t)^2(1 + D^2) = 2(D - t)(1 - Dt) >= 0"
            ),
            "strict_factor_test": "q^2 * 33189121/132710400 < 33177601/33177600",
            "strict_factor_test_left_multiplier": "33189121/132710400",
            "strict_factor_test_right": "33177601/33177600",
            "source_gap_below_one": True,
        },
        "strict_dilation_family": {
            "factor_supremum": "2*sqrt(33177601)/5761",
            "factor_supremum_squared": "132710404/33189121",
            "factor_supremum_decimal": "1.999652868184536",
            "factor_supremum_irrational": True,
            "factor_supremum_defining_polynomial": "33189121*x^2 - 132710404",
            "factor_domain": "q in Q with q > 0 and q^2 < 132710404/33189121",
            "scaled_containment_test": (
                "q^2 B^2 (1 + D)^2 < 1 + D^2; this rational inequality is "
                "equivalent to strict geometric containment"
            ),
            "invariants": [
                (
                    "Conditions 1 and 1' D4 symmetry of the point and threshold atoms "
                    "is equivariant under common scaling"
                ),
                "Conditions 2' and 3 (total budget and direction net) are unchanged",
                (
                    "Condition 5' charge is preserved by inverse dilation of placements: "
                    "a core's trace on each threshold atom's scaled points is unchanged"
                ),
            ],
        },
        "conclusion": {
            "bounded_side": "3*sqrt(33177601)/11522",
            "bounded_side_squared": "298598409/132756484",
            "bounded_side_defining_polynomial": "132756484*x^2 - 298598409",
            "decimal": "1.499739651138402",
            "relation": ">=",
            "endpoint_certificate": False,
        },
        "proof": {
            "strict_family": (
                "for every rational q > 0 with q^2 below factor_supremum_squared, "
                "the sharpened containment theorem and the scaled source data rule out "
                "a packing at side q * outer_side"
            ),
            "density_step": (
                "for every real x below bounded_side, rational density supplies q with "
                "x / outer_side < q < factor_supremum"
            ),
            "embedding_step": (
                "a packing at side x embeds in the larger side q * outer_side, "
                "contradicting that strict-subfactor no-fit proof"
            ),
            "order_step": (
                "equivalently, s(n) is at least every strict rational subbound and "
                "therefore at least their real supremum"
            ),
            "requires_compactness": False,
            "endpoint_status": (
                "the dilation-limit theorem establishes s(2) >= 3*sqrt(33177601)/11522; "
                "at the factor supremum the sharpened containment inequality is equality, "
                "so endpoint_certificate is false because the proof supplies no individual "
                "certificate at that side; the method does not establish s(2) > "
                "3*sqrt(33177601)/11522"
            ),
        },
    }


def _centre_witness(index: int, *, reflected: bool = False) -> tuple[Fraction, Fraction]:
    cosine, sine = reader._rotation(index, reflected=reflected)
    x = y = Fraction(3, 8)
    return cosine * x + sine * y, -sine * x + cosine * y


def _topology(phase: str) -> dict[str, object]:
    return {
        "phase": phase,
        "execution_model": "coordinator-serial",
        "configured_workers": 1,
        "directions_expected": reader.RAW_DIRECTIONS,
        "directions_completed": reader.RAW_DIRECTIONS,
        "child_tasks_observed": 0,
        "observed_child_count": 0,
        "maximum_simultaneous_children": 0,
        "tasks": [],
        "children": [],
    }


def _artifact_rows(output: Path, receipt_size: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for role, relative, _count, directory in reader.ARTIFACTS:
        path = output / relative
        files = tuple(path.iterdir()) if directory else (path,)
        size = (
            receipt_size
            if relative == "result.json"
            else sum(item.stat().st_size for item in files)
        )
        rows.append({"role": role, "path": relative, "count": len(files), "bytes": size})
    return rows


def _publish_receipt(output: Path, receipt: dict[str, object]) -> None:
    size = 0
    for _attempt in range(10):
        receipt["artifacts"] = _artifact_rows(output, size)
        data = (json.dumps(receipt, indent=2, allow_nan=False) + "\n").encode()
        if len(data) == size:
            (output / "result.json").write_bytes(data)
            return
        size = len(data)
    raise AssertionError("result inventory did not reach a fixed point")


def _set_path(root: dict[str, object], path: tuple[str | int, ...], value: object) -> None:
    current: object = root
    for key in path[:-1]:
        if isinstance(current, dict):
            current = cast(dict[str, object], current)[cast(str, key)]
        else:
            current = cast(list[object], current)[cast(int, key)]
    if isinstance(current, dict):
        cast(dict[str, object], current)[cast(str, path[-1])] = value
    else:
        cast(list[object], current)[cast(int, path[-1])] = value


def _execution_blobs(paths: Sequence[str]) -> list[tuple[str, bytes]]:
    """Each path's object id and bytes at the execution revision, from one `git` process.

    One `cat-file --batch` stands in for a `show` and a `rev-parse` per path, which were 46
    processes in every xdist worker's build of the profile.
    """
    request = "".join(f"{EXECUTION_REVISION}:{path}\n" for path in paths).encode()
    stream = subprocess.run(
        ("git", "cat-file", "--batch"),
        cwd=REPOSITORY,
        input=request,
        check=True,
        capture_output=True,
    ).stdout
    blobs: list[tuple[str, bytes]] = []
    offset = 0
    for path in paths:
        header_end = stream.index(b"\n", offset)
        blob, kind, size = stream[offset:header_end].decode().split(" ")
        assert kind == "blob", path
        start = header_end + 1
        blobs.append((blob, stream[start : start + int(size)]))
        offset = start + int(size) + 1
    assert offset == len(stream)
    return blobs


def _build_profile(output: Path) -> dict[str, object]:
    output.mkdir()
    candidate_data = _write(output / "candidate.json", _candidate(), indent=1)
    candidate_sha = hashlib.sha256(candidate_data).hexdigest()
    labels = [str(index) for index in range(reader.RAW_DIRECTIONS)]
    interval_labels = labels + [f"{index}'" for index in range(1, reader.RAW_DIRECTIONS)]
    raw_paths: list[Path] = []
    exact_paths: list[Path] = []
    interval_paths: list[Path] = []
    dilation_paths: list[Path] = []
    for index in range(reader.RAW_DIRECTIONS):
        u, v = _centre_witness(index)
        raw = output / "raw-directions" / f"{index}.json"
        exact = output / "normalized-exact-directions" / f"{index}.json"
        dilation = output / "dilation-directions" / f"{index}.json"
        _write(raw, {"direction": index, "charge": "2", "witness": [str(u), str(v)]})
        _write(
            exact,
            {
                "direction": index,
                "dense": "1",
                "slab": "1",
                "agree": True,
                "witness": [str(u), str(v)],
                "slab_witness": [str(u), str(v)],
            },
        )
        _write(dilation, {"direction": index, "label": str(index), "minimum": "1"})
        raw_paths.append(raw)
        exact_paths.append(exact)
        dilation_paths.append(dilation)
    for label in interval_labels:
        index = int(label.rstrip("'"))
        u, v = _centre_witness(index, reflected=label.endswith("'"))
        path = output / "normalized-interval-directions" / f"{label}.json"
        _write(
            path,
            {
                "label": label,
                "status": "certified",
                "lower": 8,
                "upper": 8,
                "witness": [float(u), float(v)],
                "boxes": 1,
                "stalled": 0,
                "budget_exhausted": False,
            },
        )
        interval_paths.append(path)
    dilation_data = _write(output / "dilation.json", _dilation(candidate_sha), indent=2)
    rss_samples = {
        "schema": "fixed-core-packet-calibration-rss/v1",
        "samples": [
            {
                "elapsed_seconds": 0.1,
                "phase": "preflight",
                "pids": [101],
                "rss_bytes": 1_024,
                "error": None,
            },
            {
                "elapsed_seconds": 0.2,
                "phase": "raw-sweep",
                "pids": [101],
                "rss_bytes": 2_048,
                "error": None,
            },
        ],
    }
    rss_data = _write(output / "rss-samples.json", rss_samples)
    coordinator = {"role": "coordinator", "pid": 101, "ppid": 100, "pgid": 101}
    topology_summaries: dict[str, object] = {}
    for name, phase, filename in (
        ("raw", "raw-sweep", "raw-worker-topology.json"),
        ("normalized_exact", "normalized-exact", "normalized-exact-worker-topology.json"),
    ):
        data = _write(
            output / filename,
            {
                "schema": "fixed-core-packet-calibration-worker-route/v1",
                "scope": reader.TOPOLOGY_SCOPE,
                "coordinator": coordinator,
                "route": _topology(phase),
            },
        )
        topology_summaries[name] = {
            "configured_workers": 1,
            "execution_model": "coordinator-serial",
            "observed_child_count": 0,
            "maximum_simultaneous_children": 0,
            "record_path": filename,
            "record_sha256": hashlib.sha256(data).hexdigest(),
        }
    manifest = [
        {"path": relative, "git_blob": blob, "sha256": hashlib.sha256(frozen).hexdigest()}
        for relative, (blob, frozen) in zip(
            SOURCE_PATHS, _execution_blobs(SOURCE_PATHS), strict=True
        )
    ]
    origin = 10.0
    settings = {
        "requested_workers": 1,
        "effective_workers": {
            "raw": 1,
            "normalized_exact": 1,
            "reflected_interval": 1,
            "dilation": 1,
        },
        "calibration_seconds": 20.0,
        "external_seconds": 30.0,
        "termination_grace_seconds": 2.0,
        "rss_sample_interval_seconds": 0.1,
        "core_side": "1/2",
        "direction_steps": reader.STEPS,
        "angle_limit": "1/2",
        "half_gap_tangent": "1/5760",
        "raw_threshold_M_over_n": "1",
        "expected_direction_rows": reader.TOTAL_DIRECTION_ROWS,
    }
    identity = {
        "implementation_revision": EXECUTION_REVISION,
        "requested_workers": 1,
        "calibration_seconds": 20.0,
        "external_seconds": 30.0,
        "termination_grace_seconds": 2.0,
        "monotonic_origin": origin,
        "calibration_deadline_monotonic": 30.0,
        "external_deadline_monotonic": 40.0,
        "run_order": 1,
        "cache_observation": "test cache observation",
        "background_load": "test background load",
    }
    cpu_observations = {
        "coordinator_start_seconds": 1.0,
        "coordinator_end_seconds": 1.5,
        "direct_children_user_start_seconds": 2.0,
        "direct_children_user_end_seconds": 2.25,
        "direct_children_system_start_seconds": 3.0,
        "direct_children_system_end_seconds": 3.125,
    }
    receipt: dict[str, object] = {
        "schema": reader.RECEIPT_SCHEMA,
        "status": "complete",
        "disposition": "calibration-passed",
        "evidence_scope": reader.CALIBRATION_SCOPE,
        "fixture": {
            "id": reader.FIXTURE_ID,
            "source_path": reader.FIXTURE_PATH,
            "source_sha256": reader.FIXTURE_SHA256,
            "source_bytes": reader.FIXTURE_BYTES,
            "provenance": reader.FIXTURE_PROVENANCE,
        },
        "sources": {
            "implementation_revision": EXECUTION_REVISION,
            "manifest": manifest,
            "runtime": {
                "python": {
                    "implementation": "cpython",
                    "version": "3.14.7",
                    "abi": "cpython-314t",
                    "gil_enabled": False,
                    "environment": "/profile/.venv",
                    "executable": "/profile/.venv/bin/python",
                    "resolved_executable": "/runtime/python",
                    "build": "test build",
                },
                "packages": {"numpy": "2.3.3", "strif": "3.0.0"},
                "attestation_scope": reader.RUNTIME_SCOPE,
            },
        },
        "invocation": {
            "started_utc": "2026-09-13T00:00:00+00:00",
            "monotonic_origin": origin,
            "host": "test-host",
            "platform": "test-platform",
            "run_order": 1,
            "cache_observation": "test cache observation",
            "background_load": "test background load",
            "identity": identity,
        },
        "settings": settings,
        "clocks": {
            "phase_duration_scope": reader.PHASE_DURATION_SCOPE,
            "preflight_seconds": 0.1,
            "launch_seconds": 0.1,
            "source_loading_seconds": 0.1,
            "raw_seconds": 0.1,
            "normalization_publication_seconds": 0.1,
            "exact_seconds": 0.1,
            "interval_seconds": 0.1,
            "dilation_seconds": 0.1,
            "full_readback_seconds": 0.1,
            "parent_final_readback_seconds": 0.1,
            "terminal_admission_seconds": 0.1,
            "worker_elapsed_seconds": 1.0,
            "worker_exit_seconds": 1.05,
            "supervisor_cleanup_seconds": 0.1,
            "external_lifetime_seconds": 1.2,
        },
        "resources": {
            "cpu_scope": reader.CPU_SCOPE,
            "cpu_observations": cpu_observations,
            "coordinator_process_seconds": 0.5,
            "reaped_direct_children_user_seconds": 0.25,
            "reaped_direct_children_system_seconds": 0.125,
            "rss": {
                "scope": reader.RSS_SCOPE,
                "sample_interval_seconds": 0.1,
                "minimum_terminal_samples": 2,
                "sample_count": 2,
                "positive_sample_count": 2,
                "maximum_actual_gap_seconds": 0.2 - 0.1,
                "observation_lifetime_seconds": 1.2,
                "unobserved_leading_seconds": 0.1,
                "unobserved_trailing_seconds": 1.2 - 0.2,
                "peak_sampled_rss_bytes": 2_048,
                "peak_sample_time_seconds": 0.2,
                "observed_pids": [101],
                "pids_by_phase": {"preflight": [101], "raw-sweep": [101]},
                "observed_phases": ["preflight", "raw-sweep"],
                "unobserved_phases": sorted(
                    set(reader.OBSERVABLE_PHASES) - {"preflight", "raw-sweep"}
                ),
                "observer_errors": [],
                "samples_path": "rss-samples.json",
                "samples_sha256": hashlib.sha256(rss_data).hexdigest(),
            },
            "worker_topology": {
                "schema": "fixed-core-packet-calibration-worker-topology/v1",
                "scope": reader.TOPOLOGY_SCOPE,
                "coordinator": coordinator,
                "routes": topology_summaries,
            },
        },
        "raw": {
            "directions_expected": reader.RAW_DIRECTIONS,
            "directions_completed": reader.RAW_DIRECTIONS,
            "completed_directions": list(range(reader.RAW_DIRECTIONS)),
            "observed_minimum_upper_bound": "2",
            "observed_argmin": 0,
            "observed_witness": json.loads(raw_paths[0].read_bytes())["witness"],
            "raw_minimum": "2",
            "budget": "2",
            "threshold_M_over_n": "1",
            "comparison": "passed",
            "witness_replay_charge": "2",
            "witness_admissible": True,
            "directions_sha256": reader._direction_digest(raw_paths),
        },
        "normalized": {
            "path": "candidate.json",
            "sha256": candidate_sha,
            "source_fixture_sha256": reader.FIXTURE_SHA256,
            "id": reader.NORMALIZED_ID,
            "alpha": "1/2",
            "point_mass": "1/4",
            "threshold_budget": "3/4",
            "total_budget": "1",
            "least_cell_charge": "1",
            "integer_scale": 8,
            "closed_form_conditions": [
                {"name": name, "detail": "independently retained detail", "holds": True}
                for name in CONDITION_NAMES
            ],
        },
        "routes": {
            "normalized_exact": {
                "status": "complete",
                "source_sha256": candidate_sha,
                "directions_expected": reader.RAW_DIRECTIONS,
                "directions_completed": reader.RAW_DIRECTIONS,
                "completed_directions": list(range(reader.RAW_DIRECTIONS)),
                "minimum": "1",
                "argmin": 0,
                "witness": json.loads(exact_paths[0].read_bytes())["witness"],
                "dense_slab_disagreements": 0,
                "directions_sha256": reader._direction_digest(exact_paths),
            },
            "reflected_interval": {
                "status": "complete",
                "source_sha256": candidate_sha,
                "directions_expected": reader.INTERVAL_DIRECTIONS,
                "directions_completed": reader.INTERVAL_DIRECTIONS,
                "completed_directions": interval_labels,
                "integer_scale": 8,
                "integer_enclosure": [8, 8],
                "enclosure": ["1", "1"],
                "stalled": 0,
                "budget_exhausted": 0,
                "accepted": True,
                "boxes_observed": reader.INTERVAL_DIRECTIONS,
                "directions_sha256": reader._direction_digest(interval_paths),
            },
            "dilation": {
                "status": "complete",
                "source_sha256": candidate_sha,
                "directions_expected": reader.RAW_DIRECTIONS,
                "directions_completed": reader.RAW_DIRECTIONS,
                "completed_directions": labels,
                "directions_sha256": reader._direction_digest(dilation_paths),
                "record_sha256": hashlib.sha256(dilation_data).hexdigest(),
                "generic_record_schema": reader.DILATION_SCHEMA,
                "generic_record_scope": (
                    "valid normalized n=2 calibration fixture; no campaign or "
                    "fixed-packet evidence"
                ),
                "factor_supremum": "2*sqrt(33177601)/5761",
                "factor_supremum_squared": "132710404/33189121",
                "bounded_side": "3*sqrt(33177601)/11522",
                "bounded_side_squared": "298598409/132756484",
                "relation": ">=",
                "endpoint_certificate": False,
                "requires_compactness": False,
            },
        },
        "artifacts": [],
        "supervision": {
            "status": "observed-exit",
            "worker_exit_status": 0,
            "process_group_reaped": True,
            "supervisor_signal": None,
            "coordinator_pid": 101,
            "coordinator_process_group_id": 101,
        },
        "phase": "complete",
        "error": None,
    }
    (output / "result.json").touch()
    _publish_receipt(output, receipt)
    return receipt


_OBJECT_ADDRESSED = re.compile(r"[0-9a-f]{40}(?::.+)?")


@pytest.fixture(scope="module", autouse=True)
def _share_pure_reader_lookups() -> Iterator[None]:
    """Memoize the reader's two pure lookups across this module's reads, and nothing else.

    A full read spawns about seventy `git` processes, all but one naming an object by id,
    and replays 14,404 membership charges that every mutated copy shares with the baseline.
    Sixteen quick tests make such a read, at 3.4-5.8s each on CI. Both lookups are
    functions of immutable inputs, so sharing them changes no outcome: a refusal raises
    before anything is stored, a query naming `HEAD` is never stored, and each worker's
    first read runs every lookup for real, so a defect in either is what gets shared.
    Deliberately defective charges and a disabled reader-bytes binding both still fail
    this module with the memo in place.

    What is not shared is every read of the profile's files, since the tests rewrite them.
    """
    git = reader._git

    @functools.cache
    def pinned(repository: Path, arguments: tuple[str, ...], *, binary: bool) -> bytes | str:
        return git(repository, *arguments, binary=binary)

    def shared(repository: Path, *arguments: str, binary: bool = False) -> bytes | str:
        if _OBJECT_ADDRESSED.fullmatch(arguments[-1]):
            return pinned(repository, arguments, binary=binary)
        return git(repository, *arguments, binary=binary)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(reader, "_git", shared)
        patch.setattr(reader, "_charge", functools.cache(reader._charge))
        yield


@pytest.fixture(scope="module")
def profile(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, dict[str, object]]:
    output = tmp_path_factory.mktemp("source-distinct-profile") / "profile-1"
    return output, _build_profile(output)


def _read(
    monkeypatch: pytest.MonkeyPatch,
    output: Path,
    *,
    execution_revision: str = EXECUTION_REVISION,
    reader_revision: str = READER_REVISION,
) -> dict[str, object]:
    monkeypatch.setattr(reader, "_bind_revisions", lambda *_args: None)
    return reader.read_profile(
        repository=REPOSITORY,
        execution_revision=execution_revision,
        reader_revision=reader_revision,
        output_dir=output,
        run_order=1,
    )


def test_full_profile_reconstructs_every_row_digest_resource_and_sidecar(
    monkeypatch: pytest.MonkeyPatch, profile: tuple[Path, dict[str, object]]
) -> None:
    output, _receipt = profile
    proof = _read(monkeypatch, output)

    assert proof["status"] == "accepted"
    assert proof["execution_revision"] == EXECUTION_REVISION
    assert proof["reader_revision"] == READER_REVISION
    assert proof["interval_boxes_observed"] == reader.INTERVAL_DIRECTIONS
    assert len(cast(list[object], proof["artifacts"])) == 10
    assert cast(dict[str, object], proof["worker_topology"])["raw"] == {
        "configured_workers": 1,
        "execution_model": "coordinator-serial",
        "observed_child_count": 0,
        "maximum_simultaneous_children": 0,
    }


def test_reader_import_closure_is_source_distinct() -> None:
    path = REPOSITORY / "packing/devtools/read_fixed_core_calibration_profile.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    local_imports = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    } | {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    assert not any(name.startswith(("devtools", "sqpack", "cases")) for name in local_imports)


def test_strict_json_duplicate_and_scientific_schema_controls(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    profile: tuple[Path, dict[str, object]],
) -> None:
    with pytest.raises(reader.ReadbackRefusalError, match="duplicate JSON"):
        reader._json_bytes(b'{"schema": 1, "schema": 2}', "control")

    output, receipt = profile
    mutated = deepcopy(receipt)
    mutated["scientific_decision"] = "accepted"
    path = tmp_path / "result.json"
    _write(path, mutated)
    with pytest.raises(reader.ReadbackRefusalError, match="fields or schema"):
        reader._validate_receipt_schema(mutated, 1)
    mutated.pop("scientific_decision")
    cast(dict[str, object], mutated["fixture"])["id"] = "BC329"
    with pytest.raises(reader.ReadbackRefusalError, match="scientific-target vocabulary"):
        reader._validate_receipt_schema(mutated, 1)
    malformed_sources = deepcopy(receipt)
    malformed_sources["sources"] = []
    with pytest.raises(reader.ReadbackRefusalError, match="sources fields"):
        reader._validate_receipt_schema(malformed_sources, 1)
    monkeypatch.setattr(reader, "_bind_revisions", lambda *_args: None)
    _publish_receipt(output, malformed_sources)
    try:
        with pytest.raises(reader.ReadbackRefusalError, match="sources fields"):
            _read(monkeypatch, output)
    finally:
        _publish_receipt(output, deepcopy(receipt))


def test_deadline_and_rss_lifetime_relations_are_independently_bound(
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile

    worker_deadline = deepcopy(baseline)
    cast(dict[str, object], worker_deadline["clocks"])["worker_elapsed_seconds"] = 20.0
    with pytest.raises(reader.ReadbackRefusalError, match="declared deadline"):
        reader._validate_receipt_schema(worker_deadline, 1)

    external_deadline = deepcopy(baseline)
    clocks = cast(dict[str, object], external_deadline["clocks"])
    clocks["external_lifetime_seconds"] = 29.9
    clocks["terminal_admission_seconds"] = 0.1
    rss = cast(
        dict[str, object], cast(dict[str, object], external_deadline["resources"])["rss"]
    )
    rss["observation_lifetime_seconds"] = 29.9
    rss["unobserved_trailing_seconds"] = 29.7
    with pytest.raises(reader.ReadbackRefusalError, match="declared deadline"):
        reader._validate_receipt_schema(external_deadline, 1)

    lifetime_split = deepcopy(baseline)
    rss = cast(dict[str, object], cast(dict[str, object], lifetime_split["resources"])["rss"])
    rss["observation_lifetime_seconds"] = 1.3
    rss["unobserved_trailing_seconds"] = 1.1
    with pytest.raises(reader.ReadbackRefusalError, match="RSS observation lifetime"):
        reader._validate_receipt_schema(lifetime_split, 1)

    malformed_coordinator = deepcopy(baseline)
    topology = cast(
        dict[str, object],
        cast(dict[str, object], malformed_coordinator["resources"])["worker_topology"],
    )
    cast(dict[str, object], topology["coordinator"])["ppid"] = 0
    with pytest.raises(reader.ReadbackRefusalError, match="topology coordinator"):
        reader._validate_topology(output, malformed_coordinator)


def test_filesystem_preflight_refuses_links_and_special_files(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, _receipt = profile

    output_link = tmp_path / "profile-link"
    output_link.symlink_to(output, target_is_directory=True)
    with pytest.raises(reader.ReadbackRefusalError, match="must not be a symlink"):
        _read(monkeypatch, output_link)

    candidate = output / "candidate.json"
    candidate_bytes = candidate.read_bytes()
    linked_bytes = tmp_path / "linked-candidate.json"
    linked_bytes.write_bytes(candidate_bytes)
    candidate.unlink()
    candidate.symlink_to(linked_bytes)
    try:
        with pytest.raises(reader.ReadbackRefusalError, match=r"wrong type: candidate\.json"):
            _read(monkeypatch, output)
    finally:
        candidate.unlink()
        candidate.write_bytes(candidate_bytes)

    candidate.unlink()
    os.mkfifo(candidate)
    try:
        with pytest.raises(reader.ReadbackRefusalError, match=r"wrong type: candidate\.json"):
            _read(monkeypatch, output)
    finally:
        candidate.unlink()
        candidate.write_bytes(candidate_bytes)


@pytest.mark.slow
def test_coherent_mathematical_and_operational_mutations_are_refused(
    monkeypatch: pytest.MonkeyPatch, profile: tuple[Path, dict[str, object]]
) -> None:
    output, baseline = profile
    result_path = output / "result.json"

    def restore_receipt() -> dict[str, object]:
        receipt = deepcopy(baseline)
        _publish_receipt(output, receipt)
        return receipt

    # A retained witness and its digest are changed together; membership still catches it.
    receipt = restore_receipt()
    raw_path = output / "raw-directions/1.json"
    original_raw = raw_path.read_bytes()
    _write(raw_path, {"direction": 1, "charge": "2", "witness": ["0", "0"]})
    raw_paths = [
        output / "raw-directions" / f"{index}.json" for index in range(reader.RAW_DIRECTIONS)
    ]
    cast(dict[str, object], receipt["raw"])["directions_sha256"] = reader._direction_digest(
        raw_paths
    )
    _publish_receipt(output, receipt)
    with pytest.raises(reader.ReadbackRefusalError, match=r"raw row|raw witness"):
        _read(monkeypatch, output)
    raw_path.write_bytes(original_raw)

    # The exact route's two methods and its digest agree on a forged witness.
    receipt = restore_receipt()
    exact_path = output / "normalized-exact-directions/1.json"
    original_exact = exact_path.read_bytes()
    _write(
        exact_path,
        {
            "direction": 1,
            "dense": "1",
            "slab": "1",
            "agree": True,
            "witness": ["0", "0"],
            "slab_witness": ["0", "0"],
        },
    )
    exact_paths = [
        output / "normalized-exact-directions" / f"{index}.json"
        for index in range(reader.RAW_DIRECTIONS)
    ]
    cast(dict[str, object], cast(dict[str, object], receipt["routes"])["normalized_exact"])[
        "directions_sha256"
    ] = reader._direction_digest(exact_paths)
    _publish_receipt(output, receipt)
    with pytest.raises(reader.ReadbackRefusalError, match="exact row"):
        _read(monkeypatch, output)
    exact_path.write_bytes(original_exact)

    # The interval route's retained float witness and route digest move together.
    receipt = restore_receipt()
    interval_path = output / "normalized-interval-directions/0.json"
    original_interval = interval_path.read_bytes()
    interval_row = json.loads(original_interval)
    interval_row["witness"] = [0.0, 0.0]
    _write(interval_path, interval_row)
    interval_labels = [str(index) for index in range(reader.RAW_DIRECTIONS)] + [
        f"{index}'" for index in range(1, reader.RAW_DIRECTIONS)
    ]
    interval_paths = [
        output / "normalized-interval-directions" / f"{label}.json" for label in interval_labels
    ]
    cast(dict[str, object], cast(dict[str, object], receipt["routes"])["reflected_interval"])[
        "directions_sha256"
    ] = reader._direction_digest(interval_paths)
    _publish_receipt(output, receipt)
    with pytest.raises(reader.ReadbackRefusalError, match="interval row"):
        _read(monkeypatch, output)
    interval_path.write_bytes(original_interval)

    # Candidate geometry, all candidate digests, and the dilation source binding move together.
    receipt = restore_receipt()
    candidate_path = output / "candidate.json"
    original_candidate = candidate_path.read_bytes()
    candidate = json.loads(original_candidate)
    candidate["square_side"] = "3/5"
    candidate_data = _write(candidate_path, candidate, indent=1)
    candidate_sha = hashlib.sha256(candidate_data).hexdigest()
    cast(dict[str, object], receipt["normalized"])["sha256"] = candidate_sha
    for route in cast(dict[str, object], receipt["routes"]).values():
        cast(dict[str, object], route)["source_sha256"] = candidate_sha
    dilation_path = output / "dilation.json"
    original_dilation = dilation_path.read_bytes()
    dilation = json.loads(original_dilation)
    cast(dict[str, object], dilation["source"])["sha256"] = candidate_sha
    dilation_data = _write(dilation_path, dilation, indent=2)
    cast(dict[str, object], cast(dict[str, object], receipt["routes"])["dilation"])[
        "record_sha256"
    ] = hashlib.sha256(dilation_data).hexdigest()
    _publish_receipt(output, receipt)
    with pytest.raises(reader.ReadbackRefusalError, match="candidate geometry"):
        _read(monkeypatch, output)
    candidate_path.write_bytes(original_candidate)
    dilation_path.write_bytes(original_dilation)

    # A coherent normalization rewrite is still outside the sole frozen derivation.
    receipt = restore_receipt()
    candidate = json.loads(original_candidate)
    cast(list[list[str]], candidate["atoms"])[0][2] = "1/8"
    candidate["point_mass"] = "1/8"
    candidate["total_budget"] = "7/8"
    candidate_data = _write(candidate_path, candidate, indent=1)
    normalized = cast(dict[str, object], receipt["normalized"])
    normalized.update(
        {
            "sha256": hashlib.sha256(candidate_data).hexdigest(),
            "point_mass": "1/8",
            "total_budget": "7/8",
        }
    )
    _publish_receipt(output, receipt)
    with pytest.raises(reader.ReadbackRefusalError, match=r"candidate geometry|normalization"):
        _read(monkeypatch, output)
    candidate_path.write_bytes(original_candidate)

    # Dilation record and receipt agree on the forged value; independent algebra refuses it.
    receipt = restore_receipt()
    dilation = json.loads(original_dilation)
    cast(dict[str, object], dilation["strict_dilation_family"])["factor_supremum_squared"] = "4"
    dilation_data = _write(dilation_path, dilation, indent=2)
    dilation_receipt = cast(
        dict[str, object], cast(dict[str, object], receipt["routes"])["dilation"]
    )
    dilation_receipt["factor_supremum_squared"] = "4"
    dilation_receipt["record_sha256"] = hashlib.sha256(dilation_data).hexdigest()
    _publish_receipt(output, receipt)
    with pytest.raises(reader.ReadbackRefusalError, match=r"dilation receipt|dilation surd"):
        _read(monkeypatch, output)
    dilation_path.write_bytes(original_dilation)

    # RSS bytes and digest change without the corresponding derived peak.
    receipt = restore_receipt()
    rss_path = output / "rss-samples.json"
    original_rss = rss_path.read_bytes()
    rss = json.loads(original_rss)
    cast(list[dict[str, object]], rss["samples"])[1]["rss_bytes"] = 4_096
    rss_data = _write(rss_path, rss)
    cast(dict[str, object], cast(dict[str, object], receipt["resources"])["rss"])[
        "samples_sha256"
    ] = hashlib.sha256(rss_data).hexdigest()
    _publish_receipt(output, receipt)
    with pytest.raises(reader.ReadbackRefusalError, match="RSS summary"):
        _read(monkeypatch, output)
    rss_path.write_bytes(original_rss)

    # A sidecar and summary digest move together, but the route execution claim is false.
    receipt = restore_receipt()
    topology_path = output / "raw-worker-topology.json"
    original_topology = topology_path.read_bytes()
    topology = json.loads(original_topology)
    cast(dict[str, object], topology["route"])["execution_model"] = "process-pool"
    topology_data = _write(topology_path, topology)
    topology_summary = cast(
        dict[str, object],
        cast(
            dict[str, object], cast(dict[str, object], receipt["resources"])["worker_topology"]
        )["routes"],
    )
    cast(dict[str, object], topology_summary["raw"])["record_sha256"] = hashlib.sha256(
        topology_data
    ).hexdigest()
    _publish_receipt(output, receipt)
    with pytest.raises(reader.ReadbackRefusalError, match="serial raw-sweep topology"):
        _read(monkeypatch, output)
    topology_path.write_bytes(original_topology)
    restore_receipt()
    assert result_path.exists()


def test_source_and_reader_revisions_are_separate_exact_bindings(
    monkeypatch: pytest.MonkeyPatch, profile: tuple[Path, dict[str, object]]
) -> None:
    output, _receipt = profile
    with pytest.raises(reader.ReadbackRefusalError, match="execution revision"):
        _read(monkeypatch, output, execution_revision="c" * 40)

    monkeypatch.undo()
    head = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    with pytest.raises(
        reader.ReadbackRefusalError, match=r"expected reader revision|current checkout"
    ):
        reader._bind_revisions(REPOSITORY, EXECUTION_REVISION, "0" * 40)
    if (REPOSITORY / "packing/devtools/read_fixed_core_calibration_profile.py").exists():
        assert head != READER_REVISION


def test_cli_emits_no_json_proof_on_refusal(capsys: pytest.CaptureFixture[str]) -> None:
    status = reader.main(
        [
            "--repository",
            str(REPOSITORY),
            "--expect-execution-revision",
            EXECUTION_REVISION,
            "--expect-reader-revision",
            "invalid",
            "--output-dir",
            str(REPOSITORY),
            "--run-order",
            "1",
        ]
    )
    captured = capsys.readouterr()
    assert status != 0
    assert captured.out == ""
    assert captured.err.startswith("REFUSED:")


@pytest.mark.slow
def test_execution_manifest_closure_and_every_missing_path(
    profile: tuple[Path, dict[str, object]],
) -> None:
    _output, receipt = profile
    assert reader._execution_source_paths(REPOSITORY, EXECUTION_REVISION) == SOURCE_PATHS
    sources = cast(dict[str, object], receipt["sources"])
    reader._validate_sources(REPOSITORY, sources, EXECUTION_REVISION)
    for missing in SOURCE_PATHS:
        altered = deepcopy(sources)
        manifest = cast(list[dict[str, object]], altered["manifest"])
        altered["manifest"] = [row for row in manifest if row["path"] != missing]
        with pytest.raises(
            reader.ReadbackRefusalError, match="complete execution import closure"
        ):
            reader._validate_sources(REPOSITORY, altered, EXECUTION_REVISION)

    for change in ("unexpected", "duplicate", "alias", "blob", "sha256"):
        altered = deepcopy(sources)
        manifest = cast(list[dict[str, object]], altered["manifest"])
        if change == "unexpected":
            manifest.append(
                {"path": "packing/README.md", "git_blob": "0" * 40, "sha256": "0" * 64}
            )
        elif change == "duplicate":
            manifest.append(deepcopy(manifest[0]))
        elif change == "alias":
            manifest[0]["path"] = "packing//.python-version"
        else:
            manifest[0]["git_blob" if change == "blob" else "sha256"] = "0" * (
                40 if change == "blob" else 64
            )
        with pytest.raises(reader.ReadbackRefusalError):
            reader._validate_sources(REPOSITORY, altered, EXECUTION_REVISION)
    with pytest.raises(reader.ReadbackRefusalError, match="execution revision"):
        reader._validate_sources(REPOSITORY, sources, "c" * 40)
    other_revision = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=REPOSITORY, check=True, capture_output=True, text=True
    ).stdout.strip()
    altered = deepcopy(sources)
    altered["implementation_revision"] = other_revision
    with pytest.raises(reader.ReadbackRefusalError):
        reader._validate_sources(REPOSITORY, altered, other_revision)


def test_running_reader_origin_and_cli_copy_refusal(
    tmp_path: Path, profile: tuple[Path, dict[str, object]]
) -> None:
    output, _receipt = profile
    head = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=REPOSITORY, check=True, capture_output=True, text=True
    ).stdout.strip()
    reader_path = REPOSITORY / "packing/devtools/read_fixed_core_calibration_profile.py"
    for name, content in (
        ("outside", reader_path.read_bytes()),
        ("altered", reader_path.read_bytes() + b"\n# changed running source\n"),
    ):
        copied = tmp_path / f"{name}.py"
        copied.write_bytes(content)
        spec = importlib.util.spec_from_file_location(f"reader_copy_{name}", copied)
        assert spec is not None
        assert spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        with pytest.raises(ValueError, match="running reader"):
            module._bind_revisions(REPOSITORY, EXECUTION_REVISION, head)
        command = (
            sys.executable,
            str(copied),
            "--repository",
            str(REPOSITORY),
            "--expect-execution-revision",
            EXECUTION_REVISION,
            "--expect-reader-revision",
            head,
            "--output-dir",
            str(output),
            "--run-order",
            "1",
        )
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        assert result.returncode == 2
        assert result.stdout == ""
        assert result.stderr.startswith("REFUSED: running reader")
    other_checkout = tmp_path / "other-checkout" / "packing/devtools"
    other_checkout.mkdir(parents=True)
    copied = other_checkout / reader_path.name
    copied.write_bytes(reader_path.read_bytes())
    result = subprocess.run(
        (
            sys.executable,
            str(copied),
            "--repository",
            str(REPOSITORY),
            "--expect-execution-revision",
            EXECUTION_REVISION,
            "--expect-reader-revision",
            head,
            "--output-dir",
            str(output),
            "--run-order",
            "1",
        ),
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.startswith("REFUSED: running reader")
    # This positive binding is exercised after the repaired reader is committed.
    reader._bind_revisions(REPOSITORY, EXECUTION_REVISION, head)
    current = reader_path.read_bytes()
    reader_path.write_bytes(current + b"\n# altered on-disk reader\n")
    try:
        with pytest.raises(reader.ReadbackRefusalError, match="reader bytes"):
            reader._bind_revisions(REPOSITORY, EXECUTION_REVISION, head)
    finally:
        reader_path.write_bytes(current)
    result = subprocess.run(
        (
            sys.executable,
            str(reader_path),
            "--repository",
            str(REPOSITORY),
            "--expect-execution-revision",
            EXECUTION_REVISION,
            "--expect-reader-revision",
            head,
            "--output-dir",
            str(output),
            "--run-order",
            "1",
        ),
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert json.loads(result.stdout)["status"] == "accepted"


@pytest.mark.slow
def test_exact_method_witness_agreement_and_closed_boundary(
    monkeypatch: pytest.MonkeyPatch, profile: tuple[Path, dict[str, object]]
) -> None:
    output, baseline = profile
    path = output / "normalized-exact-directions/0.json"
    original = path.read_bytes()
    for slab, slab_charge, agree, valid in (
        (["9/32", "9/32"], "1", True, False),
        (["3/8", "3/8"], "1", False, False),
        (["3/8", "3/8"], "1/2", True, False),
        (["6/16", "3/8"], "1", True, False),
        (["0", "0"], "1", True, False),
        (["1/4", "1/4"], "1", True, True),
    ):
        receipt = deepcopy(baseline)
        row = json.loads(original)
        row["slab_witness"] = slab
        row["slab"] = slab_charge
        row["agree"] = agree
        if valid:
            row["witness"] = slab
            cast(
                dict[str, object],
                cast(dict[str, object], receipt["routes"])["normalized_exact"],
            )["witness"] = slab
        _write(path, row)
        exact_paths = [
            output / "normalized-exact-directions" / f"{index}.json"
            for index in range(reader.RAW_DIRECTIONS)
        ]
        cast(dict[str, object], cast(dict[str, object], receipt["routes"])["normalized_exact"])[
            "directions_sha256"
        ] = reader._direction_digest(exact_paths)
        _publish_receipt(output, receipt)
        try:
            if valid:
                assert _read(monkeypatch, output)["status"] == "accepted"
            else:
                with pytest.raises(reader.ReadbackRefusalError):
                    _read(monkeypatch, output)
        finally:
            path.write_bytes(original)
            _publish_receipt(output, deepcopy(baseline))


def test_json_number_failures_follow_cli_refusal_contract(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    profile: tuple[Path, dict[str, object]],
) -> None:
    with pytest.raises(reader.ReadbackRefusalError, match="finite nonnegative"):
        reader._number(10**1000, "clock")
    with pytest.raises(reader.ReadbackRefusalError, match="strict JSON"):
        reader._json_bytes(b'{"value":' + b"1" * 5000 + b"}", "control")
    output, baseline = profile
    path = output / "result.json"
    monkeypatch.setattr(reader, "_bind_revisions", lambda *_args: None)
    overflow_receipt = deepcopy(baseline)
    cast(dict[str, object], overflow_receipt["clocks"])["raw_seconds"] = 10**1000
    _publish_receipt(output, overflow_receipt)
    overflow_bytes = path.read_bytes()
    try:
        for malformed in (b'{"value":' + b"1" * 5000 + b"}", overflow_bytes):
            path.write_bytes(malformed)
            status = reader.main(
                [
                    "--repository",
                    str(REPOSITORY),
                    "--expect-execution-revision",
                    EXECUTION_REVISION,
                    "--expect-reader-revision",
                    READER_REVISION,
                    "--output-dir",
                    str(output),
                    "--run-order",
                    "1",
                ]
            )
            captured = capsys.readouterr()
            assert status == 2
            assert captured.out == ""
            assert captured.err.startswith("REFUSED:")
    finally:
        _publish_receipt(output, deepcopy(baseline))


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (("fixture", "source_bytes"), 935.0),
        (("invocation", "run_order"), True),
        (("invocation", "run_order"), 1.0),
        (("invocation", "run_order"), "1"),
        (("invocation", "run_order"), None),
        (("invocation", "monotonic_origin"), True),
        (("invocation", "identity", "run_order"), True),
        (("invocation", "identity", "requested_workers"), 1.0),
        (("invocation", "identity", "calibration_deadline_monotonic"), True),
        (("settings", "requested_workers"), True),
        (("settings", "effective_workers", "raw"), True),
        (("settings", "effective_workers", "normalized_exact"), 1.0),
        (("settings", "effective_workers", "reflected_interval"), False),
        (("settings", "effective_workers", "dilation"), None),
        (("settings", "direction_steps"), 2880.0),
        (("settings", "expected_direction_rows"), 14404.0),
        (("settings", "calibration_seconds"), True),
        (("clocks", "raw_seconds"), True),
        (("supervision", "worker_exit_status"), False),
        (("supervision", "coordinator_pid"), 101.0),
    ],
)
def test_receipt_scalar_substitutions_refuse(
    path: tuple[str | int, ...],
    replacement: object,
    profile: tuple[Path, dict[str, object]],
) -> None:
    _output, baseline = profile
    changed = deepcopy(baseline)
    _set_path(changed, path, replacement)
    with pytest.raises(reader.ReadbackRefusalError):
        reader._validate_receipt_schema(changed, 1)


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (("n",), 2.0),
        (("direction_steps",), 2880.0),
        (("threshold_atoms", 0, "threshold"), 2.0),
        (("threshold_atoms", 1, "threshold"), True),
    ],
)
def test_candidate_integer_substitutions_refuse_before_budget_arithmetic(
    path: tuple[str | int, ...],
    replacement: object,
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile
    candidate_path = output / "candidate.json"
    original = candidate_path.read_bytes()
    candidate = json.loads(original)
    _set_path(candidate, path, replacement)
    data = _write(candidate_path, candidate, indent=1)
    receipt = deepcopy(baseline)
    cast(dict[str, object], receipt["normalized"])["sha256"] = hashlib.sha256(data).hexdigest()
    try:
        with pytest.raises(reader.ReadbackRefusalError, match="candidate geometry"):
            reader._validate_candidate(output, receipt)
    finally:
        candidate_path.write_bytes(original)


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (("raw", "observed_argmin"), False),
        (("raw", "completed_directions", 0), False),
        (("raw", "witness_admissible"), 1),
        (("routes", "normalized_exact", "argmin"), False),
        (("routes", "normalized_exact", "dense_slab_disagreements"), 0.0),
        (("routes", "reflected_interval", "integer_scale"), 8.0),
        (("routes", "reflected_interval", "integer_enclosure", 0), 8.0),
        (("routes", "reflected_interval", "stalled"), False),
        (("routes", "reflected_interval", "budget_exhausted"), 0.0),
        (("routes", "reflected_interval", "boxes_observed"), 5761.0),
        (("routes", "dilation", "directions_completed"), 2881.0),
    ],
)
@pytest.mark.slow
def test_route_scalar_substitutions_refuse(
    monkeypatch: pytest.MonkeyPatch,
    path: tuple[str | int, ...],
    replacement: object,
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile
    changed = deepcopy(baseline)
    _set_path(changed, path, replacement)
    _publish_receipt(output, changed)
    try:
        with pytest.raises(reader.ReadbackRefusalError):
            _read(monkeypatch, output)
    finally:
        _publish_receipt(output, deepcopy(baseline))


@pytest.mark.parametrize(
    ("relative", "path", "replacement"),
    [
        ("raw-directions/0.json", ("direction",), False),
        ("normalized-exact-directions/0.json", ("direction",), 0.0),
        ("normalized-interval-directions/0.json", ("lower",), 8.0),
        ("normalized-interval-directions/0.json", ("upper",), True),
        ("normalized-interval-directions/0.json", ("stalled",), False),
        ("dilation-directions/0.json", ("direction",), False),
    ],
)
def test_row_scalar_substitutions_refuse_with_rebound_digests(
    monkeypatch: pytest.MonkeyPatch,
    relative: str,
    path: tuple[str | int, ...],
    replacement: object,
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile
    artifact = output / relative
    original = artifact.read_bytes()
    row = json.loads(original)
    _set_path(row, path, replacement)
    _write(artifact, row)
    receipt = deepcopy(baseline)
    directory = artifact.parent.name
    route = {
        "raw-directions": cast(dict[str, object], receipt["raw"]),
        "normalized-exact-directions": cast(
            dict[str, object], cast(dict[str, object], receipt["routes"])["normalized_exact"]
        ),
        "normalized-interval-directions": cast(
            dict[str, object], cast(dict[str, object], receipt["routes"])["reflected_interval"]
        ),
        "dilation-directions": cast(
            dict[str, object], cast(dict[str, object], receipt["routes"])["dilation"]
        ),
    }[directory]
    labels = [str(index) for index in range(reader.RAW_DIRECTIONS)]
    if directory == "normalized-interval-directions":
        labels += [f"{index}'" for index in range(1, reader.RAW_DIRECTIONS)]
    route["directions_sha256"] = reader._direction_digest(
        [output / directory / f"{label}.json" for label in labels]
    )
    _publish_receipt(output, receipt)
    try:
        with pytest.raises(reader.ReadbackRefusalError):
            _read(monkeypatch, output)
    finally:
        artifact.write_bytes(original)
        _publish_receipt(output, deepcopy(baseline))


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (("source", "n"), 2.0),
        (("sharpened_containment", "identity"), "wrong identity"),
        (("sharpened_containment", "gap_domain"), "0 <= t"),
        (("sharpened_containment", "strict_factor_test"), "q < 9"),
        (("sharpened_containment", "source_gap_below_one"), 1),
        (("strict_dilation_family", "factor_supremum"), "-2*sqrt(33177601)/5761"),
        (("strict_dilation_family", "factor_supremum_squared"), "4"),
        (("strict_dilation_family", "factor_supremum_decimal"), "999"),
        (
            ("strict_dilation_family", "factor_supremum_defining_polynomial"),
            "33189120*x^2 - 132710404",
        ),
        (("strict_dilation_family", "factor_domain"), "q > 0"),
        (("strict_dilation_family", "invariants", 0), False),
        (("conclusion", "bounded_side"), "-3*sqrt(33177601)/11522"),
        (("conclusion", "bounded_side_squared"), "3"),
        (("conclusion", "bounded_side_defining_polynomial"), "132756484*x^2 - 298598408"),
        (("conclusion", "decimal"), "999"),
        (("conclusion", "relation"), ">"),
        (("conclusion", "endpoint_certificate"), 0),
        (("proof", "requires_compactness"), 0),
        (("proof", "endpoint_status"), "endpoint proved"),
    ],
)
@pytest.mark.slow
def test_dilation_contradictions_refuse_with_rebound_record(
    monkeypatch: pytest.MonkeyPatch,
    path: tuple[str | int, ...],
    replacement: object,
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile
    artifact = output / "dilation.json"
    original = artifact.read_bytes()
    record = json.loads(original)
    _set_path(record, path, replacement)
    data = _write(artifact, record, indent=2)
    receipt = deepcopy(baseline)
    cast(dict[str, object], cast(dict[str, object], receipt["routes"])["dilation"])[
        "record_sha256"
    ] = hashlib.sha256(data).hexdigest()
    _publish_receipt(output, receipt)
    try:
        with pytest.raises(reader.ReadbackRefusalError, match="dilation"):
            _read(monkeypatch, output)
    finally:
        artifact.write_bytes(original)
        _publish_receipt(output, deepcopy(baseline))


def _pooled_receipt(
    output: Path, baseline: dict[str, object], *, children_count: int, mode: str = "normal"
) -> dict[str, object]:
    receipt = deepcopy(baseline)
    settings = cast(dict[str, object], receipt["settings"])
    settings["requested_workers"] = 2
    cast(dict[str, object], settings["effective_workers"]).update(
        {"raw": 2, "normalized_exact": 2}
    )
    cast(dict[str, object], cast(dict[str, object], receipt["invocation"])["identity"])[
        "requested_workers"
    ] = 2
    clocks = cast(dict[str, object], receipt["clocks"])
    clocks.update(
        {
            "raw_seconds": 0.5,
            "exact_seconds": 0.5,
            "worker_elapsed_seconds": 2.0,
            "worker_exit_seconds": 2.1,
            "external_lifetime_seconds": 2.3,
        }
    )
    rss = cast(dict[str, object], cast(dict[str, object], receipt["resources"])["rss"])
    rss["observation_lifetime_seconds"] = 2.3
    rss["unobserved_trailing_seconds"] = 2.3 - 0.2
    summaries = cast(
        dict[str, object],
        cast(
            dict[str, object], cast(dict[str, object], receipt["resources"])["worker_topology"]
        )["routes"],
    )
    for name, phase, filename, default_base in (
        ("raw", "raw-sweep", "raw-worker-topology.json", 0.2),
        ("normalized_exact", "normalized-exact", "normalized-exact-worker-topology.json", 0.8),
    ):
        base = default_base
        if mode == "late":
            base = 1_000_000.0
        elif mode == "reversed" and name == "normalized_exact":
            base = 0.3
        stride = 0.0002 if mode == "long" and name == "raw" else 0.0001
        duration = stride if mode == "touch" else 0.00015 if children_count == 2 else 0.00005
        tasks: list[dict[str, object]] = []
        for index in range(reader.RAW_DIRECTIONS):
            pid = 101 if mode == "self-parent" else 201 + index % children_count
            started = base + index * stride
            tasks.append(
                {
                    "direction": index,
                    "pid": pid,
                    "ppid": 101,
                    "pgid": 101,
                    "started_seconds": started,
                    "finished_seconds": (
                        base + (index + 1) * stride
                        if mode == "touch"
                        else base + index * stride + duration
                    ),
                }
            )
        children = []
        for pid in sorted({cast(int, task["pid"]) for task in tasks}):
            owned = [task for task in tasks if task["pid"] == pid]
            children.append(
                {
                    "role": "route-worker",
                    "phase": phase,
                    "pid": pid,
                    "ppid": 101,
                    "pgid": 101,
                    "tasks_completed": len(owned),
                    "first_task_started_seconds": owned[0]["started_seconds"],
                    "last_task_finished_seconds": owned[-1]["finished_seconds"],
                }
            )
        maximum = 2 if children_count == 2 and duration > stride else 1
        sidecar = {
            "schema": "fixed-core-packet-calibration-worker-route/v1",
            "scope": reader.TOPOLOGY_SCOPE,
            "coordinator": {"role": "coordinator", "pid": 101, "ppid": 100, "pgid": 101},
            "route": {
                "phase": phase,
                "execution_model": "process-pool",
                "configured_workers": 2,
                "directions_expected": reader.RAW_DIRECTIONS,
                "directions_completed": reader.RAW_DIRECTIONS,
                "child_tasks_observed": reader.RAW_DIRECTIONS,
                "observed_child_count": len(children),
                "maximum_simultaneous_children": maximum,
                "tasks": tasks,
                "children": children,
            },
        }
        data = _write(output / filename, sidecar)
        summaries[name] = {
            "configured_workers": 2,
            "execution_model": "process-pool",
            "observed_child_count": len(children),
            "maximum_simultaneous_children": maximum,
            "record_path": filename,
            "record_sha256": hashlib.sha256(data).hexdigest(),
        }
    _publish_receipt(output, receipt)
    return receipt


@pytest.mark.parametrize(
    ("children_count", "mode"), [(2, "normal"), (1, "normal"), (1, "touch")]
)
@pytest.mark.slow
def test_valid_pooled_topologies_include_overlap_one_child_and_touching_boundaries(
    monkeypatch: pytest.MonkeyPatch,
    children_count: int,
    mode: str,
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile
    originals = {
        name: (output / name).read_bytes()
        for name in ("raw-worker-topology.json", "normalized-exact-worker-topology.json")
    }
    try:
        _pooled_receipt(output, baseline, children_count=children_count, mode=mode)
        proof = _read(monkeypatch, output)
        raw = cast(dict[str, object], cast(dict[str, object], proof["worker_topology"])["raw"])
        assert raw["observed_child_count"] == children_count
        assert raw["maximum_simultaneous_children"] == (2 if children_count == 2 else 1)
    finally:
        for name, data in originals.items():
            (output / name).write_bytes(data)
        _publish_receipt(output, deepcopy(baseline))


@pytest.mark.parametrize("mode", ["late", "reversed", "long", "self-parent"])
@pytest.mark.slow
def test_impossible_topologies_refuse_after_sidecars_and_summaries_are_rebound(
    monkeypatch: pytest.MonkeyPatch,
    mode: str,
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile
    originals = {
        name: (output / name).read_bytes()
        for name in ("raw-worker-topology.json", "normalized-exact-worker-topology.json")
    }
    try:
        _pooled_receipt(output, baseline, children_count=1, mode=mode)
        with pytest.raises(reader.ReadbackRefusalError, match=r"task|topology"):
            _read(monkeypatch, output)
    finally:
        for name, data in originals.items():
            (output / name).write_bytes(data)
        _publish_receipt(output, deepcopy(baseline))


@pytest.mark.parametrize(
    ("changes", "expected_status"),
    [
        ({"worker_exit_seconds": 1.0}, True),
        (
            {
                "worker_exit_seconds": 1.2,
                "parent_final_readback_seconds": 0.0,
                "supervisor_cleanup_seconds": 0.0,
            },
            True,
        ),
        ({"parent_final_readback_seconds": 0.15}, True),
        ({"worker_exit_seconds": 0.9}, False),
        ({"worker_exit_seconds": 1.3}, False),
        ({"parent_final_readback_seconds": 0.2}, False),
        ({"raw_seconds": 1.1}, False),
        ({"raw_seconds": 0.6, "exact_seconds": 0.6}, False),
        ({"worker_elapsed_seconds": 20.0}, False),
    ],
)
def test_clock_lifetime_edges(
    changes: dict[str, float],
    expected_status: object,
    profile: tuple[Path, dict[str, object]],
) -> None:
    _output, baseline = profile
    receipt = deepcopy(baseline)
    cast(dict[str, object], receipt["clocks"]).update(changes)
    if expected_status is True:
        reader._validate_receipt_schema(receipt, 1)
    else:
        with pytest.raises(reader.ReadbackRefusalError):
            reader._validate_receipt_schema(receipt, 1)


@pytest.mark.parametrize(
    ("path", "bad"),
    [
        (("resources", "rss", "sample_count"), 2.0),
        (("resources", "rss", "positive_sample_count"), True),
        (("resources", "rss", "minimum_terminal_samples"), False),
        (("resources", "rss", "peak_sampled_rss_bytes"), 2048.0),
        (("resources", "worker_topology", "routes", "raw", "configured_workers"), True),
        (("resources", "worker_topology", "routes", "raw", "observed_child_count"), False),
    ],
)
def test_resource_and_topology_scalar_substitutions_refuse(
    path: tuple[str | int, ...],
    bad: object,
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile
    receipt = deepcopy(baseline)
    _set_path(receipt, path, bad)
    if path[1] == "rss":
        with pytest.raises(reader.ReadbackRefusalError):
            reader._validate_resources(output, receipt)
    else:
        with pytest.raises(reader.ReadbackRefusalError):
            reader._validate_topology(output, receipt)


def test_topology_sidecar_count_substitution_refuses(
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile

    sidecar_path = output / "raw-worker-topology.json"
    original = sidecar_path.read_bytes()
    sidecar = json.loads(original)
    cast(dict[str, object], sidecar["route"])["child_tasks_observed"] = False
    data = _write(sidecar_path, sidecar)
    receipt = deepcopy(baseline)
    resources = cast(dict[str, object], receipt["resources"])
    topology = cast(dict[str, object], resources["worker_topology"])
    routes = cast(dict[str, object], topology["routes"])
    raw_summary = cast(dict[str, object], routes["raw"])
    raw_summary["record_sha256"] = hashlib.sha256(data).hexdigest()
    try:
        with pytest.raises(reader.ReadbackRefusalError, match="topology route"):
            reader._validate_topology(output, receipt)
    finally:
        sidecar_path.write_bytes(original)


def _read_with_real_binder(
    output: Path, *, execution_revision: str = EXECUTION_REVISION
) -> dict[str, object]:
    reader_revision = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return reader.read_profile(
        repository=REPOSITORY,
        execution_revision=execution_revision,
        reader_revision=reader_revision,
        output_dir=output,
        run_order=1,
    )


def test_real_binder_accepts_synthetic_baseline(
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, _baseline = profile
    proof = _read_with_real_binder(output)
    assert proof["status"] == "accepted"
    assert proof["execution_revision"] == EXECUTION_REVISION
    assert proof["reader_revision"] != EXECUTION_REVISION


@pytest.mark.parametrize(
    ("clock", "value", "accepted"),
    [
        ("source_loading_seconds", 0.9, False),
        ("launch_seconds", 1_000_000.0, False),
        ("supervisor_cleanup_seconds", 1_000_000.0, False),
        ("source_loading_seconds", 0.1, True),
        ("launch_seconds", 1.05, True),
        ("supervisor_cleanup_seconds", 0.15, True),
    ],
)
def test_real_binder_nested_and_supervisor_duration_controls(
    clock: str,
    value: float,
    accepted: object,
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile
    changed = deepcopy(baseline)
    cast(dict[str, object], changed["clocks"])[clock] = value
    _publish_receipt(output, changed)
    try:
        if accepted is True:
            assert _read_with_real_binder(output)["status"] == "accepted"
        else:
            with pytest.raises(
                reader.ReadbackRefusalError, match=r"nested preflight|supervisor"
            ):
                _read_with_real_binder(output)
    finally:
        _publish_receipt(output, deepcopy(baseline))


@pytest.mark.parametrize(
    ("control", "route", "shift", "accepted"),
    [
        ("raw-before-preflight", "raw", -0.19, False),
        ("exact-before-preceding-phases", "normalized_exact", -0.3, False),
        ("exact-leaves-no-tail", "normalized_exact", 0.8, False),
        ("raw-at-preflight-boundary", "raw", -0.1, True),
        ("exact-at-preceding-boundary", "normalized_exact", -0.1, True),
        ("exact-at-tail-boundary", "normalized_exact", None, True),
    ],
)
@pytest.mark.slow
def test_real_binder_phase_schedule_controls(
    control: str,
    route: str,
    shift: float | None,
    accepted: object,
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile
    original_sidecars = {
        name: (output / name).read_bytes()
        for name in ("raw-worker-topology.json", "normalized-exact-worker-topology.json")
    }
    try:
        changed = _pooled_receipt(output, baseline, children_count=1)
        filename = (
            "raw-worker-topology.json"
            if route == "raw"
            else "normalized-exact-worker-topology.json"
        )
        path = output / filename
        sidecar = json.loads(path.read_bytes())
        route_record = cast(dict[str, object], sidecar["route"])
        tasks = cast(list[dict[str, object]], route_record["tasks"])
        children = cast(list[dict[str, object]], route_record["children"])
        if shift is None:
            clocks = cast(dict[str, object], changed["clocks"])
            following = sum(
                cast(float, clocks[key])
                for key in ("interval_seconds", "dilation_seconds", "full_readback_seconds")
            )
            shift = (
                cast(float, clocks["worker_elapsed_seconds"])
                - following
                - cast(float, tasks[-1]["finished_seconds"])
            )
        for task in tasks:
            task["started_seconds"] = cast(float, task["started_seconds"]) + shift
            task["finished_seconds"] = cast(float, task["finished_seconds"]) + shift
        for child in children:
            child["first_task_started_seconds"] = (
                cast(float, child["first_task_started_seconds"]) + shift
            )
            child["last_task_finished_seconds"] = (
                cast(float, child["last_task_finished_seconds"]) + shift
            )
        data = _write(path, sidecar)
        resources = cast(dict[str, object], changed["resources"])
        topology = cast(dict[str, object], resources["worker_topology"])
        summaries = cast(dict[str, object], topology["routes"])
        cast(dict[str, object], summaries[route])["record_sha256"] = hashlib.sha256(
            data
        ).hexdigest()
        _publish_receipt(output, changed)
        if accepted is True:
            assert _read_with_real_binder(output)["status"] == "accepted", control
        else:
            with pytest.raises(reader.ReadbackRefusalError, match=r"worker phase|tasks"):
                _read_with_real_binder(output)
    finally:
        for name, data in original_sidecars.items():
            (output / name).write_bytes(data)
        _publish_receipt(output, deepcopy(baseline))


def test_real_binder_refuses_two_process_parent_cycle(
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile
    original_sidecars = {
        name: (output / name).read_bytes()
        for name in ("raw-worker-topology.json", "normalized-exact-worker-topology.json")
    }
    try:
        changed = _pooled_receipt(output, baseline, children_count=1)
        resources = cast(dict[str, object], changed["resources"])
        topology = cast(dict[str, object], resources["worker_topology"])
        cast(dict[str, object], topology["coordinator"])["ppid"] = 201
        summaries = cast(dict[str, object], topology["routes"])
        for route, filename in (
            ("raw", "raw-worker-topology.json"),
            ("normalized_exact", "normalized-exact-worker-topology.json"),
        ):
            path = output / filename
            sidecar = json.loads(path.read_bytes())
            cast(dict[str, object], sidecar["coordinator"])["ppid"] = 201
            data = _write(path, sidecar)
            cast(dict[str, object], summaries[route])["record_sha256"] = hashlib.sha256(
                data
            ).hexdigest()
        _publish_receipt(output, changed)
        with pytest.raises(reader.ReadbackRefusalError, match=r"task|child"):
            _read_with_real_binder(output)
    finally:
        for name, data in original_sidecars.items():
            (output / name).write_bytes(data)
        _publish_receipt(output, deepcopy(baseline))


def test_real_binder_rejects_execution_tree_identity(
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile
    tree = subprocess.run(
        ("git", "rev-parse", f"{EXECUTION_REVISION}^{{tree}}"),
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    kind = subprocess.run(
        ("git", "cat-file", "-t", tree),
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert kind == "tree"
    changed = deepcopy(baseline)
    cast(dict[str, object], changed["sources"])["implementation_revision"] = tree
    invocation = cast(dict[str, object], changed["invocation"])
    cast(dict[str, object], invocation["identity"])["implementation_revision"] = tree
    _publish_receipt(output, changed)
    try:
        with pytest.raises(reader.ReadbackRefusalError, match="not a Git commit"):
            _read_with_real_binder(output, execution_revision=tree)
    finally:
        _publish_receipt(output, deepcopy(baseline))


def _large_finite_clock_profile(
    baseline: dict[str, object], *, phase_seconds: float, worker_elapsed: float
) -> dict[str, object]:
    changed = deepcopy(baseline)
    settings = cast(dict[str, object], changed["settings"])
    settings["calibration_seconds"] = 1.6e308
    settings["external_seconds"] = 1.7e308
    invocation = cast(dict[str, object], changed["invocation"])
    identity = cast(dict[str, object], invocation["identity"])
    identity["calibration_seconds"] = settings["calibration_seconds"]
    identity["external_seconds"] = settings["external_seconds"]
    identity["calibration_deadline_monotonic"] = 1.6e308
    identity["external_deadline_monotonic"] = 1.7e308
    clocks = cast(dict[str, object], changed["clocks"])
    for key in (
        "preflight_seconds",
        "raw_seconds",
        "normalization_publication_seconds",
        "exact_seconds",
        "interval_seconds",
        "dilation_seconds",
        "full_readback_seconds",
    ):
        clocks[key] = phase_seconds
    clocks["worker_elapsed_seconds"] = worker_elapsed
    clocks["worker_exit_seconds"] = worker_elapsed
    clocks["external_lifetime_seconds"] = 1.55e308
    rss = cast(dict[str, object], cast(dict[str, object], changed["resources"])["rss"])
    rss["observation_lifetime_seconds"] = 1.55e308
    rss["unobserved_trailing_seconds"] = 1.55e308 - 0.2
    return changed


@pytest.mark.parametrize(
    ("phase_seconds", "accepted"),
    [(4e307, False), (2e307, True)],
)
def test_real_binder_phase_sum_finiteness_controls(
    phase_seconds: float,
    accepted: object,
    profile: tuple[Path, dict[str, object]],
) -> None:
    output, baseline = profile
    total = sum([phase_seconds] * 7)
    assert math.isfinite(phase_seconds)
    assert math.isfinite(total) is (accepted is True)
    worker_elapsed = total if accepted is True else 1.5e308
    changed = _large_finite_clock_profile(
        baseline, phase_seconds=phase_seconds, worker_elapsed=worker_elapsed
    )
    _publish_receipt(output, changed)
    try:
        if accepted is True:
            assert _read_with_real_binder(output)["status"] == "accepted"
        else:
            with pytest.raises(reader.ReadbackRefusalError, match=r"worker phase"):
                _read_with_real_binder(output)
    finally:
        _publish_receipt(output, deepcopy(baseline))
