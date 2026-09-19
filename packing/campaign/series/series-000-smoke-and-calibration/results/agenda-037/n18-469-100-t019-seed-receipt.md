# n=18 469/100 T-019-Seeded Covering Receipt

Status: **site set refuted, unconverged**. Locked at 18. The side stays open.

Session-139 probe: BC-191 auto `(32, 43, 53)` unioned with T-019's 1184 atom
sites scaled from `459/100` to `469/100`,
`(n, L, B, net) = (18, 469/100, 9977/10000, 181 directions)`.
The same seed certified `467/100` as T-027. Here the row loop sat at
`18.000000` from round 8 through the 900 s deadline (59 LP rounds, 288
still violated) on 6853 sites / 920 orbits. Remaining rows can only raise
this value. Adding sites can still lower it, so `469/100` is not barred.
T-027 at `467/100` is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 18 --side 469/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 32,43,53 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n17_fractional_certificate/certificate.json --seed-map scale \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-469-100-t019-seed-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-469-100-t019-seed-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-469-100-t019-seed-log.log
```

`--freeze` was not requested. The 900 s deadline stopped the row loop
after 59 rounds; no column-generation round ran. Wall 921.5 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `18.000000` |
| Sites / orbits / rows | 6853 / 920 / 17282 |
| Seed sites | 1184 |
| LP rounds | 59 |
| Crossing | round 8 (`18.000000`) |
| Wall | 921.5 s |
| `least_covered` | 0.981532 |
| Converged | no (`violated == 288` at stop) |

`devtools.decide_certificate` was not run: the mass is not below 18.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
