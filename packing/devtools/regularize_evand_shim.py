#!/usr/bin/env python3
"""Run Evan Daniel's regularizer on one count inside a replica tree.

`devtools.regularize_evand regularize` copies this file into
`<run dir>/replica/search/regularize/` beside the replica's copy of the vendored `reg.py`
and `atlas.py`, and runs it there with `python -I`, once per count. It exists because
`atlas.py compute` does not expose `reg.regularize`'s `orient` argument, and the project's
policy is the source orientation (`orient = 0`); the vendored tree is never patched.

It imports only the replica's modules and the standard library, never this project's
code, so what it runs is the vendored generator at its pin. It does what
`atlas.compute_one` does for one count -- `reg.regularize`, `atlas.level_of` on the
result mapped back to the source frame, `reg.write_cert` -- and writes the certificate
and the same JSON fields as `compute_one`'s poster record, plus the run's full report and
its timings, into `--out`:

    python -I regularize_evand_shim.py --n 26 --policy conservative --style coincide \
        --orient 0 --out DIR

`--orient` is a container symmetry `0..7` or `best` (upstream's refit). Nothing here
decides anything: the project's driver reads the certificate back and decides it.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
POLICIES = ("free", "conservative", "fewest")
STYLES = ("gravity", "pretty", "coincide")
NOTE = (
    "regularized display view of a certified packing, made by the vendored generator; "
    "the certificate is the generator's dilated copy, decided by the project, not here"
)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--n", type=int, required=True)
    command.add_argument("--policy", choices=POLICIES, default="conservative")
    command.add_argument("--style", choices=STYLES, default="coincide")
    command.add_argument("--orient", default="0", help="0..7, or best for upstream's refit")
    command.add_argument("--out", type=Path, required=True)
    return command


def _log(*parts: object) -> None:
    print(*parts, flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.orient != "best" and args.orient not in {str(g) for g in range(8)}:
        raise SystemExit(f"--orient must be 0..7 or best, not {args.orient!r}")
    sys.path.insert(0, str(HERE))
    reg = importlib.import_module("reg")
    atlas = importlib.import_module("atlas")
    mpm = importlib.import_module("mpmath")
    n: int = args.n
    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)
    seconds: dict[str, float] = {}

    wall, cpu = time.perf_counter(), time.process_time()
    _start, result, report = reg.regularize(
        n, style=args.style, angle_policy=args.policy, orient=args.orient, log=_log
    )
    seconds["regularize_wall"] = time.perf_counter() - wall
    seconds["regularize_cpu"] = time.process_time() - cpu

    wall, cpu = time.perf_counter(), time.process_time()
    level, level_text = atlas.level_of(
        reg, reg.load(n), atlas.d4inv(reg, result, report["g"]), report, args.policy
    )
    seconds["level_wall"] = time.perf_counter() - wall
    seconds["level_cpu"] = time.process_time() - cpu

    wall, cpu = time.perf_counter(), time.process_time()
    certificate = out / f"n-{n:03d}.cert"
    cert_ok, side = reg.write_cert(result, str(certificate))
    seconds["certificate_wall"] = time.perf_counter() - wall
    seconds["certificate_cpu"] = time.process_time() - cpu

    def high(packing: dict[str, Any]) -> dict[str, Any]:
        return {
            "S": mpm.nstr(packing["S"], 50),
            "sq": [
                [mpm.nstr(x, 50), mpm.nstr(y, 50), mpm.nstr(t, 50)]
                for x, y, t in zip(packing["X"], packing["Y"], packing["T"], strict=True)
            ],
        }

    record = {
        "n": n,
        "S_exact": mpm.nstr(result["S"], 60),
        "S_cert": str(side),
        "cert_valid": bool(cert_ok),
        "verify_80": report["verify"],
        "input": reg.refreshed(n) or "search/exact/batch",
        "by": report["by"],
        "orientation_g": report["g"],
        "orient_argument": args.orient,
        "symmetry": report.get("sym_imposed"),
        "shape": report.get("shape", {}).get("kind"),
        "groups_before": report["groups_before"],
        "groups_after": report["groups_after"],
        "angle_changes": report.get("merged_determined"),
        "free_merges": report.get("merged"),
        "packing": high(result),
        "policy": args.policy,
        "style": args.style,
        "level": level,
        "level_text": level_text,
        "seconds": {key: round(value, 3) for key, value in seconds.items()},
        "report": report,
        "note": NOTE,
    }
    text = json.dumps(record, default=str, indent=1)
    (out / f"n-{n:03d}.json").write_text(text + "\n", encoding="utf-8")
    _log(f"n = {n}: level {level}, certificate {'VALID' if cert_ok else 'INVALID'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
