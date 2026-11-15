"""Build a 45-degree block with four corner staircases exactly over Q(sqrt 2), and decide it.

Issue #992 (Miguel Lara, 15 November 2026) states s(977) <= 17 + 21/sqrt(2) by a
construction in prose (``certificates/n977_certificate.md`` at larasmiguel/square-s977
``26d5695``), with a floating-point CSV at the relaxed side 31.85 and no exact
certificate. `devtools.construction_checker` cannot read it: its recipes tile or border a
replayed certificate with a rational side, and this side is irrational and has no parent.
So this module writes the statement down as a Witness/v2 over the field Q(sqrt 2) and
decides it on the two maintained exact routes over a number field,
`sqpack.witness.exact_verify` and `devtools.check_algebraic_witness_independent`.

**The recipe** (`Recipe`), as the certificate states it, for a block b, an integer p and
the bottom-left staircase's row widths w_0, w_1, ...:

- the side is L = p + (b/2) sqrt 2;
- b^2 squares turned 45 degrees: for i, j in 0 .. b - 1, with u = i - (b - 1)/2 and
  v = j - (b - 1)/2, the centre (L/2 + (u - v) sqrt(2)/2, L/2 + (u + v) sqrt(2)/2) and the
  basis (sqrt(2)/2, sqrt(2)/2), whose union is the diamond |x - L/2| + |y - L/2| <=
  (b/2) sqrt 2;
- the axis-aligned unit squares with lower-left corner (c, r), 0 <= r < len(w) and
  0 <= c < w_r, and their images under quarter turns of 90, 180 and 270 degrees about
  (L/2, L/2), (x, y) -> (L - y, x).

Nothing is transcribed from the CSV, which is numerical at another side; every coordinate
here is the statement's, exactly. `build` writes squares 1 to b^2 as the block, row by row
in i then j, then the bottom-left staircase by row and column, then its three turns.

**Controls** (`CONTROLS`) are the plan stated in advance (`PLAN`, retained beside the
receipt, whose digest think-ud9e recorded before any run; Git keeps its bytes from here,
OR-16): the construction accepted at contact on both
routes, two gross and three sharp changes refused on both. `decide` runs them and says
whether each came out as stated.

**Göbel** (`goebel_comparison`). `devtools.goebel_construction.side` at the count, the
Göbel square (p - 2, b) of Friedman's survey with one L-border around it, and the
(p - 1, b) arrangement, each read exactly: the family's condition a - 1 < (b/2) sqrt 2 <
a + 1 by squaring, floor(q + (b/2) sqrt 2) by ``math.isqrt``. It states what each gives
at the recipe's side; it registers nothing and changes no reading of the record.

From ``packing/``::

    python -m devtools.diamond_staircases decide [--write | --check]
    python -m devtools.diamond_staircases witness OUT.yaml
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_output_file

from devtools import check_algebraic_witness_independent as independent
from devtools import goebel_construction as goebel
from sqpack.witness import exact_verify

ROOT = Path(__file__).resolve().parents[1]
PACKET = "lara-s977-upper-bound-2026-11-15"
PACKET_DIR = ROOT / "resources" / "web" / PACKET
RECEIPT = PACKET_DIR / "receipts" / "exact-decision.json"
PLAN = PACKET_DIR / "receipts" / "controls-plan-n977.txt"
#: When the plan was stated, before any run of the construction (think-ud9e's notes).
PLAN_STATED_AT = "2026-11-15T07:05:48Z"
SOURCE = "larasmiguel/square-s977"
SOURCE_COMMIT = "26d5695abca2f8a005856e3c1ddc47171d661e9b"
STATEMENT = "certificates/n977_certificate.md"
FORMAT = "diamond-staircase-decision-v1"
#: The field Q(sqrt 2), as a Witness/v2 states it: x^2 - 2, high degree first, and (1, 2).
MINIMAL_POLYNOMIAL = ("1", "0", "-2")
ISOLATING_INTERVAL = ("1", "2")
ROUTES = ("exact_verify", "independent")
#: The sharp controls' distances, as the plan states them.
NUDGE = Fraction(1, 10**30)
STRETCH = Fraction(1, 10**50)
#: The most processes `receipt` runs controls in: the host's two-job budget.
MAX_JOBS = 2

type Element = tuple[Fraction, Fraction]
"""a + b sqrt 2, as (a, b)."""


class RecipeError(ValueError):
    """A recipe this module refuses to build."""


@dataclass(frozen=True, slots=True)
class Recipe:
    """The construction: count, block b, the side's integer part p, the bottom-left
    staircase's row widths from the bottom wall up."""

    n: int
    block: int
    offset: int
    widths: tuple[int, ...]

    @property
    def side(self) -> Element:
        return (Fraction(self.offset), Fraction(self.block, 2))

    def staircase(self) -> list[tuple[int, int]]:
        """The bottom-left staircase's cells (c, r), by row and column."""
        return [(c, r) for r, width in enumerate(self.widths) for c in range(width)]


#: The construction #992 states, at 26d5695.
STATED = Recipe(
    n=977, block=21, offset=17, widths=(15, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2)
)


def element(value: Element) -> str | list[str]:
    """A Witness/v2 scalar: a rational string, or [a, b] for a + b sqrt 2."""
    a, b = value
    return str(a) if b == 0 else [str(a), str(b)]


def _add(left: Element, right: Element) -> Element:
    return (left[0] + right[0], left[1] + right[1])


def _sub(left: Element, right: Element) -> Element:
    return (left[0] - right[0], left[1] - right[1])


def _rational(value: Fraction | int) -> Element:
    return (Fraction(value), Fraction(0))


def _turn(point: tuple[Element, Element], side: Element) -> tuple[Element, Element]:
    """A quarter turn counterclockwise about (L/2, L/2): (x, y) -> (L - y, x)."""
    x, y = point
    return (_sub(side, y), x)


def squares(recipe: Recipe) -> list[dict[str, Any]]:
    """The recipe's squares, centre and basis, in `build`'s order."""
    b, side = recipe.block, recipe.side
    if recipe.block < 1 or recipe.offset < 1 or any(w < 1 for w in recipe.widths):
        raise RecipeError(f"{recipe}: no construction")
    half_side = (side[0] / 2, side[1] / 2)
    turned_basis = [element((Fraction(0), Fraction(1, 2)))] * 2
    out: list[dict[str, Any]] = []
    middle = Fraction(b - 1, 2)
    for i in range(b):
        for j in range(b):
            u, v = i - middle, j - middle
            centre = (
                _add(half_side, (Fraction(0), (u - v) / 2)),
                _add(half_side, (Fraction(0), (u + v) / 2)),
            )
            out.append(
                {"center": [element(centre[0]), element(centre[1])], "basis": turned_basis}
            )
    corner = [
        (_rational(Fraction(2 * c + 1, 2)), _rational(Fraction(2 * r + 1, 2)))
        for c, r in recipe.staircase()
    ]
    for _quarter in range(4):
        out.extend({"center": [element(x), element(y)], "basis": ["1", "0"]} for x, y in corner)
        corner = [_turn(point, side) for point in corner]
    if len(out) != recipe.n:
        raise RecipeError(
            f"{recipe}: the block and four staircases hold {len(out)} squares, not {recipe.n}"
        )
    return out


def build(recipe: Recipe = STATED) -> dict[str, Any]:
    """The recipe as a Witness/v2 witness over Q(sqrt 2), every coordinate exact."""
    placed = squares(recipe)
    return {
        "id": f"W-{PACKET}-n{recipe.n:03d}",
        "n": recipe.n,
        "side": element(recipe.side),
        "square_size": "1",
        "representation": "center-basis",
        "scalar": {
            "kind": "algebraic-number-field",
            "minimal_polynomial": list(MINIMAL_POLYNOMIAL),
            "isolating_interval": list(ISOLATING_INTERVAL),
        },
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [{"id": k, **square} for k, square in enumerate(placed, start=1)],
        "claim": {
            "coordinate_provenance": "reported",
            "method": "exact-algebraic",
            "limitations": (
                f"The construction {SOURCE} {SOURCE_COMMIT[:7]} states in {STATEMENT}, "
                "written exactly from its statement; an upper bound only."
            ),
        },
    }


def document(witness: Mapping[str, Any]) -> dict[str, Any]:
    """The witness in its Witness/v2 envelope, as `packing-witness verify` reads a file."""
    return {
        "softschema": {
            "contract": "packing.squares:Witness/v2",
            "schema": "witness.schema.yaml",
            "envelope": "witness",
            "status": "enforced",
        },
        "witness": dict(witness),
    }


def _kinds(failures: Sequence[Any]) -> list[str]:
    """The kinds of sqpack's failures, each a (kind, detail) pair."""
    return sorted({str(failure[0]) for failure in failures})


def _independent_kinds(failures: Sequence[str]) -> list[str]:
    """The independent route's failures, named by kind as sqpack names them."""
    found: set[str] = set()
    for failure in failures:
        if "overlap" in failure:
            found.add("overlap")
        elif "leave the container" in failure:
            found.add("container")
        else:
            found.add("shape")
    return sorted(found)


def routes(witness: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Both exact routes' verdicts on ``witness``: what each refused, the pairs each
    decided, and the contacts each decided exactly.

    sqpack's least margins are kept only as exact zeros (``zero_margins``): its printed
    decimal of a small nonzero margin loses the exponent (think-526p), so a refused
    control's margin is not copied from it. The independent route prints its least
    margins in scientific notation, and those are kept as printed."""
    started = time.process_time()
    first, report = exact_verify(witness)
    middle = time.process_time()
    second = independent.check_witness(witness)
    ended = time.process_time()
    return {
        "exact_verify": {
            "passed": bool(first["verification_passed"]),
            "failures": _kinds(first["failures"]),
            "pairs_tested": int(first["pairs_tested"]),
            "touching_pairs": int(report.touching_pairs),
            "wall_contacts": int(report.container_contacts),
            "zero_margins": first["minimum_containment_clearance"] == "0"
            and first["minimum_best_pair_gap"] == "0",
            "cpu_seconds": round(middle - started, 3),
        },
        "independent": {
            "passed": bool(second["verification_passed"]),
            "failures": _independent_kinds(second["failures"]),
            "pairs_tested": int(second["pairs_tested"]),
            "touching_pairs": int(second["touching_pairs"]),
            "wall": str(second["minimum_containment_clearance"]),
            "gap": str(second["minimum_best_pair_gap"]),
            "cpu_seconds": round(ended - middle, 3),
        },
    }


def _shift(value: Any, delta: Fraction) -> Any:
    """A Witness/v2 scalar plus a rational ``delta``."""
    if isinstance(value, str):
        return str(Fraction(value) + delta)
    return [str(Fraction(value[0]) + delta), *value[1:]]


def _duplicate(witness: dict[str, Any], _recipe: Recipe) -> None:
    last = witness["squares"][-1]
    first = witness["squares"][0]
    last["center"], last["basis"] = (
        copy.deepcopy(first["center"]),
        copy.deepcopy(first["basis"]),
    )


def _past_row_one(witness: dict[str, Any], recipe: Recipe) -> None:
    last = witness["squares"][-1]
    c = recipe.widths[1]
    last["center"] = [str(Fraction(2 * c + 1, 2)), str(Fraction(3, 2))]
    last["basis"] = ["1", "0"]


def _side_lowered(witness: dict[str, Any], _recipe: Recipe) -> None:
    witness["side"] = _shift(witness["side"], -NUDGE)


def _block_moved(witness: dict[str, Any], recipe: Recipe) -> None:
    for square in witness["squares"][: recipe.block**2]:
        square["center"] = [
            _shift(square["center"][0], -NUDGE),
            _shift(square["center"][1], -NUDGE),
        ]


def _basis_stretched(witness: dict[str, Any], _recipe: Recipe) -> None:
    square = witness["squares"][0]
    square["basis"] = [_shift(square["basis"][0], STRETCH), square["basis"][1]]


@dataclass(frozen=True, slots=True)
class Control:
    """A change the plan states in advance, its kind, and the verdict it expects on both
    routes: ``()`` for accepted, else the failure kinds both must name."""

    name: str
    kind: str
    statement: str
    change: Callable[[dict[str, Any], Recipe], None] | None
    refused_for: tuple[str, ...]


CONTROLS = (
    Control("P0", "positive", "the construction as stated", None, ()),
    Control(
        "G1",
        "gross",
        "the last square replaced by a copy of square 1",
        _duplicate,
        ("overlap",),
    ),
    Control(
        "G2",
        "gross",
        "the last square replaced by an axis-aligned square with lower-left corner "
        "(w_1, 1), one cell past row 1 of the bottom-left staircase, inside the diamond",
        _past_row_one,
        ("overlap",),
    ),
    Control(
        "S1",
        "sharp",
        "the side lowered by 10^-30, every square kept",
        _side_lowered,
        ("container",),
    ),
    Control(
        "S2",
        "sharp",
        "the b^2 turned squares moved by (-10^-30, -10^-30), toward the bottom-left "
        "staircase, whose cells with c + r = p - 2 touch the diamond's edge at a corner",
        _block_moved,
        ("overlap",),
    ),
    Control(
        "S3",
        "sharp",
        "square 1's basis first component lengthened by 10^-50",
        _basis_stretched,
        ("shape",),
    ),
)


def run_control(control: Control, recipe: Recipe) -> dict[str, Any]:
    """One control on both routes, and whether each route's verdict is the plan's."""
    witness = build(recipe)
    if control.change is not None:
        control.change(witness, recipe)
    found = routes(witness)
    expected_pass = not control.refused_for
    as_expected = all(
        found[route]["passed"] == expected_pass
        and (expected_pass or set(control.refused_for) <= set(found[route]["failures"]))
        for route in ROUTES
    )
    if expected_pass:
        as_expected = as_expected and _at_contact(found)
    return {
        "control": control.name,
        "kind": control.kind,
        "statement": control.statement,
        "expected": "accepted" if expected_pass else "refused",
        "expected_failures": list(control.refused_for),
        "routes": found,
        "as_expected": as_expected,
    }


def _at_contact(found: Mapping[str, Mapping[str, Any]]) -> bool:
    """Whether both routes decided contacts exactly: sqpack's least wall clearance and pair
    gap exactly zero, and the independent route's touching pairs decided by exact sign,
    and its least wall clearance's float approximation zero (sqpack's zero is the exact
    one)."""
    first, second = found["exact_verify"], found["independent"]
    return (
        bool(first["zero_margins"])
        and first["touching_pairs"] > 0
        and second["touching_pairs"] > 0
        and float(second["wall"]) == 0
    )


def floor_root_two(p: Fraction, q: Fraction) -> int:
    """floor(p + q sqrt 2) for integer p and q >= 0, exactly: floor(sqrt(2 q^2)) is
    isqrt(floor(2 q^2))."""
    if p.denominator != 1 or q < 0:
        raise RecipeError(f"floor({p} + {q} sqrt 2): not read here")
    return int(p) + math.isqrt(math.floor(2 * q * q))


def goebel_admits(a: int, b: int) -> bool:
    """Göbel's condition a - 1 < (b/2) sqrt 2 < a + 1, exactly, by squaring."""
    half = Fraction(b * b, 2)
    return a >= 1 and (a - 1) ** 2 < half < (a + 1) ** 2


def goebel_comparison(recipe: Recipe = STATED) -> dict[str, Any]:
    """The recipe's side against Göbel's construction, exactly (the module docstring)."""
    side = goebel.Form(Fraction(recipe.offset), Fraction(recipe.block, 2), "recipe", recipe.n)
    construction = goebel.side(recipe.n)
    if goebel.less(side, construction):
        relation = "below"
    elif goebel.less(construction, side):
        relation = "above"
    else:
        relation = "equal"
    b = recipe.block
    a = recipe.offset - 2
    member_side = (Fraction(a + 1), Fraction(b, 2))
    member = 2 * (a + 1) * a + b * b
    layer = 2 * floor_root_two(*member_side) + 1
    deeper = recipe.offset - 1
    grid = math.isqrt(recipe.n - 1) + 1
    below_grid = Fraction(b * b, 2) < (grid - recipe.offset) ** 2 and grid > recipe.offset
    return {
        "side": side.text(),
        "goebel_construction": {
            "side": construction.text(),
            "family": construction.family,
            "count": construction.count,
            "relation": relation,
            "difference": goebel.Form(
                construction.p - side.p, construction.q - side.q, "difference", 0
            ).text(),
        },
        "l_border_of_member": {
            "a": a,
            "b": b,
            "admitted": goebel_admits(a, b),
            "count": member,
            "side": goebel.Form(member_side[0], member_side[1], "", 0).text(),
            "layer_adds": layer,
            "capacity": member + layer,
            "capacity_side": goebel.Form(member_side[0] + 1, member_side[1], "", 0).text(),
        },
        "deeper_arrangement": {
            "a": deeper,
            "b": b,
            "admitted": goebel_admits(deeper, b),
            "count": 2 * (deeper + 1) * deeper + b * b,
            "staircase": deeper * (deeper + 1) // 2,
            "recipe_staircase": sum(recipe.widths),
        },
        "grid": {"side": grid, "recipe_below": below_grid},
    }


def _run(item: tuple[int, Recipe]) -> dict[str, Any]:
    index, recipe = item
    return run_control(CONTROLS[index], recipe)


def receipt(recipe: Recipe = STATED, jobs: int = 1) -> dict[str, Any]:
    """Every control on both routes, the Göbel comparison and the plan's binding. The
    controls run in ``jobs`` processes, at most `MAX_JOBS`, and are kept in plan order."""
    work = [(index, recipe) for index in range(len(CONTROLS))]
    if jobs > 1:
        with ProcessPoolExecutor(max_workers=min(jobs, MAX_JOBS)) as pool:
            ran = list(pool.map(_run, work))
    else:
        ran = [_run(item) for item in work]
    turned = recipe.block**2
    return {
        "format": FORMAT,
        "packet": PACKET,
        "source": f"https://github.com/{SOURCE}/tree/{SOURCE_COMMIT}",
        "statement": STATEMENT,
        "recipe": {
            "n": recipe.n,
            "block": recipe.block,
            "offset": recipe.offset,
            "widths": list(recipe.widths),
            "turned": turned,
            "axis_aligned": recipe.n - turned,
            "side": element(recipe.side),
        },
        "field": {
            "minimal_polynomial": list(MINIMAL_POLYNOMIAL),
            "isolating_interval": list(ISOLATING_INTERVAL),
        },
        "plan": {
            "path": str(PLAN.relative_to(ROOT.parent)),
            "stated_at": PLAN_STATED_AT,
        },
        "routes": list(ROUTES),
        "controls": ran,
        "goebel": goebel_comparison(recipe),
    }


def _stable(value: Any) -> Any:
    """``value`` without the route timings, which differ between runs."""
    if isinstance(value, dict):
        return {k: _stable(v) for k, v in value.items() if k != "cpu_seconds"}
    if isinstance(value, list):
        return [_stable(v) for v in value]
    return value


def problems(found: Mapping[str, Any]) -> list[str]:
    """What a receipt fails: the plan's presence, a control not as stated, a decision off."""
    out: list[str] = []
    if not PLAN.is_file() or found["plan"]["stated_at"] != PLAN_STATED_AT:
        out.append("the plan stated before any run is not retained beside the receipt")
    out.extend(
        f"{control['control']}: not as the plan states"
        for control in found["controls"]
        if not control["as_expected"]
    )
    border = found["goebel"]["l_border_of_member"]
    if not (border["admitted"] and border["capacity"] >= found["recipe"]["n"]):
        out.append(
            "no admitted Göbel member with one L-border holds the count at the recipe's side"
        )
    return out


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    deciding = commands.add_parser("decide", help="run the controls on both routes")
    mode = deciding.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write the receipt")
    mode.add_argument("--check", action="store_true", help="decide again and compare")
    deciding.add_argument("--jobs", type=int, default=1, help=f"processes, at most {MAX_JOBS}")
    writing = commands.add_parser("witness", help="write the Witness/v2 file")
    writing.add_argument("out", type=Path)
    args = parser.parse_args(argv)
    if args.command == "witness":
        with atomic_output_file(args.out) as temporary:
            temporary.write_text(
                yaml.safe_dump(document(build()), sort_keys=False), encoding="utf-8"
            )
        return 0
    found = receipt(jobs=args.jobs)
    failed = problems(found)
    for problem in failed:
        print(f"diamond_staircases: {problem}", file=sys.stderr)
    if args.check:
        retained = json.loads(RECEIPT.read_text(encoding="utf-8"))
        if _stable(retained) != _stable(found):
            print("diamond_staircases: the retained receipt differs", file=sys.stderr)
            return 1
    elif args.write:
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        with atomic_output_file(RECEIPT) as temporary:
            temporary.write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
    else:
        print(json.dumps(found, indent=1))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
