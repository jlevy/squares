# sqcheck: the lab's independent square-packing checker

`sqcheck.py` decides whether n unit squares fit, with disjoint interiors, in [0, s]². It was written from scratch on
2026-11-02 and shares no code with the Squares Project's checkers or with any finder we build. That keeps the lab's
rule intact: nothing counts until code that didn't find it re-checks it.

```
python3 sqcheck.py WITNESS.yaml|json [...]   [--json] [--dps 60]
python3 run_tests.py                         # 100 known-best witnesses + 300 mutations + controls (~20 s)
```

Deps: `mpmath`, `sympy`, `pyyaml` (the Mac mini venv `~/AI_Projects/square-packing/.venv` has them).

## Verdicts

| Exit | Verdict | Meaning |
|---|---|---|
| 0 | `VALID` | Exact arithmetic (rationals or Q(α)). Every containment and separation inequality is decided exactly, touching included. |
| 0 | `CERTIFIED s<=S'` | Decimal angles, so cos/sin are irrational. Checked with outward-rounded interval arithmetic. A tight packing can't be decided at its own side, so the centres are dilated by (1+λ), which makes every tight contact strict, and the check proves the packing fits in side S' = s(1+λ). λ is 1e-24 for every published witness. |
| 1 | `INVALID` | A violation was proved: an overlap, a wall crossing, a non-unit square, or the wrong count. |
| 2 | `UNDECIDED` | Interval mode couldn't decide even after dilation. |
| 3 | `MALFORMED` | Bad input: for example a reducible minimal polynomial, or an isolating interval that holds no root or more than one. |

## Method

- **Containment:** c ± (|u_x|+|v_x|)/2 lies in [0, s] in each axis.
- **Separation:** the separating-axis theorem over the four edge normals of a pair, with closed half-planes. If all four margins are strictly negative, the interiors overlap.
- **Pre-filter:** pairs whose centres are more than √2 apart are skipped, decided exactly.
- **Q(α):** zero is decided symbolically, using an irreducible minimal polynomial and the degree < d power basis. Nonzero signs come from exact rational interval Horner, refining α's isolating interval by bisection.

## Input

The Squares Project's Witness/v2 layout, in YAML or JSON. Representations: `corners`, `center-angle` (degrees or
radians) and `center-basis` (cos, sin). Scalars: rational, decimal or algebraic-number-field. Our own finders write the
same layout, usually `center-angle` with `angle_unit: radians` and decimal strings. To claim an exact `VALID` instead
of `CERTIFIED`, a finder rationalises its angles to half-angle tangents t, with basis ((1−t²)/(1+t²), 2t/(1+t²)).

## Tested (run_tests.py, `test-output.txt`)

- **All 100 known-best witnesses for n = 1..100** from jlevy/squares @2f701c27: 64 rational, 2 over Q(√2) or a degree-5
  field, and 34 decimal. All are VALID or CERTIFIED, and every certified side matches `table.csv` to 1e-9.
- **Three mutations of every witness, each required to fail:** the side shrunk by 1e-7 relative, the centres compressed
  by 1e-6, and one square duplicated. All 300 fail as required.
- **Controls:**
  - the project's overlap negative control gives INVALID;
  - a single square rotated 45° in a side-√2 box (exact over Q(√2)) gives VALID;
  - our own radians/JSON format gives CERTIFIED at √2 and INVALID at 1.4142.

The tests pass on kenan-server and on the Mac mini (Python 3.14 venv).

Covered by these tests: n = 10, 11, 17, 18, 19 and every other n ≤ 100, at the published coordinates.
