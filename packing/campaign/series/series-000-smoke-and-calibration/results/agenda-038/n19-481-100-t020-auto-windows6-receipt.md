# n=19 481/100 T-020-Seeded Auto Window-6 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-140 rank-4 probe: BC-191 auto grids `(34, 45, 56)` unioned with T-020's
atom sites from `certificate-24-5.json` scaled from `24/5` to `481/100`, plus
`--seed-windows 6`, `(n, L, B, net) = (19, 481/100, 9977/10000, 181 directions)`.
Seed sites 2836. The 1200 s deadline stopped the row loop after 37 LP rounds at
`19.132115` (333 still violated). It crossed 19 at round 16 (`19.000170`).
Closer than session-139's same construction at `97/20` (`19.808958`). Remaining
rows can only raise this value, so `19.132115` is not a covering below 19.
Adding sites, or more wall, can still lower it. T-020 is unchanged. T-028 was
not offered.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 19 --side 481/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 34,45,56 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-certificate cases/n20_fractional_certificate/certificate-24-5.json --seed-map scale \
  --seed-windows 6 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-481-100-t020-auto-windows6-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-481-100-t020-auto-windows6-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-481-100-t020-auto-windows6-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-481-100-t020-auto-windows6-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-481-100-t020-auto-windows6.log
```

No freeze file: the 1200 s deadline stopped the row loop after 37 rounds.
Wall 1226.9 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `19.132115` |
| Sites / orbits / rows | 8865 / 1172 / 10697 |
| Seed sites | 2836 |
| LP rounds | 37 |
| Crossing | round 16 (`19.000170`) |
| Wall | 1226.9 s |
| `least_covered` | 0.951466 |
| Converged | no (`violated == 333` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 19.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
