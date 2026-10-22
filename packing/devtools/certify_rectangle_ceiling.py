"""Certify, exactly, how far a rectangle-density certificate can reach for n = 1..100.

For each n this places n side-B cores at net orientations, from the repository's
known-best witness and from the ceil(sqrt n) grid, and decides their containment and
disjointness in exact rational arithmetic (sqpack.rectangle_ceiling). Each verified
placement at side L proves that no rectangle-density certificate at any side >= L has
mass below n. The receipt compares that proved ceiling with the B*UB(n) values Hosono's
pinned tools derive from their rounded upper-bound table (T-058).

From packing/:
    python -m devtools.certify_rectangle_ceiling            # write the receipts
    python -m devtools.certify_rectangle_ceiling --check    # recompute and compare
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import sys
import tarfile
from fractions import Fraction
from pathlib import Path

from strif import atomic_output_file

from sqpack.rectangle_ceiling import (
    ALPHA,
    CORE_SIDE,
    certificate_document,
    certificate_from_document,
    grid_certificate,
    place_cores,
    premise_checks,
    verify_ceiling,
)
from sqpack.rectangle_density import ANGLE_COUNT, ANGLE_STEP
from sqpack.witness import load_witness

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "resources/web/wand125-tools-2026-09-29"
SOURCE_ARCHIVE = PACKET / "upstream.tar.gz"
SOURCE_REVISION = "0d33ab61726c2ab03e3eb8f457dabaf22db8571f"
RECEIPT = PACKET / "receipts/ceiling-certificates-2026-10-02.json"
CERTIFICATES = PACKET / "receipts/ceiling-certificates-2026-10-02.json.gz"
N_RANGE = range(1, 101)


def source_table() -> dict[int, dict]:
    """The pinned source's upper-bound rows, read from the retained archive."""

    with tarfile.open(SOURCE_ARCHIVE) as archive:
        member = archive.extractfile("transfer/data/ub.json")
        if member is None:
            raise ValueError("retained archive has no transfer/data/ub.json")
        rows = json.loads(member.read(), parse_float=str)["rows"]
    return {row["n"]: row for row in rows if row.get("ub")}


def _on_grid(row: dict) -> bool:
    """The 3eb08e6 selection of B over ALPHA: an integer UB whose exact form is that integer."""

    ub = Fraction(row["ub"])
    return ub.denominator == 1 and row.get("ubExact") == str(ub.numerator)


def _floor_thousandths(value: float) -> str:
    # The source's own float computation of L_cap, reproduced as published.
    return str(math.floor(value * 1000 - 1e-6) / 1000)


def certify(n: int, row: dict | None) -> tuple[dict, dict]:
    witness_path = Path(f"witnesses/known-best/n-{n:03d}.yaml")
    witness = load_witness(ROOT / witness_path)
    witness = witness.get("witness", witness)
    placement = place_cores(witness)
    grid = grid_certificate(n)
    if not verify_ceiling(grid).verified:
        raise ValueError(f"grid certificate for n = {n} failed")
    candidates = [("grid", grid)]
    if placement is not None:
        candidates.insert(0, ("witness", placement.certificate))
    route, certificate = min(candidates, key=lambda item: item[1].side)
    report = verify_ceiling(certificate)
    if not report.verified:
        raise ValueError(f"n = {n}: {report.reasons}")
    result: dict[str, object] = {
        "n": n,
        "ceiling": str(certificate.side),
        "ceiling_decimal": f"{float(certificate.side):.12f}",
        "route": route,
        "witness": str(Path("packing") / witness_path),
        "witness_side": str(witness["side"]),
        "witness_placement": None
        if placement is None
        else {
            "side": str(placement.certificate.side),
            "net_aligned": placement.aligned,
            "worst_containment_factor": placement.worst_factor,
            "slack": str(placement.slack),
        },
        "grid_side": str(grid.side),
    }
    if row is not None:
        ub = Fraction(row["ub"])
        factor = CORE_SIDE if _on_grid(row) else ALPHA
        original, corrected = CORE_SIDE * ub, factor * ub
        result["source"] = {
            "ub": row["ub"],
            "ubExact": row.get("ubExact"),
            "B_times_ub": str(original),
            "l_cap_0d33ab6": _floor_thousandths(0.9977 * float(row["ub"])),
            "factor_3eb08e6": "B" if factor == CORE_SIDE else "ALPHA",
            "factor_times_ub": str(corrected),
            "l_cap_3eb08e6": _floor_thousandths(float(factor) * float(row["ub"])),
        }
        result["proves_B_times_ub"] = certificate.side <= original
        result["proves_factor_times_ub"] = certificate.side <= corrected
        # L_cap is the last thousandth a certificate is said to reach, so its operational
        # claim is impossibility from the next thousandth on.
        for version in ("0d33ab6", "3eb08e6"):
            reach = Fraction(result["source"][f"l_cap_{version}"])  # type: ignore[index]
            result[f"proves_above_l_cap_{version}"] = certificate.side <= reach + Fraction(
                1, 1000
            )
        result["excess_over_B_times_ub"] = f"{float(certificate.side - original):.3e}"
    return result, certificate_document(certificate)


def build() -> tuple[dict, dict]:
    table = source_table()
    rows, certificates = [], {}
    for n in N_RANGE:
        row, certificate = certify(n, table.get(n))
        rows.append(row)
        certificates[str(n)] = certificate
    premises = premise_checks()
    if not all(premises.values()):
        raise ValueError(f"a numeric premise failed: {premises}")
    sourced = [row for row in rows if "source" in row]
    receipt = {
        "generated_by": "packing/devtools/certify_rectangle_ceiling.py",
        "verifier": "packing/src/sqpack/rectangle_ceiling.py",
        "claim": "T-058",
        "net": {
            "B": str(CORE_SIDE),
            "D": str(ANGLE_STEP),
            "angle_count": ANGLE_COUNT,
            "alpha": str(ALPHA),
        },
        "premises": premises,
        "source_table": {
            "archive": "packing/resources/web/wand125-tools-2026-09-29/upstream.tar.gz",
            "revision": SOURCE_REVISION,
            "member": "transfer/data/ub.json",
        },
        "certificates": "packing/resources/web/wand125-tools-2026-09-29/receipts/"
        "ceiling-certificates-2026-10-02.json.gz",
        "summary": {
            "cases": len(rows),
            "verified": len(rows),
            "with_source_ub": len(sourced),
            "proves_B_times_ub": sum(bool(row["proves_B_times_ub"]) for row in sourced),
            "proves_factor_times_ub": sum(
                bool(row["proves_factor_times_ub"]) for row in sourced
            ),
            "proves_above_l_cap_0d33ab6": sum(
                bool(row["proves_above_l_cap_0d33ab6"]) for row in sourced
            ),
            "proves_above_l_cap_3eb08e6": sum(
                bool(row["proves_above_l_cap_3eb08e6"]) for row in sourced
            ),
            "net_aligned_routes": sum(
                row["route"] == "grid"
                or bool(row["witness_placement"] and row["witness_placement"]["net_aligned"])
                for row in rows
            ),
        },
        "rows": rows,
    }
    return receipt, certificates


def _replay(certificates: dict) -> None:
    for n, document in certificates.items():
        certificate = certificate_from_document(document)
        if certificate.n != int(n) or not verify_ceiling(certificate).verified:
            raise ValueError(f"retained ceiling certificate for n = {n} does not verify")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--check", action="store_true", help="recompute and compare")
    args = parser.parse_args(argv)
    receipt, certificates = build()
    receipt_text = json.dumps(receipt, indent=2) + "\n"
    certificate_bytes = gzip.compress(
        (json.dumps(certificates, separators=(",", ":")) + "\n").encode(), mtime=0
    )
    if args.check:
        retained = json.loads(gzip.decompress(CERTIFICATES.read_bytes()))
        _replay(retained)
        if RECEIPT.read_text() != receipt_text or retained != certificates:
            print("ceiling receipts differ from a fresh computation", file=sys.stderr)
            return 1
        print(f"ceiling receipts reproduce: {receipt['summary']}")
        return 0
    with atomic_output_file(RECEIPT) as temporary:
        Path(temporary).write_text(receipt_text)
    with atomic_output_file(CERTIFICATES) as temporary:
        Path(temporary).write_bytes(certificate_bytes)
    print(json.dumps(receipt["summary"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
