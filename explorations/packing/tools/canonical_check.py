#!/usr/bin/env python3
"""Gate check for basin identity: the invariances it claims, tested against real packings.

    uv run python tools/canonical_check.py

Three properties, each one a way the key could be wrong, and each checked on Trump's
`n = 11` packing rather than on a fixture invented to pass:

1. **Invariant** under all eight container symmetries and under square relabelling.
   If it is not, every basin count is inflated by up to a factor of eight.
2. **Stable** under a perturbation the quench undoes -- a configuration nudged off the
   optimum and quenched back must key identically. If it is not, the census counts noise
   as discovery and its curve never saturates.
3. **Discriminating**: genuinely different packings must key differently. A key that
   agrees with everything is not a key, and this is the direction that fails silently --
   a census whose keys all collide reports one basin and looks like fast saturation.

Property 3 is the one worth arguing about, so it is checked twice: against an
obviously different packing (the grid), and against the *hard* case -- the wrong-basin
`n = 11` configuration the annealer actually produced, which is the distinction the whole
campaign turns on.
"""

from __future__ import annotations

import json
import math
import random
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqpack.canonical import canonical_key
from sqpack.quench import quench_bracket


def trump() -> tuple[list[float], list[float], list[float], float]:
    """Trump's packing as floats.

    Via `tools/export_trump11.py`, which already converts the exact certificate's corner
    lists into centres and angles and asserts every edge is unit on the way. Writing that
    conversion a second time here is exactly the duplication the toolkit spec says is a
    design failure -- and it is geometry, which is the worst thing to have two copies of.
    """
    out = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent / "export_trump11.py")],
        capture_output=True,
        text=True,
        check=True,
    )
    d = json.loads(out.stdout)
    return d["x"], d["y"], d["t"], d["side"]


def grid(n_side: int) -> tuple[list[float], list[float], list[float], float]:
    """The trivial `m x m` grid: a different arrangement, for the discrimination test."""
    xs, ys = [], []
    for i in range(n_side):
        for j in range(n_side):
            xs.append(i + 0.5)
            ys.append(j + 0.5)
    return xs, ys, [0.0] * (n_side * n_side), float(n_side)


def archived_n11() -> tuple[list[float], list[float], list[float], float] | None:
    """The best `n = 11` configuration the annealer ever recorded, from exp-003.

    A real wrong-basin packing: `3.9144` against Trump's `3.8771`, which is the
    distinction the whole campaign turns on. If the key cannot separate these two, it
    cannot separate anything a census will hand it.
    """
    archive = Path(__file__).resolve().parent.parent / (
        "campaign/series/series-000-smoke-and-calibration/results/"
        "exp-003-baseline-n11-target.jsonl"
    )
    if not archive.exists():
        return None
    best = None
    for line in archive.read_text().splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if "x" in d and (best is None or d["best_side"] < best["best_side"]):
            best = d
    return None if best is None else (best["x"], best["y"], best["t"], best["best_side"])


def check(label: str, *, ok: bool, detail: str = "") -> bool:
    print(f"  {'ok  ' if ok else 'FAIL'}  {label}" + (f"  [{detail}]" if detail else ""))
    return ok


def main() -> int:
    passed = True
    x, y, theta, side = trump()
    base = canonical_key(x, y, theta, side)

    # 1. Container symmetry, applied HERE rather than via d4_images.
    #
    # The obvious version of this check asks d4_images for the images and keys each one
    # -- and cannot fail, because geometric_key minimises over the same function. A
    # negative control caught exactly that: deleting the reflections from d4_images left
    # this passing. So the transforms are written out independently below, and if the
    # two notions of "the container's symmetry group" ever disagree, this is what says so.
    def rot90(a, b, t):
        return b, [side - v for v in a], t

    def reflect(a, b, t):
        return [side - v for v in a], b, [-v for v in t]

    images, cur = [], (list(x), list(y), list(theta))
    for _ in range(4):
        images.append(cur)
        images.append(reflect(*cur))
        cur = rot90(*cur)
    keys = {canonical_key(ix, iy, it, side).geometric for ix, iy, it in images}
    passed &= check(
        "invariant under all 8 container symmetries",
        ok=keys == {base.geometric},
        detail=f"{len(keys)} distinct key(s) over {len(images)} independently built images",
    )

    rng = random.Random(20260823)
    order = list(range(len(x)))
    rng.shuffle(order)
    shuffled = canonical_key(
        [x[i] for i in order], [y[i] for i in order], [theta[i] for i in order], side
    )
    passed &= check(
        "invariant under square relabelling",
        ok=shuffled.geometric == base.geometric and shuffled.contact == base.contact,
        detail=f"permutation {order}",
    )

    # A quarter turn applied to one square must change nothing: a unit square is
    # invariant under it, so a key that noticed would be reading a coordinate rather
    # than a geometry.
    turned = list(theta)
    turned[0] += math.pi / 2
    passed &= check(
        "invariant under a quarter turn of one square",
        ok=canonical_key(x, y, turned, side).geometric == base.geometric,
    )

    # 2. Stability: perturb, quench back, key must match.
    nudged_x = [v + rng.uniform(-1e-4, 1e-4) for v in x]
    nudged_y = [v + rng.uniform(-1e-4, 1e-4) for v in y]
    result = quench_bracket(nudged_x, nudged_y, list(theta), time_budget=60.0)
    back = canonical_key(result.x, result.y, result.theta, result.side)
    verdict = base.agrees_with(back)
    passed &= check(
        "a perturbed-then-quenched copy keys as the same basin",
        ok=verdict in ("same", "same-arrangement-different-metric"),
        detail=f"{verdict}, gap to Trump {result.side - side:+.3e}",
    )

    # 3. Discrimination, twice.
    gx, gy, gt, gs = grid(4)
    other = canonical_key(gx, gy, gt, gs)
    passed &= check(
        "a different arrangement keys differently",
        ok=base.agrees_with(other) == "different",
        detail=f"n=11 rigid vs n=16 grid: {base.agrees_with(other)}",
    )

    # The discrimination that actually matters for a census: same `n`, both real, and
    # the two basins the campaign has spent ten rounds distinguishing by hand. Taken
    # from exp-003's archive rather than synthesised, because a fixture invented to pass
    # this check would prove nothing about the packings the census will meet.
    wrong = archived_n11()
    if wrong is None:
        passed &= check(
            "Trump's basin differs from the annealer's", ok=False, detail="no archive"
        )
    else:
        wx, wy, wt, wside = wrong
        found = canonical_key(wx, wy, wt, wside)
        passed &= check(
            "at the same n, the annealer's basin differs from Trump's",
            ok=base.agrees_with(found) == "different",
            detail=f"gap {wside - side:+.3e}, {found.contact_count} contacts "
            f"vs Trump's {base.contact_count}",
        )

    print(
        f"\n  Trump n=11: {base.contact_count} contacts, "
        f"angle classes {base.angle_signature}, geometric {base.geometric[:12]}…"
    )
    print("CANONICAL CHECKS PASSED" if passed else "CANONICAL CHECKS FAILED")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
