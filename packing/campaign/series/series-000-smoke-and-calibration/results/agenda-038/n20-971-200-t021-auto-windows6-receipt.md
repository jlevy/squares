# n=20 971/200 T-021-Seeded Auto Window-6 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-140 leftover rank 3: BC-191 auto grids `(34, 45, 56)` unioned with T-021's
atom sites from `certificate.json` scaled from `97/20` to `971/200`, plus
`--seed-windows 6`, `(n, L, B, net) = (20, 971/200, 9977/10000, 181 directions)`.
Seed sites 2256. The 1200 s deadline stopped the row loop after 48 LP rounds at
`19.910044` (6 still violated). The objective sat on `19.910044` from round 40.
It did not cross 20.

Remaining rows can only raise this value, so `19.910044` is not a covering below
20.
Adding sites, or more wall, can still lower it. T-021 is unchanged. T-029 was
not offered. H-218 stays unconfirmed.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 20 --side 971/200 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-certificate cases/n20_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 6 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-971-200-t021-auto-windows6-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-971-200-t021-auto-windows6-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-971-200-t021-auto-windows6-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-971-200-t021-auto-windows6-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-971-200-t021-auto-windows6.log
```

No freeze file: the 1200 s deadline stopped the row loop after 48 rounds.
Wall 1243.0 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `19.910044` |
| Sites / orbits / rows | 8285 / 1093 / 11818 |
| Seed sites | 2256 |
| LP rounds | 48 |
| Crossing | none |
| Wall | 1243.0 s |
| `least_covered` | 0.990063 |
| Converged | no (`violated == 6` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 20.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
