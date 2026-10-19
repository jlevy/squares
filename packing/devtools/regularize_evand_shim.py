#!/usr/bin/env python3
"""Run Evan Daniel's regularizer on one count inside a scratch replica, for the driver.

`devtools.regularize_evand` runs this file as `python -I regularize_evand_shim.py
--replica DIR --n N ...`, from a working directory outside the checkout. It imports
nothing from this project: under `-I` neither the checkout nor this file's directory is on
`sys.path`, and the only directory it adds is the replica's `search/regularize`, so the
modules it runs are the replica's copies of the vendored `reg.py` and `atlas.py` at the
pin. Those copies read `search/exact/batch/results.json` and
`search/exact/batch/work/n-N/witness.{exact.txt,json}` relative to themselves, which the
driver writes into the replica before this runs.

The call sequence is upstream's own, from `atlas.compute_one`, with the orientation and
the angle policy passed explicitly instead of taken from upstream's defaults:

1. `reg.regularize(n, style, angle_policy, orient, log)`: the angle merges, the
   orientation, the symmetry search, the coincide placement, the 80-digit refinement and
   the 80-digit verification, returning the oriented source `P`, the result `R` and the
   run's report.
2. `atlas.level_of(reg, reg.load(n), atlas.d4inv(reg, R, g), rep, policy)`: upstream's
   level, 0 to 3, of the result mapped back to the source frame. It is upstream's
   classification and decides nothing here.
3. `reg.write_cert(R, path)`: the dilated rational certificate, scaled by `1 + 10^-20`
   about the origin corner and checked in process by upstream's `verify_cert.verify`.

It writes one JSON document: upstream's report fields under the names the driver's
`regularize.json` uses, the result and the solved source at 50 significant digits in the
source frame (`mpmath.nstr`, fixed notation), and every square whose angle the run
changed, by index from 0, with its angle before and after. An exception is written into
the same document as `error` and the exit status is 1, so the driver records the failure
instead of reading a traceback.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import time
import traceback
from pathlib import Path
from typing import Any

#: Significant digits of every pose and side the document carries.
DIGITS = 50


def text(mpmath: Any, value: Any, digits: int = DIGITS) -> str:
    """`value` at `digits` significant digits in fixed notation, as the driver reads it."""
    return str(mpmath.nstr(value, digits, min_fixed=-mpmath.inf, max_fixed=mpmath.inf))


def packing(mpmath: Any, frame: dict[str, Any]) -> dict[str, Any]:
    """A configuration as `{S, sq: [[x, y, degrees], ...]}`, upstream's `compute_one` shape."""
    return {
        "S": text(mpmath, frame["S"]),
        "sq": [
            [text(mpmath, x), text(mpmath, y), text(mpmath, t)]
            for x, y, t in zip(frame["X"], frame["Y"], frame["T"], strict=True)
        ],
    }


def regularize(arguments: argparse.Namespace) -> dict[str, Any]:
    sys.path.insert(0, str(arguments.replica / "search" / "regularize"))
    reg: Any = importlib.import_module("reg")
    atlas: Any = importlib.import_module("atlas")
    mpmath: Any = importlib.import_module("mpmath")
    started = time.perf_counter()
    lines: list[str] = []

    def log(*parts: object) -> None:
        lines.append(" ".join(str(part) for part in parts))

    _oriented, result, rep = reg.regularize(
        arguments.n,
        style=arguments.style,
        angle_policy=arguments.variant,
        orient=arguments.orient,
        log=log,
    )
    source = reg.load(arguments.n)
    in_source_frame = atlas.d4inv(reg, result, rep["g"])
    level, level_text = atlas.level_of(
        reg, reg.load(arguments.n), in_source_frame, rep, arguments.variant
    )
    cert_ok, certified_side = reg.write_cert(result, str(arguments.certificate))
    changed = [
        {
            "square": index,
            "from": text(mpmath, before),
            "to": text(mpmath, after),
        }
        for index, (before, after) in enumerate(
            zip(source["T"], in_source_frame["T"], strict=True)
        )
        if abs(reg.fold(after - before)) > reg.EQ_TOL
    ]
    return {
        "n": arguments.n,
        "variant": arguments.variant,
        "style": arguments.style,
        "orient": arguments.orient,
        "level": level,
        "level_text": level_text,
        "S_exact": text(mpmath, result["S"], 60),
        "S_cert": str(certified_side),
        "cert_ok": bool(cert_ok),
        "g": rep["g"],
        "status": rep.get("status"),
        "free": rep.get("free"),
        "moved": rep.get("moved"),
        "max_move": rep.get("max_move"),
        "symmetry": rep.get("sym_imposed"),
        "rigid_symmetry": rep.get("rigid_sym"),
        "symmetry_dropped": rep.get("sym_dropped"),
        "symmetry_dropped_for_coincidence": rep.get("sym_dropped_for_coincidence"),
        "groups_before": rep.get("groups_before"),
        "groups_after": rep.get("groups_after"),
        "merged": rep.get("merged"),
        "angle_changes": rep.get("merged_determined"),
        "changed_angles": changed,
        "shape": (rep.get("shape") or {}).get("kind"),
        "orient_tie": rep.get("orient_tie"),
        "orient_topright": rep.get("orient_topright"),
        "orient_source": rep.get("orient_source"),
        "coincident": rep.get("coincident"),
        "face_spread": rep.get("face_spread"),
        "refine": rep.get("refine"),
        "verify": rep.get("verify"),
        "place": rep.get("place"),
        "contacts_before": rep.get("contacts_before"),
        "packing": packing(mpmath, in_source_frame),
        "source": packing(mpmath, source),
        "log": lines,
        "seconds": round(time.perf_counter() - started, 3),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run Evan Daniel's regularizer on one count inside a scratch replica."
    )
    parser.add_argument("--replica", type=Path, required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--variant", choices=("conservative", "fewest"), default="conservative")
    parser.add_argument("--style", default="coincide")
    parser.add_argument("--orient", default="0")
    arguments = parser.parse_args(argv)
    try:
        document = regularize(arguments)
        status = 0
    except Exception as error:  # noqa: BLE001 -- the driver records any upstream failure
        document = {
            "n": arguments.n,
            "error": f"{type(error).__name__}: {error}",
            "traceback": traceback.format_exc(),
        }
        status = 1
    arguments.output.write_text(
        json.dumps(document, indent=1, default=str) + "\n", encoding="utf-8"
    )
    return status


if __name__ == "__main__":
    raise SystemExit(main())
