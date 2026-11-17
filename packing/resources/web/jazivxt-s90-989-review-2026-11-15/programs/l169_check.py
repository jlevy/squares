"""Lane L169 check: decide a `.cert` certificate by both methods and write the receipt.

Usage: l169_check.py CERT EXPECTED_SHA256 OUT_JSON
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves it off

import l169_clip as clipm
import l169_decide as dec
import l169_reader as rd


def decimal_floor(f: Fraction, places: int) -> str:
    q = f.numerator * 10**places // f.denominator
    s = str(q).rjust(places + 1, "0")
    return f"{s[:-places]}.{s[-places:]}"


def main(argv: list[str]) -> int:
    path, expected, out_path = argv[1], argv[2], argv[3]
    t0 = time.process_time()
    raw = open(path, "rb").read()
    digest = hashlib.sha256(raw).hexdigest()
    reading = rd.read_text(raw)
    res = dec.decide(reading)
    side = Fraction(*reading["side"])
    upright = sum(1 for _, _, t in reading["squares"] if t[0] == 0)
    receipt = {
        "program": "l169_check.py",
        "certificate": path.rsplit("/", 1)[-1],
        "sha256": digest,
        "sha256_expected": expected,
        "sha256_matches": digest == expected,
        "bytes": len(raw),
        "line_terminator": "CRLF" if reading["terminator"] == "\r\n" else "LF",
        "scalars_read": 2 + 3 * reading["n"],
        "side_digits": [len(str(abs(side.numerator))), len(str(side.denominator))],
        "side_40_places_floor": decimal_floor(side, 40),
        "squares_upright_t_zero": upright,
        "decision": dec.public(res),
        "python": sys.version.split()[0],
        "gmp": clipm.gmp_version(),
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    verdict = res["verdict"] if digest == expected else "REFUSE (digest)"
    receipt["verdict"] = verdict
    with open(out_path, "w") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=False)
        fh.write("\n")
    d = res
    print(
        f"{verdict}: n={d['n']} pairs={d['pairs_decided']} "
        f"A={d['pairs_class_counts_A']} B={d['pairs_class_counts_B']} "
        f"least={d['least_margin']} contacts={len(d['wall_contacts'])} "
        f"touching_pairs={len(d['touching_pairs'])} cpu={receipt['cpu_seconds']}s"
    )
    return 0 if verdict == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
