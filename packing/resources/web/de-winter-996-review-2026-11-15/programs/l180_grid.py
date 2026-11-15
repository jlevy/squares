"""Lane L180, after the freeze: write the 10 x 10 grid less its top row as a binary64 text.

Written for the blind stage 4 review of issue #996. It decides nothing. It writes the
packing the record held at 90 before T-303, nine full rows of ten upright squares in
[0, 10] x [0, 9] inside the box of side 10, in the ``binary64-xyd`` form that
``devtools.measure_identity`` reads: ``n side``, then ``x y degrees`` per square.

Usage: l180_grid.py OUT
"""

from __future__ import annotations

import sys


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    rows = [f"{i + 0.5} {j + 0.5} 0" for j in range(9) for i in range(10)]
    with open(argv[1], "w", encoding="ascii") as fh:
        fh.write("# the grid at 90: nine rows of ten upright unit squares in [0, 10] x [0, 9]\n")
        fh.write("90 10\n")
        fh.write("\n".join(rows) + "\n")
    print(f"wrote {len(rows)} squares")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
