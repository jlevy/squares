"""Fast controls for the exact arithmetic A/B build provenance."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import pytest

from benchmarks import bench_rectangle_rust_transport as benchmark


def test_variant_builder_binds_executed_features_and_binary_bytes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("TMPDIR", str(tmp_path))
    monkeypatch.setenv("UV_CACHE_DIR", str(tmp_path / "uv"))
    monkeypatch.setenv("CARGO_TARGET_DIR", str(tmp_path / "cargo"))
    commands: list[tuple[str, ...]] = []

    def fake_run(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        commands.append(tuple(command))
        assert kwargs["cwd"] == benchmark.CRATE
        if command[:2] == ["cargo", "build"]:
            environment = kwargs["env"]
            assert isinstance(environment, dict)
            binary = Path(environment["CARGO_TARGET_DIR"]) / "release/sqverify-exact"
            binary.parent.mkdir(parents=True)
            binary.write_bytes(command[-1].encode())
        return subprocess.CompletedProcess(command, 0, stdout="pinned toolchain", stderr="")

    monkeypatch.setattr(benchmark.subprocess, "run", fake_run)
    candidate, baseline, provenance = benchmark._build_variants(tmp_path / "variants")  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert baseline.read_bytes() == b"experimental-normalized-mul"
    assert candidate.read_bytes() == b"experimental-coprime-mul"
    assert commands[-2][2:] == (
        "--offline",
        "--locked",
        "--release",
        "--no-default-features",
        "--features",
        "experimental-normalized-mul",
    )
    assert commands[-1][2:] == (
        "--offline",
        "--locked",
        "--release",
        "--no-default-features",
        "--features",
        "experimental-coprime-mul",
    )
    assert commands[-2][-1] == "experimental-normalized-mul"
    assert commands[-1][-1] == "experimental-coprime-mul"
    builds = provenance["builds"]
    assert isinstance(builds, list)
    assert [item["binary_sha256"] for item in builds] == [
        benchmark._sha(baseline),  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        benchmark._sha(candidate),  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    ]
    sources = provenance["source_sha256"]
    assert isinstance(sources, dict)
    assert len(sources) == 5


def test_variant_builder_refuses_internal_or_relative_target(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in ("TMPDIR", "UV_CACHE_DIR", "CARGO_TARGET_DIR"):
        monkeypatch.setenv(name, "/unused")
    with pytest.raises(ValueError, match="outside the source tree"):
        benchmark._build_variants(Path("relative"))  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    with pytest.raises(ValueError, match="outside the source tree"):
        benchmark._build_variants(benchmark.PROJECT / "target")  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
