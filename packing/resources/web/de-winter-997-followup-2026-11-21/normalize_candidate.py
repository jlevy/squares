"""Rebuild the reversible n90 reading copy from the original factual ZIP member.

Run from packing with the project interpreter. No producer program runs and no geometry
is decided here; the maintained parser checks the declared centre/half-angle format.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from strif import atomic_write_text

from devtools import evand_arrangement_reports as kernel
from devtools import retained_data
from devtools import upper_bound_reports as reports

PACKET = Path(__file__).resolve().parent


def main() -> None:
    record = json.loads((PACKET / "acquisition/sources.json").read_text())
    members = [row for row in record["members"] if row["path"] == "90/candidate.json.gz"]
    if len(members) != 1:
        raise ValueError("Candidate member is not unique in acquisition")
    member = members[0]
    source = PACKET / member["retained_at"]
    if source.is_symlink() or not source.resolve().is_relative_to(PACKET.resolve()):
        raise ValueError("Candidate is not a private file of this packet")
    raw = source.read_bytes()
    if (len(raw), hashlib.sha256(raw).hexdigest()) != (member["bytes"], member["sha256"]):
        raise ValueError("Original candidate differs from its acquisition digest")
    decoded = retained_data.gunzip_bytes(raw, limit=reports.MAX_SOURCE_BYTES)
    original = json.loads(decoded, object_pairs_hook=kernel.unique_object)
    if not isinstance(original, dict) or original.get("n") != 90:
        raise ValueError("Original candidate is not the declared 90-square object")
    metadata = {
        key: value for key, value in original.items() if key not in {"n", "side", "squares"}
    }
    derived = {
        "n": original["n"],
        "s_exact": original["side"],
        "squares": original["squares"],
        "provenance": metadata,
    }
    reverse = {
        "n": derived["n"],
        "side": derived["s_exact"],
        "squares": derived["squares"],
        **derived["provenance"],
    }
    restored = {key: reverse[key] for key in original}
    if restored != original or list(restored) != list(original):
        raise ValueError("Reading copy does not reverse to the parsed original")
    encoded = (json.dumps(derived, indent=2, ensure_ascii=False) + chr(10)).encode()
    binding = json.loads((PACKET / "acquisition/normalization.json").read_text())
    if hashlib.sha256(decoded).hexdigest() != binding["source_decoded_sha256"]:
        raise ValueError("Decoded original differs from normalization record")
    if hashlib.sha256(encoded).hexdigest() != binding["derived_sha256"]:
        raise ValueError("Reading copy differs from normalization record")
    certificate = reports.parse_certificate(encoded, 90, "pingyou-json")
    reports.admit(certificate, "9.994038766583")
    atomic_write_text(
        PACKET / "derived/candidate-reading-copy.json", encoded.decode(), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
