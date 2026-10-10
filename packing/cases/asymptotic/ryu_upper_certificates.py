"""Independent exact check of the five certificates of Ryu's Theorem 1.6 on c*(k).

Theorem 1.6 of Sungjoon Ryu's preprint "Packing k^2-c unit squares: an upper bound of
order k^{3/8} for the deficiency" (issues #471 and #486) states c*(10^5) <= 1583,
c*(10^6) <= 3972, c*(10^7) <= 10039, c*(3.825*10^7) <= 16988 and c*(10^8) <= 24790. Each
rests on a data file ``data/stair_k<k>.json.gz`` listing, for the four ends of the two
tilted bands of the L-shaped frame, the lift of the end and every piece of it in exact
rationals; the rows of the bands are not in the file and are carried by Lemmas 3.3 and
6.1, a trust boundary the paper states.

This module was written from Section 9 of the text and the data format, and shares no
code with the source's ``stair_check.py`` or ``stair_dump.py``. From (k, b, y0) alone it
recomputes the band (tan(theta/2) = b/(b^2-1), w, S, d, h), for both bands the rows
R = floor((L_b - h - 2 y0)/d) + 1 and the upper lift y1, and then decides (C0)-(C4) of the
proof in exact rationals: the file's lifts are y0 and y1, every count is a positive
integer, w < b, R >= 1 and y0 <= y1 < y0 + d, every piece is a 1 x n rectangle (for a
column cos^2 + sin^2 = 1 exactly), every vertex lies in Reg(y), and two pieces of an end
whose bounding boxes overlap have disjoint interiors by an exact separating-axis test. It
counts N = (k-b)^2 + b(R_right + R_top) + (end squares), c = k^2 - N, and checks the waste
identity of Proposition 6.3 exactly; c*(k) <= c - 1 then follows from Lemma 2.2.

The three smaller certificates are retained in
``resources/web/squarepacker-k2-minus-c-upper-2026-10-09/source/data/``; the two largest
are hosted outside Git (``hosted/squarepacker-k2-minus-c-upper-certificates.yaml``) and
are read through `sqpack.hosted_data.require`, which checks their SHA-256. Mutations
(``--mutate``) are controls: each must be refused.

Run from ``packing/``::

    uv run --frozen --all-extras --group dev python -m \\
        cases.asymptotic.ryu_upper_certificates --k 100000 [--k ...] [--mutate NAME]
"""

from __future__ import annotations

import argparse
import gzip
import io
import json
import time
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from gmpy2 import mpq

from sqpack.hosted_data import require

REPO = Path(__file__).resolve().parents[3]
RETAINED = REPO / "packing/resources/web/squarepacker-k2-minus-c-upper-2026-10-09/source/data"
HOSTED = REPO / "packing/hosted/squarepacker-k2-minus-c-upper-certificates.yaml"
HOSTED_DIR = "packing/cases/asymptotic/hosted/squarepacker-k2-minus-c-upper"
#: The rows of Table 2: k, b, y0, c = k^2 - N.
TABLE_2: dict[int, tuple[int, str, int]] = {
    100000: (623, "257/4", 1584),
    1000000: (2481, "653/4", 3973),
    10000000: (9875, "1663/4", 10040),
    38250000: (22086, "710", 16989),
    100000000: (39314, "1041", 24791),
}
MAX_DECOMPRESSED = 256 * 1024 * 1024
ENDS = (("right", "bottom"), ("right", "top"), ("top", "bottom"), ("top", "top"))

type Point = tuple[mpq, mpq]
type Rectangle = tuple[Point, Point, Point, Point]


def certificate_path(k: int) -> Path:
    """The certificate for ``k``: retained in the packet, or the checked hosted copy."""
    name = f"stair_k{k}.json.gz"
    retained = RETAINED / name
    return retained if retained.is_file() else require(f"{HOSTED_DIR}/{name}", HOSTED)


def load(path: Path) -> dict[str, Any]:
    """The certificate's JSON, decompressed with a bound on its size."""
    with gzip.GzipFile(fileobj=io.BytesIO(path.read_bytes())) as stream:
        data = stream.read(MAX_DECOMPRESSED + 1)
    if len(data) > MAX_DECOMPRESSED:
        raise ValueError(f"{path} decompresses past {MAX_DECOMPRESSED} bytes")
    document = json.loads(data.decode("ascii"))
    if not isinstance(document, dict):
        raise TypeError(f"{path} is not a JSON object")
    return document


def rational(value: object) -> mpq:
    """An exact rational from the file's integers and ``"p/q"`` or ``"p"`` strings."""
    if isinstance(value, bool):
        raise TypeError(f"not a rational: {value!r}")
    if isinstance(value, int):
        return mpq(value)
    if isinstance(value, str):
        numerator, slash, denominator = value.partition("/")
        return mpq(int(numerator), int(denominator)) if slash else mpq(int(numerator))
    raise TypeError(f"not a rational: {value!r}")


def floor(value: mpq) -> int:
    return int(value.numerator) // int(value.denominator)


def is_count(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def separated(first: Rectangle, second: Rectangle) -> bool:
    """Disjoint interiors, decided along the edge directions of both rectangles."""
    for rectangle in (first, second):
        (x0, y0), (x1, y1), _, (x3, y3) = rectangle
        for ax, ay in ((x1 - x0, y1 - y0), (x3 - x0, y3 - y0)):
            a = [x * ax + y * ay for x, y in first]
            b = [x * ax + y * ay for x, y in second]
            if max(a) <= min(b) or max(b) <= min(a):
                return True
    return False


@dataclass
class End:
    band: str
    end: str
    lift_matches: bool
    counts_are_integers: bool
    unit_tilt: bool
    pieces: int
    squares: int
    uncovered: float
    bad_shape: int
    bad_containment: int
    box_pairs: int
    overlaps: int
    passed: bool


@dataclass
class Report:
    k: int
    b: int
    y0: str
    side_below_k: bool
    width_below_b: bool
    rows: dict[str, int]
    upper_lifts_in_window: bool
    ends: list[End] = field(default_factory=list)
    squares: int = 0
    deficit: int = 0
    waste_identity: bool = False
    box_pairs: int = 0
    matches_table_2: bool = False
    passed: bool = False
    bound: str = ""
    seconds: float = 0.0
    mutation: str | None = None


#: Each control changes one piece of the right band's lower end, or its lift.
MUTATIONS: dict[str, Callable[[dict[str, Any]], None]] = {}


def _mutation(
    name: str,
) -> Callable[[Callable[[dict[str, Any]], None]], Callable[[dict[str, Any]], None]]:
    def register(
        function: Callable[[dict[str, Any]], None],
    ) -> Callable[[dict[str, Any]], None]:
        MUTATIONS[name] = function
        return function

    return register


@_mutation("column-right")
def _column_right(end: dict[str, Any]) -> None:
    """A column a third of the way along moves right by 10^-7."""
    column = end["columns"][len(end["columns"]) // 3]
    column[0] = str(rational(column[0]) + mpq(1, 10**7))


@_mutation("column-longer")
def _column_longer(end: dict[str, Any]) -> None:
    """The middle column gains one square."""
    end["columns"][len(end["columns"]) // 2][2] += 1


@_mutation("layer-longer")
def _layer_longer(end: dict[str, Any]) -> None:
    """The middle layer gains one square."""
    end["layers"][len(end["layers"]) // 2][2] += 1


@_mutation("wedge-longer")
def _wedge_longer(end: dict[str, Any]) -> None:
    """The first left-wall row gains one square."""
    end["wedge"][0][1] += 1


@_mutation("lift-raised")
def _lift_raised(end: dict[str, Any]) -> None:
    """The end's lift is raised by 1/4, so it no longer equals y0."""
    end["y"] = str(rational(end["y"]) + mpq(1, 4))


@_mutation("column-tilt")
def _column_tilt(end: dict[str, Any]) -> None:
    """The tilt's sine grows by 10^-12, so cos^2 + sin^2 != 1."""
    end["sa"] = str(rational(end["sa"]) + mpq(1, 10**12))


def rectangles(end: dict[str, Any]) -> tuple[mpq, mpq, list[tuple[int, Rectangle]]]:
    """The end's tilt and every piece as (squares, four vertices)."""
    cos, sin = rational(end["ca"]), rational(end["sa"])
    out: list[tuple[int, Rectangle]] = []
    for x_text, y_text, n in end["columns"]:
        x, y = rational(x_text), rational(y_text)
        out.append(
            (
                n,
                (
                    (x, y),
                    (x + cos, y + sin),
                    (x + cos - n * sin, y + sin + n * cos),
                    (x - n * sin, y + n * cos),
                ),
            )
        )
    for x_text, row, length in end["layers"]:
        x, y = rational(x_text), mpq(row)
        out.append((length, ((x, y), (x, y + 1), (x + length, y + 1), (x + length, y))))
    for row, length in end["wedge"]:
        y, right = mpq(row), mpq(length)
        out.append((length, ((mpq(0), y), (mpq(0), y + 1), (right, y + 1), (right, y))))
    return cos, sin, out


def check_end(
    end: dict[str, Any], width: mpq, sine: mpq, slope: mpq, expected_lift: mpq
) -> tuple[End, mpq, int]:
    """(C0) and (C2)-(C4) for one end; also its uncovered area and its squares."""
    lift = rational(end["y"])
    cos, sin, pieces = rectangles(end)
    counts = (
        all(is_count(c[2]) and c[2] >= 1 for c in end["columns"])
        and all(is_count(c[1]) and is_count(c[2]) and c[2] >= 1 for c in end["layers"])
        and all(is_count(c[0]) and is_count(c[1]) and c[1] >= 1 for c in end["wedge"])
    )
    bad_shape = bad_containment = 0
    boxes: list[tuple[mpq, mpq, mpq, mpq]] = []
    squares = 0
    for n, rectangle in pieces:
        squares += n
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = rectangle
        dx, dy, ex, ey = x1 - x0, y1 - y0, x3 - x0, y3 - y0
        if not (
            dx * dx + dy * dy == 1
            and dx * ex + dy * ey == 0
            and ex * ex + ey * ey == n * n
            and x2 == x1 + ex
            and y2 == y1 + ey
        ):
            bad_shape += 1
        if any(
            not (0 <= x <= width and 0 <= y <= lift + (x - sine) * slope) for x, y in rectangle
        ):
            bad_containment += 1
        xs, ys = [p[0] for p in rectangle], [p[1] for p in rectangle]
        boxes.append((min(xs), max(xs), min(ys), max(ys)))
    order = sorted(range(len(boxes)), key=lambda index: boxes[index][0])
    pairs = overlaps = 0
    for position, i in enumerate(order):
        for j in order[position + 1 :]:
            if boxes[j][0] >= boxes[i][1]:
                break
            if boxes[j][2] >= boxes[i][3] or boxes[i][2] >= boxes[j][3]:
                continue
            pairs += 1
            if not separated(pieces[i][1], pieces[j][1]):
                overlaps += 1
    area = lift * width + (width * width / 2 - sine * width) * slope
    unit = cos * cos + sin * sin == 1 and cos > 0 and sin > 0
    result = End(
        band="",
        end="",
        lift_matches=lift == expected_lift,
        counts_are_integers=counts,
        unit_tilt=unit,
        pieces=len(pieces),
        squares=squares,
        uncovered=float(area - squares),
        bad_shape=bad_shape,
        bad_containment=bad_containment,
        box_pairs=pairs,
        overlaps=overlaps,
        passed=False,
    )
    result.passed = (
        result.lift_matches
        and counts
        and unit
        and bad_shape == 0
        and bad_containment == 0
        and overlaps == 0
    )
    return result, area - squares, squares


def check_certificate(
    document: dict[str, Any],
    k: int,
    mutation: str | None = None,
    *,
    first_end_only: bool = False,
) -> Report:
    """Decide one certificate; ``mutation`` names a control applied to the first end.

    With ``first_end_only`` only the right band's lower end is decided, which is all a
    control needs: the mutated end alone must be refused. Such a report counts no
    squares and holds no waste identity, so it never passes as a certificate.
    """
    start = time.monotonic()
    if int(document["k"]) != k:
        raise ValueError(f"the certificate is for k = {document['k']}, not {k}")
    b = int(document["b"])
    y0 = rational(document["y0"])
    ends = document["ends"]
    if [(e["band"], e["end"]) for e in ends] != list(ENDS):
        raise ValueError(
            "the certificate's ends are not right/bottom, right/top, top/bottom, top/top"
        )
    if mutation is not None:
        MUTATIONS[mutation](ends[0])
    t = mpq(b, b * b - 1)
    cos, sin = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    width, slope, spacing, height = b * cos + sin, sin / cos, 1 / cos, b * sin + cos
    side = k - b + width
    report = Report(
        k=k,
        b=b,
        y0=str(document["y0"]),
        side_below_k=side < k,
        width_below_b=width < b,
        rows={},
        upper_lifts_in_window=True,
        mutation=mutation,
    )
    squares = mpq((k - b) ** 2)
    identity = mpq(k) ** 2 - side * side
    for band_index, (band, length) in enumerate((("right", side), ("top", mpq(k - b)))):
        rows = floor((length - height - 2 * y0) / spacing) + 1
        y1 = length - height - (rows - 1) * spacing - y0
        report.rows[band] = rows
        report.upper_lifts_in_window &= rows >= 1 and y0 >= 0 and y0 <= y1 < y0 + spacing
        squares += b * rows
        identity += (rows - 1) * slope
        for end, expected in zip(
            ends[2 * band_index : 2 * band_index + 2], (y0, y1), strict=True
        ):
            if first_end_only and report.ends:
                break
            result, uncovered, count = check_end(end, width, sin, slope, expected)
            result.band, result.end = band, end["end"]
            report.ends.append(result)
            squares += count
            identity += uncovered + slope / 2
            report.box_pairs += result.box_pairs
    deficit = mpq(k) ** 2 - squares
    report.squares = int(squares)
    report.deficit = int(deficit)
    report.waste_identity = deficit == identity
    expected_b, expected_y0, expected_c = TABLE_2.get(k, (b, report.y0, report.deficit))
    report.matches_table_2 = (b, report.y0, report.deficit) == (
        expected_b,
        expected_y0,
        expected_c,
    )
    # With first_end_only the verdict is the decided end's alone, so that a control the
    # checker failed to notice would show as passing; it then bounds nothing.
    report.passed = (
        report.side_below_k
        and report.width_below_b
        and report.upper_lifts_in_window
        and all(end.passed for end in report.ends)
        and (report.waste_identity or first_end_only)
    )
    proves = report.passed and not first_end_only
    report.bound = f"c*({k}) <= {report.deficit - 1}" if proves else "none"
    report.seconds = round(time.monotonic() - start, 2)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument(
        "--k", type=int, action="append", choices=sorted(TABLE_2), required=True
    )
    parser.add_argument("--mutate", choices=sorted(MUTATIONS), action="append", default=[])
    parser.add_argument("--file", type=Path, help="read this certificate instead (one --k)")
    args = parser.parse_args(argv)
    if args.file is not None and len(args.k) != 1:
        parser.error("--file needs exactly one --k")
    reports: list[dict[str, Any]] = []
    ok = True
    for k in args.k:
        path = args.file or certificate_path(k)
        for mutation in [None, *args.mutate]:
            report = check_certificate(
                load(path), k, mutation, first_end_only=mutation is not None
            )
            reports.append(asdict(report))
            # A control passes when it is refused; the unmutated certificate when it passes.
            ok &= report.passed == (mutation is None) and (
                mutation is not None or report.matches_table_2
            )
    print(json.dumps({"passed": ok, "reports": reports}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
