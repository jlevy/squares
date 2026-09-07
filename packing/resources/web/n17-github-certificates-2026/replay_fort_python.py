"""Replay Fort's s(17) > 4.456575 certificate with the source's own pure-Python checker.

Decompresses the retained XZ stream to a temporary file, checks the raw SHA-256 the
source publishes, then runs ``verify_certificate.py`` from the retained package and
requires its ``PYTHON_INTEGER_CERTIFICATE_VALID`` marker. Needs only Python 3; no
Boost, no compiler. About 20 s.
"""

from __future__ import annotations

import hashlib
import lzma
import subprocess
import sys
import tempfile
from pathlib import Path


def say(text: str) -> None:
    sys.stdout.write(text + "\n")


HERE = Path(__file__).resolve().parent
PACKAGE = HERE / "stanislavfort-17squares" / "certificates" / "lower_bound_4p456575"
ARCHIVE = PACKAGE / "square17_lb_4p456575.cert.xz"
RAW_SHA256 = "5fbee90dc6fedc1851e4b8b9866f8ffa41c38cb09ebb6a9f748096217f078550"
MARKER = "PYTHON_INTEGER_CERTIFICATE_VALID"


def main() -> int:
    raw = lzma.decompress(ARCHIVE.read_bytes())
    digest = hashlib.sha256(raw).hexdigest()
    if digest != RAW_SHA256:
        say(f"REFUSED: decompressed certificate hashes to {digest}, expected {RAW_SHA256}")
        return 1
    say(f"decompressed {len(raw)} bytes; SHA-256 matches the source's {RAW_SHA256[:12]}...")
    with tempfile.TemporaryDirectory() as scratch:
        certificate = Path(scratch) / "square17_lb_4p456575.cert"
        certificate.write_bytes(raw)
        run = subprocess.run(
            [sys.executable, str(PACKAGE / "verify_certificate.py"), str(certificate)],
            capture_output=True,
            text=True,
            check=False,
        )
    sys.stdout.write(run.stdout)
    sys.stderr.write(run.stderr)
    accepted = any(line.startswith(MARKER) for line in run.stdout.splitlines())
    if run.returncode != 0 or not accepted:
        say("REFUSED: the source checker did not print its validity marker")
        return 1
    say("REPLAYED: Fort's certificate for s(17) > 4456575/1000000 is accepted by its checker")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
