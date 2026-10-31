"""Is each regularizer view exactly its run's native certificate, converted?

Usage: python3.14 consistency.py INPUTS_DIR

Compares the side and, square by square in file order, the centre and the basis of
n{130,307}-view-solved.yaml with n{130,307}-solve-witness.cert, whose (cx, cy, t) rows
are converted with (cos, sin) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2)), exactly. Also
reports how many bases are not axis-aligned. Decides nothing about feasibility.
"""

from __future__ import annotations

import sys
from pathlib import Path

import qio


def main() -> None:
    inp = Path(sys.argv[1])
    for n in (130, 307):
        _, vside, vsq, head = qio.read_view(inp / f"n{n}-view-solved.yaml")
        _, cside, csq, ts = qio.read_tcert(inp / f"n{n}-solve-witness.cert")
        same = [k for k in range(len(vsq)) if vsq[k] == csq[k]]
        tilted = sum(1 for t in ts if t != 0)
        print(
            f"n={n}: view id {head.get('id')}; side equal: {vside == cside}; squares equal in order:"
            f" {len(same)}/{len(vsq)}; tilted squares (t != 0): {tilted}"
        )


if __name__ == "__main__":
    main()
