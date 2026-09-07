"""Replay Mira's s(17) > 4.468292 certificate with the source's own pure-Python checker.

Checks the SHA-256 of the retained XZ archive (the source's own transport form),
decompresses it to a temporary file, checks the raw SHA-256 the source publishes, then
runs ``verify_certificate.py`` from the retained package over all 122,626,747 nodes and
requires its ``PYTHON_INTEGER_CERTIFICATE_VALID_4P468292`` marker. Needs only Python 3;
no Boost, no compiler. About 3.5 min.
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
PACKAGE = HERE / "mira-17squares" / "certificates" / "lower_bound_4p468292"
ARCHIVE = PACKAGE / "square17_lb_4p468292.cert.xz"
ARCHIVE_SHA256 = "a349b81e630ccf7292ae0afe6ed954591f7e88fe6289847f67883204a7ed60ac"
RAW_SHA256 = "2838f315302d67da131745925e9ec7dd2a602bb299d1335ce25e4e13a7b7b6d2"
MARKER = "PYTHON_INTEGER_CERTIFICATE_VALID_4P468292"


def main() -> int:
    packed = ARCHIVE.read_bytes()
    digest = hashlib.sha256(packed).hexdigest()
    if digest != ARCHIVE_SHA256:
        say(f"REFUSED: archive hashes to {digest}, expected {ARCHIVE_SHA256}")
        return 1
    raw = lzma.decompress(packed)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != RAW_SHA256:
        say(f"REFUSED: decompressed certificate hashes to {digest}, expected {RAW_SHA256}")
        return 1
    say(f"decompressed {len(raw)} bytes; both SHA-256 values match the source's")
    with tempfile.TemporaryDirectory() as scratch:
        certificate = Path(scratch) / "square17_lb_4p468292.cert"
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
    say("REPLAYED: Mira's certificate for s(17) > 4468292/1000000 is accepted by its checker")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
