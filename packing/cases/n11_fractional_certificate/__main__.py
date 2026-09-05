"""Replay all three retained n = 11 certificates and report every condition.

Exits non-zero if any condition fails, so the replay is a gate and not a
report. Run as ``python -m cases.n11_fractional_certificate``.
"""

from __future__ import annotations

from pathlib import Path

from cases.n11_fractional_certificate.replay import (
    CERTIFICATE_PATH,
    FIRST_RUNG_PATH,
    STROMQUIST_RUNG_PATH,
    declared,
    load,
)
from sqpack.fractional.certificate import verify


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
    expected_claim = f"s({certificate.n}) >= {certificate.bounded_side}"
    if record["claim"] != expected_claim:
        print("REFUSED: the retained claim disagrees with the replay")
        return 1
    if str(certificate.total_mass) != record["total_mass"]:
        print("REFUSED: the retained total mass disagrees with the replay")
        return 1
    if str(verdict.minimum_cell_mass) != record["least_cell_mass"]:
        print("REFUSED: the retained least cell mass disagrees with the replay")
        return 1
    print(f"VERIFIED: {expected_claim}")
    return 0


def main() -> int:
    """Every retained rung must replay; the weaker rungs are not optional."""
    return max(
        replay(FIRST_RUNG_PATH),
        replay(STROMQUIST_RUNG_PATH),
        replay(CERTIFICATE_PATH),
    )


if __name__ == "__main__":
    raise SystemExit(main())
