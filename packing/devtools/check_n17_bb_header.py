"""Bounded BB header preflight; never read a tree or issue a FULL receipt."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import math
import re
import tempfile
import time
import zlib
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

from devtools import verify_n17_bb_certificate as full
from sqpack import retained_json

SCHEMA = "n17-bb-header-verification/v1"
COMPRESSED_LIMIT, DECODED_LIMIT, OUTPUT_LIMIT = 1 << 20, 10 << 20, 1 << 20
RATIONAL_BITS = 4096
ID = re.compile(r"[0-9a-f]{64}\Z")
RATIONAL = re.compile(r"-?[0-9]+/[0-9]+\Z", re.ASCII)


class IncompleteError(Exception):
    """The predeclared resource boundary was reached."""


def require(ok: Any, message: str) -> None:
    if not ok:
        raise ValueError(message)


def tick(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise IncompleteError("header wall ceiling")


def rational(value: Any) -> None:
    require(type(value) is str and bool(RATIONAL.fullmatch(value)), "rational text required")
    if len(value) > 2470:
        raise IncompleteError("header rational character ceiling")
    q = Fraction(value)
    if max(abs(q.numerator).bit_length(), q.denominator.bit_length()) > RATIONAL_BITS:
        raise IncompleteError("header rational bit ceiling")


def structure(data: Any) -> None:
    """Bound only fields the standing header checker actually consumes."""
    require(type(data) is dict and type(data.get("header")) is dict, "manifest header required")
    data = cast(dict[str, Any], data)
    h = cast(dict[str, Any], data["header"])
    pattern = h["pattern"]
    require(
        type(pattern) is list
        and 1 <= len(pattern) <= 24
        and all(type(name) is str for name in pattern)
        and len(set(pattern)) == len(pattern),
        "unique bounded pattern required",
    )
    k = len(pattern)
    rational(h["cap"])
    require(type(h["cells"]) is list and len(h["cells"]) == k, "cell roster differs")
    for polygon in h["cells"]:
        require(type(polygon) is list and 3 <= len(polygon) <= 32, "bounded cell polygon")
        for point in cast(list[Any], polygon):
            require(type(point) is list and len(point) == 2, "cell point shape")
            for value in cast(list[Any], point):
                rational(value)
    for key, width in (("root_angles", 2), ("root_boxes", 4)):
        require(type(h[key]) is list and len(h[key]) == k, f"{key} roster differs")
        for row in h[key]:
            require(type(row) is list and len(row) == width, f"{key} row shape")
            for value in row:
                rational(value)
    require(type(h["pairs"]) is list, "pair roster required")
    require(
        all(
            type(pair) is list and len(pair) == 2 and all(type(i) is int for i in pair)
            for pair in h["pairs"]
        ),
        "typed pair roster required",
    )
    multiples = h["half_pi_multiples"]
    require(type(multiples) is dict and len(multiples) <= 64, "bounded pi roster")
    for key, row in multiples.items():
        require(type(key) is str and bool(re.fullmatch(r"-?[0-9]{1,4}", key)), "pi multiplier")
        require(type(row) is list and len(row) == 2, "pi enclosure shape")
        for value in cast(list[Any], row):
            rational(value)
    settings = h.get("settings", {})
    require(type(settings) is dict, "settings mapping required")
    require(type(settings.get("taylor", False)) is bool, "typed Taylor setting required")
    if settings.get("taylor", False):
        rational(settings["taylor_k"])


def check_original_enclosure(verifier: full.Verifier, cells: full.Cells) -> None:
    """Every declared inward halfplane contains the complete original source cell."""
    for name, polygon in zip(
        verifier.manifest["header"]["pattern"], verifier.cells, strict=True
    ):
        require(len(set(polygon)) == len(polygon), "duplicate declared cell vertex")
        source = cells.polygons[name]
        for index, start in enumerate(polygon):
            end = polygon[(index + 1) % len(polygon)]
            require(start != end, "zero declared cell edge")
            require(
                all(full.cross(start, end, point) >= 0 for point in source),
                f"declared edge does not enclose original cell {name}",
            )


def check(
    manifest: Path,
    expected_sha256: str,
    manifest_id: str,
    deadline: float,
    *,
    cells: full.Cells | None = None,
) -> dict[str, Any]:
    require(
        bool(ID.fullmatch(expected_sha256)) and bool(ID.fullmatch(manifest_id)),
        "SHA identity required",
    )
    tick(deadline)
    with manifest.open("rb") as stream:
        raw = stream.read(COMPRESSED_LIMIT + 1)
    if len(raw) > COMPRESSED_LIMIT:
        raise IncompleteError("compressed manifest ceiling")
    require(hashlib.sha256(raw).hexdigest() == expected_sha256, "manifest bytes differ")
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
        decoded = stream.read(DECODED_LIMIT + 1)
    if len(decoded) > DECODED_LIMIT:
        raise IncompleteError("decoded manifest ceiling")
    data = json.loads(decoded)
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    require(hashlib.sha256(canonical).hexdigest() == manifest_id, "canonical manifest differs")
    structure(data)
    tick(deadline)
    require(full.constants_hold(), "standing Machin constants failed")
    selected_cells = full.cover_cells() if cells is None else cells
    # The standing constructor receives one bounded immutable object; no tree/trig files.
    with tempfile.TemporaryDirectory(prefix="n17-bb-header-") as temporary:
        directory = Path(temporary)
        _ = (directory / f"{manifest_id}.json.gz").write_bytes(raw)
        verifier = full.Verifier(directory, manifest_id)
        verifier.check_header(selected_cells)
        require(not verifier.failures, "; ".join(verifier.failures[:50]))
        check_original_enclosure(verifier, selected_cells)
    tick(deadline)
    with manifest.open("rb") as stream:
        after = stream.read(COMPRESSED_LIMIT + 1)
    require(after == raw, "manifest changed during header check")
    require(not verifier.failures, "; ".join(verifier.failures[:50]))
    require(verifier.counts == {"header": 1}, "unexpected standing work")
    tick(deadline)
    return {
        "schema": SCHEMA,
        "mode": "HEADER_ONLY",
        "status": "HEADER_ONLY_PASS",
        "header_checks_passed": True,
        "full_verification_passed": False,
        "tree_verification_performed": False,
        "trig_verification_performed": False,
        "ordinary_exclusion_admitted": False,
        "census_admission": False,
        "global_bound_changed": False,
        "manifest": str(manifest),
        "compressed_sha256": expected_sha256,
        "manifest_id": manifest_id,
        "pattern": data["header"]["pattern"],
        "cells_source": selected_cells.source,
        "counts": verifier.counts,
        "complete_original_cell_halfplane_enclosure_checked": True,
        "limits": {
            "compressed_bytes": COMPRESSED_LIMIT,
            "decoded_bytes": DECODED_LIMIT,
            "output_bytes": OUTPUT_LIMIT,
            "used_rational_bits": RATIONAL_BITS,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--compressed-sha256", required=True)
    parser.add_argument("--manifest-id", required=True)
    parser.add_argument("--max-seconds", type=float, default=30)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or not 0 < args.max_seconds <= 60:
        parser.error("max-seconds must be finite and in (0,60]")
    deadline = time.monotonic() + args.max_seconds
    try:
        receipt = check(args.manifest, args.compressed_sha256, args.manifest_id, deadline)
        encoded = encode(receipt)
        tick(deadline)
        rc = 0
    except (
        IncompleteError,
        ValueError,
        OSError,
        EOFError,
        zlib.error,
        KeyError,
        TypeError,
        ArithmeticError,
    ) as exc:
        receipt = {
            "schema": SCHEMA,
            "mode": "HEADER_ONLY",
            "status": "INCOMPLETE" if isinstance(exc, IncompleteError) else "HEADER_REFUSED",
            "error": str(exc)[:2048],
            "header_checks_passed": False,
            "full_verification_passed": False,
            "tree_verification_performed": False,
            "trig_verification_performed": False,
            "ordinary_exclusion_admitted": False,
            "census_admission": False,
            "global_bound_changed": False,
            "complete_original_cell_halfplane_enclosure_checked": False,
        }
        encoded = retained_json.dumps(receipt).encode()
        rc = 1
    with args.output.open("xb") as stream:
        _ = stream.write(encoded)
    return rc


def encode(receipt: dict[str, Any]) -> bytes:
    raw = retained_json.dumps(receipt).encode()
    if len(raw) > OUTPUT_LIMIT:
        raise IncompleteError("header output ceiling")
    return raw


if __name__ == "__main__":
    raise SystemExit(main())
