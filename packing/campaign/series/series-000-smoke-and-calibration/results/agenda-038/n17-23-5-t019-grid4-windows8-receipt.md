# n=17 23/5 T-019-Seeded Four-Grid Window-8 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-140 rank-3 probe: four-grid `(34, 45, 56, 64)` unioned with T-019's
atom sites scaled from `459/100` to `23/5`, plus `--seed-windows 8`,
`(n, L, B, net) = (17, 23/5, 9977/10000, 181 directions)`.
Seed sites 2208. The 1200 s deadline stopped the row loop after 46 LP rounds at
`17.120106` (237 still violated). It crossed 17 at round 19 (`17.036105`).
Session-139's best at this side remains the T-019-seeded auto plus windows 5
row at `17.042346`. Remaining rows can only raise this value, so `17.120106`
is not a covering below 17. Adding sites, or more wall, can still lower it.
T-019 is unchanged. T-028 was not offered.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 17 --side 23/5 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 34,45,56,64 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-certificate cases/n17_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 8 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-23-5-t019-grid4-windows8-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-23-5-t019-grid4-windows8-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-23-5-t019-grid4-windows8-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-23-5-t019-grid4-windows8-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-23-5-t019-grid4-windows8.log
```

No freeze file: the 1200 s deadline stopped the row loop after 46 rounds.
Wall 1215.7 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `17.120106` |
| Sites / orbits / rows | 12317 / 1611 / 16278 |
| Seed sites | 2208 |
| LP rounds | 46 |
| Crossing | round 19 (`17.036105`) |
| Wall | 1215.7 s |
| `least_covered` | 0.986645 |
| Converged | no (`violated == 237` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 17.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
