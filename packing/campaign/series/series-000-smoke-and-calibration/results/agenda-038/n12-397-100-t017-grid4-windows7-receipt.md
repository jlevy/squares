# n=12 397/100 T-017-Seeded Four-Grid Window-7 Covering Receipt

Status: **site set refuted, converged**. The side stays open.

Session-140 rank-2 probe: four-grid `(28, 38, 46, 54)` unioned with T-017's
atom sites scaled from `99/25` to `397/100`, plus `--seed-windows 7`,
`(n, L, B, net) = (12, 397/100, 9977/10000, 181 directions)`.
Seed sites 2533. The row loop converged after 36 LP rounds at `12.133391`
(0 violated). Freeze mass `48534459/4000000 = 12.13361475`, above twelve.
`decide_certificate` was not run. Adding sites can still lower the covering
value, so `397/100` is not barred. T-017 is unchanged. T-028 was not offered.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 12 --side 397/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 28,38,46,54 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-certificate cases/n12_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 7 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-397-100-t017-grid4-windows7-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-397-100-t017-grid4-windows7-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-397-100-t017-grid4-windows7-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-397-100-t017-grid4-windows7-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-397-100-t017-grid4-windows7.log
```

Freeze written; mass above 12. Wall 1078.8 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `12.133391` |
| Freeze mass | `48534459/4000000` |
| Sites / orbits / rows | 9685 / 1307 / 9678 |
| Seed sites | 2533 |
| Atoms | 1637 |
| LP rounds | 36 |
| Crossing | round 9 (`12.023202`) |
| Wall | 1078.8 s |
| `least_covered` | 1 |
| Converged | yes |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
