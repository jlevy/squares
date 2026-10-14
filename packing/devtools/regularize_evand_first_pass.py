#!/usr/bin/env python3
"""Run Evan Daniel's exact solve without its active-set recursion, for the driver.

`devtools.regularize_evand` runs this file on the retry ladder's `first-pass` rung, as
`python -I regularize_evand_first_pass.py --exact DIR INPUT --out DIR -q [...]`, where an
earlier attempt failed in an active-set step or ran out of time. It imports nothing from
this project: under `-I` neither the checkout nor this file's directory is on `sys.path`,
and the only directory it adds is `--exact`, the replica's `search/exact` or a patched
copy of it, so the solver it runs is the replica's copy of the vendored `exactsolve.py`.

Its command line is upstream's own (`exactsolve.py`'s `__main__`) with `--exact` added,
and it does what upstream's `__main__` does, with one difference: upstream's `run` is
called with `depth` at upstream's own limit of four active-set steps. `run` re-solves with
the pairs that closed during the solve as equations only while `depth < 4`, so the first
pass's outputs (`witness.json`, `witness.exact.txt`, `witness.contacts.json`,
`witness.cert`) are what the solve leaves, whatever its certificate check found. Nothing
else changes: no forced pairs, and the same precision, dilation and contact tolerance.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

#: Upstream's limit on active-set steps: `run` recurses only while `depth` is below it.
ACTIVE_SET_LIMIT = 4


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    command.add_argument("--exact", type=Path, required=True, help="the solver's directory")
    command.add_argument("input")
    command.add_argument("--dps", type=int, default=80)
    command.add_argument("--eps", default="1e-20")
    command.add_argument("--out")
    command.add_argument("--algdeg", type=int, default=0)
    command.add_argument("--tol", type=float, default=0)
    command.add_argument("-q", action="store_true")
    command.add_argument("--force-kkt", action="store_true")
    return command


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    sys.path.insert(0, str(arguments.exact))
    solver: Any = importlib.import_module("exactsolve")
    solver.FORCE_KKT = arguments.force_kkt
    solver.run(
        arguments.input,
        arguments.dps,
        arguments.eps,
        arguments.out,
        arguments.algdeg,
        arguments.tol,
        arguments.q,
        (),
        ACTIVE_SET_LIMIT,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
