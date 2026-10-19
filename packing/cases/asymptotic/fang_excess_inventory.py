"""Check Kevin Fang's theorem inventory and set its F(n) against the deficiency record.

Kevin Fang's README at ``078789a`` (retained in
``packing/resources/web/fang-excess-theorem-2026-10-13/``) states Theorem 1,
s(n^2 - n + 1) < n for every n >= 15, and Theorem 2, s(n^2 - n + F(n)) < n with
F(n) = 1 + max{p + 2q : 16p + 21q <= n - 15}. Its ``theorem/`` directory instantiates
them for n = 15..64 at side n - 1/20000.

Written from that statement and the retained tables, and sharing no code with the
source, this module decides three things exactly, without reading any geometry beyond
certificate headers:

- **The inventory's arithmetic.** F(n) is recomputed from its definition; every row of
  ``theorem/inventory.tsv`` must name the maximiser the README's tie-break picks, a base
  r = n - 16p - 21q in 15..30 and the count n^2 - n + F(n); every row of ``best.tsv`` and
  ``composites/table.csv`` must have the count n^2 - n + j it states; and the header of
  each of the 76 inventory certificates must state that count and the side
  (20000n - 1)/20000. The packet retains six of them, the ones the exact sample replays;
  the other 70 are pinned by digest, so every header is read from the frozen list
  ``acquisition/inventory-headers.json``, which must name exactly the certificates the
  tables name, and each retained file must state its row's header.
  ``--freeze-headers CHECKOUT`` writes the list from a checkout at the pin, holding each
  file's bytes to the SHA-256 the packet's manifest pinned at acquisition: the one
  boundary a digest crosses here (OR-16), allowlisted as an external checkout. Each row
  keeps that digest for the release that later retains the file.
- **The rectangles' headers.** Each of the six rectangle certificates states its count,
  width and height exactly; its waste ab - count and squeeze min(a - W, b - H) are
  recomputed, R's and R''s squeezes are held to the README's 7.436e-4 and 0.0094, and the
  uniform squeeze 1/10000 to every piece header this packet retains. Whether the squares
  lie in the rectangle is not decided here.
- **The deficiency comparison.** For each k from 15 to 72 it sets the bounds on
  c*(k) = max{c : s(k^2 - c) = k} side by side: Arslanov, Mustafin and Shangitbayev's
  k - 1; Ryu's 8 ceil(sqrt(k - 4)) - 1 (``deficiency_upper_bounds``); Theorems 1 and 2,
  k - 2 and k - 1 - F(k); the inventory's best excess j, k - 1 - j; and the record's own
  finite rows, k^2 - m - 1 for the largest count m <= k^2 whose recorded upper bound is
  below k. It also finds where Theorem 2 and Ryu's bound cross.

The record's rows are read once, when the receipt is written, and frozen in it with the
commit they were read at, so ``--check`` rebuilds the receipt from the packet and those
frozen values alone.

Run from ``packing/``::

    uv run --frozen --all-extras --group dev python -m \\
        cases.asymptotic.fang_excess_inventory --write | --check | --print
    uv run --frozen --all-extras --group dev python -m \\
        cases.asymptotic.fang_excess_inventory --freeze-headers CHECKOUT
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import check_source_coverage as coverage
from devtools.retained_data import read_retained_bytes
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/fang-excess-theorem-2026-10-13"
SOURCE = PACKET / "source"
RECEIPT = PACKET / "receipts/inventory-and-deficiency.json"
FORMAT = "fang-excess-inventory-v1"
HEADERS = PACKET / "acquisition/inventory-headers.json"
HEADERS_FORMAT = "fang-inventory-headers-v1"
MANIFEST = PACKET / "acquisition/upstream-subtree.sha256"
REVISION = "078789a4cfd36f915f1bfbe76d742413d79b2965"
#: The largest inventory certificate is about 0.42 MB.
MAX_CERTIFICATE_BYTES = 1_000_000
#: The uniform squeeze of the inventory, and its side n - D0/2.
D0 = Fraction(1, 10000)
FIRST, LAST = 15, 64
#: The deficiency table's range, and how far the crossover with Ryu's bound is searched.
TABLE = range(15, 73)
CROSSOVER_LIMIT = 2000
HORIZON = 324
#: The squeezes the README states for R and R' (Proposition 4 and the 2026-10-13 entry).
STATED_SQUEEZE = {"r17x16_n0257": Fraction(7436, 10**7), "r22x21_n0443": Fraction(94, 10**4)}
#: Pieces of PIECES.md that another packet on ``main`` retains, by their retained path.
DANIEL_TWINS = "resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact"
TWO_WEDGE = "resources/web/fang-two-wedge-certificates-2026-10-10/source"
OTHER_PIECES = {
    "n-211": f"{DANIEL_TWINS}/batch/certs/n-211.cert",
    "n0308": f"{TWO_WEDGE}/n0308/n0308.cert",
    "n0343": f"{TWO_WEDGE}/n0343/n0343.cert",
    "n0344": f"{TWO_WEDGE}/n0344/n0344.cert",
}
DANIEL_PIECES = ("n-110", "n-132", "n-156", "n-182", "n-210", "n-241", "n-273")


@dataclass(frozen=True)
class Check:
    """One statement of the source, where it is made, and the verdict here."""

    name: str
    pinpoint: str
    holds: bool
    value: str


# --------------------------------------------------------------------------- arithmetic


def maximiser(n: int) -> tuple[int, int]:
    """The (p, q) with 16p + 21q <= n - 15 maximising p + 2q, ties to the larger q."""
    budget = n - FIRST
    if budget < 0:
        raise ValueError(f"F(n) is defined for n >= {FIRST}")
    best: tuple[int, int, int] | None = None
    for q in range(budget // 21 + 1):
        p = (budget - 21 * q) // 16
        key = (p + 2 * q, q, p)
        if best is None or key[:2] > best[:2]:
            best = key
    assert best is not None
    return best[2], best[1]


def excess(n: int) -> int:
    """F(n) = 1 + max{p + 2q : 16p + 21q <= n - 15}."""
    p, q = maximiser(n)
    return 1 + p + 2 * q


def ceil_sqrt(n: int) -> int:
    root = math.isqrt(n)
    return root if root * root == n else root + 1


def ryu(k: int) -> int:
    """Ryu's Theorem 1.4: c*(k) <= 8 ceil(sqrt(k - 4)) - 1 for k >= 6."""
    return 8 * ceil_sqrt(k - 4) - 1


def ams(k: int) -> int | None:
    """Arslanov, Mustafin and Shangitbayev: c*(k) <= k - 1, stated for k >= 12."""
    return k - 1 if k >= 12 else None


def theorem_two(k: int) -> int:
    """Theorem 2 read on the deficiency: c*(k) <= k^2 - (k^2 - k + F(k)) - 1."""
    return k - 1 - excess(k)


# --------------------------------------------------------------------------- the packet


def retained_text(relative: str) -> str:
    return read_retained_bytes(SOURCE / relative).decode("utf-8")


def _table(relative: str, delimiter: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(retained_text(relative)), delimiter=delimiter))


def header(text: str) -> list[str]:
    """The first data line of a certificate: ``n S`` or ``n W H``."""
    for line in text.splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            return line.split()
    raise ValueError("a certificate with no header")


def inventory_files() -> list[str]:
    """The 76 certificates the retained tables name, in table order."""
    files = [
        f"theorem/n{int(row['n']):03d}_F{int(row['F'])}.cert"
        for row in _table("theorem/inventory.tsv", "\t")
    ]
    files += [
        f"theorem/{row['file']}"
        for row in _table("theorem/best.tsv", "\t")
        if row["file"].startswith("best/")
    ]
    return files


def manifest_digests() -> dict[str, str]:
    """Each upstream path's SHA-256, as the packet's subtree manifest records it."""
    digests: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, _, path = line.partition("  ")
        digests[path.removeprefix("./")] = digest
    return digests


def freeze_headers(checkout: Path) -> dict[str, Any]:
    """The frozen header list, read from a checkout at the pin and held to the manifest."""
    digests = manifest_digests()
    rows = []
    for relative in inventory_files():
        with (checkout / relative).open("rb") as stream:
            raw = stream.read(MAX_CERTIFICATE_BYTES + 1)
        if len(raw) > MAX_CERTIFICATE_BYTES:
            raise ValueError(f"{relative}: larger than any inventory certificate")
        digest = hashlib.sha256(raw).hexdigest()
        if digest != digests.get(relative):
            raise ValueError(f"{relative}: the checkout's bytes are not the manifest's")
        fields = header(raw.decode("utf-8"))
        if len(fields) != 2:
            raise ValueError(f"{relative}: the header is not `n S`")
        rows.append(
            {"file": relative, "count": int(fields[0]), "side": fields[1], "sha256": digest}
        )
    return {"format": HEADERS_FORMAT, "revision": REVISION, "rows": rows}


def headers_text(value: Mapping[str, Any]) -> str:
    """The frozen list with one row per line."""
    head = [f"  {json.dumps(key)}: {json.dumps(value[key])}," for key in ("format", "revision")]
    rows = ",\n".join("    " + json.dumps(row) for row in value["rows"])
    return "{\n" + "\n".join(head) + '\n  "rows": [\n' + rows + "\n  ]\n}\n"


def frozen_headers() -> tuple[dict[str, list[str]], list[str]]:
    """Each certificate's header from the frozen list, and every way the list fails.

    The list must name exactly the certificates the tables name, in their order, and a
    retained file must state its row's header. Its digests are data for the release that
    retains the other files; nothing here compares them, since the list, the manifest and
    the retained copies are all this repository's (OR-16).
    """
    stored = json.loads(HEADERS.read_text(encoding="utf-8"))
    problems: list[str] = []
    if stored.get("format") != HEADERS_FORMAT or stored.get("revision") != REVISION:
        problems.append("frozen list: format or revision")
    rows = stored.get("rows", [])
    if [row.get("file") for row in rows] != inventory_files():
        problems.append("frozen list: not the certificates the tables name, in order")
    fields: dict[str, list[str]] = {}
    for row in rows:
        relative = row["file"]
        fields[relative] = [str(row["count"]), row["side"]]
        path = SOURCE / relative
        if path.is_file() or path.with_name(path.name + ".gz").is_file():
            stated = header(retained_text(relative))
            if stated != fields[relative]:
                problems.append(f"frozen list: {relative} states {stated}, not the list's")
                fields[relative] = stated
    return fields, problems


def square_squeeze(fields: Sequence[str]) -> Fraction:
    side = Fraction(fields[1])
    return math.ceil(side) - side


def inventory_checks() -> tuple[list[Check], dict[int, int]]:
    """The inventory's rows and headers; also the best excess j each n reaches."""
    checks: list[Check] = []
    best: dict[int, int] = {}
    rows = _table("theorem/inventory.tsv", "\t")
    headers, problems = frozen_headers()
    for row in rows:
        n = int(row["n"])
        p, q = maximiser(n)
        f = excess(n)
        r = n - 16 * p - 21 * q
        count = n * n - n + f
        stated = (int(row["F"]), int(row["p"]), int(row["q"]), int(row["base_n"]))
        if stated != (f, p, q, r) or not FIRST <= r <= 30 or int(row["count"]) != count:
            problems.append(f"n={n}: row {stated} {row['count']}, recomputed {(f, p, q, r)}")
        fields = headers.get(f"theorem/n{n:03d}_F{int(row['F'])}.cert", ["0", "0"])
        side = Fraction(20000 * n - 1, 20000)
        if [int(fields[0]), Fraction(fields[1])] != [count, side] or len(fields) != 2:
            problems.append(f"n={n}: certificate header {fields[:2]}")
        if Fraction(row["side"]) != side or Fraction(row["d0"]) != D0:
            problems.append(f"n={n}: side or squeeze column")
        best[n] = f
    checks.append(
        Check(
            "theorem inventory",
            "theorem/README.md; theorem/inventory.tsv; theorem/n0NN_F*.cert line 2",
            not problems and [int(row["n"]) for row in rows] == list(range(FIRST, LAST + 1)),
            "; ".join(problems)
            or f"{len(rows)} rows n = {FIRST}..{LAST}: F(n), (p, q), base and count "
            "recomputed; each header states n^2 - n + F(n) squares at side (20000n - 1)/20000",
        )
    )
    problems = []
    files = 0
    for row in _table("theorem/best.tsv", "\t"):
        n, j, count = int(row["n"]), int(row["best_j"]), int(row["count"])
        if count != n * n - n + j or int(row["F"]) != excess(n) or j < excess(n):
            problems.append(f"n={n}: count {count}, j {j}")
        if row["file"].startswith("best/"):
            files += 1
            fields = headers.get(f"theorem/{row['file']}", ["0", "0"])
            if [int(fields[0]), Fraction(fields[1])] != [count, Fraction(20000 * n - 1, 20000)]:
                problems.append(f"n={n}: certificate header {fields[:2]}")
            if j <= excess(n):
                problems.append(f"n={n}: a best/ file with no excess beyond F(n)")
        best[n] = max(best[n], j)
    checks.append(
        Check(
            "best-excess inventory",
            "theorem/best.tsv; theorem/best/n0NN_jJ.cert line 2",
            not problems and files == 26,
            "; ".join(problems)
            or f"{files} best/ certificates, each n^2 - n + j squares at side "
            "(20000n - 1)/20000 with j > F(n); every row's count is n^2 - n + j",
        )
    )
    problems = []
    composites = _table("composites/table.csv", ",")
    for row in composites:
        n, j, count = int(row["n"]), int(row["j"]), int(row["count"])
        if count != n * n - n + j:
            problems.append(f"{row['id']}: count {count}")
        if Decimal(row["side_rounded_up_15"]) >= n:
            problems.append(f"{row['id']}: side {row['side_rounded_up_15']} not below n")
        if FIRST <= n <= LAST and j > best[n]:
            problems.append(f"{row['id']}: j = {j} beyond the inventory's {best[n]}")
    checks.append(
        Check(
            "composites dominated in excess",
            "composites/TABLE.md; composites/table.csv",
            not problems and len(composites) == 230,
            "; ".join(problems)
            or f"{len(composites)} rows: each count n^2 - n + j, each printed side below n, "
            "and no j above the inventory's best at its n",
        )
    )
    return checks, best


def rectangle_checks() -> tuple[list[Check], dict[str, Fraction]]:
    """Each rectangle header's count, box, waste and squeeze, read exactly."""
    squeezes: dict[str, Fraction] = {}
    problems: list[str] = []
    names = sorted(path.name for path in (SOURCE / "rectangles").iterdir() if path.is_dir())
    for name in names:
        fields = header(retained_text(f"rectangles/{name}/{name}.cert"))
        count, width, height = int(fields[0]), Fraction(fields[1]), Fraction(fields[2])
        a, b = math.ceil(width), math.ceil(height)
        box = name.split("_")[0].removeprefix("r")
        if f"{a}x{b}" != box or f"n{count:04d}" != name.split("_")[1] or a <= b:
            problems.append(f"{name}: header {count} {a}x{b}")
        squeeze = min(a - width, b - height)
        squeezes[name] = squeeze
        if squeeze <= 0 or squeeze < STATED_SQUEEZE.get(name, Fraction(0)):
            problems.append(f"{name}: squeeze {float(squeeze):.6g}")
        expected_waste = {"r22x21_n0443": b - 2}.get(name, b - 1)
        if a * b - count != expected_waste:
            problems.append(f"{name}: waste {a * b - count}, the README says {expected_waste}")
    check = Check(
        "rectangle headers",
        "README.md, ingredient table; rectangles/*/NOTES.md; theorem/PIECES.md",
        not problems and len(names) == 6,
        "; ".join(problems)
        or "six rectangles a x b with a > b, waste b - 1 (b - 2 for R'), squeezes "
        + ", ".join(f"{name} {float(value):.9f}" for name, value in squeezes.items()),
    )
    return [check], squeezes


def squeeze_check(squeezes: Mapping[str, Fraction]) -> Check:
    """The uniform squeeze 1/10000 against every piece header retained on ``main``."""
    pieces = dict(squeezes)
    for name in DANIEL_PIECES:
        path = ROOT / DANIEL_TWINS / f"batch/certs/{name}.cert"
        pieces[name] = square_squeeze(header(read_retained_bytes(path).decode("utf-8")))
    for name, relative in OTHER_PIECES.items():
        pieces[name] = square_squeeze(
            header(read_retained_bytes(ROOT / relative).decode("utf-8"))
        )
    least = min(pieces, key=lambda name: pieces[name])
    return Check(
        "uniform squeeze below every retained piece",
        "theorem/PIECES.md, last paragraph",
        all(value > D0 for value in pieces.values()),
        f"{len(pieces)} pieces read; least squeeze {least} {float(pieces[least]):.9f}; "
        "the direct packings n0381..n0651 and n0382..n0814 are retained by another packet",
    )


# --------------------------------------------------------------------------- the record


def read_record(commit: str) -> dict[str, Any]:
    """Each count's recorded upper bound where it is below its grid, from the live record."""
    rows: dict[str, str] = {}
    for n in range((TABLE.start - 1) ** 2 + 1, HORIZON + 1):
        case = coverage.parse_case(ROOT / f"frontier/n-{n:03d}.md")
        value = str(case["reported_upper_bound"]["value"])
        if Decimal(value) < ceil_sqrt(n):
            rows[str(n)] = value
    beyond = coverage.current_beyond_horizon(
        safe_load(coverage.COVERAGE.read_text(encoding="utf-8"))
    )
    for n, row in sorted(beyond.items()):
        if Decimal(str(row["value"])) < ceil_sqrt(n):
            rows[str(n)] = str(row["value"])
    return {"read_at": commit, "below_grid": rows}


def record_deficiency(record: Mapping[str, Any], k: int) -> int | None:
    """k^2 - m - 1 for the largest recorded count m <= k^2 with an upper bound below k."""
    counts = [
        int(n)
        for n, value in record["below_grid"].items()
        if (k - 1) ** 2 < int(n) <= k * k and Decimal(value) < k
    ]
    return k * k - max(counts) - 1 if counts else None


def deficiency_table(
    record: Mapping[str, Any], best: Mapping[int, int]
) -> list[dict[str, Any]]:
    rows = []
    for k in TABLE:
        published = [value for value in (ams(k), ryu(k)) if value is not None]
        inventory = k - 1 - best[k] if k in best else None
        theorems = [k - 2, theorem_two(k)]
        rows.append(
            {
                "k": k,
                "F": excess(k),
                "ams": ams(k),
                "ryu": ryu(k),
                "theorem_1": k - 2,
                "theorem_2": theorem_two(k),
                "inventory": inventory,
                "record_rows": record_deficiency(record, k),
                "before": min(published),
                "after_theorems": min(published + theorems),
                "after_inventory": min([*published, *theorems, inventory or k]),
            }
        )
    return rows


def _runs(values: Sequence[int]) -> list[list[int]]:
    """Consecutive integers grouped as [first, last] runs."""
    runs: list[list[int]] = []
    for value in values:
        if runs and runs[-1][1] == value - 1:
            runs[-1][1] = value
        else:
            runs.append([value, value])
    return runs


def crossover() -> dict[str, Any]:
    """Where Theorem 2 is below, equal to or above Ryu's bound, searched to the limit."""
    span = range(FIRST, CROSSOVER_LIMIT + 1)
    return {
        "theorem_2_below_ryu": _runs([k for k in span if theorem_two(k) < ryu(k)]),
        "tied": _runs([k for k in span if theorem_two(k) == ryu(k)]),
        "ryu_below_theorem_2": _runs([k for k in span if ryu(k) < theorem_two(k)]),
        "searched_to": CROSSOVER_LIMIT,
    }


def direct_sides() -> dict[int, Decimal]:
    """The direct packings' sides as the README's table prints them, rounded up."""
    sides: dict[int, Decimal] = {}
    for line in retained_text("README.md").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0].startswith("`n0") and cells[1].isdigit():
            sides[int(cells[1])] = Decimal(cells[3])
    return sides


def composite_map(record: Mapping[str, Any]) -> dict[str, Any]:
    """Each composite count's smallest side against every other report at that count.

    Sides are compared as the sources print them, rounded up at 15 places, and the
    inventory's exactly; no two that differ lie within a unit of the last place here.
    """
    best: dict[int, tuple[Decimal, str]] = {}
    for row in _table("composites/table.csv", ","):
        count, side = int(row["count"]), Decimal(row["side_rounded_up_15"])
        if count not in best or side < best[count][0]:
            best[count] = (side, row["id"])
    inventory = {
        int(row["count"]): Decimal(row["side_up15"])
        for name in ("theorem/inventory.tsv", "theorem/best.tsv")
        for row in _table(name, "\t")
    }
    direct = direct_sides()
    rows = []
    for count, (side, label) in sorted(best.items()):
        others = {
            "record": Decimal(record["below_grid"][str(count)])
            if str(count) in record["below_grid"]
            else Decimal(ceil_sqrt(count)),
            "inventory": inventory.get(count),
            "direct": direct.get(count),
        }
        below = [name for name, value in others.items() if value is not None and value <= side]
        rows.append(
            {
                "count": count,
                "composite": label,
                "side": str(side),
                **{
                    name: None if value is None else str(value)
                    for name, value in others.items()
                },
                "smallest": below or "composite",
            }
        )
    alone = [row["count"] for row in rows if row["smallest"] == "composite"]
    return {
        "counts": len(rows),
        "rows": len(_table("composites/table.csv", ",")),
        "composite_smallest": alone,
        "map": rows,
    }


def inventory_map(record: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Each inventory certificate's side, from the frozen list, against every other report.

    The other reports are the record's row or the grid, the smallest composite of the same
    count and the direct packing of the same count, each as its source prints it, rounded
    up; the inventory's sides are exact. Not part of the receipt: ``--print`` shows it.
    """
    headers, _problems = frozen_headers()
    composites: dict[int, Decimal] = {}
    for row in _table("composites/table.csv", ","):
        count, side = int(row["count"]), Decimal(row["side_rounded_up_15"])
        composites[count] = min(side, composites.get(count, side))
    direct = direct_sides()
    rows = []
    for relative in inventory_files():
        count, side = int(headers[relative][0]), Fraction(headers[relative][1])
        value = record["below_grid"].get(str(count))
        others = {
            "record": Decimal(value) if value is not None else Decimal(ceil_sqrt(count)),
            "composite": composites.get(count),
            "direct": direct.get(count),
        }
        below = [
            name
            for name, other in others.items()
            if other is not None and Fraction(other) <= side
        ]
        rows.append({"count": count, "file": relative, "smallest": below or "inventory"})
    return sorted(rows, key=lambda row: row["count"])


# --------------------------------------------------------------------------- receipt


def build(record: Mapping[str, Any]) -> dict[str, Any]:
    checks, best = inventory_checks()
    rectangles, squeezes = rectangle_checks()
    checks += rectangles
    checks.append(squeeze_check(squeezes))
    return {
        "format": FORMAT,
        "packet": PACKET.relative_to(REPO).as_posix(),
        "checks": [asdict(check) for check in checks],
        "record": dict(record),
        "deficiency": deficiency_table(record, best),
        "crossover": crossover(),
        "composites": composite_map(record),
    }


def _head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout.strip()


def _dump(value: Mapping[str, Any]) -> str:
    return json.dumps(value, indent=1, ensure_ascii=False) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="read the live record; write")
    mode.add_argument("--check", action="store_true", help="rebuild from the frozen record")
    mode.add_argument("--print", action="store_true", help="print the deficiency table")
    mode.add_argument(
        "--freeze-headers", type=Path, metavar="CHECKOUT", help="write the frozen header list"
    )
    args = parser.parse_args(argv)
    if args.freeze_headers is not None:
        frozen = freeze_headers(args.freeze_headers)
        HEADERS.write_text(headers_text(frozen), encoding="utf-8")
        print(f"{len(frozen['rows'])} headers frozen, each at its manifest digest")
        return 0
    if args.write:
        receipt = build(read_record(_head()))
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPT.write_text(_dump(receipt), encoding="utf-8")
    else:
        stored = json.loads(RECEIPT.read_text(encoding="utf-8"))
        receipt = build(stored["record"])
        if args.check and receipt != stored:
            print("FANG_EXCESS_INVENTORY_DRIFT: the receipt differs from its rebuild")
            return 1
    failed = [check for check in receipt["checks"] if not check["holds"]]
    for check in receipt["checks"]:
        print(("HOLDS " if check["holds"] else "FAILS ") + f"{check['name']}: {check['value']}")
    if args.print:
        for row in receipt["deficiency"]:
            print(json.dumps(row))
        print(json.dumps(receipt["crossover"]))
        for row in inventory_map(receipt["record"]):
            print(json.dumps(row))
    if failed:
        return 1
    print("FANG_EXCESS_INVENTORY_HOLDS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
