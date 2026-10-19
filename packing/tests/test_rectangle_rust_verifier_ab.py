"""Fast admission controls for the paired exact verifier diagnostic."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from benchmarks import bench_rectangle_rust_verifier_ab as benchmark


def test_normalization_drops_only_binary_metadata() -> None:
    normalize = benchmark._normalized  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    report: dict[str, Any] = {
        "status": "INCONCLUSIVE",
        "angles": [{"index": 1, "nodes": 1000, "unresolved_leaves": 1}],
        "backend": "rust",
        "rust_binary_sha256": "binary",
        "rust_table_sha256": "table",
        "backend_timeout": False,
    }
    normalized = normalize(report)
    assert normalized == {"status": report["status"], "angles": report["angles"]}
    with pytest.raises(ValueError, match="unadmitted backend"):
        normalize({**report, "backend_timeout": True})
    with pytest.raises(ValueError, match="missing backend metadata"):
        normalize({key: value for key, value in report.items() if key != "rust_table_sha256"})


def test_material_rule_requires_complete_pairs_and_separated_cpu_ranges() -> None:
    assess = benchmark._assess  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    rows: list[dict[str, Any]] = []
    for dataset in ("analytic", "external"):
        for pair in range(3):
            rows.extend(
                (
                    {
                        "dataset": dataset,
                        "pair": pair,
                        "arm": "reference",
                        "rust_child_cpu_seconds": 10.0 + pair / 100,
                        "invocation_wall_seconds": 20.0 + pair / 100,
                    },
                    {
                        "dataset": dataset,
                        "pair": pair,
                        "arm": "default",
                        "rust_child_cpu_seconds": 8.0 + pair / 100,
                        "invocation_wall_seconds": 19.0 + pair / 100,
                    },
                )
            )
    assert assess(rows)["material_bounded_verifier_improvement"] is True
    with pytest.raises(ValueError, match="census is incomplete or unexpected"):
        assess([*rows, {**rows[-1], "dataset": "unexpected"}])
    with pytest.raises(ValueError, match="census is incomplete"):
        assess(rows[:-1])
    duplicated = [dict(row) for row in rows]
    duplicated[-1]["pair"] = 1
    with pytest.raises(ValueError, match="identities are duplicated"):
        assess(duplicated)
    overlapping = [dict(row) for row in rows]
    for row in overlapping:
        if row["dataset"] == "external" and row["arm"] == "default":
            row["rust_child_cpu_seconds"] = 9.9 + row["pair"] / 10
    assert assess(overlapping)["material_bounded_verifier_improvement"] is False


@pytest.fixture
def build_tools(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> tuple[dict[str, str], list[tuple[str, ...]], dict[str, bool]]:
    source = tmp_path / "source.rs"
    source.write_text("frozen source", encoding="utf-8")
    sources = {str(source): benchmark._sha(source)}  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    for name, value in (
        ("TMPDIR", tmp_path),
        ("UV_CACHE_DIR", tmp_path / "uv"),
        ("CARGO_TARGET_DIR", tmp_path / "ambient-cargo"),
    ):
        monkeypatch.setenv(name, str(value))
    monkeypatch.setattr(benchmark.platform, "system", lambda: "Linux")
    commands: list[tuple[str, ...]] = []
    state = {"mutate_source": False}

    def fake_run(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        commands.append(tuple(command))
        assert kwargs["cwd"] == benchmark.CRATE
        if command[:2] == ["cargo", "build"]:
            environment = kwargs["env"]
            assert isinstance(environment, dict)
            target = Path(environment["CARGO_TARGET_DIR"])
            binary = target / "release/sqverify-exact"
            binary.parent.mkdir(parents=True, exist_ok=True)
            binary.write_bytes(
                b"reference" if "--no-default-features" in command else b"default"
            )
            if state["mutate_source"]:
                source.write_text("changed source", encoding="utf-8")
        return subprocess.CompletedProcess(
            command, 0, stdout=f"{command[0]} pinned toolchain", stderr=""
        )

    monkeypatch.setattr(benchmark.subprocess, "run", fake_run)
    return sources, commands, state


@pytest.fixture
def built_variants(
    build_tools: tuple[dict[str, str], list[tuple[str, ...]], dict[str, bool]],
    tmp_path: Path,
) -> tuple[dict[str, Path], dict[str, dict[str, object]], dict[str, str]]:
    sources, _, _ = build_tools
    binaries: dict[str, Path] = {}
    builds: dict[str, dict[str, object]] = {}
    for arm in ("reference", "default"):
        binaries[arm], builds[arm] = benchmark._build_variant(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
            arm, tmp_path / arm, sources
        )
    return binaries, builds, sources


def test_fresh_builder_executes_distinct_feature_selections(
    build_tools: tuple[dict[str, str], list[tuple[str, ...]], dict[str, bool]],
    built_variants: tuple[dict[str, Path], dict[str, dict[str, object]], dict[str, str]],
) -> None:
    _, commands, _ = build_tools
    binaries, builds, sources = built_variants
    build_commands = [command for command in commands if command[:2] == ("cargo", "build")]
    base = ("cargo", "build", "--offline", "--locked", "--release")
    assert build_commands == [(*base, "--no-default-features"), base]
    assert binaries["reference"].parent.parent != binaries["default"].parent.parent
    assert builds["reference"]["default_features"] is False
    assert builds["default"]["default_features"] is True
    for arm in ("reference", "default"):
        assert builds[arm]["source_sha256"] == sources
        assert builds[arm]["ceiling_seconds"] == 90
        assert builds[arm]["scratch_policy"] == "linux-absolute-writable-outside-repository"
        scratch = builds[arm]["scratch_paths"]
        assert isinstance(scratch, dict)
        assert scratch["CARGO_TARGET_DIR"] == str(binaries[arm].parent.parent)
    hashes = benchmark._admit_builds(binaries, builds, sources)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert hashes == {
        arm: benchmark._sha(binary)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        for arm, binary in binaries.items()
    }


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("arm", "reference", "selection"),
        ("command", ["cargo", "build", "--features", "experimental-coprime-mul"], "selection"),
        ("default_features", False, "selection"),
        ("target_dir", "/different-target", "selection"),
        ("source_sha256", {"different": "source"}, "different source"),
        ("rustc_version", "other rustc", "environment differs"),
        ("cargo_version", "other cargo", "environment differs"),
        ("rustflags", "other flags", "environment differs"),
        ("cargo_encoded_rustflags", "other encoded flags", "environment differs"),
        ("binary_sha256", "wrong binary", "binary differs"),
    ],
)
def test_build_admission_refuses_mismatched_provenance(
    built_variants: tuple[dict[str, Path], dict[str, dict[str, object]], dict[str, str]],
    field: str,
    value: object,
    message: str,
) -> None:
    binaries, builds, sources = built_variants
    changed = {arm: dict(build) for arm, build in builds.items()}
    changed["default"][field] = value
    with pytest.raises(ValueError, match=message):
        benchmark._admit_builds(binaries, changed, sources)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001


def test_build_admission_refuses_same_binary_contamination(
    built_variants: tuple[dict[str, Path], dict[str, dict[str, object]], dict[str, str]],
) -> None:
    binaries, builds, sources = built_variants
    binaries["default"].write_bytes(binaries["reference"].read_bytes())
    builds["default"]["binary_sha256"] = benchmark._sha(binaries["default"])  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    with pytest.raises(ValueError, match="binaries are identical"):
        benchmark._admit_builds(binaries, builds, sources)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001


def test_builder_refuses_source_drift_during_build(
    build_tools: tuple[dict[str, str], list[tuple[str, ...]], dict[str, bool]],
    tmp_path: Path,
) -> None:
    sources, _, state = build_tools
    state["mutate_source"] = True
    with pytest.raises(ValueError, match="source, input, or binary changed"):
        benchmark._build_variant("reference", tmp_path / "reference", sources)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001


@pytest.mark.parametrize("relative", [True, False])
def test_scratch_refuses_relative_and_source_contained_paths(
    monkeypatch: pytest.MonkeyPatch, *, relative: bool
) -> None:
    monkeypatch.setattr(benchmark.platform, "system", lambda: "Linux")
    path = Path("relative") if relative else benchmark.PROJECT / "private-scratch"
    with pytest.raises(ValueError, match=r"absolute|outside the repository"):
        benchmark._external_scratch(path)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001


def test_scratch_resolves_symlinks_before_source_boundary(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(benchmark.platform, "system", lambda: "Linux")
    alias = tmp_path / "source-alias"
    alias.symlink_to(benchmark.PROJECT.parent, target_is_directory=True)
    with pytest.raises(ValueError, match="outside the repository"):
        benchmark._external_scratch(alias / "private-scratch")  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001


@pytest.mark.parametrize("name", ["TMPDIR", "UV_CACHE_DIR", "CARGO_TARGET_DIR"])
@pytest.mark.parametrize("relative", [True, False])
def test_builder_refuses_unsafe_environment_paths(
    build_tools: tuple[dict[str, str], list[tuple[str, ...]], dict[str, bool]],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    name: str,
    *,
    relative: bool,
) -> None:
    sources, commands, _ = build_tools
    path = Path("relative") if relative else benchmark.PROJECT / "private-scratch"
    monkeypatch.setenv(name, str(path))
    with pytest.raises(ValueError, match=r"absolute|outside the repository"):
        benchmark._build_variant("reference", tmp_path / "reference", sources)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert commands == []


def test_mac_scratch_retains_original_mounted_volume_admission(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(benchmark.platform, "system", lambda: "Darwin")
    admitted: list[Path] = []
    monkeypatch.setattr(benchmark, "ensure_external_scratch", admitted.append)
    target = tmp_path / "mac-scratch"
    assert benchmark._external_scratch(target) == target.resolve()  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert admitted == [target.resolve()]


@pytest.mark.parametrize("dataset", ["analytic", "external"])
def test_material_rule_rejects_wall_regression(dataset: str) -> None:
    rows = [
        {
            "dataset": name,
            "pair": pair,
            "arm": arm,
            "rust_child_cpu_seconds": 10.0 if arm == "reference" else 8.0,
            "invocation_wall_seconds": (22.0 if name == dataset and arm == "default" else 20.0),
        }
        for name in ("analytic", "external")
        for pair in range(3)
        for arm in ("reference", "default")
    ]
    assert benchmark._assess(rows)["material_bounded_verifier_improvement"] is False  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001


@pytest.mark.parametrize("relative", [True, False])
def test_run_refuses_unsafe_output_paths(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, *, relative: bool
) -> None:
    monkeypatch.setattr(benchmark.platform, "system", lambda: "Linux")
    output = Path("receipt.json") if relative else benchmark.PROJECT / "receipt.json"
    with pytest.raises(ValueError, match=r"absolute|outside the repository"):
        benchmark.run(tmp_path / "targets", output)


@pytest.mark.parametrize("relative", [True, False])
def test_run_refuses_unsafe_target_paths(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, *, relative: bool
) -> None:
    monkeypatch.setattr(benchmark.platform, "system", lambda: "Linux")
    target = Path("targets") if relative else benchmark.PROJECT / "targets"
    with pytest.raises(ValueError, match=r"absolute|outside the repository"):
        benchmark.run(target, tmp_path / "receipt.json")


def test_receipt_publication_is_complete_and_refuses_existing_output(tmp_path: Path) -> None:
    publish = benchmark._publish_receipt  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    output = tmp_path / "receipt.json"
    result: dict[str, object] = {"status": "complete", "observations": [1, 2, 3]}
    publish(output, result)
    assert json.loads(output.read_text()) == result
    before = output.read_bytes()
    with pytest.raises(ValueError, match="refusing to overwrite"):
        publish(output, {"status": "replacement"})
    assert output.read_bytes() == before
    assert list(tmp_path.iterdir()) == [output]


def test_receipt_publication_failure_leaves_no_final_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    output = tmp_path / "receipt.json"

    def fail_before_commit(*_: object) -> None:
        raise OSError("injected pre-commit failure")

    monkeypatch.setattr(benchmark.os, "link", fail_before_commit)
    with pytest.raises(OSError, match="injected pre-commit failure"):
        benchmark._publish_receipt(output, {"status": "complete"})  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert not output.exists()
    assert list(tmp_path.iterdir()) == []


def test_receipt_publication_preserves_a_late_competing_receipt(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    output = tmp_path / "receipt.json"
    link = benchmark.os.link

    def competing_writer(source: Path, destination: Path) -> None:
        output.write_text("competing receipt")
        link(source, destination)

    monkeypatch.setattr(benchmark.os, "link", competing_writer)
    with pytest.raises(ValueError, match="refusing to overwrite"):
        benchmark._publish_receipt(output, {"status": "complete"})  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert output.read_text() == "competing receipt"
    assert list(tmp_path.iterdir()) == [output]
