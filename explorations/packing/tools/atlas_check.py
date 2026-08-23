#!/usr/bin/env python3
"""Gate check for the basin atlas: the invariants a census depends on.

    uv run python tools/atlas_check.py

The atlas is the census's output, so every way it can be quietly wrong is a way the
census can report a number nobody should believe:

1. **Deduplication.** Offering the same configuration twice must raise a frequency, not
   add a row. If it does not, `distinct_basins` counts proposals and the discovery curve
   never plateaus — which reads as "the landscape is huge" rather than "the store is
   broken".
2. **Append-only.** Adding must never remove or reorder existing rows, or the discovery
   curve stops being monotone and its plateau stops meaning saturation.
3. **Round trip.** Save then load must be the identity, or frequencies accumulated over
   a night are lost at the first reload.
4. **Merge.** Two stores of one `n` must combine by summing frequencies and unioning
   basins, which is what lets a census run on more than one machine.
5. **Schema.** Every file written validates against the declared contract.
6. **Convergence.** Most quenches in the census must actually have converged. This is
   the one that is not structural, and it is the one the first version of this file
   lacked: every check above passed on a census where 11 of 12 quenches had stopped on
   a sweep limit, and the store dutifully recorded twelve non-converged stopping points
   as twelve distinct basins. A store can only be as honest as what it is fed.

Then it exercises all of it end to end on real quench output at `n = 5`, where the
answer is small enough to argue with by hand.
"""

from __future__ import annotations

import random
import sys
import tempfile
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqpack.atlas import Atlas
from sqpack.canonical import BasinKey, canonical_key
from sqpack.quench import quench_bracket

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "atlas" / "atlas.schema.yaml"


def check(label: str, *, ok: bool, detail: str = "") -> bool:
    print(f"  {'ok  ' if ok else 'FAIL'}  {label}" + (f"  [{detail}]" if detail else ""))
    return ok


def random_start(n: int, side: float, rng: random.Random):
    """A uniform multistart draw: centres anywhere, angles anywhere in the quarter."""
    return (
        [rng.uniform(0.5, side - 0.5) for _ in range(n)],
        [rng.uniform(0.5, side - 0.5) for _ in range(n)],
        [rng.uniform(0, 1.5707963267948966) for _ in range(n)],
    )


def main() -> int:
    passed = True
    validator = Draft202012Validator(yaml.safe_load(SCHEMA.read_text()))

    # Build a small real census at n = 5, where s(5) = 2 + 1/sqrt(2) is proved and the
    # landscape is small enough to sanity-check by eye.
    # Six seeds at a realistic budget, not twelve at a token one. Measured 2026-08-23:
    # a cold n = 5 quench takes 6.5-45 s (median ~12 s) to reach its free-pass
    # certificate. The first version of this check allowed 10 s, so eight of twelve runs
    # were cut off mid-descent -- and the store then recorded eight interrupted
    # descents as eight distinct basins. A budget that truncates the instrument
    # measures the budget.
    rng = random.Random(20260823)
    atlas = Atlas(n=5)
    for seed in range(6):
        x, y, theta = random_start(5, 3.2, rng)
        r = quench_bracket(x, y, theta, time_budget=90.0)
        atlas.add(canonical_key(r.x, r.y, r.theta, r.side), seed=seed, converged=r.converged)

    # Census-only figures, captured BEFORE the deduplication step below re-adds rows
    # with converged=True. Measuring the convergence rate after that would measure the
    # test's own bookkeeping, which is the same class of error the guard exists to catch.
    census_proposals, census_non_converged = atlas.proposals, atlas.non_converged

    passed &= check(
        "a real n=5 census produces at least one basin",
        ok=bool(atlas.basins),
        detail=f"{len(atlas.basins)} distinct from {atlas.proposals} proposals",
    )

    # 1. Deduplication: re-offer everything already in the store.
    before_rows, before_proposals = len(atlas.basins), atlas.proposals
    for basin in list(atlas.basins):
        atlas.add(_key_of(basin), converged=True)
    passed &= check(
        "re-offering a known basin raises its frequency, never adds a row",
        ok=len(atlas.basins) == before_rows
        and atlas.proposals == before_proposals + before_rows,
        detail=f"{len(atlas.basins)} rows, {atlas.proposals} proposals",
    )

    # 2. Append-only: the identities present before are all still present.
    identities = {b.identity for b in atlas.basins}
    passed &= check(
        "adding never removes an existing basin",
        ok=len(identities) == len(atlas.basins),
        detail=f"{len(identities)} unique identities in {len(atlas.basins)} rows",
    )

    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "n-005.yaml"
        atlas.save(path)

        # 5. Schema.
        doc = yaml.safe_load(path.read_text())
        errors = sorted(validator.iter_errors(doc["atlas"]), key=lambda e: list(e.path))
        passed &= check(
            "the written file validates against the declared contract",
            ok=not errors,
            detail=errors[0].message if errors else CONTRACT_OK,
        )

        # 3. Round trip.
        reloaded = Atlas.load(path)
        passed &= check(
            "save then load is the identity",
            ok=reloaded.to_document() == atlas.to_document(),
            detail=f"{reloaded.proposals} proposals, {len(reloaded.basins)} basins",
        )

        # 4. Merge.
        merged = Atlas.load(path)
        merged.merge(Atlas.load(path))
        total_before = sum(b.quench_frequency for b in atlas.basins)
        passed &= check(
            "merging a store with itself doubles frequencies and adds no rows",
            ok=len(merged.basins) == len(atlas.basins)
            and sum(b.quench_frequency for b in merged.basins) == total_before * 2,
            detail=f"{len(merged.basins)} rows, "
            f"{sum(b.quench_frequency for b in merged.basins)} total frequency",
        )

    # 6. The guard the first version of this file did not have, and needed.
    #
    # Every structural invariant above passed on a census in which 11 of 12 quenches had
    # stopped on a sweep limit: the store faithfully recorded twelve non-converged
    # stopping points as twelve distinct basins. Structural checks cannot see that --
    # they check the store, not what it was fed. So this one does.
    converged = census_proposals - census_non_converged
    passed &= check(
        "most quenches in the census actually converged",
        ok=converged * 2 >= census_proposals,
        detail=f"{converged}/{census_proposals} converged; a census below half is "
        "measuring the sweep limit, not the landscape",
    )

    best = min(atlas.basins, key=lambda b: b.side)
    print(
        f"\n  n=5: {len(atlas.basins)} basins from {atlas.proposals} proposals; "
        f"best side {best.side:.12f} ({best.contact_count} contacts, "
        f"classes {list(best.angle_signature)}); closest pair {atlas.closest_pair}"
    )
    print("ATLAS CHECKS PASSED" if passed else "ATLAS CHECKS FAILED")
    return 0 if passed else 1


CONTRACT_OK = "validates"


def _key_of(basin):
    """Rebuild a BasinKey from a stored row, for the deduplication test.

    Deliberately built from the STORED fields rather than by re-quenching: the property
    under test is that the store recognises an identity it already holds, and re-quenching
    would test the quench instead.
    """
    return BasinKey(
        n=5,
        geometric=basin.geometric,
        contact=basin.contact,
        side=basin.side,
        angle_signature=basin.angle_signature,
        contact_count=basin.contact_count,
    )


if __name__ == "__main__":
    sys.exit(main())
