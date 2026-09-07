"""Replay the two Boost-free stages of the anabologyco-maker chain for s(17) >= 9141/2000.

Copies the retained package to a temporary directory, restores the four files this
archive keeps XZ-compressed and checks their raw SHA-256 values, checks the source's own
``SHA256SUMS`` manifest, then runs ``scripts/check_certificate.py`` (exact mass and
symmetry) and ``scripts/verify_filter.py`` (the exact Bernstein prefilter of the
1,344,862 event polynomials) and requires their PASS markers. The Sturm partition, the
endpoint audits and the 148,937-cell coverage audit need a C++ compiler with
Boost.Multiprecision, and the Lean layer needs Lean 4.33; this script does not run
them. Needs Python 3 with NumPy, so run it with the project interpreter.
"""

from __future__ import annotations

import hashlib
import lzma
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def say(text: str) -> None:
    sys.stdout.write(text + "\n")


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "anabologyco-square17-lower-bound"
RAW_HASHES = HERE / "raw-hashes-of-compressed-files.sha256"
COMPRESSED = (
    "data/event_polys.npy",
    "data/event_polys_filtered.tsv",
    "data/orientation_samples.tsv",
    "lean/Square17/SampleDataFull.lean",
)
STAGES = (
    ("scripts/check_certificate.py", "EXACT CERTIFICATE ARITHMETIC PASS"),
    ("scripts/verify_filter.py", "EXACT BERNSTEIN FILTER PASS"),
)


def _expected_hashes() -> dict[str, str]:
    expected: dict[str, str] = {}
    for line in RAW_HASHES.read_text(encoding="utf-8").splitlines():
        digest, _, name = line.strip().partition("  ")
        expected[name] = digest
    return expected


def _check_manifest(root: Path) -> int:
    failures = 0
    for line in (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, _, name = line.strip().partition("  ")
        target = root / name.removeprefix("./")
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != digest:
            say(f"REFUSED: {name} hashes to {actual}, manifest says {digest}")
            failures += 1
    return failures


def main() -> int:
    expected = _expected_hashes()
    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch) / "package"
        shutil.copytree(SOURCE, root)
        for name in COMPRESSED:
            packed = root / (name + ".xz")
            raw = lzma.decompress(packed.read_bytes())
            digest = hashlib.sha256(raw).hexdigest()
            if digest != expected[name]:
                say(f"REFUSED: {name} decompresses to {digest}, expected {expected[name]}")
                return 1
            (root / name).write_bytes(raw)
            packed.unlink()
        say("restored the four compressed files; raw SHA-256 values match")
        if _check_manifest(root):
            return 1
        say("SHA256SUMS: every entry matches")
        for script, marker in STAGES:
            run = subprocess.run(
                [sys.executable, str(root / script)],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            sys.stdout.write(run.stdout)
            sys.stderr.write(run.stderr)
            if run.returncode != 0 or marker not in run.stdout:
                say(f"REFUSED: {script} did not print '{marker}'")
                return 1
    say(
        "REPLAYED: the certificate-arithmetic and Bernstein-filter stages pass; "
        "the Sturm, endpoint and coverage stages were not run"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
