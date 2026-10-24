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
- Ryu's k^{2/5} and k^{3/8} rows, which speak only from k = 1.6*10^7, 4*10^26 and
  2.48*10^12, beyond every k this comparison decides one by one.

The waste bounds of the ledger's ``upper_bounds`` are each O(x^a) with no constant, so
none states a value of c*(k) at any k; a row there that gains a ``constant`` fails the
comparison, as does a deficiency row the table above does not name. That is the
freshness an assessment needs (think-e953): a new statement of the family is compared
before any assessment stands again.

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
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cases.asymptotic import fang_excess_inventory as fang
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


def ryu_theorem_1_3(k: int) -> int:
    """Ryu's Theorem 1.3 at its best b: the least k^2 - N(k, b) - 1 over 2 <= b <= k."""
    return min(k * k - ryu.count(k, b) - 1 for b in range(2, k + 1))


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


STATEMENTS: tuple[Statement, ...] = (
    Statement(AMS, "c*(k) <= k - 1 for k >= 12", 12, None, "", ams),
    Statement(
        RYU,
        "Theorems 1.3 and 1.4",
        6,
        "sqrt k, at integer sides approached from below",
        "k >= 6",
        ryu_theorem_1_3,
    ),
    Statement(
        FANG,
        "Theorem 2",
        15,
        "k, at integer sides approached from below",
        "k >= 15",
        fang.theorem_two,
    ),
    Statement(
        RYU,
        "Theorem 1.2",
        16 * 10**6,
        "k^{2/5}, at integer sides approached from below",
        "k >= 1.6*10^7",
        None,
    ),
    Statement(
        RYU,
        "Theorem 1.1 of version 1.0",
        4 * 10**26,
        "k^{3/8}, at integer sides approached from below",
        "k >= 4*10^26",
        None,
    ),
    Statement(
        RYU_V11,
        "Theorem 1.1 of version 1.1",
        248 * 10**10,
        "k^{3/8}, at integer sides approached from below",
        "k >= k_i in each tier",
        None,
    ),
)
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


def statement_for(row: Mapping[str, Any]) -> Statement:
    """The table's entry for a deficiency row, bound to it by its key, kernel and text."""
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
    return found[0]


def _runs(values: Sequence[int]) -> list[list[int]]:
    runs: list[list[int]] = []
    for value in values:
        if runs and runs[-1][1] == value - 1:
            runs[-1][1] = value
        else:
            runs.append([value, value])
    return runs


def assess(
    ledger: Mapping[str, Any], row: Mapping[str, Any], dated: Mapping[str, str]
) -> dict[str, Any]:
    """The assessment of ``row``'s theorem-wide bound against every other statement.

    ``dated`` is each source key's date in the bibliography, which orders a tie."""
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
                dated[item.source_key] > dated[own.source_key]
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
    ledger: Mapping[str, Any], dated: Mapping[str, str]
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


def load() -> tuple[dict[str, Any], dict[str, str]]:
    """The ledger and every bibliography key's date."""
    ledger = safe_load(LEDGER.read_text(encoding="utf-8"))
    sources = safe_load(BIBLIOGRAPHY.read_text(encoding="utf-8"))["sources"]
    return ledger, {str(item["key"]): str(item.get("dated", "")) for item in sources}


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
