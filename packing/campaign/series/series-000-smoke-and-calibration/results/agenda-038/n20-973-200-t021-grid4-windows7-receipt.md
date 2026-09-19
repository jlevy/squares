# n=20 973/200 T-021-Seeded Four-Grid Window-7 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-140 rank-1 probe: four-grid `(34, 46, 56, 64)` unioned with T-021's
atom sites scaled from `97/20` to `973/200`, plus `--seed-windows 7`,
`(n, L, B, net) = (20, 973/200, 9977/10000, 181 directions)`.
Seed from the live `certificate.json` (T-021 at `97/20`). Seed sites 2464.
The 1200 s deadline stopped the row loop after 34 LP rounds at `19.930198`
(492 still violated). It did not cross twenty. H-062's certificate-seeded
construction at this side crossed at `20.000223` on the same round count.
Remaining rows can only raise this value, so `19.930198` is not a covering
below 20. Adding sites, or more wall, can still lower it. T-021 is unchanged.
T-028 was not offered.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 20 --side 973/200 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 34,46,56,64 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-certificate cases/n20_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 7 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7.log
```

No freeze file: the 1200 s deadline stopped the row loop after 34 rounds.
Wall 1212.1 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `19.930198` |
| Sites / orbits / rows | 12676 / 1646 / 12984 |
| Seed sites | 2464 |
| LP rounds | 34 |
| Crossing | none |
| Wall | 1212.1 s |
| `least_covered` | 0.978980 |
| Converged | no (`violated == 492` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 20.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
