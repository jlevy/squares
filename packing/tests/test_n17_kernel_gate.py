"""Fail-closed contracts for the ordinary-U native verifier's required gate."""

# pyright: reportPrivateUsage=false
# ruff: noqa: SLF001 -- These contracts deliberately exercise internal gate seams.
from __future__ import annotations

import json
import tomllib
from fractions import Fraction
from pathlib import Path

import pytest

from sqpack.cli import validate
from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]
CRATE = REPO / "packing/n17_kernel_verify"


def context(**environment: str) -> validate.Context:
    return validate.Context(
        deep=False,
        strict=True,
        jobs=1,
        inner_jobs=1,
        environment=environment,
        timeout_seconds=300,
    )


def test_native_gate_runs_full_floor_without_mutating_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = context(RUSTDOCFLAGS="old", CARGO_TARGET_DIR="/external/native")
    observed: list[tuple[str, ...]] = []

    def commands(
        child: validate.Context,
        argv: tuple[tuple[str, ...], ...],
        *,
        cwd: Path,
    ) -> str:
        assert cwd == CRATE
        assert child.timeout_seconds == 120
        assert child.environment["RUSTDOCFLAGS"] == "old -D warnings"
        assert child.environment["CARGO_TARGET_DIR"] == "/external/native"
        observed.extend(argv)
        return "floor probes passed"

    def run(child: validate.Context, argv: tuple[str, ...], *, cwd: Path) -> str:
        assert cwd == CRATE
        assert child.timeout_seconds == 120
        observed.append(argv)
        return (
            "test result: ok. 22 passed; 0 failed; 0 ignored; 0 filtered out\n"
            "test result: ok. 0 passed; 0 failed; 0 ignored; 0 filtered out\n"
            "test result: ok. 1 passed; 0 failed; 0 ignored; 0 filtered out"
        )

    monkeypatch.setattr(validate, "_run", run)
    monkeypatch.setattr(validate.shutil, "which", lambda *_args, **_kwargs: "/cargo")
    monkeypatch.setattr(validate, "_commands", commands)
    assert "no centered-mode or census adoption claim" in validate._rust_n17_kernel_verifier(
        original
    )
    assert original.environment["RUSTDOCFLAGS"] == "old"
    assert ("/cargo", "fmt", "--all", "--check") in observed
    assert (
        "/cargo",
        "clippy",
        "--locked",
        "--release",
        "--all-targets",
        "--quiet",
        "--",
        "-D",
        "warnings",
    ) in observed
    assert ("/cargo", "test", "--locked", "--release", "--all-targets", "--quiet") in observed
    assert ("/cargo", "doc", "--locked", "--release", "--no-deps", "--quiet") in observed
    assert any(argv[-2:] == ("--crate", str(CRATE)) for argv in observed)
    assert not any("--no-run" in argv for argv in observed)


@pytest.mark.parametrize(
    "output",
    [
        "",
        "test result: ok. 0 passed; 0 failed",
        "test result: ok. 22 passed; 0 failed",
        "test result: ok. 22 passed; 0 failed\ntest result: ok. 1 passed; 0 failed; 1 ignored",
        (
            "test result: ok. 22 passed; 0 failed\n"
            "test result: ok. 1 passed; 0 failed; 1 filtered out"
        ),
    ],
)
def test_native_gate_refuses_missing_or_omitted_controls(
    monkeypatch: pytest.MonkeyPatch,
    output: str,
) -> None:
    monkeypatch.setattr(validate.shutil, "which", lambda *_args, **_kwargs: "/cargo")
    monkeypatch.setattr(
        validate, "_commands", lambda *_args, **_kwargs: "test result: ok. 99 passed"
    )
    monkeypatch.setattr(validate, "_run", lambda *_args, **_kwargs: output)
    with pytest.raises(validate.StepFailureError):
        validate._rust_n17_kernel_verifier(context())


def test_native_gate_refuses_missing_compiler(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(validate.shutil, "which", lambda *_args, **_kwargs: None)
    with pytest.raises(validate.StepFailureError, match="requires cargo"):
        validate._rust_n17_kernel_verifier(context())


def test_native_gate_preserves_floor_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(validate.shutil, "which", lambda *_args, **_kwargs: "/cargo")

    def fail(*_args: object, **_kwargs: object) -> str:
        raise validate.StepFailureError("missing documentation")

    monkeypatch.setattr(validate, "_commands", fail)
    with pytest.raises(validate.StepFailureError, match="missing documentation"):
        validate._rust_n17_kernel_verifier(context())


def test_native_gate_is_required_and_change_reachable() -> None:
    [step] = [item for item in validate.STEPS if item.name == "n17 kernel verifier (Rust)"]
    assert step.fast
    assert step.broad
    assert step.measure_verifier
    for path in (
        "packing/n17_kernel_verify/cells/cover.json",
        "packing/n17_kernel_verify/src/verify.rs",
        "packing/devtools/verify_n17_kernel_certificate.py",
        "packing/tests/test_n17_kernel_gate.py",
        "packing/campaign/explorations/X048-session-168-pilots/audit-verifier-rewrites/fixture-w7-bins8/node.json.gz",
    ):
        assert step.reachable_from(path)
    assert step in validate._select_steps(only=[], fast=True)
    assert step in validate._select_steps(only=[], fast=False, measure_verifier=True)


def test_native_manifest_toolchain_and_test_panic_policy() -> None:
    manifest = tomllib.loads((CRATE / "Cargo.toml").read_text())
    assert manifest["package"]["publish"] is False
    assert manifest["package"]["rust-version"] == "1.98"
    assert manifest["lints"]["rust"] == {
        "unsafe_code": "forbid",
        "missing_docs": "deny",
        "warnings": "deny",
    }
    assert manifest["lints"]["clippy"]["pedantic"]["level"] == "deny"
    assert manifest["lints"]["clippy"]["unwrap_used"] == "deny"
    toolchain = tomllib.loads((CRATE / "rust-toolchain.toml").read_text())["toolchain"]
    assert toolchain["channel"] == "1.98.0"
    assert set(toolchain["components"]) == {"clippy", "rustfmt"}
    assert tomllib.loads((CRATE / "clippy.toml").read_text()) == {
        "allow-unwrap-in-tests": True,
        "allow-expect-in-tests": True,
    }


def test_declared_world_matches_the_exact_standing_catalogue() -> None:
    from devtools import check_n17_capacity_one_cover as cover  # noqa: PLC0415

    world = json.loads((CRATE / "cells/cover.json").read_text())
    cells = cover.build_cover(cover.UNIQUE_24)
    assert world["design"] == cover.UNIQUE_24.name
    assert Fraction(world["U"]) == cover.U
    assert world["order"] == [cell.name for cell in cells]
    assert set(world["cells"]) == set(world["order"])
    for cell in cells:
        assert (
            tuple(
                tuple(Fraction(value) for value in point) for point in world["cells"][cell.name]
            )
            == cell.vertices
        )


def test_hosted_cold_build_is_bounded_and_never_substitutes_for_controls() -> None:
    workflow = safe_load((REPO / ".github/workflows/packing-validation.yml").read_text())
    for job_name in ("validate", "measure-verifier"):
        steps = workflow["jobs"][job_name]["steps"]
        [prepare] = [
            step
            for step in steps
            if step["name"] == "Prepare the ordinary n17 verifier under its cold ceiling"
        ]
        assert "600s" in prepare["run"]
        assert "--kill-after=10s" in prepare["run"]
        assert "--no-run" in prepare["run"]
        [key] = [step for step in steps if step.get("id") == "n17-kernel-key"]
        assert "rustc -vV" in key["run"]
        assert "Cargo.lock" in key["run"]
        assert "HEAD:packing/n17_kernel_verify" in key["run"]
        [save] = [
            step
            for step in steps
            if step["name"] == "Retain ordinary n17 verifier dependency intermediates"
        ]
        assert "always()" in save["if"]
        # Cargo revalidates partial dependencies even after a failed cold compile.
        assert "populate" not in save["if"]
    commands = [step.get("run", "") for step in workflow["jobs"]["measure-verifier"]["steps"]]
    assert any("packing-validate --measure-verifier" in command for command in commands)


@pytest.mark.parametrize("native", [True, False])
def test_census_requires_the_current_reviewed_single_file_listing(*, native: bool) -> None:
    from devtools import census_n17_certified as census  # noqa: PLC0415

    listing = {
        "id": "reviewed-python",
        "certifier": "kernel",
        "path": "packing/devtools/verify_n17_kernel_certificate.py",
    }
    receipt = {
        "provenance": (
            {
                "implementation": "rust",
                "crate": "n17-kernel-verifier",
                "source_sha256": "diagnostic",
            }
            if native
            else {"files": {listing["path"]: "diagnostic"}, "dirty": False}
        )
    }
    args = (
        {"verifier": listing["id"]},
        receipt,
        {listing["id"]: listing},
        {"name": "synthetic-fixture", "certifier": "kernel"},
        "synthetic native boundary",
    )
    if native:
        with pytest.raises(census.RefusedError, match="no single verifier"):
            census.listing_of(*args)
    else:
        assert census.listing_of(*args) == listing
