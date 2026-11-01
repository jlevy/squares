#!/usr/bin/env python3
"""The checker's written-out certificates against this review's own construction
(stage 4 review of the filled-end lemma, PR #870).

This program runs code it did not write: `devtools.filled_end_checker`, the object under
review, only to obtain the certificate text it writes for a row (`certificate_text`).
Everything it then does is its own: it holds the text's SHA-256 to the lane's decisions
receipt (read as data), parses the text with its own reader (header ``n S``, then n rows
``x y t``, every literal matched whole), turns each pose into four exact corners with its
own formula (centre plus the half-diagonals turned counter-clockwise by phi,
cos phi = (1 - t^2)/(1 + t^2), sin phi = 2t/(1 + t^2)), and compares the certificate's
squares, as a multiset of corner sets, with `fe_independent`'s construction less its
first ``surplus`` grid squares. Equal multisets mean the certificate is the packing
`fe_independent` verified. At the five edge rows it also decides the certificate's own
corners with `fe_independent`'s geometry, and at every row it negates the tilt of every
square written with t < 0 (the H band, reflected) and decides that too, which must be
refused.

    python -I fe_crosscheck.py PACKING_DIR OUT.json N...
"""

from __future__ import annotations

import gzip
import hashlib
import json
import platform
import re
import sys
import time
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fe_independent as fe  # noqa: E402

_LITERAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?")


def parse_certificate(text: str) -> tuple[int, Q, list[tuple[Q, Q, Q]]]:
    lines = text.split("\n")
    if lines[-1] != "":
        raise ValueError("no final newline")
    lines = lines[:-1]
    head = lines[0].split(" ")
    if len(head) != 2 or not head[0].isdigit() or _LITERAL.fullmatch(head[1]) is None:
        raise ValueError("bad header")
    n, side = int(head[0]), Q(head[1])
    poses = []
    for line in lines[1:]:
        fields = line.split(" ")
        if len(fields) != 3 or any(_LITERAL.fullmatch(f) is None for f in fields):
            raise ValueError(f"bad pose {line[:60]!r}")
        poses.append(tuple(Q(f) for f in fields))
    if len(poses) != n:
        raise ValueError(f"{len(poses)} poses for n = {n}")
    return n, side, poses


def corners(x: Q, y: Q, t: Q) -> list[tuple[Q, Q]]:
    c, s = fe.trig(t)
    half = Q(1, 2)
    return [(x + c * a - s * b, y + s * a + c * b) for a, b in ((half, half), (-half, half), (-half, -half), (half, -half))]


def main() -> int:
    packing = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2])
    counts = [int(a) for a in sys.argv[3:]]
    sys.path.insert(0, str(packing))
    from devtools import filled_end_checker as checker  # noqa: PLC0415

    packet = checker.PACKET
    receipt = json.loads(gzip.decompress((packet / "receipts" / "filled-end-decisions-v2.json.gz").read_bytes()))
    pinned = {item["n"]: item for item in receipt["rows"]}
    theirs = {row.n: row for row in checker.records(checker.V2)}
    text, _ = fe.deposit_text(packet, "2")
    mine = {row["n"]: row for row in fe.read_rows(text)}
    started = time.process_time()
    results = []
    for n in counts:
        row = mine[n]
        cert_text = checker.certificate_text(theirs[n])
        digest = hashlib.sha256(cert_text.encode("utf-8")).hexdigest()
        cn, cside, poses = parse_certificate(cert_text)
        side, polys, _, _ = fe.construction(row)
        surplus = len(polys) - n
        grid_seen = 0
        kept = []
        for label, pts in polys:
            if label == "grid" and grid_seen < surplus:
                grid_seen += 1
                continue
            kept.append(frozenset(pts))
        written = [corners(x, y, t) for x, y, t in poses]
        same = Counter(frozenset(pts) for pts in written) == Counter(kept)
        result = {
            "n": n,
            "certificate_sha256": digest,
            "sha256_is_the_receipt_s": digest == pinned[n]["certificate_sha256"],
            "bytes_are_the_receipt_s": len(cert_text.encode("utf-8")) == pinned[n]["certificate_bytes"],
            "header_n_and_side_are_the_row_s": cn == n and cside == row["S"],
            "squares_are_this_review_s_construction": same,
            "negative_tilts": sum(1 for _, _, t in poses if t < 0),
            "negative_tilts_are_the_h_band_s": all(t == -row["tH"] for _, _, t in poses if t < 0)
            and sum(1 for _, _, t in poses if t < 0) == sum(1 for label, _ in polys if label == "H row"),
        }
        if n in fe.EDGE_ROWS:
            verdict = fe.Verdict([("certificate", pts) for pts in written], cside)
            result["certificate_geometry"] = verdict.summary()
        flipped = [corners(x, y, -t if t < 0 else t) for x, y, t in poses]
        verdict = fe.Verdict([("flipped", pts) for pts in flipped], cside)
        result["h_tilt_sign_flipped"] = {
            "refused": not verdict.passed,
            "overlapping_pairs": len(verdict.overlaps),
            "wall_crossings": len(verdict.wall_crossings),
        }
        results.append(result)
        print(json.dumps({k: result[k] for k in ("n", "sha256_is_the_receipt_s", "squares_are_this_review_s_construction")} | {"flip_refused": result["h_tilt_sign_flipped"]["refused"]}), flush=True)
    found = {
        "program": "fe_crosscheck.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "uses_sha256": hashlib.sha256(Path(fe.__file__).read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(checker.__file__).read_bytes()).hexdigest(),
        "environment": {"python": platform.python_version(), "machine": platform.machine()},
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cpu_seconds": round(time.process_time() - started, 1),
        "all_hold": all(
            r["sha256_is_the_receipt_s"]
            and r["bytes_are_the_receipt_s"]
            and r["header_n_and_side_are_the_row_s"]
            and r["squares_are_this_review_s_construction"]
            and r["negative_tilts_are_the_h_band_s"]
            and r["h_tilt_sign_flipped"]["refused"]
            and r.get("certificate_geometry", {"passed": True})["passed"]
            for r in results
        ),
        "results": results,
    }
    fe.write_json_lines(out, found, "results")
    return 0 if found["all_hold"] else 1


if __name__ == "__main__":
    sys.exit(main())
