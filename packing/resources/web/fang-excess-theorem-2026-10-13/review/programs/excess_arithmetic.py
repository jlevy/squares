"""The arithmetic of Theorem 2: F(n), the decomposition, the counts and the deficiency.

    python3 -I -B excess_arithmetic.py THEOREM_DIR [--to N]

``THEOREM_DIR`` is the source's ``theorem/`` directory (``inventory.tsv``, ``best.tsv``,
``PIECES.md``), read as data. From the README's definition alone the program:

1. recomputes F(n) = 1 + max{p + 2q : 16p + 21q <= n - 15} and its maximiser (ties to the
   larger q) for n = 15..N, and checks that the maximiser's base r = n - 16p - 21q lies in
   15..30, which is why sixteen base packings suffice for Theorem 2's extreme case;
2. checks that every n >= 15 admits (p, q) = (floor((n - 15)/16), 0) with base in 15..30,
   which is Theorem 1's induction in steps of 16;
3. holds every row of ``inventory.tsv`` to (F, p, q, r, count = n^2 - n + F(n), side
   (20000n - 1)/20000) and every row of ``best.tsv`` to count = n^2 - n + j with j >= F(n);
4. recounts each row's chain from the pieces' counts and boxes in ``PIECES.md``: a base of
   count m^2 - m + j in an m x m box, a rectangle a x b of waste w adding b - w to the
   excess and b to the side, so that the composite's count is n^2 - n + j';
5. prints the deficiency comparison for k = 15..72 (Arslanov, Mustafin and
   Shangitbayev's k - 1; Ryu's 8 ceil(sqrt(k - 4)) - 1; Theorem 1's k - 2; Theorem 2's
   k - 1 - F(k); the inventory's k - 1 - j) and where Theorem 2 and Ryu's bound cross,
   searched to N.

Exit status 0 when every check holds. Written for the review of 14 October 2026.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import sys
from fractions import Fraction
from pathlib import Path


def say(line: str) -> None:
    sys.stdout.write(line + "\n")


def maximiser(n: int) -> tuple[int, int]:
    """``(p, q)`` maximising ``p + 2q`` under ``16p + 21q <= n - 15``, ties to larger q."""
    best: tuple[int, int, int] | None = None
    for q in range((n - 15) // 21 + 1):
        p = (n - 15 - 21 * q) // 16
        key = (p + 2 * q, q, p)
        if best is None or key[:2] > best[:2]:
            best = key
    assert best is not None
    return best[2], best[1]


def excess(n: int) -> int:
    p, q = maximiser(n)
    return 1 + p + 2 * q


def ceil_sqrt(value: int) -> int:
    root = math.isqrt(value)
    return root if root * root == value else root + 1


def ryu(k: int) -> int:
    return 8 * ceil_sqrt(k - 4) - 1


def read_pieces(path: Path) -> dict[str, tuple[int, int, int]]:
    """Each piece's ``(count, a, b)`` from the table of PIECES.md, read as data."""
    pieces: dict[str, tuple[int, int, int]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not cells[2].isdigit():
            continue
        # PIECES.md writes the box with the multiplication sign U+00D7, as in `17 x 16`.
        box = re.fullmatch(r"(\d+)\s*[x" + chr(0xD7) + r"]\s*(\d+)", cells[3])
        if box is None:
            continue
        pieces[cells[0]] = (int(cells[2]), int(box.group(1)), int(box.group(2)))
    return pieces


def chain_count(chain: str, pieces: dict[str, tuple[int, int, int]]) -> tuple[int, int]:
    """``(count, side)`` of a chain such as ``n0308[307] + R' + R`` or ``R'+R' + R'``."""
    tokens = chain.split(" + ")
    base = tokens[0]
    if base.endswith("'+R'") or base == "R'+R'":
        first, second = base.split("+")
        count_a, a, b = pieces[first]
        count_b, a2, b2 = pieces[second]
        side = b + b2
        count = side * side - (a * b - count_a) - (a2 * b2 - count_b)
    else:
        name, _, kept = base.partition("[")
        count, a, b = pieces[name]
        if kept:
            count = int(kept.rstrip("]"))
        if a != b:
            raise ValueError(f"a base piece must be square: {base}")
        side = a
    for token in tokens[1:]:
        count_r, a, b = pieces[token]
        if a <= b:
            raise ValueError(f"a rectangle piece needs a > b: {token}")
        waste = a * b - count_r
        # Lemma 3 with a square B of side m: n = b + m, c = n - m = b <= a - d, and
        # the count is n^2 - waste_A - waste_B.
        new_side = side + b
        count = new_side * new_side - waste - (side * side - count)
        side = new_side
    return count, side


def check_rows(theorem: Path) -> tuple[list[str], dict[int, int]]:
    problems: list[str] = []
    best: dict[int, int] = {}
    pieces = read_pieces(theorem / "PIECES.md")
    with (theorem / "inventory.tsv").open(encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in rows:
        n = int(row["n"])
        p, q = maximiser(n)
        f = 1 + p + 2 * q
        r = n - 16 * p - 21 * q
        stated = (int(row["F"]), int(row["p"]), int(row["q"]), int(row["base_n"]))
        if stated != (f, p, q, r):
            problems.append(f"inventory n={n}: (F, p, q, r) {stated} != {(f, p, q, r)}")
        count = n * n - n + f
        if int(row["count"]) != count:
            problems.append(f"inventory n={n}: count {row['count']} != {count}")
        if Fraction(row["side"]) != Fraction(20000 * n - 1, 20000):
            problems.append(f"inventory n={n}: side {row['side']}")
        chained, side = chain_count(row["chain"], pieces)
        if (chained, side) != (count, n):
            problems.append(f"inventory n={n}: chain {row['chain']} gives {chained} at {side}")
        best[n] = f
    if [int(row["n"]) for row in rows] != list(range(15, 65)):
        problems.append("inventory rows are not n = 15..64")
    with (theorem / "best.tsv").open(encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in rows:
        n, j = int(row["n"]), int(row["best_j"])
        if int(row["count"]) != n * n - n + j or j < excess(n) or int(row["F"]) != excess(n):
            problems.append(f"best n={n}: count {row['count']}, j {j}, F {row['F']}")
        chained, side = chain_count(row["chain"], pieces)
        if (chained, side) != (n * n - n + j, n):
            problems.append(f"best n={n}: chain {row['chain']} gives {chained} at {side}")
        best[n] = max(best[n], j)
    return problems, best


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    parser.add_argument("theorem", type=Path, help="the source's theorem/ directory")
    parser.add_argument("--to", type=int, default=2000)
    args = parser.parse_args(argv)
    problems: list[str] = []

    # 1 and 2: every n >= 15 decomposes, with the maximiser's base in 15..30.
    for n in range(15, args.to + 1):
        p, q = maximiser(n)
        r = n - 16 * p - 21 * q
        if not 15 <= r <= 30:
            problems.append(f"n={n}: the maximiser ({p}, {q}) leaves base r = {r}")
        if excess(n) < 1 or excess(n) < excess(n - 1 if n > 15 else 15):
            problems.append(f"n={n}: F(n) = {excess(n)} is below 1 or decreasing")
        p1 = (n - 15) // 16
        if not 15 <= n - 16 * p1 <= 30:
            problems.append(f"n={n}: Theorem 1's step of 16 leaves base {n - 16 * p1}")
    say(
        f"n = 15..{args.to}: the maximiser's base r lies in 15..30 and F(n) >= 1 is "
        f"non-decreasing at every n; (floor((n - 15)/16), 0) leaves a base in 15..30"
    )
    say("F(n) for n = 15..64: " + " ".join(f"{n}:{excess(n)}" for n in range(15, 65)))

    # 3 and 4: the tables.
    row_problems, best = check_rows(args.theorem)
    problems.extend(row_problems)
    say(
        "inventory.tsv and best.tsv: every row's (F, p, q, r), count, side and chain "
        + ("recount" if not row_problems else "FAIL")
    )

    # 5: the deficiency.
    say("k  AMS  Ryu  Thm1  Thm2  inventory")
    for k in range(15, 73):
        inventory = k - 1 - best[k] if k in best else None
        say(f"{k}  {k - 1}  {ryu(k)}  {k - 2}  {k - 1 - excess(k)}  {inventory}")
    below = [k for k in range(15, args.to + 1) if k - 1 - excess(k) < ryu(k)]
    tied = [k for k in range(15, args.to + 1) if k - 1 - excess(k) == ryu(k)]
    above = [k for k in range(15, args.to + 1) if k - 1 - excess(k) > ryu(k)]
    say(f"Theorem 2 below Ryu at {len(below)} values of k in 15..{args.to}: {runs(below)}")
    say(f"tied at {runs(tied)}; Ryu below Theorem 2 at {runs(above)}")
    theorem_one_below_ams = all(k - 2 < k - 1 for k in range(15, args.to + 1))
    say(f"Theorem 1 (k - 2) below AMS (k - 1) at every k >= 15: {theorem_one_below_ams}")

    for problem in problems:
        say("PROBLEM " + problem)
    say("EXCESS_ARITHMETIC_HOLDS" if not problems else "EXCESS_ARITHMETIC_FAILS")
    return 0 if not problems else 1


def runs(values: list[int]) -> str:
    out: list[list[int]] = []
    for value in values:
        if out and out[-1][1] == value - 1:
            out[-1][1] = value
        else:
            out.append([value, value])
    return ", ".join(f"{a}" if a == b else f"{a}-{b}" for a, b in out) or "none"


if __name__ == "__main__":
    sys.exit(main())
