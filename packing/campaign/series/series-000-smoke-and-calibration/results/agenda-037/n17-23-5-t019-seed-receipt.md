# n=17 23/5 T-019-Seeded Covering Receipt

Status: **site set refuted, unconverged**. The side stays open.

Session-139 probe: BC-191 auto `(32, 42, 52)` unioned with T-019's 1184 atom
sites scaled from `459/100` to `23/5`,
`(n, L, B, net) = (17, 23/5, 9977/10000, 181 directions)`.
The unseeded auto grid stopped at `17.331710` after 300 s. The seed dropped
that to `17.049597` at the 600 s deadline (40 LP rounds, 183 still violated).
Crossed seventeen at round 16 (`17.002464`). Remaining rows can only raise
this value. Adding sites can still lower it, so `23/5` is not barred.
T-019 at `459/100` is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 17 --side 23/5 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 32,42,52 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 600 \
  --seed-certificate cases/n17_fractional_certificate/certificate.json --seed-map scale \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-seed-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-seed-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-seed.log
```

`--freeze-family` was not requested. The 600 s deadline stopped the row loop
after 40 rounds; no column-generation round ran. Wall 628.0 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `17.049597` |
| Sites / orbits / rows | 6668 / 873 / 11189 |
| Seed sites | 1184 |
| LP rounds | 40 |
| Crossing | round 16 (`17.002464`) |
| Wall | 628.0 s |
| `least_covered` | 0.993656 |
| Converged | no (`violated == 183` at stop) |

`devtools.decide_certificate` was not run: the mass is not below 17.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
