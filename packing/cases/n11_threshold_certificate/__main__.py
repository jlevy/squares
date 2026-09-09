"""Replay the retained threshold certificate through the two-route retention gate.

Exits non-zero if either route refuses it, if the two routes disagree on the least cell
charge, or if the bytes are not the ones the record was registered against, so the replay
is a gate and not a report. Run as ``python -m cases.n11_threshold_certificate``.

    uv run --frozen --all-extras --group dev python -m cases.n11_threshold_certificate
    uv run --frozen --all-extras --group dev python -m cases.n11_threshold_certificate --quick

The default runs both routes, which is the only mode that can retain and takes about
ninety seconds on three workers. ``--quick`` runs the interval route alone: enough to
reject a candidate, never enough to retain one, and the gate says so in its own output.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from cases.n11_threshold_certificate.replay import (
    CERTIFICATE_PATH,
    FROZEN_SHA256,
    declared,
    digest,
)
from devtools.decide_threshold_certificate import Mode, decide


def replay(path: Path, *, workers: int, mode: Mode) -> int:
    found = digest(path)
    if found != FROZEN_SHA256:
        print(f"REFUSED: {path} has sha256 {found}, not the registered {FROZEN_SHA256}")
        return 1
    for key, value in sorted(declared(path).items()):
        print(f"declared {key}: {value}")
    return 0 if decide(path, workers=workers, mode=mode) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quick", action="store_true", help="interval route only; cannot retain"
    )
    parser.add_argument("--workers", type=int, default=int(os.environ.get("PACK_JOBS", "1")))
    args = parser.parse_args(argv)
    mode: Mode = "quick" if args.quick else "both"
    return replay(CERTIFICATE_PATH, workers=max(1, args.workers), mode=mode)


if __name__ == "__main__":
    raise SystemExit(main())
