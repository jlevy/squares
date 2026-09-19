# n=17 23/5 T-019-Seeded Window-6 Lattice Covering Receipt

Status: **site set refuted, unconverged**. The side stays open.

Session-139 probe: BC-191 auto `(32, 42, 52)` unioned with T-019's 1184 atom
sites scaled from `459/100` to `23/5`, plus `--seed-windows 6`,
`(n, L, B, net) = (17, 23/5, 9977/10000, 181 directions)`.
Seed sites 1760 = 1184 T-019 plus 576 ceiling-window lattice sites.
The same grids with `--seed-windows 5` stopped at `17.042346` after 931.6 s.
Windows 6 finished slightly worse: `17.048472` at the 900 s deadline
(46 LP rounds, 54 still violated). Crossed seventeen at round 12
(`17.000000`) and sat there through round 18, then climbed. Remaining
rows can only raise this value. Adding sites can still lower it, so
`23/5` is not barred. T-019 at `459/100` is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 17 --side 23/5 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 32,42,52 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n17_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 6 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows6-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows6-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows6-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows6-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows6.log
```

No freeze file: the 900 s deadline stopped the row loop after 46 rounds.
Wall 920.4 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `17.048472` |
| Sites / orbits / rows | 7244 / 951 / 12899 |
| Seed sites | 1760 |
| LP rounds | 46 |
| Crossing | round 12 (`17.000000`) |
| Wall | 920.4 s |
| `least_covered` | 0.999569 |
| Converged | no (`violated == 54` at stop) |

`devtools.decide_certificate` was not run: the mass is not below 17.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
