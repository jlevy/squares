#!/usr/bin/env python3
"""a(N) from the definition of SPEC.md section 1.1 alone, by exact bisection.

wand125's problems/closed-form (closed-form-v1) states, for a non-square N >= 49 with
k = floor(sqrt(N)),

    s(N) >= a(N) = k + sup{delta in (0, 1] : (k + delta)^2 - 4 S*(delta) < N},

where S*(delta) is the largest certified saving alpha_i delta + beta_i over the intervals
of intervals.json that contain delta. This program encloses that supremum from the
definition and nothing else: no closed form, no square root. On each interval I_i the
set {delta in I_i : T_i(delta) < N}, with T_i(delta) = (k + delta)^2 - 4(alpha_i delta +
beta_i), is an initial segment of I_i because T_i is strictly increasing there (the program
checks 2(k + d0_i) - 4 alpha_i > 0 at every count). So its supremum is d1_i when
T_i(d1_i) < N, nothing when T_i(d0_i) >= N (whether or not d0_i belongs to I_i), and
otherwise the root of T_i = N in (d0_i, d1_i), which bisection encloses in rational
arithmetic. The supremum over (0, 1] is the largest of these, decided by refining the
enclosures until they separate or an exact tie is established.

It reads the retained intervals.json.gz (refused unless its SHA-256 is the packet
manifest's) and, to compare, the retained output of the source's a_of_n.py
(evaluation/outputs/a_of_n-49-3600.json.gz) and the intake evaluation's receipt
(evaluation/outputs/bounds.json). For every count it decides whether each printed 30-place
value v satisfies v <= a(N) < v + 10^-30, refining until it can. It also decides the facts
about the intervals that the corollaries use.

Run from packing/ with the project interpreter:

    uv run --frozen --all-extras --group dev python -I \\
        resources/web/wand125-closed-form-2026-10-14/review/a_of_n_by_definition.py \\
        --out resources/web/wand125-closed-form-2026-10-14/review/outputs/a_by_definition.json

It decides nothing about the certificate: it takes the theorem as given and derives what
the theorem says at each count.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise
from math import floor, isqrt
from pathlib import Path
from typing import Any

sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
UPSTREAM = PACKET / "square-packing"
MANIFEST = PACKET / "acquisition" / "upstream-subtree.sha256"
INTERVALS = "problems/closed-form/intervals.json"
AUTHOR_A_OF_N = PACKET / "evaluation" / "outputs" / "a_of_n-49-3600.json.gz"
EVALUATION = PACKET / "evaluation" / "outputs" / "bounds.json"

PLACES = 30
START_BITS = 128
MAX_BITS = 4096

_RATIONAL = re.compile(r"-?\d+(?:/[1-9]\d*)?")


def rational(text: object, where: str) -> Fraction:
    if not isinstance(text, str) or _RATIONAL.fullmatch(text) is None:
        msg = f"{where}: not an integer or p/q string: {text!r}"
        raise ValueError(msg)
    return Fraction(text)


def manifest_digest(name: str) -> str:
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, _, path = line.partition("  ")
        if path.removeprefix("./") == name:
            return digest
    msg = f"{name} is not in the packet manifest"
    raise KeyError(msg)


@dataclass(frozen=True)
class Interval:
    index: int
    d0: Fraction
    d1: Fraction
    open_left: bool
    alpha: Fraction
    beta: Fraction

    def saving(self, delta: Fraction) -> Fraction:
        return self.alpha * delta + self.beta

    def t(self, k: int, delta: Fraction) -> Fraction:
        """T_i(delta) = (k + delta)^2 - 4 S_i(delta)."""
        return (k + delta) ** 2 - 4 * self.saving(delta)

    def contains(self, delta: Fraction) -> bool:
        low = delta > self.d0 if self.open_left else delta >= self.d0
        return low and delta <= self.d1


def load_intervals() -> tuple[list[Interval], str]:
    data = gzip.decompress((UPSTREAM / (INTERVALS + ".gz")).read_bytes())
    got = hashlib.sha256(data).hexdigest()
    want = manifest_digest(INTERVALS)
    if got != want:
        msg = f"intervals.json: SHA-256 {got} is not the manifest's {want}"
        raise SystemExit(msg)
    document = json.loads(data, parse_float=str)
    if document.get("schema") != "closed-form-intervals/v1":
        msg = f"unexpected schema {document.get('schema')!r}"
        raise SystemExit(msg)
    out: list[Interval] = []
    for row in document["intervals"]:
        where = f"interval {row['index']}"
        if row["closed_right"] is not True or not isinstance(row["open_left"], bool):
            msg = f"{where}: closed_right must be true and open_left a boolean"
            raise SystemExit(msg)
        out.append(
            Interval(
                index=int(row["index"]),
                d0=rational(row["d0"], where),
                d1=rational(row["d1"], where),
                open_left=bool(row["open_left"]),
                alpha=rational(row["certified_line"]["alpha"], where),
                beta=rational(row["certified_line"]["beta"], where),
            )
        )
    return out, got


# ---------------------------------------------------------------- facts about the intervals


def interval_facts(intervals: list[Interval]) -> dict[str, Any]:
    problems: list[str] = []
    ordered = sorted(intervals, key=lambda iv: iv.d0)
    if [iv.index for iv in ordered] != list(range(1, len(intervals) + 1)):
        problems.append("the intervals are not indexed 1..34 in order of d0")
    if ordered[0].d0 != 0 or not ordered[0].open_left:
        problems.append("the first interval is not (0, d1]")
    if ordered[-1].d1 != 1:
        problems.append("the last interval does not end at 1")
    for left, right in pairwise(ordered):
        if left.d1 != right.d0:
            problems.append(f"I{left.index} and I{right.index} do not share an endpoint")
        if not (left.contains(left.d1) or right.contains(right.d0)):
            problems.append(f"the endpoint {left.d1} belongs to no interval")
    for iv in intervals:
        if not iv.d0 < iv.d1:
            problems.append(f"I{iv.index} is empty")
        if not 2 * (7 + iv.d0) - 4 * iv.alpha > 0:
            problems.append(f"T_{iv.index} is not increasing at k = 7")
    # SPEC.md section 7.3: no interval has a grid transition delta = j/5 in its interior.
    transitions = [Fraction(j, 5) for j in range(1, 5)]
    interior = [
        f"I{iv.index} contains {t} in its interior"
        for iv in intervals
        for t in transitions
        if iv.d0 < t < iv.d1
    ]
    problems.extend(interior)
    margins = sorted(
        (iv.saving(d) - d / 2, iv.index, d)
        for iv in intervals
        for d in (iv.d0, iv.d1)
        if d >= Fraction(1, 50)
    )
    s_at_one = max(iv.saving(Fraction(1)) for iv in intervals if iv.contains(Fraction(1)))
    first = ordered[0]
    return {
        "intervals": len(intervals),
        "cover_0_1": not problems,
        "problems": problems,
        "max_alpha": decimal_down(max(iv.alpha for iv in intervals), 9),
        "max_alpha_below_1.7496": max(iv.alpha for iv in intervals) <= Fraction(17496, 10000),
        "interval_1_line_is_alpha_delta_with_alpha_above_half": first.beta == 0
        and first.alpha > Fraction(1, 2),
        "least_margin_over_half_delta_for_delta_ge_1_50": {
            "value": decimal_down(margins[0][0], 9),
            "interval": margins[0][1],
            "delta": str(margins[0][2]),
            "above_0.0226": margins[0][0] > Fraction(226, 10000),
        },
        "s_star_at_1": decimal_down(s_at_one, 9),
        "s_star_at_1_above_3_4": s_at_one > Fraction(3, 4),
        "transitions_j_5_are_endpoints": not interior,
    }


# ------------------------------------------------------------------- the supremum per count


def emit(line: str) -> None:
    sys.stdout.write(line + "\n")


def decimal_down(x: Fraction, places: int) -> str:
    scale = 10**places
    n = floor(x * scale)
    s = str(abs(n)).rjust(places + 1, "0")
    return ("-" if n < 0 else "") + f"{s[:-places]}.{s[-places:]}"


@dataclass
class Candidate:
    """An enclosure lo <= sup_i <= hi of one interval's supremum (exact when lo == hi)."""

    interval: Interval
    lo: Fraction
    hi: Fraction
    k: int
    n: int

    @property
    def exact(self) -> bool:
        return self.lo == self.hi

    def refine(self, bits: int) -> None:
        """Bisect until hi - lo <= 2^-bits, keeping T(lo) < N <= T(hi)."""
        if self.exact:
            return
        step = Fraction(1, 2**bits)
        while self.hi - self.lo > step:
            m = (self.lo + self.hi) / 2
            if self.interval.t(self.k, m) < self.n:
                self.lo = m
            else:
                self.hi = m

    def split_at(self, v: Fraction) -> int:
        """Decide the supremum against a rational v in the enclosure: -1, 0, 1 for <, =, >."""
        tv = self.interval.t(self.k, v)
        if tv == self.n:
            self.lo = self.hi = v
            return 0
        if tv < self.n:
            self.lo = v
            return 1
        self.hi = v
        return -1


def candidates(n: int, intervals: list[Interval]) -> list[Candidate]:
    k = isqrt(n)
    out: list[Candidate] = []
    for iv in intervals:
        if not 2 * (k + iv.d0) - 4 * iv.alpha > 0:
            msg = f"T_{iv.index} is not increasing at N = {n}"
            raise SystemExit(msg)
        if iv.t(k, iv.d1) < n:
            out.append(Candidate(iv, iv.d1, iv.d1, k, n))
        elif iv.t(k, iv.d0) < n:
            c = Candidate(iv, iv.d0, iv.d1, k, n)
            c.refine(START_BITS)
            out.append(c)
    return out


def separate(best: Candidate, other: Candidate) -> int:
    """1 if best's supremum is above other's, 0 if equal, -1 if below, refining as needed."""
    bits = START_BITS
    while True:
        if best.hi < other.lo:
            return -1
        if other.hi < best.lo:
            return 1
        if best.exact and other.exact:
            return 0 if best.lo == other.lo else (1 if best.lo > other.lo else -1)
        if best.exact:
            return -other.split_at(best.lo)
        if other.exact:
            return best.split_at(other.lo)
        bits *= 2
        if bits > MAX_BITS:
            msg = (
                f"cannot separate I{best.interval.index} from I{other.interval.index}"
                f" at N = {best.n}"
            )
            raise SystemExit(msg)
        best.refine(bits)
        other.refine(bits)


def supremum(n: int, intervals: list[Interval]) -> tuple[Candidate, list[int]]:
    """The largest per-interval supremum and the intervals that attain it."""
    cands = candidates(n, intervals)
    if not cands:
        msg = f"no delta works at N = {n}"
        raise SystemExit(msg)
    best = max(cands, key=lambda c: c.lo)
    ties = [best.interval.index]
    for other in cands:
        if other is best:
            continue
        rel = separate(best, other)
        if rel < 0:
            best, ties = other, [other.interval.index]
        elif rel == 0:
            ties.append(other.interval.index)
    return best, sorted(ties)


def floor_places(c: Candidate, places: int) -> str:
    """a(N) rounded down at `places`, refining until the enclosure decides it."""
    scale = 10**places
    bits = START_BITS
    while floor((c.k + c.lo) * scale) != floor((c.k + c.hi) * scale):
        bits *= 2
        if bits > MAX_BITS:
            msg = f"cannot round a({c.n}) at {places} places"
            raise SystemExit(msg)
        c.refine(bits)
    return decimal_down(c.k + c.lo, places)


def printed_value_holds(c: Candidate, printed: str) -> bool:
    """Whether v <= a(N) < v + 10^-PLACES for the printed 30-place value v."""
    v = Fraction(printed)
    unit = Fraction(1, 10**PLACES)
    bits = START_BITS
    while True:
        if v <= c.k + c.lo and c.k + c.hi < v + unit:
            return True
        if c.k + c.hi < v or c.k + c.lo >= v + unit:
            return False
        bits *= 2
        if bits > MAX_BITS:
            msg = f"cannot decide the printed value at N = {c.n}"
            raise SystemExit(msg)
        c.refine(bits)


# ------------------------------------------------------------------------------- driver


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--first", type=int, default=49)
    parser.add_argument("--last", type=int, default=3600)
    parser.add_argument("--out", type=Path, help="write the receipt here")
    args = parser.parse_args(argv)
    started = time.time()
    intervals, digest = load_intervals()
    facts = interval_facts(intervals)
    emit(f"intervals: {facts['intervals']}, problems: {facts['problems'] or 'none'}")
    author = {
        int(r["N"]): r
        for r in json.loads(gzip.decompress(AUTHOR_A_OF_N.read_bytes()))
        if r.get("claim") and r.get("interval") is not None
    }
    evaluation = {
        int(r["n"]): r
        for r in json.loads(EVALUATION.read_text(encoding="utf-8"))["rows"]
        if not r.get("square")
    }
    rows: list[dict[str, Any]] = []
    author_differ: list[str] = []
    evaluation_differ: list[str] = []
    interval_differ: list[str] = []
    exact_count = 0
    for n in range(args.first, args.last + 1):
        k = isqrt(n)
        if k * k == n or n < 49:
            continue
        best, ties = supremum(n, intervals)
        value = floor_places(best, PLACES)
        row: dict[str, Any] = {
            "N": n,
            "k": k,
            "attained_by": ties,
            "exact": best.exact,
            "lo": str(best.k + best.lo),
            "hi": str(best.k + best.hi),
            "a_floor_30": value,
        }
        exact_count += best.exact
        if n in author:
            ok = printed_value_holds(best, author[n]["a_N_rounded_down"])
            row["author_a_of_n_holds"] = ok
            if not ok:
                printed = author[n]["a_N_rounded_down"]
                author_differ.append(f"{n}: a_of_n {printed}, here {value}")
            if author[n]["interval"] not in ties:
                interval_differ.append(f"{n}: a_of_n I{author[n]['interval']}, here {ties}")
        if n in evaluation:
            ok = printed_value_holds(best, evaluation[n]["a_floor_30"])
            row["evaluation_holds"] = ok
            if not ok:
                printed = evaluation[n]["a_floor_30"]
                evaluation_differ.append(f"{n}: evaluation {printed}, here {value}")
            if evaluation[n]["interval"] not in ties:
                found = evaluation[n]["interval"]
                interval_differ.append(f"{n}: evaluation I{found}, here {ties}")
        rows.append(row)
    summary = {
        "counts": len(rows),
        "range": f"{args.first}-{args.last}",
        "exact_cap_k_plus_d1": exact_count,
        "roots": len(rows) - exact_count,
        "author_a_of_n_compared": sum("author_a_of_n_holds" in r for r in rows),
        "author_a_of_n_differences": author_differ,
        "evaluation_compared": sum("evaluation_holds" in r for r in rows),
        "evaluation_differences": evaluation_differ,
        "attaining_interval_differences": interval_differ,
        "seconds": round(time.time() - started, 1),
    }
    for key, value in summary.items():
        emit(f"{key}: {value if value != [] else 'none'}")
    for key, value in facts.items():
        emit(f"fact {key}: {value}")
    differences = author_differ + evaluation_differ + interval_differ
    ok = not facts["problems"] and not differences
    receipt = {
        "schema": "closed-form-review-a-by-definition/v1",
        "program": "review/a_of_n_by_definition.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "intervals_json_sha256": digest,
        "python": sys.version.split()[0],
        "interval_facts": facts,
        "summary": summary,
        "ok": ok,
        "rows": rows,
    }
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    emit("A-BY-DEFINITION OK" if ok else "A-BY-DEFINITION DIFFERS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
