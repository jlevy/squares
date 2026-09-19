# n=21 97/20 T-021-Seeded Auto Window-6 Covering Receipt

Status: **site set still open, unconverged**. The side stays open.
No freeze.

Session-140 rank-6 probe: BC-191 auto `(34, 45, 56)` unioned with T-021’s atom sites at
`97/20`, plus `--seed-windows 6`,
`(n, L, B, net) = (21, 97/20, 9977/10000, 181 directions)`. Seed from the live n=20
`certificate.json` (T-021). Seed sites 2256. The 1200 s deadline stopped the row loop
after 45 LP rounds at `19.814820` (162 still violated).
The objective sat on `19.814820` from round 39. It did not cross 21.

This is a covering measurement at the already-verified T-021 side, not a floor raise.
Remaining rows can only raise the restricted optimum.
Adding sites can still lower it.
T-021 is unchanged. T-029 was not offered.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 21 --side 97/20 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-certificate cases/n20_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 6 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-038/n21-97-20-t021-auto-windows6-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-038/n21-97-20-t021-auto-windows6-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-038/n21-97-20-t021-auto-windows6-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n21-97-20-t021-auto-windows6-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n21-97-20-t021-auto-windows6.log
```

No freeze file: the 1200 s deadline stopped the row loop after 45 rounds.
Wall 1227.8 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `19.814820` |
| Sites / orbits / rows | 7197 / 950 / 11277 |
| Seed sites | 2256 |
| LP rounds | 45 |
| Crossing | none |
| Wall | 1227.8 s |
| `least_covered` | 0.984206 |
| Converged | no (`violated == 162` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 21.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
