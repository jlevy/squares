"""Decide one certificate: its digest, its reading, both methods, and the claim's arithmetic.

Usage: python -I -B r1038_check.py CERTIFICATE STATED_SHA256 CLAIM_DECIMAL OUT_JSON

The claim is the decimal the report prints for s(n). The receipt records whether the
file's SHA-256 equals the stated one, the reader's verdict, both methods' verdict and the
facts behind it, and how the claim stands to the exact side: the side's 12-place ceiling
and floor, and the claim less the side. It prints the verdict line.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from decimal import Decimal
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1038_decide as decide  # noqa: E402
import r1038_reader as reader  # noqa: E402


def ceiling_at(value: Fraction, places: int) -> Fraction:
    scale = 10**places
    return Fraction(-((-value.numerator * scale) // value.denominator), scale)


def floor_at(value: Fraction, places: int) -> Fraction:
    scale = 10**places
    return Fraction((value.numerator * scale) // value.denominator, scale)


def main(argv: list[str]) -> int:
    path, stated, claim_text, out_path = argv[1:5]
    started = time.process_time()
    with open(path, "rb") as handle:
        data = handle.read()
    digest = hashlib.sha256(data).hexdigest()
    receipt: dict[str, object] = {
        "program": "r1038_check.py",
        "certificate": os.path.basename(path),
        "sha256": digest,
        "stated_sha256": stated,
        "sha256_equal": digest == stated,
        "bytes": len(data),
    }
    try:
        cert = reader.read_text(data.decode("utf-8"))
    except (reader.ReadRefused, UnicodeDecodeError) as error:
        receipt["reading"] = f"REFUSED: {error}"
        receipt["verdict"] = "REFUSE"
        with open(out_path, "w", encoding="utf-8") as handle:
            json.dump(receipt, handle, indent=1)
        print("REFUSE (reading)", error)
        return 1
    receipt["reading"] = "read"
    receipt["header"] = cert.header
    receipt["scalars"] = 1 + 4 * cert.n
    receipt["noncanonical_scalars"] = cert.noncanonical
    result = decide.decide(cert.side, cert.centers, cert.bases)
    receipt["decision"] = decide.summary(result)
    claim = Fraction(Decimal(claim_text))
    side = cert.side
    ceiling = ceiling_at(side, 12)
    floor = floor_at(side, 12)
    receipt["claim"] = {
        "claim": claim_text,
        "side": str(side),
        "side_40_places": decide.fixed(side, 40),
        "ceiling_12": decide.fixed(ceiling, 12),
        "floor_12": decide.fixed(floor, 12),
        "claim_is_ceiling_12": claim == ceiling,
        "claim_at_least_side": claim >= side,
        "claim_less_side": str(claim - side),
        "claim_less_side_decimal": decide.decimal(claim - side),
        "side_less_floor_decimal": decide.decimal(side - floor),
    }
    verdict = "ACCEPT" if result.verdict == "ACCEPT" and digest == stated else "REFUSE"
    receipt["verdict"] = verdict
    receipt["cpu_seconds"] = round(time.process_time() - started, 2)
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(receipt, handle, indent=1)
    print(verdict, cert.n, "squares,", len(result.margins), "pairs, side", decide.fixed(side, 30))
    return 0 if verdict == "ACCEPT" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
