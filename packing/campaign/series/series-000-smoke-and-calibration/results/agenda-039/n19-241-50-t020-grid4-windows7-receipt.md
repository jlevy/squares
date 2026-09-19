# n=19 241/50 T-020 Four-Grid Window-7 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-177: T-020 seed from `certificate-24-5.json` plus four-grid
`(34, 45, 56, 64)` plus `--seed-windows 7`,
`(n, L, B, net) = (19, 241/50, 9977/10000, 181 directions)`. Seed sites 3044.
The 1200 s deadline stopped the row loop after 34 LP rounds at `19.224565`
(387 still violated). It crossed 19 at round 13 (`19.006821`). Closer than
leftover auto plus windows 6 at this side (`19.247109`).

Remaining rows can only raise this value, so `19.224565` is not a covering
below 19.
Do not more-wall this set. T-020 stands. T-030 was not offered. H-218 stays
unconfirmed.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 19 --side 241/50 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 34,45,56,64 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-windows 7 --seed-certificate cases/n20_fractional_certificate/certificate-24-5.json \
  --seed-map scale \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n19-241-50-t020-grid4-windows7-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n19-241-50-t020-grid4-windows7-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n19-241-50-t020-grid4-windows7-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n19-241-50-t020-grid4-windows7-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n19-241-50-t020-grid4-windows7.log
```

No freeze file: the 1200 s deadline stopped the row loop after 34 rounds.
Wall 1256.8 s. The walker then started n=12 `793/200` T-017 four-grid plus
windows 7 as exp-178.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `19.224565` |
| Sites / orbits / rows | 13153 / 1724 / 11500 |
| Seed sites | 3044 |
| Grids | `(34, 45, 56, 64)` |
| LP rounds | 34 |
| Crossing | round 13 (`19.006821`) |
| Wall | 1256.8 s |
| `least_covered` | 0.963656 |
| Converged | no (`violated == 387` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 19.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
