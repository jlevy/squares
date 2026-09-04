"""Replay the retained n = 20 certificate and report every condition.

Exits non-zero if any condition fails, so the replay is a gate and not a
report. Run as ``python -m cases.n20_fractional_certificate``.
"""

from __future__ import annotations

import sys
from pathlib import Path

from cases.n20_fractional_certificate.replay import CERTIFICATE_PATH, declared, load
from sqpack.fractional.certificate import least_size_certified, verify


def replay(path: Path) -> int:
    certificate = load(path)
    verdict = verify(certificate)
    record = declared(path)
    print(f"claim: {record['claim']}")
    print(f"  n = {certificate.n}, L = {certificate.outer_side}, B = {certificate.square_side}")
    print(f"  {len(certificate.atoms)} atoms, total mass {certificate.total_mass}")
    for condition in verdict.conditions:
        mark = "PASS" if condition.holds else "FAIL"
        print(f"  {mark}  {condition.name} | {condition.detail}")
    if not verdict.accepted:
        print(f"REFUSED: {', '.join(verdict.failures)}")
        return 1
    if str(certificate.total_mass) != record["total_mass"]:
        print("REFUSED: the retained total mass disagrees with the replay")
        return 1
    least = least_size_certified(certificate.total_mass)
    print(f"VERIFIED: s(m) >= {certificate.bounded_side} for every m >= {least}")
    return 0


def main() -> int:
    """The retained certificate must replay."""
    return replay(CERTIFICATE_PATH)


if __name__ == "__main__":
    sys.exit(main())
