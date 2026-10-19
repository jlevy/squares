#!/usr/bin/env python3
"""Run this repository's third exact route on PR #622's certificate, unchanged.

Not this review's own decision. The deciding code is ``devtools.check_half_angle_area``
(``V-check-half-angle-area``), the half-angle area route, imported as it stands: its own
readers, its decision and its six controls (`verdict`). This driver only feeds it. The
review lane otherwise runs only code it writes; the coordinator of think-30n2 asked for
this run on 16 October 2026, so that the record can say whether a third exact route
decided the certificate. The route has no roster for #622 (`decide-imports` has no key
for it), so the driver calls the functions `decide-imports` calls for a release-asset
certificate, and changes none of them.

It reads the release asset by member name and extracts nothing:

- the certificate, by the route's PingYou reader (`read_pingyou_json`);
- the replay's derived fact, ``facts/n-029.yaml.gz``, by the route's fact reader
  (`read_fact`), which is the witness the register entry cites;
- the source's corners witness, by the route's corners reader (`read_witness_corners`).

It holds the three to one packing (the fact's poses and the certificate's equal, and the
corners witness the same squares as point sets), then runs `verdict` on the fact. Run it
from the repository with the project interpreter, isolated:
``uv run --frozen --all-extras --group dev --project packing python -I third_route.py
ASSET``.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
import time
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve()
PACKET = HERE.parents[2]
PACKING = HERE.parents[5]
sys.path.insert(0, str(PACKING))

from devtools import check_half_angle_area as route  # noqa: E402

ASSET_BYTES = 430075
ASSET_SHA256 = "0dc9bcd1cf5f2806a4d2e0c4c1c07e4903d91bbea611b8b938bda770b9782537"
CERT_MEMBER = "n29-certificate/certificates/n029.cert.json"
CERT_SHA256 = "a01428c51875679fbe78c11a803742b8d99f44b916a660ab6801bb0fcf76951b"
NATIVE_MEMBER = "n29-certificate/native/pingyou-20261015-n29-rational.yaml"
NATIVE_SHA256 = "0eff5b4d2a9701e30fe8912fd634c5a7124384366197533c18a5bcc26dfe4a39"
N = 29


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def member(asset: zipfile.ZipFile, name: str, digest: str) -> bytes:
    data = asset.read(name)
    if sha256(data) != digest:
        raise SystemExit(f"{name}: SHA-256 {sha256(data)}, not {digest}")
    return data


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        sys.stderr.write("usage: third_route.py ASSET\n")
        return 2
    path = Path(argv[1])
    data = path.read_bytes()
    if len(data) != ASSET_BYTES or sha256(data) != ASSET_SHA256:
        sys.stderr.write(f"{path}: not the pinned asset\n")
        return 2
    asset = zipfile.ZipFile(path)
    side_c, poses = route.read_pingyou_json(member(asset, CERT_MEMBER, CERT_SHA256), N)
    from_cert = tuple(route.placed(poses))
    fact = PACKET / "facts/n-029.yaml.gz"
    side_f, from_fact = route.read_fact(gzip.decompress(fact.read_bytes()).decode(), N)
    side_w, from_corners = route.read_witness_corners(
        member(asset, NATIVE_MEMBER, NATIVE_SHA256), N
    )
    same_squares = all(
        sorted(route.corners(*a)) == sorted(route.corners(*b))
        for a, b in zip(from_corners, from_fact, strict=True)
    )
    cpu, wall = time.process_time(), time.monotonic()
    found = route.verdict(side_f, from_fact)
    cpu, wall = time.process_time() - cpu, time.monotonic() - wall
    out = {
        "route": "devtools.check_half_angle_area (V-check-half-angle-area), unchanged",
        "route_sha256": sha256(Path(route.__file__).read_bytes()),
        "driver": "this file, which only reads and hands over",
        "read": {
            "certificate (read_pingyou_json)": CERT_MEMBER,
            "fact (read_fact)": "facts/n-029.yaml.gz",
            "corners witness (read_witness_corners)": NATIVE_MEMBER,
        },
        "fact equals the certificate, side and every pose": side_f == side_c
        and from_fact == from_cert,
        "corners witness: same side and the same 29 squares": side_w == side_f and same_squares,
        "verdict": {k: v for k, v in found.items() if k not in {"side", "wall_seconds"}},
        "cpu_s": round(cpu, 1),
        "wall_s": round(wall, 1),
    }
    least = out["verdict"].get("least_distance_squared")
    if isinstance(least, str) and len(least) > 80:
        out["verdict"]["least_distance_squared"] = f"{least[:40]}... ({len(least)} characters)"
    sys.stdout.write(json.dumps(out, indent=2) + "\n")
    return 0 if found["passed"] and all(found["controls"].values()) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
