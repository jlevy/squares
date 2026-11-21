"""Rectangle-receipt arithmetic and source checks, without executing producer code."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import NoReturn

import pytest

from devtools import replay_rectangle_receipts as replay


def test_mutants_scale_density_and_mass_only_rounding_down() -> None:
    rows = [(1, 2, 3, 4, 5, 6, 7, 8, 101, 1001)]
    assert replay.scaled(rows, Fraction(99, 100)) == [(1, 2, 3, 4, 5, 6, 7, 8, 99, 990)]
    assert replay.scaled(rows, Fraction(1, 4)) == [(1, 2, 3, 4, 5, 6, 7, 8, 25, 250)]


def test_the_set_header_is_the_square_kernels_with_the_core_domain_switch() -> None:
    measure = {"proof_net": {"step": "83/40000"}, "L": "1931/400", "B": "9977/10000"}
    g = 2**30
    header = replay.set_header(measure, 1, None)
    t = Fraction(83, 40000)
    c, s, e = (
        t.denominator**2 - t.numerator**2,
        2 * t.numerator * t.denominator,
        t.denominator**2 + t.numerator**2,
    )
    assert header[:3] == [c, s, e]
    left = t - t / 2
    v = (1 + 2 * left - left**2) / (2 * (1 + left**2))
    assert header[7] == (g * (Fraction(1931, 400) - v)).__ceil__()
    contained = replay.set_header(measure, 1, "contained_core")
    core_v = Fraction(9977, 10000) * Fraction(c + s, 2 * e)
    assert contained[7] == (g * (Fraction(1931, 400) - core_v)).__ceil__()
    assert contained[:7] == header[:7]


def test_a_refusal_counts_on_coverage_only_with_an_unresolved_box() -> None:
    base = {
        "folder": "f",
        "mutant": "99/100",
        "n": 7,
        "side": "3",
        "kernel": "square",
        "verified": False,
        "matches_archive": False,
        "nodes": 5,
        "cpu_seconds_approx": 0.1,
    }
    rows = [
        {**base, "verdict": "UNDECIDED", "unresolved": "unresolved 1 2 bound 3"},
        {**base, "verdict": "UNDECIDED", "unresolved": None},
        {**base, "verdict": "PASS", "unresolved": None},
    ]
    summary = replay.summarize(rows)["f|99/100"]
    assert (summary["directions"], summary["refused_on_coverage"], summary["nodes"]) == (
        3,
        1,
        15,
    )


@pytest.fixture
def producer_sources(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    retained = tmp_path / "retained"
    checkout = tmp_path / "checkout"
    retained.mkdir()
    checkout.mkdir()
    for name in replay.SOURCE_FILES:
        raw = f"synthetic pinned bytes for {name}\n".encode()
        (retained / name).write_bytes(raw)
        (checkout / name).write_bytes(raw)
    monkeypatch.setattr(replay, "RETAINED_SOURCE", retained)
    return retained, checkout


@pytest.mark.parametrize("changed", replay.SOURCE_FILES)
def test_main_rejects_changed_source_before_import(
    producer_sources: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    changed: str,
) -> None:
    _, checkout = producer_sources
    (checkout / changed).write_bytes(b"untrusted replacement")

    def unexpected_import(_source: Path) -> NoReturn:
        pytest.fail("producer import reached before source validation")

    monkeypatch.setattr(replay, "load_source", unexpected_import)
    with pytest.raises(SystemExit, match="differs from the retained source packet"):
        replay.main(["--source", str(checkout), "--out", str(tmp_path / "out"), "unused"])
    assert not (tmp_path / "out").exists()


def test_main_imports_only_the_validated_snapshot(
    producer_sources: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    retained, checkout = producer_sources
    (checkout / "__pycache__").mkdir()
    (checkout / "__pycache__/check.cpython-314.pyc").write_bytes(b"untrusted bytecode")

    def inspect_import(source: Path) -> NoReturn:
        assert source != checkout
        assert sorted(path.name for path in source.iterdir()) == sorted(replay.SOURCE_FILES)
        for name in replay.SOURCE_FILES:
            (checkout / name).write_bytes(b"changed after validation")
            assert (source / name).read_bytes() == (retained / name).read_bytes()
        raise RuntimeError("validated snapshot reached import")

    monkeypatch.setattr(replay, "load_source", inspect_import)
    with pytest.raises(RuntimeError, match="validated snapshot reached import"):
        replay.main(["--source", str(checkout), "--out", str(tmp_path / "out"), "unused"])


@pytest.mark.parametrize("changed", ("native_sha256", "wrapper_sha256"))
def test_receipt_source_mismatch_stops_before_compilation(
    producer_sources: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    changed: str,
) -> None:
    _, checkout = producer_sources
    folder = tmp_path / "certificate"
    folder.mkdir()
    manifest = {
        "kernel": "square",
        "native_sha256": replay.sha256((checkout / "bmcheck.cpp").read_bytes()),
        "wrapper_sha256": replay.sha256((checkout / "bm.py").read_bytes()),
        "levels": [],
    }
    manifest[changed] = "different"
    (folder / "manifest.json").write_text(json.dumps(manifest))

    def unexpected_compile(_source: Path, _kernel: str, _workdir: Path) -> NoReturn:
        pytest.fail("compiler reached before receipt source validation")

    monkeypatch.setattr(replay, "compile_kernel", unexpected_compile)
    with pytest.raises(SystemExit, match="kernel or wrapper digest differs"):
        replay.replay_folder(
            folder,
            checkout,
            ModuleType("synthetic_check"),
            ModuleType("synthetic_bm"),
            tmp_path,
            mutant="none",
            first_per_level=False,
            workers=1,
            cap=1,
        )
