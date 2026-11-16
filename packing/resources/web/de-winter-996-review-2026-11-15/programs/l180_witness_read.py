"""Lane L180, after the freeze: the twin through this repository's own witness readers.

Written for the blind stage 4 review of issue #996. It decides nothing about the bound.
It runs, read-only, ``sqpack.witness.validate_witness_document`` (the schema and its
semantic checks) and the ``witness-corners`` adapter of
``devtools.upper_bound_reports`` on the twin as published, and on a copy changed in
exactly the three ways the adapter's rules name (the schema by its file name, integer
ids, each listing started at the corner the adapter writes first), and compares the
poses the adapter recovers from that copy with the JSON file's.

Run from ``packing/`` with ``python -B`` (not ``-I``), so that ``devtools`` and
``sqpack`` import from this checkout.

Usage: l180_witness_read.py JSON TWIN SCRATCH_COPY OUT
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as F
from typing import Any

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, os.getcwd())  # packing/, for devtools and sqpack

import l180_reader as R  # noqa: E402
from devtools import upper_bound_reports as U  # noqa: E402
from sqpack.witness import validate_witness_document  # noqa: E402


def try_adapter(raw: bytes, n: int) -> dict[str, Any]:
    try:
        cert = U.witness_corners(raw, n, {})
    except U.ReportError as exc:
        return {"accepted": False, "refusal": str(exc)}
    return {"accepted": True, "certificate": cert}


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(__doc__)
        return 2
    jpath, tpath, copy_path, out = argv[1:]
    r = R.read_json(jpath)
    with open(tpath, "rb") as fh:
        raw = fh.read()
    doc = yaml.safe_load(raw.decode("utf-8"))
    res: dict[str, Any] = {"program": "l180_witness_read.py", "lane": "L180"}
    try:
        validate_witness_document(doc, path=U.WITNESS_SCHEMA, fallback_schema=U.WITNESS_SCHEMA)
        res["validate_witness_document"] = {"accepted": True}
    except Exception as exc:  # the validator's refusal, whatever its class
        res["validate_witness_document"] = {"accepted": False, "refusal": f"{type(exc).__name__}: {exc}"}
    first = try_adapter(raw, r.n)
    res["witness_corners_as_published"] = {k: v for k, v in first.items() if k != "certificate"}
    w = doc["witness"]
    tw = R.read_twin(tpath)
    listings = R.compare_twin(r, tw)["listings"]
    res["departures"] = {
        "softschema_schema": doc["softschema"]["schema"],
        "adapter_schemas": sorted(U.CORNER_SCHEMAS),
        "id_form": sorted({type(s["id"]).__name__ for s in w["squares"]}),
        "listing_from_json_pose": listings,
        "adapter_corner_order": [list(p) for p in U.CORNER_ORDER],
    }
    # The copy: the three changes and nothing else. The twin lists (+u+v), (-u+v),
    # (-u-v), (+u-v); the adapter writes (-u-v) first, so each listing is turned by two.
    doc2 = json.loads(json.dumps(doc))
    doc2["softschema"]["schema"] = U.CORNER_SCHEMA
    for k, sq in enumerate(doc2["witness"]["squares"], start=1):
        sq["id"] = k
        cs = sq["corners"]
        sq["corners"] = cs[2:] + cs[:2]
    text = yaml.safe_dump(doc2, sort_keys=False, width=10**6)
    with open(copy_path, "w", encoding="ascii") as fh:
        fh.write(text)
    second = try_adapter(text.encode("ascii"), r.n)
    entry = {k: v for k, v in second.items() if k != "certificate"}
    if second["accepted"]:
        cert = second["certificate"]
        side = F(cert.side)
        squares = list(cert.poses)
        same = side == r.side and len(squares) == r.n
        bad = []
        for k, (sq, p) in enumerate(zip(squares, r.poses, strict=True), start=1):
            x, y, t = F(sq.x), F(sq.y), F(sq.t)
            c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
            if (x, y) != (p.x, p.y) or {(c, s), (-s, c), (-c, -s), (s, -c)}.isdisjoint({(p.c, p.s)}):
                bad.append(k)
        entry["poses_equal_json"] = same and not bad
        entry["poses_differing"] = bad[:10]
    res["witness_corners_on_the_changed_copy"] = entry
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(json.dumps({k: v for k, v in res.items() if k not in ("program", "lane")})[:1500])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
