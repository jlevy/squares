#!/usr/bin/env python3
"""Evaluate wand125's closed-form lower bound a(N) exactly, and compare it with the record.

The packet retains ``intervals.json`` of wand125/square-packing ``problems/closed-form``
(closed-form-v1). Its README and SPEC.md section 1.1 state the theorem: for a non-square
N >= 49 with k = floor(sqrt(N)),

    s(N) >= a(N) = k + sup{delta in (0, 1] : (k + delta)^2 - 4 S*(delta) < N},

where S*(delta) is the largest certified saving alpha_i delta + beta_i over the 34
intervals I_i that contain delta. This program takes the theorem as given and decides,
in exact rational arithmetic, what it implies at each count. It decides nothing about the
measure certificate (the families and records), which is replay4d's and the structure
check's.

It reads the retained ``intervals.json.gz`` (and refuses bytes whose SHA-256 is not the
packet manifest's) and the front matter of ``packing/frontier/n-NNN.md``, and imports no
code of the source. It computes a(N) two ways that share only the parsed intervals:

- **Route A, the closed form.** For each interval the root
  a_i(N) = 2 alpha_i + sqrt(4 alpha_i^2 + N + 4 beta_i - 4 alpha_i k), capped at k + d1_i
  and kept only where it exceeds k + d0_i; a(N) is the largest, chosen by exact sign
  determination in Q(sqrt(R1), sqrt(R2)).
- **Route B, the theorem's own inequality.** No root is formed. For a number b,
  a(N) > b exactly when some interval holds a delta > b - k with
  T_i(delta) = (k + delta)^2 - 4(alpha_i delta + beta_i) < N; since T_i increases in
  delta for k >= 7 (checked), that is T_i(max(b - k, d0_i)) < N with
  max(b - k, d0_i) < d1_i. Irrational b is enclosed by rational intervals that are
  refined until the decision is forced.

Route B checks Route A's value to 30 decimal places at every count, and both routes
decide every comparison with the case bounds; any disagreement stops the run. Each case
bound is read exactly: its ``exact_form`` (a closed expression in integers, +, -, *, /,
sqrt and floor, parsed through a whitelisted syntax tree), Nagamochi's formula where the
reported lane carries the ``nagamochi`` kind with no exact form, and otherwise its decimal
``value``.

Run from ``packing/`` with the project interpreter::

    uv run --frozen --all-extras --group dev python -I \\
        resources/web/wand125-closed-form-2026-10-14/evaluation/closed_form_bounds.py \\
        --out resources/web/wand125-closed-form-2026-10-14/evaluation/outputs/bounds.json

``--claims-max`` (default 3600) is how far the source's comparisons with Nagamochi's and
Karakus's formulas and the k^2 - j values are checked count by count, as a diagnostic of
statements the source proves for every N. ``--author-table`` reads the site table at the
pin from a checkout (its digest must be the manifest's) and ``--author-a-of-n`` the JSON
the source's ``a_of_n.py --json --digits 30`` printed, and compares them with Route A.
"""

from __future__ import annotations

import argparse
import ast
import csv
import gzip
import hashlib
import json
import re
import sys
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise
from math import ceil, floor, isqrt
from pathlib import Path
from typing import Any

sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
PACKING = PACKET.parents[2]
UPSTREAM = PACKET / "square-packing"
MANIFEST = PACKET / "acquisition" / "upstream-subtree.sha256"
INTERVALS = "problems/closed-form/intervals.json"
AUTHOR_TABLE = "site/public/data/papers/closed-form-table.csv"
FRONTIER = PACKING / "frontier"

#: Enclosure precision schedule, in binary digits after the point.
BITS = (96, 384, 1536, 6144, 24576)
#: Decimal places at which Route B confirms Route A's value.
CONFIRM_DIGITS = 30

type Enclosure = tuple[Fraction, Fraction]


class UndecidedError(ArithmeticError):
    """A comparison that the enclosure schedule did not force."""


class RefineError(ArithmeticError):
    """An enclosure too wide for the operation; retry at higher precision."""


# ------------------------------------------------------------------------------- inputs


def manifest_digests() -> dict[str, str]:
    """The packet manifest's SHA-256 for each upstream path."""
    digests: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, _, name = line.partition("  ")
        digests[name.removeprefix("./")] = digest
    return digests


def read_pinned(path: str, data: bytes) -> bytes:
    """``data`` if its SHA-256 is the manifest's digest for ``path``, else refuse."""
    want = manifest_digests()[path]
    got = hashlib.sha256(data).hexdigest()
    if got != want:
        msg = f"{path}: SHA-256 {got} is not the manifest's {want}"
        raise ValueError(msg)
    return data


_RATIONAL = re.compile(r"-?\d+(?:/[1-9]\d*)?")


def rational(text: object, where: str) -> Fraction:
    if not isinstance(text, str) or _RATIONAL.fullmatch(text) is None:
        msg = f"{where}: not an integer or p/q string: {text!r}"
        raise ValueError(msg)
    return Fraction(text)


@dataclass(frozen=True)
class Interval:
    """One certified interval: S_i(delta) = alpha delta + beta on (d0 or [d0, d1]."""

    index: int
    d0: Fraction
    d1: Fraction
    open_left: bool
    alpha: Fraction
    beta: Fraction

    def saving(self, delta: Fraction) -> Fraction:
        return self.alpha * delta + self.beta

    def t(self, k: int, delta: Fraction) -> Fraction:
        """T_i(delta) = (k + delta)^2 - 4 S_i(delta), the measure's total mass."""
        return (k + delta) ** 2 - 4 * self.saving(delta)

    def contains(self, delta: Fraction) -> bool:
        low = delta > self.d0 if self.open_left else delta >= self.d0
        return low and delta <= self.d1


def load_intervals() -> list[Interval]:
    stored = UPSTREAM / (INTERVALS + ".gz")
    data = read_pinned(INTERVALS, gzip.decompress(stored.read_bytes()))
    document = json.loads(data, parse_float=str)
    if document.get("schema") != "closed-form-intervals/v1":
        msg = f"unexpected schema {document.get('schema')!r}"
        raise ValueError(msg)
    out: list[Interval] = []
    for row in document["intervals"]:
        where = f"interval {row['index']}"
        if row["closed_right"] is not True or not isinstance(row["open_left"], bool):
            msg = f"{where}: every interval must be closed on the right"
            raise ValueError(msg)
        line = row["certified_line"]
        out.append(
            Interval(
                index=int(row["index"]),
                d0=rational(row["d0"], where),
                d1=rational(row["d1"], where),
                open_left=row["open_left"],
                alpha=rational(line["alpha"], where),
                beta=rational(line["beta"], where),
            )
        )
    return out


# ------------------------------------------------------------ facts about the intervals


def interval_facts(intervals: Sequence[Interval]) -> dict[str, Any]:
    """Coverage of (0, 1] (SPEC.md 7.2), monotonicity of T_i for k >= 7, and the margins
    the source's corollaries use, each decided exactly."""
    problems: list[str] = []
    ordered = sorted(intervals, key=lambda iv: (iv.d0, iv.d1))
    if [iv.index for iv in intervals] != list(range(1, len(intervals) + 1)):
        problems.append("indices are not 1..n in order")
    if ordered[0].d0 != 0 or not ordered[0].open_left:
        problems.append("the first interval does not start at 0, open")
    if ordered[-1].d1 != 1:
        problems.append("the last interval does not end at 1")
    for left, right in pairwise(ordered):
        if left.d1 != right.d0:
            problems.append(f"gap or overlap between I{left.index} and I{right.index}")
        if not left.contains(left.d1) and not right.contains(right.d0):
            problems.append(f"shared endpoint {left.d1} belongs to neither interval")
    problems.extend(
        f"I{iv.index} is empty or reversed" for iv in intervals if not iv.d0 < iv.d1
    )
    # T_i'(delta) = 2(k + delta) - 4 alpha_i >= 2 * 7 - 4 alpha_i for k >= 7, delta >= 0.
    problems.extend(
        f"T_{iv.index} is not increasing for k = 7"
        for iv in intervals
        if not 2 * 7 - 4 * iv.alpha > 0
    )
    margins = [
        (iv.saving(d) - d / 2, iv.index, d)
        for iv in intervals
        for d in (iv.d0, iv.d1)
        if d >= Fraction(1, 50)
    ]
    least = min(margins)
    first = intervals[0]
    s_at_one = max(iv.saving(Fraction(1)) for iv in intervals if iv.contains(Fraction(1)))
    if first.beta != 0 or not first.alpha > Fraction(1, 2):
        problems.append("I1's line is not alpha delta with alpha > 1/2")
    if not least[0] > 0:
        problems.append("a certified line is not above delta/2 at an end with delta >= 1/50")
    if not s_at_one > Fraction(3, 4):
        problems.append("S*(1) is not above 3/4")
    return {
        "intervals": len(intervals),
        "covers_0_1": not [p for p in problems if "gap" in p or "first" in p or "last" in p],
        "max_alpha": decimal(max(iv.alpha for iv in intervals), 9),
        "t_increasing_for_k_ge_7": all(2 * 7 - 4 * iv.alpha > 0 for iv in intervals),
        "least_margin_over_half_delta_for_delta_ge_1_50": {
            "value": decimal(least[0], 9),
            "interval": least[1],
            "delta": str(least[2]),
        },
        "interval_1_alpha_minus_half": decimal(first.alpha - Fraction(1, 2), 9),
        "s_star_at_1": decimal(s_at_one, 9),
        "s_star_at_1_exceeds_3_4": s_at_one > Fraction(3, 4),
        "s_star_at_1_exceeds_1": s_at_one > 1,
        "problems": problems,
    }


# --------------------------------------------------------------------- exact arithmetic


def floor_sqrt(q: Fraction, bits: int) -> Fraction:
    """A rational <= sqrt(q), within 2^-bits."""
    scale = 1 << bits
    return Fraction(isqrt(floor(q * scale * scale)), scale)


def ceil_sqrt(q: Fraction, bits: int) -> Fraction:
    """A rational >= sqrt(q), within 2^-bits."""
    scale = 1 << bits
    m = ceil(q * scale * scale)
    r = isqrt(m)
    if r * r < m:
        r += 1
    return Fraction(r, scale)


def sign(x: Fraction) -> int:
    return (x > 0) - (x < 0)


def sign1(x: Fraction, y: Fraction, r: Fraction) -> int:
    """The exact sign of x + y sqrt(r), r >= 0."""
    if y == 0 or r == 0:
        return sign(x)
    sy = sign(y)
    if sign(x) in (0, sy):
        return sy
    gap = y * y * r - x * x
    return sy if gap > 0 else (sign(x) if gap < 0 else 0)


@dataclass(frozen=True)
class Value:
    """A rational q, or the quadratic irrational 2 alpha + sqrt(r) (``r`` not None)."""

    q: Fraction
    r: Fraction | None = None

    @classmethod
    def root(cls, alpha: Fraction, r: Fraction) -> Value:
        return cls(2 * alpha, r)

    def enclose(self, bits: int) -> Enclosure:
        if self.r is None:
            return self.q, self.q
        return self.q + floor_sqrt(self.r, bits), self.q + ceil_sqrt(self.r, bits)

    def exact_form(self) -> str:
        if self.r is None:
            return str(self.q)
        return f"{self.q} + sqrt({self.r})"


def compare(u: Value, v: Value) -> int:
    """The exact sign of u - v."""
    if u.r is None and v.r is None:
        return sign(u.q - v.q)
    if v.r is None:
        return sign1(u.q - v.q, Fraction(1), u.r or Fraction(0))
    if u.r is None:
        return -compare(v, u)
    # c + sqrt(R1) - sqrt(R2), with A = c + sqrt(R1)
    c, r1, r2 = u.q - v.q, u.r, v.r
    s_a = sign1(c, Fraction(1), r1)
    if s_a <= 0:
        return -1 if (s_a < 0 or r2 > 0) else 0
    # A > 0: sign(A^2 - R2) = sign((c^2 + R1 - R2) + 2c sqrt(R1))
    return sign1(c * c + r1 - r2, 2 * c, r1)


def decimal(x: Fraction, digits: int) -> str:
    """``x`` rounded down at ``digits`` places."""
    scale = 10**digits
    n = floor(x * scale)
    s = str(abs(n)).rjust(digits + 1, "0")
    body = f"{s[:-digits]}.{s[-digits:]}" if digits else s
    return ("-" if n < 0 else "") + body


def value_decimal(v: Value, digits: int, *, up: bool = False) -> Fraction:
    """``v`` rounded down (or up) at ``digits`` decimal places, exactly."""
    scale = 10**digits
    for bits in BITS:
        lo, hi = v.enclose(bits)
        a, b = floor(lo * scale), floor(hi * scale)
        if a == b:
            exact_point = v.r is None and lo * scale == a
            return Fraction(a + (1 if up and not exact_point else 0), scale)
    raise UndecidedError(f"cannot round {v.exact_form()} at {digits} places")


# ------------------------------------------------------ expressions of the case records


class Expr:
    """A case-record bound: an exact expression enclosed at any precision."""

    def __init__(self, text: str, enclose: Callable[[int], Enclosure]) -> None:
        self.text = text
        self._enclose = enclose

    def enclose(self, bits: int) -> Enclosure:
        return self._enclose(bits)

    def exact(self) -> Fraction | None:
        lo, hi = self.enclose(BITS[0])
        return lo if lo == hi else None


def _mul(a: Enclosure, b: Enclosure) -> Enclosure:
    p = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return min(p), max(p)


def _node(node: ast.AST, bits: int) -> Enclosure:  # noqa: PLR0911
    if isinstance(node, ast.Constant) and type(node.value) is int:
        return Fraction(node.value), Fraction(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        lo, hi = _node(node.operand, bits)
        return -hi, -lo
    if isinstance(node, ast.BinOp):
        a, b = _node(node.left, bits), _node(node.right, bits)
        if isinstance(node.op, ast.Add):
            return a[0] + b[0], a[1] + b[1]
        if isinstance(node.op, ast.Sub):
            return a[0] - b[1], a[1] - b[0]
        if isinstance(node.op, ast.Mult):
            return _mul(a, b)
        if isinstance(node.op, ast.Div):
            if b[0] <= 0 <= b[1]:
                raise RefineError
            return _mul(a, (1 / b[1], 1 / b[0]))
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in {"sqrt", "floor"}
        and len(node.args) == 1
        and not node.keywords
    ):
        lo, hi = _node(node.args[0], bits)
        if node.func.id == "sqrt":
            if lo < 0:
                raise RefineError
            return floor_sqrt(lo, bits), ceil_sqrt(hi, bits)
        if floor(lo) != floor(hi):
            raise RefineError
        return Fraction(floor(lo)), Fraction(floor(lo))
    msg = f"unsupported syntax in an exact form: {ast.dump(node)}"
    raise ValueError(msg)


_IMPLICIT = re.compile(r"(?<=[0-9)])\s*(?=sqrt\b|\()")


def parse_form(text: str) -> Expr:
    """An ``exact_form`` such as ``1/2 + sqrt(106 - floor(sqrt(106)) + 1/4)`` or
    ``7 + (1/2)sqrt(2)``; implicit multiplication before ``sqrt`` or ``(`` is read as ``*``."""
    tree = ast.parse(_IMPLICIT.sub("*", text.strip()), mode="eval")

    def enclose(bits: int) -> Enclosure:
        for attempt in BITS:
            if attempt < bits:
                continue
            try:
                return _node(tree.body, attempt)
            except RefineError:
                continue
        raise UndecidedError(f"cannot enclose {text}")

    enclose(BITS[0])  # parse errors surface here
    return Expr(text, enclose)


def value_expr(v: Value, text: str) -> Expr:
    return Expr(text, v.enclose)


def nagamochi(n: int) -> Value:
    """min(ceil(sqrt n), 1 + sqrt(n - 2 floor(sqrt n) + 1)), Nagamochi's Theorem 2 value."""
    k = isqrt(n)
    top = Fraction(k if k * k == n else k + 1)
    root = Value(Fraction(1), Fraction(n - 2 * k + 1))
    return root if compare(root, Value(top)) < 0 else Value(top)


def karakus(n: int) -> Value:
    """1/2 + sqrt(n - floor(sqrt n) + 1/4), Karakus's Corollary 6.2 value."""
    return Value(Fraction(1, 2), Fraction(n - isqrt(n)) + Fraction(1, 4))


# ------------------------------------------------------------- route A: the closed form


def route_a(n: int, intervals: Sequence[Interval]) -> tuple[int, Value]:
    """The largest admissible capped root, with the first interval that attains it."""
    k = isqrt(n)
    best: tuple[int, Value] | None = None
    for iv in intervals:
        r = 4 * iv.alpha**2 + n + 4 * iv.beta - 4 * iv.alpha * k
        if r < 0:
            continue
        root = Value.root(iv.alpha, r)
        if compare(root, Value(k + iv.d0)) <= 0:
            continue
        cand = Value(k + iv.d1) if compare(root, Value(k + iv.d1)) > 0 else root
        if best is None or compare(cand, best[1]) > 0:
            best = (iv.index, cand)
    if best is None:
        msg = f"no admissible interval at N = {n}"
        raise ArithmeticError(msg)
    return best


def relation_a(a: Value, b: Expr) -> str:
    """'>', '=' or '<' for a(N) against b, by Route A's value."""
    exact = b.exact()
    if exact is not None:
        return ">=<"[1 - compare(a, Value(exact))]
    for bits in BITS:
        alo, ahi = a.enclose(bits)
        blo, bhi = b.enclose(bits)
        if alo > bhi:
            return ">"
        if ahi < blo:
            return "<"
    raise UndecidedError(f"route A cannot separate a(N) = {a.exact_form()} from {b.text}")


# -------------------------------------------------------------- route B: the inequality


def _tri_and(*verdicts: bool | None) -> bool | None:
    """Three-valued conjunction: False beats undecided (None), which beats True."""
    if False in verdicts:
        return False
    return None if None in verdicts else True


def _less(lo: Fraction, hi: Fraction, bound: Fraction) -> bool | None:
    """Whether the number enclosed by [lo, hi] is < bound: True, False, or undecided."""
    if hi < bound:
        return True
    if lo >= bound:
        return False
    return None


def exceeds(n: int, b: Expr, intervals: Sequence[Interval]) -> bool:
    """Whether a(N) > b: some interval holds delta > b - k with T_i(delta) < N."""
    k = isqrt(n)
    for bits in BITS:
        lo, hi = b.enclose(bits)
        undecided = False
        for iv in intervals:
            mlo, mhi = max(lo - k, iv.d0), max(hi - k, iv.d0)
            inside = _less(mlo, mhi, iv.d1)
            below = _less(iv.t(k, mlo), iv.t(k, mhi), Fraction(n))
            verdict = _tri_and(inside, below)
            if verdict:
                return True
            undecided = undecided or verdict is None
        if not undecided:
            return False
    raise UndecidedError(f"route B cannot decide a({n}) > {b.text}")


def attains(n: int, b: Fraction, intervals: Sequence[Interval]) -> bool:
    """For rational b, whether a(N) >= b."""
    if exceeds(n, Expr(str(b), lambda _bits: (b, b)), intervals):
        return True
    x = b - isqrt(n)
    return any(iv.d0 < x <= iv.d1 and iv.t(isqrt(n), x) <= n for iv in intervals)


def relation_b(n: int, b: Expr, intervals: Sequence[Interval]) -> str:
    """'>', '=' or '<' (that is, a(N) <= b and a(N) != b by route A) for a(N) against b."""
    if exceeds(n, b, intervals):
        return ">"
    exact = b.exact()
    if exact is not None and attains(n, exact, intervals):
        return "="
    return "<="


def relation(n: int, a: Value, b: Expr, intervals: Sequence[Interval]) -> str:
    """Both routes' verdict; they must agree."""
    ra, rb = relation_a(a, b), relation_b(n, b, intervals)
    if not (ra == rb or (rb == "<=" and ra == "<")):
        msg = f"routes disagree at N = {n} against {b.text}: A {ra}, B {rb}"
        raise ArithmeticError(msg)
    return ra


def confirm_value(n: int, a: Value, intervals: Sequence[Interval]) -> tuple[Fraction, Fraction]:
    """Route B's check of Route A's value: lo <= a(N) <= hi, hi - lo <= 10^-CONFIRM_DIGITS."""
    lo = value_decimal(a, CONFIRM_DIGITS)
    hi = value_decimal(a, CONFIRM_DIGITS, up=True)
    if not attains(n, lo, intervals):
        msg = f"route B: a({n}) is not >= {lo}"
        raise ArithmeticError(msg)
    if exceeds(n, Expr(str(hi), lambda _bits: (hi, hi)), intervals):
        msg = f"route B: a({n}) exceeds {hi}"
        raise ArithmeticError(msg)
    return lo, hi


# --------------------------------------------------------------------- the case records


LANES = (
    "reported_lower_bound",
    "verified_lower_bound",
    "verified_upper_bound",
    "reported_upper_bound",
)


def parse_case(path: Path) -> dict[str, Any]:
    sys.path.insert(0, str(PACKING))
    from devtools.check_source_coverage import parse_case as project_parse  # noqa: PLC0415

    return project_parse(path)


def bound(n: int, lane: str, record: dict[str, Any]) -> tuple[Expr, str]:
    """The lane's bound as an exact expression, and how it was read."""
    form, kind, value = record.get("exact_form"), record.get("kind"), record.get("value")
    if form:
        return parse_form(str(form)), "exact_form"
    if lane == "reported_lower_bound" and kind == "nagamochi":
        v = nagamochi(n)
        return value_expr(v, f"nagamochi({n}) = {v.exact_form()}"), "nagamochi formula"
    exact = Fraction(str(value))
    return Expr(str(value), lambda _bits: (exact, exact)), "decimal value"


def value_matches(record: dict[str, Any], b: Expr) -> bool:
    """Whether the lane's printed ``value`` is the bound to the places it prints."""
    text = str(record.get("value"))
    places = len(text.partition(".")[2])
    printed = Fraction(text)
    lo, hi = b.enclose(BITS[2])
    unit = Fraction(1, 10**places)
    return printed - unit <= lo and hi <= printed + unit


def holders(record: dict[str, Any]) -> dict[str, Any]:
    keep = ("kind", "source_key", "proved_by", "evidence")
    return {key: record[key] for key in keep if record.get(key)}


# ------------------------------------------------------------------------------- driver


def ranges(ns: Iterable[int]) -> str:
    out: list[str] = []
    run: list[int] = []
    for n in sorted(ns):
        if run and n == run[-1] + 1:
            run.append(n)
            continue
        if run:
            out.append(f"{run[0]}-{run[-1]}" if len(run) > 1 else str(run[0]))
        run = [n]
    if run:
        out.append(f"{run[0]}-{run[-1]}" if len(run) > 1 else str(run[0]))
    return ", ".join(out)


def case_rows(lo: int, hi: int, intervals: Sequence[Interval]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in range(lo, hi + 1):
        k = isqrt(n)
        case = parse_case(FRONTIER / f"n-{n:03d}.md")
        row: dict[str, Any] = {"n": n, "k": k}
        if k * k == n:
            row["square"] = True
            rows.append(row)
            continue
        index, a = route_a(n, intervals)
        a_lo, _ = confirm_value(n, a, intervals)
        row |= {
            "interval": index,
            "form": "cap k + d1" if a.r is None else "root",
            "a_floor_30": decimal(a_lo, CONFIRM_DIGITS),
            "exact_form_chars": len(a.exact_form()),
            "vs_nagamochi": relation(n, a, value_expr(nagamochi(n), "F"), intervals),
            "vs_karakus": relation(n, a, value_expr(karakus(n), "K"), intervals),
        }
        for lane in LANES:
            record = case[lane]
            b, read = bound(n, lane, record)
            lb_lo, _ = b.enclose(BITS[2])
            row[lane] = {
                "value": str(record.get("value")),
                "read_as": read,
                "printed_value_consistent": value_matches(record, b),
                "relation": relation(n, a, b, intervals),
                "a_minus_bound_approx": decimal(value_decimal(a, 15) - lb_lo, 12),
            } | holders(record)
        row["case_status"] = case.get("status")
        rows.append(row)
    return rows


def claims_check(hi: int, intervals: Sequence[Interval]) -> dict[str, Any]:
    """The source's comparisons and top-of-block values, count by count to ``hi``."""
    not_above_f: list[int] = []
    not_above_k: list[int] = []
    tops: dict[int, list[int]] = {1: [], 2: [], 3: [], 4: []}
    checked = 0
    for n in range(49, hi + 1):
        k = isqrt(n)
        if k * k == n:
            continue
        checked += 1
        _, a = route_a(n, intervals)
        if compare(a, nagamochi(n)) <= 0:
            not_above_f.append(n)
        if compare(a, karakus(n)) <= 0:
            not_above_k.append(n)
        j = (k + 1) ** 2 - n
        if j in tops and compare(a, Value(Fraction(k + 1))) == 0:
            tops[j].append(n)
    blocks = [m * m - 1 for m in range(8, isqrt(hi + 1) + 1) if m * m - 1 <= hi]
    expect_f = sorted(
        x for m in range(8, isqrt(hi + 2) + 1) for x in (m * m - 1, m * m - 2) if x <= hi
    )
    return {
        "range": f"49-{hi}",
        "non_square_counts": checked,
        "a_not_above_nagamochi": ranges(not_above_f),
        "a_not_above_nagamochi_is_exactly_k2_minus_1_and_2": not_above_f == expect_f,
        "a_not_above_karakus": ranges(not_above_k),
        "a_not_above_karakus_is_exactly_k2_minus_1": not_above_k == blocks,
        "a_equals_k_plus_1_at": {f"(k+1)^2-{j}": ranges(ns) for j, ns in tops.items()},
    }


def compare_author_table(path: Path, intervals: Sequence[Interval]) -> dict[str, Any]:
    data = read_pinned(AUTHOR_TABLE, path.read_bytes())
    rows = list(csv.DictReader(data.decode("utf-8").splitlines()))
    floor_match = interval_match = compared = 0
    differ: list[str] = []
    for row in rows:
        n = int(row["N"])
        if n < 49 or isqrt(n) ** 2 == n or not row["a_N"]:
            continue
        compared += 1
        index, a = route_a(n, intervals)
        down = decimal(value_decimal(a, 9), 9)
        floor_match += row["a_N"] == down
        interval_match += row["a_interval"] == str(index)
        if row["a_N"] != down or row["a_interval"] != str(index):
            differ.append(
                f"{n}: table {row['a_N']} (I{row['a_interval']}), here {down} (I{index})"
            )
    return {
        "table": AUTHOR_TABLE,
        "compared": compared,
        "a_N_equals_floor_9": floor_match,
        "interval_equal": interval_match,
        "differences": differ[:40],
        "difference_count": len(differ),
        "note": "the table prints a(N) rounded down at nine places "
        "(site/tools/closed_form_table.py)",
    }


def compare_author_a_of_n(path: Path, intervals: Sequence[Interval]) -> dict[str, Any]:
    data = path.read_bytes()
    rows = json.loads(gzip.decompress(data) if path.suffix == ".gz" else data)
    same = compared = 0
    differ: list[str] = []
    for row in rows:
        n = int(row["N"])
        if not row.get("claim") or row.get("interval") is None:
            continue
        compared += 1
        index, a = route_a(n, intervals)
        mine = decimal(value_decimal(a, CONFIRM_DIGITS), CONFIRM_DIGITS)
        if row["a_N_rounded_down"] == mine and row["interval"] == index:
            same += 1
        else:
            differ.append(
                f"{n}: a_of_n {row['a_N_rounded_down']} (I{row['interval']}), "
                f"here {mine} (I{index})"
            )
    return {"compared": compared, "identical": same, "differences": differ[:40]}


def controls(intervals: Sequence[Interval]) -> dict[str, bool]:
    """Mutations this program must refuse; each entry is True when it was refused."""
    out: dict[str, bool] = {}
    stored = gzip.decompress((UPSTREAM / (INTERVALS + ".gz")).read_bytes())
    flipped = stored.replace(b'"index": 34', b'"index": 35', 1)
    try:
        read_pinned(INTERVALS, flipped)
        out["a changed intervals.json is refused by its digest"] = False
    except ValueError:
        out["a changed intervals.json is refused by its digest"] = True
    tiny = Fraction(1, 10**25)
    refused_value = True
    for n in (50, 104, 230, 319):
        _, a = route_a(n, intervals)
        try:
            confirm_value(n, Value(a.q + tiny, a.r), intervals)
            refused_value = False
        except ArithmeticError:
            pass
    out["route B refuses a(N) + 1e-25 at N = 50, 104, 230, 319"] = refused_value
    _, top = route_a(118, intervals)
    just_above = 11 + Fraction(1, 10**40)
    above = Expr("11 + 1e-40", lambda _bits: (just_above, just_above))
    out["a(118) = 11 is equal to 11 and below 11 + 1e-40"] = (
        relation(118, top, value_expr(Value(Fraction(11)), "11"), intervals) == "="
        and relation(118, top, above, intervals) == "<"
    )
    weaker = [
        Interval(iv.index, iv.d0, iv.d1, iv.open_left, iv.alpha, iv.beta - Fraction(1, 10**6))
        for iv in intervals
    ]
    _, base = route_a(230, intervals)
    _, low = route_a(230, weaker)
    out["lowering every beta by 1e-6 lowers a(230)"] = compare(low, base) < 0
    return out


def summarize(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    open_rows = [r for r in rows if not r.get("square")]
    out: dict[str, Any] = {"non_square_counts": len(open_rows)}
    for lane in LANES:
        by: dict[str, list[int]] = {}
        for r in open_rows:
            by.setdefault(r[lane]["relation"], []).append(r["n"])
        out[lane] = {rel: {"count": len(ns), "n": ranges(ns)} for rel, ns in sorted(by.items())}
    out["settles"] = ranges(
        r["n"] for r in open_rows if r["verified_upper_bound"]["relation"] == "="
    )
    out["settles_an_open_case"] = ranges(
        r["n"]
        for r in open_rows
        if r["verified_upper_bound"]["relation"] == "=" and r["case_status"] != "proved"
    )
    out["above_an_upper_bound"] = ranges(
        r["n"]
        for r in open_rows
        if ">" in (r["verified_upper_bound"]["relation"], r["reported_upper_bound"]["relation"])
    )
    out["printed_value_inconsistent"] = sorted(
        f"{r['n']} {lane}"
        for r in open_rows
        for lane in LANES
        if not r[lane]["printed_value_consistent"]
    )
    return out


def write_table(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    """One tab-separated line per count: a(N), each lane's bound, holder and relation."""
    head = [
        "n",
        "k",
        "interval",
        "form",
        "a_floor_15",
        "reported_lb",
        "reported_lb_kind",
        "reported_lb_source",
        "rel_reported_lb",
        "verified_lb",
        "verified_lb_evidence",
        "rel_verified_lb",
        "verified_ub",
        "rel_verified_ub",
        "reported_ub",
        "rel_reported_ub",
        "case_status",
    ]
    lines = ["\t".join(head)]
    for r in rows:
        if r.get("square"):
            continue
        rl, vl = r["reported_lower_bound"], r["verified_lower_bound"]
        vu, ru = r["verified_upper_bound"], r["reported_upper_bound"]
        cells = [
            r["n"],
            r["k"],
            r["interval"],
            r["form"],
            r["a_floor_30"][: r["a_floor_30"].index(".") + 16],
            rl["value"],
            rl.get("kind", ""),
            rl.get("source_key", ""),
            rl["relation"],
            vl["value"],
            " ".join(vl.get("evidence", [])),
            vl["relation"],
            vu["value"],
            vu["relation"],
            ru["value"],
            ru["relation"],
            r["case_status"],
        ]
        lines.append("\t".join(str(c) for c in cells))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--first", type=int, default=49)
    parser.add_argument("--last", type=int, default=324)
    parser.add_argument("--claims-max", type=int, default=3600)
    parser.add_argument(
        "--author-table", type=Path, help="closed-form-table.csv from a checkout at the pin"
    )
    parser.add_argument(
        "--author-a-of-n", type=Path, help="a_of_n.py 49-N --json --digits 30 output"
    )
    parser.add_argument(
        "--exact", type=Path, help="write each count's exact a(N) to this JSON file"
    )
    parser.add_argument("--out", type=Path, help="write the receipt here")
    parser.add_argument("--table", type=Path, help="write the per-count table (TSV) here")
    args = parser.parse_args(argv)

    intervals = load_intervals()
    facts = interval_facts(intervals)
    print(f"intervals: {facts['intervals']}, problems: {facts['problems'] or 'none'}")
    print(
        f"S*(1) = {facts['s_star_at_1']}..., least margin over delta/2 (delta >= 1/50): "
        f"{facts['least_margin_over_half_delta_for_delta_ge_1_50']}"
    )
    rows = case_rows(args.first, args.last, intervals)
    summary = summarize(rows)
    claims = claims_check(args.claims_max, intervals)
    receipt: dict[str, Any] = {
        "schema": "closed-form-bounds-evaluation/v1",
        "program": "evaluation/closed_form_bounds.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "intervals_json_sha256": manifest_digests()[INTERVALS],
        "python": sys.version.split()[0],
        "interval_facts": facts,
        "summary": summary,
        "claims_check": claims,
        "controls": controls(intervals),
    }
    if args.author_table:
        receipt["author_table"] = compare_author_table(args.author_table, intervals)
    if args.author_a_of_n:
        receipt["author_a_of_n"] = compare_author_a_of_n(args.author_a_of_n, intervals)
    if args.exact:
        exact = {
            str(r["n"]): route_a(r["n"], intervals)[1].exact_form()
            for r in rows
            if not r.get("square")
        }
        args.exact.write_text(json.dumps(exact, indent=0) + "\n", encoding="utf-8")
    for lane in LANES:
        print(
            f"{lane}: "
            + "; ".join(f"{rel} {v['count']} ({v['n']})" for rel, v in summary[lane].items())
        )
    for key in (
        "settles",
        "settles_an_open_case",
        "above_an_upper_bound",
        "printed_value_inconsistent",
    ):
        print(f"{key}: {summary[key] or 'none'}")
    for key, value in claims.items():
        print(f"claims {key}: {value}")
    for key, refused in receipt["controls"].items():
        print(f"control {'refused' if refused else 'NOT REFUSED'}: {key}")
    for key in ("author_table", "author_a_of_n"):
        if key in receipt:
            print(
                f"{key}: "
                + json.dumps({k: v for k, v in receipt[key].items() if k != "differences"})
            )
    if args.table:
        write_table(args.table, rows)
    if args.out:
        head = json.dumps(receipt, indent=1, ensure_ascii=False)[:-2]
        body = ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows)
        args.out.write_text(f'{head},\n "rows": [\n{body}\n ]\n}}\n', encoding="utf-8")
    return 0 if not facts["problems"] and all(receipt["controls"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
