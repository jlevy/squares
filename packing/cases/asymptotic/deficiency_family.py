"""Compare a theorem-wide deficiency bound with every other statement of its family.

The ledger's ``deficiency_upper_bounds`` (``frontier/asymptotic-waste-bounds.yaml``) holds
bounds on c*(k) = max{c : s(k^2 - c) = k}, each for every integer k of its stated range.
A row whose theorem the register holds only by its finite case projection links that
result in ``record_scope``, and ``devtools.profile_records`` counts the theorem-wide
scope as current only where the link's ``assessment`` is what this module recomputes:
the k at which the row's bound is strictly the smallest statement of the family, the k
at which it ties one, and whether it is current. A tie stays with the earlier report
(``campaign/result-import.md``, Several Reports at One Count), so a tied k is the row's
only when every statement it ties was reported later.

The family's statements, each with the least k it speaks for and the maintained
function that gives its value there:

- Arslanov, Mustafin and Shangitbayev's c*(k) <= k - 1 for k >= 12 (Electronic Journal
  of Combinatorics 28(4), P4.22, 2021), the bound the rows improve, which is not a row of
  its own (``fang_excess_inventory.ams``);
- Sungjoon Ryu's Theorems 1.3 and 1.4, the row of kernel sqrt k: the least
  k^2 - N(k, b) - 1 over 2 <= b <= k (``ryu_upper_l_packing.count``), which Theorem 1.4's
  8 ceil(sqrt(k - 4)) - 1, at b = ceil(sqrt(k - 4)), never undercuts;
- Kevin Fang's Theorem 2, k - 1 - F(k) for k >= 15 (``fang_excess_inventory.theorem_two``),
  his Theorem 1's k - 2 being never smaller;
- Evan Daniel's 4 ceil(sqrt(2k - 7)) - 1 for k >= 7, in Lean (`daniel_layers`), and Kevin
  Fang's later Theorem A, ceil(sqrt(32k)) for k >= 6 (``fang_theorem_a.theorem_a``), two
  rows of kernel sqrt k reported on 18 and 24 October 2026;
- Ryu's k^{2/5} and k^{3/8} rows, which speak only from k = 1.6*10^7, 4*10^26 and
  2.48*10^12, beyond every k this comparison decides one by one.

The waste bounds of the ledger's ``upper_bounds`` are each O(x^a) with no constant, so
none states a value of c*(k) at any k; a row there that gains a ``constant`` fails the
comparison, as does a deficiency row the table above does not name, or a row restated in
place, whose ``bound`` or ``constant`` is no longer the text its entry was compared as.
That is the freshness an assessment needs (think-e953): a new statement of the family is
compared before any assessment stands again. A tie is ordered by the bibliography's
``dated`` read as days, and a source with no day-precision date refuses rather than
ordering one.

Every k from 15 to ``TAIL - 1`` is decided one by one, in integers. From ``TAIL`` on,
Fang's bound is larger than Ryu's: F(k) <= 1 + 2(k - 15)/21, because p + 2q <=
(2/21)(16p + 21q), so k - 1 - F(k) >= (19k - 12)/21; and 8 ceil(sqrt(k - 4)) - 1 <=
8 sqrt(k - 4) + 7. The first exceeds the second where 19k - 159 > 168 sqrt(k - 4), that
is where 19k - 159 > 0 and h(k) = (19k - 159)^2 - 168^2 (k - 4) > 0; h is a quadratic
with positive leading term whose vertex is at 34266/722, below ``TAIL``, so
``tail_holds`` deciding h(TAIL) > 0 decides every k >= TAIL.

The comparison is of the family's theorem-wide statements, not of finite certificates,
which the finite case projection and the beyond-horizon register compare (the record's
rows end at n = 1024, k = 32).

Run from ``packing/``::

    uv run --frozen --all-extras --group dev python -m cases.asymptotic.deficiency_family
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

from cases.asymptotic import fang_excess_inventory as fang
from cases.asymptotic import fang_theorem_a
from cases.asymptotic import ryu_upper_l_packing as ryu
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "frontier/asymptotic-waste-bounds.yaml"
BIBLIOGRAPHY = ROOT / "resources/bibliography.yaml"
SECTION = "deficiency_upper_bounds"
#: The least k from which every k is decided by `tail_holds` rather than one by one.
TAIL = 91
AMS = "[Arslanov et al.]"
FANG = "[Fang excess theorem 2026-10-13]"
RYU = "[squarepacker k2-minus-c-upper 2026]"
RYU_V11 = "[squarepacker k2-minus-c-upper v1.1 2026]"
DANIEL = "[Daniel k2-minus-c Lean 2026-10-18]"
FANG_A = "[Fang Theorem A 2026-10-24]"
#: A day-precision bibliography date, the only kind that orders a tie.
DAY = re.compile(r"\d{4}-\d{2}-\d{2}")


def ryu_theorem_1_3(k: int) -> int:
    """Ryu's Theorem 1.3 at its best b: the least k^2 - N(k, b) - 1 over 2 <= b <= k."""
    return min(k * k - ryu.count(k, b) - 1 for b in range(2, k + 1))


def daniel_layers(k: int) -> int:
    """Evan Daniel's c*(k) <= 4 ceil(sqrt(2k - 7)) - 1 for every k >= 7 (RyuLayers)."""
    if k < 7:
        raise ValueError(f"Daniel's bound is stated for k >= 7, not k = {k}")
    return 4 * fang_theorem_a.ceil_sqrt(2 * k - 7) - 1


def ams(k: int) -> int:
    """Arslanov, Mustafin and Shangitbayev: c*(k) <= k - 1 for every k >= 12."""
    value = fang.ams(k)
    if value is None:
        raise ValueError(f"the AMS bound is stated for k >= 12, not k = {k}")
    return value


@dataclass(frozen=True)
class Statement:
    """One statement of the family: whose, which, from which k, and its value there."""

    source_key: str
    statement: str
    least_k: int
    #: The row's `kernel`, or None for a statement the ledger names only in prose.
    kernel: str | None
    #: Text the row's `side_condition` must contain, binding this entry to the row.
    anchor: str
    #: The maintained function of k, or None where `least_k` lies beyond every k decided
    #: one by one, so that the statement never bears on the comparison.
    value: Callable[[int], int] | None
    #: The row's `bound` and `constant` as this entry was checked against them, with their
    #: whitespace collapsed: a row restated in place under the same key, kernel and anchor
    #: differs from them, and so is compared again (`STATED`).
    bound: str = ""
    constant: str = ""


STATEMENTS: tuple[Statement, ...] = (
    Statement(AMS, "c*(k) <= k - 1 for k >= 12", 12, None, "", ams),
    Statement(
        RYU,
        "Theorems 1.3 and 1.4",
        6,
        "sqrt k, at integer sides approached from below",
        "k >= 6",
        ryu_theorem_1_3,
        bound=(
            "REPORTED: c*(k) <= 8 ceil(sqrt(k-4)) - 1 < 8 sqrt(k-4) + 7 for every integer k "
            ">= 6 (Theorem 1.4), where c*(k) = max{c : s(k^2-c) = k}. It comes from an "
            "explicit L-shaped packing of N(k,b) = (k-b)^2 + b(R(k) + R(k-b)) unit squares "
            "in a square of side less than k (Theorem 1.3), which gives c*(k) <= k^2 - "
            "N(k,b) - 1 < 6b + 4k/b - 3 for 2 <= b <= k and cannot give less than 8 sqrt(k) "
            "- 15 (Proposition 1.5)."
        ),
        constant=(
            "8, with b = ceil(sqrt(k-4)) and the additive -1. The family's exact count is "
            "k^2 - N(k,b) = 6b + b(floor(eta) + floor(eta')) when k - b >= 2, with eta = "
            "(2k-10)/(b^2+1) + 8/(b^2+1)^2 and eta' = eta - 2b/(b^2+1) (equation 5.1); "
            "Corollary 5.1 gives c*(k) < 4 sqrt(6) sqrt(k) for k >= 6."
        ),
    ),
    Statement(
        DANIEL,
        "packs_sub_4sqrt2_layers",
        7,
        "sqrt k, at integer sides approached from below",
        "k >= 7",
        daniel_layers,
        bound=(
            "REPORTED: c*(k) <= 4 ceil(sqrt(2k-7)) - 1 < 4 sqrt(2k-7) + 3 for every integer "
            "k >= 7, where c*(k) = max{c : s(k^2-c) = k}, proved in Lean: k^2 - 4b unit "
            "squares pack in a square of side less than k with b = ceil(sqrt(2k-7)) "
            "(packs_sub_4sqrt2_layers). The packing is Ryu's L with L - 3 rows in each band "
            "of length L and 2b axis-parallel squares in the four band ends."
        ),
        constant=(
            "4 sqrt 2, with b = ceil(sqrt(2k-7)) and the additive -1. The four band ends hold "
            "floor((b-1)/2) axis squares twice, floor(b/2) and floor(b/2) + 2, 2b in all, at "
            "the angle t = 1/b + delta with delta b (b^2+1)(6k+4b) = 1. The +5 milestone, 4 "
            "ceil(sqrt(2k-7)) + 5 (packs_sub_4sqrt2, a645fe3), fills each end with one layer."
        ),
    ),
    Statement(
        FANG_A,
        "Theorem A",
        6,
        "sqrt k, at integer sides approached from below",
        "k >= 6",
        fang_theorem_a.theorem_a,
        bound=(
            "REPORTED: c*(k) < 4 sqrt(2k) + 1, so c*(k) <= ceil(sqrt(32k)), for every integer "
            "k >= 6 (Theorem A): s(n) < k for every n <= k^2 - ceil(sqrt(32k)) - 1. Ryu's "
            "L-shaped packing with both ends of each band filled by axis-parallel rows (lift 0 "
            "at one end, the whole free length at the other) and b an odd integer with |b - "
            "sqrt(2k)| <= 1."
        ),
        constant=(
            "4 sqrt 2 with additive 1: w(k) <= b(k - S) plus two band terms (equation 1), each "
            "below 2bL/(b^2+1) + b + 2 - kappa_b, kappa_b = (7b^4+1)/(b(b^2+1)^2), as t -> 1/b "
            "(Lemma 2); sharp for this construction, whose waste is exactly 4b at k = (b^2 - b "
            "+ 8)/2 for odd b >= 5."
        ),
    ),
    Statement(
        FANG,
        "Theorem 2",
        15,
        "k, at integer sides approached from below",
        "k >= 15",
        fang.theorem_two,
        bound=(
            "REPORTED: c*(k) <= k - 1 - F(k) for every integer k >= 15 (Theorem 2), in "
            "particular c*(k) <= k - 2 (Theorem 1), where c*(k) = max{c : s(k^2-c) = k}. "
            "Theorem 1 packs n^2 - n + 1 unit squares in a square of side less than n for "
            "every n >= 15, by an induction from a base case at n = 15 through Lemma 3 and "
            "a scaling lemma; Theorem 2 packs n^2 - n + F(n)."
        ),
        constant=(
            "1, less F(k) = 1 + max{p + 2q : 16p + 21q <= k - 15}, about 2(k - 15)/21, so "
            "the bound reads about (19/21)k."
        ),
    ),
    Statement(
        RYU,
        "Theorem 1.2",
        16 * 10**6,
        "k^{2/5}, at integer sides approached from below",
        "k >= 1.6*10^7",
        None,
        bound=(
            "REPORTED: c*(k) < (20/3)(3/2)^{2/5} 5.03^{3/5} k^{2/5} + (8/3) 5.03 10^{-4/3} "
            "< 20.668 k^{2/5} + 0.623 for every integer k >= 1.6*10^7 (Theorem 1.2), and "
            "c*(k) <= (18.89 + o(1)) k^{2/5}."
        ),
        constant=(
            "20.668 and 0.623, from the end constant C_E = 5.03 of Corollary 7.4, which "
            "rests on one interval evaluation Phi(10^{-4/3}) <= 5.0163; with b = "
            "ceil((3k/(2 C_E))^{3/5}). The limit coefficient 18.89 is Phi(0) = "
            "sqrt(6.000002/0.75) + 3/2 = 4.3284 in place of C_E."
        ),
    ),
    Statement(
        RYU,
        "Theorem 1.1 of version 1.0",
        4 * 10**26,
        "k^{3/8}, at integer sides approached from below",
        "k >= 4*10^26",
        None,
        bound=(
            "REPORTED: c*(k) < (32/5)(5/3)^{3/8} 15.54^{5/8} k^{3/8} + 2*10^-5 < 43.06 "
            "k^{3/8} + 2*10^-5 for every integer k >= 4*10^26 (Theorem 1.1 of version 1.0; "
            "version 1.1 keeps it and supersedes it by the tier A5, 40.62 k^{3/8} + "
            "1.4*10^-5 for k >= 3.4*10^26, next row)."
        ),
        constant=(
            "43.06 = (32/5)(5/3)^{3/8} 15.54^{5/8} rounded up, from the end constant C_E = "
            "15.54 of Corollary 8.3 for b >= b0 = 10^16, certified by the interval covering "
            "code/cert3e.py (160 x 64 boxes, C_E <= 14.964). The source reports two further "
            "coverings that are not in the release."
        ),
    ),
    Statement(
        RYU_V11,
        "Theorem 1.1 of version 1.1",
        248 * 10**10,
        "k^{3/8}, at integer sides approached from below",
        "k >= k_i in each tier",
        None,
        bound=(
            "REPORTED: for each of twelve tiers, c*(k) < C_i k^{3/8} + a_i for every "
            "integer k >= k_i (Theorem 1.1 of version 1.1): B1 46.31, 2.2*10^13, 0.035; B1s "
            "45.49, 4.5*10^13, 0.029; B2 45.08, 6.4*10^13, 0.026; A1 48.76, 4.6*10^14, "
            "0.019; A1s 48.38, 6.1*10^14, 0.017; A2 46.42, 2.7*10^15, 0.011; A3 43.61, "
            "9.6*10^16, 0.0039; A4 41.73, 1.5*10^20, 5.7*10^-4; A5 40.62, 3.4*10^26, "
            "1.4*10^-5; C1 41.19, 5.22*10^12, 0.04; C2 41.78, 2.95*10^12, 0.047; C3 42.09, "
            "2.48*10^12, 0.05. Smaller than Theorem 1.2's bound for every k >= 2.48*10^12."
        ),
        constant=(
            "Per tier, C_i >= (32/5)(5/3)^{3/8} C_E^{5/8}, k_i >= (3/5) C_E b0^{8/5} and "
            "a_i >= (12/5) C_E b0^{-2/5}, with (b0, C_E) = B1 (10^7.7, 17.461), B1s "
            "(10^7.9, 16.968), B2 (10^8, 16.721), A1 (10^8.5, 18.961), A1s (10^8.58, "
            "18.722), A2 (10^9, 17.523), A3 (10^10, 15.859), A4 (10^12, 14.778), A5 (10^16, "
            "14.153), C1 (10^7.3617, 14.473), C2 (10^7.2, 14.805), C3 (10^7.15, 14.983). "
            "The tiers B use the variant wall filler ZC' (Lemmas 8.2-8.5); the tiers C also "
            "the sawtooth accounting and the lift of each band (Lemmas 8.6-8.8, 8.11). Each "
            "C_E is certified by the author's covering, code/cert_v3/cert_v3.py or "
            "code/cert_v4/cert_v4.py, at 320 x 128 boxes."
        ),
    ),
)
#: The fields of a row that state its bound, each held to its entry's text in full.
STATED = ("bound", "constant")
#: The statements the ledger names only in prose, compared beside its rows.
PROSE_ONLY = tuple(item for item in STATEMENTS if item.kernel is None)
#: The rows whose theorem-wide scope this module can assess, with its tail lemma.
ASSESSABLE = {(FANG, "k, at integer sides approached from below")}


class FamilyError(ValueError):
    """The ledger names a statement the comparison does not, or a row it cannot assess."""


def tail_holds(k: int = TAIL) -> bool:
    """Whether Fang's Theorem 2 exceeds Ryu's Theorem 1.4 at every k >= ``k``.

    h(k) = (19k - 159)^2 - 168^2 (k - 4) is increasing past its vertex 34266/722, so
    19k - 159 > 0, k past the vertex and h(k) > 0 decide every larger k."""
    return 722 * k > 34266 and 19 * k > 159 and (19 * k - 159) ** 2 > 168**2 * (k - 4)


def _collapsed(value: object) -> str:
    return " ".join(str(value).split()) if value is not None else ""


def statement_for(row: Mapping[str, Any]) -> Statement:
    """The table's entry for a deficiency row, bound to it by its key, kernel and
    side-condition anchor, and held to its stated bound and constant in full, so that a
    row edited in place refuses until its entry is compared again."""
    found = [
        item
        for item in STATEMENTS
        if item.kernel is not None
        and item.source_key == row.get("source_key")
        and item.kernel == row.get("kernel")
        and item.anchor in str(row.get("side_condition", ""))
    ]
    if len(found) != 1:
        raise FamilyError(
            f"{SECTION}: no single maintained statement for {row.get('source_key')} "
            f"({row.get('kernel')}); compare it before any assessment stands"
        )
    item = found[0]
    for field in STATED:
        if _collapsed(row.get(field)) != getattr(item, field):
            raise FamilyError(
                f"{SECTION}: {item.source_key} ({item.kernel}) is restated: its {field} "
                f"is not the text {item.statement} was compared as; compare it before any "
                "assessment stands"
            )
    return item


def _runs(values: Sequence[int]) -> list[list[int]]:
    runs: list[list[int]] = []
    for value in values:
        if runs and runs[-1][1] == value - 1:
            runs[-1][1] = value
        else:
            runs.append([value, value])
    return runs


def reported_on(dated: Mapping[str, object], key: str) -> date:
    """The day a source key was reported, its `dated` in the bibliography, as a date.

    A tie is ordered by these days (`assess`), so a key with no day-precision date, a
    missing, null or partial one, refuses rather than ordering a tie as text would."""
    value = dated.get(key)
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str) and DAY.fullmatch(value):
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass
    raise FamilyError(
        f"{key} has no day-precision date in the bibliography ({value!r}), so it orders "
        "no tie; date it before any assessment stands"
    )


def assess(
    ledger: Mapping[str, Any], row: Mapping[str, Any], dated: Mapping[str, object]
) -> dict[str, Any]:
    """The assessment of ``row``'s theorem-wide bound against every other statement.

    ``dated`` is each source key's date in the bibliography, which orders a tie: the
    row's own key always needs one, and so does every key it ties (`reported_on`)."""
    for waste in ledger.get("upper_bounds") or ():
        if "constant" in waste:
            raise FamilyError(
                f"upper_bounds: {waste['source_key']} states a constant, so it may state "
                "a value of c*(k); compare it before any assessment stands"
            )
    rows = [statement_for(item) for item in ledger[SECTION]]
    if len(set(rows)) != len(rows):
        raise FamilyError(f"{SECTION}: two rows bind one maintained statement")
    own = statement_for(row)
    if (own.source_key, own.kernel) not in ASSESSABLE or own.value is None:
        raise FamilyError(f"{SECTION}: no tail lemma assesses {own.source_key}")
    own_day = reported_on(dated, own.source_key)
    if not tail_holds(TAIL):
        raise FamilyError(f"the tail lemma does not hold from k = {TAIL}")
    others = [*PROSE_ONLY, *(item for item in rows if item != own)]
    for item in others:
        if item.value is None and item.least_k < TAIL:
            raise FamilyError(f"{item.source_key} {item.statement} has no value below {TAIL}")
    smallest: list[int] = []
    tied: list[int] = []
    for k in range(own.least_k, TAIL):
        mine = own.value(k)
        values = [
            (item.value(k), item)
            for item in others
            if item.value is not None and k >= item.least_k
        ]
        best = min(value for value, _ in values)
        if mine < best:
            smallest.append(k)
        elif mine == best:
            tied.append(k)
            if all(
                reported_on(dated, item.source_key) > own_day
                for value, item in values
                if value == best
            ):
                smallest.append(k)
    return {
        "current": bool(smallest),
        "smallest": _runs(smallest),
        "tied": _runs(tied),
        "compared": [
            {"source_key": item.source_key, "statement": item.statement} for item in others
        ],
    }


def recorded_assessments(
    ledger: Mapping[str, Any], dated: Mapping[str, object]
) -> list[tuple[str, dict[str, Any], dict[str, Any]]]:
    """Each linked row's recorded assessment beside its recomputation, by result."""
    found = []
    for row in ledger.get(SECTION) or ():
        recorded = (row.get("record_scope") or {}).get("assessment")
        if recorded is not None:
            found.append(
                (str(row["record_scope"]["result"]), recorded, assess(ledger, row, dated))
            )
    return found


def stale(recorded: Mapping[str, Any], recomputed: Mapping[str, Any]) -> list[str]:
    """The fields of a recorded assessment its recomputation does not reproduce."""
    return [key for key in recomputed if recorded.get(key) != recomputed[key]]


def load() -> tuple[dict[str, Any], dict[str, object]]:
    """The ledger and every bibliography key's `dated`, as the bibliography gives it:
    `reported_on` reads it as a day, and refuses one that is not."""
    ledger = safe_load(LEDGER.read_text(encoding="utf-8"))
    sources = safe_load(BIBLIOGRAPHY.read_text(encoding="utf-8"))["sources"]
    return ledger, {str(item["key"]): item.get("dated") for item in sources}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.parse_args(argv)
    ledger, dated = load()
    failed = False
    for result, recorded, recomputed in recorded_assessments(ledger, dated):
        drift = stale(recorded, recomputed)
        failed = failed or bool(drift)
        print(json.dumps({"result": result, "recomputed": recomputed, "stale": drift}))
    if failed:
        print("DEFICIENCY_FAMILY_DRIFT: a recorded assessment differs from its recomputation")
        return 1
    print("DEFICIENCY_FAMILY_HOLDS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
