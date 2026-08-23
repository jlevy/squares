#!/usr/bin/env python3
"""Golden basin maps for the small proved cases, checked against mathematics.

    uv run python tools/golden_basins.py            # rebuild and compare
    uv run python tools/golden_basins.py --update   # accept the new map as golden

## Why this is not an ordinary golden test

A golden whose expected values are *whatever the code produced last time* is a
characterization test. It catches regressions and cannot tell you the code was ever
right — and against this project's actual failure history, where four of six soundness
defects pointed in the flattering direction, a golden captured from a wrong run is a
wrong answer with a checksum on it. [D-030](../defects.md) is the live example: twelve
interrupted descents recorded as twelve basins, with every structural invariant green.
A golden taken that morning would have frozen the bug.

So the committed file is the *diff surface*, and the assertions underneath it are
grounded in things that were true before this code existed:

* **Proved optimum.** `s(n)` is known for these `n`. Anneal-then-quench must land on
  it, and **no basin may lie below it** — that is a bug unconditionally, never a record.
* **Closed form.** A real optimum is an algebraic number of modest height; a stopping
  point is not. See [`sqpack.closed_form`](../sqpack/closed_form.py).
* **Independent validity.** Every basin is re-checked by `sqpack.verify`, through code
  the quench does not share (rule **R1**).
* **Reproducibility.** Fixed seeds, so the same map twice. The committed file is the
  assertion.

The first three are what a characterization golden cannot do.

## Two questions, deliberately not mixed

The first version of this file conflated them and produced a test that failed on luck.

* **Convergence** — *given a start in the optimum's basin, does the pipeline reach the
  optimum exactly?* That is a property of the tools, it is deterministic, and it MUST
  hold. Tested end to end: anneal to get near, quench to land, recognise the closed
  form, verify validity independently. A failure here is a bug.
* **Discovery** — *does uniform multistart find the optimum in N draws?* That is a
  property of the **landscape**, it is probabilistic, and it is exactly what `H-012` is
  registered to measure. Recorded as data, never asserted. At `n = 5` eight draws found
  it once in one seed block and not at all in another, which is a finding about basin
  rarity rather than a broken tool.

Asserting the second is how a gate starts failing for reasons nobody can act on.

## Stable and unstable fields

Sides are recorded to **12 decimals**, which is above the `polished` tier's own `1e-11`
noise floor ([D-021](../defects.md)): the golden records at the precision the tier
permits, so a cross-platform LP difference below the floor cannot fail the diff while a
real regression above it still does. Wall times, hostnames and dates are not recorded at
all — an unstable field that is normalised is still a field somebody has to think about,
and the cheapest way to keep a golden stable is to have less in it.
"""

from __future__ import annotations

import argparse
import difflib
import math
import random
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqpack.atlas import Atlas
from sqpack.canonical import canonical_key
from sqpack.closed_form import ClosedForm, recognise
from sqpack.quench import quench_bracket
from sqpack.verify import corners_from_poses, float_sign, verify_packing

sys.path.insert(0, str(Path(__file__).resolve().parent))

from perimeter_test import anneal

ROOT = Path(__file__).resolve().parent.parent
GOLDEN = ROOT / "golden" / "basin-maps.yaml"

# Cases small enough to census in gate time. Every one is PROVED, which is the point:
# the answer exists independently of anything here.
CASES: tuple[tuple[int, int], ...] = ((1, 3), (2, 3), (3, 4), (4, 4), (5, 6))

# The convergence ladder: proved cases the annealer can get near and the quench must
# then land exactly. This is the end-to-end pipeline test on answers that existed before
# any of this code did.
LADDER: tuple[int, ...] = (1, 2, 3, 4, 5, 9, 10)

SIDE_DECIMALS = 12
ORACLE_TOL = 1e-10
# The quench's own floor (D-021). Nothing here may claim a difference below it.
TIER_FLOOR = 1e-11


def proved_side(n: int) -> tuple[float, str] | None:
    """The proved `s(n)`, read from `frontier/` rather than retyped."""
    text = (ROOT / "frontier" / f"n-{n:03d}.md").read_text()
    d = yaml.safe_load(text.split("---\n")[1])["packing"]
    if d["status"] != "proved":
        return None
    return float(d["upper_bound"]["value"]), d["upper_bound"].get("exact_form") or ""


def form_key(form: ClosedForm | None) -> tuple[int, int, int, int] | None:
    """Closed forms compared as integers, not floats.

    `frontier/` stores `s(5)` as `2.70710678118654`, truncated 7.5e-15 below the true
    value. Comparing floats would need a tolerance chosen to hide that; comparing the
    recognised `(4 + √2)/2` needs none, because both round-trip to the same integers.
    """
    return None if form is None else (form.p, form.q, form.d, form.r)


def start(n: int, side: float, rng: random.Random):
    """A uniform multistart draw, in a box comfortably larger than the answer."""
    return (
        [rng.uniform(0.5, side - 0.5) for _ in range(n)],
        [rng.uniform(0.5, side - 0.5) for _ in range(n)],
        [rng.uniform(0, math.pi / 2) for _ in range(n)],
    )


def census(n: int, seeds: int) -> tuple[Atlas, dict[tuple[str, str], tuple]]:
    """Quench `seeds` uniform starts and store the endpoints. Returns (atlas, configs)."""
    proved = proved_side(n)
    box = (proved[0] if proved else math.ceil(math.sqrt(n))) + 0.6
    rng = random.Random(1000 + n)
    atlas = Atlas(n=n)
    configs: dict[tuple[str, str], tuple] = {}
    for seed in range(seeds):
        x, y, theta = start(n, box, rng)
        r = quench_bracket(x, y, theta, time_budget=90.0)
        key = canonical_key(r.x, r.y, r.theta, r.side)
        atlas.add(key, seed=seed, converged=r.converged)
        configs.setdefault((key.geometric, key.contact), (r.x, r.y, r.theta, r.side))
    return atlas, configs


def ladder() -> tuple[list[dict], list[str]]:
    """Anneal near the proved optimum, quench onto it, and check it landed.

    The end-to-end pipeline on answers that existed before this code: the engine has to
    find the right basin, the quench has to polish it to the exact value, the closed
    form has to agree with the proved one as integers, and `sqpack.verify` has to accept
    the packing through code the quench does not share.

    This is the CONVERGENCE half. It is deterministic and it must hold; whether uniform
    multistart would have found the same basin is the discovery half, and is measured
    rather than asserted.
    """
    rows: list[dict] = []
    problems: list[str] = []
    for n in LADDER:
        proved = proved_side(n)
        if proved is None:
            problems.append(f"n={n} is on the ladder but is not proved in frontier/")
            continue
        want = recognise(proved[0])

        seeded = anneal(n, seed=7)
        r = quench_bracket(seeded["x"], seeded["y"], seeded["t"], time_budget=90.0)
        got, gap = recognise(r.side), r.side - proved[0]

        report = verify_packing(
            corners_from_poses(*_normalised((r.x, r.y, r.theta, r.side))),
            r.side,
            sign=float_sign(ORACLE_TOL),
        )

        if not report.valid:
            problems.append(f"n={n}: the quenched packing is not valid to sqpack")
        if gap < -TIER_FLOOR:
            problems.append(
                f"n={n}: quench returned {r.side:.12f}, BELOW the proved "
                f"s({n}) = {proved[0]!r} by {-gap:.2e}. That is a bug, not a record."
            )
        elif form_key(got) != form_key(want):
            problems.append(
                f"n={n}: anneal+quench reached {got or f'{r.side:.12f}'} "
                f"(gap {gap:+.2e}), but the proved s({n}) is {want} ({proved[1]}). "
                "The pipeline did not converge onto a known answer."
            )
        rows.append(
            {
                "n": n,
                "proved": proved[1],
                "annealer_gap": round(seeded["best_side"] - proved[0], SIDE_DECIMALS),
                "after_quench": str(got) if got else round(r.side, SIDE_DECIMALS),
                "gap": float(f"{gap:.3e}"),
                "converged": r.converged,
                "valid": report.valid,
            }
        )
    return rows, problems


def build() -> tuple[dict, list[str]]:
    """The map, and every way it failed an oracle."""
    problems: list[str] = []
    cases = []
    rungs, ladder_problems = ladder()
    problems += ladder_problems

    for n, seeds in CASES:
        atlas, configs = census(n, seeds)
        proved = proved_side(n)
        best = min(b.side for b in atlas.basins)

        rows = []
        for basin in sorted(atlas.basins, key=lambda b: (b.side, b.geometric)):
            form = recognise(basin.side)
            # ORACLE 1: independent validity, through code the quench does not share.
            cfg = configs[(basin.geometric, basin.contact)]
            report = verify_packing(
                corners_from_poses(*_normalised(cfg)), cfg[3], sign=float_sign(ORACLE_TOL)
            )
            if not report.valid:
                problems.append(
                    f"n={n}: a stored basin at side {basin.side:.12f} is NOT a valid "
                    f"packing — {report.failures[0][0] if report.failures else 'unknown'}"
                )
            # ORACLE 2: nothing may sit below a proved optimum.
            if proved and basin.side < proved[0] - TIER_FLOOR:
                problems.append(
                    f"n={n}: a basin at {basin.side:.12f} lies BELOW the proved "
                    f"s({n}) = {proved[0]!r}. That is a bug, not a discovery."
                )
            rows.append(
                {
                    "side": round(basin.side, SIDE_DECIMALS),
                    "closed_form": str(form) if form else None,
                    "contacts": basin.contact_count,
                    "angle_classes": list(basin.angle_signature),
                    "quench_frequency": basin.quench_frequency,
                    "valid": report.valid,
                }
            )

        # NOT an oracle: whether uniform multistart HAPPENED to find the optimum is a
        # property of the landscape, not of the tools. Recorded below as
        # `found_optimum` and measured by the ladder instead.

        # ORACLE 4: a census whose quenches did not converge measured its own budget.
        converged = atlas.proposals - atlas.non_converged
        if converged * 2 < atlas.proposals:
            problems.append(
                f"n={n}: only {converged}/{atlas.proposals} quenches converged; "
                "this census measured the budget, not the landscape (D-030)"
            )

        cases.append(
            {
                "n": n,
                "proposals": atlas.proposals,
                "converged": converged,
                "distinct_basins": len(atlas.basins),
                "proved_optimum": proved[1] if proved else None,
                # DATA, not an assertion: whether these draws happened to land in the
                # optimum's basin. A property of the landscape (H-012), not of the tools.
                "found_optimum": bool(
                    proved and form_key(recognise(proved[0])) == form_key(recognise(best))
                ),
                "basins": rows,
            }
        )

    return {
        "golden": {
            "note": "Rebuilt by tools/golden_basins.py. Sides to 12 decimals, which is "
            "above the polished tier's 1e-11 floor (D-021).",
            "side_decimals": SIDE_DECIMALS,
            "convergence_ladder": rungs,
            "cases": cases,
        }
    }, problems


def _normalised(cfg):
    """Translate to the origin before containment is checked, as the perimeter does."""
    x, y, theta, _ = cfg
    half = [0.5 * (abs(math.cos(t)) + abs(math.sin(t))) for t in theta]
    lox = min(a - h for a, h in zip(x, half, strict=True))
    loy = min(b - h for b, h in zip(y, half, strict=True))
    return [a - lox for a in x], [b - loy for b in y], theta


def verify_stored() -> tuple[dict, list[str]]:
    """Re-check every mathematical oracle against the COMMITTED file, without re-running.

    The expensive part of a golden is regenerating it; the assertions are cheap, because
    the file already holds the sides. So the fast path re-derives the closed form of every
    stored side, compares it against the proved `s(n)` read from `frontier/`, and checks
    that no stored basin lies below a proved optimum -- in milliseconds, every run.

    What this DOES catch, and it is the thing worth catching every time: a golden edited
    to make a test pass. The oracles are mathematics, so the file cannot be adjusted into
    agreement with them.

    What it does NOT catch is a change in the tools that would produce a different map.
    Only regeneration reaches that, which is why `--deep` exists and why the runbook's
    handover gate requires it before an unattended night.
    """
    if not GOLDEN.exists():
        return {}, [f"no golden at {GOLDEN.relative_to(ROOT)}; run with --update"]
    doc = yaml.safe_load(GOLDEN.read_text())
    problems: list[str] = []

    for rung in doc["golden"]["convergence_ladder"]:
        n = rung["n"]
        proved = proved_side(n)
        if proved is None:
            problems.append(f"n={n}: on the ladder but not proved in frontier/")
            continue
        # The stored `after_quench` is either a closed form or a bare number; either way
        # it must name the proved value.
        want = recognise(proved[0])
        stored = str(rung["after_quench"])
        if want is not None and stored != str(want):
            problems.append(
                f"n={n}: the golden records the pipeline reaching {stored}, but the "
                f"proved s({n}) is {want}"
            )
        if rung["gap"] < -TIER_FLOOR:
            problems.append(
                f"n={n}: the golden records a side BELOW the proved optimum "
                f"(gap {rung['gap']:+.2e}). That is a bug, not a record."
            )
        if not rung["valid"]:
            problems.append(f"n={n}: the golden records an INVALID packing on the ladder")

    for case in doc["golden"]["cases"]:
        n = case["n"]
        proved = proved_side(n)
        for basin in case["basins"]:
            if proved and basin["side"] < proved[0] - TIER_FLOOR:
                problems.append(
                    f"n={n}: a stored basin at {basin['side']} lies BELOW the proved "
                    f"s({n}) = {proved[0]!r}"
                )
            if not basin["valid"]:
                problems.append(f"n={n}: a stored basin is recorded as an invalid packing")
            # The recorded closed form must still be the one the recogniser derives.
            derived = recognise(basin["side"])
            recorded = basin["closed_form"]
            if (str(derived) if derived else None) != recorded:
                problems.append(
                    f"n={n}: basin {basin['side']} is recorded as {recorded} but "
                    f"recognises as {derived}"
                )
    return doc, problems


def report_stored() -> int:
    """The fast path: oracles against the committed file, no re-running."""
    doc, problems = verify_stored()
    if problems:
        print("ORACLE FAILURES against the committed golden:")
        for problem in problems:
            print(f"  {problem}")
        print("GOLDEN BASIN CHECKS FAILED")
        return 1
    rungs = doc["golden"]["convergence_ladder"]
    basins = sum(len(c["basins"]) for c in doc["golden"]["cases"])
    print(
        f"  {len(rungs)} ladder rungs and {basins} stored basins agree with the proved "
        f"values, their closed forms and their recorded validity"
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--update", action="store_true", help="accept the rebuilt map")
    ap.add_argument(
        "--deep",
        action="store_true",
        help="regenerate by re-quenching and diff (slow); without it, the committed "
        "map's oracles are re-checked from stored values",
    )
    args = ap.parse_args()

    if not args.update and not args.deep:
        return report_stored()

    doc, problems = build()
    rendered = yaml.safe_dump(doc, sort_keys=False, width=100)

    print("  convergence ladder (anneal -> quench -> must land on the proved value):")
    for rung in doc["golden"]["convergence_ladder"]:
        mark = "ok  " if rung["valid"] else "X   "
        print(
            f"    {mark}n={rung['n']:>2}  annealer {rung['annealer_gap']:+.2e}  ->  "
            f"{rung['after_quench']}  gap {rung['gap']:+.1e}  "
            f"{'converged' if rung['converged'] else 'NOT CONVERGED'}"
        )
    print("\n  multistart census (discovery is measured, never asserted):")
    for case in doc["golden"]["cases"]:
        n = case["n"]
        marks = "".join("." if b["valid"] else "X" for b in case["basins"])
        print(
            f"  n={n:>2}  {case['distinct_basins']:>2} basins from "
            f"{case['proposals']:>2} proposals ({case['converged']} converged), "
            f"best {case['basins'][0]['closed_form'] or case['basins'][0]['side']}"
            f"  {'found optimum' if case['found_optimum'] else 'optimum not drawn'}  [{marks}]"
        )
        recognised = sum(1 for b in case["basins"] if b["closed_form"])
        print(f"        {recognised}/{len(case['basins'])} basins match a closed form")

    if args.update:
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(rendered)
        print(f"\nwrote {GOLDEN.relative_to(ROOT)}")
        if problems:
            print("\nBUT the oracles are still unhappy:")
            for p in problems:
                print(f"  {p}")
            return 1
        return 0

    if not GOLDEN.exists():
        print(f"\nno golden at {GOLDEN.relative_to(ROOT)}; run with --update", file=sys.stderr)
        return 1
    if GOLDEN.read_text() != rendered:
        print("\nGOLDEN DRIFT — the map changed. Review the diff before accepting:")
        diff = difflib.unified_diff(
            GOLDEN.read_text().splitlines(), rendered.splitlines(), "golden", "rebuilt", n=2
        )
        for line in list(diff)[:60]:
            print(f"  {line}")
        problems.append("the rebuilt map differs from the committed golden")

    if problems:
        print("\nORACLE FAILURES:")
        for p in problems:
            print(f"  {p}")
        print("GOLDEN BASIN CHECKS FAILED")
        return 1
    print("\nGOLDEN BASIN CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
