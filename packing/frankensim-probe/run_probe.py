"""Run the two packing probes against an explicit local FrankenSim checkout.

The command temporarily installs the repository-owned Rust examples into the checkout.
It refuses to overwrite existing example files and restores the FrankenSim manifest in
all exit paths.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path

from strif import atomic_output_file

HERE = Path(__file__).resolve().parent


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, help="local FrankenSim repository")
    return parser


def _write_atomic(path: Path, content: str) -> None:
    with atomic_output_file(path) as temporary:
        temporary.write_text(content, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    """Install, run, and remove the two probe examples."""
    parser = _parser()
    options = parser.parse_args(argv)
    checkout = options.checkout.resolve()
    if not (checkout / "Cargo.toml").is_file():
        parser.error(f"not a FrankenSim checkout: {checkout}")

    manifest = checkout / "crates/fs-ad/Cargo.toml"
    destinations = (
        checkout / "crates/fs-ivl/examples/packing_sat.rs",
        checkout / "crates/fs-rand/examples/schedule_invariance.rs",
    )
    existing = [path for path in destinations if path.exists()]
    if existing:
        parser.error(f"refusing to overwrite existing probe targets: {existing}")

    original_manifest = manifest.read_text(encoding="utf-8")
    patched_manifest = original_manifest.replace(
        'package = "frankentorch-autograd", ', ""
    ).replace('package = "frankentorch-core", ', "")
    created_directories: list[Path] = []
    try:
        if patched_manifest != original_manifest:
            print("[probe] temporarily patching constellation package-name drift")
            _write_atomic(manifest, patched_manifest)
        for source, destination in zip(
            (HERE / "packing_sat.rs", HERE / "schedule_invariance.rs"),
            destinations,
            strict=True,
        ):
            if not destination.parent.exists():
                destination.parent.mkdir(parents=True)
                created_directories.append(destination.parent)
            shutil.copy2(source, destination)

        print("fs-ivl: certified interval verification")
        subprocess.run(
            ["cargo", "run", "--quiet", "-p", "fs-ivl", "--example", "packing_sat"],
            cwd=checkout,
            check=True,
        )
        print("fs-rand: schedule-independent counter-based stream")
        subprocess.run(
            [
                "cargo",
                "run",
                "--quiet",
                "--release",
                "-p",
                "fs-rand",
                "--example",
                "schedule_invariance",
            ],
            cwd=checkout,
            check=True,
        )
    finally:
        _write_atomic(manifest, original_manifest)
        for destination in destinations:
            destination.unlink(missing_ok=True)
        for directory in reversed(created_directories):
            directory.rmdir()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
