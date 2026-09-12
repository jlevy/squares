#!/usr/bin/env python3
"""Which settings can HOLD a known optimum, which is a necessary condition for finding one.

Run backwards from the answer. A mechanism that cannot leave a retained record where it
found it can never converge on one, so this prunes the setting space cheaply and without
searching: start every run at the exact best-known packing, run the mechanism, and measure
how far it drifts.

The test earns its keep because it has already overturned a setting. Declared as exact
equalities, `n = 11`'s own fourteen contacts make Trump's packing a *repelling* fixed
point -- drift 0.0000 at 200 iterations, 0.0012 at 1,000 and 0.2839 at 4,000,
deterministically, since a run beginning at a fixed pose has no seed in it. Exact tangency
makes the constraint sets meet non-transversally, which is the degenerate case the 2025
flow-limit result excludes from its convergence theorems. Bands and a smaller relaxation
turn the same point into a sink.

Read a row as a veto, not an endorsement. Holding an optimum is necessary and nowhere near
sufficient: the trivial grid is held perfectly by every setting here and is the trap every
search falls into.

Usage, from `packing/`:
    uv run --frozen python -m devtools.map_optimum_stability --n 5 10 11 17 26
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from devtools.divide_and_concur import corners_of, pair_separation, violation
from devtools.known_structure import contact_edges, contact_kinds, record
from devtools.run_projection_ratchet import solve
from devtools.sweep_structure_hints import orientation_classes

SETTINGS: list[tuple[str, dict[str, Any]]] = [
    ("bare projection", {}),
    ("faces, band 0.02, weight 1", {"band": 0.02, "weight": 1.0, "rung": "faces"}),
    ("faces, band 0.02, weight 4", {"band": 0.02, "weight": 4.0, "rung": "faces"}),
    ("faces, band 0.02, weight 10", {"band": 0.02, "weight": 10.0, "rung": "faces"}),
    ("all contacts, band 0.02, weight 4", {"band": 0.02, "weight": 4.0, "rung": "all"}),
    ("all contacts, EQUALITY, weight 4", {"band": 0.0, "weight": 4.0, "rung": "all"}),
]
"""The settings worth vetoing. The last is the one already known to fail, kept as a
positive control: a row that reports it as stable means the harness is broken."""


def basin_radius(
    n: int,
    name: str,
    spec: dict[str, Any],
    *,
    beta: float,
    steps: int,
    slack: float = 1.005,
    rng_seed: int = 0,
) -> dict[str, Any]:
    """The largest perturbation a setting still pulls back to the record.

    A fixed-point test asks only whether a mechanism leaves an optimum alone. A *basin*
    test asks the question that matters for search: started near the answer, does it go
    there? A setting whose basin has radius zero can hold a record and can still never
    find one, because nothing but an exact hit would ever land in it.

    Perturbations grow until the run stops returning. The reported radius is the last one
    that came back to within a twentieth of a unit side.

    **`slack` is why this is not measured at the record's own side**, and the first version
    of this instrument was wrong for the lack of it. A best-known packing is tight: kick it
    by a hundredth and the squares overlap, and at the exact record side there is nowhere to
    put them, because the packing is essentially the only arrangement that fits. Every
    setting then reports no basin at all, including the ones that hold the record perfectly,
    and the measurement says only that the record is rigid -- which was already known. Giving
    the container a little room asks the question that matters instead: released nearby,
    does the mechanism go back?
    """
    poses, side = record(n)
    side = side * slack
    edges = contact_edges(poses)
    kinds = contact_kinds(poses)
    rung = spec.get("rung")
    contacts = None
    classes = None
    if rung == "faces":
        contacts = [e for e in edges if kinds.get(e) == "edge-edge"]
        classes = orientation_classes(edges, kinds, n)
    elif rung == "all":
        contacts = edges

    ia = np.array([e[0] for e in edges])
    ib = np.array([e[1] for e in edges])
    rng = np.random.default_rng(rng_seed)

    radius = 0.0
    detail: dict[str, Any] = {}
    for kick in (0.0, 0.01, 0.03, 0.06, 0.12, 0.25):
        returns = 0
        trials = 1 if kick == 0.0 else 3
        for trial in range(trials):
            start = poses.copy()
            if kick > 0:
                start = start + rng.normal(0, kick, poses.shape)
            out = solve(
                n,
                side,
                np.random.default_rng(rng_seed + trial),
                beta=beta,
                iters=steps,
                monotone=steps,
                band=float(spec.get("band", 0.02)),
                contact_weight=float(spec.get("weight", 1.0)),
                classes=classes,
                contacts=contacts,
                start=start,
            )
            back = float(np.abs(out.poses[:, :2] - poses[:, :2]).max())
            feasible = violation(out.poses, side) <= 1e-9
            if kick == 0.0:
                v = corners_of(out.poses)
                turn = np.mod(out.poses[:, 2] - poses[:, 2] + np.pi / 4, np.pi / 2) - np.pi / 4
                detail = {
                    "drift": back,
                    "turn_deg": float(np.degrees(np.abs(turn).max())),
                    "held": feasible,
                    "contacts_kept": int((np.abs(pair_separation(v[ia], v[ib])) < 0.03).sum()),
                }
            if back < 0.05 and feasible:
                returns += 1
        if returns == trials:
            radius = kick
        else:
            break

    return {
        "n": n,
        "setting": name,
        "beta": beta,
        "radius": radius,
        "contacts": len(edges),
        **detail,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, nargs="+", default=[5, 10, 11, 17])
    ap.add_argument("--beta", type=float, nargs="+", default=[0.1, 0.5])
    ap.add_argument("--steps", type=int, default=4000)
    ap.add_argument("--slack", type=float, default=1.005)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--json", action="store_true")
    o = ap.parse_args()

    rows = [
        basin_radius(n, name, spec, beta=beta, steps=o.steps, slack=o.slack)
        for n in o.n
        for name, spec in SETTINGS
        for beta in o.beta
    ]
    if o.out:
        o.out.write_text(json.dumps(rows, default=str), encoding="utf-8")
    if o.json:
        print(json.dumps(rows, default=str, sort_keys=True))
        return 0

    print(
        f"basin around the best-known packing, {o.steps} iterations per trial, "
        f"container at {o.slack:g} of the record"
    )
    print(
        f"{'n':>4} {'setting':>34} {'moved':>8} {'turned':>8} "
        f"{'holds':>6} {'basin':>7} {'contacts':>11}"
    )
    for r in rows:
        held = "yes" if r.get("held") else "NO"
        radius = f"{r['radius']:.2f}" if r["radius"] else "none"
        print(
            f"{r['n']:>4} {r['setting']:>34} {r.get('drift', 0):>8.4f} "
            f"{r.get('turn_deg', 0):>7.2f} {held:>6} {radius:>7} "
            f"{r.get('contacts_kept', 0):>4} of {r['contacts']:<3}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
