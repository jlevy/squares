"""Rebuild the theorem inventory from the retained pieces by Lemma 3 and compare it.

    python3 -I -B glue_rebuild.py --source SRC --daniel CERTS --two-wedge TW --direct DC \\
        --headers HEADERS.json [--out DIR] [--only FILE ...]

``SRC`` is the theorem packet's ``source/`` (``theorem/inventory.tsv``, ``theorem/best.tsv``,
``rectangles/``, and the inventory certificates it retains), ``CERTS`` the directory of
Evan Daniel's ``n-N.cert`` pieces, ``TW`` the two-wedge packet's ``source/`` (``n0308``,
``n0343``, ``n0344``) and ``DC`` the direct-certificates packet's ``source/`` (``n0380`` to
``n0814``); ``HEADERS.json`` is the frozen header list with each inventory file's SHA-256.

For every row of the two tables the program reads the chain, glues it step by step with
its own implementation of Lemma 3's layout at the common squeeze d0 = 1/10000, closed,
scales the result once by 1 + d0/(2(n - d0)), writes the certificate text with the
comment line the retained files carry, and compares: the SHA-256 with the frozen list,
and, where the packet retains the file, the bytes. ``--out`` keeps the rebuilt files.

The layout is the one the README and the docstring of ``tools/glue.py`` state, written
again here from that description: with A a rectangle in an a x b box (a > b), B a square
in an m x m box or a rectangle in an a' x b' box, n = b + b', c = n - a' and the squeeze
d, the square [0, n - d]^2 holds A in [0, a - d] x [n - b, n - d] with its top at n - d,
the block D of (n - a) x b aligned unit squares in [a - d, n - d] x [n - d - b, n - d],
the block C of c x (n - b) in [0, c] x [0, n - b], and B in [c, n - d] x [0, n - d - b]
with its right side at n - d; the count is n^2 - waste_A - waste_B. A bare base is the
piece itself, unmoved, at the closed side n - d0. The program decides nothing about the
geometry; ``rectangle_check.py`` does that on its output.

Exit status 0 when every rebuilt certificate has its frozen digest. Written for the
review of 14 October 2026; see ../README.md.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from squares_exact import Certificate, certificate_text, parse_certificate

D0 = Fraction(1, 10000)
RECTANGLES = {
    "R": "r17x16_n0257",
    "R'": "r22x21_n0443",
    "r18x17": "r18x17_n0290",
    "r19x18": "r19x18_n0325",
    "r21x20": "r21x20_n0401",
    "r22x21w20": "r22x21_n0442",
}
TWO_WEDGE = ("n0308", "n0343", "n0344")


def say(line: str) -> None:
    sys.stdout.write(line + "\n")


class Pieces:
    """The piece certificates, read once each from the four packets."""

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.cache: dict[str, Certificate] = {}

    def path(self, name: str) -> Path:
        if name in RECTANGLES:
            folder = RECTANGLES[name]
            return self.args.source / "rectangles" / folder / f"{folder}.cert"
        if name.startswith("n-"):
            return self.args.daniel / f"{name}.cert"
        if name in TWO_WEDGE:
            return self.args.two_wedge / name / f"{name}.cert"
        if name.startswith("n0"):
            return self.args.direct / name / f"{name}.cert"
        raise ValueError(f"unknown piece {name}")

    def get(self, name: str) -> Certificate:
        if name not in self.cache:
            self.cache[name] = parse_certificate(self.path(name).read_text(encoding="utf-8"))
        return self.cache[name]


def block(
    x0: Fraction, y0: Fraction, cols: int, rows: int
) -> list[tuple[Fraction, Fraction, Fraction]]:
    half = Fraction(1, 2)
    return [
        (x0 + half + i, y0 + half + j, Fraction(0)) for i in range(cols) for j in range(rows)
    ]


def glue(a_cert: Certificate, b_cert: Certificate, d: Fraction) -> Certificate:
    """Lemma 3 at the squeeze ``d``, closed: the composite at side ``n - d``."""
    a, b = a_cert.box
    if a <= b:
        raise ValueError(f"the rectangle A needs a > b, got {a} x {b}")
    if b_cert.is_square:
        a2 = b2 = math.ceil(b_cert.width)
        d_b = a2 - b_cert.width
    else:
        a2, b2 = b_cert.box
        if not (b_cert.width > b_cert.height and a2 > b2):
            raise ValueError("a rectangle B needs W > H and a' > b'")
        d_b = min(a2 - b_cert.width, b2 - b_cert.height)
    d_a = min(a - a_cert.width, b - a_cert.height)
    if not 0 < d <= min(d_a, d_b, Fraction(1, 2)):
        raise ValueError(f"d = {d} is not in (0, min(d_A, d_B, 1/2)] = (0, {min(d_a, d_b)}]")
    n = b + b2
    c = n - a2
    if n < a or c < 0 or c > a - d:
        raise ValueError(f"the layout needs n >= a, 0 <= c <= a - d: n={n}, a={a}, c={c}")
    side = n - d
    squares = [(x, y + (side - a_cert.height), t) for x, y, t in a_cert.squares]
    squares += block(a - d, side - b, n - a, b)
    squares += block(Fraction(0), Fraction(0), c, n - b)
    squares += [(x + (side - b_cert.width), y, t) for x, y, t in b_cert.squares]
    waste_a, waste_b = a * b - a_cert.n, a2 * b2 - b_cert.n
    if len(squares) != n * n - waste_a - waste_b:
        raise ValueError("the count is not n^2 - waste_A - waste_B")
    return Certificate(len(squares), side, side, tuple(squares))


def strictify(cert: Certificate) -> Certificate:
    """Centres and side scaled by 1 + d0/(2(n - d0)): side n - d0/2, every margin open."""
    n = math.ceil(cert.width)
    if cert.width != n - D0:
        raise ValueError("strictify expects a closed composite at side n - d0")
    lam = 1 + D0 / (2 * (n - D0))
    return Certificate(
        cert.n,
        lam * cert.width,
        lam * cert.height,
        tuple((lam * x, lam * y, t) for x, y, t in cert.squares),
    )


def build_chain(chain: str, pieces: Pieces) -> Certificate:
    tokens = chain.split(" + ")
    base = tokens[0]
    if "+" in base:
        first, second = base.split("+")
        current = glue(pieces.get(first), pieces.get(second), D0)
    else:
        name, _, kept = base.partition("[")
        piece = pieces.get(name)
        if kept:
            count = int(kept.rstrip("]"))
            piece = Certificate(count, piece.width, piece.height, piece.squares[:count])
        if not piece.is_square:
            raise ValueError(f"a bare base must be square: {base}")
        m = math.ceil(piece.width)
        if piece.squeeze < D0:
            raise ValueError(f"{name} is squeezed less than d0")
        current = Certificate(piece.n, m - D0, m - D0, piece.squares)
    for token in tokens[1:]:
        current = glue(pieces.get(token), current, D0)
    return strictify(current)


def rows(theorem: Path) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    with (theorem / "inventory.tsv").open(encoding="utf-8") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            row["kind"] = "theorem"
            row["file"] = f"n{int(row['n']):03d}_F{int(row['F'])}.cert"
            out.append(row)
    with (theorem / "best.tsv").open(encoding="utf-8") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            if row["file"].startswith("best/"):
                row["kind"] = "best"
                out.append(row)
    return out


def comment(row: dict[str, str]) -> str:
    n, count = int(row["n"]), int(row["count"])
    if row["kind"] == "theorem":
        return (
            f"n={n}: {count} = {n}^2 - {n} + {row['F']} unit squares, theorem chain "
            f"{row['chain']} (p={row['p']}, q={row['q']}, base r={row['base_n']}), uniform "
            "squeeze d0=1/10000; tools/instantiate_theorem.py; strict, side n - d0/2"
        )
    return (
        f"n={n}: {count} = {n}^2 - {n} + {row['best_j']} unit squares, best chain "
        f"{row['chain']}, uniform squeeze d0=1/10000; tools/instantiate_theorem.py --best; "
        "strict, side n - d0/2"
    )


def first_difference(mine: str, theirs: str) -> str:
    for index, (line_a, line_b) in enumerate(
        zip(mine.splitlines(), theirs.splitlines(), strict=False)
    ):
        if line_a != line_b:
            return f"line {index + 1}: rebuilt {line_a[:60]!r}, retained {line_b[:60]!r}"
    return f"lengths {len(mine)} and {len(theirs)}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--daniel", type=Path, required=True)
    parser.add_argument("--two-wedge", type=Path, required=True)
    parser.add_argument("--direct", type=Path, required=True)
    parser.add_argument("--headers", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--only", nargs="*", default=None)
    args = parser.parse_args(argv)
    frozen = {
        row["file"]: row for row in json.loads(args.headers.read_text(encoding="utf-8"))["rows"]
    }
    pieces = Pieces(args)
    matched = retained_equal = table_digests = 0
    failures: list[str] = []
    table = rows(args.source / "theorem")
    for row in table:
        relative = f"theorem/{row['file']}"
        if args.only and row["file"] not in args.only and relative not in args.only:
            continue
        try:
            cert = build_chain(row["chain"], pieces)
        except ValueError as error:
            failures.append(f"{relative}: {error}")
            say(f"{relative}: REFUSED {error}")
            continue
        text = certificate_text(cert, comment(row))
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        expected = frozen[relative]["sha256"]
        n = int(row["n"])
        header_ok = cert.n == int(row["count"]) and cert.width == Fraction(20000 * n - 1, 20000)
        status = "digest MATCHES frozen list" if digest == expected else "digest DIFFERS"
        if digest == expected:
            matched += 1
        else:
            failures.append(f"{relative}: digest {digest[:16]} is not {expected[:16]}")
        # The table's own sha256 column must name the same file.
        if row["sha256"] == digest:
            table_digests += 1
        else:
            status += "; the table's sha256 column DIFFERS"
        retained = args.source / relative
        if retained.is_file():
            theirs = retained.read_text(encoding="utf-8")
            if theirs == text:
                retained_equal += 1
                status += "; bytes EQUAL the retained file"
            else:
                status += f"; retained file DIFFERS at {first_difference(text, theirs)}"
        say(
            f"{relative}: chain {row['chain']}: {cert.n} squares at side {cert.width}"
            f"{'' if header_ok else ' (NOT the row)'}; {status}"
        )
        if args.out is not None:
            target = args.out / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
    say(
        f"{matched} of {len(table)} rebuilt certificates have the digest the frozen list "
        f"records; {retained_equal} equal a retained file byte for byte; {table_digests} "
        "have the digest their table row states"
    )
    say("GLUE_REBUILD_HOLDS" if not failures else "GLUE_REBUILD_FAILS")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
