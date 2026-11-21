"""Replay issue 1040 using the maintained upper-bound geometry and controls.

Run from packing with the project interpreter. The attachment programs are outside
the tool's inputs. The retained copies keep the exact geometry of its two encodings.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

PACKET = Path(__file__).resolve().parent
COUNT = 259
OFFERED = "16.590016439230"
RECEIPT_FORMAT = "issue-1040-exact-replay-v1"
PROFILE = {
    "witness_prefix": "W-geiserx-1040-n",
    "claim_limitations": "Finite rational feasibility at the submitted side.",
}


def main() -> None:
    """Check custody, bind the encodings and retain both routes' control verdicts."""
    manifest = json.loads((PACKET / "acquisition/sources.json").read_text())
    for member in manifest["members"]:
        retained = (PACKET / member["retained_at"]).read_bytes()
        if (len(retained), hashlib.sha256(retained).hexdigest()) != (
            member["bytes"],
            member["sha256"],
        ):
            raise ValueError(f"Retained archive member differs: {member['path']}")

    original = PACKET / "source/upper/n259"
    derived = (PACKET / "derived/packing-reading-copy.json").read_bytes()
    centre_source = json.loads(reports.read_retained_bytes(original / "packing.json"))
    centre_source["side_decimal_info_only"] = centre_source.pop("side_decimal")
    if json.loads(derived) != centre_source:
        raise ValueError("The centre reading copy differs from the original geometry data")

    certificate = reports.parse_certificate(derived, COUNT, "ono-json", {})
    corners, corner_side = reports.legacy.independent.parse(original / "witness.yaml")
    reports.admit(certificate, OFFERED)
    if certificate.side != corner_side or [
        frozenset(square) for square in reports.legacy.corner_squares(certificate)
    ] != [frozenset(square) for square in corners]:
        raise ValueError("The two certificate encodings differ in exact geometry")

    jobs = [kernel.run_case(certificate, control, **PROFILE) for control in kernel.JOBS]
    record = {"format": RECEIPT_FORMAT, "routes": list(kernel.ROUTES), "cases": jobs}
    kernel.validate_receipt(
        record, {COUNT: certificate}, receipt_format=RECEIPT_FORMAT, **PROFILE
    )
    kernel.save_xz(PACKET / "receipts/exact-certification.json.xz", record)

    controls = sharp.control_rows(certificate, PROFILE)
    (PACKET / "receipts/sharp-controls.json").write_text(
        json.dumps({"n": COUNT, "controls": controls}, indent=2) + "\n"
    )
    if len(controls) != 11 or not all(control["as_expected"] for control in controls):
        raise ValueError("The two routes disagree with at least one sharp control expectation")


if __name__ == "__main__":
    main()
