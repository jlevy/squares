#!/usr/bin/env python3
"""Produce a Route S T-025 compression receipt for exp-161.

This command authenticates the frozen T-025 source, inventories U025, and replays the
admitted 23-orbit accept / 24-orbit reject policy.  It does not run a coverage verifier
on a decompressed candidate and does not emit a candidate certificate.  ``--authorize-target
exp-161`` is the only flag that may formulate the coverage MIP; ``--encode-coverage``
enumerates the frozen ``A w >= 1`` rows; ``--search`` may run the encoded HiGHS MIP only
after that enumeration.  The default authorized path still emits no candidate, and even
``--search`` leaves ``n_plus`` null.  Closed-core coverage is linear in the frozen U025
orbit weights.  A coverage-free MIP is never solved and never reported as N+.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import json
import os
import stat
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Final, cast

from strif import atomic_output_file

from devtools.admit_threshold_compression import (
    MAX_CERTIFICATE_BYTES,
    REVISION_LENGTH,
    SENTINELS,
    SHA256_LENGTH,
    SOURCE_PATH,
    SOURCE_REVISION,
    AdmissionError,
    _full_control_roundtrip,
    _policy_boundary_check,
    _synthetic_decompressor_check,
)
from devtools.decide_threshold_certificate import load as load_threshold_certificate
from sqpack.fractional.threshold import ThresholdCertificate
from sqpack.fractional.threshold_compression import (
    OrbitInventory,
    catalog_sha256,
    inventory_certificate,
)
from sqpack.fractional.threshold_coverage_encoding import (
    encode_frozen_coverage,
    encoding_record,
    solve_feasibility_mip,
)

PACKING = Path(__file__).resolve().parent.parent
REPOSITORY = PACKING.parent
FROZEN_SOURCE_PACKING: Final = Path("cases/n11_threshold_certificate/certificate.json")
FROZEN_CATALOG_SHA256: Final = (
    "8de1d9646efef5c49367b679a78ff20961f7f5c1d43b11ff28b5f9a6b41f0e75"
)
FROZEN_MAX_ORBITS: Final = 23
FROZEN_BUDGET_BELOW: Final = 11
FROZEN_LEAST_CHARGE: Final = 1
AUTHORIZED_TARGET: Final = "exp-161"
RECEIPT_SCHEMA: Final = "packing.squares:ThresholdCompressionProducerReceipt/v1"
FORBIDDEN_CONTROL_MANIFESTS: Final = (
    "53fbe28bd6dd022600515663ea1e3609ed2bd36a83e69e350b4bb3b45d7b7176",
    "007b394f48b0b11565ca87d09ad961258534c426bfd623a3e9bfc15aa6495e8a",
    "194f1f9f47fc94e7f945920c38a4efdb43476719eba025ea446a1d7b91fde27e",
)


class CompressionError(ValueError):
    """The producer refused a source, catalog, policy, or authorization guard."""


def _git_content(revision: str, path: str, *, label: str) -> bytes:
    try:
        return subprocess.run(
            ["git", "show", f"{revision}:{path}"],
            cwd=REPOSITORY,
            check=True,
            capture_output=True,
        ).stdout
    except subprocess.CalledProcessError as error:
        detail = error.stderr.decode(errors="replace").strip() or "git show failed"
        raise CompressionError(f"cannot read {label} at {revision}: {detail}") from error


def _bounded_regular_bytes(path: Path, *, limit: int, label: str) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    with os.fdopen(descriptor, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise CompressionError(f"{label} must be a regular file")
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise CompressionError(f"{label} exceeds the {limit}-byte limit")
    return data


def _revision(value: object, *, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != REVISION_LENGTH
        or any(char not in "0123456789abcdef" for char in value)
    ):
        raise CompressionError(f"{label} must be a full lowercase Git revision")
    return value


def _digest(value: object, *, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != SHA256_LENGTH
        or any(char not in "0123456789abcdef" for char in value)
    ):
        raise CompressionError(f"{label} must be a lowercase SHA-256 digest")
    return value


def _canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def _bind_repository_source(path: Path, revision: str, *, label: str) -> bytes:
    """Return the complete bytes after comparing them with one Git revision and path."""
    _revision(revision, label="source revision")
    try:
        relative = path.resolve().relative_to(REPOSITORY.resolve()).as_posix()
    except ValueError as error:
        raise CompressionError(f"{label} is outside the repository") from error
    current = _bounded_regular_bytes(path, limit=MAX_CERTIFICATE_BYTES, label=label)
    reviewed = _git_content(revision, relative, label=label)
    if current != reviewed:
        raise CompressionError(f"{label} differs from its declared Git revision and path")
    return current


def _load_certificate_bytes(data: bytes, *, label: str) -> ThresholdCertificate:
    try:
        certificate, _ = load_threshold_certificate(data)
    except (TypeError, ValueError, RecursionError) as error:
        raise CompressionError(f"cannot load {label}: {error}") from None
    return certificate


def _require_frozen_policy(*, max_orbits: int, budget_below: int, least_charge: int) -> None:
    if max_orbits != FROZEN_MAX_ORBITS:
        raise CompressionError(
            f"--max-orbits must be the frozen H-163 ceiling {FROZEN_MAX_ORBITS}"
        )
    if budget_below != FROZEN_BUDGET_BELOW:
        raise CompressionError(
            f"--budget-below must be the frozen H-163 budget bound {FROZEN_BUDGET_BELOW}"
        )
    if least_charge != FROZEN_LEAST_CHARGE:
        raise CompressionError(
            f"--least-charge must be the frozen H-163 least charge {FROZEN_LEAST_CHARGE}"
        )


def _require_authorization(authorize_target: str | None) -> str | None:
    if authorize_target is None:
        return None
    if authorize_target != AUTHORIZED_TARGET:
        raise CompressionError(
            f"--authorize-target {authorize_target!r} is not {AUTHORIZED_TARGET}; "
            "refusing to construct a candidate"
        )
    return authorize_target


def resolve_source(source: Path | None) -> Path:
    """Accept only the frozen T-025 certificate, as a packing- or repository-relative path."""
    expected = (REPOSITORY / SOURCE_PATH).resolve()
    if source is None:
        path = expected
    elif source.is_absolute():
        path = source
    else:
        spelling = source.as_posix()
        if spelling == SOURCE_PATH:
            path = REPOSITORY / SOURCE_PATH
        elif spelling == FROZEN_SOURCE_PACKING.as_posix():
            path = PACKING / FROZEN_SOURCE_PACKING
        else:
            raise CompressionError(
                f"source path is {spelling!r}; expected frozen T-025 certificate"
            )
    absolute = path.absolute()
    resolved = path.resolve()
    if not resolved.is_relative_to(REPOSITORY.resolve()):
        raise CompressionError("source path escapes the repository")
    if resolved != expected:
        raise CompressionError(
            f"source path is {resolved.as_posix()!r}; expected frozen path {SOURCE_PATH!r}"
        )
    if resolved != absolute:
        raise CompressionError("source path resolves through a symlink")
    return resolved


def authenticate_source(
    *, path: Path, revision: str, expect_catalog_sha256: str
) -> OrbitInventory:
    """Bind the source bytes, inventory U025, and refuse a catalog digest mismatch."""
    data = _bind_repository_source(path, revision, label="T-025 certificate")
    certificate = _load_certificate_bytes(data, label="T-025 certificate")
    inventory = inventory_certificate(certificate)
    digest = catalog_sha256(inventory)
    expected = _digest(expect_catalog_sha256, label="expected catalog SHA-256")
    if digest != expected:
        raise CompressionError(f"U025 catalog SHA-256 is {digest}; expected {expected}")
    return inventory


def _admitted_control(name: str, inventory: OrbitInventory) -> dict[str, Any]:
    try:
        if name == "policy_boundary":
            return cast(dict[str, Any], _policy_boundary_check(inventory))
        if name == "synthetic_decompressor":
            return cast(dict[str, Any], _synthetic_decompressor_check(inventory))
        return cast(dict[str, Any], _full_control_roundtrip(inventory))
    except AdmissionError as error:
        raise CompressionError(str(error)) from error


def run_selftest_controls(inventory: OrbitInventory) -> dict[str, Any]:
    """Replay the admitted 23/24 policy and full T-025 manifest without coverage."""
    policy_boundary = _admitted_control("policy_boundary", inventory)
    synthetic = _admitted_control("synthetic_decompressor", inventory)
    full = _admitted_control("full_manifest_roundtrip", inventory)
    if policy_boundary.get("coverage_ran") is not False:
        raise CompressionError("policy-boundary control must not run coverage")
    if catalog_sha256(inventory) != full.get("catalog_sha256"):
        raise CompressionError("full T-025 decompression lost catalog identity")
    return {
        "source_bound": True,
        "catalog_matched": True,
        "source_orbits": inventory.orbit_count,
        "source_atoms": inventory.atom_count,
        "source_budget": str(inventory.total_budget),
        "policy_boundary": policy_boundary,
        "synthetic_decompressor": synthetic,
        "full_manifest_roundtrip": full,
        "coverage_ran": False,
        "selftest_ran": True,
    }


def cardinality_budget_sketch(inventory: OrbitInventory) -> dict[str, Any]:
    """Describe the coverage-free HiGHS MIP.  Do not solve it.

    Nonnegative reweighting of U025 with N+ <= 23 and budget < 11 is feasible by putting
    a tiny positive weight on any 23 orbits.  This sketch exists only as the named
    forbidden program: it does not encode closed-core coverage.  Solving it, or reporting
    its N+, would be a lying scientific result.  The authorized instrument uses
    :func:`coverage_search_instrument` instead.
    """
    coefficients = [
        orbit.budget_coefficient
        for orbit in (*inventory.point_orbits, *inventory.threshold_orbits)
    ]
    return {
        "kind": "highs_mip_nonnegative_orbit_weights",
        "orbit_count": inventory.orbit_count,
        "binary_indicators": inventory.orbit_count,
        "max_orbits": FROZEN_MAX_ORBITS,
        "budget_below": FROZEN_BUDGET_BELOW,
        "budget_coefficients": coefficients,
        "constraints": [
            "sum_i budget_coefficient_i * w_i < 11",
            "sum_i z_i <= 23",
            "w_i >= 0",
            "z_i in {0, 1}",
            "w_i = 0 when z_i = 0",
        ],
        "includes_coverage": False,
        "solver": "highs",
        "search_status": "instrument_incomplete",
        "optimizer_ran": False,
        "reason": (
            "This sketch is coverage-free on purpose and must not be solved. Frozen "
            "closed-core coverage is linear in U025 orbit weights; the authorized path "
            "encodes A w >= 1 rather than reporting a lying N+ from this program."
        ),
    }


_COVERAGE_CONSTRAINTS: Final = (
    "sum_i budget_coefficient_i * w_i < 11",
    "sum_i z_i <= 23",
    "w_i >= 0",
    "z_i in {0, 1}",
    "w_i = 0 when z_i = 0",
    "A w >= 1 on every reachable frozen event cell (Pareto-reduced rows)",
    "D4 tying: one nonnegative weight per source U025 orbit",
)


def coverage_search_instrument(
    inventory: OrbitInventory,
    *,
    enumerate_coverage: bool,
    search: bool,
) -> dict[str, Any]:
    """Formulate the linear coverage MIP; enumerate or solve only when asked.

    Default authorized use describes the linear system and enumerates nothing.
    ``enumerate_coverage`` builds the frozen ``A`` rows.  ``search`` may run only after
    that enumeration; it still does not write a candidate certificate or set ``n_plus``.
    """
    if search and not enumerate_coverage:
        raise CompressionError(
            "--search requires --encode-coverage so the MIP includes A w >= 1; "
            "refusing a coverage-free solve"
        )
    coefficients = [
        orbit.budget_coefficient
        for orbit in (*inventory.point_orbits, *inventory.threshold_orbits)
    ]
    record: dict[str, Any] = {
        "kind": "highs_mip_frozen_orbit_coverage",
        "orbit_count": inventory.orbit_count,
        "binary_indicators": inventory.orbit_count,
        "max_orbits": FROZEN_MAX_ORBITS,
        "budget_below": FROZEN_BUDGET_BELOW,
        "least_charge": FROZEN_LEAST_CHARGE,
        "budget_coefficients": coefficients,
        "constraints": list(_COVERAGE_CONSTRAINTS),
        "includes_coverage": True,
        "coverage_linear": True,
        "coverage_enumerated": False,
        "solver": "highs",
        "search_status": "encoding_ready",
        "optimizer_ran": False,
        "float_incumbent": None,
        "reason": (
            "With atoms and sites frozen, T-025 closed-core charge is A w on the event "
            "cells of the full U025 arrangement. D4 tying is one weight per orbit. "
            "Omitted orbits equal zero weights on that arrangement. This instrument does "
            "not emit a candidate or treat a float incumbent as N+."
        ),
    }
    if not enumerate_coverage:
        return record
    encoding = encode_frozen_coverage(inventory)
    record["coverage_enumerated"] = True
    record["search_status"] = "encoding_complete"
    record["encoding"] = encoding_record(encoding)
    if not search:
        return record
    outcome = solve_feasibility_mip(
        encoding, max_orbits=FROZEN_MAX_ORBITS, budget_below=FROZEN_BUDGET_BELOW
    )
    if outcome.status == "timeout_unresolved":
        record["search_status"] = "timeout_unresolved"
        record["optimizer_ran"] = True
    elif outcome.status == "float_infeasible_unresolved":
        record["search_status"] = "float_infeasible_unresolved"
        record["optimizer_ran"] = True
    elif outcome.status == "solver_error_unresolved":
        record["search_status"] = "solver_error_unresolved"
        record["optimizer_ran"] = False
    else:
        record["search_status"] = "float_incumbent_unverified"
        record["optimizer_ran"] = True
    record["float_incumbent"] = {
        "status": outcome.status,
        "n_plus": outcome.n_plus,
        "objective": outcome.objective,
        "message": outcome.message,
    }
    return record


def build_receipt(
    *,
    source: Path | None = None,
    expect_source_revision: str = SOURCE_REVISION,
    expect_catalog_sha256: str = FROZEN_CATALOG_SHA256,
    max_orbits: int = FROZEN_MAX_ORBITS,
    budget_below: int = FROZEN_BUDGET_BELOW,
    least_charge: int = FROZEN_LEAST_CHARGE,
    authorize_target: str | None = None,
    encode_coverage: bool = False,
    search: bool = False,
) -> dict[str, Any]:
    """Run source, catalog, and policy controls; emit no candidate on the default path."""
    authorization = _require_authorization(authorize_target)
    if (encode_coverage or search) and authorization != AUTHORIZED_TARGET:
        raise CompressionError(
            "--encode-coverage and --search require --authorize-target exp-161"
        )
    _require_frozen_policy(
        max_orbits=max_orbits, budget_below=budget_below, least_charge=least_charge
    )
    revision = _revision(expect_source_revision, label="source revision")
    if revision != SOURCE_REVISION:
        raise CompressionError(
            f"source revision is {revision}; expected frozen revision {SOURCE_REVISION}"
        )
    path = resolve_source(source)
    inventory = authenticate_source(
        path=path,
        revision=revision,
        expect_catalog_sha256=expect_catalog_sha256,
    )
    controls = run_selftest_controls(inventory)
    search_record: dict[str, Any] | None = None
    search_status = "not_run"
    optimizer_ran = False
    if authorization == AUTHORIZED_TARGET:
        search_record = coverage_search_instrument(
            inventory, enumerate_coverage=encode_coverage, search=search
        )
        search_status = cast(str, search_record["search_status"])
        optimizer_ran = bool(search_record["optimizer_ran"])
    return {
        "schema": RECEIPT_SCHEMA,
        "source_revision": SOURCE_REVISION,
        "catalog_sha256": catalog_sha256(inventory),
        "target_ran": False,
        "optimizer_ran": optimizer_ran,
        "candidate_created": False,
        "coverage_ran": False,
        "n_plus": None,
        "selected_orbits": None,
        "generating_account": None,
        "forbidden_control_manifests": list(FORBIDDEN_CONTROL_MANIFESTS),
        "search_status": search_status,
        "authorization": authorization,
        "max_orbits": FROZEN_MAX_ORBITS,
        "budget_below": FROZEN_BUDGET_BELOW,
        "least_charge": FROZEN_LEAST_CHARGE,
        "search": search_record,
        "controls": controls,
        "scope": (
            "Source authentication, U025 catalog identity, and the admitted 23/24-orbit "
            "policy boundary. Frozen closed-core coverage is linear in orbit weights. "
            "No candidate certificate, exact coverage route, or H-163 verdict is "
            "established on this path."
        ),
    }


def _protected_paths() -> set[Path]:
    protected = {(REPOSITORY / SOURCE_PATH).resolve()}
    protected.update((REPOSITORY / anchor.path).resolve() for anchor in SENTINELS)
    protected.update((REPOSITORY / anchor.source_path).resolve() for anchor in SENTINELS)
    return protected


def _refuse_protected_output(output: Path) -> None:
    if output.resolve() in _protected_paths():
        raise CompressionError("receipt output may not overwrite a bound input")


def _write_receipt(output: Path, encoded: bytes) -> None:
    _refuse_protected_output(output)
    with atomic_output_file(output, make_parents=True) as temporary:
        temporary.write_bytes(encoded)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    command.add_argument(
        "--source",
        type=Path,
        default=FROZEN_SOURCE_PACKING,
        help="packing-relative T-025 certificate (frozen path only)",
    )
    command.add_argument(
        "--expect-source-revision",
        default=SOURCE_REVISION,
        help="full lowercase Git revision of the frozen T-025 certificate",
    )
    command.add_argument(
        "--expect-catalog-sha256",
        default=FROZEN_CATALOG_SHA256,
        help="lowercase SHA-256 of the canonical U025 catalog",
    )
    command.add_argument("--max-orbits", type=int, default=FROZEN_MAX_ORBITS)
    command.add_argument("--budget-below", type=int, default=FROZEN_BUDGET_BELOW)
    command.add_argument("--least-charge", type=int, default=FROZEN_LEAST_CHARGE)
    command.add_argument(
        "--authorize-target",
        default=None,
        help="must be exp-161 to formulate the coverage MIP; default still emits no candidate",
    )
    command.add_argument(
        "--encode-coverage",
        action="store_true",
        help="enumerate frozen A w >= 1 rows; requires --authorize-target exp-161",
    )
    command.add_argument(
        "--search",
        action="store_true",
        help=(
            "run the encoded HiGHS MIP after --encode-coverage; still writes no candidate "
            "and does not set n_plus"
        ),
    )
    command.add_argument(
        "--selftest",
        action="store_true",
        help="replay source, catalog, and 23/24 policy controls without coverage",
    )
    command.add_argument(
        "--output",
        type=Path,
        default=None,
        help="write the producer receipt here; omitted output defaults to --selftest",
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    options = parser().parse_args(argv)
    try:
        if options.output is not None:
            _refuse_protected_output(cast(Path, options.output))
        receipt = build_receipt(
            source=options.source,
            expect_source_revision=options.expect_source_revision,
            expect_catalog_sha256=options.expect_catalog_sha256,
            max_orbits=options.max_orbits,
            budget_below=options.budget_below,
            least_charge=options.least_charge,
            authorize_target=options.authorize_target,
            encode_coverage=bool(options.encode_coverage),
            search=bool(options.search),
        )
        encoded = _canonical_json(receipt)
        if options.output is not None:
            output = cast(Path, options.output)
            _write_receipt(output, encoded)
            print(f"Route S compression producer receipt written: {output}")
        if options.selftest or options.output is None:
            print("Route S compression producer selftest passed")
    except (OSError, ValueError) as error:
        print(f"Route S compression producer refused: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
