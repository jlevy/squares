# H-216 n=6 299/100 Sites2 Freeze Receipt

Status: **open**. Neither confirmation nor refutation.

This run is calibration of the helper-free point-atom language at n=6. It is not an n=11
bound, and it does not move `s(6) = 3`.

[H-216](../../../../hypotheses/H-216-point-certificate-at-n6-299-100.md) asks whether a
helper-free point-atom certificate exists at `(n, L, B, net) = (6, 299/100, 9977/10000,
181 directions)` on some named site set.
Confirm only with a frozen covering of mass strictly below 6 that both routes of
`devtools.decide_certificate` accept.
Kill only with an exact depth-one family of total at least 6 that
`devtools.independent_ceiling_reader` and `sqpack.fractional.ceiling.verify_ceiling`
both accept. A float LP, an incomplete row set, a stalled interval route, or the attic
scratch numbers `83/14` and `6.006571` decide neither direction.

The first freeze on auto grids `(18, 24, 29)` gave covering `76027/12500` = 6.08216 and
does not confirm. This receipt is a second named site set on the same `(n, L, B, net)`.
It does not re-run polish or either ceiling reader on that first family.

## Site Set

BC-191 auto grids at densities `17/2`, `23/2`, `57/4` plus one extra density `67/4`,
inset `1/2`, on container side `299/100` and square side `9977/10000`.
`site_counts_for_side` writes those four densities as grid counts `(18, 24, 29, 34)`.
The extra count `34` is also the count the same rule gives for density `413/25`, the
finest component of BC-191’s next measured three-grid rung.

`devtools.run_fractional_colgen` has no extra-density flag.
`--grid-counts` is the in-tree way to name the four-grid set.
It also has no arrangement-vertex site flag; `--seed-windows` seeds a ceiling-window
lattice, which is a different construction and was left at 0. No seed certificate.

Column generation then added seven site orbits, the same count the auto freeze added,
and stopped at the default `--column-rounds 8` still holding a negative reduced-cost
candidate. The covering is rows-complete on the frozen set.

| Stage | Orbits | Sites | Dual rows |
| --- | ---: | ---: | ---: |
| Round 0 | 393 | 2885 | 2522 |
| Freeze (round 7) | 400 | 2941 | 2797 |

`--support-cap 0` kept every positive dual row while pricing.
The freeze wrote 28 priced support rows.

## Freeze

Command, from `packing/`, wall 87.4 s, stopped `converged: every placement covers mass
1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 6 --side 299/100 --shrink 9977/10000 --direction-steps 181 --support-cap 0 \
  --grid-counts 18,24,29,34 \
  --max-rounds 40 --deadline-seconds 3600 \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-sites2-family.json \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-sites2-covering.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-sites2-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-sites2-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-sites2.log
```

The argv used `--deadline-seconds 3600`. The run stopped on convergence, not the
deadline.

## Covering

| Quantity | Value |
| --- | --- |
| Rationalised total mass | `151931/25000` = 6.07724 |
| Float LP objective | 6.076773566569485 |
| Atoms | 160 |
| `least_cell_mass` | null (no cell sweep) |
| Claimed mass `< 6` | no |

`devtools.decide_certificate` was not run.
The covering freeze exists, but its claimed mass is not strictly below 6, so it cannot
confirm H-216. The float objective and the rationalised mass without a two-route
decision are V0/C0 for the determination.

Relative to the auto freeze `76027/12500` = 6.08216, this four-grid covering is lower by
`123/25000` = 0.00492 and remains above 6.

## Dual Family

The freeze family carried 224 placements of total `6253/1029`. The in-run
`verify_ceiling` screen on the unpolished family reported max depth `1.186710` and
feasible total `5.120688` at 228440 vertices (35888 decided exactly).

Polish and both ceiling readers were not run on this family.
Covering mass is not below 6, so confirmation is already impossible.
Kill would need an exact depth-one family of total at least 6; the in-run screen is not
that object. `polish_ceiling_family` refuses a record that repeats a placement, and this
freeze writes axis-parallel squares as both `t = 0` and `t = 1`. There is no in-tree
flag on `run_fractional_colgen` that merges those writings before polish.

## Determination

H-216 remains **open**.

- Confirmation failed: this covering freeze has mass `151931/25000`, which is not below
  6, and `decide_certificate` was not invoked.
- Refutation was not attempted on this family.
  The in-run screen’s feasible total `5.120688` is below 6 and is not an exact depth-one
  verdict.
- The attic bracket `[83/14, 6.006571]` is still V0/C0 scratch and is not used here.
- The freeze family’s total `6253/1029` matches the site-set LP objective.
  It is not a language-wide lower bound: max depth on the unpolished family is above 1.

## Artifacts

Paths are under
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/`.

| File | SHA-256 |
| --- | --- |
| `h216-n6-299-100-sites2-family.json` | `5f1ee8e50ed328c4d93c1456550d5317ed7a5785cf1dfc2b38e543c6efd0b5be` |
| `h216-n6-299-100-sites2-covering.json` | `427dab186b37119b4e14dc0fb4d73c138720ca9dc536944689ed9911d16940a8` |
| `h216-n6-299-100-sites2-run.json` | `63c838860ed68e352f1f211f4231e9c6b7483e09c1e65a79241d520bfe5f214b` |

Companion logs: `h216-n6-299-100-sites2.log`, `h216-n6-299-100-sites2-rows.jsonl`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
