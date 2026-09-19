# n=20 971/200 T-021 Four-Grid Window-7 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-164: T-021 four-grid `(34, 46, 56, 64)` unioned with T-021's atom
sites from `certificate.json` scaled from `97/20` to `971/200`, plus
`--seed-windows 7`, `(n, L, B, net) = (20, 971/200, 9977/10000, 181 directions)`.
Seed sites 2464. The 2400 s deadline stopped the row loop after 48 LP rounds at
`19.857588` (225 still violated). The objective sat near `19.857` from round 41.
It did not cross 20.

Remaining rows can only raise this value, so `19.857588` is not a covering below
20.
Adding sites, or a thinner side on this four-grid class, can still lower it. T-021
is unchanged. T-030 was not offered. H-218 stays unconfirmed.

This mass is below the leftover auto plus windows 6 row at the same side
(`19.910044`) and below the same four-grid at `973/200` (`19.939212`).

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 20 --side 971/200 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 34,46,56,64 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 2400 \
  --seed-certificate cases/n20_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 7 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n20-971-200-t021-grid4-windows7-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n20-971-200-t021-grid4-windows7-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n20-971-200-t021-grid4-windows7-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n20-971-200-t021-grid4-windows7-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n20-971-200-t021-grid4-windows7.log
```

No freeze file: the 2400 s deadline stopped the row loop after 48 rounds.
Wall 2516.1 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `19.857588` |
| Sites / orbits / rows | 12676 / 1646 / 15378 |
| Seed sites | 2464 |
| LP rounds | 48 |
| Crossing | none |
| Wall | 2516.1 s |
| `least_covered` | 0.991565 |
| Converged | no (`violated == 225` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 20.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
