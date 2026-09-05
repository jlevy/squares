#!/usr/bin/env python3
"""The accepted production helpers independently corroborate exp-045's -W obstruction.

The exp-045 certificate was produced by `cases/n5/minus_w_obstruction.py`, which grew out
of the exp-043 draft and does not call the accepted row-jet, stress, scale, and owner-4
helpers -- the ones exp-045's first admission condition names. Until 2026-08-31 those
helpers had run only on the exp-036 `+W` control, per their admitted scope, so the
condition was satisfiable in spirit but not demonstrably satisfied. The independent
audit closed that gap by running them on the actual `-W` direction, and this check
replays that bridge so it cannot rot:

- for each registered stratum, the negation of the production `W` equals the retained
  certificate's `canonical_minus_W`, coefficient by coefficient in `Q(sqrt 2)`;
- `minus_w_owner4.owner4_record` on `-W` yields a strictly negative constant that is
  independent of the arbitrary correction (checked with two different corrections) and
  equal to its `+W` twin;
- `minus_w_scale.scale_records` on `-W` builds all five routes per stratum -- fifteen
  records in all -- with every bounded correction coefficient and the beta coefficient
  exactly zero, the deciding constant strictly negative, both cusp coefficients strictly
  negative, and every coefficient equal to its `+W` twin (the sign-symmetry
  determination, derived here rather than read from the certificate);
- the shared deciding constant's magnitude equals the certificate's retained
  `obstruction_coefficient`, tying the two implementations to one number.

Agreement here is two independently written implementations deciding the same exact
question the same way. It does not enlarge exp-045's claim boundary by anything: one
direction, three poses, no nonlinear realization, no H-023 disposition.

Gate coverage is `tests/test_minus_w_bridge.py`, which replays this check inside the
behavioral test step; there is deliberately no separate validation step, because the
check costs about 75 seconds and a named step would run the same arithmetic twice per
gate.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_minus_w_bridge
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from cases.n5 import minus_w_owner4, minus_w_scale, tangent_cones, tangent_inventory
from sqpack.field import NumberField

ROOT = Path(__file__).resolve().parent.parent
CERTIFICATE = (
    ROOT
    / "campaign/series/series-000-smoke-and-calibration/results"
    / "exp-045-h-023-n5-minus-w-scale-and-controls.json"
)


def main() -> int:
    field = NumberField((1, 0, -2), (1, 2))
    retained = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    cases = {
        (case["stratum"], case["owner"]): case for case in retained["certificate"]["cases"]
    }

    def element(pair: list[str]):
        rational, root = pair
        return field.rational(Fraction(rational)) + field.rational(Fraction(root)) * field.alpha

    zero = tuple(field.zero for _ in range(tangent_cones.VARIABLE_COUNT))
    probe = tuple(field.rational(index - 7) for index in range(tangent_cones.VARIABLE_COUNT))

    problems: list[str] = []
    scale_total = 0
    for stratum in tangent_cones.STRATA:
        plus_w = tuple(tangent_inventory.geometry_vectors(field, stratum)[0]["W"])
        minus_w = tuple(-component for component in plus_w)

        retained_minus = [
            element(pair) for pair in cases[(stratum, "owner3:a+")]["canonical_minus_W"]
        ]
        if any(x != y for x, y in zip(minus_w, retained_minus, strict=True)):
            problems.append(f"{stratum}: -W disagrees with the retained canonical_minus_W")
            continue

        owner4_zero = minus_w_owner4.owner4_record(field, stratum, minus_w, zero)
        owner4_probe = minus_w_owner4.owner4_record(field, stratum, minus_w, probe)
        owner4_plus = minus_w_owner4.owner4_record(field, stratum, plus_w, zero)
        if owner4_zero.constant != owner4_probe.constant:
            problems.append(f"{stratum}: owner-4 constant depends on the correction")
        if owner4_zero.constant.sign() >= 0:
            problems.append(f"{stratum}: owner-4 constant is not strictly negative")
        if owner4_zero.constant != owner4_plus.constant:
            problems.append(f"{stratum}: owner-4 constants differ between +W and -W")

        obstruction = element(
            list(cases[(stratum, "owner3:a+")]["certificate"]["obstruction_coefficient"])
        )
        if owner4_zero.constant != -obstruction:
            problems.append(
                f"{stratum}: helper constant does not match the retained "
                "obstruction_coefficient"
            )

        minus_records = minus_w_scale.scale_records(field, stratum, minus_w, zero)
        plus_records = minus_w_scale.scale_records(field, stratum, plus_w, zero)
        for minus_record, plus_record in zip(minus_records, plus_records, strict=True):
            scale_total += 1
            key = f"{stratum}/{minus_record.key}"
            affine = minus_record.bounded_affine
            if any(not g.is_zero() for g in affine.correction_coefficients):
                problems.append(f"{key}: a bounded correction coefficient is nonzero")
            if not affine.beta_coefficient.is_zero():
                problems.append(f"{key}: the beta coefficient is nonzero")
            if affine.constant.sign() >= 0:
                problems.append(f"{key}: the deciding constant is not strictly negative")
            if affine.constant != plus_record.bounded_affine.constant:
                problems.append(f"{key}: bounded constants differ between +W and -W")
            cusp = minus_record.unbounded_cusp
            if cusp.kappa_positive.sign() >= 0 or cusp.kappa_negative.sign() >= 0:
                problems.append(f"{key}: a cusp coefficient is not strictly negative")
            if (cusp.kappa_positive, cusp.kappa_negative) != (
                plus_record.unbounded_cusp.kappa_positive,
                plus_record.unbounded_cusp.kappa_negative,
            ):
                problems.append(f"{key}: cusp coefficients differ between +W and -W")

    if scale_total != 15 and not problems:
        problems.append(f"{scale_total} scale records built, expected 15")

    if problems:
        print(f"{len(problems)} bridge disagreements between the helpers and exp-045:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print(
        "production helpers corroborate exp-045: 15 owner-3 scale records and 3 owner-4 "
        "records obstruct -W at every stratum, with +W/-W coefficients equal"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
