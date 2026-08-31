#!/usr/bin/env python3
"""Price the shared row-jet inventory against what actually calls it.

`BC-038` asks whether wiring `evaluate_stress` to `RowJetInventory` repays its build cost.
A profile cannot answer that, and the commitment's own note says why: the saving depends on
whether the calls **share a field identity and a stratum**, and a profile sees neither. Two
calls that rebuild the same rows are a saving; two calls with different fields are not the
same call at all.

So this counts rather than times. For every `evaluate_stress` call in a run it records the
identity of the number field, the stratum and the owner, and separately counts how many
times `active_row_jets` actually rebuilds a stratum. From those two numbers the answer
follows arithmetically:

- **rebuilds** is what the inventory could remove;
- **distinct (field, stratum) pairs** is the floor it could remove them to;
- their difference is the whole prize, and it is zero when every call brings its own field.

`RowJetInventory.active_rows` refuses a field it does not own by identity, not by value, so
a caller that constructs its own field can never be served by someone else's inventory.
That is a deliberate soundness property -- two `Q(sqrt 2)` objects are different fields as
far as exact arithmetic is concerned -- and it is also the thing that decides this
commitment.

Usage:
    uv run --frozen --all-extras --group dev python -m devtools.price_row_jet_sharing
    uv run --frozen --all-extras --group dev python -m devtools.price_row_jet_sharing --check
"""

from __future__ import annotations

import argparse
import contextlib
import json
import pathlib
import statistics
import sys
import time
from collections import Counter, defaultdict
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from strif import atomic_output_file

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESULTS = ROOT / "campaign" / "series" / "series-000-smoke-and-calibration" / "results"
OUT = RESULTS / "bc-038-row-jet-sharing.json"

DRIVER = ("-q", "-p", "no:cacheprovider", "tests", "-m", "exhaustive_exact")
"""The `exhaustive exact behavioral tests` step, which is the group the profile named."""


class Identities:
    """Stable small integers for objects, compared by identity.

    `id()` looks like the obvious key and is wrong for this: it is a memory address, and
    CPython reuses the address of a freed object. Two consecutive runs of this tool
    reported 11 and then 10 distinct number fields for the same twenty-four tests, because
    a field built by one test was collected and the next test's field landed on its
    address. A count that moves between identical runs cannot be a contract.

    Holding a reference is the fix and also the cost: the fields stay alive for the run.
    There are about a dozen and each is a degree-two field, so that is a rounding error
    against the row jets themselves.
    """

    def __init__(self) -> None:
        self._seen: list[Any] = []

    def of(self, item: Any) -> int:
        for index, known in enumerate(self._seen):
            if known is item:
                return index
        self._seen.append(item)
        return len(self._seen) - 1


@dataclass
class Tally:
    """What one run did, in counts rather than seconds."""

    stress_calls: int = 0
    rebuilds: int = 0
    rebuild_seconds: float = 0.0
    stress_keys: Counter[tuple[int, str, str]] = field(default_factory=Counter)
    rebuild_keys: Counter[tuple[int, str]] = field(default_factory=Counter)
    seconds_by_stratum: dict[str, list[float]] = field(
        default_factory=lambda: defaultdict(list)
    )
    identities: Identities = field(default_factory=Identities)

    @property
    def distinct_fields(self) -> int:
        return len({key[0] for key in self.stress_keys})

    @property
    def distinct_field_strata(self) -> int:
        return len({(key[0], key[1]) for key in self.stress_keys})

    @property
    def strata(self) -> list[str]:
        return sorted(self.seconds_by_stratum)

    def typical(self, stratum: str) -> float:
        """One stratum's build cost, as the median of its observed builds.

        The median rather than the mean because the first build of a run pays import and
        warm-up that the rest do not, and one outlier in a sample of a dozen would set the
        projected cost of every hypothetical build below.
        """
        return statistics.median(self.seconds_by_stratum[stratum])

    @property
    def shareable_rebuilds(self) -> int:
        """Rebuilds an inventory could remove: every repeat of a `(field, stratum)` pair.

        A first build per pair is unavoidable -- the inventory pays it too, just earlier --
        so only the repeats are savings. Counting the whole rebuild total instead is the
        mistake that makes every cache look free.
        """
        return sum(count - 1 for count in self.rebuild_keys.values())


@contextlib.contextmanager
def instrument(tally: Tally) -> Iterator[None]:
    """Count `evaluate_stress` and `active_row_jets` for the duration of the block.

    Both are replaced by module attribute, which is how their callers reach them, and both
    are restored afterwards even on failure. `test_minus_w_row_inventory` installs its own
    counter over `active_row_jets` and restores what it found, so it restores this wrapper
    rather than trampling it.
    """
    from cases.n5 import minus_w_row_jets, minus_w_stress  # noqa: PLC0415 - heavy import

    original_rows = minus_w_row_jets.active_row_jets
    original_stress = minus_w_stress.evaluate_stress

    def counted_rows(field_argument: Any, stratum: str) -> Any:
        tally.rebuilds += 1
        tally.rebuild_keys[(tally.identities.of(field_argument), stratum)] += 1
        started = time.perf_counter()
        try:
            return original_rows(field_argument, stratum)
        finally:
            spent = time.perf_counter() - started
            tally.rebuild_seconds += spent
            tally.seconds_by_stratum[stratum].append(spent)

    def counted_stress(
        field_argument: Any, stratum: str, owner: str, *args: Any, **kwargs: Any
    ) -> Any:
        tally.stress_calls += 1
        tally.stress_keys[(tally.identities.of(field_argument), stratum, owner)] += 1
        return original_stress(field_argument, stratum, owner, *args, **kwargs)

    minus_w_row_jets.active_row_jets = counted_rows
    minus_w_stress.evaluate_stress = counted_stress
    try:
        yield
    finally:
        minus_w_row_jets.active_row_jets = original_rows
        minus_w_stress.evaluate_stress = original_stress


def measure() -> tuple[Tally, float, int]:
    """Run the driver once under instrumentation."""
    import pytest  # noqa: PLC0415 - heavy optional import

    tally = Tally()
    started = time.perf_counter()
    with instrument(tally):
        status = pytest.main([*DRIVER])
    return tally, time.perf_counter() - started, int(status)


def projections(tally: Tally, overhead: float) -> dict[str, Any]:
    """What each sharing strategy would cost, priced from the builds actually observed.

    Three strategies, and the middle one is the one the commitment proposes:

    - **as it stands**: every call rebuilds, which is what was measured;
    - **an eager inventory per field**: `RowJetInventory.build` constructs *every*
      registered stratum for one field, so its cost is the field count times the whole
      stratum set -- including strata that field never asks for;
    - **a lazy memo per (field, stratum)**: the floor, since a first build of each pair is
      unavoidable however it is arranged.

    Priced from each stratum's own median observed build rather than from one average, so a
    stratum that is dearer than the others is not silently subsidised by the cheap ones.
    """
    per_stratum = {stratum: tally.typical(stratum) for stratum in tally.strata}
    lazy = sum(per_stratum[stratum] for _identity, stratum in tally.rebuild_keys)
    eager = tally.distinct_fields * sum(per_stratum.values())
    status_quo = tally.rebuild_seconds
    return {
        "per_stratum_median_seconds": {
            stratum: round(value, 3) for stratum, value in per_stratum.items()
        },
        "build_seconds": {
            "as_it_stands": round(status_quo, 3),
            "eager_inventory_per_field": round(eager, 3),
            "lazy_memo_per_field_stratum": round(lazy, 3),
        },
        "driver_seconds": {
            "as_it_stands": round(status_quo + overhead, 3),
            "eager_inventory_per_field": round(eager + overhead, 3),
            "lazy_memo_per_field_stratum": round(lazy + overhead, 3),
        },
        "speedup": {
            "eager_inventory_per_field": round((status_quo + overhead) / (eager + overhead), 2),
            "lazy_memo_per_field_stratum": round(
                (status_quo + overhead) / (lazy + overhead), 2
            ),
        },
        "unavoidable_overhead_seconds": round(overhead, 3),
    }


def report() -> dict[str, Any]:
    tally, elapsed, status = measure()
    overhead = max(elapsed - tally.rebuild_seconds, 0.0)
    return {
        "schema_version": 2,
        "subject": {
            "commitment": "BC-038",
            "question": (
                "does wiring evaluate_stress to the shared row inventory repay its build "
                "cost at exact semantic equality?"
            ),
            "driver": "pytest " + " ".join(DRIVER),
            "driver_status": status,
        },
        "counts": {
            "evaluate_stress_calls": tally.stress_calls,
            "active_row_jets_rebuilds": tally.rebuilds,
            "distinct_number_fields": tally.distinct_fields,
            "distinct_field_stratum_pairs": tally.distinct_field_strata,
            "shareable_rebuilds": tally.shareable_rebuilds,
            "registered_strata": len(tally.strata),
            "eager_inventory_builds": tally.distinct_fields * len(tally.strata),
        },
        "timing_not_a_contract": {
            "why": (
                "retained for the report and deliberately excluded from --check: seconds "
                "move with host load, counts do not, and it is the counts that decide "
                "whether there is anything to share"
            ),
            **projections(tally, overhead),
        },
    }


def verdict(counts: dict[str, int]) -> str:
    """The arithmetic, stated rather than left to the reader."""
    if counts["shareable_rebuilds"] == 0:
        return (
            "reject: no rebuild is shareable. Every evaluate_stress call arrives with its "
            "own number field, so an inventory built for one caller is refused by identity "
            "for every other."
        )
    eager = counts["eager_inventory_builds"]
    actual = counts["active_row_jets_rebuilds"]
    floor = counts["distinct_field_stratum_pairs"]
    return (
        f"{counts['shareable_rebuilds']} of {actual} rebuilds repeat a (field, stratum) "
        f"pair; an eager inventory would build {eager} and a lazy memo {floor}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="compare counts against the retained record"
    )
    args = parser.parse_args()

    built = report()
    if args.check:
        if not OUT.exists():
            print(f"  {OUT.name} is missing", file=sys.stderr)
            return 1
        retained = json.loads(OUT.read_text(encoding="utf-8"))
        if retained["counts"] != built["counts"]:
            print(f"  {OUT.name} counts have drifted", file=sys.stderr)
            print(f"    retained {retained['counts']}", file=sys.stderr)
            print(f"    measured {built['counts']}", file=sys.stderr)
            return 1
        print(f"  row-jet sharing reproduces: {verdict(built['counts'])}")
        return 0

    with atomic_output_file(OUT) as tmp:
        tmp.write_text(json.dumps(built, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT.parent)}")
    print(f"  {verdict(built['counts'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
