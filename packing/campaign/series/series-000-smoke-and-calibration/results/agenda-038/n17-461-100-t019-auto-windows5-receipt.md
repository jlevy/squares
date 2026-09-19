# n=17 461/100 T-019-Seeded Auto Window-5 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-140 leftover rank 2: BC-191 auto grids `(32, 43, 53)` unioned with T-019's
atom sites from `certificate.json` scaled from `459/100` to `461/100`, plus
`--seed-windows 5`, `(n, L, B, net) = (17, 461/100, 9977/10000, 181 directions)`.
Seed sites 1584. The 1200 s deadline stopped the row loop after 56 LP rounds at
`17.195968` (18 still violated). It crossed 17 at round 11 (`17.030928`) and sat
on `17.195968` from round 45. This side is `4.61`, one cent above `23/5`.
Remaining rows can only raise this value, so `17.195968` is not a covering below
17.
Adding sites, or more wall, can still lower it. T-019 is unchanged. T-029 was
not offered. H-218 stays unconfirmed.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 17 --side 461/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-certificate cases/n17_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 5 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-461-100-t019-auto-windows5-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-461-100-t019-auto-windows5-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-461-100-t019-auto-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-461-100-t019-auto-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-461-100-t019-auto-windows5.log
```

No freeze file: the 1200 s deadline stopped the row loop after 56 rounds.
Wall 1237.9 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `17.195968` |
| Sites / orbits / rows | 7253 / 975 / 14077 |
| Seed sites | 1584 |
| LP rounds | 56 |
| Crossing | round 11 (`17.030928`) |
| Wall | 1237.9 s |
| `least_covered` | 0.997823 |
| Converged | no (`violated == 18` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 17.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
