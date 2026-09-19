# n=20 243/50 T-021 Four-Grid Window-7 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-165: T-021 four-grid `(34, 46, 56, 64)` unioned with T-021's atom
sites from `certificate.json` scaled from `97/20` to `243/50`, plus
`--seed-windows 7`, `(n, L, B, net) = (20, 243/50, 9977/10000, 181 directions)`.
Seed sites 2464. The 1200 s deadline stopped the row loop after 36 LP rounds at
`19.887914` (459 still violated). It did not cross 20.

Remaining rows can only raise this value, so `19.887914` is not a covering below
20.
Do not more-wall this set. T-021 is unchanged. T-030 was not offered. H-218 stays
unconfirmed.

This mass is above the same four-grid at `971/200` (`19.857588`) and below leftover
auto plus windows 6 at `971/200` (`19.910044`).

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 20 --side 243/50 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 34,46,56,64 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-certificate cases/n20_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 7 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n20-243-50-t021-grid4-windows7-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n20-243-50-t021-grid4-windows7-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n20-243-50-t021-grid4-windows7-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n20-243-50-t021-grid4-windows7-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n20-243-50-t021-grid4-windows7.log
```

No freeze file: the 1200 s deadline stopped the row loop after 36 rounds.
Wall 1269.1 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `19.887914` |
| Sites / orbits / rows | 12676 / 1646 / 13250 |
| Seed sites | 2464 |
| LP rounds | 36 |
| Crossing | none |
| Wall | 1269.1 s |
| `least_covered` | 0.965974 |
| Converged | no (`violated == 459` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 20.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
