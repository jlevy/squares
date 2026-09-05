"""The standalone verifier decides the retained bytes, and refuses everything else.

`cases/n11_fractional_certificate/minimal_verify.py` is a second decision on
`certificate.json`: no numpy, no `sqpack`, nothing imported from this repository, and
its own SHA-256 pin on the bytes it will speak for. These tests run it the way a reader
does -- as a script, in a subprocess, on a path -- so what is asserted is the program's
printed verdict and its exit status, not the return value of an internal function.

Two refusals are worth separating, because they are different guarantees. A copy with
one weight lightened is still a well-formed certificate; it is refused because the atom
set is no longer D4-invariant, which is Condition 1. A copy with one byte changed is
refused before anything is parsed at all, because the digest is not the pinned one. The
first says the conditions are decided; the second says they are decided about *these*
bytes.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

PACKING = Path(__file__).resolve().parents[1]
CASE = PACKING / "cases" / "n11_fractional_certificate"
VERIFIER = CASE / "minimal_verify.py"
CERTIFICATE = CASE / "certificate.json"


def run(*arguments: str | Path) -> subprocess.CompletedProcess[str]:
    """Run the verifier as its own usage line says to: a script, given a path."""

    return subprocess.run(
        [sys.executable, str(VERIFIER), *(str(argument) for argument in arguments)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_the_pinned_digest_is_the_retained_certificates_own_and_is_written_once() -> None:
    """One statement of the hash, in one file, and it is the artifact's."""

    source = VERIFIER.read_text(encoding="utf-8")
    digest = hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest()
    pinned = re.findall(r'PINNED_SHA256 = "([0-9a-f]{64})"', source)

    assert pinned == [digest]
    assert source.count(digest) == 1


def test_a_single_lightened_weight_is_refused_by_condition_1(tmp_path: Path) -> None:
    """Halving one atom's weight leaves a well-formed file whose atoms are not D4."""

    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    x, y, weight = record["atoms"][0]
    record["atoms"][0] = [x, y, str(Fraction(weight) / 2)]
    lightened = tmp_path / "lightened.json"
    lightened.write_text(json.dumps(record), encoding="utf-8")

    result = run(lightened, "--unpinned")

    assert result.returncode == 1
    assert "REFUSED" in result.stdout
    assert "D4 image" in result.stdout
    assert "VERIFIED" not in result.stdout


def test_one_changed_byte_is_refused_by_the_pin(tmp_path: Path) -> None:
    """The digest is checked before the JSON is parsed, so nothing else is reached."""

    raw = CERTIFICATE.read_bytes()
    changed = raw.replace(b'"7/4000"', b'"7/4001"', 1)
    assert changed != raw
    assert len(changed) == len(raw)
    edited = tmp_path / "one-byte.json"
    edited.write_bytes(changed)

    result = run(edited)

    assert result.returncode == 1
    assert result.stdout.startswith("REFUSED  SHA-256")
    assert hashlib.sha256(changed).hexdigest() in result.stdout
    assert "Condition" not in result.stdout


def test_an_absent_certificate_is_refused_rather_than_crashing(tmp_path: Path) -> None:
    result = run(tmp_path / "not-here.json")

    assert result.returncode == 1
    assert "REFUSED" in result.stdout


@pytest.mark.exhaustive_exact
def test_the_retained_bytes_are_verified_on_the_full_net() -> None:
    """The whole decision, end to end.

    Measured 2026-09-05: 49.4 s for this node, of which 47.5 s is the verifier itself
    on CPython 3.14 and 47.3 s on the system's CPython 3.11. The marker registry in
    `test_module_boundaries.py` carries why that price belongs in this tier.
    """

    result = run(CERTIFICATE)

    assert result.returncode == 0, result.stdout
    assert "VERIFIED  s(11) >= 381/100" in result.stdout
    assert "Condition 1  PASS  1121 atoms" in result.stdout
    assert "Condition 2  PASS  total mass 434547/40000" in result.stdout
    assert "Condition 5  PASS  least covered mass 4001/4000" in result.stdout
    assert "of 181, over" in result.stdout
